# Laravel Cashier (Stripe) Integration Strategy

> **Purpose:** Integrate Laravel Cashier with our existing Tenancy & Billing system for seamless Stripe compatibility.

---

## Executive Summary

Our current implementation and Laravel Cashier can work together seamlessly. The key insight is that **Laravel Cashier operates at the User level** (Billable trait on User model), while **our system operates at the Tenancy level**. We can bridge these by:

1. Making `Tenancy` the billable entity (not User)
2. Using our `PaymentGatewayContract` as an abstraction layer
3. Implementing a `StripePaymentGatewayService` that wraps Cashier

---

## Architecture Comparison

| Aspect | Laravel Cashier | Our Implementation | Integration Approach |
|--------|-----------------|-------------------|---------------------|
| Billable Entity | User | Tenancy | Make Tenancy billable |
| Subscriptions | `subscriptions` table | `tenancy_subscriptions` | Map or extend |
| Payment Methods | `payment_methods` on User | `tenancy_payment_methods` | Sync via webhooks |
| Provider | Stripe only | Gateway agnostic | Cashier = one implementation |
| Webhooks | Auto-handled | Custom handling | Use Cashier handlers + custom |

---

## Integration Options

### Option A: Cashier as Primary (Recommended)

Make `Tenancy` use the `Billable` trait and leverage Cashier's full feature set.

```php
// app/Models/Tenancy.php
use Laravel\Cashier\Billable;

class Tenancy extends Model
{
    use Billable;
    
    // Cashier will add: stripe_id, pm_type, pm_last_four, trial_ends_at
}
```

**Pros:**
- Full Stripe feature support (Checkout, Portal, Tax, Invoices)
- Automatic webhook handling
- PDF invoice generation
- SCA/3D Secure support
- Tested, maintained by Laravel

**Cons:**
- Locked to Stripe
- Must adapt our subscription models to Cashier's structure

---

### Option B: Cashier Behind Our Contract (Hybrid)

Use Cashier internally but expose through our `PaymentGatewayContract`.

```php
// domain/app/Services/Payments/Stripe/StripePaymentGatewayService.php

class StripePaymentGatewayService implements PaymentGatewayContract
{
    public function createSubscription(
        TenancySubscription $subscription,
        TenancyPaymentMethod $paymentMethod
    ): array {
        $tenancy = $subscription->tenancy;
        
        // Use Cashier's fluent API
        $stripeSubscription = $tenancy
            ->newSubscription('default', $subscription->subscriptionPlan->stripe_price_id)
            ->create($paymentMethod->provider_payment_method_id);
        
        // Sync back to our model
        $subscription->update([
            'external_subscription_id' => $stripeSubscription->stripe_id,
            'payment_gateway' => 'stripe',
        ]);
        
        return [
            'success' => true,
            'external_subscription_id' => $stripeSubscription->stripe_id,
        ];
    }
}
```

**Pros:**
- Gateway-agnostic interface maintained
- Can swap providers later
- Uses our existing models and flows

**Cons:**
- More implementation work
- Must keep two systems in sync

---

## Recommended Integration: Option A with Bridge

### Step 1: Install Cashier

```bash
composer require laravel/cashier
php artisan vendor:publish --tag="cashier-migrations"
```

### Step 2: Make Tenancy Billable

```php
// app/Models/Tenancy.php
use Laravel\Cashier\Billable;

class Tenancy extends Model
{
    use Billable;

    // Override to use email as Stripe customer email
    public function stripeEmail(): ?string
    {
        return $this->email;
    }

    public function stripeName(): ?string
    {
        return $this->public_name;
    }
}
```

### Step 3: Modify Cashier Migrations

Don't add columns to `users`, add to `tenancies`:

```php
// Modify Cashier migration to target tenancies table
Schema::table('tenancies', function (Blueprint $table) {
    $table->string('stripe_id')->nullable()->index();
    $table->string('pm_type')->nullable();
    $table->string('pm_last_four', 4)->nullable();
    $table->timestamp('trial_ends_at')->nullable(); // Already exists
});
```

### Step 4: Configure Cashier Customer Model

```php
// app/Providers/AppServiceProvider.php
use Laravel\Cashier\Cashier;
use App\Models\Tenancy;

public function boot(): void
{
    Cashier::useCustomerModel(Tenancy::class);
}
```

### Step 5: Adapt Our Subscription Service

```php
// app/Services/Tenancy/TenancySubscriptionService.php

use Laravel\Cashier\Subscription as CashierSubscription;

class TenancySubscriptionService
{
    public function createSubscription(
        Tenancy $tenancy,
        SubscriptionPlan $plan,
        bool $startTrial = true
    ): TenancySubscription {
        // Use Cashier for Stripe subscription
        $builder = $tenancy->newSubscription('default', $plan->stripe_price_id);
        
        if ($startTrial && $plan->trial_days > 0) {
            $builder->trialDays($plan->trial_days);
        }
        
        // If has payment method, create immediately
        if ($tenancy->hasPaymentMethod()) {
            $stripeSubscription = $builder->create();
        } else {
            // Create for later payment collection
            $stripeSubscription = $builder->createAndSendInvoice();
        }
        
        // Sync to our TenancySubscription model
        return TenancySubscription::create([
            'tenancy_id' => $tenancy->id,
            'subscription_plan_id' => $plan->id,
            'status' => $stripeSubscription->onTrial() ? 'trial' : 'active',
            'trial_ends_at' => $stripeSubscription->trial_ends_at,
            'current_period_start' => now(),
            'current_period_end' => now()->addMonth(),
            'external_subscription_id' => $stripeSubscription->stripe_id,
            'payment_gateway' => 'stripe',
        ]);
    }
    
    public function upgradePlan(
        TenancySubscription $subscription,
        SubscriptionPlan $newPlan
    ): TenancySubscription {
        $tenancy = $subscription->tenancy;
        
        // Use Cashier's swap method
        $tenancy->subscription('default')->swap($newPlan->stripe_price_id);
        
        // Update our model
        $subscription->update([
            'subscription_plan_id' => $newPlan->id,
        ]);
        
        return $subscription->fresh();
    }
}
```

