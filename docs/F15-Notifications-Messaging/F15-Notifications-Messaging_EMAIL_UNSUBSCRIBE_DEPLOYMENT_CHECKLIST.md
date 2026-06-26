# Email Unsubscribe System - Deployment Checklist

## Pre-Deployment Verification

### ✅ Files Created
- [x] Migration: `2024_12_22_000002_create_email_subscriptions_table.php`
- [x] Model: `EmailSubscription.php`
- [x] Controller: `UnsubscribeController.php`
- [x] Routes: `unsubscribe_routes.php`
- [x] Helper: `EmailSubscriptionHelper.php`
- [x] Views: 5 blade templates in `unsubscribe/` directory
- [x] Updated: `AppNotificationBuilder.php`
- [x] Updated: `layouts/emails.blade.php`

### ✅ Documentation
- [x] Complete system documentation
- [x] Jumpseller implementation guide
- [x] Implementation summary
- [x] This deployment checklist

---

## Deployment Steps

### Step 1: Verify Routes Registration

**File to modify**: `domain/routes/api.php`

Add this line if not already present:

```php
require __DIR__ . '/unsubscribe_routes.php';
```

**Verify**:
```bash
php artisan route:list | grep unsubscribe
```

Expected output:
```
GET|HEAD  unsubscribe/{token} ............... unsubscribe.show
POST      unsubscribe/{token} ............... unsubscribe.process
POST      unsubscribe/{token}/resubscribe ... unsubscribe.resubscribe
GET|HEAD  api/subscriptions/statistics ...... subscriptions.statistics
```

---

### Step 2: Run Database Migration

```bash
cd dash-backend

# Check migration is listed
php artisan migrate:status

# Run migration
php artisan migrate

# Verify table was created
php artisan tinker
>>> Schema::hasTable('email_subscriptions')
=> true

>>> DB::table('email_subscriptions')->count()
=> 0

>>> exit
```

**Rollback if needed**:
```bash
php artisan migrate:rollback --step=1
```

---

### Step 3: Update Jumpseller Email Class

**File to modify**: `domain/app/Mail/MarketplaceOrderUpdateMail.php`

**Changes needed**:

1. Add imports at top:
```php
use App\AppNotifications\EmailSubscriptionHelper;
use Domain\App\Models\Common\EmailSubscription;
```

2. Add property:
```php
public $unsubscribeUrl;
```

3. Add to constructor (at the end):
```php
// Get customer email
$customerEmail = $order->customer_email 
    ?? data_get($order->data, 'customer.email') 
    ?? data_get($order->billing_address, 'email')
    ?? null;

// Generate unsubscribe URL
if ($customerEmail) {
    $this->unsubscribeUrl = EmailSubscriptionHelper::getUnsubscribeUrl(
        $customerEmail,
        $order->tenant_id,
        EmailSubscription::TYPE_MARKETING
    );
}
```

4. Update build() method:
```php
public function build()
{
    return $this->subject($this->title)
        ->view('emails.marketplace-order-update')
        ->with(['unsubscribeUrl' => $this->unsubscribeUrl]);
}
```

**Reference**: See `JUMPSELLER_UNSUBSCRIBE_IMPLEMENTATION.md` for complete example

---

### Step 4: Clear Caches

```bash
# Clear all caches
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# Optimize for production
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

---

### Step 5: Test Functionality

#### 5.1 Send Test Email

```bash
php artisan tinker
```

```php
// Get a real order with customer email
$order = Domain\App\Models\Order\Order::whereNotNull('customer_email')->latest()->first();

// Or use test data
$order = Domain\App\Models\Order\Order::find(YOUR_ORDER_ID);

// Send test email to yourself
Mail::to('your-email@example.com')->send(
    new Domain\App\Mail\MarketplaceOrderUpdateMail($order)
);

// Check subscription was created
$sub = Domain\App\Models\Common\EmailSubscription::where('email', 'your-email@example.com')->first();

echo "Subscription created: " . ($sub ? 'YES' : 'NO') . "\n";
echo "Token: " . ($sub ? $sub->unsubscribe_token : 'N/A') . "\n";
echo "URL: " . ($sub ? $sub->getUnsubscribeUrl() : 'N/A') . "\n";

exit
```

#### 5.2 Check Email

1. Open the test email in your inbox
2. Scroll to footer
3. Verify "Unsubscribe from these emails" link is present
4. Link should be: `https://yourdomain.com/unsubscribe/{TOKEN}`

#### 5.3 Test Unsubscribe Flow

1. Click unsubscribe link in email
2. Should see confirmation page with:
   - Your email address
   - Reason dropdown
   - Feedback textarea
   - Confirm/Cancel buttons
3. Select reason "too_many_emails"
4. Add feedback: "Testing unsubscribe"
5. Click "Unsubscribe"
6. Should see success page

#### 5.4 Verify Database

```bash
php artisan tinker
```

```php
$sub = Domain\App\Models\Common\EmailSubscription::where('email', 'your-email@example.com')->first();

echo "Is subscribed: " . ($sub->is_subscribed ? 'YES' : 'NO') . "\n";
echo "Unsubscribed at: " . $sub->unsubscribed_at . "\n";
echo "Reason: " . $sub->unsubscribe_reason . "\n";
echo "Feedback: " . $sub->unsubscribe_feedback . "\n";

exit
```

Expected output:
```
Is subscribed: NO
Unsubscribed at: 2024-12-22 10:30:45
Reason: too_many_emails
Feedback: Testing unsubscribe
```

#### 5.5 Test Filtering

```bash
php artisan tinker
```

```php
// Try to send another email
Mail::to('your-email@example.com')->send(
    new Domain\App\Mail\MarketplaceOrderUpdateMail($order)
);

// Check logs - should show email was filtered
exit
```

