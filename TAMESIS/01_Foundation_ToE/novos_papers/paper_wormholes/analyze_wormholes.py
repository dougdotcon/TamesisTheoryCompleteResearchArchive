"""
Macroscopic Wormholes: If Leptons Are Wormholes, Can We Make Big Ones?
Explores the possibility of traversable wormholes in TAMESIS.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# Constants
G = 6.674e-11  # m³/kg/s²
c = 3e8  # m/s
hbar = 1.054e-34  # J·s
l_P = 1.616e-35  # m (Planck length)

def analyze_macroscopic_wormholes():
    """
    Analyze the possibility of macroscopic wormholes in TAMESIS.
    """
    print("🕳️ Analyzing Macroscopic Wormholes...\n")
    
    print("=" * 50)
    print("LEPTONS AS MICROSCOPIC WORMHOLES")
    print("=" * 50)
    print("""
    In TAMESIS, charged leptons (e, μ, τ) are:
    - Genus-1 topological defects
    - Wormhole-like structures connecting boundary to interior
    - Size: ~Planck scale (~10^-35 m)
    
    These are STABLE because:
    - Topologically protected
    - Cannot "untie" without infinite energy
    - Holographically anchored
    """)
    
    print("=" * 50)
    print("SCALING TO MACROSCOPIC")
    print("=" * 50)
    print("""
    To make a macroscopic (human-traversable) wormhole:
    
    1. SIZE REQUIREMENT
       - Throat radius: r > 1 meter
       - Classical GR requires: "exotic matter" (ρ < 0)
       
    2. ENERGY REQUIREMENT (Morris-Thorne)
       - E ~ c^4 × r / G
       - For r = 1m: E ~ 10^44 J (mass of Jupiter!)
       
    3. STABILITY REQUIREMENT
       - Need to prevent collapse
       - Casimir effect? Quantum fluctuations?
    """)
    
    # Calculate energy requirements
    r_throat = 1.0  # meter
    E_required = c**4 * r_throat / G
    M_equivalent = E_required / c**2
    M_jupiter = 1.9e27  # kg
    
    print(f"\n  Throat radius: {r_throat} m")
    print(f"  Energy required: {E_required:.2e} J")
    print(f"  Mass equivalent: {M_equivalent:.2e} kg")
    print(f"  = {M_equivalent/M_jupiter:.1f} Jupiter masses")
    
    print("\n" + "=" * 50)
    print("TAMESIS PERSPECTIVE")
    print("=" * 50)
    print("""
    In the holographic framework:
    
    1. METRIC ENGINEERING
       - We derived warp drive from γ manipulation
       - Wormholes = localized γ → 0 regions
       
    2. THE CHALLENGE
       - Creating γ < 0 (negative compression) is hard
       - May require quantum coherence on macro scale
       
    3. POSSIBILITY
       - NOT forbidden by TAMESIS
       - Requires technology beyond current capability
       - Energy ~ planetary mass
    """)
    
    return {
        "r_throat_m": r_throat,
        "energy_J": E_required,
        "mass_kg": M_equivalent,
        "feasible": "theoretically possible, practically difficult"
    }

def plot_wormhole_schematic():
    """Visualize wormhole structure."""
    print("\n📊 Generating Wormhole Schematic...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Microscopic (lepton)
    ax1 = axes[0]
    
    theta = np.linspace(0, 2*np.pi, 100)
    
    # Draw torus (wormhole topology)
    R = 1  # Major radius
    r = 0.3  # Minor radius
    
    for phi in np.linspace(0, 2*np.pi, 20):
        x = (R + r*np.cos(phi)) * np.cos(theta)
        y = (R + r*np.cos(phi)) * np.sin(theta) * 0.3  # Flatten for side view
        ax1.plot(x, y + r*np.sin(phi), 'b-', alpha=0.3)
    
    # Draw throat
    ax1.annotate('', xy=(0, -0.3), xytext=(0, 0.3),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax1.text(0.15, 0, 'Throat\n~10⁻³⁵ m', fontsize=10, color='red')
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-0.8, 0.8)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Microscopic Wormhole (Lepton)\nPlanck Scale', fontsize=12, fontweight='bold')
    
    # Right: Macroscopic (hypothetical)
    ax2 = axes[1]
    
    # Draw embedding diagram
    x = np.linspace(-3, 3, 100)
    y_upper = 1 + 0.5 * np.cosh(x/2)
    y_lower = -1 - 0.5 * np.cosh(x/2)
    
    ax2.fill_between(x, y_upper, 4, color='lightblue', alpha=0.3)
    ax2.fill_between(x, y_lower, -4, color='lightblue', alpha=0.3)
    
    ax2.plot(x, y_upper, 'b-', linewidth=2)
    ax2.plot(x, y_lower, 'b-', linewidth=2)
    
    # Connect at throat
    throat_x = np.array([0, 0])
    throat_y = np.array([y_upper[50], y_lower[50]])
    ax2.plot([0, 0], [1.5, -1.5], 'r-', linewidth=3, label='Throat (r ~ 1m)')
    
    ax2.annotate('Universe A', xy=(-2, 3), fontsize=11)
    ax2.annotate('Universe B', xy=(-2, -3.5), fontsize=11)
    ax2.annotate('Energy ~\nJupiter mass', xy=(1, 0), fontsize=10, color='red',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    ax2.set_xlim(-3.5, 3.5)
    ax2.set_ylim(-4, 4)
    ax2.axis('off')
    ax2.set_title('Macroscopic Wormhole (Hypothetical)\nHuman Traversable', fontsize=12, fontweight='bold')
    
    plt.suptitle('Wormhole Scaling: From Leptons to Spacecraft', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "assets", "wormhole_scaling.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("🕳️ MACROSCOPIC WORMHOLE ANALYSIS")
    print("   Paper 23: Can We Build Traversable Wormholes?")
    print("=" * 60 + "\n")
    
    results = analyze_macroscopic_wormholes()
    plot_wormhole_schematic()
    
    print("\n" + "=" * 60)
    print("📋 CONCLUSION")
    print("=" * 60)
    print("""
    Macroscopic wormholes are NOT FORBIDDEN by TAMESIS.
    
    However:
    • Energy requirement: ~Jupiter mass (~10^44 J)
    • Technology: Far beyond current capability
    • Stability: Requires unknown metric engineering
    
    Leptons PROVE the topology exists at Planck scale.
    Scaling up is an engineering problem, not a physics one.
    """)
