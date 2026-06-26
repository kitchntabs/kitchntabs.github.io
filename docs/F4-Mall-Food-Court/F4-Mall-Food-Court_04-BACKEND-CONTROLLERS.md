---
title: Mall App - Backend Controllers
layout: default
nav_order: 4
parent: Mall Application
---

# Mall App - Backend Controllers

## Overview

Mall controllers are located in `domain/app/Http/Controllers/API/Mall/` and handle different aspects of the mall ordering system.

## Controllers

### 1. MallSessionController

**File Path:** `domain/app/Http/Controllers/API/Mall/MallSession/MallSessionController.php`

**Purpose:** Core session management - creation, validation, lifecycle, and notifications.

#### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/session/create` | Create new session |
| GET | `/session/{hash}` | Get session details |
| PUT | `/session/{hash}` | Update session |
| POST | `/session/{hash}/complete` | Mark completed |
| POST | `/session/{hash}/cancel` | Cancel session |
| POST | `/session/validate-hash` | Check hash availability |
| GET | `/session/mall/{mallId}/sessions` | List sessions for mall |
| GET | `/{hash}/getSessionAuth` | **Key** - Authenticate client |
| GET | `/session/{hash}/notifications` | Get notifications |
| POST | `/session/{hash}/notifications/mark-read` | Mark read |

#### Key Methods

##### `createSession(Request $request)`

Creates a new session for a mall.

```php
public function createSession(Request $request)
{
    $validated = $request->validate([
        'mall_id' => 'required|exists:malls,id',
        'customer_name' => 'nullable|string|max:255',
        'mall_location' => 'nullable|string|max:255',
    ]);

    $session = MallSession::create([
        'mall_id' => $validated['mall_id'],
        'customer_name' => $validated['customer_name'] ?? null,
        'mall_location' => $validated['mall_location'] ?? null,
        'status' => MallSession::STATUS_PENDING,
    ]);

    return response()->json([
        'hash' => $session->hash,
        'session' => new MallSessionResource($session),
    ], 201);
}
```

##### `getSessionAuth(string $hash)`

**Critical method** - Authenticates a client accessing a session.

```php
public function getSessionAuth(string $hash)
{
    $session = MallSession::where('hash', $hash)->firstOrFail();
    
    // If pending, activate the session
    if ($session->isPending()) {
        $session->update([
            'status' => MallSession::STATUS_ACTIVE,
            'meta' => [
                'activated_at' => now()->toIso8601String(),
                'client_ip' => request()->ip(),
                'user_agent' => request()->userAgent(),
            ],
        ]);
        
        // Notify manager tenant about session activation
        $this->notifySessionActivation($session);
    }
    
    // If active, validate client identity
    if ($session->isActive()) {
        // Check expiration (6 hours)
        $activatedAt = Carbon::parse($session->meta['activated_at'] ?? $session->created_at);
        if ($activatedAt->diffInHours(now()) >= 6) {
            $session->markAsCompleted();
            return response()->json(['error' => 'Session expired'], 410);
        }
        
        // Validate IP or User-Agent matches
        $storedIp = $session->meta['client_ip'] ?? null;
        $storedAgent = $session->meta['user_agent'] ?? null;
        $currentIp = request()->ip();
        $currentAgent = request()->userAgent();
        
        if ($storedIp !== $currentIp && $storedAgent !== $currentAgent) {
            Log::warning('Session access from different client', [
                'hash' => $hash,
                'stored_ip' => $storedIp,
                'current_ip' => $currentIp,
            ]);
            // Allow but log suspicious access
        }
    }
    
    // Build auth response
    return $this->buildAuthResponse($session);
}
```

##### `getNotifications(string $hash, Request $request)`

Retrieves notifications for a session with filtering.

```php
public function getNotifications(string $hash, Request $request)
{
    $session = MallSession::where('hash', $hash)->firstOrFail();
    
    $query = $session->notifications()
        ->orderBy('created_at', 'desc');
    
    // Filters
    if ($request->has('type')) {
        $query->where('type', $request->type);
    }
    if ($request->has('is_read')) {
        $query->where('is_read', $request->boolean('is_read'));
    }
    if ($request->has('tenant_id')) {
        $query->where('tenant_id', $request->tenant_id);
    }
    if ($request->has('since')) {
        $query->where('created_at', '>=', $request->since);
    }
    
    $notifications = $query->limit(50)->get();
    
    return response()->json([
        'notifications' => MallSessionNotificationResource::collection($notifications),
        'unread_count' => $session->unreadNotifications()->count(),
        'total_count' => $session->notifications()->count(),
    ]);
}
```

##### `markNotificationsAsRead(string $hash, Request $request)`

Marks notifications as read (bulk or specific IDs).

