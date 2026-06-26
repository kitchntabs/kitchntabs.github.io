---
title: Mall App - Notification System
layout: default
nav_order: 6
parent: Mall Application
---

# Mall App - Notification System

## Overview

The Mall App uses a multi-channel notification system supporting WebSocket (real-time), Push (FCM), Database (persistence), and Email delivery.

## Notification Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   NOTIFICATION FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐                                              │
│   │ Tab Status   │                                              │
│   │ Change       │                                              │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────────────────────────────┐                      │
│   │ TabsNotificationService /            │                      │
│   │ MallOrderSyncService                 │                      │
│   │ - Build notification data            │                      │
│   │ - Determine channel                  │                      │
│   └──────────────┬───────────────────────┘                      │
│                  │                                               │
│                  ▼                                               │
│   ┌──────────────────────────────────────┐                      │
│   │ AppNotificationBuilder::send()       │                      │
│   │ - Process notification config        │                      │
│   │ - Route to enabled channels          │                      │
│   └──────────────┬───────────────────────┘                      │
│                  │                                               │
│       ┌──────────┼──────────┬──────────┐                        │
│       ▼          ▼          ▼          ▼                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐               │
│  │ Socket  │ │  Push   │ │Database │ │  Email  │               │
│  │(WebSocket)│ │  (FCM)  │ │         │ │         │               │
│  └────┬────┘ └────┬────┘ └────┬────┘ └─────────┘               │
│       │           │           │                                  │
│       ▼           ▼           ▼                                  │
│  ┌─────────┐ ┌─────────┐ ┌────────────────────┐                 │
│  │ Pusher/ │ │Firebase │ │mall_session_       │                 │
│  │ Soketi  │ │Cloud Msg│ │notifications table │                 │
│  └────┬────┘ └────┬────┘ └────────────────────┘                 │
│       │           │                                              │
│       ▼           ▼                                              │
│  ┌───────────────────────────────────────────┐                  │
│  │              CLIENT DEVICES               │                  │
│  │  - Browser (WebSocket)                    │                  │
│  │  - Mobile App (Push)                      │                  │
│  └───────────────────────────────────────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Notification Classes

### Base Class: BaseMallSessionNotification

**File Path:** `domain/app/Notifications/Mall/BaseMallSessionNotification.php`

**Purpose:** Abstract base for all mall session notifications.

```php
abstract class BaseMallSessionNotification extends AppNotificationBase
{
    protected $rawMallSession;

    public function __construct(
        $modelInstance = null,
        $data = null,
        $type = null,
        $scope = null,
        $targets = [],
        $channel = null,
        $targetType = null,
        $tenant = null,
        array $individual = [],
        bool $sendInstance = false,
        string $title = null,
        string $message = null
    ) {
        // Store raw MallSession for database persistence
        if ($modelInstance instanceof MallSession) {
            $this->rawMallSession = $modelInstance;
            Log::channel('notifications')->info('Stored raw MallSession instance', [
                'mall_session_id' => $modelInstance->id,
                'mall_session_hash' => $modelInstance->hash,
            ]);
        }
        
        parent::__construct(
            $modelInstance, $data, $type, $scope, $targets, $channel, 
            $targetType, $tenant, $individual, $sendInstance, $title, $message
        );

        // Explicitly call buildNotification for MallSession notifications
        if ($this->rawMallSession instanceof MallSession) {
            Log::channel('notifications')->info('Calling buildNotification for MallSession');
            $this->buildNotification();
        }
    }

    /**
     * Build notification and persist to database
     */
    public function buildNotification()
    {
        // Call child class implementation
        $this->buildNotificationPayload();
        
        // Persist to database
        $this->persistNotification();
    }

    /**
     * Persist notification to mall_session_notifications table
     */
    protected function persistNotification()
    {
        $mallSession = $this->rawMallSession;

        if (!$mallSession || !($mallSession instanceof MallSession)) {
            Log::channel('notifications')->warning('Cannot persist: Invalid MallSession', [
                'notification_class' => get_class($this),
            ]);
            return;
        }

        try {
            $notificationData = [
                'mall_session_id' => $mallSession->id,
                'type' => $this->type ?? $this->data['event'] ?? 'mall_notification',
                'title' => $this->notificationPayload->title ?? 'Mall Notification',
                'message' => $this->notificationPayload->message ?? '',
                'data' => $this->data,
                'tenant_id' => $this->data['tenant_id'] ?? null,
                'tenant_name' => $this->data['tenant_name'] ?? null,
                'status' => $this->data['status'] ?? null,
                'is_read' => false,
                'reference_type' => isset($this->data['master_tab_id']) 
                    ? 'Domain\App\Models\Tab\Tab' : null,
                'reference_id' => $this->data['master_tab_id'] ?? null,
            ];

            $notification = MallSessionNotification::create($notificationData);

            Log::channel('notifications')->info('Notification persisted', [
                'notification_id' => $notification->id,
                'session_hash' => $mallSession->hash,
                'type' => $notificationData['type'],
            ]);

        } catch (\Exception $e) {
            Log::channel('notifications')->error('Error persisting notification', [
                'error' => $e->getMessage(),
                'session_hash' => $mallSession->hash ?? 'unknown',
            ]);
        }
    }

    /**
     * Child classes must implement this
     */
    abstract protected function buildNotificationPayload();
}
```

