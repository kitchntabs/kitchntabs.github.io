# User Preferences System - Technical Documentation

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Data Model](#data-model)
- [Backend Implementation](#backend-implementation)
- [Frontend Implementation](#frontend-implementation)
- [Notification Integration](#notification-integration)
- [Adding New Preferences](#adding-new-preferences)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

## Overview

The User Preferences System is a flexible, extensible framework that allows users to configure their personal settings across the Dash platform. The system follows an opt-in/opt-out model where users can control various aspects of their experience, particularly notification delivery channels.

### Key Features
- **JSON-based Storage**: Preferences stored as JSON in the user model
- **Notification Opt-in/Opt-out**: Users control email and push notification delivery per notification type
- **Config-First Defaults**: Initial preference values come from notification class config (hasEmail/hasPush)
- **User Override**: User preferences override config defaults when explicitly set
- **Dynamic Configuration**: Available preferences are auto-discovered from notification classes
- **Real-time Updates**: Changes take effect immediately without requiring logout
- **Frontend Integration**: React-based settings UI with AuthContext integration

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER PREFERENCES ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                          FRONTEND LAYER                               │   │
│  │  ┌────────────────────┐  ┌─────────────────────────────────────────┐ │   │
│  │  │ UserPreferences.tsx│  │ AuthContext (user.preferences)          │ │   │
│  │  │ - Render switches   │  │ - Stores user object with preferences   │ │   │
│  │  │ - Save preferences  │  │ - fetchAuth() refreshes user data      │ │   │
│  │  └────────────────────┘  └─────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                            API LAYER                                  │   │
│  │  PUT /api/system/user/preferences                                    │   │
│  │  GET /api/auth/getauth (returns user.preferences + systemValues)     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                          BACKEND LAYER                                │   │
│  │  ┌───────────────────────────┐  ┌──────────────────────────────────┐ │   │
│  │  │ UserController            │  │ User Model                       │ │   │
│  │  │ - updatePreferences()     │  │ - preferences (JSON column)      │ │   │
│  │  └───────────────────────────┘  └──────────────────────────────────┘ │   │
│  │                                                                       │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐│   │
│  │  │ AppNotification::via()                                            ││   │
│  │  │ - Checks user.preferences.notifications before sending            ││   │
│  │  │ - Respects email/push opt-out per notification type               ││   │
│  │  └───────────────────────────────────────────────────────────────────┘│   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Model

### User Preferences Structure

```php
// User.php - preferences column (JSON cast)
{
    "notifications": [
        {
            "id": "Domain\\App\\Notifications\\Tab\\TabCreatedNotification",
            "name": "TabCreatedNotification",
            "email": true,
            "push": false
        },
        {
            "id": "Domain\\App\\Notifications\\Tab\\TabConfirmedNotification",
            "name": "TabConfirmedNotification",
            "email": true,
            "push": true
        }
        // ... more notification preferences
    ]
    // Future: other preference groups can be added here
    // "theme": { "mode": "dark", "color": "blue" },
    // "display": { "language": "en", "timezone": "America/Santiago" }
}
```

### SystemValues: Available Notifications

The backend provides a cached list of configurable notifications via `systemValues.user_notifications`:

```json
{
    "user_notifications": [
        {
            "id": "Domain\\App\\Notifications\\Tab\\TabCreatedNotification",
            "name": "TabCreatedNotification",
            "className": "Domain\\App\\Notifications\\Tab\\TabCreatedNotification",
            "hasEmail": true,
            "hasPush": true,
            "hasSocket": true,
            "hasDatabase": false
        }
    ]
}
```

### Database Schema

```sql
-- users table
ALTER TABLE users ADD COLUMN preferences JSON NULL;

-- Example query to get notification preferences
SELECT 
    id, 
    email,
    JSON_EXTRACT(preferences, '$.notifications') as notification_prefs
FROM users 
WHERE id = 'user-uuid';
```

## Backend Implementation

### User Model Configuration

```php
// app/Models/User.php

class User extends Authenticatable
{
    protected $fillable = [
        // ... other fields
        'preferences',
    ];

    protected $casts = [
        'preferences' => 'json',
    ];
}
```

### UserController: Preferences Endpoint

```php
// domain/app/Http/Controllers/API/Extended/UserController.php

/**
 * Update user preferences
 * 
 * @param Request $request
 * @return JsonResponse
 */
public function updatePreferences(Request $request)
{
    $user = $request->user();
    
    $validated = $request->validate([
        'preferences' => 'required|array',
        'preferences.notifications' => 'sometimes|array',
        'preferences.notifications.*.id' => 'required|string',
        'preferences.notifications.*.name' => 'required|string',
        'preferences.notifications.*.email' => 'required|boolean',
        'preferences.notifications.*.push' => 'required|boolean',
    ]);
    
    // Merge with existing preferences
    $currentPreferences = $user->preferences ?? [];
    $newPreferences = array_merge($currentPreferences, $validated['preferences']);
    
    $user->update(['preferences' => $newPreferences]);
    
    Log::info('User preferences updated', [
        'user_id' => $user->id,
        'preferences' => $newPreferences,
    ]);
    
    return response()->json([
        'message' => 'Preferences updated successfully',
        'preferences' => $newPreferences,
    ]);
}
```

### Route Registration

```php
// routes/system.php (or routes/api.php)

Route::middleware(['auth:sanctum'])->prefix('system/user')->group(function () {
    Route::put('/preferences', [UserController::class, 'updatePreferences']);
});
```

### Notification Caching Command

```php
// app/Console/Commands/CacheUserNotifications.php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\File;

class CacheUserNotifications extends Command
{
    protected $signature = 'notifications:cache-user-notifications';
    protected $description = 'Cache available user notification configurations';

    public function handle()
    {
        $notifications = [];
        $notificationPath = base_path('domain/app/Notifications/Tab');
        
        if (!File::isDirectory($notificationPath)) {
            $this->error("Notification path not found: {$notificationPath}");
            return 1;
        }

        $files = File::glob($notificationPath . '/*Notification.php');
        
        foreach ($files as $file) {
            $className = $this->getClassNameFromFile($file);
            
            if (!$className || !class_exists($className)) {
                continue;
            }

            if (!method_exists($className, 'config')) {
                continue;
            }

            $config = $className::config();
            $channels = $config['channels'] ?? [];
            
            $notifications[] = [
                'id' => $className,
                'name' => class_basename($className),
                'className' => $className,
                'hasEmail' => $channels['mail'] ?? false,
                'hasPush' => $channels['push'] ?? false,
                'hasSocket' => $channels['socket'] ?? false,
                'hasDatabase' => $channels['database'] ?? false,
            ];
        }

        // Cache to file
        $cacheFile = storage_path('app/cache/user_notifications.json');
        File::ensureDirectoryExists(dirname($cacheFile));
        File::put($cacheFile, json_encode($notifications, JSON_PRETTY_PRINT));
        
        $this->info('Cached ' . count($notifications) . ' notification configurations');
        return 0;
    }
    
    protected function getClassNameFromFile($file): ?string
    {
        $content = File::get($file);
        
        if (preg_match('/namespace\s+([^;]+);/', $content, $namespaceMatch) &&
            preg_match('/class\s+(\w+)/', $content, $classMatch)) {
            return $namespaceMatch[1] . '\\' . $classMatch[1];
        }
        
        return null;
    }
}
```

### Loading Cached Notifications in AuthController

```php
// In getAuth() method or auth response builder

protected function getUserNotifications(): array
{
    $cacheFile = storage_path('app/cache/user_notifications.json');
    
    if (file_exists($cacheFile)) {
        return json_decode(file_get_contents($cacheFile), true) ?? [];
    }
    
    return [];
}

// Add to systemValues in auth response
'systemValues' => [
    // ... other values
    'user_notifications' => $this->getUserNotifications(),
]
```

## Frontend Implementation

### UserPreferences Component

```typescript
// packages/dash-admin/src/components/user/UserPreferences.tsx

import React, { useState, useEffect } from "react";
import { 
    Box, Typography, Switch, FormControlLabel, 
    Card, CardContent, Alert, Button, Snackbar 
} from "@mui/material";
import { Save as SaveIcon } from "@mui/icons-material";
import { useAxios } from 'dash-axios-hook';
import { useAuthContext } from '../../contexts/auth/AuthContext';
import { AuthPersistenceService } from 'dash-auth';

interface NotificationConfig {
    id: string;
    name: string;
    hasEmail: boolean;
    hasPush: boolean;
}

interface NotificationPreference {
    id: string;
    name: string;
    email: boolean;
    push: boolean;
}

const UserPreferences: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [isDirty, setIsDirty] = useState(false);
    const [preferences, setPreferences] = useState<NotificationPreference[]>([]);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    
    const axios = useAxios();
    const { user, fetchAuth } = useAuthContext();
    
    // Available notifications from systemValues (cached)
    const systemValues = AuthPersistenceService.getSystemValues();
    const availableNotifications: NotificationConfig[] = systemValues?.user_notifications || [];

    // Build preferences from user data
    const buildPreferencesFromUser = (userPrefs: any, notifications: NotificationConfig[]) => {
        const notificationPrefs = userPrefs?.notifications || [];
        
        return notifications.map((notif) => {
            const existing = notificationPrefs.find((p: any) => p.id === notif.id);
            return {
                id: notif.id,
                name: notif.name,
                // IMPORTANT: Default to config values (hasEmail/hasPush) unless user has explicitly set
                email: existing?.email !== undefined ? existing.email : notif.hasEmail,
                push: existing?.push !== undefined ? existing.push : notif.hasPush,
            };
        });
    };

    useEffect(() => {
        if (availableNotifications.length > 0) {
            const initialPrefs = buildPreferencesFromUser(user?.preferences, availableNotifications);
            setPreferences(initialPrefs);
            setLoading(false);
        }
    }, [user?.preferences, availableNotifications.length]);

    const handleToggle = (notificationId: string, type: 'email' | 'push', checked: boolean) => {
        setPreferences(prev => prev.map(pref => 
            pref.id === notificationId ? { ...pref, [type]: checked } : pref
        ));
        setIsDirty(true);
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            const response = await axios.put('/system/user/preferences', {
                preferences: { notifications: preferences },
            });
            
            // Update local state from response
            if (response.data?.preferences?.notifications) {
                const updatedPrefs = buildPreferencesFromUser(response.data.preferences, availableNotifications);
                setPreferences(updatedPrefs);
            }
            
            setSnackbar({ open: true, message: 'Preferences saved!', severity: 'success' });
            setIsDirty(false);
            
            // Refresh auth context
            if (fetchAuth) await fetchAuth();
        } catch (error: any) {
            setSnackbar({ 
                open: true, 
                message: error.response?.data?.message || 'Failed to save', 
                severity: 'error' 
            });
        } finally {
            setSaving(false);
        }
    };

    // Render logic...
};
```

## Notification Integration

### How Preferences are Checked

The `AppNotification::via()` method checks user preferences before including mail/push channels:

```php
// app/AppNotifications/AppNotification.php - via() method

public function via($user)
{
    // ... determine channels from config ...
    
    // Check user notification preferences for mail and push channels
    $notificationClass = get_class($this->notification);
    $userHasOptedInMail = true; // Default to true (backwards compatible)
    $userHasOptedInPush = true;
    
    if ($user && isset($user->preferences) && is_array($user->preferences)) {
        $notificationPrefs = $user->preferences['notifications'] ?? [];
        
        foreach ($notificationPrefs as $pref) {
            if ($pref['id'] === $notificationClass) {
                $userHasOptedInMail = (bool) ($pref['email'] ?? true);
                $userHasOptedInPush = (bool) ($pref['push'] ?? true);
                
                Log::channel('notifications')->info('User notification preference found', [
                    'user_id' => $user->id,
                    'notification_class' => $notificationClass,
                    'email_opt_in' => $userHasOptedInMail,
                    'push_opt_in' => $userHasOptedInPush,
                ]);
                break;
            }
        }
    }
    
    // Apply user preferences
    if (!$userHasOptedInMail) {
        $mailEnabled = false;
    }
    
    if (!$userHasOptedInPush) {
        $push = false;
    }
    
    // Build response array with filtered channels
    // ...
}
```

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NOTIFICATION DELIVERY FLOW                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────┐                                                   │
│   │ Event Triggered │                                                   │
│   │ (e.g., Tab      │                                                   │
│   │  Created)       │                                                   │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ AppNotificationBuilder::send()                                   │  │
│   │ - Creates notification instance                                  │  │
│   │ - Determines target users                                        │  │
│   └────────────────────────────┬────────────────────────────────────┘  │
│                                │                                        │
│                                ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ For each target user: $user->notify(new AppNotification(...))   │  │
│   └────────────────────────────┬────────────────────────────────────┘  │
│                                │                                        │
│                                ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ AppNotification::via($user)                                      │  │
│   │                                                                   │  │
│   │ 1. Get channels from notification config                        │  │
│   │    └─ TabCreatedNotification::config()['channels']              │  │
│   │                                                                   │  │
│   │ 2. Check user preferences                                       │  │
│   │    └─ $user->preferences['notifications']                       │  │
│   │    └─ Find preference matching notification class               │  │
│   │    └─ Get email/push opt-in values                              │  │
│   │                                                                   │  │
│   │ 3. Filter channels based on user preferences                    │  │
│   │    └─ If user opted out of email → remove 'mail'                │  │
│   │    └─ If user opted out of push → remove 'push'                 │  │
│   │                                                                   │  │
│   │ 4. Return filtered channels array                               │  │
│   │    └─ e.g., ['database', 'broadcast'] (no mail/push)            │  │
│   └────────────────────────────┬────────────────────────────────────┘  │
│                                │                                        │
│            ┌───────────────────┼───────────────────┐                   │
│            │                   │                   │                   │
│            ▼                   ▼                   ▼                   │
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐          │
│   │   WebSocket    │  │   Database     │  │   Mail/Push    │          │
│   │ (always sent)  │  │ (if enabled)   │  │ (if opted in)  │          │
│   └────────────────┘  └────────────────┘  └────────────────┘          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Adding New Preferences

### Step 1: Create/Update Notification Class

```php
// domain/app/Notifications/Tab/MyNewNotification.php

namespace Domain\App\Notifications\Tab;

use App\AppNotifications\AppNotificationBase;
use App\AppNotifications\AppNotificationPayload;

class MyNewNotification extends AppNotificationBase
{
    public static function config()
    {
        return [
            "name"     => self::class,
            "active"   => true,
            "channels" => [
                "socket"   => true,   // Always sent via WebSocket
                "mail"     => true,   // Enable email (configurable)
                "database" => false,  // No database storage
                "push"     => true,   // Enable push (configurable)
            ],
            "access"   => "user",
        ];
    }

    public function buildNotification()
    {
        $title = $this->title ?? 'My Notification';
        $message = $this->message ?? 'Something happened!';

        $this->notificationPayload = new AppNotificationPayload(
            self::class,
            $title,
            $message,
            $this->data,
            $this->data['type'] ?? 'my.notification'
        );
    }
}
```

### Step 2: Regenerate Cache

```bash
# Run inside Docker container
sail artisan notifications:cache-user-notifications

# Or via entrypoint.sh (runs on container start)
```

### Step 3: Restart Backend Container (for entrypoint)

```bash
sail restart
# OR
docker-compose restart laravel.test
```

### Step 4: Re-login Frontend

The user needs to re-login (or call fetchAuth) to get the updated `systemValues.user_notifications`.

### Adding Non-Notification Preferences

To add other preference types (theme, language, etc.):

#### 1. Update UserController Validation

```php
public function updatePreferences(Request $request)
{
    $validated = $request->validate([
        'preferences' => 'required|array',
        'preferences.notifications' => 'sometimes|array',
        // Add new preference types
        'preferences.theme' => 'sometimes|array',
        'preferences.theme.mode' => 'sometimes|in:light,dark,system',
        'preferences.theme.color' => 'sometimes|string',
        'preferences.display' => 'sometimes|array',
        'preferences.display.language' => 'sometimes|string',
    ]);
    
    // ... merge and save
}
```

#### 2. Add preference_formats to SystemValues

```php
// In auth response builder
'preference_formats' => [
    [
        'id' => 'notifications',
        'group' => 'notifications',
        'tab' => 'notifications',
        'attribute' => 'preferences.notifications',
        'label' => 'Notification Preferences',
        'type' => 'custom',
        'component' => 'NotificationPreferences',
    ],
    [
        'id' => 'theme',
        'group' => 'appearance',
        'tab' => 'appearance',
        'attribute' => 'preferences.theme',
        'label' => 'Theme Settings',
        'type' => 'custom',
        'component' => 'ThemePreferences',
    ],
]
```

#### 3. Create Frontend Component

```typescript
// packages/dash-admin/src/components/user/ThemePreferences.tsx

const ThemePreferences: React.FC = () => {
    const { user, fetchAuth } = useAuthContext();
    const [theme, setTheme] = useState(user?.preferences?.theme || { mode: 'dark' });
    
    // ... implement theme selection UI
};
```

## API Reference

### GET /api/auth/getauth

Returns authenticated user data including preferences.

**Response:**
```json
{
    "user": {
        "id": "user-uuid",
        "preferences": {
            "notifications": [
                { "id": "...", "name": "...", "email": true, "push": false }
            ]
        }
    },
    "systemValues": {
        "user_notifications": [
            {
                "id": "Domain\\App\\Notifications\\Tab\\TabCreatedNotification",
                "name": "TabCreatedNotification",
                "hasEmail": true,
                "hasPush": true
            }
        ]
    }
}
```

### PUT /api/system/user/preferences

Updates user preferences.

**Request:**
```json
{
    "preferences": {
        "notifications": [
            {
                "id": "Domain\\App\\Notifications\\Tab\\TabCreatedNotification",
                "name": "TabCreatedNotification",
                "email": true,
                "push": false
            }
        ]
    }
}
```

**Response:**
```json
{
    "message": "Preferences updated successfully",
    "preferences": {
        "notifications": [...]
    }
}
```

## Troubleshooting

### Preferences Not Showing in UI

1. **Check localStorage systemValues**:
   ```javascript
   console.log(JSON.parse(localStorage.getItem('systemValues')));
   ```

2. **Verify cache file exists**:
   ```bash
   sail shell
   cat storage/app/cache/user_notifications.json
   ```

3. **Regenerate cache**:
   ```bash
   sail artisan notifications:cache-user-notifications
   ```

4. **Re-login to refresh auth**

### Preferences Not Being Respected

1. **Check notification logs**:
   ```bash
   tail -f storage/logs/notifications.log | grep "preference"
   ```

2. **Verify user.preferences in database**:
   ```sql
   SELECT preferences FROM users WHERE id = 'user-id';
   ```

3. **Debug via() method**:
   - Check if $user is passed correctly
   - Verify preferences JSON structure

### New Notification Not Appearing

1. Run `sail artisan notifications:cache-user-notifications`
2. Check that notification class has `config()` method
3. Verify channels include `mail: true` or `push: true`
4. Re-login to get updated systemValues

---

*Last Updated: December 2024*
*Version: 1.0.0*
