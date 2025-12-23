# Mall Session Order Update Flow - Technical Documentation

## Overview

The Mall Session Order Update Flow enables customers to modify their orders after initial creation, as long as the order hasn't been confirmed by the restaurant staff. This feature supports the multi-tenant food court ordering system where a single customer session can have orders from multiple restaurants (tenants).

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Mall Session** | A temporary session created when a customer scans a QR code, identified by a 5-character hash (e.g., "KUULO") |
| **Master Tab** | The main order aggregating all items, owned by the mall's manager tenant |
| **Tenant Tab (Slave Tab)** | Individual orders per restaurant, linked to the master tab via `master_tab_id` |
| **Brokerable** | Polymorphic relationship linking orders to their source (MallSession) |

### Business Rules

1. **Only CREATED status orders can be updated** - Once a tenant confirms an order, it cannot be modified
2. **Partial updates are supported** - If some tenant tabs are confirmed, only the CREATED ones are updated
3. **Products are matched by line_id or product_id** - Enables precise item targeting
4. **Quantity 0 deletes the item** - Setting quantity to 0 removes the product from the order
5. **Totals are recalculated automatically** - Subtotal and total_amount are updated after changes
6. **Notifications are sent to staff** - Restaurant staff receive real-time updates about order changes

---

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MALL ORDER UPDATE SYSTEM                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────┐                                                    │
│  │   FRONTEND LAYER    │                                                    │
│  │                     │                                                    │
│  │  ┌───────────────┐  │                                                    │
│  │  │ MallClient    │  │  React-Admin based customer ordering interface     │
│  │  │ TabsList      │  │  - Displays current orders                         │
│  │  │               │  │  - Enables quantity editing                        │
│  │  └───────┬───────┘  │  - Real-time WebSocket updates                     │
│  │          │          │                                                    │
│  │  ┌───────▼───────┐  │                                                    │
│  │  │ DASHMallClient│  │  Custom data provider for mall operations          │
│  │  │ DataProvider  │  │  - Injects mall_session and mall_id                │
│  │  │               │  │  - Maps resources to public API endpoints          │
│  │  └───────┬───────┘  │                                                    │
│  └──────────┼──────────┘                                                    │
│             │                                                                │
│             │ PUT /api/public/mall/tab/{id}                                  │
│             ▼                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        BACKEND LAYER                                 │    │
│  │                                                                      │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                   MallTabsController                         │    │    │
│  │  │  extends TabController                                       │    │    │
│  │  │  uses: MallTabCrudOperationsTrait                           │    │    │
│  │  │        MallTabNotificationsTrait                            │    │    │
│  │  │        MallTabHelpersTrait                                  │    │    │
│  │  └──────────────────────┬──────────────────────────────────────┘    │    │
│  │                         │                                           │    │
│  │           ┌─────────────┼─────────────┐                            │    │
│  │           │             │             │                            │    │
│  │           ▼             ▼             ▼                            │    │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                  │    │
│  │  │MallTabRequest│ │ _update()   │ │Notifications│                  │    │
│  │  │ Validation  │ │ Method      │ │  Service    │                  │    │
│  │  └─────────────┘ └─────────────┘ └─────────────┘                  │    │
│  │                                                                      │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        DATA LAYER                                    │    │
│  │                                                                      │    │
│  │  ┌───────────┐   ┌───────────┐   ┌───────────────┐                 │    │
│  │  │   Tab     │   │   Order   │   │  OrderItem    │                 │    │
│  │  │  (Master) │◄──┤           │◄──┤  (Products)   │                 │    │
│  │  └─────┬─────┘   └───────────┘   └───────────────┘                 │    │
│  │        │                                                            │    │
│  │        │ master_tab_id                                              │    │
│  │        ▼                                                            │    │
│  │  ┌───────────┐   ┌───────────┐   ┌───────────────┐                 │    │
│  │  │   Tab     │   │   Order   │   │  OrderItem    │                 │    │
│  │  │  (Tenant) │◄──┤           │◄──┤  (Products)   │                 │    │
│  │  └───────────┘   └───────────┘   └───────────────┘                 │    │
│  │                                                                      │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Database Schema (Relevant Tables)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATABASE RELATIONSHIPS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────┐         ┌─────────────────┐                           │
│   │  mall_sessions  │         │     tenants     │                           │
│   │                 │         │                 │                           │
│   │ id              │         │ id              │                           │
│   │ hash (5 chars)  │         │ name            │                           │
│   │ mall_id         │◄────────┤ mall_id (mgr)   │                           │
│   │ customer_name   │         │                 │                           │
│   │ mall_location   │         └────────┬────────┘                           │
│   │ status          │                  │                                    │
│   │ meta            │                  │                                    │
│   └────────┬────────┘                  │                                    │
│            │                           │                                    │
│            │ brokerable_id             │ tenant_id                          │
│            ▼                           ▼                                    │
│   ┌─────────────────┐         ┌─────────────────┐                           │
│   │      tabs       │         │     orders      │                           │
│   │                 │         │                 │                           │
│   │ id              │◄────────┤ tabable_id      │                           │
│   │ tenant_id       │────────►│ tenant_id       │                           │
│   │ status          │         │ brokerable_type │ (MallSession)             │
│   │ is_master_tab   │         │ brokerable_id   │────────────────┐          │
│   │ master_tab_id   │─┐       │ subtotal        │                │          │
│   │ brokerable_type │ │       │ total_amount    │                │          │
│   │ brokerable_id   │ │       │ discount_amount │                │          │
│   │ note            │ │       │ parent_order_id │─┐              │          │
│   └────────┬────────┘ │       └────────┬────────┘ │              │          │
│            │          │                │          │              │          │
│            │          │                │          │              │          │
│   ┌────────▼────────┐ │       ┌────────▼────────┐ │              │          │
│   │  tabs (slave)   │◄┘       │ order_products  │ │              │          │
│   │                 │         │                 │ │              │          │
│   │ master_tab_id   │         │ id              │ │              │          │
│   │ is_master_tab=0 │         │ order_id        │◄┘              │          │
│   │ tenant_id       │         │ product_id      │                │          │
│   │ status          │         │ quantity        │                │          │
│   └─────────────────┘         │ unit_price      │                │          │
│                               │ line_id         │                │          │
│                               │ note            │                │          │
│                               └─────────────────┘                │          │
│                                                                  │          │
│                               ┌──────────────────────────────────┘          │
│                               ▼                                             │
│                      (Points to mall_sessions.id)                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Update Flow Scenarios

