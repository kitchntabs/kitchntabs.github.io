# Tenancy-wide AI Agent management in kitchntabs-web

## Context

KitchnTabs gives each tenant (restaurant) exactly one AI agent
(`ai_agent_core.max_agents_per_tenant = 1`, forced in
`kitchntabs-backend-domain/app/Providers/AppDomainServiceProvider.php:139`). Today the
only way to reach that agent is to open kitchntabs-web, use the `TenantSwitcher` to
switch **into** a restaurant, and configure it there — one restaurant at a time.

A TenancyAdmin managing many restaurants has no cross-tenant view. This adds one, in
kitchntabs-web at the **tenancy level**, mirroring how VaneXa registers `vx-lab` at both
levels (`apps/vanexa-web/src/resources/KitchnTabsWebPrivateResources.tsx`).

Per your clarification, the tenancy view differs from the existing per-tenant view in
exactly two ways:

1. it lists **every tenant's** agent in one list (with a Restaurant column), and
2. **create** carries a **tenant selector**, so an agent can be created for a chosen tenant.

Everything else — the same endpoint, the same form, the same tabs — is reused.

Three real defects were found while mapping this and are folded in (see §4).

---

## 1. Why no new controller or endpoint is needed

`KitchnTabsWebPrivateAppLoader.tsx:107-189` loads **exactly one manifest at a time** —
tenancy level loads `KitchnTabsWebPrivateResources`, tenant level loads
`KitchnTabsWebTenantPrivateResources`, never both ("load ONLY tenant-specific resources,
not merged with base").

So two resource configs can share `model: 'ai/agent-config'` without a react-admin name
collision: the singleton config registers at tenant level, the cross-tenant list registers
at tenancy level. Same routes (`routes/api/ai_agent.php`), same controller, same
permissions (already granted to `TenancyAdmin` by
`database/migrations/permissions/2026_08_09_170000_add_ai_agent_config_permissions.php`).

```
Tenancy level (no active_tenant_id, no X-Tenant-Id header)
  └── KitchnTabsWebPrivateResources
        └── agentConfigTenancyResource   → list of ALL agents + Restaurant column
        └── agentDocumentTenancyResource → list of ALL documents + Restaurant column

Tenant level (active_tenant_id set, X-Tenant-Id sent by useAxios interceptor)
  └── KitchnTabsWebTenantPrivateResources
        └── agentConfigResource     (existing singleton "Configure Agent")
        └── agentDocumentResource   (existing)
```

---

## 2. Backend — `kitchntabs-backend-domain`

### 2.1 Scoping: adopt the core visibility scope

`App\Traits\ResourceVisibility::scopeVisibleThroughTenant()`
(`dash-backend/app/Traits/ResourceVisibility.php:30`) **already implements exactly the
required three-way behaviour** and auto-detects the `tenancy_id` column via
`Schema::hasColumn`:

| Caller | Result |
|---|---|
| SystemAdmin | everything |
| TenancyAdmin + valid `X-Tenant-Id` | that one tenant (tenant-level view) |
| TenancyAdmin + invalid `X-Tenant-Id` | fails closed (`whereRaw('1=0')`) |
| TenancyAdmin, no header | all tenants in the tenancy (**the new tenancy view**) |
| Tenant / other | own tenant |

Both `ai_agent_configurations` and `kt_agent_documents` already have **`tenant_id` *and*
`tenancy_id`** with real FKs — **no migration needed**.

- `app/Models/AI/AgentConfiguration.php` and `app/Models/AI/AgentDocument.php` — add
  `use App\Traits\ResourceVisibility;`.
- `AgentConfigController::_preList()` — replace the hand-rolled `if isSystemAdmin / if
  TenancyAdmin → where('tenancy_id') / else where('tenant_id')` block with
  `$this->model->visibleThroughTenant($request->user())`, keeping the existing
  `->with('documents')` eager load and adding `->with('tenant:id,name')`.
  This is the "narrow to active tenant" fix you approved: today this list ignores
  `X-Tenant-Id`, so a TenancyAdmin switched into one restaurant still sees every agent.
- `AgentDocumentController::_preList()` and `getForSelect()` — same swap. These currently
  have **no TenancyAdmin branch at all**, so a tenancy-only admin (null `tenant_id`) sees
  zero documents.

### 2.2 The tenant selector on create

`AgentConfigRequest` deliberately rejects `tenant_id` today ("what stops a TenancyAdmin or
Tenant from creating — or re-pointing — a configuration at someone else's tenant"). Keep
that property while allowing the new selector:

- `app/Http/Request/AI/AgentConfigRequest.php` — add
  `'tenant_id' => ['nullable','uuid', Rule::exists('tenants','id')->where('tenancy_id', $this->user()?->tenancy_id)]`.
  Scoping the `exists` rule to the caller's own tenancy is what preserves the guarantee —
  a foreign tenant's uuid fails validation rather than being silently accepted.
- `AgentConfigController::_create()` — resolve the target tenant as
  *explicit validated `tenant_id`* → else existing `activeTenantId($user)`. Only honour the
  explicit value for a TenancyAdmin/SystemAdmin; a plain Tenant stays pinned to
  `$user->tenant_id`. Then `unset($validated['tenant_id'])` before the mass-assignment, the
  same way `character_*`/`document_ids` are already handled.
- Stamp `tenancy_id` from the **target tenant's** `tenancy_id`, not `$user->tenancy_id` —
  today a tenancy-only admin can write a `tenancy_id` inconsistent with `tenant_id`, and
  `AgentConfigPolicy::manage()` matches on `tenancy_id`, so an inconsistent row becomes
  unmanageable.
- Mirror the same target-tenant resolution in `AgentDocumentController::_create()`, which
  currently hardcodes `$user->tenant_id` and so uploads to the admin's *home* tenant even
  when switched.

The existing `updateOrCreate(['tenant_id' => $tenantId], ...)` keeps the one-agent-per-tenant
guarantee: picking a restaurant that already has an agent edits it rather than erroring
(the `unique(tenant_id, agent_key)` index and `guardTenantAgentLimit()` remain the backstop).

### 2.3 Expose the tenant name

`AgentConfigResource` / `AgentDocumentResource` return `tenant_id` but no readable name.
Add to both `toArray()`:

```php
'tenant' => $this->whenLoaded('tenant', fn () => [
    'id' => $this->tenant->id,
    'name' => $this->tenant->name,
]),
```

`whenLoaded` keeps list rows free of an N+1 when the relation wasn't eager-loaded.

### 2.4 Filter by tenant

`app/ModelFilters/AI/AgentConfigFilter.php` and `AgentDocumentFilter.php` have no
`tenantId` method, so a `filter={"tenant_id":…}` from the list toolbar is silently ignored.
Add `public function tenantId($id) { return $this->where('tenant_id', $id); }` to both.

---

## 3. Frontend — `kt-agent` + `kitchntabs-web`

`kt-agent` is a `workspace:*` package source-aliased in dev
(`apps/kitchntabs-web/vite.config.mts` `localPackageSrc.aliases`), so edits are live with no
publish step — unlike the `@dashadmin/*` packages.

### 3.1 Tenancy schemas — `packages/kt-agent/src/schemas/`

New `agentConfigTenancy.ts` and `agentDocumentTenancy.ts`, each spreading the existing
schema and prepending a tenant column. Reuse the established reference-column idiom from
`apps/kitchntabs-web/src/resources/private/schemas/service_account.tsx:31-43` — the
tenancy-scoped one, **not** the `system/tenant` variant used by `tenancyResources.tsx`:

```ts
import agentConfigSchema from './agentConfig';

const tenantColumn: IDashAutoAdminAttribute = {
    tab: 'resource.ai.agent_config.tab_general',
    label: 'resource.ai.agent_config.field_tenant',
    attribute: 'tenant_id',
    type: 'tenancy/tenants.name',   // → ReferenceField, see AttributeToField.tsx:341
    multiple: false,
    pagination: false,
    component: SelectInput,
    inList: true,
    inEdit: false,   // an agent cannot be re-pointed at another tenant after creation
};

export default [tenantColumn, ...agentConfigSchema];
```

`type: '<resource>.<field>'` + `multiple: false` is what `AttributeToField.tsx:341-348`
turns into a `ReferenceField` showing the name in the list and a populated `SelectInput` on
the form. The `tenancy/tenants` resource is registered at tenancy level by
`./private/tenancyResources`, so the reference resolves.

### 3.2 Tenancy resources — `packages/kt-agent/src/resources/`

New `agentConfigTenancyResource.tsx` and `agentDocumentTenancyResource.tsx`, built by
spreading the existing config (the same pattern `vx-lab/src/resources/labResources.tsx:28`
uses for `LabProjectResourceWithWindow`):

```tsx
const agentConfigTenancyResource: IDashAutoAdminResourceConfig = {
    ...agentConfigResource,
    roles: ['TenancyAdmin'],          // bare string; 'System' bypasses via checkRole
    label: 'resource.ai.agent_config.tenancy_label',
    schema: agentConfigTenancySchema,
    menu: [{ title: 'resource.ai.agent_config.tenancy_menu_list', redirect: '/ai/agent-config' }],
    mainAction: { title: 'resource.ai.agent_config.tenancy_main_action', redirect: '/ai/agent-config/create' },
};
```

Note the `mainAction` drops the singleton `mode:'create' / fn:'virtualhash'` idiom — at
tenancy level this is a real list, so create must open a normal create form carrying the
tenant selector. Keep `isFormData`, `formGroupMode: 'tabs'`, and the `contextComponent`
that feeds the Kiosk Configuration tab from `ai/agent-config/settings/formats`.

Export both from `packages/kt-agent/src/resources/index.ts`.

### 3.3 Registration

- `apps/kitchntabs-web/src/resources/KitchnTabsWebPrivateResources.tsx` — **add**
  `agentConfigTenancyResource` + `agentDocumentTenancyResource`.
- `apps/kitchntabs-app/src/resources/KitchnTabsWebPrivateResources.tsx` — **add** the two
  *existing* base resources (`agentConfigResource`, `agentDocumentResource`). The app already
  has the `kt-agent` dependency and the full `resource.ai.*` i18n block; the resources'
  `roles` already include `TENANT_ROLE`. This is the gap where a restaurant logging into its
  own app cannot see its agent at all.
- `apps/kitchntabs-web/src/resources/KitchnTabsWebTenantPrivateResources.tsx` — unchanged.

### 3.4 i18n

Add to the `resource.ai` block in **both** `en.tsx` and `es.tsx` for kitchntabs-web
(`apps/kitchntabs-web/src/i18n/en.tsx:363`, `es.tsx:354`):
`agent_config.tenancy_label` / `tenancy_menu_list` / `tenancy_main_action` / `field_tenant`,
and the `document.*` equivalents. (e.g. "AI Agents" / "Agentes IA", "Restaurant" / "Restaurante".)

---

## 4. Defects found during exploration (fold in)

1. **Empty `document_ids` 422.** `AgentConfigRequest`'s `'document_ids.*' => 'uuid'` plus
   `isFormData: true` reproduces the exact bug already fixed in `vanexa-backend-domain`:
   dash-admin's `processFormData()` serialises an **empty** array as one entry
   `document_ids[]=""`, which fails `uuid`. Saving an agent with no documents selected 422s.
   Fix identically — a `prepareForValidation()` stripping empty strings from `document_ids`.
2. **Cross-tenant read (IDOR).** Neither `AgentConfigController` nor `AgentDocumentController`
   defines `_preGetOne()`, so `ReactAdminBaseController::getOne()` runs `findOrFail($id)`
   against an **unscoped** query — any holder of the `getOne` permission can read any
   tenant's agent by uuid. Add `_preGetOne()` applying the same `visibleThroughTenant()`
   scope. (`_update`/`_delete` are already protected by `_authorize('manage', $item)`.)
3. **Tenancy consistency** — §2.2's `tenancy_id` stamping, above.

---

## 5. Verification

Backend (in the container, via `pnpm dash:start kitchntabs local`):

```bash
php artisan config:clear && php artisan route:clear   # composer install caches config/routes
php artisan test --filter=Agent                        # existing domain suite, expect no NEW failures
```

Then, as a TenancyAdmin token, confirm the header drives the scope:

```bash
# tenancy level — expect agents from EVERY tenant in the tenancy, each with tenant.name
curl -s "$API/api/ai/agent-config" -H "Authorization: Bearer $TOKEN" | jq '.data[] | {id, tenant}'

# tenant level — same token + header, expect ONLY that tenant's agent
curl -s "$API/api/ai/agent-config" -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: $TENANT_A" | jq '.data | length'

# forged header (tenant outside the tenancy) — expect 0 rows, not a full list
curl -s "$API/api/ai/agent-config" -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: $FOREIGN" | jq '.data | length'

# create for a chosen tenant
curl -s -X POST "$API/api/ai/agent-config" -H "Authorization: Bearer $TOKEN" \
  -F "name=Agent A" -F "tenant_id=$TENANT_A" | jq '{tenant_id, tenancy_id}'

# create for a tenant OUTSIDE the tenancy — expect 422, not a created row
curl -s -X POST "$API/api/ai/agent-config" -H "Authorization: Bearer $TOKEN" \
  -F "name=X" -F "tenant_id=$FOREIGN" | jq
```

Frontend — `pnpm dev:web:kitchntabs-web:development:linked`, log in as a TenancyAdmin:

1. At **Tenancy Account** level: the new "AI Agents" + "Agent Documents" entries appear;
   each list shows one row per restaurant with a readable Restaurant column.
2. Create → the Tenant selector lists only this tenancy's restaurants; save; the row appears
   against the chosen restaurant.
3. Save an agent with **no documents selected** → saves cleanly (defect 1).
4. `TenantSwitcher` into one restaurant → menu swaps to the tenant manifest, "AI Agent" now
   shows **only that restaurant's** agent (defect fixed in §2.1).
5. Switch back to Tenancy Account → full cross-tenant list returns.
6. Type-check: `npx tsc --noEmit -p apps/kitchntabs-web` and `-p packages/kt-agent`, comparing
   against the current baseline (both have pre-existing unrelated errors).

Also confirm in kitchntabs-app that a plain Tenant user now sees "AI Agent" and only ever
their own.


1. kt-agent package tree
Root: /Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent


package.json            npm manifest: exports map, typesVersions, deps
tsconfig.json           extends dash-tsconfig/react-library.json, rootDir src, path alias @kt-agent/*
tsup.config.ts          bundle:false ESM build, dist/ mirrors src/, jsx: 'automatic', dts: false
src/
  index.ts              barrel: re-exports ./resources, ./schemas, ./components
  resources/
    index.ts            exports agentConfigResource, agentDocumentResource
    agentConfigResource.tsx    singleton AI-agent config resource (model 'ai/agent-config')
    agentDocumentResource.tsx  agent knowledge-base document resource (model 'ai/document')
  schemas/
    index.ts            exports agentConfigSchema, PERSONA_VOICES, agentDocumentSchema
    agentConfig.ts      8 attributes across 6 tabs + PERSONA_VOICES constant
    agentDocument.ts    5 attributes on a single tab
  components/
    index.ts            exports CharacterFileUpload, DocumentIdsSelector, AgentKioskSettings
    CharacterFileUpload.tsx  image/file dropzone that also renders the already-saved *_url asset
    DocumentIdsSelector.tsx  paginated searchable checkbox picker writing document_ids
    AgentKioskSettings.tsx   backend-schema-driven "Kiosk Configuration" tab (settings JSON column)
There are 14 files total, no tests, no stories, no aggregated agentResources.tsx, and no chat/agentic window component in this package. (The AgenticWindow analog lives in the sibling package: /Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/vx-lab/src/components/AgenticWindow.tsx, aggregated by /Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/vx-lab/src/resources/labResources.tsx.)

2. Resource configs
/Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent/src/resources/agentConfigResource.tsx
Key fields:


roles: [DASHAppConstants.system.SYSTEM_ROLE, 'TenancyAdmin', DASHAppConstants.system.TENANT_ROLE],
component: ResourceTemplate,
model: 'ai/agent-config',
label: 'resource.ai.agent_config.label',
schema: agentConfigSchema,
icon: <SmartToyIcon />,
group: 'resource.groups.configuration',
menu: [{ title: 'resource.ai.agent_config.menu_list', redirect: '/ai/agent-config' }],
mainAction: { title: 'resource.ai.agent_config.main_action', mode: 'create', fn: 'virtualhash', redirect: '/create' },
view: true, create: true, edit: true,
drawer: false,
drawerOptions: { create: false, edit: true, view: true },
isFormData: true,
mutationMode: 'pessimistic',
saveButtonAlwaysEnabled: true,
formGroupMode: 'tabs',
listProps: { storeKey: false },
Plus the notable contextComponent that skips the extra fetch in list mode:


contextComponent: ({ resourceConfig, mode, children }) =>
    mode === 'list' ? children : (
        <SystemRequestsCache
            cacheKey="kt_agent_kiosk_settings_formats_cache"
            apiUrl="ai/agent-config/settings/formats"
            cacheSeconds={300}
        >{children}</SystemRequestsCache>
    ),
The header comment documents the singleton idiom: mainAction create + virtualhash because ai_agent_core.max_agents_per_tenant = 1 and the backend _create() upserts on tenant_id.

/Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent/src/resources/agentDocumentResource.tsx
Same roles array; differences from the config resource:


model: 'ai/document',
label: 'resource.ai.document.label',
icon: <DescriptionIcon />,
group: 'resource.groups.configuration',
menu: [{ title: 'resource.ai.document.menu_list', redirect: '/ai/document' }],
mainAction: { title: 'resource.ai.document.main_action', mode: 'create', fn: 'virtualhash', redirect: '/create' },
drawer: true,
drawerOptions: { create: true, edit: true, view: true },
isFormData: true,
mutationMode: 'pessimistic', saveButtonAlwaysEnabled: true, formGroupMode: 'tabs', listProps: { storeKey: false },
No contextComponent. Its comment notes the file is write-once (backend AgentDocumentRequest rejects swaps).

Other resource files
None. /Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent/src/resources/index.ts is only two named re-exports; there is no array-style agentResources.tsx like vx-lab's labResources.tsx.

3. Schemas
/Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent/src/schemas/agentConfig.ts
Exports PERSONA_VOICES = [{ id: 'female', name: 'Female' }, { id: 'male', name: 'Male' }] — a gender, not a TTS voice id. Default export is as IDashAutoAdminAttribute[] (cast, not annotated, to dodge excess-property checks on options).

attribute	tab	type	flags	component / extras
name	tab_general	'string'	inList: true	—
is_active	tab_general	Boolean	inList: true	processor: 'Boolean' (FormData "true"/"false" would 422 Laravel's boolean rule)
base_prompt	tab_base_prompt	—	custom: true, inList: false	RichTextFieldWrapper
persona_prompt	tab_persona_prompt	—	custom: true, inList: false	RichTextFieldWrapper
persona_voice	tab_character	'select'	inList: false	options: PERSONA_VOICES, fieldProps: { defaultValue: 'female' }
character_sprite (listAttribute: character_sprite_url)	tab_character	String	custom: true, inList: false, processor: 'File'	CharacterFileUpload, componentProps.formatsLabel: 'PNG atlas • 2048×4096 (4×8 grid of 512px cells) • max 8MB'
character_manifest (listAttribute: character_manifest_url)	tab_character	String	custom: true, inList: false, processor: 'File'	CharacterFileUpload, accept: { 'application/json': ['.json'] }, optional
document_ids	tab_documents	Array	custom: true, inList: false	DocumentIdsSelector
settings	tab_kiosk_settings	String	custom: true, inList: false, inShow: false	AgentKioskSettings
No inCreate/inEdit flags are used anywhere in either schema — only inList, one inShow, and one readOnly.

Two deliberate absences documented in comments: (a) no provider/model fields — AgentConfiguration::booted() stamps config/kt_agent_defaults.php over them on every save; (b) no Instructions/system_prompt tab — the real system prompt is config/kt_agent_system_prompt.php and is never tenant-editable.

/Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent/src/schemas/agentDocument.ts
All five attributes are on tab resource.ai.document.tab_document:

attribute	type	flags	component / extras
file (listAttribute: thumbnail_url)	String	custom: true, inList: false, processor: 'File'	CharacterFileUpload, accepts pdf/doc/docx/txt/md/csv/html, formatsLabel: '... max 50MB'
name	'string'	inList: true	—
description	'textarea'	inList: true	fieldProps: { rows: 4 }; surfaced to the model via KitchntabsAgentContextBuilder::documentCatalog
is_active	Boolean	inList: true	processor: 'Boolean'
original_name	'string'	inList: true, readOnly: true	—
4. Components
DocumentIdsSelector.tsx — DOCUMENTS_RESOURCE = 'ai/document'. Renders a react-admin <List disableSyncWithLocation filter={{ isActive: true }} storeKey="kt-agent-documents-selector"> with a SearchInput toolbar and a checkbox row per document. Three method variants (Edit/Create/View) dispatched by a switch (method). The edit variant seeds from the record, and the comment flags why:


// Seeded from the record rather than left empty: without this the form
// would submit an empty document_ids on any save that didn't touch this
// tab, silently clearing the agent's whole knowledge base.
View mode renders record.documents as MUI Chips.

AgentKioskSettings.tsx — backend-driven UI ported from vx-lab's ProjectSettings. Reads useSystemRequestsCache() (populated by the resource's contextComponent), takes formats.data.setting_formats || formats.data, filters entry.visible !== false, and renders through DashAutoFormTabs wrapped in a FormTabsRenderer component boundary "so DashAutoFormTabs' hooks don't violate Rules of Hooks". The load-bearing gotcha:


// Look the stored value up by `id`, NOT by `attribute` — the
// attribute is the dot PATH ('settings.kiosk_x') while the JSON
// column is keyed by the bare id ('kiosk_x').
const stored = agent?.settings?.[entry.id];
View mode renders MUISimpleJsonTable vertically. Record resolution: const agent = (record as any) ?? recordFromContext; because UserAction passes the record as an explicit prop.

CharacterFileUpload.tsx — switches between ImageInput/FileInput based on whether the accept map contains an image/* mime, and separately renders the already-saved asset from record[attribute.listAttribute || attribute.attribute], because ImageInput binds to the write field (character_sprite) which the API never returns.

5. package.json / entry
/Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent/package.json — name kt-agent, v1.0.0, type: module, main/module = dist/index.js, types: "./src/index.ts".


"exports": {
  ".": "./dist/index.js",
  "./resources": "./dist/resources/index.js",
  "./src/resources": "./dist/resources/index.js",
  "./schemas": "./dist/schemas/index.js",
  "./src/schemas": "./dist/schemas/index.js",
  "./*": "./dist/*.js",
  "./src/*": "./dist/*.js"
},
"typesVersions": { "*": { "src/*": ["src/*", "src/*/index"], "*": ["src/*", "src/*/index"] } }
Dependencies: @mui/icons-material ^9.3.0, @mui/material ^9.3.0, react 19.2.8, react-admin 5.15.1, react-dom 19.2.8. Dev: the @dashadmin/dash-{eslint,prettier,tsconfig} 1.3.47 trio + typescript. Note dash-admin, dash-auto-admin, dash-constants, react-hook-form are all imported by source but not declared as deps (the standard kt-* convention — they resolve from the consuming app).

src/index.ts is three lines: export * from './resources' | './schemas' | './components'.

6. Every registration site of kt-agent across the monorepo
Monorepo-wide grep for kt-agent outside the package itself returns exactly 8 files:

File	What it does
/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/src/resources/KitchnTabsWebTenantPrivateResources.tsx	THE ONLY ACTUAL REGISTRATION. Registers both agentConfigResource and agentDocumentResource.
/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/package.json:46	"kt-agent": "workspace:*" dependency
/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-app/package.json:46	"kt-agent": "workspace:*" dependency — but the app registers no agent resource
/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/src/i18n/en.tsx:363 and es.tsx	resource.ai.* translation block (comment // AI agent (kt-agent))
/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-app/src/i18n/en.tsx:468 and es.tsx	identical resource.ai.* translation block — present but unused, since no manifest in that app loads the resources
/Users/farandal/KITCHNTABS/kitchntabs-frontend/pnpm-lock.yaml	workspace link
The single registration block:


// apps/kitchntabs-web/src/resources/KitchnTabsWebTenantPrivateResources.tsx:74-78
// ========================================================================
// AI AGENT RESOURCES (from kt-agent)
// ========================================================================
agentConfigResource: () => import('kt-agent/resources/agentConfigResource'),
agentDocumentResource: () => import('kt-agent/resources/agentDocumentResource'),
Nothing in apps/kitchntabs-system, apps/vanexa-*, or any other package references kt-agent. Vite resolves kt-agent/resources/... to packages/kt-agent/src/resources/... in dev via the always-on localPackageSrc.aliases block in /Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/vite.config.mts:586-628.

7. Manifest comparison: tenancy vs tenant
The dispatcher: /Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/src/KitchnTabsWebPrivateAppLoader.tsx

 * Loads different resource manifests depending on tenant context:
 * - Tenancy level (no active_tenant_id): Loads KitchnTabsWebPrivateResources (tenancy admin resources)
 * - Tenant level (active_tenant_id set): Merges tenant-specific resources + routes
It reads dashStorage.getItem('active_tenant_id') on mount and listens for the tenant_switch window event from TenantSwitcher, bumping switchKey to force a full react-admin remount. Then, at line 115:


if (isTenantLevel) {
  // Tenant-level: load ONLY tenant-specific resources (not merged with base)
  // Base manifest already contains the same keys - merging produces identical resources
  import('./resources/KitchnTabsWebTenantPrivateResources') ...
} else {
  // Tenancy-level: load only base resources
  import('./resources/KitchnTabsWebPrivateResources') ...
}
Note the doc comment says "merges" but the code does not — the tenant branch loads the tenant manifest exclusively. Only routes are merged (baseRts.private() + tenantRoutes()).

/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/src/resources/KitchnTabsWebPrivateResources.tsx — TENANCY level
Loads when a TenancyAdmin is logged in with no active tenant. Contents: tenancyResources (local ./private/tenancyResources — account, subscription, invoices, payment methods, tenants, service accounts), geohierarchy, the ecommerce catalog set, import/export, marketplace/checkout gateway/POS/metadata/campaign. Mall, tabs, cashcount, self-service and mall-service are absent or commented out. No agent resources. Its header comment is the generic boilerplate ("Resource manifest for the KitchnTabs application") — it does not describe the tenancy/tenant split.

/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/src/resources/KitchnTabsWebTenantPrivateResources.tsx — TENANT level
Loads once a TenancyAdmin switches into a specific tenant. Its header comment is the one that documents the split:


 * Resource manifest for the KitchnTabs TenancyAdmin panel (kitchntabs-web),
 * loaded once a TenancyAdmin switches (TenantSwitcher) into a specific
 * tenant. This mirrors what that tenant's own kitchntabs-app session shows,
 * so a TenancyAdmin sees the exact same menu a restaurant's own account
 * would — mall/tabs/self-service/mall-service resources included.
 *
 * KitchnTabsWebPrivateAppLoader loads ONLY this manifest at tenant level
 * (it does not merge with KitchnTabsWebPrivateResources), so this file must
 * be a complete tenant-scoped set, not just a delta.
It carries everything the tenancy manifest has minus tenancyResources, plus mallResources ("SYSTEM_ROLE-gated; included for parity"), tabResources, cashCountResource, selfServiceResource, mallServiceResource, ecommerceTenantResource — and the two agent resources.

/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-app/src/resources/KitchnTabsWebPrivateResources.tsx — the only manifest in kitchntabs-app
kitchntabs-app has no tenant-level manifest at all; /Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-app/src/KitchnTabsWebPrivateAppLoader.tsx says why:


 * kitchntabs-app is a single-tenant session — its users belong to exactly
 * one tenant, so there is no tenant-switching to react to here (that's a
 * kitchntabs-web/vanexa-web-only feature for TenancyAdmins). This loader
 * always resolves the one resource manifest and never remounts.
Its single manifest additionally carries profileResource (via ./profileResourceOverride) and userResource from dash-admin, which the web manifests do not. It has mallResources, tabResources, cashCountResource, selfServiceResource, mallServiceResource, ecommerceTenantResource — but no checkoutGatewayResource (present in both web manifests) and no agent resources.

Bottom line on the agent resources
Only apps/kitchntabs-web/src/resources/KitchnTabsWebTenantPrivateResources.tsx currently carries them. Consequences:

A TenancyAdmin at tenancy level (no tenant selected) does not see AI Agent or Agent Documents.
A restaurant logging into kitchntabs-app does not see them either, despite the app already depending on kt-agent in package.json and already shipping the full resource.ai.* i18n block in en.tsx/es.tsx. Adding the same two lines to apps/kitchntabs-app/src/resources/KitchnTabsWebPrivateResources.tsx is all that's missing there — the resources' roles array already includes DASHAppConstants.system.TENANT_ROLE.



1. Cross-tenant / TENANT-column patterns
The framework has no dedicated "tenant column" abstraction. A foreign key rendered as a readable name is declared with a type: '<model>.<field>' string on a schema attribute (parsed in AttributeToField.tsx, see §3). Here are all live tenant-reference hits:

a) apps/kitchntabs-web/src/resources/private/tenancyResources.tsx:465-518 (identical at apps/vanexa-web/.../tenancyResources.tsx:465-518)
Inside the tenancy/users resource — the one real cross-tenant list in the codebase (a TenancyAdmin sees users belonging to any of their tenants, with a tenant column):


{
    tab: 'Datos Usuario',
    label: 'Cliente',
    attribute: 'tenant_id',
    //listAttribute: 'name',
    type: 'system/tenant.name',
    pagination: false,
    multiple: false,
    component: SelectInput,
    fieldProps: {
        allowEmpty: true,          // Allow empty selection
        emptyText: 'Sin cliente',  // Text for empty option
    },
    componentProps: {
        link: false,
        parse: (value: any) => { /* '' | undefined | 'null' -> null; numeric string -> Number */ },
        format: (value: any) => { /* null/undefined -> '' */ }
    },
    processor: 'Null',
},
Note this one points at system/tenant (a System-level endpoint) — a caveat if you copy it for a TenancyAdmin-only screen.

b) apps/kitchntabs-web/src/resources/private/schemas/service_account.tsx:31-43 (same in vanexa-web)
The cleanest and most recent template — same idea but resolved against the tenancy-scoped endpoint tenancy/tenants, and explicitly inList: true:


{
    tab: 'Datos',
    label: 'resource.tenancy.serviceAccounts.tenant',
    attribute: 'tenant_id',
    type: 'tenancy/tenants.name',
    multiple: false,
    pagination: false,
    component: SelectInput,
    // The key is pinned to this tenant permanently.
    inEdit: false,
    inList: true,
},
c) packages/kt-mall/src/schemas/MallSchema.tsx:29-50
Reference plus a custom searchable autocomplete (custom: true overrides the default reference input, but type still drives the list-view ReferenceField):


