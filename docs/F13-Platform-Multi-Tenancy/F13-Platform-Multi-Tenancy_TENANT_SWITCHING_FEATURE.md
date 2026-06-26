
# Tenancy–Tenant Switching Feature

## Overview

The Tenant Switching feature allows authenticated **tenancy-level** administrators to dynamically switch their admin panel context between the **Tenancy Account** (managing entity) and any of its associated **Tenants** (individual business units) — without logging out or reloading the page.

When a user switches context:
- The **sidebar menu** updates to show only the resources available at that level
- The **API requests** automatically target the selected tenant via an `X-Tenant-Id` header
- **CSS variables, logos, and branding** update to reflect the active tenant's theme colors and settings
- The **MUI theme** is rebuilt with the new tenant's color palette
- The **react-admin application** fully remounts with a new resource set and routes

This feature is gated behind the `ENABLE_TENANT_IMPERSONATION` system constant and only renders when the authenticated user belongs to a tenancy account that has associated tenants.

---

## Architecture

### Component Hierarchy

```
KitchnTabsWebPrivateAppLoader
├── (listens for) window event: 'tenant_switch'
├── (manages) tenantContext state → drives resource loading
├── (dispatches) setResources() → Redux store
│
└── KitchnTabsWebPrivateApp (key={switchKey} → forces remount)
    ├── DashThemeProvider (MUI ThemeProvider + DashThemeContext)
    │   ├── reads AuthPersistenceService.getTenantSettings() on mount
    │   ├── builds MUI theme via appTheme() with tenant colors
    │   ├── observes data-theme attribute for light/dark mode changes
    │   └── recreateTheme() → rebuilds palette + updates CSS variables
    │
    ├── DASHAdmin (customResources, useCoreResources=false)
    │   ├── calculateResources() → dispatches to Redux
    │   ├── useSelector(selectResources) → AsyncResources
    │   └── AsyncResources (React.memo) → AdminUI → renders resources
    │
    └── AppMaterialMenu
        └── useSelector(state.resources.items) → builds sidebar groups
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        TENANT SWITCHING DATA FLOW                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐                                                         │
│  │ TenantSwitcher  │  (UI: header dropdown)                                 │
│  │                 │                                                         │
│  │ 1. Persist      │  dashStorage.setItem('active_tenant_id', tenantId)     │
│  │ 2. API Call     │  GET /auth/tenancyAuth  (X-Tenant-Id: {tenantId})      │
│  │ 3. Persist auth │  AuthPersistenceService.saveAuth(response)             │
│  │ 4. Update CSS   │  updateDomCssVariables(mode, colors, values)           │
│  │ 5. Update logos │  dispatch(setPanelSettings({logos}))                    │
│  │ 6. Dispatch     │  window.dispatchEvent('tenant_switch', detail)         │
│  └────────┬────────┘                                                         │
│           │                                                                  │
│           │  CustomEvent('tenant_switch')                                    │
│           ▼                                                                  │
│  ┌──────────────────────────┐                                                │
│  │ PrivateAppLoader         │                                                │
│  │                          │                                                │
│  │ 1. Clear resources/routes│  setResources(null)                            │
│  │ 2. Increment switchKey   │  setSwitchKey(prev + 1)                        │
│  │ 3. Update tenantContext  │  setTenantContext(detail.tenantId)              │
│  └────────┬─────────────────┘                                                │
│           │                                                                  │
│           │  useEffect([tenantContext])                                       │
│           ▼                                                                  │
│  ┌──────────────────────────┐                                                │
│  │ Resource Loading         │                                                │
│  │                          │                                                │
│  │ tenantContext = null:     │  → KitchnTabsWebPrivateResources (23 res)     │
│  │ tenantContext = "123":    │  → KitchnTabsWebTenantPrivateResources (4 res)│
│  │                          │                                                │
│  │ clearResourceCache()     │                                                │
│  │ loadResourcesFromManifest│                                                │
│  │ dispatch(setResources()) │  → Redux store                                │
│  └────────┬─────────────────┘                                                │
│           │                                                                  │
│           │  key={switchKey} forces full remount                             │
│           ▼                                                                  │
│  ┌──────────────────────────┐                                                │
│  │ KitchnTabsWebPrivateApp  │  (new instance)                               │
│  │                          │                                                │
│  │ ┌── DashThemeProvider ──┐│                                                │
│  │ │ Reads tenant settings ││                                                │
│  │ │ Builds MUI theme      ││                                                │
│  │ │ Applies CSS variables ││                                                │
│  │ └───────────────────────┘│                                                │
│  │                          │                                                │
│  │ ┌── DASHAdmin ──────────┐│                                                │
│  │ │ calculateResources →  ││  dispatch(setResources)                        │
│  │ │ AsyncResources        ││  reads from Redux → renders AdminUI            │
│  │ └───────────────────────┘│                                                │
│  │                          │                                                │
│  │ ┌── AppMaterialMenu ────┐│                                                │
│  │ │ useSelector(resources) ││  → builds grouped sidebar menu items          │
│  │ └───────────────────────┘│                                                │
│  └──────────────────────────┘                                                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Files Involved

### Frontend — Application Layer

| File | Purpose |
|------|---------|
| `apps/kitchntabs-web/src/components/tenancy/TenantSwitcher.tsx` | UI dropdown + switching logic (API call, persistence, event dispatch) |
| `apps/kitchntabs-web/src/components/tenancy/index.ts` | Barrel export for TenantSwitcher and utility functions |
| `apps/kitchntabs-web/src/components/DashHeaderActions.tsx` | Header component that renders `<TenantSwitcher />` alongside notifications |
| `apps/kitchntabs-web/src/KitchnTabsWebPrivateAppLoader.tsx` | Orchestrator — listens for switch events, loads manifests, dispatches to Redux, remounts app |
| `apps/kitchntabs-web/src/KitchnTabsWebPrivateApp.tsx` | Renders `<DASHAdmin>` with resolved resources and routes |
| `apps/kitchntabs-web/src/resources/KitchnTabsWebPrivateResources.tsx` | Tenancy-level resource manifest (18 keys → ~23 resolved resources) |
| `apps/kitchntabs-web/src/resources/KitchnTabsWebTenantPrivateResources.tsx` | Tenant-level resource manifest (4 keys → 4 resolved resources) |
| `apps/kitchntabs-web/src/dash-extensions/config/DASHAuthProvider.tsx` | Auth provider — respects `active_tenant_id` in `getIdentity` flow |

### Frontend — Shared Libraries (Dash Admin Framework)

| File | Purpose |
|------|---------|
| `packages/dash-admin/src/DASHAdmin.tsx` | Core admin — `calculateResources`, Redux dispatch, `AsyncResources` memo |
| `packages/dash-admin/src/default-theme/DashThemeContext.tsx` | MUI ThemeProvider wrapper — reads tenant colors on mount, rebuilds palette on switch, observes `data-theme` for mode changes |
| `packages/dash-admin/src/default-theme/menu/AppMaterialMenu.tsx` | Sidebar menu — reads `state.resources.items` from Redux |
| `packages/dash-admin/src/default-theme/updateDomCssVariables.tsx` | (Copy) CSS variable injection into `<style id="dash-theme-variables">` — kept in sync with dash-utils version |
| `packages/dash-admin-state/src/redux/actions/Resources.tsx` | Redux action: `setResources`, `appendResources` |
| `packages/dash-admin-state/src/redux/reducers/Resources.tsx` | Redux reducer: `SET_RESOURCES → { items: [...payload] }` |
| `packages/dash-app-common/src/components/DashResourceLoader.tsx` | `loadResourcesFromManifest`, `clearResourceCache` (WeakMap-based) |
| `packages/dash-axios-hook/src/hooks/useAxios.tsx` | Axios interceptor — injects `X-Tenant-Id` header from `active_tenant_id` |
| `packages/dash-utils/src/utils/updateDomCssVariables.tsx` | Primary CSS variable injection — creates `<style id="dash-theme-variables">` at end of `<head>`, generates suffixed + base alias CSS variables |
| `packages/dash-styles/src/index.tsx` | `appTheme()` builder — `_color()` helper resolves tenant colors → CSS variable fallback → MUI palette, `getAllCssVariablesFromStyleSheets()` reads static LESS defaults |
| `packages/dash-styles/src/dash-css-transformer.less` | LESS → CSS compilation — defines ~200+ `:root` CSS custom properties (suffixed: `--key--light`, `--key--dark`) from LESS variables |
| `packages/dash-auth/src/AuthPersistanceService.tsx` | Persistence API — `saveAuth()`, `getTenantSettings()`, `setTenantSettings()` — stores/retrieves tenant colors from localStorage |

### Backend

| File | Purpose |
|------|---------|
| `dash-backend/domain/app/Http/Controllers/API/Auth/AuthController.php` | `getTenancyAuth()` — reads `X-Tenant-Id` header to scope response to specific tenant; returns `tenantSettings` (including `colors`) from `$tenant->settings` JSON column |
| `dash-backend/app/Models/Tenant.php` | `settings` accessor (JSON cast), `setting($name)` method with config defaults fallback |
| `dash-backend/config/tenants.php` | Defines `theme_colors` setting format with `default_value` containing ~100+ color variables; defines `theme_values` with CSS dimension defaults |

---

## Components In Detail

### 1. TenantSwitcher

**Location:** `apps/kitchntabs-web/src/components/tenancy/TenantSwitcher.tsx`

A hover/click dropdown rendered in the admin header bar. It presents:
- **Tenancy Account** option (the managing entity)
- **Individual Tenant** options (from `systemValues.tenants`)

#### Exported Utilities

```typescript
// Dispatch the event that triggers the entire switching flow
export const dispatchTenantSwitchEvent = (detail: TenantSwitchEventDetail) => {
    window.dispatchEvent(new CustomEvent('tenant_switch', { detail }));
};

