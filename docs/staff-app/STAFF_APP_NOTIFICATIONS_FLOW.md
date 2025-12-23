# Staff App Notifications Flow

## Overview

This document describes the notification system for the **Staff/Kitchen App** - the restaurant staff interface for managing orders and receiving real-time updates.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     STAFF APP NOTIFICATION ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────┐     ┌──────────────────────┐     ┌────────────────┐
  │   NOTIFICATION       │     │    WEBSOCKET         │     │   STAFF APP    │
  │   SOURCES            │────▶│    CHANNEL           │────▶│   (FRONTEND)   │
  └──────────────────────┘     └──────────────────────┘     └────────────────┘
                                                                    │
   • Order Created                private-tenant.{id}.system        │
   • Status Changed                                                 ▼
   • Customer Order (Mall)        ┌────────────────────────────────────────┐
   • Assistance Request           │  LaravelEchoContext                    │
                                  │  - Listens to tenant system channel    │
                                  │  - Processes incoming events           │
                                  │  - Triggers UI updates                 │
                                  └────────────────────────────────────────┘
```

---

## Notification Events Matrix

| Event Type | Trigger | Notification Class | Target Roles | Channels | TTS | FCM Push |
|------------|---------|-------------------|--------------|----------|-----|----------|
| `tab.status` | Status change (staff) | `TabChannelNotification` | kitchen, staff, admin | socket | ❌ | ❌ |
| `tab.update` | Tab update | `TenantChannelMessageNotification` | kitchen, staff, admin | socket | ❌ | ❌ |
| `tab.created` | New order created | `TabChannelNotification` | kitchen, staff, admin | socket, push | ✅ | ✅ |
| `mall_tab_creation` | Mall order (tenant tab) | `MallSessionTabCreationNotification` | kitchen, staff | socket, push | ✅ | ✅ |
| `mall_assistance` | Customer assistance | `MallStoreAssistanceNotification` | kitchen, staff | socket, push | ✅ | ✅ |
| `mall_order_status_update` | Mall order status | `MallSessionOrderStatusNotification` | - | session channel | ❌ | ❌ |

---

## WebSocket Channel Configuration

### Channel: `private-tenant.{tenant_id}.system`

This is the primary channel for staff notifications.

```typescript
// Frontend subscription (LaravelEchoContext)
echo.private(`tenant.${tenantId}.system`)
    .listen('.tab.status', handleTabStatus)
    .listen('.tab.update', handleTabUpdate)
    .listen('.message', handleMessage)
    .listen('.speech', handleSpeech)
    .listen('.urgency-alert:speech', handleUrgencyAlert);
```

### Event Types

| Event Key | Description | Actions |
|-----------|-------------|---------|
| `.tab.status` | Tab status changed | Refresh list, show toast |
| `.tab.update` | Tab data updated | Refresh list |
| `.message` | General message | Display notification |
| `.speech` | TTS message | Trigger TTS playback |
| `.urgency-alert:speech` | Urgent alert | Play alarm + TTS |

---

## Tab Status Change Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     TAB STATUS CHANGE NOTIFICATION FLOW                      │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │  Staff Changes  │
  │  Tab Status     │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         LARAVEL BACKEND                                  │
  │                                                                          │
  │  TabController::update()                                                 │
  │    │                                                                     │
  │    ├──▶ TabsNotificationService::handleStatusChange()                   │
  │    │      │                                                              │
  │    │      ├──▶ Update Tab status & date fields                          │
  │    │      ├──▶ Update Order status (mapped)                             │
  │    │      └──▶ sendNotification()                                       │
  │    │             │                                                       │
  │    │             └──▶ AppNotificationBuilder::send()                    │
  │    │                    - TenantChannelMessageNotification              │
  │    │                    - channel: tenant.{id}.system                   │
  │    │                    - targets: kitchen, staff, admin                │
  │    │                                                                     │
  │    └──▶ MallTabNotificationService::handleSlaveTabStatusChange()        │
  │           (if mall order - syncs master tab)                            │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
           │
           │  WebSocket Event
           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         STAFF APP (FRONTEND)                             │
  │                                                                          │
  │  LaravelEchoContext                                                     │
  │    │                                                                     │
  │    └──▶ TabsList / KitchenTabsList                                      │
  │           │                                                              │
  │           ├──▶ useEffect([lastEvent])                                   │
  │           │      if (lastEvent.data.type === 'tab.status')             │
  │           │        - showMessage() - toast notification                 │
  │           │        - refresh() - reload list                            │
  │           │                                                              │
  │           └──▶ UI updates automatically                                 │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Status Transitions

### Valid Status Transitions

| From Status | Allowed Transitions |
|-------------|---------------------|
| `CREATED` | `CONFIRMED`, `CANCELLED`, `CLOSED` |
| `CONFIRMED` | `IN_PREPARATION`, `PREPARED`, `CLOSED`, `CANCELLED` |
| `IN_PREPARATION` | `PREPARED`, `CANCELLED` |
| `PREPARED` | `DELIVERED`, `CLOSED`, `CANCELLED` |
| `DELIVERED` | `CLOSED`, `CANCELLED` |

### Status Flow Diagram

```
                    ┌──────────┐
                    │  CREATED │
                    └────┬─────┘
                         │
                         ▼
                    ┌──────────┐
                    │CONFIRMED │
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               │
  ┌─────────────┐   ┌──────────┐        │
  │IN_PREPARATION│──▶│ PREPARED │        │
  └─────────────┘   └────┬─────┘        │
                         │               │
                         ▼               │
                    ┌──────────┐        │
                    │ DELIVERED│        │
                    └────┬─────┘        │
                         │               │
                         ▼               │
                    ┌──────────┐        │
                    │  CLOSED  │◀───────┘
                    └──────────┘

                         │
                   (any status)
                         │
                         ▼
                    ┌──────────┐
                    │CANCELLED │
                    └──────────┘
