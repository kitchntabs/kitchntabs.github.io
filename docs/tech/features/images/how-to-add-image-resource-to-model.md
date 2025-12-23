# How to Add an Image Resource to a Model Using HandlesImageUploads

This guide describes the requirements and process to add an image (or icon) upload and serving capability to a Laravel Eloquent model using the `HandlesImageUploads` trait.

---

## Requirements

- The model must have a column to store the image path (e.g., `image_path`, `icon_path`).
- The model should have an accessor to generate the public URL for the image.
- The controller handling create/update must use the `HandlesImageUploads` trait and call its methods.
- The request class should validate the image input.
- The resource class should expose the image URL.

---

## Step-by-Step Process

### 1. Add the Image Path Column

Add a column to your model's migration (e.g., `image_path` or `icon_path`).

```php
$table->string('image_path')->nullable();
```

### 2. Update the Model

- Add the image path to `$fillable`.
- Add an accessor for the image URL (see Brand or SystemPointOfSale for examples).
- Optionally, add the image URL to `$appends`.

```php
protected $fillable = [
    // ...existing fields...
    'image_path',
];

protected $appends = ['image_url'];

protected function imageUrl(): Attribute
{
    return Attribute::make(
        get: function () {
            $path = $this->image_path ?: '';
            $disk = config('app.media_disk', config('filesystems.default', 'public'));
            if (!$path) {
                return null;
            }
            if ($disk !== 'public') {
                return \Illuminate\Support\Facades\Storage::disk($disk)->url($path);
            }
            return url(str_replace('public', 'storage', $path));
        }
    );
}
```

### 3. Update the Request Class

- Add validation rules for the image field.

```php
'image' => 'nullable|image|max:2048|mimes:png,jpg,jpeg',
```

- Optionally, handle special cases (e.g., base64, nested file arrays) in `prepareForValidation()`.

### 4. Update the Controller

- Use the `HandlesImageUploads` trait.
- In `_create` and `_update`, call `$this->handleImageUpload(...)` to process the image upload.
- Store the returned path in the model's image path field.

```php
use App\Traits\HandlesImageUploads;

$upload = $this->handleImageUpload($request, $validated, $tenantId, 'resource_name', 'image_path', 'image');
$validated['image_path'] = $upload && $upload['path'] ? $upload['path'] : null;
```

### 5. Update the Resource Class

- Expose the image URL (either via accessor or directly).

```php
'image_url' => $this->image_url,
```

---

## Example

See the implementation in:

- `Brand` model, controller, request, and resource.
- `SystemPointOfSale` model, controller, request, and resource.

---

## Storage Disk Configuration

### Local Development (MEDIA_DISK=local)

When using local storage, files are stored in `storage/app/` and served through a custom FileController endpoint.

**Environment Configuration:**
```env
MEDIA_DISK=local
FILESYSTEM_DISK=local
APP_URL=https://api.kitchntabs.com
```

**How It Works:**
1. Files are stored in: `storage/app/img/resource_name/tenant_id/filename.jpg`
2. URLs are generated as: `https://api.kitchntabs.com/api/storage/img/resource_name/tenant_id/filename.jpg`
3. Requests are handled by `FileController@serve` which reads files from `storage/app/`
4. No symlink required - files are served directly through the controller

**FileController Setup:**

The `FileController` is located at `app/Http/Controllers/API/FileController.php` and serves files from storage:

```php
namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\HttpFoundation\StreamedResponse;

class FileController extends Controller
{
    public function serve(string $path)
    {
        $path = urldecode($path);
        $disk = config('filesystems.default', 'local');
        
        if (!Storage::disk($disk)->exists($path)) {
            abort(404, 'File not found');
        }
        
        $file = Storage::disk($disk)->get($path);
        $mimeType = Storage::disk($disk)->mimeType($path);
        
        return response($file, 200)->header('Content-Type', $mimeType);
    }
}
```

**Route Configuration (routes/api.php):**
```php
Route::get('/api/storage/{path}', [FileController::class, 'serve'])
    ->where('path', '.*')
    ->name('storage.serve');
```

**Benefits:**
- Works immediately without symlinks
- Can add authentication/authorization later if needed
- Serves files from any path in `storage/app/`
- Returns proper Content-Type headers
- Works seamlessly with ngrok tunneling

### Production (MEDIA_DISK=s3)

When using S3, files are stored in AWS S3 buckets and served directly from S3 URLs.

**Environment Configuration:**
```env
MEDIA_DISK=s3
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-2
AWS_BUCKET=your-bucket-name
AWS_URL=https://your-bucket.s3.region.amazonaws.com
AWS_ENDPOINT=https://s3.region.amazonaws.com
```

**How It Works:**
1. Files are uploaded directly to S3: `s3://bucket-name/img/resource_name/tenant_id/filename.jpg`
2. URLs are generated using S3's public URL: `https://bucket-name.s3.region.amazonaws.com/img/...`
3. Files are served directly from S3 (no Laravel processing)
4. Can use CloudFront CDN for better performance

**S3 Bucket Configuration Requirements:**
- Set proper CORS policies to allow frontend access
- Configure bucket policies for public read access (if needed)
- Set up lifecycle policies for automatic cleanup of old files
- Consider using CloudFront distribution for better global performance

### DashFileStorage Trait Behavior

The `DashFileStorage` trait automatically handles both storage types:

```php
public function getFileUrl(string $filename, string $path = '', ?int $tenantId = null): ?string
{
    if (!$filename) {
        return null;
    }

    $disk = $this->getStorageDisk();
    $tenantId = $tenantId ?? $this->getTenantId();
    $fullPath = $this->getStoragePath($path, $tenantId) . $filename;

    if (!Storage::disk($disk)->exists($fullPath)) {
        return null;
    }

    if ($disk === 's3') {
        // For S3, Storage::url() will return the full S3 URL
        return Storage::disk($disk)->url($fullPath);
    } else {
        // For local storage, return a public URL via our FileController
        // This serves files from storage/app/ through /api/storage/ endpoint
        return url('/api/storage/' . $fullPath);
    }
}
```

### Switching Between Environments

To switch between local and S3 storage, simply update your `.env` file:

**For Local Development:**
```env
MEDIA_DISK=local
FILESYSTEM_DISK=local
```

**For Production:**
```env
MEDIA_DISK=s3
FILESYSTEM_DISK=s3
```

The application code remains the same - the trait handles the differences automatically.

## Notes

- The `DashFileStorage` trait supports both local and S3 storage automatically
- For local storage, files are stored in `storage/app/` and served via `/api/storage/` endpoint
- For S3, files are uploaded to S3 and full public URLs are returned
- No storage symlink required for local development - `FileController` handles serving files
- The `handleImageUpload` method returns an array with both `path` and `url` keys
- Always log file uploads for easier debugging
- Frontend frameworks like React Admin may wrap file uploads in nested structures
- The same codebase works for both local development (ngrok) and production (S3)
- Consider adding authentication middleware to the storage route if files should be protected

---
