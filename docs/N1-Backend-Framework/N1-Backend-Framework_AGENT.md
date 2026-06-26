Dash is a full-stack solution that combines two specialized components.
You are an expert Laravel, PHP, React and React-Admin developer. 

Dash-Backend: A  Laravel-based API that delivers enterprise-grade features including multi-tenant architecture, granular role-based permissions, real-time WebSocket messaging, comprehensive audit trails, and domain-driven design principles, segregating the core dash logic which provides the base features from the domain logic which provides the specific client project logic.

Dash-Frontend: A frontend built on top of ReactAdmin that provides rich UI components, standardized CRUD operations, advanced data management, and seamless API integration. It extends ReactAdmin's capabilities with custom components and workflows specifically designed to leverage Dash-Backend's features, implementing specialized protocols between Frontend/Backend communication. 

Together, these components create a complete platform for rapidly building scalable, secure, and feature-rich administrative interfaces while maintaining clean separation of concerns and professional code organization.

The integration between Laravel and ReactAdmin is seamless through standardized API endpoints and resource controllers, as evidenced in the ReactAdminBaseController class that handles common CRUD operations, allowing an architecture for rapid development of feature-rich admin interfaces while maintaining clean separation between frontend and backend concerns.

Example:
Creating a CRUD (Create, Read, Update, Delete) application for a simple To-Do list.

The Dash Backend offers a straightforward scaffolding command designed to facilitate the creation of a simple CRUD application. This command illustrates all the essential components necessary for developing a Resource Module within the Dash framework, to quickly implement CRUD functionality, simply invoke the CreateDashModuleCommand and specify the desired Group and Module Name.

sail artisan make:dash-module {GroupName} {ResourceName} {--force}

What is a Group?

The group is basically the path of your resource in your api, that is both represented at frontend and backend. 

/api/group/module_name

TD: The feature considers nested resources, technically the framework enables it, nevertheless the scaffolding tool for tutorial purposes has only been implemented and tested for one depth level.

What is a ResourceName?

The Resource Name is the name of your resource that is represented both, in backend and frontend urls, the Module implements the CRUD endpoints for backend and frontend. 
While the Group can have multiple Resources, a Resource wraps the CRUD operations for a specific model. 

http://dash.frontend.url/group/resource_name
http://dash.backend.url/api/group/resource_name

What is necessary to create a CRUD application for a model?

Dash Framework, requires  Laravel’s backend Migration, Model, Controller, Filter, Request, Policy and Resource. And a Dash Resource Frontend configuration file and schema. 

Backend File Locations for a Dash Resource.

The controllers, models, routes and migrations for your application must be located within the domain folder.

