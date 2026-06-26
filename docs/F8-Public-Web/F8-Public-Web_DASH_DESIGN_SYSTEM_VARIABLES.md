
# Dash Design System: Color & Theme Architecture

## Overview

The Dash Design System has transitioned to a **CSS Variable-first architecture**. We have fully deprecated the reliance on LESS variables for color values. While LESS is still used for structural CSS generation and nesting, all dynamic values (colors, spacing, typography) are now driven exclusively by native CSS custom properties (`var(--name)`).

This architecture allows for:
1.  **Instant Runtime Theming**: Switching themes or updating tenant colors without page reloads.
2.  **Domain/Tenant Overrides**: Public apps can injection specific color palettes via API.
3.  **Light/Dark Mode**: Handled natively via variable swapping in the DOM.

---

## 1. **Core Philosophy: "CSS Vars are Truth"**

The "Single Source of Truth" for any color is now the CSS variable in the DOM, **not** the LESS variable.

*   **Deprecated:** `background: @primary-color;`
*   **Active Standard:** `background: var(--primary-color);`

### Variable Naming Convention
*   **Base Variable:** `var(--primary-color)` - The active value used in components.
*   **Mode-Specific Defaults:** `var(--primary-color--light)` and `var(--primary-color--dark)`.

---

## 2. **Architecture Layers**

### Layer 1: Static Defaults (`dash-variables.less`)
Defines the fallback values for all variables. These are compiled into the CSS but often overridden at runtime.
*   Located in: `apps/[app-name]/src/dash-variables.less`
*   **Role**: Provides the "factory default" look if no Javascript injection happens.

### Layer 2: CSS Transformer (`dash-css-transformer.less`)
Use `dash-styles` to generate the initial `:root` block.
*   Maps LESS variables to CSS properties with mode suffixes.
*   Example output:
    ```css
    :root {
      --primary-color--light: #8f00cb;
      --primary-color--dark: #F3F0FF;
    }
    ```

### Layer 3: Runtime Injection (`updateDomCssVariables.ts`)
This is the engine of the system. It reads the specific mode values (e.g., `--light`) and assigns them to the base variables.
*   **Function**: `updateDomCssVariables(theme, overrides, defaults)`
*   **Action**: Generates a `<style id="dash-theme-variables">` block in `<head>`.
*   **Logic**:
    *   If Theme = 'light', it reads `primary-color--light`.
    *   It writes `--primary-color: [value]` to the style block.

---

## 3. **The `getSessionAuth` Flow**

For apps like `kitchntabs-web` or `kitchntabs-app` (Kiosk), the theming is dynamic based on the loaded Tenant.

1.  **Boot**: App loads with defaults from `dash-variables.less`.
2.  **Auth/Config Fetch**: App calls `/getSessionAuth` or similar endpoint.
3.  **Response**: API returns `tenantSettings.colors` (JSON object).
4.  **Injection**: The app MUST call `updateDomCssVariables('light', apiColors)` to apply them.
5.  **Result**: The UI updates instantly as `--primary-color` changes value in the DOM.

---

## 4. **How to Debug**

If a color is not applying (e.g., Dialog header is Purple instead of Green):

1.  **Inspect the Element**: verifying it uses `var(--variable-name)`.
2.  **Check Computed Styles**: What is the resolved value of that variable?
3.  **Check `<head>`**: Look for `<style id="dash-theme-variables">`.
    *   Does it exist?
    *   Does it contain the variable definition? (e.g., `--primary-color: #34831b;`)
    *   Is it at the bottom of `<head>` (highest priority)?
4.  **Check `injectTenantStyles`**: Ensure this function is called *after* new settings are fetched.

---

## 5. **MUI ThemeProvider Wrapping Requirement**

CSS variables control **CSS styling** (backgrounds, borders, gradients). But MUI buttons and components 
get their colors from the JavaScript **MUI palette** (`palette.primary.main`), NOT from CSS variables 
directly. This palette is set inside a `ThemeProvider`.

