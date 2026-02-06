"""
Script to unify all individual HTML papers into unified_papers.html
"""
import os
import re
from pathlib import Path

# Configuration
PAPERS_DIR = Path(__file__).parent
ROOT_DIR = PAPERS_DIR.parent
UNIFIED_FILE = ROOT_DIR / "unified_papers.html"
OUTPUT_FILE = ROOT_DIR / "unified_papers_complete.html"

# Paper directories to process (in order)
PAPER_DIRS = [
    "paper_universo_pai",
    "paper_escatologia",
    "paper_engenharia_metrica", 
    "paper_consciencia",
    "paper_validacao_galactica",
    "paper_holografia",
    "paper_neutrinos",
    "paper_cluster_lensing",
    "paper_origin_omega",
    "paper_schrodinger_test",
    "paper_heavy_quarks",
    "paper_unification",
    "paper_ds_cft",
    "paper_inflation",
    "paper_horizon_access",
    "paper_multiverse",
    "paper_higgs_topology",
    "paper_jwst_galaxies",
    "paper_hubble_tension",
    "paper_flavor_anomalies",
    "paper_susy",
    "paper_dark_candidates",
    "paper_wormholes",
    "paper_emergent_time",
    "paper_bekenstein_lab",
    "paper_baryon_topology",
    "paper_cmb_bmodes",
    "paper_gravitational_waves",
    "paper_cosmological_voids",
    "paper_cp_violation",
    "paper_neutrino_oscillations",
    "paper_strong_cp",
    "paper_cosmological_constant",
    "paper_information_paradox",
    "paper_measurement_problem",
    "paper_fine_structure",
    "paper_singularity",
]

def extract_body_content(html_path: Path) -> str:
    """Extract content between <body> and </body> tags."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract body content
        match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if match:
            body = match.group(1).strip()
            return body
        return ""
    except Exception as e:
        print(f"  ⚠️ Error reading {html_path}: {e}")
        return ""

def get_paper_title(paper_dir: str) -> str:
    """Generate a readable title from directory name."""
    title = paper_dir.replace("paper_", "").replace("_", " ").title()
    return title

def create_paper_section(paper_dir: str, paper_id: int, body_content: str) -> str:
    """Wrap paper content in a section div."""
    title = get_paper_title(paper_dir)
    
    section = f'''
    <!-- Paper {paper_id}: {title} -->
    <div class="paper-section" id="paper-{paper_id}">
        {body_content}
    </div>
'''
    return section

def update_toc(existing_html: str, paper_dirs: list) -> str:
    """Update the table of contents with new papers."""
    # Find TOC section
    toc_start = existing_html.find('<ul class="toc-list">')
    toc_end = existing_html.find('</ul>', toc_start)
    
    if toc_start == -1 or toc_end == -1:
        return existing_html
    
    # Build new TOC entries for papers 7+
    new_entries = []
    for i, paper_dir in enumerate(paper_dirs, start=7):
        title = get_paper_title(paper_dir)
        badge_type = "extension"  # Default badge
        
        # Categorize papers
        if "validation" in paper_dir or "galaxies" in paper_dir or "tension" in paper_dir:
            badge_type = "verification"
        elif "cosmolog" in paper_dir or "inflation" in paper_dir or "universe" in paper_dir or "cmb" in paper_dir:
            badge_type = "cosmology"
        elif "fundamentals" in paper_dir or "electron" in paper_dir or "omega" in paper_dir:
            badge_type = "foundation"
        
        entry = f'''            <li><span class="badge badge-{badge_type}">Paper {i}</span> <a href="#paper-{i}">{title}</a></li>'''
        new_entries.append(entry)
    
    # We'll append new entries after the existing ones
    new_toc_items = "\n".join(new_entries)
    
    # Insert before </ul>
    modified_html = existing_html[:toc_end] + "\n" + new_toc_items + "\n        " + existing_html[toc_end:]
    
    return modified_html

def main():
    print("=" * 60)
    print("🔧 UNIFYING HTML PAPERS")
    print("=" * 60)
    
    # Read existing unified file
    print(f"\n📖 Reading: {UNIFIED_FILE}")
    with open(UNIFIED_FILE, 'r', encoding='utf-8') as f:
        unified_content = f.read()
    
    # Find insertion point (before </body>)
    insertion_point = unified_content.rfind('</body>')
    if insertion_point == -1:
        print("❌ Could not find </body> tag in unified_papers.html")
        return
    
    # Process each paper
    new_sections = []
    processed = 0
    
    print(f"\n📝 Processing {len(PAPER_DIRS)} papers...\n")
    
    for i, paper_dir in enumerate(PAPER_DIRS, start=7):
        paper_path = PAPERS_DIR / paper_dir / "index.html"
        
        if paper_path.exists():
            body_content = extract_body_content(paper_path)
            if body_content:
                section = create_paper_section(paper_dir, i, body_content)
                new_sections.append(section)
                processed += 1
                title = get_paper_title(paper_dir)
                print(f"  ✅ Paper {i}: {title}")
            else:
                print(f"  ⚠️ Paper {i}: {paper_dir} - Empty content")
        else:
            print(f"  ❌ Paper {i}: {paper_dir} - File not found")
    
    # Combine all new sections
    all_new_content = "\n".join(new_sections)
    
    # Insert new content before </body>
    final_content = (
        unified_content[:insertion_point] + 
        "\n\n    <!-- ========== NEW SUPPLEMENTARY PAPERS ========== -->\n" +
        all_new_content + 
        "\n" +
        unified_content[insertion_point:]
    )
    
    # Update TOC
    final_content = update_toc(final_content, PAPER_DIRS)
    
    # Write output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\n{'=' * 60}")
    print(f"✅ UNIFIED PAPER CREATED")
    print(f"   Papers processed: {processed}/{len(PAPER_DIRS)}")
    print(f"   Output: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()
