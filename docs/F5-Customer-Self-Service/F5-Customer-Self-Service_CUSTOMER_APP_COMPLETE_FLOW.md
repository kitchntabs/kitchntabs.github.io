
# Customer App (Mall Client) - Complete Flow Documentation

## Overview

This document describes the complete flow of the **Customer App (Mall Client)** - the public-facing application that allows customers to order from multiple restaurants in a mall/food court via QR code scanning.

---

## System Architecture

```mermaid
flowchart LR
    A["CUSTOMER<br/>(Phone/Web)"] <--> B["MALL CLIENT<br/>(React)"]
    B <--> C["PUBLIC API<br/>(Laravel)"]
    B --> D["WebSocket<br/>Channel:<br/>session.{hash}"]
    C --> E["MallSession<br/>(Database)"]
    D <--> E
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Mall Session** | Temporary session created when customer scans QR code (5-char hash) |
| **Master Tab** | Aggregated order under mall manager tenant |
| **Tenant Tab** | Individual order per restaurant within the session |
| **Session Hash** | Unique 5-character identifier (e.g., "M5U2W") |

---

## QR Code & Session Flow

```mermaid
flowchart TD
    A["Customer Scans QR Code at Table"] -->|"QR contains: https://app.domain.com/mall/session/{hash}"| B
    B["FRONTEND ROUTING<br/>Route: /mall/session/:sessionId<br/>Component: MallClientWrapper"] --> C
    C["SESSION VALIDATION<br/>1. Check localStorage for previous session hash<br/>2. Compare with URL hash - clear if different<br/>3. Store current hash: dashStorage.setItem('mall-session-hash', hash)"] --> D
    D["API: GET /api/public/mall/{hash}/getSessionAuth<br/>MallSessionController::getSessionAuth()"] --> D1["Find MallSession by hash"]
    D --> D2["If PENDING → Activate session<br/>- status = 'active'<br/>- meta = activated_at, client_ip, user_agent"]
    D --> D3["If ACTIVE → Validate client identity<br/>- Check session expiration (6 hours)<br/>- Log suspicious access if IP/UA differs"]
    D --> D4["Return auth response:<br/>- tenant (mall manager)<br/>- systemValues (mall, tenants, settings)<br/>- redirectTo"]
    D4 --> E
    E["INITIALIZE CLIENT APP<br/>1. Store auth data in AuthPersistenceService<br/>2. Subscribe to WebSocket: session.{hash} (public channel)<br/>3. Initialize MallSessionEchoContext for real-time updates<br/>4. Load available restaurants (tenants)<br/>5. Show order creation interface"]
```

---

## Session Lifecycle

```mermaid
stateDiagram-v2
    [*] --> PENDING: Created via QR generation (by mall admin)
    PENDING --> ACTIVE: Customer scans QR (validates IP/UserAgent)
    ACTIVE --> COMPLETED: all orders fulfilled
    ACTIVE --> CANCELLED: manual cancellation
    ACTIVE --> EXPIRED: after 6hrs
    note right of ACTIVE
        Can create orders
        Duration: 6 hours max
    end note
