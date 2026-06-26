# Multi-Tenant Association Pattern Applied

## Date
2026-01-27

## Summary
Applied multi-tenant association pattern to all critical e-commerce resources that implement multi-tenancy. This ensures that resources created by TenancyAdmin users are:
1. Properly associated with the tenancy via `tenancy_id`
2. Auto-associated with all tenants in the tenancy (unless specific `tenant_ids` are provided)
3. Visible in list queries that filter by `tenancy_id`

## Pattern Implementation

### Controllers Updated (6 total)

#### 1. **PricelistController** ✅
- **_create()**: Sets `tenancy_id`, auto-associates with all tenancy tenants
- **_update()**: Handles `tenant_ids` sync
- **is_primary scope**: Uses `tenancy_id` instead of `tenant_id`
- **Load relationship**: `tenants`

#### 2. **BrandController** ✅
- **_create()**: Sets `tenancy_id`, auto-associates with all tenancy tenants
- **_update()**: Handles `tenant_ids` sync
- **is_primary scope**: Uses `tenancy_id` instead of `tenant_id`
- **Load relationship**: `tenants`

#### 3. **CategoryController** ✅
- **_create()**: Sets `tenancy_id`, auto-associates with all tenancy tenants
- **_update()**: Handles `tenant_ids` sync
- **is_primary scope**: Uses `tenancy_id` instead of `tenant_id`
- **Load relationship**: `tenants`

#### 4. **StockTypeController** ✅
- **_create()**: Sets `tenancy_id`, auto-associates with all tenancy tenants
- **_update()**: Handles `tenant_ids` sync
- **is_primary scope**: Uses `tenancy_id` instead of `tenant_id`
- **Load relationship**: `tenants`

#### 5. **GalleryController** ✅
- **_create()**: Sets `tenancy_id`, auto-associates with all tenancy tenants
- **_update()**: Handles `tenant_ids` sync
- **Load relationship**: `tenants`

#### 6. **ModifierGroupController** ✅
- **_create()**: Sets `tenancy_id`, auto-associates with all tenancy tenants
- **_update()**: Handles `tenant_ids` sync
- **Load relationship**: `tenants`

### Request Files Updated (5 total)

#### 1. **PricelistRequest** ✅
- Uses `MultiTenantRequestTrait`
- `tenant_id`: nullable
- `tenant_ids`: array validation with tenancy scope

#### 2. **BrandRequest** ✅
- Uses `MultiTenantRequestTrait`
- `tenant_id`: nullable
- *(tenant_ids already existed)*

#### 3. **CategoryRequest** ✅
- Uses `MultiTenantRequestTrait` (already had it)
- `tenant_id`: nullable
- `tenant_ids`: array validation with tenancy scope (already existed)

#### 4. **GalleryRequest** ✅
- Uses `MultiTenantRequestTrait` (already had it)
- `tenant_id`: nullable
- `tenant_ids`: **ADDED** - array validation with tenancy scope

#### 5. **ModifierRequest** ✅
- **ADDED** `MultiTenantRequestTrait`
- `tenant_id`: **Changed** from required to nullable
- `tenant_ids`: **ADDED** - array validation with tenancy scope
- **ADDED** `prepareForValidation()` to resolve tenant_id

#### 6. **StockTypeRequest** ✅
- Uses `MultiTenantRequestTrait` (already had it)
- `tenant_id`: nullable (already done)
- *(tenant_ids to be added if needed)*

## Pattern Template

