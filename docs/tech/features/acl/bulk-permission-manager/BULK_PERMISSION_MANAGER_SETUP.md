# Bulk Permission Manager - Quick Setup Guide

## Overview

This guide will help you quickly set up and use the Bulk Permission Manager feature that was just created.

## What Was Created

### Backend Files (Laravel)
1. ✅ **RolePermissionBulkController.php** - Main controller with 3 endpoints
2. ✅ **RolePermissionBulkRequest.php** - Request validation
3. ✅ **RolePermissionBulkResource.php** - API resource transformer
4. ✅ **Routes** - Added to `routes/system.php`

### Frontend Files (React)
1. ✅ **RolePermissionBulkManager.tsx** - Material UI table component
2. ✅ **rolePermissionBulkSchema.tsx** - Schema configuration
3. ✅ **systemResources.tsx** - Updated with new resource

## Installation Steps

### 1. Backend Setup

No additional setup needed! The files are already in place:

```bash
# Verify files exist
ls -la dash-backend/app/Http/Controllers/API/System/RolePermissionBulkController.php
ls -la dash-backend/app/Http/Requests/API/System/RolePermissionBulkRequest.php
ls -la dash-backend/app/Http/Resources/RolePermissionBulkResource.php
```

### 2. Test Backend Endpoints

```bash
# Get your auth token first
TOKEN="your_bearer_token_here"

# Test getting permissions for role ID 1
curl -X GET "https://api.kitchntabs.com/api/system/role/1/permissions-bulk?page=1&perPage=10" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"

# Test getting stats
curl -X GET "https://api.kitchntabs.com/api/system/role/1/permissions-bulk/stats" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

### 3. Frontend Setup

The frontend files are already in place. Just verify they exist:

```bash
# Verify files
ls -la dash-frontend/packages/dash-admin/src/components/permission/RolePermissionBulkManager.tsx
ls -la dash-frontend/packages/dash-admin/src/schemas/rolePermissionBulk.tsx
```

### 4. Build and Run

```bash
# If using Laravel Sail
cd dash-backend
./vendor/bin/sail up -d

# Build frontend
cd dash-frontend
npm install  # if needed
npm run dev  # or npm run build
```

## Accessing the Feature

### Option 1: Direct URL

Navigate to: `http://your-frontend-url/system/role/{roleId}/permissions-bulk`

Replace `{roleId}` with an actual role ID (e.g., 1, 2, 3)

Example: `https://api.kitchntabs.com/system/role/1/permissions-bulk`

### Option 2: Add Link to Role Edit Page (Recommended)

You can add a button to the role edit/view page that links to the bulk manager:

**In your role view/edit component, add:**

```tsx
import { Button } from '@mui/material';
import { useRecordContext, useNavigate } from 'react-admin';

const BulkPermissionButton = () => {
    const record = useRecordContext();
    const navigate = useNavigate();
    
    if (!record) return null;
    
    return (
        <Button
            variant="contained"
            color="primary"
            onClick={() => navigate(`/system/role/${record.id}/permissions-bulk`)}
        >
            Manage Permissions (Bulk)
        </Button>
    );
};
```

## Usage Examples

### 1. Filter Permissions by Group

1. Navigate to the bulk manager
2. Click the "Group" dropdown
3. Select a group (e.g., "users", "permissions", "tenants")
4. Results update automatically

### 2. Enable Multiple Permissions

1. Check the boxes next to the permissions you want to enable
2. Click "Enable Selected" button
3. Click "Save Changes" (floating button at bottom right)
4. Wait for success notification

### 3. View Statistics

1. Click the bar chart icon (📊) in the toolbar
2. View overall statistics and per-group breakdown
3. Click X to close statistics panel

### 4. Search and Enable

1. Type search term in search box (e.g., "user")
2. Review filtered results
3. Click "Enable All Visible" to enable all shown permissions
4. Click "Save Changes"

## API Endpoints Reference

### GET `/api/system/role/{id}/permissions-bulk`

Fetch paginated permissions with their checked status.

