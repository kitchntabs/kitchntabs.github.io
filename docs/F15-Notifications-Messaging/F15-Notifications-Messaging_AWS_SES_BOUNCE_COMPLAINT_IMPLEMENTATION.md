
# AWS SES Bounce & Complaint Handling - Implementation Summary

## Overview
Complete implementation of AWS SES bounce and complaint handling architecture with automatic email suppression to protect sender reputation.

## Architecture Components

### 1. Database Layer
**Migration**: `domain/database/migrations/2024_12_22_000001_create_email_delivery_status_table.php`

**Table Schema**: `email_delivery_status`
```sql
- id (bigint, PK)
- tenant_id (bigint, FK, nullable)
- email (varchar, indexed)
- status (enum: active, bounced_hard, bounced_soft, complained, suppressed)
- bounce_type (enum: null, permanent, transient, complaint)
- bounce_count (int, default 0)
- last_bounce_at (timestamp, nullable)
- suppressed_at (timestamp, nullable)
- metadata (json, nullable)
- timestamps
```

**Model**: `domain/app/Models/Common/EmailDeliveryStatus.php`
- Fillable fields: tenant_id, email, status, bounce_type, bounce_count, last_bounce_at, suppressed_at, metadata
- Status constants: ACTIVE, BOUNCED_HARD, BOUNCED_SOFT, COMPLAINED, SUPPRESSED
- Bounce type constants: PERMANENT, TRANSIENT, COMPLAINT
- Query scopes: suppressed(), active(), byTenant()
- Helper methods: shouldSuppress(), isActive(), incrementBounceCount()

### 2. Service Layer
**Service**: `domain/app/Services/Email/EmailBounceService.php`

**Key Methods**:
- `processBounce(array $bounceData)` - Process bounce notification from SES
- `processComplaint(array $complaintData)` - Process complaint notification from SES
- `shouldSuppressEmail(string $email, ?int $tenantId = null)` - Check if email should be suppressed
- `getSuppressionStatus(string $email, ?int $tenantId = null)` - Get detailed suppression info
- `removeSuppression(string $email, ?int $tenantId = null)` - Manual suppression removal
- `getTenantStatistics(int $tenantId)` - Get tenant email statistics

**Suppression Logic**:
- Hard bounces: Immediate suppression
- Soft bounces: Suppress after 3 attempts
- Complaints: Immediate suppression

### 3. AWS Infrastructure (CDK)
**Template**: `kitchntabs-ci-cdk/lib/templates/ses-notification-template.ts`

**Resources Created**:
1. **SNS Topics**:
   - `{project}-{env}-ses-bounces` - For bounce notifications
   - `{project}-{env}-ses-complaints` - For complaint notifications

2. **Lambda Function**: `{project}-{env}-ses-bounce-handler`
   - Runtime: Node.js 18.x
   - Handler: index.handler
   - Environment variables: WEBHOOK_URL, WEBHOOK_SECRET
   - Permissions: CloudWatch Logs
   - Subscribed to both SNS topics

3. **CloudWatch Log Groups**:
   - `/aws/lambda/{project}-{env}-ses-bounce-handler`
   - Retention: 7 days

**Lambda Code**: `kitchntabs-ci-cdk/lambda/ses-bounce-handler/index.js`
- Parses SNS messages
- Extracts bounce/complaint data
- POSTs to Laravel webhook with authentication

### 4. API Layer
**Controller**: `domain/app/Http/Controllers/API/Webhooks/SesWebhookController.php`

**Endpoints**:
1. `POST /api/webhooks/ses/notifications` - Public webhook (X-Webhook-Secret authentication)
2. `GET /api/webhooks/ses/check-email/{email}` - Check email status (auth:sanctum)
3. `POST /api/webhooks/ses/remove-suppression` - Remove suppression (auth:sanctum)
4. `GET /api/webhooks/ses/statistics` - Get statistics (auth:sanctum)

**Routes**: `domain/routes/api/webhooks_ses.php`
- Auto-loaded by Laravel's route service provider

### 5. Notification Integration
**Updated**: `app/AppNotifications/AppNotificationBuilder.php`

