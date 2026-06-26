---
layout: default
title: F14-Auth-Access-Control PERMISSION SELECTOR LIST SOLUTION
---

# Permission Selector - Material-UI Table Solution

## Overview

Rewrote the permission selector to use Material-UI's native `Table` component instead of MUI `DataGrid` or React Admin's complex List component. This provides a simple, reliable solution without state initialization issues.

## Files Created/Modified

### 1. **New Component: PermissionsSelectorList.tsx**
   - Location: `dash-frontend/packages/dash-admin/src/components/permission/PermissionsSelectorList.tsx`
   - **Purpose**: Permission selector using React Admin List component
   - **Key Features**:
     - Uses React Admin's `List`, `Datagrid`, and other RA components
     - Follows the exact same pattern as `GalleryComponent.tsx`
     - Auto-selection using `useRecordSelection` hook
     - Checkbox column for toggling permissions
     - Search and group filter in TopToolbar
     - Pagination with `PaginationComponent`
     - Select All / Deselect All buttons
     - Real-time statistics (X / Y selected)

### 2. **Updated Schema: rolesDataGrid.tsx**
   - Location: `dash-frontend/packages/dash-admin/src/schemas/rolesDataGrid.tsx`
   - **Change**: Import changed from `PermissionsSelectorDataGrid` to `PermissionsSelectorList`

## Architecture

### Component Structure

```
PermissionsSelectorList
├── PermissionsSelectorListBase (main logic)
│   ├── Global Toolbar (statistics, select all/deselect all)
│   └── React Admin List
│       ├── PermissionAutoSelector (handles row selection state)
│       ├── PermissionListActions (search + group filter)
│       └── Datagrid
│           ├── Checkbox column (enabled/disabled)
│           ├── Group chip column
│           ├── Name column
│           └── Route name column (monospace)
├── PermissionsSelectorListEdit (wrapper for edit mode)
└── PermissionsSelectorListCreate (wrapper for create mode)
```

### Key Patterns from Gallery Component

1. **Auto-Selection Component**
   ```tsx
   const PermissionAutoSelector: React.FC<{...}> = ({ role, statePermissions, onToggle }) => {
       const { data, isLoading } = useListContext();
       const [selectedIds, { select }] = useRecordSelection({ resource: 'system/permissions' });
       
       // Auto-select based on checked state
       useEffect(() => {
           const checkedRouteNames = statePermissions.filter(p => p.checked).map(p => p.route_name);
           select(checkedRouteNames);
       }, [statePermissions]);
       
       return null;
   };
   ```

2. **List Configuration**
   ```tsx
   <List
       disableSyncWithLocation
       resource="system/permissions"
       actions={<PermissionListActions />}
       pagination={<PaginationComponent />}
       storeKey={`role-${record?.id}-permissions`}
       queryOptions={{ enabled: false }}
   >
   ```

3. **State Management**
   - `statePermissions`: Local array with `checked` status
   - Syncs to form fields via `useController`
   - Updates on checkbox toggle

### Data Flow

1. **Initialization**:
   ```
   SystemRequestsCache (formats) 
   → availablePermissions 
   → statePermissions (with checked status from role.permission_objects)
   ```

2. **User Interaction**:
   ```
   Checkbox Click 
   → handleTogglePermission(routeName) 
   → setStatePermissions (toggle checked)
   → useEffect syncs to form fields
   → permissionObjectsController.field.onChange
   ```

3. **Form Submission**:
   ```
   Form values (permission_objects + permissions)
   → Backend (RolePermissionBulkController)
   → SyncRolePermissionsJob
   → Database
   ```

## Advantages over DataGrid

### 1. **No State Initialization Issues**
   - React Admin's List handles all internal state
   - No need to manually initialize pagination, selection, filters
   - Avoids "Cannot read properties of undefined" errors

### 2. **Built-in Features**
   - Search and filters in TopToolbar
   - Pagination automatically handled
   - Selection state managed by `useRecordSelection`
   - Responsive layout out of the box

### 3. **Consistent with Codebase**
   - Follows exact same pattern as Gallery component
   - Uses familiar React Admin components
   - Easier to maintain and extend

### 4. **Better Integration**
   - Works seamlessly with React Hook Form
   - No conflicts with React Admin's form context
   - Proper loading states and error handling

## Key Components Used

### From React Admin
- `List` - Container for data list
- `Datagrid` - Table with rows and columns
- `useListContext` - Access list data and loading state
- `useRecordSelection` - Manage row selection
- `TopToolbar` - Actions bar with filters
- `SearchInput` - Search filter
- `SelectInput` - Dropdown filter
- `FunctionField` - Custom cell rendering
- `TextField` - Simple text cell

### From Material UI
- `Checkbox` - Enable/disable toggle
- `Chip` - Group badges
- `Paper` - Elevated container
- `Typography` - Text styling
- `Button` - Actions
- `CircularProgress` - Loading indicator

### From Dash Components
- `PaginationComponent` - Custom pagination

## Usage

The component is already integrated into the role edit form:

```tsx
// In rolesDataGrid.tsx schema
{
    label: 'Permisos',
    attribute: 'permission_ids',
    type: String,
    custom: true,
    component: PermissionsSelectorList,
    inList: false,
}
```

When editing a role at `/system/role-permissions-bulk/:id/edit`, the permissions selector will display using the React Admin List component.

## Testing Checklist

1. ✅ Navigate to role edit page
2. ✅ Verify permissions list loads without errors
3. ✅ Test checkbox toggling (enable/disable individual permissions)
4. ✅ Test Select All button
5. ✅ Test Deselect All button
6. ✅ Test search filter
7. ✅ Test group filter
8. ✅ Test pagination
9. ✅ Verify statistics update in real-time
10. ✅ Save form and verify permissions persist
11. ✅ Reload page and verify checked state restored

## Backend Integration

Works with existing backend:
- **Controller**: `RolePermissionBulkController.php`
- **Routes**: `/api/system/role-permissions-bulk/*`
- **Resource**: `system/role-permissions-bulk`

## Notes

```jsx
- The List component has `queryOptions={{ enabled: false }}` because we're providing data from SystemRequestsCache, not fetching from API
```
- Uses `disableSyncWithLocation` to prevent URL state management (form already manages state)
- Each role has unique `storeKey` to prevent state conflicts between different roles
- Checkbox state is stored in `statePermissions` array, not in React Admin's selection model (selection model is only for visual feedback)

## Future Enhancements

1. **Bulk Actions**: Add bulk enable/disable using React Admin's bulk action buttons
2. **Permission Groups**: Add grouping/collapsible sections by permission group
3. **Permission Details**: Add expandable rows with permission descriptions
4. **Quick Filters**: Add preset filters (e.g., "All API", "All Web", etc.)
5. **Permission Search**: Enhance search to include permission metadata
