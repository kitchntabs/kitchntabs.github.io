# KitchnTabs ER Diagram: Domain Layer

**Business Logic & Feature Models (158 total)**

The Domain Layer implements all business features and workflows on top of the Core Layer foundation.

## Domain Areas Overview

| Domain | Models | Purpose |
|--------|--------|---------|
| **E-Commerce** | 47 | Products, categories, pricing, inventory, templates |
| **Delivery & Logistics** | 41 | Orders, shipments, tracking, drivers, routes |
| **Order Management** | 3 | Orders, order items, payments |
| **Marketplace** | 9 | Third-party integrations (Jumpseller, Uber Eats, etc.) |
| **Checkout & Payment** | 5 | Payment gateways, transactions, notifications |
| **Cash Management** | 7 | Cash counts, register reconciliation |
| **Mall Operations** | 3 | Multi-store sessions, notifications |
| **Campaigns** | 1 | Marketing campaigns & promotions |
| **Tab & Session** | 1 | Table sessions (POS) |

## Detailed Domain ER Diagrams

### 1. E-Commerce & Products (47 models)

**Core Entities**: Product, Category, Brand, Stock, Price, Gallery

```mermaid
erDiagram
    TENANT ||--o{ PRODUCT : "has"
    TENANT ||--o{ CATEGORY : "has"
    TENANT ||--o{ BRAND : "has"
    
    PRODUCT ||--o{ STOCK : "has"
    PRODUCT ||--o{ PRICE : "has"
    PRODUCT ||--o{ GALLERY : "contains"
    PRODUCT ||--o{ PRODUCT_METADATA : "has"
    
    CATEGORY ||--o{ CATEGORY : "parent"
    BRAND ||--o{ PRODUCT : "manufactures"
    
    PRODUCT ||--o{ MODIFIER_GROUP : "has"
    MODIFIER_GROUP ||--o{ MODIFIER : "contains"
    
    PRODUCT_TEMPLATE ||--o{ PRODUCT_TEMPLATE_COLUMN : "defines"
    PRODUCT ||--o{ PRODUCT_TEMPLATE : "uses"
    
    MARKETPLACE ||--o{ SYSTEM_MARKETPLACE_CATEGORY : "maps"
    CATEGORY ||--o{ SYSTEM_MARKETPLACE_CATEGORY : "syncs_to"
    
    PRICELIST ||--o{ PRICE : "groups"
    PRODUCT ||--o{ PRICELIST : "belongs_to"
```

**Key Models**:
- **Product** — Base product entity
- **Category** — Hierarchical product categories
- **Stock** — Inventory levels by location
- **Price** — Multi-level pricing (base, promotional, tier)
- **Gallery** — Product images & media
- **ModifierGroup/Modifier** — Product customizations (sizes, toppings)
- **ProductTemplate** — Data structure definitions

---

### 2. Order Management (3 models)

**Core Entities**: Order, OrderProduct, Payment

```mermaid
erDiagram
    TENANT ||--o{ ORDER : "has"
    USER ||--o{ ORDER : "places"
    
    ORDER ||--o{ ORDER_PRODUCT : "contains"
    PRODUCT ||--o{ ORDER_PRODUCT : "ordered_as"
    
    ORDER ||--o{ PAYMENT : "has"
    CHECKOUT_GATEWAY ||--o{ PAYMENT : "processes"
    
    ORDER ||--o{ DELIVERY_ORDER : "ships"
    DELIVERY_ORDER ||--o{ DRIVER : "assigned_to"
    
    MALL_SESSION ||--o{ ORDER : "originates_from"
    TAB ||--o{ ORDER : "billed_to"
```

**Key Models**:
- **Order** — Customer order with status machine
- **OrderProduct** — Order line items with modifiers
- **Payment** — Payment records, status tracking

---

### 3. Mall Operations (3 models)

**Core Entities**: Mall, MallSession, MallSessionNotification

