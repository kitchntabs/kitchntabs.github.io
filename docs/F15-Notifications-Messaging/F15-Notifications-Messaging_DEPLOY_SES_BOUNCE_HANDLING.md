# Quick Deployment Guide: SES Bounce & Complaint Handling

## Prerequisites
- ✅ AWS Account with SES configured
- ✅ AWS CLI installed and configured
- ✅ Node.js 18.x installed (for CDK)
- ✅ Laravel backend accessible via public URL
- ✅ Database access for migrations

## Step 1: Environment Configuration

### Backend (.env)
Add these variables to `/Users/farandal/DASH-PW-PROJECT/dash-backend/.env`:

```env
# SES Webhook Configuration
WEBHOOK_SECRET=replace-with-secure-random-32-char-string

# Verify these are set correctly
MAIL_FROM_ADDRESS=noreply@yourdomain.com
MAIL_FROM_NAME="${APP_NAME}"
```

Generate secure webhook secret:
```bash
openssl rand -base64 32
```

### CDK Environment
Set these before deploying:

```bash
export ENV=production
export STACK_TYPE=infrastructure
export WEBHOOK_URL="https://api.yourdomain.com/api/webhooks/ses/notifications"
export WEBHOOK_SECRET="your-webhook-secret-from-env"
```

## Step 2: Deploy Database Migration

```bash
cd /Users/farandal/DASH-PW-PROJECT/dash-backend

# Run migration
php artisan migrate

# Verify table was created
php artisan db:table email_delivery_status
```

Expected output:
```
+---------------------+---------------------+----------+------+---------+----------------+
| Column              | Type                | Nullable | Key  | Default | Extra          |
+---------------------+---------------------+----------+------+---------+----------------+
| id                  | bigint unsigned     | NO       | PRI  |         | auto_increment |
| tenant_id           | bigint unsigned     | YES      | MUL  |         |                |
| email               | varchar(255)        | NO       | MUL  |         |                |
| status              | enum(...)           | NO       |      | active  |                |
| bounce_type         | enum(...)           | YES      |      |         |                |
| bounce_count        | int                 | NO       |      | 0       |                |
| last_bounce_at      | timestamp           | YES      |      |         |                |
| suppressed_at       | timestamp           | YES      |      |         |                |
| metadata            | json                | YES      |      |         |                |
| created_at          | timestamp           | YES      |      |         |                |
| updated_at          | timestamp           | YES      |      |         |                |
+---------------------+---------------------+----------+------+---------+----------------+
```

## Step 3: Deploy AWS Infrastructure (CDK)

```bash
cd /Users/farandal/DASH-PW-PROJECT/kitchntabs-ci-cdk

# Install dependencies (if not already done)
npm install

# Bootstrap CDK (first time only)
npx cdk bootstrap aws://ACCOUNT-ID/REGION --profile your-profile

# Deploy SES notification stack
ENV=production \
STACK_TYPE=infrastructure \
WEBHOOK_URL="https://api.yourdomain.com/api/webhooks/ses/notifications" \
WEBHOOK_SECRET="your-webhook-secret" \
npx cdk deploy KitchnTabsProductionSESNotifications --profile your-profile
```

### Expected CDK Outputs

After successful deployment, note these ARNs:

```
KitchnTabsProductionSESNotifications.BounceTopicArn = arn:aws:sns:us-east-1:123456789:kitchntabs-production-ses-bounces
KitchnTabsProductionSESNotifications.ComplaintTopicArn = arn:aws:sns:us-east-1:123456789:kitchntabs-production-ses-complaints
KitchnTabsProductionSESNotifications.LambdaFunctionArn = arn:aws:lambda:us-east-1:123456789:function:kitchntabs-production-ses-bounce-handler
KitchnTabsProductionSESNotifications.SetupInstructions = Configure SES identity notifications to use these SNS topics
```

**Save these ARNs** - you'll need them for the next step!

## Step 4: Configure SES Identity Notifications

### Option A: AWS Console (Recommended for First Time)

