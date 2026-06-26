---
layout: default
title: F5-Customer-Self-Service MALL SESSION NOTIFICATIONS FLOW
---

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

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           MALL SESSION NOTIFICATION SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────────────────┐   │
│  │   Customer      │     │   Mall Session  │     │        Notification             │   │
│  │   (Mobile App)  │────▶│   Controller    │────▶│        Builder                  │   │
│  │                 │     │                 │     │   AppNotificationBuilder        │   │
│  └─────────────────┘     └─────────────────┘     └──────────────┬──────────────────┘   │
│                                                                  │                       │
│                          ┌───────────────────────────────────────┼───────────────────┐  │
│                          │                                       │                   │  │
│                          ▼                                       ▼                   ▼  │
│               ┌─────────────────┐                    ┌──────────────┐    ┌──────────────┐
│               │   WebSocket     │                    │    Email     │    │    FCM       │
│               │   (Pusher)      │                    │   (SMTP)     │    │   (Push)     │
│               └────────┬────────┘                    └──────┬───────┘    └──────┬───────┘
│                        │                                    │                   │       │
│         ┌──────────────┼──────────────┐                     │                   │       │
│         │              │              │                     │                   │       │
│         ▼              ▼              ▼                     ▼                   ▼       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  Electron   │ │   React     │ │   Python    │    │   Staff     │    │   Mobile    │ │
│  │  Desktop    │ │   Browser   │ │   Service   │    │   Email     │    │   Device    │ │
│  │  (Kitchen)  │ │   (Admin)   │ │   (TTS)     │    │   Inbox     │    │   (FCM)     │ │
│  └─────────────┘ └─────────────┘ └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Notification Flow Diagram

