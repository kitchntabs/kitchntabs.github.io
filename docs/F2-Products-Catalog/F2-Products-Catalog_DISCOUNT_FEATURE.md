---
layout: default
title: F2-Products-Catalog DISCOUNT FEATURE
---

# Discount Feature - Technical Documentation

## Overview

The discount feature allows applying optional discounts to orders within the Tab system. Discounts can be entered as either a **percentage** or a **fixed amount**, and are calculated and stored at the order level.

## Architecture

### Database Schema

**Table: `orders`** (Migration: `2025_11_27_134139_add_discount_fields_to_orders_table.php`)

| Field | Type | Description |
|-------|------|-------------|
| `subtotal` | decimal(10,2) | Order subtotal before discount |
| `discount_type` | string, nullable | Either `'percentage'` or `'fixed'` |
| `discount_value` | decimal(10,2), nullable | The discount value (percentage 0-100 or fixed amount) |
| `discount_amount` | decimal(10,2), nullable | Calculated discount amount in currency |
| `discount_reason` | string, nullable | Optional reason for the discount |

### Backend Components

#### Order Model (`domain/app/Models/Order/Order.php`)

**Constants:**
```php
const DISCOUNT_TYPE_PERCENTAGE = 'percentage';
const DISCOUNT_TYPE_FIXED = 'fixed';
```

**Methods:**
- `calculateDiscountAmount(float $subtotal, ?string $type, ?float $value): float` - Calculates the discount amount based on type and value
- `applyDiscount(string $type, float $value, ?string $reason = null): void` - Applies a discount to the order
- `removeDiscount(): void` - Removes any applied discount

**Fillable Fields:**
```php
'subtotal', 'discount_type', 'discount_value', 'discount_amount', 'discount_reason'
```

#### Tab Controller (`domain/app/Http/Controllers/API/Tabs/TabController.php`)

The `_update` method handles discount data from the request:
1. Extracts discount fields from validated request
2. Passes discount data to `handleOrderUpdate()` or applies directly via `applyDiscount()`
3. Returns updated discount info in the response

**Request Validation** (`domain/app/Http/Request/Tab/TabRequest.php`):
```php
'discount_type' => 'nullable|string|in:percentage,fixed',
'discount_value' => 'nullable|numeric|min:0',
'discount_reason' => 'nullable|string|max:255',
```

#### Tab Resource (`domain/app/Http/Resources/Tab/TabResource.php`)

Returns discount fields in API response:
```php
'subtotal' => $this->order->subtotal,
'discount_type' => $this->order->discount_type,
'discount_value' => $this->order->discount_value,
'discount_amount' => $this->order->discount_amount,
'discount_reason' => $this->order->discount_reason,
```

### Frontend Components

#### DiscountSection (`apps/dash/src/components/tab2/components/DiscountSection.tsx`)

An isolated, reusable component for discount input:

**Features:**
- Collapsible UI with expand/collapse toggle
- Type selector: Percentage or Fixed Amount
- Value input with appropriate constraints
- Optional reason field
- Clear discount button
- Real-time discount calculation display

**Props:**
```typescript
interface DiscountSectionProps {
    method?: 'create' | 'edit' | 'show';
}
```

**Key Implementation Details:**
- Uses `useEditContext` to get tab record data in edit mode
- Uses `useRef` to prevent re-initialization (avoids infinite loops)
- Falls back to record values when form values are undefined
- Integrates with react-hook-form via `Controller` components

#### OrderSummary (`apps/dash/src/components/tab2/components/OrderSummary.tsx`)

Displays order totals including discount:
- Subtotal (before discount)
- Discount amount (if applied) with type indicator
- Service fee (calculated on amount after discount)
- Final total

#### ITab Interface (`apps/dash/src/components/tab/interfaces/ITab.ts`)

```typescript
order?: {
    // ... other fields
    subtotal: string | number;
    discount_type: 'percentage' | 'fixed' | null;
    discount_value: string | number | null;
    discount_amount: string | number;
    discount_reason: string | null;
    // ...
}
```

### Email/Print Template

**Template:** `resources/views/tab/tab.blade.php`

