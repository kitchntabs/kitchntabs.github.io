---
layout: default
title: F4-Mall-Food-Court KITCHNTABS MALL WEBSOCKET SYSTEM
---

# KitchnTabs Mall WebSocket Messaging System

## Overview

The KitchnTabs Mall application uses WebSocket technology to provide real-time order status updates to customers. This document describes the architecture, event flow, and implementation details of the async messaging system.

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend Broadcaster | Laravel Broadcasting | Dispatch events |
| WebSocket Server | Pusher/Soketi | Message relay |
| Frontend Client | Laravel Echo + Pusher.js | Event subscription |
| Channel Type | Public Channels | No auth required for guests |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WEBSOCKET ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐                     ┌─────────────────┐                │
│  │  Laravel        │                     │  Customer       │                │
│  │  Backend        │                     │  Browser        │                │
│  └────────┬────────┘                     └────────┬────────┘                │
│           │                                       │                          │
│           │ 1. Dispatch Event                     │ 4. Receive Event         │
│           ▼                                       ▼                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     Pusher/Soketi Server                            │    │
│  │                                                                      │    │
│  │  Channel: session.{sessionId}                                       │    │
│  │  Example: session.DFJNL                                             │    │
│  │                                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  2. Backend → Pusher (HTTP POST)                                            │
│  3. Pusher → Browser (WebSocket)                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Channel Naming Convention

### Public Channels (Mall Client)

Public channels don't require authentication, making them ideal for guest users.

```
session.{sessionId}
```

**Examples:**
- `session.DFJNL` - Session with hash DFJNL
- `session.ABC12` - Session with hash ABC12

### Private Channels (Admin/Tenant)

Private channels require authentication and are used for tenant notifications.

```
tenant.{tenantId}.system
user.{userId}
```

---

## Frontend Implementation

### Echo Client Manager (Singleton)

The `EchoClientManager` ensures only one Echo client exists per channel type.

```typescript
// Located: packages/dash-admin/src/contexts/com/useLaravelEcho.tsx

class EchoClientManager {
    private static instance: EchoClientManager;
    public clients: Map<string, Echo<"pusher">>;

    private constructor() {
        this.clients = new Map();
    }

    public static getInstance(): EchoClientManager {
        if (!EchoClientManager.instance) {
            EchoClientManager.instance = new EchoClientManager();
        }
        return EchoClientManager.instance;
    }

    // Store client by type ('public' or 'private')
    public setClient(hash: string, client: Echo<"pusher">): void
    public getClient(hash: string): Echo<"pusher"> | undefined
    public removeClient(hash: string): boolean
}
```

### useLaravelEcho Hook

The main hook for subscribing to WebSocket channels.

```typescript
// Usage
const { lastEvent, isConnected } = useLaravelEcho({
    type: 'public',                           // Channel type
    channel: `session.${sessionId}`,          // Channel name
    enabled: !!sessionId,                     // Enable when sessionId exists
    debug: true,                              // Enable logging
});
```

**Hook Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `'public' \| 'private'` | Channel authentication type |
| `channel` | `string` | Full channel name |
| `events` | `object` | Event handlers (optional) |
| `userId` | `number` | User ID for private channels |
| `pingInterval` | `number` | Keep-alive interval (default: 30s) |
| `debug` | `boolean` | Enable console logging |
| `enabled` | `boolean` | Enable/disable subscription |

**Return Values:**

| Property | Type | Description |
|----------|------|-------------|
| `lastEvent` | `{ event: string, data: any }` | Most recent event |
| `isConnected` | `boolean` | Connection status |
| `echoChannel` | `Channel` | Echo channel instance |

### Echo Client Configuration

```typescript
const completeConfig = {
    broadcaster: 'pusher',
    key: getEnv('APP_SOCKETS_KEY') || 'dash',
    wsHost: socketHostEnv || window.location.hostname,
    wsPort: portEnv,
    secure: isSSL,
    forceTLS: isSSL,
    encrypted: isSSL,
    useTLS: isSSL,
    disableStats: !isSSL,
    enabledTransports: isSSL ? ['wss', 'ws'] : ['ws'],
    cluster: 'mt1',
    activityTimeout: 120000,
    pongTimeout: 30000,
};
```

