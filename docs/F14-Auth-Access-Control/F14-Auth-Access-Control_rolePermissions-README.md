
# Role Permissions Configuration

> **Last Updated:** July 2025

This directory contains JSON configuration files that define the default permissions for each system role.

## Files

- **systemAdminPermissions.json** - System Administrator (Level 0) — 775 permissions
- **tenantAdminPermissions.json** - Tenant Administrator (Level 2) — 782 permissions (also used by TenancyAdmin)
- **normalUserPermissions.json** - Normal User (Level 3) — 255 permissions

> **Note:** The `TenancyAdmin` role (Level 1) currently shares `tenantAdminPermissions.json` with `Tenant`. A dedicated `tenancyAdminPermissions.json` is planned (see TODO in `RoleSeeder.php`).

## Roles

| Role | Constant | Level | Permission File | Count |
|------|----------|-------|-----------------|-------|
| System | `Role::NAME_SYSTEM_ADMIN` | 0 | `systemAdminPermissions.json` | 775 |
| TenancyAdmin | `Role::NAME_TENANCY_ADMIN` | 1 | `tenantAdminPermissions.json` (shared) | 782 |
| Tenant | `Role::NAME_TENANT_ADMIN` | 2 | `tenantAdminPermissions.json` | 782 |
| User | `Role::NAME_NORMAL_USER` | 3 | `normalUserPermissions.json` | 255 |

## Structure

Each JSON file follows this schema:

```json
{
  "role": "System",           // Role name (matches Role::NAME_* constant)
  "level": 0,                 // Role level (matches Role::LEVEL_* constant)
  "description": "...",       // Human-readable description
  "permissions": [            // Array of permission route names
    "api.system.permission.getList",
    "api.system.role.create"
  ]
}
```

## Usage

These files are automatically loaded by the `RoleSeeder` during database seeding:

```bash
php artisan db:seed --class=RoleSeeder
```

The seeder will:
1. Create or find each role
2. Load its corresponding permissions JSON file
3. Look up permissions by `route_name`
4. Sync the permissions to the role using `syncPermissions()`

## Modifying Permissions

To change default permissions for a role:

1. Edit the appropriate JSON file
2. Add or remove `route_name` values from the `permissions` array
3. Re-run the seeder:
   ```bash
   php artisan db:seed --class=RoleSeeder
   ```

**Note:** The route names must exist in the `permissions` table (seeded by `PermissionSeeder`).

## Permission Route Names

Permission route names follow this convention:

```
api.{context}.{resource}.{action}
```

**Examples:**
- `api.system.users.getList` - List users
- `api.system.permission.create` - Create permission
- `api.admin.tenants.update` - Update tenant
- `api.admin.trash.tenants.delete` - Permanently delete trashed tenant

## Validation

The seeder validates:
- ✓ File exists and is readable
- ✓ JSON is valid
- ✓ `permissions` array exists
- ✓ Permissions exist in database
- ✓ Role exists

Errors are logged and displayed during seeding.

## Best Practices

1. **Keep permissions scoped** - Each role should have minimum necessary permissions
2. **Document changes** - Update role descriptions when modifying permissions
3. **Test after changes** - Verify roles work as expected
4. **Version control** - Commit changes to these files
5. **Use route names** - Always reference permissions by route_name, not ID

## See Also

- `database/data/systemPermissions.json` - Permission definitions (53 groups, 777 permissions)
- `database/seeders/RoleSeeder.php` - Role seeding logic (4 roles)
- `app/Models/Role.php` - Role constants and levels
- `app/Http/Middleware/AccessMiddleware.php` - Route-level permission enforcement
- `domain/app/Policies/Extended/TenantPolicy.php` - Model-level authorization (multi-tenant)
- `ROLE_PERMISSION_SYSTEM.md` - Complete system documentation
- `docs/MULTI_TENANT_POLICY_GUIDE.md` - Multi-tenant policy layer documentation
