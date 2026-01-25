import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def damped_harmonic_oscillator(viscosity_eta, initial_amplitude=1.0, duration=10, dt=0.01):
    """
    Simulates a neural signal (Cognitive Control) propagating through a hormonal medium.
    
    Physics Model: Dampened Harmonic Oscillator
    m*x'' + c*x' + k*x = 0
    
    Where 'c' (damping coefficient) is determined by 'Hormonal Viscosity'.
    - Low Viscosity (Optimal Hormones): Signal propagates clearly.
    - High Viscosity (Imbalance/Stress): Signal is overdamped (Mental Fatigue).
    """
    
    t = np.arange(0, duration, dt)
    x = np.zeros_like(t)
    
    # Initial Conditions
    x[0] = initial_amplitude
    v = 0 # Initial velocity
    
    # System Parameters
    m = 1.0  # Mass of the signal (constant)
    k = 10.0 # Neural Stiffness (Connection strength, assumed intact)
    
    # Damping ratio zeta = c / (2 * sqrt(m*k))
    # Fluid Viscosity 'eta' maps directly to Damping 'c'
    c = viscosity_eta 
    
    # Euler Integration
    for i in range(1, len(t)):
        # Acceleration a = (-k*x - c*v) / m
        a = (-k * x[i-1] - c * v) / m
        v += a * dt
        x[i] = x[i-1] + v * dt
        
    return t, x

def simulate_hormonal_impact():
    """
    Hypothesis 3: Hormonal Viscosity
    
    Data Source: 'Free testosterone and perceived stress in women...'
    - Finding: Testosterone levels correlate with stress response.
    - Metaphor: Hormones create the 'fluid environment' for neurons.
    """
    
    # Scenarios based on clinical profiles
    scenarios = {
        'Optimal Hormonal State (Low Viscosity)': 0.5,
        'Mild Imbalance (Medium Viscosity)': 2.0,
        'Severe Stress/Imbalance (High Viscosity)': 6.0
    }
    
    sns.set_style("darkgrid")
    plt.figure(figsize=(10, 6))
    
    for label, eta in scenarios.items():
        t, signal = damped_harmonic_oscillator(viscosity_eta=eta)
        plt.plot(t, signal, label=f"{label} ($\eta$={eta})", linewidth=2)
        
    plt.title("Hypothesis 3: Hormonal Viscosity & Signal Damping", fontsize=16)
    plt.xlabel("Time (Processing Speed)", fontsize=12)
    plt.ylabel("Cognitive Signal Amplitude", fontsize=12)
    plt.axhline(0, color='black', alpha=0.3)
    
    # Annotations
    plt.text(1.0, 0.8, "Clear Thought Process", color='blue')
    plt.text(2.0, 0.1, "Mental Fatigue / Brain Fog", color='red')
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('hormonal_viscosity_damping.png', dpi=300)
    print("Simulation complete. Plot saved to 'hormonal_viscosity_damping.png'")

if __name__ == "__main__":
    print("Simulating Hormonal Viscosity...")
    simulate_hormonal_impact()
