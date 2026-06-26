# Tenancy Account Feature 
## High Level overview:

The Tenancy Account feature introduces a higher-level abstraction (Tenancy model) above existing Tenant models.

### Overview: 
The “TenancyAccount” term, refers to the Tenancy Model.

### Reference models:
App\Models\Tenancy

### Tenancy Lifecycle (state machine):

ACTIVE → CANCELED → SUSPENDED → SOFT_DELETED → (Permanent Deletion)
           ↓
        EXPIRED (alternative path for non-payment)
           ↓
       SUSPENDED → SOFT_DELETED → (Permanent Deletion)

## System Roles Reference
- System Admin (level 0) - Full system access
- TenancyAdmin (level 1) - Manages entire tenancy account
- Tenant (level 2) - Manages single tenant (restaurant)
- User and other custom roles (level 3 and level 3+) - Standard user access

## Tenancy provisioning

  ┌─────────────┐
  │   Guest     │
  │   User      │
  └──────┬──────┘
         │
         │ 1. POST /api/trial/register
         │    (email, password, public_id, public_name, name, lastname, etc.)
         ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │              TrialRegistrationController::register()              
  │                                                                  
  │  - Validate input (unique email on users AND pending_registrations)
  │  - Verify reCAPTCHA (if enabled)                                
  │  - Create PendingRegistration record                            
  │  - Generate 64-char verification_token                          
  │  - Set expires_at = now + 24 hours                             
  │  - Send TrialVerificationMail                                   
  └──────────────────────┬───────────────────────────────────────────┘
                         │
                         │ Creates PendingRegistration
                         │ status: 'pending'
                         ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                    pending_registrations table                    
  │                                                                  
  │  - id (UUID)                                                    
  │  - email, password (hashed), name, lastname                     
  │  - public_id, public_name                                       
  │  - phone, primary_language, primary_currency, primary_timezone  
  │  - verification_token (64-char random string)                   
  │  - plan_id (optional, default plan used if null)               
  │  - status: 'pending' | 'verified' | 'provisioning' | 'provisioned' | 'failed'
  │  - expires_at (24 hours from creation)                         
  │  - metadata (ip, user_agent, timestamps)                       
  └──────────────────────────────────────────────────────────────────┘
                         │
                         │ Email sent
                         ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                    TrialVerificationMail                          
  │                                                                  
  │  Link: {frontend_url}/trial/verify?id={uuid}&token={token}&lang={lang}
  │  Expiration: 24 hours from registration                         
  └──────────────────────────────────────────────────────────────────┘
                         │
                         │ User clicks link
                         │ 2. GET /api/trial/verify/{id}/{token}
                         ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │           TrialRegistrationController::verifyEmail()             
  │                                                                  
  │  - Find PendingRegistration by id                               
  │  - Check not expired (expires_at > now)                         
  │  - Verify token matches (hash_equals)                           
  │  - Mark as verified (status: 'verified', email_verified_at: now)
  │  - Dispatch TenancyProvisioningJob                              
  └──────────────────────┬───────────────────────────────────────────┘
                         │
                         │ Job dispatched to Horizon queue
                         ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                   TenancyProvisioningJob                          
  │                                                                  
  │  Queue: default (Horizon)                                       
  │  Tries: 1                                                       
  │  Unique: tenancy-provisioning-{pending_id} (3600s lock)        
  │                                                                  
  │  Flow:                                                          
  │  1. Find PendingRegistration                                    
  │  2. Check not already provisioned or expired                    
  │  3. Mark as 'provisioning'                                      
  │  4. Get subscription plan (from pending or default)             
  │  5. Call TenancyProvisioningService::provisionTenancy()        
  │  6. Create default ecommerce resources                          
  │  7. Mark as 'provisioned' with metadata                        
  │  8. Soft delete the pending registration                        
  │  9. Send TrialWelcome email                                     
  └──────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │            TenancyProvisioningService::provisionTenancy()      
  │                                                                
  │  All operations wrapped in DB::transaction()                   
  │                                                                
  │  1. Create Tenancy                                             
  │     - public_id, public_name, legal_name, email, slug          
  │     - status: 'active'                                         
  │     - primary_language, primary_currency, primary_timezone     
  │                                                                
  │  2. Create Default Tenant                                      
  │     - name: "{tenancy.public_name} - Main"                     
  │     - Link primary language & currency                         
  │                                                                
  │  3. Create User                                                
  │     - Link to tenancy and tenant                               
  │     - email_verified_at: now (already verified)                
  │                                                                
  │  4. Assign Roles                                               
  │     - TenancyAdmin (level 1, redirect: /tenancy)               
  │     - Tenant (level 2)                                         
  │                                                                
  │  5. Create Subscription                                        
  │     - Link to selected/default plan                            
  │     - trial_ends_at: now + plan.trial_days (usually 30 days)   
  │     - status: 'on_trial'                                       
  │                                                                
  │  6. Associate Payment Gateways                                 
  │     - Link all active SystemPaymentGateways                    
  │                                                                
  │  7. Sync Plan Addons                                           
  │     - Enable marketplaces from plan (UberEats, etc.)          
  │     - Enable point of sales from plan                          
  └──────────────────────────────────────────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │       TenancyProvisioningService::createDefaultResources()      
  │                                                                 
  │  Creates localized default ecommerce resources:                 
  │                                                                 
  │  1. Default Category                                            
  │     - name: "Categoría Principal" (es) / "Main Category" (en)  
  │     - is_primary: true                                         
  │                                                                 
  │  2. Default Gallery                                             
  │     - title: "Galería de Ejemplo" (es) / "Sample Gallery" (en) 
  │                                                                 
  │  3. Default Brand                                               
  │     - name: {tenancy.public_name}                              
  │     - is_primary: true                                         
  │                                                                 
  │  4. Default PriceList                                           
  │     - name: "Lista de Precios Principal" / "Main Price List"   
  │     - currency: primary_currency                               
  │     - is_primary: true                                         
  │                                                                 
  │  5. Default StockType                                           
  │     - name: "Bodega Principal" / "Main Warehouse"              
  │     - is_primary: true                                         
  └──────────────────────────────────────────────────────────────────┘
                         │
                         │ Welcome email sent
                         ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                      Account Ready                              
  │                                                                 
  │  User can now login at /login with their email/password         
  │  They will be redirected to /tenancy (TenancyAdmin dashboard)   
  └──────────────────────────────────────────────────────────────────┘


