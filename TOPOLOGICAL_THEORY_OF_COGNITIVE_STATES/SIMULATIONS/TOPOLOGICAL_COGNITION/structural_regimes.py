"""
Topological Theory of Cognitive States: Toy Model Simulation
Author: Douglas H. M. Fulber
DOI: 10.5281/zenodo.18364790

This script simulates the three primary topological regimes described in Paper A:
1. Critical Integration (Healthy) -> Small-World Network
2. Entropic Trapping (Anxiety) -> Over-Clustered / Ring Lattice
3. Modular Fragmentation (Dissociation) -> Disconnected Caveman Graph

It computes:
- Algebraic Connectivity (Lambda_2)
- Modularity (Q approximation via community structure)
- Spectral Density (Distribution of Eigenvalues)
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la

# Configuration
N_NODES = 100
SEED = 42

def analyze_spectrum(G, name):
    """Computes Laplacian eigenvalues and basic topological metrics."""
    # Laplacian Matrix
    L = nx.laplacian_matrix(G).toarray()
    eigenvalues = la.eigvalsh(L)
    
    # Sort eigenvalues
    eigenvalues = np.sort(eigenvalues)
    
    # Metrics
    lambda_2 = eigenvalues[1] if len(eigenvalues) > 1 else 0
    clustering = nx.average_clustering(G)
    try:
        path_length = nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        path_length = np.inf # Disconnected
        
    print(f"--- {name} ---")
    print(f"Algebraic Connectivity (Lambda_2): {lambda_2:.4f}")
    print(f"Avg Clustering Coeff (C): {clustering:.4f}")
    print(f"Avg Path Length (L): {path_length}")
    print("-" * 20)
    
    return eigenvalues

def plot_regimes(regimes):
    """Plots the spectral density and network structure for each regime."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Topological Regimes of Cognitive States", fontsize=16)
    
    names = ["Critical (Healthy)", "Trapped (Anxiety)", "Fragmented (Dissociation)"]
    
    for i, (name, G) in enumerate(regimes.items()):
        # Draw Graph
        ax_graph = axes[0, i]
        pos = nx.spring_layout(G, seed=SEED)
        nx.draw(G, pos, ax=ax_graph, node_size=30, node_color='teal', alpha=0.7, edge_color='gray')
        ax_graph.set_title(f"Topology: {name}")
        
        # Plot Spectrum
        eigenvalues = analyze_spectrum(G, name)
        ax_hist = axes[1, i]
        ax_hist.hist(eigenvalues, bins=20, color='purple', alpha=0.7, edgecolor='black')
        ax_hist.set_title(f"Spectral Signature ({name})")
        ax_hist.set_xlabel("Eigenvalue ($\lambda$)")
        ax_hist.set_ylabel("Density")
        ax_hist.grid(True, alpha=0.3)
        
        # Annotate Lambda 2
        lambda_2 = eigenvalues[1]
        ax_hist.axvline(lambda_2, color='red', linestyle='--', label=f'$\lambda_2={lambda_2:.2f}$')
        ax_hist.legend()

    plt.tight_layout()
    plt.savefig("regimes_comparison.png", dpi=300)
    print("Simulation complete. Results saved to 'regimes_comparison.png'.")

def main():
    print("Initializing Topological Simulation...\n")
    
    # 1. Healthy Regime: Watts-Strogatz Small World
    # High Clustering, Low Path Length. "Edge of Chaos".
    G_healthy = nx.watts_strogatz_graph(n=N_NODES, k=6, p=0.1, seed=SEED)
    
    # 2. Entropic Trap (Anxiety): Regular Lattice / Ring
    # Extremely High Clustering, Long Path Length. Energy trapped in local loops.
    # We use k=8 to simulate over-connection locally, but p=0 (no shortcuts)
    G_trap = nx.watts_strogatz_graph(n=N_NODES, k=8, p=0.0, seed=SEED)
    
    # 3. Fragmented Regime (Dissociation): Disconnected Caveman
    # High Modularity, Infinite Path Length.
    # 5 cliques of 20 nodes, 0 probability of rewiring (totally disconnected)
    G_fragmented = nx.connected_caveman_graph(l=5, k=20)
    # To make it truly fragmented (disconnected), we remove the linking edges created by connected_caveman
    # Actually, relaxed_caveman with p=0 is better or just removing edges between communities manually
    # Let's use a simple approach: Random partition graph with close to zero inter-group probability
    # Or just destroy G_fragmented bridges:
    # connected_caveman creates a cycle of cliques. Let's remove 2 edges to break the ring.
    edges = list(G_fragmented.edges())
    # This is a bit hacky, but effectively we want very low Lambda_2
    # Let's stick with the connected caveman but with very sparse inter-connections to show Low Lambda_2 (not necessarily 0 for math stability)
    # Actually, paper definition says Lambda_2 -> 0. Let's use p=0.01 rewiring on a caveman to allow slight integration but very poor.
    G_fragmented = nx.relaxed_caveman_graph(l=5, k=20, p=0.01, seed=SEED)

    regimes = {
        "Critical (Healthy)": G_healthy,
        "Trapped (Anxiety)": G_trap,
        "Fragmented (Dissociation)": G_fragmented
    }
    
    plot_regimes(regimes)

if __name__ == "__main__":
    main()
