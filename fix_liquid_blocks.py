#!/usr/bin/env python3
import re
import os

# Files with Liquid syntax errors in code blocks
problem_files = [
    "docs/F14-Auth-Access-Control/F14-Auth-Access-Control_PERMISSION_SELECTOR_DATAGRID.md",
    "docs/F23-DeliveryModule/ARCH_DELIVERY_GUIDE.md",
    "docs/F11-Checkout-Gateways/F11-Checkout-Gateways_ML-CHECKOUT-PRO-DOCS.md",
    "docs/F12-Billing-Subscriptions-Payments/F12-Billing-Subscriptions-Payments_SUBSCRIPTION_PLAN_ADDONS_FEATURE.md",
]

for filepath in problem_files:
    if not os.path.exists(filepath):
        print(f"✗ {filepath} not found")
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Pattern to find code blocks with {{ }}
    # Look for ```...{{ ... }}...``` patterns
    lines = content.split('\n')
    in_code_block = False
    fixed_lines = []
    code_block = []
    code_block_start = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.strip().startswith('```'):
            if not in_code_block:
                # Starting code block
                in_code_block = True
                code_block = [line]
                code_block_start = i
            else:
                # Ending code block
                code_block.append(line)
                
                # Check if block contains {{ with colons or $ symbols
                block_text = '\n'.join(code_block)
                if (re.search(r'\{\{[^}]*:', block_text) or 
                    re.search(r'\{\{\s*\$', block_text) or
                    re.search(r'\{\{[^}]*,\s*[^}]*\}\}', block_text)):
                    # Wrap in raw tags
                    fixed_lines.append('{% raw %}')
                    fixed_lines.extend(code_block)
                    fixed_lines.append('{% endraw %}')
                else:
                    fixed_lines.extend(code_block)
                
                in_code_block = False
                code_block = []
        elif in_code_block:
            code_block.append(line)
        else:
            fixed_lines.append(line)
        
        i += 1
    
    # Handle case where file ends in code block
    if in_code_block and code_block:
        fixed_lines.extend(code_block)
    
    new_content = '\n'.join(fixed_lines)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f"✓ {filepath}")

print("\nFixed code blocks with Liquid syntax")