### Mall Session Order Creation Flow

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         MALL SESSION ORDER CREATION FLOW                                  │
└──────────────────────────────────────────────────────────────────────────────────────────┘

  CUSTOMER                   BACKEND                            RECIPIENTS
  ────────                   ───────                            ──────────

  ┌───────────┐
  │  Scan QR  │
  │  Code     │
  └─────┬─────┘
        │
        │  1. Create Session
        ▼
  ┌───────────────┐
  │ Select Items  │
  │ from Multiple │
  │ Restaurants   │
  └───────┬───────┘
        │
        │  2. Submit Order
        ▼
  ┌───────────────┐         ┌─────────────────────────────────────────────────────────────┐
  │  MallTabs     │────────▶│                    NOTIFICATION DISPATCH                    │
  │  Controller   │         │                                                             │
  │  ._create()   │         │  ┌─────────────────────────────────────────────────────┐   │
  └───────────────┘         │  │  1. CREATE MASTER TAB (Mall Manager Tenant)          │   │
                            │  │     └─▶ Socket ONLY (UI refresh)                     │   │
                            │  │         ❌ No Email, ❌ No FCM Push                   │   │
                            │  └─────────────────────────────────────────────────────┘   │
                            │                                                             │
                            │  ┌─────────────────────────────────────────────────────┐   │
                            │  │  2. CREATE TENANT TAB (Per Restaurant)               │   │
                            │  │     └─▶ MallSessionTabCreationNotification           │   │────▶ 🔔 Staff
                            │  │         ✅ Socket (UI refresh)                       │   │────▶ 🔔 Kitchen
                            │  │         ✅ FCM Push (mobile notification)            │   │
                            │  │         ✅ TTS Speech (Python service)               │   │
                            │  │         ✅ Alarm (frontend sound)                    │   │
                            │  └─────────────────────────────────────────────────────┘   │
                            │                                                             │
                            │  ┌─────────────────────────────────────────────────────┐   │
                            │  │  3. TAB STATUS CHANGE (TabChannelNotification)       │   │
                            │  │     CREATED Status:                                  │   │
                            │  │       • Master Tab: Socket ONLY                      │   │────▶ ❌ Mall Manager
                            │  │       • Tenant Tab: Socket + Email                   │   │────▶ ✅ Store Staff
                            │  │     CONFIRMED Status:                                │   │
                            │  │       • Tenant Tab: Socket + Email + FCM + TTS       │   │────▶ ✅ Kitchen
                            │  └─────────────────────────────────────────────────────┘   │
                            │                                                             │
                            └─────────────────────────────────────────────────────────────┘
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

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND COMPONENT DIAGRAM                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            CONTROLLERS LAYER                                     │   │
│   │                                                                                  │   │
│   │  ┌─────────────────────┐    ┌─────────────────────┐    ┌────────────────────┐   │   │
│   │  │ MallTabsController  │    │ MallSessionController│   │ MallStoresController│   │   │
│   │  │                     │    │                      │   │                     │   │   │
│   │  │ • _create()         │    │ • getSessionAuth()   │   │ • assistance()      │   │   │
│   │  │ • update()          │    │ • getNotifications() │   │                     │   │   │
│   │  └──────────┬──────────┘    └──────────────────────┘   └─────────────────────┘   │   │
│   │             │                                                                     │   │
│   └─────────────┼─────────────────────────────────────────────────────────────────────┘   │
│                 │                                                                         │
│                 ▼                                                                         │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              TRAITS LAYER                                        │   │
│   │                                                                                  │   │
│   │  ┌──────────────────────────────────────────────────────────────────────────┐   │   │
│   │  │                     MallTabHelpersTrait                                   │   │   │
│   │  │                                                                           │   │   │
│   │  │  • createMasterTab()     - Creates aggregator tab for mall manager       │   │   │
│   │  │  • createTenantTab()     - Creates individual store tabs                  │   │   │
│   │  │  • buildProductSummary() - Generates "un Bulgogi, dos Bibimbap" text     │   │   │
│   │  │  • groupProductsByTenant() - Splits order by restaurant                   │   │   │
│   │  │                                                                           │   │   │
│   │  └──────────────────────────────────────────────────────────────────────────┘   │   │
│   │                                                                                  │   │
│   └──────────────────────────────────────────────────────────────────────────────────┘   │
│                 │                                                                         │
│                 ▼                                                                         │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            SERVICES LAYER                                        │   │
│   │                                                                                  │   │
│   │  ┌──────────────────────────────────────────────────────────────────────────┐   │   │
│   │  │                   TabsNotificationService                                 │   │   │
│   │  │                                                                           │   │   │
│   │  │  • handleStatusChange()          - Main entry point for status changes   │   │   │
│   │  │  • sendNotification()            - Dispatches TabChannelNotification     │   │   │
│   │  │  • enrichNotificationDataWithOrderDetails() - Adds order info for email │   │   │
│   │  │  • speechOrderProducts()         - Generates TTS speech text             │   │   │
│   │  │                                                                           │   │   │
│   │  │  KEY LOGIC:                                                               │   │   │
│   │  │  • Master tabs ($tab->is_master_tab) → Socket only, NO email             │   │   │
│   │  │  • Tenant CREATED → Socket + Email to staff                              │   │   │
│   │  │  • Tenant CONFIRMED → Socket + Email + FCM + TTS to kitchen              │   │   │
│   │  │                                                                           │   │   │
│   │  └──────────────────────────────────────────────────────────────────────────┘   │   │
│   │                                                                                  │   │
│   └──────────────────────────────────────────────────────────────────────────────────┘   │
│                 │                                                                         │
│                 ▼                                                                         │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          NOTIFICATIONS LAYER                                     │   │
│   │                                                                                  │   │
│   │  ┌────────────────────────────┐  ┌─────────────────────────────────────────┐   │   │
│   │  │ MallSessionTabCreation     │  │ TabChannelNotification                  │   │   │
│   │  │ Notification               │  │                                          │   │   │
│   │  │                            │  │ Channels:                                │   │   │
│   │  │ Channels:                  │  │ • socket: true                           │   │   │
│   │  │ • socket: true             │  │ • mail: true (conditional)              │   │   │
│   │  │ • push: true (tenant only) │  │ • push: true (CONFIRMED only)           │   │   │
│   │  │ • mail: false              │  │ • database: true                        │   │   │
│   │  │                            │  │                                          │   │   │
│   │  └────────────────────────────┘  └─────────────────────────────────────────┘   │   │
│   │                                                                                  │   │
│   │  ┌────────────────────────────┐  ┌─────────────────────────────────────────┐   │   │
│   │  │ MallStoreAssistance        │  │ MallSessionOrderStatus                  │   │   │
│   │  │ Notification               │  │ Notification                            │   │   │
│   │  │                            │  │                                          │   │   │
│   │  │ Channels:                  │  │ (For customer-facing status updates)    │   │   │
│   │  │ • socket: true             │  │                                          │   │   │
│   │  │ • push: true               │  │                                          │   │   │
│   │  │ • mail: false              │  │                                          │   │   │
│   │  └────────────────────────────┘  └─────────────────────────────────────────┘   │   │
│   │                                                                                  │   │
│   └──────────────────────────────────────────────────────────────────────────────────┘   │
│                 │                                                                         │
│                 ▼                                                                         │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      NOTIFICATION BUILDER (Core)                                 │   │
│   │                                                                                  │   │
│   │  ┌──────────────────────────────────────────────────────────────────────────┐   │   │
│   │  │                    AppNotificationBuilder::send()                         │   │   │
│   │  │                                                                           │   │   │
│   │  │  Parameters:                                                              │   │   │
│   │  │  • notificationClass - Which notification class to use                   │   │   │
│   │  │  • channel           - WebSocket channel (e.g., "tenant.2.system")       │   │   │
│   │  │  • scope             - "channel" | "private" | "public"                  │   │   │
│   │  │  • targets           - ['kitchen', 'staff', 'admin']                     │   │   │
│   │  │  • targetType        - "role" | "user"                                   │   │   │
│   │  │  • individual        - ["push", "mail"] for per-user delivery            │   │   │
│   │  │  • config.channels   - Override notification channels                     │   │   │
│   │  │  • data              - Notification payload (tts, alarm, speech, etc.)   │   │   │
│   │  │                                                                           │   │   │
│   │  └──────────────────────────────────────────────────────────────────────────┘   │   │
│   │                                                                                  │   │
│   └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Frontend Components

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND COMPONENT DIAGRAM                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                             ELECTRON DESKTOP APP                                    │ │
│  │                                                                                     │ │
│  │  ┌─────────────────────┐    ┌─────────────────────┐    ┌───────────────────────┐  │ │
│  │  │   React Admin App   │    │    Python Service   │    │   WebSocket Client    │  │ │
│  │  │   (KitchnTabs)      │    │    (kt_service.py)  │    │   (LaravelEchoContext)│  │ │
│  │  │                     │    │                     │    │                        │  │ │
│  │  │  • TabsListView     │    │  • TTS Generation   │    │  • Pusher/Soketi      │  │ │
│  │  │  • OrderDetails     │◀───│  • Alarm Playback   │◀───│  • Channel Subscribe  │  │ │
│  │  │  • Notifications    │    │  • Audio Player     │    │  • Event Handling     │  │ │
│  │  │                     │    │                     │    │                        │  │ │
│  │  └─────────────────────┘    └─────────────────────┘    └───────────────────────┘  │ │
│  │                                                                                     │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                               MOBILE APP (Android/iOS)                              │ │
│  │                                                                                     │ │
│  │  ┌─────────────────────┐    ┌─────────────────────┐                                │ │
│  │  │    Capacitor App    │    │   FCM Service       │                                │ │
│  │  │    (React-Admin)    │    │   (Push Handler)    │                                │ │
│  │  │                     │    │                     │                                │ │
│  │  │  • Native Push      │◀───│  • Background Push  │                                │ │
│  │  │  • WebView UI       │    │  • Notification     │                                │ │
│  │  │                     │    │    Display          │                                │ │
│  │  └─────────────────────┘    └─────────────────────┘                                │ │
│  │                                                                                     │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              MALL CLIENT (Customer PWA)                             │ │
│  │                                                                                     │ │
│  │  ┌─────────────────────┐    ┌─────────────────────┐                                │ │
│  │  │  MallSessionEcho    │    │  MallClientTabsList │                                │ │
│  │  │  Context            │    │                     │                                │ │
│  │  │                     │    │  • Order Status     │                                │ │
│  │  │  • Status Updates   │───▶│  • Progress Bars    │                                │ │
│  │  │  • WebSocket Events │    │  • Notifications    │                                │ │
│  │  │                     │    │                     │                                │ │
│  │  └─────────────────────┘    └─────────────────────┘                                │ │
│  │                                                                                     │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Event Flows

