
# Bulk Permission Manager - System Architecture Diagram

## High-Level Architecture

```mermaid
flowchart TD
    Title["<b>BULK PERMISSION MANAGER</b><br/>Full-Stack MVC Implementation"]
    
    subgraph Frontend["FRONTEND (React)"]
        RolePermissionBulkManager["RolePermissionBulkManager.tsx<br/>(810 lines)<br/><br/>Components:<br/>- Material UI Table DataGrid<br/>- Pagination Controls<br/>- Filter Toolbar Search Group Level Status<br/>- Sort Headers 6 sortable columns<br/>- Bulk Action Buttons<br/>- Statistics Dashboard<br/>- Floating Save Button<br/><br/>State Management:<br/>- useState permissions filters selected etc<br/>- useEffect data fetching sync<br/>- useCallback memoized handlers"]
        HTTPReq["HTTP Requests Axios"]
    end
    
    subgraph Backend["BACKEND Laravel"]
        APIRoutes["API Routes system.php<br/><br/>GET /role/{id}/permissions-bulk → getPermissions<br/>POST /role/{id}/permissions-bulk/update → bulkUpdate<br/>GET /role/{id}/permissions-bulk/stats → getStats"]
        BulkController["RolePermissionBulkController.php<br/>(398 lines)<br/><br/>Methods:<br/>- getPermissions: Pagination Filtering Sorting Auth<br/>- bulkUpdate: Validation Auth Transaction Bulk ops Cache<br/>- getStats: Aggregate Queries Per-group Percentages"]
        BulkRequest["RolePermissionBulkRequest.php<br/>(53 lines)<br/><br/>Validates:<br/>- permission_ids array required exists<br/>- action required in add,remove,set"]
        DBLayer["Database Layer Eloquent ORM<br/><br/>Models Used:<br/>- Role Spatie<br/>- Permission Spatie<br/>- RolePolicy Authorization"]
    end
    
    subgraph Database["DATABASE MySQL/PostgreSQL"]
        PermissionsTable["permissions<br/>---<br/>id PK<br/>name<br/>route_name<br/>group<br/>level<br/>guard_name<br/>is_active<br/>description"]
        PivotTable["role_has_permissions<br/>---<br/>role_id FK<br/>permission_id FK<br/>Pivot"]
        RolesTable["roles<br/>---<br/>id PK<br/>name<br/>level<br/>guard_name"]
    end
    
    Title --> Frontend
    RolePermissionBulkManager --> HTTPReq
    HTTPReq --> APIRoutes
    APIRoutes --> BulkController
    BulkController --> BulkRequest
    BulkRequest --> DBLayer
    DBLayer --> PermissionsTable
    DBLayer --> PivotTable
    DBLayer --> RolesTable
```

## Request Flow Diagram

```mermaid
flowchart TD
    Start["User Action: Enable Selected Permissions"]
    Step1["1. FRONTEND: User selects permissions<br/>State: selected = [1, 2, 3, 4, 5]"]
    Step2["2. FRONTEND: User clicks Enable Selected<br/>handleBulkToggle called<br/>Updates local state visual feedback<br/>setHasChanges true"]
    Step3["3. FRONTEND: User clicks Save Changes<br/>handleSave called<br/>Prepares API request"]
    Step4["4. HTTP REQUEST<br/>POST /api/system/role/1/permissions-bulk/update<br/>Headers: Authorization Bearer token<br/>Body: permission_ids [1,2,3,4,5] action add"]
    Step5["5. BACKEND: Request hits middleware<br/>Authentication check auth:sanctum<br/>Access control check<br/>Passes to controller"]
    Step6["6. BACKEND: RolePermissionBulkController::bulkUpdate<br/>Find role throws 404 if not found<br/>Authorize user policy check<br/>Validate request<br/>Verify permission levels<br/>Begin transaction<br/>- Query existing role_has_permissions<br/>- Calculate new permissions diff<br/>- INSERT new records<br/>- Clear permission cache<br/>Commit transaction"]
    Step7["7. HTTP RESPONSE<br/>Status: 200 OK<br/>Body: message action role_id affected_count"]
    Step8["8. FRONTEND: Handle success<br/>Show success notification<br/>Re-fetch permissions updated state<br/>Reset selected array<br/>setHasChanges false"]
    Step9["9. UI UPDATE<br/>Table shows updated permission states<br/>Green checkmarks appear<br/>Stats update if visible"]
    
    Start --> Step1 --> Step2 --> Step3 --> Step4 --> Step5 --> Step6 --> Step7 --> Step8 --> Step9
```

## Component Interaction Diagram