```php
public function markNotificationsAsRead(string $hash, Request $request)
{
    $session = MallSession::where('hash', $hash)->firstOrFail();
    
    if ($request->has('notification_ids')) {
        // Mark specific notifications
        $session->notifications()
            ->whereIn('id', $request->notification_ids)
            ->update(['is_read' => true]);
    } else {
        // Mark all as read
        $session->unreadNotifications()->update(['is_read' => true]);
    }
    
    return response()->json(['success' => true]);
}
```

---

### 2. MallTabsController

**File Path:** `domain/app/Http/Controllers/API/Mall/MallTabs/MallTabsController.php`

**Purpose:** Handle mall orders (tabs) - extends base TabController with mall-specific logic.

#### Uses Traits

- `MallTabCrudOperationsTrait` - Create/update operations
- `MallTabNotificationsTrait` - Notification sending
- `MallTabHelpersTrait` - Helper methods

#### Key Methods

##### `_create(Request $request)` (from Trait)

Creates master tab and tenant tabs for a mall order.

```php
protected function _create(Request $request)
{
    // 1. Validate request
    $validated = $this->validateMallOrderRequest($request);
    
    // 2. Get MallSession and update customer info
    $mallSession = MallSession::where('hash', $validated['mall_session'])->firstOrFail();
    $mallSession->update([
        'customer_name' => $validated['customer_name'],
        'mall_location' => $validated['table_number'],
    ]);
    
    // 3. Group products by tenant
    $productsByTenant = $this->groupProductsByTenant($validated['products']);
    
    // 4. Create master tab under manager tenant
    $masterTab = $this->createMasterTab(
        $mallSession,
        $validated,
        $productsByTenant
    );
    
    // 5. Create tenant tabs for each tenant
    foreach ($productsByTenant as $tenantId => $products) {
        $tenantTab = $this->createTenantTab(
            $masterTab,
            $tenantId,
            $products,
            $validated
        );
        
        // 6. Notify tenant of new order
        $this->notifyTenantOfNewOrder($tenantTab);
    }
    
    // 7. Send urgent notification to manager
    $this->notifyManagerOfNewOrder($masterTab);
    
    return new TabResource($masterTab->load(['order.items', 'tenantTabs']));
}
```

##### `createMasterTab()` (from Trait)

```php
protected function createMasterTab(
    MallSession $session,
    array $validated,
    array $productsByTenant
): Tab
{
    $mall = $session->mall;
    $managerTenant = $mall->managerTenant;
    
    // Create master tab
    $masterTab = Tab::create([
        'tenant_id' => $managerTenant->id,
        'status' => Tab::STATUS_CREATED,
        'delivery_method' => 'TABLE',
        'note' => $this->buildCustomerNote($validated),
        'is_master_tab' => true,
        'brokerable_type' => MallSession::class,
        'brokerable_id' => $session->id,
    ]);
    
    // Create master order with ALL products
    $allProducts = collect($productsByTenant)->flatten(1);
    $order = $this->createOrderForTab($masterTab, $allProducts, $session);
    
    return $masterTab;
}
```

##### `createTenantTab()` (from Trait)

```php
protected function createTenantTab(
    Tab $masterTab,
    int $tenantId,
    array $products,
    array $validated
): Tab
{
    // Create tenant tab linked to master
    $tenantTab = Tab::create([
        'tenant_id' => $tenantId,
        'status' => Tab::STATUS_CREATED,
        'delivery_method' => 'TABLE',
        'note' => $this->buildCustomerNote($validated),
        'master_tab_id' => $masterTab->id,
        'is_master_tab' => false,
        'brokerable_type' => MallSession::class,
        'brokerable_id' => $masterTab->brokerable_id,
    ]);
    
    // Create tenant order linked to master order
    $order = $this->createOrderForTab(
        $tenantTab, 
        $products, 
        $masterTab->brokerable,
        $masterTab->order  // Parent order
    );
    
    return $tenantTab;
}
```

##### `updateTenantTabStatus()`

Updates a tenant tab status and syncs with master.

```php
public function updateTenantTabStatus(int $tabId, Request $request)
{
    $validated = $request->validate([
        'status' => 'required|in:' . implode(',', Tab::STATUSES),
    ]);
    
    $tenantTab = Tab::findOrFail($tabId);
    $oldStatus = $tenantTab->status;
    $newStatus = $validated['status'];
    
    // Update tenant tab
    $tenantTab->update([
        'status' => $newStatus,
        "date_{$this->statusToDateField($newStatus)}" => now(),
    ]);
    
    // Sync with master tab
    if ($tenantTab->master_tab_id) {
        app(MallOrderSyncService::class)
            ->syncTenantTabStatusWithMaster($tenantTab);
    }
    
    return new TabResource($tenantTab);
}
```