---

## Context Provider Hierarchy

The WebSocket events flow through a hierarchy of React contexts:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CONTEXT PROVIDER HIERARCHY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MallClientWrapper                                                           │
│  │                                                                           │
│  └── MallSessionEchoProvider                                                │
│      │   - SINGLE WebSocket subscriber (useLaravelEcho)                     │
│      │   - Subscribes to session.{sessionId}                                │
│      │   - Processes and stores events                                      │
│      │                                                                       │
│      └── MallEchoBridgeWrapper                                              │
│          │   - Uses useMallSessionEcho() to get events                      │
│          │   - Bridges events from app to package                           │
│          │                                                                   │
│          └── MallEchoBridgeProvider (from kt-mall package)                  │
│              │   - Provides events to package components                    │
│              │   - Package can't import from app, so uses bridge            │
│              │                                                               │
│              └── KitchnTabsPrivateApp                                       │
│                  │                                                           │
│                  └── Resource Components                                    │
│                      │                                                       │
│                      └── MallTabsContext (contextComponent)                 │
│                          │                                                   │
│                          └── MallClientTabsProvider                         │
│                              │   - Uses useMallEchoBridge()                 │
│                              │   - Provides lastEvent to children           │
│                              │                                               │
│                              └── MallClientTabsList                         │
│                                  - Consumes lastEvent                       │
│                                  - Triggers refresh() on events             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## MallSessionEchoContext

The primary WebSocket subscription context for the mall client.

### Interface

```typescript
// Located: apps/kitchntabs-mall/src/contexts/MallSessionEchoContext.tsx

interface IMallSessionEchoContext {
    events: any[];                              // All received events
    lastEvent: any | null;                      // Most recent event
    productStatuses: Record<number, IProductStatus>;  // Product status map
    tenantStatuses: Record<number, string>;     // Tenant status map
    isConnected: boolean;                       // WebSocket connection status
    sessionId: string | null;                   // Current session ID
    clear: () => void;                          // Clear lastEvent
}
```

### Event Processing

```typescript
// Process incoming events
useEffect(() => {
    if (echoEvent) {
        const eventData = echoEvent.data || echoEvent;
        const notificationPayload = echoEvent.notificationPayload;
        
        // Store full event for consumers
        setLastEvent(echoEvent);
        setEvents(prev => [...prev, echoEvent]);
        
        // Check if this is a mall order update
        const isMallOrderUpdate = 
            eventData.type === 'mall_order_status_update' || 
            eventData.type === 'mall_order_confirmation' ||
            notificationPayload?.class === 'MallSessionOrderStatusNotification';
        
        if (isMallOrderUpdate) {
            const payload = notificationPayload?.notificationPayload || eventData;
            const { tenant_id, status, products } = payload;
            
            // Update tenant status
            if (tenant_id) {
                setTenantStatuses(prev => ({
                    ...prev,
                    [tenant_id]: status
                }));
            }
            
            // Update product statuses
            if (products) {
                setProductStatuses(prev => {
                    const updated = { ...prev };
                    products.forEach(product => {
                        updated[product.product_id] = {
                            product_id: product.product_id,
                            product_name: product.product_name,
                            status: product.status || status,
                            quantity: product.quantity,
                            tenant_id,
                        };
                    });
                    return updated;
                });
            }
        }
    }
}, [echoEvent]);
```

---

## MallEchoBridgeContext

The bridge context allows the `kt-mall` package to receive events without importing from the app.

### Why a Bridge?

TypeScript's `rootDir` constraints prevent the `kt-mall` package from importing directly from the `kitchntabs-mall` app. The bridge pattern solves this:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BRIDGE PATTERN                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  kitchntabs-mall (app)              kt-mall (package)                       │
│  ─────────────────────              ──────────────────                      │
│                                                                              │
│  MallSessionEchoContext             MallEchoBridgeContext                   │
│  (WebSocket subscriber)             (Event receiver)                        │
│         │                                    ▲                               │
│         │                                    │                               │
│         └────────────────────────────────────┘                               │
│              Props passed via                                                │
│              MallEchoBridgeProvider                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Bridge Interface

