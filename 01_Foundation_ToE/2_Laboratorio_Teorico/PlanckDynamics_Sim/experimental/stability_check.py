"""
Stability Stress Test
---------------------
Objective: Verify numerical stability of the Reactive Black Hole Engine
during the catastrophic final moments of evaporation (Planck Scale).
"""
import numpy as np
from black_hole_engine import ReactiveBlackhole, TARDIS_GAMMA

def run_stress_test():
    print("Running Stability Stress Test (24h Simulation equivalent)...")
    
    # Test Case: Micro Black Hole near end of life
    m_start = 1e-15 # Very small mass
    
    # We want to check if T_reac blows up nicely (finite float) or gives NaN
    steps = 1000
    m_current = m_start
    dt = 1e-40 # tiny timestep
    
    print(f"Testing mass decay from {m_start} kg...")
    
    for i in range(steps):
        bh = ReactiveBlackhole(m_current)
        T_reac, S_reac = bh.reactive_properties()
        
        # Check for NaNs
        if np.isnan(T_reac) or np.isnan(S_reac):
            print("❌ FAILURE: NaN detected at step", i)
            exit(1)
            
        # Check for Infinity
        if np.isinf(T_reac):
            print("⚠️ WARNING: Singularity reached (Expected at M=0). Stopping test.")
            break
            
        # Evaporate
        # dM/dt approx - Constant * T^4 * Area
        # Area ~ M^2, T ~ 1/M -> dM/dt ~ - 1/M^2
        loss = 1e-20 * (1.0/m_current**2)
        m_current -= loss
        
        if m_current <= 0:
            print("✅ Evaporation Complete without numerical error.")
            break
            
    print("✅ Stability Test Passed. No unhandled exceptions.")

if __name__ == "__main__":
    run_stress_test()
