import numpy as np
import networkx as nx
import scipy.linalg as la

def get_spectral_properties(G, label):
    try:
        L = nx.normalized_laplacian_matrix(G).toarray()
        eigenvalues = la.eigvalsh(L)
        eigenvalues = np.sort(eigenvalues)
        
        # Gap: Lambda_2
        gap = eigenvalues[1] if len(eigenvalues) > 1 else 0
        
        # Fielder Value (Algebraic Connectivity)
        algebraic_conn = eigenvalues[1]
        
        print(f"[{label}] Nodes: {len(G)} | Gap: {gap:.4f} | Alg. Conn: {algebraic_conn:.4f}")
        return gap, eigenvalues
    except:
        return 0, []

def run_cognitive_sim():
    print("\n--- SIMULATION 02: COGNITIVE TOPOLOGY ---")
    N = 200
    
    # 1. Healthy Mind (Small World)
    # Balanced integration and segregation.
    # Watts-Strogatz(n, k=10, p=0.1)
    G_healthy = nx.watts_strogatz_graph(N, k=10, p=0.1)
    gap_healthy, _ = get_spectral_properties(G_healthy, "HEALTHY")
    
    # 2. Mania (Random Network / Over-connected)
    # Loss of structure, signals propagate instantly everywhere.
    # Erdos-Renyi (p=0.2) -> High noise background.
    G_mania = nx.erdos_renyi_graph(N, p=0.2)
    gap_mania, _ = get_spectral_properties(G_mania, "MANIA")
    
    # 3. Depression (High Modularity / Disconnected)
    # Introduction of "dead zones". Ring Lattice.
    # Watts-Strogatz(n, k=4, p=0.0) -> Pure lattice, signals take forever.
    G_depression = nx.watts_strogatz_graph(N, k=4, p=0.0)
    gap_depression, _ = get_spectral_properties(G_depression, "DEPRESSION")
    
    # Check Leue Condition
    # Mania has Huge Gap (High Energy) but unstable (Chaos).
    # Depression has Tiny Gap (Order).
    # Healthy matches 1/f noise best.

if __name__ == "__main__":
    run_cognitive_sim()
