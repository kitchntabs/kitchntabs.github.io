---
layout: default
title: F14-Auth-Access-Control ROLE PERMISSION VISUAL GUIDE
---

# Role Permission System - Visual Overview

> **Last Updated:** June 2025 — Updated for 4-role hierarchy and current permission counts.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     DASH PERMISSION SYSTEM                          │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                    ROLE HIERARCHY (4 Roles)                  │   │
│  │                                                            │   │
│  │  Level 0: System Admin  ──────────────────┐               │   │
│  │         (Full Access + Middleware Bypass) │               │   │
│  │              │                            │               │   │
│  │              │ can manage                 │               │   │
│  │              ▼                            │               │   │
│  │  Level 1: Tenancy Admin  ───────────────┤               │   │
│  │         (Multi-Tenant Mgmt)              │               │   │
│  │              │                            │               │   │
│  │              │ can manage                 │               │   │
│  │              ▼                            │               │   │
│  │  Level 2: Tenant Admin  ────────────────┤               │   │
│  │         (Business Operations)              │               │   │
│  │              │                            │               │   │
│  │              │ can manage                 │               │   │
│  │              ▼                            │               │   │
│  │  Level 3: Normal User  ─────────────────┘               │   │
│  │         (Read Only)                                        │   │
│  │                                                            │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │               PERMISSION GROUPS (53 total)                 │   │
│  │                                                            │   │
│  │  System (L0)  Tenant (L1)  Ecommerce (L2)  Tabs (L2)      │   │
│  │  8 groups     3 groups     28 groups        3 groups       │   │
│  │                                                            │   │
│  │  Common (L2)  App (L2)     Other (L2)                      │   │
│  │  4 groups     2 groups     5 groups                        │   │
│  │                                                            │   │
│  └────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Permission Distribution

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                    ROLE PERMISSION SUMMARY (4 Roles)                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  System Admin  (L0)  │ 775 perms  │ Full access + AccessMiddleware bypass   │
│  Tenancy Admin (L1)  │ 782 perms  │ Multi-tenant mgmt (shares Tenant cfg)  │
│  Tenant Admin  (L2)  │ 782 perms  │ Business operations, no sys admin       │
│  Normal User   (L3)  │ 255 perms  │ Read-only across most resources         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Note: Tenancy Admin currently uses tenantAdminPermissions.json (same as
Tenant Admin). A dedicated tenancyAdminPermissions.json is a TODO.

Legend:
  L0-L3 = Role level (lower = higher authority)
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      SEEDING PROCESS                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────────┐
        │      1. PermissionSeeder.php             │
        │                                          │
        │  • Loads systemPermissions.json          │
        │  • Loads domain/permissions.json         │
        │  • Inserts into permissions table        │
        │                                          │
        │  Output: 777+ permissions in database    │
        └──────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────────┐
        │       2. RoleSeeder.php                  │
        │                                          │
        │  ┌────────────────────────────────────┐ │
        │  │ System Admin (Level 0)             │ │
        │  │ • Load: systemAdminPermissions.json│ │
        │  │ • Assign: 775 permissions          │ │
        │  └────────────────────────────────────┘ │
        │                                          │
        │  ┌────────────────────────────────────┐ │
        │  │ Tenancy Admin (Level 1)            │ │
        │  │ • Load: tenantAdminPermissions.json│ │
        │  │ • Assign: 782 permissions (shared) │ │
        │  │ • TODO: tenancyAdminPermissions    │ │
        │  └────────────────────────────────────┘ │
        │                                          │
        │  ┌────────────────────────────────────┐ │
        │  │ Tenant Admin (Level 2)             │ │
        │  │ • Load: tenantAdminPermissions.json│ │
        │  │ • Assign: 782 permissions          │ │
        │  └────────────────────────────────────┘ │
        │                                          │
        │  ┌────────────────────────────────────┐ │
        │  │ Normal User (Level 3)              │ │
        │  │ • Load: normalUserPermissions.json │ │
        │  │ • Assign: 255 permissions          │ │
        │  └────────────────────────────────────┘ │
        │                                          │
        │  Output: 4 roles with permissions        │
        └──────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────────┐
        │        3. UserSeeder.php                 │
        │                                          │
        │  • Creates initial users                 │
        │  • Assigns roles to users                │
        │                                          │
        └──────────────────────────────────────────┘