```

---

## Notification Payload Structure

### Tab Status Notification (`tab.status`)

```json
{
    "event": "message",
    "data": {
        "user": 123,
        "old": "CREATED",
        "new": "CONFIRMED",
        "message": "[PINOYWOK] Comanda #125 cambió a estado Confirmado",
        "type": "tab.status",
        "marketplace": {
            "id": null,
            "type": "other",
            "name": "PinoyWok"
        },
        "tab_id": 125,
        "order_id": 125,
        "tenant_id": 2,
        "tenant_name": "PinoyWok",
        "customer": {
            "name": "Francisco Aranda",
            "email": null,
            "phone": null
        },
        "delivery": {
            "method": "TABLE",
            "method_label": "Servicio en mesa"
        },
        "order_items": [
            {
                "product_name": "Bulgogi",
                "quantity": 1,
                "unit_price": "13990",
                "modifiers": [
                    {"name": "Cerdo", "price_adjustment": "0.00"}
                ]
            }
        ],
        "order_totals": {
            "subtotal": "13990.00",
            "total": "13990.00",
            "currency": "CLP"
        },
        "tab_note": "Cliente: Francisco Aranda - Mesa: 8"
    },
    "model": "Domain\\App\\Models\\Tab\\Tab",
    "targetType": "role",
    "targetRoles": ["staff", "kitchen", "admin"],
    "channel": "private-tenant.2.system",
    "timestamp": "2025-12-12T00:41:42-03:00"
}
```

### Mall Tab Creation Notification (`speech`)

```json
{
    "event": "message",
    "data": {
        "customer_name": "Francisco Aranda",
        "mall_location": "8",
        "note": "Cliente: Francisco Aranda - Mesa: 8",
        "products_summary": "un Bulgogi, dos Bibimbap",
        "speech": "Nuevo pedido en la mesa 8. un Bulgogi, dos Bibimbap.",
        "tts": "true",
        "alarm": "true"
    },
    "model": "Domain\\App\\Models\\Tab\\Tab",
    "type": "speech",
    "targetRoles": ["kitchen", "staff"],
    "channel": "private-tenant.2.system",
    "notificationPayload": {
        "class": "MallSessionTabCreationNotification",
        "title": "Nuevo pedido en la mesa 8",
        "message": "Francisco Aranda: un Bulgogi, dos Bibimbap"
    }
}
```

### Assistance Request (`urgency-alert:speech`)

```json
{
    "event": "message",
    "data": {
        "type": "alert",
        "title": "New user order",
        "message": "Customer Francisco Aranda at table 8",
        "customer_info": {
            "name": "Francisco Aranda",
            "table": "8"
        },
        "speech": "Customer Francisco Aranda at table 8",
        "tts": "true",
        "alarm": "true"
    },
    "model": "Domain\\App\\Models\\Mall\\MallSession",
    "type": "urgency-alert:speech",
    "targetRoles": ["kitchen", "staff"],
    "channel": "private-tenant.2.system",
    "notificationPayload": {
        "class": "MallStoreAssistanceNotification",
        "title": "New user order",
        "message": "Customer Francisco Aranda at table 8"
    }
}
```

---

## Frontend Event Handling

### TabsList Component

```typescript
// packages/kt-tabs/src/components/TabsList.tsx

