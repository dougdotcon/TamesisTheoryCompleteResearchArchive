"""
=============================================================================
  TAMESIS RESEARCH — INFO-VIRUS DYNAMICS (NARRATIVE WARS)
=============================================================================

  Objective: Simulate the spread of "Fake News" (High-Entropy Virus)
  and "Truth" (Low-Entropy Kernel) through a network of Monads.

  Model: SIR-Tamesis (Susceptible -> Infected -> Recovered/Immunized)
  - S: Susceptible (Neutral Monad, no strong narrative).
  - I: Infected (Has absorbed the Virus/Fake News).
  - R: Recovered (Has absorbed the Truth/Antikernel).

  Key Innovation:
  - Virus (Fake News):  Low "Logical Depth", cheap to replicate.
                         Spreads FAST but WEAKENS the Spectral Gap.
  - Truth (Kernel):     High "Logical Depth", expensive to process.
                         Spreads SLOW but HEALS the Spectral Gap.

  Dual Interpretation:
  - EPIDEMIOLOGY:  Disease vs Immunity.
  - MEMETICS:      Propaganda vs Critical Thinking.
  - ECONOMICS:     Ponzi Scheme vs Real Value.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from scipy.linalg import eigvalsh
import os

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_NODES = 300
SIM_STEPS = 100
FRAMES = 60

# Infection parameters
VIRUS_SPREAD_RATE = 0.15     # Probability of infecting a neighbor per step
TRUTH_SPREAD_RATE = 0.06     # Truth is harder to spread (high logical depth)
VIRUS_RECOVERY_RATE = 0.02   # Spontaneous recovery from Fake News is rare
TRUTH_IMMUNITY_RATE = 0.005  # Once immunized, very stable

# =============================================================================
# THE ENGINE
# =============================================================================

class InfoVirusEngine:
    def __init__(self):
        # Build a Small-World network (social network topology)
        self.G = nx.watts_strogatz_graph(N_NODES, k=6, p=0.1, seed=42)

        # State: 0=Susceptible, 1=Infected(Virus), 2=Recovered(Truth)
        self.state = np.zeros(N_NODES, dtype=int)

        # Per-node "Spectral Health" (proxy for consciousness/critical thinking)
        self.health = np.ones(N_NODES) * 0.5  # Baseline

        self.history = []  # (step, n_S, n_I, n_R, avg_health, spectral_gap)

    def inject_virus(self, n_seeds=5):
        """Inject Fake News into random nodes (Patient Zero)."""
        seeds = np.random.choice(N_NODES, size=n_seeds, replace=False)
        for s in seeds:
            self.state[s] = 1
            self.health[s] = 0.1  # Virus damages the node
        print(f"[*] Virus Injected into {n_seeds} nodes.")

    def inject_truth(self, n_seeds=3):
        """Inject Truth Kernel into a few strategically placed nodes."""
        # Choose HIGH-DEGREE nodes (influencers)
        degrees = dict(self.G.degree())
        sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
        seeds = sorted_nodes[:n_seeds]
        for s in seeds:
            self.state[s] = 2
            self.health[s] = 1.0  # Truth fully heals
        print(f"[*] Truth Kernel Injected into {n_seeds} high-degree nodes.")

    def step(self):
        """Execute one time step of the SIR-Tamesis model."""
        new_state = self.state.copy()
        new_health = self.health.copy()

        for node in self.G.nodes():
            neighbors = list(self.G.neighbors(node))
            if not neighbors:
                continue

            neighbor_states = self.state[neighbors]

            if self.state[node] == 0:  # SUSCEPTIBLE
                # Can be infected by Virus OR immunized by Truth
                n_infected = np.sum(neighbor_states == 1)
                n_recovered = np.sum(neighbor_states == 2)

                # Probability of catching the Virus
                p_virus = 1 - (1 - VIRUS_SPREAD_RATE) ** n_infected
                # Probability of absorbing the Truth
                p_truth = 1 - (1 - TRUTH_SPREAD_RATE) ** n_recovered

                r = np.random.random()
                if r < p_virus:
                    new_state[node] = 1
                    new_health[node] *= 0.3  # Virus damages health
                elif r < p_virus + p_truth:
                    new_state[node] = 2
                    new_health[node] = min(1.0, new_health[node] + 0.4)

            elif self.state[node] == 1:  # INFECTED (Virus)
                # Small chance of spontaneous recovery
                if np.random.random() < VIRUS_RECOVERY_RATE:
                    new_state[node] = 0
                    new_health[node] += 0.1

                # Can be CURED by Truth neighbors
                n_recovered = np.sum(neighbor_states == 2)
                p_cure = 1 - (1 - TRUTH_SPREAD_RATE * 1.5) ** n_recovered
                if np.random.random() < p_cure:
                    new_state[node] = 2
                    new_health[node] = min(1.0, new_health[node] + 0.5)

                # Virus continues to degrade health
                new_health[node] = max(0.0, new_health[node] - 0.01)

            elif self.state[node] == 2:  # RECOVERED (Truth)
                # Very stable, but not perfectly immune
                if np.random.random() < TRUTH_IMMUNITY_RATE:
                    new_state[node] = 0  # Rare loss of immunity

        self.state = new_state
        self.health = np.clip(new_health, 0, 1)

    def measure(self, t):
        """Record metrics."""
        n_s = np.sum(self.state == 0)
        n_i = np.sum(self.state == 1)
        n_r = np.sum(self.state == 2)
        avg_h = np.mean(self.health)

        # Spectral Gap (consciousness of the network)
        L = nx.laplacian_matrix(self.G).toarray().astype(float)
        # Weight by health: sick nodes weaken connections
        for i in range(N_NODES):
            for j in range(N_NODES):
                if i != j and L[i][j] != 0:
                    L[i][j] *= (self.health[i] + self.health[j]) / 2
            L[i][i] = -np.sum(L[i, :]) + L[i, i]  # Fix diagonal

        eigenvalues = eigvalsh(L)
        spectral_gap = eigenvalues[1] if len(eigenvalues) > 1 else 0

        self.history.append((t, n_s, n_i, n_r, avg_h, spectral_gap))

    def run(self, steps=SIM_STEPS):
        """Run the full SIR simulation."""
        print("[*] Running Info-Virus Simulation...")
        for t in range(steps):
            self.step()
            if t % 2 == 0:
                self.measure(t)
        print(f"    Simulation Complete. Final: S={np.sum(self.state==0)}, "
              f"I={np.sum(self.state==1)}, R={np.sum(self.state==2)}")

    # -------------------------------------------------------------------------
    # VISUALIZATIONS
    # -------------------------------------------------------------------------

    def plot_sir_dynamics(self, filename="sir_dynamics.png"):
        print("[*] Plotting SIR Dynamics...")
        fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
        plt.style.use('dark_background')
        fig.patch.set_facecolor('#0a0a0f')

        times = [h[0] for h in self.history]

        # SIR Curves
        axes[0].fill_between(times, [h[1] for h in self.history],
                             alpha=0.4, color='gray', label='Susceptible')
        axes[0].fill_between(times, [h[2] for h in self.history],
                             alpha=0.6, color='red', label='Infected (Virus)')
        axes[0].fill_between(times, [h[3] for h in self.history],
                             alpha=0.6, color='cyan', label='Recovered (Truth)')
        axes[0].set_ylabel("Population")
        axes[0].set_title("SIR-TAMESIS: NARRATIVE WARS (Fake News vs Truth)")
        axes[0].legend()
        axes[0].grid(True, color='#222222')

        # Average Health
        axes[1].plot(times, [h[4] for h in self.history], color='lime', linewidth=2)
        axes[1].set_ylabel("Avg. Health ($\\lambda_{consciousness}$)")
        axes[1].axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='Critical Threshold')
        axes[1].legend()
        axes[1].grid(True, color='#222222')

        # Spectral Gap
        axes[2].plot(times, [h[5] for h in self.history], color='#FFD700', linewidth=2)
        axes[2].set_ylabel("Spectral Gap ($\\lambda_1$)")
        axes[2].set_xlabel("Time (Steps)")
        axes[2].grid(True, color='#222222')

        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"    Saved: {path}")

    def plot_truth_vs_lies(self, filename="truth_vs_lies.png"):
        """Visualize the final state of the network."""
        print("[*] Plotting Truth vs Lies Map...")
        plt.figure(figsize=(10, 10))
        plt.style.use('dark_background')

        pos = nx.spring_layout(self.G, iterations=50, seed=42)

        # Node colors by state
        colors = []
        sizes = []
        for n in self.G.nodes():
            if self.state[n] == 0:
                colors.append('#444444')  # Grey = Susceptible
                sizes.append(15)
            elif self.state[n] == 1:
                colors.append('#FF0000')  # Red = Infected
                sizes.append(30)
            else:
                colors.append('#00FFFF')  # Cyan = Truth
                sizes.append(25)

        # Edges colored by connection type
        edge_colors = []
        for u, v in self.G.edges():
            if self.state[u] == 1 or self.state[v] == 1:
                edge_colors.append('#330000')  # Dark red = Virus path
            elif self.state[u] == 2 and self.state[v] == 2:
                edge_colors.append('#003333')  # Teal = Truth network
            else:
                edge_colors.append('#111111')

        nx.draw_networkx_edges(self.G, pos, edge_color=edge_colors, width=0.5, alpha=0.4)

        xs = [pos[n][0] for n in self.G.nodes()]
        ys = [pos[n][1] for n in self.G.nodes()]
        plt.scatter(xs, ys, c=colors, s=sizes, zorder=5, alpha=0.8)

        n_i = np.sum(self.state == 1)
        n_r = np.sum(self.state == 2)
        plt.title(f"NARRATIVE WAR: FINAL STATE\n"
                  f"Red = Infected ({n_i}) | Cyan = Immunized ({n_r}) | Grey = Susceptible",
                  color='white', fontsize=13)
        plt.axis('off')

        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"    Saved: {path}")

    def generate_war_gif(self, filename="narrative_war.gif"):
        """Animate the Narrative War in real-time."""
        print("[*] Rendering Narrative War GIF...")
        fig = plt.figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#0a0a0f')

        # Fresh simulation for animation
        anim_G = nx.watts_strogatz_graph(150, k=6, p=0.1, seed=42)
        anim_state = np.zeros(150, dtype=int)
        anim_health = np.ones(150) * 0.5
        pos = nx.spring_layout(anim_G, iterations=50, seed=42)

        # Inject at frame 0
        virus_seeds = np.random.choice(150, size=3, replace=False)
        for s in virus_seeds:
            anim_state[s] = 1
            anim_health[s] = 0.1

        # Inject truth at frame 15
        degrees = dict(anim_G.degree())
        truth_seeds = sorted(degrees, key=degrees.get, reverse=True)[:2]

        def update(frame):
            nonlocal anim_state, anim_health
            ax.cla()
            ax.set_axis_off()
            ax.set_xlim(-1.3, 1.3)
            ax.set_ylim(-1.3, 1.3)

            # Inject truth at frame 15
            if frame == 15:
                for s in truth_seeds:
                    anim_state[s] = 2
                    anim_health[s] = 1.0

            # SIR Step
            if frame > 0:
                new_s = anim_state.copy()
                for node in anim_G.nodes():
                    nbs = list(anim_G.neighbors(node))
                    if not nbs:
                        continue
                    nb_states = anim_state[nbs]

                    if anim_state[node] == 0:
                        n_inf = np.sum(nb_states == 1)
                        n_rec = np.sum(nb_states == 2)
                        p_v = 1 - (1 - 0.12) ** n_inf
                        p_t = 1 - (1 - 0.05) ** n_rec
                        r = np.random.random()
                        if r < p_v:
                            new_s[node] = 1
                            anim_health[node] *= 0.3
                        elif r < p_v + p_t:
                            new_s[node] = 2
                            anim_health[node] = min(1.0, anim_health[node] + 0.4)
                    elif anim_state[node] == 1:
                        n_rec = np.sum(nb_states == 2)
                        p_c = 1 - (1 - 0.08) ** n_rec
                        if np.random.random() < p_c:
                            new_s[node] = 2
                            anim_health[node] = min(1.0, anim_health[node] + 0.5)
                anim_state = new_s

            # Draw
            colors = []
            sizes = []
            for n in anim_G.nodes():
                if anim_state[n] == 0:
                    colors.append('#333333')
                    sizes.append(10)
                elif anim_state[n] == 1:
                    colors.append('#FF0000')
                    sizes.append(25)
                else:
                    colors.append('#00FFFF')
                    sizes.append(20)

            nx.draw_networkx_edges(anim_G, pos, ax=ax, edge_color='#111111',
                                   width=0.3, alpha=0.3)
            xs = [pos[n][0] for n in anim_G.nodes()]
            ys = [pos[n][1] for n in anim_G.nodes()]
            ax.scatter(xs, ys, c=colors, s=sizes, zorder=5, alpha=0.8)

            n_i = np.sum(anim_state == 1)
            n_r = np.sum(anim_state == 2)
            phase = "VIRUS SPREADING" if frame < 15 else "TRUTH DEPLOYED"
            ax.text(0, 1.15, f"NARRATIVE WAR: {phase} (T={frame})",
                    color='white', ha='center', fontweight='bold', fontsize=11)
            ax.text(0, 1.02, f"Infected: {n_i} | Immunized: {n_r}",
                    color='gray', ha='center', fontsize=9)

        ani = animation.FuncAnimation(fig, update, frames=FRAMES, blit=False)
        path = os.path.join(OUTPUT_DIR, filename)
        ani.save(path, writer='pillow', fps=8)
        plt.close(fig)
        print(f"    Saved: {path}")

# =============================================================================
# MAIN
# =============================================================================

def run_simulation():
    print("=" * 60)
    print("  TAMESIS: INFO-VIRUS DYNAMICS (NARRATIVE WARS)")
    print("=" * 60)

    engine = InfoVirusEngine()

    # Phase 1: Inject Virus (Fake News arrives first -- always)
    engine.inject_virus(n_seeds=5)

    # Let the virus spread for a bit
    print("[*] Phase 1: Virus spreading unchecked...")
    for t in range(20):
        engine.step()
        if t % 2 == 0:
            engine.measure(t)

    # Phase 2: Inject Truth (delayed response -- the Kernel awakens)
    engine.inject_truth(n_seeds=3)

    # Phase 3: War
    print("[*] Phase 2: Truth deployed. War begins...")
    for t in range(20, SIM_STEPS):
        engine.step()
        if t % 2 == 0:
            engine.measure(t)

    # Report
    n_s = np.sum(engine.state == 0)
    n_i = np.sum(engine.state == 1)
    n_r = np.sum(engine.state == 2)

    print(f"\n{'='*60}")
    print(f"  FINAL STATE")
    print(f"{'='*60}")
    print(f"  Susceptible: {n_s}")
    print(f"  Infected (Virus/Fake News): {n_i}")
    print(f"  Recovered (Truth/Kernel): {n_r}")
    print(f"  Average Health: {np.mean(engine.health):.3f}")
    print(f"{'='*60}")

    # Visualizations
    engine.plot_sir_dynamics()
    engine.plot_truth_vs_lies()
    engine.generate_war_gif()

    print("\n[SUCCESS] Info-Virus Simulation Completed.")
    print("=" * 60)
    print("INTERPRETATION:")
    print("  Fake News spreads FAST (low logical depth, cheap to replicate).")
    print("  Truth spreads SLOW but HEALS (high logical depth, immune system).")
    print("  Strategic placement of Truth in HIGH-DEGREE nodes is critical.")
    print("=" * 60)

if __name__ == "__main__":
    run_simulation()
