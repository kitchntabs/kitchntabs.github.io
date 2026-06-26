---
layout: default
title: N5-Desktop-Device-Service RASPBERRY PI SETUP
---

# KitchnTabs on Raspberry Pi - Quick Setup Guide

Fast setup for installing KitchnTabs on Raspberry Pi.

## Prerequisites

- Raspberry Pi 3B+, 4, or 5
- Raspbian/Debian OS (Bullseye or Bookworm)
- Network connectivity
- 2GB+ free storage

## Step 1: Determine Your Architecture

SSH into your Raspberry Pi and check:

```bash
ssh pi@raspberry-pi.local  # or pi@192.168.1.XXX

uname -m
```

**Output meanings:**
- `armv7l` → 32-bit (Pi 3B+/4 with 32-bit OS)
- `aarch64` → 64-bit (Pi 4/5 with 64-bit Bookworm OS)

## Step 2: Build on Development Machine

Choose your architecture and build:

**For 64-bit Raspberry Pi (recommended for Pi 4/5):**
```bash
cd /path/to/kitchntabs-frontend

# Development build (no S3 publishing)
pnpm release:electron:kitchntabs-app:debian:arm64:development

# Creates: release/kitchntabs-1.3.15-arm64.deb
```

**For 32-bit Raspberry Pi (Pi 3B+/4):**
```bash
# Development build
pnpm release:electron:kitchntabs-app:debian:armv7l:development

# Creates: release/kitchntabs-1.3.15-armv7l.deb
```

**For older 32-bit (Buster):**
```bash
USE_BUSTER_BINARIES=true pnpm release:electron:kitchntabs-app:debian:armv7l:development
```

## Step 3: Transfer .deb to Raspberry Pi

**Option A: SCP (easiest)**
```bash
scp release/kitchntabs-1.3.15-arm64.deb pi@raspberry-pi.local:/tmp/
```

**Option B: USB Drive**
```bash
# Copy file to USB
cp release/kitchntabs-1.3.15-arm64.deb /Volumes/USB-NAME/

# On Pi: mount USB
mkdir ~/usb
sudo mount /dev/sda1 ~/usb
cp ~/usb/kitchntabs-1.3.15-arm64.deb /tmp/
```

**Option C: S3 Download** (if published to S3)
```bash
ssh pi@raspberry-pi.local
cd /tmp
wget https://s3.us-east-2.amazonaws.com/kitchntabs-releases/releases/kitchntabs-1.3.15-arm64.deb
```

## Step 4: Install on Raspberry Pi

```bash
# SSH into your Pi
ssh pi@raspberry-pi.local

# Update packages
sudo apt-get update

# Install dependencies
sudo apt-get install -y libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils

# Install KitchnTabs
cd /tmp
sudo dpkg -i kitchntabs-1.3.15-arm64.deb

# Verify
kitchntabs --version
```

## Step 5: Run KitchnTabs

**Quick test:**
```bash
kitchntabs
```

**As a background service:**
```bash
# Create service file
sudo nano /etc/systemd/system/kitchntabs.service
```

Paste this content:
```ini
[Unit]
Description=KitchnTabs POS Terminal
After=network.target

[Service]
Type=simple
User=pi
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

# View logs
sudo journalctl -u kitchntabs -f
```

## Troubleshooting

**Installation fails with dependency errors:**
```bash
sudo apt-get install -f
sudo dpkg -i kitchntabs-1.3.15-arm64.deb
```

**"command not found: kitchntabs":**
```bash
# Use full path
/opt/kitchntabs/kitchntabs

# Or create symlink
sudo ln -s /opt/kitchntabs/kitchntabs /usr/local/bin/kitchntabs
```

**App won't start:**
```bash
# Check dependencies
sudo apt-get install -y libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6

# Try with debug output
DEBUG=* /opt/kitchntabs/kitchntabs
```

**Check install location:**
```bash
dpkg -L kitchntabs | head -20
```

## Uninstall

```bash
# Stop service
sudo systemctl stop kitchntabs
sudo systemctl disable kitchntabs

# Remove
sudo apt-get remove kitchntabs

# Clean up service file
sudo rm /etc/systemd/system/kitchntabs.service
sudo systemctl daemon-reload
```

## Architecture Compatibility

| Model | OS | Arch | Build Command |
|-------|----|----|---|
| Pi 3B+ | Bullseye 32-bit | armv7l | `pnpm release:electron:kitchntabs-app:debian:armv7l:development` |
| Pi 4 | Bullseye 32-bit | armv7l | `pnpm release:electron:kitchntabs-app:debian:armv7l:development` |
| Pi 4 | Bookworm 64-bit | aarch64 | `pnpm release:electron:kitchntabs-app:debian:arm64:development` |
| Pi 5 | Bookworm 64-bit | aarch64 | `pnpm release:electron:kitchntabs-app:debian:arm64:development` |

## File Locations

