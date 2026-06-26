
# Staff App - Complete Flow Documentation

## Overview

This document describes the complete flow of the **Staff/Kitchen App** - from login to order management and all operations available to restaurant staff.

---

## System Architecture

```mermaid
flowchart LR
    User["STAFF USER<br/>(Kitchen/Cashier)"]
    App["STAFF APP<br/>(React)"]
    API["LARAVEL API<br/>(Backend)"]
    WS["WebSocket<br/>(Pusher/Soketi)"]
    DB["Database<br/>(MySQL)"]

    User <--> App
    App <--> API
    App --> WS
    API --> DB
    WS <--> DB
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

```mermaid
flowchart TD
    Open["Staff Opens Application"]
    Check["CHECK AUTH STATE<br/>1. Check localStorage for existing token<br/>2. Validate token with API (GET /api/user)"]
    Valid["Valid Token"]
    Login["LOGIN FLOW<br/>1. Display login form (email/password)<br/>2. POST /api/auth/login<br/>3. Receive token + user data<br/>4. Store in localStorage (AuthPersistenceService)<br/>5. Initialize WebSocket connection"]
    Init["INITIALIZE APP STATE<br/>1. Load tenant settings (systemValues)<br/>2. Subscribe to WebSocket channel: tenant.{id}.system<br/>3. Load initial tab list<br/>4. Initialize notification handlers"]

    Open --> Check
    Check --> Valid
    Check --> Login
    Valid --> Init
    Login --> Init
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

```mermaid
flowchart TD
    Click["Staff Clicks [+ Crear Tab]"]
    Form["TAB CREATE FORM<br/>- Delivery Method: Mesa<br/>- Table/Note input<br/>- Products: search/filter, add to cart (e.g. Bulgogi $13,990, Bibimbap $12,990, Ramen $11,990, Soju $5,990)<br/>- Cart: line items with modifiers and Total (e.g. x2 Bulgogi w/ Cerdo, Arroz; x1 Coca-Cola; Total: $29,970)<br/>- Actions: Cancelar / Crear Orden"]
    Backend["BACKEND PROCESSING<br/>TabController::store()<br/>- Create Tab record (status: CREATED)<br/>- Create Order record<br/>- Create OrderProduct records<br/>- Calculate totals<br/>- Send WebSocket notification"]

    Click --> Form
    Form -->|Submit| Backend
```

---

## Order Status Management Flow

```mermaid
flowchart TD
    Click["Staff Clicks Status Button"]
    FE["FRONTEND (useTabActions hook)<br/>1. Validate current status allows transition<br/>2. Show confirmation if needed<br/>3. Call dataProvider.update('tab/tab', { status: newStatus })"]
    API["API: PUT /api/tab/tab/{id}<br/>TabController::update()"]
    Validate["Validate status transition"]
    Handle["TabsNotificationService::handleStatusChange()<br/>- Update Tab.status<br/>- Update date_* field<br/>- Update Order.status (mapped)<br/>- sendNotification() → WebSocket"]
    Mall["If Mall order: MallTabNotificationService<br/>- Sync master tab status<br/>- Notify customer via MallSession channel"]
    Broadcast["WebSocket Broadcast"]
    Clients["ALL CONNECTED CLIENTS<br/>- Other staff apps receive update<br/>- Kitchen displays refresh<br/>- Customer app (if Mall) receives notification"]

    Click --> FE
    FE --> API
    API --> Validate
    Validate --> Handle
    Validate --> Mall
    Handle --> Broadcast
    Mall --> Broadcast
    Broadcast --> Clients
```

---

## Payment Processing Flow

