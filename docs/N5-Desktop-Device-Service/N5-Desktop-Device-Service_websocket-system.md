---
layout: default
title: N5-Desktop-Device-Service websocket-system
---

# DASH Real‑Time / WebSocket System — Technical Documentation

This document describes the end‑to‑end real‑time signaling system used by the DASH
platform (backend `dash-backend`, the `dash-backend-docker` dev stack, and the
React frontends under `kitchntabs-frontend`). It covers the architecture, the
libraries, the configuration on both backend and frontend, Redis, queues,
Horizon, Supervisor, Reverb, and — most importantly — the **SSL vs non‑SSL
(dev vs prod)** behavior that is the usual source of connection problems.

> TL;DR for local dev: the browser must connect with **plain `ws` to
> `ws://localhost:25001/app/dash`** (not `wss`), the backend `REVERB_APP_KEY`
> must equal the frontend `VITE_APP_SOCKETS_KEY` (`dash`), and **Reverb must be
> running** (it is started in a separate terminal, not by Supervisor).

---

## 1. High‑level overview

The system uses the **Pusher protocol** spoken by **Laravel Reverb** (a
first‑party, self‑hosted WebSocket server). The frontend talks to it through
**Laravel Echo** + **pusher‑js**. Authorization for private channels is done over
plain HTTP against the Laravel API; message fan‑out and background work go
through **Redis** (queues, cache, the Reverb app registry, and optional Reverb
horizontal scaling). **Horizon** supervises the Redis queue workers.

```
                         ┌──────────────────────────────────────────────┐
                         │                  Browser (SPA)                │
                         │   Laravel Echo  +  pusher-js                  │
                         └───────┬──────────────────────────┬───────────┘
              (1) HTTP  POST     │                          │  (2) WebSocket
              private-channel    │                          │  ws(s)://host:port/app/<key>
              auth (Bearer)      │                          │
                                 ▼                          ▼
                  ┌───────────────────────┐     ┌─────────────────────────┐
                  │  Laravel API (HTTP)   │     │   Laravel Reverb         │
                  │  php artisan serve    │     │   php artisan reverb:start│
                  │  POST /api/ws/auth    │     │   :25001 (dev) / :443 prod │
                  │  Broadcast::auth()    │     └───────────┬─────────────┘
                  │  channels.php rules   │                 │ (4) broadcast
                  └───────────┬───────────┘                 │     event payloads
                              │ (3) event dispatched        │
                              │     ShouldBroadcast         │
                              ▼                             │
                  ┌───────────────────────┐                │
                  │   Redis               │◄───────────────┘
                  │  • queues (Horizon)   │   • Reverb app registry (reverb:apps)
                  │  • cache              │   • Reverb scaling pub/sub (optional)
                  └───────────────────────┘
```

**Signaling flow:**

1. **Connect** — Echo/pusher‑js opens a WebSocket to `ws(s)://<host>:<port>/app/<app-key>`.
   Reverb validates `<app-key>` against its app registry and replies with
   `pusher:connection_established` (carrying a `socket_id`).
2. **Authorize (private/presence channels only)** — for each `private-…` /
   `presence-…` subscription, pusher‑js POSTs `{ channel_name, socket_id }` to the
   Laravel auth endpoint (`/api/ws/auth`) with the user's Bearer token. Laravel runs
   the matching `Broadcast::channel(...)` rule in `routes/channels.php` and returns a
   signed auth token.
3. **Subscribe** — Echo sends `pusher:subscribe` with that token; Reverb verifies the
   signature (using the shared app secret) and joins the channel.
4. **Broadcast** — when the backend dispatches a `ShouldBroadcast` event/notification,
   it is (optionally queued and) sent to Reverb over the Pusher HTTP API; Reverb pushes
   the payload to all subscribed sockets.

---

## 2. Components & libraries