### Key Files

| File | Purpose |
|------|---------|
| `app/Http/Controllers/API/Auth/TrialRegistrationController.php` | Handles registration, email verification, resend, status check |
| `app/Models/PendingRegistration.php` | Model for pending registrations with soft deletes |
| `app/Jobs/TenancyProvisioningJob.php` | Queued job that orchestrates provisioning |
| `app/Services/Tenancy/TenancyProvisioningService.php` | Core service for creating tenancy, user, tenant, subscription |
| `app/Services/Tenancy/TenancySubscriptionService.php` | Handles subscription creation |
| `app/Mail/TrialVerificationMail.php` | Email with verification link |
| `app/Mail/TrialWelcome.php` | Welcome email after successful provisioning |
| `app/Mail/TenancyProvisioningFailed.php` | Failure notification email |


## PendingRegistration Model Lifecycle:

When a tenancy is registered, it falls into a registration state machine lifecycle
to monitor the state of the registrations. 

```
pending → verified → provisioning → provisioned → (soft deleted)
                 ↘                ↘
                  → expired        → failed
```

| Status | Description |
|--------|-------------|
| `pending` | Created, awaiting email verification |
| `verified` | Email verified, awaiting provisioning |
| `provisioning` | Provisioning job is running |
| `provisioned` | Successfully provisioned, record soft-deleted |
| `failed` | Provisioning failed, user notified via email |

## Subscription Plan & Trial Period

When a tenancy is registered, it assigns a default subscription plan.
Note: The default plan, is often the free-plan with the trial period.
As we handle the subscription internally, in the current Kitchntabs scenario
The subscription is not associated to the payment gateways, that often offer 
the subscription handling, the default association is decoupled from the payment gateways subscription handling
therefore it gets as an internal subscription only.

- **Default Plan:** First active plan with `is_default: true`, or lowest tier active plan
- **Trial Period:** `trial_days` from the plan (typically 30 days)
- **Trial End Date:** `trial_ends_at = now + plan.trial_days`
- **Initial Status:** `on_trial`

## Plan Addons (Marketplaces & POS)

When provisioning, the system syncs addons based on the subscription plan:

1. **Marketplaces:** UberEats, Rappi, PedidosYa, etc.
   - Defined in `config/subscription_plans.php` → `addon_formats`
   - Linked via `tenant_system_marketplace` pivot table

2. **Point of Sales:** KitchnTabs POS, etc.
   - Linked via `tenant_system_point_of_sale` pivot table

## Cleanup System

Stale pending registrations are automatically cleaned up:

- **Schedule:** Daily at 3 AM via `registrations:cleanup` command
- **Threshold:** `PENDING_REGISTRATIONS_CLEANUP_HOURS` env (default: 48 hours)
- **Targets:** Expired, provisioned (soft-deleted), or failed records older than threshold
- **Action:** Soft delete (preserves audit trail)

**Manual cleanup:**
```bash
sail artisan registrations:cleanup --dry-run  # Preview
sail artisan registrations:cleanup            # Execute
sail artisan registrations:cleanup --hours=72 # Custom threshold
```

## Provisioned Tenancy Resources Summary

After successful provisioning, the following resources exist:

| Resource | Details |
|----------|---------|
| **Tenancy** | Organization-level entity with subscription |
| **Tenant** | "{name} - Main" default store | A default tenant is created and associate to the TenancyAccount.
| **User** | Admin user with TenancyAdmin + Tenant roles | The default AdminUser with TenancyAdmin + Tenant roles.
| **Subscription** | Trial subscription linked to plan | The default plan associated to the TenancyAccount. 
| **Category** | Default primary category | A Default category associated to all the TenancyAccount tenants. 
| **Gallery** | Default gallery | A Default gallery associated to all the TenancyAccount tenants. 
| **Brand** | Brand named after tenancy | A Brand category associated to all the TenancyAccount tenants. 
| **PriceList** | Default price list with primary currency | A Default pricelist associated to all the TenancyAccount tenants. 
| **StockType** | Default warehouse/stock type | A Default stock type associated to all the TenancyAccount tenants. 
| **Payment Gateways** | All active system payment gateways | The TenancyAccount gets associated to all the payment gateway, though this is a tech debt (TD) => The payment gateway association logic on provisioning, must be according some logic, depending on country, region, and currency. 
| **Marketplaces** | Based on plan addons | Accordingly to the subscription plan addons configuration and their system marketplaces mapping, they gets associated on provisioning.
| **Point of Sales** | Based on plan addons | Accordingly to the subscription plan addons configuration and their point of sales mapping, they gets associated on provisioning.

### Relationships

- A Tenancy has many Tenants
- A Tenancy has many Products, each product can be associated to multiple tenants, so they can be availbale to many tenants that the tenancy account manages. 
- A Tenancy has many Users, each user can be associated to a single Tenant. This is important, because most of the application features are tenant based. There is a tenancy panel, and tenant panels. 
- A Tenancy can only have a current subscription, even the model handles multiple subscriptions for the record, only one is current. 
- A Tenancy can have multiple categories, and each category can be associated to multiple tenants. 
- A Tenancy can have multiple galleries, and each gallery can be associated to multiple tenants. 
- A Tenancy can have multiple brands, and each brand can be associated to multiple tenants.
- A Tenancy can have multiple pricelists, and each pricelist can be associated to multiple tenants.
- A Tenancy can have multiple stocktypes, and each stocktype can be associated to multiple tenants. 
- A Tenancy can have multiple modifierGroups, and each modifierGroup can be associated to multiple tenants.
- A Tenancy can have multiple metadataFormats, and each metadataFormat can be associated to multiple tenants.


### Marketplaces and Point of Sales relationships.

...
We need to complete this


# SYSTEM MULTI TENANCY POLICY

## OVERVIEW

### Examples:
- TenancyAdmin can create/update/delete resources without tenant_ids.
- Resource is associated with all tenancy tenants by default if not tenant_ids provided.
- TenancyAdmin can create resource with specific tenant_ids, then created resource is associated only with specified tenants.
- TenantAdmin/User can create and see their resources, which are constrainted by the tenant_id which the tenant level role user belongs (only one).
- for all cases the tenancy_id must be resolved automatically from the user performing the operation.
- if no tenant_ids provided we will assume all the current tenants of the tenancy. 
- SystemAdmin has full control (must specify tenant_ids or tenancy_id)
- Tenant role level users, can only have access to the tenant resources belonging to the tenant associated. 

## STANDARD RESOURCE POLICY:

Models should in general implement the standard multi-tenant authorization policy.

e.g: domain/app/Policies/ECommerce/{Model}Policy.php

manage() - Authorizes based on:
- SystemAdmin → always allowed
- TenancyAdmin → check tenancy_id match OR tenants pivot
- TenantAdmin → check legacy tenant_id OR tenants (tenant_ids) pivot
- delete() - Uses same logic as manage

Note: domain/app/Providers/AuthServiceProvider.php must register the implemented policy: 

## Controller implementation

should implement authorize() calls in {Model}Controller.php:

_update() → $this->authorize('manage', $item)
_delete() → $this->authorize('delete', $item)