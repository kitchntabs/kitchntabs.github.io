---
layout: default
title: F5-Customer-Self-Service CUSTOMER APP COMPLETE FLOW
---

# Customer App (Mall Client) - Complete Flow Documentation

## Overview

This document describes the complete flow of the **Customer App (Mall Client)** - the public-facing application that allows customers to order from multiple restaurants in a mall/food court via QR code scanning.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CUSTOMER APP SYSTEM ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
  │    CUSTOMER     │        │   MALL CLIENT   │        │   PUBLIC API    │
  │   (Phone/Web)   │◀──────▶│    (React)      │◀──────▶│   (Laravel)     │
  │                 │        │                 │        │                 │
  └─────────────────┘        └────────┬────────┘        └────────┬────────┘
                                      │                          │
                             ┌────────▼────────┐        ┌────────▼────────┐
                             │   WebSocket     │        │   MallSession   │
                             │   Channel:      │◀──────▶│   (Database)    │
                             │ session.{hash}  │        │                 │
                             └─────────────────┘        └─────────────────┘
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

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         QR CODE & SESSION FLOW                               │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │  Customer Scans │
  │  QR Code at     │
  │  Table          │
  └────────┬────────┘
           │
           │  QR contains: https://app.domain.com/mall/session/{hash}
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    FRONTEND ROUTING                                      │
  │                                                                          │
  │  Route: /mall/session/:sessionId                                        │
  │  Component: MallClientWrapper                                            │
  │                                                                          │
  └────────────────────────────┬────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    SESSION VALIDATION                                    │
  │                                                                          │
  │  1. Check localStorage for previous session hash                        │
  │  2. Compare with URL hash - clear if different                          │
  │  3. Store current hash: dashStorage.setItem('mall-session-hash', hash)  │
  │                                                                          │
  └────────────────────────────┬────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │              API: GET /api/public/mall/{hash}/getSessionAuth             │
  │                                                                          │
  │  MallSessionController::getSessionAuth()                                │
  │    │                                                                     │
  │    ├──▶ Find MallSession by hash                                        │
  │    │                                                                     │
  │    ├──▶ If PENDING → Activate session                                   │
  │    │      • status = 'active'                                           │
  │    │      • meta = { activated_at, client_ip, user_agent }              │
  │    │                                                                     │
  │    ├──▶ If ACTIVE → Validate client identity                            │
  │    │      • Check session expiration (6 hours)                          │
  │    │      • Log suspicious access if IP/UA differs                      │
  │    │                                                                     │
  │    └──▶ Return auth response:                                           │
  │           • tenant (mall manager)                                        │
  │           • systemValues (mall, tenants, settings)                      │
  │           • redirectTo                                                   │
  │                                                                          │
  └────────────────────────────┬────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    INITIALIZE CLIENT APP                                 │
  │                                                                          │
  │  1. Store auth data in AuthPersistenceService                           │
  │  2. Subscribe to WebSocket: session.{hash} (public channel)             │
  │  3. Initialize MallSessionEchoContext for real-time updates             │
  │  4. Load available restaurants (tenants)                                │
  │  5. Show order creation interface                                       │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Session Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SESSION LIFECYCLE                                     │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌───────────────┐
                    │   PENDING     │ ◀─── Created via QR generation
                    │               │      (by mall admin)
                    └───────┬───────┘
                            │
                            │ Customer scans QR
                            │ (validates IP/UserAgent)
                            ▼
                    ┌───────────────┐
                    │    ACTIVE     │ ◀─── Can create orders
                    │               │      Duration: 6 hours max
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
  │   COMPLETED   │ │   CANCELLED   │ │   EXPIRED     │
  │               │ │               │ │ (after 6hrs)  │
  │ (all orders   │ │ (manual       │ │               │
  │  fulfilled)   │ │  cancellation)│ │               │
  └───────────────┘ └───────────────┘ └───────────────┘
