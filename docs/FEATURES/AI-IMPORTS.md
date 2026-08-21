# AI-Assisted Product Import (`ai_menu`)

## Context

Onboarding a restaurant today means retyping its entire menu into the catalog. We
already have a working Bedrock extraction pipeline that reads a menu PDF page by
page and emits an `.xlsx` byte-compatible with `NormalizedProductsImport` — but it
is artisan-only (`menu-poc02:import`), untracked, and hands off to the real import
by *printing an instruction for a human to copy*.

This plan wires that pipeline into the existing import UI as a third import
mechanism alongside `normalized` and `template`.

The load-bearing constraint comes from our own benchmark
(`/Users/farandal/KITCHNTABS/menu-model-benchmarks/`): **vision extraction is not
deterministic and not always right.** The same model returned 3 products on one run
and 4 on the next; Nova Pro invented a phantom product by concatenating a price-grid
header ("Laksa Tonkotsu Ramyun"). Wrong prices in a POS catalog are the most
damaging possible error. So the design treats extraction as a **separate, explicitly
confirmed stage** — never something that silently feeds an import.

Decisions taken with the user:

| Question | Decision |
|---|---|
| Where extraction lives | Its own `EXTRACTION_*` status track, before preview |
| Review UI | Inline **edit + delete**, so bad rows are fixed in-app |
| Model selection | Fixed server-side via `BEDROCK_MENU_MODEL`; no UI |
| Scope | Menu-specific — `import_type = 'ai_menu'` |

## Target flow

```
CREATE     upload PDF (1 file) or images (N files)   → status NOT_INITIATED
EXTRACT    Bedrock, page by page                     → EXTRACTION_INITIATED → COMPLETED
REVIEW     edit / delete products, then Confirm      → sets extraction_confirmed_at,
                                                        regenerates the .xlsx
PREVIEW    existing normalized dry-run over that xlsx → PREVIEW_*
IMPORT     existing ImportNormalizedProductsJob       → IMPORT_*
```

Re-previewing is free (re-reads the xlsx). Re-extracting is an explicit, billed
action. **Preview and Import are disabled for `ai_menu` until
`extraction_confirmed_at` is set** — this is the "must be disabled if there is no AI
output confirmed" requirement.

## Branches

`feat/ai-import` already exists in `kitchntabs-backend-domain` (holds the untracked
POC files). Create it in `kitchntabs-frontend` off `development`. No `dash-backend`
change is anticipated — we reuse `AppNotificationBuilder` as-is; only branch there if
that proves wrong.

---

## Backend — `kitchntabs-backend-domain`

### 1. Migration
`database/migrations/ecommerce/*_add_ai_extraction_to_product_import_instances.php`

Add to `product_import_instances`:
- `extraction_data` `jsonb` nullable — the editable product array
- `extraction_meta` `jsonb` nullable — model, token usage, cost, warnings, page count
- `extraction_confirmed_at` `timestamp` nullable — the import gate

### 2. Model — `app/Models/ECommerce/ProductImportInstance.php`
Add `STATUS_EXTRACTION_INITIATED|COMPLETED|FAILED`, add the three columns to
`$fillable`, cast the two json columns to `array`, and add helpers mirroring the
existing `usesNormalized()`:

```php
public function usesAiMenu(): bool { return $this->import_type === 'ai_menu'; }
public function isExtractionConfirmed(): bool { return !is_null($this->extraction_confirmed_at); }
```

### 3. Mechanism registration
- `app/Services/ECommerce/Imports/ImportMechanismRegistry.php` → register
  `'ai_menu' => AiMenuImportMechanism::class`.
- New `app/Services/ECommerce/Imports/AiMenuImportMechanism.php` implementing
  `Contracts/ImportMechanism`. Its `getImportOptionsFormats()` returns the
  normalized options **plus** `pricelist`, `brand_name`, `sku_prefix`, `max_pages`.
  Model choice is deliberately absent (env-controlled).

Because `getImportOptionsFormats()` already drives the options form dynamically
(`importOptionsSelector.tsx` fetches per `import_type`), the options UI needs no
frontend work.

### 4. Extraction job
Rename/move `app/Jobs/Menu/ImportMenuMultimodalJob.php` →
`app/Jobs/Imports/ExtractMenuProductsJob.php`, changing its contract to match the
platform rather than the POC:

- Constructor `($productImportInstanceId, $tenantId, $options, $user)` — drop the
  `$tenancyAccountId` POC parameter; derive S3 namespacing from tenancy/tenant via
  `DashFileStorage::dashPath()`.
- Read sources from **`s3-private`** (`options.source_files[]`), not the `local`
  disk. PDF → Imagick page loop as today; images → each file is one page.
- Persist `extraction_data` / `extraction_meta` onto the instance instead of writing
  an xlsx. **The xlsx is generated at confirm time, from the edited data.**