---

### 3. MallStoresController

**File Path:** `domain/app/Http/Controllers/API/Mall/MallStores/MallStoresController.php`

**Purpose:** Public store listing and assistance requests.

#### Key Methods

##### `_preList()`

Filter and eager load stores for a mall.

```php
protected function _preList()
{
    $mallId = request('mall_id');
    
    if ($mallId) {
        $this->model = $this->model
            ->whereHas('malls', function ($q) use ($mallId) {
                $q->where('malls.id', $mallId)
                  ->where('mall_tenant.is_active', true);
            })
            ->with(['media', 'products' => function ($q) {
                $q->where('is_active', true)
                  ->with('media');
            }]);
    }
}
```

##### `assistance(int $storeId, Request $request)`

Handle staff assistance requests.

```php
public function assistance(int $storeId, Request $request)
{
    $validated = $request->validate([
        'mall_session' => 'required|string|size:5',
    ]);
    
    $session = MallSession::where('hash', $validated['mall_session'])->firstOrFail();
    $store = Tenant::findOrFail($storeId);
    
    // Check session is active
    if (!$session->isActive()) {
        return response()->json(['error' => 'Session not active'], 400);
    }
    
    // Check rate limit (max 2 per store per session)
    $requests = $session->assistance_requests ?? [];
    $storeRequests = $requests[$storeId] ?? 0;
    
    if ($storeRequests >= self::MAX_ASSISTANCE_REQUESTS_PER_SESSION) {
        return response()->json([
            'error' => 'Maximum assistance requests reached for this store'
        ], 429);
    }
    
    // Update request count
    $requests[$storeId] = $storeRequests + 1;
    $session->update(['assistance_requests' => $requests]);
    
    // Send push notification to store staff
    AppNotificationBuilder::send(
        notificationClass: MallStoreAssistanceNotification::class,
        data: [
            'session_hash' => $session->hash,
            'customer_name' => $session->customer_name,
            'table_number' => $session->mall_location,
            'store_id' => $storeId,
            'store_name' => $store->name,
        ],
        channel: "tenant.{$storeId}.system",
        scope: "channel",
        targets: ['staff', 'admin'],
        targetType: "role",
        individual: ["push"],
    );
    
    return response()->json([
        'success' => true,
        'remaining_requests' => self::MAX_ASSISTANCE_REQUESTS_PER_SESSION - $requests[$storeId],
    ]);
}
```

---

### 4. PublicMallController

**File Path:** `domain/app/Http/Controllers/API/Mall/PublicMallController.php`

**Purpose:** Public endpoints for mall access without authentication.

#### Key Methods

##### `getAuth(string $slug)`

Get mall auth data by slug (no session required).

```php
public function getAuth(string $slug)
{
    $mall = Mall::where('slug', $slug)
        ->where('is_active', true)
        ->with(['managerTenant', 'activeTenants'])
        ->firstOrFail();
    
    return $this->buildAuthResponse($mall);
}
```

---

### 5. SystemMallSessionController

**File Path:** `domain/app/Http/Controllers/API/Mall/SystemMallSessionController.php`

**Purpose:** Admin CRUD for MallSession (ReactAdmin compatible).

#### Key Methods

##### `mallStatistics(int $mallId)`

Get session counts by status.

```php
public function mallStatistics(int $mallId)
{
    $stats = MallSession::where('mall_id', $mallId)
        ->selectRaw('status, COUNT(*) as count')
        ->groupBy('status')
        ->pluck('count', 'status');
    
    return response()->json([
        'pending' => $stats['pending'] ?? 0,
        'active' => $stats['active'] ?? 0,
        'completed' => $stats['completed'] ?? 0,
        'cancelled' => $stats['cancelled'] ?? 0,
        'total' => array_sum($stats->toArray()),
    ]);
}
```

##### `generateNextHash(int $mallId)`

Generate QR code data for new session.

```php
public function generateNextHash(int $mallId)
{
    $hash = MallSession::generateNextHash();
    
    $session = MallSession::create([
        'mall_id' => $mallId,
        'hash' => $hash,
        'status' => MallSession::STATUS_PENDING,
    ]);
    
    return response()->json([
        'hash' => $hash,
        'qr_url' => config('app.frontend_url') . "/mall/session/{$hash}",
        'session_id' => $session->id,
    ]);
}
```

---

## Controller Traits

### MallTabCrudOperationsTrait

**File Path:** `domain/app/Http/Controllers/API/Mall/MallTabs/MallTabCrudOperationsTrait.php`

**Key Methods:**
- `validateMallOrderRequest()` - Validate order payload
- `groupProductsByTenant()` - Split products by tenant
- `createMasterTab()` - Create master tab under manager
- `createTenantTab()` - Create individual tenant tabs