---

### MallSessionOrderStatusNotification

**File Path:** `domain/app/Notifications/Mall/MallSessionOrderStatusNotification.php`

**Purpose:** Notification for order status updates.

```php
class MallSessionOrderStatusNotification extends BaseMallSessionNotification
{
    public static function config()
    {
        return [
            "name" => MallSessionOrderStatusNotification::class,
            "active" => true,
            "channels" => [
                "socket" => true,    // Real-time WebSocket
                "mail" => false,     // No email
                "database" => true,  // Persist to DB
                "push" => false,     // No push for status updates
            ],
            "delay" => 0,
        ];
    }

    protected function buildNotificationPayload()
    {
        Log::channel('notifications')->info("Building MallSessionOrderStatusNotification");

        $tenantName = $this->data['tenant_name'] ?? 'A store';
        $status = strtolower($this->data['status'] ?? 'updated');
        $productCount = isset($this->data['products']) ? count($this->data['products']) : 0;

        $title = $this->getStatusTitle($status, $tenantName);
        $message = $this->getStatusMessage($tenantName, $status, $productCount);

        // Set priority based on status
        $this->data['priority'] = $this->getMessagePriority($status);
        $this->data['type'] = 'mall_order_status_update';

        $this->notificationPayload = new AppNotificationPayload(
            self::class,
            $title,
            $message,
            $this->data,
            $this->type ?? 'mall_order_status_update'
        );
    }

    private function getStatusTitle(string $status, string $tenantName): string
    {
        return match ($status) {
            'in_preparation' => __('tabs.mall_notifications.order_in_preparation'),
            'prepared' => __('tabs.mall_notifications.order_ready'),
            'delivered' => __('tabs.mall_notifications.order_ready_pickup'),
            'closed' => __('tabs.mall_notifications.order_completed'),
            'cancelled' => __('tabs.mall_notifications.order_cancelled'),
            'confirmed' => __('tabs.mall_notifications.order_confirmed'),
            default => __('tabs.mall_notifications.order_status_updated', [
                'store' => $tenantName,
                'status' => $status,
            ]),
        };
    }

    private function getStatusMessage(string $tenantName, string $status, int $productCount): string
    {
        return match ($status) {
            'in_preparation' => __('tabs.mall_notifications.order_in_preparation_message', [
                'store' => $tenantName,
            ]),
            'prepared' => __('tabs.mall_notifications.order_prepared_message', [
                'store' => $tenantName,
                'count' => $productCount,
            ]),
            'delivered' => __('tabs.mall_notifications.order_delivered_message', [
                'store' => $tenantName,
            ]),
            default => __('tabs.mall_notifications.order_status_message', [
                'store' => $tenantName,
                'status' => $status,
            ]),
        };
    }

    private function getMessagePriority(string $status): string
    {
        return match ($status) {
            'prepared', 'delivered', 'cancelled' => 'high',
            'in_preparation', 'confirmed' => 'normal',
            default => 'low',
        };
    }
}
```

---

### MallSessionTabCreationNotification

**File Path:** `domain/app/Notifications/MallSessionTabCreationNotification.php`

**Purpose:** Notification when a new order is created.

