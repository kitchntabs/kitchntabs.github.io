Deploy staging frontends (web/system/app) to Cloudflare Pages, pointed at api-dev/ws-dev
Context
Need three staging sites reachable at web-staging.kitchntabs.com, system-staging.kitchntabs.com, app-staging.kitchntabs.com — transpiled builds of kitchntabs-web, kitchntabs-system, and kitchntabs-app, deployed to Cloudflare Pages, but talking to the existing dev backend (api-dev.kitchntabs.com / ws-dev.kitchntabs.com) rather than a new backend.

This doesn't require inventing new infrastructure — production frontends are already deployed to Cloudflare Pages via a working, fully-automated script (kitchntabs-ci-cdk/scripts/deploy-frontend.js). This plan extends that exact mechanism with a staging variant, and adds three new per-app env files that are identical to production except for which backend they point at.

One fix already applied at your request: deploy-frontend.js and env-sync.js both referenced a stale sibling-repo name (kitchntabs-frontend-refactored) that doesn't exist — the real repo is kitchntabs-frontend. Both are now corrected.

⚠️ Critical constraint to confirm before proceeding
api-dev.kitchntabs.com and ws-dev.kitchntabs.com are not a standing AWS service — they're a Cloudflare Tunnel routed to http://localhost:25000 on a developer's own machine (confirmed via dash-backend-docker/scripts/cloudflare-tunnel.js's documented example and kitchntabs-ci-cdk/WORKSPACE_SETUP.md: "Backend similarly available at https://api-dev.kitchntabs.com via its own tunnel"). Concretely, this is the same dash_image_app container we've been using all session on port 25000.

This means the staging sites will only be able to reach the API while someone's local dev backend + tunnel is actively running (pnpm dash:start kitchntabs.tunnel --tunnel from dash-backend-docker, per this repo's CLAUDE.md). A Cloudflare Pages deployment is otherwise always-on, but it'll show network errors on every API call whenever that tunnel is down. If that's acceptable (e.g. for ad-hoc QA sessions where someone keeps their tunnel open), the plan below proceeds as-is. If you actually want an always-on backend, that's a materially different (larger) task — a real "dev" AWS stack — not covered here.

What's already in place (verified, no changes needed)
CORS: dash-backend/config/cors.php has allowed_origins_patterns with #^https://([a-z0-9-]+\.)?kitchntabs\.com$# — comment literally says "covers staging/preview subdomains". The three new *-staging.kitchntabs.com origins are already allowed.
Auth: confirmed bearer-token (Authorization: Bearer <token>, set in dash-frontend-core/packages/dash-axios-hook/src/hooks/useAxios.tsx), not cookie/Sanctum-stateful — so SANCTUM_STATEFUL_DOMAINS is not a blocker.
Build system: kitchntabs-frontend/build_config.js already treats MODE=staging as a first-class value (hard-validated against development|staging|production) and already recognizes a 'staging' bucket in customModeConfigs (debugMode true, hotReload false) — matched via the CUSTOM_MODE suffix, so CUSTOM_MODE=kitchntabs.staging resolves to it automatically. No build_config.js/vite.config.mts changes needed.
Deploy pipeline: kitchntabs-ci-cdk/scripts/deploy-frontend.js already does everything needed per app — builds via a configScript+buildScript pair, creates the Cloudflare Pages project if missing, deploys via wrangler pages deploy, attaches the custom domain, and upserts a proxied CNAME (domain → project.pages.dev). The environment CLI arg only selects which .env.<environment> supplies Cloudflare API credentials — it's account/zone-wide, so reusing production's credentials for a staging app deploy is correct, not a hack (same Cloudflare account, same kitchntabs.com zone).
Changes to make
1. kitchntabs-frontend — three new per-app env files
Each mirrors that app's own .env.kitchntabs.production file exactly (same feature flags, sidebar widths, recaptcha, etc.), with only the URL-related vars swapped to point at api-dev/ws-dev — using the same API/WS values already proven working in .env.kitchntabs.tunnel (VITE_APP_SOCKETS_PORT=443, SCHEME=https, KEY=dash, since ALB/tunnel terminates TLS the same way in both cases):

apps/kitchntabs-web/.env.kitchntabs.staging
apps/kitchntabs-app/.env.kitchntabs.staging
apps/kitchntabs-system/.env.kitchntabs.staging
VITE_ENV_PREFIX='VITE_'
VITE_APP_ENV='staging'

VITE_APP_FRONTEND_URL=https://{web|app|system}-staging.kitchntabs.com
VITE_APP_BACKEND_URL=https://api-dev.kitchntabs.com
VITE_APP_ADMIN_API_URL=https://api-dev.kitchntabs.com/api

