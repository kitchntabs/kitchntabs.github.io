# Python Service Testing Guide

This document describes how to test the KitchenTabs Python services on different platforms.

## Overview

KitchenTabs includes three Python services built with PyInstaller:

| Service | Description | Size by Platform |
|---------|-------------|------------------|
| `kt_service` | Main WebSocket service for orders and events | macOS: 90MB, Linux x64: 118MB, ARM64: 109MB, ARMv7l: 22MB |
| `print_service` | Thermal printing service (ESC/POS) | macOS: 27MB, Linux x64: 29MB, ARM64: 25MB, ARMv7l: 18MB |
| `tts_service` | Text-to-Speech service | macOS: 11MB, Linux x64: 7.3MB, ARM64: 7.1MB, ARMv7l: 6.4MB |

## Platform Support

| Platform | Architecture | GLIBC Required | Status |
|----------|--------------|----------------|--------|
| Raspberry Pi OS (Buster) | armv7l (32-bit) | 2.28 | ❌ **Not Supported** - upgrade to Bullseye |
| Raspberry Pi OS (Buster) | arm64 (64-bit) | 2.28 | ❌ **Not Supported** - upgrade to Bullseye |
| Raspberry Pi OS (Bullseye+) | armv7l/arm64 | 2.31+ | ✅ Supported |
| Raspberry Pi OS (Bookworm) | armv7l/arm64 | 2.36+ | ✅ Supported |
| macOS | arm64 (Apple Silicon) | N/A | ✅ Supported |
| macOS | x64 (Intel) | N/A | ✅ Supported |
| Windows | x64 | N/A | ✅ Supported |
| Linux (Ubuntu 22.04+) | x64 | 2.31+ | ✅ Supported |

### ⚠️ Important: GLIBC Compatibility

The Python services are built using Docker with `python:3.9-slim-bullseye` base image, which requires **GLIBC 2.31** or higher.

**Raspberry Pi OS Requirements:**
- **Minimum:** Raspberry Pi OS Bullseye (Debian 11)
- **Recommended:** Raspberry Pi OS Bookworm (Debian 12)

If your Raspberry Pi is running **Buster** (Debian 10), you MUST upgrade your OS before the services will run.

### Upgrading Raspberry Pi OS

**Option 1: Fresh Install (Recommended)**
1. Download Raspberry Pi OS Bullseye or Bookworm from https://www.raspberrypi.com/software/
2. Flash to SD card using Raspberry Pi Imager
3. Boot and configure

**Option 2: In-place Upgrade (Advanced)**
```bash
# Backup your data first!
sudo apt update && sudo apt full-upgrade -y

# Edit sources to point to bullseye
sudo sed -i 's/buster/bullseye/g' /etc/apt/sources.list
sudo sed -i 's/buster/bullseye/g' /etc/apt/sources.list.d/raspi.list

# Upgrade
sudo apt update
sudo apt full-upgrade -y

# Reboot
sudo reboot

# Verify
cat /etc/os-release | grep VERSION
ldd --version | head -1
```

## Building for Linux (Cross-Compilation)

Use Docker to cross-compile for Linux architectures from macOS or Linux.

### Prerequisites

1. Docker Desktop installed and running
2. QEMU support enabled (automatic in Docker Desktop)

### Build Commands

```bash
# Navigate to dash-python-service
cd /path/to/dash-python-service

# Build for all Linux architectures
./build-docker.sh --all

# Build for specific architecture
./build-docker.sh --arch=x64      # Linux x64 (Ubuntu, Debian)
./build-docker.sh --arch=arm64    # Raspberry Pi 4 (64-bit)
./build-docker.sh --arch=armv7l   # Raspberry Pi 3/4 (32-bit)

# Build with specific config
./build-docker.sh --all --config=ngrok   # Development config
./build-docker.sh --all --config=prod    # Production config

# Clean up Docker images after build
./build-docker.sh --all --clean
```

### Build Output

