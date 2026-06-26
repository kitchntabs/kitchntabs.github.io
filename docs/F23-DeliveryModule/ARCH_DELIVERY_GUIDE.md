---
layout: default
title: ARCH DELIVERY GUIDE
---

Migration Guide: PinoyWok Delivery System to Dash Framework
Based on the codebase you've shared, I'll guide you through migrating the PinoyWok delivery system to your existing Dash architecture. Since you mentioned you already have messaging, Order, and Product models, we'll focus on extending those while adding the delivery tracking functionality.

Step 1: Database Schema Extensions
First, let's extend your database schema to support the delivery tracking functionality:

sail artisan make:dash-module Delivery TrackingOrder --force

Copy
Execute

Create Additional Migrations
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('delivery_tracking_status', function (Blueprint $table) {
            $table->id();
            $table->foreignId('order_id')->constrained('orders');
            $table->string('status'); // paid, assigned, withdrawed, delivered
            $table->timestamp('status_timestamp');
            $table->json('meta_data')->nullable();
            $table->timestamps();
            
            // Index for faster lookups
            $table->index(['order_id', 'status']);
        });
    }

    public function down()
    {
        Schema::dropIfExists('delivery_tracking_status');
    }
};

Copy


YYYY_MM_DD_create_delivery_tracking_status_table.php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('delivery_drivers', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('phone');
            $table->boolean('active')->default(true);
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('delivery_drivers');
    }
};

Copy


YYYY_MM_DD_create_delivery_drivers_table.php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->string('tracking_number')->nullable()->after('id');
            $table->string('tracking_url')->nullable();
            $table->string('delivery_status')->default('pending');
            $table->foreignId('driver_id')->nullable()->constrained('delivery_drivers');
            $table->integer('preparation_time')->nullable();
            $table->timestamp('withdraw_time')->nullable();
            $table->json('delivery_coordinates')->nullable();
            $table->string('verification_code')->nullable();
        });
    }

    public function down()
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->dropColumn([
                'tracking_number',
                'tracking_url',
                'delivery_status',
                'driver_id',
                'preparation_time',
                'withdraw_time',
                'delivery_coordinates',
                'verification_code'
            ]);
        });
    }
};

Copy


YYYY_MM_DD_add_delivery_fields_to_orders_table.php
Step 2: Create Model Classes
Extend Order Model
<?php

namespace Domain\App\Models;

use Domain\App\Models\Delivery\Driver;
use Domain\App\Models\Delivery\TrackingStatus;
use EloquentFilter\Filterable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Rennokki\QueryCache\Traits\QueryCacheable;

class Order extends Model
{
    use HasFactory, Filterable, QueryCacheable;

    protected $fillable = [
        // existing fields
        'tracking_number',
        'tracking_url',
        'delivery_status',
        'driver_id',
        'preparation_time',
        'withdraw_time',
        'delivery_coordinates',
        'verification_code'
    ];

    protected $casts = [
        'delivery_coordinates' => 'array',
        'withdraw_time' => 'datetime',
    ];

    // Relationship to driver
    public function driver()
    {
        return $this->belongsTo(Driver::class);
    }

    // Relationship to tracking statuses
    public function trackingStatuses()
    {
        return $this->hasMany(TrackingStatus::class);
    }

    // Calculate preparation time based on order items
    public function calculatePreparationTime()
    {
        $totalQuantity = $this->items()->sum('quantity');
        
        if ($totalQuantity < 4) {
            return 25; // Minimum 25 minutes
        }
        
        $extraMinutes = floor(($totalQuantity - 4) / 5) * 5;
        return 25 + $extraMinutes;
    }

    // Generate a tracking code
    public function generateTrackingCode()
    {
        return substr(base64_encode($this->id), 0, 4);
    }

    // Verify a tracking code
    public function verifyTrackingCode($code)
    {
        return $this->generateTrackingCode() === $code;
    }
}

Copy


Order.php
Create Driver Model
<?php

namespace Domain\App\Models\Delivery;

use Domain\App\Models\Order;
use EloquentFilter\Filterable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Rennokki\QueryCache\Traits\QueryCacheable;

class Driver extends Model
{
    use HasFactory, Filterable, QueryCacheable;

    protected $table = 'delivery_drivers';

    protected $fillable = [
        'name',
        'phone',
        'active'
    ];

    protected $casts = [
        'active' => 'boolean'
    ];

    // Relationship to orders
    public function orders()
    {
        return $this->hasMany(Order::class);
    }

    // Get active orders for this driver
    public function activeOrders()
    {
        return $this->orders()
            ->whereIn('delivery_status', ['assigned', 'withdrawed'])
            ->orderBy('withdraw_time');
    }
}

Copy


Driver.php
Create TrackingStatus Model
<?php

namespace Domain\App\Models\Delivery;

use Domain\App\Models\Order;
use EloquentFilter\Filterable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Rennokki\QueryCache\Traits\QueryCacheable;

class TrackingStatus extends Model
{
    use HasFactory, Filterable, QueryCacheable;

    protected $table = 'delivery_tracking_status';

    protected $fillable = [
        'order_id',
        'status',
        'status_timestamp',
        'meta_data'
    ];

    protected $casts = [
        'status_timestamp' => 'datetime',
        'meta_data' => 'array'
    ];

    // Relationship to order
    public function order()
    {
        return $this->belongsTo(Order::class);
    }
}

Copy


TrackingStatus.php
Step 3: Create Controllers
Driver Controller
<?php

namespace Domain\App\Http\Controllers\API\Delivery\Driver;

use Domain\App\Models\Delivery\Driver;
use App\Http\Controllers\API\Admin\ReactAdminBaseController;

class DriverController extends ReactAdminBaseController
{
    public $resource = 'driver';
    public $requestValidator = DriverRequest::class;
    public $modelFilter = DriverFilter::class;
    public $policy = DriverPolicy::class;

    public function __construct()
    {
        $this->model = Driver::query();
    }
}

Copy


DriverController.php
TrackingOrder Controller
<?php

namespace Domain\App\Http\Controllers\API\Delivery\TrackingOrder;

use Domain\App\Models\Order;
use Domain\App\Models\Delivery\TrackingStatus;
use Illuminate\Http\Request;
use App\Http\Controllers\API\Admin\ReactAdminBaseController;
use Domain\App\Services\GoogleMapsService;

