---
layout: default
title: F15-Notifications-Messaging WS MESSAGING
---

NOTIFICATIONS DOCUMENTATION

Sending an event: Example @ dash-backend/app/Http/Controllers/API/Messaging/WebSocketTestController.php

// Private message sending:
AppNotificationBuilder::send(
          PrivateMessageNotification::class,
          "Private user message",
          $user,
          null,
          "private"
      );
      
// Public message sending:
AppNotificationBuilder::send(
        PublicMessageNotification::class,
        'Test message at ' . now(),
      );



Example of public notification flow logs:

[2025-04-05 18:16:23] local.INFO: New Notification of type App\AppNotifications\Notifications\PublicMessageNotification  
[2025-04-05 18:16:23] local.INFO: array (
  'name' => 'App\\AppNotifications\\Notifications\\PublicMessageNotification',
  'active' => true,
  'scope' => 'public',
  'targets' => 
  array (
  ),
  'channels' => 
  array (
    'socket' => true,
    'mail' => false,
    'database' => false,
  ),
)  
[2025-04-05 18:16:23] local.INFO: Sending public notification  
[2025-04-05 18:16:23] local.INFO: New App Notification  
[2025-04-05 18:16:23] local.INFO: name App\AppNotifications\Notifications\PublicMessageNotification  
[2025-04-05 18:16:23] local.INFO: targetType public  
[2025-04-05 18:16:23] local.INFO: MODEL INSTANCE NOT AVAILABLE  

