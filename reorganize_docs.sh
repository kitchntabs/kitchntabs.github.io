#!/bin/bash
# Reorganize docs folder to match ClickUp epic structure
# Backs up old structure before reorganizing

set -e

DOCS_DIR="/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/docs"
BACKUP_DIR="/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/docs_backup_$(date +%Y%m%d_%H%M%S)"
MAPPING_FILE="/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/DOCS_TO_CLICKUP_MAPPING.md"

echo "🚀 Reorganizing docs to match ClickUp epic structure"
echo ""

# Step 1: Backup current structure
echo "📦 Backing up current structure to: $BACKUP_DIR"
cp -r "$DOCS_DIR" "$BACKUP_DIR"
echo "✅ Backup complete"
echo ""

# Step 2: Create epic folders
echo "📁 Creating epic folders..."
mkdir -p "$DOCS_DIR/F1-Orders-and-Tabs"
mkdir -p "$DOCS_DIR/F2-Products-and-Catalog"
mkdir -p "$DOCS_DIR/F3-Product-Import-Export"
mkdir -p "$DOCS_DIR/F4-Mall-Food-Court"
mkdir -p "$DOCS_DIR/F5-Customer-Self-Service"
mkdir -p "$DOCS_DIR/F6-Tenant-Staff-App"
mkdir -p "$DOCS_DIR/F7-System-Admin-Application"
mkdir -p "$DOCS_DIR/F8-Public-Web"
mkdir -p "$DOCS_DIR/F9-Marketplaces"
mkdir -p "$DOCS_DIR/F10-Point-of-Sale"
mkdir -p "$DOCS_DIR/F11-Checkout-Gateways"
mkdir -p "$DOCS_DIR/F12-Billing-Subscriptions-Payments"
mkdir -p "$DOCS_DIR/F13-Platform-Multi-Tenancy"
mkdir -p "$DOCS_DIR/F14-Auth-Access-Control"
mkdir -p "$DOCS_DIR/F15-Notifications-Messaging"
mkdir -p "$DOCS_DIR/F16-AI-Agents"
mkdir -p "$DOCS_DIR/F17-Inventory"
mkdir -p "$DOCS_DIR/F18-Campaigns"
mkdir -p "$DOCS_DIR/F19-Internationalization"
mkdir -p "$DOCS_DIR/F20-Media-Images"

mkdir -p "$DOCS_DIR/N1-Backend-Framework"
mkdir -p "$DOCS_DIR/N2-Frontend-Framework"
mkdir -p "$DOCS_DIR/N3-Infrastructure-CI-CD"
mkdir -p "$DOCS_DIR/N4-Build-Toolchain"
mkdir -p "$DOCS_DIR/N5-Desktop-Device-Service"
mkdir -p "$DOCS_DIR/N6-Caching-Performance"
mkdir -p "$DOCS_DIR/N7-Security"
mkdir -p "$DOCS_DIR/N8-Observability"
mkdir -p "$DOCS_DIR/N9-App-Publishing"
mkdir -p "$DOCS_DIR/N10-Administrative-Legal"

mkdir -p "$DOCS_DIR/General-Utilities"
mkdir -p "$DOCS_DIR/Archive"

echo "✅ Epic folders created"
echo ""

# Step 3: Move files based on mapping
# This is a helper function to move a file if it exists
move_file() {
    local src="$1"
    local dest_folder="$2"

    if [ -f "$src" ]; then
        mv "$src" "$dest_folder/$(basename "$src")"
        echo "✓ Moved: $(basename "$src") → $dest_folder"
        return 0
    else
        return 1
    fi
}

echo "📋 Moving files to epic folders..."
echo ""

# F1: Orders & Tabs
echo "→ F1: Orders & Tabs"
move_file "$DOCS_DIR/DELETE_TENANCY_ACCOUNT.md" "$DOCS_DIR/F1-Orders-and-Tabs" 2>/dev/null || true
move_file "$DOCS_DIR/DELIVERY.md" "$DOCS_DIR/F1-Orders-and-Tabs" 2>/dev/null || true
move_file "$DOCS_DIR/docs/tech/domain-models/Tab-README.md" "$DOCS_DIR/F1-Orders-and-Tabs" 2>/dev/null || true
move_file "$DOCS_DIR/docs/tech/domain-models/Order-README.md" "$DOCS_DIR/F1-Orders-and-Tabs" 2>/dev/null || true