```

---

## Order Creation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORDER CREATION FLOW                                  │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │  Customer Opens │
  │  Order Form     │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         ORDER CREATION UI                                │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  🔍 Buscar productos...                                         │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Filtrar por tienda: [Todas ▼]  Categoría: [Todas ▼]           │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │                                                                  │    │
  │  │  🍕 PIZZA PLACE         🍣 SUSHI BAR         🍔 BURGER JOINT    │    │
  │  │                                                                  │    │
  │  │  ┌──────────┐         ┌──────────┐         ┌──────────┐        │    │
  │  │  │ [IMG]    │         │ [IMG]    │         │ [IMG]    │        │    │
  │  │  │ Margarita│         │ Rolls    │         │ Classic  │        │    │
  │  │  │ $12,990  │         │ $15,990  │         │ $9,990   │        │    │
  │  │  │ [+]      │         │ [+]      │         │ [+]      │        │    │
  │  │  └──────────┘         └──────────┘         └──────────┘        │    │
  │  │                                                                  │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  🛒 Carrito (3 items)                              Total: $38,970│    │
  │  │                                                                  │    │
  │  │  x1 Margarita (Pizza Place) ...................... $12,990      │    │
  │  │  x1 California Roll (Sushi Bar) .................. $15,990      │    │
  │  │  x1 Classic Burger (Burger Joint) ................ $9,990       │    │
  │  │                                                                  │    │
  │  │                                        [Realizar Pedido →]      │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │
           │ Click "Realizar Pedido"
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    CUSTOMER DATA MODAL (MallAppMediator)                 │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │                                                                  │    │
  │  │   Complete tu pedido                                            │    │
  │  │                                                                  │    │
  │  │   Tu nombre: [_______________________]                          │    │
  │  │                                                                  │    │
  │  │   Número de mesa: [____]                                        │    │
  │  │                                                                  │    │
  │  │                                              [Continuar]        │    │
  │  │                                                                  │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │
           │ Submit with customer data
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    DASHMallClientDataProvider.create()                   │
  │                                                                          │
  │  Automatically injects:                                                  │
  │    • mall_id (from systemValues)                                        │
  │    • mall_session (from localStorage)                                   │
  │                                                                          │
  └────────────────────────────┬────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                  API: POST /api/public/mall/tab                          │
  │                                                                          │
  │  MallTabsController::_create()                                          │
  │    │                                                                     │
  │    ├──▶ Validate request (validateMallOrderRequest)                     │
  │    │                                                                     │
  │    ├──▶ Update MallSession with customer info                           │
  │    │      • customer_name                                                │
  │    │      • mall_location (table number)                                │
  │    │                                                                     │
  │    ├──▶ Group products by tenant (groupProductsByTenant)                │
  │    │                                                                     │
  │    ├──▶ Create MASTER TAB (under mall manager)                          │
  │    │      • is_master_tab = true                                        │
  │    │      • Contains ALL products                                       │
  │    │      • Socket notification only (no FCM push)                      │
  │    │                                                                     │
  │    ├──▶ For EACH TENANT with products:                                  │
  │    │      │                                                              │
  │    │      └──▶ Create TENANT TAB                                        │
  │    │            • master_tab_id = masterTab.id                          │
  │    │            • Contains only that tenant's products                  │
  │    │            • Send notification with:                               │
  │    │                - WebSocket (socket)                                │
  │    │                - FCM Push (push)                                   │
  │    │                - TTS speech                                        │
  │    │                - Alarm trigger                                     │
  │    │                - Product summary ("un Bulgogi, dos Bibimbap")      │
  │    │                                                                     │
  │    └──▶ Return master tab response                                      │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Multi-Restaurant Order Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MULTI-RESTAURANT ORDER STRUCTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────────────────┐
  │                          MALL SESSION                                      │
  │                                                                            │
  │  hash: "M5U2W"                                                            │
  │  customer_name: "Francisco Aranda"                                        │
  │  mall_location: "8" (table)                                               │
  │  status: "active"                                                         │
  │                                                                            │
  └─────────────────────────────────────┬─────────────────────────────────────┘
                                        │
                                        │ brokerable relationship
                                        ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │                          MASTER TAB                                        │
  │                                                                            │
  │  tenant_id: mall_manager_tenant_id                                        │
  │  is_master_tab: true                                                      │
  │  status: CREATED → CONFIRMED → PREPARED → DELIVERED → CLOSED             │
  │                                                                            │
  │  ORDER (Master):                                                          │
  │    • Contains ALL products from ALL tenants                               │
  │    • is_master_order: true                                                │
  │    • Product statuses sync from tenant orders                            │
  │                                                                            │
  └────────────────────────────┬──────────────────────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
  │  TENANT TAB #1  │ │  TENANT TAB #2  │ │  TENANT TAB #3  │
  │                 │ │                 │ │                 │
  │  Pizza Place    │ │  Sushi Bar      │ │  Burger Joint   │
  │  tenant_id: 5   │ │  tenant_id: 6   │ │  tenant_id: 7   │
  │                 │ │                 │ │                 │
  │  master_tab_id  │ │  master_tab_id  │ │  master_tab_id  │
  │  = masterTab.id │ │  = masterTab.id │ │  = masterTab.id │
  │                 │ │                 │ │                 │
  │  ORDER:         │ │  ORDER:         │ │  ORDER:         │
  │  • Margarita x1 │ │  • Rolls x1     │ │  • Burger x1    │
  │                 │ │                 │ │                 │
  │  status: PREP   │ │  status: READY  │ │  status: CONF   │
  └─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Real-Time Order Tracking

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REAL-TIME ORDER TRACKING                                │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │ Restaurant Staff│
  │ Updates Status  │
  └────────┬────────┘
           │
           │ PUT /api/tab/tab/{tenant_tab_id}
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         BACKEND PROCESSING                               │
  │                                                                          │
  │  TabsNotificationService::handleStatusChange()                          │
  │    │                                                                     │
  │    ├──▶ Update tenant tab status                                        │
  │    ├──▶ Update tenant order status                                      │
  │    │                                                                     │
  │    └──▶ handleSlaveTabStatusChange()                                    │
  │           │                                                              │
  │           ├──▶ Sync master order product statuses                       │
  │           ├──▶ Update master tab status (aggregate)                     │
  │           └──▶ notifyMallSession()                                      │
  │                  │                                                       │
  │                  └──▶ MallSessionOrderStatusNotification                │
  │                         • Channel: session.{hash}                       │
  │                         • Includes: tenant_name, status, products       │
  │                                                                          │
  └────────────────────────────┬────────────────────────────────────────────┘
           │
           │ WebSocket Event
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    CUSTOMER APP (MallClientTabsList)                     │
  │                                                                          │
  │  MallClientTabsContext receives event                                   │
  │    │                                                                     │
  │    ├──▶ Update tenantStatusesByTab state                                │
  │    ├──▶ Show toast notification                                         │
  │    └──▶ Refresh order list                                              │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
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

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NOTIFICATION FLOW TO CUSTOMER                             │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌─────────────────────────────┐
                         │   MallSessionOrderStatus    │
                         │   Notification              │
                         └──────────────┬──────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
              ▼                         ▼                         ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │    WebSocket    │     │    Database     │     │   FCM Push      │
    │                 │     │    Storage      │     │   (Optional)    │
    │ Channel:        │     │                 │     │                 │
    │ session.{hash}  │     │ mall_session_   │     │ (if registered) │
    │                 │     │ notifications   │     │                 │
    └────────┬────────┘     └────────┬────────┘     └────────┬────────┘
             │                       │                       │
             │                       │                       │
             ▼                       ▼                       ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │                        CUSTOMER EXPERIENCE                          │
    │                                                                     │
    │  WebSocket → Instant toast notification + list refresh             │
    │  Database  → Retrievable notification history                      │
    │  FCM Push  → Background notification (if app closed)               │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
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

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ASSISTANCE REQUEST FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │ Customer Clicks │
  │ "Request Help"  │
  │ for a store     │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │              API: POST /api/public/mall/stores/{id}/assistance           │
  │                                                                          │
  │  MallStoresController::assistance()                                      │
  │    │                                                                     │
  │    ├──▶ Validate session is active                                      │
  │    │                                                                     │
  │    ├──▶ Check rate limit (max 2 per store per session)                  │
  │    │                                                                     │
  │    ├──▶ Update session.assistance_requests counter                      │
  │    │                                                                     │
  │    └──▶ Send notification:                                              │
  │           MallStoreAssistanceNotification                               │
  │             • Channel: tenant.{storeId}.system                          │
  │             • Targets: kitchen, staff                                   │
  │             • Type: urgency-alert:speech                                │
  │             • TTS: "Customer {name} at table {table}"                   │
  │             • Alarm: true                                               │
  │             • FCM Push: true                                            │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    RESTAURANT STAFF RECEIVES                             │
  │                                                                          │
  │  • Loud alarm sound plays                                               │
  │  • TTS announces: "Customer Francisco at table 8 needs help"            │
  │  • FCM push notification on mobile device                               │
  │  • WebSocket notification updates dashboard                             │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
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

```
MallClientWrapper
├── MallSessionEchoProvider (WebSocket context)
│   └── KitchnTabsPrivateApp
│       ├── GlobalTenantWrapper (theming/settings)
│       ├── MallAppMediator (customer data modal)
│       │
│       └── MallClientAppResources
│           └── ResourceTemplate (tab)
│               ├── MallTabsContext
│               │
│               ├── CREATE VIEW
│               │   ├── MallOrderStoresField (store filters)
│               │   ├── MallOrderProducts (product grid)
│               │   ├── MallProductModifiersModal
│               │   └── MallCartSummary
│               │
│               └── LIST VIEW
│                   └── MallClientTabsList
│                       └── OrderProductsView
│                           └── MallSessionOrderProgress
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