Displays discount in receipt when present:
```blade
@if(!empty($tab['discount_amount']))
    <div>
        <span>Descuento 
            @if($tab['discount_type'] === 'percentage')
                ({{ $tab['discount_value'] }}%)
            @endif
        </span>
        <span style="color: #dc3545;">-{{ $tab['discount_amount'] }}</span>
    </div>
    @if(!empty($tab['discount_reason']))
        <small>{{ $tab['discount_reason'] }}</small>
    @endif
@endif
```

## Calculation Logic

### Discount Amount Calculation

```typescript
// Frontend (utils.tsx)
const calculateDiscountAmount = (subtotal: number, type: string, value: number): number => {
    if (type === 'percentage') {
        return Math.min((subtotal * value) / 100, subtotal); // Cap at 100%
    }
    if (type === 'fixed') {
        return Math.min(value, subtotal); // Cap at subtotal
    }
    return 0;
};
```

```php
// Backend (Order.php)
public function calculateDiscountAmount(float $subtotal, ?string $type, ?float $value): float
{
    if (!$type || !$value || $value <= 0) {
        return 0;
    }
    
    if ($type === self::DISCOUNT_TYPE_PERCENTAGE) {
        return min(($subtotal * $value) / 100, $subtotal);
    }
    
    if ($type === self::DISCOUNT_TYPE_FIXED) {
        return min($value, $subtotal);
    }
    
    return 0;
}
```

### Service Fee Calculation

Service fee is calculated on the **amount after discount**:

```php
$amountAfterDiscount = $subtotal - $discountAmount;
$serviceFeeAmount = $amountAfterDiscount * $serviceFeePercentage;
$total = $amountAfterDiscount + $serviceFeeAmount;
```

## Data Flow

### Creating/Editing a Tab with Discount

1. **Frontend**: User expands DiscountSection, selects type, enters value
2. **Form Submit**: Discount fields sent as `discount_type`, `discount_value`, `discount_reason`
3. **Backend Validation**: TabRequest validates the discount fields
4. **Order Update**: TabController calls `handleOrderUpdate()` with discount data
5. **Discount Applied**: Order model's `applyDiscount()` calculates and stores discount
6. **Response**: Updated order with discount info returned via TabResource

### Displaying Discount

1. **API Response**: Tab data includes order with discount fields
2. **DiscountSection**: Reads record values, initializes form fields
3. **OrderSummary**: Watches form values, displays calculated totals
4. **Receipt/Email**: Template conditionally renders discount section

## Files Modified/Created

### Backend
- `domain/database/migrations/orders/2025_11_27_134139_add_discount_fields_to_orders_table.php` (created)
- `domain/app/Models/Order/Order.php` (modified)
- `domain/app/Http/Controllers/API/Tabs/TabController.php` (modified)
- `domain/app/Http/Request/Tab/TabRequest.php` (modified)
- `domain/app/Http/Resources/Tab/TabResource.php` (modified)
- `domain/app/Services/Tabs/TabOrderManagementTrait.php` (modified)
- `resources/views/tab/tab.blade.php` (modified)

### Frontend
- `apps/dash/src/components/tab2/components/DiscountSection.tsx` (created)
- `apps/dash/src/components/tab2/components/OrderSummary.tsx` (modified)
- `apps/dash/src/components/tab2/EditOrder.tsx` (modified)
- `apps/dash/src/components/tab2/CreateOrder.tsx` (modified)
- `apps/dash/src/components/tab2/index.tsx` (modified)
- `apps/dash/src/components/tab2/utils.tsx` (modified)
- `apps/dash/src/components/tab/interfaces/ITab.ts` (modified)
- `apps/dash/src/schemas/tab/tabSchema.tsx` (modified)

## Usage Example

### Applying a 10% Discount
```json
{
    "discount_type": "percentage",
    "discount_value": 10,
    "discount_reason": "Cliente frecuente"
}
```

### Applying a Fixed $5000 Discount
```json
{
    "discount_type": "fixed",
    "discount_value": 5000,
    "discount_reason": "Cortesía del chef"
}
```

### API Response with Discount
```json
{
    "order": {
        "subtotal": "10000.00",
        "discount_type": "percentage",
        "discount_value": "10.00",
        "discount_amount": "1000.00",
        "discount_reason": "Cliente frecuente",
        "total_amount": "9000.00"
    }
}
```
