
# Mall App - Flow Diagrams

## Overview

This document provides visual flow diagrams for the Mall App's key processes.

---

## 1. Session Initialization Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SESSION INITIALIZATION FLOW                           │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐
  │   Customer   │
  │   Scans QR   │
  └──────┬───────┘
         │
         ▼
  ┌──────────────────────────────────────────────────────┐
  │               /mall/session/{hash}                    │
  │               MallClientWrapper.tsx                   │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │              Check localStorage for hash             │
  │              dashStorage.getItem('mall-session-hash')│
  └──────────────────────┬───────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
  ┌──────────────┐               ┌──────────────┐
  │  Hash Found  │               │ Hash Missing │
  │  in Storage  │               │ Use URL Hash │
  └──────┬───────┘               └──────┬───────┘
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │            API: GET /public/mall/session/{hash}      │
  │            PublicMallController::getSessionByHash    │
  └──────────────────────┬───────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
  ┌──────────────┐               ┌──────────────┐
  │  Session     │               │  Session     │
  │  Exists      │               │  Not Found   │
  └──────┬───────┘               └──────┬───────┘
         │                               │
         │                               ▼
         │                       ┌──────────────┐
         │                       │ Create New   │
         │                       │ MallSession  │
         │                       └──────┬───────┘
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │         Check customer_name in session               │
  └──────────────────────┬───────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
  ┌──────────────┐               ┌──────────────┐
  │  Has Name    │               │  No Name     │
  │  Continue    │               │  Show Modal  │
  └──────┬───────┘               └──────┬───────┘
         │                               │
         │                               ▼
         │                       ┌──────────────────┐
         │                       │ MallAppMediator  │
         │                       │ Collect Name     │
         │                       └────────┬─────────┘
         │                                │
         │                                ▼
         │                       ┌──────────────────┐
         │                       │ API: POST        │
         │                       │ /session/update  │
         │                       │ customer_name    │
         │                       └────────┬─────────┘
         │                                │
         └───────────────┬────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │           Subscribe to WebSocket Channel             │
  │           mall-session.{session_id}                  │
  │           MallSessionEchoProvider                    │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │              Load Mall App Resources                 │
  │              MallClientAppResources                  │
  │              Show Restaurant List                    │
  └──────────────────────────────────────────────────────┘
```

---

## 2. Order Creation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ORDER CREATION FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐
  │  Customer    │
  │ Selects Menu │
  └──────┬───────┘
         │
         ▼
  ┌──────────────────────────────────────────────────────┐
  │         Browse Products (OrderProductsMallFilters)   │
  │         Filter by category, search                   │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │           Add Products to Cart (Tab)                 │
  │           MallOrderProducts Component                │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │              Review Order Summary                    │
  │              Show products, quantities, total        │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │                 Confirm Order                        │
  │                 Submit Button Click                  │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │         API: POST /mall/tabs                         │
  │         DASHMallClientDataProvider.create()          │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │                BACKEND PROCESSING                    │
  │                                                      │
  │  1. MallTabsController::store()                     │
  │  2. Get session from mall-session-hash header       │
  │  3. Validate products belong to tenant              │
  │  4. Create Tab record                               │
  │  5. Create Order record                             │
  │  6. Create OrderItem records                        │
  │  7. Link Tab to MallSession                         │
  │  8. Dispatch TabCreationJob                         │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │              TabCreationJob                          │
  │                                                      │
  │  1. Update Tab status to CREATED                    │
  │  2. Dispatch notification                           │
  │                                                      │
  │     MallSessionTabCreationNotification              │
  │       - via('broadcast', 'database', 'fcm')         │
  │       - channel: mall-session.{session_id}          │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
  ┌──────────────┐               ┌──────────────┐
  │   Customer   │               │  Restaurant  │
  │   Receives   │               │  Receives    │
  │  Confirmation│               │ New Order    │
  └──────────────┘               └──────────────┘
```

---

