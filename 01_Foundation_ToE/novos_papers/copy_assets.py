"""
Copy all paper assets to central assets folder
"""
import os
import shutil
from pathlib import Path

PAPERS_DIR = Path(r"C:\Users\Douglas\Desktop\ToE\novos_papers")
ASSETS_DIR = Path(r"C:\Users\Douglas\Desktop\ToE\assets")

# Ensure assets dir exists
ASSETS_DIR.mkdir(exist_ok=True)

# Find and copy all PNG files
copied = 0
for paper_dir in PAPERS_DIR.iterdir():
    if paper_dir.is_dir() and paper_dir.name.startswith("paper_"):
        assets_path = paper_dir / "assets"
        if assets_path.exists():
            for img_file in assets_path.glob("*.png"):
                dest = ASSETS_DIR / img_file.name
                shutil.copy2(img_file, dest)
                print(f"✅ {img_file.name}")
                copied += 1

print(f"\n🎉 Copied {copied} images to {ASSETS_DIR}")
