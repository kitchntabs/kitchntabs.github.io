---
layout: default
title: F15-Notifications-Messaging DASH NOTIFICATIONS CATALOG
---

# Dash Notifications Catalog

This document lists all notifications sent by the KitchnTabs system, including their purpose, when they occur, who receives them, and through which channels they are delivered.

---

## Channel Legend

| Icon | Channel | Description |
|:----:|---------|-------------|
| 🔌 | **Socket** | Real-time notification via WebSocket |
| 📧 | **Email** | Email notification |
| 💾 | **Database** | Stored in database for history/retrieval |
| 📱 | **Push (FCM)** | Mobile push notification via Firebase |

---

## Orders & Tabs

### Order Status Notification

| Property | Value |
|----------|-------|
| **Name** | Tab Channel Notification |
| **Subject** | "Nueva Orden #123" / "Orden Actualizada" |
| **When it occurs** | When an order is created, confirmed, in preparation, prepared, delivered, or closed |
| **Target** | Kitchen staff, waitstaff, and administrators |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database • 📱 Push |

---

### Tab Status Notification

| Property | Value |
|----------|-------|
| **Name** | Tab Status Notification |
| **Subject** | "Estado de Orden Actualizado" |
| **When it occurs** | When a tab/order status changes |
| **Target** | Public (POS displays) |
| **Channels** | 🔌 Socket |

---

## Mall / Food Court

### Mall Session Order Status

| Property | Value |
|----------|-------|
| **Name** | Mall Session Order Status Notification |
| **Subject** | "Tu orden está en preparación" / "Tu orden está lista" |
| **When it occurs** | When a restaurant updates the status of a customer's order in a food court |
| **Target** | Customer (via their session) |
| **Channels** | 🔌 Socket • 💾 Database |

---

### Mall Order Created

| Property | Value |
|----------|-------|
| **Name** | Mall Session Tab Creation Notification |
| **Subject** | "Nueva orden recibida" |
| **When it occurs** | When a customer places an order at a food court via QR code |
| **Target** | Restaurant staff |
| **Channels** | 🔌 Socket • 💾 Database • 📱 Push |

---

### Mall Order Updated

| Property | Value |
|----------|-------|
| **Name** | Mall Order Updated Notification |
| **Subject** | "Actualización de pedido" |
| **When it occurs** | When any update is made to a mall order |
| **Target** | Restaurant staff and managers |
| **Channels** | 🔌 Socket • 💾 Database • 📱 Push |

---

### Mall Store Assistance Request

| Property | Value |
|----------|-------|
| **Name** | Mall Store Assistance Notification |
| **Subject** | "Cliente solicita asistencia" |
| **When it occurs** | When a customer requests help from a restaurant at a food court |
| **Target** | Restaurant staff |
| **Channels** | 🔌 Socket • 📱 Push |

---

### Mall Session Notification

| Property | Value |
|----------|-------|
| **Name** | Mall Session Notification |
| **Subject** | "Notificación de sesión" |
| **When it occurs** | General mall session events |
| **Target** | Customer session |
| **Channels** | 🔌 Socket • 📱 Push |

---

## E-Commerce / Product Management

### Product Import Completed

| Property | Value |
|----------|-------|
| **Name** | Product Import Notification |
| **Subject** | "Importación masiva completada" |
| **When it occurs** | When a bulk product import job finishes successfully |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### Product Import Validation

| Property | Value |
|----------|-------|
| **Name** | Validate Product Import Notification |
| **Subject** | "Validación de importación completada" |
| **When it occurs** | When product import validation finishes |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### Product Import Progress

| Property | Value |
|----------|-------|
| **Name** | Product Import Progress Notification |
| **Subject** | "Progreso de importación: X%" |
| **When it occurs** | During product import to show progress updates |
| **Target** | User who initiated the import |
| **Channels** | 🔌 Socket |

---

### Product Import Error

| Property | Value |
|----------|-------|
| **Name** | Product Import Error Notification |
| **Subject** | "Error en importación de productos" |
| **When it occurs** | When product import encounters errors |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### Product Export Completed

| Property | Value |
|----------|-------|
| **Name** | Product Export Notification |
| **Subject** | "Exportación de productos completada" |
| **When it occurs** | When a product export job finishes successfully |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket • 📧 Email |

---

### Product Export Progress

| Property | Value |
|----------|-------|
| **Name** | Product Export Progress Notification |
| **Subject** | "Progreso de exportación: X%" |
| **When it occurs** | During product export to show progress |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket |

---

### Product Export Error

