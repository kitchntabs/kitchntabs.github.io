# Electron Build & Configuration System

## Technical Documentation

> **Version:** 1.1  
> **Last Updated:** December 11, 2025  
> **Scope:** KitchnTabs Electron Application Build Pipeline

---

## 1. Overview

### The Challenge

Building a cross-platform Electron application that bundles Python background services presents unique challenges:

1. **Multi-Environment Configuration**: Different API endpoints for development (`ngrok`), staging, and production environments
2. **Cross-Platform Python Services**: Python binaries must be compiled for each target architecture (macOS, Windows, Linux x64, ARM32, ARM64)
3. **Configuration Injection**: The bundled application must use the correct API/WebSocket endpoints based on build mode
4. **Development Parity**: Development and production environments must behave consistently

### The Solution

Our build system implements a **Configuration-Driven Build Pipeline** that:

- Reads `CUSTOM_MODE` environment variable to determine the target environment
- Dynamically selects and bundles the correct YAML configuration file
- Compiles or selects pre-built Python service binaries for the target architecture
- Injects environment-specific settings into both the Electron main process and Python services

### Production Optimizations

For production builds, the system automatically applies security and performance optimizations:

#### Electron Main Process
- **Developer Console Disabled**: `win.webContents.openDevTools()` is only called in development mode (`isDev = true`)
- **Production Logging**: Console logs are minimized, error logging is maintained for debugging

#### Vite Build Process
- **Code Minification**: `minify: "esbuild"` enabled in production
- **Source Maps Disabled**: `sourcemap: false` in production builds
- **Console Log Removal**: Custom Vite plugin strips `console.log`, `console.warn`, etc. from production bundles
- **Bundle Optimization**: Tree shaking and dead code elimination enabled

