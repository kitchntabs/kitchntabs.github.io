# Delete Tenancy Account Command

## Overview

The `DeleteTenancyAccountCommand` is a comprehensive Laravel artisan command for permanently deleting tenancies and ALL their associated resources from the system. This command ensures complete data cleanup including related users, tenants, products, orders, billing records, media files, and all pivot table entries.

## Command Signature

```bash
sail artisan tenancy:delete {tenancy_id?} {--force} {--dry-run} {--all-except-seeded}
```

## Arguments & Options

| Argument/Option | Description |
|-----------------|-------------|
| `tenancy_id` | (Optional) Specific tenancy UUID to delete |
| `--force` | Skip confirmation prompts |
| `--dry-run` | Show what would be deleted without actually deleting |
| `--all-except-seeded` | Delete all tenancies except the seeded one (`019c04db-3820-7035-bfd8-2931c3e14ca2`) |

## Usage Examples

### Delete a specific tenancy
```bash
sail artisan tenancy:delete 019c1234-5678-90ab-cdef-1234567890ab
```

### Delete with force (no confirmation)
```bash
sail artisan tenancy:delete 019c1234-5678-90ab-cdef-1234567890ab --force
```

### Preview what would be deleted (dry-run)
```bash
sail artisan tenancy:delete 019c1234-5678-90ab-cdef-1234567890ab --dry-run
```

### Delete all tenancies except the seeded one
```bash
sail artisan tenancy:delete --all-except-seeded --force
```

## Protected Tenancy

The **seeded tenancy** is protected and will NEVER be deleted:
- **ID:** `019c04db-3820-7035-bfd8-2931c3e14ca2`

This protection is enforced by the `SEEDED_TENANCY_ID` constant in the command.

## Deletion Phases

The command executes a 12-phase deletion process within a database transaction:

### Phase 1: Delete Media Files
- Product images (via Spatie MediaLibrary)
- Gallery images
- Category images
- Uses `clearMediaCollection()` for proper file cleanup

### Phase 2: Delete Product-Related Records
- `product_prices` - Product pricing
- `product_stocks` - Inventory records
- `product_price_stocks` - Price-stock relations
- `order_products` - Order line items
- `product_modifier_groups` - Modifier associations
- `product_tenants` - Product multi-tenant pivot
- `product_categories` - Category assignments
- Products themselves (forceDelete for soft-deleted records)

### Phase 3: Delete Orders
- Orders (no SoftDeletes - uses `delete()`)

### Phase 4: Delete Tabs
- Tabs (no SoftDeletes - uses `delete()`)

### Phase 5: Delete Tenant Resources
- **Categories**: `category_tenants` pivot + Category records
- **Brands**: `brand_tenants` pivot + Brand records
- **Galleries**: `gallery_tenants` pivot + Gallery records
- **Pricelists**: `pricelist_tenants` pivot + Pricelist records
- **Campaigns**: `campaign_tenants` pivot + Campaign records
- **Stock Types**: `stock_type_tenants` pivot + StockType records
- **Point of Sales**: 
  - `point_of_sale_tenants` pivot
  - `output_pos_pricelist_mappings`
  - `output_pos_stock_type_mappings`
  - PointOfSale records (forceDelete)
- **Marketplaces**:
  - `marketplace_tenants` pivot
  - `output_category_mappings`
  - Marketplace records (forceDelete)
- **Product Templates**: `product_template_tenants` pivot + ProductTemplate records
- **Product Import Instances** (by tenancy_id)
- **Metadata Formats**: InputMetadataFormatMapping + MetadataFormat records
- **Input/Output Mappings**:
  - InputCategoryMapping
  - OutputCategoryMapping
  - InputBrandMapping
- **Currency**: `currency_tenant` pivot
- **System Marketplaces**: 
  - Delete PointOfSale records referencing tenant_system_point_of_sales
  - Delete Marketplace records referencing tenant_system_marketplaces
  - `tenant_system_marketplaces` pivot
  - `tenant_system_point_of_sales` pivot
- **Logs** (if tenant has logs relationship)
- **Schedules** (if tenant has schedules relationship)

### Phase 6: Delete Modifier Groups
- `modifier_group_tenants` pivot
- ModifierGroup records by `tenancy_id`
- ModifierGroup records by `tenant_id`

### Phase 7: Delete Users
- Users associated with each tenant (via `tenant_id`)
- **Must be deleted BEFORE tenants due to FK constraint**

### Phase 8: Delete Tenants
- Soft-deleted tenants (forceDelete)
- Active tenants

### Phase 9: Delete Billing Records
- Subscriptions
- PaymentMethods
- Payments

### Phase 10: Delete Data Exports
- DataExport records (by tenancy_id)

