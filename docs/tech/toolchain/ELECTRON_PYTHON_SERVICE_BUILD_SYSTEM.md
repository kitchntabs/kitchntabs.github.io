# Electron + Python Service Build System Documentation

## Overview

The KitchnTabs application is a hybrid desktop application that combines:
- **Electron** - Cross-platform desktop shell
- **React (Vite)** - Frontend UI framework
- **Python Service (kt_service)** - Backend service for WebSocket communication and thermal printing

This document explains how these components are built and packaged together.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ELECTRON APPLICATION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────────┐   │
│  │   Electron Main  │    │   React Frontend │    │   Python Service     │   │
│  │   (Node.js)      │    │   (Vite Bundle)  │    │   (kt_service)       │   │
│  │                  │    │                  │    │                      │   │
│  │  - Window mgmt   │    │  - UI Components │    │  - WebSocket client  │   │
│  │  - IPC handlers  │    │  - React-Admin   │    │  - Thermal printing  │   │
│  │  - Auto-updater  │    │  - State mgmt    │    │  - Audio playback    │   │
│  │  - Spawns Python │    │  - API calls     │    │  - Event handling    │   │
│  └────────┬─────────┘    └──────────────────┘    └──────────┬───────────┘   │
│           │                                                  │               │
│           │              IPC / Process Spawn                 │               │
│           └──────────────────────────────────────────────────┘               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Build Pipeline

### Complete Build Flow

```
pnpm release:electron:kitchntabs:development
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│  1. CONFIG GENERATION (build_config.js)                               │
│     └─ Creates build_config.json with CUSTOM_MODE, platform, etc.     │
└───────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│  2. PYTHON SERVICE BUILD (build-python-service.js)                    │
│     ├─ Reads build_config.json                                        │
│     ├─ Calls ../dash-python-service/build-service.js                  │
│     ├─ Copies config.{CUSTOM_MODE}.yaml → config.yaml                 │
│     ├─ Runs PyInstaller to create standalone executable               │
│     └─ Output: dash-python-service/kt_service/kt_service              │
└───────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│  3. ICON GENERATION (electron-icon-builder)                           │
│     └─ Creates icons/mac/icon.icns, icons/win/icon.ico, icons/png/*   │
└───────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│  4. FRONTEND BUILD (turbo build)                                      │
│     ├─ Builds React app with Vite                                     │
│     ├─ Injects environment variables from .env.{CUSTOM_MODE}          │
│     └─ Output: apps/dash/dist/                                        │
└───────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│  5. ELECTRON PACKAGING (build-electron.js → electron-builder)         │
│     ├─ Hides pnpm workspace files (workaround)                        │
│     ├─ Builds Electron main/preload with Vite                         │
│     ├─ Packages app with electron-builder                             │
│     ├─ Copies Python service as extraResource                         │
│     └─ Output: release/*.zip, release/*.deb, release/*.exe            │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Key Scripts & Files

### 1. Build Configuration (`build_config.js`)

**Location:** `dash-frontend/build_config.js`

**Purpose:** Generates `build_config.json` based on environment variables.

**Environment Variables:**
| Variable | Description | Example |
|----------|-------------|---------|
| `MODE` | Build mode | `development`, `production` |
| `CUSTOM_MODE` | Configuration profile | `kitchntabs.ngrok`, `kitchntabs.production` |
| `TARGET_TYPE` | Target platform type | `desktop`, `mobile`, `web` |
| `PLATFORM` | Specific platform | `electron`, `android`, `ios` |

**Output (`build_config.json`):**
```json
{
  "mode": "development",
  "customMode": "kitchntabs.ngrok",
  "targetType": "desktop",
  "platform": "electron",
  "buildId": "build-1764378809420-sjy42z",
  "timestamp": "2025-11-29T01:13:29.420Z",
  "customModeConfig": {
    "apiBaseUrl": "https://api.kitchntabs.com",
    "environment": "development",
    "debugMode": true
  }
}
```

---

### 2. Python Service Build (`build-python-service.js`)

**Location:** `dash-frontend/build-python-service.js`

**Purpose:** Orchestrates the Python service build from the frontend project.

**Workflow:**
1. Reads `build_config.json` to get `CUSTOM_MODE`
2. Calls `dash-python-service/build-service.js`
3. Verifies the executable was created

---

### 3. Python Service Builder (`build-service.js`)

**Location:** `dash-python-service/build-service.js`

**Purpose:** Builds the Python service using PyInstaller.

**Config File Mapping:**
| CUSTOM_MODE | Config File |
|-------------|-------------|
| `kitchntabs.ngrok` | `config.kitchntabs.ngrok.yaml` |
| `kitchntabs.production` | `config.kitchntabs.prod.yaml` |
| `kitchntabs.prod` | `config.kitchntabs.prod.yaml` |
| `dev` (macOS) | `config.dev.mac.yaml` |
| `dev` (Windows) | `config.dev.yaml` |

**PyInstaller Command:**
```bash
python3.9 -m PyInstaller ./src/kt_service.py \
  --onefile \
  --distpath ./kt_service \
  --add-data "config.yaml:." \
  --add-data "pw_env/lib/python3.9/site-packages/escpos/*.json:escpos" \
  --collect-data escpos \
  --noconfirm \
  --clean
