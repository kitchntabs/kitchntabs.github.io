---
layout: default
title: F2-Products-Catalog MODIFIER GROUPS FEATURE
---

MODIFIER GROUPS FEATURE

The modifier groups is an entity associated to Products, that will define price modifier rules for a specific product. 

A modifier group has options. e.g: "protein"
A modifier group options example: "chicken", "salmon", "tofu", "shrimp"
Each modifier option modifies the price of a product within an Order, depending the option selected by the user. 

A modifier group has types SINGLE, MULTIPLE
A modifier group option has the price value for the modification.

E.g:

ModifierGroupA : {
    "name" : "protein",
    "type": "SINGLE",
    "options": {
        "chicken": 1000,
        "shrimp": 2000,
        "tofu": -500,
        "salmon": 2000
    }
}

ModifierGroupB : {
    "name" : "extra",
    "type": "MULTIPLE",
    "options": {
        "egg": 700,
        "sauce": 500
    }
}


Modifier Groups Feature Implementation Plan
Here's a comprehensive plan for implementing the Modifier Groups feature for products in your restaurant ordering system:

1. Database Structure Implementation
Step 1: Create Migrations
First, let's create the necessary migrations for the modifier groups and options:

php artisan make:migration create_modifier_groups_table

Copy


Send command to Terminal
php artisan make:migration create_modifier_options_table

Copy


Send command to Terminal
php artisan make:migration create_product_modifier_groups_table

Copy


Send command to Terminal
php artisan make:migration create_order_product_modifiers_table

Copy


Send command to Terminal
Step 2: Define Migration Structures
A. Modifier Groups Migration
public function up()
{
    Schema::create('modifier_groups', function (Blueprint $table) {
        $table->id();
        $table->foreignId('tenant_id')->constrained('tenants');
        $table->string('name');
        $table->enum('type', ['SINGLE', 'MULTIPLE']);
        $table->text('description')->nullable();
        $table->boolean('is_required')->default(false);
        $table->integer('min_selections')->default(0);
        $table->integer('max_selections')->nullable();
        $table->timestamps();
        $table->softDeletes();
    });
}

Copy


xxxx_xx_xx_create_modifier_groups_table.php
B. Modifier Options Migration
public function up()
{
    Schema::create('modifier_options', function (Blueprint $table) {
        $table->id();
        $table->foreignId('modifier_group_id')->constrained('modifier_groups')->onDelete('cascade');
        $table->string('name');
        $table->decimal('price_adjustment', 10, 2);
        $table->text('description')->nullable();
        $table->boolean('is_default')->default(false);
        $table->integer('display_order')->default(0);
        $table->timestamps();
        $table->softDeletes();
    });
}

Copy


xxxx_xx_xx_create_modifier_options_table.php
C. Product Modifier Groups Pivot Migration
public function up()
{
    Schema::create('product_modifier_groups', function (Blueprint $table) {
        $table->id();
        $table->foreignId('product_id')->constrained('products')->onDelete('cascade');
        $table->foreignId('modifier_group_id')->constrained('modifier_groups')->onDelete('cascade');
        $table->integer('display_order')->default(0);
        $table->timestamps();
        
        $table->unique(['product_id', 'modifier_group_id']);
    });
}

Copy


xxxx_xx_xx_create_product_modifier_groups_table.php
D. Order Product Modifiers Migration
public function up()
{
    Schema::create('order_product_modifiers', function (Blueprint $table) {
        $table->id();
        $table->foreignId('order_product_id')->constrained('order_products')->onDelete('cascade');
        $table->foreignId('modifier_option_id')->constrained('modifier_options');
        $table->decimal('price_adjustment', 10, 2);
        $table->timestamps();
    });
}

Copy


xxxx_xx_xx_create_order_product_modifiers_table.php
2. Model Definitions
Step 3: Create Models
php artisan make:model ModifierGroup

Copy


Send command to Terminal
php artisan make:model ModifierOption

Copy


Send command to Terminal
php artisan make:model OrderProductModifier

Copy