```
kt_service_builds/
├── x64/
│   ├── kt_service      (118 MB) - ELF 64-bit LSB executable, x86-64
│   ├── print_service   (29 MB)
│   ├── tts_service     (7.3 MB)
│   └── config.yaml
├── arm64/
│   ├── kt_service      (109 MB) - ELF 64-bit LSB executable, ARM aarch64
│   ├── print_service   (25 MB)
│   ├── tts_service     (7.1 MB)
│   └── config.yaml
└── armv7l/
    ├── kt_service      (22 MB)  - ELF 32-bit LSB executable, ARM, EABI5
    ├── print_service   (18 MB)
    ├── tts_service     (6.4 MB)
    └── config.yaml
```

### Docker Build Notes

- ARM builds use QEMU emulation and take longer (~15-30 minutes each)
- x64 builds are native on Intel/AMD hosts (~5-10 minutes)
- All builds use `python:3.9-slim-bullseye` base image (GLIBC 2.31)
- Build artifacts are automatically extracted to `kt_service_builds/`

## Testing on Raspberry Pi

### Prerequisites

1. Raspberry Pi with Raspberry Pi OS installed
2. SSH access configured
3. The `.deb` package transferred to the device

### Installation

```bash
# Transfer the .deb package
scp release/kitchntabs-<version>-armv7l.deb root@<raspberry-ip>:/opt/

# SSH into the Raspberry Pi
ssh root@<raspberry-ip>

# Install the package
dpkg -i /opt/kitchntabs-<version>-armv7l.deb
```

### Verify Installation

```bash
# Check the symlink was created
which kitchntabs
# Expected: /usr/bin/kitchntabs

ls -la /usr/bin/kitchntabs
# Expected: lrwxrwxrwx ... /usr/bin/kitchntabs -> /opt/kitchntabs/kitchntabs

# Check installed files
ls -la /opt/kitchntabs/
ls -la /opt/kitchntabs/resources/python-service/
```

### Verify Binary Architecture

```bash
# Check that binaries are correct ARM format
file /opt/kitchntabs/resources/python-service/*

# Expected output for armv7l:
# kt_service:    ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV)
# print_service: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV)
# tts_service:   ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV)

# Expected output for arm64:
# kt_service:    ELF 64-bit LSB executable, ARM aarch64
# print_service: ELF 64-bit LSB executable, ARM aarch64
# tts_service:   ELF 64-bit LSB executable, ARM aarch64
```

### Check GLIBC Compatibility

```bash
# Check system GLIBC version
ldd --version | head -1
# For Buster: ldd (Debian GLIBC 2.28-10+rpi1) 2.28
# For Bullseye: ldd (Debian GLIBC 2.31-...) 2.31

# Check OS version
cat /etc/os-release | grep -E 'PRETTY|VERSION'
```

### Test Individual Services

#### 1. Test kt_service (WebSocket Service)

```bash
# Navigate to service directory
cd /opt/kitchntabs/resources/python-service

# Test execution (should show help or start briefly)
./kt_service --help

# Or run in foreground to see startup logs
./kt_service

# Expected: Service starts and connects to WebSocket server
# Press Ctrl+C to stop
```

#### 2. Test print_service (Printing Service)

```bash
cd /opt/kitchntabs/resources/python-service

# Test execution
./print_service --help

# Or run in foreground
./print_service

# Note: Requires a USB thermal printer connected
# The service will start and wait for print jobs via HTTP
```

#### 3. Test tts_service (Text-to-Speech Service)

```bash
cd /opt/kitchntabs/resources/python-service

# Test execution
./tts_service --help

# Or run in foreground
./tts_service

# Note: Requires audio output configured
# The service will start and wait for TTS requests via HTTP
```

### Test Full Application

```bash
# Run the full Electron application
kitchntabs

# Or with display environment (if running headless)
DISPLAY=:0 kitchntabs

# Check logs for service startup
# Look for messages like:
# - "Python service started"
# - "WebSocket connected"
# - "Print service ready"
```

### Common Issues

#### GLIBC Version Mismatch

**Error:**
```
./kt_service: /lib/arm-linux-gnueabihf/libc.so.6: version `GLIBC_2.33' not found
./kt_service: /lib/arm-linux-gnueabihf/libc.so.6: version `GLIBC_2.34' not found
```

