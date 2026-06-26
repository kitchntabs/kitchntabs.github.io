---
layout: default
title: F14-Auth-Access-Control COMPLETE PERMISSION SYSTEM
---

# Complete Permission System - Route-Based Implementation

> **Last Updated:** June 2025 — Updated for 4-role hierarchy and current permission counts.

## Overview

This permission system covers **ALL 777+ unique API endpoints** found in the application's routes. The permissions are organized into **53 logical groups** based on the route structure. The system now includes **4 roles** (System, TenancyAdmin, Tenant, User) with a complementary Multi-Tenant Policy layer for model-level ownership checks.

## System Structure

### Permission Organization

Permissions are grouped by **context.resource** pattern:

```
api.{context}.{resource}.{action}
│   │         │          │
│   │         │          └─ Action: getList, create, update, delete, etc.
│   │         └─ Resource: users, roles, products, tenants, etc.
│   └─ Context: system, app, ecommerce, common, etc.
└─ Prefix: Always 'api'
```

### Context Levels

| Context | Level | Description |
|---------|-------|-------------|
| **system** | 0 | System-level operations (permissions, roles, tenants) |
| **admin** | 1 | Administrative operations |
| **tenant** | 1 | Tenant-scoped operations |
| **app** | 2 | Application-level operations |
| **ecommerce** | 2 | E-commerce operations |
| **common** | 2 | Common resources (countries, regions, currencies) |
| **logistic** | 2 | Logistics operations |
| **tab** | 2 | POS/Tab operations |
| **auth** | 2 | Authentication operations |
| **example** | 2 | Example/demo resources |
| **public** | 2 | Public endpoints |

## Statistics

```
Total API Endpoints:     777+
Permission Groups:       53
Total Roles:             4

System Admin Access:     775 permissions (+ AccessMiddleware bypass)
Tenancy Admin Access:    782 permissions (shares Tenant config — TODO: separate file)
Tenant Admin Access:     782 permissions (95% coverage)
Normal User Access:      255 permissions (33% coverage)
```

## Permission Groups

### System Context (Level 0)
- `system.permissions` - Permission management
- `system.roles` - Role management
- `system.tenants` - Tenant management
- `system.users` - User management (system-wide)
- `system.subscriptions` - Subscription management
- `system.fcm` - Firebase Cloud Messaging
- `system.logs` - System logs
- `system.mall` - Mall system management

### Admin Context (Level 1)
- `admin.logistic` - Logistic administration

### Tenant Context (Level 1)
- `tenant.roles` - Tenant-specific roles
- `tenant.tenant` - Tenant self-management
- `tenant.user` - Tenant user management

### App Context (Level 2)
- `app.logs` - Application logs
- `app.tenant` - Application tenant operations

### E-commerce Context (Level 2)
- `ecommerce.brand` - Brand management
- `ecommerce.category` - Category management
- `ecommerce.product` - Product management
- `ecommerce.product_templates` - Product templates
- `ecommerce.product_import_instances` - Product imports
- `ecommerce.product_export_templates` - Product exports
- `ecommerce.product_logs` - Product logs
- `ecommerce.campaigns` - Campaign management
- `ecommerce.campaign_marketplaces` - Campaign marketplace associations
- `ecommerce.campaign_marketplace_products` - Campaign marketplace products
- `ecommerce.campaigns_calendar` - Campaign calendar
- `ecommerce.marketplace` - Marketplace management
- `ecommerce.system_marketplaces` - System marketplace configuration
- `ecommerce.system_marketplace_categories` - System marketplace categories
- `ecommerce.system_marketplace_metadata_formats` - Marketplace metadata formats
- `ecommerce.metadata_formats` - Metadata formats
- `ecommerce.point_of_sales` - Point of sale management
- `ecommerce.system_point_of_sales` - System POS configuration
- `ecommerce.point_of_sale_associations` - POS associations
- `ecommerce.orders` - Order management
- `ecommerce.prices` - Price management
- `ecommerce.pricelists` - Pricelist management
- `ecommerce.stock` - Stock management
- `ecommerce.stock_type` - Stock type management
- `ecommerce.currency` - Currency management (ecommerce)
- `ecommerce.modifiers` - Modifiers management
- `ecommerce.gallery` - Gallery management
- `ecommerce.stats` - Statistics

### Common Context (Level 2)
- `common.communes` - Commune/district management
- `common.country` - Country management
- `common.currency` - Currency management (common)
- `common.region` - Region/state management

### Tab/POS Context (Level 2)
- `tab.cashcount` - Cash count operations
- `tab.kitchentab` - Kitchen tab operations
- `tab.tab` - Tab/order management

### Other Contexts (Level 2)
- `auth.update` - User profile updates
- `example.todo` - Example TODO resource
- `public.mall` - Public mall endpoints

