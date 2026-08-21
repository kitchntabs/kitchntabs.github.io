# MCP tool management for DashAdmin agents

## Context

Both agentic products can *register* MCP servers but neither can *use* them.
`ai_agent_mcp_servers` exists in core and VaneXa has CRUD over it, but the rows
are inert: `LabContextBuilder::formatMcpServers()` only names them in the system
prompt, and `BedrockAgentRunner` never puts them in `toolConfig`. This is listed
as a known limitation in `vanexa-backend-domain/docs/LAB-AGENTIC-INTERFACE.md` §10.
KitchnTabs has no MCP client surface at all — it only *serves* MCP at `POST /api/mcp`.

The goal is that a tenant (KitchnTabs) or a Lab (VaneXa) can register an MCP
server, discover the tools it offers, pick which of those tools the agent may
call, and have the agent actually call them mid-turn.

The two domains anchor "an agent" on different entities, which is the central
constraint: VaneXa's agent is a **LabProject** (many per tenant; persona lives
there, `AgentConfiguration` is tenant-wide), KitchnTabs' agent is the
**AgentConfiguration** row itself (capped at one per tenant). The association
therefore cannot be a plain FK in core.

### Decisions taken

| Fork | Decision |
|---|---|
| Association | Polymorphic pivot in core (`owner_type`/`owner_id`), same idiom core already uses for `ai_agent_sessions.subject` |
| Scope | Full client **and** invocation — discovery, selection, and real `tools/call` during a turn |
| Transport | Streamable HTTP only; `sse`/`docker`/`stdio` remain storable but fail at call time with a clear result |
| Selection scope | Agent-level selection is the default set; a session may **narrow** it for that conversation only |

---

## 1. Core — `dash-backend/app/AiAgentCore`

### 1.1 Migration `database/migrations/2026_08_19_000010_create_ai_agent_mcp_tooling_tables.php`

Guarded with `Schema::hasTable()` like the existing
`2026_08_10_000010_create_ai_agent_tables.php`.

```
ai_agent_mcp_tools                     -- discovery cache, so the picker needs no live call
  id             uuid PK
  mcp_server_id  uuid FK -> ai_agent_mcp_servers  cascade
  name           string                -- the REMOTE name, unprefixed
  description    text null
  input_schema   json null
  is_available   bool default true     -- false = vanished from the server's last tools/list
  last_seen_at   timestamp null
  UNIQUE(mcp_server_id, name)

ai_agent_mcp_selections                -- the morph pivot
  id             bigint PK             -- auto-inc, NOT uuid: sync()/attach() never set a
                                       --   pivot id, and a uuid PK with no DB default fails
                                       --   NOT NULL on every insert (both domains hit this
                                       --   on their *_document_selections tables)
  owner_type     string                -- LabProject | AgentConfiguration
  owner_id       uuid
  mcp_server_id  uuid FK cascade
  enabled_tools  json null             -- null = every discovered tool; [] = none
  is_active      bool default true
  UNIQUE(owner_type, owner_id, mcp_server_id)
  INDEX(owner_type, owner_id)
```

Plus `Schema::table('ai_agent_mcp_servers')`: `last_discovery_at` (timestamp,
null), `last_discovery_error` (text, null), `tool_count` (unsigned int, 0) — so
the list view can show connection health without probing on every render.

### 1.2 Models

- `Models/McpTool` — `belongsTo` server. Casts `input_schema` array, `is_available` bool.
- `Models/McpSelection` — `morphTo('owner')`, `belongsTo` server, casts `enabled_tools` array.
- `Models/McpServerRegistration` — add `tools()` / `selections()` hasMany; update the
  docblock, which currently says "calling out to a registered one as a *client* is
  not implemented yet".
- `Concerns/HasMcpServers` trait — `mcpSelections()` (morphMany) + `mcpServers()`
  (morphToMany through the pivot). Applied to `LabProject` and `AgentConfiguration`
  in the domains. This is the piece that makes one core pivot serve both anchors.

