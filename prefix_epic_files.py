#!/usr/bin/env python3
"""
Add epic prefix to all files in epic folders
"""

import re
from pathlib import Path

DOCS_DIR = Path("/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/docs")

# Mapping of folder names to their prefixes
FOLDER_PREFIXES = {
    "F1-Orders-Tabs": "F1-Orders-Tabs",
    "F2-Products-Catalog": "F2-Products-Catalog",
    "F3-Product-Import-Export": "F3-Product-Import-Export",
    "F4-Mall-Food-Court": "F4-Mall-Food-Court",
    "F5-Customer-Self-Service": "F5-Customer-Self-Service",
    "F6-Tenant-Staff-App": "F6-Tenant-Staff-App",
    "F7-System-Admin-Application": "F7-System-Admin-Application",
    "F8-Public-Web": "F8-Public-Web",
    "F9-Marketplaces": "F9-Marketplaces",
    "F10-Point-of-Sale": "F10-Point-of-Sale",
    "F11-Checkout-Gateways": "F11-Checkout-Gateways",
    "F12-Billing-Subscriptions-Payments": "F12-Billing-Subscriptions-Payments",
    "F13-Platform-Multi-Tenancy": "F13-Platform-Multi-Tenancy",
    "F14-Auth-Access-Control": "F14-Auth-Access-Control",
    "F15-Notifications-Messaging": "F15-Notifications-Messaging",
    "F16-AI-Agents": "F16-AI-Agents",
    "F17-Inventory": "F17-Inventory",
    "F18-Campaigns": "F18-Campaigns",
    "F19-Internationalization": "F19-Internationalization",
    "F20-Media-Images": "F20-Media-Images",
    "F21-Tenancy-Management": "F21-Tenancy-Management",
    "F22-MiddlewareService": "F22-MiddlewareService",
    "F23-DeliveryModule": "F23-DeliveryModule",
    "F24-InventoryModule": "F24-InventoryModule",
    "F25-CashcountModule": "F25-CashcountModule",
    "N1-Backend-Framework": "N1-Backend-Framework",
    "N2-Frontend-Framework": "N2-Frontend-Framework",
    "N3-Infrastructure-CICD": "N3-Infrastructure-CICD",
    "N4-Build-Toolchain": "N4-Build-Toolchain",
    "N5-Desktop-Device-Service": "N5-Desktop-Device-Service",
    "N6-Caching-Performance": "N6-Caching-Performance",
    "N7-Security": "N7-Security",
    "N8-Observability": "N8-Observability",
    "N9-App-Publishing": "N9-App-Publishing",
    "N10-Administrative-Legal": "N10-Administrative-Legal",
}

stats = {
    "files_renamed": 0,
    "skipped": 0,
    "errors": [],
}


def log(message, level="INFO"):
    if level == "ERROR":
        print(f"❌ {message}")
    elif level == "SUCCESS":
        print(f"✅ {message}")
    else:
        print(f"ℹ️  {message}")


def rename_files_in_folder(folder_path: Path, prefix: str):
    """Rename all .md files in a folder with the given prefix."""
    md_files = sorted(folder_path.glob("*.md"))

    if not md_files:
        return 0

    count = 0
    print(f"\n→ {folder_path.name}/ ({len(md_files)} files)")

    for file_path in md_files:
        # Skip if already prefixed
        if file_path.name.startswith(f"{prefix}_"):
            print(f"  ⊘ {file_path.name:65} (already prefixed)")
            stats["skipped"] += 1
            continue

        # Create new filename with prefix
        new_name = f"{prefix}_{file_path.stem}.md"
        new_path = folder_path / new_name

        try:
            file_path.rename(new_path)
            print(f"  ✓ {file_path.name:65} → {new_name}")
            stats["files_renamed"] += 1
            count += 1
        except Exception as e:
            error_msg = f"Error renaming {file_path.name} in {folder_path.name}: {e}"
            stats["errors"].append(error_msg)
            log(error_msg, "ERROR")

    return count


def main():
    print("\n🚀 Adding epic prefixes to documentation files\n")

    total_renamed = 0

    # Process epic folders
    for folder_name, prefix in sorted(FOLDER_PREFIXES.items()):
        folder_path = DOCS_DIR / folder_name

        if not folder_path.exists():
            continue

        renamed_count = rename_files_in_folder(folder_path, prefix)
        total_renamed += renamed_count

    # Process General-Utilities
    gen_folder = DOCS_DIR / "General-Utilities"
    if gen_folder.exists():
        print(f"\n→ General-Utilities/ (GEN prefix)")
        for file_path in sorted(gen_folder.glob("*.md")):
            if file_path.name.startswith("GEN_"):
                print(f"  ⊘ {file_path.name:65} (already prefixed)")
                stats["skipped"] += 1
                continue

            new_name = f"GEN_{file_path.stem}.md"
            new_path = gen_folder / new_name

            try:
                file_path.rename(new_path)
                print(f"  ✓ {file_path.name:65} → {new_name}")
                stats["files_renamed"] += 1
                total_renamed += 1
            except Exception as e:
                stats["errors"].append(f"Error renaming {file_path.name}: {e}")
                log(f"Error renaming {file_path.name}: {e}", "ERROR")

    # Summary
    print("\n" + "=" * 80)
    print("📊 Summary")
    print("=" * 80)
    print(f"\nFiles renamed:  {stats['files_renamed']}")
    print(f"Files skipped:  {stats['skipped']} (already prefixed)")
    print(f"Errors:         {len(stats['errors'])}")

    if stats["errors"]:
        print("\n⚠️  Issues:")
        for error in stats["errors"][:5]:
            print(f"  • {error}")
        if len(stats["errors"]) > 5:
            print(f"  ... and {len(stats['errors']) - 5} more")

    print("\n" + "=" * 80)
    print("✅ All done!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelled")
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        raise