Check `storage/logs/laravel.log`:
```
[INFO] Filtering unsubscribed email from notification {"user_id":123,"email":"your-email@example.com"}
```

#### 5.6 Test Resubscribe

1. Visit: `https://yourdomain.com/unsubscribe/{TOKEN}`
2. Should see "Already unsubscribed" page
3. Look for resubscribe option (if implemented)
4. Or test via API:

```bash
curl -X POST "https://yourdomain.com/unsubscribe/{TOKEN}/resubscribe" \
  -H "Content-Type: application/json"
```

---

### Step 6: Test Statistics Endpoint

```bash
curl -X GET "https://yourdomain.com/api/subscriptions/statistics" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Accept: application/json"
```

Expected response:
```json
{
    "total_subscriptions": 1,
    "subscribed": 0,
    "unsubscribed": 1,
    "by_type": {
        "marketing": 1
    },
    "unsubscribe_reasons": {
        "too_many_emails": 1
    }
}
```

---

## Production Deployment

### Environment Variables

No new environment variables required. Uses existing:
- `APP_URL` - for generating unsubscribe URLs
- `MAIL_FROM_ADDRESS` - already configured

### Monitoring

#### Set Up Alerts

Monitor these metrics daily:
1. Unsubscribe rate (should be < 2%)
2. Top unsubscribe reasons
3. Failed unsubscribe attempts (invalid tokens)

#### Log Monitoring

Watch `storage/logs/laravel.log` for:
```
[INFO] User unsubscribed
[INFO] Filtering unsubscribed email
[ERROR] Failed to get unsubscribe token
```

#### Database Monitoring

Daily query:
```sql
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN is_subscribed = 0 THEN 1 ELSE 0 END) as unsubscribed,
    ROUND(SUM(CASE WHEN is_subscribed = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as rate
FROM email_subscriptions;
```

---

## Post-Deployment

### Day 1
- [x] Verify unsubscribe links appear in emails
- [x] Check first unsubscribe works correctly
- [x] Monitor logs for errors

### Week 1
- [x] Review unsubscribe rate (should be < 2%)
- [x] Check top unsubscribe reasons
- [x] Verify filtering is working
- [x] Monitor any error logs

### Week 2
- [x] Analyze feedback from unsubscribe reasons
- [x] Adjust email frequency if needed
- [x] Review and respond to feedback

### Month 1
- [x] Full statistics review
- [x] Compare deliverability rates
- [x] Adjust strategy based on data

---

## Rollback Plan

If issues arise:

### Quick Rollback

1. **Disable filtering temporarily**:

Edit `app/AppNotifications/AppNotificationBuilder.php`, comment out subscription check:

```php
// Temporarily disable unsubscribe filtering
// if (!$isSubscribed) {
//     Log::channel('notifications')->info('Filtering unsubscribed email');
//     return false;
// }
```

2. **Clear caches**:
```bash
php artisan config:clear
php artisan route:clear
```

### Full Rollback

```bash
# Rollback migration
php artisan migrate:rollback --step=1

# Remove route registration
# Edit domain/routes/api.php and comment out:
# require __DIR__ . '/unsubscribe_routes.php';

# Clear caches
php artisan config:clear
php artisan route:clear
```

---

## Troubleshooting

### Issue: Unsubscribe link not showing

**Check**:
1. Is `$unsubscribeUrl` set in Mailable?
2. Is token generation working?
3. Is email using `layouts/emails.blade.php`?

**Debug**:
```php
// Add to MarketplaceOrderUpdateMail constructor
Log::info('Unsubscribe URL generated', [
    'order_id' => $order->id,
    'customer_email' => $customerEmail,
    'url' => $this->unsubscribeUrl,
]);
```

### Issue: Invalid token errors

**Check database**:
```sql
SELECT * FROM email_subscriptions WHERE unsubscribe_token = 'YOUR_TOKEN';
```

### Issue: Users still receiving emails

**Check subscription status**:
```php
$sub = EmailSubscription::where('email', 'user@example.com')->first();
var_dump($sub->is_subscribed);
```

**Check filtering**:
```bash
# Check logs for filtering messages
tail -f storage/logs/laravel.log | grep "Filtering unsubscribed"
```

---

## Success Criteria

- ✅ Migration runs successfully
- ✅ Routes are accessible
- ✅ Unsubscribe link appears in emails
- ✅ Unsubscribe flow works end-to-end
- ✅ Users stop receiving emails after unsubscribe
- ✅ Database records are created correctly
- ✅ Statistics endpoint returns data
- ✅ No errors in logs

---

## Support Contacts

- **Technical Issues**: Check logs first, then documentation
- **Database Issues**: Verify migration ran correctly
- **Integration Issues**: Review `JUMPSELLER_UNSUBSCRIBE_IMPLEMENTATION.md`
- **Compliance Questions**: Review CAN-SPAM/GDPR checklist in documentation

---

## Documentation Links

- [Full System Documentation](./EMAIL_UNSUBSCRIBE_SYSTEM.md)
- [Jumpseller Implementation](./JUMPSELLER_UNSUBSCRIBE_IMPLEMENTATION.md)
- [Implementation Summary](./EMAIL_UNSUBSCRIBE_IMPLEMENTATION_SUMMARY.md)
- [AWS SES Best Practices](./AWS_SES_EMAIL_PRACTICES_KITCHNTABS.md)
- [Bounce Handling System](./EMAIL_BOUNCE_COMPLAINT_SYSTEM.md)

---

**Version**: 1.0.0  
**Date**: December 22, 2024  
**Status**: Ready for Deployment  
**Estimated Time**: 30-45 minutes for full deployment and testing
