---
layout: default
title: F19-Internationalization TRANSLATION GUIDE
---

# KitchnTabs Translation Guide

## Overview

The KitchnTabs application uses react-admin's i18n system with JSON translation files. Currently supporting:
- **Spanish (es)** - Default language
- **English (en)**

## File Locations

### Frontend Translation Files
- `/apps/kitchntabs/src/i18n/es.tsx` - Spanish translations
- `/apps/kitchntabs/src/i18n/en.tsx` - English translations

### Backend Translation Files (Laravel)
- `/dash-backend/lang/es/` - Spanish translations
- `/dash-backend/lang/en/` - English translations

## How Translations Work

### 1. React-Admin i18n System

The app uses react-admin's `useTranslate()` hook:

```tsx
import { useTranslate } from 'react-admin';

const MyComponent = () => {
  const translate = useTranslate();
  
  return <div>{translate('tab.status.created')}</div>;
  // Output (es): "Creado"
  // Output (en): "Created"
};
```

### 2. Translation Keys Structure

Translation keys follow a hierarchical pattern:

```json
{
  "domain.subdomain.key": "Translation"
}
```

**Examples:**
```json
{
  "tab.status.created": "Creado",
  "tab.action.confirm": "Confirmar",
  "tab.products.search.label": "Buscar",
  "tab.order.total": "Total"
}
```

### 3. Interpolation (Variables)

Use `%{variableName}` for dynamic values:

```json
{
  "tab.products.display.showing_results": "Mostrando %{displayed} de %{total} resultados"
}
```

```tsx
translate('tab.products.display.showing_results', { 
  displayed: 10, 
  total: 50 
});
// Output: "Mostrando 10 de 50 resultados"
```

## Current Translation Coverage

### ✅ Already Translated
- Tab statuses (created, confirmed, in_preparation, etc.)
- Tab actions (confirm, close, print, etc.)
- Product search interface
- Order products interface
- Modifiers and options
- Payment interface
- Mall notifications

### ❌ Missing Translations

Based on the codebase, here are **key areas that need translations**:

#### 1. General UI Elements
```json
{
  "app.welcome": "Bienvenido",
  "app.logout": "Cerrar sesión",
  "app.profile": "Perfil",
  "app.settings": "Configuración",
  "app.save": "Guardar",
  "app.cancel": "Cancelar",
  "app.delete": "Eliminar",
  "app.edit": "Editar",
  "app.create": "Crear",
  "app.back": "Volver",
  "app.loading": "Cargando...",
  "app.error": "Error",
  "app.success": "Éxito"
}
```

#### 2. Authentication
```json
{
  "auth.login": "Iniciar sesión",
  "auth.email": "Correo electrónico",
  "auth.password": "Contraseña",
  "auth.forgot_password": "¿Olvidaste tu contraseña?",
  "auth.remember_me": "Recordarme",
  "auth.logout": "Cerrar sesión"
}
```

#### 3. Resource CRUD (react-admin defaults)
```json
{
  "ra.action.create": "Crear",
  "ra.action.edit": "Editar",
  "ra.action.show": "Ver",
  "ra.action.delete": "Eliminar",
  "ra.action.save": "Guardar",
  "ra.action.cancel": "Cancelar",
  "ra.action.list": "Lista",
  "ra.notification.created": "Elemento creado",
  "ra.notification.updated": "Elemento actualizado",
  "ra.notification.deleted": "Elemento eliminado",
  "ra.page.list": "%{name} Lista",
  "ra.page.edit": "%{name} #%{id}",
  "ra.page.create": "Crear %{name}",
  "ra.page.show": "%{name} #%{id}"
}
```

#### 4. Products
```json
{
  "products.name": "Nombre",
  "products.price": "Precio",
  "products.category": "Categoría",
  "products.stock": "Stock",
  "products.description": "Descripción",
  "products.add_to_cart": "Agregar al carrito",
  "products.out_of_stock": "Agotado"
}
```

#### 5. Orders
```json
{
  "orders.order_number": "Número de orden",
  "orders.date": "Fecha",
  "orders.status": "Estado",
  "orders.customer": "Cliente",
  "orders.subtotal": "Subtotal",
  "orders.discount": "Descuento",
  "orders.total": "Total",
  "orders.payment_method": "Método de pago"
}
```

#### 6. Mall-specific
```json
{
  "mall.session": "Sesión de Mall",
  "mall.scan_qr": "Escanear código QR",
  "mall.select_restaurant": "Seleccionar restaurante",
  "mall.your_orders": "Tus órdenes",
  "mall.order_from": "Ordenar de %{restaurant}",
  "mall.order_progress": "Progreso de la orden",
  "mall.request_assistance": "Solicitar asistencia",
  "mall.assistance_requested": "Asistencia solicitada"
}
```

