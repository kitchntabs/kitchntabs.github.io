# macOS Build Guide — M1/M2/M3 and Intel

## Quick Start

### For macOS M1/M2/M3 (Apple Silicon)
```bash
pnpm release:electron:kitchntabs-app:macos:arm64:production
```

### For macOS Intel (x64)
```bash
pnpm release:electron:kitchntabs-app:macos:x64:production
```

Both commands:
- ✅ Build for production (minification + console stripping enabled)
- ✅ Compile Electron main/preload processes
- ✅ Package as `.dmg` or `.zip` (electron-builder configures this)
- ✅ Upload to S3 automatically (`--publish always`)
- ✅ Use AWS credentials from `kitchntabs` profile

---

## What Each Script Does

### Step-by-Step Breakdown

```
1. pnpm config:electron:kitchntabs-app:production
   └─ Generates build_config.json with production settings
   └─ Sets MODE=production, CUSTOM_MODE=kitchntabs.production
   └─ Triggers environment setup

2. turbo build --filter=kitchntabs-app --no-cache
   └─ Builds the React app (apps/kitchntabs-app/dist)
   └─ Minification + console stripping active (production)

3. node build-python-service.js
   └─ Prepares Python services for macOS
   └─ Copies binaries to resources/python-service/

4. electron-icon-builder --input=./assets/logo-squared.png
   └─ Generates macOS .icns icon from PNG

5. vite build -c electron.vite.config.mts
   └─ Builds Electron main + preload processes
   └─ Minifies (production) or leaves unminified (dev)

6. cross-env AWS_PROFILE=kitchntabs ... node build-electron.js
   └─ Runs electron-builder with AWS credentials
   └─ Packages as .dmg (macOS)
   └─ Publishes to S3 (kitchntabs-releases bucket)
```

---

## Build Artifacts

### Output Location
```
release/
├── kitchntabs-1.3.37-arm64.dmg      # M1/M2/M3 (arm64)
├── kitchntabs-1.3.37-arm64.dmg.blockmap
├── kitchntabs-1.3.37-x64.dmg        # Intel (x64)
├── kitchntabs-1.3.37-x64.dmg.blockmap
├── macos-arm64-unpacked/            # Unpacked build directory
└── builder-effective-config.yaml    # electron-builder config used
```

### File Sizes (Estimated)

| Arch | Format | Size | Note |
|------|--------|------|------|
| arm64 | .dmg | ~180-200 MB | Apple Silicon (M1/M2/M3) |
| x64 | .dmg | ~180-200 MB | Intel MacBook Pro / Air |

---

## S3 Upload Details

Both commands upload to the **same S3 bucket** with architecture-specific filenames:

```
s3://kitchntabs-releases/
├── releases/
│   ├── kitchntabs-1.3.37-arm64.dmg
│   ├── kitchntabs-1.3.37-arm64.dmg.blockmap
│   ├── kitchntabs-1.3.37-x64.dmg
│   └── kitchntabs-1.3.37-x64.dmg.blockmap
│   └── latest-mac.yml          # Latest version metadata
```

The `.blockmap` files and `latest-mac.yml` enable delta updates (electron-updater downloads only changed bytes).

---

## Prerequisites

### AWS Credentials
```bash
# Verify your AWS profile has S3 access
aws s3 ls kitchntabs-releases --profile kitchntabs
```

If not configured:
```bash
aws configure --profile kitchntabs
# Enter AWS Access Key ID
# Enter AWS Secret Access Key
# Region: us-east-2
# Format: json
```

### Build Dependencies
```bash
pnpm install              # Install all dependencies
pnpm turbo build          # Verify turbo builds work
```

### Python Services
Ensure dash-python-service is available:
```bash
ls -la ../dash-python-service/kt_service_builds/arm64/
# Should show: kt_service, print_service, tts_service
```

---

## Build Process Timeline

| Step | Time | Notes |
|------|------|-------|
| Config | ~5s | Quick setup |
| Turbo build | ~2-3 min | React + TypeScript compilation |
| Python setup | ~10s | Copy binaries |
| Icons | ~5s | Generate .icns |
| Vite build | ~30s | Electron main/preload |
| electron-builder | ~5-10 min | Package + sign |
| S3 upload | ~3-5 min | Depends on network (200MB file) |
| **Total** | **~12-20 min** | One-time production release |

---

## Environment Variables

These are set automatically by the scripts, but you can override:

