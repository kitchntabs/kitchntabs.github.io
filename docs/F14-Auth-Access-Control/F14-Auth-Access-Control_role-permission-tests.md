# Role Permission Feature Tests Documentation

## Overview

The Role Permission feature tests validate the endpoints responsible for assigning and retrieving permissions for a specific role in Dash-Backend. These tests cover access control, request validation, and response structure for the endpoints consumed by the Dash-Frontend ReactAdmin flows.

## Test Files

- `ReadRolePermissionTest.php`
- `StoreRolePermissionTest.php`

## Route Mapping

| Action              | Route Name                               | HTTP Method | Example Route                                   |
|---------------------|-------------------------------------------|-------------|-------------------------------------------------|
| List role permissions | api.system.role.permissions.getList       | GET         | /api/system/role/{id}/permissions               |
| Sync role permissions | api.system.role.permissions.create        | POST        | /api/system/role/{id}/permissions               |

## Test Structure

### 1. ReadRolePermissionTest

- **guests_cannot_fetch_role_permissions**: Ensures unauthenticated callers receive 401 Unauthorized.
- **unauthorized_users_cannot_fetch_role_permissions**: Verifies users without the `api.system.role.permissions.getList` permission receive 403 Forbidden.
- **authorized_users_can_fetch_a_list_of_role_permissions**: Confirms authorized users receive a 200 response with the permission collection and meta payload.
- **system_admin_can_fetch_role_permissions**: Asserts a System Admin role can access the endpoint and successfully retrieve permissions regardless of assignment.
- **tenant_admin_can_fetch_role_permissions_if_permission_assigned**: Checks a Tenant Admin with the explicit permission can access the endpoint.
- **normal_user_cannot_fetch_role_permissions**: Ensures Normal users without privileges receive 403 Forbidden.

### 2. StoreRolePermissionTest

- **guests_cannot_store_role_permissions**: Ensures unauthenticated requests receive 401 Unauthorized.
- **unauthorized_users_cannot_store_role_permissions**: Confirms users lacking `api.system.role.permissions.create` cannot sync permissions.
- **authorized_users_can_store_role_permissions**: Validates a successful sync returns the updated permission collection and meta payload.
- **authorized_users_cannot_store_role_permissions_with_levels_lower_than_their_own**: Enforces level-based restrictions when assigning permissions to roles.
- **the_attributes_are_validated_to_store_role_permissions**: Covers validation errors for missing, invalid, or unknown permission identifiers.

## Validation Rules

Validation is handled inline within `RoleController::storePermissions`:

- `permissions` (required) must be an array.
- `permissions.*` must be an integer ID that exists in the `permissions` table.
- Only permissions with a level greater than or equal to the acting user's level are applied.

## Response Structure

Both endpoints return a standardized payload:

```json
{
  "data": [
    {
      "id": 1,
      "name": "List Permissions",
      "route_name": "api.system.permissions.getList",
      "group": "system.permissions",
      "level": 0
    }
  ],
  "meta": {
    "total": 1
  }
}
```

## Test Utilities

- **signIn**: Authenticates a user via Sanctum for the request cycle.
- **signInWithPermissionsTo**: Authenticates a user and assigns the required permission route names before making API calls.
- **seed(['PermissionSeeder'])**: Loads the base permission catalog to ensure permission lookups succeed.

## Integration Notes

- Tests leverage Laravel's `RefreshDatabase` trait for isolation and use model factories for roles, users, and permissions.
- Tenant provisioning side effects are disabled during tests to keep transactions consistent.
- Route names match the definitions in `routes/system.php` ensuring parity with Dash-Frontend expectations.

## Extending Tests

When introducing new role-permission behaviour:

1. Add permission definitions to `database/data/systemPermissions.json`.
2. Map new route names to the appropriate roles in `database/data/rolePermissions/*.json`.
3. Extend the tests with additional scenarios (e.g., batch sync failure cases).
4. Ensure the controller returns the standardized `{ data, meta }` payload and update tests accordingly.

## References

- [Role Controller](dash-backend/app/Http/Controllers/API/System/RoleController.php)
- [Permission Resource](dash-backend/app/Http/Resources/PermissionResource.php)
- [Role Model](dash-backend/app/Models/Role.php)
- [PermissionSeeder](dash-backend/database/seeders/PermissionSeeder.php)
- [ReadRolePermissionTest](dash-backend/tests/Feature/API/Admin/RolePermission/ReadRolePermissionTest.php)
- [StoreRolePermissionTest](dash-backend/tests/Feature/API/Admin/RolePermission/StoreRolePermissionTest.php)
