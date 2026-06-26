
# KitchnTabs — Functional & Non-Functional Requirements

> **Document type:** Software Requirements Specification (SRS)
> **Scope:** Full KitchnTabs platform — Laravel API backend, React frontends (System, Mall, Web, App), Electron desktop shell, Python device service, and AWS/Cloudflare infrastructure.
> **Derived from:** Project documentation (`docs/`), domain models, and the implemented codebase (`dash-backend`, `kitchntabs-frontend`, `dash-python-service`, `kitchntabs-ci-cdk`).
> **Last compiled:** 2026-06-25

## How to read this document

- **FR-xxx** — Functional Requirement (what the system does).
- **NFR-xxx** — Non-Functional Requirement (quality attribute / constraint).
- Each requirement is grouped by **component** and then by **feature**.
- Status tags where known: `(implemented)`, `(partial)`, `(planned)`.

---

## Table of Contents

1. [Platform & Multi-Tenancy](#1-platform--multi-tenancy)
2. [Authentication & Access Control](#2-authentication--access-control)
3. [System Admin Application](#3-system-admin-application)
4. [Tenant / Staff Application (POS & Operations)](#4-tenant--staff-application-pos--operations)
5. [Mall / Food Court Experience](#5-mall--food-court-experience)
6. [Customer & Self-Service Experience](#6-customer--self-service-experience)
7. [Public Web / Marketing Site](#7-public-web--marketing-site)
8. [Order & Tab Management](#8-order--tab-management)
9. [Product Catalog & Modifiers](#9-product-catalog--modifiers)
10. [Point of Sale (POS) Integration](#10-point-of-sale-pos-integration)
11. [Marketplace Integrations](#11-marketplace-integrations)
12. [Checkout Gateways (End-Customer Payments)](#12-checkout-gateways-end-customer-payments)
13. [Billing, Subscriptions & Payment Gateways](#13-billing-subscriptions--payment-gateways)
14. [Notifications & Real-Time Messaging](#14-notifications--real-time-messaging)
15. [AI Agents (Voice & Image)](#15-ai-agents-voice--image)
16. [Desktop Shell & Device Service (Electron + Python)](#16-desktop-shell--device-service-electron--python)
17. [Campaigns & Marketing Automation](#17-campaigns--marketing-automation)
18. [Product Import / Export](#18-product-import--export)
19. [Internationalization (i18n)](#19-internationalization-i18n)
20. [Media & Image Management](#20-media--image-management)
21. [Caching & Performance](#21-caching--performance)
22. [Infrastructure, Build & Deployment](#22-infrastructure-build--deployment)
23. [Cross-Cutting Non-Functional Requirements](#23-cross-cutting-non-functional-requirements)

---

## 1. Platform & Multi-Tenancy

### 1.1 Tenancy Accounts
- **FR-1.1.1** The system SHALL support a `Tenancy` account abstraction above individual `Tenant` (restaurant/location) records, so one billing account can own multiple restaurants. *(implemented)*
- **FR-1.1.2** A Tenancy SHALL store `public_name`, `legal_name`, `public_id` (RUT/Tax ID), `email`, `url`, `slug`, `status`, and JSON `settings`/`metadata`.
- **FR-1.1.3** A Tenancy SHALL move through a lifecycle: `trial → active → suspended → cancelled → deleted`, with timestamps for `trial_ends_at`, `suspended_at`, and `marked_for_deletion_at`.
- **FR-1.1.4** The system SHALL support automated provisioning of a new tenancy's initial tenant, roles, default catalog, and default integrations on creation. *(implemented)*
- **FR-1.1.5** A TenancyAdmin SHALL be able to switch the active tenant context across all restaurants under the account without re-authenticating. *(implemented)*

### 1.2 Tenant Isolation
- **FR-1.2.1** All tenant-owned resources SHALL be scoped by `tenant_id` via the `ResourceVisibility` trait, preventing cross-tenant data access.
- **FR-1.2.2** Polymorphic/brokerable relationships SHALL allow orders to be linked to a mall session, marketplace, or POS while preserving tenant scoping.
- **NFR-1.2.1** Tenant data isolation SHALL be enforced at the query layer (global scopes), not solely in the UI, so an authenticated request can never read another tenant's records.
- **NFR-1.2.2** Tenant-scoped identifiers exposed publicly SHALL use non-sequential hash IDs (see [§8](#8-order--tab-management)) to prevent enumeration.

### 1.3 Subscription Entitlements
- **FR-1.3.1** A tenancy's subscription plan SHALL gate which marketplaces, POS systems, checkout gateways, and feature add-ons the account may use (entitlement pivots).
- **FR-1.3.2** Integration pickers in the UI SHALL only display integrations the account's plan entitles. *(implemented)*

---

## 2. Authentication & Access Control

### 2.1 Roles
- **FR-2.1.1** The system SHALL implement a 4-level role hierarchy: `System` (L0), `TenancyAdmin` (L1), `Tenant` (L2), `User` (L3).
- **FR-2.1.2** The `System` role SHALL bypass route-level access middleware (full platform access).
- **FR-2.1.3** Authorization SHALL be level-based: a higher level may manage lower levels, enforced by `RolePolicy`.

### 2.2 Permissions
- **FR-2.2.1** The system SHALL maintain a granular permission catalog (≈777 permissions across ≈53 groups) defined in seed data.
- **FR-2.2.2** Each role SHALL have a default permission set (System ≈775, TenancyAdmin/Tenant ≈782, User ≈255) seeded on fresh install.
- **FR-2.2.3** Route access SHALL be enforced server-side by `AccessMiddleware`; the frontend SHALL additionally hide/disable UI for unauthorized actions.
- **FR-2.2.4** A CLI command SHALL validate role-permission configuration integrity (`validate:role-permissions`).

### 2.3 Bulk Permission Manager
- **FR-2.3.1** Admins SHALL be able to view and edit permissions for many roles/resources in a single bulk interface. *(implemented)*
- **FR-2.3.2** The bulk manager SHALL support CRUD on role-permission assignments with validation against the permission catalog.

### 2.4 Authentication Mechanics
- **FR-2.4.1** API access SHALL use bearer token authentication (Sanctum-style personal access tokens).
- **FR-2.4.2** Customer mall/self-service sessions SHALL be usable **without** login (anonymous QR sessions). *(implemented)*
- **FR-2.4.3** WebSocket private channel subscription SHALL be authorized via a signed auth endpoint (`/api/ws/auth`).
- **NFR-2.4.1** Credentials and API keys SHALL never appear in committed source, documentation, or client bundles (verified by docs security review).

---

## 3. System Admin Application

> Frontend app: `kitchntabs-system` (React-Admin). Audience: platform operators (System role).

- **FR-3.1** System admins SHALL manage the catalog of platform-level integrations: `SystemMarketplace`, `SystemPointOfSale`, `SystemPaymentGateway`, and checkout gateway providers.
- **FR-3.2** System admins SHALL manage subscription plans, add-ons, and pricing.
- **FR-3.3** System admins SHALL manage tenancy accounts (create, suspend, cancel, schedule deletion) and impersonate/switch into tenant contexts for support.
- **FR-3.4** System admins SHALL manage global roles, permissions, and the bulk permission manager.
- **FR-3.5** System admins SHALL view platform-wide monitoring: active sessions, statistics, and audit/activity logs.
- **NFR-3.1** Destructive account actions (suspend/cancel/delete) SHALL be auditable and reversible where state permits.

---

## 4. Tenant / Staff Application (POS & Operations)

> Frontend app: `kitchntabs-app` (Electron + web). Modules: `kt-tabs`, `kt-store`, `kt-cashcount`, `kt-mallservice`. Audience: restaurant staff/admin.

### 4.1 Order Operations
- **FR-4.1.1** Staff SHALL view a live queue of incoming orders/tabs scoped to their tenant.
- **FR-4.1.2** Staff SHALL advance an order through its lifecycle (confirm → in preparation → prepared → delivered → closed) and cancel orders.
- **FR-4.1.3** The UI SHALL display real-time order arrivals and status changes via WebSocket without manual refresh.
- **FR-4.1.4** New/confirmed orders SHALL trigger an audible alarm and (on desktop) a spoken TTS announcement. *(implemented)*

### 4.2 Point-of-Sale Entry
- **FR-4.2.1** Staff SHALL create orders manually (counter, table, or delivery) selecting products, quantities, modifiers, and notes.
- **FR-4.2.2** The POS SHALL support delivery methods `COUNTER`, `TABLE`, and `DELIVERY`.
- **FR-4.2.3** Staff SHALL be able to print a sale note / kitchen ticket to a thermal printer. *(implemented, desktop)*

### 4.3 Cash Management
- **FR-4.3.1** The app SHALL provide a cash-count (`kt-cashcount`) workflow for shift open/close reconciliation.

### 4.4 Mall Service (Tenant side of food court)
- **FR-4.4.1** Within a mall, a tenant SHALL receive and manage only the tenant-tabs belonging to their restaurant.
- **FR-4.4.2** Staff SHALL respond to customer "assistance requested" notifications. *(implemented)*

---

## 5. Mall / Food Court Experience

> Frontend: `kitchntabs-mall` app + `kt-mall` / `kt-kiosk` packages. Audience: food-court customers and mall admins.

### 5.1 Mall Session
- **FR-5.1.1** Scanning a table QR code SHALL create/resume a `MallSession` identified by a short hash (e.g. 5 chars) and route to `/mall/session/{hash}`.
- **FR-5.1.2** The system SHALL validate the session hash and show an error for invalid/expired sessions.
- **FR-5.1.3** The session hash SHALL persist in browser storage so a customer can resume without rescanning.
- **FR-5.1.4** On first session, the system SHALL optionally collect customer data (name/contact) via a modal.

### 5.2 Multi-Restaurant Ordering
- **FR-5.2.1** A customer SHALL browse all active restaurants (tenants) in the mall with name, logo, and availability.
- **FR-5.2.2** A customer SHALL order from multiple restaurants within one session; each restaurant order becomes a **tenant tab** linked to a **master tab**.
- **FR-5.2.3** Each tenant tab's status SHALL be tracked independently while the master tab aggregates session state.
- **FR-5.2.4** Product lists SHALL support categories, search, images, availability flags, and infinite scroll.

### 5.3 Order Tracking & Assistance
- **FR-5.3.1** Customers SHALL receive real-time per-restaurant status updates over WebSocket (no polling).
- **FR-5.3.2** Customers SHALL request staff assistance from the session UI.

### 5.4 Mall Administration
- **FR-5.4.1** Mall admins SHALL configure mall settings, tenant relationships, and generate QR codes for tables/locations.
- **FR-5.4.2** Mall admins SHALL monitor active sessions and session statistics.

---

## 6. Customer & Self-Service Experience

> Modules: `kt-selfservice`, `kt-kiosk`. Audience: end customers ordering directly.

- **FR-6.1** Customers SHALL place self-service orders that progress through a visible timeline (Created → Confirmed → In Preparation → Prepared → Delivered → Closed, with Cancelled branch).
- **FR-6.2** Self-service orders SHALL integrate with a checkout gateway so the customer can pay online (see [§12](#12-checkout-gateways-end-customer-payments)). *(partial — DashTest demo working)*
- **FR-6.3** A successful self-service payment SHALL auto-confirm the tab (`CREATED → CONFIRMED`) and set `is_paid = true`. *(implemented for DashTest)*
- **FR-6.4** After payment the customer SHALL be returned to the kiosk tab-detail page (`/selfservice/{hash}/tab/{orderId}`). *(implemented)*
- **FR-6.5** Customers SHALL receive notifications about their order via socket and database channels.
- **NFR-6.1** The self-service flow SHALL be usable on shared/kiosk devices without persisting one customer's session data for the next.

---

## 7. Public Web / Marketing Site

> Frontend app: `kitchntabs-web` (deployed to Cloudflare Pages, canonical `kitchntabs.com`).

- **FR-7.1** The site SHALL serve public marketing content and the canonical apex + `www` domains.
- **FR-7.2** The site SHALL host legal pages: Privacy Policy in English and Spanish.
- **NFR-7.1** Public pages SHALL be served as a static SPA via CDN for low-latency global delivery.

---

## 8. Order & Tab Management

> Domain: `Domain\App\Models\Tab\Tab` and related Order models.

### 8.1 Tab Lifecycle
- **FR-8.1.1** A Tab SHALL have statuses `CREATED → CONFIRMED → IN_PREPARATION → PREPARED → DELIVERED → CLOSED`, plus a `CANCELLED` terminal branch.
- **FR-8.1.2** A Tab SHALL carry `hash_id`, `tenant_id`, polymorphic `order_id`, `status`, and `delivery_method`.
- **FR-8.1.3** Tab status changes SHALL broadcast a WebSocket event to the tenant channel.
- **FR-8.1.4** Tab status changes SHALL (re)generate a PDF sale note where applicable.

### 8.2 Identifiers & Audit
- **FR-8.2.1** Tabs SHALL expose a 6-character public `hash_id` (via `HasHashId`) usable for route-model binding instead of numeric IDs.
- **FR-8.2.2** Tab changes SHALL be recorded in an activity/audit log (`LogsActivity`).

### 8.3 API
- **FR-8.3.1** The API SHALL provide CRUD endpoints for tabs scoped to the tenant: `GET /api/tabs`, `GET /api/tabs/{hash_id}`, `POST /api/tabs`, `PUT /api/tabs/{hash_id}`, `DELETE /api/tabs/{hash_id}`.
- **NFR-8.3.1** List endpoints SHALL be paginated and filterable; default queries SHALL be tenant-scoped automatically.

---

## 9. Product Catalog & Modifiers

- **FR-9.1** Tenants SHALL manage products with name, description, price, image(s), category, and availability.
- **FR-9.2** Products SHALL support **modifier groups** (e.g. "Con gas / Sin gas") with per-modifier price adjustments.
- **FR-9.3** Order line items SHALL capture selected modifiers and their price adjustments at time of order.
- **FR-9.4** Catalog data exposed to mall/self-service SHALL respect availability and tenant scoping.
- **NFR-9.1** Catalog reads for customer-facing surfaces SHALL be cache-backed for responsiveness (see [§21](#21-caching--performance)).

---

## 10. Point of Sale (POS) Integration

> Domain: `SystemPointOfSale`, `TenantSystemPointOfSale`, POS instances.

- **FR-10.1** System admins SHALL define available POS integrations (`SystemPointOfSale`: class, icon, name).
- **FR-10.2** Subscription entitlement pivots (`tenancy_system_point_of_sales`) SHALL control which POS systems an account can use.
- **FR-10.3** Each tenant SHALL have exactly **one default POS**, enforced at the model layer.
- **FR-10.4** POS instances SHALL support associations to `StockType` records for inventory granularity.
- **FR-10.5** POS SHALL drive downstream data: pricelists, products, stock types, documents, and notifications.
- **FR-10.6** The platform SHALL ship at least a `ManualPosServiceProvider` (manual order entry, no external API). *(implemented)*
- **NFR-10.1** New POS providers SHALL be addable by implementing the POS service contract without changing core flows.

---

## 11. Marketplace Integrations

> Domain: `SystemMarketplace`, `Marketplace`, marketplace service classes.

### 11.1 Framework
- **FR-11.1.1** System admins SHALL define available marketplace integrations once at platform level.
- **FR-11.1.2** Subscription plans SHALL gate marketplace availability per tenancy.
- **FR-11.1.3** Each tenant SHALL independently configure and connect allowed marketplaces (per-tenant instances with OAuth tokens & connection params).
- **FR-11.1.4** The framework SHALL support OAuth flows, webhook ingestion, API-call tracking, and category/metadata sync per integration.

### 11.2 Jumpseller
- **FR-11.2.1** The system SHALL ingest Jumpseller order webhooks and create corresponding tabs/orders. *(implemented)*
- **FR-11.2.2** The system SHALL support Jumpseller catalog publishing. *(implemented)*
- **FR-11.2.3** The system SHALL implement email unsubscribe handling for Jumpseller-sourced customers. *(implemented)*
- **FR-11.2.4** Self-service checkout SHALL integrate with Jumpseller where configured. *(implemented)*

### 11.3 Uber Eats
- **FR-11.3.1** The system SHALL integrate with the Uber Eats API for order ingestion. *(implemented)*
- **FR-11.3.2** Uber CREATED orders SHALL set an `alarm` flag so staff devices alert immediately.

### 11.4 Dash Marketplace
- **FR-11.4.1** The platform SHALL support a first-party "Dash" marketplace service class.
- **NFR-11.1** Marketplace credentials SHALL be stored encrypted and never exposed to the frontend or docs.

---

## 12. Checkout Gateways (End-Customer Payments)

> Domain: Checkout Gateway Providers (CGP). Distinct from billing/subscription gateways.

- **FR-12.1** TenancyAccounts SHALL configure checkout gateway **instances**, created at account level and **shared** with one or more tenants (mirroring marketplace sharing), with a **per-tenant default** selection.
- **FR-12.2** The system SHALL expose a **generic `CheckoutGateway` contract** so providers are interchangeable.
- **FR-12.3** v1 SHALL target two CL providers to validate genericity: **Transbank Webpay** (redirect/return-URL confirmed) and **Mercado Pago** (webhook-capable). *(planned)*
- **FR-12.4** A **DashTest** demo provider (self-hosted fake bank page, no external SDK) SHALL exercise the full create-order → pay → confirm flow. *(implemented)*
- **FR-12.5** The standard checkout flow SHALL: create order → redirect to provider → on success confirm payment and update the tab.
- **FR-12.6** Webhook-capable providers SHALL confirm payment asynchronously via webhook ingestion.
- **FR-12.7** (Forward target) Branded checkout result pages SHALL be served as server-rendered Blade views reusing tenant-branding extraction, under `checkout.kitchntabs.com`. *(planned)*
- **NFR-12.1** The checkout contract SHALL not be shaped around a single provider's quirks (validated against ≥2 providers before GA).
- **NFR-12.2** Payment confirmation SHALL be idempotent so duplicate webhook/return calls do not double-confirm or double-charge.

---

## 13. Billing, Subscriptions & Payment Gateways

> Event-driven, multi-gateway billing that separates **billing authority** (gateway) from **entitlement authority** (application).

### 13.1 Gateways
- **FR-13.1.1** The system SHALL support multiple subscription billing gateways: **Internal** (simulation), **Rebill** (LATAM: ARS/BRL/CLP/COP/MXN), **Flow.cl** (CL/PE/MX), and **Transbank**.
- **FR-13.1.2** All gateways SHALL implement a common `PaymentGatewayContract`.
- **FR-13.1.3** Gateway webhooks SHALL drive subscription state changes.

### 13.2 Subscription Lifecycle
- **FR-13.2.1** Subscriptions SHALL be linked to a **Tenancy** (not an individual user).
- **FR-13.2.2** The system SHALL run separate state machines for **billing** lifecycle and **subscription/entitlement** lifecycle.
- **FR-13.2.3** **Upgrades** SHALL apply immediately; **downgrades** SHALL be deferred to period end.
- **FR-13.2.4** Trial periods SHALL automatically transition `trial → active → suspended → deleted` per policy.
- **FR-13.2.5** The system SHALL support subscription reactivation after lapse.
- **FR-13.2.6** Plan changes SHALL emit a notification the frontend can react to (refresh entitlements). *(implemented)*

### 13.3 Add-ons & Pricing
- **FR-13.3.1** Plans SHALL support add-ons that extend entitlements (extra marketplaces, POS, etc.).
- **FR-13.3.2** A price-formatting service SHALL render currency consistently across locales.

### 13.4 Audit
- **FR-13.4.1** All billing operations SHALL emit domain events and be recorded via activity logging.
- **NFR-13.1** Billing state SHALL be reconstructable from the event/audit trail.
- **NFR-13.2** A failed payment SHALL never silently revoke entitlements; revocation SHALL follow the defined suspension policy with grace handling.

---

## 14. Notifications & Real-Time Messaging

> Channels: 🔌 Socket (WebSocket), 📧 Email, 💾 Database, 📱 Push (FCM).

### 14.1 Real-Time Transport
- **FR-14.1.1** The system SHALL deliver real-time events over WebSockets (Laravel Echo + Pusher protocol / Reverb-Soketi).
- **FR-14.1.2** Private channels SHALL be per-tenant (`private-tenant.{id}.system`) and authorized via the auth endpoint.
- **FR-14.1.3** A Python device service AND the web client SHALL both be able to subscribe to tenant channels.

### 14.2 Notification Catalog (representative)
- **FR-14.2.1** **Order/Tab status notifications** SHALL fire on create/confirm/prepare/deliver/close to kitchen, waitstaff, and admins via Socket + Email + DB + Push.
- **FR-14.2.2** **Tab status notifications** for public POS displays SHALL fire over Socket.
- **FR-14.2.3** **Mall session order status** SHALL notify the customer over Socket + DB.
- **FR-14.2.4** **Assistance requests** SHALL notify tenant staff in real time.
- **FR-14.2.5** **Subscription/plan-change** and **billing** notifications SHALL be delivered to account admins.
- **FR-14.2.6** Each notification SHALL declare its target audience and delivery channels.

### 14.3 Email
- **FR-14.3.1** Transactional emails SHALL be sent via SES with bounce/complaint handling (SNS → Lambda → webhook).
- **FR-14.3.2** Emails SHALL use tenant branding extraction for per-tenant look & feel.
- **FR-14.3.3** Email content SHALL be translatable (backend translations).

### 14.4 Push
- **FR-14.4.1** Mobile push SHALL be delivered via Firebase Cloud Messaging (FCM).

- **NFR-14.1** Notification delivery SHALL degrade gracefully: if one channel fails, others SHALL still deliver.
- **NFR-14.2** Duplicate notifications SHALL be de-duplicated client-side by a stable key (timestamp + tab id).

---

## 15. AI Agents (Voice & Image)

> Two AI-assisted order-entry features integrated with the Tab system.

### 15.1 Voice Agent
- **FR-15.1.1** The system SHALL accept spoken commands and transcribe them (Whisper) to add/remove/modify products in an order.
- **FR-15.1.2** Recognized actions SHALL resolve to real catalog products and modifiers before being applied.

### 15.2 Image Agent
- **FR-15.2.1** The system SHALL analyze uploaded images (menus, handwritten orders, receipts) via a vision model to extract order line items.
- **FR-15.2.2** Extracted items SHALL pass through the same product/modifier resolution pipeline.

### 15.3 Shared Pipeline
- **FR-15.3.1** Both agents SHALL present an analysis drawer showing detected actions and status indicators before committing.
- **FR-15.3.2** Modifier resolution SHALL map free-text modifiers to defined modifier groups.
- **FR-15.3.3** AI features SHALL expose configuration options (enable/disable, model selection where applicable).
- **NFR-15.1** AI provider keys SHALL be server-side only; the client SHALL never call the AI provider directly.
- **NFR-15.2** AI extraction SHALL be advisory — a human SHALL confirm before the order is finalized.

---

## 16. Desktop Shell & Device Service (Electron + Python)

> `kitchntabs-app` Electron shell + `dash-python-service` (kt_service, print_service, tts_service).

### 16.1 Desktop Shell
- **FR-16.1.1** The desktop app SHALL run the React app inside Electron with auto-update support.
- **FR-16.1.2** The shell SHALL spawn and supervise the Python background service, passing the auth token, tenant channel, config path, and log path.
- **FR-16.1.3** The shell SHALL acquire a single-instance lock and clean up stale locks on start.
- **FR-16.1.4** The shell SHALL load a per-build config (`config.<custom_mode>.yaml`) selecting endpoints, printer, and speech settings.
- **FR-16.1.5** The shell SHALL expose an IPC bridge (`DashIPCService`) for `speak`, `playSound`, `print`, `notify`, and Python script control.

### 16.2 Printing
- **FR-16.2.1** The service SHALL print kitchen tickets / sale notes to a configured thermal/ESC-POS printer (vendor/product/device path/max width configurable).
- **FR-16.2.2** The service SHALL fetch a PDF by URL and print it on demand via IPC.

### 16.3 Text-to-Speech (Audio)
- **FR-16.3.1** The service SHALL generate spoken audio for configurable messages (welcome, connected/disconnected, order events) in a configurable language (default `es`).
- **FR-16.3.2** Confirmed orders and assistance requests SHALL trigger a spoken announcement on the desktop. *(implemented)*
- **FR-16.3.3** TTS triggered alongside an alarm SHALL be delayed to play after the alarm completes.

### 16.4 Connectivity Resilience
- **FR-16.4.1** The service SHALL monitor internet connectivity and reflect connection state.
- **FR-16.4.2** The service SHALL reconnect to the WebSocket server and re-subscribe to its channel after disconnects.
- **NFR-16.1** The desktop service SHALL be buildable for multiple architectures (x64/arm, incl. armv7l) via the documented PyInstaller toolchain.
- **NFR-16.2** Device-service failures (printer offline, TTS binary missing) SHALL be logged and SHALL NOT crash the desktop app.

---

## 17. Campaigns & Marketing Automation

- **FR-17.1** Admins SHALL create and manage marketing campaigns (campaign manager).
- **FR-17.2** The system SHALL support a campaign publishing workflow.
- **FR-17.3** Campaigns SHALL target customer segments and integrate with the notification/email channels.
- **NFR-17.1** Campaign sends SHALL respect unsubscribe state and email-suppression (bounces/complaints).

---

## 18. Product Import / Export

- **FR-18.1** Tenants SHALL bulk-import products via the product import system (file-based).
- **FR-18.2** Tenants SHALL export their product catalog.
- **FR-18.3** Import SHALL validate rows and report errors per row before committing.
- **NFR-18.1** Large imports SHALL be processed without blocking the UI (background/queue where applicable).

---

## 19. Internationalization (i18n)

- **FR-19.1** The frontend SHALL support multiple languages with per-app i18n resources.
- **FR-19.2** The backend SHALL support translated content for emails and notifications.
- **FR-19.3** Status labels (e.g. `tab.status.*`) SHALL be translatable with sensible fallbacks.
- **FR-19.4** Speech announcements SHALL honor the configured `SPEECH_LANGUAGE`.
- **NFR-19.1** Spanish and English SHALL be first-class; adding a locale SHALL not require code changes to consuming components.

---

## 20. Media & Image Management

- **FR-20.1** Models SHALL support attached image resources with generated conversions (e.g. preview sizes).
- **FR-20.2** Media SHALL be stored in S3 buckets: public (`kitchntabs`), private (`kitchntabs-private`), and dev variants.
- **FR-20.3** Public assets SHALL be served via public S3/CDN URLs; private files SHALL require authorized access.
- **NFR-20.1** Image conversions SHALL be generated asynchronously and cached.

---

## 21. Caching & Performance

- **FR-21.1** Customer-facing mall product reads SHALL use a dedicated cache layer (mall products cache).
- **FR-21.2** The frontend SHALL use React Query caching with defined invalidation for mall data.
- **FR-21.3** Backend SHALL use Redis/Valkey for cache, sessions, and queues.
- **NFR-21.1** Cache invalidation SHALL occur on the underlying data mutation so customers never see stale availability/pricing beyond a bounded window.

---

## 22. Infrastructure, Build & Deployment

### 22.1 Backend Infrastructure (AWS, `kitchntabs-ci-cdk`)
- **FR-22.1.1** Infrastructure SHALL be defined as code via AWS CDK v2 (TypeScript) using a dynamic multi-stack pattern keyed by `STACK_TYPE`/`ENV`.
- **FR-22.1.2** Stacks SHALL provision: Infrastructure (S3/ECR/SES), Database (RDS PostgreSQL), Redis (ElastiCache Valkey), and Backend (ECS Fargate + ALB + autoscaling + Secrets Manager).
- **FR-22.1.3** The backend SHALL run as an ARM64 Fargate service behind an HTTPS ALB with HTTP→HTTPS redirect.
- **FR-22.1.4** Each deploy SHALL generate an endpoints manifest (`outputs/endpoints.<env>.{json,md}`).
- **FR-22.1.5** ECS Exec SHALL be enabled for shell access to run migrations/maintenance.

### 22.2 Frontend Deployment (Cloudflare)
- **FR-22.2.1** Frontend apps SHALL build per-app and deploy to Cloudflare Pages, with custom domains and proxied CNAME DNS upserted automatically.
- **FR-22.2.2** The deploy flow SHALL disable ECH at the zone level (via Cloudflare API) while keeping TLS 1.3. *(implemented)*
- **FR-22.2.3** Apps SHALL be processed sequentially (config → build → deploy) due to shared build output.

### 22.3 Configuration
- **FR-22.3.1** Each stack/app SHALL be configured via layered `.env.<env>` files merged at runtime; secrets SHALL be git-ignored.
- **FR-22.3.2** A build-config generator SHALL emit `build_config.json` driving Vite per platform (web/electron/mobile).
- **NFR-22.1** Deployment SHALL be reproducible from a clean workstation following documented phase order (Bootstrap → Infra → DB → Redis → Backend).

---

## 23. Cross-Cutting Non-Functional Requirements

### 23.1 Security
- **NFR-23.1.1** All external traffic SHALL be encrypted (TLS 1.3); Redis connections SHALL use TLS.
- **NFR-23.1.2** Secrets SHALL be stored in AWS Secrets Manager / encrypted env, never in source, bundles, or docs.
- **NFR-23.1.3** Authorization SHALL be enforced server-side; client-side gating is presentation only.
- **NFR-23.1.4** Public identifiers SHALL be non-enumerable hash IDs.
- **NFR-23.1.5** Webhook handlers SHALL verify provider signatures/authenticity where the provider supports it.

### 23.2 Reliability & Availability
- **NFR-23.2.1** The backend SHALL auto-scale (1–2+ tasks) and self-heal failed tasks via ECS health checks.
- **NFR-23.2.2** A health endpoint (`/api/healthz`) SHALL report service health for the ALB and monitoring.
- **NFR-23.2.3** Real-time clients SHALL automatically reconnect and resubscribe after network interruptions.
- **NFR-23.2.4** Order/payment operations SHALL be idempotent against retried webhooks and duplicate client events.

### 23.3 Performance
- **NFR-23.3.1** Customer-facing reads SHALL be cache-backed and paginated; list views SHALL avoid N+1 queries.
- **NFR-23.3.2** Static frontends SHALL be CDN-delivered for low global latency.

### 23.4 Observability
- **NFR-23.4.1** Application logs SHALL ship to CloudWatch (`/ecs/api`) with defined retention.
- **NFR-23.4.2** All significant domain/billing actions SHALL be recorded in an activity/audit log (Spatie ActivityLog).
- **NFR-23.4.3** The desktop service SHALL write a local rotating log for field diagnostics.

### 23.5 Maintainability & Extensibility
- **NFR-23.5.1** The backend SHALL follow domain-driven structure (`domain/app/...`) separating models, controllers, services, and notifications.
- **NFR-23.5.2** Integrations (marketplace, POS, payment, checkout) SHALL be addable via contracts without modifying core flows.
- **NFR-23.5.3** The frontend SHALL be a pnpm monorepo of reusable `dash-*` / `kt-*` packages shared across apps.
- **NFR-23.5.4** Role/permission definitions SHALL be data-driven (JSON seeds) and validated by tooling.

### 23.6 Portability
- **NFR-23.6.1** The app SHALL run as web (Cloudflare Pages), desktop (Electron, multi-arch), and SHALL retain a Capacitor mobile build path.
- **NFR-23.6.2** The backend image SHALL be ARM64-first for cost efficiency on Graviton/Fargate.

### 23.7 Compliance & Privacy
- **NFR-23.7.1** The platform SHALL publish bilingual privacy policies and honor email unsubscribe requests.
- **NFR-23.7.2** Customer PII collected in anonymous sessions SHALL be minimized and scoped to the session/order.

---

## Appendix A — Component → Source Map

| Component | Primary location |
|-----------|------------------|
| Backend API (Laravel, DDD) | `dash-backend/domain/app/...`, `dash-backend/app/...` |
| System admin SPA | `kitchntabs-frontend/apps/kitchntabs-system` |
| Mall/food-court SPA | `kitchntabs-frontend/apps/kitchntabs-mall` + `packages/kt-mall`, `packages/kt-kiosk` |
| Staff/POS desktop app | `kitchntabs-frontend/apps/kitchntabs-app` (+ `kt-tabs`, `kt-store`, `kt-cashcount`, `kt-selfservice`, `kt-mallservice`) |
| Public web | `kitchntabs-frontend/apps/kitchntabs-web` |
| Shared FE packages | `kitchntabs-frontend/packages/dash-*`, `kt-*` |
| Device service | `dash-python-service/src` (`kt_service.py`, `print_service.py`, `tts_service.py`) |
| Infrastructure | `kitchntabs-ci-cdk` |

## Appendix B — Status Legend

| Tag | Meaning |
|-----|---------|
| `(implemented)` | Built and in use per docs/code. |
| `(partial)` | Partially built / one provider or path working. |
| `(planned)` | Specified as forward target, not yet built. |
| *(untagged)* | Required behavior; maturity not separately asserted here. |

---

<p align="center"><em>Generated from KitchnTabs documentation and codebase, 2026-06-25.</em></p>
