---
layout: default
title: F15-Notifications-Messaging NOTIFICATIONS
---

NOTIFICATIONS DOCUMENTATION

This sample sends a notificiation for a job completion message to a specific tenant system channel
AppNotificationBuilder::send(
notificationClass: JobCompletionNotification::class,
data: $info,
type: $info['type'] ?? 'job.completion.message',
channel: "tenant.{$tenant_id}.system",
scope: "channel",
modelInstance: null,
targets: ['admin'],
targetType: "role"
);

This sample sends a notificiation to a particular user in his private channel.
AppNotificationBuilder::send(
notificationClass: CampaignMarketplaceProductStatusNotification::class,
data: $info,
modelInstance: $user,
channel: "user",
scope: "private",
targets: [$user->id]
);

Important, the tenant data needs to be serialized before

   $tenant = Tenant::with('media')->find($this->tenantId);
        $tenantResource = new TenantResource($tenant);
        $tenantData = $tenantResource->toArray(request());

  // Send private notification to the user who initiated the export
        AppNotificationBuilder::send(
            notificationClass: ProductExportNotification::class,
            data: $data,
            type: 'export.completed',
            modelInstance: $this->user,
            channel: "user",
            scope: "private",
            targets: [$this->user->id],
            tenant: $tenantData
        );


Frontend listening:
 const { events, lastEvent } = useContext<ILaravelEchoContext>(LaravelEchoContext);


  useEffect(() => {
    // This use effect handles the template notification
    const storedEvent = localStorage.getItem('lastImportEvent');
    const currentEvent = JSON.stringify(lastEvent);
    if (lastEvent && storedEvent !== currentEvent) {
      
      switch (lastEvent.notificationPayload.class) {
        case "ValidateProductImportNotification":
        case "ProductImportNotification":
        case "ProductImportProgressNotification":
        case "ProductImportErrorNotification":
          setLastNotification(lastEvent);
          localStorage.setItem('lastImportEvent', currentEvent);
          break;
      }
    }
  }, [lastEvent]);

   useEffect(() => {
    // This use effect handles the normalized import notifications
    const storedEvent = localStorage.getItem('lastNormalizedImportEvent');
    const currentEvent = JSON.stringify(lastEvent);
    if (lastEvent && storedEvent !== currentEvent) {
 
      switch (lastEvent.type) {
        case "import.started":
        case "import.failed":
        case "import.completed":
          setLastNormalizedNotification(lastEvent);
          localStorage.setItem('lastNormalizedImportEvent', currentEvent);
          break;
      }
    }
  }, [lastEvent]);



  Documentation:

  AppNotification System Documentation
Overview
The AppNotification system is a comprehensive notification framework built on Laravel that supports multiple delivery channels (database, email, websockets) and various scoping mechanisms (public, private, channel-based). It provides a flexible way to send notifications to users, roles, or broadcast to channels.

Architecture Components
1. AppNotificationBuilder
The main entry point for sending notifications. It acts as a factory and dispatcher that handles routing notifications to appropriate channels and targets.

2. AppNotification
A Laravel Notification wrapper that implements ShouldQueue and ShouldBroadcast. It handles the actual delivery through multiple channels (mail, database, broadcast).

3. AppNotificationBase
An abstract base class that all notification types must extend. It provides the structure and common functionality for notification classes.

Core Flow
graph TD
    A[AppNotificationBuilder::send()] --> B{Scope Type?}
    B -->|public| C[PublicMessageNotification + Broadcast]
    B -->|private| D[Resolve User Targets]
    B -->|channel| E[Event Dispatch to Channel]
    
    D --> F[Create AppNotification per User]
    F --> G[Queue Notification]
    G --> H[via() determines channels]
    H --> I[Database Storage]
    H --> J[Email Delivery]
    H --> K[WebSocket Broadcast]
    
    E --> L[Broadcast to Channel]
    L --> M[WebSocket Channel Delivery]

Copy

Apply

Method Signature
AppNotificationBuilder::send(
    $notificationClass,     // Notification class to instantiate
    $type = "message",      // Notification type identifier
    $data = [],            // Additional payload data
    $modelInstance = null, // Model instance (User, etc.)
    $targets = [],         // Array of target IDs/names
    $scope = "public",     // Scope: public|private|channel
    $channel = null,       // Channel name for broadcasts
    $targetType = "user"   // Target type: user|role
)

Copy

Apply

