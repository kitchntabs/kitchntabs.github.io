# Adding an Image Field to a Model in Dash Framework

This document describes the complete process of adding an image upload field to a model in the Dash framework, covering both backend (Laravel) and frontend (React) implementation.

## Overview

Adding an image to a model requires changes in both the backend and frontend:

| Layer | Components to Modify |
|-------|---------------------|
| **Backend** | Model, Migration, Controller, Request, Resource |
| **Frontend** | Schema, Components (List + Edit), Resource Config |

## Backend Implementation

### 1. Database Migration

Add an `image_path` column to store the relative path of the uploaded image.

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
            $table->string('image_path')->nullable()->after('name');
        });
    }

    public function down(): void
    {
        Schema::table('your_table', function (Blueprint $table) {
            $table->dropColumn('image_path');
        });
    }
};
```

Run the migration:
```bash
sail artisan migrate
```

### 2. Model Configuration

Update your model to include the `image_path` field and create an accessor for the full URL.

```php
<?php

namespace Domain\App\Models\YourModule;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Support\Facades\Storage;

class YourModel extends Model
{
    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        // ... other fields
        'image_path',
    ];

    /**
     * The accessors to append to the model's array form.
     */
    protected $appends = ['image_url'];

    /**
     * Get the image URL accessor.
     */
    protected function imageUrl(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->image_path ? $this->getImageUrl() : null
        );
    }

    /**
     * Get the full image URL based on storage configuration.
     */
    private function getImageUrl(): ?string
    {
        if (!$this->image_path) {
            return null;
        }

        // Get the configured disk (same as used in Controller for upload)
        $disk = env('MEDIA_DISK', 'public');
        
        // Get the URL from storage using the correct disk
        $url = Storage::disk($disk)->url($this->image_path);

        // Check if URL is already absolute (S3 or external)
        if (filter_var($url, FILTER_VALIDATE_URL)) {
            return $url; // S3 or absolute URL, return as-is
        }

        // For local storage, add /api prefix to the path
        return url(str_replace('/storage/', '/api/storage/', $url));
    }
}
```

### 3. Request Validation

Add validation rules for the image field in your FormRequest class.

```php
<?php

namespace Domain\App\Http\Request\YourModule;

use Illuminate\Foundation\Http\FormRequest;

class YourModelRequest extends FormRequest
{
    public function rules()
    {
        return [
            // ... other rules
            'image' => 'nullable|image|max:2048|mimes:png,jpg,jpeg,gif,webp,svg',
        ];
    }
}
```

### 4. Controller Implementation

Handle image upload in both `_create` and `_update` methods. The controller must check the `MEDIA_DISK` environment variable to use the correct storage disk.

```php
<?php

namespace Domain\App\Http\Controllers\API\YourModule;

use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use Domain\App\Http\Controllers\ReactAdminBaseController;
use Domain\App\Models\YourModule\YourModel;

class YourModelController extends ReactAdminBaseController
{
    public $resource = 'your_model';
    public $requestValidator = YourModelRequest::class;
    // ... other properties

    public function __construct()
    {
        $this->model = YourModel::query();
    }

    public function _create($request)
    {
        $validated = app($this->requestValidator)->validated();

        // Create the model first
        $item = $this->model->create($validated);

        // Handle image upload after creation (so we have the item ID for the path)
        if ($request->hasFile('image') && $request->file('image')->isValid()) {
            $disk = env('MEDIA_DISK', 'public');
            $path = "img/your_models/{$item->id}";
            
            if ($disk === 's3') {
                // For S3, use store() without 'public/' prefix (no ACL issues)
                $imagePath = $request->file('image')->store($path, $disk);
                $item->image_path = $imagePath;
            } else {
                // For local storage, use storePublicly with 'public/' prefix
                $imagePath = $request->file('image')->storePublicly("public/{$path}", $disk);
                $item->image_path = str_replace('public/', '', $imagePath);
            }
            
            Log::info('Image uploaded', ['disk' => $disk, 'path' => $item->image_path]);
            $item->save();
        }

        return YourModelResource::make($item);
    }

