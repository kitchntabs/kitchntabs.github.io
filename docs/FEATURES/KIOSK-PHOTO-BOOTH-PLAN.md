# Kiosk Photo Booth — branded souvenir photo with QR download

## Context

Both kiosks (KitchnTabs `kitchntabs.py`, VaneXa `vanexa.py` — one shared
`kt-kiosk-agent` codebase) currently do exactly one thing with speech: open an AI
conversation on the wake word. This adds a second, **AI-independent** trigger: a
visitor says *"foto"*, the kiosk takes their picture, the backend frames it in the
tenant's branding, and a QR appears on screen so they can take the photo home.

This is the feature deferred in `vanexa-backend-domain/docs/LAB-PROJECT-SETTINGS.md`
§8.3 — *"Screenshot on face recognition — requested, deferred; needs a
privacy/retention decision first, since storing images of the public is a different
data class than these settings."* That decision is now made: **photos are ephemeral**
(short TTL, auto-purged, no gallery), which is what unblocks it.

### Decisions already taken

| | |
|---|---|
| Retention | Ephemeral. `expires_at` ~24h, purged by a scheduled job. No gallery, no consent flow beyond an on-screen notice. |
| AI transform | Processor interface defined; **v1 ships framing only**. The Bedrock "digital twin" is a stub for a later PR. |
| QR target | A **branded landing page**, not a raw image download. |
| Orientation | From the **kiosk screen format**. Templates: vertical 1080×1920, horizontal 1920×1080, square 1080×1080. |
| Triggers | A configurable `kiosk_photo_trigger_words` setting, same backend-driven pattern as the other `kiosk_*` keys. |
| Capture resolution | **Floor of 800×600.** If the venue's configured `CAP_PROP_FRAME_*` is already at or above it, use the live frame untouched. If it is below (TC191W/Pi at 320×240), temporarily raise the capture for the shot and restore afterwards. |
| Capture UX | 5-second countdown starting **the instant the trigger matches** → white flash → "procesando…" → QR overlay, auto-dismissing. |
| Sharing | Landing page carries share/social buttons, **switchable in backend config**. |
| Privacy notice | On-screen before capture, **translated server-side** and delivered to the kiosk. |
| Frame layout | Gradient background `--primary-color--dark` → `--primary-contrast--dark`, coloured border, **horizontal logo centred top**, photo centred, **squared logo bottom-left**, **character bottom-right**. |

---

## Architecture

The codebase's own rule (see `App\AiAgentCore`, `App\ReportCore`, `App\DeviceCore`):
**domain-agnostic mechanism → `dash-backend` core; product-shaped surface →
duplicated per domain.** Almost all of this is mechanism, so most of it lands in one
new core module and the per-domain work is small.

```
kiosk ("foto")  ──POST──►  core: PhotoBoothCore
                             ├─ resolve branding  ──► domain-bound contract
                             ├─ compose frame (Imagick)
                             └─ return { token, landing_url }
kiosk draws QR(landing_url)
phone scans     ──GET───►  core: landing page ──► download (private disk)
hourly                     core: purge job
```

---

## 1. Core module — `dash-backend/app/PhotoBoothCore/`

Follow `App\AiAgentCore`'s layout exactly (self-contained folder, own config, own
migrations, own routes, registered from its service provider).

```
app/PhotoBoothCore/
  Contracts/PhotoBrandingResolverContract.php   # domain-bound
  Contracts/PhotoProcessorContract.php          # pluggable transform
  ValueObjects/PhotoBrandingContext.php
  Models/KioskPhoto.php
  Services/PhotoFrameComposer.php               # the Imagick work
  Services/CharacterSpriteCropper.php
  Services/BrandingAssetCache.php               # download+cache logos locally
  Processors/PassthroughProcessor.php           # v1
  Processors/BedrockImageProcessor.php          # v2 stub
  Jobs/PurgeExpiredKioskPhotosJob.php
  Http/Controllers/KioskPhotoController.php
  Http/Requests/KioskPhotoUploadRequest.php
  config/photo_booth.php
  database/migrations/xxxx_create_kiosk_photos_table.php
  resources/views/landing.blade.php
routes/photo_booth.php                          # sibling of routes/device.php
```

