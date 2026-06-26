
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

```mermaid
flowchart TD
    subgraph Frontend["FRONTEND LAYER"]
        MTL["MallClientTabsList<br/>React-Admin based customer ordering interface<br/>- Displays current orders<br/>- Enables quantity editing<br/>- Real-time WebSocket updates"]
        DP["DASHMallClientDataProvider<br/>Custom data provider for mall operations<br/>- Injects mall_session and mall_id<br/>- Maps resources to public API endpoints"]
        MTL --> DP
    end

    DP -->|"PUT /api/public/mall/tab/{id}"| Backend

    subgraph Backend["BACKEND LAYER"]
        MTC["MallTabsController<br/>extends TabController<br/>uses: MallTabCrudOperationsTrait, MallTabNotificationsTrait, MallTabHelpersTrait"]
        MTR["MallTabRequest Validation"]
        UPD["_update() Method"]
        NS["Notifications Service"]
        MTC --> MTR
        MTC --> UPD
        MTC --> NS
    end

    Backend --> DataLayer

    subgraph DataLayer["DATA LAYER"]
        TabMaster["Tab (Master)"]
        OrderMaster["Order"]
        OrderItemMaster["OrderItem (Products)"]
        TabTenant["Tab (Tenant)"]
        OrderTenant["Order"]
        OrderItemTenant["OrderItem (Products)"]

        OrderMaster --> TabMaster
        OrderItemMaster --> OrderMaster
        TabMaster -->|master_tab_id| TabTenant
        OrderTenant --> TabTenant
        OrderItemTenant --> OrderTenant
    end
```

### Database Schema (Relevant Tables)

```mermaid
erDiagram
    mall_sessions {
        int id
        string hash "5 chars"
        int mall_id
        string customer_name
        string mall_location
        string status
        json meta
    }
    tenants {
        int id
        string name
        int mall_id "mgr"
    }
    tabs {
        int id
        int tenant_id
        string status
        bool is_master_tab
        int master_tab_id
        string brokerable_type
        int brokerable_id
        string note
    }
    orders {
        int tabable_id
        int tenant_id
        string brokerable_type "MallSession"
        int brokerable_id
        decimal subtotal
        decimal total_amount
        decimal discount_amount
        int parent_order_id
    }
    order_products {
        int id
        int order_id
        int product_id
        int quantity
        decimal unit_price
        string line_id
        string note
    }

    tenants }o--|| mall_sessions : "mall_id (mgr)"
    mall_sessions ||--o{ tabs : "brokerable_id"
    tenants ||--o{ orders : "tenant_id"
    tabs ||--o{ orders : "tabable_id"
    tabs ||--o{ tabs : "master_tab_id (slave tabs)"
    orders ||--o{ order_products : "order_id"
    orders }o--|| orders : "parent_order_id"
    orders }o--|| mall_sessions : "brokerable_id"
```

---

## Update Flow Scenarios

### Scenario 1: Simple Quantity Update (All Tabs CREATED)

**Preconditions:**
- Customer has an active mall session
- Master tab status: CREATED
- All tenant tabs status: CREATED

**Flow:**

```mermaid
flowchart TD
    A["CUSTOMER: Edit Order, Change Qty 1 → 3"] -->|Click Save| B

    subgraph FE["FRONTEND"]
        B["DASHMallClientDataProvider.update()<br/>1. Get mall_session from localStorage ('KUULO')<br/>2. Get mall_id from systemValues<br/>3. Build products array with updated quantities<br/>4. Inject mall_session and mall_id into payload"]
    end

    B -->|"PUT /api/public/mall/tab/36<br/>{ products: [{product_id: 26, quantity: 3}], mall_session: 'KUULO', mall_id: 1 }"| C

    subgraph BE["BACKEND PROCESSING"]
        C["1. MallTabRequest Validation<br/>- isUpdateRequest() → true (has route id)<br/>- Apply UPDATE rules (all fields optional)<br/>- Validation passes"]
        D["2. _update() Method<br/>a. Load master tab (id=36) with relationships<br/>b. Verify is_master_tab = true<br/>c. Check master status = CREATED<br/>d. Load all tenant tabs (slave tabs)"]
        E["3. Build Products Lookup Map<br/>incomingProductsMap = {<br/>'line:line_1765249522339...': {product_id: 26, qty: 3},<br/>'product:26': {product_id: 26, qty: 3} }"]
        F["4. Process Each Tenant Tab<br/>FOR each tenantTab:<br/>IF status != CREATED → skip with warning<br/>ELSE: FOR each orderItem in tenantTab.order.items:<br/>Match by line_id OR product_id<br/>IF matched: IF new quantity = 0 → DELETE item ELSE → UPDATE quantity<br/>Update note if provided<br/>Recalculate tenant order totals:<br/>subtotal = SUM(item.qty * item.unit_price)<br/>total_amount = subtotal - discount_amount"]
        G["5. Sync Master Tab Order<br/>- Collect all items from all tenant orders<br/>- Update master order items to match<br/>- Recalculate master order totals"]
        H["6. Send Notifications (After DB Commit)<br/>FOR each updated tenantTab:<br/>→ WebSocket to staff: tenant.{id}.orders<br/>→ FCM push to staff devices"]
        C --> D --> E --> F --> G --> H
    end

    H -->|"Response: Updated MallTabResource"| I["Frontend receives updated data<br/>- Refreshes order list<br/>- Shows success toast"]
```

---

### Scenario 2: Partial Update (Some Tabs Confirmed)

**Preconditions:**
- Customer has orders from multiple restaurants
- Restaurant A: Tab status = CONFIRMED (already being prepared)
- Restaurant B: Tab status = CREATED (can still be modified)

