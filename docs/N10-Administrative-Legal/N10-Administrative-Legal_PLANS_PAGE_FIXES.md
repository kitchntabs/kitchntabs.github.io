---
layout: default
title: N10-Administrative-Legal PLANS PAGE FIXES
---

# Plans Page Fixes - Currency Selector & Translations

## Summary of Changes

This document outlines all changes made to implement:
1. **Currency selector** for switching between CLP and USD pricing
2. **Fixed price formatting** to correctly display CLP (no decimals) vs USD (with decimals)
3. **Complete translation system** for plan names, features, and all UI text

---

## 1. Translation Files Updated

### English Translations (`en.tsx`)

Added comprehensive translation keys for plans:

```typescript
plans: {
    title: "Choose Your Plan",
    subtitle: "Start your free trial today. No credit card required.",
    getStarted: "Get Started",
    footer: "All plans include a free trial period. Cancel anytime.",
    loading: "Loading plans...",
    error: "Failed to load subscription plans. Please try again later.",
    noPlans: "No plans available at this time.",
    
    // Plan names by slug
    planNames: {
        "free-trial": "Free Trial",
        "basic-plan": "Basic Plan",
        "professional-plan": "Professional Plan",
        "enterprise-plan": "Enterprise Plan"
    },
    
    // Plan descriptions by slug
    planDescriptions: {
        "free-trial": "30-day free trial with basic features",
        "basic-plan": "Perfect for individuals and small teams",
        "professional-plan": "Advanced features for growing businesses",
        "enterprise-plan": "Complete solution for large organizations"
    },
    
    // Feature translations
    features: {
        basic_features: "Basic features",
        email_support: "Email support",
        one_store: "1 store",
        three_users: "3 users",
        fifty_products: "50 products",
        unlimited_stores: "Unlimited stores",
        unlimited_users: "Unlimited users",
        unlimited_products: "Unlimited products",
        priority_support: "Priority support",
        advanced_analytics: "Advanced analytics",
        custom_domain: "Custom domain",
        api_access: "API access",
        white_label: "White label"
    },
    
    // Billing cycles
    billingCycle: {
        monthly: "per month",
        yearly: "per year",
        monthly_short: "/mo",
        yearly_short: "/yr"
    },
    
    // Trial badge
    trialDays: "%{days}-day free trial",
    
    // Badges
    popular: "Popular",
    selected: "Selected"
}
```

### Spanish Translations (`es.tsx`)

Added matching Spanish translations with proper Spanish text:

```typescript
plans: {
    title: "Elige Tu Plan",
    subtitle: "Comienza tu prueba gratuita hoy. No se requiere tarjeta de crédito.",
    // ... (complete Spanish equivalents)
    billingCycle: {
        monthly: "por mes",
        yearly: "por año",
        monthly_short: "/mes",
        yearly_short: "/año"
    },
    trialDays: "Prueba gratis %{days} días",
}
```

---

## 2. Plans.tsx - Added Currency Selector

### New Imports
```typescript
import { useState } from 'react';
import { ToggleButton, ToggleButtonGroup } from '@mui/material';
import { useCurrencies } from '../../hooks/useSystemConfig';
```

### Added Currency State Management
```typescript
const { data: currencies } = useCurrencies();
const defaultCurrency = currencies?.[0]?.code || 'CLP';
const [selectedCurrency, setSelectedCurrency] = useState<string>(defaultCurrency);

const handleCurrencyChange = (
    event: React.MouseEvent<HTMLElement>,
    newCurrency: string | null
) => {
    if (newCurrency !== null) {
        setSelectedCurrency(newCurrency);
    }
};
```

### Added Currency Selector UI
```typescript
{/* Currency Selector */}
{currencies && currencies.length > 1 && (
    <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
        <ToggleButtonGroup
            value={selectedCurrency}
            exclusive
            onChange={handleCurrencyChange}
            aria-label="currency selector"
            size="small"
        >
            {currencies.map((currency) => (
                <ToggleButton 
                    key={currency.code} 
                    value={currency.code}
                    aria-label={currency.code}
                >
                    {currency.code}
                    {currency.symbol && ` (${currency.symbol})`}
                </ToggleButton>
            ))}
        </ToggleButtonGroup>
    </Box>
)}
```

### Pass Currency to Display Component
```typescript
<PublicSubscriptionPlansDisplay
    plans={plans}
    // ... other props
    currencyCode={selectedCurrency}  // Dynamic currency
/>
```

---

## 3. PublicSubscriptionPlansDisplay.tsx - Major Updates

### Added Translation Hook
```typescript
import { useTranslate } from '../hooks/usePolyglotTranslation';

const translate = useTranslate();
```

### Fixed Price Formatting
**OLD (INCORRECT):**
```typescript
const formatPrice = (price: number, currencyCode: string = 'CLP'): string => {
    const amount = price / 100;  // Always divided by 100 (WRONG for CLP)
    if (currencyCode === 'CLP') {
        return `$${amount.toLocaleString('es-CL', { minimumFractionDigits: 0 })}`;
    }
    return `$${amount.toFixed(2)}`;
};
```