#### 7. Validation Messages
```json
{
  "validation.required": "Este campo es requerido",
  "validation.email": "Debe ser un correo electrónico válido",
  "validation.min_length": "Debe tener al menos %{min} caracteres",
  "validation.max_length": "No debe exceder %{max} caracteres",
  "validation.numeric": "Debe ser un número",
  "validation.positive": "Debe ser un número positivo"
}
```

## How to Add Translations

### Step 1: Identify Untranslated Text

Search for hardcoded strings in your components:

```bash
# Find hardcoded strings (Spanish example)
grep -r "Confirmar\|Cerrar\|Guardar" apps/kitchntabs/src --include="*.tsx" --include="*.ts"
```

### Step 2: Add Translation Keys

**Before:**
```tsx
<Button>Cerrar Tab</Button>
```

**After:**
```tsx
import { useTranslate } from 'react-admin';

const MyComponent = () => {
  const translate = useTranslate();
  return <Button>{translate('tab.action.close')}</Button>;
};
```

### Step 3: Add to Translation Files

**es.json:**
```json
{
  "tab.action.close": "Cerrar Tab"
}
```

**en.json:**
```json
{
  "tab.action.close": "Close Tab"
}
```

## React-Admin Default Translations

React-admin comes with built-in translations. To override or extend them:

```tsx
// main.tsx
import spanishMessages from 'ra-language-spanish';
import englishMessages from 'ra-language-english';

const i18nProvider = polyglotI18nProvider(
  locale => ({
    ...locale === 'es' ? spanishMessages : englishMessages,
    ...require(`./i18n/${locale}.json`)
  }),
  'es' // default locale
);
```

## Best Practices

### 1. Consistent Naming
Use hierarchical keys:
- `domain.subdomain.key`
- `tab.status.created`
- `product.action.add`

### 2. Avoid Duplication
Reuse common translations:
```json
{
  "common.save": "Guardar",
  "common.cancel": "Cancelar",
  "common.delete": "Eliminar"
}
```

### 3. Context-Specific Keys
When the same word has different meanings:
```json
{
  "tab.close": "Cerrar Tab",      // Close a tab
  "window.close": "Cerrar Ventana" // Close a window
}
```

### 4. Pluralization
Use separate keys for singular/plural:
```json
{
  "product.count.one": "%{count} producto",
  "product.count.other": "%{count} productos"
}
```

## Testing Translations

### 1. Switch Languages at Runtime

The language toggle in the sidebar allows testing both languages:
- Click the flag icon (🇪🇸 or 🇺🇸)
- Select desired language
- All text should update immediately

### 2. Check for Missing Keys

If a translation key is missing, react-admin will display the key itself:
```
// If this appears on screen:
tab.action.some_missing_key

// It means the key is not in your translation file
```

### 3. Verify Interpolation

Test dynamic values:
```tsx
translate('tab.products.display.showing_results', { 
  displayed: 0, 
  total: 0 
});
// Should handle edge cases like zero values
```

## Migration Tasks

### Immediate Actions Needed

1. **Audit Existing Code**
   - Search for hardcoded Spanish/English strings
   - List all untranslated text
   - Prioritize by user visibility

2. **Create Translation Keys**
   - Add missing keys to both `es.json` and `en.json`
   - Ensure consistency between files
   - Use meaningful, hierarchical keys

3. **Update Components**
   - Replace hardcoded strings with `translate()` calls
   - Test each component in both languages
   - Verify interpolation works correctly

4. **Document Custom Keys**
   - Keep this guide updated
   - Document any domain-specific translation patterns
   - Share with team members

## Language Configuration Backend

### Default Language for Tenants

All tenants now default to Spanish (es):

**Migration Command** (runs on deployment):
```bash
php artisan tenants:migrate-languages
```

**New Tenants:**
Automatically assigned Spanish as primary language via Eloquent boot event.

**API Response:**
```json
{
  "tenant": {
    "id": "uuid",
    "name": "My Restaurant",
    "settings": {
      "primary_language": {
        "id": 2,
        "code": "es",
        "name": "Spanish",
        "native_name": "Español"
      }
    }
  }
}
```

## Resources

- [react-admin i18n Documentation](https://marmelab.com/react-admin/Translation.html)
- [Polyglot.js (underlying library)](https://airbnb.io/polyglot.js/)
- [ra-language-spanish](https://github.com/marmelab/react-admin/tree/master/packages/ra-language-spanish)

## Next Steps

1. Run the tenant migration command:
   ```bash
   cd dash-backend
   sail artisan tenants:migrate-languages
   ```

2. Test language switching in the UI

3. Begin systematic translation of remaining hardcoded strings

4. Consider using a translation management tool (e.g., i18next, Lokalise) for larger scale

