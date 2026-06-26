# ClickUp Sync — Live State (resume map)

Space: **KitchnTabs Backlog** `901313868441` (workspace `90132880480`). Free plan: no tags, list cap ~40, **30 req/min** (pace bursts ≤25 with ~60s sleeps), no delete-list tool.

## Custom field IDs
- **Type** `0f8a0ea1-d861-463f-8d1d-7b08c84bc53a` → Functional `32740dde-2d82-4e29-985a-391d81f0645f` · NonFunctional `12ccd21b-96f6-4759-9a73-4e5cc97abd5c`
- **Environment** `8620aeaa-423c-4811-baad-769eda2067db` → Backlog `226d6808-6b2b-4c03-9366-4ec72f069f8f` · In Progress `7e5cc8db-0744-4fe2-9d62-434a31410a34` · Dev `fea2e181-6624-4589-a196-59d59e9c81ad` · Staging `a4e035ff-7204-4756-9c04-01cb35408c76` · Production `5046787c-cbdd-40cd-a534-672afafdc1a0` · Blocked `4f40419c-0aca-4f02-8c7c-c7f7aaa59b5f`
- **Theme** (labels) `3a8eaa67-0c03-4a6f-8945-8b899831bf77` → AI `03dddceb-351c-464b-aa54-f864adf3710c` · Payments `7ab65061-f67b-4e0f-9921-b2692d45b2de` · Marketplaces `73830753-0c96-46c6-bbff-f734330b7571` · Infra `fcecdde7-4254-4961-a83f-976718f3dd3b` · Mobile `87809763-c2ad-4aa3-8003-3e30c8134f09` · Desktop `0653874f-57e4-4a7e-8a5d-7bb54c5716f3` · Billing `e2e45b79-3de0-471a-a673-3ef4ef1bfd47` · Tech Debt `9b3a36b5-4838-441e-8ed1-8ddeb9875dae` · Cert Pending `6313d707-61a8-4d36-8421-82ec88ea8b68` · Backend `f921cffe-6f48-4e42-b078-522ea5cb5995` · Frontend `a8d16763-c626-4c9b-84e6-33b4953ecc5e` · Middleware `8779aa0f-dd2f-44f1-90c0-4d7f38bc832b` · SystemApp `7aba3f80-360f-4172-82ff-a138679a385b` · WebApp `74c214e8-1241-4b1b-b8ef-2f874838e5b4` · StaffApp `0562de18-2f97-4de3-9bc9-f41f76d2c602` · MallApp `e185917a-d58e-49b6-ae47-f91c75261968`

Theme label value format in create_task custom_fields: JSON array string, e.g. `"[\"<uuid>\"]"`.

## Epic folder + list IDs, and task status
| # | Epic | folder_id | list_id | tasks |
|---|------|-----------|---------|-------|
| 1 | Orders & Tabs | 901318507102 | 901327678646 | ✅ 6 |
| 2 | Products & Catalog | 901318507103 | 901327678647 | ✅ 4 |
| 3 | Product Import / Export | 901318507104 | 901327678648 | ✅ 2 |
| 4 | Mall / Food Court | 901318507105 | 901327678650 | ⬜ |
| 5 | Customer & Self-Service | 901318507106 | 901327678651 | ⬜ |
| 6 | Tenant / Staff App | 901318507107 | 901327678652 | ⬜ |
| 7 | System Admin Application | 901318507108 | 901327678653 | ⬜ |
| 8 | Public Web | 901318507109 | 901327678654 | ⬜ |
| 9 | Marketplaces | 901318507110 | 901327678655 | ⬜ |
| 10 | Point of Sale (Devices) | 901318507111 | 901327678656 | ⬜ |
| 11 | Checkout Gateways | 901318507112 | 901327678657 | ⬜ |
| 12 | Billing, Subscriptions & Payments | 901318507113 | 901327678658 | ⬜ |
| 13 | Platform & Multi-Tenancy | 901318507114 | 901327678659 | ⬜ |
| 14 | Auth & Access Control (ACL) | 901318507115 | 901327678660 | ⬜ |
| 15 | Notifications & Messaging | 901318507116 | 901327678662 | ⬜ |
| 16 | AI Agents (Voice & Image) | 901318507117 | 901327678663 | ⬜ |
| 17 | Inventory (AI-assisted) | 901318507118 | 901327678664 | ⬜ |
| 18 | Campaigns | 901318507119 | 901327678665 | ⬜ |
| 19 | Internationalization (i18n) | 901318507120 | 901327678673 | ⬜ |
| 20 | Media & Images | 901318507121 | 901327678674 | ⬜ |
| 21 | Backend Framework | 901318507122 | 901327678675 | ⬜ |
| 22 | Frontend Framework | 901318507123 | 901327678676 | ⬜ |
| 23 | Infrastructure & CI/CD | 901318507124 | 901327678677 | ⬜ |
| 24 | Build Toolchain | 901318507125 | 901327678678 | ⬜ |
| 25 | Desktop & Device Service (Python) | 901318507452 | 901327678679 | ⬜ |
| 26 | Caching & Performance | 901318507453 | 901327678680 | ⬜ |
| 27 | Security | 901318507454 | 901327678681 | ⬜ |
| 28 | Observability | 901318507455 | 901327678682 | ⬜ |
| 29 | App Publishing (Stores) | 901318507456 | 901327678683 | ⬜ |
| 30 | Administrative & Legal | 901318507457 | 901327678684 | ⬜ |

Remaining: tasks for epics 4–30, then master public Doc with nested pages (one per docs/*.md), then index.