// Read the currently active tenant (null = tenancy level)
export const getActiveTenantId = (): string | null => { ... };

// Check if the feature is enabled
export const isTenantImpersonationEnabled = (): boolean => { ... };
```

#### Event Detail Interface

```typescript
export interface TenantSwitchEventDetail {
    tenantId: string | null;   // null = tenancy account level
    tenantName: string;
    isTenanancyLevel: boolean;
}
```

#### Switch Flow (handleSwitch)

1. **Persist tenant ID** — `dashStorage.setItem('active_tenant_id', tenantId)` (before API call so axios interceptor picks it up)
2. **API call** — `GET /auth/tenancyAuth` with `X-Tenant-Id` header when switching to a specific tenant
3. **Persist auth response** — `AuthPersistenceService.saveAuth(authData)` (stores `tenantSettings` and `tenantImages` to localStorage)
4. **Update auth context** — `setAuthEvent({ authenticated: true, user, auth, token, roles })`
5. **Update CSS variables** — `updateDomCssVariables(currentThemeMode, tenantSettings?.colors, tenantSettings?.values)` — reads actual `data-theme` attribute for correct mode; always called even when `colors` is undefined (resets to compiled LESS defaults)
6. **Update logos** — `dispatch(setPanelSettings({ horizontalLogo, squaredLogo, loginBackground }))`
7. **Persist tenant settings** — `AuthPersistenceService.setTenantSettings(tenantSettings)`
8. **Dispatch switch event** — `dispatchTenantSwitchEvent({ tenantId, tenantName, isTenanancyLevel })`

If the switch fails, storage is reverted to the previous `activeTenantId`.

---

### 2. KitchnTabsWebPrivateAppLoader

**Location:** `apps/kitchntabs-web/src/KitchnTabsWebPrivateAppLoader.tsx`

The orchestrator component that bridges the switch event to the react-admin application lifecycle.

#### State Management

| State | Type | Purpose |
|-------|------|---------|
| `tenantContext` | `string \| null \| UNINITIALIZED` | Tracks which tenant is active. `UNINITIALIZED` prevents premature loading. |
| `resources` | `any[]` | Resolved resource config array passed to `KitchnTabsWebPrivateApp` |
| `routes` | `{ private, public }` | Route functions for the admin app |
| `switchKey` | `number` | Incremented on each switch to force full remount via React `key` prop |
| `isLoading` | `boolean` | Guards rendering until resources are ready |

#### Lifecycle

1. **Mount**: Reads `active_tenant_id` from `dashStorage` → sets initial `tenantContext`
2. **Event listener**: Listens for `tenant_switch` events → clears resources, increments `switchKey`, updates `tenantContext`
3. **Resource loading effect** (`useEffect([tenantContext])`):
   - If `tenantContext` is a string (tenant level) → loads **only** `KitchnTabsWebTenantPrivateResources`
   - If `tenantContext` is null (tenancy level) → loads `KitchnTabsWebPrivateResources`
   - Calls `clearResourceCache()` to bust the WeakMap cache
   - Calls `loadResourcesFromManifest()` to resolve lazy imports
   - Dispatches resolved resources to Redux via `setReduxResources()`
4. **Render**: Passes resolved resources as a pre-resolved array to `KitchnTabsWebPrivateApp` with `key={switchKey}` for forced remount

#### Why Force Remount?

React-admin's internal state (data provider cache, resource registrations, route matching) is initialized at mount time. Changing resources via props alone does not reliably update all internal state. The `key` prop change causes React to unmount the old instance entirely and mount a fresh one with the new resources.

---

### 3. Resource Manifests

#### Tenancy-Level: `KitchnTabsWebPrivateResources`

Contains the full set of admin resources (~18 manifest keys resolving to ~23 resource configs):

- **Tenancy management**: tenancy accounts, users, roles, permissions
- **Geo-hierarchy**: communes, countries, regions
- **E-commerce**: products, categories, galleries, brands, currencies, price lists, stock types, modifier groups
- **Import/export**: product import templates and instances
- **Tenant resources**: marketplaces, points of sale, metadata formats, campaigns

#### Tenant-Level: `KitchnTabsWebTenantPrivateResources`

Contains only the subset of resources relevant when operating as a specific tenant (4 keys):

- `marketplaceResource`
- `pointOfSaleResource`
- `metadataFormatsResource`
- `campaignResource`

> **Design Decision**: The tenant manifest loads **only** tenant-specific resources rather than merging with the base manifest. This ensures a clear distinction in the sidebar menu between tenancy administration (full resource set) and tenant operation (scoped resource set).

---

### 4. DASHAdmin (Framework)

**Location:** `packages/dash-admin/src/DASHAdmin.tsx`

The core admin component from the Dash Admin framework. Key behaviors relevant to tenant switching:

#### calculateResources

A `useCallback` that computes the final resource array:

```typescript
const calculateResources = useCallback(() => {
    const _resources = !children
        ? customResources
            ? useCoreResources === false
                ? customResources                          // Use only custom (our case)
                : [...coreResources, ...customResources]   // Merge with core
            : coreResources                                // Core only
        : [];                                              // Children mode (no resources)
    dispatch(setResources(_resources));
}, [children, customResources, useCoreResources, dispatch]);
```

This runs in a `useEffect([calculateResources])` — reactive to prop changes. Since `PrivateAppLoader` passes a **new array reference** on each switch, the `useCallback` recomputes and dispatches to Redux.

#### AsyncResources (React.memo)

Wraps `AdminUI` and receives resources from Redux via `useSelector`. Its custom comparator checks:
- Array length equality
- Per-item reference equality

When switching from 23 resources to 4 (or vice versa), the length check fails immediately, allowing the re-render.

#### DASHAdminApp (React.memo)

The outer memo checks `prevProps.customResources === nextProps.customResources`. Since the loader creates a new array on each switch, this comparison always fails, allowing the prop change to propagate.

---

### 5. AppMaterialMenu

**Location:** `packages/dash-admin/src/default-theme/menu/AppMaterialMenu.tsx`

Reads resources from Redux and builds the sidebar menu:

```typescript
const resources = useSelector((state) => state.resources.items);
```

When `SET_RESOURCES` is dispatched, Redux creates a new `{ items: [...payload] }` object, so the selector returns a new reference, triggering a re-render. The menu then recomputes groups and menu items from the updated resource list.

---

### 6. Axios Interceptor (X-Tenant-Id)

**Location:** `packages/dash-axios-hook/src/hooks/useAxios.tsx`

Every outgoing API request passes through an interceptor that reads from storage:

```typescript
instance.interceptors.request.use(function (config) {
    const activeTenantId = dashStorage.getItem('active_tenant_id');
    if (activeTenantId) {
        config.headers['X-Tenant-Id'] = activeTenantId;
    }
    return config;
});
```

This ensures all API calls made after a switch target the correct tenant without requiring changes to individual API calls.

---

### 7. Auth Provider Integration

**Location:** `apps/kitchntabs-web/src/dash-extensions/config/DASHAuthProvider.tsx`

The `getIdentity` method respects the switching feature:

```typescript
const activeTenantId = dashStorage.getItem('active_tenant_id');
if (activeTenantId) {
    dashStorage.setItem('tenant_id', activeTenantId);
}
```

This prevents the auth provider from auto-setting `tenant_id` from the user object (which always points to the tenancy), preserving the user's explicit tenant selection.

---

### 8. DashResourceLoader

**Location:** `packages/dash-app-common/src/components/DashResourceLoader.tsx`

Manages lazy loading and caching of resource manifests:

- **`loadResourcesFromManifest(manifest)`** — Resolves all lazy `() => import(...)` entries in parallel, flattens arrays, deduplicates by `model` (last wins), caches in a `WeakMap` keyed by manifest object reference
- **`clearResourceCache(manifest)`** — Removes a specific manifest from the cache, forcing fresh resolution on next load

The loader calls `clearResourceCache` before each load to ensure stale tenant resources are never served from cache.

---

## Switching Sequence (Step by Step)

```
User clicks "Tenant X" in TenantSwitcher dropdown
  │
  ├─ 1.  dashStorage.setItem('active_tenant_id', '123')
  ├─ 2.  GET /auth/tenancyAuth  { headers: { X-Tenant-Id: '123' } }
  ├─ 3.  AuthPersistenceService.saveAuth(response)
  │       └── stores tenantSettings + tenantImages to localStorage
  ├─ 4.  setAuthEvent({ user, auth, token, roles })
  ├─ 5.  updateDomCssVariables(currentMode, colors, values)
  │       ├── reads data-theme attribute → "dark" or "light"
  │       ├── if colors defined → writes suffixed variables + base aliases
  │       └── if colors undefined → reads static LESS defaults → resets to defaults
  ├─ 6.  dispatch(setPanelSettings({ logos }))
  ├─ 7.  AuthPersistenceService.setTenantSettings(tenantSettings)
  ├─ 8.  window.dispatchEvent('tenant_switch', { tenantId: '123', ... })
  │
  └─ PrivateAppLoader receives event
       │
       ├─ 9.  setResources(null)         → loading guard activates
       ├─ 10. setSwitchKey(prev + 1)     → will force remount
       ├─ 11. setTenantContext('123')     → triggers resource effect
       │
       └─ useEffect([tenantContext]) fires
            │
            ├─ 12. import KitchnTabsWebTenantPrivateResources
            ├─ 13. clearResourceCache(manifest)
            ├─ 14. loadResourcesFromManifest(manifest) → 4 resources
            ├─ 15. dispatch(setReduxResources(4 resources))
            ├─ 16. setResources(resolvedArray)
            ├─ 17. setRoutes(mergedRoutes)
            ├─ 18. setIsLoading(false)
            │
            └─ Render phase (key change forces full remount)
                 │
                 ├─ 19. <KitchnTabsWebPrivateApp key="private-app-1" />
                 │       (new key → old instance unmounts, new mounts)
                 │
                 ├─ 20. DashThemeProvider mounts
                 │       ├── AuthPersistenceService.getTenantSettings() → reads new colors
                 │       ├── appTheme(options, { colors, tenantSettings }) → MUI palette
                 │       └── updateDomCssVariables() on mount effect
                 │
                 ├─ 21. DASHAdmin receives customResources (4 items)
                 │       calculateResources() → dispatch(setResources)
                 │
                 ├─ 22. Redux: state.resources.items = [4 items]
                 │
                 ├─ 23. AsyncResources re-renders with 4 resources
                 │
                 └─ 24. AppMaterialMenu re-renders → shows 4 menu items
                        with new tenant's theme colors applied
