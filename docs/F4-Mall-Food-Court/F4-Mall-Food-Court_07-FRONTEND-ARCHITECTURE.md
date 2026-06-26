---
title: Mall App - Frontend Architecture
layout: default
nav_order: 7
parent: Mall Application
---

# Mall App - Frontend Architecture

## Overview

The Mall App frontend is built with React and React-Admin, located in the `dash-frontend` monorepo using pnpm workspaces.

## Project Structure

```
dash-frontend/
├── apps/
│   └── kitchntabs-mall/              # Main Mall Application
│       └── src/
│           ├── main.tsx              # Entry point
│           ├── KitchnTabsMallBootstrap.tsx
│           ├── core/
│           │   ├── KitchnTabsPrivateApp.tsx
│           │   └── KitchnTabsPublicApp.tsx
│           ├── components/
│           │   └── mall/
│           │       ├── MallClientWrapper.tsx    # Public client
│           │       ├── MallAppWrapper.tsx       # Admin client
│           │       ├── MallPublicWrapper.tsx    # Landing pages
│           │       └── MallAppMediator.tsx      # Customer data modal
│           └── dash-extensions/
│               ├── config/
│               │   ├── DASHMallClientDataProvider.tsx
│               │   ├── DASHMallDataProvider.tsx
│               │   ├── DASHMallClientAuthProvider.tsx
│               │   └── DASHMallAuthProvider.tsx
│               └── components/
└── packages/
    └── kt-mall/                      # Mall Components Package
        └── src/
            ├── components/
            │   ├── MallClientTabsList.tsx
            │   ├── MallOrderProductsField.tsx
            │   ├── MallTabsContext.tsx
            │   ├── MallSessionOrderProgress.tsx
            │   └── MallSessionOrderNotifications.tsx
            ├── schemas/
            │   └── MallTabSchema.tsx
            ├── contexts/
            │   └── MallSessionEchoContext.tsx
            └── resources/
                ├── MallAppResources.tsx
                └── MallClientAppResources.tsx
```

## Entry Points

### main.tsx

```typescript
// apps/kitchntabs-mall/src/main.tsx
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from 'dash-admin';
import KitchnTabsMallBootstrap from './KitchnTabsMallBootstrap';

// Initialize theme
const theme = localStorage.getItem('dash-theme') || 'dark';
document.documentElement.classList.add(`theme-${theme}`);

// Render app
const root = createRoot(document.getElementById('root')!);
root.render(
    <Provider store={store}>
        <KitchnTabsMallBootstrap />
    </Provider>
);
```

### KitchnTabsMallBootstrap.tsx

Main authentication controller that routes to appropriate app.

```typescript
// apps/kitchntabs-mall/src/KitchnTabsMallBootstrap.tsx
import { useSelector, useDispatch } from 'react-redux';
import { DashAuthState, setAuth } from 'dash-admin';
import KitchnTabsPrivateApp from './core/KitchnTabsPrivateApp';
import KitchnTabsPublicApp from './core/KitchnTabsPublicApp';

const KitchnTabsMallBootstrap: React.FC = () => {
    const dispatch = useDispatch();
    const auth = useSelector((state: { auth: DashAuthState }) => state.auth);
    
    // Initialize from persisted auth
    useEffect(() => {
        const persistedAuth = AuthPersistenceService.get();
        if (persistedAuth?.token) {
            dispatch(setAuth({ isAuthenticated: true, ...persistedAuth }));
        }
    }, []);

    // Route to appropriate app
    if (auth.isAuthenticated) {
        return (
            <KitchnTabsPrivateApp
                customResources={MallAdminResources}
                customDataProvider={DASHMallDataProvider}
                customAuthProvider={DASHMallAuthProvider}
            />
        );
    }

    // Public app handles mall client sessions
    return <KitchnTabsPublicApp />;
};

export default KitchnTabsMallBootstrap;
```

## App Wrappers

### MallClientWrapper (Public Customer App)

**Purpose:** Session-based wrapper for customers accessing via QR code.