### Controller _create() Method
```php
public function _create($request)
{
    $validated = app($this->requestValidator)->validated();
    $user = $request->user();

    // Set tenancy_id if user has one
    if ($user->tenancy_id) {
        $validated['tenancy_id'] = $user->tenancy_id;
    }

    $item = $this->model->create($validated);

    // Handle multi-tenant association
    if ($user->isTenancyAdmin() && $user->tenancy_id) {
        if (isset($validated['tenant_ids']) && is_array($validated['tenant_ids'])) {
            $item->tenants()->sync($validated['tenant_ids']);
        } else {
            // Auto-associate with all tenants in tenancy
            $tenantIds = \Domain\App\Models\Extended\Tenant::where('tenancy_id', $user->tenancy_id)
                ->pluck('id')->toArray();
            $item->tenants()->sync($tenantIds);
        }
    } elseif (isset($validated['tenant_ids'])) {
        $item->tenants()->sync($validated['tenant_ids']);
    } elseif ($user->tenant_id) {
        $item->tenants()->sync([$user->tenant_id]);
    }

    // Update is_primary scope if applicable
    if (isset($item->is_primary) && $item->is_primary) {
        Model::query()
            ->where('tenancy_id', $item->tenancy_id)
            ->where('is_primary', true)
            ->where('id', '!=', $item->id)
            ->update(['is_primary' => false]);
    }

    $item->load('tenants');
    return ResourceClass::make($item);
}
```

### Controller _update() Method
```php
public function _update($request, $id, $item)
{
    $validated = app($this->requestValidator)->validated();
    $item->update($validated);

    // Handle tenant_ids sync if provided
    if (isset($validated['tenant_ids']) && is_array($validated['tenant_ids'])) {
        $item->tenants()->sync($validated['tenant_ids']);
    }

    // Update is_primary scope if applicable
    if (isset($item->is_primary) && $item->is_primary) {
        Model::query()
            ->where('tenancy_id', $item->tenancy_id)
            ->where('is_primary', true)
            ->where('id', '!=', $item->id)
            ->update(['is_primary' => false]);
    }

    $item->load('tenants');
    return ResourceClass::make($item);
}
```

### Request Validation
```php
use Domain\App\Http\Traits\MultiTenantRequestTrait;

class ResourceRequest extends FormRequest
{
    use MultiTenantRequestTrait;

    protected function prepareForValidation()
    {
        $this->resolveTenantId();
    }

    public function rules()
    {
        return [
            'tenant_id' => [
                'nullable',
                'uuid',
                Rule::exists('tenants', 'id')
                    ->when(
                        !$this->user()->isSystemAdmin(),
                        fn($query) => $query->where('id', $this->user()->tenant_id)
                    )
                    ->withoutTrashed()
            ],
            'tenant_ids' => 'sometimes|array',
            'tenant_ids.*' => [
                'required',
                'uuid',
                'distinct',
                Rule::exists('tenants', 'id')
                    ->when(
                        $this->getTenancyIdForValidation(),
                        fn($query) => $query->where('tenancy_id', $this->getTenancyIdForValidation())
                    )
                    ->withoutTrashed()
            ],
        ];
    }
}
```

## User Scenarios Covered

### Scenario 1: TenancyAdmin creates resource without specifying tenant_ids
- `tenancy_id` is automatically set from user
- Resource is auto-associated with ALL tenants in the tenancy
- Resource appears in list queries for TenancyAdmin (filtered by `tenancy_id`)

### Scenario 2: TenancyAdmin creates resource with specific tenant_ids
- `tenancy_id` is automatically set from user
- Resource is associated ONLY with specified tenants
- Resource appears in list queries for TenancyAdmin (filtered by `tenancy_id`)

### Scenario 3: TenantAdmin/User creates resource
- `tenancy_id` is automatically set from user (if they have one)
- Resource is associated with their specific tenant
- Resource appears in their filtered queries

### Scenario 4: SystemAdmin creates resource
- Can set `tenancy_id` explicitly or leave null
- Can specify `tenant_ids` explicitly
- Full control over associations

## Root Cause Resolved

**Original Issue**: Resources created by TenancyAdmin were not appearing in list queries because:
1. `tenancy_id` was not being set on creation
2. No entries were created in pivot tables (e.g., `pricelist_tenants`)
3. `ResourceVisibility` trait filters by `where('tenancy_id', $user->tenancy_id)` for TenancyAdmin users
4. Since `tenancy_id` was NULL, the query excluded the resources

**Solution**: Automatically set `tenancy_id` and create pivot table associations during resource creation.

## Testing Checklist