```typescript
// Located: packages/kt-mall/src/contexts/MallEchoBridgeContext.tsx

interface IMallEchoBridgeContext {
    lastEvent: any | null;
    events: any[];
    isConnected: boolean;
    sessionId: string | null;
    tenantStatuses: Record<number, string>;
    productStatuses: Record<number, any>;
}
```

### Usage in Package Components

```typescript
// In MallClientTabsContext.tsx (kt-mall package)
import { useMallEchoBridge } from '../contexts/MallEchoBridgeContext';

const MallClientTabsProvider = ({ children }) => {
    // Get lastEvent from bridge instead of direct subscription
    const { lastEvent } = useMallEchoBridge();
    
    // Process events...
};
```

---

## Event Types

### mall_order_status_update

Sent when a restaurant updates an order status.

```typescript
interface MallOrderStatusUpdateEvent {
    event: 'mall_order_status_update';
    type: 'mall_order_status_update';
    data: {
        master_tab_id: number;
        tenant_tab_id: number;
        tenant_id: string;
        tenant_name: string;
        status: 'CREATED' | 'CONFIRMED' | 'IN_PREPARATION' | 'PREPARED' | 'DELIVERED' | 'CLOSED' | 'CANCELLED';
        products: Array<{
            product_id: number;
            product_name: string;
            quantity: number;
            status: string;
        }>;
        timestamp: string;
        mall_session_hash: string;
    };
    notificationPayload?: {
        class: 'MallSessionOrderStatusNotification';
        notificationPayload: {
            title: string;
            message: string;
            // ... same as data above
        };
    };
}
```

### mall_tab_creation

Sent when a new order is created.

```typescript
interface MallTabCreationEvent {
    event: 'mall_tab_creation';
    type: 'mall_tab_creation';
    data: {
        master_tab_id: number;
        tenant_tabs: Array<{
            tenant_tab_id: number;
            tenant_id: string;
            tenant_name: string;
        }>;
        customer_info: {
            name: string;
            table: string;
        };
        products: Array<{
            product_id: number;
            product_name: string;
            quantity: number;
        }>;
        mall_session_hash: string;
    };
}
```

---

## Component Event Handling

### MallClientTabsList

The order list component that handles real-time updates.

```typescript
// Located: packages/kt-mall/src/components/MallClientTabsList.tsx

const MallClientTabsList = ({ resourceConfig }) => {
    const { lastEvent, tenantStatusesByTab } = useMallClientTabsContext();
    const refresh = useRefresh();

    useEffect(() => {
        if (!lastEvent) return;

        // Check for mall order updates
        const isMallOrderUpdate = 
            lastEvent.event === "mall_order_status_update" ||
            lastEvent.type === "mall_order_status_update" ||
            lastEvent.data?.type === "mall_order_status_update";

        if (isMallOrderUpdate) {
            const payload = lastEvent.notificationPayload?.notificationPayload || lastEvent.data;
            const tenantName = payload.tenant_name || 'El restaurante';
            const status = payload.status;
            
            // Show toast notification
            toast.info(`${tenantName} ha actualizado tu orden a: ${status}`);
            
            // Refresh the list to get updated data
            refresh();
        }
    }, [lastEvent, refresh]);

    // Render order cards...
};
```

### StoreProgressBars

Component that displays per-restaurant progress.

```typescript
const StoreProgressBars = ({ masterTabId, record }) => {
    const { getTenantStatusesForTab } = useMallClientTabsContext();
    
    // Get tenant statuses from context (WebSocket updates)
    const tenantTabs = getTenantStatusesForTab(masterTabId);

    // Render progress bars per tenant
    return (
        <Box>
            {tenantTabs.map((tenant) => (
                <Box key={tenant.tenant_id}>
                    <Typography>{tenant.tenant_name}</Typography>
                    <LinearProgress 
                        value={tenant.progress} 
                        color={getProgressColor(tenant.status)}
                    />
                </Box>
            ))}
        </Box>
    );
};
```

