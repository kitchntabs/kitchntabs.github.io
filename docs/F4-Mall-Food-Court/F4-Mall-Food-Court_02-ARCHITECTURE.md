
# Mall App - System Architecture

## High-Level Architecture

```mermaid
graph TD
    Customer["Customer (Client)"] --> Frontend
    Staff["Restaurant Staff"] --> Frontend
    Admin["Mall Administrator"] --> Frontend
    Frontend["FRONTEND LAYER<br/>Mall Client (Public)<br/>Tenant App (Auth)<br/>Admin Dashboard (Auth)"] --> APIGateway
    APIGateway["API GATEWAY (Laravel)<br/>Public APIs /public/mall<br/>Auth APIs /mall<br/>Admin APIs /system/mall"] --> DB["MySQL Database"]
    APIGateway --> WS["WebSocket Server"]
    APIGateway --> Redis["Redis Cache"]
    WS --> FCM["FCM Push"]
```

## Component Architecture

### Backend Components

```mermaid
graph LR
    Entities["DOMAIN ENTITIES<br/>Tab, Order, Restaurant, Customer, Tenant"]
    UseCases["USE CASES<br/>CreateTab, UpdateTabStatus, QueryOrders, NotifyStaff, CalculateTotal"]
    Controllers["CONTROLLERS<br/>MallTabsController, MallSessionController, MallStoresController"]
    Services["SERVICES<br/>OrderService, NotificationService, TenantService"]
    Repositories["REPOSITORIES<br/>TabRepository, OrderRepository, RestaurantRepository"]
    Database["DATABASE<br/>MySQL Tables: tabs, orders, restaurants, tenants"]
    
    Entities --> UseCases
    UseCases --> Controllers
    Controllers --> Services
    Services --> Repositories
    Repositories --> Database
```

### Frontend Components

```mermaid
graph TD
    subgraph "Data Models"
        Tab["Tab Entity<br/>id, master_tab_id, tenant_id, status, items"]
        Order["Order Entity<br/>id, tab_id, products, total, status"]
        Restaurant["Restaurant Entity<br/>id, tenant_id, name, cuisines"]
        Tenant["Tenant Entity<br/>id, name, email, role"]
    end
    
    subgraph "API Responses"
        TabResponse["TabResponse<br/>id, status, items[], total, meta"]
        OrderResponse["OrderResponse<br/>id, products[], total, created_at"]
    end
    
    Tab --> Order
    Restaurant --> Tenant
    Tab --> TabResponse
    Order --> OrderResponse
```

## Data Flow Architecture

### Session-Based Data Flow

```mermaid
graph TD
    API["API Layer"] --> Service["Service Layer"]
    Service --> Repository["Repository Layer"]
    Repository --> DB["Database Layer"]
    
    subgraph "API Layer Responsibilities"
        A1["Validate requests"]
        A2["Transform DTOs"]
        A3["Return JSON responses"]
    end
    
    subgraph "Service Layer Responsibilities"
        S1["Business logic"]
        S2["Orchestration"]
        S3["Transactions"]
    end
    
    subgraph "Repository Layer Responsibilities"
        R1["Database queries"]
        R2["Model persistence"]
        R3["Data access"]
    end
```

### Order Creation Data Flow

```mermaid
sequenceDiagram
    participant Customer
    participant FrontendApp as Frontend
    participant APIGateway as API Gateway
    participant Services
    participant Database
    participant WebSocket
    participant Notification

    Customer->>FrontendApp: Select items and submit
    FrontendApp->>APIGateway: POST /api/public/mall/tab
    APIGateway->>Services: OrderService.createTab()
    Services->>Database: Save tab and orders
    Database-->>Services: Tab ID
    Services->>WebSocket: Broadcast tab.created event
    WebSocket-->>FrontendApp: Tab created notification
    Services->>Notification: Trigger notifications to staff/kitchen
    Notification-->>Notification: Send emails and FCM pushes
    APIGateway-->>FrontendApp: 201 Created
    FrontendApp-->>Customer: Show confirmation
```

## API Route Architecture

### Route Groups

| Group | Auth | Prefix | Purpose |
|-------|------|--------|---------|
| **Public Mall** | None | `/api/public/mall` | Customer ordering |
| **Mall Admin** | Sanctum | `/api/mall` | Tenant management |
| **System Mall** | Sanctum | `/api/system/mall` | System admin |

### Public API Endpoints

```
/api/public/mall/
├── session/
│   ├── POST   /create              → Create new session
│   ├── GET    /{hash}              → Get session details
│   ├── PUT    /{hash}              → Update session
│   ├── POST   /{hash}/complete     → Complete session
│   ├── POST   /{hash}/cancel       → Cancel session
│   ├── GET    /{hash}/notifications → Get notifications
│   └── POST   /{hash}/notifications/mark-read
├── stores/
│   ├── GET    /                    → List stores
│   ├── GET    /{id}                → Get store details
│   └── POST   /{id}/assistance     → Request assistance
├── products/
│   └── GET    /                    → List products
├── tab/
│   ├── GET    /                    → List tabs (filtered by session)
│   ├── POST   /                    → Create order
│   ├── GET    /{id}                → Get tab details
│   └── PUT    /{id}                → Update tab
├── {slug}/getAuth                  → Mall auth by slug
└── {sessionId}/getSessionAuth      → Session auth by hash
```

## Database Architecture

### Entity Relationships

```mermaid
graph TD
    Start["Customer places order"] --> GroupByTenant["Group products by restaurant"]
    GroupByTenant --> CreateMaster["Create master tab (aggregator)"]
    CreateMaster --> CreateTenant["Create tenant tab for each restaurant"]
    CreateTenant --> ValidateStock["Validate stock availability"]
    ValidateStock --> Decision{Stock OK?}
    Decision -->|No| CancelOrder["Cancel order and refund"]
    Decision -->|Yes| CreateOrders["Create order records"]
    CreateOrders --> NotifyStaff["Notify staff of new orders"]
    NotifyStaff --> NotifyCustomer["Notify customer of confirmation"]
    NotifyCustomer --> UpdateStatus["Update status to CONFIRMED"]
    UpdateStatus --> End["Order workflow complete"]
```

### Key Tables

| Table | Purpose |
|-------|---------|
| `malls` | Mall/food court entities |
| `mall_tenant` | Pivot: malls ↔ tenants |
| `mall_sessions` | Customer sessions |
| `mall_session_notifications` | Persisted notifications |
| `tabs` | Orders (master/tenant) |
| `orders` | Order details |
| `order_products` | Line items |
