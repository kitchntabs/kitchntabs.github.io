
# Campaign Management Manual

## Creating and Publishing a Campaign

### Overview
This procedure guides Tenant Administrators through the complete process of creating, configuring, and publishing a campaign to external marketplaces like Uber Eats. Campaigns allow you to promote products with special pricing and manage inventory across multiple marketplace integrations.

### Prerequisites

#### System-Level Prerequisites
- **System Administrator Action Required**: A System Administrator must first provision the Uber Eats marketplace to your tenant account
- **Marketplace Provisioning**: Uber Eats integration must be enabled and configured for your tenant

#### User-Level Prerequisites
- **User Role**: You must have the **Admin** role for the tenant
- **Access Level**: Tenant Administrator privileges
- **System Access**: Valid login credentials for the DASH-PW-PROJECT platform

#### Business Prerequisites
- **Pricelist**: At least one active pricelist must exist in your tenant account
- **Stocklist**: At least one stock type/list must be configured for inventory management

### Step-by-Step Instructions

#### Step 1: Access the Campaigns Section
1. Log in to the DASH-PW-PROJECT platform using your administrator credentials
2. In the sidebar menu, click on **Campaigns**
3. This will display the campaigns overview page

#### Step 2: Create a New Campaign
1. Locate and click the **Create** button (typically found in the top-right corner or within the campaigns list)
2. This will open the campaign creation form

#### Step 3: Configure Campaign Details
1. **Campaign Name**: Enter a descriptive name for your campaign (e.g., "Holiday Specials 2025")
2. **Campaign Type**:
   - Toggle the **Permanent/Scheduled** switch:
     - **Permanent**: Campaign runs indefinitely until manually stopped
     - **Scheduled**: Campaign has specific start and end dates
3. **Pricing Configuration**:
   - Select the primary pricelist for regular prices
   - Optionally set discount pricing (percentage or fixed amount)
4. **Inventory Management**:
   - Select the stock list to use for inventory tracking during the campaign
5. **Marketplace Selection**:
   - Choose the marketplace(s) where this campaign will be published
   - For this procedure, select **Uber Eats** integration
6. Review all settings and click **Save** or **Create Campaign**

#### Step 4: Access Campaign Details
1. After creation, you will be redirected to the campaigns list
2. Find your newly created campaign in the list
3. Click the **View** icon (eye icon) to access the campaign details page

#### Step 5: Associate Products
1. In the campaign details view, locate and click **Associate Products**
2. This will open the product selection interface
3. Choose the products you want to include in this campaign:
   - Browse available products
   - Select individual products or use bulk selection options
   - Configure product-specific settings if available (pricing overrides, stock limits, etc.)
4. Click the **Save** button that appears above the product table to confirm your selections

#### Step 6: Publish the Campaign
1. After saving product associations, you will be redirected to the associated products list
2. Review the products and their campaign settings
3. In the upper right corner of the UI, click **Publish Campaign**
4. Confirm the publication when prompted

### Expected Results

#### Immediate Results
- Campaign status changes to **Publishing** or **In Progress**
- Campaign tracker records are created for execution monitoring
- Products begin publishing to the selected marketplace(s)

#### Background Processing
- System creates `CampaignMarketplace` records for each selected marketplace
- `CampaignMarketplaceProduct` records are generated for each product-marketplace combination
- Publishing jobs are queued for execution
- Progress tracking begins through `CampaignTracker` records

#### Final Results
- Campaign status updates to **Published** when all products are successfully published
- Products appear on Uber Eats with campaign pricing
- Orders from the campaign are tracked and attributed correctly

### Campaign Status Flow
```
DRAFT → PUBLISHING → PUBLISHED
    ↓       ↓           ↓
CANCELLED  PAUSED     FINISHING → FINISHED
```

### Troubleshooting

