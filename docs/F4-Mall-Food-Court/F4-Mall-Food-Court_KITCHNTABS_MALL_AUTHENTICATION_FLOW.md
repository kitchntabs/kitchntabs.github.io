# KitchnTabs Mall - Authentication Flow Technical Documentation

## Overview

The KitchnTabs Mall application implements a **dual authentication architecture** that serves two distinct user types:

1. **Authenticated Admin Users**: Restaurant staff/mall administrators who login with credentials
2. **Guest Mall Customers**: Public users who access mall ordering via QR code session URLs without login

This document explains how the authentication system works, the interaction between React Admin's auth requirements and guest session handling, and the critical timing considerations for proper route rendering.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [URL Pattern Detection](#2-url-pattern-detection)
3. [Guest Authentication Flow](#3-guest-authentication-flow)
4. [Component Hierarchy](#4-component-hierarchy)
5. [The React Admin Authentication Challenge](#5-the-react-admin-authentication-challenge)
6. [Session Validation Flow](#6-session-validation-flow)
7. [Auth Provider Implementations](#7-auth-provider-implementations)
8. [Route Configuration](#8-route-configuration)
9. [WebSocket Integration](#9-websocket-integration)
10. [Data Flow Diagrams](#10-data-flow-diagrams)
11. [Troubleshooting Guide](#11-troubleshooting-guide)
12. [Key Files Reference](#12-key-files-reference)

---

## 1. Architecture Overview

### High-Level Authentication Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KitchnTabs Mall App                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    KitchnTabsMallBootstrap                           │    │
│  │                    (Entry Point & Router)                            │    │
│  └────────────────────────────┬────────────────────────────────────────┘    │
│                               │                                              │
│               ┌───────────────┴───────────────┐                             │
│               │                               │                             │
│               ▼                               ▼                             │
│   ┌─────────────────────┐         ┌─────────────────────────────────────┐  │
│   │   Admin Flow        │         │        Guest Session Flow            │  │
│   │   (/login, /admin)  │         │    (/:mallSlug/s/:sessionId/*)      │  │
│   │                     │         │                                      │  │
│   │  ┌───────────────┐  │         │  ┌─────────────────────────────┐    │  │
│   │  │ Redux Auth    │  │         │  │ Pre-set authenticated=true  │    │  │
│   │  │ isAuthenticated│ │         │  │ in localStorage             │    │  │
│   │  └───────────────┘  │         │  └─────────────────────────────┘    │  │
│   │         │           │         │              │                       │  │
│   │         ▼           │         │              ▼                       │  │
│   │  ┌───────────────┐  │         │  ┌─────────────────────────────┐    │  │
│   │  │ DASHMall      │  │         │  │ MallClientWrapper           │    │  │
│   │  │ AuthProvider  │  │         │  │ (Session Validation HoC)    │    │  │
│   │  └───────────────┘  │         │  └─────────────────────────────┘    │  │
│   │         │           │         │              │                       │  │
│   │         ▼           │         │              ▼                       │  │
│   │  ┌───────────────┐  │         │  ┌─────────────────────────────┐    │  │
│   │  │KitchnTabs     │  │         │  │ DASHMallClientAuthProvider  │    │  │
│   │  │PrivateApp     │  │         │  │ (Guest Auth)                │    │  │
│   │  └───────────────┘  │         │  └─────────────────────────────┘    │  │
│   └─────────────────────┘         │              │                       │  │
│                                   │              ▼                       │  │
│                                   │  ┌─────────────────────────────┐    │  │
│                                   │  │ KitchnTabsPrivateApp        │    │  │
│                                   │  │ (with guest permissions)    │    │  │
│                                   │  └─────────────────────────────┘    │  │
│                                   └─────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Session URL** | URL pattern `/:mallSlug/s/:sessionId` that identifies a guest mall ordering session |
| **authenticated flag** | localStorage value that React Admin uses to determine if private routes should render |
| **Guest Authentication** | Treating public users as "authenticated" for React Admin route rendering purposes |
| **Session Validation** | Backend API call to verify session hash is valid and not expired |

---

## 2. URL Pattern Detection

### URL Patterns

The application recognizes different URL patterns to determine the appropriate authentication flow:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           URL Pattern Detection                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Pattern 1: Session URL (Guest Mall Ordering)                               │
│  ─────────────────────────────────────────────                              │
│  Format: /:mallSlug/s/:sessionId/*                                          │
│  Example: /malltest/s/LNXEX                                                 │
│  Regex: /^\/[^/]+\/s\/[A-Z0-9]{5,}/i                                       │
│  Result: → MallClientWrapper + Guest Auth                                   │
│                                                                              │
│  Pattern 2: Direct Session Hash (Legacy)                                    │
│  ────────────────────────────────────────                                   │
│  Format: /:sessionId                                                        │
│  Example: /LNXEX                                                            │
│  Regex: /^\/([A-Z0-9]{5,})(?:\/|$)/i                                       │
│  Result: → MallClientWrapper + Guest Auth                                   │
│                                                                              │
│  Pattern 3: Non-Session URL (Admin/Public)                                  │
│  ──────────────────────────────────────────                                 │
│  Examples: /, /login, /admin/*                                              │
│  No regex match                                                              │
│  Result: → Standard auth flow (login required)                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detection Code (KitchnTabsMallBootstrap.tsx)

```typescript
// Check if URL matches a mall session pattern (/:mallSlug/s/:sessionId)
// Must be computed early before any conditional returns
const isSessionUrl = /^\/[^/]+\/s\/[A-Z0-9]{5,}/i.test(pathname);
```

---

## 3. Guest Authentication Flow

### The Critical Timing Problem

React Admin's `AsyncResources` component checks `authenticated` from `useAuthContext()` on **first render** to determine if private routes should be rendered:

```typescript
// In DASHAdmin.tsx - AsyncResources component
const { authenticated } = useAuthContext();

// Only renders customAuthRoutes if authenticated is true
{(authenticated) ? getCustomAuthRoutes()
  .filter(route => ...)
  .map((route, index) => ...) : null}
```

**Problem**: For guest mall users, `authenticated` is initially `false` because they haven't logged in. Even if the auth provider's `checkAuth()` resolves, React Admin may have already decided not to render private routes.

### Solution: Pre-set authenticated=true

The solution is to set `authenticated=true` in localStorage **synchronously during render**, before any React Admin components mount:

```typescript
// KitchnTabsMallBootstrap.tsx - CRITICAL: Set before React Admin mounts
if (isSessionUrl) {
    const currentAuth = dashStorage.getItem('authenticated');
    if (currentAuth !== 'true') {
        console.log('🔐 Setting guest authenticated=true');
        dashStorage.setItem('authenticated', 'true');
    }
}
```

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Guest Authentication Timing Flow                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ① User scans QR code → Browser navigates to /malltest/s/LNXEX             │
│     │                                                                        │
│     ▼                                                                        │
│  ② KitchnTabsMallBootstrap RENDER (synchronous)                             │
│     │                                                                        │
│     ├──▶ Detect isSessionUrl = true (regex match)                           │
│     │                                                                        │
│     ├──▶ ⚡ CRITICAL: Set localStorage 'authenticated' = 'true'             │
│     │    (Must happen BEFORE AdminContext reads it)                         │
│     │                                                                        │
│     └──▶ Render <MallClientWrapper>                                         │
│            │                                                                 │
│            ▼                                                                 │
│  ③ MallClientWrapper RENDER                                                 │
│     │                                                                        │
│     ├──▶ Parse URL → extract sessionId                                      │
│     │                                                                        │
│     ├──▶ Store session hash in localStorage                                 │
│     │                                                                        │
│     ├──▶ Show loading spinner                                               │
│     │                                                                        │
│     └──▶ useEffect → Start async validation                                 │
│            │                                                                 │
│            ▼                                                                 │
│  ④ Validation Effect (async)                                                │
│     │                                                                        │
│     ├──▶ API: GET /public/mall/{sessionId}/getSessionAuth                   │
│     │                                                                        │
│     ├──▶ Success → setValidationState({ isValid: true })                    │
│     │                                                                        │
│     └──▶ Failure → Clear 'authenticated', show error                        │
│            │                                                                 │
│            ▼                                                                 │
│  ⑤ KitchnTabsPrivateApp RENDER                                              │
│     │                                                                        │
│     ├──▶ Uses DASHMallClientAuthProvider (guest auth)                       │
│     │                                                                        │
│     └──▶ AdminContext reads 'authenticated' = 'true' from localStorage      │
│            │                                                                 │
│            ▼                                                                 │
│  ⑥ AsyncResources RENDER                                                    │
│     │                                                                        │
│     ├──▶ authenticated = true ✓                                             │
│     │                                                                        │
│     └──▶ Renders customAuthRoutes (including MallClientWelcome at /)        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Hierarchy

### Complete Component Tree

```
KitchnTabsMallBootstrap
│
├── [isAuthenticated = true] ──────────────────────────────────────┐
│   │                                                               │
│   └── KitchnTabsPrivateApp                                       │
│       ├── BrowserRouter (basename="/")                           │
│       ├── DASHMallAuthProvider (real auth)                       │
│       ├── DASHMallDataProvider                                   │
│       └── DASHAdmin                                              │
│           └── AsyncResources                                     │
│               └── AdminUI                                        │
│                   ├── dashPrivateRoutes                          │
│                   └── KitchnTabsMallResources                    │
│                                                                   │
├── [isSessionUrl = true] ─────────────────────────────────────────┐
│   │                                                               │
│   └── MallClientWrapper                                          │
│       ├── URL Parsing (sessionId, mallSlug)                      │
│       ├── Session Validation (API call)                          │
│       ├── MallSessionEchoProvider (WebSocket)                    │
│       │                                                           │
│       └── KitchnTabsPrivateApp                                   │
│           ├── BrowserRouter (basename="/malltest/s/LNXEX")       │
│           ├── DASHMallClientAuthProvider (guest auth)            │
│           ├── DASHMallClientDataProvider                         │
│           └── DASHAdmin                                          │
│               └── AsyncResources                                 │
│                   └── AdminUI                                    │
│                       ├── dashPrivateRoutes                      │
│                       │   └── MallClientWelcome (at /)           │
│                       └── KitchnTabsMallResources                │
│                                                                   │
└── [neither] ─────────────────────────────────────────────────────┐
    │                                                               │
    └── KitchnTabsPublicApp                                        │
        ├── dashPublicRoutes                                       │
        │   └── DASHLightWeightLogin (at /)                        │
        └── Standard public routes                                 │
```

---

## 5. The React Admin Authentication Challenge

### Problem Statement

React Admin is designed for authenticated applications. Its `AdminContext` and `AsyncResources` components use the `authenticated` state to decide which routes to render:

1. **AuthContext** reads `authenticated` from Redux state OR localStorage
2. **AsyncResources** conditionally renders `customAuthRoutes` based on `authenticated`
3. **First render** determines initial route rendering - changing `authenticated` later may not re-trigger

### Why Standard Auth Providers Don't Work for Guests

```typescript
// Standard pattern - doesn't work for guests
const authProvider = {
    checkAuth: async () => {
        // Even if this resolves, React Admin may have already
        // decided not to render private routes
        return Promise.resolve();
    }
};
```

### The Solution

**Two-part approach:**

1. **Pre-set `authenticated=true`** in localStorage synchronously in Bootstrap (before React Admin mounts)
2. **Auth provider that always resolves** (`DASHMallClientAuthProvider`)

```typescript
// KitchnTabsMallBootstrap.tsx - SYNCHRONOUS, during render
if (isSessionUrl) {
    dashStorage.setItem('authenticated', 'true');
}

// DASHMallClientAuthProvider.tsx - ASYNC, but always resolves
const authProvider = {
    checkAuth: async () => Promise.resolve(),
    getIdentity: async () => Promise.resolve({ id: 'guest', fullName: 'Guest' }),
    // ... all methods resolve
};
```

---

## 6. Session Validation Flow

### Validation State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Session Validation States                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐                                                           │
│  │   INITIAL    │  isValidating: true                                       │
│  │   STATE      │  isValid: false                                           │
│  └──────┬───────┘                                                           │
│         │                                                                    │
│         │ useEffect triggers                                                 │
│         ▼                                                                    │
│  ┌──────────────┐                                                           │
│  │  VALIDATING  │  API: GET /public/mall/{sessionId}/getSessionAuth        │
│  │              │  Shows: <CircularProgress />                              │
│  └──────┬───────┘                                                           │
│         │                                                                    │
│    ┌────┴────┐                                                              │
│    │         │                                                              │
│    ▼         ▼                                                              │
│ ┌──────┐  ┌──────────┐                                                      │
│ │SUCCESS│  │  ERROR   │                                                      │
│ │      │  │          │                                                      │
│ │isValid│  │isValid:  │                                                      │
│ │: true │  │false     │                                                      │
│ └──┬───┘  └────┬─────┘                                                      │
│    │           │                                                             │
│    │           │ Clear 'authenticated' from localStorage                    │
│    │           │ Show error message                                         │
│    │           │                                                             │
│    ▼           ▼                                                             │
│ ┌──────────┐  ┌──────────────────────────────────────┐                      │
│ │ Render   │  │ Error States:                        │                      │
│ │ Children │  │ - 404: Session not found             │                      │
│ │          │  │ - 410: Session expired               │                      │
│ │          │  │ - 403: Access denied                 │                      │
│ └──────────┘  │ - 500: Server error                  │                      │
│               └──────────────────────────────────────┘                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Backend API Response

**Endpoint**: `GET /public/mall/{sessionId}/getSessionAuth`

**Success Response** (200):
```json
{
    "tenant": { /* tenant data */ },
    "auth": {
        "tenant_id": 123,
        "tenant_name": "Mall Name",
        "settings": { /* mall settings */ }
    },
    "systemValues": {
        "pos": [],
        "mall": { /* mall data */ },
        "tenants": [ /* active tenants */ ]
    },
    "redirectTo": "/public/mall/tab/create"
}
```

**Error Responses**:
- `410 Gone`: Session expired (includes `expired_at` timestamp)
- `404 Not Found`: Invalid session hash
- `403 Forbidden`: Access denied

---

## 7. Auth Provider Implementations

### DASHMallAuthProvider (Admin Users)

Used for authenticated admin/staff users. Extends the standard `DASHAuthProvider`.

```typescript
// Real authentication - login with credentials
const authProvider = {
    login: async ({ username, password }) => {
        const response = await api.post('/login', { username, password });
        // Store token, user data in localStorage
        return response;
    },
    checkAuth: async () => {
        const token = localStorage.getItem('token');
        if (!token) throw new Error('Not authenticated');
        return Promise.resolve();
    },
    logout: async () => {
        localStorage.clear();
        return '/login';
    },
    // ... other methods
};
```

### DASHMallClientAuthProvider (Guest Users)

Used for guest mall ordering. All methods resolve - no real authentication.

```typescript
/**
 * Mall Client Auth Provider
 * 
 * Treats guests as "authenticated" so React Admin renders private routes.
 * The guest identity allows access to mall ordering without login.
 */
const authProvider = {
    // Always return guest identity
    getIdentity: async () => Promise.resolve({
        id: 'guest',
        fullName: 'Guest',
        avatar: undefined,
    }),
    
    // Always resolve - tells React Admin user is "authenticated"
    checkAuth: async () => Promise.resolve(),
    
    // No login required
    login: async () => Promise.resolve(),
    
    // No logout action
    logout: async () => Promise.resolve(),
    
    // Don't redirect on errors
    checkError: async () => Promise.resolve(),
    
    // Guest permissions
    getPermissions: async () => Promise.resolve(['guest', 'public']),
};
```

---

## 8. Route Configuration

### Route Types

| Route Type | Context | Renders When |
|------------|---------|--------------|
| `dashPublicRoutes` | Non-session URLs | `isAuthenticated = false` AND `isSessionUrl = false` |
| `dashPrivateRoutes` | Session URLs | `isSessionUrl = true` (guest) OR `isAuthenticated = true` |
| `customAuthRoutes` | React Admin | `authenticated = true` (from localStorage) |

### Route Definitions (KitchnTabsMallRoutes.tsx)

```typescript
// For guest mall users (session URLs) - shows MallClientWelcome at /
export const dashPrivateRoutes = () => [
    ...dashSharedRoutes(),
    <Route
        key="landing"
        data-layout="no-layout"
        path='/'
        element={<MallClientWelcome />}
    />,
    <Route
        key="private-not-found" 
        path="*"
        element={<NotFound />}
    />
];

// For non-session URLs - shows Login at /
export const dashPublicRoutes = () => [
    ...dashSharedRoutes(),
    <Route
        key="landing"
        data-layout="no-layout"
        path='/'
        element={<DASHLightWeightLogin />}
    />,
    <Route
        key="public-not-found"
        path="*"
        element={<NotFound />}
    />
];
```

### React Router basename

The `basename` is dynamically set based on the session URL:

```typescript
// MallClientWrapper calculates sessionBasePath
const sessionBasePath = `/${mallSlug}/s/${sessionId}`; // e.g., "/malltest/s/LNXEX"

// Passed to KitchnTabsPrivateApp
<KitchnTabsPrivateApp appPath={sessionBasePath} />

// Used as BrowserRouter basename
<BrowserRouter basename={appPath || '/'}>
```

This means:
- Session URL `/malltest/s/LNXEX` → basename `/malltest/s/LNXEX`
- Route `/` inside app → Full URL `/malltest/s/LNXEX/`
- Route `/orders` inside app → Full URL `/malltest/s/LNXEX/orders`

---

## 9. WebSocket Integration

### MallSessionEchoProvider

Wraps the guest app to provide WebSocket connectivity for real-time order updates:

```typescript
// MallClientWrapper.tsx
return (
    <MallSessionEchoProvider sessionId={sessionId}>
        <KitchnTabsPrivateApp {...props} />
    </MallSessionEchoProvider>
);
```

### WebSocket Channel

```
Channel: session.{sessionId}
Events:
  - mall_order_status_update
  - mall_tab_creation
  - mall_assistance_request
```

---

## 10. Data Flow Diagrams

### Complete Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Complete Mall Session Authentication Flow                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 1. USER ACTION: Scan QR Code                                         │   │
│  │    QR contains: https://domain.com/malltest/s/LNXEX                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 2. BROWSER: Navigate to URL                                          │   │
│  │    pathname = "/malltest/s/LNXEX"                                    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 3. KitchnTabsMallBootstrap: URL PATTERN CHECK                        │   │
│  │                                                                       │   │
│  │    isSessionUrl = /^\/[^/]+\/s\/[A-Z0-9]{5,}/i.test(pathname)       │   │
│  │    isSessionUrl = true ✓                                             │   │
│  │                                                                       │   │
│  │    ⚡ CRITICAL: dashStorage.setItem('authenticated', 'true')        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 4. RENDER DECISION                                                    │   │
│  │                                                                       │   │
│  │    if (isAuthenticated) → Admin App                                  │   │
│  │    else if (isSessionUrl) → MallClientWrapper + Guest App  ←─────────│   │
│  │    else → Public App (Login)                                         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 5. MallClientWrapper: MOUNT                                          │   │
│  │                                                                       │   │
│  │    a. Parse URL → sessionId="LNXEX", mallSlug="malltest"            │   │
│  │    b. Calculate sessionBasePath="/malltest/s/LNXEX"                  │   │
│  │    c. Store in localStorage:                                         │   │
│  │       - mall-session-hash = "LNXEX"                                  │   │
│  │       - authenticated = "true" (reinforced)                          │   │
│  │    d. Initial state: isValidating=true → Show spinner               │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 6. MallClientWrapper: useEffect VALIDATION                           │   │
│  │                                                                       │   │
│  │    API Request: GET /public/mall/LNXEX/getSessionAuth               │   │
│  │                                                                       │   │
│  │    ┌─────────────────┐    ┌─────────────────┐                        │   │
│  │    │    SUCCESS      │    │     ERROR       │                        │   │
│  │    │    (200)        │    │ (404/410/403)   │                        │   │
│  │    └────────┬────────┘    └────────┬────────┘                        │   │
│  │             │                       │                                 │   │
│  │             ▼                       ▼                                 │   │
│  │    isValid = true          isValid = false                           │   │
│  │    Store tenant data       Clear 'authenticated'                     │   │
│  │                            Show error message                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼ (on success)                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 7. RENDER CHILDREN (KitchnTabsPrivateApp)                            │   │
│  │                                                                       │   │
│  │    Props:                                                            │   │
│  │    - appPath = "/malltest/s/LNXEX" (used as BrowserRouter basename) │   │
│  │    - customAuthProvider = DASHMallClientAuthProvider                 │   │
│  │    - customDataProvider = DASHMallClientDataProvider                 │   │
│  │                                                                       │   │
│  │    Wrapped in: <MallSessionEchoProvider sessionId="LNXEX">           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 8. KitchnTabsPrivateApp: MOUNT                                       │   │
│  │                                                                       │   │
│  │    <BrowserRouter basename="/malltest/s/LNXEX">                      │   │
│  │      <DASHAdmin                                                      │   │
│  │        authProvider={DASHMallClientAuthProvider}                     │   │
│  │        dataProvider={DASHMallClientDataProvider}                     │   │
│  │        basename="/malltest/s/LNXEX"                                  │   │
│  │      >                                                               │   │
│  │        <AsyncResources ... />                                        │   │
│  │      </DASHAdmin>                                                    │   │
│  │    </BrowserRouter>                                                  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 9. DASHAdmin/AsyncResources: AUTH CHECK                              │   │
│  │                                                                       │   │
│  │    const { authenticated } = useAuthContext();                       │   │
│  │    // Reads from localStorage: authenticated = "true" ✓             │   │
│  │                                                                       │   │
│  │    authenticated = true                                              │   │
│  │    → Renders customAuthRoutes (dashPrivateRoutes)                   │   │
│  │    → Shows MallClientWelcome at /                                    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                               │                                              │
│                               ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 10. FINAL STATE: User sees MallClientWelcome                         │   │
│  │                                                                       │   │
│  │    URL: https://domain.com/malltest/s/LNXEX                         │   │
│  │    Component: <MallClientWelcome />                                  │   │
│  │    WebSocket: Connected to session.LNXEX channel                    │   │
│  │    Auth: Guest (no login required)                                   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌─────────┐ ┌───────────────────┐ ┌───────────────────┐ ┌─────────────────┐ ┌───────────┐
│ Browser │ │ Bootstrap         │ │ MallClientWrapper │ │ Backend API     │ │ React     │
│         │ │                   │ │                   │ │                 │ │ Admin     │
└────┬────┘ └─────────┬─────────┘ └─────────┬─────────┘ └────────┬────────┘ └─────┬─────┘
     │                │                     │                    │                │
     │ Navigate to    │                     │                    │                │
     │ /malltest/s/X  │                     │                    │                │
     │───────────────▶│                     │                    │                │
     │                │                     │                    │                │
     │                │ Detect isSessionUrl │                    │                │
     │                │ = true              │                    │                │
     │                │─────────────────────│                    │                │
     │                │                     │                    │                │
     │                │ Set localStorage    │                    │                │
     │                │ authenticated=true  │                    │                │
     │                │─────────────────────│                    │                │
     │                │                     │                    │                │
     │                │ Render              │                    │                │
     │                │─────────────────────▶                    │                │
     │                │                     │                    │                │
     │                │                     │ Parse URL          │                │
     │                │                     │ Store session hash │                │
     │                │                     │───────────────────▶│                │
     │                │                     │                    │                │
     │                │                     │ GET /getSessionAuth│                │
     │                │                     │───────────────────▶│                │
     │                │                     │                    │                │
     │                │                     │◀───────────────────│                │
     │                │                     │ 200 OK             │                │
     │                │                     │ { tenant, auth }   │                │
     │                │                     │                    │                │
     │                │                     │ Render children    │                │
     │                │                     │ with appPath       │                │
     │                │                     │────────────────────────────────────▶│
     │                │                     │                    │                │
     │                │                     │                    │    Read        │
     │                │                     │                    │    authenticated
     │                │                     │                    │    = true      │
     │                │                     │                    │                │
     │                │                     │                    │    Render      │
     │◀──────────────────────────────────────────────────────────────────────────│
     │ Show MallClientWelcome              │                    │                │
     │                │                     │                    │                │
```

---

## 11. Troubleshooting Guide

### Problem: Session URL shows Login instead of MallClientWelcome

**Symptoms:**
- Navigating to `/malltest/s/LNXEX` shows Login page
- Console shows "DASHLightWeightLogin.tsx: Initializing app authentication..."

**Cause:** `authenticated` flag not set before React Admin reads it

**Solution:**
1. Ensure `authenticated=true` is set synchronously in Bootstrap:
```typescript
if (isSessionUrl) {
    dashStorage.setItem('authenticated', 'true');
}
```
2. This must happen BEFORE any conditional returns or async operations

### Problem: Session validation fails with 410 (Expired)

**Symptoms:**
- Error message shows "Session has expired"
- Backend returns 410 status

**Cause:** Session older than 10 hours from activation

**Solution:**
- Generate new session QR code
- Sessions auto-expire after 10 hours

### Problem: WebSocket not receiving updates

**Symptoms:**
- Order status updates not appearing in real-time
- Console shows WebSocket connection errors

**Cause:** MallSessionEchoProvider not wrapping the app correctly

**Solution:**
- Verify `sessionId` is passed to MallSessionEchoProvider
- Check WebSocket server configuration

### Problem: Routes not matching after navigation

**Symptoms:**
- Internal navigation works, but page shows 404
- URL shows correct path but wrong component renders

**Cause:** BrowserRouter basename mismatch

**Solution:**
- Verify `appPath` is correctly passed from MallClientWrapper
- Ensure `sessionBasePath` calculation is correct

---

## 12. Key Files Reference

| File | Purpose |
|------|---------|
| `apps/kitchntabs-mall/src/KitchnTabsMallBootstrap.tsx` | Main entry point, URL detection, auth flag pre-setting |
| `apps/kitchntabs-mall/src/components/mall/MallClientWrapper.tsx` | Session validation HoC, URL parsing, WebSocket wrapper |
| `apps/kitchntabs-mall/src/dash-extensions/config/DASHMallClientAuthProvider.tsx` | Guest auth provider (all methods resolve) |
| `apps/kitchntabs-mall/src/dash-extensions/config/DASHMallClientDataProvider.tsx` | Data provider with session context injection |
| `apps/kitchntabs-mall/src/KitchnTabsMallRoutes.tsx` | Route definitions (public vs private) |
| `apps/kitchntabs-mall/src/core/KitchnTabsPrivateApp.tsx` | Private app wrapper, BrowserRouter configuration |
| `packages/dash-admin/src/DASHAdmin.tsx` | React Admin wrapper, AsyncResources (auth gating) |

---

## Summary

The KitchnTabs Mall authentication system solves the challenge of using React Admin (designed for authenticated apps) with public guest users. The key insight is:

1. **React Admin checks `authenticated` synchronously** on first render
2. **Setting `authenticated=true` must happen BEFORE React Admin mounts**
3. **Session validation is async** but route rendering decision is sync
4. **The solution**: Pre-set `authenticated=true` in Bootstrap when a session URL is detected

This architecture enables:
- ✅ Guest users accessing mall ordering without login
- ✅ Real users logging in for admin functionality  
- ✅ Proper route rendering for both user types
- ✅ Session validation with appropriate error handling
- ✅ WebSocket integration for real-time updates