```mermaid
flowchart TD
    Root["RolePermissionBulkManager Component"]
    
    Root --> Filters["Filters Toolbar"]
    Root --> Table["Table Grid"]
    Root --> Stats["Statistics Dashboard"]
    
    Filters --> SearchField["Search Field"]
    Filters --> GroupSelect["Group Select"]
    Filters --> LevelSelect["Level Select"]
    Filters --> StatusSelect["Status Select"]
    
    Table --> Checkbox["Checkbox Column"]
    Table --> Enabled["Enabled Column"]
    Table --> Data["Data Columns"]
    Table --> Pagination["Pagination Controls"]
    
    Stats --> ProgressBars["Progress Bars"]
    Stats --> Metrics["Metrics Cards"]
    
    SearchField --> BulkActions["Bulk Actions Toolbar<br/>- Enable All<br/>- Disable All<br/>- Enable Sel<br/>- Disable Sel"]
    Checkbox --> BulkActions
    Pagination --> BulkActions
    
    BulkActions --> SaveBtn["Save Button Floating"]
```

## Data Flow Diagram

```mermaid
flowchart TD
    Title["Frontend State Management"]
    
    Init["Initial Load<br/>- roleId from URL params<br/>- page = 0<br/>- rowsPerPage = 25<br/>- filters = {search: '' group: '' level: '' ...}"]
    
    UseEffect["useEffect triggers fetchPermissions"]
    
    APICall["API Call<br/>GET /role/{id}/permissions-bulk?page=1&perPage=25"]
    
    Response["Response received"]
    
    StateUpdate["State Updates<br/>- permissions = response.data<br/>- total = response.meta.total<br/>- groups = response.filters.groups<br/>- levels = response.filters.levels<br/>- role = response.role<br/>- originalChecked = Set checked permission IDs"]
    
    UserInteract["User interactions"]
    
    UserActions["User Actions<br/>- Search → updates searchTerm → triggers re-fetch<br/>- Filter → updates filter state → triggers re-fetch<br/>- Sort → updates sort state → triggers re-fetch<br/>- Select → updates selected array → no fetch<br/>- Toggle → updates permission.checked → no fetch<br/>- Page change → updates page → triggers re-fetch"]
    
    ChangeDetect["Changes detected"]
    
    ChangeTrack["Change Tracking<br/>hasChanges = current checked ≠ originalChecked"]
    
    SaveClick["Save button clicked"]
    
    SaveOp["Save Operation<br/>- Calculate diff added removed<br/>- POST /role/{id}/permissions-bulk/update<br/>- Re-fetch permissions after success"]
    
    Title --> Init --> UseEffect --> APICall --> Response --> StateUpdate --> UserInteract --> UserActions --> ChangeDetect --> ChangeTrack --> SaveClick --> SaveOp
```

## Authorization Flow

```mermaid
flowchart TD
    Request["Request: POST /role/{id}/permissions-bulk/update"]
    
    Step1["1. Sanctum Middleware<br/>- Verify Bearer token<br/>- Load authenticated user"]
    
    Step2["2. Access Middleware<br/>- Check user has system access"]
    
    Step3["3. Controller: bulkUpdate"]
    
    Step4["4. Find Role<br/>Role::findOrFail id<br/>Throw 404 if not found"]
    
    Step5["5. Policy Check<br/>authorize manage role<br/>RolePolicy::manage<br/>- Check: user.level ≤ role.level<br/>- Deny if user level > role level"]
    
    Step6["6. Validate Request<br/>RolePermissionBulkRequest::validated<br/>- permission_ids: array required<br/>- action: in:add,remove,set"]
    
    Step7["7. Verify Permission Levels<br/>Check all permission_ids have level ≥ user.level<br/>Throw 403 if any permission above user level"]
    
    Step8["8. Proceed with Update<br/>Transaction + bulk operations"]
    
    Response["Response: 200 OK or 403 Forbidden or 404 Not Found"]
    
    Request --> Step1 --> Step2 --> Step3 --> Step4 --> Step5 --> Step6 --> Step7 --> Step8 --> Response
```

## Performance Optimization Strategies

```mermaid
flowchart TD
    Title["Performance Optimization Strategies"]
    
    subgraph Backend["Backend Optimizations"]
        DB["Database<br/>- Indexed columns: id group level route_name<br/>- Pagination LIMIT OFFSET<br/>- Eager loading prevented not needed<br/>- Bulk inserts single query multiple records"]
        Query["Query Optimization<br/>- Select only needed columns<br/>- Use whereIn for set membership checks<br/>- Aggregate queries for statistics<br/>- Avoid N+1 queries"]
        Cache["Caching<br/>- Permission cache cleared after update<br/>- Consider Redis for session cache<br/>- Filter options can be cached"]
        Trans["Transactions<br/>- Batch operations in single transaction"]
    end
    
    subgraph Frontend["Frontend Optimizations"]
        React["React Performance<br/>- useCallback for memoized functions<br/>- Prevent unnecessary re-renders<br/>- Lazy loading for statistics<br/>- Controlled re-fetches"]
        Data["Data Handling<br/>- Paginated loading not all data at once<br/>- Client-side state for quick toggles<br/>- Batch saves not individual requests<br/>- Optimistic UI updates"]
        Network["Network<br/>- Axios for efficient HTTP<br/>- Bearer token auth no cookies<br/>- Compressed responses if enabled"]
    end
    
    Title --> Backend
    Title --> Frontend
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