Controllers: domain/app/Http/Controllers/API/{GroupName}/{ModuleName}/*
Models: domain/app/Models/{GroupName}/
Routes: domain/routes/api/
Migrations: domain/database/migrations/

Frontend File Locations for a Dash Resource.

Resource: ./apps/dash/src/resources

The frontend application specifies its resources in the file located at apps/dash/src/DASHResources.tsx. Regardless of where a particular resource configuration resides within your DashAdmin project, it must be added to the DASHResources object. It's important to keep in mind two fundamental concepts in the React frontend: Dash Resource and Dash Schema.

- Dash Resource configuration (IDashAutoAdminResourceConfig)

A Dash Resource outlines the configuration options for a dash-auto-admin resource within the Dash Admin framework. It encompasses properties that define the group, resource, and schema, along with additional attributes such as labels, icons, custom components, buttons, toolbars, layouts, and various other options. These settings allow for the customization of the resource's behavior, influencing the operation of auto-admin components, including list, edit, create, and show views, as well as the overall layout and functionality of the resource.

- Dash Schema configuration  (IDashAutoAdminAttribute[])

A Dash Resource outlines the configuration options for a dash-auto-admin resource within the Dash Admin framework. It encompasses properties that define the group, resource, and schema, along with additional attributes such as labels, icons, custom components, buttons, toolbars, layouts, and various other options. These settings allow for the customization of the resource's behavior, influencing the operation of auto-admin components, including list, edit, create, and show views, as well as the overall layout and functionality of the resource.

Tutorial: CRUD TODO LIST:

This guide represents step by step the creation of a simple TODO List crud application with Dash Framework. Show the full code required for the implementation.

To create a simple TODO list CRUD application with the Dash framework, follow these steps:

Step 1: Create the Migration File
This file will define the schema for your "todos" table in the database.
Note: Database table names must be “Plural”, while Laravel’s Models “Singular”

<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('todos', function (Blueprint $table) {
            $table->id();
            $table->string('name', 100);
            $table->boolean('active')->default(false);
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('todos');
    }
};

Place this migration file in domain/database/migrations``[1].

Step 2: Create the Model
Define the Todo model which will interact with the database.

<?php

namespace Domain\App\Models\Example;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use EloquentFilter\Filterable;
use Rennokki\QueryCache\Traits\QueryCacheable;

class Todo extends Model
{
    use HasFactory, Filterable, QueryCacheable;

    protected $fillable = ['name', 'active'];

    protected $casts = [
        'active' => 'boolean'
    ];

    // Define relationships and other model logic here
}

Make sure the model is in domain/app/Models/Example directory.


Step 3: Create the Controller
Define the controller with CRUD operations for the Todo resource.


<?php

namespace Domain\App\Http\Controllers\API\Example\Todo;

use Domain\App\Models\Example\Todo;
use Illuminate\Support\Facades\Request;
use App\Http\Controllers\API\Admin\ReactAdminBaseController;

class TodoController extends ReactAdminBaseController
{
    public $resource         = 'todo';
    public $requestValidator = TodoRequest::class;
    public $modelFilter      = TodoFilter::class;
    public $policy           = TodoPolicy::class;
´rou
    public function __construct()
    {
        $this->model = Todo::query();
    }

    // Additional methods for CRUD operations...
}

The controller handles all the CRUD operations and should be placed in domain/app/Http/Controllers/API/Example/Todo``[2].


Step 4: Define the Resource
Create a resource file to define how data will be transformed into JSON.

<?php
namespace Domain\App\Http\Controllers\API\Example\Todo;

use Illuminate\Http\Resources\Json\JsonResource;

class TodoResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id'     => $this->id,
            'name'   => $this->name,
            'active' => $this->active
        ];
    }
}


Place this in domain/app/Http/Controllers/API/Example/Todo directory[3].








Step 5: Define the Policy
Manage access control using the policy.

<?php

namespace Domain\App\Http\Controllers\API\Example\Todo;

use App\Models\User;
use Domain\App\Models\Example\Todo;
use Illuminate\Auth\Access\HandlesAuthorization;

class TodoPolicy
{
    use HandlesAuthorization;

    // Define policy rules here...
}

Store in domain/app/Http/Controllers/API/Example/Todo``[4].


Step 6: Define the Request Validation
Create request validation logic.

<?php

namespace Domain\App\Http\Controllers\API\Example\Todo;

use Illuminate\Foundation\Http\FormRequest;

class TodoRequest extends FormRequest
{
    public function rules()
    {
        return ['name' => 'required|string|max:100'];
    }

    public function validated($key = null, $default = null)
    {
        return parent::validated($key, $default);
    }
}


Also store this in domain/app/Http/Controllers/API/Example/Todo``[5].


Step 7: Create Routes
Define routes for accessing the Todo endpoints.

<?php

use Illuminate\Support\Facades\Route;

Route::group(['middleware' => ['auth:sanctum'], 'as' => 'example.', 'prefix' => 'example'], function () {
    Route::prefix('todo')->name('todo.')->group(function () {
        $class = \Domain\App\Http\Controllers\API\Example\Todo\TodoController::class;
        Route::get('forSelect/{url?}', [$class, 'getForSelect'])->name('getForSelect');
        // Additional route definitions...
    });
});


Add this in domain/routes/api/``[6].

Step 8: Create Frontend Resource Configuration

import { TrashTemplate, ResourceTemplate } from "dash-admin";
import Dot from "@mui/icons-material/FiberManualRecord";
import React from "react";

const Icon = Dot as unknown as React.FC;

const TodoSchema = [
    {
        tab: 'Datos',
        attribute: 'name',
        label: 'Nombre',
        type: String,
    }
];

const TodoResource = {
    roles: ["*"],
    component: ResourceTemplate,
    customRoutes: (resourceConfig) => TrashTemplate(resourceConfig),
    model: "example/todo",
    label: "Todo",
    schema: TodoSchema,
    icon: <Icon />,
    group: "Example",
    
    menu: [
        {
            title: "List",
            redirect: "/example/todo",
        },
        {
            title: "Trash",
            redirect: "/example/trash/todo",
        },
    ],

    mainAction: {
        title: "Crear Todo",
        mode: "create",
        fn:"virtualhash",
        redirect: "inline/create",
    },

    view: true,
    create: true,
    edit: true,
  
    drawer: true,
    drawerOptions: {
        create: true,
        edit: true,
        view: true
    },
};

export default TodoResource;






This code should be placed in ./apps/dash/src/resources``[7].

Following these steps will set up a basic TODO List CRUD application using the Dash Framework with Laravel and React components.

Files required:
Place this files @:

[1]: {date}_todo_migration.php -> domain/database/migrations
[2]: TodoController.php -> domain/app/Http/Controllers/API/Example/Todo
[3]: TodoResource.php -> domain/app/Http/Controllers/API/Example/Todo 
[4]: TodoPolicy.php -> domain/app/Http/Controllers/API/Example/Todo 
[5]: TodoRequest.php -> domain/app/Http/Controllers/API/Example/Todo 
[6]: todo_routes.php -> domain/routes/api/
[7]: TodoResource.tsx -> ./apps/dash/src/resources


Step 9:

Add Resource to DASHResources


Include the Todo resource in the DASHResources object to ensure it gets loaded into the application.

// apps/dash/src/DASHResources.tsx
import { TodoResource } from './resources/TodoResource';

export const DASHResources = [
   TodoResource,
   // Add other resources here
];


By following these steps, you have all the necessary files and code for a complete TODO List CRUD application using Dash. You can now manage TODOs from the DashAdmin interface with backend support from Laravel, providing a seamless development experience while maintaining clear separations between frontend and backend. Adjust and extend the code as needed to fit additional customizations and features.


BASE PROMPT:

You are an expert software engineer and developer in Laravel and React. 

Dash is a powerful full-stack solution that combines two specialized components:

- DashBackend: A robust Laravel-based API that delivers enterprise-grade features including multi-tenant architecture, granular role-based permissions, real-time WebSocket messaging, comprehensive audit trails, and domain-driven design principles.

- DashAdmin: A frontend built on top of ReactAdmin that provides rich UI components, standardized CRUD operations, advanced data management, and seamless API integration. It extends ReactAdmin's capabilities with custom components and workflows specifically designed to leverage Dash-Backend's features, implementing specialized protocols between Frontend/Backend communication. 

Together, these components create a complete platform for rapidly building scalable, secure, and feature-rich administrative interfaces while maintaining clean separation of concerns and professional code organization.

.*//DASHAdmin
React Frontend CORE FEATURES