## 3. Order Status Update Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ORDER STATUS UPDATE FLOW                                │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌────────────────┐
  │  Restaurant    │
  │  Staff Updates │
  │  Order Status  │
  └───────┬────────┘
          │
          ▼
  ┌──────────────────────────────────────────────────────┐
  │         Restaurant Dashboard (Dash Admin)            │
  │         Select new status from dropdown              │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │         API: PUT /admin/tabs/{id}                    │
  │         { status: 'IN_PREPARATION' }                 │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │                BACKEND PROCESSING                    │
  │                                                      │
  │  TabsController::update()                           │
  │    │                                                 │
  │    ├─▶ Update Tab.status                            │
  │    │                                                 │
  │    ├─▶ If Tab has mall_session_id:                  │
  │    │      Call MallOrderSyncService                 │
  │    │                                                 │
  │    └─▶ dispatch(TabStatusChangedJob)                │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │           MallOrderSyncService::syncOrderStatus      │
  │                                                      │
  │  1. Get MallSession from Tab                        │
  │  2. Get tenant info (restaurant name)               │
  │  3. Build notification payload:                     │
  │     - status, tenant_id, tenant_name                │
  │     - master_tab_id, tenant_tab_id                  │
  │     - products, timestamp                           │
  │                                                      │
  │  4. Dispatch MallSessionOrderStatusNotification     │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │       MallSessionOrderStatusNotification             │
  │                                                      │
  │  extends BaseMallSessionNotification                │
  │                                                      │
  │  Channels:                                          │
  │    - broadcast (Pusher/Soketi)                      │
  │    - database (MallSessionNotification)             │
  │    - fcm (Firebase Cloud Messaging)                 │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │  WebSocket   │ │   Database   │ │     FCM      │
  │  (Pusher)    │ │   Storage    │ │    Push      │
  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
         │               │               │
         │               │               │
         │               ▼               │
         │        ┌──────────────┐       │
         │        │ MallSession  │       │
         │        │ Notification │       │
         │        │   (record)   │       │
         │        └──────────────┘       │
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │              CUSTOMER RECEIVES                       │
  │                                                      │
  │  Browser (WebSocket):                               │
  │    - LaravelEchoContext receives event              │
  │    - MallClientTabsList.useEffect triggered         │
  │    - Toast notification shown                       │
  │    - useRefresh() called to update list             │
  │                                                      │
  │  Mobile (FCM):                                      │
  │    - Push notification displayed                    │
  │    - Tapping opens order details                    │
  │                                                      │
  └──────────────────────────────────────────────────────┘
```

---

## 4. WebSocket Event Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WEBSOCKET EVENT FLOW                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │         Laravel Backend             │
                    │                                     │
                    │  broadcast(new Notification())     │
                    │        │                            │
                    │        ▼                            │
                    │  ┌──────────────┐                   │
                    │  │ Pusher/Soketi│                   │
                    │  │   Driver     │                   │
                    │  └──────┬───────┘                   │
                    │         │                           │
                    └─────────┼───────────────────────────┘
                              │
                              │ WebSocket Message
                              │
                              ▼
          ┌───────────────────────────────────────────────────┐
          │                 Pusher/Soketi Server              │
          │                                                   │
          │  Channel: private-mall-session.{session_id}       │
          │  Event: .mall_order_status_update                 │
          │                                                   │
          └───────────────────────┬───────────────────────────┘
                                  │
                                  │ WebSocket Push
                                  │
                                  ▼
          ┌───────────────────────────────────────────────────┐
          │              React Frontend (Browser)             │
          │                                                   │
          │  ┌─────────────────────────────────────────────┐  │
          │  │           LaravelEchoContext                │  │
          │  │                                             │  │
          │  │  echo.private(`mall-session.${sessionId}`) │  │
          │  │    .listen('.mall_order_status_update',    │  │
          │  │      (event) => setLastEvent(event))       │  │
          │  │                                             │  │
          │  └──────────────────┬──────────────────────────┘  │
          │                     │                             │
          │                     │ Context Update              │
          │                     ▼                             │
          │  ┌─────────────────────────────────────────────┐  │
          │  │         MallClientTabsList                  │  │
          │  │                                             │  │
          │  │  useEffect(() => {                         │  │
          │  │    if (lastEvent?.type === 'mall_order...')│  │
          │  │      showToast(message);                   │  │
          │  │      refresh();                            │  │
          │  │  }, [lastEvent])                           │  │
          │  │                                             │  │
          │  └─────────────────────────────────────────────┘  │
          │                                                   │
          └───────────────────────────────────────────────────┘
```

