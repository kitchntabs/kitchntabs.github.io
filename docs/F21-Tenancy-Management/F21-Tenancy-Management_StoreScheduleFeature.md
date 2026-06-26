---
description: Store Schedule Feature Documentation
---

# Store Schedule Feature Documentation

## Overview

The Store Schedule feature allows tenants to define their operating hours for each day of the week. This system automatically manages the store's open/closed status based on the configured schedule and timezone, while also providing manual override capabilities.

## Architecture

The feature is implemented across the full stack:
- **Backend (Laravel)**: Models, migrations, and logic to handle schedule persistence and status checks.
- **Frontend (React)**: UI components for configuring the schedule within the Tenant Settings.
- **Configuration**: System-wide settings to enable/disable the feature and set defaults.

### 1. Configuration (`config/tenant_schedule.php`)

The system is configurable via environment variables:

| Key | Environment Variable | Default | Description |
|-----|---------------------|---------|-------------|
| `enabled` | `TENANT_SCHEDULE_ENABLED` | `true` | Master switch for the schedule system. |
| `check_interval` | `TENANT_SCHEDULE_CHECK_INTERVAL` | `5` | Frequency (in minutes) for the automated status check job. |
| `default_timezone` | `TENANT_DEFAULT_TIMEZONE` | `America/Santiago` | Fallback timezone for tenants. |

### 2. Backend Implementation

#### Models

**`Domain\App\Models\Extended\Tenant.php`**
The `Tenant` model has been extended to include:
- **Relationships**:
  - `schedules()`: HasMany relationship with `TenantSchedule`.
- **Attributes**:
  - `is_open` (boolean): Current open status.
  - `schedule_enabled` (boolean): Whether the schedule logic is active.
  - `manually_closed` (boolean): Override flag to force close.
  - `manually_opened` (boolean): Override flag to force open.
  - `timezone` (string): Tenant's specific timezone.
  - `last_schedule_check` (datetime): Timestamp of the last automated check.
- **Key Methods**:
  - `isCurrentlyOpen()`: Determines status based on schedule and manual overrides.
  - `isInSlot()`: Checks if current time (in tenant's timezone) falls within any active schedule slot.
  - `openStore()` / `closeStore()`: Handles manual status changes, setting appropriate override flags.
  - `getNextOpenTime()`: Calculates the next scheduled opening time.

**`Domain\App\Models\Extended\TenantSchedule.php`**
Represents a single schedule slot:
- **Attributes**: `day_of_week` (0-6), `open_time`, `close_time`, `is_active`.
- **Logic**: Handles time comparison, including overnight shifts (e.g., 10 PM to 2 AM).

#### Scheduler & Horizontal Scaling

The automated status updates are handled by the Laravel Scheduler and Horizon.

**Job: `Domain\App\Jobs\UpdateTenantOpenStatus`**
- **Trigger**: Dispatched every 5 minutes from `app/Console/Kernel.php`.
- **Mechanism**:
  1.  Iterates through all tenants with `schedule_enabled = true`.
  2.  Calculates new status based on current time (in tenant's timezone).
  3.  Updates `is_open` if changed, respecting manual overrides.

**Horizontal Scaling Safety (`onOneServer`)**
The application runs in a horizontally scaled environment (ECS Fargate) where multiple containers are running simultaneously. Each container runs its own `schedule:work` process via Supervisor.

To prevent "Split Brain" issues where every container dispatches a copy of the job (resulting in duplicate processing), we rely on:

1.  **Atomicity (`onOneServer`)**:
    In `Kernel.php`, the job is scheduled with `->onOneServer()`.
    *   **How it works**: Before dispatching the job, the scheduler attempts to acquire an atomic lock in the default cache store (Redis).
    *   **Result**: Only **one** container successfully acquires the lock and dispatches the job to the queue. The other containers skip this step for the current minute.
    *   **Requirement**: A centralized cache driver (Redis/Memcached) must be configured, which is true for our environment (Redis).

2.  **Job Uniqueness (`ShouldBeUnique`)**:
    The `UpdateTenantOpenStatus` job implements the `ShouldBeUnique` interface.
    *   **How it works**: When the job is dispatched, Laravel checks if a lock for `uniqueId()` ('global_tenant_schedule_update') already exists in the cache.
    *   **Result**: Even if a race condition occurred and `onOneServer` failed (unlikely), the second protection layer ensures only **one instance** of the job can exist in the queue or be processing at any given time.

### 3. Frontend Implementation

#### Components

**`TenantStoreSchedule.tsx`**
A custom field component for `react-admin` that provides a user-friendly interface for schedule management.
- **Features**:
  - Enable/Disable toggle for the entire schedule.
  - Day-by-day toggle.
  - Multiple time slots per day.
  - Time pickers for Start and End times.
  - Support for adding/removing slots.
  - Read-only view for 'list' and 'show' contexts.
- **Data Handling**:
  - Fetches existing `schedules` from the record.
  - Flattens the complex local state into a list of schedule objects for API submission.

#### Schema

**`tenant_tenant.tsx`**
Defines the Tenant resource schema, including the new fields:
- `timezone`: A dropdown of available timezones.
- `schedule_enabled`: Uses the `TenantStoreSchedule` component.
- `store_status`: (presumably `TenantStoreStatus`) to display current status.

#### Resources

**`StoreResources.tsx`**
Defines the `tenant/store` and `tenant/store/schedule` resources for the admin interface.

## Usage Flow

1.  **Setup**: The tenant selects their `Timezone` and enables `Store Schedule` in their settings.
2.  **Configuration**: The tenant defines opening hours for each day of the week using the `TenantStoreSchedule` component.
3.  **Automated Check**:
    - Every 5 minutes, the centralized scheduler triggers the `UpdateTenantOpenStatus` job.
    - Horizon workers pick up the job.
    - The job iterates all active tenants and updates their status if needed.
4.  **Manual Override**:
    - If a tenant manually clicks "Open Store" while outside scheduled hours, `manually_opened` is set to true.
    - If a tenant manually clicks "Close Store" while during scheduled hours, `manually_closed` is set to true.
    - These overrides persist until the next schedule state change (or manual reversal).