**Changes**:
1. Added import: `use Domain\App\Services\Email\EmailBounceService;`
2. Created helper method: `filterSuppressedEmails(Collection $users): Collection`
3. Applied filtering in 3 locations:
   - Line ~305: Tenant user notifications (channel scope)
   - Line ~465: Role-based notifications (database channel)
   - Line ~475: Already had filtering in place

**Filtering Logic**:
```php
private static function filterSuppressedEmails(Collection $users): Collection
{
    if ($users->isEmpty()) {
        return $users;
    }
    
    $bounceService = app(EmailBounceService::class);
    $emails = $users->pluck('email')->filter()->unique()->values();
    
    if ($emails->isEmpty()) {
        return $users;
    }
    
    $suppressedEmails = [];
    foreach ($emails as $email) {
        if ($bounceService->shouldSuppressEmail($email)) {
            $suppressedEmails[] = $email;
        }
    }
    
    if (empty($suppressedEmails)) {
        return $users;
    }
    
    return $users->reject(function ($user) use ($suppressedEmails) {
        return in_array($user->email, $suppressedEmails);
    });
}
```

## Deployment Steps

### 1. Deploy Database Migration
```bash
cd /Users/farandal/DASH-PW-PROJECT/dash-backend
php artisan migrate
```

### 2. Configure Environment Variables
Add to `.env`:
```env
# Webhook authentication
WEBHOOK_SECRET=your-secure-random-string-here

# For CDK deployment
WEBHOOK_URL=https://your-api-domain.com/api/webhooks/ses/notifications
```

### 3. Deploy CDK Stack
```bash
cd /Users/farandal/DASH-PW-PROJECT/kitchntabs-ci-cdk

# Set environment variables
export ENV=production
export STACK_TYPE=infrastructure
export WEBHOOK_URL="https://your-api-domain.com/api/webhooks/ses/notifications"
export WEBHOOK_SECRET="your-secure-random-string-here"

# Deploy
npm run cdk:deploy

# Or manually
npx cdk deploy KitchnTabsProductionSESNotifications --profile your-aws-profile
```

### 4. Configure SES Identity Notifications
After CDK deployment, note the SNS topic ARNs from the outputs, then:

**Option A: AWS Console**
1. Go to SES > Verified Identities
2. Select your email/domain
3. Go to "Notifications" tab
4. Configure:
   - Bounce notifications: Select SNS topic `{project}-{env}-ses-bounces`
   - Complaint notifications: Select SNS topic `{project}-{env}-ses-complaints`
   - Include original headers: Yes (recommended)

**Option B: AWS CLI**
```bash
# Get topic ARNs from CDK outputs
BOUNCE_TOPIC_ARN="arn:aws:sns:region:account:project-env-ses-bounces"
COMPLAINT_TOPIC_ARN="arn:aws:sns:region:account:project-env-ses-complaints"
IDENTITY="your-verified-email@domain.com"

# Configure bounce notifications
aws ses set-identity-notification-topic \
  --identity $IDENTITY \
  --notification-type Bounce \
  --sns-topic $BOUNCE_TOPIC_ARN

# Configure complaint notifications
aws ses set-identity-notification-topic \
  --identity $IDENTITY \
  --notification-type Complaint \
  --sns-topic $COMPLAINT_TOPIC_ARN

# Enable headers (optional but recommended)
aws ses set-identity-headers-in-notifications-enabled \
  --identity $IDENTITY \
  --notification-type Bounce \
  --enabled

aws ses set-identity-headers-in-notifications-enabled \
  --identity $IDENTITY \
  --notification-type Complaint \
  --enabled
```

### 5. Test the Flow

**Send Test Email**:
```bash
# Use SES simulator addresses for testing
curl -X POST https://your-api-domain.com/api/test-email \
  -H "Authorization: Bearer your-token" \
  -d '{"to": "bounce@simulator.amazonses.com"}'
```

**Check Logs**:
```bash
# Lambda logs
aws logs tail /aws/lambda/project-env-ses-bounce-handler --follow

# Laravel logs
tail -f /path/to/dash-backend/storage/logs/laravel.log
```

