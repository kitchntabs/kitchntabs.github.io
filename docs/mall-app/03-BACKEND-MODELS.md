---
title: Mall App - Backend Models
layout: default
nav_order: 3
parent: Mall Application
---

# Mall App - Backend Models

## Overview

The Mall App uses Domain-Driven Design with models located in `domain/app/Models/Mall/`.

## Models

### 1. Mall

**File Path:** `domain/app/Models/Mall/Mall.php`

**Purpose:** Represents a physical mall or food court that aggregates multiple tenant stores.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | integer | Primary key |
| `name` | string | Mall display name |
| `slug` | string | URL-friendly identifier |
| `description` | text | Mall description |
| `address` | string | Physical address |
| `phone` | string | Contact phone |
| `email` | string | Contact email |
| `website` | string | Website URL |
| `is_active` | boolean | Enable/disable mall |
| `manager_tenant_id` | integer | FK to managing tenant |
| `settings` | JSON | Custom configurations |

#### Relationships

```php
// The tenant that manages this mall
public function managerTenant(): BelongsTo
{
    return $this->belongsTo(Tenant::class, 'manager_tenant_id');
}

// All tenants in this mall (many-to-many via pivot)
public function tenants(): BelongsToMany
{
    return $this->belongsToMany(Tenant::class, 'mall_tenant')
        ->withPivot(['is_active', 'position'])
        ->withTimestamps();
}

// Only active tenants
public function activeTenants(): BelongsToMany
{
    return $this->tenants()->wherePivot('is_active', true);
}

// All products from all tenants (indirect)
public function products(): HasManyThrough
{
    return $this->hasManyThrough(Product::class, Tenant::class);
}
```

#### Key Methods

```php
// Generate unique slug from name
public static function generateUniqueSlug(string $name): string

// Query scopes
public function scopeActive($query)
public function scopeBySlug($query, string $slug)
```

---

### 2. MallSession

**File Path:** `domain/app/Models/Mall/MallSession.php`

**Purpose:** Represents a customer session created when scanning a QR code. This is the core model for the public ordering flow.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | integer | Primary key |
| `hash` | string(5) | Unique session identifier (e.g., "M5U2W") |
| `mall_id` | integer | FK to mall |
| `customer_name` | string | Customer's name |
| `mall_location` | string | Table number/location |
| `status` | enum | pending, active, completed, cancelled |
| `meta` | JSON | Activation data (IP, user agent) |
| `assistance_requests` | JSON | Track assistance calls per store |
| `created_at` | timestamp | Session creation time |
| `updated_at` | timestamp | Last update time |

#### Status Constants

```php
const STATUS_PENDING = 'pending';      // Created but not yet accessed
const STATUS_ACTIVE = 'active';        // Customer is actively ordering
const STATUS_COMPLETED = 'completed';  // All orders fulfilled
const STATUS_CANCELLED = 'cancelled';  // Session cancelled
```

#### Relationships

```php
// The mall this session belongs to
public function mall(): BelongsTo
{
    return $this->belongsTo(Mall::class);
}

// Orders created in this session (polymorphic)
public function orders(): MorphMany
{
    return $this->morphMany(Order::class, 'brokerable');
}

// Notifications for this session
public function notifications(): HasMany
{
    return $this->hasMany(MallSessionNotification::class);
}

// Unread notifications only
public function unreadNotifications(): HasMany
{
    return $this->notifications()->where('is_read', false);
}
```

#### Key Methods