useEffect(() => {
    if (!lastEvent) return;
    
    // Handle tab status changes from other users
    if (lastEvent?.model === "Domain\\App\\Models\\Tab\\Tab" && 
        (lastEvent as INotificationPayload<ITabStatusChange>).data.user !== user.id) {
        
        showMessage(translate('tab.status_change_notification', {
            old: translate(`tab.status.${lastEvent.data.old?.toLowerCase()}`),
            new: translate(`tab.status.${lastEvent.data.new?.toLowerCase()}`),
        }));
        refresh();
    } else {
        // Also refresh for own changes
        refresh();
    }
}, [lastEvent]);
```

### KitchenTabsList Component

```typescript
// packages/kt-tabs/src/components/KitchenTabsList.tsx

useEffect(() => {
    if (lastEvent?.model === "Domain\\App\\Models\\Tab\\Tab" && 
        lastEvent.data?.type === "tab.status") {
        // Handle status change notification
        showMessage(`Estado actualizado: ${statusLabels[lastEvent.data.new]}`);
        refresh();
    }
}, [lastEvent]);
```

---

## TTS/Speech Integration (Python Service)

### WebSocket Message Processing

```python
# kt_service.py

def process_message(message):
    data = message.get('data', {})
    payload = data.get('notificationPayload', {})
    
    # Check if TTS is enabled
    tts_enabled = payload.get('tts') == 'true' or data.get('tts') == 'true'
    
    if tts_enabled:
        speech_text = payload.get('speech') or data.get('speech')
        if speech_text:
            play_tts(speech_text)
    
    # Check for alarm
    if payload.get('alarm') == 'true' or data.get('alarm') == 'true':
        play_alarm_sound()
```

### Message Types Triggering TTS

| Notification Class | TTS Flag | Speech Content |
|--------------------|----------|----------------|
| `MallSessionTabCreationNotification` | `tts: 'true'` | "Nuevo pedido en la mesa X. {products_summary}." |
| `MallStoreAssistanceNotification` | `tts: 'true'` | "Customer {name} at table {table}" |
| `TabChannelNotification` (CONFIRMED) | `tts: 'true'` | Product list speech |

---

## FCM Push Notifications (Staff)

### When FCM Push is Sent

| Event | Target Roles | FCM Push |
|-------|--------------|----------|
| New Mall Order (tenant tab) | kitchen, staff | ✅ |
| Assistance Request | kitchen, staff | ✅ |
| Regular tab status change | - | ❌ |

### FCM Payload Example

```json
{
    "notification": {
        "title": "Nuevo pedido en la mesa 8",
        "body": "Francisco Aranda: un Bulgogi, dos Bibimbap"
    },
    "data": {
        "type": "mall_tab_creation",
        "tenant_id": "2",
        "tab_id": "125",
        "mall_location": "8",
        "alarm": "true"
    }
}
```

---

## Backend Components Reference

| Component | File Path | Purpose |
|-----------|-----------|---------|
| `TabController` | `domain/app/Http/Controllers/API/Tabs/TabController.php` | Tab CRUD operations |
| `TabsNotificationService` | `domain/app/Services/Tabs/TabsNotificationService.php` | Status change notifications |
| `MallTabNotificationService` | `domain/app/Services/Tabs/MallTabNotificationService.php` | Mall order sync |
| `TenantChannelMessageNotification` | `app/AppNotifications/Notifications/TenantChannelMessageNotification.php` | Channel notifications |
| `MallSessionTabCreationNotification` | `domain/app/Notifications/MallSessionTabCreationNotification.php` | Mall order notifications |
| `AppNotificationBuilder` | `app/AppNotifications/AppNotificationBuilder.php` | Notification dispatcher |

---

## Frontend Components Reference

| Component | File Path | Purpose |
|-----------|-----------|---------|
| `TabsList` | `packages/kt-tabs/src/components/TabsList.tsx` | Main tab list view |
| `KitchenTabsList` | `packages/kt-tabs/src/components/KitchenTabsList.tsx` | Kitchen display view |
| `LaravelEchoContext` | `dash-admin/src/contexts/com/LaravelEchoContext.tsx` | WebSocket management |
| `tabResource` | `packages/kt-tabs/src/resources/tabResource.tsx` | Tab resource config |

---

## Debugging & Monitoring

### Laravel Log Channels

```php
// config/logging.php
'notifications' => [
    'driver' => 'daily',
    'path' => storage_path('logs/notifications.log'),
    'level' => 'debug',
],
```

### Key Log Messages

```php
// Tab status change
Log::info('Tab status changed', [
    'tab_id' => $tab->id,
    'old_status' => $oldStatus,
    'new_status' => $newStatus
]);

// Notification sent
Log::channel('notifications')->info('Sending notification', [
    'class' => $notificationClass,
    'channel' => $channel,
    'targets' => $targets
]);
```

### Frontend Debug

```typescript
// Enable WebSocket debugging
console.log('WebSocket event received:', lastEvent);
console.log('Event data:', lastEvent?.data);
console.log('Target roles:', lastEvent?.targetRoles);
```
