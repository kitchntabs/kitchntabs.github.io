# DASH Tenancy & Billing System - Technical Documentation

> **Version:** 1.0  
> **Last Updated:** January 2026  
> **Audience:** Developers, AI Agents, System Architects

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Data Models](#3-data-models)
4. [Services](#4-services)
5. [Controllers & API Endpoints](#5-controllers--api-endpoints)
6. [Payment Gateway Contract](#6-payment-gateway-contract)
7. [Subscription Lifecycle](#7-subscription-lifecycle)
8. [Plan Limits & Enforcement](#8-plan-limits--enforcement)
9. [Webhook Handling](#9-webhook-handling)
10. [Testing](#10-testing)
11. [Extension Guide](#11-extension-guide)

---

## 1. Overview

The DASH Tenancy & Billing System provides multi-tenant infrastructure with subscription-based billing. It enables:

- **Multi-tenancy**: Isolated tenant environments with configurable settings
- **Subscription Plans**: Tiered plans with limits and features
- **Payment Processing**: Extensible payment gateway contract
- **Usage Enforcement**: Plan-based limits on resources

### Key Design Principles

| Principle | Implementation |
|-----------|----------------|
| Extensibility | PaymentGatewayContract interface for new gateways |
| Isolation | Each tenancy has isolated data and settings |
| Flexibility | JSON-based limits and metadata for dynamic configuration |
| Robustness | Payment retry logic, webhook handling, audit trails |

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TENANCY & BILLING ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Controllers   │────▶│    Services     │────▶│     Models      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ TenancyController│    │ TenancyService  │     │    Tenancy      │
│ TenancySubscription│  │ TenancySubscription│  │ TenancySubscription│
│   Controller    │     │   Service       │     │ SubscriptionPlan│
│ TenancyPayment  │     │                 │     │ TenancyPayment  │
│   Controller    │     │                 │     │ TenancyPaymentMethod│
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ PaymentGateway      │
                    │    Contract         │
                    ├─────────────────────┤
                    │ InternalGateway     │
                    │ (future) Stripe     │
                    │ (future) PayPal     │
                    └─────────────────────┘
```

### Directory Structure

```
app/
├── Models/
│   ├── Tenancy.php
│   ├── TenancySubscription.php
│   ├── TenancyPayment.php
│   ├── TenancyPaymentMethod.php
│   ├── TenancySystemPaymentGateway.php
│   ├── SystemPaymentGateway.php
│   └── Subscription/
│       └── SubscriptionPlan.php
├── Services/
│   └── Tenancy/
│       ├── TenancyService.php
│       └── TenancySubscriptionService.php
├── Http/
│   └── Controllers/
│       └── API/
│           ├── Tenancy/
│           │   ├── TenancyController.php
│           │   ├── TenancySubscriptionController.php
│           │   ├── TenancyPaymentController.php
│           │   ├── TenancyPaymentMethodController.php
│           │   └── TenancyUserController.php
│           └── Webhooks/
│               └── PaymentWebhookController.php
└── Policies/
    └── TenancyPolicy.php

domain/app/Services/Payments/
├── Contracts/
│   └── PaymentGatewayContract.php
├── Internal/
│   └── InternalPaymentGatewayService.php
├── Rebill/
│   └── RebillPaymentGatewayService.php
└── Flow/
    └── FlowPaymentGatewayService.php
```

### Payment Gateway Association

During tenancy provisioning, all active system payment gateways are automatically associated with the new tenancy. This allows tenancies to use any of the available payment gateways.

**Current Behavior:** All active gateways are associated regardless of country/currency.

**Future Enhancement:** Gateway filtering based on:
- `tenancy.primary_currency` vs gateway `supported_currencies`
- Tenancy country vs gateway `supported_countries`

**Manual Association (existing tenancies):**
```bash
sail artisan tenancy:associate-gateways
sail artisan tenancy:associate-gateways --tenancy=<uuid>
sail artisan tenancy:associate-gateways --dry-run
```

---

## 3. Data Models

### 3.1 Tenancy

The core tenant entity representing an organization or account.

**Table:** `tenancies`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | Primary key (UUIDv7) |
| `public_name` | string | Display name |
| `legal_name` | string | Legal/business name |
| `public_id` | string | Unique public identifier |
| `email` | string | Contact email |
| `url` | string | Business website URL |
| `slug` | string | URL-safe identifier |
| `status` | enum | active, suspended, trial, cancelled, deleted |
| `primary_language` | string | Business primary language (es, en) |
| `primary_currency` | string | Business primary currency code |
| `primary_timezone` | string | Business primary timezone |
| `trial_ends_at` | datetime | Trial expiration |
| `suspended_at` | datetime | When suspended |
| `marked_for_deletion_at` | datetime | Scheduled deletion |
| `settings` | json | Tenant configuration |
| `metadata` | json | Additional metadata |

**Key Methods:**

```php
// Check trial status
$tenancy->isOnTrial(): bool
$tenancy->trialDaysRemaining(): int
$tenancy->trialExpiringSoon(int $days = 7): bool

// Status checks
$tenancy->isActive(): bool
$tenancy->isSuspended(): bool

// Settings helper
$tenancy->setting(string $key, $default = null): mixed
```

**Relationships:**

```php
$tenancy->users()              // HasMany User
$tenancy->subscriptions()      // HasMany TenancySubscription
$tenancy->activeSubscription() // HasOne TenancySubscription (current)
$tenancy->paymentMethods()     // HasMany TenancyPaymentMethod
$tenancy->payments()           // HasMany TenancyPayment
$tenancy->systemPaymentGateways() // BelongsToMany SystemPaymentGateway
```

---

### 3.2 TenancySubscription

Represents a subscription period for a tenancy.

**Table:** `tenancy_subscriptions`

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | Primary key |
| `tenancy_id` | uuid | FK to tenancies |
| `subscription_plan_id` | bigint | FK to subscription_plans |
| `status` | enum | trial, active, past_due, cancelled |
| `trial_ends_at` | datetime | Trial end |
| `current_period_start` | datetime | Billing period start |
| `current_period_end` | datetime | Billing period end |
| `cancelled_at` | datetime | When cancelled |
| `external_subscription_id` | string | Gateway subscription ID |
| `payment_gateway` | string | Gateway identifier |
| `failed_payment_attempts` | int | Retry counter |
| `last_payment_attempt_at` | datetime | Last charge attempt |
| `next_payment_attempt_at` | datetime | Next retry scheduled |
| `metadata` | json | Additional data |

**Status Transitions:**

```
trial ──▶ active (payment success)
      ──▶ cancelled (trial expired without payment)

active ──▶ past_due (payment failed)
       ──▶ cancelled (user cancellation)

past_due ──▶ active (retry success)
         ──▶ suspended (max retries exceeded)
```

---

### 3.3 SubscriptionPlan

Defines available subscription tiers.

**Table:** `subscription_plans`

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | Primary key |
| `name` | string | Plan display name |
| `slug` | string | URL-safe identifier |
| `description` | string | Plan description |
| `prices` | json | Price map by currency code (e.g. {"CLP": 2990, "USD": 5}) |
| `billing_cycle` | enum | monthly, yearly |
| `trial_days` | int | Trial period length |
| `features` | json | Feature list |
| `limits` | json | Resource limits |
| `is_active` | bool | Available for purchase |
| `metadata` | json | Additional config |
| `flow_plan_id` | string | External ID for Flow gateway |
| `rebill_plan_id` | string | External ID for Rebill gateway |

### Pricing Structure

Prices are stored in the `prices` JSON column, allowing different price points per currency.

```json
{
    "CLP": 2990,
    "USD": 500,
    "EUR": 450
}
```

The system will attempt to find the price matching the tenancy's `primary_currency`. If not found, it may fall back to the base `price` or default currency.

**Gateway Sync:**
When syncing to gateways (Flow, Rebill), the system uses the currency-specific price if available. For example, Flow plans will use the `CLP` price from the array.

**Limits Structure:**

```json
{
    "max_tenants": 3,
    "max_users_per_tenant": 10,
    "max_products_per_tenant": 500,
    "max_orders_per_month": null,
    "features": {
        "marketplace_integrations": true,
        "custom_point_of_sales": true,
        "api_access": true,
        "priority_support": false
    }
}
```

**Key Methods:**

```php
$plan->getLimit(string $key, $default = null): mixed
$plan->hasFeature(string $feature): bool
$plan->getAllLimits(): array
$plan->isWithinLimit(string $key, int $currentUsage): bool
$plan->canUpgradeFrom(SubscriptionPlan $other): bool
$plan->canDowngradeFrom(SubscriptionPlan $other): bool
$plan->getPriceForCurrency(string $currency): ?int
$plan->getFormattedPriceForCurrency(string $currency): string
```

---

### 3.4 TenancyPaymentMethod

Stored payment methods for a tenancy.

**Table:** `tenancy_payment_methods`

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | Primary key |
| `tenancy_id` | uuid | FK to tenancies |
| `tenancy_system_payment_gateway_id` | bigint | FK to gateway config |
| `provider_payment_method_id` | string | External ID (pm_xxx) |
| `type` | string | card, bank_transfer, etc |
| `last_four` | string | Last 4 digits |
| `brand` | string | Card brand |
| `is_default` | bool | Default payment method |
| `expires_at` | datetime | Expiration date |
| `metadata` | json | Additional data |

---

### 3.5 TenancyPayment

Payment transaction records.

**Table:** `tenancy_payments`

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | Primary key |
| `tenancy_id` | uuid | FK to tenancies |
| `tenancy_subscription_id` | bigint | FK to subscription |
| `tenancy_payment_method_id` | bigint | FK to payment method |
| `amount` | int | Amount in cents |
| `currency` | string | Currency code |
| `status` | enum | pending, succeeded, failed, refunded |
| `provider_transaction_id` | string | External transaction ID |
| `provider_response` | json | Raw gateway response |
| `refunded_amount` | int | Partial/full refund |
| `metadata` | json | Additional data |

---

## 4. Services

### 4.1 TenancyService

**Location:** `app/Services/Tenancy/TenancyService.php`

Handles tenancy lifecycle operations.

```php
class TenancyService
{
    // Create new tenancy with optional subscription
    public function createTenancy(array $data, ?SubscriptionPlan $plan = null): Tenancy
    
    // Suspend tenancy (payment issues, policy violation)
    public function suspendTenancy(Tenancy $tenancy, string $reason): void
    
    // Reactivate suspended tenancy
    public function reactivateTenancy(Tenancy $tenancy): void
    
    // Get usage statistics for limit enforcement
    public function getUsageStats(Tenancy $tenancy): array
    
    // Attach default payment gateway
    public function attachDefaultPaymentGateway(Tenancy $tenancy): void
}
```

**Usage Example:**

```php
$service = app(TenancyService::class);

// Create tenancy with trial
$tenancy = $service->createTenancy([
    'public_name' => 'My Restaurant',
    'email' => 'contact@myrestaurant.com',
], $starterPlan);

// Get usage for limit check
$usage = $service->getUsageStats($tenancy);
// Returns: ['users_count' => 3, 'products_count' => 150, ...]
```

---

### 4.2 TenancySubscriptionService

**Location:** `app/Services/Tenancy/TenancySubscriptionService.php`

Manages subscription operations.

```php
class TenancySubscriptionService
{
    // Create new subscription
    public function createSubscription(
        Tenancy $tenancy,
        SubscriptionPlan $plan,
        bool $startTrial = true
    ): TenancySubscription
    
    // Upgrade to higher plan
    public function upgradePlan(
        TenancySubscription $subscription,
        SubscriptionPlan $newPlan
    ): TenancySubscription
    
    // Downgrade with usage validation
    public function downgradePlan(
        TenancySubscription $subscription,
        SubscriptionPlan $newPlan
    ): TenancySubscription
    
    // Cancel subscription
    public function cancelSubscription(
        TenancySubscription $subscription,
        bool $atPeriodEnd = true
    ): TenancySubscription
    
    // Renew subscription for next period
    public function renewSubscription(
        TenancySubscription $subscription
    ): TenancySubscription
    
    // Validate downgrade is allowed
    public function validateDowngrade(
        TenancySubscription $subscription,
        SubscriptionPlan $newPlan
    ): array
}
```

**Downgrade Validation:**

```php
$result = $service->validateDowngrade($subscription, $lowerPlan);

// Returns:
[
    'allowed' => false,
    'conflicts' => [
        'users_count' => [
            'current' => 15,
            'limit' => 10,
            'over' => 5,
            'message' => 'You need to remove 5 users before downgrading'
        ]
    ]
]
```

---

## 5. Controllers & API Endpoints

### 5.1 TenancyController

**Location:** `app/Http/Controllers/API/Tenancy/TenancyController.php`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tenancy/tenancy` | List tenancies |
| GET | `/api/tenancy/tenancy/{id}` | Get tenancy details |
| POST | `/api/tenancy/tenancy` | Create tenancy |
| PUT | `/api/tenancy/tenancy/{id}` | Update tenancy |
| DELETE | `/api/tenancy/tenancy/{id}` | Soft delete tenancy |
| GET | `/api/tenancy/tenancy/{id}/usage-stats` | Get usage statistics |
| POST | `/api/tenancy/tenancy/{id}/suspend` | Suspend tenancy |
| POST | `/api/tenancy/tenancy/{id}/reactivate` | Reactivate tenancy |

---

### 5.2 TenancySubscriptionController

**Location:** `app/Http/Controllers/API/Tenancy/TenancySubscriptionController.php`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tenancy/subscriptions` | List subscriptions |
| GET | `/api/tenancy/subscriptions/{id}` | Get subscription details |
| POST | `/api/tenancy/subscriptions` | Create subscription |
| POST | `/api/tenancy/subscriptions/{id}/upgrade` | Upgrade plan |
| POST | `/api/tenancy/subscriptions/{id}/downgrade` | Downgrade plan |
| POST | `/api/tenancy/subscriptions/{id}/cancel` | Cancel subscription |
| POST | `/api/tenancy/subscriptions/{id}/resume` | Resume cancelled |
| POST | `/api/tenancy/subscriptions/{id}/renew` | Force renewal |

---

### 5.3 TenancyPaymentMethodController

**Location:** `app/Http/Controllers/API/Tenancy/TenancyPaymentMethodController.php`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tenancy/payment-methods` | List payment methods |
| POST | `/api/tenancy/payment-methods` | Add payment method |
| DELETE | `/api/tenancy/payment-methods/{id}` | Remove payment method |
| POST | `/api/tenancy/payment-methods/{id}/default` | Set as default |

---

### 5.4 PaymentWebhookController

**Location:** `app/Http/Controllers/API/Webhooks/PaymentWebhookController.php`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/webhooks/internal` | Internal gateway webhooks |
| POST | `/api/payments/webhooks/internal/simulate` | Simulate events (non-prod) |
| GET | `/api/payments/webhooks/info` | Get endpoint info |

---

## 6. Payment Gateway Contract

### 6.1 Interface Definition

**Location:** `domain/app/Services/Payments/Contracts/PaymentGatewayContract.php`

The contract defines the standard interface for all payment gateways:

```php
interface PaymentGatewayContract
{
    // Configuration
    public function __construct(?TenancySystemPaymentGateway $gatewayConfig = null);
    public static function getIdentifier(): string;
    public static function getDisplayName(): string;
    public static function getCapabilities(): array;
    public static function getConnectionParamFormats(): array;
    public function verifyCredentials(): bool;
    
    // Payment Methods
    public function createPaymentMethod(array $data): array;
    public function getPaymentMethod(string $externalId): ?array;
    public function updatePaymentMethod(string $externalId, array $data): array;
    public function deletePaymentMethod(string $externalId): bool;
    
    // Subscriptions
    public function createSubscription(
        TenancySubscription $subscription,
        TenancyPaymentMethod $paymentMethod
    ): array;
    public function updateSubscription(TenancySubscription $subscription, array $changes): array;
    public function cancelSubscription(TenancySubscription $subscription, bool $atPeriodEnd = true): array;
    public function resumeSubscription(TenancySubscription $subscription): array;
    
    // Charges
    public function charge(
        string $paymentMethodId,
        int $amountInCents,
        string $currency,
        array $metadata = []
    ): array;
    public function refund(string $transactionId, ?int $amountInCents = null, string $reason = ''): array;
    
    // Webhooks
    public function validateWebhookSignature(string $payload, string $signature): bool;
    public function handleWebhook(string $eventType, array $payload): array;
    public static function getWebhookEndpoint(): string;
    
    // Invoices
    public function getInvoice(string $invoiceId): ?array;
    public function listInvoices(TenancySubscription $subscription, int $limit = 10): array;
    public function getInvoiceUrl(string $invoiceId): ?string;
}
```

---

### 6.2 InternalPaymentGatewayService

**Location:** `domain/app/Services/Payments/Internal/InternalPaymentGatewayService.php`

A simulation gateway for development and demo purposes.

**Capabilities:**

```php
[
    'supports_subscriptions' => true,
    'supports_trials' => true,
    'supports_proration' => false,
    'supports_refunds' => true,
    'supports_partial_refunds' => false,
    'supports_webhooks' => true,
    'supports_invoices' => true,
    'is_simulation' => true,
]
```

**Configuration:**

```php
// Adjust success rate for testing
$gateway = new InternalPaymentGatewayService($config);
$gateway->setSuccessRate(100); // 100% success
$gateway->setSuccessRate(0);   // 100% failure
```

**Usage:**

```php
$gateway = new InternalPaymentGatewayService();

// Create payment method
$result = $gateway->createPaymentMethod([
    'last4' => '4242',
    'brand' => 'Visa',
]);
// Returns: ['success' => true, 'payment_method' => ['id' => 'pm_internal_xxx', ...]]

// Charge
$result = $gateway->charge('pm_internal_xxx', 2900, 'USD', ['order_id' => 123]);
// Returns: ['success' => true, 'transaction_id' => 'txn_internal_xxx', ...]

// Handle webhook
$result = $gateway->handleWebhook('payment.succeeded', ['subscription_id' => 'sub_xxx']);
```

---

### 6.3 Implementing a New Gateway

To add a new payment gateway (e.g., Stripe):

```php
namespace Domain\App\Services\Payments\Stripe;

use Domain\App\Services\Payments\Contracts\PaymentGatewayContract;

class StripePaymentGatewayService implements PaymentGatewayContract
{
    protected \Stripe\StripeClient $stripe;
    
    public function __construct(?TenancySystemPaymentGateway $config = null)
    {
        $this->stripe = new \Stripe\StripeClient(
            $config?->connection_params['api_key'] ?? config('services.stripe.secret')
        );
    }
    
    public static function getIdentifier(): string
    {
        return 'stripe';
    }
    
    public function createPaymentMethod(array $data): array
    {
        $paymentMethod = $this->stripe->paymentMethods->attach(
            $data['payment_method_id'],
            ['customer' => $data['customer_id']]
        );
        
        return [
            'success' => true,
            'payment_method' => [
                'id' => $paymentMethod->id,
                'last4' => $paymentMethod->card->last4,
                'brand' => $paymentMethod->card->brand,
            ],
        ];
    }
    
    // Implement all other contract methods...
}
```

Then register in `SystemPaymentGateway::getAvailableClasses()`:

```php
public static function getAvailableClasses(): array
{
    return [
        \Domain\App\Services\Payments\Internal\InternalPaymentGatewayService::class,
        \Domain\App\Services\Payments\Stripe\StripePaymentGatewayService::class,
    ];
}
```

---

## 7. Subscription Lifecycle

### 7.1 New Subscription Flow

```
User Signs Up
     │
     ▼
┌─────────────┐
│ Select Plan │
└─────────────┘
     │
     ▼
┌─────────────┐    has trial?    ┌─────────────┐
│Create Tenancy│───── Yes ──────▶│ status:trial│
└─────────────┘                  └─────────────┘
     │                                  │
     │ No                               │ trial ends
     ▼                                  ▼
┌─────────────┐                  ┌─────────────┐
│Add Payment  │◀─────────────────│Prompt for   │
│  Method     │                  │  Payment    │
└─────────────┘                  └─────────────┘
     │
     ▼
┌─────────────┐
│Charge First │
│  Payment    │
└─────────────┘
     │
     ├── Success ──▶ status: active
     │
     └── Failure ──▶ Retry Logic
```

### 7.2 Renewal Flow

```php
// Scheduled job runs daily
$subscriptions = TenancySubscription::where('current_period_end', '<', now())
    ->where('status', 'active')
    ->get();

foreach ($subscriptions as $subscription) {
    $service->renewSubscription($subscription);
}
```

### 7.3 Payment Retry Flow

```
Payment Fails
     │
     ▼
Increment failed_payment_attempts
     │
     ▼
Set next_payment_attempt_at (exponential backoff)
     │
     ├── Attempt 1: +1 day
     ├── Attempt 2: +2 days
     └── Attempt 3: +4 days
     │
     ▼
attempts >= 3?
     │
     ├── No ──▶ Wait for next attempt
     │
     └── Yes ──▶ status: past_due
                      │
                      │ +7 days
                      ▼
               Suspend Tenancy
```

---

## 8. Plan Limits & Enforcement

### 8.1 Limit Types

| Limit Key | Description |
|-----------|-------------|
| `max_tenants` | Max child tenancies (for parent accounts) |
| `max_users_per_tenant` | Max users in a tenancy |
| `max_products_per_tenant` | Max products |
| `max_orders_per_month` | Monthly order cap |
| `max_storage_mb` | Storage quota |

### 8.2 Enforcement Points

**Controller Level:** Use the `HasSubscriptionLimits` trait:

```php
use App\Http\Controllers\Traits\HasSubscriptionLimits;

class ProductController extends Controller
{
    use HasSubscriptionLimits;
    
    public function store(Request $request)
    {
        $this->checkLimit('max_products_per_tenant', 'products');
        
        // Create product...
    }
}
```

**Service Level:**

```php
$plan = $tenancy->activeSubscription->subscriptionPlan;
$usage = $tenancyService->getUsageStats($tenancy);

if (!$plan->isWithinLimit('max_products_per_tenant', $usage['products_count'])) {
    throw new SubscriptionLimitExceededException('Product limit reached');
}
```

### 8.3 Downgrade Validation

```php
$service = app(TenancySubscriptionService::class);
$validation = $service->validateDowngrade($subscription, $newPlan);

if (!$validation['allowed']) {
    return response()->json([
        'error' => 'Cannot downgrade due to current usage',
        'conflicts' => $validation['conflicts'],
    ], 422);
}
```

---

## 9. Webhook Handling

### 9.1 Supported Events

| Event Type | Action |
|------------|--------|
| `payment.succeeded` | Activate subscription, reset retry counter |
| `payment.failed` | Increment retry counter, schedule next attempt |
| `subscription.created` | Sync subscription record |
| `subscription.updated` | Sync plan changes |
| `subscription.cancelled` | Mark as cancelled |
| `invoice.paid` | Record payment, extend period |
| `trial.ending` | Send notification |

### 9.2 Webhook Security

All webhooks validate signatures:

```php
// In PaymentWebhookController
$signature = $request->header('X-Webhook-Signature');
$payload = $request->getContent();

if (!$gateway->validateWebhookSignature($payload, $signature)) {
    return response()->json(['error' => 'Invalid signature'], 401);
}
```

### 9.3 Testing Webhooks

Use the simulation endpoint (non-production only):

```bash
curl -X POST http://localhost/api/payments/webhooks/internal/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "payment.failed",
    "subscription_id": "sub_internal_xxx",
    "amount": 2900
  }'
```

---

## 10. Testing

### 10.1 Test Files

| Test File | Coverage |
|-----------|----------|
| `TenancyModelTest.php` | Tenancy model operations |
| `TenancyControllerTest.php` | API endpoints |
| `TenancyServiceTest.php` | Service layer logic |
| `TenancySubscriptionServiceTest.php` | Subscription operations |
| `TenancyProvisioningIntegrationTest.php` | End-to-end flows |
| `InternalPaymentGatewayServiceTest.php` | Payment gateway |

### 10.2 Running Tests

```bash
# All tenancy-related tests
./vendor/bin/sail artisan test --filter=Tenancy

# Specific test file
./vendor/bin/sail artisan test tests/Unit/Services/TenancyServiceTest.php

# Payment gateway tests
./vendor/bin/sail artisan test --filter=InternalPaymentGateway
```

### 10.3 Test Fixtures

```php
// Create plan with limits
$plan = SubscriptionPlan::create([
    'name' => 'Test Plan',
    'slug' => 'test-plan',
    'price' => 2900,
    'billing_cycle' => 'monthly',
    'limits' => [
        'max_users_per_tenant' => 5,
        'max_products_per_tenant' => 100,
    ],
]);

// Create subscription
$subscription = TenancySubscription::create([
    'tenancy_id' => $tenancy->id,
    'subscription_plan_id' => $plan->id,
    'status' => 'active',
    'current_period_start' => now(),
    'current_period_end' => now()->addMonth(),
]);
```

---

## 11. Extension Guide

### 11.1 Adding Custom Limits

1. Add to plan limits JSON:

```json
{
    "limits": {
        "max_custom_resource": 50
    }
}
```

2. Create enforcement logic:

```php
public function checkCustomResourceLimit(Tenancy $tenancy): void
{
    $plan = $tenancy->activeSubscription->subscriptionPlan;
    $usage = CustomResource::where('tenancy_id', $tenancy->id)->count();
    
    if (!$plan->isWithinLimit('max_custom_resource', $usage)) {
        throw new SubscriptionLimitExceededException('Custom resource limit reached');
    }
}
```

### 11.2 Adding Usage Tracking

Update `TenancyService::getUsageStats()`:

```php
public function getUsageStats(Tenancy $tenancy): array
{
    return [
        'users_count' => $tenancy->users()->count(),
        'products_count' => Product::where('tenant_id', $tenancy->id)->count(),
        'custom_resources_count' => CustomResource::where('tenancy_id', $tenancy->id)->count(),
    ];
}
```

### 11.3 Custom Webhook Handlers

Extend the gateway's `handleWebhook` method:

```php
public function handleWebhook(string $eventType, array $payload): array
{
    return match($eventType) {
        'custom.event' => $this->handleCustomEvent($payload),
        default => parent::handleWebhook($eventType, $payload),
    };
}

protected function handleCustomEvent(array $payload): array
{
    // Custom logic...
    return ['handled' => true, 'action' => 'custom_action_completed'];
}
```

---

## Quick Reference

### Important Classes

| Class | Purpose |
|-------|---------|
| `TenancyService` | Tenancy lifecycle operations |
| `TenancySubscriptionService` | Subscription management |
| `PaymentGatewayContract` | Gateway interface |
| `InternalPaymentGatewayService` | Demo/test gateway |
| `SubscriptionPlan` | Plan definitions with limits |

### Key Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /api/tenancy/tenancy/{id}/usage-stats` | Current usage |
| `POST /api/tenancy/subscriptions/{id}/upgrade` | Upgrade plan |
| `POST /api/tenancy/subscriptions/{id}/downgrade` | Downgrade plan |
| `POST /api/payments/webhooks/internal` | Payment webhooks |

### Status Values

| Model | Statuses |
|-------|----------|
| Tenancy | active, trial, suspended, cancelled |
| TenancySubscription | trial, active, past_due, cancelled |
| TenancyPayment | pending, succeeded, failed, refunded |

---

*End of Documentation*