Notification Scopes
1. Public Scope
Broadcasts to all connected clients (not tenant-scoped yet).

AppNotificationBuilder::send(
    notificationClass: PublicAnnouncementNotification::class,
    type: 'announcement',
    data: ['message' => 'System maintenance scheduled'],
    scope: "public"
);

Copy

Apply

2. Private Scope
Sends notifications to specific users in their private channels.

AppNotificationBuilder::send(
    notificationClass: UserWelcomeNotification::class,
    data: $welcomeData,
    modelInstance: $user,
    scope: "private",
    targets: [$user->id],
    targetType: "user"
);

Copy

Apply

3. Channel Scope
Broadcasts to specific channels, typically for role-based or tenant-specific notifications.

AppNotificationBuilder::send(
    notificationClass: JobCompletionNotification::class,
    data: $jobInfo,
    type: 'job.completion.message',
    channel: "tenant.{$tenant_id}.system",
    scope: "channel",
    targets: ['admin'],
    targetType: "role"
);

Copy

Apply

Target Resolution
User Targets
When targetType = "user", the system resolves targets as user IDs:

$resolved_targets = User::whereIn('id', $targets)->get();

Copy

Apply

Role Targets
When targetType = "role", the system finds all users with specified roles:

$resolved_targets = User::whereHas('roles', function($query) use ($targets) {
    $query->whereIn('name', $targets);
})->get();

Copy

Apply

Delivery Channels
The via() method in AppNotification determines delivery channels based on configuration:

Database: Stores notification in notifications table
Broadcast: Sends via WebSockets for real-time delivery
Mail: Sends email notifications (if APP_MAIL_ENABLED=true)
Configuration-Based Notifications
Notifications can have additional configuration that enables:

Role-Scoped Notifications
// In notification class config
public static function config() {
    return [
        'active' => true,
        'roles' => ['admin', 'manager'],
        'channels' => ['database', 'mail', 'broadcast']
    ];
}

Copy

Apply

Email Notifications
public static function config() {
    return [
        'active' => true,
        'emails' => ['admin@company.com'],
        'mailView' => 'notifications.custom-template',
        'subject' => 'Important System Notification'
    ];
}

Copy

Apply

Common Use Cases
1. Job Completion Notification (System to Admins)
AppNotificationBuilder::send(
    notificationClass: JobCompletionNotification::class,
    data: $jobInfo,
    type: 'job.completion.message',
    channel: "tenant.{$tenant_id}.system",
    scope: "channel",
    targets: ['admin'],
    targetType: "role"
);

Copy

Apply

2. User-Specific Notification
AppNotificationBuilder::send(
    notificationClass: CampaignStatusNotification::class,
    data: $campaignInfo,
    modelInstance: $user,
    scope: "private",
    targets: [$user->id],
    targetType: "user"
);

Copy

Apply

3. Multi-User Notification
AppNotificationBuilder::send(
    notificationClass: TeamUpdateNotification::class,
    data: $updateInfo,
    scope: "private",
    targets: [1, 2, 3, 4], // User IDs
    targetType: "user"
);

Copy

Apply

4. Role-Based Notification
AppNotificationBuilder::send(
    notificationClass: SecurityAlertNotification::class,
    data: $alertInfo,
    scope: "private",
    targets: ['admin', 'security'],
    targetType: "role"
);

Copy

Apply

WebSocket Broadcasting
Channel Names
Private User: user.{user_id}
Custom Channel: {channel_name} (as specified)
Public: Global broadcast channel
Event Names
Determined by broadcastAs() method, typically returns the notification type.

Model Instance Handling
When a modelInstance is provided:

User Instance: Targets the user directly
Other Models: Attempts to find associated user via $model->user
Serialization: Calls localize() or serialize() if available
Public Links: Generates publicResourceLink() if method exists
Error Handling
Failed notifications are logged to the 'notifications' channel
Missing targets default to model instance user
Invalid configurations fall back to defaults
Queue failures are logged with full exception details
Best Practices
Always specify scope explicitly to avoid unexpected behavior
Use meaningful notification types for frontend handling
Implement configuration methods for reusable notifications
Test channel permissions before deploying channel-scoped notifications
Consider tenant isolation for multi-tenant applications
Technical Debt Notes
Public notifications are not tenant-scoped yet
Channel scope with role targeting could be simplified
Email personal address CC functionality is commented out
Admin notification rules need review for consistency