### `kiosk_photos` table

| column | notes |
|---|---|
| `id` | uuid |
| `tenancy_id`, `tenant_id` | scoping |
| `agent_ref` | nullable — LabProject id (VX) / AgentConfiguration id (KT) |
| `token` | `Str::random(32)`, unique, **the route key** |
| `format` | `vertical` \| `horizontal` \| `square` |
| `source_path` | private disk |
| `framed_path` | private disk, nullable until composed |
| `processor` | `none` \| `bedrock` |
| `status` | `pending` \| `ready` \| `failed` |
| `expires_at` | indexed — the purge job's only input |

### Why a random token, not a signed URL

`ValidateSignature` exists in core and no route uses it; `URL::temporarySignedRoute`
would give expiry for free. Rejected for three reasons, in order of weight:

1. **QR density.** A signed URL carries `?expires=…&signature=<64 hex>`. That is a
   far denser QR to read off a glossy screen at 1–2 m, which is the actual physical
   situation. A 32-char token in the path keeps the code light.
2. Rotating `APP_KEY` would invalidate every outstanding photo link.
3. A token column can be revoked by nulling it; a signature cannot.

**Do NOT reuse `SelfServiceSession::generateNextHash()`** (`strtoupper(Str::random(5))`)
— that is a table code people read aloud, not a secret, and ~916M is brute-forceable.

### Storage — and why the "private disk" is NOT enough on its own

**Verified finding, and it changes the design.** The obvious answer is
`DashFileStorage::getPrivateStorageDisk()`. But:

```php
config/filesystems.php:15   'default'            => env('FILESYSTEM_DISK', 'local'),
config/filesystems.php:41   'media_private_disk' => env('MEDIA_PRIVATE_DISK', 'local'),
FileController.php:24       $disk = config('filesystems.default', 'local');
```

**Both default to `local` — the same disk.** `App\Http\Controllers\API\FileController`
serves `/api/storage/{path}` with `->where('path','.*')` and **no authentication at
all**, so in a default configuration a file on the "private" disk is served by path
just like a public one. The `dashadmin-images` skill's advice — *"keep private docs on
`media_private_disk` and stream them through a controller"* — only holds when the two
disks are actually configured differently, which they are not out of the box.

Three layers, all of them cheap:

1. **A dedicated disk rooted outside `storage/app`.** Add to `config/filesystems.php`:
   ```php
   'kiosk_photos' => ['driver' => 'local', 'root' => storage_path('kiosk-photos'), 'throw' => false],
   ```
   `local`'s root is `storage_path('app')`, so **no `/api/storage/{path}` can reach
   outside it** — this is real isolation, not a naming convention. In production point
   it at s3 with its own prefix.
2. **The token is the filename.** `{token}.jpg`, under
   `dashPath('kiosk_photo', $tenancyId, $tenantId)`. Even if a future config change
   collapsed the disks again, the path is as unguessable as the download URL itself.
3. **The controller is the only reader**, and it is the only place `expires_at` is
   enforced.

> Layer 1 is the one that matters. Note that without it, a raw-path fetch would bypass
> the expiry check — an expired-but-not-yet-purged photo would stay fetchable for up to
> one purge interval.

---

## 2. Frame composition — `PhotoFrameComposer`

Imagick, guarded with `class_exists(\Imagick::class)` exactly as
`LabDocumentController::generateThumbnail` does, and writing via
`Storage::disk($disk)->put($selfBuiltPath, $blob)` rather than `storeFile()` (whose
`getStoragePath()` prepends an extra tenant segment on s3 and drifts from the DB column).

Layout, per the agreed design:

```
┌──────────────────────────────┐  gradient: primary-color--dark
│      [ horizontal logo ]     │            → primary-contrast--dark
│   ┌──────────────────────┐   │  border: primary-color--dark
│   │                      │   │
│   │     the photo        │   │  photo box: contain-fit, never upscale
│   │                      │   │  past 1.5× (320×240 sources exist)
│   └──────────────────────┘   │
│ [squared]        [character] │
└──────────────────────────────┘
```

- Gradient: `$im->newPseudoImage($w, $h, "gradient:{$from}-{$to}")`.
- Colours resolved `$tenant->settings['colors']['primary-color--dark']` →
  `…['primary-color']` → `DefaultBrandingService::colors()`. The same fallback chain
  the email Blades already use.
- Logos from `$tenant->getImageUrl('horizontal_logo', 'horizontal-medium')` /
  `('squared_logo','squared-medium')`, downloaded once and disk-cached by
  `BrandingAssetCache` (mirror `kt-kiosk-agent/pw/kitchntabs/theme.py`'s md5-keyed cache).
- **Never upscale a 320×240 source aggressively.** Contain-fit it and let the frame
  carry the composition; a hugely upscaled blur looks worse than a smaller inset.

### The character crop — `CharacterSpriteCropper`

The atlas is 2048×4096, a 4×8 grid of 512 px cells (`pw/character_kit/layout.py`, and
its TS twin `vx-character-preview/src/rig/layout.ts`). Cells are **full-canvas layers
composited at the same origin**, so a face is:

```
chest (index 0) → head (1) → eyes_open (4)
cellRect(i) = { x: (i % 4) * 512, y: floor(i / 4) * 512, 512, 512 }
```

Read the indices from the project's manifest rather than hard-coding them — both
domains already serve it at `lab/project/{id}/character-manifest` and
`ai/agent-config/{id}/character-manifest`, built from `settings.kiosk_character_rig`.
Fall back to the canonical sample manifest, and **omit the character entirely** if the
agent has no sprite rather than drawing the reference character on someone's souvenir.

---

## 3. The domain-bound seam

One contract, two thin implementations. This is the only genuinely product-shaped
part, and it mirrors how `RagProviderContract` / `AgentContextBuilderContract` are
rebound in each `AppDomainServiceProvider::register()`.

```php
interface PhotoBrandingResolverContract {
    public function resolve($tenant, ?string $agentRef): PhotoBrandingContext;
}
```

`PhotoBrandingContext`: colours, horizontal/squared logo URLs, character atlas path +
manifest, agent display name.

| domain | implementation | reads |
|---|---|---|
| vanexa | `Domain\App\Services\Lab\LabPhotoBrandingResolver` | `LabProject` by id → `character_sprite_path`, `settings.kiosk_character_rig` |
| kitchntabs | `Domain\App\Services\AI\AgentPhotoBrandingResolver` | tenant's active `AgentConfiguration` (one per tenant) |

---

## 4. Routes — `dash-backend/routes/photo_booth.php`

| method | path | auth | purpose |
|---|---|---|---|
| POST | `/api/kiosk/photo` | `auth:sanctum` **only** | upload + compose, returns `{token, landing_url, status}` |
| GET | `/photo/{token}` | public (web) | branded landing page |
| GET | `/api/kiosk/photo/{token}/file` | public | streams framed image from the private disk |
| GET | `/api/kiosk/photo/{token}/status` | public | for the landing page to poll while a processor runs |

**`auth:sanctum` WITHOUT `access`, authorizing in the controller.** `AccessMiddleware`
does an exact route-name match against a `Permission` row and 403s when absent — a
kiosk device account missing a seeded grant would fail silently in a venue. This is the
same reasoning already recorded on `lab/project/{id}/character-manifest`. **No permission
migration needed**, which is also what keeps this one core route file working for both
domains.

Public routes check `expires_at` and 410 when past it, matching the self-service
`410 Session expired` convention.

### v1 is synchronous; the queue arrives with the processor

Framing is ~200–500 ms of Imagick — cheap enough to do inline, and the QR is then
ready the instant the kiosk gets its response. The `agent` queue's supervisor is
`memory: 128–256 MB` / `timeout: 300`, and heavy Imagick already lives on
`products-import` (256–512 MB) for a reason. When `BedrockImageProcessor` lands
(10–30 s), *that* dispatches to a job and the landing page polls `status` — which is
exactly why `status` exists in the contract from day one.

---

## 5. Kiosk changes — `kt-kiosk-agent`

The key structural fact: **`TenantAssistant` (KitchnTabs) subclasses `VanexaAssistant`.
One edit to `pw/vanexa/assistant.py` serves both products.**

### New shared modules

| file | role |
|---|---|
| `pw/ui/qr_render.py` | **Promote** `_render_qr_surface(url, box_size)` out of `pw/ui/selfservice_qr.py` (already product-neutral) and re-import it there. `qrcode==7.4.2` is already in every requirements file and both PyInstaller specs. |
| `pw/ui/photo_overlay.py` | Countdown → flash → processing → QR. `show/clear/visible/update/draw(surface)` API, copying `pw/vanexa/rich_view.py`'s fade/linger model. Non-modal, auto-dismissing. |
| `pw/photo_booth.py` | Orchestration: countdown → grab frame → JPEG encode → upload → hand the URL to the overlay. Product-neutral. Owns the capture-resolution policy below. |
| `pw/photo_client.py` | HTTP client. Copy `DeviceAgent.session_log()`'s multipart shape (`files={"file": ("photo.jpg", blob, "image/jpeg")}`), `_url`/`_headers` + `api_log` conventions, bearer + `X-Tenant-Id`. |

### The capture sequence (owned by `pw/photo_booth.py`)

```
trigger matches
  └─► countdown starts IMMEDIATELY (5s) — spoken + on-screen numerals
        the trigger must never feel ignored, so nothing blocking happens first
  └─► at t-0: capture
        if configured capture >= 800x600  ->  use the live LatestFrame
        else                              ->  raise, settle, grab, restore
  └─► white flash frame + shutter sound
  └─► "procesando..."  (upload runs on a worker thread, never the render loop)
  └─► QR overlay for kiosk_photo_qr_seconds, then auto-dismiss
```

**The resolution floor.** `PHOTO_MIN_CAPTURE = (800, 600)`. Below it:

```python
cap.set(CAP_PROP_FRAME_WIDTH, w); cap.set(CAP_PROP_FRAME_HEIGHT, h)
for _ in range(3): cap.read()      # discard — auto-exposure/白balance settle
ret, shot = cap.read()
cap.set(CAP_PROP_FRAME_WIDTH, orig_w); cap.set(CAP_PROP_FRAME_HEIGHT, orig_h)
```

The 5-second countdown is what makes this safe: the re-negotiation hitch (~200–500 ms
on some UVC cameras, and a few stall outright) happens while the visitor is watching
numerals, not mid-conversation. **Wrap it in try/finally and always restore** — a
camera left at 800×600 would slow the main loop for the rest of the session on exactly
the hardware that cannot afford it. If the re-negotiation fails, fall back to the live
frame and take the small photo rather than failing the capture.

### Edits to existing shared files

- **`pw/wake_word.py`** — **probably no change at all.** `contains_wake_word(text,
  value, threshold)` already takes a comma-separated value, expands it via `aliases()`
  and matches phrases up to `MAX_NAME_WORDS`. Call it with `kiosk_photo_triggers` and
  it works. Add a thin named wrapper only if it reads better at the call site, and pin
  the new trigger cases in `testing/test_wake_word.py` either way.
- **`pw/camera.py`** — add a tiny thread-safe `LatestFrame` holder. The live frame is
  currently a module global `last_good_frame` inside each entry file and is
  **unreachable from `pw/`**; the assistant thread needs it. Both main loops publish
  into it once per iteration.
- **`pw/vanexa/assistant.py`** — one new branch in the `assistant_thread()` if/elif
  chain, **before** the wake-word check so a photo works outside a conversation. New
  constructor kwargs `PHOTO_TRIGGERS=[…]`, `ON_PHOTO=callable`, passed from
  `kitchntabs.py:1775` and `vanexa.py:1587` alongside the existing `WAKE=`/`CHARACTER_NAME=`.

### Edits to both entry files (the copy-paste twins)

`kitchntabs.py` and `vanexa.py` are verbatim twins for the render loop — every change
below goes in **both**:

- publish `last_good_frame` into `camera.LatestFrame`
- construct `photo_overlay` + `photo_booth`, pass `ON_PHOTO`
- `photo_overlay.update()` / `.draw(screen)` in the "drawn last" band — after
  `selfservice_qr.draw_url_bar` (guard with `globals().get(...)`, as
  `_bottom_bar_height` already does), before `login_overlay`
- read the new settings in `_apply_kiosk_overrides()`

Use the **clean** `frame` / `last_good_frame`, never `fr_cv` — that one has face
bounding boxes drawn on it.

### New `kiosk_*` settings — in the AGENT / PROJECT config

Declared identically in **both** `vanexa-backend-domain/config/lab_project_settings.php`
and `kitchntabs-backend-domain/config/kt_agent_kiosk_settings.php` — flat keys,
`kiosk_`-prefixed, `visible => true` so an operator can edit them on the agent's Kiosk
Configuration tab, and therefore also writable by the kiosk's own settings dialog
through `updateKioskSettings`.

```
kiosk_photo_enabled            boolean   default false
kiosk_photo_triggers           string    default "foto, photo, fotografia, una foto, sacame una foto"
kiosk_photo_countdown_seconds  integer   default 5
kiosk_photo_qr_seconds         integer   default 45
kiosk_photo_processor          select    none | bedrock   default none
kiosk_photo_min_capture_width  integer   default 800
kiosk_photo_min_capture_height integer   default 600
```

#### The trigger value is COMMA-SEPARATED, and that is not arbitrary

`pw/wake_word.py`'s `aliases(name)` **already** splits a configured value on commas,
and its docstring states the reason verbatim:

> *"COMMA-SEPARATED ON PURPOSE. The phonetic fold above only knows Spanish; it cannot
> help with a name from another language, and it cannot anticipate a mangling specific
> to one venue's microphone, model or accent. Since this value arrives from tenant/Lab
> settings (an operator editing a form, not a developer editing code), the operator
> needs a way to add whatever their own [venue produces]."*

So `kiosk_photo_triggers` is a **single comma-separated string**, exactly like the
existing `WAKE_WORD` and `CHARACTER_NAME` settings — **not** a newline textarea, which
would be a second, gratuitously different convention for the same job. Each entry may
be a **word or a phrase**, and entries exist precisely so an operator can add phonetic
variations their venue actually produces (`"foto, foco, photo, fot o"`).

Matching is then the existing machinery, unchanged: `normalize()` strips accents and
punctuation, `phonetic_fold()` applies the Spanish sound rules (h dropped, v→b,
z/x/ce/ci→s, qu/c→k, doubles collapsed), and `SequenceMatcher` scores at the existing
0.80 threshold. **A new setting, no new matching code.**

> **Limit to know:** `MAX_NAME_WORDS = 3` in `pw/wake_word.py` — the matcher slides a
> window of at most three words, so a four-word phrase can never match. Either keep
> entries to ≤3 words or raise that constant deliberately (it is shared with the wake
> word and character name, so raising it costs a little CPU on every recognised line).

Also add `kiosk_photo_sharing` (boolean) if per-agent control of the landing page's
share buttons is wanted in addition to the deployment-wide `config/photo_booth.php`
switch — the agent-level flag should be able to turn sharing OFF where config has it on,
never the reverse.

---

## 6. Privacy notice — translated server-side

The ephemeral-retention decision only holds up if people are told. The notice must be
**translated on the backend**, not hardcoded in the kiosk.

Per `F19-Internationalization_BACKEND_TRANSLATIONS.md`, translation files must be
written to **both** locations or the wrong one silently wins:

```
dash-backend/lang/{en,es}/photo_booth.php
dash-backend/resources/lang/{en,es}/photo_booth.php   # legacy, checked FIRST
```

Keys: `privacy_notice`, `countdown_prompt`, `processing`, `scan_to_download`,
`photo_failed`, plus the landing page's own copy.

Delivery: `GET /api/kiosk/photo/strings` (auth:sanctum), returning the resolved strings
for the caller's locale. `App\Http\Middleware\SetLocaleFromHeader` already reads
`Accept-Language` (accepting only `en`/`es`) and is in the API stack — **the kiosk
client must start sending that header**, derived from the tenant's
`primary_language_code`, which it already receives in `tenantSettings`. Fetch once at
boot and cache; fall back to a bundled Spanish string if the call fails, so a kiosk
that cannot reach the backend still shows *some* notice rather than none.

The notice renders in the photo overlay during the countdown — the one moment the
visitor is definitely looking at the screen and can still walk away.

## 7. Landing page sharing — optional, config-gated

`config/photo_booth.php`:

```php
'sharing' => [
    'enabled'  => env('PHOTO_BOOTH_SHARING', true),
    'channels' => ['native', 'whatsapp', 'x', 'linkedin', 'facebook'],
],
```

- **`native`** = the Web Share API (`navigator.share`) with the image as a `File`.
  This is the one that matters on a phone, which is the only device that will ever
  open this page — it opens the OS share sheet and reaches every app the person
  actually uses. Feature-detect and hide the button when unsupported.
- The named channels are plain `https://` intent links, rendered only when listed.
  They share the **landing URL**, not the image bytes (none of them accept an upload
  by URL scheme).
- `enabled => false` renders Download alone.

A tenant running a private event will want this off; a summit will want it on — hence
config rather than a hardcoded row of icons.

## 8. Purge

`PurgeExpiredKioskPhotosJob` — deletes rows and both files where `expires_at < now()`.
Schedule hourly. TTL from `config('photo_booth.ttl_hours', 24)`. Deleting the file must
tolerate an already-missing object (log and continue) rather than throwing — the row is
the authority on what should exist.

---

## 9. Processor interface

```php
interface PhotoProcessorContract {
    public function process(string $sourcePath, PhotoBrandingContext $ctx): string;
    public function isAsync(): bool;
}
```

`PassthroughProcessor` returns `$sourcePath`, `isAsync() === false`. Composition then
runs inline and the photo is `ready` on upload.

`BedrockImageProcessor` (v2 stub) will be the **first `invokeModel` call in this
codebase** — everything else uses `converse`/`converseStream`. When implementing it:
copy `BedrockChatClient::client()`'s **conditional** credential handling (explicit keys
only when both env vars are set, otherwise let the ECS task role work). Do **not** copy
`ExtractMenuProductsJob`'s unconditional `['key'=>env(…), 'secret'=>env(…)]`, which
hard-fails on task-role-only environments. Note Nova Canvas / Titan Image availability
differs by region, and three different region defaults are already in play
(`us-east-2` for BedrockAgentRunner + lab_rag, `us-east-1` for kiosk_agent).