```typescript
// apps/kitchntabs-mall/src/components/mall/MallClientWrapper.tsx
import { useParams } from 'react-router-dom';
import { useAxios } from 'dash-axios-hook';
import { dashStorage } from 'dash-utils';
import { MallSessionEchoProvider } from 'kt-mall';
import DASHMallClientDataProvider from '../../dash-extensions/config/DASHMallClientDataProvider';
import DASHMallClientAuthProvider from '../../dash-extensions/config/DASHMallClientAuthProvider';
import MallClientAppResources from 'kt-mall/src/resources/MallClientAppResources';

interface MallClientWrapperProps {
    appPath?: string;
}

const MallClientWrapper: React.FC<MallClientWrapperProps> = ({ appPath }) => {
    const { sessionId } = useParams<{ sessionId: string }>();
    const axios = useAxios();
    
    const [tenantData, setTenantData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const validateSession = async () => {
            try {
                // Clear previous session data if different session
                const previousHash = dashStorage.getItem('mall-session-hash');
                if (previousHash && previousHash !== sessionId) {
                    dashStorage.clear();
                }

                // Store current session hash
                dashStorage.setItem('mall-session-hash', sessionId);

                // Validate session with backend
                const response = await axios.get(`/public/mall/${sessionId}/getSessionAuth`);
                setTenantData(response.data);
                
                // Store auth data for data provider
                AuthPersistenceService.setSystemValues(response.data.systemValues);
                
            } catch (err: any) {
                if (err.response?.status === 410) {
                    setError('Session expired');
                } else if (err.response?.status === 404) {
                    setError('Session not found');
                } else {
                    setError('Failed to validate session');
                }
            } finally {
                setLoading(false);
            }
        };

        if (sessionId) {
            validateSession();
        }
    }, [sessionId]);

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return (
            <Box textAlign="center" p={4}>
                <Typography color="error">{error}</Typography>
            </Box>
        );
    }

    // Render app wrapped with WebSocket provider
    return (
        <MallSessionEchoProvider sessionId={sessionId}>
            <KitchnTabsPrivateApp
                customResources={MallClientAppResources}
                appPath={`/mall/session/${sessionId}`}
                useOwnRouter={false}
                customDataProvider={DASHMallClientDataProvider}
                customAuthProvider={DASHMallClientAuthProvider}
                GlobalHook={() => <GlobalTenantWrapper tenantData={tenantData} />}
            >
                <MallAppMediator />
            </KitchnTabsPrivateApp>
        </MallSessionEchoProvider>
    );
};

export default MallClientWrapper;
```

### MallAppMediator

**Purpose:** Handles customer data collection before order submission.

```typescript
// apps/kitchntabs-mall/src/components/mall/MallAppMediator.tsx
import { Dialog, DialogTitle, DialogContent, TextField, Button } from '@mui/material';
import { dashStorage } from 'dash-utils';

const MallAppMediator: React.FC = () => {
    const [open, setOpen] = useState(false);
    const [customerName, setCustomerName] = useState('');
    const [tableNumber, setTableNumber] = useState('');

    useEffect(() => {
        // Listen for event from form validation
        const handleOpenDialog = () => setOpen(true);
        window.addEventListener('enter-public-order-data', handleOpenDialog);
        return () => window.removeEventListener('enter-public-order-data', handleOpenDialog);
    }, []);

    const handleSubmit = () => {
        // Store customer data for order creation
        dashStorage.setItem('orderData', JSON.stringify({
            name: customerName,
            tableNumber: tableNumber,
        }));
        setOpen(false);
        
        // Re-trigger form submission
        window.dispatchEvent(new CustomEvent('retry-order-submission'));
    };

    return (
        <Dialog open={open} onClose={() => setOpen(false)}>
            <DialogTitle>Complete Your Order</DialogTitle>
            <DialogContent>
                <TextField
                    label="Your Name"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    fullWidth
                    margin="normal"
                    required
                />
                <TextField
                    label="Table Number"
                    value={tableNumber}
                    onChange={(e) => setTableNumber(e.target.value)}
                    fullWidth
                    margin="normal"
                    required
                />
                <Button 
                    onClick={handleSubmit} 
                    variant="contained" 
                    disabled={!customerName || !tableNumber}
                >
                    Continue
                </Button>
            </DialogContent>
        </Dialog>
    );
};

export default MallAppMediator;
```

---

## Data Providers

### DASHMallClientDataProvider

**Purpose:** Data provider for public mall client that injects session filters.

