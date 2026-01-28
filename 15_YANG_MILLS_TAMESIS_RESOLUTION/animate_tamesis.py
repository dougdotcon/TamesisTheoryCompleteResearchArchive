import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os
from PIL import Image

# Setup directories
FRAME_DIR = "d:/TamesisTheoryCompleteResearchArchive/15_YANG_MILLS_TAMESIS_RESOLUTION/frames"
os.makedirs(FRAME_DIR, exist_ok=True)

def generate_tamesis_loop(n_frames=60):
    # Fixed positions for consistency
    n_nodes = 30
    pos = {i: np.array([np.cos(2*np.pi*i/n_nodes), np.sin(2*np.pi*i/n_nodes)]) for i in range(n_nodes)}
    
    # Random perturbations to make it look "organic"
    np.random.seed(42)
    pos = {i: p + np.random.normal(0, 0.1, 2) for i, p in pos.items()}

    for f in range(n_frames):
        plt.figure(figsize=(6, 6), facecolor='black')
        ax = plt.gca()
        ax.set_facecolor('black')
        
        # Calculate Phase (0 to 1)
        # We use a sine wave for perfect loop: start -> complex -> start
        t = np.sin(np.pi * f / n_frames) 
        
        # 1. Graph Connectivity (Discrete -> Complex)
        G = nx.complete_graph(n_nodes)
        edges = list(G.edges())
        # Sort edges by distance to make growth look localized
        edges.sort(key=lambda x: np.linalg.norm(pos[x[0]] - pos[x[1]]))
        
        # Number of visible edges increases with t
        n_edges_visible = int(t * len(edges))
        visible_edges = edges[:max(n_edges_visible, n_nodes)]
        
        # 2. Draw Edges (Glowing transition)
        edge_alpha = 0.1 + 0.4 * t
        nx.draw_networkx_edges(G, pos, edgelist=visible_edges, 
                               edge_color='cyan', alpha=edge_alpha, width=0.5)
        
        # 3. Draw Nodes (Particles emerging)
        node_size = 20 + 100 * (t**2)
        node_color = plt.cm.plasma(t)
        nx.draw_networkx_nodes(G, pos, node_size=node_size, 
                               node_color=[node_color], alpha=0.8)
        
        # 4. Background Manifold Effect (Smoothing)
        if t > 0.5:
             # Add a smooth blur-like glow to simulate the continuum limit
             glow_t = (t - 0.5) * 2
             ax.scatter([p[0] for p in pos.values()], [p[1] for p in pos.values()], 
                        s=1000 * glow_t, color='blue', alpha=0.05 * glow_t)

        plt.xlim(-1.5, 1.5)
        plt.ylim(-1.5, 1.5)
        plt.axis('off')
        
        # Save frame
        plt.savefig(f"{FRAME_DIR}/frame_{f:03d}.png", dpi=100, facecolor='black')
        plt.close()
        if f % 10 == 0:
            print(f"Generated frame {f}/{n_frames}")

    print("Frames ready. Now run FFMPEG.")

if __name__ == "__main__":
    generate_tamesis_loop(60)
