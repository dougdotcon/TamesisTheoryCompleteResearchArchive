import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.linalg import expm
import time

class TamesisAdvValidator:
    def __init__(self, n_nodes=500):
        self.n_nodes = n_nodes
        # Initialize a Random Geometric Graph (RGG) - Standard for manifold emergence
        self.radius = np.sqrt(2.0 / n_nodes) * 1.5 
        self.pos = {i: np.random.rand(2) for i in range(n_nodes)}
        self.G = nx.random_geometric_graph(n_nodes, self.radius, pos=self.pos)
        
    def test_continuum_scaling(self):
        """
        Verify if the metric density g_mu_nu smooths out as N increases.
        Noise should scale as 1/sqrt(N).
        """
        print(f"--- Scaling Test: N={self.n_nodes} ---")
        # Use local degree distribution as a proxy for the Ricci Scalar / Local Curvature
        degrees = np.array([d for n, d in self.G.degree()])
        mean_deg = np.mean(degrees)
        std_deg = np.std(degrees)
        
        # Relative noise (fluctuations in the local 'fabric')
        rel_noise = std_deg / mean_deg
        print(f"Mean Connectivity: {mean_deg:.4f} | Std Dev: {std_deg:.4f}")
        print(f"Relative Metric Noise: {rel_noise:.4f}")
        return rel_noise

    def simulate_scattering_cross_section(self):
        """
        Simulate two topological defects (vortices) moving toward each other.
        Measure the informational 'deflection' as a proxy for cross-section.
        """
        print("\n--- Scattering Cross-Section Simulation ---")
        # Define two 'defect' zones
        center1 = np.array([0.3, 0.5])
        center2 = np.array([0.7, 0.5])
        
        node_positions = np.array(list(self.pos.values()))
        dist1 = np.linalg.norm(node_positions - center1, axis=1)
        dist2 = np.linalg.norm(node_positions - center2, axis=1)
        
        # Increase connectivity locally to simulate 'Defect' mass
        for i in range(self.n_nodes):
            if dist1[i] < 0.1 or dist2[i] < 0.1:
                # Add extra 'knot' edges
                neighbors = np.where(np.linalg.norm(node_positions - node_positions[i], axis=1) < self.radius*2)[0]
                for nb in neighbors:
                    if nb != i: self.G.add_edge(i, nb)

        # Measure 'Informational Resistance' between the two defects
        # High resistance = Low cross section (they don't see each other)
        # We use Resistance Distance (Effective Resistance in graphs)
        L = nx.laplacian_matrix(self.G).toarray()
        L_pinv = np.linalg.pinv(L)
        
        # Sample nodes from center 1 and center 2
        nodes1 = np.where(dist1 < 0.05)[0]
        nodes2 = np.where(dist2 < 0.05)[0]
        
        resistances = []
        for n1 in nodes1[:5]:
            for n2 in nodes2[:5]:
                r = L_pinv[n1,n1] + L_pinv[n2,n2] - 2*L_pinv[n1,n2]
                resistances.append(r)
        
        avg_res = np.mean(resistances)
        # Cross section is inversely proportional to resistance in info-networks
        sigma = 1.0 / avg_res 
        print(f"Average Info-Resistance: {avg_res:.4f}")
        print(f"Emergent Cross-Section (Sigma): {sigma:.4f} (Kernel Units)")
        return sigma

def run_scaling_series():
    ns = [100, 500, 1000, 2000]
    errors = []
    for n in ns:
        val = TamesisAdvValidator(n)
        err = val.test_continuum_scaling()
        errors.append(err)
    
    plt.figure(figsize=(8, 5))
    plt.plot(ns, errors, 'bo-', label='Observed Noise')
    # Theoretical 1/sqrt(N)
    theoretical = [errors[0] * np.sqrt(ns[0]/n) for n in ns]
    plt.plot(ns, theoretical, 'r--', label='1/sqrt(N) (POW)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Node Count (N)')
    plt.ylabel('Metric Gaussian Noise')
    plt.title('Tamesis Scaling: Convergence to Continuum Manifold')
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.savefig('d:/TamesisTheoryCompleteResearchArchive/14_VERIFICATION_TAMESIS_THEORY/scaling_robustness.png')
    print("\n[Output] Scaling Robustness plot saved.")

if __name__ == "__main__":
    run_scaling_series()
    final_val = TamesisAdvValidator(1000)
    final_val.simulate_scattering_cross_section()
