# Tenant Attributes Refactoring

## Overview
Refactored tenant contact information from individual database columns to a JSON `attributes` schema, mirroring the existing `settings` implementation.

## Changes Made

### 1. Database Migration
**File:** `database/migrations/Modules/System/2025_10_15_171129_remove_tenant_contact_columns_use_attributes_instead.php`

- Migrates existing data from columns to `attributes` JSON field
- Removes the following columns:
  - `public_name`
  - `address`
  - `phone`
  - `mobile`
  - `contact_name`
  - `contact_email`
  - `contact_phone`
- Includes rollback functionality

### 2. Configuration
**File:** `config/tenants.php`

Added new `attribute_formats` configuration array with the following attributes:
- `public_name` - Public facing name of the tenant
- `address` - Physical address
- `phone` - Primary phone number
- `mobile` - Mobile phone number
- `contact_name` - Primary contact person name
- `contact_email` - Contact email address
- `contact_phone` - Contact person phone number

All attributes are:
- Grouped under 'contact'
- Optional (nullable)
- Editable
- Include validation rules
- Have appropriate field types (string, textarea, email)

### 3. Model Updates
**File:** `app/Models/Tenant.php`

#### Updated Properties:
- **`$fillable`**: Removed old columns, added `attributes`
- **`$casts`**: Added `'attributes' => 'array'`
- **`$attributes`**: Added default `'attributes' => '[]'`

#### New Methods:
```php
public function attribute($name, $default = null)
```
Retrieves an attribute value with fallback to default from config.

```php
public static function getSystemAttributeFormats()
```
Returns the attribute formats from the config file.

### 4. Request Validation
**File:** `app/Http/Requests/API/System/TenantRequest.php`

#### Removed Validation Rules:
- All individual contact field rules (public_name, address, phone, etc.)

#### Added Methods:
```php
public function getAttributeRules()
```
Dynamically generates validation rules for attributes based on `attribute_formats` config.

#### Updated:
- `rules()` method now merges both setting and attribute rules

### 5. Controller
**File:** `app/Http/Controllers/API/System/TenantController.php`

#### Updated Method:
```php
public function getSystemSettingFormats()
```
API endpoint now returns both setting and attribute format definitions in a single response:
```php
return ResponseHandler::json([
    'data'  => [
        'setting_formats' => $settingFormats,
        'attribute_formats' => $attributeFormats
    ],
    'total' => count($settingFormats) + count($attributeFormats)
]);
```

#### Deprecated Method:
```php
public function getSystemAttributeFormats()
```
Still available for backward compatibility but deprecated. Recommended to use `getSystemSettingFormats()` instead.

### 6. Routes
**File:** `routes/system.php`

#### Updated Route:
```php
GET /api/system/tenant/systemSettingFormats
```
Now returns both settings and attributes formats.

#### Existing Route (Deprecated):
```php
GET /api/system/tenant/systemAttributeFormats
```
Still available for backward compatibility.

### 7. Resource
**File:** `app/Http/Resources/TenantResource.php`

#### Updated:
- Removed individual contact field mappings
- Added `attributes` to the resource output
- Attributes are included when `includeSettings` is true

### 8. Factory
**File:** `database/factories/TenantFactory.php`

#### Updated:
- Removed individual contact field definitions
- Added `attributes` array with faker-generated contact data

### 9. Tests
**File:** `tests/Feature/API/SystemAdmin/SystemAdminTenantManagementTest.php`

#### New Tests:
1. `test_system_admin_can_get_tenant_list()` - Verify tenants list includes attributes
2. `test_system_admin_can_get_single_tenant()` - Verify single tenant includes attributes
3. `test_system_admin_can_update_tenant_settings()` - Test settings update
4. `test_system_admin_can_update_tenant_attributes()` - Test attributes update
5. `test_system_admin_can_update_both_settings_and_attributes()` - Test combined update
6. `test_can_get_system_setting_formats()` - Verify settings format endpoint
7. `test_can_get_system_attribute_formats()` - Verify attributes format endpoint
8. `test_attribute_validation_rules_are_enforced()` - Test email validation
9. `test_can_create_tenant_with_attributes()` - Test creating tenant with attributes

## API Endpoints

### Existing (Updated):
- `GET /api/system/tenant` - Returns tenants with `attributes` field
- `GET /api/system/tenant/{id}` - Returns tenant with `attributes` field
- `PUT /api/system/tenant/{id}` - Accepts `attributes` in request body
- `POST /api/system/tenant` - Accepts `attributes` in request body

### New:
- `GET /api/system/tenant/systemAttributeFormats` - Returns attribute format definitions

## Usage Examples

### Creating a Tenant with Attributes
```php
POST /api/system/tenant
{
    "name": "My Company",
    "public_id": "12.345.678-9",
    "attributes": {
        "public_name": "My Public Company Name",
        "address": "123 Main Street",
        "phone": "+1-555-1234",
        "mobile": "+1-555-5678",
        "contact_name": "John Doe",
        "contact_email": "john@example.com",
        "contact_phone": "+1-555-9012"
    }
}
```

### Updating Tenant Attributes
```php
PUT /api/system/tenant/1
{
    "name": "My Company",
    "public_id": "12.345.678-9",
    "attributes": {
        "public_name": "Updated Name",
        "phone": "+1-555-0000"
    }
}
```

### Accessing Attributes in Code
```php
$tenant = Tenant::find(1);

// Using the attribute() method with default fallback
$publicName = $tenant->attribute('public_name');
$phone = $tenant->attribute('phone', 'No phone provided');

// Direct access to attributes array
$address = $tenant->attributes['address'] ?? null;
```

### Getting Attribute Formats
```php
$formats = Tenant::getSystemAttributeFormats();
// Returns array from config('tenants.attribute_formats')
```

## Migration Instructions

### To Apply Changes:
```bash
./vendor/bin/sail artisan migrate
```

### To Rollback:
```bash
./vendor/bin/sail artisan migrate:rollback
```

## Testing

Run the test suite:
```bash
./vendor/bin/sail artisan test --filter=SystemAdminTenantManagementTest
```

## Benefits

1. **Consistency**: Attributes now work exactly like settings
2. **Flexibility**: Easy to add new attributes via config without database migrations
3. **Maintainability**: Single JSON column instead of multiple columns
4. **Extensibility**: Frontend can dynamically render form fields based on attribute_formats
5. **Validation**: Centralized validation rules in config
6. **Type Safety**: All attributes properly typed and validated

## Breaking Changes

⚠️ **Important**: This is a breaking change for:
- Any code directly accessing old column properties (e.g., `$tenant->public_name`)
- Frontend forms expecting individual fields instead of attributes object
- API clients expecting old field structure

### Migration Path:
Replace direct property access with attribute method:
```php
// Old
$name = $tenant->public_name;

// New
$name = $tenant->attribute('public_name');
```

## Future Enhancements

1. Add attribute accessors/mutators for backward compatibility
2. Create a TenantAttribute model for more complex attribute handling
3. Add attribute-specific validation classes
4. Implement attribute versioning/history
