
can you give me a latex version please. 

# KitchnTabs Email Sending Practices for AWS SES Review

**Document Version:** 1.0  
**Date:** December 22, 2025  
**Prepared by:** KitchnTabs Development Team  
**Contact:** Francisco Aranda <farandal@gmail.com> - <info@kitchntabs.com>
**Website:** https://kitchntabs.com
**App:** https://panel.kitchntabs.com

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Company & Platform Overview](#2-company--platform-overview)
3. [Email Sending Practices](#3-email-sending-practices)
4. [Recipient List Management](#4-recipient-list-management)
5. [Email Categories & Examples](#5-email-categories--examples)
6. [Email Flow Diagrams](#6-email-flow-diagrams)
7. [Bounce & Complaint Handling](#7-bounce--complaint-handling)
8. [Unsubscribe Management](#8-unsubscribe-management)
9. [Technical Infrastructure](#9-technical-infrastructure)
10. [Quality Assurance](#10-quality-assurance)
11. [Email Templates](#11-email-templates)

---

## 1. Executive Summary

**KitchnTabs** is a B2B SaaS platform providing restaurant and food court management solutions to businesses in Latin America, primarily Chile. Our platform sends transactional and operational emails that are critical to business operations.

### Key Points:

- **Nature of Emails:** 100% transactional emails (no marketing/promotional content)
- **Primary Recipients:** 
  - Business users (restaurant staff, administrators)
  - End customers (who have explicitly consented via marketplace checkout)
- **Volume:** Low to moderate (estimated 50-500 emails/day depending on order volume)
- **Languages:** Spanish (primary), English (secondary)
- **Consent:** All recipients have explicitly opted-in or consented via transactional relationships

---

## 2. Company & Platform Overview

### 2.1 About KitchnTabs

KitchnTabs is a comprehensive restaurant management platform consisting of:

- **Dash Backend:** Laravel-based API providing multi-tenant architecture, role-based permissions, real-time WebSocket messaging, and order management
- **Dash Admin:** React-based admin dashboard for business users
- **Mall/Food Court System:** QR-based ordering system for food courts
- **Marketplace Integrations:** Jumpseller, Uber Eats, and other e-commerce platforms

### 2.2 Business Model

```mermaid
flowchart TD
    subgraph ECO["KITCHNTABS ECOSYSTEM"]
        A["RESTAURANT A (Tenant)"]
        B["RESTAURANT B (Tenant)"]
        C["RESTAURANT C (Tenant)"]
        A --> P
        B --> P
        C --> P
        P["KITCHNTABS PLATFORM (Multi-Tenant SaaS)"]
        P --> D["Dashboard (Business)"]
        P --> M["Marketplace Integration"]
        P --> F["Food Court (Customer)"]
    end
```

### 2.3 User Types

| User Type | Description | Email Frequency |
|-----------|-------------|-----------------|
| **Tenant Admin** | Restaurant owner/manager | 1-5 emails/week |
| **Tenant Staff** | Kitchen/front-of-house staff | 1-10 emails/day (order notifications) |
| **End Customer** | Customer placing orders via marketplace | 1-3 emails/order (status updates) |

---

## 3. Email Sending Practices

### 3.1 Email Frequency

| Email Category | Frequency | Trigger |
|----------------|-----------|---------|
| **Order Status Updates** | Per order (3-5 per order lifecycle) | Order state changes |
| **Password Reset** | On-demand | User request |
| **Account Verification** | Once per user | Registration |
| **Export Notifications** | As needed | User-initiated exports |
| **Low Stock Alerts** | Daily digest | Inventory threshold breach |
| **Import Notifications** | As needed | Bulk import completion |

### 3.2 Email Volume Estimates

| Period | Expected Volume | Notes |
|--------|-----------------|-------|
| **Daily** | 50-500 emails | Depends on order volume per tenant |
| **Weekly** | 350-3,500 emails | Business days see higher volume |
| **Monthly** | 1,500-15,000 emails | Seasonal variations apply |

### 3.3 Sending Patterns

```
       Email Volume Distribution (Typical Day (estimation))
       
Emails│                    ████                    
  60 │                   █████                    
     │                  ███████                   
  40 │                 █████████ █                
     │               ███████████████              
  20 │            █████████████████████           
     │         ███████████████████████████        
   0 │────────────────────────────────────────────
       00  04  08  12  16  20  24   Hour (Local Time)
       
       Peak hours: 12:00-14:00, 19:00-21:00 (meal times)
```

---

## 4. Recipient List Management

### 4.1 How Recipients Are Added

#### Business Users (Tenant Staff/Admins)

```mermaid
flowchart TD
    subgraph FLOW["BUSINESS USER REGISTRATION FLOW"]
        A["Tenant Admin Creates Account"] --> B["REGISTRATION FORM
- Email address (required)
- Terms of Service acceptance (required)
- Email notification preferences (configurable)"]
        B --> C["VERIFICATION EMAIL SENT
Subject: 'Verificar cuenta'
Action: User clicks verification link"]
        C --> D["EMAIL VERIFIED
User is now able to receive operational emails"]
    end
```

#### End Customers (Marketplace Orders)

```mermaid
flowchart TD
    subgraph FLOW["END CUSTOMER EMAIL CONSENT FLOW (Jumpseller Integration)"]
        A["Customer Places Order on Jumpseller"] --> B["JUMPSELLER CHECKOUT
- Customer provides email
- Customer accepts Jumpseller Terms of Service
- Jumpseller TOS includes consent for order status emails"]
        B --> C["WEBHOOK TO KITCHNTABS
Jumpseller sends order data including:
- customer.email
- customer.notification_preferences"]
        C --> D["KITCHNTABS PROCESSES ORDER
- Order status emails sent ONLY if customer consented
- Email sent from tenant's configured sending address"]
    end
```

### 4.2 Email List Hygiene

| Practice | Implementation |
|----------|----------------|
| **No purchased lists** | All recipients are organic (business users or marketplace customers) |
| **Email verification** | Business users must verify email before receiving notifications |
| **Consent-based** | End customers consent via marketplace checkout process |
| **Regular cleanup** | Inactive accounts flagged after 6 months of no activity |

---

## 5. Email Categories & Examples

### 5.1 Email Notifications Catalog

| # | Email Type | Trigger | Recipients | Subject Example |
|---|------------|---------|------------|-----------------|
| 1 | **Order Status Update** | Order state changes | Kitchen Staff, Admins | "Nueva Orden #12345" |
| 2 | **Marketplace Order Update** | Order status change | End Customer | "¡Actualización de tu pedido!" |
| 3 | **Password Reset** | User request | Requesting User | "Restablecer contraseña" |
| 4 | **Account Verification** | New registration | New User | "Verificar cuenta" |
| 5 | **Account Verified** | Email confirmed | User | "¡Cuenta verificada exitosamente!" |
| 6 | **Welcome Email** | After verification | New User | "Bienvenido a KitchnTabs" |
| 7 | **Export Completed** | Data export finishes | Requesting User | "Exportación completada" |
| 8 | **Product Import Result** | Bulk import completes | Tenant Admins | "Importación completada" |
| 9 | **Low Stock Alert** | Stock below threshold | Tenant Admins | "Alerta de stock bajo" |
| 10 | **Private Message** | Internal messaging | Specific User | "Mensaje privado" |

### 5.2 Order Status Email Lifecycle

For a typical order, the customer receives emails at these stages:

```
ORDER LIFECYCLE EMAIL SEQUENCE
══════════════════════════════════════════════════════════════════════════

 TIME     STATUS              EMAIL SENT?    SUBJECT
 ─────    ──────              ───────────    ───────────────────────────
 
 T+0      CREATED             ✅ Yes         "¡Pedido recibido!"
          (Order placed)
          
 T+5min   CONFIRMED           ✅ Yes         "¡Tu pedido ha sido confirmado!"
          (Restaurant accepts)
          
 T+15min  IN_PREPARATION      ✅ Yes         "Tu pedido está en preparación"
          (Kitchen starts)
          
 T+30min  PREPARED            ✅ Yes         "¡Tu pedido está listo!"
          (Ready for pickup)
          
 T+45min  SHIPPED/PICKED_UP   ✅ Yes         "Tu pedido está en camino"
          (Out for delivery)
          
 T+60min  DELIVERED           ✅ Yes         "¡Pedido entregado!"
          (Customer received)

══════════════════════════════════════════════════════════════════════════

Note: Not all orders go through all stages. Some orders are pickup-only,
      some are cancelled. Each status change triggers a notification.
```

---

## 6. Email Flow Diagrams

### 6.1 Marketplace Order Email Flow

```mermaid
sequenceDiagram
    title MARKETPLACE ORDER EMAIL NOTIFICATION FLOW
    participant Customer
    participant Jumpseller
    participant KitchnTabs
    participant Tenant

    Customer->>Jumpseller: 1. Place Order (with email consent)
    Jumpseller->>KitchnTabs: 2. Webhook: order_paid
    KitchnTabs->>Tenant: 3. Create Tab/Order
    KitchnTabs->>Tenant: 4. Notify Staff (Email + Push)
    KitchnTabs->>Customer: 5. Order Confirmation (Email)
    Tenant->>KitchnTabs: 6. Staff Updates Status to IN_PREPARATION
    KitchnTabs->>Customer: 7. Status Update ("En preparación")
    KitchnTabs->>Jumpseller: 8. Sync back to Jumpseller
```

### 6.2 User Registration Email Flow

```mermaid
sequenceDiagram
    title USER REGISTRATION EMAIL FLOW
    participant NewUser as NEW USER
    participant KitchnTabs as KITCHNTABS
    participant SES as AWS SES

    NewUser->>KitchnTabs: 1. Register Account (email, password, TOS)
    Note over KitchnTabs: 2. Generate verification token & store user
    KitchnTabs->>SES: 3. Send verification email via SES
    SES->>KitchnTabs: 4. Email Delivered
    KitchnTabs->>NewUser: 5. Verification Email "Verificar cuenta"
    NewUser->>KitchnTabs: 6. Click Verification Link
    Note over KitchnTabs: 7. Mark email verified in database
    KitchnTabs->>SES: 8. Send welcome email
    KitchnTabs->>NewUser: 9. Welcome Email "Bienvenido!"
```

### 6.3 Password Reset Email Flow

```mermaid
sequenceDiagram
    title PASSWORD RESET EMAIL FLOW
    participant User as USER
    participant KitchnTabs as KITCHNTABS
    participant SES as AWS SES

    User->>KitchnTabs: 1. Request Password Reset
    Note over KitchnTabs: 2. Check email exists
    Note over KitchnTabs: 3. Generate reset token (expires in 60 min)
    KitchnTabs->>SES: 4. Send reset email
    KitchnTabs->>User: 5. Reset Email "Restablecer contraseña"
    User->>KitchnTabs: 6. Click Reset Link
    Note over KitchnTabs: 7. Validate token
    Note over KitchnTabs: 8. Show reset form
    User->>KitchnTabs: 9. Submit New Password
    Note over KitchnTabs: 10. Update password
    Note over KitchnTabs: 11. Invalidate token
```

### 6.4 Bulk Export Email Flow

```mermaid
sequenceDiagram
    title BULK EXPORT EMAIL NOTIFICATION FLOW
    participant TenantAdmin as TENANT ADMIN
    participant KitchnTabs as KITCHNTABS
    participant SES as AWS SES

    TenantAdmin->>KitchnTabs: 1. Request Product Export
    KitchnTabs->>TenantAdmin: 2. WebSocket: "Export Started"
    Note over KitchnTabs: [Background Job Runs] Processing 1000s of products...
    KitchnTabs->>TenantAdmin: 3. Progress Updates "10%... 50%... 90%..."
    Note over KitchnTabs: 4. Generate Excel file
    Note over KitchnTabs: 5. Upload to S3
    Note over KitchnTabs: 6. Generate signed URL
    KitchnTabs->>SES: 7. Send completion email
    KitchnTabs->>TenantAdmin: 8. Export Email "Exportación completada" [Download Link]
```

---

## 7. Bounce & Complaint Handling

### 7.1 Current Implementation Status

> ⚠️ **Note:** Bounce and complaint handling via SNS notifications is planned but not yet implemented. Below is the proposed implementation.

### 7.2 Proposed Bounce Handling Architecture

```mermaid
flowchart TD
    SES["AWS SES"] --> Bounce["Bounce Event"]
    SES --> Complaint["Complaint Event"]
    SES --> Delivery["Delivery Event"]
    Bounce --> SNS["Amazon SNS Topic"]
    Complaint --> SNS
    Delivery --> SNS
    SNS --> API["KitchnTabs API /api/webhooks/ses-feedback"]
    API --> HardBounce["Hard Bounce → Suppress Forever"]
    API --> SoftBounce["Soft Bounce → Retry 3x then Suppress"]
    API --> ComplaintAction["Complaint → Suppress + Log"]
    HardBounce --> Table["email_statuses table
- email
- status
- bounce_type
- suppressed_at"]
    SoftBounce --> Table
    ComplaintAction --> Table
```

### 7.3 Bounce Type Handling

| Bounce Type | Action | Retention |
|-------------|--------|-----------|
| **Hard Bounce** (permanent) | Immediately suppress email | Permanent |
| **Soft Bounce** (temporary) | Retry up to 3 times over 24h | Suppress after 3 failures |
| **Complaint** | Immediately suppress + log for review | Permanent |

### 7.4 Database Schema

```sql
CREATE TABLE email_delivery_status (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    tenant_id UUID NULL,
    status ENUM('active', 'bounced', 'complained', 'suppressed') DEFAULT 'active',
    bounce_type VARCHAR(50) NULL, -- 'Permanent', 'Transient'
    bounce_subtype VARCHAR(50) NULL, -- 'General', 'NoEmail', 'Suppressed'
    complaint_type VARCHAR(50) NULL, -- 'abuse', 'not-spam'
    retry_count INT DEFAULT 0,
    last_bounce_at TIMESTAMP NULL,
    suppressed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_tenant (tenant_id)
);
```

### 7.5 Email Sending Check

Before sending any email, the system check:

```php
// Proposed implementation in AppNotificationBuilder
public function shouldSendEmail(string $email): bool
{
    $status = EmailDeliveryStatus::where('email', $email)->first();
    
    if (!$status) {
        return true; // New email, OK to send
    }
    
    if ($status->status === 'suppressed') {
        Log::info("Email suppressed: {$email}", [
            'reason' => $status->bounce_type ?? $status->complaint_type
        ]);
        return false;
    }
    
    return true;
}
```

---

## 8. Unsubscribe Management

### 8.1 User Preference Center

Business users can manage their notification preferences through the platform:

```mermaid
flowchart TD
    subgraph PREFS["USER NOTIFICATION PREFERENCES (Dashboard Settings)"]
        subgraph ORDER["Order Notifications"]
            O1["New order alerts (checked): Email, Push, Socket"]
            O2["Order status changes (checked): Email, Push, Socket"]
            O3["Order cancellations (checked): Email, Push, Socket"]
        end
        subgraph INV["Inventory Notifications"]
            I1["Low stock alerts (checked): Email, Socket"]
            I2["Import/Export completion (checked): Email, Socket"]
        end
        subgraph SYS["System Notifications"]
            S1["Password changes (checked): Email"]
            S2["Marketing updates (unchecked): Email"]
        end
        SAVE["Save Preferences"]
        ORDER --> SAVE
        INV --> SAVE
        SYS --> SAVE
    end
```

### 8.2 Unsubscribe Methods

| Method | Implementation | Notes |
|--------|----------------|-------|
| **Preference Center** | In-app settings page | Full control over notification types |
| **Email Footer Link** | List-Unsubscribe header | One-click unsubscribe for specific categories |
| **Reply-based** | Not implemented | Low priority for transactional emails |

### 8.3 End Customer Unsubscribe

For marketplace customers:
- Transactional emails (order updates) cannot be unsubscribed as they are essential for order fulfillment
- Customers can contact the restaurant directly to request email removal
- System respects marketplace-level preferences passed via webhook

---

## 9. Technical Infrastructure

### 9.1 Email Sending Architecture

```mermaid
flowchart TD
    subgraph APP["APPLICATION LAYER"]
        NC["Notification Classes"] --> ANB["AppNotificationBuilder (Central Router)"]
        ANB --> MQ["Laravel Mail Queue (Redis)"]
    end
    subgraph QUEUE["QUEUE PROCESSING"]
        subgraph HORIZON["Laravel Horizon"]
            Q1["default queue"]
            Q2["emails queue"]
            Q3["exports queue"]
            Q4["notifications queue"]
        end
    end
    subgraph TRANSPORT["TRANSPORT LAYER"]
        SESDRIVER["Laravel Mail with SES Driver
config/mail.php:
'default' => env('MAIL_MAILER', 'ses'),
'from' => ['address' => 'info@kitchntabs.com']"]
    end
    subgraph AWS["AWS SERVICES"]
        SES["AWS SES (Sending)"] --> SNS["AWS SNS (Feedback)"]
        SNS --> CW["CloudWatch (Metrics)"]
    end

    MQ --> Q2
    Q2 --> SESDRIVER
    SESDRIVER --> SES
```

### 9.2 Configuration

**Environment Variables:**
```bash
MAIL_MAILER=ses
MAIL_FROM_ADDRESS=no-reply@kitchntabs.com
MAIL_FROM_NAME="KitchnTabs"

AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
```

### 9.3 Sending Domains

| Domain | Purpose | DKIM | SPF | DMARC |
|--------|---------|------|-----|-------|
| kitchntabs.com | Primary sending domain | ✅ | ✅ | ✅ |
| pinoywok.cl | Tenant-specific (legacy) | ✅ | ✅ | ✅ |

---

## 10. Quality Assurance

### 10.1 Email Quality Checklist

| Check | Status | Implementation |
|-------|--------|----------------|
| ✅ Valid From address | Implemented | Verified domain |
| ✅ Clear subject lines | Implemented | Descriptive, no spam triggers |
| ✅ Plain text alternative | Implemented | All emails have text version |
| ✅ Unsubscribe header | Planned | List-Unsubscribe header |
| ✅ Mobile-responsive | Implemented | All templates responsive |
| ✅ Proper encoding | Implemented | UTF-8 throughout |
| ✅ No broken images | Implemented | CDN-hosted images |

### 10.2 Content Guidelines

- **No promotional content** in transactional emails
- **Clear sender identification** (company name, logo)
- **Relevant, expected content** based on user action
- **Spanish language** with proper localization
- **Contact information** in footer

---

## 11. Email Templates

### 11.1 Order Status Update Email

**Subject:** "¡Actualización de tu pedido!"

```html
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│                              [COMPANY LOGO]                                      │
│                                                                                  │
│                     ┌─────────────────────────┐                                 │
│                     │      JUMPSELLER         │                                 │
│                     └─────────────────────────┘                                 │
│                                                                                  │
│                  ¡Actualización de tu pedido!                                    │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  Hola Juan, te informamos que el estado de tu pedido ha cambiado.               │
│                                                                                  │
│  Pedido: #12345                                                                  │
│  Fecha: 22/12/2025 14:30                                                        │
│                                                                                  │
│                                                  ┌──────────────────┐           │
│                                                  │ EN PREPARACIÓN   │           │
│                                                  └──────────────────┘           │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  PRODUCTOS ORDENADOS                                                            │
│  ──────────────────────────────────────────                                     │
│                                                                                  │
│  🍕 Pizza Margherita .......................... x2 ........... $15.990         │
│  🥤 Coca-Cola 500ml ........................... x2 ........... $3.000          │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  Subtotal: $18.990                                                              │
│  Envío: $2.990                                                                  │
│  TOTAL: $21.980                                                                 │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  INFORMACIÓN DE ENVÍO                                                           │
│  ──────────────────────────────────────────                                     │
│                                                                                  │
│  Av. Providencia 1234, Santiago                                                 │
│  Llegada estimada: 22/12/2025 15:00                                             │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  Si tienes preguntas, contáctanos en contact@restaurant.cl                      │
│                                                                                  │
│                              © 2025 KitchnTabs                                  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 11.2 Password Reset Email

**Subject:** "Restablecer contraseña"

```html
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│                              [COMPANY LOGO]                                      │
│                                                                                  │
│                     Recuperación de contraseña                                   │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  A continuación, verás un enlace para restablecer tu contraseña.                │
│  Cuando hagas click en aquel enlace te dirigirá a realizar los                  │
│  cambios necesarios para recuperar tu contraseña.                               │
│                                                                                  │
│                     ┌─────────────────────────┐                                 │
│                     │  Recuperar contraseña   │                                 │
│                     └─────────────────────────┘                                 │
│                                                                                  │
│  Este enlace expirará en 60 minutos.                                            │
│                                                                                  │
│  Si no solicitaste este cambio, puedes ignorar este correo.                     │
│                                                                                  │
│                              © 2025 KitchnTabs                                  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 11.3 Welcome Email

**Subject:** "¡Bienvenido a KitchnTabs!"

```html
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│                              [COMPANY LOGO]                                      │
│                                                                                  │
│                       ¡Bienvenido Juan!                                          │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  Nombre del usuario: juan@example.com                                            │
│                                                                                  │
│  Tu cuenta ha sido creada exitosamente. Ya puedes ingresar                       │
│  y comenzar a usar la plataforma.                                                │
│                                                                                  │
│                     ┌─────────────────────────┐                                 │
│                     │  Ingresar al sistema    │                                 │
│                     └─────────────────────────┘                                 │
│                                                                                  │
│                              © 2025 KitchnTabs                                  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 11.4 Export Completed Email

**Subject:** "Exportación completada"

```html
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│                              [COMPANY LOGO]                                      │
│                                                                                  │
│                       Export Completed                                           │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  Your export has been completed successfully.                                    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  📁 File: products_export_2025-12-22.xlsx                               │   │
│  │  ⏰ Completed: Dec 22, 2025 at 14:30                                    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│                     ┌─────────────────────────┐                                 │
│                     │  📊 Download Excel File │                                 │
│                     └─────────────────────────┘                                 │
│                              (2.5 MB)                                           │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  🔒 Important Information:                                                       │
│  • Download links are temporary and will expire after 24 hours                  │
│  • Please download your file as soon as possible                                │
│                                                                                  │
│                              © 2025 KitchnTabs                                  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Appendix A: Recommendations Requested

Based on this documentation, we request AWS SES team recommendations on:

1. **Bounce Handling:** Best practices for implementing SNS-based bounce processing
2. **Complaint Management:** Optimal workflow for handling abuse complaints
3. **Sending Limits:** Appropriate rate limits for our transactional volume
4. **Dedicated IP:** Whether our volume warrants dedicated IP address(es)
5. **Monitoring:** CloudWatch alarms and metrics we should configure
6. **DMARC Policy:** Recommended policy (none → quarantine → reject) progression

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-22 | Francisco Aranda L <farandal@gmail.com> | Initial document |

---

**Contact Information:**

- **Technical Contact:** farandal@gmail.com
- **Website:** https://kitchntabs.com
