#!/usr/bin/env python3
"""
Normalize docs folder and file names:
1. Replace all double dashes (--) with single dashes (-)
2. Prepend epic folder name as prefix to all files
"""

import os
import re
from pathlib import Path
from datetime import datetime

DOCS_DIR = Path("/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/docs")
BACKUP_DIR = DOCS_DIR.parent / f"docs_backup_normalized_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

stats = {
    "folders_renamed": 0,
    "files_renamed": 0,
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


def normalize_name(name: str) -> str:
    """Convert double dashes to single dashes."""
    return name.replace("--", "-")


def get_epic_prefix(folder_name: str) -> str:
    """Extract epic code and name from folder name, return prefix."""
    # Examples: F1-Orders-Tabs, N3-Infrastructure-CICD, F12-Billing-Subscriptions-Payments
    # Extract the epic code (F1, N3, F12, etc.)
    match = re.match(r"^([FN]\d+)-(.+)$", folder_name)
    if match:
        epic_code = match.group(1)
        epic_name = match.group(2)
        return f"{epic_code}-{epic_name}"
    return folder_name


def rename_folders():
    """Rename all folders, converting -- to -."""
    print("📁 Renaming folders (-- to -)...\n")

    for folder in DOCS_DIR.iterdir():
        if not folder.is_dir() or folder.name.startswith("."):
            continue

        normalized_name = normalize_name(folder.name)

        if normalized_name != folder.name:
            new_path = folder.parent / normalized_name
            try:
                folder.rename(new_path)
                print(f"  ✓ {folder.name:45} → {normalized_name}")
                stats["folders_renamed"] += 1
            except Exception as e:
                stats["errors"].append(f"Error renaming folder {folder.name}: {e}")
                log(f"Error renaming {folder.name}: {e}", "ERROR")

    print()


def rename_files_in_epic(epic_folder: Path, epic_prefix: str):
    """Rename all files in an epic folder with the epic prefix."""
    for file_path in epic_folder.glob("*.md"):
        if file_path.is_file():
            # Build new filename: PREFIX_ORIGINALNAME.md
            original_name = file_path.stem
            new_name = f"{epic_prefix}_{original_name}.md"

            # Also normalize the filename itself
            new_name = normalize_name(new_name)

            new_path = file_path.parent / new_name

            if new_path != file_path:
                try:
                    file_path.rename(new_path)
                    print(f"    ✓ {file_path.name:60} → {new_name}")
                    stats["files_renamed"] += 1
                except Exception as e:
                    stats["errors"].append(f"Error renaming file {file_path.name}: {e}")
                    log(f"Error renaming {file_path.name}: {e}", "ERROR")


def process_all_files():
    """Process all epic folders and rename files."""
    print("📄 Renaming files (adding epic prefix)...\n")

    # Process epic folders
    for folder in sorted(DOCS_DIR.iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue

        # Skip utility folders
        if folder.name in ["General-Utilities", "archive"]:
            print(f"→ {folder.name}/ (skipped - utility folder)")
            continue

        # Get epic prefix
        epic_prefix = get_epic_prefix(folder.name)

        if epic_prefix == folder.name:
            # Not an epic folder, skip
            continue

        print(f"→ {folder.name}/")
        rename_files_in_epic(folder, epic_prefix)

    print()

    # Process General-Utilities separately
    general_folder = DOCS_DIR / "General-Utilities"
    if general_folder.exists():
        print(f"→ General-Utilities/ (prefixing as GEN)")
        rename_files_in_epic(general_folder, "GEN")

    # Process archive separately
    archive_folder = DOCS_DIR / "archive"
    if archive_folder.exists():
        print(f"→ archive/ (prefixing as ARCH)")
        rename_files_in_epic(archive_folder, "ARCH")

    print()


def update_mapping_file():
    """Update DOCS_TO_CLICKUP_MAPPING.md to reflect new file names."""
    mapping_file = DOCS_DIR.parent / "DOCS_TO_CLICKUP_MAPPING.md"

    if not mapping_file.exists():
        return

    print("📋 Updating DOCS_TO_CLICKUP_MAPPING.md...")

    with open(mapping_file, "r") as f:
        content = f.read()

    # Replace double dashes with single dashes in paths
    # This handles folder names in paths
    original_content = content

    # Update folder references in paths
    for old_folder_name in [
        "Orders--Tabs",
        "Products--Catalog",
        "Import--Export",
        "Food-Court",
        "Self-Service",
        "Staff-App",
        "Admin-Application",
        "Multi-Tenancy",
        "Access-Control",
        "Messaging",
        "Agents",
        "Subscriptions--Payments",
        "Tenancy",
    ]:
        new_folder_name = old_folder_name.replace("--", "-")
        if old_folder_name != new_folder_name:
            content = content.replace(old_folder_name, new_folder_name)

    if content != original_content:
        with open(mapping_file, "w") as f:
            f.write(content)
        log("Mapping file updated", "SUCCESS")
    else:
        log("Mapping file already normalized", "INFO")

    print()


def main():
    """Main process."""
    print("\n🚀 Normalizing documentation files and folders\n")

    # Step 1: Backup
    print("📦 Creating backup...")
    if DOCS_DIR.exists():
        import shutil

        shutil.copytree(DOCS_DIR, BACKUP_DIR)
        log(f"Backed up to: {BACKUP_DIR}", "SUCCESS")
    print()

    # Step 2: Rename folders (-- to -)
    rename_folders()

    # Step 3: Rename files (add epic prefix)
    process_all_files()

    # Step 4: Update mapping file
    update_mapping_file()

    # Step 5: Summary
    print("=" * 80)
    print("📊 Normalization Summary")
    print("=" * 80)
    print()
    print(f"Backup location: {BACKUP_DIR}")
    print(f"Folders renamed: {stats['folders_renamed']}")
    print(f"Files renamed: {stats['files_renamed']}")
    print()

    if stats["errors"]:
        print("⚠️  Issues encountered:")
        for error in stats["errors"][:10]:
            print(f"  • {error}")
        if len(stats["errors"]) > 10:
            print(f"  ... and {len(stats['errors']) - 10} more")
    else:
        print("✅ No errors!")

    print()
    print("=" * 80)
    print("✅ Normalization complete!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review the new file names: ls -la docs/F1*/")
    print("2. Verify all files are renamed correctly")
    print("3. If satisfied, delete backup: rm -rf " + str(BACKUP_DIR))
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelled by user")
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        raise
