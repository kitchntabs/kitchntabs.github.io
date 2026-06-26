---
title: Mall App - Backend Services
layout: default
nav_order: 5
parent: Mall Application
---

# Mall App - Backend Services

## Overview

Services contain the business logic for mall operations, located in `domain/app/Services/`.

## Services

### 1. MallOrderSyncService

**File Path:** `domain/app/Services/Mall/MallOrderSyncService.php`

**Purpose:** Synchronizes tenant tab statuses with master tab and handles order product updates.

#### Key Methods

##### `syncTenantTabStatusWithMaster(Tab $tenantTab)`

Main entry point for status synchronization.

```php
public function syncTenantTabStatusWithMaster(Tab $tenantTab): void
{
    Log::info('MallOrderSyncService::syncTenantTabStatusWithMaster', [
        'tenant_tab_id' => $tenantTab->id,
        'tenant_tab_status' => $tenantTab->status,
    ]);

    // Get master tab
    $masterTab = $tenantTab->masterTab;
    if (!$masterTab) {
        Log::warning('No master tab found for tenant tab', ['tenant_tab_id' => $tenantTab->id]);
        return;
    }

    // Sync product statuses from tenant order to master order
    $this->syncMasterOrderProducts($masterTab, $tenantTab);

    // Notify the mall session about the status change
    $this->notifyMallSession($masterTab, $tenantTab);
}
```

##### `syncMasterOrderProducts(Tab $masterTab, Tab $tenantTab)`

Updates master order items to reflect tenant order item statuses.

```php
protected function syncMasterOrderProducts(Tab $masterTab, Tab $tenantTab): void
{
    $masterOrder = $masterTab->order;
    $tenantOrder = $tenantTab->order;
    
    if (!$masterOrder || !$tenantOrder) {
        return;
    }

    // Map tab status to order item status
    $newStatus = $this->mapTabStatusToOrderStatus($tenantTab->status);

    // Update matching products in master order
    foreach ($tenantOrder->items as $tenantItem) {
        $masterItem = $masterOrder->items()
            ->where('product_id', $tenantItem->product_id)
            ->where('line_id', $tenantItem->line_id)
            ->first();
        
        if ($masterItem) {
            $masterItem->update(['status' => $newStatus]);
            
            Log::info('Updated master order item status', [
                'master_item_id' => $masterItem->id,
                'product_id' => $tenantItem->product_id,
                'new_status' => $newStatus,
            ]);
        }
    }
}
```

##### `mapTabStatusToOrderStatus(string $tabStatus)`

Maps tab statuses to order statuses.

```php
protected function mapTabStatusToOrderStatus(string $tabStatus): string
{
    return match ($tabStatus) {
        Tab::STATUS_CREATED => Order::STATUS_CREATED,
        Tab::STATUS_CONFIRMED => Order::STATUS_CREATED,
        Tab::STATUS_IN_PREPARATION => Order::STATUS_IN_PREPARATION,
        Tab::STATUS_PREPARED => Order::STATUS_PREPARED,
        Tab::STATUS_DELIVERED => Order::STATUS_SHIPPED,
        Tab::STATUS_CLOSED => Order::STATUS_CLOSED,
        Tab::STATUS_CANCELLED => Order::STATUS_CANCELLED,
        default => Order::STATUS_CREATED,
    };
}
```

##### `notifyMallSession(Tab $masterTab, Tab $tenantTab)`

Sends WebSocket notification to the mall session.

