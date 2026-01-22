"""
Collapse Dynamics Simulations
=============================

This module implements models for the temporal dynamics of quantum
coherence breakdown near the critical mass M_c.

Main Hypotheses to Test:
------------------------
H1: Collapse time follows power law: τ(M) = τ_P × (M/M_c)^(-α)
H2: The exponent α is between 1 and 8 (phase space origin)
H3: For M < M_c, intrinsic decoherence is negligible vs environmental

Key Functions:
--------------
- collapse_time_power_law: Power law model for coherence time
- intrinsic_decoherence_rate: Rate of intrinsic (non-environmental) collapse
- compare_with_environmental: Compare intrinsic vs environmental decoherence
- phase_portrait: Map the (M, τ) parameter space
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Tuple, Optional

# Import constants
from .constants import (
    M_C, M_PLANCK, TAU_PLANCK, A_0, A_PLANCK, HBAR, C, G_SI, K_B,
    XI, PHASE_SPACE_EXPONENT
)


# =============================================================================
# MODEL 1: POWER LAW COLLAPSE TIME
# =============================================================================

def collapse_time_power_law(
    mass: np.ndarray,
    exponent: float = 1.0,
    tau_scale: float = None
) -> np.ndarray:
    """
    Model: Collapse time follows power law with critical mass threshold.
    
    τ(M) = τ_scale × (M_c / M)^α  for M > M_c
    τ(M) = ∞                      for M ≤ M_c
    
    Parameters:
    -----------
    mass : np.ndarray
        Array of masses (kg)
    exponent : float
        Power law exponent α (default 1.0, testing range 1-8)
    tau_scale : float
        Reference time scale (default: derived from Planck time)
    
    Returns:
    --------
    tau : np.ndarray
        Coherence time (s). Returns np.inf for M ≤ M_c
    
    Physical Interpretation:
    ------------------------
    - α = 1: Linear regime (Markovian collapse)
    - α = 2: Quadratic (gravitationally-induced)
    - α = 8: Full phase space geometric origin
    """
    if tau_scale is None:
        # Derive from Planck scale with Ω correction
        # This gives reasonable times for mesoscopic systems
        tau_scale = TAU_PLANCK * (A_PLANCK / A_0)**0.5  # ~ 10⁻⁵ s
    
    mass = np.atleast_1d(mass)
    tau = np.full_like(mass, np.inf, dtype=float)
    
    # Above critical mass: finite coherence time
    above_critical = mass > M_C
    tau[above_critical] = tau_scale * (M_C / mass[above_critical])**exponent
    
    return tau


def collapse_time_exponential(
    mass: np.ndarray,
    omega: float = 117.038
) -> np.ndarray:
    """
    Alternative Model: Exponential scaling with Ω.
    
    τ(M) = τ_P × Ω^(f(M/M_c))
    
    where f(x) is a monotonic function.
    
    Parameters:
    -----------
    mass : np.ndarray
        Array of masses (kg)
    omega : float
        Universal scaling constant (default: 117.038)
    
    Returns:
    --------
    tau : np.ndarray
        Coherence time (s)
    """
    mass = np.atleast_1d(mass)
    
    # Scaling function: f(x) = (M_c / M) for M > M_c
    ratio = M_C / np.clip(mass, 1e-30, None)
    
    # Exponential scaling: Ω^(M_c / M)
    tau = TAU_PLANCK * (omega ** ratio)
    
    # Clamp to reasonable values
    tau = np.clip(tau, TAU_PLANCK, 1e30)
    
    return tau


# =============================================================================
# MODEL 2: INTRINSIC DECOHERENCE RATE
# =============================================================================

def intrinsic_decoherence_rate(
    mass: np.ndarray,
    delta_x: float = 1e-6,
    model: str = "mc_power"
) -> np.ndarray:
    """
    Calculate intrinsic (non-environmental) decoherence rate.
    
    Γ_intr = 1 / τ(M)
    
    Parameters:
    -----------
    mass : np.ndarray
        Mass of system (kg)
    delta_x : float
        Spatial separation of superposition (m)
    model : str
        "mc_power" : M_c power law model
        "mc_exp" : M_c exponential model
        "dp" : Diósi-Penrose gravitational
        "csl" : Continuous Spontaneous Localization
    
    Returns:
    --------
    gamma : np.ndarray
        Decoherence rate (s⁻¹)
    """
    mass = np.atleast_1d(mass)
    
    if model == "mc_power":
        tau = collapse_time_power_law(mass, exponent=2.0)
        gamma = 1.0 / tau
        # Enhance with spatial dependence
        gamma *= (delta_x / (HBAR / (M_C * C)))**2
        
    elif model == "mc_exp":
        tau = collapse_time_exponential(mass)
        gamma = 1.0 / tau
        
    elif model == "dp":
        # Diósi-Penrose: Γ_DP ≈ G m² / (ℏ Δx)
        gamma = G_SI * mass**2 / (HBAR * delta_x)
        
    elif model == "csl":
        # CSL: Γ_CSL ≈ λ (m / m_nucleon)² (Δx / r_C)²
        m_nucleon = 1.67e-27
        r_C = 1e-7
        lambda_csl = 1e-16
        gamma = lambda_csl * (mass / m_nucleon)**2 * (delta_x / r_C)**2
        
    else:
        raise ValueError(f"Unknown model: {model}")
    
    return gamma


# =============================================================================
# MODEL 3: COMPARISON WITH ENVIRONMENTAL DECOHERENCE
# =============================================================================

def environmental_decoherence_rate(
    mass: float,
    temperature: float = 300,
    pressure: float = 1e-10,
    photon_rate: float = 0
) -> dict:
    """
    Calculate environmental decoherence from various sources.
    
    Parameters:
    -----------
    mass : float
        Mass of system (kg)
    temperature : float
        Temperature (K)
    pressure : float
        Gas pressure (Pa)
    photon_rate : float
        Photon scattering rate (s⁻¹)
    
    Returns:
    --------
    rates : dict
        Dictionary with contributions from each source
    """
    rates = {}
    
    # Thermal photon decoherence
    # Γ_photon ∝ (k_B T / ℏc)³ × σ_abs × c
    lambda_thermal = HBAR * C / (K_B * temperature)
    rates["photon_thermal"] = (2 * np.pi * K_B * temperature / HBAR)**3 * 1e-20  # Rough estimate
    
    # Gas collision decoherence
    # Γ_gas ≈ n_gas × σ × v_thermal
    v_thermal = np.sqrt(2 * K_B * temperature / (28 * 1.66e-27))  # N2 molecules
    n_gas = pressure / (K_B * temperature)
    sigma = 1e-19  # m² (geometric cross-section for nm particle)
    rates["gas_collision"] = n_gas * sigma * v_thermal
    
    # Added photon scattering
    rates["photon_scatter"] = photon_rate
    
    # Total
    rates["total"] = sum(rates.values())
    
    return rates


def compare_decoherence_regimes(
    mass_range: np.ndarray,
    temperature: float = 4,
    pressure: float = 1e-12
) -> dict:
    """
    Compare intrinsic vs environmental decoherence across mass range.
    
    Parameters:
    -----------
    mass_range : np.ndarray
        Array of masses to evaluate (kg)
    temperature : float
        System temperature (K)
    pressure : float
        Vacuum pressure (Pa)
    
    Returns:
    --------
    results : dict
        Contains 'mass', 'gamma_intrinsic', 'gamma_env', 'crossover_mass'
    """
    gamma_intrinsic = intrinsic_decoherence_rate(mass_range, model="mc_power")
    
    gamma_env = np.array([
        environmental_decoherence_rate(m, temperature, pressure)["total"]
        for m in mass_range
    ])
    
    # Find crossover point
    crossover_idx = np.argmin(np.abs(gamma_intrinsic - gamma_env))
    crossover_mass = mass_range[crossover_idx]
    
    return {
        "mass": mass_range,
        "gamma_intrinsic": gamma_intrinsic,
        "gamma_env": gamma_env,
        "crossover_mass": crossover_mass
    }


# =============================================================================
# PHASE SPACE ANALYSIS
# =============================================================================

def phase_portrait(
    mass_range: np.ndarray = None,
    exponent_range: np.ndarray = None,
    save_path: str = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate phase portrait of collapse times in (M, α) space.
    
    Parameters:
    -----------
    mass_range : np.ndarray
        Range of masses (kg)
    exponent_range : np.ndarray
        Range of power law exponents
    save_path : str
        Path to save figure (optional)
    
    Returns:
    --------
    M_grid, alpha_grid, tau_grid : np.ndarray
        2D grids for plotting
    """
    if mass_range is None:
        mass_range = np.logspace(-18, -12, 100)  # 10⁻¹⁸ to 10⁻¹² kg
    
    if exponent_range is None:
        exponent_range = np.linspace(1, 8, 50)
    
    M_grid, alpha_grid = np.meshgrid(mass_range, exponent_range)
    tau_grid = np.zeros_like(M_grid)
    
    for i, alpha in enumerate(exponent_range):
        tau_grid[i, :] = collapse_time_power_law(mass_range, exponent=alpha)
    
    # Replace inf with large number for plotting
    tau_grid = np.where(np.isinf(tau_grid), 1e30, tau_grid)
    
    if save_path:
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Contour plot
        levels = np.logspace(-10, 10, 21)
        cs = ax.contourf(np.log10(M_grid), alpha_grid, np.log10(tau_grid),
                         levels=np.linspace(-10, 10, 21), cmap='viridis')
        
        # Mark critical mass
        ax.axvline(np.log10(M_C), color='red', linestyle='--', 
                   linewidth=2, label=f'$M_c$ = {M_C:.2e} kg')
        
        ax.set_xlabel('log₁₀(M / kg)', fontsize=12)
        ax.set_ylabel('Exponent α', fontsize=12)
        ax.set_title('Collapse Time Phase Portrait', fontsize=14)
        
        cbar = plt.colorbar(cs, ax=ax)
        cbar.set_label('log₁₀(τ / s)', fontsize=12)
        
        ax.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
    
    return M_grid, alpha_grid, tau_grid


