# Dash Notification System - Technical Documentation

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Notification Channels](#notification-channels)
- [Configuration](#configuration)
- [Components](#components)
- [Implementation Guide](#implementation-guide)
- [API Reference](#api-reference)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

The Dash Notification System is a comprehensive, multi-channel notification framework built on Laravel that provides enterprise-grade messaging capabilities including real-time WebSocket communication, email notifications, database storage, and Firebase push notifications. The system supports delayed delivery, multi-tenant architecture, role-based targeting, and seamless integration with the Dash ecosystem.

### Key Features
- **Multi-Channel Support**: Email, WebSocket, Database, Push Notifications
- **Delayed Delivery**: Configurable notification delays
- **Multi-Tenant Aware**: Tenant-scoped notifications with proper data isolation
- **Role-Based Targeting**: Send notifications to specific user roles
- **Real-Time Broadcasting**: WebSocket integration for instant messaging
- **Firebase Integration**: Push notifications to mobile devices
- **Audit Trail**: Database storage for notification tracking
- **Flexible Configuration**: Per-notification class configuration

## Architecture

The notification system follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
├─────────────────────────────────────────────────────────────┤
│  AppNotificationBuilder (Entry Point & Orchestration)      │
├─────────────────────────────────────────────────────────────┤
│                   Notification Classes                      │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐│
│  │ AppNotification     │  │ AppNotificationBase             ││
│  │ (Laravel Handler)   │  │ (Business Logic)                ││
│  └─────────────────────┘  └─────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    Channel Handlers                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────────┐│
│  │  Mail   │ │ Socket  │ │Database │ │ Push (Firebase)     ││
│  └─────────┘ └─────────┘ └─────────┘ └─────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    External Services                        │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐│
│  │ Laravel Queue       │  │ Firebase Cloud Messaging       ││
│  │ System              │  │ (FCM)                           ││
│  └─────────────────────┘  └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Notification Channels

### 1. Database Channel (`database`)
Stores notifications in the database for audit trails and notification history.

**Features:**
- Persistent storage
- Read/unread status tracking
- Notification history
- Query capabilities

**Database Table Structure:**
```sql
notifications (
    id UUID PRIMARY KEY,
    type VARCHAR,
    notifiable_type VARCHAR,
    notifiable_id BIGINT,
    data JSON,
    read_at TIMESTAMP NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

### 2. Email Channel (`mail`)
Sends notifications via email with customizable templates and tenant-aware configuration.

**Features:**
- HTML/Text email support
- Custom email templates
- Tenant-specific "from" addresses
- Attachment support
- CC/BCC functionality

**Configuration:**
- Controlled by `APP_MAIL_ENABLED` environment variable
- Tenant-specific email settings
- Template resolution with fallbacks

### 3. WebSocket Channel (`socket`/`broadcast`)
Real-time notifications through WebSocket connections for instant messaging.

**Features:**
- Real-time delivery
- Private/Public channels
- Role-based broadcasting
- Event-driven architecture

**Channel Types:**
- **Private**: `user.{user_id}` - Direct user notifications
- **Channel**: `tenant.{tenant_id}.system` - Tenant-scoped channels
- **Public**: Global broadcast channels

### 4. Push Notification Channel (`push`)
Mobile push notifications via Firebase Cloud Messaging (FCM).

**Features:**
- Cross-platform support (iOS/Android)
- Rich notification payloads
- Token-based targeting
- Delivery confirmation
- Batch sending capabilities
- Alarm/Order priority handling for Android

**Requirements:**
- Users must have valid FCM tokens stored in `fcm_token` field
- Firebase project configuration
- FCM service account credentials

**Architecture:**

The push notification system uses a dedicated `PushChannel` class (`app/Channels/PushChannel.php`) that handles all FCM delivery:

```
┌─────────────────────────────────────────────────────────────┐
│  AppNotificationBuilder::send()                             │
│  ↓ Creates notification with channels config                │
├─────────────────────────────────────────────────────────────┤
│  AppNotification                                            │
│  ↓ via() returns ['push'] if enabled                        │
├─────────────────────────────────────────────────────────────┤
│  PushChannel::send($notifiable, $notification)              │
│  ↓ Extracts title/body from toArray()                       │
│  ↓ Handles alarm/order priority flags                       │
├─────────────────────────────────────────────────────────────┤
│  FirebaseService                                            │
│  ↓ sendNotification() / sendAlarmNotification()             │
└─────────────────────────────────────────────────────────────┘
```

**Title and Body Extraction:**

`PushChannel` extracts notification content from the `toArray()` method:
- **Title**: `$data['mailSubject']` (from `notificationPayload->title` via `AppNotificationBase`)
- **Body**: `$data['notificationPayload']['message']` (from `AppNotificationPayload->message`)

**Priority Handling:**

The system supports special notification types for Android alarm/order handling:
- `alarm: 'true'` in data → Uses `sendAlarmNotification()` (data-only, high priority)
- `order: 'true'` in data → Uses `sendOrderNotification()` (notification + data, high priority)
- Regular notifications → Uses `sendNotification()` (standard priority)

**Extra Data Payload:**

Additional fields passed to the mobile app:
- `type`: Notification type identifier
- `targetType`: 'user' or 'role'
- `timestamp`: ISO8601 timestamp
- `speech`: Text-to-speech content (if provided)
- `tab_id`: Related tab identifier (if provided)
- `alarm`: 'true' for alarm-type notifications
- `order`: 'true' for order-type notifications
- `priority`: 'high' for priority notifications

## Configuration

### Notification Class Configuration

Each notification class defines its behavior through a static `config()` method:

```php
public static function config()
{
    return [
        "name"     => self::class,
        "active"   => true,
        "channels" => [
            "socket"   => true,  // WebSocket notifications
            "mail"     => false, // Email notifications  
            "database" => false, // Database storage
            "push"     => true   // Push notifications
        ],
        "delay"    => 60,        // Delay in seconds
        "roles"    => ["admin"], // Additional role targets
        "emails"   => ["admin@example.com"] // Additional email targets
    ];
}
```

### Configuration Options

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `name` | string | Notification class name | Required |
| `active` | boolean | Enable/disable notification | `true` |
| `channels` | array | Channel configuration | `{}` |
| `delay` | integer | Delay in seconds | `0` |
| `roles` | array | Additional role targets | `[]` |
| `emails` | array | Additional email recipients | `[]` |

### Channel Configuration

| Channel | Type | Description |
|---------|------|-------------|
| `mail` | boolean | Email notifications |
| `socket` | boolean | WebSocket broadcasting |
| `database` | boolean | Database storage |
| `push` | boolean | Firebase push notifications |

## Components

### 1. AppNotificationBuilder

The main entry point for sending notifications. Handles routing, targeting, and channel management.

**File:** `app/AppNotifications/AppNotificationBuilder.php`

**Responsibilities:**
- Notification routing and orchestration
- Target resolution (users/roles)
- Channel management
- Configuration processing
- Delay implementation

### 2. AppNotification

Laravel notification class that implements the actual delivery mechanisms.

**File:** `app/AppNotifications/AppNotification.php`

**Responsibilities:**
- Channel method implementation (`toMail`, `toArray`, `toBroadcast`, `toPush`)
- Message formatting
- Delivery execution
- Error handling

### 3. AppNotificationBase

Abstract base class for specific notification implementations.

**File:** `app/AppNotifications/AppNotificationBase.php`

**Responsibilities:**
- Common notification properties
- Message building interface
- Configuration management
- Payload handling

### 4. FirebaseService

Service class for Firebase Cloud Messaging integration.

**File:** `app/Services/Firebase/FirebaseService.php`

**Responsibilities:**
- FCM token management
- Push notification delivery
- Batch messaging
- Error handling

## Implementation Guide

### Creating a New Notification

1. **Create Notification Class**

```php
<?php

namespace App\AppNotifications\Notifications;

use App\AppNotifications\AppNotificationBase;
use App\AppNotifications\AppNotificationPayload;

class OrderCompletedNotification extends AppNotificationBase
{
    public static function config()
    {
        return [
            "name"     => self::class,
            "active"   => true,
            "channels" => [
                "socket"   => true,
                "mail"     => true,
                "database" => true,
                "push"     => true
            ],
            "delay"    => 0, // Immediate delivery
        ];
    }

    public function buildNotification()
    {
        $this->notificationPayload = new AppNotificationPayload(
            self::class,
            "Order Completed",
            "Your order #{$this->data['order_id']} has been completed",
            $this->data,
            $this->type
        );
    }
}
```

2. **Send Notification**

```php
use App\AppNotifications\AppNotificationBuilder;

AppNotificationBuilder::send(
    notificationClass: OrderCompletedNotification::class,
    type: "order_completed",
    data: ['order_id' => $order->id],
    modelInstance: $order,
    targets: [$order->user_id],
    scope: "private",
    targetType: "user"
);
```

### Targeting Options

#### User Targeting
```php
AppNotificationBuilder::send(
    notificationClass: MyNotification::class,
    targets: [1, 2, 3], // User IDs
    targetType: "user"
);
```

#### Role Targeting
```php
AppNotificationBuilder::send(
    notificationClass: MyNotification::class,
    targets: ["admin", "manager"],
    targetType: "role"
);
```

#### Channel Broadcasting
```php
AppNotificationBuilder::send(
    notificationClass: MyNotification::class,
    scope: "channel",
    channel: "tenant.123.notifications",
    targets: ["admin"],
    targetType: "role"
);
```

### Delayed Notifications

Configure delays in the notification class:

```php
public static function config()
{
    return [
        "delay" => 300, // 5 minutes delay
        // ... other config
    ];
}
```

Or use Laravel's built-in delay:

```php
$user->notify((new AppNotification($notification))->delay(now()->addMinutes(5)));
```

## API Reference

### AppNotificationBuilder::send()

```php
public static function send(
    $notificationClass,     // Notification class name
    $type = "message",      // Notification type
    $data = [],            // Additional data payload
    $modelInstance = null,  // Related model instance
    $targets = [],         // Array of target IDs
    $scope = "public",     // Scope: "public", "private", "channel"
    $channel = null,       // Channel name for channel scope
    $targetType = "user",  // Target type: "user" or "role"
    $tenant = null         // Tenant context
)
```

### Channel Methods

#### toMail($notifiable)
Formats notification for email delivery.

**Returns:** `MailMessage`

#### toArray($notifiable)  
Formats notification for database storage.

**Returns:** `array`

#### toBroadcast($notifiable)
Formats notification for WebSocket broadcasting.

**Returns:** `BroadcastMessage`

#### toPush($notifiable)
Handles push notification delivery via Firebase.

**Returns:** `null` (handles delivery internally)

### Firebase Service Methods

#### sendNotification($token, $title, $body, $data = [])
Send notification to single device.

#### sendToMultipleTokens($tokens, $title, $body, $data = [])
Send notification to multiple devices.

## Best Practices

### 1. Configuration Management
- Always define explicit channel configuration
- Use environment variables for feature flags
- Keep delay values reasonable (< 24 hours)

### 2. Performance Optimization
- Use queues for high-volume notifications
- Implement batch processing for role-based notifications
- Cache role memberships for frequent lookups

### 3. Error Handling
- Implement retry mechanisms for failed deliveries
- Log notification failures with context
- Handle missing FCM tokens gracefully

### 4. Security Considerations
- Validate notification content
- Implement rate limiting
- Use tenant-scoped targeting
- Sanitize user-generated content

### 5. Testing
- Mock external services (Firebase) in tests
- Test all channel combinations
- Verify delay functionality
- Test tenant isolation

## Examples

### Basic User Notification
```php
AppNotificationBuilder::send(
    notificationClass: WelcomeNotification::class,
    type: "welcome",
    data: ['username' => $user->name],
    modelInstance: $user,
    targets: [$user->id],
    scope: "private",
    targetType: "user"
);
```

### Role-Based System Alert
```php
AppNotificationBuilder::send(
    notificationClass: SystemMaintenanceNotification::class,
    type: "system_alert",
    data: ['maintenance_time' => '2024-01-15 02:00:00'],
    targets: ["admin", "support"],
    scope: "public",
    targetType: "role"
);
```

### Tenant Channel Notification
```php
AppNotificationBuilder::send(
    notificationClass: TenantUpdateNotification::class,
    type: "tenant_update",
    data: $updateData,
    scope: "channel",
    channel: "tenant.{$tenantId}.updates",
    targets: ["manager"],
    targetType: "role"
);
```

### Delayed Email Notification
```php
class DelayedReminderNotification extends AppNotificationBase
{
    public static function config()
    {
        return [
            "channels" => ["mail" => true, "database" => true],
            "delay" => 3600, // 1 hour delay
        ];
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Notifications Not Delivered
**Symptoms:** Notifications don't reach recipients

**Solutions:**
- Check channel configuration in notification class
- Verify queue workers are running
- Check environment variables (`APP_MAIL_ENABLED`)
- Validate target user IDs exist

#### 2. Push Notifications Failing
**Symptoms:** Push notifications not received on devices

**Solutions:**
- Verify FCM tokens are stored in user records
- Check Firebase service configuration
- Validate FCM credentials and project ID
- Test Firebase connectivity

#### 3. WebSocket Broadcasting Issues
**Symptoms:** Real-time notifications not appearing

**Solutions:**
- Verify WebSocket server is running
- Check channel subscription in frontend
- Validate broadcasting configuration
- Test WebSocket connectivity

#### 4. Delayed Notifications Not Working
**Symptoms:** Notifications sent immediately despite delay config

**Solutions:**
- Ensure queue workers are processing jobs
- Check queue configuration
- Verify delay value format (seconds)
- Test with small delay values first

### Debug Commands

```bash
# Check queue status
php artisan queue:work --verbose

# Clear notification cache
php artisan cache:clear

# Test Firebase connectivity
php artisan tinker
>>> app(\App\Services\Firebase\FirebaseService::class)->sendNotification('test-token', 'Test', 'Test message')

# View notification logs
tail -f storage/logs/laravel.log | grep notifications
```

### Log Channels

The system uses dedicated log channels for better debugging:

```php
// View notification logs
Log::channel('notifications')->info('Notification sent', $data);
```

Configure in `config/logging.php`:
```php
'channels' => [
    'notifications' => [
        'driver' => 'daily',
        'path' => storage_path('logs/notifications.log'),
        'level' => 'debug',
    ],
]
```

## Marketplace Order Notifications

### Overview
The Dash system provides specialized notifications for marketplace orders (Uber Eats, Jumpseller, etc.) through the `TabsNotificationService`. These notifications are sent when orders are created, confirmed, or cancelled, and integrate with the tab status workflow.

### Notification Types

#### 1. Tab Status Notification (`TabChannelNotification`)
Sent when a tab's status changes (CREATED, CONFIRMED, IN_PREPARATION, PREPARED, DELIVERED, CLOSED, CANCELLED).

**Data Payload:**
```php
$data = [
    "user" => $userId,                    // User who triggered the change
    "old" => $oldStatus,                   // Previous status
    "new" => $newStatus,                   // New status
    "message" => $localizedMessage,        // Localized status message
    "type" => "tab.status",               // Notification type
    "marketplace" => $marketplaceInfo,     // Marketplace details
    "tab_id" => $tabId,                   // Tab identifier
    
    // Added for enriched notifications (CREATED/CONFIRMED status):
    "event" => "marketplace_order_status", // Event type for consistency
    "status" => $newStatus,               // Current status
    "timestamp" => "ISO8601 datetime",    // Event timestamp
    "order_id" => $orderId,               // Order identifier
    "tenant_id" => $tenantId,             // Tenant identifier
    "tenant_name" => $tenantName,         // Tenant name
    "customer" => [                       // Customer information
        "name" => $customerName,
        "email" => $customerEmail,
        "phone" => $customerPhone
    ],
    "delivery" => [                       // Delivery information
        "method" => "delivery|counter|table",
        "method_label" => $label,
        "shipping_option" => $shippingOption,
        "address" => [...]                // Shipping address if delivery
    ],
    "order_items" => [...],               // Order products with modifiers
    "order_totals" => [                   // Order amounts
        "subtotal" => $subtotal,
        "shipping" => $shipping,
        "discount" => $discount,
        "total" => $total,
        "currency" => "CLP"
    ]
];
```

### Marketplace-Specific Behavior

#### Uber Eats Orders
- **CREATED status**: Email notification is **NOT** sent (only WebSocket). Uber orders require manual confirmation first.
- **CONFIRMED status**: Email + Push + WebSocket notifications are sent with alarm sound.
- **CANCELLED by restaurant**: Automatically calls Uber API to reject the order if still in CREATED state.
- **Timeout/Failure webhook**: Tab and order are automatically cancelled when Uber sends timeout notification.

#### Jumpseller Orders
- **CREATED status**: Email + WebSocket notifications are sent immediately (orders arrive pre-paid).
- **CONFIRMED status**: Email + Push + WebSocket notifications with alarm sound.

### Email Notification Template
Email notifications use the `notifications.tab_order` Blade template located at:
```
resources/views/notifications/tab_order.blade.php
```

The template displays:
- Order header with marketplace branding
- Order status badge
- Customer information
- Delivery method and address
- Order items with modifiers
- Order totals
- Footer with "Powered by Dash" branding

### Implementation Example

```php
use Domain\App\Services\Tabs\TabsNotificationService;

// Inject the service
$tabNotificationService = app(TabsNotificationService::class);

// Send notification for status change
$tabNotificationService->handleStatusChange($tab, Tab::STATUS_CONFIRMED, true);
```

### Channel Configuration

Tab notifications use the tenant system channel:
```php
"channel" => "tenant.{$tab->tenant_id}.system"
```

Target roles: `['kitchen', 'staff', 'admin']`

### Related Services

- `TabsNotificationService`: Main service for tab status notifications
- `UberService::rejectOrder()`: Rejects Uber order when tab is cancelled
- `WebhookTrait::processOrderFailure()`: Handles Uber timeout/failure webhooks
- `TabChannelNotification`: Notification class with email template configuration

### Configuration

The `TabChannelNotification` class configuration:
```php
public static function config()
{
    return [
        'active' => true,
        'channels' => ['database' => false, 'mail' => false, 'push' => false],
        'subject' => 'Actualización de Pedido',
        'mailView' => 'notifications.tab_order'
    ];
}
```

Note: Channel settings are overridden dynamically by `TabsNotificationService::sendNotification()` based on tab status.
````

---

*This documentation covers the complete Dash Notification System implementation. For additional support or feature requests, please refer to the project's issue tracker or contact the development team.*