```

---

## Backend Support

The `AuthController::getTenancyAuth()` endpoint (via `GET /auth/tenancyAuth`) checks for the `X-Tenant-Id` request header:

- **Without header** (tenancy level): Returns auth scoped to the tenancy account, including the list of all associated tenants in `systemValues.tenants`
- **With header** (tenant level): Returns auth scoped to the specified tenant — tenant-specific settings, images, products, and configurations — while still including the tenants list for the switcher dropdown

The tenancy/tenants list is always included in the response regardless of which tenant is active, allowing the `TenantSwitcher` to remain functional at any level.

---

## Configuration

### Enable/Disable

The feature is controlled by the `ENABLE_TENANT_IMPERSONATION` system constant:

```typescript
// dash-constants
DASHAdminSystemConstants.system.ENABLE_TENANT_IMPERSONATION = true;
```

When disabled, `TenantSwitcher` renders `null` and the admin operates purely at tenancy level.

### Auth Endpoint

Configured via environment variable:

```
VITE_APP_GETAUTH_ENDPOINT='auth/tenancyAuth'
```

The switcher always uses this endpoint (rather than toggling between `tenancyAuth` and `getauth`) to ensure the tenancy metadata and tenant list are always preserved in the response.

---

## Key Design Decisions

### 1. Event-Driven Communication

The `TenantSwitcher` communicates with `PrivateAppLoader` via a `CustomEvent` on `window` rather than through React context or props. This decouples the UI component (which lives in the header layout) from the resource orchestrator (which wraps the entire admin app), avoiding prop-drilling through multiple layers.

### 2. Full Remount via Key Prop

Rather than attempting to surgically update react-admin's internal state, a `switchKey` increment forces React to unmount and remount the entire `KitchnTabsWebPrivateApp`. This ensures a clean slate — no stale data provider cache, no orphaned route registrations, no lingering resource state.

### 3. Direct Redux Dispatch from Loader

The loader dispatches resolved resources to Redux before passing them as props to `KitchnTabsWebPrivateApp`. This ensures the `AppMaterialMenu` (which reads from `state.resources.items`) updates immediately rather than waiting for the prop-to-DASHAdmin-to-calculateResources-to-Redux chain.

### 4. Separate Resource Manifests

Tenant-level resources are defined in a **separate manifest** (`KitchnTabsWebTenantPrivateResources`) rather than filtering the base manifest. This provides:
- Clear visibility into what each level exposes
- No accidental resource leakage between levels
- Independent code-splitting per manifest

### 5. UNINITIALIZED Sentinel

The initial `tenantContext` state uses a `Symbol('UNINITIALIZED')` sentinel instead of `null`. This distinguishes "hasn't been read from storage yet" from "tenancy level (no active tenant)", preventing a premature resource load before storage is consulted on page refresh.

### 6. Pre-Request Storage Persistence

The `active_tenant_id` is persisted to `dashStorage` **before** the auth API call. This ensures the axios interceptor (which reads from storage) includes the `X-Tenant-Id` header in the auth request itself, not just in subsequent requests.

---

## Debugging

Comprehensive logging is available via browser console. Key log prefixes:

| Prefix | Source | What It Logs |
|--------|--------|-------------|
| `🔄 PrivateAppLoader:` | KitchnTabsWebPrivateAppLoader | Tenant context changes, manifest loading, resource resolution |
| `📤 PrivateAppLoader:` | KitchnTabsWebPrivateAppLoader | Redux dispatch count and content |
| `📊 DASHAdmin.calculateResources:` | DASHAdmin | Resource calculation details — count, models, `useCoreResources` flag |
| `📤 DASHAdmin:` | DASHAdmin | Resources dispatched to Redux |
| `🔄 DASHAdmin:` | DASHAdmin | `calculateResources` effect triggers |
| `📊 AppMaterialMenu:` | AppMaterialMenu | Resource changes — prev/new count, added/removed models |
| `[TenantSwitcher]` | TenantSwitcher | Switch success/failure, target tenant |

### Expected Log Sequence (Switching to Tenant)

```
[TenantSwitcher] Switched to Pizza Place (123)
🔄 PrivateAppLoader: Tenant switch detected { tenantId: '123', tenantName: 'Pizza Place' }
🔄 PrivateAppLoader: Loading resources (tenant level: true, tenant: 123)...
🔄 PrivateAppLoader: [TENANT] Manifest loaded { tenantKeys: [...] }
✅ PrivateAppLoader: [TENANT] Resolved 4 resources { models: [...], groups: [...] }
📤 PrivateAppLoader: [TENANT] Dispatched 4 resources to Redux
📊 AppMaterialMenu: Resources from Redux { prevCount: 23, newCount: 4, removed: [...] }
🔄 DASHAdmin: calculateResources effect triggered
📊 DASHAdmin.calculateResources: { count: 4, useCoreResources: false, ... }
📤 DASHAdmin: Dispatching 4 resources to Redux
📊 DASHAdmin: Redux resources updated - 4 items
```

---

## Extending Tenant Resources

To add more resources at the tenant level, add entries to `KitchnTabsWebTenantPrivateResources`:

```typescript
// apps/kitchntabs-web/src/resources/KitchnTabsWebTenantPrivateResources.tsx
export const KitchnTabsWebTenantPrivateResources: ResourceManifest = {
    marketplaceResource: () => import('kt-ecommerce/src/resources/marketplaceResource'),
    pointOfSaleResource: () => import('kt-ecommerce/src/resources/pointOfSaleResource'),
    metadataFormatsResource: () => import('kt-ecommerce/src/resources/metadataFormatsResource'),
    campaignResource: () => import('kt-ecommerce/src/resources/campaignResource'),

    // Add new tenant-level resources here:
    // productResource: () => import('kt-ecommerce/src/resources/productResource'),
    // categoryResource: () => import('kt-ecommerce/src/resources/categoryResource'),
};
```

Each entry follows the **ResourceManifest** pattern: a key mapping to a lazy `() => import(...)` function whose default export is an `IDashAutoAdminResourceConfig` (or an array of them).

---
---

# Part 2: Theme Color Switching — Full Technical Documentation

## Overview

When switching between tenancy and tenant levels (or between different tenants), the application's visual theme — colors, backgrounds, borders, sidebar tones, and all themed UI elements — must update dynamically to reflect the active entity's branding. This is accomplished through a multi-layered CSS variable system that bridges LESS compilation, runtime DOM injection, MUI theme generation, and localStorage persistence.

The theme color switching addresses three distinct visual layers:
1. **CSS Custom Properties** — `:root` variables consumed by LESS-compiled component styles (e.g., `var(--primary-color)`)
2. **MUI Theme Palette** — Material UI's `createTheme()` palette used by MUI components
3. **Tenant Branding** — Logos, backgrounds, and other image assets

---

## CSS Variable Architecture

### Variable Naming Convention

All theme-aware CSS variables use a **suffixed** naming pattern:

```
--{variable-name}--{mode}
```

Where `{mode}` is either `light` or `dark`. Examples:
- `--primary-color--dark: #8f00cb`
- `--primary-color--light: #6a0099`
- `--sidebar-bg--dark: #1a1a2e`
- `--module-bg--light: #ffffff`

