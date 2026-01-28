"""
Physical Constants for M_c Research
====================================

This module defines all fundamental constants and derived scales
used in the critical mass quantum collapse simulations.

The critical mass M_c is derived from:

    M_c = m_P × (a_0 / a_P)^(1/8)

where:
    m_P = Planck mass
    a_0 = Cosmological acceleration (c × H_0)
    a_P = Planck acceleration

The exponent 1/8 arises from 8D phase space geometry considerations.
"""

import numpy as np
from scipy.constants import G, hbar, c, k as k_B

# =============================================================================
# FUNDAMENTAL CONSTANTS (SI Units)
# =============================================================================

# Gravitational constant
G_SI = G  # m³ kg⁻¹ s⁻²

# Reduced Planck constant
HBAR = hbar  # J·s

# Speed of light
C = c  # m/s

# Boltzmann constant
K_B = k_B  # J/K

# =============================================================================
# PLANCK UNITS
# =============================================================================

# Planck length
L_PLANCK = np.sqrt(HBAR * G_SI / C**3)  # ≈ 1.616 × 10⁻³⁵ m

# Planck mass
M_PLANCK = np.sqrt(HBAR * C / G_SI)  # ≈ 2.176 × 10⁻⁸ kg

# Planck time
T_PLANCK = L_PLANCK / C  # ≈ 5.391 × 10⁻⁴⁴ s

# Planck energy
E_PLANCK = M_PLANCK * C**2  # ≈ 1.956 × 10⁹ J

# Planck temperature
TEMP_PLANCK = E_PLANCK / K_B  # ≈ 1.417 × 10³² K

# Planck acceleration
A_PLANCK = C / T_PLANCK  # ≈ 5.56 × 10⁵¹ m/s²

# Planck coherence time scale
TAU_PLANCK = T_PLANCK  # Reference scale for collapse times

# =============================================================================
# COSMOLOGICAL SCALES
# =============================================================================

# Hubble constant (current best estimate)
H_0_SI = 70 * 1000 / (3.086e22)  # 70 km/s/Mpc → ≈ 2.27 × 10⁻¹⁸ s⁻¹

# Cosmological acceleration (MOND scale / horizon acceleration)
A_0 = C * H_0_SI  # ≈ 6.8 × 10⁻¹⁰ m/s²

# Cosmic horizon scale
R_HUBBLE = C / H_0_SI  # ≈ 1.32 × 10²⁶ m

# =============================================================================
# OMEGA CONSTANT (From Unified Physics Framework)
# =============================================================================

# Universal scaling factor (phenomenological)
OMEGA = 117.038

# =============================================================================
# CRITICAL MASS M_c (THE CENTRAL PREDICTION)
# =============================================================================

# Acceleration ratio (fundamental hierarchy)
XI = A_0 / A_PLANCK  # ≈ 1.22 × 10⁻⁶¹

# Exponent from 8D phase space geometry
PHASE_SPACE_EXPONENT = 1/8

# CRITICAL MASS - The central testable prediction
M_C = M_PLANCK * (XI ** PHASE_SPACE_EXPONENT)  # ≈ 5.3 × 10⁻¹⁶ kg

# In atomic mass units (Daltons)
M_C_AMU = M_C / 1.66054e-27  # ≈ 3.2 × 10¹¹ Da

# In number of protons
M_C_PROTONS = M_C / 1.6726e-27  # ≈ 3.2 × 10¹¹ protons

# =============================================================================
# DERIVED SCALES FOR SIMULATIONS
# =============================================================================

# Characteristic coherence length at M_c
LAMBDA_C = HBAR / (M_C * C)  # ≈ 3.7 × 10⁻¹⁰ m (sub-nanometer)

# =============================================================================
# CALIBRATED TIME SCALE (From Gravitational/Penrose-like derivation)
# =============================================================================
# 
# τ_c = ℏ / E_grav where E_grav = G × M_c² / R_c
# R_c is the characteristic radius of a silica sphere at M_c
# This gives τ_c ≈ 2.18 seconds at M = M_c
#

# Silica density (for nanoparticle calculations)
RHO_SILICA = 2200  # kg/m³

# Characteristic radius at M_c
R_C_SILICA = (3 * M_C / (4 * np.pi * RHO_SILICA))**(1/3)  # ≈ 386 nm

# Gravitational self-energy at M_c
E_GRAV_MC = G_SI * M_C**2 / R_C_SILICA

# CALIBRATED COHERENCE TIME at M_c (Penrose-like derivation)
TAU_C_CALIBRATED = HBAR / E_GRAV_MC  # ≈ 2.18 seconds

# Power law exponent (from 8D phase space → quadratic most physical)
ALPHA_DEFAULT = 2.0

# Characteristic coherence time scale
TAU_PLANCK = T_PLANCK  # Reference scale for collapse times

# Thermal de Broglie wavelength at 300K for mass = M_c
LAMBDA_THERMAL_MC = np.sqrt(2 * np.pi * HBAR**2 / (M_C * K_B * 300))

