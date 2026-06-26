# Settings & Attributes Validation Fix

## Problem

When updating a tenant with settings or attributes, only fields with explicit validation rules were being persisted. Fields like `colors`, `meta`, and `values` that didn't have validation rules in the config were being stripped out by Laravel's validation.

### Example Issue:

**Payload sent:**
```json
{
  "settings": {
    "service_fee": 10,
    "meta": {"a": "b", "c": "d"},
    "values": {"sidebar-large-width": "200px"},
    "colors": {"primary-color--light": "#C97773", ...}
  }
}
```

**Response received (incorrect):**
```json
{
  "settings": {
    "service_fee": 10  // Only service_fee was saved!
  }
}
```

## Root Cause

The `TenantRequest` validation rules were:
1. Only validating fields that had explicit `rules` defined in `config/tenants.php`
2. Using Laravel's `validated()` method which **only returns fields that pass validation**
3. Fields without validation rules were being discarded

In the config, `meta`, `colors`, and `values` didn't have `rules` defined (commented out or missing), so they were not included in the validation rules and thus not saved.

## Solution

Updated `app/Http/Requests/API/System/TenantRequest.php` to:

### 1. Allow Dynamic Fields with Wildcard Rules

Added wildcard validation rules to accept any field within `settings` and `attributes`:

```php
public function getSettingRules()
{
    $isCreate = $this->isMethod('post');
    $rules = ['settings' => $isCreate ? 'nullable|array' : 'sometimes|array'];
    
    // ✅ Add wildcard rule to allow any setting field
    $rules['settings.*'] = 'nullable';

    if(!$isCreate) {
        $settingFormats = Tenant::getSystemSettingFormats();

        foreach ($settingFormats as $settingFormat) {
            $attribute = $settingFormat['attribute'];
            $editable  = $settingFormat['editable'] ?? false;

            if (!$editable || !isset($settingFormat['rules'])) {
                continue;
            }

            // Extract just the attribute name from 'settings.attribute_name'
            $attributeName = str_replace('settings.', '', $attribute);
            
            // Specific validation rules for fields that have them
            $rules["settings.$attributeName"] = $settingFormat['rules'];
        }
    }

    return $rules;
}
```

### 2. Same Fix for Attributes

```php
public function getAttributeRules()
{
    $isCreate = $this->isMethod('post');
    $rules = ['attributes' => $isCreate ? 'nullable|array' : 'sometimes|array'];
    
    // ✅ Add wildcard rule to allow any attribute field
    $rules['attributes.*'] = 'nullable';

    if(!$isCreate) {
        $attributeFormats = Tenant::getSystemAttributeFormats();

        foreach ($attributeFormats as $attributeFormat) {
            $attribute = $attributeFormat['attribute'];
            $editable  = $attributeFormat['editable'] ?? false;

            if (!$editable || !isset($attributeFormat['rules'])) {
                continue;
            }

            // Specific validation rules for fields that have them
            $rules["attributes.$attribute"] = $attributeFormat['rules'];
        }
    }

    return $rules;
}
```

## How It Works Now

1. **Wildcard Rule (`settings.*` and `attributes.*`)**: Allows ANY field within settings/attributes to pass validation
2. **Specific Rules**: Fields with explicit validation rules (like `service_fee`) still get validated with their specific rules
3. **All Fields Persisted**: Because all fields pass validation (either via wildcard or specific rules), they all get included in `validated()` and thus saved to the database

## Validation Flow

```
Request Payload
    ↓
Validation Rules Applied:
  - settings: nullable|array ✅
  - settings.*: nullable ✅ (catches colors, meta, values, etc.)
  - settings.service_fee: required|numeric (if defined) ✅
    ↓
All fields pass validation
    ↓
validated() returns ALL fields
    ↓
$item->update($validated)
    ↓
All settings & attributes saved! ✅
```

## Expected Behavior Now

**Payload sent:**
```json
{
  "settings": {
    "service_fee": 10,
    "meta": {"a": "b", "c": "d"},
    "values": {"sidebar-large-width": "200px"},
    "colors": {"primary-color--light": "#C97773", ...}
  }
}
```

**Response received (correct):**
```json
{
  "settings": {
    "service_fee": 10,
    "meta": {"a": "b", "c": "d"},
    "values": {"sidebar-large-width": "200px"},
    "colors": {"primary-color--light": "#C97773", ...}
  }
}
```

## Testing

Test the update with:
```bash
POST /api/system/tenant/9
{
  "settings": {
    "service_fee": 10,
    "meta": {"test": "value"},
    "colors": {"primary": "#000"},
    "values": {"width": "200px"}
  },
  "attributes": {
    "public_name": "Test",
    "phone": "123456"
  },
  "_method": "PUT"
}
```

All fields should now be persisted correctly.

## Benefits

1. ✅ **Dynamic Fields**: Settings/attributes can have any fields without requiring config changes
2. ✅ **Validation Still Works**: Fields with explicit rules are still validated
3. ✅ **Backward Compatible**: Existing validation rules still work
4. ✅ **Flexible**: New fields can be added without code changes
5. ✅ **Type Safety**: The wildcard rule still enforces that values are nullable (prevents errors)
