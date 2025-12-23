# Product Import System - Technical Documentation

## Overview

The Dash Backend provides a robust product import system that supports two distinct import mechanisms:

1. **Normalized Import**: Uses a standardized Excel format with predefined columns
2. **Template Import**: Uses configurable ProductTemplate mappings for flexible column definitions

Both mechanisms are designed to work consistently, sharing architectural patterns for status management, notifications, and error handling.

---

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRODUCT IMPORT FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
  │   Frontend   │──────▶│ ProductCon-  │──────▶│   Import     │
  │   Upload     │       │ troller::    │       │    Job       │
  │   File       │       │ import()     │       │              │
  └──────────────┘       └──────────────┘       └──────┬───────┘
                                                       │
                         ┌─────────────────────────────┼─────────────────────┐
                         │                             │                     │
                         ▼                             ▼                     ▼
                  ┌──────────────┐            ┌──────────────┐       ┌──────────────┐
                  │ Normalized   │            │   Template   │       │ ProductImport│
                  │ Import Job   │            │ Import Job   │       │ Instance     │
                  │              │            │              │       │ (Status)     │
                  └──────────────┘            └──────────────┘       └──────────────┘
```

### Key Components

| Component | Path | Purpose |
|-----------|------|---------|
| `ProductController` | `domain/app/Http/Controllers/API/ECommerce/ProductController.php` | Handles import API endpoint |
| `ImportNormalizedProductsJob` | `domain/app/Jobs/Imports/ImportNormalizedProductsJob.php` | Processes normalized Excel imports |
| `ImportProductsJob` | `domain/app/Jobs/ECommerce/ImportProductsJob.php` | Processes template-based imports |
| `ProductImportInstance` | `domain/app/Models/ECommerce/ProductImportInstance.php` | Tracks import status and data |
| `ImportMechanismRegistry` | `domain/app/Services/ECommerce/Imports/ImportMechanismRegistry.php` | Registry for import mechanisms |

---

## Import Mechanisms

### 1. Normalized Import

The normalized import expects an Excel file with standardized columns:

- `sku` (required) - Product SKU
- `name` - Product name
- `description` - Product description
- `category` - Category identifier
- `brand` - Brand identifier
- `price` - Product price
- `stock` - Stock quantity
- Additional columns for prices/stocks per pricelist/stocktype

**Job Class**: `ImportNormalizedProductsJob`

**Features**:
- ShouldBeUnique implementation prevents concurrent imports
- Structured notification types (started, progress, completed, failed)
- Timeout handling via `timeoutJob()` method
- Centralized error handling via `handleJobFailure()`
- Log saving for debugging

### 2. Template Import

The template import uses `ProductTemplate` configurations to map Excel columns to product fields:

- Flexible column mapping via `ProductTemplateColumn`
- Supports relationable columns (Pricelist, StockType, MetadataFormat, Marketplace)
- Works with both Excel files and JSON data

**Job Class**: `ImportProductsJob`

**Features**:
- ShouldBeUnique implementation prevents concurrent imports
- Structured notification types aligned with normalized import
- Centralized status management via `updateImportStatus()`
- Unified notification sending via `sendNotification()`
- Error categorization for user-friendly messages

---

## Status Management

### ProductImportInstance Statuses

| Status | Constant | Description |
|--------|----------|-------------|
| `preview_initiated` | `STATUS_PREVIEW_INITIATED` | Preview validation started |
| `preview_completed` | `STATUS_PREVIEW_COMPLETED` | Preview validation finished successfully |
| `preview_failed` | `STATUS_PREVIEW_FAILED` | Preview validation failed |
| `import_initiated` | `STATUS_IMPORT_INITIATED` | Import started |
| `import_completed` | `STATUS_IMPORT_COMPLETED` | Import finished successfully |
| `import_failed` | `STATUS_IMPORT_FAILED` | Import failed |

### Status Flow

```
                    PREVIEW MODE                          IMPORT MODE
                    ────────────                          ───────────
                         │                                     │
                         ▼                                     ▼
              ┌──────────────────┐                  ┌──────────────────┐
              │ PREVIEW_INITIATED│                  │ IMPORT_INITIATED │
              └────────┬─────────┘                  └────────┬─────────┘
                       │                                     │
           ┌───────────┴───────────┐             ┌───────────┴───────────┐
           │                       │             │                       │
           ▼                       ▼             ▼                       ▼
