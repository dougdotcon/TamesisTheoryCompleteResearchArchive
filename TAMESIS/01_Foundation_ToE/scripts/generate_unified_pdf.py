"""
Generate a unified PDF from index.html and all linked papers.
This script:
1. Parses the main index.html
2. Extracts paper links from "Project Papers & Experiments"
3. Merges all papers into a single HTML with page breaks and internal navigation
4. Optionally converts to PDF using Edge/Chrome headless mode
"""

import os
import re
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

# Base directory
BASE_DIR = Path(__file__).parent.parent
OUTPUT_HTML = BASE_DIR / "unified_papers.html"
OUTPUT_PDF = BASE_DIR / "unified_papers.pdf"

# Paper links in reading order (extracted from index.html)
PAPERS = [
    ("paper-1", "Foundations: Derivation of Fundamental Electronic Properties", 
     "2_Laboratorio_Teorico/DerivationofFundamental/index.html"),
    ("paper-2", "Verification: Information as Geometry (Entropic Gravity)", 
     "1_Motores_Cientificos/EntropicGravity_Engine/index.html"),
    ("paper-3", "Verification: Planck Dynamics Simulation", 
     "2_Laboratorio_Teorico/PlanckDynamics_Sim/index.html"),
    ("paper-4", "Cosmology: The Reactive Universe", 
     "1_Motores_Cientificos/ReactiveCosmoMapper/index.html"),
    ("paper-5", "Cosmology: Black Hole Universe Cosmology", 
     "2_Laboratorio_Teorico/Bounce_Cosmology/index.html"),
    ("paper-6", "Extensions: P vs NP Thermodynamic Constraints", 
     "3_Experiment/P_vs_NP_Paper/paper_p_vs_np.html"),
]


def extract_body_content(html_path: Path, paper_id: str) -> str:
    """Extract the main content from a paper HTML, adjusting image paths."""
    if not html_path.exists():
        return f'<div class="paper-section" id="{paper_id}"><p style="color:red;">File not found: {html_path}</p></div>'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Find the body content
    body = soup.find('body')
    if not body:
        return f'<div class="paper-section" id="{paper_id}"><p style="color:red;">No body found in: {html_path}</p></div>'
    
    # Remove "Back to Main" links
    for link in body.find_all('a'):
        if 'Back' in link.get_text():
            link.decompose()
    
    # Adjust image paths to be relative to base directory
    paper_dir = html_path.parent
    for img in body.find_all('img'):
        src = img.get('src', '')
        if src and not src.startswith('http'):
            # Make path relative to base directory
            abs_img_path = paper_dir / src
            if abs_img_path.exists():
                rel_path = abs_img_path.relative_to(BASE_DIR)
                img['src'] = str(rel_path).replace('\\', '/')
    
    return f'''
    <div class="paper-section" id="{paper_id}">
        {body.decode_contents()}
    </div>
    '''