{
    tab: 'Management',
    label: 'Manager Tenant',
    attribute: 'manager_tenant_id',
    listAttribute: 'manager_tenant',
    type: "system/tenant.name",
    custom: true,
    pagination: false,
    multiple: false,
    component: ({ method, attribute, resourceConfig }) =>
        <SearchableSelectChipsControlRecordContext
            ... resource={"system/tenant"} viewAttribute={'name'} valueKeyId={'id'}
            renderText={(option) => option?.name ? `${option.name}` : ''} ... />
}
Resource: packages/kt-mall/src/resources/MallResources.tsx:13 → roles: [DASHAppConstants.system.SYSTEM_ROLE], model: "system/mall".

d) Commented-out precedents (still useful as the canonical shape)
packages/kt-ecommerce/src/schemas/pricelist.tsx:15-24 — attribute: 'tenant_id', type: 'tenant/tenant.name'
packages/kt-ecommerce/src/schemas/stocktype.tsx:14-22 — attribute: 'tenant_id', type: 'ecommerce/tenant.name'
packages/kt-ecommerce/src/schemas/tenant_superadmin.tsx:122-152 and tenant_tenant.tsx:186-215 — 'ecommerce/tenants.name', 'ecommerce/tenant.public_id'
e) tenant_ids (many-to-many) — the actual multi-tenant assignment pattern
Every one of these uses custom: true + component: TenantIdsSelector, inList: false:
kt-ecommerce/src/schemas/: checkoutGateway.tsx:37-46, gallery.ts:51-57, metadata.tsx:65-71, category.ts:86-92, brand.tsx:78-84, modifiers.tsx:91-97, product.tsx:385-391, pricelist.tsx:45-51, stocktype.tsx:92-98, pointofsaleSchema.tsx:100-106, tenantMarketplace.tsx:109-115, systemMarketplace.ts:50, systemPointOfSale.ts:49; plus kt-mall/src/schemas/MallSchema.tsx:95.

