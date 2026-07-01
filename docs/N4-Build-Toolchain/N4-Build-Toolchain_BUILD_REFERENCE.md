# Build Reference Card — All Platforms

Quick lookup for all production build commands across Android, iOS, macOS, and Linux.

---

## Android

### **AAB (Google Play Store)**
```bash
pnpm release:android:kitchntabs-app:production
```
- Output: `android/app/build/outputs/bundle/release/app-release.aab`
- Size: ~60-80 MB
- Time: ~10-15 min
- Use for: Google Play Store submission

### **APK (Direct Installation)**
```bash
pnpm release-apk:android:kitchntabs-app:production
```
- Output: `android/app/build/outputs/apk/release/app-release.apk`
- Size: ~120-150 MB
- Time: ~10-15 min
- Use for: Testing, direct install via `adb`

**Full docs:** See `ANDROID_BUILD_GUIDE.md`

---

## macOS

### **Apple Silicon (M1/M2/M3)**
```bash
pnpm release:electron:kitchntabs-app:macos:arm64:production
```
- Output: `release/kitchntabs-1.3.37-arm64.dmg`
- Size: ~180-200 MB
- Time: ~12-20 min (includes 3-5 min S3 upload)
- Upload: S3 auto-upload enabled

### **Intel (x64)**
```bash
pnpm release:electron:kitchntabs-app:macos:x64:production
```
- Output: `release/kitchntabs-1.3.37-x64.dmg`
- Size: ~180-200 MB
- Time: ~12-20 min (includes 3-5 min S3 upload)
- Upload: S3 auto-upload enabled

**Full docs:** See `MACOS_BUILD_GUIDE.md`

---

## Linux

### **Debian ARM64 (Raspberry Pi 64-bit)**
```bash
pnpm release:electron:kitchntabs-app:debian:arm64:production
```
- Output: `release/kitchntabs-1.3.37-arm64.deb`
- Size: ~150-180 MB (asar enabled)
- Time: ~12-20 min (includes 3-5 min S3 upload)
- Upload: S3 auto-upload enabled

### **Debian x64 (Linux PC/Server)**
```bash
pnpm release:electron:kitchntabs-app:debian:amd64:production
```
- Output: `release/kitchntabs-1.3.37-x64.deb`
- Size: ~150-180 MB (asar enabled)
- Time: ~12-20 min (includes 3-5 min S3 upload)
- Upload: S3 auto-upload enabled

**Full docs:** See `LINUX_BUILD_GUIDE.md` (if exists, or use Debian scripts above)

---

## Build Features (All Production Builds)

✅ **Minification** — Code is minified for smallest size
✅ **Console stripping** — All `console.log()` statements removed
✅ **Error-only logging** — Only `console.error()` and `log.error()` visible
✅ **Asar enabled** — App code compressed into archive
✅ **Python services** — Pre-integrated and bundled
✅ **Auto-upload** — S3 upload on success (Electron builds)
✅ **AWS auth** — Credentials from `kitchntabs` AWS profile
✅ **Signing** — APK/AAB signed with release keystore (Android); code-signed (macOS/Linux)

---

## Prerequisites

### All Platforms
```bash
pnpm install                    # Install dependencies
pnpm turbo build                # Verify turbo works
export NODE_OPTIONS=--max-old-space-size=4048  # If OOM errors
```

### Android
```bash
which adb gradlew keytool       # Check tools installed
ls android/                     # Check Capacitor exists
```

### macOS/Linux (Electron)
```bash
which electron-builder          # Check builder installed
export AWS_PROFILE=kitchntabs   # AWS auth (set automatically in scripts)
```

---

## Build Timeline Summary

| Platform | Type | Time | Size |
|----------|------|------|------|
| **Android** | AAB | ~10-15 min | 60-80 MB |
| **Android** | APK | ~10-15 min | 120-150 MB |
| **macOS** | arm64 (.dmg) | ~12-20 min | 180-200 MB |
| **macOS** | x64 (.dmg) | ~12-20 min | 180-200 MB |
| **Linux** | arm64 (.deb) | ~12-20 min | 150-180 MB |
| **Linux** | x64 (.deb) | ~12-20 min | 150-180 MB |

---

## Upload Destinations

| Platform | Build | Destination | Auto-Upload |
|----------|-------|-------------|-------------|
| Android | AAB | Google Play Console (manual) | ❌ No |
| Android | APK | Direct install / Slack / Drive | ❌ No |
| macOS | .dmg | S3 `kitchntabs-releases` | ✅ Yes |
| Linux | .deb | S3 `kitchntabs-releases` | ✅ Yes |

---

## Configuration Files

| File | Purpose |
|------|---------|
| `apps/kitchntabs-app/package.json` | App version & dependencies |
| `package.json` (root) | Build scripts & versions |
| `electron.vite.config.mts` | Electron build config (Vite) |
| `electron-builder.config.js` | Electron packaging (electron-builder) |
| `apps/kitchntabs-app/vite.config.mts` | React app build config |
| `android/app/build.gradle` | Android/Gradle config |
| `PRODUCTION_OPTIMIZATIONS.md` | Minification & logging details |

---

## Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| `Cannot find module` | Run `pnpm install` |
| `Out of memory` | Increase `NODE_OPTIONS=--max-old-space-size=8192` |
| S3 upload hangs | Increase `publish.timeout` in config |
| APK install fails | Check `minSdkVersion` in gradle; use `adb devices` to verify device |
| Android build too slow | Run with `--no-cache` flag; check disk space |
| macOS code signing fails | Ensure Apple Developer cert configured (see `MACOS_BUILD_GUIDE.md`) |
| Python services missing | Rebuild with `node build-python-service.js` or check `../dash-python-service/` |

---

## Full Documentation

- **ANDROID_BUILD_GUIDE.md** — Complete Android AAB/APK guide
- **MACOS_BUILD_GUIDE.md** — Complete macOS M1/Intel guide
- **PRODUCTION_OPTIMIZATIONS.md** — Minification & console stripping
- **ASAR_TEST_PLAN.md** — App archive compression details
- **DEVELOPMENT.md** — Dash packages development workflow

---

## Version Updates

Before each release, update the version in **`package.json`**:

```json
{
  "version": "1.3.37"
}
```

This automatically updates:
- All build artifact filenames
- Electron auto-updater metadata (`latest-mac.yml`, etc.)
- App version in Android/macOS/Linux builds

---

## Quick Start (New Dev)

1. Clone repo & `pnpm install`
2. Choose your target platform from this card
3. Run the build command
4. Watch for errors in terminal
5. Artifacts appear in `release/` (Electron) or `android/app/build/outputs/` (Android)

---

_Last updated: 2026-07-01_
_Covers: Android AAB/APK, macOS arm64/x64, Linux arm64/x64_
