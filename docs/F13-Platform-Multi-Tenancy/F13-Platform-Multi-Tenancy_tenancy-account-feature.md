
# Tenancy Account Feature Documentation

## Overview

The **Tenancy Account** feature introduces a higher-level abstraction (`Tenancy` model) above existing `Tenant` models to manage billing, subscriptions, and multiple restaurant instances. This allows:

- **Multi-tenant billing**: One subscription covers multiple restaurants
- **Centralized management**: TenancyAdmin role to manage all restaurants under an account
- **Flexible payment processing**: Plugin-based payment gateway architecture
- **Trial periods and subscription lifecycle**: Complete automation from trial → active → suspended → deleted

## Database Architecture

### Core Tables

#### `tenancies`
Primary table managing tenancy accounts.

**Columns:**
- `id` (UUID7) - Primary key
- `public_name` - Display name ("Joe's Restaurants")
- `legal_name` - Legal entity name  
- `public_id` - Business registration number (RUT, Tax ID)
- `email` - Business email
- `url` - Business website (optional)
- `slug` - URL-friendly identifier
- `status` - Enum: trial, active, suspended, cancelled, deleted
- `trial_ends_at` - Trial period end date
- `suspended_at` - Suspension timestamp  
- `marked_for_deletion_at` - Deletion scheduling
- `settings` (JSON) - Configurable settings
- `metadata` (JSON) - Additional attributes

#### `system_payment_gateways`
Available payment gateway integrations (like `system_marketplaces`).

**Columns:**
- `id` - Primary key
- `name` - Gateway name ("Internal", "Stripe", "PayPal")
- `class` - Service class implementing `PaymentGatewayInterface`
- `icon_path` - Gateway logo
- `region` - Regional availability (optional)
- `is_active` - Enable/disable gateway

#### `tenancy_system_payment_gateways` (Pivot)
Associates tenancies with available payment gateways.

#### `tenancy_subscriptions`
Subscription records linked to Tenancy (not User).

**Columns:**
- `tenancy_id` - FK to tenancies
- `subscription_plan_id` - FK to subscription_plans
- `status` - trial, active, past_due, cancelled, expired
- `trial_ends_at`, `current_period_start`, `current_period_end`
- `external_subscription_id` - Gateway-specific ID
- `metadata` (JSON)

#### `tenancy_payment_methods`
Payment methods per tenancy-gateway association.

#### `tenancy_payments`
Payment transaction records.

#### `tenancy_users` (Pivot)
Associates users with tenancies and their role (owner, admin, member).

## Role Hierarchy

### Updated Levels
- **System Admin** (level 0) - Full system access
- **TenancyAdmin** (level 1) - **NEW** - Manages entire tenancy account
- **Tenant** (level 2) - Manages single restaurant (unchanged behavior)
- **User** (level 3) - Standard user access

## Models

### `App\Models\Tenancy`

**Key Methods:**
```php
// Settings/Attributes (config-driven)
$tenancy->setting('billing_email');
$tenancy->attribute('industry');
$tenancy->setSetting('auto_pay_enabled', false);

// Relationships
$tenancy->tenants();                  // HasMany Tenant
$tenancy->users();                    // HasMany User
$tenancy->subscriptions();            // HasMany TenancySubscription
$tenancy->currentSubscription();      // Get active subscription
$tenancy->systemPaymentGateways();    // BelongsToMany
$tenancy->paymentMethods();           // HasManyThrough

// State Management
$tenancy->isInTrial();
$tenancy->isActive();
$tenancy->suspend();
$tenancy->reactivate();
$tenancy->markForDeletion();
```

### `App\Models\TenancySubscription`

**Key Methods:**
```php
$subscription->isActive();
$subscription->isOnTrial();
$subscription->daysUntilExpiry();
$subscription->cancel();
$subscription->renew();
$subscription->markPastDue();
```

### `App\Models\SystemPaymentGateway`

**Key Methods:**
```php
$gateway->getServiceInstance();  // Returns PaymentGatewayInterface implementation
SystemPaymentGateway::getAvailableClasses();
```

### `App\Models\PaymentMethod`

**Key Methods:**
```php
$paymentMethod->setAsDefault();
$paymentMethod->deactivate();
```

### `App\Models\TenancyPayment`

**Key Methods:**
```php
$payment->markAsSucceeded();
$payment->markAsFailed($reason);
$payment->markAsRefunded();
```

## Payment Gateway Architecture

### Interface: `Domain\App\Services\Payments\PaymentGatewayInterface`

All payment gateways must implement:
```php
createPaymentMethod(array $data): array
charge(string $paymentMethodId, float $amount, string $currency): array
refund(string $transactionId, float $amount): array
getPaymentMethod(string $paymentMethodId): ?array
deletePaymentMethod(string $paymentMethodId): bool
```

