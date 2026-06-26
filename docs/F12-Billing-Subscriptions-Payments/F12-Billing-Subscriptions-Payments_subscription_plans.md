---
layout: default
title: F12-Billing-Subscriptions-Payments subscription plans
---

# Subscription Plans Management

## Overview

The Subscription Plans Management feature allows System Administrators to manage subscription plans with dynamic limits configuration. This module follows the same patterns as the Tenant Settings module, providing a backend-driven, config-based approach to defining plan limits.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SUBSCRIPTION PLANS ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                        BACKEND (Laravel)                              │  │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│   │  │ subscription_   │  │ SubscriptionPlan│  │ Subscription       │   │  │
│   │  │ plans.php       │  │ Controller      │  │ PlanRequest        │   │  │
│   │  │ (config)        │  │                 │  │                    │   │  │
│   │  └────────┬────────┘  └────────┬────────┘  └─────────┬──────────┘   │  │
│   │           │                    │                      │              │  │
│   │           ▼                    ▼                      ▼              │  │
│   │  ┌──────────────────────────────────────────────────────────────┐   │  │
│   │  │                    API Endpoints                              │   │  │
│   │  │  GET  /api/system/subscription-plan                           │   │  │
│   │  │  POST /api/system/subscription-plan                           │   │  │
│   │  │  GET  /api/system/subscription-plan/{id}                      │   │  │
│   │  │  PUT  /api/system/subscription-plan/{id}                      │   │  │
│   │  │  GET  /api/system/subscription-plan/limitFormats              │   │  │
│   │  └──────────────────────────────────────────────────────────────┘   │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                     │                                        │
│                                     ▼                                        │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                       FRONTEND (React)                                │  │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│   │  │ subscriptionPlan│  │ PlanLimits      │  │ systemResources.tsx │   │  │
│   │  │ Schema          │  │ Settings.tsx    │  │ (Resource Config)   │   │  │
│   │  └────────┬────────┘  └────────┬────────┘  └─────────┬───────────┘   │  │
│   │           │                    │                      │              │  │
│   │           ▼                    ▼                      ▼              │  │
│   │  ┌──────────────────────────────────────────────────────────────┐   │  │
│   │  │              System Admin Dashboard (KitchnTabs-System)       │   │  │
│   │  │              /system/subscription-plan                         │   │  │
│   │  └──────────────────────────────────────────────────────────────┘   │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Backend Components

### 1. Configuration File

**File:** `config/subscription_plans.php`

This file defines the limit formats that are available for subscription plans. Each limit has:

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier for the limit |
| `group` | string | Logical grouping (tenants, products, etc.) |
| `tab` | string | UI tab where this limit appears |
| `attribute` | string | Key used in the limits JSON |
| `label` | string | Display label |
| `type` | string | `boolean` or `integer` |
| `rules` | string | Laravel validation rules |
| `default_value` | mixed | Default value for new plans |
| `description` | string | Help text for the field |

**Limit Groups:**

- **Tenants:** Max users, max locations
- **Products:** Max products, max categories, max modifiers
- **Orders:** Max orders per day/month
- **Storage:** Max media storage (MB), max images
- **Features:** Feature toggles (analytics, API access, reports)
- **Notifications:** Push notifications, SMS, email limits

**Example:**

```php
'limit_formats' => [
    [
        'id' => 'max_products',
        'group' => 'products',
        'tab' => 'Product Limits',
        'attribute' => 'max_products',
        'label' => 'Maximum Products',
        'type' => 'integer',
        'rules' => 'nullable|integer|min:0',
        'default_value' => 100,
        'description' => 'Maximum number of products (0 = unlimited)',
    ],
    // ...
],
```

### 2. Controller

**File:** `app/Http/Controllers/API/Subscription/SubscriptionPlanController.php`

**Key Methods:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `getList` | GET /subscription-plan | List all plans |
| `getOne` | GET /subscription-plan/{id} | Get single plan |
| `create` | POST /subscription-plan | Create new plan |
| `update` | PUT /subscription-plan/{id} | Update existing plan |
| `getLimitFormats` | GET /subscription-plan/limitFormats | Get config for dynamic form |

**getLimitFormats Response:**

```json
{
    "formats": [...],  // Flat array of all limit formats
    "grouped": {       // Grouped by tab
        "Product Limits": [...],
        "User Limits": [...],
        "Feature Toggles": [...]
    },
    "tabs": ["Product Limits", "User Limits", "Feature Toggles"]
}
```