- Drive statuses `EXTRACTION_INITIATED → EXTRACTION_COMPLETED|FAILED`.
- Broadcast `extraction.started|progress|completed|failed` through
  `AppNotificationBuilder`, reusing the shape
  `ImportNormalizedProductsJob::sendNotification()` uses — including
  `truncateNotificationData()`, since Pusher caps payloads at 10 KB and a menu's
  warnings array can be long.
- `uniqueId()` → `"extract_menu_{$productImportInstanceId}"` (per instance, like the
  template job — *not* per tenant like the normalized job, so two menus can extract
  concurrently).

Keep verbatim, they encode real bugs already fixed: the standalone-`Imagick`-frame
cropping (cloning the multi-page handle resets the iterator), the
`absolute_price → price_adjustment` arithmetic in PHP, deterministic
`generateSku()`, and writing `modifier_option_price` as a **string** (numeric `0`
reads back from xlsx as `NULL`, which would make the import's
`?? $option->price_adjustment` fallback preserve a stale surcharge).

### 5. Rows/xlsx generation → extract to a service
Move `buildNormalizedRows()` / `importHeadings()` / `writeImportFile()` out of the
job into `app/Services/ECommerce/Imports/MenuExtractionNormalizer.php`, so both the
job and the confirm endpoint use one implementation. Keeps using
`app/Helpers/Exports/MenuNormalizedRowsExport.php` unchanged.

Write the xlsx to **`s3-private`** under `dashPath('product_import', $tenancyId,
$tenantId)` and set it as the instance's `filepath`, so the untouched
`ImportNormalizedProductsJob` picks it up through its normal `source_disk` probe.

> Drift risk to close here: the POC's `importHeadings()` omits `terms` and the
> `stock_*` / `campaign_*` columns that `NormalizedProductsExport::headings()`
> emits. Derive the heading list from one shared constant so the two cannot diverge.

### 6. Controller + routes
`app/Http/Controllers/API/ECommerce/ProductController.php` — `import()` currently
branches `if ($importType === 'normalized')`. Add an `ai_menu` arm that **refuses to
dispatch unless `extraction_confirmed_at` is set**, then falls through to the
existing normalized dispatch (the file is a normal xlsx by that point).

`ProductImportInstanceController.php` — four new actions:

| Verb | URI | Purpose |
|---|---|---|
| POST | `/ecommerce/product/extract` | dispatch `ExtractMenuProductsJob`; same idempotency + re-entrancy guards `import()` uses |
| GET | `/ecommerce/product_import_instances/{id}/extraction` | return `extraction_data` + `extraction_meta` |
| PUT | `/ecommerce/product_import_instances/{id}/extraction` | persist edited `extraction_data`; clears `extraction_confirmed_at` |
| POST | `/ecommerce/product_import_instances/{id}/extraction/confirm` | regenerate xlsx from current data, set `extraction_confirmed_at` |
| GET | `/ecommerce/product_import_instances/{id}/extraction/download` | stream the xlsx built from the current `extraction_data`, for editing outside the app |

Register in `routes/api/ecommerce.php` inside the existing
`prefix('ecommerce')` group (~line 292, beside the other
`product_import_instances` custom routes).

### 7. Upload handling
`app/Http/Request/ECommerce/ProductImportInstanceRequest.php` — today
`'products_file' => 'nullable|file|mimes:xlsx,xls,csv'`. Make it conditional on
`import_type`:
- `ai_menu` + `upload_kind=pdf` → `products_file` `mimes:pdf`
- `ai_menu` + `upload_kind=images` → `source_files` array, `source_files.*`
  `mimes:jpg,jpeg,png,webp`
- otherwise unchanged

`_create()` stores every file via the existing three-tier disk fallback and records
the resulting paths in `options.source_files[]` and `options.upload_kind`.

---

## Frontend — `kitchntabs-frontend/packages/kt-ecommerce`

All paths under `src/`. The options form needs no work (it is already schema-driven
off the backend).

### 8. Mode selector
`components/ProductImport/ImportTypeSelector.tsx` — add a third card, `'ai_menu'`,
next to the existing normalized/template cards. It already clears
`product_template_id` on non-template selection; extend that guard.

### 9. Source upload
New `components/ProductImport/MenuSourceUpload.tsx`: a PDF/images toggle bound to
`upload_kind`, then a dropzone. Use `FileUploader` from `react-drag-drop-files`
following `components/Product/GallerySelector.tsx` — that is the established
multi-file pattern in this codebase (thumbnail grid, per-file remove, 10 MB guard),
and it handles the N-image case that react-admin's single `FileInput` does not.

`components/ProductImport/ExcelUploadAndPreview.tsx` and
`TemplateSelectorRAA.tsx` both `useWatch({name:'import_type'})` already — add
`ai_menu` to their hidden branches.

