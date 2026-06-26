---
layout: default
title: F15-Notifications-Messaging EMAIL SYSTEM TESTS
---

# Email System Test Suite Documentation

This document describes the comprehensive test suite for the bounce, complaint, and unsubscribe features.

## Overview

The test suite covers three main areas:
1. **Bounce & Complaint Handling** - EmailBounceService functionality
2. **Email Subscriptions** - Subscription management and unsubscribe logic
3. **Email Filtering** - Integration with AppNotificationBuilder

## Test Files

### 1. EmailBounceServiceTest.php
**Location:** `tests/Feature/Email/EmailBounceServiceTest.php`

**Coverage:** EmailBounceService business logic

**Test Cases:**
- ✅ Record hard bounces (permanent failures)
- ✅ Record soft bounces (temporary failures)
- ✅ Increment bounce counts on multiple bounces
- ✅ Auto-upgrade soft to hard bounce after threshold (3 bounces)
- ✅ Record complaints (spam reports)
- ✅ Suppress hard bounced emails from future sends
- ✅ Suppress complained emails from future sends
- ✅ Allow soft bounced emails (temporary issues)
- ✅ Allow clean emails (no issues)
- ✅ Get bounce statistics by tenant
- ✅ Process SNS bounce notifications
- ✅ Process SNS complaint notifications
- ✅ Handle invalid email addresses gracefully
- ✅ Remove suppression status
- ✅ Get list of suppressed emails
- ✅ Store metadata with bounces

**Run:**
```bash
sail artisan test --filter=EmailBounceServiceTest
```

---

### 2. EmailSubscriptionTest.php
**Location:** `tests/Feature/Email/EmailSubscriptionTest.php`

**Coverage:** EmailSubscription model and business logic

**Test Cases:**
- ✅ Create subscription records
- ✅ Auto-generate unsubscribe tokens
- ✅ Find subscriptions by token
- ✅ Handle invalid tokens
- ✅ Unsubscribe with reason and feedback
- ✅ Unsubscribe without feedback
- ✅ Resubscribe users
- ✅ Check subscription status by email
- ✅ Check unsubscribe status
- ✅ Get or create subscription (idempotent)
- ✅ Generate unsubscribe URLs
- ✅ Scope queries (subscribed, unsubscribed, by tenant, by type)
- ✅ Store metadata as JSON
- ✅ Bulk unsubscribe operations
- ✅ Validate email format
- ✅ Prevent duplicate subscriptions (unique constraint)

**Run:**
```bash
sail artisan test --filter=EmailSubscriptionTest
```

---

### 3. UnsubscribeControllerTest.php
**Location:** `tests/Feature/Email/UnsubscribeControllerTest.php`

**Coverage:** HTTP endpoints for unsubscribe flow

**Test Cases:**
- ✅ Show unsubscribe form with valid token
- ✅ Show error for invalid token
- ✅ Process unsubscribe request
- ✅ Unsubscribe without feedback (reason only)
- ✅ Require reason for unsubscribe
- ✅ Validate reason is in allowed list
- ✅ Show already unsubscribed message
- ✅ Resubscribe functionality
- ✅ Error when resubscribing active subscription
- ✅ Track IP and user agent on unsubscribe
- ✅ Redirect to tenant website after unsubscribe (if configured)
- ✅ One-click unsubscribe (List-Unsubscribe header)
- ✅ Handle concurrent unsubscribe requests (idempotent)
- ✅ Log unsubscribe actions
- ✅ Sanitize feedback input (XSS prevention)
- ✅ Respect tenant isolation
- ✅ Show preferences page
- ✅ Update email preferences

**Run:**
```bash
sail artisan test --filter=UnsubscribeControllerTest
```

---

### 4. EmailSubscriptionHelperTest.php
**Location:** `tests/Unit/Email/EmailSubscriptionHelperTest.php`

**Coverage:** Helper methods for filtering and checking emails

**Test Cases:**
- ✅ Filter unsubscribed emails from list
- ✅ Filter hard bounced emails from list
- ✅ Filter complained emails from list
- ✅ Allow soft bounced emails (temporary)
- ✅ Filter both unsubscribed and bounced
- ✅ Generate unsubscribe URLs
- ✅ Create subscription on URL generation if not exists
- ✅ Check if email can receive emails
- ✅ Get suppression reason (why email is blocked)
- ✅ Handle empty email lists
- ✅ Handle invalid emails
- ✅ Filter by subscription type (marketing vs transactional)
- ✅ Cache subscription checks for performance
- ✅ Bulk check multiple emails
- ✅ Return list health statistics