class TrackingOrderController extends ReactAdminBaseController
{
    public $resource = 'tracking-order';
    public $requestValidator = TrackingOrderRequest::class;
    public $modelFilter = TrackingOrderFilter::class;
    public $policy = TrackingOrderPolicy::class;

    public function __construct()
    {
        $this->model = Order::query();
    }

    // Generate tracking page URL for a specific order
    public function getTrackingUrl(Order $order)
    {
        return response()->json([
            'tracking_url' => config('app.tracking_url') . '/' . $order->id
        ]);
    }

    // Public tracking page that doesn't require authentication
    public function publicTracking($id)
    {
        $order = Order::findOrFail($id);
        
        // Return view data for the tracking page
        return response()->json([
            'order' => new TrackingOrderResource($order),
            'statuses' => $order->trackingStatuses()->orderBy('status_timestamp', 'desc')->get()
        ]);
    }

    // Update order status (for driver app)
    public function updateStatus(Request $request, $id)
    {
        $order = Order::findOrFail($id);
        
        // Verify tracking code
        if (!$order->verifyTrackingCode($request->code)) {
            return response()->json(['message' => 'Invalid verification code'], 403);
        }
        
        $newStatus = $request->status;
        $validStatuses = ['assigned', 'withdrawed', 'delivered'];
        
        if (!in_array($newStatus, $validStatuses)) {
            return response()->json(['message' => 'Invalid status'], 400);
        }
        
        // Create new status record
        $trackingStatus = new TrackingStatus([
            'order_id' => $order->id,
            'status' => $newStatus,
            'status_timestamp' => now(),
            'meta_data' => $request->meta_data
        ]);
        $trackingStatus->save();
        
        // Update order
        $order->delivery_status = $newStatus;
        if ($newStatus === 'withdrawed') {
            $order->withdraw_time = now();
        }
        $order->save();
        
        // Trigger notifications via your existing messaging system
        // event(new OrderStatusUpdated($order, $newStatus));
        
        return response()->json([
            'message' => 'Status updated successfully',
            'order' => new TrackingOrderResource($order)
        ]);
    }

    // Assign driver to order
    public function assignDriver(Request $request, $id)
    {
        $order = Order::findOrFail($id);
        $driverId = $request->driver_id;
        
        $order->driver_id = $driverId;
        $order->delivery_status = 'assigned';
        $order->save();
        
        // Create tracking status
        $trackingStatus = new TrackingStatus([
            'order_id' => $order->id,
            'status' => 'assigned',
            'status_timestamp' => now(),
            'meta_data' => ['driver_id' => $driverId]
        ]);
        $trackingStatus->save();
        
        // Generate verification code
        $order->verification_code = $order->generateTrackingCode();
        $order->save();
        
        // event(new DriverAssigned($order));
        
        return response()->json([
            'message' => 'Driver assigned successfully',
            'verification_code' => $order->verification_code
        ]);
    }

    // Geocode address using Google Maps
    public function geocodeAddress(Request $request, GoogleMapsService $mapsService)
    {
        $address = $request->address;
        $coordinates = $mapsService->geocodeAddress($address);
        
        return response()->json($coordinates);
    }
}

Copy


TrackingOrderController.php
Supporting Files for TrackingOrderController
<?php

namespace Domain\App\Http\Controllers\API\Delivery\TrackingOrder;

use Illuminate\Foundation\Http\FormRequest;

class TrackingOrderRequest extends FormRequest
{
    public function rules()
    {
        return [
            'status' => 'sometimes|required|string|in:paid,assigned,withdrawed,delivered',
            'driver_id' => 'sometimes|required|exists:delivery_drivers,id',
            'code' => 'sometimes|required|string',
            'meta_data' => 'sometimes|array'
        ];
    }

    public function validated($key = null, $default = null)
    {
        return parent::validated($key, $default);
    }
}

Copy


TrackingOrderRequest.php
<?php

namespace Domain\App\Http\Controllers\API\Delivery\TrackingOrder;

use Illuminate\Http\Resources\Json\JsonResource;

class TrackingOrderResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'tracking_number' => $this->tracking_number,
            'tracking_url' => $this->tracking_url,
            'status' => $this->delivery_status,
            'preparation_time' => $this->preparation_time,
            'withdraw_time' => $this->withdraw_time,
            'coordinates' => $this->delivery_coordinates,
            'driver' => $this->driver ? [
                'id' => $this->driver->id,
                'name' => $this->driver->name,
                'phone' => $this->driver->phone
            ] : null,
            'customer' => [
                'name' => $this->customer_name,
                'email' => $this->customer_email,
                'phone' => $this->customer_phone
            ],
            'shipping_address' => [
                'address' => $this->shipping_address,
                'city' => $this->shipping_city,
                'state' => $this->shipping_state,
                'zip' => $this->shipping_zip
            ],
            'tracking_history' => $this->trackingStatuses()
                ->orderBy('status_timestamp', 'desc')
                ->get()
                ->map(function($status) {
                    return [
                        'status' => $status->status,
                        'timestamp' => $status->status_timestamp->format('Y-m-d H:i:s')
                    ];
                })
        ];
    }
}

Copy


TrackingOrderResource.php
Step 4: Create Routes
<?php

use Illuminate\Support\Facades\Route;
use Domain\App\Http\Controllers\API\Delivery\Driver\DriverController;
use Domain\App\Http\Controllers\API\Delivery\TrackingOrder\TrackingOrderController;

// Authenticated routes
Route::group(['middleware' => ['auth:sanctum'], 'as' => 'delivery.', 'prefix' => 'delivery'], function () {
    // Driver routes
    Route::prefix('driver')->name('driver.')->group(function () {
        Route::get('forSelect/{url?}', [DriverController::class, 'getForSelect'])->name('getForSelect');
        Route::apiResource('', DriverController::class)->parameters(['' => 'driver']);
    });
    
    // TrackingOrder routes
    Route::prefix('tracking-order')->name('tracking-order.')->group(function () {
        Route::get('forSelect/{url?}', [TrackingOrderController::class, 'getForSelect'])->name('getForSelect');
        Route::post('{id}/assign-driver', [TrackingOrderController::class, 'assignDriver'])->name('assign-driver');
        Route::get('{order}/tracking-url', [TrackingOrderController::class, 'getTrackingUrl'])->name('tracking-url');
        Route::post('geocode-address', [TrackingOrderController::class, 'geocodeAddress'])->name('geocode-address');
        Route::apiResource('', TrackingOrderController::class)->parameters(['' => 'tracking-order']);
    });
});

