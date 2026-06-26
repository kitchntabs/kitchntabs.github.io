---
layout: default
title: F14-Auth-Access-Control PERMISSION SELECTOR DATAGRID
---

# Permission Selector DataGrid - Implementation Guide

## Overview

I've created a **MUI DataGrid version** of the Permission Selector that works **exactly the same way** as the existing card-based solution, but with a table interface instead of cards.

## What Was Created

### New Files

1. **PermissionsSelectorDataGrid.tsx** - Complete DataGrid implementation
   - Location: `dash-frontend/packages/dash-admin/src/components/permission/PermissionsSelectorDataGrid.tsx`
   - 450+ lines of code
   - Full feature parity with original

2. **rolesDataGrid.tsx** - Alternative schema using DataGrid
   - Location: `dash-frontend/packages/dash-admin/src/schemas/rolesDataGrid.tsx`
   - Drop-in replacement for roles.tsx

## How It Works (Same as Original)

### Data Flow

```
1. Load available permissions from cache (SystemRequestsCache)
   └─ Uses: system/permission/availablePermissions endpoint

2. Initialize state with all permissions
   └─ Mark which ones are checked based on record.permission_objects

3. User interactions update local state
   └─ Toggle individual permissions
   └─ Bulk operations (select all, deselect all, bulk enable/disable)

4. Sync to form fields
   ├─ permission_objects: Array of checked permission objects
   └─ permissions: Array of checked route_names

5. Form submission sends permission_objects to backend
   └─ Backend processes via RoleController::_update()
```

### Key Behaviors (Preserved)

✅ **Only checked permissions are sent** to the backend
✅ **Uses permission_objects field** (array of permission objects with checked: true)
✅ **Uses permissions field** (array of route_names)
✅ **Syncs on every state change** via useEffect
✅ **Debounced search** (300ms delay)
✅ **Initializes from record.permission_objects** on edit
✅ **Works with create and edit modes**
✅ **Integrates with react-hook-form** via useController

## Features

### DataGrid Features

- ✅ **Sortable columns** (click headers to sort)
- ✅ **Pagination** (10, 25, 50, 100 rows per page)
- ✅ **Row selection** (checkboxes for bulk operations)
- ✅ **Search** (across name, route_name, group)
- ✅ **Group filter** (dropdown with all available groups)
- ✅ **Individual enable/disable** (checkbox in "Enabled" column)
- ✅ **Bulk operations**
  - Select All / Deselect All (all permissions)
  - Enable Selected / Disable Selected (selected rows)
- ✅ **Statistics** (shows X / Y selected count)
- ✅ **Responsive design**

### Columns

1. **Enabled** - Checkbox to enable/disable permission
2. **Group** - Permission group (as chip)
3. **Name** - Permission display name
4. **Route Name** - API route (monospace font)

## How to Switch to DataGrid

### Option 1: Replace Existing (Affects All Roles)

Update `dash-frontend/packages/dash-admin/src/schemas/roles.tsx`:

```tsx
import { IDashAutoAdminAttribute } from 'dash-auto-admin';
import PermissionsSelectorDataGrid from '../components/permission/PermissionsSelectorDataGrid';

const roleSchema: IDashAutoAdminAttribute[] = [
	{
		label: 'Nombre',
		attribute: 'name',
		type: String,
	},
	{
		label: 'Nivel',
		attribute: 'level',
		type: Number,
		inList: false,
	},
	{
		label: 'Grupo (web)',
		attribute: 'guard_name',
		type: String,
		inList: false,
	},
	{
		label: 'Permisos',
		attribute: 'permission_ids',
		type: String,
		custom: true,
		component: PermissionsSelectorDataGrid, // CHANGED
		inList: false,
	},
];

export default roleSchema;
```

### Option 2: Create Separate Resource (Both Available)

Update `dash-frontend/packages/dash-admin/src/systemResources.tsx`:

```tsx
import roleSchema from './schemas/roles';
import roleSchemaDataGrid from './schemas/rolesDataGrid';

// Add a new resource for DataGrid version
const systemResources: IAppResourceConfig[] = [
    // ... existing resources ...
    
    {
        roles: [DASHAppConstants.system.SYSTEM_ROLE],
        component: ResourceTemplate,
        model: 'system/role',
        label: 'roles',
        icon: <SystemUpdateAlt />,
        group: 'Recursos de sistema',
        menu: [
            {
                title: 'Roles (Cards)',
                redirect: '/system/role',
            },
        ],
        schema: roleSchema, // Original card-based
        // ... rest of config
    },
    
    {
        roles: [DASHAppConstants.system.SYSTEM_ROLE],
        component: ResourceTemplate,
        model: 'system/role-datagrid',
        label: 'roles (DataGrid)',
        icon: <SystemUpdateAlt />,
        group: 'Recursos de sistema',
        menu: [
            {
                title: 'Roles (DataGrid)',
                redirect: '/system/role-datagrid',
            },
        ],
        schema: roleSchemaDataGrid, // DataGrid version
        // ... same config as roles
    },
];
```

