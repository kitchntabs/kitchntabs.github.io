---
title: Mall App - Architecture
layout: default
nav_order: 2
parent: Mall Application
---

# Mall App - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           MALL APP SYSTEM                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────┐   │
│  │   Customer   │    │  Restaurant  │    │    Mall Administrator    │   │
│  │   (Client)   │    │    Staff     │    │                          │   │
│  └──────┬───────┘    └──────┬───────┘    └────────────┬─────────────┘   │
│         │                   │                         │                  │
│         ▼                   ▼                         ▼                  │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      FRONTEND LAYER                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │   │
│  │  │ Mall Client │  │ Tenant App  │  │      Admin Dashboard    │   │   │
│  │  │  (Public)   │  │ (Auth)      │  │        (Auth)           │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                       API GATEWAY (Laravel)                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │   │
│  │  │ Public APIs  │  │ Auth APIs    │  │   Admin APIs         │   │   │
│  │  │ /public/mall │  │ /mall        │  │   /system/mall       │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│         ┌──────────────────────────┼──────────────────────────┐         │
│         ▼                          ▼                          ▼         │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐   │
│  │   MySQL     │           │  WebSocket  │           │    Redis    │   │
│  │  Database   │           │   Server    │           │   Cache     │   │
│  └─────────────┘           └─────────────┘           └─────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│                           ┌─────────────┐                               │
│                           │     FCM     │                               │
│                           │    Push     │                               │
│                           └─────────────┘                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Backend Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     LARAVEL BACKEND                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    CONTROLLERS                           │    │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐   │    │
│  │  │ MallSession     │  │ MallTabs                    │   │    │
│  │  │ Controller      │  │ Controller                  │   │    │
│  │  │ - createSession │  │ - _create (master+tenant)   │   │    │
│  │  │ - getSessionAuth│  │ - updateTenantTabStatus     │   │    │
│  │  │ - getNotifs     │  │ - cancelMallOrder           │   │    │
│  │  └─────────────────┘  └─────────────────────────────┘   │    │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐   │    │
│  │  │ MallStores      │  │ PublicMall                  │   │    │
│  │  │ Controller      │  │ Controller                  │   │    │
│  │  │ - assistance    │  │ - getAuth                   │   │    │
│  │  └─────────────────┘  └─────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      SERVICES                            │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ MallOrderSyncService                            │    │    │
│  │  │ - syncTenantTabStatusWithMaster()               │    │    │
│  │  │ - syncMasterOrderProducts()                     │    │    │
│  │  │ - notifyMallSession()                           │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ TabsNotificationService                         │    │    │
│  │  │ - handleSlaveTabStatusChange()                  │    │    │
│  │  │ - notifyMallSession()                           │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                       MODELS                             │    │
│  │  ┌────────────┐  ┌───────────────┐  ┌────────────────┐  │    │
│  │  │    Mall    │  │  MallSession  │  │ MallSession    │  │    │
│  │  │            │  │               │  │ Notification   │  │    │
│  │  └────────────┘  └───────────────┘  └────────────────┘  │    │
│  │  ┌────────────┐  ┌───────────────┐  ┌────────────────┐  │    │
│  │  │    Tab     │  │     Order     │  │    Tenant      │  │    │
│  │  │(master/    │  │               │  │                │  │    │
│  │  │ tenant)    │  │               │  │                │  │    │
│  │  └────────────┘  └───────────────┘  └────────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   NOTIFICATIONS                          │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ BaseMallSessionNotification                     │    │    │
│  │  │ - buildNotification()                           │    │    │
│  │  │ - persistNotification()                         │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │         ▲                              ▲                 │    │
│  │         │                              │                 │    │
│  │  ┌──────┴──────────┐        ┌─────────┴─────────┐       │    │
│  │  │ OrderStatus     │        │ TabCreation       │       │    │
│  │  │ Notification    │        │ Notification      │       │    │
│  │  └─────────────────┘        └───────────────────┘       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Frontend Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     REACT FRONTEND                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  APP ENTRY POINTS                        │    │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐   │    │
│  │  │  main.tsx       │  │  KitchnTabsMallBootstrap    │   │    │
│  │  │  (Redux setup)  │  │  (Auth routing)             │   │    │
│  │  └─────────────────┘  └─────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                  │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │ MallClient    │  │ MallApp       │  │ MallPublic    │       │
│  │ Wrapper       │  │ Wrapper       │  │ Wrapper       │       │
│  │ (Public)      │  │ (Admin)       │  │ (Landing)     │       │
│  └───────┬───────┘  └───────────────┘  └───────────────┘       │
│          │                                                       │
│          ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   DATA PROVIDERS                         │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ DASHMallClientDataProvider                      │    │    │
│  │  │ - Resource mapping (tab → public/mall/tab)      │    │    │
│  │  │ - Auto-inject mall_session filter               │    │    │
│  │  │ - Session ID from localStorage                  │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                 WEBSOCKET CONTEXT                        │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ MallSessionEchoContext                          │    │    │
│  │  │ - Subscribe to session.{hash} channel           │    │    │
│  │  │ - Track product/tenant statuses                 │    │    │
│  │  │ - Provide lastEvent to consumers                │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   UI COMPONENTS                          │    │
│  │  ┌────────────────┐  ┌────────────────────────────┐     │    │
│  │  │ MallClient     │  │ MallOrderProductsField     │     │    │
│  │  │ TabsList       │  │ (Product selection)        │     │    │
│  │  └────────────────┘  └────────────────────────────┘     │    │
│  │  ┌────────────────┐  ┌────────────────────────────┐     │    │
│  │  │ MallSession    │  │ MallSessionOrder           │     │    │
│  │  │ OrderProgress  │  │ Notifications              │     │    │
│  │  └────────────────┘  └────────────────────────────┘     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

