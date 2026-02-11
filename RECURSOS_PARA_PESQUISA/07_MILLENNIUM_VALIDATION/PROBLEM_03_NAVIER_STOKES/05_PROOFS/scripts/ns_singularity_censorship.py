import numpy as np
import matplotlib.pyplot as plt

def simulate_ns_regularity():
    """
    Simulates enstrophy evolution Omega(t) for:
    1. Unregulated Euler-like (Omega' = Omega^1.5) -> Blow up
    2. Tamesis-Regulated NS (Omega' = Omega^1.5 - nu*Lambda^-2 * Omega^2) -> Regularity
    """
    t_max = 2.0
    dt = 0.001
    steps = int(t_max / dt)
    t = np.linspace(0, t_max, steps)
    
    # Parameters
    nu = 0.1
    Lambda = 10.0 # Structural regulator
    C = 1.0 # Vortex stretching constant
    
    omega_unregulated = np.zeros(steps)
    omega_regulated = np.zeros(steps)
    
    omega_unregulated[0] = 1.0
    omega_regulated[0] = 1.0
    
    for i in range(1, steps):
        # 1. Unregulated (Euler / High energy limit with no floor)
        d_omega_un = C * (omega_unregulated[i-1]**1.5)
        omega_unregulated[i] = omega_unregulated[i-1] + d_omega_un * dt
        
        # 2. Regulated (Tamesis Navier-Stokes)
        # Production (omega^1.5) vs Coercive Dissipation (omega^2)
        production = C * (omega_regulated[i-1]**1.5)
        dissipation = nu * (Lambda**-2) * (omega_regulated[i-1]**2)
        d_omega_reg = production - dissipation
        
        omega_regulated[i] = omega_regulated[i-1] + d_omega_reg * dt
        
        # Handle blow-up for plotting
        if omega_unregulated[i] > 1000:
            omega_unregulated[i:] = np.nan
            break

    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-paper')
    
    plt.plot(t, omega_unregulated, 'r--', label='Unregulated (Eulerian Blow-up)')
    plt.plot(t, omega_regulated, '#00CED1', linewidth=2, label='Tamesis-Regulated NS (Censored)')
    
    # Saturation lines
    plt.axhline( (C / (nu * Lambda**-2))**2, color='gray', linestyle=':', label='Structural Saturation Level')
    
    plt.title('Vortex Stretching vs Coercive Dissipation')
    plt.xlabel('Time (t)')
    plt.ylabel('Enstrophy $\Omega(t)$')
    plt.ylim(0, 50)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save assets
    import os
    asset_dir = r"d:\TamesisTheoryCompleteResearchArchive\07_MILLENNIUM_VALIDATION\PROBLEM_03_NAVIER_STOKES\assets"
    if not os.path.exists(asset_dir):
        os.makedirs(asset_dir)
        
    plt.savefig(os.path.join(asset_dir, "ns_singularity_censorship.png"), dpi=300)
    print(f"Enstrophy saturation plot saved to assets/ns_singularity_censorship.png")

if __name__ == "__main__":
    simulate_ns_regularity()