### Phase 11: Delete Pending Registrations
- PendingRegistration records (by `metadata->tenancy_id`)
- PendingRegistration records (by matching email)

### Phase 12: Delete Tenancy
- The tenancy record itself

## Tables Cleaned

### Core Tables
- `tenancies`
- `tenants`
- `users`

### Product-Related Tables
- `products`
- `product_prices`
- `product_stocks`
- `product_price_stocks`
- `product_tenants`
- `product_categories`
- `product_modifier_groups`

### Resource Tables
- `categories`, `category_tenants`
- `brands`, `brand_tenants`
- `galleries`, `gallery_tenants`
- `pricelists`, `pricelist_tenants`
- `campaigns`, `campaign_tenants`
- `stock_types`, `stock_type_tenants`
- `point_of_sales`, `point_of_sale_tenants`
- `marketplaces`, `marketplace_tenants`
- `product_templates`, `product_template_tenants`
- `product_import_instances`
- `metadata_formats`

### Mapping Tables
- `output_pos_pricelist_mappings`
- `output_pos_stock_type_mappings`
- `output_category_mappings`
- `input_category_mappings`
- `input_brand_mappings`
- `input_metadata_format_mappings`

### System Pivot Tables
- `tenant_system_marketplaces`
- `tenant_system_point_of_sales`
- `currency_tenant`

### Order Tables
- `orders`
- `order_products`
- `order_product_modifiers`
- `tabs`

### Modifier Tables
- `modifier_groups`
- `modifier_group_tenants`
- `modifier_options`

### Billing Tables
- `subscriptions`
- `payment_methods`
- `payments`

### Other Tables
- `data_exports`
- `pending_registrations`
- Media files (via Spatie MediaLibrary)

## Important Considerations

### Foreign Key Handling
The command handles complex FK relationships:
1. **Users → Tenants**: Users must be deleted before tenants
2. **Marketplaces → tenant_system_marketplaces**: Marketplaces reference system marketplaces via FK
3. **PointOfSales → tenant_system_point_of_sales**: POS records reference system POS via FK

The command fetches `tenant_system_*` IDs first, then deletes all records referencing them before deleting the pivots.

### SoftDeletes Handling
Models with SoftDeletes use `withTrashed()->forceDelete()`:
- Product, Category, Gallery, Brand, Pricelist, PointOfSale, StockType
- ProductTemplate, MetadataFormat, ModifierGroup, Tenant, User, Marketplace

Models WITHOUT SoftDeletes use `delete()`:
- Order, Tab, Campaign

### Transaction Safety
All deletions occur within a database transaction. If any phase fails, all changes are rolled back.

### Media Files
Uses Spatie MediaLibrary's `clearMediaCollection()` for proper file deletion from disk.

## Error Handling

The command catches exceptions and:
1. Rolls back the transaction
2. Logs the error
3. Reports which tenancy failed
4. Continues with remaining tenancies (in batch mode)
5. Shows summary at the end

## Output Example

```
Found 5 tenancies to delete (excluding seeded)

─────────────────────────────────────────
Processing Tenancy: 019c1234-5678-90ab-cdef-1234567890ab
  Name: TestTenancy1

Resources to delete:
  Users: 3
  Tenants: 1
  Products: 150
  Categories: 12
  Orders: 25
  ...

Deleting resources...
  Phase 1: Deleting media files...
  Phase 2: Deleting product-related records...
  Phase 3: Deleting orders...
  ...
  Phase 11: Deleting tenancy...
  ✓ All resources deleted
✓ Tenancy 019c1234-5678-90ab-cdef-1234567890ab deleted successfully!

═══════════════════════════════════════════
Summary: 5 deleted, 0 failed
```

## Related Services

- `TenancyAccountManagementService::initiateAccountDeletion()` - Soft-delete initiation
- `TenancyAccountManagementService::executeAccountDeletion()` - Full deletion execution
- `DeprovisionTenancyJob` - Async job for complete deletion

## File Location

```
app/Console/Commands/DeleteTenancyAccountCommand.php
```

## Changelog

- **2025-01-XX**: Initial implementation
- Fixed `product_categories` table name (was `category_product`)
- Fixed `currency_tenant` table name (was `currency_tenants`)
- Added `tenant_system_marketplaces` and `tenant_system_point_of_sales` pivot cleanup
- Fixed FK constraint: Delete users before tenants
- Fixed FK constraint: Delete by `tenant_system_*_id` before deleting pivots
- Fixed `product_modifier_groups` table name (was `modifier_group_product`)
- Added `output_category_mappings` deletion by `tenant_id`
- Added Phase 11: Delete `pending_registrations` by `metadata->tenancy_id` and email match
