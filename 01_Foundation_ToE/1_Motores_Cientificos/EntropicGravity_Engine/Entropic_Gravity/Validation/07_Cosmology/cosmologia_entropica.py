"""
Scientific Audit Module 07: Cosmological Expansion (The Boss Battle)
--------------------------------------------------------------------
Author: Antigravity (Elite Physicist System)

Objective:
Compare the Hubble Expansion History H(z) predicted by:
1. Standard Lambda-CDM (Dark Matter + Dark Energy)
2. Entropic Cosmology (Baryons Only + Entropic Terms)

Hypothesis:
If Entropic Gravity mirrors Dark Matter effects, H_entropic(z) must match H_LCDM(z)
using only Omega_b (0.049) instead of Omega_m (0.315).
"""

import numpy as np
import matplotlib.pyplot as plt

# --- CONSTANTS (Planck 2018) ---
H0 = 67.4       # km/s/Mpc
Omega_b = 0.049 # Baryons
Omega_m = 0.315 # Total Matter (CDM + Baryons)
Omega_L = 1.0 - Omega_m # Dark Energy

# Redshift array
z_range = np.linspace(0, 2.5, 100)

def hubble_LCDM(z):
    """Standard Model"""
    E2 = Omega_m * (1+z)**3 + Omega_L
    return H0 * np.sqrt(E2)

def hubble_entropic(z):
    """
    Entropic Model (Naive Baryon-Only)
    User hypothesis: H^2 ~ H0^2 [ Omega_b(1+z)^3 + (1-Omega_b) ]
    """
    E2_naive = Omega_b * (1+z)**3 + (1 - Omega_b)
    return H0 * np.sqrt(E2_naive)

def run_cosmology_test():
    print("🔬 RUNNING COSMOLOGY EXPANSION TEST...")
    
    H_lcdm = hubble_LCDM(z_range)
    H_ent = hubble_entropic(z_range)
    
    # Obs Data (Chronometers)
    obs_z = np.array([0.07, 0.12, 0.20, 0.28, 0.40, 0.47, 1.3, 1.53, 1.75])
    obs_H = np.array([69.0, 75.0, 72.9, 88.8, 95.0, 89.0, 168, 177, 202])
    obs_err = np.array([19.6, 2.0, 29.6, 11.2, 17.0, 50.0, 17.0, 14.0, 40.0])

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(z_range, H_lcdm, 'k--', label=r'$\Lambda$CDM (Standard - Has Dark Matter)')
    plt.plot(z_range, H_ent, 'r-', linewidth=2, label='Entropic Cosmology (Baryons Only)')
    plt.errorbar(obs_z, obs_H, yerr=obs_err, fmt='o', color='blue', label='Data', alpha=0.6)
    
    plt.xlabel('Redshift (z)')
    plt.ylabel('H(z) [km/s/Mpc]')
    plt.title('Expansion History: The Final Test')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("cosmology_analysis.png")
    print("✅ Cosmology Plot Saved: cosmology_analysis.png")
    
    # Calculate Discrepancy at z=1.5
    idx = np.argmin(np.abs(z_range - 1.5))
    diff = H_lcdm[idx] - H_ent[idx]
    
    with open("cosmology_report.md", "w", encoding='utf-8') as f:
        f.write("# Challenge 7: Cosmological Expansion (The Boss Battle)\n\n")
        f.write("## Hypothesis Test\n")
        f.write("We tested the Entropic universe using **only Baryons** ($\Omega_b = 0.049$) against the Standard Model ($\Omega_m = 0.315$).\n\n")
        f.write("## Results\n")
        f.write(f"- At z=1.5, H_LCDM = `{H_lcdm[idx]:.1f}`\n")
        f.write(f"- At z=1.5, H_Entropic = `{H_ent[idx]:.1f}`\n")
        f.write(f"- Discrepancy: `{diff:.1f}` km/s/Mpc\n\n")
        
        if diff > 20:
            f.write("## ❌ CRITICAL FAILURE\n")
            f.write("The Naive Entropic model **fails** to reproduce the expansion history. Without Dark Matter ($\Omega_m$), there is not enough mass scaling as $(1+z)^3$ to decelerate the universe in the past (or sustain high H(z)). The curve is too flat.\n\n")
            f.write("### Scientific Implications\n")
            f.write("1. **Baryons are not enough:** Even with Entropic gravity, you cannot simply replace $\Omega_m$ with $\Omega_b$ in the Friedmann equation.\n")
            f.write("2. **Missing Physics:** Verlinde's full theory (2016) suggests an *Apparent* Dark Matter density $\Omega_{D}^{app}$ that emerges from the Entropic Strain.\n")
            f.write("3. **Next Step:** We must implement the full Emergent Gravity equations where $\Omega_{apparent} \propto \sqrt{H}$ rather than just ignoring it.\n")
        else:
            f.write("## ✅ SUCCESS\n")
            f.write("The expansion history matches!\n")

if __name__ == "__main__":
    run_cosmology_test()