**If a MUI component renders OUTSIDE any `ThemeProvider`, it will use MUI's default blue `#1976d2`.**

### Common Pitfall: Error Screens

Wrapper components like `SelfServiceClientWrapper` may render error states (e.g., `DashInfo`) 
BEFORE the child app (which contains the `ThemeProvider`) mounts:

```
SelfServiceAppLoader
  └─ DashThemeProviderLight        ← MUST wrap here
      └─ SelfServiceClientWrapper  ← Error DashInfo renders here
          └─ KitchnTabsPrivateApp  ← ThemeProvider is here (never reached on error)
```

**Fix**: Wrap the outermost component with `DashThemeProviderLight` so that all children
(including error screens) inherit a properly themed MUI palette.

### `DashThemeProviderLight` Palette Priority

The lightweight theme provider reads CSS variables and maps them to MUI palette:
- `palette.primary.main` ← `--btn-bg--{mode}` (button color), fallback to `--primary-color--{mode}`
- `palette.primary.contrastText` ← `--btn-color--{mode}`, fallback to `--primary-contrast--{mode}`

This matches the behavior of the full theme provider in `dash-styles/src/index.tsx`.

---

## 6. **Adding New Variables**

1.  **Define in LESS**: Add to `dash-variables.less` with `--light` and `--dark` suffixes.
2.  **Usage**: Use `var(--variable-name)` in your component styles.
3.  **Runtime**: Ensure `updateDomCssVariables` logic includes your key in `logKeys` (optional, for debugging) or simply ensure it's present in the defaults/overrides object.

---

**Summary**: LESS is for structure. CSS Variables are for values. The DOM is the database of current theme state. MUI buttons require a `ThemeProvider` — CSS variables alone are not sufficient for palette-driven components.




# DASH Design System: Color & Theme Architecture

## Overview

The DASH design system uses a LESS → CSS-variable pipeline with runtime theme switching. Colors are defined as LESS variables, compiled into CSS custom properties at build time, and dynamically remapped at runtime when the user toggles between light and dark modes.

---

## 1. File Map

| Layer | File | Purpose |
|-------|------|---------|
| **LESS variables** | `dash-styles/src/variables/dash-colors.less` | Base/shared color definitions |
| **Light theme** | `dash-styles/src/variables/dash-colors-light.less` | `@var--light` overrides |
| **Dark theme** | `dash-styles/src/variables/dash-colors-dark.less` | `@var--dark` overrides |
| **CSS transformer** | `dash-styles/src/dash-css-transformer.less` | Maps `@less-var` → `--css-var` inside `:root` |
| **MUI palette** | `dash-styles/src/index.tsx` | `defaultOptions()` and `defaultComponentOverrides()` — bridges CSS vars to MUI theme |
| **Runtime remap** | `dash-utils/src/utils/updateDomCssVariables.tsx` | Remaps base CSS vars from suffixed variants on theme toggle |
| **Theme provider (public)** | `dash-boilerplate/src/theme/DashThemeProviderLight.tsx` | Lightweight MUI `ThemeProvider` for public apps |
| **Theme provider (admin)** | `DashAppComponent.tsx` / `KitchnTabsWebAppWithProviders.tsx` | Full admin app theme bootstrap |
| **Tenant defaults** | `dash-backend/config/tenants.php` → `theme_colors` | Backend default color values per tenant |

---

## 2. CSS Variable Naming Convention

Every color follows a **three-key pattern**:

```
--color-name              ← "base" key (active/runtime value)
--color-name--light       ← light theme value
--color-name--dark        ← dark theme value
```

**Example:**
```less
// In dash-colors-light.less
@text-light-color--light: #6c6c6c;

// In dash-colors-dark.less
@text-light-color--dark: #ffffff;

// In dash-css-transformer.less (:root)
--text-light-color--light: @text-light-color--light;
--text-light-color--dark:  @text-light-color--dark;
```

The **base key** (`--text-light-color` without suffix) is **not** defined statically in the transformer. It is set dynamically at runtime by `updateDomCssVariables()`.

