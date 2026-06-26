#!/usr/bin/env python3
"""
KitchnTabs Docs → ClickUp Bulk Upload

Reads DOCS_TO_CLICKUP_MAPPING.md, uploads all 195 markdown files as ClickUp document pages
organized by epic (F1-F20, N1-N10).

Requirements:
    - Python 3.8+
    - requests library
    - ClickUp API token (via environment variable CLICKUP_API_TOKEN)

Usage:
    python upload_docs_to_clickup.py [--dry-run] [--start-epic F1] [--limit 50]

Environment:
    CLICKUP_API_TOKEN: Your ClickUp API token (required)

Rate Limiting:
    - ClickUp API: 30 requests/minute
    - Script batches 25 requests per burst, pauses 60s between bursts
"""

import os
import sys
import time
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import subprocess
import json

# Configuration
DOCUMENT_ID = "2ky5d730-1053"  # KitchnTabs Documentation
SCRIPT_DIR = Path(__file__).resolve().parent
MAPPING_FILE = SCRIPT_DIR / "DOCS_TO_CLICKUP_MAPPING.md"
DOCS_ROOT = SCRIPT_DIR / "docs"
RATE_LIMIT_DELAY = 60  # seconds between bursts
REQUESTS_PER_BURST = 25  # requests per burst (30 req/min limit)
DRY_RUN = "--dry-run" in sys.argv
START_EPIC = None
LIMIT = None

# Parse command-line arguments
for arg in sys.argv[1:]:
    if arg == "--dry-run":
        DRY_RUN = True
    elif arg.startswith("--start-epic="):
        START_EPIC = arg.split("=")[1]
    elif arg.startswith("--limit="):
        LIMIT = int(arg.split("=")[1])

if DRY_RUN:
    print("🔍 DRY RUN MODE — No pages will be created\n")

# Statistics
stats = {
    "total_files": 0,
    "uploaded": 0,
    "skipped": 0,
    "errors": 0,
    "epic_pages": {},
}


def log(message: str, level: str = "INFO"):
    """Log a message with timestamp."""
    timestamp = time.strftime("%H:%M:%S")
    prefix = f"[{timestamp}]"
    if level == "ERROR":
        print(f"❌ {prefix} {message}")
    elif level == "WARN":
        print(f"⚠️  {prefix} {message}")
    elif level == "SUCCESS":
        print(f"✅ {prefix} {message}")
    else:
        print(f"ℹ️  {prefix} {message}")


def parse_mapping_file() -> Dict[str, List[Tuple[str, str]]]:
    """Parse DOCS_TO_CLICKUP_MAPPING.md and extract epic → files mapping."""
    if not MAPPING_FILE.exists():
        log(f"Mapping file not found: {MAPPING_FILE}", "ERROR")
        sys.exit(1)

    mapping = {}
    current_epic = None
    with open(MAPPING_FILE) as f:
        for line in f:
            # Match epic headers: ## F1: Orders & Tabs (N files)
            epic_match = re.match(r"^## (F\d+|N\d+):\s+(.+?)(?:\s*\(|$)", line)
            if epic_match:
                epic_code = epic_match.group(1)
                epic_name = epic_match.group(2)
                current_epic = f"{epic_code}: {epic_name}"
                mapping[current_epic] = []

            # Match file lines: - `path/file.md` — description
            if current_epic and line.startswith("- `"):
                file_match = re.match(r"^-\s+`([^`]+)`\s*—\s*(.+)$", line)
                if file_match:
                    file_path = file_match.group(1)
                    description = file_match.group(2)
                    mapping[current_epic].append((file_path, description))

    return mapping


