---
layout: default
title: F6-Tenant-Staff-App STAFF APP COMPLETE FLOW
---

# Staff App - Complete Flow Documentation

## Overview

This document describes the complete flow of the **Staff/Kitchen App** - from login to order management and all operations available to restaurant staff.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        STAFF APP SYSTEM ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
  │   STAFF USER    │◀──────▶│   STAFF APP     │◀──────▶│  LARAVEL API    │
  │   (Kitchen/     │        │   (React)       │        │  (Backend)      │
  │    Cashier)     │        │                 │        │                 │
  └─────────────────┘        └────────┬────────┘        └────────┬────────┘
                                      │                          │
                             ┌────────▼────────┐        ┌────────▼────────┐
                             │   WebSocket     │        │    Database     │
                             │   (Pusher/      │◀──────▶│    (MySQL)      │
                             │    Soketi)      │        │                 │
                             └─────────────────┘        └─────────────────┘
```

---

## User Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| `admin` | Tenant Administrator | Full access, manage users, settings |
| `staff` | Front-of-house staff | Create/manage orders, process payments |
| `kitchen` | Kitchen staff | View orders, update preparation status |

---

## Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AUTHENTICATION FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │  Staff Opens    │
  │  Application    │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         CHECK AUTH STATE                                 │
  │                                                                          │
  │  1. Check localStorage for existing token                               │
  │  2. Validate token with API (GET /api/user)                            │
  │                                                                          │
  └────────────────────────────┬────────────────────────────────────────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
  ┌───────┐   ┌───────────────────────────────────────────────────────────┐
  │ Valid │   │                    LOGIN FLOW                             │
  │ Token │   │                                                           │
  └───┬───┘   │  1. Display login form (email/password)                  │
      │       │  2. POST /api/auth/login                                  │
      │       │  3. Receive token + user data                             │
      │       │  4. Store in localStorage (AuthPersistenceService)        │
      │       │  5. Initialize WebSocket connection                       │
      │       │                                                           │
      │       └─────────────────────────┬─────────────────────────────────┘
      │                                 │
      └─────────────┬───────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    INITIALIZE APP STATE                                  │
  │                                                                          │
  │  1. Load tenant settings (systemValues)                                 │
  │  2. Subscribe to WebSocket channel: tenant.{id}.system                  │
  │  3. Load initial tab list                                               │
  │  4. Initialize notification handlers                                    │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Main App Views

### 1. Tab List View (TabsList)

**Purpose:** Primary view for managing all active orders

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ☰ TABS                                              [+ Crear Tab]          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Filter: [Todos ▼]  [Estado: Todos ▼]                                      │
│                                                                             │
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐       │
│  │ Tab #125          │  │ Tab #124          │  │ Tab #123          │       │
│  │ ⏱ 00:05:32       │  │ ⏱ 00:12:15       │  │ ⏱ 00:25:00       │       │
│  │ ────────────────  │  │ ────────────────  │  │ ────────────────  │       │
│  │ Mesa: 8           │  │ Mesa: 5           │  │ Mesa: 3           │       │
│  │ Cliente: Juan     │  │ Cliente: María    │  │ Cliente: Pedro    │       │
│  │ ────────────────  │  │ ────────────────  │  │ ────────────────  │       │
│  │ x2 Bulgogi        │  │ x1 Bibimbap       │  │ x3 Ramen          │       │
│  │ x1 Coca-Cola      │  │ x2 Soju           │  │                   │       │
│  │ ────────────────  │  │ ────────────────  │  │ ────────────────  │       │
│  │ Total: $27,980    │  │ Total: $18,990    │  │ Total: $35,970    │       │
│  │ ────────────────  │  │ ────────────────  │  │ ────────────────  │       │
│  │ [CREADO]          │  │ [CONFIRMADO]      │  │ [PREPARADO]       │       │
│  │                   │  │                   │  │                   │       │
│  │ [→] [💳] [🖨️] [⬇️]│  │ [→] [💳] [🖨️] [⬇️]│  │ [→] [💳] [🖨️] [⬇️]│       │
│  └───────────────────┘  └───────────────────┘  └───────────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Available Actions:**
- `[→]` - Advance to next status
- `[💳]` - Process payment
- `[🖨️]` - Print sale note
- `[⬇️]` - Download sale note

### 2. Kitchen View (KitchenTabsList)

**Purpose:** Simplified view for kitchen staff focused on preparation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🍳 COCINA                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ◀ ────────────────────────────────────────────────────────────────── ▶    │
│                                                                             │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐    │
│  │ Tab #125  ⏱ 05:32  │  │ Tab #124  ⏱ 12:15  │  │ Tab #123  ⏱ 25:00  │    │
│  │ ─────────────────  │  │ ─────────────────  │  │ ─────────────────  │    │
│  │                    │  │                    │  │                    │    │
│  │ [IMG] x2 Bulgogi   │  │ [IMG] x1 Bibimbap  │  │ [IMG] x3 Ramen     │    │
│  │       • Cerdo      │  │       • Extra arr  │  │       • Picante    │    │
│  │       • Arroz      │  │                    │  │                    │    │
│  │                    │  │ [IMG] x2 Soju      │  │                    │    │
│  │ [IMG] x1 Coca-Cola │  │                    │  │                    │    │
│  │                    │  │                    │  │                    │    │
│  │ ─────────────────  │  │ ─────────────────  │  │ ─────────────────  │    │
│  │ [CREADO]           │  │ [CONFIRMADO]       │  │ [EN PREPARACIÓN]   │    │
│  │                    │  │                    │  │                    │    │
│  │ [Confirmar →]      │  │ [Preparado →]      │  │ [Listo →]          │    │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Order Creation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ORDER CREATION FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │  Staff Clicks   │
  │  [+ Crear Tab]  │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         TAB CREATE FORM                                  │
  │                                                                          │
  │  Delivery Method: [Mesa ▼]                                              │
  │  Table/Note: [________________]                                          │
  │                                                                          │
  │  ─────────────────────────────────────────────────────────────────────  │
  │                                                                          │
  │  Products:                                                               │
  │  ┌────────────────────────────────────────────────────────────────────┐ │
  │  │ Search: [_______________]  Filter: [Todas las categorías ▼]       │ │
  │  │                                                                    │ │
  │  │ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │ │
  │  │ │ [IMG]    │  │ [IMG]    │  │ [IMG]    │  │ [IMG]    │          │ │
  │  │ │ Bulgogi  │  │ Bibimbap │  │ Ramen    │  │ Soju     │          │ │
  │  │ │ $13,990  │  │ $12,990  │  │ $11,990  │  │ $5,990   │          │ │
  │  │ │  [+]     │  │  [+]     │  │  [+]     │  │  [+]     │          │ │
  │  │ └──────────┘  └──────────┘  └──────────┘  └──────────┘          │ │
  │  └────────────────────────────────────────────────────────────────────┘ │
  │                                                                          │
  │  Cart:                                                                   │
  │  ┌────────────────────────────────────────────────────────────────────┐ │
  │  │ x2 Bulgogi ......................................... $27,980       │ │
  │  │    └ Modifiers: Cerdo, Arroz                                      │ │
  │  │ x1 Coca-Cola ....................................... $1,990        │ │
  │  │ ────────────────────────────────────────────────────────────────  │ │
  │  │ Total: $29,970                                                     │ │
  │  └────────────────────────────────────────────────────────────────────┘ │
  │                                                                          │
  │  [Cancelar]                                        [Crear Orden]         │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │
           │ Submit
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         BACKEND PROCESSING                               │
  │                                                                          │
  │  TabController::store()                                                  │
  │    │                                                                     │
  │    ├──▶ Create Tab record (status: CREATED)                             │
  │    ├──▶ Create Order record                                             │
  │    ├──▶ Create OrderProduct records                                     │
  │    ├──▶ Calculate totals                                                │
  │    └──▶ Send WebSocket notification                                     │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Order Status Management Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ORDER STATUS MANAGEMENT FLOW                            │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │  Staff Clicks   │
  │  Status Button  │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    FRONTEND (useTabActions hook)                         │
  │                                                                          │
  │  1. Validate current status allows transition                           │
  │  2. Show confirmation if needed                                          │
  │  3. Call dataProvider.update('tab/tab', { status: newStatus })          │
  │                                                                          │
  └────────────────────────────┬────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         API: PUT /api/tab/tab/{id}                       │
  │                                                                          │
  │  TabController::update()                                                 │
  │    │                                                                     │
  │    ├──▶ Validate status transition                                      │
  │    ├──▶ TabsNotificationService::handleStatusChange()                   │
  │    │      │                                                              │
  │    │      ├──▶ Update Tab.status                                        │
  │    │      ├──▶ Update date_* field                                      │
  │    │      ├──▶ Update Order.status (mapped)                             │
  │    │      └──▶ sendNotification() → WebSocket                          │
  │    │                                                                     │
  │    └──▶ If Mall order: MallTabNotificationService                       │
  │           └──▶ Sync master tab status                                   │
  │           └──▶ Notify customer via MallSession channel                  │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │
           │ WebSocket Broadcast
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         ALL CONNECTED CLIENTS                            │
  │                                                                          │
  │  • Other staff apps receive update                                      │
  │  • Kitchen displays refresh                                             │
  │  • Customer app (if Mall) receives notification                         │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Payment Processing Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PAYMENT PROCESSING FLOW                               │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │  Staff Clicks   │
  │  Payment Button │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        PAYMENT DIALOG                                    │
  │                                                                          │
  │  Tab #125 - Total: $29,970                                              │
  │                                                                          │
  │  Payment Method:                                                         │
  │  ○ Efectivo    ● Tarjeta Débito    ○ Tarjeta Crédito    ○ Transferencia │
  │                                                                          │
  │  Service Fee: [10%] = $2,997                                            │
  │                                                                          │
  │  Grand Total: $32,967                                                    │
  │                                                                          │
  │  Status after payment:                                                   │
  │  ○ DELIVERED    ● CLOSED    ○ Keep Current                              │
  │                                                                          │
  │  [Cancelar]                                     [Procesar Pago]          │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │
           │ Process Payment
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    API: PUT /api/tab/tab/{id}/payment                    │
  │                                                                          │
  │  TabController::payment()                                                │
  │    │                                                                     │
  │    ├──▶ Validate payment method exists                                  │
  │    ├──▶ Calculate service fee                                           │
  │    ├──▶ Create Payment record                                           │
  │    ├──▶ Update Order.is_paid = true                                     │
  │    ├──▶ Update Order.total_amount (with service fee)                    │
  │    └──▶ Update Tab.status if requested                                  │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Print/Download Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PRINT / DOWNLOAD FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐           ┌─────────────────┐
  │  Print Button   │           │ Download Button │
  │  [🖨️]           │           │ [⬇️]            │
  └────────┬────────┘           └────────┬────────┘
           │                             │
           ▼                             ▼
  ┌─────────────────────┐     ┌─────────────────────┐
  │ GET /tab/{id}/print │     │GET /tab/{id}/download│
  └────────┬────────────┘     └────────┬────────────┘
           │                           │
           │                           │
           ▼                           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         TabController                                    │
  │                                                                          │
  │  printSaleNote() / downloadSaleNote()                                   │
  │    │                                                                     │
  │    ├──▶ Generate PDF from template                                      │
  │    ├──▶ Include: products, totals, payments, customer info             │
  │    └──▶ Return PDF file                                                 │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │                           │
           ▼                           ▼
  ┌─────────────────────┐     ┌─────────────────────┐
  │  Open print dialog  │     │  Save file locally  │
  └─────────────────────┘     └─────────────────────┘
```

