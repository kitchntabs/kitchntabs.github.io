# Production Build & Deployment Technical Documentation

## Overview

This document describes the complete production build and deployment pipeline for the **KitchnTabs** application, covering the flow from source code to running AWS ECS Fargate containers.

The system consists of three main repositories:
- **dash-frontend** - React/ReactAdmin frontend application
- **dash-backend** - Laravel API backend with Docker containerization
- **kitchntabs-ci-cdk** - AWS CDK infrastructure as code

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION BUILD & DEPLOYMENT PIPELINE                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                           PHASE 1: BUILD ORCHESTRATION                              │
  │                           (kitchntabs-ci-cdk)                                       │
  │                                                                                     │
  │   pnpm deploy:prod                                                                  │
  │         │                                                                           │
  │         ├───────────────────────────┐                                               │
  │         │                           │                                               │
  │         ▼                           ▼                                               │
  │   ┌───────────────────┐      ┌───────────────────┐                                  │
  │   │  BUILD FRONTEND   │      │   VERSION BUMP    │                                  │
  │   │  (dash-frontend)  │      │  (dash-backend)   │                                  │
  │   └─────────┬─────────┘      └─────────┬─────────┘                                  │
  │             │                          │                                            │
  │             ▼                          ▼                                            │
  │   ┌───────────────────┐      ┌───────────────────┐                                  │
  │   │  apps/kitchntabs/ │      │  npm version      │                                  │
  │   │  dist/            │      │  minor            │                                  │
  │   └─────────┬─────────┘      │  git commit       │                                  │
  │             │                └─────────┬─────────┘                                  │
  │             │                          │                                            │
  │             └──────────┬───────────────┘                                            │
  │                        ▼                                                            │
  │              ┌───────────────────┐                                                  │
  │              │  UPDATE IMAGE_    │                                                  │
  │              │  VERSION in .env  │                                                  │
  │              └─────────┬─────────┘                                                  │
  │                        │                                                            │
  │                        ▼                                                            │
  │              ┌───────────────────┐                                                  │
  │              │  pnpm bk:production│                                                 │
  │              │  (CDK Deploy)      │                                                 │
  │              └───────────────────┘                                                  │
  └─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                           PHASE 2: DOCKER BUILD                                     │
  │                           (dash-backend)                                            │
  │                                                                                     │
  │   docker.build.sh --envFile kitchntabs --env production --public {frontend_dist}    │
  │         │                                                                           │
  │         ├─► Source .env.kitchntabs.production                                       │
  │         │                                                                           │
  │         ├─► Copy frontend dist → ./public/                                          │
  │         │                                                                           │
  │         ├─► docker build with ARM64 platform                                        │
  │         │     └─► Dockerfile                                                        │
  │         │           ├─► PHP 8.2-fpm-bullseye base                                   │
  │         │           ├─► Install dependencies (nginx, supervisor, redis, etc.)      │
  │         │           ├─► Copy application code                                       │
  │         │           ├─► Copy config templates (nginx, supervisor, php-fpm)          │
  │         │           └─► Set entrypoint.sh as CMD                                    │
  │         │                                                                           │
  │         ├─► Tag with latest + commit hash (e.g., 3d7c68b)                           │
  │         │                                                                           │
  │         └─► Push to ECR: kitchntabs-production:latest + :3d7c68b                    │
  │                                                                                     │
  └─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                           PHASE 3: CDK INFRASTRUCTURE DEPLOY                        │
  │                           (kitchntabs-ci-cdk)                                       │
  │                                                                                     │
  │   stackMgr.js bk production                                                         │
  │         │                                                                           │
  │         ├─► Load .env.production + .env.bk.production                               │
  │         │                                                                           │
  │         ├─► Check CDK bootstrap                                                     │
  │         │                                                                           │
  │         ├─► cdk synth (generate CloudFormation)                                     │
  │         │     └─► config/backend/production.ts                                      │
  │         │                                                                           │
  │         ├─► cdk diff (show changes)                                                 │
  │         │                                                                           │
  │         └─► cdk deploy                                                              │
  │               │                                                                     │
  │               ├─► VPC + Security Groups                                             │
  │               ├─► ECS Cluster (Fargate)                                             │
  │               ├─► ALB + Target Group (/api/healthz)                                 │
  │               ├─► Task Definition (ARM64, 256 CPU, 2GB RAM)                         │
  │               ├─► Fargate Service (FARGATE_SPOT)                                    │
  │               ├─► CloudWatch Log Group (14 days retention)                          │
  │               └─► Auto Scaling (CPU-based, 1-2 tasks)                               │
  │                                                                                     │
  └─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                           PHASE 4: CONTAINER RUNTIME                                │
  │                           (ECS Fargate Task)                                        │
  │                                                                                     │
  │   entrypoint.sh executes on container start                                         │
  │         │                                                                           │
  │         ├─► Download RDS CA Bundle                                                  │
  │         │                                                                           │
  │         ├─► Copy environment file (.env.kitchntabs.production → .env)               │
  │         │                                                                           │
  │         ├─► Detect ECS/Fargate platform → set PLATFORM=fargate                      │
  │         │                                                                           │
  │         ├─► replace_env_vars() for config templates:                                │
  │         │     ├─► redis.conf → /opt/redis-stable/redis.conf                         │
  │         │     ├─► custom-supervisor.conf → /etc/supervisor/conf.d/                  │
  │         │     ├─► nginx.conf → /etc/nginx/nginx.conf                                │
  │         │     ├─► api.nginx.conf → /etc/nginx/servers/                              │
  │         │     ├─► php.dash.ini.conf → /usr/local/etc/php/php.ini                    │
  │         │     └─► php-fpm-custom.conf → /usr/local/etc/php-fpm-custom.conf          │
  │         │                                                                           │
  │         ├─► Start supervisord (horizon, schedule:run, reverb)                       │
  │         │                                                                           │
  │         ├─► Start nginx                                                             │
  │         │                                                                           │
  │         ├─► Start php-fpm                                                           │
  │         │                                                                           │
  │         └─► exec tail -f /dev/null (keep-alive)                                     │
  │                                                                                     │
  └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Phase Breakdown

### Phase 1: Build Orchestration

**Entry Point:** `kitchntabs-ci-cdk/deploy-prod.sh`

```bash
pnpm deploy:prod
```

#### Step 1.1: Build Frontend

| Project | Command | Output |
|---------|---------|--------|
| dash-frontend | `pnpm build:web:kitchntabs:production` | `apps/kitchntabs/dist/` |

This builds the React/ReactAdmin frontend with production configuration from `.env.kitchntabs.production`.

#### Step 1.2: Version Bump

| Project | Command | Effect |
|---------|---------|--------|
| dash-backend | `npm version minor --no-git-tag-version` | Updates `package.json` version |
| dash-backend | `composer config version $(jq -r .version package.json)` | Updates `composer.json` version |
| dash-backend | `git commit -m "production deploy v.$VERSION"` | Commits version change |

#### Step 1.3: Update IMAGE_VERSION

The script captures the latest commit hash (6 digits) and updates:

```bash
# kitchntabs-ci-cdk/.env.bk.production
IMAGE_VERSION=3d7c68b  # Updated with latest commit hash
```

#### Step 1.4: Build Backend Docker Image

```bash
pnpm bk:production
# Triggers: docker.build.sh + CDK deploy
```

---

### Phase 2: Docker Build

**Script:** `dash-backend/docker.build.sh`

**Command:**
```bash
pnpm build:mac:prod --envFile kitchntabs --env production \
  --public /Users/farandal/DASH-PW-PROJECT/dash-frontend/apps/kitchntabs/dist
```

#### Environment Loading

```bash
# Sources: .env.kitchntabs.production
# Sets: ENV_FILENAME=env.kitchntabs.production
```

#### Build Arguments

| Argument | Value | Purpose |
|----------|-------|---------|
| `ENV` | production | Application environment |
| `ARCH` | arm64 | CPU architecture (M1/M2 Mac) |
| `PROJECT_NAME` | kitchntabs | Project identifier |
| `SERVER_NAME` | kitchntabs.com | Nginx server name |
| `ENV_FILENAME` | env.kitchntabs.production | Runtime env file selection |
| `CODEBUILD_BUILD_NUMBER` | 3d7c68b | Git commit hash (image tag) |

#### Docker Build Command

```bash
docker build \
  --platform linux/arm64 \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --cache-from ${CACHE_FROM} \
  --build-arg ENV=production \
  --build-arg ARCH=arm64 \
  --build-arg PROJECT_NAME=kitchntabs \
  --build-arg SERVER_NAME=kitchntabs.com \
  --build-arg ENV_FILENAME=env.kitchntabs.production \
  ... \
  -t kitchntabs-production:latest .
```

#### ECR Push

```bash
# Tag with latest
docker tag kitchntabs-production:latest \
  635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:latest

# Tag with commit hash
docker tag kitchntabs-production:latest \
  635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:3d7c68b

# Push both tags
docker push 635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:latest
docker push 635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:3d7c68b
```

---

### Phase 3: CDK Infrastructure Deploy

**Script:** `kitchntabs-ci-cdk/scripts/stackMgr.js`

**Command:** `pnpm bk:production` → `node scripts/stackMgr.js bk production`

#### Environment Files Loaded

1. `.env.production` - General production settings
2. `.env.bk.production` - Backend-specific settings

#### CDK Stack Configuration

**File:** `kitchntabs-ci-cdk/config/backend/production.ts`

#### AWS Resources Created/Updated

| Resource | Name Pattern | Configuration |
|----------|--------------|---------------|
| **VPC** | Default or custom | 2 Availability Zones |
| **ECS Cluster** | `KT-bk-production-cluster` | Fargate capacity provider |
| **Log Group** | `KT-bk-production-log-group` | 14 days retention |
| **ALB** | `KT-bk-production-alb` | Internet-facing, HTTPS redirect |
| **Target Group** | `KT-bk-production-tg` | Health check: `/api/healthz` |
| **Task Definition** | `KT-bk-production-task` | ARM64, 256 CPU, 2GB RAM |
| **Fargate Service** | `KT-bk-production-service` | FARGATE_SPOT, 1-2 tasks |

#### Health Check Configuration

```typescript
healthCheck: {
  path: '/api/healthz',
  interval: 300,      // 5 minutes
  timeout: 30,        // 30 seconds
  healthyThresholdCount: 2,
  unhealthyThresholdCount: 10,
  healthyHttpCodes: '200-499'  // Only fail on 5xx
}
```

#### Auto Scaling

```typescript
scaling.scaleOnCpuUtilization('CpuScaling', {
  targetUtilizationPercent: 95,
  scaleInCooldown: 120,    // 2 minutes
  scaleOutCooldown: 60     // 1 minute
});

// Capacity: 1 min, 2 max
```

#### Container Environment

```typescript
environment: {
  USE_SUPERVISOR: 'true',
  REDIS_SERVER: 'false'  // Uses external ElastiCache
}
```

---

### Phase 4: Container Runtime

**Script:** `dash-backend/docker/entrypoint.sh`

The entrypoint executes when the Fargate task starts and configures all services dynamically.

#### Runtime Configuration Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           ENTRYPOINT.SH EXECUTION FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  1. SECURITY SETUP
     │
     ├─► Download RDS CA Bundle → /tmp/rds-combined-ca-bundle.pem
     └─► Copy to ~/.postgresql/root.crt (for PostgreSQL SSL)

  2. ENVIRONMENT SETUP
     │
     ├─► Copy .env.kitchntabs.production → .env
     ├─► Export all variables from .env
     └─► Detect ECS metadata → set PLATFORM=fargate

  3. CONFIG TEMPLATE PROCESSING (replace_env_vars)
     │
     ├─► redis.conf
     │     Template: docker/app/redis.conf
     │     Output:   /opt/redis-stable/redis.conf
     │
     ├─► supervisor config
     │     Template: docker/app/custom-supervisor.conf
     │     Output:   /etc/supervisor/conf.d/custom-supervisor.conf
     │
     ├─► nginx.conf
     │     Template: docker/nginx/nginx.conf
     │     Output:   /etc/nginx/nginx.conf
     │
     ├─► api.nginx.conf
     │     Template: docker/nginx/api.nginx.conf
     │     Output:   /etc/nginx/servers/nginx.www.conf
     │
     ├─► php.ini
     │     Template: docker/app/php.dash.ini.conf
     │     Output:   /usr/local/etc/php/php.ini
     │
     └─► php-fpm.conf
           Template: docker/app/php-fpm-custom.conf
           Output:   /usr/local/etc/php-fpm-custom.conf

  4. SERVICE STARTUP
     │
     ├─► supervisord -c /etc/supervisor/supervisord.conf
     │     └─► Starts: horizon, schedule:run, reverb
     │
     ├─► nginx -c /etc/nginx/nginx.conf
     │     └─► Listens on ports 80, 443
     │
     └─► php-fpm --fpm-config /usr/local/etc/php-fpm-custom.conf
           └─► PHP FastCGI Process Manager

  5. KEEP-ALIVE
     │
     └─► exec tail -f /dev/null
           └─► Prevents container exit
