# KitchnTabs Documentation

<p align="center">
  <img src="assets/kitchntabs-h.png" alt="KitchnTabs Logo" width="400">
</p>

<p align="center">
  <strong>Comprehensive Restaurant & Food Court Management Platform</strong>
</p>

<p align="center">
  <a href="https://kitchntabs.github.io">📚 View Documentation</a> •
  <a href="https://api.kitchntabs.com">🔗 API Endpoint</a>
</p>

---

## 🚀 About KitchnTabs

KitchnTabs is a full-stack enterprise solution for restaurant and food court management, built with Laravel and React. Our platform combines powerful backend APIs with intuitive frontend interfaces to deliver a seamless experience for customers, staff, and administrators.

### Platform Components

- **Dash Backend** — Laravel 11 REST API with multi-tenant architecture
- **Dash Admin** — React-Admin dashboard for restaurant management
- **Mall App** — QR code-based ordering for food courts
- **Customer App** — Mobile-first ordering experience
- **Staff App** — Real-time order management

## 📖 Documentation

Visit our comprehensive documentation at **[kitchntabs.github.io](https://kitchntabs.github.io)**

### Quick Links

- **[Mall Application](https://kitchntabs.github.io/docs/mall-app/01-OVERVIEW.html)** - Food court ordering system
- **[Customer App](https://kitchntabs.github.io/docs/customer-app/CUSTOMER_APP_COMPLETE_FLOW.html)** - Mobile ordering experience
- **[Staff App](https://kitchntabs.github.io/docs/staff-app/STAFF_APP_COMPLETE_FLOW.html)** - Real-time order management
- **[Access Control](https://kitchntabs.github.io/docs/tech/features/acl/dash-role-permission-overview.html)** - Role-based permissions
- **[Notification System](https://kitchntabs.github.io/docs/tech/features/notifications/NOTIFICATION_SYSTEM_DOCUMENTATION.html)** - Real-time & push notifications
- **[Build System](https://kitchntabs.github.io/docs/tech/toolchain/PRODUCTION_BUILD_TECHNICAL_DOCUMENTATION.html)** - Production deployment

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           KitchnTabs Platform                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐         ┌──────────────┐     │
│  │   Laravel    │◄───────►│    React     │     │
│  │   Backend    │         │   Frontend   │     │
│  │              │         │              │     │
│  │  • REST API  │         │  • Admin UI  │     │
│  │  • WebSocket │         │  • Mall App  │     │
│  │  • Multi-    │         │  • Customer  │     │
│  │    Tenant    │         │    App       │     │
│  └──────────────┘         └──────────────┘     │
│         │                        │              │
│         ▼                        ▼              │
│  ┌──────────────┐         ┌──────────────┐     │
│  │   MySQL      │         │   Redis      │     │
│  │   Database   │         │   Cache      │     │
│  └──────────────┘         └──────────────┘     │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 🔑 Key Features

### For Customers
- ✅ QR code table access
- ✅ Multi-restaurant ordering
- ✅ Real-time order tracking
- ✅ Push notifications
- ✅ No authentication required

### For Restaurant Staff
- ✅ Real-time order management
- ✅ Status update workflows
- ✅ Push notifications
- ✅ Kitchen display integration

### For Administrators
- ✅ Multi-tenant management
- ✅ Role-based access control
- ✅ Analytics & reporting
- ✅ QR code generation
- ✅ Marketplace integrations

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend API | Laravel 11, PHP 8.2 |
| Frontend | React 18, React-Admin |
| Database | MySQL/PostgreSQL |
| Cache | Redis |
| Real-time | Laravel Echo, Pusher/Soketi |
| Push | Firebase Cloud Messaging |
| Build | Vite, pnpm workspaces |
| Deployment | Docker, AWS |

## 📡 API Endpoint

All API requests should be made to:

```
https://api.kitchntabs.com
```

### Authentication

KitchnTabs uses Laravel Sanctum for API authentication:

```bash
curl -X POST https://api.kitchntabs.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

Include your token in subsequent requests:

```bash
curl https://api.kitchntabs.com/api/orders \
  -H "Authorization: Bearer {your-token}"
```

## 🔒 Security

- ✅ All sensitive credentials have been removed from documentation
- ✅ HTTPS enforced for all API endpoints
- ✅ Token-based authentication
- ✅ Role-based access control
- ✅ Multi-tenant data isolation

## 📝 Contributing to Documentation

This documentation is built with Jekyll and hosted on GitHub Pages.

### Local Development

```bash
# Clone the repository
git clone https://github.com/kitchntabs/kitchntabs.github.io.git
cd kitchntabs.github.io

# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve

# View at http://localhost:4000
```

### Documentation Structure

```
kitchntabs-github-io/
├── docs/
│   ├── mall-app/           # Mall application docs
│   ├── customer-app/       # Customer app docs
│   ├── staff-app/          # Staff app docs
│   └── tech/               # Technical documentation
│       ├── features/       # Feature documentation
│       ├── architecture/   # System architecture
│       └── toolchain/      # Build & deployment
├── assets/                 # Images and resources
├── _layouts/               # Jekyll layouts
└── index.md                # Homepage
```

## 🎨 Design System

KitchnTabs uses a consistent design system:

- **Primary Color**: `#8f00cb` (Purple)
- **Contrast Color**: `#00044c` (Deep Blue)
- **Font**: System fonts for optimal performance

## 📄 License

© 2025 KitchnTabs. All rights reserved.

## 💬 Support

For questions or support:

- **Documentation Issues**: Open an issue on GitHub
- **API Questions**: Contact your account manager
- **Emergency Support**: Contact support team

---

<p align="center">
  Built with ❤️ for the restaurant industry
</p>
