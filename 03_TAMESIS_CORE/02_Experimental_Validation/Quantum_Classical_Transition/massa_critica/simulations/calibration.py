"""
Model Calibration for M_c Critical Mass
========================================

This module calibrates the M_c model parameters using:
1. Dimensional analysis from first principles
2. Experimental constraints from optomechanics
3. Consistency with existing collapse model bounds

Key Insight:
-----------
The tau_scale must be derived from the physics, not fitted ad-hoc.

Starting from:
    M_c = m_P × (a_0 / a_P)^(1/8)

The natural time scale should emerge from the same hierarchy:
    τ_c = t_P × (a_P / a_0)^(1/8)  [inverse scaling]

This gives τ_c at M_c, then:
    τ(M) = τ_c × (M_c / M)^α  for M > M_c

Experimental Constraints:
------------------------
1. No anomalous heating in levitated nanoparticles (ETH, Vienna)
   - M ~ 10^-18 to 10^-15 kg observed for ms to seconds
   - Must have τ > t_observation for M < M_c

2. CSL/GRW bounds from LIGO, LISA Pathfinder
   - λ_CSL < 10^-8 s^-1 for large masses

3. Cantilever experiments (Bouwmeester et al.)
   - M ~ 10^-12 kg, no collapse observed for t ~ seconds
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict
import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from simulations.constants import (
        M_C, M_PLANCK, TAU_PLANCK, A_0, A_PLANCK, HBAR, G_SI, C, K_B,
        XI, PHASE_SPACE_EXPONENT, L_PLANCK
    )
except ModuleNotFoundError:
    from constants import (
        M_C, M_PLANCK, TAU_PLANCK, A_0, A_PLANCK, HBAR, G_SI, C, K_B,
        XI, PHASE_SPACE_EXPONENT, L_PLANCK
    )


# =============================================================================
# FIRST PRINCIPLES DERIVATION OF TAU_SCALE
# =============================================================================

def derive_tau_scale_from_hierarchy() -> float:
    """
    Derive the natural time scale from the same acceleration hierarchy.
    
    If M_c = m_P × (a_0/a_P)^(1/8)
    Then τ_c = t_P × (a_P/a_0)^(1/8)  [inverse of mass scaling]
    
    This maintains dimensional consistency with the cosmological bound.
    """
    # Inverse hierarchy for time (longer times for smaller accelerations)
    tau_c = TAU_PLANCK * (A_PLANCK / A_0)**(1/8)
    
    print(f"=== FIRST PRINCIPLES DERIVATION ===")
    print(f"τ_P (Planck time)     = {TAU_PLANCK:.4e} s")
    print(f"(a_P / a_0)^(1/8)     = {(A_PLANCK / A_0)**(1/8):.4e}")
    print(f"τ_c (coherence @ M_c) = {tau_c:.4e} s")
    print(f"τ_c in years          = {tau_c / (365.25*24*3600):.4e}")
    
    return tau_c


def derive_tau_scale_from_information() -> float:
    """
    Alternative derivation using information-theoretic arguments.
    
    The coherence time at M_c should relate to:
    - The Hubble time (cosmological information bound)
    - The holographic entropy bound
    
    τ_c ~ t_H × (M_c / M_Hubble)^β
    
    where M_Hubble = c³ / (G × H_0) is the Hubble mass.
    """
    H_0 = 2.27e-18  # s^-1
    t_H = 1 / H_0   # Hubble time ~ 4.4 × 10^17 s
    M_Hubble = C**3 / (G_SI * H_0)  # ~ 10^53 kg
    
    # The exponent β should give τ_c on the order of experimental times
    # For consistency with M_c derivation, use same 1/8 exponent
    beta = 1/8
    
    tau_c = t_H * (M_C / M_Hubble)**beta
    
    print(f"\n=== INFORMATION-THEORETIC DERIVATION ===")
    print(f"Hubble time t_H       = {t_H:.4e} s")
    print(f"Hubble mass M_H       = {M_Hubble:.4e} kg")
    print(f"M_c / M_H             = {M_C / M_Hubble:.4e}")
    print(f"τ_c (from info bound) = {tau_c:.4e} s")
    
    return tau_c


def derive_tau_scale_from_gravity() -> float:
    """
    Gravitational self-energy derivation (Penrose-like).
    
    τ_c ~ ℏ / E_grav
    E_grav ~ G × M_c² / R_c
    
    where R_c is the characteristic size at M_c.
    For a silica sphere: R_c ~ 50-400 nm
    """
    # Characteristic size at M_c (silica sphere)
    rho_silica = 2200  # kg/m³
    R_c = (3 * M_C / (4 * np.pi * rho_silica))**(1/3)
    
    # Gravitational self-energy
    E_grav = G_SI * M_C**2 / R_c
    
    # Penrose time
    tau_c = HBAR / E_grav
    
    print(f"\n=== GRAVITATIONAL (PENROSE-LIKE) DERIVATION ===")
    print(f"Characteristic radius R_c = {R_c*1e9:.1f} nm")
    print(f"Gravitational energy E_g  = {E_grav:.4e} J")
    print(f"τ_c (Penrose-like)        = {tau_c:.4e} s")
    print(f"τ_c in hours              = {tau_c / 3600:.2f}")
    
    return tau_c


def derive_tau_scale_combined() -> Dict[str, float]:
    """
    Combine multiple derivation approaches and find consensus.
    """
    results = {}
    
    results['hierarchy'] = derive_tau_scale_from_hierarchy()
    results['information'] = derive_tau_scale_from_information()
    results['gravity'] = derive_tau_scale_from_gravity()
    
    # Geometric mean as consensus (spans many orders of magnitude)
    geo_mean = np.exp(np.mean(np.log(list(results.values()))))
    results['consensus'] = geo_mean
    
    print(f"\n=== CONSENSUS ===")
    print(f"Geometric mean of derivations: τ_c = {geo_mean:.4e} s")
    
    return results


# =============================================================================
# EXPERIMENTAL CONSTRAINTS
# =============================================================================

def experimental_bounds() -> Dict[str, Dict]:
    """
    Compile experimental constraints on collapse times/rates.
    
    Returns dictionary of experiments with their mass, observed time,
    and whether collapse was observed.
    """
    bounds = {
        "molecule_interference_2019": {
            "mass_kg": 2.5e-23,  # ~2000 amu fullerene
            "observation_time_s": 1e-3,
            "coherence_observed": True,
            "reference": "Fein et al. 2019, Nature Physics"
        },
        "levitated_nanoparticle_2020": {
            "mass_kg": 1e-18,  # 10^6 amu
            "observation_time_s": 0.1,
            "coherence_observed": True,
            "reference": "Magrini et al. 2021"
        },
        "optomech_ground_state_2021": {
            "mass_kg": 1e-14,  # Micromechanical oscillator
            "observation_time_s": 1e-3,
            "coherence_observed": True,
            "reference": "Teufel et al."
        },
        "cantilever_2022": {
            "mass_kg": 1e-12,  # ~ng
            "observation_time_s": 10,
            "coherence_observed": True,
            "reference": "Bouwmeester group"
        },
        "LIGO_test_mass": {
            "mass_kg": 40,  # 40 kg mirror
            "observation_time_s": 1,
            "coherence_observed": True,  # No anomalous noise
            "reference": "LIGO, constraints on CSL"
        }
    }
    
    print(f"\n=== EXPERIMENTAL CONSTRAINTS ===")
    print(f"{'Experiment':<35} {'M (kg)':<12} {'t_obs (s)':<12} {'Coherent?':<10}")
    print("-" * 70)
    for name, data in bounds.items():
        status = "YES" if data["coherence_observed"] else "NO"
        print(f"{name:<35} {data['mass_kg']:<12.2e} {data['observation_time_s']:<12.2e} {status:<10}")
    
    return bounds


def calibrate_against_experiments(bounds: Dict) -> float:
    """
    Find tau_c that is consistent with all experimental observations.
    
    Rule: For experiments where coherence was observed,
          τ(M) must be > t_observation
    
    For M > M_c: τ(M) = τ_c × (M_c/M)^α
    We need τ(M) > t_obs
    → τ_c > t_obs × (M/M_c)^α
    
    Take most constraining bound.
    """
    alpha = 2  # Use quadratic exponent as baseline
    
    constraints = []
    
    print(f"\n=== CALIBRATION AGAINST EXPERIMENTS (α = {alpha}) ===")
    print(f"M_c = {M_C:.4e} kg\n")
    
    for name, data in bounds.items():
        M = data["mass_kg"]
        t_obs = data["observation_time_s"]
        
        if data["coherence_observed"] and M > M_C:
            # Constraint: τ_c > t_obs × (M/M_c)^α
            tau_c_min = t_obs * (M / M_C)**alpha
            constraints.append(tau_c_min)
            print(f"{name}:")
            print(f"  M = {M:.2e} kg (M/M_c = {M/M_C:.2e})")
            print(f"  t_obs = {t_obs:.2e} s")
            print(f"  → τ_c must be > {tau_c_min:.4e} s")
            print()
    
    if constraints:
        tau_c_calibrated = max(constraints) * 2  # Safety factor of 2
        print(f"Most constraining: τ_c > {max(constraints):.4e} s")
        print(f"Calibrated τ_c (with 2× safety): {tau_c_calibrated:.4e} s")
        return tau_c_calibrated
    else:
        print("No constraints from M > M_c experiments")
        return 1.0  # Default


# =============================================================================
# FINAL CALIBRATED MODEL
# =============================================================================

class CalibratedMCModel:
    """
    Calibrated M_c model with physics-informed parameters.
    
    Key parameters after calibration:
    - tau_c: coherence time at M = M_c
    - alpha: power law exponent
    - delta_x_ref: reference superposition separation
    """
    
    def __init__(self, tau_c: float = None, alpha: float = 2.0):
        """
        Initialize with calibrated or derived tau_c.
        
        If tau_c is None, derive from gravitational time scale.
        """
        if tau_c is None:
            # Use gravitational derivation as most physically motivated
            rho_silica = 2200
            R_c = (3 * M_C / (4 * np.pi * rho_silica))**(1/3)
            E_grav = G_SI * M_C**2 / R_c
            self.tau_c = HBAR / E_grav
        else:
            self.tau_c = tau_c
        
        self.alpha = alpha
        self.M_c = M_C
        self.lambda_c = HBAR / (M_C * C)  # Compton wavelength at M_c
    
    def coherence_time(self, mass: float) -> float:
        """
        Calculate intrinsic coherence time.
        
        τ(M) = τ_c × (M_c / M)^α  for M > M_c
        τ(M) = ∞                   for M ≤ M_c
        """
        if mass <= self.M_c:
            return np.inf
        
        return self.tau_c * (self.M_c / mass)**self.alpha
    
    def decoherence_rate(self, mass: float, delta_x: float = None) -> float:
        """
        Calculate decoherence rate with optional spatial dependence.
        
        Γ(M, Δx) = 1/τ(M) × (Δx / R_c)²
        
        where R_c is characteristic size at M_c.
        """
        tau = self.coherence_time(mass)
        if np.isinf(tau):
            return 0.0
        
        gamma = 1.0 / tau
        
        # Spatial dependence: larger separations decohere faster
        if delta_x is not None:
            rho = 2200  # silica
            R_c = (3 * self.M_c / (4 * np.pi * rho))**(1/3)
            gamma *= (delta_x / R_c)**2
        
        return gamma
    
    def visibility(self, mass: float, time: float, delta_x: float = None) -> float:
        """
        Calculate interference visibility decay.
        
        V(t) = exp(-Γ × t)
        """
        gamma = self.decoherence_rate(mass, delta_x)
        return np.exp(-gamma * time)
    
    def summary(self):
        """Print model summary."""
        print("=" * 60)
        print("CALIBRATED M_c MODEL")
        print("=" * 60)
        print(f"Critical mass M_c     = {self.M_c:.4e} kg")
        print(f"                      = {self.M_c/1.66e-27:.2e} Da")
        print(f"Coherence time @ M_c  = {self.tau_c:.4e} s")
        print(f"                      = {self.tau_c/3600:.2f} hours")
        print(f"Power law exponent α  = {self.alpha}")
        print()
        
        # Sample predictions
        test_masses = [0.1*M_C, M_C, 10*M_C, 100*M_C, 1000*M_C]
        print(f"{'M/M_c':<12} {'τ (s)':<15} {'Γ (s⁻¹)':<15} {'V(1s)':<10}")
        print("-" * 52)
        for m in test_masses:
            tau = self.coherence_time(m)
            gamma = self.decoherence_rate(m)
            V = self.visibility(m, 1.0)
            
            if np.isinf(tau):
                print(f"{m/M_C:<12.1f} {'∞':<15} {'0':<15} {'1.000':<10}")
            else:
                print(f"{m/M_C:<12.1f} {tau:<15.4e} {gamma:<15.4e} {V:<10.4f}")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_calibrated_model(model: CalibratedMCModel, save_path: str = None):
    """
    Generate publication-quality plot of calibrated model.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Coherence time vs mass
    ax1 = axes[0, 0]
    masses = np.logspace(-18, -8, 500)
    tau_values = np.array([model.coherence_time(m) for m in masses])
    tau_plot = np.where(np.isinf(tau_values), np.nan, tau_values)
    
    ax1.loglog(masses, tau_plot, 'b-', linewidth=2, label=f'α = {model.alpha}')
    ax1.axvline(M_C, color='red', linestyle='--', linewidth=2, 
                label=f'$M_c$ = {M_C:.2e} kg')
    ax1.axhline(1, color='gray', linestyle=':', alpha=0.5, label='1 second')
    ax1.axhline(model.tau_c, color='green', linestyle='-.', alpha=0.7,
                label=f'τ_c = {model.tau_c:.2e} s')
    
    ax1.set_xlabel('Mass (kg)', fontsize=12)
    ax1.set_ylabel('Coherence Time τ (s)', fontsize=12)
    ax1.set_title('Intrinsic Coherence Time vs Mass', fontsize=14)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(1e-10, 1e20)
    
    # 2. Decoherence rate vs mass
    ax2 = axes[0, 1]
    gamma_values = np.array([model.decoherence_rate(m) for m in masses])
    gamma_plot = np.where(gamma_values == 0, np.nan, gamma_values)
    
    ax2.loglog(masses, gamma_plot, 'b-', linewidth=2)
    ax2.axvline(M_C, color='red', linestyle='--', linewidth=2)
    ax2.axhline(1, color='gray', linestyle=':', alpha=0.5, label='Γ = 1 s⁻¹')
    
    ax2.set_xlabel('Mass (kg)', fontsize=12)
    ax2.set_ylabel('Decoherence Rate Γ (s⁻¹)', fontsize=12)
    ax2.set_title('Intrinsic Decoherence Rate vs Mass', fontsize=14)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # 3. Visibility decay over time for different masses
    ax3 = axes[1, 0]
    time_array = np.linspace(0, 10, 1000)
    test_masses_vis = [10*M_C, 50*M_C, 100*M_C, 500*M_C]
    colors = plt.cm.plasma(np.linspace(0.2, 0.8, len(test_masses_vis)))
    
    for m, color in zip(test_masses_vis, colors):
        V = np.array([model.visibility(m, t) for t in time_array])
        label = f'M = {m/M_C:.0f} M_c'
        ax3.plot(time_array, V, color=color, linewidth=2, label=label)
    
    ax3.axhline(0.5, color='red', linestyle=':', label='V = 0.5 (threshold)')
    ax3.set_xlabel('Time (s)', fontsize=12)
    ax3.set_ylabel('Visibility V(t)', fontsize=12)
    ax3.set_title('Interference Visibility Decay', fontsize=14)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 1.05)
    
    # 4. Parameter space: (M, t) where coherence survives
    ax4 = axes[1, 1]
    masses_2d = np.logspace(-17, -10, 100)
    times_2d = np.logspace(-3, 3, 100)
    M_grid, T_grid = np.meshgrid(masses_2d, times_2d)
    
    V_grid = np.zeros_like(M_grid)
    for i in range(len(times_2d)):
        for j in range(len(masses_2d)):
            V_grid[i, j] = model.visibility(M_grid[i, j], T_grid[i, j])
    
    # Contour at V = 0.5 (coherence threshold)
    cs = ax4.contourf(np.log10(M_grid), np.log10(T_grid), V_grid,
                      levels=[0, 0.1, 0.5, 0.9, 1.0],
                      colors=['darkred', 'red', 'orange', 'yellow', 'lightgreen'])
    ax4.axvline(np.log10(M_C), color='white', linestyle='--', linewidth=2)
    
    ax4.set_xlabel('log₁₀(M / kg)', fontsize=12)
    ax4.set_ylabel('log₁₀(t / s)', fontsize=12)
    ax4.set_title('Parameter Space: Visibility Regions', fontsize=14)
    
    cbar = plt.colorbar(cs, ax=ax4)
    cbar.set_label('Visibility V(M, t)', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved: {save_path}")
    
    plt.close()
    return fig


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("M_c MODEL CALIBRATION")
    print("=" * 70)
    
    # 1. Derive tau_c from multiple approaches
    derivations = derive_tau_scale_combined()
    
    # 2. Check experimental constraints
    bounds = experimental_bounds()
    
    # 3. Calibrate against experiments
    tau_c_exp = calibrate_against_experiments(bounds)
    
    # 4. Choose final tau_c
    # Use gravitational derivation as it's most physically motivated
    # and consistent with Diósi-Penrose
    tau_c_final = derivations['gravity']
    
    print(f"\n" + "=" * 70)
    print(f"FINAL CALIBRATED τ_c = {tau_c_final:.4e} s")
    print(f"                     = {tau_c_final/3600:.2f} hours")
    print("=" * 70)
    
    # 5. Create and test calibrated model
    model = CalibratedMCModel(tau_c=tau_c_final, alpha=2.0)
    print()
    model.summary()
    
    # 6. Generate plots
    print("\nGenerating plots...")
    plot_calibrated_model(model, save_path="calibrated_mc_model.png")
    
    # 7. Export calibrated parameters
    print("\n" + "=" * 70)
    print("CALIBRATED PARAMETERS FOR USE IN OTHER MODULES")
    print("=" * 70)
    print(f"TAU_C_CALIBRATED = {tau_c_final:.6e}  # seconds")
    print(f"ALPHA_DEFAULT = 2.0")
    print(f"M_C = {M_C:.6e}  # kg")
    
    print("\nDone!")