---

## 3. Runtime Theme Switching Flow

When the user clicks the theme toggle, the following sequence occurs:

```
User clicks toggle
       │
       ▼
DarkToggleMode.onClick()
  ├─ setMode(newMode)              → MUI useColorScheme
  ├─ dashStorage.setItem('theme')  → persist preference
  ├─ document.documentElement.setAttribute('data-theme', newMode)
  └─ dispatch(toggleThemeType)     → Redux
       │
       ▼
DashThemeProviderLight (MutationObserver on data-theme)
  ├─ setCurrentMode(newMode)       → React state
  ├─ updateDomCssVariables(newMode) ← CRITICAL: remaps base CSS vars
  └─ createMinimalTheme(newMode)   → fresh MUI theme from CSS vars
       │
       ▼
updateDomCssVariables(theme)
  ├─ Reads all --var--light / --var--dark from compiled stylesheets
  ├─ For keys ending in current theme suffix (e.g. --dark):
  │   └─ Sets base key: --text-light-color = value of --text-light-color--dark
  └─ Writes all to <style id="dash-theme-variables"> at end of <head>
       │
       ▼
CSS cascade resolves: var(--text-light-color) now returns the correct theme value
MUI palette uses fresh hex values from getThemeColors(mode)
```

### Key Insight

Components reference the **base key** (`var(--text-light-color)`) — never the suffixed variants directly. The `updateDomCssVariables()` function is the bridge that copies the correct suffixed value into the base key at runtime.

**Without `updateDomCssVariables()`, the base key never updates and the UI appears stuck on the initial theme.**

---

## 4. MUI Palette Integration

### `defaultOptions()` (`dash-styles/src/index.tsx`)

Reads CSS variables and `data-theme` at call time, producing a full MUI theme config with:
- `palette` — hard-coded hex values from CSS vars at the current mode
- `colorSchemes` — `{ light: { palette }, dark: { palette } }`
- `components` — MUI component overrides using `var(--...)` references

**⚠️ Warning:** Since palette values are baked at call time, this function must NOT be memoized with empty deps. Use `defaultComponentOverrides()` for static memoization.

### `defaultComponentOverrides()` (`dash-styles/src/index.tsx`)

Returns only the `components` and `typography` keys from `defaultOptions()`. These use CSS `var()` references that resolve at runtime, so they are safe to memoize once.

```tsx
// ✅ Safe — only CSS var references, theme-agnostic
const extendedThemeOptions = useMemo(() => ({
    ...defaultComponentOverrides({})
}), []);

// ❌ Stale — baked hex values, never re-computes
const extendedThemeOptions = useMemo(() => ({
    ...defaultOptions({})
}), []);
```

### `DashThemeProviderLight` (`dash-boilerplate`)

Lightweight provider for the public app that:
1. Reads CSS vars for the current mode via `getThemeColors(mode)`
2. Creates a MUI theme with `createMinimalTheme(mode, extendedOptions)`
3. Safeguards against stale `palette`/`colorSchemes` in `extendedOptions`
4. Calls `updateDomCssVariables(mode)` on every mode change

---

## 5. Admin App vs Public App

| Concern | Admin App | Public App |
|---------|-----------|------------|
| Theme provider | `DashAppComponent` + react-admin | `DashThemeProviderLight` |
| MUI options | `appTheme()` from `dash-styles` | `defaultComponentOverrides()` |
| CSS var remap | `updateDomCssVariables()` called in `DashAppComponent` | `updateDomCssVariables()` called in `DashThemeProviderLight` |
| Tenant colors | Passed as `colors` param to `updateDomCssVariables()` | Not applicable (uses compiled LESS defaults) |

---

## 6. How to Add a New Color Variable

### Step 1: Define LESS variables

In `dash-colors.less` (or light/dark files):

```less
@table-header-color: #999;
@table-header-bg: #CCC;
@table-header-color--light: @table-header-color;
@table-header-bg--light: @table-header-bg;
@table-header-color--dark: #CCC;
@table-header-bg--dark: #999;
```

