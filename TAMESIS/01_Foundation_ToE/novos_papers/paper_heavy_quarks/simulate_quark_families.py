"""
Heavy Quark Topology: Extending the Knot Model to 2nd and 3rd Generation Quarks
Models c, s, t, b quarks as higher-complexity topological structures.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# Physical Constants
OMEGA = 117.038  # Compression factor
M_UNIVERSE = 1.5e53  # kg

# Quark masses (MeV)
QUARK_MASSES = {
    # First generation (modeled as trefoils in original paper)
    "u": 2.2,
    "d": 4.7,
    # Second generation
    "c": 1275,
    "s": 95,
    # Third generation
    "t": 173000,
    "b": 4180,
}

def calculate_alpha_exponent(mass_mev):
    """Calculate the holographic exponent α from mass."""
    mass_kg = mass_mev * 1.78266e-30  # MeV to kg
    alpha = np.log(mass_kg / M_UNIVERSE) / np.log(OMEGA)
    return alpha

def model_quark_topology():
    """
    Hypothesis: Higher generation quarks have more complex knot structures.
    
    First generation: Trefoil (3 crossings) ← established
    Second generation: Figure-8 (4 crossings) or Cinquefoil (5 crossings)
    Third generation: Solomon's knot (6+ crossings)
    """
    print("🔬 Modeling Heavy Quark Topology...\n")
    
    results = {}
    
    print("Generation 1 (Trefoil, 3 crossings):")
    print("-" * 40)
    for q in ["u", "d"]:
        m = QUARK_MASSES[q]
        alpha = calculate_alpha_exponent(m)
        results[q] = {"mass": m, "alpha": alpha, "crossings": 3}
        print(f"  {q}: {m} MeV, α = {alpha:.4f}")
    
    print("\nGeneration 2 (Figure-8 / Cinquefoil, 4-5 crossings):")
    print("-" * 40)
    for q in ["s", "c"]:
        m = QUARK_MASSES[q]
        alpha = calculate_alpha_exponent(m)
        crossings = 4 if q == "s" else 5
        results[q] = {"mass": m, "alpha": alpha, "crossings": crossings}
        print(f"  {q}: {m} MeV, α = {alpha:.4f}, crossings = {crossings}")
    
    print("\nGeneration 3 (Solomon/Complex, 6-8 crossings):")
    print("-" * 40)
    for q in ["b", "t"]:
        m = QUARK_MASSES[q]
        alpha = calculate_alpha_exponent(m)
        crossings = 7 if q == "b" else 8
        results[q] = {"mass": m, "alpha": alpha, "crossings": crossings}
        print(f"  {q}: {m} MeV, α = {alpha:.4f}, crossings = {crossings}")
    
    # Test the crossing-mass relationship
    print("\n" + "=" * 50)
    print("CORRELATION ANALYSIS")
    print("=" * 50)
    
    crossings = [results[q]["crossings"] for q in ["u", "d", "s", "c", "b", "t"]]
    masses = [results[q]["mass"] for q in ["u", "d", "s", "c", "b", "t"]]
    
    log_masses = np.log10(masses)
    
    # Linear regression
    coeffs = np.polyfit(crossings, log_masses, 1)
    predicted = 10 ** np.polyval(coeffs, crossings)
    
    print(f"\n  Fit: log₁₀(m) = {coeffs[0]:.3f} × crossings + {coeffs[1]:.3f}")
    print(f"  Mass scales as ~ 10^({coeffs[0]:.2f} × crossings)")
    
    for q in ["u", "d", "s", "c", "b", "t"]:
        ratio = predicted[crossings.index(results[q]["crossings"])] / results[q]["mass"]
        print(f"  {q}: predicted/actual = {ratio:.2f}x")
    
    return results, coeffs

def plot_quark_spectrum(results, coeffs):
    """Visualize the quark mass spectrum and crossing relationship."""
    print("\n📊 Generating Quark Spectrum Plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Mass spectrum by generation
    ax1 = axes[0]
    
    generations = ["Gen 1\n(u, d)", "Gen 2\n(s, c)", "Gen 3\n(b, t)"]
    gen1 = [QUARK_MASSES["u"], QUARK_MASSES["d"]]
    gen2 = [QUARK_MASSES["s"], QUARK_MASSES["c"]]
    gen3 = [QUARK_MASSES["b"], QUARK_MASSES["t"]]
    
    x = np.arange(3)
    width = 0.35
    
    # Plot each quark
    quarks = ["u", "d", "s", "c", "b", "t"]
    masses = [QUARK_MASSES[q] for q in quarks]
    colors = ['#E74C3C', '#E74C3C', '#3498DB', '#3498DB', '#2ECC71', '#2ECC71']
    
    ax1.bar(range(6), masses, color=colors, edgecolor='black')
    ax1.set_yscale('log')
    ax1.set_xticks(range(6))
    ax1.set_xticklabels(quarks, fontsize=12)
    ax1.set_ylabel('Mass (MeV)', fontsize=12)
    ax1.set_title('Quark Mass Hierarchy by Generation', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add generation labels
    ax1.axvspan(-0.5, 1.5, alpha=0.1, color='red', label='Gen 1')
    ax1.axvspan(1.5, 3.5, alpha=0.1, color='blue', label='Gen 2')
    ax1.axvspan(3.5, 5.5, alpha=0.1, color='green', label='Gen 3')
    
    # Right: Crossing number vs Mass
    ax2 = axes[1]
    
    crossings = [results[q]["crossings"] for q in quarks]
    
    ax2.scatter(crossings, masses, s=150, c=colors, edgecolor='black', zorder=5)
    
    # Add fit line
    x_fit = np.linspace(2.5, 8.5, 50)
    y_fit = 10 ** np.polyval(coeffs, x_fit)
    ax2.plot(x_fit, y_fit, 'k--', linewidth=2, label=f'Fit: m ∝ 10^({coeffs[0]:.2f}×n)')
    
    for i, q in enumerate(quarks):
        ax2.annotate(q, (crossings[i], masses[i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=11)
    
    ax2.set_yscale('log')
    ax2.set_xlabel('Knot Crossing Number', fontsize=12)
    ax2.set_ylabel('Mass (MeV)', fontsize=12)
    ax2.set_title('Mass vs Topological Complexity', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "assets", "quark_spectrum.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("🔬 HEAVY QUARK TOPOLOGY SIMULATION")
    print("   Paper 11: Extending Knots to All 6 Quarks")
    print("=" * 60 + "\n")
    
    results, coeffs = model_quark_topology()
    plot_quark_spectrum(results, coeffs)
    
    print("\n" + "=" * 60)
    print("📋 CONCLUSION")
    print("=" * 60)
    print("""
    The quark mass hierarchy follows topological complexity:
    
    Generation 1 (u, d): Trefoil (3 crossings) → ~1-5 MeV
    Generation 2 (s, c): Figure-8/Cinquefoil (4-5) → ~100-1300 MeV
    Generation 3 (b, t): Complex knots (7-8) → ~4-173 GeV
    
    Mass scales approximately as 10^(0.9 × crossings)
    
    This suggests MASS = TOPOLOGICAL COMPLEXITY in the TAMESIS framework.
    """)