def create_unified_html():
    """Create a single HTML file with all papers and navigation."""
    
    # Build Table of Contents
    toc_items = []
    for paper_id, title, _ in PAPERS:
        toc_items.append(f'<li><a href="#{paper_id}">{title}</a></li>')
    
    toc_html = f'''
    <div class="toc-section">
        <h2>Supplementary Papers</h2>
        <p class="toc-description">This unified document contains the complete derivation papers and computational verifications. Click any title to navigate.</p>
        <ol class="toc-list">
            {''.join(toc_items)}
        </ol>
    </div>
    '''
    
    # Read main index.html - FULL CONTENT (the unified framework paper)
    main_index = BASE_DIR / "index.html"
    with open(main_index, 'r', encoding='utf-8') as f:
        main_soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Get header, abstract, AND the full content body
    header = main_soup.find('header')
    abstract = main_soup.find('div', class_='abstract-box')
    content_body = main_soup.find('div', class_='content-body')
    
    # Also get the Project Papers section (to remove it from main, since we're appending them)
    papers_section = main_soup.find('div', style=lambda x: x and 'Project Papers' in str(x) if x else False)
    if papers_section:
        papers_section.decompose()  # Remove from content since we're adding full papers
    
    header_html = header.decode() if header else ''
    abstract_html = abstract.decode() if abstract else ''
    content_html = content_body.decode() if content_body else ''
    
    # Build paper sections
    paper_sections = []
    for paper_id, title, rel_path in PAPERS:
        html_path = BASE_DIR / rel_path
        content = extract_body_content(html_path, paper_id)
        paper_sections.append(content)
    
    # Combine everything
    unified_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Holographic Origin of Matter and Dynamics - Complete Papers</title>
    
    <!-- KaTeX for Math -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
    
    <style>
        body {{
            font-family: 'Times New Roman', Times, serif;
            line-height: 1.6;
            color: #1a1a1a;
            max-width: 210mm;
            margin: 0 auto;
            padding: 2cm;
            background-color: #fff;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid #ccc;
            padding-bottom: 1rem;
        }}
        
        h1 {{
            font-size: 22pt;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }}
        
        h2 {{
            font-size: 14pt;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            border-bottom: 2px solid #000;
            padding-bottom: 0.2rem;
        }}
        
        h3 {{
            font-size: 12pt;
            font-style: italic;
            margin-top: 1.2rem;
            margin-bottom: 0.5rem;
        }}
        
        .authors {{
            font-size: 12pt;
            font-style: italic;
            margin-bottom: 0.5rem;
        }}
        
        .affiliations {{
            font-size: 10pt;
            color: #555;
            margin-bottom: 1.5rem;
        }}
        
        .abstract-box {{
            max-width: 80%;
            margin: 0 auto 2rem auto;
            font-size: 0.95rem;
            text-align: justify;
            background-color: #f9f9f9;
            padding: 1.5rem;
            border-left: 3px solid #000;
        }}
        
        .abstract-title {{
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
            display: block;
            text-align: center;
        }}
        
        .toc-section {{
            background-color: #f0f7ff;
            padding: 1.5rem;
            margin: 2rem 0;
            border-left: 3px solid #0056b3;
        }}
        
        .toc-section h2 {{
            margin-top: 0;
            color: #004494;
            border-bottom: none;
        }}
        
        .toc-list {{
            margin: 1rem 0 0 0;
            padding-left: 1.5rem;
        }}
        
        .toc-list li {{
            margin-bottom: 0.5rem;
        }}
        
        .toc-list a {{
            color: #0056b3;
            text-decoration: none;
        }}
        
        .toc-list a:hover {{
            text-decoration: underline;
        }}
        
        /* Paper sections - page break before each */
        .paper-section {{
            page-break-before: always;
            break-before: page;
            margin-top: 2rem;
        }}
        
        /* First paper doesn't need page break */
        .paper-section:first-of-type {{
            page-break-before: avoid;
            break-before: avoid;
        }}
        
        /* Content styling */
        .content-body {{
            column-count: 2;
            column-gap: 1cm;
            text-align: justify;
        }}
        
        p {{
            margin-bottom: 1rem;
            text-indent: 1em;
        }}
        
        p.no-indent {{
            text-indent: 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 10pt;
            break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #333;
            padding: 0.4rem;
            text-align: center;
        }}
        
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        
        .result-highlight {{
            background-color: #e8f5e9;
            font-weight: bold;
        }}
        
        .equation-box {{
            background-color: #f5f5f5;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 3px solid #333;
            break-inside: avoid;
        }}
        
        .master-equation {{
            background-color: #e3f2fd;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border: 2px solid #1976d2;
            text-align: center;
            break-inside: avoid;
        }}
        
        figure {{
            margin: 1.5rem 0;
            break-inside: avoid;
            page-break-inside: avoid;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0.5rem auto;
            border: 1px solid #eee;
        }}
        
        figcaption {{
            font-size: 9pt;
            color: #444;
            margin-top: 0.4rem;
            text-align: center;
            font-style: italic;
        }}
        
        .references ol {{
            font-size: 9pt;
            padding-left: 1.5rem;
        }}
        
        .references li {{
            margin-bottom: 0.5rem;
        }}
        
        /* Print Optimizations */
        @media print {{
            body {{
                padding: 0;
                margin: 0;
            }}
            
            @page {{
                size: A4;
                margin: 2cm;
            }}
            
            a {{
                text-decoration: none;
                color: #000;
            }}
            
            .toc-section {{
                page-break-after: always;
            }}
        }}
    </style>
</head>
<body>
    {header_html}
    {abstract_html}
    {toc_html}
    
    <!-- Main Unified Framework Content -->
    {content_html}
    
    <!-- Supplementary Papers -->
    {''.join(paper_sections)}
    
</body>
</html>
'''
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(unified_html)
    
    print(f"✅ Created unified HTML: {OUTPUT_HTML}")
    return OUTPUT_HTML


def convert_to_pdf(html_path: Path):
    """Convert HTML to PDF using Edge or Chrome headless mode."""
    
    # Try Edge first (Windows default)
    browsers = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    
    browser_path = None
    for path in browsers:
        if os.path.exists(path):
            browser_path = path
            break
    
    if not browser_path:
        print("❌ No browser found for PDF conversion.")
        print(f"   Please open {html_path} in a browser and use Print > Save as PDF")
        return None
    
    # Run headless PDF conversion
    cmd = [
        browser_path,
        '--headless',
        '--disable-gpu',
        '--no-sandbox',
        f'--print-to-pdf={OUTPUT_PDF}',
        f'file:///{html_path.absolute()}'.replace('\\', '/')
    ]
    
    print(f"🔄 Converting to PDF using: {os.path.basename(browser_path)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if OUTPUT_PDF.exists() and OUTPUT_PDF.stat().st_size > 0:
            print(f"✅ Created PDF: {OUTPUT_PDF}")
            return OUTPUT_PDF
        else:
            print(f"❌ PDF conversion failed. Check {html_path} manually.")
            return None
    except subprocess.TimeoutExpired:
        print("❌ PDF conversion timed out.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    print("=" * 60)
    print("📄 Unified PDF Generator for TARDIS: The Theory of Everything")
    print("=" * 60)
    
    # Step 1: Create unified HTML
    html_path = create_unified_html()
    
    # Step 2: Convert to PDF
    pdf_path = convert_to_pdf(html_path)
    
    print("\n" + "=" * 60)
    if pdf_path:
        print(f"🎉 SUCCESS! PDF created at: {pdf_path}")
    else:
        print(f"📝 HTML created at: {html_path}")
        print("   Open in browser and use Print > Save as PDF")
    print("=" * 60)


if __name__ == "__main__":
    main()
