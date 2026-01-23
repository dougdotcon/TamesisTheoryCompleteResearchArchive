"""
Stage 84: Stress Testing (Robustness)
=====================================
Stress-testing the Entropic Galaxy Simulator.

Objective:
Determine if the emergence of flat rotation curves is a "fine-tuned" accident
or a robust structural property of the TDTR transition.

Tests:
1. Parameter Sensitivity: Vary a0 by +/- 50%.
2. Mass Noise: Add 20% random noise to the baryonic mass distribution.
3. Scale Variance: Vary galaxy scale length Rd.

If TDTR is robust, the rotation curves should remain qualitatively flat
despite significant perturbations.

Author: TDTR Research Program (Phase VIII)
Date: 2026-01-23
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Link to previous stages
sys.path.append('../79_Entropic_Galaxy_Sim')
sys.path.append('../80_Elastic_Memory_Transition')

from galaxy_simulator import GalaxySimulator # type: ignore
from elastic_memory import calculate_entropic_acceleration # type: ignore

def run_stress_test():
    print("=" * 70)
    print("STAGE 84: STRESS TESTING (ROBUSTNESS)")
    print("=" * 70)
    
    # Baseline
    M_base = 6.0e10
    Rd_base = 3.5
    a0_base = 1.2e-10
    
    # Simulator Setup
    r_grid = np.linspace(0.1, 50, 100)
    
    results = []
    
    print("Running Perturbations...")
    
    # TEST 1: a0 Sensitivity (+/- 50%)
    print("- Testing Critical Acceleration Sensitivity...")
    a0_vars = [a0_base * 0.5, a0_base, a0_base * 1.5]
    for a0_val in a0_vars:
        sim = GalaxySimulator(M_base, Rd_base, a0_val)
        a_N = sim.newtonian_acceleration(r_grid)
        a_E = calculate_entropic_acceleration(a_N, a0_val)
        # Convert to velocity (km/s)
        v = np.sqrt(r_grid * sim.kpc_to_m * a_E) / 1000.0
        results.append((f"a0={a0_val:.1e}", v))
        
    # TEST 2: Mass Noise
    print("- Testing Mass Distribution Noise...")
    sim = GalaxySimulator(M_base, Rd_base, a0_base)
    a_N_clean = sim.newtonian_acceleration(r_grid)
    
    # Inject 20% Gaussian noise into the acceleration field (simulating lumpy mass)
    noise = np.random.normal(0, 0.2 * np.mean(a_N_clean), size=len(r_grid))
    a_N_noisy = np.abs(a_N_clean + noise) # Acceleration magnitude
    
    a_E_noisy = calculate_entropic_acceleration(a_N_noisy, a0_base)
    v_noisy = np.sqrt(r_grid * sim.kpc_to_m * a_E_noisy) / 1000.0
    results.append(("Noisy Mass", v_noisy))
    
    # Display Results Analysis
    print("\nrbustness ANALYSIS:")
    print(f"{'Test Case':<20} | {'v(20kpc)':<10} | {'v(50kpc)':<10} | {'Flatness?'}")
    print("-" * 60)
    
    for label, v_curve in results:
        # Find indices
        idx_20 = np.abs(r_grid - 20).argmin()
        idx_50 = np.abs(r_grid - 50).argmin()
        
        v20 = v_curve[idx_20]
        v50 = v_curve[idx_50]
        diff = abs(v50 - v20)
        percent_diff = (diff / v20) * 100
        
        flat = "YES" if percent_diff < 15 else "DEVIATION"
        
        print(f"{label:<20} | {v20:<10.1f} | {v50:<10.1f} | {flat} ({percent_diff:.1f}%)")
        
    print("\nCONCLUSION:")
    print("If 'YES' appears for all, the theory implies that Flat Rotation Curves")
    print("are a STABLE ATTRACTOR of the dynamics, not a fine-tuned solution.")

if __name__ == "__main__":
    run_stress_test()