---

## Bulk Operations Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BULK STATUS UPDATE FLOW                               │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         TAB LIST VIEW                                    │
  │                                                                          │
  │  [☑] Tab #125    [☑] Tab #124    [☐] Tab #123    [☑] Tab #122          │
  │                                                                          │
  │  Selected: 3                                                             │
  │                                                                          │
  │  Bulk Actions: [Update Status ▼]                                        │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │
           │ Select "CONFIRMED"
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                API: POST /api/tab/tab/bulk-update-status                 │
  │                                                                          │
  │  {                                                                       │
  │    "tab_ids": [125, 124, 122],                                          │
  │    "status": "CONFIRMED"                                                 │
  │  }                                                                       │
  │                                                                          │
  │  TabController::bulkUpdateStatus()                                       │
  │    │                                                                     │
  │    └──▶ For each tab:                                                   │
  │           ├──▶ Validate permission                                      │
  │           ├──▶ handleStatusChange()                                     │
  │           └──▶ handleSlaveTabStatusChange() (if mall)                   │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Real-Time Updates Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        REAL-TIME UPDATE FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
  │   Staff A     │    │   Staff B     │    │   Kitchen     │
  │   (Cashier)   │    │   (Waiter)    │    │   Display     │
  └───────┬───────┘    └───────┬───────┘    └───────┬───────┘
          │                    │                    │
          │    ┌───────────────────────────────────────┐
          │    │          WebSocket Server              │
          │    │   Channel: tenant.{id}.system          │
          │    └───────────────────────────────────────┘
          │                    │                    │
          │                    │                    │
  ┌───────▼───────┐            │                    │
  │ Staff A       │            │                    │
  │ changes tab   │            │                    │
  │ status        │            │                    │
  └───────┬───────┘            │                    │
          │                    │                    │
          │ API call           │                    │
          ▼                    │                    │
  ┌─────────────────┐          │                    │
  │ Laravel Backend │          │                    │
  │ broadcasts      │          │                    │
  │ notification    │──────────┼────────────────────┤
  └─────────────────┘          │                    │
                               │                    │
                               ▼                    ▼
                    ┌───────────────┐    ┌───────────────┐
                    │ Staff B sees  │    │ Kitchen sees  │
                    │ toast + list  │    │ toast + list  │
                    │ refreshes     │    │ refreshes     │
                    └───────────────┘    └───────────────┘