### Flow 1: Customer Creates Mall Order

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FLOW 1: CUSTOMER CREATES MALL ORDER                              │
└────────────────────────────────────────────────────────────────────────────────────────┘

  STEP 1: Customer submits order with items from Restaurant A and Restaurant B
  ═══════════════════════════════════════════════════════════════════════════

  Customer App                    MallTabsController._create()
  ────────────                    ─────────────────────────────
       │
       │  POST /api/public/mall/tab
       │  {
       │    products: [...],
       │    customer_name: "Francisco",
       │    table_number: "8"
       │  }
       │
       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         BACKEND PROCESSING                               │
  │                                                                          │
  │  1. groupProductsByTenant()                                              │
  │     └─▶ Products split: Restaurant A (2 items), Restaurant B (1 item)   │
  │                                                                          │
  │  2. createMasterTab() - Mall Manager Tenant                              │
  │     ├─▶ Tab created: is_master_tab = true                               │
  │     ├─▶ Order created with ALL products (aggregated)                    │
  │     │                                                                    │
  │     └─▶ NOTIFICATION: MallSessionTabCreationNotification                │
  │         ├─ Channel: tenant.{mall_manager_id}.system                     │
  │         ├─ Socket: ✅ (UI refresh only)                                 │
  │         ├─ Email: ❌                                                     │
  │         ├─ FCM Push: ❌                                                  │
  │         ├─ TTS: ❌ (tts='false')                                        │
  │         └─ Targets: ['kitchen', 'staff']                                │
  │                                                                          │
  │  3. createTenantTab() - Restaurant A                                     │
  │     ├─▶ Tab created: master_tab_id = {master_tab.id}                    │
  │     ├─▶ Order created with Restaurant A products only                   │
  │     ├─▶ buildProductSummary() → "un Bulgogi, dos Bibimbap"              │
  │     │                                                                    │
  │     └─▶ NOTIFICATION: MallSessionTabCreationNotification                │
  │         ├─ Channel: tenant.{restaurant_a_id}.system                     │
  │         ├─ Socket: ✅                                                    │
  │         ├─ Email: ❌                                                     │
  │         ├─ FCM Push: ✅ individual: ["push"]                            │
  │         ├─ TTS: ✅ (tts='true', speech='Nuevo pedido...')               │
  │         ├─ Alarm: ✅ (alarm='true')                                     │
  │         ├─ Targets: ['kitchen', 'staff']                                │
  │         ├─ Title: "Nuevo pedido en la mesa 8"                           │
  │         └─ Message: "Francisco: un Bulgogi, dos Bibimbap"               │
  │                                                                          │
  │  4. createTenantTab() - Restaurant B                                     │
  │     └─▶ (Same as Restaurant A, different tenant channel)                │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘

  STEP 2: Tab Status Change triggers TabChannelNotification
  ══════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    TabsNotificationService.handleStatusChange()          │
  │                                                                          │
  │  For each tab (master + tenant tabs):                                    │
  │                                                                          │
  │  MASTER TAB (is_master_tab = true):                                      │
  │  ─────────────────────────────────                                       │
  │  • Status: CREATED                                                       │
  │  • Channels: socket=✅, mail=❌, push=❌                                  │
  │  • Recipients: None (socket only for UI)                                 │
  │  • Reason: Master tabs are aggregators, not operational orders           │
  │                                                                          │
  │  TENANT TAB (is_master_tab = false):                                     │
  │  ────────────────────────────────────                                    │
  │  • Status: CREATED                                                       │
  │  • Channels: socket=✅, mail=✅, push=❌                                  │
  │  • Recipients: staff (for CREATED status)                                │
  │  • Email includes: order_items, customer info, tenant logo               │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

