"""
TAMESIS VALIDATION EXPERIMENT: ER = EPR (VISUALIZATION)
=======================================================
Hypothesis: Spacetime geometry (ER) is emergent from quantum entanglement (EPR).
Mechanism: Adding edges (entanglement) to a graph reduces the effective distance 
           and changes the curvature between nodes.

This script simulates a 1D ring universe, adds a transversal link (entanglement),
and generates a comparison plot 'er_epr_result.png'.
"""

import networkx as nx
import matplotlib.pyplot as plt
import time
import os

def log_step(step, message):
    print(f"[{time.strftime('%H:%M:%S')}] STEP {step}: {message}")

def run_er_epr_simulation():
    print("----------------------------------------------------------------")
    print("   TAMESIS KERNEL: ER=EPR VERIFICATION PROTOCOL                 ")
    print("----------------------------------------------------------------")
    
    # 1. Initialize 'Spacetime' (A Ring Graph representing a 1D closed universe)
    N_NODES = 50
    log_step(1, f"Initializing Spacetime Grid (N={N_NODES} nodes)...")
    G = nx.cycle_graph(N_NODES)
    
    node_A = 0
    node_B = N_NODES // 2  # Opposite side of the universe
    
    # Position nodes in a circle for visualization
    pos = nx.circular_layout(G)
    
    # 2. Setup Plot
    plt.figure(figsize=(12, 6))
    plt.suptitle("Tamesis Protocol: ER=EPR Visualization\nEntanglement Short-Circuits Spacetime Geometry", fontsize=16)

    # --- SUBPLOT 1: CLASSICAL (ER) ---
    plt.subplot(1, 2, 1)
    
    # Calculate path
    path_initial = nx.shortest_path(G, source=node_A, target=node_B)
    dist_initial = len(path_initial) - 1
    
    # Draw logic
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='gray', alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=[node_A, node_B], node_size=100, node_color='red')
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray')
    
    # Highlight classic path
    path_edges_initial = list(zip(path_initial, path_initial[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges_initial, edge_color='orange', width=2)
    
    plt.title(f"Classical State (Pre-Entanglement)\nGeodesic Distance: {dist_initial} hops")
    plt.axis('off')

    log_step(2, f"Classical Distance: {dist_initial} hops")

    # 3. Apply 'Entanglement' (Create an EPR pair / Add a direct edge)
    log_step(3, "Injecting Quantum Entanglement (EPR Pair)...")
    G.add_edge(node_A, node_B, type='quantum_link')
    
    # --- SUBPLOT 2: QUANTUM (ER=EPR) ---
    plt.subplot(1, 2, 2)
    
    # Calculate path
    path_final = nx.shortest_path(G, source=node_A, target=node_B)
    dist_final = len(path_final) - 1
    
    # Draw logic
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='gray', alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=[node_A, node_B], node_size=100, node_color='#00ff00') # Green for connected
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray')
    
    # Highlight new path (Wormhole)
    path_edges_final = list(zip(path_final, path_final[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges_final, edge_color='#00ff00', width=3, style='dashed')
    
    plt.title(f"Quantum State (Post-Entanglement)\nGeodesic Distance: {dist_final} hop (Wormhole Formed)")
    plt.axis('off')
    
    log_step(4, f"New Distance: {dist_final} hop")
    
    # 4. Save
    output_path = "er_epr_result.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    
    log_step(5, f"Graph generated: {os.path.abspath(output_path)}")
    print(f"\n[SUCCESS] Visualization saved to {output_path}")

if __name__ == "__main__":
    run_er_epr_simulation()