### Session-Based Data Flow

```
┌────────────────────────────────────────────────────────────────────┐
│                    SESSION DATA FLOW                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   CUSTOMER                    BACKEND                   DATABASE    │
│   ─────────                   ───────                   ────────    │
│                                                                     │
│   ┌───────────┐                                                     │
│   │ Scan QR   │                                                     │
│   │ Code      │                                                     │
│   └─────┬─────┘                                                     │
│         │                                                           │
│         │ GET /public/mall/{hash}/getSessionAuth                    │
│         ├────────────────────────────►┌─────────────┐               │
│         │                             │ Validate    │               │
│         │                             │ Session     │               │
│         │                             └──────┬──────┘               │
│         │                                    │                      │
│         │                                    │ UPDATE mall_sessions │
│         │                                    │ status = 'active'    │
│         │                                    │ meta = {ip, agent}   │
│         │                                    ├─────────────────────►│
│         │                                    │                      │
│         │◄───────────────────────────────────┤                      │
│         │  Auth response (tenant, settings)  │                      │
│         │                                                           │
│   ┌─────┴─────┐                                                     │
│   │ Store in  │                                                     │
│   │ localStorage│                                                   │
│   │ mall-session│                                                   │
│   │ -hash     │                                                     │
│   └───────────┘                                                     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Order Creation Data Flow

```
┌────────────────────────────────────────────────────────────────────┐
│                    ORDER CREATION FLOW                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   CUSTOMER          DATA PROVIDER         BACKEND         DATABASE  │
│   ────────          ─────────────         ───────         ────────  │
│                                                                     │
│   ┌──────────┐                                                      │
│   │ Select   │                                                      │
│   │ Products │                                                      │
│   └────┬─────┘                                                      │
│        │                                                            │
│        │ Submit                                                     │
│        ▼                                                            │
│   ┌──────────┐                                                      │
│   │ Validate │                                                      │
│   │ Customer │                                                      │
│   │ Info     │                                                      │
│   └────┬─────┘                                                      │
│        │                                                            │
│        │ create(tab, data)                                          │
│        ├──────────────────►┌────────────┐                           │
│        │                   │ Inject     │                           │
│        │                   │ mall_session│                          │
│        │                   │ mall_id    │                           │
│        │                   └─────┬──────┘                           │
│        │                         │                                  │
│        │                         │ POST /public/mall/tab            │
│        │                         ├──────────────►┌─────────┐        │
│        │                         │               │ Create  │        │
│        │                         │               │ Master  │        │
│        │                         │               │ Tab     │───────►│
│        │                         │               └────┬────┘        │
│        │                         │                    │             │
│        │                         │               ┌────▼────┐        │
│        │                         │               │ Create  │        │
│        │                         │               │ Tenant  │───────►│
│        │                         │               │ Tabs    │        │
│        │                         │               └────┬────┘        │
│        │                         │                    │             │
│        │                         │               ┌────▼────┐        │
│        │                         │               │ Send    │        │
│        │                         │               │ Notifs  │        │
│        │                         │               └─────────┘        │
│        │◄────────────────────────┤                                  │
│        │  Master Tab Response    │                                  │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
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

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE RELATIONSHIPS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐         ┌───────────────┐                        │
│   │   Mall   │◄────────┤  mall_tenant  │                        │
│   │          │  1:M    │   (pivot)     │                        │
│   └────┬─────┘         └───────┬───────┘                        │
│        │                       │                                 │
│        │ 1:M                   │ M:1                             │
│        ▼                       ▼                                 │
│   ┌──────────────┐       ┌──────────┐                           │
│   │ MallSession  │       │  Tenant  │                           │
│   │              │       │          │                           │
│   │ - hash       │       │          │                           │
│   │ - status     │       │          │                           │
│   │ - meta       │       │          │                           │
│   └──────┬───────┘       └────┬─────┘                           │
│          │                    │                                  │
│          │ 1:M                │ 1:M                              │
│          ▼                    ▼                                  │
│   ┌──────────────────┐  ┌──────────┐                            │
│   │ MallSession      │  │   Tab    │◄─────────┐                 │
│   │ Notification     │  │          │          │                 │
│   └──────────────────┘  │ - status │          │ master_tab_id   │
│                         │ - is_master_tab     │                 │
│                         └────┬─────┘──────────┘                 │
│                              │                                   │
│                              │ 1:1                               │
│                              ▼                                   │
│                         ┌──────────┐                            │
│                         │  Order   │                            │
│                         │          │◄─────────┐                 │
│                         │ - status │          │ parent_order_id │
│                         │ - brokerable_type   │                 │
│                         │ - brokerable_id     │                 │
│                         └────┬─────┘──────────┘                 │
│                              │                                   │
│                              │ 1:M                               │
│                              ▼                                   │
│                         ┌──────────────┐                        │
│                         │ OrderProduct │                        │
│                         │              │                        │
│                         │ - product_id │                        │
│                         │ - quantity   │                        │
│                         │ - status     │                        │
│                         └──────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
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
