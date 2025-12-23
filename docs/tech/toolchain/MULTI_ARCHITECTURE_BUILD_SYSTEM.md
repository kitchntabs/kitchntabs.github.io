# Multi-Architecture Build System for Electron + Python Services

## Overview

This document describes the cross-compilation build system used to package Python services alongside an Electron application for multiple Linux ARM architectures. The system enables building executable binaries on a macOS development machine that can run natively on Raspberry Pi and other ARM-based Linux devices.

The solution combines:
- **Docker buildx** with QEMU emulation for cross-compiling Python services
- **PyInstaller** for creating standalone executables
- **electron-builder** with custom `afterPack` hooks for architecture-specific binary injection

---

## Requirements

### Development Environment
- **macOS** (Apple Silicon or Intel)
- **Docker Desktop** with buildx plugin
- **Node.js** 18+ with pnpm
- **Python 3.9** with virtual environment

### Docker Configuration
- Docker buildx builder with multi-platform support
- QEMU user-static for ARM emulation
- Sufficient disk space (~20GB for build cache)

### Target Platforms
| Platform | Architecture | Use Case |
|----------|-------------|----------|
| `linux/arm/v7` | ARMv7l (32-bit) | Raspberry Pi 3/4 (32-bit OS) |
| `linux/arm64` | ARM64 (64-bit) | Raspberry Pi 4/5 (64-bit OS) |
| `darwin/arm64` | Apple Silicon | macOS development/production |

---

## Architecture

### Directory Structure

```
dash-python-service/
├── src/
│   ├── kt_service.py          # Main WebSocket service
│   ├── print_service.py       # Thermal printing service
│   └── tts_service.py         # Text-to-Speech service
├── docker/
│   ├── Dockerfile.linux-armv7l  # ARM 32-bit build
│   └── Dockerfile.linux-arm64   # ARM 64-bit build
├── kt_service_builds/           # Cross-compiled outputs
│   ├── armv7l/
│   │   ├── kt_service
│   │   ├── print_service
│   │   └── tts_service
│   └── arm64/
│       ├── kt_service
│       ├── print_service
│       └── tts_service
├── kt_service/                  # Native macOS builds
├── build-docker.js              # Docker cross-compilation orchestrator
├── build.js                     # Native PyInstaller build script
└── config.*.yaml                # Configuration files

dash-frontend/
├── electron-builder.config.js   # Electron packaging with afterPack hooks
├── build-python-service.js      # Pre-build verification script
└── release/
    ├── kitchntabs-*-armv7l.deb  # ARM 32-bit package
    └── kitchntabs-*-arm64.deb   # ARM 64-bit package
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        macOS Development Machine                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
│  │  build-python-  │───▶│  build-docker   │───▶│  kt_service_    │     │
│  │  service.js     │    │  .js            │    │  builds/        │     │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘     │
│          │                      │                      │                │
│          │                      ▼                      │                │
│          │              ┌───────────────┐              │                │
│          │              │ Docker buildx │              │                │
│          │              │ + QEMU        │              │                │
│          │              └───────────────┘              │                │
│          │                      │                      │                │
│          ▼                      ▼                      ▼                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    electron-builder                              │   │
│  │                    afterPack hook                                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │   │
│  │  │ armv7l pkg  │  │  arm64 pkg  │  │  darwin pkg │              │   │
│  │  │ (Docker)    │  │  (Docker)   │  │  (Native)   │              │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
            ┌───────────────────────────────────────────┐
            │           Output Packages                  │
            ├───────────────────────────────────────────┤
            │  • kitchntabs-1.0.19-armv7l.deb           │
            │  • kitchntabs-1.0.19-arm64.deb            │
            │  • kitchntabs-1.0.19-arm64.dmg (macOS)    │
            └───────────────────────────────────────────┘
```

---

## Build Flow

### 1. Pre-Build Verification (`build-python-service.js`)

The frontend build script first verifies Docker builds exist for Linux ARM targets:

```javascript
function checkDockerBuilds() {
    const services = ['kt_service', 'print_service', 'tts_service'];
    const archs = ['armv7l', 'arm64'];
    
    for (const arch of archs) {
        for (const service of services) {
            // Check if binary exists and has valid size
            const binaryPath = `kt_service_builds/${arch}/${service}`;
            if (!exists(binaryPath)) {
                return { complete: false, missing: [service] };
            }
        }
    }
    return { complete: true };
}
```

### 2. Docker Cross-Compilation (`build-docker.js`)

If Docker builds are missing or outdated, the script triggers cross-compilation:

```bash
# Build for ARM 32-bit (Raspberry Pi)
pnpm build:docker:armv7l:ngrok

# Build for ARM 64-bit
pnpm build:docker:arm64:ngrok
```

