# Role & Permission System Documentation

> **Last Updated:** June 2025 — Updated to reflect 4-role hierarchy, current permission counts, AccessMiddleware documentation, and compatibility with the Multi-Tenant Policy system.

## Overview

The DASH application implements a hierarchical Role-Based Access Control (RBAC) system using Spatie's Laravel Permission package. The system uses **four roles** with level-based hierarchy, **53 permission groups** covering 777+ unique API endpoints, and a route-level `AccessMiddleware` for enforcement.

This permission system works as **Layer 1** (endpoint-level access control). For model-level ownership authorization, see the complementary Multi-Tenant Policy system documented in `docs/MULTI_TENANT_POLICY_GUIDE.md` and `docs/TENANCY_ARCHITECTURE.md`.

## System Architecture

### Role Hierarchy

The system uses a **level-based hierarchy** where lower numbers indicate higher authority:

| Role | Level | Name Constant | Level Constant | Description |
|------|-------|---------------|----------------|-------------|
| **System Admin** | 0 | `Role::NAME_SYSTEM_ADMIN` (`'System'`) | `Role::LEVEL_SYSTEM_ADMIN` | Highest authority - Full system access. Bypasses AccessMiddleware. |
| **Tenancy Admin** | 1 | `Role::NAME_TENANCY_ADMIN` (`'TenancyAdmin'`) | `Role::LEVEL_TENANCY_ADMIN` | Multi-tenant management authority. Currently shares Tenant Admin permissions (TODO: separate file). |
| **Tenant Admin** | 2 | `Role::NAME_TENANT_ADMIN` (`'Tenant'`) | `Role::LEVEL_TENANT_ADMIN` | Tenant-level authority - Manages business operations, e-commerce, users |
| **Normal User** | 3 | `Role::NAME_NORMAL_USER` (`'User'`) | `Role::LEVEL_NORMAL_USER` | Basic user - Read-only access to most resources |

> **Note:** `Role::MAX_LEVEL = 32767` is reserved for future use.

### AccessMiddleware (Route-Level Enforcement)

The `AccessMiddleware` (`app/Http/Middleware/AccessMiddleware.php`) enforces permissions at the route level:

1. **No auth** → `403`
2. **System Admin role** → **PASS** (bypasses all permission checks)
3. **Has matching permission** → **PASS**
4. **Otherwise** → `403`

**Applied to:** `system.*`, `tenant.*`, `ecommerce.*`, `app.*`, `tab.*`, `logistic.*` route groups.

**NOT applied to:** `tenancy.*` routes (only `auth:sanctum`), `public.*` routes (no auth required).

> **Important:** `Gate::before` is defined in both `AuthServiceProvider` files but is currently **not active** (not called in `boot()`). The System Admin bypass works because AccessMiddleware explicitly checks `hasRole(Role::NAME_SYSTEM_ADMIN)`.

### Permission Structure

Permissions are organized into **groups** and assigned **levels** matching their minimum required role level:

```json
{
    "group": "permissions",
    "level": 0,
    "labels": [
        {
            "name": "List Permissions",
            "route_name": "api.system.permission.getList"
        }
    ]
}
```

#### Current Permission Groups (53 groups)

**System Context (Level 0):**
- `system.permissions` — Permission management
- `system.roles` — Role management
- `system.tenants` — Tenant management
- `system.users` — User management (system-wide)
- `system.subscriptions` — Subscription management
- `system.fcm` — Firebase Cloud Messaging
- `system.logs` — System logs
- `system.mall` — Mall system management

**Admin Context (Level 1):**
- `admin.logistic` — Logistic administration

**Tenant Context (Level 1):**
- `tenant.roles` — Tenant-specific roles
- `tenant.tenant` — Tenant self-management
- `tenant.user` — Tenant user management

**App Context (Level 2):**
- `app.logs` — Application logs
- `app.tenant` — Application tenant operations

**E-commerce Context (Level 2):**
- `ecommerce.brand`, `ecommerce.category`, `ecommerce.product`, `ecommerce.product_templates`, `ecommerce.product_import_instances`, `ecommerce.product_export_templates`, `ecommerce.product_logs`, `ecommerce.campaigns`, `ecommerce.campaign_marketplaces`, `ecommerce.campaign_marketplace_products`, `ecommerce.campaigns_calendar`, `ecommerce.marketplace`, `ecommerce.system_marketplaces`, `ecommerce.system_marketplace_categories`, `ecommerce.system_marketplace_metadata_formats`, `ecommerce.metadata_formats`, `ecommerce.point_of_sales`, `ecommerce.system_point_of_sales`, `ecommerce.point_of_sale_associations`, `ecommerce.orders`, `ecommerce.prices`, `ecommerce.pricelists`, `ecommerce.stock`, `ecommerce.stock_type`, `ecommerce.currency`, `ecommerce.modifiers`, `ecommerce.gallery`, `ecommerce.stats`

**Common Context (Level 2):**
- `common.communes`, `common.country`, `common.currency`, `common.region`