```mermaid
flowchart TD
    Click["Staff Clicks Payment Button"]
    Dialog["PAYMENT DIALOG<br/>Tab #125 - Total: $29,970<br/>Payment Method: Efectivo / Tarjeta Débito / Tarjeta Crédito / Transferencia<br/>Service Fee: 10% = $2,997<br/>Grand Total: $32,967<br/>Status after payment: DELIVERED / CLOSED / Keep Current<br/>Actions: Cancelar / Procesar Pago"]
    API["API: PUT /api/tab/tab/{id}/payment<br/>TabController::payment()<br/>- Validate payment method exists<br/>- Calculate service fee<br/>- Create Payment record<br/>- Update Order.is_paid = true<br/>- Update Order.total_amount (with service fee)<br/>- Update Tab.status if requested"]

    Click --> Dialog
    Dialog -->|Process Payment| API
```

---

## Print/Download Flow

```mermaid
flowchart TD
    PrintBtn["Print Button [🖨️]"]
    DownloadBtn["Download Button [⬇️]"]
    PrintAPI["GET /tab/{id}/print"]
    DownloadAPI["GET /tab/{id}/download"]
    Controller["TabController<br/>printSaleNote() / downloadSaleNote()<br/>- Generate PDF from template<br/>- Include: products, totals, payments, customer info<br/>- Return PDF file"]
    OpenPrint["Open print dialog"]
    SaveFile["Save file locally"]

    PrintBtn --> PrintAPI --> Controller
    DownloadBtn --> DownloadAPI --> Controller
    Controller -->|print| OpenPrint
    Controller -->|download| SaveFile
```

---

## Bulk Operations Flow

```mermaid
flowchart TD
    ListView["TAB LIST VIEW<br/>[☑] Tab #125  [☑] Tab #124  [☐] Tab #123  [☑] Tab #122<br/>Selected: 3<br/>Bulk Actions: [Update Status ▼]"]
    Select["Select 'CONFIRMED'"]
    API["API: POST /api/tab/tab/bulk-update-status<br/>{ tab_ids: [125, 124, 122], status: 'CONFIRMED' }<br/>TabController::bulkUpdateStatus()"]
    Loop["For each tab:<br/>- Validate permission<br/>- handleStatusChange()<br/>- handleSlaveTabStatusChange() (if mall)"]

    ListView --> Select --> API --> Loop
```

---

## Real-Time Updates Flow

```mermaid
flowchart TD
    SA["Staff A (Cashier)"]
    SB["Staff B (Waiter)"]
    KD["Kitchen Display"]
    WS["WebSocket Server<br/>Channel: tenant.{id}.system"]

    SA --> SAChange["Staff A changes tab status"]
    SAChange --> API["API call"]
    API --> Backend["Laravel Backend broadcasts notification"]
    Backend --> SBSees["Staff B sees toast + list refreshes"]
    Backend --> KDSees["Kitchen sees toast + list refreshes"]

    SA -.-> WS
    SB -.-> WS
    KD -.-> WS
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

```mermaid
graph TD
    App["App"]
    AuthProvider["AuthProvider"]
    DashAdmin["DashAdmin"]
    LaravelEcho["LaravelEchoContext<br/>(WebSocket)"]
    Resources["Resources"]
    TabResource["TabResource<br/>(tab/tab)"]
    TabsList["TabsList"]
    TabListItem["TabListItem"]
    PaymentDialog["PaymentDialog"]
    CloseDialog["CloseDialog"]
    TabCreate["TabCreate"]
    ProductSelector["ProductSelector"]
    OrderSummary["OrderSummary"]
    TabEdit["TabEdit"]
    KitchenResource["KitchenResource<br/>(tab/kitchen)"]
    KitchenTabsList["KitchenTabsList"]
    OrderProductsView["OrderProductsView"]

    App --> AuthProvider
    AuthProvider --> DashAdmin
    DashAdmin --> LaravelEcho
    DashAdmin --> Resources
    Resources --> TabResource
    Resources --> KitchenResource
    TabResource --> TabsList
    TabResource --> TabCreate
    TabResource --> TabEdit
    TabsList --> TabListItem
    TabsList --> PaymentDialog
    TabsList --> CloseDialog
    TabCreate --> ProductSelector
    TabCreate --> OrderSummary
    KitchenResource --> KitchenTabsList
    KitchenTabsList --> OrderProductsView
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