---

## 5. FCM Push Notification Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FCM PUSH NOTIFICATION FLOW                              │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────┐
  │  Customer Opens Mall App in Browser                  │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │           Request Notification Permission            │
  │           Notification.requestPermission()           │
  └──────────────────────┬───────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
  ┌──────────────┐               ┌──────────────┐
  │   Granted    │               │   Denied     │
  └──────┬───────┘               └──────┬───────┘
         │                               │
         │                               └──▶ (WebSocket only)
         │
         ▼
  ┌──────────────────────────────────────────────────────┐
  │            Get FCM Token from Firebase               │
  │            messaging.getToken()                      │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │       Register Token with Mall Session               │
  │       API: POST /public/mall/session/{hash}/token    │
  │       { fcm_token: 'abc123...' }                    │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │       MallSession.fcm_token = 'abc123...'           │
  │       Token stored for push notifications           │
  └──────────────────────────────────────────────────────┘


            WHEN ORDER STATUS CHANGES:

  ┌──────────────────────────────────────────────────────┐
  │       MallSessionOrderStatusNotification             │
  │       ->via('fcm')                                   │
  │       ->toFcm($notifiable)                          │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │                Firebase Servers                      │
  │                                                      │
  │  Send to token: 'abc123...'                         │
  │  Payload: {                                          │
  │    notification: {                                   │
  │      title: "Actualización de orden",               │
  │      body: "Restaurante X: En preparación"          │
  │    },                                                │
  │    data: {                                           │
  │      type: "mall_order_status_update",              │
  │      status: "IN_PREPARATION",                       │
  │      tenant_id: "123"                               │
  │    }                                                 │
  │  }                                                   │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │            Customer's Browser/Device                 │
  │                                                      │
  │  ┌────────────────────────────────────────────────┐  │
  │  │  🔔 Actualización de orden                    │  │
  │  │  Restaurante X: En preparación               │  │
  │  └────────────────────────────────────────────────┘  │
  │                                                      │
  │  (Even if browser tab is in background)             │
  └──────────────────────────────────────────────────────┘