### Scenario 1: Simple Quantity Update (All Tabs CREATED)

**Preconditions:**
- Customer has an active mall session
- Master tab status: CREATED
- All tenant tabs status: CREATED

**Flow:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCENARIO 1: SIMPLE QUANTITY UPDATE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   CUSTOMER                  FRONTEND                 BACKEND                 │
│   ────────                  ────────                 ───────                 │
│                                                                              │
│   ┌─────────────┐                                                           │
│   │ Edit Order  │                                                           │
│   │ Change Qty  │                                                           │
│   │ 1 → 3       │                                                           │
│   └──────┬──────┘                                                           │
│          │                                                                   │
│          │ Click Save                                                        │
│          ▼                                                                   │
│   ┌──────────────────────────────────────────────────────┐                  │
│   │ DASHMallClientDataProvider.update()                  │                  │
│   │                                                      │                  │
│   │ 1. Get mall_session from localStorage ("KUULO")      │                  │
│   │ 2. Get mall_id from systemValues                     │                  │
│   │ 3. Build products array with updated quantities      │                  │
│   │ 4. Inject mall_session and mall_id into payload      │                  │
│   │                                                      │                  │
│   └────────────────────────┬─────────────────────────────┘                  │
│                            │                                                 │
│                            │ PUT /api/public/mall/tab/36                     │
│                            │ {                                               │
│                            │   products: [{product_id: 26, quantity: 3}],   │
│                            │   mall_session: "KUULO",                        │
│                            │   mall_id: 1                                    │
│                            │ }                                               │
│                            ▼                                                 │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                      BACKEND PROCESSING                               │  │
│   │                                                                       │  │
│   │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│   │  │ 1. MallTabRequest Validation                                    │ │  │
│   │  │    - isUpdateRequest() → true (has route id)                    │ │  │
│   │  │    - Apply UPDATE rules (all fields optional)                   │ │  │
│   │  │    - Validation passes ✓                                        │ │  │
│   │  └─────────────────────────────────────────────────────────────────┘ │  │
│   │                              │                                        │  │
│   │                              ▼                                        │  │
│   │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│   │  │ 2. _update() Method                                             │ │  │
│   │  │                                                                 │ │  │
│   │  │    a. Load master tab (id=36) with relationships                │ │  │
│   │  │    b. Verify is_master_tab = true                               │ │  │
│   │  │    c. Check master status = CREATED ✓                           │ │  │
│   │  │    d. Load all tenant tabs (slave tabs)                         │ │  │
│   │  │                                                                 │ │  │
│   │  └─────────────────────────────────────────────────────────────────┘ │  │
│   │                              │                                        │  │
│   │                              ▼                                        │  │
│   │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│   │  │ 3. Build Products Lookup Map                                    │ │  │
│   │  │                                                                 │ │  │
│   │  │    incomingProductsMap = {                                      │ │  │
│   │  │      "line:line_1765249522339...": {product_id: 26, qty: 3},   │ │  │
│   │  │      "product:26": {product_id: 26, qty: 3}                    │ │  │
│   │  │    }                                                            │ │  │
│   │  │                                                                 │ │  │
│   │  └─────────────────────────────────────────────────────────────────┘ │  │
│   │                              │                                        │  │
│   │                              ▼                                        │  │
│   │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│   │  │ 4. Process Each Tenant Tab                                      │ │  │
│   │  │                                                                 │ │  │
│   │  │    FOR each tenantTab:                                          │ │  │
│   │  │      IF status != CREATED → skip with warning                   │ │  │
│   │  │      ELSE:                                                      │ │  │
│   │  │        FOR each orderItem in tenantTab.order.items:             │ │  │
│   │  │          Match by line_id OR product_id                         │ │  │
│   │  │          IF matched:                                            │ │  │
│   │  │            IF new quantity = 0 → DELETE item                    │ │  │
│   │  │            ELSE → UPDATE quantity                               │ │  │
│   │  │          Update note if provided                                │ │  │
│   │  │                                                                 │ │  │
│   │  │        Recalculate tenant order totals:                         │ │  │
│   │  │          subtotal = SUM(item.qty * item.unit_price)             │ │  │
│   │  │          total_amount = subtotal - discount_amount              │ │  │
│   │  │                                                                 │ │  │
│   │  └─────────────────────────────────────────────────────────────────┘ │  │
│   │                              │                                        │  │
│   │                              ▼                                        │  │
│   │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│   │  │ 5. Sync Master Tab Order                                        │ │  │
│   │  │                                                                 │ │  │
│   │  │    - Collect all items from all tenant orders                   │ │  │
│   │  │    - Update master order items to match                         │ │  │
│   │  │    - Recalculate master order totals                            │ │  │
│   │  │                                                                 │ │  │
│   │  └─────────────────────────────────────────────────────────────────┘ │  │
│   │                              │                                        │  │
│   │                              ▼                                        │  │
│   │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│   │  │ 6. Send Notifications (After DB Commit)                         │ │  │
│   │  │                                                                 │ │  │
│   │  │    FOR each updated tenantTab:                                  │ │  │
│   │  │      → WebSocket to staff: tenant.{id}.orders                   │ │  │
│   │  │      → FCM push to staff devices                                │ │  │
│   │  │                                                                 │ │  │
│   │  └─────────────────────────────────────────────────────────────────┘ │  │
│   │                                                                       │  │
│   └───────────────────────────────────────────────────────────────────────┘  │
│                            │                                                 │
│                            │ Response: Updated MallTabResource               │
│                            ▼                                                 │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │ Frontend receives updated data                                        │  │
│   │ - Refreshes order list                                                │  │
│   │ - Shows success toast                                                 │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Scenario 2: Partial Update (Some Tabs Confirmed)