**Docker Build Process:**

1. **QEMU Setup**: Registers ARM binary handlers via `tonistiigi/binfmt`
2. **Builder Creation**: Creates buildx builder with multi-platform support
3. **Image Build**: Runs Dockerfile with `--platform linux/arm/v7` or `linux/arm64`
4. **Binary Extraction**: Copies PyInstaller outputs from container to host

### 3. Dockerfile Structure

```dockerfile
# Dockerfile.linux-armv7l
FROM python:3.9-slim-bullseye

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential ffmpeg libusb-1.0-0-dev \
    libasound2-dev portaudio19-dev libsndfile1-dev

WORKDIR /app

# Install Python dependencies with piwheels (ARM-optimized)
RUN pip install --upgrade pip && \
    echo "[global]\nextra-index-url=https://www.piwheels.org/simple" > /etc/pip.conf

COPY requirements-armv7l.txt ./requirements.txt
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt && \
    pip install pyinstaller

# Copy source and config
COPY src/ ./src/
COPY config*.yaml ./
RUN cp ${CONFIG_FILE} config.yaml

# Build all three services
RUN python -m PyInstaller ./src/kt_service.py --onefile --distpath ./dist \
    --add-data "config.yaml:." --collect-data escpos

RUN python -m PyInstaller ./src/print_service.py --onefile --distpath ./dist \
    --add-data "config.yaml:." --collect-data escpos

RUN python -m PyInstaller ./src/tts_service.py --onefile --distpath ./dist

# Copy to output directory
RUN mkdir -p /output && \
    cp ./dist/kt_service /output/ && \
    cp ./dist/print_service /output/ && \
    cp ./dist/tts_service /output/
```

### 4. Electron Packaging (`electron-builder.config.js`)

The `afterPack` hook injects architecture-specific binaries:

```javascript
afterPack: async (context) => {
    const { electronPlatformName, arch } = context;
    const services = ['kt_service', 'print_service', 'tts_service'];
    
    // Determine architecture mapping
    const archMap = {
        1: 'x64',
        2: 'armv7l',  // Arch.armv7l
        3: 'arm64'   // Arch.arm64
    };
    
    const targetArch = archMap[arch];
    const pythonServiceDir = path.join(context.appOutDir, 'resources', 'python-service');
    
    for (const service of services) {
        let sourcePath;
        
        if (electronPlatformName === 'linux' && ['armv7l', 'arm64'].includes(targetArch)) {
            // Use Docker-built binaries for Linux ARM
            sourcePath = path.join(dockerBuildsDir, targetArch, service);
        } else {
            // Use native build for macOS
            sourcePath = path.join(nativeBuildsDir, service);
        }
        
        fs.copyFileSync(sourcePath, path.join(pythonServiceDir, service));
        fs.chmodSync(path.join(pythonServiceDir, service), 0o755);
    }
}
```

---

## QEMU Setup

### Initial Configuration

QEMU must be registered in Docker's Linux VM before cross-compilation:

```bash
# Install QEMU handlers (run once per Docker restart)
docker run --rm --privileged --platform linux/arm64 \
    tonistiigi/binfmt:latest --install all
```

### Builder Creation

Create a buildx builder with multi-architecture support:

```bash
# Remove existing builder if misconfigured
docker buildx rm kt-builder 2>/dev/null

# Create new builder with ARM support
docker buildx create \
    --name kt-builder \
    --driver docker-container \
    --bootstrap \
    --platform linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6

# Set as default builder
docker buildx use kt-builder

# Verify platforms
docker buildx ls
# Expected output:
# kt-builder *  docker-container
#   kt-builder0  ... running linux/amd64*, linux/arm64*, linux/arm/v7*, linux/arm/v6*
```

---

## Build Commands

### Full Release Build

```bash
# From dash-frontend directory
cd /path/to/dash-frontend

# Build Debian packages for ARM (dev mode)
pnpm release:electron:kitchntabs:debian:dev

# Build Debian packages for ARM (production)
pnpm release:electron:kitchntabs:debian:prod
```

### Individual Docker Builds

```bash
# From dash-python-service directory
cd /path/to/dash-python-service

# Build ARM 32-bit with ngrok config
pnpm build:docker:armv7l:ngrok

# Build ARM 64-bit with ngrok config
pnpm build:docker:arm64:ngrok

# Build ARM 32-bit with production config
pnpm build:docker:armv7l:prod

# Build ARM 64-bit with production config
pnpm build:docker:arm64:prod
```

### Native macOS Build

```bash
# Build for current platform (macOS)
pnpm build:service:all:ngrok
```

