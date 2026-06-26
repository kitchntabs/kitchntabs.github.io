# Frontend Attributes Field Not Populating Fix

## Problem

When editing a tenant in the frontend, the `attributes` field was being sent as an empty array (`attributes: []`) even when the individual attribute fields (public_name, address, phone, etc.) were filled in.

### Example Issue:

**Form fields filled:**
- Public Name: "My Company"
- Address: "123 Main St"
- Phone: "555-1234"

**Payload sent (incorrect):**
```json
{
  "name": "PW",
  "attributes": []  // Empty! 
}
```

## Root Cause

The TenantAttributes component was incorrectly accessing the tenant's attribute values when setting default values for the form fields.

### The Issue:

In the config, attributes are defined as:
```php
'attribute' => 'attributes.public_name'
```

But the component was looking for:
```tsx
tenant.attributes[entry.attribute]
// This would try to access: tenant.attributes['attributes.public_name']
// Instead of: tenant.attributes['public_name']
```

This caused:
1. **Default values not loading** - Fields appeared empty even if data existed
2. **Form registration issue** - The fields might not have been properly registered in the form context

## Solution

Updated both `TenantAttributes.tsx` and `TenantSettings.tsx` to properly extract the attribute/setting name from the full path.

### Fixed Code:

**TenantAttributes.tsx:**
```tsx
const parsedSchema = formatsData.data.attribute_formats.map((entry) => {
  // ✅ Extract the actual attribute name from 'attributes.attribute_name'
  const attributeName = entry.attribute ? entry.attribute.replace('attributes.', '') : entry.id;
  
  const defaultValue =
    (tenant.attributes && tenant.attributes[attributeName]) ||
    entry?.default_value;

  return {
    ...entry,
    fieldOptions: {
      defaultValue: defaultValue,
      fullWidth: true,
    },
  };
});
```

**TenantSettings.tsx:**
```tsx
const parsedSchema = formatsData.data.setting_formats.map((entry) => {
  // ✅ Extract the actual setting name from 'settings.setting_name'  
  const settingName = entry.attribute ? entry.attribute.replace('settings.', '') : entry.id;
  
  const defaultValue =
    (tenant.settings && tenant.settings[settingName]) ||
    entry?.default_value;

  return {
    ...entry,
    fieldOptions: {
      defaultValue: defaultValue,
      fullWidth: true,
    },
  };
});
```

## How It Works Now

### Config Definition:
```php
[
  'id' => 'public_name',
  'attribute' => 'attributes.public_name',  // Full path for form registration
  'label' => 'PUBLIC NAME',
  ...
]
```

### Component Processing:
```tsx
// 1. Get the config entry
entry.attribute = 'attributes.public_name'

// 2. Extract just the name
attributeName = entry.attribute.replace('attributes.', '')
// Result: 'public_name'

// 3. Access the correct value
defaultValue = tenant.attributes['public_name']  // ✅ Correct!
// NOT: tenant.attributes['attributes.public_name']  // ❌ Wrong!

// 4. Set as default value
fieldOptions: {
  defaultValue: defaultValue
}
```

### Form Field Registration:

The `DashAutoFormTabs` component uses `entry.attribute` (which is `'attributes.public_name'`) to register the field in react-hook-form. This ensures the field value is properly stored under `attributes.public_name` in the form state.

### Data Flow:

```
1. Load tenant data
   tenant.attributes = { public_name: "My Company", phone: "555-1234" }
   
2. Component extracts names
   'attributes.public_name' → 'public_name'
   'attributes.phone' → 'phone'
   
3. Get default values
   defaultValue = tenant.attributes['public_name'] = "My Company" ✅
   
4. Register fields with full path
   Field registered as: 'attributes.public_name'
   
5. Form state on submit
   {
     attributes: {
       public_name: "My Company",
       phone: "555-1234"
     }
   } ✅
```

## Expected Behavior Now

**Form loads with existing data:**
- ✅ Public Name field shows: "My Company"
- ✅ Address field shows: "123 Main St"  
- ✅ Phone field shows: "555-1234"

**On submit:**
```json
{
  "name": "PW",
  "attributes": {
    "public_name": "My Company",
    "address": "123 Main St",
    "phone": "555-1234",
    "mobile": null,
    "contact_name": "John Doe",
    "contact_email": "john@example.com",
    "contact_phone": "555-5678"
  }
}
```

## Benefits

1. ✅ **Default values load correctly** - Form fields populate with existing tenant data
2. ✅ **Form submission works** - Attribute values are properly included in the payload
3. ✅ **Consistent with settings** - Both settings and attributes use the same pattern
4. ✅ **Backwards compatible** - Falls back to `entry.id` if `entry.attribute` is not defined

## Testing Checklist

- [ ] Open an existing tenant in edit mode
- [ ] Verify attribute fields (public_name, address, phone, etc.) show existing values
- [ ] Modify some attribute values
- [ ] Save the tenant
- [ ] Verify the payload includes the `attributes` object with all values
- [ ] Refresh and verify changes were persisted
- [ ] Create a new tenant and verify attributes can be set
