# Bulk Permission Manager - System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         BULK PERMISSION MANAGER                         │
│                    Full-Stack MVC Implementation                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │         RolePermissionBulkManager.tsx (810 lines)             │    │
│  │                                                               │    │
│  │  Components:                                                  │    │
│  │  ├─ Material UI Table (DataGrid)                             │    │
│  │  ├─ Pagination Controls                                      │    │
│  │  ├─ Filter Toolbar (Search, Group, Level, Status)            │    │
│  │  ├─ Sort Headers (6 sortable columns)                        │    │
│  │  ├─ Bulk Action Buttons                                      │    │
│  │  ├─ Statistics Dashboard                                     │    │
│  │  └─ Floating Save Button                                     │    │
│  │                                                               │    │
│  │  State Management:                                            │    │
│  │  ├─ useState (permissions, filters, selected, etc.)          │    │
│  │  ├─ useEffect (data fetching, sync)                          │    │
│  │  └─ useCallback (memoized handlers)                          │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                              ↓ ↑                                        │
│                        HTTP Requests (Axios)                            │
│                              ↓ ↑                                        │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓ ↑
                          REST API Calls
                               ↓ ↑
┌─────────────────────────────────────────────────────────────────────────┐
│                            BACKEND (Laravel)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                    API Routes (system.php)                    │    │
│  │                                                               │    │
│  │  GET  /role/{id}/permissions-bulk          → getPermissions  │    │
│  │  POST /role/{id}/permissions-bulk/update   → bulkUpdate      │    │
│  │  GET  /role/{id}/permissions-bulk/stats    → getStats        │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                              ↓                                          │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │      RolePermissionBulkController.php (398 lines)            │    │
│  │                                                               │    │
│  │  Methods:                                                     │    │
│  │  ├─ getPermissions($roleId)                                  │    │
│  │  │   ├─ Pagination                                           │    │
│  │  │   ├─ Filtering (search, group, level, checked)           │    │
│  │  │   ├─ Sorting                                              │    │
│  │  │   └─ Authorization check                                  │    │
│  │  │                                                            │    │
│  │  ├─ bulkUpdate($roleId)                                      │    │
│  │  │   ├─ Validation (RolePermissionBulkRequest)              │    │
│  │  │   ├─ Authorization check                                  │    │
│  │  │   ├─ Database transaction                                 │    │
│  │  │   ├─ Bulk operations (add/remove/set)                    │    │
│  │  │   └─ Cache clearing                                       │    │
│  │  │                                                            │    │
│  │  └─ getStats($roleId)                                        │    │
│  │      ├─ Aggregate queries                                    │    │
│  │      ├─ Per-group statistics                                 │    │
│  │      └─ Percentage calculations                              │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                              ↓                                          │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │        RolePermissionBulkRequest.php (53 lines)              │    │
│  │                                                               │    │
│  │  Validates:                                                   │    │
│  │  ├─ permission_ids (array, required, exists)                 │    │
│  │  └─ action (required, in:add,remove,set)                     │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                              ↓                                          │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │              Database Layer (Eloquent ORM)                    │    │
│  │                                                               │    │
│  │  Models Used:                                                 │    │
│  │  ├─ Role (Spatie)                                            │    │
│  │  ├─ Permission (Spatie)                                      │    │
│  │  └─ RolePolicy (Authorization)                               │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                              ↓                                          │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATABASE (MySQL/PostgreSQL)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────┐  │
│  │   permissions       │  │ role_has_permissions│  │    roles     │  │
│  ├─────────────────────┤  ├─────────────────────┤  ├──────────────┤  │
│  │ id (PK)             │  │ role_id (FK)        │  │ id (PK)      │  │
│  │ name                │  │ permission_id (FK)  │  │ name         │  │
│  │ route_name          │  └─────────────────────┘  │ level        │  │
│  │ group               │           (Pivot)         │ guard_name   │  │
│  │ level               │                            └──────────────┘  │
│  │ guard_name          │                                              │
│  │ is_active           │                                              │
│  │ description         │                                              │
│  └─────────────────────┘                                              │
└─────────────────────────────────────────────────────────────────────────┘
```

## Request Flow Diagram

```
User Action: "Enable Selected Permissions"
│
├─ 1. FRONTEND: User selects permissions (checkboxes)
│   └─ State: selected = [1, 2, 3, 4, 5]
│
├─ 2. FRONTEND: User clicks "Enable Selected"
│   └─ handleBulkToggle(true) called
│   └─ Updates local state (visual feedback)
│   └─ setHasChanges(true)
│
├─ 3. FRONTEND: User clicks "Save Changes"
│   └─ handleSave() called
│   └─ Prepares API request
│
├─ 4. HTTP REQUEST
│   POST /api/system/role/1/permissions-bulk/update
│   Headers: { Authorization: "Bearer {token}" }
│   Body: {
│     permission_ids: [1, 2, 3, 4, 5],
│     action: "add"
│   }
│
├─ 5. BACKEND: Request hits middleware
│   ├─ Authentication check (auth:sanctum)
│   ├─ Access control check
│   └─ Passes to controller
│
├─ 6. BACKEND: RolePermissionBulkController::bulkUpdate()
│   ├─ Find role (throws 404 if not found)
│   ├─ Authorize user (policy check)
│   ├─ Validate request (RolePermissionBulkRequest)
│   ├─ Verify permission levels
│   │
│   ├─ Begin transaction
│   │   ├─ Query existing role_has_permissions
│   │   ├─ Calculate new permissions (diff)
│   │   ├─ INSERT new records
│   │   └─ Clear permission cache
│   └─ Commit transaction
│
├─ 7. HTTP RESPONSE
│   Status: 200 OK
│   Body: {
│     message: "5 permission(s) added successfully",
│     data: {
│       role_id: 1,
│       action: "add",
│       affected_count: 5
│     }
│   }
│
├─ 8. FRONTEND: Handle success
│   ├─ Show success notification
│   ├─ Re-fetch permissions (updated state)
│   ├─ Reset selected array
│   └─ setHasChanges(false)
│
└─ 9. UI UPDATE
    └─ Table shows updated permission states
    └─ Green checkmarks appear
    └─ Stats update (if visible)
