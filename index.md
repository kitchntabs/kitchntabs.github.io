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

KitchnTabs is a full-stack solution for restaurant and food court management. Our documentation is organized by **Epic** to match our product roadmap in ClickUp.

---

## 📚 Documentation by Epic

### 🎯 Functional Epics (F1–F25)

**Product features and user-facing functionality**

#### [F1: Orders & Tabs](docs/F1-Orders-Tabs/)
Restaurant order management and tab lifecycle
- [Tab Domain Model](docs/F1-Orders-Tabs/F1-Orders-Tabs_Tab-README.md)
- [Order Processing](docs/F1-Orders-Tabs/F1-Orders-Tabs_Order-README.md)
- [Hash ID Security](docs/F1-Orders-Tabs/F1-Orders-Tabs_HASH_ID_IMPLEMENTATION.md)
- [Delivery System](docs/F1-Orders-Tabs/F1-Orders-Tabs_DELIVERY.md)
- [Tenant Lifecycle](docs/F1-Orders-Tabs/F1-Orders-Tabs_DELETE_TENANCY_ACCOUNT.md)
- [MallTabs Architecture](docs/F1-Orders-Tabs/F1-Orders-Tabs_TABS_MALLTABS_ARCHITECTURE.md)

#### [F2: Products & Catalog](docs/F2-Products-Catalog/)
Product information management with pricing and customization
- Browse all product documentation

#### [F3: Product Import / Export](docs/F3-Product-Import-Export/)
Bulk product data ingestion and export functionality
- Browse all import/export documentation

#### [F4: Mall / Food Court](docs/F4-Mall-Food-Court/)
Multi-store food court management and shared marketplace
- Browse all mall application documentation

#### [F5: Customer & Self-Service](docs/F5-Customer-Self-Service/)
Customer-facing application and self-service ordering
- Browse all customer app documentation

#### [F6: Tenant / Staff App](docs/F6-Tenant-Staff-App/)
Staff and vendor management with real-time order tracking
- Browse all staff app documentation

#### [F7: System Admin Application](docs/F7-System-Admin-Application/)
Administrative dashboard for platform management
- Browse all admin documentation

#### [F8: Public Web](docs/F8-Public-Web/)
Public-facing website and brand presence
- Browse all web documentation

#### [F9: Marketplaces](docs/F9-Marketplaces/)
Third-party marketplace integrations (Jumpseller, Uber Eats)
- Browse all marketplace documentation

#### [F10: Point of Sale](docs/F10-Point-of-Sale/)
Physical POS system integration
- Browse all POS documentation

#### [F11: Checkout Gateways](docs/F11-Checkout-Gateways/)
Payment processor integrations
- Browse all payment gateway documentation

#### [F12: Billing, Subscriptions & Payments](docs/F12-Billing-Subscriptions-Payments/)
Subscription management, invoicing, and revenue operations
- Browse all billing documentation

#### [F13: Platform & Multi-Tenancy](docs/F13-Platform-Multi-Tenancy/)
Core multi-tenancy architecture and tenant isolation
- Browse all multi-tenancy documentation

#### [F14: Auth & Access Control](docs/F14-Auth-Access-Control/)
Role-based permissions and granular access control
- Browse all access control documentation

#### [F15: Notifications & Messaging](docs/F15-Notifications-Messaging/)
Multi-channel notification delivery system
- Browse all notification documentation

#### [F16: AI Agents](docs/F16-AI-Agents/)
Artificial intelligence and machine learning capabilities
- Browse all AI documentation

#### [F17: Inventory](docs/F17-Inventory/)
Inventory management and stock tracking system
- Browse all inventory documentation

#### [F18: Campaigns](docs/F18-Campaigns/)
Marketing campaigns and promotional management
- Browse all campaign documentation

#### [F19: Internationalization](docs/F19-Internationalization/)
Multi-language and localization support
- Browse all i18n documentation

#### [F20: Media & Images](docs/F20-Media-Images/)
Image management and media handling
- Browse all media documentation

#### [F21: Tenancy Management](docs/F21-Tenancy-Management/)
Tenant lifecycle and account management
- Browse all tenancy management documentation

#### [F22: MiddlewareService](docs/F22-MiddlewareService/)
Service middleware and cross-cutting concerns
- Browse all middleware documentation

#### [F23: DeliveryModule](docs/F23-DeliveryModule/)
Delivery logistics and fulfillment management
- Browse all delivery documentation

#### [F24: InventoryModule](docs/F24-InventoryModule/)
Advanced inventory management and optimization
- Browse all inventory module documentation

#### [F25: CashcountModule](docs/F25-CashcountModule/)
Cash handling and reconciliation system
- Browse all cashcount documentation

---

### 🏗️ Non-Functional Epics (N1–N10)

**Technical infrastructure and system architecture**

#### [N1: Backend Framework](docs/N1-Backend-Framework/)
Core Laravel infrastructure and domain-driven design
- [Full Architecture](docs/N1-Backend-Framework/N1-Backend-Framework_ARCHITECTURE.md)
- [Implementation Summary](docs/N1-Backend-Framework/N1-Backend-Framework_IMPLEMENTATION_SUMMARY.md)
- Browse all backend documentation

#### [N2: Frontend Framework](docs/N2-Frontend-Framework/)
React-based component system and admin UI
- Browse all frontend documentation

#### [N3: Infrastructure & CI/CD](docs/N3-Infrastructure-CICD/)
Deployment infrastructure and continuous integration
- Browse all infrastructure documentation

#### [N4: Build Toolchain](docs/N4-Build-Toolchain/)
Build processes and application compilation
- Browse all build documentation

#### [N5: Desktop & Device Service](docs/N5-Desktop-Device-Service/)
Electron-based desktop application and Python service integration
- Browse all desktop documentation

#### [N6: Caching & Performance](docs/N6-Caching-Performance/)
Performance optimization and caching strategies
- Browse all caching documentation

#### [N7: Security](docs/N7-Security/)
Security practices and threat protection
- Browse all security documentation

#### [N8: Observability](docs/N8-Observability/)
Logging, monitoring, and operational visibility
- Browse all observability documentation

#### [N9: App Publishing](docs/N9-App-Publishing/)
Mobile and desktop application distribution
- Browse all app publishing documentation

#### [N10: Administrative & Legal](docs/N10-Administrative-Legal/)
Settings, utilities, and compliance documentation
- Browse all administrative documentation

---

## 🔗 Quick Links

- **[Full Documentation Index](INDEX.md)** — Complete table of contents with all documents listed
- **[Site Map](SITEMAP.md)** — Comprehensive site structure
- **[Contributing Guide](CONTRIBUTING.md)** — How to contribute to documentation
- **[README](README.md)** — Repository information

---

## 📡 API Endpoint

```
https://api.kitchntabs.com
```

### Authentication

Include your Sanctum token in requests:

```bash
curl https://api.kitchntabs.com/api/orders \
  -H "Authorization: Bearer {your-token}"
```

---

## 💬 Support

- **Documentation Issues**: [GitHub Issues](https://github.com/kitchntabs/kitchntabs.github.io/issues)
- **API Questions**: Contact your account manager
- **Emergency Support**: Contact support team

---

<div class="footer-section">
  <p>© 2025 KitchnTabs. All rights reserved.</p>
  <p>Built with ❤️ for the restaurant industry</p>
</div>