Send command to Terminal
Step 4: Define Model Relationships
A. ModifierGroup Model
<?php

namespace Domain\App\Models;

use Domain\App\Models\ECommerce\Product;
use Domain\App\Models\ECommerce\Tenant;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class ModifierGroup extends Model
{
    use HasFactory, SoftDeletes;

    public const TYPE_SINGLE = 'SINGLE';
    public const TYPE_MULTIPLE = 'MULTIPLE';

    protected $fillable = [
        'tenant_id',
        'name',
        'type',
        'description',
        'is_required',
        'min_selections',
        'max_selections'
    ];

    /**
     * Get the tenant that owns the modifier group.
     */
    public function tenant()
    {
        return $this->belongsTo(Tenant::class);
    }

    /**
     * Get the options for the modifier group.
     */
    public function options()
    {
        return $this->hasMany(ModifierOption::class)->orderBy('display_order');
    }

    /**
     * Get the products that belong to the modifier group.
     */
    public function products()
    {
        return $this->belongsToMany(Product::class, 'product_modifier_groups')
            ->withPivot('display_order')
            ->withTimestamps();
    }
}

Copy


ModifierGroup.php
B. ModifierOption Model
<?php

namespace Domain\App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class ModifierOption extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'modifier_group_id',
        'name',
        'price_adjustment',
        'description',
        'is_default',
        'display_order'
    ];

    /**
     * Get the modifier group that owns the option.
     */
    public function modifierGroup()
    {
        return $this->belongsTo(ModifierGroup::class);
    }

    /**
     * Get the order product modifiers for this option.
     */
    public function orderProductModifiers()
    {
        return $this->hasMany(OrderProductModifier::class);
    }
}

Copy


ModifierOption.php
C. OrderProductModifier Model
<?php

namespace Domain\App\Models\Order;

use Domain\App\Models\ModifierOption;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class OrderProductModifier extends Model
{
    use HasFactory;

    protected $fillable = [
        'order_product_id',
        'modifier_option_id',
        'price_adjustment'
    ];

    /**
     * Get the order product that owns the modifier.
     */
    public function orderProduct()
    {
        return $this->belongsTo(OrderProduct::class);
    }

    /**
     * Get the modifier option for this order product modifier.
     */
    public function modifierOption()
    {
        return $this->belongsTo(ModifierOption::class);
    }
}

Copy


OrderProductModifier.php
Step 5: Update Existing Models
A. Update Product Model
// Add this relationship to the Product model

/**
 * Get the modifier groups for the product.
 */
public function modifierGroups()
{
    return $this->belongsToMany(ModifierGroup::class, 'product_modifier_groups')
        ->withPivot('display_order')
        ->withTimestamps()
        ->orderBy('pivot_display_order');
}

Copy


Product.php
B. Update OrderProduct Model
// Add this relationship to the OrderProduct model

/**
 * Get the modifiers for this order product.
 */
public function modifiers()
{
    return $this->hasMany(OrderProductModifier::class);
}

/**
 * Calculate the total price including modifiers.
 */
public function getTotalPriceAttribute()
{
    $basePrice = $this->unit_price * $this->quantity;
    $modifierAdjustments = $this->modifiers->sum('price_adjustment');
    
    return $basePrice + ($modifierAdjustments * $this->quantity);
}

Copy


OrderProduct.php
3. Controllers and Resources
Step 6: Create Controllers
php artisan make:controller  Domain/App/Http/Controllers/API/ECommerce/ModifierGroupController

Copy


Send command to Terminal
php artisan make:controller Domain/App/Http/Controllers/API/ECommerce/ModifierOptionController

Copy


Send command to Terminal
Step 7: Create Resources
php artisan make:resource ModifierGroups/ModifierGroupResource

Copy


Send command to Terminal
php artisan make:resource ModifierGroups/ModifierOptionResource

Copy


Send command to Terminal
php artisan make:resource ECommerce/OrderProductModifierResource

Copy


Send command to Terminal
Step 8: Implement Resources
A. ModifierGroupResource
<?php

namespace Domain\App\Http\Resources\ModifierGroups;

