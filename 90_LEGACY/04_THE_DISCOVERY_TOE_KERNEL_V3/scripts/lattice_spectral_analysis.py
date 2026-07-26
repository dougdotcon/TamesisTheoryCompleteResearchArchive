"""
LATTICE SPECTRAL ANALYSIS
Subject: Statistical Properties of Graph Laplacian Spectra in Entropic Networks
Context: Discrete Gauge Theory / Kernel v3

This script performs a spectral analysis of the graph Laplacian L = D - A for
networks evolved under Entropic Maximization protocols.
It calculates the Algebraic Connectivity (Fiedler Value, λ2) and analyzes
the spectral density distribution.

Metrics:
- λ2 (Fiedler Value): Indicator of global connectivity / spectral gap.
- Spectral Gap Ratio: λ2 / λn
"""

import numpy as np
import networkx as nx
from universe_simulation import UniverseSimulation

class LatticeSpectralAnalyzer(UniverseSimulation):
    def get_spectral_properties(self):
        """
        Computes the eigenvalues of the normalized Laplacian.
        Returns:
            eigenvalues (sorted np.array)
            lambda_2 (float)
        """
        # mapping to NetworkX
        nodes = list(self.graph.nodes.keys())
        mapping = {node_id: i for i, node_id in enumerate(nodes)}
        
        A = np.zeros((len(nodes), len(nodes)))
        for node_id, node in self.graph.nodes.items():
            i = mapping[node_id]
            for neighbor_id in node.neighbors:
                j = mapping[neighbor_id]
                A[i, j] = 1
                A[j, i] = 1 # Undirected
        
        # Degree matrix
        degrees = np.sum(A, axis=1)
        D = np.diag(degrees)
        
        # Laplacian L = D - A
        L = D - A
        
        # Eigenvalues
        # eigh for symmetric matrices (guaranteed real eigenvalues)
        eigvals = np.linalg.eigvalsh(L)
        eigvals.sort()
        
        # Analytical properties
        # lambda_1 should be 0 (up to numerical precision)
        # lambda_2 is the Fiedler value
        
        return eigvals

    def run_analysis(self, steps=100, sampling_interval=10):
        print(f"--- Starting Spectral Analysis (N={len(self.graph.nodes)}, T={self.T}) ---")
        
        data_points = []
        
        for t in range(steps):
            self.run_step()
            
            if t % sampling_interval == 0:
                eigvals = self.get_spectral_properties()
                lambda_2 = eigvals[1] if len(eigvals) > 1 else 0.0
                max_lambda = eigvals[-1] if len(eigvals) > 0 else 0.0
                
                # Check for component count (number of zero eigenvalues)
                num_zeros = np.sum(np.abs(eigvals) < 1e-9)
                
                stats = {
                    'step': t,
                    'lambda_2': lambda_2,
                    'spectral_gap': lambda_2 / max_lambda if max_lambda > 0 else 0,
                    'connected_components': num_zeros
                }
                data_points.append(stats)
                print(f"Step {t:03d} | lambda_2: {lambda_2:.5f} | Components: {num_zeros}")
                
        return data_points

if __name__ == "__main__":
    # Parameters analogous to a "Planck scale" lattice simulation
    # N=100 nodes, Temperature=1.0 (Phase Transition proximity)
    analyzer = LatticeSpectralAnalyzer(num_nodes=100, temperature=1.0)
    
    # Run equilibrium dynamics
    results = analyzer.run_analysis(steps=200, sampling_interval=20)
    
    # Statistical Summary
    l2_values = [r['lambda_2'] for r in results[2:]] # Discard burn-in
    mean_gap = np.mean(l2_values)
    std_gap = np.std(l2_values)
    min_gap = np.min(l2_values)
    
    print("\n--- STATISTICAL RESULTS ---")
    print(f"Mean Spectral Gap (lambda_2): {mean_gap:.5f} +/- {std_gap:.5f}")
    print(f"Minimum Observed Gap:   {min_gap:.5f}")
    
    if min_gap > 1e-5:
        print("RESULT: Strict spectral gap maintained throughout evolution.")
    else:
        print("RESULT: Gap closure observed (Simulates massless phase).")
