
# Role Permission System - Visual Overview

> **Last Updated:** June 2025 — Updated for 4-role hierarchy and current permission counts.

## System Architecture

```mermaid
flowchart TD
    subgraph DPS["DASH PERMISSION SYSTEM"]
        subgraph RH["ROLE HIERARCHY (4 Roles)"]
            L0["Level 0: System Admin<br/>(Full Access + Middleware Bypass)"] -- "can manage" --> L1["Level 1: Tenancy Admin<br/>(Multi-Tenant Mgmt)"]
            L1 -- "can manage" --> L2["Level 2: Tenant Admin<br/>(Business Operations)"]
            L2 -- "can manage" --> L3["Level 3: Normal User<br/>(Read Only)"]
        end
        subgraph PG["PERMISSION GROUPS (53 total)"]
            PG1["System (L0)<br/>8 groups"]
            PG2["Tenant (L1)<br/>3 groups"]
            PG3["Ecommerce (L2)<br/>28 groups"]
            PG4["Tabs (L2)<br/>3 groups"]
            PG5["Common (L2)<br/>4 groups"]
            PG6["App (L2)<br/>2 groups"]
            PG7["Other (L2)<br/>5 groups"]
        end
    end
```

## Permission Distribution

```mermaid
flowchart TD
    subgraph RPS["ROLE PERMISSION SUMMARY (4 Roles)"]
        A["System Admin (L0)<br/>775 perms<br/>Full access + AccessMiddleware bypass"]
        B["Tenancy Admin (L1)<br/>782 perms<br/>Multi-tenant mgmt (shares Tenant cfg)"]
        C["Tenant Admin (L2)<br/>782 perms<br/>Business operations, no sys admin"]
        D["Normal User (L3)<br/>255 perms<br/>Read-only across most resources"]
    end
```

Note: Tenancy Admin currently uses tenantAdminPermissions.json (same as
Tenant Admin). A dedicated tenancyAdminPermissions.json is a TODO.

Legend:
  L0-L3 = Role level (lower = higher authority)
```

## Data Flow

```mermaid
flowchart TD
    Start["SEEDING PROCESS"] --> A["1. PermissionSeeder.php<br/>- Loads systemPermissions.json<br/>- Loads domain/permissions.json<br/>- Inserts into permissions table<br/><br/>Output: 777+ permissions in database"]
    A --> B2
    subgraph B2["2. RoleSeeder.php"]
        B1["System Admin (Level 0)<br/>- Load: systemAdminPermissions.json<br/>- Assign: 775 permissions"]
        B3["Tenancy Admin (Level 1)<br/>- Load: tenantAdminPermissions.json<br/>- Assign: 782 permissions (shared)<br/>- TODO: tenancyAdminPermissions"]
        B4["Tenant Admin (Level 2)<br/>- Load: tenantAdminPermissions.json<br/>- Assign: 782 permissions"]
        B5["Normal User (Level 3)<br/>- Load: normalUserPermissions.json<br/>- Assign: 255 permissions"]
        B6["Output: 4 roles with permissions"]
    end
    B2 --> C["3. UserSeeder.php<br/>- Creates initial users<br/>- Assigns roles to users"]
```

## Request Authorization Flow

```mermaid
flowchart TD
    A["Incoming Request<br/>POST /api/users"] --> B["auth:sanctum<br/>(Authentication)"]
    B --> C["AccessMiddleware (Layer 1)<br/>1. System Admin?<br/>2. Has permission?<br/>3. Otherwise"]
    C -- "1. System Admin? Yes" --> P1["PASS (bypass)"]
    C -- "2. Has permission? Yes" --> P2["PASS"]
    C -- "3. Otherwise: No" --> E1["403"]
    P1 --> D["Policy Check (Layer 2, optional)<br/>MultiTenantAuth<br/>Trait ownership"]
    P2 --> D
    D -- "Allowed" --> F["Execute Controller Action"]
    D -- "Denied" --> G["Return 403 Error"]
