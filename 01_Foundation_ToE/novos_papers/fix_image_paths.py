"""
Fix image paths in unified_papers.html to point to assets/ directory
"""
import re
from pathlib import Path

UNIFIED_FILE = Path(r"C:\Users\Douglas\Desktop\ToE\unified_papers.html")

print("📖 Reading unified_papers.html...")
with open(UNIFIED_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match various image src paths
# Matches: src="assets/xxx.png" or src="paper_xxx/assets/xxx.png" etc.
patterns = [
    # Pattern for relative paths like "assets/xxx.png"
    (r'src="assets/([^"]+)"', r'src="assets/\1"'),
    # Pattern for nested paths - convert to flat
    (r'src="[^"]*?/assets/([^"]+)"', r'src="assets/\1"'),
]

# Simple replacement - just ensure all image paths go to assets/
# Replace any path ending in /assets/xxx.png with assets/xxx.png
pattern = r'src="[^"]*?assets/([^"]+\.png)"'
replacement = r'src="assets/\1"'

count = len(re.findall(pattern, content))
new_content = re.sub(pattern, replacement, content)

print(f"📝 Fixed {count} image paths")

# Write back
with open(UNIFIED_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Updated {UNIFIED_FILE}")