    public function _update($request, $id, $item)
    {
        $validated = app($this->requestValidator)->validated();

        // Handle image upload - only update if a new file is provided
        if ($request->hasFile('image') && $request->file('image')->isValid()) {
            $disk = env('MEDIA_DISK', 'public');
            $path = "img/your_models/{$item->id}";
            
            if ($disk === 's3') {
                // For S3, use store() without 'public/' prefix
                $imagePath = $request->file('image')->store($path, $disk);
                $validated['image_path'] = $imagePath;
            } else {
                // For local storage, use storePublicly with 'public/' prefix
                $imagePath = $request->file('image')->storePublicly("public/{$path}", $disk);
                $validated['image_path'] = str_replace('public/', '', $imagePath);
            }
            
            Log::info('Image updated', ['disk' => $disk, 'path' => $validated['image_path']]);
        }

        $item->update($validated);

        return YourModelResource::make($item);
    }
}
```

### 5. Resource (API Response)

Include image-related fields in your API resource.

```php
<?php

namespace Domain\App\Http\Resources\YourModule;

use Illuminate\Http\Resources\Json\JsonResource;

class YourModelResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id'             => $this->id,
            // ... other fields
            'image_path'     => $this->image_path,
            'image_url'      => $this->image_url,
            'has_image'      => !is_null($this->image_path),
            'image_filename' => $this->image_path ? basename($this->image_path) : null,
        ];
    }
}
```

---

## Frontend Implementation

### 1. Create List View Component

This component displays a thumbnail in the data grid with hover-to-zoom functionality.

**File:** `packages/kt-ecommerce/src/components/YourModule/YourModelIconList.tsx`

```tsx
import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { IDashAutoAdminCustomFieldComponent } from 'dash-auto-admin';
import { ImagePlaceHolder } from 'kt-utils';
import { useRecordContext } from 'react-admin';
import { Box } from '@mui/material';

const ICON_SETTINGS = {
  THUMBNAIL: {
    WIDTH: 48,
    HEIGHT: 48,
    OBJECT_FIT: 'contain' as const
  },
  ZOOM: {
    WIDTH: 200,
    HEIGHT: 70,
    OBJECT_FIT: 'contain' as const,
    BACKDROP_COLOR: 'rgba(0, 0, 0, 0.5)',
    BORDER_RADIUS: '8px',
    ANIMATION_DURATION: 200
  },
  PORTAL: {
    Z_INDEX: 9999,
    OFFSET_X: 10,
    OFFSET_Y: 10
  }
} as const;

interface ZoomPortalProps {
  src: string;
  alt: string;
  label: string;
  mousePosition: { x: number; y: number };
  isVisible: boolean;
}

const ZoomPortal: React.FC<ZoomPortalProps> = ({ src, alt, label, mousePosition, isVisible }) => {
  if (!isVisible) return null;

  return createPortal(
    <div style={{
      position: 'fixed',
      left: mousePosition.x + ICON_SETTINGS.PORTAL.OFFSET_X,
      top: mousePosition.y + ICON_SETTINGS.PORTAL.OFFSET_Y,
      zIndex: ICON_SETTINGS.PORTAL.Z_INDEX,
      pointerEvents: 'none',
      opacity: isVisible ? 1 : 0,
      backgroundColor: ICON_SETTINGS.ZOOM.BACKDROP_COLOR,
      borderRadius: ICON_SETTINGS.ZOOM.BORDER_RADIUS,
      padding: '8px',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    }}>
      <img 
        src={src} 
        alt={alt} 
        style={{
          width: ICON_SETTINGS.ZOOM.WIDTH,
          height: ICON_SETTINGS.ZOOM.HEIGHT,
          objectFit: ICON_SETTINGS.ZOOM.OBJECT_FIT,
          borderRadius: ICON_SETTINGS.ZOOM.BORDER_RADIUS,
        }}
        draggable={false}
      />
      {label && (
        <div style={{
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          color: '#ffffff',
          fontSize: '12px',
          padding: '4px 8px',
          borderRadius: '4px',
          marginTop: '4px',
        }}>
          {label}
        </div>
      )}
    </div>,
    document.body
  );
};

