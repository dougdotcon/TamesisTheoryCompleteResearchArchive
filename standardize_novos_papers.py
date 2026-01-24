
import os
import re
from html.parser import HTMLParser


ROOT_DIRS = [
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\01_Foundation_ToE\novos_papers",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\01_Foundation_ToE\1_Motores_Cientificos",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\02_Research_Limits",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\03_System_Closure",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\04_Universe_Equation",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\05_Final_Reduction",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\06_Operational_Derivation",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\07_Rigorous_Mathematics",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\08_Modified_Operators",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\09_Hyperbolic_Connection",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\10_Hyperbolic_Space",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\11_Hyperbolic_Laplacian",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\12_Selberg_Connes",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\13_RH_Operator",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\14_ToE_Physics",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\15_Layer1_Selberg_Cusp",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\16_Layer2_Conceptual_Architecture",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\17_Arg_Phi_Decomposition",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\18_Publishable_Lemma",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\19_Selberg_Weil_Interface",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\20_Final_Paper",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\21_Connes_Dilation_Operator",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\22_Spectral_Reconstruction",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\23_Trace_Regularization",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\24_Theta_Derivative_Trace",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\25_Prime_Contribution_Trace",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\26_Complete_Spectral_Identity",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\27_RH_As_Spectral_Property",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\28_Graph_Zeta_Primes",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\29_Chaotic_Flow_Primes",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\30_Computational_Primes",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\31_Euclidean_Spectral_Operator",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\32_Complexity_As_Prime_Count",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\33_Computational_Levinson",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\34_Spectral_Theory_Computation",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\35_Unified_Constants_Derivation",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\36_Theory_of_Regime_Transitions",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\37_U12_Physical_Tests",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\38_U12_Applications",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\39_U2_Lindblad_Class",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\40_U0_Threshold_Class",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\41_Universality_Atlas",
    r"d:\TamesisTheoryCompleteResearchArchive\TAMESIS\42_Closure_Paper"
]