// Public routes (no authentication required)
Route::prefix('tracking')->name('tracking.')->group(function () {
    Route::get('{id}', [TrackingOrderController::class, 'publicTracking'])->name('public');
    Route::post('{id}/update', [TrackingOrderController::class, 'updateStatus'])->name('update-status');
});

Copy


delivery.php
Step 5: Create Service for Google Maps Integration
<?php

namespace Domain\App\Services;

use Illuminate\Support\Facades\Http;

class GoogleMapsService
{
    protected $apiKey;
    
    public function __construct()
    {
        $this->apiKey = config('services.google.maps_api_key');
    }
    
    public function geocodeAddress($address)
    {
        $response = Http::get('https://maps.googleapis.com/maps/api/geocode/json', [
            'address' => $address,
            'key' => $this->apiKey
        ]);
        
        $data = $response->json();
        
        if ($response->successful() && isset($data['results'][0]['geometry']['location'])) {
            return [
                'lat' => $data['results'][0]['geometry']['location']['lat'],
                'lng' => $data['results'][0]['geometry']['location']['lng'],
                'formatted_address' => $data['results'][0]['formatted_address']
            ];
        }
        
        return null;
    }
    
    public function getDirections($origin, $destination)
    {
        $response = Http::get('https://maps.googleapis.com/maps/api/directions/json', [
            'origin' => $origin,
            'destination' => $destination,
            'key' => $this->apiKey
        ]);
        
        return $response->json();
    }
}

Copy


GoogleMapsService.php
Step 6: Setup Events and Notifications
<?php

namespace Domain\App\Events;

use Domain\App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderStatusUpdated implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public $order;
    public $status;

    public function __construct(Order $order, $status)
    {
        $this->order = $order;
        $this->status = $status;
    }

    public function broadcastOn()
    {
        return new PrivateChannel('orders.'.$this->order->id);
    }
    
    public function broadcastAs()
    {
        return 'status.updated';
    }
    
    public function broadcastWith()
    {
        return [
            'order_id' => $this->order->id,
            'status' => $this->status,
            'timestamp' => now()->toIso8601String()
        ];
    }
}

Copy


OrderStatusUpdated.php
<?php

namespace Domain\App\Notifications;

use Domain\App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

class OrderStatusChanged extends Notification implements ShouldQueue
{
    use Queueable;

    protected $order;
    protected $status;

    public function __construct(Order $order, $status)
    {
        $this->order = $order;
        $this->status = $status;
    }

    public function via($notifiable)
    {
        return ['mail', 'database'];
    }

    public function toMail($notifiable)
    {
        $statusMessages = [
            'paid' => 'Your order has been confirmed',
            'assigned' => 'Your order has been assigned to a driver',
            'withdrawed' => 'Your order has been picked up by the driver',
            'delivered' => 'Your order has been delivered'
        ];
        
        $message = $statusMessages[$this->status] ?? 'Your order status has been updated';
        
        return (new MailMessage)
            ->subject('Order Status Update: ' . $message)
            ->line('Order #' . $this->order->id)
            ->line($message)
            ->action('Track Your Order', url($this->order->tracking_url))
            ->line('Thank you for choosing PinoyWok!');
    }

    public function toArray($notifiable)
    {
        return [
            'order_id' => $this->order->id,
            'status' => $this->status,
            'timestamp' => now()->toIso8601String()
        ];
    }
}

Copy


OrderStatusChanged.php
Step 7: Create Frontend Components (React)
Now let's set up the frontend components for the Dash Admin interface:

Driver Resource
import { ResourceTemplate } from "dash-admin";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import React from "react";

const DriverSchema = [
    {
        tab: 'Driver Details',
        attribute: 'name',
        label: 'Name',
        type: String,
        visible: {
            list: true,
            show: true,
            create: true,
            edit: true
        }
    },
    {
        tab: 'Driver Details',
        attribute: 'phone',
        label: 'Phone Number',
        type: String,
        visible: {
            list: true,
            show: true,
            create: true,
            edit: true
        }
    },
    {
        tab: 'Driver Details',
        attribute: 'active',
        label: 'Active',
        type: Boolean,
        visible: {
            list: true,
            show: true,
            create: true,
            edit: true
        }
    }
];

const DriverResource = {
    roles: ["admin", "manager"],
    component: ResourceTemplate,
    model: "delivery/driver",
    label: "Drivers",
    schema: DriverSchema,
    icon: <LocalShippingIcon />,
    group: "Delivery",
    
    menu: [
        {
            title: "All Drivers",
            redirect: "/delivery/driver",
        }
    ],

    mainAction: {
        title: "Add Driver",
        mode: "create",
        fn: "virtualhash",
        redirect: "inline/create",
    },

    view: true,
    create: true,
    edit: true,
    delete: true,
  
    drawer: true,
    drawerOptions: {
        create: true,
        edit: true,
        view: true
    },
};

export default DriverResource;

Copy


DriverResource.tsx
TrackingOrder Resource
import { ResourceTemplate } from "dash-admin";
import TrackChangesIcon from "@mui/icons-material/TrackChanges";
import React from "react";
import OrderMapView from "../components/delivery/OrderMapView";
import TrackingUrlButton from "../components/delivery/TrackingUrlButton";
import AssignDriverButton from "../components/delivery/AssignDriverButton";
import OrderStatusChip from "../components/delivery/OrderStatusChip";