For each updated controller, verify:
- [ ] TenancyAdmin can create resource without tenant_ids
- [ ] Created resource appears in list for TenancyAdmin
- [ ] Resource is associated with all tenancy tenants
- [ ] TenancyAdmin can create resource with specific tenant_ids
- [ ] Created resource is associated only with specified tenants
- [ ] TenancyAdmin can update resource tenant_ids
- [ ] `is_primary` flag works with tenancy scope (not tenant scope)
- [ ] TenantAdmin/User can create and see their resources
- [ ] for all cases the tenancy_id must be resolved automatically from the user performing the operation.
- [ ] if no tenant_ids provided we will assume all the current tenants of the tenancy. 
- [ ] SystemAdmin has full control (must specify tenant_ids or tenancy_id)

## Files Modified

### Controllers (6 files)
1. `/domain/app/Http/Controllers/API/ECommerce/PricelistController.php`
2. `/domain/app/Http/Controllers/API/ECommerce/BrandController.php`
3. `/domain/app/Http/Controllers/API/ECommerce/CategoryController.php`
4. `/domain/app/Http/Controllers/API/ECommerce/StockTypeController.php`
5. `/domain/app/Http/Controllers/API/ECommerce/GalleryController.php`
6. `/domain/app/Http/Controllers/API/ECommerce/ModifierGroupController.php`

### Requests (5 files)
1. `/domain/app/Http/Request/ECommerce/PricelistRequest.php`
2. `/domain/app/Http/Request/ECommerce/BrandRequest.php`
3. `/domain/app/Http/Request/ECommerce/CategoryRequest.php`
4. `/domain/app/Http/Request/ECommerce/GalleryRequest.php`
5. `/domain/app/Http/Request/ECommerce/ModifierRequest.php`

## Additional Notes

- **MultiTenantRequestTrait** provides consistent tenant/tenancy resolution across all Request files
- All pivot tables follow the naming convention: `{model}_tenants`
- The `tenants` relationship should always be loaded in responses to include association information
- For resources with `is_primary` flag, the scope check uses `tenancy_id` instead of `tenant_id`

## Related Documentation

- See `/domain/app/Http/Traits/ECommerce/ResourceVisibility.php` for query filtering logic
- See `/domain/app/Http/Traits/MultiTenantRequestTrait.php` for tenant resolution logic
- See `2026_01_27_010000_add_multi_tenant_support_to_remaining_ecommerce_tables.php` migration

## Next Steps

1. Test all updated controllers with TenancyAdmin, TenantAdmin, and SystemAdmin roles
2. Run SQL fix script for any existing records that need tenancy_id and pivot associations
3. Consider applying same pattern to other controllers as needed (e.g., Currency, Marketplace, PointOfSale, Campaign, ProductTemplate)



# Product import instances note:

Creating a ProductImportInstance

How it works now:

User Role	tenant_id provided?	tenant_ids provided?	Result
TenancyAdmin	No	No	Auto-associate with ALL tenants in tenancy
TenancyAdmin	No	Yes	Use provided tenant_ids
TenancyAdmin	Yes	No	Use single tenant_id
Regular Admin	Yes	No	Use single tenant_id (required)
The imported products can later be associated with all the tenants stored in options.tenant_ids during the import processing phase.

Creating a ProductImportInstance as a TenancyAdmin without providing tenant_id. The system will automatically:
Set tenancy_id from your user account
Resolve all tenants in your tenancy for product association
Use the first tenant for file storage path organization


#

Instead of checking if a tenants() method exists (which would return true for MetadataFormat even though its pivot table has incompatible column types), I now use an explicit whitelist of models that have properly configured tenants() many-to-many relationships:

<?php
protected static array $modelsWithTenantsRelationship = [
    \Domain\App\Models\ECommerce\Product::class,
];

Only models in this whitelist will have the orWhereHas('tenants', ...) clause applied. To enable multi-tenant filtering for other models in the future, you just need to:

Ensure the pivot table has compatible column types (UUID for both foreign keys)
Add the model class to the $modelsWithTenantsRelationship array
This prevents the SQL type mismatch error for models like MetadataFormat that have a tenants() relationship defined but with an improperly configured pivot table.


