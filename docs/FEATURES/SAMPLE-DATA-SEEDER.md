# Sample data seeder

> **Command:** `php artisan kt:seed-sample-tenancy`
> **Layer:** `kitchntabs-backend-domain/app/Console/Commands/SeedSampleTenancyCommand.php`
> **Status:** ✅ Verified — 2 years, 2 restaurants, ~16,400 tabs in **21 seconds**.

Builds a demo tenancy with two restaurants and two years of realistic trading
history, so every report and dashboard has something worth looking at.

There are two shapes. **Standalone** builds a whole demo tenancy from scratch.
**`--into`** adds sample restaurants to a tenancy that already exists, leaving
its real restaurants, catalog and sales untouched.

```bash
# standalone: 2 years, ~10 sales/day/restaurant, 90 recent periods snapshotted
docker compose exec app php artisan kt:seed-sample-tenancy

# a quick one while iterating
docker compose exec app php artisan kt:seed-sample-tenancy --days=30 --snapshots=0

# into a tenancy you created by hand — adds 2 sample restaurants beside its own
docker compose exec app php artisan kt:seed-sample-tenancy --into=mi-grupo-real --days=365

# and undo exactly that
docker compose exec app php artisan kt:seed-sample-tenancy --into=mi-grupo-real --remove
```

Standalone signs in as `admin@sample-group.test` / `password`. `--into` creates
**no** user: the tenancy already has its own admins, and an account whose
password is `password` should not outlive the data it arrived with.

| Option | Default | Meaning |
|---|---|---|
| `--slug` | `sample-group` | Standalone mode: tenancy slug; re-running replaces **this** tenancy only |
| `--into` | — | Slug of an **existing** tenancy to add sample restaurants to |
| `--remove` | — | With `--into`, remove that tenancy's sample data instead |
| `--days` | `730` | Days of history |
| `--per-day` | `10` | Average sales/day/restaurant (before weighting) |
| `--snapshots` | `90` | Recent closed periods given a `widget_data` snapshot (`0`, a number, or `all`) |
| `--source` | `pinoywok` | Tenancy whose catalog is copied |
| `--force` | — | Allow running outside `local` (never production) |

## What it produces

| | |
|---|---|
| 1 tenancy, 2 tenants | `Sample · Centro`, `Sample · Providencia` |
| Catalog | A **copy** of PinoyWok's 77 products — every one with a photo — plus categories and modifier options |
| Per-tenant menu | Different random subsets (~50 and ~62 products), overlapping but distinct |
| Tills | 2 per restaurant — `Efectivo` and `Tarjeta de crédito` |
| Sales | ~16,400 tabs · ~40,700 line items · ~15,400 payments |
| Periods | 1,462 cash counts — one/day/tenant, closed with variance, **today's left open** |
| Snapshots | The 90 most recent closed periods per tenant |

## The Import / Remove buttons

A TenancyAdmin can do the same thing from **Account → Sample data**, and a
System admin can do it for any tenancy.

```
GET    api/sample-data/{tenancy}    status + progress
POST   api/sample-data/{tenancy}    queue an import   -> 202
DELETE api/sample-data/{tenancy}    queue a removal   -> 202
```