```php
protected function notifyMallSession(Tab $masterTab, Tab $tenantTab): void
{
    $mallSession = $masterTab->brokerable;
    
    if (!$mallSession || !($mallSession instanceof MallSession)) {
        Log::warning('No MallSession found for master tab', [
            'master_tab_id' => $masterTab->id,
        ]);
        return;
    }

    // Build notification data
    $notificationData = [
        'event' => 'mall_order_status_update',
        'tenant_tab_id' => $tenantTab->id,
        'tenant_id' => $tenantTab->tenant_id,
        'tenant_name' => $tenantTab->tenant->name ?? 'Unknown',
        'status' => $tenantTab->status,
        'master_tab_id' => $masterTab->id,
        'timestamp' => now()->toIso8601String(),
        'products' => $tenantTab->order->items->map(fn($item) => [
            'id' => $item->product_id,
            'name' => $item->product_name,
            'quantity' => $item->quantity,
            'status' => $item->status,
        ])->toArray(),
        'mall_session_hash' => $mallSession->hash,
    ];

    // Send via WebSocket and persist to database
    AppNotificationBuilder::send(
        notificationClass: MallSessionOrderStatusNotification::class,
        data: $notificationData,
        channel: "session.{$mallSession->hash}",
        scope: "public",
        modelInstance: $mallSession,
        type: 'mall_order_status_update'
    );

    Log::info('Mall session notified of order status change', [
        'session_hash' => $mallSession->hash,
        'tenant_tab_id' => $tenantTab->id,
        'status' => $tenantTab->status,
    ]);
}
```

##### `syncMallOrderPaymentStatus(Tab $masterTab, bool $isPaid)`

Synchronizes payment status between master and tenant orders.

```php
public function syncMallOrderPaymentStatus(Tab $masterTab, bool $isPaid): void
{
    // Update master order
    if ($masterTab->order) {
        $masterTab->order->update(['is_paid' => $isPaid]);
    }

    // Update all tenant orders
    foreach ($masterTab->tenantTabs as $tenantTab) {
        if ($tenantTab->order) {
            $tenantTab->order->update(['is_paid' => $isPaid]);
        }
    }

    Log::info('Synced payment status for mall order', [
        'master_tab_id' => $masterTab->id,
        'is_paid' => $isPaid,
        'tenant_count' => $masterTab->tenantTabs->count(),
    ]);
}
```

---

### 2. TabsNotificationService

**File Path:** `domain/app/Services/Tabs/TabsNotificationService.php`

**Purpose:** Comprehensive notification service for tab operations, including mall-specific notifications.

#### Mall-Specific Methods

##### `handleSlaveTabStatusChange(Tab $tenantTab, string $oldStatus, bool $silent = false)`

Handles status changes for tenant tabs and notifies mall sessions.

```php
public function handleSlaveTabStatusChange(
    Tab $tenantTab, 
    string $oldStatus, 
    bool $silent = false
): void
{
    $masterTab = $tenantTab->masterTab;
    
    if (!$masterTab) {
        return;
    }

    // Check if this is a mall order
    if ($masterTab->brokerable_type !== MallSession::class) {
        return;
    }

    // Sync order items with master
    $this->syncMasterOrderItems($masterTab, $tenantTab);

    // Send notification if not silent
    if (!$silent) {
        $this->notifyMallSession($masterTab, $tenantTab, $tenantTab->status);
    }

    // Update master tab status based on all tenant statuses
    $this->updateMasterTabStatus($masterTab, $tenantTab);
}
```

##### `syncMasterOrderItems(Tab $masterTab, Tab $tenantTab)`

Updates master order items from tenant order items.

```php
protected function syncMasterOrderItems(Tab $masterTab, Tab $tenantTab): void
{
    $masterOrder = $masterTab->order;
    $tenantOrder = $tenantTab->order;

    if (!$masterOrder || !$tenantOrder) {
        return;
    }

    foreach ($tenantOrder->items as $tenantItem) {
        // Find matching item in master order
        $masterItem = $masterOrder->items()
            ->where('line_id', $tenantItem->line_id)
            ->first();

        if ($masterItem) {
            // Update status to match tenant item
            $masterItem->update([
                'status' => $tenantItem->status ?? $this->mapTabStatusToItemStatus($tenantTab->status),
            ]);
        }
    }
}
```

##### `notifyMallSession(Tab $masterTab, Tab $tenantTab, string $status)`

Sends notification to mall session channel.