## Role Permissions Breakdown

### System Admin (Level 0) - 775 Permissions

**Access Level:** FULL - All operations on all endpoints. Bypasses AccessMiddleware entirely.

**Capabilities:**
- ✅ Full CRUD on all resources
- ✅ System configuration (permissions, roles)
- ✅ Tenant management (create, update, delete, trash operations)
- ✅ E-commerce operations
- ✅ Logistics management
- ✅ POS/Tab operations
- ✅ All administrative functions

**Excluded:** None

**Permission File:** `rolePermissions/systemAdminPermissions.json`

---

### Tenancy Admin (Level 1) - 782 Permissions (shares Tenant config)

**Access Level:** Multi-tenant management authority. Currently identical to Tenant Admin.

**Current State:** Uses `tenantAdminPermissions.json` (same as Tenant Admin). A dedicated `tenancyAdminPermissions.json` is a **TODO** in the `RoleSeeder`.

**Permission File:** `rolePermissions/tenantAdminPermissions.json` (temporary)

---

### Tenant Admin (Level 2) - 782 Permissions (95%)

**Access Level:** Almost full access, except system permission/role management

**Capabilities:**
- ✅ Tenant operations (view, update)
- ✅ User management (full CRUD)
- ✅ E-commerce operations (full CRUD)
- ✅ Product management
- ✅ Order management
- ✅ Campaign management
- ✅ Marketplace operations
- ✅ POS/Tab operations
- ✅ Stock management
- ✅ Common resources (countries, regions, etc.)

**Excluded:**
- ❌ `api.system.permission.*` (32 permissions) - Cannot manage system permissions
- ❌ `api.system.role.*` (0 permissions in current routes) - Cannot manage system roles

**Reasoning:** Tenant admins should manage their business operations but not alter the fundamental permission system.

**Permission File:** `rolePermissions/tenantAdminPermissions.json`

---

### Normal User (Level 3) - 255 Permissions (33%)

**Access Level:** Read-only operations across most resources

**Capabilities:**
- ✅ View/List operations (getList, getOne, getMany, getManyReference)
- ✅ Filter operations (filterValues, filterValue)
- ✅ Select operations (getForSelect)
- ✅ Read-only access to:
  - Products
  - Categories
  - Brands
  - Orders
  - Campaigns
  - Marketplace data
  - Stock information
  - Common resources
  - POS data

**Excluded:**
- ❌ All Create operations
- ❌ All Update operations
- ❌ All Delete operations
- ❌ System administration (permissions, roles, tenants)
- ❌ Administrative operations

**Reasoning:** Normal users need visibility into system data for operational purposes but should not modify critical resources.

**Permission File:** `rolePermissions/normalUserPermissions.json`

## File Structure

```
database/data/
├── systemPermissions.json              (53 groups, 777+ permissions)
├── systemPermissions.json.backup       (previous version)
└── rolePermissions/
    ├── systemAdminPermissions.json     (775 permissions)
    ├── systemAdminPermissions.json.backup
    ├── tenantAdminPermissions.json     (782 permissions — used by TenancyAdmin too)
    ├── tenantAdminPermissions.json.backup
    ├── normalUserPermissions.json      (255 permissions - 33% coverage)
    ├── normalUserPermissions.json.backup
    └── README.md
```

## Seeding Process

```bash
# 1. Seed permissions (creates all 759 permissions in database)
./vendor/bin/sail artisan db:seed --class=PermissionSeeder

# 2. Seed roles (assigns permissions to each role)
./vendor/bin/sail artisan db:seed --class=RoleSeeder

# 3. Full fresh seed
./vendor/bin/sail artisan migrate:fresh --seed
```

## Validation

```bash
# Validate all permission configurations
./vendor/bin/sail artisan validate:role-permissions

# Expected output:
# - 53 permission groups validated
# - All route names exist in systemPermissions.json
# - All role permissions reference valid routes
# - No missing or orphaned permissions
```

## Customization

### Commenting Out Unused Permissions

Since all endpoints are included, you can comment out unused permissions:

1. **In systemPermissions.json** - Remove entire groups or individual permissions not needed
2. **In role permission files** - Remove specific route names from the permissions array

### Example: Disable Example TODO Module

**systemPermissions.json:**
```json
// Remove or comment this group
{
  "group": "example.todo",
  "level": 2,
  "labels": [ ... ]
}
```

**Role permission files:**
```json
{
  "permissions": [
    // Remove these lines
    // "api.example.todo.getList",
    // "api.example.todo.create",
    ...
  ]
}
```

### Adding Custom Permissions

If new endpoints are added:

1. Add to `systemPermissions.json`:
```json
{
  "group": "custom.resource",
  "level": 2,
  "labels": [
    {"name": "List Resource", "route_name": "api.custom.resource.getList"}
  ]
}
```

2. Add to appropriate role files:
```json
{
  "permissions": [
    "api.custom.resource.getList"
  ]
}
```

3. Re-seed:
```bash
./vendor/bin/sail artisan db:seed --class=PermissionSeeder
./vendor/bin/sail artisan db:seed --class=RoleSeeder
```

## Common Operations

### Check What Permissions Are Assigned

```bash
./vendor/bin/sail artisan tinker

# System Admin
>>> $role = Role::where('name', 'System')->first();
>>> $role->permissions->count(); // Should be 775

# Tenancy Admin
>>> $role = Role::where('name', 'TenancyAdmin')->first();
>>> $role->permissions->count(); // Should be 782

# Tenant Admin
>>> $role = Role::where('name', 'Tenant')->first();
>>> $role->permissions->count(); // Should be 782

# Normal User
>>> $role = Role::where('name', 'User')->first();
>>> $role->permissions->count(); // Should be 255
```

### List Permissions By Group

```bash
>>> $permissions = Permission::where('route_name', 'LIKE', 'api.ecommerce.product.%')->get();
>>> $permissions->pluck('route_name');
```

### Check User Access

```bash
>>> $user = User::find(1);
>>> $user->hasPermissionTo('api.ecommerce.product.create');
>>> $user->can('api.ecommerce.product.update');
```

## Permission Naming Patterns

### Standard CRUD Operations
- `*.getList` - List/index all records
- `*.getOne` - Show single record
- `*.getMany` - Get multiple specific records
- `*.getManyReference` - Get records by reference
- `*.create` - Create new record
- `*.putCreate` - Create via PUT
- `*.update` - Update record
- `*.postUpdate` - Update via POST
- `*.delete` - Delete record
- `*.postDelete` - Delete via POST
- `*.deleteMany` - Bulk delete

### Advanced Operations
- `*.partial` - Partial update
- `*.updateMany` - Bulk update
- `*.filterValues` - Get filter options
- `*.filterValue` - Filter data
- `*.getForSelect` - Get options for dropdowns
- `*.changeStatus` - Change status

### Specialized Operations
- `*.publish` - Publish campaigns/products
- `*.pause` - Pause operations
- `*.finish` - Complete operations
- `*.import` - Import data
- `*.export` - Export data
- `*.download` - Download files

## Migration Notes

### From Previous System

The new system includes **ALL** endpoints that were previously missing:

**Previously Missing (Now Included):**
- All E-commerce endpoints (~400 permissions)
- Campaign management
- Product import/export
- Marketplace integration
- POS operations
- Tab management
- Logistics
- Common resources (countries, regions, communes)

**Backward Compatibility:**
- All previous permissions remain valid
- New permissions are additive
- Existing role assignments will need re-seeding

## Security Considerations

1. **Permission Explosion:** With 759 permissions, review what each role truly needs
2. **Read-Only Users:** Normal users have extensive read access - audit if needed
3. **Comment Out Unused:** Disable unused endpoints to reduce attack surface
4. **Regular Audits:** Periodically review which permissions are actually used
5. **Least Privilege:** Start with minimal permissions, add as needed

## Troubleshooting

### Too Many Permissions Error

If you encounter database/performance issues:

```bash
# Chunk the seeding process
# Edit RoleSeeder to use chunking (already implemented)
```

### Permission Not Found

```bash
# Check if permission exists
>>> Permission::where('route_name', 'api.xxx.yyy.zzz')->first()

# Re-seed if missing
>>> ./vendor/bin/sail artisan db:seed --class=PermissionSeeder
```

### Role Has Wrong Permission Count

```bash
# Clear cache
>>> ./vendor/bin/sail artisan cache:clear

# Re-sync role permissions
>>> ./vendor/bin/sail artisan db:seed --class=RoleSeeder
```

## Next Steps

1. ✅ Review the generated permissions
2. ⚠️ Comment out unused endpoint groups
3. ✅ Test permission assignments
4. ✅ Seed database with new permissions
5. ✅ Validate all roles have correct access
6. ⚠️ Update frontend to match new permission structure
7. ⚠️ Document business-specific permission requirements

## Related Files

- **Main Documentation:** `ROLE_PERMISSION_SYSTEM.md`
- **Quick Reference:** `ROLE_PERMISSION_QUICK_REFERENCE.md`
- **Visual Guide:** `ROLE_PERMISSION_VISUAL_GUIDE.md`
- **Multi-Tenant Policy:** `docs/MULTI_TENANT_POLICY_GUIDE.md`
- **Tenancy Architecture:** `docs/TENANCY_ARCHITECTURE.md`
