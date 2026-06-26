---
layout: default
title: F15-Notifications-Messaging EMAIL UNSUBSCRIBE SYSTEM
---

# Email Unsubscribe System Documentation

## Overview

The Email Unsubscribe System provides CAN-SPAM Act and GDPR-compliant unsubscribe functionality for marketing emails sent through the Dash platform. This system allows customers to opt-out of marketing communications while maintaining the ability to receive transactional emails.

## Features

- **Token-Based Unsubscribe**: Secure unsubscribe links using unique 64-character tokens
- **Opt-Out Model**: Users are subscribed by default, can opt-out anytime
- **Multi-Tenant Support**: Per-tenant subscription management
- **Subscription Types**: Separate tracking for marketing vs transactional emails
- **Reason Tracking**: Collects unsubscribe reasons and feedback
- **Audit Trail**: Tracks IP, user agent, timestamps for compliance
- **Web Interface**: User-friendly unsubscribe confirmation pages
- **Auto-Filtering**: Automatically excludes unsubscribed emails from notifications

---

## Database Schema

### Table: `email_subscriptions`

```sql
CREATE TABLE email_subscriptions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    tenant_id BIGINT UNSIGNED NULL,
    subscription_type VARCHAR(50) NOT NULL DEFAULT 'marketing',
    is_subscribed BOOLEAN NOT NULL DEFAULT true,
    unsubscribe_token VARCHAR(64) UNIQUE NOT NULL,
    unsubscribed_at TIMESTAMP NULL,
    unsubscribe_reason VARCHAR(100) NULL,
    unsubscribe_feedback TEXT NULL,
    metadata JSON NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_email_subscribed (email, is_subscribed),
    INDEX idx_token (unsubscribe_token),
    INDEX idx_composite (email, tenant_id, subscription_type),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);
```

### Subscription Types

| Type | Description | Use Case |
|------|-------------|----------|
| `marketing` | Marketing emails, newsletters, promotions | Jumpseller order updates, promotional campaigns |
| `transactional` | Critical order/account emails | Payment confirmations, password resets |
| `all` | All types of emails | Complete opt-out |

### Unsubscribe Reasons

- `too_many_emails` - Receiving too many emails
- `not_relevant` - Content not relevant/interesting
- `never_subscribed` - Never signed up for emails
- `privacy_concerns` - Privacy concerns
- `other` - Other reason (with optional feedback)

---

## System Components

### 1. Migration

**File**: `domain/database/migrations/2024_12_22_000002_create_email_subscriptions_table.php`

```bash
# Run migration
php artisan migrate

# Rollback if needed
php artisan migrate:rollback --step=1
```

### 2. Model

**File**: `domain/app/Models/Common/EmailSubscription.php`

**Key Methods**:
```php
// Get or create subscription record
$subscription = EmailSubscription::getOrCreate(
    $email, 
    $tenantId, 
    EmailSubscription::TYPE_MARKETING
);

// Check if subscribed (true if no record = opt-out model)
$isSubscribed = EmailSubscription::isSubscribed($email, $tenantId, $type);

// Unsubscribe
$subscription->unsubscribe('too_many_emails', 'Getting too many order updates');

// Resubscribe
$subscription->resubscribe();

// Get unsubscribe URL
$url = $subscription->getUnsubscribeUrl();

// Find by token
$subscription = EmailSubscription::findByToken($token);
```

**Scopes**:
```php
// Get subscribed users
EmailSubscription::subscribed()->get();

// Get unsubscribed users
EmailSubscription::unsubscribed()->get();

// Filter by tenant
EmailSubscription::byTenant($tenantId)->get();

// Filter by type
EmailSubscription::byType(EmailSubscription::TYPE_MARKETING)->get();
```

### 3. Controller

**File**: `domain/app/Http/Controllers/API/Public/UnsubscribeController.php`

