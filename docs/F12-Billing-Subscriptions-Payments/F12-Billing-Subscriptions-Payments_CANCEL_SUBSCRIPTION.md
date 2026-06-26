---
layout: default
title: F12-Billing-Subscriptions-Payments CANCEL SUBSCRIPTION
---

## Subscription Cancellation Feature

#### 1. **Models**

**TenancySubscription** (`app/Models/TenancySubscription.php`)
- Manages subscription lifecycle states
- Key fields:
  - `status`: Subscription status (trial, active, cancelled, past_due, expired)
  - `cancelled_at`: Timestamp of cancellation
  - `cancels_at`: Scheduled cancellation date (for end-of-period cancellations)
  - `cancellation_reason`: Text explanation for cancellation

**Tenancy** (Tenancy.php)
- Represents the tenancy account
- Key methods:
  - `isSuspended()`: Checks if tenancy is suspended
  - `suspend()`: Suspends the tenancy
  - `reactivate()`: Reactivates a suspended tenancy
- Fields:
  - `status`: active, suspended, trial, cancelled
  - `suspended_at`: Suspension timestamp
  - `marked_for_deletion_at`: Scheduled deletion date

#### 2. **Controllers**

**TenancySubscriptionController** (TenancySubscriptionController.php)

**Key Endpoint:**
```php
POST /api/tenancy/subscriptions/{id}/cancel
```

**Implementation:**
```php
public function cancel(Request $request, $id)
{
    $subscription = TenancySubscription::findOrFail($id);
    
    // Authorization check
    $user = $request->user();
    if (!$user->isSystemAdmin() && $user->tenancy_id !== $subscription->tenancy_id) {
        abort(403, 'Unauthorized');
    }

    $this->subscriptionService->cancel($subscription);
    
    return response()->json(['success' => true, 'message' => 'Subscription cancelled']);
}
```

**Authorization:**
- TenancyAdmin can cancel their own subscription
- SystemAdmin can cancel any subscription

---

#### 3. **Services**

**TenancySubscriptionService** (TenancySubscriptionService.php)

**Main Cancellation Methods:**

```php
/**
 * Cancel a subscription with gateway sync.
 * 
 * @param TenancySubscription $subscription
 * @param bool $atPeriodEnd Whether to cancel at period end or immediately
 * @return TenancySubscription
 */
public function cancelSubscription(
    TenancySubscription $subscription, 
    bool $atPeriodEnd = true
): TenancySubscription
{
    // 1. Sync with payment gateway if exists
    if ($subscription->payment_gateway) {
        $gateway = $this->getGatewayService($subscription->payment_gateway);
        if ($gateway) {
            $gateway->cancelSubscription($subscription, $atPeriodEnd);
        }
    }

    if ($atPeriodEnd) {
        // Schedule cancellation at period end
        $subscription->update([
            'cancelled_at' => now(),
            // Keep status active until period ends
        ]);
    } else {
        // Cancel immediately
        $subscription->update([
            'status' => 'cancelled',
            'cancelled_at' => now(),
        ]);
    }

    return $subscription->fresh();
}

/**
 * Legacy cancel method (delegates to model).
 */
public function cancel(TenancySubscription $subscription): void
{
    $subscription->cancel();
}
```

**TenancyAccountManagementService** (TenancyAccountManagementService.php)

Handles account deletion after subscription cancellation:

```php
public function initiateAccountDeletion(Tenancy $tenancy, User $requestingUser): array
{
    // 1. Immediately disable the account
    $scheduledDeletionDate = $this->getScheduledDeletionDate();
    
    $tenancy->update([
        'status' => 'suspended',
        'suspended_at' => now(),
        'marked_for_deletion_at' => $scheduledDeletionDate,
        'metadata' => array_merge($tenancy->metadata ?? [], [
            'deletion_requested_by' => $requestingUser->id,
            'deletion_requested_at' => now()->toIso8601String(),
            'deletion_reason' => 'user_requested',
        ]),
    ]);

    // 2. Soft-delete all non-TenancyAdmin users immediately
    $this->softDeleteNonAdminUsers($tenancy);

    // 3. Send notification email
    $this->sendAccountDisabledNotifications($tenancy, $scheduledDeletionDate);

    // 4. Schedule deprovisioning job
    $delayDays = $this->getDeprovisioningDelayDays(); // Default: 30 days
    DeprovisionTenancyJob::dispatch($tenancy->id)
        ->delay(now()->addDays($delayDays));

    return [
        'success' => true,
        'status' => 'suspended',
        'scheduled_deletion_at' => $scheduledDeletionDate->toIso8601String(),
        'days_until_deletion' => $delayDays,
    ];
}
```

