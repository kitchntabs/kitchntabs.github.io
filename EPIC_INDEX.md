---
title: Epic-Based Documentation Index
layout: default
---

# KitchnTabs Documentation by Epic

**Complete documentation organized by the 35-epic structure used in ClickUp.**

This is the master index for navigating KitchnTabs documentation. All files are organized into **35 Epics** (25 Functional + 10 Non-Functional) that mirror the product roadmap.

---

## Functional Epics (F1–F25)

### [F1: Orders & Tabs](/docs/F1-Orders-Tabs/)
**Restaurant order management system with complete order lifecycle tracking.**

6 documents covering tab models, order processing, hash ID security, delivery tracking, tenant lifecycle, and multi-tenant order architecture.

- Directory: `/docs/F1-Orders-Tabs/`
- Documents: 6
- Key topics: Order lifecycle, tab status machine, multi-tenant ordering

---

### [F2: Products & Catalog](/docs/F2-Products-Catalog/)
**Product information management with pricing and customization support.**

Product domain models, category hierarchies, modifier groups, and pricing strategies.

- Directory: `/docs/F2-Products-Catalog/`
- Documents: 3
- Key topics: Product catalog, modifiers, pricing

---

### [F3: Product Import / Export](/docs/F3-Product-Import-Export/)
**Bulk product data ingestion and export functionality.**

Automated import systems with validation, error handling, and batch processing.

- Directory: `/docs/F3-Product-Import-Export/`
- Documents: 2
- Key topics: Bulk import, validation, export

---

### [F4: Mall / Food Court](/docs/F4-Mall-Food-Court/)
**Multi-store food court management and shared marketplace.**

Complete food court ordering system with multi-tenant architecture and real-time synchronization.

- Directory: `/docs/F4-Mall-Food-Court/`
- Documents: 16
- Key topics: Mall sessions, store coordination, multi-tenant orders

---

### [F5: Customer & Self-Service](/docs/F5-Customer-Self-Service/)
**Customer-facing application and self-service ordering platform.**

Mobile-first customer app with real-time tracking and WebSocket updates.

- Directory: `/docs/F5-Customer-Self-Service/`
- Documents: 8
- Key topics: Customer flows, notifications, order tracking

---

### [F6: Tenant / Staff App](/docs/F6-Tenant-Staff-App/)
**Staff and vendor management application with role-based workflows.**

Real-time staff interface for order management and notifications.

- Directory: `/docs/F6-Tenant-Staff-App/`
- Documents: 3
- Key topics: Staff workflows, real-time updates, order management

---

### [F7: System Admin Application](/docs/F7-System-Admin-Application/)
**Administrative dashboard for platform management and oversight.**

Comprehensive admin portal with user management, audit trails, and system monitoring.

- Directory: `/docs/F7-System-Admin-Application/`
- Documents: 6
- Key topics: Admin workflows, user management, audit trails

---

### [F8: Public Web](/docs/F8-Public-Web/)
**Public-facing website and brand presence.**

Marketing site and public information portal.

- Directory: `/docs/F8-Public-Web/`
- Documents: 3
- Key topics: Design system, branding, responsive design

---

### [F9: Marketplaces](/docs/F9-Marketplaces/)
**Third-party marketplace integrations and synchronization.**

Integrations with Jumpseller, Uber Eats, and other platforms.

- Directory: `/docs/F9-Marketplaces/`
- Documents: 10
- Key topics: Marketplace APIs, synchronization, order routing

---

### [F10: Point of Sale](/docs/F10-Point-of-Sale/)
**Physical point-of-sale system integration and management.**

Integration with traditional POS systems.

- Directory: `/docs/F10-Point-of-Sale/`
- Documents: 1
- Key topics: POS framework, integration

---

### [F11: Checkout Gateways](/docs/F11-Checkout-Gateways/)
**Payment processor integrations and checkout flows.**

Multi-gateway payment processing (Transbank, Mercado Pago, Flow.cl, Rebill).

- Directory: `/docs/F11-Checkout-Gateways/`
- Documents: 7
- Key topics: Payment processors, PCI compliance, webhooks