After installation:
```
/opt/kitchntabs/kitchntabs          # Main executable
/opt/kitchntabs/resources/          # App resources
/opt/kitchntabs/config.yaml         # Configuration
/opt/kitchntabs/resources/python-service/  # Python services
```

## Next Steps

1. Configure the app (edit `/opt/kitchntabs/config.yaml` if needed)
2. Set up as systemd service for auto-start
3. Check logs: `sudo journalctl -u kitchntabs -f`
4. Enable auto-updates from S3 bucket



# Troubleshooting


View Logs
If Running as Systemd Service

# View real-time logs (like tail -f)
sudo journalctl -u kitchntabs -f

# View last 50 lines
sudo journalctl -u kitchntabs -n 50

# View logs from last hour
sudo journalctl -u kitchntabs --since "1 hour ago"

# View with timestamps
sudo journalctl -u kitchntabs -o short-iso

# Search for errors
sudo journalctl -u kitchntabs | grep -i error
If Running Directly in Terminal

# Run with debug output
DEBUG=* /opt/kitchntabs/kitchntabs

# Or
LOG_LEVEL=debug /opt/kitchntabs/kitchntabs

# Both
DEBUG=* LOG_LEVEL=debug /opt/kitchntabs/kitchntabs
Python Service Logs
The Python services (tts_service, kt_service, print_service) may have their own logs:


# Check if services are running
ps aux | grep -E "tts_service|kt_service|print_service"

# Look for Python service output in main logs
sudo journalctl -u kitchntabs -f | grep -i python

# Check service stderr/stdout
ls -la /opt/kitchntabs/resources/python-service/
Application Data & Config Locations

# Installed location
ls -la /opt/kitchntabs/

# App data (user config, cache)
ls -la ~/.config/kitchntabs/
ls -la ~/.cache/kitchntabs/

# Config file
cat /opt/kitchntabs/config.yaml
Enable Full Debug Mode
Create a debug startup script:


sudo nano /usr/local/bin/kitchntabs-debug
Paste this:


#!/bin/bash
export DEBUG=*
export LOG_LEVEL=debug
export NODE_DEBUG=*
/opt/kitchntabs/kitchntabs "$@"
Then:


sudo chmod +x /usr/local/bin/kitchntabs-debug

# Run with full debug
kitchntabs-debug
Troubleshoot TTS Service Specifically

# 1. Check if tts_service binary exists and is executable
ls -lh /opt/kitchntabs/resources/python-service/tts_service
file /opt/kitchntabs/resources/python-service/tts_service

# 2. Try running it directly
/opt/kitchntabs/resources/python-service/tts_service --help

# 3. Check dependencies
ldd /opt/kitchntabs/resources/python-service/tts_service

# 4. Check if it's the right architecture
file /opt/kitchntabs/resources/python-service/tts_service
uname -m  # Compare with binary arch
Create a Log File
Redirect logs to a file for easier inspection:


# Create log directory
mkdir -p ~/kitchntabs-logs

# Run and save logs
DEBUG=* /opt/kitchntabs/kitchntabs > ~/kitchntabs-logs/app.log 2>&1 &

# View logs
tail -f ~/kitchntabs-logs/app.log

# Or search logs
grep -i "tts\|speech\|audio" ~/kitchntabs-logs/app.log
Systemd Service with Logging
If using systemd, modify the service to capture logs:


sudo nano /etc/systemd/system/kitchntabs.service
Update the [Service] section:


[Service]
Type=simple
User=pi
ExecStart=/opt/kitchntabs/kitchntabs
StandardOutput=journal
StandardError=journal
SyslogIdentifier=kitchntabs
Environment="DEBUG=*"
Environment="LOG_LEVEL=debug"
Restart=on-failure
RestartSec=10
Then:


sudo systemctl daemon-reload
sudo systemctl restart kitchntabs
sudo journalctl -u kitchntabs -f
Quick Diagnostic Commands

# Check if app is running
ps aux | grep kitchntabs

# Check CPU/memory usage
top -p $(pgrep kitchntabs)

# Check open files (including audio devices)
lsof -p $(pgrep kitchntabs) | grep -i audio

# Check audio system
aplay -l  # List audio devices
alsamixer  # Audio mixer

# Check system logs for hardware issues
dmesg | tail -20
Common TTS Issues

# 1. Check if audio output works
aplay /usr/share/sounds/freedesktop/stereo/complete.oga

# 2. Check audio device permissions
ls -l /dev/snd/
id pi  # Check user groups

# 3. Add audio group if needed
sudo usermod -aG audio pi

# 4. Check Python runtime
which python3
python3 --version
Save Logs for Analysis

# Save full debug session
DEBUG=* LOG_LEVEL=debug /opt/kitchntabs/kitchntabs 2>&1 | tee ~/debug-session-$(date +%Y%m%d-%H%M%S).log

# Then share the log file
cat ~/debug-session-*.log | tail -200  # Last 200 lines