### 3. Request Validation

**File:** `app/Http/Requests/API/Subscription/SubscriptionPlanRequest.php`

Validates incoming plan data including:

```php
public function rules(): array
{
    return [
        'name' => 'required|string|max:255',
        'slug' => 'required|string|max:255',
        'price' => 'required|integer|min:0',
        'billing_cycle' => 'required|in:monthly,yearly',
        'is_active' => 'boolean',
        'trial_days' => 'nullable|integer|min:0',
        'limits' => 'nullable|array',
        'limits.*' => 'nullable',
        'features' => 'nullable|array',
        'metadata' => 'nullable|array',
    ];
}
```

### 4. Resource

**File:** `app/Http/Resources/Subscription/SubscriptionPlanResource.php`

Transforms the model for API responses:

```php
public function toArray($request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'slug' => $this->slug,
        'description' => $this->description,
        'price' => $this->price,
        'formatted_price' => $this->formatted_price,
        'billing_cycle' => $this->billing_cycle,
        'trial_days' => $this->trial_days,
        'has_trial' => $this->has_trial,
        'is_active' => $this->is_active,
        'limits' => $this->limits ?? [],
        'features' => $this->features,
        'metadata' => $this->metadata,
        'active_subscriptions_count' => $this->subscriptions_count ?? 0,
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

## Frontend Components

### 1. Schema Definition

**File:** `packages/dash-admin/src/schemas/subscriptionPlan.ts`

Defines form fields organized into tabs:

| Tab | Fields |
|-----|--------|
| Basic Info | name, slug, description, is_active |
| Pricing | price, formatted_price, billing_cycle, trial_days, has_trial |
| Limits | Dynamic limits via PlanLimitsSettings |
| Features | Feature toggles array |
| Metadata | JSON metadata editor |
| Stats | active_subscriptions_count, created_at, updated_at |

### 2. PlanLimitsSettings Component

**File:** `packages/dash-admin/src/components/subscription/PlanLimitsSettings.tsx`

A dynamic form component that:

1. Fetches limit formats from backend via SystemRequestsCache
2. Groups limits by tab
3. Renders appropriate input components (switch for boolean, number for integer)
4. Handles create, edit, and view modes

**Usage:**

```tsx
// In schema
{
    tab: 'Limits',
    attribute: 'limits',
    label: 'Plan Limits',
    type: Object,
    custom: true,
    component: PlanLimitsSettings,
}
```

**Component Structure:**

```tsx
// Different components for different modes
export const PlanLimitsSettingsEdit = ({ record, source }) => { ... }
export const PlanLimitsSettingsCreate = ({ record, source }) => { ... }
export const PlanLimitsSettingsView = ({ record, source }) => { ... }