```

**Output:** `dash-python-service/kt_service/kt_service` (88 MB executable)

---

### 4. Electron Build Wrapper (`build-electron.js`)

**Location:** `dash-frontend/build-electron.js`

**Purpose:** Wraps electron-builder to handle pnpm workspace compatibility issues.

**Workaround Steps:**
1. Backup `package.json`
2. Hide `pnpm-workspace.yaml` and `pnpm-lock.yaml`
3. Temporarily rename `node_modules`
4. Run electron-builder
5. Restore all files

This is necessary because electron-builder 26.x has issues with pnpm workspaces.

---

### 5. Electron Builder Config (`electron-builder.config.js`)

**Location:** `dash-frontend/electron-builder.config.js`

**Key Configurations:**

```javascript
module.exports = {
  appId: 'com.kitchntab.app',
  productName: 'kitchntabs',
  asar: false,
  npmRebuild: false,
  electronVersion: '36.7.4',
  
  // Python service is copied here
  extraResources: [
    {
      from: '../dash-python-service/kt_service',
      to: 'python-service',
      filter: process.platform === 'win32' 
        ? ['**/*.exe'] 
        : ['**/kt_service']
    },
    {
      from: '../dash-python-service',
      to: 'python-service',
      filter: ['*.yaml']
    }
  ],
  
  mac: {
    target: [{ target: 'zip', arch: ['arm64', 'x64'] }]
  },
  
  linux: {
    target: [
      { target: 'deb', arch: ['x64', 'armv7l', 'arm64'] },
      { target: 'AppImage', arch: ['x64', 'armv7l', 'arm64'] }
    ]
  },
  
  win: {
    target: [{ target: 'nsis', arch: ['x64'] }]
  }
}
```

---

## Python Service (kt_service)

### Purpose

The Python service (`kt_service.py`) runs as a background process spawned by Electron. It provides:

1. **WebSocket Client** - Connects to Laravel Reverb/Pusher for real-time events
2. **Thermal Printing** - Sends print jobs to ESC/POS printers
3. **Audio Playback** - Plays notification sounds
4. **Event Handling** - Processes incoming events from the backend

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      kt_service.py                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   main()     │    │  WebSocket   │    │   Handlers   │       │
│  │              │───▶│  Connection  │───▶│              │       │
│  │  - Args      │    │              │    │  - print     │       │
│  │  - Config    │    │  - Pusher    │    │  - speech    │       │
│  │  - Loop      │    │  - Auth      │    │  - events    │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
│  Dependencies:                                                   │
│  ├── websockets     - WebSocket client                          │
│  ├── aiohttp        - HTTP client for auth                      │
│  ├── escpos         - Thermal printer support                   │
│  ├── Pillow         - Image processing                          │
│  └── librosa/scipy  - Audio processing                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Command Line Arguments

```bash
kt_service <token> <channel> <config_file> <log_file>
```

| Argument | Description | Example |
|----------|-------------|---------|
| `token` | User authentication token | `24\|eJHkese14E9...` |
| `channel` | WebSocket channel to subscribe | `private-tenant.1.system` |
| `config_file` | YAML configuration file | `config.kitchntabs.ngrok.yaml` |
| `log_file` | Log output file | `log.txt` |

### Configuration File (`config.yaml`)

```yaml
APP_NAME: kitchntabs
WS_HOST: "ws.kitchntabs.com"
WS_PORT: ""
WS_SCHEME: "https"
API_HOST: "api.kitchntabs.com"
API_PORT: ""
API_SCHEME: "https"
APP: "dash"