---

## Caveats and Troubleshooting

### 1. QEMU "exec format error"

**Symptom:**
```
exec /bin/sh: exec format error
```

**Cause:** QEMU handlers are not registered in Docker's VM.

**Solution:**
```bash
# Re-register QEMU handlers
docker run --rm --privileged --platform linux/arm64 \
    tonistiigi/binfmt:latest --install all

# Verify registration
docker run --rm --platform linux/arm/v7 alpine:latest echo "ARM works!"
```

### 2. Buildx Builder Missing ARM Platforms

**Symptom:** Build fails with platform not supported.

**Cause:** The buildx builder wasn't created with ARM platforms.

**Solution:**
```bash
# Check current platforms
docker buildx ls

# If ARM missing, recreate builder
docker buildx rm kt-builder
docker buildx create --name kt-builder --driver docker-container \
    --bootstrap --platform linux/amd64,linux/arm64,linux/arm/v7
docker buildx use kt-builder
```

### 3. Disk Space Exhaustion

**Symptom:**
```
cp: error writing '/output/kt_service': No space left on device
```

**Cause:** Docker build cache is full.

**Solution:**
```bash
# Clean all Docker resources
docker system prune -a -f --volumes

# Clear buildx cache
docker buildx prune --all -f
```

### 4. QEMU Not Persisting After Docker Restart

**Cause:** QEMU registration is lost when Docker Desktop restarts.

**Solution:** Run QEMU registration before each build session:
```bash
docker run --rm --privileged --platform linux/arm64 \
    tonistiigi/binfmt:latest --install arm
```

Or add to `build-docker.js` to auto-register.

### 5. Wrong Binary Architecture in Package

**Symptom:** Application crashes on Raspberry Pi with "cannot execute binary file."

**Verification:**
```bash
# Check binary architecture
file release/linux-armv7l-unpacked/resources/python-service/kt_service

# Expected for ARMv7l:
# ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV)

# Expected for ARM64:
# ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV)
```

**Cause:** afterPack hook using wrong source directory.

**Solution:** Verify `electron-builder.config.js` has correct path logic.

### 6. piwheels Dependency Issues (ARMv7l Only)

**Symptom:** pip install fails for numpy/scipy on ARM 32-bit.

**Cause:** Some packages aren't available on piwheels.

**Solution:** Use `requirements-armv7l.txt` with pinned versions known to work:
```txt
numpy==1.24.3
scipy==1.10.1
```

---

## Performance Considerations

| Architecture | Build Time | Binary Size (kt_service) |
|--------------|------------|--------------------------|
| macOS ARM64 (native) | ~60s | 90 MB |
| Linux ARM64 (Docker) | ~90s | 109 MB |
| Linux ARMv7l (Docker) | ~800s | 22 MB |

**Notes:**
- ARMv7l builds are significantly slower due to QEMU emulation overhead
- ARMv7l binaries are smaller due to 32-bit architecture
- Build times improve with cached Docker layers

---

## Service Configuration

Each service reads from `config.yaml` bundled at build time:

```yaml
# WebSocket Configuration
WS_HOST: ""
WS_PORT: ""  # Empty for Electron (managed by main process)
WS_SCHEME: "wss"

# Text-to-Speech Configuration
SPEECH_WELCOME_MESSAGE: "Bienvenido a kitchentabs"
SPEECH_CONNECTED_MESSAGE: "Conectado al servidor"
SPEECH_LANGUAGE: "es"

# Paths (relative to executable in packaged app)
CONFIG_PATH: ""  # Auto-detected in packaged environment
```

---

## Deployment

### Transfer to Raspberry Pi

```bash
# SCP the .deb package
scp release/kitchntabs-1.0.19-armv7l.deb user@raspberry-pi:/tmp/

# SSH and install
ssh user@raspberry-pi
sudo dpkg -i /tmp/kitchntabs-1.0.19-armv7l.deb
sudo apt-get install -f  # Fix any dependency issues
```

### Systemd Service (Optional)

```ini
[Unit]
Description=KitchenTabs POS Terminal
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/opt/kitchntabs/kitchntabs --no-sandbox
Restart=always
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-29 | Initial multi-architecture build system |

---

## Related Documentation

- [ELECTRON_BUILD_PROCESS.md](./ELECTRON_BUILD_PROCESS.md) - Electron packaging details
- [ELECTRON_PYTHON_SERVICE_BUILD_SYSTEM.md](./ELECTRON_PYTHON_SERVICE_BUILD_SYSTEM.md) - Python service integration
- [Docker Buildx Documentation](https://docs.docker.com/buildx/working-with-buildx/)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
