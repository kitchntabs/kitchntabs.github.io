# feat/ai-tenant-settings
# AI settings in the tenant settings at a kitchntabs backend domain layer. 

## AI Settings:

> **Status:** ✅ Implemented on branch `feat/ai-tenant-settings` (dash-backend,
> kitchntabs-backend-domain). 7/7 feature tests passing. No frontend changes -
> the Tenant Settings Module's backend-driven UI renders the new `ai` tab
> automatically. See [Implementation notes](#implementation-notes) below for
> where the plan needed a small core change.
> **Layer:** `kitchntabs-backend-domain` **domain** feature for the settings
> themselves (schema + which sub-keys are secret), plus one small, deliberately
> generic **dash-backend core** addition: encryption-at-rest for whichever
> setting sub-keys any domain declares as secret. See notes below for why the
> "no core changes" premise didn't hold once real third-party API keys were
> involved.
> **Related:** [F21 — Teanant Settigs Module](../kitchntabs.github.io/docs/F21-Tenancy-Management/F21-Tenancy-Management_TENANT_SETTINGS_MODULE.md)

### 1. Goal

The AI Tenant Settings section allows at a Tenant level to configure custom domain settings specifically for AI features. 
The settings must allow to configure an OPEN_AI Key and ANTHROPIC_KEY for now, more to add in the future.
It must allow to select by Tenant, which is the default AI provider to be used. 
It must allow a text editor to input the main Agent instructions. 

A default agent will be like: 
"Eres el asistente virtual de {Tenant Name}, un {Tenant Description}. Responde de forma breve, cálida y natural, como si hablaras cara a cara con un cliente frente al mostrador."

So we will have
OPENAI_KEY
ANTHROPIC_KEY
ELEVENLABS_KEY
AGENT_MAIN_PROMPT

The audio AI (ElevenLabs) is a separate concern from the text/chat LLM (OpenAI/Anthropic), so the
tenant needs two independent provider selectors, not one:

- `primary_llm_ai` — which provider answers text/chat: `openai` | `anthropic`
- `primary_audio_ai` — which provider handles voice/audio synthesis: `elevenlabs` (only option today,
  extensible)

---

## Implementation notes

### How it uses the existing Tenant Settings Module

Per [F21](../kitchntabs.github.io/docs/F21-Tenancy-Management/F21-Tenancy-Management_TENANT_SETTINGS_MODULE.md),
adding a tenant setting is normally a backend-only change: define an entry in `setting_formats`, and
the existing `TenantSettings`/`DashAutoFormTabs` frontend renders it automatically, grouped by
whatever `tab` value the entry declares. `alarm_settings` (an existing domain setting under a
`notifications` tab) already proves a domain-introduced tab renders with zero frontend changes — this
feature adds a new `ai` tab the same way.

The domain does **not** edit `dash-backend/config/tenants.php` directly. It ships its own
`kitchntabs-backend-domain/config/ai_tenant_settings.php`, which
`AppDomainServiceProvider::mergeDomainTenantSettings()` appends onto core's
`config('tenants.setting_formats')` at boot — the same mechanism already used for
`config/tenant_settings.php` and `config/checkout_tenant.php`.

### The six settings

| id | tab | type | encrypted | notes |
|---|---|---|---|---|
| `primary_llm_ai` | `ai` | `select` | no | `openai` \| `anthropic` |
| `primary_audio_ai` | `ai` | `select` | no | `elevenlabs` (only option today) |
| `ai_openai_key` | `ai` | `string` | **yes** | |
| `ai_anthropic_key` | `ai` | `string` | **yes** | |
| `ai_elevenlabs_key` | `ai` | `string` | **yes** | |
| `ai_agent_main_prompt` | `ai` | `textarea` | no | default value is the template above; `{Tenant Name}`/`{Tenant Description}` are resolved at runtime by whatever agent service consumes this setting — not by this settings feature |

### Why "no core changes required" turned out to be wrong

Three OpenAI/Anthropic/ElevenLabs API keys are real, billing-linked, third-party secrets — not
ordinary tenant preferences. The tenant `settings` column had no encryption of any kind before this
feature (a plain `array` cast), and the controller that actually serves tenant-settings writes
(`System\TenantController`) resolves the bare **core** `App\Models\Tenant` class directly, not the
domain extension. A domain-only encryption approach — overriding a method on
`Domain\App\Models\Extended\Tenant` — was tried first and **silently did not apply** on that real
write path, confirmed empirically before shipping it: encrypting only where the domain class happens
to be used would have given a false sense of security while every real admin save stored the key in
plaintext.

The fix that actually works regardless of which concrete class is instantiated: a **config-driven**
list.

- **Core** (`dash-backend`): `config/tenants.php` gains one new key, `encrypted_setting_keys` (empty
  by default — core defines the mechanism, not the secrets). `App\Models\Tenant` gains
  `getSettingsAttribute()`/`setSettingsAttribute()`, which transparently encrypt/decrypt (via
  `Crypt::encryptString()`/`decryptString()`) whichever sub-keys `getEncryptedSettingKeys()` lists,
  leaving every other setting untouched. A value that fails to decrypt (written before encryption
  existed, or via a path that bypassed the mutator) is returned as-is rather than throwing.
- **Domain**: `config/ai_tenant_settings.php` also declares `'encrypted_setting_keys' =>
  ['ai_openai_key', 'ai_anthropic_key', 'ai_elevenlabs_key']`, merged into
  `config('tenants.encrypted_setting_keys')` by the same `mergeDomainTenantSettings()` that already
  merges `setting_formats` — so the two travel together from one file.

Because `config()` is process-global rather than tied to a class hierarchy, this applies identically
whether a `Tenant` record is instantiated as the core class or the domain extension — verified by a
test that hits the encryption path via `new App\Models\Tenant()` directly, matching exactly what
`System\TenantController` does.

**Important caveat, not a bug:** the decrypted plaintext value still appears in the edit form for any
actor with tenant-edit access — the existing settings UI pre-fills every field's current value on
open (`TenantSettingsEdit` reads `tenant.settings[settingName]` directly). Encryption protects the
value **at rest in the database** (from a DB dump, backup, leaked query log, or a compromised DB-only
credential) — it does not, and architecturally cannot without new frontend masking work, hide the
value from someone who already has permission to edit this tenant's settings. That's the same trust
boundary as any other admin-managed credential in this system.

### Files changed

```
dash-backend/
├── config/tenants.php                          [modified: +encrypted_setting_keys key]
├── app/Models/Tenant.php                        [modified: +getEncryptedSettingKeys(),
│                                                  getSettingsAttribute()/setSettingsAttribute()
│                                                  now encrypt/decrypt; removed the redundant
│                                                  'settings' => 'array' cast entry - it silently
│                                                  wins over a magic accessor/mutator pair in this
│                                                  Eloquent version, confirmed empirically]
└── tests/Feature/TenantSettingsEncryptionTest.php  [new, 7 tests]

kitchntabs-backend-domain/
├── config/ai_tenant_settings.php                [new: the 6 setting_formats entries +
│                                                  encrypted_setting_keys]
└── app/Providers/AppDomainServiceProvider.php   [modified: register the new config file;
                                                   mergeDomainTenantSettings() also merges
                                                   encrypted_setting_keys]
```

`Domain\App\Models\Extended\Tenant` needed **no change** — it inherits the core accessor/mutator
pair via normal PHP inheritance, and reads the same merged `config('tenants.encrypted_setting_keys')`
as the core class.

### Test coverage

`tests/Feature/TenantSettingsEncryptionTest.php` (dash-backend), 7 tests:

- listed setting keys are encrypted at rest (raw DB row holds real, `Crypt`-decryptable ciphertext;
  an unlisted key in the same settings array is stored untouched)
- encrypted values round-trip transparently on a fresh read
- encryption applies via the bare core `Tenant` class specifically (the real-world case that broke
  under the domain-only design)
- a legacy/pre-encryption plaintext value decrypts gracefully (returned as-is) rather than throwing
- encryption applies through the real `PUT /api/system/tenant/{id}` admin endpoint end-to-end, not
  only at the model layer
- the new `ai` tab's six settings are exposed via the real `GET
  /api/system/tenant/systemSettingFormats` endpoint
- settings with no encrypted keys configured are completely unaffected (regression guard for every
  other tenant setting already in production)

Full dash-backend Core suite: 650 passed, one pre-existing unrelated failure
(`SubscriptionPlanManagementTest::it_can_list_subscription_plans`, already documented as unrelated in
the Service Accounts API Keys feature notes).

### Not done / left to a future feature

- No AI agent runtime consumes these settings yet (interpolating `{Tenant Name}`/`{Tenant
  Description}` into `ai_agent_main_prompt`, actually calling OpenAI/Anthropic/ElevenLabs with the
  stored keys). This feature is the settings storage layer only.
- No validation that an entered API key is actually valid/live (e.g. a test call to the provider) -
  only format/length validation on save.
