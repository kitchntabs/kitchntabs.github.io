# Tenant Image Drag & Drop Feature

## Overview

This document describes the implementation of drag-and-drop functionality for tenant images (banner, horizontal logo, and squared logo). Users can now drag image files directly onto the upload areas, in addition to clicking to browse files.

## Features

### Image Types & Collections

The Tenant model manages three types of images via Spatie Media Library:

1. **Banner** (`banner_images`)
   - Collection: `banner`
   - Dimensions: 200x200px (display size)
   - Aspect Ratio: 1:1
   - Endpoint: `/tenant/tenant/{id}/upload-banner`

2. **Horizontal Logo** (`horizontal_logo_images`)
   - Collection: `horizontal_logo`
   - Dimensions: 230x80px (display size)
   - Aspect Ratio: 23:8
   - Endpoint: `/tenant/tenant/{id}/upload-horizontal-logo`

3. **Squared Logo** (`squared_logo_images`)
   - Collection: `squared_logo`
   - Dimensions: 80x80px (display size)
   - Aspect Ratio: 1:1
   - Endpoint: `/tenant/tenant/{id}/upload-squared-logo`

### Image Conversions

Each image type has specific conversions generated automatically:

**Banner Conversions:**
- `banner-preview`: 512x512px (cropped)
- `banner-medium`: 1024x1024px (cropped)
- `banner-large`: Original size (optimized)

**Horizontal Logo Conversions:**
- `horizontal-preview`: 230x80px (cropped)
- `horizontal-medium`: 600x100px (cropped)

**Squared Logo Conversions:**
- `squared-preview`: 80x80px (cropped)
- `squared-medium`: 200x200px (cropped)

## Implementation

### Frontend Component: TenantImage.tsx

**Location**: `dash-frontend/apps/dash/src/components/ecommerce/TenantImage.tsx`

#### Key Changes

1. **Added Drag State Management**
```tsx
const [isDragging, setIsDragging] = useState(false);
```

2. **File Processing Function**
```tsx
const processFile = useCallback((file: File) => {
  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
  if (!allowedTypes.includes(file.type)) {
    notify('Tipo de archivo no válido. Use JPEG, PNG, GIF o WebP.', { type: 'error' });
    return false;
  }

  // Validate file size (2MB)
  if (file.size > 2 * 1024 * 1024) {
    notify('El archivo es demasiado grande. Máximo 2MB.', { type: 'error' });
    return false;
  }

  // Create preview URL
  const previewUrl = URL.createObjectURL(file);
  setPreviewImage(previewUrl);
  setSelectedFile(file);
  return true;
}, [notify]);
```

3. **Drag Event Handlers**
```tsx
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
  if (file) {
    processFile(file);
  }
}, [processFile]);
```

4. **Enhanced UI for Empty State**
{% raw %}
```tsx
<Box
  onDragEnter={handleDragEnter}
  onDragLeave={handleDragLeave}
  onDragOver={handleDragOver}
  onDrop={handleDrop}
  sx={{
    border: isDragging ? '2px solid #1976d2' : '2px dashed #ccc',
    backgroundColor: isDragging ? '#e3f2fd' : '#f5f5f5',
    cursor: 'pointer',
    transition: 'all 0.2s ease-in-out',
    '&:hover': {
      backgroundColor: '#e8f4f8',
      borderColor: '#90caf9',
    }
  }}
>
  <CloudUploadIcon sx={{ fontSize: 48, color: isDragging ? '#1976d2' : '#ccc' }} />
  <Typography>
    {isDragging ? 'Suelte la imagen aquí' : 'Arrastre una imagen o haga clic'}
  </Typography>
</Box>
```
{% endraw %}

5. **Enhanced UI for Existing Image State**
{% raw %}
```tsx
<Box
  onDragEnter={handleDragEnter}
  onDragLeave={handleDragLeave}
  onDragOver={handleDragOver}
  onDrop={handleDrop}
  sx={{
    border: isDragging ? '2px solid #1976d2' : '1px solid #e0e0e0',
    backgroundColor: isDragging ? '#e3f2fd' : '#f5f5f5',
    cursor: 'pointer',
    transition: 'all 0.2s ease-in-out',
  }}
>
  <img src={currentImageUrl} alt="Current Image" />
  {isDragging && (
    <Box sx={{ position: 'absolute', backgroundColor: 'rgba(25, 118, 210, 0.8)' }}>
      <CloudUploadIcon sx={{ fontSize: 48, color: 'white' }} />
    </Box>
  )}
</Box>
```
{% endraw %}

### Backend: Tenant Model

**Location**: `dash-backend/app/Models/Tenant.php`

#### Media Collections Configuration