use Illuminate\Http\Resources\Json\JsonResource;

class ModifierGroupResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'tenant_id' => $this->tenant_id,
            'name' => $this->name,
            'type' => $this->type,
            'description' => $this->description,
            'is_required' => $this->is_required,
            'min_selections' => $this->min_selections,
            'max_selections' => $this->max_selections,
            'options' => $this->whenLoaded('options', fn() => ModifierOptionResource::collection($this->options)->resolve()),
            'products' => $this->whenLoaded('products', fn() => ProductResource::collection($this->products)->resolve()),
        ];
    }
}

Copy


ModifierGroupResource.php
B. ModifierOptionResource
<?php

namespace Domain\App\Http\Resources\ModifierGroups;

use Illuminate\Http\Resources\Json\JsonResource;

class ModifierOptionResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'modifier_group_id' => $this->modifier_group_id,
            'name' => $this->name,
            'price_adjustment' => $this->price_adjustment,
            'description' => $this->description,
            'is_default' => $this->is_default,
            'display_order' => $this->display_order,
        ];
    }
}

Copy


ModifierOptionResource.php
C. OrderProductModifierResource
<?php

namespace Domain\App\Http\Resources\ECommerce;

use Illuminate\Http\Resources\Json\JsonResource;
use Domain\App\Http\Resources\ModifierGroups\ModifierOptionResource;

class OrderProductModifierResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'order_product_id' => $this->order_product_id,
            'modifier_option_id' => $this->modifier_option_id,
            'price_adjustment' => $this->price_adjustment,
            'modifier_option' => $this->whenLoaded('modifierOption', fn() => ModifierOptionResource::make($this->modifierOption)->resolve()),
        ];
    }
}

OrderProductModifierResource.php
Step 9: Update Existing Resources

A. Update OrderProductResource
// Update the OrderProductResource to include modifiers

public function toArray($request)
{
    return [
        'id'                    => $this->id,
        'sku'                   => $this->sku,
        'name'                  => $this->name,
        'quantity'              => $this->pivot->quantity,
        'unit_price'            => $this->pivot->unit_price,
        'sale_fee'              => $this->pivot->sale_fee,
        'modifiers'             => $this->whenLoaded('modifiers', fn() => OrderProductModifierResource::collection($this->modifiers)->resolve()),
        'total_price'           => $this->total_price,
    ];
}

OrderProductResource.php

4. Controller Implementation
Step 10: Implement ModifierGroupController
<?php

namespace Domain\App\Http\Controllers\API\ModifierGroups;

use Domain\App\Models\ModifierGroup;
use App\Support\ResponseHandler;
use Domain\App\Http\Resources\ModifierGroups\ModifierGroupResource;
use App\Http\Controllers\API\System\ReactAdminBaseController;

class ModifierGroupController extends ReactAdminBaseController
{
    public $resource = 'modifier_group';
    
    public function __construct()
    {
        $this->model = ModifierGroup::query();
    }

    public function _preList($request)
    {
        $this->model
            ->visibleThroughTenant($request->user())
            ->with(['options']);
    }

    public function _postList($data)
    {
        return ModifierGroupResource::collection($data);
    }

    public function _postGetOne($item)
    {
        $item->load(['options', 'products']);
        return ModifierGroupResource::make($item);
    }

    public function _create($request)
    {
        $validated = $request->validate([
            'tenant_id' => 'required|exists:tenants,id',
            'name' => 'required|string|max:255',
            'type' => 'required|in:SINGLE,MULTIPLE',
            'description' => 'nullable|string',
            'is_required' => 'boolean',
            'min_selections' => 'integer|min:0',
            'max_selections' => 'nullable|integer|min:1',
            'options' => 'array',
            'options.*.name' => 'required|string|max:255',
            'options.*.price_adjustment' => 'required|numeric',
            'options.*.description' => 'nullable|string',
            'options.*.is_default' => 'boolean',
            'options.*.display_order' => 'integer',
        ]);

        $modifierGroup = ModifierGroup::create([
            'tenant_id' => $validated['tenant_id'],
            'name' => $validated['name'],
            'type' => $validated['type'],
            'description' => $validated['description'] ?? null,
            'is_required' => $validated['is_required'] ?? false,
            'min_selections' => $validated['min_selections'] ?? 0,
            'max_selections' => $validated['max_selections'] ?? null,
        ]);

        if (isset($validated['options'])) {
            foreach ($validated['options'] as $optionData) {
                $modifierGroup->options()->create($optionData);
            }
        }

        $modifierGroup->load('options');
        return ModifierGroupResource::make($modifierGroup);
    }

