# Price Formatting Service

A centralized service for formatting prices according to currency rules and locale preferences.

## Location
`app/Services/Billing/PriceFormattingService.php`

## Features

- **Zero-decimal currency support**: Handles CLP, JPY, KRW, and other currencies that don't use cents
- **Currency model integration**: Uses database `Currency` records for symbols and formats
- **Caching**: Caches currency lookups for performance
- **Resolution hierarchy**: Resolves currency/language from TenancyAccount → Tenant → User (future)

## Usage

### Basic Formatting

```php
use App\Services\Billing\PriceFormattingService;

$formatter = app(PriceFormattingService::class);

// Format with explicit currency
$formatted = $formatter->formatPrice(9990, 'CLP');  // "$9.990 CLP"
$formatted = $formatter->formatPrice(1999, 'USD');  // "$19.99 USD"

// Format with tenancy context (uses tenancy's primary_currency)
$formatted = $formatter->formatPrice(9990, null, $tenancy);
```

### Subscription Plan Formatting

```php
// Format a plan's price for a tenancy
$formatted = $formatter->formatPlanPrice($plan, $tenancy);
```

### Currency Resolution

```php
// Get currency code from hierarchy
$currency = $formatter->resolveCurrencyCode(null, $tenancy);  // "CLP"

// Get language code from hierarchy  
$language = $formatter->resolveLanguageCode(null, $tenancy);  // "es"
```

## Zero-Decimal Currencies

These currencies store prices as whole units (NOT in cents):

| Code | Currency |
|------|----------|
| CLP | Chilean Peso |
| JPY | Japanese Yen |
| KRW | South Korean Won |
| VND | Vietnamese Dong |
| IDR | Indonesian Rupiah |

## Resolution Hierarchy

The service resolves currency/language in this order:

1. **Explicitly provided** - If you pass a currency code directly
2. **TenancyAccount** - Uses `primary_currency` / `primary_language`
3. **Tenant** (future) - Will use tenant-specific settings
4. **User** (future) - Will use user preferences
5. **System default** - Falls back to `config('system.default_currency')`

## API Reference

### `formatPrice(int $amount, ?string $currencyCode, ?Tenancy $tenancy): string`
Formats a price amount for display.

### `formatPlanPrice($plan, ?Tenancy $tenancy): string`
Formats a subscription plan's price for a tenancy.

### `isZeroDecimalCurrency(string $code): bool`
Returns true if the currency doesn't use cents.

### `getCurrencyDetails(string $code): ?Currency`
Gets the Currency model (cached) for a currency code.

### `resolveCurrencyCode(?string $provided, ?Tenancy $tenancy): string`
Resolves the appropriate currency code from the hierarchy.

### `clearCache(?string $code = null): void`
Clears cached currency data.

## Example: In a Mailable

```php
class SubscriptionWelcome extends Mailable
{
    protected PriceFormattingService $priceFormatter;

    public function __construct(...)
    {
        $this->priceFormatter = app(PriceFormattingService::class);
    }

    public function content(): Content
    {
        $formattedPrice = $this->priceFormatter->formatPlanPrice(
            $this->subscription->subscriptionPlan,
            $this->tenancy
        );
        
        return new Content(
            view: 'emails.subscription-welcome',
            with: ['planPrice' => $formattedPrice]
        );
    }
}
```

## Future Enhancements

- Tenant-specific currency settings
- User preference overrides
- Locale-aware number formatting
- Currency symbol positioning (prefix/suffix)