#### Issue: Campaign Creation Fails
**Cause**: Missing prerequisites or invalid configuration
**Solutions**:
- Verify Uber Eats marketplace is provisioned by System Administrator
- Ensure at least one pricelist exists
- Confirm stocklist is properly configured
- Check that all required fields are filled

#### Issue: Products Not Associating
**Cause**: Product selection issues or permissions
**Solutions**:
- Verify products exist and are active
- Check user permissions for product management
- Ensure products are compatible with selected marketplace

#### Issue: Publishing Fails
**Cause**: Marketplace API issues or configuration problems
**Solutions**:
- Check Uber Eats API credentials and connectivity
- Review campaign tracker logs for specific error messages
- Verify product data meets marketplace requirements
- Contact System Administrator for API-related issues

#### Issue: Campaign Not Visible on Marketplace
**Cause**: Publishing delays or synchronization issues
**Solutions**:
- Wait for publishing process to complete (check campaign status)
- Verify marketplace account is active and properly configured
- Check for any error notifications in the system

### Monitoring Campaign Performance

#### Real-time Monitoring
- Use the campaign details view to track publishing progress
- Monitor `CampaignTracker` status for execution phases
- Check product-level status in associated products list

#### Performance Metrics
- Track sales through campaign-attributed orders
- Monitor stock levels and low-stock alerts
- Review marketplace-specific performance data

### Related Procedures
- [Provisioning Marketplace Integrations](marketplace-provisioning.md)
- [Managing Pricelists](pricelist-management.md)
- [Configuring Stock Types](stock-management.md)
- [Campaign Performance Analytics](campaign-analytics.md)
- [Handling Campaign Errors](campaign-error-resolution.md)

### Technical Notes

#### Database Records Created
- `campaigns` - Main campaign record
- `campaign_marketplace` - Links campaign to Uber Eats marketplace
- `campaign_marketplace_products` - Individual product configurations
- `campaign_trackers` - Execution progress tracking

#### Publishing Process
1. Campaign creation triggers marketplace-specific publishing jobs
2. Each marketplace processes products according to its API requirements
3. Progress is tracked hierarchically (main process → marketplace processes)
4. Errors are logged and can trigger manual resolution workflows

#### Integration Points
- Uber Eats API for product publishing and order attribution
- Internal pricing system for campaign pricing calculations
- Inventory management for stock tracking during campaigns

### Support and Escalation

#### For Tenant Administrators
- Check campaign tracker logs for detailed error information
- Review system notifications for publishing status updates
- Use the associated products view to identify specific product issues

#### When to Contact Support
- Publishing consistently fails after multiple attempts
- Marketplace API credentials appear invalid
- System errors prevent campaign creation or management
- Performance issues with campaign publishing

#### Information to Provide
When contacting support, include:
- Campaign ID and name
- Tenant ID
- Specific error messages
- Steps taken before the issue occurred
- Marketplace integration details (Uber Eats)

---

## Scheduled Campaigns - Automated Processing

### Overview

Scheduled campaigns allow you to set a **start date** and **end date** for automatic publishing and finishing. The system automatically handles the lifecycle of scheduled campaigns without manual intervention.

### How Scheduled Campaigns Work

When you toggle a campaign as **Scheduled** (instead of **Permanent**):
1. Set the **Start Date**: When the campaign should automatically publish
2. Set the **End Date**: When the campaign should automatically finish

The system's scheduler checks every **5 minutes** for:
- Campaigns ready to **auto-publish** (start date reached)
- Campaigns ready to **auto-finish** (end date passed)

### Scheduled Campaign Lifecycle

```
[PENDING + scheduled=true + start_date]
        │
        │ ← System checks every 5 minutes
        │
        ▼ (when start_date <= now)
[PUBLISHING → PUBLISHED]
        │
        │ ← Campaign runs normally
        │
        ▼ (when end_date <= now)
[FINISHING → FINISHED]
```

### Technical Implementation

#### Artisan Command
```bash
# Signature
php artisan campaigns:process-scheduled [--dry-run] [--force]

# Options:
#   --dry-run    Preview what would be processed without making changes
#   --force      Process campaigns even if outside scheduled time (recovery mode)
```

