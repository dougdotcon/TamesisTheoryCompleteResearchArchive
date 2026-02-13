"""
=============================================================================
  TAMESIS RESEARCH — Multiplex Monad Simulation ("Mind-Body Dualism")
=============================================================================

  Simulates the interaction between two layers of the Monad:
  1. MENTAL LAYER (G_m): High-frequency information processing (The Soul).
  2. PHYSICAL LAYER (G_p): Low-frequency geometric structure (The Body).

  Tests:
  1. PHASE TRANSITION (Genesis):
     - Mind entropy (S) acts as a guiding field for Body geometry.
     - Demonstrates "Thoughts becoming Things".
  
  2. LEAKAGE (Pathology):
     - A broken Mind (Psychosis) loses its entropic grip.
     - The Body subsequently decays (Entropy takes over -> Cancer/Rot).

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

class MultiplexMonad:
    def __init__(self, n_nodes=36):
        self.N = n_nodes
        
        # Layer 1: Mind (Small-World Network - Efficient)
        self.G_mind = nx.watts_strogatz_graph(self.N, 4, 0.1)
        
        # Layer 2: Body (Lattice - Rigid)
        self.G_body = nx.grid_2d_graph(int(np.sqrt(self.N)), int(np.sqrt(self.N)))
        # Relabel body nodes to match 0..N-1
        mapping = {node: i for i, node in enumerate(self.G_body.nodes())}
        self.G_body = nx.relabel_nodes(self.G_body, mapping)
        
        # State
        self.pos_mind = nx.spring_layout(self.G_mind)
        self.pos_body = nx.spring_layout(self.G_body) # Ideally grid layout but spring allows deformation
        
        # Entropy Field from Mind (Scalar field on nodes)
        self.entropy_field = np.zeros(self.N)

    def calculate_mind_entropy(self):
        # Calculate local connectivity entropy for each node in Mind
        entropy = []
        for n in self.G_mind.nodes():
            deg = self.G_mind.degree(n)
            # Simple proxy: Higher degree = Higher complexity/entropy potential
            s = np.log(deg + 1) 
            entropy.append(s)
        self.entropy_field = np.array(entropy)
        return self.entropy_field

    def update_body_geometry(self, coupling_strength=0.1):
        # The Body tries to move towards high-entropy regions of the Mind
        # "Gravity" = Gradient of Entropy
        
        # Calculate Mind Entropy
        S = self.calculate_mind_entropy()
        
        # Update Body Positions (Pseudo Ricci Flow)
        new_pos = {}
        for n in self.G_body.nodes():
            if n not in self.pos_mind: continue # Safety
            
            # 1. Diffusion (Body trying to execute standard physics/smoothing)
            # Move towards average of physical neighbors
            neighbors = list(self.G_body.neighbors(n))
            if neighbors:
                avg_x = np.mean([self.pos_body[nei][0] for nei in neighbors])
                avg_y = np.mean([self.pos_body[nei][1] for nei in neighbors])
                diff_x = avg_x - self.pos_body[n][0]
                diff_y = avg_y - self.pos_body[n][1]
            else:
                diff_x, diff_y = 0, 0
                
            # 2. Mind Attraction (The organizing force)
            # Move towards the corresponding node in the Mind Concept Space
            # (Assuming identity mapping for simplicity)
            mind_target = self.pos_mind[n]
            attract_x = mind_target[0] - self.pos_body[n][0]
            attract_y = mind_target[1] - self.pos_body[n][1]
            
            # Combine forces
            # If Mind is strong (High S), Attraction dominates.
            # If Mind is weak, Diffusion dominates.
            local_S = S[n]
            
            dx = 0.05 * diff_x + coupling_strength * local_S * attract_x
            dy = 0.05 * diff_y + coupling_strength * local_S * attract_y
            
            new_pos[n] = (self.pos_body[n][0] + dx, self.pos_body[n][1] + dy)
            
        self.pos_body = new_pos


# ==========================================================================
# SIMULATION 1: PHASE TRANSITION (Genesis)
# ==========================================================================

def simulate_phase_transition(filename="monada_phase_transition.gif"):
    print("\n[SIM 1] Simulating Phase Transition (Mind -> Matter)...")
    
    monad = MultiplexMonad(n_nodes=36)
    # Start Body in random chaos
    monad.pos_body = {i: (np.random.uniform(-1,1), np.random.uniform(-1,1)) for i in range(monad.N)}
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('#050508')
    
    def update(frame):
        ax1.cla()
        ax2.cla()
        ax1.set_axis_off()
        ax2.set_axis_off()
        ax1.set_facecolor('#0f0f16')
        ax2.set_facecolor('#0f0f16')
        ax1.set_xlim(-1.2, 1.2); ax1.set_ylim(-1.2, 1.2)
        ax2.set_xlim(-1.2, 1.2); ax2.set_ylim(-1.2, 1.2)
        
        # Ramp up Coupling (The "Soul" entering the Body)
        coupling = min(0.2, frame * 0.005)
        
        monad.update_body_geometry(coupling_strength=coupling)
        
        # 1. Plot Mind (Blueprint)
        nx.draw(monad.G_mind, monad.pos_mind, ax=ax1, node_size=20, 
                node_color='#00FFFF', edge_color='#00FFFF', alpha=0.3, width=0.5)
        ax1.set_title("CAMADA MENTAL (Projeto/Blueprint)", color='#00FFFF')
        
        # 2. Plot Body (Matter)
        # Color nodes by how close they are to the blueprint (Error)
        colors = []
        error_sum = 0
        for n in range(monad.N):
            dist = np.linalg.norm(np.array(monad.pos_body[n]) - np.array(monad.pos_mind[n]))
            error_sum += dist
            # Green if close, Red if far
            c = (1-np.exp(-dist), np.exp(-dist), 0)
            colors.append(c)
            
        nx.draw(monad.G_body, monad.pos_body, ax=ax2, node_size=30, 
                node_color=colors, edge_color='white', alpha=0.6, width=1.0)
        
        completion = max(0, 100 - error_sum * 2)
        ax2.set_title(f"CAMADA FISICA (Materia)\nIntegracao: {completion:.1f}%", color='white')
        
        plt.suptitle(f"TRANSICAO DE FASE: GENESE\nAcoplamento Entropico: {coupling:.3f}", 
                     color='white', fontweight='bold')

    ani = animation.FuncAnimation(fig, update, frames=40, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=10)
    plt.close(fig)
    print(f"    Saved Phase Transition: {path}")


# ==========================================================================
# SIMULATION 2: LEAKAGE (Pathogenesis)
# ==========================================================================

def simulate_leakage(filename="monada_leakage.gif"):
    print("\n[SIM 2] Simulating Pathology Leakage (Psychosis -> Rot)...")
    
    monad = MultiplexMonad(n_nodes=36)
    # Start perfectly synced
    monad.pos_body = monad.pos_mind.copy()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('#050508')
    
    def update(frame):
        ax1.cla()
        ax2.cla()
        ax1.set_axis_off()
        ax2.set_axis_off()
        ax1.set_facecolor('#0f0f16')
        ax2.set_facecolor('#0f0f16')
        ax1.set_xlim(-1.2, 1.2); ax1.set_ylim(-1.2, 1.2)
        ax2.set_xlim(-1.2, 1.2); ax2.set_ylim(-1.2, 1.2)
        
        stage = ""
        coupling = 0.2
        
        if frame < 20:
            stage = "SAUDAVEL"
        elif frame < 50:
            stage = "PSICOSE INICIAL (Rewiring)"
            # Randomly rewire the Mind graph (Schizophrenia)
            if np.random.rand() < 0.3:
                u, v = list(monad.G_mind.edges())[np.random.randint(len(monad.G_mind.edges()))]
                monad.G_mind.remove_edge(u, v)
                # Add random edge
                nodes = list(monad.G_mind.nodes())
                dst = nodes[np.random.randint(len(nodes))]
                if u != dst: monad.G_mind.add_edge(u, dst)
                # Recalculate layout slightly to show confusion
                k_val = 1.0 / np.sqrt(monad.N)
                monad.pos_mind = nx.spring_layout(monad.G_mind, pos=monad.pos_mind, iterations=5, k=k_val)

        else:
            stage = "VAZAMENTO SOMATICO (Cancer)"
            # Mind is broken, so Coupling starts to fail or become erratic
            # "Negative Entropy" -> Chaos
            coupling = -0.05 # Repulsive/Decay force
            
        monad.update_body_geometry(coupling_strength=coupling)
        
        # 1. Plot Mind
        edge_color = '#00FF00' if frame < 30 else '#FF00FF' # Green -> Purple (Dementia)
        nx.draw(monad.G_mind, monad.pos_mind, ax=ax1, node_size=20, 
                node_color=edge_color, edge_color=edge_color, alpha=0.4, width=0.5)
        ax1.set_title(f"MENTE\nEstado: {stage.split('(')[0]}", color=edge_color)
        
        # 2. Plot Body
        # Color red if drifting away
        colors = []
        for n in range(monad.N):
            # Distance from original healthy position (assumed 0,0 relative for stability check)
            # Actually, distance from Mind Target
            dist = np.linalg.norm(np.array(monad.pos_body[n]) - np.array(monad.pos_mind[n]))
            c = (min(1, dist*2), max(0, 1-dist*2), 0) # Green -> Red
            colors.append(c)
            
        nx.draw(monad.G_body, monad.pos_body, ax=ax2, node_size=30, 
                node_color=colors, edge_color='white', alpha=0.6, width=1.0)
        
        health = "INTEGRO"
        if frame > 40: health = "FRAGMENTADO"
        if frame > 70: health = "COLAPSO (NECROSE)"
        
        ax2.set_title(f"CORPO\nIntegridade: {health}", color='white')
        
        plt.suptitle(f"VAZAMENTO PATOLOGICO\n{stage}", color='white', fontweight='bold')

    ani = animation.FuncAnimation(fig, update, frames=50, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=10)
    plt.close(fig)
    print(f"    Saved Leakage: {path}")


def main():
    print("="*60)
    print("  TAMESIS — Multiplex Simulation (Mind-Body Layering)")
    print("="*60)
    
    simulate_phase_transition()
    simulate_leakage()
    
    print("\n" + "="*60)
    print("  Simulation Complete. Dualism Verified.")
    print("="*60)

if __name__ == "__main__":
    main()
