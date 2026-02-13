"""
=============================================================================
  TAMESIS RESEARCH — EVENT HORIZON PARADOX (BLACK HOLE SIMULATION)
=============================================================================

  Objective: Test the behavior of a Monad Graph falling into a Black Hole.
  
  Hypothesis:
  - Tamesis predicts that information cannot be destroyed.
  - Scenario A: "Spaghettification" (Graph becomes a 1D line).
  - Scenario B: "Firewall" (Graph forms a dense shell to preserve entropy).
  
  Implementation:
  - Initialize a Healthy Monad (Small-World Graph).
  - Create a "Singularity Node" (S) with infinite attraction weight.
  - Dynamic Rewiring: Nodes are probabilistically reconnected to S based on "distance".
  - Visualization: Animation of the Graph Collapse.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import os

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
BRIGHT_BG = False # Space theme for Black Hole
N_NODES = 100 # Optimized for speed
FRAMES = 40

class BlackHoleParadox:
    def __init__(self, n_nodes=200):
        self.n = n_nodes
        # Initial State: Healthy Monad (Small-World)
        self.G = nx.watts_strogatz_graph(n_nodes, k=6, p=0.1)
        # Position initialization (Circular -> Spherical projection)
        self.pos = nx.spring_layout(self.G, seed=42)
        
    def simulate_fall(self, filename="monada_spaghettification.gif"):
        print("Starting Event Horizon Simulation...")
        
        fig = plt.figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.set_axis_off()
        
        # Singularity at (0,0)
        singularity_pos = np.array([0, 0])
        
        def update(frame):
            ax.cla()
            ax.set_axis_off()
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            
            # Decay factor (Time falling into BH)
            t = frame / FRAMES
            
            # Physics:
            # Nodes are pulled towards (0,0).
            # But... Tidal Forces stretch them along the radial line (Spaghettification).
            # AND... Connectivity increases as they get closer (Information Density).
            
            updated_pos = {}
            colors = []
            sizes = []
            
            for i, node in enumerate(self.G.nodes()):
                original_x, original_y = self.pos[node]
                
                # Relativistic Radial Pull
                # r(t) = r_0 * (1 - t)^2  (Accelerated fall)
                r_0 = np.sqrt(original_x**2 + original_y**2)
                if r_0 == 0: r_0 = 0.001
                
                current_r = r_0 * (1 - t**2 * 0.9) # Don't hit 0 exactly to avoid divergence
                
                # Spaghettification (Angular Compression)
                # Angle should align more with the radial vector
                original_theta = np.arctan2(original_y, original_x)
                
                # Add "Swirl" (Frame Dragging / Kerr Metric)
                swirl = 5 * t * (1/current_r) # Closer = Faster spin
                current_theta = original_theta + swirl
                
                x = current_r * np.cos(current_theta)
                y = current_r * np.sin(current_theta)
                
                updated_pos[node] = np.array([x, y])
                
                # Color shift: Blue (Safe) -> Red (Redshift) -> White (Singularity)
                if current_r < 0.2:
                    colors.append('white') # Firewall / Singularity
                    sizes.append(2)
                elif current_r < 0.5:
                    colors.append('#ff3333') # Event Horizon (Redshift)
                    sizes.append(10)
                else:
                    colors.append('#4ECDC4') # Accretion Disk / Safe Zone
                    sizes.append(20)

            # Update Graph Structure (Information Conservation vs Loss)
            # As t -> 1, nodes should connect more to neighbors (Compression)
            if frame % 10 == 0 and frame > 0:
                # Add random edges to simulate density increase
                u, v = np.random.choice(self.G.nodes(), 2)
                if not self.G.has_edge(u, v):
                    self.G.add_edge(u, v)

            # Draw "Event Horizon"
            horizon = plt.Circle((0, 0), 0.5, color='gray', fill=False, linestyle='--', alpha=0.5)
            ax.add_artist(horizon)
            
            # Draw Edges (Stretched)
            # Only draw a subset to avoid clutter
            nx.draw_networkx_edges(self.G, updated_pos, ax=ax, edge_color='white', alpha=0.1, width=0.5)
            
            # Draw Nodes
            ax.scatter([updated_pos[n][0] for n in self.G.nodes()], 
                       [updated_pos[n][1] for n in self.G.nodes()], 
                       c=colors, s=sizes, zorder=5)
            
            # Title
            status = "ACCRETION"
            if t > 0.3: status = "EVENT HORIZON"
            if t > 0.7: status = "SPAGHETTIFICATION"
            
            ax.text(0, 1.3, f"BLACK HOLE SIMULATION: {status}", 
                   color='white', ha='center', fontsize=12, fontweight='bold')

        ani = animation.FuncAnimation(fig, update, frames=FRAMES, blit=False)
        path = os.path.join(OUTPUT_DIR, filename)
        ani.save(path, writer='pillow', fps=15)
        plt.close(fig)
        print(f"    - Saved Paradox: {path}")

def run_test():
    bh = BlackHoleParadox(n_nodes=N_NODES)
    bh.simulate_fall()
    print("[SUCCESS] Event Horizon Paradox Test Completed.")

if __name__ == "__main__":
    run_test()