**Cause:**
Your Raspberry Pi is running Raspbian/Raspberry Pi OS **Buster** (Debian 10) which has GLIBC 2.28.
The services require GLIBC 2.31+ (Bullseye or newer).

**Solution:**
Upgrade your Raspberry Pi OS to Bullseye or Bookworm. See the "Upgrading Raspberry Pi OS" section above.

> **Note:** Building with Buster base images is no longer possible because Debian Buster reached End-of-Life (EOL) in June 2024 and the package repositories are no longer available.

#### Missing Libraries

**Error:**
```
./kt_service: error while loading shared libraries: libXXX.so: cannot open shared object file
```

**Solution:**
Install missing system libraries:
```bash
apt-get update
apt-get install -y libusb-1.0-0 libasound2 libsndfile1 portaudio19-dev
```

## Testing on macOS

### Prerequisites

1. macOS 12+ (Monterey or later)
2. Node.js 20+ installed
3. Python 3.9+ installed (via Homebrew or pyenv)
4. Virtual environment with dependencies installed

### Setup Virtual Environment

```bash
# Navigate to dash-python-service
cd /path/to/dash-python-service

# Create virtual environment (if not exists)
python3.9 -m venv pw_env

# Activate virtual environment
source pw_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### Build Services

```bash
# Build all services with production config
npm run build:prod

# Or build with ngrok config for development
npm run build:ngrok

# Or build individual services
npm run build:kt      # kt_service only
npm run build:print   # print_service only
npm run build:tts     # tts_service only
```

### Test Native Services

```bash
# Test kt_service (WebSocket service)
./kt_service/kt_service --help
./kt_service/kt_service  # Starts service, Ctrl+C to stop

# Test print_service (requires USB thermal printer)
./kt_service/print_service --help
./kt_service/print_service

# Test tts_service (requires audio output)
./kt_service/tts_service --help
./kt_service/tts_service
```

### Build and Test Electron App

```bash
# Navigate to dash-frontend
cd /path/to/dash-frontend

# Build for macOS (production)
npm run release:electron:kitchntabs:production

# The .dmg will be in release/ directory
# Output: kitchntabs-<version>-mac-arm64.dmg (Apple Silicon)
#     or: kitchntabs-<version>-mac-x64.dmg (Intel)

# Open and test the application
open release/kitchntabs-*.dmg
```

### Verify Binary Architecture (macOS)

```bash
# Check binary type
file kt_service/kt_service
# Expected: Mach-O 64-bit executable arm64 (for Apple Silicon)
# Or: Mach-O 64-bit executable x86_64 (for Intel)

# Check for universal binary
lipo -info kt_service/kt_service
```

### Expected Output (macOS arm64)

```
kt_service/
├── kt_service      (90 MB)  - Mach-O 64-bit executable arm64
├── print_service   (27 MB)  - Mach-O 64-bit executable arm64
└── tts_service     (11 MB)  - Mach-O 64-bit executable arm64
```

## Testing on Windows

### Prerequisites

1. Windows 10/11 64-bit
2. Node.js 20+ installed
3. Python 3.9+ installed
4. Virtual environment with dependencies installed

### Setup Virtual Environment

```powershell
# Navigate to dash-python-service
cd \path\to\dash-python-service

# Create virtual environment
python -m venv pw_env

# Activate virtual environment
.\pw_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### Build Services

**Option 1: Using Node.js script (recommended)**
```powershell
# Build all services with production config
npm run build:prod

# Or build with ngrok config for development
npm run build:ngrok

# Or build a specific service
npm run build:kt
npm run build:print
npm run build:tts
```

**Option 2: Using batch script**
```batch
# Build with default config (config.kitchntabs.prod.yaml)
build.win.bat

# Build with custom config
build.win.bat config.kitchntabs.ngrok.yaml
```

### Test Services

```powershell
# Test kt_service
.\kt_service\kt_service.exe --help
.\kt_service\kt_service.exe

# Test print_service (requires USB thermal printer)
.\kt_service\print_service.exe --help
.\kt_service\print_service.exe

# Test tts_service (requires audio output)
.\kt_service\tts_service.exe --help
.\kt_service\tts_service.exe
```