At runtime, the system also generates **unsuffixed base aliases** that resolve to the current mode:

```
--primary-color: #8f00cb        ← alias for --primary-color--dark (when mode is dark)
--sidebar-bg: #1a1a2e           ← alias for --sidebar-bg--dark
```

These base aliases are what component LESS/CSS actually consumes via `var(--primary-color)`.

### Variable Categories

| Category | Examples | Description |
|----------|----------|-------------|
| **Core palette** | `primary-color`, `secondary-color`, `highlight-color` | Brand colors |
| **Text** | `text-color`, `text-contrast`, `text-light`, `heading-color` | Typography |
| **Backgrounds** | `bodybg-primary`, `module-bg`, `main-bg`, `component-bg` | Surface colors |
| **Sidebar** | `sidebar-bg`, `sidebar-primary`, `sidebar-contrast`, `sidebar_icon` | Navigation panel |
| **Header** | `header-bg`, `header-font`, `header-badge` | Top bar |
| **Borders** | `border-color`, `component-border`, `component-border-split` | Dividers and edges |
| **State** | `component-hover-bg`, `component-active-bg`, `disabled-color` | Interaction states |
| **Links** | `link-color`, `link-hover`, `link-active` | Anchor elements |
| **Alerts** | `alert-error-bg`, `alert-warning-title`, `alert-success-bg` | Notification colors |
| **Buttons** | `btn-bg`, `btn-color` | Button defaults |
| **Layout** | `framed_layout-bg`, `nav-bg`, `scroll_track` | Structural elements |
| **Dimensions** | `sidebar-large-width`, `sidebar-small-width` | CSS dimension values (via `values`) |

