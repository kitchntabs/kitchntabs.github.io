
# Mall App - Flow Diagrams

## Overview

This document provides visual flow diagrams for the Mall App's key processes.

---

## 1. Session Initialization Flow

```mermaid
flowchart TD
    A["Customer Scans QR"] --> B["/mall/session/{hash}<br/>MallClientWrapper.tsx"]
    B --> C["Check localStorage for hash<br/>dashStorage.getItem('mall-session-hash')"]
    C --> D["Hash Found in Storage"]
    C --> E["Hash Missing<br/>Use URL Hash"]
    D --> F["API: GET /public/mall/session/{hash}<br/>PublicMallController::getSessionByHash"]
    E --> F
    F --> G["Session Exists"]
    F --> H["Session Not Found"]
    H --> I["Create New MallSession"]
    G --> J["Check customer_name in session"]
    I --> J
    J --> K["Has Name<br/>Continue"]
    J --> L["No Name<br/>Show Modal"]
    L --> M["MallAppMediator<br/>Collect Name"]
    M --> N["API: POST /session/update<br/>customer_name"]
    K --> O["Subscribe to WebSocket Channel<br/>mall-session.{session_id}<br/>MallSessionEchoProvider"]
    N --> O
    O --> P["Load Mall App Resources<br/>MallClientAppResources<br/>Show Restaurant List"]
```

---

## 2. Order Creation Flow

```mermaid
flowchart TD
    A["Customer Selects Menu"] --> B["Browse Products (OrderProductsMallFilters)<br/>Filter by category, search"]
    B --> C["Add Products to Cart (Tab)<br/>MallOrderProducts Component"]
    C --> D["Review Order Summary<br/>Show products, quantities, total"]
    D --> E["Confirm Order<br/>Submit Button Click"]
    E --> F["API: POST /mall/tabs<br/>DASHMallClientDataProvider.create()"]
    F --> G["BACKEND PROCESSING<br/>1. MallTabsController::store()<br/>2. Get session from mall-session-hash header<br/>3. Validate products belong to tenant<br/>4. Create Tab record<br/>5. Create Order record<br/>6. Create OrderItem records<br/>7. Link Tab to MallSession<br/>8. Dispatch TabCreationJob"]
    G --> H["TabCreationJob<br/>1. Update Tab status to CREATED<br/>2. Dispatch notification<br/><br/>MallSessionTabCreationNotification<br/>- via('broadcast', 'database', 'fcm')<br/>- channel: mall-session.{session_id}"]
    H --> I["Customer Receives Confirmation"]
    H --> J["Restaurant Receives New Order"]
```

---

## 3. Order Status Update Flow

```mermaid
flowchart TD
    A["Restaurant Staff Updates Order Status"] --> B["Restaurant Dashboard (Dash Admin)<br/>Select new status from dropdown"]
    B --> C["API: PUT /admin/tabs/{id}<br/>{ status: 'IN_PREPARATION' }"]
    C --> D["BACKEND PROCESSING<br/>TabsController::update()"]
    D --> D1["Update Tab.status"]
    D --> D2["If Tab has mall_session_id:<br/>Call MallOrderSyncService"]
    D --> D3["dispatch(TabStatusChangedJob)"]
    D2 --> E["MallOrderSyncService::syncOrderStatus<br/>1. Get MallSession from Tab<br/>2. Get tenant info (restaurant name)<br/>3. Build notification payload:<br/>- status, tenant_id, tenant_name<br/>- master_tab_id, tenant_tab_id<br/>- products, timestamp<br/>4. Dispatch MallSessionOrderStatusNotification"]
    E --> F["MallSessionOrderStatusNotification<br/>extends BaseMallSessionNotification<br/><br/>Channels:<br/>- broadcast (Pusher/Soketi)<br/>- database (MallSessionNotification)<br/>- fcm (Firebase Cloud Messaging)"]
    F --> G["WebSocket (Pusher)"]
    F --> H["Database Storage"]
    F --> I["FCM Push"]
    H --> J["MallSession Notification (record)"]
    G --> K["CUSTOMER RECEIVES<br/><br/>Browser (WebSocket):<br/>- LaravelEchoContext receives event<br/>- MallClientTabsList.useEffect triggered<br/>- Toast notification shown<br/>- useRefresh() called to update list<br/><br/>Mobile (FCM):<br/>- Push notification displayed<br/>- Tapping opens order details"]
    J --> K
    I --> K
```

---

## 4. WebSocket Event Flow

```mermaid
flowchart TD
    subgraph Backend["Laravel Backend"]
        A["broadcast(new Notification())"] --> B["Pusher/Soketi Driver"]
    end
    B -- "WebSocket Message" --> C
    subgraph Server["Pusher/Soketi Server"]
        C["Channel: private-mall-session.{session_id}<br/>Event: .mall_order_status_update"]
    end
    C -- "WebSocket Push" --> D
    subgraph Frontend["React Frontend (Browser)"]
        D["LaravelEchoContext<br/>echo.private(`mall-session.${sessionId}`)<br/>.listen('.mall_order_status_update',<br/>(event) => setLastEvent(event))"]
        D -- "Context Update" --> E["MallClientTabsList<br/>useEffect(() => {<br/>if (lastEvent?.type === 'mall_order...')<br/>showToast(message);<br/>refresh();<br/>}, [lastEvent])"]
    end
```

---

## 5. FCM Push Notification Flow

