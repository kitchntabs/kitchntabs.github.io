# TypeScript Interface Generation Feature

## Overview

The TypeScript Interface Generation feature provides automatic generation of TypeScript interfaces from PHP Request and Resource classes in the Laravel backend. This ensures type safety and consistency between the backend API and frontend TypeScript code, particularly for React Admin applications.

The feature consists of:
- A core service that analyzes PHP classes and generates TypeScript interfaces
- A queue-able job for batch interface generation
- An Artisan command for CLI interface generation
- An API endpoint on each controller for retrieving interfaces
- Automatic file organization with barrel exports

## Architecture

### Core Components

#### TypeScriptInterfaceGeneratorService.php

**Location:** `app/Services/TypeScriptInterfaceGeneratorService.php`

The core service responsible for generating TypeScript interfaces from PHP classes. Key features:

- **Source Code Parsing**: Parses `rules()` method source code without instantiating classes to avoid authentication issues
- **Reflection Analysis**: Uses PHP Reflection to analyze Resource class `toArray()` methods
- **Type Mapping**: Comprehensive mapping from PHP types to TypeScript types
- **Interface Generation**: Creates three types of interfaces per controller:
  - Resource interface (for API responses)
  - Request interface (for form validation)
  - List interface (for paginated responses)

**Key Methods:**
- `generateInterfaces(string $controllerClass)`: Main entry point
- `generateResourceInterface()`: Analyzes JsonResource classes
- `generateRequestInterface()`: Parses FormRequest validation rules
- `generateListInterface()`: Creates paginated list interfaces
- `extractRulesFromRequestClass()`: Parses validation rules from source code

#### GenerateTypeScriptInterfacesJob.php

**Location:** `app/Jobs/GenerateTypeScriptInterfacesJob.php`

A queue-able Laravel job for generating interface files asynchronously.

**Features:**
- Processes individual controllers
- Handles file I/O operations
- Provides helper methods for batch processing
- Includes error handling and logging

**Key Methods:**
- `handle()`: Executes the interface generation
- `dispatchMany(array $controllers)`: Dispatches multiple jobs
- `dispatchFromDirectory(string $directory)`: Processes all controllers in a directory

#### GenerateTypeScriptInterfacesCommand.php

**Location:** `app/Console/Commands/GenerateTypeScriptInterfacesCommand.php`

Artisan command for CLI-based interface generation.

**Command:** `php artisan generate:interfaces`

**Options:**
- `--list`: List all available controllers
- `--system`: Generate for system controllers only
- `--domain`: Generate for domain controllers only
- `--all`: Generate for all controllers
- `--sync`: Run synchronously (not queued)
- `--output=path`: Custom output directory
- `--prefix=IPrefix`: Custom interface prefix

### Files Modified

#### ReactAdminBaseController.php

**Location:** `app/Http/Controllers/API/System/ReactAdminBaseController.php`

**Modifications:**
- Added `public $interfacePrefix = null;` property for configurable prefixes
- Added `interfaces(Request $request)` method to return generated interfaces as JSON
- Added `getDefaultInterfacePrefix()` method to determine prefix based on namespace

#### react-admin-methods.php

**Location:** `config/react-admin-methods.php`

**Modifications:**
- Added `'interfaces'` route configuration:
  ```php
  'interfaces' => [
      'path' => '/interfaces',
      'method' => 'get',
      'controllerMethod' => 'interfaces',
      'mode' => 'view'
  ]
  ```

### Output Structure

#### Directory Structure

```
resources/
└── interfaces/
    ├── index.ts              # Main barrel export
    ├── system/
    │   ├── index.ts          # System interfaces export
    │   ├── User.interfaces.ts
    │   ├── Role.interfaces.ts
    │   └── ...
    └── domain/
        ├── index.ts          # Domain interfaces export
        └── ...
```

#### Interface Naming Conventions