```mermaid
erDiagram
    MALL ||--o{ MALL_SESSION : "hosts"
    TENANT ||--o{ MALL : "operates"
    
    MALL_SESSION ||--o{ MALL_SESSION_NOTIFICATION : "broadcasts"
    MALL_SESSION ||--o{ ORDER : "originates"
    
    USER ||--o{ MALL_SESSION : "initiates"
    MALL_SESSION ||--o{ ASSISTANCE_REQUEST : "tracks"
```

**Key Models**:
- **Mall** — Multi-tenant food court entity
- **MallSession** — Customer session across stores
- **MallSessionNotification** — Real-time notifications (WebSocket)

---

### 4. Marketplace Integration (9 models)

**Core Entities**: SystemMarketplace, Marketplace, MarketplaceCall

```mermaid
erDiagram
    SYSTEM_MARKETPLACE ||--o{ SYSTEM_MARKETPLACE_CATEGORY : "defines"
    SYSTEM_MARKETPLACE ||--o{ SYSTEM_MARKETPLACE_METADATA_FORMAT : "has"
    
    TENANT ||--o{ TENANT_SYSTEM_MARKETPLACE : "integrates"
    SYSTEM_MARKETPLACE ||--o{ TENANT_SYSTEM_MARKETPLACE : "available_to"
    
    TENANT ||--o{ MARKETPLACE : "manages"
    MARKETPLACE ||--o{ MARKETPLACE_CALL : "tracks_sync"
    MARKETPLACE ||--o{ MARKETPLACE_NOTIFICATION : "receives"
    
    CATEGORY ||--o{ OUTPUT_CATEGORY_MAPPING : "maps_to"
    SYSTEM_MARKETPLACE_CATEGORY ||--o{ OUTPUT_CATEGORY_MAPPING : "synced_as"
    
    MARKETPLACE ||--o{ TENANT_SYSTEM_MARKETPLACE : "syncs_to"
```

**Key Models**:
- **SystemMarketplace** — Supported marketplaces (Uber Eats, Jumpseller, etc.)
- **TenantSystemMarketplace** — Tenant's marketplace connection
- **MarketplaceCall** — API call logs and sync history
- **MarketplaceNotification** — Webhook notifications

---

### 5. Checkout & Payment (5 models)

**Core Entities**: SystemCheckoutGateway, CheckoutGateway, CheckoutGatewayTransaction

```mermaid
erDiagram
    SYSTEM_CHECKOUT_GATEWAY ||--o{ CHECKOUT_GATEWAY : "available_as"
    TENANT ||--o{ CHECKOUT_GATEWAY_TENANT : "configures"
    SYSTEM_CHECKOUT_GATEWAY ||--o{ CHECKOUT_GATEWAY_TENANT : "provided_by"
    
    CHECKOUT_GATEWAY ||--o{ CHECKOUT_GATEWAY_TRANSACTION : "processes"
    ORDER ||--o{ CHECKOUT_GATEWAY_TRANSACTION : "paid_via"
    
    CHECKOUT_GATEWAY ||--o{ CHECKOUT_GATEWAY_NOTIFICATION : "webhooks"
```

**Key Models**:
- **SystemCheckoutGateway** — Payment providers (Stripe, Mercado Pago, Transbank, etc.)
- **CheckoutGatewayTenant** — Tenant's payment credentials
- **CheckoutGatewayTransaction** — Payment records
- **CheckoutGatewayNotification** — Webhook events

---

### 6. Delivery & Logistics (41 models)

**Core Entities**: DeliveryOrder, Driver, DriverType, Route

```mermaid
erDiagram
    TENANT ||--o{ DELIVERY_ORDER : "ships"
    ORDER ||--o{ DELIVERY_ORDER : "creates"
    
    DRIVER ||--o{ DELIVERY_ORDER : "delivers"
    DRIVER ||--o{ DRIVER_TYPE : "has"
    
    DELIVERY_ORDER ||--o{ EVIDENCE : "tracks"
    DELIVERY_ORDER ||--o{ DELIVERY_ROUTE : "follows"
    
    EXPORT ||--o{ DELIVERY_ORDER : "exports_to"
    CONNECTION ||--o{ DELIVERY_ORDER : "syncs_via"
```

