"""
Decoherence Models Comparison
=============================

This module implements multiple collapse/decoherence models for
systematic comparison and experimental discrimination:

1. M_c Model (This work): Cosmological acceleration-based collapse
2. CSL (Continuous Spontaneous Localization): Adler, Bassi et al.
3. GRW (Ghirardi-Rimini-Weber): Historical collapse model
4. DP (Diósi-Penrose): Gravitational self-energy collapse

Each model provides different predictions for:
- Collapse time τ(M) as function of mass
- Decoherence rate Γ(M, Δx) as function of mass and separation
- Heating rate (motional energy increase)
- Interference visibility decay

The goal is to identify experimental scenarios that DISCRIMINATE
between models, not just detect collapse.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple
from abc import ABC, abstractmethod

# Import constants
from .constants import (
    M_C, M_PLANCK, TAU_PLANCK, HBAR, G_SI, C,
    CSL_LAMBDA, CSL_R_C, GRW_LAMBDA, GRW_A
)


# =============================================================================
# ABSTRACT BASE CLASS FOR COLLAPSE MODELS
# =============================================================================

@dataclass
class CollapseModelPrediction:
    """Container for model predictions."""
    collapse_time: float  # seconds
    decoherence_rate: float  # s⁻¹
    heating_rate: float  # K/s (temperature increase)
    visibility_decay_rate: float  # s⁻¹
    
    def __repr__(self):
        return (f"CollapseModelPrediction(\n"
                f"  τ = {self.collapse_time:.4e} s,\n"
                f"  Γ = {self.decoherence_rate:.4e} s⁻¹,\n"
                f"  dT/dt = {self.heating_rate:.4e} K/s,\n"
                f"  Γ_vis = {self.visibility_decay_rate:.4e} s⁻¹\n)")


class CollapseModel(ABC):
    """Abstract base class for collapse models."""
    
    name: str = "Abstract"
    
    @abstractmethod
    def collapse_time(self, mass: float, delta_x: float) -> float:
        """Calculate collapse/decoherence time."""
        pass
    
    @abstractmethod
    def decoherence_rate(self, mass: float, delta_x: float) -> float:
        """Calculate decoherence rate Γ."""
        pass
    
    def heating_rate(self, mass: float, delta_x: float, 
                    omega_mech: float = 1e5) -> float:
        """
        Calculate momentum diffusion heating rate.
        
        For optomechanical systems, collapse models predict
        heating via momentum kicks.
        """
        # Default: heating ~ Γ × (ℏω_mech)² / (m × k_B)
        gamma = self.decoherence_rate(mass, delta_x)
        k_B = 1.38e-23
        return gamma * (HBAR * omega_mech)**2 / (mass * k_B)
    
    def visibility_decay_rate(self, mass: float, delta_x: float) -> float:
        """
        Calculate interference visibility decay rate.
        
        V(t) = V_0 × exp(-Γ_vis × t)
        """
        # Usually same as decoherence rate
        return self.decoherence_rate(mass, delta_x)
    
    def predict(self, mass: float, delta_x: float, 
               omega_mech: float = 1e5) -> CollapseModelPrediction:
        """Generate full prediction for experimental comparison."""
        return CollapseModelPrediction(
            collapse_time=self.collapse_time(mass, delta_x),
            decoherence_rate=self.decoherence_rate(mass, delta_x),
            heating_rate=self.heating_rate(mass, delta_x, omega_mech),
            visibility_decay_rate=self.visibility_decay_rate(mass, delta_x)
        )


# =============================================================================
# MODEL IMPLEMENTATIONS
# =============================================================================

class MCModel(CollapseModel):
    """
    Critical Mass Model (This Work)
    ================================
    
    Based on cosmological acceleration horizon:
    
    M_c = m_P × (a_0 / a_P)^(1/8) ≈ 5.3 × 10⁻¹⁶ kg
    
    For M > M_c, unitarity violation occurs.
    
    Parameters:
    -----------
    exponent : float
        Power law exponent (default 2, range 1-8)
    tau_scale : float
        Reference time scale (derived from Planck units)
    """
    
    name = "M_c Critical Mass"
    
    def __init__(self, exponent: float = 2.0, tau_scale: float = None):
        self.exponent = exponent
        # Default: geometric mean of Planck and cosmological times
        self.tau_scale = tau_scale or 1e-5  # ~10 µs reference
    
    def collapse_time(self, mass: float, delta_x: float) -> float:
        """
        τ(M) = τ_scale × (M_c / M)^α × (λ_c / Δx)^2
        
        where λ_c = ℏ / (M_c × c) is the Compton wavelength at M_c.
        """
        if mass <= M_C:
            return np.inf
        
        lambda_c = HBAR / (M_C * C)
        spatial_factor = (lambda_c / delta_x)**2
        
        tau = self.tau_scale * (M_C / mass)**self.exponent * spatial_factor
        return tau
    
    def decoherence_rate(self, mass: float, delta_x: float) -> float:
        """Γ = 1/τ for finite τ, else 0."""
        tau = self.collapse_time(mass, delta_x)
        if np.isinf(tau):
            return 0.0
        return 1.0 / tau


class CSLModel(CollapseModel):
    """
    Continuous Spontaneous Localization (CSL)
    ==========================================
    
    Adler, Bassi et al.
    
    Key parameters:
    - λ_CSL ≈ 10⁻¹⁶ s⁻¹ (collapse rate per nucleon)
    - r_C ≈ 10⁻⁷ m (correlation length)
    
    Decoherence rate:
    Γ_CSL ≈ λ × (m / m_0)² × f(Δx, r_C)
    
    where f is a localization function.
    """
    
    name = "CSL"
    
    def __init__(self, lambda_csl: float = 1e-16, r_c: float = 1e-7):
        self.lambda_csl = lambda_csl
        self.r_c = r_c
        self.m_nucleon = 1.67e-27  # kg
    
    def collapse_time(self, mass: float, delta_x: float) -> float:
        gamma = self.decoherence_rate(mass, delta_x)
        if gamma == 0:
            return np.inf
        return 1.0 / gamma
    
    def decoherence_rate(self, mass: float, delta_x: float) -> float:
        """
        Γ_CSL = λ × (m / m_nucleon)² × [1 - exp(-(Δx/r_C)²)]
        """
        n_nucleons = mass / self.m_nucleon
        
        # Spatial localization factor
        if delta_x < 1e-15:  # Very small separation
            return 0.0
        
        spatial_factor = 1 - np.exp(-(delta_x / self.r_c)**2)
        
        return self.lambda_csl * n_nucleons**2 * spatial_factor


class GRWModel(CollapseModel):
    """
    Ghirardi-Rimini-Weber (GRW) Model
    ==================================
    
    Original spontaneous collapse model.
    
    Parameters:
    - λ_GRW ≈ 10⁻¹⁶ s⁻¹ (hits per particle)
    - a ≈ 10⁻⁷ m (localization width)
    
    Each particle experiences random localization "hits".
    """
    
    name = "GRW"
    
    def __init__(self, lambda_grw: float = 1e-16, a: float = 1e-7):
        self.lambda_grw = lambda_grw
        self.a = a
        self.m_nucleon = 1.67e-27
    
    def collapse_time(self, mass: float, delta_x: float) -> float:
        gamma = self.decoherence_rate(mass, delta_x)
        if gamma == 0:
            return np.inf
        return 1.0 / gamma
    
    def decoherence_rate(self, mass: float, delta_x: float) -> float:
        """
        Γ_GRW = N × λ × [1 - exp(-(Δx/a)²)]
        
        where N is number of particles.
        """
        n_particles = mass / self.m_nucleon
        
        if delta_x < 1e-15:
            return 0.0
        
        spatial_factor = 1 - np.exp(-(delta_x / self.a)**2)
        
        return n_particles * self.lambda_grw * spatial_factor


class DiosiPenroseModel(CollapseModel):
    """
    Diósi-Penrose Gravitational Collapse
    =====================================
    
    Gravitational self-energy induces collapse.
    
    τ_DP ≈ ℏ / E_grav
    E_grav ≈ G m² R⁻¹
    
    where R is the size/separation scale.
    
    This gives: τ_DP ≈ ℏ R / (G m²)
    """
    
    name = "Diósi-Penrose"
    
    def __init__(self, reduction_factor: float = 1.0):
        self.reduction_factor = reduction_factor
    
    def collapse_time(self, mass: float, delta_x: float) -> float:
        """
        τ_DP = ℏ × Δx / (G × m²)
        """
        if delta_x <= 0 or mass <= 0:
            return np.inf
        
        E_grav = G_SI * mass**2 / delta_x
        tau = HBAR / (E_grav * self.reduction_factor)
        
        return tau
    
    def decoherence_rate(self, mass: float, delta_x: float) -> float:
        tau = self.collapse_time(mass, delta_x)
        if np.isinf(tau):
            return 0.0
        return 1.0 / tau


# =============================================================================
# COMPARISON FUNCTIONS
# =============================================================================

def compare_models_mass_scan(
    mass_range: np.ndarray = None,
    delta_x: float = 1e-6,
    save_path: str = None
) -> Dict[str, np.ndarray]:
    """
    Compare all models across mass range.
    
    Parameters:
    -----------
    mass_range : np.ndarray
        Masses to evaluate (kg)
    delta_x : float
        Fixed superposition separation (m)
    save_path : str
        Path to save figure
    
    Returns:
    --------
    results : dict
        Dictionary with model names and decoherence rates
    """
    if mass_range is None:
        mass_range = np.logspace(-18, -10, 200)
    
    models = {
        "M_c (α=2)": MCModel(exponent=2),
        "M_c (α=4)": MCModel(exponent=4),
        "CSL": CSLModel(),
        "GRW": GRWModel(),
        "Diósi-Penrose": DiosiPenroseModel()
    }
    
    results = {"mass": mass_range}
    
    for name, model in models.items():
        gamma = np.array([model.decoherence_rate(m, delta_x) for m in mass_range])
        results[name] = gamma
    
    # Plotting
    if save_path:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = plt.cm.tab10(range(len(models)))
        linestyles = ['-', '--', '-', '-', '-']
        
        for (name, gamma), color, ls in zip(
            [(k, results[k]) for k in models.keys()], colors, linestyles
        ):
            # Mask zeros for log plot
            gamma_plot = np.where(gamma > 0, gamma, np.nan)
            ax.loglog(mass_range, gamma_plot, color=color, linestyle=ls,
                     linewidth=2, label=name)
        
        # Mark critical mass
        ax.axvline(M_C, color='red', linestyle=':', linewidth=2,
                   label=f'$M_c$ = {M_C:.2e} kg')
        
        # Reference: 1/s (detectable in typical experiments)
        ax.axhline(1, color='gray', linestyle='--', alpha=0.5, 
                   label='Γ = 1 s⁻¹')
        ax.axhline(1e-3, color='gray', linestyle=':', alpha=0.3)
        
        ax.set_xlabel('Mass (kg)', fontsize=14)
        ax.set_ylabel('Decoherence Rate Γ (s⁻¹)', fontsize=14)
        ax.set_title(f'Collapse Models Comparison\n(Δx = {delta_x:.0e} m)', fontsize=16)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(mass_range[0], mass_range[-1])
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        print(f"Saved: {save_path}")
        plt.close()
    
    return results


def compare_models_spatial_scan(
    delta_x_range: np.ndarray = None,
    mass: float = 1e-15,
    save_path: str = None
) -> Dict[str, np.ndarray]:
    """
    Compare models across spatial separation range.
    
    This is crucial for discriminating models: they have different
    Δx dependencies.
    """
    if delta_x_range is None:
        delta_x_range = np.logspace(-9, -3, 200)
    
    models = {
        "M_c (α=2)": MCModel(exponent=2),
        "CSL": CSLModel(),
        "GRW": GRWModel(),
        "Diósi-Penrose": DiosiPenroseModel()
    }
    
    results = {"delta_x": delta_x_range}
    
    for name, model in models.items():
        gamma = np.array([model.decoherence_rate(mass, dx) for dx in delta_x_range])
        results[name] = gamma
    
    if save_path:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = plt.cm.tab10(range(len(models)))
        
        for (name, gamma), color in zip(
            [(k, results[k]) for k in models.keys()], colors
        ):
            gamma_plot = np.where(gamma > 0, gamma, np.nan)
            ax.loglog(delta_x_range, gamma_plot, color=color,
                     linewidth=2, label=name)
        
        ax.set_xlabel('Superposition Separation Δx (m)', fontsize=14)
        ax.set_ylabel('Decoherence Rate Γ (s⁻¹)', fontsize=14)
        ax.set_title(f'Collapse Models: Spatial Dependence\n(M = {mass:.0e} kg)', fontsize=16)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        print(f"Saved: {save_path}")
        plt.close()
    
    return results


def find_discrimination_region(
    model_A: CollapseModel,
    model_B: CollapseModel,
    mass_range: np.ndarray = None,
    delta_x_range: np.ndarray = None,
    threshold_ratio: float = 10.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Find regions where models differ by more than threshold.
    
    Parameters:
    -----------
    model_A, model_B : CollapseModel
        Models to compare
    mass_range, delta_x_range : np.ndarray
        Parameter space to search
    threshold_ratio : float
        Minimum ratio |Γ_A / Γ_B| to consider "discriminable"
    
    Returns:
    --------
    discrimination_masses, discrimination_dx : np.ndarray
        Coordinates where discrimination is possible
    """
    if mass_range is None:
        mass_range = np.logspace(-17, -12, 50)
    if delta_x_range is None:
        delta_x_range = np.logspace(-8, -4, 50)
    
    M_grid, DX_grid = np.meshgrid(mass_range, delta_x_range)
    
    ratio_grid = np.zeros_like(M_grid)
    
    for i, dx in enumerate(delta_x_range):
        for j, m in enumerate(mass_range):
            gamma_A = model_A.decoherence_rate(m, dx)
            gamma_B = model_B.decoherence_rate(m, dx)
            
            if gamma_A > 0 and gamma_B > 0:
                ratio = max(gamma_A / gamma_B, gamma_B / gamma_A)
            else:
                ratio = np.inf if (gamma_A > 0) != (gamma_B > 0) else 1.0
            
            ratio_grid[i, j] = ratio
    
    # Find discriminable regions
    discriminable = ratio_grid >= threshold_ratio
    
    return M_grid, DX_grid, ratio_grid, discriminable


