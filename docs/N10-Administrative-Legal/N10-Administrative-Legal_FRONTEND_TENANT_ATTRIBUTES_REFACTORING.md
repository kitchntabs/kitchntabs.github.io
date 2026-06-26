# Frontend Tenant Attributes Refactoring

## Overview
Updated the frontend to support the new tenant `attributes` JSON field, replacing individual contact field columns with a dynamic attributes system following the same pattern as the `settings` implementation.

## Files Created

### 1. TenantAttributes.tsx
**Path:** `/dash-frontend/packages/dash-admin/src/components/tenant/TenantAttributes.tsx`

A new component that handles the rendering of tenant attributes in different modes:
- **TenantAttributesEdit**: Renders dynamic form fields for editing attributes
- **TenantAttributesCreate**: Renders dynamic form fields for creating attributes
- **TenantAttributesView**: Renders a read-only table view of attributes

The component:
- Fetches attribute formats from the backend via `useSystemRequestsCache`
- Maps attribute formats to form schema with default values
- Uses `DashAutoFormTabs` to render the dynamic form
- Handles all CRUD operations (create, edit, view, list)

### 2. TenantAttributesContext.tsx
**Path:** `/dash-frontend/packages/dash-admin/src/components/tenant/TenantAttributesContext.tsx`

A context provider for caching tenant attribute formats:
- Uses IndexedDB for persistent caching
- Implements global fetch promise to prevent duplicate requests
- Caches data for 10 seconds to reduce API calls
- Provides `useTenantAttributesFormats()` hook for components

## Files Modified

### 1. tenant_superadmin.tsx
**Path:** `/dash-frontend/packages/dash-admin/src/schemas/tenant_superadmin.tsx`

**Changes:**
- Added import for `TenantAttributes` component
- Removed individual contact field definitions:
  - `public_name` (Razón Social)
  - `address` (Dirección)
  - `phone` (Teléfono)
  - `mobile` (Teléfono Móvil)
  - `contact_name` (Nombre del contacto)
  - `contact_email` (Email del contacto)
  - `contact_phone` (Teléfono del contacto)
- Added new `attributes` field using custom component:
  ```tsx
  {
    tab: 'Datos contacto',
    label: 'Datos de contacto',
    attribute: 'attributes',
    type: String,
    custom: true,
    inList: false,
    component: TenantAttributes,
    inCreate: false,
    inShow: false
  }
  ```

### 2. systemResources.tsx
**Path:** `/dash-frontend/packages/dash-admin/src/systemResources.tsx`

**Changes:**
- Updated the tenant resource `contextComponent` to wrap with both SystemRequestsCache providers:
  - Settings cache: `system/tenant/systemSettingFormats`
  - Attributes cache: `system/tenant/systemAttributeFormats`
- Nested the providers to provide both contexts to child components

### 3. Tenant.tsx (Interface)
**Path:** `/dash-frontend/packages/dash-admin/src/interfaces/Tenant.tsx`

**Changes:**
- Added `attributes: any[]` field
- Removed deprecated individual contact fields:
  - `public_name`
  - `address`
  - `phone`
  - `mobile`
  - `contact_name`
  - `contact_email`
  - `contact_phone`

## Implementation Details

### SystemRequestsCache Integration
The attributes and settings functionality uses a single `SystemRequestsCache` provider to fetch and cache both formats from the backend:

```tsx
<SystemRequestsCache
    cacheKey="tenant_formats_cache"
    apiUrl="system/tenant/systemSettingFormats"
    cacheSeconds={300}
>
    {children}
</SystemRequestsCache>
```

This provides:
- Automatic caching with IndexedDB
- Configurable cache duration (300 seconds)
- Automatic refetching when cache expires
- Loading state management
- Single endpoint for both settings and attributes formats

The endpoint returns both `setting_formats` and `attribute_formats` in a single response:
```json
{
  "data": {
    "setting_formats": [...],
    "attribute_formats": [...]
  }
}
```

### Attribute Schema Parsing
The component dynamically builds form schemas from backend attribute formats:

