
# SES Bounce & Complaint Handling - Deployment Checklist

## Pre-Deployment Checklist

### Environment Setup
- [ ] AWS CLI installed and configured
- [ ] AWS profile has SES, SNS, Lambda, CloudWatch permissions
- [ ] Node.js 18.x installed for CDK
- [ ] Laravel backend accessible via public URL
- [ ] Database backup completed

### Configuration
- [ ] Generated secure WEBHOOK_SECRET (32+ characters)
- [ ] Added WEBHOOK_SECRET to Laravel `.env`
- [ ] Verified MAIL_FROM_ADDRESS in `.env`
- [ ] Verified MAIL_FROM_NAME in `.env`
- [ ] Noted SES verified identity (email/domain)

### Code Review
- [ ] Reviewed migration file: `2024_12_22_000001_create_email_delivery_status_table.php`
- [ ] Reviewed model: `EmailDeliveryStatus.php`
- [ ] Reviewed service: `EmailBounceService.php`
- [ ] Reviewed controller: `SesWebhookController.php`
- [ ] Reviewed Lambda: `ses-bounce-handler/index.js`
- [ ] Reviewed CDK template: `ses-notification-template.ts`
- [ ] Reviewed AppNotificationBuilder changes

---

## Deployment Steps

### Step 1: Database Migration ⏱️ 2 minutes
- [ ] Backed up database
- [ ] Run: `php artisan migrate`
- [ ] Verify table created: `php artisan db:table email_delivery_status`
- [ ] Check table has correct columns and indexes
- [ ] Rollback plan documented

**Rollback**: `php artisan migrate:rollback --step=1`

---

### Step 2: CDK Deployment ⏱️ 5-8 minutes
- [ ] Set environment variables:
  ```bash
  export ENV=production
  export STACK_TYPE=infrastructure
  export WEBHOOK_URL="https://api.yourdomain.com/api/webhooks/ses/notifications"
  export WEBHOOK_SECRET="your-secret"
  ```
- [ ] Navigate to CDK directory: `cd kitchntabs-ci-cdk`
- [ ] Install dependencies: `npm install` (if needed)
- [ ] Deploy stack: `npx cdk deploy KitchnTabsProductionSESNotifications --profile your-profile`
- [ ] **Save output ARNs**:
  - [ ] Bounce Topic ARN: `_______________________`
  - [ ] Complaint Topic ARN: `_______________________`
  - [ ] Lambda Function ARN: `_______________________`
- [ ] Verify Lambda created in AWS Console
- [ ] Verify SNS topics created
- [ ] Check Lambda environment variables set correctly

**Rollback**: `npx cdk destroy KitchnTabsProductionSESNotifications --profile your-profile`

---

### Step 3: SES Identity Configuration ⏱️ 3-5 minutes

