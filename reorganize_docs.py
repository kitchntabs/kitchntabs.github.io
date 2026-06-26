#!/usr/bin/env python3
"""
Reorganize docs folder to match ClickUp epic structure

Reads DOCS_TO_CLICKUP_MAPPING.md and moves files into epic-based folders.
Creates backups before reorganizing.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

DOCS_DIR = Path("/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/docs")
MAPPING_FILE = Path("/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/DOCS_TO_CLICKUP_MAPPING.md")
BACKUP_DIR = DOCS_DIR.parent / f"docs_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Track moves
stats = {
    "backed_up": 0,
    "created_folders": 0,
    "moved_files": 0,
    "errors": [],
}


def log(message, level="INFO"):
    """Log with formatting."""
    if level == "ERROR":
        print(f"❌ {message}")
    elif level == "SUCCESS":
        print(f"✅ {message}")
    elif level == "WARN":
        print(f"⚠️  {message}")
    else:
        print(f"ℹ️  {message}")


def sanitize_epic_name(name: str) -> str:
    """Convert epic name to folder name."""
    # Remove special characters, replace spaces with hyphens
    return re.sub(r"[^\w\s-]", "", name).replace(" ", "-")


def parse_mapping() -> dict:
    """Parse DOCS_TO_CLICKUP_MAPPING.md and extract epic → files mapping."""
    if not MAPPING_FILE.exists():
        log(f"Mapping file not found: {MAPPING_FILE}", "ERROR")
        return {}

    mapping = {}
    current_epic = None

    with open(MAPPING_FILE) as f:
        for line in f:
            # Match epic headers: ## F1: Orders & Tabs (N files)
            epic_match = re.match(r"^## (F\d+|N\d+):\s+(.+?)(?:\s*\(|$)", line)
            if epic_match:
                epic_code = epic_match.group(1)
                epic_name = epic_match.group(2).strip()
                current_epic = f"{epic_code}: {epic_name}"
                mapping[current_epic] = []

            # Match file lines: - `path/file.md` — description
            if current_epic and line.startswith("- `"):
                file_match = re.match(r"^-\s+`([^`]+)`\s*—\s*(.+)$", line)
                if file_match:
                    file_path = file_match.group(1)
                    description = file_match.group(2).strip()
                    mapping[current_epic].append((file_path, description))

    return mapping


def file_exists_in_docs(file_path: str) -> Path:
    """Find a file in the docs directory (with or without docs/ prefix)."""
    # Handle different path formats
    if file_path.startswith("docs/"):
        file_path = file_path[5:]  # Remove docs/ prefix

    full_path = DOCS_DIR / file_path
    if full_path.exists():
        return full_path

    # Try alternate locations
    for alt_path in [
        DOCS_DIR / file_path,
        DOCS_DIR.parent / "docs" / file_path,
    ]:
        if alt_path.exists():
            return alt_path

    return None


def reorganize():
    """Main reorganization process."""
    print("\n🚀 Reorganizing docs to match ClickUp epic structure\n")

    # Step 1: Backup
    print("📦 Creating backup...")
    if DOCS_DIR.exists():
        shutil.copytree(DOCS_DIR, BACKUP_DIR)
        stats["backed_up"] = sum(1 for _ in BACKUP_DIR.rglob("*"))
        log(f"Backed up to: {BACKUP_DIR}", "SUCCESS")
    print()

    # Step 2: Parse mapping
    print("📖 Parsing mapping file...")
    mapping = parse_mapping()
    if not mapping:
        log("No mapping found", "ERROR")
        return
    log(f"Found {len(mapping)} epics", "SUCCESS")
    print()

    # Step 3: Create epic folders
    print("📁 Creating epic folders...")
    for epic in mapping.keys():
        epic_code = epic.split(":")[0]
        epic_name = epic.split(": ", 1)[1]
        folder_name = f"{epic_code}-{sanitize_epic_name(epic_name)}"
        folder_path = DOCS_DIR / folder_name

        folder_path.mkdir(parents=True, exist_ok=True)
        stats["created_folders"] += 1
        print(f"  ✓ {folder_name}/")

    # Create utility folders
    for util_folder in ["General-Utilities", "Archive"]:
        (DOCS_DIR / util_folder).mkdir(parents=True, exist_ok=True)
        stats["created_folders"] += 1
    print()

    # Step 4: Move files
    print("📋 Moving files to epic folders...")
    print()

    files_in_mapping = set()
    for epic, files in mapping.items():
        epic_code = epic.split(":")[0]
        epic_name = epic.split(": ", 1)[1]
        folder_name = f"{epic_code}-{sanitize_epic_name(epic_name)}"
        dest_folder = DOCS_DIR / folder_name

        for file_path, description in files:
            # Find the file
            full_path = file_exists_in_docs(file_path)
            if not full_path:
                stats["errors"].append(f"File not found: {file_path}")
                continue

            # Skip if already in correct destination
            if full_path.parent == dest_folder:
                continue

            files_in_mapping.add(full_path)

            # Move the file
            try:
                new_path = dest_folder / full_path.name
                if not new_path.exists():
                    shutil.move(str(full_path), str(new_path))
                    print(f"  ✓ {full_path.name:50} → {folder_name}/")
                    stats["moved_files"] += 1
            except Exception as e:
                stats["errors"].append(f"Error moving {file_path}: {e}")

    print()

    # Step 5: Move remaining files to General-Utilities or Archive
    print("📚 Organizing remaining files...")
    general_util_folder = DOCS_DIR / "General-Utilities"
    archive_folder = DOCS_DIR / "Archive"

    # Find all .md files not yet moved
    for md_file in DOCS_DIR.rglob("*.md"):
        if md_file.parent.name.startswith(("F", "N", "General", "Archive")):
            # Already in an epic or utility folder
            continue

        # Move to appropriate folder
        if md_file.parent.name == "archive" or any(
            x in md_file.name.lower() for x in ["archive", "deprecated", "old"]
        ):
            new_path = archive_folder / md_file.name
        else:
            new_path = general_util_folder / md_file.name

        if not new_path.exists():
            try:
                shutil.move(str(md_file), str(new_path))
                print(f"  ✓ {md_file.name:50} → {new_path.parent.name}/")
                stats["moved_files"] += 1
            except Exception as e:
                stats["errors"].append(f"Error moving {md_file}: {e}")

    print()

    # Step 6: Clean up empty directories
    print("🧹 Cleaning up empty directories...")
    removed_dirs = 0
    for directory in DOCS_DIR.rglob("*"):
        if directory.is_dir() and not any(directory.iterdir()):
            try:
                directory.rmdir()
                removed_dirs += 1
            except Exception:
                pass

    if removed_dirs > 0:
        print(f"  ✓ Removed {removed_dirs} empty directories")
    print()

    # Step 7: Summary
    print("=" * 80)
    print("📊 Reorganization Summary")
    print("=" * 80)
    print()
    print(f"Backup location: {BACKUP_DIR}")
    print(f"Files backed up: {stats['backed_up']}")
    print(f"Epic folders created: {stats['created_folders']}")
    print(f"Files moved: {stats['moved_files']}")
    print()

    # Show new structure
    print("📂 New folder structure:")
    print()
    for folder in sorted(DOCS_DIR.iterdir()):
        if folder.is_dir() and not folder.name.startswith("."):
            file_count = len(list(folder.glob("*.md")))
            subdir_count = len(list(folder.glob("*/")))
            print(f"  {folder.name:40} ({file_count} files, {subdir_count} subfolders)")

    print()

    # Show errors
    if stats["errors"]:
        print("⚠️  Issues encountered:")
        for error in stats["errors"][:10]:  # Show first 10
            print(f"  • {error}")
        if len(stats["errors"]) > 10:
            print(f"  ... and {len(stats['errors']) - 10} more")
        print()

    print("=" * 80)
    print("✅ Reorganization complete!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review the new structure")
    print("2. Move feature docs from General-Utilities to appropriate epic folders")
    print(f"3. If satisfied, delete backup: rm -rf {BACKUP_DIR}")
    print()


if __name__ == "__main__":
    try:
        reorganize()
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelled by user")
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        raise