const YourModelIconList: React.FC<IDashAutoAdminCustomFieldComponent> = ({ 
  method, 
  attribute, 
  resourceConfig 
}) => {
  const record = useRecordContext();
  const [isZooming, setIsZooming] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const imageRef = useRef<HTMLDivElement>(null);

  const iconUrl = record?.image_url;
  const itemName = record?.name;

  const handleMouseEnter = () => iconUrl && setIsZooming(true);
  const handleMouseLeave = () => setIsZooming(false);
  const handleMouseMove = (event: React.MouseEvent) => {
    setMousePosition({ x: event.clientX, y: event.clientY });
  };

  useEffect(() => {
    return () => setIsZooming(false);
  }, []);

  return (
    <>
      <div
        ref={imageRef}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onMouseMove={handleMouseMove}
        style={{ display: 'inline-block' }}
      >
        <ImagePlaceHolder
          placeHolder={
            <Box sx={{
              width: ICON_SETTINGS.THUMBNAIL.WIDTH,
              height: ICON_SETTINGS.THUMBNAIL.HEIGHT,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: '#f5f5f5',
              borderRadius: 1,
              border: '1px solid #e0e0e0',
            }}>
              <Box sx={{ fontSize: '10px', color: '#999', textAlign: 'center' }}>
                Sin imagen
              </Box>
            </Box>
          }
          src={iconUrl}
          style={{
            width: ICON_SETTINGS.THUMBNAIL.WIDTH,
            height: ICON_SETTINGS.THUMBNAIL.HEIGHT,
            objectFit: ICON_SETTINGS.THUMBNAIL.OBJECT_FIT,
            cursor: iconUrl ? 'zoom-in' : 'default',
          }}
          alt={itemName || 'Item icon'}
        />
      </div>
      
      {iconUrl && (
        <ZoomPortal
          src={iconUrl}
          alt={itemName || 'Item icon'}
          label={itemName || ''}
          mousePosition={mousePosition}
          isVisible={isZooming}
        />
      )}
    </>
  );
};

export default YourModelIconList;
```

### 2. Create Edit/Create Component

This component handles file upload with drag-and-drop support.

**File:** `packages/kt-ecommerce/src/components/YourModule/YourModelImage.tsx`

```tsx
import { IDashAutoAdminCustomFieldComponent } from "dash-auto-admin";
import React, { useState, useCallback } from "react";
import { useRecordContext } from "react-admin";
import { Box, Typography, Card, CardContent, CardHeader } from "@mui/material";
import { CloudUpload as CloudUploadIcon } from "@mui/icons-material";
import { useFormContext, useController } from "react-hook-form";

interface YourModelImageProps extends IDashAutoAdminCustomFieldComponent {}

const YourModelImageView: React.FC<YourModelImageProps> = ({ attribute }) => {
  const record = useRecordContext();
  
  if (!record || !record[attribute.listAttribute]) {
    return null;
  }

  return (
    <Box sx={{
      width: 300,
      height: 104,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#f5f5f5',
      borderRadius: 2,
      overflow: 'hidden',
    }}>
      <img
        src={record[attribute.listAttribute]}
        alt="Item Image"
        style={{ width: '100%', height: '100%', objectFit: 'contain' }}
      />
    </Box>
  );
};

