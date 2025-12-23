# Mall React Query Caching System

## Technical Documentation

**Version:** 1.0  
**Last Updated:** December 15, 2025  
**Author:** Development Team

---

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution Architecture](#solution-architecture)
4. [Key Components](#key-components)
5. [Implementation Details](#implementation-details)
6. [Configuration](#configuration)
7. [Usage Examples](#usage-examples)
8. [Flow Diagrams](#flow-diagrams)
9. [Debugging Guide](#debugging-guide)
10. [Best Practices](#best-practices)

---

## Overview

The Mall React Query Caching System is an optimization layer built on top of TanStack Query (React Query) that provides intelligent caching, request deduplication, and efficient data synchronization for the KitchnTabs Mall ordering application.

### Key Features

- **Request Deduplication**: Multiple components requesting the same data result in a single API call
- **Intelligent Caching**: Data is cached for configurable periods (default: 10 minutes)
- **Automatic Synchronization**: UI components react to cache changes without additional API calls
- **Hash-Based Change Detection**: Efficient detection of actual data changes vs. reference changes
- **Dual Pagination Support**: Handles both horizontal carousel and infinite scroll modes

---

## Problem Statement

### Original Issues

Before implementing this system, the mall ordering interface suffered from several performance issues:

1. **Duplicate API Requests**: When selecting a store, 3+ identical requests were made to fetch products
2. **No Request Deduplication**: Each component made its own API calls independently
3. **No Caching**: Every navigation or store selection triggered fresh API calls
4. **UI Update Failures**: When switching stores, the product list wouldn't update because of shallow comparison logic

### Impact

- Increased server load
- Slower user experience
- Unnecessary bandwidth consumption
- Poor mobile performance

---

## Solution Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MALL CACHING ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌────────────────────────────────────────────────────────────────────┐    │
│   │                      React Components                               │    │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
│   │  │MallStoresList│  │MallProductGrid│ │MallOrderCreateContext   │  │    │
│   │  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘  │    │
│   │         │                 │                       │                 │    │
│   └─────────┼─────────────────┼───────────────────────┼─────────────────┘    │
│             │                 │                       │                      │
│             ▼                 ▼                       ▼                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    Custom React Query Hooks                          │   │
│   │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐   │   │
│   │  │  useMallStores   │  │  useMallProducts │  │ useMallPrefetch │   │   │
│   │  └────────┬─────────┘  └────────┬─────────┘  └────────┬────────┘   │   │
│   │           │                     │                     │             │   │
│   └───────────┼─────────────────────┼─────────────────────┼─────────────┘   │
│               │                     │                     │                  │
│               ▼                     ▼                     ▼                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      TanStack Query Cache                            │   │
│   │                                                                      │   │
│   │  Query Keys:                                                        │   │
│   │  ┌────────────────────────────────────────────────────────────┐    │   │
│   │  │ ['mall', 'stores', { mall_id }]                            │    │   │
│   │  │ ['mall', 'products', { mall_id, tenant_id?, featured? }]   │    │   │
│   │  └────────────────────────────────────────────────────────────┘    │   │
│   │                                                                      │   │
│   │  Cache Config: staleTime=10min, gcTime=15min                        │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         Backend API                                  │   │
│   │  GET /public/mall/stores?mall_id=X                                  │   │
│   │  GET /public/mall/products?mall_id=X&tenant_id=Y                    │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. useMallDataQueries.ts

**Location:** `dash-frontend/apps/kitchntabs-mall/src/kt-mall/hooks/useMallDataQueries.ts`

This is the core module that provides React Query hooks for mall data fetching.

#### Exports

| Export | Type | Description |
|--------|------|-------------|
| `MALL_CACHE_CONFIG` | Object | Cache configuration constants |
| `useMallStores()` | Hook | Fetches and caches store/tenant data |
| `useMallProducts()` | Hook | Fetches and caches product data |
| `useMallPrefetch()` | Hook | Prefetches data for performance |

### 2. MallOrderCreateContext.tsx

**Location:** `dash-frontend/apps/kitchntabs-mall/src/kt-mall/contexts/MallOrderCreateContext.tsx`

The main context that:
- Consumes React Query hooks
- Manages pagination state (carousel pages)
- Handles store/product selection
- Synchronizes UI with cached data using hash-based comparison

### 3. MallProductGrid.tsx

**Location:** `dash-frontend/apps/kitchntabs-mall/src/kt-mall/components/MallProductGrid.tsx`

The UI component that renders products in either:
- **Horizontal mode**: Carousel with pagination arrows
- **Infinite mode**: Vertical grid with infinite scroll

---

## Implementation Details

### Cache Configuration

```typescript
// useMallDataQueries.ts

export const MALL_CACHE_CONFIG = {
    staleTime: 10 * 60 * 1000,      // 10 minutes - data considered fresh
    gcTime: 15 * 60 * 1000,         // 15 minutes - garbage collection time
    refetchOnWindowFocus: false,    // Don't refetch when window regains focus
    refetchOnMount: false,          // Don't refetch when component mounts
};
```

#### Configuration Explained

| Property | Value | Purpose |
|----------|-------|---------|
| `staleTime` | 10 minutes | Data won't trigger refetch for 10 minutes |
| `gcTime` | 15 minutes | Unused cache entries removed after 15 minutes |
| `refetchOnWindowFocus` | false | Prevents refetch when user returns to tab |
| `refetchOnMount` | false | Uses cached data instead of refetching |

### Query Key Structure

Query keys are structured arrays that uniquely identify cached data:

```typescript
// Stores query key
['mall', 'stores', { mall_id: 123 }]

// Products query key (all products)
['mall', 'products', { mall_id: 123, tenant_id: null, featured: false }]

// Products query key (specific store)
['mall', 'products', { mall_id: 123, tenant_id: 456, featured: false }]

// Products query key (featured only)
['mall', 'products', { mall_id: 123, tenant_id: null, featured: true }]
```

### useMallStores Hook

```typescript
export function useMallStores() {
    const mallId = useMallId();
    const dataProvider = useDataProvider();

    return useQuery({
        queryKey: ['mall', 'stores', { mall_id: mallId }],
        queryFn: async () => {
            console.log('🏪 [useMallStores] Fetching stores for mall:', mallId);
            const response = await dataProvider.getList('stores', {
                pagination: { page: 1, perPage: 100 },
                sort: { field: 'name', order: 'ASC' },
                filter: { mall_id: mallId },
            });
            console.log('🏪 [useMallStores] Fetched:', response.data?.length, 'stores');
            return response;
        },
        enabled: !!mallId,
        ...MALL_CACHE_CONFIG,
    });
}
```

### useMallProducts Hook

```typescript
export function useMallProducts(options?: MallProductsOptions) {
    const { tenantId = null, featured = false } = options || {};
    const mallId = useMallId();
    const dataProvider = useDataProvider();

    return useQuery({
        queryKey: ['mall', 'products', { mall_id: mallId, tenant_id: tenantId, featured }],
        queryFn: async () => {
            console.log('📦 [useMallProducts] Fetching products:', { mallId, tenantId, featured });
            
            const filter: Record<string, any> = { mall_id: mallId };
            if (tenantId) filter.tenant_id = tenantId;
            if (featured) filter.is_featured = true;

            const response = await dataProvider.getList('products', {
                pagination: { page: 1, perPage: 500 },
                sort: { field: 'name', order: 'ASC' },
                filter,
            });
            
            console.log('📦 [useMallProducts] Fetched:', response.data?.length, 'products');
            return response;
        },
        enabled: !!mallId,
        ...MALL_CACHE_CONFIG,
    });
}
```

### Hash-Based Change Detection

The system uses hash-based comparison to detect actual data changes:

```typescript
// In MallOrderCreateContext.tsx

// Generate a hash from product IDs to detect actual content changes
const getProductsHash = useCallback((products: any[]) => {
    if (!products || products.length === 0) return '';
    return products.map(p => p.id).sort((a, b) => a - b).join(',');
}, []);

// Track the last hash to detect changes
const lastProductsHashRef = useRef<string>('');

// In the effect that syncs products
useEffect(() => {
    const currentHash = getProductsHash(queriedProducts);
    
    // Skip if hash hasn't changed (same products)
    if (currentHash === lastProductsHashRef.current) {
        console.log('⏭️ Products hash unchanged, skipping carousel init');
        return;
    }
    
    // Hash changed - update UI
    lastProductsHashRef.current = currentHash;
    console.log('🔄 Products changed, reinitializing carousel...');
    
    // ... initialization logic
}, [queriedProducts, getProductsHash]);
```

### Dual Pagination Mode Support

The context handles both pagination modes:

```typescript
// Initialize products based on pagination mode
useEffect(() => {
    // ... validation checks ...
    
    if (paginationMode === 'infinite') {
        // INFINITE MODE: Load all products at once
        console.log('🔄 Initializing products for infinite mode...');
        setCarouselPages({ 1: sortedProducts });
        setCarouselTotalPages(1); // All products on one "page"
        console.log('✅ Infinite grid initialized:', sortedProducts.length, 'products');
    } else {
        // HORIZONTAL MODE: Paginate for carousel
        console.log('🔄 Initializing carousel for horizontal mode...');
        const firstPageProducts = sortedProducts.slice(0, ITEMS_PER_PAGE);
        setCarouselPages({ 1: firstPageProducts });
        setCarouselTotalPages(Math.ceil(total / ITEMS_PER_PAGE));
        console.log('✅ Carousel initialized:', firstPageProducts.length, 'products on page 1');
    }
}, [paginationMode, queriedProducts, showFeaturedOnly, getProductsHash]);
```

---

## Configuration

### Adjusting Cache Duration

To modify cache behavior, update the `MALL_CACHE_CONFIG` object:

```typescript
// For shorter cache (5 minutes)
export const MALL_CACHE_CONFIG = {
    staleTime: 5 * 60 * 1000,      // 5 minutes
    gcTime: 10 * 60 * 1000,        // 10 minutes
    refetchOnWindowFocus: false,
    refetchOnMount: false,
};

// For longer cache (30 minutes)
export const MALL_CACHE_CONFIG = {
    staleTime: 30 * 60 * 1000,     // 30 minutes
    gcTime: 45 * 60 * 1000,        // 45 minutes
    refetchOnWindowFocus: false,
    refetchOnMount: false,
};

// For development (no cache)
export const MALL_CACHE_CONFIG = {
    staleTime: 0,                   // Always stale
    gcTime: 0,                      // Immediate garbage collection
    refetchOnWindowFocus: true,
    refetchOnMount: true,
};
```

### Enabling Refetch on Window Focus

For real-time data requirements:

```typescript
export const MALL_CACHE_CONFIG = {
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
    refetchOnWindowFocus: true,    // Enable this
    refetchOnMount: false,
};
```

---

## Usage Examples

### Basic Usage in a Component

```tsx
import { useMallStores, useMallProducts } from '../hooks/useMallDataQueries';

const MyComponent: React.FC = () => {
    // Fetch all stores
    const { data: storesData, isLoading: storesLoading } = useMallStores();
    
    // Fetch all products
    const { data: productsData, isLoading: productsLoading } = useMallProducts();
    
    if (storesLoading || productsLoading) {
        return <Loading />;
    }
    
    const stores = storesData?.data || [];
    const products = productsData?.data || [];
    
    return (
        <div>
            <h2>Stores ({stores.length})</h2>
            {stores.map(store => (
                <StoreCard key={store.id} store={store} />
            ))}
            
            <h2>Products ({products.length})</h2>
            {products.map(product => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
    );
};
```

### Filtering Products by Store

```tsx
const StoreProducts: React.FC<{ storeId: number }> = ({ storeId }) => {
    // Fetch products for specific store
    const { data, isLoading } = useMallProducts({ tenantId: storeId });
    
    if (isLoading) return <Loading />;
    
    const products = data?.data || [];
    
    return (
        <div>
            <h3>Products for Store #{storeId}</h3>
            {products.map(product => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
    );
};
```

### Fetching Featured Products Only

```tsx
const FeaturedProducts: React.FC = () => {
    // Fetch only featured products
    const { data, isLoading } = useMallProducts({ featured: true });
    
    if (isLoading) return <Loading />;
    
    const products = data?.data || [];
    
    return (
        <div className="featured-section">
            <h2>⭐ Featured Products</h2>
            {products.map(product => (
                <FeaturedCard key={product.id} product={product} />
            ))}
        </div>
    );
};
```

### Using with Context

```tsx
import { useMallOrderCreate } from '../contexts/MallOrderCreateContext';

const ProductGrid: React.FC = () => {
    const {
        carouselProducts,     // Current visible products
        selectedStore,        // Currently selected store
        setSelectedStore,     // Store selection handler
        isLoadingProducts,    // Loading state
    } = useMallOrderCreate();
    
    const handleStoreChange = (store: Store) => {
        setSelectedStore(store);
        // Products will automatically update via React Query cache
    };
    
    return (
        <div>
            <StoreSelector 
                onSelect={handleStoreChange}
                selected={selectedStore}
            />
            
            {isLoadingProducts ? (
                <Loading />
            ) : (
                <div className="product-grid">
                    {carouselProducts.map(product => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            )}
        </div>
    );
};
```

### Manual Cache Invalidation

```tsx
import { useQueryClient } from '@tanstack/react-query';

const AdminPanel: React.FC = () => {
    const queryClient = useQueryClient();
    
    const handleProductUpdate = async (productId: number, data: any) => {
        // Update product via API
        await updateProduct(productId, data);
        
        // Invalidate products cache to refetch
        queryClient.invalidateQueries({ queryKey: ['mall', 'products'] });
    };
    
    const handleClearAllCache = () => {
        // Clear all mall-related cache
        queryClient.invalidateQueries({ queryKey: ['mall'] });
    };
    
    return (
        <div>
            <button onClick={handleClearAllCache}>
                Clear Cache
            </button>
        </div>
    );
};
```

---

## Flow Diagrams

### Store Selection Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STORE SELECTION FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  User clicks store "Pizza Place"
         │
         ▼
  ┌─────────────────────────────────────────────┐
  │ setSelectedStore({ id: 123, name: "Pizza" })│
  └──────────────────────┬──────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────┐
  │ Context updates selectedTenantId to 123     │
  └──────────────────────┬──────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────┐
  │ useMallProducts({ tenantId: 123 }) called   │
  └──────────────────────┬──────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
  ┌──────────────┐               ┌──────────────┐
  │ Cache HIT    │               │ Cache MISS   │
  │ (data exists)│               │ (first load) │
  └──────┬───────┘               └──────┬───────┘
         │                               │
         │                               ▼
         │                       ┌──────────────┐
         │                       │ API Request  │
         │                       │ GET /products│
         │                       └──────┬───────┘
         │                               │
         │                               ▼
         │                       ┌──────────────┐
         │                       │ Store in     │
         │                       │ Cache        │
         │                       └──────┬───────┘
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────┐
  │ queriedProducts updates (new reference)      │
  └──────────────────────┬──────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────┐
  │ getProductsHash(queriedProducts) calculated  │
  │ Example: "12,34,56,78,90"                   │
  └──────────────────────┬──────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
  ┌──────────────────┐           ┌──────────────────┐
  │ Hash UNCHANGED   │           │ Hash CHANGED     │
  │ Skip update      │           │ Update UI        │
  └──────────────────┘           └────────┬─────────┘
                                          │
                                          ▼
                                 ┌──────────────────┐
                                 │ setCarouselPages │
                                 │ (new products)   │
                                 └────────┬─────────┘
                                          │
                                          ▼
                                 ┌──────────────────┐
                                 │ UI Re-renders    │
                                 │ Shows new products│
                                 └──────────────────┘
```

### Request Deduplication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       REQUEST DEDUPLICATION FLOW                             │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
  │  Component A    │   │  Component B    │   │  Component C    │
  │ useMallProducts │   │ useMallProducts │   │ useMallProducts │
  └────────┬────────┘   └────────┬────────┘   └────────┬────────┘
           │                     │                     │
           │ Same query key      │ Same query key      │
           │                     │                     │
           └──────────┬──────────┴──────────┬──────────┘
                      │                     │
                      ▼                     ▼
           ┌────────────────────────────────────────────┐
           │           TanStack Query                   │
           │                                            │
           │  Detects duplicate query keys              │
           │  Merges requests into single fetch         │
           │                                            │
           └─────────────────────┬──────────────────────┘
                                 │
                                 ▼ (SINGLE API CALL)
           ┌────────────────────────────────────────────┐
           │              Backend API                   │
           │    GET /public/mall/products               │
           └─────────────────────┬──────────────────────┘
                                 │
                                 ▼
           ┌────────────────────────────────────────────┐
           │              Cache Updated                 │
           │  All components receive same data          │
           └────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
  │  Component A    │   │  Component B    │   │  Component C    │
  │  Renders data   │   │  Renders data   │   │  Renders data   │
  └─────────────────┘   └─────────────────┘   └─────────────────┘

  BEFORE: 3 API calls
  AFTER:  1 API call (67% reduction)
```

---

## Debugging Guide

### Console Log Prefixes

The system uses emoji prefixes for easy log identification:

| Prefix | Meaning | Example |
|--------|---------|---------|
| 🏪 | Store operations | `🏪 [useMallStores] Fetching stores...` |
| 📦 | Product operations | `📦 [useMallProducts] Fetched: 48 products` |
| 🔄 | Sync/Update operations | `🔄 Initializing products for infinite mode...` |
| ✅ | Success | `✅ Carousel initialized: 8 products` |
| ⏭️ | Skipped operation | `⏭️ Products hash unchanged, skipping` |
| 🎠 | Carousel specific | `🎠 Loading carousel page 2...` |

### Common Issues and Solutions

#### Issue: Products not updating when switching stores

**Symptoms:** Clicking different stores shows the same products

**Diagnosis:**
1. Check console for `🔄 Products changed...` log
2. If not present, hash comparison is detecting no change

**Solution:** Verify `selectedTenantId` is being passed to `useMallProducts`:
```typescript
const { data } = useMallProducts({ tenantId: selectedTenantId });
```

#### Issue: Cache not working (always fetching)

**Symptoms:** Every store click triggers an API call

**Diagnosis:**
1. Check `staleTime` value is > 0
2. Verify query key structure is consistent

**Solution:** Ensure consistent query keys:
```typescript
// ✅ Good - consistent key structure
queryKey: ['mall', 'products', { mall_id: mallId, tenant_id: tenantId }]

// ❌ Bad - inconsistent structure
queryKey: tenantId 
    ? ['mall', 'products', mallId, tenantId]
    : ['mall', 'products', mallId]
```

#### Issue: Infinite scroll showing wrong products

**Symptoms:** Grid mode shows carousel products or outdated data

**Diagnosis:** Check for `🔄 Initializing products for infinite mode...` log

**Solution:** Ensure the mode-specific initialization runs:
```typescript
if (paginationMode === 'infinite') {
    setCarouselPages({ 1: sortedProducts });
} else {
    setCarouselPages({ 1: firstPageProducts.slice(0, ITEMS_PER_PAGE) });
}
```

### DevTools Inspection

React Query DevTools can be used for cache inspection:

```tsx
// In development, add to your App.tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const App = () => (
    <QueryClientProvider client={queryClient}>
        <MyApp />
        <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
);
```

---

## Best Practices

### 1. Query Key Consistency

Always use the same structure for query keys:

```typescript
// ✅ Recommended: Object-based keys for complex queries
queryKey: ['mall', 'products', { mall_id, tenant_id, featured }]

// ✅ Also good: Simple array for simple queries
queryKey: ['mall', 'stores', mall_id]
```

### 2. Avoid Premature Optimization

Don't disable cache features unless necessary:

```typescript
// ❌ Avoid unless truly needed
refetchOnMount: 'always',
staleTime: 0,

// ✅ Trust the cache
staleTime: 10 * 60 * 1000,
refetchOnMount: false,
```

### 3. Use Hash-Based Comparison for UI Updates

When synchronizing cached data with UI state:

```typescript
// ✅ Good: Compare actual content
const hash = products.map(p => p.id).sort().join(',');
if (hash !== lastHashRef.current) {
    updateUI(products);
}

// ❌ Bad: Compare references or counts
if (products !== lastProductsRef.current) {  // Always triggers
if (products.length !== lastCount) {          // Misses content changes
```

### 4. Handle Loading States Gracefully

```typescript
const { data, isLoading, isError, error } = useMallProducts();

if (isLoading) return <Skeleton />;
if (isError) return <ErrorMessage error={error} />;
if (!data?.data?.length) return <EmptyState />;

return <ProductGrid products={data.data} />;
```

### 5. Invalidate Cache After Mutations

```typescript
const queryClient = useQueryClient();

const updateProduct = async (id: number, data: any) => {
    await api.updateProduct(id, data);
    
    // Invalidate related queries
    queryClient.invalidateQueries({ queryKey: ['mall', 'products'] });
};
```

---

## File Reference

| File | Purpose |
|------|---------|
| `useMallDataQueries.ts` | React Query hooks for stores/products |
| `MallOrderCreateContext.tsx` | Context managing state and cache sync |
| `MallProductGrid.tsx` | UI component consuming cached data |
| `MallStoresList.tsx` | Store list component using cached stores |

---

## Related Documentation

- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [React Query Caching Guide](https://tanstack.com/query/latest/docs/react/guides/caching)
- [KitchnTabs Mall App Overview](./docs/kt-mall/01-OVERVIEW.md)

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 15, 2025 | Initial implementation with stores/products caching |