```

---

## 6. Multi-Restaurant Order Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MULTI-RESTAURANT ORDER FLOW                               │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────┐
  │                   Mall Session                       │
  │                                                      │
  │  id: 100                                            │
  │  hash: "abc123"                                     │
  │  customer_name: "Juan"                              │
  │  mall_id: 1                                         │
  │                                                      │
  └───────────────────────┬──────────────────────────────┘
                          │
                          │ Creates multiple tabs
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
  ┌───────────┐     ┌───────────┐     ┌───────────┐
  │  Tab #1   │     │  Tab #2   │     │  Tab #3   │
  │           │     │           │     │           │
  │ tenant:   │     │ tenant:   │     │ tenant:   │
  │ Pizza     │     │ Sushi     │     │ Burger    │
  │ Place     │     │ Bar       │     │ Joint     │
  │           │     │           │     │           │
  │ status:   │     │ status:   │     │ status:   │
  │ PREPARED  │     │ IN_PREP   │     │ CONFIRMED │
  └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
        │                 │                 │
        │                 │                 │
        ▼                 ▼                 ▼
  ┌───────────┐     ┌───────────┐     ┌───────────┐
  │ Order #1  │     │ Order #2  │     │ Order #3  │
  │           │     │           │     │           │
  │ - Pizza   │     │ - Rolls   │     │ - Burger  │
  │ - Coke    │     │ - Sake    │     │ - Fries   │
  └───────────┘     └───────────┘     └───────────┘


              CUSTOMER VIEW:

  ┌─────────────────────────────────────────────────────┐
  │                   Mis Órdenes                       │
  ├─────────────────────────────────────────────────────┤
  │                                                     │
  │  ┌─────────────────────────────────────────────┐   │
  │  │ 🍕 Pizza Place                    PREPARADO │   │
  │  │ ████████████████████░░░░░░░░░░░  80%       │   │
  │  │ Pizza Margherita, Coca-Cola               │   │
  │  └─────────────────────────────────────────────┘   │
  │                                                     │
  │  ┌─────────────────────────────────────────────┐   │
  │  │ 🍣 Sushi Bar                  EN PREPARACIÓN │   │
  │  │ ████████████░░░░░░░░░░░░░░░░  60%          │   │
  │  │ California Rolls, Sake                     │   │
  │  └─────────────────────────────────────────────┘   │
  │                                                     │
  │  ┌─────────────────────────────────────────────┐   │
  │  │ 🍔 Burger Joint                  CONFIRMADO │   │
  │  │ ████████░░░░░░░░░░░░░░░░░░░░░  40%         │   │
  │  │ Cheeseburger, French Fries                │   │
  │  └─────────────────────────────────────────────┘   │
  │                                                     │
  └─────────────────────────────────────────────────────┘


              STATUS UPDATES (Independent):

  Restaurant A changes to DELIVERED
        │
        ▼
  Notification: "Pizza Place ha entregado tu orden"
        │
        ▼
  Tab #1 status: DELIVERED
  Tab #2 status: IN_PREPARATION (unchanged)
  Tab #3 status: CONFIRMED (unchanged)
```

---

## 7. Database Notification Storage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   DATABASE NOTIFICATION STORAGE FLOW                         │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────┐
  │       MallSessionOrderStatusNotification             │
  │       (implements ShouldQueue)                       │
  │                                                      │
  │       via(): ['broadcast', 'database', 'fcm']       │
  └──────────────────────┬───────────────────────────────┘
                         │
                         │ Database channel
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │       toDatabase($notifiable) method                 │
  │                                                      │
  │  return [                                           │
  │    'type' => 'mall_order_status_update',           │
  │    'title' => 'Actualización de orden',            │
  │    'message' => 'Tu orden está en preparación',    │
  │    'data' => [                                      │
  │      'status' => 'IN_PREPARATION',                 │
  │      'tenant_id' => 123,                           │
  │      'tenant_name' => 'Pizza Place',               │
  │      'products' => [...],                          │
  │    ],                                               │
  │  ];                                                 │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │   MallSessionNotificationStorageService              │
  │                                                      │
  │   storeNotification(MallSession $session, $data)    │
  │                                                      │
  │   Creates: MallSessionNotification record           │
  │     - mall_session_id: 100                         │
  │     - type: 'mall_order_status_update'             │
  │     - title: 'Actualización de orden'              │
  │     - message: 'Tu orden está en preparación'      │
  │     - data: {json}                                  │
  │     - is_read: false                               │
  │     - created_at: now()                            │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │            mall_session_notifications table          │
  │                                                      │
  │  ┌────┬────────────┬────────────────────────────┐   │
  │  │ id │ session_id │ type                       │   │
  │  ├────┼────────────┼────────────────────────────┤   │
  │  │  1 │        100 │ mall_session_tab_creation  │   │
  │  │  2 │        100 │ mall_order_status_update   │   │
  │  │  3 │        100 │ mall_order_status_update   │   │
  │  │  4 │        100 │ mall_order_status_update   │   │
  │  └────┴────────────┴────────────────────────────┘   │
  │                                                      │
  └──────────────────────────────────────────────────────┘


              CUSTOMER RETRIEVES NOTIFICATIONS:

  ┌──────────────────────────────────────────────────────┐
  │  API: GET /public/mall/session/{hash}/notifications │
  │                                                      │
  │  PublicMallController::getNotifications()           │
  │                                                      │
  │  Returns: [                                         │
  │    {                                                │
  │      id: 4,                                         │
  │      type: 'mall_order_status_update',             │
  │      title: 'Actualización de orden',              │
  │      message: 'Tu orden está lista para recoger',  │
  │      tenant_name: 'Pizza Place',                   │
  │      status: 'PREPARED',                           │
  │      created_at: '2024-01-15T12:30:00Z',          │
  │      is_read: false                                │
  │    },                                               │
  │    ...                                              │
  │  ]                                                  │
  │                                                      │
  └──────────────────────────────────────────────────────┘