```typescript
// apps/kitchntabs-mall/src/dash-extensions/config/DASHMallClientDataProvider.tsx
import { AuthPersistenceService } from 'dash-auth';
import { dashStorage } from 'dash-utils';
import genericDataProvider from './DASHDataProvider';

// Resource path mapping
const RESOURCE_PATH_MAP: Record<string, string> = {
    'tab': 'public/mall/tab',
    'stores': 'public/mall/stores',
    'products': 'public/mall/products',
};

const mapResourceToApiPath = (resource: string): string => {
    return RESOURCE_PATH_MAP[resource] || resource;
};

const getMallId = () => {
    try {
        return AuthPersistenceService.getSystemValues()?.mall?.id || null;
    } catch {
        return null;
    }
};

const getSessionId = () => {
    try {
        // Primary: from localStorage (set by MallClientWrapper)
        const sessionHash = dashStorage.getItem('mall-session-hash');
        if (sessionHash) {
            console.log('[MallClientDataProvider] getSessionId:', sessionHash);
            return sessionHash;
        }
        
        // Fallback: parse from current path
        const appPath = dashStorage.getItem('currentAppPath');
        if (appPath) {
            const segments = appPath.split('/');
            return segments[segments.length - 1];
        }
        
        return null;
    } catch {
        return null;
    }
};

const addMallIdToParams = (params: any) => {
    const mall_id = getMallId();
    const mall_session = getSessionId();
    
    const additionalFilters: Record<string, any> = {};
    
    if (mall_id) {
        additionalFilters.mall_id = mall_id;
    }
    
    if (mall_session) {
        additionalFilters.mall_session = mall_session;
    }
    
    if (!mall_id && !mall_session) {
        console.warn('No mall_id or mall_session available');
        return params;
    }

    return {
        ...params,
        filter: {
            ...params.filter,
            ...additionalFilters,
        },
    };
};

const dataProvider = {
    ...genericDataProvider,

    getList: async (resource: string, params: any, options?: any) => {
        console.log('🔥 [MallClientDataProvider] getList CALLED', { resource, params });
        const apiResource = mapResourceToApiPath(resource);
        const enhancedParams = addMallIdToParams(params);
        console.log('[MallClientDataProvider] getList:', {
            resource,
            apiResource,
            originalFilter: params.filter,
            enhancedFilter: enhancedParams.filter,
        });
        return genericDataProvider.getList(apiResource, enhancedParams, options);
    },

    getOne: async (resource: string, params: any) => {
        const apiResource = mapResourceToApiPath(resource);
        const mall_id = getMallId();
        const session_id = getSessionId();

        if (!mall_id && !session_id) {
            return genericDataProvider.getOne(apiResource, params);
        }

        const url = `${apiResource}/${params.id}?mall_session=${session_id}`;
        const response = await axios.get(url);
        return { data: response.data };
    },

    create: async (resource: string, params: any) => {
        const apiResource = mapResourceToApiPath(resource);
        const mall_id = getMallId();
        const mall_session = getSessionId();

        if (!mall_id || !mall_session) {
            throw new Error('Mall context required for create');
        }

        // Inject mall context into data
        const enhancedData = {
            ...params.data,
            mall_id,
            mall_session,
        };

        return genericDataProvider.create(apiResource, { ...params, data: enhancedData });
    },

    // Disable dangerous operations for public client
    delete: async () => {
        throw new Error('Delete not allowed for mall client');
    },

    deleteMany: async () => {
        throw new Error('Delete not allowed for mall client');
    },
};

export default dataProvider;
```

---

## Auth Providers

### DASHMallClientAuthProvider

**Purpose:** Auth provider for public mall client (no authentication required).

```typescript
// apps/kitchntabs-mall/src/dash-extensions/config/DASHMallClientAuthProvider.tsx
import baseAuthProvider from './DASHAuthProvider';

const mallClientAuthProvider = {
    ...baseAuthProvider,

    // No authentication required - always resolve
    checkAuth: () => Promise.resolve(),

    // Return empty identity (no user)
    getIdentity: () => Promise.resolve({
        id: 'guest',
        fullName: 'Guest',
    }),

    // No login required
    login: () => Promise.resolve(),

    // No logout action
    logout: () => Promise.resolve(),
};

export default mallClientAuthProvider;
```

---

## WebSocket Context

### MallSessionEchoContext

**Purpose:** Provides WebSocket connectivity for real-time notifications.