#### Build Scripts
- Production builds use `MODE=production` which triggers all optimizations
- Development builds retain debugging features for easier troubleshooting

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BUILD PIPELINE                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   npm run release:electron:kitchntabs:development                               │
│                        │                                                         │
│                        ▼                                                         │
│   ┌──────────────────────────────────────────────────────────────────┐          │
│   │  1. config:electron:kitchntabs:development                       │          │
│   │     └─► build_config.js                                          │          │
│   │         └─► Sets CUSTOM_MODE=kitchntabs.development              │          │
│   │         └─► Creates build_config.json                            │          │
│   └──────────────────────────────────────────────────────────────────┘          │
│                        │                                                         │
│                        ▼                                                         │
│   ┌──────────────────────────────────────────────────────────────────┐          │
│   │  2. build-python-service.js                                      │          │
│   │     └─► Reads build_config.json                                  │          │
│   │     └─► Finds config.kitchntabs.development.yaml                 │          │
│   │     └─► Copies to apps/dash/config.yaml                          │          │
│   │     └─► Builds Python services (PyInstaller/Docker)              │          │
│   └──────────────────────────────────────────────────────────────────┘          │
│                        │                                                         │
│                        ▼                                                         │
│   ┌──────────────────────────────────────────────────────────────────┐          │
│   │  3. vite build + electron-builder                                │          │
│   │     └─► Bundles React app                                        │          │
│   │     └─► Packages Electron main process                           │          │
│   │     └─► extraResources: config.yaml → Resources/config.yaml      │          │
│   │     └─► extraResources: python-service/* → Resources/python-service/        │
│   └──────────────────────────────────────────────────────────────────┘          │
│                        │                                                         │
│                        ▼                                                         │
│   ┌──────────────────────────────────────────────────────────────────┐          │
│   │  FINAL PACKAGE                                                   │          │
│   │     ├── Contents/                                                │          │
│   │     │   ├── MacOS/kitchntabs (executable)                       │          │
│   │     │   └── Resources/                                           │          │
│   │     │       ├── config.yaml (kitchntabs.development)            │          │
│   │     │       ├── python-service/                                  │          │
│   │     │       │   ├── kt_service                                  │          │
│   │     │       │   ├── print_service                               │          │
│   │     │       │   └── tts_service                                 │          │
│   │     │       ├── icons/                                          │          │
│   │     │       └── sounds/                                         │          │
│   └──────────────────────────────────────────────────────────────────┘          │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Configuration Files

### 3.1 Environment-Specific YAML Configs

Located in `apps/dash/`:

| File | Environment | API Host | WebSocket Host |
|------|-------------|----------|----------------|
| `config.kitchntabs.development.yaml` | Development | `api.kitchntabs.com` | `ws.kitchntabs.com` |
| `config.kitchntabs.production.yaml` | Production | `api.kitchntabs.com` | `ws.kitchntabs.com` |

**Example: `config.kitchntabs.development.yaml`**

```yaml
APP_NAME: "kitchntabs"
WS_HOST: "ws.kitchntabs.com"
WS_PORT: ""
WS_SCHEME: "https"
API_HOST: "api.kitchntabs.com"
API_PORT: ""
API_SCHEME: "https"
APP: "dash"

AUTH_ENDPOINT: "api/ws/auth"

SPAWN_BACKGROUND_SERVICE: true
DEV_PYTHON_ENV: "../../../dash-python-service/pw_env/bin/python3.9"
PYTHON_SERVICE_PATH_DEV: "../../../dash-python-service/src/kt_service.py"
PYTHON_SERVICE_PATH_PROD: "./python-service/kt_service"
PRINT_SERVICE_PATH_DEV: "../../../dash-python-service/src/print_service.py"
PRINT_SERVICE_PATH_PROD: "./python-service/print_service"
SPEECH_SERVICE_PATH_DEV: "../../../dash-python-service/src/tts_service.py"
SPEECH_SERVICE_PATH_PROD: "./python-service/tts_service"
```

### 3.2 Build Configuration (`build_config.json`)

Generated by `build_config.js` at build time:

```json
{
  "mode": "development",
  "customMode": "kitchntabs.development",
  "targetType": "desktop",
  "platform": "electron",
  "timestamp": "2025-11-30T12:00:00.000Z",
  "buildId": "build-1732968000000-abc123",
  "platformConfig": {
    "buildType": "electron",
    "outputDir": "build",
    "packageFormat": "static"
  },
  "customModeConfig": {
    "apiBaseUrl": "https://api.kitchntabs.com",
    "environment": "development",
    "debugMode": true
  }
}
```

---

## 4. Key Scripts

### 4.1 `build_config.js`

**Purpose:** Generates `build_config.json` from environment variables.

**Key Features:**
- Parses `MODE`, `CUSTOM_MODE`, `TARGET_TYPE`, `PLATFORM` env vars
- Loads environment variables from `.env.{CUSTOM_MODE}` files
- Validates configuration
- Outputs structured JSON for downstream build steps

**Environment Variables:**

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `MODE` | Build mode | `development`, `staging`, `production` |
| `CUSTOM_MODE` | Configuration variant | `kitchntabs.development`, `kitchntabs.production` |
| `TARGET_TYPE` | Target platform type | `desktop`, `mobile`, `web` |
| `PLATFORM` | Specific platform | `electron`, `android`, `ios` |

### 4.2 `build-python-service.js`

**Purpose:** Prepares Python services and configuration for Electron packaging.

**Key Responsibilities:**

1. **Read Build Configuration**
   ```javascript
   function readBuildConfig() {
     const config = JSON.parse(fs.readFileSync('build_config.json', 'utf8'));
     return {
       customMode: config.customMode || 'kitchntabs.prod',
       platform: config.platform || process.platform
     };
   }
   ```

2. **Prepare Configuration File**
   ```javascript
   function prepareElectronConfigFiles(customMode) {
     // Primary: Use frontend config file matching CUSTOM_MODE exactly
     // e.g., CUSTOM_MODE=kitchntabs.development → config.kitchntabs.development.yaml
     let sourceConfigName = `config.${customMode}.yaml`;
     let sourceConfig = path.join(appsDir, sourceConfigName);
     
     // Copy to config.yaml for bundling
     fs.copyFileSync(sourceConfig, path.join(appsDir, 'config.yaml'));
   }
   ```

3. **Build Python Services**
   - Native builds for current platform using PyInstaller
   - Docker cross-compilation for Linux ARM (armv7l, arm64)

**Config Resolution Order:**

```
1. Frontend: apps/dash/config.{CUSTOM_MODE}.yaml (preferred)
   └── e.g., apps/dash/config.kitchntabs.development.yaml
   
2. Fallback: dash-python-service/config.*.yaml (legacy compatibility)
   └── e.g., dash-python-service/config.kitchntabs.ngrok.yaml
```

### 4.3 `electron/main/index.ts`

**Purpose:** Main Electron process that starts the app and Python services.

**CUSTOM_MODE Handling in Development:**

```typescript
// Get CUSTOM_MODE from environment (set during build process)
const CUSTOM_MODE: string | undefined = process.env.CUSTOM_MODE;

// Determine config file name based on CUSTOM_MODE
const getConfigFileName = (): string => {
  if (CUSTOM_MODE) {
    const customConfigFile = `config.${CUSTOM_MODE}.yaml`;
    if (isDev) {
      const customConfigPath = path.join(appPath, customConfigFile);
      if (fs.existsSync(customConfigPath)) {
        return customConfigFile;
      }
    } else {
      // In production, assume the custom config was bundled
      return customConfigFile;
    }
  }
  return 'config.yaml';
};
```

**Config Loading:**

```typescript
const configFileName = getConfigFileName();
let configFile = isDev
  ? path.join(appPath, `./${configFileName}`)
  : process.platform === 'darwin'
    ? path.join(appPath, `./Resources/${configFileName}`)
    : path.join(app.getAppPath(), `../${configFileName}`);

const config = YAML.parse(fs.readFileSync(configFile, 'utf8'));
```

### 4.4 `electron-builder.config.js`

**Purpose:** Configures electron-builder for packaging the application.

**Key Configuration:**

```javascript
module.exports = {
  appId: 'com.kitchntab.app',
  productName: 'kitchntabs',
  
  extraResources: [
    // Python service binaries
    {
      from: path.resolve(__dirname, '../dash-python-service/kt_service'),
      to: 'python-service',
      filter: ['**/kt_service', '**/print_service', '**/tts_service']
    },
    // Configuration file (prepared by build-python-service.js)
    {
      from: path.resolve(__dirname, 'apps/dash/config.yaml'),
      to: 'config.yaml'
    }
  ]
};
```

---

## 5. NPM Scripts Reference

### Development Scripts

```bash
# Start Electron in development with ngrok/development config
npm run dev:electron:kitchntabs:development

