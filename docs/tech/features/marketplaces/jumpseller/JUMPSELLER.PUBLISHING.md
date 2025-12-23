Jumpseller Product Publishing Flow

The Jumpseller product publishing process uses a multi-layered job architecture to handle large-scale product publishing operations efficiently. 
The flow is designed to support chunked processing, progress tracking, and optimized API calls to the Jumpseller marketplace.

Flow Architecture

1. Campaign Process Initiation
File: CampaignProcessJob.php

The process begins when a campaign publishing action is triggered:

CampaignProcessJob::handle()
├── processStarted() - Updates campaign status to "publishing"
├── processProducts() - Main orchestration method
│   ├── getProductsQuery() - Filters products for publishing
│   └── processProductsByMarketplace() - Groups products by system marketplace
@deprecated: └── processFinished() - Updates campaign status to "published"


2. Marketplace-Specific Processing
Method: processProductsByMarketplace()

Products are grouped by system marketplace and processed according to marketplace-specific settings:

processProductsByMarketplace()
├── Group products by system_marketplace_id
├── For each marketplace:
│   ├── shouldSystemMarketplaceUseChunking() - Checks if chunking is needed
│   ├── If chunking: processSystemMarketplaceProductsInChunks()
│   └── If bulk: processSystemMarketplaceProductsInBulk()
└── Track overall progress across all marketplaces


3. Chunked Processing (Jumpseller Path)
Method: processSystemMarketplaceProductsInChunks()

For Jumpseller, chunking is enabled (shouldUseChunking(): true):

processSystemMarketplaceProductsInChunks()
├── Create marketplace process tracker
├── Determine phases: getMarketplacePhases()
│   ├── product_data: BatchUpdateProductsJob
│   ├── variants: BatchUpdateVariantsJob
│   └── images: BatchUpdateImagesJob
├── Split products into chunks (chunkSize = 5)
├── For each chunk:
│   ├── Create PublishProductsJob instance
│   ├── Pass processTracker.id for progress tracking
│   └── Execute job->handle()
└── Complete marketplace process tracker



4. Product Publishing Job
File: PublishProductsJob.php

Each chunk is processed through the generic publishing job:

PublishProductsJob::handle()
├── prepareCampaignMarketplaceProducts() - Validate products
├── publishProducts() - Call marketplace-specific service
│   ├── validateMarketplaceConnection()
│   ├── Get marketplace class: JumpsellerService
│   ├── Handle rate limiting if needed
│   └── Call: marketplaceInstance->publishProducts()
└── sendNotificationIfNeeded() - Optional notifications



5. Jumpseller Service Publishing
File: JumpsellerService.php

The marketplace service handles the actual API integration:

JumpsellerService::publishProducts()
├── Extract campaign and product information
├── Dispatch OptimizedPublishProductsJob
│   ├── Pass user, productIds, marketplaceId
│   ├── Include campaignId and trackerId
│   └── Queue on 'campaigns' queue
└── Background job handles actual API calls



6. Optimized Publishing Job
File: OptimizedPublishProductsJob.php

The final layer handles Jumpseller-specific optimizations:

OptimizedPublishProductsJob::handle()
├── validateProducts() - Check prices, stock, SKUs
├── Split into smaller chunks (chunkSize = 10)
├── Dispatch phase-specific jobs with delays:
│   ├── BatchUpdateProductsJob (product data)
│   ├── BatchUpdateVariantsJob (variants)
│   └── BatchUpdateImagesJob (images)
└── Each job updates progress tracker phases



Progress Tracking
Tracker Hierarchy
Main Campaign Tracker (trackerId)
├── Phase: product_data
├── Phase: variants  
├── Phase: images
└── Marketplace Process Trackers
    ├── processTracker.id (per marketplace)
    └── Updates main tracker phases



Progress Updates
CampaignProcessJob: Creates main tracker with calculated phases
processSystemMarketplaceProductsInChunks: Creates marketplace process tracker
OptimizedPublishProductsJob: Updates phase-specific progress
Batch Jobs: Report completion status back to trackers
Key Features
Chunking Strategy
Campaign Level: Groups by marketplace (unlimited size)
Marketplace Level: Chunks of 5 products for PublishProductsJob
API Level: Chunks of 10 products for OptimizedPublishProductsJob
Error Handling
Graceful Degradation: Continues processing other chunks on failure
Error Aggregation: Collects errors in errorsBag for reporting
Tracker Updates: Marks failed phases in progress tracking
Rate Limiting
Detection: Checks hasRequestsLimiter() and getDateTimeForSendNextRequest()
Recursive Dispatch: Delays jobs when rate limits are hit
Backoff Strategy: Uses marketplace-specific delay calculations
Marketplace Phases
Jumpseller defines three distinct phases:

product_data: Basic product information (name, price, description)
variants: Product variants based on modifier groups
images: Product image uploads
Configuration Points
Marketplace Settings
// JumpsellerService.php
public static function shouldUseChunking(): bool {
    return true; // Enables chunked processing
}

public static function getProcessPhases(): array {
    return [
        'product_data' => BatchUpdateProductsJob::class,
        'variants' => BatchUpdateVariantsJob::class,
        'images' => BatchUpdateImagesJob::class
    ];
}



Chunk Sizes
CampaignProcessJob: 5 products per PublishProductsJob
OptimizedPublishProductsJob: 10 products per batch job
Rate Limiting: 1-second delays between chunks
This architecture provides scalable, trackable, and fault-tolerant product publishing for the Jumpseller marketplace integration.