```php
class MallSessionTabCreationNotification extends BaseMallSessionNotification
{
    public static function config()
    {
        return [
            "name" => MallSessionTabCreationNotification::class,
            "active" => true,
            "channels" => [
                "socket" => true,    // Real-time
                "mail" => false,
                "database" => true,  // Persist
                "push" => true,      // Push to staff
            ],
            "delay" => 0,
        ];
    }

    protected function buildNotificationPayload()
    {
        Log::channel('notifications')->info("Building MallSessionTabCreationNotification");

        $customerName = $this->data['customer_info']['name'] ?? 'Customer';
        $tableNumber = $this->data['customer_info']['table'] ?? '';

        $title = __('tabs.mall_notifications.new_order_created');

        if (isset($this->data['tenant_name'])) {
            $title = __('tabs.mall_notifications.new_order_at_store', [
                'store' => $this->data['tenant_name'],
            ]);
        }

        $productCount = isset($this->data['products']) ? count($this->data['products']) : 0;

        if ($productCount > 0) {
            $message = __('tabs.mall_notifications.new_order_with_items', [
                'customer' => $customerName,
                'table' => $tableNumber,
                'count' => $productCount,
            ]);
        } elseif ($tableNumber) {
            $message = __('tabs.mall_notifications.new_order_message', [
                'customer' => $customerName,
                'table' => $tableNumber,
            ]);
        } else {
            $message = __('tabs.mall_notifications.new_order_message_no_table', [
                'customer' => $customerName,
            ]);
        }

        $this->notificationPayload = new AppNotificationPayload(
            self::class,
            $title,
            $message,
            $this->data,
            $this->type ?? 'mall_tab_creation'
        );
    }
}
```

---

### MallStoreAssistanceNotification

**File Path:** `domain/app/Notifications/Mall/MallStoreAssistanceNotification.php`

**Purpose:** Urgent notification when customer requests staff assistance.

```php
class MallStoreAssistanceNotification extends BaseMallSessionNotification
{
    public static function config()
    {
        return [
            "name" => MallStoreAssistanceNotification::class,
            "active" => true,
            "channels" => [
                "socket" => true,
                "mail" => false,
                "database" => false,  // Don't persist assistance requests
                "push" => true,       // Push is critical for assistance
            ],
            "delay" => 5, // 5 second delay to prevent spam
        ];
    }

    protected function buildNotificationPayload()
    {
        $customerName = $this->data['customer_name'] ?? 'A customer';
        $tableNumber = $this->data['table_number'] ?? 'unknown';
        $storeName = $this->data['store_name'] ?? 'your store';

        $title = __('tabs.mall_notifications.assistance_requested');
        $message = __('tabs.mall_notifications.assistance_message', [
            'customer' => $customerName,
            'table' => $tableNumber,
        ]);

        $this->data['priority'] = 'urgent';
        $this->data['sound'] = 'alert';
        $this->data['vibration'] = true;

        $this->notificationPayload = new AppNotificationPayload(
            self::class,
            $title,
            $message,
            $this->data,
            'mall_assistance_request'
        );
    }
}
```

---

## AppNotificationBuilder

**File Path:** `app/AppNotifications/AppNotificationBuilder.php`

**Purpose:** Central notification dispatcher that routes to appropriate channels.

### Key Method: `send()`

```php
public static function send(
    string $notificationClass,
    array $data = [],
    string $channel = null,
    string $scope = "channel",
    $modelInstance = null,
    string $type = null,
    array $targets = [],
    string $targetType = "role",
    $tenant = null,
    array $individual = [],
    bool $sendInstance = false,
    string $title = null,
    string $message = null
): void
{
    // Get notification config
    $notificationConfig = $notificationClass::config();

    $config_is_active = $notificationConfig['active'] ?? true;
    if (!$config_is_active) {
        Log::channel('notifications')->info("Notification disabled", [
            'class' => $notificationClass,
        ]);
        return;
    }

    // Socket channel (WebSocket)
    if ($notificationConfig['channels']['socket'] ?? false) {
        Log::channel('notifications')->info("Sending WebSocket notification", [
            'channel' => $channel,
            'scope' => $scope,
        ]);

        event(new AppNotification(new $notificationClass(
            modelInstance: $modelInstance,
            data: $data,
            type: $type,
            scope: $scope,
            targets: $targets,
            channel: $channel,
            targetType: $targetType,
            tenant: $tenant,
            individual: [],
            sendInstance: $sendInstance,
            title: $title,
            message: $message
        )));
    }

    // Database channel
    if ($notificationConfig['channels']['database'] ?? false) {
        Log::channel('notifications')->info("Database notification enabled", [
            'class' => $notificationClass,
            'scope' => $scope,
        ]);
        
        // For role-based notifications, send to users
        if ($scope === 'channel' && $targetType === 'role') {
            $users = self::getUsersByRoles($targets, $channel);
            
            foreach ($users as $user) {
                $dbNotification = new $notificationClass(
                    $modelInstance, $data, $type, 'private', $targets,
                    null, $targetType, $tenant, [], $sendInstance, $title, $message
                );
                $dbNotification->buildNotification();
                $user->notify(new AppNotification($dbNotification));
            }
        }
        // Note: Mall session notifications handle their own persistence
        // via BaseMallSessionNotification::persistNotification()
    }

    // Push channel (FCM)
    if (in_array('push', $individual) || ($notificationConfig['channels']['push'] ?? false)) {
        Log::channel('notifications')->info("Sending push notification", [
            'targets' => $targets,
        ]);
        
        // Get FCM tokens for target users
        $tokens = self::getFcmTokensForTargets($targets, $channel, $tenant);
        
        if (!empty($tokens)) {
            self::sendFcmNotification($notificationClass, $data, $tokens, $title, $message);
        }
    }
}
```

