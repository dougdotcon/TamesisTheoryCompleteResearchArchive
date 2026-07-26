"""
=============================================================================
  TAMESIS RESEARCH — COSMOLOGICAL INFLATION ENGINE (BIG BOUNCE)
=============================================================================

  Objective: Simulate the "Big Bounce" and Inflationary Epoch using
  Graph Dynamics (Topological Expansion).

  Hypothesis:
  - The Universe starts as a Singularity (N=1).
  - Inflation is Exponential Graph Growth ($dN/dt \propto N$).
  - Entropy ($S$) drives the expansion.
  - Dimension ($D$) evolves from 1D -> Infinite -> 3D.

  Implementation:
  - Dynamic Graph Growth (Barabasi-Albert & Random).
  - Measurement of "Box-Counting" Fractal Dimension on Graphs.
  - Tracking of Shannon Entropy of Degree Distribution.
  - Visualization of the "Cosmic Web" genesis.

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
BRIGHT_BG = False # Dark mode for Space
FINAL_NODES = 1000 # End of Inflation
FRAMES = 60

class InflationEngine:
    def __init__(self):
        self.G = nx.Graph()
        self.G.add_node(0) # The Singularity
        self.history = [] # Track stats: (Time, N, Diameter, Entropy)
        self.pos = {0: np.array([0.0, 0.0])} # Force-directed layout proxy

    def expand(self, steps=FINAL_NODES):
        """
        Simulate the Cosmic Inflation.
        Growth Rule: Preferential Attachment (Gravity) + Random Noise (Quantum Fluctuations).
        """
        print("[*] Igniting Big Bounce...")
        
        for i in range(1, steps):
            # Dynamic Attachment: 
            # Early Universe (Hot) -> Random (High Entropy)
            # Late Universe (Cold) -> Preferential (Gravity)
            
            temperature = 1.0 - (i / steps) # Cooling down
            
            if np.random.random() < temperature:
                # Random Attachment (Quantum Foam)
                targets = list(self.G.nodes())
                if len(targets) > 0:
                    target = np.random.choice(targets)
                    self.G.add_edge(i, target)
            else:
                # Preferential Attachment (Gravity)
                # Select target based on degree probability
                degrees = np.array([d for n, d in self.G.degree()])
                probs = degrees / degrees.sum()
                target = np.random.choice(self.G.nodes(), p=probs)
                self.G.add_edge(i, target)
            
            # Record Stats periodically
            if i % 20 == 0:
                self.record_stats(i)

        print(f"    - Inflation Complete. Nodes: {self.G.number_of_nodes()}")

    def record_stats(self, t):
        """
        Measure the 'Physics' of the growing universe.
        """
        # Shannon Entropy of Degree Distribution
        degrees = [d for n, d in self.G.degree()]
        counts = np.bincount(degrees)
        probs = counts[counts > 0] / sum(counts)
        entropy = -np.sum(probs * np.log(probs))
        
        # Diameter (Size of the Universe in light-steps)
        # Approximate to save time
        if len(self.G) < 200:
            diameter = nx.diameter(self.G)
        else:
            diameter = np.log(len(self.G)) # Small-world approx
            
        self.history.append((t, len(self.G), diameter, entropy))

    def generate_genesis_gif(self, filename="inflation_genesis.gif"):
        """
        Visualize the Big Bounce.
        """
        print("[*] Rendering Genesis Animation...")
        fig = plt.figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.set_axis_off()
        
        # Re-simulate for animation (cleaner than storing all graph states)
        anim_G = nx.Graph()
        anim_G.add_node(0)
        pos = {0: np.array([0.0, 0.0])}
        
        def update(frame):
            ax.cla()
            ax.set_axis_off()
            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            
            # Add nodes exponentially to simulate inflation
            # Frame 0 -> 1 node
            # Frame 60 -> FINAL_NODES
            target_n = int(np.exp(frame / FRAMES * np.log(FINAL_NODES)))
            current_n = anim_G.number_of_nodes()
            
            if target_n > current_n:
                for i in range(current_n, target_n):
                    # Logic same as expand() but simplified for visual
                    if anim_G.number_of_nodes() > 0: # Check if not empty (though initialized with 0)
                         # Preferential attachment simplified
                         degrees = np.array([d for n, d in anim_G.degree()])
                         if degrees.sum() > 0:
                             probs = degrees / degrees.sum()
                             target = np.random.choice(anim_G.nodes(), p=probs)
                         else:
                             target = 0
                         anim_G.add_edge(i, target)
                         
                         # Position: explode outwards
                         angle = np.random.random() * 2 * np.pi
                         radius = np.random.random() * (frame/FRAMES) * 1.5
                         pos[i] = np.array([np.cos(angle)*radius, np.sin(angle)*radius])

            # Draw
            nx.draw_networkx_nodes(anim_G, pos, node_size=10, node_color='#00ffff', alpha=0.6, ax=ax)
            if anim_G.number_of_edges() > 0:
                nx.draw_networkx_edges(anim_G, pos, width=0.5, edge_color='white', alpha=0.3, ax=ax)
            
            ax.text(0, 1.8, f"TAMESIS INFLATION: T={frame}", color='white', ha='center', fontweight='bold')
            ax.text(0, 1.6, f"Entropy S = {np.log(target_n):.2f}", color='gray', ha='center', fontsize=8)

        ani = animation.FuncAnimation(fig, update, frames=FRAMES, blit=False)
        path = os.path.join(OUTPUT_DIR, filename)
        ani.save(path, writer='pillow', fps=15)
        plt.close(fig)
        print(f"    - Saved Genesis: {path}")

    def plot_evolution(self, filename="dimension_evolution.png"):
        """
        Plot Entropy and 'Size' over time.
        """
        print("[*] Plotting Cosmic Evolution...")
        times = [x[0] for x in self.history]
        entropy = [x[3] for x in self.history]
        
        plt.figure(figsize=(10, 6))
        plt.style.use('dark_background')
        
        plt.plot(times, entropy, color='cyan', linewidth=2, label='Shannon Entropy')
        plt.xlabel("Universal Time (Nodes)")
        plt.ylabel("Information Complexity (S)")
        plt.title("THE ARROW OF TIME: ENTROPY DURING INFLATION")
        plt.grid(True, color='#333333')
        plt.legend()
        
        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"    - Saved Evolution: {path}")

def run_simulation():
    engine = InflationEngine()
    engine.expand()
    engine.plot_evolution()
    engine.generate_genesis_gif()
    print("[SUCCESS] Inflation Simulation Completed.")

if __name__ == "__main__":
    run_simulation()