```

---

## Order Creation Flow

```mermaid
flowchart TD
    A["Customer Opens Order Form"] --> B
    B["ORDER CREATION UI<br/>- Search bar: 'Buscar productos...'<br/>- Filters: tienda (store), categoría<br/>- Product grid by store (Pizza Place, Sushi Bar, Burger Joint) with image, name, price, add button<br/>- Cart summary (Carrito) with line items and total<br/>- 'Realizar Pedido' button"] -->|"Click 'Realizar Pedido'"| C
    C["CUSTOMER DATA MODAL (MallAppMediator)<br/>'Complete tu pedido' form:<br/>- Tu nombre (name input)<br/>- Número de mesa (table number input)<br/>- 'Continuar' button"] -->|"Submit with customer data"| D
    D["DASHMallClientDataProvider.create()<br/>Automatically injects:<br/>- mall_id (from systemValues)<br/>- mall_session (from localStorage)"] --> E
    E["API: POST /api/public/mall/tab<br/>MallTabsController::_create()"] --> E1["Validate request (validateMallOrderRequest)"]
    E --> E2["Update MallSession with customer info<br/>- customer_name<br/>- mall_location (table number)"]
    E --> E3["Group products by tenant (groupProductsByTenant)"]
    E --> E4["Create MASTER TAB (under mall manager)<br/>- is_master_tab = true<br/>- Contains ALL products<br/>- Socket notification only (no FCM push)"]
    E --> E5["For EACH TENANT with products:<br/>Create TENANT TAB<br/>- master_tab_id = masterTab.id<br/>- Contains only that tenant's products<br/>- Send notification with:<br/>&nbsp;&nbsp;WebSocket (socket), FCM Push (push), TTS speech,<br/>&nbsp;&nbsp;Alarm trigger, Product summary ('un Bulgogi, dos Bibimbap')"]
    E --> E6["Return master tab response"]
```

---

## Multi-Restaurant Order Structure

```mermaid
flowchart TD
    A["MALL SESSION<br/>hash: 'M5U2W'<br/>customer_name: 'Francisco Aranda'<br/>mall_location: '8' (table)<br/>status: 'active'"] -->|"brokerable relationship"| B
    B["MASTER TAB<br/>tenant_id: mall_manager_tenant_id<br/>is_master_tab: true<br/>status: CREATED → CONFIRMED → PREPARED → DELIVERED → CLOSED<br/><br/>ORDER (Master):<br/>- Contains ALL products from ALL tenants<br/>- is_master_order: true<br/>- Product statuses sync from tenant orders"]
    B --> C1["TENANT TAB #1<br/>Pizza Place<br/>tenant_id: 5<br/>master_tab_id = masterTab.id<br/>ORDER: Margarita x1<br/>status: PREP"]
    B --> C2["TENANT TAB #2<br/>Sushi Bar<br/>tenant_id: 6<br/>master_tab_id = masterTab.id<br/>ORDER: Rolls x1<br/>status: READY"]
    B --> C3["TENANT TAB #3<br/>Burger Joint<br/>tenant_id: 7<br/>master_tab_id = masterTab.id<br/>ORDER: Burger x1<br/>status: CONF"]
```

---

## Real-Time Order Tracking

```mermaid
flowchart TD
    A["Restaurant Staff Updates Status"] -->|"PUT /api/tab/tab/{tenant_tab_id}"| B
    B["BACKEND PROCESSING<br/>TabsNotificationService::handleStatusChange()"] --> B1["Update tenant tab status"]
    B --> B2["Update tenant order status"]
    B --> B3["handleSlaveTabStatusChange()"]
    B3 --> B3a["Sync master order product statuses"]
    B3 --> B3b["Update master tab status (aggregate)"]
    B3 --> B3c["notifyMallSession()"]
    B3c --> B4["MallSessionOrderStatusNotification<br/>- Channel: session.{hash}<br/>- Includes: tenant_name, status, products"]
    B4 -->|"WebSocket Event"| C
    C["CUSTOMER APP (MallClientTabsList)<br/>MallClientTabsContext receives event"] --> C1["Update tenantStatusesByTab state"]
    C --> C2["Show toast notification"]
    C --> C3["Refresh order list"]