VITE_APP_SOCKETS_HOST=ws-dev.kitchntabs.com
VITE_APP_SOCKETS_PORT=443
VITE_APP_SOCKETS_SCHEME=https
VITE_APP_SOCKETS_KEY=dash
VITE_APP_SOCKETS_ENABLED=true
VITE_APP_SOCKETS_BROADCASTER=pusher
VITE_APP_SOCKETS_AUTH_ENDPOINT=api/ws/auth

... (remainder copied verbatim from that app's own .env.kitchntabs.production —
     VITE_APP_DEFAULT_REDIRECT, VITE_LATEST_RELEASE_VERSION, VITE_HMR_HOST, VITE_DEV_HOST,
     VITE_APP_GETAUTH_ENDPOINT, sidebar widths, VITE_DASH_ADMIN_ROLE, tenant-logic flags,
     filters, recaptcha, and — for web/app only — VITE_APP_RELEASE_STAGE / PRERELEASE_INVITATION_CODE)
2. kitchntabs-frontend/package.json — three new build script pairs
Mirrors the existing :production triad pattern (e.g. line 20/80 for web) exactly, just with MODE=staging CUSTOM_MODE=kitchntabs.staging:

"config:web:kitchntabs-web:staging": "cross-env MODE=staging CUSTOM_MODE=kitchntabs.staging TARGET_TYPE=web PLATFORM=web APP_PATH=apps/kitchntabs-web node build_config.js",
"build:web:kitchntabs-web:staging": "pnpm config:web:kitchntabs-web:staging && pnpm prod-kt-web",
...and equivalently for kitchntabs-app (APP_PATH=apps/kitchntabs-app, reuses prod-kt-app) and kitchntabs-system (APP_PATH=apps/kitchntabs-system, reuses prod-kt-system). The existing prod-kt-* scripts are mode-agnostic (cd apps/X && pnpm build) — they just consume whatever build_config.json/env the config step wrote, so they're reused unchanged.

3. kitchntabs-ci-cdk/scripts/deploy-frontend.js — three new APPS entries
Add flat entries alongside the existing system/web/app keys (no restructuring of main() needed — environment keeps meaning "which .env.<environment> has the CF credentials", separate from which app keys get deployed):

'web-staging': {
  appDir: 'apps/kitchntabs-web',
  configScript: 'config:web:kitchntabs-web:staging',
  buildScript: 'prod-kt-web',
  pagesProject: 'kitchntabs-web-staging',
  domains: ['web-staging.kitchntabs.com'],
},
'system-staging': { appDir: 'apps/kitchntabs-system', configScript: 'config:web:kitchntabs-system:staging', buildScript: 'prod-kt-system', pagesProject: 'kitchntabs-system-staging', domains: ['system-staging.kitchntabs.com'] },
'app-staging': { appDir: 'apps/kitchntabs-app', configScript: 'config:web:kitchntabs-app:staging', buildScript: 'prod-kt-app', pagesProject: 'kitchntabs-app-staging', domains: ['app-staging.kitchntabs.com'] },
4. kitchntabs-ci-cdk/package.json — convenience scripts
"frontend:staging": "node scripts/deploy-frontend.js production web-staging system-staging app-staging",
"frontend:staging:web": "node scripts/deploy-frontend.js production web-staging",
"frontend:staging:system": "node scripts/deploy-frontend.js production system-staging",
"frontend:staging:app": "node scripts/deploy-frontend.js production app-staging",
Deliberately reuses production as the credentials arg — same Cloudflare account/zone, no new secrets file needed.

What I will NOT do without further explicit confirmation
Run pnpm frontend:staging — this is a real, external action: it creates live Cloudflare Pages projects and writes public DNS records. I'll prepare everything so it's a single command, but you (or I, with your go-ahead in a later turn) should run it deliberately, once .env.production's Cloudflare credentials are confirmed present on whichever machine runs it.
Anything about making api-dev/ws-dev a standing service — out of scope per the constraint above unless you say otherwise.
Verification
pnpm build:web:kitchntabs-web:staging (and system/app) locally first — confirms the new env files parse and apps/kitchntabs-web/dist/index.html is produced, before touching Cloudflare at all.
Start the local tunnel (pnpm dash:start kitchntabs.tunnel --tunnel from dash-backend-docker) so api-dev.kitchntabs.com/ws-dev.kitchntabs.com are actually reachable.
Run pnpm frontend:staging from kitchntabs-ci-cdk — watch for the three "✅ Frontend deployment complete" summary lines with https://*-staging.kitchntabs.com URLs.
Open each staging URL, confirm the app loads and a login round-trip succeeds (network tab shows api-dev.kitchntabs.com calls returning 200, not CORS/network errors).
Confirm DNS: dig web-staging.kitchntabs.com etc. should resolve to Cloudflare's proxy IPs.