### Step 2: Map to CSS variables

In `dash-css-transformer.less` inside the `:root` block:

```less
--table-header-color: @table-header-color;
--table-header-color--light: @table-header-color--light;
--table-header-color--dark: @table-header-color--dark;
--table-header-bg: @table-header-bg;
--table-header-bg--light: @table-header-bg--light;
--table-header-bg--dark: @table-header-bg--dark;
```

### Step 3: (Optional) Make tenant-configurable

Add to `dash-backend/config/tenants.php` → `theme_colors.default_value`:

```php
"table-header-color--light" => "#999",
"table-header-color--dark"  => "#CCC",
"table-header-bg--light"    => "#CCC",
"table-header-bg--dark"     => "#999",
```

### Step 4: Use in stylesheets

```less
.your-class {
    color: var(--table-header-color, @table-header-color);
}
```

The base key (`--table-header-color`) will automatically be remapped by `updateDomCssVariables()` when the theme switches.

---

## 7. Important Color Groups

| Group | CSS Variables | Description |
|-------|-------------|-------------|
| **Body** | `--bodybg-primary`, `--bodybg-secondary` | Page background gradient |
| **Primary** | `--primary-color`, `--primary-contrast` | Sidebar, main brand colors |
| **Highlight** | `--highlight-color`, `--highlight-color-contrast` | Accent / CTA color |
| **Module** | `--module-bg`, `--module-border` | Cards, popovers, panels |
| **Text** | `--text-color`, `--text-contrast`, `--text-light`, `--text-header` | Typography |
| **Component** | `--component-bg`, `--component-hover-bg`, `--component-active-bg` | Interactive elements |
| **Button** | `--btn-bg`, `--btn-color`, `--btn-primary-bg`, `--btn-primary-color` | All button variants |
| **Alert** | `--alert-{info,error,warning,success}-bg` | Alert component backgrounds |
| **Sidebar** | `--sidebar-bg`, `--sidebar-active`, `--sidebar-icon` | Navigation sidebar |
| **Table** | `--table-header-color`, `--table-header-bg` | Data grid / table headers |

---

## 8. Compile-Time Variable Pipeline (Vite `additionalData`)

Colors get their final value at **runtime** (`updateDomCssVariables()` injects a
`<style id="dash-theme-variables">`). **Layout/dimension** variables do **not** — they
are emitted **once, at LESS compile time**, by `dash-css-transformer.less`. Understanding
how the transformer gets the right values is essential.

Each app's `vite.config.mts` prepends three imports to **every** `.less` file via
`css.preprocessorOptions.less.additionalData`, in this exact order:

```less
// apps/<app>/src/vite.config.mts
@import "../../../packages/dash-styles/src/dash-variables.less";   // 1. dash-styles DEFAULTS (@vars)
@import "@app/dash-variables.less";                                // 2. APP OVERRIDES (@vars)  ← wins
@import "../../../packages/dash-styles/src/dash-css-transformer.less"; // 3. emits :root { --css-var: @var }
```

Because LESS resolves a variable to its **last** assignment in scope, the app's
`dash-variables.less` (step 2) overrides the dash defaults (step 1) **before** the
transformer (step 3) reads them. So:

```less
// dash-styles/src/variables/sizes.less   →  @sidebar-large-width: 255px;   (default)
// apps/kitchntabs-system/src/dash-variables.less → @sidebar-large-width: 180px;   (override)
// dash-css-transformer.less:
--sidebar-large-width: @sidebar-large-width;   // emits 180px for kitchntabs-system, 255px elsewhere
```

> ⚠️ **Critical rule for dimensions:** in `dash-css-transformer.less`, a dimension CSS
> variable MUST reference the LESS var (`--sidebar-large-width: @sidebar-large-width;`),
> **never** a literal (`--sidebar-large-width: 255px;`). A literal ignores the app's
> `dash-variables.less` override entirely (the override is in scope but unused), and the
> change silently does nothing. This is different from the color rows, which are literal
> dash-styles fallbacks that get replaced at runtime.

