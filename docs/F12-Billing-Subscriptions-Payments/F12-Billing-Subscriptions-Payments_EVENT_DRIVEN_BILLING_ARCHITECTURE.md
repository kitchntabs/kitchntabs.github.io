---
layout: default
title: F12-Billing-Subscriptions-Payments EVENT DRIVEN BILLING ARCHITECTURE
---

# Event-Driven Billing Architecture

## Overview

This document describes the event-driven billing architecture for KitchnTabs subscription management. The architecture provides a clear separation between **billing authority** (payment gateway) and **entitlement authority** (application).

## Core Principles

### 1. Billing Authority Lives in the Gateway
The payment gateway is the source of truth for:
- Payment success/failure
- Card registration status
- Subscription renewals
- Invoice generation

### 2. Entitlement Authority Lives in Your App
Your application decides:
- Which features a tenant can access
- When plan changes take effect
- How to respond to billing events

### 3. Events Drive State Changes
All billing operations emit domain events that listeners react to:
- Events are logged for audit trail
- Listeners handle state transitions
- Webhook handlers fire events, not update database directly

---

## State Machines

### Billing State (Tenancy Level)

Tracks the overall billing relationship with a tenant.

```
NONE ─────────────────────────────────────────────────────┐
  │ User initiates card registration                       │
  ▼                                                        │
CARD_PENDING ─────────────────────────────────────────────│
  │ Card registration success    │ Card registration fail  │
  ▼                              └─────────────────────────┘
CARD_ACTIVE ──────────────────────────────────────────────┐
  │ Subscription created                                   │
  ▼                                                        │
SUBSCRIBED ───────────────────────────────────────────────┤
  │ Subscription cancelled    │ Payment method removed     │
  └───────────────────────────┴────────────────────────────┘
         │                          │
         ▼                          ▼
    CARD_ACTIVE                   NONE
```

**Enum:** `App\Enums\BillingState`

| State | Description |
|-------|-------------|
| `NONE` | No billing relationship established |
| `CARD_PENDING` | Card registration in progress (async) |
| `CARD_ACTIVE` | Card registered, ready for subscription |
| `SUBSCRIBED` | Active subscription exists |

### Subscription State (Subscription Level)

Tracks the lifecycle of individual subscriptions.

```
TRIAL ───────────────────────────────────────────────────┐
  │ Trial ends + payment success                          │
  ▼                                                       │
ACTIVE ──────────────────────────────────────────────────│
  │ Payment fails           │ Payment success             │
  ▼                         └─────────────────────────────┘
PAST_DUE ────────────────────────────────────────────────┤
  │ Max retries exceeded    │ Payment success             │
  ▼                         └─────────────────────────────┘
SUSPENDED ───────────────────────────────────────────────┤
  │ Cancelled                                             │
  ▼                                                       │
CANCELED ─────────────────────────────────────────────────
```

**Enum:** `App\Enums\SubscriptionState`

| State | Feature Access | Description |
|-------|---------------|-------------|
| `TRIAL` | ✅ Yes | In trial period |
| `ACTIVE` | ✅ Yes | Paid and current |
| `PAST_DUE` | ✅ Yes (grace) | Payment failed, retrying |
| `SUSPENDED` | ❌ No | Payment exhausted, awaiting resolution |
| `CANCELED` | ❌ No | Subscription terminated |

---

## Domain Events

All billing events extend `App\Events\Billing\BaseBillingEvent`.

### Event List

| Event | Trigger | Description |
|-------|---------|-------------|
| `BillingStateChanged` | State machine | Tenancy billing state transition |
| `SubscriptionStateChanged` | State machine | Subscription state transition |
| `CardRegistrationInitiated` | User action | Card registration started |
| `CardRegistrationCompleted` | Gateway webhook | Card successfully registered |
| `CardRegistrationFailed` | Gateway webhook | Card registration failed |
| `InvoicePaid` | Gateway webhook | Payment successful |
| `InvoicePaymentFailed` | Gateway webhook | Payment failed |
| `PlanChangeRequested` | User action | Plan upgrade/downgrade initiated |
| `PlanChangeApplied` | State machine | Plan change took effect |
| `SubscriptionCancelled` | User/Admin action | Subscription cancelled |
| `SubscriptionRenewed` | Gateway webhook | Subscription renewed for new period |
| `TrialEnding` | Scheduled job | Trial ending reminder |