| Layer | Component | Where |
|---|---|---|
| WS server | **Laravel Reverb** (`laravel/reverb`) | `dash-backend`, run as `php artisan reverb:start` |
| Broadcasting | Laravel Broadcasting (`pusher`‑compatible `reverb` driver) | `dash-backend/config/broadcasting.php` |
| Channel auth | `DashBroadcastAuthController` + `routes/channels.php` | `dash-backend/app/Http/Controllers/DashBroadcastAuthController.php` |
| Queues | Laravel Queue on **Redis** | `QUEUE_CONNECTION=redis` |
| Queue supervision | **Laravel Horizon** (`php artisan horizon`) | `dash-backend/config/horizon.php` |
| Process mgr | **Supervisor** (web server only) | image `/etc/supervisor/conf.d/supervisord.conf` |
| Store | **Redis** (predis client) | `dash_image_redis` container |
| Frontend client | **Laravel Echo** + **pusher‑js** | `kitchntabs-frontend/.../contexts/com/useLaravelEcho.tsx` |

---

## 3. Backend configuration

### 3.1 Broadcasting (`config/broadcasting.php`)

The active connection is `reverb` (selected by `BROADCAST_DRIVER=reverb`). This is
what the **backend uses to publish** events to the Reverb server:

```php
'reverb' => [
    'driver' => 'reverb',
    'key'    => env('REVERB_APP_KEY'),
    'secret' => env('REVERB_APP_SECRET'),
    'app_id' => env('REVERB_APP_ID'),
    'options' => [
        'host'   => env('REVERB_HOST', '127.0.0.1'),
        'port'   => env('REVERB_PORT', 443),
        'scheme' => env('REVERB_SCHEME', 'http'),
        'useTLS' => env('REVERB_SCHEME', 'http') === 'https',
    ],
],
```

### 3.2 Reverb server (`config/reverb.php`)

The **server bind** and the **app registry**:

```php
'servers' => [
  'reverb' => [
    'host' => env('REVERB_SERVER_HOST', '0.0.0.0'),
    'port' => env('REVERB_SERVER_PORT', 8080),   // dev: 25001
    'hostname' => env('REVERB_HOST'),
    'scaling' => [ 'enabled' => env('REVERB_SCALING_ENABLED', false), 'channel' => 'reverb', 'server' => [ /* redis */ ] ],
    ...
  ],
],
'apps' => [
  'provider' => 'config',          // NOTE: hardcoded 'config' (REVERB_APPS_DRIVER is ignored here)
  'apps' => [[
     'key'    => env('REVERB_APP_KEY'),     // <-- the `/app/<key>` the client connects to
     'secret' => env('REVERB_APP_SECRET'),
     'app_id' => env('REVERB_APP_ID'),
     'allowed_origins' => ['*', 'ws.kitchntabs.com', 'api.kitchntabs.com', 'localhost', ...],
  ]],
],
```

> ⚠️ **App‑key contract:** the client connects to `/app/<key>`. `<key>` **must equal**
> `REVERB_APP_KEY` (the `apps.provider` is `'config'`, so the registered key is taken
> straight from this env var). The platform's canonical key is **`dash`**. A mismatch
> produces a `4001 app-not-found` close right after the socket opens.

### 3.3 Channel authorization (`routes/channels.php`)

Private channels and their rules:

| Channel | Rule |
|---|---|
| `session.{sessionId}` | public — always allowed |
| `user.{id}` | `(int) $user->id === (int) $id` |
| `tenant.{tenantId}` | `$user->tenant_id == $tenantId` |
| `tenant.{tenantId}.system` | `$user->tenant_id == $tenantId` |
| `tenant.{tenantId}.chat` | `$user->tenant_id == $tenantId` |

### 3.4 Auth endpoint

```
POST /api/ws/auth   ->  App\Http\Controllers\DashBroadcastAuthController@authenticate
                        (logs to the `reverb` channel, then Broadcast::auth($request))
```

It is a thin wrapper over `Broadcast::auth()`; the frontend points Echo's
`authEndpoint` at it (see §4). `POST /api/broadcasting/auth` also exists as the
Laravel default.

### 3.5 Backend env reference (dev values)

From `dash-backend-docker/.env.local` (mounted into the container as `.env`):