```

## Request Authorization Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                   HTTP REQUEST FLOW                              │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Incoming Request   │
                │  POST /api/users    │
                └─────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  auth:sanctum       │
                │  (Authentication)   │
                └─────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  AccessMiddleware   │
                │  (Layer 1)          │
                │                     │
                │  1. System Admin?   │──── Yes ──▶ PASS (bypass)
                │  2. Has permission? │──── Yes ──▶ PASS
                │  3. Otherwise       │──── No  ──▶ 403
                └─────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Policy Check       │
                │  (Layer 2, optional)│
                │  MultiTenantAuth    │
                │  Trait ownership    │
                └─────────────────────┘
                      │         │
                 ✓ Allowed  ✗ Denied
                      │         │
                      ▼         ▼
            ┌──────────────┐  ┌──────────────┐
            │   Execute    │  │   Return     │
            │   Controller │  │   403 Error  │
            │   Action     │  │              │
            └──────────────┘  └──────────────┘

Note: tenancy.* routes do NOT use AccessMiddleware (only auth:sanctum).
      public.* routes require no authentication at all.
```

## File Structure Diagram

```
dash-backend/
│
├── app/
│   ├── Models/
│   │   ├── Role.php ──────────────────── Role constants & model
│   │   │   • NAME_SYSTEM_ADMIN = 'System'      (Level 0)
│   │   │   • NAME_TENANCY_ADMIN = 'TenancyAdmin' (Level 1)
│   │   │   • NAME_TENANT_ADMIN = 'Tenant'       (Level 2)
│   │   │   • NAME_NORMAL_USER = 'User'          (Level 3)
│   │   │
│   │   └── Permission.php ─────────────── Permission model
│   │       • MAX_LEVEL = 32767
│   │       • route_name, group, level
│   │
│   ├── Policies/
│   │   └── RolePolicy.php ────────────── Level-based authorization
│   │       • manage(): level-based check
│   │
│   ├── Http/
│   │   ├── Middleware/
│   │   │   └── AccessMiddleware.php ──── Route-level enforcement
│   │   │       • System Admin bypass
│   │   │       • Permission lookup by route_name
│   │   │
│   │   ├── Resources/
│   │   │   ├── RoleResource.php
│   │   │   └── PermissionResource.php
│   │   │
│   │   └── Requests/
│   │       └── API/System/
│   │           ├── PermissionRequest.php
│   │           └── RolePermissionRequest.php
│   │
│   ├── Jobs/
│   │   └── SyncRolePermissionsJob.php ── Async permission sync
│   │
│   └── Console/Commands/
│       └── ValidateRolePermissions.php ─ Validation command
│
├── database/
│   ├── data/
│   │   ├── systemPermissions.json ────── 777+ permission definitions (53 groups)
│   │   │
│   │   └── rolePermissions/
│   │       ├── systemAdminPermissions.json ─ 775 permissions
│   │       ├── tenantAdminPermissions.json ─ 782 permissions (also used by TenancyAdmin)
│   │       ├── normalUserPermissions.json ── 255 permissions
│   │       └── README.md
│   │
│   └── seeders/
│       ├── PermissionSeeder.php ──────── Creates permissions
│       │   1. Load systemPermissions.json
│       │   2. Load domain/permissions.json
│       │   3. Insert permissions
│       │
│       ├── RoleSeeder.php ────────────── Creates 4 roles + assigns
│       │   1. Create System role (L0)
│       │   2. Create TenancyAdmin role (L1, shared config)
│       │   3. Create Tenant role (L2)
│       │   4. Create User role (L3)
│       │
│       └── UserSeeder.php ────────────── Creates users
│
├── domain/
│   └── app/Policies/
│       ├── Traits/
│       │   └── MultiTenantAuthorizationTrait.php ── Model ownership
│       └── Extended/
│           └── TenantPolicy.php ── 3-tier tenant authorization
│
├── docs/
│   ├── MULTI_TENANT_POLICY_GUIDE.md ── Multi-tenant policy docs
│   └── TENANCY_ARCHITECTURE.md ─────── Tenancy architecture docs
│
└── ROLE_PERMISSION_SYSTEM.md ────────── Full documentation
```

## Permission Levels Explained