### Event Structure

```php
abstract class BaseBillingEvent
{
    public Tenancy $tenancy;
    public ?TenancySubscription $subscription;
    public Carbon $occurredAt;
    public string $source;      // 'user', 'admin', 'gateway_webhook', 'system'
    public array $metadata;
}
```

---

## Listeners

### Event → Listener Mapping

| Event | Listener | Action |
|-------|----------|--------|
| `CardRegistrationCompleted` | `HandleCardRegistrationCompleted` | Transition to CARD_ACTIVE |
| `CardRegistrationFailed` | `HandleCardRegistrationFailed` | Transition to NONE |
| `InvoicePaid` | `HandleInvoicePaid` | Transition to ACTIVE, extend period |
| `InvoicePaymentFailed` | `HandleInvoicePaymentFailed` | Transition to PAST_DUE or SUSPENDED |
| `PlanChangeApplied` | `HandlePlanChangeApplied` | Update effective plan |
| `SubscriptionCancelled` | `HandleSubscriptionCancelled` | Handle immediate or scheduled cancel |
| All Events | `LogBillingActivity` | Log to Spatie Activity Log |

### Listener Registration

Listeners are registered in `App\Providers\EventServiceProvider`:

```php
protected $listen = [
    InvoicePaid::class => [HandleInvoicePaid::class],
    InvoicePaymentFailed::class => [HandleInvoicePaymentFailed::class],
    // ...
];

protected $subscribe = [
    LogBillingActivity::class,  // Subscribes to ALL billing events
];
```

---

## Plan Change Policies

### Policy 1: Upgrades Are Immediate

When a customer upgrades to a higher-tier plan:
1. Change takes effect immediately
2. Customer gets immediate access to new features
3. Gateway handles prorated billing (if supported)

```php
PlanChangeType::UPGRADE->isImmediate() === true
```

### Policy 2: Downgrades Are Deferred

When a customer downgrades to a lower-tier plan:
1. Change is scheduled for end of current billing period
2. Customer retains access to current plan until period ends
3. New plan activates at renewal

```php
PlanChangeType::DOWNGRADE->isDeferred() === true
```

### Policy 3: No Proration (Default)

Our gateways (Flow.cl, Rebill) don't support automatic proration:
- Customers pay full price of new plan
- Credits/refunds handled manually if needed

---

## Database Schema

### tenancies table (additions)

| Column | Type | Description |
|--------|------|-------------|
| `billing_state` | enum | Current billing state |
| `card_registration_token` | string | Pending registration token |
| `card_registration_initiated_at` | timestamp | When registration started |

### tenancy_subscriptions table (additions)

| Column | Type | Description |
|--------|------|-------------|
| `subscription_state` | enum | Current subscription state |
| `effective_plan_id` | bigint | Currently active plan |
| `pending_plan_id` | bigint | Scheduled plan change |
| `pending_plan_effective_at` | timestamp | When pending change applies |
| `pending_plan_change_type` | enum | UPGRADE, DOWNGRADE, LATERAL |
| `cancels_at` | timestamp | Scheduled cancellation date |
| `cancellation_reason` | string | Why subscription was cancelled |

---

## Service Classes

### BillingStateMachine

Central service for state transitions with validation and logging.

