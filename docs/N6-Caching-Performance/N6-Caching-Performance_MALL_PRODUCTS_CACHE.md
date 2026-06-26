# Mall Products Server-Side Caching

This document explains the server-side caching implementation for Mall Products API to handle multiple requests efficiently.

## Features Implemented

### 1. Automatic Caching in ReactAdminBaseController
- Added caching to the `getList()` method for both paginated and non-paginated requests
- Uses Laravel's `Cache::remember()` with configurable duration
- Generates intelligent cache keys based on controller, method, and request parameters

### 2. Mall-Specific Cache Key Generation
- `MallProductController` overrides cache key generation to include:
  - `mall_id` parameter
  - `tenant_ids` parameter
  - Pagination parameters (`page`, `perPage`)
  - All query filters

### 3. Configuration
- Cache duration is configurable via environment variable:
  ```env
  CACHE_GET_LIST_IN_SECONDS=300  # 5 minutes default
  ```
- Located in `config/constants.php`

### 4. Cache Management
- Cache can be disabled per controller instance using `$this->disableCache()`
- Manual cache clearing endpoint available

## API Endpoints

### Get Products (Cached)
```
GET /api/public/mall/products?mall_id=1&page=1&perPage=50
```

### Clear Cache
```
DELETE /api/public/mall/products/cache/clear?mall_id=1
```

## Cache Key Format
```
react_admin_MallProductController_getList_paginated_{hash}
```

The hash includes:
- mall_id
- tenant_ids
- page
- perPage
- All filter parameters
- Load options (load_gallery, load_modifier_groups, etc.)

## Logging
Cache operations are logged with the following information:
- Cache key generated
- Cache enabled/disabled status
- Cache duration
- Mall ID and tenant information

## Testing the Cache

### 1. Enable Caching (Default)
The cache is enabled by default. Multiple requests to the same endpoint with identical parameters will be served from cache.

### 2. Disable Caching for Testing
In `MallProductController::__construct()`, uncomment:
```php
$this->disableCache();
```

### 3. Monitor Cache Performance
Check Laravel logs for entries like:
```
[INFO] Mall products cache info: {
    "cache_key": "react_admin_MallProductController_getList_paginated_abc123",
    "cache_enabled": true,
    "cache_duration": 300
}
```

### 4. Clear Cache Manually
```bash
# Clear cache for specific mall
curl -X DELETE "http://your-api-url/api/public/mall/products/cache/clear?mall_id=1"

# Or clear all Laravel cache
php artisan cache:clear
```

## Environment Variables

Add to your `.env` file:
```env
# Cache duration for products list (seconds)
CACHE_GET_LIST_IN_SECONDS=300

# Existing cache settings
CACHE_FOR_SELECTS_IN_SECONDS=14400
CACHE_GET_MANY_IN_SECONDS=14400
```

## Performance Benefits

With this caching implementation:
- Multiple identical requests within 5 minutes return cached results
- Database queries are reduced significantly
- Response times improve for repeated requests
- Server load decreases during high traffic periods

## Cache Invalidation Strategy

Currently, the cache uses time-based expiration (5 minutes default). For more advanced scenarios, consider:
- Event-based cache invalidation when products are updated
- Cache tagging for more granular cache clearing
- Redis cache driver for better performance in production

## Notes

- Cache keys include all relevant parameters to ensure data consistency
- The cache respects all existing filtering and relationship loading
- Pagination is properly cached per page
- Mall-specific isolation prevents data leakage between different malls