**Preconditions:**
- Customer has orders from multiple restaurants
- Restaurant A: Tab status = CONFIRMED (already being prepared)
- Restaurant B: Tab status = CREATED (can still be modified)

**Flow:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCENARIO 2: PARTIAL UPDATE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   INITIAL STATE:                                                            │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   Master Tab (id=36)         Tenant Tab A (id=37)                  │   │
│   │   status: CREATED            status: CONFIRMED ← Can't modify      │   │
│   │   is_master_tab: true        master_tab_id: 36                     │   │
│   │   │                          tenant: "Pizza Place"                 │   │
│   │   │                          │                                     │   │
│   │   │                          └── Order Items:                      │   │
│   │   │                              - Pizza Margherita (qty: 2)       │   │
│   │   │                                                                │   │
│   │   │                          Tenant Tab B (id=38)                  │   │
│   │   │                          status: CREATED ← Can modify          │   │
│   │   └─────────────────────────►master_tab_id: 36                     │   │
│   │                              tenant: "Sushi Bar"                   │   │
│   │                              │                                     │   │
│   │                              └── Order Items:                      │   │
│   │                                  - California Roll (qty: 1)        │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   CUSTOMER REQUEST:                                                         │
│   "Change California Roll quantity from 1 to 3"                             │
│                                                                              │
│   PROCESSING:                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   1. Load master tab and all tenant tabs                           │   │
│   │                                                                     │   │
│   │   2. Process Tenant Tab A (Pizza Place):                           │   │
│   │      - Status = CONFIRMED                                          │   │
│   │      - SKIP with warning: "Products from Pizza Place skipped       │   │
│   │        because order is already CONFIRMED"                         │   │
│   │                                                                     │   │
│   │   3. Process Tenant Tab B (Sushi Bar):                             │   │
│   │      - Status = CREATED ✓                                          │   │
│   │      - Find California Roll by product_id or line_id               │   │
│   │      - Update quantity: 1 → 3                                      │   │
│   │      - Recalculate order totals                                    │   │
│   │                                                                     │   │
│   │   4. Sync master tab:                                              │   │
│   │      - Master order reflects both tenant orders                    │   │
│   │      - Totals updated                                              │   │
│   │                                                                     │   │
│   │   5. Return response with warnings:                                │   │
│   │      {                                                             │   │
│   │        "data": { ... updated master tab ... },                     │   │
│   │        "meta": {                                                   │   │
│   │          "partial_update": true,                                   │   │
│   │          "updated_products_count": 1,                              │   │
│   │          "skipped_products_count": 1,                              │   │
│   │          "warnings": [                                             │   │
│   │            "Products from Pizza Place skipped (CONFIRMED)"         │   │
│   │          ]                                                         │   │
│   │        }                                                           │   │
│   │      }                                                             │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Scenario 3: Product Deletion (Quantity = 0)