Representative (checkoutGateway.tsx:36-46):


{
    // Which stores (tenants) this instance serves; bound to tenant_ids, synced on save.
    attribute: "tenant_ids",
    type: String,
    custom: true,
    component: TenantIdsSelector,
    inList: false,
    inCreate: true,
    inEdit: true,
    inShow: false,
},
2. TenantIdsSelector — /Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-ecommerce/src/components/TenantIdsSelector.tsx
Pattern: a mode-dispatching custom field component that embeds a nested react-admin <List resource='tenancy/tenants'> and writes an id array straight into the react-hook-form state.

Default export is a switch on method (edit / create / view|list) returning TenantIdsSelectorEdit / ...Create / ...View. This is the standard IDashAutoAdminCustomFieldComponent contract ({ method, attribute, resourceConfig, record }).
Edit: useEditContext() seeds Set<string> from record.tenant_ids, then setValue("tenant_ids", ids) (react-hook-form useFormContext). Toggling a checkbox mutates the Set and calls setValue("tenant_ids", Array.from(updated)) immediately — no hidden input, the value only lives in RHF.
The picker itself is a full react-admin <List> with disableSyncWithLocation, resource='tenancy/tenants', storeKey='tenancy-tenants', a <SearchInput source="q" alwaysOn> in a TopToolbar, and PaginationComponent from dash-components. Rows are rendered by TenantsListWithCheckboxes, which reads useListContext() and renders item.name + <Checkbox>.
View/list mode reads record.tenants (the hydrated relation, not the ids) and renders MUI <Chip label={tenant.name}>.
Hard-coded 'tenancy/tenants' — note that unlike TenantMarketplaceSelector it does not read resourceConfig.config.
Similar/related components (packages/kt-ecommerce/src/components/): TenantMarketplaceSelector.tsx, TenantMarketplaceSelectorForUser.tsx, TenantMarketplaceAssociation.tsx, TenantPointOfSaleAssociation.tsx, TenantMarketplaceResource/TenantMarketplaceSelector.tsx, RASearchableSelectChipsRecordContext.tsx (used by MallSchema). vx-lab/src/resources/labProjectResource.tsx:174-179 reuses the exact same shape for document_ids + DocumentIdsSelector.