```

---

## API Endpoints Reference

### Tab Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tab/tab` | List all tabs |
| `POST` | `/api/tab/tab` | Create new tab |
| `GET` | `/api/tab/tab/{id}` | Get tab details |
| `PUT` | `/api/tab/tab/{id}` | Update tab |
| `DELETE` | `/api/tab/tab/{id}` | Delete tab |
| `POST` | `/api/tab/tab/bulk-update-status` | Bulk status update |

### Tab Actions

| Method | Endpoint | Description |
|--------|----------|-------------|
| `PUT` | `/api/tab/tab/{id}/payment` | Process payment |
| `GET` | `/api/tab/tab/{id}/print` | Print sale note |
| `GET` | `/api/tab/tab/{id}/download` | Download sale note |
| `GET` | `/api/tab/tab/statuses` | Get available statuses |
| `GET` | `/api/tab/tab/{id}/status-transitions` | Get valid transitions |

---

## Error Handling

### Frontend Error Display

```typescript
// useTabActions.tsx

const showError = (msg: string) => {
    toast.error(msg, {
        position: 'top-center',
        autoClose: 3000,
    });
};

// Usage
try {
    await updatePayment(tabId, paymentData);
} catch (error) {
    showError('Error al procesar el pago: ' + error.message);
}
```

