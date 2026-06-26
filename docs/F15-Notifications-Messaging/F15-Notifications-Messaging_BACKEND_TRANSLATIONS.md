
# Backend Translation Guide

This document explains how translations are implemented in the Laravel backend, including file locations, implementation patterns, and email localization.

## Translation File Locations

Laravel supports two locations for translation files. **Both must be kept in sync!**

| Location | Priority | Description |
|----------|----------|-------------|
| `resources/lang/{locale}/` | **1st (Higher)** | Legacy location - Laravel checks this first |
| `lang/{locale}/` | 2nd | Modern location (Laravel 9+) |

> [!IMPORTANT]
> If a translation file exists in both locations, Laravel will use the one in `resources/lang/` first! Always update **both** locations when adding new translations.

### Translation Files Structure

```
dash-backend/
├── lang/
│   ├── en/
│   │   ├── emails.php       # Email translations
│   │   ├── validation.php   # Validation messages
│   │   └── ...
│   └── es/
│       ├── emails.php
│       ├── validation.php
│       └── ...
└── resources/
    └── lang/
        ├── en/              # Legacy - kept in sync with lang/en/
        ├── es/              # Legacy - kept in sync with lang/es/
        └── es.json          # JSON translations (react-admin)
```

## Basic Usage

### Using the `__()` Helper

```php
// Simple translation
$text = __('emails.welcome');  // Returns: "Bienvenido" (if locale is 'es')

// With replacements
$text = __('emails.subscription_welcome_subject', ['plan' => 'Starter']);
// Returns: "¡Bienvenido a Starter! Tu suscripción está activa"
```

### Translation File Format

```php
// lang/es/emails.php
<?php

return [
    'welcome' => 'Bienvenido',
    'subscription_welcome_subject' => '¡Bienvenido a :plan! Tu suscripción está activa',
    'price_label' => 'Precio',
];
```

### Setting the Locale

```php
use Illuminate\Support\Facades\App;

// Set locale globally
App::setLocale('es');

// Check current locale
$locale = App::getLocale();

// Get with fallback
$locale = App::getLocale() ?? 'es';
```

---

## Email Translations

### Mailable Class Pattern

```php
<?php

namespace App\Mail;

use Illuminate\Mail\Mailable;
use Illuminate\Support\Facades\App;

class SubscriptionWelcome extends Mailable
{
    protected string $userLocale;

    public function __construct(
        public User $user,
        public Tenancy $tenancy,
        ?string $locale = null
    ) {
        // Get locale from tenancy or default to 'es'
        $this->userLocale = $locale ?? $tenancy->primary_language ?? 'es';
        
        // Tell Laravel to use this locale for the mailable
        $this->locale($this->userLocale);
    }

    public function envelope(): Envelope
    {
        // Set locale before translation
        App::setLocale($this->userLocale);
        
        return new Envelope(
            subject: __('emails.subscription_welcome_subject', [
                'plan' => $this->subscription->subscriptionPlan?->name
            ]),
        );
    }

    public function content(): Content
    {
        // Set locale before rendering content
        App::setLocale($this->userLocale);
        
        return new Content(
            view: 'emails.subscription-welcome',
            with: [
                'name' => $this->user->name,
                'lang' => $this->userLocale,
                // ... other data
            ],
        );
    }
}
```

### Blade Template Usage

```blade
{{-- resources/views/emails/subscription-welcome.blade.php --}}
@extends('layouts.emails')

@section('content')
    <h1>{{ __('emails.subscription_welcome') }}, {{ $name }}!</h1>
    
    <p>{{ __('emails.thank_you_subscribing') }} <strong>{{ $tenancyName }}</strong>.</p>
    
    <table>
        <tr>
            <td>{{ __('emails.plan_label') }}:</td>
            <td>{{ $planName }}</td>
        </tr>
        <tr>
            <td>{{ __('emails.price_label') }}:</td>
            <td>{{ $planPrice }}</td>
        </tr>
    </table>
    
    <a href="{{ $loginUrl }}">{{ __('emails.access_account_button') }}</a>
@endsection
```

---

## Translation Keys Reference

### Email Translation Keys (`lang/{locale}/emails.php`)

| Key | Description |
|-----|-------------|
| `verify_subject` | Trial verification email subject |
| `welcome_subject` | Trial welcome email subject |
| `subscription_welcome_subject` | Subscription welcome email subject |
| `provisioning_failed_subject` | Provisioning failed email subject |
| `need_help` | "Need help getting started?" |
| `check_docs` | "Check our documentation" |

---

## Troubleshooting

### Translations Not Working

1. **Check both file locations exist:**
   ```bash
   ls -la lang/es/emails.php resources/lang/es/emails.php
   ```

2. **Verify the key exists in the file:**
   ```bash
   php artisan tinker --execute="print_r(include('lang/es/emails.php'));"
   ```

3. **Test translation directly:**
   ```bash
   php artisan tinker --execute="App::setLocale('es'); echo __('emails.subscription_welcome');"
   ```

4. **Clear all caches:**
   ```bash
   php artisan cache:clear
   php artisan view:clear
   php artisan config:clear
   php artisan optimize:clear
   ```

5. **Sync files if needed:**
   ```bash
   cp lang/es/emails.php resources/lang/es/emails.php
   cp lang/en/emails.php resources/lang/en/emails.php
   ```

### Queue Workers Not Picking Up Changes

After updating translation files, restart Horizon:
```bash
php artisan horizon:terminate
```

---

## Adding New Translations

1. Add the key to **both** locations:
   - `lang/{locale}/emails.php`
   - `resources/lang/{locale}/emails.php`

2. Use the key in your code:
   ```php
   __('emails.new_key')
   ```

3. Clear caches and restart workers:
   ```bash
   php artisan optimize:clear
   php artisan horizon:terminate
   ```