**Verify Database**:
```sql
SELECT * FROM email_delivery_status WHERE email = 'bounce@simulator.amazonses.com';
```

## Testing Scenarios

### 1. Hard Bounce Test
```bash
# Send to SES simulator bounce address
to: bounce@simulator.amazonses.com

# Expected result:
# - Email sent
# - SES generates bounce notification
# - SNS publishes to bounce topic
# - Lambda receives message
# - Lambda POSTs to webhook
# - EmailBounceService processes bounce
# - email_delivery_status record created with status: bounced_hard
# - Future emails to this address filtered out
```

### 2. Complaint Test
```bash
# Send to SES simulator complaint address
to: complaint@simulator.amazonses.com

# Expected result:
# - Email sent
# - User manually marks as spam (simulated)
# - SES generates complaint notification
# - SNS publishes to complaint topic
# - Lambda receives message
# - Lambda POSTs to webhook
# - EmailBounceService processes complaint
# - email_delivery_status record created with status: complained
# - Future emails to this address filtered out
```

### 3. Soft Bounce Test
```bash
# Send to temporary failure address (simulated)
# Repeat 3 times

# Expected result:
# - First 2 bounces: status remains active, bounce_count incremented
# - 3rd bounce: status changes to suppressed
# - Future emails filtered out
```

## Monitoring

### CloudWatch Metrics
- Lambda invocations: `/aws/lambda/{project}-{env}-ses-bounce-handler`
- Lambda errors: Check CloudWatch Logs for exceptions
- Lambda duration: Monitor for performance issues

### Laravel Logs
```bash
# Bounce processing logs
grep "EmailBounceService" storage/logs/laravel.log

# Webhook logs
grep "SesWebhookController" storage/logs/laravel.log

# Notification filtering logs
grep "Filtered suppressed emails" storage/logs/laravel.log
```

### Database Queries
```sql
-- Check suppressed emails
SELECT email, status, bounce_count, last_bounce_at 
FROM email_delivery_status 
WHERE status IN ('bounced_hard', 'complained', 'suppressed');

-- Tenant statistics
SELECT tenant_id, status, COUNT(*) as count 
FROM email_delivery_status 
GROUP BY tenant_id, status;

-- Recent bounces
SELECT * FROM email_delivery_status 
WHERE last_bounce_at >= NOW() - INTERVAL 24 HOUR 
ORDER BY last_bounce_at DESC;
```

## API Usage

### Check Email Status
```bash
curl -X GET https://your-api-domain.com/api/webhooks/ses/check-email/user@example.com \
  -H "Authorization: Bearer your-sanctum-token"
```

**Response**:
```json
{
  "email": "user@example.com",
  "is_suppressed": true,
  "status": "bounced_hard",
  "bounce_type": "permanent",
  "bounce_count": 1,
  "last_bounce_at": "2024-12-22T10:30:00.000000Z",
  "suppressed_at": "2024-12-22T10:30:00.000000Z"
}
```

### Remove Suppression
```bash
curl -X POST https://your-api-domain.com/api/webhooks/ses/remove-suppression \
  -H "Authorization: Bearer your-sanctum-token" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

**Response**:
```json
{
  "success": true,
  "message": "Suppression removed for user@example.com"
}
```

### Get Statistics
```bash
curl -X GET "https://your-api-domain.com/api/webhooks/ses/statistics?tenant_id=1" \
  -H "Authorization: Bearer your-sanctum-token"
