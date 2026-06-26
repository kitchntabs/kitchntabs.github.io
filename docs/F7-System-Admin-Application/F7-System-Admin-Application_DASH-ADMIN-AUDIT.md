---
layout: default
title: F7-System-Admin-Application DASH-ADMIN-AUDIT
---

# DASH Admin Audit Mechanism

A comprehensive, centralized audit logging system for tracking changes to models in the DASH Admin framework. It leverages the **Spatie Laravel Activity Log** package on the backend and provides a reusable **AuditLog** component on the frontend.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Backend Setup (Step by Step)](#backend-setup-step-by-step)
5. [Frontend Setup (Step by Step)](#frontend-setup-step-by-step)
6. [API Reference](#api-reference)
7. [Full Example: Adding Audit to a New Model](#full-example-adding-audit-to-a-new-model)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The DASH Admin Audit Mechanism provides:
- Automatic logging of all CRUD operations on models
- User attribution (who made the change)
- Timestamp tracking (when the change occurred)
- Old/new value comparison for updates
- Server-side error logging for debugging
- A reusable React component for displaying audit logs

---

## Features

| Feature | Description |
|---------|-------------|
| **Automatic Logging** | Changes are logged automatically when models are created, updated, or deleted |
| **User Attribution** | The authenticated user is recorded as the "causer" of each change |
| **Value Tracking** | For updates, both old and new values are stored |
| **Pagination** | Audit logs support server-side pagination |
| **Filtering** | Filter by event type, date range, user, and log category |
| **Export** | CSV and print export functionality in the frontend |
| **JSON Details** | View full log properties in a dialog |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AUDIT FLOW                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐ │
│  │   Frontend   │     │   Backend    │     │    Database          │ │
│  │  AuditLog    │────▶│ Controller   │────▶│ activity_log table   │ │
│  │  Component   │◀────│ audit()      │◀────│                      │ │
│  └──────────────┘     └──────────────┘     └──────────────────────┘ │
│                                                                      │
│  Model Changes:                                                      │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐ │
│  │   Model      │     │ LogsActivity │     │    activity_log      │ │
│  │   CRUD       │────▶│   Trait      │────▶│    (auto-logged)     │ │
│  └──────────────┘     └──────────────┘     └──────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Backend Setup (Step by Step)

### Step 1: Add LogsActivity Trait to Your Model

Add the Spatie `LogsActivity` trait and implement `getActivitylogOptions()`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\LogOptions;
use Spatie\Activitylog\Traits\LogsActivity;

class Product extends Model
{
    use LogsActivity;

    protected $fillable = ['name', 'price', 'description', 'is_active'];

    /**
     * Configure activity log options for this model
     */
    public function getActivitylogOptions(): LogOptions
    {
        return LogOptions::defaults()
            ->logAll()                              // Log all attributes
            ->logExcept(['updated_at', 'created_at']) // Exclude timestamps
            ->logOnlyDirty()                        // Only log changed values
            ->dontSubmitEmptyLogs();                // Don't log empty changes
    }
}
```

**Alternative: Use the HasAuditLog Trait**

For a quick setup with sensible defaults, use the convenience trait:

```php
use App\Traits\HasAuditLog;

class Product extends Model
{
    use HasAuditLog;
}
```

### Step 2: Configure Activity Log Options (Optional)

Customize what gets logged using `getActivitylogOptions()`:

```php
public function getActivitylogOptions(): LogOptions
{
    return LogOptions::defaults()
        // What to log
        ->logAll()                              // Log all fillable attributes
        // OR
        ->logOnly(['name', 'price'])            // Log only specific attributes
        // OR
        ->logFillable()                         // Log all fillable attributes
        
        // What to exclude
        ->logExcept(['password', 'remember_token', 'updated_at'])
        
        // When to log
        ->logOnlyDirty()                        // Only when values change
        ->dontSubmitEmptyLogs()                 // Skip if nothing changed
        
        // Customize log name (category)
        ->useLogName('products')                // Default is 'default'
        
        // Custom description
        ->setDescriptionForEvent(fn(string $eventName) => 
            "Product has been {$eventName}"
        );
}
```

### Step 3: Verify Route Configuration

The audit routes are pre-configured in `config/react-admin-methods.php`. Verify they exist and are ordered correctly:

```php
return [
    // ... other routes

    // Audit routes - MUST be BEFORE 'update' and 'getOne' to avoid route collision
    'audit' => [
        'path'    => '/audit/{id}',
        'method'  => 'GET',
        'action'  => 'audit',
    ],
    'auditAll' => [
        'path'    => '/audit',
        'method'  => 'GET',
        'action'  => 'auditAll',
    ],

    // These routes come AFTER audit routes
    'update' => [
        'path'    => '/{id}',
        'method'  => 'PUT',
        'action'  => 'update',
    ],
    'getOne' => [
        'path'    => '/{id}',
        'method'  => 'GET',
        'action'  => 'getOne',
    ],
    
    // ...
];
```

> ⚠️ **Important**: Route order matters! The `/audit` routes must come before `/{id}` routes.

### Step 4: Ensure Controller Extends ReactAdminBaseController

Your controller must extend `ReactAdminBaseController` which provides the `audit()` and `auditAll()` methods:

```php
<?php

namespace Domain\App\Http\Controllers\API\Products;

use App\Http\Controllers\API\System\ReactAdminBaseController;
use App\Models\Product;

class ProductController extends ReactAdminBaseController
{
    public $resource = 'product';

    public function __construct()
    {
        $this->model = Product::query();
    }
}
```

---

## Frontend Setup (Step by Step)

### Step 1: Import the AuditLog Component

The `AuditLog` component is available from the `dash-components` package:

```typescript
import { AuditLog } from 'dash-components';
```

### Step 2: Add Audit Tab to Your Schema

Add the audit log field to your model's schema file:

```typescript
import { IDashAutoAdminAttribute } from "dash-auto-admin";
import { AuditLog } from "dash-components";

const productSchema: IDashAutoAdminAttribute[] = [
    // ... your existing fields ...

    // ============ Audit Tab ============
    {
        tab: 'Audit',                    // Tab name in the form
        attribute: 'audit_logs',         // Virtual attribute (not persisted)
        label: 'Audit Logs',             // Display label
        type: Array,                     // Type indicator
        inList: false,                   // Hide in list view
        inEdit: true,                    // Show in edit view
        inShow: true,                    // Show in show/view mode
        inCreate: false,                 // Hide in create mode (no logs exist yet)
        readOnly: true,                  // Read-only field
        custom: true,                    // Uses custom component
        component: AuditLog,             // The generic AuditLog component
        fieldProps: {
            helperText: 'View all changes made to this record',
        },
    },
];

export default productSchema;
```

### Schema Properties Reference

| Property | Value | Description |
|----------|-------|-------------|
| `tab` | `'Audit'` | Creates a dedicated "Audit" tab |
| `attribute` | `'audit_logs'` | Virtual attribute name (not in database) |
| `type` | `Array` | Indicates array data type |
| `inList` | `false` | Don't show in list view |
| `inEdit` | `true` | Show in edit mode |
| `inShow` | `true` | Show in view/show mode |
| `inCreate` | `false` | Hide in create mode |
| `readOnly` | `true` | Cannot be modified |
| `custom` | `true` | Uses custom rendering component |
| `component` | `AuditLog` | The reusable audit component from `dash-components` |

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{prefix}/{resource}/audit/{id}` | Get audit logs for a specific record |
| GET | `/api/{prefix}/{resource}/audit?subject_id={id}` | Get audit logs filtered by subject ID |

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `subject_id` | integer | Filter by record ID |
| `log_name` | string | Filter by log category (e.g., 'default', 'errors') |
| `event` | string | Filter by event type ('created', 'updated', 'deleted') |
| `causer_id` | integer | Filter by user ID who made the changes |
| `date_from` | string | Start date filter (ISO 8601 format) |
| `date_to` | string | End date filter (ISO 8601 format) |
| `page` | integer | Page number (default: 1) |
| `perPage` | integer | Records per page (default: 15) |

### Response Format

```json
{
  "data": [
    {
      "id": 1,
      "log_name": "default",
      "description": "updated",
      "event": "updated",
      "subject_type": "App\\Models\\Product",
      "subject_id": 123,
      "causer_type": "App\\Models\\User",
      "causer_id": 1,
      "causer_name": "John Doe",
      "properties": {
        "old": { "name": "Old Name", "price": 10.00 },
        "attributes": { "name": "New Name", "price": 15.00 }
      },
      "created_at": "2026-02-03T10:30:00+00:00",
      "updated_at": "2026-02-03T10:30:00+00:00"
    }
  ],
  "total": 25,
  "page": 1,
  "perPage": 15,
  "subject": {
    "type": "App\\Models\\Product",
    "id": 123
  }
}
```

---

## Full Example: Adding Audit to a New Model

### Backend

**1. Model (`domain/app/Models/Inventory/Warehouse.php`):**

```php
<?php

namespace Domain\App\Models\Inventory;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Spatie\Activitylog\LogOptions;
use Spatie\Activitylog\Traits\LogsActivity;

class Warehouse extends Model
{
    use HasFactory, LogsActivity;

    protected $fillable = ['name', 'location', 'capacity', 'is_active'];

    protected $casts = [
        'is_active' => 'boolean',
        'capacity' => 'integer',
    ];

    public function getActivitylogOptions(): LogOptions
    {
        return LogOptions::defaults()
            ->logAll()
            ->logExcept(['updated_at', 'created_at'])
            ->logOnlyDirty()
            ->dontSubmitEmptyLogs()
            ->useLogName('inventory');
    }
}
```

**2. Controller (`domain/app/Http/Controllers/API/Inventory/WarehouseController.php`):**

```php
<?php

namespace Domain\App\Http\Controllers\API\Inventory;

use App\Http\Controllers\API\System\ReactAdminBaseController;
use Domain\App\Models\Inventory\Warehouse;

class WarehouseController extends ReactAdminBaseController
{
    public $resource = 'warehouse';

    public function __construct()
    {
        $this->model = Warehouse::query();
    }
}
```

### Frontend

**3. Schema (`warehouseSchema.ts`):**

```typescript
import { IDashAutoAdminAttribute } from "dash-auto-admin";
import { AuditLog } from "dash-components";

const warehouseSchema: IDashAutoAdminAttribute[] = [
    {
        tab: 'Basic Info',
        attribute: 'name',
        label: 'Warehouse Name',
        type: String,
        inList: true,
        inEdit: true,
        inShow: true,
        inCreate: true,
        required: true,
    },
    {
        tab: 'Basic Info',
        attribute: 'location',
        label: 'Location',
        type: String,
        inList: true,
        inEdit: true,
        inShow: true,
        inCreate: true,
    },
    {
        tab: 'Basic Info',
        attribute: 'capacity',
        label: 'Capacity',
        type: Number,
        inList: true,
        inEdit: true,
        inShow: true,
        inCreate: true,
    },
    {
        tab: 'Basic Info',
        attribute: 'is_active',
        label: 'Active',
        type: Boolean,
        inList: true,
        inEdit: true,
        inShow: true,
        inCreate: true,
    },

    // ============ Audit Tab ============
    {
        tab: 'Audit',
        attribute: 'audit_logs',
        label: 'Audit Logs',
        type: Array,
        inList: false,
        inEdit: true,
        inShow: true,
        inCreate: false,
        readOnly: true,
        custom: true,
        component: AuditLog,
        fieldProps: {
            helperText: 'View all changes made to this warehouse',
        },
    },
];

export default warehouseSchema;
```

**4. Resource (`WarehouseResource.tsx`):**

```typescript
import { ResourceTemplate } from "dash-admin";
import WarehouseIcon from "@mui/icons-material/Warehouse";
import warehouseSchema from "./warehouseSchema";

const WarehouseResource = {
    group: "Inventory",
    roles: ["admin", "inventory_manager"],
    component: ResourceTemplate,
    model: "inventory/warehouse",
    label: "Warehouses",
    schema: warehouseSchema,
    icon: <WarehouseIcon />,
    menu: [{ title: "List", redirect: "/inventory/warehouse" }],
    view: true,
    create: true,
    edit: true,
};

export default WarehouseResource;
```

---

## Testing

Run the audit tests:

```bash
./vendor/bin/sail test --filter=AuditTest
```

### Sample Test

```php
<?php

namespace Tests\Feature\API;

use Tests\TestCase;
use App\Models\User;
use App\Models\Product;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;
use Spatie\Activitylog\Models\Activity;

class ProductAuditTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        Sanctum::actingAs(User::factory()->create(), ['*']);
    }

    public function test_it_logs_activity_when_product_is_created()
    {
        $product = Product::create(['name' => 'Test Product', 'price' => 10]);

        $activity = Activity::where('subject_type', Product::class)
            ->where('subject_id', $product->id)
            ->where('event', 'created')
            ->first();

        $this->assertNotNull($activity);
        $this->assertEquals('created', $activity->event);
    }

    public function test_it_can_retrieve_audit_logs_via_api()
    {
        $product = Product::create(['name' => 'Test', 'price' => 10]);

        $response = $this->getJson("/api/products/audit?subject_id={$product->id}");

        $response->assertStatus(200)
            ->assertJsonStructure([
                'data' => [['id', 'event', 'description', 'created_at']],
                'total', 'page', 'perPage',
            ]);
    }
}
```

---

## Troubleshooting

### "Invalid input syntax for type bigint: 'audit'"

**Cause**: Route order issue - `/{id}` is catching `/audit`

**Solution**: Ensure audit routes come before `/{id}` routes in `config/react-admin-methods.php`

### No audit logs appearing

**Cause**: Model doesn't have `LogsActivity` trait

**Solution**: Add the trait and `getActivitylogOptions()` method

### "activity_log table doesn't exist"

**Solution**: Run migrations:
```bash
./vendor/bin/sail artisan migrate
```

### User not recorded in audit logs

**Cause**: User not authenticated

**Solution**: Ensure requests use Sanctum authentication

---

## Related Files

| File | Purpose |
|------|---------|
| `config/react-admin-methods.php` | Route configuration |
| `app/Traits/HasAuditLog.php` | Convenience trait for models |
| `app/Http/Controllers/API/System/ReactAdminBaseController.php` | Base controller with audit methods |
| `packages/dash-components/src/components/AuditLog/AuditLog.tsx` | Generic frontend component |
```