const YourModelImageEdit: React.FC<YourModelImageProps> = ({ attribute }) => {
  const record = useRecordContext();
  const { setValue } = useFormContext();
  const { field } = useController({ name: attribute.attribute });
  
  const [isDragging, setIsDragging] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const currentImageUrl = record?.[attribute.listAttribute] || null;

  const processFile = useCallback((file: File) => {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'];
    if (!allowedTypes.includes(file.type)) {
      alert('Tipo de archivo no válido. Use JPEG, PNG, GIF, WebP o SVG.');
      return false;
    }

    if (file.size > 2 * 1024 * 1024) {
      alert('El archivo es demasiado grande. Máximo 2MB.');
      return false;
    }

    const preview = URL.createObjectURL(file);
    setPreviewUrl(preview);
    
    setValue(attribute.attribute, {
      rawFile: file,
      src: preview,
      title: file.name,
    });

    return true;
  }, [attribute.attribute, setValue]);

  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) processFile(file);
    event.target.value = '';
  }, [processFile]);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) processFile(file);
  }, [processFile]);

  React.useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const displayUrl = previewUrl || currentImageUrl;

  return (
    <Card sx={{ width: '100%' }}>
      <CardHeader title={attribute.label || "Imagen"} />
      <CardContent>
        <Box
          component="label"
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          sx={{
            width: 300,
            height: 104,
            border: isDragging ? '2px solid #1976d2' : displayUrl ? '1px solid #e0e0e0' : '2px dashed #ccc',
            borderRadius: 2,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: isDragging ? '#e3f2fd' : '#f5f5f5',
            overflow: 'hidden',
            position: 'relative',
            cursor: 'pointer',
            transition: 'all 0.2s ease-in-out',
            '&:hover': {
              backgroundColor: '#e8f4f8',
              borderColor: '#90caf9',
            }
          }}
        >
          {displayUrl ? (
            <>
              <img
                src={displayUrl}
                alt="Preview"
                style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
              />
              {isDragging && (
                <Box sx={{
                  position: 'absolute',
                  top: 0, left: 0, right: 0, bottom: 0,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  backgroundColor: 'rgba(25, 118, 210, 0.8)',
                  zIndex: 1,
                }}>
                  <CloudUploadIcon sx={{ fontSize: 48, color: 'white' }} />
                </Box>
              )}
            </>
          ) : (
            <Box display="flex" flexDirection="column" alignItems="center" gap={1}>
              <CloudUploadIcon sx={{ fontSize: 48, color: isDragging ? '#1976d2' : '#ccc' }} />
              <Typography variant="caption" color="textSecondary" textAlign="center">
                {isDragging ? 'Suelte la imagen aquí' : 'Arrastre una imagen o haga clic'}
              </Typography>
            </Box>
          )}
          <input
            type="file"
            hidden
            accept="image/jpeg,image/jpg,image/png,image/gif,image/webp,image/svg+xml"
            onChange={handleFileSelect}
          />
        </Box>

        <Box mt={2}>
          <Typography variant="caption" color="textSecondary" display="block">
            Formatos: JPEG, PNG, GIF, WebP, SVG
          </Typography>
          <Typography variant="caption" color="textSecondary" display="block">
            Tamaño máximo: 2MB
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

const YourModelImage = ({
  method,
  attribute,
  resourceConfig
}: IDashAutoAdminCustomFieldComponent) => {
  switch (method) {
    case 'edit':
    case 'create':
      return <YourModelImageEdit attribute={attribute} method={method} resourceConfig={resourceConfig} />;
    case 'view':
      return <YourModelImageView attribute={attribute} method={method} resourceConfig={resourceConfig} />;
  }
};

export default YourModelImage;
```

### 3. Update Schema

Add two entries to your schema - one for list view and one for edit/create.

**File:** `packages/kt-ecommerce/src/schemas/yourModel.ts`

```typescript
import { IDashAutoAdminAttribute } from "dash-auto-admin";
import YourModelImage from "../components/YourModule/YourModelImage";
import YourModelIconList from "../components/YourModule/YourModelIconList";

const yourModelSchema: IDashAutoAdminAttribute[] = [
  // List view - thumbnail with zoom
  {
    attribute: 'image_url',
    label: 'Imagen',
    type: "custom",
    component: YourModelIconList,
    inList: true,
    inEdit: false,
    inCreate: false,
    inShow: false
  },

  // ... other fields ...

  // Edit/Create view - upload component
  {
    attribute: "image",
    listAttribute: 'image_url',
    type: String,
    custom: true,
    component: YourModelImage,
    inList: false,
    label: "Imagen",
    processor: "File"
  },
];

export default yourModelSchema;
```

### 4. Update Resource Configuration

Ensure your resource config has `isFormData: true` to enable file uploads.

**File:** `packages/kt-ecommerce/src/resources/yourModelResource.tsx`

```typescript
import { IDashAutoAdminResourceConfig } from "dash-auto-admin";
import yourModelSchema from "../schemas/yourModel";

const yourModelResource: IDashAutoAdminResourceConfig = {
  // ... other config ...
  schema: yourModelSchema,
  
  // REQUIRED for file uploads
  isFormData: true,
  
  // Recommended settings
  mutationMode: "pessimistic",
  saveButtonAlwaysEnabled: true,
  refreshAfter: true,
};

export default yourModelResource;
```

### 5. Export Components

Add exports to your component index file.

**File:** `packages/kt-ecommerce/src/components/YourModule/index.ts`

```typescript
export { default as YourModelImage } from './YourModelImage';
export { default as YourModelIconList } from './YourModelIconList';
```

---

## File Storage Structure

### Local Storage (Development)

Images are stored in the following structure:

```
storage/app/public/
└── img/
    └── your_models/
        └── {model_id}/
            └── {random_filename}.{ext}
```

The `image_path` stored in the database is relative (e.g., `img/your_models/123/abc123.jpg`).

### S3 Storage (Production)

Images are stored in the S3 bucket:

```
s3://your-bucket/
└── img/
    └── your_models/
        └── {model_id}/
            └── {random_filename}.{ext}
```

The `image_path` stored in the database follows the same relative pattern.

### URL Generation

The `image_url` accessor returns the full URL based on the storage configuration:
- **Local storage:** `https://your-domain.com/api/storage/img/your_models/123/abc123.jpg`
- **S3 storage:** `https://your-bucket.s3.region.amazonaws.com/img/your_models/123/abc123.jpg`

---

## Storage Configuration: Local vs S3

### Overview

The Dash framework supports both local and S3 storage for uploaded images. The storage backend is controlled by the `MEDIA_DISK` environment variable:

| Environment | MEDIA_DISK | Storage Location |
|-------------|------------|------------------|
| Development | `public` | `storage/app/public/` (local filesystem) |
| Production | `s3` | AWS S3 bucket |

### Environment Configuration

#### Development (`.env.local` or `.env`)

```env
# Use local public disk for development
MEDIA_DISK=public
FILESYSTEM_DISK=local
```

#### Production (`.env.production`)

```env
# Use S3 for production
MEDIA_DISK=s3
FILESYSTEM_DISK=s3

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-2
AWS_BUCKET=your-bucket-name
AWS_URL=https://your-bucket-name.s3.us-east-2.amazonaws.com
```

### Filesystem Configuration

Ensure your `config/filesystems.php` has both disks configured:

```php
'disks' => [
    'public' => [
        'driver' => 'local',
        'root' => storage_path('app/public'),
        'url' => env('APP_URL').'/storage',
        'visibility' => 'public',
        'throw' => false,
    ],

    's3' => [
        'driver' => 's3',
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-2'),
        'bucket' => env('AWS_BUCKET'),
        'url' => env('AWS_URL'),
        'endpoint' => env('AWS_ENDPOINT'),
        'use_path_style_endpoint' => env('AWS_USE_PATH_STYLE_ENDPOINT', false),
        'throw' => false,
    ],
],
```

### Key Differences Between Local and S3

| Aspect | Local (`public`) | S3 |
|--------|------------------|----|
| **Storage method** | `storePublicly()` | `store()` |
| **Path prefix** | `public/` (stripped before saving) | None |
| **URL format** | Relative, needs `/api/storage/` prefix | Absolute S3 URL |
| **ACL** | Uses filesystem visibility | Bucket policy (no ACL) |
| **Symlink required** | Yes (`php artisan storage:link`) | No |

### Common Pitfalls

#### 1. Hardcoding the Disk

❌ **Wrong:**
```php
// Always uses local storage, ignores MEDIA_DISK config
$imagePath = $request->file('image')->storePublicly("public/img/...");
$url = Storage::disk('public')->url($this->image_path);
```

✅ **Correct:**
```php
// Respects MEDIA_DISK environment variable
$disk = env('MEDIA_DISK', 'public');
if ($disk === 's3') {
    $imagePath = $request->file('image')->store("img/...", $disk);
} else {
    $imagePath = $request->file('image')->storePublicly("public/img/...", $disk);
    $imagePath = str_replace('public/', '', $imagePath);
}

// URL generation
$url = Storage::disk($disk)->url($this->image_path);
```

#### 2. Using `storePublicly()` with S3

`storePublicly()` attempts to set ACL on the uploaded file. AWS S3 buckets with "Bucket Owner Enforced" object ownership will reject this. Use `store()` for S3:

```php
if ($disk === 's3') {
    // store() doesn't set ACL - works with Bucket Owner Enforced
    $imagePath = $file->store($path, $disk);
} else {
    // storePublicly() sets visibility - needed for local public access
    $imagePath = $file->storePublicly("public/{$path}", $disk);
}
```

#### 3. Forgetting the `public/` Prefix for Local Storage

Local storage requires the `public/` prefix for the symbolic link to work, but this prefix should be stripped before saving to the database:

```php
// Local storage: store with prefix, save without
$imagePath = $file->storePublicly("public/img/categories/{$id}", 'public');
$item->image_path = str_replace('public/', '', $imagePath);
// Saved as: img/categories/123/file.jpg
// Accessible via: /storage/img/categories/123/file.jpg
```

### Migrating Images from Local to S3

If you have existing images in local storage that need to be migrated to S3:

```php
// Migration script example
$disk = Storage::disk('public');
$s3 = Storage::disk('s3');

$models = YourModel::whereNotNull('image_path')->get();

foreach ($models as $model) {
    $path = $model->image_path;
    
    if ($disk->exists($path)) {
        // Copy to S3
        $s3->put($path, $disk->get($path));
        Log::info("Migrated: {$path}");
    }
}
```

**Note:** After changing `MEDIA_DISK` from `public` to `s3`, existing images uploaded to local storage will no longer be accessible. You must either migrate the images or re-upload them.

---

## Checklist

### Backend
- [ ] Migration with `image_path` column
- [ ] Model with `image_path` in `$fillable`
- [ ] Model with `image_url` in `$appends`
- [ ] Model with `imageUrl()` accessor
- [ ] Request validation for `image` field
- [ ] Controller `_create` method handles file upload
- [ ] Controller `_update` method handles file upload
- [ ] Resource includes `image_path`, `image_url`, `has_image`, `image_filename`

### Frontend
- [ ] List view component (thumbnail with zoom)
- [ ] Edit/Create component (drag-and-drop upload)
- [ ] Schema with two entries (`image_url` for list, `image` for edit)
- [ ] Resource config with `isFormData: true`
- [ ] Components exported in index file

---

## Reference Implementations

- **Category:** `domain/app/Models/ECommerce/Category.php` + `packages/kt-ecommerce/src/components/Category/`
- **SystemMarketplace:** `domain/app/Models/Marketplace/SystemMarketplace.php` + `packages/kt-ecommerce/src/components/`