### 1.3 Client — `Mcp/`

- **`McpHttpClient`** — JSON-RPC 2.0 over the `Http` facade: `initialize()`,
  `listTools()`, `callTool($name, $args)`. Bearer from the model's encrypted
  `auth_token`, extra headers from `config`. Speaks the same Streamable HTTP
  transport core's own `McpServerAdapter` already serves, so the two are
  symmetric. A non-`http` `transport_type` throws `McpTransportException`
  immediately rather than attempting a connection.
- **`McpToolDiscoveryService::discover(McpServerRegistration): Collection`** —
  calls `listTools()`, upserts `ai_agent_mcp_tools`, flips vanished rows to
  `is_available = false` (never deletes — a selection referencing it must survive
  a transient outage), writes `last_discovery_at` / `last_discovery_error` /
  `tool_count`.
- **`McpProxyTool implements AgentToolContract`** — one instance per enabled
  remote tool, built per turn.
  - `name()` → `mcp__{serverSlug}__{toolName}`, sanitised to Bedrock's
    `[a-zA-Z0-9_-]{1,64}` and hash-truncated past 64 chars. Namespacing prevents a
    remote `search_menu` colliding with KitchnTabs' own registered one.
  - `parameters()` → the cached `input_schema`.
  - `isServerExecuted()` → `true`.
  - `execute()` → `callTool`, mapped to `AgentToolResult`. A transport failure
    becomes `AgentToolResult::error(...)`, never a throw — matching the contract's
    existing rule that a failed tool is something the model recovers from.

### 1.4 Resolution — `Services/AgentToolResolver`

The single place the two-level selection rule lives:

```
resolve($owner, ?AgentSession $session): array<string, AgentToolContract>
  = ToolRegistry->forNames($agentConfig->enabled_tools)          -- local tools
  + McpProxyTool per (active selection × enabled_tools × is_available)
  − session narrowing: metadata.selected_mcp_ids  (servers)
                       metadata.disabled_mcp_tools (individual tools)
```

Session narrowing can only **remove**, never add — a conversation cannot grant
itself a tool the agent was not configured for.

### 1.5 Required fix — `Services/AgentTurnExecutor::execute()`

It currently resolves the called tool via `$this->registry->get($call['name'])`.
MCP proxies are per-tenant and built per turn, so they are **not** in the global
singleton registry — every MCP call would return `Unknown tool`. `execute()` must
resolve from the advertised `$tools` map (which `resolvable()` already builds)
and fall back to the registry. Small change, but nothing works without it.

### 1.6 Wiring

- `AiAgentCoreServiceProvider`: bind `McpToolProviderContract` → default impl,
  singleton `AgentToolResolver`, register `McpHttpClient`.
- `config/ai_agent_core.php`: new `mcp.client` block — `timeout`, `connect_timeout`,
  `max_tools_per_server`, `discovery_ttl`, `allowed_transports` (default `['http']`).

---

## 2. Domains

Both follow the same shape; the only difference is the owner and the route prefix.

| | VaneXa (`lab/`) | KitchnTabs (`ai/`) |
|---|---|---|
| Owner | `LabProject` | `AgentConfiguration` |
| MCP CRUD | exists at `lab/mcp-server` — extend | **new**, mirroring `agentDocumentResource` |
| Selection endpoint | `PUT lab/project/{id}/mcp-selection` | `mcp_server_ids` on the config's own Save |

**Both get:**
- `use HasMcpServers` on the owner model.
- `POST {prefix}/mcp-server/{id}/discover` → `McpToolDiscoveryService`, returns the
  refreshed tool list. `GET {prefix}/mcp-server/{id}/tools` → the cached rows.
- `mcp_servers` / `mcp_selections` exposed on the owner's API Resource, eager-loaded
  in `_preList`/`_postGetOne` exactly as `documents` already is.
- `RunAgentTurnJob` and `AgentChatController::sendMessageSimple` pass
  `tools: $resolver->resolve($owner, $session)` — neither passes `tools:` today, so
  both silently use `$registry->all()`.