### Three Sources of CSS Variables

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CSS VARIABLE SOURCE HIERARCHY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Priority (lowest → highest):                                               │
│                                                                             │
│  1. COMPILED LESS (Static)                                                  │
│     ┌────────────────────────────────────────────────────────────┐          │
│     │ dash-css-transformer.less → Vite LESS compiler             │          │
│     │                                                            │          │
│     │ :root {                                                    │          │
│     │   --primary-color--dark: #8f00cb;   ← from @primary-color │          │
│     │   --primary-color--light: #6a0099;  ← from LESS vars      │          │
│     │   --sidebar-bg--dark: #1a1a2e;      ← ~200+ variables     │          │
│     │   ...                                                      │          │
│     │ }                                                          │          │
│     │                                                            │          │
│     │ Loaded via <link> or <style> in <head>                     │          │
│     │ Contains ONLY suffixed variables (--key--light, --key--dark)│          │
│     │ Unsuffixed variables are COMMENTED OUT                     │          │
│     └────────────────────────────────────────────────────────────┘          │
│                                                                             │
│  2. DYNAMIC TENANT OVERRIDES (Runtime)                                      │
│     ┌────────────────────────────────────────────────────────────┐          │
│     │ <style id="dash-theme-variables">                          │          │
│     │                                                            │          │
│     │ :root {                                                    │          │
│     │   --primary-color--dark: #ff5722;   ← tenant override     │          │
│     │   --primary-color: #ff5722;         ← base alias          │          │
│     │   --sidebar-bg--dark: #2d1b4e;      ← tenant override     │          │
│     │   --sidebar-bg: #2d1b4e;            ← base alias          │          │
│     │   ...                                                      │          │
│     │ }                                                          │          │
│     │                                                            │          │
│     │ Positioned at END of <head> via appendChild()              │          │
│     │ HIGHEST cascade priority — overrides compiled LESS         │          │
│     │ Contains BOTH suffixed AND unsuffixed (base alias) vars    │          │
│     └────────────────────────────────────────────────────────────┘          │
│                                                                             │
│  3. MUI THEME (JavaScript)                                                  │
│     ┌────────────────────────────────────────────────────────────┐          │
│     │ appTheme() → createTheme() → <ThemeProvider theme={...}>   │          │
│     │                                                            │          │
│     │ palette: {                                                 │          │
│     │   primary: { main: "#ff5722" },     ← from _color() helper│          │
│     │   secondary: { main: "#FFB366" },                          │          │
│     │   background: { default: "#1a1a2e" },                      │          │
│     │   ...                                                      │          │
│     │ }                                                          │          │
│     │                                                            │          │
│     │ MUI components read from theme object,                     │          │
│     │ LESS-compiled components read from CSS variables            │          │
│     └────────────────────────────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. dash-css-transformer.less (Static CSS Variables)

**Location:** `packages/dash-styles/src/dash-css-transformer.less` (~543 lines)

The LESS file that defines all CSS custom properties at the `:root` level. It is imported by each app's `vite.config.mts` via the LESS `additionalData` directive:

```javascript
// vite.config.mts
css: {
    preprocessorOptions: {
        less: {
            additionalData: `
                @import "../../../packages/dash-styles/src/dash-css-transformer.less";
            `
        }
    }
}
```

#### Structure

The file has three sections:

1. **Commented-out unsuffixed defaults** (lines 7–131) — These are intentionally inactive. If enabled, they would prevent theme switching because they create base aliases at compile time that can't be overridden by the dynamic style.

2. **Light-mode suffixed variables** (lines ~132–260):
```less
--primary-color--light: @primary-color;
--primary-contrast--light: @primary-contrast;
--secondary-color--light: @secondary-color;
--module-bg--light: @module-bg;
// ... ~60 variables
```

3. **Dark-mode suffixed variables** (lines ~261–400):
```less
--primary-color--dark: @primary-color--dark;
--primary-contrast--dark: @primary-contrast--dark;
--secondary-color--dark: @secondary-color--dark;
--module-bg--dark: @module-bg--dark;
// ... ~60 variables
```

4. **Unsuffixed base colors** (lines ~400–543) — Color constants that are mode-independent:
```less
--info-color: @info-color;
--dash-blue: @dash-blue;
--dash-red: @dash-red;
// ... etc
```

#### Key Behavior

- LESS variables (e.g., `@primary-color--dark`) are compiled at build time into static hex values
- The compiled CSS is injected into `<head>` as a `<style>` or `<link>` element
- These compiled values serve as the **baseline defaults** for the application
- They appear BEFORE the dynamic `<style id="dash-theme-variables">` in the DOM, so they can be overridden

---

### 2. updateDomCssVariables() (Runtime CSS Injection)

**Location:** `packages/dash-utils/src/utils/updateDomCssVariables.tsx` (176 lines)
**Copy:** `packages/dash-admin/src/default-theme/updateDomCssVariables.tsx` (kept in sync)

The core function that injects tenant-specific CSS variables into the DOM at runtime.

#### Signature

```typescript
export const updateDomCssVariables = (
    theme: string,                           // "dark" or "light"
    colors?: { [x: string]: string },        // Tenant color overrides (suffixed keys)
    values?: { [x: string]: string }         // Tenant dimension values (unsuffixed)
) => void;
```

#### Algorithm

```
updateDomCssVariables("dark", colors, values)
  │
  ├─ 1. Find or create <style id="dash-theme-variables">
  │
  ├─ 2. ALWAYS move to end of <head> via appendChild()
  │     └─ Ensures highest CSS cascade priority
  │
  ├─ 3. If colors is undefined → read static LESS defaults
  │     └─ getStaticCssVariables() → iterates all stylesheets
  │        EXCEPT the dynamic style element → returns compiled :root vars
  │
  ├─ 4. Collect all variable keys from colors or static vars
  │
  ├─ 5. For each key:
  │     ├─ Resolve value: colors[key] → staticVars[--key] → getCssVarFromDom(key)
  │     ├─ Include only current-theme suffixed vars or non-theme vars
  │     └─ If key ends with --{theme}: also generate base alias
  │        e.g., --primary-color--dark → also set --primary-color
  │
  └─ 6. Write to DOM: themeStyleElement.textContent = `:root { ${styleString} }`
```

#### Helper Functions

| Function | Purpose |
|----------|---------|
| `getCssVarFromDom(key)` | Reads a single CSS variable from `getComputedStyle(document.documentElement)` — last-resort fallback |
| `getAllCSSVariableNames(styleSheets)` | Lists all `--` prefixed property names across all stylesheets |
| `getStaticCssVariables()` | Reads `:root` variables from all stylesheets **except** `dash-theme-variables` — returns the compiled LESS defaults without contamination from previous tenant overrides |

#### Critical Design: CSS Cascade Priority

The `<style id="dash-theme-variables">` element is always positioned at the **end** of `<head>` via `appendChild()`. In CSS cascade rules, when two selectors have equal specificity (both target `:root`), the one appearing **later** in source order wins. This ensures tenant-specific values override the compiled LESS defaults.

