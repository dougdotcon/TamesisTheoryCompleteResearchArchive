import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass

# --- PHYSCIAL CONSTANTS (METAPHORICAL) ---
# k_B in this context represents "Information Processing Capacity"
K_B = 1.0 

@dataclass
class BrainState:
    connectivity_z: float  # Functional connectivity (z-score)
    cognitive_control: float # Performance metric
    entropy: float

def verlinde_force(entropy_gradient, temperature):
    """
    F = T * nabla S
    The 'force' required to switch thoughts or control cognition.
    """
    return temperature * entropy_gradient

def simulate_treatment_cohort(n_patients=100, biotype_ratio=0.27):
    """
    Simulates a clinical trial population based on parameters from:
    'A cognitive neural circuit biotype of depression...' (Nature Mental Health)
    """
    
    # 1. Initialize Population
    n_biotype_pos = int(n_patients * biotype_ratio)
    n_biotype_neg = n_patients - n_biotype_pos
    
    # Biotype + (Depressed Circuit): Low Connectivity (z < 0), Low Variance (Rigid)
    # Using article data: z ~ -0.75 baseline 
    biotype_pos_con = np.random.normal(loc=-0.75, scale=0.3, size=n_biotype_pos)
    
    # Biotype - (Intact Circuit): Normal Connectivity (z >= 0)
    biotype_neg_con = np.random.normal(loc=0.5, scale=0.4, size=n_biotype_neg)
    
    cohort_connectivity = np.concatenate([biotype_pos_con, biotype_neg_con])
    biotype_labels = ['Biotype +'] * n_biotype_pos + ['Biotype -'] * n_biotype_neg
    
    return cohort_connectivity, biotype_labels

def entropic_dynamics_simulation():
    """
    Simulates the 'Entropic Gravity' of the depressed state.
    Hypothesis: Depression is a local entropy maximum (trap) that is globally sub-optimal.
    TMS acts as thermal injection to escape the local trap.
    """
    
    # Define the "Energy Landscape" (Potential Well)
    # x axis = Connectivity Z-score
    # y axis = Potential Energy (U)
    # We model Biotype (+) as being stuck in a deep well at z = -0.8
    
    z_range = np.linspace(-2.5, 2.5, 500)
    
    # Potential Function: Double well system
    # Well 1 (Depression): Deep, narrow at z = -0.8
    # Well 2 (Health): Broad, stable at z = +0.5
    u_depression = -1.5 * np.exp(-(z_range + 0.8)**2 / 0.2)
    u_health = -1.0 * np.exp(-(z_range - 0.5)**2 / 0.8)
    potential_u = u_depression + u_health
    
    # Entropic Force = - dU/dz (Tendency to fall into wells)
    # In Verlinde's view, this force is emergent from entropy gradients.
    force = -np.gradient(potential_u, z_range)
    
    # --- SIMULATE TMS INTERVENTION ---
    # TMS adds "Temperature" (Random Kinetic Energy) allowing escape from wells
    
    trajectories = []
    
    # Patient starting in Biotype + state
    start_pos = -0.8
    
    # Simulation Parameters
    timesteps = 100
    dt = 0.1
    
    # Scenarios: No Treatment vs TMS
    scenarios = {
        'No Treatment (T=0.1)': 0.1,
        'TMS Stimulation (T=0.8)': 0.8
    }
    
    results = {}
    
    for name, temp in scenarios.items():
        pos = start_pos
        path = [pos]
        for _ in range(timesteps):
            # 1. Deterministic Force (Gravity/Entropy Gradient)
            # Find nearest index in pre-calculated field
            idx = (np.abs(z_range - pos)).argmin()
            f_det = force[idx]
            
            # 2. Stochastic Thermal Force (TMS)
            f_stoch = np.random.normal(0, np.sqrt(temp))
            
            # Update Position (Overdamped Langevin)
            pos += (f_det + f_stoch) * dt
            
            # Boundary conditions
            pos = np.clip(pos, -2.5, 2.5)
            path.append(pos)
        results[name] = path

    return z_range, potential_u, results

def plot_results(z_range, potential_u, paths):
    sns.set_style("darkgrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: The Entropic Landscape
    ax1.plot(z_range, potential_u, color='black', linewidth=2)
    ax1.fill_between(z_range, potential_u, min(potential_u)-0.5, alpha=0.1, color='gray')
    ax1.set_title("The 'Mental Gravity' Landscape", fontsize=14)
    ax1.set_xlabel("Connectivity (Z-Score)", fontsize=12)
    ax1.set_ylabel("Entropic Potential (Stability)", fontsize=12)
    
    # Annotate Wells
    ax1.text(-1.2, -1.0, "Depression Trap\n(Biotype +)", color='red', fontweight='bold')
    ax1.text(0.6, -0.6, "Healthy State\n(Biotype -)", color='green', fontweight='bold')
    
    # Plot 2: Treatment Trajectories
    time = np.arange(len(paths['No Treatment (T=0.1)']))
    
    ax2.plot(time, paths['No Treatment (T=0.1)'], 
             label='No Treatment', color='red', alpha=0.7, linestyle='--')
    
    ax2.plot(time, paths['TMS Stimulation (T=0.8)'], 
             label='TMS Intervention', color='blue', linewidth=2)
            
    # Target Zone
    ax2.axhline(0, color='green', linestyle=':', label='Healthy Connectivity Threshold')
    
    ax2.set_title("TMS Intervention Simulation: Escaping the Well", fontsize=14)
    ax2.set_xlabel("Treatment Sessions (Time)", fontsize=12)
    ax2.set_ylabel("Connectivity State", fontsize=12)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('entropic_biotype_simulation.png', dpi=300)
    print("Simulation complete. Plot saved to 'entropic_biotype_simulation.png'")

if __name__ == "__main__":
    print("Initializing Unified Physics x Psychiatry Simulation...")
    z, u, trajectories = entropic_dynamics_simulation()
    plot_results(z, u, trajectories)
