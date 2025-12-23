# Dash Email Notification System - Technical Documentation

## Overview

The Dash Email Notification System is a multi-channel notification infrastructure that supports WebSocket (real-time), Email, Database (persistence), and Push (FCM) delivery. This document focuses on the **email notification** capabilities and how **tenant branding** is injected into all email templates.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EMAIL NOTIFICATION FLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                 AppNotificationBuilder::send()                      │   │
│   │   - Entry point for all notifications                               │   │
│   │   - Accepts: notificationClass, data, modelInstance, tenant, etc.  │   │
│   └────────────────────────────────┬────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                   AppNotificationBase (Abstract)                    │   │
│   │   - Constructor calls processTenantData()                          │   │
│   │   - Resolves tenant from: explicit param, modelInstance->tenant_id │   │
│   │   - Uses TenantResource to convert tenant model to array           │   │
│   │   - Normalizes tenant data (logo URLs, colors, contact info)       │   │
│   └────────────────────────────────┬────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      AppNotification                                │   │
│   │   toMail($notifiable):                                              │   │
│   │     - Gets tenantData via getTenantData()                          │   │
│   │     - Injects 'tenant' and 'tenantData' into view data             │   │
│   │     - Sets FROM email/name from tenant contact info                │   │
│   │     - Renders view: notifications.{mailView} or notifications.generic │
│   └────────────────────────────────┬────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      Blade Email Templates                          │   │
│   │   - layouts/emails.blade.php (main layout with tenant branding)    │   │
│   │   - notifications/tab_order.blade.php (order notifications)        │   │
│   │   - notifications/generic.blade.php (fallback template)            │   │
│   │   - Uses data_get_safe() for stdClass/array compatibility          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. AppNotificationBuilder (`app/AppNotifications/AppNotificationBuilder.php`)

**Purpose:** Entry point for sending all notifications in the system.

**Method Signature:**
```php
public static function send(
    string $notificationClass,          // Notification class to use
    array $data = [],                    // Notification data payload
    $modelInstance = null,               // Model instance (used for tenant resolution)
    string $type = null,                 // Notification type identifier
    string $scope = "channel",           // [private|channel|public]
    array $targets = [],                 // Target user IDs or role names
    string $targetType = null,           // [user|role]
    string $channel = null,              // Channel name (e.g., "tenant.1.system")
    $tenant = null,                      // Tenant model or data (for branding)
    array $individual = [],              // Individual channels: ["push", "mail", "database", "socket"]
    bool $sendInstance = false,          // Include model in payload
    string $title = null,                // Notification title
    string $message = null,              // Notification message
    array $config = []                   // Additional configuration
)
```

**Tenant Data Flow:**
1. If `$tenant` parameter is provided explicitly, it's used directly
2. If not provided, system attempts to resolve from `$modelInstance->tenant_id`
3. Tenant model is converted to array via `TenantResource`

---

### 2. AppNotificationBase (`app/AppNotifications/AppNotificationBase.php`)

**Purpose:** Abstract base class for all notification types with tenant data processing.

**Key Methods:**

| Method | Description |
|--------|-------------|
| `processTenantData()` | Main method that processes and normalizes tenant data |
| `resolveTenantFromModelInstance()` | Resolves tenant from model's `tenant_id` attribute |
| `normalizeTenantData()` | Ensures all required fields exist with defaults |
| `getTenantData()` | Returns tenant data as array (handles object conversion) |
| `cleanResourceData()` | Removes MissingValue objects from resource output |

**Tenant Data Resolution Priority:**
1. **Explicit tenant parameter** - If passed to `AppNotificationBuilder::send(tenant: $tenant)`
2. **Model instance resolution** - If `$modelInstance->tenant_id` exists, loads tenant model
3. **Default configuration** - Falls back to app configuration defaults

**Normalized Tenant Data Fields:**
```php
[
    'id' => int,
    'name' => string,
    'display_name' => string,
    'email' => string,
    'contact_email' => string,
    'phone' => string,
    'address' => string,
    'logo_url' => string,              // Full URL
    'horizontal_logo_url' => string,   // Full URL
    'squared_logo_url' => string,      // Full URL
    'banner_url' => string,            // Full URL
    'dashboard_url' => string,
    'support_url' => string,
    'settings' => [
        'colors' => [
            'primary-color' => string,
            'secondary-color' => string,
            'primary-contrast' => string,
            'highlight-color' => string,
            // ... more color settings
        ]
    ]
]
```