**Endpoints**:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/unsubscribe/{token}` | Show unsubscribe confirmation page |
| POST | `/unsubscribe/{token}` | Process unsubscribe request |
| POST | `/unsubscribe/{token}/resubscribe` | Process resubscribe request |
| GET | `/api/subscriptions/statistics` | Admin: Get subscription stats |

**Request Validation**:
```php
POST /unsubscribe/{token}
{
    "reason": "too_many_emails",  // Required: one of the enum values
    "feedback": "Optional text"   // Optional: max 500 chars
}
```

### 4. Routes

**File**: `domain/routes/api/unsubscribe_routes.php`

```php
// Public routes (no authentication)
Route::prefix('unsubscribe')->group(function () {
    Route::get('/{token}', [UnsubscribeController::class, 'show'])
        ->name('unsubscribe.show');
    Route::post('/{token}', [UnsubscribeController::class, 'unsubscribe'])
        ->name('unsubscribe.process');
    Route::post('/{token}/resubscribe', [UnsubscribeController::class, 'resubscribe'])
        ->name('unsubscribe.resubscribe');
});

// Admin routes (auth:sanctum)
Route::middleware(['auth:sanctum'])->group(function () {
    Route::get('/api/subscriptions/statistics', [UnsubscribeController::class, 'statistics'])
        ->name('subscriptions.statistics');
});
```

### 5. Views

**Directory**: `resources/views/unsubscribe/`

| File | Purpose |
|------|---------|
| `confirm.blade.php` | Unsubscribe confirmation form |
| `success.blade.php` | Successful unsubscribe message |
| `already-unsubscribed.blade.php` | Already unsubscribed message |
| `invalid.blade.php` | Invalid/expired token error |
| `resubscribed.blade.php` | Successful resubscribe message |

### 6. Email Layout Integration

**File**: `resources/views/layouts/emails.blade.php`

The unsubscribe link is automatically added to the email footer:

```blade
@if(isset($unsubscribeUrl))
<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(0,0,0,0.1);">
    <a href="{{ $unsubscribeUrl }}" style="color: #666; text-decoration: none; font-size: 12px;">
        Unsubscribe from these emails
    </a>
</div>
@endif
```

### 7. Helper Service

**File**: `app/AppNotifications/EmailSubscriptionHelper.php`

**Usage Examples**:

```php
use App\AppNotifications\EmailSubscriptionHelper;

// Get unsubscribe URL for email
$url = EmailSubscriptionHelper::getUnsubscribeUrl(
    'customer@example.com',
    $tenantId,
    EmailSubscription::TYPE_MARKETING
);

// Check if subscribed
$isSubscribed = EmailSubscriptionHelper::isSubscribed(
    'customer@example.com',
    $tenantId,
    EmailSubscription::TYPE_MARKETING
);

// Filter unsubscribed emails from list
$emails = ['user1@example.com', 'user2@example.com'];
$subscribed = EmailSubscriptionHelper::filterUnsubscribedEmails(
    $emails,
    $tenantId,
    EmailSubscription::TYPE_MARKETING
);

// Prepare notification data with unsubscribe URL
$data = EmailSubscriptionHelper::prepareNotificationData(
    $notificationData,
    'customer@example.com',
    $tenantId,
    EmailSubscription::TYPE_MARKETING
);
```

### 8. Notification Integration

**File**: `app/AppNotifications/AppNotificationBuilder.php`

The system automatically:
1. **Filters unsubscribed users** before sending emails
2. **Adds unsubscribe URLs** to notification data for marketing emails

**Configuration**:

Add your notification classes to the marketing list in `EmailSubscriptionHelper`:

```php
private static $marketingNotifications = [
    'Domain\\App\\Notifications\\Marketplace\\MarketplaceOrderUpdateNotification',
    'Domain\\App\\Notifications\\Marketing\\NewsletterNotification',
    // Add more...
];
```

---

## Implementation Guide

### Step 1: Run Migration

```bash
cd dash-backend
php artisan migrate
```

### Step 2: Register Routes

Add to `domain/routes/api.php`:

```php
require __DIR__ . '/unsubscribe_routes.php';
```

### Step 3: Add Unsubscribe to Mailable

For custom Mailable classes (like `MarketplaceOrderUpdateMail`):

```php
use App\AppNotifications\EmailSubscriptionHelper;
use Domain\App\Models\Common\EmailSubscription;

