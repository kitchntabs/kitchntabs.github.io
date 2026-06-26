# ClickUp Setup Blueprint — KitchnTabs Dev & Engineering

> **Space:** KitchnTabs Dev & Engineering — ID `90176181674`
> **Type:** Evergreen project
> **Source of truth for tasks:** development spreadsheet (Tipo / Componente / Description / Desarrollo / Staging / Producción / Notas) + [REQUIREMENTS.md](REQUIREMENTS.md) + `docs/*.md`
> **Status:** Ready to execute via ClickUp MCP once `clickup_*` tools are live in-session.

## Agreed architecture (decisions)

| Decision | Choice |
|---|---|
| Hierarchy | **Component = Epic = Folder** → Feature = **List** → User Story = **Task** → dev work = **Subtask** |
| Functional vs Non-functional | **Custom field (dropdown) + tag** on each item (not a folder split) |
| Environment readiness | **Single status pipeline**: `Backlog → In Dev → In Staging → In Production → Live` |
| Documentation | **Mirror** each `docs/*.md` into **ClickUp Docs**, linked to its Epic |
| Cadence | **Priority-tiered backlog** (native Priority + milestone tags, no sprints) |

---

## 1. Space-level configuration (create first)

### 1.1 Custom task statuses (workflow)
Apply to the whole space:

| Order | Status | Type | Meaning |
|---|---|---|---|
| 1 | `Backlog` | not-started | Planned, not started |
| 2 | `In Dev` | active | Built/working in Desarrollo |
| 3 | `In Staging` | active | Deployed/validating in Staging |
| 4 | `In Production` | active | Deploying / validating in Producción |
| 5 | `Live` | done | Verified live in Producción |
| – | `Blocked` | active | Waiting on external dependency/cert |
| – | `Cancelled` | closed | Won't do |

### 1.2 Custom fields (space-wide)
| Field | Type | Options |
|---|---|---|
| **Tipo** | Dropdown | `Functional`, `Non-Functional` |
| **Doc** | URL | Link to mirrored ClickUp Doc / source doc |
| **Tech Debt** | Text (long) | From spreadsheet `Notas` (deuda técnica) |

### 1.3 Priority (native ClickUp)
`Urgent` / `High` / `Normal` / `Low`.

### 1.4 Tags
- Type tags: `functional`, `non-functional`
- Milestone/theme tags: `payments`, `ai`, `marketplaces`, `infra`, `mobile`, `desktop`, `billing`, `tech-debt`, `cert-pending`

---

## 2. Epics (Folders) — full list