```html
<head>
    <style> /* Compiled LESS: --primary-color--dark: #8f00cb */ </style>
    <link rel="stylesheet" href="/assets/app.css" />
    <!-- ... other styles ... -->
    <style id="dash-theme-variables">
        :root { --primary-color--dark: #ff5722; --primary-color: #ff5722; }
    </style>  <!-- ← LAST = WINS -->
</head>
```

#### Handling Missing Colors (Reset to Defaults)

When switching to a tenant that has NOT configured custom colors, `colors` will be `undefined`. The function handles this gracefully:

1. `getStaticCssVariables()` reads the compiled LESS CSS defaults (skipping `dash-theme-variables` to avoid reading stale values from the previous tenant)
2. These static default values are written into `dash-theme-variables`, effectively resetting the visual theme
3. Base aliases are regenerated from the static defaults for the current mode

This ensures a clean visual reset — the previous tenant's colors are completely replaced.

---

### 3. appTheme() and _color() (MUI Theme Builder)

**Location:** `packages/dash-styles/src/index.tsx` (~733 lines)

Builds the MUI theme configuration consumed by `<ThemeProvider>`.

#### _color() Helper

The bridge between tenant colors and MUI palette values:

```typescript
const _color = (key, colorKey, mode = null) => {
    if (colors) {
        // Path A: Use tenant-specific colors (from API response)
        const colorValue = colors[`${colorKey}--${mode || currentTheme}`];
        return colorValue ? { [key]: colorValue } : {};
    } else if (cssVars[`--${colorKey}--${mode || currentTheme}`]) {
        // Path B: Use compiled LESS CSS variable defaults
        const cssVarValue = cssVars[`--${colorKey}--${mode || currentTheme}`];
        return cssVarValue ? { [key]: cssVarValue } : {};
    } else {
        return {};
    }
};
```

**Resolution priority:**
1. `colors` parameter → direct tenant override from API (e.g., `colors["primary-color--dark"]`)
2. `cssVars` fallback → read from `getAllCssVariablesFromStyleSheets(":root")` — compiled LESS defaults

#### getAllCssVariablesFromStyleSheets()

Reads all CSS variables from `:root` rules across all stylesheets, **skipping** the `dash-theme-variables` dynamic element:

```typescript
const getAllCssVariablesFromStyleSheets = (selector: string) => {
    // ...
    for (let i = 0; i < document.styleSheets.length; i++) {
        const styleSheet = document.styleSheets[i];
        // Skip dynamic theme element to read only compiled/static defaults
        if ((styleSheet.ownerNode as HTMLElement)?.id === 'dash-theme-variables') continue;
        // ... collect `:root` variables ...
    }
    return cssVariables;
};
```

This skip is critical: without it, `_color()` fallback would read the *previous* tenant's colors from the dynamic style element instead of the compiled defaults, causing stale colors when switching to a tenant without custom colors.

#### Palette Construction

`createPalette(mode)` maps CSS variable keys to MUI palette structure:

```
CSS Variable Key          → MUI Palette Path
─────────────────────────   ──────────────────
primary-color--{mode}     → palette.primary.main
primary-contrast--{mode}  → palette.primary.contrastText
secondary-color--{mode}   → palette.secondary.main
module-bg--{mode}         → palette.background.default
text-color--{mode}        → palette.text.primary
alert-error-bg--{mode}    → palette.error.main
component-hover-bg--{mode}→ palette.action.hover
...
```

---

### 4. DashThemeContext / DashThemeProvider (MUI Theme Wrapper)

**Location:** `packages/dash-admin/src/default-theme/DashThemeContext.tsx` (~171 lines)

Wraps the entire app in MUI's `<ThemeProvider>` and manages theme state.

#### Context Value

```typescript
interface DashThemeContextType {
    theme: Theme;                                          // MUI Theme object
    themeOptions: ReturnType<typeof appTheme>;              // Raw theme options
    recreateTheme: (tenantSettings?: any) => void;         // Force theme rebuild
    currentMode: string;                                   // "dark" or "light"
}
```

#### Initialization (Flash Prevention)

On mount, both `themeOptions` and `theme` useState initializers read persisted tenant settings:

```typescript
const [themeOptions, setThemeOptions] = useState(() => {
    const initialTenantSettings = AuthPersistenceService.getTenantSettings();
    return appTheme(extendedOptions, {
        currentMode,
        colors: initialTenantSettings?.colors,
        tenantSettings: initialTenantSettings,
    });
});
```

This prevents a "flash of default colors" on page refresh — the very first render already has the correct tenant palette.

#### Theme Recreation

The `recreateTheme()` method is called when colors need to update:

```typescript
const recreateTheme = (tenantSettings?: any, mode?: string) => {
    const settings = tenantSettings || getTenantSettings();
    const themeMode = mode || document.documentElement.getAttribute('data-theme') || 'dark';
    
    const newThemeOptions = appTheme(extendedOptions, {
        tenantSettings: settings,
        colors: settings?.colors,
        currentMode: themeMode,
    });
    
    const newTheme = createTheme(newThemeOptions);
    setThemeOptions(newThemeOptions);
    setTheme(newTheme);
    updateDomCssVariables(themeMode, settings?.colors, settings?.values);
};
```

#### Event Listeners

| Trigger | Effect |
|---------|--------|
| `data-theme` attribute mutation | `MutationObserver` detects mode change → `recreateTheme()` with new mode |
| `currentMode` state change | Effect fires → `recreateTheme()` |
| Initial mount | Effect reads `getTenantSettings()` → `recreateTheme()` |
| `DASHTRefreshTheme` custom event | Handler fires → `recreateTheme()` |

---

### 5. AuthPersistenceService (Persistence Layer)

**Location:** `packages/dash-auth/src/AuthPersistanceService.tsx` (~463 lines)

Manages tenant settings persistence in localStorage.

#### Key Methods

| Method | Purpose |
|--------|---------|
| `saveAuth(authData)` | Persists full auth response; stores `tenantSettings` and `tenantImages` as separate localStorage keys |
| `getTenantSettings()` | Returns `JSON.parse(localStorage.getItem('dash_tenant_settings'))` or null |
| `setTenantSettings(settings)` | Stores settings to `dash_tenant_settings` localStorage key |
| `getTenantImages()` | Returns persisted tenant images |
| `setTenantImages(images)` | Stores tenant images |

#### Data Shape

```typescript
// tenantSettings (from auth.tenantSettings)
{
    colors: {                              // Optional — only present when tenant has custom colors
        "primary-color--dark": "#ff5722",
        "primary-color--light": "#e64a19",
        "secondary-color--dark": "#FFB366",
        "sidebar-bg--dark": "#2d1b4e",
        // ... ~100+ suffixed color variables
    },
    values: {                              // Optional — CSS dimension values
        "sidebar-large-width": "255px",
        "sidebar-small-width": "64px",
    },
    primary_currency: { ... },
    primary_language: { ... },
    // ... other non-visual settings
}
```

---

### 6. injectTenantStyles() (Bootstrap Injection)

**Location:** Module-level code in app entry points:
- `apps/kitchntabs-web/src/KitchnTabsWebAppWithProviders.tsx`
- `apps/kitchntabs-web/src/DashAppComponent.tsx`

Called **once at module load time** (before React renders) to inject persisted tenant colors from localStorage. This provides immediate visual theming before the React tree mounts:

```typescript
const injectTenantStyles = () => {
    const tenantSettings = AuthPersistenceService.getTenantSettings();
    if (tenantSettings) {
        try {
            const colors = tenantSettings.colors;
            const currentMode = document.documentElement.getAttribute('data-theme')
                || DASHLayoutSettings.THEME_TYPE_DARK;
            updateDomCssVariables(currentMode, colors, tenantSettings.values);
        } catch (error) {
            console.error('Error parsing tenant settings:', error);
        }
    }
};
injectTenantStyles();
```

This ensures that even during the initial React render (before any effects fire), the CSS variables are already set correctly from the last known tenant.

---

## Backend: Tenant Color Configuration

### Auth Endpoint Response

The backend `AuthController::getTenancyAuth()` builds `tenantSettings` from the raw `settings` JSON column on the `tenants` table:

```php
// AuthController.php
$tenantSettings = (array) $tenant->settings;  // Raw DB JSON column
$tenantSettings['primary_currency'] = $currency;
$tenantSettings['primary_language'] = $language;
$tenantSettings = (object) $tenantSettings;

$auth = [
    "tenantSettings" => $tenantSettings,      // Contains colors IF tenant has saved them
    "tenantImages" => $tenant->getTenantImages(),
];
```

#### Important: `$tenant->settings` vs `$tenant->setting('colors')`

| Access Pattern | Behavior |
|----------------|----------|
| `$tenant->settings` | Raw JSON column cast to array — **no default merging** |
| `$tenant->setting('colors')` | Method with `default_value` fallback from `config/tenants.php` |

The auth endpoint uses the raw property access, meaning:
- **Tenants with saved colors** → `tenantSettings.colors` contains `{ "primary-color--dark": "#hex", ... }`
- **Tenants WITHOUT saved colors** → `tenantSettings.colors` is `undefined` (key absent from JSON)

The frontend handles the `undefined` case by resetting to compiled LESS defaults (see `updateDomCssVariables` section above).

### Color Configuration Storage

Colors are stored in the `tenants.settings` JSON column under the `colors` key:

```json
{
    "colors": {
        "bodybg-primary--light": "#ffffffff",
        "bodybg-secondary--light": "#ecececff",
        "primary-color--light": "#8f00cb",
        "primary-color--dark": "#bb86fc",
        "primary-contrast--light": "#00044c",
        "primary-contrast--dark": "#ffffff",
        "secondary-color--light": "#FFB366",
        "secondary-color--dark": "#FF9933"
        // ... ~100+ variables for both light and dark modes
    },
    "values": {
        "sidebar-large-width": "255px",
        "sidebar-small-width": "64px"
    }
}
```

### Config Defaults

Default color values are defined in `config/tenants.php` under the `theme_colors` setting format:

```php
[
    'id'            => 'theme_colors',
    'group'         => 'colors',
    'attribute'     => 'settings.colors',
    'type'          => 'custom',
    'component'     => 'JsonColorSelector',
    'default_value' => [
        "bodybg-primary--light" => "#ffffffff",
        "primary-color--light" => "#8f00cb",
        "primary-color--dark" => "#bb86fc",
        // ... 100+ color variables
    ],
],
```

These defaults are used by the `JsonColorSelector` UI component and the `$tenant->setting('colors')` method, but are **not** merged into the auth endpoint response automatically.

---

