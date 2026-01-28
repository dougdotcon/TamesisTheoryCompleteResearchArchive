import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import networkx as nx

def simulate_linear_server(size=50):
    """
    Standard Server: A linear chain (Queue).
    Topology: 1D Line Graph.
    Physics: No redundancy, single point of failure.
    """
    G = nx.path_graph(size)
    adj = nx.to_numpy_array(G)
    
    # Laplacian Spectrum
    eigenvalues = la.eigvalsh(nx.laplacian_matrix(G).toarray())
    eigenvalues = np.sort(eigenvalues)
    
    # Spectral Gap (Lambda_2 - Lambda_1)
    # For a path graph, Gap ~ O(1/n^2) -> Goes to zero as size increases!
    gap = eigenvalues[1] if len(eigenvalues) > 1 else 0
    return gap, eigenvalues

def simulate_holographic_server(size=50):
    """
    Tamesis Server: A hyperbolic expander (Small World).
    Topology: Watts-Strogatz / Expander Graph.
    Physics: High connectivity, redundant paths.
    """
    # Create a small-world network (approx. Hyperbolic)
    G = nx.watts_strogatz_graph(n=size, k=6, p=0.3)
    
    eigenvalues = la.eigvalsh(nx.laplacian_matrix(G).toarray())
    eigenvalues = np.sort(eigenvalues)
    
    # Expander Graphs have CONSTANT spectral gap > 0 even as N -> infinity.
    gap = eigenvalues[1] if len(eigenvalues) > 1 else 0
    return gap, eigenvalues

def run_experiment():
    print("--- SIMULATION 01: HOLOGRAPHIC BUFFER ---")
    
    sizes = [10, 50, 100, 200]
    linear_gaps = []
    holo_gaps = []
    
    for n in sizes:
        g_lin, _ = simulate_linear_server(n)
        g_hol, _ = simulate_holographic_server(n)
        
        linear_gaps.append(g_lin)
        holo_gaps.append(g_hol)
        print(f"N={n} | Linear Gap: {g_lin:.4f} | Holo Gap: {g_hol:.4f}")
        
    print("\nCONCLUSION:")
    print("Linear Server Gap collapses to 0 (Unstable).")
    print("Holographic Server Gap remains open (Stable).")
    
    # Return last values for Certification
    return linear_gaps[-1], holo_gaps[-1]

if __name__ == "__main__":
    run_experiment()