**Via AWS Console**:
- [ ] Navigate to [SES Console](https://console.aws.amazon.com/ses/)
- [ ] Go to **Verified identities**
- [ ] Select your email/domain
- [ ] Click **Notifications** tab
- [ ] Click **Edit** under "Feedback notifications"
- [ ] Set Bounce topic: `kitchntabs-production-ses-bounces`
- [ ] Enable "Include original headers" for bounces
- [ ] Set Complaint topic: `kitchntabs-production-ses-complaints`
- [ ] Enable "Include original headers" for complaints
- [ ] Click **Save changes**
- [ ] Verify configuration saved

**OR Via AWS CLI**:
```bash
BOUNCE_TOPIC_ARN="your-bounce-topic-arn"
COMPLAINT_TOPIC_ARN="your-complaint-topic-arn"
IDENTITY="noreply@yourdomain.com"

aws ses set-identity-notification-topic \
  --identity "$IDENTITY" \
  --notification-type Bounce \
  --sns-topic "$BOUNCE_TOPIC_ARN" \
  --profile your-profile

aws ses set-identity-notification-topic \
  --identity "$IDENTITY" \
  --notification-type Complaint \
  --sns-topic "$COMPLAINT_TOPIC_ARN" \
  --profile your-profile

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
```

- [ ] Run above commands successfully
- [ ] Verify with: `aws ses get-identity-notification-attributes --identities "$IDENTITY"`

**Rollback**: Remove SNS topics from SES identity (set to empty)

---

### Step 4: Verification & Testing ⏱️ 10-15 minutes

#### Test 1: Hard Bounce
- [ ] Send email to `bounce@simulator.amazonses.com`
- [ ] Wait 1-2 minutes for notification
- [ ] Check Lambda logs: `aws logs tail /aws/lambda/...-ses-bounce-handler --follow`
- [ ] Check Laravel logs: `tail -f storage/logs/laravel.log`
- [ ] Verify database record:
  ```sql
  SELECT * FROM email_delivery_status WHERE email = 'bounce@simulator.amazonses.com';
  ```
- [ ] Expected: status = 'bounced_hard', bounce_count = 1
- [ ] Try sending another email to same address
- [ ] Verify email is filtered out (check logs for "Filtered suppressed emails")

#### Test 2: Complaint
- [ ] Send email to `complaint@simulator.amazonses.com`
- [ ] Wait 1-2 minutes
- [ ] Check logs (Lambda + Laravel)
- [ ] Verify database record:
  ```sql
  SELECT * FROM email_delivery_status WHERE email = 'complaint@simulator.amazonses.com';
  ```
- [ ] Expected: status = 'complained', bounce_type = 'complaint'
- [ ] Verify future emails filtered

#### Test 3: API Endpoints
- [ ] Test check email status:
  ```bash
  curl -X GET https://api.yourdomain.com/api/webhooks/ses/check-email/bounce@simulator.amazonses.com \
    -H "Authorization: Bearer YOUR_TOKEN"
  ```
- [ ] Verify response shows suppression data
- [ ] Test statistics endpoint:
  ```bash
  curl -X GET "https://api.yourdomain.com/api/webhooks/ses/statistics?tenant_id=1" \
    -H "Authorization: Bearer YOUR_TOKEN"
  ```
- [ ] Test remove suppression:
  ```bash
  curl -X POST https://api.yourdomain.com/api/webhooks/ses/remove-suppression \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -d '{"email": "bounce@simulator.amazonses.com"}'
  ```
- [ ] Verify email can receive messages again

#### Test 4: Real Email (Optional but Recommended)
- [ ] Send to a real test email address
- [ ] Verify received successfully
- [ ] Check database for active status
- [ ] Confirm no errors in logs

---

### Step 5: Monitoring Setup ⏱️ 5 minutes
- [ ] Set up CloudWatch alarm for Lambda errors:
  - Metric: AWS/Lambda → Errors
  - Function: kitchntabs-production-ses-bounce-handler
  - Threshold: > 5 errors in 5 minutes
  - Notification: Email to ops team
- [ ] Set up alarm for Lambda throttles (optional)
- [ ] Set up log insights query for bounce trends
- [ ] Document alarm endpoints for team
- [ ] Add to monitoring dashboard

---

### Step 6: Documentation ⏱️ 5 minutes
- [ ] Update team wiki with:
  - Lambda function name
  - SNS topic ARNs
  - Webhook endpoint URL
  - Admin API endpoints
- [ ] Share deployment summary with team
- [ ] Add to runbook:
  - How to check suppressed emails
  - How to remove suppression manually
  - How to check bounce rates
  - Emergency rollback procedure
- [ ] Update on-call guide with new components

---

## Post-Deployment Checklist (24 hours after)

### Day 1 Monitoring
- [ ] Check Lambda invocation count (should match email volume)
- [ ] Check Lambda error rate (should be < 1%)
- [ ] Review database growth (email_delivery_status table)
- [ ] Check for any suppressed emails
- [ ] Review bounce rate by tenant
- [ ] Verify no customer complaints about missing emails

### Day 1 Queries
```sql
-- Check total records
SELECT COUNT(*) as total FROM email_delivery_status;

-- Check by status
SELECT status, COUNT(*) as count 
FROM email_delivery_status 
GROUP BY status;

-- Check recent bounces (last 24h)
SELECT email, status, bounce_count, last_bounce_at 
FROM email_delivery_status 
WHERE last_bounce_at >= NOW() - INTERVAL 24 HOUR 
ORDER BY last_bounce_at DESC;

-- Check suppressed emails
SELECT email, status, bounce_type, suppressed_at 
FROM email_delivery_status 
WHERE status IN ('bounced_hard', 'complained', 'suppressed');
```

### Day 7 Review
- [ ] Review weekly bounce rate trends
- [ ] Check for any false positives (valid emails suppressed)
- [ ] Review Lambda costs in AWS Billing
- [ ] Optimize if needed (e.g., reduce log retention)
- [ ] Update documentation based on learnings
- [ ] Schedule monthly review meeting

---

## Troubleshooting Checklist

### Issue: Migration Failed
- [ ] Check database connection
- [ ] Verify migration file syntax
- [ ] Check for table name conflicts
- [ ] Review Laravel logs for errors
- [ ] Rollback and retry

### Issue: CDK Deploy Failed
- [ ] Check AWS credentials
- [ ] Verify IAM permissions
- [ ] Check CDK version (>= 2.100.0)
- [ ] Review CloudFormation events in console
- [ ] Check for resource limits

### Issue: Lambda Not Invoked
- [ ] Check SNS topic subscriptions
- [ ] Verify SES identity notifications configured
- [ ] Check Lambda execution role permissions
- [ ] Review SNS message delivery logs
- [ ] Send test SNS message

### Issue: Webhook Returns Error
- [ ] Check WEBHOOK_SECRET matches
- [ ] Verify webhook URL is accessible
- [ ] Check Laravel logs for errors
- [ ] Test webhook directly with curl
- [ ] Verify route is registered

### Issue: Emails Not Filtered
- [ ] Check AppNotificationBuilder.php changes
- [ ] Verify filterSuppressedEmails() is called
- [ ] Check logs for "Filtered suppressed emails"
- [ ] Verify database has suppressed records
- [ ] Test shouldSuppressEmail() directly

---

## Rollback Checklist (If Needed)

### Immediate Rollback (Critical Issue)
- [ ] **STOP**: Document the issue first
- [ ] Remove SNS topics from SES identity
- [ ] Disable filtering in AppNotificationBuilder:
  ```php
  // Comment out filterSuppressedEmails() calls
  // Or add feature flag to bypass
  ```
- [ ] Deploy code changes
- [ ] Notify team of rollback
- [ ] Continue investigating issue

### Full Rollback (After Analysis)
- [ ] Remove SNS topic configuration from SES
- [ ] Destroy CDK stack: `npx cdk destroy KitchnTabsProductionSESNotifications`
- [ ] Rollback migration: `php artisan migrate:rollback --step=1`
- [ ] Remove code changes (git revert)
- [ ] Deploy previous version
- [ ] Document lessons learned

---

## Sign-Off

### Deployed By
- **Name**: ___________________
- **Date**: ___________________
- **Time**: ___________________

### Verified By
- **Name**: ___________________
- **Date**: ___________________
- **Time**: ___________________

### Production Approval
- **Name**: ___________________
- **Title**: ___________________
- **Date**: ___________________
- **Signature**: ___________________

---

## Notes & Issues
```
[Space for deployment notes, issues encountered, or special considerations]




```

---

## Metrics Baseline (Record at Deployment)

| Metric | Value | Date/Time |
|--------|-------|-----------|
| Total emails in system | _______ | _________ |
| Active email addresses | _______ | _________ |
| Known bounces (before) | _______ | _________ |
| Known complaints (before) | _______ | _________ |
| Lambda invocations (24h) | _______ | _________ |
| Average bounce rate | _______ % | _________ |

## Contact Information

| Role | Name | Contact |
|------|------|---------|
| Technical Lead | _____________ | _______________ |
| DevOps Lead | _____________ | _______________ |
| On-Call Engineer | _____________ | _______________ |
| AWS Account Admin | _____________ | _______________ |

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-22  
**Next Review**: 7 days after deployment
