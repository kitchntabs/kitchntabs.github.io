---
layout: default
title: F12-Billing-Subscriptions-Payments PAYMENT-GATEWAY-TESTS
---


# Test gateway connectivity
php artisan gateways:test

# Test specific gateway
php artisan gateways:test --gateway=flow
php artisan gateways:test --gateway=rebill

# Run gateway tests
php artisan test --filter=PaymentGatewayTest
# Run only external API tests (requires valid credentials)
php artisan test --filter=PaymentGatewayTest --group=external

php artisan gateways:sync-plans --sync

# Basic gateway tests (no database needed)
sail artisan test --filter=PaymentGatewayTest
# External API tests only
sail artisan test --filter=PaymentGatewayTest --group=external