---

### [F12: Billing, Subscriptions & Payments](/docs/F12-Billing-Subscriptions-Payments/)
**Subscription management, invoicing, and revenue operations.**

Complete billing platform with subscription lifecycle and financial reporting.

- Directory: `/docs/F12-Billing-Subscriptions-Payments/`
- Documents: 21
- Key topics: Subscriptions, invoicing, billing policies, payments

---

### [F13: Platform & Multi-Tenancy](/docs/F13-Platform-Multi-Tenancy/)
**Core multi-tenancy architecture and tenant isolation.**

Foundational multi-tenant infrastructure with data isolation.

- Directory: `/docs/F13-Platform-Multi-Tenancy/`
- Documents: 8
- Key topics: Tenant scoping, multi-tenancy patterns, provisioning

---

### [F14: Auth & Access Control](/docs/F14-Auth-Access-Control/)
**Role-based permissions and granular access control.**

RBAC system with permission inheritance and permission selectors.

- Directory: `/docs/F14-Auth-Access-Control/`
- Documents: 23
- Key topics: Permissions, role hierarchies, token management

---

### [F15: Notifications & Messaging](/docs/F15-Notifications-Messaging/)
**Multi-channel notification delivery system.**

Email, SMS, push notifications via AWS SES, Firebase.

- Directory: `/docs/F15-Notifications-Messaging/`
- Documents: 16
- Key topics: Email systems, push notifications, notification catalogs

---

### [F16: AI Agents](/docs/F16-AI-Agents/)
**Artificial intelligence and machine learning capabilities.**

AI-powered features, recommendations, and automation.

- Directory: `/docs/F16-AI-Agents/`
- Documents: 1
- Key topics: AI/ML, chatbots, ML deployment

---

### [F17: Inventory](/docs/F17-Inventory/)
**Inventory management and stock tracking system.**

Real-time stock tracking and reorder automation.

- Directory: `/docs/F17-Inventory/`
- Documents: 0
- Key topics: Stock management, forecasting

---

### [F18: Campaigns](/docs/F18-Campaigns/)
**Marketing campaigns and promotional management.**

Campaign creation, scheduling, and performance tracking.

- Directory: `/docs/F18-Campaigns/`
- Documents: 5
- Key topics: Campaign publishing, promotions, A/B testing

---

### [F19: Internationalization](/docs/F19-Internationalization/)
**Multi-language and localization support.**

i18n infrastructure for global deployment.

- Directory: `/docs/F19-Internationalization/`
- Documents: 5
- Key topics: Translations, localization, multi-language support

---

### [F20: Media & Images](/docs/F20-Media-Images/)
**Image management and media handling.**

Centralized media system with CDN delivery and optimization.

- Directory: `/docs/F20-Media-Images/`
- Documents: 3
- Key topics: Image optimization, media library, gallery management

---

### [F21: Tenancy Management](/docs/F21-Tenancy-Management/)
**Tenant lifecycle and account management.**

Tenant provisioning, customization, and termination.

- Directory: `/docs/F21-Tenancy-Management/`
- Documents: 2
- Key topics: Tenant provisioning, account lifecycle

---

### [F22: MiddlewareService](/docs/F22-MiddlewareService/)
**Service middleware and cross-cutting concerns.**

Core middleware for auth, logging, rate limiting.

- Directory: `/docs/F22-MiddlewareService/`
- Documents: 0
- Key topics: Middleware, request validation, security headers

---

### [F23: DeliveryModule](/docs/F23-DeliveryModule/)
**Delivery logistics and fulfillment management.**

End-to-end delivery tracking and route optimization.

- Directory: `/docs/F23-DeliveryModule/`
- Documents: 1
- Key topics: Delivery tracking, driver management, notifications

---

### [F24: InventoryModule](/docs/F24-InventoryModule/)
**Advanced inventory management and optimization.**

Enterprise inventory with forecasting and multi-location support.

- Directory: `/docs/F24-InventoryModule/`
- Documents: 0
- Key topics: Stock allocation, supply chain optimization

---