---

#### 4. **Events**

**SubscriptionCancelled** (SubscriptionCancelled.php)

```php
class SubscriptionCancelled extends BaseBillingEvent
{
    public TenancySubscription $subscription;
    public string $cancellationReason;
    public bool $immediate;
    public ?\DateTimeInterface $effectiveAt;
    
    public function __construct(
        TenancySubscription $subscription,
        string $cancellationReason,
        bool $immediate = false,
        ?\DateTimeInterface $effectiveAt = null,
        string $source = 'user_action',
        array $metadata = []
    ) {
        parent::__construct($subscription->tenancy, $source, $metadata);
        
        $this->subscription = $subscription;
        $this->cancellationReason = $cancellationReason;
        $this->immediate = $immediate;
        $this->effectiveAt = $effectiveAt ?? $subscription->current_period_end;
    }
}
```

**Registered in EventServiceProvider:**
```php
protected $listen = [
    SubscriptionCancelled::class => [
        HandleSubscriptionCancelled::class,
    ],
];
```

---

#### 5. **Listeners**

**HandleSubscriptionCancelled** (HandleSubscriptionCancelled.php)

```php
class HandleSubscriptionCancelled implements ShouldQueue
{
    public function handle(SubscriptionCancelled $event): void
    {
        $subscription = $event->subscription;
        $tenancy = $event->tenancy;
        
        if ($event->immediate) {
            // Immediate cancellation
            $this->stateMachine->transitionSubscriptionState(
                subscription: $subscription,
                newState: SubscriptionState::CANCELED,
                source: $event->source,
                reason: $event->cancellationReason
            );
            
            // Transition billing state
            $newBillingState = $tenancy->paymentMethods()->exists() 
                ? BillingState::CARD_ACTIVE 
                : BillingState::NONE;
            
            $this->stateMachine->transitionBillingState(
                tenancy: $tenancy,
                newState: $newBillingState,
                source: $event->source,
                reason: 'Subscription cancelled'
            );
        } else {
            // Schedule cancellation at period end
            $subscription->update([
                'cancels_at' => $event->effectiveAt ?? $subscription->current_period_end,
                'cancellation_reason' => $event->cancellationReason,
            ]);
        }
    }
}
```

---

### Cancellation Flows

#### **1. Immediate Cancellation Flow**

```
User Request
    │
    ▼
POST /api/tenancy/subscriptions/{id}/cancel
    │
    ├─ Authorization Check
    │
    ▼
TenancySubscriptionService::cancel()
    │
    ├─ Sync with Payment Gateway
    │
    ├─ Update subscription.status = 'cancelled'
    ├─ Set subscription.cancelled_at = now()
    │
    ▼
Dispatch SubscriptionCancelled Event
    │
    ▼
HandleSubscriptionCancelled Listener
    │
    ├─ Transition to CANCELED state
    ├─ Update Billing State
    ├─ Send Email Notification
    │
    ▼
Response: Success
```

#### **2. End-of-Period Cancellation Flow**

```
User Request (atPeriodEnd = true)
    │
    ▼
TenancySubscriptionService::cancelSubscription($subscription, true)
    │
    ├─ Sync with Payment Gateway
    │
    ├─ Set subscription.cancelled_at = now()
    ├─ Set subscription.cancels_at = current_period_end
    ├─ Keep status = 'active'
    │
    ▼
HandleSubscriptionCancelled Listener
    │
    ├─ Schedule cancellation
    ├─ Send Email Notification
    │
    ▼
[Period End Reached]
    │
    ▼
Billing Job/Webhook
    │
    ├─ Update subscription.status = 'cancelled'
    ├─ Suspend Tenancy (optional)
```

---

### Email Notifications

**Subscription Cancelled Email**

**Template Keys** (lang/en/billing.php):
```php
'subscription_cancelled_subject' => 'Subscription Cancelled',
'subscription_cancelled_greeting' => 'Hello :name,',
'subscription_cancelled_body' => 'Your :plan subscription has been cancelled and will end on :date.',
'subscription_cancelled_reactivate' => 'If you change your mind, you can reactivate your subscription at any time.',
'subscription_cancelled_salutation' => 'We hope to see you again! :company Team',
```

