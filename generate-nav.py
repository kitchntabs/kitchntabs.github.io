#!/usr/bin/env python3
"""
KitchnTabs Documentation Navigation Generator

This script automatically generates the sidebar navigation for the Jekyll site
based on the folder structure in the docs/ directory.

Usage:
    python3 generate-nav.py          # Preview navigation HTML
    python3 generate-nav.py --update # Update _layouts/default.html
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

# Configuration
DOCS_DIR = "docs"
LAYOUT_FILE = "_layouts/default.html"

# Icons for different sections (can be customized)
SECTION_ICONS = {
    "mall-app": "📱",
    "customer-app": "👥",
    "staff-app": "👨‍💼",
    "tenant-app": "🏪",
    "admin-app": "⚙️",
    "tech": "⚙️",
    "api": "🔌",
    "guides": "📖",
    "tutorials": "🎓",
    "resources": "📋",
}

# Section titles (can be customized)
SECTION_TITLES = {
    "mall-app": "MALL APP",
    "customer-app": "CUSTOMER APP",
    "staff-app": "STAFF APP",
    "tenant-app": "TENANT APP",
    "admin-app": "ADMIN APP",
    "tech": "TECHNICAL",
    "api": "API REFERENCE",
    "guides": "GUIDES",
    "tutorials": "TUTORIALS",
    "resources": "RESOURCES",
}


def humanize_name(name: str) -> str:
    """Convert file/folder name to human-readable format"""
    # Remove file extension
    name = re.sub(r'\.(md|html)$', '', name)
    
    # Remove leading numbers (e.g., "01-OVERVIEW" -> "OVERVIEW")
    name = re.sub(r'^\d+-', '', name)
    
    # Replace hyphens and underscores with spaces
    name = name.replace('-', ' ').replace('_', ' ')
    
    # Capitalize appropriately
    if name.isupper():
        return name.title()
    
    return name


def get_sort_key(name: str) -> Tuple[int, str]:
    """Extract sort order from filename (e.g., 01-OVERVIEW -> (1, 'OVERVIEW'))"""
    match = re.match(r'^(\d+)-(.+)', name)
    if match:
        return (int(match.group(1)), match.group(2))
    return (999, name)


def should_include_file(filename: str) -> bool:
    """Determine if a file should be included in navigation"""
    # Skip hidden files, README, and certain extensions
    if filename.startswith('.') or filename.startswith('_'):
        return False
    if filename.upper() in ['README.MD', 'INDEX.MD']:
        return False
    if not filename.endswith('.md'):
        return False
    return True


def scan_directory(path: Path, base_path: Path) -> List[Dict]:
    """Recursively scan directory and build navigation structure"""
    items = []
    
    if not path.exists():
        return items
    
    # Get all items in directory
    entries = sorted(path.iterdir(), key=lambda x: get_sort_key(x.name))
    
    for entry in entries:
        if entry.is_file() and should_include_file(entry.name):
            # Calculate relative path for link
            rel_path = entry.relative_to(base_path)
            link = f"/{rel_path}".replace('.md', '')
            
            items.append({
                'type': 'file',
                'name': entry.stem,
                'title': humanize_name(entry.stem),
                'link': link,
            })
        
        elif entry.is_dir() and not entry.name.startswith('.') and not entry.name.startswith('_'):
            # Check if directory has files
            sub_items = scan_directory(entry, base_path)
            if sub_items:
                items.append({
                    'type': 'group',
                    'name': entry.name,
                    'title': humanize_name(entry.name),
                    'items': sub_items,
                })
    
    return items


def generate_nav_html(section: str, items: List[Dict], indent: int = 4) -> str:
    """Generate HTML for navigation items"""
    html = []
    indent_str = ' ' * indent
    
    for item in items:
        if item['type'] == 'file':
            html.append(f'{indent_str}<li><a href="{item["link"]}">{item["title"]}</a></li>')
        
        elif item['type'] == 'group':
            group_id = f"{section}-{item['name']}-group".replace('/', '-')
            html.append(f'{indent_str}<li class="nav-group">')
            html.append(f'{indent_str}    <div class="nav-group-toggle" data-target="{group_id}">')
            html.append(f'{indent_str}        <span>{item["title"]}</span>')
            html.append(f'{indent_str}        <span class="toggle-icon">▼</span>')
            html.append(f'{indent_str}    </div>')
            html.append(f'{indent_str}    <ul class="nav-group-items" id="{group_id}">')
            
            # Recursively generate nested items
            nested_html = generate_nav_html(section, item['items'], indent + 8)
            html.append(nested_html)
            
            html.append(f'{indent_str}    </ul>')
            html.append(f'{indent_str}</li>')
    
    return '\n'.join(html)


def generate_sidebar_html() -> str:
    """Generate complete sidebar HTML"""
    base_path = Path(DOCS_DIR)
    sidebar_sections = []
    
    # Get top-level sections
    if base_path.exists():
        sections = sorted([d for d in base_path.iterdir() if d.is_dir() and not d.name.startswith('.')],
                         key=lambda x: get_sort_key(x.name))
        
        for section_path in sections:
            section_name = section_path.name
            items = scan_directory(section_path, Path('.'))
            
            if not items:
                continue
            
            # Get icon and title
            icon = SECTION_ICONS.get(section_name, "📄")
            title = SECTION_TITLES.get(section_name, humanize_name(section_name).upper())
            
            # Generate section HTML
            section_html = f'''        <nav class="sidebar-nav">
            <div class="sidebar-nav-title">{icon} {title}</div>
            <ul>
{generate_nav_html(section_name, items, 16)}
            </ul>
        </nav>'''
            
            sidebar_sections.append(section_html)
    
    # Add static Resources section
    resources_html = '''        <nav class="sidebar-nav">
            <div class="sidebar-nav-title">📋 RESOURCES</div>
            <ul>
                <li><a href="/privacy/en/">Privacy Policy</a></li>
                <li><a href="/CONTRIBUTING">Contributing</a></li>
                <li><a href="/SITEMAP">Site Map</a></li>
            </ul>
        </nav>'''
    sidebar_sections.append(resources_html)
    
    return '\n\n'.join(sidebar_sections)


def update_layout_file(sidebar_html: str) -> bool:
    """Update the _layouts/default.html file with new navigation"""
    if not os.path.exists(LAYOUT_FILE):
        print(f"Error: {LAYOUT_FILE} not found")
        return False
    
    with open(LAYOUT_FILE, 'r') as f:
        content = f.read()
    
    # Find the sidebar section
    sidebar_start = content.find('<aside class="sidebar">')
    sidebar_end = content.find('</aside>')
    
    if sidebar_start == -1 or sidebar_end == -1:
        print("Error: Could not find sidebar section in layout file")
        return False
    
    # Replace sidebar content
    new_content = (
        content[:sidebar_start] +
        f'<aside class="sidebar">\n{sidebar_html}\n    ' +
        content[sidebar_end:]
    )
    
    with open(LAYOUT_FILE, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Successfully updated {LAYOUT_FILE}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Generate sidebar navigation for KitchnTabs documentation'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update _layouts/default.html with generated navigation'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview the generated HTML without updating'
    )
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🔍 Scanning documentation structure...")
    sidebar_html = generate_sidebar_html()
    
    if args.update:
        print("\n📝 Updating layout file...")
        if update_layout_file(sidebar_html):
            print("\n✨ Done! Review changes and commit:")
            print("   git diff _layouts/default.html")
            print("   git add _layouts/default.html")
            print('   git commit -m "Update navigation structure"')
            print("   git push origin main")
    else:
        print("\n" + "="*60)
        print("GENERATED SIDEBAR HTML:")
        print("="*60)
        print(sidebar_html)
        print("="*60)
        print("\nTo update the layout file, run:")
        print("   python3 generate-nav.py --update")


if __name__ == '__main__':
    main()