AUTH_ENDPOINT: "api/ws/auth"
LOGS_PATH: "./logs/"

# Printer settings
PRINTER_VENDOR: 0x04b8
PRINTER_PRODUCT: 0x0e20
```

### Event Flow

```
Laravel Backend                Python Service              Electron App
      │                              │                           │
      │  WebSocket Event             │                           │
      │  {type: "print",             │                           │
      │   data: {tab_id: 39}}        │                           │
      │─────────────────────────────▶│                           │
      │                              │                           │
      │                              │  Parse event              │
      │                              │  Call print_order()       │
      │                              │                           │
      │                              │  HTTP GET /api/tabs/39    │
      │◀─────────────────────────────│                           │
      │  Tab data response           │                           │
      │─────────────────────────────▶│                           │
      │                              │                           │
      │                              │  Generate receipt         │
      │                              │  Send to ESC/POS printer  │
      │                              │                           │
```

---

## NPM Scripts Reference

### Full Release Builds (includes Python service)

| Script | Description | Config Mode |
|--------|-------------|-------------|
| `release:electron:kitchntabs:production` | Production macOS build | `kitchntabs.production` |
| `release:electron:kitchntabs:development` | Development macOS build | `kitchntabs.ngrok` |
| `release:electron:kitchntabs:ngrok` | Ngrok macOS build | `kitchntabs.ngrok` |
| `release:electron:kitchntabs:debian` | Production Linux/RPi build | `kitchntabs.production` |
| `release:electron:kitchntabs:debian:dev` | Development Linux/RPi build | `kitchntabs.ngrok` |

### Partial Builds (no Python service)

| Script | Description |
|--------|-------------|
| `release:electron:kitchntabs:production:web` | Only build web assets |
| `release:electron:kitchntabs:production:app` | Only run electron-builder |
| `release:electron:kitchntabs:ngrok:web` | Only build web assets (ngrok) |
| `release:electron:kitchntabs:ngrok:app` | Only run electron-builder |

### Development Scripts

| Script | Description |
|--------|-------------|
| `dev:electron:kitchntabs:ngrok` | Run Electron in dev mode |
| `dev:electron:kitchntabs:production` | Run Electron with prod API |

---

## Output Artifacts

### macOS
```
release/
├── mac-arm64/
│   └── kitchntabs.app/
│       └── Contents/
│           └── Resources/
│               └── python-service/
│                   ├── kt_service        # ARM64 executable
│                   └── config.yaml
├── mac/
│   └── kitchntabs.app/                   # x64 version
├── kitchntabs-1.0.3-arm64-mac.zip
└── kitchntabs-1.0.3-mac.zip
```

### Linux (Debian/Raspberry Pi)
```
release/
├── kitchntabs-1.0.3-arm64.deb            # RPi 64-bit
├── kitchntabs-1.0.3-armv7l.deb           # RPi 32-bit
├── kitchntabs-1.0.3-x64.deb              # Intel/AMD
├── kitchntabs-1.0.3-arm64.AppImage
├── kitchntabs-1.0.3-armv7l.AppImage
└── kitchntabs-1.0.3-x64.AppImage
```

### Windows
```
release/
├── win-unpacked/
│   └── resources/
│       └── python-service/
│           ├── kt_service.exe
│           └── config.yaml
└── kitchntabs-1.0.3.exe                  # NSIS installer
```

---

## Troubleshooting

### Python Build Issues

**Problem:** PyInstaller not finding virtual environment
```
✅ Virtual environment found
❌ Config file not found
```
**Solution:** Ensure `pw_env` exists and is activated:
```bash
cd dash-python-service
source pw_env/bin/activate
pip install -r requirements.txt
```

**Problem:** Missing escpos JSON files
```
ModuleNotFoundError: No module named 'escpos'
```
**Solution:** Ensure escpos is properly installed and the JSON files are included:
```bash
pip install python-escpos
```

---

## Cross-Compilation for Linux ARM (Raspberry Pi)

### The Problem

PyInstaller **cannot cross-compile** - it only creates executables for the same platform/architecture it runs on. Building on macOS creates macOS binaries, not Linux ARM binaries.

### The Solution: Docker + QEMU

We use Docker with QEMU emulation to build Linux binaries for multiple architectures from macOS or Windows.

### Prerequisites

1. **Docker Desktop** installed and running
2. **QEMU support** (usually automatic in Docker Desktop)
3. For Apple Silicon Macs: Ensure "Use Rosetta for x86/amd64 emulation" is **disabled** in Docker settings

### Quick Start

```bash
# Navigate to the Python service directory
cd dash-python-service

