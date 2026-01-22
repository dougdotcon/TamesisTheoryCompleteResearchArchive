"""
Origin of Omega: Attempting to Derive Ω = 117.038 from First Principles
This is exploratory research to find the fundamental origin of the compression factor.
"""
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
import os

# The target value
OMEGA = 117.038

def explore_mathematical_origins():
    """
    Attempt to find mathematical relationships that produce Ω = 117.038.
    """
    print("🔢 Exploring Mathematical Origins of Ω = 117.038...\n")
    
    results = []
    
    # ═══════════════════════════════════════════════════════════════
    # Approach 1: Prime Factorization
    # ═══════════════════════════════════════════════════════════════
    print("━" * 50)
    print("Approach 1: Prime Factorization")
    print("━" * 50)
    
    # 117 = 9 × 13 = 3² × 13
    print(f"  117 = 3² × 13")
    print(f"  3 = first odd prime, 13 = 6th prime")
    
    # Check approximation
    approx_1 = 3**2 * 13
    error_1 = abs(approx_1 - OMEGA) / OMEGA * 100
    print(f"  3² × 13 = {approx_1}, error from Ω: {error_1:.3f}%")
    results.append(("3² × 13", approx_1, error_1))
    
    # ═══════════════════════════════════════════════════════════════
    # Approach 2: Fine Structure Constant Relationship
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'━' * 50}")
    print("Approach 2: Relationship to α (Fine Structure)")
    print("━" * 50)
    
    alpha_inv = 137.035999  # 1/α
    ratio = alpha_inv / OMEGA
    print(f"  α⁻¹ / Ω = {ratio:.6f} ≈ 1.171")
    print(f"  Note: Ω^1.033 ≈ α⁻¹")
    
    # Ω = α⁻¹ / x => x = α⁻¹ / Ω = 1.171
    # Interesting: 1.171 ≈ γ_μ (muon exponent)!
    gamma_mu = 1.1195
    print(f"  Remarkably: α⁻¹/Ω = {ratio:.4f} ≈ γ_μ = {gamma_mu}")
    error_2 = abs(ratio - gamma_mu) / gamma_mu * 100
    print(f"  Error: {error_2:.2f}%")
    results.append(("α⁻¹ / γ_μ", alpha_inv / gamma_mu, abs(alpha_inv/gamma_mu - OMEGA)/OMEGA*100))
    
    # ═══════════════════════════════════════════════════════════════
    # Approach 3: Euler's Number and Pi
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'━' * 50}")
    print("Approach 3: Transcendental Numbers")
    print("━" * 50)
    
    e = np.e
    pi = np.pi
    
    candidates = [
        ("π² × e × 4", pi**2 * e * 4, None),
        ("e^(π + 1)", np.exp(pi + 1), None),
        ("(π × e)³ / 13", (pi * e)**3 / 13, None),
        ("4π² + 77", 4*pi**2 + 77, None),
        ("100 + e × 2π", 100 + e * 2 * pi, None),
    ]
    
    for name, val, _ in candidates:
        error = abs(val - OMEGA) / OMEGA * 100
        print(f"  {name} = {val:.4f}, error: {error:.2f}%")
        results.append((name, val, error))
    
    # ═══════════════════════════════════════════════════════════════
    # Approach 4: Black Hole Parent Properties
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'━' * 50}")
    print("Approach 4: Parent Black Hole Topology")
    print("━" * 50)
    
    # If our universe is a BH in a parent universe, Ω could relate to
    # the dimensionality or topology of the parent.
    
    # Hypothesis: Ω emerges from the ratio of parent to child Planck areas
    # In AdS/CFT, the central charge c is related to dimensions
    
    # For AdS₅/CFT₄: c = π³ N² / 2 where N is the gauge rank
    # If N relates to our Ω...
    
    # Alternative: Holographic ratio
    # Ω = (R_universe / l_P)^β for some β
    
    R_universe = 4.4e26  # m
    l_P = 1.616e-35  # m
    ratio_universe = R_universe / l_P
    
    # log(ratio) / log(Ω) gives how many "Ω-scales" fit
    n_scales = np.log(ratio_universe) / np.log(OMEGA)
    print(f"  R_universe / l_P = {ratio_universe:.3e}")
    print(f"  ln(R/l_P) / ln(Ω) = {n_scales:.2f} levels")
    print(f"  This suggests ~30 holographic levels!")
    
    # ═══════════════════════════════════════════════════════════════
    # Approach 5: Standard Model Gauge Groups
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'━' * 50}")
    print("Approach 5: Standard Model Gauge Groups")
    print("━" * 50)
    
    # SU(3) × SU(2) × U(1) → 8 + 3 + 1 = 12 generators
    generators_SM = 8 + 3 + 1
    print(f"  SM generators: {generators_SM}")
    
    # 117 / 12 = 9.75 ≈ 10
    ratio_gen = 117 / generators_SM
    print(f"  117 / 12 = {ratio_gen:.2f}")
    
    # Dimensions of SM fermion representations
    # Each generation: (3,2,1/6) + (3,1,2/3) + (3,1,-1/3) + (1,2,-1/2) + (1,1,-1)
    # = 6 + 3 + 3 + 2 + 1 = 15 (×2 for L/R) → 30 Weyl spinors per generation
    # 3 generations → 90 fermionic degrees of freedom
    print(f"  Fermionic DOF (3 gen): 90")
    print(f"  117 - 90 = 27 = 3³ (gauge bosons + Higgs?)")
    
    # Deep connection?
    print(f"\n  Possible: Ω = 90 + 27 = Fermions + Bosons?")
    
    # ═══════════════════════════════════════════════════════════════
    # Approach 6: The "Magical" Formula Attempt
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'━' * 50}")
    print("Approach 6: Numerical Coincidences")
    print("━" * 50)
    
    # Try: Ω = 2^a × 3^b × ... or simple formula
    best_matches = []
    
    # Search space: powers of small primes and transcendentals
    for a in range(-5, 10):
        for b in range(-5, 10):
            for c in range(-5, 5):
                val = (2**a) * (3**b) * (pi**c)
                if 110 < val < 125:
                    error = abs(val - OMEGA) / OMEGA * 100
                    if error < 1:
                        best_matches.append((f"2^{a} × 3^{b} × π^{c}", val, error))
    
    if best_matches:
        best_matches.sort(key=lambda x: x[2])
        for name, val, err in best_matches[:3]:
            print(f"  {name} = {val:.4f}, error: {err:.4f}%")
            results.append((name, val, err))
    
    # ═══════════════════════════════════════════════════════════════
    # Final Analysis
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'━' * 50}")
    print("CONCLUSION: Best Candidate Origins")
    print("━" * 50)
    
    results_sorted = sorted(results, key=lambda x: x[2])[:5]
    for name, val, err in results_sorted:
        print(f"  {name}: {val:.4f} (error: {err:.4f}%)")
    
    return results_sorted