### Build Electron App

```powershell
# Navigate to dash-frontend
cd \path\to\dash-frontend

# Build for Windows
npm run release:electron:kitchntabs:production

# Installer will be in release/ directory
# Output: kitchntabs-<version>-win-x64.exe
```

### Expected Output

```
kt_service\
├── kt_service.exe      (~90-120 MB)
├── print_service.exe   (~25-30 MB)
└── tts_service.exe     (~7-11 MB)
```

## Service Configuration

All services read configuration from `config.yaml` (bundled inside the executable) or can be overridden with environment variables.

### Key Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHON_SERVICE_PORT` | HTTP port for print/tts services | 5001 |
| `WS_HOST` | WebSocket server host | (from config) |
| `WS_PORT` | WebSocket server port | (from config) |
| `PRINTER_TYPE` | Printer connection type | usb |
| `PRINTER_VENDOR_ID` | USB vendor ID for printer | (auto-detect) |
| `PRINTER_PRODUCT_ID` | USB product ID for printer | (auto-detect) |

### Config File Location

- **Packaged App**: Inside `resources/config.prod.yaml`
- **Development**: `apps/dash/config.prod.yaml`
- **Python Service**: Bundled in executable

## Automated Testing Script

Create a test script for Raspberry Pi:

```bash
#!/bin/bash
# test-services.sh - Test all KitchenTabs services

set -e

SERVICE_DIR="/opt/kitchntabs/resources/python-service"

echo "=== KitchenTabs Service Testing ==="
echo ""

# Check installation
echo "1. Checking installation..."
if [ -f "$SERVICE_DIR/kt_service" ]; then
    echo "   ✅ kt_service found"
else
    echo "   ❌ kt_service NOT found"
    exit 1
fi

if [ -f "$SERVICE_DIR/print_service" ]; then
    echo "   ✅ print_service found"
else
    echo "   ❌ print_service NOT found"
fi

if [ -f "$SERVICE_DIR/tts_service" ]; then
    echo "   ✅ tts_service found"
else
    echo "   ❌ tts_service NOT found"
fi

# Check binary architecture
echo ""
echo "2. Checking binary architecture..."
file "$SERVICE_DIR/kt_service" | grep -q "ARM" && echo "   ✅ ARM binary" || echo "   ❌ Not ARM binary"

# Check GLIBC compatibility
echo ""
echo "3. Checking GLIBC compatibility..."
GLIBC_VERSION=$(ldd --version | head -1 | grep -oE '[0-9]+\.[0-9]+$')
echo "   System GLIBC: $GLIBC_VERSION"

# Try to run services
echo ""
echo "4. Testing service execution..."

# Test kt_service (timeout after 5 seconds)
echo "   Testing kt_service..."
timeout 5s "$SERVICE_DIR/kt_service" 2>&1 | head -5 || true
echo "   ✅ kt_service executed"

# Test print_service
echo "   Testing print_service..."
timeout 5s "$SERVICE_DIR/print_service" 2>&1 | head -5 || true
echo "   ✅ print_service executed"

# Test tts_service
echo "   Testing tts_service..."
timeout 5s "$SERVICE_DIR/tts_service" 2>&1 | head -5 || true
echo "   ✅ tts_service executed"

echo ""
echo "=== Testing Complete ==="
```

Save this script and run it:

```bash
chmod +x test-services.sh
./test-services.sh
```

## Uninstalling

### Raspberry Pi

```bash
# Remove the package
dpkg -r dash-frontend

# Or completely purge (removes config files too)
dpkg --purge dash-frontend

# Verify removal
which kitchntabs  # Should not exist
ls /opt/kitchntabs  # Should not exist
```

### macOS

```bash
# Move to trash
mv /Applications/kitchntabs.app ~/.Trash/
```

### Windows

```powershell
# Use the uninstaller in Control Panel
# Or run the uninstaller directly
.\release\kitchntabs-uninstaller.exe
```
