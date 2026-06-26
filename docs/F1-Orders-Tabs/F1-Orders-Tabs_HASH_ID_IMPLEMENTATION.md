---
layout: default
title: F1-Orders-Tabs HASH ID IMPLEMENTATION
---

# Hash ID Implementation Guide

This document details the architecture and implementation steps for the 6-character alphanumeric Hash ID system used in this project. Using Hash IDs prevents exposing sequential primary keys in the API, improving security.

## 1. Architecture Overview

-   **Database**: Tables retain `id` (bigint) as the primary key for performance and internal relationships. A new `hash_id` (string, indexed) column is added for public reference.
-   **Model**: Models generate `hash_id` automatically on creation.
-   **API**: All API endpoints accept and return `hash_id`. The backend transparently converts between `hash_id` and `id`.
-   **Validation**: Custom traits ensure unique rules and foreign key checks resolve hashes correctly.

## 2. Core Components

### 2.1 Database Migration
Every table exposed via API must have a `hash_id` column.

```php
$table->string('hash_id', 20)->nullable()->unique()->index();
```

### 2.2 Model Trait: `HasHashId`
Located at `App\Traits\HasHashId`.
-   **Function**: Generates random 6-char string on `creating`.
-   **Route Binding**: Overrides `getRouteKeyName` to use `hash_id`.

### 2.3 Request Trait: `ResolvesHashId`
Located at `App\Traits\ResolvesHashId`.
-   **Function**: Helper methods to resolve numeric IDs for validation.

### 2.4 Global Filter: `RaFilter`
Located at `App\ModelFilters\RaFilter`.
-   **Function**: Handles `ids[]` and `tenant_id` parameters, checking if they are hashes and querying the `hash_id` column accordingly.

---

## 3. Step-by-Step Implementation for a New Resource

Follow these steps when creating or migrating a resource (e.g., `Product`).

### Step 1: Database Migration
Ensure the table has the `hash_id` column.

```php
public function up()
{
    Schema::create('products', function (Blueprint $table) {
        $table->id();
        $table->string('hash_id', 20)->nullable()->unique()->index();
        // ... other columns
    });
}
```

### Step 2: Model Configuration
Import and use the `HasHashId` trait.

```php
namespace App\Models;

use App\Traits\HasHashId;
use Illuminate\Database\Eloquent\Model;

class Product extends Model
{
    use HasHashId;
    
    // ...
}
```

### Step 3: API Resource (Response)
Ensure the `id` field returns the `hash_id`.

```php
class ProductResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->hash_id, // EXPOSE HASH ID
            'name' => $this->name,
            // ...
        ];
    }
}
```

### Step 4: Form Request (Validation)
Use `ResolvesHashId` to handle validation rules safely.

```php
use App\Traits\ResolvesHashId;

class ProductRequest extends FormRequest
{
    use ResolvesHashId;

    protected function prepareForValidation()
    {
        // Resolve Foreign Keys (e.g. category_id)
        if ($this->category_id && !is_numeric($this->category_id)) {
            $cat = \App\Models\Category::where('hash_id', $this->category_id)->first();
            $this->merge(['category_id' => $cat ? $cat->id : 0]);
        }
    }

    public function rules()
    {
        return [
            // Handle Unique Validation (Ignore Self)
            'code' => Rule::unique('products')->ignore($this->getNumericId(Product::class)),
            
            // Foreign Keys (now numeric due to prepareForValidation)
            'category_id' => 'required|exists:categories,id',
        ];
    }
}
```

### Step 5: Filters
**Do NOT** implement `ids()` or `tenantId()` methods in your specific ModelFilter (e.g., `ProductFilter`). The base `RaFilter` handles this globally.

```php
class ProductFilter extends ModelFilter
{
    // Only implement specific filters
    public function name($name) {
        return $this->whereLike('name', $name);
    }
    
    // NO ids() method!
    // NO tenantId() method!
}
```

### Step 6: Controller
Ensure your Controller creates/updates correctly. Avoid `app()->validated()` which might fail to capture request data.

```php
public function _create($request)
{
    // Use request->all() or specific attributes
    $item = $this->model->create($request->all());
    return ProductResource::make($item);
}
```

### Step 7: Testing
Verify functionality using `HashedResourceCrudTest`.

---

## 4. Troubleshooting Common Errors

### "invalid input syntax for type bigint" (500 Error)
-   **Cause**: A query is trying to compare a string (hash) to a numeric ID column.
-   **Fix**: 
    1.  Check Filters: ensure you don't have a specific `ids` or `tenantId` method overriding `RaFilter`.
    2.  Check Validation: ensure Foreign Keys are resolved in `prepareForValidation`.
    3.  Check Controller: ensure lookups use `findByIdOrHashId` or `where('hash_id', ...)`.

### "Not null violation" on Create
-   **Cause**: Data is being passed as empty to `create()`.
-   **Fix**: Check Controller `_create` method. Replace `$validated = app($this->requestValidator)->validated()` with `$validated = $request->all()`.

### "id: null" in API Response
-   **Cause**: Model does not have `hash_id` populated.
-   **Fix**: Ensure Model uses `HasHashId`. Run `php artisan hashid:backfill`.