```php
// Generate unique 5-character hash on model creation
protected static function boot()
{
    parent::boot();
    static::creating(function ($model) {
        if (empty($model->hash)) {
            $model->hash = static::generateUniqueHash();
        }
    });
}

// Generate a unique hash
public static function generateUniqueHash(): string
{
    do {
        $hash = strtoupper(Str::random(5));
    } while (static::where('hash', $hash)->exists());
    return $hash;
}

// Get next available hash (for QR generation)
public static function generateNextHash(): string

// Get master tab for this session
public function getMasterTab(): ?Tab
{
    return Tab::where('brokerable_type', MallSession::class)
        ->where('brokerable_id', $this->id)
        ->where('is_master_tab', true)
        ->first();
}

// Get all tenant tabs (slave tabs)
public function getSlaveTabs(): Collection
{
    $masterTab = $this->getMasterTab();
    if (!$masterTab) return collect();
    
    return Tab::where('master_tab_id', $masterTab->id)->get();
}

// Add notification to this session
public function addNotification(array $data): MallSessionNotification
{
    return $this->notifications()->create([
        'type' => $data['type'] ?? 'mall_notification',
        'title' => $data['title'] ?? '',
        'message' => $data['message'] ?? '',
        'data' => $data['data'] ?? $data,
        'tenant_id' => $data['tenant_id'] ?? null,
        'tenant_name' => $data['tenant_name'] ?? null,
        'status' => $data['status'] ?? null,
        'reference_type' => $data['reference_type'] ?? null,
        'reference_id' => $data['reference_id'] ?? null,
    ]);
}

// Status transitions
public function markAsActive(): void
public function markAsCompleted(): void
public function markAsCancelled(): void

// Status checks
public function isActive(): bool
public function isPending(): bool
public function isCompleted(): bool

// Query scopes
public function scopeByHash($query, string $hash)
public function scopeByMall($query, int $mallId)
public function scopeByStatus($query, string $status)
```

#### Session Lifecycle

```
┌─────────────┐
│   PENDING   │ ← Created via QR code
└──────┬──────┘
       │
       │ Customer accesses session
       │ (validates IP/UserAgent)
       ▼
┌─────────────┐
│   ACTIVE    │ ← Can create orders
└──────┬──────┘
       │
       │ All orders completed OR 6 hours elapsed
       ▼
┌─────────────┐
│  COMPLETED  │
└─────────────┘

       OR

┌─────────────┐
│  CANCELLED  │ ← Manual cancellation
└─────────────┘
```

---

### 3. MallSessionNotification

**File Path:** `domain/app/Models/Mall/MallSessionNotification.php`

**Purpose:** Persists notifications sent to mall sessions for history retrieval and offline recovery.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | integer | Primary key |
| `mall_session_id` | integer | FK to mall session |
| `type` | string | Notification type (e.g., `mall_order_status_update`) |
| `title` | string | Display title |
| `message` | text | Display message |
| `data` | JSON | Full notification payload |
| `tenant_id` | integer | Source tenant ID |
| `tenant_name` | string | Source tenant name |
| `status` | string | Order status at notification time |
| `is_read` | boolean | Read/unread flag |
| `reference_type` | string | Polymorphic type (e.g., `Tab`) |
| `reference_id` | integer | Polymorphic ID |
| `created_at` | timestamp | Creation time |

#### Relationships

```php
public function mallSession(): BelongsTo
{
    return $this->belongsTo(MallSession::class);
}
```

#### Key Methods

```php
// Query scopes
public function scopeUnread($query)
{
    return $query->where('is_read', false);
}

public function scopeOfType($query, string $type)
{
    return $query->where('type', $type);
}

// Mark as read
public function markAsRead(): void
{
    $this->update(['is_read' => true]);
}

// Factory method
public static function createFromData(
    MallSession $session, 
    array $data, 
    ?string $referenceType = null, 
    ?int $referenceId = null
): self
```

---

## Tab Model Extensions for Mall

The `Tab` model (in `domain/app/Models/Tab/Tab.php`) has extensions for mall functionality:

### Additional Properties

| Property | Type | Description |
|----------|------|-------------|
| `is_master_tab` | boolean | True if this is a master (aggregating) tab |
| `master_tab_id` | integer | FK to master tab (for tenant tabs) |
| `brokerable_type` | string | Polymorphic type (e.g., `MallSession`) |
| `brokerable_id` | integer | FK to MallSession |

### Relationships

```php
// The master tab this tenant tab belongs to
public function masterTab(): BelongsTo
{
    return $this->belongsTo(Tab::class, 'master_tab_id');
}

// Tenant tabs belonging to this master tab
public function tenantTabs(): HasMany
{
    return $this->hasMany(Tab::class, 'master_tab_id');
}

// The session this tab belongs to (polymorphic)
public function brokerable(): MorphTo
{
    return $this->morphTo();
}
```

