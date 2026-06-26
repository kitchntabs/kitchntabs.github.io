
# Adding an Attribute to a Model in Dash Framework

This document describes the complete process of adding a new attribute to an existing model in the Dash framework, covering both backend (Laravel) and frontend (React) implementation.

## Overview

Adding a new attribute to a model requires changes in both the backend and frontend:

| Layer | Components to Modify |
|-------|---------------------|
| **Backend** | Migration, Model, Request, Resource |
| **Frontend** | Schema |

## Attribute Types

Common attribute types and their implementations:

| Type | Laravel Migration | Laravel Validation | React-Admin Type |
|------|-------------------|-------------------|------------------|
| **String** | `$table->string('field')` | `'required\|string\|max:256'` | `String` |
| **Boolean** | `$table->boolean('field')` | `'required\|boolean'` | `Boolean` |
| **Integer** | `$table->integer('field')` | `'required\|integer\|min:0'` | `Number` |
| **Decimal** | `$table->decimal('field', 10, 2)` | `'required\|numeric\|min:0'` | `Number` |
| **Text** | `$table->text('field')` | `'nullable\|string'` | `String` (multiline) |
| **Date** | `$table->date('field')` | `'required\|date'` | `Date` |
| **DateTime** | `$table->dateTime('field')` | `'required\|date'` | `Date` |
| **Enum** | `$table->enum('field', [...])` | `'required\|in:val1,val2'` | Custom Select |
| **JSON** | `$table->json('field')` | `'nullable\|array'` | Custom Component |
| **UUID (FK)** | `$table->uuid('field')` | `'required\|uuid\|exists:table,id'` | `ReferenceInput` |

---

## Backend Implementation

### 1. Database Migration

Create a migration to add the new column.

```bash
sail artisan make:migration add_field_name_to_table_name_table --table=table_name
```

#### Example: Adding a Boolean Field

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('your_table', function (Blueprint $table) {
            // Boolean with default value
            $table->boolean('is_internal')->default(false)->after('existing_column');
            
            // Add index if field will be queried frequently
            $table->index('is_internal');
        });
    }

    public function down(): void
    {
        Schema::table('your_table', function (Blueprint $table) {
            $table->dropIndex(['is_internal']);
            $table->dropColumn('is_internal');
        });
    }
};
```

#### Example: Adding a String Field

```php
Schema::table('your_table', function (Blueprint $table) {
    $table->string('code', 50)->nullable()->after('name');
    $table->unique('code'); // If unique constraint needed
});
```

#### Example: Adding a Foreign Key

```php
Schema::table('your_table', function (Blueprint $table) {
    $table->uuid('related_model_id')->nullable()->after('tenant_id');
    $table->foreign('related_model_id')
        ->references('id')
        ->on('related_models')
        ->onDelete('set null');
    $table->index('related_model_id');
});
```

Run the migration:
```bash
sail artisan migrate
```

### 2. Model Configuration

Add the new field to the model's `$fillable` array.

```php
<?php

namespace Domain\App\Models\YourModule;

use Illuminate\Database\Eloquent\Model;

class YourModel extends Model
{
    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        // ... existing fields
        'is_internal',  // Add new field
    ];

    /**
     * The attributes that should be cast.
     * (Optional - for type casting)
     */
    protected $casts = [
        'is_internal' => 'boolean',
        'settings' => 'array',      // For JSON fields
        'created_at' => 'datetime',
    ];
}
```

### 3. Request Validation

Add validation rules for the new field in your FormRequest class.

```php
<?php

namespace Domain\App\Http\Request\YourModule;

use Illuminate\Foundation\Http\FormRequest;

class YourModelRequest extends FormRequest
{
    /**
     * Prepare the data for validation.
     * (Required for boolean fields sent as strings from forms)
     */
    protected function prepareForValidation()
    {
        // Convert string 'true'/'false' to boolean for boolean fields
        if ($this->has('is_internal')) {
            $this->merge([
                'is_internal' => filter_var($this->is_internal, FILTER_VALIDATE_BOOLEAN),
            ]);
        }
    }

    public function rules()
    {
        return [
            // ... existing rules
            
            // Boolean field
            'is_internal' => 'sometimes|boolean',
            
            // Required string
            'code' => [
                'required',
                'string',
                'max:50',
                Rule::unique('your_table')->ignore($this->id),
            ],
            
            // Optional string
            'description' => 'nullable|string|max:1000',
            
            // Integer with range
            'priority' => 'required|integer|min:1|max:100',
            
            // Foreign key
            'related_model_id' => [
                'nullable',
                'uuid',
                Rule::exists('related_models', 'id')->withoutTrashed(),
            ],
        ];
    }
}
```

### 4. Resource (API Response)

Include the new field in your API resource.

```php
<?php

namespace Domain\App\Http\Resources\YourModule;

use Illuminate\Http\Resources\Json\JsonResource;

class YourModelResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id'          => $this->id,
            'name'        => $this->name,
            // ... existing fields
            
            // Add new field
            'is_internal' => $this->is_internal,
            
            // For relations (optional)
            'related_model' => $this->whenLoaded('relatedModel', 
                fn() => RelatedModelResource::make($this->relatedModel)
            ),
        ];
    }
}
```

---

## Frontend Implementation

### Update Schema

Add the new field to your schema definition.

**File:** `packages/kt-ecommerce/src/schemas/yourModel.ts`

```typescript
import { IDashAutoAdminAttribute } from "dash-auto-admin";