# Start Electron in development with production config
npm run dev:electron:kitchntabs:production
```

### Release Scripts

```bash
# Build for development (ngrok endpoints)
npm run release:electron:kitchntabs:development

# Build for production (optimized: no dev tools, minified, no console logs)
npm run release:electron:kitchntabs:production

# Build Debian packages for Linux (ARM64 + ARMv7)
pnpm release:electron:kitchntabs:debian

# Build for Raspberry Pi ARM64 (development)
npm run release:electron:kitchntabs:debian:arm64:development

# Build for Raspberry Pi ARMv7 (Buster)
npm run release:electron:kitchntabs:debian:buster:dev
```

**Note:** Production builds (`MODE=production`) automatically apply optimizations:
- Electron dev tools disabled
- Vite minification enabled
- Console logs removed from bundles
- Source maps disabled

### Script Breakdown

| Script | Config Mode | Build Config | Python Build |
|--------|-------------|--------------|--------------|
| `release:electron:kitchntabs:development` | `kitchntabs.development` | ngrok APIs | Native |
| `release:electron:kitchntabs:production` | `kitchntabs.production` | Production APIs | Native |
| `release:electron:kitchntabs:debian:arm64` | `kitchntabs.production` | Production APIs | Docker ARM64 |
| `release:electron:kitchntabs:debian:buster:dev` | `kitchntabs.development` | ngrok APIs | Docker ARMv7-Buster |

---

## 6. Build Flow Details

### Step 1: Configuration Generation

```bash
# Executed by config:electron:kitchntabs:development
cross-env MODE=development \
         CUSTOM_MODE=kitchntabs.development \
         TARGET_TYPE=desktop \
         PLATFORM=electron \
         node build_config.js
