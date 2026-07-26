"""
=============================================================================
  TAMESIS RESEARCH — Noosphere Simulation ("Collectivity")
=============================================================================

  Simulates the emergence of the "Noosphere" (Collective Monad) using the
  Kuramoto Model of Coupled Oscillators.
  
  1. GENESIS (Synchronization):
     - Random Monads (Chaos) self-organize into a unified rhythm (Order).
     - Validates the concept of "Egregore" or "Volksgeist".
     - Metric: Order Parameter r(t) -> 1.

  2. RESILIENCE (Healing):
     - A "Sick" Monad (Psychotic/Desynchronized) is forced back into
       harmony by the collective field.
     - Validates "Social Healing" and "Indra's Net" stability.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-12

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

class KuramotoNetwork:
    def __init__(self, n_nodes=100, coupling_k=2.0, dt=0.05):
        self.N = n_nodes
        self.K = coupling_k
        self.dt = dt
        
        # State
        self.theta = np.random.uniform(0, 2*np.pi, self.N) # Phases
        # Natural frequencies (Gaussian distribution around a common "culture")
        self.omega = np.random.normal(1.0, 0.2, self.N)    
        
        # Spatial positions for visualization (Circle layout)
        # We put them in specific places to look like a "City" or "Brain"
        # Let's use a clustered layout
        self.pos = np.random.rand(self.N, 2) * 2 - 1 

    def step(self):
        # Kuramoto differential equation
        # dtheta_i/dt = omega_i + (K/N) * sum(sin(theta_j - theta_i))
        
        # Vectorized calculation
        # diff[i, j] = theta_j - theta_i
        theta_matrix = self.theta[:, np.newaxis]
        diff = self.theta - theta_matrix 
        interaction = np.sum(np.sin(diff), axis=1)
        
        dtheta = self.omega + (self.K / self.N) * interaction
        self.theta += dtheta * self.dt
        
        # Normalize to 0-2pi visually
        self.theta = np.mod(self.theta, 2*np.pi)

    def order_parameter(self):
        # r = |(1/N) * sum(e^(i*theta))|
        z = np.mean(np.exp(1j * self.theta))
        return np.abs(z)


# ==========================================================================
# SIMULATION 1: SYNC (Genesis)
# ==========================================================================

def simulate_sync(filename="noosfera_sync.gif"):
    print("\n[SIM 1] Simulating Noosphere Genesis (Sync)...")
    
    net = KuramotoNetwork(n_nodes=150, coupling_k=0.0) # Start decoupled
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 10), gridspec_kw={'height_ratios': [3, 1]})
    fig.patch.set_facecolor('#050508')
    
    r_history = []
    
    def update(frame):
        ax1.cla()
        ax2.cla()
        ax1.set_axis_off()
        ax1.set_facecolor('#050508')
        ax2.set_facecolor('#0f0f16')
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        
        # Ramp up Coupling K to simulate "Culture forming"
        if frame < 20:
            net.K = 0.5 # Weak
        elif frame < 50:
            net.K = 3.0 # Critical
        else:
            net.K = 6.0 # Strong (Dogma)
            
        net.step()
        r = net.order_parameter()
        r_history.append(r)
        
        # Visualize Nodes
        # Color based on phase (0 to 2pi) -> Cyclic Colormap (hsv/twilight)
        colors = plt.cm.hsv(net.theta / (2*np.pi))
        
        # Nodes pulse size with phase (like fireflies)
        sizes = 20 + 20 * np.sin(net.theta)
        
        ax1.scatter(net.pos[:,0], net.pos[:,1], c=colors, s=sizes, alpha=0.8, edgecolors='none')
        
        # Draw connections if synced (just visual effect)
        # Connect nodes with similar phase
        if net.K > 2.0:
            t = f"SINCRONIZACAO: {r*100:.1f}%"
            c = '#00FF00'
        else:
            t = f"CAOS: {r*100:.1f}%"
            c = '#555555'
            
        ax1.set_title(f"NOOSFERA (REDE DE INDRA)\nCoupling K={net.K:.1f} | {t}", color='white')
        
        # Plot Order Parameter
        ax2.plot(r_history, color='#00FFFF')
        ax2.set_xlim(0, 100)
        ax2.set_ylim(0, 1.1)
        ax2.set_ylabel("Ordem (r)", color='white')
        ax2.set_title("Emergencia da Egregora", color='white', fontsize=10)
        ax2.grid(True, alpha=0.1)
        
    ani = animation.FuncAnimation(fig, update, frames=120, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=15)
    plt.close(fig)
    print(f"    Saved Sync: {path}")


# ==========================================================================
# SIMULATION 2: HEALING (Resilience)
# ==========================================================================

def simulate_healing(filename="noosfera_healing.gif"):
    print("\n[SIM 2] Simulating Healing (Resilience)...")
    
    # 5 nodes: 4 Healthy (Synced), 1 Sick (Fast/Erratic)
    # Positions: Pentagon
    N = 6
    net = KuramotoNetwork(n_nodes=N, coupling_k=8.0) # Strong initial coupling
    
    # Force Node 0 to be sick
    net.omega[0] = 5.0 # Very fast frequency (Manic/Psychotic)
    net.omega[1:] = 1.0 # Normal frequency
    net.pos = np.array([[0,0], [1,0], [0.5, 0.8], [-0.5, 0.8], [-1,0], [0,-1]]) * 0.8
    
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#050508')
    ax.set_facecolor('#050508')
    ax.set_axis_off()
    
    def update(frame):
        ax.cla()
        ax.set_axis_off()
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        
        # Step
        net.step()
        
        # Draw Network connections (The Collective Web)
        for i in range(N):
            for j in range(i+1, N):
                # Calculate color of edge: Red if disparate phase, Blue if synced
                phase_diff = abs(net.theta[i] - net.theta[j])
                phase_diff = min(phase_diff, 2*np.pi - phase_diff)
                
                if phase_diff < 0.5:
                    ec = '#4ECDC4' # Synced
                    lw = 2
                else: 
                    ec = '#EF4444' # Dissonant
                    lw = 1
                ax.plot([net.pos[i,0], net.pos[j,0]], [net.pos[i,1], net.pos[j,1]], color=ec, alpha=0.5, linewidth=lw)
        
        # Draw Nodes
        # Node 0 is the patient
        # Colors pulse
        colors = []
        for i in range(N):
            val = np.sin(net.theta[i])
            if i == 0:
                # Patient
                c = (1, 0, 0, 0.5 + 0.5*val) # Red pulse
            else:
                # Society
                c = (0, 1, 1, 0.5 + 0.5*val) # Cyan pulse
            colors.append(c)
            
        ax.scatter(net.pos[:,0], net.pos[:,1], c=colors, s=300)
        
        # Text
        # Calculate local sync of Node 0
        diffs = [min(abs(net.theta[0] - net.theta[j]), 2*np.pi - abs(net.theta[0] - net.theta[j])) for j in range(1, N)]
        avg_diff = np.mean(diffs)
        
        status = "CRITICO"
        if avg_diff < 1.0: status = "EM RECUPERACAO"
        if avg_diff < 0.2: status = "CURADO (RESSONANCIA TOTAL)"
        
        ax.text(0, 0.9, f"TERAPIA TOPOLOGICA: {status}", ha='center', color='white', fontsize=14, fontweight='bold')
        ax.text(net.pos[0,0], net.pos[0,1]-0.15, "PACIENTE (Monada 0)", ha='center', color='#EF4444', fontsize=10)
        
    ani = animation.FuncAnimation(fig, update, frames=100, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=15)
    plt.close(fig)
    print(f"    Saved Healing: {path}")


def main():
    print("="*60)
    print("  TAMESIS — Noosphere Simulation (Collective Monad)")
    print("="*60)
    
    simulate_sync()
    simulate_healing()
    
    print("\n" + "="*60)
    print("  Simulation Complete. The Geist is Awake.")
    print("="*60)

if __name__ == "__main__":
    main()
