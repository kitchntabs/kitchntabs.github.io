---
title: Mall App - Frontend Components
layout: default
nav_order: 8
parent: Mall Application
---

# Mall App - Frontend Components

## Overview

Mall-specific UI components are located in `packages/kt-mall/src/components/`.

## Components

### 1. MallClientTabsList

**File Path:** `packages/kt-mall/src/components/MallClientTabsList.tsx`

**Purpose:** Custom data grid for displaying customer orders with real-time updates.

```typescript
import { IDashAutoAdminDataGrid } from 'dash-auto-admin';
import { Box, Card, CardContent, CardHeader, Chip, Typography, Alert } from '@mui/material';
import { useContext, useEffect, useState } from 'react';
import { useRefresh, WithListContext } from 'react-admin';
import { toast } from 'react-toastify';
import LaravelEchoContext from 'dash-admin/src/contexts/com/LaravelEchoContext';
import { TabTimerClock } from 'kt-tabs';

interface IOrderStatusUpdateNotification {
    event: string;
    status: string;
    tenant_id?: number;
    tenant_name?: string;
    mall_session_hash?: string;
    master_tab_id?: number;
    tenant_tab_id?: number;
    products?: any[];
    timestamp?: string;
    type: string;
}

const MallClientTabsList: React.FC<IDashAutoAdminDataGrid> = ({ resourceConfig }) => {
    const { lastEvent } = useContext(LaravelEchoContext);
    const refresh = useRefresh();

    const statusLabel: Record<string, string> = {
        'CREATED': 'Creado',
        'CONFIRMED': 'Confirmado',
        'IN_PREPARATION': 'En preparación',
        'PREPARED': 'Preparado',
        'DELIVERED': 'Entregado',
        'CLOSED': 'Cerrado',
        'CANCELLED': 'Cancelado',
    };

    const showMessage = (info: string) => {
        toast.info(info, {
            position: 'top-center',
            autoClose: 3000,
        });
    };

    // Listen for WebSocket events
    useEffect(() => {
        // Classic tab status updates
        if (lastEvent?.model === "Domain\\App\\Models\\Tab\\Tab" &&
            lastEvent.data?.type === "tab.status") {
            showMessage(`Estado cambiado de ${lastEvent.data.old} a ${lastEvent.data.new}`);
            refresh();
        }

        // Tab updates
        if (lastEvent?.model === "Domain\\App\\Models\\Tab\\Tab" &&
            lastEvent.data?.type === "tab.update") {
            refresh();
        }

        // Mall order status updates - from Tab model
        if (lastEvent?.model === "Domain\\App\\Models\\Tab\\Tab" &&
            lastEvent.data?.type === "mall_order_status_update") {
            const data = lastEvent.data as IOrderStatusUpdateNotification;
            showMessage(
                `${data.tenant_name || 'El restaurante'} ha actualizado tu orden a: ` +
                `${statusLabel[data.status] || data.status}`
            );
            refresh();
        }

        // Mall order status updates - from Order model
        if (lastEvent?.model === "Domain\\App\\Models\\Order\\Order" &&
            lastEvent.data?.type === "mall_order_status_update") {
            const data = lastEvent.data as IOrderStatusUpdateNotification;
            showMessage(
                `${data.tenant_name || 'El restaurante'} ha actualizado tu orden a: ` +
                `${statusLabel[data.status] || data.status}`
            );
            refresh();
        }
    }, [lastEvent]);

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'CREATED': return 'default';
            case 'CONFIRMED': return 'primary';
            case 'IN_PREPARATION': return 'warning';
            case 'PREPARED': return 'info';
            case 'DELIVERED': return 'success';
            case 'CLOSED': return 'secondary';
            case 'CANCELLED': return 'error';
            default: return 'default';
        }
    };

    return (
        <WithListContext render={({ isPending, data }) => (
            <>
                {data?.length === 0 && (
                    <Alert severity="info" sx={{ mb: 2 }}>
                        No tienes órdenes activas. Puedes crear una nueva orden usando el menú.
                    </Alert>
                )}
                
                <Box sx={{
                    display: 'grid',
                    gap: 1,
                    gridTemplateColumns: {
                        xs: 'repeat(1, 1fr)',
                        md: 'repeat(2, 1fr)',
                        lg: 'repeat(3, 1fr)',
                    },
                }}>
                    {data?.map((record: any) => (
                        <Card key={record.id} sx={{ p: 1, mb: 2 }}>
                            <CardHeader
                                title={
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                        <Typography variant="h5">
                                            Orden #{record.id}
                                        </Typography>
                                        <TabTimerClock createdAt={record.date_confirmed} />
                                    </Box>
                                }
                            />
                            <CardContent>
                                <Chip
                                    label={statusLabel[record.status] || record.status}
                                    size="small"
                                    color={getStatusColor(record.status)}
                                />
                                
                                <OrderProductsView 
                                    record={record} 
                                    resourceConfig={resourceConfig} 
                                />
                            </CardContent>
                        </Card>
                    ))}
                </Box>
            </>
        )} />
    );
};

export default MallClientTabsList;
```