# =============================================================================
# HYPOTHESIS TESTING
# =============================================================================

def test_hypothesis_H1(mass_test: float = 1e-15):
    """
    Test H1: Power law behavior of collapse time.
    
    Generates comparison of different exponents.
    """
    print("=" * 60)
    print("HYPOTHESIS H1: Power Law Collapse Time")
    print("=" * 60)
    print(f"Test mass: {mass_test:.2e} kg (M/M_c = {mass_test/M_C:.2f})")
    print()
    
    exponents = [1, 2, 4, 8]
    
    print(f"{'Exponent α':<15} {'τ (s)':<15} {'τ/τ_P':<15}")
    print("-" * 45)
    
    for alpha in exponents:
        tau = collapse_time_power_law(mass_test, exponent=alpha)
        if tau < np.inf:
            print(f"{alpha:<15} {tau[0]:<15.4e} {tau[0]/TAU_PLANCK:<15.4e}")
        else:
            print(f"{alpha:<15} {'∞':<15} {'∞':<15}")


def test_hypothesis_H2():
    """
    Test H2: Optimal exponent from phase space considerations.
    
    The expectation is α ∈ [1, 8] based on 8D phase space geometry.
    """
    print("=" * 60)
    print("HYPOTHESIS H2: Phase Space Origin of Exponent")
    print("=" * 60)
    print()
    
    # For 8D phase space, expect transitions at specific mass ratios
    print("Expected behavior for different exponents:")
    print()
    print("α = 1: Linear (Markovian, memory-less)")
    print("α = 2: Quadratic (gravitational self-energy)")
    print("α = 4: Half-phase space (entropic)")
    print("α = 8: Full 8D phase space projection")
    print()
    
    # Test at 10× M_c
    mass_test = 10 * M_C
    
    print(f"At M = 10 × M_c = {mass_test:.2e} kg:")
    for alpha in [1, 2, 4, 8]:
        tau = collapse_time_power_law(mass_test, exponent=alpha)
        print(f"  α = {alpha}: τ = {tau[0]:.4e} s")