**Run:**
```bash
sail artisan test --filter=EmailSubscriptionHelperTest
```

---

### 5. AppNotificationBuilderFilteringTest.php
**Location:** `tests/Unit/Email/AppNotificationBuilderFilteringTest.php`

**Coverage:** Integration with notification system

**Test Cases:**
- ✅ Filter unsubscribed users from email notifications
- ✅ Filter bounced users from email notifications
- ✅ Filter both unsubscribed and bounced users
- ✅ Allow transactional emails to unsubscribed users
- ✅ Never send to bounced emails (even transactional)
- ✅ Log filtered recipients
- ✅ Handle soft bounces differently (allow but throttle)
- ✅ Apply rate limiting to soft bounces
- ✅ Track suppression metrics

**Run:**
```bash
sail artisan test --filter=AppNotificationBuilderFilteringTest
```

---

## Running Tests

### Run All Email Tests
```bash
sail artisan test tests/Feature/Email tests/Unit/Email
```

### Run Specific Test Suite
```bash
# Bounce service tests
sail artisan test --filter=EmailBounceServiceTest

# Subscription tests
sail artisan test --filter=EmailSubscriptionTest

# Controller tests
sail artisan test --filter=UnsubscribeControllerTest

# Helper tests
sail artisan test --filter=EmailSubscriptionHelperTest

# Filtering tests
sail artisan test --filter=AppNotificationBuilderFilteringTest
```

### Run Single Test
```bash
sail artisan test --filter=it_can_record_a_hard_bounce
```

### Run with Coverage
```bash
sail artisan test --coverage --min=80
```

---

## Test Data Setup

### Factories

Two factories are included for generating test data:

**EmailDeliveryStatusFactory**
```php
// Basic
EmailDeliveryStatus::factory()->create();

// Hard bounced
EmailDeliveryStatus::factory()->hardBounced()->create();

// Soft bounced
EmailDeliveryStatus::factory()->softBounced()->create();

// Complained
EmailDeliveryStatus::factory()->complained()->create();

// With metadata
EmailDeliveryStatus::factory()
    ->withMetadata(['source' => 'test'])
    ->create();
```

**EmailSubscriptionFactory**
```php
// Basic subscribed
EmailSubscription::factory()->create();

// Unsubscribed
EmailSubscription::factory()->unsubscribed()->create();

// Unsubscribed with reason
EmailSubscription::factory()
    ->unsubscribedWith('too_many_emails', 'Feedback here')
    ->create();

// Transactional type
EmailSubscription::factory()->transactional()->create();

// Newsletter type
EmailSubscription::factory()->newsletter()->create();

// With metadata
EmailSubscription::factory()
    ->withMetadata(['source' => 'jumpseller'])
    ->create();
```

---

## Test Scenarios

### Scenario 1: Hard Bounce Flow
1. Email is sent to non-existent address
2. AWS SES returns permanent bounce
3. System records bounce with `status='bounced_hard'`
4. Email is added to suppression list
5. Future sends to this email are blocked

**Tested by:** `it_can_record_a_hard_bounce`, `it_suppresses_hard_bounced_emails`

---

### Scenario 2: Soft Bounce Upgrade
1. Email bounces due to "mailbox full" (temporary)
2. System records soft bounce
3. Email bounces again (count = 2)
4. Email bounces third time (count = 3)
5. System auto-upgrades to hard bounce
6. Email is suppressed

**Tested by:** `it_upgrades_soft_bounce_to_hard_after_threshold`

---

### Scenario 3: Complaint Flow
1. User marks email as spam
2. AWS SES sends complaint notification
3. System records complaint
4. Email is permanently suppressed
5. Cannot send future emails even if user resubscribes

**Tested by:** `it_can_record_a_complaint`, `it_suppresses_complained_emails`

---

### Scenario 4: Unsubscribe Flow
1. User clicks unsubscribe link in email
2. System shows unsubscribe form
3. User selects reason and provides feedback
4. System updates subscription status
5. User receives confirmation
6. Future marketing emails are blocked
7. Transactional emails still allowed