---

### 2. MallOrderProductsField

**File Path:** `packages/kt-mall/src/components/MallOrderProductsField.tsx`

**Purpose:** Custom field component for product selection and display in orders.

```typescript
import { IDashAutoAdminCustomFieldComponent } from 'dash-auto-admin';
import { useRecordContext } from 'react-admin';
import { 
    MallSessionOrderProgress, 
    MallSessionOrderNotifications,
    MallOrderProducts 
} from 'kt-tabs';
import { OrderProductsMallFilters, OrderProductsList } from 'kt-tabs';

const MallOrderProductsField: React.FC<IDashAutoAdminCustomFieldComponent> = ({
    resourceConfig,
    attribute,
    method,
}) => {
    const record = useRecordContext();

    // CREATE MODE: Product selection with filters
    if (method === 'create') {
        return (
            <Box>
                <OrderProductsMallFilters />
                <MallOrderProducts 
                    infiniteScroll={true}
                    showPrice={true}
                />
            </Box>
        );
    }

    // EDIT MODE: Product list with progress tracking
    if (method === 'edit') {
        return (
            <Box>
                <MallSessionOrderProgress record={record} />
                <OrderProductsList record={record} />
            </Box>
        );
    }

    // VIEW MODE: Show order products
    if (method === 'view' || method === 'show') {
        return (
            <Box>
                <MallSessionOrderNotifications orderId={record?.id} />
                <OrderProductsList record={record} />
            </Box>
        );
    }

    // LIST MODE: Simple count
    if (method === 'list') {
        const itemCount = record?.order?.items?.length || 0;
        return <span>{itemCount} productos</span>;
    }

    return null;
};

export default MallOrderProductsField;
```

---

### 3. MallTabsContext

**File Path:** `packages/kt-mall/src/components/MallTabsContext.tsx`

**Purpose:** Context wrapper for tab management.

```typescript
import React from 'react';
import { TabContextWrapper } from 'kt-tabs';
import { IDashAutoAdminResourceConfig } from 'dash-auto-admin';

interface MallTabsContextProps {
    resourceConfig: IDashAutoAdminResourceConfig;
    children: React.ReactNode;
    mode?: 'create' | 'edit' | 'show';
}

const MallTabsContext: React.FC<MallTabsContextProps> = ({
    resourceConfig,
    children,
    mode,
}) => {
    return (
        <TabContextWrapper
            resourceConfig={resourceConfig}
            enableInfiniteScroll={true}
            showPrice={true}
            mallMode={true}
        >
            {children}
        </TabContextWrapper>
    );
};

export default MallTabsContext;
```

---

### 4. MallSessionOrderProgress

**File Path:** `packages/kt-mall/src/components/MallSessionOrderProgress.tsx`

**Purpose:** Displays order progress per tenant.