> Pre-existing bug worth fixing while here: `ExcelUploadAndPreview`'s MIME check
> only gates the *preview*. React-admin applies its internal `onDrop` after
> `...options` in `useDropzone`, so returning `false` does not stop the file
> becoming the form value — a rejected file still uploads on save. Pass `accept` as
> a top-level `FileInput` prop.

### 10. Extraction review tab
`components/ProductImport/MenuExtractionReview.tsx`, registered as a
`tab: "resource.import.instances.tabs.extraction"` entry in
`schemas/productImport.ts`, placed **before** the preview tab. Page chrome
(Extract/Save/Confirm/Download buttons, progress bar, token-usage card, the
page-level warnings summary as a collapsed-by-default accordion) lives here;
the product/group/option grid itself is a separate component.

- "Extract with AI" button, gated on status; live progress from the websocket
  context.
- Surface `extraction_meta.warnings` prominently (the heuristics that caught the
  phantom-product and identical-option-price cases) and token usage / cost.
- **Download the generated .xlsx** at any point, so the operator can finish the
  edit in Excel/Sheets when that is faster than the inline editor. Generated on
  demand from the current `extraction_data`, so it reflects unsaved-to-file edits.
- "Confirm & generate import file" → `POST .../extraction/confirm`.

**`components/ProductImport/MenuExtractionTable.tsx`** — the editable grid,
built on [material-react-table](https://www.material-react-table.com) v3
(`material-react-table` dependency in `kt-ecommerce/package.json`; peers
`@mui/material`/`@mui/icons-material` v6+, `@mui/x-date-pickers` v7.15+,
`@emotion/*` v11.13+ — all already satisfied by this monorepo's pinned MUI v7 /
React 19 versions via the `pnpm-workspace.yaml` `overrides` block). Replaced an
earlier nested-accordion layout (product accordion → modifier-group cards →
option rows) that the user found too heavy to scan.

Product → modifier group → option is rendered as one **tree table**
(`enableExpanding`, `getSubRows`), not three separate grids — MRT's tree
feature handles the indentation and expand/collapse natively. The three row
kinds are heterogeneous (a product has SKU/category/price, a group has
type/min/max, an option has price-adjustment/is_default), so internally
everything is flattened into one `IMenuTableRow` shape tagged with
`kind: 'product' | 'group' | 'option'`, and each column decides per-row
whether it applies via `enableEditing: (row) => ...` — irrelevant cells render
blank rather than as a disabled input, e.g. `category` only edits on product
rows, `isDefault` only on option rows.

Editing uses `editDisplayMode: 'table'` — every editable cell is a live input
all the time (spreadsheet-style), not click-to-edit-a-row. Each column defines
a fully custom `Edit` renderer directly controlled by the page's `products`
state (not MRT's own edit-value cache or its `onEditingRowSave`/create-row
machinery), because this page already has its own save/confirm semantics at
the `products`-array level — the per-row optimistic-update pattern from MRT's
CRUD examples is built for a typical per-row REST API and doesn't fit here.

No "add product": extraction is the only source of products by design — an
operator corrects what the model found, they don't hand-author new dishes in
this grid. Modifier groups and options **are** addable via row-action icons
(mirroring "add subordinate" from MRT's tree-editing example), alongside
delete (all three kinds) and a warnings-dialog trigger (product rows with
warnings only) using the same `useDialog()` pattern as the page-level summary.

### Reference: the canonical template shape

The generated file must match `KitchnTabs - Plantilla Importación Productos`:

- `price_<pricelist>` is slugged with underscores — e.g. `price_local_portugal`.
- `categories` accepts a comma-separated list (`Arroz y Gohan, Ofertas`); the AI
  import writes the single extracted category to both `categories` and
  `primary_category`.
- A product with several modifier groups repeats across rows. The template repeats
  the SKU on the second group's row; `NormalizedProductsImport::groupRowsByProduct`
  attaches a blank-SKU row to the **last seen SKU**, so blanking it (what the
  generator does) and repeating it are equivalent. Option rows always blank the
  product columns.
- `modifier_group_is_required` / `modifier_option_is_default` are `Yes`/`No`
  strings, not booleans. `modifier_option_display_order` is 1-based.
- A negative `modifier_option_price` is legal (`Noru -500` in the sample) — the
  editor must not clamp adjustments to >= 0.

### 11. Gating + context
`components/ProductImport/ProductImportComponent.tsx` — `startProcess()` sends
`import_type: record.import_type || 'normalized'`; that already forwards `ai_menu`
correctly. Extend the two button-visibility conditions (~L702-740) so that for
`ai_menu` both Preview and Import are disabled unless
`record.extraction_confirmed_at`.

`components/ProductImport/ProductImportContext.tsx` — add `extraction.*` to the
event switch (~L229-324). It reuses the existing `import.*` payload shape, so the
existing progress/stats components render unchanged.

> Note: this component keeps a duplicate copy of progress state
> (`localProgress`/`localStats` merged with context via `localImportActive ? … : …`)
> and re-processes `lastImportEvent` in its own effect. Extend that existing
> pattern rather than refactoring it — a refactor here is a separate change.

### 12. Types and i18n
- `ProductImportContext.tsx` — add `export type TImportType = 'normalized' |
  'template' | 'ai_menu'` and replace the ~8 inline string literals; add
  `IExtractedProduct`, `IExtractedModifierGroup`, `IExtractionMeta`.
- i18n keys under `resource.import.instances.*` must be added to **six** files —
  `en.tsx` + `es.tsx` in each of `apps/kitchntabs-{web,app,system}/src/i18n/`.
  There is no shared i18n for these.
- While adding statuses: the existing block defines `PREVIEW_STARTED`/`IMPORT_STARTED`
  but the backend emits `PREVIEW_INITIATED`/`IMPORT_INITIATED`, so those two states
  currently render a raw key. Fix alongside the new `EXTRACTION_*` labels.

Do **not** use `evalActionPermission` for the new gating — it is deprecated.

---

## Verification

1. **Extraction, against known ground truth.** `pw.pdf` page 6 is transcribed in
   `menu-model-benchmarks/README.md`: Laksa 8990 and Tonkotsu/Ramyun 8490, each one
   product with a `Proteína` SINGLE group (+0/+0/+500/+1500-2000/+2000-3000), plus
   Neoguri Ramyun. Upload it through the UI, extract, and diff the review tab
   against that table. Expect occasional misses — that is what the review UI is for.
2. **Round-trip integrity.** After Confirm, download the generated xlsx and re-read
   it with `WithHeadingRow`; assert every heading is present and that a `0` price
   adjustment survives as `"0"`, not `NULL`.
3. **The gate.** With `extraction_confirmed_at` null, assert `POST
   /ecommerce/product/import` is refused for an `ai_menu` instance and both buttons
   are disabled. Edit a product → assert the timestamp clears and the gate closes
   again.
4. **End to end.** Confirm → Preview → check `products_to_create` matches the
   reviewed count → Import → verify products, modifier groups, option prices and
   galleries in the DB.
5. **Images path.** Repeat with 2-3 JPEGs instead of a PDF; assert each image is
   treated as one page.
6. **Regression.** Run an existing `normalized` and a `template` import unchanged —
   the shared controller, context and component must not have shifted behaviour.

Local env: `pnpm dash:start kitchntabs.tunnel --tunnel` from `dash-backend-docker`.
Queue is `products-import`; extraction is long-running, so watch Horizon.

---

# Implementation Reference (as built)

Everything above this line was the plan going in. This section documents what
the code actually does, on branch `feat/ai-import` in both
`kitchntabs-backend-domain` and `kitchntabs-frontend`, including the fixes
made after the first working version shipped. Written in present tense as a
reference — for the *why* behind a specific decision, `git log -p` on the file
is more precise than this doc; this is for finding your way around the system
without reading the whole history first.

## Data model

`product_import_instances` gained three columns
(`2026_07_28_120000_add_ai_extraction_to_product_import_instances_table.php`):

| Column | Type | Purpose |
|---|---|---|
| `extraction_data` | `jsonb` nullable | The reviewable/editable product array — the operator's working copy, not raw model output once edited |
| `extraction_meta` | `jsonb` nullable | Model id, token usage, cost estimate, page count, validation warnings |
| `extraction_confirmed_at` | `timestamp` nullable | The import gate. Null blocks preview/import; cleared by any edit |

`ProductImportInstance` (`app/Models/ECommerce/ProductImportInstance.php`)
adds `STATUS_EXTRACTION_INITIATED|COMPLETED|FAILED` alongside the existing
preview/import statuses, casts both JSON columns to `array`, and exposes:

```php
public function usesAiMenu(): bool { return $this->import_type === 'ai_menu'; }
public function isExtractionConfirmed(): bool { return !is_null($this->extraction_confirmed_at); }
public function canRunImport(): bool { return !$this->usesAiMenu() || $this->isExtractionConfirmed(); }
```

## Backend components

**`AiMenuImportMechanism`** (`app/Services/ECommerce/Imports/`) — registered
in `ImportMechanismRegistry` as `'ai_menu'`. Its `getImportOptionsFormats()`
returns the standard normalized options plus four extraction-only ones
(`pricelist`, `brand_name`, `sku_prefix`, `max_pages`); deliberately no model
picker — the model is fixed server-side via `BEDROCK_MENU_MODEL`. Because this
drives the frontend's options form dynamically, the AI options UI needed zero
frontend work. `processImport()` just delegates to
`ImportNormalizedProductsJob` — by the time it's called the file is an
ordinary normalized xlsx.

**`MenuExtractionPrompt`** (`app/Services/ECommerce/Imports/`) — the Bedrock
system/user prompt as static methods, `system()` and `user()`. Extracted so
two callers share one prompt: `ExtractMenuProductsJob` (production) and
`ImportMenuMultimodalJob`/`MenuImportPoc02Command` (the benchmark harness in
`menu-model-benchmarks/`) — otherwise the harness measures a prompt that isn't
what production actually sends. The prompt's central rule: variants (protein,
size, flavor) are never separate products, they're one product with a
modifier group; a grid header naming several dishes side by side
(`"Laksa Tonkotsu Ramyun"`) must split into separate products, never
concatenate into one.

**`MenuExtractionNormalizer`** (`app/Services/ECommerce/Imports/`) — converts
`extraction_data` into normalized import rows and an xlsx. Shares its column
list with the human-facing export via three public constants on
`NormalizedProductsExport` (`PRODUCT_COLUMNS`, `MODIFIER_GROUP_COLUMNS`,
`MODIFIER_OPTION_COLUMNS`) — before this refactor the two producers had
independently-written column lists that had already drifted once (`terms` was
added to one and not the other). Runs twice in an instance's life: once after
extraction (to report a row count) and again on confirm (to produce the file
that's actually imported), so an operator's edits can never be bypassed —
confirm always regenerates from current `extraction_data`, never reuses a
stale file.

**`ExtractMenuProductsJob`** (`app/Jobs/Imports/`) — the production
extraction job, queued on `products-import`. Constructor:
`($productImportInstanceId, $tenantId, $options, $user)`.

- Reads source files from `s3-private` via `options.source_files[]`. A PDF is
  rasterized page-by-page with Imagick; an image upload is already one page
  per file. Capped at `options.max_pages` (default 30,
  `ExtractMenuProductsJob::DEFAULT_MAX_PAGES`) as a cost guard against an
  oversized upload.
- Calls Bedrock's Converse API per page (`temperature: 0`, though output is
  *not* deterministic — see Known limitations), crops each product's photo
  out of the page using the model's bounding box, and uploads the crop to
  `s3` for the review UI to display.
- Computes `price_adjustment` from `absolute_price` in PHP rather than trusting
  the model's arithmetic: base price = the cheapest `absolute_price` across a
  product's own option group, every option's adjustment = its price minus that
  base. The model is asked to copy printed prices verbatim, never to subtract.
- Writes `modifier_option_price` as a **string**, not a number: a numeric `0`
  round-trips through xlsx as `NULL`, which would make
  `NormalizedProductsImport`'s `?? $option->price_adjustment` fallback
  silently preserve a stale surcharge on re-import instead of zeroing it out.
- `generateSku()` is deterministic (hash of the product name), so re-running
  extraction on the same menu maps onto the same SKUs rather than creating
  duplicates.
- Drives `EXTRACTION_INITIATED → EXTRACTION_COMPLETED|FAILED` and broadcasts
  `extraction.started|progress|completed|failed` through
  `AppNotificationBuilder` / `NormalizedImportProgressNotification`, reusing
  the exact payload shape `ImportNormalizedProductsJob` already uses for
  `import.*` events (including `truncateNotificationData()`, since Pusher caps
  messages at 10 KB and a menu's warning list can be long) — the frontend's
  progress components need no special-casing to handle extraction progress.
- `uniqueId()` → `"extract_menu_{$productImportInstanceId}"`: locked per
  *instance*, not per tenant, so two different menus can extract concurrently
  (unlike the tenant-wide lock on the normalized import job).
- Exposes `getValidationWarnings()` / the static `validationWarningsFor()`:
  heuristics for the two vision-model failure modes actually observed in
  benchmarking — a product name containing another product's name (a grid
  header captured as one phantom product instead of being split), and a
  modifier group where every option shares the same price adjustment (the
  model read one grid column and applied it to every variant).
- Exposes `getTokenUsage()`: exact token counts from Bedrock's own response,
  plus a cost estimate *only* for models present in the hardcoded
  `MODEL_RATES_PER_MTOK` table (a handful of Nova variants) — an unlisted
  model reports tokens with `estimated_cost_usd: null` rather than a guessed
  figure.

Kept from the original POC (`ImportMenuMultimodalJob`,
`MenuImportPoc01Command`/`MenuImportPoc02Command` under `app/Jobs/Menu/` and
`app/Console/Commands/`) as a standalone benchmark harness — it's what drives
comparisons across Bedrock models in `menu-model-benchmarks/` without needing
any DB setup. Not wired into the app; artisan-only.

**Controller surface** — `ProductController::import()` gained an `ai_menu`
arm that returns `422` with `requires_extraction_confirmation: true` unless
`extraction_confirmed_at` is set; once confirmed, it's treated identically to
a `normalized` import (the confirmed file already *is* a normal xlsx).

`ProductImportInstanceController` gained:

| Method | Route | Behavior |
|---|---|---|
| `extract()` | `POST .../{id}/extract` | Dispatches `ExtractMenuProductsJob`; same idempotency (`already_completed`) / re-entrancy (`already_running`) guards as `import()`; `force: true` re-runs a completed extraction |
| `getExtraction()` | `GET .../{id}/extraction` | Returns `extraction_data` + `extraction_meta` + `extraction_confirmed_at` |
| `updateExtraction()` | `PUT .../{id}/extraction` | Validates the full nested product/group/option shape, recomputes warnings via `ExtractMenuProductsJob::validationWarningsFor()`, **always clears `extraction_confirmed_at`** — an edit can never ride on a stale confirmation |
| `confirmExtraction()` | `POST .../{id}/extraction/confirm` | Builds the xlsx from *current* `extraction_data` via `MenuExtractionNormalizer`, writes it to `s3-private`, sets it as `filepath`, sets `extraction_confirmed_at`, resets `status` to `NOT_INITIATED` so preview/import become reachable |
| `downloadExtraction()` | `GET .../{id}/extraction/download` | Streams an xlsx built **on demand** from current `extraction_data`, not from storage — reflects edits that haven't even been saved yet, for an operator who'd rather finish corrections in Excel |

Also added: `storeUploadedFile()` (the three-tier disk-fallback logic
extracted out of `_create()` so both the single `products_file` and the
`source_files[]` array use it) and `sanitizeOptions()` — strips the literal
strings `"undefined"` / `"null"` / `""` from incoming options before they
merge over the mechanism's defaults. `multipart/form-data` has no types: an
unset JS value serializes to the seven-character string `"undefined"`, and
since options are merged *over* the defaults, that string was winning —
`pricelist: "undefined"` would silently produce a `price_undefined` column
and a matching junk pricelist rather than an error. `false`, `0`, and `"0"`
are preserved (they're meaningful).

**Request validation** (`ProductImportInstanceRequest`) branches on
`import_type` + `upload_kind`: `ai_menu` + `pdf` requires `products_file`
(mimes:pdf, max 50 MB); `ai_menu` + `images` requires `source_files[]`
(mimes jpg/jpeg/png/webp, max 10 MB each).

Removed `app/Http/Controllers/API/Menu/` — unreferenced copies of the Todo
sample scaffold that still declared `namespace ...\Example\Todo`, discovered
to be dead weight while wiring this feature's routes.

## Frontend components

All under `packages/kt-ecommerce/src/components/ProductImport/`.

**`MenuSourceUpload.tsx`** — PDF/images toggle bound to `upload_kind`, then a
dropzone via `react-drag-drop-files` (the multi-file pattern already
established in `components/Product/GallerySelector.tsx`; react-admin's
`FileInput` only handles a single file). Images mode shows per-page
thumbnails numbered by upload order, since that order becomes page order for
extraction. Split into edit/view sub-components dispatched by `method`,
because `useWatch` — needed in edit mode to read `import_type` — throws when
called on show/list, which render outside a react-hook-form provider; the
mode check has to happen *inside* each variant, not in a shared wrapper above
the switch.

**`MenuExtractionReview.tsx`** — page chrome: Extract / Save / Confirm /
Download buttons, progress bar, token-usage card, and the page-level warnings
summary (a collapsed-by-default `Accordion`, not a permanent `Alert` — a menu
with many warnings shouldn't push the product grid below the fold). The
product/group/option grid itself is a separate component (below).

Data fetching uses `@tanstack/react-query`'s `useQuery`
(`queryKey: ['ecommerce', 'product_import_instances', id, 'extraction']`,
`staleTime: 30_000`) rather than a raw `axios.get` in a `useEffect` — the
original version fired four concurrent duplicate requests to the same
endpoint on a single page load, because nothing coalesced overlapping call
sites (initial mount, the websocket-driven reload, any parent re-render that
remounted the schema component). `saveExtraction()` / `confirmExtraction()`
write their results straight into the query cache via `setQueryData` instead
of triggering a redundant re-fetch; the websocket completion handler calls
`queryClient.invalidateQueries()` rather than fetching directly. The editable
`products` draft stays local `useState`, synced from the query result by an
effect keyed on the query's data reference — react-query's default structural
sharing keeps that reference stable when a background refetch returns
byte-identical data, so an in-progress edit isn't clobbered unless the server
data genuinely changed.

**`MenuExtractionTable.tsx`** — the editable grid, built on
[material-react-table](https://www.material-react-table.com) v3
(dependency in `kt-ecommerce/package.json`; peers `@mui/material` /
`@mui/icons-material` v6+, `@mui/x-date-pickers` v7.15+, `@emotion/*` v11.13+
— all satisfied by this monorepo's pinned MUI v7 / React 19 via
`pnpm-workspace.yaml`'s `overrides`). Replaced an initial nested-accordion
layout (product accordion → modifier-group cards → option rows) that was too
heavy to scan for a menu with dozens of dishes.

Product → modifier group → option renders as one **tree table**
(`enableExpanding` + `getSubRows`), not three separate grids. The three row
kinds are heterogeneous — a product has SKU/category/price, a group has
type/min/max, an option has a price adjustment and `is_default` — so
everything flattens into one `IMenuTableRow` shape tagged with
`kind: 'product' | 'group' | 'option'`, and each column's `enableEditing` is a
function of that kind: irrelevant cells render blank instead of a disabled
input (e.g. `category` only applies to product rows).

Editing uses `editDisplayMode: 'table'` — every editable cell is a live input
all the time, spreadsheet-style, rather than a click-to-edit step per row.
Each column's `Edit` renderer is fully custom and writes directly into the
page's `products` state; MRT's own edit-value cache and
`onCreatingRowSave`/`onEditingRowSave` machinery go unused, because this page
already has its own save/confirm semantics operating on the whole `products`
array at once — the per-row optimistic-update pattern from MRT's CRUD
examples is built for a typical per-row REST API and doesn't fit here. Row
actions: add modifier group (product rows), add option (group rows), delete
(any row), and a warnings-dialog trigger (product rows with warnings, via the
same `useDialog()` pattern — `dash-dialog`'s `variant` type is
`'default' | 'info' | 'success' | 'danger'`, no `'warning'`, so `'info'` is
used). No "add product": extraction is the only source of products by design
— an operator corrects what the model found rather than hand-authoring new
dishes in this grid.

Pagination is a single switch, `PAGINATION_CONFIG` at the top of the file
(`enabled`, `pageSize`, `rowsPerPageOptions`), rather than scattered magic
numbers — flip `enabled` to change the default for every caller; the
component also accepts `enablePagination`/`pageSize` props for a one-off
per-instance override. `paginateExpandedRows: false` keeps a page boundary
aligned to top-level products (without it, TanStack Table paginates the fully
*expanded* row list, so a product's own modifier groups could get split
across a page). `paginationDisplayMode: 'pages'` renders MUI's numbered
`<Pagination>` control rather than MRT's default `<TablePagination>`
(arrows + "x-y of z" text) — the default component's own controls weren't
rendering for reasons not fully root-caused, and `'pages'` mode uses a
different underlying MUI component entirely, sidestepping the problem.
`rowsPerPageOptions` must include the configured `pageSize`: MUI's rows-per-
page `<Select>` silently falls back to displaying its first option when the
real value isn't among the choices, which is why the control once showed "5"
regardless of the page size actually in effect.

The table renders at its natural full height and relies on page-level scroll
to reach rows below the fold, after an earlier attempt at a bounded,
internally-scrolling container (`muiTableContainerProps` with `maxHeight` +
`overflow: auto`) turned out not to work reliably: a nested scroll container
only scrolls if every ancestor between it and the viewport also permits
overflow, and this table sits inside a DASH tab panel whose layout isn't
controlled from here. Page-level scroll is what this layout already relies on
to reach the Preview/Import tabs, so it's known to work in this container
chain.

**`ProductImportComponent.tsx`** — the Preview/Import buttons are disabled
for an `ai_menu` instance until `extraction_confirmed_at` is set, with an
inline `Alert` explaining why. The server enforces the same rule
independently (see `ProductController::import()` above); this only avoids
offering an action that would be rejected.

**`ProductImportContext.tsx`** — the websocket event switch gained
`extraction.started|progress|completed|failed` cases, reusing the existing
`import.*` progress/stats state, so the existing progress bar and stats
components needed no changes to also handle extraction.

Fixed an actual infinite render loop discovered after shipping: the
provider's `processImportEvent` callback depended directly on
`notify`/`translate`/`refresh` from react-admin, none of which are guaranteed
a stable identity across renders. A churning identity re-ran the
events-processing effect on *every* render, not just when a genuinely new
websocket event arrived — and once `MenuExtractionReview` started calling
`refresh()` synchronously out of its own effect on `extraction.completed`,
that refetch cascaded back down through the provider and fed the loop.
Fixed by reading those three through a `latestActionsRef` so
`processImportEvent`'s own identity no longer depends on them, by memoizing
the provider's exposed `contextValue` so an unrelated re-render doesn't force
every consumer to re-render too, and by removing the `refresh()` call from
`MenuExtractionReview`'s completion effect entirely (redundant — the provider
already schedules one 1.5s after the same event).

**`types.ts`** (new) — `TImportType`, `TUploadKind`, `TModifierGroupType`,
`TImportStatus`, `IExtractedProduct`, `IExtractedModifierGroup`,
`IExtractedOption`, `IExtractionMeta`, `IExtractionResponse`, `ITokenUsage`.
Replaced roughly eight inline `'normalized' | 'template'` string literals
scattered across the import components.

**i18n** — `resource.import.instances.ai.*`, `types.ai_menu`,
`no_template.*`, and corrected `statuses.*` were added to all six files
(`en.tsx` + `es.tsx` in each of `apps/kitchntabs-{web,app,system}/src/i18n/`
— there's no shared i18n for these). While touching `statuses.*`: a
pre-existing bug meant the block defined `PREVIEW_STARTED`/`IMPORT_STARTED`
but the backend actually emits `PREVIEW_INITIATED`/`IMPORT_INITIATED`, so
those two states had always rendered a raw translation key in the status
chip; fixed alongside adding the new `EXTRACTION_*` labels.

**Dependencies** added to `kt-ecommerce/package.json`:
`material-react-table@^3.2.1`, `@tanstack/react-query@5.101.2` — the latter
pinned to the *exact* version (no `^`) already resolved everywhere else in the
workspace via `pnpm-workspace.yaml`'s `overrides`, so it can't accidentally
pull a second, incompatible copy into the dependency graph.

## Known limitations

- **Extraction is not deterministic**, even at `temperature: 0` — repeated
  runs over the identical page can return a different product count or
  different grid readings. This is the entire reason the review/confirm step
  exists rather than importing extraction output directly; see
  `menu-model-benchmarks/` for the model comparison that established this.
- The validator's substring heuristic (grid-header-as-phantom-product) has at
  least one known false positive: `'Neoguri Ramyun'` gets flagged for
  containing `'Ramyun'` even when they are genuinely different dishes.
- No automated test suite. Verification so far has been manual: a live
  extraction run against ground truth transcribed from a real menu page (see
  `menu-model-benchmarks/README.md`), an xlsx round-trip check (write via
  `MenuExtractionNormalizer`, read back with `WithHeadingRow`, confirm every
  heading survives and a `0` price adjustment doesn't become `NULL`), and a
  standalone Node script sanity-checking the tree table's immutable
  patch/delete/add logic in isolation from React.
- A `@emotion/react` "already loaded" console warning has been observed in
  dev with `LINK_DASH_CORE=true` — attributed to that flag aliasing the
  `dash-*` packages to sibling-repo source (which then resolves emotion from
  a different `node_modules` than the app does), not to anything added by
  this feature; neither new dependency (`material-react-table`,
  `@tanstack/react-query`) brings its own emotion instance.


Availbale bedrock modal image models 

meta Logo
Llama 4 Maverick 17B Instruct
By Meta

Fine Tuning, Text summarization, Code generation, Function calling, Advanced understanding, Assistants, Chatbots
Serverless Serverless
Cross-region inference

meta Logo
Llama 4 Scout 17B Instruct
By Meta

Fine Tuning, Text summarization, Code generation, Function calling, Advanced understanding, Assistants, Chatbots
Serverless Serverless
Cross-region inference

amazon Logo
Nova 2 Lite
By Amazon

Image, Video, Text to Text
Serverless Serverless
Cross-region inference

amazon Logo
Nova Premier
By Amazon

Legacy
Agents, Chat optimized, Code generation, Complex reasoning analysis, Conversation, Math, Multilingual support, Question answering, RAG, Text generation, Text summarization, Translation, Text, Image, Video-to-text
Serverless Serverless
Cross-region inference

amazon Logo
Nova Lite
By Amazon

Agents, Chat optimized, Conversation, Math, Multilingual support, Question answering, RAG, Text generation, Text summarization, Translation, Text, Image, Video-to-text
Serverless Serverless

amazon Logo
Nova Pro
By Amazon

Agents, Chat optimized, Code generation, Complex reasoning analysis, Conversation, Math, Multilingual support, Question answering, RAG, Text generation, Text summarization, Translation, Text, Image, Video-to-text
Serverless Serverless
Cross-region inference

google Logo
Gemma 3 12B IT
By Google

Text generation; Code generation; Reasoning; Question answering; Summarization; Multilingual support; Tool use
Serverless Serverless

google Logo
Gemma 3 27B PT
By Google

Base pretrained modeling; Multimodal understanding; Reasoning; Code understanding; Long-context representation learning
Serverless Serverless

google Logo
Gemma 3 4B IT
By Google

Text generation; Code generation; Reasoning; Question answering; Summarization; Multilingual support; Instruction following
Serverless Serverless

nvidia Logo
NVIDIA Nemotron Nano 12B v2 VL BF16
By NVIDIA

Image and document understanding; Visual QA; Multimodal reasoning; Text generation; Document intelligence
Serverless Serverless

qwen Logo
Qwen3 VL 235B A22B
By Qwen

Text generation; Image understanding; Document OCR and layout