def plot_omega_relationships():
    """Visualize the relationship between Ω and other fundamental quantities."""
    print("\n📊 Generating Omega Relationships Plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Ω in context of other constants
    ax1 = axes[0]
    
    constants = [
        ("Ω", OMEGA, "#E74C3C"),
        ("α⁻¹", 137.04, "#3498DB"),
        ("π²×12", np.pi**2 * 12, "#2ECC71"),
        ("e⁴", np.e**4, "#9B59B6"),
        ("3²×13", 117, "#F39C12"),
    ]
    
    names = [c[0] for c in constants]
    values = [c[1] for c in constants]
    colors = [c[2] for c in constants]
    
    bars = ax1.bar(names, values, color=colors, edgecolor='black')
    ax1.axhline(y=OMEGA, color='red', linestyle='--', linewidth=2, label=f'Ω = {OMEGA}')
    ax1.set_ylabel('Value', fontsize=12)
    ax1.set_title('Ω Compared to Related Constants', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{val:.2f}', ha='center', fontsize=10)
    
    # Right: Holographic levels
    ax2 = axes[1]
    
    levels = np.arange(0, 45)
    masses = 1.5e53 * (OMEGA ** (-levels))  # kg
    
    ax2.semilogy(levels, masses, 'b-', linewidth=2)
    
    # Mark special particles
    m_e = 9.1e-31
    m_p = 1.67e-27
    
    # Find levels
    level_e = -np.log(m_e / 1.5e53) / np.log(OMEGA)
    level_p = -np.log(m_p / 1.5e53) / np.log(OMEGA)
    
    ax2.axhline(m_e, color='red', linestyle='--', label=f'Electron (level ≈ {level_e:.1f})')
    ax2.axhline(m_p, color='green', linestyle='--', label=f'Proton (level ≈ {level_p:.1f})')
    ax2.axhline(masses[0], color='purple', linestyle=':', alpha=0.5, label='Universe')
    
    ax2.set_xlabel('Holographic Level (n)', fontsize=12)
    ax2.set_ylabel('Mass (kg)', fontsize=12)
    ax2.set_title('Mass Hierarchy from Ω Scaling', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "assets", "omega_origin.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()
    return output_path

def plot_prime_structure():
    """Visualize the prime factorization of 117."""
    print("\n📊 Generating Prime Structure Plot...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prime factorization tree
    # 117 = 9 × 13 = 3² × 13
    
    from matplotlib.patches import Circle, FancyArrowPatch
    
    # Draw nodes
    nodes = {
        "117": (0.5, 0.9),
        "9": (0.3, 0.6),
        "13": (0.7, 0.6),
        "3": (0.2, 0.3),
        "3'": (0.4, 0.3),
    }
    
    for label, (x, y) in nodes.items():
        color = '#E74C3C' if label in ["3", "3'", "13"] else '#3498DB'
        circle = Circle((x, y), 0.08, color=color, alpha=0.8)
        ax.add_patch(circle)
        display_label = "3" if label == "3'" else label
        ax.text(x, y, display_label, ha='center', va='center', fontsize=14, 
                fontweight='bold', color='white')
    
    # Draw edges
    edges = [
        ("117", "9"), ("117", "13"),
        ("9", "3"), ("9", "3'")
    ]
    
    for start, end in edges:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        ax.annotate("", xy=(x2, y2+0.08), xytext=(x1, y1-0.08),
                   arrowprops=dict(arrowstyle="->", color='black', lw=2))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    ax.set_title('Prime Factorization: 117 = 3² × 13', fontsize=14, fontweight='bold')
    
    # Add explanation
    ax.text(0.5, 0.05, 
            "117 factors into 3² × 13\n"
            "• 3 is the first odd prime (triangular stability)\n"
            "• 13 is the 6th prime (2×3)\n"
            "• 3² represents the 3 spatial dimensions squared",
            ha='center', fontsize=11, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "assets", "prime_structure.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("🔮 ORIGIN OF OMEGA: Deriving Ω = 117.038")
    print("   Paper 9: Why This Number?")
    print("=" * 60 + "\n")
    
    results = explore_mathematical_origins()
    plot_omega_relationships()
    plot_prime_structure()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    print("\nBest candidates for Ω origin:")
    print("  1. Prime structure: 3² × 13 = 117 (integer part)")
    print("  2. SM connection: 90 fermions + 27 bosons = 117")
    print("  3. α⁻¹ / γ_μ ≈ 122 (close but not exact)")
    print("\nThe 0.038 residual may encode:")
    print("  • Quantum corrections")
    print("  • Parent universe parameters")
    print("  • Running coupling effects")