def test_hypothesis_H3(temperature: float = 4.0, pressure: float = 1e-12):
    """
    Test H3: Intrinsic vs environmental decoherence crossover.
    
    For M < M_c, intrinsic should be negligible.
    """
    print("=" * 60)
    print("HYPOTHESIS H3: Intrinsic vs Environmental Crossover")
    print("=" * 60)
    print(f"Conditions: T = {temperature} K, P = {pressure:.1e} Pa")
    print()
    
    masses = np.array([0.1*M_C, M_C, 10*M_C, 100*M_C])
    
    print(f"{'M / M_c':<12} {'Γ_intr (s⁻¹)':<15} {'Γ_env (s⁻¹)':<15} {'Dominant':<15}")
    print("-" * 57)
    
    for m in masses:
        gamma_intr = intrinsic_decoherence_rate(np.array([m]), model="mc_power")[0]
        gamma_env = environmental_decoherence_rate(m, temperature, pressure)["total"]
        
        dominant = "INTRINSIC" if gamma_intr > gamma_env else "ENVIRONMENTAL"
        
        print(f"{m/M_C:<12.1f} {gamma_intr:<15.4e} {gamma_env:<15.4e} {dominant:<15}")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_collapse_time_vs_mass(
    save_path: str = None
):
    """
    Generate publication-quality plot of τ(M) for different models.
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    mass_range = np.logspace(-18, -12, 200)
    
    # Different exponent models
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, 4))
    exponents = [1, 2, 4, 8]
    
    for alpha, color in zip(exponents, colors):
        tau = collapse_time_power_law(mass_range, exponent=alpha)
        tau_plot = np.where(np.isinf(tau), np.nan, tau)
        ax.loglog(mass_range, tau_plot, color=color, linewidth=2,
                  label=f'α = {alpha}')
    
    # Mark M_c
    ax.axvline(M_C, color='red', linestyle='--', linewidth=2,
               label=f'$M_c$ = {M_C:.2e} kg')
    
    # Reference lines
    ax.axhline(1, color='gray', linestyle=':', alpha=0.5, label='1 second')
    ax.axhline(1e-3, color='gray', linestyle=':', alpha=0.3)
    
    ax.set_xlabel('Mass (kg)', fontsize=12)
    ax.set_ylabel('Coherence Time τ (s)', fontsize=12)
    ax.set_title('Intrinsic Coherence Time vs Mass\n(Power Law Model)', fontsize=14)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    ax.set_xlim(1e-18, 1e-12)
    ax.set_ylim(1e-15, 1e15)
    
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
    print("\n" + "=" * 60)
    print("COLLAPSE DYNAMICS SIMULATIONS")
    print("=" * 60)
    
    # Run hypothesis tests
    test_hypothesis_H1()
    print()
    test_hypothesis_H2()
    print()
    test_hypothesis_H3()
    
    # Generate plots
    print("\n" + "=" * 60)
    print("GENERATING PLOTS...")
    print("=" * 60)
    
    plot_collapse_time_vs_mass("collapse_time_vs_mass.png")
    phase_portrait(save_path="phase_portrait.png")
    
    print("\nDone!")