## Complete Theme Color Switching Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   THEME COLOR SWITCHING FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌────────────────────┐                                                    │
│   │ User Clicks Switch │                                                    │
│   │ in TenantSwitcher  │                                                    │
│   └─────────┬──────────┘                                                    │
│             │                                                               │
│             ▼                                                               │
│   ┌────────────────────────────────────────────────────────┐                │
│   │  1. API: GET /auth/tenancyAuth                         │                │
│   │     Header: X-Tenant-Id: {tenantId}                    │                │
│   └─────────┬──────────────────────────────────────────────┘                │
│             │                                                               │
│             ▼                                                               │
│   ┌────────────────────────────────────────────────────────┐                │
│   │  BACKEND: AuthController::getTenancyAuth()             │                │
│   │                                                        │                │
│   │  $tenant = Tenant::find($requestedTenantId);           │                │
│   │  $tenantSettings = (array) $tenant->settings;          │                │
│   │                                                        │                │
│   │  Returns: {                                            │                │
│   │    auth: {                                             │                │
│   │      tenantSettings: {                                 │                │
│   │        colors: { "primary-color--dark": "#ff5722",..}  │  ← or absent  │
│   │        values: { "sidebar-large-width": "255px" }      │                │
│   │      },                                                │                │
│   │      tenantImages: { horizontal_logo, squared_logo }   │                │
│   │    }                                                   │                │
│   │  }                                                     │                │
│   └─────────┬──────────────────────────────────────────────┘                │
│             │                                                               │
│             ▼                                                               │
│   ┌────────────────────────────────────────────────────────┐                │
│   │  2. PERSIST: AuthPersistenceService.saveAuth()         │                │
│   │     → localStorage['dash_tenant_settings'] = settings  │                │
│   │     → localStorage['dash_tenant_images'] = images      │                │
│   └─────────┬──────────────────────────────────────────────┘                │
│             │                                                               │
│             ▼                                                               │
│   ┌────────────────────────────────────────────────────────┐                │
│   │  3. UPDATE CSS: updateDomCssVariables(mode, colors, v) │                │
│   │                                                        │                │
│   │  mode = document.documentElement.data-theme ("dark")   │                │
│   │                                                        │                │
│   │  IF colors defined:                                    │                │
│   │    → Write tenant colors to <style> element            │                │
│   │    → Generate base aliases (--key from --key--dark)     │                │
│   │                                                        │                │
│   │  IF colors undefined:                                  │                │
│   │    → getStaticCssVariables() reads compiled LESS       │                │
│   │    → Write static defaults to <style> element          │                │
│   │    → Effectively resets to framework defaults           │                │
│   │                                                        │                │
│   │  <style id="dash-theme-variables"> at END of <head>    │                │
│   │  :root { --primary-color--dark: #ff5722;               │                │
│   │          --primary-color: #ff5722; ... }                │                │
│   └─────────┬──────────────────────────────────────────────┘                │
│             │                                                               │
│             ├──── LESS-compiled components now see new colors               │
│             │     via var(--primary-color), var(--sidebar-bg), etc.         │
│             │                                                               │
│             ▼                                                               │
│   ┌────────────────────────────────────────────────────────┐                │
│   │  4. REMOUNT: PrivateAppLoader increments switchKey     │                │
│   │     → DashThemeProvider remounts                       │                │
│   │     → Reads AuthPersistenceService.getTenantSettings() │                │
│   │     → appTheme({ colors, tenantSettings }) builds MUI  │                │
│   │     → _color("main","primary-color","dark")            │                │
│   │       → colors["primary-color--dark"] → "#ff5722"      │                │
│   │     → createTheme({ palette: { primary: {main:#ff5722}}│                │
│   │     → <ThemeProvider theme={newTheme}>                  │                │
│   └─────────┬──────────────────────────────────────────────┘                │
│             │                                                               │
│             ├──── MUI components now see new palette values                 │
│             │                                                               │
│             ▼                                                               │
│   ┌────────────────────────────────────────────────────────┐                │
│   │  5. UPDATE LOGOS                                       │                │
│   │     dispatch(setPanelSettings({                        │                │
│   │       horizontalLogo, squaredLogo, loginBackground     │                │
│   │     }))                                                │                │
│   │     → Header, sidebar, login page reflect new branding │                │
│   └────────────────────────────────────────────────────────┘                │
│                                                                             │
│   RESULT: All visual elements now reflect the new tenant's theme           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Light/Dark Mode Switching Flow

The theme mode (light/dark) operates independently of tenant switching but shares the same CSS variable infrastructure.

### Mode Storage

The current mode is stored in the `data-theme` attribute on `<html>`:

```html
<html data-theme="dark">
```

### Mode Change Flow

```
User toggles light/dark mode
  │
  ├─ 1. Update: document.documentElement.setAttribute('data-theme', 'light')
  │
  ├─ 2. MutationObserver in DashThemeProvider fires
  │     └─ setCurrentMode('light')
  │
  ├─ 3. useEffect([currentMode]) fires → recreateTheme(settings, 'light')
  │     ├─ appTheme({ colors, currentMode: 'light' })
  │     │   └─ _color() reads colors["primary-color--light"] instead of --dark
  │     ├─ createTheme(newThemeOptions)
  │     └─ updateDomCssVariables('light', colors, values)
  │         └─ Regenerates base aliases from --light suffixed vars
  │            e.g., --primary-color = value of --primary-color--light
  │
  └─ 4. UI updates:
        ├─ CSS components: var(--primary-color) now resolves to light value
        └─ MUI components: palette.primary.main now has light value
```

### Interaction with Tenant Colors

When both mode change and tenant switch occur, the system handles them correctly because:
- The mode is always read dynamically from `data-theme` (never hardcoded)
- The suffix system (`--dark` / `--light`) ensures both modes are always available in the colors map
- `updateDomCssVariables()` only generates base aliases for the **current** mode's suffixed variables

---

## Bugs Fixed (Historical Reference)

The following bugs were identified and fixed during the theme switching implementation:

### Bug 1: CSS Cascade Priority (Critical)

**Problem:** `<style id="dash-theme-variables">` was inserted at `document.head.firstChild` (lowest cascade priority). The compiled LESS CSS loaded later in `<head>` had higher priority, silently overwriting tenant-specific suffixed variables.

**Fix:** Changed from `insertBefore(themeStyleElement, document.head.firstChild)` to `document.head.appendChild(themeStyleElement)` — positions the style at the end of `<head>` for highest cascade priority.

### Bug 2: Static/Dynamic Variable Contamination

**Problem:** `getAllCssVariablesFromStyleSheets()` iterated ALL stylesheets including `dash-theme-variables`. When `_color()` fell back to CSS variables for a tenant without custom colors, it read the *previous* tenant's values from the dynamic style instead of the compiled defaults.

**Fix:** Added `if ((styleSheet.ownerNode as HTMLElement)?.id === 'dash-theme-variables') continue;` to skip the dynamic element. Also added `getStaticCssVariables()` helper in `updateDomCssVariables.tsx` with the same skip logic.

### Bug 3: Missing Colors Not Resetting

**Problem:** `TenantSwitcher` had `if (tenantSettings?.colors) { updateDomCssVariables(...) }` — when switching to a tenant without custom colors (`colors` undefined), the function was never called, leaving the previous tenant's colors visible.

**Fix:** Removed the guard. `updateDomCssVariables` is now always called. When `colors` is undefined, `getStaticCssVariables()` reads compiled LESS defaults and resets the visual theme.

### Bug 4: Hardcoded Dark Mode

**Problem:** `TenantSwitcher` and `injectTenantStyles()` used `DASHLayoutSettings.THEME_TYPE_DARK` (hardcoded `"dark"`) as the theme parameter, ignoring the actual current mode from `data-theme`.

**Fix:** Changed to `document.documentElement.getAttribute('data-theme') || DASHLayoutSettings.THEME_TYPE_DARK` — reads the actual current mode.

### Bug 5: Flash of Default Colors on Mount

**Problem:** `DashThemeContext` initial state did not include tenant colors — `appTheme(extendedOptions, { currentMode })` without colors. This caused a flash of default framework colors before the mount effect ran `recreateTheme()`.

**Fix:** Initial `useState` now reads `AuthPersistenceService.getTenantSettings()` and passes `colors` and `tenantSettings` to `appTheme()` immediately.

---

## Debugging

### Theme-Specific Logs

| Log | Source | What It Logs |
|-----|--------|-------------|
| `Updating colors from local storage, mode: {mode}` | `injectTenantStyles()` | Bootstrap CSS injection at module load time |
| `Recreating MUI theme with tenant settings:` | `DashThemeContext.recreateTheme()` | Full tenant settings object and mode being applied |
| `Theme mode changed from {old} to {new}` | `DashThemeContext` (MutationObserver) | Light/dark mode toggle detected |
| `Updating theme with new mode:` | `DashThemeContext` | Mode change triggering CSS variable update |
| `Current mode updated to:` | `DashThemeContext` | `currentMode` state effect fired |
| `Recreating MUI theme on mount` | `DashThemeContext` | Initial theme build on component mount |
| `[TenantSwitcher] Error updating CSS variables:` | `TenantSwitcher` | CSS variable injection failure |

### Debug Mode in updateDomCssVariables

Set `debug = true` in `updateDomCssVariables()` to enable per-variable logging:

```typescript
const debug = true; // Set to true for development
```

This outputs colored console logs for specific tracked variables (configurable via `logKeys` array):

```
⬤ --framed_layout-bg--dark: #1a1a2e;
⬤ [DEFAULT][--dark] --framed_layout-bg: #1a1a2e;
STYLES --primary-color--dark: #ff5722; --primary-color: #ff5722; ...
```

### Verifying CSS Variable State

In browser DevTools:

```javascript
// Check the dynamic style element position
document.getElementById('dash-theme-variables')

// Check computed value of a specific variable
getComputedStyle(document.documentElement).getPropertyValue('--primary-color')

// List all current CSS variables from the dynamic element
document.getElementById('dash-theme-variables').textContent

// Check current theme mode
document.documentElement.getAttribute('data-theme')

// Check persisted tenant settings
JSON.parse(localStorage.getItem('dash_tenant_settings'))
```

---

## Known Limitations

1. **Other app variants**: `apps/kitchntabs/src/DashAppComponent.tsx`, `apps/kitchntabs-system/src/DashAppComponent.tsx`, and `apps/kitchntabs-system/src/KitchnTabsWebAppWithProviders.tsx` still use hardcoded `THEME_TYPE_DARK` in their `injectTenantStyles()` functions. These should be updated to read from `data-theme` for full light/dark mode support.

2. **Backend color defaults not merged**: The `getTenancyAuth()` endpoint returns raw `$tenant->settings` without merging defaults from `config/tenants.php`. This means tenants that have never saved custom colors get `undefined` for the `colors` key. The frontend handles this gracefully by resetting to compiled LESS defaults, but it means the admin's default colors (from config) are not applied — only the framework's LESS-compiled defaults are.

3. **Two copies of updateDomCssVariables**: The file exists in both `dash-utils` and `dash-admin` packages. Changes must be applied to both copies. Consider consolidating to a single source of truth.