```tsx
const parsedSchema = formatsData.data.attribute_formats.map((entry) => {
  const defaultValue = (tenant.attributes && tenant.attributes[entry.attribute]) || entry?.default_value;
  
  return {
    ...entry,
    fieldOptions: {
      defaultValue: defaultValue,
      fullWidth: true,
    },
    ...(method === 'view' && { readOnly: true }),
  };
});
```

Similarly for settings:
```tsx
const parsedSchema = formatsData.data.setting_formats.map((entry) => {
  const defaultValue = (tenant.settings && tenant.settings[entry.attribute]) || entry?.default_value;
  
  return {
    ...entry,
    fieldOptions: {
      defaultValue: defaultValue,
      fullWidth: true,
    },
    ...(method === 'view' && { readOnly: true }),
  };
});
```

### Form Rendering
Uses `DashAutoFormTabs` to render dynamic forms:

```tsx
DashAutoFormTabs({
  schema: attributeFormatsSchema,
  resourceConfig: null,
  options: {
    mode: method,
    label: 'Datos de contacto',
  }
})
```

## API Endpoints Expected

The frontend expects the following backend endpoints:

1. **GET** `/api/system/tenant/systemSettingFormats` (Updated)
   - Returns both setting and attribute format definitions in a single response
   - Used for building dynamic forms for both settings and attributes
   - Response format:
     ```json
     {
       "data": {
         "setting_formats": [
           {
             "attribute": "some_setting",
             "label": "Some Setting",
             "type": "string",
             "default_value": null,
             "validation": {...},
             ...
           }
         ],
         "attribute_formats": [
           {
             "attribute": "public_name",
             "label": "Razón Social",
             "type": "string",
             "default_value": null,
             "validation": {...},
             ...
           }
         ]
       },
       "total": 15
     }
     ```

2. **GET** `/api/system/tenant/systemAttributeFormats` (Deprecated)
   - Still available for backward compatibility
   - Returns only attribute format definitions
   - Recommended to use `systemSettingFormats` endpoint instead

3. **GET** `/api/system/tenant` (Updated)
   - Now returns both `settings` and `attributes` fields
   - Response includes:
     ```json
     {
       "id": 1,
       "name": "...",
       "settings": {
         "some_setting": "...",
         ...
       },
       "attributes": {
         "public_name": "...",
         "address": "...",
         "phone": "...",
         ...
       }
     }
     ```

4. **PUT/POST** `/api/system/tenant/{id}` (Updated)
   - Accepts both `settings` and `attributes` objects in request body
   - Request format:
     ```json
     {
       "name": "...",
       "settings": {
         "some_setting": "...",
         ...
       },
       "attributes": {
         "public_name": "...",
         "address": "...",
         ...
       }
     }
     ```

## Benefits

1. **Consistency**: Attributes work exactly like settings
2. **Flexibility**: Easy to add new attributes via backend config without frontend changes
3. **Maintainability**: Single JSON field instead of multiple individual fields
4. **Performance**: Caching reduces API calls
5. **Type Safety**: Proper TypeScript interfaces
6. **User Experience**: Dynamic forms that adapt to backend configuration

## Testing Checklist

- [ ] Verify tenant list displays correctly
- [ ] Verify tenant edit form shows attributes tab
- [ ] Verify attribute values are loaded correctly
- [ ] Verify attribute validation works
- [ ] Verify attributes are saved correctly
- [ ] Verify create tenant with attributes works
- [ ] Verify caching mechanism works (check IndexedDB)
- [ ] Verify view mode shows attributes in table format
- [ ] Verify no console errors

## Migration Notes

⚠️ **Breaking Changes**: 
- Frontend components accessing `tenant.public_name`, `tenant.address`, etc. directly will break
- Update references to use `tenant.attributes.public_name`, etc.
- Or use the new Tenant interface which only has `attributes` field

## Future Enhancements

1. Add TypeScript types for specific attributes
2. Create attribute-specific validators
3. Add attribute grouping/categories in UI
4. Implement attribute change history/audit
5. Add attribute import/export functionality