**Tab/POS Context (Level 2):**
- `tab.cashcount`, `tab.kitchentab`, `tab.tab`

**Other Contexts (Level 2):**
- `auth.update`, `example.todo`, `public.mall`

### Access Control Rules

1. **Level-Based Access**: Users can only manage roles/permissions at their level or higher
   - System Admin (Level 0) can manage everything; bypasses AccessMiddleware
   - Tenancy Admin (Level 1) manages tenancy-level operations
   - Tenant Admin (Level 2) can manage Level 2+ (business operations, users)
   - Normal User (Level 3) has read-only access

2. **Policy Enforcement**: The `RolePolicy` ensures users cannot modify roles above their level:
   ```php
   public function manage(User $user, Role $role)
   {
       return $user->level <= $role->level;
   }
   ```

3. **Multi-Tenant Policy Layer** (complementary): The `MultiTenantAuthorizationTrait` adds model-level ownership checks on top of endpoint permissions. See `docs/MULTI_TENANT_POLICY_GUIDE.md`.

## Default Role Permissions

### System Admin (Level 0) — 775 permissions

**Full System Access** — Can perform all operations across the entire system. Bypasses AccessMiddleware entirely.

**Capabilities:**
- ✓ All Permission CRUD operations
- ✓ All Role CRUD operations  
- ✓ All Tenant CRUD operations (including trash)
- ✓ All User CRUD operations
- ✓ All E-commerce operations
- ✓ All POS/Tab operations
- ✓ All Logistics operations
- ✓ All administrative functions

**Configuration:** `database/data/rolePermissions/systemAdminPermissions.json`

### Tenancy Admin (Level 1) — 782 permissions (shares Tenant config)

**Multi-Tenant Management** — Intended for users who manage multiple tenants across a tenancy.

**Current State:** Uses `tenantAdminPermissions.json` (same as Tenant Admin). A dedicated `tenancyAdminPermissions.json` is a **TODO** in the `RoleSeeder`.

**Configuration:** `database/data/rolePermissions/tenantAdminPermissions.json` (temporary)

### Tenant Admin (Level 2) — 782 permissions

**Business Operations Management** — Can manage all tenant business operations including e-commerce, products, orders, campaigns, POS, users.

**Capabilities:**
- ✓ Tenant operations (view, update own tenant)
- ✓ User management (full CRUD)
- ✓ E-commerce operations (full CRUD)
- ✓ Product management, Order management, Campaign management
- ✓ Marketplace and POS/Tab operations
- ✓ Stock management, Common resources
- ✗ Cannot manage system permissions (`api.system.permission.*`)
- ✗ Cannot manage system roles (`api.system.role.*`)

**Configuration:** `database/data/rolePermissions/tenantAdminPermissions.json`

### Normal User (Level 3) — 255 permissions

**Read-Only Access** — Read-only access across most resources.

**Capabilities:**
- ✓ View/List operations (getList, getOne, getMany, getManyReference)
- ✓ Filter and Select operations
- ✓ Read-only access to products, categories, orders, campaigns, stock, POS data
- ✗ Cannot create, update, or delete resources
- ✗ Cannot access system administration

**Configuration:** `database/data/rolePermissions/normalUserPermissions.json`

## File Structure

```
dash-backend/
├── app/
│   ├── Models/
│   │   ├── Role.php              # Role model with 4 role constants
│   │   └── Permission.php        # Permission model (route_name, group, level)
│   ├── Policies/
│   │   └── RolePolicy.php        # Level-based authorization logic
│   ├── Http/
│   │   ├── Middleware/
│   │   │   └── AccessMiddleware.php  # Route-level permission enforcement
│   │   ├── Resources/
│   │   │   ├── RoleResource.php
│   │   │   └── PermissionResource.php
│   │   └── Requests/
│   │       └── API/System/
│   │           ├── PermissionRequest.php
│   │           └── RolePermissionRequest.php
│   └── Jobs/
│       └── SyncRolePermissionsJob.php  # Background permission sync
├── database/
│   ├── data/
│   │   ├── systemPermissions.json       # 777 permission definitions (53 groups)
│   │   └── rolePermissions/
│   │       ├── systemAdminPermissions.json   # 775 permissions
│   │       ├── tenantAdminPermissions.json   # 782 permissions (used by TenancyAdmin too)
│   │       ├── normalUserPermissions.json    # 255 permissions
│   │       └── README.md
│   └── seeders/
│       ├── PermissionSeeder.php      # Creates permissions from JSON + domain
│       └── RoleSeeder.php            # Creates 4 roles & assigns permissions
├── domain/
│   └── app/
│       └── Policies/
│           ├── Traits/
│           │   └── MultiTenantAuthorizationTrait.php  # Model ownership checks
│           └── Extended/
│               └── TenantPolicy.php   # 3-tier tenant authorization
└── docs/
    ├── MULTI_TENANT_POLICY_GUIDE.md   # Multi-tenant policy documentation
    └── TENANCY_ARCHITECTURE.md        # Tenancy architecture documentation
```

