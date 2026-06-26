---
title: Documentation Reorganization Summary
layout: default
---

# Documentation Reorganization to ClickUp Epic Structure

## Overview

The KitchnTabs documentation has been reorganized to align with the **35-epic structure** created in ClickUp (25 Functional + 10 Non-Functional). This ensures the documentation repository serves as the **source of truth** that mirrors your product roadmap.

---

## What Changed

### 1. ✅ Local Docs Folder Structure (Completed)

**Before:** Mixed folder structure (mall-app/, customer-app/, staff-app/, tech/features/*, etc.)

**After:** Epic-based organization with 35 folders:
```
docs/
├── F1-Orders-Tabs/          (6 files)
├── F2-Products-Catalog/     (3 files)
├── F3-Product-Import-Export/ (2 files)
├── F4-Mall-Food-Court/      (16 files)
├── F5-Customer-Self-Service/ (8 files)
├── F6-Tenant-Staff-App/     (3 files)
├── F7-System-Admin-Application/ (6 files)
├── ... (F8-F25 and N1-N10)
└── Archive/                 (4 files)
```

### 2. ✅ File Naming Convention (Completed)

**Before:** Generic filenames (Tab-README.md, Order-README.md, etc.)

**After:** Epic-prefixed filenames with single dashes:
```
F1-Orders-Tabs_Tab-README.md
F1-Orders-Tabs_Order-README.md
F1-Orders-Tabs_HASH_ID_IMPLEMENTATION.md
(no double dashes -- anywhere)
```

### 3. ✅ Jekyll Site Navigation (Completed)

Updated the Jekyll documentation site to reflect epic-based organization:

- **index.md** → Reorganized by epic groupings (F1-F25, N1-N10)
- **EPIC_INDEX.md** → New master index for all 35 epics with descriptions
- **INDEX.md** → Complete table of contents (all 195+ documents)
- **README.md** → Updated quick links to reference epics

### 4. 🔄 Navigation System (Ready)

The existing `generate-nav.py` script automatically scans the folder structure and generates sidebar navigation. Works with the new epic-based organization.

---

## Directory Structure Details

### Functional Epics (F1–F25)

| Epic | Folder | Files | Description |
|---|---|---|---|
| F1 | F1-Orders-Tabs | 6 | Order management, tabs, delivery |
| F2 | F2-Products-Catalog | 3 | Product domain, modifiers, pricing |
| F3 | F3-Product-Import-Export | 2 | Bulk import/export, validation |
| F4 | F4-Mall-Food-Court | 16 | Food court, multi-store, sessions |
| F5 | F5-Customer-Self-Service | 8 | Customer app, tracking, notifications |
| F6 | F6-Tenant-Staff-App | 3 | Staff workflows, real-time updates |
| F7 | F7-System-Admin-Application | 6 | Admin dashboard, user management |
| F8 | F8-Public-Web | 3 | Public site, design system |
| F9 | F9-Marketplaces | 10 | Jumpseller, Uber Eats, integrations |
| F10 | F10-Point-of-Sale | 1 | POS integration |
| F11 | F11-Checkout-Gateways | 7 | Payment processors, webhooks |
| F12 | F12-Billing-Subscriptions-Payments | 21 | Subscriptions, invoicing, payments |
| F13 | F13-Platform-Multi-Tenancy | 8 | Multi-tenancy, tenant scoping |
| F14 | F14-Auth-Access-Control | 23 | RBAC, permissions, security |
| F15 | F15-Notifications-Messaging | 16 | Email, SMS, push notifications |
| F16 | F16-AI-Agents | 1 | AI/ML capabilities |
| F17 | F17-Inventory | 0 | Stock management (ready for docs) |
| F18 | F18-Campaigns | 5 | Marketing campaigns, promotions |
| F19 | F19-Internationalization | 5 | i18n, translations, localization |
| F20 | F20-Media-Images | 3 | Image management, CDN |
| F21 | F21-Tenancy-Management | 2 | Tenant lifecycle, provisioning |
| F22 | F22-MiddlewareService | 0 | Middleware, cross-cutting (ready) |
| F23 | F23-DeliveryModule | 1 | Delivery tracking |
| F24 | F24-InventoryModule | 0 | Advanced inventory (ready) |
| F25 | F25-CashcountModule | 0 | Cash handling (ready) |

### Non-Functional Epics (N1–N10)

| Epic | Folder | Files | Description |
|---|---|---|---|
| N1 | N1-Backend-Framework | 7 | Laravel, DDD patterns, architecture |
| N2 | N2-Frontend-Framework | 1 | React, design system, components |
| N3 | N3-Infrastructure-CICD | 8 | CI/CD, deployment, AWS |
| N4 | N4-Build-Toolchain | 8 | Build system, Electron, webpack |
| N5 | N5-Desktop-Device-Service | 5 | Electron, Python IPC, hardware |
| N6 | N6-Caching-Performance | 2 | Redis, performance optimization |
| N7 | N7-Security | 0 | Security practices (ready) |
| N8 | N8-Observability | 1 | Logging, monitoring, CloudWatch |
| N9 | N9-App-Publishing | 0 | App store publishing (ready) |
| N10 | N10-Administrative-Legal | 9 | Settings, utilities, compliance |

---

## Statistics

```
Total Epics:           35 (25 Functional + 10 Non-Functional)
Total Documents:       195+
Documented Epics:      25 (with 1+ files)
Ready-to-Document:     10 (with 0 files, ready for future content)
Archive:               4 files

Folder Structure:      Epic-based (F1-F25, N1-N10)
File Naming:           {EPIC_CODE}_{original_filename}.md
Dash Conversion:       All -- converted to single -
```

---

## Navigation & Linking

### Index Files

1. **index.md** — Homepage with epic quick links (recommended entry point)
2. **EPIC_INDEX.md** — Master epic index with all 35 epics described
3. **INDEX.md** — Complete document table of contents
4. **SITEMAP.md** — Full site structure

### How Users Navigate

1. **By Epic** → Visit [EPIC_INDEX.md](EPIC_INDEX.md) and click epic of interest
2. **By Topic** → Use [index.md](/) for functional/non-functional groupings
3. **By Document** → Use [INDEX.md](INDEX.md) for complete list with descriptions
4. **Via Sidebar** → Auto-generated by `generate-nav.py` from folder structure

---

## Synchronization with ClickUp

The documentation now mirrors the ClickUp workspace:

| ClickUp Element | Docs Element | Notes |
|---|---|---|
| 35 Epic Folders | 35 Epic Directories | F1-F25 Functional, N1-N10 Non-Functional |
| Epic Names | Folder Names | Exact matching for discoverability |
| Lists (Tasks) | Files in Folders | Each file = document or reference |
| Documentation | ClickUp Pages | Sync'd separately via ClickUp MCP |

---

## File Organization Rules

### Naming Convention
- Format: `{EPIC_CODE}_{FILENAME}.md`
- Single dashes only (no double dashes --)
- Underscores separate epic code from filename

### Examples
```
✅ F1-Orders-Tabs_Tab-README.md
✅ F4-Mall-Food-Court_NOTIFICATIONS.md
✅ N1-Backend-Framework_ARCHITECTURE.md
❌ F1-Orders--Tabs_Tab-README.md (double dash in epic)
❌ F1_Tab_README.md (missing epic name)
```

### Folder Organization
- One folder per epic
- Files within organized by topic (no subfolders)
- Archive folder for deprecated docs

---

## Future Maintenance

### Adding New Documentation

When adding docs to an epic:

1. Create file in appropriate epic folder:
   ```bash
   docs/F{N}-{Epic-Name}/{EPIC_CODE}_{filename}.md
   ```

2. Update epic folder's index (if created)

3. Run navigation generator:
   ```bash
   python3 generate-nav.py --update
   ```

4. Commit changes:
   ```bash
   git add docs/ _layouts/default.html
   git commit -m "docs: add {title} to {epic} epic"
   git push origin main
   ```

### Creating New Epic Documentation

If you need to document an empty epic (e.g., F17, F22, F24, F25):

1. Create folder: `docs/F{N}-{Epic-Name}/`
2. Add first document with epic prefix
3. Update indices (index.md, EPIC_INDEX.md)
4. Run `generate-nav.py --update`

---

## Benefits

✅ **Alignment** — Docs mirror ClickUp product roadmap  
✅ **Discoverability** — Clear epic organization  
✅ **Scalability** — Ready for 35 epics of documentation  
✅ **Consistency** — Single naming/folder convention  
✅ **Sync'd** — ClickUp pages link back to docs  
✅ **Source of Truth** — Repository is authoritative  

---

## Related Documents

- [EPIC_INDEX.md](EPIC_INDEX.md) — Master index of all 35 epics
- [INDEX.md](INDEX.md) — Complete table of contents (all files)
- [generate-nav.py](generate-nav.py) — Auto-navigation generator
- [DOCS_TO_CLICKUP_MAPPING.md](/DOCS_TO_CLICKUP_MAPPING.md) — File-to-epic mapping

---

<div class="footer-section">
  <p>Documentation reorganized to align with ClickUp 35-epic structure</p>
  <p>© 2025 KitchnTabs. All rights reserved.</p>
</div>