**Query Parameters:**
- `page` (int, default: 1) - Page number
- `perPage` (int, default: 25) - Items per page
- `search` (string) - Search term
- `group` (string) - Filter by group
- `level` (int) - Filter by level
- `checked` (bool) - Filter by assigned status
- `sortField` (string) - Field to sort by
- `sortOrder` (string) - 'asc' or 'desc'

**Response:**
```json
{
  "data": [...],
  "meta": {
    "current_page": 1,
    "total": 759,
    ...
  },
  "filters": {
    "groups": [...],
    "levels": [...]
  },
  "role": {
    "id": 1,
    "name": "System Admin",
    "level": 0
  }
}
```

### POST `/api/system/role/{id}/permissions-bulk/update`

Bulk update permissions for a role.

**Body:**
```json
{
  "permission_ids": [1, 2, 3, 4],
  "action": "add"  // or "remove" or "set"
}
```

**Actions:**
- `add` - Add permissions to role (preserves existing)
- `remove` - Remove permissions from role
- `set` - Replace all permissions with the provided set

**Response:**
```json
{
  "message": "4 permission(s) added successfully",
  "data": {
    "role_id": 1,
    "action": "add",
    "affected_count": 4
  }
}
```

### GET `/api/system/role/{id}/permissions-bulk/stats`

Get statistics about role permissions.

**Response:**
```json
{
  "role": {...},
  "stats": {
    "total_permissions": 759,
    "assigned_permissions": 500,
    "unassigned_permissions": 259,
    "percentage_assigned": 65.88
  },
  "groups": [
    {
      "group": "users",
      "total": 50,
      "assigned": 45,
      "percentage": 90
    },
    ...
  ]
}
```

## Troubleshooting

### Issue: 404 Not Found

**Solution:** Make sure the backend routes are registered. Check `routes/system.php`.

### Issue: 403 Unauthorized

**Solution:** 
- Check that you're logged in as a user with appropriate role level
- System Admin (level 0) can manage all permissions
- Lower level users have restrictions

### Issue: Frontend not showing the component

**Solution:**
- Clear browser cache
- Rebuild frontend: `npm run build`
- Check browser console for errors
- Verify the route is registered in systemResources.tsx

### Issue: Changes not saving

**Solution:**
- Check browser network tab for failed requests
- Check backend logs: `tail -f storage/logs/laravel.log`
- Verify database connection
- Check permission cache is being cleared

## Performance Tips

### For Thousands of Permissions

1. **Use Filters:** Always filter by group or level to reduce dataset
2. **Adjust Page Size:** Use 25 or 50 items per page
3. **Use Search:** Search for specific permission names
4. **Batch Operations:** Select and update in batches rather than all at once

### Optimization Settings

**Backend (`.env`):**
```env
DB_CONNECTION=mysql
QUEUE_CONNECTION=sync  # or 'redis' for better performance
CACHE_DRIVER=redis     # or 'memcached'
```

**Frontend:**
Adjust rows per page in the UI (10, 25, 50, 100)

## Next Steps

1. **Add Menu Link:** Add a direct link to the bulk manager in your navigation menu
2. **Role Edit Button:** Add a button in the role edit page to access bulk manager
3. **Customize:** Adjust the UI colors, labels, or behavior as needed
4. **Test:** Test with your actual roles and permissions
5. **Monitor:** Check performance with your permission count
6. **Document:** Add this feature to your internal documentation

## Support

For issues or questions:

1. Check the [Full Documentation](./BULK_PERMISSION_MANAGER.md)
2. Review [Role Permission System Docs](./dash-backend/ROLE_PERMISSION_SYSTEM.md)
3. Check browser console and network tab
4. Check Laravel logs: `storage/logs/laravel.log`
5. Enable debug mode: `APP_DEBUG=true` in `.env`

## Summary

✅ **Backend:** 3 new files + routes
✅ **Frontend:** 2 new files + resource config
✅ **Features:** Pagination, filtering, sorting, bulk ops, statistics
✅ **Performance:** Optimized for thousands of permissions
✅ **Security:** Level-based authorization
✅ **Documentation:** Complete guides and API reference

The feature is **ready to use** - just navigate to the URL and start managing permissions!