def read_markdown_file(file_path: str) -> Optional[str]:
    """Read a markdown file from the docs directory."""
    full_path = DOCS_ROOT / file_path
    if not full_path.exists():
        log(f"File not found: {file_path}", "WARN")
        return None

    try:
        with open(full_path, encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        log(f"Error reading {file_path}: {e}", "ERROR")
        return None


def create_clickup_page(
    epic: str, file_path: str, description: str, content: str
) -> bool:
    """Create a ClickUp document page via the MCP API using bash subprocess."""
    if DRY_RUN:
        log(f"[DRY] Would create: {epic} — {description[:50]}...", "INFO")
        return True

    # Page name: "{EPIC}: {DESCRIPTION}"
    page_name = f"{epic.split(': ', 1)[1]} — {description}"

    # Prepare the content with metadata
    full_content = f"{content}\n\n---\n\n**Source:** `{file_path}`  \n**Updated:** {time.strftime('%Y-%m-%d')}"

    # Use bash with gh MCP CLI to call the ClickUp API
    # This assumes you have ClickUp MCP set up and authenticated
    try:
        # Build the command to call ClickUp's create_document_page
        # We'll use a direct approach with the API
        cmd = [
            "bash",
            "-c",
            f"""
echo 'Creating ClickUp page...'
# Using native ClickUp API via curl (requires CLICKUP_API_TOKEN)
""",
        ]

        # Instead, let's use Python requests to call the API directly
        import requests

        api_token = os.getenv("CLICKUP_API_TOKEN")
        if not api_token:
            log(
                "CLICKUP_API_TOKEN environment variable not set. Cannot upload without authentication.",
                "ERROR",
            )
            return False

        headers = {
            "Authorization": api_token,
            "Content-Type": "application/json",
        }

        # Create document page
        url = f"https://api.clickup.com/api/v2/doc/{DOCUMENT_ID}/page"
        payload = {
            "name": page_name,
            "content": full_content,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code in [200, 201]:
            log(f"Created: {page_name[:60]}...", "SUCCESS")
            return True
        else:
            log(
                f"Failed to create page ({response.status_code}): {response.text[:100]}",
                "ERROR",
            )
            return False

    except ImportError:
        log("requests library not installed. Install with: pip install requests", "ERROR")
        return False
    except Exception as e:
        log(f"Error creating page: {e}", "ERROR")
        return False


def upload_all_docs():
    """Main upload process."""
    log("Parsing mapping file...", "INFO")
    mapping = parse_mapping_file()

    total_files = sum(len(files) for files in mapping.values())
    log(f"Found {len(mapping)} epics with {total_files} files total", "INFO")

    if LIMIT:
        log(f"Limiting to {LIMIT} files", "INFO")

    # Filter epics if --start-epic specified
    epics_to_process = list(mapping.keys())
    if START_EPIC:
        try:
            start_idx = next(
                i for i, e in enumerate(epics_to_process) if e.startswith(START_EPIC)
            )
            epics_to_process = epics_to_process[start_idx:]
            log(f"Starting from epic: {START_EPIC}", "INFO")
        except StopIteration:
            log(f"Epic not found: {START_EPIC}", "ERROR")
            return

    print("\n" + "=" * 80)
    print(f"{'EPIC':<30} | {'FILES':<6} | {'STATUS':<40}")
    print("=" * 80)

    files_uploaded = 0
    files_processed = 0

    for epic_idx, epic in enumerate(epics_to_process):
        files = mapping[epic]
        stats["epic_pages"][epic] = {"total": len(files), "uploaded": 0, "errors": 0}

        for file_idx, (file_path, description) in enumerate(files):
            if LIMIT and files_processed >= LIMIT:
                log(f"Reached limit of {LIMIT} files", "WARN")
                break

            files_processed += 1
            stats["total_files"] += 1

            # Read file content
            content = read_markdown_file(file_path)
            if not content:
                stats["skipped"] += 1
                stats["epic_pages"][epic]["errors"] += 1
                print(f"{epic:<30} | {file_idx + 1:<6} | ❌ File not found: {file_path}")
                continue

            # Create ClickUp page
            if create_clickup_page(epic, file_path, description, content):
                files_uploaded += 1
                stats["uploaded"] += 1
                stats["epic_pages"][epic]["uploaded"] += 1
                status = "✅ Created"
            else:
                stats["errors"] += 1
                stats["epic_pages"][epic]["errors"] += 1
                status = "❌ Failed"

            print(f"{epic:<30} | {file_idx + 1:<6} | {status}")

            # Rate limiting: throttle after REQUESTS_PER_BURST
            if files_processed % REQUESTS_PER_BURST == 0:
                log(
                    f"Rate limit pause: {RATE_LIMIT_DELAY}s ({files_processed}/{total_files} files)",
                    "INFO",
                )
                time.sleep(RATE_LIMIT_DELAY)

        if LIMIT and files_processed >= LIMIT:
            break

    print("=" * 80)
    print(f"\n📊 Upload Complete\n")
    print(f"  Total files processed: {files_processed}")
    print(f"  Successfully uploaded: {files_uploaded}")
    print(f"  Skipped/Errors: {stats['total_files'] - files_uploaded}")
    print()

    # Per-epic summary
    print("📈 By Epic:")
    for epic in epics_to_process:
        if epic in stats["epic_pages"]:
            ep_stats = stats["epic_pages"][epic]
            print(
                f"  {epic:<40} {ep_stats['uploaded']:>3}/{ep_stats['total']:>3} uploaded"
            )

    if DRY_RUN:
        print("\n🔍 DRY RUN COMPLETE — No pages were actually created")
    else:
        print(f"\n✅ All done! Visit: https://app.clickup.com/90132880480/docs/{DOCUMENT_ID}")


def main():
    """Entry point."""
    print("\n🚀 KitchnTabs Docs → ClickUp Bulk Upload\n")

    # Check for required environment
    api_token = os.getenv("CLICKUP_API_TOKEN")
    if not api_token and not DRY_RUN:
        log("CLICKUP_API_TOKEN not set", "ERROR")
        print("\nSet your API token:")
        print("  export CLICKUP_API_TOKEN='your_token_here'")
        print("  python upload_docs_to_clickup.py\n")
        sys.exit(1)

    try:
        upload_all_docs()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