```typescript
import React, { useContext, useEffect, useState } from 'react';
import { Box, LinearProgress, Typography, Chip, Paper } from '@mui/material';
import MallSessionEchoContext from '../contexts/MallSessionEchoContext';

interface TenantProgress {
    tenant_id: number;
    tenant_name: string;
    status: string;
    products: any[];
}

interface MallSessionOrderProgressProps {
    record?: any;
}

const MallSessionOrderProgress: React.FC<MallSessionOrderProgressProps> = ({ record }) => {
    const { tenantStatuses, events } = useContext(MallSessionEchoContext);
    const [tenantProgress, setTenantProgress] = useState<TenantProgress[]>([]);

    const statusOrder = ['CREATED', 'CONFIRMED', 'IN_PREPARATION', 'PREPARED', 'DELIVERED'];
    
    const getProgressPercent = (status: string) => {
        const index = statusOrder.indexOf(status);
        return index >= 0 ? ((index + 1) / statusOrder.length) * 100 : 0;
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'CREATED': return 'default';
            case 'CONFIRMED': return 'primary';
            case 'IN_PREPARATION': return 'warning';
            case 'PREPARED': return 'info';
            case 'DELIVERED': return 'success';
            case 'CANCELLED': return 'error';
            default: return 'default';
        }
    };

    // Build tenant progress from events
    useEffect(() => {
        const progressMap: Record<number, TenantProgress> = {};

        events.forEach((event) => {
            if (event.data?.type === 'mall_order_status_update') {
                const { tenant_id, tenant_name, status, products } = event.data;
                progressMap[tenant_id] = {
                    tenant_id,
                    tenant_name,
                    status,
                    products: products || [],
                };
            }
        });

        // Also update from real-time tenantStatuses
        Object.entries(tenantStatuses).forEach(([tenantId, status]) => {
            const id = parseInt(tenantId);
            if (progressMap[id]) {
                progressMap[id].status = status;
            }
        });

        setTenantProgress(Object.values(progressMap));
    }, [events, tenantStatuses]);

    if (tenantProgress.length === 0) {
        return null;
    }

    return (
        <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
                Estado por restaurante
            </Typography>
            
            {tenantProgress.map((tenant) => (
                <Box key={tenant.tenant_id} sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">
                            {tenant.tenant_name}
                        </Typography>
                        <Chip
                            label={tenant.status}
                            size="small"
                            color={getStatusColor(tenant.status)}
                        />
                    </Box>
                    <LinearProgress
                        variant="determinate"
                        value={getProgressPercent(tenant.status)}
                        color={getStatusColor(tenant.status) as any}
                    />
                </Box>
            ))}
        </Paper>
    );
};

export default MallSessionOrderProgress;
```

---

### 5. MallSessionOrderNotifications

**File Path:** `packages/kt-mall/src/components/MallSessionOrderNotifications.tsx`

**Purpose:** Displays notification history for an order.

