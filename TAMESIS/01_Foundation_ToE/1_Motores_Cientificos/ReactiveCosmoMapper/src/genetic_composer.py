"""
Genetic Composer - The Ultimate Musician
Interactive Terminal App for composing music using Musical DNA Fusion.
"""
import requests
import json
import os
import sys

# API Configuration
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "xiaomi/mimo-v2-flash:free"

# ═══════════════════════════════════════════════════════════════════
# MUSICAL GENOMES (The DNA Fragments)
# ═══════════════════════════════════════════════════════════════════

GENOMES = {
    "bach": {
        "name": "Johann Sebastian Bach",
        "era": "Baroque (1685-1750)",
        "dna": "Counterpoint, Fugue structures, Mathematical symmetry, Multiple independent voices, Sequential patterns, Harmonic stability.",
        "style": "rigorous, logical, intellectual, architectural",
        "analogy": "The Kernel of music - foundational structure."
    },
    "mozart": {
        "name": "Wolfgang Amadeus Mozart",
        "era": "Classical (1756-1791)",
        "dna": "Sonata form, Short memorable phrases, Clear harmonic language, Light-to-shadow emotional dynamics, Melody-centric, Elegant simplicity.",
        "style": "clear, narrative, balanced, natural, empathetic",
        "analogy": "The Perfect Interface - accessible beauty."
    },
    "chopin": {
        "name": "Frédéric Chopin",
        "era": "Romantic (1810-1849)",
        "dna": "Chromatic harmony, Rubato (flexible tempo), Liquid arpeggios, Cantabile melodies, Psychological tension, Folk influences (Mazurka, Polonaise).",
        "style": "emotional, intimate, lyrical, yearning, free",
        "analogy": "The Emotional Engine - raw feeling compressed into notes."
    },
    "beethoven": {
        "name": "Ludwig van Beethoven",
        "era": "Classical/Romantic (1770-1827)",
        "dna": "Thematic development, Conflict and resolution, Dramatic arcs, Motivic cells, Sforzando accents, Heroic narratives.",
        "style": "powerful, dramatic, evolutionary, heroic, conflicted",
        "analogy": "The Conflict Driver - struggle and triumph."
    },
    "debussy": {
        "name": "Claude Debussy",
        "era": "Impressionist (1862-1918)",
        "dna": "Whole-tone scales, Parallel chords, Modal ambiguity, Atmospheric textures, Color over function, Suspended time.",
        "style": "ethereal, colorful, ambiguous, dreamy, visual",
        "analogy": "The Graphics Renderer - painting with sound."
    }
}

# ═══════════════════════════════════════════════════════════════════
# TAMESIS CONSTANTS
# ═══════════════════════════════════════════════════════════════════

TARDIS_CONTEXT = """
Additionally, all compositions must be anchored to the TAMESIS Harmonic Theory:
- Base Frequency: 117 Hz (Gamma - The Universal Tension).
- Preferred Key: A Minor (Am) or A Major.
- Core Chord: AAGOOCH (Am9 no5) = A, G, C, B.
- Avoid excessive resolution; maintain cosmic tension.
"""

def display_banner():
    print("\n" + "═" * 60)
    print("🧬 GENETIC COMPOSER - The Ultimate Musician 🧬")
    print("   Fusing Musical DNA with TAMESIS Harmony")
    print("═" * 60)

def display_menu():
    print("\nAvailable Genomes:")
    for i, (key, genome) in enumerate(GENOMES.items(), 1):
        print(f"  [{i}] {genome['name']} ({genome['era']})")
        print(f"      → {genome['analogy']}")
    print()

def get_user_choice(prompt, max_val):
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= max_val:
                return choice
            else:
                print(f"  ⚠️ Please enter a number between 1 and {max_val}.")
        except ValueError:
            print("  ⚠️ Invalid input. Please enter a number.")

def compose_with_fusion(primary_genome, secondary_genome):
    """Send the fusion request to the LLM."""
    print("\n🎹 Connecting to the Cosmic Composer (OpenRouter)...")
    
    prompt = f"""
You are the greatest composer in history, a fusion of masters.

Your PRIMARY influence is: **{primary_genome['name']}**
- Era: {primary_genome['era']}
- Musical DNA: {primary_genome['dna']}
- Style Keywords: {primary_genome['style']}

Your SECONDARY influence (add flavor, not dominate) is: **{secondary_genome['name']}**
- DNA: {secondary_genome['dna']}

{TARDIS_CONTEXT}

---
## YOUR TASK

Compose a **complete short Piano piece** (16-32 bars).
Output in **ABC Notation** format.

After the ABC code, provide a **PERFORMANCE GUIDE** in plain text explaining:
1. How to play this piece (tempo, dynamics, rubato usage).
2. Which sections reflect the PRIMARY genome.
3. Which sections reflect the SECONDARY genome.

Format your response EXACTLY like this:
=== ABC START ===
(your ABC notation here)
=== ABC END ===

=== PERFORMANCE GUIDE ===
(your text guide here)
=== END GUIDE ===
"""

    try:
        response = requests.post(
            url=API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://TAMESIS-project.com",
                "X-Title": "Genetic Composer"
            },
            data=json.dumps({
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a master music composition engine. Output only structured ABC Notation and performance guides."},
                    {"role": "user", "content": prompt}
                ]
            }),
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print("✅ Composition Received!")
            return content
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def parse_response(raw_response):
    """Extract ABC and Guide from structured response."""
    abc_code = ""
    guide = ""
    
    if "=== ABC START ===" in raw_response and "=== ABC END ===" in raw_response:
        abc_code = raw_response.split("=== ABC START ===")[1].split("=== ABC END ===")[0].strip()
    else:
        # Fallback: assume everything before "PERFORMANCE" is ABC
        abc_code = raw_response.split("PERFORMANCE")[0].replace("```abc", "").replace("```", "").strip()
    
    if "=== PERFORMANCE GUIDE ===" in raw_response:
        guide = raw_response.split("=== PERFORMANCE GUIDE ===")[1].split("=== END GUIDE ===")[0].strip()
    elif "PERFORMANCE GUIDE" in raw_response:
        guide = raw_response.split("PERFORMANCE GUIDE")[1].strip()
    
    return abc_code, guide

