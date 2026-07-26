"""
=============================================================================
  TAMESIS RESEARCH — QUANTUM LIMIT STRESS-TEST (TENSOR NETWORKS)
=============================================================================

  Objective: Test if Quantum Entanglement (MPS/PEPS) survives "Gravitational
  Compression" (High Connectivity/Curvature).

  Hypothesis:
  - Tamesis predicts that Entanglement Entropy grows with Connectivity (Gravity).
  - Failure Mode: If Gravity "crushes" the state, Entropy should collapse (Area Law).
  - Success Mode: Entropy scales with Volume (Volume Law) -> "Holographic Monad".

  Implementation:
  - Mock Quantum State using Bond Dimension logic (Simulated MPS).
  - Network: 1D Chain (Quantum Spine) embedded in a Small-World Graph (Monad).
  - Stress Test: Increase "Gravity" (Rewiring Probability p).
  - Measure: Entanglement Entropy vs Gravity.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
BRIGHT_BG = True
N_QUBITS = 100
STEPS = 50

class QuantumMonad:
    def __init__(self, n_qubits=100):
        self.n = n_qubits
        self.G = nx.path_graph(n_qubits) # Start as a 1D Chain (MPS)
        self.gravity_levels = np.linspace(0, 1.0, STEPS)
        self.entropies = []

    def simulate_entanglement_survival(self):
        """
        Simulates the effect of "Gravitational Rewiring" on Entanglement.
        
        Logic:
        - In a pure MPS (1D chain), Entropy S ~ Const (Area Law).
        - In a Random Graph (Black Hole), Entropy S ~ N (Volume Law).
        - We want to see the transition.
        """
        print(f"[*] Starting Quantum Stress-Test (N={self.n})...")
        
        for p in self.gravity_levels:
            # Create Small-World Graph with probability p of rewiring
            # p=0: Regular Lattice (MPS) -> Low Gravity
            # p=1: Random Graph (Black Hole) -> Extreme Gravity
            G_temp = nx.watts_strogatz_graph(self.n, k=4, p=p)
            
            # Measure "Entanglement Proxy": Integration of the Graph
            # We use "Average Path Length" (L) and "Clustering" (C)
            # Entanglement ~ 1/L (Short paths = Stronger Entanglement)
            
            # However, to be more "Tensor Network" like, we calculate the 
            # Spectral Entropy of the Density Matrix (Laplacian).
            L_mat = nx.normalized_laplacian_matrix(G_temp)
            eigenvalues = np.linalg.eigvalsh(L_mat.todense())
            
            # Von Neumann Entropy = -Sum(lambda * log(lambda))
            # Normalized to probability distribution
            eigenvalues = eigenvalues[eigenvalues > 1e-10] # Remove zero
            prob = eigenvalues / np.sum(eigenvalues)
            entropy = -np.sum(prob * np.log(prob))
            
            self.entropies.append(entropy)

        print("    - Simulation Complete.")

    def plot_results(self, filename="monada_entanglement_survival.png"):
        """
        Plots Entropy vs Gravity.
        """
        print("[*] Plotting Quantum Limit...")
        plt.figure(figsize=(10, 6))
        if BRIGHT_BG:
            plt.style.use('default')
            grid_color = '#dddddd'
        else:
            plt.style.use('dark_background')
            grid_color = '#333333'

        plt.plot(self.gravity_levels, self.entropies, color='#8B5CF6', linewidth=3, label='Holographic Entropy')
        
        # Critical Point Annotation
        max_s = max(self.entropies)
        max_idx = np.argmax(self.entropies)
        max_g = self.gravity_levels[max_idx]
        
        plt.scatter([max_g], [max_s], color='red', s=100, zorder=5)
        plt.text(max_g, max_s + 0.1, f"Critical Gravity\n(K_crit = {max_g:.2f})", 
                 color='red', ha='center', fontweight='bold')

        plt.xlabel("Gravitational Compression (Rewiring p)")
        plt.ylabel("Entanglement Entropy ($S_{vN}$)")
        plt.title("QUANTUM LIMIT: ENTANGLEMENT SURVIVAL")
        plt.grid(True, color=grid_color)
        plt.legend()
        
        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"    - Saved: {path}")

def run_test():
    q_monad = QuantumMonad(n_qubits=N_QUBITS)
    q_monad.simulate_entanglement_survival()
    q_monad.plot_results()
    print("[SUCCESS] Quantum Stress-Test Completed.")

if __name__ == "__main__":
    run_test()
