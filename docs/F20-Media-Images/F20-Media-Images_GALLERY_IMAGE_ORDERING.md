---
layout: default
title: F20-Media-Images GALLERY IMAGE ORDERING
---

# Gallery Image Ordering Feature

## Overview

This document describes the implementation of drag-and-drop image reordering functionality in the Gallery management system. Users can visually reorder images within a gallery, and the order persists across page reloads and sessions.

## Architecture

### Frontend Components

**Location**: `dash-frontend/apps/dash/src/components/ecommerce/Gallery/GalleryComponent.tsx`

The Gallery component uses `react-18-beautiful-dnd-grid` (ListManager) to provide drag-and-drop functionality for reordering images.

### Backend Components

**Key Files**:
- `dash-backend/domain/app/Http/Controllers/API/ECommerce/GalleryController.php`
- `dash-backend/domain/app/Http/Request/ECommerce/GalleryRequest.php`
- `dash-backend/domain/app/Models/ECommerce/Gallery.php`

**Storage**: Image order is stored in the `display_order` custom property within Spatie Media Library's `custom_properties` JSON column in the `media` table.

## Implementation Flow

### 1. Frontend: User Interaction

When a user drags an image to a new position:

```tsx
// GalleryComponent.tsx
const onDragEnd = (source, destination) => {
    if (destination === null || destination === undefined || destination === false)
        return;

    const original = galleryImages[source];
    const moved = galleryImages[destination];
    
    setGalleryImages((prevState) => {
        let aux = [...prevState];
        aux[destination] = original;
        aux[source] = moved;
        return aux;
    });
};
```

**What happens**: The component swaps the array positions of the dragged image and its destination, updating the local state immediately for instant visual feedback.

### 2. Frontend: State Synchronization

React's `useEffect` hook watches for changes to `galleryImages` and syncs the new order to the form:

```tsx
// GalleryComponent.tsx
useEffect(() => {
    if (gallery?.images) {
        // Send current image IDs
        currImages.field.onChange(galleryImages.map((item) => item.id));
        
        // Send image order with display_order values
        setValue("images_order", galleryImages.map((item, index) => ({
            id: item.id,
            display_order: index
        })));
    }
}, [galleryImages]);
```

**Result**: Creates an `images_order` array where each image gets its array index as its `display_order`:
```javascript
[
  { id: 9, display_order: 0 },
  { id: 8, display_order: 1 }
]
```

### 3. Frontend: Form Submission

Before sending to the backend, `formPostFormatter` converts the JavaScript objects to FormData format:

```tsx
// galleryResource.tsx
formPostFormatter(params, form) {
    if (params?.images_order && Array.isArray(params.images_order)) {
        form.delete("images_order[]");
        form.delete("images_order");
        
        params.images_order.forEach((orderItem, idx) => {
            if (orderItem && orderItem.id !== undefined && orderItem.display_order !== undefined) {
                form.append(`images_order[${idx}][id]`, orderItem.id.toString());
                form.append(`images_order[${idx}][display_order]`, orderItem.display_order.toString());
            }
        });
    }
    // ... handle other fields
    return form;
}
```

**FormData Output**:
```
images_order[0][id]=9
images_order[0][display_order]=0
images_order[1][id]=8
images_order[1][display_order]=1
```

**Why this format?** Laravel cannot parse JSON within FormData (which is required for file uploads). The indexed array notation `field[index][key]` is Laravel's standard way to receive nested arrays in FormData.

### 4. Backend: Request Validation

Laravel validates the incoming data structure:

```php
// GalleryRequest.php
public function rules()
{
    $rules = [
        // ... other rules
        'images_order' => 'sometimes|array',
        'images_order.*.id' => 'required|integer|exists:media,id',
        'images_order.*.display_order' => 'required|integer|min:0',
    ];
    return $rules;
}
```

**Validation ensures**:
- `images_order` is optional but must be an array if present
- Each item must have a valid `id` that exists in the `media` table
- Each item must have a `display_order` that's a non-negative integer