---

## Verification

**Backend, in the running container** (`docker exec vanexa_image_app …`):
1. `php artisan migrate --path=…create_kiosk_photos_table.php`
2. `php artisan route:list --name=photo` — confirm all four routes register.
   **`php artisan route:clear && php artisan config:clear` first** — `composer install`
   runs `route:cache`, so new routes are invisible with no error. This exact trap
   produced a 500 on `/api/auth/getauth` earlier in this project.
3. Tinker: build a `PhotoBrandingContext` for a real tenant and run
   `PhotoFrameComposer` against a fixture JPEG at **800×600** (the floor) and at
   1280×720, in all three orientations. Write them to `/tmp` and open them — check the
   gradient direction, logo placement, and the character crop.
3b. Confirm the strings endpoint honours locale:
   `curl -H 'Accept-Language: en' …/api/kiosk/photo/strings` vs `es`.
4. `curl` the upload endpoint with a bearer token and a fixture file; confirm
   `{token, landing_url, status:"ready"}`.
5. Open `landing_url` in a browser; confirm branding and that Download works.
6. **Confirm the framed file is NOT reachable via `/api/storage/{path}`.** Take the
   stored path and try it directly:
   `docker exec <app> curl -s -o /dev/null -w '%{http_code}\n' 'http://localhost/api/storage/<path>'`
   — must be 404. If it returns 200, the dedicated disk is not rooted outside
   `storage/app` and §1 layer 1 has not actually been done.
