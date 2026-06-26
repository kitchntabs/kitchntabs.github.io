# Dash Framework - Internationalization (i18n) Technical Documentation

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Core Components](#3-core-components)
4. [Translation Providers](#4-translation-providers)
5. [React Context System](#5-react-context-system)
6. [Language Switching](#6-language-switching)
7. [Translation Files Structure](#7-translation-files-structure)
8. [Component Integration](#8-component-integration)
9. [Implementation Examples](#9-implementation-examples)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Overview

The Dash Framework uses a sophisticated internationalization (i18n) system that supports:

- **Multiple languages** (English, Spanish, and extensible to others)
- **Polyglot-style interpolation** using `%{variable}` syntax
- **Seamless integration** with React Admin's i18n system
- **Lightweight providers** for public apps that don't require React Admin
- **Real-time language switching** without page reload
- **Persistence** via localStorage

### Key Design Principles

1. **Single Source of Truth**: One `I18nBridgeContext` for all components
2. **Bridge Pattern**: Allows components outside React Admin's context to access translations
3. **Lightweight Options**: Public apps can use a simplified provider without React Admin dependencies
4. **Redux Integration**: Language preference synced with Redux state

---

## 2. Architecture

### High-Level Component Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DASH I18N ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        APPLICATION ENTRY                              │   │
│  │                                                                       │   │
│  │   ┌─────────────────────────────────────────────────────────────┐    │   │
│  │   │  I18nBridgeProvider (from dash-admin)                       │    │   │
│  │   │  - Wraps entire application                                  │    │   │
│  │   │  - Provides context for i18nProvider and locale              │    │   │
│  │   └───────────────────────────┬─────────────────────────────────┘    │   │
│  │                               │                                       │   │
│  │   ┌───────────────────────────▼─────────────────────────────────┐    │   │
│  │   │  I18nBridgeSetter                                            │    │   │
│  │   │  - Sets the actual i18n provider on context                  │    │   │
│  │   │  - Called early in render cycle                              │    │   │
│  │   └───────────────────────────┬─────────────────────────────────┘    │   │
│  │                               │                                       │   │
│  └───────────────────────────────┼───────────────────────────────────────┘   │
│                                  │                                           │
│         ┌────────────────────────┴────────────────────────┐                  │
│         │                                                 │                  │
│         ▼                                                 ▼                  │
│  ┌─────────────────────────┐                    ┌─────────────────────────┐ │
│  │   PRIVATE APP           │                    │   PUBLIC APP            │ │
│  │   (React Admin based)   │                    │   (Lightweight)         │ │
│  │                         │                    │                         │ │
│  │  polyglotI18nProvider   │                    │ createSimpleI18nProvider│ │
│  │  - Full RA integration  │                    │ - No RA dependency      │ │
│  │  - ra-i18n-polyglot     │                    │ - dash-boilerplate      │ │
│  └─────────────────────────┘                    └─────────────────────────┘ │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        CONSUMING COMPONENTS                           │   │
│  │                                                                       │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │   │
│  │  │ AppMaterialMenu │  │  LangSwitcher   │  │ Custom Components   │   │   │
│  │  │ useI18nBridge() │  │ useLocaleState()│  │ useI18nBridge()     │   │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Package Dependencies

```
dash-admin
├── I18nBridgeContext.tsx          # Primary context for i18n bridging
├── LangSwitcher.tsx               # Language switching UI component
├── usePolyglotTranslation.tsx     # Redux-based locale hooks
└── providers/i18n/                # Base translation files (en, es)

dash-boilerplate
├── createSimpleI18nProvider.ts    # Lightweight provider factory
├── I18nBridgeProviderLight.tsx    # Alternative context (legacy)
└── types.ts                       # TypeScript interfaces

Application (kitchntabs-web, kitchntabs-mall, etc.)
├── i18n/en.tsx                    # App-specific English translations
├── i18n/es.tsx                    # App-specific Spanish translations
└── KitchnTabs*App.tsx             # App entry with i18n setup
```

---

## 3. Core Components

### 3.1 I18nBridgeContext (Primary)

**Location:** `packages/dash-admin/src/contexts/I18nBridgeContext.tsx`

**Purpose:** Bridges the i18n provider from inside React Admin's context to components that render outside of it.

```typescript
interface I18nBridgeContextValue {
    i18nProvider: I18nProvider | null;  // The actual translation provider
    locale: string;                      // Current locale (triggers re-renders)
    setI18nProvider: (provider: I18nProvider) => void;
    setLocale: (locale: string) => void;
}
```

**Key Features:**
- Provides centralized i18n access for all components
- `locale` state triggers re-renders when language changes
- Works with both React Admin's polyglotI18nProvider and lightweight providers

**Provider Component:**

```tsx
export const I18nBridgeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [i18nProvider, setI18nProviderState] = useState<I18nProvider | null>(null);
    const [locale, setLocale] = useState<string>('es');

    const setI18nProvider = useCallback((provider: I18nProvider) => {
        setI18nProviderState(provider);
        // Sync initial locale from provider
        if (provider?.getLocale) {
            setLocale(provider.getLocale());
        }
    }, []);

    return (
        <I18nBridgeContext.Provider value={{ i18nProvider, locale, setI18nProvider, setLocale }}>
            {children}
        </I18nBridgeContext.Provider>
    );
};
```

### 3.2 Available Hooks

#### `useI18nBridge()`

Main hook for accessing the i18n bridge context.

```typescript
const { i18nProvider, locale, setI18nProvider, setLocale } = useI18nBridge();
```

#### `useBridgedLocales()`

Get available locales from the bridged provider.

```typescript
const locales = useBridgedLocales();
// Returns: [{ locale: 'en', name: 'English' }, { locale: 'es', name: 'Español' }]
```

#### `useBridgedChangeLocale()`

Change locale and trigger re-renders across the app.

```typescript
const changeLocale = useBridgedChangeLocale();
await changeLocale('en');
```

#### `useBridgedLocale()`

Get current locale string.

```typescript
const currentLocale = useBridgedLocale();
// Returns: 'es' or 'en'
```

---

## 4. Translation Providers

### 4.1 For Private Apps (React Admin)

**Uses:** `polyglotI18nProvider` from `ra-i18n-polyglot`

**Location:** App entry files (e.g., `KitchnTabsPrivateApp.tsx`)

```typescript
import polyglotI18nProvider from 'ra-i18n-polyglot';
import { en as dashAdminEn, es as dashAdminEs } from 'dash-admin';
import customEnglish from './i18n/en';
import customSpanish from './i18n/es';

// Merge translations
const translations = {
    en: { ...dashAdminEn, ...customEnglish },
    es: { ...dashAdminEs, ...customSpanish },
};

// Create provider
const provider = polyglotI18nProvider(
    (locale) => translations[locale] || translations.es,
    'es',  // Default locale
    [
        { locale: 'en', name: 'English' },
        { locale: 'es', name: 'Español' },
    ],
    { allowMissing: true }
);
```

**Provider Interface (from React Admin):**

```typescript
interface I18nProvider {
    translate: (key: string, options?: any) => string;
    changeLocale: (locale: string) => Promise<void>;
    getLocale: () => string;
    getLocales?: () => Array<{ locale: string; name: string }>;
    getMessages?: (locale: string) => Record<string, any>;
}
```

### 4.2 For Public Apps (Lightweight)

**Uses:** `createSimpleI18nProvider` from `dash-boilerplate`

**Location:** `packages/dash-boilerplate/src/i18n/createSimpleI18nProvider.ts`

```typescript
import { createSimpleI18nProvider } from 'dash-boilerplate';
import customEnglish from './i18n/en';
import customSpanish from './i18n/es';

const translationsData = {
    en: { ...customEnglish },
    es: { ...customSpanish },
};

const i18nProvider = createSimpleI18nProvider({
    translations: translationsData,
    initialLocale: localStorage.getItem('dash-user-locale') || 'es',
    fallbackLocale: 'en',
    locales: [
        { locale: 'en', name: 'English' },
        { locale: 'es', name: 'Español' },
    ],
    onLocaleChange: (locale) => {
        console.log('Locale changed to:', locale);
    },
});
```

**Provider Interface (Lightweight):**

```typescript
interface SimpleI18nProvider {
    translate: (key: string, options?: Record<string, any>) => string;
    changeLocale: (locale: string) => Promise<void>;
    getLocale: () => string;
    getLocales?: () => Array<{ locale: string; name: string }>;
    getMessages?: (locale: string) => Record<string, any>;
}
```

### 4.3 Implementation Details

The lightweight provider uses a simple interpolation mechanism:

```typescript
// Polyglot-style variable interpolation
const interpolate = (text: string, options?: Record<string, any>): string => {
    if (!options || !text) return text;
    return Object.keys(options).reduce((acc, key) => {
        return acc.replace(new RegExp(`%\\{${key}\\}`, 'g'), String(options[key]));
    }, text);
};

// Example usage
translate('tab.status.change_to', { status: 'Confirmed' });
// Returns: "Change status to Confirmed"
```

---

## 5. React Context System

### Context Hierarchy

```
<Provider store={reduxStore}>        // Redux store (for useLocaleState)
    <I18nBridgeProvider>             // i18n bridge context
        <I18nBridgeSetter />         // Sets provider on context
        <QueryClientProvider>
            <RouterComponent>
                <DASHAdmin>           // For private apps
                    <AppMaterialMenu />  // Uses useI18nBridge()
                    <LangSwitcher />     // Uses both Redux and Bridge
                </DASHAdmin>
            </RouterComponent>
        </QueryClientProvider>
    </I18nBridgeProvider>
</Provider>
```

### I18nBridgeSetter Pattern

A helper component that sets the provider early in the render cycle:

```tsx
const I18nBridgeSetter = ({ provider }: { provider: any }) => {
    const { setI18nProvider } = useI18nBridge();
    
    React.useEffect(() => {
        if (provider) {
            console.log('🌐 I18nBridgeSetter: Setting provider');
            setI18nProvider(provider);
        }
    }, [provider, setI18nProvider]);
    
    return null;
};

// Usage in app
<I18nBridgeProvider>
    <I18nBridgeSetter provider={i18nProvider} />
    {/* Rest of app */}
</I18nBridgeProvider>
```

---

## 6. Language Switching

### 6.1 LangSwitcher Component

**Location:** `packages/dash-admin/src/components/i18n/LangSwitcher.tsx`

**Purpose:** Provides UI for users to change language.

```tsx
import { useLocales, useLocaleState } from '../../hooks/usePolyglotTranslation';
import { useBridgedChangeLocale } from '../../contexts/I18nBridgeContext';

const LangSwitcher = () => {
    const languages = useLocales();
    const [locale, setLocale] = useLocaleState();  // Redux
    const changeBridgedLocale = useBridgedChangeLocale();  // Bridge context

    const changeLocale = (newLocale: string) => () => {
        // Update Redux state
        setLocale(newLocale);
        // Update bridge context (triggers component re-renders)
        changeBridgedLocale(newLocale);
    };

    return (
        <div>
            {languages.map(language => (
                <button 
                    key={language.locale}
                    onClick={changeLocale(language.locale)}
                >
                    {language.name}
                </button>
            ))}
        </div>
    );
};
```

### 6.2 State Flow on Language Change

```
User clicks language
         │
         ▼
┌─────────────────────────┐
│     setLocale()         │  ─────▶  Redux state updated
│  (useLocaleState hook)  │         (state.settings.locale)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  changeBridgedLocale()  │  ─────▶  i18nProvider.changeLocale()
│  (useBridgedChangeLocale)│        + setLocale() in context
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Context locale state   │  ─────▶  All components using useI18nBridge()
│     changes             │          re-render with new locale
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    localStorage         │  ─────▶  'dash-user-locale' persisted
│      updated            │
└─────────────────────────┘
```

### 6.3 Redux Hooks for Locale

**Location:** `packages/dash-admin/src/hooks/usePolyglotTranslation.tsx`

```typescript
// Get available locales from Redux
export const useLocales = ({ locales }: { locales?: any[] } = {}) => {
    const availableLocales = useSelector(
        (state: IDASHAppState) => state.settings?.availableLocales
    );
    return locales?.length > 0 ? locales : availableLocales || defaultLocales;
};

// Get and set locale via Redux
export const useLocaleState = (): [string, (locale: string) => void] => {
    const dispatch = useDispatch();
    const currentLocale = useSelector(
        (state: IDASHAppState) => state.settings?.locale || 'es'
    );

    const setLocale = useCallback((newLocale: string) => {
        dispatch(DASH_REDUX_ACTIONS.switchLanguage(newLocale));
        localStorage.setItem('dash-user-locale', newLocale);
    }, [dispatch]);

    return [currentLocale, setLocale];
};
```

### 6.4 URL Locale Detection

**Location:** `packages/dash-boilerplate/src/utils/DashBootstrapUtils.ts`

**Purpose:** Automatically detect and apply locale from URL query parameters (e.g., `?lang=en`).

This is particularly useful for:
- Email links that should open in a specific language
- Marketing URLs with language targeting
- External integrations that need to control language

```typescript
import { useUrlLocaleDetection, LOCALE_CHANGE_EVENT } from 'dash-boilerplate';

// In your bootstrap component:
const MyBootstrap: React.FC = () => {
    // Detect ?lang=es or ?lang=en from URL and apply it
    useUrlLocaleDetection(['es', 'en'], 'es');
    
    return <App />;
};
```

**How it works:**

1. **URL Parameter Reading:** Reads the `lang` query parameter
2. **Validation:** Checks if the value is in the allowed locales array
3. **Redux Update:** Dispatches `switchLanguage` action to Redux
4. **localStorage Persistence:** Saves to `dash-user-locale`
5. **Custom Event:** Emits `dash:locale-change` event for I18nBridgeProvider

**Flow Diagram:**

```
URL: /page?lang=en
         │
         ▼
┌─────────────────────────────┐
│  useUrlLocaleDetection()    │
│  in Bootstrap component     │
└───────────┬─────────────────┘
            │
            ├─────────────▶ Redux: dispatch(switchLanguage('en'))
            │
            ├─────────────▶ localStorage.setItem('dash-user-locale', 'en')
            │
            ▼
┌─────────────────────────────┐
│  Emit CustomEvent           │
│  'dash:locale-change'       │
│  { detail: { locale: 'en' }}│
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  I18nBridgeProvider listens │
│  Updates context locale     │
│  Calls provider.changeLocale│
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  All components re-render   │
│  with new locale            │
└─────────────────────────────┘
```

**Custom Event Details:**

```typescript
// Event name constant (exported from both packages)
export const LOCALE_CHANGE_EVENT = 'dash:locale-change';

// Event structure
interface LocaleChangeEvent extends CustomEvent {
    detail: {
        locale: string;  // The new locale code (e.g., 'en', 'es')
    };
}
```

---

## 7. Translation Files Structure

### 7.1 File Organization

```
apps/kitchntabs-web/src/i18n/
├── en.tsx    # English translations
└── es.tsx    # Spanish translations

packages/dash-admin/src/providers/i18n/
├── en.ts     # Base English translations (ra.* keys)
├── es.ts     # Base Spanish translations (ra.* keys)
└── languages.tsx  # Re-exports
```

### 7.2 Translation File Format

**App-specific translations:**

```typescript
// apps/kitchntabs-web/src/i18n/es.tsx
const customEs = {
    // Flat keys
    "Delivery Method": "Método de Entrega",
    "Table Number": "Número de Mesa",
    
    // Nested objects (dot notation access)
    tab: {
        tabs: 'Tabs',
        kitchen_tabs: 'Comandas de Cocina',
        action: {
            cancel: 'Cancelar',
            confirm: 'Confirmar',
            print: 'Imprimir',
        },
        status: {
            created: 'Creado',
            confirmed: 'Confirmado',
            // With interpolation
            change_to: "Cambiar estado a %{status}",
        },
        products: {
            search: {
                label: "Buscar",
                // Multiple interpolations
                local_active: "Búsqueda local activa. Escribe %{count} caracteres más.",
            },
        },
    },
    
    // Menu translations
    menu: {
        home: "Inicio",
        plans: "Planes",
        order: "Ordenar",
    },
    
    // Resource labels
    resource: {
        system: {
            tenants: {
                label: "Tenants",
            },
        },
        groups: {
            products: "Productos",
        },
    },
};

export default customEs;
```

**Base translations (React Admin keys):**

```typescript
// packages/dash-admin/src/providers/i18n/es.ts
const dashSpanish = {
    ra: {
        action: {
            add: 'Agregar',
            cancel: 'Cancelar',
            create: 'Crear',
            delete: 'Eliminar',
            edit: 'Editar',
            save: 'Guardar',
            // ...
        },
        auth: {
            logout: 'Cerrar sesión',
            password: 'Contraseña',
            sign_in: 'Iniciar sesión',
            // ...
        },
        // ...
    },
};
```

### 7.3 Merging Translations

```typescript
// In private app entry
const translations = {
    en: {
        ...dashAdminEn,    // Base RA translations
        ...customEnglish,  // App-specific translations (override)
    },
    es: {
        ...dashAdminEs,
        ...customSpanish,
    },
};
```

---

## 8. Component Integration

### 8.1 AppMaterialMenu (Sidebar)

**Location:** `packages/dash-admin/src/default-theme/menu/AppMaterialMenu.tsx`

**Challenge:** Renders OUTSIDE React Admin's AdminContext hierarchy.

**Solution:** Uses `useI18nBridge()` to access translations.

```tsx
const AppMaterialMenu: React.FC = () => {
    // Get i18n from Bridge context
    const { i18nProvider, locale: currentLocale } = useI18nBridge();
    
    // Create translate function
    const translate = React.useCallback((key: string, options?: any) => {
        if (typeof key !== 'string') return key;
        if (i18nProvider?.translate) {
            try {
                return i18nProvider.translate(key, options);
            } catch (e) {
                return key;
            }
        }
        return key;
    }, [i18nProvider]);

    // Re-build menu items when locale changes
    useEffect(() => {
        // Build menu with translated labels
        const _items = resources.map(resource => ({
            label: translate(resource.label, { _: resource.label }),
            // ...
        }));
        setItems(_items);
    }, [resources, currentLocale, translate]);  // currentLocale in dependencies!
    
    return <GenerateItems items={items} translate={translate} />;
};
```

**Key Points:**
- `currentLocale` in useEffect dependencies triggers menu rebuild on language change
- `translate` function wrapped in useCallback to prevent unnecessary re-renders
- Fallback to key if translation fails

### 8.2 Custom Components

**Using translations in any component:**

```tsx
import { useI18nBridge } from 'dash-admin/src/contexts/I18nBridgeContext';

const MyComponent = () => {
    const { i18nProvider, locale } = useI18nBridge();
    
    const t = (key: string, options?: any) => {
        return i18nProvider?.translate(key, options) || key;
    };
    
    return (
        <div>
            <h1>{t('tab.tabs')}</h1>
            <p>{t('tab.status.change_to', { status: 'Confirmado' })}</p>
        </div>
    );
};
```

### 8.3 Form Labels and Validation

```tsx
const MyForm = () => {
    const { i18nProvider } = useI18nBridge();
    const t = (key: string) => i18nProvider?.translate(key) || key;
    
    return (
        <form>
            <TextField 
                label={t('tab.attribute.note')}
                placeholder={t('tab.order.note_placeholder')}
            />
            <Button>{t('tab.action.confirm')}</Button>
        </form>
    );
};
```

---

## 9. Implementation Examples

### 9.1 Setting Up a New Public App

```tsx
// NewPublicApp.tsx
import React, { useMemo } from 'react';
import { createSimpleI18nProvider } from 'dash-boilerplate';
import { I18nBridgeProvider, useI18nBridge } from 'dash-admin/src/contexts/I18nBridgeContext';
import customEnglish from './i18n/en';
import customSpanish from './i18n/es';

// I18n bridge setter component
const I18nBridgeSetter = ({ provider }) => {
    const { setI18nProvider } = useI18nBridge();
    
    React.useEffect(() => {
        if (provider) setI18nProvider(provider);
    }, [provider, setI18nProvider]);
    
    return null;
};

const NewPublicApp = () => {
    // Create translation data
    const translationsData = useMemo(() => ({
        en: { ...customEnglish },
        es: { ...customSpanish },
    }), []);

    // Create i18n provider
    const i18nProvider = useMemo(() => {
        const initialLocale = localStorage.getItem('dash-user-locale') || 'es';
        return createSimpleI18nProvider({
            translations: translationsData,
            initialLocale,
        });
    }, [translationsData]);

    return (
        <I18nBridgeProvider>
            <I18nBridgeSetter provider={i18nProvider} />
            <YourAppContent />
        </I18nBridgeProvider>
    );
};
```

### 9.2 Setting Up a New Private App

```tsx
// NewPrivateApp.tsx
import React, { useMemo, useEffect } from 'react';
import polyglotI18nProvider from 'ra-i18n-polyglot';
import { en as dashAdminEn, es as dashAdminEs } from 'dash-admin';
import { I18nBridgeProvider, useI18nBridge } from 'dash-admin/src/contexts/I18nBridgeContext';
import customEnglish from './i18n/en';
import customSpanish from './i18n/es';

const translations = {
    en: { ...dashAdminEn, ...customEnglish },
    es: { ...dashAdminEs, ...customSpanish },
};

const NewPrivateApp = () => {
    const [i18nProvider, setI18nProvider] = React.useState(null);
    
    useEffect(() => {
        const locale = localStorage.getItem('dash-user-locale') || 'es';
        const provider = polyglotI18nProvider(
            (locale) => translations[locale] || translations.es,
            locale,
            [
                { locale: 'en', name: 'English' },
                { locale: 'es', name: 'Español' },
            ],
            { allowMissing: true }
        );
        setI18nProvider(provider);
    }, []);

    if (!i18nProvider) return <LoadingSpinner />;

    return (
        <I18nBridgeProvider>
            <DASHAdmin i18nProvider={i18nProvider}>
                {/* Admin content */}
            </DASHAdmin>
        </I18nBridgeProvider>
    );
};
```

### 9.3 Adding a New Language

**Step 1:** Create translation file

```typescript
// apps/your-app/src/i18n/fr.tsx
const customFr = {
    "Delivery Method": "Mode de livraison",
    tab: {
        tabs: 'Onglets',
        action: {
            confirm: 'Confirmer',
        },
    },
};
export default customFr;
```

**Step 2:** Add to translations map

```typescript
import customFrench from './i18n/fr';

const translations = {
    en: { ...dashAdminEn, ...customEnglish },
    es: { ...dashAdminEs, ...customSpanish },
    fr: { ...dashAdminFr, ...customFrench },  // Add French
};
```

**Step 3:** Update locales array

```typescript
const provider = polyglotI18nProvider(
    (locale) => translations[locale] || translations.es,
    'es',
    [
        { locale: 'en', name: 'English' },
        { locale: 'es', name: 'Español' },
        { locale: 'fr', name: 'Français' },  // Add French option
    ]
);
```

### 9.4 Creating Interpolated Translations

```typescript
// Translation file
const translations = {
    welcome: "Welcome, %{name}!",
    items_count: "You have %{count} items",
    order_summary: "Order #%{orderId} for %{customer} - Total: %{total}",
};

// Component usage
const WelcomeMessage = () => {
    const { i18nProvider } = useI18nBridge();
    
    return (
        <div>
            {/* Simple interpolation */}
            <h1>{i18nProvider?.translate('welcome', { name: 'John' })}</h1>
            
            {/* Numeric interpolation */}
            <p>{i18nProvider?.translate('items_count', { count: 5 })}</p>
            
            {/* Multiple interpolations */}
            <p>{i18nProvider?.translate('order_summary', {
                orderId: 123,
                customer: 'Jane',
                total: '$99.99'
            })}</p>
        </div>
    );
};
```

---

## 10. Troubleshooting

### 10.1 Common Issues

#### Translation Keys Showing Instead of Values

**Symptom:** UI shows `menu.home` instead of `Home`

**Causes & Solutions:**

1. **Provider not set on context**
   ```tsx
   // Ensure I18nBridgeSetter runs early
   <I18nBridgeProvider>
       <I18nBridgeSetter provider={i18nProvider} />  // ← Must be here
       <RestOfApp />
   </I18nBridgeProvider>
   ```

2. **Wrong context being used**
   ```tsx
   // Use the correct hook
   import { useI18nBridge } from 'dash-admin/src/contexts/I18nBridgeContext';
   // NOT from dash-boilerplate
   ```

3. **Missing translation key**
   ```typescript
   // Check key exists in translation file
   const translations = {
       menu: {
           home: "Home",  // ← Key must exist
       },
   };
   ```

#### Language Not Switching

**Symptom:** Clicking language option doesn't update UI

**Causes & Solutions:**

1. **Not updating bridge context locale**
   ```tsx
   const changeLocale = (newLocale: string) => {
       setLocale(newLocale);              // Redux
       changeBridgedLocale(newLocale);    // Bridge context ← Don't forget!
   };
   ```

2. **Component not using currentLocale in dependencies**
   ```tsx
   // Include currentLocale in useEffect dependencies
   useEffect(() => {
       // Rebuild translated content
   }, [currentLocale]);  // ← Required for re-render
   ```

#### Menu Not Updating on Language Change

**Symptom:** Menu stays in old language after switching

**Solution:** Ensure `currentLocale` is in useEffect dependencies:

```tsx
const { locale: currentLocale } = useI18nBridge();

useEffect(() => {
    const menuItems = buildTranslatedMenu();
    setItems(menuItems);
}, [currentLocale]);  // ← Menu rebuilds when this changes
```

### 10.2 Debugging Tips

**Enable debug logging in components:**

```tsx
const { i18nProvider, locale } = useI18nBridge();

useEffect(() => {
    console.log('🌐 Current provider:', i18nProvider);
    console.log('🌐 Current locale:', locale);
    console.log('🧪 Test translate:', i18nProvider?.translate('menu.home'));
}, [i18nProvider, locale]);
```

**Check provider configuration:**

```tsx
console.log('Provider details:', {
    hasProvider: !!i18nProvider,
    hasTranslate: !!i18nProvider?.translate,
    hasGetLocales: !!i18nProvider?.getLocales,
    currentLocale: i18nProvider?.getLocale?.(),
    availableLocales: i18nProvider?.getLocales?.(),
});
```

**Test translation with specific key:**

```tsx
const testKey = 'tab.action.confirm';
console.log(`Translation for "${testKey}":`, i18nProvider?.translate(testKey));
```

### 10.3 Best Practices

1. **Always use I18nBridgeProvider at app root**
2. **Set provider early with I18nBridgeSetter**
3. **Include `currentLocale` in useEffect dependencies for translated content**
4. **Use useCallback for translate functions to prevent unnecessary re-renders**
5. **Provide fallback values for missing translations**
6. **Merge base translations (dash-admin) with app-specific ones**
7. **Persist locale to localStorage for session continuity**

---

## Appendix: Type Definitions

### I18nBridgeContextValue

```typescript
interface I18nBridgeContextValue {
    i18nProvider: I18nProvider | null;
    locale: string;
    setI18nProvider: (provider: I18nProvider) => void;
    setLocale: (locale: string) => void;
}
```

### SimpleI18nProvider

```typescript
interface SimpleI18nProvider {
    translate: (key: string, options?: Record<string, any>) => string;
    changeLocale: (locale: string) => Promise<void>;
    getLocale: () => string;
    getLocales?: () => LocaleDefinition[];
    getMessages?: (locale: string) => Record<string, any>;
}
```

### LocaleDefinition

```typescript
interface LocaleDefinition {
    locale: string;
    name: string;
    languageId?: string;
    icon?: string;
}
```

### TranslationsMap

```typescript
type TranslationMessages = Record<string, any>;
type TranslationsMap = Record<string, TranslationMessages>;
```

### CreateSimpleI18nProviderOptions

```typescript
interface CreateSimpleI18nProviderOptions {
    translations: TranslationsMap;
    initialLocale?: string;
    fallbackLocale?: string;
    locales?: LocaleDefinition[];
    onLocaleChange?: (locale: string) => void;
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-20 | Initial documentation |

---

## Related Documentation

- [React Admin i18n Documentation](https://marmelab.com/react-admin/TranslationSetup.html)
- [Node Polyglot Documentation](https://airbnb.io/polyglot.js/)
- [Dash Admin State Management](./DASH_ADMIN_STATE_DOCUMENTATION.md)