```typescript
import React, { useContext, useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, Chip } from '@mui/material';
import { useAxios } from 'dash-axios-hook';
import { dashStorage } from 'dash-utils';
import MallSessionEchoContext from '../contexts/MallSessionEchoContext';

interface Notification {
    id: number;
    type: string;
    title: string;
    message: string;
    tenant_name?: string;
    status?: string;
    created_at: string;
    is_read: boolean;
}

interface MallSessionOrderNotificationsProps {
    orderId?: number;
}

const MallSessionOrderNotifications: React.FC<MallSessionOrderNotificationsProps> = ({
    orderId,
}) => {
    const axios = useAxios();
    const { lastEvent } = useContext(MallSessionEchoContext);
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [loading, setLoading] = useState(true);

    const sessionHash = dashStorage.getItem('mall-session-hash');

    // Fetch notifications from API
    const fetchNotifications = async () => {
        if (!sessionHash) return;

        try {
            const response = await axios.get(
                `/public/mall/session/${sessionHash}/notifications`
            );
            setNotifications(response.data.notifications || []);
        } catch (error) {
            console.error('Failed to fetch notifications:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNotifications();
    }, [sessionHash]);

    // Refresh on new WebSocket event
    useEffect(() => {
        if (lastEvent?.data?.type === 'mall_order_status_update') {
            fetchNotifications();
        }
    }, [lastEvent]);

    const getStatusColor = (status?: string) => {
        switch (status) {
            case 'CREATED': return '#9e9e9e';
            case 'CONFIRMED': return '#2196f3';
            case 'IN_PREPARATION': return '#ff9800';
            case 'PREPARED': return '#03a9f4';
            case 'DELIVERED': return '#4caf50';
            case 'CANCELLED': return '#f44336';
            default: return '#9e9e9e';
        }
    };

    if (loading) {
        return <Typography>Cargando notificaciones...</Typography>;
    }

    if (notifications.length === 0) {
        return null;
    }

    return (
        <Box sx={{ mb: 2 }}>
            <Typography variant="h6" gutterBottom>
                Historial de actualizaciones
            </Typography>
            
            {notifications.map((notification) => (
                <Card
                    key={notification.id}
                    sx={{
                        mb: 1,
                        borderLeft: `4px solid ${getStatusColor(notification.status)}`,
                        opacity: notification.is_read ? 0.7 : 1,
                    }}
                >
                    <CardContent sx={{ py: 1, '&:last-child': { pb: 1 } }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="subtitle2">
                                {notification.title}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                                {new Date(notification.created_at).toLocaleTimeString()}
                            </Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary">
                            {notification.message}
                        </Typography>
                        {notification.tenant_name && (
                            <Chip
                                label={notification.tenant_name}
                                size="small"
                                sx={{ mt: 1 }}
                            />
                        )}
                    </CardContent>
                </Card>
            ))}
        </Box>
    );
};

export default MallSessionOrderNotifications;
```

---

### 6. MallQRGenerator

**File Path:** `packages/kt-mall/src/components/MallQRGenerator.tsx`

**Purpose:** QR code generator for mall administrators.

```typescript
import React, { useState } from 'react';
import { 
    Box, 
    Button, 
    Card, 
    CardContent, 
    Typography, 
    TextField,
    Grid 
} from '@mui/material';
import QRCode from 'react-qr-code';
import { useAxios } from 'dash-axios-hook';

const MallQRGenerator: React.FC = () => {
    const axios = useAxios();
    const [sessions, setSessions] = useState<any[]>([]);
    const [count, setCount] = useState(1);
    const [loading, setLoading] = useState(false);

    const generateSessions = async () => {
        setLoading(true);
        const newSessions: any[] = [];

        for (let i = 0; i < count; i++) {
            try {
                const response = await axios.post('/mall/session/generate-hash', {
                    mall_id: getMallId(),
                });
                newSessions.push(response.data);
            } catch (error) {
                console.error('Failed to generate session:', error);
            }
        }

        setSessions([...sessions, ...newSessions]);
        setLoading(false);
    };

    const getQRUrl = (hash: string) => {
        return `${window.location.origin}/mall/session/${hash}`;
    };

    return (
        <Box p={3}>
            <Typography variant="h4" gutterBottom>
                Generador de QR para Mesas
            </Typography>

            <Box sx={{ mb: 3, display: 'flex', gap: 2, alignItems: 'center' }}>
                <TextField
                    type="number"
                    label="Cantidad"
                    value={count}
                    onChange={(e) => setCount(parseInt(e.target.value) || 1)}
                    inputProps={{ min: 1, max: 50 }}
                    size="small"
                />
                <Button
                    variant="contained"
                    onClick={generateSessions}
                    disabled={loading}
                >
                    {loading ? 'Generando...' : 'Generar QR'}
                </Button>
            </Box>

            <Grid container spacing={2}>
                {sessions.map((session) => (
                    <Grid item xs={12} sm={6} md={4} lg={3} key={session.hash}>
                        <Card>
                            <CardContent sx={{ textAlign: 'center' }}>
                                <QRCode
                                    value={getQRUrl(session.hash)}
                                    size={150}
                                />
                                <Typography variant="h6" sx={{ mt: 1 }}>
                                    {session.hash}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                    Mesa / Ubicación
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default MallQRGenerator;
```

