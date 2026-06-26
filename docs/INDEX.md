
# KitchnTabs Documentation Index

Complete documentation index organized by epic. Each section contains the epic description and all associated technical documents.

**Total Epics:** 35 (25 Functional + 10 Non-Functional)  
**Total Documents:** 195+

---

## Table of Contents

### Functional Epics (F1–F25)
- [F1: Orders & Tabs](#f1-orders--tabs)
- [F2: Products & Catalog](#f2-products--catalog)
- [F3: Product Import / Export](#f3-product-import--export)
- [F4: Mall / Food Court](#f4-mall--food-court)
- [F5: Customer & Self-Service](#f5-customer--self-service)
- [F6: Tenant / Staff App](#f6-tenant--staff-app)
- [F7: System Admin Application](#f7-system-admin-application)
- [F8: Public Web](#f8-public-web)
- [F9: Marketplaces](#f9-marketplaces)
- [F10: Point of Sale](#f10-point-of-sale)
- [F11: Checkout Gateways](#f11-checkout-gateways)
- [F12: Billing & Subscriptions](#f12-billing--subscriptions--payments)
- [F13: Platform & Multi-Tenancy](#f13-platform--multi-tenancy)
- [F14: Auth & Access Control](#f14-auth--access-control)
- [F15: Notifications & Messaging](#f15-notifications--messaging)
- [F16: AI Agents](#f16-ai-agents)
- [F17: Inventory](#f17-inventory)
- [F18: Campaigns](#f18-campaigns)
- [F19: Internationalization](#f19-internationalization)
- [F20: Media & Images](#f20-media--images)
- [F21: Tenancy Management](#f21-tenancy-management)
- [F22: MiddlewareService](#f22-middlewareservice)
- [F23: DeliveryModule](#f23-deliverymodule)
- [F24: InventoryModule](#f24-inventorymodule)
- [F25: CashcountModule](#f25-cashcountmodule)

### Non-Functional Epics (N1–N10)
- [N1: Backend Framework](#n1-backend-framework)
- [N2: Frontend Framework](#n2-frontend-framework)
- [N3: Infrastructure & CI/CD](#n3-infrastructure--cicd)
- [N4: Build Toolchain](#n4-build-toolchain)
- [N5: Desktop & Device Service](#n5-desktop--device-service)
- [N6: Caching & Performance](#n6-caching--performance)
- [N7: Security](#n7-security)
- [N8: Observability](#n8-observability)
- [N9: App Publishing](#n9-app-publishing)
- [N10: Administrative & Legal](#n10-administrative--legal)

---

## Functional Epics (F1–F25)

### F1: Orders & Tabs

**Restaurant order management system with complete order lifecycle tracking.**

Manages restaurant tabs and orders from creation through delivery. Includes order confirmation, preparation status tracking, delivery method management (counter, table, delivery), and cancellation workflows. Implements real-time order updates via WebSocket and integrates with kitchen display systems. Features automatic receipt generation and audit trail logging for all order state changes.

**Documents:**
- [F1-Orders-Tabs_DELETE_TENANCY_ACCOUNT.md](F1-Orders-Tabs/F1-Orders-Tabs_DELETE_TENANCY_ACCOUNT.md) — Account lifecycle
- [F1-Orders-Tabs_DELIVERY.md](F1-Orders-Tabs/F1-Orders-Tabs_DELIVERY.md) — Delivery tracking
- [F1-Orders-Tabs_HASH_ID_IMPLEMENTATION.md](F1-Orders-Tabs/F1-Orders-Tabs_HASH_ID_IMPLEMENTATION.md) — Hash ID strategy
- [F1-Orders-Tabs_Order-README.md](F1-Orders-Tabs/F1-Orders-Tabs_Order-README.md) — Order model reference
- [F1-Orders-Tabs_TABS_MALLTABS_ARCHITECTURE.md](F1-Orders-Tabs/F1-Orders-Tabs_TABS_MALLTABS_ARCHITECTURE.md) — Tab/mall architecture
- [F1-Orders-Tabs_Tab-README.md](F1-Orders-Tabs/F1-Orders-Tabs_Tab-README.md) — Tab domain model

---

### F2: Products & Catalog

**Product information management with pricing and customization support.**

Comprehensive product catalog with support for multiple categories, hierarchical product organization, and dynamic pricing. Includes modifier groups for customizable items (sizes, toppings, options), discount application, and product-level availability management. Supports bulk operations, attribute management, and integration with inventory systems for real-time stock updates.

**Documents:**
- [F2-Products-Catalog_DISCOUNT_FEATURE.md](F2-Products-Catalog/F2-Products-Catalog_DISCOUNT_FEATURE.md) — Discount system
- [F2-Products-Catalog_ECommerce-README.md](F2-Products-Catalog/F2-Products-Catalog_ECommerce-README.md) — Product domain model
- [F2-Products-Catalog_MODIFIER_GROUPS_FEATURE.md](F2-Products-Catalog/F2-Products-Catalog_MODIFIER_GROUPS_FEATURE.md) — Modifier groups & pricing

---

### F3: Product Import / Export

**Bulk product data ingestion and export functionality.**

Automated import/export system for products with validation, error handling, and batch processing. Supports multiple file formats (CSV, Excel), field mapping configuration, and dry-run validation before commit. Includes error reporting, duplicate detection, and rollback capabilities. Handles large-scale product updates efficiently with progress tracking and import history.

**Documents:**
- [F3-Product-Import-Export_PRODUCT_IMPORT_EXPORT_USER_GUIDE.md](F3-Product-Import-Export/F3-Product-Import-Export_PRODUCT_IMPORT_EXPORT_USER_GUIDE.md) — Import/export guide
- [F3-Product-Import-Export_PRODUCT_IMPORT_SYSTEM_DOCUMENTATION.md](F3-Product-Import-Export/F3-Product-Import-Export_PRODUCT_IMPORT_SYSTEM_DOCUMENTATION.md) — Bulk import validation

---

### F4: Mall / Food Court

**Multi-store food court management and shared marketplace.**

Unified platform for managing multiple vendors/stores within a single food court environment. Enables shared meal sessions across stores, collaborative ordering, and store-level inventory management. Includes session management, multi-store notifications, authentication across stores, and aggregated reporting. Supports independent store branding while maintaining cross-store functionality.

**Documents:**
- [F4-Mall-Food-Court_01-OVERVIEW.md](F4-Mall-Food-Court/F4-Mall-Food-Court_01-OVERVIEW.md) — Mall app overview
- [F4-Mall-Food-Court_02-ARCHITECTURE.md](F4-Mall-Food-Court/F4-Mall-Food-Court_02-ARCHITECTURE.md) — Architecture
- [F4-Mall-Food-Court_03-BACKEND-MODELS.md](F4-Mall-Food-Court/F4-Mall-Food-Court_03-BACKEND-MODELS.md) — Backend models
- [F4-Mall-Food-Court_04-BACKEND-CONTROLLERS.md](F4-Mall-Food-Court/F4-Mall-Food-Court_04-BACKEND-CONTROLLERS.md) — Controllers
- [F4-Mall-Food-Court_05-BACKEND-SERVICES.md](F4-Mall-Food-Court/F4-Mall-Food-Court_05-BACKEND-SERVICES.md) — Services
- [F4-Mall-Food-Court_06-NOTIFICATIONS.md](F4-Mall-Food-Court/F4-Mall-Food-Court_06-NOTIFICATIONS.md) — Notifications
- [F4-Mall-Food-Court_07-FRONTEND-ARCHITECTURE.md](F4-Mall-Food-Court/F4-Mall-Food-Court_07-FRONTEND-ARCHITECTURE.md) — Frontend architecture
- [F4-Mall-Food-Court_08-FRONTEND-COMPONENTS.md](F4-Mall-Food-Court/F4-Mall-Food-Court_08-FRONTEND-COMPONENTS.md) — Components
- [F4-Mall-Food-Court_09-USER-STORIES.md](F4-Mall-Food-Court/F4-Mall-Food-Court_09-USER-STORIES.md) — User stories
- [F4-Mall-Food-Court_10-FLOW-DIAGRAMS.md](F4-Mall-Food-Court/F4-Mall-Food-Court_10-FLOW-DIAGRAMS.md) — Flow diagrams
- [F4-Mall-Food-Court_KITCHNTABS_MALL_APPLICATION_FLOW.md](F4-Mall-Food-Court/F4-Mall-Food-Court_KITCHNTABS_MALL_APPLICATION_FLOW.md) — Application flow
- [F4-Mall-Food-Court_KITCHNTABS_MALL_AUTHENTICATION_FLOW.md](F4-Mall-Food-Court/F4-Mall-Food-Court_KITCHNTABS_MALL_AUTHENTICATION_FLOW.md) — Auth flow diagram
- [F4-Mall-Food-Court_KITCHNTABS_MALL_AUTH_FLOW.md](F4-Mall-Food-Court/F4-Mall-Food-Court_KITCHNTABS_MALL_AUTH_FLOW.md) — Auth flow
- [F4-Mall-Food-Court_KITCHNTABS_MALL_WEBSOCKET_SYSTEM.md](F4-Mall-Food-Court/F4-Mall-Food-Court_KITCHNTABS_MALL_WEBSOCKET_SYSTEM.md) — WebSocket system
- [F4-Mall-Food-Court_Mall-README.md](F4-Mall-Food-Court/F4-Mall-Food-Court_Mall-README.md) — Mall model
- [F4-Mall-Food-Court_tenant-marketplace-campaign-architecture.md](F4-Mall-Food-Court/F4-Mall-Food-Court_tenant-marketplace-campaign-architecture.md) — Multi-tenant campaign arch

---

### F5: Customer & Self-Service

**Customer-facing application and self-service ordering platform.**

Dedicated mobile and web application for customers to browse products, place orders, and track delivery. Features session-based ordering with real-time updates via WebSocket, order status notifications, and delivery tracking. Includes customer account management, order history, loyalty program integration, and secure payment processing. Supports trial registration and account lifecycle management.

**Documents:**
- [F5-Customer-Self-Service_CUSTOMER_APP_COMPLETE_FLOW.md](F5-Customer-Self-Service/F5-Customer-Self-Service_CUSTOMER_APP_COMPLETE_FLOW.md) — Complete customer flow
- [F5-Customer-Self-Service_MALL_SESSION_NOTIFICATIONS_FLOW.md](F5-Customer-Self-Service/F5-Customer-Self-Service_MALL_SESSION_NOTIFICATIONS_FLOW.md) — Session notifications
- [F5-Customer-Self-Service_MALL_SESSION_ORDER_UPDATE_FLOW.md](F5-Customer-Self-Service/F5-Customer-Self-Service_MALL_SESSION_ORDER_UPDATE_FLOW.md) — Order update flow
- [F5-Customer-Self-Service_SELFSERVICE_API_REFERENCE.md](F5-Customer-Self-Service/F5-Customer-Self-Service_SELFSERVICE_API_REFERENCE.md) — API reference
- [F5-Customer-Self-Service_SELFSERVICE_FEATURE.md](F5-Customer-Self-Service/F5-Customer-Self-Service_SELFSERVICE_FEATURE.md) — Self-service feature spec
- [F5-Customer-Self-Service_SELFSERVICE_TECHNICAL_DOC.md](F5-Customer-Self-Service/F5-Customer-Self-Service_SELFSERVICE_TECHNICAL_DOC.md) — Technical documentation
- [F5-Customer-Self-Service_SELFSERVICE_USER_GUIDE.md](F5-Customer-Self-Service/F5-Customer-Self-Service_SELFSERVICE_USER_GUIDE.md) — User guide
- [F5-Customer-Self-Service_TRIAL_REGISTRATION_FLOW.md](F5-Customer-Self-Service/F5-Customer-Self-Service_TRIAL_REGISTRATION_FLOW.md) — Trial flow

---

### F6: Tenant / Staff App

**Staff and vendor management application with role-based workflows.**

Dedicated application for restaurant staff and store managers. Includes order management, inventory tracking, staff scheduling, performance analytics, and real-time notifications. Features role-based access control, shift management, and communication tools. Integrates with point-of-sale systems and provides comprehensive reporting and insights for operational management.

**Documents:**
- [F6-Tenant-Staff-App_PYTHON_SERVICE_TESTING.md](F6-Tenant-Staff-App/F6-Tenant-Staff-App_PYTHON_SERVICE_TESTING.md) — Python device service testing
- [F6-Tenant-Staff-App_STAFF_APP_COMPLETE_FLOW.md](F6-Tenant-Staff-App/F6-Tenant-Staff-App_STAFF_APP_COMPLETE_FLOW.md) — Complete staff flow
- [F6-Tenant-Staff-App_STAFF_APP_NOTIFICATIONS_FLOW.md](F6-Tenant-Staff-App/F6-Tenant-Staff-App_STAFF_APP_NOTIFICATIONS_FLOW.md) — Notifications flow

---

### F7: System Admin Application

**Administrative dashboard for platform management and oversight.**

Comprehensive admin portal for platform operators and system administrators. Enables user management, tenant administration, system settings configuration, and global reporting. Includes audit trail viewing, security management, and system health monitoring. Supports bulk operations, user provisioning, and compliance tracking. Features sidebar navigation for all administrative functions.

**Documents:**
- [F7-System-Admin-Application_DASH-ADMIN-AUDIT.md](F7-System-Admin-Application/F7-System-Admin-Application_DASH-ADMIN-AUDIT.md) — Admin audit trail
- [F7-System-Admin-Application_DASH_ADMIN_FRAMEWORK.md](F7-System-Admin-Application/F7-System-Admin-Application_DASH_ADMIN_FRAMEWORK.md) — Admin framework
- [F7-System-Admin-Application_DASH_DIALOG.md](F7-System-Admin-Application/F7-System-Admin-Application_DASH_DIALOG.md) — Dialog components
- [F7-System-Admin-Application_DASH_LAZY_ADMIN_APP_RERENDERING_BUG.md](F7-System-Admin-Application/F7-System-Admin-Application_DASH_LAZY_ADMIN_APP_RERENDERING_BUG.md) — Rerendering issue
- [F7-System-Admin-Application_REACT-ADMIN-LIST.md](F7-System-Admin-Application/F7-System-Admin-Application_REACT-ADMIN-LIST.md) — React-Admin guide
- [F7-System-Admin-Application_SIDEBAR_ARCHITECTURE.md](F7-System-Admin-Application/F7-System-Admin-Application_SIDEBAR_ARCHITECTURE.md) — Sidebar architecture

---

### F8: Public Web

**Public-facing website and brand presence.**

Marketing website and public information portal. Includes company information, product showcase, pricing pages, contact forms, and brand storytelling. Implements responsive design, SEO optimization, and integrations with marketing tools. Features blog section, FAQ, and call-to-action elements for customer acquisition and engagement.

**Documents:**
- [F8-Public-Web_# Dash Design System: Color & Theme Arch.md](F8-Public-Web/F8-Public-Web_# Dash Design System: Color & Theme Arch.md) — Color/theme arch
- [F8-Public-Web_DASH_DESIGN_SYSTEM_VARIABLES.md](F8-Public-Web/F8-Public-Web_DASH_DESIGN_SYSTEM_VARIABLES.md) — Design tokens
- [F8-Public-Web_design-system-less-css.md](F8-Public-Web/F8-Public-Web_design-system-less-css.md) — Design system

---

### F9: Marketplaces

**Third-party marketplace integrations and synchronization.**

Integration layer for external marketplaces (Jumpseller, Uber Eats, etc.). Enables product catalog sync, order synchronization, inventory management, and fulfillment workflows. Handles bidirectional data flow between platforms, order routing, and multi-channel order consolidation. Supports platform-specific rules, commission handling, and dispute resolution.

**Documents:**
- [F9-Marketplaces_FEAT-SYSTEM-MARKETPLACES.md](F9-Marketplaces/F9-Marketplaces_FEAT-SYSTEM-MARKETPLACES.md) — System framework
- [F9-Marketplaces_JUMPSELLER-API.md](F9-Marketplaces/F9-Marketplaces_JUMPSELLER-API.md) — Jumpseller API reference
- [F9-Marketplaces_JUMPSELLER.PUBLISHING.md](F9-Marketplaces/F9-Marketplaces_JUMPSELLER.PUBLISHING.md) — Publishing
- [F9-Marketplaces_JUMPSELLER_UNSUBSCRIBE_IMPLEMENTATION.md](F9-Marketplaces/F9-Marketplaces_JUMPSELLER_UNSUBSCRIBE_IMPLEMENTATION.md) — Unsubscribe
- [F9-Marketplaces_MARKETPLACE_SERVICE_OVERVIEW.md](F9-Marketplaces/F9-Marketplaces_MARKETPLACE_SERVICE_OVERVIEW.md) — Service overview
- [F9-Marketplaces_Marketplace-README.md](F9-Marketplaces/F9-Marketplaces_Marketplace-README.md) — Marketplace model
- [F9-Marketplaces_UBER_API.md](F9-Marketplaces/F9-Marketplaces_UBER_API.md) — Uber API
- [F9-Marketplaces_UBER_INTEGRATION.md](F9-Marketplaces/F9-Marketplaces_UBER_INTEGRATION.md) — Uber integration
- [F9-Marketplaces_UBER_INTEGRATION2.md](F9-Marketplaces/F9-Marketplaces_UBER_INTEGRATION2.md) — Uber integration reference
- [F9-Marketplaces_USER_PREFERENCES_SYSTEM2.md](F9-Marketplaces/F9-Marketplaces_USER_PREFERENCES_SYSTEM2.md) — User preferences

---

### F10: Point of Sale

**Physical point-of-sale system integration and management.**

Integration with traditional POS systems for in-store transactions. Enables unified order management across online and in-store channels. Features transaction processing, receipt generation, drawer management, and reconciliation. Supports offline functionality and synchronization with central systems.

**Documents:**
- [F10-Point-of-Sale_FEAT-SYSTEM-POINT-OF-SALES.md](F10-Point-of-Sale/F10-Point-of-Sale_FEAT-SYSTEM-POINT-OF-SALES.md) — POS framework

---

### F11: Checkout Gateways

**Payment processor integrations and checkout flows.**

Multi-gateway payment processing with support for various payment methods (credit cards, digital wallets, local payment systems). Integrates with payment processors (Transbank, Mercado Pago, Flow.cl, Rebill). Features secure checkout flows, PCI compliance, recurring payment support, and transaction reconciliation. Handles payment failures, retries, and dispute management.

**Documents:**
- [F11-Checkout-Gateways_CHECKOUT_GATEWAYS_FEATURE.md](F11-Checkout-Gateways/F11-Checkout-Gateways_CHECKOUT_GATEWAYS_FEATURE.md) — Base interface
- [F11-Checkout-Gateways_FEAT-MERCADOPAGO.md](F11-Checkout-Gateways/F11-Checkout-Gateways_FEAT-MERCADOPAGO.md) — Mercado Pago
- [F11-Checkout-Gateways_FEAT-SYSTEM-CHECKOUT-GATEWAYS.md](F11-Checkout-Gateways/F11-Checkout-Gateways_FEAT-SYSTEM-CHECKOUT-GATEWAYS.md) — Base interface
- [F11-Checkout-Gateways_FEAT-TRANSBANK-PST.md](F11-Checkout-Gateways/F11-Checkout-Gateways_FEAT-TRANSBANK-PST.md) — Transbank Webpay
- [F11-Checkout-Gateways_ML-CHECKOUT-PRO-DOCS.md](F11-Checkout-Gateways/F11-Checkout-Gateways_ML-CHECKOUT-PRO-DOCS.md) — Mercado Pago checkout pro
- [F11-Checkout-Gateways_ML-WEBHOOKS.md](F11-Checkout-Gateways/F11-Checkout-Gateways_ML-WEBHOOKS.md) — Webhooks
- [F11-Checkout-Gateways_TRANSBANK_INTEGRATION.md](F11-Checkout-Gateways/F11-Checkout-Gateways_TRANSBANK_INTEGRATION.md) — Transbank integration

---

### F12: Billing, Subscriptions & Payments

**Subscription management, invoicing, and revenue operations.**

Complete billing platform with subscription plan management, usage-based billing, and recurring payments. Includes invoice generation, payment collection, dunning workflows, and financial reporting. Features plan customization, add-ons management, proration handling, and lifecycle management (activation, renewal, cancellation). Supports multiple billing currencies and tax calculation.

**Documents:**
- [F12-Billing-Subscriptions-Payments_BILLING_POLICY_README.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_BILLING_POLICY_README.md) — Policy reference
- [F12-Billing-Subscriptions-Payments_CANCEL_SUBSCRIPTION.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_CANCEL_SUBSCRIPTION.md) — Cancellation flow
- [F12-Billing-Subscriptions-Payments_EVENT_DRIVEN_BILLING_ARCHITECTURE.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_EVENT_DRIVEN_BILLING_ARCHITECTURE.md) — Event-driven architecture
- [F12-Billing-Subscriptions-Payments_FEATURE-PAYMENTS.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_FEATURE-PAYMENTS.md) — Payments overview
- [F12-Billing-Subscriptions-Payments_FLOW_PAYMENT_GATEWAY.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_FLOW_PAYMENT_GATEWAY.md) — Flow.cl gateway
- [F12-Billing-Subscriptions-Payments_KITCHNTABS_BILLING_POLICY.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_KITCHNTABS_BILLING_POLICY.md) — Billing policy
- [F12-Billing-Subscriptions-Payments_LARAVEL_CASHIER_INTEGRATION.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_LARAVEL_CASHIER_INTEGRATION.md) — Cashier integration
- [F12-Billing-Subscriptions-Payments_PAYMENT-GATEWAY-TESTS.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_PAYMENT-GATEWAY-TESTS.md) — Payment gateway tests
- [F12-Billing-Subscriptions-Payments_PAYMENT_GATEWAYS.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_PAYMENT_GATEWAYS.md) — Payment gateways
- [F12-Billing-Subscriptions-Payments_PAYMENT_GATEWAY_INTEGRATION.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_PAYMENT_GATEWAY_INTEGRATION.md) — Integration guide
- [F12-Billing-Subscriptions-Payments_PRICE_FORMATTING_SERVICE.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_PRICE_FORMATTING_SERVICE.md) — Price formatting
- [F12-Billing-Subscriptions-Payments_REBILL_PAYMENT_GATEWAY.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_REBILL_PAYMENT_GATEWAY.md) — Rebill gateway
- [F12-Billing-Subscriptions-Payments_REDBILL-API.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_REDBILL-API.md) — Rebill API
- [F12-Billing-Subscriptions-Payments_SUBSCRIPTION_BUG_FIXES.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_SUBSCRIPTION_BUG_FIXES.md) — Bug fixes & patches
- [F12-Billing-Subscriptions-Payments_SUBSCRIPTION_FLOW_TECHNICAL_DOCUMENTATION.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_SUBSCRIPTION_FLOW_TECHNICAL_DOCUMENTATION.md) — Subscription flow
- [F12-Billing-Subscriptions-Payments_SUBSCRIPTION_PLAN_ADDONS_FEATURE.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_SUBSCRIPTION_PLAN_ADDONS_FEATURE.md) — Plans & add-ons
- [F12-Billing-Subscriptions-Payments_SUBSCRIPTION_REACTIVATION_TECHNICAL_DOCUMENTATION.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_SUBSCRIPTION_REACTIVATION_TECHNICAL_DOCUMENTATION.md) — Reactivation
- [F12-Billing-Subscriptions-Payments_SUBSCRIPTION_SYSTEM_COMPLETE_DOCUMENTATION.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_SUBSCRIPTION_SYSTEM_COMPLETE_DOCUMENTATION.md) — Complete system doc
- [F12-Billing-Subscriptions-Payments_TENANCY_BILLING_SYSTEM.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_TENANCY_BILLING_SYSTEM.md) — Billing system
- [F12-Billing-Subscriptions-Payments_TENANCY_LIFECYCLE_TESTING.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_TENANCY_LIFECYCLE_TESTING.md) — Lifecycle tests
- [F12-Billing-Subscriptions-Payments_subscription_plans.md](F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_subscription_plans.md) — Subscription plans

---

### F13: Platform & Multi-Tenancy

**Core multi-tenancy architecture and tenant isolation.**

Foundational multi-tenant infrastructure ensuring complete data isolation between customers. Implements tenant-scoped database access, domain routing, and resource isolation. Features tenant lifecycle management (provisioning, customization, termination), attribute configuration, and tenant switching for staff. Ensures security and compliance through architectural isolation patterns.

**Documents:**
- [F13-Platform-Multi-Tenancy_MULTI_TENANT_ASSOCIATION_APPLIED.md](F13-Platform-Multi-Tenancy/F13-Platform-Multi-Tenancy_MULTI_TENANT_ASSOCIATION_APPLIED.md) — Multi-tenant associations
- [F13-Platform-Multi-Tenancy_PROVISIONING_SOLUTION.md](F13-Platform-Multi-Tenancy/F13-Platform-Multi-Tenancy_PROVISIONING_SOLUTION.md) — Provisioning solution
- [F13-Platform-Multi-Tenancy_SYSTEM_MULTI_TENANCY_POLICY.md](F13-Platform-Multi-Tenancy/F13-Platform-Multi-Tenancy_SYSTEM_MULTI_TENANCY_POLICY.md) — Multi-tenancy policy
- [F13-Platform-Multi-Tenancy_TENANT_ATTRIBUTES_REFACTORING.md](F13-Platform-Multi-Tenancy/F13-Platform-Multi-Tenancy_TENANT_ATTRIBUTES_REFACTORING.md) — Attributes refactoring
- [F13-Platform-Multi-Tenancy_TENANT_INITIAL_PROVISION.md](F13-Platform-Multi-Tenancy/F13-Platform-Multi-Tenancy_TENANT_INITIAL_PROVISION.md) — Initial provisioning
- [F13-Platform-Multi-Tenancy_TENANT_SWITCHING_FEATURE.md](F13-Platform-Multi-Tenancy/F13-Platform-Multi-Tenancy_TENANT_SWITCHING_FEATURE.md) — Tenant switching
- [F13-Platform-Multi-Tenancy_TenancyFeature.md](F13-Platform-Multi-Tenancy/F13-Platform-Multi-Tenancy_TenancyFeature.md) — Tenancy feature overview
- [F13-Platform-Multi-Tenancy_tenancy-account-feature.md](F13-Platform-Multi-Tenancy/F13-Platform-Multi-Tenancy_tenancy-account-feature.md) — Account feature

---

### F14: Auth & Access Control

**Role-based permissions and granular access control.**

Comprehensive permission system with role-based access control (RBAC) at API and UI levels. Implements role hierarchies, permission inheritance, and bulk permission management. Features permission selectors for fine-grained access definition, JWT/Sanctum token authentication, and refresh token management. Includes permission testing framework and audit logging of permission changes.

**Documents:**
- [F14-Auth-Access-Control_BULK_PERMISSION_MANAGER.md](F14-Auth-Access-Control/F14-Auth-Access-Control_BULK_PERMISSION_MANAGER.md) — Bulk manager
- [F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_ARCHITECTURE.md](F14-Auth-Access-Control/F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_ARCHITECTURE.md) — Architecture
- [F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_CRUD_FIX.md](F14-Auth-Access-Control/F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_CRUD_FIX.md) — CRUD fix
- [F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_REACTADMIN_REFACTOR.md](F14-Auth-Access-Control/F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_REACTADMIN_REFACTOR.md) — React-Admin refactor
- [F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_ROUTE_FIX.md](F14-Auth-Access-Control/F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_ROUTE_FIX.md) — Route fix
- [F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_SETUP.md](F14-Auth-Access-Control/F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_SETUP.md) — Setup
- [F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_SUMMARY.md](F14-Auth-Access-Control/F14-Auth-Access-Control_BULK_PERMISSION_MANAGER_SUMMARY.md) — Summary
- [F14-Auth-Access-Control_COMPLETE_PERMISSION_SYSTEM.md](F14-Auth-Access-Control/F14-Auth-Access-Control_COMPLETE_PERMISSION_SYSTEM.md) — Complete permission system
- [F14-Auth-Access-Control_PERMISSION_FRONTEND_BACKEND_FIX.md](F14-Auth-Access-Control/F14-Auth-Access-Control_PERMISSION_FRONTEND_BACKEND_FIX.md) — Frontend/backend fix
- [F14-Auth-Access-Control_PERMISSION_SELECTOR_DATAGRID.md](F14-Auth-Access-Control/F14-Auth-Access-Control_PERMISSION_SELECTOR_DATAGRID.md) — Permission selector
- [F14-Auth-Access-Control_PERMISSION_SELECTOR_DATAGRID_SUMMARY.md](F14-Auth-Access-Control/F14-Auth-Access-Control_PERMISSION_SELECTOR_DATAGRID_SUMMARY.md) — Summary
- [F14-Auth-Access-Control_PERMISSION_SELECTOR_LIST_SOLUTION.md](F14-Auth-Access-Control/F14-Auth-Access-Control_PERMISSION_SELECTOR_LIST_SOLUTION.md) — List solution
- [F14-Auth-Access-Control_REFRESH_TOKEN_IMPLEMENTATION.md](F14-Auth-Access-Control/F14-Auth-Access-Control_REFRESH_TOKEN_IMPLEMENTATION.md) — Token refresh
- [F14-Auth-Access-Control_ROLE_PERMISSION_IMPLEMENTATION.md](F14-Auth-Access-Control/F14-Auth-Access-Control_ROLE_PERMISSION_IMPLEMENTATION.md) — Implementation
- [F14-Auth-Access-Control_ROLE_PERMISSION_QUICK_REFERENCE.md](F14-Auth-Access-Control/F14-Auth-Access-Control_ROLE_PERMISSION_QUICK_REFERENCE.md) — Quick reference
- [F14-Auth-Access-Control_ROLE_PERMISSION_SYSTEM.md](F14-Auth-Access-Control/F14-Auth-Access-Control_ROLE_PERMISSION_SYSTEM.md) — System documentation
- [F14-Auth-Access-Control_ROLE_PERMISSION_SYSTEM_FINAL.md](F14-Auth-Access-Control/F14-Auth-Access-Control_ROLE_PERMISSION_SYSTEM_FINAL.md) — Final role/permission system
- [F14-Auth-Access-Control_ROLE_PERMISSION_VISUAL_GUIDE.md](F14-Auth-Access-Control/F14-Auth-Access-Control_ROLE_PERMISSION_VISUAL_GUIDE.md) — Visual guide
- [F14-Auth-Access-Control_dash-role-permission-overview.md](F14-Auth-Access-Control/F14-Auth-Access-Control_dash-role-permission-overview.md) — Overview
- [F14-Auth-Access-Control_permission-tests.md](F14-Auth-Access-Control/F14-Auth-Access-Control_permission-tests.md) — Permission tests
- [F14-Auth-Access-Control_role-permission-tests.md](F14-Auth-Access-Control/F14-Auth-Access-Control_role-permission-tests.md) — Role-permission tests
- [F14-Auth-Access-Control_role-tests.md](F14-Auth-Access-Control/F14-Auth-Access-Control_role-tests.md) — Role tests
- [F14-Auth-Access-Control_rolePermissions-README.md](F14-Auth-Access-Control/F14-Auth-Access-Control_rolePermissions-README.md) — README

---

### F15: Notifications & Messaging

**Multi-channel notification delivery system.**

Integrated notification platform supporting email, SMS, push notifications, and in-app messages. Features notification catalogs, template management, and delivery scheduling. Includes email preference management, unsubscribe functionality, bounce handling, and complaint tracking via AWS SES. Supports notification personalization and user notification preferences.

**Documents:**
- [F15-Notifications-Messaging_AWS_SES_BOUNCE_COMPLAINT_IMPLEMENTATION.md](F15-Notifications-Messaging/F15-Notifications-Messaging_AWS_SES_BOUNCE_COMPLAINT_IMPLEMENTATION.md) — Bounce/complaint handling
- [F15-Notifications-Messaging_AWS_SES_EMAIL_PRACTICES_KITCHNTABS.md](F15-Notifications-Messaging/F15-Notifications-Messaging_AWS_SES_EMAIL_PRACTICES_KITCHNTABS.md) — SES best practices
- [F15-Notifications-Messaging_AWS_SES_EMAIL_PRACTICES_KITCHNTABS_SIMPLE.md](F15-Notifications-Messaging/F15-Notifications-Messaging_AWS_SES_EMAIL_PRACTICES_KITCHNTABS_SIMPLE.md) — SES practices (simplified)
- [F15-Notifications-Messaging_BACKEND_TRANSLATIONS.md](F15-Notifications-Messaging/F15-Notifications-Messaging_BACKEND_TRANSLATIONS.md) — Email translations
- [F15-Notifications-Messaging_DASH_EMAIL_NOTIFICATION_SYSTEM.md](F15-Notifications-Messaging/F15-Notifications-Messaging_DASH_EMAIL_NOTIFICATION_SYSTEM.md) — Email system
- [F15-Notifications-Messaging_DASH_NOTIFICATIONS_CATALOG.md](F15-Notifications-Messaging/F15-Notifications-Messaging_DASH_NOTIFICATIONS_CATALOG.md) — Notifications catalog
- [F15-Notifications-Messaging_DEPLOY_SES_BOUNCE_HANDLING.md](F15-Notifications-Messaging/F15-Notifications-Messaging_DEPLOY_SES_BOUNCE_HANDLING.md) — Deployment guide
- [F15-Notifications-Messaging_EMAIL_SYSTEM_TESTS.md](F15-Notifications-Messaging/F15-Notifications-Messaging_EMAIL_SYSTEM_TESTS.md) — Email tests
- [F15-Notifications-Messaging_EMAIL_UNSUBSCRIBE_DEPLOYMENT_CHECKLIST.md](F15-Notifications-Messaging/F15-Notifications-Messaging_EMAIL_UNSUBSCRIBE_DEPLOYMENT_CHECKLIST.md) — Deployment checklist
- [F15-Notifications-Messaging_EMAIL_UNSUBSCRIBE_IMPLEMENTATION_SUMMARY.md](F15-Notifications-Messaging/F15-Notifications-Messaging_EMAIL_UNSUBSCRIBE_IMPLEMENTATION_SUMMARY.md) — Implementation summary
- [F15-Notifications-Messaging_EMAIL_UNSUBSCRIBE_SYSTEM.md](F15-Notifications-Messaging/F15-Notifications-Messaging_EMAIL_UNSUBSCRIBE_SYSTEM.md) — Unsubscribe system
- [F15-Notifications-Messaging_NOTIFICATIONS.md](F15-Notifications-Messaging/F15-Notifications-Messaging_NOTIFICATIONS.md) — Notifications overview
- [F15-Notifications-Messaging_NOTIFICATION_SYSTEM_DOCUMENTATION.md](F15-Notifications-Messaging/F15-Notifications-Messaging_NOTIFICATION_SYSTEM_DOCUMENTATION.md) — System documentation
- [F15-Notifications-Messaging_PRIVATE_NOTIFICATION.md](F15-Notifications-Messaging/F15-Notifications-Messaging_PRIVATE_NOTIFICATION.md) — Private notifications
- [F15-Notifications-Messaging_SES_BOUNCE_HANDLING_CHECKLIST.md](F15-Notifications-Messaging/F15-Notifications-Messaging_SES_BOUNCE_HANDLING_CHECKLIST.md) — Handling checklist
- [F15-Notifications-Messaging_WS_MESSAGING.md](F15-Notifications-Messaging/F15-Notifications-Messaging_WS_MESSAGING.md) — WebSocket messaging

---

### F16: AI Agents

**Artificial intelligence and machine learning capabilities.**

AI-powered features including intelligent recommendations, predictive analytics, and automated decision-making. Includes chatbot integration, natural language processing, and machine learning model management. Features training pipelines, model deployment, and performance monitoring. Enables intelligent automation of business processes and customer interactions.

**Documents:**
- [F16-AI-Agents_AI_AGENTS_DOCUMENTATION.md](F16-AI-Agents/F16-AI-Agents_AI_AGENTS_DOCUMENTATION.md) — Full AI agents documentation

---

### F17: Inventory

**Inventory management and stock tracking system.**

Comprehensive inventory management with real-time stock tracking across locations. Features inventory adjustments, stock reconciliation, low stock alerts, and reorder automation. Includes inventory forecasting, supplier management, and cost tracking. Supports batch/lot tracking and expiration date management for perishable items.

**Documents:**
*(No documents yet; ready for inventory module documentation)*

---

### F18: Campaigns

**Marketing campaigns and promotional management.**

Campaign creation and management platform for promotions, discounts, and marketing initiatives. Features campaign scheduling, audience targeting, and performance tracking. Includes A/B testing capabilities, coupon management, and integration with sales channels. Supports multi-channel campaign execution and ROI tracking.

**Documents:**
- [F18-Campaigns_CAMPAIGN_MANAGER_TECHNICAL_DOCUMENTATION.md](F18-Campaigns/F18-Campaigns_CAMPAIGN_MANAGER_TECHNICAL_DOCUMENTATION.md) — Campaign manager
- [F18-Campaigns_CAMPAIGN_PUBLISHING_FLOW.md](F18-Campaigns/F18-Campaigns_CAMPAIGN_PUBLISHING_FLOW.md) — Publishing flow
- [F18-Campaigns_CampaignPublishingSystemTD.md](F18-Campaigns/F18-Campaigns_CampaignPublishingSystemTD.md) — Publishing system
- [F18-Campaigns_Cloudwatch.success.uber-campaign.publishing.md](F18-Campaigns/F18-Campaigns_Cloudwatch.success.uber-campaign.publishing.md) — Uber campaign example
- [F18-Campaigns_campaign-management-manual.md](F18-Campaigns/F18-Campaigns_campaign-management-manual.md) — Manual

---

### F19: Internationalization

**Multi-language and localization support.**

Full internationalization infrastructure supporting multiple languages and regional customization. Includes translation management, currency formatting, regional date/time formats, and locale-specific content. Features translation validation and community translation support. Enables deployment to global markets with appropriate localization.

**Documents:**
- [F19-Internationalization_BACKEND_TRANSLATIONS.md](F19-Internationalization/F19-Internationalization_BACKEND_TRANSLATIONS.md) — Backend translations
- [F19-Internationalization_DASH_I18N_TECHNICAL_DOCUMENTATION.md](F19-Internationalization/F19-Internationalization_DASH_I18N_TECHNICAL_DOCUMENTATION.md) — Technical documentation
- [F19-Internationalization_I18N_INTEGRATION_GUIDE.md](F19-Internationalization/F19-Internationalization_I18N_INTEGRATION_GUIDE.md) — Integration guide
- [F19-Internationalization_TRANSLATION_GUIDE.md](F19-Internationalization/F19-Internationalization_TRANSLATION_GUIDE.md) — Translation guide
- [F19-Internationalization_TRANSLATION_VALIDATION.md](F19-Internationalization/F19-Internationalization_TRANSLATION_VALIDATION.md) — Validation

---

### F20: Media & Images

**Image management and media handling.**

Centralized media management system for product images, gallery management, and asset organization. Features image optimization, CDN delivery, and lazy loading. Includes image ordering, tagging, and search. Supports bulk uploads, image processing (resizing, cropping), and version control.

**Documents:**
- [F20-Media-Images_ADDING_IMAGE_TO_MODEL.md](F20-Media-Images/F20-Media-Images_ADDING_IMAGE_TO_MODEL.md) — Add image (simplified)
- [F20-Media-Images_GALLERY_IMAGE_ORDERING.md](F20-Media-Images/F20-Media-Images_GALLERY_IMAGE_ORDERING.md) — Gallery image ordering
- [F20-Media-Images_how-to-add-image-resource-to-model.md](F20-Media-Images/F20-Media-Images_how-to-add-image-resource-to-model.md) — Add image resource

---

### F21: Tenancy Management

**Tenant lifecycle and account management.**

Complete tenant account management from signup through termination. Features tenant provisioning, configuration management, billing setup, and account termination workflows. Includes account status tracking, settings management, and support ticket integration. Handles tenant customization and whitelabel configuration.

**Documents:**
- [F21-Tenancy-Management_StoreScheduleFeature.md](F21-Tenancy-Management/F21-Tenancy-Management_StoreScheduleFeature.md) — Store schedule feature
- [F21-Tenancy-Management_TENANT_SETTINGS_MODULE.md](F21-Tenancy-Management/F21-Tenancy-Management_TENANT_SETTINGS_MODULE.md) — Tenant settings module

---

### F22: MiddlewareService

**Service middleware and cross-cutting concerns.**

Core middleware services handling authentication, authorization, logging, and request/response transformation. Implements rate limiting, request validation, error handling, and security headers. Features request correlation tracking and performance monitoring. Provides foundation for all API services.

**Documents:**
*(No documents yet; ready for middleware documentation)*

---

### F23: DeliveryModule

**Delivery logistics and fulfillment management.**

End-to-end delivery management including order routing, driver assignment, and real-time tracking. Features delivery scheduling, route optimization, driver management, and customer notifications. Includes delivery performance analytics and proof of delivery. Supports multiple delivery partner integrations.

**Documents:**
- [F23-DeliveryModule_StoreScheduleFeature.md](F23-DeliveryModule/F23-DeliveryModule_StoreScheduleFeature.md) — Store schedule/delivery feature

---

### F24: InventoryModule

**Advanced inventory management and optimization.**

Enterprise-grade inventory system with advanced forecasting, optimization, and multi-location management. Features intelligent stock allocation, reorder automation, and supply chain optimization. Includes inventory analytics, cost tracking, and valuation methods. Supports complex fulfillment scenarios and multi-warehouse operations.

**Documents:**
*(No documents yet; ready for advanced inventory documentation)*

---

### F25: CashcountModule

**Cash handling and reconciliation system.**

Cash management system for tracking cash transactions, drawer operations, and reconciliation. Features cash counting workflows, discrepancy detection, and audit trails. Includes shift reconciliation, cash transfer management, and security protocols. Supports multi-currency handling and regional compliance requirements.

**Documents:**
*(No documents yet; ready for cashcount documentation)*

---

## Non-Functional Epics (N1–N10)

### N1: Backend Framework

**Core Laravel infrastructure and domain-driven design architecture.**

Foundation of the backend built on Laravel framework implementing domain-driven design principles. Provides core/domain layer separation, service layer patterns, and trait-based functionality. Features Eloquent ORM integration, event-driven architecture, and comprehensive testing infrastructure. Establishes conventions for model relationships, scoping, and business logic organization.

**Documents:**
- [N1-Backend-Framework_ADDING_ATTRIBUTE_TO_MODEL.md](N1-Backend-Framework/N1-Backend-Framework_ADDING_ATTRIBUTE_TO_MODEL.md) — Model attributes
- [N1-Backend-Framework_AGENT.md](N1-Backend-Framework/N1-Backend-Framework_AGENT.md) — Agent pattern
- [N1-Backend-Framework_AGENT_DEFAULT.md](N1-Backend-Framework/N1-Backend-Framework_AGENT_DEFAULT.md) — Default agent
- [N1-Backend-Framework_ARCHITECTURE.md](N1-Backend-Framework/N1-Backend-Framework_ARCHITECTURE.md) — Full architecture
- [N1-Backend-Framework_IMPLEMENTATION_SUMMARY.md](N1-Backend-Framework/N1-Backend-Framework_IMPLEMENTATION_SUMMARY.md) — Implementation summary
- [N1-Backend-Framework_SETTINGS_ATTRIBUTES_VALIDATION_FIX.md](N1-Backend-Framework/N1-Backend-Framework_SETTINGS_ATTRIBUTES_VALIDATION_FIX.md) — Attributes validation
- [N1-Backend-Framework_AGENT.md](N1-Backend-Framework/N1-Backend-Framework_AGENT.md) — Agent overview

---

### N2: Frontend Framework

**React-based component system and administrative UI framework.**

Frontend technology stack built on React and React-Admin. Provides reusable component library, state management patterns, and form handling. Features responsive design system with CSS-in-JS/LESS, theme support, and accessibility compliance. Includes component registry, design tokens, and development utilities.

**Documents:**
- [N2-Frontend-Framework_COMPONENT_REGISTRY.md](N2-Frontend-Framework/N2-Frontend-Framework_COMPONENT_REGISTRY.md) — Component registry

---

### N3: Infrastructure & CI/CD

**Deployment infrastructure and continuous integration/deployment.**

Cloud infrastructure management using AWS/CDK for IaC. Implements automated CI/CD pipelines, containerization strategies, and deployment automation. Features environment management (dev, staging, production), configuration management, and infrastructure provisioning. Includes monitoring, logging, and incident response capabilities.

**Documents:**
- [N3-Infrastructure-CICD_CI.md](N3-Infrastructure-CICD/N3-Infrastructure-CICD_CI.md) — CI pipeline
- [N3-Infrastructure-CICD_CONFIG.md](N3-Infrastructure-CICD/N3-Infrastructure-CICD_CONFIG.md) — Configuration
- [N3-Infrastructure-CICD_DELIVERY_GUIDE.md](N3-Infrastructure-CICD/N3-Infrastructure-CICD_DELIVERY_GUIDE.md) — Delivery guide
- [N3-Infrastructure-CICD_HTTP2.md](N3-Infrastructure-CICD/N3-Infrastructure-CICD_HTTP2.md) — HTTP/2 configuration
- [N3-Infrastructure-CICD_KITCHNTABS-FRONTEND-CI-TECHNICAL-DOC.md](N3-Infrastructure-CICD/N3-Infrastructure-CICD_KITCHNTABS-FRONTEND-CI-TECHNICAL-DOC.md) — Frontend CI
- [N3-Infrastructure-CICD_LIGHTSAIL.md](N3-Infrastructure-CICD/N3-Infrastructure-CICD_LIGHTSAIL.md) — Lightsail deployment
- [N3-Infrastructure-CICD_LOCAL.md](N3-Infrastructure-CICD/N3-Infrastructure-CICD_LOCAL.md) — Local setup
- [N3-Infrastructure-CICD_README.AWS.md](N3-Infrastructure-CICD/N3-Infrastructure-CICD_README.AWS.md) — AWS setup

---

### N4: Build Toolchain

**Build processes and application compilation systems.**

Build automation for backend, frontend, and desktop applications. Features webpack configuration, Electron app building, multi-architecture support, and code optimization. Includes scaffolding tools, development server setup, and production build optimization. Manages dependencies and version management across projects.

**Documents:**
- [N4-Build-Toolchain_ELECTRON_BUILD_AND_CONFIG_SYSTEM.md](N4-Build-Toolchain/N4-Build-Toolchain_ELECTRON_BUILD_AND_CONFIG_SYSTEM.md) — Build & config
- [N4-Build-Toolchain_ELECTRON_BUILD_PROCESS.md](N4-Build-Toolchain/N4-Build-Toolchain_ELECTRON_BUILD_PROCESS.md) — Build process
- [N4-Build-Toolchain_ELECTRON_PYTHON_SERVICE_BUILD_SYSTEM.md](N4-Build-Toolchain/N4-Build-Toolchain_ELECTRON_PYTHON_SERVICE_BUILD_SYSTEM.md) — Electron+Python build
- [N4-Build-Toolchain_MIGRATION_YARN_PNPM.md](N4-Build-Toolchain/N4-Build-Toolchain_MIGRATION_YARN_PNPM.md) — Yarn/PNPM migration
- [N4-Build-Toolchain_MULTI_ARCHITECTURE_BUILD_SYSTEM.md](N4-Build-Toolchain/N4-Build-Toolchain_MULTI_ARCHITECTURE_BUILD_SYSTEM.md) — Multi-architecture
- [N4-Build-Toolchain_PRODUCTION_BUILD_TECHNICAL_DOCUMENTATION.md](N4-Build-Toolchain/N4-Build-Toolchain_PRODUCTION_BUILD_TECHNICAL_DOCUMENTATION.md) — Production build
- [N4-Build-Toolchain_README.md](N4-Build-Toolchain/N4-Build-Toolchain_README.md) — Toolchain README
- [N4-Build-Toolchain_SCAFFOLDING.md](N4-Build-Toolchain/N4-Build-Toolchain_SCAFFOLDING.md) — Project scaffolding

---

### N5: Desktop & Device Service

**Electron-based desktop application and Python service integration.**

Cross-platform Electron application for desktop usage with integrated Python services. Features IPC communication between Electron and Python layers, native system integration, and auto-update mechanisms. Includes device hardware integration (printers, displays, sensors) and offline functionality. Supports Linux, macOS, and Windows platforms.

**Documents:**
- [N5-Desktop-Device-Service_BUILD_DEBIAN_AMD64_WSL.md](N5-Desktop-Device-Service/N5-Desktop-Device-Service_BUILD_DEBIAN_AMD64_WSL.md) — Build for WSL
- [N5-Desktop-Device-Service_RASPBERRY_PI_SETUP.md](N5-Desktop-Device-Service/N5-Desktop-Device-Service_RASPBERRY_PI_SETUP.md) — Raspberry Pi setup
- [N5-Desktop-Device-Service_REDIS_PREDIS_CHAT.md](N5-Desktop-Device-Service/N5-Desktop-Device-Service_REDIS_PREDIS_CHAT.md) — Redis chat
- [N5-Desktop-Device-Service_dev-notes.md](N5-Desktop-Device-Service/N5-Desktop-Device-Service_dev-notes.md) — Dev notes
- [N5-Desktop-Device-Service_websocket-system.md](N5-Desktop-Device-Service/N5-Desktop-Device-Service_websocket-system.md) — WebSocket system

---

### N6: Caching & Performance

**Performance optimization and caching strategies.**

Comprehensive caching layer using Redis for performance optimization. Implements query result caching, session management, and real-time data synchronization. Features cache invalidation strategies, TTL management, and cache warming. Includes performance monitoring and optimization recommendations.

**Documents:**
- [N6-Caching-Performance_MALL_PRODUCTS_CACHE.md](N6-Caching-Performance/N6-Caching-Performance_MALL_PRODUCTS_CACHE.md) — Products cache
- [N6-Caching-Performance_MALL_REACT_QUERY_CACHING_SYSTEM.md](N6-Caching-Performance/N6-Caching-Performance_MALL_REACT_QUERY_CACHING_SYSTEM.md) — React Query caching

---

### N7: Security

**Security practices and threat protection.**

Security framework encompassing authentication, encryption, and threat prevention. Implements HTTPS/TLS configuration, API security, data encryption, and security headers. Features vulnerability scanning, dependency management, and security audit logging. Includes compliance standards implementation (GDPR, PCI-DSS, SOC 2).

**Documents:**
*(No documents yet; refer to REQUIREMENTS.md §23 Security)*

---

### N8: Observability

**Logging, monitoring, and operational visibility.**

Comprehensive observability platform with centralized logging, metrics collection, and tracing. Integrates CloudWatch, application performance monitoring, and real-time dashboards. Features alerting, anomaly detection, and performance analytics. Enables proactive issue detection and root cause analysis.

**Documents:**
- [N8-Observability_Cloudwatch.success.uber-campaign.publishing.md](N8-Observability/N8-Observability_Cloudwatch.success.uber-campaign.publishing.md) — CloudWatch example

---

### N9: App Publishing

**Mobile and desktop application distribution.**

Application packaging and distribution to app stores (iOS, Android, Windows Store). Features automated signing, versioning, release management, and update distribution. Includes beta testing programs, crash reporting, and analytics integration. Manages app store optimization and release notes.

**Documents:**
*(No documents yet; ready for app publishing documentation)*

---

### N10: Administrative & Legal

**Settings, utilities, and compliance documentation.**

Administrative utilities and system configuration. Includes tenant settings management, user preferences, and system utilities. Features configuration management, data backup, and export functionality. Maintains compliance documentation and legal requirements tracking.

**Documents:**
- [N10-Administrative-Legal_FRONTEND_ATTRIBUTES_FIELD_FIX.md](N10-Administrative-Legal/N10-Administrative-Legal_FRONTEND_ATTRIBUTES_FIELD_FIX.md) — Frontend attributes fix
- [N10-Administrative-Legal_FRONTEND_TENANT_ATTRIBUTES_REFACTORING.md](N10-Administrative-Legal/N10-Administrative-Legal_FRONTEND_TENANT_ATTRIBUTES_REFACTORING.md) — Frontend refactoring
- [N10-Administrative-Legal_JUMPSELLER_INTEGRATION.md](N10-Administrative-Legal/N10-Administrative-Legal_JUMPSELLER_INTEGRATION.md) — Jumpseller integration
- [N10-Administrative-Legal_JUMPSELLER_WEBHOOKS.md](N10-Administrative-Legal/N10-Administrative-Legal_JUMPSELLER_WEBHOOKS.md) — Jumpseller webhooks
- [N10-Administrative-Legal_PLANS_PAGE_FIXES.md](N10-Administrative-Legal/N10-Administrative-Legal_PLANS_PAGE_FIXES.md) — Plans page fixes
- [N10-Administrative-Legal_SELFSERVICE_JUMPSELLER_CHECKOUT_IMPLEMENTATION.md](N10-Administrative-Legal/N10-Administrative-Legal_SELFSERVICE_JUMPSELLER_CHECKOUT_IMPLEMENTATION.md) — Jumpseller checkout
- [N10-Administrative-Legal_TENANT_SETTINGS_MODULE.md](N10-Administrative-Legal/N10-Administrative-Legal_TENANT_SETTINGS_MODULE.md) — Tenant settings
- [N10-Administrative-Legal_TYPESCRIPT_INTERFACE_GENERATION.md](N10-Administrative-Legal/N10-Administrative-Legal_TYPESCRIPT_INTERFACE_GENERATION.md) — TypeScript generation
- [N10-Administrative-Legal_USER_PREFERENCES_SYSTEM.md](N10-Administrative-Legal/N10-Administrative-Legal_USER_PREFERENCES_SYSTEM.md) — User preferences

---

## Document Statistics

| Category | Epic Count | Document Count |
|---|---|---|
| **Functional** | 25 | ~170 files |
| **Non-Functional** | 10 | ~25 files |
| **Archive** | — | 4 files |
| **General Utilities** | — | — |
| **Total** | **35** | **195+** |

---

## How to Use This Index

1. **Find your epic** — Use the Table of Contents to jump to your epic
2. **Review documents** — Each epic lists all related technical documents
3. **Access documentation** — Click on document links to read the full content
4. **Understand scope** — Epic descriptions explain responsibilities and boundaries

---

**Last Updated:** 2026-06-26  
**Format:** Markdown with linked table of contents and document references  
**Accessibility:** Organized for team onboarding and knowledge discovery