```

**Response**:
```json
{
  "tenant_id": 1,
  "total_records": 150,
  "active_emails": 145,
  "bounced_hard": 3,
  "bounced_soft": 1,
  "complained": 1,
  "suppressed": 5,
  "bounce_rate": 3.33
}
```

## Troubleshooting

### Issue: Webhook Not Receiving Notifications
**Symptoms**: Lambda executes but webhook returns 401/403
**Solution**: 
1. Verify WEBHOOK_SECRET matches in Lambda env and Laravel .env
2. Check X-Webhook-Secret header in Lambda logs
3. Verify webhook URL is publicly accessible

### Issue: Emails Still Being Sent to Suppressed Addresses
**Symptoms**: Suppressed emails still receive notifications
**Solution**:
1. Check AppNotificationBuilder.php has all 3 filtering points
2. Verify filterSuppressedEmails() is being called
3. Check logs for "Filtered suppressed emails" messages
4. Verify EmailBounceService::shouldSuppressEmail() returns true

### Issue: Lambda Execution Errors
**Symptoms**: CloudWatch shows Lambda errors
**Solution**:
1. Check Lambda logs: `aws logs tail /aws/lambda/project-env-ses-bounce-handler --follow`
2. Verify webhook URL is correct in Lambda environment variables
3. Check network connectivity from Lambda to API
4. Verify SNS message format matches expected structure

### Issue: Bounces Not Recorded in Database
**Symptoms**: SES generates bounces but database empty
**Solution**:
1. Check Laravel logs for EmailBounceService errors
2. Verify database migration ran successfully
3. Check webhook authentication is working
4. Verify SNS topic subscriptions are active

## Security Considerations

1. **Webhook Authentication**: 
   - Use strong random WEBHOOK_SECRET (min 32 characters)
   - Rotate WEBHOOK_SECRET periodically
   - Monitor for failed authentication attempts

2. **Rate Limiting**:
   - Consider adding rate limiting to webhook endpoint
   - Monitor for unusual bounce patterns

3. **Data Privacy**:
   - Email addresses are PII - handle accordingly
   - Consider GDPR compliance for EU users
   - Implement data retention policies

4. **IAM Permissions**:
   - Lambda has minimal permissions (logs only)
   - SNS topics restricted to SES service
   - API endpoints protected with Sanctum authentication

## Maintenance

### Periodic Tasks
1. **Review Suppression List**: Monthly review of suppressed emails
2. **Clean Old Records**: Consider archiving records older than 1 year
3. **Monitor Bounce Rates**: Track overall and per-tenant bounce rates
4. **Update Lambda**: Keep Lambda runtime and dependencies updated

### Metrics to Track
- Total suppressed emails
- Bounce rate by tenant
- Complaint rate by tenant
- Lambda execution success rate
- Webhook response times

## Cost Considerations

### AWS Costs
- **SNS**: ~$0.50 per million notifications (first million free)
- **Lambda**: ~$0.20 per million requests + compute time
- **CloudWatch Logs**: ~$0.50 per GB ingested

### Estimated Monthly Cost
For 100,000 emails/month with 2% bounce rate:
- SNS: ~$0.01 (2,000 notifications)
- Lambda: ~$0.01 (2,000 invocations, <100ms each)
- CloudWatch: ~$0.01 (minimal logs)
- **Total**: ~$0.03/month

## Implementation Checklist

- [x] Created database migration
- [x] Created EmailDeliveryStatus model
- [x] Created EmailBounceService
- [x] Created Lambda function
- [x] Created CDK template
- [x] Updated production CDK config
- [x] Created webhook controller
- [x] Created webhook routes
- [x] Integrated filtering in AppNotificationBuilder
- [ ] Run database migration
- [ ] Deploy CDK stack
- [ ] Configure SES identity notifications
- [ ] Test with SES simulator addresses
- [ ] Monitor CloudWatch logs
- [ ] Document team procedures

## References

- [AWS SES Bounce Handling](https://docs.aws.amazon.com/ses/latest/dg/notification-contents.html)
- [AWS SNS Documentation](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [Laravel Notifications](https://laravel.com/docs/11.x/notifications)
- Internal: `AWS_SES_EMAIL_PRACTICES_KITCHNTABS_SIMPLE.md`

## Support

For issues or questions, refer to:
1. CloudWatch Logs: `/aws/lambda/{project}-{env}-ses-bounce-handler`
2. Laravel Logs: `storage/logs/laravel.log`
3. Database: `email_delivery_status` table
4. This documentation: `AWS_SES_BOUNCE_COMPLAINT_IMPLEMENTATION.md`

---

**Last Updated**: 2024-12-22
**Version**: 1.0.0
**Status**: ✅ Implementation Complete, Ready for Deployment
