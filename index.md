---
title: KitchnTabs Documentation
layout: default
---

<div class="hero-section">
  <img src="/assets/kitchntabs-h.png" alt="KitchnTabs Logo" class="hero-logo">
  <h1>KitchnTabs Documentation</h1>
  <p class="hero-subtitle">Comprehensive Restaurant & Food Court Management Platform</p>
</div>

## Welcome

KitchnTabs is a full-stack solution that combines specialized components for restaurant and food court management, built with Laravel and React for enterprise-grade performance and scalability.

### Platform Components

- **Dash Backend** — Laravel-based REST API with multi-tenant architecture
- **Dash Admin** — React-Admin dashboard for restaurant management
- **Mall App** — QR code-based ordering system for food courts
- **Customer App** — Mobile-first ordering experience
- **Staff App** — Real-time order management for restaurant staff

---

## 📚 Documentation Index

### 🏢 Mall Application
Complete documentation for the food court ordering system.

- [Overview & Architecture](docs/mall-app/01-OVERVIEW.html)
- [System Architecture](docs/mall-app/02-ARCHITECTURE.html)
- [Backend Models](docs/mall-app/03-BACKEND-MODELS.html)
- [Backend Controllers](docs/mall-app/04-BACKEND-CONTROLLERS.html)
- [Backend Services](docs/mall-app/05-BACKEND-SERVICES.html)
- [Notification System](docs/mall-app/06-NOTIFICATIONS.html)
- [Frontend Architecture](docs/mall-app/07-FRONTEND-ARCHITECTURE.html)
- [Frontend Components](docs/mall-app/08-FRONTEND-COMPONENTS.html)
- [User Stories & Workflows](docs/mall-app/09-USER-STORIES.html)
- [Flow Diagrams](docs/mall-app/10-FLOW-DIAGRAMS.html)

### 📱 Customer Application
Mobile ordering experience documentation.

- [Complete Customer App Flow](docs/customer-app/CUSTOMER_APP_COMPLETE_FLOW.html)
- [Mall Session Notifications](docs/customer-app/MALL_SESSION_NOTIFICATIONS_FLOW.html)
- [Order Update Flow](docs/customer-app/MALL_SESSION_ORDER_UPDATE_FLOW.html)

### 👨‍🍳 Staff Application
Real-time order management for restaurant staff.

- [Complete Staff App Flow](docs/staff-app/STAFF_APP_COMPLETE_FLOW.html)
- [Staff Notifications Flow](docs/staff-app/STAFF_APP_NOTIFICATIONS_FLOW.html)

### 🔐 Access Control & Security
Role-based permission system documentation.

- [Role & Permission Overview](docs/tech/features/acl/dash-role-permission-overview.html)
- [Permission Tests](docs/tech/features/acl/permission-tests.html)
- [Role Permission Tests](docs/tech/features/acl/role-permission-tests.html)
- [Role Tests](docs/tech/features/acl/role-tests.html)

#### Bulk Permission Manager
- [Architecture](docs/tech/features/acl/bulk-permission-manager/BULK_PERMISSION_MANAGER_ARCHITECTURE.html)
- [Setup Guide](docs/tech/features/acl/bulk-permission-manager/BULK_PERMISSION_MANAGER_SETUP.html)
- [Summary](docs/tech/features/acl/bulk-permission-manager/BULK_PERMISSION_MANAGER_SUMMARY.html)

### 🔔 Notification System
Real-time and push notification documentation.

- [Email Notification System](docs/tech/features/notifications/DASH_EMAIL_NOTIFICATION_SYSTEM.html)
- [Notifications Catalog](docs/tech/features/notifications/DASH_NOTIFICATIONS_CATALOG.html)
- [System Documentation](docs/tech/features/notifications/NOTIFICATION_SYSTEM_DOCUMENTATION.html)

### 🛒 Marketplace Integrations
Third-party platform integration guides.

#### Jumpseller
- [Webhook Integration](docs/tech/features/marketplaces/jumpseller/JUMPSELLER_WEBHOOKS.html)
- [Unsubscribe Implementation](docs/tech/features/marketplaces/jumpseller/JUMPSELLER_UNSUBSCRIBE_IMPLEMENTATION.html)

