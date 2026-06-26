#!/usr/bin/env python3
import os
import sys

docs_dir = "docs"
count = 0

for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Check if file already has front matter
            if not content.startswith("---"):
                # Extract title from filename
                title = file.replace(".md", "").replace("_", " ")
                
                # Add front matter
                frontmatter = f"""---
layout: default
title: {title}
---

"""
                new_content = frontmatter + content
                
                with open(filepath, 'w') as f:
                    f.write(new_content)
                
                count += 1
                print(f"✓ {filepath}")

print(f"\nAdded front matter to {count} files")