```dotenv
APP_ENV=local
APP_URL=http://localhost
BROADCAST_DRIVER=reverb
QUEUE_CONNECTION=redis
SESSION_DRIVER=file
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_CLIENT=predis
REDIS_PASSWORD=********

# Reverb server (bind)
REVERB_SERVER=reverb
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=25001
REVERB_APPS_DRIVER=redis          # note: config/reverb.php uses provider 'config' regardless
REVERB_APPS_REDIS_CONNECTION=default
REVERB_APPS_REDIS_PREFIX=reverb:apps

# Reverb client/broadcaster + app credentials
REVERB_HOST=localhost
REVERB_PORT=25001
REVERB_SCHEME=http                # dev: http  -> ws ; prod: https -> wss
REVERB_APP_ID=mock_app
REVERB_APP_KEY=dash               # MUST match frontend VITE_APP_SOCKETS_KEY
REVERB_APP_SECRET=********
REVERB_APP_PING_INTERVAL=60
REVERB_APP_ACTIVITY_TIMEOUT=30
REVERB_APP_MAX_MESSAGE_SIZE=10000

# Prod TLS termination (only used when REVERB_SCHEME=https / behind ALB or local TLS)
REVERB_TLS_CERT=/opt/certs/certificate.crt
REVERB_TLS_KEY=/opt/certs/private.key
REVERB_TLS_CA=/opt/certs/ca_bundle.crt
```

---

## 4. Frontend configuration

### 4.1 The Echo client (`useLaravelEcho.tsx`)

`kitchntabs-frontend/packages/dash-admin/src/contexts/com/useLaravelEcho.tsx`
builds the pusher‑js/Echo config from env (`getEnv` reads `process.env['VITE_'+key]`):

```ts
const socketHostEnv = getEnv('APP_SOCKETS_HOST');
const socketScheme  = getEnv('APP_SOCKETS_SCHEME')?.toLowerCase();
const isSSL         = socketScheme === 'https';          // https -> wss + TLS
const wsHost        = socketHostEnv || window.location.hostname;
const portEnv       = getEnv('APP_SOCKETS_PORT');

const completeConfig = {
  broadcaster: 'pusher',
  key: getEnv('APP_SOCKETS_KEY') || 'dash',
  wsHost,
  ...(portEnv ? { wsPort: portEnv } : {}),     // empty port => pusher default (443 wss / 80 ws)
  forceTLS: isSSL,
  enabledTransports: isSSL ? ['wss', 'ws'] : ['ws'],
  cluster: 'mt1',
  // ...
};
// private channels:
completeConfig.authEndpoint = `${VITE_APP_BACKEND_URL}/api/ws/auth`;
completeConfig.auth = { headers: { Authorization: `Bearer ${token}`, Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' } };
```

Resulting URL: `<scheme>://<wsHost>:<wsPort>/app/<key>`.

### 4.2 Frontend env reference (kitchntabs‑system, dev)

`kitchntabs-frontend/apps/kitchntabs-system/.env.kitchntabs.local`:

```dotenv
VITE_ENV_PREFIX='VITE_'
VITE_APP_FRONTEND_URL=http://localhost:3008
VITE_APP_BACKEND_URL=http://localhost:25000      # used for /api/ws/auth + REST
VITE_APP_ADMIN_API_URL=http://localhost:25000/api

VITE_APP_SOCKETS_ENABLED=true
VITE_APP_SOCKETS_BROADCASTER=pusher
VITE_APP_SOCKETS_HOST=localhost
VITE_APP_SOCKETS_PORT=25001                      # Reverb's port (dev)
VITE_APP_SOCKETS_SCHEME=http                     # http -> ws ; https -> wss
VITE_APP_SOCKETS_KEY=dash                        # MUST match backend REVERB_APP_KEY
VITE_APP_SOCKETS_AUTH_ENDPOINT=api/ws/auth
```

> Vite reads env **only at dev‑server startup** — restart the frontend dev server
> after changing any `VITE_*` value.

---

## 5. SSL vs non‑SSL — the dev/prod split (read this)

This is the single most important section. The scheme/port must be consistent
across the client, the Reverb server, and any TLS‑terminating proxy.

### 5.1 Local development (no TLS) — `ws`