- A permission migration under `database/migrations/permissions/` following the
  existing `2026_08_09_170100_add_ai_agent_chat_permissions.php` pattern (hand-listed
  route names for the non-CRUD `discover`/`tools` routes).

**VaneXa only:** `LabContextBuilder::mcpServersFor()` switches from
`session.metadata.selected_mcp_ids` to the agent-level selection, with the session
value retained as the narrowing filter. `labResources.tsx` currently has
`McpServerResource` commented out of its array — enable it.

**KitchnTabs only:** full new module under
`app/Http/Controllers/API/AI/McpServer/` (Controller, Request, Filter, Policy,
Resource, TrashController), scoped with `visibleThroughTenant` like
`AgentConfigController::_preList`.

---

## 3. Frontend

**`packages/kt-agent`** (new) and **`packages/vx-lab`** (finish the existing stub):

- `resources/mcpServerResource.tsx` — CRUD over the server registration.
  KitchnTabs' is new; VaneXa's exists and needs `auth_token` (password input) and a
  discovery status column added.
- `components/McpServerIdsSelector.tsx` — the association field. Same shape as the
  existing `DocumentIdsSelector` (paginated searchable checkbox list writing a
  `{thing}_ids` array), but each checked server expands to a nested checkbox list of
  its discovered tools writing `mcp_enabled_tools[serverId] = string[]`, plus a
  "Discover tools" button hitting the new endpoint.
- A `tab_mcp` entry on `agentConfigSchema` / `labProjectSchema` pointing at it.
- `AgenticWindow`'s right panel: shows the agent's enabled MCP tools and lets the
  session toggle them off (write-through to `session.metadata.disabled_mcp_tools`) —
  this is the per-session narrowing surface.
- i18n keys under `resource.ai.mcp.*` in `kitchntabs-web` / `kitchntabs-app` (en+es)
  and the VaneXa apps.

Note the form traps from the `dashadmin-forms` skill that apply here: `mcp_enabled_tools`
is a **nested** object, so under `isFormData: true` it must be `processor: 'Stringify'`
and `json_decode`d server-side — a dot path only nests one level.

---

## 4. Verification

**Core (PHPUnit, `dash-backend`):**
- `McpHttpClient` against `Http::fake()` — initialize/list/call, auth header, timeout, non-http transport rejected.
- `McpToolDiscoveryService` — upsert, vanished-tool flip to `is_available=false`, error recorded without throwing.
- `AgentToolResolver` — agent-level set; session narrowing removes; session **cannot** add a tool not configured.
- `AgentTurnExecutor` — a turn calling a proxy tool resolves and continues (this is the §1.5 fix's regression test).

**End to end, local stack** (`pnpm dash:start kitchntabs local`):
- Register a public MCP server, hit `discover`, confirm `ai_agent_mcp_tools` populates.
- Select a subset, then ask the agent something that needs it and watch
  `TOOL_CALL_START/ARGS/RESULT` arrive in the AgenticWindow's tool-activity row.
- Deselect the tool, repeat, confirm it is no longer advertised.
- Run once with `php artisan migrate` (never `migrate:fresh` — the dev DB must survive).

**Frontend:** `pnpm typecheck` + `pnpm build` per package and for `kitchntabs-app` /
`kitchntabs-web` / `vanexa-app`, compared against the current zero-error baseline.

---

## Risks

- **Latency**: each MCP round trip is an extra network hop inside a turn already
  bounded by `max_tool_iterations`. The `timeout` config exists to keep a slow
  remote server from holding a Horizon worker.
- **SSRF**: `url` is tenant-editable and the backend fetches it. Needs at minimum a
  scheme allowlist and a private-IP-range block in `McpHttpClient`; worth confirming
  whether you want an explicit domain allowlist too.
- **Token-cost blowup**: a server advertising 80 tools inflates every prompt.
  `max_tools_per_server` caps it; the tool picker is the real mitigation.
