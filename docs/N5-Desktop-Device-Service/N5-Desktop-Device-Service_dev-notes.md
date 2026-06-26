---
layout: default
title: N5-Desktop-Device-Service dev-notes
---

# Migraciones necesarias:
    -   Agregar columna 'expires_at' (not) a la tabla de personal_access_tokens
        ALTER TABLE public.personal_access_tokens ADD expires_at timestamptz NULL;

    - Agregar la columna tenant_id al modelo de usuario  
      ALTER TABLE public.users ADD tenant_id varchar NULL DEFAULT 1;

    - Agregar un tenant para DASH

    - Quitar la restricción de not null para el apellido en la base de datos. 
      Debido a que el modelo de usuarios del boilerplate, utilizado para gestionar roles de usaurio, no permite 'lastname'.
      ALTER TABLE public.users ALTER COLUMN lastname DROP NOT NULL;

    - a la tabla de migraciones se debe agregar las migraciones ya incluidas en la DB de prod:
      - 2023_01_11_112014_create_tenants_table
      - 2023_01_11_112348_create_users_table
      - 2023_01_13_144505_create_notifications_table

   - Correr sólo la migración sólo para la tabla tenants. verificar instrucción anterior.
      sail artisan migrate:refresh --path=/database/migrations/2023_01_11_112014_create_tenants_table.php

    - deprecar/eliminar actual tabla de roles (se generara por laravel permissions)
      - ALTER TABLE public.roles RENAME TO deprecated_roles;

    - php artisan migrate --seed

    - migrate roles
# Sync roles antiguos a nuevos de paquete laravel permission
   sail artisan db:sync_roles

# Deprecations
  - AppNotifications: Needs refactoring (User Contract)

# Fix
Composer merge pluggin

# Considerar para deploy:
 configuracion de zona horaria America/Santiago tanto en postgres como en la config del proyecto
 cambiar endpoint de app mobile mayoria de cambios son de camelCase a snake_case
 cambiar url de redireccion de mercadolibre se agrega prefijo "api"