| Setting | Value | Why |
|---|---|---|
| Frontend `VITE_APP_SOCKETS_SCHEME` | `http` | → `ws://`, `forceTLS:false`, `enabledTransports:['ws']` |
| Frontend `VITE_APP_SOCKETS_HOST` | `localhost` | direct to Reverb |
| Frontend `VITE_APP_SOCKETS_PORT` | `25001` | Reverb's host‑mapped port (must NOT be empty) |
| Frontend `VITE_APP_SOCKETS_KEY` | `dash` | matches backend |
| Backend `REVERB_SCHEME` | `http` | server speaks plain ws |
| Backend `REVERB_SERVER_PORT` | `25001` | bind `0.0.0.0:25001`, mapped host→`25001` |
| Resulting URL | `ws://localhost:25001/app/dash` | ✅ |

There is **no reverse‑proxy for `/app`** in dev — the browser connects **directly**
to Reverb on `25001` (the HTTP app is a separate process on `25000`).

**Common dev mistake:** leaving `VITE_APP_SOCKETS_SCHEME=https` and/or
`VITE_APP_SOCKETS_PORT=''` produces `wss://localhost/app/dash` (port 443, TLS),
which fails with `net::ERR_CONNECTION_REFUSED` because nothing serves TLS on 443.

### 5.2 Production (TLS) — `wss`

| Setting | Value |
|---|---|
| Frontend `VITE_APP_SOCKETS_SCHEME` | `https` (→ `wss`) |
| Frontend `VITE_APP_SOCKETS_HOST` | `ws.kitchntabs.com` |
| Frontend `VITE_APP_SOCKETS_PORT` | `443` (must be set, not empty) |
| Backend `REVERB_SCHEME` | `https` |
| TLS | terminated at the ALB/edge (`:443`) **or** by Reverb directly via `REVERB_TLS_CERT/KEY/CA` |

In production the URL is `wss://ws.kitchntabs.com:443/app/dash`. TLS is typically
terminated by the load balancer; Reverb itself can also terminate TLS using the
`REVERB_TLS_*` cert paths when run with `--hostname`/scheme `https`.

### 5.3 Related HTTPS behaviors (Laravel side)

These affect **HTTP** URL generation (REST + the `/api/ws/auth` endpoint + media
URLs), not the socket scheme directly, but they share the same dev/prod logic:

- `App\Providers\AppServiceProvider::boot()` calls `URL::forceScheme('https')` only
  when `app()->environment('production')`, or the (forwarded) host contains
  `ngrok` / `trycloudflare.com` / `kitchntabs.com`, or `FORCE_HTTPS=true`.
  → In plain local dev it stays **http**.
- `App\Http\Middleware\TrustProxies` trusts **all** proxies (`$proxies = '*'`) and
  honors `X-Forwarded-Proto/Host/Port`, so URLs reflect the real edge host/port
  (e.g. `localhost:25000`) even though `APP_URL=http://localhost` omits the port.
- Media/file URLs use `url('/api/storage/...')` (env‑correct scheme) — see the
  separate storage docs. (Historically this used `secure_url()` which forced `https`
  and broke local http dev.)

---

## 6. Redis

Redis (`dash_image_redis`, predis client) backs several real‑time concerns:

- **Queues** — `QUEUE_CONNECTION=redis`. Broadcast events that implement
  `ShouldBroadcast` (vs `ShouldBroadcastNow`) are enqueued and delivered by workers.
- **Cache** — application cache.
- **Reverb app registry** — keys under `reverb:apps` (`REVERB_APPS_*`). Note the
  effective provider is `'config'` in `config/reverb.php`, so the app key still comes
  from `REVERB_APP_KEY`; the redis registry settings are present but the config
  provider is what's used.
- **Reverb scaling (optional, multi‑node)** — `REVERB_SCALING_ENABLED=true` makes
  Reverb publish/subscribe over Redis (`REVERB_SCALING_CHANNEL=reverb`) so multiple
  Reverb instances share connections/broadcasts. Off by default (single node).

`REDIS_HOST=redis`, `REDIS_PORT=6379`, `REDIS_CLIENT=predis`.

---

## 7. Queues & Horizon

