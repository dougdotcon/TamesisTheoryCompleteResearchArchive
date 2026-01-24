"""
AUDIT SCRIPT: GALAXY ROTATION CURVE (DARK MATTER REPLACEMENT)
=============================================================
Objective: Verify if TAMESIS/Entropic Gravity explains galaxy rotation 
           curves without Dark Matter.

Test Case: NGC 6503 (Spiral Galaxy)
Data Source: Lelli et al. (2016) - SPARC Database

Approximate Parameters for NGC 6503:
- Baryonic Mass (Star+Gas): ~4.8e9 Solar Masses
- Test Radius: 20 kpc
- Observed Velocity: ~116 km/s

Newtonian Prediction vs TAMESIS Prediction
"""

import numpy as np
from reactive_gravity import ReactiveGravity

# --- CONSTANTS ---
M_SUN = 1.989e30      # kg
KPC = 3.086e19        # meters
G = 6.67430e-11       # SI

# --- NGC 6503 DATA ---
MASS_BARYONIC_SOLAR = 4.8e9
RADIUS_KPC = 20.0
V_OBSERVED_KMS = 116.0

def audit_rotation():
    print("="*60)
    print("AUDIT TARGET: NGC 6503 (Dark Matter Test)")
    print("="*60)
    
    # Inputs
    mass_kg = MASS_BARYONIC_SOLAR * M_SUN
    radius_m = RADIUS_KPC * KPC
    
    print(f"[-] Baryonic Mass: {MASS_BARYONIC_SOLAR:.2e} M_sun")
    print(f"[-] Test Radius: {RADIUS_KPC} kpc")
    print(f"[-] Observed Velocity: {V_OBSERVED_KMS} km/s")
    
    # 1. Newtonian Prediction (Classic Physics)
    # v = sqrt(GM/r)
    v_newton_ms = np.sqrt(G * mass_kg / radius_m)
    v_newton_kms = v_newton_ms / 1000.0
    
    print("-" * 40)
    print(f"[1] Newtonian Prediction (No Dark Matter):")
    print(f"    v = {v_newton_kms:.2f} km/s")
    error_newton = abs(v_newton_kms - V_OBSERVED_KMS) / V_OBSERVED_KMS * 100
    print(f"    Error: {error_newton:.2f}% (Too slow!)")
    
    # 2. TAMESIS Prediction (Entropic Gravity / MOND)
    # Using the Engine
    engine = ReactiveGravity(a0=1.2e-10)
    v_tardis_kms = engine.calculate_velocity(mass_kg, radius_m)
    
    print("-" * 40)
    print(f"[2] TAMESIS/Entropic Prediction:")
    print(f"    v = {v_tardis_kms:.2f} km/s")
    error_tardis = abs(v_tardis_kms - V_OBSERVED_KMS) / V_OBSERVED_KMS * 100
    print(f"    Error: {error_tardis:.2f}%")
    
    print("-" * 40)
    
    # Conclusion
    if error_tardis < 10.0 and error_newton > 30.0:
        print("\n[SUCCESS] TAMESIS explains the rotation curve without Dark Matter.")
        print(f"          Improvement factor: {error_newton/error_tardis:.1f}x better than Newton.")
    else:
        print("\n[FAILURE] TAMESIS failed to match observation significantly better.")

if __name__ == "__main__":
    audit_rotation()
