# Role Feature Tests Documentation

## Overview

The Role feature tests validate the API endpoints for managing roles in Dash-Backend. These tests ensure correct access control, data validation, and response structure for all CRUD operations. The tests are designed for seamless integration with ReactAdmin-based Dash-Frontend.

## Test Files

- `CreateRoleTest.php`
- `DeleteRoleTest.php`
- `ReadRoleTest.php`
- `UpdateRoleTest.php`

## Route Mapping

All tests use standardized Dash API routes:

| Action      | Route Name                   | HTTP Method | Example Route                        |
|-------------|-----------------------------|-------------|--------------------------------------|
| List        | api.system.roles.getList     | GET         | /api/system/role                     |
| Create      | api.system.roles.create      | POST        | /api/system/role                     |
| Read One    | api.system.roles.getOne      | GET         | /api/system/role/{id}                |
| Update      | api.system.roles.update      | PUT         | /api/system/role/{id}                |
| Delete      | api.system.roles.delete      | DELETE      | /api/system/role/{id}                |

## Test Structure

### 1. CreateRoleTest

- **guests_cannot_create_roles**: Ensures unauthenticated users receive 401 Unauthorized.
- **unauthorized_users_cannot_create_roles**: Ensures users without permission receive 403 Forbidden.
- **authorized_users_can_create_a_role**: Validates successful creation and correct response structure.
- **the_attributes_are_validated_to_create_a_role**: Checks all validation rules for role creation.

### 2. DeleteRoleTest

- **guests_cannot_delete_roles**: Ensures unauthenticated users cannot delete.
- **unauthorized_users_cannot_delete_roles**: Ensures users without permission cannot delete.
- **authorized_users_can_delete_a_role**: Validates successful deletion and database state.

### 3. ReadRoleTest

- **guests_cannot_fetch_roles**: Ensures unauthenticated users cannot list or show.
- **unauthorized_users_cannot_fetch_roles**: Ensures users without permission cannot list or show.
- **authorized_users_can_fetch_a_list_of_roles**: Validates list response and item count.
- **authorized_users_can_fetch_a_single_role**: Validates single item fetch and response.

### 4. UpdateRoleTest

- **guests_cannot_update_roles**: Ensures unauthenticated users cannot update.
- **unauthorized_users_cannot_update_roles**: Ensures users without permission cannot update.
- **authorized_users_can_update_a_role**: Validates successful update and response.
- **the_attributes_are_validated_to_update_a_role**: Checks all validation rules for update.

## Validation Rules

Validation is handled by the Role request class:

- `name`: required, string, alpha_dash, max 255, unique
- `level`: required, integer, min user level, max Role::MAX_LEVEL
- `guard_name`: required, string, in:web

## Response Structure

- **Single Resource**: Flat JSON object with all attributes.
- **Collection**: Array of objects, optionally with meta information.

Example single resource:
```json
{
  "id": 1,
  "name": "admin",
  "guard_name": "web",
  "level": 1,
  "permissions": [],
  "permission_objects": []
}
```

## Test Utilities

- **signIn**: Authenticates a user for the test.
- **signInWithPermissionsTo**: Authenticates a user and assigns required permissions.
- **getValidAttributes**: Generates valid attributes for creation/update.

## Integration Notes

- Tests use Laravel's `RefreshDatabase` trait for isolation.
- Roles and permissions are seeded before each test.
- All route names match the backend API definitions for Dash.

## Extending Tests

To add more tests:
- Use the same structure and route naming conventions.
- Validate new attributes in the Role request class.
- Ensure response assertions match the actual API output.

## References

- [Dash Backend Documentation](../README.md)
- [ReactAdminBaseController](domain/app/Http/Controllers/API/Admin/ReactAdminBaseController.php)
- [Role Model](app/Models/Role.php)
- [Role Resource](app/Http/Resources/RoleResource.php)
- [Role Request](app/Http/Requests/API/System/RoleRequest.php)