class MarketplaceOrderUpdateMail extends Mailable
{
    public $unsubscribeUrl;
    
    public function __construct(Order $order, $tenantData = null)
    {
        // ... existing code ...
        
        // Add unsubscribe URL
        $customerEmail = $order->customer_email ?? $order->data['customer']['email'] ?? null;
        $tenantId = $order->tenant_id ?? null;
        
        if ($customerEmail) {
            $this->unsubscribeUrl = EmailSubscriptionHelper::getUnsubscribeUrl(
                $customerEmail,
                $tenantId,
                EmailSubscription::TYPE_MARKETING
            );
        }
    }
    
    public function build()
    {
        return $this->subject($this->title)
            ->view('emails.marketplace-order-update')
            ->with(['unsubscribeUrl' => $this->unsubscribeUrl]);
    }
}
```

### Step 4: Add to Email Template

Your email templates extending `layouts/emails.blade.php` will automatically show the unsubscribe link if `$unsubscribeUrl` is set.

For standalone templates:

```blade
@if(isset($unsubscribeUrl))
<div style="text-align: center; margin-top: 20px;">
    <a href="{{ $unsubscribeUrl }}" style="color: #999; font-size: 12px;">
        Unsubscribe from these emails
    </a>
</div>
@endif
```

### Step 5: Test the Flow

```bash
# Send test email
php artisan tinker
> $order = Domain\App\Models\Order\Order::find(1);
> Mail::to('test@example.com')->send(new Domain\App\Mail\MarketplaceOrderUpdateMail($order));

# Check subscription record
> Domain\App\Models\Common\EmailSubscription::where('email', 'test@example.com')->first();

# Test unsubscribe
# Visit: http://your-app.test/unsubscribe/{token}
```

---

## API Examples

### Get Subscription Statistics

```bash
curl -X GET "https://api.yourdomain.com/api/subscriptions/statistics" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Accept: application/json"
```

**Response**:
```json
{
    "total_subscriptions": 1250,
    "subscribed": 1100,
    "unsubscribed": 150,
    "by_type": {
        "marketing": 1000,
        "transactional": 150,
        "all": 100
    },
    "unsubscribe_reasons": {
        "too_many_emails": 80,
        "not_relevant": 45,
        "never_subscribed": 15,
        "privacy_concerns": 10
    }
}
```

### Unsubscribe User

```bash
curl -X POST "https://api.yourdomain.com/unsubscribe/{token}" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "too_many_emails",
    "feedback": "I receive order updates too frequently"
  }'
```

**Response**:
```json
{
    "message": "You have been successfully unsubscribed",
    "email": "customer@example.com"
}
```

---

## Compliance

### CAN-SPAM Act Requirements ✓

- ✅ Clear unsubscribe mechanism in every marketing email
- ✅ Process unsubscribe requests within 10 business days (instant in our case)
- ✅ Physical address included in email footer (from tenant data)
- ✅ Identify message as advertisement (via email content)
- ✅ Honor opt-out requests promptly

### GDPR Requirements ✓

- ✅ Right to be forgotten (unsubscribe removes from marketing list)
- ✅ Consent tracking (opt-out model with timestamp)
- ✅ Data portability (subscription data can be exported)
- ✅ Audit trail (IP, user agent, timestamp tracking)
- ✅ Clear privacy information (linked in email footer)

---

## Monitoring & Analytics

### Logs

All unsubscribe actions are logged to `storage/logs/laravel.log`:

```
[2024-12-22 10:30:45] local.INFO: User unsubscribed {"email":"user@example.com","tenant_id":1,"reason":"too_many_emails"}
```

### Database Queries

```sql
-- Unsubscribe rate by tenant
SELECT 
    tenant_id,
    COUNT(*) as total,
    SUM(CASE WHEN is_subscribed = 0 THEN 1 ELSE 0 END) as unsubscribed,
    ROUND(SUM(CASE WHEN is_subscribed = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as unsubscribe_rate
FROM email_subscriptions
GROUP BY tenant_id;

-- Most common unsubscribe reasons
SELECT 
    unsubscribe_reason,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM email_subscriptions WHERE is_subscribed = 0), 2) as percentage