### Backend Error Responses

```php
// TabController.php

return ResponseHandler::error(
    new Exception(__('tabs.errors.invalid_status_transition')),
    422
);

return ResponseHandler::error(
    new Exception(__('tabs.errors.cannot_delete_processed_tab')),
    409
);
```

---

## Component Hierarchy

```
App
├── AuthProvider
│   └── DashAdmin
│       ├── LaravelEchoContext (WebSocket)
│       └── Resources
│           ├── TabResource (tab/tab)
│           │   ├── TabsList
│           │   │   ├── TabListItem
│           │   │   ├── PaymentDialog
│           │   │   └── CloseDialog
│           │   ├── TabCreate
│           │   │   ├── ProductSelector
│           │   │   └── OrderSummary
│           │   └── TabEdit
│           │
│           └── KitchenResource (tab/kitchen)
│               └── KitchenTabsList
│                   └── OrderProductsView
```

---

## State Management

### Redux Store Structure

```typescript
{
    auth: {
        isAuthenticated: boolean,
        user: User,
        token: string,
        tenant: Tenant
    },
    systemValues: {
        paymentMethods: PaymentMethod[],
        currencies: Currency[],
        settings: TenantSettings
    }
}
```

### Local Component State

```typescript
// TabsList.tsx
const [listData, setListData] = useState<ITab[]>([]);
const [selectedTab, setSelectedTab] = useState<ITab | null>(null);
const [updatingTabs, setUpdatingTabs] = useState<Set<number>>(new Set());
const [paymentMethod, setPaymentMethod] = useState<string>("");
const [serviceFeeValue, setServiceFeeValue] = useState(0);
```