```php
use App\Services\Billing\BillingStateMachine;

$stateMachine = app(BillingStateMachine::class);

// Transition billing state
$stateMachine->transitionBillingState(
    tenancy: $tenancy,
    newState: BillingState::CARD_ACTIVE,
    source: 'gateway_webhook',
    reason: 'Card registered successfully'
);

// Transition subscription state
$stateMachine->transitionSubscriptionState(
    subscription: $subscription,
    newState: SubscriptionState::ACTIVE,
    source: 'gateway_webhook',
    reason: 'Payment confirmed'
);

// Determine plan change type
$changeType = $stateMachine->determinePlanChangeType($fromPlan, $toPlan);

// Check feature access
$hasAccess = $stateMachine->hasFeatureAccess($subscription);
```

---

## Webhook Integration

### Flow (Gateway Webhook)

```php
// In FlowWebhookTrait

public function handlePaymentReceived(array $data): void
{
    $payment = Payment::where('external_id', $data['flowOrder'])->first();
    $subscription = $payment->subscription;
    
    // Fire event instead of directly updating
    event(new InvoicePaid(
        tenancy: $subscription->tenancy,
        subscription: $subscription,
        amount: $data['amount'],
        currency: 'CLP',
        gatewayPaymentId: $data['flowOrder'],
        source: 'gateway_webhook'
    ));
}
```

### Rebill (Gateway Webhook)

```php
// In RebillWebhookTrait

public function handleSubscriptionRenewed(array $data): void
{
    $subscription = TenancySubscription::where('external_subscription_id', $data['subscriptionId'])->first();
    
    event(new SubscriptionRenewed(
        tenancy: $subscription->tenancy,
        subscription: $subscription,
        periodStart: Carbon::parse($data['periodStart']),
        periodEnd: Carbon::parse($data['periodEnd']),
        renewalCount: $subscription->metadata['renewal_count'] ?? 1,
        source: 'gateway_webhook'
    ));
}
```

---

## Activity Logging

All billing events are logged using Spatie Activity Log.

### Log Format

```php
activity('billing')
    ->performedOn($tenancy)
    ->causedBy(auth()->user())
    ->withProperties([
        'event' => 'invoice_paid',
        'amount' => 29990,
        'currency' => 'CLP',
        'source' => 'gateway_webhook',
    ])
    ->log('Billing event: invoice_paid');
```

### Querying Logs

```php
// Get all billing activity for a tenancy
Activity::forSubject($tenancy)
    ->inLog('billing')
    ->orderBy('created_at', 'desc')
    ->get();

// Get all payment failures
Activity::inLog('billing')
    ->where('properties->event', 'invoice_payment_failed')
    ->get();
```

---

## File Structure

```
app/
├── Enums/
│   ├── BillingState.php           # Billing lifecycle states
│   ├── SubscriptionState.php      # Subscription lifecycle states
│   └── PlanChangeType.php         # Plan change types
├── Events/
│   └── Billing/
│       ├── BaseBillingEvent.php
│       ├── BillingStateChanged.php
│       ├── SubscriptionStateChanged.php
│       ├── CardRegistrationInitiated.php
│       ├── CardRegistrationCompleted.php
│       ├── CardRegistrationFailed.php
│       ├── InvoicePaid.php
│       ├── InvoicePaymentFailed.php
│       ├── PlanChangeRequested.php
│       ├── PlanChangeApplied.php
│       ├── SubscriptionCancelled.php
│       ├── SubscriptionRenewed.php
│       └── TrialEnding.php
├── Listeners/
│   └── Billing/
│       ├── HandleCardRegistrationCompleted.php
│       ├── HandleCardRegistrationFailed.php
│       ├── HandleInvoicePaid.php
│       ├── HandleInvoicePaymentFailed.php
│       ├── HandlePlanChangeApplied.php
│       ├── HandleSubscriptionCancelled.php
│       └── LogBillingActivity.php
├── Services/
│   └── Billing/
│       └── BillingStateMachine.php
└── Providers/
    └── EventServiceProvider.php    # Event-listener bindings
```

---

## Migration

Run the migration to add new fields:

```bash
sail artisan migrate
```

The migration adds all necessary fields to support the event-driven architecture while maintaining backward compatibility with existing `status` field.