Both run as queued jobs (`SampleDataJob`, Horizon's `default` queue): a two-year
import writes ~73,000 rows in ~20 seconds, well past what a browser request
should hold open. The UI polls the status endpoint every 2.5s while a run is in
progress; progress lives in the cache, not a table, because it is worthless once
the run ends.

**Authorisation is two separate checks.** The route permission decides who may
call the endpoint at all (granted to `TenancyAdmin`; `System` needs no grant).
`SampleDataController::resolve()` then decides *which* tenancy they may point it
at — a TenancyAdmin is restricted to their own. Without the second check any
TenancyAdmin could pass another tenancy's id and wipe data that is not theirs.
The status code is the contract the UI translates from: **422** already has
sample data, **409** a run is in progress, **403** not your tenancy.

### What makes removal safe

Every row the import creates is marked, and removal only ever touches marked
rows — never a name, a slug, or a date range:

| Marker | Covers |
|---|---|
| `tenants.is_sample` | the sample restaurants. Everything tenant-scoped (tabs, orders, payments, cash counts, tills) is reached by sweeping those ids through the schema-derived dependent walk |
| `<catalog>.is_sample` | `products`, `categories`, `modifier_groups`, `modifier_options`, `prices` — tenancy-scoped, so they sit beside the real catalog and cannot be found by tenant id |

Order is load-bearing, and the failure it prevents is not obvious:

```
trading data  ->  products  ->  categories  ->  tenants
```

Creating a tenant provisions a category owned by it, and sample products point
at categories. Deleting the tenants first fails on
`categories_tenant_id_foreign`, because a category cannot go while a product
still references it.

**One case deliberately does not delete.** If a *real* product has come to
depend on a sample category, that category is promoted to real instead —
`is_sample` and `tenant_id` cleared, `tenancy_id` kept, which under the standard
resource policy makes it a shared tenancy-wide category. Deleting it would take
the customer's product with it (`products.category_id` is NOT NULL); refusing to
delete would leave the sample restaurants undeletable forever.

## Product images

The sample catalog ships with photos, committed to the domain repo so it looks
like a real menu on any machine and in any environment — no access to the source
tenancy's storage required.

```bash
# one-off, run by a developer; the output is committed
docker compose exec app php artisan kt:export-sample-images
```

Writes `kitchntabs-backend-domain/database/sample-data/`:

| | |
|---|---|
| `images/*.jpg` | 69 files, **2.9 MB** total, 700×700, 22–38 KB each |
| `images.json` | `SKU => filename` — 77 SKUs, since galleries are shared between products |

**Why re-encoded rather than copied.** PinoyWok's 69 primary images are **74 MB**
as uploaded (avg 907 KB, max 2.8 MB). That does not belong in a git repo. They
are thumbnails on a product card, so the exporter bounds the longest edge at
`--max-width` and re-encodes as JPEG at `--quality`, which lands the set at 2.9 MB
— a 96% reduction for output that is indistinguishable at the size it renders.
PNG alpha is flattened onto white, which JPEG cannot carry and which would
otherwise render black.

**Products without an image are excluded from the sample entirely.** 77 of
PinoyWok's 96 products have a primary image; the other 19 are not copied. A demo
catalog of grey placeholders is worse than a smaller one that looks real, and
the images are what the kiosk and the product cards are judged on.

**Categories ship without images** — not an omission: **zero** categories carry
an `image_path` in any tenancy, so there is nothing to export.

### How an image reaches a product

Not through a column. `product.gallery_id → Gallery →` Spatie media on the
`gallery` collection, with `custom_properties.is_primary` marking the one the UI
shows. The importer creates one gallery per product and attaches the baked file
with `preservingOriginal()` — **without it Spatie MOVES the file**, emptying the
repo of the very assets that were committed so this would work anywhere.

Removal deletes those galleries through Eloquent rather than SQL, because the
rows are only half of it: Spatie deletes the media records *and* the files (and
their generated conversions) from the model event. A raw `DELETE` would strand
an image on the media disk for every sample product, every run. Verified: the
media disk goes 25 MB → 0 on removal, and the 69 committed assets are untouched.

A real product that was pointed at a sample gallery has `gallery_id` released
rather than the gallery kept — unlike a category, losing the photo costs nothing,
and `gallery_id` is nullable where `category_id` is not.

## Why a command, not a seeder

`DatabaseSeeder` auto-discovers **every** `.php` under
`domain/database/seeders/<Folder>/` and runs it on every `db:seed` — which
includes the `$this->seed()` in each domain test's `setUp()`. Eighty thousand
rows there would add minutes to every single test. A command is opt-in.

## Design decisions

**The catalog is copied, not shared.** Products belong to a tenancy and reach
tenants through `product_tenants`, so pointing the demo at PinoyWok's rows would
make one tenancy's edits change another's menu — and make teardown dangerous.

**Realistic patterns, not uniform randomness.** Volume follows a weekday curve
(Sat ≫ Mon), a gentle yearly swell and per-day jitter; times follow two service
peaks. Verified in the data: lunch peaks at 12–13h and dinner at 19–21h **in
Santiago local time**, and Sat/Fri lead the week. Uniform randomness would make
the hour-of-day, day-of-week and trend reports flat noise — the same as having
no data in them.

**Local times converted to UTC.** The columns are `timestamp without time zone`
holding UTC, and the reports convert back to the venue's zone. Generating local
times and converting is what makes the lunch peak land at lunchtime.

**Bulk inserts, not Eloquent.** ~80k rows through models would be as many events,
and `CashCountObserver` would fire a full dashboard build for each of the ~1,460
closed periods. Snapshots are generated deliberately afterwards, for recent
periods only.

**Teardown is derived from the schema.** `tenants` has ~90 FK dependents and the
list changes with every migration. The command reads `pg_constraint` at runtime
and retries in passes to handle ordering, rather than carrying a hardcoded list
that would be wrong within a sprint.

---

## Notes: flaws, risks and improvements

Everything below was found while building this and verified against the running
schema. Split into what is wrong with **the seeder**, and what the seeder
*revealed* about the **platform**.

### A. Limitations of the seeder itself

**A1 · Modifiers are priced but not recorded.** A line item sometimes adds a
random modifier's price to `unit_price`, but no `order_product_modifiers` row is
written. So modifier *revenue* is realistic while modifier *structure* is
absent — any future report that groups by modifier will find nothing. Fixing it
means linking products to modifier groups (a pivot the copy does not populate
either).

**A2 · Cash count children are not generated.** `cash_count_pos_breakdowns` and
`cash_count_product_sales` stay empty, so the cash count show view's POS
Breakdown and Product Sales panels are blank for seeded periods even though the
totals are right. The data to derive them exists; it is just not written.

**A3 · Prices are tenancy-level, not per tenant.** Both restaurants charge
identically. Real groups differ by location, and a price-comparison report would
have nothing to show.

**A4 · Origin mix is fixed, not trending.** Channel weights are constant across
two years. A more useful demo would grow the marketplace share over time, so the
origin report has a story rather than a flat split.

**A5 · Cancellations are uniform at ~5%.** No bad weeks, no correlation with
volume. The "realistic + anomalies" option would have given the reports
something to actually surface.

**A6 · No `updated_at` drift.** Every row's `updated_at` equals its close time,
so anything auditing edit activity sees none.

**A7 · Prices were never copied.** ✅ *Fixed 2026-08-23.* The copy filtered
`prices` by `tenancy_id`, a column **no price populates** (0 of 192), so the
loop matched nothing and every sample line fell back to the flat `6990.0`
default in `buildSale()`. Seeded revenue looked plausible while every product
cost exactly the same, which quietly flattened every price-related report. Now
keyed off the products being copied: 65 distinct unit prices, 200–16,490.

**A8 · Modifier groups were copied from the whole database.** ✅ *Fixed
2026-08-23.* The copy read `modifier_groups` with no tenancy filter at all, on
the reasoning that none carried a `tenancy_id`. That survived only because the
standalone teardown deleted the previous copies first; `--into` has no such
teardown, so each run re-copied its own output (135 options became 270) and
pulled **other tenancies'** modifier groups into the target. Now scoped to the
source tenancy — which the B1 backfill made possible.

**A9 · Products were copied without their categories.** ✅ *Fixed 2026-08-23.*
Only the legacy `products.category_id` was copied, never the `product_categories`
pivot, so seeded products had a primary category but no tags — and anything
reading `Product::categories()` (the current path) saw an empty catalog.

### B. Platform issues this surfaced

**B1 · Two tenant-association models coexist, and the intended sharing rule is
not implemented.** ⚠️ *(Corrected 2026-08-23 — an earlier version of this note
misdiagnosed the cause as unpopulated `tenancy_id`; that is not the problem.)*

The catalog entities disagree about how a row is bound to a tenant:

| entity | `tenant_id` | `tenancy_id` | pivot rows | model |
|---|---|---|---|---|
| `products` | NULL ×96 | set ×96 | **96** | tenancy-owned + explicit pivot |
| `categories` | **set ×19** | 3 | **0** | legacy single-tenant |
| `modifier_groups` | **set ×32** | 0 | **0** | legacy single-tenant |

Both shapes *read* correctly, because `Domain\App\Http\Traits\ECommerce\
ResourceVisibility`'s tenancy branch ORs three clauses (`tenancy_id`,
`whereHas('tenant')`, `whereHas('tenants')`) — which is why nobody noticed. A
TenancyAdmin sees everything; there are no orphaned rows.

