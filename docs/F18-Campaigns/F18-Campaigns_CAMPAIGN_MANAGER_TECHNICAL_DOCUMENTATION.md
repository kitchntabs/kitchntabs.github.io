# Campaign Manager & Publishing Service - Technical Documentation

**Version**: 1.0  
**Last Updated**: December 5, 2025  
**Project**: DASH-PW-PROJECT (Dash Framework)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Backend Components](#3-backend-components)
   - [Models](#31-models)
   - [Controllers](#32-controllers)
   - [Jobs](#33-jobs)
   - [Services](#34-services)
4. [Frontend Components](#4-frontend-components)
   - [Resource Configuration](#41-resource-configuration)
   - [Component Hierarchy](#42-component-hierarchy)
   - [Batch Actions](#43-batch-actions)
5. [Marketplace Publishing Service](#5-marketplace-publishing-service)
   - [Service Architecture](#51-service-architecture)
   - [Uber Eats Integration](#52-uber-eats-integration)
   - [Jumpseller Integration](#53-jumpseller-integration)
6. [Data Flow](#6-data-flow)
   - [Publishing Flow](#61-publishing-flow)
   - [Pause Flow](#62-pause-flow)
   - [Finish Flow](#63-finish-flow)
7. [Database Schema](#7-database-schema)
8. [API Reference](#8-api-reference)
9. [State Management](#9-state-management)
10. [Error Handling](#10-error-handling)
11. [Configuration](#11-configuration)

---

## 1. Overview

The Campaign Manager is a comprehensive solution for managing product campaigns across multiple marketplaces. It enables businesses to:

- **Create campaigns** with configurable pricing and stock settings
- **Publish products** to multiple marketplaces simultaneously (Uber Eats, Jumpseller, MercadoLibre, etc.)
- **Monitor status** of published products in real-time
- **Batch operations** for pausing, resuming, and finishing products
- **Track progress** via a sophisticated tracker system with phases

### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Marketplace Support** | Publish to multiple platforms from a single campaign |
| **Real-time Progress Tracking** | WebSocket-enabled progress updates |
| **Batch Operations** | Bulk publish/pause/finish operations |
| **Price Isolation** | Campaign-specific price lists (cloned from source) |
| **Stock Management** | Independent stock tracking per campaign |
| **Audit Trail** | Complete logging of all operations |

---

## 2. Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React-Admin)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ CampaignList│  │CampaignEdit │  │ProductTable │  │BatchActions │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ REST API / WebSocket
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND (Laravel)                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Controllers                                   │   │
│  │  CampaignController │ CampaignProductController │ TrackerController │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           Job Queue                                  │   │
│  │  CampaignProcessJob → PublishProductsJob → ManagePublishedProducts  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Marketplace Services                             │   │
│  │  UberService │ JumpsellerService │ MercadoLibreService │ ...        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL MARKETPLACES                               │
│        Uber Eats API │ Jumpseller API │ MercadoLibre API │ ...             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, React-Admin, MUI DataGrid, TypeScript |
| Backend | Laravel 10, PHP 8.2 |
| Queue | Laravel Horizon, Redis |
| Database | MySQL/PostgreSQL |
| Real-time | Laravel Echo, WebSockets |
| Cache | Redis |

---

## 3. Backend Components

### 3.1 Models

#### Campaign Model
**Path**: `domain/app/Models/ECommerce/Campaign.php`

The main entity representing a marketing campaign.

```php
class Campaign extends Model
{
    protected $fillable = [
        'tenant_id',
        'name',
        'description',
        'status',
        'scheduled',
        'start_date',
        'end_date'
    ];

    // Status Constants
    const STATUS_PENDING = 'PENDING';
    const STATUS_PUBLISHING = 'PUBLISHING';
    const STATUS_PUBLISHED = 'PUBLISHED';
    const STATUS_PAUSING = 'PAUSING';
    const STATUS_PAUSED = 'PAUSED';
    const STATUS_FINISHING = 'FINISHING';
    const STATUS_FINISHED = 'FINISHED';
}
```

**Relationships**:
| Relationship | Type | Target |
|--------------|------|--------|
| `tenant()` | BelongsTo | Tenant |
| `campaignMarketplaces()` | HasMany | CampaignMarketplace |
| `marketplaces()` | BelongsToMany | Marketplace |
| `campaignMarketplaceProducts()` | HasManyThrough | CampaignMarketplaceProduct |
| `logs()` | MorphMany | Log |

---

#### CampaignMarketplace Model
**Path**: `domain/app/Models/ECommerce/CampaignMarketplace.php`

Pivot entity linking campaigns to marketplaces with pricing/stock configuration.

```php
class CampaignMarketplace extends Model
{
    protected $table = 'campaign_marketplace';
    
    protected $fillable = [
        'campaign_id',
        'marketplace_id',
        'source_primary_pricelist_id',  // Original pricelist
        'source_sale_pricelist_id',
        'primary_pricelist_id',          // Cloned campaign pricelist
        'sale_pricelist_id',
        'source_stock_type_id',
        'stock_type_id'
    ];
}
```

**Key Method**:
```php
public function formatProducts($productIds): Collection
{
    // Returns products with computed prices and stocks
    // Used by marketplace services for publishing
}
```

---

#### CampaignMarketplaceProduct Model
**Path**: `domain/app/Models/ECommerce/CampaignMarketplaceProduct.php`

Tracks individual product status within a campaign-marketplace combination.

```php
class CampaignMarketplaceProduct extends Model
{
    protected $fillable = [
        'campaign_marketplace_id',
        'product_id',
        'status',
        'sales_count',
        'stock_alert_threshold',
        'marketplace_info',     // JSON: marketplace-specific data
        'marketplace_error'     // Error message from marketplace
    ];

    // Status Constants
    const STATUS_PENDING = 'PENDING';
    const STATUS_PUBLISHED = 'PUBLISHED';
    const STATUS_PAUSED = 'PAUSED';
    const STATUS_WARNING = 'WARNING';
    const STATUS_ERRORED = 'ERRORED';
    const STATUS_FINISHED = 'FINISHED';
}
```

**Query Scopes**:
```php
// Products that can be updated on marketplaces
scopeValidForUpdateOnMarketplaces()

// Products that can be paused
scopeValidForPause()

// Products that can be republished
scopeValidForRepublish()

// Products that can be published
scopeValidForPublish()

// Products that can be finished
scopeValidForFinish()
```

---

#### CampaignTracker Model
**Path**: `domain/app/Models/ECommerce/CampaignTracker.php`

Tracks progress and status of campaign operations.

```php
class CampaignTracker extends Model
{
    // Process Types
    const PROCESS_TYPE_MAIN = 'main';
    const PROCESS_TYPE_MARKETPLACE = 'marketplace';

    // Actions
    const ACTION_PUBLISHING = 'publishing';
    const ACTION_PAUSING = 'pausing';
    const ACTION_FINISHING = 'finishing';
    const ACTION_REPUBLISHING = 'republishing';

    // Statuses
    const STATUS_PENDING = 'pending';
    const STATUS_IN_PROGRESS = 'in_progress';
    const STATUS_COMPLETED = 'completed';
    const STATUS_FAILED = 'failed';

    protected $fillable = [
        'tenant_id', 'campaign_id', 'marketplace_id',
        'action', 'process_type', 'parent_tracker_id',
        'status', 'progress', 'total_tasks',
        'completed_tasks', 'failed_tasks',
        'phases_config', 'phases_status',
        'metadata', 'marketplace_metadata',
        'started_at', 'completed_at'
    ];
}
```

---

### 3.2 Controllers

#### CampaignController
**Path**: `domain/app/Http/Controllers/API/ECommerce/CampaignController.php`

**Base Class**: `ReactAdminBaseController`

| Endpoint | Method | Action | Description |
|----------|--------|--------|-------------|
| `GET /ecommerce/campaign` | `index` | List | List all campaigns |
| `GET /ecommerce/campaign/{id}` | `show` | Show | Get single campaign |
| `POST /ecommerce/campaign` | `store` | Create | Create campaign |
| `PUT /ecommerce/campaign/{id}` | `update` | Update | Update campaign |
| `DELETE /ecommerce/campaign/{id}` | `destroy` | Delete | Delete campaign |
| `PUT /ecommerce/campaign/{id}/publish` | `publish` | Publish | Start publishing |
| `PUT /ecommerce/campaign/{id}/republish` | `republish` | Republish | Republish products |
| `PUT /ecommerce/campaign/{id}/pause` | `pause` | Pause | Pause campaign |
| `PUT /ecommerce/campaign/{id}/finish` | `finish` | Finish | Finish campaign |
| `GET /ecommerce/campaign/tracker/{id}` | `getTrackerProgress` | Track | Get tracker progress |
| `PUT /ecommerce/campaign/{id}/reset` | `forceReset` | Reset | Force reset campaign |

**Publish Method**:
```php
public function publish(Request $request, Campaign $campaign)
{
    $this->clearCampaignLocks($campaign);
    
    CampaignProcessJob::dispatch(
        $request->user(),
        $campaign,
        'publish',
        false,
        ['validForPublish'],
        5  // chunk size
    );

    return response()->json([
        'message' => 'Publishing started',
        'tracker_id' => $trackerId
    ]);
}
```

---

#### CampaignProductController
**Path**: `domain/app/Http/Controllers/API/ECommerce/CampaignProductController.php`

Handles individual and batch product operations within a campaign. **Now creates trackers for progress monitoring.**

| Endpoint | Method | Description | Returns Tracker |
|----------|--------|-------------|----------------|
| `GET /campaign/{id}/products` | `index` | List campaign products | No |
| `POST /campaign/{id}/products` | `store` | Add products to campaign | No |
| `PUT /campaign/{id}/products` | `changeStatus` | Batch status change | No |
| `DELETE /campaign/{id}/products?action=delete` | `delete` | Delete products | **Yes** |
| `DELETE /campaign/{id}/products?action=finish` | `delete` | Finish products | **Yes** |
| `POST /campaign/{id}/products/publish` | `publish` | Publish individual products | **Yes** |
| `POST /campaign/{id}/products/pause` | `pause` | Pause individual products | **Yes** |
| `POST /campaign/{id}/products/finish` | `finish` | Finish individual products | **Yes** |

**Delete Method with Tracker** (example):
```php
public function delete(Request $request, $id)
{
    // ... validation ...
    
    // Create tracker for progress monitoring
    $trackerService = app(CampaignTrackerService::class);
    $action = $request->query('action') === 'finish' ? 'finish' : 'delete';
    $tracker = $trackerService->createTracker($campaign, $action, $request->user());
    
    // Initialize tracker with product count
    $trackerService->initializeTrackerPhases($tracker->id, [
        'processing' => $campaignMarketplaceProducts->count()
    ], [
        'total_products' => $campaignMarketplaceProducts->count(),
        'action' => $action
    ]);

    // Dispatch job with tracker ID
    DeleteProductsJob::dispatch(
        $request->user(), 
        $campaignMarketplaceProducts, 
        true, true, false, 
        $tracker->id,  // Pass tracker ID
        'default', 'processing'
    );

    return ResponseHandler::json([
        'message' => 'Se notificará al finalizar la eliminación.',
        'tracker_id' => $tracker->id,
        'total_products' => $campaignMarketplaceProducts->count()
    ]);
}
```

---

### 3.3 Jobs

#### Job Architecture

```
CampaignProcessJob (Main Orchestrator - Full Campaign Operations)
    │
    ├── Creates CampaignTracker
    ├── Initializes phases from marketplace service
    │
    └── Dispatches per-marketplace jobs:
        ├── PublishProductsJob (chunks of 5 products)
        ├── PauseProductsJob
        └── FinishProductsJob
            │
            └── ManagePublishedProductsJob (post-processing)

CampaignProductController (Individual Product Operations)
    │
    ├── Creates CampaignTracker in controller
    ├── Initializes tracker phases with product count
    │
    └── Dispatches jobs with tracker ID:
        ├── DeleteProductsJob (timeout: 600s)
        ├── PublishProductsJob (timeout: 900s)
        ├── PauseProductsJob (timeout: 600s)
        └── FinishProductsJob (timeout: 600s)
            │
            └── Marketplace Service updates tracker per-product
```

#### Job Timeout Configuration

| Job | Timeout | Tries | Purpose |
|-----|---------|-------|--------|
| CampaignProcessJob | 7200s (2h) | 1 | Main orchestrator |
| PublishProductsJob | 900s (15m) | 3 | Publish products to marketplace |
| DeleteProductsJob | 600s (10m) | 3 | Delete products from marketplace |
| PauseProductsJob | 600s (10m) | 3 | Pause products on marketplace |
| FinishProductsJob | 600s (10m) | 3 | Finish/unpublish products |
| ManagePublishedProductsJob | 600s (10m) | 1 | Post-processing |
| ManagePausedProductsJob | 600s (10m) | 1 | Post-pause processing |
| ManageFinishedProductsJob | 600s (10m) | 1 | Post-finish processing |
| UpdateProductsWithPresaleJob | 600s (10m) | 1 | Presale updates |

---

#### CampaignProcessJob
**Path**: `domain/app/Jobs/ECommerce/Campaigns/CampaignProcessJob.php`

**Queue**: `campaigns`  
**Timeout**: 7200 seconds (2 hours)

Main orchestrator for all campaign operations.

```php
class CampaignProcessJob implements ShouldQueue
{
    public function __construct(
        public User $user,
        public Campaign $campaign,
        public string $action,           // 'publish', 'pause', 'finish', 'republish'
        public bool $forceAction = false,
        public array $campaignMarketplaceProductScopes = [],
        public int $chunkSize = 5
    ) {}

    public function handle(): void
    {
        // 1. Cancel existing in-progress trackers
        $this->cancelExistingTrackers();
        
        // 2. Create new tracker
        $tracker = $this->createTracker();
        
        // 3. Acquire lock
        $lock = Cache::lock("campaign.{$this->campaign->id}.{$this->action}");
        
        // 4. Initialize tracker phases
        $this->initializeTracker($tracker);
        
        // 5. Process products by marketplace
        $this->processProducts();
        
        // 6. Wait for completion
        $this->waitForCompletion();
        
        // 7. Finalize
        $this->checkAndCompleteProcess();
    }
}
```

---

#### PublishProductsJob
**Path**: `domain/app/Jobs/ECommerce/CampaignMarketplaceProducts/PublishProductsJob.php`

Handles the actual publishing of products to marketplaces.

```php
class PublishProductsJob implements ShouldQueue
{
    use ActionJobCommonTrait;

    public function __construct(
        public User $user,
        public Collection $campaignMarketplaceProducts,
        public bool $shouldNotify = false,
        public bool $shouldThrowErrors = false,
        public bool $allowZeroStock = false,
        public ?string $trackerId = null,
        public ?Marketplace $marketplace = null,
        public ?string $phase = null
    ) {}

    protected function executeMarketplaceOperation(
        $marketplaceInstance,
        $products
    ): void {
        $marketplaceInstance->publishProducts(
            $this->user,
            $products,
            $this->shouldNotify,
            $this->shouldThrowErrors,
            $this->allowZeroStock,
            $this->trackerId
        );
    }
}
```

---

#### ManagePublishedProductsJob
**Path**: `domain/app/Jobs/ECommerce/CampaignMarketplaceProducts/ManagePublishedProductsJob.php`

Post-processing after marketplace operations.

```php
class ManagePublishedProductsJob implements ShouldQueue
{
    public function handle(): void
    {
        // 1. Update product statuses (PUBLISHED, ERRORED, WARNING)
        // 2. Update tracker progress
        // 3. Send notifications
        // 4. Pause same products on other active campaigns
        // 5. Create UnresolvedErroredProduct records for failures
    }
}
```

---

### 3.4 Services

#### CampaignTrackerService
**Path**: `domain/app/Services/Campaign/CampaignTrackerService.php`

Manages campaign progress tracking.

```php
class CampaignTrackerService
{
    public function createTracker(Campaign $campaign, string $action): CampaignTracker
    {
        return CampaignTracker::create([
            'tenant_id' => $campaign->tenant_id,
            'campaign_id' => $campaign->id,
            'action' => $action,
            'status' => CampaignTracker::STATUS_PENDING,
            'progress' => 0,
            'total_tasks' => 0,
            'completed_tasks' => 0,
            'failed_tasks' => 0
        ]);
    }

    public function initializeTrackerPhases(
        CampaignTracker $tracker,
        array $phases,
        int $totalProducts
    ): void {
        $tracker->update([
            'phases_config' => $phases,
            'phases_status' => $this->initializePhaseStatuses($phases),
            'total_tasks' => $totalProducts
        ]);
    }

    public function updatePhaseProgress(
        CampaignTracker $tracker,
        string $phase,
        int $completed,
        int $failed = 0
    ): void {
        // Update phase status and recalculate overall progress
    }
}
```

---

#### CampaignNotificationService
**Path**: `domain/app/Services/Campaign/CampaignNotificationService.php`

Handles campaign-related notifications via WebSocket.

```php
class CampaignNotificationService
{
    public function campaignStatusChanged(Campaign $campaign, string $status): void
    {
        broadcast(new CampaignStatusChanged($campaign, $status));
    }

    public function campaignProgress(Campaign $campaign, array $progress): void
    {
        broadcast(new CampaignProgress($campaign, $progress));
    }

    public function campaignError(Campaign $campaign, string $error): void
    {
        broadcast(new CampaignError($campaign, $error));
    }
}
```

---

## 4. Frontend Components

### 4.1 Resource Configuration

**Path**: `apps/dash/src/resources/Campaign/CampaignResource.tsx`

```typescript
const campaignResource: IAppResourceConfig = {
    roles: [DASHAppConstants.system.TENANT_ROLE],
    component: CampaignResource,
    model: "ecommerce/campaign",
    group: "Campañas",
    label: "Campañas",
    schema: campaignSchema,
    icon: <GifBox />,
    
    menu: [{ 
        title: "Listado de Campañas", 
        redirect: "/ecommerce/campaign" 
    }],
    
    mainAction: { 
        title: "Crear", 
        fn: "redirect", 
        mode: "create", 
        redirect: "create" 
    },
    
    showDialogAfterSubmit: true,
    redirectAfterCreate: "list",
    redirectAfterUpdate: 'edit',
    resetSelectedIdsOnLoad: true,
};
```

### Campaign Schema

| Attribute | Label | Type | Create | Edit | List |
|-----------|-------|------|--------|------|------|
| `name` | Nombre | String | ✅ | ✅ | ✅ |
| `description` | Descripción | String | ✅ | ✅ | ❌ |
| `products_count` | Productos | Number | ❌ | ❌ | ✅ |
| `total_errored` | Errores | Number | ❌ | ❌ | ✅ |
| `total_paused` | Pausados | Number | ❌ | ❌ | ✅ |
| `total_published` | Publicados | Number | ❌ | ❌ | ✅ |
| `total_sales` | Ventas | Number | ❌ | ❌ | ✅ |
| `campaign_settings` | Configuración | Custom | ✅ | ✅ | ❌ |
| `marketplaces` | Marketplaces | Custom | ✅ | ❌ | ✅ |

---

### 4.2 Component Hierarchy

```
apps/dash/src/components/ecommerce/Campaign/
├── CampaignEdit.tsx                    # Main edit view (748 lines)
├── Settings.tsx                        # Scheduled/permanent toggle
├── MarketplacesSelector.tsx            # Marketplace checkboxes
├── ProductsSelector.tsx                # Product selector
│
├── Campaign/
│   ├── CampaignButtons.tsx             # Action buttons
│   ├── CampaignProductTable.tsx        # Product data grid (375 lines)
│   ├── CampaignProductsBatchActions.tsx # Batch operations UI
│   └── CampaignStats.tsx               # Campaign statistics
│
├── Products/
│   ├── CampaignProductsBatchOperations.tsx
│   ├── ProductStatusCell.tsx
│   └── Grid/
│       ├── ActionStatusCell.tsx
│       ├── StatusCell.tsx
│       ├── PriceCell.tsx               # Inline price editing
│       ├── StockCell.tsx               # Inline stock editing
│       └── ...
│
├── Tabs/
│   └── Logs.tsx                        # Campaign activity logs
│
└── Create/
    └── PriceStock.tsx                  # Price/stock configuration
```

---

### 4.3 Batch Actions

**Path**: `apps/dash/src/components/ecommerce/Campaign/Campaign/CampaignProductsBatchActions.tsx`

```typescript
interface CampaignProductsBatchActionsProps {
    batchSelectedCampaignProducts: ICampaignProduct[];
    setBatchSelectedCampaignProducts: (products: ICampaignProduct[]) => void;
}

const CampaignProductsBatchActions: React.FC<Props> = ({
    batchSelectedCampaignProducts,
    setBatchSelectedCampaignProducts
}) => {
    const changeProductStatus = async (
        productIds: number[], 
        status: string
    ) => {
        const payload = {
            tenant_id: Number(tenant_id),
            product_ids: productIds,
            campaign_marketplace_ids: Array.from(new Set(
                batchSelectedCampaignProducts.flatMap(product =>
                    product.campaign_marketplaces.map(mp => mp.id)
                )
            ))
        };

        await httpClient.put(
            `/ecommerce/campaign/${campaign_id}/products`,
            { data: payload }
        );
        
        refresh();
    };

    return (
        <ButtonGroup>
            <Tooltip title="Republicar">
                <IconButton onClick={() => handleAction('republish')}>
                    <PlayIcon />
                </IconButton>
            </Tooltip>
            <Tooltip title="Pausar">
                <IconButton onClick={() => handleAction('pause')}>
                    <PauseIcon />
                </IconButton>
            </Tooltip>
            <Tooltip title="Finalizar">
                <IconButton onClick={() => handleAction('finish')}>
                    <StopIcon />
                </IconButton>
            </Tooltip>
            <Tooltip title="Eliminar">
                <IconButton onClick={() => handleAction('delete')}>
                    <DeleteIcon />
                </IconButton>
            </Tooltip>
        </ButtonGroup>
    );
};
```

---

## 5. Marketplace Publishing Service

### 5.1 Service Architecture

**Path**: `domain/app/Services/ECommerce/Marketplaces/`

```
Marketplaces/
├── Contracts/
│   └── Marketplace.php              # Interface contract
├── Abstracts/
│   └── Manager.php                  # Base manager class
├── Uber/
│   ├── UberService.php             # Main service
│   ├── ServiceTraits/
│   │   ├── Api.php
│   │   ├── Menu.php                # Menu management
│   │   ├── Store.php
│   │   ├── OrderTrait.php
│   │   └── WebhookTrait.php
│   └── Resources/
│       └── Menu.php                # Menu API resource
├── Jumpseller/
│   ├── JumpsellerService.php
│   └── Traits/
│       ├── PublishServiceMethods.php
│       ├── PauseServiceMethods.php
│       └── ...
├── MercadoLibre/
├── Falabella/
└── ...
```

#### Marketplace Interface

```php
interface Marketplace
{
    public function __construct(MarketplaceModel $marketplace);
    
    // Core Operations
    public function publishProducts(
        User $user,
        Collection $products,
        bool $notify,
        bool $throw,
        bool $allowZeroStock,
        ?string $trackerId
    ): void;
    
    public function pauseProducts(
        User $user,
        Collection $products,
        bool $notify,
        bool $throw,
        bool $republish,
        ?string $trackerId
    ): void;
    
    public function finishProducts(
        User $user,
        Collection $products,
        bool $notify,
        bool $throw,
        bool $republish,
        ?string $trackerId
    ): void;
    
    // Sync Operations
    public function handleSyncCategories(?string $hashUpdate): string;
    
    // Webhook Handling
    public function handleWebhook(string $type, array $payload): array;
    
    // Order Management
    public function confirmOrder(array $payload): array;
    public function rejectOrder(array $payload): array;
}
```

---

### 5.2 Uber Eats Integration

**Path**: `domain/app/Services/ECommerce/Marketplaces/Uber/UberService.php`

#### Overview

Uber Eats uses a **menu-based architecture** where products are published as items within a structured menu. Key characteristics:

- **Menu Structure**: Items → Categories → Menus
- **API Pattern**: Full menu replacement (PUT operation)
- **Modifier Support**: Modifier groups and modifier options for product customization
- **Price Format**: Cents (integer values)

#### Menu Data Structure

```php
$menuData = [
    'menus' => [[
        'id' => "menu_{$storeId}",
        'title' => ['translations' => ['en_us' => 'Menu Name']],
        'service_availability' => [
            [
                'day_of_week' => 'monday',
                'time_periods' => [
                    ['start_time' => '09:00', 'end_time' => '22:00']
                ]
            ],
            // ... other days
        ],
        'category_ids' => ['category_1', 'category_2']
    ]],
    'categories' => [[
        'id' => 'category_1',
        'title' => ['translations' => ['en_us' => 'Category Name']],
        'entities' => [
            ['id' => 'item_123', 'type' => 'ITEM'],
            ['id' => 'item_456', 'type' => 'ITEM']
        ]
    ]],
    'items' => [[
        'id' => 'item_123',
        'title' => ['translations' => ['en_us' => 'Product Name']],
        'description' => ['translations' => ['en_us' => 'Description']],
        'price_info' => [
            'price' => 1500,  // $15.00 in cents
            'overrides' => []
        ],
        'tax_info' => ['tax_rate' => 0],
        'external_data' => 'SKU123',
        'modifier_group_ids' => ['mg_1']
    ]],
    'modifier_groups' => [[
        'id' => 'mg_1',
        'title' => ['translations' => ['en_us' => 'Options']],
        'quantity_info' => [
            'quantity' => ['min_permitted' => 0, 'max_permitted' => 5]
        ],
        'modifier_options' => [[
            'id' => 'mo_1',
            'title' => ['translations' => ['en_us' => 'Extra Cheese']],
            'price_info' => [
                'price' => 0,
                'overrides' => [[
                    'context_type' => 'MODIFIER_GROUP',
                    'context_value' => 'mg_1',
                    'price' => 200  // $2.00
                ]]
            ]
        ]]
    ]]
];
```

#### Key Methods

| Method | Purpose |
|--------|---------|
| `publishProducts()` | Main entry point for publishing |
| `prepareMenuData()` | Converts products to Uber menu format |
| `mergeMenuData()` | Merges existing menu with new products |
| `cleanupUberMenu()` | Removes products not in current campaign |
| `updateMenu()` | Sends menu to Uber API |
| `pauseProduct()` | Sets item suspension_info |
| `finishProduct()` | Removes item from menu |

#### Publishing Flow

```php
public function publishProducts(
    $user,
    $campaignMarketplaceProducts,
    $shouldNotify,
    $shouldThrowErrors,
    $allowZeroStock,
    $trackerId
): void {
    // 1. Get store ID from marketplace connection_params
    $storeId = $this->marketplace->connection_params['store_id'];
    
    // 2. Group products by category
    $productsByCategory = $this->groupProductsByCategory($products);
    
    // 3. Prepare menu data
    $menuData = $this->prepareMenuData($campaignMarketplace, $productsByCategory, $storeId);
    
    // 4. Determine publish type (partial vs full)
    $totalCampaignProducts = $campaignMarketplace->campaignMarketplaceProducts()->count();
    $isPartialPublish = $productsBeingPublished < $totalCampaignProducts;
    
    // 5. Get existing menu
    $currentMenu = $this->menuResource()->getMenu($storeId);
    
    // 6. Merge or create menu
    if ($currentMenu) {
        if ($isPartialPublish) {
            // Skip cleanup for partial publish
            $mergedMenu = $this->mergeMenuData($currentMenu, $menuData);
        } else {
            // Full publish - clean up old products
            $cleanedMenu = $this->cleanupUberMenu($storeId, $currentMenu, $campaignProductIds);
            $mergedMenu = $this->mergeMenuData($cleanedMenu, $menuData);
        }
        $this->menuResource()->updateMenu($storeId, $mergedMenu);
    } else {
        $this->menuResource()->createMenu($storeId, $menuData);
    }
    
    // 7. Update marketplace_info for each product
    foreach ($products as $product) {
        $product->update([
            'marketplace_info' => [
                'id' => "item_{$product->product_id}",
                'store_id' => $storeId,
                'status' => 'available',
                'updated_at' => now()->toIso8601String()
            ]
        ]);
    }
    
    // 8. Dispatch post-processing job
    ManagePublishedProductsJob::dispatch(...);
}
```

#### Partial Publish Behavior

When publishing selected products (not all campaign products):

```php
// Detect partial publish
$isPartialPublish = $productsBeingPublished < $totalCampaignProducts;

if ($isPartialPublish) {
    Log::info('Partial publish: Skipping cleanup to preserve other products');
    // Use current menu as-is, only add/update selected products
    $cleanedMenu = $currentMenu;
} else {
    // Full publish: Clean up products no longer in campaign
    $cleanedMenu = $this->cleanupUberMenu($storeId, $currentMenu, $campaignProductIds);
}
```

---

### 5.3 Jumpseller Integration

**Path**: `domain/app/Services/ECommerce/Marketplaces/Jumpseller/JumpsellerService.php`

#### Overview

Jumpseller uses a **product-based API** where each product is created/updated individually.

- **API Pattern**: Individual product CRUD operations
- **Product Structure**: Products with variants, categories, images
- **Price Format**: Decimal values

#### Publishing Flow (with Tracker Integration)

```php
public function publishProducts(
    $user,
    $campaignMarketplaceProducts,
    $shouldNotify,
    $shouldThrowErrors,
    $allowZeroStock,
    $trackerId
): void {
    $totalProducts = $campaignMarketplaceProducts->count();
    $processedCount = 0;
    $successCount = 0;
    $errorCount = 0;
    
    // Initialize tracker service if trackerId is provided
    $trackerService = $trackerId ? app(CampaignTrackerService::class) : null;
    
    foreach ($campaignMarketplaceProducts as $campaignMarketplaceProduct) {
        try {
            $productInfo = $campaignMarketplaceProduct->marketplace_info;
            
            if (!empty($productInfo['id'])) {
                // Update existing product
                $response = $this->update($campaignMarketplaceProduct);
            } else {
                // Create new product
                $response = $this->publishProduct($campaignMarketplaceProduct);
            }
            
            // Update marketplace_info
            $campaignMarketplaceProduct->update([
                'status' => CampaignMarketplaceProduct::STATUS_PUBLISHED,
                'marketplace_info' => [
                    'id' => $response['id'],
                    'permalink' => $response['permalink'],
                    'status' => 'available',
                    'updated_at' => now()->toIso8601String()
                ]
            ]);
            
            $successCount++;
        } catch (Exception $e) {
            $errorCount++;
            $campaignMarketplaceProduct->update([
                'status' => CampaignMarketplaceProduct::STATUS_ERRORED,
                'error_message' => $e->getMessage()
            ]);
        }
        
        $processedCount++;
        
        // Update tracker progress after each product (WebSocket notification sent)
        if ($trackerService && $trackerId) {
            $trackerService->updateProgress(
                $trackerId,
                'processing',
                $processedCount,
                $successCount,
                $errorCount
            );
        }
    }
    
    // Mark tracker as completed
    if ($trackerService && $trackerId) {
        $trackerService->completeTracker($trackerId, $errorCount > 0);
    }
}
```

#### Marketplace Service Traits with Tracker Integration

All Jumpseller service traits now support per-product progress tracking:

| Trait | Location | Tracker Support |
|-------|----------|-----------------|
| `PublishServiceMethods` | `Jumpseller/Traits/PublishServiceMethods.php` | ✅ Per-product updates |
| `DeleteServiceMethods` | `Jumpseller/Traits/DeleteServiceMethods.php` | ✅ Per-product updates |
| `PauseServiceMethods` | `Jumpseller/Traits/PauseServiceMethods.php` | ✅ Per-product updates |
| `FinishServiceMethods` | `Jumpseller/Traits/FinishServiceMethods.php` | ✅ Per-product updates |
```

---

## 6. Data Flow

### 6.1 Publishing Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. USER ACTION                                                              │
│    Click "Publicar campaña" button in frontend                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. API REQUEST                                                              │
│    PUT /api/ecommerce/campaign/{id}/publish                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. CONTROLLER (CampaignController::publish)                                 │
│    - Clear existing locks                                                   │
│    - Dispatch CampaignProcessJob                                            │
│    - Return tracker_id to frontend                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. ORCHESTRATOR JOB (CampaignProcessJob)                                    │
│    - Cancel existing trackers                                               │
│    - Create new CampaignTracker                                             │
│    - Update campaign status → PUBLISHING                                    │
│    - Group products by marketplace                                          │
│    - Initialize tracker phases from marketplace service                     │
│    - Dispatch PublishProductsJob for each chunk                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                        ┌─────────────┴─────────────┐
                        ▼                           ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐
│ 5. PUBLISH JOB (Chunk 1)    │   │ 5. PUBLISH JOB (Chunk 2)    │
│    - Validate products      │   │    - Same process           │
│    - Call marketplace API   │   │                             │
└─────────────────────────────┘   └─────────────────────────────┘
                        │                           │
                        ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 6. MARKETPLACE SERVICE (UberService/JumpsellerService)                      │
│    - Prepare data for marketplace API format                                │
│    - Make API calls (create/update menu or products)                        │
│    - Handle responses and errors                                            │
│    - Update CampaignMarketplaceProduct.marketplace_info                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 7. POST-PROCESSING (ManagePublishedProductsJob)                             │
│    - Update product statuses (PUBLISHED/ERRORED/WARNING)                    │
│    - Update tracker progress                                                │
│    - Send WebSocket notifications                                           │
│    - Create UnresolvedErroredProduct for failures                           │
│    - Pause same products on other active campaigns                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 8. COMPLETION (CampaignProcessJob::checkAndCompleteProcess)                 │
│    - Verify all jobs completed                                              │
│    - Update campaign status → PUBLISHED                                     │
│    - Release locks                                                          │
│    - Send completion notification                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Pause Flow

```
User clicks "Pausar" → CampaignController::pause()
    → CampaignProcessJob (action='pause')
        → PauseProductsJob
            → MarketplaceService::pauseProducts()
                - Uber: Set suspension_info on items
                - Jumpseller: Set status='disabled'
            → ManagePausedProductsJob
                - Update status → PAUSED
                - Send notifications
        → Campaign status → PAUSED
```

### 6.3 Finish Flow

```
User clicks "Finalizar" → CampaignController::finish()
    → CampaignProcessJob (action='finish')
        → FinishProductsJob
            → MarketplaceService::finishProducts()
                - Uber: Remove items from menu OR suspend indefinitely
                - Jumpseller: Delete product OR set status='disabled'
            → ManageFinishedProductsJob
                - Update status → FINISHED
                - Clear marketplace_info
                - Send notifications
        → Campaign status → FINISHED
```

---

## 7. Database Schema

### Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐
│   Tenant    │────<│      Campaign       │>────│Marketplace  │
└─────────────┘     └─────────────────────┘     └─────────────┘
                              │
                              │ HasMany
                              ▼
                    ┌─────────────────────┐
                    │ CampaignMarketplace │─────────────┐
                    │    (Pivot Table)    │             │
                    └─────────────────────┘             │
                              │                         │
                              │ HasMany                 │ BelongsTo
                              ▼                         ▼
              ┌───────────────────────────────┐   ┌───────────┐
              │ CampaignMarketplaceProduct    │   │ Pricelist │
              │ - status                      │   │ StockType │
              │ - marketplace_info (JSON)     │   └───────────┘
              │ - marketplace_error           │
              └───────────────────────────────┘
                              │
                              │ BelongsTo
                              ▼
                       ┌───────────┐
                       │  Product  │
                       └───────────┘

┌─────────────────────────────┐
│     CampaignTracker         │
│ - action (publish/pause/...)│
│ - status                    │
│ - progress                  │
│ - phases_config (JSON)      │
│ - phases_status (JSON)      │
└─────────────────────────────┘
```

### Key Tables

| Table | Purpose |
|-------|---------|
| `campaigns` | Main campaign records |
| `campaign_marketplace` | Campaign-to-marketplace pivot with pricing config |
| `campaign_marketplace_product` | Product tracking per campaign-marketplace |
| `campaign_trackers` | Progress tracking for operations |
| `marketplaces` | Marketplace configurations |
| `pricelists` | Price list definitions |
| `stock_types` | Stock type definitions |

---

## 8. API Reference

### Campaign Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/ecommerce/campaign` | List campaigns | - |
| `POST` | `/ecommerce/campaign` | Create campaign | `{name, description, scheduled, start_date, end_date, marketplaces[]}` |
| `GET` | `/ecommerce/campaign/{id}` | Get campaign | - |
| `PUT` | `/ecommerce/campaign/{id}` | Update campaign | `{name, description, ...}` |
| `DELETE` | `/ecommerce/campaign/{id}` | Delete campaign | - |
| `PUT` | `/ecommerce/campaign/{id}/publish` | Start publishing | - |
| `PUT` | `/ecommerce/campaign/{id}/republish` | Republish products | - |
| `PUT` | `/ecommerce/campaign/{id}/pause` | Pause campaign | - |
| `PUT` | `/ecommerce/campaign/{id}/finish` | Finish campaign | - |
| `PUT` | `/ecommerce/campaign/{id}/reset` | Force reset | - |
| `GET` | `/ecommerce/campaign/tracker/{id}` | Get tracker progress | - |

### Product Endpoints

| Method | Endpoint | Description | Request Body | Returns Tracker |
|--------|----------|-------------|--------------|-----------------|
| `GET` | `/ecommerce/campaign/{id}/products` | List products | - | No |
| `POST` | `/ecommerce/campaign/{id}/products` | Add products | `{product_ids[]}` | No |
| `PUT` | `/ecommerce/campaign/{id}/products` | Batch status change | `{product_ids[], campaign_marketplace_ids[], status}` | No |
| `DELETE` | `/ecommerce/campaign/{id}/products?action=delete` | Delete products | `{product_ids[], campaign_marketplace_ids[]}` | **Yes** |
| `DELETE` | `/ecommerce/campaign/{id}/products?action=finish` | Finish products | `{product_ids[], campaign_marketplace_ids[]}` | **Yes** |
| `POST` | `/ecommerce/campaign/{id}/products/publish` | Publish products | `{product_ids[], campaign_marketplace_ids[]}` | **Yes** |
| `POST` | `/ecommerce/campaign/{id}/products/pause` | Pause products | `{product_ids[], campaign_marketplace_ids[]}` | **Yes** |
| `POST` | `/ecommerce/campaign/{id}/products/finish` | Finish products | `{product_ids[], campaign_marketplace_ids[]}` | **Yes** |

### Response Formats

**Individual Product Operation Response** (new):
```json
{
    "message": "Se notificará al finalizar la eliminación.",
    "tracker_id": 123,
    "total_products": 41
}
```

**Campaign Response**:
```json
{
    "id": 1,
    "name": "Black Friday 2025",
    "description": "Annual sale campaign",
    "status": "PUBLISHED",
    "scheduled": true,
    "start_date": "2025-11-29T00:00:00Z",
    "end_date": "2025-11-30T23:59:59Z",
    "products_count": 150,
    "total_published": 148,
    "total_errored": 2,
    "total_paused": 0,
    "total_sales": 1250,
    "tracker_id": 45,
    "tracker_summary": {
        "status": "completed",
        "progress": 100,
        "completed_tasks": 150,
        "failed_tasks": 2
    },
    "campaign_marketplaces": [
        {
            "id": 1,
            "marketplace_id": 5,
            "marketplace": {
                "id": 5,
                "name": "Uber Eats"
            }
        }
    ]
}
```

**Tracker Progress Response**:
```json
{
    "id": 45,
    "campaign_id": 1,
    "action": "publishing",
    "status": "in_progress",
    "progress": 65,
    "total_tasks": 150,
    "completed_tasks": 98,
    "failed_tasks": 2,
    "phases_status": {
        "prepare_menu": {
            "status": "completed",
            "completed": 1,
            "total": 1
        },
        "publish_items": {
            "status": "in_progress",
            "completed": 97,
            "total": 149
        }
    },
    "started_at": "2025-12-05T10:00:00Z",
    "last_activity_at": "2025-12-05T10:15:30Z"
}
```

---

## 9. State Management

### Campaign Status State Machine

```
                    ┌──────────────┐
                    │   PENDING    │◄─────────────────────┐
                    └──────┬───────┘                      │
                           │                             │
                           │ publish()                   │
                           ▼                             │
                    ┌──────────────┐                     │
                    │  PUBLISHING  │                     │
                    └──────┬───────┘                     │
                           │                             │
                           │ success                     │
                           ▼                             │
┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│   PAUSING    │◄───│  PUBLISHED   │───►│  FINISHING   │ │
└──────┬───────┘    └──────────────┘    └──────┬───────┘ │
       │                   ▲                    │         │
       │ success           │ republish()        │ success │
       ▼                   │                    ▼         │
┌──────────────┐           │            ┌──────────────┐  │
│    PAUSED    │───────────┘            │   FINISHED   │──┘
└──────────────┘                        └──────────────┘
```

### Product Status State Machine

```
┌──────────────┐
│   PENDING    │
└──────┬───────┘
       │
       │ publishProducts()
       ▼
┌──────────────┐                    ┌──────────────┐
│  PUBLISHED   │◄──────────────────►│    PAUSED    │
└──────┬───────┘  pause/republish   └──────┬───────┘
       │                                    │
       │ finishProducts()                   │ finishProducts()
       ▼                                    ▼
┌──────────────┐                    ┌──────────────┐
│   FINISHED   │                    │   FINISHED   │
└──────────────┘                    └──────────────┘

┌──────────────┐
│   ERRORED    │ (Can occur from any operation)
└──────────────┘

┌──────────────┐
│   WARNING    │ (Published with issues)
└──────────────┘
```

### Frontend State

```typescript
// Campaign Edit State
const [inTransitionState, setInTransitionstate] = useState<boolean>(false);
const [selectedProducts, setSelectedProducts] = useState([]);
const [trackerSummary, setTrackerSummary] = useState<TrackerSummary>(null);

// Product Table State
const [batchSelectedCampaignProducts, setBatchSelectedCampaignProducts] = useState<any[]>([]);
const [searchText, setSearchText] = useState('');
const [editData, setEditData] = useState(undefined);
```

---

## 10. Error Handling

### Error Categories

| Category | Description | User Action |
|----------|-------------|-------------|
| **Validation Errors** | Missing price, invalid stock | Fix product data |
| **API Errors** | Marketplace API failures | Retry or contact support |
| **Timeout Errors** | Long-running operations | Wait and refresh |
| **Rate Limit Errors** | Too many API calls | Automatic retry with backoff |

### Error Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Error Occurs                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Marketplace Service                                      │
│  1. Log::error() with context                                               │
│  2. Add to erroredCampaignMarketplaceProducts                               │
│  3. If shouldThrowErrors: throw exception                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ManagePublishedProductsJob                               │
│  1. Update product status → ERRORED                                         │
│  2. Store error in marketplace_error column                                 │
│  3. Create UnresolvedErroredProduct record                                  │
│  4. Update tracker failed_tasks count                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Notification Service                                     │
│  1. Send WebSocket notification with error details                          │
│  2. Display error in frontend toast/alert                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Error Storage

```php
// CampaignMarketplaceProduct
$product->update([
    'status' => CampaignMarketplaceProduct::STATUS_ERRORED,
    'marketplace_error' => $exception->getMessage()
]);

// UnresolvedErroredProduct (for tracking)
UnresolvedErroredProduct::create([
    'campaign_marketplace_product_id' => $product->id,
    'error_message' => $exception->getMessage(),
    'error_code' => $exception->getCode(),
    'error_context' => json_encode($context)
]);
```

---

## 11. Configuration

### Marketplace Connection Parameters

```php
// Uber Eats
$marketplace->connection_params = [
    'store_id' => 'uber_store_abc123',
    'menu_id' => 'menu_xyz789',
    'client_id' => 'uber_client_id',
    'client_secret' => 'encrypted_secret'
];

// Jumpseller
$marketplace->connection_params = [
    'login' => 'store_login',
    'authtoken' => 'encrypted_token',
    'store_id' => 'jumpseller_store_id'
];
```

### Queue Configuration

```php
// config/horizon.php
'campaigns' => [
    'connection' => 'redis',
    'queue' => ['campaigns'],
    'balance' => 'auto',
    'minProcesses' => 1,
    'maxProcesses' => 10,
    'tries' => 3,
    'timeout' => 7200,  // 2 hours
],
```

### Rate Limiting

```php
// Per marketplace rate limits
$rateLimits = [
    'uber' => [
        'requests_per_minute' => 60,
        'burst_limit' => 100
    ],
    'jumpseller' => [
        'requests_per_minute' => 120,
        'burst_limit' => 200
    ]
];
```

### Environment Variables

```env
# Queue
QUEUE_CONNECTION=redis
HORIZON_PREFIX=dash_horizon_

# Uber Eats
UBER_EATS_CLIENT_ID=xxx
UBER_EATS_CLIENT_SECRET=xxx
UBER_EATS_WEBHOOK_SECRET=xxx

# Jumpseller
JUMPSELLER_API_URL=https://api.jumpseller.com
JUMPSELLER_WEBHOOK_SECRET=xxx

# Campaign Settings
CAMPAIGN_PUBLISH_CHUNK_SIZE=5
CAMPAIGN_JOB_TIMEOUT=7200
```

---

## Appendix A: TypeScript Interfaces

```typescript
// Campaign
export interface ICampaign {
    id: number;
    name: string;
    description: string;
    scheduled: boolean;
    start_date?: string;
    end_date?: string;
    status: CampaignStatuses;
    tenant_id: number;
    campaign_marketplaces: ICampaignMarketplace[];
    products_count: number;
    total_errored: number;
    total_finished: number;
    total_paused: number;
    total_pending: number;
    total_published: number;
    total_sales: number;
    total_warning: number;
    tracker_id?: number;
    tracker_summary?: ITrackerSummary;
}

export enum CampaignStatuses {
    PENDING = 'PENDING',
    PUBLISHING = 'PUBLISHING',
    PUBLISHED = 'PUBLISHED',
    PAUSING = 'PAUSING',
    PAUSED = 'PAUSED',
    FINISHING = 'FINISHING',
    FINISHED = 'FINISHED'
}

// Campaign Product
export interface ICampaignProduct {
    id: number;
    sku: string;
    description: string;
    primary_price: string;
    sale_price: string;
    stock: string;
    status: ProductStatuses;
    campaign_marketplaces: ICampaignMarketplace[];
}

export enum ProductStatuses {
    PENDING = 'PENDING',
    PUBLISHED = 'PUBLISHED',
    PAUSED = 'PAUSED',
    FINISHED = 'FINISHED',
    ERRORED = 'ERRORED',
    WARNING = 'WARNING'
}

// Tracker
export interface ITrackerSummary {
    id: number;
    status: string;
    progress: number;
    total_tasks: number;
    completed_tasks: number;
    failed_tasks: number;
    phases_status: Record<string, IPhaseStatus>;
}

export interface IPhaseStatus {
    status: 'pending' | 'in_progress' | 'completed' | 'failed';
    completed: number;
    total: number;
}
```

---

## Appendix B: Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Campaign stuck in PUBLISHING | Job timeout or crash | Use force reset endpoint |
| Products not appearing on marketplace | API error or rate limiting | Check logs, retry |
| Tracker not updating | WebSocket disconnected | Refresh page, check connection |
| Partial publish removing products | Old behavior before fix | Update to latest version |

### Debug Commands

```bash
# Check campaign status
php artisan tinker
Campaign::find(1)->status

# View tracker progress
CampaignTracker::where('campaign_id', 1)->latest()->first()

# Force reset campaign
php artisan campaign:reset {campaign_id}

# View job queue
php artisan horizon:status

# Check failed jobs
php artisan queue:failed
```

### Log Locations

```
storage/logs/laravel.log          # General logs
storage/logs/campaigns.log        # Campaign-specific logs (if configured)
```

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-05 | GitHub Copilot | Initial documentation |
