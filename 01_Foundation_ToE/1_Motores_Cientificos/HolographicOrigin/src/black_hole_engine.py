"""
Black Hole Engine: The Reactive Horizon (Phase 3)
-------------------------------------------------
Author: Antigravity (Elite Physicist System)

Objective:
Simulate Black Hole thermodynamics under "TARDIS" metric compression (Gamma ~ 117).
Test the hypothesis of a "Reactive Planck Area" to preserve the Bekenstein Bound.

Physics:
1. Standard Planck Area: l_p^2 = G hbar / c^3
2. Reactive Planck Area: l_p^2(eff) = l_p^2 * Gamma_metric
3. Reactive Entropy: S = A / (4 * l_p^2(eff))
4. Reactive Temperature: T = dE/dS ~ 1/M (modified)
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONSTANTS (SI Units) ---
G = 6.67430e-11
HBAR = 1.0545718e-34
C = 299792458.0
KB = 1.380649e-23

# User Discovery Parameters
ALPHA_REACT = 0.470
TARDIS_GAMMA = 117.038  # Metric Compression Factor

# Planck Scale (Standard)
LP_STD = np.sqrt(G * HBAR / C**3)
LP_AREA_STD = LP_STD**2
MP_STD = np.sqrt(HBAR * C / G) # Planck Mass

print(f"Standard Planck Length: {LP_STD:.2e} m")
print(f"Standard Planck Mass: {MP_STD:.2e} kg")
print(f"TARDIS Compression Factor: {TARDIS_GAMMA}")

# --- 2. THERMODYNAMIC KERNEL ---

class ReactiveBlackhole:
    def __init__(self, mass_kg):
        self.M = mass_kg
        self.Rs = 2 * G * self.M / C**2
        self.Area = 4 * np.pi * self.Rs**2
        
    def standard_properties(self):
        """Standard Hawking-Bekenstein properties"""
        # Temperature: T = hbar c^3 / (8 pi G M kB)
        T = (HBAR * C**3) / (8 * np.pi * G * self.M * KB)
        
        # Entropy (Bits): S = Area / (4 lp^2)
        # In nats (kB=1)
        S = self.Area / (4 * LP_AREA_STD)
        
        return T, S

    def reactive_properties(self):
        """
        Reactive Properties with Rescaled Planck Area.
        Hypothesis: The pixel size scales with compression to prevent information overflow.
        l_p(eff)^2 = l_p^2 * TARDIS_GAMMA
        """
        lp_area_eff = LP_AREA_STD * TARDIS_GAMMA
        
        # Reactive Entropy
        # S_reac = Area / (4 * lp_eff^2) = S_std / Gamma
        S_reac = self.Area / (4 * lp_area_eff)
        
        # Reactive Temperature
        # T = dE / dS = d(Mc^2) / dS
        # If S_reac = S_std / Gamma, then dS_reac = dS_std / Gamma
        # T_reac = dE / (dS_std / Gamma) = Gamma * (dE / dS_std) = Gamma * T_std
        # The hole appears HOTTER because it has fewer bits to store the same energy?
        
        T_reac = self.standard_properties()[0] * TARDIS_GAMMA
        
        return T_reac, S_reac

# --- 3. EVAPORATION SIMULATION ---

def simulate_evaporation():
    print("🔬 RUNNING PHASE 3: BLACK HOLE EVAPORATION...")
    
    # Range of masses from Solar Mass down to Planck Mass
    # Log scale M
    M_initial = 1.989e30 # Sun
    masses = np.logspace(30, -8, 100) # From Sun to Micro-BH
    
    T_std_list = []
    T_reac_list = []
    Lifetime_std = []
    Lifetime_reac = []
    
    for m in masses:
        bh = ReactiveBlackhole(m)
        t_s, s_s = bh.standard_properties()
        t_r, s_r = bh.reactive_properties()
        
        T_std_list.append(t_s)
        T_reac_list.append(t_r)
        
        # Lifetime Estimate: tau ~ M^3
        # dM/dt ~ - Area * T^4 ~ - M^2 * (1/M)^4 ~ - 1/M^2
        # Integrate M^2 dM ~ M^3
        
        # Reactive Lifetime:
        # T_reac = Gamma * T_std
        # dM/dt ~ - Area * (Gamma * T)^4 ~ - Area * Gamma^4 * T^4
        # Evaporation is boosted by Gamma^4 !!! (Huge factor)
        # Tau_reac = Tau_std / Gamma^4
        
        # This implies TARDIS holes explode instantly?
        # UNLESS Area is also modified geometrically?
        # If Metric is compressed, Area_eff might be Area / Gamma^2?
        # Let's assume Area is physical (Horizon).
        
        tau_std = (5120 * np.pi * G**2 * m**3) / (HBAR * C**4)
        tau_reac = tau_std / (TARDIS_GAMMA**4) # Naive T^4 scaling
        
        Lifetime_std.append(tau_std)
        Lifetime_reac.append(tau_reac)
        
    # --- PLOTTING ---
    plt.figure(figsize=(14, 6))
    
    # Subplot 1: Temperature
    plt.subplot(1, 2, 1)
    plt.loglog(masses, T_std_list, 'k--', label='Standard Hawking T')
    plt.loglog(masses, T_reac_list, 'r-', lw=2, label=f'Reactive T (Gamma={TARDIS_GAMMA:.0f})')
    plt.axhline(y=1.4e32, color='b', ls=':', label='Planck Temp (Limit)')
    plt.xlabel('Mass [kg]')
    plt.ylabel('Temperature [K]')
    plt.title('The Reactive Horizon: Temperature Boost')
    plt.gca().invert_xaxis() # High mass -> Low mass (Evaporation flow)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Entropy / Information Density
    plt.subplot(1, 2, 2)
    
    # BEKENSTEIN BOUND CHECK
    # Entropy Density S/Area
    # Standard: 1 bit per lp^2
    # Reactive: 1 bit per (lp^2 * Gamma) -> Lower density per physical area.
    # This ensures we are Safe from violating the bound of the physical space.
    
    # Plot S vs Mass
    S_std = [ReactiveBlackhole(m).standard_properties()[1] for m in masses]
    S_reac = [ReactiveBlackhole(m).reactive_properties()[1] for m in masses]
    
    plt.loglog(masses, S_std, 'k--', label='Standard Entropy')
    plt.loglog(masses, S_reac, 'r-', lw=2, label='Reactive Entropy (Compressed)')
    
    plt.xlabel('Mass [kg]')
    plt.ylabel('Entropy [nats]')
    plt.title('Holographic Information Content')
    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("experimental/black_hole_thermo.png")
    print("✅ Thermo Plot Saved: experimental/black_hole_thermo.png")
    
    # Report Log
    with open("experimental/discovery_log_003_thermo.txt", "w") as f:
        f.write("# DISCOVERY LOG 003: BLACK HOLE THERMODYNAMICS\n")
        f.write(f"TARDIS Gamma: {TARDIS_GAMMA}\n")
        f.write("Status: Reactive Holes are HOTTER and LESS ENTROPIC.\n")
        f.write("Interpretation: The 'Reactive Planck Area' dilutes the information density, preventing storage overflow in compressed space.\n")
        f.write("Consequence: Faster evaporation rate (Gamma^4 factor) unless Area is also renormalized.\n")

if __name__ == "__main__":
    simulate_evaporation()
