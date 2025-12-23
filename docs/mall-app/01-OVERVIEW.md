---
title: Mall App - Overview
layout: default
nav_order: 1
parent: Mall Application
---

# KitchnTabs Mall App - Technical Documentation

## Overview

The KitchnTabs Mall App is a full-stack solution for food court/mall ordering systems. It enables customers to scan QR codes at tables, browse multiple restaurant menus, place orders, and receive real-time status updates - all without authentication.

## Key Features

### For Customers (Mall Client)
- **QR Code Access**: Scan a QR code to start a session without login
- **Multi-Tenant Ordering**: Browse and order from multiple restaurants in one transaction
- **Real-Time Updates**: WebSocket notifications for order status changes
- **Order Tracking**: View order progress per restaurant
- **Staff Assistance**: Request help from restaurant staff

### For Restaurant Staff (Tenant Admin)
- **Order Management**: View and manage incoming orders
- **Status Updates**: Update order status (confirmed → preparing → ready → delivered)
- **Push Notifications**: Receive alerts for new orders and assistance requests

### For Mall Administrators
- **Mall Management**: Configure mall settings, manage tenant relationships
- **Session Monitoring**: View active sessions, statistics
- **QR Code Generation**: Generate QR codes for tables/locations

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Laravel 11, PHP 8.2 |
| **Frontend** | React 18, React-Admin, TypeScript |
| **Real-Time** | Laravel Echo, Pusher/Soketi WebSockets |
| **Database** | MySQL/PostgreSQL |
| **Push Notifications** | Firebase Cloud Messaging (FCM) |
| **Build** | Vite, pnpm workspaces |

## Project Structure

```
DASH-PW-PROJECT/
├── dash-backend/                    # Laravel API
│   ├── app/                         # Core application code
│   │   └── AppNotifications/        # Notification system
│   └── domain/                      # Domain-driven design
│       ├── app/
│       │   ├── Http/Controllers/API/Mall/  # Mall controllers
│       │   ├── Models/Mall/         # Mall models
│       │   ├── Notifications/Mall/  # Mall notifications
│       │   └── Services/Mall/       # Mall services
│       └── routes/api/              # API routes
│
└── dash-frontend/                   # React frontend
    ├── apps/
    │   └── kitchntabs-mall/         # Mall application
    │       └── src/
    │           ├── components/mall/ # Mall wrappers
    │           └── dash-extensions/ # Data/Auth providers
    └── packages/
        └── kt-mall/                 # Mall components package
            └── src/
                ├── components/      # Mall UI components
                └── schemas/         # Resource schemas
```

## Core Concepts

### 1. Mall Session
A temporary session created when a customer scans a QR code. Identified by a unique 5-character hash (e.g., "M5U2W").

### 2. Master Tab / Tenant Tabs
- **Master Tab**: The main order aggregating all items from different restaurants
- **Tenant Tabs**: Individual orders per restaurant, linked to the master tab

### 3. Brokerable Relationship
Orders are polymorphically linked to MallSession via `brokerable_type` and `brokerable_id`.

### 4. Real-Time Notifications
WebSocket channels per session deliver instant status updates without polling.

## Documentation Index

1. [Overview](./01-OVERVIEW.md) - This document
2. [Architecture](./02-ARCHITECTURE.md) - System architecture and components
3. [Backend Models](./03-BACKEND-MODELS.md) - Database models and relationships
4. [Backend Controllers](./04-BACKEND-CONTROLLERS.md) - API controllers and routes
5. [Backend Services](./05-BACKEND-SERVICES.md) - Business logic services
6. [Notifications](./06-NOTIFICATIONS.md) - Real-time notification system
7. [Frontend Architecture](./07-FRONTEND-ARCHITECTURE.md) - React application structure
8. [Frontend Components](./08-FRONTEND-COMPONENTS.md) - UI components
9. [User Stories](./09-USER-STORIES.md) - User flows and scenarios
10. [Flow Diagrams](./10-FLOW-DIAGRAMS.md) - Visual flow representations
