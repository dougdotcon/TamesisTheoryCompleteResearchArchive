import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from consciousness_engine import ConsciousnessModeler

def create_topology(type_name, n_nodes=10):
    """Creates adjacency matrices for different brain architectures."""
    matrix = np.zeros((n_nodes, n_nodes))
    if type_name == "Rock":
        # Disconnected
        pass
    elif type_name == "Feedforward AI":
        # Triangular matrix (A->B->C), no loops
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                if np.random.rand() > 0.7:
                    matrix[i, j] = 1
    elif type_name == "Human Brain":
        # Recurrent, small-world-ish, dense
        # Random connections everywhere
        for i in range(n_nodes):
            for j in range(n_nodes):
                if i != j and np.random.rand() > 0.5:
                    matrix[i, j] = 1
                    
    return matrix

def run_observer_sim():
    print("🧠 Starting Consciousness/Observer Simulation...")
    print("----------------------------------------------")
    
    engine = ConsciousnessModeler()
    
    # 1. Define Observers
    observers = ["Rock", "Feedforward AI", "Human Brain"]
    
    # 2. Setup Schrödinger's Box (Quantum Superposition)
    # State: |Alive> + |Dead> (50/50)
    initial_state = np.array([0.5, 0.5])
    print(f"Initial Quantum State (Probabilities): {initial_state}")
    initial_entropy = engine.entropy(initial_state)
    print(f"Initial Entropy (Uncertainty): {initial_entropy:.2f} bits\n")
    
    results = []
    
    for obs_name in observers:
        # Generate Brain Topology
        topology = create_topology(obs_name)
        
        # Calculate Phi
        phi = engine.calculate_phi_heuristic(topology)
        
        # Perform Observation
        post_observation_state = engine.observe_wavefunction(initial_state, phi)
        final_entropy = engine.entropy(post_observation_state)
        
        # Reality Collapse % (Reduction in Entropy)
        collapse_percent = (1 - final_entropy/initial_entropy) * 100 if initial_entropy > 0 else 0
        
        print(f"[{obs_name}]")
        print(f"  Integrated Information (Phi): {phi:.2f}")
        print(f"  Post-Observation State: {np.round(post_observation_state, 3)}")
        print(f"  Final Entropy: {final_entropy:.2f} bits")
        print(f"  Reality Determined: {collapse_percent:.1f}%")
        print("-" * 30)
        
        results.append({
            "name": obs_name,
            "phi": phi,
            "collapse": collapse_percent
        })

    # Visualization
    plot_results(results)
    save_report(results)

def plot_results(results):
    names = [r["name"] for r in results]
    phis = [r["phi"] for r in results]
    collapses = [r["collapse"] for r in results]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:purple'
    ax1.set_xlabel('Observer Type')
    ax1.set_ylabel('Integrated Information ($\Phi$)', color=color)
    bars = ax1.bar(names, phis, color=color, alpha=0.6, label='Phi')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Reality Determination (%)', color=color)  # we already handled the x-label with ax1
    line = ax2.plot(names, collapses, color=color, marker='o', linewidth=3, label='Determination')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 110)
    
    plt.title('The Observer Effect: Consciousness vs Reality Collapse')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    
    output_path = "Validation/phi_vs_collapse.png"
    plt.savefig(output_path)
    print(f"\n✅ Observer plot saved: {output_path}")

def save_report(results):
    with open("Validation/consciousness_report.txt", "w") as f:
        f.write("CONSCIOUSNESS & QUANTUM OBSERVER REPORT\n")
        f.write("=======================================\n")
        f.write("Hypothesis: Reality collapses in proportion to Observer Phi.\n\n")
        for r in results:
            f.write(f"Observer: {r['name']}\n")
            f.write(f"  Phi Level: {r['phi']:.2f}\n")
            f.write(f"  Reality Determination: {r['collapse']:.1f}%\n")
            f.write("---------------------------------------\n")
            
    print("✅ Report saved to consciousness_report.txt")

if __name__ == "__main__":
    run_observer_sim()