```typescript
// packages/kt-mall/src/contexts/MallSessionEchoContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { useLaravelEcho } from 'dash-admin';

export interface IProductStatus {
    product_id: number;
    status: string;
    updated_at: string;
}

export interface IMallSessionEchoContext {
    events: any[];
    lastEvent: any | null;
    productStatuses: Record<number, IProductStatus>;
    tenantStatuses: Record<number, string>;
    isConnected: boolean;
    sessionId: string | null;
    clear: () => void;
}

const MallSessionEchoContext = createContext<IMallSessionEchoContext>({
    events: [],
    lastEvent: null,
    productStatuses: {},
    tenantStatuses: {},
    isConnected: false,
    sessionId: null,
    clear: () => {},
});

interface MallSessionEchoProviderProps {
    sessionId: string;
    children: React.ReactNode;
}

export const MallSessionEchoProvider: React.FC<MallSessionEchoProviderProps> = ({
    sessionId,
    children,
}) => {
    const [events, setEvents] = useState<any[]>([]);
    const [lastEvent, setLastEvent] = useState<any | null>(null);
    const [productStatuses, setProductStatuses] = useState<Record<number, IProductStatus>>({});
    const [tenantStatuses, setTenantStatuses] = useState<Record<number, string>>({});

    // Subscribe to session channel
    const { isConnected, lastMessage } = useLaravelEcho({
        type: 'public',
        channel: `session.${sessionId}`,
        enabled: !!sessionId,
        debug: true,
    });

    // Process incoming messages
    useEffect(() => {
        if (!lastMessage) return;

        const event = lastMessage;
        setEvents((prev) => [...prev, event]);
        setLastEvent(event);

        // Handle order status updates
        if (event.data?.type === 'mall_order_status_update') {
            const { tenant_id, status, products } = event.data;

            // Update tenant status
            setTenantStatuses((prev) => ({
                ...prev,
                [tenant_id]: status,
            }));

            // Update product statuses
            if (products) {
                const newProductStatuses = { ...productStatuses };
                products.forEach((product: any) => {
                    newProductStatuses[product.product_id] = {
                        product_id: product.product_id,
                        status: product.status || status,
                        updated_at: event.data.timestamp,
                    };
                });
                setProductStatuses(newProductStatuses);
            }
        }
    }, [lastMessage]);

    const clear = () => {
        setEvents([]);
        setLastEvent(null);
        setProductStatuses({});
        setTenantStatuses({});
    };

{% raw %}
    return (
        <MallSessionEchoContext.Provider
            value={{
                events,
                lastEvent,
                productStatuses,
                tenantStatuses,
                isConnected,
                sessionId,
                clear,
            }}
        >
            {children}
        </MallSessionEchoContext.Provider>
    );
{% endraw %}

    export const useMallSessionEcho = () => useContext(MallSessionEchoContext);

export default MallSessionEchoContext;
```

---

## Resource Configuration

### MallClientAppResources

**Purpose:** Resource definitions for mall client (customer ordering).

```typescript
// packages/kt-mall/src/resources/MallClientAppResources.tsx
import { IDashAutoAdminResourceConfig } from 'dash-auto-admin';
import ResourceTemplate from 'dash-admin/src/templates/ResourceTemplate';
import { RestaurantMenu } from '@mui/icons-material';
import { dashStorage } from 'dash-utils';
import { MallTabSchema } from '../schemas';
import { MallTabsContext, MallClientTabsList } from '../components';

const MallClientAppResources: IDashAutoAdminResourceConfig[] = [
    {
        group: "Haz tu orden aquí!",
        roles: ["Public"],
        component: ResourceTemplate,
        model: "tab",
        redirect: "create",
        label: "Haz tu orden aquí!",
        schema: MallTabSchema,
        icon: <RestaurantMenu />,

        // Custom components
        contextComponent: MallTabsContext,
        dataGridComponent: MallClientTabsList,

        // Menu
        menu: [
            { title: "☰ Tus ordenes", redirect: "tab" },
            { title: "★ Nueva Orden", redirect: "tab/create" },
        ],

        mainAction: {
            title: "⊕ Hacer un pedido",
            fn: "redirect",
            mode: "create",
            redirect: "create",
        },

        // Drawer config
        drawer: true,
        drawerOptions: { edit: true, create: false },

        // Form config
        mutationMode: "pessimistic",
        saveButtonAlwaysEnabled: true,
        processErrors: true,
        listProps: { storeKey: false, empty: false },

        // Validation - inject customer data
        beforeSubmit(values) {
            const orderData = dashStorage.getItem('orderData');
            const { name, tableNumber } = orderData 
                ? JSON.parse(orderData) 
                : { name: null, tableNumber: null };

            if (!name || !tableNumber) {
                throw new Error("MISSING_SESSION_DATA");
            }

            values.customer_name = name;
            values.table_number = tableNumber;
            return values;
        },

        // Error handling - open customer data modal
        onError(mode, error) {
            if (mode === "create" && error.message === "MISSING_SESSION_DATA") {
                window.dispatchEvent(new CustomEvent('enter-public-order-data'));
                return;
            }
            throw error;
        },
    },
];

export default MallClientAppResources;
```
