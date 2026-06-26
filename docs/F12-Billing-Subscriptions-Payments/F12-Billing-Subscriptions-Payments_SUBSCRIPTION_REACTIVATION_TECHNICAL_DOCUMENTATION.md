
# KitchnTabs Subscription Reactivation System - Technical Documentation

> **Version:** 1.0  
> **Last Updated:** February 2026  
> **Status:** Technical Reference  
> **Audience:** Engineers, Technical Support, QA Team  
> **Payment Gateway:** Flow.cl (Chile)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Architecture Overview](#architecture-overview)
4. [Entity-Relationship Diagram](#entity-relationship-diagram)
5. [State Machine Diagrams](#state-machine-diagrams)
6. [Reactivation Decision Flow](#reactivation-decision-flow)
7. [Flow.cl API Integration](#flowcl-api-integration)
8. [Reactivation Methods](#reactivation-methods)
9. [Border Cases & Special Scenarios](#border-cases--special-scenarios)
10. [Implementation Details](#implementation-details)
11. [Testing Scenarios](#testing-scenarios)
12. [Troubleshooting Guide](#troubleshooting-guide)

---

## Executive Summary

The Subscription Reactivation System handles the complex scenario where a customer **cancels** their subscription and later **resubscribes** to the same or different plan. The system intelligently determines whether to:

1. **Reactivate** via `changePlan` (preserving credit balance)
2. **Create new** subscription (when reactivation not possible)

### Key Decision: changePlan vs New Subscription

| Scenario | Method | Credit Preserved | Double Charge Risk |
|----------|--------|------------------|-------------------|
| Cancelled at period end, still within period | `changePlan` | ✅ Yes | ❌ None |
| Period expired, subscription truly cancelled | New Subscription | ❌ No | ⚠️ Possible* |
| No previous subscription | New Subscription | N/A | ❌ None |

*Credit trapped in old subscription cannot be recovered if new subscription is created.

### Critical Business Rule

> **When a subscription is cancelled with `at_period_end=1`, Flow.cl keeps the subscription ACTIVE until the period ends. During this window, using `changePlan` instead of creating a new subscription preserves any credit balance from previous prorations.**

---

## Problem Statement

### The Double-Charge Bug

**Scenario:** Customer subscribed to "Kitchn Scale" plan, received proration credit from a previous downgrade, then cancelled and immediately resubscribed.

**What happened:**
1. Subscription #94 (sus_u6a4862f8d) - Charged $22,490
2. Downgrade proration → Credit balance: -$21,500
3. Cancel subscription (at_period_end=1) → Still active until period ends
4. Resubscribe → System created NEW subscription #95 (sus_c0bc7764a8)
5. NEW subscription charged $22,490 AGAIN
6. Credit balance **trapped** in old subscription #94

**Root Cause:** System was always creating a new subscription on resubscribe, instead of using `changePlan` to reactivate the existing (pending cancellation) subscription.

### The Solution

Modified `resubscribe()` method to:
1. Check if existing subscription can be reactivated via `changePlan`
2. If yes → Use `changePlan` (preserves credit)
3. If no → Fall back to creating new subscription

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SUBSCRIPTION REACTIVATION ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐                                                   │
│  │    TenancyAdmin      │                                                   │
│  │    Dashboard         │                                                   │
│  └──────────┬───────────┘                                                   │
│             │                                                                │
│             │  POST /tenancy/{id}/resubscribe                               │
│             ▼                                                                │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                TenancySubscriptionController                          │   │
│  │                                                                       │   │
│  │  resubscribe(Request $request, Tenancy $tenancy)                     │   │
│  │    - Validates plan_id                                                │   │
│  │    - Calls service->resubscribe()                                    │   │
│  └───────────────────────────────────┬──────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                TenancySubscriptionService                             │   │
│  │                                                                       │   │
│  │  resubscribe(Tenancy, SubscriptionPlan)                              │   │
│  │    │                                                                  │   │
│  │    ├─▶ canReactivateViaChangePlan()  ──────────┐                     │   │
│  │    │         │                                  │                     │   │
│  │    │         ├─ Has external_subscription_id?  │                     │   │
│  │    │         ├─ Has cancels_at set?            │ Decision            │   │
│  │    │         ├─ current_period_end > now()?    │ Logic               │   │
│  │    │         ├─ Gateway supports changePlan?   │                     │   │
│  │    │         └─ Flow status != 4 (cancelled)?  │                     │   │
│  │    │                                            │                     │   │
│  │    │        ┌────────────────────────────┐     │                     │   │
│  │    │        │          TRUE               │◄────┘                     │   │
│  │    │        └─────────────┬──────────────┘                           │   │
│  │    │                      │                                           │   │
│  │    │                      ▼                                           │   │
│  │    │        ┌──────────────────────────────────────────────────────┐ │   │
│  │    ├──YES──▶│ reactivateViaChangePlan()                            │ │   │
│  │    │        │   - gateway->updateSubscription(plan_id)             │ │   │
│  │    │        │   - Clear cancels_at, cancelled_at                   │ │   │
│  │    │        │   - Status → ACTIVE                                  │ │   │
│  │    │        │   - Restore soft-deleted users                       │ │   │
│  │    │        │   - Fire TenancyAccountReactivated event             │ │   │
│  │    │        └──────────────────────────────────────────────────────┘ │   │
│  │    │                                                                  │   │
│  │    │        ┌────────────────────────────┐                           │   │
│  │    │        │          FALSE              │                           │   │
│  │    │        └─────────────┬──────────────┘                           │   │
│  │    │                      │                                           │   │
│  │    │                      ▼                                           │   │
│  │    │        ┌──────────────────────────────────────────────────────┐ │   │
│  │    └──NO───▶│ createNewSubscriptionForReactivation()               │ │   │
│  │             │   - this->create(tenancy, plan)                      │ │   │
│  │             │   - Dispatch CreateGatewaySubscriptionJob            │ │   │
│  │             │   - Restore soft-deleted users                       │ │   │
│  │             │   - Fire TenancyAccountReactivated event             │ │   │
│  │             └──────────────────────────────────────────────────────┘ │   │
│  │                                                                       │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                FlowPaymentGatewayService                              │   │
│  │                                                                       │   │
│  │  updateSubscription() ──▶ POST /subscription/changePlan              │   │
│  │  createSubscription() ──▶ POST /subscription/create                  │   │
│  │  getSubscriptionFromFlow() ──▶ GET /subscription/{id}                │   │
│  │                                                                       │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         Flow.cl API                                   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  REACTIVATION-RELATED ENTITIES                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│              Tenancy                  │
├──────────────────────────────────────┤
│ PK: id (UUID)                        │
│     public_name                      │
│     email                            │
│ ★   status (enum)                    │◄─────────────────┐
│ ★   billing_state (enum)             │                  │
│     payment_gateway                  │                  │
│     primary_currency                 │                  │
│     suspended_at                     │                  │
│     marked_for_deletion_at           │                  │
└──────────────┬───────────────────────┘                  │
               │                                          │
               │ 1:N (One tenancy, many subscriptions)    │ Status transitions:
               ▼                                          │ - ACTIVE
┌──────────────────────────────────────┐                  │ - CANCELED
│        TenancySubscription           │                  │ - SUSPENDED
├──────────────────────────────────────┤                  │ - SOFT_DELETED
│ PK: id                               │                  │
│ FK: tenancy_id                       │                  │
│ FK: subscription_plan_id ────────────┼──────────┐       │
│                                      │          │       │
│ ★   status (enum)                    │          │       │
│ ★   subscription_state (enum)        │◄─────────┼───────┘
│                                      │          │
│ ★   external_subscription_id ────────┼──────────┼──────▶ Flow subscription ID
│     external_customer_id             │          │
│     payment_gateway                  │          │
│                                      │          │
│ ★   current_period_start             │          │
│ ★   current_period_end               │◄─────────┼────── Key for reactivation check
│ ★   cancelled_at                     │          │
│ ★   cancels_at                       │◄─────────┼────── Set when at_period_end=1
│ ★   cancellation_reason              │          │
│                                      │          │
│     trial_ends_at                    │          │
│     failed_payment_attempts          │          │
│     metadata (JSON)                  │          │
└──────────────────────────────────────┘          │
                                                  │
                                                  ▼
                               ┌──────────────────────────────────────┐
                               │        SubscriptionPlan              │
                               ├──────────────────────────────────────┤
                               │ PK: id                               │
                               │     name                             │
                               │     slug                             │
                               │ ★   flow_plan_id ────────────────────┼──▶ Flow plan ID
                               │     billing_cycle                    │
                               │     prices (JSON)                    │
                               │     features (JSON)                  │
                               │     limits (JSON)                    │
                               │     is_active                        │
                               └──────────────────────────────────────┘

┌──────────────────────────────────────┐
│     Flow.cl Subscription (External)  │
├──────────────────────────────────────┤
│     subscriptionId                   │◄────── Maps to external_subscription_id
│     planId                           │
│     customerId                       │
│ ★   status (1=active, 4=cancelled)   │◄────── Used in reactivation check
│ ★   cancel_at_period_end (0 or 1)    │◄────── Key indicator
│     period_start                     │
│     period_end                       │
│ ★   balance                          │◄────── Credit from proration
└──────────────────────────────────────┘

Legend:
★ = Key fields for reactivation logic
PK = Primary Key
FK = Foreign Key
```

---

## State Machine Diagrams

### Subscription Status Transitions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SUBSCRIPTION STATUS STATE MACHINE                         │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────┐
                              │    PENDING    │
                              │               │
                              │ (Awaiting     │
                              │  gateway job) │
                              └───────┬───────┘
                                      │
                                      │ Gateway subscription created
                                      ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │                           TRIALING                               │
    │                                                                  │
    │  (Optional trial period - subscription active, no charges yet)  │
    │                                                                  │
    └──────────────────────────────┬──────────────────────────────────┘
                                   │
                                   │ Trial ends / First payment
                                   ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │                            ACTIVE                                │◄──────┐
    │                                                                  │       │
    │  (Subscription active and paid)                                 │       │
    │                                                                  │       │
    └───────────┬─────────────────────────────┬───────────────────────┘       │
                │                             │                                │
                │ Payment failed              │ User cancels                   │
                ▼                             ▼                                │
    ┌───────────────────┐         ┌───────────────────────────────┐           │
    │                   │         │                                │           │
    │     PAST_DUE      │         │   ACTIVE (cancel scheduled)   │           │
    │                   │         │                                │           │
    │  (Grace period    │         │  cancels_at = period_end      │           │
    │   for payment)    │         │  cancelled_at = now()          │           │
    │                   │         │                                │           │
    └─────────┬─────────┘         └─────────────┬─────────────────┘           │
              │                                 │                              │
              │ Max retries                     │ Period ends                  │
              │ exceeded                        ▼                              │
              │                   ┌────────────────────────────────┐           │
              │                   │                                 │           │
              │                   │         CANCELLED               │           │
              │                   │                                 │           │
              │                   │  (No longer active in gateway) │           │
              │                   │                                 │           │
              │                   └────────────────┬───────────────┘           │
              │                                    │                           │
              └────────────────────┬───────────────┘                           │
                                   │                                           │
                                   │ Resubscribe                               │
                                   │                                           │
                                   ▼                                           │
                    ┌──────────────────────────────────┐                       │
                    │                                   │                       │
                    │     REACTIVATION DECISION         │                       │
                    │                                   │                       │
                    │  Can use changePlan?              │                       │
                    │      │                            │                       │
                    │      ├── YES ────────────────────►│───────────────────────┘
                    │      │   (via changePlan)         │   Status → ACTIVE
                    │      │                            │   Credit preserved
                    │      │                            │
                    │      └── NO ─────────────────────►│ New subscription created
                    │          (new subscription)       │   Status → PENDING → ACTIVE
                    │                                   │
                    └──────────────────────────────────┘
```

### Flow.cl Subscription Status Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLOW.CL STATUS MAPPING                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────┐      ┌────────────────────────────────────────────┐
│   Flow Status      │      │              Local Status                   │
├────────────────────┤      ├────────────────────────────────────────────┤
│                    │      │                                            │
│  status = 1        │─────▶│  ACTIVE                                    │
│  (Active)          │      │  Subscription is live and billing          │
│                    │      │                                            │
├────────────────────┤      ├────────────────────────────────────────────┤
│                    │      │                                            │
│  status = 1        │─────▶│  ACTIVE (but scheduled for cancellation)  │
│  cancel_at_period  │      │  cancels_at = period_end                  │
│  _end = 1          │      │  ★ CAN REACTIVATE VIA changePlan ★        │
│                    │      │                                            │
├────────────────────┤      ├────────────────────────────────────────────┤
│                    │      │                                            │
│  status = 2        │─────▶│  PAST_DUE                                  │
│  (Past Due)        │      │  Payment failed, retrying                  │
│                    │      │                                            │
├────────────────────┤      ├────────────────────────────────────────────┤
│                    │      │                                            │
│  status = 4        │─────▶│  CANCELLED                                 │
│  (Cancelled)       │      │  Truly cancelled, cannot use changePlan   │
│                    │      │  ✗ MUST CREATE NEW SUBSCRIPTION ✗         │
│                    │      │                                            │
└────────────────────┘      └────────────────────────────────────────────┘
```

---

## Reactivation Decision Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               REACTIVATION METHOD DECISION FLOWCHART                         │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────────────┐
                              │   Resubscribe Called  │
                              │   (tenancy, plan)     │
                              └───────────┬───────────┘
                                          │
                                          ▼
                              ┌───────────────────────┐
                              │ Get current           │
                              │ subscription          │
                              └───────────┬───────────┘
                                          │
                                          ▼
                         ┌────────────────────────────────┐
                         │ Has external_subscription_id?  │
                         └────────────────┬───────────────┘
                                          │
                         ┌────────────────┴────────────────┐
                         │                                 │
                        NO                                YES
                         │                                 │
                         ▼                                 ▼
           ┌─────────────────────────┐        ┌───────────────────────┐
           │   CREATE NEW            │        │ Has cancels_at set?   │
           │   SUBSCRIPTION          │        │ (at_period_end=1)     │
           └─────────────────────────┘        └───────────┬───────────┘
                                                          │
                                         ┌────────────────┴────────────────┐
                                         │                                 │
                                        NO                                YES
                                         │                                 │
                                         ▼                                 ▼
                           ┌─────────────────────────┐   ┌───────────────────────────┐
                           │   CREATE NEW            │   │ current_period_end        │
                           │   SUBSCRIPTION          │   │ > now()?                  │
                           └─────────────────────────┘   │ (Still within period)     │
                                                         └───────────┬───────────────┘
                                                                     │
                                                    ┌────────────────┴────────────────┐
                                                    │                                 │
                                                   NO                                YES
                                                    │                                 │
                                                    ▼                                 ▼
                                      ┌─────────────────────────┐   ┌────────────────────────┐
                                      │   CREATE NEW            │   │ Gateway supports       │
                                      │   SUBSCRIPTION          │   │ updateSubscription?    │
                                      │   (Period expired)      │   └───────────┬────────────┘
                                      └─────────────────────────┘               │
                                                                   ┌────────────┴────────────┐
                                                                   │                         │
                                                                  NO                        YES
                                                                   │                         │
                                                                   ▼                         ▼
                                                     ┌─────────────────────────┐   ┌─────────────────────┐
                                                     │   CREATE NEW            │   │ Query Flow API:     │
                                                     │   SUBSCRIPTION          │   │ getSubscriptionFrom │
                                                     └─────────────────────────┘   │ Flow()              │
                                                                                   └───────────┬─────────┘
                                                                                               │
                                                                           ┌───────────────────┴───────────────────┐
                                                                           │                                       │
                                                                  status = 4                              status != 4
                                                                  (Cancelled)                             (Still active)
                                                                           │                                       │
                                                                           ▼                                       ▼
                                                             ┌─────────────────────────┐         ┌─────────────────────────────┐
                                                             │   CREATE NEW            │         │   REACTIVATE VIA            │
                                                             │   SUBSCRIPTION          │         │   changePlan                │
                                                             │   (Flow sub cancelled)  │         │                             │
                                                             └─────────────────────────┘         │   ★ CREDIT PRESERVED ★      │
                                                                                                 │                             │
                                                                                                 │   - gateway->               │
                                                                                                 │     updateSubscription()   │
                                                                                                 │   - Clear cancels_at       │
                                                                                                 │   - Status → ACTIVE        │
                                                                                                 └─────────────────────────────┘
```

---

## Flow.cl API Integration

### Key Endpoints Used

| Endpoint | Method | Purpose | Reactivation Use |
|----------|--------|---------|------------------|
| `/subscription/create` | POST | Create new subscription | Fallback when changePlan not possible |
| `/subscription/changePlan` | POST | Change plan with proration | **Primary reactivation method** |
| `/subscription/cancel` | POST | Cancel subscription | Sets `cancel_at_period_end` |
| `/subscription/get` | POST | Get subscription details | Check status before reactivation |

### /subscription/changePlan (Key for Reactivation)

**Request:**
```json
{
    "subscriptionId": "sus_u6a4862f8d",
    "newPlanId": "plan_kitchn_scale"
}
```

**Response:**
```json
{
    "subscriptionId": "sus_u6a4862f8d",
    "planId": "plan_kitchn_scale",
    "status": 1,
    "balance": -21500,          // ★ Credit balance preserved!
    "period_start": "2026-02-01",
    "period_end": "2026-03-01",
    "cancel_at_period_end": 0   // ★ Cancellation cleared!
}
```

### /subscription/cancel with at_period_end

**Request:**
```json
{
    "subscriptionId": "sus_u6a4862f8d",
    "at_period_end": 1
}
```

**Response:**
```json
{
    "subscriptionId": "sus_u6a4862f8d",
    "status": 1,                    // ★ Still ACTIVE!
    "cancel_at_period_end": 1,      // ★ Scheduled for cancellation
    "period_end": "2026-03-01"
}
```

### Credit Balance Behavior

| Operation | Credit Balance Effect |
|-----------|----------------------|
| Downgrade (immediate) | Credit created for unused time |
| changePlan (reactivation) | **Credit preserved and applied** |
| Create new subscription | **Credit lost** (trapped in old subscription) |

---

## Reactivation Methods

### Method 1: reactivateViaChangePlan() (Preferred)

**When used:** Existing subscription can be reactivated

**Process:**
1. Call `gateway->updateSubscription()` with new plan ID
2. Clear `cancels_at`, `cancelled_at`, `cancellation_reason`
3. Update status to ACTIVE
4. Restore soft-deleted users
5. Fire `TenancyAccountReactivated` event

**Benefits:**
- ✅ Credit balance preserved
- ✅ No double charging
- ✅ Subscription continuity
- ✅ Same subscription ID in Flow

```php
protected function reactivateViaChangePlan(
    Tenancy $tenancy,
    TenancySubscription $existingSubscription,
    SubscriptionPlan $plan,
    $gateway
): array {
    // Use changePlan to reactivate
    $flowPlanId = $plan->flow_plan_id ?? $plan->slug;
    $result = $gateway->updateSubscription($existingSubscription, [
        'plan_id' => $flowPlanId,
    ]);

    if (!($result['success'] ?? false)) {
        // Fall back to new subscription
        return $this->createNewSubscriptionForReactivation($tenancy, $plan, $gateway);
    }

    // Update local subscription
    $existingSubscription->update([
        'subscription_plan_id' => $plan->id,
        'status' => 'active',
        'subscription_state' => SubscriptionState::ACTIVE,
        'cancelled_at' => null,
        'cancels_at' => null,
        'cancellation_reason' => null,
    ]);

    // Restore users, reactivate tenancy, fire event...
    return [
        'success' => true,
        'reactivation_method' => 'changePlan',
        'credit_preserved' => true,
    ];
}
```

### Method 2: createNewSubscriptionForReactivation() (Fallback)

**When used:** Reactivation via changePlan not possible

**Process:**
1. Create new `TenancySubscription` record
2. Dispatch `CreateGatewaySubscriptionJob`
3. Restore soft-deleted users
4. Fire `TenancyAccountReactivated` event

**Limitations:**
- ❌ Credit balance lost
- ❌ New subscription ID in Flow
- ⚠️ Potential double charge if old subscription had credit

```php
protected function createNewSubscriptionForReactivation(
    Tenancy $tenancy,
    SubscriptionPlan $plan,
    $gateway
): array {
    // Create new subscription locally
    $subscription = $this->create($tenancy, $plan, false);

    // Dispatch gateway job for paid plans
    if ($planPrice > 0 && $gateway) {
        $subscription->update([
            'pending_plan_id' => $plan->id,
            'status' => 'pending',
            'subscription_state' => SubscriptionState::PENDING->value,
        ]);
        
        CreateGatewaySubscriptionJob::dispatch($subscription, $plan, $currency);
    }

    // Restore users, reactivate tenancy, fire event...
    return [
        'success' => true,
        'reactivation_method' => 'new_subscription',
        'credit_preserved' => false,  // ⚠️ Credit not preserved
    ];
}
```

---

## Border Cases & Special Scenarios

### Case 1: Immediate Resubscription (Same Day Cancel/Resubscribe)

**Scenario:** Customer cancels, then resubscribes the same day.

```
Timeline:
├── Jan 1: Subscription created, period Jan 1 - Feb 1
├── Jan 15: Downgrade → Credit balance: $50
├── Jan 15: Cancel (at_period_end=1)
├── Jan 15: Resubscribe (same day)
│
│   ★ Flow Status: status=1, cancel_at_period_end=1
│   ★ Local: cancels_at = Feb 1, current_period_end = Feb 1
│
│   Decision: canReactivateViaChangePlan() = TRUE
│   Action: Use changePlan
│   Result: Credit preserved, no new charge
```

**Expected Behavior:** ✅ Reactivate via changePlan

### Case 2: Resubscription After Period End

**Scenario:** Customer cancels, waits until period ends, then resubscribes.

```
Timeline:
├── Jan 1: Subscription created, period Jan 1 - Feb 1
├── Jan 15: Downgrade → Credit balance: $50
├── Jan 15: Cancel (at_period_end=1)
├── Feb 5: Resubscribe (after period ended)
│
│   ★ Flow Status: status=4 (cancelled)
│   ★ Local: current_period_end = Feb 1 (past)
│
│   Decision: canReactivateViaChangePlan() = FALSE
│   Reason: current_period_end.isPast() = true
│   Action: Create new subscription
│   Result: New charge, credit lost
```

**Expected Behavior:** ⚠️ New subscription (credit lost)

### Case 3: Resubscription to Different Plan

**Scenario:** Customer cancels Plan A, resubscribes to Plan B.

```
Timeline:
├── Jan 1: Subscribed to Premium ($99/month)
├── Jan 15: Downgrade to Basic ($29/month) → Credit: $35
├── Jan 20: Cancel Basic (at_period_end=1)
├── Jan 25: Resubscribe to Enterprise ($199/month)
│
│   Decision: canReactivateViaChangePlan() = TRUE
│   Action: Use changePlan with Enterprise plan ID
│   Result: 
│     - Credit ($35) applied to Enterprise
│     - Proration calculated: (Enterprise pro-rata) - $35
│     - Net charge: $XX
```

**Expected Behavior:** ✅ Reactivate via changePlan (different plan OK)

### Case 4: Resubscription with Expired Payment Method

**Scenario:** Customer's card expired during cancellation period.

```
Timeline:
├── Jan 1: Subscription active
├── Jan 15: Cancel (at_period_end=1)
├── Feb 15: Card expires
├── Feb 20: Resubscribe (but card expired)
│
│   Decision: canReactivateViaChangePlan() = TRUE
│   Action: Use changePlan
│   Flow Response: Error - payment method expired
│   
│   Fallback: Create new subscription
│   Required: Customer must add new payment method
```

**Expected Behavior:** ✅ Attempt changePlan → ⚠️ Fallback to new subscription

### Case 5: Gateway API Failure During Reactivation

**Scenario:** Flow API returns error during changePlan.

```php
// In reactivateViaChangePlan()
$result = $gateway->updateSubscription($existingSubscription, [
    'plan_id' => $flowPlanId,
]);

if (!($result['success'] ?? false)) {
    // Automatic fallback
    return $this->createNewSubscriptionForReactivation($tenancy, $plan, $gateway);
}
```

**Expected Behavior:** ✅ Automatic fallback to new subscription

### Case 6: Free Plan Resubscription

**Scenario:** Customer cancels paid plan, resubscribes to free plan.

```
Timeline:
├── Jan 1: Subscribed to Premium ($99/month)
├── Jan 15: Cancel (at_period_end=1)
├── Jan 20: Resubscribe to Free ($0/month)
│
│   Decision: isPaidPlan = false
│   Action: Skip gateway operations
│   Result: Local subscription created, no gateway call
```

**Expected Behavior:** ✅ Local subscription only (no gateway)

### Case 7: Subscription with Pending Scheduled Change

**Scenario:** Customer had a scheduled downgrade, then cancelled.

```
Timeline:
├── Jan 1: Premium plan active
├── Jan 10: Scheduled downgrade to Basic (for Feb 1)
├── Jan 15: Cancel (at_period_end=1)
├── Jan 20: Resubscribe to Premium
│
│   Local State:
│     - subscription_plan_id = Premium
│     - scheduled_plan_id = Basic
│     - cancels_at = Feb 1
│
│   Action: changePlan to Premium
│   Result: 
│     - Cancellation cleared
│     - Scheduled change effectively cancelled (changePlan overrides)
```

**Expected Behavior:** ✅ Reactivate clears scheduled change

---

## Implementation Details

### canReactivateViaChangePlan() Logic

```php
protected function canReactivateViaChangePlan(?TenancySubscription $subscription, $gateway): bool
{
    // 1. Must have subscription
    if (!$subscription) {
        return false;
    }

    // 2. Must have external subscription ID
    if (empty($subscription->external_subscription_id)) {
        return false;
    }

    // 3. Must have been cancelled at period end (cancels_at is set)
    if (!$subscription->cancels_at) {
        return false;
    }

    // 4. Must still be within the billing period
    if (!$subscription->current_period_end || $subscription->current_period_end->isPast()) {
        return false;
    }

    // 5. Gateway must support updateSubscription
    if (!$gateway || !method_exists($gateway, 'updateSubscription')) {
        return false;
    }

    // 6. (Optional) Check Flow status is not 4 (cancelled)
    if (method_exists($gateway, 'getSubscriptionFromFlow')) {
        $flowSubscription = $gateway->getSubscriptionFromFlow(
            $subscription->external_subscription_id
        );
        
        if ($flowSubscription) {
            $flowStatus = $flowSubscription['status'] ?? null;
            if ($flowStatus === 4) {
                return false; // Truly cancelled
            }
            
            // Check cancel_at_period_end for confirmation
            $cancelAtPeriodEnd = $flowSubscription['cancel_at_period_end'] ?? 0;
            if ($cancelAtPeriodEnd) {
                return true; // Can be reactivated
            }
        }
    }

    return true;
}
```

### Database Fields Used

| Field | Table | Purpose |
|-------|-------|---------|
| `external_subscription_id` | `tenancy_subscriptions` | Flow subscription ID |
| `cancels_at` | `tenancy_subscriptions` | Scheduled cancellation date |
| `current_period_end` | `tenancy_subscriptions` | Billing period end date |
| `cancelled_at` | `tenancy_subscriptions` | When cancellation was requested |
| `cancellation_reason` | `tenancy_subscriptions` | Reason for cancellation |
| `flow_plan_id` | `subscription_plans` | Plan ID in Flow system |

---

## Testing Scenarios

### Test 1: Successful Reactivation via changePlan

```php
/**
 * @test
 */
public function it_reactivates_cancelled_subscription_via_change_plan()
{
    // Arrange
    $tenancy = Tenancy::factory()->create();
    $plan = SubscriptionPlan::factory()->create(['flow_plan_id' => 'plan_premium']);
    $subscription = TenancySubscription::factory()->create([
        'tenancy_id' => $tenancy->id,
        'external_subscription_id' => 'sus_test123',
        'cancels_at' => now()->addDays(15),
        'current_period_end' => now()->addDays(15),
        'cancelled_at' => now()->subDay(),
    ]);

    // Mock Flow API
    $this->mockFlowGetSubscription(['status' => 1, 'cancel_at_period_end' => 1]);
    $this->mockFlowChangePlan(['success' => true]);

    // Act
    $service = app(TenancySubscriptionService::class);
    $result = $service->resubscribe($tenancy, $plan);

    // Assert
    $this->assertTrue($result['success']);
    $this->assertEquals('changePlan', $result['reactivation_method']);
    $this->assertTrue($result['credit_preserved']);
    
    $subscription->refresh();
    $this->assertEquals('active', $subscription->status);
    $this->assertNull($subscription->cancels_at);
    $this->assertNull($subscription->cancelled_at);
}
```

### Test 2: Fallback to New Subscription When Period Ended

```php
/**
 * @test
 */
public function it_creates_new_subscription_when_period_has_ended()
{
    // Arrange
    $tenancy = Tenancy::factory()->create();
    $plan = SubscriptionPlan::factory()->create();
    $subscription = TenancySubscription::factory()->create([
        'tenancy_id' => $tenancy->id,
        'external_subscription_id' => 'sus_test123',
        'cancels_at' => now()->subDay(),        // Past
        'current_period_end' => now()->subDay(), // Past
    ]);

    // Act
    $service = app(TenancySubscriptionService::class);
    $result = $service->resubscribe($tenancy, $plan);

    // Assert
    $this->assertTrue($result['success']);
    $this->assertEquals('new_subscription', $result['reactivation_method']);
    
    // Should have created a new subscription
    $this->assertCount(2, $tenancy->subscriptions);
}
```

### Test 3: Fallback When Flow API Reports Cancelled

```php
/**
 * @test
 */
public function it_creates_new_subscription_when_flow_status_is_cancelled()
{
    // Arrange
    $subscription = TenancySubscription::factory()->create([
        'external_subscription_id' => 'sus_test123',
        'cancels_at' => now()->addDays(5),
        'current_period_end' => now()->addDays(5),
    ]);

    // Mock Flow returns status 4 (cancelled)
    $this->mockFlowGetSubscription(['status' => 4]);

    // Act
    $result = $this->service->resubscribe($subscription->tenancy, $this->plan);

    // Assert
    $this->assertEquals('new_subscription', $result['reactivation_method']);
}
```

---

## Troubleshooting Guide

### Issue: Double Charge on Resubscription

**Symptoms:**
- Customer charged twice for same period
- Two receipts generated
- Two Flow subscription IDs

**Diagnosis:**
1. Check if `canReactivateViaChangePlan()` returned `false`
2. Check Flow subscription status at time of resubscribe
3. Check if `current_period_end` was in the past

**Resolution:**
1. Identify which charge to refund
2. Cancel duplicate subscription in Flow
3. Update local records

### Issue: Credit Balance Not Applied

**Symptoms:**
- Customer had credit from downgrade
- Credit not applied to resubscription

**Diagnosis:**
1. Check `reactivation_method` in response
2. If `new_subscription`, credit was trapped

**Resolution:**
1. Check old subscription in Flow for balance
2. Manual credit/refund may be required
3. Contact Flow support if needed

### Issue: Reactivation Attempt Fails

**Symptoms:**
- Error in logs: "changePlan failed"
- Fallback to new subscription

**Diagnosis:**
1. Check Flow API response
2. Verify `flow_plan_id` is correct
3. Check subscription status in Flow dashboard

**Resolution:**
1. Verify payment method is valid
2. Check plan exists in Flow
3. Contact Flow support if API issue

---

## Appendix: Related Documentation

- [SUBSCRIPTION_FLOW_TECHNICAL_DOCUMENTATION.md](./SUBSCRIPTION_FLOW_TECHNICAL_DOCUMENTATION.md) - Main subscription flows
- [KITCHNTABS_BILLING_POLICY.md](./KITCHNTABS_BILLING_POLICY.md) - Billing policy rules
- [SUBSCRIPTION_SYSTEM_COMPLETE_DOCUMENTATION.md](./SUBSCRIPTION_SYSTEM_COMPLETE_DOCUMENTATION.md) - System overview
- [TENANCY_BILLING_SYSTEM.md](./TENANCY_BILLING_SYSTEM.md) - Tenancy billing integration

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | February 2026 | System | Initial documentation |

---

*Last Updated: February 4, 2026*