| Property | Value |
|----------|-------|
| **Name** | Product Export Error Notification |
| **Subject** | "Error en exportación de productos" |
| **When it occurs** | When product export encounters errors |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket |

---

### Low Stock Alert

| Property | Value |
|----------|-------|
| **Name** | Low Stock Notification |
| **Subject** | "Alerta de stock bajo" |
| **When it occurs** | When a product's stock falls below the configured threshold |
| **Target** | Tenant administrators |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### POS Product Update

| Property | Value |
|----------|-------|
| **Name** | Point of Sale Product Upserted Notification |
| **Subject** | "Producto actualizado desde POS" |
| **When it occurs** | When a product is created or updated from the Point of Sale system |
| **Target** | Tenant users |
| **Channels** | 🔌 Socket |

---

### POS Products Batch Update

| Property | Value |
|----------|-------|
| **Name** | Point of Sale Products Upserted Notification |
| **Subject** | "Productos actualizados desde POS" |
| **When it occurs** | When multiple products are synced from the Point of Sale system |
| **Target** | Tenant users |
| **Channels** | 🔌 Socket |

---

### POS Stock Types Sync

| Property | Value |
|----------|-------|
| **Name** | Sync Point of Sale Stock Types Notification |
| **Subject** | "Tipos de stock sincronizados" |
| **When it occurs** | When stock types are synchronized from POS |
| **Target** | Tenant users |
| **Channels** | 🔌 Socket |

---

### POS Pricelists Sync

| Property | Value |
|----------|-------|
| **Name** | Sync Point of Sale Pricelists Notification |
| **Subject** | "Listas de precios sincronizadas" |
| **When it occurs** | When pricelists are synchronized from POS |
| **Target** | Tenant users |
| **Channels** | 🔌 Socket |

---

### Normalized Import Message

| Property | Value |
|----------|-------|
| **Name** | Normalized Import Message Notification |
| **Subject** | "Mensaje de importación" |
| **When it occurs** | During normalized product import process |
| **Target** | User who initiated the import |
| **Channels** | 🔌 Socket |

---

### Normalized Import Progress

| Property | Value |
|----------|-------|
| **Name** | Normalized Import Progress Notification |
| **Subject** | "Progreso de importación normalizada" |
| **When it occurs** | During normalized import to show progress |
| **Target** | User who initiated the import |
| **Channels** | 🔌 Socket |

---

## Campaigns / Marketplace Publishing

### Campaign Product Import

| Property | Value |
|----------|-------|
| **Name** | Campaign Marketplace Product Import Notification |
| **Subject** | "Importación de productos a campaña completada" |
| **When it occurs** | When products are imported/published to a marketplace campaign |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### Campaign Product Status

| Property | Value |
|----------|-------|
| **Name** | Campaign Marketplace Product Status Notification |
| **Subject** | "Estado de producto en marketplace actualizado" |
| **When it occurs** | When a product's status changes in a marketplace (published, paused, error, etc.) |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket |

---

### Campaign Status Update

| Property | Value |
|----------|-------|
| **Name** | Campaign Status Notification |
| **Subject** | "Estado de campaña actualizado" |
| **When it occurs** | When a campaign's overall status changes |
| **Target** | Tenant users |
| **Channels** | 🔌 Socket • 💾 Database |

---

### Campaign Tracker

| Property | Value |
|----------|-------|
| **Name** | Campaign Tracker Notification |
| **Subject** | "Actualización de seguimiento de campaña" |
| **When it occurs** | During campaign processing to track progress |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket |

---

### Campaign Job Completion

| Property | Value |
|----------|-------|
| **Name** | Job Completion Notification |
| **Subject** | "Trabajo de campaña completado" |
| **When it occurs** | When a campaign background job finishes |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket |

---

### Product Removal Reminder

| Property | Value |
|----------|-------|
| **Name** | Removal Reminder Notification |
| **Subject** | "Recordatorio: Productos por eliminar de campaña" |
| **When it occurs** | Reminder before products are automatically removed from a campaign |
| **Target** | Tenant users and administrators |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### Manual Product Upsert

| Property | Value |
|----------|-------|
| **Name** | Manual Upsert Notification |
| **Subject** | "Productos actualizados manualmente en marketplace" |
| **When it occurs** | When products are manually updated/published to a marketplace |
| **Target** | Tenant administrators |
| **Channels** | 📧 Email |

---

### Manual Product Republish

| Property | Value |
|----------|-------|
| **Name** | Manual Republish Notification |
| **Subject** | "Productos republicados en marketplace" |
| **When it occurs** | When products are manually republished to a marketplace |
| **Target** | Tenant administrators |
| **Channels** | 📧 Email |

