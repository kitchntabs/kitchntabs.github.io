
# KitchnTabs Billing Policy

> **Version:** 1.0  
> **Last Updated:** January 2026  
> **Status:** Active Policy  
> **Applies To:** All KitchnTabs subscription plans using Flow.cl payment gateway

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Guiding Principle](#guiding-principle)
3. [Upgrade Policy](#upgrade-policy)
4. [Downgrade Policy](#downgrade-policy)
5. [Technical Implementation](#technical-implementation)
6. [Customer Communication](#customer-communication)
7. [Future Considerations](#future-considerations)

---

## Executive Summary

KitchnTabs implements a **no-proration billing policy** for subscription plan changes due to technical limitations with the Flow.cl payment gateway and early-stage operational priorities.

| Policy Aspect | Implementation |
|---------------|----------------|
| **Upgrades** | Immediate charge, full amount, no credit for unused time |
| **Downgrades** | Deferred to period end, no refunds, no calculations |
| **Trial Period** | 30 days internal free trial (exception to payment-first rule) |
| **Refunds** | Not automatic; handled case-by-case by support |
| **Proration** | Not supported |

---

## Guiding Principle

### "No Value Delivered Without Payment First"

**Exception:** 30-day internal free trial for new customers.

### Why This Policy?

#### 1. Technical Constraints
- **Flow.cl does not support automatic proration**
- Attempting custom proration creates complex edge cases
- Risk of calculation errors and customer disputes

#### 2. Revenue Protection
- Prevents revenue leakage from calculation mistakes
- Clear audit trail (full charges only)
- Simplified reconciliation with payment gateway

#### 3. Operational Simplicity
- Avoids complex intermediate states
- Reduces support ticket complexity
- Standard early-stage SaaS practice

#### 4. Customer Clarity
- Predictable pricing (no surprise partial charges)
- Easy to understand "full month" logic
- Transparent when communicated upfront

---

## Upgrade Policy

### Summary

**Immediate plan change + immediate full charge**

### Flow Diagram

```
Customer on Basic Plan ($29/month)
Paid through: February 28, 2026
Upgrade requested: February 10, 2026
Target: Premium Plan ($99/month)

┌─────────────────────────────────────────────────────────────┐
│ February 10, 2026 - Upgrade Request                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. User clicks "Upgrade to Premium"                       │
│     ↓                                                       │
│  2. Immediate charge: $99 (full amount)                    │
│     ↓                                                       │
│  3. Payment successful                                      │
│     ↓                                                       │
│  4. Plan changes immediately in Flow                        │
│     ↓                                                       │
│  5. Premium features activated                              │
│     ↓                                                       │
│  6. Next billing: March 10, 2026 ($99)                     │
│                                                             │
│  ❌ No credit for Feb 10-28 unused Basic time              │
│  ❌ No refund                                               │
│  ✅ User considered to have "consumed" Basic period        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Process

| Step | Action | System Behavior |
|------|--------|-----------------|
| 1 | User selects new plan | Display full price clearly |
| 2 | Confirm upgrade | Show "You'll be charged $99 today" |
| 3 | Process payment | Charge full plan amount via Flow |
| 4 | Payment succeeds | Update subscription plan in database |
| 5 | Sync to gateway | Update Flow subscription (or create new) |
| 6 | Activate features | Enable new plan limits immediately |
| 7 | Confirm to user | Email confirmation + dashboard update |

### Technical Implementation

```php
// TenancySubscriptionService.php - upgrade() method

public function upgrade(TenancySubscription $subscription, SubscriptionPlan $newPlan): TenancySubscription
{
    // 1. Update local database FIRST
    $subscription->update([
        'subscription_plan_id' => $newPlan->id,
        'status' => 'active',
    ]);
    
    // 2. Sync with Flow gateway
    $gateway = $this->getGatewayService('flow');
    $currency = $subscription->tenancy->primary_currency ?? 'CLP';
    $price = $newPlan->getPriceForCurrency($currency);
    
    if ($subscription->external_subscription_id) {
        // Update existing subscription in Flow
        $gateway->updateSubscription($subscription, [
            'plan' => $newPlan,
            'plan_id' => $newPlan->flow_plan_id,
            'price' => $price,  // Full amount, no proration
        ]);
    } else {
        // Create new subscription in Flow
        $paymentMethod = $subscription->tenancy->paymentMethods()->first();
        $result = $gateway->createSubscription($subscription, $paymentMethod);
        
        // Full charge happens here via Flow
    }
    
    return $subscription->fresh();
}
```

### Customer Expectation Management

**✅ DO:**
- Show full price clearly: "You'll be charged $99 today"
- Explain immediate activation: "Premium features available now"
- Clarify next billing date: "Next charge: March 10, 2026"

**❌ DON'T:**
- Promise or imply proration
- Show confusing "partial period" messaging
- Create ambiguity about charge amount

---

## Downgrade Policy

### Summary

**Deferred to period end + no refunds**

### Flow Diagram

```
Customer on Premium Plan ($99/month)
Paid through: March 10, 2026
Downgrade requested: February 15, 2026
Target: Basic Plan ($29/month)

┌─────────────────────────────────────────────────────────────┐
│ February 15, 2026 - Downgrade Request                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. User clicks "Downgrade to Basic"                       │
│     ↓                                                       │
│  2. Validate usage vs Basic limits                         │
│     ↓                                                       │
│  3. Mark subscription as "pending_downgrade"               │
│     ↓                                                       │
│  4. NO changes in Flow gateway yet                         │
│     ↓                                                       │
│  5. User keeps Premium features until March 10             │
│     ↓                                                       │
│  6. March 10: Switch to Basic in Flow                      │
│     ↓                                                       │
│  7. Next billing: March 10, 2026 ($29)                     │
│                                                             │
│  ❌ No refund for unused Premium time                      │
│  ❌ No calculations                                         │
│  ✅ Simple: keep features until paid period ends           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Process

| Step | Action | System Behavior |
|------|--------|-----------------|
| 1 | User selects lower plan | Show "effective at period end" message |
| 2 | Validate downgrade | Check current usage vs new plan limits |
| 3 | Conflicts? | If yes, block and show what needs to be removed |
| 4 | No conflicts | Mark subscription with pending downgrade |
| 5 | Database update | Set `scheduled_plan_id` = new plan |
| 6 | Continue current | User keeps all current features |
| 7 | Period ends | Scheduled job processes downgrade |
| 8 | Update gateway | Change plan in Flow to new plan |
| 9 | Next billing | Charge new (lower) amount |

### Validation Logic

Before allowing downgrade, system checks:

```php
// TenancySubscriptionService.php - validateDowngrade()

public function validateDowngrade(Tenancy $tenancy, SubscriptionPlan $newPlan): array
{
    $conflicts = [];
    $newLimits = $newPlan->limits ?? [];
    
    // Check tenant count
    $currentTenants = $tenancy->tenants()->count();
    $tenantLimit = $newLimits['max_tenants'] ?? null;
    
    if ($tenantLimit !== null && $currentTenants > $tenantLimit) {
        $conflicts['tenants'] = [
            'current' => $currentTenants,
            'limit' => $tenantLimit,
            'message' => "Remove " . ($currentTenants - $tenantLimit) . " tenant(s)",
        ];
    }
    
    // Check other resources...
    // - max_users
    // - max_storage_mb
    // - max_locations
    // - etc.
    
    return $conflicts;
}
```

### Technical Implementation

```php
// TenancySubscriptionService.php - downgrade() method

public function downgrade(TenancySubscription $subscription, SubscriptionPlan $newPlan): TenancySubscription
{
    // 1. Validate first
    $conflicts = $this->validateDowngrade($subscription->tenancy, $newPlan);
    
    if (!empty($conflicts)) {
        throw new \Exception('Cannot downgrade: ' . json_encode($conflicts));
    }
    
    // 2. Mark as pending downgrade (NOT synced to gateway yet)
    $subscription->update([
        'scheduled_plan_id' => $newPlan->id,
        'scheduled_plan_change_at' => $subscription->current_period_end,
    ]);
    
    // 3. At period end, scheduled job will:
    //    - Update subscription_plan_id to scheduled_plan_id
    //    - Sync to Flow gateway with new plan
    //    - Clear scheduled_plan_id
    
    return $subscription->fresh();
}
```

### Scheduled Job (Period End)

```php
// App\Console\Commands\ProcessScheduledPlanChanges.php

public function handle()
{
    TenancySubscription::whereNotNull('scheduled_plan_id')
        ->where('scheduled_plan_change_at', '<=', now())
        ->chunk(50, function ($subscriptions) {
            foreach ($subscriptions as $subscription) {
                $newPlan = SubscriptionPlan::find($subscription->scheduled_plan_id);
                
                // Sync to gateway NOW (at period end)
                $gateway = $this->getGatewayService($subscription->payment_gateway);
                $gateway->updateSubscription($subscription, [
                    'plan' => $newPlan,
                    'price' => $newPlan->getPriceForCurrency($subscription->tenancy->primary_currency),
                ]);
                
                // Update local database
                $subscription->update([
                    'subscription_plan_id' => $subscription->scheduled_plan_id,
                    'scheduled_plan_id' => null,
                    'scheduled_plan_change_at' => null,
                ]);
            }
        });
}
```

### Customer Expectation Management

**✅ DO:**
- Show clear effective date: "Changes take effect on March 10"
- Clarify feature retention: "You'll keep Premium until March 10"
- Show next billing amount: "Next charge: $29 on March 10"

**❌ DON'T:**
- Imply immediate downgrade
- Promise refunds or credits
- Create confusion about when change happens

---

## Customer Communication

### Upgrade Confirmation Email

```
Subject: ✅ Welcome to KitchnTabs Premium!

Hi [Name],

Your upgrade to Premium is complete!

✅ Plan: Premium ($99/month)
✅ Charged today: $99
✅ Features: Active immediately
📅 Next billing: March 10, 2026

What's new in Premium:
• Unlimited locations
• Advanced reporting
• Priority support

Questions? Reply to this email or visit our Help Center.

Thanks,
The KitchnTabs Team
```

### Downgrade Confirmation Email

```
Subject: ℹ️ Your plan change is scheduled

Hi [Name],

Your plan change request has been received.

Current Plan: Premium ($99/month)
New Plan: Basic ($29/month)
Effective Date: March 10, 2026

Until March 10:
✅ You'll keep all Premium features
✅ No changes to your account

After March 10:
📉 Plan switches to Basic
💰 Next charge: $29 (March 10, 2026)

Questions? Reply to this email.

Thanks,
The KitchnTabs Team
```

---

## Future Considerations

### When to Revisit This Policy

1. **Gateway Migration**: If switching from Flow to a proration-capable gateway (e.g., Stripe)
2. **Scale Achievement**: When monthly recurring revenue justifies custom proration logic
3. **Market Pressure**: If competitors offer proration and it becomes a conversion blocker
4. **Customer Feedback**: If downgrade policy causes significant churn

### Potential Evolution Path

```
Phase 1 (Current): No proration
    ↓
Phase 2: Proration for upgrades only (if gateway supports)
    ↓
Phase 3: Full proration system (custom logic + gateway integration)
```

### Cost-Benefit Analysis for Custom Proration

| Benefit | Cost |
|---------|------|
| Better customer perception | Development time: ~40 hours |
| Competitive parity | Testing complexity: High |
| Reduced support tickets | Ongoing maintenance burden |
| Potential conversion uplift | Risk of calculation bugs |

**Recommendation:** Maintain current policy until **monthly revenue > $50k** or **customer complaints > 10/month**.

---

## Compliance & Legal

### Chilean Consumer Law (Ley del Consumidor)

- **Transparency:** All pricing must be clear before purchase ✅
- **Right to information:** Terms must be accessible ✅
- **No deceptive practices:** Don't imply proration if not provided ✅

### Recommended Disclosures

On pricing page:
```
* Upgrades are charged immediately at the full monthly rate. 
  No credit is provided for unused time on your current plan.

* Downgrades take effect at the end of your current billing period.
  You'll keep your current features until then.
```

In terms of service:
```
6.2 Plan Changes

(a) Upgrades: When you upgrade your plan, you will be charged 
    immediately for the full monthly amount of the new plan. 
    No proration or credit will be provided for unused time 
    on your previous plan.

(b) Downgrades: When you downgrade your plan, the change will 
    take effect at the end of your current billing period. 
    No refund will be provided for the current period.
```

---

## Implementation Checklist

### Development Team

- [x] `TenancySubscriptionService::upgrade()` - immediate sync to gateway
- [x] `TenancySubscriptionService::downgrade()` - deferred, validate first
- [x] `TenancySubscriptionService::validateDowngrade()` - check limits
- [ ] Scheduled job: `ProcessScheduledPlanChanges` (runs daily)
- [ ] Admin dashboard: show "pending downgrade" indicator
- [ ] Customer portal: show "effective date" for downgrades

### Frontend Team

- [ ] Upgrade flow: Display full charge amount prominently
- [ ] Upgrade confirmation: "You'll be charged $X today"
- [ ] Downgrade flow: Display "effective [date]" message
- [ ] Downgrade validation: Show conflicts (e.g., "Remove 2 tenants first")
- [ ] Account page: Show scheduled plan changes

### Support Team

- [ ] FAQ: Document upgrade/downgrade policy
- [ ] Knowledge Base: Add examples and scenarios
- [ ] Support macros: Pre-written responses for common questions
- [ ] Training: Educate agents on policy rationale

### Legal/Compliance

- [ ] Update Terms of Service
- [ ] Update Pricing Page disclaimers
- [ ] Email templates: Upgrade confirmation
- [ ] Email templates: Downgrade confirmation
- [ ] Review with Chilean legal counsel (if operating in Chile)

---

## Appendix: Comparison with Other SaaS

### Industry Benchmarks

| Company | Upgrade Policy | Downgrade Policy |
|---------|----------------|------------------|
| **Early-stage SaaS** | Usually no proration | Deferred to period end |
| **Stripe Billing** | Proration available | Proration available |
| **GitHub** | Immediate proration | Immediate change, no refund |
| **Heroku** | Immediate proration | Immediate change, no refund |
| **Slack** | Proration | Proration |
| **KitchnTabs** | **No proration** ✅ | **Deferred, no refund** ✅ |

**Conclusion:** KitchnTabs policy is **conservative but standard** for early-stage products.

---

## Questions & Answers

### Q: Why not offer proration like Stripe?

**A:** Flow.cl (our payment gateway) doesn't support automatic proration. Building custom proration logic would:
1. Require ~40 hours of development
2. Introduce calculation bug risks
3. Add ongoing maintenance burden
4. Provide minimal ROI at current scale

### Q: Will customers complain?

**A:** Possibly, but mitigated by:
1. **Clear communication** upfront
2. **Industry precedent** (common for early-stage)
3. **Focus on value** (features > billing mechanics)
4. **Responsive support** (handle edge cases individually)

### Q: When will this policy change?

**A:** When one of:
1. We migrate to a proration-capable gateway (e.g., Stripe)
2. Monthly revenue > $50k justifies custom logic
3. Customer complaints > 10/month indicate market demand
4. Competitive pressure makes it necessary

### Q: What about annual plans?

**A:** If added in the future:
- **Upgrade annual → higher annual:** Charge difference immediately
- **Downgrade annual → lower annual:** Apply at renewal
- **Monthly ↔ annual:** Requires cancellation + new subscription

---

**Document Owner:** Engineering Team  
**Last Review:** January 2026  
**Next Review:** July 2026 (6 months)