---

## Connection Management

### Connection Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CONNECTION LIFECYCLE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. INITIALIZATION                                                           │
│     - Component mounts with sessionId                                       │
│     - useLaravelEcho hook creates Echo client                               │
│     - Client subscribes to session.{sessionId}                              │
│                                                                              │
│  2. CONNECTED                                                                │
│     - Echo client receives 'connected' event from Pusher                    │
│     - isConnected set to true                                               │
│     - Ping timer started (30s interval)                                     │
│                                                                              │
│  3. RECEIVING EVENTS                                                         │
│     - bind_global captures all events on channel                            │
│     - Events stored in lastEvent state                                      │
│     - Consumers (contexts, components) react to lastEvent changes           │
│                                                                              │
│  4. DISCONNECTED                                                             │
│     - Echo client receives 'disconnected' event                             │
│     - isConnected set to false                                              │
│     - Ping timer stopped                                                    │
│     - Automatic reconnection handled by Pusher.js                           │
│                                                                              │
│  5. CLEANUP                                                                  │
│     - Component unmounts                                                    │
│     - Ping timer cleared                                                    │
│     - Echo client disconnected                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Keep-Alive Mechanism

The system uses a ping mechanism to keep the connection alive:

```typescript
const pingConnection = useCallback(() => {
    if (laravelEchoClient?.connector?.pusher) {
        laravelEchoClient.connector.pusher.send_event('client-ping', {
            timestamp: new Date().toISOString()
        });
    }
}, [laravelEchoClient]);

// Start ping timer on connection
echo.connector.pusher.connection.bind('connected', () => {
    pingTimerRef.current = window.setInterval(pingConnection, 30000);
});

// Stop ping timer on disconnect
echo.connector.pusher.connection.bind('disconnected', () => {
    if (pingTimerRef.current) {
        window.clearInterval(pingTimerRef.current);
        pingTimerRef.current = null;
    }
});
```

---

## Environment Configuration

Required environment variables for WebSocket configuration:

```env
# Enable/disable sockets
APP_SOCKETS_ENABLED=true

# WebSocket server host
APP_SOCKETS_HOST=ws.example.com

# WebSocket scheme (https = secure WebSocket)
APP_SOCKETS_SCHEME=https

# WebSocket port (optional)
APP_SOCKETS_PORT=443

# Pusher app key
APP_SOCKETS_KEY=your-pusher-key

# Auth endpoint for private channels
APP_SOCKETS_AUTH_ENDPOINT=/api/ws/auth
```

---

## Debugging

### Console Logging

Enable `debug: true` in useLaravelEcho for detailed logs:

```
📡 Initializing Echo client with config: {...}
📡 Connected to Pusher!
📡 Global event received: mall_order_status_update {...}
📬 Mall session event received: {...}
📦 Order status update from Pizza Place: IN_PREPARATION
🌉 MallEchoBridgeWrapper: Bridging event to kt-mall package: {...}
[MallClientTabsList] 🔔 Processing lastEvent: {...}
[MallClientTabsList] ✅ Mall order update detected, calling refresh()
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Events not received | Multiple subscribers | Ensure single MallSessionEchoProvider |
| Events received but list doesn't update | Bridge not connected | Check MallEchoBridgeProvider is wrapping components |
| Connection drops frequently | Network issues | Check pingInterval, verify server health |
| Events delayed | Server-side queue | Check Laravel queue worker status |

---

## Related Documentation

- [KitchnTabs Mall Application Flow](./KITCHNTABS_MALL_APPLICATION_FLOW.md)
- [Guest Authentication Flow](./KITCHNTABS_MALL_AUTH_FLOW.md)
- [Laravel Broadcasting Documentation](https://laravel.com/docs/broadcasting)
