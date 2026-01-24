"""
AUDIT SCRIPT: ELECTRON MASS DERIVATION
======================================
Objective: Verify if the TARDIS formula yields the correct electron mass.

Formula identified in analysis:
m_e = M_universe * Omega^gamma_e

Parameters:
- Omega = 117.038 (Fundamental Parameter)
- M_universe = 1.5e53 kg (Mass of Observable Universe)
- gamma_e = -40.233777 (Scaling Exponent from Log 004)

Standard Value (CODATA 2018):
m_e = 9.10938356e-31 kg
"""

import numpy as np

# --- CONSTANTS ---
OMEGA = 117.038
M_UNIVERSE = 1.5e53 # kg (Estimation)
GAMMA_E = -40.233777

# CODATA 2018
M_ELECTRON_REAL = 9.10938356e-31

def calculate_mass():
    print(f"[-] TARDIS Parameter Omega: {OMEGA}")
    print(f"[-] Universe Mass: {M_UNIVERSE:.2e} kg")
    print(f"[-] Scaling Exponent: {GAMMA_E}")
    
    # Calculation
    # m_e = M_uni * Omega^(gamma)
    m_calc = M_UNIVERSE * (OMEGA ** GAMMA_E)
    
    print(f"\n[+] Calculated Mass: {m_calc:.8e} kg")
    print(f"[+] Real Mass (CODATA): {M_ELECTRON_REAL:.8e} kg")
    
    # Error
    error = abs(m_calc - M_ELECTRON_REAL) / M_ELECTRON_REAL * 100
    print(f"\n[!] Error: {error:.4f}%")
    
    if error < 1.0:
        print("\n[SUCCESS] The formula PREDICTS the electron mass within 1% error.")
    elif error < 10.0:
        print("\n[PARTIAL] The formula gets the order of magnitude correct.")
    else:
        print("\n[FAILURE] The formula is incorrect.")

if __name__ == "__main__":
    calculate_mass()