Notes:

User Role	tenant_id provided?	tenant_ids provided?	Result
TenancyAdmin	No	No	Auto-associate with ALL tenants in tenancy
TenancyAdmin	No	Yes	Use provided tenant_ids
TenancyAdmin	Yes	No	Use single tenant_id
Regular Admin	Yes	No	Use single tenant_id (required)


For TenancyAdmin users: Resources should be created with tenancy_id only (no tenant_id)
Tenant associations: Use tenant_ids array to associate products with specific tenants via the resource_tenants pivot
Visibility: TenancyAdmin sees all resources with their tenancy_id OR resources associated via tenants() relationship
Backward compatibility: Keep tenant_id field but deprecate it

ResourceVisibility - TenancyAdmin see entities associated via tenants() relationship where the tenant belongs to their tenancy


How it works now:
User Role	tenant_id	Validation Behavior
TenantAdmin	Required (their tenant)	Resources must belong to their specific tenant
TenancyAdmin	Nullable	Resources can belong to ANY tenant in their tenancy
SystemAdmin	Required	Can access any tenant


Deprecating tenant_id in favor of tenant_ids:
In this case I'm a TenancyAdmin role user, creating a resource 
as I'm TenancyAdmin role, the resource shall be associated IMPLICITELY to all tenants belonging to the TenancyAccount.
tenant_id will be deprecated, in favor of tenant_ids. 
If the TenancyAdmin choose optionally to set the resource to some tenants, through the fillable tenant_ids then that explicit association will allow to filter later. but implicitely they will show all tenants of a TenancyAccount, this will be the global default behaviour for all the models we will review today. 





After a change applied Example: 

Summary of Changes
1. MarketplaceRequest.php - Updated validation rules
Added MultiTenantRequestTrait
Added resolveTenantId() call in prepareForValidation()
Made tenant_id nullable (was required)
Added tenant_ids array validation with tenancy scope
Fixed tenant_system_marketplace_id validation for TenancyAdmin users (uses custom closure to check tenant belongs to their tenancy)
2. PointOfSaleRequest.php - Updated validation rules
Added MultiTenantRequestTrait
Added resolveTenantId() call in prepareForValidation()
Made tenant_id nullable (added it - was not present before)
Added tenant_ids array validation with tenancy scope
Fixed tenant_system_point_of_sale_id validation for TenancyAdmin users
3. MarketplaceController.php - Added multi-tenant association
Updated _preList() to eager load tenants relationship
Updated _postGetOne() to load tenants relationship
Updated _create() to:
Set tenancy_id from user
Auto-associate with all tenancy tenants (for TenancyAdmin)
Or use provided tenant_ids if specified
Load tenants relationship before returning
Updated _update() to sync tenant_ids if provided
4. PointOfSaleController.php - Added multi-tenant association
Updated _preList() to eager load tenants relationship
Updated _postGetOne() to load tenants relationship
Updated _create() to handle multi-tenant association (same pattern)
Updated _update() to sync tenant_ids if provided
5. MarketplaceResource.php - Added tenant fields
Added tenancy_id, tenant_id, tenant_ids, tenants fields
6. PointOfSaleResource.php - Added tenant fields
Added tenancy_id, tenant_id, tenant_ids, tenants fields
7. ResourceVisibility.php (ECommerce trait) - Fixed TenancyAdmin visibility
Fixed scopeVisibleThroughRelationTenant() to properly check tenant's tenancy_id (uses tenant IDs lookup instead of direct tenancy_id on relation)
8. ResourceVisibility.php (App trait) - Added TenancyAdmin support
Added TenancyAdmin support to scopeVisibleThroughTenant()
Fixed scopeVisibleThroughRelationTenant() for TenancyAdmin (same fix)
Now TenancyAdmin users can:

Create marketplaces/POS without specifying tenant_id (auto-sets tenancy_id)
Auto-associate resources with all tenants in their tenancy
Optionally specify specific tenant_ids for selective association
See all marketplaces/POS within their tenancy in list queries
Response includes tenant_ids and tenants arrays