// Define the schema for the tracking order resource
const TrackingOrderSchema = [
    {
        tab: 'Order Details',
        attribute: 'id',
        label: 'Order ID',
        type: Number,
        visible: {
            list: true,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Order Details',
        attribute: 'tracking_number',
        label: 'Tracking Number',
        type: String,
        visible: {
            list: true,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Order Details',
        attribute: 'delivery_status',
        label: 'Status',
        type: String,
        component: OrderStatusChip,
        visible: {
            list: true,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Order Details',
        attribute: 'preparation_time',
        label: 'Prep Time (mins)',
        type: Number,
        visible: {
            list: true,
            show: true,
            create: false,
            edit: true
        }
    },
    {
        tab: 'Order Details',
        attribute: 'withdraw_time',
        label: 'Pickup Time',
        type: Date,
        visible: {
            list: false,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Customer Info',
        attribute: 'customer.name',
        label: 'Customer Name',
        type: String,
        visible: {
            list: true,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Customer Info',
        attribute: 'customer.email',
        label: 'Customer Email',
        type: String,
        visible: {
            list: false,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Customer Info',
        attribute: 'customer.phone',
        label: 'Customer Phone',
        type: String,
        visible: {
            list: false,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Customer Info',
        attribute: 'shipping_address.address',
        label: 'Shipping Address',
        type: String,
        visible: {
            list: false,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Map',
        attribute: 'map_view',
        label: 'Delivery Map',
        component: OrderMapView,
        type: undefined,
        visible: {
            list: false,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Driver',
        attribute: 'driver.name',
        label: 'Driver Name',
        type: String,
        visible: {
            list: true,
            show: true,
            create: false,
            edit: false
        }
    },
    {
        tab: 'Driver',
        attribute: 'driver.phone',
        label: 'Driver Phone',
        type: String,
        visible: {
            list: false,
            show: true,
            create: false,
            edit: false
        }
    }
];

const TrackingOrderResource = {
    roles: ["admin", "manager"],
    component: ResourceTemplate,
    model: "delivery/tracking-order",
    label: "Delivery Tracking",
    schema: TrackingOrderSchema,
    icon: <TrackChangesIcon />,
    group: "Delivery",
    
    menu: [
        {
            title: "All Orders",
            redirect: "/delivery/tracking-order",
        },
        {
            title: "Pending Assignment",
            redirect: "/delivery/tracking-order?filter={\"delivery_status\":\"paid\"}",
        },
        {
            title: "In Delivery",
            redirect: "/delivery/tracking-order?filter={\"delivery_status\":[\"assigned\",\"withdrawed\"]}",
        },
        {
            title: "Delivered",
            redirect: "/delivery/tracking-order?filter={\"delivery_status\":\"delivered\"}",
        }
    ],

    mainAction: {
        title: "View Map Dashboard",
        fn: "custom",
        action: () => {
            window.location.href = '/delivery/dashboard';
        }
    },

    view: true,
    create: false,
    edit: true,
    delete: false,
  
    drawer: true,
    drawerOptions: {
        view: true,
        edit: true
    },
    
    // Add custom buttons
    listViewButton: {
        enabled: true
    },
    
    listEditButton: {
        enabled: true
    },
    
    listActions: [
        {
            component: TrackingUrlButton,
            props: {
                label: "Tracking URL"
            }
        },
        {
            component: AssignDriverButton,
            props: {
                label: "Assign Driver"
            }
        }
    ]
};

export default TrackingOrderResource;

Copy


TrackingOrderResource.tsx
Add Custom Components
import React from 'react';
import { Chip } from '@mui/material';
import { IDashAutoAdminCustomFieldComponent } from 'dash-auto-admin';

const statusColors = {
    paid: 'info',
    assigned: 'warning',
    withdrawed: 'primary',
    delivered: 'success',
    default: 'default'
};

const OrderStatusChip: React.FC<IDashAutoAdminCustomFieldComponent> = ({ 
    record, 
    attribute 
}) => {
    if (!record) return null;
    
    const status = record.delivery_status || 'default';
    const color = statusColors[status] || statusColors.default;
    
    const getStatusLabel = (status: string) => {
        switch(status) {
            case 'paid': return 'Paid';
            case 'assigned': return 'Assigned';
            case 'withdrawed': return 'In Transit';
            case 'delivered': return 'Delivered';
            default: return 'Unknown';
        }
    };
    
    return (
        <Chip 
            label={getStatusLabel(status)} 
            color={color as any} 
            size="small"
            variant="outlined"
        />
    );
};

export default OrderStatusChip;

Copy


OrderStatusChip.tsx
import React, { useEffect, useRef, useState } from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { useRecordContext } from 'react-admin';
import { IDashAutoAdminCustomFieldComponent } from 'dash-auto-admin';
import { Loader } from '@googlemaps/js-api-loader';

const OrderMapView: React.FC<IDashAutoAdminCustomFieldComponent> = () => {
    const record = useRecordContext();
    const mapRef = useRef<HTMLDivElement>(null);
    const [mapLoaded, setMapLoaded] = useState(false);
    
    useEffect(() => {
        if (!record?.coordinates?.lat || !record?.coordinates?.lng) return;
        
        const loader = new Loader({
            apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
            version: 'weekly',
        });
        
        loader.load().then(() => {
            setMapLoaded(true);
            
            if (!mapRef.current || !window.google) return;
            
            const restaurantLocation = { lat: -33.43949, lng: -70.6179356 }; // PinoyWok location
            const deliveryLocation = { 
                lat: record.coordinates.lat, 
                lng: record.coordinates.lng 
            };
            
            const map = new window.google.maps.Map(mapRef.current, {
                center: deliveryLocation,
                zoom: 14,
            });
            
            // Restaurant marker
            new window.google.maps.Marker({
                position: restaurantLocation,
                map,
                title: 'PinoyWok Restaurant',
                icon: {
                    url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                }
            });
            
            // Delivery location marker
            new window.google.maps.Marker({
                position: deliveryLocation,
                map,
                title: 'Delivery Address'
            });
            
            // Draw route
            const directionsService = new window.google.maps.DirectionsService();
            const directionsRenderer = new window.google.maps.DirectionsRenderer({
                map
            });
            
            directionsService.route({
                origin: restaurantLocation,
                destination: deliveryLocation,
                travelMode: window.google.maps.TravelMode.DRIVING
            }, (response, status) => {
                if (status === 'OK') {
                    directionsRenderer.setDirections(response);
                    
                    const route = response?.routes[0];
                    if (route && route.legs && route.legs[0]) {
                        const leg = route.legs[0];
                        const distanceText = document.getElementById('distance-text');
                        if (distanceText) {
                            distanceText.textContent = `Distance: ${leg.distance?.text}, Duration: ${leg.duration?.text}`;
                        }
                    }
                }
            });
        });
    }, [record]);
    
    if (!record || !record.coordinates) {
        return <Typography>No location data available</Typography>;
    }
    
    return (
```jsx
        <Box sx={{ width: '100%', height: '100%', p: 2 }}>
            <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
                <Typography id="distance-text" variant="body1">
                    Loading route information...
                </Typography>
            </Paper>
            <Box 
                ref={mapRef} 
```
                ref={mapRef} 
                sx={{ 
                    width: '100%', 
                    height: 400, 
                    borderRadius: 1,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}
            >
                {!mapLoaded && <Typography>Loading map...</Typography>}
            </Box>
        </Box>
    );
};

export default OrderMapView;

Copy


OrderMapView.tsx
import React, { useState } from 'react';
import { 
    Button, 
    Dialog, 
    DialogTitle, 
    DialogContent, 
    DialogActions, 
    TextField, 
    IconButton,
    Typography,
    Box
} from '@mui/material';
import { useRecordContext, useDataProvider, useNotify } from 'react-admin

Copy


TrackingUrlButton.tsx
continue 


Context
— none fetched

Thought Process
Let me continue with the custom components for the frontend, specifically for the delivery tracking system. I need to complete the TrackingUrlButton and add a few more components like the AssignDriverButton.

import React, { useState } from 'react';
import { 
    Button, 
    Dialog, 
    DialogTitle, 
    DialogContent, 
    DialogActions, 
    TextField, 
    IconButton,
    Typography,
    Box
} from '@mui/material';
import { useRecordContext, useDataProvider, useNotify } from 'react-admin';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import TrackChangesIcon from '@mui/icons-material/TrackChanges';

const TrackingUrlButton = () => {
    const record = useRecordContext();
    const [open, setOpen] = useState(false);
    const [trackingUrl, setTrackingUrl] = useState('');
    const dataProvider = useDataProvider();
    const notify = useNotify();

    const handleClick = async () => {
        if (!record || !record.id) return;
        
        try {
            const { data } = await dataProvider.getOne(
                'delivery/tracking-order/tracking-url',
                { id: record.id }
            );
            
            setTrackingUrl(data.tracking_url);
            setOpen(true);
        } catch (error) {
            notify('Error fetching tracking URL', { type: 'error' });
        }
    };
    
    const handleClose = () => {
        setOpen(false);
    };
    
    const handleCopy = () => {
        navigator.clipboard.writeText(trackingUrl);
        notify('Tracking URL copied to clipboard', { type: 'success' });
    };

    return (
        <>
            <Button
                onClick={handleClick}
                startIcon={<TrackChangesIcon />}
                size="small"
            >
                Tracking URL
            </Button>
            
            <Dialog open={open} onClose={handleClose} maxWidth="md">
                <DialogTitle>Order Tracking URL</DialogTitle>
                <DialogContent>
```jsx
                    <Typography variant="body2" sx={{ mb: 2 }}>
                        Share this link with the customer to track their order:
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <TextField
                            fullWidth
                            value={trackingUrl}
```
                            value={trackingUrl}
                            InputProps={{
                                readOnly: true,
                            }}
                            variant="outlined"
                            size="small"
                        />
```jsx
                        <IconButton onClick={handleCopy} sx={{ ml: 1 }}>
                            <ContentCopyIcon />
                        </IconButton>
                    </Box>
                    
                    <Typography variant="caption" color="textSecondary">
                        The tracking page will show real-time updates of the order status.
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Close</Button>
                </DialogActions>
            </Dialog>
        </>
    );
```
    );
};

export default TrackingUrlButton;

Copy


TrackingUrlButton.tsx
import React, { useState, useEffect } from 'react';
import {
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Typography,
    Box,
    Chip
} from '@mui/material';
import { useRecordContext, useDataProvider, useNotify, useRefresh } from 'react-admin';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';

const AssignDriverButton = () => {
    const record = useRecordContext();
    const [open, setOpen] = useState(false);
    const [drivers, setDrivers] = useState([]);
    const [selectedDriver, setSelectedDriver] = useState('');
    const [loading, setLoading] = useState(false);
    const [verificationCode, setVerificationCode] = useState('');
    const dataProvider = useDataProvider();
    const notify = useNotify();
    const refresh = useRefresh();

    // Only show for orders with 'paid' status
    if (record?.delivery_status !== 'paid') {
        return null;
    }

    useEffect(() => {
        if (open) {
            loadDrivers();
        }
    }, [open]);

    const loadDrivers = async () => {
        try {
            const { data } = await dataProvider.getList(
                'delivery/driver',
                {
                    pagination: { page: 1, perPage: 50 },
                    sort: { field: 'name', order: 'ASC' },
                    filter: { active: true }
                }
            );
            
            setDrivers(data);
        } catch (error) {
            notify('Error loading drivers', { type: 'error' });
        }
    };

    const handleClick = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
        setSelectedDriver('');
        setVerificationCode('');
    };

    const handleAssign = async () => {
        if (!record || !record.id || !selectedDriver) return;
        
        setLoading(true);
        
        try {
            const { data } = await dataProvider.create(
                'delivery/tracking-order/assign-driver',
                {
                    id: record.id,
                    data: { driver_id: selectedDriver }
                }
            );
            
            setVerificationCode(data.verification_code);
            notify('Driver assigned successfully', { type: 'success' });
            refresh();
        } catch (error) {
            notify('Error assigning driver', { type: 'error' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <Button
                onClick={handleClick}
                startIcon={<AssignmentIndIcon />}
                size="small"
            >
                Assign Driver
            </Button>
            
            <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
                <DialogTitle>Assign Driver to Order #{record?.id}</DialogTitle>
                <DialogContent>
                    {!verificationCode ? (
                        <>
```jsx
                            <Typography variant="body2" sx={{ mb: 2 }}>
                                Select a driver to assign to this order:
                            </Typography>
                            <FormControl fullWidth sx={{ mb: 2 }}>
                                <InputLabel>Driver</InputLabel>
                                <Select
                                    value={selectedDriver}
```
                                    value={selectedDriver}
                                    onChange={(e) => setSelectedDriver(e.target.value)}
                                    label="Driver"
                                >
                                    {drivers.map((driver) => (
                                        <MenuItem key={driver.id} value={driver.id}>
                                            {driver.name} - {driver.phone}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </>
                    ) : (
```jsx
                        <Box sx={{ textAlign: 'center', py: 2 }}>
                            <Typography variant="h6" sx={{ mb: 2 }}>
                                Driver Assigned Successfully
                            </Typography>
                            <Typography variant="body2" sx={{ mb: 2 }}>
                                The driver will need this verification code to access the order details:
                            </Typography>
                            <Chip
                                label={verificationCode}
```
                                label={verificationCode}
                                color="primary"
                                size="large"
```jsx
                                sx={{ fontSize: '1.5rem', py: 3, px: 2 }}
                            />
                            <Typography variant="caption" sx={{ display: 'block', mt: 2 }}>
                                Please provide this code to the driver
                            </Typography>
                        </Box>
                    )}
```
                    )}
                </DialogContent>
                <DialogActions>
                    {!verificationCode ? (
                        <>
                            <Button onClick={handleClose}>Cancel</Button>
                            <Button 
                                onClick={handleAssign} 
                                variant="contained" 
                                disabled={!selectedDriver || loading}
                            >
                                Assign Driver
                            </Button>
                        </>
                    ) : (
                        <Button onClick={handleClose} variant="contained">Close</Button>
                    )}
                </DialogActions>
            </Dialog>
        </>
    );
};

export default AssignDriverButton;

Copy


AssignDriverButton.tsx
Now, let's create a Map Dashboard component for visualizing all active deliveries:

import React, { useEffect, useRef, useState } from 'react';
import { useDataProvider, Loading, Error } from 'react-admin';
import { 
    Box, 
    Paper, 
    Typography, 
    Grid, 
    Card, 
    CardContent, 
    Chip,
    Divider,
    List,
    ListItem,
    ListItemText,
    ListItemAvatar,
    Avatar
} from '@mui/material';
import { Loader } from '@googlemaps/js-api-loader';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import HomeIcon from '@mui/icons-material/Home';

const DeliveryDashboard = () => {
    const mapRef = useRef<HTMLDivElement>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeOrders, setActiveOrders] = useState([]);
    const dataProvider = useDataProvider();
    
    // Load active orders
    useEffect(() => {
        const fetchActiveOrders = async () => {
            try {
                const { data } = await dataProvider.getList(
                    'delivery/tracking-order',
                    {
                        pagination: { page: 1, perPage: 100 },
                        sort: { field: 'id', order: 'DESC' },
                        filter: { delivery_status: ['assigned', 'withdrawed'] }
                    }
                );
                
                setActiveOrders(data);
                setLoading(false);
            } catch (err) {
                setError(err);
                setLoading(false);
            }
        };
        
        fetchActiveOrders();
        
        // Refresh data every 30 seconds
        const interval = setInterval(fetchActiveOrders, 30000);
        return () => clearInterval(interval);
    }, []);
    
    // Initialize the Google Map
    useEffect(() => {
        if (loading || error || !activeOrders.length) return;
        
        const loader = new Loader({
            apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
            version: 'weekly',
        });
        
        loader.load().then(() => {
            if (!mapRef.current || !window.google) return;
            
            const restaurantLocation = { lat: -33.43949, lng: -70.6179356 }; // PinoyWok location
            
            const map = new window.google.maps.Map(mapRef.current, {
                center: restaurantLocation,
                zoom: 12,
            });
            
            // Restaurant marker
            new window.google.maps.Marker({
                position: restaurantLocation,
                map,
                title: 'PinoyWok Restaurant',
                icon: {
                    url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                }
            });
            
            // Add markers for each active order
            activeOrders.forEach(order => {
                if (!order.coordinates?.lat || !order.coordinates?.lng) return;
                
                const deliveryLocation = { 
                    lat: order.coordinates.lat, 
                    lng: order.coordinates.lng 
                };
                
                const marker = new window.google.maps.Marker({
                    position: deliveryLocation,
                    map,
                    title: `Order #${order.id} - ${order.customer.name}`,
                    label: order.id.toString()
                });
                
                // Info window with order details
                const infoWindow = new window.google.maps.InfoWindow({
                    content: `
                        <div style="padding: 10px;">
                            <h3>Order #${order.id}</h3>
                            <p><strong>Customer:</strong> ${order.customer.name}</p>
                            <p><strong>Status:</strong> ${order.delivery_status}</p>
                            <p><strong>Driver:</strong> ${order.driver ? order.driver.name : 'Unassigned'}</p>
                            <p><strong>Address:</strong> ${order.shipping_address.address}</p>
                        </div>
                    `
                });
                
                marker.addListener('click', () => {
                    infoWindow.open(map, marker);
                });
                
                // Draw route from restaurant to delivery location
                const directionsService = new window.google.maps.DirectionsService();
                const directionsRenderer = new window.google.maps.DirectionsRenderer({
                    map,
                    suppressMarkers: true,
                    polylineOptions: {
                        strokeColor: order.delivery_status === 'withdrawed' ? '#FF0000' : '#0000FF',
                        strokeWeight: 4
                    }
                });
                
                directionsService.route({
                    origin: restaurantLocation,
                    destination: deliveryLocation,
                    travelMode: window.google.maps.TravelMode.DRIVING
                }, (response, status) => {
                    if (status === 'OK') {
                        directionsRenderer.setDirections(response);
                    }
                });
            });
        });
    }, [loading, error, activeOrders]);
    
    if (loading) return <Loading />;
    if (error) return <Error error="Failed to load active orders" />;
    
    return (
```jsx
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" sx={{ mb: 3 }}>
                Delivery Dashboard
            </Typography>
            
            <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                    <Paper elevation={3} sx={{ height: '70vh', p: 2 }}>
                        <Typography variant="h6" sx={{ mb: 2 }}>
                            Active Deliveries Map
                        </Typography>
                        
                        <Box 
                            ref={mapRef} 
```
                            ref={mapRef} 
                            sx={{ 
                                width: '100%', 
                                height: 'calc(100% - 40px)',
                                borderRadius: 1,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                            }}
                        >
                            {!activeOrders.length && (
                                <Typography variant="subtitle1">
                                    No active deliveries to display
                                </Typography>
                            )}
                        </Box>
                    </Paper>
                </Grid>
                
                <Grid item xs={12} md={4}>
```jsx
                    <Card sx={{ mb: 3 }}>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Active Deliveries: {activeOrders.length}
```
                                Active Deliveries: {activeOrders.length}
                            </Typography>
```jsx
                            <Box sx={{ display: 'flex', gap: 1 }}>
                                <Chip 
                                    icon={<LocalShippingIcon />} 
```
                                    icon={<LocalShippingIcon />} 
                                    label={`Assigned: ${activeOrders.filter(o => o.delivery_status === 'assigned').length}`} 
                                    color="warning" 
                                    variant="outlined" 
                                />
                                <Chip 
                                    icon={<LocalShippingIcon />} 
                                    label={`In Transit: ${activeOrders.filter(o => o.delivery_status === 'withdrawed').length}`} 
                                    color="primary" 
                                    variant="outlined" 
                                />
                            </Box>
                        </CardContent>
                    </Card>
                    
```jsx
                    <Paper elevation={3} sx={{ maxHeight: 'calc(70vh - 100px)', overflow: 'auto' }}>
                        <Typography variant="h6" sx={{ p: 2, pb: 1 }}>
                            Active Orders
                        </Typography>
                        <Divider />
                        
                        <List>
                            {activeOrders.length === 0 ? (
                                <ListItem>
                                    <ListItemText primary="No active deliveries" />
                                </ListItem>
                            ) : (
                                activeOrders.map(order => (
                                    <React.Fragment key={order.id}>
                                        <ListItem>
                                            <ListItemAvatar>
                                                <Avatar>
                                                    {order.delivery_status === 'assigned' 
                                                        ? <RestaurantIcon /> 
                                                        : <LocalShippingIcon />}
```
                                                        : <LocalShippingIcon />}
                                                </Avatar>
                                            </ListItemAvatar>
                                            <ListItemText 
                                                primary={`Order #${order.id}`}
                                                secondary={
                                                    <>
                                                        <Typography component="span" variant="body2">
                                                            {order.customer.name} • {order.shipping_address.address}
                                                        </Typography>
                                                        <br />
                                                        <Typography component="span" variant="body2" color="textSecondary">
                                                            Driver: {order.driver?.name || 'Unassigned'}
                                                        </Typography>
                                                        <br />
                                                        <Chip 
                                                            size="small"
                                                            label={order.delivery_status === 'assigned' ? 'Assigned' : 'In Transit'} 
                                                            color={order.delivery_status === 'assigned' ? 'warning' : 'primary'} 
                                                            variant="outlined"
```jsx
                                                            sx={{ mt: 1 }}
                                                        />
                                                    </>
                                                }
```
                                                }
                                            />
                                        </ListItem>
                                        <Divider variant="inset" component="li" />
                                    </React.Fragment>
                                ))
                            )}
                        </List>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default DeliveryDashboard;

Copy


DeliveryDashboard.tsx
Step 8: Create Public Tracking Page
Create a standalone tracking page that customers can access without authentication:

import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { 
    Container,
    Paper,
    Typography,
    Box,
    Stepper,
    Step,
    StepLabel,
    Grid,
    Divider,
    List,
    ListItem,
    ListItemText,
    Card,
    CardContent,
    CircularProgress
} from '@mui/material';
import { Loader } from '@googlemaps/js-api-loader';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import HomeIcon from '@mui/icons-material/Home';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import axios from 'axios';

const steps = [
    { label: 'Order Confirmed', icon: <RestaurantIcon /> },
    { label: 'Preparing', icon: <RestaurantIcon /> },
    { label: 'Out for Delivery', icon: <LocalShippingIcon /> },
    { label: 'Delivered', icon: <HomeIcon /> }
];

const getStepFromStatus = (status) => {
    switch (status) {
        case 'paid': return 0;
        case 'assigned': return 1;
        case 'withdrawed': return 2;
        case 'delivered': return 3;
        default: return 0;
    }
};

const PublicTrackingPage = () => {
    const { id } = useParams();
    const [order, setOrder] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const mapRef = useRef(null);
    
    useEffect(() => {
        const fetchOrder = async () => {
            try {
                const response = await axios.get(`/api/tracking/${id}`);
                setOrder(response.data.order);
                setLoading(false);
            } catch (err) {
                setError('Order not found or tracking unavailable');
                setLoading(false);
            }
        };
        
        fetchOrder();
        
        // Poll for updates every 30 seconds
        const interval = setInterval(fetchOrder, 30000);
        return () => clearInterval(interval);
    }, [id]);
    
    useEffect(() => {
        if (!order || !mapRef.current) return;
        
        const loader = new Loader({
            apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
            version: 'weekly',
        });
        
        loader.load().then(() => {
            if (!window.google) return;
            
            const restaurantLocation = { lat: -33.43949, lng: -70.6179356 }; // PinoyWok location
            const deliveryLocation = { 
                lat: order.coordinates?.lat, 
                lng: order.coordinates?.lng 
            };
            
            if (!deliveryLocation.lat || !deliveryLocation.lng) return;
            
            const map = new window.google.maps.Map(mapRef.current, {
                center: deliveryLocation,
                zoom: 14,
            });
            
            // Restaurant marker
            new window.google.maps.Marker({
                position: restaurantLocation,
                map,
                title: 'PinoyWok Restaurant',
                icon: {
                    url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                }
            });
            
            // Delivery location marker
            new window.google.maps.Marker({
                position: deliveryLocation,
                map,
                title: 'Delivery Address'
            });
            
            // Draw route
            const directionsService = new window.google.maps.DirectionsService();
            const directionsRenderer = new window.google.maps.DirectionsRenderer({
                map,
                suppressMarkers: true
            });
            
            directionsService.route({
                origin: restaurantLocation,
                destination: deliveryLocation,
                travelMode: window.google.maps.TravelMode.DRIVING
            }, (response, status) => {
                if (status === 'OK') {
                    directionsRenderer.setDirections(response);
                }
            });
        });
    }, [order]);
    
    if (loading) {
        return (
```jsx
            <Container maxWidth="md" sx={{ py: 5, textAlign: 'center' }}>
                <CircularProgress />
                <Typography variant="h6" sx={{ mt: 2 }}>
                    Loading order tracking...
                </Typography>
            </Container>
        );
```
        );
    }
    
    if (error) {
        return (
```jsx
            <Container maxWidth="md" sx={{ py: 5, textAlign: 'center' }}>
                <Typography variant="h5" color="error" gutterBottom>
                    {error}
```
                    {error}
                </Typography>
                <Typography variant="body1">
                    Please check your tracking number or contact customer support.
                </Typography>
            </Container>
        );
    }
    
    const activeStep = getStepFromStatus(order.status);
    
    return (
```jsx
        <Container maxWidth="md" sx={{ py: 5 }}>
            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <Box>
                        <Typography variant="h4" gutterBottom>
                            Order #{order.id} Tracking
                        </Typography>
                        <Typography variant="subtitle1">
                            Tracking Number: {order.tracking_number}
```
                            Tracking Number: {order.tracking_number}
                        </Typography>
                    </Box>
                    {order.status === 'delivered' && (
                        <CheckCircleIcon 
                            color="success" 
```jsx
                            sx={{ ml: 'auto', fontSize: 40 }} 
                        />
                    )}
```
                    )}
                </Box>
                
                <Stepper activeStep={activeStep} alternativeLabel>
                    {steps.map((step, index) => (
                        <Step key={step.label}>
                            <StepLabel StepIconComponent={() => (
```jsx
                                <Box sx={{ textAlign: 'center' }}>
                                    {index <= activeStep ? (
                                        <Box sx={{ color: 'primary.main' }}>
                                            {step.icon}
```
                                            {step.icon}
                                        </Box>
                                    ) : step.icon}
                                </Box>
                            )}>
                                {step.label}
                            </StepLabel>
                        </Step>
                    ))}
                </Stepper>
            </Paper>
            
            <Grid container spacing={4}>
                <Grid item xs={12} md={7}>
                    <Paper elevation={3}>
```jsx
                        <Box sx={{ p: 2 }}>
                            <Typography variant="h6" gutterBottom>
                                Delivery Map
                            </Typography>
                        </Box>
                        <Divider />
                        <Box 
                            ref={mapRef} 
```
                            ref={mapRef} 
                            sx={{ 
                                width: '100%', 
                                height: 350,
                            }}
                        />
```jsx
                        <Box sx={{ p: 2 }}>
                            <Typography variant="body2" color="textSecondary">
                                {order.shipping_address.address}
```
                                {order.shipping_address.address}
                            </Typography>
                        </Box>
                    </Paper>
                </Grid>
                
                <Grid item xs={12} md={5}>
```jsx
                    <Card sx={{ mb: 3 }}>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Delivery Info
                            </Typography>
                            <List dense>
                                <ListItem>
                                    <ListItemText 
                                        primary="Estimated Preparation Time" 
                                        secondary={`${order.preparation_time} minutes`} 
```
                                        secondary={`${order.preparation_time} minutes`} 
                                    />
                                </ListItem>
                                {order.withdraw_time && (
                                    <ListItem>
                                        <ListItemText 
                                            primary="Pickup Time" 
                                            secondary={new Date(order.withdraw_time).toLocaleString()} 
                                        />
                                    </ListItem>
                                )}
                                {order.status === 'withdrawed' && (
                                    <ListItem>
                                        <ListItemText 
                                            primary="Estimated Arrival" 
                                            secondary={
                                                new Date(new Date(order.withdraw_time).getTime() + 20 * 60000).toLocaleString()
                                            } 
                                        />
                                    </ListItem>
                                )}
                            </List>
                        </CardContent>
                    </Card>
                    
                    <Paper elevation={3}>
```jsx
                        <Box sx={{ p: 2 }}>
                            <Typography variant="h6" gutterBottom>
                                Order Status Updates
                            </Typography>
                        </Box>
                        <Divider />
                        <List>
                            {order.tracking_history?.map((history, index) => (
                                <ListItem key={index}>
                                    <ListItemText 
                                        primary={(() => {
                                            switch(history.status) {
                                                case 'paid': return 'Order Confirmed';
```
                                                case 'paid': return 'Order Confirmed';
                                                case 'assigned': return 'Preparing Your Order';
                                                case 'withdrawed': return 'Out for Delivery';
                                                case 'delivered': return 'Order Delivered';
                                                default: return history.status;
                                            }
                                        })()}
                                        secondary={new Date(history.timestamp).toLocaleString()} 
                                    />
                                </ListItem>
                            ))}
                        </List>
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
};

export default PublicTrackingPage;

Copy


PublicTrackingPage.tsx
Step 9: Register Routes in the Dash App
Update your app routes to include the dashboard and public tracking page:

// Add these imports
import DeliveryDashboard from './pages/DeliveryDashboard';
import PublicTrackingPage from './pages/PublicTrackingPage';

// Add these to your DASHAdmin component in the customRoutes prop
customRoutes={[
    // Other custom routes
    <Route key="delivery-dashboard" path="/delivery/dashboard" element={<DeliveryDashboard />} />,
]}

// Add these to the customAuthRoutes prop for the public tracking page (no auth required)
customAuthRoutes={[
    // Other custom auth routes
    <Route key="public-tracking" path="/tracking/:id" element={<PublicTrackingPage />} />,
]}

Copy


App.tsx
Step 10: Register Resources
Finally, add the new resources to your DASHResources.tsx file:

import { DASHResources as CoreResources } from 'dash-admin';
import DriverResource from './resources/DriverResource';
import TrackingOrderResource from './resources/TrackingOrderResource';

export const DASHResources = [
    ...CoreResources,
    DriverResource,
    TrackingOrderResource,
    // other resources
];

Copy


DASHResources.tsx
Step 11: Add WebSocket Listeners
Add WebSocket listeners to your Dash application to enable real-time updates:

import { useEffect } from 'react';
import { useRefresh, useNotify } from 'react-admin';
import Echo from 'laravel-echo';

const OrderStatusListener = () => {
    const refresh = useRefresh();
    const notify = useNotify();
    
    useEffect(() => {
        // Assuming you have Echo set up in your Dash application
        const echo = window.Echo;
        
        // Listen for status updates on the orders channel
        const channel = echo.private('orders');
        
        channel.listen('.status.updated', (e) => {
            // Refresh the current view to show updated data
            refresh();
            
            // Show a notification
            const statusMessages = {
                'paid': 'Order confirmed',
                'assigned': 'Order assigned to driver',
                'withdrawed': 'Order picked up by driver',
                'delivered': 'Order delivered'
            };
            
            notify(`Order #${e.order_id}: ${statusMessages[e.status] || 'Status updated'}`, {
                type: 'info',
                autoHideDuration: 5000
            });
        });
        
        return () => {
            channel.stopListening('.status.updated');
        };
    }, []);
    
    // This component doesn't render anything
    return null;
};

export default OrderStatusListener;

Copy


OrderStatusListener.tsx
Then add this component to your app layout:

import { AppLayout } from 'dash-admin';
import OrderStatusListener from '../components/delivery/OrderStatusListener';

const CustomLayout = (props) => (
    <>
        <OrderStatusListener />
        <AppLayout {...props} />
    </>
);

export default CustomLayout;

Copy


CustomLayout.tsx
Summary of Migration
You've now successfully migrated the PinoyWok delivery tracking system to your Dash architecture. The migration includes:

Database Changes: Extended the Order model with tracking fields and added new Driver and TrackingStatus models
Backend API: Created controllers to handle tracking, assignment, and status updates
Admin Interface: Added resources for managing drivers and tracking orders
Public Tracking: Implemented a standalone tracking page for customers
Map Integration: Integrated Google Maps for visualization of delivery locations
Real-time Updates: Added WebSocket support for real-time status updates
This implementation takes advantage of Dash's structured architecture while preserving the key functionality from the original PinoyWok delivery system. You can now manage the entire delivery flow from order receipt to delivery completion within your Dash application.