### 5. Backend: Update Display Order

The controller processes the validated data:

```php
// GalleryController.php _update method
if (isset($validated['images_order']) && is_array($validated['images_order'])) {
    Log::info("Updating image order for " . count($validated['images_order']) . " images");
    
    foreach ($validated['images_order'] as $orderData) {
        if (isset($orderData['id']) && isset($orderData['display_order'])) {
            $media = Media::find($orderData['id']);
            
            // Verify media belongs to this gallery
            if ($media && $media->model_id === $item->id) {
                $customProperties = $media->custom_properties;
                $customProperties['display_order'] = $orderData['display_order'];
                $media->custom_properties = $customProperties;
                $media->save();
                
                Log::info("Updated media ID {$media->id} display_order to {$orderData['display_order']}");
            }
        }
    }
}
```

**What happens**:
1. Loop through each item in `images_order`
2. Find the corresponding Media record by ID
3. Verify it belongs to the current gallery (security check)
4. Update the `display_order` in the `custom_properties` JSON column
5. Save the Media record

**Database Storage**: Spatie Media Library stores custom properties in the `media` table:
```sql
-- media table
custom_properties: {"display_order": 0, "is_primary": false}
```

### 6. Backend: Return Sorted Images

When fetching gallery images, they're automatically sorted by `display_order`:

```php
// Gallery.php Model
public function getImageUrlsLight()
{
    return $this->getMedia('gallery')
        ->sortBy(function ($media) {
            return $media->getCustomProperty('display_order', 0);
        })
        ->values()  // Reset array keys after sorting
        ->map(function ($media) {
            return [
                'id' => $media->id,
                'url' => $this->getAbsoluteMediaUrl($media, 'preview'),
            ];
        });
}
```

**Why `values()`?** After sorting, Laravel collections maintain original keys. The `values()` method resets the keys to 0, 1, 2... which is important for frontend array handling.

## Data Flow Diagram

```
┌─────────────────┐
│  User drags     │
│  image in UI    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ onDragEnd swaps │
│ array positions │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  useEffect      │
│  creates        │
│  images_order   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ formPost        │
│ Formatter       │
│ converts to     │
│ FormData        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Laravel         │
│ validates       │
│ request         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Controller      │
│ updates         │
│ display_order   │
│ in database     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Model returns   │
│ images sorted   │
│ by display_order│
└─────────────────┘
```

## Key Technical Decisions

### Why Custom Properties Instead of a Separate Column?

**Decision**: Store `display_order` in Spatie Media Library's `custom_properties` JSON column.

**Rationale**:
- Spatie Media Library provides built-in support for custom properties
- No need to extend the `media` table schema
- Flexible for future additions (can add more properties without migrations)
- Maintains encapsulation within the Media Library system

### Why FormData Indexed Notation?

**Decision**: Use `field[index][key]` notation instead of JSON stringification.

**Problem**: Laravel's FormData handling doesn't automatically parse JSON strings, and we need FormData for file uploads.

**Solution**: Use indexed array notation which Laravel natively parses:
```
images_order[0][id]=9          ✅ Laravel parses correctly
images_order[]={"id":9,...}    ❌ Becomes string "[object Object]"
```

### Why Sort on Read Instead of Database Ordering?

**Decision**: Sort images in the model's getter methods, not at database query level.

**Rationale**:
- `display_order` is stored in a JSON column, making SQL sorting complex
- Collection sorting in PHP is simpler and more maintainable
- Performance impact is minimal (galleries typically have < 50 images)
- Easier to add additional sorting logic later

## Testing the Feature

### Manual Testing Steps

1. **Navigate to Gallery Edit**:
   ```
   http://localhost:3000/#/ecommerce/gallery/{id}
   ```

2. **Verify Initial Order**:
   - Note the current order of images
   - Check the database: `SELECT id, custom_properties FROM media WHERE model_id = {gallery_id}`

3. **Drag and Drop**:
   - Drag the second image to the first position
   - Click "Save"