### [F25: CashcountModule](/docs/F25-CashcountModule/)
**Cash handling and reconciliation system.**

Cash management and drawer operations.

- Directory: `/docs/F25-CashcountModule/`
- Documents: 0
- Key topics: Cash reconciliation, security protocols

---

## Non-Functional Epics (N1–N10)

### [N1: Backend Framework](/docs/N1-Backend-Framework/)
**Core Laravel infrastructure and domain-driven design architecture.**

Foundation with service layer patterns and DDD principles.

- Directory: `/docs/N1-Backend-Framework/`
- Documents: 7
- Key topics: Architecture, Laravel patterns, domain models

---

### [N2: Frontend Framework](/docs/N2-Frontend-Framework/)
**React-based component system and administrative UI framework.**

React + React-Admin with design tokens and accessibility.

- Directory: `/docs/N2-Frontend-Framework/`
- Documents: 1
- Key topics: React components, design system, state management

---

### [N3: Infrastructure & CI/CD](/docs/N3-Infrastructure-CICD/)
**Deployment infrastructure and continuous integration/deployment.**

AWS CDK, CI/CD pipelines, environment management.

- Directory: `/docs/N3-Infrastructure-CICD/`
- Documents: 8
- Key topics: CI/CD, deployment, infrastructure as code

---

### [N4: Build Toolchain](/docs/N4-Build-Toolchain/)
**Build processes and application compilation systems.**

Webpack, Electron builds, multi-architecture compilation.

- Directory: `/docs/N4-Build-Toolchain/`
- Documents: 8
- Key topics: Build automation, Electron, production builds

---

### [N5: Desktop & Device Service](/docs/N5-Desktop-Device-Service/)
**Electron-based desktop application and Python service integration.**

Cross-platform Electron with IPC and hardware integration.

- Directory: `/docs/N5-Desktop-Device-Service/`
- Documents: 5
- Key topics: Electron, Python integration, device hardware

---

### [N6: Caching & Performance](/docs/N6-Caching-Performance/)
**Performance optimization and caching strategies.**

Redis caching, query optimization, performance monitoring.

- Directory: `/docs/N6-Caching-Performance/`
- Documents: 2
- Key topics: Redis, performance monitoring, cache invalidation

---

### [N7: Security](/docs/N7-Security/)
**Security practices and threat protection.**

Authentication, encryption, vulnerability management.

- Directory: `/docs/N7-Security/`
- Documents: 0
- Key topics: Security architecture, compliance, threat modeling

---

### [N8: Observability](/docs/N8-Observability/)
**Logging, monitoring, and operational visibility.**

CloudWatch, APM, real-time dashboards.

- Directory: `/docs/N8-Observability/`
- Documents: 1
- Key topics: Logging, monitoring, alerting

---

### [N9: App Publishing](/docs/N9-App-Publishing/)
**Mobile and desktop application distribution.**

App store publishing, CI/CD for app releases.

- Directory: `/docs/N9-App-Publishing/`
- Documents: 0
- Key topics: App store deployment, release management

---

### [N10: Administrative & Legal](/docs/N10-Administrative-Legal/)
**Settings, utilities, and compliance documentation.**

Configuration, backup, compliance requirements.

- Directory: `/docs/N10-Administrative-Legal/`
- Documents: 9
- Key topics: Admin utilities, compliance, settings

---

## Summary

| Category | Epic Count | Total Documents |
|---|---|---|
| **Functional (F1–F25)** | 25 | ~170 |
| **Non-Functional (N1–N10)** | 10 | ~25 |
| **Total** | **35** | **195+** |

---

## Navigation Tips

1. **By Epic** — Use this index to explore documentation organized by product epic
2. **By Technology** — See Non-Functional epics for architecture and infrastructure
3. **By Feature** — See Functional epics for user-facing features
4. **Full Index** — Visit [INDEX.md](INDEX.md) for a complete table of contents

---

<div class="footer-section">
  <p>Documentation organized by epic structure matching ClickUp roadmap</p>
  <p>© 2025 KitchnTabs. All rights reserved.</p>
</div>