> Each Folder = one Epic. `Tipo` and a starting **rollout status** (derived from the spreadsheet's Dev/Staging/Prod columns) are shown. Each Folder gets its mirrored ClickUp Doc(s).

### Functional epics

| # | Epic (Folder) | Start status | Priority | Mirror docs |
|---|---|---|---|---|
| F1 | **Orders & Tabs** | Live | High | `docs/tech/domain-models/Tab-README.md`, `Order-README.md`, `docs/tech/features/tabs/TABS_MALLTABS_ARCHITECTURE.md`, `docs/tech/architecture/HASH_ID_IMPLEMENTATION.md` |
| F2 | **Products & Catalog** | Live | High | `docs/tech/domain-models/ECommerce-README.md`, `docs/tech/features/ui/MODIFIER_GROUPS_FEATURE.md` |
| F3 | **Product Import / Export** | Live | Normal | `docs/tech/features/products/PRODUCT_IMPORT_SYSTEM_DOCUMENTATION.md`, `PRODUCT_IMPORT_EXPORT_USER_GUIDE.md` |
| F4 | **Mall / Food Court** | Live | High | `docs/mall-app/01-OVERVIEW.md` … `10-FLOW-DIAGRAMS.md`, `docs/tech/domain-models/Mall-README.md` |
| F5 | **Customer & Self-Service** | Live | High | `docs/customer-app/CUSTOMER_APP_COMPLETE_FLOW.md`, `MALL_SESSION_NOTIFICATIONS_FLOW.md`, `MALL_SESSION_ORDER_UPDATE_FLOW.md` |
| F6 | **Tenant / Staff App (POS & Ops)** | Live | High | `docs/staff-app/STAFF_APP_COMPLETE_FLOW.md`, `STAFF_APP_NOTIFICATIONS_FLOW.md` |
| F7 | **System Admin Application** | Live | Normal | `docs/DASH-ADMIN-AUDIT.md`, `docs/tech/features/sidebar/SIDEBAR_ARCHITECTURE.md` |
| F8 | **Public Web** | Live | Low | `index.md`, `docs/tech/features/design/*` |
| F9 | **Marketplaces** | In Staging | High | `docs/tech/features/marketplaces/FEAT-SYSTEM-MARKETPLACES.md`, `integrations/MARKETPLACE_SERVICE_OVERVIEW.md`, Jumpseller + UberEats subdocs |
| F10 | **Point of Sale (devices)** | Backlog | Normal | `docs/tech/features/point-of-sales/FEAT-SYSTEM-POINT-OF-SALES.md` |
| F11 | **Checkout Gateways** | In Staging | High | `docs/tech/features/checkout-gateways/FEAT-SYSTEM-CHECKOUT-GATEWAYS.md`, `FEAT-TRANSBANK-PST.md`, `FEAT-MERCADOPAGO.md`, `ML-CHECKOUT-PRO-DOCS.md`, `ML-WEBHOOKS.md` |
| F12 | **Billing, Subscriptions & Payments** | In Staging | High | `docs/tech/features/billing/SUBSCRIPTION_SYSTEM_COMPLETE_DOCUMENTATION.md` (+ billing/*), `docs/tech/features/payments/PAYMENT_GATEWAYS.md`, `FLOW_PAYMENT_GATEWAY.md`, `REBILL_PAYMENT_GATEWAY.md`, `docs/system/subscription_plans.md` |
| F13 | **Platform & Multi-Tenancy** | Live | High | `docs/tech/features/tenancy/*` (8 files) |
| F14 | **Auth & Access Control (ACL)** | Live | High | `docs/tech/features/permissions/*`, `docs/tech/features/acl/*` (incl. bulk-permission-manager/*) |
| F15 | **Notifications & Messaging** | Live | High | `docs/tech/features/notifications/*`, `docs/mall-app/06-NOTIFICATIONS.md`, `docs/tech/architecture/WS_MESSAGING.md`, `LARAVEL_WEBSOCKETS_README.md`, email/* |
| F16 | **AI Agents (Voice & Image)** | Mixed* | High | `docs/tech/features/ai/AI_AGENTS_DOCUMENTATION.md` |
| F17 | **Inventory (AI-assisted)** | Backlog | Normal | *(to author — recipes + invoice-image intake)* |
| F18 | **Campaigns** | Live | Low | `docs/tech/features/campaigns/CAMPAIGN_MANAGER_TECHNICAL_DOCUMENTATION.md`, `CampaignPublishingSystemTD.md` |
| F19 | **Internationalization (i18n)** | Live | Low | `docs/tech/features/i8ln/BACKEND_TRANSLATIONS.md`, `email/BACKEND_TRANSLATIONS.md` |
| F20 | **Media & Images** | Live | Low | `docs/tech/features/images/how-to-add-image-resource-to-model.md`, `TENANT_IMAGE_DRAG_DROP.md` |

\* **F16 AI** rollout is mixed — handled at the Feature/Story level (android voice+image = Live; iOS = Backlog; predictive agent = Backlog).

### Non-Functional epics

| # | Epic (Folder) | Start status | Priority | Mirror docs |
|---|---|---|---|---|
| N1 | **Backend Framework** | Live | High | `docs/AGENT.md`, `docs/tech/architecture/ARCHITECTURE.md`, `docs/tech/architecture/IMPLEMENTATION_SUMMARY.md`, `dash-backend-docker/docs/solution-architecture.md` |
| N2 | **Frontend Framework** | Live | High | `docs/tech/features/ui/COMPONENT_REGISTRY.md`, `docs/mall-app/07-FRONTEND-ARCHITECTURE.md`, `08-FRONTEND-COMPONENTS.md` |
| N3 | **Infrastructure & CI/CD** | Live | High | `docs/tech/deployment/*` (CI, CONFIG, AWS, LOCAL, LIGHTSAIL), `kitchntabs-ci-cdk/README.md` |
| N4 | **Build Toolchain (Electron/Python/Multi-arch)** | Live | Normal | `docs/tech/toolchain/*` |
| N5 | **Desktop & Device Service (Middleware Python)** | Mixed* | High | `docs/tech/toolchain/ELECTRON_PYTHON_SERVICE_BUILD_SYSTEM.md`, `dash-python-service/README.md` |
| N6 | **Caching & Performance** | Live | Normal | `docs/tech/features/cache/MALL_REACT_QUERY_CACHING_SYSTEM.md`, `docs/tech/domain-models/MALL_PRODUCTS_CACHE.md` |
| N7 | **Security** | Live | High | *(REQUIREMENTS.md §23.1 — author summary doc)* |
| N8 | **Observability** | Live | Normal | *(REQUIREMENTS.md §23.4 — author summary doc)* |
| N9 | **App Publishing (Stores)** | In Staging | Normal | *(Android internal preview; iOS pending)* |
| N10 | **Administrative & Legal (DTE/Billing entity)** | Backlog | High | *(estatuto, cuenta corriente, DTE manual + automática)* |

\* **N5** mixed: TTS / thermal printer / socket+IPC = Live; voice recognition desktop = In Dev; external POS device connectivity = Backlog.

---

## 3. Feature Lists & seed stories per Epic (examples)

> Full set generated at execution time from REQUIREMENTS.md FRs (→ Tasks) and NFRs (→ Tasks under N-epics). Representative seeds:

**F9 Marketplaces** (Folder) → Lists:
- `Marketplace Framework` — Task: system/tenant instances, OAuth, webhook ingestion, API tracking
- `Jumpseller` — Tasks: webhooks `Live`, publishing `Live`, unsubscribe `Live`, self-service checkout `Live`
- `Uber Eats` — Tasks: order ingestion `In Staging` (tag `cert-pending`), CREATED alarm flag `In Staging`
- `Pedidos Ya` — Task: integration `Backlog`
- `Rappi` — Task: integration `Backlog`

**F11 Checkout Gateways** → Lists:
- `Base Checkout Interface` — `Live`
- `DashTest demo provider` — `Live`
- `Transbank Webpay (kiosk/self-service)` — `In Staging` (tag `cert-pending`)
- `Mercado Pago (kiosk/self-service)` — `In Staging` (tag `cert-pending`)
- `checkout.kitchntabs.com Blade results` — `Backlog`

**F16 AI Agents** → Lists:
- `Voice Agent` — Tasks: desktop+android `Live`; iOS `Backlog`; phonetic-metadata optimization `Live`
- `Image Agent` — Tasks: android `Live`; iOS `Backlog`
- `Predictive Agent (insumos/demand/sales)` — `Backlog`

**N5 Desktop & Device Service** → Lists:
- `TTS / Audio` `Live` · `Thermal Printer` `Live` · `Socket + IPC bridge` `Live`
- `Voice recognition (desktop)` `In Dev`
- `External POS device connectivity (Transbank/MercadoPago/Sumup machines)` `Backlog`

**N3 Infrastructure & CI/CD** → Lists:
- `Local dev env` `Live` · `Backend CI (AWS CloudFormation, autoscale)` `Live`
- `Frontend CI (Cloudflare Pages)` `Live` (Tech Debt: free-tier CloudFront cost risk → tag `tech-debt`)

**N10 Administrative & Legal** → Lists:
- `Company statute update (financial products)` `Backlog`
- `Bank current account` `Backlog`
- `DTE / e-invoicing — manual` `Backlog` · `DTE / e-invoicing — automatic` `Backlog`

---

## 4. Execution order (when MCP tools are live)

1. Create the **status set** + **custom fields** + **tags** on space `90176181674`.
2. Create all **Epic Folders** (§2) with `Tipo` + priority + milestone tags.
3. For each Folder: create **Feature Lists** (§3) and **Story Tasks** with the correct starting **status** + **Notas → Tech Debt** field.
4. Break selected stories into **Subtasks** from REQUIREMENTS.md FRs/NFRs.
5. Create **ClickUp Docs**: mirror each mapped `docs/*.md`, attach/link to its Epic, set the `Doc` URL field.
6. Build space **views**: Board (by status), List (grouped by Epic), Priority backlog, and a "Rollout" board filtered to `In Staging`/`In Production` for release tracking.

## 5. Idempotency / re-run notes
- Match Folders/Lists/Tasks by name before creating to avoid duplicates on re-run.
- Doc mirror: update existing Doc page if a Doc with the same title already exists under the Epic.
- Spreadsheet remains the human-facing source; this space is the execution mirror.