const yourModelSchema: IDashAutoAdminAttribute[] = [
  // ... existing fields

  // Boolean field
  {
    attribute: 'is_internal',
    label: 'Interno',
    type: Boolean
  },

  // String field
  {
    attribute: 'code',
    label: 'Código',
    type: String
  },

  // Number field
  {
    attribute: 'priority',
    label: 'Prioridad',
    type: Number
  },

  // Date field
  {
    attribute: 'created_at',
    label: 'Fecha de creación',
    type: Date,
    inCreate: false,  // Don't show in create form
    inEdit: false     // Don't show in edit form (read-only)
  },

  // Reference field (foreign key)
  {
    attribute: 'related_model_id',
    label: 'Modelo relacionado',
    type: 'your_module/related_model.id',  // Resource path + .id
    inList: false
  },

  // Custom visibility per view
  {
    attribute: 'internal_notes',
    label: 'Notas internas',
    type: String,
    inList: false,    // Hide in list view
    inShow: true,     // Show in detail view
    inCreate: true,   // Show in create form
    inEdit: true      // Show in edit form
  },
];

export default yourModelSchema;
```

---

## Schema Attribute Options

| Option | Type | Description |
|--------|------|-------------|
| `attribute` | `string` | Field name (must match API response) |
| `label` | `string` | Display label (can be translation key) |
| `type` | `String \| Boolean \| Number \| Date \| 'resource.id'` | Field type |
| `inList` | `boolean` | Show in list/grid view (default: `true`) |
| `inShow` | `boolean` | Show in detail view (default: `true`) |
| `inCreate` | `boolean` | Show in create form (default: `true`) |
| `inEdit` | `boolean` | Show in edit form (default: `true`) |
| `custom` | `boolean` | Use custom component |
| `component` | `React.FC` | Custom component for rendering |
| `tab` | `string` | Group in a specific tab |
| `required` | `boolean` | Mark as required in forms |
| `disabled` | `boolean` | Disable editing |
| `helperText` | `string` | Helper text below the field |

---

## Complete Example: Adding `is_internal` to Category

### 1. Migration

```php
// domain/database/migrations/2026_01_11_000001_add_is_internal_to_categories_table.php

<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('categories', function (Blueprint $table) {
            $table->boolean('is_internal')->default(false)->after('is_primary');
            $table->index('is_internal');
        });
    }

    public function down(): void
    {
        Schema::table('categories', function (Blueprint $table) {
            $table->dropIndex(['is_internal']);
            $table->dropColumn('is_internal');
        });
    }
};
```

### 2. Model

```php
// domain/app/Models/ECommerce/Category.php

protected $fillable = [
    'tenant_id',
    'category_id',
    'name',
    'image_path',
    'is_primary',
    'is_internal',  // Added
    'tree_index',
];
```

### 3. Request

```php
// domain/app/Http/Request/ECommerce/CategoryRequest.php

protected function prepareForValidation()
{
    if ($this->has('is_primary')) {
        $this->merge([
            'is_primary' => filter_var($this->is_primary, FILTER_VALIDATE_BOOLEAN),
        ]);
    }
    // Added
    if ($this->has('is_internal')) {
        $this->merge([
            'is_internal' => filter_var($this->is_internal, FILTER_VALIDATE_BOOLEAN),
        ]);
    }
}

public function rules()
{
    $rules = [
        // ... existing rules
        'is_primary' => 'required|boolean',
        'is_internal' => 'sometimes|boolean',  // Added
    ];
    return $rules;
}
```

### 4. Resource

```php
// domain/app/Http/Resources/ECommerce/CategoryResource.php

public function toArray($request)
{
    return [
        'id'          => $this->id,
        'name'        => $this->name,
        'is_primary'  => $this->is_primary,
        'is_internal' => $this->is_internal,  // Added
        // ... other fields
    ];
}
```

### 5. Schema

```typescript
// packages/kt-ecommerce/src/schemas/category.ts

{
  attribute: 'is_primary',
  label: 'Principal',
  type: Boolean
},

// Added
{
  attribute: 'is_internal',
  label: 'Interno',
  type: Boolean
},
```

---

## Checklist

### Backend
- [ ] Create migration with column and index (if needed)
- [ ] Run migration (`sail artisan migrate`)
- [ ] Add field to Model's `$fillable` array
- [ ] Add `$casts` entry if type casting needed
- [ ] Add validation rules to Request class
- [ ] Add `prepareForValidation()` for boolean fields
- [ ] Add field to Resource response

### Frontend
- [ ] Add field to schema with correct type
- [ ] Configure visibility (`inList`, `inEdit`, etc.)
- [ ] Add translation key for label (if using i18n)

---

## Common Patterns

### Boolean with Radio Buttons
```typescript
{
  attribute: 'is_active',
  label: 'Estado',
  type: Boolean,
  // Will render as checkbox by default
}
```

### Read-only Field
```typescript
{
  attribute: 'created_at',
  label: 'Fecha de creación',
  type: Date,
  inCreate: false,
  inEdit: false,
  inList: true,
  inShow: true
}
```

### Hidden in List, Visible in Forms
```typescript
{
  attribute: 'description',
  label: 'Descripción',
  type: String,
  inList: false,
  inCreate: true,
  inEdit: true
}
```

### Required Field with Helper Text
```typescript
{
  attribute: 'code',
  label: 'Código',
  type: String,
  required: true,
  helperText: 'Código único de identificación'
}
```

---

## Reference Implementations

- **Category.is_primary:** Boolean field example
- **Category.is_internal:** Boolean field with index
- **Product.price:** Decimal field
- **Order.status:** Enum field
- **Tab.tenant_id:** Foreign key reference