**Key Models**:
- **DeliveryOrder** — Shipment with tracking
- **Driver** — Delivery personnel
- **Evidence** — Proof of delivery (photos, signatures)
- **Export** — Integration with logistics (WMS, etc.)

---

### 7. Cash Management (7 models)

**Core Entities**: CashCount, CashCountPointOfSale, CashCountProduct

```mermaid
erDiagram
    TENANT ||--o{ CASH_COUNT : "performs"
    POINT_OF_SALE ||--o{ CASH_COUNT_POINT_OF_SALE : "belongs_to"
    
    CASH_COUNT ||--o{ CASH_COUNT_POINT_OF_SALE : "counts"
    CASH_COUNT ||--o{ CASH_COUNT_PRODUCT : "reconciles"
    
    PRODUCT ||--o{ CASH_COUNT_PRODUCT : "tracked_in"
    
    CASH_COUNT ||--o{ CASH_COUNT_POS_BREAKDOWN : "breaks_down"
    PRODUCT_SALE ||--o{ CASH_COUNT_PRODUCT_SALE : "validates"
```

**Key Models**:
- **CashCount** — Register reconciliation session
- **CashCountPointOfSale** — POS register details
- **CashCountProduct** — Item-level counting
- **ProductSale** — Sales line items

---

## Summary Table

| Domain | Models | Key Entities | Purpose |
|--------|--------|--------------|---------|
| E-Commerce | 47 | Product, Category, Stock, Price | Product catalog & inventory |
| Delivery | 41 | DeliveryOrder, Driver, Route | Order fulfillment |
| Marketplace | 9 | SystemMarketplace, Marketplace | 3rd-party sync |
| Checkout | 5 | CheckoutGateway, Transaction | Payment processing |
| Order | 3 | Order, OrderProduct, Payment | Order lifecycle |
| Cash Mgmt | 7 | CashCount, PointOfSale | Register reconciliation |
| Mall | 3 | Mall, MallSession, Notification | Multi-store operations |
| Campaign | 1 | CampaignTracker | Marketing campaigns |
| Tab/POS | 1 | Tab | Table session management |

## Cross-Domain Relationships

```mermaid
erDiagram
    CORE_LAYER ||--o{ ECOMMERCE : "provides_foundation"
    CORE_LAYER ||--o{ ORDER : "provides_foundation"
    CORE_LAYER ||--o{ CHECKOUT : "provides_foundation"
    CORE_LAYER ||--o{ DELIVERY : "provides_foundation"
    
    ECOMMERCE ||--o{ ORDER : "products_in"
    ECOMMERCE ||--o{ MARKETPLACE : "syncs_to"
    
    ORDER ||--o{ CHECKOUT : "payment_for"
    ORDER ||--o{ DELIVERY : "fulfillment_of"
    
    MARKETPLACE ||--o{ CHECKOUT : "enables"
    
    MALL ||--o{ ORDER : "originates"
    MALL ||--o{ CASH_MANAGEMENT : "reconciles"
    
    DELIVERY ||--o{ DRIVER : "assigns"
```

## Data Flow

1. **Order Creation** → E-Commerce (products) → Order (line items) → Checkout (payment) → Delivery (fulfillment)
2. **Marketplace Sync** → SystemMarketplace (available) → TenantSystemMarketplace (configured) → MarketplaceCall (periodic sync)
3. **Multi-Store** → Mall (entity) → MallSession (customer) → Order (items) → CashManagement (reconciliation)

---

## Design Principles

- **Domain Isolation**: Each domain is loosely coupled, communicates via events/APIs
- **Tenant Scoping**: All entities inherit tenant context from Core Layer
- **Audit Trail**: All modifications logged for compliance & debugging
- **Event-Driven**: Domain changes trigger notifications (WebSocket, webhooks, etc.)
- **Scalability**: Models designed for horizontal scaling via partitioning