    public function _update($request, $id, $item)
    {
        $validated = $request->validate([
            'name' => 'string|max:255',
            'type' => 'in:SINGLE,MULTIPLE',
            'description' => 'nullable|string',
            'is_required' => 'boolean',
            'min_selections' => 'integer|min:0',
            'max_selections' => 'nullable|integer|min:1',
        ]);

        $item->update($validate

Copy


ModifierGroupController.php
continue



Context
— none fetched
4. Controller Implementation (continued)
Step 10: Implement ModifierGroupController (continued)
        $item->update($validated);

        $item->load('options');
        return ModifierGroupResource::make($item);
    }

    public function _delete($request, $id, $item)
    {
        // Check if the modifier group is in use by any orders
        $inUse = $item->options()
            ->whereHas('orderProductModifiers')
            ->exists();

        if ($inUse) {
            return ResponseHandler::error(
                new \Exception('Cannot delete modifier group that is in use by orders'),
                409
            );
        }

        $item->options()->delete();
        $item->delete();

        return ResponseHandler::json(['message' => 'Modifier group deleted successfully']);
    }

    public function attachToProduct($modifierGroupId, $productId)
    {
        $modifierGroup = ModifierGroup::findOrFail($modifierGroupId);
        $modifierGroup->products()->syncWithoutDetaching([$productId => ['display_order' => 0]]);
        
        return ResponseHandler::json(['message' => 'Modifier group attached to product successfully']);
    }

    public function detachFromProduct($modifierGroupId, $productId)
    {
        $modifierGroup = ModifierGroup::findOrFail($modifierGroupId);
        $modifierGroup->products()->detach($productId);
        
        return ResponseHandler::json(['message' => 'Modifier group detached from product successfully']);
    }
}

Copy


ModifierGroupController.php
Step 11: Implement ModifierOptionController
<?php

namespace Domain\App\Http\Controllers\API\ModifierGroups;

use Domain\App\Models\ModifierGroup;
use Domain\App\Models\ModifierOption;
use App\Support\ResponseHandler;
use Domain\App\Http\Resources\ModifierGroups\ModifierOptionResource;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class ModifierOptionController extends Controller
{
    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request, $modifierGroupId)
    {
        $modifierGroup = ModifierGroup::findOrFail($modifierGroupId);
        
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'price_adjustment' => 'required|numeric',
            'description' => 'nullable|string',
            'is_default' => 'boolean',
            'display_order' => 'integer',
        ]);

        $option = $modifierGroup->options()->create($validated);
        
        return ModifierOptionResource::make($option);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, $modifierGroupId, $optionId)
    {
        $option = ModifierOption::where('modifier_group_id', $modifierGroupId)
            ->where('id', $optionId)
            ->firstOrFail();
        
        $validated = $request->validate([
            'name' => 'string|max:255',
            'price_adjustment' => 'numeric',
            'description' => 'nullable|string',
            'is_default' => 'boolean',
            'display_order' => 'integer',
        ]);

        $option->update($validated);
        
        return ModifierOptionResource::make($option);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy($modifierGroupId, $optionId)
    {
        $option = ModifierOption::where('modifier_group_id', $modifierGroupId)
            ->where('id', $optionId)
            ->firstOrFail();
        
        // Check if the option is in use by any orders
        if ($option->orderProductModifiers()->exists()) {
            return ResponseHandler::error(
                new \Exception('Cannot delete modifier option that is in use by orders'),
                409
            );
        }
        
        $option->delete();
        
        return ResponseHandler::json(['message' => 'Modifier option deleted successfully']);
    }
}

