# KitchnTabs Documentation Index

Master index of all build, deployment, and development documentation.

---

## 🚀 Getting Started

**New to KitchnTabs builds?** Start here:

1. **[BUILD_REFERENCE.md](BUILD_REFERENCE.md)** (5 min read)
   - Quick command reference for all platforms
   - Choose your target (Android/macOS/Linux)
   - Copy-paste build commands

2. **[PRODUCTION_OPTIMIZATIONS.md](PRODUCTION_OPTIMIZATIONS.md)** (10 min read)
   - Understand what's optimized in production builds
   - Minification & console stripping details
   - Why builds are faster

---

## 📱 Platform-Specific Guides

### Android

**[ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md)** — Complete Android reference

| Format | Use Case | Command |
|--------|----------|---------|
| **AAB** | Google Play Store | `pnpm release:android:kitchntabs-app:production` |
| **APK** | Direct install / Testing | `pnpm release-apk:android:kitchntabs-app:production` |

Topics:
- Signing & keystore configuration
- Gradle setup & troubleshooting
- Version management (versionCode)
- Testing via ADB
- Development vs production builds
- Google Play Console submission

---

### macOS

**[MACOS_BUILD_GUIDE.md](MACOS_BUILD_GUIDE.md)** — Complete macOS reference

| Architecture | Command |
|--------------|---------|
| **M1/M2/M3** (arm64) | `pnpm release:electron:kitchntabs-app:macos:arm64:production` |
| **Intel** (x64) | `pnpm release:electron:kitchntabs-app:macos:x64:production` |

Topics:
- AWS S3 auto-upload setup
- Python services integration
- Code signing & notarization
- Universal binary creation
- S3 credential configuration

---

### Linux

**Build scripts:**

| Platform | Command |
|----------|---------|
| **Raspberry Pi 64-bit** | `pnpm release:electron:kitchntabs-app:debian:arm64:production` |
| **Linux PC/Server** | `pnpm release:electron:kitchntabs-app:debian:amd64:production` |

Details: See **[BUILD_REFERENCE.md](BUILD_REFERENCE.md)** for Linux section

---

## 🔧 Build Configuration & Optimization

### [PRODUCTION_OPTIMIZATIONS.md](PRODUCTION_OPTIMIZATIONS.md)

Covers production-only settings:
- Minification (code -20-30% size)
- Console log stripping
- Error-only logging in production
- Environment-aware logging
- Verification steps

**Key features:**
- React app: console statements removed
- Electron main/preload: minified
- Logging: production switches to `error` level only

---

## 🌍 Environment Configuration System

### [ENVIRONMENT_CONFIGURATION_SYSTEM.md](https://github.com/kitchntabs/kitchntabs-github-io/blob/main/docs/N4-Build-Toolchain/N4-Build-Toolchain_ENVIRONMENT_CONFIGURATION_SYSTEM.md)

Complete technical guide to the build-time environment key system (in docs repo):

- **End-to-end data flow** — how `.env`, `build_config.js`, and vite's `define` work together
- **Precedence rules** — library default → .env file → release script override
- **PAGE_TRANSITIONS example** — environment-driven flag for Raspberry Pi animations
- **Recipe for adding new keys** — step-by-step pattern with code examples
- **Mermaid diagrams** — visual flow from source to runtime
- **Troubleshooting** — why flags don't take effect and how to debug

Covers all 6 core environment keys and boolean parsing best practices.

---

## 📦 Asar (App Archive) Compression

### [ASAR_TEST_PLAN.md](ASAR_TEST_PLAN.md)

Guide for testing the asar (app archive) feature:
- Why asar is enabled (smaller download)
- How to verify it works
- Expected size reduction (25-35%)
- Troubleshooting unpacking issues

---

## 📚 Source Package Development

### [DEVELOPMENT.md](DEVELOPMENT.md) (dash-frontend-core repo)

If you're modifying the `dash-*` source packages:
- How source → published workflow works
- Verdaccio local registry setup
- Version bump policy
- NPM publish script usage
- Dependency management

---

## 📋 Document Quick Links

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [BUILD_REFERENCE.md](BUILD_REFERENCE.md) | Quick command lookup | 5 min |
| [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md) | Android AAB & APK | 20 min |
| [MACOS_BUILD_GUIDE.md](MACOS_BUILD_GUIDE.md) | macOS M1/Intel | 15 min |
| [PRODUCTION_OPTIMIZATIONS.md](PRODUCTION_OPTIMIZATIONS.md) | Minification & logging | 10 min |
| [ASAR_TEST_PLAN.md](ASAR_TEST_PLAN.md) | App archive testing | 10 min |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Source packages (dash-*) | 15 min |