# =============================================================================
# EXPERIMENTAL PREDICTIONS
# =============================================================================

def predict_cantilever_noise(
    mass: float = 1e-15,
    frequency_hz: float = 1e5,
    temperature: float = 4.0,
    model: CollapseModel = None
) -> dict:
    """
    Predict excess noise in mechanical resonator experiments.
    
    Parameters:
    -----------
    mass : float
        Effective mass of resonator (kg)
    frequency_hz : float
        Mechanical frequency (Hz)
    temperature : float
        Environment temperature (K)
    model : CollapseModel
        Collapse model to use (default: M_c)
    
    Returns:
    --------
    predictions : dict
        - thermal_noise: Standard quantum limit noise
        - intrinsic_noise: Collapse model contribution
        - total_noise: Sum in quadrature
        - signal_to_excess: Detectability metric
    """
    if model is None:
        model = MCModel(exponent=2)
    
    omega = 2 * np.pi * frequency_hz
    k_B = 1.38e-23
    
    # Ground state position uncertainty
    x_zpf = np.sqrt(HBAR / (2 * mass * omega))
    
    # Thermal occupation
    n_th = k_B * temperature / (HBAR * omega)
    
    # Thermal noise PSD (m²/Hz)
    S_thermal = 4 * k_B * temperature / (mass * omega**2) * 1e-10  # Rough Q factor
    
    # Collapse-induced noise
    # Assume Δx ~ x_zpf for ground state superposition
    gamma = model.decoherence_rate(mass, x_zpf)
    
    # Collapse kicks add momentum diffusion
    # PSD from collapse: S_collapse ~ ℏ² Γ / m²
    S_collapse = HBAR**2 * gamma / mass**2
    
    # Total noise
    S_total = np.sqrt(S_thermal**2 + S_collapse**2)
    
    return {
        "thermal_psd": S_thermal,
        "collapse_psd": S_collapse,
        "total_psd": S_total,
        "excess_ratio": S_collapse / S_thermal if S_thermal > 0 else np.inf,
        "gamma_collapse": gamma
    }