Copy


ModifierOptionController.php
5. Update Order and Tab Controllers
Step 12: Update TabController to Handle Modifiers
// Update the handleOrderUpdate method to handle modifiers

private function handleOrderUpdate(Tab $tab, array $products, $currency_id, $pricelist_id)
{
    $order = $tab->order;

    // If order exists, delete existing items to replace with new ones
    $order->items()->delete();

    $totalAmount = 0;

    // Add products to order
    foreach ($products as $productId => $data) {
        $product = Product::with('prices')->findOrFail($productId);
        $quantity = $data['quantity'];
        $price = $product->prices->where('pricelist_id', $order->pricelist_id)->first()->price;
        
        // Create the order product
        $orderProduct = OrderProduct::create([
            'order_id' => $order->id,
            'product_id' => $product->id,
            'quantity' => $quantity,
            'unit_price' => $price,
            'itemable_type' => Tab::class,
            'itemable_id' => $tab->id
        ]);
        
        // Handle modifiers if they exist
        if (isset($data['modifiers']) && is_array($data['modifiers'])) {
            foreach ($data['modifiers'] as $modifierOptionId => $modifierData) {
                $modifierOption = ModifierOption::findOrFail($modifierOptionId);
                
                // Create the order product modifier
                $orderProduct->modifiers()->create([
                    'modifier_option_id' => $modifierOptionId,
                    'price_adjustment' => $modifierOption->price_adjustment
                ]);
            }
        }
        
        // Calculate subtotal including modifiers
        $modifierAdjustments = $orderProduct->modifiers->sum('price_adjustment');
        $subtotal = ($price + $modifierAdjustments) * $quantity;
        
        // Update the order product with the calculated subtotal
        $orderProduct->subtotal = $subtotal;
        $orderProduct->save();
        
        $totalAmount += $subtotal;
    }

    // Update order total
    $order->total_amount = $totalAmount;
    $order->save();
}

Copy


TabController.php
Step 13: Update OrderResource to Include Modifiers
// Update the OrderResource to include modifiers in the products

public function toArray($request)
{
    return [
        // ... existing fields
        'products' => $this->whenLoaded(
            'products',
            fn() => $this->products->count() > 0 ?
                OrderProductResource::collection($this->products->load('modifiers.modifierOption'))->resolve()
                : null
        ),
        // ... other fields
    ];
}

Copy


OrderResource.php
6. API Routes
Step 14: Define Routes for Modifier Groups
// Add these routes to your API routes file

// Modifier Groups
Route::prefix('modifier-groups')->group(function () {
    Route::get('/', [ModifierGroupController::class, 'index']);
    Route::post('/', [ModifierGroupController::class, 'store']);
    Route::get('/{id}', [ModifierGroupController::class, 'show']);
    Route::put('/{id}', [ModifierGroupController::class, 'update']);
    Route::delete('/{id}', [ModifierGroupController::class, 'destroy']);
    
    // Attach/detach from products
    Route::post('/{modifierGroupId}/products/{productId}', [ModifierGroupController::class, 'attachToProduct']);
    Route::delete('/{modifierGroupId}/products/{productId}', [ModifierGroupController::class, 'detachFromProduct']);
    
    // Modifier Options
    Route::post('/{modifierGroupId}/options', [ModifierOptionController::class, 'store']);
    Route::put('/{modifierGroupId}/options/{optionId}', [ModifierOptionController::class, 'update']);
    Route::delete('/{modifierGroupId}/options/{optionId}', [ModifierOptionController::class, 'destroy']);
});

Copy


api.php
7. Update Product Controller to Include Modifier Groups
Step 15: Update ProductController
// Update the _postGetOne method to include modifier groups

