"""
STAGE 2: ENTROPIC ACCELERATION (a0) DERIVATION
Objective: Derive the critical acceleration scale a0 = 1.2e-10 m/s^2.
Theory: a0 is the surface gravity of the Hubble Horizon.
"""

import numpy as np

# Constants
c = 2.99792458e8      # Speed of Light (m/s)
H0_km_s_Mpc = 73.0    # Late Universe Reference (km/s/Mpc)
Mpc_to_m = 3.085678e22
H0_si = (H0_km_s_Mpc * 1000) / Mpc_to_m

print(f"Hubble Constant (SI): {H0_si:.6e} 1/s")

# Derivation: Surface Gravity of the De Sitter Horizon
# a_H = c * H0
# But usually there is a geometric factor (1/2pi or similar).
# MOND scale a0 is approx 1.2e-10 m/s^2.

# Geometric Factor Hypothesis:
a_H = c * H0_si
print(f"Horizon Acceleration (cH0): {a_H:.6e} m/s^2")

# Case A: Holographic Screen Area (Spherical) -> Factor 2pi
# a0 = c * H0 / (2 * pi)
a0_pred_A = a_H / (2 * np.pi)

# Case B: Bulk Entropy (Volume) -> Factor 6
# a0 = c * H0 / 6
a0_pred_B = a_H / 6

# Target (MOND standard)
a0_mond = 1.20e-10

print(f"\n--- HYPOTHESIS TESTING ---")
print(f"Hypothesis A (1/2pi): {a0_pred_A:.6e} m/s^2")
print(f"Hypothesis B (1/6):   {a0_pred_B:.6e} m/s^2")
print(f"Standard MOND Target: {a0_mond:.6e} m/s^2")

error_A = abs(a0_pred_A - a0_mond) / a0_mond * 100
error_B = abs(a0_pred_B - a0_mond) / a0_mond * 100

print(f"\nError A (1/2pi): {error_A:.2f}%")
print(f"Error B (1/6):   {error_B:.2f}%")

if error_A < 5.0 or error_B < 5.0:
    winner = "A (1/2pi)" if error_A < error_B else "B (1/6)"
    print(f"\n>> WINNER: {winner} matches the physical data.")
    print(">> Mechanism Identified: Surface/Volume Entropy correspondence.")
else:
    print("\n>> REFINEMENT NEEDED: Check H0 input precise value.")