```

---

## Configuration Files Reference

### Supervisor Configuration

**File:** `docker/app/custom-supervisor.conf`

```ini
[program:horizon]
process_name=dash-horizon
command=php /var/www/dash/artisan horizon
autostart=true
autorestart=true
user=dash
redirect_stderr=true
stdout_logfile=/dev/stdout  # Logs to CloudWatch via awslogs

[program:schedule-run]
process_name=dash-crontab
command=php /var/www/dash/artisan schedule:run
autostart=true
autorestart=true
user=dash
redirect_stderr=true
stdout_logfile=/dev/stdout

[program:reverb]
process_name=dash-reverb
command=php /var/www/dash/artisan reverb:start --host=127.0.0.1 --port=6001
autostart=true
autorestart=true
user=dash
redirect_stderr=true
stdout_logfile=/dev/stdout
```

### Nginx Configuration

**File:** `docker/nginx/api.nginx.conf`

```nginx
server {
    root /var/www/dash/public;
    client_max_body_size 128M;
    
    server_name ${SERVER_NAME} api.${PROJECT_DOMAIN};
    access_log /dev/stdout;   # Logs to CloudWatch
    error_log /dev/stderr;
    
    listen 80;
    listen [::]:80;
    
    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### Environment Variables Substitution

The `replace_env_vars()` function in entrypoint.sh:

1. Scans template file for `${VARIABLE}` patterns
2. Exports current environment values
3. Uses `envsubst` to replace placeholders
4. Writes processed config to target location

Example:
```bash
# Template: server_name ${SERVER_NAME};
# After:    server_name kitchntabs.com;
```

---

## Logging Architecture

The application uses a **dual-logging strategy** to ensure comprehensive observability:

1. **ECS awslogs Driver** - Captures all stdout/stderr from the container (primary method)
2. **CloudWatch Agent** - Collects application-specific log files for detailed monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           LOGGING FLOW TO CLOUDWATCH                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────────────────┐
  │                        ECS FARGATE TASK                                │
  │                                                                        │
  │   METHOD 1: STDOUT/STDERR (ECS awslogs driver)                        │
  │   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
  │   │   Laravel    │   │    Nginx     │   │  Supervisor  │              │
  │   │   App Logs   │   │ access/error │   │   Managed    │              │
  │   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘              │
  │          │                  │                  │                       │
  │          ▼                  ▼                  ▼                       │
  │   ┌──────────────────────────────────────────────────────────────┐    │
  │   │                       STDERR / STDOUT                        │    │
  │   │   (All services configured to log to /dev/stdout, /dev/stderr)│    │
  │   └──────────────────────────────────────────────────────────────┘    │
  │                                │                                       │
  │                                │ awslogs driver                        │
  │                                ▼                                       │
  │   ┌──────────────────────────────────────────────────────────────┐    │
  │   │  CloudWatch Log Group: kitchntabs-bk-production-loggroup     │    │
  │   │  Stream Prefix: kitchntabs-bk-production                     │    │
  │   └──────────────────────────────────────────────────────────────┘    │
  │                                                                        │
  │   METHOD 2: FILE-BASED (CloudWatch Agent)                             │
  │   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
  │   │ laravel.log  │   │ horizon.log  │   │ reverb.log   │              │
  │   │ notifs.log   │   │ artisan.log  │   │ nginx/*.log  │              │
  │   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘              │
  │          │                  │                  │                       │
  │          ▼                  ▼                  ▼                       │
  │   ┌──────────────────────────────────────────────────────────────┐    │
  │   │              CLOUDWATCH AGENT (onPremise mode)               │    │
  │   │   Config: /opt/aws/amazon-cloudwatch-agent/etc/              │    │
  │   └──────────────────────────────────────────────────────────────┘    │
  │                                │                                       │
  │                                ▼                                       │
  │   ┌──────────────────────────────────────────────────────────────┐    │
  │   │  Separate CloudWatch Log Groups per log type:                │    │
  │   │  • KT-bk-production-log-group-laravel                        │    │
  │   │  • KT-bk-production-log-group-horizon                        │    │
  │   │  • KT-bk-production-log-group-reverb                         │    │
  │   │  • KT-bk-production-log-group-artisan                        │    │
  │   │  • KT-bk-production-log-group-nginx                          │    │
  │   │  • KT-bk-production-log-group-notifications                  │    │
  │   │  • KT-bk-production-log-group-build                          │    │
  │   └──────────────────────────────────────────────────────────────┘    │
  │                                                                        │
  └────────────────────────────────────────────────────────────────────────┘
```

### CloudWatch Agent Configuration

The CloudWatch Agent is configured via `docker/app/amazon-cloudwatch-agent.json` and started in `entrypoint.sh`.

**Key Configuration Points:**

1. **Mode:** Uses `onPremise` mode (not `ec2`) to avoid IMDS dependency in Fargate
2. **Region:** Explicitly set via `${AWS_REGION}` environment variable
3. **Start Command:** Uses `amazon-cloudwatch-agent-ctl` wrapper

**File:** `docker/app/amazon-cloudwatch-agent.json`

```json
{
  "agent": {
    "metrics_collection_interval": 60,
    "run_as_user": "root",
    "region": "${AWS_REGION}"
  },
  "metrics": {
    "metrics_collected": {
      "cpu": { "measurement": ["cpu_usage_idle", "cpu_usage_user", "cpu_usage_system"] },
      "mem": { "measurement": ["mem_used_percent"] },
      "disk": { "measurement": ["used_percent"] }
    }
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/tmp/entrypoint_*.log",
            "log_group_name": "KT-bk-production-log-group-build",
            "log_stream_name": "{instance_id}-build"
          },
          {
            "file_path": "/var/www/dash/storage/logs/laravel.log",
            "log_group_name": "KT-bk-production-log-group-laravel",
            "log_stream_name": "{instance_id}-laravel",
            "multi_line_start_pattern": "^\\[[0-9]{4}-[0-9]{2}-[0-9]{2}"
          },
          {
            "file_path": "/var/log/supervisor/horizon.log",
            "log_group_name": "KT-bk-production-log-group-horizon",
            "log_stream_name": "{instance_id}-horizon"
          }
        ]
      }
    }
  }
}
```

**Startup in entrypoint.sh:**

```bash
# Configure and start CloudWatch Agent
if [ -f "${APP_DIR}/docker/app/amazon-cloudwatch-agent.json" ]; then
    echo "Configuring CloudWatch Agent..."
    sudo mkdir -p /opt/aws/amazon-cloudwatch-agent/etc/
    replace_env_vars "${APP_DIR}/docker/app/amazon-cloudwatch-agent.json" \
        "/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json"
    
    echo "Starting CloudWatch Agent..."
    # Use onPremise mode - works in Fargate without IMDS
    sudo -E /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
        -a fetch-config \
        -m onPremise \
        -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
        -s || echo "CloudWatch Agent failed to start, continuing..."
fi
```

### IAM Permissions for CloudWatch Agent

The ECS Task Role must include the `CloudWatchAgentServerPolicy` managed policy:

```typescript
// kitchntabs-ci-cdk/config/bk/production.ts
const executionRole = new iam.Role(stack, `${project}-${stackType}-${environment}-task-execution-role`, {
  assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
  managedPolicies: [
    iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonECSTaskExecutionRolePolicy'),
    iam.ManagedPolicy.fromAwsManagedPolicyName('CloudWatchAgentServerPolicy'),  // Required!
    // ... other policies
  ]
});

// Task Definition must use this role as BOTH executionRole AND taskRole
const taskDef = new ecs.FargateTaskDefinition(stack, `${project}-taskdef`, {
  executionRole,
  taskRole: executionRole,  // Required for CloudWatch Agent to authenticate
  // ...
});
```

### CloudWatch Agent vs awslogs Driver

| Feature | ECS awslogs Driver | CloudWatch Agent |
|---------|-------------------|------------------|
| **Setup** | Automatic via CDK | Manual in entrypoint.sh |
| **Log Source** | stdout/stderr only | Any file path |
| **Multi-line** | Limited | Full support with patterns |
| **Metrics** | None | CPU, Memory, Disk |
| **Log Groups** | Single | Multiple per log type |
| **Use Case** | General container logs | Application-specific logs |

---

## File Locations Summary

### kitchntabs-ci-cdk

| File | Purpose |
|------|---------|
| `deploy-prod.sh` | Main deployment orchestration script |
| `scripts/stackMgr.js` | CDK stack management |
| `bin/dash-serverless.ts` | CDK app entry point |
| `config/backend/production.ts` | Backend infrastructure definition |
| `.env.bk.production` | Backend stack environment variables |
| `.env.production` | General production environment |

### dash-backend

| File | Purpose |
|------|---------|
| `docker.build.sh` | Docker build and ECR push script |
| `Dockerfile` | Container image definition |
| `.env.kitchntabs.production` | Production Laravel configuration |
| `docker/entrypoint.sh` | Container startup script |
| `docker/app/custom-supervisor.conf` | Supervisor process definitions |
| `docker/app/amazon-cloudwatch-agent.json` | CloudWatch Agent configuration |
| `docker/nginx/api.nginx.conf` | Nginx server configuration |
| `docker/app/php-fpm-custom.conf` | PHP-FPM configuration |
| `docker/app/redis.conf` | Redis configuration template |

### dash-frontend

| File | Purpose |
|------|---------|
| `apps/kitchntabs/dist/` | Built frontend assets |
| `.env.kitchntabs.production` | Frontend production configuration |

---

## Quick Reference Commands

```bash
# Full production deploy (from kitchntabs-ci-cdk)
pnpm deploy:prod

# Backend only deploy (from kitchntabs-ci-cdk)
pnpm bk:production

# Build Docker image only (from dash-backend)
pnpm build:mac:prod --envFile kitchntabs --env production \
  --public /path/to/frontend/dist

# Build frontend only (from dash-frontend)
pnpm build:web:kitchntabs:production

# CDK diff (preview changes)
cdk diff --app "npx ts-node bin/dash-serverless.ts" --profile KitchenTabs

# CDK synth (generate CloudFormation)
cdk synth --app "npx ts-node bin/dash-serverless.ts" --profile KitchenTabs
```

---

## Environment Variables Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           ENVIRONMENT VARIABLES INHERITANCE                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  BUILD TIME                        DEPLOY TIME                      RUNTIME
  ──────────                        ───────────                      ───────

  dash-backend/                     kitchntabs-ci-cdk/               Container
  .env.kitchntabs.production        .env.bk.production               .env
        │                                 │                              │
        │                                 │                              │
        ▼                                 ▼                              ▼
  ┌──────────────┐               ┌──────────────┐               ┌──────────────┐
  │ Docker build │               │ CDK deploy   │               │ entrypoint   │
  │ arguments    │               │ parameters   │               │ exports      │
  │              │               │              │               │              │
  │ ENV          │               │ IMAGE_VERSION│               │ APP_ENV      │
  │ ARCH         │               │ MAX_CAPACITY │               │ DB_HOST      │
  │ SERVER_NAME  │               │ MIN_CAPACITY │               │ REDIS_HOST   │
  │ ENV_FILENAME │               │ TASK_CPU     │               │ etc.         │
  └──────────────┘               └──────────────┘               └──────────────┘
        │                                 │                              │
        │                                 │                              │
        ▼                                 ▼                              ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │                           RUNNING FARGATE TASK                            │
  │                                                                           │
  │   Container Environment = Build Args + Task Def Env + .env exports        │
  │                                                                           │
  └───────────────────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| ECR push fails | Not logged in to ECR | Run AWS ECR login command |
| CDK deploy fails | Bootstrap not done | Run `pnpm bootstrap` |
| Container unhealthy | Health check failing | Check `/api/healthz` endpoint |
| Logs not appearing | Wrong log destination | Verify stdout/stderr redirects |
| Config not applied | Template var not set | Check entrypoint.sh variable exports |
| CloudWatch Agent fails | Wrong mode for Fargate | Use `-m onPremise` not `-m ec2` |
| CloudWatch Agent: Region missing | IMDS not available | Set `region` in agent JSON config |
| CloudWatch Agent: TOML error | Config translation failed | Use `amazon-cloudwatch-agent-ctl` wrapper |

### CloudWatch Agent Troubleshooting

**Error: `Region info is missing for mode: ec2`**
```
E! failed to generate TOML configuration validation content: 
   [Under path : /agent/ruleRegion/ | Error : Region info is missing for mode: ec2]
```
**Cause:** Using `ec2` mode in Fargate where IMDS is not available.
**Solution:** 
1. Add `"region": "${AWS_REGION}"` to agent config
2. Use `-m onPremise` mode instead of `-m ec2`
3. Ensure `AWS_REGION` is passed to container environment

**Error: `dial tcp 169.254.169.254:80: connect: invalid argument`**
```
E! [EC2] Fetch hostname from EC2 metadata fail: RequestError: send request failed
```
**Cause:** Agent trying to contact EC2 Instance Metadata Service (unavailable in Fargate).
**Solution:** Use `onPremise` mode which doesn't require IMDS.

### Debugging Commands

```bash
# Check ECS service events
aws ecs describe-services --cluster KT-bk-production-cluster \
  --services KT-bk-production-service --profile KitchenTabs

# View CloudWatch logs (main container logs)
aws logs tail kitchntabs-bk-production-loggroup --follow --profile KitchenTabs

# View CloudWatch logs (Laravel application logs via agent)
aws logs tail kitchntabs-bk-production-loggroup-laravel --follow --profile KitchenTabs

# Execute command in running container
aws ecs execute-command --cluster KT-bk-production-cluster \
  --task <task-id> --container KT-bk-production-container \
  --interactive --command "/bin/bash" --profile KitchenTabs

# Check CloudWatch Agent status inside container
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m onPremise -a status
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-17 | Initial documentation |
| 1.1.0 | 2025-12-18 | Added CloudWatch Agent configuration and troubleshooting |


# SAMPLE LOG:

farandal@192 kitchntabs-ci-cdk % pnpm deploy:prod

> dash-serverless-cdk@1.0.0 deploy:prod /Users/farandal/DASH-PW-PROJECT/kitchntabs-ci-cdk
> chmod +x ./deploy-prod.sh && ./deploy-prod.sh

Now using node v20.19.6 (npm v10.8.2)

> dash-frontend@1.3.2 build:web:kitchntabs:production /Users/farandal/DASH-PW-PROJECT/dash-frontend
> MODE=production CUSTOM_MODE=kitchntabs.production TARGET_TYPE=web PLATFORM=web APP_PATH=apps/kitchntabs node build_config.js && vite build -c electron.vite.config.mts && cross-env NODE_ENV=production BUILD_ENV=prod CUSTOM_MODE=kitchntabs.production concurrently "cd apps/kitchntabs && pnpm build"

🔧 Generating build configuration...

📄 Loading env file: .env.kitchntabs.production

📋 Build Configuration:
========================
Mode: production
Target Type: web
Platform: web
Custom Mode: kitchntabs.production
App Path: apps/kitchntabs
Memory Limit: Default
Build ID: build-1766250429583-9u239i
Timestamp: 2025-12-20T17:07:09.583Z
API Base URL: https://api.kitchntabs.com
Sockets URL: N/A
Debug Mode: true

🔧 Environment Variables:
  VITE_APP_BACKEND_URL: https://api.kitchntabs.com
  VITE_APP_ADMIN_API_URL: https://api.kitchntabs.com/api
  VITE_APP_SOCKETS_HOST: ws.kitchntabs.com
  VITE_APP_SOCKETS_SCHEME: https
  VITE_APP_SOCKETS_KEY: dash
  VITE_DEV_PORT: 3006
  VITE_HMR_PORT: 3006
  VITE_HMR_HOST: localhost
========================

✅ Build configuration created successfully!
📁 Config file: /Users/farandal/DASH-PW-PROJECT/dash-frontend/build_config.json
🚀 Ready to build with the generated configuration!

💡 Suggested next steps:
   1. npm run build
   2. npm run deploy
📁 Electron build using APP_PATH: apps/kitchntabs
vite v7.2.6 building client environment for production...
✓ 1 modules transformed.
dist/index.html  0.18 kB │ gzip: 0.14 kB
✓ built in 32ms
vite v7.2.6 building client environment for production...
✓ 755 modules transformed.
apps/kitchntabs/dist-electron/main/index.js             0.21 kB │ gzip:   0.12 kB
apps/kitchntabs/dist-electron/main/index-yCHr6wtO.js  520.72 kB │ gzip: 107.62 kB
apps/kitchntabs/dist-electron/main/index-DfZQr6qI.js  905.94 kB │ gzip: 187.69 kB
✓ built in 2.04s
vite v7.2.6 building client environment for production...
✓ 1 modules transformed.
apps/kitchntabs/dist-electron/preload/index.js  3.61 kB │ gzip: 1.16 kB
✓ built in 20ms
[0] 
[0] > kitchntabs-app@1.0.0 build /Users/farandal/DASH-PW-PROJECT/dash-frontend/apps/kitchntabs
[0] > cross-env NODE_OPTIONS=--max-old-space-size=4048 npx vite build --emptyOutDir
[0] 
[0] === VITE BUILD CONFIGURATION ===
[0] 📋 Loaded build_config.json: build-1766250429583-9u239i
[0] MODE: production
[0] CUSTOM_MODE: kitchntabs.production
[0] TARGET_TYPE: web
[0] PLATFORM: web
[0] BUILD_ID: build-1766250429583-9u239i
[0] BUILD_TIMESTAMP: 2025-12-20T17:07:09.583Z
[0] DEBUG_MODE: true
[0] Process args: []
[0] Is Production Build: true
[0] Is Development Build: false
[0] ENV File Path: /Users/farandal/DASH-PW-PROJECT/dash-frontend/apps/kitchntabs/.env.kitchntabs.production
[0] 📂 Loading custom env file: /Users/farandal/DASH-PW-PROJECT/dash-frontend/apps/kitchntabs/.env.kitchntabs.production
[0] 📋 Loaded custom env vars: [
[0]   'VITE_ENV_PREFIX',
[0]   'VITE_APP_ENV',
[0]   'VITE_APP_FRONTEND_URL',
[0]   'VITE_APP_BACKEND_URL',
[0]   'VITE_APP_ADMIN_API_URL',
[0]   'VITE_APP_SOCKETS_HOST',
[0]   'VITE_APP_SOCKETS_PORT',
[0]   'VITE_APP_DEFAULT_REDIRECT',
[0]   'VITE_DEV_PORT',
[0]   'VITE_HMR_PORT',
[0]   'VITE_HMR_HOST',
[0]   'VITE_APP_GETAUTH_ENDPOINT',
[0]   'VITE_APP_SOCKETS_ENABLED',
[0]   'VITE_APP_SOCKETS_BROADCASTER',
[0]   'VITE_APP_SOCKETS_SCHEME',
[0]   'VITE_APP_SOCKETS_KEY',
[0]   'VITE_APP_SOCKETS_AUTH_ENDPOINT',
[0]   'VITE_SIDEBAR_WIDH',
[0]   'VITE_SIDEBAR_COLLAPSED_WIDH',
[0]   'VITE_DASH_ADMIN_ROLE',
[0]   'VITE_ENABLE_TENANT_LOGIC',
[0]   'VITE_ENABLE_TENANT_IMPERSONATION',
[0]   'VITE_ENABLE_LOGS_AND_NOTIFICATIONS',
[0]   'VITE_FILTERS_COLLAPSE_COUNT',
[0]   'VITE_FILTERS_COLLAPSE_SIZE',
[0]   'VITE_APP_RECAPTCHA_ENABLED',
[0]   'VITE_APP_RECAPTCHA_TOKEN',
[0]   'VITE_APP_OPENAI_API_KEY'
[0] ]
[0] Platform Detection: {
[0]   isAndroid: false,
[0]   isIOS: false,
[0]   isCapacitorBuild: false,
[0]   androidExists: true,
[0]   iosExists: false,
[0]   targetType: 'web',
[0]   platform: 'web'
[0] }
[0] Final MODE: production
[0] ENV Vars: {
[0]   DEBUG: false,
[0]   VITE_ENV_PREFIX: 'VITE_',
[0]   VITE_APP_ENV: 'production',
[0]   VITE_APP_FRONTEND_URL: 'https://panel.kitchntabs.com',
[0]   VITE_APP_BACKEND_URL: 'https://api.kitchntabs.com',
[0]   VITE_APP_ADMIN_API_URL: 'https://api.kitchntabs.com/api',
[0]   VITE_APP_SOCKETS_HOST: 'ws.kitchntabs.com',
[0]   VITE_APP_SOCKETS_PORT: '',
[0]   VITE_APP_DEFAULT_REDIRECT: '/',
[0]   VITE_DEV_PORT: '3006',
[0]   VITE_HMR_PORT: '3006',
[0]   VITE_HMR_HOST: 'localhost',
[0]   VITE_APP_GETAUTH_ENDPOINT: 'auth/getauth',
[0]   VITE_APP_SOCKETS_ENABLED: 'true',
[0]   VITE_APP_SOCKETS_BROADCASTER: 'pusher',
[0]   VITE_APP_SOCKETS_SCHEME: 'https',
[0]   VITE_APP_SOCKETS_KEY: 'dash',
[0]   VITE_APP_SOCKETS_AUTH_ENDPOINT: 'api/ws/auth',
[0]   VITE_SIDEBAR_WIDH: '280',
[0]   VITE_SIDEBAR_COLLAPSED_WIDH: '80',
[0]   VITE_DASH_ADMIN_ROLE: 'System',
[0]   VITE_ENABLE_TENANT_LOGIC: 'true',
[0]   VITE_ENABLE_TENANT_IMPERSONATION: 'true',
[0]   VITE_ENABLE_LOGS_AND_NOTIFICATIONS: 'false',
[0]   VITE_FILTERS_COLLAPSE_COUNT: '5',
[0]   VITE_FILTERS_COLLAPSE_SIZE: '0px',
[0]   VITE_APP_RECAPTCHA_ENABLED: 'false',
[0]   VITE_APP_RECAPTCHA_TOKEN: '6LfrqV0rAAAAAITchd4QEtbPgLwfME5xcGKTl1-H',
[0]   VITE_APP_OPENAI_API_KEY: '***REDACTED***',
[0]   VITE_APP_VERSION: '1.0.0',
[0]   VITE_BUILD_TIME: '2025-12-20T17:07:13.063Z',
[0]   VITE_BUILD_ID: 'build-1766250429583-9u239i',
[0]   VITE_BUILD_TIMESTAMP: '2025-12-20T17:07:09.583Z',
[0]   VITE_IS_ELECTRON: false,
[0]   VITE_PLATFORM: 'darwin',
[0]   VITE_IS_WINDOWS: false,
[0]   VITE_IS_MAC: true,
[0]   VITE_IS_LINUX: false,
[0]   VITE_IS_ANDROID: false,
[0]   VITE_IS_IOS: false,
[0]   VITE_IS_CAPACITOR: false,
[0]   VITE_IS_MOBILE: false,
[0]   VITE_CAPACITOR_PLATFORM: 'web',
[0]   VITE_ANDROID_AVAILABLE: true,
[0]   VITE_IOS_AVAILABLE: false,
[0]   VITE_PLATFORM_TYPE: 'web',
[0]   VITE_TARGET_TYPE: 'web',
[0]   VITE_CUSTOM_MODE: 'kitchntabs.production',
[0]   VITE_MEMORY_LIMIT: null,
[0]   VITE_BUILD_FRAMEWORK: 'react',
[0]   VITE_DEBUG_MODE: true,
[0]   VITE_HOT_RELOAD: true,
[0]   VITE_DEV_TOOLS: true,
[0]   VITE_MOCK_DATA: false,
[0]   VITE_APP_STORAGE_TYPE: 'localStorage'
[0] }
[0] === FINAL CONFIG ===
[0] Mode: production
[0] Is Mobile Build: false
[0] Is Desktop Build: false
[0] Is Capacitor Build: false
[0] External Modules: []
[0] Manual Chunks: [
[0]   'vendor-dayjs',
[0]   'vendor-react',
[0]   'vendor-mui',
[0]   'vendor-react-admin',
[0]   'vendor-dash',
[0]   'vendor-utils',
[0]   'vendor-heavy',
[0]   'dash-notifications',
[0]   'dash-communications',
[0]   'dash-theme'
[0] ]
[0] Platform Info: {
[0]   isAndroid: false,
[0]   isIOS: false,
[0]   isCapacitorBuild: false,
[0]   androidExists: true,
[0]   iosExists: false,
[0]   targetType: 'web',
[0]   platform: 'web'
[0] }
[0] Build Config Loaded: true
[0] Output Directory: ../dist/
[0] Target Framework: react
[0] Target Features: [ 'pwa', 'service-worker', 'web-apis' ]
[0] ====================
[0] vite v7.2.6 building client environment for production...
[0] 🔧 Building with config: build-1766250429583-9u239i
[0] 🌐 API Base URL: https://api.kitchntabs.com
[0] 🔧 VITE HMR CLIENT CONFIG 🔧
[0] clientHost: localhost
[0] protocol: wss
[0] path: /hmr/
[0] -----------------------------
[0] transforming...
[0] ✓ 56353 modules transformed.
[0] rendering chunks...
[0] computing gzip size...
[0] ../dist/build-info.json                                        0.18 kB │ gzip:   0.15 kB
[0] ../dist/index.html                                             2.03 kB │ gzip:   0.80 kB
[0] ../dist/assets/click2-CIgSKUUA.mp3                            12.96 kB
[0] ../dist/images/logo-horizontal-SsZkh9iR.png                   40.03 kB
[0] ../dist/assets/success-bQnasmkR.mp3                           50.88 kB
[0] ../dist/assets/modalError-VupVBq1T.mp3                        71.89 kB
[0] ../dist/assets/modalInfo-DxdOQoTt.mp3                         75.23 kB
[0] ../dist/images/logo-squared-BwWHkoFV.png                     109.16 kB
[0] ../dist/fonts/Montserrat-Black-MRZlm8li.ttf                  197.89 kB
[0] ../dist/fonts/Montserrat-Regular-D3UCWjz4.ttf                197.98 kB
[0] ../dist/fonts/Montserrat-Bold-nPtuWU9B.ttf                   198.07 kB
[0] ../dist/fonts/Montserrat-Medium-DW6Dzcuv.ttf                 198.10 kB
[0] ../dist/fonts/Montserrat-SemiBold-CoriCZkQ.ttf               198.20 kB
[0] ../dist/images/login-back-Dn8dDO05.png                       202.32 kB
[0] ../dist/assets/vendor-mui-BU3nLhQd.css                         0.03 kB │ gzip:   0.05 kB
[0] ../dist/assets/DateRangePicker-Bpo6JWfW.css                    2.10 kB │ gzip:   0.66 kB
[0] ../dist/assets/index-L6dxQ_--.css                            103.44 kB │ gzip:  20.09 kB
[0] ../dist/js/isComponent-Cyx7Gpf-.js                             0.25 kB │ gzip:   0.18 kB
[0] ../dist/js/PaginationComponent-LMXJvC0W.js                     0.25 kB │ gzip:   0.22 kB
[0] ../dist/js/useWindowSize-CHq8_i54.js                           0.32 kB │ gzip:   0.23 kB
[0] ../dist/js/notificationFormats-Dlqzmkx2.js                     0.39 kB │ gzip:   0.27 kB
[0] ../dist/js/validators-BUt32JA6.js                              0.49 kB │ gzip:   0.34 kB
[0] ../dist/js/ThemePallete-DKB6A6KS.js                            0.54 kB │ gzip:   0.29 kB
[0] ../dist/js/NotificationRenderer-BK0XXt7E.js                    0.55 kB │ gzip:   0.31 kB
[0] ../dist/js/NoResults-DTDh3puV.js                               0.56 kB │ gzip:   0.36 kB
[0] ../dist/js/StaticLayout-DsZQSUyT.js                            0.58 kB │ gzip:   0.32 kB
[0] ../dist/js/Legal-BNmkQG67.js                                   0.59 kB │ gzip:   0.35 kB
[0] ../dist/js/NotificationsWidget-C2IPkIIE.js                     0.63 kB │ gzip:   0.33 kB
[0] ../dist/js/SingleImageUploader-eD5xwFpZ.js                     0.66 kB │ gzip:   0.42 kB
[0] ../dist/js/ImagePlaceHolder-WLYKPHRz.js                        0.70 kB │ gzip:   0.42 kB
[0] ../dist/js/LogFileById-DmrItfvO.js                             0.83 kB │ gzip:   0.53 kB
[0] ../dist/js/DASHApp-CCgylIPA.js                                 0.86 kB │ gzip:   0.45 kB
[0] ../dist/js/MarketplaceCallback-B7dCAI3B.js                     0.93 kB │ gzip:   0.54 kB
[0] ../dist/js/ProductTemplateImportForm-CLDwHf_1.js               0.97 kB │ gzip:   0.54 kB
[0] ../dist/js/KitchnTabsPublicApp-_546pQkh.js                     1.09 kB │ gzip:   0.61 kB
[0] ../dist/js/ProductTemplateShow-W-jjn580.js                     1.13 kB │ gzip:   0.52 kB
[0] ../dist/js/ListActive-6naKlKa5.js                              1.13 kB │ gzip:   0.66 kB
[0] ../dist/js/useSize-RGhpazDe.js                                 1.36 kB │ gzip:   0.68 kB
[0] ../dist/js/MarketplaceTags-DyTwA5cC.js                         1.45 kB │ gzip:   0.85 kB
[0] ../dist/js/stockTypeResource-BGD4bbCJ.js                       1.50 kB │ gzip:   0.80 kB
[0] ../dist/js/Avatar-DOmMrdME.js                                  1.54 kB │ gzip:   0.79 kB
[0] ../dist/js/pricelistResource-B4eh-vK4.js                       1.60 kB │ gzip:   0.84 kB
[0] ../dist/js/brandResource-Cp1axmWj.js                           1.74 kB │ gzip:   0.84 kB
[0] ../dist/js/TrashTemplate-Cyg3U9B2.js                           1.82 kB │ gzip:   0.82 kB
[0] ../dist/js/productImportTemplateResource-s8C7xZXi.js           1.87 kB │ gzip:   0.97 kB
[0] ../dist/js/SignUpSuccess-XB2Ptq5r.js                           1.96 kB │ gzip:   1.02 kB
[0] ../dist/js/PriceStock-Dr22Kwg7.js                              1.96 kB │ gzip:   0.92 kB
[0] ../dist/js/currencyResource-AydeG1Ec.js                        2.07 kB │ gzip:   1.05 kB
[0] ../dist/js/ApplicationLayout-i54K7Noo.js                       2.09 kB │ gzip:   0.85 kB
[0] ../dist/js/Login-Bt5dDAxf.js                                   2.34 kB │ gzip:   1.19 kB
[0] ../dist/js/communeResource-CUrN6Rvb.js                         2.42 kB │ gzip:   1.18 kB
[0] ../dist/js/ImportMetadataButton-C0HVp8CZ.js                    2.44 kB │ gzip:   1.22 kB
[0] ../dist/js/countryResource-BxFBFTEK.js                         2.49 kB │ gzip:   1.23 kB
[0] ../dist/js/regionResource-Dkei8n-O.js                          2.51 kB │ gzip:   1.25 kB
[0] ../dist/js/ColorDisplayComponent-BhRe9Mrl.js                   2.51 kB │ gzip:   1.13 kB
[0] ../dist/js/MultiLevelTable-CrwUS9cu.js                         2.59 kB │ gzip:   1.22 kB
[0] ../dist/js/MuiSimpleJsonTable-D3ogDf1f.js                      2.61 kB │ gzip:   1.25 kB
[0] ../dist/js/MuiSimpleJsonTable-CcrtbLd6.js                      2.62 kB │ gzip:   1.25 kB
[0] ../dist/js/FileSaver.min-BrLJoCrD.js                           2.63 kB │ gzip:   1.24 kB
[0] ../dist/js/DASHModal-DtchLjXV.js                               2.70 kB │ gzip:   1.04 kB
[0] ../dist/js/SystemRequestsCache-BqeCkSRH.js                     3.00 kB │ gzip:   1.09 kB
[0] ../dist/js/DASHLanding-qncFAKy5.js                             3.14 kB │ gzip:   1.51 kB
[0] ../dist/js/metadataFormatsResource-DsCSIkQI.js                 3.23 kB │ gzip:   1.29 kB
[0] ../dist/js/DashAutoFormMuiTabs-BeVCI2T8.js                     3.99 kB │ gzip:   0.84 kB
[0] ../dist/js/campaignResource-C0Bg09Y4.js                        4.31 kB │ gzip:   1.69 kB
[0] ../dist/js/Register-DUjSKiDA.js                                4.41 kB │ gzip:   1.58 kB
[0] ../dist/js/index-5DBVETjT.js                                   4.47 kB │ gzip:   1.92 kB
[0] ../dist/js/Profile-DfXKJnXO.js                                 5.36 kB │ gzip:   2.02 kB
[0] ../dist/js/index.es--hapEEOP.js                                5.82 kB │ gzip:   1.80 kB
[0] ../dist/js/color-thief-Cf9SoGPP.js                             6.43 kB │ gzip:   2.76 kB
[0] ../dist/js/ResourceTemplate-BHG1eGa7.js                        6.68 kB │ gzip:   1.83 kB
[0] ../dist/js/userResource-Dpg4TRqQ.js                            6.74 kB │ gzip:   2.09 kB
[0] ../dist/js/recaptcha-wrapper-BMNnJ0EE.js                       7.53 kB │ gzip:   2.54 kB
[0] ../dist/js/pointOfSaleResource-CT_DFcxp.js                     7.87 kB │ gzip:   3.04 kB
[0] ../dist/js/MallResources-DICD2SWs.js                           8.51 kB │ gzip:   3.30 kB
[0] ../dist/js/systemPointOfSaleResource-Q_VNop-4.js               8.92 kB │ gzip:   3.60 kB
[0] 
[0] (!) Some chunks are larger than 500 kB after minification. Consider:
[0] - Using dynamic import() to code-split the application
[0] - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
[0] - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
[0] ../dist/js/systemMarketplaceResource-D_btNQZ2.js               9.05 kB │ gzip:   3.64 kB
[0] ../dist/js/numeral-C9zNYX4V.js                                11.44 kB │ gzip:   4.02 kB
[0] ../dist/js/CampaignResourceTemplate-BuKeqP4w.js               11.88 kB │ gzip:   4.05 kB
[0] ../dist/js/marketplaceResource-D9PApM7g.js                    12.14 kB │ gzip:   4.36 kB
[0] ../dist/js/modifiersResource-B7AWXx30.js                      12.23 kB │ gzip:   3.93 kB
[0] ../dist/js/SignUp-CJTalEuk.js                                 13.47 kB │ gzip:   4.43 kB
[0] ../dist/js/useBreakpoint-BOhJCiLv.js                          14.11 kB │ gzip:   5.56 kB
[0] ../dist/js/vendor-dayjs-DNnzKjeE.js                           14.51 kB │ gzip:   5.90 kB
[0] ../dist/js/SizeContext-CxilhqQa.js                            14.77 kB │ gzip:   5.32 kB
[0] ../dist/js/profileResource-CbgPJGxH.js                        19.16 kB │ gzip:   3.24 kB
[0] ../dist/js/index-CAoR8tE5.js                                  20.80 kB │ gzip:   7.20 kB
[0] ../dist/js/systemResources-C_2WGoYu.js                        22.11 kB │ gzip:   6.46 kB
[0] ../dist/js/MUIHtmlToolTip-B-ws61ur.js                         23.28 kB │ gzip:   7.64 kB
[0] ../dist/js/ecommerceTenantResource-B72DYJ93.js                23.91 kB │ gzip:   6.59 kB
[0] ../dist/js/index-08eqRuI7.js                                  25.58 kB │ gzip:  10.19 kB
[0] ../dist/js/index-Cmq5oTgA.js                                  29.35 kB │ gzip:   9.98 kB
[0] ../dist/js/DashResourceContext-C31ebKTA.js                    31.43 kB │ gzip:   8.81 kB
[0] ../dist/js/cashCountResource-lfBtVcGV.js                      33.94 kB │ gzip:   7.68 kB
[0] ../dist/js/CampaignEdit-BA7o3Aei.js                           35.76 kB │ gzip:   9.19 kB
[0] ../dist/js/DateRangePicker-BP6ZuKdH.js                        42.12 kB │ gzip:  15.81 kB
[0] ../dist/js/ProductResourceHelper-Bjq_iQBk.js                  46.83 kB │ gzip:  12.22 kB
[0] ../dist/js/presets-fizG0Mr_.js                                50.52 kB │ gzip:  19.95 kB
[0] ../dist/js/Tooltip-DRh87a7c.js                                56.60 kB │ gzip:  18.99 kB
[0] ../dist/js/index-CeRuh80h.js                                  59.60 kB │ gzip:  21.53 kB
[0] ../dist/js/moment-D0ql__SF.js                                 60.66 kB │ gzip:  19.62 kB
[0] ../dist/js/index-CJ09Zn0z.js                                  64.64 kB │ gzip:  16.75 kB
[0] ../dist/js/vendor-react-router-00p4bJC3.js                    87.67 kB │ gzip:  29.66 kB
[0] ../dist/js/galleryResource-Bo4qnlzi.js                       104.59 kB │ gzip:  33.66 kB
[0] ../dist/js/categoryResource-BsQui42z.js                      125.46 kB │ gzip:  33.03 kB
[0] ../dist/js/productResource-D01amkB2.js                       127.32 kB │ gzip:  36.85 kB
[0] ../dist/js/KitchnTabsPrivateApp-C-rfWa7b.js                  152.44 kB │ gzip:  44.25 kB
[0] ../dist/js/tabResource-y2Xuebxo.js                           165.94 kB │ gzip:  46.67 kB
[0] ../dist/js/Tree-CcNbWzTs.js                                  166.72 kB │ gzip:  57.38 kB
[0] ../dist/js/vendor-utils-B0fxPkfN.js                          180.81 kB │ gzip:  66.94 kB
[0] ../dist/js/vendor-react-U4Grg_rV.js                          194.41 kB │ gzip:  60.83 kB
[0] ../dist/js/KitchnTabsBootstrap-rti-FkMs.js                   240.17 kB │ gzip:  69.28 kB
[0] ../dist/js/ProductTemplateImportFormComponent-BvRaMLVz.js    283.44 kB │ gzip:  83.44 kB
[0] ../dist/js/main-BjuAVpuj.js                                  333.39 kB │ gzip: 100.26 kB
[0] ../dist/js/vendor-heavy-BDgXIY2F.js                          340.13 kB │ gzip: 111.81 kB
[0] ../dist/js/productImportInstanceResource-hkkeKPoy.js         483.85 kB │ gzip: 140.11 kB
[0] ../dist/js/vendor-react-admin-BTL-zkJc.js                    662.64 kB │ gzip: 170.92 kB
[0] ../dist/js/index-oWXQTSin.js                                 936.46 kB │ gzip: 338.72 kB
[0] ../dist/js/vendor-mui-yByF2K8H.js                          1,835.89 kB │ gzip: 541.30 kB
[0] ✓ built in 1m 30s
[0] cd apps/kitchntabs && pnpm build exited with code 0
v1.50.0
[development 80ba11b] production deploy v.1.50.0
 2 files changed, 2 insertions(+), 2 deletions(-)

> dash-backend-helper@1.50.0 build:mac:prod /Users/farandal/DASH-PW-PROJECT/dash-backend
> chmod +x ./docker.build.sh && ./docker.build.sh --arch arm64 "--envFile" "kitchntabs" "--env" "production" "--public" "/Users/farandal/DASH-PW-PROJECT/dash-frontend/apps/kitchntabs/dist" "--yes"

Sourcing .env.kitchntabs.production file
ENV_FILENAME not provided, setting to env.kitchntabs.production
> ARGUMENTS:
SKIP_BUILD: false
SKIP_PUSH: false
SKIP_SOURCING: false
SKIP_PULL: false
ENV: production
ENV_FILE: kitchntabs
ECR_REPOSITORY: kitchntabs-production
ECR_REGION: us-east-2
SERVER_NAME: localhost
ENV_FILENAME: env.kitchntabs.production
CODEBUILD_BUILD_NUMBER not set. Using latest git commit hash: 80ba11b
> BUILD PARAMS:
PROJECT_NAME kitchntabs
ECR_REPOSITORY kitchntabs-production
AWS_ACCOUNT 635862864028
AWS_DEFAULT_REGION us-east-2
ENV production
SERVER_NAME localhost
CODEBUILD_BUILD_NUMBER 80ba11b
Using architecture: arm64

Logging in to Amazon ECR...
aws ecr get-login-password --region us-east-2 --profile KitchnTabs | docker login --username AWS --password-stdin 635862864028.dkr.ecr.us-east-2.amazonaws.com
Login Succeeded
latest: Pulling from kitchntabs-production
Digest: sha256:9e2bcb2684318cd0f553c53b76d34a4636d309b5630c4f7c0dc677d86a055cae
Status: Image is up to date for 635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:latest
635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:latest
Copied contents of /Users/farandal/DASH-PW-PROJECT/dash-frontend/apps/kitchntabs/dist to ./public
> BUILDING DOCKER IMAGE...
About to run the following command:

docker build     --platform linux/arm64     --build-arg BUILDKIT_INLINE_CACHE=1 --cache-from 635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:latest     --build-arg ENV=production     --build-arg ARCH=arm64     --build-arg PROJECT_NAME=kitchntabs     --build-arg HOST_NAME=localhost     --build-arg HTTP_PORT=80     --build-arg HTTPS_PORT=443     --build-arg SERVER_NAME=localhost     --build-arg PHP_PORT=9000     --build-arg USER=dash     --build-arg USER_PASSWORD=dash1234..!     --build-arg GROUP=www-data     --build-arg APP_DIR=/var/www/dash/     --build-arg CODEBUILD_BUILD_NUMBER=80ba11b     --build-arg AWS_DEFAULT_REGION=us-east-2     --build-arg AWS_ACCESS_KEY_ID=***REDACTED***     --build-arg AWS_SECRET_ACCESS_KEY=***REDACTED***     --build-arg ENV_FILENAME=env.kitchntabs.production     -t kitchntabs-production:latest .

Auto-confirming build (--yes flag provided)
8.2-fpm-bullseye: Pulling from library/php
Digest: sha256:e0d898e694202df3327dd9945792202de12798f8d0969ab6b44d3163c2b033b2
Status: Image is up to date for php:8.2-fpm-bullseye
docker.io/library/php:8.2-fpm-bullseye
[+] Building 413.2s (92/92) FINISHED                                                                     
 => [internal] load build definition from Dockerfile                                                0.0s
 => => transferring dockerfile: 37B                                                                 0.0s
 => [internal] load .dockerignore                                                                   0.0s
 => => transferring context: 35B                                                                    0.0s
 => [internal] load metadata for docker.io/library/php:8.2-fpm-bullseye                             0.0s
 => importing cache manifest from 635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-producti  0.1s
 => [ 1/85] FROM docker.io/library/php:8.2-fpm-bullseye                                             0.0s
 => [internal] load build context                                                                  12.4s
 => => transferring context: 18.58MB                                                               12.0s
 => CACHED [ 2/85] WORKDIR /var/www/dash/                                                           0.0s
 => [ 3/85] RUN dpkg --configure -a                                                                 2.6s
 => [ 4/85] RUN apt-get autoclean && apt-get update && apt-get upgrade -y && apt-get -u dist-upgr  17.1s
 => [ 5/85] RUN apt-get install -y software-properties-common     build-essential     openssh-ser  72.4s
 => [ 6/85] RUN apt-get install -y wget ca-certificates                                             1.6s 
 => [ 7/85] RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-ke  3.0s 
 => [ 8/85] RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg m  0.3s 
 => [ 9/85] RUN apt-get update && apt-get install -y postgresql-client                              6.5s 
 => [10/85] RUN ARCH=$(uname -m) &&     if [ "arm64" = "aarch64" ] || [ "arm64" = "arm64" ]; then   9.2s 
 => [11/85] RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - &&     apt-get install   12.3s 
 => [12/85] WORKDIR /tmp                                                                            0.1s 
 => [13/85] RUN ARCH=$(uname -m) &&     if [ "arm64" = "aarch64" ] || [ "arm64" = "arm64" ]; then   8.9s 
 => [14/85] WORKDIR /opt                                                                            0.1s 
 => [15/85] RUN curl -o redis-stable.tar.gz http://download.redis.io/redis-stable.tar.gz            0.6s 
 => [16/85] RUN tar xvzf redis-stable.tar.gz                                                        0.8s 
 => [17/85] WORKDIR /opt/redis-stable                                                               0.0s 
 => [18/85] RUN make distclean                                                                      0.8s 
 => [19/85] RUN make BUILD_TLS=yes                                                                 89.6s 
 => [20/85] RUN ln -s /opt/redis-stable/src/redis-cli /usr/bin/redis-cli                            0.2s 
 => [21/85] RUN rm -rf ../redis-stable.tar.gz                                                       0.1s 
 => [22/85] RUN apt-get install wkhtmltopdf -y                                                     16.9s 
 => [23/85] RUN apt install pdftk -y                                                               11.0s 
 => [24/85] RUN docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql                         4.7s 
 => [25/85] RUN apt-get update && apt-get install -y     libjpeg-dev     libpng-dev     libfreetyp  2.8s 
 => [26/85] RUN docker-php-ext-configure gd --with-jpeg --with-freetype                             1.9s 
 => [27/85] RUN docker-php-ext-install pdo pdo_mysql pdo_pgsql pgsql mbstring exif pcntl bcmath g  70.4s 
 => [28/85] RUN apt-get update && apt-get install -y libssl-dev     && pecl download redis     &&  14.6s 
 => [29/85] RUN php -r "echo 'phpredis TLS support: ' . (defined('Redis::OPT_TLS_CONTEXT') ? 'ENAB  0.2s 
 => [30/85] RUN docker-php-source delete                                                            0.1s
 => [31/85] RUN apt-get clean && rm -rf /var/lib/apt/lists/*                                        0.2s
 => [32/85] RUN /bin/bash -c 'echo "Architecture System: $(uname -m)"'                              0.1s
 => [33/85] RUN echo "Architecture Arg: arm64"                                                      0.2s
 => [34/85] WORKDIR /var/www/dash/                                                                  0.0s
 => [35/85] RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin -  4.1s
 => [36/85] RUN if [ "www-data" != "www-data" ]; then groupadd -g ${USER_UUID} www-data; fi         0.2s
 => [37/85] RUN useradd -u 1000 -ms /bin/bash -g www-data -p $(openssl passwd -crypt dash1234..!)   0.2s
 => [38/85] RUN usermod -aG sudo dash                                                               0.2s
 => [39/85] RUN mkdir -p /home/dash                                                                 0.1s
 => [40/85] RUN chown -R dash:www-data /home/dash                                                   0.1s
 => [41/85] RUN chmod -R 755 /home/dash                                                             0.1s
 => [42/85] RUN mkdir -p /opt/certs/                                                                0.2s
 => [43/85] COPY ./docker/certs/kitchntabs/* /opt/certs/                                            0.0s
 => [44/85] RUN chmod 644 /opt/certs/*                                                              0.2s
 => [45/85] COPY ./docker/entrypoint.sh /etc/entrypoint.sh                                          0.0s
 => [46/85] COPY ./docker/app/functions.sh /etc/functions.sh                                        0.0s
 => [47/85] COPY ./docker/app/gitconfig.conf /var/www/dash/.gitconfig                               0.0s
 => [48/85] RUN echo "dash ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/user_sudo                      0.1s
 => [49/85] RUN chmod 440 /etc/sudoers.d/user_sudo                                                  0.2s
 => [50/85] COPY --chown=dash:www-data . /var/www/dash/                                            17.4s
 => [51/85] RUN chmod 775 /var/www/dash/                                                            0.4s
 => [52/85] RUN chmod 775 -R /var/www/dash//bootstrap/cache                                         0.1s
 => [53/85] RUN if [ ! -d "/var/www/dash/vendor" ]; then mkdir /var/www/dash/vendor;  fi            0.1s
 => [54/85] RUN chmod 775 /var/www/dash/vendor                                                      0.1s
 => [55/85] RUN mkdir /etc/nginx/servers                                                            0.2s
 => [56/85] RUN mkdir /etc/nginx/configs                                                            0.2s
 => [57/85] COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf                                    0.0s
 => [58/85] COPY ./docker/app/cacert.pem /usr/local/etc/php/conf.d/cacert.pem                       0.0s
 => [59/85] RUN mkdir /var/run/php                                                                  0.1s
 => [60/85] RUN chmod 775 /var/run/php                                                              0.1s
 => [61/85] RUN mkdir /usr/local/etc/php-fpm-custom.d                                               0.1s
 => [62/85] RUN chmod 775 /usr/local/etc/php-fpm-custom.d                                           0.2s
 => [63/85] RUN touch /var/www/dash/storage/logs/laravel.log                                        0.1s
 => [64/85] RUN chmod 777 /var/www/dash/storage/logs/laravel.log                                    0.1s
 => [65/85] RUN touch /var/www/dash/storage/logs/supervisor-artisan.log                             0.2s
 => [66/85] RUN chmod 777 /var/www/dash/storage/logs/supervisor-artisan.log                         0.2s
 => [67/85] RUN touch /var/www/dash/storage/logs/supervisor-schedule.log                            0.2s
 => [68/85] RUN chmod 777 /var/www/dash/storage/logs/supervisor-schedule.log                        0.1s
 => [69/85] RUN touch /var/www/dash/storage/logs/supervisor-horizon.log                             0.1s
 => [70/85] RUN chmod 777 /var/www/dash/storage/logs/supervisor-horizon.log                         0.2s
 => [71/85] RUN chmod 777 /var/www/dash/storage/logs                                                0.1s
 => [72/85] RUN mkdir -p /home/dash/.aws                                                            0.2s
 => [73/85] RUN chown -R dash:www-data /home/dash/.aws                                              0.3s
 => [74/85] RUN chmod -R 700 /home/dash/.aws                                                        0.2s
 => [75/85] WORKDIR /var/www/dash/                                                                  0.0s
 => [76/85] RUN git config --global --add safe.directory /var/www/dash/                             0.1s
 => [77/85] RUN composer install --no-interaction --optimize-autoloader                             6.4s
 => [78/85] RUN chown -R dash:www-data /home/dash                                                   0.2s
 => [79/85] RUN mkdir -p /usr/local/etc/php-fpm-custom.d                                            0.1s
 => [80/85] RUN chown dash:www-data /usr/local/etc/php-fpm-custom.d                                 0.1s
 => [81/85] RUN touch /home/dash/.gitconfig                                                         0.1s
 => [82/85] RUN chmod 644 /home/dash/.gitconfig                                                     0.1s
 => [83/85] RUN git config --global --add safe.directory /var/www/dash/                             0.2s
 => [84/85] RUN php artisan horizon:install                                                         0.5s
 => [85/85] RUN php artisan storage:link                                                            0.4s
 => exporting to image                                                                              0.0s
 => => exporting layers                                                                             0.0s
 => => writing image sha256:94e3e51d4a2e8f800220bc0b2d87644efe09678d726146f63956f87227b3755e        0.0s
 => => naming to docker.io/library/kitchntabs-production:latest                                     0.0s
 => exporting cache                                                                                 0.0s
 => => preparing build cache for export                                                             0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
Checking if ECR repository exists...
Repository kitchntabs-production already exists.
Tagging Docker image...
Pushing Docker image to ECR... docker push 635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:latest
The push refers to repository [635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production]
d386f609225c: Preparing 
4341f9e6b728: Preparing 
09c5c41cbc96: Preparing 
10ba16172a43: Preparing 
c64bc3043ad4: Preparing 
81c4006cd554: Preparing 
a30e24214d6f: Preparing 
30ae41dc3f5e: Preparing 
fe09a8c8f343: Preparing 
5f70bf18a086: Preparing 
d05d38e33f88: Preparing 
0f22958d502c: Preparing 
5f70bf18a086: Preparing 
e4820370deaf: Preparing 
76bb7cca8751: Preparing 
518589a36ffc: Preparing 
448f558f6993: Preparing 
f28b51ca2d79: Preparing 
e3087344a47b: Preparing 
91823f4f4583: Preparing 
7ed5a987d5e0: Preparing 
cda577118532: Preparing 
fc16b9768200: Preparing 
7a6087f79f5e: Preparing 
c77b8aa22bb5: Preparing 
b4a822997280: Preparing 
5f70bf18a086: Preparing 
71be4d4a0c62: Preparing 
5f70bf18a086: Preparing 
5f70bf18a086: Preparing 
9b3fe0dbb4dd: Preparing 
76ad2537bcf0: Preparing 
c612ce796987: Preparing 
4a9bcba846c4: Preparing 
ea95a7e540ca: Preparing 
25d32df78d9c: Preparing 
ee2b6926d13b: Preparing 
b06d29c93765: Preparing 
e61943dddbb6: Preparing 
b9197c6d6f09: Preparing 
5f70bf18a086: Preparing 
9787ad0c4bf0: Preparing 
10cbd633df7d: Preparing 
6371d332f728: Preparing 
44c4ab0334b3: Preparing 
1ec16b5c4b50: Preparing 
0ca80185f010: Preparing 
8315b5ceba6a: Preparing 
b641040ce833: Preparing 
fbdad267f49f: Preparing 
ea95a7e540ca: Pushed 
aa7c3db9b607: Pushed 
c555bbc990d6: Pushed 
aebef9108d3e: Pushed 
0d91d8140a64: Pushed 
28160869c1a6: Pushed 
ca0b2b0edc46: Pushed 
f68a4b816b85: Pushed 
2eee2baaccc3: Pushed 
06e218bc7fad: Pushed 
325e92dda745: Pushed 
11c4aaf358d6: Pushed 
5517c1ecca8e: Pushed 
9b8253ebc08f: Pushed 
55e244fef4fb: Pushed 
fae428ffe2fa: Pushed 
9c53da6cfcee: Pushed 
eff38aa3f4bb: Pushed 
cda0c7ae4804: Pushed 
9d75fe2fd306: Pushed 
b0e3533ba4e4: Pushed 
a59ca8d4ab74: Pushed 
3b401092118d: Pushed 
177a75fe2c9d: Pushed 
0a0c20a2cfa3: Pushed 
30529633cafa: Pushed 
7ab40dc875fc: Layer already exists 
f00f4dd6963b: Layer already exists 
e84a947bd930: Layer already exists 
f66da00ca5cc: Layer already exists 
e1ae8a634360: Layer already exists 
f3e31ec9d377: Layer already exists 
a01eeb5ca502: Layer already exists 
f79c93f62cef: Layer already exists 
d6a075bdd7eb: Layer already exists 
01a01c897688: Layer already exists 
72844059aa5b: Layer already exists 
33fd41279f42: Layer already exists 
latest: digest: sha256:eadb720a70be8e0d808c146032703772ff02dc5e4a8ca211ee9b31ef92b63ccd size: 20302
The push refers to repository [635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production]
d386f609225c: Preparing 
4341f9e6b728: Preparing 
09c5c41cbc96: Preparing 
10ba16172a43: Preparing 
c64bc3043ad4: Preparing 
81c4006cd554: Preparing 
a30e24214d6f: Preparing 
30ae41dc3f5e: Preparing 
fe09a8c8f343: Preparing 
5f70bf18a086: Preparing 
d05d38e33f88: Preparing 
0f22958d502c: Preparing 
5f70bf18a086: Preparing 
e4820370deaf: Preparing 
76bb7cca8751: Preparing 
518589a36ffc: Preparing 
448f558f6993: Preparing 
f28b51ca2d79: Preparing 
e3087344a47b: Preparing 
91823f4f4583: Preparing 
7ed5a987d5e0: Preparing 
cda577118532: Preparing 
fc16b9768200: Preparing 
7a6087f79f5e: Preparing 
c77b8aa22bb5: Preparing 
b4a822997280: Preparing 
5f70bf18a086: Preparing 
71be4d4a0c62: Preparing 
5f70bf18a086: Preparing 
5f70bf18a086: Preparing 
9b3fe0dbb4dd: Preparing 
76ad2537bcf0: Preparing 
30ae41dc3f5e: Waiting 
4a9bcba846c4: Preparing 
ea95a7e540ca: Preparing 
5f70bf18a086: Waiting 
ee2b6926d13b: Preparing 
b06d29c93765: Preparing 
e61943dddbb6: Preparing 
b9197c6d6f09: Preparing 
5f70bf18a086: Preparing 
9787ad0c4bf0: Preparing 
d05d38e33f88: Waiting 
6371d332f728: Preparing 
0f22958d502c: Waiting 
1ec16b5c4b50: Preparing 
0ca80185f010: Preparing 
8315b5ceba6a: Preparing 
b641040ce833: Preparing 
d8af79c39b15: Waiting 
3893f116566c: Layer already exists 
aa7c3db9b607: Layer already exists 
c555bbc990d6: Layer already exists 
aebef9108d3e: Layer already exists 
0d91d8140a64: Layer already exists 
28160869c1a6: Layer already exists 
ca0b2b0edc46: Layer already exists 
f68a4b816b85: Layer already exists 
2eee2baaccc3: Layer already exists 
06e218bc7fad: Layer already exists 
325e92dda745: Layer already exists 
11c4aaf358d6: Layer already exists 
5517c1ecca8e: Layer already exists 
9b8253ebc08f: Layer already exists 
55e244fef4fb: Layer already exists 
fae428ffe2fa: Layer already exists 
9c53da6cfcee: Layer already exists 
eff38aa3f4bb: Layer already exists 
cda0c7ae4804: Layer already exists 
9d75fe2fd306: Layer already exists 
b0e3533ba4e4: Layer already exists 
a59ca8d4ab74: Layer already exists 
3b401092118d: Layer already exists 
177a75fe2c9d: Layer already exists 
0a0c20a2cfa3: Layer already exists 
30529633cafa: Layer already exists 
7ab40dc875fc: Layer already exists 
f00f4dd6963b: Layer already exists 
e84a947bd930: Layer already exists 
f66da00ca5cc: Layer already exists 
e1ae8a634360: Layer already exists 
f3e31ec9d377: Layer already exists 
a01eeb5ca502: Layer already exists 
f79c93f62cef: Layer already exists 
d6a075bdd7eb: Layer already exists 
01a01c897688: Layer already exists 
72844059aa5b: Layer already exists 
33fd41279f42: Layer already exists 
80ba11b: digest: sha256:eadb720a70be8e0d808c146032703772ff02dc5e4a8ca211ee9b31ef92b63ccd size: 20302
Image successfully pushed to ECR: 635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:80ba11b

> dash-serverless-cdk@1.0.0 bk:production:auto /Users/farandal/DASH-PW-PROJECT/kitchntabs-ci-cdk
> node scripts/stackMgr.js bk production --yes

Loaded environment variables from /Users/farandal/DASH-PW-PROJECT/kitchntabs-ci-cdk/.env.production
Loaded environment variables from /Users/farandal/DASH-PW-PROJECT/kitchntabs-ci-cdk/.env.bk.production
=== DASH Serverless CDK - Stack Manager ===
Stack Type: bk
Environment: production
AWS Profile: KitchenTabs
AWS Stack: KTBackendStack
AWS Region: us-east-2
Executing: aws s3api head-bucket --bucket cdk-hnb659fds-assets-635862864028-us-east-2 --profile KitchenTabs
Synthesizing CloudFormation template...
Executing: cdk synth --app "npx ts-node bin/dash-serverless.ts" --profile KitchenTabs
[Warning at /KTBackendStack/KT-bk-production-taskdef/KT-bk-production-container] Proper policies need to be attached before pulling from ECR repository, or use 'fromEcrRepository'.

Executing: aws cloudformation describe-stacks --stack-name KTBackendStack --profile KitchenTabs
Executing: cdk diff --app "npx ts-node bin/dash-serverless.ts" --profile KitchenTabs
[Warning at /KTBackendStack/KT-bk-production-taskdef/KT-bk-production-container] Proper policies need to be attached before pulling from ECR repository, or use 'fromEcrRepository'.
Stack KTBackendStack
Resources
[~] AWS::ECS::TaskDefinition KT-bk-production-taskdef KTbkproductiontaskdef2B84EBA8 replace
 └─ [~] ContainerDefinitions (requires replacement)
     └─ @@ -23,7 +23,7 @@
        [ ]   }
        [ ] ],
        [ ] "Essential": true,
        [-] "Image": "635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:81d8fce",
        [+] "Image": "635862864028.dkr.ecr.us-east-2.amazonaws.com/kitchntabs-production:80ba11b",
        [ ] "LogConfiguration": {
        [ ]   "LogDriver": "awslogs",
        [ ]   "Options": {


✨  Number of stacks with differences: 1

Auto-confirming stack update (--yes flag provided)
Executing: cdk deploy --app "npx ts-node bin/dash-serverless.ts" --profile KitchenTabs --require-approval never

# SAMPLE entrylog log. fargate instance provisioning: 

--2025-12-20 17:32:38--  https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
Resolving truststore.pki.rds.amazonaws.com (truststore.pki.rds.amazonaws.com)... 3.170.131.38, 3.170.131.39, 3.170.131.14, ...
Connecting to truststore.pki.rds.amazonaws.com (truststore.pki.rds.amazonaws.com)|3.170.131.38|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 165408 (162K) [binary/octet-stream]
Saving to: '/tmp/rds-combined-ca-bundle.pem'
     0K .......... .......... .......... .......... .......... 30% 69.6M 0s
    50K .......... .......... .......... .......... .......... 61% 40.0M 0s
   100K .......... .......... .......... .......... .......... 92% 39.2M 0s
   150K .......... .                                          100% 38.3M=0.003s
2025-12-20 17:32:38 (45.6 MB/s) - '/tmp/rds-combined-ca-bundle.pem' saved [165408/165408]
Copying /var/www/dash/.env.kitchntabs.production to /var/www/dash/.env and /var/www/dash/.env.production
variables from current .env file: env.kitchntabs.production
file found at /var/www/dash/.env
AWS_DEFAULT_REGION already set to: us-east-2
AWS_REGION already set to: us-east-2
Environment variables loaded (not printing for security)...
Processing file: /var/www/dash//docker/app/redis.conf
Replacing environment variables in: /var/www/dash//docker/app/redis.conf
Horizon debug mode ENABLED (-vvv)
Reverb debug mode ENABLED (--debug)
Queue debug mode ENABLED (-vvv)
Processing file: /var/www/dash//docker/app/custom-supervisor.conf
Replacing environment variables in: /var/www/dash//docker/app/custom-supervisor.conf
  - ${HORIZON_VERBOSE} -> -vvv
  - ${REVERB_VERBOSE} -> --debug
Processing file: /var/www/dash/docker/nginx/nginx.conf
Replacing environment variables in: /var/www/dash/docker/nginx/nginx.conf
  - ${GROUP} -> www-data
  - ${SYSTEM_USER} -> dash
Processing file: /var/www/dash/docker/nginx/api.nginx.conf
Replacing environment variables in: /var/www/dash/docker/nginx/api.nginx.conf
  - ${PROJECT_DOMAIN} -> kitchntabs.com
  - ${SERVER_NAME} -> localhost
Processing file: /var/www/dash/docker/nginx/api.nginx.ssl.conf
Replacing environment variables in: /var/www/dash/docker/nginx/api.nginx.ssl.conf
  - ${APP_DIR} -> /var/www/dash/
  - ${AWS_REGION} -> us-east-2
  - ${ENVIRONMENT} -> 
  - ${NGINX_DOMAINS} -> localhost
  - ${NGINX_LOG_PATH} -> /var/log/nginx/
  - ${NGINX_PUBLIC_DOMAIN} -> localhost
  - ${PROJECT_DOMAIN} -> kitchntabs.com
  - ${PROJECT_NAME} -> kitchntabs
  - ${SERVER_NAME} -> localhost
  - ${SSL_CLIENT} -> 
Processing file: /var/www/dash//docker/app/php.dash.ini.conf
Replacing environment variables in: /var/www/dash//docker/app/php.dash.ini.conf
  - ${foo} -> 
Processing file: /var/www/dash//docker/app/php-fpm-custom.conf
Replacing environment variables in: /var/www/dash//docker/app/php-fpm-custom.conf
  - ${AWS_DEFAULT_REGION} -> us-east-2
  - ${AWS_REGION} -> us-east-2
  - ${GROUP} -> www-data
  - ${PHP_PORT} -> 9000
  - ${SYSTEM_USER} -> dash
Using original AWS credentials from .env file
Fargate platform detected: skipping in-container CloudWatch Logs group/stream creation.
Rely on ECS awslogs driver + task definition (log group, stream prefix, retention).
Testing AWS CLI access...
AWS CLI is configured correctly and has access (default profile/role)
Printing supervisor configuration files:
Contents of /etc/supervisor/conf.d/custom-supervisor.conf:
[program:horizon]
process_name=dash-horizon
#/usr/bin/php8.1
# HORIZON_VERBOSE is substituted by entrypoint.sh (set to -vvv when HORIZON_DEBUG=true)
command=php /var/www/dash/artisan horizon -vvv
autostart=true
autorestart=true
user=dash
redirect_stderr=true
stdout_logfile=/var/www/dash/storage/logs/supervisor-horizon.log
stderr_logfile=/var/www/dash/storage/logs/supervisor-horizon-error.log
environment=HOME="/home/dash",USER="dash",AWS_DEFAULT_REGION="us-east-2",AWS_REGION="us-east-2"
[program:schedule-run]
process_name=dash-crontab
#/usr/bin/php8.1
command=php /var/www/dash/artisan schedule:run
autostart=true
autorestart=true
user=dash
environment=HOME="/home/dash",USER="dash",AWS_DEFAULT_REGION="us-east-2",AWS_REGION="us-east-2"
numprocs=1
redirect_stderr=true
stdout_logfile=/var/www/dash/storage/logs/supervisor-schedule.log
stderr_logfile=/var/www/dash/storage/logs/supervisor-schedule-error.log
stopwaitsecs=60
[program:reverb]
process_name=dash-reverb
#/usr/bin/php8.1
# REVERB_VERBOSE is substituted by entrypoint.sh (set to --debug when REVERB_DEBUG=true)
command=php /var/www/dash/artisan reverb:start --host=127.0.0.1 --port=6001 --debug
autostart=true
autorestart=true
user=dash
environment=HOME="/home/dash",USER="dash",AWS_DEFAULT_REGION="us-east-2",AWS_REGION="us-east-2"
redirect_stderr=true
stdout_logfile=/var/www/dash/storage/logs/supervisor-reverb.log
stderr_logfile=/var/www/dash/storage/logs/supervisor-reverb-error.log
stopwaitsecs=3600----------------------------------------
Printing nginx server configuration files:
Contents of /etc/nginx/servers/api.nginx.ssl.conf:
# server {
#     listen 80;
#     listen [::]:80;
#     server_name localhost;
#     return 301 https://localhost$request_uri;
# }

server {
      #root  /var/www/dash/public;
      root /var/www/dash/public;
      client_max_body_size 128M;

      #server_name localhost;
      #access_log /var/log/nginx/dash.access.log;
      #error_log /var/log/nginx/dash.error.log;
      access_log /var/log/nginx/dash.access.log;
      error_log /var/log/nginx/dash.nginx.error.log;

      listen 443 ssl;
      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_prefer_server_ciphers on;
      #ssl_certificate /var/www/kitchntabs/certs/dash-bundle.crt;
      #ssl_certificate_key /var/www/kitchntabs/certs/dash.key;
      #ssl_certificate /var/www/dash/certs/bundle.crt;
      #ssl_certificate_key /var/www/dash/certs/private.key;
      ssl_certificate /opt/certs/certificate.crt;
      ssl_certificate_key /opt/certs/private.key;
      ssl_trusted_certificate /opt/certs/ca_bundle.crt;
      #ssl_client_certificate ;

      #conf
      location / {
       try_files $uri $uri/ /index.php$is_args$args;
      }

      gzip on;
      gzip_disable "msie6";
      #gzip_disable "MSIE [1-6]\.";
      gzip_vary on;
      gzip_proxied any;
      #gzip_proxied expired no-cache no-store private auth;
      gzip_comp_level 6;
      gzip_buffers 32 16k;
      gzip_http_version 1.1;
      gzip_min_length 250;
      #gzip_min_length 10240;
      gzip_types image/jpeg image/bmp image/svg+xml text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/x-icon;
      #gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml;

      index index.php

      sendfile off;
      expires off;

      #proxy_read_timeout 600;
      #proxy_connect_timeout 600;
      #proxy_send_timeout 600;

      location = /favicon.ico {
        access_log off;
        log_not_found off;
      }

      location = /robots.txt {
        access_log off;
        log_not_found off;
      }

      location ~ /\. { deny all; access_log off; log_not_found off; }

      try_files      $uri = 404;


      location = /webhooks/ {
          try_files $uri $uri/ /index.php$is_args$args;
      }

      location =  /notifications/ {
          try_files $uri $uri/ /index.php$is_args$args;
      }

    #   location = / {
    #       return 301 https://dashboard-v2.kitchntabs.cl;
    #   }

    #     location /storage {
    #       proxy_http_version     1.1;
    #       proxy_set_header       Connection "";
    #       proxy_set_header       Authorization '';
    #       proxy_set_header       Host kitchntabs-storage-.s3.us-east-2.amazonaws.com;
    #       proxy_hide_header      x-amz-id-2;
    #       proxy_hide_header      x-amz-request-id;
    #       proxy_hide_header      x-amz-meta-server-side-encryption;
    #       proxy_hide_header      x-amz-server-side-encryption;
    #       proxy_hide_header      Set-Cookie;
    #       proxy_ignore_headers   Set-Cookie;
    #       proxy_intercept_errors on;
    #       add_header             Cache-Control max-age=31536000;
    #       proxy_pass             https://kitchntabs-storage-.s3.us-east-2.amazonaws.com;
    #   }

      location ~ \.php$ {
       if ($request_method = 'OPTIONS') {
        add_header Access-Control-Allow-Origin '*';
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Max-Age' 1728000;
        add_header 'Content-Type' 'text/plain; charset=utf-8';
        add_header 'Content-Length' 0;
        return 204;
      }

     
      #Opcionalmente incluir fastcgi-php.conf
      #include snippets/fastcgi-php.conf;

      #o configurar:
      proxy_pass_request_headers  on;
      fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
      fastcgi_read_timeout 36000;
      fastcgi_index  index.php;
      fastcgi_param  SCRIPT_FILENAME     $document_root$fastcgi_script_name;
      include        fastcgi_params;
  }

}

server {
    listen 443 ssl;
    server_name ws.kitchntabs.com wss.kitchntabs.com;


    ssl_certificate /opt/certs/certificate.crt;
    ssl_certificate_key /opt/certs/private.key;
    ssl_trusted_certificate /opt/certs/ca_bundle.crt;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    location / {
      
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";

        proxy_pass http://127.0.0.1:6001;

    }

}

server {
    listen 443 ssl;
    server_name api.kitchntabs.com;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_certificate /opt/certs/certificate.crt;
    ssl_certificate_key /opt/certs/private.key;
    ssl_trusted_certificate /opt/certs/ca_bundle.crt;

    # Let Laravel handle all requests naturally (no /api prefix restriction)
    root /var/www/dash/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

    location ~ \.php$ {
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin '*';
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        proxy_pass_request_headers on;
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_read_timeout 36000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}

server {
    root /var/www/dash/public;
    client_max_body_size 128M;

    server_name panel.kitchntabs.com;
    access_log /var/log/nginx/panel.ssl.access.log;
    error_log /var/log/nginx/panel.ssl.error.log;

    listen 443 ssl;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_certificate /opt/certs/certificate.crt;
    ssl_certificate_key /opt/certs/private.key;
    ssl_trusted_certificate /opt/certs/ca_bundle.crt;

    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 32 16k;
    gzip_http_version 1.1;
    gzip_min_length 250;
    gzip_types image/jpeg image/bmp image/svg+xml text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/x-icon;

    index index.html index.php;

    sendfile off;
    expires off;

    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt { access_log off; log_not_found off; }
    location ~ /\. { deny all; access_log off; log_not_found off; }

    # Remove or ensure this is NOT present: autoindex on;
    # Serve static files, else fallback to index.html for React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Remove PHP handling block if not needed for React frontend
    # location ~ \.php$ {
    #     if ($request_method = 'OPTIONS') {
    #         add_header Access-Control-Allow-Origin '*';
    #         add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
    #         add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
    #         add_header 'Access-Control-Allow-Credentials' 'true';
    #         add_header 'Access-Control-Max-Age' 1728000;
    #         add_header 'Content-Type' 'text/plain; charset=utf-8';
    #         add_header 'Content-Length' 0;
    #         return 204;
    #     }

    #     proxy_pass_request_headers on;
    #     fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
    #     fastcgi_read_timeout 36000;
    #     fastcgi_index index.php;
    #     fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    #     include fastcgi_params;
    # }
}

server {
    root /var/www/dash/public;
    client_max_body_size 128M;

    server_name _;
    access_log /var/log/nginx/panel.ssl.access.log;
    error_log /var/log/nginx/panel.ssl.error.log;

    listen 443 ssl;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_certificate /opt/certs/certificate.crt;
    ssl_certificate_key /opt/certs/private.key;
    ssl_trusted_certificate /opt/certs/ca_bundle.crt;

    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 32 16k;
    gzip_http_version 1.1;
    gzip_min_length 250;
    gzip_types image/jpeg image/bmp image/svg+xml text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/x-icon;

    index index.html index.php;

    sendfile off;
    expires off;

    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt { access_log off; log_not_found off; }
    location ~ /\. { deny all; access_log off; log_not_found off; }

    # Serve static files, else fallback to index.html for React Router
    location / {
        try_files $uri $uri/ /index.html;
    }
}----------------------------------------
Contents of /etc/nginx/servers/nginx.www.conf:
server {
    # Root directory
    root /var/www/dash/public;
    client_max_body_size 128M;

    # Server name and logs
    # SERVER_NAME localhost
    # PROJECT_DOMAIN kitchntabs.com
    
    server_name localhost api.kitchntabs.com;    
    access_log /var/log/nginx/dash.access.log;
    error_log /var/log/nginx/dash.nginx.error.log;

    # Listen directives
    listen 80;
    listen [::]:80;

    # Gzip configuration
    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 32 16k;
    gzip_http_version 1.1;
    gzip_min_length 250;
    gzip_types image/jpeg image/bmp image/svg+xml text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/x-icon;

    # Default index
    index index.php;

    sendfile off;
    expires off;

    # Timeouts
    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;

    # Standard static file handling
    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt { access_log off; log_not_found off; }
    location ~ /\. { deny all; access_log off; log_not_found off; }

    # Main location block
    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

    # PHP handling
    location ~ \.php$ {
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin '*';
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        # FastCGI configuration
        proxy_pass_request_headers on;
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_read_timeout 36000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}

server {
    root /var/www/dash/public;
    client_max_body_size 128M;

    server_name panel.kitchntabs.com;
    access_log off;
    error_log /var/log/nginx/dash.nginx.error.log;

    listen 80;
    listen [::]:80;

    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 32 16k;
    gzip_http_version 1.1;
    gzip_min_length 250;
    gzip_types image/jpeg image/bmp image/svg+xml text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/x-icon;

    index index.html index.php;

    sendfile off;
    expires off;

    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt { access_log off; log_not_found off; }
    location ~ /\. { deny all; access_log off; log_not_found off; }

    # Serve static files, else fallback to index.html for React Router
    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
   
    listen 80;
    listen [::]:80;

    server_name ws.kitchntabs.com;
    access_log off;
    error_log /var/log/nginx/dash.nginx.error.log;

    location / {
        
        
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        
        proxy_pass http://127.0.0.1:6001;
        
    }
}

server {
    root /var/www/dash/public;
    client_max_body_size 128M;

    server_name _;
    access_log off;
    error_log /var/log/nginx/dash.nginx.error.log;

    listen 80;
    listen [::]:80;

    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 32 16k;
    gzip_http_version 1.1;
    gzip_min_length 250;
    gzip_types image/jpeg image/bmp image/svg+xml text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/x-icon application/pdf;

    index index.html index.php;

    sendfile off;
    expires off;

    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt { access_log off; log_not_found off; }
    location ~ /\. { deny all; access_log off; log_not_found off; }

    # Serve static files, else fallback to index.html for React Router
    location / {
        try_files $uri $uri/ /index.html;
    }
}----------------------------------------
========================================================================
Running Startup Diagnostics...
========================================================================
========================================================================
[DIAG] 2025-12-20 17:32:51 - DASH Backend Startup Diagnostics
========================================================================
[DIAG-INFO] 2025-12-20 17:32:51 - Hostname: ip-172-31-5-179.us-east-2.compute.internal
[DIAG-INFO] 2025-12-20 17:32:51 - Date: Sat Dec 20 17:32:51 UTC 2025
[DIAG-INFO] 2025-12-20 17:32:51 - User: dash
[DIAG-INFO] 2025-12-20 17:32:51 - Platform: fargate
[DIAG-INFO] 2025-12-20 17:32:51 - App Environment: production
========================================================================
[DIAG] 2025-12-20 17:32:51 - Testing AWS Region Configuration
========================================================================
[DIAG-PASS] 2025-12-20 17:32:51 - [0;32m✓[0m AWS_REGION is set: us-east-2
[DIAG-PASS] 2025-12-20 17:32:51 - [0;32m✓[0m AWS_DEFAULT_REGION is set: us-east-2
[DIAG-PASS] 2025-12-20 17:32:51 - [0;32m✓[0m .env contains AWS_REGION: us-east-2
========================================================================
[DIAG] 2025-12-20 17:32:51 - Testing AWS Credentials
========================================================================
[DIAG-PASS] 2025-12-20 17:32:51 - [0;32m✓[0m ECS credentials endpoint available: /v2/credentials/526ad13b-97b1-43ce-8605-b8cc4e91d3be
[DIAG-PASS] 2025-12-20 17:32:51 - [0;32m✓[0m ECS credentials fetched successfully (AccessKeyId: ASIAZIDDBK...)
[DIAG-PASS] 2025-12-20 17:32:51 - [0;32m✓[0m AWS_ACCESS_KEY_ID is set (AKIAZIDDBK...)
[DIAG-PASS] 2025-12-20 17:32:51 - [0;32m✓[0m AWS_SECRET_ACCESS_KEY is set ([MASKED])
[DIAG-WARN] 2025-12-20 17:32:51 - [1;33m⚠[0m AWS_SESSION_TOKEN not set (may be OK for non-temporary credentials)
========================================================================
[DIAG] 2025-12-20 17:32:51 - Testing S3 Access
========================================================================
[DIAG-INFO] 2025-12-20 17:32:51 - Testing S3 bucket: kitchntabs in region: us-east-2
[DIAG-PASS] 2025-12-20 17:32:55 - [0;32m✓[0m S3 bucket accessible via AWS CLI
[DIAG-FAIL] 2025-12-20 17:32:55 - [0;31m✗[0m S3 endpoint not reachable: s3.us-east-2.amazonaws.com
========================================================================
[DIAG] 2025-12-20 17:32:55 - Testing Redis/Valkey Connection
========================================================================
[DIAG-INFO] 2025-12-20 17:32:55 - Testing Redis at: kt-production-valkey-ypetaz.serverless.use2.cache.amazonaws.com:6379
[DIAG-INFO] 2025-12-20 17:32:55 - Using TLS for AWS ElastiCache/Valkey
[DIAG-PASS] 2025-12-20 17:32:55 - [0;32m✓[0m Redis connection successful: PONG
========================================================================
[DIAG] 2025-12-20 17:32:55 - Testing PostgreSQL Connection
========================================================================
[DIAG-INFO] 2025-12-20 17:32:55 - Testing PostgreSQL at: ktdatastack-production-db-instance.c5aaiq2w4muk.us-east-2.rds.amazonaws.com:5432
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m PostgreSQL connection successful
========================================================================
[DIAG] 2025-12-20 17:32:56 - Testing SSL Certificates
========================================================================
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m RDS CA bundle exists: /etc/ssl/certs/postgresql.crt
[DIAG-INFO] 2025-12-20 17:32:56 - Certificate bundle contains 108 certificates
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m Application SSL certificate exists: /opt/certs/certificate.crt
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m Application SSL private key exists: /opt/certs/private.key
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m Application CA bundle exists: /opt/certs/ca_bundle.crt
========================================================================
[DIAG] 2025-12-20 17:32:56 - Testing File Permissions
========================================================================
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m Storage directory is writable: /var/www/dash/storage
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m Logs directory is writable: /var/www/dash/storage/logs
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m .env file is readable
[DIAG-INFO] 2025-12-20 17:32:56 - Storage directory ownership: dash:www-data
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m Can create files in logs directory
========================================================================
[DIAG] 2025-12-20 17:32:56 - Testing PHP Configuration
========================================================================
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m PHP available: PHP 8.2.29 (cli) (built: Aug  5 2025 03:31:26) (NTS)
[DIAG-PASS] 2025-12-20 17:32:56 - [0;32m✓[0m PHP can read AWS_REGION from environment: us-east-2
[DIAG-WARN] 2025-12-20 17:32:56 - [1;33m⚠[0m PHP-FPM socket not found (may not be started yet): /var/run/php/php8.2-fpm.sock
[DIAG-WARN] 2025-12-20 17:32:57 - [1;33m⚠[0m Laravel artisan output unexpected: [2025-12-20 14:32:57] production.DEBUG: ReverbTlsServiceProvider: Bound TlsRedisClientFactory for Reverb scaling  
========================================================================
[DIAG] 2025-12-20 17:32:57 - Testing Laravel Configuration
========================================================================
[DIAG-PASS] 2025-12-20 17:33:00 - [0;32m✓[0m Laravel S3 region configured: us-east-2
[DIAG-INFO] 2025-12-20 17:33:02 - Laravel database driver: pgsql
[DIAG-INFO] 2025-12-20 17:33:04 - Laravel cache driver: redis
========================================================================
[DIAG] 2025-12-20 17:33:04 - Testing Network Connectivity
========================================================================
[DIAG-PASS] 2025-12-20 17:33:05 - [0;32m✓[0m Outbound internet connectivity OK
[DIAG-INFO] 2025-12-20 17:33:05 - EC2 metadata service not available (expected for Fargate)
[DIAG-PASS] 2025-12-20 17:33:05 - [0;32m✓[0m ECS metadata endpoint accessible
========================================================================
[DIAG] 2025-12-20 17:33:05 - Diagnostics Summary
========================================================================
  [0;32mPassed:[0m  23
  [0;31mFailed:[0m  1
  [1;33mWarnings:[0m 3
[DIAG-INFO] 2025-12-20 17:33:05 - Some tests failed. Review the output above for details.
[DIAG-RESULT] FAILED (1 failures, 3 warnings)
[DIAG] Diagnostics completed with some issues (non-fatal)
========================================================================
Diagnostics Complete - Continuing with startup...
========================================================================
Testing Redis connection...
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
PONG
Configuring CloudWatch Agent...
CloudWatch Log Group: kitchntabs-bk-production-loggroup
Processing file: /var/www/dash//docker/app/amazon-cloudwatch-agent.json
Replacing environment variables in: /var/www/dash//docker/app/amazon-cloudwatch-agent.json
  - ${AWS_REGION} -> us-east-2
  - ${CW_LOG_GROUP} -> kitchntabs-bk-production-loggroup
Starting CloudWatch Agent (Fargate mode - direct binary)...
Using existing AWS credentials from .env for CloudWatch Agent
Converting CloudWatch Agent config to TOML...
Starting config-translator, this will map back to a call to amazon-cloudwatch-agent
Executing /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent with arguments: [config-translator -output /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.toml -mode ec2 -config /opt/aws/amazon-cloudwatch-agent/etc/common-config.toml -multi-config remove -input /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json]2025/12/20 17:33:06 Reading json config file path: /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json ...
Cannot access : lstat : no such file or directory 
2025/12/20 17:33:06 unable to scan config dir  with error: lstat : no such file or directory
2025/12/20 17:33:06 I! Valid Json input schema.
D! [EC2] Found active network interface
I! imds retry client will retry 1 timesD! could not get hostname without imds v1 fallback enable thus enable fallback
E! [EC2] Fetch hostname from EC2 metadata fail: RequestError: send request failed
caused by: Get "http://169.254.169.254/latest/meta-data/hostname": dial tcp 169.254.169.254:80: connect: invalid argument
D! could not get instance document without imds v1 fallback enable thus enable fallback
E! [EC2] Fetch identity document from EC2 metadata fail: EC2MetadataRequestError: failed to get EC2 instance identity document
caused by: RequestError: send request failed
caused by: Get "http://169.254.169.254/latest/dynamic/instance-identity/document": dial tcp 169.254.169.254:80: connect: invalid argument
2025/12/20 17:33:07 Configuration validation first phase succeeded
Starting CloudWatch Agent binary in background...
CloudWatch Agent started successfully (PID: 1403)
Setting proper ownership for storage/logs...
Pre-creating log files with correct permissions...
Preserving original AWS credentials from .env.kitchntabs.production
Clearing Laravel config cache...
[2025-12-20 14:33:11] production.DEBUG: ReverbTlsServiceProvider: Bound TlsRedisClientFactory for Reverb scaling  
   INFO  Configuration cache cleared successfully.  
Skipping cache:clear (Redis may not be ready during startup)
Testing nginx configuration...
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
Starting nginx service...
sudo -E -n php-fpm --fpm-config /usr/local/etc/php-fpm-custom.conf