### Internal Gateway (Default)

`Domain\App\Services\Payments\Internal\InternalPaymentGatewayService`

- 90% simulated success rate for charges
- No external API calls
- Perfect for testing and demos

**Usage:**
```php
$gateway = SystemPaymentGateway::where('name', 'Internal')->first();
$service = $gateway->getServiceInstance();

$result = $service->charge('pm_internal_123', 99.99, 'USD');
// Returns: ['status' => 'succeeded', 'transaction_id' => '...']
```

## Configuration

### `config/tenancies.php`

Defines settings and attributes for the Tenancy model.

**Structure:**
```php
return [
    'setting_formats' => [
        [
            'id' => 'billing_email',
            'type' => 'string',
            'rules' => 'nullable|email',
            'default_value' => null,
            // ...
        ],
    ],
    'attribute_formats' => [ /* ... */ ],
];
```

## Migrations

All 11 migrations completed:
1. `create_tenancies_table`
2. `create_system_payment_gateways_table`
3. `create_tenancy_system_payment_gateways_table`
4. `create_tenancy_subscriptions_table`
5. `create_tenancy_payment_methods_table`
6. `create_tenancy_payments_table`
7. `create_tenancy_users_table`
8. `add_tenancy_id_to_tenants_table`
9. `add_tenancy_id_to_users_table`
10. `add_limits_to_subscription_plans_table`
11. `create_tenancy_admin_role_and_update_levels`

**Run migrations:**
```bash
./vendor/bin/sail artisan migrate --force
```

## Seeders

### `SystemPaymentGatewaysSeeder`

Seeds the Internal payment gateway.

**Run seeder:**
```bash
./vendor/bin/sail artisan db:seed --class=SystemPaymentGatewaysSeeder --force
```

## Usage Examples

### Creating a Tenancy

```php
use App\Models\Tenancy;
use App\Models\SystemPaymentGateway;
use App\Models\TenancySystemPaymentGateway;

$tenancy = Tenancy::create([
    'public_name' => "Joe's Restaurant Group",
    'legal_name' => "Joe's Restaurants LLC",
    'public_id' => '12345678-9',
    'email' => 'joe@joes-restaurants.com',
    'slug' => 'joes-restaurant-group',
    'status' => 'trial',
    'trial_ends_at' => now()->addMonth(),
]);

// Assign internal payment gateway
$internalGateway = SystemPaymentGateway::where('name', 'Internal')->first();
$tenancy->systemPaymentGateways()->attach($internalGateway->id);
```

### Checking Subscription Limits

```php
$subscription = $tenancy->currentSubscription();
$plan = $subscription->subscriptionPlan;
$limits = $plan->limits;

$maxTenants = $limits['max_tenants']; // e.g., 3
$currentTenants = $tenancy->tenants()->count();

if ($currentTenants >= $maxTenants) {
    throw new \Exception("Tenant limit reached");
}
```

### Processing a Payment

```php
use App\Models\TenancyPayment;

$tenancySubscription = $tenancy->currentSubscription();
$paymentMethod = $tenancy->paymentMethods()->where('is_default', true)->first();

$gateway = $paymentMethod->tenancySystemPaymentGateway->systemPaymentGateway;
$service = $gateway->getServiceInstance();

$result = $service->charge(
    $paymentMethod->provider_payment_method_id,
    $tenancySubscription->subscriptionPlan->price,
    'USD'
);

$payment = TenancyPayment::create([
    'tenancy_subscription_id' => $tenancySubscription->id,
    'tenancy_payment_method_id' => $paymentMethod->id,
    'payment_gateway' => $gateway->name,
    'transaction_id' => $result['transaction_id'],
    'amount' => $result['amount'],
    'currency' => 'USD',
    'status' => $result['status'],
]);

if ($result['status'] === 'succeeded') {
    $tenancySubscription->renew();
} else {
    $tenancySubscription->markPastDue();
}
```

## Testing

### Unit Tests (TODO)
- Tenancy model tests
- TenancySubscription model tests  
- Payment gateway tests
- Role hierarchy tests

### Feature Tests (TODO)
- Tenancy CRUD operations
- Subscription lifecycle
- Payment processing flows
- Limit enforcement

## Next Steps

1. **Update existing models**: Add `tenancy()` relationship to `Tenant` and `User` models
2. **Create controllers**: TenancyController, TenancySubscriptionController, etc.
3. **Add services**: TenancyProvisioningService, LimitEnforcementService
4. **Write tests**: Comprehensive test coverage
5. **Create API endpoints**: RESTful API for tenancy management
6. **Build frontend**: React Admin CRUD for tenancies

## Support

For questions or issues, contact the development team or refer to the technical requirements document.