# =============================================================================
# EXPERIMENTAL REFERENCE SCALES
# =============================================================================

# Silica density (for nanoparticle calculations)
RHO_SILICA = 2200  # kg/m³

# Silica nanoparticle radius for M = M_c
# M = (4/3) π r³ ρ → r = (3M / 4πρ)^(1/3)
R_SILICA_MC = (3 * M_C / (4 * np.pi * RHO_SILICA))**(1/3)  # ≈ 40-50 nm

# =============================================================================
# COMPARISON MODELS (CSL, GRW, Diósi-Penrose Parameters)
# =============================================================================

# CSL (Continuous Spontaneous Localization)
CSL_LAMBDA = 1e-16  # s⁻¹ (collapse rate per nucleon)
CSL_R_C = 1e-7  # m (correlation length)

# GRW (Ghirardi-Rimini-Weber)
GRW_LAMBDA = 1e-16  # s⁻¹ (collapse rate per particle)
GRW_A = 1e-7  # m (localization width)

# Diósi-Penrose time scale
def diosi_penrose_time(mass, delta_x):
    """
    Diósi-Penrose gravitational collapse time.
    
    τ_DP ≈ ℏ / E_grav
    E_grav ≈ G m² / Δx
    
    Parameters:
    -----------
    mass : float
        Mass of the object (kg)
    delta_x : float
        Superposition separation (m)
    
    Returns:
    --------
    tau_dp : float
        Collapse time (s)
    """
    E_grav = G_SI * mass**2 / delta_x
    return HBAR / E_grav


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_constants():
    """Print all key constants for reference."""
    print("=" * 60)
    print("PHYSICAL CONSTANTS FOR M_c RESEARCH")
    print("=" * 60)
    print(f"\n--- PLANCK UNITS ---")
    print(f"Planck mass (m_P)        = {M_PLANCK:.4e} kg")
    print(f"Planck length (l_P)      = {L_PLANCK:.4e} m")
    print(f"Planck time (t_P)        = {T_PLANCK:.4e} s")
    print(f"Planck acceleration (a_P)= {A_PLANCK:.4e} m/s²")
    
    print(f"\n--- COSMOLOGICAL SCALES ---")
    print(f"Hubble constant (H_0)    = {H_0_SI:.4e} s⁻¹")
    print(f"MOND acceleration (a_0)  = {A_0:.4e} m/s²")
    print(f"Hubble radius (R_H)      = {R_HUBBLE:.4e} m")
    
    print(f"\n--- HIERARCHY RATIO ---")
    print(f"Xi = a_0 / a_P           = {XI:.4e}")
    print(f"Xi^(1/8)                 = {XI**(1/8):.4e}")
    
    print(f"\n--- CRITICAL MASS (CENTRAL PREDICTION) ---")
    print(f"M_c = m_P × Xi^(1/8)     = {M_C:.4e} kg")
    print(f"M_c in Daltons           = {M_C_AMU:.4e} Da")
    print(f"M_c in proton masses     = {M_C_PROTONS:.4e}")
    
    print(f"\n--- CALIBRATED MODEL PARAMETERS ---")
    print(f"τ_c (coherence @ M_c)    = {TAU_C_CALIBRATED:.4e} s ({TAU_C_CALIBRATED:.2f} seconds)")
    print(f"α (power law exponent)   = {ALPHA_DEFAULT}")
    print(f"Grav. self-energy @ M_c  = {E_GRAV_MC:.4e} J")
    
    print(f"\n--- EXPERIMENTAL SCALES ---")
    print(f"Silica sphere radius @ M_c = {R_SILICA_MC*1e9:.1f} nm")
    print(f"Compton wavelength @ M_c   = {LAMBDA_C:.4e} m")
    
    print("=" * 60)


def mass_to_particles(mass, particle_mass=1.6726e-27):
    """Convert mass to number of particles (default: protons)."""
    return mass / particle_mass


def particles_to_mass(n_particles, particle_mass=1.6726e-27):
    """Convert number of particles to mass."""
    return n_particles * particle_mass


def silica_sphere_mass(radius_m):
    """Calculate mass of silica sphere from radius."""
    return (4/3) * np.pi * radius_m**3 * RHO_SILICA


def silica_sphere_radius(mass_kg):
    """Calculate radius of silica sphere from mass."""
    return (3 * mass_kg / (4 * np.pi * RHO_SILICA))**(1/3)


# =============================================================================
# MAIN (for testing)
# =============================================================================

if __name__ == "__main__":
    print_constants()
    
    # Test Diósi-Penrose for a typical mesoscopic system
    test_mass = 1e-15  # kg (slightly above M_c)
    test_delta_x = 1e-6  # 1 micron separation
    tau_dp = diosi_penrose_time(test_mass, test_delta_x)
    print(f"\nDiósi-Penrose time for M={test_mass:.1e} kg, Δx={test_delta_x:.1e} m:")
    print(f"τ_DP = {tau_dp:.4e} s")