```mermaid
flowchart TD
    A["Customer Opens Mall App in Browser"] --> B["Request Notification Permission<br/>Notification.requestPermission()"]
    B --> C["Granted"]
    B --> D["Denied"]
    D -.-> E["(WebSocket only)"]
    C --> F["Get FCM Token from Firebase<br/>messaging.getToken()"]
    F --> G["Register Token with Mall Session<br/>API: POST /public/mall/session/{hash}/token<br/>{ fcm_token: 'abc123...' }"]
    G --> H["MallSession.fcm_token = 'abc123...'<br/>Token stored for push notifications"]

    H2["WHEN ORDER STATUS CHANGES:<br/>MallSessionOrderStatusNotification<br/>-&gt;via('fcm')<br/>-&gt;toFcm($notifiable)"] --> I["Firebase Servers<br/>Send to token: 'abc123...'<br/>Payload: {<br/>notification: {<br/>title: 'Actualización de orden',<br/>body: 'Restaurante X: En preparación'<br/>},<br/>data: {<br/>type: 'mall_order_status_update',<br/>status: 'IN_PREPARATION',<br/>tenant_id: '123'<br/>}<br/>}"]
    I --> J["Customer's Browser/Device<br/>🔔 Actualización de orden<br/>Restaurante X: En preparación<br/>(Even if browser tab is in background)"]
```

---

## 6. Multi-Restaurant Order Flow

```mermaid
flowchart TD
    A["Mall Session<br/>id: 100<br/>hash: 'abc123'<br/>customer_name: 'Juan'<br/>mall_id: 1"] -- "Creates multiple tabs" --> T1
    A --> T2
    A --> T3
    T1["Tab #1<br/>tenant: Pizza Place<br/>status: PREPARED"] --> O1["Order #1<br/>- Pizza<br/>- Coke"]
    T2["Tab #2<br/>tenant: Sushi Bar<br/>status: IN_PREP"] --> O2["Order #2<br/>- Rolls<br/>- Sake"]
    T3["Tab #3<br/>tenant: Burger Joint<br/>status: CONFIRMED"] --> O3["Order #3<br/>- Burger<br/>- Fries"]

    subgraph CV["CUSTOMER VIEW: Mis Órdenes"]
        CV1["🍕 Pizza Place - PREPARADO (80%)<br/>Pizza Margherita, Coca-Cola"]
        CV2["🍣 Sushi Bar - EN PREPARACIÓN (60%)<br/>California Rolls, Sake"]
        CV3["🍔 Burger Joint - CONFIRMADO (40%)<br/>Cheeseburger, French Fries"]
    end

    O1 -.-> CV1
    O2 -.-> CV2
    O3 -.-> CV3

    subgraph SU["STATUS UPDATES (Independent)"]
        S1["Restaurant A changes to DELIVERED"] --> S2["Notification: 'Pizza Place ha entregado tu orden'"]
        S2 --> S3["Tab #1 status: DELIVERED<br/>Tab #2 status: IN_PREPARATION (unchanged)<br/>Tab #3 status: CONFIRMED (unchanged)"]
    end
```

---

## 7. Database Notification Storage Flow

```mermaid
flowchart TD
    A["MallSessionOrderStatusNotification<br/>(implements ShouldQueue)<br/>via(): ['broadcast', 'database', 'fcm']"] -- "Database channel" --> B["toDatabase($notifiable) method<br/>return [<br/>'type' =&gt; 'mall_order_status_update',<br/>'title' =&gt; 'Actualización de orden',<br/>'message' =&gt; 'Tu orden está en preparación',<br/>'data' =&gt; [<br/>'status' =&gt; 'IN_PREPARATION',<br/>'tenant_id' =&gt; 123,<br/>'tenant_name' =&gt; 'Pizza Place',<br/>'products' =&gt; [...],<br/>],<br/>];"]
    B --> C["MallSessionNotificationStorageService<br/>storeNotification(MallSession $session, $data)<br/><br/>Creates: MallSessionNotification record<br/>- mall_session_id: 100<br/>- type: 'mall_order_status_update'<br/>- title: 'Actualización de orden'<br/>- message: 'Tu orden está en preparación'<br/>- data: {json}<br/>- is_read: false<br/>- created_at: now()"]
    C --> D["mall_session_notifications table<br/>id | session_id | type<br/>1 | 100 | mall_session_tab_creation<br/>2 | 100 | mall_order_status_update<br/>3 | 100 | mall_order_status_update<br/>4 | 100 | mall_order_status_update"]
    D -- "CUSTOMER RETRIEVES NOTIFICATIONS" --> E["API: GET /public/mall/session/{hash}/notifications<br/>PublicMallController::getNotifications()<br/><br/>Returns: [<br/>{<br/>id: 4,<br/>type: 'mall_order_status_update',<br/>title: 'Actualización de orden',<br/>message: 'Tu orden está lista para recoger',<br/>tenant_name: 'Pizza Place',<br/>status: 'PREPARED',<br/>created_at: '2024-01-15T12:30:00Z',<br/>is_read: false<br/>},<br/>...<br/>]"]
```

---

## 8. Error Handling Flow

```mermaid
flowchart TD
    subgraph WS["WEBSOCKET DISCONNECTION"]
        A["Connected"] --> B["Disconnect Detected"]
        B --> C["Reconnect Attempt"]
        C --> D["Success - Resume"]
        C --> E["Retry (backoff)"]
        C --> F["Fail - Alert"]
    end

    subgraph API["API ERROR HANDLING"]
        G["API Call"] --> H["Error Response"]
        H --> I["Handle Error"]
        I --> J["401 - Redirect Login"]
        I --> K["404 - Show NotFound"]
        I --> L["422 - Show Errors"]
        I --> M["500 - Show Retry"]
    end

    subgraph FCM["FCM ERROR HANDLING"]
        N["FCM Token Expired"] --> O["Invalid Token"]
        O --> P["Refresh Token"]
        P --> Q["Update in Session"]
    end
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
