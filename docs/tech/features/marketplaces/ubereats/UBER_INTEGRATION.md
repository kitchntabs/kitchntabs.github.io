## 🍔 Uber Integration Testing Guide for POS

Based on my investigation, here's what I found about the Uber integration architecture and how to test it:

### **Architecture Overview**

```
Uber Eats App → Uber API → Webhook → Your Backend → Order → Tab → POS Notification
```

### **Key Components**

| Component | Location | Purpose |
|-----------|----------|---------|
| `UberService.php` | `domain/app/Services/ECommerce/Marketplaces/Uber/` | Main service handling products/menu publishing |
| WebhookTrait.php | WebhookTrait.php | Processes all webhook events |
| `OrderTrait.php` | `ServiceTraits/OrderTrait.php` | Order confirmation/rejection |
| OAuthClient.php | OAuthClient.php | Authentication with Uber |
| MarketplaceController.php | Controller | Receives webhooks at endpoint |

### **Webhook Endpoint**

The webhook URL for Uber is:
```
POST /api/ecommerce/marketplace/{marketplace_id}/webhook/order
```

For example: `https://api.kitchntabs.com/api/ecommerce/marketplace/2/webhook/order`

### **Uber Webhook Events Handled**

| Event Type | Method | Description |
|------------|--------|-------------|
| `orders.notification` | `processOrderNotification()` | New order received |
| `orders.cancel` | `processOrderCancel()` | Order cancelled by Uber/customer |
| `orders.scheduled.notification` | `processScheduledOrderNotification()` | Scheduled order notification |
| `orders.release` | `processOrderRelease()` | Courier approaching (geo-fence) |
| `orders.failure` | `processOrderFailure()` | Order failed |
| `orders.fulfillment_issues.resolved` | `processFulfillmentIssuesResolved()` | Issues resolved |
| `delivery.state_changed` | `processDeliveryStateChanged()` | Delivery status change |

### **Order Flow**

1. **Uber sends webhook** → `POST /api/ecommerce/marketplace/{id}/webhook/order`
2. **`MarketplaceController::webhook()`** → Routes to appropriate service
3. **`UberService::handleWebhook()`** → Delegates to `WebhookTrait::handleUberWebhook()`
4. **`processOrderNotification()`** → Fetches order details from Uber API
5. **`createOrUpdateOrderFromUberData()`** → Creates `Order` model + `OrderProduct` records
6. **`createTabForOrder()`** → Creates `Tab` with status `STATUS_CREATED`
7. **`TabsNotificationService::handleStatusChange()`** → Sends FCM notification to POS

### **Testing Steps**

#### **Step 1: Verify Marketplace Configuration**

Check your marketplace record in the database:
```sql
SELECT id, name, connection_params, active 
FROM marketplaces 
WHERE id = {your_marketplace_id};
```

Required `connection_params`:
- `access_token` - OAuth token from Uber
- `store_id` - Your Uber Eats store ID
- `webhook_token` (optional) - For signature verification

#### **Step 2: Test Connection**

In the admin interface, go to your Uber marketplace and run the connection tests:
- **stores** - Lists all your Uber stores
- **store** - Gets specific store details
- **store_status** - Gets store online/offline status
- **orders** - Lists recent orders
- **menus** - Gets current menu

#### **Step 3: Simulate a Webhook (Manual Testing)**

You can simulate an Uber webhook using curl:

```bash
curl -X POST "https://api.kitchntabs.com/api/ecommerce/marketplace/{marketplace_id}/webhook/order" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "orders.notification",
    "event_id": "test-event-123",
    "resource_href": "https://api.uber.com/v1/delivery/order/{your_test_order_id}",
    "meta": {
      "resource_id": "test-order-123"
    }
  }'
```

**Note:** The webhook fetches order details from Uber API using the `resource_href`, so the order must exist in Uber.

#### **Step 4: Check Logs**

Monitor Laravel logs for webhook processing:
```bash
tail -f storage/logs/laravel.log | grep -i uber
```

Look for:
- `Processing Uber webhook event`
- `Creating or updating order from Uber data`
- `Tab created for order`

#### **Step 5: Verify Tab Creation**

After a webhook is processed, check:
```sql
SELECT t.*, o.source_id as uber_order_id 
FROM tabs t 
JOIN orders o ON t.order_id = o.id AND t.order_type = 'Domain\\App\\Models\\Order\\Order'
WHERE t.tenant_id = {your_tenant_id}
ORDER BY t.created_at DESC
LIMIT 5;
```

### **Real Testing with Uber Test Orders**

To test with real Uber orders:

1. **Enable Test Mode in Uber Dashboard** - Uber provides a sandbox/test environment
2. **Create Test Orders** - Use Uber's testing tools to simulate orders
3. **Configure Webhook URL** - Set your webhook URL in Uber Developer Portal

### **Order Confirmation from POS**

When the Tab is accepted in POS, it should call:
```
PUT /v1/delivery/order/{orderId}/accept
```

When rejected:
```
PUT /v1/delivery/order/{orderId}/deny
```

With reason codes: `OUT_OF_ITEMS`, `RESTAURANT_CLOSED`, `CANNOT_COMPLETE`




Based on the Uber support email you attached, here are the credentials and URLs to access the Uber Eats administration interface:

## 🔐 Uber Eats Test Store Credentials

### **Portal Access URL**
```
https://merchants.ubereats.com
```

### **Login Credentials**
| Field | Value |
|-------|-------|
| **Email** | Contact your account manager |
| **Password** | Contact your account manager |

### **Test Store Details**
- **Store Name**: PinoyWok Test Store (Chile)
- **Purpose**: Testing integration before production validation

---

## 📋 Next Steps from Uber

According to the email, you need to:

1. **Log in** to `https://merchants.ubereats.com` with the credentials above
2. **Configure the test store** with your menu items
3. **Test the integration** (webhooks, order flow, etc.)
4. **Schedule a validation call** with Uber once testing is complete

---

## 🔧 For Your Integration

Once you log in, you'll need to:

1. **Get the Store ID** - Find this in the store settings or URL
2. **Configure Webhook URL** - Set it to your backend:
   ```
   https://api.kitchntabs.com/api/ecommerce/marketplace/{marketplace_id}/webhook/order
   ```
3. **Test orders** - Create test orders to verify the full flow

Would you like me to help you:
1. Log the Store ID from your current marketplace configuration?
2. Check if there's an existing Uber marketplace record in your system?
3. Set up ngrok to expose your local backend for webhook testing?