**Flow:**

```mermaid
flowchart TD
    subgraph InitialState["INITIAL STATE"]
        Master["Master Tab (id=36)<br/>status: CREATED<br/>is_master_tab: true"]
        TabA["Tenant Tab A (id=37)<br/>status: CONFIRMED ← Can't modify<br/>master_tab_id: 36<br/>tenant: 'Pizza Place'<br/>Order Items: Pizza Margherita (qty: 2)"]
        TabB["Tenant Tab B (id=38)<br/>status: CREATED ← Can modify<br/>master_tab_id: 36<br/>tenant: 'Sushi Bar'<br/>Order Items: California Roll (qty: 1)"]
        Master --> TabA
        Master --> TabB
    end

    Request["CUSTOMER REQUEST:<br/>'Change California Roll quantity from 1 to 3'"]
    InitialState --> Request

    Request --> P1["1. Load master tab and all tenant tabs"]
    P1 --> P2["2. Process Tenant Tab A (Pizza Place):<br/>Status = CONFIRMED<br/>SKIP with warning: 'Products from Pizza Place skipped because order is already CONFIRMED'"]
    P2 --> P3["3. Process Tenant Tab B (Sushi Bar):<br/>Status = CREATED<br/>Find California Roll by product_id or line_id<br/>Update quantity: 1 → 3<br/>Recalculate order totals"]
    P3 --> P4["4. Sync master tab:<br/>Master order reflects both tenant orders<br/>Totals updated"]
    P4 --> P5["5. Return response with warnings:<br/>'data': updated master tab,<br/>'meta': { partial_update: true, updated_products_count: 1,<br/>skipped_products_count: 1,<br/>warnings: ['Products from Pizza Place skipped (CONFIRMED)'] }"]
```

---

### Scenario 3: Product Deletion (Quantity = 0)

**Flow:**

```mermaid
flowchart TD
    Start["Customer sets quantity to 0 for 'Extra Huevo'<br/>REQUEST PAYLOAD:<br/>products: [<br/>{ product_id: 26, quantity: 3, line_id: 'line_xxx' },<br/>{ product_id: 87, quantity: 0, line_id: 'line_yyy' } ← DELETE<br/>]"]
    Loop["FOR each product in request"]
    Check{"quantity > 0?"}
    Update["orderItem.quantity = newQuantity<br/>orderItem.save()<br/>LOG: 'Updated order item quantity'"]
    Delete["orderItem.delete()<br/>LOG: 'Deleted order item'"]
    Then["THEN:<br/>Recalculate totals (deleted item excluded)<br/>Sync master order (remove deleted item from master)"]

    Start --> Loop --> Check
    Check -->|Yes| Update --> Then
    Check -->|"No (quantity = 0)"| Delete --> Then
```

---

### Scenario 4: Update Blocked (Order Already Confirmed)

**Flow:**

```mermaid
flowchart TD
    A["Master Tab status = CONFIRMED"]
    B["REQUEST: PUT /api/public/mall/tab/36"]
    C["RESPONSE: 422 Unprocessable Entity<br/>message: 'This order has already been confirmed and cannot be modified'<br/>errors.message: ['tabs.mall_errors.order_already_confirmed']"]
    D["FRONTEND HANDLING:<br/>- Show error toast to customer<br/>- Disable edit controls for this order<br/>- Suggest creating a new order if needed"]

    A --> B --> C --> D
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

```mermaid
flowchart TD
    Update["ORDER UPDATE"]
    Notify["notifyTenantTabUpdated()<br/>Build notification data:<br/>- event: 'mall_order_updated'<br/>- tenant_tab_id, tenant_id, tenant_name<br/>- master_tab_id<br/>- updated_products: [{ product_id, name, old_qty, new_qty }]<br/>- timestamp<br/>- customer_info: { name, table }"]
    WS["WebSocket<br/>Channel: tenant.{id}.orders"]
    DB["Database<br/>Store in mall_session_notifs"]
    FCM["FCM Push<br/>Send to staff devices"]

    subgraph StaffApp["STAFF APP (KitchnTabs)"]
        Listener["WebSocket Listener<br/>echo.private('tenant.${tenantId}.orders')<br/>.listen('.mall_order_updated', (event) =&gt; {<br/>showToast('Order #' + event.master_tab_id + ' updated by customer');<br/>refreshOrderList(); });"]
        Push["Push Notification (if app in background):<br/>'Order Updated'<br/>Customer at Table 15 changed their order"]
    end

    Update --> Notify
    Notify --> WS
    Notify --> DB
    Notify --> FCM
    WS --> Listener
    FCM --> Push
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

```mermaid
sequenceDiagram
    participant Customer
    participant Frontend
    participant Backend
    participant Database
    participant Staff

    Customer->>Frontend: Edit quantity
    Frontend->>Backend: PUT /tab/36
    Backend->>Database: BEGIN TX
    Backend->>Database: Load master tab
    Database-->>Backend: 
    Backend->>Database: Load tenant tabs
    Database-->>Backend: 
    Backend->>Database: Update items
    Database-->>Backend: 
    Backend->>Database: Recalc totals
    Database-->>Backend: 
    Backend->>Database: Sync master
    Database-->>Backend: 
    Backend->>Database: COMMIT TX
    Database-->>Backend: 
    Backend->>Staff: Send WebSocket
    Backend->>Staff: Send FCM Push
    Backend-->>Frontend: Updated Tab
    Frontend-->>Customer: Show success
    Staff-->>Database: Order updated!
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