The breakage is at the **tenant** level. All 96 products are shared with both
tenants; all 96 of their categories belong to PinoyWok alone:

```
PinoyWok          → 96 products visible, 96 categories visible
PinoyWok - Bilbao → 96 products visible,  0 categories visible
```

Shared products land in categories the receiving tenant cannot see.

**The underlying cause is a missing clause.** The intended rule — *a resource not
specifically associated with a tenant is visible to every tenant in the tenancy*
— is documented as the standard resource policy but is absent from the trait's
tenant branch, which is only:

```php
$q->where('tenant_id', $user->tenant_id);
$q->orWhereHas('tenants', fn($sub) => $sub->where('tenants.id', $user->tenant_id));
```

So a row with `tenancy_id` set, `tenant_id` NULL and no pivot rows is invisible
to *every* tenant user — the inverse of the intent. It has never surfaced because
all 96 products are explicitly pivoted, so the fallback is never exercised. Create
a product without selecting tenants and it disappears for tenant users, while the
TenancyAdmin still sees it.

**Fix — two independent pieces, and order matters.**

1. Add the fallback to the trait's tenant branch:
   ```php
   $q->orWhere(fn($sub) => $sub
       ->where('tenancy_id', $user->tenancy_id)
       ->whereDoesntHave('tenants'));
   ```
   Blast radius on current data is 3 categories. Index the pivot FKs — this is a
   correlated `NOT EXISTS` per row.