```

---

## Customer Order View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CUSTOMER ORDER VIEW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────────────────┐
  │  ☰ TUS ORDENES                                    [+ Nueva Orden]         │
  ├───────────────────────────────────────────────────────────────────────────┤
  │                                                                           │
  │  ┌─────────────────────────────────────────────────────────────────────┐ │
  │  │  Orden #125                                            ⏱ 00:05:32   │ │
  │  │  ─────────────────────────────────────────────────────────────────  │ │
  │  │                                                                     │ │
  │  │  🍕 PIZZA PLACE                                      [PREPARADO ✓]  │ │
  │  │  ████████████████████████████████████░░░░░░░░  80%                 │ │
  │  │    x1 Margarita                                                     │ │
  │  │                                                                     │ │
  │  │  🍣 SUSHI BAR                                    [EN PREPARACIÓN]   │ │
  │  │  ██████████████████████░░░░░░░░░░░░░░░░░░░░░░  50%                 │ │
  │  │    x1 California Roll                                               │ │
  │  │    x2 Nigiri                                                        │ │
  │  │                                                                     │ │
  │  │  🍔 BURGER JOINT                                     [CONFIRMADO]   │ │
  │  │  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  25%                 │ │
  │  │    x1 Classic Burger                                                │ │
  │  │    x1 Papas Fritas                                                  │ │
  │  │                                                                     │ │
  │  │  ─────────────────────────────────────────────────────────────────  │ │
  │  │  Total: $38,970                                                     │ │
  │  └─────────────────────────────────────────────────────────────────────┘ │
  │                                                                           │
  │  ℹ️  Recibirás notificaciones cuando tus pedidos estén listos            │
  │                                                                           │
  └───────────────────────────────────────────────────────────────────────────┘
```

---

## Notification Flow to Customer

```mermaid
flowchart TD
    A["MallSessionOrderStatusNotification"] --> B["WebSocket<br/>Channel: session.{hash}"]
    A --> C["Database Storage<br/>mall_session_notifications"]
    A --> D["FCM Push (Optional)<br/>(if registered)"]
    B --> E["CUSTOMER EXPERIENCE<br/>WebSocket → Instant toast notification + list refresh<br/>Database → Retrievable notification history<br/>FCM Push → Background notification (if app closed)"]
    C --> E
    D --> E
```

---

## WebSocket Event Structure (Customer)

### Order Status Update Event

```json
{
    "event": "mall_order_status_update",
    "data": {
        "type": "mall_order_status_update",
        "tenant_tab_id": 126,
        "tenant_id": 5,
        "tenant_name": "Pizza Place",
        "status": "PREPARED",
        "master_tab_id": 125,
        "timestamp": "2025-12-12T00:45:00-03:00",
        "products": [
            {
                "product_id": 50,
                "name": "Margarita",
                "quantity": 1,
                "status": "PREPARED"
            }
        ],
        "mall_session_hash": "M5U2W"
    },
    "notificationPayload": {
        "class": "MallSessionOrderStatusNotification",
        "title": "¡Tu pedido está listo!",
        "message": "Pizza Place ha preparado tu orden"
    }
}
```

---

## Data Provider (Customer App)

### DASHMallClientDataProvider

```typescript
// Key features:

// 1. Resource path mapping
const RESOURCE_PATH_MAP = {
    'tab': 'public/mall/tab',
    'stores': 'public/mall/stores',
    'products': 'public/mall/products',
};

// 2. Auto-inject mall context
const addMallIdToParams = (params) => {
    const mall_id = getMallId();           // from systemValues
    const mall_session = getSessionId();   // from localStorage
    
    return {
        ...params,
        filter: {
            ...params.filter,
            mall_id,
            mall_session,
        },
    };
};

// 3. Disabled dangerous operations
delete: () => { throw new Error('Delete not allowed'); },
deleteMany: () => { throw new Error('Delete not allowed'); },
```

---

## Assistance Request Flow

```mermaid
flowchart TD
    A["Customer Clicks 'Request Help' for a store"] --> B
    B["API: POST /api/public/mall/stores/{id}/assistance<br/>MallStoresController::assistance()"] --> B1["Validate session is active"]
    B --> B2["Check rate limit (max 2 per store per session)"]
    B --> B3["Update session.assistance_requests counter"]
    B --> B4["Send notification: MallStoreAssistanceNotification<br/>- Channel: tenant.{storeId}.system<br/>- Targets: kitchen, staff<br/>- Type: urgency-alert:speech<br/>- TTS: 'Customer {name} at table {table}'<br/>- Alarm: true<br/>- FCM Push: true"]
    B4 --> C
    C["RESTAURANT STAFF RECEIVES<br/>- Loud alarm sound plays<br/>- TTS announces: 'Customer Francisco at table 8 needs help'<br/>- FCM push notification on mobile device<br/>- WebSocket notification updates dashboard"]
```