**Flow:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCENARIO 3: PRODUCT DELETION                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Customer sets quantity to 0 for "Extra Huevo"                             │
│                                                                              │
│   REQUEST PAYLOAD:                                                          │
│   {                                                                         │
│     "products": [                                                           │
│       { "product_id": 26, "quantity": 3, "line_id": "line_xxx" },          │
│       { "product_id": 87, "quantity": 0, "line_id": "line_yyy" }  ← DELETE │
│     ]                                                                       │
│   }                                                                         │
│                                                                              │
│   PROCESSING:                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   FOR each product in request:                                     │   │
│   │                                                                     │   │
│   │     IF quantity > 0:                                               │   │
│   │       orderItem.quantity = newQuantity                             │   │
│   │       orderItem.save()                                             │   │
│   │       LOG: "Updated order item quantity"                           │   │
│   │                                                                     │   │
│   │     ELSE IF quantity = 0:                                          │   │
│   │       orderItem.delete()                                           │   │
│   │       LOG: "Deleted order item"                                    │   │
│   │                                                                     │   │
│   │   THEN:                                                            │   │
│   │     Recalculate totals (deleted item excluded)                     │   │
│   │     Sync master order (remove deleted item from master)            │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Scenario 4: Update Blocked (Order Already Confirmed)

