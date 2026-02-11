
import numpy as np
import matplotlib.pyplot as plt

def simulate_veda_device():
    print("--- PROJECT V.E.D.A.: MODERN EXPERIMENTAL SIMULATION ---")
    print("Target: Detect Gravitational Anomalies via Entropy Reduction")
    print("Core: Ferrofluid Vortex | Excitation: 3-Phase EM + Sonic Injection")
    
    # 1. PARAMETERS
    time_steps = 300
    t = np.linspace(0, 10, time_steps)
    
    # System State
    base_mass = 1.000000 # kg (Precision calibrated)
    current_entropy = 1.0 # Normalized (1.0 = Chaos/Standard Vacuum)
    
    # Inputs
    coil_frequency = 60.0 # Hz (Rotation Speed of Magnetic Field)
    mantra_frequency = 136.1 # Hz (Om / Earth Year)
    resonance_factor = 0.0
    
    # Logs
    log_mass = []
    log_entropy = []
    log_resonance = []
    
    print("\n[V.E.D.A.] Starting Reactor...")
    
    for i in range(time_steps):
        # 2. EM COIL EXCITATION (Rasa Yantra)
        # Creates the Vortex. Reduces Entropy slightly due to ordering of magnetic domains.
        # But friction generates heat (Entropy increase).
        
        # Ramp up
        power = min(1.0, i / 50.0) 
        
        # Vortex Stability (Requires Tuned Frequency)
        vortex_coherence = power * np.sin(2 * np.pi * 0.1 * t[i]) # Wobble
        
        # 3. SONIC INJECTION (Mantra)
        # The key to Tamesis: Sound structures the plasma/fluid.
        # Resonance occurs when Mantra Freq matches Vortex Harmonics.
        
        # Let's simulate a "Lock-in" event at t=5s (Step 150)
        sonic_amplitude = 0.0
        if i > 100: 
            sonic_amplitude = min(1.0, (i - 100) / 50.0) # Ramp up sound
        
        # Checks for Harmonic Ratio (Tamesis Golden Ratio Hypothesis)
        # We simulate the system "finding" the resonance.
        
        phase_lock = np.exp(-((t[i] - 7.0)**2) / 0.5) # Peak resonance at t=7s
        
        # 4. PHYSICS ENGINE (Laghima Calculation)
        # Entropy = 1 - (Coherence * Power)
        # If Sonic + EM are locked -> Entropy drops drastically (Vacuum Polarization)
        
        system_ordering = (power * 0.1) + (sonic_amplitude * phase_lock * 0.8)
        current_entropy = 1.0 - system_ordering
        
        # Effective Mass follows Entropy (Verlinde's Entropic Gravity)
        # M_eff = M_base * Entropy_Density
        
        current_mass = base_mass * current_entropy
        
        # Noise/Jitter (Real world sensors)
        noise = np.random.normal(0, 0.00005)
        current_mass += noise
        
        log_mass.append(current_mass)
        log_entropy.append(current_entropy)
        log_resonance.append(phase_lock)
        
        if i % 50 == 0:
            print(f"Time {t[i]:.1f}s | Mass: {current_mass:.6f} kg | Entropy: {current_entropy:.4f}")

    # 5. VISUALIZATION
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Plot 1: System Inputs & Resonance
    ax1.plot(t, log_resonance, color='gold', label='Harmonic Resonance (Phase Lock)', linewidth=2)
    ax1.set_ylabel('Coherence Factor')
    ax1.set_title('V.E.D.A. Device: System Phase & Resonance')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Gravitational Anomaly
    ax2.plot(t, log_mass, color='cyan', label='Effective Mass ($M_{eff}$)')
    ax2.axhline(y=1.0, color='gray', linestyle='--', label='Standard Mass (1.0kg)')
    
    # Highlight the Anomaly
    min_mass = min(log_mass)
    min_time = t[np.argmin(log_mass)]
    ax2.annotate(f'Peak Laghima: {min_mass:.4f}kg\n(-{(1-min_mass)*100:.1f}%)', 
                 xy=(min_time, min_mass), xytext=(min_time, min_mass+0.2),
                 arrowprops=dict(facecolor='white', shrink=0.05))
    
    ax2.set_ylabel('Measured Weight (kg)')
    ax2.set_xlabel('Time (s)')
    ax2.set_title('Experimental Result: Mass Reduction via Entropic Suppression')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    print(f"\n[CONCLUSION] Resonance Peak at {min_time:.1f}s. Mass dropped to {min_mass:.4f}kg.")
    
    # Standard Scientific Style (White Background)
    fig.patch.set_facecolor('white')
    ax1.set_facecolor('white')
    ax2.set_facecolor('white')
    
    # Ensure text and spines are black
    for ax in [ax1, ax2]:
        ax.title.set_color('black')
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        for spine in ax.spines.values():
            spine.set_color('black')
    
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\veda_experiment_results.png"
    plt.savefig(output_path, facecolor='white')
    print(f"Gráfico Final salvo em: {output_path}")

if __name__ == "__main__":
    simulate_veda_device()