```php
protected function notifyMallSession(Tab $masterTab, Tab $tenantTab, string $status): void
{
    try {
        $mallSession = MallSession::find($masterTab->brokerable_id);
        
        if (!$mallSession) {
            Log::warning('MallSession not found for notification', [
                'brokerable_id' => $masterTab->brokerable_id,
            ]);
            return;
        }

        // Build products array with status
        $products = $tenantTab->order->items->map(function ($item) {
            return [
                'id' => $item->id,
                'product_id' => $item->product_id,
                'name' => $item->product_name,
                'quantity' => $item->quantity,
                'status' => $item->status,
                'image_url' => $item->product->image_url ?? null,
            ];
        })->toArray();

        $notificationData = [
            'event' => 'mall_order_status_update',
            'tenant_tab_id' => $tenantTab->id,
            'tenant_id' => $tenantTab->tenant_id,
            'tenant_name' => $tenantTab->tenant->name ?? 'Unknown Tenant',
            'status' => $status,
            'master_tab_id' => $masterTab->id,
            'child_order_id' => $tenantTab->order->id,
            'parent_order_id' => $masterTab->order->id,
            'timestamp' => now()->toIso8601String(),
            'customer_info' => [
                'name' => $mallSession->customer_name,
                'table' => $mallSession->mall_location,
            ],
            'products' => $products,
            'mall_session_hash' => $mallSession->hash,
        ];

        Log::info('Sending mall session notification', [
            'mall_session_hash' => $mallSession->hash,
            'tenant_tab_id' => $tenantTab->id,
            'status' => $status,
            'products_count' => count($products),
        ]);

        AppNotificationBuilder::send(
            notificationClass: MallSessionOrderStatusNotification::class,
            data: $notificationData,
            channel: "session.{$mallSession->hash}",
            scope: "public",
            modelInstance: $mallSession,
            type: 'mall_order_status_update'
        );

    } catch (\Exception $e) {
        Log::error('Error sending mall session notification: ' . $e->getMessage(), [
            'tenant_tab_id' => $tenantTab->id,
            'master_tab_id' => $masterTab->id,
            'error' => $e->getMessage(),
        ]);
    }
}
```

##### `updateMasterTabStatus(Tab $masterTab, Tab $updatedTenantTab)`

Updates master tab status based on aggregate tenant status.

```php
protected function updateMasterTabStatus(Tab $masterTab, Tab $updatedTenantTab): void
{
    $tenantTabs = Tab::where('master_tab_id', $masterTab->id)->get();
    
    if ($tenantTabs->isEmpty()) {
        return;
    }

    $statusCounts = $tenantTabs->groupBy('status')->map->count();
    $totalTabs = $tenantTabs->count();

    $newMasterStatus = null;

    // Determine new master status based on tenant statuses
    if (isset($statusCounts[Tab::STATUS_CANCELLED]) && 
        $statusCounts[Tab::STATUS_CANCELLED] === $totalTabs) {
        // All cancelled → master cancelled
        $newMasterStatus = Tab::STATUS_CANCELLED;
    } elseif (isset($statusCounts[Tab::STATUS_CLOSED]) && 
              $statusCounts[Tab::STATUS_CLOSED] === $totalTabs) {
        // All closed → master closed
        $newMasterStatus = Tab::STATUS_CLOSED;
    } elseif (isset($statusCounts[Tab::STATUS_DELIVERED]) && 
              $statusCounts[Tab::STATUS_DELIVERED] === $totalTabs) {
        // All delivered → master delivered
        $newMasterStatus = Tab::STATUS_DELIVERED;
    } elseif (isset($statusCounts[Tab::STATUS_PREPARED]) && 
              $statusCounts[Tab::STATUS_PREPARED] + 
              ($statusCounts[Tab::STATUS_DELIVERED] ?? 0) === $totalTabs) {
        // All prepared or delivered → master prepared
        $newMasterStatus = Tab::STATUS_PREPARED;
    } elseif (isset($statusCounts[Tab::STATUS_IN_PREPARATION])) {
        // Any in preparation → master in preparation
        $newMasterStatus = Tab::STATUS_IN_PREPARATION;
    } elseif (isset($statusCounts[Tab::STATUS_CONFIRMED])) {
        // Any confirmed → master confirmed
        $newMasterStatus = Tab::STATUS_CONFIRMED;
    }

    if ($newMasterStatus && $newMasterStatus !== $masterTab->status) {
        $masterTab->update([
            'status' => $newMasterStatus,
            "date_{$this->statusToDateField($newMasterStatus)}" => now(),
        ]);

        Log::info('Updated master tab status', [
            'master_tab_id' => $masterTab->id,
            'old_status' => $masterTab->status,
            'new_status' => $newMasterStatus,
        ]);
    }
}
```