# Build for all Linux architectures (x64, arm64, armv7l)
npm run build:docker:all

# Or build for specific architecture
npm run build:docker:armv7l    # Raspberry Pi 32-bit
npm run build:docker:arm64     # Raspberry Pi 64-bit  
npm run build:docker:x64       # Intel/AMD Linux

# Build with specific config
npm run build:docker:prod      # Production config
npm run build:docker:ngrok     # Development/ngrok config
```

### Build Output

```
dash-python-service/
├── kt_service_builds/
│   ├── x64/
│   │   ├── kt_service          # Linux x64 binary
│   │   └── config.yaml
│   ├── arm64/
│   │   ├── kt_service          # Linux ARM64 binary (RPi 4 64-bit)
│   │   └── config.yaml
│   └── armv7l/
│       ├── kt_service          # Linux ARMv7l binary (RPi 3/4 32-bit)
│       └── config.yaml
└── kt_service/
    ├── kt_service_x64          # Copied for easy access
    ├── kt_service_arm64
    └── kt_service_armv7l
```

### Docker Build Scripts

| Script | Description |
|--------|-------------|
| `build-docker.sh` | Bash script (macOS/Linux) |
| `build-docker.js` | Node.js script (cross-platform) |

### How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Docker Cross-Compilation Flow                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Your Mac (ARM64 or x64)                                                │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │  Docker Desktop                                                 │     │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │     │
│  │  │ linux/amd64      │  │ linux/arm64      │  │ linux/arm/v7 │  │     │
│  │  │ container        │  │ container        │  │ container    │  │     │
│  │  │                  │  │                  │  │              │  │     │
│  │  │ QEMU emulation   │  │ QEMU emulation   │  │ QEMU emul.   │  │     │
│  │  │ Python 3.9       │  │ Python 3.9       │  │ Python 3.9   │  │     │
│  │  │ PyInstaller      │  │ PyInstaller      │  │ PyInstaller  │  │     │
│  │  │                  │  │                  │  │              │  │     │
│  │  │ → kt_service     │  │ → kt_service     │  │ → kt_service │  │     │
│  │  │   (x64 ELF)      │  │   (ARM64 ELF)    │  │   (ARMv7)    │  │     │
│  │  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘  │     │
│  │           │                     │                   │          │     │
│  └───────────┼─────────────────────┼───────────────────┼──────────┘     │
│              │                     │                   │                │
│              ▼                     ▼                   ▼                │
│         kt_service_builds/x64  kt_service_builds/arm64  armv7l         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Electron Builder Integration

The `electron-builder.config.js` automatically uses the correct binary:

1. **macOS/Windows**: Uses native PyInstaller build from `kt_service/`
2. **Linux**: Uses `afterPack` hook to copy architecture-specific binary from `kt_service_builds/<arch>/`

### Complete Debian Build Workflow

```bash
# 1. Build Python service for all Linux architectures
cd dash-python-service
npm run build:docker:prod

