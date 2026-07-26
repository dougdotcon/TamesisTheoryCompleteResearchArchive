import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def kuramoto_order_parameter(theta):
    """
    Calculates the Order Parameter (r) of synchronization.
    r = 1 (Full Sync), r = 0 (Chaos)
    """
    z = np.mean(np.exp(1j * theta))
    return np.abs(z)

def simulate_neural_coupling():
    """
    Hypothesis 2: Resonance & Phase Locking
    
    Data Source: 'A cognitive neural circuit biotype...'
    - Problem: dLPFC & dACC are disconnected (Weak Coupling).
    - Intervention: TMS provides a rhythmic driver.
    
    Physics Model: Kuramoto Model of Coupled Oscillators
    d(theta_i)/dt = omega_i + K/N * sum(sin(theta_j - theta_i)) + TMS_Driver
    """
    
    # Parameters
    N = 100 # Neurons in the circuit
    steps = 1000
    dt = 0.05
    
    # Natural frequencies (Intrinsic firing rates, gamma band approx)
    omega = np.random.normal(40, 5, N) 
    
    # Scenario 1: Depression (Weak Coupling)
    # The 'Connectivity' metric from the paper maps to the Coupling Constant K
    K_depressed = 0.5 # Below critical threshold for sync
    
    # Scenario 2: TMS Intervention (External Driver)
    # TMS forces entrainment at a specific frequency
    TMS_strength = 5.0
    TMS_freq = 10 # 10Hz stimulation (Alpha band often used in TMS)
    
    # Simulation Arrays
    theta_depressed = np.random.uniform(0, 2*np.pi, N)
    theta_treated = np.copy(theta_depressed)
    
    sync_depressed = []
    sync_treated = []
    
    t_span = np.arange(steps) * dt
    
    for t in t_span:
        # --- 1. Depressed Dynamics (Autonomous) ---
        # Mean field influence
        r_dep = np.mean(np.exp(1j * theta_depressed))
        psi_dep = np.angle(r_dep)
        
        # Kuramoto update
        dtheta_dep = omega + K_depressed * np.abs(r_dep) * np.sin(psi_dep - theta_depressed)
        # Add 'Entropic Noise' (Cognitive interference)
        dtheta_dep += np.random.normal(0, 1.0, N)
        
        theta_depressed += dtheta_dep * dt
        sync_depressed.append(kuramoto_order_parameter(theta_depressed))
        
        # --- 2. TMS Treated Dynamics (Driven) ---
        # Mean field
        r_trt = np.mean(np.exp(1j * theta_treated))
        psi_trt = np.angle(r_trt)
        
        # Driver (TMS Pulse) modeled as periodic forcing function
        tms_pulse = TMS_strength * np.sin(2 * np.pi * TMS_freq * t - theta_treated)
        
        dtheta_trt = omega + K_depressed * np.abs(r_trt) * np.sin(psi_trt - theta_treated) + tms_pulse
        # Reduced noise due to "focused attention" effect of treatment
        dtheta_trt += np.random.normal(0, 0.5, N)
        
        theta_treated += dtheta_trt * dt
        sync_treated.append(kuramoto_order_parameter(theta_treated))

    return t_span, sync_depressed, sync_treated

def plot_synchrony(time, sync_dep, sync_trt):
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    
    plt.plot(time, sync_trt, label='TMS Intervention (Driven Resonance)', color='blue', linewidth=2)
    plt.plot(time, sync_dep, label='Depressed State (Week Coupling)', color='red', alpha=0.6, linestyle='--')
    
    plt.axhline(0.8, color='green', linestyle=':', label='Critical Sync Threshold (Functional Circuit)')
    
    plt.title("Hypothesis 2: Neural Resonance & Phase Locking", fontsize=16)
    plt.xlabel("Time (ms)", fontsize=12)
    plt.ylabel("Order Parameter (Synchronization)", fontsize=12)
    plt.legend(loc='lower right')
    
    plt.annotate("Phase Transition\n(Response)", xy=(15, 0.85), xytext=(10, 0.95),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.tight_layout()
    plt.savefig('neural_resonance_synchrony.png', dpi=300)
    print("Simulation complete. Plot saved to 'neural_resonance_synchrony.png'")

if __name__ == "__main__":
    print("Simulating Neural Coupled Oscillators (Kuramoto Model)...")
    t, s_dep, s_trt = simulate_neural_coupling()
    plot_synchrony(t, s_dep, s_trt)