## Seeding Process

The database seeding follows this order:

1. **PermissionSeeder** - Creates all permissions from `systemPermissions.json` (777 permissions across 53 groups) and domain-specific permissions
2. **RoleSeeder** - Creates 4 roles and assigns default permissions from JSON configs:
   - System Admin → `systemAdminPermissions.json` (775 permissions)
   - Tenancy Admin → `tenantAdminPermissions.json` (782 permissions, shared — TODO: separate file)
   - Tenant Admin → `tenantAdminPermissions.json` (782 permissions)
   - Normal User → `normalUserPermissions.json` (255 permissions)
3. **UserSeeder** - Creates initial users and assigns roles

### Running Seeders

```bash
# Fresh migration with seeding
php artisan migrate:fresh --seed

# Run specific seeder
php artisan db:seed --class=RoleSeeder
```

## Adding New Permissions

### 1. Define in systemPermissions.json

Add to the appropriate group:

```json
{
    "group": "products",
    "level": 2,
    "labels": [
        {
            "name": "List Products",
            "route_name": "api.system.products.getList"
        },
        {
            "name": "Create Product",
            "route_name": "api.system.products.create"
        }
    ]
}
```

### 2. Update Role Permission Configs

Add the route names to the appropriate role permission JSON files:

**systemAdminPermissions.json:**
```json
{
    "permissions": [
        "api.system.products.getList",
        "api.system.products.create",
        "api.system.products.update",
        "api.system.products.delete"
    ]
}
```

**tenantAdminPermissions.json:**
```json
{
    "permissions": [
        "api.system.products.getList",
        "api.system.products.create"
    ]
}
```

### 3. Run Seeders

```bash
php artisan db:seed --class=PermissionSeeder
php artisan db:seed --class=RoleSeeder
```

## Permission Checking

### In Controllers

```php
// Check specific permission
$this->authorize('api.system.user.create');

// Check role management
$this->authorize('manage', $role);
```

### In Routes

```php
Route::middleware(['permission:api.system.user.create'])
    ->post('/users', [UserController::class, 'store']);
```

### In Blade/Views

```php
@can('api.system.user.create')
    <button>Create User</button>
@endcan
```

## Permission Sync Job

The `SyncRolePermissionsJob` handles bulk permission assignments asynchronously:

```php
// Dispatch chunked permission sync
SyncRolePermissionsJob::dispatchChunked(
    roleId: $role->id,
    permissionObjects: $permissionArray,
    isEcommerce: false
);
```

## Best Practices

1. **Always use route names** as permission identifiers (not numeric IDs)
2. **Group related permissions** together for easier management
3. **Set appropriate levels** - permissions should match their minimum required role level
4. **Use Policy classes** for complex authorization logic
5. **Clear cache** after permission changes: `app()['cache']->forget('spatie.permission.cache')`
6. **Test thoroughly** after modifying permission configurations
7. **Document changes** in role permission JSON files

## Troubleshooting

### Permissions not applying after seeding
```bash
php artisan cache:clear
php artisan config:clear
```

### Role can't be found
```bash
# Check if roles were created
php artisan tinker
>>> App\Models\Role::all();
```

### Permission denied unexpectedly
- Verify user has the correct role assigned
- Check permission exists in database
- Confirm role has permission assigned
- Clear Spatie permission cache

## Security Considerations

1. **Level protection** - Users cannot escalate privileges beyond their level
2. **Policy enforcement** - All role modifications check authorization
3. **Audit trails** - Permission changes should be logged
4. **Minimal permissions** - Grant only necessary permissions (principle of least privilege)
5. **Regular review** - Periodically audit role permissions

## Future Enhancements

- [ ] Dedicated `tenancyAdminPermissions.json` for TenancyAdmin role (currently shares Tenant file)
- [ ] Activate `Gate::before` or remove dead code from AuthServiceProviders
- [ ] Dynamic permission creation through UI
- [ ] Permission templates for common role types
- [ ] Permission inheritance/cascading
- [ ] Time-based permission grants
- [ ] Permission usage analytics
- [ ] Multi-tenant permission isolation

## Dual Authorization Layer Compatibility

The DASH system uses **two complementary authorization layers**:

| Layer | Mechanism | Scope | Purpose |
|-------|-----------|-------|---------|
| **Layer 1**: Spatie Permissions | `AccessMiddleware` + Role/Permissions | Route-level | "Does this user have permission to access this endpoint?" |
| **Layer 2**: Multi-Tenant Policies | `MultiTenantAuthorizationTrait` + Policies | Model-level | "Does this user own / have access to this specific resource?" |

Both layers must pass for an action to succeed. They are **additive** — the multi-tenant policy system does NOT override or replace the base permission system.

For full details, see:
- `docs/MULTI_TENANT_POLICY_GUIDE.md` — Policy implementation guide
- `docs/TENANCY_ARCHITECTURE.md` — Full tenancy architecture documentation