### Flow 2: Staff Confirms Order

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          FLOW 2: STAFF CONFIRMS ORDER                                   │
└────────────────────────────────────────────────────────────────────────────────────────┘

  Staff Dashboard                 TabsController.updateStatus()
  ───────────────                 ─────────────────────────────
       │
       │  PUT /api/tabs/{id}
       │  { status: "CONFIRMED" }
       │
       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    TabsNotificationService.handleStatusChange()          │
  │                                                                          │
  │  TENANT TAB - Status: CREATED → CONFIRMED                                │
  │  ────────────────────────────────────────                                │
  │                                                                          │
  │  1. Update tab.status = 'CONFIRMED'                                      │
  │  2. Update tab.date_confirmed = now()                                    │
  │  3. Update associated order status                                       │
  │  4. If has master_tab_id → update master order products                  │
  │                                                                          │
  │  5. NOTIFICATION: TabChannelNotification                                 │
  │     ├─ Channel: tenant.{tenant_id}.system                               │
  │     ├─ Socket: ✅                                                        │
  │     ├─ Email: ✅ (full order details with tenant logo)                  │
  │     ├─ FCM Push: ✅ individual: ["push", "mail"]                        │
  │     ├─ TTS: ✅ (tts='true', tts_delay=10)                               │
  │     ├─ Alarm: ✅ (alarm='true')                                         │
  │     ├─ Targets: ['kitchen'] (CONFIRMED → kitchen only for mall orders)  │
  │     ├─ Title: "[RESTAURANT] Orden Confirmada"                           │
  │     └─ Message: Speech text with order items                            │
  │                                                                          │
  │  6. Recipients receive:                                                  │
  │     • Kitchen staff: FCM push + Email + TTS speech                      │
  │     • Desktop app: WebSocket + Alarm sound + TTS                        │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
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

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ROLE-BASED TARGETING FLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Order Type        Status           Target Roles        Delivery            │
│   ──────────        ──────           ────────────        ────────            │
│                                                                              │
│   Mall Order        CREATED    ───▶  ['staff']     ───▶  Socket + Email     │
│   (tenant tab)                                                               │
│                                                                              │
│   Mall Order        CONFIRMED  ───▶  ['kitchen']   ───▶  Socket + Email +   │
│   (tenant tab)                                           FCM + TTS          │
│                                                                              │
│   Mall Order        Other      ───▶  ['kitchen',   ───▶  Socket only        │
│   (master tab)      Status          'staff']                                │
│                                                                              │
│   Regular Order     Any        ───▶  ['kitchen',   ───▶  Per status config  │
│                                       'staff',                               │
│                                       'admin']                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
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