**Account Disabled Email** (sent when account is suspended):

**Template Keys** (lang/en/tenancy.php):
```php
'account_disabled_subject' => 'Your account ":account_name" has been disabled',
'account_disabled_intro' => 'Your account ":account_name" has been disabled and scheduled for deletion.',
'scheduled_deletion_date' => 'Scheduled Deletion Date',
'days_remaining' => 'Days Remaining',
'cancel_deletion_button' => 'Cancel Account Deletion',
```

**Mailable Class:**
```php
App\Mail\TenancyAccountDisabledMail
```

---

### Account Deletion Flow

After subscription cancellation, if user requests account deletion:

```
1. User requests account deletion
   ↓
2. TenancyAccountManagementService::initiateAccountDeletion()
   ├─ Set tenancy.status = 'suspended'
   ├─ Set tenancy.suspended_at = now()
   ├─ Set tenancy.marked_for_deletion_at = now() + 30 days
   ↓
3. Soft-delete all non-TenancyAdmin users
   ↓
4. Send TenancyAccountDisabledMail
   ↓
5. Dispatch DeprovisionTenancyJob (delayed 30 days)
   ↓
   [30 days grace period]
   ↓
6. DeprovisionTenancyJob executes
   ├─ Hard-delete all data
   ├─ Remove from payment gateway
   ├─ Send TenancyAccountDeletedMail
   ↓
7. Account permanently removed
```

---

### Payment Gateway Integration

Each payment gateway must implement:

```php
interface PaymentGatewayInterface
{
    public function cancelSubscription(
        TenancySubscription $subscription, 
        bool $atPeriodEnd
    ): void;
}
```

**Example:**
```php
class StripeGateway implements PaymentGatewayInterface
{
    public function cancelSubscription(TenancySubscription $subscription, bool $atPeriodEnd): void
    {
        $stripeSubscription = \Stripe\Subscription::retrieve(
            $subscription->gateway_subscription_id
        );
        
        if ($atPeriodEnd) {
            $stripeSubscription->cancel(['at_period_end' => true]);
        } else {
            $stripeSubscription->cancel();
        }
    }
}
```

---

### Testing

**Factory Support:**

```php
// TenancySubscriptionFactory
TenancySubscription::factory()->cancelled()->create();

// TenancyFactory
Tenancy::factory()->suspended()->create();
```

**Test Example:**
```php
public function test_tenancy_admin_can_cancel_subscription()
{
    $tenancy = Tenancy::factory()->create();
    $subscription = TenancySubscription::factory()->active()->create([
        'tenancy_id' => $tenancy->id,
    ]);
    $admin = User::factory()->create(['tenancy_id' => $tenancy->id]);
    $admin->assignRole('TenancyAdmin');

    $response = $this->actingAs($admin)
        ->postJson("/api/tenancy/subscriptions/{$subscription->id}/cancel");

    $response->assertOk();
    $subscription->refresh();
    $this->assertEquals('cancelled', $subscription->status);
}
```

---

### Configuration

**Config: tenancy.php**

```php
'deprovisioning_delay_days' => env('TENANCY_DEPROVISIONING_DELAY_DAYS', 30),
```

**Environment Variable:**
```
TENANCY_DEPROVISIONING_DELAY_DAYS=30
```

---

### Frontend Integration (React-Admin)

**API Endpoint:**
```typescript
const cancelSubscription = async (subscriptionId: number) => {
  const response = await dataProvider.create('tenancy/subscriptions/cancel', {
    data: { id: subscriptionId }
  });
  return response;
};
```

---

### Key Considerations

1. **Grace Period**: 30-day default grace period before permanent deletion
2. **User Preservation**: TenancyAdmin users remain active during grace period to allow cancellation reversal
3. **Data Export**: Users should export data before cancellation
4. **Payment Gateway Sync**: Ensures billing stops at the gateway level
5. **Audit Trail**: All actions logged via BillingActivity events
6. **Reversibility**: Cancellation can be reversed during grace period

---

### Related Documentation

- **Subscription Limits**: See `PlanLimitsService` for enforcing plan limits
- **Billing State Machine**: See `BillingStateMachine` for state transitions
- **Account Management**: See `TenancyAccountManagementService` for full lifecycle
- **Payment Gateways**: See `app/Services/Billing/PaymentGateways/` for gateway implementations