Configurable-resource variant worth copying — TenantMarketplaceSelector.tsx:28:


const { data: tenant } = useGetOne(`${resourceConfig.config?.tenant_selector_model || "tenant/tenant"}`, { id: tenantContext.id }, { refetchOnWindowFocus: false });
fed by the resource config at tenancyResources.tsx:197:


config: { tenant_selector_model: 'tenant/tenant'}, // custom config resourceConfig dependant to let the TenantMarketplaceSelector in the schema know which model to use for fetching tenant data
3. How DashAdmin declares a reference/lookup column
IDashAutoAdminReference — /Users/farandal/KITCHNTABS/dash-frontend-core/packages/dash-auto-admin/src/interfaces/IDashAutoAdminReference.ts (full file)

import IDashAutoAdminAttribute from './IDashAutoAdminAttribute';

export interface IDashAutoAdminReference {
	reference: string;
	target: string;
	type?: 'ReferenceArrayField' | 'ReferenceManyField';
	tab?: string;
	schema: IDashAutoAdminAttribute[];
	BulkActions?: any;
}
Consumed at IDashAutoAdminResourceConfig.ts:61 (references?: IDashAutoAdminReference[]), rendered by dash-auto-admin/src/DashAutoReferenceTab.tsx, src/mui/AutoReferenceTab.tsx, src/mui/AutoReferenceFormTab.tsx, src/TabbedLayout.tsx.

Important: references is a related-records tab on a show/edit page, not a list column. The only live usage in the whole monorepo is /Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-ecommerce/src/resources/regionResource.tsx:28-30:


references: [
    { reference: 'commune', tab: 'Comunas', target: 'region_id', schema: communesSchema, type: "ReferenceManyField" },
],
Everywhere else it is commented out (pointOfSaleResource.tsx:35, marketplaceResource.tsx:21, currencyResource.tsx:21, statsResource.tsx:38, metadataFormatsResource.tsx:23, notificationResource.tsx:17, systemPointOfSaleResource.tsx:21, systemMarketplaceResource.tsx:21, tenancyResources.tsx:534).

The actual list-column mechanism — dash-auto-admin/src/mui/AttributeToField.tsx