def generate_html(abc_code, guide, primary, secondary):
    """Generate the complete HTML output."""
    html_template = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <title>Partitura Genética: {primary['name']} × {secondary['name']}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/abcjs/6.2.2/abcjs-basic-min.js"></script>
    <style>
        :root {{ --bg: #0a0a12; --fg: #e0e0f0; --accent: #a0a0ff; --paper: #fff; }}
        body {{ font-family: 'Georgia', serif; background: var(--bg); color: var(--fg); padding: 20px; }}
        h1 {{ color: var(--accent); text-align: center; letter-spacing: 3px; }}
        .subtitle {{ text-align: center; font-style: italic; margin-bottom: 30px; }}
        .paper {{ background: var(--paper); padding: 30px; border-radius: 8px; max-width: 900px; margin: 0 auto 30px auto; color: #000; }}
        .guide {{ background: #1a1a2e; padding: 25px; border-radius: 8px; max-width: 900px; margin: 0 auto; border-left: 4px solid var(--accent); }}
        .guide h2 {{ color: var(--accent); margin-top: 0; }}
        .guide p {{ line-height: 1.8; white-space: pre-wrap; }}
        .dna {{ display: flex; justify-content: center; gap: 20px; margin-bottom: 20px; }}
        .genome-tag {{ background: #333; padding: 8px 15px; border-radius: 20px; font-size: 0.9em; }}
        .genome-tag.primary {{ background: #4a90d9; color: #fff; }}
        .genome-tag.secondary {{ background: #9b59b6; color: #fff; }}
    </style>
</head>
<body>
    <h1>🧬 Partitura Genética</h1>
    <p class="subtitle">Uma fusão de {primary['name']} e {secondary['name']}, ancorada na Harmonia TAMESIS (117 Hz)</p>

    <div class="dna">
        <span class="genome-tag primary">Primary: {primary['name']}</span>
        <span class="genome-tag secondary">Secondary: {secondary['name']}</span>
    </div>

    <div id="paper" class="paper"></div>

    <div class="guide">
        <h2>📖 Guia de Performance</h2>
        <p>{guide}</p>
    </div>

    <div class="guide" style="margin-top: 20px;">
        <h2>🧬 Análise Genética</h2>
        <p><strong>Genoma Primário ({primary['name']}):</strong> {primary['dna']}</p>
        <p><strong>Genoma Secundário ({secondary['name']}):</strong> {secondary['dna']}</p>
        <p><strong>Âncora TAMESIS:</strong> Frequência base 117 Hz. Tensão cósmica preservada via progressões Am9.</p>
    </div>

    <script type="text/javascript">
        var abc = `{abc_code}`;
        ABCJS.renderAbc("paper", abc, {{ responsive: "resize" }});
    </script>
</body>
</html>
"""
    return html_template

def main():
    display_banner()
    display_menu()
    
    genome_keys = list(GENOMES.keys())
    
    print("Step 1: Choose your PRIMARY genome (the foundation).")
    primary_idx = get_user_choice("  Enter number [1-5]: ", 5)
    primary_key = genome_keys[primary_idx - 1]
    primary = GENOMES[primary_key]
    print(f"  → Selected: {primary['name']}")
    
    print("\nStep 2: Choose your SECONDARY genome (the flavor).")
    secondary_idx = get_user_choice("  Enter number [1-5]: ", 5)
    secondary_key = genome_keys[secondary_idx - 1]
    secondary = GENOMES[secondary_key]
    print(f"  → Selected: {secondary['name']}")
    
    print(f"\n🧪 Synthesizing: {primary['name']} × {secondary['name']}...")
    
    raw_response = compose_with_fusion(primary, secondary)
    
    if raw_response:
        abc_code, guide = parse_response(raw_response)
        
        if not abc_code:
            print("⚠️ Could not extract ABC. Using fallback.")
            abc_code = f"X:1\\nT:{primary['name']} x {secondary['name']} Fusion\\nM:4/4\\nL:1/8\\nK:Am\\n|: A2 E2 c2 B2 | G2 E2 D2 C2 :|"
        
        if not guide:
            guide = "Performance instructions were not generated. Play with expression and follow your intuition."
        
        html_content = generate_html(abc_code, guide, primary, secondary)
        
        output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "DECODIFICANDO", "06_LINGUISTICA")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "partitura_genetica.html")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\n✅ Success! Your Genetic Score has been created.")
        print(f"   📄 File: {output_path}")
        print(f"   🎹 Open the HTML in your browser to view and play.")
    else:
        print("❌ Failed to generate composition. Please check your API key.")

if __name__ == "__main__":
    main()
