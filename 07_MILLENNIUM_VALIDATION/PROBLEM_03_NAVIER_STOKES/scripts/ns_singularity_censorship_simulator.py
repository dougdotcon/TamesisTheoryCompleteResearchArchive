import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def simulate_enstrophy():
    """
    Simulates the evolution of enstrophy Omega(t) in 3D Navier-Stokes.
    Compares the 'Mathematical Blow-up' (standard) with 'Tamesis Censorship'.
    """
    # Parameters
    nu = 0.01  # Viscosity
    A = 0.5    # Vortex stretching coefficient
    a = 0.05   # Lattice spacing (structural regulator)
    Omega_max = 1.0 / (a**4) # Physical capacity limit (Pixelization)
    
    t = np.linspace(0, 5, 1000)
    Omega0 = 0.1
    
    # Standard Continuum Model (dOmega/dt = A * Omega^(3/2) - nu * Omega^k)
    # We use a simplified model often cited in blow-up studies.
    def dOmega_dt_standard(Omega, t):
        # Vortex stretching ~ Omega^(3/2)
        # Dissipation ~ Omega (simplification for L2 enstrophy)
        return A * (Omega**1.5) - nu * Omega
    
    # Tamesis Regulated Model
    # Imposes a saturation factor (1 - Omega/Omega_max)
    def dOmega_dt_tamesis(Omega, t):
        # As Omega approaches Omega_max, the growth rate is killed
        # by the structural impossibility of smaller pixels.
        stretching = A * (Omega**1.5)
        dissipation = nu * Omega
        regulator = np.maximum(0, 1 - (Omega / Omega_max))
        return stretching * regulator - dissipation

    # Integrate
    enstrophy_standard = odeint(dOmega_dt_standard, Omega0, t)
    enstrophy_tamesis = odeint(dOmega_dt_tamesis, Omega0, t)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-paper')
    
    plt.plot(t, enstrophy_standard, label='Continuum Model (Hypothetical Blow-up)', color='red', alpha=0.7, linestyle='--')
    plt.plot(t, enstrophy_tamesis, label='Tamesis Regulated (Pixelated Resolution)', color='#1f77b4', linewidth=2.5)
    
    plt.axhline(y=Omega_max, color='black', linestyle=':', label='Information Capacity Limit (a)')
    
    plt.yscale('log')
    plt.xlabel('Time (t)')
    plt.ylabel('Enstrophy $\Omega(t)$')
    plt.title('Navier-Stokes: Singularity Censorship via Bandwidth Regulation')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save assets
    import os
    asset_dir = r"d:\TamesisTheoryCompleteResearchArchive\07_MILLENNIUM_VALIDATION\PROBLEM_03_NAVIER_STOKES\assets"
    if not os.path.exists(asset_dir):
        os.makedirs(asset_dir)
        
    plt.savefig(os.path.join(asset_dir, "ns_singularity_censorship.png"), dpi=300)
    print(f"Simulation saved to assets/ns_singularity_censorship.png")
    
    # Generate Spectrum data (K-41 like)
    k = np.logspace(0, 5, 100)
    E_k = k**(-5/3) * np.exp(-(k*a)**2) # Spectral cut-off
    
    plt.figure(figsize=(10, 6))
    plt.loglog(k, k**(-5/3), 'r--', label='Kolmogorov (K-41)')
    plt.loglog(k, E_k, '#1f77b4', label='Tamesis Spectral Filter')
    plt.axvline(x=1/a, color='black', linestyle=':', label='Dissipation Pivot ($k_{max}$)')
    plt.xlabel('Wavenumber $k$')
    plt.ylabel('Energy $E(k)$')
    plt.title('Energy Spectrum with Structural Regularization')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(asset_dir, "ns_energy_spectrum.png"), dpi=300)
    print(f"Spectrum saved to assets/ns_energy_spectrum.png")

    # Inequality Attack (D vs P)
    Omega_vals = np.logspace(-1, np.log10(Omega_max*2), 100)
    Production = A * (Omega_vals**1.5)
    Dissipation = nu * (Omega_vals**2) / (a**2) # Heuristic for bandwidth limited enstrophy dissipation
    
    plt.figure(figsize=(10, 6))
    plt.loglog(Omega_vals, Production, 'r--', label='Production ($\sim \Omega^{3/2}$)')
    plt.loglog(Omega_vals, Dissipation, '#1f77b4', label='Dissipation ($\sim \Omega^{2}$)')
    plt.axvline(x=Omega_max, color='black', linestyle=':', label='Saturation Threshold')
    plt.xlabel('Enstrophy $\Omega$')
    plt.ylabel('Rate of Change')
    plt.title('The Inequality Attack: Dissipation vs Production')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(asset_dir, "ns_inequality_attack.png"), dpi=300)
    print(f"Inequality Attack saved to assets/ns_inequality_attack.png")

if __name__ == "__main__":
    simulate_enstrophy()
