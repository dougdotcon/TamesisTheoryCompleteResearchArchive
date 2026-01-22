"""
Dark Matter Candidates in TARDIS: Gravitinos, Axions, or Nothing?
Analyzes whether any BSM particles are predicted/needed.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

def analyze_dark_candidates():
    """
    Analyze dark matter candidates in TARDIS framework.
    """
    print("🌑 Analyzing Dark Matter Candidates...\n")
    
    print("=" * 50)
    print("STANDARD DARK MATTER CANDIDATES")
    print("=" * 50)
    print("""
    1. WIMPs (Weakly Interacting Massive Particles)
       - Mass: ~10-1000 GeV
       - Interaction: Weak force
       - Status: NOT FOUND at LHC, direct detection null
       
    2. Axions
       - Mass: ~10^-6 - 10^-3 eV
       - Origin: Strong CP problem solution
       - Status: Searches ongoing
       
    3. Gravitinos
       - Mass: ~keV - TeV
       - Origin: SUSY graviton partner
       - Status: Requires SUSY (not found)
       
    4. Primordial Black Holes
       - Mass: wide range
       - Origin: Early universe
       - Status: Constrained but possible
    """)
    
    print("=" * 50)
    print("TARDIS PERSPECTIVE")
    print("=" * 50)
    print("""
    In Entropic Gravity:
    
    1. NO WIMP NEEDED
       - Rotation curves explained without DM
       - Galaxy dynamics = entropic effects
       
    2. AXIONS: MAYBE
       - Still solve strong CP problem
       - Not for dark matter, but for θ-parameter
       - INDEPENDENT of TARDIS
       
    3. GRAVITINOS: NO
       - Require SUSY, which is not needed
       
    4. PBHs: INTERESTING
       - If we're inside a BH, PBHs = child universes
       - Not "dark matter" but real objects
       
    5. STERILE NEUTRINOS: MAYBE
       - Neutrinos are "unknots" with minimal mass
       - Sterile neutrino = different knot?
       - Could exist but not as DM
    """)
    
    return {
        "wimp_needed": False,
        "axion_status": "independent of TARDIS",
        "gravitino_status": "not needed (no SUSY)",
        "pbh_interpretation": "child universes",
        "conclusion": "No dark matter particle required"
    }

def plot_dm_exclusion():
    """Plot dark matter candidate status."""
    print("\n📊 Generating DM Candidates Plot...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    candidates = ['WIMPs', 'Axions', 'Gravitinos', 'PBHs', 'Sterile ν']
    needed_in_tardis = [0, 0.5, 0, 0.3, 0.3]  # 0=No, 1=Yes, 0.5=Maybe
    status_sm = [1, 1, 1, 0.5, 0.7]  # Typical SM+DM need
    
    x = np.arange(len(candidates))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, status_sm, width, label='Standard DM Need', color='gray', alpha=0.7)
    bars2 = ax.bar(x + width/2, needed_in_tardis, width, label='TARDIS Need', color='green', alpha=0.7)
    
    ax.set_ylabel('Required/Predicted', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(candidates, fontsize=11)
    ax.set_title('Dark Matter Candidates: Standard vs TARDIS', fontsize=14, fontweight='bold')
    ax.legend()
    ax.set_ylim([0, 1.3])
    ax.grid(True, alpha=0.3, axis='y')
    
    # Status labels
    ax.text(0, 0.05, 'NOT\nFOUND', ha='center', fontsize=8, color='white')
    ax.text(1, 0.55, 'Independent', ha='center', fontsize=8)
    ax.text(2, 0.05, 'No SUSY', ha='center', fontsize=8, color='white')
    ax.text(3, 0.35, 'Child\nUniverses', ha='center', fontsize=8)
    ax.text(4, 0.35, 'Different\nKnot?', ha='center', fontsize=8)
    
    plt.tight_layout()
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "assets", "dm_candidates.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("🌑 DARK MATTER CANDIDATES ANALYSIS")
    print("   Paper 22: Gravitinos, Axions, or Nothing?")
    print("=" * 60 + "\n")
    
    results = analyze_dark_candidates()
    plot_dm_exclusion()
    
    print("\n" + "=" * 60)
    print("📋 CONCLUSION")
    print("=" * 60)
    print("""
    TARDIS does NOT require dark matter particles.
    
    • WIMPs: Not needed, not found → CONSISTENT
    • Axions: Independent problem (strong CP), not DM
    • Gravitinos: Require SUSY, not needed
    • PBHs: Reinterpreted as child universes
    
    The "dark matter" is entropic gravity, not a particle.
    """)
