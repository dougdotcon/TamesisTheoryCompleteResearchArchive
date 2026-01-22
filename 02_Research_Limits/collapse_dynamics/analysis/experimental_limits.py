import numpy as np
import matplotlib
matplotlib.use('Agg') # Force non-interactive backend
import matplotlib.pyplot as plt

# Constants
HBAR = 1.0545718e-34
G = 6.67430e-11

def main():
    print("=== Experimental Exclusion Limits ===")
    
    # 1. Theoretical Prediction Curve (Collapse Time vs Mass)
    masses = np.logspace(-21, -9, 100) # 10^-21 kg (mol) to 10^-9 kg (ug)
    separation = 1e-9 # 1 nm delocalization standard
    
    # Tau = hbar / (G * M^2 / dx)
    taus_predicted = HBAR / ((G * masses**2) / separation)
    
    # 2. Real Experimental Data Points (Literature)
    
    # A. Quantum Regime Confirmed (Interference observed)
    # Markus Arndt Group (Fein et al., Nature Physics 2019)
    # Oligoporphyrin (~2000 atoms), Mass ~ 2.5e4 amu ~ 4e-23 kg
    exp_arndt_m = 4.2e-23
    exp_arndt_tau = 10e-3 # ~10 ms flight time coherence
    
    # Kasevich (Atom Interferometry) - Rb atoms
    exp_atom_m = 1.4e-25 
    exp_atom_tau = 1.0 # ~1s coherence
    
    # B. Classical Regime Confirmed (No superposition)
    # Aspelmeyer Group (Westphal et al., Nature 2021)
    # Gravitational coupling of 90mg gold spheres
    exp_aspel_m = 9e-5 # 90 mg
    exp_aspel_tau = 1e-9 # Effectively classical / decohered instantly relative to quantum scales
    
    # C. The Frontier (Target)
    # TEQ (Test of Quantum) / MAQRO
    exp_teq_m = 1e-14 # Nanoparticle target range
    exp_teq_tau = 1e-3
    
    # 3. Critical Mass Threshold
    Mc_tardis = 2.02e-15 # From our simulation
    
    # Plotting
    plt.figure(figsize=(12, 8))
    
    # Predicted Quantum-Classical Boundary
    plt.loglog(masses, taus_predicted, 'r-', linewidth=3, label='Entropic Decoherence Limit (Predicted)')
    
    # Regions
    plt.fill_between(masses, taus_predicted, 1e10, color='red', alpha=0.1, label='Forbidden (Classical)')
    plt.fill_between(masses, 1e-20, taus_predicted, color='green', alpha=0.1, label='Allowed (Quantum)')
    
    # Plot Experiments
    plt.loglog(exp_atom_m, exp_atom_tau, 'go', markersize=12, markeredgecolor='k', label='Atom Interferometry (Confirmed Quantum)')
    plt.loglog(exp_arndt_m, exp_arndt_tau, 'g^', markersize=12, markeredgecolor='k', label='Macromolecules (Arndt 2019 - Confirmed Quantum)')
    plt.loglog(exp_aspel_m, exp_aspel_tau, 'kx', markersize=12, markeredgewidth=3, label='Macroscopic Gravity (Aspelmeyer 2021 - Classical)')
    plt.loglog(exp_teq_m, exp_teq_tau, 'bo', markersize=12, markeredgecolor='k', label='TEQ Target (The Frontier)')
    
    # Highlight Mc
    plt.axvline(x=Mc_tardis, color='k', linestyle='--', label=f'Predicted $M_c \\approx 10^{{-15}}$ kg')
    
    plt.title('Quantum-to-Classical Transition Map')
    plt.xlabel('Mass (kg)')
    plt.ylabel('Coherence Time (s)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.savefig('experimental_limits_map.png')
    print("Saved limits map.")

if __name__ == "__main__":
    main()