# 2. Build Electron app for Debian (from dash-frontend)
cd ../dash-frontend
pnpm release:electron:kitchntabs:debian
```

### Build Time Estimates

| Architecture | First Build | Cached Build |
|--------------|-------------|--------------|
| x64          | ~5-10 min   | ~2-3 min     |
| arm64        | ~15-25 min  | ~5-8 min     |
| armv7l       | ~20-35 min  | ~8-12 min    |

**Note:** ARM builds are slower due to QEMU emulation. First builds include downloading base images and installing dependencies.

### Verifying Binaries

```bash
# Check binary architecture
file kt_service_builds/armv7l/kt_service
# Expected: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV)

file kt_service_builds/arm64/kt_service  
# Expected: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV)

file kt_service_builds/x64/kt_service
# Expected: ELF 64-bit LSB executable, x86-64, version 1 (SYSV)
```

---

## Electron Build Issues

**Problem:** node_modules collection taking too long
```
Collecting node_modules...
```
**Solution:** The `build-electron.js` script hides node_modules. If stuck, manually restore:
```bash
mv node_modules.bak node_modules
mv pnpm-workspace.yaml.bak pnpm-workspace.yaml
mv pnpm-lock.yaml.bak pnpm-lock.yaml
```

**Problem:** Code signing warnings on macOS
```
skipped macOS application code signing
```
**Solution:** For distribution, set up Apple Developer certificates. For development, this warning can be ignored.

---

## Environment Files

### `.env.kitchntabs.ngrok`
Development configuration pointing to ngrok tunnels:
```env
VITE_APP_BACKEND_URL=https://api.kitchntabs.com
VITE_APP_ADMIN_API_URL=https://api.kitchntabs.com/api
VITE_APP_SOCKETS_HOST=ws.kitchntabs.com
VITE_APP_SOCKETS_SCHEME=https
VITE_APP_SOCKETS_KEY=dash
```

### `.env.kitchntabs.production`
Production configuration:
```env
VITE_APP_BACKEND_URL=https://api.kitchntabs.com
VITE_APP_ADMIN_API_URL=https://api.kitchntabs.com/api
VITE_APP_SOCKETS_HOST=ws.kitchntabs.com
VITE_APP_SOCKETS_SCHEME=https
VITE_APP_SOCKETS_KEY=dash
```

---

## File Structure Summary

```
DASH-PW-PROJECT/
├── dash-frontend/
│   ├── build_config.js              # Config generator
│   ├── build-python-service.js      # Python build orchestrator
│   ├── build-electron.js            # Electron build wrapper
│   ├── electron-builder.config.js   # Electron builder config
│   ├── electron.vite.config.mts     # Vite config for Electron
│   ├── build_config.json            # Generated build config
│   ├── apps/dash/
│   │   ├── .env.kitchntabs.ngrok
│   │   ├── .env.kitchntabs.production
│   │   └── dist/                    # Built frontend
│   └── release/                     # Build output
│
└── dash-python-service/
    ├── build-service.js             # Python build script
    ├── package.json                 # NPM scripts
    ├── config.kitchntabs.ngrok.yaml
    ├── config.kitchntabs.prod.yaml
    ├── pw_env/                      # Python virtual env
    ├── src/
    │   ├── kt_service.py            # Main service
    │   ├── print_service.py         # Print handler
    │   └── pinoywok/                # Service modules
    └── kt_service/
        └── kt_service               # Built executable
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.3 | 2025-11-29 | Added Python service build integration |
| 1.0.2 | 2025-11-28 | Fixed config path resolution for Linux |
| 1.0.1 | 2025-11-27 | pnpm workspace workaround |
| 1.0.0 | 2025-11-26 | Initial release |