```

---

## 8. Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ERROR HANDLING FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────────────────┐
  │                        WEBSOCKET DISCONNECTION                            │
  │                                                                           │
  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                   │
  │  │  Connected  │───▶│ Disconnect  │───▶│  Reconnect  │                   │
  │  │             │    │  Detected   │    │  Attempt    │                   │
  │  └─────────────┘    └─────────────┘    └──────┬──────┘                   │
  │                                               │                           │
  │                          ┌────────────────────┼────────────────────┐     │
  │                          │                    │                    │     │
  │                          ▼                    ▼                    ▼     │
  │                    ┌───────────┐        ┌───────────┐        ┌─────────┐ │
  │                    │  Success  │        │  Retry    │        │  Fail   │ │
  │                    │  Resume   │        │  (backoff)│        │  Alert  │ │
  │                    └───────────┘        └───────────┘        └─────────┘ │
  │                                                                           │
  └───────────────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────────────────┐
  │                          API ERROR HANDLING                               │
  │                                                                           │
  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                   │
  │  │  API Call   │───▶│   Error     │───▶│   Handle    │                   │
  │  │             │    │   Response  │    │   Error     │                   │
  │  └─────────────┘    └─────────────┘    └──────┬──────┘                   │
  │                                               │                           │
  │                     ┌─────────────────────────┼─────────────────────────┐│
  │                     │           │             │             │           ││
  │                     ▼           ▼             ▼             ▼           ││
  │               ┌─────────┐┌─────────┐   ┌─────────┐   ┌─────────┐       ││
  │               │   401   ││   404   │   │   422   │   │   500   │       ││
  │               │ Redirect││  Show   │   │  Show   │   │  Show   │       ││
  │               │ Login   ││ NotFound│   │ Errors  │   │  Retry  │       ││
  │               └─────────┘└─────────┘   └─────────┘   └─────────┘       ││
  │                                                                         ││
  └─────────────────────────────────────────────────────────────────────────┘│

  ┌───────────────────────────────────────────────────────────────────────────┐
  │                         FCM ERROR HANDLING                                │
  │                                                                           │
  │  ┌─────────────┐    ┌─────────────┐                                      │
  │  │ FCM Token   │───▶│   Invalid   │                                      │
  │  │ Expired     │    │   Token     │                                      │
  │  └─────────────┘    └──────┬──────┘                                      │
  │                            │                                              │
  │                            ▼                                              │
  │                     ┌─────────────┐    ┌─────────────┐                   │
  │                     │  Refresh    │───▶│  Update in  │                   │
  │                     │  Token      │    │  Session    │                   │
  │                     └─────────────┘    └─────────────┘                   │
  │                                                                           │
  └───────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference

| Flow | Trigger | Key Components |
|------|---------|----------------|
| Session Init | QR Scan | MallClientWrapper, PublicMallController |
| Order Create | Confirm Button | DASHMallClientDataProvider, MallTabsController |
| Status Update | Staff Action | MallOrderSyncService, MallSessionOrderStatusNotification |
| WebSocket | Any Notification | LaravelEchoContext, Pusher |
| FCM Push | Notification dispatch | Firebase, toFcm() |
| Multi-Order | Multiple restaurants | MallSession, multiple Tabs |
| DB Storage | Notification | MallSessionNotificationStorageService |