1. Go to [AWS SES Console](https://console.aws.amazon.com/ses/)
2. Navigate to **Verified identities**
3. Select your verified email or domain
4. Click **Notifications** tab
5. Click **Edit** in the "Feedback notifications" section

Configure:
- **Bounce notifications**:
  - Topic: Select `kitchntabs-production-ses-bounces`
  - Include original headers: ✅ Yes
  
- **Complaint notifications**:
  - Topic: Select `kitchntabs-production-ses-complaints`
  - Include original headers: ✅ Yes

6. Click **Save changes**

### Option B: AWS CLI (Faster for Multiple Identities)

```bash
# Set variables from CDK outputs
BOUNCE_TOPIC_ARN="arn:aws:sns:region:account:kitchntabs-production-ses-bounces"
COMPLAINT_TOPIC_ARN="arn:aws:sns:region:account:kitchntabs-production-ses-complaints"
IDENTITY="noreply@yourdomain.com"  # Your verified email/domain

# Configure bounce notifications
aws ses set-identity-notification-topic \
  --identity "$IDENTITY" \
  --notification-type Bounce \
  --sns-topic "$BOUNCE_TOPIC_ARN" \
  --profile your-profile

# Configure complaint notifications
aws ses set-identity-notification-topic \
  --identity "$IDENTITY" \
  --notification-type Complaint \
  --sns-topic "$COMPLAINT_TOPIC_ARN" \
  --profile your-profile

# Enable original headers (recommended)
aws ses set-identity-headers-in-notifications-enabled \
  --identity "$IDENTITY" \
  --notification-type Bounce \
  --enabled \
  --profile your-profile

aws ses set-identity-headers-in-notifications-enabled \
  --identity "$IDENTITY" \
  --notification-type Complaint \
  --enabled \
  --profile your-profile

# Verify configuration
aws ses get-identity-notification-attributes \
  --identities "$IDENTITY" \
  --profile your-profile
```

Expected output:
```json
{
  "NotificationAttributes": {
    "noreply@yourdomain.com": {
      "BounceTopic": "arn:aws:sns:...:kitchntabs-production-ses-bounces",
      "ComplaintTopic": "arn:aws:sns:...:kitchntabs-production-ses-complaints",
      "HeadersInBounceNotificationsEnabled": true,
      "HeadersInComplaintNotificationsEnabled": true,
      "ForwardingEnabled": false
    }
  }
}
```

## Step 5: Test the Integration

### Test 1: Hard Bounce

```bash
# Send test email using SES simulator
curl -X POST https://api.yourdomain.com/api/test-notification \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "bounce@simulator.amazonses.com",
    "type": "test"
  }'
```

**Expected Flow**:
1. ✉️ Email sent via SES
2. ⚠️ SES generates bounce notification
3. 📢 SNS publishes to bounce topic
4. ⚡ Lambda receives and processes
5. 🔗 Lambda POSTs to webhook
6. 💾 Database record created
7. 🚫 Future emails to this address blocked

**Verify**:
```bash
# Check database
mysql -u user -p database -e "SELECT * FROM email_delivery_status WHERE email = 'bounce@simulator.amazonses.com';"

# Expected result:
# +----+-----------+------------------------------------+--------------+-------------+--------------+---------------------+---------------------+----------+
# | id | tenant_id | email                              | status       | bounce_type | bounce_count | last_bounce_at      | suppressed_at       | metadata |
# +----+-----------+------------------------------------+--------------+-------------+--------------+---------------------+---------------------+----------+
# | 1  | NULL      | bounce@simulator.amazonses.com     | bounced_hard | permanent   | 1            | 2024-12-22 10:30:00 | 2024-12-22 10:30:00 | {...}    |
# +----+-----------+------------------------------------+--------------+-------------+--------------+---------------------+---------------------+----------+
```

### Test 2: Complaint

```bash
# Send to complaint simulator
curl -X POST https://api.yourdomain.com/api/test-notification \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "complaint@simulator.amazonses.com",
    "type": "test"
  }'

# Wait for notification (can take 1-2 minutes)

# Check database
mysql -u user -p database -e "SELECT * FROM email_delivery_status WHERE email = 'complaint@simulator.amazonses.com';"
```

### Test 3: Email Suppression

```bash
# Try to send another email to bounced address
curl -X POST https://api.yourdomain.com/api/test-notification \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "bounce@simulator.amazonses.com",
    "type": "test"
  }'

# Email should be filtered out - check logs
tail -f /path/to/dash-backend/storage/logs/laravel.log | grep "Filtered suppressed emails"
```

Expected log:
```
[2024-12-22 10:35:00] local.INFO: Filtered suppressed emails from tenant users {"tenant_id":1,"original_count":5,"filtered_count":4,"suppressed_count":1}
```

## Step 6: Monitor Logs

### Lambda Logs (CloudWatch)
```bash
# Tail Lambda logs in real-time
aws logs tail /aws/lambda/kitchntabs-production-ses-bounce-handler \
  --follow \
  --profile your-profile
```

### Laravel Logs
```bash
cd /Users/farandal/DASH-PW-PROJECT/dash-backend

# Watch all logs
tail -f storage/logs/laravel.log

# Filter for bounce-related logs
tail -f storage/logs/laravel.log | grep -E "EmailBounceService|SesWebhookController|Filtered suppressed"
```

## Step 7: Verify API Endpoints

### Check Email Status
```bash
curl -X GET https://api.yourdomain.com/api/webhooks/ses/check-email/bounce@simulator.amazonses.com \
  -H "Authorization: Bearer YOUR_SANCTUM_TOKEN"
```

Expected response:
```json
{
  "email": "bounce@simulator.amazonses.com",
  "is_suppressed": true,
  "status": "bounced_hard",
  "bounce_type": "permanent",
  "bounce_count": 1,
  "last_bounce_at": "2024-12-22T10:30:00.000000Z",
  "suppressed_at": "2024-12-22T10:30:00.000000Z"
}
```

### Get Statistics
```bash
curl -X GET "https://api.yourdomain.com/api/webhooks/ses/statistics?tenant_id=1" \
  -H "Authorization: Bearer YOUR_SANCTUM_TOKEN"
```

## Troubleshooting Quick Fixes

### Issue: Migration Fails
```bash
# Check if table already exists
php artisan db:show email_delivery_status

# If exists, rollback and re-run
php artisan migrate:rollback --step=1
php artisan migrate
```

### Issue: CDK Deploy Fails
```bash
# Check CDK version
npx cdk --version  # Should be >= 2.100.0

# Update if needed
npm install -g aws-cdk

# Check AWS credentials
aws sts get-caller-identity --profile your-profile

# Re-run deployment with verbose logging
npx cdk deploy KitchnTabsProductionSESNotifications --verbose --profile your-profile
```

### Issue: Lambda Not Receiving Messages
```bash
# Check SNS subscription status
aws sns list-subscriptions --profile your-profile | grep ses-bounce-handler

# Expected output: "Protocol": "lambda", "SubscriptionArn": "arn:aws:sns:..."

# If missing, manually subscribe (CDK should have done this)
aws sns subscribe \
  --topic-arn "$BOUNCE_TOPIC_ARN" \
  --protocol lambda \
  --notification-endpoint "$LAMBDA_ARN" \
  --profile your-profile
```

### Issue: Webhook Returns 401
```bash
# Check Lambda environment variables
aws lambda get-function-configuration \
  --function-name kitchntabs-production-ses-bounce-handler \
  --profile your-profile \
  --query 'Environment.Variables'

# Verify WEBHOOK_SECRET matches Laravel .env
grep WEBHOOK_SECRET /path/to/dash-backend/.env

# If mismatch, update Lambda
aws lambda update-function-configuration \
  --function-name kitchntabs-production-ses-bounce-handler \
  --environment "Variables={WEBHOOK_URL=https://api.yourdomain.com/api/webhooks/ses/notifications,WEBHOOK_SECRET=correct-secret}" \
  --profile your-profile
```

### Issue: Bounces Not Recorded
```bash
# Test webhook directly
curl -X POST https://api.yourdomain.com/api/webhooks/ses/notifications \
  -H "X-Webhook-Secret: your-webhook-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "notificationType": "Bounce",
    "bounce": {
      "bounceType": "Permanent",
      "bouncedRecipients": [
        {"emailAddress": "test@example.com"}
      ]
    }
  }'

# Should return 200 OK

# Check Laravel logs for errors
tail -50 storage/logs/laravel.log
```

## Health Check Commands

Run these periodically to ensure everything is working:

```bash
# 1. Check Lambda is running
aws lambda invoke \
  --function-name kitchntabs-production-ses-bounce-handler \
  --payload '{"test": true}' \
  /tmp/lambda-response.json \
  --profile your-profile

# 2. Check database has records
echo "SELECT COUNT(*) as total_records FROM email_delivery_status;" | mysql -u user -p database

# 3. Check suppressed emails count
echo "SELECT COUNT(*) as suppressed FROM email_delivery_status WHERE status IN ('bounced_hard', 'complained', 'suppressed');" | mysql -u user -p database

# 4. Check Lambda errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=kitchntabs-production-ses-bounce-handler \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 3600 \
  --statistics Sum \
  --profile your-profile
```

## Rollback Procedure

If something goes wrong:

### 1. Disable SES Notifications
```bash
# Remove SNS topics from SES identity
aws ses set-identity-notification-topic \
  --identity "$IDENTITY" \
  --notification-type Bounce \
  --profile your-profile

aws ses set-identity-notification-topic \
  --identity "$IDENTITY" \
  --notification-type Complaint \
  --profile your-profile
```

### 2. Remove Suppression Logic
```bash
# Temporarily disable filtering in AppNotificationBuilder.php
# Comment out the filterSuppressedEmails() calls at lines ~305, ~465
# Or set a feature flag in config/notifications.php
```

### 3. Destroy CDK Stack
```bash
npx cdk destroy KitchnTabsProductionSESNotifications --profile your-profile
```

### 4. Rollback Migration
```bash
php artisan migrate:rollback --step=1
```

## Next Steps After Deployment

1. ✅ **Monitor for 24 hours**: Watch logs for any errors
2. ✅ **Test with real email**: Send to a real address and verify
3. ✅ **Document procedures**: Update team wiki with access info
4. ✅ **Set up alerts**: CloudWatch alarms for Lambda errors
5. ✅ **Review monthly**: Check bounce rates and suppression list

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  SES BOUNCE HANDLING - QUICK REFERENCE                      │
├─────────────────────────────────────────────────────────────┤
│  Lambda Function:                                           │
│    kitchntabs-production-ses-bounce-handler                 │
│                                                             │
│  SNS Topics:                                                │
│    - kitchntabs-production-ses-bounces                      │
│    - kitchntabs-production-ses-complaints                   │
│                                                             │
│  Webhook URL:                                               │
│    POST /api/webhooks/ses/notifications                     │
│                                                             │
│  Admin Endpoints:                                           │
│    GET  /api/webhooks/ses/check-email/{email}              │
│    POST /api/webhooks/ses/remove-suppression               │
│    GET  /api/webhooks/ses/statistics                       │
│                                                             │
│  Database:                                                  │
│    Table: email_delivery_status                            │
│                                                             │
│  Logs:                                                      │
│    Lambda: /aws/lambda/...-ses-bounce-handler              │
│    Laravel: storage/logs/laravel.log                       │
│                                                             │
│  Test Addresses:                                            │
│    bounce@simulator.amazonses.com                          │
│    complaint@simulator.amazonses.com                       │
└─────────────────────────────────────────────────────────────┘
```

---

**Deployment Time**: ~15-20 minutes  
**Last Updated**: 2024-12-22  
**Status**: ✅ Ready for Production