- **Queue driver:** Redis (`QUEUE_CONNECTION=redis`).
- **Horizon** (`config/horizon.php`) supervises the workers. Defined supervisors and
  their queues (dev/local):

  | Supervisor (purpose) | Queues | Balance |
  |---|---|---|
  | default | `default`, `campaigns`, `campaign-publishing-phase` | simple |
  | imports | `products-import`, `products-import-preview` | simple |
  | ML notifications | `MlNotification` | auto |
  | packages | `Packages` | auto |
  | webhooks | `Webhooks` | auto |

- **Run:** `php artisan horizon` (dashboard at `/horizon`). Broadcasting and
  notifications that are queued flow through these workers before reaching Reverb.

---

## 8. Process model — Supervisor vs script‑managed

This trips people up: **only the web server is supervised inside the container.**

`/etc/supervisor/conf.d/supervisord.conf` (baked into the image) contains a single
program:

```ini
[program:php]
command=/usr/bin/php -S 0.0.0.0:80 -t /var/www/html/public .../server.php   ; i.e. `php artisan serve`
user=sail
```

**Reverb and Horizon are NOT supervised.** They are launched out‑of‑band by the dev
startup script in separate terminal windows:

```
dash-backend-docker/scripts/run-local-mac.sh   # opens Terminal windows running:
  • docker compose exec app php artisan reverb:start     (Reverb)
  • docker compose exec app php artisan horizon          (Horizon / queue workers)
  • ... test runners
```

**Consequence:** recreating the `app` container (`docker compose up -d app`) kills
Reverb and Horizon and **nothing restarts them**. Restart manually, e.g.:

```bash
# Reverb (background, like the script)
docker exec -d dash_image_app sh -c \
  'cd /var/www/html && php artisan reverb:start --host=0.0.0.0 --port=25001 >> storage/logs/reverb.log 2>&1'

# Horizon
docker exec -d dash_image_app sh -c 'cd /var/www/html && php artisan horizon >> storage/logs/laravel.log 2>&1'
```

> If you want these to survive restarts automatically, add `[program:reverb]` and
> `[program:horizon]` to Supervisor (or mount a custom `supervisord.conf`). This is a
> deliberate design choice today (separate terminals for live logs).

---

## 9. Dev startup & ports

**Start the stack with the script** (it exports `ENV_FILE` correctly — see §10):

```bash
cd dash-backend-docker
./scripts/run-local-mac.sh local     # default environment = "local"
```

It runs `docker compose up -d`, `php artisan migrate`, generates docs, then opens
Reverb / Horizon / test terminals.

**Port map (dev):**

| Service | Container | Host | Notes |
|---|---|---|---|
| Laravel HTTP (`artisan serve`) | `80` | `25000` | REST API + `/api/ws/auth` + `/api/storage` |
| Reverb (WebSocket) | `25001` | `25001` | direct ws endpoint `/app/<key>` |
| API docs (nginx) | `80` | `18010` | static docs |
| Frontend (kitchntabs‑system, Vite) | — | `3008` | `VITE_DEV_PORT`; HMR `4433` |
| Postgres / Redis / Mailhog | — | internal | compose services |

---

## 10. `ENV_FILE` gotcha (operational)

The compose `app` service mounts the Laravel env file via
`${ENV_FILE}:/var/www/html/.env`. The **real** dev env file is
`dash-backend-docker/.env.local` (resolved by the script as `.env.<environment>`).

- `scripts/run-local-mac.sh` **exports `ENV_FILE`** so Compose variable substitution
  uses the correct file. Shell env wins over the value in `dash-backend-docker/.env`.
- A bare `docker compose up` does **not** export it. If the default `ENV_FILE` points
  to a non‑existent path, Docker silently creates an **empty directory** at
  `/var/www/html/.env`, wiping the entire environment (symptoms: Postgres
  `no password supplied`, empty `REVERB_APP_KEY`, broken broadcasting).
- Prefer the script. The compose default has been corrected to `.env.local` so a bare
  `up` no longer destroys the env.

---