---

## Order Model Extensions for Mall

The `Order` model has extensions for mall functionality:

### Additional Properties

| Property | Type | Description |
|----------|------|-------------|
| `parent_order_id` | integer | FK to parent order (for tenant orders) |
| `brokerable_type` | string | Polymorphic type (e.g., `MallSession`) |
| `brokerable_id` | integer | FK to MallSession |

### Relationships

```php
// Parent order (for tenant orders linked to master)
public function parentOrder(): BelongsTo
{
    return $this->belongsTo(Order::class, 'parent_order_id');
}

// Child orders (tenant orders under master)
public function childOrders(): HasMany
{
    return $this->hasMany(Order::class, 'parent_order_id');
}

// The session this order belongs to (polymorphic)
public function brokerable(): MorphTo
{
    return $this->morphTo();
}
```

---

## Database Schema

### malls table

```sql
CREATE TABLE malls (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    address VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    manager_tenant_id BIGINT UNSIGNED,
    settings JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    
    FOREIGN KEY (manager_tenant_id) REFERENCES tenants(id)
);
```

### mall_tenant pivot table

```sql
CREATE TABLE mall_tenant (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    mall_id BIGINT UNSIGNED NOT NULL,
    tenant_id BIGINT UNSIGNED NOT NULL,
    is_active BOOLEAN DEFAULT true,
    position INT DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    FOREIGN KEY (mall_id) REFERENCES malls(id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE KEY mall_tenant_unique (mall_id, tenant_id)
);
```

### mall_sessions table

```sql
CREATE TABLE mall_sessions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    hash VARCHAR(5) UNIQUE NOT NULL,
    mall_id BIGINT UNSIGNED NOT NULL,
    customer_name VARCHAR(255),
    mall_location VARCHAR(255),
    status ENUM('pending', 'active', 'completed', 'cancelled') DEFAULT 'pending',
    meta JSON,
    assistance_requests JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    FOREIGN KEY (mall_id) REFERENCES malls(id),
    INDEX idx_hash (hash),
    INDEX idx_status (status),
    INDEX idx_mall_status (mall_id, status)
);
```

### mall_session_notifications table

```sql
CREATE TABLE mall_session_notifications (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    mall_session_id BIGINT UNSIGNED NOT NULL,
    type VARCHAR(100) NOT NULL,
    title VARCHAR(255),
    message TEXT,
    data JSON,
    tenant_id BIGINT UNSIGNED,
    tenant_name VARCHAR(255),
    status VARCHAR(50),
    is_read BOOLEAN DEFAULT false,
    reference_type VARCHAR(255),
    reference_id BIGINT UNSIGNED,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    FOREIGN KEY (mall_session_id) REFERENCES mall_sessions(id) ON DELETE CASCADE,
    INDEX idx_session_read (mall_session_id, is_read),
    INDEX idx_type (type)
);
```

### Tab model additions

```sql
ALTER TABLE tabs ADD COLUMN is_master_tab BOOLEAN DEFAULT false;
ALTER TABLE tabs ADD COLUMN master_tab_id BIGINT UNSIGNED;
ALTER TABLE tabs ADD COLUMN brokerable_type VARCHAR(255);
ALTER TABLE tabs ADD COLUMN brokerable_id BIGINT UNSIGNED;

ALTER TABLE tabs ADD FOREIGN KEY (master_tab_id) REFERENCES tabs(id);
ALTER TABLE tabs ADD INDEX idx_brokerable (brokerable_type, brokerable_id);
```

### Order model additions

```sql
ALTER TABLE orders ADD COLUMN parent_order_id BIGINT UNSIGNED;
ALTER TABLE orders ADD COLUMN brokerable_type VARCHAR(255);
ALTER TABLE orders ADD COLUMN brokerable_id BIGINT UNSIGNED;

ALTER TABLE orders ADD FOREIGN KEY (parent_order_id) REFERENCES orders(id);
ALTER TABLE orders ADD INDEX idx_brokerable (brokerable_type, brokerable_id);
```
