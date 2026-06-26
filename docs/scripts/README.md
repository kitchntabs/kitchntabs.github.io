# Documentation & Build Scripts

Internal scripts and utilities for maintaining the KitchnTabs documentation site.

## 📋 Available Scripts

- **Sidebar Generator** — Auto-generates the documentation sidebar from epic structure
- **Epic Index Generator** — Creates index pages for all epics
- **Timeline Extractor** — Extracts development timelines from git history

## 🚀 Usage

All scripts should be run from the repository root:

```bash
python3 /tmp/gen_sidebar.py    # Generate sidebar
python3 /tmp/generate_epic_index.py  # Generate epic indices
```

## 📝 Script Documentation

### Sidebar Generation

Automatically generates `_sidebar.md` from the epic folder structure.

- **Purpose**: Maintain navigation as new epics are added
- **Input**: Epic folders in `docs/` directory
- **Output**: `_sidebar.md` with organized epic structure
- **Trigger**: Run after adding new epics

### Epic Index Generation

Creates `index.md` for each epic with overview and scope.

- **Purpose**: Provide quick navigation for each epic
- **Input**: Epic metadata and document count
- **Output**: `docs/[EPIC]/index.md` files
- **Trigger**: Run when epic structure or content changes

### Timeline Extraction

Extracts commit history to infer feature development timelines.

- **Purpose**: Auto-populate ClickUp Gantt charts with development dates
- **Input**: Git repositories (dash-backend, kitchntabs-frontend, etc.)
- **Output**: `EPIC_TIMELINE.json` with start/end dates
- **Trigger**: Run periodically to update timelines

## 🔧 Maintenance

Scripts are located in:
- `~/.claude/skills/` — Claude Code development session automation
- `/tmp/` — Temporary build and generation scripts

## 📚 Related Documentation

- [N0: Architecture](/docs/N0-Architecture/) — System design
- [Epic Index](/EPIC_INDEX.md) — All epics