### 8.1 Two override conventions — and the import order each requires

Apps override design tokens in their `apps/<app>/src/dash-variables.less` using **one of
two conventions**, and **the `additionalData` import order MUST match the convention**:

| Convention | App writes | Required order | Apps |
|---|---|---|---|
| **LESS `@var`** | `@primary-color: #8f00cb;` `@sidebar-large-width: 180px;` | app **BEFORE** transformer | `kitchntabs-system`, `kitchntabs-mall` |
| **CSS `--var`** | `:root { --primary-color--light: #8f00cb; }` | app **AFTER** transformer | `kitchntabs-web`, `kitchntabs-app`, `kitchntabs` |

Why the order differs:

- **LESS `@var` apps** rely on the transformer *reading* their `@var` overrides, so the app
  must be imported **before** the transformer (so the override is the last `@var`
  assignment in scope when the transformer compiles):
  ```less
  @import ".../dash-variables.less";          // dash defaults
  @import "@app/dash-variables.less";         // app @var overrides  ← before
  @import ".../dash-css-transformer.less";    // reads @vars, emits :root
  ```
- **CSS `--var` apps** emit their own `:root` block that must *win the cascade* over the
  transformer's `:root`, so the app must be imported **after** the transformer (last
  `:root` for an equal-specificity selector wins):
  ```less
  @import ".../dash-variables.less";          // dash defaults
  @import ".../dash-css-transformer.less";    // transformer :root (gray defaults)
  @import "@app/dash-variables.less";         // app --var :root  ← after, wins
  ```

> 🐞 **Symptom of a wrong order:** a CSS-`--var` app whose `additionalData` imports the app
> *before* the transformer renders the **dash-styles gray defaults** (e.g. `--primary-color
> --light: #c3c3c3`) instead of its own colors, because the transformer's `:root` loads last
> and wins. Fixed by moving `@import '@app/dash-variables.less'` to the **end** of
> `additionalData`. (This was the kitchntabs-web purple-not-applying bug, 2026-06-13.)

> The sidebar-dimension mapping (`--sidebar-large-width: @sidebar-large-width;`) works under
> both orders: LESS-`@var` apps override the `@var` (transformer emits it); CSS-`--var` apps
> let the transformer emit the `255px` default, then override it with their own `--var`.

---

## 9. Layout & Dimension Variables

| CSS Variable | LESS source (`@var`) | Default | Notes |
|---|---|---|---|
| `--sidebar-large-width` | `@sidebar-large-width` | `255px` | Expanded sidebar width |
| `--sidebar-small-width` | `@sidebar-small-width` | `60px` | Collapsed sidebar width |
| `--sidebar-mini-drawer-width` | (literal) | `100px` | |
| `--sidebar-horizontal-height` | (literal) | `120px` | |
| `--min-body-width` | (literal) | `575px` | |

**To override a layout dimension for one app:** set the **LESS** var in
`apps/<app>/src/dash-variables.less`:

```less
@sidebar-large-width: 180px;
@sidebar-small-width: 60px;
```

Do **not** redefine `--sidebar-large-width` as a CSS var in the app's `styles.less`
`:root` — the transformer's `:root` (injected via `additionalData` into every file)
loads after it and wins, so an app-level `:root` hardcode is dead/misleading. The LESS
var is the single source of truth.

### Debugging "my dimension variable isn't applying"

1. **Inspect** the element: confirm it uses `var(--sidebar-large-width)`.
2. **Computed value** wrong (e.g. `255px` not `180px`)? Open
   `dash-styles/src/dash-css-transformer.less` and verify the line reads
   `--sidebar-large-width: @sidebar-large-width;` (a `@`-reference), not a literal `px`.
3. Confirm your app's `dash-variables.less` sets the **`@`** LESS var (not a `--` CSS var).
4. Search the app's `styles.less`/`:root` for a competing `--sidebar-large-width:` hardcode
   and remove it.
5. Restart the Vite dev server — `additionalData` and transformer changes are compile-time.
