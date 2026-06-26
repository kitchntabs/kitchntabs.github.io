
# Building Electron App for Debian AMD64

This guide walks through building and packaging the KitchenTabs Electron application for Debian AMD64 architecture.

- **Windows Users**: Use WSL2 (Ubuntu) to build Linux packages
- **macOS Users**: Build directly on macOS using native tools

## Prerequisites

### macOS

- macOS 11+ (Intel or Apple Silicon)
- Xcode Command Line Tools
- Homebrew package manager
- Node.js v20.19.0+
- npm v9.6.7+

Install Xcode Command Line Tools:
```bash
xcode-select --install
```

Install Homebrew (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install build dependencies:
```bash
brew install ruby@3.0 node@20
# Add Ruby to PATH if needed
echo 'export PATH="/usr/local/opt/ruby@3.0/bin:$PATH"' >> ~/.zshrc
```

### Windows (using WSL2)

- Windows 10/11 with WSL2 enabled
- Ubuntu 20.04+ distribution installed in WSL2
- Node.js v20.19.0+ (in WSL)
- npm v9.6.7+ (in WSL)

---

## macOS Build Instructions

### macOS Step 1: Install Build Tools

```bash
# Install fpm via gem (required for creating .deb packages)
sudo gem install fpm

# Install pnpm
npm install -g pnpm@9.15.0

# Verify installations
fpm --version
pnpm --version
```

### macOS Step 2: Navigate to Project

```bash
cd /path/to/KITCHNTABS/kitchntabs-frontend
```

### macOS Step 3: Build Release for Debian AMD64

```bash
# Production release (without publishing)
pnpm config:electron:kitchntabs-app:production && \
turbo build --filter=kitchntabs-app --no-cache && \
node build-python-service.js && \
electron-icon-builder --input=./assets/logo-squared.png --output=./ && \
vite build -c electron.vite.config.mts && \
cross-env NODE_OPTIONS=--max-old-space-size=8096 node build-electron.js \
  --config electron-builder.config.js \
  --linux deb --x64
```

Or use the npm script:

```bash
# Development build
pnpm release:electron:kitchntabs-app:debian:amd64:development

# Production build (no publishing)
# Modify the script in package.json to remove --publish always, or run manually
```

### macOS Step 4: Locate Output

The `.deb` package will be created at:

```
release/kitchntabs-1.3.15-amd64.deb
```

---

## Windows Build Instructions (WSL2)

### Check WSL Distributions

```powershell
wsl --list --verbose
```

If Ubuntu isn't installed:

```powershell
wsl --install -d Ubuntu
```

## Step 1: Start WSL and Navigate to Project

```powershell
wsl -d Ubuntu
cd /mnt/c/KITCHNTABS/kitchntabs-frontend
```

## Step 2: Install Build Dependencies

The build requires `fpm` (Effecting Package Manager) and other tools to create `.deb` packages on a Linux system.

### Update Package Manager

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Install Required Tools

```bash
# Install build tools and fpm
sudo apt-get install -y \
  build-essential \
  ruby-dev \
  fpm \
  python3 \
  git

# Verify fpm installation
fpm --version
```

### Install pnpm

```bash
sudo npm install -g pnpm@9.15.0
pnpm --version
```

## Step 3: Install Node Dependencies

```bash
# From the project root
pnpm install
```

## Step 4: Build Python Services (if needed)

If building for the first time or after Python service updates, build the services for AMD64:

```bash
# Navigate to Python service directory
cd ../dash-python-service

# Build Docker image for x64
npm run build:docker:x64

# This will create binaries for:
# - kt_service
# - print_service  
# - tts_service

# Return to frontend directory
cd ../kitchntabs-frontend
```

**Note:** This step requires Docker. If Docker isn't available, skip this step and the build will attempt to use existing binaries.

## Step 5: Build Release for Debian AMD64

The build process is split into configuration, vite build, turbo build, and electron-builder packaging.

### Option A: Production Release (with S3 publishing)

```bash
pnpm release:electron:kitchntabs-app:debian:amd64
```

**Requirements:**
- AWS credentials configured with profile `kitchntabs`
- S3 bucket `kitchntabs-releases` accessible in `us-east-2` region

### Option B: Production Release (without publishing)

```bash
# Configure for production
pnpm config:electron:kitchntabs-app:production

# Build turbo dependencies
turbo build --filter=kitchntabs-app --no-cache

# Build Python services setup
node build-python-service.js

# Build icons
electron-icon-builder --input=./assets/logo-squared.png --output=./

# Build with Vite
vite build -c electron.vite.config.mts

# Package with electron-builder (without publishing)
cross-env NODE_OPTIONS=--max-old-space-size=8096 node build-electron.js \
  --config electron-builder.config.js \
  --linux deb --x64
```

### Option C: Development Release

```bash
pnpm release:electron:kitchntabs-app:debian:amd64:development
```

## Step 6: Locate Output

Once the build completes successfully, the `.deb` package will be in:

```
release/kitchntabs-1.3.15-amd64.deb
```

Copy it back to Windows:

```powershell
# From Windows PowerShell
Copy-Item -Path "\\wsl$\Ubuntu\mnt\c\KITCHNTABS\kitchntabs-frontend\release\kitchntabs-*.deb" -Destination "C:\KITCHNTABS\releases\"
```

## Build Process Explanation

### 1. Configuration (`pnpm config:electron:kitchntabs-app:production`)
- Sets `MODE=production`, `CUSTOM_MODE=kitchntabs.production`
- Generates environment-specific configuration files

### 2. Turbo Build (`turbo build --filter=kitchntabs-app`)
- Builds all workspace dependencies
- Compiles TypeScript, bundles CSS, etc.

### 3. Python Services (`node build-python-service.js`)
- Prepares Python service binaries
- Copies architecture-specific binaries to the release directory

### 4. Icon Generation (`electron-icon-builder`)
- Creates platform-specific app icons from source image

### 5. Vite Build (`vite build -c electron.vite.config.mts`)
- Bundles Electron main process
- Bundles Electron preload script
- Creates `dist-electron/` with all bundled code

### 6. Electron Builder (`electron-builder`)
- Packages bundled app into `.deb` format
- Creates Linux desktop entry
- Generates installer metadata
- Creates symlinks for terminal access

## AWS S3 Publishing Setup

The production build scripts can automatically publish .deb packages to an S3 bucket for distribution and auto-updates. This section covers setup and troubleshooting.

### Prerequisites

- AWS Account with S3 access
- S3 bucket created (default: `kitchntabs-releases`)
- IAM user with S3 permissions

### Configuration

#### 1. Create AWS Credentials

1. Log into AWS Console → IAM → Users
2. Create a user or select an existing one (recommended: `KitchnTabsAdmin`)
3. Create an "Access Key" under Security Credentials
4. Save the **Access Key ID** and **Secret Access Key**

#### 2. Configure AWS CLI Profile

```bash
# Create kitchntabs profile with credentials
aws configure --profile kitchntabs

# When prompted:
# AWS Access Key ID: [paste your access key]
# AWS Secret Access Key: [paste your secret key]
# Default region name: us-east-2
# Default output format: json
```

#### 3. Verify S3 Access

```bash
# List the bucket
aws s3 ls s3://kitchntabs-releases --profile kitchntabs

# Test upload (optional)
echo "test" > /tmp/test.txt
aws s3 cp /tmp/test.txt s3://kitchntabs-releases/test.txt --profile kitchntabs
aws s3 rm s3://kitchntabs-releases/test.txt --profile kitchntabs
```

### Building with S3 Publishing

#### Option A: Automatic Publishing (Recommended)

The npm scripts include `--publish always`, which automatically uploads to S3:

```bash
# macOS
pnpm release:electron:kitchntabs-app:debian:amd64

# Windows (WSL)
wsl -d Ubuntu -e bash -c "cd /mnt/c/KITCHNTABS/kitchntabs-frontend && pnpm release:electron:kitchntabs-app:debian:amd64"
```

**Requirements:**
- AWS profile `kitchntabs` configured (see above)
- Network connectivity to S3
- ~5 minutes for build + upload

#### Option B: Build Without Publishing (Troubleshooting)

If S3 uploads fail, build without publishing and upload manually:

```bash
# Build without --publish always
pnpm config:electron:kitchntabs-app:production && \
turbo build --filter=kitchntabs-app --no-cache && \
node build-python-service.js && \
electron-icon-builder --input=./assets/logo-squared.png --output=./ && \
vite build -c electron.vite.config.mts && \
cross-env NODE_OPTIONS=--max-old-space-size=8096 npx electron-builder \
  --config electron-builder.config.js \
  --linux deb --x64
```

The .deb file will be in `release/kitchntabs-1.3.15-amd64.deb`.

#### Manual S3 Upload

After building locally, upload manually:

```bash
aws s3 cp release/kitchntabs-1.3.15-amd64.deb \
  s3://kitchntabs-releases/releases/ \
  --profile kitchntabs \
  --acl private
```

### Build Failure Recovery

**Important:** The build process temporarily hides `pnpm-lock.yaml` and `pnpm-workspace.yaml` to work around pnpm workspace issues. If the build fails, these files must be restored before running the build again.

#### Auto-Restore

```bash
# Restore with npm script
pnpm restore:build-files
```

#### Manual Restore

```bash
cd /path/to/kitchntabs-frontend
mv pnpm-lock.yaml.build-backup pnpm-lock.yaml
mv pnpm-workspace.yaml.build-backup pnpm-workspace.yaml
```

If files don't exist, the build already completed successfully.

## Troubleshooting

### AWS: "InvalidAccessKeyId"

**Error:** `S3 PutObject failed (HTTP 403): InvalidAccessKeyId`

**Solution:**
1. Verify AWS credentials are configured:
   ```bash
   aws configure get aws_access_key_id --profile kitchntabs
   ```
2. Ensure credentials are not expired
3. Check IAM permissions (user needs `s3:PutObject`, `s3:GetObject` on bucket)
4. Try building without publishing (Option B above)

### Build: "No package found with name 'kitchntabs-app'"

**Error:** `turbo: No package found with name 'kitchntabs-app' in workspace`

**Solution:** Restore pnpm files:
```bash
pnpm restore:build-files
```

### Build: "write EPIPE" during S3 upload

**Error:** `write EPIPE` when uploading .deb to S3

**Possible causes:**
- Network timeout during large file upload
- S3 bucket permissions issue
- electron-builder S3 publisher bug

**Solution:**
1. Build without publishing first:
   ```bash
   # Use Option B above (no --publish always)
   ```
2. Upload manually after build succeeds:
   ```bash
   aws s3 cp release/kitchntabs-1.3.15-amd64.deb \
     s3://kitchntabs-releases/releases/ \
     --profile kitchntabs
   ```

### macOS: "fpm: command not found"

**Solution:** Install fpm via gem:
```bash
sudo gem install fpm
# If using Ruby 3.0+:
sudo gem install -n /usr/local/bin fpm
```

### Windows (WSL): "fpm: command not found"

**Solution:** Ensure fpm is installed in WSL:
```bash
sudo apt-get install -y ruby-dev
sudo gem install fpm
```

### Issue: "Python service binaries not found"

**Solution:** Build Python services for x64:
```bash
cd ../dash-python-service
npm run build:docker:x64
cd ../kitchntabs-frontend
```

If Docker isn't available, the build will proceed with a warning but may fail during packaging.

### macOS: "permission denied" when installing fpm

**Solution:** Use sudo or install in user directory:
```bash
# Option 1: Use sudo
sudo gem install fpm

# Option 2: Install in user directory
gem install --user-install fpm
# Then add to PATH:
export PATH="~/.gem/ruby/3.0.0/bin:$PATH"
```

### macOS: "xcrun: error: SDK \"macosx\" cannot be located" (Apple Silicon)

**Solution:** Install Xcode command line tools:
```bash
xcode-select --install
sudo xcode-select --reset
```

### Issue: "Cannot find module './apps/kitchntabs/package.json'"

**Solution:** This is already fixed in the updated `electron-builder.config.js`. Ensure you're using the latest version that references `apps/kitchntabs-app` instead of `apps/kitchntabs`.

### Issue: "ENOENT: spawn fpm ENOENT" on Windows (PowerShell)

**Solution:** This indicates you're trying to build on Windows directly. Use WSL2 instead:
```powershell
wsl -d Ubuntu -e bash -c "cd /mnt/c/KITCHNTABS/kitchntabs-frontend && pnpm release:electron:kitchntabs-app:debian:amd64"
```

### Issue: AWS Credentials Not Found

If using the production command with `--publish always`:
```bash
# Configure AWS credentials in WSL
aws configure --profile kitchntabs
# Or set environment variables:
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-2
```

Or skip publishing:
```bash
cross-env NODE_OPTIONS=--max-old-space-size=8096 node build-electron.js \
  --config electron-builder.config.js \
  --linux deb --x64
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODE` | development | Build mode (development/production) |
| `CUSTOM_MODE` | kitchntabs.development | Configuration mode |
| `TARGET_TYPE` | desktop | Target type (desktop/mobile/web) |
| `PLATFORM` | electron | Platform (electron/web/android/ios) |
| `APP_PATH` | apps/kitchntabs-app | Application directory |
| `NODE_OPTIONS` | --max-old-space-size=8096 | Node memory limit (increase for large builds) |
| `AWS_PROFILE` | kitchntabs | AWS profile for S3 publishing |
| `USE_BUSTER_BINARIES` | false | Use Debian Buster-compatible binaries for older systems |

## Configuration Files

Key configuration files for the build:

- **electron-builder.config.js** — Main Electron build configuration
  - Defines targets (deb, AppImage, etc.)
  - Specifies files to include/exclude
  - Configures Python service integration
  
- **electron.vite.config.mts** — Vite bundling configuration
  - Bundles main process, preload, and renderer
  - Handles dev server vs. production build
  
- **build_config.js** — Generates environment-specific configs
  - Creates `electron-config.yaml` with API endpoints
  - Generates `.env` files for the app
  
- **build-python-service.js** — Manages Python service setup
  - Handles architecture-specific binary selection
  - Sets up Buster compatibility if needed

## Installation on Linux Systems

### AMD64 Systems (x64)

The build process creates `release/kitchntabs-1.3.15-amd64.deb` for standard 64-bit Linux systems.

#### Install

```bash
# Transfer to Linux system (from macOS/Windows)
scp release/kitchntabs-1.3.15-amd64.deb user@linux-host:/tmp/

# Or download from S3
aws s3 cp s3://kitchntabs-releases/releases/kitchntabs-1.3.15-amd64.deb /tmp/

# Install on Linux system
cd /tmp
sudo dpkg -i kitchntabs-1.3.15-amd64.deb

# Verify installation
kitchntabs --version
```

#### Uninstall

```bash
sudo apt-get remove kitchntabs
```

### Raspberry Pi (ARM 32-bit & 64-bit)

KitchnTabs can run on Raspberry Pi 3B+, 4, and 5 with either 32-bit (Bullseye) or 64-bit (Bookworm) OS.

**Supported configurations:**
- Raspberry Pi 3B+ (32-bit: armv7l)
- Raspberry Pi 4 (32-bit: armv7l or 64-bit: arm64)
- Raspberry Pi 5 (64-bit: arm64)

#### Build for Raspberry Pi

Before installing, build the appropriate .deb for your Pi:

**64-bit (Bookworm, Raspberry Pi 4/5):**
```bash
pnpm release:electron:kitchntabs-app:debian:arm64:development
# Creates: release/kitchntabs-1.3.15-arm64.deb
```

**32-bit (Bullseye, Raspberry Pi 3B+/4):**
```bash
pnpm release:electron:kitchntabs-app:debian:armv7l:development
# Creates: release/kitchntabs-1.3.15-armv7l.deb
```

**32-bit with Buster compatibility (older Pi):**
```bash
cross-env USE_BUSTER_BINARIES=true pnpm release:electron:kitchntabs-app:debian:armv7l:development
```

#### Transfer to Raspberry Pi

**Option A: SCP (Recommended)**

```bash
# From development machine (macOS/Windows/Linux)
scp release/kitchntabs-1.3.15-arm64.deb pi@raspberry-pi.local:/tmp/

# Or with IP address
scp release/kitchntabs-1.3.15-arm64.deb pi@192.168.1.100:/tmp/
```

**Option B: USB Flash Drive**

```bash
# 1. Copy .deb to USB on development machine
cp release/kitchntabs-1.3.15-arm64.deb /Volumes/USB-NAME/

# 2. On Raspberry Pi, plug in USB and mount
mkdir ~/usb-mount
sudo mount /dev/sda1 ~/usb-mount

# 3. Copy from USB
cp ~/usb-mount/kitchntabs-1.3.15-arm64.deb /tmp/
```

**Option C: Download from S3**

```bash
# On Raspberry Pi
cd /tmp
wget https://s3.us-east-2.amazonaws.com/kitchntabs-releases/releases/kitchntabs-1.3.15-arm64.deb
# or
curl -O https://s3.us-east-2.amazonaws.com/kitchntabs-releases/releases/kitchntabs-1.3.15-arm64.deb
```

#### Install on Raspberry Pi

```bash
# SSH into Raspberry Pi
ssh pi@raspberry-pi.local

# Update package lists
sudo apt-get update

# Install dependencies (if needed)
sudo apt-get install -y libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils

# Install KitchnTabs
cd /tmp
sudo dpkg -i kitchntabs-1.3.15-arm64.deb

# Verify installation
kitchntabs --version
```

#### Troubleshooting Installation

**"dpkg: dependency problems"**
```bash
# Automatically install missing dependencies
sudo apt-get install -f

# Then try installing again
sudo dpkg -i kitchntabs-1.3.15-arm64.deb
```

**"command not found: kitchntabs"**
```bash
# The app is installed at:
/opt/kitchntabs/kitchntabs --version

# Create symlink if needed
sudo ln -s /opt/kitchntabs/kitchntabs /usr/local/bin/kitchntabs
```

**"Permission denied" when running**
```bash
# Ensure executable permissions
sudo chmod +x /opt/kitchntabs/kitchntabs

# Run with sudo if needed
sudo /opt/kitchntabs/kitchntabs
```

#### Running KitchnTabs on Raspberry Pi

**Command line:**
```bash
kitchntabs

# With debug output
DEBUG=* kitchntabs

# With specific log level
LOG_LEVEL=debug kitchntabs
```

**As a service (systemd):**

Create `/etc/systemd/system/kitchntabs.service`:
```ini
[Unit]
Description=KitchnTabs POS Terminal
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/kitchntabs
ExecStart=/opt/kitchntabs/kitchntabs
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable kitchntabs
sudo systemctl start kitchntabs
sudo systemctl status kitchntabs
```

**Check logs:**
```bash
sudo journalctl -u kitchntabs -f
```

#### Uninstall from Raspberry Pi

```bash
# Stop service (if running as systemd)
sudo systemctl stop kitchntabs
sudo systemctl disable kitchntabs

# Remove package
sudo apt-get remove kitchntabs

# Remove service file (if created)
sudo rm /etc/systemd/system/kitchntabs.service
sudo systemctl daemon-reload
```

## Next Steps

After successful build:

1. **Test the package on your target system** (AMD64, ARM64, or ARM32)
   ```bash
   sudo dpkg -i release/kitchntabs-1.3.15-*.deb
   ```

2. **Verify installation**
   ```bash
   kitchntabs --version
   # or
   /opt/kitchntabs/kitchntabs --version
   ```

3. **Publish to S3** (if credentials configured)
   ```bash
   pnpm release:electron:kitchntabs-app:debian:amd64
   ```

## Performance Tips

- Use `--max-old-space-size=8096` for Node memory (8GB)
- Increase to 16384 for very large projects
- Run on fast SSD for quicker builds
- First build will be slower due to dependency resolution
- Subsequent builds are faster if dependencies haven't changed

## Support

For issues:

1. Check the build output for specific error messages
2. Ensure all prerequisites are installed in WSL
3. Verify `apps/kitchntabs-app/` directory exists and has content
4. Check that Python service binaries exist if needed
5. Review the electron-builder config for file paths

See `electron-builder.config.js` for advanced configuration options.

## Platform Comparison

| Task | macOS | Windows (WSL2) |
|------|-------|----------------|
| **Prerequisites** | Xcode CLT, Homebrew | WSL2, Ubuntu |
| **Install fpm** | `brew install fpm` or `gem install fpm` | `sudo apt-get install ruby-dev` + `sudo gem install fpm` |
| **Install pnpm** | `npm install -g pnpm@9.15.0` | `sudo npm install -g pnpm@9.15.0` |
| **Build command** | Run directly in terminal | Run inside WSL with `wsl -d Ubuntu` or use the npm scripts |
| **Output location** | `release/kitchntabs-*.deb` | `release/kitchntabs-*.deb` |
| **Time to build** | ~5-10 minutes | ~5-10 minutes |

## Running Builds from Windows PowerShell with WSL

If you're on Windows and want to run the build from PowerShell without entering WSL:

```powershell
# Development build
wsl -d Ubuntu -- bash -c "cd /mnt/c/KITCHNTABS/kitchntabs-frontend && pnpm release:electron:kitchntabs-app:debian:amd64:development"

# Production build (without publishing)
wsl -d Ubuntu -- bash -c "cd /mnt/c/KITCHNTABS/kitchntabs-frontend && pnpm config:electron:kitchntabs-app:production && turbo build --filter=kitchntabs-app --no-cache && node build-python-service.js && electron-icon-builder --input=./assets/logo-squared.png --output=./ && vite build -c electron.vite.config.mts && NODE_OPTIONS=--max-old-space-size=8096 node build-electron.js --config electron-builder.config.js --linux deb --x64"
```