- Data-driven CRUD operations through standardized REST endpoints
- Advanced filtering, sorting and pagination
- Customizable data grids and forms
- Resource-based architecture matching Laravel's API responses.
- Built-in authentication and authorization flows integration (register, login, change-password, recover-password).
- Rich UI components for rapid admin interface development
- Extensible theming system

The integration between Laravel and ReactAdmin is seamless through standardized API endpoints and resource controllers, as evidenced in the ReactAdminBaseController class that handles common CRUD operations, allowing an architecture for rapid development of feature-rich admin interfaces while maintaining clean separation between frontend and backend concerns.

The system leverages ReactAdmin's powerful data provider capabilities to handle complex data operations, while Laravel's backend provides the robust API foundation, authentication, and multi-tenant data isolation.

.*//DASHBackend
Backend CORE FEATURES

Dash-Backend is a robust Laravel-based web dashboard API that delivers a comprehensive Multi-Tenant architecture with built-in data isolation. 

The system features advanced user management with granular role-based permissions controlled at API method level. It includes real-time capabilities through WebSocket-enabled messaging, detailed audit trail tracking, and follows Domain-Driven Design principles with a clear separation between core business logic and application concerns. The architecture ensures scalability and maintainability while providing a solid foundation for enterprise-grade applications.

The modular structure and API-first approach make it an excellent choice for powering modern web applications that require sophisticated access control, real-time features, and multi-tenant capabilities right from the start.

DASH ESSENTIALS

Creating a CRUD (Create, Read, Update, Delete) application for a simple To-Do list.

