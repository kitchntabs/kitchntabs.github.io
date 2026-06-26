# Tenant Initial Provisioning

## Overview

When a new **Domain Tenant** (`Domain\App\Models\Extended\Tenant`) is created, it is automatically provisioned with default resources required for e-commerce operations:
- **Default Currency** (if not already attached)
- **Default Pricelist** (primary)
- **Default Stock Type** (primary)

**Note:** This provisioning **only works for Domain Tenant models**, not the base `App\Models\Tenant`. The trait gracefully skips provisioning if the model doesn't have the required relationships.

## Implementation

### Architecture Decision

**The provisioning logic is implemented in the MODEL using a TRAIT**, not in the controller.

**Location:** `/domain/app/Models/Extended/Traits/TenantInitialProvision.php`

**Why in the Model/Trait?**
1. ✅ **Separation of Concerns**: Business logic belongs in the model layer
2. ✅ **Consistency**: Works regardless of creation method (API, factory, seeder, CLI, console, etc.)
3. ✅ **Testability**: Easier to test in isolation
4. ✅ **DRY Principle**: No need to duplicate logic across multiple controllers/commands
5. ✅ **Automatic**: Uses Eloquent model events (`created` event) to trigger automatically
6. ✅ **Resilient**: Gracefully skips if model doesn't have required relationships

### How It Works

The `TenantInitialProvision` trait is used by the Domain `Tenant` model:

```php
class Tenant extends BaseTenant implements HasMedia
{
    use InteractsWithMedia, TenantInitialProvision;
    // ...
}
```

When a Domain tenant is created, the trait's `bootTenantInitialProvision()` method listens to the `created` event and calls `provisionInitialResources()`.

The trait checks if the required relationships exist before attempting provisioning, making it safe to use with both base and domain models.

### Provisioning Flow

1. **Check for Required Relationships**
   - Verifies model has `currencies()`, `pricelists()`, and `stockTypes()` methods
   - Skips provisioning if relationships don't exist (base Tenant model)

2. **Ensure Default Currency**
   - Checks if tenant has currencies attached
   - If not, attaches system default currency (or first available)
   - Sets it as primary

3. **Provision Default Pricelist**
   - Creates a pricelist named "Default Pricelist"
   - Uses tenant's primary currency
   - Sets `is_primary = true`
   - Sets `is_internal = false`

4. **Provision Default Stock Type**
   - Creates a stock type named "Default Stock"
   - Sets `is_primary = true`
   - Sets `is_internal = false`

## Relationships

```
Tenant (1) ─── (M) Pricelist
  └─ tenant_id, name (unique constraint)
  └─ is_primary, is_internal (boolean flags)

Tenant (1) ─── (M) StockType
  └─ tenant_id, name (unique constraint)
  └─ is_primary, is_internal (boolean flags)

Tenant (M) ──< (M) Currency (via pivot table)
  └─ pivot: is_primary (boolean flag)
```

## Testing

Tests verify the provisioning behavior for **Domain Tenant models only**.

### Domain Tenant Provisioning Tests

**Location:** `/tests/Feature/API/Domain/TenantProvisioningTest.php`

#### 1. `test_domain_tenant_is_provisioned_with_default_pricelist_and_stock_type`
- Creates Domain tenant directly via Eloquent
- Verifies currency attachment
- Verifies default pricelist exists with correct properties
- Verifies default stock type exists with correct properties

#### 2. `test_domain_tenant_created_via_factory_is_also_provisioned`
- Creates Domain tenant using Factory
- Ensures provisioning works regardless of creation method
- Verifies currency, pricelist, and stock type are created

#### 3. `test_domain_tenant_with_existing_currency_uses_it_for_pricelist`
- Verifies that pricelist uses tenant's attached currency
- Tests currency-pricelist relationship

#### 4. `test_provisioning_is_idempotent`
- Tests behavior when provisionInitialResources is called multiple times
- Documents current behavior (duplicates may be created)

### Running the Tests

```bash
# Run all Domain provisioning tests
php artisan test tests/Feature/API/Domain/TenantProvisioningTest.php

# Or run a specific test
php artisan test --filter=test_domain_tenant_is_provisioned_with_default_pricelist_and_stock_type
```

### Base Tenant Tests

The base `App\Models\Tenant` tests remain in:
**Location:** `/tests/Feature/API/SystemAdmin/SystemAdminTenantManagementTest.php`

These tests focus on:
- System admin CRUD operations
- Authorization (normal users, tenant admins)
- Settings and attributes management

Base tenants **do not** get automatic provisioning since they lack the required relationships.

## Usage Examples

### Via Domain Tenant Eloquent
```php
use Domain\App\Models\Extended\Tenant;

$tenant = Tenant::create([
    'name' => 'New Company',
    'public_id' => '12.345.678-9',
]);
// Automatically provisions:
// - Default currency attachment
// - Default pricelist
// - Default stock type
```

### Via Domain Tenant Factory
```php
use Domain\App\Models\Extended\Tenant;

$tenant = Tenant::factory()->create();
// Automatically provisions all default resources
```

### Base Tenant (No Provisioning)
```php
use App\Models\Tenant;

$tenant = Tenant::create([
    'name' => 'Base Tenant',
    'public_id' => '12.345.678-9',
]);
// No provisioning - base model lacks required relationships
// Trait gracefully skips provisioning
```

## Customization

To modify the default values, edit the trait methods:

- `ensureDefaultCurrency()` - Currency attachment logic
- `provisionDefaultPricelist()` - Pricelist creation logic  
- `provisionDefaultStockType()` - Stock type creation logic

## Dependencies

- `Domain\App\Models\Common\Currency`
- `Domain\App\Models\ECommerce\Pricelist`
- `Domain\App\Models\ECommerce\StockType`

## Error Handling

- If no currency exists in the system, a warning is logged and provisioning continues
- If currency attachment fails, pricelist creation is skipped
- All operations are logged for debugging

## Future Enhancements

Potential improvements:
- Make default names configurable via config file
- Allow skipping provisioning via flag
- Support custom provisioning templates per tenant type
- Add events/hooks for custom provisioning logic