```php
public function registerMediaCollections(): void
{
    $this->addMediaCollection('banner')
        ->acceptsMimeTypes(['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'])
        ->singleFile()
        ->useDisk(env('MEDIA_DISK', 'public'));

    $this->addMediaCollection('horizontal_logo')
        ->acceptsMimeTypes(['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'])
        ->singleFile()
        ->useDisk(env('MEDIA_DISK', 'public'));

    $this->addMediaCollection('squared_logo')
        ->acceptsMimeTypes(['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'])
        ->singleFile()
        ->useDisk(env('MEDIA_DISK', 'public'));
}
```

#### Image Update Method

```php
public function updateImage($requestKey, $collection)
{
    // Clear existing media first (with S3 error handling)
    try {
        $this->clearMediaCollection($collection);
    } catch (\Exception $e) {
        // Handle S3 errors gracefully
        $this->getMedia($collection)->each(function ($media) {
            $media->forceDelete();
        });
    }

    // Add new media
    if (request()->hasFile($requestKey)) {
        $media = $this->addMediaFromRequest($requestKey)
            ->toMediaCollection($collection);
    }
}
```

### Backend: TenantController

**Location**: `dash-backend/app/Http/Controllers/API/System/TenantController.php`

#### Upload Endpoints

```php
public function uploadBanner(Request $request, $id)
{
    $request->validate([
        'banner' => 'required|image|mimes:jpeg,jpg,png,gif,webp|max:2048'
    ]);

    $tenant = Tenant::findOrFail($id);
    $tenant->updateImage('banner', 'banner');
    
    return $this->_postGetOne($tenant->fresh());
}

public function uploadHorizontalLogo(Request $request, $id)
{
    $request->validate([
        'horizontal_logo' => 'required|image|mimes:jpeg,jpg,png,gif,webp|max:2048'
    ]);

    $tenant = Tenant::findOrFail($id);
    $tenant->updateImage('horizontal_logo', 'horizontal_logo');
    
    return $this->_postGetOne($tenant->fresh());
}

public function uploadSquaredLogo(Request $request, $id)
{
    $request->validate([
        'squared_logo' => 'required|image|mimes:jpeg,jpg,png,gif,webp|max:2048'
    ]);

    $tenant = Tenant::findOrFail($id);
    $tenant->updateImage('squared_logo', 'squared_logo');
    
    return $this->_postGetOne($tenant->fresh());
}
```

## User Experience Flow

### Uploading via Drag & Drop

1. **User navigates** to tenant configuration page
2. **Sees three image sections**: Banner, Horizontal Logo, Squared Logo
3. **For each section**:
   - If no image exists: Shows dashed border with upload icon
   - If image exists: Shows current image with hover effect

4. **User drags image file** over an upload area:
   - Border changes to solid blue
   - Background changes to light blue
   - Text changes to "Suelte la imagen aquí"
   - Upload icon turns blue

5. **User drops image**:
   - File is validated (type and size)
   - Preview appears with confirmation buttons (✓ and ✗)
   - User can confirm or cancel

6. **User confirms upload**:
   - Image uploads to backend via FormData
   - Backend saves to media collection
   - Generates conversions automatically
   - Returns updated tenant data
   - Frontend refreshes and shows new image

### Uploading via Click

1. **User clicks** on upload area or upload button
2. **File browser opens**
3. **User selects image file**
4. **Same validation and preview flow** as drag & drop

### Deleting Images

1. **User sees delete button** on existing images
2. **Clicks delete**
3. **Backend removes** media from storage and database
4. **Frontend updates** to show empty state

## Validation Rules

### File Type
- Allowed: JPEG, JPG, PNG, GIF, WebP
- Error message: "Tipo de archivo no válido. Use JPEG, PNG, GIF o WebP."

### File Size
- Maximum: 2MB (2048KB)
- Error message: "El archivo es demasiado grande. Máximo 2MB."

### Image Dimensions
- No strict minimum/maximum enforced
- Conversions will crop/resize as needed
- Recommended: Upload high-resolution images (at least 1000px width)

## Storage Configuration

### Local Storage (Development)
```env
MEDIA_DISK=public
```
- Files stored in: `storage/app/public/`
- Accessible via: `http://domain/storage/...`

### S3 Storage (Production)
```env
MEDIA_DISK=s3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=...
AWS_BUCKET=...
```

### Error Handling

The system gracefully handles S3 errors:
```php
try {
    $this->clearMediaCollection($collection);
} catch (\Exception $e) {
    if (str_contains($e->getMessage(), 'S3Exception')) {
        // Log warning but continue
        $this->getMedia($collection)->each(function ($media) {
            $media->forceDelete(); // Remove DB records only
        });
    }
}
```

## API Responses

