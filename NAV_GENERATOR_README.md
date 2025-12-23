# Navigation Generator for KitchnTabs Docs

This script automatically generates the sidebar navigation for the documentation site based on your folder structure.

## Features

- 🔍 **Automatic Discovery**: Scans `docs/` folder and all subdirectories
- 🏗️ **Nested Navigation**: Creates collapsible groups for nested folders
- 🎯 **Smart Sorting**: Respects numbered prefixes (e.g., `01-OVERVIEW`, `02-ARCHITECTURE`)
- 🎨 **Custom Icons**: Assigns emoji icons to different sections
- ✨ **Human-Readable**: Converts filenames to readable titles
- 🔄 **Auto-Update**: Can directly update `_layouts/default.html`

## Usage

### 1. Preview Generated Navigation

```bash
python3 generate-nav.py
```

This will scan your docs folder and print the generated HTML without making changes.

### 2. Update Layout File

```bash
python3 generate-nav.py --update
```

This will automatically update `_layouts/default.html` with the new navigation structure.

### 3. After Adding New Docs

When you add new documentation files:

```bash
# 1. Add your new markdown files to docs/
mkdir -p docs/new-section
echo "# New Doc" > docs/new-section/my-doc.md

# 2. Run the generator
python3 generate-nav.py --update

# 3. Review and commit
git diff _layouts/default.html
git add _layouts/default.html docs/
git commit -m "Add new documentation section"
git push origin main
```

## Folder Structure Conventions

### File Naming

- Use numbered prefixes for ordering: `01-overview.md`, `02-getting-started.md`
- Use hyphens for spaces: `user-guide.md` → "User Guide"
- Use all caps for acronyms: `API-REFERENCE.md` → "API Reference"

### Section Icons

The script automatically assigns icons based on folder names:

| Folder | Icon | Title |
|--------|------|-------|
| `mall-app` | 📱 | MALL APP |
| `customer-app` | 👥 | CUSTOMER APP |
| `staff-app` | 👨‍💼 | STAFF APP |
| `tenant-app` | 🏪 | TENANT APP |
| `tech` | ⚙️ | TECHNICAL |
| `api` | 🔌 | API REFERENCE |
| `guides` | 📖 | GUIDES |
| `tutorials` | 🎓 | TUTORIALS |

**To add custom icons**, edit the `SECTION_ICONS` dictionary in `generate-nav.py`:

```python
SECTION_ICONS = {
    "my-section": "🚀",
    # ... other icons
}
```

## Example Folder Structure

```
docs/
├── mall-app/
│   ├── 01-OVERVIEW.md
│   ├── 02-ARCHITECTURE.md
│   └── features/
│       ├── sessions.md
│       └── orders.md
├── tech/
│   ├── architecture/
│   │   └── ARCHITECTURE.md
│   └── features/
│       ├── acl/
│       │   ├── overview.md
│       │   └── tests.md
│       └── notifications/
│           └── system.md
└── guides/
    ├── getting-started.md
    └── deployment.md
```

This generates:

```
📱 MALL APP
  - Overview
  - Architecture
  ▼ Features
    - Sessions
    - Orders

⚙️ TECHNICAL
  ▼ Architecture
    - Architecture
  ▼ Features
    ▼ ACL
      - Overview
      - Tests
    ▼ Notifications
      - System

📖 GUIDES
  - Getting Started
  - Deployment
```

## Customization

### Change Section Order

Edit the `SECTION_TITLES` dictionary to control which sections appear and their display names.

### Exclude Files

The script automatically excludes:
- Hidden files (starting with `.`)
- Files starting with `_`
- `README.md` and `INDEX.md`
- Non-markdown files

To exclude additional patterns, modify the `should_include_file()` function.

### Change Indent/Formatting

Modify the `generate_nav_html()` function to adjust HTML formatting.

## Troubleshooting

### Script doesn't find docs folder
Make sure you run it from the repository root:
```bash
cd /path/to/kitchntabs-github-io
python3 generate-nav.py
```

### Links are broken
The script generates Jekyll-compatible links without `.html` extensions. Ensure your markdown files have proper front matter:
```yaml
---
layout: default
title: My Page
---
```

### Navigation doesn't collapse
Make sure the JavaScript in `_layouts/default.html` hasn't been modified. The script generates proper `data-target` attributes for collapsible groups.

## Tips

1. **Use numbered prefixes** for important ordering (01, 02, 03...)
2. **Keep folder names short** - they become navigation labels
3. **Use descriptive filenames** - they appear in the nav menu
4. **Group related docs** in subfolders for automatic nested navigation
5. **Run the script before committing** new docs to keep nav in sync

## Integration with Git Workflow

Add to your commit workflow:

```bash
# Create a git alias
git config alias.update-nav '!python3 generate-nav.py --update'

# Then use it
git update-nav
git add _layouts/default.html
git commit -m "Update navigation"
```

Or add to a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit
python3 generate-nav.py --update
git add _layouts/default.html
```
