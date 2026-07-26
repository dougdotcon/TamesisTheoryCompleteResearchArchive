"""
=============================================================================
  TAMESIS RESEARCH — REHEATING ENGINE (PHASE TRANSITION)
=============================================================================

  Objective: Simulate the end of Cosmic Inflation, when vacuum energy
  condenses into Real Matter (high-degree Hubs).

  Dual Interpretation:
  - COSMOLOGICAL: Vacuum Energy -> Particles (Galaxies, Stars).
  - ECONOPHYSICAL: Fiat Money -> Real Assets (Gold, BTC, Land).

  Dark Matter Correction (Tamesis Canon):
  - Dark Matter is NOT disconnected nodes.
  - It IS the "Elastic Memory" of the vacuum: topological tension
    left behind by inflation that exerts extra gravitational pull.

  Phases:
  1. INFLATION:  Graph grows exponentially. Track "Edge Tension".
  2. SATURATION: Entropy stalls. Tension exceeds critical threshold.
  3. REHEATING:  Expansion stops. Low-degree nodes donate edges to Hubs.
  4. MEASUREMENT: Degree distribution, Gini coefficient, Tension map.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from collections import Counter
import os

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_INFLATION = 500    # Nodes created during inflation
N_REHEATING_STEPS = 200  # Rewiring steps during reheating
FRAMES = 60

# =============================================================================
# THE ENGINE
# =============================================================================

class ReheatingEngine:
    def __init__(self):
        self.G = nx.Graph()
        self.G.add_node(0)
        self.history = []  # (phase, time, N_nodes, entropy, tension, gini)
        self.tension_field = {}  # Per-edge tension

    # -------------------------------------------------------------------------
    # PHASE 1: INFLATION
    # -------------------------------------------------------------------------
    def inflate(self):
        """
        Expand the graph exponentially.
        Track "Edge Tension" = how stretched each edge is relative to
        the expanding diameter. This is the DARK MATTER proxy.
        """
        print("[PHASE 1] Inflation (Expanding the Vacuum)...")

        for i in range(1, N_INFLATION):
            # Temperature decays: early universe is random, late is gravitational
            temp = 1.0 - (i / N_INFLATION)

            if np.random.random() < temp * 0.6:
                # Random attachment (Quantum foam / Credit creation)
                target = np.random.choice(list(self.G.nodes()))
            else:
                # Preferential attachment (Gravity / Capital accumulation)
                degrees = np.array([d for _, d in self.G.degree()])
                if degrees.sum() > 0:
                    probs = degrees / degrees.sum()
                    target = np.random.choice(list(self.G.nodes()), p=probs)
                else:
                    target = 0

            self.G.add_edge(i, target)

            # Also add 1-2 extra random edges to create richer topology
            if i > 10 and np.random.random() < 0.3:
                extra_target = np.random.choice(list(self.G.nodes()))
                if extra_target != i:
                    self.G.add_edge(i, extra_target)

            if i % 25 == 0:
                self._record("INFLATION", i)

        print(f"    Inflation Complete. N={self.G.number_of_nodes()}, E={self.G.number_of_edges()}")

    # -------------------------------------------------------------------------
    # PHASE 2: SATURATION DETECTION
    # -------------------------------------------------------------------------
    def detect_saturation(self):
        """
        Check if entropy growth has stalled (dS/dt -> 0).
        """
        print("[PHASE 2] Detecting Saturation Point...")
        if len(self.history) < 3:
            print("    Not enough history. Proceeding to Reheating.")
            return

        recent_entropies = [h[3] for h in self.history[-5:]]
        delta_s = np.diff(recent_entropies)
        avg_delta = np.mean(np.abs(delta_s))

        print(f"    Average dS/dt = {avg_delta:.4f}")
        if avg_delta < 0.05:
            print("    >> SATURATION DETECTED: Entropy growth has stalled!")
        else:
            print("    >> Still expanding. Forcing Reheating for simulation.")

    # -------------------------------------------------------------------------
    # PHASE 3: REHEATING (CONDENSATION)
    # -------------------------------------------------------------------------
    def reheat(self):
        """
        The expansion stops. Now we REWIRE:
        - Low-degree nodes lose edges.
        - High-degree nodes gain edges.
        This simulates gravitational collapse / wealth concentration.
        """
        print("[PHASE 3] Reheating (Condensation of Matter)...")

        for step in range(N_REHEATING_STEPS):
            # Find a low-degree node (the "poor" / "void")
            degrees = dict(self.G.degree())
            min_deg_nodes = [n for n, d in degrees.items() if d <= 2 and d > 0]

            if not min_deg_nodes:
                break  # Everyone is already connected or collapsed

            donor = np.random.choice(min_deg_nodes)
            donor_neighbors = list(self.G.neighbors(donor))

            if not donor_neighbors:
                continue

            # Find a high-degree node (the "rich" / "galaxy")
            max_deg = max(degrees.values())
            rich_nodes = [n for n, d in degrees.items() if d >= max_deg * 0.5 and n != donor]

            if not rich_nodes:
                continue

            receiver = np.random.choice(rich_nodes)

            # Transfer one edge from donor's neighbor to the receiver
            neighbor = np.random.choice(donor_neighbors)
            self.G.remove_edge(donor, neighbor)

            if not self.G.has_edge(neighbor, receiver):
                self.G.add_edge(neighbor, receiver)

            if step % 25 == 0:
                self._record("REHEATING", N_INFLATION + step)

        print(f"    Reheating Complete. N={self.G.number_of_nodes()}, E={self.G.number_of_edges()}")

    # -------------------------------------------------------------------------
    # MEASUREMENTS
    # -------------------------------------------------------------------------
    def _record(self, phase, t):
        degrees = [d for _, d in self.G.degree()]
        counts = np.bincount(degrees)
        probs = counts[counts > 0] / sum(counts)
        entropy = -np.sum(probs * np.log(probs + 1e-12))

        # Tension: ratio of actual edges to max possible (density)
        n = self.G.number_of_nodes()
        max_edges = n * (n - 1) / 2
        tension = self.G.number_of_edges() / max_edges if max_edges > 0 else 0

        # Gini Coefficient of degree distribution
        gini = self._gini(degrees)

        self.history.append((phase, t, n, entropy, tension, gini))

    def _gini(self, values):
        sorted_vals = np.sort(values)
        n = len(sorted_vals)
        if n == 0 or np.sum(sorted_vals) == 0:
            return 0
        index = np.arange(1, n + 1)
        return (2 * np.sum(index * sorted_vals) / (n * np.sum(sorted_vals))) - (n + 1) / n

    def compute_dark_matter(self):
        """
        Dark Matter = Elastic Memory = Edges connecting distant nodes.
        If two connected nodes are "far away" in the graph (high shortest path
        if we remove their direct edge), the edge is under high tension.
        We approximate this with: Tension(e) = 1 / (local_clustering(u) + local_clustering(v) + eps)
        Low clustering around an edge means it's a "long-range scar" = Dark Matter.
        """
        print("[*] Computing Dark Matter Tension Field...")
        clustering = nx.clustering(self.G)
        for u, v in self.G.edges():
            c_u = clustering.get(u, 0)
            c_v = clustering.get(v, 0)
            self.tension_field[(u, v)] = 1.0 / (c_u + c_v + 0.01)

        print(f"    Dark Matter Edges Mapped: {len(self.tension_field)}")

    # -------------------------------------------------------------------------
    # VISUALIZATIONS
    # -------------------------------------------------------------------------
    def plot_mass_distribution(self, filename="mass_distribution.png"):
        print("[*] Plotting Mass Distribution (Power Law)...")
        plt.figure(figsize=(10, 6))
        plt.style.use('dark_background')

        degrees = [d for _, d in self.G.degree()]
        degree_count = Counter(degrees)
        ks = sorted(degree_count.keys())
        pk = [degree_count[k] / len(degrees) for k in ks]

        plt.loglog(ks, pk, 'o', color='cyan', markersize=6, alpha=0.7, label='Post-Reheating')

        # Fit power law line
        log_ks = np.log(np.array(ks[1:], dtype=float))
        log_pk = np.log(np.array(pk[1:], dtype=float))
        if len(log_ks) > 2:
            coeffs = np.polyfit(log_ks, log_pk, 1)
            gamma = -coeffs[0]
            fit_line = np.exp(coeffs[1]) * np.array(ks[1:])**coeffs[0]
            plt.loglog(ks[1:], fit_line, '--', color='red', linewidth=2,
                       label=f'Power Law: $\\gamma = {gamma:.2f}$')

        plt.xlabel("Degree $k$ (Mass / Connectivity)")
        plt.ylabel("$P(k)$ (Frequency)")
        plt.title("MASS DISTRIBUTION AFTER REHEATING\n(Scale-Free Universe)")
        plt.legend()
        plt.grid(True, color='#333333', alpha=0.5)

        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"    Saved: {path}")

    def plot_dark_matter(self, filename="dark_matter_tension.png"):
        print("[*] Plotting Dark Matter Tension Map...")
        plt.figure(figsize=(10, 10))
        plt.style.use('dark_background')

        pos = nx.spring_layout(self.G, iterations=50, seed=42)

        # Color edges by tension
        tensions = list(self.tension_field.values())
        t_min, t_max = min(tensions), max(tensions)

        # Normalize
        norm_tensions = [(t - t_min) / (t_max - t_min + 1e-12) for t in tensions]

        # Draw low-tension edges (Normal Matter) in grey
        # Draw high-tension edges (Dark Matter) in purple
        for (u, v), nt in zip(self.tension_field.keys(), norm_tensions):
            if nt > 0.7:
                color = '#8B5CF6'  # Purple = Dark Matter
                alpha = 0.8
                width = 1.5
            else:
                color = '#333333'  # Grey = Normal
                alpha = 0.2
                width = 0.3
            plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                     color=color, alpha=alpha, linewidth=width)

        # Draw nodes sized by degree
        degrees = dict(self.G.degree())
        node_sizes = [max(degrees[n] * 3, 5) for n in self.G.nodes()]
        node_colors = ['#00ffff' if degrees[n] > 5 else '#444444' for n in self.G.nodes()]

        xs = [pos[n][0] for n in self.G.nodes()]
        ys = [pos[n][1] for n in self.G.nodes()]
        plt.scatter(xs, ys, s=node_sizes, c=node_colors, alpha=0.7, zorder=5)

        plt.title("DARK MATTER TENSION MAP\nPurple = Elastic Memory (Dark Matter) | Cyan = Visible Matter")
        plt.axis('off')

        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"    Saved: {path}")

    def plot_evolution(self, filename="reheating_evolution.png"):
        print("[*] Plotting Phase Evolution...")
        fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
        plt.style.use('dark_background')
        fig.patch.set_facecolor('#0a0a0f')

        times = [h[1] for h in self.history]
        entropy = [h[3] for h in self.history]
        tension = [h[4] for h in self.history]
        gini = [h[5] for h in self.history]

        # Color by phase
        infl_mask = [h[0] == "INFLATION" for h in self.history]
        reh_mask = [h[0] == "REHEATING" for h in self.history]

        # Entropy
        axes[0].plot(times, entropy, color='cyan', linewidth=2)
        axes[0].axvline(x=N_INFLATION, color='red', linestyle='--', alpha=0.5, label='Reheating Start')
        axes[0].set_ylabel("Shannon Entropy (S)")
        axes[0].set_title("THERMODYNAMIC EVOLUTION: INFLATION -> REHEATING")
        axes[0].legend()
        axes[0].grid(True, color='#222222')

        # Tension (Dark Matter)
        axes[1].plot(times, tension, color='#8B5CF6', linewidth=2)
        axes[1].axvline(x=N_INFLATION, color='red', linestyle='--', alpha=0.5)
        axes[1].set_ylabel("Edge Tension (Dark Matter)")
        axes[1].grid(True, color='#222222')

        # Gini (Inequality)
        axes[2].plot(times, gini, color='#FF5733', linewidth=2)
        axes[2].axvline(x=N_INFLATION, color='red', linestyle='--', alpha=0.5)
        axes[2].set_ylabel("Gini Coefficient (Inequality)")
        axes[2].set_xlabel("Time (Nodes / Steps)")
        axes[2].grid(True, color='#222222')

        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"    Saved: {path}")

    def generate_transition_gif(self, filename="reheating_transition.gif"):
        """
        Animate the Phase Transition.
        """
        print("[*] Rendering Phase Transition GIF...")
        fig = plt.figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.set_axis_off()

        # Pre-compute layout at different stages
        # We'll simulate in real-time for the animation
        anim_G = nx.Graph()
        anim_G.add_node(0)
        pos = {0: np.array([0.0, 0.0])}

        def update(frame):
            ax.cla()
            ax.set_axis_off()
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(-2.5, 2.5)

            # Phase logic
            inflation_frames = FRAMES // 2
            reheating_frames = FRAMES - inflation_frames

            if frame < inflation_frames:
                # INFLATION PHASE
                phase = "INFLATION"
                t = frame / inflation_frames
                target_n = int(np.exp(t * np.log(N_INFLATION * 0.3)))  # Smaller for visual
                target_n = max(target_n, anim_G.number_of_nodes())

                for i in range(anim_G.number_of_nodes(), target_n):
                    if anim_G.number_of_nodes() > 0:
                        degrees = np.array([d for _, d in anim_G.degree()])
                        if degrees.sum() > 0:
                            probs = degrees / degrees.sum()
                            tgt = np.random.choice(list(anim_G.nodes()), p=probs)
                        else:
                            tgt = 0
                        anim_G.add_edge(i, tgt)
                        angle = np.random.random() * 2 * np.pi
                        radius = np.random.random() * t * 2
                        pos[i] = np.array([np.cos(angle)*radius, np.sin(angle)*radius])

                bg_color = '#001122'  # Blue = Cold Inflation
            else:
                # REHEATING PHASE
                phase = "REHEATING"
                reh_t = (frame - inflation_frames) / reheating_frames

                # Rewire: move edges from low-degree to high-degree
                deg = dict(anim_G.degree())
                low = [n for n, d in deg.items() if d <= 2 and d > 0]
                if low:
                    donor = np.random.choice(low)
                    neighbors = list(anim_G.neighbors(donor))
                    if neighbors:
                        max_d = max(deg.values())
                        rich = [n for n, d in deg.items() if d >= max_d * 0.3 and n != donor]
                        if rich:
                            receiver = np.random.choice(rich)
                            nb = np.random.choice(neighbors)
                            anim_G.remove_edge(donor, nb)
                            if not anim_G.has_edge(nb, receiver):
                                anim_G.add_edge(nb, receiver)
                            # Pull receiver position toward center (condensation)
                            pos[receiver] = pos[receiver] * 0.95

                bg_color = '#220000'  # Red = Hot Reheating

            fig.patch.set_facecolor(bg_color)

            # Draw
            degrees = dict(anim_G.degree())
            node_colors = []
            node_sizes = []
            for n in anim_G.nodes():
                d = degrees.get(n, 0)
                if d > 8:
                    node_colors.append('#FFD700')  # Gold = Hub / Galaxy
                    node_sizes.append(d * 5)
                elif d > 3:
                    node_colors.append('#00ffff')  # Cyan = Normal Matter
                    node_sizes.append(d * 3)
                else:
                    node_colors.append('#333333')  # Grey = Void
                    node_sizes.append(3)

            valid_edges = [(u, v) for u, v in anim_G.edges() if u in pos and v in pos]
            if valid_edges:
                nx.draw_networkx_edges(anim_G, pos, edgelist=valid_edges,
                                       ax=ax, edge_color='white', alpha=0.15, width=0.3)

            xs = [pos[n][0] for n in anim_G.nodes() if n in pos]
            ys = [pos[n][1] for n in anim_G.nodes() if n in pos]
            cs = [node_colors[i] for i, n in enumerate(anim_G.nodes()) if n in pos]
            ss = [node_sizes[i] for i, n in enumerate(anim_G.nodes()) if n in pos]
            ax.scatter(xs, ys, c=cs, s=ss, zorder=5, alpha=0.8)

            ax.text(0, 2.2, f"TAMESIS: {phase}", color='white', ha='center', fontweight='bold', fontsize=14)

        ani = animation.FuncAnimation(fig, update, frames=FRAMES, blit=False)
        path = os.path.join(OUTPUT_DIR, filename)
        ani.save(path, writer='pillow', fps=12)
        plt.close(fig)
        print(f"    Saved Transition: {path}")

# =============================================================================
# MAIN
# =============================================================================

def run_simulation():
    engine = ReheatingEngine()

    # Phase 1
    engine.inflate()

    # Phase 2
    engine.detect_saturation()

    # Phase 3
    engine.reheat()

    # Phase 4: Measure
    engine.compute_dark_matter()

    # Visualize
    engine.plot_evolution()
    engine.plot_mass_distribution()
    engine.plot_dark_matter()
    engine.generate_transition_gif()

    print("\n[SUCCESS] Reheating Simulation Completed.")
    print("=" * 60)
    print("INTERPRETATION:")
    print("  COSMOLOGICAL: Vacuum -> Galaxies (Hubs) + Voids (Isolates)")
    print("  ECONOPHYSICAL: Fiat -> Real Assets (BTC/Gold) + Bankruptcies")
    print("=" * 60)

if __name__ == "__main__":
    run_simulation()