**Flow:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCENARIO 4: UPDATE BLOCKED                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Master Tab status = CONFIRMED                                             │
│                                                                              │
│   REQUEST: PUT /api/public/mall/tab/36                                      │
│                                                                              │
│   RESPONSE: 422 Unprocessable Entity                                        │
│   {                                                                         │
│     "message": "This order has already been confirmed and cannot be         │
│                 modified",                                                  │
│     "errors": {                                                             │
│       "message": ["tabs.mall_errors.order_already_confirmed"]               │
│     }                                                                       │
│   }                                                                         │
│                                                                              │
│   FRONTEND HANDLING:                                                        │
│   - Show error toast to customer                                            │
│   - Disable edit controls for this order                                    │
│   - Suggest creating a new order if needed                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Interactions

### Frontend Components

#### DASHMallClientDataProvider

**File:** `dash-frontend/apps/kitchntabs-mall/src/dash-extensions/config/DASHMallClientDataProvider.tsx`

**Responsibilities:**
- Map resources to public API endpoints (`tab` → `public/mall/tab`)
- Inject `mall_session` and `mall_id` into all requests
- Handle error responses and display appropriate messages

**Key Code:**

```typescript
// Resource mapping
const RESOURCE_PATH_MAP: Record<string, string> = {
    'tab': 'public/mall/tab',
    'stores': 'public/mall/stores',
    'products': 'public/mall/products',
};

// Update method
update: async (resource: string, params: any) => {
    const apiResource = mapResourceToApiPath(resource);
    const mall_id = getMallId();
    const mall_session = getSessionId();

    // Inject mall context
    const enhancedData = {
        ...params.data,
        mall_id,
        mall_session,
    };

    return genericDataProvider.update(apiResource, { 
        ...params, 
        data: enhancedData 
    });
}
```

#### MallClientAppResources

**File:** `dash-frontend/packages/kt-mall/src/MallClientAppResources.tsx`

**Responsibilities:**
- Define resource configuration for mall client
- Handle form submission and validation
- Process errors and trigger customer data modal

**Key Configuration:**

```typescript
{
    model: "tab",
    mutationMode: "pessimistic",
    saveButtonAlwaysEnabled: true,
    
    beforeSubmit(values) {
        // Inject customer data from localStorage
        const orderData = dashStorage.getItem('orderData');
        const { name, tableNumber } = orderData 
            ? JSON.parse(orderData) 
            : { name: null, tableNumber: null };

        if (!name || !tableNumber) {
            throw new Error("MISSING_SESSION_DATA");
        }

        values.customer_name = name;
        values.table_number = tableNumber;
        return values;
    },

    onError(mode, error) {
        if (mode === "create" && error.message === "MISSING_SESSION_DATA") {
            window.dispatchEvent(new CustomEvent('enter-public-order-data'));
            return;
        }
        throw error;
    },
}
```

---

### Backend Components

#### MallTabRequest

**File:** `dash-backend/domain/app/Http/Request/Mall/MallTabRequest.php`

**Responsibilities:**
- Validate incoming requests
- Distinguish between CREATE and UPDATE operations
- Apply appropriate validation rules

**Key Code:**

```php
protected function isUpdateRequest(): bool
{
    return $this->route('id') !== null || $this->has('id');
}

public function rules(): array
{
    // For UPDATE requests, all fields are optional
    if ($this->isUpdateRequest()) {
        return [
            'mall_id' => 'sometimes|integer|exists:malls,id',
            'mall_session' => 'sometimes|string|size:5',
            'customer_name' => 'nullable|string|max:255',
            'table_number' => 'nullable|string|max:50',
            'products' => 'sometimes|array',
            'products.*.product_id' => 'sometimes|integer|exists:products,id',
            'products.*.quantity' => 'sometimes|integer|min:0', // 0 = delete
            // ...
        ];
    }

    // For CREATE requests, require essential fields
    return [
        'mall_id' => 'required|integer|exists:malls,id',
        'mall_session' => 'required|string|size:5',
        'customer_name' => 'required|string|max:255',
        'products' => 'required|array|min:1',
        // ...
    ];
}
```

#### MallTabCrudOperationsTrait

**File:** `dash-backend/domain/app/Traits/Mall/MallTabCrudOperationsTrait.php`

**Responsibilities:**
- Implement `_update()` method for mall orders
- Match products by line_id or product_id
- Update tenant tab orders and sync to master
- Recalculate order totals