# Template parts
TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
    <style>
        /* PRL Style: Two-column layout, compact, Times New Roman */
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 10pt;
            line-height: 1.15;
            color: #000;
            max-width: 210mm;
            margin: 0 auto;
            padding: 1.5cm;
            background-color: #fff;
        }}
        .content-wrapper {{
            column-count: 2;
            column-gap: 0.8cm;
            text-align: justify;
        }}
        header {{
            text-align: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #ccc;
        }}
        h1 {{
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 0.5rem;
            line-height: 1.2;
            text-transform: none;
        }}
        .authors {{ font-size: 10pt; margin-bottom: 0.2rem; }}
        .affiliations {{ font-size: 9pt; font-style: italic; color: #444; margin-bottom: 1rem; }}
        .date {{ font-size: 9pt; color: #666; }}
        .abstract {{
            font-weight: bold;
            font-size: 9pt;
            margin: 0 auto 1.5rem auto;
            width: 85%;
            text-align: justify;
            font-style: italic;
        }}
        h2 {{
            font-size: 10pt;
            font-weight: bold;
            text-transform: uppercase;
            margin-top: 1.2rem;
            margin-bottom: 0.6rem;
            border-bottom: 1px solid #000;
            break-after: avoid;
        }}
        h3 {{
            font-size: 10pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 1rem;
            margin-bottom: 0.4rem;
        }}
        p {{ margin-bottom: 0.8rem; text-indent: 1em; }}
        p.no-indent {{ text-indent: 0; }}
        .equation {{ text-align: center; margin: 0.8rem 0; font-size: 10pt; }}
        /* Specialized Boxes compatibility */
        .axiom-box {{ border-left: 3px solid #000; padding: 0.8rem; margin: 1rem 0; font-style: italic; }}
        .prediction-box {{ border: 1px solid #d32f2f; padding: 1rem; margin: 1rem 0; background: #fff5f5; }}
        .master-equation {{ background: #f8f8f8; padding: 1rem; margin: 1rem 0; border: 1px solid #ccc; text-align: center; }}
        .conclusion-box {{ background: #e8f5e9; padding: 1rem; margin: 1.5rem 0; border: 1px solid #4caf50; text-align: center; }}
        
        figure {{ margin: 1rem 0; text-align: center; break-inside: avoid; }}
        figure img {{ width: 100%; border: 1px solid #eee; }}
        figcaption {{ font-size: 8.5pt; color: #333; margin-top: 0.4rem; text-align: justify; }}
        table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 8.5pt; }}
        th, td {{ border-bottom: 1px solid #000; padding: 0.4rem; text-align: left; }}
        th {{ font-weight: bold; border-top: 1px solid #000; }}
        .references {{
            margin-top: 2rem;
            padding-top: 0.5rem;
            border-top: 1px solid #000;
            font-size: 8pt;
            line-height: 1.1;
        }}
        .references ol {{ padding-left: 1rem; margin-top: 0.5rem; }}
        .references li {{ margin-bottom: 0.2rem; }}
    </style>
</head>
<body>
    <header>
        <h1>{paper_title}</h1>
        <div class="authors">Douglas H. M. Fulber</div>
        <div class="affiliations">Universidade Federal do Rio de Janeiro, Rio de Janeiro, Brazil</div>
        <div class="date">(Dated: January 23, 2026)</div>
    </header>
"""

TEMPLATE_BODY_START = """
    <div class="abstract">
        {abstract}
    </div>

    <div class="content-wrapper">
"""

TEMPLATE_END = """
    </div>
</body>
</html>
"""

def extract_content(html_content):
    # Simple regex extraction for robustness against malformed HTML
    
    # Title
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    page_title = title_match.group(1).strip() if title_match else "Unified Theory Paper"
    
    # H1
    h1_match = re.search(r'<h1>(.*?)</h1>', html_content, re.DOTALL)
    paper_title = h1_match.group(1).strip() if h1_match else page_title

    # Abstract
    abstract_match = re.search(r'<div class="abstract-box"[^>]*>(.*?)</div>', html_content, re.DOTALL)
    if abstract_match:
        # Clean abstract content (remove span title if present)
        abstract_content = abstract_match.group(1).strip()
        abstract_content = re.sub(r'<span[^>]*>.*?</span>', '', abstract_content, count=1).strip() # Remove "Abstract" label
    else:
        abstract_content = "Abstract not found."

    # References
    refs_match = re.search(r'<div class="references"[^>]*>(.*?)</div>', html_content, re.DOTALL)
    references = refs_match.group(1).strip() if refs_match else ""

    # Main Body - tricky part, we need everything between header/abstract and references/footer
    # We'll use start/end markers logic
    
    # Find end of abstract
    abstract_end_idx = 0
    if abstract_match:
        abstract_end_idx = abstract_match.end()
    else:
        # fallback to header end
        header_end = re.search(r'</header>', html_content)
        if header_end:
            abstract_end_idx = header_end.end()
            
    # Find start of references or footer or end body
    body_end_idx = len(html_content)
    if refs_match:
        body_end_idx = refs_match.start()
    else:
        footer_match = re.search(r'<div class="footer"', html_content) or re.search(r'</body>', html_content)
        if footer_match:
            body_end_idx = footer_match.start()
            
    raw_body = html_content[abstract_end_idx:body_end_idx].strip()
    
    # Identify H2s and other main content
    # Remove any stray HRs or empty divs
    return page_title, paper_title, abstract_content, raw_body, references


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    page_title, paper_title, abstract, body, references = extract_content(content)
    
    # Clean body - specifically ensure H2s are captured well
    # The body might contain raw text or unclosed tags if we regex sliced it, but simple slicing is usually okay for well formed files
    
    new_content = TEMPLATE_HEAD.format(page_title=page_title, paper_title=paper_title)
    new_content += TEMPLATE_BODY_START.format(abstract=abstract)
    new_content += body
    
    if references:
        new_content += f'\n<div class="references">{references}</div>'
        
    new_content += TEMPLATE_END
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Processed: {file_path}")

def main():
    count = 0
    for root_dir in ROOT_DIRS:
        print(f"Scanning {root_dir}...")
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".html"):
                    full_path = os.path.join(root, file)
                    try:
                        process_file(full_path)
                        count += 1
                    except Exception as e:
                        print(f"Error processing {file}: {e}")
    print(f"Finished. Processed {count} files.")

if __name__ == "__main__":
    main()
