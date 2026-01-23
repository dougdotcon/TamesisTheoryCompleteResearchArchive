"""
Quantum-Classical Transition Simulation
========================================

Simulates the interface visibility as a function of mass,
comparing the Tamesis step-function prediction with CSL/GRW smooth decay.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

# Academic style
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})


# Physical constants
M_c = 2.2e-14  # Critical mass (kg)
hbar = 1.055e-34
c = 3e8
G = 6.674e-11
m_atom = 1.67e-27
l_P = 1.616e-35


def visibility_tamesis(M, M_c, width_fraction=0.01):
    """
    Tamesis prediction: step-function transition at M_c.
    
    The transition width is set by (width_fraction * M_c).
    """
    width = width_fraction * M_c
    # Hyperbolic tangent for smooth approximation
    return 0.5 * (1 - np.tanh((M - M_c) / width))


def visibility_csl(M, lambda_csl=1e-8, r_csl=1e-7):
    """
    Continuous Spontaneous Localization (CSL) prediction.
    
    Visibility decays exponentially with mass.
    """
    # Simplified CSL: V ~ exp(-lambda * N^2 * t)
    # For steady state comparison, use mass-dependent decay
    N = M / m_atom  # Number of nucleons
    decay_rate = lambda_csl * (N / 1e10)**2
    return np.exp(-decay_rate)


def visibility_grw(M, lambda_grw=1e-16):
    """
    Ghirardi-Rimini-Weber (GRW) prediction.
    
    Smooth exponential decay.
    """
    N = M / m_atom
    return np.exp(-lambda_grw * N)


def coherence_time_tamesis(M, M_c):
    """
    Coherence time as function of mass.
    
    Tamesis: diverges below M_c, collapses above.
    """
    tau = np.zeros_like(M)
    
    # Below M_c: quantum coherence maintained
    below = M < M_c
    tau[below] = 1e10  # Effectively infinite
    
    # Above M_c: immediate collapse
    above = M >= M_c
    tau[above] = l_P / c  # Planck time ~ instant
    
    return tau


def coherence_time_csl(M, lambda_csl=1e-8):
    """
    CSL coherence time: smooth decay with mass.
    """
    N = M / m_atom
    return 1.0 / (lambda_csl * (N / 1e10)**2 + 1e-15)


def simulate_transition():
    """
    Generate all transition plots.
    """
    M = np.logspace(-18, -10, 500)
    
    # ============================================================
    # Figure 1: Visibility Comparison
    # ============================================================
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
    
    V_tam = visibility_tamesis(M, M_c)
    V_csl = visibility_csl(M)
    V_grw = visibility_grw(M)
    
    ax.semilogx(M * 1e15, V_tam, 'r-', lw=2.5, label='Tamesis (step at $M_c$)')
    ax.semilogx(M * 1e15, V_csl, 'b--', lw=1.5, label='CSL (smooth)')
    ax.semilogx(M * 1e15, V_grw, 'g:', lw=1.5, label='GRW (smooth)')
    
    ax.axvline(M_c * 1e15, color='gray', ls=':', lw=1, alpha=0.7)
    ax.annotate(f'$M_c$ = {M_c*1e15:.0f} fg', xy=(M_c*1e15, 0.5), fontsize=9,
                xytext=(M_c*1e15 * 3, 0.6), arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax.set_xlabel('Mass (femtograms)')
    ax.set_ylabel('Interference Visibility')
    ax.set_title('Quantum-Classical Transition: Tamesis vs Mainstream', fontweight='bold')
    ax.legend(loc='right', frameon=True, edgecolor='black')
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(1e-3, 1e5)
    
    plt.tight_layout()
    plt.savefig('visibility_comparison.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: visibility_comparison.png")
    
    # ============================================================
    # Figure 2: Coherence Time
    # ============================================================
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
    
    tau_tam = coherence_time_tamesis(M, M_c)
    tau_csl = coherence_time_csl(M)
    
    ax.loglog(M * 1e15, tau_tam, 'r-', lw=2.5, label='Tamesis')
    ax.loglog(M * 1e15, tau_csl, 'b--', lw=1.5, label='CSL')
    
    ax.axvline(M_c * 1e15, color='gray', ls=':', lw=1, alpha=0.7)
    ax.axhline(1, color='gray', ls='--', lw=0.5, alpha=0.5)
    
    ax.set_xlabel('Mass (femtograms)')
    ax.set_ylabel('Coherence Time (s)')
    ax.set_title('Coherence Time vs Mass', fontweight='bold')
    ax.legend(loc='upper right', frameon=True, edgecolor='black')
    ax.set_ylim(1e-44, 1e12)
    ax.set_xlim(1e-3, 1e5)
    
    ax.text(M_c * 1e15 * 0.1, 1e8, 'Quantum\n(stable)', fontsize=9, ha='center')
    ax.text(M_c * 1e15 * 10, 1e-30, 'Classical\n(collapsed)', fontsize=9, ha='center')
    
    plt.tight_layout()
    plt.savefig('coherence_time.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: coherence_time.png")
    
    # ============================================================
    # Figure 3: Phase Diagram
    # ============================================================
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
    
    # Mass axis (log scale)
    mass_range = np.logspace(-20, -8, 100)
    
    # Quantum region (below M_c)
    quantum_region = mass_range < M_c
    classical_region = mass_range >= M_c
    
    ax.fill_between(mass_range[quantum_region] * 1e15, 0, 1, 
                    alpha=0.3, color='blue', label='Quantum Regime')
    ax.fill_between(mass_range[classical_region] * 1e15, 0, 1, 
                    alpha=0.3, color='red', label='Classical Regime')
    
    ax.axvline(M_c * 1e15, color='black', lw=2, label=f'$M_c$ = {M_c*1e15:.0f} fg')
    
    # Mark key masses
    key_masses = [
        (1e-27, 'H atom'),
        (1e-24, 'C₆₀'),
        (2.2e-14, '$M_c$'),
        (1e-12, 'Bacteria'),
    ]
    
    for m, label in key_masses:
        ax.axvline(m * 1e15, color='gray', ls=':', lw=0.5, alpha=0.5)
        ax.text(m * 1e15, 0.95, label, rotation=90, va='top', ha='right', fontsize=8)
    
    ax.set_xscale('log')
    ax.set_xlabel('Mass (femtograms)')
    ax.set_ylabel('')
    ax.set_title('Phase Diagram: Quantum vs Classical', fontweight='bold')
    ax.legend(loc='lower right', frameon=True, edgecolor='black')
    ax.set_xlim(1e-12, 1e3)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    
    plt.tight_layout()
    plt.savefig('phase_diagram.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: phase_diagram.png")
    
    # ============================================================
    # Figure 4: Experimental Detection Region
    # ============================================================
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
    
    # Current experimental frontier
    mass_frontier = np.logspace(-20, -10, 100)
    
    # Achieved interference (confirmed quantum)
    achieved = [
        (1e-27, 'Atoms'),
        (1e-24, 'Small molecules'),
        (1e-22, 'C₆₀'),
        (1e-21, 'Large organics'),
    ]
    
    # Target experiments
    targets = [
        (1e-18, 'OTIMA'),
        (1e-16, 'MAQRO'),
        (2.2e-14, 'Tamesis $M_c$'),
        (1e-13, 'TEQ'),
    ]
    
    # Plot regions
    ax.axvspan(1e-27, 1e-21, alpha=0.3, color='green', label='Achieved (quantum)')
    ax.axvspan(1e-21, M_c, alpha=0.2, color='yellow', label='Frontier (in progress)')
    ax.axvspan(M_c, 1e-10, alpha=0.2, color='red', label='Classical (predicted)')
    
    ax.axvline(M_c, color='black', lw=2)
    ax.text(M_c * 1.2, 0.5, f'$M_c$ = {M_c*1e15:.0f} fg', fontsize=10, fontweight='bold', rotation=90, va='center')
    
    # Mark experiments
    for i, (m, name) in enumerate(achieved):
        ax.scatter(m, 0.8, s=100, c='green', marker='o', zorder=5)
        ax.text(m, 0.85, name, ha='center', fontsize=8)
    
    for i, (m, name) in enumerate(targets):
        ax.scatter(m, 0.3, s=100, c='orange', marker='^', zorder=5)
        ax.text(m, 0.2, name, ha='center', fontsize=8)
    
    ax.set_xscale('log')
    ax.set_xlabel('Mass (kg)')
    ax.set_ylabel('')
    ax.set_title('Experimental Roadmap to $M_c$', fontweight='bold')
    ax.legend(loc='upper left', frameon=True, edgecolor='black')
    ax.set_xlim(1e-28, 1e-10)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    
    plt.tight_layout()
    plt.savefig('experimental_roadmap.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: experimental_roadmap.png")


if __name__ == "__main__":
    print("Simulating Quantum-Classical Transition...")
    print(f"Critical Mass M_c = {M_c} kg = {M_c*1e15:.1f} fg")
    print()
    
    simulate_transition()
    
    print()
    print("All transition simulations complete!")