---

### 3. AppNotification (`app/AppNotifications/AppNotification.php`)

**Purpose:** Laravel Notification implementation that handles email delivery.

**Key Method - `toMail()`:**
```php
public function toMail($notifiable)
{
    // Get tenant data (always returns array)
    $tenantData = $this->notification->getTenantData();
    
    $data = [
        'notifiable' => $notifiable,
        'modelInstance' => $this->notification->modelInstance,
        'notificationPayload' => $this->notification->notificationPayload->getMessageObject(),
        'model' => $this->notification->model,
        'target' => $this->notification->targetUser,
        'targetType' => $this->notification->targetType,
        'mailSubject' => $this->notification->mailSubject,
        'data' => $this->notification->data,
        'type' => $this->notification->type,
        
        // TENANT DATA INJECTION
        'tenant' => $tenantData,
        'tenantData' => $tenantData,  // Alias for backward compatibility
    ];

    // FROM field uses tenant branding
    $fromEmail = $tenantData['contact_email'] ?? $tenantData['email'] ?? env('MAIL_FROM_ADDRESS');
    $fromName = $tenantData['display_name'] ?? $tenantData['name'] ?? env('MAIL_FROM_NAME');

    return (new MailMessage)
        ->from($fromEmail, $fromName)
        ->subject($this->notification->mailSubject)
        ->view($this->mailView, $data);
}
```

---

## Email-Enabled Notification Classes

The following notification classes have the `mail` channel enabled:

### Core System Notifications

| Notification Class | Location | Email View | Description |
|--------------------|----------|------------|-------------|
| `TabChannelNotification` | `domain/app/Notifications/Tab/` | `notifications.tab_order` | Order status updates (CREATED, CONFIRMED, PREPARED, etc.) |
| `TenantChannelMessageNotification` | `app/AppNotifications/Notifications/` | `notifications.generic` | Tenant channel messages |
| `PrivateMessageNotification` | `app/AppNotifications/Notifications/` | `notifications.generic` | Private user messages |
| `UserTestMessageNotification` | `domain/app/Notifications/ECommerce/` | `notifications.generic` | Test notifications |

### E-Commerce Notifications

| Notification Class | Location | Email View | Description |
|--------------------|----------|------------|-------------|
| `ProductImportNotification` | `domain/app/Notifications/ECommerce/` | `notifications.generic` | Mass product import completion |
| `ValidateProductImportNotification` | `domain/app/Notifications/ECommerce/` | `notifications.generic` | Product import validation results |
| `CampaignMarketplaceProductImportNotification` | `domain/app/Notifications/ECommerce/` | `notifications.generic` | Campaign product publishing status |

---

## Email Templates

### Main Layout: `layouts/emails.blade.php`

**Location:** `resources/views/layouts/emails.blade.php`

**Features:**
- Responsive email design with mobile-first approach
- Dynamic tenant branding (logo, colors)
- Safe data accessor function `data_get_safe()` for stdClass/array compatibility
- CSS variable-based theming using tenant settings

**Tenant Data Usage:**
```php
@php
    // Support both $tenant and $tenantData variable names
    $rawTenant = $tenant ?? $tenantData ?? null;
    
    // Extract values using safe accessor
    $displayName = data_get_safe($rawTenant, 'display_name', config('app.name'));
    $settings = data_get_safe($rawTenant, 'settings', null);
    $colors = data_get_safe($settings, 'colors', null);
    
    // Get color values with fallbacks
    $primaryColor = data_get_safe($colors, 'primary-color--light', '#417300');
    $secondaryColor = data_get_safe($colors, 'secondary-color--light', '#20274e');
    // ... more colors
@endphp
```

### Tab Order Template: `notifications/tab_order.blade.php`

**Location:** `resources/views/notifications/tab_order.blade.php`

**Extends:** `layouts.emails`

