# DASH Role & Permission System Overview

## Purpose

The DASH Role & Permission system enforces hierarchical access control across the Laravel-based backend that powers Dash-Admin. It orchestrates how roles, permissions, and policies interact to secure REST resources while keeping the configuration maintainable and extensible for multi-tenant scenarios.

## Hierarchical Component Map

```
DASH RBAC Stack
└── Laravel Application (dash-backend)
    ├── Spatie Permission Package
    │   ├── Role Model Extension (app/Models/Role.php)
    │   └── Permission Model Extension (app/Models/Permission.php)
    ├── Configuration Layer
    │   ├── Permission Catalog      (database/data/systemPermissions.json)
    │   └── Role Permission Profiles (database/data/rolePermissions/*.json)
    ├── Seeding & Validation
    │   ├── PermissionSeeder        (database/seeders/PermissionSeeder.php)
    │   ├── RoleSeeder              (database/seeders/RoleSeeder.php)
    │   └── validate:role-permissions artisan command
    ├── HTTP Surface
    │   ├── RoleController          (app/Http/Controllers/API/System/RoleController.php)
    │   ├── PermissionController    (app/Http/Controllers/API/System/PermissionController.php)
    │   └── ReactAdminBaseController (shared CRUD behaviours)
    ├── Middleware & Traits
    │   ├── AccessMiddleware        (app/Http/Middleware/AccessMiddleware.php)
    │   └── ReactAdminBasePermissionCheckTrait
    └── Policies & Jobs
        ├── RolePolicy              (app/Policies/RolePolicy.php)
        └── SyncRolePermissionsJob  (app/Jobs/SyncRolePermissionsJob.php)
```

Each layer depends on the preceding one; configuration feeds the seeding logic, which primes the database that controllers and middleware query at runtime.

## Key Characteristics

- **Level-Based Hierarchy** – Roles carry numeric `level` values (`Role::LEVEL_SYSTEM_ADMIN`, `Role::LEVEL_TENANT_ADMIN`, `Role::LEVEL_NORMAL_USER`) that gate which permissions they can manage and which targets they can operate on.
- **Route-Centric Permissions** – Every permission aligns with an API route name following `api.{context}.{resource}.{action}`, giving one-to-one parity with ReactAdmin operations.
- **Seed-Driven Bootstrap** – JSON configuration files define both the global permission catalog (`systemPermissions.json`) and the default role assignments stored under `database/data/rolePermissions/`. Seeders translate those definitions into database state.
- **Policy Enforcement** – `RolePolicy` relies on role levels to prevent privilege escalation, while controllers invoke `authorize()` to gate sensitive operations.
- **Middleware Guarding** – `AccessMiddleware` intercepts API requests, resolves the route name, and ensures the authenticated user either has the System role or an explicit permission matching the route.
- **Extensible Sync Job** – `SyncRolePermissionsJob` batches large permission updates, ensuring consistency during complex assignments triggered through the admin UI.

## Runtime Workflow

1. **Authentication** – Users authenticate via Sanctum; their roles and permissions are auto-loaded thanks to Spatie's relationships.
2. **Request Entry** – Requests pass through `AccessMiddleware`, which checks for the required permission based on the route name.
3. **Controller Execution** – Controllers extend `ReactAdminBaseController`, inheriting list/show/create/update/delete scaffolding while invoking `permissionCheck()` for fine-grained validation.
4. **Policy Evaluation** – For role-specific actions, `RolePolicy` enforces level constraints (`manage`, `update`, etc.).
5. **Response Serialization** – Data is returned through Laravel API Resources (`RoleResource`, `PermissionResource`) to ensure consistent payloads for Dash-Admin.

## Configuration & Data Sources

- **Permission Catalog** (`database/data/systemPermissions.json`)
  - Defines groups, human-readable labels, route names, and minimum levels.
  - Consumed by `PermissionSeeder` to populate `permissions` table.
- **Role Profiles** (`database/data/rolePermissions/*.json`)
  - Map roles (System, Tenant, User) to arrays of route names.
  - Consumed by `RoleSeeder` to sync permissions to roles.
- **Validation Command** (`php artisan validate:role-permissions`)
  - Uses Laravel console infrastructure to parse JSON, ensure schema compliance, and verify presence of each permission record.

## Deployment & Maintenance

- **Initial Setup** – Run `php artisan migrate --seed` (or Sail equivalent) to seed both permissions and roles from JSON definitions.
- **Updating Permissions**
  1. Modify `systemPermissions.json` and/or role profile files.
  2. Execute `php artisan validate:role-permissions` to catch mismatches.
  3. Rerun `php artisan db:seed --class=PermissionSeeder` and `RoleSeeder` as needed.
- **Cache Management** – Clear the Spatie cache (`php artisan cache:clear`) whenever permissions change to avoid stale guard data.

## Dependency Overview

- **Laravel Framework** – Provides routing, middleware, policies, queues, and database abstractions underpinning the system.
- **Spatie/laravel-permission** – Supplies trait-based role/permission relationships, caching, and helper APIs (`hasRole`, `hasPermissionTo`). The project extends Spatie models to add level metadata, factories, and domain-specific behaviours.
- **ReactAdmin Convention** – Not a code dependency but a structural one: permission naming mirrors ReactAdmin data provider actions, ensuring the frontend can request the correct endpoints and interpret authorization failures.

## Extension Points

- **Custom Roles** – Add new JSON profile files and update `RoleSeeder` to create/sync the role.
- **Domain-Specific Permissions** – Place additional permission definitions under `domain/database/data/permissions.json`; `PermissionSeeder` automatically merges them during seeding.
- **UI Integration Hooks** – Controllers expose `getForSelect`, `getMany`, and other ReactAdmin-compatible methods, making frontend permission editors straightforward to implement.

## Related Documentation

- `ROLE_PERMISSION_SYSTEM.md` – Deep dive into architecture and operational procedures.
- `ROLE_PERMISSION_IMPLEMENTATION.md` – Implementation history and rationale.
- `ROLE_PERMISSION_QUICK_REFERENCE.md` – Task-oriented cheat sheet with commands and troubleshooting tips.