```
┌────────────────────────────────────────────────────────────┐
│              PERMISSION LEVEL HIERARCHY                    │
│                                                            │
│   Lower Number = Higher Authority                         │
│                                                            │
│   Level 0 (Highest) ───┐                                  │
│     • System Admin     │                                  │
│     • Can manage       │                                  │
│       everything       │                                  │
│     • Bypasses         │                                  │
│       AccessMiddleware │                                  │
│                        │                                  │
│   Level 1 ─────────────┤                                  │
│     • Tenancy Admin    │                                  │
│     • Multi-tenant     │                                  │
│       management       │                                  │
│                        │                                  │
│   Level 2 ─────────────┤                                  │
│     • Tenant Admin     │                                  │
│     • Can manage       │                                  │
│       Level 2+         │                                  │
│                        │                                  │
│   Level 3 (Lowest) ────┘                                  │
│     • Normal User                                         │
│     • Read-only                                           │
│       access                                              │
│                                                            │
│   Level 32767 (MAX)                                       │
│     • Reserved for                                        │
│       future use                                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Common Operations

```
╔════════════════════════════════════════════════════════════╗
║             PERMISSION CHECK EXAMPLES                      ║
╚════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────┐
│  User with "System" Role                                 │
│  Level: 0                                                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  AccessMiddleware: BYPASSED (System role check)          │
│  Can perform:                                            │
│    ✓ Create permissions                                 │
│    ✓ Manage all roles                                   │
│    ✓ Full tenant management                             │
│    ✓ Full user management                               │
│    ✓ Access trash operations                            │
│    ✓ All ecommerce, POS, logistics operations           │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  User with "TenancyAdmin" Role                           │
│  Level: 1                                                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  AccessMiddleware: Checked (same perms as Tenant)        │
│  Can perform:                                            │
│    ✗ Create permissions (Level 0 required)              │
│    ✗ Manage system roles (Level 0 required)             │
│    ✓ All business operations (ecommerce, POS, etc.)     │
│    ✓ Full user management                               │
│    ~ Multi-tenant management (via Policy layer)         │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  User with "Tenant" Role                                 │
│  Level: 2                                                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  AccessMiddleware: Checked (782 permissions)             │
│  Can perform:                                            │
│    ✗ Create permissions (Level 0 required)              │
│    ✗ Manage roles (Level 0 required)                    │
│    ~ View/Update tenants (limited)                      │
│    ✓ Full user management                               │
│    ✓ Full ecommerce, POS, tab operations                │
│    ✗ Trash operations (Level 0 required)                │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  User with "User" Role                                   │
│  Level: 3                                                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  AccessMiddleware: Checked (255 permissions)             │
│  Can perform:                                            │
│    ✗ Any permission operations                          │
│    ✗ Any role operations                                │
│    ✗ Any tenant operations                              │
│    ~ View/List most resources (read-only)               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Key Relationships

```
┌─────────┐         ┌─────────────┐         ┌────────────┐
│  User   │────────▶│  user_has   │◀────────│    Role    │
│         │  Many   │   _roles    │  Many   │            │
└─────────┘         └─────────────┘         └────────────┘
                                                   │
                                                   │
                                                   ▼
                                            ┌─────────────┐
                                            │  role_has   │
                                            │_permissions │
                                            └─────────────┘
                                                   │
                                                   │
                                                   ▼
                                            ┌────────────┐
                                            │ Permission │
                                            │            │
                                            └────────────┘
```

## Summary Statistics

```
╔══════════════════════════════════════════════════════════╗
║                    SYSTEM SUMMARY                        ║
║              (Updated: July 2025)                        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Total Roles:              4                             ║
║  Total Permissions:        777 (in systemPermissions)    ║
║  Total Permission Groups:  53                            ║
║                                                          ║
║  ┌────────────────────────────────────────────────────┐ ║
║  │ Role Distribution:                                 │ ║
║  │  • System Admin:    775 perms (bypasses middleware)│ ║
║  │  • TenancyAdmin:    782 perms (= Tenant, + TODO)  │ ║
║  │  • Tenant Admin:    782 perms (full business ops)  │ ║
║  │  • Normal User:     255 perms (read-mostly)       │ ║
║  └────────────────────────────────────────────────────┘ ║
║                                                          ║
║  ┌────────────────────────────────────────────────────┐ ║
║  │ Permission Groups (53 total):                      │ ║
║  │  Examples: permissions, roles, tenants, users,    │ ║
║  │  products, categories, orders, tabs, campaigns,   │ ║
║  │  logistics, media, malls, coupons, attributes...  │ ║
║  │  (See systemPermissions.json for full list)       │ ║
║  └────────────────────────────────────────────────────┘ ║
║                                                          ║
║  ┌────────────────────────────────────────────────────┐ ║
║  │ Authorization Layers:                              │ ║
║  │  Layer 1: AccessMiddleware (route permissions)    │ ║
║  │  Layer 2: Policies (model-level ownership)        │ ║
║  │  Both layers are additive and compatible.         │ ║
║  └────────────────────────────────────────────────────┘ ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```