┌──────────────────┐   ┌──────────────────┐  ┌──────────────────┐   ┌──────────────────┐
│ PREVIEW_COMPLETED│   │  PREVIEW_FAILED  │  │ IMPORT_COMPLETED │   │   IMPORT_FAILED  │
└──────────────────┘   └──────────────────┘  └──────────────────┘   └──────────────────┘
```

---

## Notification System

### Notification Types

| Type | Constant | Description |
|------|----------|-------------|
| `import.started` | `NOTIFICATION_TYPE_STARTED` | Import process has begun |
| `import.progress` | `NOTIFICATION_TYPE_PROGRESS` | Progress update during import |
| `import.completed` | `NOTIFICATION_TYPE_COMPLETED` | Import finished successfully |
| `import.failed` | `NOTIFICATION_TYPE_FAILED` | Import failed with error |

### Notification Data Structure

```php
[
    'type' => 'import.progress',           // Notification type
    'message' => 'Processing...',          // Human-readable message
    'phase' => 'ImportingProductData',     // Current phase name
    'phaseNumber' => 1,                    // Current phase number (1-based)
    'totalPhases' => 5,                    // Total number of phases
    'processedItems' => 50,                // Items processed in current phase
    'totalItems' => 100,                   // Total items in current phase
    'percentage' => 50,                    // Progress percentage
    'productImportInstanceId' => 123,      // Import instance ID
    'tenantId' => 1,                       // Tenant ID
    'tenantName' => 'My Store',            // Tenant name
    'mode' => 'import',                    // 'preview' or 'import'
    'timestamp' => '2024-01-15T12:00:00Z', // ISO timestamp
]
```

### Notification Classes

| Class | Purpose |
|-------|---------|
| `ProductImportProgressNotification` | Progress updates during import |
| `ProductImportNotification` | Completion notification with log data |
| `ProductImportErrorNotification` | Error notification with details |
| `NormalizedImportProgressNotification` | Normalized import progress (extends base) |

---

## Import Phases

Both import mechanisms follow these phases:

### Template Import Phases

| Phase | Constant | Description |
|-------|----------|-------------|
| 1 | `ImportingProductData` | Create/update product records |
| 2 | `ImportingPrices` | Update product prices per pricelist |
| 3 | `ImportingStocks` | Update product stocks per stock type |
| 4 | `UpdatingPackStocks` | Recalculate pack product stocks |
| 5 | `UpdatingMetadata` | Update product metadata values |

### Normalized Import Phases

| Phase | Constant | Description |
|-------|----------|-------------|
| 1 | `Validating` | Validate import data |
| 2 | `ImportingProducts` | Create/update products |
| 3 | `ImportingPrices` | Update prices |
| 4 | `ImportingStocks` | Update stocks |
| 5 | `ImportingMedia` | Process product images |
| 6 | `Finalizing` | Cleanup and finalization |

---

## Error Handling

### Error Types

| Error Type | Description | User Message |
|------------|-------------|--------------|
| `missing_category` | No primary category configured | Configuration error message |
| `missing_brand` | No primary brand configured | Configuration error message |
| `database_constraint` | Required field is null | Data validation message |
| `file_not_found` | Import file doesn't exist | File error message |
| `timeout` | Job exceeded timeout | Timeout message |
| `general` | Other errors | Generic error with details |

### Error Handling Flow

```php
// In handleJobFailure()
protected function handleJobFailure($exception, string $mode): void
{
    // 1. Update status to failed
    $this->updateImportStatus($mode, 'failed');
    
    // 2. Save error log to import instance
    $this->saveLog($exception);
    
    // 3. Send failure notification with user-friendly message
    $this->notifyError($exception);
}
```

---

## Job Uniqueness

Both jobs implement `ShouldBeUnique` to prevent concurrent imports:

```php
// Template Import
public function uniqueId(): string
{
    return 'template_import_' . $this->productImportInstance->id . '_' . $mode;
}

// Normalized Import
public function uniqueId(): string
{
    return 'normalized_import_' . $this->productImportInstance->id . '_' . $mode;
}
```

The unique lock is maintained for 3600 seconds (1 hour) by default.

---

## Timeout Handling

Both jobs have timeout handling:

```php
public $timeout = 2600; // ~43 minutes