---

### 3. MallSessionNotificationStorageService

**File Path:** `domain/app/Services/Mall/MallSessionNotificationStorageService.php`

**Purpose:** Utility service to store notifications to the database.

```php
class MallSessionNotificationStorageService
{
    /**
     * Store a notification for a mall session
     */
    public static function storeNotification(
        string $hash,
        array $data,
        ?string $referenceType = null,
        ?string $referenceId = null
    ): ?MallSessionNotification
    {
        try {
            $mallSession = MallSession::where('hash', $hash)->first();
            
            if (!$mallSession) {
                Log::warning('Cannot store notification: MallSession not found', [
                    'hash' => $hash,
                ]);
                return null;
            }

            $notification = $mallSession->addNotification([
                'type' => $data['type'] ?? $data['event'] ?? 'mall_notification',
                'title' => $data['title'] ?? 'Notification',
                'message' => $data['message'] ?? '',
                'data' => $data,
                'tenant_id' => $data['tenant_id'] ?? null,
                'tenant_name' => $data['tenant_name'] ?? null,
                'status' => $data['status'] ?? null,
                'reference_type' => $referenceType,
                'reference_id' => $referenceId,
            ]);

            Log::info('Notification stored for mall session', [
                'notification_id' => $notification->id,
                'session_hash' => $hash,
                'type' => $notification->type,
            ]);

            return $notification;

        } catch (\Exception $e) {
            Log::error('Error storing mall session notification: ' . $e->getMessage(), [
                'hash' => $hash,
                'error' => $e->getMessage(),
            ]);
            return null;
        }
    }
}
```

---

## Status Transition Logic

### Tab Status Progression

```
CREATED → CONFIRMED → IN_PREPARATION → PREPARED → DELIVERED → CLOSED
                                                           ↘
                                                        CANCELLED (from any state)
```

### Status Checking Methods

```php
// In TabsNotificationService
protected function isNewerStatus(string $newStatus, string $currentStatus): bool
{
    $statusOrder = [
        Tab::STATUS_CREATED => 1,
        Tab::STATUS_CONFIRMED => 2,
        Tab::STATUS_IN_PREPARATION => 3,
        Tab::STATUS_PREPARED => 4,
        Tab::STATUS_DELIVERED => 5,
        Tab::STATUS_CLOSED => 6,
        Tab::STATUS_CANCELLED => 7, // Special case
    ];

    return ($statusOrder[$newStatus] ?? 0) > ($statusOrder[$currentStatus] ?? 0);
}
```

### Master Tab Status Rules

| Tenant Statuses | Master Status |
|-----------------|---------------|
| All CANCELLED | CANCELLED |
| All CLOSED | CLOSED |
| All DELIVERED | DELIVERED |
| All PREPARED/DELIVERED | PREPARED |
| Any IN_PREPARATION | IN_PREPARATION |
| Any CONFIRMED | CONFIRMED |
| Otherwise | No change |

---

## Service Dependencies

```
┌────────────────────────────────┐
│       TabsNotificationService  │
│  - handleSlaveTabStatusChange  │
│  - syncMasterOrderItems        │
│  - notifyMallSession           │
└───────────────┬────────────────┘
                │
                │ calls
                ▼
┌────────────────────────────────┐
│      MallOrderSyncService      │
│  - syncTenantTabStatusWithMaster│
│  - syncMasterOrderProducts     │
│  - notifyMallSession           │
└───────────────┬────────────────┘
                │
                │ uses
                ▼
┌────────────────────────────────┐
│    AppNotificationBuilder      │
│  - send()                      │
└───────────────┬────────────────┘
                │
                │ creates
                ▼
┌────────────────────────────────┐
│  MallSessionOrderStatus        │
│  Notification                  │
│  - buildNotificationPayload    │
│  - persistNotification         │
└────────────────────────────────┘
```
