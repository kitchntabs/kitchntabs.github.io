
# Mall Session Notifications Flow - Technical Documentation

## Overview

This document provides comprehensive technical documentation for the notification system in the KitchnTabs Mall application. It covers all notification events, recipients, delivery channels, and the interconnected components that make the system work.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Notification Flow Diagram](#notification-flow-diagram)
3. [Notification Events Matrix](#notification-events-matrix)
4. [Component Architecture](#component-architecture)
5. [Detailed Event Flows](#detailed-event-flows)
6. [Delivery Channels](#delivery-channels)
7. [Role-Based Targeting](#role-based-targeting)
8. [Code Component Reference](#code-component-reference)

---

## System Architecture

```mermaid
flowchart TD
    Customer["Customer (Mobile App)"] --> Controller["Mall Session Controller"]
    Controller --> Builder["Notification Builder<br/>AppNotificationBuilder"]
    Builder --> WS["WebSocket (Pusher)"]
    Builder --> Email["Email (SMTP)"]
    Builder --> FCM["FCM (Push)"]
    WS --> Electron["Electron Desktop (Kitchen)"]
    WS --> React["React Browser (Admin)"]
    WS --> Python["Python Service (TTS)"]
    Email --> StaffInbox["Staff Email Inbox"]
    FCM --> MobileDevice["Mobile Device (FCM)"]
```

---

## Notification Flow Diagram

### Mall Session Order Creation Flow

```mermaid
flowchart TD
    A["Scan QR Code"] --> B["1. Create Session"]
    B --> C["Select Items from Multiple Restaurants"]
    C --> D["2. Submit Order"]
    D --> E["MallTabsController._create()"]
    E --> F["NOTIFICATION DISPATCH"]
    F --> G["1. CREATE MASTER TAB (Mall Manager Tenant)<br/>Socket ONLY (UI refresh)<br/>No Email, No FCM Push"]
    F --> H["2. CREATE TENANT TAB (Per Restaurant)<br/>MallSessionTabCreationNotification<br/>Socket (UI refresh)<br/>FCM Push (mobile notification)<br/>TTS Speech (Python service)<br/>Alarm (frontend sound)"]
    H --> H1["Staff"]
    H --> H2["Kitchen"]
    F --> I["3. TAB STATUS CHANGE (TabChannelNotification)"]
    I --> I1["CREATED Status - Master Tab: Socket ONLY"]
    I1 --> I1R["Mall Manager (not notified)"]
    I --> I2["CREATED Status - Tenant Tab: Socket + Email"]
    I2 --> I2R["Store Staff"]
    I --> I3["CONFIRMED Status - Tenant Tab: Socket + Email + FCM + TTS"]
    I3 --> I3R["Kitchen"]
```

---

## Notification Events Matrix

### By Event Type

| Event | Notification Class | Socket | Email | FCM Push | TTS/Speech | Alarm |
|-------|-------------------|--------|-------|----------|------------|-------|
| **Mall Tab Created (Master)** | `MallSessionTabCreationNotification` | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Mall Tab Created (Tenant)** | `MallSessionTabCreationNotification` | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Tab Status: CREATED (Master)** | `TabChannelNotification` | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Tab Status: CREATED (Tenant)** | `TabChannelNotification` | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Tab Status: CONFIRMED (Tenant)** | `TabChannelNotification` | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Tab Status: IN_PREPARATION** | `TabChannelNotification` | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Tab Status: PREPARED** | `TabChannelNotification` | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Tab Status: DELIVERED** | `TabChannelNotification` | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Tab Status: CANCELLED** | `TabChannelNotification` | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Store Assistance Request** | `MallStoreAssistanceNotification` | ✅ | ❌ | ✅ | ✅ | ✅ |

### By Recipient Role

| Role | CREATED (Master) | CREATED (Tenant) | CONFIRMED | Other Status |
|------|------------------|------------------|-----------|--------------|
| **Mall Manager** | Socket only | ❌ | ❌ | ❌ |
| **Staff** | ❌ | Socket + Email | ❌ | Socket only |
| **Kitchen** | ❌ | ❌ | Socket + Email + FCM + TTS | Socket only |
| **Admin** | Socket only | Socket + Email | Socket + Email + FCM | Socket only |

---

## Component Architecture

### Backend Components

```mermaid
flowchart TD
    subgraph Controllers["CONTROLLERS LAYER"]
        MTC["MallTabsController<br/>_create()<br/>update()"]
        MSC["MallSessionController<br/>getSessionAuth()<br/>getNotifications()"]
        MSTC["MallStoresController<br/>assistance()"]
    end

    subgraph Traits["TRAITS LAYER"]
        MTHT["MallTabHelpersTrait<br/>createMasterTab() - Creates aggregator tab for mall manager<br/>createTenantTab() - Creates individual store tabs<br/>buildProductSummary() - Generates 'un Bulgogi, dos Bibimbap' text<br/>groupProductsByTenant() - Splits order by restaurant"]
    end

    subgraph Services["SERVICES LAYER"]
        TNS["TabsNotificationService<br/>handleStatusChange() - Main entry point for status changes<br/>sendNotification() - Dispatches TabChannelNotification<br/>enrichNotificationDataWithOrderDetails() - Adds order info for email<br/>speechOrderProducts() - Generates TTS speech text<br/><br/>KEY LOGIC:<br/>Master tabs (is_master_tab) - Socket only, NO email<br/>Tenant CREATED - Socket + Email to staff<br/>Tenant CONFIRMED - Socket + Email + FCM + TTS to kitchen"]
    end

    subgraph Notifications["NOTIFICATIONS LAYER"]
        MSTCN["MallSessionTabCreationNotification<br/>Channels: socket: true, push: true (tenant only), mail: false"]
        TCN["TabChannelNotification<br/>Channels: socket: true, mail: true (conditional), push: true (CONFIRMED only), database: true"]
        MSAN["MallStoreAssistanceNotification<br/>Channels: socket: true, push: true, mail: false"]
        MSOSN["MallSessionOrderStatusNotification<br/>(For customer-facing status updates)"]
    end

    subgraph Builder["NOTIFICATION BUILDER (Core)"]
        ANB["AppNotificationBuilder::send()<br/>Parameters: notificationClass, channel (e.g. tenant.2.system), scope (channel/private/public), targets (kitchen/staff/admin), targetType (role/user), individual (push/mail), config.channels, data (tts, alarm, speech, etc.)"]
    end

    MTC --> MTHT
    Traits --> Services
    Services --> Notifications
    Notifications --> Builder
```

### Frontend Components

```mermaid
flowchart LR
    subgraph Electron["ELECTRON DESKTOP APP"]
        WSClient["WebSocket Client (LaravelEchoContext)<br/>Pusher/Soketi, Channel Subscribe, Event Handling"]
        PyService["Python Service (kt_service.py)<br/>TTS Generation, Alarm Playback, Audio Player"]
        ReactAdmin["React Admin App (KitchnTabs)<br/>TabsListView, OrderDetails, Notifications"]
        WSClient --> PyService
        PyService --> ReactAdmin
    end

    subgraph Mobile["MOBILE APP (Android/iOS)"]
        FCMService["FCM Service (Push Handler)<br/>Background Push, Notification Display"]
        Capacitor["Capacitor App (React-Admin)<br/>Native Push, WebView UI"]
        FCMService --> Capacitor
    end

    subgraph MallClient["MALL CLIENT (Customer PWA)"]
        MSEchoContext["MallSessionEchoContext<br/>Status Updates, WebSocket Events"]
        MallClientTabsList["MallClientTabsList<br/>Order Status, Progress Bars, Notifications"]
        MSEchoContext --> MallClientTabsList
    end
```

---

## Detailed Event Flows

### Flow 1: Customer Creates Mall Order

```mermaid
flowchart TD
    A["Customer App: POST /api/public/mall/tab<br/>{ products: [...], customer_name: 'Francisco', table_number: '8' }"] --> B["MallTabsController._create() - BACKEND PROCESSING"]
    B --> C["1. groupProductsByTenant()<br/>Products split: Restaurant A (2 items), Restaurant B (1 item)"]
    C --> D["2. createMasterTab() - Mall Manager Tenant<br/>Tab created: is_master_tab = true<br/>Order created with ALL products (aggregated)"]
    D --> D1["NOTIFICATION: MallSessionTabCreationNotification<br/>Channel: tenant.{mall_manager_id}.system<br/>Socket: yes (UI refresh only)<br/>Email: no, FCM Push: no, TTS: no (tts='false')<br/>Targets: ['kitchen', 'staff']"]
    C --> E["3. createTenantTab() - Restaurant A<br/>Tab created: master_tab_id = {master_tab.id}<br/>Order created with Restaurant A products only<br/>buildProductSummary() -> 'un Bulgogi, dos Bibimbap'"]
    E --> E1["NOTIFICATION: MallSessionTabCreationNotification<br/>Channel: tenant.{restaurant_a_id}.system<br/>Socket: yes, Email: no<br/>FCM Push: yes individual: ['push']<br/>TTS: yes (tts='true', speech='Nuevo pedido...')<br/>Alarm: yes (alarm='true')<br/>Targets: ['kitchen', 'staff']<br/>Title: 'Nuevo pedido en la mesa 8'<br/>Message: 'Francisco: un Bulgogi, dos Bibimbap'"]
    C --> F["4. createTenantTab() - Restaurant B<br/>(Same as Restaurant A, different tenant channel)"]
    D1 --> G["STEP 2: Tab Status Change triggers TabChannelNotification<br/>TabsNotificationService.handleStatusChange()"]
    E1 --> G
    F --> G
    G --> H["MASTER TAB (is_master_tab = true)<br/>Status: CREATED<br/>Channels: socket=yes, mail=no, push=no<br/>Recipients: None (socket only for UI)<br/>Reason: Master tabs are aggregators, not operational orders"]
    G --> I["TENANT TAB (is_master_tab = false)<br/>Status: CREATED<br/>Channels: socket=yes, mail=yes, push=no<br/>Recipients: staff (for CREATED status)<br/>Email includes: order_items, customer info, tenant logo"]
```

### Flow 2: Staff Confirms Order

```mermaid
sequenceDiagram
    participant Staff as Staff Dashboard
    participant Tabs as TabsController.updateStatus()
    participant Service as TabsNotificationService.handleStatusChange()
    participant Kitchen as Kitchen Staff / Desktop App

    Staff->>Tabs: PUT /api/tabs/{id} { status: "CONFIRMED" }
    Tabs->>Service: handleStatusChange() - TENANT TAB Status CREATED -> CONFIRMED
    Service->>Service: 1. Update tab.status = 'CONFIRMED'
    Service->>Service: 2. Update tab.date_confirmed = now()
    Service->>Service: 3. Update associated order status
    Service->>Service: 4. If has master_tab_id, update master order products
    Service->>Kitchen: 5. NOTIFICATION TabChannelNotification<br/>Channel tenant.{tenant_id}.system<br/>Socket yes, Email yes (full order details with tenant logo)<br/>FCM Push yes individual ["push","mail"]<br/>TTS yes (tts='true', tts_delay=10), Alarm yes<br/>Targets ['kitchen'] (CONFIRMED -> kitchen only for mall orders)<br/>Title "[RESTAURANT] Orden Confirmada"<br/>Message Speech text with order items
    Kitchen->>Kitchen: 6. Recipients receive - Kitchen staff FCM push + Email + TTS speech; Desktop app WebSocket + Alarm sound + TTS
```

---

## Delivery Channels

### Channel Details

| Channel | Technology | Use Case | Backend Component |
|---------|------------|----------|-------------------|
| **Socket** | Pusher/Soketi WebSocket | Real-time UI updates | `AppNotification` event broadcast |
| **Email** | SMTP (Laravel Mail) | Order confirmations, receipts | `toMail()` method in notification |
| **FCM Push** | Firebase Cloud Messaging | Mobile app background notifications | `toFcm()` method via `individual: ["push"]` |
| **TTS/Speech** | Python `gTTS` service | Voice announcements in kitchen | WebSocket → Python → Audio playback |
| **Database** | MySQL `notifications` table | Notification history, user inbox | `toDatabase()` method |

### Channel Configuration in Code

```php
// Notification class static config
public static function config()
{
    return [
        "name"     => TabChannelNotification::class,
        "active"   => true,
        "channels" => [
            "socket"   => true,   // WebSocket broadcast
            "mail"     => true,   // Email delivery
            "database" => true,   // Store in notifications table
            "push"     => true,   // FCM push (requires individual: ["push"])
        ],
        "mailView" => "notifications.tab_order",
    ];
}

// Per-send override in AppNotificationBuilder
AppNotificationBuilder::send(
    config: [
        'channels' => [
            "socket"   => true,
            "mail"     => false,  // Disable email for this send
            "database" => false,
            "push"     => true,
        ],
    ],
    individual: ["push"],  // Enable per-user FCM delivery
);
```

---

## Role-Based Targeting

### Role Definitions

| Role | Description | Typical Users |
|------|-------------|---------------|
| **admin** | Full system access | Restaurant owner, manager |
| **staff** | Front-of-house staff | Waiters, cashiers |
| **kitchen** | Kitchen staff | Cooks, kitchen manager |

### Targeting Rules for Mall Orders

```php
// In TabsNotificationService::sendNotification()

$isMallOrder = !empty($tab->mall_id) || !empty($tab->master_tab_id);

if ($isMallOrder && isset($data['new'])) {
    if ($data['new'] === Tab::STATUS_CREATED) {
        $targets = ['staff'];  // Staff receives CREATED notifications
    } elseif ($data['new'] === Tab::STATUS_CONFIRMED) {
        $targets = ['kitchen'];  // Kitchen receives CONFIRMED notifications
    }
} else {
    $targets = ['kitchen', 'staff', 'admin'];  // Regular orders: all roles
}
```

### Targeting Flow Diagram

```mermaid
flowchart TD
    A["Order Type & Status"] --> B{Order Type?}
    B -->|Mall Order - CREATED| C1["(tenant tab)<br/>Target Roles: ['staff']<br/>Delivery: Socket + Email"]
    B -->|Mall Order - CONFIRMED| C2["(tenant tab)<br/>Target Roles: ['kitchen']<br/>Delivery: Socket + Email + FCM + TTS"]
    B -->|Mall Order - Other Status| C3["(master tab)<br/>Target Roles: ['kitchen', 'staff']<br/>Delivery: Socket only"]
    B -->|Regular Order - Any Status| C4["Target Roles: ['kitchen', 'staff', 'admin']<br/>Delivery: Per status config"]
```

---

## Code Component Reference

### File Locations

| Component | Path |
|-----------|------|
| **MallTabsController** | `domain/app/Http/Controllers/API/Mall/MallTabs/MallTabsController.php` |
| **MallTabHelpersTrait** | `domain/app/Traits/Mall/MallTabHelpersTrait.php` |
| **TabsNotificationService** | `domain/app/Services/Tabs/TabsNotificationService.php` |
| **MallSessionTabCreationNotification** | `domain/app/Notifications/MallSessionTabCreationNotification.php` |
| **TabChannelNotification** | `domain/app/Notifications/Tab/TabChannelNotification.php` |
| **MallStoreAssistanceNotification** | `domain/app/Notifications/Mall/MallStoreAssistanceNotification.php` |
| **AppNotificationBuilder** | `app/AppNotifications/AppNotificationBuilder.php` |
| **Python TTS Service** | `dash-python-service/src/kt_service.py` |
| **Frontend Echo Context** | `packages/dash-admin/src/contexts/com/LaravelEchoContext.tsx` |

### Key Methods

#### MallTabHelpersTrait

```php
/**
 * Creates master tab (aggregator) for mall manager
 * - Socket only notification (no email, no FCM)
 * - TTS disabled
 */
private function createMasterTab(...): Tab

/**
 * Creates tenant tab for individual restaurant
 * - FCM push + TTS + Alarm enabled
 * - Includes product summary in message
 */
private function createTenantTab(...): Tab

/**
 * Generates "un Bulgogi, dos Bibimbap" text
 */
private function buildProductSummary(array $products): string
```

#### TabsNotificationService

```php
/**
 * Main entry point for status change notifications
 * - Validates transition
 * - Updates tab and order status
 * - Dispatches appropriate notification
 */
public function handleStatusChange(Tab $tab, string $newStatus, bool $silent = false): Tab

/**
 * Determines channels and targets based on:
 * - Tab type (master vs tenant)
 * - Status (CREATED, CONFIRMED, etc.)
 * - Marketplace type (Uber vs others)
 */
private function sendNotification(Tab $tab, array $data, ...): void
```

---

## Summary: Email Recipients by Scenario

### Single Mall Session Order (Customer orders from 1 restaurant)

| Email | Recipient | When | Content |
|-------|-----------|------|---------|
| ❌ | Mall Manager | - | No email (master tab) |
| ✅ | Store Staff | CREATED | Order received |
| ✅ | Store Kitchen | CONFIRMED | Order confirmed, ready to prepare |

### Multi-Restaurant Mall Session Order (Customer orders from 2 restaurants)

| Email | Recipient | When | Content |
|-------|-----------|------|---------|
| ❌ | Mall Manager | - | No email (master tab) |
| ✅ | Restaurant A Staff | CREATED | Restaurant A items |
| ✅ | Restaurant A Kitchen | CONFIRMED | Restaurant A items |
| ✅ | Restaurant B Staff | CREATED | Restaurant B items |
| ✅ | Restaurant B Kitchen | CONFIRMED | Restaurant B items |

---

## Troubleshooting

### Common Issues

1. **Mall manager receiving emails**: Check `is_master_tab` field on tab
2. **Missing FCM notifications**: Ensure `individual: ["push"]` is set
3. **TTS not playing**: Check `tts` flag is `'true'` (string, not boolean)
4. **Duplicate notifications**: Check for multiple notification sends in code path

### Debug Logging

```php
// Enable notifications channel logging
Log::channel('notifications')->info("...", $data);

// Check Laravel logs
tail -f storage/logs/laravel.log | grep -i notification
```

---

*Last Updated: December 2025*
*Version: 1.0*
