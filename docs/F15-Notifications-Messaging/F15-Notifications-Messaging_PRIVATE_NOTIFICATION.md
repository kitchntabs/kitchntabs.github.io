---
layout: default
title: F15-Notifications-Messaging PRIVATE NOTIFICATION
---

$user = \App\Models\User::find(5); 
\App\AppNotifications\AppNotificationBuilder::send(
    notificationClass: \App\AppNotifications\Notifications\PrivateMessageNotification::class,
    data: ['message' => 'Private user message'],
    type: 'message',
    modelInstance: $user,
    channel: "user",
    scope: "private",
    targets: [$user->id],
    targetType: "user" 
);