```

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│              RolePermissionBulkManager Component                │
└─────────────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Filters   │  │   Table     │  │  Statistics │
│   Toolbar   │  │   Grid      │  │  Dashboard  │
└─────────────┘  └─────────────┘  └─────────────┘
    │                   │                 │
    │ ┌─────────────────┤                 │
    │ │                 │                 │
    ▼ ▼                 ▼                 ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Search    │  │  Checkbox   │  │  Progress   │
│   Field     │  │  Column     │  │   Bars      │
├─────────────┤  ├─────────────┤  ├─────────────┤
│   Group     │  │  Enabled    │  │  Metrics    │
│   Select    │  │  Column     │  │   Cards     │
├─────────────┤  ├─────────────┤  └─────────────┘
│   Level     │  │  Data       │
│   Select    │  │  Columns    │
├─────────────┤  ├─────────────┤
│   Status    │  │  Pagination │
│   Select    │  │  Controls   │
└─────────────┘  └─────────────┘
         │                │
         └────────┬───────┘
                  ▼
         ┌─────────────────┐
         │  Bulk Actions   │
         │    Toolbar      │
         ├─────────────────┤
         │ - Enable All    │
         │ - Disable All   │
         │ - Enable Sel    │
         │ - Disable Sel   │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  Save Button    │
         │   (Floating)    │
         └─────────────────┘
```

## Data Flow Diagram

