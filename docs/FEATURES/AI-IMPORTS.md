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
New `components/ProductImport/MenuExtractionReview.tsx`, registered as a new
`tab: "resource.import.instances.tabs.extraction"` entry in
`schemas/productImport.ts`, placed **before** the preview tab.

- "Extract with AI" button, gated on status; live progress from the websocket
  context.
- One card per product showing the **cropped product photo** extracted from the
  page, alongside name, category, description, base price.
- **Fully editable**, not just the scalar product fields:
  - product: name, category, description, base price, delete
  - modifier group: name, type (SINGLE/MULTIPLE), required, min/max selections,
    add group, delete group
  - option: name, price adjustment, is_default, reorder, add option, delete option
  - all persisted with `PUT .../extraction`
- Surface `extraction_meta.warnings` prominently (the heuristics that caught the
  phantom-product and identical-option-price cases) and token usage / cost.
- **Download the generated .xlsx** at any point, so the operator can finish the
  edit in Excel/Sheets when that is faster than the inline editor. Generated on
  demand from the current `extraction_data`, so it reflects unsaved-to-file edits.
- "Confirm & generate import file" → `POST .../extraction/confirm`.

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