```

**Output:** `build_config.json`

### Step 2: Python Service & Config Preparation

```bash
node build-python-service.js
```

**Actions:**
1. Reads `build_config.json` to get `customMode`
2. Copies `apps/dash/config.kitchntabs.development.yaml` → `apps/dash/config.yaml`
3. Builds Python services if needed (native or Docker)

### Step 3: Vite Build

```bash
vite build -c electron.vite.config.mts
turbo build --no-cache
```

**Actions:**
1. Bundles React application to `apps/dash/dist/`
2. Builds Electron main/preload scripts to `apps/dash/dist-electron/`

### Step 4: Electron Packaging

```bash
node build-electron.js --config electron-builder.config.js
```

**Actions:**
1. Packages app using electron-builder
2. Copies `extraResources` (config.yaml, python-service/*, icons/, sounds/)
3. Creates platform-specific installer (.dmg, .exe, .deb, .AppImage)

---

## 7. Python Service Architecture

### Services Overview

| Service | Purpose | Binary Name |
|---------|---------|-------------|
| `kt_service` | WebSocket listener for kitchen orders | `kt_service` / `kt_service.exe` |
| `print_service` | Receipt printing | `print_service` / `print_service.exe` |
| `tts_service` | Text-to-Speech announcements | `tts_service` / `tts_service.exe` |

### Build Matrix

| Platform | Architecture | Build Method | Output Location |
|----------|--------------|--------------|-----------------|
| macOS | x64, arm64 | PyInstaller (native) | `dash-python-service/kt_service/` |
| Windows | x64 | PyInstaller (native) | `dash-python-service/kt_service/` |
| Linux | x64 | PyInstaller (native) | `dash-python-service/kt_service/` |
| Linux | armv7l | Docker cross-compile | `dash-python-service/kt_service_builds/armv7l/` |
| Linux | arm64 | Docker cross-compile | `dash-python-service/kt_service_builds/arm64/` |
| Linux | armv7l-buster | Docker cross-compile | `dash-python-service/kt_service_builds/armv7l-buster/` |

### Service Initialization

The Electron main process starts Python services with the config file:

```typescript
const pythonCmd = PYTHON_SERVICE_PATH_PROD;
const args = [
  token,                            // Auth token
  channel,                          // WebSocket channel
  PYTHON_SERVICE_CONFIG_PATH_PROD,  // Config file path
  logFile                           // Log file path
];

pythonProcess = spawn(pythonCmd, args);
```

---

## 8. Runtime Configuration Flow

### Development Mode

```
1. npm run dev:electron:kitchntabs:development
   │
   ├─► CUSTOM_MODE=kitchntabs.development passed to Electron
   │
   └─► electron/main/index.ts
       │
       ├─► getConfigFileName() → 'config.kitchntabs.development.yaml'
       │
       ├─► Checks if file exists in apps/dash/
       │
       └─► Loads YAML → config object
           │
           └─► Python service uses api.kitchntabs.com for API calls
```

### Production Mode (Packaged App)

```
1. User launches KitchnTabs.app
   │
   ├─► Electron main process starts
   │
   └─► electron/main/index.ts
       │
       ├─► Reads Resources/config.yaml
       │   (which is config.kitchntabs.development.yaml or
       │    config.kitchntabs.production.yaml, depending on build)
       │
       └─► Loads YAML → config object
           │
           └─► Python service uses configured API endpoints
```

---

## 9. Troubleshooting

### Config Not Loading

**Symptom:** Python service connects to wrong API endpoint

**Diagnosis:**
```bash
# Check build_config.json
cat build_config.json | grep customMode

# Check which config was bundled (in packaged app)
# macOS:
cat /Applications/kitchntabs.app/Contents/Resources/config.yaml

# Linux:
cat /opt/kitchntabs/resources/config.yaml
```

**Solution:** Ensure correct `CUSTOM_MODE` was set during build:
```bash
npm run release:electron:kitchntabs:development  # Uses kitchntabs.development
npm run release:electron:kitchntabs:production   # Uses kitchntabs.production
```

### Dev Tools Opening in Production

**Symptom:** Production app opens developer console on startup

**Diagnosis:**
Check that the build was done with `MODE=production`:
```bash
# Check build_config.json
cat build_config.json | grep '"mode"'