---

## Messaging / Communication

### Private Message

| Property | Value |
|----------|-------|
| **Name** | Private Message Notification |
| **Subject** | "Mensaje privado" |
| **When it occurs** | When a private message is sent to a specific user |
| **Target** | Specific user |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### Tenant Channel Message

| Property | Value |
|----------|-------|
| **Name** | Tenant Channel Message Notification |
| **Subject** | "Mensaje del canal" |
| **When it occurs** | When a message is broadcast to a tenant channel |
| **Target** | All users in the tenant channel |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### Public Message

| Property | Value |
|----------|-------|
| **Name** | Public Message Notification |
| **Subject** | "Notificación pública" |
| **When it occurs** | When a public announcement is made |
| **Target** | Public (all connected clients) |
| **Channels** | 🔌 Socket |

---

### User Private Message

| Property | Value |
|----------|-------|
| **Name** | User Private Message Notification |
| **Subject** | "Mensaje privado" |
| **When it occurs** | When a private message is sent to a tenant user |
| **Target** | Tenant user |
| **Channels** | 🔌 Socket |

---

## Testing / Development

### User Test Message

| Property | Value |
|----------|-------|
| **Name** | User Test Message Notification |
| **Subject** | "Mensaje de prueba" |
| **When it occurs** | For testing notification delivery to a user |
| **Target** | Tenant users |
| **Channels** | 🔌 Socket • 📧 Email • 💾 Database |

---

### Public Test Message

| Property | Value |
|----------|-------|
| **Name** | Public Test Message Notification |
| **Subject** | "Notificación pública de prueba" |
| **When it occurs** | For testing public notification broadcast |
| **Target** | Public |
| **Channels** | 🔌 Socket |

---

## Authentication

### Password Reset

| Property | Value |
|----------|-------|
| **Name** | Reset Password Notification |
| **Subject** | "Restablecer contraseña" |
| **When it occurs** | When a user requests a password reset |
| **Target** | The user who requested the reset |
| **Channels** | 📧 Email |

---

## Summary by Channel

### Email Notifications (📧)

| Notification | Target |
|--------------|--------|
| Tab Channel Notification | Kitchen, Staff, Admin |
| Product Import Notification | Tenant Users, Admin |
| Validate Product Import Notification | Tenant Users, Admin |
| Product Import Error Notification | Tenant Users, Admin |
| Product Export Notification | Tenant Users, Admin |
| Low Stock Notification | Tenant Admin |
| Campaign Marketplace Product Import | Tenant Users, Admin |
| Removal Reminder Notification | Tenant Users, Admin |
| Manual Upsert Notification | Tenant Admin |
| Manual Republish Notification | Tenant Admin |
| Private Message Notification | Specific User |
| Tenant Channel Message | Tenant Channel Users |
| User Test Message Notification | Tenant Users |
| Reset Password Notification | Requesting User |

### Push Notifications (📱 FCM)

| Notification | Target |
|--------------|--------|
| Tab Channel Notification | Kitchen, Staff, Admin |
| Mall Session Tab Creation | Restaurant Staff |
| Mall Order Updated | Restaurant Staff |
| Mall Store Assistance | Restaurant Staff |
| Mall Session Notification | Customer |

### Database Storage (💾)

| Notification | Target |
|--------------|--------|
| Tab Channel Notification | Kitchen, Staff, Admin |
| Mall Session Order Status | Customer Session |
| Mall Session Tab Creation | Restaurant Staff |
| Mall Order Updated | Restaurant Staff |
| Product Import Notification | Tenant Users, Admin |
| Validate Product Import | Tenant Users, Admin |
| Product Import Error | Tenant Users, Admin |
| Low Stock Notification | Tenant Admin |
| Campaign Marketplace Product Import | Tenant Users, Admin |
| Campaign Status | Tenant Users |
| Removal Reminder | Tenant Users, Admin |
| Private Message | Specific User |
| Tenant Channel Message | Tenant Channel Users |
| User Test Message | Tenant Users |

---

## Target Audience Reference

| Target | Description |
|--------|-------------|
| **Tenant Admin** | Business owner or administrator of a tenant/store |
| **Tenant User** | Regular staff member of a tenant |
| **Kitchen** | Kitchen staff (cooks, prep) |
| **Staff** | Front-of-house staff (waiters, cashiers) |
| **Admin** | System or store administrator |
| **Customer** | End customer placing orders |
| **Public** | All connected clients (displays, screens) |

---

*Last Updated: December 2024*