4. **Verify Persistence**:
   - Refresh the page
   - Images should maintain the new order
   - Check database again - `display_order` values should be updated

5. **API Response Check**:
   - Open browser DevTools > Network tab
   - Save gallery after reordering
   - Inspect response JSON - images array should reflect new order

### Expected Request Payload

```
POST /api/ecommerce/gallery/8
Content-Type: multipart/form-data

images_order[0][id]: 9
images_order[0][display_order]: 0
images_order[1][id]: 8
images_order[1][display_order]: 1
current_images[]: 9
current_images[]: 8
```

### Expected Response

```json
{
  "id": 8,
  "images": [
    {
      "id": 9,
      "url": "http://localhost/api/storage/galleries/8/conversions/img_9_preview.jpg"
    },
    {
      "id": 8,
      "url": "http://localhost/api/storage/galleries/8/conversions/img_8_preview.jpg"
    }
  ]
}
```

Note: Images are ordered by `display_order` (9 before 8), not by ID.

## Troubleshooting

### Images Return in Wrong Order

**Symptom**: After reordering and saving, images appear in original order on page refresh.

**Possible Causes**:
1. `display_order` not being saved to database
2. Model not sorting by `display_order`
3. Frontend caching old data

**Solution**:
```bash
# Check database
SELECT id, custom_properties FROM media WHERE model_id = {gallery_id};

# Verify display_order is present in custom_properties
# Example: {"display_order": 1, "is_primary": false}
```

### FormData Showing [object Object]

**Symptom**: Request payload shows `images_order[]: [object Object]`

**Cause**: `formPostFormatter` not properly serializing the objects.

**Solution**: Ensure `formPostFormatter` in `galleryResource.tsx` is using indexed notation:
```tsx
form.append(`images_order[${idx}][id]`, orderItem.id.toString());
form.append(`images_order[${idx}][display_order]`, orderItem.display_order.toString());
```

### Validation Errors

**Symptom**: Laravel returns 422 validation error for `images_order`.

**Cause**: Usually malformed data or missing validation rules.

**Solution**: Check `GalleryRequest.php` has correct rules:
```php
'images_order' => 'sometimes|array',
'images_order.*.id' => 'required|integer|exists:media,id',
'images_order.*.display_order' => 'required|integer|min:0',
```

## Future Enhancements

### Bulk Reordering
Currently reorders all images on every save. Could optimize to only update changed positions:
```php
// Compare old vs new display_order
if ($media->getCustomProperty('display_order') !== $orderData['display_order']) {
    // Only update if changed
}
```

### Drag Preview
Add visual feedback during drag operation showing where image will land.

### Auto-numbering
When images are deleted, automatically renumber remaining images to eliminate gaps in `display_order` sequence.

### Database Indexing
If galleries grow large (>100 images), consider adding a dedicated `display_order` column with an index for faster sorting.

## Related Files

### Frontend
- `dash-frontend/apps/dash/src/components/ecommerce/Gallery/GalleryComponent.tsx` - Main gallery component with drag-drop
- `dash-frontend/apps/dash/src/resources/ecommerce/galleryResource.tsx` - Gallery resource configuration
- `dash-frontend/apps/dash/src/schemas/ecommerce/gallery.tsx` - Gallery schema definition

### Backend
- `dash-backend/domain/app/Http/Controllers/API/ECommerce/GalleryController.php` - Gallery controller
- `dash-backend/domain/app/Http/Request/ECommerce/GalleryRequest.php` - Request validation
- `dash-backend/domain/app/Models/ECommerce/Gallery.php` - Gallery model
- `dash-backend/domain/app/Http/Resources/ECommerce/GalleryResource.php` - API response formatting

## Dependencies

### Frontend
- `react-18-beautiful-dnd-grid` - Drag and drop grid component (ListManager)
- `react-hook-form` - Form state management
- `@mui/material` - UI components (ImageList, ImageListItem)

### Backend
- `spatie/laravel-medialibrary` - Media management and custom properties
- Laravel 10.x - Framework with FormRequest validation
