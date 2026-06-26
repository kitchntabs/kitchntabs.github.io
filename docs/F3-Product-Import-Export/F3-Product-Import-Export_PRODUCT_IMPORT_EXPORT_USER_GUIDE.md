# Product Import & Export — User Guide

This guide explains how to export your product catalog to Excel, edit it, and import it back into the system. No technical knowledge is required.

---

## Table of Contents

1. [Overview](#overview)
2. [Exporting Products](#exporting-products)
   - [Export All Products](#export-all-products)
   - [Export Selected Products](#export-selected-products)
   - [Export Modes](#export-modes)
3. [Understanding the Export File](#understanding-the-export-file)
   - [Columns Reference](#columns-reference)
   - [Price and Stock Columns](#price-and-stock-columns)
   - [Modifier Groups and Options](#modifier-groups-and-options)
   - [Campaign Columns](#campaign-columns)
4. [Editing the File](#editing-the-file)
5. [Importing Products](#importing-products)
   - [Import Options](#import-options)
6. [Common Use Cases](#common-use-cases)
7. [Tips and Warnings](#tips-and-warnings)

---

## Overview

The import/export system lets you manage your entire product catalog using Excel (`.xlsx`) files. This is useful for:

- **Bulk price updates** — change hundreds of prices at once
- **Bulk stock adjustments** — update stock levels across all products
- **Adding modifier groups and options** — define customisation menus (protein choice, toppings, etc.)
- **Onboarding a new catalog** — import products from a spreadsheet instead of adding them one by one
- **Migrating data** — export from one environment and import into another
- **Campaign management** — control which products appear in delivery platforms (Jumpseller, Uber Eats, etc.)

---

## Exporting Products

### Export All Products

1. Go to **Products** in the left menu.
2. Click the **Export** button in the toolbar (top right of the product list).
3. A dialog appears. Leave **All products** selected.
4. Choose the export mode (see [Export Modes](#export-modes) below).
5. Click **Export**.
6. When the file is ready, a notification appears with a download link. Click it to download the `.xlsx` file.

> For large catalogs (more than ~50 products) the export runs in the background. You will receive a notification when the file is ready — you do not need to keep the page open.

### Export Selected Products

1. In the product list, check the checkbox next to each product you want to export.
2. Click the **Export** button.
3. In the dialog, select **Productos seleccionados** (Selected products). The count of selected products is shown.
4. Choose the export mode and click **Export**.

### Export Modes

| Mode | Description | Best used for |
|------|-------------|---------------|
| **Normalized** | Single-sheet flat format with one row per product (and extra rows for modifier groups/options) | Editing, bulk updates, re-importing |
| **Detailed** | Multi-sheet format with comprehensive relational data | Reporting, data backup, analysis |
| **Standard** | Multi-sheet format with basic product data | General-purpose export |

> **Use Normalized mode** if you plan to edit the file and import it back. This is the only format supported for import.

---

## Understanding the Export File

Open the downloaded `.xlsx` file in Excel or LibreOffice Calc.

### Columns Reference

The first row is always the header. These columns are always present:

| Column | Description | Example |
|--------|-------------|---------|
| `sku` | Unique product code | `DVIE` |
| `name` | Product name | `Daily Viernes - Sushi` |
| `description` | Product description | `Roll de sushi (8 piezas)...` |
| `display_order` | Sort order (1 = first, empty = last) | `5` |
| `categories` | Category names, comma-separated | `Sushi, Ofertas` |
| `primary_category` | Main category name | `Sushi` |
| `category_ids` | Internal category IDs (do not edit) | `019ec939-...` |
| `brand_name` | Brand name | `PinoyWok` |
| `is_pack` | Is this a combo/pack product? | `Yes` / `No` |
| `is_enabled` | Is the product visible to customers? | `Yes` / `No` |
| `infinite_stock` | Never runs out of stock | `Yes` / `No` |
| `gallery_title` | Name of the product image gallery | `Daily Viernes` |
| `images` | Image URLs, comma-separated | `https://...` |

### Price and Stock Columns

After the base columns, you will see **dynamic price columns** (`price_*`) and **stock columns** (`stock_*`). These are named after your pricelists and stock types.

**Example price columns:**
| Column | Pricelist |
|--------|-----------|
| `price_local` | Local price list |
| `price_local_portugal` | Portugal price list |
| `price_jumpseller` | Jumpseller marketplace price |

**Example stock columns:**
| Column | Stock type |
|--------|------------|
| `stock_almacen` | Main warehouse stock |
| `stock_local` | In-store stock |

Leave a price or stock cell **empty** to leave it unchanged on import. Set it to `0` to explicitly set zero.

### Modifier Groups and Options

Modifier groups are customisation menus attached to a product (for example: "Choose your protein" or "Add toppings"). Each modifier group can have multiple selectable options (for example: Chicken, Shrimp, Tofu).

In the export file, modifier groups and their options appear as **extra rows below the product row**:

| sku | name | ... | modifier_group_name | modifier_group_type | modifier_option_name | modifier_option_price |
|-----|------|-----|---------------------|---------------------|----------------------|-----------------------|
| `DVIE` | `Daily Viernes - Sushi` | ... | `Opciones Daily Viernes` | `SINGLE` | | |
| | | ... | | | `Burger` | `500` |
| | | ... | | | `Tempura` | `1000` |
| | | ... | | | `Noru` | `-500` |
| | | ... | | | `California` | `0` |

**Rules:**
- The first row for a product contains the product data AND the first modifier group.
- Each option gets its own row directly below, with the product and group columns left empty.
- If a product has more than one modifier group, the second group appears on the next row after all the options for the first group, again with product columns empty.
- A product with no modifier groups has exactly one row.

**Modifier group columns:**

| Column | Description | Example |
|--------|-------------|---------|
| `modifier_group_name` | Name of the modifier group | `Opciones Daily Viernes` |
| `modifier_group_type` | `SINGLE` (choose one) or `MULTIPLE` (choose many) | `SINGLE` |
| `modifier_group_description` | Optional description | `Choose your protein` |
| `modifier_group_is_required` | Must the customer choose? | `Yes` / `No` |
| `modifier_group_min_selections` | Minimum choices required | `1` |
| `modifier_group_max_selections` | Maximum choices allowed | `1` |

**Modifier option columns:**

| Column | Description | Example |
|--------|-------------|---------|
| `modifier_option_name` | Option name | `Burger` |
| `modifier_option_description` | Optional description | |
| `modifier_option_price` | Price adjustment (can be negative) | `500` (add $500), `-500` (subtract $500), `0` (no change) |
| `modifier_option_is_default` | Pre-selected by default? | `Yes` / `No` |
| `modifier_option_display_order` | Sort order | `1`, `2`, `3`… |

### Campaign Columns

If you have active campaigns (Jumpseller, Uber Eats, etc.) you will see `campaign_*` columns after the stock columns. Each column shows the product's current status in that campaign.

| Column | Example values |
|--------|---------------|
| `campaign_jumpseller_products` | `PUBLISHED`, `PAUSED`, `FINISHED`, or empty |
| `campaign_uber_eats` | `PUBLISHED`, `PAUSED`, `FINISHED`, or empty |

You can edit these values in the file and re-import to bulk-update campaign product statuses. See [Import Options](#import-options) for details.

---

## Editing the File

> **Important:** Always use the file exported from the system as your starting point. Do not create a new Excel file from scratch.

**Safe to edit:**
- `name`, `description`, `display_order`
- `is_enabled`, `infinite_stock`, `is_pack`
- `brand_name`, `categories`, `primary_category`
- Any `price_*` column
- Any `stock_*` column
- `modifier_group_*` and `modifier_option_*` columns
- `campaign_*` columns (when re-importing with Campaign Sync enabled)
- `gallery_title`, `images`

**Do NOT edit:**
- `category_ids` — these are internal UUIDs used for lookup
- `sku` — changing a SKU changes which product is matched on import; only do this intentionally if creating new products
- Column headers (row 1)
- The row structure of modifier groups (empty cells in product columns on option rows must stay empty)

**Adding a new modifier option row:**
1. Insert a new row below the modifier group row or the last existing option for that group.
2. Leave all product columns and modifier group columns empty.
3. Fill in only the `modifier_option_*` columns.

**Adding a new modifier group to a product:**
1. After all options for the last existing group, insert a new row.
2. Leave the product columns empty.
3. Fill in the `modifier_group_*` columns.
4. Add option rows below.

---

## Importing Products

1. Go to **Products** in the left menu.
2. Click the **Import** button in the toolbar.
3. Click **Choose file** and select your `.xlsx` file.
4. Configure the import options (see below).
5. Click **Preview** to validate the file without making changes, or **Import** to apply changes immediately.
6. A notification will arrive when the import is complete, showing a summary of created, updated, and skipped products.

### Import Options

#### What to do with existing products

| Option | Description |
|--------|-------------|
| **Update existing products** | Products already in the system (matched by SKU) will be updated with the file data. Enable this for bulk updates. |
| **Create new products** | Products with SKUs not found in the system will be created. Enable this when onboarding a new catalog. |
| **Delete products not in file** | Products present in the system but absent from the import file will be soft-deleted. Use with caution — this is designed for full catalog replacement only. |
| **Skip invalid rows** | If a row has an error, skip it and continue instead of stopping the entire import. Recommended for large files. |

#### Categories and Brands

| Option | Description |
|--------|-------------|
| **Create missing categories** | If a category in the file doesn't exist, create it automatically. |
| **Create missing brands** | If a brand in the file doesn't exist, create it automatically. |

#### Images

| Option | Description |
|--------|-------------|
| **Preserve existing images** | Keep images already uploaded to the product. If disabled, existing images are removed before adding new ones from the file. |
| **Append new images** | Add image URLs from the file to the existing gallery without removing old images. |
| **Skip gallery processing** | Ignore all `gallery_title` and `images` columns — useful for price-only updates. |

#### Prices and Stock

| Option | Description |
|--------|-------------|
| **Create missing pricelists** | If a `price_*` column refers to a pricelist that doesn't exist, create it. |
| **Create missing stock types** | If a `stock_*` column refers to a stock type that doesn't exist, create it. |

#### Campaign Sync

| Option | Description |
|--------|-------------|
| **Sync campaigns** | Process `campaign_*` columns to update product statuses across marketplaces. Only affects products in **active (PUBLISHED)** campaigns. Valid target statuses: `PUBLISHED`, `PAUSED`, `FINISHED`. |

---

## Common Use Cases

### Bulk price update

1. Export all products in **Normalized** mode.
2. Open the file and edit the `price_*` columns.
3. Import with **Update existing** enabled and **Create new products** disabled.
4. Disable image processing to speed up the import.

### Add modifier options to existing products

1. Export the products you want to edit in **Normalized** mode.
2. Add option rows below the modifier group row for each product.
3. Import with **Update existing** enabled.

### Full catalog replacement

1. Prepare the complete catalog file in the normalized format.
2. Import with **Update existing**, **Create new products**, and **Delete products not in file** all enabled.
3. Use Preview mode first to verify before applying.

### Pause products on a campaign

1. Export all products (Normalized mode).
2. Find the `campaign_jumpseller_products` column (or similar).
3. Change the value to `PAUSED` for the products you want to pause.
4. Import with **Sync campaigns** enabled.

---

## Tips and Warnings

- **Preview before importing** — always run a preview for large files to catch errors before they affect live data.
- **Back up first** — export your current catalog before any bulk import that modifies or deletes existing data.
- **SKU is the key** — products are matched by their SKU. If you change a SKU, the import treats it as a new product (or fails to find the existing one).
- **Empty cells vs zero** — an empty price cell means "don't change this price". A `0` means "set this price to zero".
- **Modifier option price adjustments** — values can be negative. A `-500` means the option is $500 cheaper than the base product price.
- **Images are downloaded** — if you include external image URLs, the system downloads and stores them. Make sure the URLs are publicly accessible.
- **Campaign sync is additive** — an empty campaign cell does nothing. Only filled cells trigger a status change.
- **Do not change column headers** — the system reads columns by their exact header name. Renaming or deleting a header column will cause that data to be ignored.