// line 341-348
if (typeof input.type === 'string') {
    const _params = {...};
    const _inputType = replaceParams(_params, input.type);
    const [reference, sourceName] = _inputType.split('.');

    if (input && input.multiple === false) {
        const componentProps = {
            ...,
            label: input.label,
            link: 'show',
            source: input.listAttribute ? input.listAttribute : input.attribute,
            reference: reference,
            ...input.componentProps
        }
        ...  // -> ReferenceField / TextField(source=sourceName)
and for the multiple case (line 254-292) it emits <ReferenceArrayField reference={reference}><SingleFieldList><ChipField source={sourceName} /></SingleFieldList></ReferenceArrayField>.

So: type: 'tenancy/tenants.name' + multiple: false ⇒ ReferenceField on tenancy/tenants displaying .name. listAttribute overrides the source used in list view; fieldProps.linkType: false / componentProps.link: false disables the drill-through link (see tenancyResources.tsx:448-455 on roles for a working example).

2-3 real kt-* usages (FK → readable name in a list)
packages/kt-ecommerce/src/schemas/pricelist.tsx:26-34 — attribute: 'currency_id', type: 'ecommerce/currency/forSelect.code', multiple: false, component: SelectInput.
packages/kt-mall/src/schemas/MallSchema.tsx:29-33 — attribute: 'manager_tenant_id', listAttribute: 'manager_tenant', type: "system/tenant.name".
apps/*/src/resources/private/schemas/service_account.tsx:31-43 — attribute: 'tenant_id', type: 'tenancy/tenants.name', inList: true.
apps/*/src/resources/private/tenancyResources.tsx:446-458 — the array/multiple case: attribute: 'roles', listAttribute: 'role_ids', type: 'system/role.name', multiple: true, fieldProps: { linkType: false }.
4. /Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/src/resources/KitchnTabsWebPrivateResources.tsx — complete contents
71 lines. Header comment says resources are loaded via dynamic import() so Vite can code-split. Exports KitchnTabsWebPrivateResources: ResourceManifest (type from dash-app-common), and re-exports as default.

Registered keys (active):

key	import
tenancyResources	./private/tenancyResources
communeResource	kt-ecommerce/resources/geohierarchy/communeResource
countryResource	kt-ecommerce/resources/geohierarchy/countryResource
regionResource	kt-ecommerce/resources/geohierarchy/regionResource
productResource	kt-ecommerce/resources/productResource
categoryResource	kt-ecommerce/resources/categoryResource
galleryResource	kt-ecommerce/resources/galleryResource
brandResource	kt-ecommerce/resources/brandResource
currencyResource	kt-ecommerce/resources/currencyResource
pricelistResource	kt-ecommerce/resources/pricelistResource
stockTypeResource	kt-ecommerce/resources/stockTypeResource
modifierGroupResource	kt-ecommerce/resources/modifiersResource
productImportTemplateResource	kt-ecommerce/resources/productImportTemplateResource
productImportInstanceResource	kt-ecommerce/resources/productImportInstanceResource
marketplaceResource	kt-ecommerce/resources/marketplaceResource
checkoutGatewayResource	kt-ecommerce/resources/checkoutGatewayResource
pointOfSaleResource	kt-ecommerce/resources/pointOfSaleResource
metadataFormatsResource	kt-ecommerce/resources/metadataFormatsResource
campaignResource	kt-ecommerce/resources/campaignResource
Commented out (line numbers): privateWebResources (23), ecommerceTenantResource (25), mallResources (36), systemMarketplaceResource (59), systemPointOfSaleResource (60), orderResource (63), deliveryDriverResource (64), deliveryRouteResource (65).

Note the key observation for your task: at tenancy level, kitchntabs-web registers many tenant-domain kt-ecommerce resources — i.e. this manifest is not strictly tenancy-scoped today. The vanexa-web equivalent is clean (only tenancyResources + labResources).

5. VaneXa manifests — /Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/vanexa-web/src/resources/
Files: KitchnTabsWebPrivateResources.tsx, KitchnTabsWebPublicResources.tsx, KitchnTabsWebTenantPrivateResources.tsx, plus private/ (tenancyResources.tsx, schemas/{service_account,tenancy_account,tenancy_invoice,tenancy_payment_method,tenancy_subscription,tenancy_tenant}.tsx) and public/homeResources.tsx.

vx-lab is registered at BOTH levels in vanexa-web:

Tenancy level — KitchnTabsWebPrivateResources.tsx:18-24:

export const KitchnTabsWebPrivateResources: ResourceManifest = {
    tenancyResources: () => import('./private/tenancyResources'),
    labResources: () => import('vx-lab/resources/labResources'),
};
Tenant level — KitchnTabsWebTenantPrivateResources.tsx:18-28 (only entry), with the comment: "vanexa-web is the TenancyAdmin panel: this is what a TenancyAdmin sees once they switch (TenantSwitcher) into a specific tenant, matching what that tenant's own vanexa-app session shows."

labResources: () => import('vx-lab/resources/labResources'),
Public — KitchnTabsWebPublicResources.tsx:23: publicWebResources: () => import('./public/homeResources').
apps/vanexa-app/src/resources/KitchnTabsWebPrivateResources.tsx registers profileResource (./profileResourceOverride), userResource (dash-admin/resources/User/userResource), labResources (vx-lab/resources/labResources).
Because labResources is registered at tenancy level too, it currently shows up in the tenancy menu — but every resource in it is role-gated to Tenant/TenancyAdmin:
packages/vx-lab/src/resources/labResources.tsx:60-65 exports only [LabProjectResourceWithWindow, LabDocumentResource] (AgentConfig and McpServer are commented out).

labProjectResource.tsx:178-180 → roles: ['Tenant']
labDocumentResource.tsx:125-129, mcpServerResource.tsx:65-69, agentConfigResource.tsx:69-73 → roles: [DASHAppConstants.system.SYSTEM_ROLE, 'TenancyAdmin', 'Tenant']
Manifest switching logic — apps/vanexa-web/src/KitchnTabsWebPrivateAppLoader.tsx:107-189: const isTenantLevel = !!tenantContext (from dashStorage.getItem('active_tenant_id'), re-evaluated on a tenant_switch window event, line ~100). Tenant level loads ONLY KitchnTabsWebTenantPrivateResources ("not merged with base"); tenancy level loads only KitchnTabsWebPrivateResources. Both go through clearResourceCache(manifest) → loadResourcesFromManifest(manifest) → dispatch(setReduxResources(resolved)).

6. Role gating
checkRole — /Users/farandal/KITCHNTABS/dash-frontend-core/packages/dash-admin/src/helpers/checkRole.tsx (lines 18-30, full impl)

const checkRole = (permissions, roles) => {
	const debug = false;
	if (debug) console.info('Check Roles', permissions, roles);
	if ((Array.isArray(roles) && roles.map(r => r.toLowerCase()).includes('*'))) return true;
	if (permissions.map(r => r.toLowerCase()).includes('system')) return true;
	const cookie_tenant_id = getCookie('tenant_id');
	if (roles.map(r => r.toLowerCase()).includes('has_admin_id') && !cookie_tenant_id) return false;
	return roles.map(r => r.toLowerCase()).find((role) => permissions.map(r => r.toLowerCase()).includes(role));
};
Key behaviours: case-insensitive; '*' = everyone; anyone holding the literal role system bypasses everything; 'HAS_ADMIN_ID' is a pseudo-role requiring a tenant_id cookie.

Call sites: dash-admin/src/DASHAdmin.tsx:297-299; menu filtering default-theme/menu/AppMaterialMenu.tsx:260 (resource.group === group && checkRole(userRoles, resource.roles)) and :358 (!hasGroup && checkRole(userRoles, resource.roles) && resource.hidden !== true); dashboard tiles default-theme/menu/AppDashboardGrid.tsx:138.

Constants — /Users/farandal/KITCHNTABS/dash-frontend-core/packages/dash-constants/src/DASHAppConstants.ts:7-32

const DASHAppConstants = {
	system: {
    GUEST_ROLE: { id: 99, level: 99, name: 'Guest' },
    URL_PREFIX: getEnv('DASH_URL_PREFIX') || '#/', // When using drawer
		SYSTEM_ROLE:  getEnv('DASH_SYSTEM_ROLE') || 'System',
		TENANT_ROLE: getEnv('DASH_TENANT_ROLE') || 'Tenant',
		USER_ROLE: getEnv('DASH_USER_ROLE') || 'User',
    /* APP ROLES */
		CREATOR_ROLE: getEnv('APP_CREATOR_ROLE') || 'Creador',
		CLOSING_ROLE: getEnv('APP_CLOSING_ROLE') || 'Cerrador',
		GUNNER_ROLE: getEnv('APP_GUNNER_ROLE') || 'Pistolero',
		DRIVER_ROLE: getEnv('APP_DRIVER_ROLE') || 'Conductor',
    /* OTHERS */
    LOGIN_SOUNDS: ..., UI_SOUNDS: ..., RECAPTCHA_ENABLED: ..., RECAPTCHA_TOKEN: ..., DEFAULT_ROWS_PER_PAGE: ...,
	},
	...
A second, overlapping set lives in /Users/farandal/KITCHNTABS/dash-frontend-core/packages/dash-constants/src/DASHAdminSystemConstants.tsx:47-50:


  DASH_SYSTEM_ROLE: getEnv('DASH_SYSTEM_ROLE') || 'System',
  DASH_ADMIN_ROLE: getEnv('DASH_ADMIN_ROLE') || 'Administrator',
  HAS_ADMINISTRATOR_ID_ROLE: 'HasAdministratorId',
  ENABLE_TENANT_LOGIC: getEnv('ENABLE_TENANT_LOGIC') || true,
(dash-admin/src/resources.tsx uses constants.system.DASH_SYSTEM_ROLE; systemResources.tsx uses DASHAppConstants.system.SYSTEM_ROLE. Both resolve to 'System'.)

Answer to your specific question: 'TenancyAdmin' is NOT a constant.
It exists only as a bare string literal, everywhere:

apps/{kitchntabs,vanexa}-web/src/resources/private/tenancyResources.tsx lines 79, 101, 135, 164, 191 → roles: ["TenancyAdmin", "System"]; line 313 → roles: ["TenancyAdmin"]
packages/vx-lab/src/resources/{labDocumentResource,mcpServerResource,agentConfigResource}.tsx → 'TenancyAdmin' mixed with DASHAppConstants.system.SYSTEM_ROLE
packages/kt-agent/src/resources/{agentConfigResource.tsx:27,agentDocumentResource.tsx:25} → 'TenancyAdmin'
Other bare-string roles in use: "ServiceAccountManager" (tenancyResources.tsx:600), "Tenant", "System", "*".

7. The tenancy-admin-exclusive resource — your closest template
roles: ["TenancyAdmin"] (and nothing else) appears exactly once: the tenancy/users resource at
/Users/farandal/KITCHNTABS/kitchntabs-frontend/apps/kitchntabs-web/src/resources/private/tenancyResources.tsx:311-586 (byte-identical in apps/vanexa-web/...:311-586).


{
       roles: ["TenancyAdmin"],
        component: ResourceTemplate,
        trash: true,
        isFormData: true,
        model: 'tenancy/users',
         group: "resource.tenancy.groups.system",
        label: 'resource.system.users.label',
        refreshAfter: true,
        referenceFilters: [
            {
                id: 'search',
                label: 'resource.system.users.filter_search',
                source: 'q',
                reference: null,
                optionText: '',
                alwaysOn: true,
            },
        ],
        icon: <Person />,
        redirectAfterUpdate: false,
        showDialogAfterSubmit: true,
        showNotifyAfterSubmit: true,
        menu: [
            { title: 'resource.system.users.menu_list', redirect: '/tenancy/users' },
            { title: "🗑", redirect: "/tenancy/users/trash" }
        ],
        mainAction: {
            title: 'resource.system.users.main_action',
            redirect: '/tenancy/users/create',
        },
        mutationMode: 'pessimistic',
        dataGridProps: { stickyHeader: true, rowClick: false },
        dataGridWrapper: (props: any) => (
            <TableContainer sx={{ maxHeight: 800 }}>{props.children}</TableContainer>
        ),
        formPostFormatter: (params, form) => { return form; },
        ...drawerSettings,
},
Its inline schema (lines 323-533) contains the tenant_id → 'system/tenant.name' column quoted in §1a. This is the one resource in the repo that genuinely lists records across many tenants for a TenancyAdmin.

Shared drawerSettings used by every resource in that file (tenancyResources.tsx:50-60):


const drawerSettings = {
    drawer: true,
    drawerOptions: { view: true, edit: true, create: false },
    listViewButton: { props: { buttonProps: { variant: 'text', size: 'small' }, label: '' } },
    listEditButton: { props: { buttonProps: { variant: 'text', size: 'small' }, label: '' } },
};
Runner-up templates

tenancy/tenants (tenancyResources.tsx:189-306, roles: ["TenancyAdmin", "System"], path: "/tenancy/tenants", schema: tenancyTenantSchema, config: { tenant_selector_model: 'tenant/tenant' }, referenceFilters: [{ id:"name", source:"name", reference:null, alwaysOn:true }], contextComponent wrapping non-list modes in SystemRequestsCache, postFormatter normalising the attributes array-to-object hack). This is literally the list of tenants.
system/service_accounts (tenancyResources.tsx:594-660, roles: ["ServiceAccountManager", "System"], path: "/tenancy/service-accounts") — the newest, best-commented resource; shows a tenant column via tenancy/tenants.name, toolbarCreateButton: { enabled: true } (create:true alone does not render it), and a createSuccessDialog override.
Recommended composition for a new tenancy-admin cross-tenant list
Add the resource object to apps/vanexa-web/src/resources/private/tenancyResources.tsx (or a new file registered in KitchnTabsWebPrivateResources.tsx — not ...TenantPrivateResources.tsx, since that manifest is only loaded when active_tenant_id is set).
roles: ["TenancyAdmin"] — bare string; System bypasses automatically via checkRole, so you don't need to list it.
model: 'tenancy/<thing>', group: "resource.tenancy.groups.system", component: ResourceTemplate, ...drawerSettings.
Tenant column: { attribute: 'tenant_id', type: 'tenancy/tenants.name', multiple: false, inList: true, component: SelectInput } — use the tenancy/-prefixed endpoint, not system/tenant.
If you need multi-tenant assignment rather than a single FK, reuse TenantIdsSelector with custom: true, component: TenantIdsSelector, inList: false.
1. Routes
File: /Users/farandal/KITCHNTABS/kitchntabs-backend-domain/routes/api/ai_agent.php

Loaded by /Users/farandal/KITCHNTABS/kitchntabs-backend-domain/routes/api.php, which does foreach (glob(base_path('domain/routes/api/*.php'))), itself grouped under prefix api + middleware api by /Users/farandal/KITCHNTABS/dash-backend/app/Providers/RouteServiceProvider.php:39.

Outer group (line 22):


Route::group(['middleware' => ['access', 'auth:sanctum', 'verified'], 'as' => 'ai.', 'prefix' => 'ai'], function () {
access = App\Http\Middleware\AccessMiddleware (dash-backend/app/Http/Kernel.php:69) — the route_name → permission gate.

ai/agent-config → AgentConfigController (route names api.ai.agent-config.*)
Two hand-registered routes first (deliberately before the /{id} loop):

Method	URI	Controller method	Route name
GET	/api/ai/agent-config/current	getForTenant	api.ai.agent-config.getForTenant
GET	/api/ai/agent-config/settings/formats	getSettingFormats	api.ai.agent-config.getSettingFormats
Then the config('react-admin-methods') loop (/Users/farandal/KITCHNTABS/dash-backend/config/react-admin-methods.php), each with ->middleware('ControllerOptions:mode/<mode>'), expanding to (relative to /api/ai/agent-config):

getList GET / (view) · getMany GET /getMany (view) · getManyReference GET /getManyReference (view) · getForSelect GET /getForSelect (view) · deleteMany POST /deleteMany (edit) · audit GET /audit/{id} (view) · auditAll GET /audit (view) · update PUT /{id} (view) · partial POST /partial/{id} (view) · postUpdate POST /{id}/update (edit) · updateMany POST /updateMany (edit) · getOne GET /{id} (getOne) · create POST / (edit) · putCreate PUT / (edit) · delete DELETE /{id} (edit) · postDelete POST /{id}/delete (edit) · filterValues GET /filter/{field} (view) · filterValue GET /filter/{field}/getMany (view) · interfaces GET /interfaces (view)

ai/document → AgentDocumentController (route names api.ai.document.*)
Same react-admin loop, no hand-registered extras (getForSelect is covered by the loop and overridden in the controller).

ai/chat → AgentChatController (api.ai.chat.*)
GET|POST sessions, GET|PUT|DELETE sessions/{sessionId}, GET|POST sessions/{sessionId}/messages, POST sessions/{sessionId}/messages/simple, GET sessions/{sessionId}/context.

Role gating (permission migrations, .../database/migrations/permissions/)
2026_08_09_170000_add_ai_agent_config_permissions.php — all api.ai.agent-config.* CRUD + getForTenant granted to Role::NAME_TENANCY_ADMIN ('TenancyAdmin') and Role::NAME_TENANT_ADMIN ('Tenant') only, level: 2, group ai.agent-config.
2026_08_11_000300_add_ai_agent_config_setting_formats_permission.php — api.ai.agent-config.getSettingFormats → same two roles.
2026_08_11_000400_add_ai_agent_config_kiosk_read_permission.php — api.ai.agent-config.getForTenant additionally → Role::NAME_NORMAL_USER ('User') and Role::NAME_STAFF ('Staff') (for the Python voice kiosk).
2026_08_11_000100_add_ai_agent_document_permissions.php — all api.ai.document.* → TenancyAdmin + Tenant only.
Frontend prefix confirmation — MATCHES
/Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent/src/resources/agentConfigResource.tsx:31 → model: 'ai/agent-config', and line 73 apiUrl="ai/agent-config/settings/formats".
/Users/farandal/KITCHNTABS/kitchntabs-frontend/packages/kt-agent/src/resources/agentDocumentResource.tsx:29 → model: 'ai/document'.
2. Controllers
/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Http/Controllers/API/AI/AgentConfig/AgentConfigController.php
Class properties: $resource = AgentConfigResource::class, $requestValidator = AgentConfigRequest::class, $modelFilter = AgentConfigFilter::class, $policy = AgentConfigPolicy::class, $_model = AgentConfiguration::class; constructor sets $this->model = AgentConfiguration::query();. Extends App\Http\Controllers\API\System\ReactAdminBaseController, uses HandlesImageUploads.

_preList() — THIS IS THE SCOPING ANSWER (lines 45-66):


public function _preList($request)
{
    // Eager-loaded here and not only in _postGetOne because the frontend's
    // Edit view is populated from a getList-shaped fetch (a list row gets
    // promoted straight into the edit record cache) rather than a separate
    // getOne round trip — without this, document_ids is silently absent on
    // the form even though GET .../agent-config/{id} returns it correctly.
    $this->model->with('documents');

    $user = auth()->user();

    if ($user->isSystemAdmin()) {
        return;
    }

    if ($user->hasRole(Role::NAME_TENANCY_ADMIN)) {
        $this->model->where('tenancy_id', $user->tenancy_id);
        return;
    }

    $this->model->where('tenant_id', $user->tenant_id);
}
So: SystemAdmin → unscoped; TenancyAdmin → tenancy_id = user.tenancy_id (all tenants in the tenancy, ignoring X-Tenant-Id); everyone else → tenant_id = user.tenant_id. It does not use visibleThroughTenant, so the tenant-switcher header narrowing that every other resource honours is absent here.

_preGetOne() — DOES NOT EXIST on this controller. The base controller (ReactAdminBaseController::getOne, line 563-593) only calls _preGetOne if it exists, then does $this->model->findOrFail($id) against the unscoped AgentConfiguration::query(). _preList is not invoked for getOne. Same for AgentDocumentController. This is an IDOR: any role with the getOne permission can read any tenant's agent config / document row by uuid. (Update/delete are protected, since _update/_delete call _authorize('manage', $item).)

_create() (lines 78-126):


public function _create($request)
{
    $this->_authorize('create', null);

    $user     = auth()->user();
    $tenantId = $this->activeTenantId($user);

    // Without this guard a user carrying no tenant_id would upsert against
    // ['tenant_id' => null] — which is the PLATFORM-WIDE fallback row that
    // EloquentAgentConfigResolver hands to every tenant that hasn't
    // configured its own agent. ...
    if (!$tenantId) {
        return response()->json([
            'message' => 'An active tenant is required to configure an agent.',
        ], 422);
    }

    $validated = app($this->requestValidator)->validated();

    $documentIds = $validated['document_ids'] ?? null;
    unset(
        $validated['character_icon'],
        $validated['character_sprite'],
        $validated['character_manifest'],
        $validated['document_ids'],
    );

    $this->handleCharacterUploads($request, $validated, $user->tenancy_id, $tenantId);

    // One config per tenant — a second "create" edits the existing row.
    $item = AgentConfiguration::updateOrCreate(
        ['tenant_id' => $tenantId],
        array_merge($validated, [
            'tenancy_id' => $user->tenancy_id,
        ])
    );

    if (is_array($documentIds)) {
        $item->documents()->sync($this->documentIdsForTenant($documentIds, $tenantId));
    }

    return $this->resource::make($item->load('documents'));
}
Note: tenancy_id is stamped from $user->tenancy_id, not from the target tenant's tenancy — for a SystemAdmin or a tenancy-only admin this can write a tenancy_id inconsistent with tenant_id's actual tenancy.

_update() (lines 128-151):


public function _update($request, $id, $item)
{
    $this->_authorize('manage', $item);

    $validated = app($this->requestValidator)->validated();

    $documentIds = $validated['document_ids'] ?? null;
    unset(
        $validated['character_icon'],
        $validated['character_sprite'],
        $validated['character_manifest'],
        $validated['document_ids'],
    );

    $this->handleCharacterUploads($request, $validated, $item->tenancy_id, $item->tenant_id);

    $item->update($validated);

    if (is_array($documentIds)) {
        $item->documents()->sync($this->documentIdsForTenant($documentIds, $item->tenant_id));
    }

    return $this->resource::make($item->load('documents'));
}
Tenancy resolution helper activeTenantId() (lines 181-202) — the only place X-Tenant-Id is honoured:


private function activeTenantId(User $user): ?string
{
    if (!$user->isTenancyAdmin() || !$user->tenancy_id) {
        return $user->tenant_id;
    }

    $activeTenantId = request()->header('X-Tenant-Id');

    if ($activeTenantId) {
        $belongsToTenancy = Tenant::where('id', $activeTenantId)
            ->where('tenancy_id', $user->tenancy_id)
            ->exists();

        if ($belongsToTenancy) {
            return $activeTenantId;
        }
    }

    return $user->tenant_id ?: Tenant::where('tenancy_id', $user->tenancy_id)
        ->oldest()
        ->value('id');
}
Note the asymmetry vs core scopeVisibleThroughTenant: on an invalid header this falls back to the home/oldest tenant rather than failing closed.

Also documentIdsForTenant() (re-derives ids by tenant_id), _delete() (_authorize('delete', $item)), getSettingFormats() (returns config('kt_agent_kiosk_settings.setting_formats')), and getForTenant():


$config = AgentConfiguration::with('documents')
    ->where('tenant_id', $this->activeTenantId($user))
    ->where('is_active', true)
    ->first();
/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Http/Controllers/API/AI/AgentDocument/AgentDocumentController.php
use DashFileStorage; $resource/$requestValidator/$modelFilter/$policy/$_model → AgentDocumentResource / AgentDocumentRequest / AgentDocumentFilter / AgentDocumentPolicy / AgentDocument; constructor __construct(private KitchntabsAgentRagService $rag) sets $this->model = AgentDocument::query();.

_preList() (lines 48-61) — NO TenancyAdmin branch at all:


public function _preList($request)
{
    // Eager-loaded for the same reason as AgentConfigController::_preList —
    // the edit form is populated from a getList-shaped fetch.
    $this->model->with('agentConfigurations');

    $user = auth()->user();

    if ($user->isSystemAdmin()) {
        return;
    }

    $this->model->where('tenant_id', $user->tenant_id);
}
Asymmetry: documents list is scoped strictly by tenant_id; a TenancyAdmin with no home tenant_id (tenancy-only account) gets where tenant_id = null → zero rows, while the config list for the same user returns the whole tenancy. getForSelect() (lines 158-168) has the same tenant_id-only scoping.

_preGetOne() — does not exist (same IDOR note as above).

_create() (lines 73-116):


public function _create($request)
{
    $this->_authorize('create', null);

    $user = auth()->user();

    if (!$user->tenant_id) {
        return response()->json([
            'message' => 'An active tenant is required to upload agent documents.',
        ], 422);
    }

    $file = $request->file('file');

    $documentId   = (string) Str::uuid();
    $originalName = $file->getClientOriginalName();
    $name         = $request->input('name') ?: pathinfo($originalName, PATHINFO_FILENAME);

    // file_path holds the S3 key in the RAG bucket, not a local disk path.
    $key = $this->rag->store($file, $documentId, (string) $user->tenant_id);

    $thumbnailPath = $this->generateThumbnail($file, $documentId, $user->tenancy_id, $user->tenant_id);

    $item = AgentDocument::create([
        'id'             => $documentId,
        'tenant_id'      => $user->tenant_id,
        'tenancy_id'     => $user->tenancy_id,
        'uploaded_by'    => $user->id,
        'name'           => $name,
        'description'    => $request->input('description'),
        'original_name'  => $originalName,
        'file_path'      => $key,
        'thumbnail_path' => $thumbnailPath,
        'file_type'      => $file->getMimeType(),
        'file_size'      => $file->getSize(),
        'is_active'      => true,
    ]);

    $this->syncAgentSelection($request, $item, (string) $user->tenant_id);

    SyncAgentKnowledgeBaseJob::dispatch();

    return $this->resource::make($item->load('agentConfigurations'));
}
Note: it uses $user->tenant_id directly and never calls anything like activeTenantId() — a TenancyAdmin using the tenant switcher uploads to their home tenant, not the switched one.

_update() (lines 118-134):


public function _update($request, $id, $item)
{
    $this->_authorize('manage', $item);

    // Metadata only — the indexed object is immutable for this document id ...
    $item->update([
        'name'        => $request->input('name', $item->name),
        'description' => $request->input('description', $item->description),
        'is_active'   => $request->boolean('is_active', $item->is_active),
    ]);

    $this->syncAgentSelection($request, $item, (string) $item->tenant_id);

    return $this->resource::make($item->load('agentConfigurations'));
}
3. Requests / Resources / Filters / Policies
/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Http/Request/AI/AgentConfigRequest.php

return [
    'name'           => 'nullable|string|max:255',
    'settings'       => 'nullable|array',
    'is_active'      => 'nullable|boolean',

    // Persona
    'base_prompt'    => 'nullable|string',
    'persona_prompt' => 'nullable|string',
    'persona_voice'  => 'nullable|string|max:16',

    'character_icon'     => 'nullable|file|mimes:png,jpg,jpeg,webp|max:4096',
    'character_sprite'   => 'nullable|file|mimes:png,jpg,jpeg,webp|max:8192',
    'character_manifest' => 'nullable|file|mimetypes:application/json,text/plain|max:1024',

    'document_ids'   => 'nullable|array',
    'document_ids.*' => 'uuid',
];
Deliberately NOT accepted: tenant_id, tenancy_id, agent_key, provider, model, system_prompt, instructions. No authorize() override (FormRequest default true; gating is via policy in the controller).

/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Http/Request/AI/AgentDocumentRequest.php

$isCreate = $this->isMethod('post') && !$this->route('id');

return [
    'file' => [
        $isCreate ? 'required' : 'nullable',
        'file',
        'mimes:pdf,doc,docx,txt,md,csv,html',
        'max:51200', // 50 MB
    ],
    'name'        => 'nullable|string|max:255',
    'description' => 'nullable|string|max:2000',
    'is_active'   => 'nullable|boolean',

    'agent_configuration_ids'   => 'nullable|array',
    'agent_configuration_ids.*' => 'uuid',
];
/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Http/Resources/AI/AgentConfigResource.php

public function toArray($request)
{
    return [
        'id'            => $this->id,
        'tenant_id'     => $this->tenant_id,
        'tenancy_id'    => $this->tenancy_id,
        'agent_key'     => $this->agent_key,
        'name'          => $this->name,
        'provider'      => $this->provider,
        'model'         => $this->model,
        'system_prompt' => $this->system_prompt,
        'instructions'  => $this->instructions,
        'settings'      => $this->settings,
        'is_active'     => $this->is_active,

        'base_prompt'    => $this->base_prompt,
        'persona_prompt' => $this->persona_prompt,
        'persona_voice'  => $this->persona_voice,

        'character_icon_path'     => $this->character_icon_path,
        'character_sprite_path'   => $this->character_sprite_path,
        'character_manifest_path' => $this->character_manifest_path,
        'character_icon_url'      => $this->character_icon_url,
        'character_sprite_url'    => $this->character_sprite_url,
        'character_manifest_url'  => $this->character_manifest_url,

        'document_ids' => $this->whenLoaded(
            'documents',
            fn () => $this->documents->pluck('id')->all()
        ),
        'documents' => AgentDocumentResource::collection($this->whenLoaded('documents')),

        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
No tenant.name / tenancy label is exposed — worth noting if a TenancyAdmin list needs to show which tenant a row belongs to.

/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Http/Resources/AI/AgentDocumentResource.php

public function toArray($request)
{
    return [
        'id'            => $this->id,
        'tenant_id'     => $this->tenant_id,
        'tenancy_id'    => $this->tenancy_id,
        'uploaded_by'   => $this->uploaded_by,
        'name'          => $this->name,
        'description'   => $this->description,
        'original_name' => $this->original_name,
        'file_type'     => $this->file_type,
        'file_size'     => $this->file_size,
        'thumbnail_url' => $this->thumbnail_url,
        'is_active'     => $this->is_active,

        // Deliberately NOT exposed: file_path.

        'agent_configuration_ids' => $this->whenLoaded(
            'agentConfigurations',
            fn () => $this->agentConfigurations->pluck('id')->all()
        ),

        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
Filters
/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/ModelFilters/AI/AgentConfigFilter.php — $drop_id = false, $relations = []; methods q($search) (ILIKE over name, provider, model), id, provider, isActive. No tenantId / tenancyId filter method — so a frontend filter={"tenant_id":...} would be ignored.

/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/ModelFilters/AI/AgentDocumentFilter.php — same shape; q over name, description, original_name; plus id, fileType, isActive.

Policies
/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Policies/AI/AgentConfigPolicy.php:


public function manage(User $user, AgentConfiguration $item)
{
    if ($user->isSystemAdmin()) { return true; }
    if ($user->hasRole(Role::NAME_TENANCY_ADMIN) && $user->tenancy_id == $item->tenancy_id) { return true; }
    if ($user->hasRole(Role::NAME_TENANT_ADMIN) && $user->tenant_id == $item->tenant_id) { return true; }
    return false;
}

public function create(User $user)
{
    return $user->isSystemAdmin()
        || $user->hasRole(Role::NAME_TENANCY_ADMIN)
        || $user->hasRole(Role::NAME_TENANT_ADMIN);
}

public function delete(User $user, AgentConfiguration $item) { return $this->manage($user, $item); }
The TenancyAdmin branch checks $item->tenancy_id — a row whose tenancy_id is NULL (created before the column was stamped, or created by a path that didn't set it) is invisible/unmanageable to a TenancyAdmin even if its tenant_id belongs to their tenancy.

/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Policies/AI/AgentDocumentPolicy.php — identical structure against AgentDocument.

4. Models
Core: /Users/farandal/KITCHNTABS/dash-backend/app/AiAgentCore/Models/AgentConfiguration.php

protected $table = 'ai_agent_configurations';
protected $keyType = 'string';
public $incrementing = false;
protected $guarded = [];          // no $fillable — everything mass-assignable
protected $casts = [
    'is_active'     => 'boolean',
    'settings'      => 'array',
    'enabled_tools' => 'array',
];
public $sortable = ['id','agent_key','name','provider','model','is_active','created_at'];
Traits: HasFactory, Filterable, QueryCacheable. Relations: sessions(), tenant() → App\Models\Tenant, tenancy() → App\Models\Tenancy (so tenancy_id exists and is a real FK).

Domain subclass: /Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Models/AI/AgentConfiguration.php
extends App\AiAgentCore\Models\AgentConfiguration. Adds protected $appends = ['character_icon_url','character_sprite_url','character_manifest_url'];, overrides booted() (calls parent::booted(), then defaults base_prompt/persona_voice on create, and a saving() hook that force-stamps provider/model from config('kt_agent_defaults.*')), overrides tenant() → Domain\App\Models\Extended\Tenant, adds documents() belongsToMany via kt_agent_document_selections, and the three *_url accessors. It does not use ResourceVisibility, so AgentConfiguration::visibleThroughTenant() does not exist today.

/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Models/AI/AgentDocument.php

protected $table = 'kt_agent_documents';
protected $keyType = 'string';
public $incrementing = false;
protected $guarded = [];
protected $appends = ['thumbnail_url'];
protected $casts = ['is_active' => 'boolean', 'file_size' => 'integer'];
public $sortable = ['id','name','file_size','is_active','created_at'];
Traits HasFactory, Filterable, SoftDeletes; relations agentConfigurations() (pivot) and tenant(). No tenancy() relation and no ResourceVisibility.

Both models have tenant_id AND tenancy_id columns.

5. Migrations
/Users/farandal/KITCHNTABS/dash-backend/app/AiAgentCore/database/migrations/2026_08_10_000010_create_ai_agent_tables.php
Registered via AiAgentCoreServiceProvider::loadMigrationsFrom(__DIR__.'/database/migrations') (line 58). Every create is if (!Schema::hasTable(...)) guarded.

ai_agent_configurations:

Column	Type
id	uuid, primary
tenant_id	uuid, nullable, FK → tenants.id cascade, indexed
tenancy_id	uuid, nullable, FK → tenancies.id cascade — YES, it exists
agent_key	string, default 'default'
name	string, nullable
provider	string, default 'anthropic'
model	string, default 'claude-sonnet-4-6'
system_prompt	text, nullable
instructions	text, nullable
settings	json, nullable
enabled_tools	json, nullable
is_active	boolean, default true
created_at/updated_at	timestamps
—	unique(['tenant_id','agent_key']), index('tenant_id')
Note: no index on tenancy_id (only the FK). No soft deletes.

ai_agent_mcp_servers: id uuid pk, tenant_id uuid nullable FK, tenancy_id uuid nullable FK, name string, description text nullable, transport_type string default 'sse', url string nullable, config json nullable, auth_token text nullable (encrypted cast), is_active boolean default true, softDeletes, timestamps, index tenant_id.

ai_agent_sessions: id uuid pk, agent_configuration_id uuid nullable FK→ai_agent_configurations set null, tenant_id uuid nullable FK→tenants cascade, user_id uuid nullable FK→users cascade, nullableUuidMorphs('subject') (subject_type string + subject_id uuid), title string nullable, is_active boolean default true, metadata json nullable, timestamps, index tenant_id. No tenancy_id on sessions.

ai_agent_messages: id uuid pk, agent_session_id uuid FK cascade, role string, content longText, tool_calls json nullable, tool_results json nullable, metadata json nullable, timestamps, index agent_session_id.

/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/database/migrations/2026_08_11_000000_add_agent_persona_and_documents.php
Adds to ai_agent_configurations (all nullable): base_prompt text (after instructions), persona_prompt text, persona_voice string(16), character_icon_path string, character_sprite_path string, character_manifest_path string.

Creates kt_agent_documents:

Column	Type
id	uuid, primary
tenant_id	uuid, NOT NULL, FK → tenants.id cascade, indexed
tenancy_id	uuid, nullable, FK → tenancies.id on delete SET NULL — YES, it exists
uploaded_by	uuid, nullable
name	string
description	text, nullable
original_name	string
file_path	string (S3 key in RAG bucket)
thumbnail_path	string, nullable (media disk)
file_type	string, nullable
file_size	unsignedBigInteger, default 0
is_active	boolean, default true
deleted_at	softDeletes
created_at/updated_at	timestamps
Creates kt_agent_document_selections: id bigIncrements (deliberately not uuid — pivot sync), agent_configuration_id uuid FK→ai_agent_configurations cascade, document_id uuid FK→kt_agent_documents cascade, timestamps, unique(['agent_configuration_id','document_id']).

Other
/Users/farandal/KITCHNTABS/kitchntabs-backend-domain/database/migrations/2026_08_11_000200_create_kt_agent_carts.php references ai_agent_sessions.
/Users/farandal/KITCHNTABS/dash-backend/app/AiAgentCore/database/migrations/2026_08_11_000010_create_ai_usage_events_table.php.

No other migration in either repo alters ai_agent_configurations or kt_agent_documents.

6. config/ai_agent_core.php
It is not at dash-backend/config/ai_agent_core.php — it lives at /Users/farandal/KITCHNTABS/dash-backend/app/AiAgentCore/config/ai_agent_core.php and is merged by AiAgentCoreServiceProvider line 35: $this->mergeConfigFrom(__DIR__ . '/config/ai_agent_core.php', 'ai_agent_core');


<?php

return [
    /*
     * How many times the agent may call tools and come back for another turn
     * before we stop feeding results in. ...
     */
    'max_tool_iterations' => (int) env('AI_AGENT_MAX_TOOL_ITERATIONS', 3),

    /*
     * Which agent `resolveFor()` picks when the caller doesn't name one. ...
     */
    'default_agent_key' => env('AI_AGENT_DEFAULT_KEY', 'default'),

    /*
     * Cap on agents per tenant. null = uncapped (the natural behaviour).
     * A product that offers exactly one configurable agent per tenant sets
     * this to 1 — enforced in AgentConfiguration, so it holds for every
     * creation path rather than just the UI that happens to check.
     */
    'max_agents_per_tenant' => env('AI_AGENT_MAX_PER_TENANT') !== null
        ? (int) env('AI_AGENT_MAX_PER_TENANT')
        : null,

    /*
     * Token/timing accounting. ...
     */
    'usage' => [
        'enabled' => filter_var(env('AI_AGENT_USAGE_ENABLED', true), FILTER_VALIDATE_BOOLEAN),
        'persist' => filter_var(env('AI_AGENT_USAGE_PERSIST', true), FILTER_VALIDATE_BOOLEAN),
        'log_channel' => env('AI_AGENT_USAGE_LOG_CHANNEL', 'ai-agents'),
        'source' => env('AI_AGENT_USAGE_SOURCE', env('DOMAIN_NAME', config('app.name'))),
    ],

    /*
     * Ceiling on a single broadcast AG-UI event. ...
     */
    'broadcast' => [
        'max_event_bytes' => (int) env('AI_AGENT_MAX_EVENT_BYTES', 8192),
    ],

    'mcp' => [
        'server_name'    => env('AI_AGENT_MCP_SERVER_NAME', config('app.name', 'dash') . '-mcp'),
        'server_version' => '1.0.0',
        'required_ability' => env('AI_AGENT_MCP_ABILITY', 'mcp:invoke'),
    ],
];
max_agents_per_tenant in the KitchnTabs deployment is forced to 1 by the domain, not by env — /Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Providers/AppDomainServiceProvider.php:139:


// KitchnTabs gives each tenant exactly one agent. AiAgentCore supports
// many per tenant (unique on tenant_id + agent_key) and treats the cap
// as policy rather than a schema variant, so this is the whole opt-in —
// enforced in AgentConfiguration::creating(), which means seeders and
// console commands hit the same limit as the API.
//
// Set here rather than in .env so the guarantee travels with the domain
// instead of depending on every environment remembering to declare it.
// A plain config() write for the same reason mergeDomainTenantSettings()
// uses one: mergeConfigFrom() only fills keys that are entirely absent,
// and AiAgentCoreServiceProvider has already published this one.
config(['ai_agent_core.max_agents_per_tenant' => 1]);
AI_AGENT_MAX_PER_TENANT appears nowhere else in either repo or in kitchntabs-ci-cdk.

7. app/AiAgentCore/ — resolver + cap enforcement
/Users/farandal/KITCHNTABS/dash-backend/app/AiAgentCore/Services/EloquentAgentConfigResolver.php (full)

class EloquentAgentConfigResolver implements AgentConfigResolverContract
{
    public function resolveFor(?string $tenantId, ?string $agentKey = null): mixed
    {
        $key = $agentKey ?: config('ai_agent_core.default_agent_key', 'default');

        $config = AgentConfiguration::query()
            ->where('is_active', true)
            ->when($tenantId, fn ($q) => $q->where('tenant_id', $tenantId))
            ->where('agent_key', $key)
            ->first();

        if (!$config && $agentKey !== null && $tenantId !== null) {
            $config = AgentConfiguration::query()
                ->where('is_active', true)
                ->where('tenant_id', $tenantId)
                ->where('agent_key', config('ai_agent_core.default_agent_key', 'default'))
                ->first();
        }

        $config = $config ?: AgentConfiguration::query()
            ->where('is_active', true)
            ->whereNull('tenant_id')
            ->first();

        if (!$config) {
            throw new NoActiveAgentConfigurationException(
                'No active agent configuration for tenant ' . ($tenantId ?? 'null') . " (agent_key: {$key})"
            );
        }

        return $config;
    }

    public function listFor(?string $tenantId): Collection
    {
        return AgentConfiguration::query()
            ->when($tenantId, fn ($q) => $q->where('tenant_id', $tenantId))
            ->orderBy('agent_key')
            ->get();
    }
}
Resolution is tenant_id-only — tenancy_id plays no part. Fallback #3 is the platform-wide tenant_id IS NULL row. Bound in AiAgentCoreServiceProvider:42. Note it returns the core AgentConfiguration, not the domain subclass (so the domain's saving()/persona hooks and documents() are absent on resolver-returned instances).

Cap enforcement — /Users/farandal/KITCHNTABS/dash-backend/app/AiAgentCore/Models/AgentConfiguration.php

protected static function booted(): void
{
    static::creating(function (self $config) {
        $config->id = $config->id ?: (string) Str::uuid();
        $config->agent_key = $config->agent_key
            ?: config('ai_agent_core.default_agent_key', 'default');

        self::guardTenantAgentLimit($config);
    });
}

/**
 * Enforced here rather than in a controller so every path — API, seeder,
 * console command, another domain's own UI — hits the same limit.
 */
private static function guardTenantAgentLimit(self $config): void
{
    $max = config('ai_agent_core.max_agents_per_tenant');

    if ($max === null || $config->tenant_id === null) {
        return;
    }

    $existing = static::query()->where('tenant_id', $config->tenant_id)->count();

    if ($existing >= (int) $max) {
        throw new TooManyAgentsForTenantException(
            "Tenant {$config->tenant_id} already has {$existing} agent(s); the configured limit is {$max}."
        );
    }
}
Note static::query() on the domain subclass resolves to the same ai_agent_configurations table, and the count is not filtered by soft-deletes (there are none) — so with the cap at 1 a tenant that already has a row can never create a second, which is precisely what updateOrCreate(['tenant_id' => $tenantId], ...) in the controller sidesteps. Exception class: /Users/farandal/KITCHNTABS/dash-backend/app/AiAgentCore/Exceptions/TooManyAgentsForTenantException.php.

8. visibleThroughTenant — the existing tenant-visibility scope
There are two traits with the same method name.

A. The one the agent controllers' docblock references and that Tab uses: /Users/farandal/KITCHNTABS/dash-backend/app/Traits/ResourceVisibility.php
Tab uses this one — /Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Models/Tab/Tab.php:6 use App\Traits\ResourceVisibility;, line 27 use HasFactory, ResourceVisibility, .... Called at TabController.php:258, 670, 698, 784 e.g. $this->model->visibleThroughTenant($request->user()).


public function scopeVisibleThroughTenant($query, User $user)
{
    // System Admins can see everything
    if ($user->isSystemAdmin()) {
        $requestTenantId = request()->get('tenant_id');
        if ($requestTenantId && is_numeric($requestTenantId)) {
            return $query->where('tenant_id', $requestTenantId);
        }
        return $query;
    }

    // TenancyAdmin: scoped to whichever single tenant the switcher
    // currently has active (X-Tenant-Id header ...). No header
    // (the "Tenancy Account" / tenancy-wide view) keeps the previous
    // see-everything-in-the-tenancy behavior.
    //
    // The header is validated against the user's own tenancy before
    // being trusted ... It fails closed (no rows) rather than
    // silently falling back to the full tenancy ...
    if ($user->isTenancyAdmin() && $user->tenancy_id) {
        $activeTenantId = request()->header('X-Tenant-Id');

        if ($activeTenantId) {
            $belongsToTenancy = \App\Models\Tenant::where('id', $activeTenantId)
                ->where('tenancy_id', $user->tenancy_id)
                ->exists();

            if ($belongsToTenancy) {
                return $query->where('tenant_id', $activeTenantId);
            }

            return $query->whereRaw('1 = 0');
        }

        // Check if this model has a tenancy_id column
        $model = $query->getModel();
        $hasTenancyIdColumn = \Illuminate\Support\Facades\Schema::hasColumn($model->getTable(), 'tenancy_id');

        if ($hasTenancyIdColumn) {
            // Model has tenancy_id column - use direct check OR tenant relationship
            return $query->where(function($q) use ($user) {
                $q->where('tenancy_id', $user->tenancy_id)
                  ->orWhereHas('tenant', fn($sub) => $sub->where('tenancy_id', $user->tenancy_id));
            });
        } else {
            // Model doesn't have tenancy_id column - rely only on tenant relationship
            return $query->whereHas('tenant', fn($sub) => $sub->where('tenancy_id', $user->tenancy_id));
        }
    }

    return $query->where('tenant_id', $user->tenant_id);
}
Answer to your question: yes, it handles TenancyAdmin explicitly and in a three-way manner:

X-Tenant-Id present + valid for their tenancy → narrowed to that single tenant.
X-Tenant-Id present + invalid → fails closed (whereRaw('1 = 0')).
No header ("Tenancy Account" view) → all tenants in the tenancy, via tenancy_id = user.tenancy_id OR tenant.tenancy_id = user.tenancy_id (the OR whereHas('tenant') leg is what rescues rows with a NULL tenancy_id). It auto-detects the tenancy_id column with Schema::hasColumn, so it works on both agent tables as-is.
Plain Tenant/User → tenant_id = user.tenant_id.

Same file also has scopeVisibleThroughRelationTenant($query, $relation, User $user) (lines 101-138) with identical TenancyAdmin logic applied through a relation.

Other core consumers: dash-backend/app/Http/Controllers/API/Tenant/TenantUserController.php, .../API/Logs/LogController.php, app/Providers/ConstantsProvider.php.

B. The e-commerce variant: /Users/farandal/KITCHNTABS/kitchntabs-backend-domain/app/Http/Traits/ECommerce/ResourceVisibility.php
Used by the ECommerce controllers (Product, Category, Brand, Gallery, …). Differences that matter if you copy it:

It ignores X-Tenant-Id entirely; a TenancyAdmin always sees the whole tenancy.
SystemAdmin with no tenant_id in the request falls back to $user->tenant_id rather than returning everything.
It has an explicit whitelist $modelsWithTenantsRelationship for the many-to-many tenants() pivot leg (AgentConfiguration/AgentDocument are not in it, and have no tenants() relation).
TenancyAdmin branch:

if ($user->isTenancyAdmin() && $user->tenancy_id) {
    $hasTenantRelation = method_exists($model, 'tenant');

    return $query->where(function($q) use ($user, $hasTenantsRelation, $hasTenantRelation) {
        $q->where('tenancy_id', $user->tenancy_id);

        if ($hasTenantRelation) {
            $q->orWhereHas('tenant', fn($sub) => $sub->where('tenancy_id', $user->tenancy_id));
        }

        if ($hasTenantsRelation) {
            $q->orWhereHas('tenants', fn($sub) => $sub->where('tenancy_id', $user->tenancy_id));
        }
    });
}
It also offers scopeVisibleThroughTenancy() (pure tenancy_id match) and its own scopeVisibleThroughRelationTenant().

Summary of the gaps most relevant to what you're likely about to change
AgentConfiguration and AgentDocument do not use either ResourceVisibility trait — both controllers hand-roll scoping in _preList, and the two hand-rolled versions disagree with each other and with the core scope.
AgentConfigController::_preList uses tenancy_id for TenancyAdmin and ignores X-Tenant-Id, while AgentConfigController::activeTenantId() (used by _create and getForTenant) does honour X-Tenant-Id. So a TenancyAdmin's list shows every tenant's agent regardless of the switcher, but "create"/"current" target the switched tenant. Also, _preList does not check $user->tenancy_id is non-null, so a TenancyAdmin without a tenancy would match all rows with tenancy_id IS NULL… actually where('tenancy_id', null) produces = NULL → no rows, so it fails closed there.
AgentDocumentController::_preList / getForSelect / _create have no TenancyAdmin branch at all — a tenancy-only TenancyAdmin (tenant_id null) sees zero documents and gets a 422 on upload, even though they can create/see the agent config.
Neither controller defines _preGetOne, so GET /api/ai/agent-config/{id} and GET /api/ai/document/{id} run findOrFail against an unscoped query — cross-tenant read for anyone holding the getOne permission.
tenancy_id exists on both tables (ai_agent_configurations and kt_agent_documents), both nullable with real FKs, so switching to visibleThroughTenant (core version) would work without a migration — but existing rows created before the tenancy_id stamp, or created with a tenancy_id taken from $user->tenancy_id while tenant_id came from X-Tenant-Id, may be inconsistent.