### Step 6: Add Stripe Price ID to SubscriptionPlan

```php
// Migration
Schema::table('subscription_plans', function (Blueprint $table) {
    $table->string('stripe_price_id')->nullable()->after('price');
    $table->string('stripe_product_id')->nullable()->after('stripe_price_id');
});
```

### Step 7: Leverage Cashier's Checkout for Signup

```php
// routes/web.php
Route::get('/subscribe/{plan}', function (Request $request, SubscriptionPlan $plan) {
    return $request->user()->tenancy
        ->newSubscription('default', $plan->stripe_price_id)
        ->trialDays($plan->trial_days)
        ->allowPromotionCodes()
        ->checkout([
            'success_url' => route('dashboard'),
            'cancel_url' => route('pricing'),
        ]);
});
```

### Step 8: Use Stripe Billing Portal

```php
// Let customers manage their subscription
Route::get('/billing', function (Request $request) {
    return $request->user()->tenancy->redirectToBillingPortal(route('dashboard'));
});
```

---

## Data Model Mapping

### Our Models → Cashier Tables

| Our Model | Cashier Table | Sync Strategy |
|-----------|--------------|---------------|
| `Tenancy` | `tenancies` (with Stripe columns) | Billable trait |
| `TenancySubscription` | `subscriptions` | Webhook sync |
| `TenancyPaymentMethod` | Payment methods via Stripe | API sync |
| `TenancyPayment` | Invoices via Stripe | Webhook sync |
| `SubscriptionPlan` | Stripe Products/Prices | Manual mapping |

### Webhook Sync

```php
// Listen to Cashier webhook events
// app/Listeners/StripeEventListener.php

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    public function handle(WebhookReceived $event): void
    {
        $payload = $event->payload;
        
        switch ($payload['type']) {
            case 'customer.subscription.updated':
                $this->syncSubscription($payload['data']['object']);
                break;
            case 'invoice.payment_succeeded':
                $this->recordPayment($payload['data']['object']);
                break;
        }
    }
    
    protected function syncSubscription(array $stripeSubscription): void
    {
        $subscription = TenancySubscription::where(
            'external_subscription_id', 
            $stripeSubscription['id']
        )->first();
        
        if ($subscription) {
            $subscription->update([
                'status' => $stripeSubscription['status'],
                'current_period_end' => Carbon::createFromTimestamp(
                    $stripeSubscription['current_period_end']
                ),
            ]);
        }
    }
}
```

---

## Migration Path

### Phase 1: Install & Configure (Day 1)
1. Install Cashier
2. Add Stripe columns to `tenancies` table
3. Add `stripe_price_id` to `subscription_plans`
4. Configure Cashier to use Tenancy as customer model

### Phase 2: Create Stripe Products (Day 2)
1. Create Products in Stripe Dashboard
2. Create Prices for each SubscriptionPlan
3. Update `subscription_plans` with Stripe IDs

### Phase 3: Adapt Services (Day 3-4)
1. Update TenancySubscriptionService to use Cashier
2. Add webhook event listeners
3. Test subscription flows

### Phase 4: Frontend Integration (Day 5)
1. Add Stripe.js for payment method collection
2. Implement Checkout for new subscriptions
3. Add Billing Portal link

---

## Keeping Both Systems

You can keep our `PaymentGatewayContract` while using Cashier:

```php
// StripePaymentGatewayService wraps Cashier
class StripePaymentGatewayService implements PaymentGatewayContract
{
    public static function getIdentifier(): string
    {
        return 'stripe';
    }
    
    public function charge(
        string $paymentMethodId,
        int $amountInCents,
        string $currency,
        array $metadata = []
    ): array {
        $tenancy = $this->getTenancy();
        
        try {
            $payment = $tenancy->charge($amountInCents, $paymentMethodId, [
                'currency' => $currency,
                'metadata' => $metadata,
            ]);
            
            return [
                'success' => true,
                'transaction_id' => $payment->id,
                'amount' => $amountInCents,
            ];
        } catch (IncompletePayment $e) {
            return [
                'success' => false,
                'requires_action' => true,
                'payment_intent_id' => $e->payment->id,
                'client_secret' => $e->payment->clientSecret(),
            ];
        }
    }
}
```

---

## Summary

| Recommendation | Details |
|----------------|---------|
| **Install Cashier** | `composer require laravel/cashier` |
| **Make Tenancy Billable** | Add `Billable` trait to Tenancy model |
| **Use Cashier for Stripe** | Full Stripe integration via Cashier |
| **Keep Contract** | `PaymentGatewayContract` for abstraction |
| **Sync via Webhooks** | Keep `TenancySubscription` in sync |
| **Use Checkout + Portal** | Leverage Stripe's hosted pages |

This approach gives you:
- ✅ Full Stripe features (Checkout, Portal, Tax, SCA)
- ✅ Gateway abstraction for future providers
- ✅ Your existing limit enforcement
- ✅ Minimal code changes
- ✅ Production-ready payment handling