### Successful Upload Response
```json
{
  "id": 1,
  "name": "Tenant Name",
  "images": {
    "banner": {
      "original": "https://domain/storage/1/banner.jpg"
    },
    "horizontal_logo": {
      "original": "https://domain/storage/1/horizontal_logo.jpg"
    },
    "squared_logo": {
      "original": "https://domain/storage/1/squared_logo.jpg"
    }
  }
}
```

### Empty Image State
```json
{
  "id": 1,
  "name": "Tenant Name",
  "images": {
    "banner": [],
    "horizontal_logo": [],
    "squared_logo": []
  }
}
```

## Browser Compatibility

The drag-and-drop feature uses standard HTML5 Drag and Drop API:

- ✅ Chrome 4+
- ✅ Firefox 3.5+
- ✅ Safari 3.1+
- ✅ Edge 12+
- ✅ Opera 12+

## Testing

### Manual Testing Steps

1. **Test Empty State Drag & Drop**:
   - Navigate to tenant configuration
   - Drag a valid image over banner area
   - Verify visual feedback (blue border, background change)
   - Drop image
   - Verify preview appears
   - Confirm upload
   - Verify image displays correctly

2. **Test Existing Image Drag & Drop**:
   - With an image already uploaded
   - Drag a new image over existing image
   - Verify overlay appears during drag
   - Drop image
   - Verify new preview replaces old image preview
   - Confirm upload
   - Verify new image displays

3. **Test Click Upload**:
   - Click upload button
   - Select image from file browser
   - Verify same flow as drag & drop

4. **Test Validation**:
   - Try uploading a PDF file (should fail)
   - Try uploading a 5MB image (should fail)
   - Verify error notifications appear

5. **Test All Three Image Types**:
   - Repeat above tests for banner, horizontal logo, and squared logo
   - Verify each maintains its own state independently

6. **Test Image Deletion**:
   - Upload image
   - Click delete button
   - Verify image is removed
   - Verify empty state returns

## Known Limitations

1. **Single File Only**: Each collection only accepts one file. Dragging multiple files will only process the first one.

2. **No Cropping Tool**: Images are automatically cropped to conversions. No manual cropping interface is provided.

3. **No Progress Bar**: For small images (< 2MB), upload is fast enough that a progress bar isn't necessary. For larger files, consider adding one.

4. **Mobile Limitations**: Drag and drop doesn't work on mobile devices. The click-to-upload fallback works universally.

## Future Enhancements

### Image Cropping Tool
Add a client-side cropping interface before upload:
```tsx
import Cropper from 'react-easy-crop';

// Allow user to select crop area
// Generate cropped blob
// Upload cropped image
```

### Multiple Sizes Preview
Show all conversion sizes after upload:
```tsx
<Stack direction="row" spacing={1}>
  <img src={images.preview} alt="Preview" />
  <img src={images.medium} alt="Medium" />
  <img src={images.large} alt="Large" />
</Stack>
```

### Batch Upload
Allow uploading all three images at once:
```tsx
// Upload banner, horizontal_logo, and squared_logo in single request
formData.append('banner', bannerFile);
formData.append('horizontal_logo', horizontalLogoFile);
formData.append('squared_logo', squaredLogoFile);
```

### Upload Progress
For larger images or slower connections:
```tsx
const [uploadProgress, setUploadProgress] = useState(0);

axios.post(url, formData, {
  onUploadProgress: (progressEvent) => {
    const percentCompleted = Math.round(
      (progressEvent.loaded * 100) / progressEvent.total
    );
    setUploadProgress(percentCompleted);
  }
});
```

## Related Files

### Frontend
- `dash-frontend/apps/dash/src/components/ecommerce/TenantImage.tsx` - Main component with drag & drop
- `dash-frontend/apps/dash/src/schemas/ecommerce/tenant_tenant.tsx` - Schema configuration
- `dash-frontend/apps/dash/src/resources/ecommerce/ecommerceTenantResource.tsx` - Resource configuration

### Backend
- `dash-backend/app/Models/Tenant.php` - Tenant model with media collections
- `dash-backend/app/Http/Controllers/API/System/TenantController.php` - Upload endpoints
- `dash-backend/app/Http/Resources/TenantResource.php` - API response formatting

## Dependencies

### Frontend
- `@mui/material` - UI components (Box, Button, Typography, etc.)
- `@mui/icons-material` - Icons (CloudUpload, Delete, etc.)
- `react-admin` - Data management (useNotify, useRefresh, etc.)
- `dash-axios-hook` - HTTP client for API calls

### Backend
- `spatie/laravel-medialibrary` - Media management
- `spatie/image` - Image processing and conversions
- Laravel 10.x - Framework with validation and file handling
