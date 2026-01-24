"""
Laboratory-Scale Entropic Gravity Calculator

This module calculates expected entropic gravity corrections
for laboratory-scale experiments.

Key Questions:
1. At what scale do MOND effects become detectable?
2. Can the External Field Effect manifest in lab systems?
3. What precision is needed to detect entropic corrections?

Author: Douglas H. M. Fulber
Project: Lab Gravity - TAMESIS Framework
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional

# =============================================================================
# CONSTANTS
# =============================================================================

# Fundamental constants
G = 6.674e-11  # m^3 kg^-1 s^-2
c = 2.998e8    # m/s
hbar = 1.055e-34  # J·s
kB = 1.381e-23  # J/K

# MOND scale
A0 = 1.2e-10  # m/s^2 - MOND acceleration threshold

# Earth's gravity
G_EARTH = 9.81  # m/s^2

# Masses
M_SUN = 1.989e30  # kg
M_EARTH = 5.972e24  # kg

# Distances
R_EARTH = 6.371e6  # m
AU = 1.496e11  # m


# =============================================================================
# MOND FUNCTIONS
# =============================================================================

def mond_interpolation(g_newton: float, a0: float = A0) -> float:
    """
    Calculate MOND acceleration from Newtonian acceleration.
    
    Uses standard interpolation function:
    g_mond = g_N / μ(g_mond/a0)
    
    Solved iteratively.
    """
    if g_newton <= 0:
        return 0
    
    # In deep MOND (g << a0): g_mond = sqrt(g_N * a0)
    # In Newtonian (g >> a0): g_mond = g_N
    
    x = g_newton / a0
    
    # Standard interpolation function
    # μ(x) = x / sqrt(1 + x^2)
    # This gives: g_mond = g_N * sqrt(1 + (a0/g_mond)^2)
    
    # For g_N >> a0: g_mond ≈ g_N
    # For g_N << a0: g_mond ≈ sqrt(g_N * a0)
    
    # Simple interpolation
    if x > 100:
        return g_newton  # Newtonian limit
    elif x < 0.01:
        return np.sqrt(g_newton * a0)  # Deep MOND
    else:
        # Full calculation
        # g_mond = g_N / μ where μ = g_mond/a0 / sqrt(1 + (g_mond/a0)^2)
        # Approximately: g_mond ≈ g_N * sqrt(1 + a0^2/g_N^2) / 2 + corrections
        
        # Iterative solution
        g_mond = g_newton
        for _ in range(10):
            x_m = g_mond / a0
            mu = x_m / np.sqrt(1 + x_m**2)
            g_mond = g_newton / mu
        
        return g_mond


def mond_correction_factor(g_newton: float, a0: float = A0) -> float:
    """
    Calculate the MOND correction factor: g_mond / g_newton.
    
    Returns 1 in Newtonian regime, >1 in MOND regime.
    """
    g_mond = mond_interpolation(g_newton, a0)
    return g_mond / g_newton if g_newton > 0 else 1.0


def external_field_effect(g_internal: float, g_external: float, 
                          a0: float = A0) -> float:
    """
    Calculate effective acceleration with External Field Effect.
    
    When g_external > a0, the MOND boost is suppressed.
    """
    if g_external < 0.01 * a0:
        # No external field - full MOND
        return mond_interpolation(g_internal, a0)
    
    if g_external > 10 * a0:
        # Strong external field - quasi-Newtonian
        return g_internal
    
    # Intermediate regime
    x_ext = g_external / a0
    mu_ext = x_ext / np.sqrt(1 + x_ext**2)
    
    # The effective MOND boost is suppressed
    g_mond_full = mond_interpolation(g_internal, a0)
    boost = g_mond_full / g_internal if g_internal > 0 else 1.0
    
    # Reduce boost by external field
    effective_boost = 1 + (boost - 1) * (1 - mu_ext)
    
    return g_internal * effective_boost


# =============================================================================
# LABORATORY SYSTEMS
# =============================================================================

@dataclass
class LabExperiment:
    """Represents a laboratory gravity experiment."""
    name: str
    test_mass: float  # kg
    source_mass: float  # kg
    separation: float  # m
    measurement_precision: float  # m/s^2
    
    @property
    def newtonian_acceleration(self) -> float:
        """Newtonian acceleration of test mass due to source."""
        return G * self.source_mass / self.separation**2
    
    @property
    def mond_acceleration(self) -> float:
        """MOND acceleration (with Earth as external field)."""
        return external_field_effect(
            self.newtonian_acceleration, 
            G_EARTH
        )
    
    @property
    def mond_correction(self) -> float:
        """Fractional MOND correction: (g_mond - g_newton) / g_newton."""
        return (self.mond_acceleration - self.newtonian_acceleration) / \
               self.newtonian_acceleration if self.newtonian_acceleration > 0 else 0
    
    @property
    def is_detectable(self) -> bool:
        """Is the MOND correction larger than measurement precision?"""
        delta_g = abs(self.mond_acceleration - self.newtonian_acceleration)
        return delta_g > self.measurement_precision


def create_standard_experiments() -> List[LabExperiment]:
    """Create list of standard laboratory gravity experiments."""
    
    experiments = [
        LabExperiment(
            name="Cavendish (classic)",
            test_mass=0.01,  # 10 g
            source_mass=1.0,  # 1 kg lead ball
            separation=0.1,  # 10 cm
            measurement_precision=1e-10  # m/s^2
        ),
        LabExperiment(
            name="Eöt-Wash torsion balance",
            test_mass=0.001,  # 1 g
            source_mass=10.0,  # 10 kg
            separation=0.05,  # 5 cm
            measurement_precision=1e-13  # m/s^2 (state of art)
        ),
        LabExperiment(
            name="Atom interferometer",
            test_mass=1.44e-25,  # Rb atom
            source_mass=500,  # 500 kg source
            separation=1.0,  # 1 m
            measurement_precision=1e-11  # m/s^2
        ),
        LabExperiment(
            name="MICROSCOPE satellite",
            test_mass=0.4,  # 400 g
            source_mass=M_EARTH,
            separation=R_EARTH + 700e3,  # 700 km orbit
            measurement_precision=1e-15  # m/s^2
        ),
        LabExperiment(
            name="Hypothetical MOND detector",
            test_mass=0.001,
            source_mass=100,
            separation=0.01,  # 1 cm
            measurement_precision=1e-15  # Required precision
        ),
    ]
    
    return experiments


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_lab_feasibility():
    """Analyze feasibility of detecting MOND in laboratory."""
    
    print("=" * 70)
    print("LABORATORY ENTROPIC GRAVITY FEASIBILITY ANALYSIS")
    print("=" * 70)
    
    # First, show the scale of the problem
    print("\n[1] The Scale Problem:")
    print(f"    MOND threshold a₀ = {A0:.2e} m/s²")
    print(f"    Earth surface g  = {G_EARTH:.2f} m/s²")
    print(f"    Ratio: g_Earth / a₀ = {G_EARTH/A0:.2e}")
    print("\n    Earth's gravity is ~10¹¹ times stronger than a₀!")
    print("    This means we're DEEP in the Newtonian regime.")
    
    # Analyze experiments
    print("\n[2] Laboratory Experiment Analysis:")
    print("-" * 70)
    
    experiments = create_standard_experiments()
    
    for exp in experiments:
        print(f"\n    {exp.name}:")
        print(f"      Newtonian g:     {exp.newtonian_acceleration:.3e} m/s²")
        print(f"      MOND g:          {exp.mond_acceleration:.3e} m/s²")
        print(f"      Correction:      {exp.mond_correction*100:.6f}%")
        print(f"      Precision:       {exp.measurement_precision:.3e} m/s²")
        print(f"      Detectable:      {'YES' if exp.is_detectable else 'NO'}")
    
    # The EFE insight
    print("\n" + "=" * 70)
    print("[3] THE EXTERNAL FIELD EFFECT INSIGHT")
    print("=" * 70)
    
    print("""
    We now know (from SPARC data) that the External Field Effect is REAL.
    
    Earth's gravitational field acts as an EXTERNAL FIELD for any 
    laboratory experiment. This SUPPRESSES any MOND enhancement.
    
    This means:
    - Laboratory experiments on Earth CANNOT detect pure MOND effects
    - The EFE "shields" us from the low-acceleration regime
    - We need to go to SPACE (away from massive bodies) to see MOND
    """)
    
    # Alternative approaches
    print("\n" + "=" * 70)
    print("[4] ALTERNATIVE APPROACHES")
    print("=" * 70)
    
    print("""
    1. SPACE-BASED EXPERIMENTS
       - Far from Sun/Earth, g_ext → 0
       - Pioneer anomaly might have been EFE signature
       - LISA Pathfinder data could be reanalyzed
    
    2. DIFFERENTIAL MEASUREMENTS
       - Compare vertical vs horizontal accelerations
       - Look for directional dependence (toward galactic center)
    
    3. COSMOLOGICAL TESTS
       - CMB anomalies at large angular scales
       - Galaxy cluster dynamics
       - Gravitational lensing statistics
    
    4. PULSAR TIMING
       - Ultra-precise timing in different galactic environments
       - Look for EFE on pulsar orbital dynamics
    """)
    
    # Conclusion
    print("\n" + "=" * 70)
    print("[5] CONCLUSION")
    print("=" * 70)
    
    print("""
    VERDICT: Direct laboratory detection of MOND is NOT FEASIBLE
    
    Reasons:
    1. Earth's gravity is 10¹¹ times a₀ - too strong
    2. External Field Effect suppresses any MOND boost
    3. Required precision (10⁻¹⁵ m/s² or better) is at technology limit
    
    Best path forward:
    → Use SPACE-BASED missions in weak gravitational environments
    → Analyze existing spacecraft tracking data for anomalies
    → Focus on ASTROPHYSICAL tests (which we already confirmed with EFE!)
    """)
    
    return experiments


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    experiments = analyze_lab_feasibility()