public function timeoutJob()
{
    $exception = new Exception("Import job timeout after {$this->timeout} seconds");
    $this->handleJobFailure($exception, $mode);
}
```

---

## User Resolution

The jobs resolve the user from multiple sources for notification targeting:

```php
protected function getUser(): ?User
{
    // 1. Check if user is already a User instance
    if ($this->user instanceof User) {
        return $this->user;
    }

    // 2. Try to load from userId
    if ($this->userId) {
        $user = User::find($this->userId);
        if ($user) return $user;
    }

    // 3. Try to load from ProductImportInstance
    if ($this->productImportInstance?->user_id) {
        $user = User::find($this->productImportInstance->user_id);
        if ($user) return $user;
    }

    return null;
}
```

---

## API Endpoint

### POST /api/ecommerce/products/import

**Request Body**:

```json
{
    "import_type": "template",     // or "normalized"
    "file": "[binary]",            // Excel file
    "product_template_id": 123,    // Required for template imports
    "preview": false               // Optional: run in preview mode
}
```

**Response**:

```json
{
    "success": true,
    "message": "Import job dispatched",
    "data": {
        "import_instance_id": 456,
        "status": "import_initiated"
    }
}
```

---

## File Storage

Import files are stored on configured disks with this fallback order:

1. Stored disk from import instance options (`storage_disk`)
2. `s3-private`
3. `local`
4. `s3`

Files are cleaned up after successful import completion.

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `QUEUE_IMPORTJOB_TIMEOUT` | 2600 | Job timeout in seconds |

### Tenant Settings

| Setting | Description |
|---------|-------------|
| `SETTING_IMPORTED_ITEMS_NOTIFICATIONS_INTERVAL` | Notify every N items |

---

## Database Schema

### product_import_instances

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | Primary key |
| `user_id` | uuid | User who initiated import |
| `tenant_id` | bigint | Tenant ID |
| `product_template_id` | bigint | Template ID (for template imports) |
| `filepath` | string | Path to import file |
| `status` | enum | Current status |
| `options` | json | Import options (storage_disk, etc.) |
| `log` | json | Import log with results/errors |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Last update timestamp |

---

## Extending the System

### Adding a New Import Mechanism

1. Create a new mechanism class in `domain/app/Services/ECommerce/Imports/`:

```php
class CustomImportMechanism extends BaseImportMechanism
{
    public function processImport(ProductImportInstance $instance): void
    {
        // Your import logic
    }
}
```

2. Register in `ImportMechanismRegistry`:

```php
protected static array $mechanisms = [
    'normalized' => NormalizedImportMechanism::class,
    'template' => TemplateImportMechanism::class,
    'custom' => CustomImportMechanism::class,
];
```

3. Create a corresponding job class following the architecture patterns.

---

## Best Practices

1. **Always use the centralized methods**:
   - `updateImportStatus()` for status changes
   - `sendNotification()` for notifications
   - `handleJobFailure()` for error handling

2. **Maintain notification consistency**:
   - Use the defined notification type constants
   - Include all required fields in notification data

3. **Handle user resolution properly**:
   - Use `getUser()` instead of `$this->user` directly
   - Handle cases where user may not be available

4. **Log appropriately**:
   - Log at INFO level for normal operations
   - Log at ERROR level for exceptions
   - Include relevant context (instance_id, tenant_id, etc.)

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "No primary category found" | Tenant has no primary category | Set `is_primary=true` on a category |
| "No primary brand found" | Tenant has no primary brand | Set `is_primary=true` on a brand |
| "File does not exist" | File not found on any disk | Check file storage configuration |
| Import stuck | Job not processing | Check queue worker status |
| No notifications | User not resolvable | Ensure user_id is set on instance |

### Debugging

1. Check Laravel logs for import job output
2. Query `product_import_instances` table for status
3. Check `log` column for error details
4. Monitor queue with `artisan queue:monitor`

---

## Related Files

- `domain/app/Jobs/ECommerce/ValidateProductsToImportJob.php` - Validation sub-job
- `domain/app/Models/ECommerce/ProductTemplate.php` - Template configuration
- `domain/app/Models/ECommerce/ProductTemplateColumn.php` - Column mappings
- `domain/app/Notifications/ECommerce/ProductImportProgressNotification.php` - Notification class
- `app/AppNotifications/AppNotificationBuilder.php` - Notification builder