**Features:**
- Order details display (products, prices, modifiers)
- Marketplace branding (Uber, Jumpseller, etc.)
- Delivery information
- Customer information
- Order totals

**Tenant Data Usage:**
```php
@php
    // Normalize tenant data (handles stdClass conversion)
    if (isset($tenant) && is_object($tenant)) {
        $tenant = json_decode(json_encode($tenant), true);
    }
    $tenantData = $tenantData ?? $tenant ?? [];
    
    // Get company info
    $companyName = $tenantData['name'] ?? config('app.name');
    $logoUrl = $tenantData['horizontal_logo_url'] ?? $tenantData['squared_logo_url'] ?? null;
@endphp

{{-- Display Logo --}}
@if($logoUrl)
<tr>
    <td align="center" style="padding: 24px 0;">
        <img src="{{ $logoUrl }}" alt="{{ $companyName }}" style="max-width: 200px;">
    </td>
</tr>
@endif
```

### Generic Template: `notifications/generic.blade.php`

**Location:** `resources/views/notifications/generic.blade.php`

**Extends:** `notifications.layout`

**Purpose:** Fallback template for notifications without custom email views.

---

## Sending Email Notifications - Usage Examples

### Example 1: Order Status Notification (with explicit tenant)

```php
use App\AppNotifications\AppNotificationBuilder;
use Domain\App\Notifications\Tab\TabChannelNotification;

// Load tenant with media for logo URLs
$tenant = $tab->tenant;
$tenant->load('media');

AppNotificationBuilder::send(
    notificationClass: TabChannelNotification::class,
    channel: "tenant.{$tab->tenant_id}.system",
    scope: "channel",
    modelInstance: $tab,
    targets: ['kitchen', 'staff', 'admin'],
    targetType: "role",
    individual: ['mail'],  // Enable email for these users
    tenant: $tenant,       // Explicit tenant for branding
    title: "New Order #{$tab->id}",
    message: "A new order has been placed",
    data: [
        'tab_id' => $tab->id,
        'status' => $tab->status,
        'order_items' => $orderItems,
    ],
    type: 'tab.new_order'
);
```

### Example 2: Notification with Automatic Tenant Resolution

```php
// When modelInstance has tenant_id, tenant is resolved automatically
AppNotificationBuilder::send(
    notificationClass: ProductImportNotification::class,
    modelInstance: $importJob,  // Has tenant_id attribute
    targets: ['tenant_admin'],
    targetType: "role",
    // tenant: not passed - will be resolved from $importJob->tenant_id
    title: "Import Completed",
    message: "Your product import has finished",
    data: $importResults,
    type: 'import.complete'
);
```

### Example 3: Private User Notification

```php
AppNotificationBuilder::send(
    notificationClass: PrivateMessageNotification::class,
    scope: "private",
    targets: [$user->id],
    targetType: "user",
    tenant: $user->tenant,
    title: "Account Update",
    message: "Your account settings have been changed",
    data: $changeDetails,
    type: 'user.account_update'
);
```

---