#### Uber Eats
- [Integration Guide](docs/tech/features/marketplaces/ubereats/UBER_INTEGRATION.html)

### 🏗️ System Architecture
Technical architecture and design patterns.

- [System Architecture Overview](docs/tech/architecture/ARCHITECTURE.html)
- [Tabs & Mall Tabs Architecture](docs/tech/features/tabs/TABS_MALLTABS_ARCHITECTURE.html)

### ⚙️ Build & Deployment
Production build system and toolchain documentation.

- [Production Build Documentation](docs/tech/toolchain/PRODUCTION_BUILD_TECHNICAL_DOCUMENTATION.html)
- [Electron Build Process](docs/tech/toolchain/ELECTRON_BUILD_PROCESS.html)
- [Electron Build & Config System](docs/tech/toolchain/ELECTRON_BUILD_AND_CONFIG_SYSTEM.html)
- [Multi-Architecture Build System](docs/tech/toolchain/MULTI_ARCHITECTURE_BUILD_SYSTEM.html)

### 🎨 Design System
UI/UX design guidelines and theme system.

- [Dash Design System](docs/tech/features/design/DASH_DESIGN_SYSTEM.html)

### 📦 Features

#### Product Management
- [Product Import System](docs/tech/features/products/PRODUCT_IMPORT_SYSTEM_DOCUMENTATION.html)

#### Campaign Management
- [Campaign Publishing System](docs/tech/features/campaigns/Campaign Publishing System - TD.html)
- [Campaign Manager](docs/tech/features/campaigns/CAMPAIGN_MANAGER_TECHNICAL_DOCUMENTATION.html)

#### Media Management
- [Image Resource Guide](docs/tech/features/images/how-to-add-image-resource-to-model.html)

#### Caching
- [React Query Caching System](docs/tech/features/cache/MALL_REACT_QUERY_CACHING_SYSTEM.html)

#### AI Integration
- [AI Agents Documentation](docs/tech/features/ai/AI_AGENTS_DOCUMENTATION.html)

---

## 🔒 Privacy & Legal

- [Privacy Policy (English)](privacy/en/)
- [Política de Privacidad (Español)](privacy/es/)

---

## 🚀 Quick Start

### API Endpoint
All API requests should be made to:
```
https://api.kitchntabs.com
```

### Authentication
KitchnTabs uses Laravel Sanctum for API authentication. Include your token in the Authorization header:
```
Authorization: Bearer {your-token}
```

---

## 💬 Support

For technical support or questions:
- **Documentation Issues**: Open an issue on GitHub
- **API Questions**: Contact your account manager
- **Emergency Support**: Contact support team

---

## 📖 Additional Resources

- **[Complete Sitemap](SITEMAP.html)** - Comprehensive list of all documentation
- **[Contributing Guide](CONTRIBUTING.html)** - How to contribute to documentation
- **[README](https://github.com/kitchntabs/kitchntabs.github.io)** - Repository information

---

<div class="footer-section">
  <p>© 2025 KitchnTabs. All rights reserved.</p>
  <p>Built with ❤️ for the restaurant industry</p>
  <p style="margin-top: 1rem; font-size: 0.9rem;">
    <a href="SITEMAP.html">Sitemap</a> • 
    <a href="CONTRIBUTING.html">Contributing</a> • 
    <a href="https://github.com/kitchntabs">GitHub</a>
  </p>
</div>

- **Order Management**: Real-time order processing and tracking
- **Multi-Tenant Architecture**: Support for multiple restaurants
- **Marketplace Integration**: Connect with platforms like Jumpseller and Uber Eats
- **QR Code Ordering**: Contactless ordering for food courts
- **Analytics & Reporting**: Business intelligence tools

## Support

- **Email**: support@kitchntabs.com
- **Documentation Issues**: [GitHub Issues](https://github.com/kitchntabs/kitchntabs.github.io/issues)
- **Website**: [kitchntabs.com](https://kitchntabs.com)

---

*Last updated: December 22, 2025*