---

## Schemas

### MallTabSchema

**File Path:** `packages/kt-mall/src/schemas/MallTabSchema.tsx`

**Purpose:** Schema definition for mall tab/order forms.

```typescript
import { IDashAutoAdminAttribute } from 'dash-auto-admin';
import MallOrderProductsField from '../components/MallOrderProductsField';

const MallTabSchema: IDashAutoAdminAttribute[] = [
    {
        tab: 'Productos',
        attribute: 'products',
        label: 'Productos',
        type: Array,
        customFieldComponent: MallOrderProductsField,
        modes: {
            create: { component: MallOrderProductsField },
            edit: { component: MallOrderProductsField },
            view: { component: MallOrderProductsField },
            list: { component: MallOrderProductsField },
        },
    },
    {
        tab: 'Detalles',
        attribute: 'tenant',
        label: 'Restaurante',
        type: Object,
        displayOnly: true,
        modes: {
            list: { show: true, render: (record) => record?.tenant?.name },
            view: { show: true },
        },
    },
    {
        tab: 'Detalles',
        attribute: 'status',
        label: 'Estado',
        type: String,
        displayOnly: true,
        modes: {
            list: { show: true },
            view: { show: true },
            edit: { show: false },
        },
    },
    {
        tab: 'Detalles',
        attribute: 'note',
        label: 'Nota',
        type: String,
        displayOnly: true,
        modes: {
            list: { show: false },
            view: { show: true },
        },
    },
    {
        tab: 'Progreso',
        attribute: 'progress',
        label: 'Progreso',
        type: Object,
        customFieldComponent: MallSessionOrderProgress,
        modes: {
            edit: { show: true },
            view: { show: true },
        },
    },
    {
        tab: 'Notificaciones',
        attribute: 'notifications',
        label: 'Historial',
        type: Array,
        customFieldComponent: MallSessionOrderNotifications,
        modes: {
            view: { show: true },
        },
    },
    {
        tab: 'Información',
        attribute: 'created_at',
        label: 'Fecha de creación',
        type: Date,
        displayOnly: true,
        modes: {
            list: { show: true },
            view: { show: true },
        },
    },
];

export default MallTabSchema;
```

---

## Component Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPONENT HIERARCHY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   MallClientWrapper                                             │
│   ├── MallSessionEchoProvider (WebSocket)                       │
│   │   └── MallSessionEchoContext                                │
│   │                                                              │
│   └── KitchnTabsPrivateApp                                      │
│       ├── MallAppMediator (Customer Data Modal)                 │
│       ├── GlobalTenantWrapper (Theme/Settings)                  │
│       │                                                          │
│       └── ResourceTemplate (from MallClientAppResources)        │
│           ├── MallTabsContext (Context Wrapper)                 │
│           │                                                      │
│           └── DashAutoList                                       │
│               └── MallClientTabsList (DataGrid)                 │
│                   ├── Uses: LaravelEchoContext (events)         │
│                   ├── Uses: useRefresh() (React-Admin)          │
│                   └── Contains: OrderProductsView               │
│                                                                  │
│   On Create/Edit:                                               │
│   ├── MallOrderProductsField                                    │
│   │   ├── Create: OrderProductsMallFilters + MallOrderProducts  │
│   │   ├── Edit: MallSessionOrderProgress + OrderProductsList    │
│   │   └── View: MallSessionOrderNotifications + OrderProducts   │
│   │                                                              │
│   ├── MallSessionOrderProgress                                  │
│   │   └── Uses: MallSessionEchoContext (tenantStatuses)         │
│   │                                                              │
│   └── MallSessionOrderNotifications                             │
│       ├── Fetches: /api/public/mall/session/{hash}/notifications│
│       └── Uses: MallSessionEchoContext (lastEvent)              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```
