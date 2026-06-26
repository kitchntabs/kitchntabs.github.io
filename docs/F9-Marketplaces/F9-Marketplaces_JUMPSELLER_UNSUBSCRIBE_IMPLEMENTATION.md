# Jumpseller Email Unsubscribe - Quick Implementation Guide

## Overview

This guide shows how to add unsubscribe functionality to Jumpseller marketplace order update emails.

---

## Current File: MarketplaceOrderUpdateMail.php

**Location**: `domain/app/Mail/MarketplaceOrderUpdateMail.php`

### Step 1: Add Unsubscribe Property

Add this property to the class:

```php
public $unsubscribeUrl;
```

### Step 2: Update Constructor

Add unsubscribe URL generation in the constructor:

```php
use App\AppNotifications\EmailSubscriptionHelper;
use Domain\App\Models\Common\EmailSubscription;

public function __construct(
    Order $order, 
    $title = null, 
    $orderMessage = null, 
    $status = null, 
    $statusColor = null,
    $secondaryMessage = null,
    $tenantData = null
) {
    // ... existing code ...
    
    // ADD THIS AT THE END OF CONSTRUCTOR:
    
    // Get customer email from order
    $customerEmail = $order->customer_email 
        ?? data_get($order->data, 'customer.email') 
        ?? data_get($order->billing_address, 'email')
        ?? null;
    
    // Generate unsubscribe URL if we have customer email
    if ($customerEmail) {
        $this->unsubscribeUrl = EmailSubscriptionHelper::getUnsubscribeUrl(
            $customerEmail,
            $order->tenant_id,
            EmailSubscription::TYPE_MARKETING
        );
    }
}
```

### Step 3: Pass to View

Update the `build()` method to pass the unsubscribe URL:

```php
public function build()
{
    return $this->subject($this->title)
        ->view('emails.marketplace-order-update')
        ->with([
            'unsubscribeUrl' => $this->unsubscribeUrl
        ]);
}
```

---

## Email Template

**Location**: `resources/views/emails/marketplace-order-update.blade.php`

The email already extends `layouts/emails.blade.php`, which now includes the unsubscribe link automatically if `$unsubscribeUrl` is set.

**No changes needed to the template!** The layout will handle it.

---

## Complete Modified File

Here's what the complete modified `MarketplaceOrderUpdateMail.php` should look like:

```php
<?php

namespace Domain\App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use Domain\App\Models\Order\Order;
use Carbon\Carbon;
use App\AppNotifications\EmailSubscriptionHelper;
use Domain\App\Models\Common\EmailSubscription;

class MarketplaceOrderUpdateMail extends Mailable
{
    use Queueable, SerializesModels;

    public $order;
    public $title;
    public $orderMessage;
    public $status;
    public $statusColor;
    public $secondaryMessage;
    public $estimatedArrival;
    public $trackingUrl;
    public $companyName;
    public $companyEmail;
    public $companyUrl;
    public $logoUrl;
    public $tenantData;
    public $unsubscribeUrl;  // NEW

    public function __construct(
        Order $order, 
        $title = null, 
        $orderMessage = null, 
        $status = null, 
        $statusColor = null,
        $secondaryMessage = null,
        $tenantData = null
    ) {
        $this->order = $order;
        
        // If tenantData is not provided, get it from the order
        $this->tenantData = $tenantData ?: $order->getTenantData();
        
        // Load order items with their product relationships
        $this->order->load(['items.product', 'items.modifiers.modifierOption']);

        // Set default values if not provided
        $this->title = $title ?? '¡Actualización de tu pedido!';
        $this->orderMessage = $orderMessage ?? 'te informamos que el estado de tu pedido ha cambiado.';
        $this->status = $status ?? $order->status;
        
        // Map status to colors
        $statusColors = [
            'CREATED' => '#6c757d',
            'SALE_NOTE_GENERATED' => '#007bff',
            'IN_PREPARATION' => '#fd7e14',
            'PREPARED' => '#17a2b8',
            'PICKED_UP' => '#6f42c1',
            'SCHEDULE_SHIPPING' => '#20c997',
            'SHIPPED' => '#28a745',
            'RETURNED' => '#dc3545',
            'NOT_SHIPPED' => '#dc3545',
        ];
        
        $this->statusColor = $statusColor ?? ($statusColors[$order->status] ?? '#5cb85c');
        
        // Calculate estimated arrival
        $this->estimatedArrival = isset($order->data['estimated_arrival']) 
            ? $order->data['estimated_arrival']
            : Carbon::now()->addMinutes(20)->format('d/m/Y H:i');
            
        // Set secondary message
        $this->secondaryMessage = $secondaryMessage ?? 
            'Tu pedido está siendo preparado. Te notificaremos cuando el repartidor haya recogido el pedido. Gracias!';
            
        // Set tracking URL
        $this->trackingUrl = "https://tracking.pinoywok.cl/{$order->id}";
        
        // Company info
        $this->companyName = data_get($this->tenantData, 'display_name', data_get($this->tenantData, 'name', config('app.name', 'PinoyWok')));
        $this->companyEmail = data_get($this->tenantData, 'contact_email', data_get($this->tenantData, 'email', config('mail.from.address')));
        $this->companyUrl = data_get($this->tenantData, 'website', 'https://www.pinoywok.cl');
        $this->logoUrl = data_get($this->tenantData, 'horizontal_logo_url', 'https://images.jumpseller.com/store/pinoywok1/store/logo/Dise_o_sin_t_tulo.png?1708271276');
        
        // NEW: Generate unsubscribe URL
        $customerEmail = $order->customer_email 
            ?? data_get($order->data, 'customer.email') 
            ?? data_get($order->billing_address, 'email')
            ?? null;
        
        if ($customerEmail) {
            $this->unsubscribeUrl = EmailSubscriptionHelper::getUnsubscribeUrl(
                $customerEmail,
                $order->tenant_id,
                EmailSubscription::TYPE_MARKETING
            );
        }
    }

    public function build()
    {
        return $this->subject($this->title)
            ->view('emails.marketplace-order-update')
            ->with([
                'unsubscribeUrl' => $this->unsubscribeUrl
            ]);
    }
}
```

