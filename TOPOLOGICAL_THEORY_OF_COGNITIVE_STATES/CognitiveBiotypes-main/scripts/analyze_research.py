import os
import glob

def analyze_files(directory):
    # Defined keywords strictly for Precision Psychiatry research
    keywords = {
        "Mechanisms": ["cognitive control", "dlpfc", "dacc", "circuit", "connectivity", "neural", "testosterone"],
        "Concepts": ["biotype", "precision psychiatry", "stratification", "individualized", "biomarker"],
        "Treatments": ["tms", "medication", "cognitive", "therapy", "yoga", "mindfulness"],
        "Social": ["stigma", "quality of life", "patient"]
    }

    # Find all text and markdown files
    files = glob.glob(os.path.join(directory, "**", "*.txt"), recursive=True) + \
            glob.glob(os.path.join(directory, "**", "*.md"), recursive=True)

    print(f"Analyzing {len(files)} research files for Psychiatric concepts...\n")
    
    summary = {}

    for filepath in files:
        # Skip the 'projeto_toe' directory entirely to avoid off-topic physics files
        if "projeto_toe" in filepath:
            continue
            
        filename = os.path.basename(filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            file_hits = []
            for category, terms in keywords.items():
                hits = [term for term in terms if term in content]
                if hits:
                    unique_hits = sorted(list(set(hits)))
                    file_hits.append(f"{category}: {', '.join(unique_hits)}")
            
            if file_hits:
                summary[filename] = file_hits
        except Exception as e:
            # Silently skip files that can't be read
            pass

    # Output Report
    for filename, hits in summary.items():
        print(f"FILE: {filename}")
        for hit in hits:
            print(f"  - {hit}")
        print("-" * 40)

if __name__ == "__main__":
    research_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "research")
    
    if os.path.exists(research_dir):
        analyze_files(research_dir)
    else:
        print(f"Research directory not found at: {research_dir}")