## Tenant Data Injection Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TENANT DATA INJECTION FLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. CALLER sends notification:                                              │
│     AppNotificationBuilder::send(                                           │
│         tenant: $tenant,        // Option A: Explicit                       │
│         modelInstance: $model,  // Option B: Auto-resolve from model        │
│     )                                                                        │
│                                                                              │
│  2. AppNotificationBase CONSTRUCTOR:                                        │
│     ├── If $tenant provided:                                                │
│     │   └── Use TenantResource to convert to array                         │
│     │                                                                        │
│     ├── Else if $modelInstance->tenant_id exists:                           │
│     │   └── Load Tenant model → Use TenantResource                          │
│     │                                                                        │
│     └── Else:                                                                │
│         └── Use default tenant data from config                             │
│                                                                              │
│  3. normalizeTenantData():                                                  │
│     ├── Process logo URLs (relative → absolute)                             │
│     ├── Set fallback values for missing fields                              │
│     └── Build dashboard/support URLs                                        │
│                                                                              │
│  4. AppNotification::toMail():                                              │
│     ├── Call getTenantData() → returns normalized array                     │
│     ├── Inject into view as $tenant and $tenantData                         │
│     └── Set FROM email/name from tenant contact info                        │
│                                                                              │
│  5. EMAIL TEMPLATE (layouts/emails.blade.php):                              │
│     ├── Extract tenant colors → apply as inline styles                      │
│     ├── Display tenant logo                                                 │
│     └── Show tenant name in footer                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_MAIL_ENABLED` | Enable/disable email sending | `false` |
| `MAIL_FROM_ADDRESS` | Default FROM email (fallback) | `no-reply@undefined.cl` |
| `MAIL_FROM_NAME` | Default FROM name (fallback) | `UNDEFINED` |

### Notification Class Configuration

Each notification class defines its channel configuration via the static `config()` method:

```php
class TabChannelNotification extends AppNotificationBase
{
    public static function config()
    {
        return [
            "name"     => TabChannelNotification::class,
            "active"   => true,
            "channels" => [
                "socket"   => true,   // WebSocket (real-time)
                "mail"     => true,   // Email
                "database" => true,   // Database persistence
                "push"     => true,   // Firebase Cloud Messaging
            ],
            "mailView" => "notifications.tab_order",  // Custom email template
        ];
    }
}
```

---

## Best Practices

### 1. Always Load Tenant Media Relations

When passing tenant explicitly, ensure media relations are loaded for logo URLs:

```php
$tenant = $tab->tenant;
$tenant->load('media');

AppNotificationBuilder::send(
    tenant: $tenant,
    // ...
);
```

### 2. Use Specific Email Templates for Important Notifications

Create dedicated templates for critical notifications:

```php
public static function config()
{
    return [
        // ...
        "mailView" => "notifications.my_custom_template",
    ];
}
```

### 3. Handle stdClass in Templates

Always use `data_get_safe()` or explicit conversion:

```php
@php
    if (isset($tenant) && is_object($tenant)) {
        $tenant = json_decode(json_encode($tenant), true);
    }
@endphp
```

### 4. Verify Email Sending is Enabled

Check `APP_MAIL_ENABLED=true` in your environment:

```php
// In via() method of AppNotification
$mail && (env('APP_MAIL_ENABLED', 'false') == 'true') && $responseArray[] = "mail";
```

---

## Troubleshooting

### Email Not Sending

1. Check `APP_MAIL_ENABLED` is set to `true`
2. Verify notification class has `"mail" => true` in config
3. Check Laravel notification logs: `storage/logs/notifications.log`

### Tenant Data Missing in Email

1. Verify `$tenant` is passed to `AppNotificationBuilder::send()`
2. Check if `$modelInstance->tenant_id` exists for auto-resolution
3. Enable debug logging in `AppNotificationBase::processTenantData()`

### Logo Not Displaying

1. Ensure tenant has media relations loaded
2. Verify `horizontal_logo_url` or `squared_logo_url` is set
3. Check URL is absolute (not relative path)

---

## File Locations Summary

| Component | Path |
|-----------|------|
| AppNotificationBuilder | `app/AppNotifications/AppNotificationBuilder.php` |
| AppNotificationBase | `app/AppNotifications/AppNotificationBase.php` |
| AppNotification | `app/AppNotifications/AppNotification.php` |
| TabChannelNotification | `domain/app/Notifications/Tab/TabChannelNotification.php` |
| TenantChannelMessageNotification | `app/AppNotifications/Notifications/TenantChannelMessageNotification.php` |
| Email Layout | `resources/views/layouts/emails.blade.php` |
| Tab Order Template | `resources/views/notifications/tab_order.blade.php` |
| Generic Template | `resources/views/notifications/generic.blade.php` |
| TabsNotificationService | `domain/app/Services/Tabs/TabsNotificationService.php` |

---

## Related Documentation

- [Dash Notification System](./DASH_NOTIFICATION_SYSTEM.md) - Full multi-channel notification documentation
- [Mall App Notifications](./MALL_APP_NOTIFICATIONS.md) - Mall-specific notification flows
- [Tenant Resource](./dash-backend/app/Http/Resources/TenantResource.php) - Tenant data transformation

---

*Last Updated: January 2025*