public function _postGetOne($item)
{
    $item->load([
        'category',
        'brand',
        'products',
        'gallery',
        'modifierGroups.options', // Add this line to load modifier groups with their options

        'prices' => function ($priceQuery) {
            $priceQuery->withWhereHas(
                'pricelist',
                fn($pricelistQuery) => $pricelistQuery->where('is_internal', false)->with('currency')
            );
        },
        'stocks' => function ($stockQuery) {
            $stockQuery->withWhereHas('stockType', fn($stockTypeQuery) => $stockTypeQuery->where('is_internal', false));
        },
    ]);

    $item->category
        ->append('breadcrumbed_name')
        ->unsetRelations();

    return ProductResource::make($item);
}

Copy


ProductController.php
Step 16: Update ProductResource
// Update the ProductResource to include modifier groups

public function toArray($request)
{
    $data = [
        // ... existing fields
        'modifier_groups' => $this->whenLoaded('modifierGroups', fn() => ModifierGroupResource::collection($this->modifierGroups)->resolve()),
        // ... other fields
    ];

    // Only include primary_image if gallery is loaded
    if ($this->relationLoaded('gallery')) {
        $data['primary_image'] = $this->primary_image;
    }

    return $data;
}

Copy


ProductResource.php
8. Testing the Implementation
Step 17: Create Database Seeders
php artisan make:seeder ModifierGroupsSeeder

Copy


Send command to Terminal
<?php

namespace Database\Seeders;

use Domain\App\Models\ModifierGroup;
use Domain\App\Models\ECommerce\Product;
use Illuminate\Database\Seeder;

class ModifierGroupsSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Create a protein modifier group
        $proteinGroup = ModifierGroup::create([
            'tenant_id' => 1, // Adjust based on your tenant setup
            'name' => 'Protein',
            'type' => ModifierGroup::TYPE_SINGLE,
            'description' => 'Choose your protein',
            'is_required' => true,
            'min_selections' => 1,
            'max_selections' => 1,
        ]);

        // Add options to the protein group
        $proteinGroup->options()->createMany([
            [
                'name' => 'Chicken',
                'price_adjustment' => 1000,
                'display_order' => 1,
                'is_default' => true,
            ],
            [
                'name' => 'Shrimp',
                'price_adjustment' => 2000,
                'display_order' => 2,
            ],
            [
                'name' => 'Tofu',
                'price_adjustment' => -500,
                'display_order' => 3,
            ],
            [
                'name' => 'Salmon',
                'price_adjustment' => 2000,
                'display_order' => 4,
            ],
        ]);

        // Create an extras modifier group
        $extrasGroup = ModifierGroup::create([
            'tenant_id' => 1, // Adjust based on your tenant setup
            'name' => 'Extras',
            'type' => ModifierGroup::TYPE_MULTIPLE,
            'description' => 'Add extras to your dish',
            'is_required' => false,
            'min_selections' => 0,
            'max_selections' => null,
        ]);

        // Add options to the extras group
        $extrasGroup->options()->createMany([
            [
                'name' => 'Egg',
                'price_adjustment' => 700,
                'display_order' => 1,
            ],
            [
                'name' => 'Sauce',
                'price_adjustment' => 500,
                'display_order' => 2,
            ],
        ]);

        // Attach modifier groups to some products
        $products = Product::take(5)->get();
        foreach ($products as $product) {
            $product->modifierGroups()->attach($proteinGroup->id, ['display_order' => 1]);
            $product->modifierGroups()->attach($extrasGroup->id, ['display_order' => 2]);
        }
    }
}

Copy


ModifierGroupsSeeder.php
Step 18: Run Migrations and Seeders
php artisan migrate

Copy


Send command to Terminal
php artisan db:seed --class=ModifierGroupsSeeder

Copy


Send command to Terminal
9. Frontend Integration (Optional)
For the frontend, you would need to:

Create components to display modifier groups and options when selecting products
Update order creation forms to include modifier selections
Show selected modifiers in order details
Calculate and display adjusted prices based on selected modifiers
Summary of Implementation Steps
Database Structure:

Created migrations for modifier_groups, modifier_options, product_modifier_groups, and order_product_modifiers tables
Models:

Created ModifierGroup, ModifierOption, and OrderProductModifier models
Updated Product and OrderProduct models with relationships
Resources:

Created ModifierGroupResource, ModifierOptionResource, and OrderProductModifierResource
Updated OrderProductResource and ProductResource
Controllers:

Implemented ModifierGroupController and ModifierOptionController
Updated TabController to handle modifiers in orders
Routes:

Added API routes for modifier groups and options
Testing:

Created seeders for testing the implementation
This implementation allows you to:

Define modifier groups with single or multiple selection options
Associate modifier groups with products
Apply price adjustments when ordering products with modifiers
Track selected modifiers in orders
Calculate total prices including modifiers
The system is flexible enough to handle various types of modifiers commonly used in restaurant ordering systems.


Command:
sail artisan migrate    
sail artisan db:seed --class=Domain\\Database\\Seeders\\ECommerce\\ModifierGroupsSeeder

Routes:
  GET|HEAD  api/ecommerce/modifier ............................................................................................. api.ecommerce.getList › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@getList
  POST      api/ecommerce/modifier ............................................................................................... api.ecommerce.create › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@create
  POST      api/ecommerce/modifier/deleteMany ............................................................................ api.ecommerce.deleteMany › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@deleteMany
  GET|HEAD  api/ecommerce/modifier/filter/{field} .................................................................... api.ecommerce.filterValues › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@filterValues
  GET|HEAD  api/ecommerce/modifier/filter/{field}/getMany .............................................................. api.ecommerce.filterValue › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@filterValue
  GET|HEAD  api/ecommerce/modifier/getMany ..................................................................................... api.ecommerce.getMany › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@getMany
  GET|HEAD  api/ecommerce/modifier/getManyReference .......................................................... api.ecommerce.getManyReference › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@getManyReference
  POST      api/ecommerce/modifier/updateMany ............................................................................ api.ecommerce.updateMany › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@updateMany
  PUT       api/ecommerce/modifier/{id} .......................................................................................... api.ecommerce.update › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@update
  GET|HEAD  api/ecommerce/modifier/{id} .......................................................................................... api.ecommerce.getOne › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@getOne
  DELETE    api/ecommerce/modifier/{id} .......................................................................................... api.ecommerce.delete › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@delete
  POST      api/ecommerce/modifier/{id}/delete ............................................................................... api.ecommerce.postDelete › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@delete
  POST      api/ecommerce/modifier/{id}/update ............................................................................... api.ecommerce.postUpdate › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@update
  POST      api/ecommerce/modifier/{modifierGroupId}/options ........................................................................... api.ecommerce. › Domain\App\Http\Controllers\API\ECommerce\ModifierOptionController@store
  PUT       api/ecommerce/modifier/{modifierGroupId}/options/{optionId} ............................................................... api.ecommerce. › Domain\App\Http\Controllers\API\ECommerce\ModifierOptionController@update
  DELETE    api/ecommerce/modifier/{modifierGroupId}/options/{optionId} .............................................................. api.ecommerce. › Domain\App\Http\Controllers\API\ECommerce\ModifierOptionController@destroy
  POST      api/ecommerce/modifier/{modifierGroupId}/products/{productId} ..................................................... api.ecommerce. › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@attachToProduct
  DELETE    api/ecommerce/modifier/{modifierGroupId}/products/{productId} ................................................... api.ecommerce. › Domain\App\Http\Controllers\API\ECommerce\ModifierGroupController@detachFromProduct


FRONTEND

Promt:

Take a look into ecommerceResource.tsx , it defines the resources to manage product related entities in the frontend, such as categories, galleries, etc. Examine the code for currecny, pricelist and gallery resources. pricelistResource.tsx , currencyResource.tsx , galleryResource.tsx. Each resource has a schema, which is the configuration for the attributes of the backend model. this are the schemas.gallery.tsx , pricelist.tsx , currencyResource.tsx 

I need you to guide me in the implementation of the frontend resources, schemas and components required, that will allow me to manage the application Mofifier Groups. Its important to highlight, that I need a similar association system that the one implemented in the gallery as you can see in the GalleryComponent.tsx.