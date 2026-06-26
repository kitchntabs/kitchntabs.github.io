
# Subscription System Bug Fixes

## Date: 2024-01-15

## Issues Identified

After real-world testing with Flow.cl payment gateway, two critical bugs were discovered:

### 1. **Data Consistency Bug**: `effective_plan_id` was NULL
- **Problem**: After plan change, `effective_plan_id` field remained `null` instead of tracking the active entitlement plan
- **Impact**: Event-driven architecture couldn't properly track which features user should have access to
- **Root Cause**: Backend service wasn't setting `effective_plan_id` during plan changes

### 2. **Frontend Cache Bug**: UI showing stale plan data
- **Problem**: UI continued showing "free-trial" plan after successful upgrade to paid plan
- **Impact**: Users see incorrect information about their current subscription
- **Root Cause**: React-Admin aggressive caching + relationships not being loaded

## Fixes Applied

### Backend Fixes

#### 1. Updated `TenancySubscriptionResource` 
**File**: `dash-backend/app/Http/Resources/TenancySubscriptionResource.php`

**Changes**:
- Added all event-driven architecture fields to API response:
  - `effective_plan_id` - Current entitlement plan
  - `subscription_state` - New state enum (trial/active/past_due/suspended/canceled)
  - `pending_plan_id` - Plan scheduled for next period
  - `pending_plan_change_type` - Type of pending change (upgrade/downgrade)
  - `pending_plan_effective_at` - When pending change takes effect
  - `cancels_at` - Scheduled cancellation date
  - `cancellation_reason` - Why subscription is being cancelled

- Added relationship loading:
  - `subscription_plan` - Legacy billing plan from gateway
  - `effective_plan` - Current entitlement plan (event-driven)
  - `pending_plan` - Next period's plan

**Code**:
```php
public function toArray($request): array
{
    return [
        'id' => $this->id,
        'tenancy_id' => $this->tenancy_id,
        
        // Legacy fields (for backward compatibility)
        'subscription_plan_id' => $this->subscription_plan_id,
        'status' => $this->status,
        'cancelled_at' => $this->cancelled_at?->toISOString(),
        
        // Event-driven architecture fields
        'effective_plan_id' => $this->effective_plan_id,
        'subscription_state' => $this->subscription_state,
        'pending_plan_id' => $this->pending_plan_id,
        'pending_plan_change_type' => $this->pending_plan_change_type,
        'pending_plan_effective_at' => $this->pending_plan_effective_at?->toISOString(),
        'cancels_at' => $this->cancels_at?->toISOString(),
        'cancellation_reason' => $this->cancellation_reason,
        
        // ... other fields ...
        
        // Include plans when loaded
        'subscription_plan' => $this->whenLoaded('subscriptionPlan'),
        'effective_plan' => $this->whenLoaded('effectivePlan'),
        'pending_plan' => $this->whenLoaded('pendingPlan'),
        
        // Legacy alias
        'plan' => $this->whenLoaded('subscriptionPlan'),
    ];
}
```

#### 2. Updated `TenancySubscriptionController::changePlan()`
**File**: `dash-backend/app/Http/Controllers/API/Tenancy/TenancySubscriptionController.php`

**Changes**:
- Added relationship eager-loading after plan change
- Ensures API response includes full plan details

**Code**:
```php
public function changePlan(Request $request, $id)
{
    // ... validation and authorization ...
    
    try {
        $subscription = $this->subscriptionService->changePlan($subscription, $newPlan);
        
        // ✅ NEW: Reload with relationships
        $subscription->load(['subscriptionPlan', 'effectivePlan', 'pendingPlan']);
        
        return response()->json(['success' => true, 'data' => new TenancySubscriptionResource($subscription)]);
    } catch (\Exception $e) {
        return response()->json(['success' => false, 'error' => $e->getMessage()], 400);
    }
}
```

**Note**: The `TenancySubscriptionService::upgrade()` and `upgradePlan()` methods were **already correctly setting** `effective_plan_id`:

```php
$updateData = [
    'subscription_plan_id' => $newPlan->id,
    'effective_plan_id' => $newPlan->id, // ✅ Already present
    'status' => 'active',
];
```

### Frontend Fixes

#### 1. Updated `TenancySubscriptionList` Component
**File**: `dash-frontend/apps/kitchntabs-web/src/components/billing/TenancySubscriptionList.tsx`

**Changes**:
- Added cache-busting timestamp to all API requests
- Configured API to include relationships: `subscriptionPlan`, `effectivePlan`, `pendingPlan`
- Changed plan display to use `effective_plan` with fallback to `subscription_plan` (backward compatibility)
- Changed `currentPlanId` prop to use `effective_plan_id || subscription_plan_id`
- Changed `onSuccess` callback to force full refresh with loading indicator

**Code Snippets**:
```typescript
// Cache busting
const cacheBuster = Date.now();

// Include relationships in API request
meta: { 
    forceRefresh: true,
    include: 'subscriptionPlan,effectivePlan,pendingPlan',
}

// Use effective_plan with fallback
const displayPlan = (subscription as any).effective_plan || subscription.subscription_plan;
const effectivePlanId = (subscription as any).effective_plan_id || subscription.subscription_plan_id;

// Pass effective_plan_id to selector
<SubscriptionPlansSelector
    currentPlanId={(subscription as any)?.effective_plan_id || subscription?.subscription_plan_id}
    subscriptionId={subscription?.id}
    hasPaymentMethod={paymentMethods.length > 0}
    onSuccess={() => fetchData(true)} // Force full refresh
/>
```

#### 2. Updated Schema Definition
**File**: `dash-frontend/apps/kitchntabs-web/src/resources/private/schemas/tenancy_subscription.tsx`

**Changes**:
- Changed primary plan field from `subscription_plan.name` to `effective_plan.name`
- Added custom render with fallback for backward compatibility
- Added `Subscription State` field (new enum)
- Relabeled old `Status` as "Status (Legacy)"
- Added "Pending Changes" tab with 3 fields
- Added `cancels_at` and `cancellation_reason` fields

**Code**:
```typescript
{
    label: 'Current Plan',
    attribute: 'effective_plan.name',
    type: String,
    // Fallback to subscription_plan.name if effective_plan is null
    render: (record: any) => {
        return record?.effective_plan?.name || record?.subscription_plan?.name || 'N/A';
    },
}
```

#### 3. Updated Resource Configuration
**File**: `dash-frontend/apps/kitchntabs-web/src/resources/private/tenancyResources.tsx`

**Changes**:
- Added `listProps.queryOptions.meta.include` to subscription resource
- Configured to include relationships in all API calls

**Code**:
```typescript
{
    model: "tenancy/subscriptions",
    // ...
    listProps: {
        queryOptions: {
            meta: {
                include: 'subscriptionPlan,effectivePlan,pendingPlan',
            },
        },
    },
}
```

## Testing Instructions

