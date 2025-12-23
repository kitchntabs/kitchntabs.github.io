# Electron Build Process Documentation

## Overview

This document provides an in-depth explanation of the Electron build process for the **KitchnTabs** desktop application. The build system is designed to work with a **pnpm monorepo workspace** and uses **Vite** for bundling the Electron main process, preload scripts, and renderer process.

The build process addresses a critical compatibility issue between **electron-builder** and **pnpm workspaces**, which required a custom wrapper script solution.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Build Tools & Dependencies](#build-tools--dependencies)
3. [The pnpm Workspace Problem](#the-pnpm-workspace-problem)
4. [Build Wrapper Script](#build-wrapper-script)
5. [Vite Configuration](#vite-configuration)
6. [Electron Builder Configuration](#electron-builder-configuration)
7. [Build Commands](#build-commands)
8. [Platform-Specific Builds](#platform-specific-builds)
9. [Directory Structure](#directory-structure)
10. [Config File Resolution](#config-file-resolution)
11. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Build Pipeline                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Configuration      →  Set environment (production/dev)      │
│  2. Icon Generation    →  electron-icon-builder                 │
│  3. Turbo Build        →  Build React app + Electron process    │
│  4. Build Wrapper      →  build-electron.js (pnpm workaround)   │
│  5. Electron Builder   →  Package for target platform           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | File | Purpose |
|-----------|------|---------|
| Build Wrapper | `build-electron.js` | Workaround for pnpm/electron-builder incompatibility |
| Vite Config | `electron.vite.config.mts` | Bundle main process, preload, and renderer |
| Builder Config | `electron-builder.config.js` | Package configuration for all platforms |
| Main Process | `apps/dash/electron/main/index.ts` | Electron main process entry |
| Preload Script | `apps/dash/electron/preload/index.ts` | Secure bridge between main and renderer |

---

## Build Tools & Dependencies

### Core Dependencies

```json
{
  "electron": "36.7.4",
  "electron-builder": "26.0.12",
  "vite": "^5.x",
  "vite-plugin-electron": "^0.x"
}
```

### Runtime Dependencies (Bundled by Vite)

These dependencies are bundled into the main process JavaScript file:

- `electron-updater` - Auto-update functionality
- `electron-log` - Logging system
- `electron-store` - Persistent storage
- `yaml` - YAML config file parsing
- `dotenv` - Environment variable loading
- `sound-play` - Audio playback

---

## The pnpm Workspace Problem

### The Issue

**electron-builder v26.x** uses `YarnNodeModulesCollector` internally to collect dependencies for packaging. This collector **cannot properly parse pnpm's symlink-based dependency structure**, causing the build to fail with:

```
⨯ Unexpected end of JSON input
Error: /Users/.../dash-frontend/node_modules/.pnpm/@types+eslint@8.56.12
```

### Why It Happens

1. pnpm uses a **content-addressable store** with symlinks
2. electron-builder tries to traverse `node_modules/.pnpm/` 
3. The nested structure causes JSON parsing failures
4. pnpm-workspace.yaml triggers workspace detection that further confuses electron-builder

### The Solution

Instead of fighting electron-builder's node_modules collection, we **bypass it entirely**:

1. **Bundle all dependencies** into the main process using Vite (no runtime node_modules needed)
2. **Hide pnpm-specific files** during build (workspace yaml, lock file)
3. **Create a minimal package.json** with zero dependencies
4. **Trick electron-builder** into thinking it's a simple non-workspace project

---

## Build Wrapper Script

### File: `build-electron.js`

This wrapper script is the **critical component** that enables electron-builder to work with pnpm workspaces.

### Strategy

```javascript
// Only externalize electron itself - bundle everything else
const nativeModules = ['electron'];

// In vite config:
external: nativeModules  // This bundles electron-updater, yaml, etc.
```

### Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                 build-electron.js Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. BACKUP PHASE                                                │
│     ├─ Copy package.json → package.json.original-backup         │
│     ├─ Rename pnpm-workspace.yaml → .build-backup               │
│     ├─ Rename pnpm-lock.yaml → .build-backup                    │
│     └─ Rename node_modules → node_modules_build_backup          │
│                                                                 │
│  2. SETUP PHASE                                                 │
│     ├─ Create empty node_modules/                               │
│     ├─ Create minimal package.json (ZERO dependencies)          │
│     └─ Create fake yarn.lock (tricks electron-builder)          │
│                                                                 │
│  3. BUILD PHASE                                                 │
│     └─ Run electron-builder from backup node_modules location   │
│                                                                 │
│  4. RESTORE PHASE (always runs, even on error)                  │
│     ├─ Delete fake yarn.lock                                    │
│     ├─ Delete temporary node_modules                            │
│     ├─ Restore original node_modules                            │
│     ├─ Restore original package.json                            │
│     ├─ Restore pnpm-workspace.yaml                              │
│     └─ Restore pnpm-lock.yaml                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Minimal Package.json Created

```json
{
  "name": "kitchntabs",
  "version": "1.0.3",
  "description": "KitchnTabs Desktop Application",
  "author": {
    "name": "Dash Team",
    "email": "dev@kitchntabs.com"
  },
  "main": "apps/dash/dist-electron/main/index.js",
  "private": true
  // NO dependencies - Vite bundles everything!
}
```

### Safety Mechanisms

The wrapper includes multiple safety mechanisms:

```javascript
// Register cleanup handlers for all exit scenarios
process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(1); });
process.on('SIGTERM', () => { cleanup(); process.exit(1); });
process.on('uncaughtException', (err) => { 
  console.error('Uncaught exception:', err);
  cleanup(); 
  process.exit(1); 
});
```

---

## Vite Configuration

### File: `electron.vite.config.mts`

The Vite configuration is **crucial** because it determines what gets bundled vs. externalized.

### Key Configuration

```typescript
// CRITICAL: Only externalize electron itself
const nativeModules = ['electron'];

export default defineConfig({
  plugins: [
    electron({
      main: {
        entry: 'apps/dash/electron/main/index.ts',
        vite: {
          build: {
            outDir: 'apps/dash/dist-electron/main',
            rollupOptions: {
              // Only externalize native modules - bundle everything else
              external: nativeModules,
              output: {
                format: 'cjs',  // CommonJS for Electron compatibility
                entryFileNames: '[name].js'
              }
            }
          }
        }
      },
      preload: {
        input: 'apps/dash/electron/preload/index.ts',
        vite: {
          build: {
            outDir: 'apps/dash/dist-electron/preload',
            rollupOptions: {
              external: nativeModules,
              output: {
                format: 'cjs',
                entryFileNames: '[name].js'
              }
            }
          }
        }
      }
    })
  ]
});
```

### Why Bundle Everything?

| Approach | Pros | Cons |
|----------|------|------|
| **External deps (default)** | Smaller bundle, faster build | Requires node_modules at runtime, breaks with pnpm |
| **Bundle all deps (our approach)** | No runtime node_modules needed, works with pnpm | Slightly larger bundle |

By bundling all dependencies (except `electron` itself), we eliminate the need for electron-builder to collect node_modules at all.

---

## Electron Builder Configuration

### File: `electron-builder.config.js`

### Core Settings

```javascript
module.exports = {
  appId: 'com.kitchntab.app',
  productName: 'kitchntabs',
  asar: false,                        // Keep files uncompressed
  npmRebuild: false,                  // No native deps to rebuild
  nodeGypRebuild: false,              // No node-gyp needed
  buildDependenciesFromSource: false,
  electronVersion: '36.7.4',          // Explicit version (required)
  
  directories: {
    output: 'release/',
    buildResources: 'icons'
  }
};
```

### Files Configuration

```javascript
files: [
  "electron-config.yaml",
  "resources/sounds/**/*",
  "apps/dash/dist/**",           // Renderer build output
  "apps/dash/dist-electron/**",  // Main process build output
  "apps/dash/electron-config.prod.yaml",
  
  // EXCLUDE all node_modules (bundled by Vite)
  "!**/node_modules/**",
  "!**/node_modules",
  "!**/packages/**",
  "!**/node_modules/.pnpm/**",
  "!**/*.ts",
  "!**/*.map",
  "!package-lock.json",
  "!pnpm-lock.yaml",
  "!yarn.lock"
]
```

### Platform Configurations

#### macOS

```javascript
mac: {
  icon: 'icons/mac/icon.icns',
  category: 'public.app-category.business',
  target: [
    {
      target: 'zip',
      arch: ['arm64', 'x64']  // Both Apple Silicon and Intel
    }
  ],
  hardenedRuntime: true,
  gatekeeperAssess: false,
  entitlements: 'entitlements.mac.plist',
  entitlementsInherit: 'entitlements.mac.plist',
  notarize: false
}
```

#### Linux (Debian/Raspberry Pi)

```javascript
linux: {
  icon: 'icons/png/',
  category: 'Office',
  target: [
    {
      target: 'deb',
      arch: ['x64', 'armv7l', 'arm64']  // x64, Pi 32-bit, Pi 64-bit
    },
    {
      target: 'AppImage',
      arch: ['x64', 'armv7l', 'arm64']
    }
  ],
  artifactName: '${productName}-${version}-${arch}.${ext}'
},

deb: {
  depends: [
    'libgtk-3-0', 'libnotify4', 'libnss3', 
    'libxss1', 'libxtst6', 'xdg-utils', 
    'libatspi2.0-0', 'libuuid1', 'libsecret-1-0'
  ],
  category: 'Office',
  priority: 'optional'
}
```

#### Windows

```javascript
win: {
  icon: 'icons/win/icon.ico',
  target: [{
    target: 'nsis',
    arch: ['x64']
  }]
},

nsis: {
  oneClick: false,
  allowToChangeInstallationDirectory: true,
  installerIcon: 'icons/win/icon.ico',
  uninstallerIcon: 'icons/win/icon.ico',
  createDesktopShortcut: true,
  createStartMenuShortcut: true,
  perMachine: true
}
```

### Extra Resources

```javascript
extraResources: [
  // Python service executable
  {
    from: '../dash-python-service/kt_service',
    to: 'python-service',
    filter: process.platform === 'win32' ? ['**/*.exe'] : ['**/kt_service']
  },
  // YAML configuration files
  {
    from: '../dash-python-service',
    to: 'python-service',
    filter: ['*.yaml']
  },
  // Icons
  {
    from: 'icons',
    to: 'icons'
  },
  // App config
  {
    from: 'apps/dash/',
    to: './',
    filter: ['*.yaml']
  }
]
```

---

## Build Commands

### NPM Scripts

Located in `package.json`:

| Command | Description |
|---------|-------------|
| `release:electron:kitchntabs:production` | Full production build for macOS |
| `release:electron:kitchntabs:debian` | Linux .deb for x64, armv7l, arm64 |
| `release:electron:kitchntabs:debian:dev` | Dev build for Linux (uses ngrok) |
| `release:electron:kitchntabs:development` | Development build for macOS |
| `release:electron:kitchntabs:production:app` | App-only build (skip web build) |

### Full Build Pipeline

```bash
# Production macOS build
pnpm release:electron:kitchntabs:production
```

This runs:
1. `pnpm config:electron:kitchntabs:production` - Set config
2. `electron-icon-builder --input=./apps/dash/src/assets/logo-squared.png --output=./` - Generate icons
3. `turbo build --no-cache` - Build React app and Electron process
4. `node build-electron.js --config electron-builder.config.js` - Package app

### Raspberry Pi Build

```bash
# Debian packages for Raspberry Pi (32-bit and 64-bit)
pnpm release:electron:kitchntabs:debian
```

This adds flags: `--linux deb --armv7l --arm64`

---

## Platform-Specific Builds

### Build Output

| Platform | Architecture | Output File |
|----------|--------------|-------------|
| macOS | arm64 | `release/kitchntabs-1.0.3-arm64-mac.zip` |
| macOS | x64 | `release/kitchntabs-1.0.3-mac.zip` |
| Linux | armv7l (Pi 32-bit) | `release/kitchntabs-1.0.3-armv7l.deb` |
| Linux | arm64 (Pi 64-bit) | `release/kitchntabs-1.0.3-arm64.deb` |
| Linux | x64 | `release/kitchntabs-1.0.3-x64.deb` |
| Windows | x64 | `release/kitchntabs-1.0.3.exe` |

### Architecture Notes

- **armv7l**: 32-bit ARM (Raspberry Pi OS 32-bit)
- **arm64**: 64-bit ARM (Raspberry Pi OS 64-bit, Apple Silicon)
- **x64**: 64-bit Intel/AMD

---

## Directory Structure

### Source Files

```
dash-frontend/
├── apps/
│   └── dash/
│       ├── electron/
│       │   ├── main/
│       │   │   └── index.ts          # Main process entry
│       │   └── preload/
│       │       └── index.ts          # Preload script
│       ├── src/                       # React renderer source
│       ├── dist/                      # Built renderer (after build)
│       ├── dist-electron/             # Built electron (after build)
│       │   ├── main/
│       │   │   └── index.js
│       │   └── preload/
│       │       └── index.js
│       ├── package.json               # App version info
│       └── config.prod.yaml           # Production config
├── build-electron.js                  # pnpm workaround wrapper
├── electron-builder.config.js         # Builder configuration
├── electron.vite.config.mts           # Vite bundling config
├── package.json                       # Build scripts
└── release/                           # Build output directory
```

### Build Output Structure (macOS)

```
kitchntabs.app/
└── Contents/
    ├── MacOS/
    │   └── kitchntabs              # Electron executable
    ├── Resources/
    │   ├── app/
    │   │   └── apps/dash/
    │   │       ├── dist/           # React build
    │   │       └── dist-electron/  # Electron build
    │   ├── icons/
    │   ├── python-service/
    │   └── config.prod.mac.yaml
    └── Info.plist
```

### Build Output Structure (Linux .deb)

```
/opt/kitchntabs/
├── kitchntabs                      # Electron executable
├── resources/
│   ├── app/
│   │   └── apps/dash/
│   │       ├── dist/
│   │       └── dist-electron/
│   ├── icons/
│   ├── python-service/
│   └── config.prod.yaml
└── [electron libraries]
```

---

## Config File Resolution

### The Problem

The main process needs to load `config.prod.yaml` at runtime. The path differs based on:
1. Development vs Production
2. Platform (macOS vs Linux vs Windows)
3. Packaged vs Unpackaged

### Solution in `index.ts`

```typescript
const BUILD_ENV: string = process.env.BUILD_ENV?.toLowerCase() || "prod";
const configFileName = process.platform === 'darwin' 
  ? `config.${BUILD_ENV}.mac.yaml` 
  : `config.${BUILD_ENV}.yaml`;

let configFile = "";
if (isDev) {
  // Development: relative to app directory
  configFile = path.join(appPath, `./${configFileName}`);
} else {
  // Production: config in resources folder
  if (process.platform === 'darwin') {
    // macOS: Resources folder inside .app bundle
    configFile = path.join(appPath, `./Resources/${configFileName}`);
  } else {
    // Linux/Windows: use absolute path from app.getAppPath()
    configFile = path.join(app.getAppPath(), `../${configFileName}`);
  }
}
```

### Path Resolution Table

| Platform | Environment | Path Pattern |
|----------|-------------|--------------|
| macOS | Development | `{appPath}/config.dev.mac.yaml` |
| macOS | Production | `{appPath}/Resources/config.prod.mac.yaml` |
| Linux | Development | `{appPath}/config.dev.yaml` |
| Linux | Production | `/opt/kitchntabs/resources/config.prod.yaml` |
| Windows | Development | `{appPath}/config.dev.yaml` |
| Windows | Production | `{appPath}/resources/config.prod.yaml` |

---

## Troubleshooting

### Common Issues

#### 1. "Unexpected end of JSON input"

**Cause**: electron-builder trying to parse pnpm node_modules structure

**Solution**: Ensure `build-electron.js` is being used:
```bash
node build-electron.js --config electron-builder.config.js
```

#### 2. "Cannot find module 'electron-updater'"

**Cause**: Module externalized but not bundled

**Solution**: Check `electron.vite.config.mts`:
```typescript
// Should only externalize electron
external: ['electron']  // NOT ['electron', 'electron-updater']
```

#### 3. "Config file not found" on Linux

**Cause**: Using relative path that doesn't resolve correctly

**Solution**: Use absolute path with `app.getAppPath()`:
```typescript
configFile = path.join(app.getAppPath(), `../${configFileName}`);
```

#### 4. Build succeeds but app crashes immediately

**Cause**: Usually missing config file or incorrect path

**Debug**: Check electron-log output:
```bash
# Linux
cat ~/.config/kitchntabs/logs/electron-log.txt

# macOS  
cat ~/Library/Application\ Support/kitchntabs/logs/electron-log.txt
```

#### 5. Package.json corrupted after failed build

**Recovery**:
```bash
git checkout package.json
```

The wrapper script should restore automatically, but if interrupted it may fail.

### Verify Build Environment

```bash
# Check Node version
node --version  # Should be v20.x

# Check pnpm
pnpm --version

# Check electron-builder
npx electron-builder --version  # Should be 26.0.12

# Check electron
npx electron --version  # Should be 36.7.4
```

### Manual Build Steps (for debugging)

```bash
# 1. Build React app
pnpm turbo build --no-cache

# 2. Generate icons
npx electron-icon-builder --input=./apps/dash/src/assets/logo-squared.png --output=./

# 3. Run wrapper script with verbose output
DEBUG=electron-builder node build-electron.js --config electron-builder.config.js
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.3 | 2024-11-28 | Fixed config path resolution for Linux, bundle all deps |
| 1.0.2 | 2024-11-28 | Added pnpm workspace workaround |
| 1.0.0 | 2024-11-xx | Initial release |

---

## References

- [electron-builder Documentation](https://www.electron.build/)
- [Vite Plugin Electron](https://github.com/electron-vite/vite-plugin-electron)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Electron Documentation](https://www.electronjs.org/docs)