**Tested by:** Multiple tests in `UnsubscribeControllerTest`

---

### Scenario 5: Email Filtering Before Send
1. System prepares to send notification to 100 users
2. Filter removes 5 unsubscribed users
3. Filter removes 3 hard bounced users
4. Filter removes 2 complained users
5. Email sent to remaining 90 users
6. Metrics logged for monitoring

**Tested by:** Tests in `AppNotificationBuilderFilteringTest`

---

## Assertions Reference

### Common Assertions

```php
// Database assertions
$this->assertDatabaseHas('email_delivery_status', [...]);
$this->assertDatabaseMissing('email_subscriptions', [...]);

// HTTP assertions
$response->assertStatus(200);
$response->assertViewIs('email.unsubscribe.form');
$response->assertViewHas('subscription');
$response->assertSee('text in view');
$response->assertSessionHasErrors('field');

// Model assertions
$this->assertTrue($model->is_subscribed);
$this->assertFalse($service->shouldSuppressEmail($email));
$this->assertEquals('bounced_hard', $status->status);
$this->assertNotNull($subscription->unsubscribed_at);

// Collection assertions
$this->assertCount(3, $collection);
$this->assertContains('email@example.com', $collection);
$this->assertEmpty($collection);
```

---

## Mocking External Services

Tests **do not** require AWS services. All external dependencies are mocked:

```php
// Notification mocking
Notification::fake();

// Mail mocking
Mail::fake();

// Event mocking
Event::fake();

// Log verification
Log::shouldReceive('info')
    ->once()
    ->with('Message', ['context' => 'data']);
```

---

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          docker-compose up -d
          docker-compose exec -T app php artisan test tests/Feature/Email tests/Unit/Email
```

---

## Coverage Goals

| Component | Target Coverage | Current Status |
|-----------|----------------|----------------|
| EmailBounceService | 95% | ✅ Complete |
| EmailSubscription Model | 90% | ✅ Complete |
| UnsubscribeController | 85% | ✅ Complete |
| EmailSubscriptionHelper | 95% | ✅ Complete |
| Filtering Integration | 80% | ✅ Complete |

---

## Debugging Failed Tests

### View Test Output
```bash
sail artisan test --filter=TestName --debug
```

### Inspect Database State
```bash
sail artisan tinker
```
```php
// Check email status
EmailDeliveryStatus::where('email', 'test@example.com')->first();

// Check subscription
EmailSubscription::where('email', 'test@example.com')->first();
```

### Enable Query Log
```php
protected function setUp(): void
{
    parent::setUp();
    DB::enableQueryLog();
}

protected function tearDown(): void
{
    dump(DB::getQueryLog());
    parent::tearDown();
}
```

---

## Best Practices

1. **Use RefreshDatabase trait** - Ensures clean database state per test
2. **Use factories** - Generate realistic test data
3. **Test edge cases** - Empty inputs, invalid data, concurrent requests
4. **Test error conditions** - Invalid tokens, expired links, missing data
5. **Verify security** - XSS prevention, SQL injection, CSRF
6. **Mock external services** - Never call real AWS APIs in tests
7. **Keep tests isolated** - Each test should be independent
8. **Use descriptive names** - `it_can_record_a_hard_bounce` over `test_bounce`
9. **Assert specific values** - Don't just check `assertNotNull`
10. **Test both success and failure paths**

---

## Maintenance

### When Adding New Features

1. Write tests first (TDD approach)
2. Run existing tests to ensure no regressions
3. Update this documentation
4. Ensure coverage stays above 80%

### When Fixing Bugs

1. Write a failing test that reproduces the bug
2. Fix the bug
3. Verify test passes
4. Add test to appropriate test suite

---

## Support

For questions or issues with tests:
1. Check test output for specific error messages
2. Review this documentation for examples
3. Inspect test database state with Tinker
4. Check Laravel testing documentation: https://laravel.com/docs/testing

---

## Quick Reference Card

```bash
# Run all email tests
sail test tests/Feature/Email tests/Unit/Email

# Run specific test
sail test --filter=it_can_record_a_hard_bounce

# Run with coverage
sail test --coverage-html coverage

# Debug test
sail test --filter=TestName --debug

# Stop on failure
sail test --stop-on-failure

# Parallel execution
sail test --parallel
```