### 1. Clear Browser Cache
```bash
# In browser DevTools Console:
localStorage.clear();
sessionStorage.clear();
# Then hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

### 2. Test Plan Change
1. Login to your tenancy account
2. Go to "Subscription" page
3. Current plan should show correctly (using `effective_plan`)
4. Click on a different plan
5. Confirm the change
6. **Expected Results**:
   - API response includes `effective_plan_id` with new plan ID
   - API response includes full `effective_plan` object with plan details
   - UI immediately updates to show new plan (no stale cache)
   - No need to refresh page manually

### 3. Verify API Response
Use browser DevTools Network tab to inspect the API response:

**After plan change** (`POST /api/tenancy/subscriptions/{id}/change-plan`):
```json
{
    "success": true,
    "data": {
        "id": 47,
        "tenancy_id": "019bf2d6-22ab-713a-b07d-1c978fcf079d",
        "subscription_plan_id": 286,
        "effective_plan_id": 286,  // ✅ Should match new plan
        "subscription_state": "active",
        "status": "active",
        "subscription_plan": {
            "id": 286,
            "name": "Restaurante Micro",
            "price": 1490000
        },
        "effective_plan": {  // ✅ Should be included
            "id": 286,
            "name": "Restaurante Micro",
            "price": 1490000
        }
    }
}
```

## Architecture Notes

### Event-Driven vs Legacy Fields

The system maintains two sets of fields for backward compatibility during migration:

| Purpose | Legacy Field | Event-Driven Field | Notes |
|---------|--------------|-------------------|-------|
| **Billing Authority** | `subscription_plan_id` | `subscription_plan_id` | Gateway's billing plan |
| **Entitlement Authority** | `subscription_plan_id` | `effective_plan_id` | What user can access NOW |
| **State Tracking** | `status` | `subscription_state` | More detailed states |
| **Cancellation** | `cancelled_at` | `cancels_at` | Scheduled vs immediate |
| **Plan Changes** | Immediate update | `pending_plan_id` | Deferred to period end |

### Field Priority Rules

1. **For Display**: Use `effective_plan` → fallback to `subscription_plan`
2. **For Entitlements**: Use `effective_plan_id` → fallback to `subscription_plan_id`
3. **For State**: Use `subscription_state` → fallback to `status`

### Why Both Fields Exist

- **`subscription_plan_id`**: What plan is registered in the payment gateway (Flow, Rebill, etc.)
- **`effective_plan_id`**: What plan features the user has access to RIGHT NOW

**Example Scenario - Downgrade**:
1. User downgrades from $50/month plan to $20/month plan on Jan 15
2. Downgrade scheduled for end of period (Feb 1)
3. From Jan 15 to Feb 1:
   - `subscription_plan_id` = $20 plan (gateway will bill this next)
   - `effective_plan_id` = $50 plan (user keeps current features until period ends)
   - `pending_plan_id` = $20 plan
   - `pending_plan_change_type` = "downgrade"
   - `pending_plan_effective_at` = "2024-02-01"

## Migration Status

### ✅ Completed
- Event-driven fields added to database schema
- `TenancySubscriptionResource` includes all new fields
- Frontend requests relationships in API calls
- Frontend uses `effective_plan` for display with fallback
- Backend sets `effective_plan_id` during upgrades
- Controller loads relationships after plan changes
- Schema updated to show new fields

### ⏳ Pending
- Verify downgrade flow also sets `effective_plan_id` when change applies
- Test with real Flow.cl subscription (user needs to retry)
- Integrate BillingStateMachine into service methods
- Update webhook handlers to fire domain events
- Add unit tests for new field population

### 🔮 Future Enhancements
- Implement automatic plan change application on period end
- Add webhook handlers for gateway subscription updates
- Fire domain events (`InvoicePaid`, `PlanChangeApplied`, etc.)
- Replace direct database updates with state machine transitions

## Related Documentation

- [SUBSCRIPTION_SYSTEM_COMPLETE_DOCUMENTATION.md](./docs/SUBSCRIPTION_SYSTEM_COMPLETE_DOCUMENTATION.md) - Full system architecture
- Backend Service: `dash-backend/app/Services/Tenancy/TenancySubscriptionService.php`
- Backend Controller: `dash-backend/app/Http/Controllers/API/Tenancy/TenancySubscriptionController.php`
- Backend Resource: `dash-backend/app/Http/Resources/TenancySubscriptionResource.php`
- Frontend Component: `dash-frontend/apps/kitchntabs-web/src/components/billing/TenancySubscriptionList.tsx`
- Frontend Schema: `dash-frontend/apps/kitchntabs-web/src/resources/private/schemas/tenancy_subscription.tsx`
- Frontend Config: `dash-frontend/apps/kitchntabs-web/src/resources/private/tenancyResources.tsx`
