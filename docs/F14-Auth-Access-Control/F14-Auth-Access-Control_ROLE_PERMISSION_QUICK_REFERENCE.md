---
layout: default
title: F14-Auth-Access-Control ROLE PERMISSION QUICK REFERENCE
---

# Quick Reference: Role Permission System

> **Last Updated:** June 2025 — Updated for 4-role hierarchy (System, TenancyAdmin, Tenant, User).

## 🎯 Quick Commands

### Validate Configurations
```bash
# Check all role permission configs are valid
./vendor/bin/sail artisan validate:role-permissions

# Or without docker
php artisan validate:role-permissions
```

### Fresh Database Setup
```bash
# Complete fresh setup with permissions
./vendor/bin/sail artisan migrate:fresh --seed
```

### Re-seed Permissions Only
```bash
# Update permission definitions
./vendor/bin/sail artisan db:seed --class=PermissionSeeder

# Update role assignments
./vendor/bin/sail artisan db:seed --class=RoleSeeder
```

### Clear Caches
```bash
./vendor/bin/sail artisan cache:clear
./vendor/bin/sail artisan config:clear
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `database/data/systemPermissions.json` | Permission definitions (777 perms, 53 groups) |
| `database/data/rolePermissions/systemAdminPermissions.json` | System Admin defaults (775) |
| `database/data/rolePermissions/tenantAdminPermissions.json` | Tenant Admin defaults (782) — also used by TenancyAdmin |
| `database/data/rolePermissions/normalUserPermissions.json` | Normal User defaults (255) |
| `database/seeders/PermissionSeeder.php` | Creates permissions |
| `database/seeders/RoleSeeder.php` | Creates 4 roles + assigns permissions |
| `app/Models/Role.php` | Role constants (4 roles) |
| `app/Models/Permission.php` | Permission model |
| `app/Http/Middleware/AccessMiddleware.php` | Route-level permission enforcement |
| `app/Policies/RolePolicy.php` | Level-based authorization logic |

## 🔑 Role Constants

```php
// In app/Models/Role.php
Role::NAME_SYSTEM_ADMIN  = 'System'       // Level 0 — Bypasses AccessMiddleware
Role::NAME_TENANCY_ADMIN = 'TenancyAdmin' // Level 1 — Multi-tenant management
Role::NAME_TENANT_ADMIN  = 'Tenant'       // Level 2 — Business operations
Role::NAME_NORMAL_USER   = 'User'         // Level 3 — Read-only access
```

## 📊 Default Permission Counts

- **System Admin** → 775 permissions (full access + AccessMiddleware bypass)
- **Tenancy Admin** → 782 permissions (shares Tenant config — TODO: separate file)
- **Tenant Admin** → 782 permissions (business operations, no system admin)
- **Normal User** → 255 permissions (read-only across most resources)

## ✏️ How to Modify Permissions

### Add Permission to System
1. Edit `database/data/systemPermissions.json`:
   ```json
   {
     "group": "products",
     "level": 2,
     "labels": [
       {"name": "List Products", "route_name": "api.system.products.getList"}
     ]
   }
   ```
2. Run: `sail artisan db:seed --class=PermissionSeeder`

### Assign Permission to Role
1. Edit role config (e.g., `systemAdminPermissions.json`):
   ```json
   {
     "permissions": [
       "existing.permission",
       "api.system.products.getList"  // ← Add this
     ]
   }
   ```
2. Run: `sail artisan db:seed --class=RoleSeeder`

## 🔍 Verification

### Check Role Permissions in Tinker
```php
./vendor/bin/sail artisan tinker

// Check System Admin
$system = Role::where('name', 'System')->with('permissions')->first();
$system->permissions->count(); // Should be 775

// Check Tenancy Admin
$tenancy = Role::where('name', 'TenancyAdmin')->with('permissions')->first();
$tenancy->permissions->count(); // Should be 782 (shares Tenant config)

// Check Tenant Admin
$tenant = Role::where('name', 'Tenant')->with('permissions')->first();
$tenant->permissions->count(); // Should be 782

// Check Normal User
$user = Role::where('name', 'User')->with('permissions')->first();
$user->permissions->count(); // Should be 255

// Check all roles
Role::with('permissions')->get()->map(function($r) {
    return ['name' => $r->name, 'level' => $r->level, 'count' => $r->permissions->count()];
});
```

### Check User Permissions
```php
$user = User::find(1);
$user->roles;
$user->permissions;
$user->hasPermissionTo('api.system.user.getList');
```

## 🐛 Troubleshooting

### Permissions not working after seeding
```bash
./vendor/bin/sail artisan cache:clear
./vendor/bin/sail artisan config:clear
```

### "Permission does not exist" error
```bash
# Verify permission exists
./vendor/bin/sail artisan tinker
>>> Permission::where('route_name', 'your.route.name')->first()

# If not found, check systemPermissions.json and re-seed
./vendor/bin/sail artisan db:seed --class=PermissionSeeder
```

### Role has no permissions
```bash
# Re-run role seeder
./vendor/bin/sail artisan db:seed --class=RoleSeeder

# Check logs for errors
tail -f storage/logs/laravel.log
```

## 📚 Permission Naming Convention

```
api.{context}.{resource}.{action}
│   │        │          │
│   │        │          └─ Action: getList, create, update, delete, etc.
│   │        └─ Resource: users, tenants, permissions, etc.
│   └─ Context: system, admin, etc.
└─ Prefix: Always 'api'
```

**Examples:**
- `api.system.user.getList`
- `api.system.permission.create`
- `api.admin.tenants.update`
- `api.admin.trash.tenants.delete`

## ⚡ Common Tasks

### Create new admin user with System role
```php
./vendor/bin/sail artisan tinker

$user = User::create([
    'name' => 'Admin User',
    'email' => 'admin@example.com',
    'password' => bcrypt('password')
]);

$role = Role::where('name', 'System')->first();
$user->assignRole($role);
```

### Check what a user can do
```php
$user = User::find(1);
$user->getAllPermissions()->pluck('route_name');
```

### Add custom permission to existing role
```php
$role = Role::where('name', 'Tenant')->first();
$permission = Permission::where('route_name', 'api.custom.action')->first();
$role->givePermissionTo($permission);
```

## 📖 Documentation

- **Full System Docs:** `ROLE_PERMISSION_SYSTEM.md`
- **Complete Permission List:** `COMPLETE_PERMISSION_SYSTEM.md`
- **Visual Guide:** `ROLE_PERMISSION_VISUAL_GUIDE.md`
- **Config README:** `database/data/rolePermissions/README.md`
- **Multi-Tenant Policy:** `docs/MULTI_TENANT_POLICY_GUIDE.md`
- **Tenancy Architecture:** `docs/TENANCY_ARCHITECTURE.md`

## ✅ Checklist for Adding New Feature

- [ ] Define permissions in `systemPermissions.json`
- [ ] Seed permissions: `sail artisan db:seed --class=PermissionSeeder`
- [ ] Add to role configs (systemAdmin, tenantAdmin, normalUser)
- [ ] Seed roles: `sail artisan db:seed --class=RoleSeeder`
- [ ] Validate: `sail artisan validate:role-permissions`
- [ ] Add authorization checks in controllers
- [ ] Test with different role levels
- [ ] Update documentation