# F2: Products & Catalog
echo "→ F2: Products & Catalog"
move_file "$DOCS_DIR/DISCOUNT_FEATURE.md" "$DOCS_DIR/F2-Products-and-Catalog" 2>/dev/null || true

# F4: Mall / Food Court
echo "→ F4: Mall / Food Court"
# Mall app folder files
if [ -d "$DOCS_DIR/mall-app" ]; then
    mv "$DOCS_DIR/mall-app"/* "$DOCS_DIR/F4-Mall-Food-Court/" 2>/dev/null || true
    rmdir "$DOCS_DIR/mall-app" 2>/dev/null || true
fi

# F5: Customer & Self-Service
echo "→ F5: Customer & Self-Service"
if [ -d "$DOCS_DIR/customer-app" ]; then
    mv "$DOCS_DIR/customer-app"/* "$DOCS_DIR/F5-Customer-Self-Service/" 2>/dev/null || true
    rmdir "$DOCS_DIR/customer-app" 2>/dev/null || true
fi
move_file "$DOCS_DIR/TRIAL_REGISTRATION_FLOW.md" "$DOCS_DIR/F5-Customer-Self-Service" 2>/dev/null || true

# F6: Tenant / Staff App
echo "→ F6: Tenant / Staff App"
if [ -d "$DOCS_DIR/staff-app" ]; then
    mv "$DOCS_DIR/staff-app"/* "$DOCS_DIR/F6-Tenant-Staff-App/" 2>/dev/null || true
    rmdir "$DOCS_DIR/staff-app" 2>/dev/null || true
fi
move_file "$DOCS_DIR/PYTHON_SERVICE_TESTING.md" "$DOCS_DIR/F6-Tenant-Staff-App" 2>/dev/null || true

# F7: System Admin Application
echo "→ F7: System Admin Application"
move_file "$DOCS_DIR/DASH_LAZY_ADMIN_APP_RERENDERING_BUG.md" "$DOCS_DIR/F7-System-Admin-Application" 2>/dev/null || true
move_file "$DOCS_DIR/REACT-ADMIN-LIST.md" "$DOCS_DIR/F7-System-Admin-Application" 2>/dev/null || true
move_file "$DOCS_DIR/DASH-ADMIN-AUDIT.md" "$DOCS_DIR/F7-System-Admin-Application" 2>/dev/null || true

# F9: Marketplaces
echo "→ F9: Marketplaces"
move_file "$DOCS_DIR/JUMPSELLER-API.md" "$DOCS_DIR/F9-Marketplaces" 2>/dev/null || true

# F11: Checkout Gateways
echo "→ F11: Checkout Gateways"
move_file "$DOCS_DIR/ML-CHECKOUT-PRO-DOCS.md" "$DOCS_DIR/F11-Checkout-Gateways" 2>/dev/null || true
move_file "$DOCS_DIR/ML-WEBHOOKS.md" "$DOCS_DIR/F11-Checkout-Gateways" 2>/dev/null || true

# F12: Billing, Subscriptions & Payments
echo "→ F12: Billing, Subscriptions & Payments"
move_file "$DOCS_DIR/CANCEL_SUBSCRIPTION.md" "$DOCS_DIR/F12-Billing-Subscriptions-Payments" 2>/dev/null || true
move_file "$DOCS_DIR/SUBSCRIPTION_BUG_FIXES.md" "$DOCS_DIR/F12-Billing-Subscriptions-Payments" 2>/dev/null || true
move_file "$DOCS_DIR/TENANCY_LIFECYCLE_TESTING.md" "$DOCS_DIR/F12-Billing-Subscriptions-Payments" 2>/dev/null || true
move_file "$DOCS_DIR/REDBILL-API.md" "$DOCS_DIR/F12-Billing-Subscriptions-Payments" 2>/dev/null || true
move_file "$DOCS_DIR/PAYMENT-GATEWAY-TESTS.md" "$DOCS_DIR/F12-Billing-Subscriptions-Payments" 2>/dev/null || true
move_file "$DOCS_DIR/FEATURE-PAYMENTS.md" "$DOCS_DIR/F12-Billing-Subscriptions-Payments" 2>/dev/null || true

# F13: Platform & Multi-Tenancy
echo "→ F13: Platform & Multi-Tenancy"
move_file "$DOCS_DIR/TenancyFeature.md" "$DOCS_DIR/F13-Platform-Multi-Tenancy" 2>/dev/null || true

# F14: Auth & Access Control
echo "→ F14: Auth & Access Control"
move_file "$DOCS_DIR/PERMISSION_SELECTOR_DATAGRID.md" "$DOCS_DIR/F14-Auth-Access-Control" 2>/dev/null || true
move_file "$DOCS_DIR/PERMISSION_SELECTOR_DATAGRID_SUMMARY.md" "$DOCS_DIR/F14-Auth-Access-Control" 2>/dev/null || true
move_file "$DOCS_DIR/PERMISSION_SELECTOR_LIST_SOLUTION.md" "$DOCS_DIR/F14-Auth-Access-Control" 2>/dev/null || true
move_file "$DOCS_DIR/REFRESH_TOKEN_IMPLEMENTATION.md" "$DOCS_DIR/F14-Auth-Access-Control" 2>/dev/null || true

# F15: Notifications & Messaging
echo "→ F15: Notifications & Messaging"
move_file "$DOCS_DIR/NOTIFICATIONS.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/PRIVATE_NOTIFICATION.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/EMAIL_UNSUBSCRIBE_SYSTEM.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/EMAIL_UNSUBSCRIBE_IMPLEMENTATION_SUMMARY.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/EMAIL_UNSUBSCRIBE_DEPLOYMENT_CHECKLIST.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/AWS_SES_EMAIL_PRACTICES_KITCHNTABS.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/AWS_SES_EMAIL_PRACTICES_KITCHNTABS_SIMPLE.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/AWS_SES_BOUNCE_COMPLAINT_IMPLEMENTATION.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/DEPLOY_SES_BOUNCE_HANDLING.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true
move_file "$DOCS_DIR/SES_BOUNCE_HANDLING_CHECKLIST.md" "$DOCS_DIR/F15-Notifications-Messaging" 2>/dev/null || true

# F18: Campaigns
echo "→ F18: Campaigns"
move_file "$DOCS_DIR/CAMPAIGN_PUBLISHING_FLOW.md" "$DOCS_DIR/F18-Campaigns" 2>/dev/null || true
move_file "$DOCS_DIR/campaign-management-manual.md" "$DOCS_DIR/F18-Campaigns" 2>/dev/null || true
move_file "$DOCS_DIR/Cloudwatch.success.uber-campaign.publishing.md" "$DOCS_DIR/F18-Campaigns" 2>/dev/null || true
move_file "$DOCS_DIR/tenant-marketplace-campaign-architecture.md" "$DOCS_DIR/F18-Campaigns" 2>/dev/null || true

# F20: Media & Images
echo "→ F20: Media & Images"
move_file "$DOCS_DIR/ADDING_IMAGE_TO_MODEL.md" "$DOCS_DIR/F20-Media-Images" 2>/dev/null || true
move_file "$DOCS_DIR/GALLERY_IMAGE_ORDERING.md" "$DOCS_DIR/F20-Media-Images" 2>/dev/null || true

# N1: Backend Framework
echo "→ N1: Backend Framework"
move_file "$DOCS_DIR/AGENT.md" "$DOCS_DIR/N1-Backend-Framework" 2>/dev/null || true
move_file "$DOCS_DIR/AGENT_DEFAULT.md" "$DOCS_DIR/N1-Backend-Framework" 2>/dev/null || true
move_file "$DOCS_DIR/ADDING_ATTRIBUTE_TO_MODEL.md" "$DOCS_DIR/N1-Backend-Framework" 2>/dev/null || true
move_file "$DOCS_DIR/SETTINGS_ATTRIBUTES_VALIDATION_FIX.md" "$DOCS_DIR/N1-Backend-Framework" 2>/dev/null || true

# N2: Frontend Framework
echo "→ N2: Frontend Framework"
move_file "$DOCS_DIR/DASH_DESIGN_SYSTEM_VARIABLES.md" "$DOCS_DIR/N2-Frontend-Framework" 2>/dev/null || true

# N3: Infrastructure & CI/CD
echo "→ N3: Infrastructure & CI/CD"
move_file "$DOCS_DIR/HTTP2.md" "$DOCS_DIR/N3-Infrastructure-CI-CD" 2>/dev/null || true

# N5: Desktop & Device Service
echo "→ N5: Desktop & Device Service"
move_file "$DOCS_DIR/REDIS_PREDIS_CHAT.md" "$DOCS_DIR/N5-Desktop-Device-Service" 2>/dev/null || true

# N8: Observability
echo "→ N8: Observability"
# Cloudwatch file already moved to F18, but could also go here

# General utilities
echo "→ General Utilities"
move_file "$DOCS_DIR/TYPESCRIPT_INTERFACE_GENERATION.md" "$DOCS_DIR/General-Utilities" 2>/dev/null || true
move_file "$DOCS_DIR/FRONTEND_ATTRIBUTES_FIELD_FIX.md" "$DOCS_DIR/General-Utilities" 2>/dev/null || true
move_file "$DOCS_DIR/FRONTEND_TENANT_ATTRIBUTES_REFACTORING.md" "$DOCS_DIR/General-Utilities" 2>/dev/null || true
move_file "$DOCS_DIR/PLANS_PAGE_FIXES.md" "$DOCS_DIR/General-Utilities" 2>/dev/null || true

echo ""
echo "✅ Files reorganized"
echo ""

# Step 4: Move remaining tech docs
echo "📚 Moving tech folder contents to appropriate epics..."
if [ -d "$DOCS_DIR/tech" ]; then
    # Move domain-models
    if [ -d "$DOCS_DIR/tech/domain-models" ]; then
        # These are already referenced above, but move any remaining
        mv "$DOCS_DIR/tech/domain-models"/* "$DOCS_DIR/F1-Orders-and-Tabs/" 2>/dev/null || true
    fi

    # Move architecture docs to N1
    if [ -d "$DOCS_DIR/tech/architecture" ]; then
        mv "$DOCS_DIR/tech/architecture"/* "$DOCS_DIR/N1-Backend-Framework/" 2>/dev/null || true
    fi

    # Move deployment docs to N3
    if [ -d "$DOCS_DIR/tech/deployment" ]; then
        mv "$DOCS_DIR/tech/deployment"/* "$DOCS_DIR/N3-Infrastructure-CI-CD/" 2>/dev/null || true
    fi

    # Move toolchain docs to N4
    if [ -d "$DOCS_DIR/tech/toolchain" ]; then
        mv "$DOCS_DIR/tech/toolchain"/* "$DOCS_DIR/N4-Build-Toolchain/" 2>/dev/null || true
    fi

    # Move features docs to appropriate epics
    if [ -d "$DOCS_DIR/tech/features" ]; then
        # This is complex, move the whole features folder for now
        mv "$DOCS_DIR/tech/features"/* "$DOCS_DIR/General-Utilities/" 2>/dev/null || true
    fi

    # Move any remaining tech files
    mv "$DOCS_DIR/tech"/*.md "$DOCS_DIR/General-Utilities/" 2>/dev/null || true

    # Clean up empty tech folder
    rmdir "$DOCS_DIR/tech" 2>/dev/null || true
fi

# Move system folder
if [ -d "$DOCS_DIR/system" ]; then
    mv "$DOCS_DIR/system"/* "$DOCS_DIR/General-Utilities/" 2>/dev/null || true
    rmdir "$DOCS_DIR/system" 2>/dev/null || true
fi

# Move archive folder
if [ -d "$DOCS_DIR/archive" ]; then
    mv "$DOCS_DIR/archive"/* "$DOCS_DIR/Archive/" 2>/dev/null || true
    rmdir "$DOCS_DIR/archive" 2>/dev/null || true
fi

echo "✅ Tech and utility folders consolidated"
echo ""

# Step 5: Summary
echo "📊 Summary"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""
echo "New structure:"
ls -d "$DOCS_DIR"/F* "$DOCS_DIR"/N* "$DOCS_DIR"/General* "$DOCS_DIR"/Archive 2>/dev/null | xargs -I {} basename {} | sort
echo ""
echo "✅ Reorganization complete!"
echo ""
echo "Next steps:"
echo "1. Review the new structure: ls -la $DOCS_DIR"
echo "2. Move feature docs from General-Utilities to specific epic folders"
echo "3. If satisfied, delete the backup: rm -rf $BACKUP_DIR"
echo "4. Update any internal documentation links"