---

## API Endpoints Reference (Customer)

### Public Mall Endpoints (No Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/public/mall/{hash}/getSessionAuth` | Validate and activate session |
| `GET` | `/api/public/mall/stores` | List available restaurants |
| `GET` | `/api/public/mall/stores/{id}` | Get restaurant details |
| `GET` | `/api/public/mall/products` | List products (with mall_id filter) |
| `GET` | `/api/public/mall/tab` | List customer's orders |
| `POST` | `/api/public/mall/tab` | Create new order |
| `GET` | `/api/public/mall/tab/{id}` | Get order details |
| `POST` | `/api/public/mall/stores/{id}/assistance` | Request staff help |
| `GET` | `/api/public/mall/session/{hash}/notifications` | Get notification history |
| `POST` | `/api/public/mall/session/{hash}/notifications/mark-read` | Mark notifications read |

---

## Frontend Component Hierarchy

```mermaid
flowchart TD
    A["MallClientWrapper"] --> B["MallSessionEchoProvider (WebSocket context)"]
    B --> C["KitchnTabsPrivateApp"]
    C --> D["GlobalTenantWrapper (theming/settings)"]
    C --> E["MallAppMediator (customer data modal)"]
    C --> F["MallClientAppResources"]
    F --> G["ResourceTemplate (tab)"]
    G --> H["MallTabsContext"]
    G --> I["CREATE VIEW"]
    I --> I1["MallOrderStoresField (store filters)"]
    I --> I2["MallOrderProducts (product grid)"]
    I --> I3["MallProductModifiersModal"]
    I --> I4["MallCartSummary"]
    G --> J["LIST VIEW"]
    J --> K["MallClientTabsList"]
    K --> L["OrderProductsView"]
    L --> M["MallSessionOrderProgress"]
```

---

## State Management (Customer)

### localStorage Keys

| Key | Value | Purpose |
|-----|-------|---------|
| `mall-session-hash` | "M5U2W" | Current session identifier |
| `orderData` | `{name, tableNumber}` | Customer info for orders |

### Context State (MallClientTabsContext)

```typescript
{
    lastEvent: WebSocketEvent | null,
    tenantStatusesByTab: {
        [tabId]: {
            [tenantId]: "PREPARED" | "IN_PREPARATION" | ...
        }
    }
}
```

---

## Error Handling

### Session Errors

| Error | HTTP Code | User Message |
|-------|-----------|--------------|
| Session not found | 404 | "Sesión no encontrada" |
| Session expired | 410 | "La sesión ha expirado" |
| Session inactive | 400 | "Sesión no está activa" |

### Order Errors

| Error | Handling |
|-------|----------|
| Missing customer data | Show MallAppMediator modal |
| Product unavailable | Show toast, remove from cart |
| Session expired | Redirect to error page |

---

## Mobile Responsiveness

The customer app is designed mobile-first:

```
┌────────────────────────────────────────┐
│  Mobile View (xs)                      │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │  🔍 Buscar...                    │  │
│  └──────────────────────────────────┘  │
│                                        │
│  [Todas ▼] [Categoria ▼]              │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │  [IMG]                           │  │
│  │  Bulgogi                         │  │
│  │  $13,990                    [+]  │  │
│  └──────────────────────────────────┘  │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │  [IMG]                           │  │
│  │  Bibimbap                        │  │
│  │  $12,990                    [+]  │  │
│  └──────────────────────────────────┘  │
│                                        │
│  ════════════════════════════════════  │
│  🛒 Carrito (2)         Total: $26,980 │
│                     [Pedir →]          │
│  ════════════════════════════════════  │
│                                        │
└────────────────────────────────────────┘
```