### Option 3: Quick Test (Temporary)

Just edit one file to test immediately:

```tsx
// In dash-frontend/packages/dash-admin/src/schemas/roles.tsx
import PermissionsSelectorDataGrid from '../components/permission/PermissionsSelectorDataGrid';

// Change line 26:
component: PermissionsSelectorDataGrid,
```

## Comparison: Cards vs DataGrid

| Feature | Cards | DataGrid |
|---------|-------|----------|
| **Visual Style** | Grouped cards | Table with rows |
| **Grouping** | Visible groups | Filter by group |
| **Sorting** | By group only | All columns |
| **Pagination** | Load more per card | Global pagination |
| **Search** | 2 fields (group + item) | 1 unified search |
| **Bulk Selection** | By group or all | By row checkboxes |
| **Performance** | Good (virtualized) | Excellent (built-in) |
| **Space Usage** | More vertical | More compact |
| **Best For** | Visual overview | Large datasets |

## API Compatibility

### Request Format (Unchanged)

```json
// On save, sends:
{
  "permission_objects": [
    {
      "group": "users",
      "name": "User List",
      "route_name": "api.system.user.getList",
      "checked": true
    },
    // ... only checked permissions
  ],
  "permissions": [
    "api.system.user.getList",
    // ... only checked route_names
  ]
}
```

### Backend Processing (Unchanged)

The backend `RoleController::_update()` already handles this format:

```php
if (isset($validated['permission_objects'])) {
    \App\Jobs\SyncRolePermissionsJob::dispatchChunked(
        $item->id, 
        $validated['permission_objects'], 
        false
    );
}
```

## Testing Checklist

- [ ] Load role edit page - should show DataGrid
- [ ] Check initial permissions load correctly
- [ ] Toggle individual permission - should update immediately
- [ ] Use "Select All" - all should be checked
- [ ] Use "Deselect All" - all should be unchecked
- [ ] Search for permission - should filter results
- [ ] Filter by group - should show only that group
- [ ] Select rows and use "Enable Selected"
- [ ] Select rows and use "Disable Selected"
- [ ] Save changes - should persist to backend
- [ ] Reload page - saved permissions should be checked
- [ ] Test with create mode (new role)
- [ ] Check browser console for errors

## Troubleshooting

### DataGrid doesn't show

**Check:** MUI X DataGrid package is installed

```bash
npm list @mui/x-data-grid
# or
yarn list @mui/x-data-grid
```

**Fix:** Install if missing

```bash
npm install @mui/x-data-grid
# or
yarn add @mui/x-data-grid
```

### Permissions not saving

**Check:** Browser console and network tab

- Look for errors in console
- Check POST request to `/system/role/{id}`
- Verify `permission_objects` array is in request body

### Performance issues with thousands of permissions

**Solution:** DataGrid has built-in virtualization, but you can:
- Reduce initial page size
- Enable column virtualization
- Add more aggressive filtering

{% raw %}
```tsx
// In PermissionsSelectorDataGrid.tsx, update initialState:
initialState={{
    pagination: {
        paginationModel: { pageSize: 10 }, // Smaller page size
    },
}}
```
{% endraw %}

## Code Quality

### What's the Same

- ✅ Same state management pattern
- ✅ Same form integration (useController)
- ✅ Same backend format (permission_objects)
- ✅ Same debouncing logic
- ✅ Same initialization from record
- ✅ Same sync to form fields

### What's Different

- ❌ No card grouping (replaced with filter)
- ❌ No expand/collapse (not needed)
- ❌ Single unified search (not separate)
- ✅ DataGrid built-in features (sort, pagination, selection)
- ✅ More compact UI
- ✅ Better for large datasets

## Performance

### Cards Version
- Renders all groups
- Expand/collapse for performance
- Good for < 1000 permissions

### DataGrid Version  
- Virtual scrolling built-in
- Only renders visible rows
- Excellent for 1000+ permissions
- Faster sorting/filtering

## Migration Path

### Immediate (No Risk)

1. Keep both versions available
2. Test DataGrid on staging
3. Get user feedback
4. Gradually migrate

### Recommended

1. Create separate resource (Option 2 above)
2. Add both to menu: "Roles (Cards)" and "Roles (DataGrid)"
3. Let users choose preferred interface
4. After 1-2 weeks, remove less popular version

### Quick Win

1. Just replace the import in `roles.tsx`
2. Test thoroughly
3. Deploy if satisfied
4. Rollback by reverting one line if issues

## Summary

✅ **Drop-in replacement** - works exactly the same
✅ **No backend changes** - uses same API format  
✅ **Better for large datasets** - built-in virtualization
✅ **More features** - sorting, pagination, bulk selection
✅ **Easy to test** - change one import line
✅ **Easy to rollback** - change one import line back

The DataGrid version provides a more traditional table interface while maintaining 100% compatibility with the existing backend and data flow.