def predict_visibility_decay(
    mass: float,
    delta_x: float,
    time_array: np.ndarray,
    model: CollapseModel = None
) -> np.ndarray:
    """
    Predict interference visibility as function of time.
    
    V(t) = V_0 × exp(-Γ × t)
    """
    if model is None:
        model = MCModel(exponent=2)
    
    gamma = model.visibility_decay_rate(mass, delta_x)
    return np.exp(-gamma * time_array)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DECOHERENCE MODELS COMPARISON")
    print("=" * 60)
    
    # Test all models at M = 10 × M_c
    test_mass = 10 * M_C
    test_dx = 1e-6
    
    models = [
        MCModel(exponent=2),
        MCModel(exponent=4),
        CSLModel(),
        GRWModel(),
        DiosiPenroseModel()
    ]
    
    print(f"\nTest conditions: M = {test_mass:.2e} kg, Δx = {test_dx:.0e} m")
    print()
    print(f"{'Model':<20} {'τ (s)':<15} {'Γ (s⁻¹)':<15}")
    print("-" * 50)
    
    for model in models:
        pred = model.predict(test_mass, test_dx)
        print(f"{model.name:<20} {pred.collapse_time:<15.4e} {pred.decoherence_rate:<15.4e}")
    
    # Generate comparison plots
    print("\n" + "=" * 60)
    print("GENERATING PLOTS...")
    print("=" * 60)
    
    compare_models_mass_scan(save_path="models_mass_comparison.png")
    compare_models_spatial_scan(save_path="models_spatial_comparison.png")
    
    # Cantilever noise prediction
    print("\n" + "=" * 60)
    print("CANTILEVER NOISE PREDICTION")
    print("=" * 60)
    
    noise_pred = predict_cantilever_noise(mass=1e-15, frequency_hz=1e5, temperature=4.0)
    print(f"Thermal PSD: {noise_pred['thermal_psd']:.4e} m²/Hz")
    print(f"Collapse PSD: {noise_pred['collapse_psd']:.4e} m²/Hz")
    print(f"Excess ratio: {noise_pred['excess_ratio']:.4e}")
    
    print("\nDone!")
