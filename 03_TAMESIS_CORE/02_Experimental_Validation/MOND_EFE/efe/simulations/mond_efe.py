"""
MOND + External Field Effect (EFE) Rotation Curve Predictor

This module implements the Modified Newtonian Dynamics (MOND) framework
with the External Field Effect for predicting galaxy rotation curves.

Author: Douglas H. M. Fulber
Project: EFE Validation (TAMESIS Framework)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from dataclasses import dataclass
from typing import Tuple, Optional, Callable

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

# MOND acceleration scale (m/s^2)
# This is the characteristic acceleration below which MOND effects dominate
A0 = 1.2e-10  # Milgrom's constant

# Gravitational constant
G = 6.674e-11  # m^3 kg^-1 s^-2

# Unit conversions
KPC_TO_M = 3.086e19  # 1 kpc in meters
MSUN = 1.989e30  # Solar mass in kg
KM_S_TO_M_S = 1000  # km/s to m/s


# =============================================================================
# INTERPOLATION FUNCTIONS (mu functions)
# =============================================================================

def mu_simple(x: float) -> float:
    """
    Simple interpolation function: mu(x) = x / (1 + x)
    
    Parameters:
        x: g_N / a_0 (Newtonian acceleration normalized by MOND scale)
    
    Returns:
        mu(x) interpolation value
    """
    return x / (1.0 + x)


def mu_standard(x: float) -> float:
    """
    Standard interpolation function: mu(x) = x / sqrt(1 + x^2)
    
    This is the most commonly used form in MOND literature.
    """
    return x / np.sqrt(1.0 + x**2)


def mu_deep_mond(x: float) -> float:
    """
    Deep MOND limit: mu(x) → x for x << 1
    """
    if x < 0.01:
        return x
    return mu_standard(x)


# =============================================================================
# GALAXY MODEL
# =============================================================================

@dataclass
class GalaxyModel:
    """
    Represents a galaxy with its mass distribution and external field.
    
    Attributes:
        name: Galaxy identifier
        distance: Distance in Mpc
        luminosity: Total luminosity in solar luminosities
        mass_to_light: Mass-to-light ratio (M/L in solar units)
        scale_length: Exponential disk scale length in kpc
        g_ext: External gravitational field magnitude in m/s^2 (for EFE)
    """
    name: str
    distance: float  # Mpc
    luminosity: float  # L_sun
    mass_to_light: float  # M_sun / L_sun
    scale_length: float  # kpc
    g_ext: float = 0.0  # m/s^2 (external field for EFE)
    
    @property
    def total_mass(self) -> float:
        """Total baryonic mass in kg"""
        return self.luminosity * self.mass_to_light * MSUN
    
    def enclosed_mass(self, r_kpc: float) -> float:
        """
        Enclosed mass at radius r for exponential disk.
        Uses Freeman disk approximation.
        
        M(<r) = M_total * [1 - (1 + r/h) * exp(-r/h)]
        
        Parameters:
            r_kpc: Radius in kpc
        
        Returns:
            Enclosed mass in kg
        """
        x = r_kpc / self.scale_length
        return self.total_mass * (1.0 - (1.0 + x) * np.exp(-x))
    
    def newtonian_acceleration(self, r_kpc: float) -> float:
        """
        Newtonian gravitational acceleration at radius r.
        
        g_N = G * M(<r) / r^2
        
        Parameters:
            r_kpc: Radius in kpc
        
        Returns:
            Newtonian acceleration in m/s^2
        """
        r_m = r_kpc * KPC_TO_M
        M_enc = self.enclosed_mass(r_kpc)
        return G * M_enc / r_m**2


# =============================================================================
# MOND ROTATION CURVE CALCULATOR
# =============================================================================

class MONDCalculator:
    """
    Calculates rotation curves in MOND with optional External Field Effect.
    """
    
    def __init__(self, 
                 mu_function: Callable = mu_standard,
                 a0: float = A0):
        """
        Initialize MOND calculator.
        
        Parameters:
            mu_function: Interpolation function mu(x)
            a0: MOND acceleration scale
        """
        self.mu = mu_function
        self.a0 = a0
    
    def mond_acceleration(self, g_N: float) -> float:
        """
        Calculate MOND acceleration from Newtonian acceleration.
        
        Solves: g_N = g * mu(g / a0)
        
        Parameters:
            g_N: Newtonian acceleration
        
        Returns:
            MOND acceleration
        """
        if g_N < 1e-20:
            return 0.0
        
        # In deep MOND regime: g = sqrt(g_N * a0)
        # In Newtonian regime: g = g_N
        
        x = g_N / self.a0
        
        if x > 100:  # Newtonian regime
            return g_N
        elif x < 0.01:  # Deep MOND regime
            return np.sqrt(g_N * self.a0)
        else:
            # Solve numerically
            def equation(g):
                return g * self.mu(g / self.a0) - g_N
            
            # Bounds: between deep MOND and Newtonian
            g_min = np.sqrt(g_N * self.a0) * 0.5
            g_max = g_N * 2.0
            
            try:
                return brentq(equation, g_min, g_max)
            except ValueError:
                # Fallback to simple formula
                return np.sqrt(g_N * self.a0) if x < 1 else g_N
    
    def mond_acceleration_with_efe(self, 
                                    g_N: float, 
                                    g_ext: float,
                                    theta: float = 0.0) -> float:
        """
        Calculate MOND acceleration WITH External Field Effect.
        
        The EFE modifies the effective mu function when an external
        field g_ext is present.
        
        Parameters:
            g_N: Internal Newtonian acceleration
            g_ext: External field magnitude
            theta: Angle between internal and external field
        
        Returns:
            MOND acceleration with EFE
        """
        if g_ext < 1e-15:
            return self.mond_acceleration(g_N)
        
        # Effective acceleration including external field
        # This is a simplified 1D treatment
        g_total = np.sqrt(g_N**2 + g_ext**2 + 2*g_N*g_ext*np.cos(theta))
        
        # In strong external field (g_ext >> g_N), MOND effects are suppressed
        x_ext = g_ext / self.a0
        
        if x_ext > 1:
            # External field dominates: quasi-Newtonian regime
            # The internal dynamics become approximately Newtonian
            # but with a renormalized G
            mu_ext = self.mu(x_ext)
            g_efe = g_N / mu_ext
            return g_efe
        else:
            # Mixed regime: solve full equation
            return self.mond_acceleration(g_total) * (g_N / g_total)
    
    def rotation_velocity(self, 
                          galaxy: GalaxyModel, 
                          r_kpc: float,
                          include_efe: bool = True) -> float:
        """
        Calculate rotation velocity at radius r.
        
        v = sqrt(g * r)
        
        Parameters:
            galaxy: Galaxy model
            r_kpc: Radius in kpc
            include_efe: Whether to include External Field Effect
        
        Returns:
            Rotation velocity in km/s
        """
        g_N = galaxy.newtonian_acceleration(r_kpc)
        
        if include_efe and galaxy.g_ext > 0:
            g_mond = self.mond_acceleration_with_efe(g_N, galaxy.g_ext)
        else:
            g_mond = self.mond_acceleration(g_N)
        
        r_m = r_kpc * KPC_TO_M
        v_m_s = np.sqrt(g_mond * r_m)
        
        return v_m_s / KM_S_TO_M_S
    
    def rotation_curve(self,
                       galaxy: GalaxyModel,
                       r_array: np.ndarray,
                       include_efe: bool = True) -> np.ndarray:
        """
        Calculate full rotation curve.
        
        Parameters:
            galaxy: Galaxy model
            r_array: Array of radii in kpc
            include_efe: Whether to include EFE
        
        Returns:
            Array of rotation velocities in km/s
        """
        return np.array([
            self.rotation_velocity(galaxy, r, include_efe) 
            for r in r_array
        ])


# =============================================================================
# NEWTONIAN (LAMBDA-CDM) CALCULATOR FOR COMPARISON
# =============================================================================

class NewtonianCalculator:
    """
    Standard Newtonian rotation curve (no dark matter, no MOND).
    This represents pure baryonic prediction.
    """
    
    def rotation_velocity(self, galaxy: GalaxyModel, r_kpc: float) -> float:
        """Calculate Newtonian rotation velocity (baryons only)."""
        g_N = galaxy.newtonian_acceleration(r_kpc)
        r_m = r_kpc * KPC_TO_M
        v_m_s = np.sqrt(g_N * r_m) if g_N > 0 else 0
        return v_m_s / KM_S_TO_M_S
    
    def rotation_curve(self, galaxy: GalaxyModel, r_array: np.ndarray) -> np.ndarray:
        """Calculate full Newtonian rotation curve."""
        return np.array([self.rotation_velocity(galaxy, r) for r in r_array])


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_rotation_curves(galaxy: GalaxyModel,
                         r_array: np.ndarray,
                         observed_v: Optional[np.ndarray] = None,
                         observed_err: Optional[np.ndarray] = None,
                         save_path: Optional[str] = None):
    """
    Plot comparison of rotation curve predictions.
    
    Parameters:
        galaxy: Galaxy model
        r_array: Radii array in kpc
        observed_v: Observed velocities (optional)
        observed_err: Velocity errors (optional)
        save_path: Path to save figure
    """
    mond_calc = MONDCalculator()
    newton_calc = NewtonianCalculator()
    
    # Calculate predictions
    v_newton = newton_calc.rotation_curve(galaxy, r_array)
    v_mond_no_efe = mond_calc.rotation_curve(galaxy, r_array, include_efe=False)
    v_mond_with_efe = mond_calc.rotation_curve(galaxy, r_array, include_efe=True)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot predictions
    ax.plot(r_array, v_newton, 'b--', label='Newtonian (baryons only)', linewidth=1.5)
    ax.plot(r_array, v_mond_no_efe, 'g-', label='MOND (no EFE)', linewidth=2)
    
    if galaxy.g_ext > 0:
        ax.plot(r_array, v_mond_with_efe, 'r-', label='MOND (with EFE)', linewidth=2)
    
    # Plot observations if available
    if observed_v is not None:
        if observed_err is not None:
            ax.errorbar(r_array[:len(observed_v)], observed_v, yerr=observed_err,
                       fmt='ko', markersize=5, capsize=3, label='Observed')
        else:
            ax.plot(r_array[:len(observed_v)], observed_v, 'ko', 
                   markersize=5, label='Observed')
    
    # Labels and formatting
    ax.set_xlabel('Radius (kpc)', fontsize=12)
    ax.set_ylabel('Rotation Velocity (km/s)', fontsize=12)
    ax.set_title(f'Rotation Curve: {galaxy.name}', fontsize=14)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, r_array[-1])
    ax.set_ylim(0, None)
    
    # Add external field annotation if present
    if galaxy.g_ext > 0:
        g_ext_normalized = galaxy.g_ext / A0
        ax.annotate(f'$g_{{ext}}/a_0 = {g_ext_normalized:.2f}$',
                   xy=(0.02, 0.98), xycoords='axes fraction',
                   fontsize=10, ha='left', va='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


# =============================================================================
# EXAMPLE: TEST WITH A SYNTHETIC GALAXY
# =============================================================================

def main():
    """Run example calculation."""
    
    print("=" * 60)
    print("MOND + EFE Rotation Curve Calculator")
    print("=" * 60)
    
    # Create example galaxy (similar to a dwarf satellite)
    galaxy_isolated = GalaxyModel(
        name="Isolated Dwarf",
        distance=0.1,  # Mpc
        luminosity=1e8,  # L_sun
        mass_to_light=2.0,  # M/L
        scale_length=1.5,  # kpc
        g_ext=0.0  # No external field
    )
    
    # Same galaxy but in external field (satellite of Milky Way)
    galaxy_satellite = GalaxyModel(
        name="Satellite Dwarf (in MW field)",
        distance=0.1,
        luminosity=1e8,
        mass_to_light=2.0,
        scale_length=1.5,
        g_ext=1.5e-10  # MW field at ~50 kpc
    )
    
    # Radius array
    r_array = np.linspace(0.1, 10.0, 100)
    
    # Calculate and compare
    mond = MONDCalculator()
    
    v_isolated = mond.rotation_curve(galaxy_isolated, r_array, include_efe=False)
    v_satellite_no_efe = mond.rotation_curve(galaxy_satellite, r_array, include_efe=False)
    v_satellite_efe = mond.rotation_curve(galaxy_satellite, r_array, include_efe=True)
    
    print(f"\nGalaxy: {galaxy_isolated.name}")
    print(f"  Total Mass: {galaxy_isolated.total_mass/MSUN:.2e} M_sun")
    print(f"  V_max (MOND): {max(v_isolated):.1f} km/s")
    
    print(f"\nGalaxy: {galaxy_satellite.name}")
    print(f"  External Field: {galaxy_satellite.g_ext:.2e} m/s^2")
    print(f"  g_ext / a0: {galaxy_satellite.g_ext/A0:.2f}")
    print(f"  V_max (MOND no EFE): {max(v_satellite_no_efe):.1f} km/s")
    print(f"  V_max (MOND with EFE): {max(v_satellite_efe):.1f} km/s")
    print(f"  EFE suppression: {(1 - max(v_satellite_efe)/max(v_satellite_no_efe))*100:.1f}%")
    
    # Plot comparison
    print("\nGenerating comparison plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Isolated dwarf
    ax1 = axes[0]
    newton = NewtonianCalculator()
    v_newton = newton.rotation_curve(galaxy_isolated, r_array)
    
    ax1.plot(r_array, v_newton, 'b--', label='Newtonian', linewidth=1.5)
    ax1.plot(r_array, v_isolated, 'g-', label='MOND', linewidth=2)
    ax1.set_xlabel('Radius (kpc)')
    ax1.set_ylabel('V (km/s)')
    ax1.set_title(f'{galaxy_isolated.name}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right: Satellite (EFE comparison)
    ax2 = axes[1]
    ax2.plot(r_array, v_satellite_no_efe, 'g--', label='MOND (no EFE)', linewidth=1.5)
    ax2.plot(r_array, v_satellite_efe, 'r-', label='MOND (with EFE)', linewidth=2)
    ax2.set_xlabel('Radius (kpc)')
    ax2.set_ylabel('V (km/s)')
    ax2.set_title(f'{galaxy_satellite.name}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.annotate(f'$g_{{ext}}/a_0 = {galaxy_satellite.g_ext/A0:.2f}$',
                xy=(0.02, 0.98), xycoords='axes fraction',
                fontsize=10, ha='left', va='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('efe_comparison.png', dpi=150)
    print("Saved: efe_comparison.png")
    plt.show()
    
    print("\n" + "=" * 60)
    print("KEY PREDICTION (Falsification Criterion):")
    print("=" * 60)
    print("""
If EFE is real (MOND/Entropic Gravity):
  - Satellite galaxies in strong external fields show LOWER 
    rotation velocities than identical isolated galaxies
  - The suppression scales with g_ext / a0

If EFE is NOT real (Lambda-CDM):
  - Internal dynamics are independent of external field
  - No systematic difference between satellite and isolated dwarfs
    (after accounting for tidal effects)
    
KILL CONDITION: If satellites show NO EFE signature despite 
sitting in strong external fields, entropic gravity is falsified.
""")


if __name__ == "__main__":
    main()