---

## Testing

### 1. Run Migration

```bash
cd dash-backend
php artisan migrate
```

### 2. Register Routes

Add to `domain/routes/api.php` if not already there:

```php
require __DIR__ . '/unsubscribe_routes.php';
```

### 3. Send Test Email

```bash
php artisan tinker
```

```php
// Get a test order
$order = Domain\App\Models\Order\Order::latest()->first();

// Send test email
Mail::to('your-email@example.com')->send(
    new Domain\App\Mail\MarketplaceOrderUpdateMail($order)
);

// Check if subscription record was created
Domain\App\Models\Common\EmailSubscription::where('email', 'your-email@example.com')->first();
```

### 4. Test Unsubscribe Flow

1. Check your email inbox
2. Look for "Unsubscribe from these emails" link at the bottom
3. Click the link
4. Fill out the unsubscribe form
5. Confirm unsubscribe
6. Try sending another email - it should be filtered

### 5. Verify Database

```sql
-- Check subscription record
SELECT * FROM email_subscriptions 
WHERE email = 'your-email@example.com';

-- Check unsubscribe was recorded
SELECT email, is_subscribed, unsubscribe_reason, unsubscribed_at 
FROM email_subscriptions 
WHERE is_subscribed = 0;
```

---

## What Happens

### 1. First Email Sent
- EmailSubscription record created automatically
- Unique token generated (64 chars)
- Unsubscribe link added to email footer

### 2. Customer Clicks Unsubscribe
- Taken to `/unsubscribe/{token}` page
- Shown confirmation form with reason dropdown
- Can provide optional feedback

### 3. Customer Confirms
- Record updated: `is_subscribed = false`
- Timestamp, reason, feedback, IP recorded
- Shown success page

### 4. Next Email Attempt
- `AppNotificationBuilder` checks subscription status
- Email filtered out before sending
- Logged to `laravel.log`

---

## Monitoring

### Check Unsubscribe Rate

```php
use Domain\App\Models\Common\EmailSubscription;

$stats = [
    'total' => EmailSubscription::count(),
    'subscribed' => EmailSubscription::subscribed()->count(),
    'unsubscribed' => EmailSubscription::unsubscribed()->count(),
    'rate' => round(
        (EmailSubscription::unsubscribed()->count() / EmailSubscription::count()) * 100, 
        2
    ) . '%'
];

dd($stats);
```

### Top Unsubscribe Reasons

```sql
SELECT 
    unsubscribe_reason,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) 
        FROM email_subscriptions 
        WHERE is_subscribed = 0
    ), 2) as percentage
FROM email_subscriptions
WHERE is_subscribed = 0
GROUP BY unsubscribe_reason
ORDER BY count DESC;
```

---

## Troubleshooting

### Unsubscribe link not showing?

**Check**:
```php
// In MarketplaceOrderUpdateMail constructor
Log::info('Jumpseller email unsubscribe', [
    'order_id' => $order->id,
    'customer_email' => $customerEmail,
    'unsubscribe_url' => $this->unsubscribeUrl,
]);
```

### User still receiving emails after unsubscribe?

**Check subscription record**:
```php
$sub = EmailSubscription::where('email', 'user@example.com')->first();
dd([
    'exists' => $sub ? 'yes' : 'no',
    'is_subscribed' => $sub->is_subscribed ?? null,
    'unsubscribed_at' => $sub->unsubscribed_at ?? null,
]);
```

**Check if filtering is working**:
```php
// In AppNotificationBuilder
Log::channel('notifications')->info('Checking subscription', [
    'email' => $user->email,
    'is_subscribed' => EmailSubscriptionHelper::isSubscribed($user->email, $user->tenant_id)
]);
```

---

## Compliance Checklist

- ✅ Unsubscribe link in every marketing email
- ✅ One-click unsubscribe (no login required)
- ✅ Processed immediately (not 10 days later)
- ✅ Physical address in email footer (from tenant data)
- ✅ Clear identification of sender
- ✅ Audit trail with timestamps
- ✅ Privacy policy linked in footer
- ✅ Reason tracking for improvement

---

## Next Steps

1. **Monitor**: Watch unsubscribe rates and reasons
2. **Improve**: Adjust email frequency based on feedback
3. **Segment**: Consider different subscription types (order updates vs promotions)
4. **Re-engage**: Plan win-back campaigns for unsubscribed users
5. **Integrate**: Connect with customer support for manual unsubscribe requests

---

## Support

For issues or questions:
1. Check logs: `storage/logs/laravel.log`
2. Review database: `email_subscriptions` table
3. Test with real email address
4. Check [full documentation](./EMAIL_UNSUBSCRIBE_SYSTEM.md)