The Dash Backend offers a straightforward scaffolding command designed to facilitate the creation of a simple CRUD application. This command illustrates all the essential components necessary for developing a Resource Module within the Dash framework, to quickly implement CRUD functionality, simply invoke the CreateDashModuleCommand and specify the desired Group and Module Name.

sail artisan make:dash-module {GroupName} {ResourceName} {--force}

What is a Group?

The group is basically the path of your resource in your api, that is both represented at frontend and backend. 

/api/group/module_name

TD: The feature considers nested resources, technically the framework enables it, nevertheless the scaffolding tool for tutorial purposes has only been implemented and tested for one depth level.

What is a ResourceName?

The Resource Name is the name of your resource that is represented both, in backend and frontend urls, the Module implements the CRUD endpoints for backend and frontend. 
While the Group can have multiple Resources, a Resource wraps the CRUD operations for a specific model. 

http://dash.frontend.url/group/resource_name (Reference DashAdmin ResourceTemplate, for more about Dash frontend url formats).
http://dash.backend.url/api/group/resource_name (Reference ReactAdminBaseController for more about Dash backend url formats).

What is necessary to create a CRUD application for a model?

Dash Framework, requires a Laravel’s migration (the database schema for the model), a Laravel’s Model, a Laravel’s Controller, and a Dash Resource Frontend configuration file.
Meanwhile the Dash Laravel’s Controller requires optionally a Request, a Policy, and a Filter.

Backend File Locations for a Dash Resource.

The controllers, models, routes and migrations for your application must be located within the domain folder.

- Controllers: domain/app/Http/Controllers/API/{GroupName}/{ModuleName}/*
- Models: domain/app/Models/{GroupName}/
- Routes: domain/routes/api/
- Migrations: domain/database/migrations/

Frontend File Locations for a Dash Resource.

Resource: ./apps/dash/src/resources

The frontend application specifies its resources in the file located at apps/dash/src/DASHResources.tsx. Regardless of where a particular resource configuration resides within your DashAdmin project, it must be added to the DASHResources object. It's important to keep in mind two fundamental concepts in the React frontend: Dash Resource and Dash Schema.

- Dash Resource configuration (IDashAutoAdminResourceConfig)

A Dash Resource outlines the configuration options for a dash-auto-admin resource within the Dash Admin framework. It encompasses properties that define the group, resource, and schema, along with additional attributes such as labels, icons, custom components, buttons, toolbars, layouts, and various other options. These settings allow for the customization of the resource's behavior, influencing the operation of auto-admin components, including list, edit, create, and show views, as well as the overall layout and functionality of the resource.

- Dash Schema configuration  (IDashAutoAdminAttribute[])

A Dash Resource outlines the configuration options for a dash-auto-admin resource within the Dash Admin framework. It encompasses properties that define the group, resource, and schema, along with additional attributes such as labels, icons, custom components, buttons, toolbars, layouts, and various other options. These settings allow for the customization of the resource's behavior, influencing the operation of auto-admin components, including list, edit, create, and show views, as well as the overall layout and functionality of the resource.

Assitance notes:
-  use Domain\App for all namespaces at code generation.
- for models and controllers, replicate the features outlined at the files provided. consider the implementation of the request File, Filter file and Policy.
- for models always add: use HasFactory, Filterable, QueryCacheable;
- for models always  implement casts for boolean and arrays, depending on the schema e.g:  protected $casts = [
        'active' => 'boolean'
    ];
- for a controller always return a full code example for the Request, the Polocy and the Filter. 
- For frontend request resources, always use all configuration options presented into the files examples. 

For complex implementations, please refer to the files regarding the Tabs and prefixed with "tab" or "tabs" in the filename that exemplified a fully function restaurant tabs application.


-Use sail if needed.
-Dont use 2>&1 in outputs.
-Always read the files in the context and analyze them before evaluating the solution in the current context window. 
-Use MUI components
-Frontend schema context (refer to the sampleComponent) specially regarding the view modes and the structure for the components. 

-Use sail if needed.
-Dont use 2>&1 in outputs.
-Always read the files in the context and analyze them before evaluating the solution in the current context window. 
-Use MUI components
-Frontend schema context (refer to the sampleComponent) specially regarding the view modes and the structure for the components. 