**System Controllers** (namespace: `App\Http\Controllers\API\System\`):
- Resource: `IBackendSystem{Model}Resource`
- Request: `IBackendSystem{Model}Request`
- List: `IBackendSystem{Model}List`

**Domain Controllers** (namespace: `Domain\App\Http\Controllers\API\`):
- Resource: `IBackendDomain{Model}Resource`
- Request: `IBackendDomain{Model}Request`
- List: `IBackendDomain{Model}List`

**Examples:**
- System User Controller: `IBackendSystemUserResource`, `IBackendSystemUserRequest`, `IBackendSystemUserList`
- Domain User Controller: `IBackendDomainUserResource`, `IBackendDomainUserRequest`, `IBackendDomainUserList`

## Usage

### Command Line Usage

#### List Available Controllers
```bash
php artisan generate:interfaces --list
```

#### Generate for Specific Controller
```bash
php artisan generate:interfaces "App\\Http\\Controllers\\API\\System\\UserController" --sync
```

#### Generate for System Controllers
```bash
php artisan generate:interfaces --system --sync
```

#### Generate for Domain Controllers
```bash
php artisan generate:interfaces --domain --sync
```

#### Generate for All Controllers (Queued)
```bash
php artisan generate:interfaces --all
```

#### Custom Output Directory
```bash
php artisan generate:interfaces --system --output=resources/types --sync
```

#### Custom Prefix
```bash
php artisan generate:interfaces --system --prefix=IApi --sync
```

### API Endpoint Usage

Each controller that extends `ReactAdminBaseController` now has an `/interfaces` endpoint:

**Endpoint:** `GET /api/{prefix}/{resource}/interfaces`

**Example:** `GET /api/system/user/interfaces`

**Response:**
```json
{
  "resource": "export interface IBackendSystemUserResource {\n    id: number;\n    tenant_id: number;\n    name: string;\n    email: string;\n    // ... other fields\n}",
  "request": "export interface IBackendSystemUserRequest {\n    name: string;\n    email?: string;\n    // ... other fields\n}",
  "list": "export interface IBackendSystemUserList {\n    data: IBackendSystemUserResource[];\n    total: number;\n    // ... pagination fields\n}"
}
```

### Frontend Integration

Import generated interfaces in your TypeScript files:

```typescript
// Import from barrel exports
import { IBackendSystemUserResource, IBackendSystemUserRequest } from '@/interfaces';

// Use in components
interface UserFormProps {
  user: IBackendSystemUserResource;
  onSubmit: (data: IBackendSystemUserRequest) => void;
}
```

## Technical Details

### Type Mapping

The service maps PHP types to TypeScript types:

| PHP Type | TypeScript Type |
|----------|-----------------|
| `int`, `integer` | `number` |
| `string` | `string` |
| `bool`, `boolean` | `boolean` |
| `float`, `double` | `number` |
| `array` | `any[]` |
| `Carbon` | `string` |
| `DateTime` | `string` |
| Custom classes | `any` |

### Validation Rule Parsing

The service parses Laravel validation rules from the `rules()` method:

```php
// PHP FormRequest
public function rules(): array
{
    return [
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        'age' => 'nullable|integer|min:18',
    ];
}
```

**Generated TypeScript:**
```typescript
export interface IBackendSystemUserRequest {
    name: string;
    email: string;
    age?: number;
}
```

### Resource Analysis

Analyzes `JsonResource` `toArray()` methods to determine response structure:

```php
// PHP Resource
public function toArray($request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'created_at' => $this->created_at?->toISOString(),
    ];
}
```

**Generated TypeScript:**
```typescript
export interface IBackendSystemUserResource {
    id: number;
    name: string;
    email: string;
    created_at: string;
}
```

### List Interface Generation

Creates paginated list interfaces based on Laravel's pagination structure:

```typescript
export interface IBackendSystemUserList {
    data: IBackendSystemUserResource[];
    total: number;
    per_page: number;
    current_page: number;
    last_page: number;
    from: number;
    to: number;
}
```

## Configuration

### Interface Prefix Configuration

Controllers can override the default prefix:

```php
class CustomController extends ReactAdminBaseController
{
    public $interfacePrefix = 'ICustom';
    
    // Will generate: ICustomModelResource, ICustomModelRequest, ICustomModelList
}
```

### Custom Output Directories

The command supports custom output directories:

```bash
php artisan generate:interfaces --system --output=frontend/src/types --sync
```

This will create files in `frontend/src/types/system/` instead of `resources/interfaces/system/`.

## Error Handling

### Common Issues

1. **Class Loading Errors**: The service parses source files directly to avoid autoloading issues
2. **Invalid Namespaces**: Domain controllers may have incorrect namespace declarations
3. **Missing Methods**: Controllers without `requestValidator` or `resource` properties are skipped

### Debugging

Enable detailed logging:

```bash
php artisan generate:interfaces --system --sync -v
```

Check generated files for syntax errors before committing.

## Best Practices

1. **Run Regularly**: Regenerate interfaces after schema changes
2. **Version Control**: Commit generated interface files
3. **Type Checking**: Use generated interfaces in frontend code
4. **Validation**: Test API endpoints return expected data structures
5. **Documentation**: Update frontend documentation when interfaces change

## Examples

### Complete Workflow

1. **Modify a Request class:**
   ```php
   // app/Http/Requests/UserRequest.php
   public function rules(): array
   {
       return [
           'name' => 'required|string|max:255',
           'email' => 'required|email|unique:users,email',
           'role_ids' => 'array',
           'role_ids.*' => 'exists:roles,id',
       ];
   }
   ```

2. **Regenerate interfaces:**
   ```bash
   php artisan generate:interfaces "App\\Http\\Controllers\\API\\System\\UserController" --sync
   ```

3. **Generated interface:**
   ```typescript
   export interface IBackendSystemUserRequest {
       name: string;
       email: string;
       role_ids?: number[];
   }
   ```

4. **Use in frontend:**
   ```typescript
   const submitUser = async (data: IBackendSystemUserRequest) => {
       await api.post('/api/system/user', data);
   };
   ```

## Maintenance

### Updating Interfaces

After backend changes:
1. Run the generation command for affected controllers
2. Review generated interfaces for accuracy
3. Update frontend code if needed
4. Test API integration

### Queue Processing

For large-scale generation, use queued jobs:
```bash
php artisan generate:interfaces --all
php artisan queue:work
```

### Cleanup

Remove old interface files:
```bash
rm -rf resources/interfaces/
php artisan generate:interfaces --all --sync
```