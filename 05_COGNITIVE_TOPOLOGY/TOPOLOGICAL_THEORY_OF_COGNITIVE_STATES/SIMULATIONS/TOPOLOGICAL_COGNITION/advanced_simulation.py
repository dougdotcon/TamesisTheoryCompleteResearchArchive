"""
Topological Theory of Cognitive States: Advanced Simulation
Author: Douglas H. M. Fulber
DOI: 10.5281/zenodo.18364790

This script expands the toy model to include complex dynamic states:
1. Mania (Hypersynchrony/Noise): Random Graph (Erdos-Renyi).
2. Psychedelic (Entropic Expansion): High Rewiring (p -> 1.0) but preserving degree distribution.
3. Dementia (Topological Decay): Random Edge Pruning on a Healthy Graph.

It computes Spectral Signatures for these states.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la

# Configuration
N_NODES = 100
SEED = 2026

def analyze_spectrum(G, name):
    """Computes Laplacian eigenvalues and basic topological metrics."""
    # Laplacian Matrix
    L = nx.laplacian_matrix(G).toarray()
    eigenvalues = la.eigvalsh(L)
    eigenvalues = np.sort(eigenvalues)
    
    # Metrics
    lambda_2 = eigenvalues[1] if len(eigenvalues) > 1 else 0
    clustering = nx.average_clustering(G)
    try:
        path_length = nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        path_length = np.inf 
        
    print(f"--- {name} ---")
    print(f"Lambda_2: {lambda_2:.4f}")
    print(f"Clustering (C): {clustering:.4f}")
    print(f"Path Length (L): {path_length}")
    print("-" * 20)
    
    return eigenvalues

def plot_advanced_regimes(regimes):
    """Plots the spectral density and network structure."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Advanced Topological Regimes (Phase 3.5)", fontsize=16)
    
    names = list(regimes.keys())
    
    for i, (name, G) in enumerate(regimes.items()):
        # Draw Graph
        ax_graph = axes[0, i]
        pos = nx.spring_layout(G, seed=SEED)
        nx.draw(G, pos, ax=ax_graph, node_size=30, node_color='orange', alpha=0.7, edge_color='gray')
        ax_graph.set_title(f"Topology: {name}")
        
        # Plot Spectrum
        eigenvalues = analyze_spectrum(G, name)
        ax_hist = axes[1, i]
        ax_hist.hist(eigenvalues, bins=20, color='darkred', alpha=0.7, edgecolor='black')
        ax_hist.set_title(f"Spectral Signature ({name})")
        
        lambda_2 = eigenvalues[1]
        ax_hist.axvline(lambda_2, color='blue', linestyle='--', label=f'$\lambda_2={lambda_2:.2f}$')
        ax_hist.legend()

    plt.tight_layout()
    plt.savefig("advanced_regimes.png", dpi=300)
    print("Advanced simulation complete. Results saved to 'advanced_regimes.png'.")

def main():
    print("Initializing Advanced Simulation...\n")
    
    # 1. Mania (Hypersynchrony / White Noise)
    # Modeled as Erdos-Renyi Random Graph
    # Everything is connected to everything randomly. No structure.
    G_mania = nx.erdos_renyi_graph(n=N_NODES, p=0.1, seed=SEED)
    
    # 2. Psychedelic State (Entropic Expansion)
    # Modeled as a Healthy Graph with INCREASED long-range connections (p=0.5)
    # "Flattening the landscape" - Reducing hierarchy.
    G_psychedelic = nx.watts_strogatz_graph(n=N_NODES, k=6, p=0.5, seed=SEED)
    
    # 3. Dementia (Topological Decay)
    # Start with Healthy, then prune 40% of edges randomly.
    G_healthy = nx.watts_strogatz_graph(n=N_NODES, k=6, p=0.1, seed=SEED)
    edges = list(G_healthy.edges())
    num_to_remove = int(len(edges) * 0.4)
    np.random.seed(SEED)
    edges_to_remove = np.random.choice(len(edges), num_to_remove, replace=False)
    
    G_dementia = G_healthy.copy()
    # Need to map indices back to edges
    edges_list = [edges[i] for i in edges_to_remove]
    G_dementia.remove_edges_from(edges_list)
    
    # Keep only giant component to avoid simple disconnection error for Lambda2 check
    # But dementia IS disconnection, so let's keep it and accept low Lambda2.

    regimes = {
        "Mania (Randomness)": G_mania,
        "Psychedelic (Integration)": G_psychedelic,
        "Dementia (Decay)": G_dementia
    }
    
    plot_advanced_regimes(regimes)

if __name__ == "__main__":
    main()
