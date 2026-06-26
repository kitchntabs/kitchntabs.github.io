# Tenant Configuration Settings Module Documentation

This document outlines the architecture, interdependencies, and workflow of the Tenant Configuration Settings module in the Dash ecosystem.

## 1. Architecture Overview

The Tenant Settings module allows for dynamic configuration of tenant-specific properties (settings, themes, colors, contact info) driven by a backend configuration. This "Backend-Driven UI" approach ensures that adding new settings does not always require frontend code changes.

### Key Components

1.  **Backend (`dash-backend`)**:
    *   **Source of Truth**: `config/tenants.php` defines the schema for all settings (type, label, validation rules, visibility, tabs).
    *   **API Endpoint**: `system/tenant/systemSettingFormats` (or similar) exposes this configuration to the frontend.
    *   **Data Storage**: Tenant settings are stored as JSON in the database (typically in a `settings` column on the `tenants` table).

2.  **Frontend (`dash-admin`)**:
    *   **Context Layer**: `SystemRequestsCache.tsx` (and legacy `TenantSettingsContext.tsx`) caches the configuration from the API to avoid redundant network requests.
    *   **Presentation Layer**:
        *   `TenantSettings.tsx`: Renders the "generic" settings form.
        *   `TenantTheme.tsx`: Renders the "theme/color" settings form.
        *   `TenantAttributes.tsx`: Renders contact/attribute information.
    *   **Schema Definition**: `tenant_superadmin.tsx` integrates these components into the main Tenant resource view in `react-admin`.

## 2. Interdependencies

The module relies on several inter-connected parts:

*   **`dash-auto-admin`**: The underlying library that renders form inputs based on the schema objects (e.g., `DashAutoFormTabs`, `DashAutoFormGroups`).
*   **`SystemRequestsCache`**: A critical context provider that manages fetching and caching (in memory and IndexedDB) of system-wide configurations, including tenant setting formats.
*   **`TenantSettingsContext`**: A specific usage of the caching mechanism for tenant settings (note: seems to be transitioning to using the more generic `SystemRequestsCache`).
*   **`react-hook-form`**: Used for form state management within the components.

## 3. How It Works (Data Flow)

1.  **Configuration Definition**: Developers define setting fields in `config/tenants.php` in the backend. Each field has properties like `id`, `tab`, `type` (boolean, string, color), `default_value`, etc.
2.  **API Consumption**:
    *   The frontend `SystemRequestsCacheProvider` fetches `config/tenants.php` data via the API on app load (or on demand).
    *   It caches this data in IndexedDB (`SystemRequestsCacheDB`) to speed up subsequent loads.
3.  **Component Rendering**:
    *   **Tenant Load**: When opening a Tenant record, `react-admin` fetches the tenant data (including current `settings` values).
    *   **Schema Load**: `TenantSettings` and `TenantTheme` subscribe to `useSystemRequestsCache()` to get the *format* definitions.
    *   **Filtering**:
        *   `TenantSettings` filters for items where `tab !== 'colors'`.
        *   `TenantTheme` filters for items where `tab === 'colors'`.
    *   **Form Generation**: `DashAutoFormTabs` (from `dash-auto-admin`) takes the merged data (Schema + Values) and renders the appropriate input fields.

## 4. How to Add More Settings

To add a new setting, you generally **only need to touch the Backend**.

### Step 1: Update Backend Configuration

Open `dash-backend/config/tenants.php`.

Add a new array item to the `setting_formats` array:

```php
[
    'id'            => 'new_feature_enabled',      // Unique key for the setting
    'group'         => 'features',                 // Logical grouping (visual)
    'tab'           => 'general',                  // 'colors' for Theme tab, others for Config tab
    'attribute'     => 'settings.new_feature',     // Dot notation path in the JSON column
    'label'         => 'Enable New Feature',       // User-facing label
    'visible'       => true,
    'required'      => false,
    'type'          => 'boolean',                  // 'boolean', 'string', 'integer', 'color', etc.
    'editable'      => true,
    'default_value' => false,
    'description'   => 'Toggles the new feature.',
],
```

### Step 2: (Optional) Frontend Customization

If your new setting requires a completely custom UI component that `dash-auto-admin` doesn't support by default:

1.  Define a new `custom` setting in `config/tenants.php`:
    ```php
    'type' => 'custom',
    'component' => 'MyNewComponent'
    ```
2.  Register/Handle `MyNewComponent` within the `dash-auto-admin` mapping or the `TenantSettings` renderer (this part depends on how `DashAutoForm` resolves custom components, usually via a registry or switch case).

### Step 3: Verify

1.  Reload the frontend (to clear the IndexedDB cache or wait for cache expiry).
2.  Navigate to the Tenant configuration.
3.  The new field should appear automatically in the correct tab.

## 5. Troubleshooting

*   **Changes not showing up?**: The frontend heavily caches these schemas. Try clearing your browser's Application Storage (IndexedDB > SystemRequestsCacheDB) or force a hard reload.
*   **Validation Errors**: Ensure frontend validation rules (if any) match the backend rules defined in the config.
