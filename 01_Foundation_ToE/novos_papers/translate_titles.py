"""
Translate Portuguese titles to English in unified_papers.html
"""
import re
from pathlib import Path

UNIFIED_FILE = Path(r"C:\Users\Douglas\Desktop\ToE\unified_papers.html")

# Translation dictionary: Portuguese -> English
TRANSLATIONS = {
    "Universo Pai": "Parent Universe",
    "Escatologia": "Cosmic Eschatology", 
    "Engenharia Metrica": "Metric Engineering",
    "Consciencia": "Consciousness",
    "Validacao Galactica": "Galactic Validation",
    "Holografia": "Holography",
    "Neutrinos": "Neutrinos",
    "Ds Cft": "dS/CFT Correspondence",
    "Cmb Bmodes": "CMB B-Modes",
    "Cp Violation": "CP Violation",
    "Strong Cp": "Strong CP Problem",
    "Jwst Galaxies": "JWST Galaxies",
    "Susy": "Supersymmetry",
}

print("📖 Reading unified_papers.html...")
with open(UNIFIED_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Apply translations
changes = 0
for pt, en in TRANSLATIONS.items():
    if pt in content:
        content = content.replace(pt, en)
        changes += 1
        print(f"  ✅ '{pt}' → '{en}'")

# Write back
with open(UNIFIED_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Translated {changes} terms")
print(f"📄 Updated: {UNIFIED_FILE}")