## 11. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `WebSocket connection to 'wss://localhost/app/dash' failed: ERR_CONNECTION_REFUSED` | Frontend using TLS scheme + no port in http dev | Set `VITE_APP_SOCKETS_SCHEME=http`, `VITE_APP_SOCKETS_PORT=25001`; restart Vite |
| Socket opens then immediately closes (`4001`) | App‑key mismatch | Make `REVERB_APP_KEY` == `VITE_APP_SOCKETS_KEY` (`dash`) |
| Connection refused on `25001` (any scheme) | Reverb not running | Start `php artisan reverb:start` (see §8); recreate kills it |
| Private channel subscribe fails (403) | Auth endpoint/token or channel rule | Check Bearer token, `VITE_APP_BACKEND_URL`, and `routes/channels.php`; logs on the `reverb` channel |
| Everything env‑broken after `docker compose up` | `.env` mounted as empty dir | Use the script / export `ENV_FILE=.env.local` (see §10) |
| Events never arrive but socket is connected | Queue/Horizon not running, or `BROADCAST_DRIVER` wrong | Start Horizon; confirm `BROADCAST_DRIVER=reverb`; check the queue the event uses |
| Media/REST URLs are `https` in http dev | `secure_url()`/`forceScheme` | Ensure local env (no ngrok host, `FORCE_HTTPS` unset); media now uses `url()` |

**Quick verification of the WS layer (server‑side):**

```bash
# Expect: HTTP/1.1 101 Switching Protocols + {"event":"pusher:connection_established", ...}
python3 - <<'PY'
import socket, base64, os
s = socket.create_connection(("localhost", 25001), timeout=6)
s.sendall((
  "GET /app/dash?protocol=7&client=js&version=8.5.0 HTTP/1.1\r\n"
  "Host: localhost:25001\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
  f"Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\n"
  "Sec-WebSocket-Version: 13\r\nOrigin: http://localhost:3008\r\n\r\n").encode())
data = s.recv(8192); head, _, rest = data.partition(b"\r\n\r\n")
print(head.split(b"\r\n")[0].decode()); print((rest or s.recv(8192))[:240])
PY
```

---

## 12. Configuration cross‑reference

| Concern | Backend var | Frontend var | Dev value | Prod value |
|---|---|---|---|---|
| WS scheme | `REVERB_SCHEME` | `VITE_APP_SOCKETS_SCHEME` | `http` (`ws`) | `https` (`wss`) |
| WS host | `REVERB_HOST` | `VITE_APP_SOCKETS_HOST` | `localhost` | `ws.kitchntabs.com` |
| WS port | `REVERB_PORT` / `REVERB_SERVER_PORT` | `VITE_APP_SOCKETS_PORT` | `25001` | `443` |
| App key | `REVERB_APP_KEY` | `VITE_APP_SOCKETS_KEY` | `dash` | `dash` |
| App secret | `REVERB_APP_SECRET` | — (never sent to client) | — | — |
| HTTP base (auth/REST) | `APP_URL` | `VITE_APP_BACKEND_URL` | `http://localhost:25000` | `https://api.kitchntabs.com` |
| Broadcast driver | `BROADCAST_DRIVER` | `VITE_APP_SOCKETS_BROADCASTER` | `reverb` / `pusher` | `reverb` / `pusher` |

### Key files

- `dash-backend/config/broadcasting.php` — broadcaster connections
- `dash-backend/config/reverb.php` — Reverb server + app registry + scaling
- `dash-backend/config/horizon.php` — queue supervisors
- `dash-backend/routes/channels.php` — private‑channel authorization
- `dash-backend/app/Http/Controllers/DashBroadcastAuthController.php` — `/api/ws/auth`
- `dash-backend/app/Providers/AppServiceProvider.php` — `forceScheme('https')` logic
- `dash-backend/app/Http/Middleware/TrustProxies.php` — proxy/scheme trust
- `kitchntabs-frontend/packages/dash-admin/src/contexts/com/useLaravelEcho.tsx` — Echo client
- `kitchntabs-frontend/apps/kitchntabs-system/.env.kitchntabs.local` — frontend dev env
- `dash-backend-docker/docker-compose.yml`, `dash-backend-docker/.env.local`, `dash-backend-docker/scripts/run-local-mac.sh` — dev stack

---

*Last updated: 2026‑06‑13.*