**NEW (CORRECT):**
```typescript
/**
 * Format price based on currency type
 * - CLP: Prices are stored as full amounts (e.g., 4990 = $4,990)
 * - USD: Prices are stored in cents (e.g., 600 = $6.00)
 */
const formatPrice = (price: number, currencyCode: string = 'CLP'): string => {
    if (currencyCode === 'CLP') {
        // CLP prices are stored as full amounts, no division needed
        return `$${price.toLocaleString('es-CL', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    } else if (currencyCode === 'USD') {
        // USD prices are stored in cents, divide by 100
        const amount = price / 100;
        return `$${amount.toFixed(2)}`;
    }
    // Default: assume cents format for other currencies
    const amount = price / 100;
    return `$${amount.toFixed(2)}`;
};
```

### Translate Plan Names
**OLD:**
```typescript
<Typography>{plan.name}</Typography>
```

**NEW:**
```typescript
<Typography>
    {translate(`plans.planNames.${plan.slug}`) || plan.name}
</Typography>
```

### Translate Billing Cycle
**OLD:**
```typescript
<Typography>
    /{plan.billing_cycle === 'monthly' ? 'mes' : 'año'}
</Typography>
```

**NEW:**
```typescript
<Typography>
    {translate(`plans.billingCycle.${plan.billing_cycle}_short`)}
</Typography>
```

### Translate Features
**OLD:**
```typescript
<Typography>{feature}</Typography>
```

**NEW:**
```typescript
<Typography>
    {translate(`plans.features.${feature}`) || feature}
</Typography>
```

### Translate Trial Badge
**OLD:**
```typescript
<Chip label={`Prueba gratis ${plan.trial_days} días`} />
```

**NEW:**
```typescript
<Chip label={translate('plans.trialDays', { days: plan.trial_days })} />
```

### Translate Badges
**OLD:**
```typescript
<Chip label="Popular" />
<Chip label="Selected" />
```

**NEW:**
```typescript
<Chip label={translate('plans.popular')} />
<Chip label={translate('plans.selected')} />
```

### Translate Messages
```typescript
// Loading
{translate('plans.loading')}

// Error
{translate('plans.error')}

// No plans
{translate('plans.noPlans')}
```

---

## 4. Price Display Examples

### Before (INCORRECT):
- **API Response:** `prices: { CLP: 4990, USD: 6 }`
- **Display:** "$49.90 /mes" (WRONG - divided 4990 by 100)

### After (CORRECT):
- **API Response:** `prices: { CLP: 4990, USD: 600 }`
- **CLP Display:** "$4,990 /mes" ✓ (no division, integer format)
- **USD Display:** "$6.00 /mo" ✓ (divided by 100, 2 decimals)

---

## 5. Translation Key Structure

### Plan Names
```
plans.planNames.{slug}
Example: plans.planNames.basic-plan → "Basic Plan" / "Plan Básico"
```

### Features
```
plans.features.{feature_key}
Example: plans.features.email_support → "Email support" / "Soporte por email"
```

### Billing Cycles
```
plans.billingCycle.monthly_short → "/mo" / "/mes"
plans.billingCycle.yearly_short → "/yr" / "/año"
```

### Trial Days (with variable)
```
plans.trialDays → "%{days}-day free trial" / "Prueba gratis %{days} días"
Usage: translate('plans.trialDays', { days: 30 })
```

---

## 6. Currency Selector Behavior

1. **Default Currency:** Uses first currency from system config or 'CLP'
2. **Visibility:** Only shows if more than 1 currency available
3. **Toggle Button Group:** Clean UI for currency switching
4. **Real-time Update:** Changes price display immediately
5. **Persists Selection:** State maintained during component lifecycle

---

## 7. Testing Checklist

- [ ] Currency selector appears when multiple currencies available
- [ ] CLP prices display without decimals (e.g., $4,990)
- [ ] USD prices display with 2 decimals (e.g., $6.00)
- [ ] Plan names translated correctly in both languages
- [ ] Features translated correctly
- [ ] Billing cycle labels translated (/mes vs /mo)
- [ ] Trial badge shows correct number of days
- [ ] Popular and Selected badges translated
- [ ] Loading, error, and no plans messages translated
- [ ] Currency selection updates all plan prices
- [ ] Plans page title and subtitle translated

---

## 8. Files Modified

1. **dash-frontend/apps/kitchntabs-web/src/i18n/en.tsx** - Added English translations
2. **dash-frontend/apps/kitchntabs-web/src/i18n/es.tsx** - Added Spanish translations
3. **dash-frontend/apps/kitchntabs-web/src/components/pages/Plans.tsx** - Added currency selector
4. **dash-frontend/apps/kitchntabs-web/src/components/billing/PublicSubscriptionPlansDisplay.tsx** - Fixed formatting and added translations

---

## 9. API Response Structure Reference

```json
{
  "subscription_plans": [
    {
      "id": 1,
      "slug": "free-trial",
      "name": "Free Trial",
      "price": 0,
      "prices": {
        "CLP": 0,
        "USD": 0
      },
      "billing_cycle": "monthly",
      "trial_days": 30,
      "features": ["basic_features", "email_support"],
      "is_popular": false
    },
    {
      "id": 2,
      "slug": "basic-plan",
      "name": "Basic Plan",
      "price": 6990,
      "prices": {
        "CLP": 4990,
        "USD": 600
      },
      "billing_cycle": "monthly",
      "trial_days": 15,
      "features": ["one_store", "three_users", "fifty_products"],
      "is_popular": true
    }
  ]
}
```

---

## 10. Future Enhancements

- Add annual/monthly billing cycle toggle
- Add discount calculation for annual plans
- Add plan comparison table
- Add FAQ section per plan
- Add testimonials per plan tier
- Add custom plan builder for enterprise