```
Frontend State Management
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  Initial Load                                                │
│  ├─ roleId (from URL params)                                │
│  ├─ page = 0                                                 │
│  ├─ rowsPerPage = 25                                         │
│  └─ filters = { search: '', group: '', level: '', ... }     │
│                                                              │
│  ↓ useEffect triggers fetchPermissions()                     │
│                                                              │
│  API Call                                                    │
│  └─ GET /role/{id}/permissions-bulk?page=1&perPage=25       │
│                                                              │
│  ↓ Response received                                         │
│                                                              │
│  State Updates                                               │
│  ├─ permissions = response.data                             │
│  ├─ total = response.meta.total                             │
│  ├─ groups = response.filters.groups                        │
│  ├─ levels = response.filters.levels                        │
│  ├─ role = response.role                                    │
│  └─ originalChecked = Set(checked permission IDs)           │
│                                                              │
│  ↓ User interactions                                         │
│                                                              │
│  User Actions                                                │
│  ├─ Search → updates searchTerm → triggers re-fetch         │
│  ├─ Filter → updates filter state → triggers re-fetch       │
│  ├─ Sort → updates sort state → triggers re-fetch           │
│  ├─ Select → updates selected array → no fetch              │
│  ├─ Toggle → updates permission.checked → no fetch          │
│  └─ Page change → updates page → triggers re-fetch          │
│                                                              │
│  ↓ Changes detected                                          │
│                                                              │
│  Change Tracking                                             │
│  └─ hasChanges = (current checked ≠ originalChecked)        │
│                                                              │
│  ↓ Save button clicked                                       │
│                                                              │
│  Save Operation                                              │
│  ├─ Calculate diff (added, removed)                         │
│  ├─ POST /role/{id}/permissions-bulk/update                 │
│  └─ Re-fetch permissions after success                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Authorization Flow

```
Request: POST /role/{id}/permissions-bulk/update
│
├─ 1. Sanctum Middleware
│   └─ Verify Bearer token
│   └─ Load authenticated user
│
├─ 2. Access Middleware
│   └─ Check user has system access
│
├─ 3. Controller: bulkUpdate()
│   │
│   ├─ 4. Find Role
│   │   └─ Role::findOrFail($id)
│   │       └─ Throw 404 if not found
│   │
│   ├─ 5. Policy Check
│   │   └─ $this->authorize('manage', $role)
│   │       └─ RolePolicy::manage()
│   │           ├─ Check: user.level <= role.level
│   │           └─ Deny if user level > role level
│   │
│   ├─ 6. Validate Request
│   │   └─ RolePermissionBulkRequest::validated()
│   │       ├─ permission_ids: array, required
│   │       └─ action: in:add,remove,set
│   │
│   ├─ 7. Verify Permission Levels
│   │   └─ Check all permission_ids have level >= user.level
│   │       └─ Throw 403 if any permission is above user level
│   │
│   └─ 8. Proceed with Update
│       └─ Transaction + bulk operations
│
└─ Response: 200 OK or 403 Forbidden or 404 Not Found
```

## Performance Optimization Strategies

```
Backend Optimizations
├─ Database
│   ├─ Indexed columns: id, group, level, route_name
│   ├─ Pagination (LIMIT + OFFSET)
│   ├─ Eager loading prevented (not needed)
│   └─ Bulk inserts (single query for multiple records)
│
├─ Query Optimization
│   ├─ Select only needed columns
│   ├─ Use whereIn for set membership checks
│   ├─ Aggregate queries for statistics
│   └─ Avoid N+1 queries
│
├─ Caching
│   ├─ Permission cache cleared after update
│   ├─ Consider Redis for session/cache
│   └─ Filter options can be cached
│
└─ Transactions
    └─ Batch operations in single transaction

Frontend Optimizations
├─ React Performance
│   ├─ useCallback for memoized functions
│   ├─ Prevent unnecessary re-renders
│   ├─ Lazy loading for statistics
│   └─ Controlled re-fetches
│
├─ Data Handling
│   ├─ Paginated loading (not all data at once)
│   ├─ Client-side state for quick toggles
│   ├─ Batch saves (not individual requests)
│   └─ Optimistic UI updates
│
└─ Network
    ├─ Axios for efficient HTTP
    ├─ Bearer token auth (no cookies)
    └─ Compressed responses (if enabled)
```

## Error Handling Flow

```
Error Scenarios
│
├─ Backend Errors
│   ├─ 404 Not Found
│   │   └─ Role doesn't exist
│   │       └─ Return JSON error message
│   │
│   ├─ 403 Forbidden
│   │   ├─ User unauthorized for role
│   │   └─ Permission level too high
│   │       └─ Return JSON error message
│   │
│   ├─ 422 Validation Error
│   │   └─ Invalid request data
│   │       └─ Return validation errors
│   │
│   └─ 500 Server Error
│       ├─ Database connection failed
│       ├─ Transaction error
│       └─ Unexpected exception
│           └─ Log to Laravel log
│           └─ Return generic error (production)
│
└─ Frontend Handling
    ├─ Axios interceptor catches errors
    ├─ Display notification (react-admin notify)
    ├─ Log to console (development)
    └─ Restore previous state (if needed)
```

This architecture provides a robust, scalable, and maintainable solution for managing thousands of permissions efficiently.
