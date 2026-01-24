import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import logm

def simulate_page_curve():
    """
    Simulates the Entanglement Entropy of the Hawking Radiation emitted 
    by a Black Hole evolving under Unitary Dynamics.
    
    Goal: Reproduce the "Page Curve".
    1. Entropy rises initially (Hawking Radiation looks thermal).
    2. Entropy reaches a maximum at Page Time (~50% evaporation).
    3. Entropy falls back to zero (Information is recovered).
    
    If the process were NOT unitary (Information Loss), the curve would keep rising.
    """
    
    print("--- Simulating Black Hole Scrambling ---")
    
    # System Size (Number of Qubits)
    # Keeping it small for simulation speed (Exponential scaling!)
    N_qubits = 10 
    Dim = 2**N_qubits
    
    print(f"Total Qubits: {N_qubits}")
    print(f"Hilbert Space Dimension: {Dim}")
    
    # Initial State: Pure State |00...0> in the Black Hole
    # Density Matrix rho = |psi><psi|
    # For a pure state, we can analytically track the entropy of subsystems.
    # But simulating the full unitary dynamics is heavy.
    
    # Simplified Page Curve Model (Don Page, 1993):
    # S_rad ~ time (for t < t_page)
    # S_rad ~ N - time (for t > t_page)
    # Correct formula for random state:
    # S_A = log(d_A) - d_A / (2 d_B)  (if d_A < d_B)
    
    n_steps = N_qubits + 1
    entropy_radiation = []
    entropy_blackhole = []
    time_steps = np.arange(n_steps)
    
    print("Calculating Entropy at each step...")
    
    for k in time_steps:
        # k = Number of qubits radiated away
        n_rad = k
        n_bh = N_qubits - k
        
        dim_rad = 2**n_rad
        dim_bh = 2**n_bh
        
        # Calculate Entanglement Entropy of the Radiation S(R)
        # Using Page's Formula for a random pure state divided into part A and B.
        # S_ent = ln(min(dA, dB)) - min(dA, dB) / (2 * max(dA, dB))
        
        if dim_rad == 0 or dim_bh == 0:
            s = 0 # Empty system has 0 entropy
        else:
            min_dim = min(dim_rad, dim_bh)
            max_dim = max(dim_rad, dim_bh)
            
            # Entropy in bits (log2)
            # Theoretical Page Value
            s = np.log2(min_dim) - min_dim / (2 * max_dim)
            
        entropy_radiation.append(s)
        
        # In a unitary system, S(BH) must equal S(Rad) because the total state is pure.
        entropy_blackhole.append(s) 
        
    print("Simulation Complete.")
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Hawking Prediction (Information Loss)
    # Entropy just keeps growing as more thermal radiation is emitted
    hawking_curve = time_steps * 1.0 # 1 bit per qubit roughly
    
    # Plot Lines
    ax.plot(time_steps, hawking_curve, 'r--', label='Hawking Prediction (Info Loss)')
    ax.plot(time_steps, entropy_radiation, 'g-o', linewidth=2, label='Page Curve (Unitary TARDIS)')
    
    # Page Time Line
    page_time = N_qubits / 2
    ax.axvline(x=page_time, color='b', linestyle=':', label='Page Time (50% Evaporation)')
    
    ax.set_title(f"Black Hole Information Recovery: The Page Curve (N={N_qubits} Qubits)", fontsize=14)
    ax.set_xlabel("Qubits Radiated (Time)", fontsize=12)
    ax.set_ylabel("Entanglement Entropy (Bits)", fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Save
    plt.tight_layout()
    plt.savefig('../analysis/page_curve.png')
    print("Plot saved to limits/paradox/analysis/page_curve.png")

if __name__ == "__main__":
    simulate_page_curve()