---

## 🎯 Common Tasks

### Build for production & upload to S3 (macOS/Linux)

```bash
# macOS M1
pnpm release:electron:kitchntabs-app:macos:arm64:production

# Linux ARM64
pnpm release:electron:kitchntabs-app:debian:arm64:production
```

See: [MACOS_BUILD_GUIDE.md](MACOS_BUILD_GUIDE.md) or [BUILD_REFERENCE.md](BUILD_REFERENCE.md)

---

### Build Android for Google Play Store

```bash
pnpm release:android:kitchntabs-app:production
```

Then upload the `.aab` file to Google Play Console.

See: [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md)

---

### Build Android APK for testing

```bash
pnpm release-apk:android:kitchntabs-app:production
adb install -r android/app/build/outputs/apk/release/app-release.apk
```

See: [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md) — Local Testing section

---

### Update source packages & publish

1. Edit source in `/dash-frontend-core/packages/dash-*`
2. Bump version
3. `pnpm publish:local` (Verdaccio) or `NPM_TOKEN=... node scripts/publish-npm.mjs` (npm)
4. Re-run `pnpm install` in `kitchntabs-frontend-refactored`

See: [DEVELOPMENT.md](DEVELOPMENT.md) (in `/dash-frontend-core`)

---

## ⚠️ Important Notes

### Security

- 🔒 **Never commit AWS credentials** to git
- 🔒 **Rotate npm tokens** if shared in chat/logs
- 🔒 **Protect keystores** (Android signing keys)

See: Platform guides for credential setup

---

### Version Management

All production builds use the version in **`package.json`** (root):

```json
{
  "version": "1.3.37"
}
```

Update this before each release.

---

### Build Timeline

| Platform | Time | Size |
|----------|------|------|
| Android AAB | ~10-15 min | 60-80 MB |
| Android APK | ~10-15 min | 120-150 MB |
| macOS | ~12-20 min | 180-200 MB |
| Linux | ~12-20 min | 150-180 MB |

Includes compile time + upload (Electron).

---

## 📞 Troubleshooting

**Something broken?**

1. Check [BUILD_REFERENCE.md](BUILD_REFERENCE.md) — Troubleshooting quick links
2. Platform-specific guide (Android/macOS/Linux)
3. Search for error message in relevant guide

---

## 📂 File Structure

```
kitchntabs-frontend-refactored/
├── DOCUMENTATION_INDEX.md        ← You are here
├── BUILD_REFERENCE.md            ← Quick lookup
├── ANDROID_BUILD_GUIDE.md        ← Android detailed
├── MACOS_BUILD_GUIDE.md          ← macOS detailed
├── PRODUCTION_OPTIMIZATIONS.md   ← Minification & logging
├── ASAR_TEST_PLAN.md             ← App archive testing
├── package.json                  ← Scripts & version
├── electron-builder.config.js    ← Electron packaging
├── electron.vite.config.mts      ← Electron build
├── apps/kitchntabs-app/
│   ├── vite.config.mts           ← React app build
│   ├── electron/main/index.ts    ← Electron entry
│   └── package.json              ← App version
└── android/
    └── app/build.gradle          ← Android config
```

---

## 📚 Reading Order (by role)

### QA / Tester
1. [BUILD_REFERENCE.md](BUILD_REFERENCE.md) — understand build commands
2. Platform-specific guide (for your target platform)
3. [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md) — Local Testing section

### DevOps / Release Engineer
1. [BUILD_REFERENCE.md](BUILD_REFERENCE.md) — all commands at a glance
2. [PRODUCTION_OPTIMIZATIONS.md](PRODUCTION_OPTIMIZATIONS.md)
3. Platform guides (Android/macOS/Linux)

### Frontend Developer
1. [PRODUCTION_OPTIMIZATIONS.md](PRODUCTION_OPTIMIZATIONS.md) — understand minification
2. [DEVELOPMENT.md](DEVELOPMENT.md) (dash-frontend-core) — if modifying source packages
3. Platform guides as needed

### DevSecOps / Security
1. [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md) — Signing configuration
2. [MACOS_BUILD_GUIDE.md](MACOS_BUILD_GUIDE.md) — Code signing & notarization
3. Check all guides for credential handling

---

## 🔄 Last Updated

- **2026-07-01** — Documentation complete
- Covers: Android (AAB/APK), macOS (M1/Intel), Linux (arm64/x64)
- All production builds: minification, console stripping, error-only logging, S3 auto-upload

---

_Start with [BUILD_REFERENCE.md](BUILD_REFERENCE.md) — it's your fastest path to building._