6b. Open the landing page on a phone; confirm the share sheet appears, and that
   `PHOTO_BOOTH_SHARING=false` removes the buttons entirely.
7. Set `expires_at` to the past, run the purge job, confirm row + files gone and the
   landing page 410s.

**Kiosk:**
8. `python3 testing/test_wake_word.py` — extend with photo-trigger cases: each
   comma-separated entry, a multi-word phrase, likely Vosk manglings, and a
   four-word phrase asserted to NOT match (documenting `MAX_NAME_WORDS`).
9. Run `vanexa.py` against dev with `kiosk_photo_enabled` on; say "foto"; watch
   countdown → flash → QR. Scan it with a phone on the same network.
10. Repeat with `kitchntabs.py` — the whole point of the `VanexaAssistant` subclass
    seam is that this should need no additional wiring.
11. Confirm graceful degradation: `kiosk_photo_enabled=false`, no camera, and backend
    unreachable must each leave the kiosk fully functional.

---

## Risks / open questions

1. **Shutter latency.** `assistant_thread` polls with `time.sleep(1)`, so the word →
   countdown path is ~1 s + STT. Starting the countdown on match (not after upload)
   hides it, but the 5 s must begin at the match or the trigger feels ignored.
2. **Camera re-negotiation is the riskiest new code.** Some UVC cameras stall or return
   garbage for several frames after a `.set()`; a few refuse entirely. `try/finally`
   restore, discard frames after the change, and fall back to the live frame on
   failure. This runs on exactly the cheap hardware most likely to misbehave — test on
   a real TC191W before shipping, not just on a Mac.