```bash
# Override AWS profile
AWS_PROFILE=my-other-profile pnpm release:electron:kitchntabs-app:macos:arm64:production

# Increase Node memory limit (if OOM errors)
NODE_OPTIONS=--max-old-space-size=16384 pnpm release:electron:kitchntabs-app:macos:arm64:production

# Build without upload (for testing)
pnpm config:electron:kitchntabs-app:production && \
turbo build --filter=kitchntabs-app --no-cache && \
node build-python-service.js && \
electron-icon-builder --input=./assets/logo-squared.png --output=./ && \
vite build -c electron.vite.config.mts && \
NODE_OPTIONS=--max-old-space-size=8096 node build-electron.js --config electron-builder.config.js --macos --arm64
# (note: no --publish always, no cross-env AWS_PROFILE)
```

---

## Troubleshooting

### S3 Upload Hangs/Times Out
The timeout is set to 10 minutes. If it still times out:
```bash
# Check upload speed
# Terminal 1: Monitor network
iftop -i en0

# Terminal 2: Run build
pnpm release:electron:kitchntabs-app:macos:arm64:production
```

If upload is very slow (~1 MB/s), consider:
- Check WiFi signal strength
- Wired Ethernet if possible
- Increase timeout in `electron-builder.config.js` → `publish.timeout`

### Missing Python Services
```bash
# Verify binaries exist for your architecture
ls ../dash-python-service/kt_service_builds/arm64/
# Should show: kt_service, print_service, tts_service

# If missing, build them:
cd ../dash-python-service
npm run build:docker:arm64    # For M1/M2/M3
npm run build:docker:x64      # For Intel
```

### Out of Memory
```bash
# Increase Node heap size
NODE_OPTIONS=--max-old-space-size=16384 pnpm release:electron:kitchntabs-app:macos:arm64:production
```

### Code Signing / Notarization
Currently **disabled** in config (see `electron-builder.config.js` line 237):
```js
notarize: false,  // Set to true if you have Apple Developer credentials
```

For production macOS App Store / developer distribution, you'll need:
1. Apple Developer ID certificate
2. Configure signing in `electron-builder.config.js`
3. Set `notarize: true` for App Transport Security

---

## Verification

### After Build Completes

```bash
# Check release artifacts
ls -lh release/*.dmg

# Verify S3 upload
aws s3 ls kitchntabs-releases/releases/ --profile kitchntabs | grep -E "\.dmg|\.yml"

# Extract and inspect the .dmg (optional)
hdiutil mount release/kitchntabs-1.3.37-arm64.dmg
ls /Volumes/kitchntabs/
hdiutil unmount /Volumes/kitchntabs/
```

### Test the Built App

```bash
# Extract from .dmg
hdiutil mount release/kitchntabs-1.3.37-arm64.dmg
# Drag kitchntabs.app to /Applications (or run from volume)
open /Volumes/kitchntabs/kitchntabs.app
```

Check logs:
```bash
# Electron logs
cat ~/Library/Logs/kitchntabs/electron-log.txt

# System logs
log stream --predicate 'process == "kitchntabs"'
```

---

## Universal Binary (Optional)

To build a **universal binary** that runs on both M1 AND Intel without electron-updater complexity:

Edit `electron-builder.config.js`:
```js
mac: {
  icon: 'icons/mac/icon.icns',
  target: [
    {
      target: 'dmg',
      arch: ['arm64', 'x64']  // Both in one .dmg
    },
    {
      target: 'zip',
      arch: ['universal']  // Universal binary (bigger file)
    }
  ]
}
```

Then run:
```bash
pnpm config:electron:kitchntabs-app:production && \
turbo build --filter=kitchntabs-app --no-cache && \
node build-python-service.js && \
electron-icon-builder --input=./assets/logo-squared.png --output=./ && \
vite build -c electron.vite.config.mts && \
NODE_OPTIONS=--max-old-space-size=8096 node build-electron.js --config electron-builder.config.js --macos
# (no --arm64 or --x64 = builds all configured arches)
```

---

## Version Bumping

Before each release, update the version in `package.json`:

```json
{
  "version": "1.3.37"
}
```

This automatically:
- Updates `.dmg` filename to `kitchntabs-1.3.37-arm64.dmg`
- Updates `latest-mac.yml` version check
- Enables delta updates (electron-updater)

---

## Related Documentation

- **PRODUCTION_OPTIMIZATIONS.md** — Minification & console stripping
- **electron-builder.config.js** — Full build configuration
- **ASAR_TEST_PLAN.md** — App archive compression details

---

_Last updated: 2026-07-01_
_Status: macOS M1/Intel arm64/x64 builds with S3 auto-upload ✅_
