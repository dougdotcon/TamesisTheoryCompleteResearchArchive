"""
=============================================================================
DERIVATION 09: NEUTRINO MASSES FROM TAMESIS KERNEL
=============================================================================
Neutrino masses are extraordinarily small: m_ν < 0.1 eV vs m_e = 511 keV

The Tamesis explanation uses the SEESAW MECHANISM naturally emerging from
graph topology:
- Right-handed neutrinos exist at "deep" graph layers (large Q)
- Their mass M_R ~ M_Pl * ε^Q_R is huge (GUT scale)
- Light neutrino masses: m_ν ~ m_D²/M_R (seesaw formula)

Observed (from oscillations, PDG 2024):
- Δm²_21 = 7.53 × 10⁻⁵ eV² (solar)
- |Δm²_31| = 2.453 × 10⁻³ eV² (atmospheric)
- Sum: Σm_ν < 0.12 eV (cosmological bound)

Normal ordering: m1 < m2 < m3
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# From Tamesis derivations
v_EW = 246e9  # eV (electroweak scale)
epsilon = 0.208  # Tunneling amplitude from fermion mass fit
M_GUT = 2e16 * 1e9  # eV (GUT scale ~ 2×10^16 GeV)

# Observed mass-squared differences
delta_m21_sq_obs = 7.53e-5  # eV²
delta_m31_sq_obs = 2.453e-3  # eV² (normal ordering)

# =============================================================================
# TAMESIS SEESAW MODEL
# =============================================================================

def dirac_mass(Q_L, Q_R, v=v_EW, eps=epsilon):
    """
    Dirac mass from Froggatt-Nielsen mechanism.
    m_D = v * ε^{|Q_L - Q_R|}
    """
    return v * eps**abs(Q_L - Q_R)

def majorana_mass(Q_R, M_scale=M_GUT, eps=epsilon):
    """
    Right-handed Majorana mass.
    M_R = M_GUT * ε^{Q_R}
    
    Right-handed neutrinos are localized at DEEP layers (large Q_R)
    giving them huge masses.
    """
    return M_scale * eps**Q_R

def seesaw_mass(m_D, M_R):
    """
    Type-I seesaw formula.
    m_ν ≈ m_D² / M_R
    """
    return m_D**2 / M_R

def compute_neutrino_masses(Q_L, Q_R_values, M_GUT_scale):
    """
    Compute light neutrino masses via seesaw.
    
    Parameters:
    -----------
    Q_L : list
        Horizontal charges for left-handed neutrinos (same as charged leptons)
    Q_R_values : list
        Horizontal charges for right-handed neutrinos
    M_GUT_scale : float
        GUT scale for Majorana masses
    """
    masses = []
    for i in range(3):
        m_D = dirac_mass(Q_L[i], Q_R_values[i])
        M_R = majorana_mass(Q_R_values[i], M_GUT_scale)
        m_nu = seesaw_mass(m_D, M_R)
        masses.append(m_nu)
    return np.array(masses)

def optimize_charges():
    """
    Find Q_R values that reproduce observed mass-squared differences.
    """
    # Left-handed charges (same as charged leptons from derivation_03)
    Q_L = [8, 4, 2]  # e, μ, τ
    
    # We need to find Q_R such that:
    # Δm²_21 = m2² - m1² ≈ 7.5×10⁻⁵ eV²
    # Δm²_31 = m3² - m1² ≈ 2.5×10⁻³ eV²
    
    best_params = None
    best_chi2 = np.inf
    
    # Grid search over Q_R values and M_GUT scale
    for Q_R1 in range(10, 20):
        for Q_R2 in range(8, 18):
            for Q_R3 in range(5, 15):
                for log_M in np.linspace(15, 17, 10):
                    M_scale = 10**log_M * 1e9  # Convert to eV
                    Q_R = [Q_R1, Q_R2, Q_R3]
                    
                    masses = compute_neutrino_masses(Q_L, Q_R, M_scale)
                    
                    # Sort masses (normal ordering)
                    masses_sorted = np.sort(masses)
                    
                    if masses_sorted[0] > 0 and masses_sorted[1] > 0:
                        dm21_sq = masses_sorted[1]**2 - masses_sorted[0]**2
                        dm31_sq = masses_sorted[2]**2 - masses_sorted[0]**2
                        
                        # Chi-squared
                        chi2 = ((dm21_sq - delta_m21_sq_obs)/delta_m21_sq_obs)**2 + \
                               ((dm31_sq - delta_m31_sq_obs)/delta_m31_sq_obs)**2
                        
                        if chi2 < best_chi2:
                            best_chi2 = chi2
                            best_params = (Q_L, Q_R, M_scale, masses_sorted)
    
    return best_params, best_chi2

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TAMESIS THEORY: NEUTRINO MASS DERIVATION")
    print("=" * 70)
    
    print(f"\nObserved mass-squared differences:")
    print(f"  Δm²_21 (solar)       = {delta_m21_sq_obs:.2e} eV²")
    print(f"  |Δm²_31| (atmospheric) = {delta_m31_sq_obs:.2e} eV²")
    
    # Optimize
    print("\nSearching for optimal Tamesis parameters...")
    result, chi2 = optimize_charges()
    
    if result is None:
        print("No good fit found. Using analytical estimate...")
        # Analytical estimate
        Q_L = [8, 4, 2]
        Q_R = [14, 12, 9]
        M_scale = 2e16 * 1e9
        masses = compute_neutrino_masses(Q_L, Q_R, M_scale)
        masses_sorted = np.sort(masses)
    else:
        Q_L, Q_R, M_scale, masses_sorted = result
    
    print(f"\nOptimal Tamesis parameters:")
    print(f"  Q_L (left-handed)  = {Q_L}")
    print(f"  Q_R (right-handed) = {Q_R}")
    print(f"  M_GUT scale        = {M_scale/1e9:.2e} GeV")
    print(f"  ε (from fermions)  = {epsilon}")
    
    # Compute derived quantities
    dm21_sq = masses_sorted[1]**2 - masses_sorted[0]**2
    dm31_sq = masses_sorted[2]**2 - masses_sorted[0]**2
    sum_masses = np.sum(masses_sorted)
    
    print(f"\n" + "=" * 70)
    print("RESULTS: PREDICTED vs OBSERVED")
    print("=" * 70)
    
    print(f"\nNeutrino masses (normal ordering):")
    print(f"  m1 = {masses_sorted[0]*1e3:.4f} meV")
    print(f"  m2 = {masses_sorted[1]*1e3:.4f} meV")
    print(f"  m3 = {masses_sorted[2]*1e3:.4f} meV")
    print(f"  Σm_ν = {sum_masses*1e3:.2f} meV  (cosmological bound: < 120 meV)")
    
    print(f"\nMass-squared differences:")
    print(f"  {'Observable':<20} {'Predicted':>15} {'Observed':>15} {'Ratio':>10}")
    print("-" * 65)
    print(f"  {'Δm²_21 (eV²)':<20} {dm21_sq:>15.2e} {delta_m21_sq_obs:>15.2e} {dm21_sq/delta_m21_sq_obs:>10.2f}")
    print(f"  {'Δm²_31 (eV²)':<20} {dm31_sq:>15.2e} {delta_m31_sq_obs:>15.2e} {dm31_sq/delta_m31_sq_obs:>10.2f}")
    
    # Seesaw mechanism details
    print(f"\n" + "=" * 70)
    print("SEESAW MECHANISM DETAILS")
    print("=" * 70)
    
    for i in range(3):
        m_D = dirac_mass(Q_L[i], Q_R[i])
        M_R = majorana_mass(Q_R[i], M_scale)
        m_nu = seesaw_mass(m_D, M_R)
        print(f"\nGeneration {i+1}:")
        print(f"  Q_L = {Q_L[i]}, Q_R = {Q_R[i]}")
        print(f"  m_D = {m_D/1e9:.2e} GeV (Dirac)")
        print(f"  M_R = {M_R/1e9:.2e} GeV (Majorana)")
        print(f"  m_ν = m_D²/M_R = {m_nu*1e3:.4f} meV")
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Panel 1: Mass hierarchy
    ax1 = axes[0, 0]
    generations = ['m₁', 'm₂', 'm₃']
    ax1.bar(generations, masses_sorted * 1e3, color='steelblue', edgecolor='black')
    ax1.set_ylabel('Mass (meV)', fontsize=11)
    ax1.set_title('Neutrino Mass Hierarchy (Normal Ordering)', fontsize=12)
    ax1.axhline(120, color='red', ls='--', label='Cosmological bound')
    ax1.legend()
    for i, m in enumerate(masses_sorted):
        ax1.text(i, m*1e3 + 2, f'{m*1e3:.2f}', ha='center', fontsize=10)
    
    # Panel 2: Seesaw visualization
    ax2 = axes[0, 1]
    scales = ['m_D (GeV)', 'M_R (GeV)', 'm_ν (eV)']
    m_D_avg = np.mean([dirac_mass(Q_L[i], Q_R[i]) for i in range(3)]) / 1e9
    M_R_avg = np.mean([majorana_mass(Q_R[i], M_scale) for i in range(3)]) / 1e9
    m_nu_avg = np.mean(masses_sorted)
    
    values = [np.log10(m_D_avg), np.log10(M_R_avg), np.log10(m_nu_avg)]
    colors = ['green', 'red', 'blue']
    bars = ax2.bar(scales, values, color=colors, edgecolor='black')
    ax2.set_ylabel('log₁₀(mass scale)', fontsize=11)
    ax2.set_title('Seesaw Mechanism: m_ν = m_D²/M_R', fontsize=12)
    ax2.axhline(0, color='black', lw=0.5)
    for bar, val in zip(bars, values):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 0.5, 
                f'10^{val:.1f}', ha='center', fontsize=10)
    
    # Panel 3: Comparison with observed
    ax3 = axes[1, 0]
    x = np.arange(2)
    width = 0.35
    pred_vals = [dm21_sq * 1e5, dm31_sq * 1e3]  # Scale for visibility
    obs_vals = [delta_m21_sq_obs * 1e5, delta_m31_sq_obs * 1e3]
    
    bars1 = ax3.bar(x - width/2, pred_vals, width, label='Tamesis', color='steelblue')
    bars2 = ax3.bar(x + width/2, obs_vals, width, label='Observed', color='coral')
    ax3.set_ylabel('Δm² (scaled)', fontsize=11)
    ax3.set_xticks(x)
    ax3.set_xticklabels(['Δm²₂₁ (×10⁵ eV²)', 'Δm²₃₁ (×10³ eV²)'])
    ax3.set_title('Mass-Squared Differences', fontsize=12)
    ax3.legend()
    
    # Panel 4: Q_R charges and localization
    ax4 = axes[1, 1]
    layers = np.linspace(-5, 20, 500)
    
    for i, (qL, qR) in enumerate(zip(Q_L, Q_R)):
        psi_L = np.exp(-0.5 * ((layers - qL) / 1.5)**2)
        psi_R = np.exp(-0.5 * ((layers - qR) / 1.5)**2)
        ax4.plot(layers, psi_L, '-', lw=2, label=f'ν_L gen {i+1} (Q={qL})')
        ax4.plot(layers, psi_R, '--', lw=2, alpha=0.7, label=f'ν_R gen {i+1} (Q={qR})')
    
    ax4.set_xlabel('Graph layer (Q)', fontsize=11)
    ax4.set_ylabel('Wavefunction', fontsize=11)
    ax4.set_title('Neutrino Localization: L vs R', fontsize=12)
    ax4.legend(fontsize=8, ncol=2)
    ax4.axvspan(10, 20, alpha=0.1, color='red', label='GUT scale region')
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Neutrino Masses from Tamesis Seesaw Mechanism', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig('../assets/derivation_09_neutrino_masses.png', dpi=300, bbox_inches='tight')
    plt.savefig('../assets/derivation_09_neutrino_masses.pdf', dpi=300, bbox_inches='tight')
    print(f"\nFigure saved to assets/derivation_09_neutrino_masses.png")
    
    # Final assessment
    ratio_21 = dm21_sq / delta_m21_sq_obs
    ratio_31 = dm31_sq / delta_m31_sq_obs
    
    print(f"\n" + "=" * 70)
    print("FINAL ASSESSMENT")
    print("=" * 70)
    
    if 0.5 < ratio_21 < 2.0 and 0.5 < ratio_31 < 2.0:
        print("Status: ✓ GOOD - Both Δm² within factor of 2")
    elif 0.1 < ratio_21 < 10 and 0.1 < ratio_31 < 10:
        print("Status: ◐ PARTIAL - Order of magnitude correct")
    else:
        print("Status: ✗ Needs refinement")
    
    print(f"\nKey prediction: Σm_ν = {sum_masses*1e3:.1f} meV")
    print(f"Testable by: KATRIN, cosmological surveys")
    
    plt.show()