// Main component that switches based on mode
const PlanLimitsSettings = ({ method, ...props }) => {
    switch (method) {
        case 'create': return <PlanLimitsSettingsCreate {...props} />;
        case 'edit': return <PlanLimitsSettingsEdit {...props} />;
        default: return <PlanLimitsSettingsView {...props} />;
    }
};
```

### 3. Resource Configuration

**File:** `packages/dash-admin/src/systemResources.tsx`

```tsx
{
    roles: ['System'],
    model: 'system/subscription-plan',
    component: ResourceTemplate,
    label: 'Subscription Plans',
    icon: <CardMembershipIcon />,
    schema: subscriptionPlanSchema,
    
    // Context provider for fetching limit formats
    contextComponent: ({ children }) => (
        <SystemRequestsCache requests={[
            { key: 'limitFormats', url: '/system/subscription-plan/limitFormats' }
        ]}>
            {children}
        </SystemRequestsCache>
    ),
    
    // Clean up limits object before sending
    postFormatter: (data) => {
        if (data.limits && typeof data.limits === 'object') {
            const cleanLimits = {};
            Object.keys(data.limits).forEach(key => {
                if (data.limits[key] !== undefined && data.limits[key] !== '') {
                    cleanLimits[key] = data.limits[key];
                }
            });
            data.limits = cleanLimits;
        }
        return data;
    },
    
    create: true,
    edit: true,
    view: true,
    delete: true,
}
```

## Data Model

### SubscriptionPlan Model

**Table:** `subscription_plans`

| Column | Type | Description |
|--------|------|-------------|
| id | bigint | Primary key |
| name | varchar(255) | Plan display name |
| slug | varchar(255) | URL identifier |
| description | text | Plan description |
| price | integer | Price in cents |
| billing_cycle | enum | 'monthly' or 'yearly' |
| trial_days | integer | Trial period days |
| is_active | boolean | Availability flag |
| limits | json | Plan limits object |
| features | json | Enabled features array |
| metadata | json | Additional metadata |
| created_at | timestamp | Creation timestamp |
| updated_at | timestamp | Last update |

### Limits JSON Structure

```json
{
    "max_products": 100,
    "max_categories": 20,
    "max_users": 5,
    "max_locations": 3,
    "max_media_storage_mb": 500,
    "analytics_enabled": true,
    "api_access_enabled": false,
    "custom_reports_enabled": true,
    "push_notifications_enabled": true,
    "max_sms_per_month": 1000
}
```

## API Routes

**File:** `routes/system.php`

```php
Route::prefix('subscription-plan')->name('subscription-plan.')->group(function () {
    $class = SubscriptionPlanController::class;
    
    // Standard CRUD routes
    Route::get('/', [$class, 'getList'])->name('getList');
    Route::post('/', [$class, 'create'])->name('create');
    Route::get('/{id}', [$class, 'getOne'])->name('getOne');
    Route::put('/{id}', [$class, 'update'])->name('update');
    Route::delete('/{id}', [$class, 'delete'])->name('delete');
    
    // Custom route for limit formats
    Route::get('/limitFormats', [$class, 'getLimitFormats'])->name('limitFormats');
});
```

## Usage Examples

### Creating a Plan

```http
POST /api/system/subscription-plan
Content-Type: application/json
Authorization: Bearer {token}

{
    "name": "Professional",
    "slug": "professional",
    "description": "Best for growing businesses",
    "price": 29900,
    "billing_cycle": "monthly",
    "trial_days": 14,
    "is_active": true,
    "limits": {
        "max_products": 500,
        "max_users": 10,
        "max_locations": 5,
        "analytics_enabled": true,
        "api_access_enabled": true
    },
    "features": ["analytics", "api-access", "custom-reports"]
}
```

### Updating Plan Limits

```http
PUT /api/system/subscription-plan/1
Content-Type: application/json
Authorization: Bearer {token}

{
    "limits": {
        "max_products": 1000,
        "max_users": 20
    }
}
```

## Checking Plan Limits (Service Usage)

Other parts of the application can check plan limits using:

```php
// In a service or controller
$tenant = auth()->user()->tenant;
$subscription = $tenant->activeSubscription;
$plan = $subscription->plan;

// Check a specific limit
$maxProducts = $plan->limits['max_products'] ?? 0;
$currentProducts = $tenant->products()->count();

if ($maxProducts > 0 && $currentProducts >= $maxProducts) {
    throw new PlanLimitExceededException('Product limit reached');
}

// Check a feature toggle
if (!($plan->limits['api_access_enabled'] ?? false)) {
    throw new FeatureNotAvailableException('API access not available on your plan');
}
```

## Default Plans

The config includes default plan templates:

| Plan | Price | Key Limits |
|------|-------|------------|
| Free Trial | $0 | 10 products, 1 user, basic features |
| Basic | $9.99/mo | 50 products, 3 users, standard features |
| Professional | $29.99/mo | 500 products, 10 users, advanced features |
| Enterprise | Custom | Unlimited, all features |

## Extending Limits

To add new plan limits:

1. **Update config:**
   ```php
   // config/subscription_plans.php
   'limit_formats' => [
       // ... existing limits
       [
           'id' => 'new_limit',
           'group' => 'custom',
           'tab' => 'Custom Limits',
           'attribute' => 'new_limit_key',
           'label' => 'New Limit',
           'type' => 'integer',
           'rules' => 'nullable|integer|min:0',
           'default_value' => 10,
           'description' => 'Description of the new limit',
       ],
   ],
   ```

2. **Clear config cache:**
   ```bash
   php artisan config:clear
   ```

3. **Frontend updates automatically** - The PlanLimitsSettings component fetches limits dynamically from the backend.

## Related Documentation

- [Tenancy & Billing System](./tenancy_billing_system.md)
- [Tenant Settings](./tenant_settings.md)
- [System Admin Dashboard](./system_admin.md)