**Key Methods:**

| Method | Description |
|--------|-------------|
| `_update($request, $id, $item)` | Main update entry point |
| `updateTenantTabProducts($tenantTab, $products)` | Update items in tenant order |
| `syncMasterTabOrderFromTenants($masterTab, $tenantTabs)` | Sync master order from all tenants |

#### MallTabNotificationsTrait

**File:** `dash-backend/domain/app/Traits/Mall/MallTabNotificationsTrait.php`

**Responsibilities:**
- Send notifications when orders are updated
- Notify restaurant staff via WebSocket and FCM
- Persist notifications for offline retrieval

**Key Methods:**

| Method | Description |
|--------|-------------|
| `notifyTenantTabUpdated($tenantTab, $masterTab, $updatedProducts)` | Notify staff of order update |
| `notifyMallSessionOnOrderUpdate($masterTab, $tenantTabs)` | Notify customer of update |

---

## Notification Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NOTIFICATION FLOW ON UPDATE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ORDER UPDATE                                                              │
│        │                                                                     │
│        ▼                                                                     │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │               notifyTenantTabUpdated()                              │   │
│   │                                                                     │   │
│   │   Build notification data:                                         │   │
│   │   - event: "mall_order_updated"                                    │   │
│   │   - tenant_tab_id, tenant_id, tenant_name                          │   │
│   │   - master_tab_id                                                  │   │
│   │   - updated_products: [{ product_id, name, old_qty, new_qty }]     │   │
│   │   - timestamp                                                      │   │
│   │   - customer_info: { name, table }                                 │   │
│   │                                                                     │   │
│   └──────────────────────────┬──────────────────────────────────────────┘   │
│                              │                                               │
│              ┌───────────────┼───────────────┐                              │
│              │               │               │                              │
│              ▼               ▼               ▼                              │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│   │  WebSocket   │  │   Database   │  │  FCM Push    │                     │
│   │              │  │              │  │              │                     │
│   │  Channel:    │  │  Store in    │  │  Send to     │                     │
│   │  tenant.{id} │  │  mall_session│  │  staff       │                     │
│   │  .orders     │  │  _notifs     │  │  devices     │                     │
│   └──────┬───────┘  └──────────────┘  └──────┬───────┘                     │
│          │                                    │                             │
│          │                                    │                             │
│          ▼                                    ▼                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                    STAFF APP (KitchnTabs)                            │  │
│   │                                                                      │  │
│   │   ┌────────────────────────────────────────────────────────────┐    │  │
│   │   │  WebSocket Listener                                        │    │  │
│   │   │                                                            │    │  │
│   │   │  echo.private(`tenant.${tenantId}.orders`)                │    │  │
│   │   │    .listen('.mall_order_updated', (event) => {            │    │  │
│   │   │      showToast("Order #" + event.master_tab_id +          │    │  │
│   │   │                " updated by customer");                    │    │  │
│   │   │      refreshOrderList();                                   │    │  │
│   │   │    });                                                     │    │  │
│   │   │                                                            │    │  │
│   │   └────────────────────────────────────────────────────────────┘    │  │
│   │                                                                      │  │
│   │   Push Notification (if app in background):                         │  │
│   │   ┌────────────────────────────────────────────────────────────┐    │  │
│   │   │  🔔 Order Updated                                          │    │  │
│   │   │  Customer at Table 15 changed their order                 │    │  │
│   │   └────────────────────────────────────────────────────────────┘    │  │
│   │                                                                      │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Error Handling

### Error Types and Responses

| Error Code | Scenario | Response |
|------------|----------|----------|
| 422 | Order already confirmed | `tabs.mall_errors.order_already_confirmed` |
| 422 | Not a master tab | `tabs.mall_errors.not_master_tab` |
| 422 | Validation failed | Field-specific error messages |
| 404 | Tab not found | Standard 404 response |
| 500 | Database error | Generic error with logged details |

### Partial Update Warnings

When some products can't be updated (e.g., tenant already confirmed), the response includes warnings:

```json
{
    "data": { /* updated master tab */ },
    "meta": {
        "partial_update": true,
        "updated_products_count": 2,
        "skipped_products_count": 1,
        "warnings": [
            "Products from Pizza Place skipped because order is CONFIRMED"
        ],
        "message": "Some products could not be updated"
    }
}
```

