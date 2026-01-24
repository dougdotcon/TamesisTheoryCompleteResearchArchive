import os
import re

ROOT_DIR = r"d:\TamesisTheoryCompleteResearchArchive"
DOI_TEXT = "DOI: 10.5281/zenodo.18357364"
DOI_HTML = f'<div class="doi-badge"><a href="https://doi.org/10.5281/zenodo.18357364" style="text-decoration:none; color:inherit;">{DOI_TEXT}</a></div>'

CSS_INJECTION = """
        .doi-badge {
            font-family: 'Lato', sans-serif;
            font-size: 9px;
            color: #666;
            position: absolute;
            top: 10px;
            right: 20px;
            background: #fdfdfd;
            padding: 2px 5px;
            border: 1px solid #eee;
            border-radius: 3px;
            z-index: 1000;
        }
"""

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if "10.5281/zenodo.18357364" in content:
            print(f"Skipping (DOI exists): {filepath}")
            return

        # 1. Inject CSS
        if "</style>" in content:
            # Inject before the closing style tag
            new_content = content.replace("</style>", CSS_INJECTION + "\n    </style>", 1)
        else:
            # No style tag? Add one in head
            if "</head>" in new_content:
                new_content = content.replace("</head>", f"<style>{CSS_INJECTION}</style></head>", 1)
            else:
                # Malformed HTML, skip CSS injection but try body
                new_content = content

        # 2. Inject HTML Badge
        # Regex to find body tag with potential attributes
        body_pattern = re.compile(r"(<body[^>]*>)", re.IGNORECASE)
        if body_pattern.search(new_content):
            new_content = body_pattern.sub(r"\1" + "\n    " + DOI_HTML, new_content, 1)
        else:
            print(f"Skipping (No body tag): {filepath}")
            return

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    print("Starting DOI Injection...")
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.lower().endswith('.html'):
                filepath = os.path.join(root, file)
                process_file(filepath)
                count += 1
    print(f"Finished processing {count} files.")

if __name__ == "__main__":
    main()