# Should show: "mode": "production"
```

**Solution:** 
- Ensure `MODE=production` is set during build
- Check `electron/main/index.ts` - dev tools should only open when `isDev = true`
- Rebuild with production mode: `npm run release:electron:kitchntabs:production`

### Console Logs in Production Bundle

**Symptom:** Console logs appear in production app

**Diagnosis:**
Check that Vite build included the console removal plugin:
```bash
# Check if production optimizations were applied
grep -r "console\." dist/  # Should return no results
```

**Solution:**
- Ensure `MODE=production` for Vite build
- Check `vite.config.mts` has the remove-console plugin enabled for production
- Rebuild the frontend: `vite build -c electron.vite.config.mts`

### Python Service Not Starting

**Symptom:** "Python service binary not found" error

**Diagnosis:**
```bash
# Check if binaries exist
ls -la dash-python-service/kt_service/

# Check electron-log for path issues
# In packaged app, check:
~/Library/Logs/kitchntabs/main.log  # macOS
~/.config/kitchntabs/logs/          # Linux
```

**Solution:**
```bash
# Rebuild Python services
npm run release:electron:kitchntabs:development:force

# Or manually trigger Docker build for Linux ARM
cd dash-python-service
npm run build:docker:armv7l:ngrok
```

### Wrong API Endpoints in Development

**Symptom:** Development app uses production APIs

**Diagnosis:**
```bash
# Check if config file exists
ls -la apps/dash/config.kitchntabs.development.yaml

# Check CUSTOM_MODE env var
echo $CUSTOM_MODE
```

**Solution:**
```bash
# Ensure the script passes CUSTOM_MODE correctly
CUSTOM_MODE=kitchntabs.development npm run dev:electron
```

---

## 10. Adding a New Environment

### Step 1: Create Config File

```bash
# Create new YAML config
touch apps/dash/config.{client}.{environment}.yaml
```

Example: `apps/dash/config.clientname.staging.yaml`

```yaml
APP_NAME: "clientname"
WS_HOST: "ws.kitchntabs.com"
API_HOST: "api.kitchntabs.com"
WS_SCHEME: "https"
API_SCHEME: "https"
# ... rest of config
```

### Step 2: Create NPM Scripts

```json
{
  "scripts": {
    "config:electron:clientname:staging": "cross-env MODE=staging CUSTOM_MODE=clientname.staging TARGET_TYPE=desktop PLATFORM=electron node build_config.js",
    "dev:electron:clientname:staging": "pnpm config:electron:clientname:staging && cross-env CUSTOM_MODE=clientname.staging electron .",
    "release:electron:clientname:staging": "pnpm config:electron:clientname:staging && turbo build --no-cache && node build-python-service.js && electron-icon-builder --input=./apps/dash/src/assets/logo-squared.png --output=./ && vite build -c electron.vite.config.mts && cross-env NODE_OPTIONS=--max-old-space-size=8096 node build-electron.js --config electron-builder.config.js"
  }
}
```

### Step 3: Create .env File (Optional)

```bash
# apps/dash/.env.clientname.staging
VITE_APP_BACKEND_URL=https://api.kitchntabs.com
VITE_APP_ADMIN_API_URL=https://api.kitchntabs.com/api
VITE_APP_SOCKETS_HOST=ws.kitchntabs.com
VITE_APP_SOCKETS_PORT=6001
VITE_APP_SOCKETS_SCHEME=https
```

---

## 11. Summary

The KitchnTabs Electron build system provides a robust, flexible pipeline for building cross-platform desktop applications with embedded Python services. Key features include:

- **Environment-driven builds**: `CUSTOM_MODE` controls all configuration
- **Automatic config selection**: Build scripts automatically select the correct YAML config
- **Cross-platform Python services**: Native builds for development, Docker for ARM deployment
- **Clear separation of concerns**: Configuration, building, and packaging are distinct steps

This architecture ensures that developers can easily switch between environments during development and confidently deploy to production with the correct configuration.

---

## 12. Related Documentation

- [ELECTRON_PYTHON_SERVICE_BUILD_SYSTEM.md](./ELECTRON_PYTHON_SERVICE_BUILD_SYSTEM.md) - Detailed Python service build process
- [ELECTRON_BUILD_PROCESS.md](./ELECTRON_BUILD_PROCESS.md) - General Electron build overview
- [dash-python-service/README.md](../dash-python-service/README.md) - Python service documentation

---

*Document generated for the KitchnTabs project build system.*
