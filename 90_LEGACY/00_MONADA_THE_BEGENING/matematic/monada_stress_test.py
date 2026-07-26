"""
=============================================================================
  TAMESIS RESEARCH — Monad Stress Test ("Pathology Report")
=============================================================================

  Simulates the failure modes of the Harmonic Monad to find topological limits.
  
  1. DISSOCIATION ("Psychosis"):
     - Increasing randomness (p) until Spectral Gap (lambda_1) collapses.
     - Hypothesis: The Monad loses cohesiveness and identity.

  2. SATURATION ("Black Hole"):
     - Increasing node density (N) until Curvature diverges.
     - Hypothesis: Information processing freezes (Event Horizon).

  3. DISSONANCE ("War"):
     - Interacting Monads with Orthogonal/Anti-Phase spectra.
     - Hypothesis: Destructive interference annihilates information.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-12

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import scipy.linalg
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================================
# TEST 1: PSYCHOSIS (Spectral Gap Collapse)
# ==========================================================================

def simulate_psychosis(filename="monada_psychosis.gif"):
    print("\n[TEST 1] Simulating Psychosis (Dissociation)...")
    
    # Parameters
    N = 100
    k = 4
    p_values = np.linspace(0, 1.0, 60) # Scanning rewind prob from 0 to 1
    
    gaps = []
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('#050508')
    
    def update(frame):
        ax1.cla()
        ax2.cla()
        ax1.set_axis_off()
        ax1.set_facecolor('#0f0f16')
        ax2.set_facecolor('#0f0f16')
        
        p = p_values[frame]
        
        # 1. Generate Graph
        G = nx.watts_strogatz_graph(N, k, p)
        
        # 2. Compute Spectrum
        L = nx.laplacian_matrix(G).toarray()
        eigenvalues = scipy.linalg.eigh(L, eigvals_only=True)
        gap = eigenvalues[1] if len(eigenvalues) > 1 else 0
        gaps.append(gap)
        
        # 3. Plot Graph (The "Brain")
        pos = nx.circular_layout(G)
        # Add some jitter based on p to show disorder
        pos = {n: (coords[0] + np.random.uniform(-0.1, 0.1)*p, 
                   coords[1] + np.random.uniform(-0.1, 0.1)*p) 
               for n, coords in pos.items()}
        
        edge_color = '#8B5CF6' if gap > 0.1 else '#EF4444' # Purple (Healthy) -> Red (Sick)
        nx.draw(G, pos, ax=ax1, node_size=20, node_color=edge_color, 
                edge_color=edge_color, alpha=0.6, width=0.5)
        ax1.set_title(f"Topologia Mental (p={p:.2f})", color='white')
        
        # 4. Plot Gap History (The "Vital Sign")
        ax2.plot(gaps, color='#00FFFF', linewidth=2)
        ax2.set_xlim(0, len(p_values))
        ax2.set_ylim(0, max(gaps)*1.1 if gaps else 1)
        ax2.set_title("Gap Espectral (Consciencia)", color='white')
        ax2.grid(True, alpha=0.1)
        
        status = "SAUDAVEL"
        if gap < 0.2: status = "RISCO"
        if gap < 0.05: status = "COLAPSO (PSICOSE)"
        
        plt.suptitle(f"STRESS TEST: DISSOCIACAO PLASTICA\nStatus: {status}", 
                     color='white', fontweight='bold')
        
    ani = animation.FuncAnimation(fig, update, frames=len(p_values), blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=10)
    plt.close(fig)
    print(f"    Saved Psychosis: {path}")


# ==========================================================================
# TEST 2: BLACK HOLE (Information Saturation)
# ==========================================================================

def simulate_blackhole(filename="monada_blackhole.gif"):
    print("\n[TEST 2] Simulating Black Hole (Saturation)...")
    
    # We increase connectivity (k) until the graph becomes a Complete Graph (or close)
    # The "Mass" increases.
    
    max_k = 20
    frames = 40
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('#000000') # Absolute black bg
    ax.set_facecolor('#000000')
    ax.set_axis_off()
    
    def update(frame):
        ax.cla()
        ax.set_axis_off()
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        
        # Determine k (connectivity)
        # Avoid k >= N errors
        N = 50
        k_curr = 2 + int((frame / frames) * max_k)
        if k_curr >= N: k_curr = N - 1
        
        # Generate dense graph
        # Using Barabasi-Albert for "Centralization" effect
        # m = number of edges to attach for new node. High m = High density.
        m = max(1, min(k_curr, N-1))
        G = nx.barabasi_albert_graph(N, m)
        
        # Calculate Centrality (Gravity)
        # centrality = nx.degree_centrality(G)
        
        # 3D Layout (Spherical)
        # Calculating layout every frame is slow but necessary for "collapse" visual
        pos = nx.spring_layout(G, dim=3, iterations=10) # Low iterations for jitter
        
        # Draw
        x_nodes = [pos[i][0] for i in G.nodes()]
        y_nodes = [pos[i][1] for i in G.nodes()]
        z_nodes = [pos[i][2] for i in G.nodes()]
        
        # Color: Transition from Gold -> White -> Black (Event Horizon)
        if k_curr < 8:
            color = '#FFD700' # Relativistic Gold
            alpha = 0.6
        elif k_curr < 15:
            color = '#FFFFFF' # Radiation Pressure
            alpha = 0.8
        else:
            color = '#111111' # Collapse
            alpha = 0.2 # Fading out
            
        ax.scatter(x_nodes, y_nodes, z_nodes, c=color, s=20 + k_curr*2)
        
        # Draw edges
        for edge in G.edges():
            x = [pos[edge[0]][0], pos[edge[1]][0]]
            y = [pos[edge[0]][1], pos[edge[1]][1]]
            z = [pos[edge[0]][2], pos[edge[1]][2]]
            ax.plot(x, y, z, color=color, alpha=0.3, linewidth=0.5)
            
        # Text
        status = "ESTAVEL"
        if k_curr > 8: status = "CRITICO (Inflacao)"
        if k_curr > 15: status = "COLAPSO (Singularidade)"
        
        ax.text2D(0.5, 0.95, f"STRESS TEST: SATURACAO DE INFORMACAO\nDensidade: {k_curr} links/no | Status: {status}", 
                 transform=ax.transAxes, ha='center', color='white', fontweight='bold')
        
    ani = animation.FuncAnimation(fig, update, frames=frames, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=10)
    plt.close(fig)
    print(f"    Saved Black Hole: {path}")


# ==========================================================================
# TEST 3: WAR (Destructive Interference)
# ==========================================================================

def simulate_war(filename="monada_war.gif"):
    print("\n[TEST 3] Simulating War (Destructive Interference)...")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#1a0505') # Dark red bg
    ax.set_facecolor('#1a0505')
    ax.set_ylim(-2, 2)
    ax.set_xlim(0, 10)
    ax.set_axis_off()
    
    x = np.linspace(0, 10, 500)
    
    def update(frame):
        ax.cla()
        ax.set_axis_off()
        ax.set_ylim(-2.5, 2.5)
        ax.set_xlim(0, 10)
        
        # Two waves approaching
        # Wave A (Purple) - Moving Right
        offset_a = 2 + frame * 0.1
        y_a = np.sin(2 * np.pi * (x - offset_a)) * np.exp(-0.5 * (x - offset_a)**2)
        
        # Wave B (Red/Anti-phase) - Moving Left
        # Shifted by PI to be in anti-phase
        offset_b = 8 - frame * 0.1
        y_b = np.sin(2 * np.pi * (x - offset_b) + np.pi) * np.exp(-0.5 * (x - offset_b)**2)
        
        # Total (Interference)
        y_total = y_a + y_b
        
        # Plot Individual Waves (Ghostly)
        ax.plot(x, y_a, color='#8B5CF6', alpha=0.3, linestyle='--', label='Monada A')
        ax.plot(x, y_b, color='#EF4444', alpha=0.3, linestyle='--', label='Monada B (Anti-Fase)')
        
        # Plot Result
        # Using disjoint segments to show "cancellation gaps"
        ax.plot(x, y_total, color='white', linewidth=2, label='Realidade Resultante')
        ax.fill_between(x, y_total, 0, color='white', alpha=0.1)
        
        # Detect Cancellation - correctly this time
        # We check the overlap region
        cancel = False
        if abs(offset_a - offset_b) < 1.0:
            # Significant overlap
            max_amp = np.max(np.abs(y_total))
            if max_amp < 0.1: # Threshold for "Silence"
                cancel = True
        
        status = "APROXIMACAO"
        overlap_val = np.exp(-0.5 * (offset_a - offset_b)**2)
        
        if overlap_val > 0.1:
            if cancel or (overlap_val > 0.8 and np.max(np.abs(y_total)) < 0.5):
                status = "ANIQUILACAO TOTAL (GUERRA)"
                ax.text(5, 0, "VACUO DE INFORMACAO", ha='center', color='red', fontsize=12, fontweight='bold')
            else:
                status = "INTERFERENCIA"
        
        ax.set_title(f"STRESS TEST: DISSONANCIA DE FASE\nStatus: {status}", color='white')
        
        # Fix legend
        leg = ax.legend(loc='upper right', facecolor='#1a0505', edgecolor='white')
        for text in leg.get_texts():
            text.set_color("white")

    ani = animation.FuncAnimation(fig, update, frames=60, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=15)
    plt.close(fig)
    print(f"    Saved War: {path}")


def main():
    print("="*60)
    print("  TAMESIS — Harmonic Monad Stress Test")
    print("="*60)
    
    simulate_psychosis()
    simulate_blackhole()
    simulate_war()
    
    print("\n" + "="*60)
    print("  Analysis Complete. Pathologies Documented.")
    print("="*60)

if __name__ == "__main__":
    main()