3. **`/api/storage` enumeration is a pre-existing hole**, and the "private" disk does
   not close it in the default config (see §1). The dedicated out-of-root disk is the
   mitigation; the wider hole is worth a separate look, but is out of scope here.
4. **`SelfServiceQROverlay` is currently KitchnTabs-only.** Promoting the renderer must
   not drag `pw/kitchntabs/selfservice.py` into `vanexa.py`'s import graph.
5. **A new domain migrations *subdirectory* is not seen until the container restarts.**
   Core migrations avoid this; if any domain-side migration is added, restart.
6. **The kiosk does not send `Accept-Language` today.** The translated-strings endpoint
   is useless until it does. Small change, easy to forget, and it fails *silently* into
   the fallback locale.
7. **Copy still has to be written** — the privacy notice in en + es is a product/legal
   sentence, not a technical one, and it gates a venue deploy.
8. **`navigator.share` with a `File` is not universally supported** (and requires a
   secure context). Feature-detect; never render a button that does nothing.
9. **`MAX_NAME_WORDS = 3`** caps trigger phrases at three words, and it is shared with
   the wake word and character name. A four-word trigger will silently never fire.
10. **Open:** the frame templates are described but not designed. Someone should mock
   the three orientations before the composer is written, or it will be tuned by
   recompiling.