FROM email_subscriptions
WHERE is_subscribed = 0
GROUP BY unsubscribe_reason
ORDER BY count DESC;

-- Recent unsubscribes
SELECT email, unsubscribed_at, unsubscribe_reason, unsubscribe_feedback
FROM email_subscriptions
WHERE is_subscribed = 0
ORDER BY unsubscribed_at DESC
LIMIT 50;
```

---

## Troubleshooting

### Issue: Unsubscribe link not showing in emails

**Check**:
1. Is `$unsubscribeUrl` being passed to the email view?
2. Is the notification class in the marketing list in `EmailSubscriptionHelper`?
3. Is the email using `layouts/emails.blade.php` as the layout?

**Debug**:
```php
// In your Mailable's build() method
Log::info('Unsubscribe URL', ['url' => $this->unsubscribeUrl]);
```

### Issue: Users still receiving emails after unsubscribe

**Check**:
1. Is the unsubscribe record created? Check database
2. Is filtering enabled in `AppNotificationBuilder`?
3. Is the correct subscription type being checked?

**Debug**:
```php
$subscription = EmailSubscription::where('email', 'user@example.com')->first();
Log::info('Subscription status', [
    'email' => 'user@example.com',
    'is_subscribed' => $subscription->is_subscribed ?? 'No record'
]);
```

### Issue: Invalid token errors

**Check**:
1. Token is 64 characters and URL-safe
2. Token exists in database: `SELECT * FROM email_subscriptions WHERE unsubscribe_token = '...'`
3. Token wasn't already used (already unsubscribed)

---

## Future Enhancements

### Planned Features

1. **Preference Center**: Allow users to customize subscription types
2. **Email Frequency Control**: Let users choose email frequency
3. **Re-engagement Campaigns**: Win-back campaigns for unsubscribed users
4. **Batch Unsubscribe**: Allow users to manage multiple email addresses
5. **Integration with Bounce System**: Coordinate unsubscribe and bounce suppression

### Configuration Options

Consider adding to `config/mail.php`:

```php
'unsubscribe' => [
    'enabled' => env('MAIL_UNSUBSCRIBE_ENABLED', true),
    'link_text' => env('MAIL_UNSUBSCRIBE_TEXT', 'Unsubscribe from these emails'),
    'require_reason' => env('MAIL_UNSUBSCRIBE_REQUIRE_REASON', true),
    'allow_resubscribe' => env('MAIL_UNSUBSCRIBE_ALLOW_RESUBSCRIBE', true),
],
```

---

## Support & Maintenance

### Regular Tasks

- **Weekly**: Review unsubscribe statistics
- **Monthly**: Analyze unsubscribe reasons and improve email content
- **Quarterly**: Audit compliance with regulations
- **Annually**: Review and update privacy policy

### Key Metrics to Track

- Unsubscribe rate (should be < 2% for healthy list)
- Top unsubscribe reasons
- Resubscribe rate
- Time to unsubscribe (should be instant)
- Unsubscribe by email type/tenant

---

## Related Documentation

- [Email Bounce & Complaint Handling](./EMAIL_BOUNCE_COMPLAINT_SYSTEM.md)
- [AWS SES Setup](./AWS_SES_EMAIL_PRACTICES_KITCHNTABS.md)
- [Notification System](./DASH_NOTIFICATIONS_CATALOG.md)

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2024-12-22 | 1.0.0 | Initial implementation |