#### Scheduler Configuration
The command runs automatically via Laravel's task scheduler:

```php
// app/Console/Kernel.php
$schedule->command('campaigns:process-scheduled')
         ->everyFiveMinutes()
         ->withoutOverlapping()
         ->appendOutputTo(storage_path('logs/campaigns-scheduled.log'));
```

#### Processing Logic

| Campaign State | Condition | Action |
|----------------|-----------|--------|
| `scheduled=true`, `status=PENDING`, `start_date <= now` | Ready to publish | Dispatch `CampaignProcessJob('publish')` |
| `scheduled=true`, `status=PUBLISHED`, `end_date <= now` | Ready to finish | Dispatch `CampaignProcessJob('finish')` |

### Monitoring Scheduled Campaigns

#### Log Files
- **Scheduler Log**: `storage/logs/supervisor-schedule.log`
- **Campaign Processing Log**: `storage/logs/campaigns-scheduled.log`
- **Laravel Log**: `storage/logs/laravel.log`

#### Manual Verification
```bash
# Check scheduler status (inside container)
supervisorctl status

# View scheduled campaign logs
tail -f /var/www/dash/storage/logs/campaigns-scheduled.log

# Dry-run to see pending scheduled campaigns
php artisan campaigns:process-scheduled --dry-run
```

### Troubleshooting Scheduled Campaigns

#### Issue: Campaign Not Auto-Publishing
**Possible Causes**:
- Scheduler not running (`schedule:work` not active)
- Start date not yet reached
- Campaign status is not `PENDING`
- `scheduled` flag is `false`

**Solutions**:
1. Check supervisor status: `supervisorctl status`
2. Verify campaign configuration in database
3. Check scheduler logs for errors
4. Run dry-run to diagnose: `php artisan campaigns:process-scheduled --dry-run`

#### Issue: Campaign Not Auto-Finishing
**Possible Causes**:
- End date not yet passed
- Campaign status is not `PUBLISHED`
- Scheduler process stopped

**Solutions**:
1. Verify end_date is in the past
2. Confirm campaign is in `PUBLISHED` status
3. Check scheduler is running
4. Force finish if needed: `php artisan campaigns:process-scheduled --force`

#### Issue: Scheduler Not Running
**Cause**: Supervisor using `schedule:run` instead of `schedule:work`

**Solution**: Ensure supervisor config uses:
```ini
command=php /var/www/dash/artisan schedule:work
```

### Recovery Procedures

#### Force Process All Scheduled Campaigns
```bash
# This will process campaigns regardless of dates (for recovery)
php artisan campaigns:process-scheduled --force
```

#### Manually Publish a Campaign
```bash
php artisan tinker
>>> $campaign = \Domain\App\Models\ECommerce\Campaign::find(123);
>>> \Domain\App\Jobs\ECommerce\Campaigns\CampaignProcessJob::dispatch($user, $campaign, 'publish');
```

#### Manually Finish a Campaign
```bash
php artisan tinker
>>> $campaign = \Domain\App\Models\ECommerce\Campaign::find(123);
>>> \Domain\App\Jobs\ECommerce\Campaigns\CampaignProcessJob::dispatch($user, $campaign, 'finish');
```

### Best Practices

1. **Set Start Date in the Future**: Allow buffer time for any system delays
2. **Use Dry-Run First**: Before deploying, test with `--dry-run` to verify logic
3. **Monitor Logs**: Regularly check `campaigns-scheduled.log` for processing activity
4. **Avoid Overlapping Campaigns**: Ensure campaigns for the same products don't conflict

---

*Last Updated: December 27, 2025*
*Document Version: 1.1*
*Applies to: DASH-PW-PROJECT Campaign Management System*</content>
<parameter name="filePath">/Users/farandal/DASH-PW-PROJECT/campaign-management-manual.md