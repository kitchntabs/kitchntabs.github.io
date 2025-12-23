# Permission Feature Tests Documentation

## Overview

The Permission feature tests validate the API endpoints for managing permissions in the Dash-Backend. These tests ensure correct access control, data validation, and response structure for all CRUD operations. They are designed to work seamlessly with ReactAdmin-based Dash-Frontend.

## Test Files

- `CreatePermissionTest.php`
- `DeletePermissionTest.php`
- `ReadPermissionTest.php`
- `UpdatePermissionTest.php`

## Route Mapping

All tests use the standardized Dash API routes:

| Action      | Route Name                        | HTTP Method | Example Route                                 |
|-------------|-----------------------------------|-------------|-----------------------------------------------|
| List        | api.system.permissions.getList     | GET         | /api/system/permissions                       |
| Create      | api.system.permissions.create      | POST        | /api/system/permissions                       |
| Read One    | api.system.permissions.getOne      | GET         | /api/system/permission/{id}                  |
| Update      | api.system.permissions.update      | PUT         | /api/system/permission/{id}                  |
| Delete      | api.system.permissions.delete      | DELETE      | /api/system/permission/{id}                  |

## Test Structure

### 1. CreatePermissionTest

- **guests_cannot_create_permissions**: Ensures unauthenticated users receive 401 Unauthorized.
- **unauthorized_users_cannot_create_permissions**: Ensures users without permission receive 403 Forbidden.
- **authorized_users_can_create_a_permission**: Validates successful creation and correct response structure.
- **the_attributes_are_validated_to_create_a_permission**: Checks all validation rules for permission creation.

### 2. DeletePermissionTest

- **guests_cannot_delete_permissions**: Ensures unauthenticated users cannot delete.
- **unauthorized_users_cannot_delete_permissions**: Ensures users without permission cannot delete.
- **authorized_users_can_delete_a_permission**: Validates successful deletion and database state.

### 3. ReadPermissionTest

- **guests_cannot_fetch_permissions**: Ensures unauthenticated users cannot list.
- **unauthorized_users_cannot_fetch_permissions**: Ensures users without permission cannot list.
- **authorized_users_can_fetch_a_list_of_permissions**: Validates list response and item count.
- **authorized_users_can_fetch_a_single_permission**: Validates single item fetch and response.

### 4. UpdatePermissionTest

- **guests_cannot_update_permissions**: Ensures unauthenticated users cannot update.
- **unauthorized_users_cannot_update_permissions**: Ensures users without permission cannot update.
- **authorized_users_can_update_a_permission**: Validates successful update and response.
- **the_attributes_are_validated_to_update_a_permission**: Checks all validation rules for update.

## Validation Rules

Validation is handled by `PermissionRequest.php`:

- `name`: required, string, max 255, unique
- `route_name`: required, string, max 255, unique
- `level`: required, integer, min user level, max Permission::MAX_LEVEL
- `group`: required, string, max 255
- `guard_name`: required, string, in:web
- `is_active`: sometimes, boolean

## Response Structure

- **Single Resource**: Flat JSON object with all attributes.
- **Collection**: Array of objects, optionally with meta information.

Example single resource:
```json
{
  "id": 1,
  "name": "manage_users",
  "guard_name": "web",
  "route_name": "api.system.users.manage",
  "level": 1,
  "group": "system",
  "is_active": true,
  "description": null,
  "created_at": "2024-06-01T12:00:00Z",
  "updated_at": "2024-06-01T12:00:00Z"
}
```

## Test Utilities

- **signIn**: Authenticates a user for the test.
- **signInWithPermissionsTo**: Authenticates a user and assigns required permissions.
- **getValidAttributes**: Generates valid attributes for creation/update.

## Integration Notes

- Tests use Laravel's `RefreshDatabase` trait for isolation.
- Permissions are seeded before each test.
- All route names match the backend API definitions for Dash.

## Extending Tests

To add more tests:
- Use the same structure and route naming conventions.
- Validate new attributes in `PermissionRequest.php`.
- Ensure response assertions match the actual API output.

## References

- [Dash Backend Documentation](../README.md)
- [ReactAdminBaseController](domain/app/Http/Controllers/API/Admin/ReactAdminBaseController.php)
- [Permission Model](app/Models/Permission.php)
- [Permission Resource](app/Http/Resources/PermissionResource.php)
- [Permission Request](app/Http/Requests/API/System/PermissionRequest.php)