### MallTabNotificationsTrait

**File Path:** `domain/app/Http/Controllers/API/Mall/MallTabs/MallTabNotificationsTrait.php`

**Key Methods:**
- `notifyMallSessionOnConfirmation()` - Send confirmation notification
- `notifyMallSessionProductStatus()` - Send status update
- `logMallSessionOrderCreated()` - Debug logging

### MallTabHelpersTrait

**File Path:** `domain/app/Http/Controllers/API/Mall/MallTabs/MallTabHelpersTrait.php`

**Key Methods:**
- `buildCustomerNote()` - Format customer info for notes
- Helper methods for tab/order creation

### MallAuthResponseTrait

**File Path:** `domain/app/Http/Controllers/API/Mall/MallAuthResponseTrait.php`

**Purpose:** Build standardized auth response for mall clients.

```php
protected function buildAuthResponse($mallOrSession)
{
    $mall = $mallOrSession instanceof MallSession 
        ? $mallOrSession->mall 
        : $mallOrSession;
    
    $managerTenant = $mall->managerTenant;
    
    return response()->json([
        'tenant' => new TenantResource($managerTenant),
        'auth' => [
            'tenant_id' => $managerTenant->id,
            'tenant_name' => $managerTenant->name,
            'settings' => $managerTenant->settings,
            'images' => $managerTenant->images,
        ],
        'systemValues' => [
            'pos' => $managerTenant->pointOfSales ?? [],
            'mall' => new MallResource($mall),
            'tenants' => TenantResource::collection($mall->activeTenants),
        ],
        'redirectTo' => '/public/mall/tab/create',
    ]);
}
```

---

## API Routes Summary

### Public Routes (No Auth)

```php
// domain/routes/api/mall_routes.php

Route::prefix('public/mall')->group(function () {
    // Sessions
    Route::prefix('session')->group(function () {
        Route::post('/create', [MallSessionController::class, 'createSession']);
        Route::get('/{hash}', [MallSessionController::class, 'getSession']);
        Route::put('/{hash}', [MallSessionController::class, 'updateSession']);
        Route::post('/{hash}/complete', [MallSessionController::class, 'completeSession']);
        Route::post('/{hash}/cancel', [MallSessionController::class, 'cancelSession']);
        Route::post('/validate-hash', [MallSessionController::class, 'validateHash']);
        Route::get('/mall/{mallId}/sessions', [MallSessionController::class, 'getMallSessions']);
        Route::get('/{hash}/notifications', [MallSessionController::class, 'getNotifications']);
        Route::post('/{hash}/notifications/mark-read', [MallSessionController::class, 'markNotificationsAsRead']);
    });
    
    // Stores
    Route::prefix('stores')->group(function () {
        Route::get('/', [MallStoresController::class, 'getList']);
        Route::get('/{id}', [MallStoresController::class, 'getOne']);
        Route::post('/{id}/assistance', [MallStoresController::class, 'assistance']);
    });
    
    // Products
    Route::prefix('products')->group(function () {
        Route::get('/', [MallProductsController::class, 'getList']);
        Route::get('/{id}', [MallProductsController::class, 'getOne']);
    });
    
    // Tabs (Orders)
    Route::prefix('tab')->group(function () {
        Route::get('/', [MallTabsController::class, 'getList']);
        Route::post('/', [MallTabsController::class, 'create']);
        Route::get('/{id}', [MallTabsController::class, 'getOne']);
        Route::put('/{id}', [MallTabsController::class, 'update']);
    });
    
    // Auth endpoints
    Route::get('{slug}/getAuth', [PublicMallController::class, 'getAuth']);
    Route::get('{sessionId}/getSessionAuth', [MallSessionController::class, 'getSessionAuth']);
});
```

### Authenticated Routes

```php
// Mall Admin routes (requires auth:sanctum)
Route::middleware(['auth:sanctum'])->prefix('mall')->group(function () {
    Route::post('/client_session/{mallSlug}', [MallSessionController::class, 'createClientSession']);
    Route::post('/client_session/{mallSlug}/clearPending', [MallSessionController::class, 'clearPending']);
    // Standard CRUD via MallController
});

// System Admin routes (requires auth:sanctum)
Route::middleware(['auth:sanctum'])->prefix('system/mall')->group(function () {
    // Mall CRUD via SystemMallController
    Route::prefix('session')->group(function () {
        // Session Admin via SystemMallSessionController
        Route::get('/{mallId}/statistics', [SystemMallSessionController::class, 'mallStatistics']);
        Route::post('/{mallId}/generate-hash', [SystemMallSessionController::class, 'generateNextHash']);
    });
});
```