2. Migrate `categories` and `modifier_groups` onto the products model: backfill
   `tenancy_id` from `tenants.tenancy_id`, leave the pivot empty, keep `tenant_id`
   as the narrowing override for genuinely tenant-private rows.

Piece 2 alone would make categories invisible to tenant users, so piece 1 must
land first or together.

**B2 · Mixed key strategies inside one feature.** `modifier_groups.id` is a
`uuid`; `modifier_options.id` is a `bigint`. Same feature, added at different
times. Any code assuming one shape breaks on the other.

**B3 · ~90 FK dependents on `tenants`, almost none cascading.** Deleting a
tenant means clearing ~90 tables in dependency order by hand — which is why
there is a whole `DELETE_TENANCY_ACCOUNT` document. Adding
`onDelete('cascade')` where a child is genuinely owned would remove an entire
class of operational risk.

**B4 · Soft deletes + unique slugs are a trap.** `Tenancy` soft-deletes but
`slug` is uniquely indexed, so a deleted tenancy holds its slug **forever** and
blocks recreation with an opaque constraint violation. Either the index should
be partial (`WHERE deleted_at IS NULL`) or the slug should be released on
delete.

**B5 · `payments.marketplace_status` does not exist** despite being documented
in `F1-Orders-Tabs_Order-README.md`. Corrected in that doc.

**B6 · `products.category_id` is NOT NULL with no tenancy consistency.** Nothing
prevents a product pointing at a category bound to a different tenant — which is
exactly the state the existing data is in (see B1). The seeder had to work around
it: copying categories by `tenancy_id` yielded almost nothing and left
`category_id` NULL, so it copies the categories the products actually reference.

### C. Security

**C1 · Weak-password admin.** ✅ *Guarded.* The command creates a TenancyAdmin
whose password is literally `password`. It now refuses to run in `production`
outright, and requires `--force` outside `local`. Without that guard, a
misconfigured console or a scheduled task would have created a live admin
account with a trivial password.

**C2 · The teardown deletes across ~90 tables.** Scoped by slug and never
touching another tenancy — but it is a destructive operation reachable from a
CLI, which is the second reason for the production guard.

**C3 · Demo data is indistinguishable from real data at the table level.**
✅ *Resolved 2026-08-23.* `is_sample` now marks `tenants` and every
tenancy-scoped catalog table, so demo rows can be excluded explicitly rather
than inferred from a slug. This was a prerequisite for the import button, not a
nicety: sample data can now land in a tenancy that holds real trading data, and
without the marker "remove the sample data" has nothing exact to match on.

⚠️ **The reports do not filter on it yet.** A TenancyAdmin who imports sample
restaurants will see them in tenancy-wide reports, because those aggregate over
every tenant in the tenancy. That is arguably what you want after deliberately
importing demo restaurants — but if it is not, the reports need an explicit
`is_sample = false` predicate.

### D. Performance

**D1 · 21 seconds for ~73,000 rows** — bulk inserts in 1,000-row chunks. Fine.

**D2 · Snapshots dominate the cost at scale.** Each runs the full widget set
(~12 queries). `--snapshots=all` would be ~17,500 queries. The default of 90
recent periods per tenant is the reason the full run stays in seconds.

**D3 · The whole run is not transactional.** An interruption leaves a partial
tenancy. Re-running cleans it up, so this is an annoyance rather than a hazard —
but wrapping each tenant in a transaction would make it atomic.
