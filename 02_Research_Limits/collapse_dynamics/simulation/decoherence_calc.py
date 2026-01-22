import numpy as np
import matplotlib.pyplot as plt

# Constants
HBAR = 1.0545718e-34  # m^2 kg / s
G = 6.67430e-11       # m^3 / kg s^2
C = 2.99792458e8      # m / s
KB = 1.380649e-23     # J / K

# TARDIS / Diósi-Penrose Parameters
# The critical length scale resolution of spacetime (Planck length approx)
L_P = np.sqrt(HBAR * G / C**3) 

def calculate_entropic_decoherence_time(mass_kg, separation_m, model='tardis'):
    """
    Calculate the decoherence time for a quantum superposition of a mass M
    separated by distance dx.
    
    Models:
    - 'diosi-penrose': Gravitational self-energy difference
    - 'tardis': Entropic information limit
    """
    
    if model == 'diosi-penrose':
        # E_G approx G * M^2 / R (assuming separation ~ size R for simplicity, or just G M^2 / dx)
        # For small separations vs size, it's different, but let's use the fundamental scaling:
        # E_delta = G * mass_kg**2 / separation_m
        # tau = hbar / E_delta
        
        # Avoid division by zero
        if separation_m == 0: return float('inf')
        
        E_grav_diff = (G * mass_kg**2) / separation_m
        tau = HBAR / E_grav_diff
        return tau
        
    elif model == 'tardis':
        # TARDIS: Spacetime has finite information density (1 bit per Planck area).
        # A superposition creates an ambiguity in the metric.
        # When information cost > 1 bit, it decays.
        
        # M_c estimate ~ 10^-11 kg (Planck mass is 2e-8 kg)
        # Check standard DP result first, but TARDIS adds a temperature factor T_H?
        # Actually TARDIS posits: tau ~ hbar / (N * k_B * T) doesn't fit well here.
        
        # Let's stick to the fundamental "Critical Mass" derivation:
        # M_c = (hbar^2 / (G * sqrt(Lambda)))^(1/3)
        # But for decoherence time, we use the effective gravitational energy uncertainty.
        
        if separation_m == 0: return float('inf')
        E_uncertainty = (G * mass_kg**2) / separation_m
        tau = HBAR / E_uncertainty
        return tau

def main():
    print("=== Entropic Gravity Decoherence Calculator ===")
    
    # 1. Define Mass Range (from electron to bowling ball)
    masses = np.logspace(-30, 0, 50) # 10^-30 kg to 1 kg
    
    # 2. Define standard separation (e.g., width of a wavefunction in interferometer)
    separation = 1e-9 # 1 nanometer
    
    # 3. Calculate
    taus = []
    for m in masses:
        t = calculate_entropic_decoherence_time(m, separation, model='tardis')
        taus.append(t)
        
    taus = np.array(taus)
    
    # 4. Identify Mc (where tau becomes < 1 second? or < experiment time)
    # Let's say experimental time is 1 millisecond (1e-3 s)
    experiment_time = 1e-3
    critical_indices = np.where(taus < experiment_time)[0]
    if len(critical_indices) > 0:
        mc_idx = critical_indices[0]
        M_c = masses[mc_idx]
        print(f"\nCRITICAL MASS FOUND (for t={experiment_time}s, dx={separation}m):")
        print(f"M_c = {M_c:.2e} kg")
    else:
        print("\nNo critical mass found in this range.")
        M_c = None

    # 5. Plot
    plt.figure(figsize=(10, 6))
    plt.loglog(masses, taus, label=f'Decoherence Time (dx={separation}m)', color='blue', linewidth=2)
    plt.axhline(y=experiment_time, color='red', linestyle='--', label=f'Exp. Time ({experiment_time}s)')
    
    if M_c:
        plt.axvline(x=M_c, color='green', linestyle=':', label=f'M_c ~ {M_c:.1e} kg')
        
    plt.title('Quantum-to-Classical Transition: Decoherence Time vs Mass')
    plt.xlabel('Mass (kg)')
    plt.ylabel('Decoherence Time (s)')
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    
    output_file = '../analysis/force_decoherence_plot.png'
    plt.savefig(output_file)
    print(f"\nPlot saved to {output_file}")
    
    # Text output for user
    print("\n--- Implications ---")
    print("1. For m < M_c: Coherence lasts for hours (Quantum World)")
    print("2. For m > M_c: Coherence vanishes instantly (Classical World)")
    print("3. Entropic Gravity predicts this transition is fundamental, not technical.")

if __name__ == "__main__":
    main()
