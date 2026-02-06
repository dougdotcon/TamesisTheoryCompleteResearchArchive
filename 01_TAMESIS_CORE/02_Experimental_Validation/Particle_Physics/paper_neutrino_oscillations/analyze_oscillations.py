"""
Neutrino Oscillations: Do They Follow from Unknot Topology?
Explores neutrino mixing in the TAMESIS framework.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# Neutrino mixing parameters (experimental)
THETA_12 = 33.44  # degrees (solar)
THETA_23 = 49.2   # degrees (atmospheric)
THETA_13 = 8.57   # degrees (reactor)
DM21_SQ = 7.42e-5  # eV² (solar)
DM32_SQ = 2.51e-3  # eV² (atmospheric)

def analyze_neutrino_oscillations():
    """
    Analyze neutrino oscillations in TAMESIS framework.
    """
    print("🔬 Analyzing Neutrino Oscillations...\n")
    
    print("=" * 50)
    print("EXPERIMENTAL FACTS")
    print("=" * 50)
    print(f"""
    Neutrino mixing angles:
      θ₁₂ = {THETA_12}° (solar)
      θ₂₃ = {THETA_23}° (atmospheric)
      θ₁₃ = {THETA_13}° (reactor)
      
    Mass-squared differences:
      Δm²₂₁ = {DM21_SQ:.2e} eV²
      Δm²₃₂ = {DM32_SQ:.2e} eV²
      
    Neutrinos oscillate between flavors!
    This proves they have MASS.
    """)
    
    print("=" * 50)
    print("STANDARD EXPLANATION")
    print("=" * 50)
    print("""
    Mass eigenstates ≠ Flavor eigenstates:
    
    |ν_e⟩ = U_e1|ν_1⟩ + U_e2|ν_2⟩ + U_e3|ν_3⟩
    
    The PMNS matrix U mixes mass and flavor.
    WHY these angles? Unknown.
    """)
    
    print("=" * 50)
    print("TAMESIS INTERPRETATION")
    print("=" * 50)
    print("""
    Neutrinos are "unknots" (genus 0, trivial topology):
    
    1. THREE UNKNOTS, SLIGHTLY DIFFERENT
       - ν₁, ν₂, ν₃ differ by tiny deformations
       - Not crossings, but "twist" or "writhe"
       
    2. FLAVOR = BOUNDARY COUPLING
       - How the unknot couples to e, μ, τ leptons
       - Different couplings = different flavors
       
    3. OSCILLATIONS = PHASE EVOLUTION
       - The tiny mass differences cause phase differences
       - Detected as flavor transitions
       
    4. MIXING ANGLES
       - May come from geometry of unknot deformations
       - θ₁₂ ≈ 33° ~ arctan(1/√2)? (tribimaximal hint)
       - Connection to algebra (group theory)?
    """)
    
    # Check tribimaximal pattern
    tribimaximal = np.degrees(np.arctan(1/np.sqrt(2)))
    print(f"\n  Tribimaximal angle: {tribimaximal:.1f}°")
    print(f"  Observed θ₁₂: {THETA_12}°")
    print(f"  Deviation: {THETA_12 - tribimaximal:.1f}°")
    
    return {
        "theta_12": THETA_12,
        "theta_23": THETA_23,
        "theta_13": THETA_13,
        "tribimaximal_hint": tribimaximal
    }

def plot_oscillations():
    """Visualize neutrino oscillations."""
    print("\n📊 Generating Oscillation Plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Oscillation probability
    ax1 = axes[0]
    
    L_over_E = np.linspace(0, 1000, 500)  # km/GeV
    
    # Simplified two-flavor oscillation
    dm2 = 2.5e-3  # eV²
    theta = np.radians(45)
    
    P_survival = 1 - np.sin(2*theta)**2 * np.sin(1.27 * dm2 * L_over_E)**2
    P_appearance = np.sin(2*theta)**2 * np.sin(1.27 * dm2 * L_over_E)**2
    
    ax1.plot(L_over_E, P_survival, 'b-', linewidth=2, label='P(νμ → νμ) survival')
    ax1.plot(L_over_E, P_appearance, 'r-', linewidth=2, label='P(νμ → ντ) appearance')
    
    ax1.set_xlabel('L/E (km/GeV)', fontsize=12)
    ax1.set_ylabel('Probability', fontsize=12)
    ax1.set_title('Neutrino Oscillation Probability\n(Atmospheric, 2-flavor approx)', 
                 fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1.1])
    
    # Right: Mixing angles in triangle
    ax2 = axes[1]
    
    angles = [THETA_12, THETA_23, THETA_13]
    labels = ['θ₁₂\n(solar)', 'θ₂₃\n(atmos)', 'θ₁₃\n(reactor)']
    colors = ['gold', 'blue', 'green']
    
    bars = ax2.bar(labels, angles, color=colors, edgecolor='black')
    
    ax2.axhline(45, color='red', linestyle='--', alpha=0.5, label='Maximal (45°)')
    ax2.axhline(35.26, color='orange', linestyle=':', alpha=0.5, 
               label='Tribimaximal θ₁₂')
    
    ax2.set_ylabel('Mixing Angle (degrees)', fontsize=12)
    ax2.set_title('PMNS Mixing Angles\nWhy These Values?', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim([0, 60])
    
    plt.suptitle('Neutrino Oscillations: Unknots with Tiny Deformations?', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "assets", "neutrino_oscillations.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("🔬 NEUTRINO OSCILLATION ANALYSIS")
    print("   Paper 31: Unknots and Flavor Mixing")
    print("=" * 60 + "\n")
    
    results = analyze_neutrino_oscillations()
    plot_oscillations()
    
    print("\n" + "=" * 60)
    print("📋 CONCLUSION")
    print("=" * 60)
    print("""
    Neutrino oscillations in TAMESIS:
    
    1. Neutrinos are unknots (trivial topology)
    2. Three mass states differ by tiny deformations
    3. Flavor mixing = how unknots couple to charged leptons
    4. Mixing angles may have geometric origin
    
    θ₁₂ ≈ tribimaximal suggests underlying symmetry.
    """)