---

## WebSocket Channels

### Channel Naming Convention

| Channel Type | Format | Scope | Purpose |
|--------------|--------|-------|---------|
| Session | `session.{hash}` | public | Customer notifications |
| Tenant System | `tenant.{id}.system` | channel | Staff notifications |
| User Private | `user.{id}` | private | Individual notifications |

### Channel Subscription (Frontend)

```typescript
// Public session channel
const echo = new Echo({
    broadcaster: 'pusher',
    key: process.env.PUSHER_KEY,
    cluster: process.env.PUSHER_CLUSTER,
});

// Subscribe to session channel
echo.channel(`session.${sessionHash}`)
    .listen('.mall_order_status_update', (event) => {
        // Handle status update
        console.log('Order status updated:', event);
    })
    .listen('.mall_tab_creation', (event) => {
        // Handle new order confirmation
        console.log('Order created:', event);
    });
```

### Channel Authorization (Backend)

```php
// routes/channels.php

// Public channels (no auth required)
Broadcast::channel('session.{hash}', function () {
    return true; // Public - anyone can listen
});

// Private channels (auth required)
Broadcast::channel('tenant.{tenantId}.system', function ($user, $tenantId) {
    return $user->tenant_id === (int) $tenantId;
});

Broadcast::channel('user.{userId}', function ($user, $userId) {
    return $user->id === (int) $userId;
});
```

---

## Notification Data Structure

### Order Status Update Payload

```json
{
    "event": "mall_order_status_update",
    "type": "mall_order_status_update",
    "tenant_tab_id": 123,
    "tenant_id": 45,
    "tenant_name": "Pizza Place",
    "status": "IN_PREPARATION",
    "master_tab_id": 100,
    "child_order_id": 123,
    "parent_order_id": 100,
    "timestamp": "2025-12-08T10:30:00.000000Z",
    "customer_info": {
        "name": "John Doe",
        "table": "15"
    },
    "products": [
        {
            "id": 1,
            "product_id": 50,
            "name": "Margherita Pizza",
            "quantity": 2,
            "status": "IN_PREPARATION",
            "image_url": "https://..."
        }
    ],
    "mall_session_hash": "M5U2W",
    "priority": "normal"
}
```

### Tab Creation Payload

```json
{
    "event": "mall_tab_creation",
    "type": "mall_tab_creation",
    "tenant_id": 45,
    "tenant_name": "Pizza Place",
    "master_tab_id": 100,
    "tenant_tab_id": 123,
    "customer_info": {
        "name": "John Doe",
        "table": "15"
    },
    "products": [
        {
            "id": 50,
            "name": "Margherita Pizza",
            "quantity": 2
        }
    ],
    "mall_session_hash": "M5U2W"
}
```

---

## Translation Keys

```php
// lang/en/tabs.php

return [
    'mall_notifications' => [
        // Status titles
        'order_in_preparation' => 'Order in preparation',
        'order_ready' => 'Order ready!',
        'order_ready_pickup' => 'Ready for pickup',
        'order_completed' => 'Order completed',
        'order_cancelled' => 'Order cancelled',
        'order_confirmed' => 'Order confirmed',
        'order_status_updated' => ':store updated your order to :status',

        // Status messages
        'order_in_preparation_message' => ':store is preparing your order',
        'order_prepared_message' => ':store has :count items ready',
        'order_delivered_message' => ':store has delivered your order',
        'order_status_message' => ':store: Order is now :status',

        // Tab creation
        'new_order_created' => 'New order created',
        'new_order_at_store' => 'New order at :store',
        'new_order_message' => 'Order from :customer at table :table',
        'new_order_message_no_table' => 'Order from :customer',
        'new_order_with_items' => ':customer at table :table ordered :count items',

        // Assistance
        'assistance_requested' => 'Assistance requested!',
        'assistance_message' => ':customer at table :table needs help',
    ],
];
```
