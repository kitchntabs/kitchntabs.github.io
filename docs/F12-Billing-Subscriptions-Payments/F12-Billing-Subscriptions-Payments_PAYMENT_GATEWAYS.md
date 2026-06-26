# Payment Gateway Integration Guide

This document covers the integration of external payment gateways for tenancy billing in the DASH platform.

## Available Gateways

| Gateway | Identifier | Region | Currencies | Card Method |
|---------|------------|--------|------------|-------------|
| **Internal** | `internal` | - | All | Simulation |
| **REDBILL** | `rebill` | LATAM | ARS, BRL, CLP, COP, MXN | SDK tokenization |
| **Flow.cl** | `flow` | CL, PE, MX | CLP, PEN, MXN | Redirect/Widget/Email |

---

## Architecture

All payment gateways implement `PaymentGatewayContract`:

```
domain/app/Services/Payments/
├── Contracts/
│   └── PaymentGatewayContract.php
├── Internal/
│   └── InternalPaymentGatewayService.php
├── Rebill/
│   ├── RebillPaymentGatewayService.php
│   └── Traits/
│       ├── RebillApiTrait.php
│       ├── RebillCustomersTrait.php
│       ├── RebillSubscriptionsTrait.php
│       ├── RebillWebhookTrait.php
│       └── RebillPaymentRetryTrait.php
└── Flow/
    ├── FlowPaymentGatewayService.php
    └── Traits/
        ├── FlowApiTrait.php
        ├── FlowCustomersTrait.php
        ├── FlowSubscriptionsTrait.php
        └── FlowWebhookTrait.php
```

---

## Common Interface

All gateways expose these methods:

```php
// Identification
static getIdentifier(): string
static getDisplayName(): string
static getCapabilities(): array
static getWebhookEndpoint(): string

// Configuration
static getConnectionParamFormats(): array
verifyCredentials(): bool

// Payment Methods
createPaymentMethod(array $data): array
getPaymentMethod(string $externalId): ?array
deletePaymentMethod(string $externalId): bool

// Subscriptions
createSubscription(TenancySubscription $sub, TenancyPaymentMethod $pm): array
updateSubscription(TenancySubscription $sub, array $changes): array
cancelSubscription(TenancySubscription $sub, bool $atPeriodEnd): array

// Charges & Refunds
charge(string $paymentMethodId, int $amountInCents, string $currency, array $metadata): array
refund(string $transactionId, ?int $amountInCents, string $reason): array

// Webhooks
handleWebhook(string $eventType, array $payload): array
validateWebhookSignature(string $payload, string $signature): bool
```

---

## Configuration

### Environment Variables

```env
# REDBILL
REBILL_API_URL=https://api.rebill.com/v3
REBILL_API_KEY=your_api_key
REBILL_WEBHOOK_SECRET=your_webhook_secret
REBILL_ENVIRONMENT=sandbox
REBILL_PUBLIC_KEY=your_public_key

# Flow.cl
FLOW_API_URL=https://www.flow.cl/api
FLOW_API_KEY=your_api_key
FLOW_SECRET_KEY=your_secret_key
FLOW_ENVIRONMENT=sandbox
FLOW_CARD_REGISTRATION_METHOD=redirect
```

### Database Columns

| Table | Column | Purpose |
|-------|--------|---------|
| `tenancies` | `rebill_customer_id` | REDBILL customer mapping |
| `tenancies` | `flow_customer_id` | Flow customer mapping |
| `subscription_plans` | `rebill_plan_id` | REDBILL plan mapping |
| `subscription_plans` | `flow_plan_id` | Flow plan mapping |

---

## Webhook Endpoints

| Gateway | Endpoint | Signature Header |
|---------|----------|------------------|
| Internal | `/api/payments/webhooks/internal` | `X-Webhook-Signature` |
| REDBILL | `/api/payments/webhooks/rebill` | `X-Rebill-Signature` |
| Flow.cl | `/api/payments/webhooks/flow` | Token-based |

---

## Plan Synchronization

Sync local plans to payment gateways:

```php
// REDBILL
dispatch(new \App\Jobs\SyncRebillPlansJob());

// Flow.cl  
dispatch(new \App\Jobs\SyncFlowPlansJob());
```

---

## Related Documentation

- [REDBILL Integration](./REBILL_PAYMENT_GATEWAY.md)
- [Flow.cl Integration](./FLOW_PAYMENT_GATEWAY.md)
- [Tenancy Billing System](./TENANCY_BILLING_SYSTEM.md)