---

## Sequence Diagrams

### Complete Update Sequence

```
┌────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐     ┌─────────┐
│Customer│     │ Frontend │     │  Backend  │     │ Database │     │  Staff  │
└───┬────┘     └────┬─────┘     └─────┬─────┘     └────┬─────┘     └────┬────┘
    │               │                 │                │                │
    │ Edit quantity │                 │                │                │
    │──────────────►│                 │                │                │
    │               │                 │                │                │
    │               │ PUT /tab/36     │                │                │
    │               │────────────────►│                │                │
    │               │                 │                │                │
    │               │                 │ BEGIN TX       │                │
    │               │                 │───────────────►│                │
    │               │                 │                │                │
    │               │                 │ Load master tab│                │
    │               │                 │───────────────►│                │
    │               │                 │◄───────────────│                │
    │               │                 │                │                │
    │               │                 │ Load tenant tabs                │
    │               │                 │───────────────►│                │
    │               │                 │◄───────────────│                │
    │               │                 │                │                │
    │               │                 │ Update items   │                │
    │               │                 │───────────────►│                │
    │               │                 │◄───────────────│                │
    │               │                 │                │                │
    │               │                 │ Recalc totals  │                │
    │               │                 │───────────────►│                │
    │               │                 │◄───────────────│                │
    │               │                 │                │                │
    │               │                 │ Sync master    │                │
    │               │                 │───────────────►│                │
    │               │                 │◄───────────────│                │
    │               │                 │                │                │
    │               │                 │ COMMIT TX      │                │
    │               │                 │───────────────►│                │
    │               │                 │◄───────────────│                │
    │               │                 │                │                │
    │               │                 │ Send WebSocket │                │
    │               │                 │────────────────────────────────►│
    │               │                 │                │                │
    │               │                 │ Send FCM Push  │                │
    │               │                 │────────────────────────────────►│
    │               │                 │                │                │
    │               │ Updated Tab     │                │                │
    │               │◄────────────────│                │                │
    │               │                 │                │                │
    │ Show success  │                 │                │                │
    │◄──────────────│                 │                │                │
    │               │                 │                │                │
    │               │                 │                │  Order updated! │
    │               │                 │                │◄───────────────│
    │               │                 │                │                │
```

---

## Testing Scenarios

### Unit Tests

| Test | Description |
|------|-------------|
| `test_update_quantity_success` | Verify quantity update when tab is CREATED |
| `test_update_blocked_when_confirmed` | Verify 422 when master tab is CONFIRMED |
| `test_partial_update_with_warnings` | Verify partial update when some tenants confirmed |
| `test_delete_product_with_zero_quantity` | Verify product deletion when qty=0 |
| `test_totals_recalculated_after_update` | Verify subtotal and total_amount updated |
| `test_master_synced_from_tenants` | Verify master order reflects tenant changes |

### Integration Tests

| Test | Description |
|------|-------------|
| `test_full_update_flow` | End-to-end update from frontend to database |
| `test_websocket_notification_sent` | Verify WebSocket event dispatched |
| `test_fcm_notification_sent` | Verify FCM push sent to staff |
| `test_concurrent_updates` | Verify handling of race conditions |

---

## Performance Considerations

1. **Database Transactions** - All updates wrapped in transaction to ensure consistency
2. **Eager Loading** - Tenant tabs loaded with orders and items in single query
3. **Batch Updates** - Multiple items updated in single pass per tenant
4. **Notification Queuing** - Notifications dispatched after commit to avoid blocking

---

## Security Considerations

1. **Session Validation** - Mall session hash validated on every request
2. **Status Check** - Only CREATED orders can be modified
3. **Tenant Isolation** - Users can only update their own session's orders
4. **Rate Limiting** - API rate limits prevent abuse

---

## Future Enhancements

1. **Optimistic Updates** - Show changes immediately, rollback on error
2. **Conflict Resolution** - Handle concurrent updates from multiple devices
3. **Undo Functionality** - Allow reverting recent changes
4. **Change History** - Track all modifications for audit trail
