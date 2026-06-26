---
layout: default
title: N10-Administrative-Legal JUMPSELLER INTEGRATION
---

# Jumpseller Integration - Technical Documentation

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [File Structure](#3-file-structure)
4. [Authentication](#4-authentication)
5. [API Integration](#5-api-integration)
6. [Multi-Phase Publishing](#6-multi-phase-publishing)
7. [Traits Documentation](#7-traits-documentation)
8. [Job Classes](#8-job-classes)
9. [Variant/Modifier Mapping](#9-variantmodifier-mapping)
10. [Order Management](#10-order-management)
11. [Webhook Handling](#11-webhook-handling)
12. [Error Handling](#12-error-handling)
13. [API Reference](#13-api-reference)

---

## 1. Overview

The **JumpsellerService** is a comprehensive e-commerce marketplace integration that enables bi-directional synchronization between the Dash platform and Jumpseller stores. It implements the `MarketplaceContract` interface and provides multi-phase publishing, order management, and webhook handling.

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **Multi-Phase Publishing** | Products → Variants → Images in separate phases |
| **Chunked Processing** | Process products in configurable batches |
| **Variant Mapping** | Map modifier groups to Jumpseller variants |
| **Order Synchronization** | Full order lifecycle management |
| **Webhook Integration** | Real-time order and inventory updates |

### Integration Characteristics

| Characteristic | Value |
|----------------|-------|
| Publishing Style | Multi-phase (product_data → variants → images) |
| Rate Limiting | 800 requests/minute, 20 requests/second |
| Authentication | HTTP Basic Auth (login + authtoken) |
| Data Format | REST API with JSON |
| Chunking Support | Yes (5 products/chunk) |

---

## 2. Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           JumpsellerService                                  │
│                     (implements MarketplaceContract)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          SERVICE TRAITS                              │   │
│  ├─────────────────┬─────────────────┬─────────────────┬───────────────┤   │
│  │ PublishService  │ PauseService    │ FinishService   │ DeleteService │   │
│  │ Methods         │ Methods         │ Methods         │ Methods       │   │
│  ├─────────────────┼─────────────────┼─────────────────┼───────────────┤   │
│  │ OrdersService   │ CategoryService │ Notification    │               │   │
│  │ Methods         │ Methods         │ ServiceMethods  │               │   │
│  └─────────────────┴─────────────────┴─────────────────┴───────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     PHASE-SPECIFIC JOBS                              │   │
│  ├─────────────────┬─────────────────┬─────────────────┬───────────────┤   │
│  │ BatchUpdate     │ BatchUpdate     │ BatchUpdate     │ BatchPause    │   │
│  │ ProductsJob     │ VariantsJob     │ ImagesJob       │ ProductsJob   │   │
│  ├─────────────────┼─────────────────┼─────────────────┼───────────────┤   │
│  │ BatchFinish     │ BatchDelete     │                 │               │   │
│  │ ProductsJob     │ ProductsJob     │                 │               │   │
│  └─────────────────┴─────────────────┴─────────────────┴───────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP Basic Auth
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         JUMPSELLER API                                       │
│                   https://api.jumpseller.com                                 │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│   Product Endpoints  │   Order Endpoints    │    Category Endpoints         │
│                      │                      │                               │
│ /products.json       │ /orders/{id}.json    │ /categories.json              │
│ /products/{id}.json  │ /fulfillments.json   │ /categories/{id}.json         │
│ /products/{id}/      │                      │                               │
│   variants.json      │                      │                               │
│ /products/{id}/      │                      │                               │
│   images.json        │                      │                               │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

### Multi-Phase Publishing Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    JUMPSELLER MULTI-PHASE PUBLISHING                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│ CampaignProcess │
│ Job             │
└────────┬────────┘
         │
         │ getProcessPhases('publish')
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Phases Configuration:                                                        │
│ ┌──────────────────┬─────────────────────┬─────────────────────────────────┐│
│ │ 'product_data'   │ 'variants'          │ 'images'                        ││
│ │ BatchUpdate      │ BatchUpdate         │ BatchUpdate                     ││
│ │ ProductsJob      │ VariantsJob         │ ImagesJob                       ││
│ └──────────────────┴─────────────────────┴─────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────────┘
         │
         │ Bus::chain([Phase1, Phase2, Phase3, CheckCompletion])
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  PHASE 1: product_data (BatchUpdateProductsJob)                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ • Validate products (price > 0, stock ≥ 0)                             │ │
│  │ • Check if product exists in Jumpseller (by SKU or ID)                 │ │
│  │ • Create new product OR update existing                                │ │
│  │ • Store Jumpseller product ID in marketplace_info                      │ │
│  │ • Set status → PUBLISHED                                               │ │
│  │ • Track progress via CampaignTrackerService                            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                          │                                                   │
│                          ▼                                                   │
│  PHASE 2: variants (BatchUpdateVariantsJob)                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ • Filter to products with marketplace_info (already published)         │ │
│  │ • Process modifier groups → Jumpseller variants                        │ │
│  │ • Generate SKU: {BASE_SKU}-{MODIFIER_GROUP_ID}-{OPTION_ID}             │ │
│  │ • Create/update/delete variants as needed                              │ │
│  │ • Track progress                                                       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                          │                                                   │
│                          ▼                                                   │
│  PHASE 3: images (BatchUpdateImagesJob)                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ • Filter to products with marketplace_info                             │ │
│  │ • Delete existing images from Jumpseller                               │ │
│  │ • Upload new images from product gallery                               │ │
│  │ • Use absolute AWS URLs                                                │ │
│  │ • Track progress                                                       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                          │                                                   │
│                          ▼                                                   │
│  CheckCampaignCompletionJob                                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ • Verify all phases completed                                          │ │
│  │ • Update campaign status                                               │ │
│  │ • Complete tracker                                                     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. File Structure

```
domain/app/Services/ECommerce/Marketplaces/Jumpseller/
├── JumpsellerService.php              # Main service class (~2966 lines)
│
├── OAuth/
│   └── OAuthClient.php                # Authentication handler
│
├── Jobs/
│   ├── BatchUpdateProductsJob.php     # Phase 1: product_data
│   ├── BatchUpdateVariantsJob.php     # Phase 2: variants
│   ├── BatchUpdateImagesJob.php       # Phase 3: images
│   ├── BatchPauseProductsJob.php      # Pause action
│   ├── BatchFinishProductsJob.php     # Finish action
│   └── BatchDeleteProductsJob.php     # Delete action
│
└── Traits/
    ├── PublishServiceMethods.php      # Publishing logic
    ├── PauseServiceMethods.php        # Pausing logic
    ├── FinishServiceMethods.php       # Finishing logic
    ├── DeleteServiceMethods.php       # Deletion logic
    ├── OrdersServiceMethods.php       # Order management
    ├── CategoryServiceMethods.php     # Category sync
    ├── NotificationServiceMethods.php # Email notifications
    └── JobsPhaseNotification.php      # Phase notification helpers
```

---

## 4. Authentication

### OAuth Client

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/OAuth/OAuthClient.php`

### Authentication Method

Jumpseller uses **HTTP Basic Authentication** with store login and API authtoken:

```php
$this->client = Http::baseUrl($jumpsellerApiUrl)
    ->acceptJson()
    ->withBasicAuth($this->login, $this->authToken);
```

### Configuration Constants

```php
public const OWN_TOKEN_ALLOWED = true;
public const CUSTOM_CONNECTION_ALLOWED = false;
public const CONNECTION_PARAMS_LOGIN_KEY = 'login';
public const CONNECTION_PARAMS_AUTH_TOKEN_KEY = 'authtoken';
public const CONNECTION_PARAMS_WEBHOOK_TOKEN = 'webhook_token';
```

### Connection Parameters Format

```php
[
    ['attribute' => 'connection_params.login', 'label' => 'LOGIN', 'required' => true],
    ['attribute' => 'connection_params.authtoken', 'label' => 'AUTH TOKEN', 'required' => true],
    ['attribute' => 'connection_params.webhook_token', 'label' => 'WEBHOOK TOKEN', 'required' => true],
]
```

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     JUMPSELLER AUTHENTICATION                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Store Setup   │    │   API Request   │    │   Jumpseller    │
│   in Dash       │───▶│   with Basic    │───▶│   API Server    │
│                 │    │   Auth Header   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                      │                      │
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Admin enters login + authtoken in marketplace settings       │
│ 2. Credentials stored in marketplace.connection_params          │
│ 3. Each API request includes:                                   │
│    Authorization: Basic base64(login:authtoken)                 │
│ 4. Jumpseller validates credentials                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. API Integration

### HTTP Client Setup

```php
protected function buildClient(): PendingRequest
{
    $login = $this->marketplace->connection_params['login'];
    $authToken = $this->marketplace->connection_params['authtoken'];
    $baseUrl = config('system_marketplaces.jumpseller.api_url', 'https://api.jumpseller.com');
    
    return Http::baseUrl($baseUrl)
        ->acceptJson()
        ->asJson()
        ->withBasicAuth($login, $authToken)
        ->timeout(60);
}
```

### Rate Limiting

| Limit | Value |
|-------|-------|
| Requests per minute | 800 |
| Requests per second | 20 |
| Built-in delay | 500ms between requests |

### Request Throttling

```php
protected function throttleRequest(): void
{
    // 500ms delay between requests to avoid rate limiting
    usleep(500000);
}
```

### Error Response Handling

```php
protected function handleApiError(Response $response, string $operation): void
{
    $statusCode = $response->status();
    $body = $response->json();
    
    if ($statusCode === 429) {
        // Rate limited - wait and retry
        sleep(5);
        throw new \Exception('Rate limited, please retry');
    }
    
    if ($statusCode === 404) {
        // Resource not found - may be acceptable for delete operations
        Log::warning("Jumpseller {$operation}: Resource not found", ['response' => $body]);
        return;
    }
    
    if ($statusCode >= 400) {
        throw new \Exception("Jumpseller {$operation} failed: " . json_encode($body));
    }
}
```

---

## 6. Multi-Phase Publishing

### Phases Configuration

```php
public static function getProcessPhases(string $action = 'publish'): array
{
    return match($action) {
        'pause' => [
            'processing' => BatchPauseProductsJob::class
        ],
        'finish' => [
            'processing' => BatchFinishProductsJob::class
        ],
        'delete' => [
            'processing' => BatchDeleteProductsJob::class
        ],
        'publish', 'republish' => [
            'product_data' => BatchUpdateProductsJob::class,
            'variants' => BatchUpdateVariantsJob::class,
            'images' => BatchUpdateImagesJob::class
        ],
        default => [
            'processing' => PublishProductsJob::class
        ]
    };
}
```

### Chunking Configuration

```php
public function shouldUseChunking(): bool
{
    return true;
}

public function getChunkSize(): int
{
    return 5; // Process 5 products per chunk
}
```

### Task Calculation

```php
public function calculateTasksForProducts($products): int
{
    // Each product requires: 1 (product) + 1 (variants) + 1 (images) = 3 tasks
    return $products->count() * 3;
}
```

### Phase Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       PUBLISHING SEQUENCE                                     │
└──────────────────────────────────────────────────────────────────────────────┘

                    CHUNK 1 (5 products)
                    ┌───────────────────┐
                    │ BatchUpdateProduc │ Phase: product_data
                    │ tsJob             │ Progress: 0-33%
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ BatchUpdateVarian │ Phase: variants
                    │ tsJob             │ Progress: 34-66%
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ BatchUpdateImages │ Phase: images
                    │ Job               │ Progress: 67-100%
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ CheckCampaignComp │
                    │ letionJob         │
                    └───────────────────┘


Progress Tracking (via CampaignTrackerService):

┌────────────────────────────────────────────────────────────────────────────┐
│ tracker.phases_status = {                                                  │
│   "product_data": {                                                        │
│     "status": "completed",                                                 │
│     "progress": 100.00,                                                    │
│     "total_items": 5,                                                      │
│     "processed_items": 5,                                                  │
│     "successful_items": 5,                                                 │
│     "failed_items": 0                                                      │
│   },                                                                       │
│   "variants": {                                                            │
│     "status": "in_progress",                                               │
│     "progress": 60.00,                                                     │
│     "total_items": 5,                                                      │
│     "processed_items": 3,                                                  │
│     "successful_items": 3,                                                 │
│     "failed_items": 0                                                      │
│   },                                                                       │
│   "images": {                                                              │
│     "status": "pending",                                                   │
│     "progress": 0.00,                                                      │
│     "total_items": 5,                                                      │
│     "processed_items": 0                                                   │
│   }                                                                        │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Traits Documentation

### 7.1 PublishServiceMethods

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Traits/PublishServiceMethods.php`

| Method | Signature | Description |
|--------|-----------|-------------|
| `publishProducts()` | `($user, $cmps, ...)` | Main publish entry point |
| `processIndividualProduct()` | `(CampaignMarketplaceProduct)` | Process single product |
| `createNewProduct()` | `(CampaignMarketplaceProduct)` | Create new product in Jumpseller |
| `publishProduct()` | `($cmp, $product, $dataOnly)` | Execute publish API call |

**Key Features:**
- Checks if product exists before deciding create/update
- Handles variants with proper Jumpseller format
- Uploads images with absolute URLs
- Updates `marketplace_info` with Jumpseller product ID and permalink

**Create Product Flow:**

```php
protected function createNewProduct(CampaignMarketplaceProduct $cmp): void
{
    $product = $cmp->product;
    $formattedProduct = $this->parseProduct($cmp, $product);
    
    // API call to create product
    $response = $this->client->post('/products.json', [
        'product' => $formattedProduct
    ]);
    
    if ($response->successful()) {
        $jumpsellerProduct = $response->json()['product'];
        
        // Store marketplace info
        $cmp->update([
            'status' => CampaignMarketplaceProduct::STATUS_PUBLISHED,
            'marketplace_info' => [
                'id' => $jumpsellerProduct['id'],
                'permalink' => $jumpsellerProduct['permalink'],
                'published_at' => now()->toISOString()
            ]
        ]);
    }
}
```

### 7.2 PauseServiceMethods

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Traits/PauseServiceMethods.php`

| Method | Signature | Description |
|--------|-----------|-------------|
| `pauseProducts()` | `($user, $cmps, ...)` | Main pause entry point |
| `processIndividualProductPause()` | `(CampaignMarketplaceProduct)` | Process single pause |
| `pauseExistingProduct()` | `(CampaignMarketplaceProduct)` | Pause in marketplace |
| `pauseProductInMarketplace()` | `(CampaignMarketplaceProduct)` | API call to set `not-available` |
| `updateTrackerProgress()` | `($trackerId, $phase, ...)` | Track progress |

**Implementation:**

```php
protected function pauseProductInMarketplace(CampaignMarketplaceProduct $cmp): array
{
    $productId = $cmp->marketplace_info['id'];
    
    $response = $this->client->put("/products/{$productId}.json", [
        'product' => [
            'status' => 'not-available'
        ]
    ]);
    
    if ($response->successful()) {
        $cmp->update([
            'status' => CampaignMarketplaceProduct::STATUS_PAUSED
        ]);
    }
    
    return $response->json();
}
```

### 7.3 FinishServiceMethods

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Traits/FinishServiceMethods.php`

| Method | Signature | Description |
|--------|-----------|-------------|
| `finishProducts()` | `($user, $cmps, ...)` | Main finish entry point |
| `finishProductInMarketplace()` | `(CampaignMarketplaceProduct)` | Delete from Jumpseller |

**Implementation:**
- Attempts to delete product from Jumpseller via API
- Handles 404 responses gracefully (product already deleted)
- **Always** sets status to `FINISHED` regardless of API result
- Clears `marketplace_info`

```php
protected function finishProductInMarketplace(CampaignMarketplaceProduct $cmp): array
{
    $productId = $cmp->marketplace_info['id'] ?? null;
    
    if ($productId) {
        try {
            $response = $this->client->delete("/products/{$productId}.json");
        } catch (\Exception $e) {
            // Log but continue - product may already be deleted
            Log::warning("Jumpseller product delete failed", ['error' => $e->getMessage()]);
        }
    }
    
    // Always mark as finished
    $cmp->update([
        'status' => CampaignMarketplaceProduct::STATUS_FINISHED,
        'marketplace_info' => null
    ]);
    
    return ['success' => true];
}
```

### 7.4 DeleteServiceMethods

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Traits/DeleteServiceMethods.php`

| Method | Signature | Description |
|--------|-----------|-------------|
| `deleteProducts()` | `($user, $cmps, ..., $deleteFromCampaign)` | Main delete entry point |
| `deleteProductFromMarketplace()` | `(CampaignMarketplaceProduct)` | API deletion + record cleanup |
| `deleteProductImages()` | `(string $productId)` | Delete all product images |

**Two Modes:**
1. `deleteFromCampaign = false`: Deletes from Jumpseller, sets status to `PENDING`
2. `deleteFromCampaign = true`: Deletes from Jumpseller AND deletes database record

### 7.5 OrdersServiceMethods

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Traits/OrdersServiceMethods.php`

| Method | Signature | Description |
|--------|-----------|-------------|
| `updateOrderStatus()` | `($tab, $orderId, $status, $payload)` | Update order in Jumpseller |
| `handleFulfillmentStatusUpdate()` | `($orderId, $status, $payload)` | Create/update fulfillments |
| `confirmOrder()` | `(array $payload)` | Confirm order (no-op for Jumpseller) |
| `rejectOrder()` | `(array $payload)` | Cancel order in Jumpseller |
| `getOrderStatus()` | `(string $orderId)` | Fetch order status |
| `handleOrderPaid()` | `(array $payload)` | Webhook: creates order + tab |
| `handleOrderCanceled()` | `(array $payload)` | Webhook: cancels order |

**Order Status Mapping:**

```php
// Internal Status → Jumpseller Status
$statusMapping = [
    Order::STATUS_CREATED => 'requested',
    Order::STATUS_PAID => 'requested',
    Order::STATUS_IN_PREPARATION => 'requested',
    Order::STATUS_PREPARED => 'pickup_available', // fulfillment
    Order::STATUS_PREPARED => 'requested',        // shipment
    Order::STATUS_PICKED_UP => 'in_transit',
    Order::STATUS_SHIPPED => 'delivered',
    Order::STATUS_RETURNED => 'failed'
];
```

### 7.6 CategoryServiceMethods

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Traits/CategoryServiceMethods.php`

| Method | Signature | Description |
|--------|-----------|-------------|
| `findCategoryByName()` | `(string $name)` | Search Jumpseller categories |
| `createCategory()` | `(string $name)` | Create new category |
| `parseCategories()` | `(Product $product)` | Get category IDs for product |
| `getCategoryIds()` | `(Product $product)` | Get/create category mapping |
| `ensureCategoriesExist()` | `(array $names)` | Create categories if needed |
| `verifyCategories()` | `(array $ids)` | Verify categories exist |

### 7.7 NotificationServiceMethods

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Traits/NotificationServiceMethods.php`

| Method | Signature | Description |
|--------|-----------|-------------|
| `notifyOrderUpdate()` | `(Order $order)` | Send email notification to customer |
| `getStatusDisplay()` | `(string $status)` | Returns Spanish status label |

**Notification Logic:**
- Skips notifications for `CREATED`, `PREPARED`, `NOT_SHIPPED`, `CLOSED`
- Special handling for `CLOSED` status: sends `SHIPPED` if delivered, `CANCELLED` if not
- Uses `MarketplaceOrderUpdateMail` mailable

---

## 8. Job Classes

### 8.1 BatchUpdateProductsJob

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Jobs/BatchUpdateProductsJob.php`

**Phase:** `product_data`

**Purpose:** Creates/updates basic product information in Jumpseller

**Flow:**
```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     BatchUpdateProductsJob Flow                               │
└──────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐
│   handle()  │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. Get marketplace service instance                                          │
└──────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 2. Start tracker phase                                                       │
│    CampaignTrackerService::startPhase($trackerId, 'product_data')            │
└──────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 3. Validate products                                                         │
│    - Price > 0                                                               │
│    - Stock ≥ 0 (or allowZeroStock)                                           │
└──────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 4. For each valid product:                                                   │
│    a. Check if exists in Jumpseller (by marketplace_info.id or SKU)          │
│    b. If exists: PUT /products/{id}.json                                     │
│    c. If new: POST /products.json                                            │
│    d. Update marketplace_info with Jumpseller ID                             │
│    e. Set status = PUBLISHED                                                 │
└──────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 5. Update tracker progress                                                   │
│    CampaignTrackerService::updatePhaseProgress($trackerId, 'product_data',   │
│                                                $processed, $success, $fail)  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 BatchUpdateVariantsJob

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Jobs/BatchUpdateVariantsJob.php`

**Phase:** `variants`

**Purpose:** Updates product variants (modifier groups → Jumpseller variants)

**Key Logic:**

```php
protected function processVariants($existingProducts): void
{
    foreach ($existingProducts as $cmp) {
        try {
            $service->updateProductVariantsOnly($cmp);
            $this->updateTrackerProgress($trackerId, 'variants', $processed++, $success++, $failed);
        } catch (\Exception $e) {
            $this->updateTrackerProgress($trackerId, 'variants', $processed++, $success, ++$failed);
        }
    }
}
```

### 8.3 BatchUpdateImagesJob

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Jobs/BatchUpdateImagesJob.php`

**Phase:** `images`

**Purpose:** Uploads/replaces product images

**Flow:**
1. Filter to products with `marketplace_info`
2. Delete existing images from Jumpseller
3. Upload new images with absolute URLs
4. Track progress

### 8.4 BatchPauseProductsJob

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Jobs/BatchPauseProductsJob.php`

**Phase:** `processing`

**Purpose:** Pauses products in Jumpseller by setting status to `not-available`

### 8.5 BatchFinishProductsJob

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Jobs/BatchFinishProductsJob.php`

**Phase:** `processing`

**Purpose:** Deletes products from Jumpseller

**Key Feature:** Uses `CampaignTrackerService::updatePhaseProgress()` directly

```php
// Line 68-69
CampaignTrackerService::updatePhaseProgress(
    $this->trackerId,
    $this->phase,
    $processed,
    $successful,
    $failed
);
```

### 8.6 BatchDeleteProductsJob

**Location:** `domain/app/Services/ECommerce/Marketplaces/Jumpseller/Jobs/BatchDeleteProductsJob.php`

**Phase:** `processing`

**Purpose:** Complete product deletion with optional campaign removal

---

## 9. Variant/Modifier Mapping

### SKU Format

```
{BASE_SKU}-{MODIFIER_GROUP_ID}-{OPTION_ID}
Example: PROD001-5-12
```

### Modifier to Variant Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODIFIER GROUP → VARIANT MAPPING                          │
└─────────────────────────────────────────────────────────────────────────────┘

Dash Product (with Modifier Groups):
┌──────────────────────────────────────────────────────────────────────────────┐
│ Product: "Pizza Margarita"                                                   │
│ SKU: "PIZZA001"                                                              │
│ Price: $12.00                                                                │
│                                                                              │
│ Modifier Group: "Size" (id: 5)                                               │
│   ├── Option: "Small" (id: 10) - price_adjustment: -$2.00                    │
│   ├── Option: "Medium" (id: 11) - price_adjustment: $0.00                    │
│   └── Option: "Large" (id: 12) - price_adjustment: +$3.00                    │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ generateEnhancedVariants()
                                    ▼
Jumpseller Variants:
┌──────────────────────────────────────────────────────────────────────────────┐
│ Variant 1:                                                                   │
│   SKU: "PIZZA001-5-10"                                                       │
│   Price: $10.00                                                              │
│   Options: [{name: "Size", value: "Small"}]                                  │
│   Metadata: {modifier_group_id: 5, modifier_option_id: 10}                   │
│                                                                              │
│ Variant 2:                                                                   │
│   SKU: "PIZZA001-5-11"                                                       │
│   Price: $12.00                                                              │
│   Options: [{name: "Size", value: "Medium"}]                                 │
│   Metadata: {modifier_group_id: 5, modifier_option_id: 11}                   │
│                                                                              │
│ Variant 3:                                                                   │
│   SKU: "PIZZA001-5-12"                                                       │
│   Price: $15.00                                                              │
│   Options: [{name: "Size", value: "Large"}]                                  │
│   Metadata: {modifier_group_id: 5, modifier_option_id: 12}                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Variant Generation Code

```php
private function generateEnhancedVariants($campaignMarketplace, $product, $modifierGroups, $formattedProduct): array
{
    $variants = [];
    $baseSku = $product->sku;
    $basePriceValue = floatval($formattedProduct['price']);
    $stockValue = $product->infinite_stock ? 0 : $product->stock;
    
    foreach ($modifierGroups as $modifierGroup) {
        foreach ($modifierGroup->options as $index => $option) {
            $variantSku = $baseSku . '-' . $modifierGroup->id . '-' . $option->id;
            $variantPrice = $basePriceValue + floatval($option->price_adjustment ?? 0);
            
            $variant = [
                'sku' => $variantSku,
                'price' => $variantPrice,
                'stock' => $stockValue,
                'stock_unlimited' => $product->infinite_stock,
                'options' => [
                    [
                        'name' => $modifierGroup->name,
                        'option_type' => 'option',
                        'value' => $option->name,
                        'product_option_position' => 1,
                        'product_value_position' => $index
                    ]
                ],
                'metadata' => [
                    'modifier_group_id' => $modifierGroup->id,
                    'modifier_option_id' => $option->id,
                ]
            ];
            
            $variants[] = $variant;
        }
    }
    
    return $variants;
}
```

### Jumpseller Variant API Format

```php
$formattedVariant = [
    'sku' => $variantSku,
    'price' => $variantPrice,
    'stock' => $stock,
    'stock_unlimited' => $isUnlimited,
    'options' => [
        [
            'name' => $groupName,          // e.g., "Size"
            'option_type' => 'option',
            'value' => $optionValue,       // e.g., "Large"
            'product_option_position' => $position,
            'product_value_position' => $index
        ]
    ]
];
```

---

## 10. Order Management

### Order Creation Flow (Webhook)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ORDER_PAID WEBHOOK FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│ Webhook:        │
│ order_paid      │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. Verify webhook authenticity (HMAC)                                        │
│    $calculatedHmac = base64_encode(hash_hmac('sha256', $data, $token, true)) │
│    hash_equals($hmacHeader, $calculatedHmac)                                 │
└──────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 2. Check if order already exists                                             │
│    Order::where('source_id', $jumpsellerOrderId)->first()                    │
└──────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 3. Create Order record                                                       │
│    - source_id = Jumpseller order ID                                         │
│    - status = PAID                                                           │
│    - brokerable_type = Marketplace::class                                    │
│    - brokerable_id = $marketplace->id                                        │
└──────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 4. Process order products                                                    │
│    For each product in webhook:                                              │
│    a. Match SKU (including variant SKU support)                              │
│    b. Create OrderProduct record                                             │
│    c. If variant: Create OrderProductModifier records                        │
└──────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 5. Create Tab for order                                                      │
│    Links order to POS system for kitchen/service tracking                    │
└──────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 6. Create initial fulfillment (for delivery orders)                          │
│    POST /fulfillments.json                                                   │
└──────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 7. Send WebSocket notification                                               │
│    Notify frontend of new order                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Order Status Update Flow

```php
public function updateOrderStatus(Tab $tab, string $orderId, string $status, array $payload = []): array
{
    $order = $tab->order;
    $jumpsellerStatus = $this->mapStatusToJumpseller($status);
    
    // Update order in Jumpseller
    $response = $this->client->put("/orders/{$orderId}.json", [
        'order' => [
            'status' => $jumpsellerStatus
        ]
    ]);
    
    // Handle fulfillment updates if needed
    if (in_array($status, ['prepared', 'shipped', 'delivered'])) {
        $this->handleFulfillmentStatusUpdate($orderId, $status, $payload);
    }
    
    // Send customer notification
    $this->notifyOrderUpdate($order);
    
    return $response->json();
}
```

### Fulfillment Status Mapping

```php
$fulfillmentStatusMapping = [
    'prepared' => 'pickup_available',    // For pickup orders
    'shipped' => 'in_transit',           // For delivery orders
    'delivered' => 'delivered',
    'returned' => 'failed'
];
```

---

## 11. Webhook Handling

### Supported Webhooks

| Webhook Type | Handler Method | Description |
|--------------|----------------|-------------|
| `order_paid` | `handleOrderPaid()` | Creates order + tab |
| `order_canceled` | `handleOrderCanceled()` | Cancels order + restores stock |
| `product_created` | `handleProductCreated()` | Logs external product creation |
| `product_updated` | `handleProductUpdated()` | Syncs stock changes |

### Webhook Authentication

```php
private function verifyWebhookAuthenticity(string $data, string $hmacHeader): bool
{
    $webhookToken = $this->marketplace->connection_params['webhook_token'];
    $calculatedHmac = base64_encode(hash_hmac('sha256', $data, $webhookToken, true));
    return hash_equals($hmacHeader, $calculatedHmac);
}
```

### Webhook Payload Example (order_paid)

```json
{
  "webhook_type": "order_paid",
  "order": {
    "id": 123456,
    "status": "paid",
    "total": 25.99,
    "subtotal": 23.99,
    "shipping": 2.00,
    "tax": 0,
    "currency": "CLP",
    "customer": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+56912345678"
    },
    "shipping_address": {
      "street": "123 Main St",
      "city": "Santiago",
      "country": "Chile"
    },
    "products": [
      {
        "id": 789,
        "sku": "PROD001",
        "name": "Product Name",
        "quantity": 2,
        "price": 11.99,
        "variant_id": 456,
        "variant_sku": "PROD001-5-12"
      }
    ]
  }
}
```

### Main Webhook Handler

```php
public function handleWebhook(string $type, array $payload): array
{
    return match($type) {
        'order_paid' => $this->handleOrderPaid($payload),
        'order_canceled' => $this->handleOrderCanceled($payload),
        'product_created' => $this->handleProductCreated($payload),
        'product_updated' => $this->handleProductUpdated($payload),
        default => ['status' => 'unhandled', 'type' => $type]
    };
}
```

---

## 12. Error Handling

### Error Handling Strategy

| Strategy | Description |
|----------|-------------|
| **Graceful degradation** | Continue processing other products on single failures |
| **404 handling** | Treat as success for delete/finish operations |
| **Status updates** | Set `ERRORED` status with error message |
| **Comprehensive logging** | Log all API calls and errors |

### Error Status Flow

```php
try {
    // API operation
    $response = $this->client->post('/products.json', $data);
    
    if (!$response->successful()) {
        throw new \Exception($response->body());
    }
    
    $cmp->update(['status' => CampaignMarketplaceProduct::STATUS_PUBLISHED]);
    
} catch (\Exception $e) {
    Log::error('Jumpseller publish failed', [
        'product_id' => $cmp->product_id,
        'error' => $e->getMessage()
    ]);
    
    $cmp->update([
        'status' => CampaignMarketplaceProduct::STATUS_ERRORED,
        'error_message' => $e->getMessage()
    ]);
    
    if ($shouldThrowErrors) {
        throw $e;
    }
}
```

### 404 Handling for Delete/Finish

```php
protected function finishProductInMarketplace(CampaignMarketplaceProduct $cmp): array
{
    $productId = $cmp->marketplace_info['id'] ?? null;
    
    if ($productId) {
        $response = $this->client->delete("/products/{$productId}.json");
        
        // 404 is acceptable - product already deleted
        if ($response->status() === 404) {
            Log::info('Jumpseller product already deleted', ['id' => $productId]);
        } elseif (!$response->successful()) {
            Log::warning('Jumpseller delete failed', [
                'id' => $productId,
                'status' => $response->status()
            ]);
        }
    }
    
    // Always mark as finished regardless of API result
    $cmp->update([
        'status' => CampaignMarketplaceProduct::STATUS_FINISHED,
        'marketplace_info' => null
    ]);
    
    return ['success' => true];
}
```

---

## 13. API Reference

### Product Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List products | GET | `/products.json` |
| Get product | GET | `/products/{id}.json` |
| Create product | POST | `/products.json` |
| Update product | PUT | `/products/{id}.json` |
| Delete product | DELETE | `/products/{id}.json` |

### Variant Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List variants | GET | `/products/{id}/variants.json` |
| Get variant | GET | `/products/{id}/variants/{vid}.json` |
| Create variant | POST | `/products/{id}/variants.json` |
| Update variant | PUT | `/products/{id}/variants/{vid}.json` |
| Delete variant | DELETE | `/products/{id}/variants/{vid}.json` |

### Image Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List images | GET | `/products/{id}/images.json` |
| Upload image | POST | `/products/{id}/images.json` |
| Delete image | DELETE | `/products/{id}/images/{iid}.json` |

### Category Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List categories | GET | `/categories.json` |
| Get category | GET | `/categories/{id}.json` |
| Create category | POST | `/categories.json` |

### Order Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List orders | GET | `/orders.json` |
| Get order | GET | `/orders/{id}.json` |
| Update order | PUT | `/orders/{id}.json` |

### Fulfillment Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List fulfillments | GET | `/orders/{id}/fulfillments.json` |
| Create fulfillment | POST | `/fulfillments.json` |
| Update fulfillment | PUT | `/fulfillments/{id}.json` |

### Product Request Format

```json
{
  "product": {
    "name": "Product Name",
    "sku": "PROD001",
    "price": 19.99,
    "stock": 100,
    "stock_unlimited": false,
    "status": "available",
    "description": "Product description",
    "categories": [1, 2, 3],
    "weight": 0.5,
    "dimensions": {
      "length": 10,
      "width": 5,
      "height": 3
    }
  }
}
```

### Variant Request Format

```json
{
  "variant": {
    "sku": "PROD001-LARGE",
    "price": 24.99,
    "stock": 50,
    "stock_unlimited": false,
    "options": [
      {
        "name": "Size",
        "option_type": "option",
        "value": "Large",
        "product_option_position": 1,
        "product_value_position": 2
      }
    ]
  }
}
```

### Image Request Format

```json
{
  "image": {
    "url": "https://cdn.example.com/images/product.jpg"
  }
}
```

---

## Related Documentation

- [Marketplace Service Overview](./MARKETPLACE_SERVICE_OVERVIEW.md)
- [Uber Integration Documentation](./UBER_INTEGRATION.md)

---

*Last Updated: December 2024*