```

Note: tenancy.* routes do NOT use AccessMiddleware (only auth:sanctum).
      public.* routes require no authentication at all.

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

```mermaid
flowchart TD
    Title["PERMISSION LEVEL HIERARCHY<br/>Lower Number = Higher Authority"]
    L0["Level 0 (Highest)<br/>- System Admin<br/>- Can manage everything<br/>- Bypasses AccessMiddleware"]
    L1["Level 1<br/>- Tenancy Admin<br/>- Multi-tenant management"]
    L2["Level 2<br/>- Tenant Admin<br/>- Can manage Level 2+"]
    L3["Level 3 (Lowest)<br/>- Normal User<br/>- Read-only access"]
    LMAX["Level 32767 (MAX)<br/>- Reserved for future use"]

    Title --> L0
    L0 --> L1
    L1 --> L2
    L2 --> L3
    L3 -.-> LMAX
```

## Common Operations

```mermaid
flowchart TD
    subgraph PCE["PERMISSION CHECK EXAMPLES"]
        A["User with 'System' Role (Level: 0)<br/>AccessMiddleware: BYPASSED (System role check)<br/>Can perform:<br/>✓ Create permissions<br/>✓ Manage all roles<br/>✓ Full tenant management<br/>✓ Full user management<br/>✓ Access trash operations<br/>✓ All ecommerce, POS, logistics operations"]
        B["User with 'TenancyAdmin' Role (Level: 1)<br/>AccessMiddleware: Checked (same perms as Tenant)<br/>Can perform:<br/>✗ Create permissions (Level 0 required)<br/>✗ Manage system roles (Level 0 required)<br/>✓ All business operations (ecommerce, POS, etc.)<br/>✓ Full user management<br/>~ Multi-tenant management (via Policy layer)"]
        C["User with 'Tenant' Role (Level: 2)<br/>AccessMiddleware: Checked (782 permissions)<br/>Can perform:<br/>✗ Create permissions (Level 0 required)<br/>✗ Manage roles (Level 0 required)<br/>~ View/Update tenants (limited)<br/>✓ Full user management<br/>✓ Full ecommerce, POS, tab operations<br/>✗ Trash operations (Level 0 required)"]
        D["User with 'User' Role (Level: 3)<br/>AccessMiddleware: Checked (255 permissions)<br/>Can perform:<br/>✗ Any permission operations<br/>✗ Any role operations<br/>✗ Any tenant operations<br/>~ View/List most resources (read-only)"]
    end
```

## Key Relationships

```mermaid
flowchart LR
    User["User"] -- "Many" --> UHR["user_has_roles"]
    Role["Role"] -- "Many" --> UHR
    UHR --> RHP["role_has_permissions"]
    RHP --> Permission["Permission"]
```

## Summary Statistics

```
╔══════════════════════════════════════════════════════════╗
║                    SYSTEM SUMMARY                        ║
║              (Updated: July 2025)                        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
```mermaid
flowchart TD
    subgraph SS["SYSTEM SUMMARY (Updated: July 2025)"]
        INFO1["Total Roles: 4<br/>Total Permissions: 777 (in systemPermissions)<br/>Total Permission Groups: 53"]
        RD["Role Distribution:<br/>- System Admin: 775 perms (bypasses middleware)<br/>- TenancyAdmin: 782 perms (= Tenant, + TODO)<br/>- Tenant Admin: 782 perms (full business ops)<br/>- Normal User: 255 perms (read-mostly)"]
        PG["Permission Groups (53 total):<br/>Examples: permissions, roles, tenants, users,<br/>products, categories, orders, tabs, campaigns,<br/>logistics, media, malls, coupons, attributes...<br/>(See systemPermissions.json for full list)"]
        AL["Authorization Layers:<br/>Layer 1: AccessMiddleware (route permissions)<br/>Layer 2: Policies (model-level ownership)<br/>Both layers are additive and compatible."]
    end
```
