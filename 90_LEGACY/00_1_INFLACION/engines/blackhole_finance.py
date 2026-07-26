"""
=============================================================================
  TAMESIS RESEARCH — FINANCIAL BLACK HOLES & NOOSPHERE MITIGATION
=============================================================================

  Objective: Simulate the formation of "Financial Black Holes" (extreme
  Hub saturation where value is trapped) and test if the Noosphere
  (collective decentralized network) can prevent total collapse.

  Dual Interpretation:
  - COSMOLOGICAL: Supermassive Black Hole formation + Hawking Radiation.
  - ECONOPHYSICAL: "Too Big to Fail" monopolies + DeFi redistribution.

  Phases:
  1. POST-REHEATING: Build a Scale-Free graph (the economy after inflation).
  2. BLACK HOLE FORMATION: Let Hubs absorb edges until Event Horizon.
  3. SCENARIO A (No Intervention): Pure gravitational collapse.
  4. SCENARIO B (Noosphere): Hawking Radiation + Decentralized Bridges.
  5. COMPARISON: Gini, Survival Rate, Hub Mass.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from collections import Counter
import copy
import os

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_NODES = 400
COLLAPSE_STEPS = 150
FRAMES = 60

# =============================================================================
# HELPER: Build a Post-Reheating Economy
# =============================================================================

def build_post_reheating_graph(n=N_NODES):
    """
    Create a Scale-Free graph representing the economy AFTER Reheating.
    Uses Barabasi-Albert model (preferential attachment = capitalism).
    """
    G = nx.barabasi_albert_graph(n, m=2, seed=42)
    return G

def gini(degrees):
    sorted_vals = np.sort(np.array(degrees, dtype=float))
    n = len(sorted_vals)
    if n == 0 or np.sum(sorted_vals) == 0:
        return 0
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * sorted_vals) / (n * np.sum(sorted_vals))) - (n + 1) / n

# =============================================================================
# SCENARIO A: PURE COLLAPSE (No Intervention)
# =============================================================================

def simulate_collapse(G, steps=COLLAPSE_STEPS):
    """
    Pure gravitational collapse: edges flow from poor to rich.
    No intervention. The strong devour the weak.
    """
    history = []  # (step, gini, max_hub_share, survival_rate, n_edges)

    for step in range(steps):
        degrees = dict(G.degree())
        total_edges = G.number_of_edges()

        if total_edges == 0:
            break

        # Find poorest nodes (degree 1-2)
        poor = [n for n, d in degrees.items() if 0 < d <= 2]
        if not poor:
            poor = [n for n, d in degrees.items() if d > 0][:5]
        if not poor:
            break

        # Find richest node
        richest = max(degrees, key=degrees.get)

        # Transfer 1-3 edges from poor to rich
        for _ in range(min(3, len(poor))):
            donor = np.random.choice(poor)
            neighbors = list(G.neighbors(donor))
            if not neighbors:
                continue
            nb = np.random.choice(neighbors)
            G.remove_edge(donor, nb)
            if not G.has_edge(nb, richest) and nb != richest:
                G.add_edge(nb, richest)

        # Record
        degrees = dict(G.degree())
        all_deg = list(degrees.values())
        max_deg = max(all_deg) if all_deg else 0
        total_e = G.number_of_edges()
        hub_share = max_deg / (2 * total_e) if total_e > 0 else 0
        alive = sum(1 for d in all_deg if d > 0)
        survival = alive / len(all_deg) if all_deg else 0

        history.append((step, gini(all_deg), hub_share, survival, total_e))

    return history

# =============================================================================
# SCENARIO B: NOOSPHERE INTERVENTION
# =============================================================================

def simulate_noosphere(G, steps=COLLAPSE_STEPS):
    """
    Same gravitational collapse, BUT with two Noosphere mechanisms:
    1. Hawking Radiation: The biggest Hub leaks 1-2 edges per step.
    2. Decentralized Bridges: Random peer-to-peer edges are created.
    """
    history = []

    for step in range(steps):
        degrees = dict(G.degree())
        total_edges = G.number_of_edges()

        if total_edges == 0:
            break

        # --- GRAVITATIONAL COLLAPSE (same as Scenario A) ---
        poor = [n for n, d in degrees.items() if 0 < d <= 2]
        if not poor:
            poor = [n for n, d in degrees.items() if d > 0][:5]
        if not poor:
            break

        richest = max(degrees, key=degrees.get)

        for _ in range(min(3, len(poor))):
            donor = np.random.choice(poor)
            neighbors = list(G.neighbors(donor))
            if not neighbors:
                continue
            nb = np.random.choice(neighbors)
            G.remove_edge(donor, nb)
            if not G.has_edge(nb, richest) and nb != richest:
                G.add_edge(nb, richest)

        # --- NOOSPHERE MECHANISM 1: HAWKING RADIATION ---
        # The Black Hole leaks edges back to the network
        degrees = dict(G.degree())
        richest = max(degrees, key=degrees.get)

        if degrees[richest] > 5:  # Only leak if Hub is big enough
            for _ in range(2):
                # Must re-fetch neighbors each iteration (graph mutates)
                current_nbs = list(G.neighbors(richest))
                if not current_nbs:
                    break
                leaked_nb = np.random.choice(current_nbs)
                if G.has_edge(richest, leaked_nb):
                    G.remove_edge(richest, leaked_nb)

                    # Give leaked edge to a random isolated/poor node
                    isolated = [n for n, d in G.degree() if d <= 1 and n != richest]
                    if isolated:
                        receiver = np.random.choice(isolated)
                        if not G.has_edge(leaked_nb, receiver):
                            G.add_edge(leaked_nb, receiver)

        # --- NOOSPHERE MECHANISM 2: DECENTRALIZED BRIDGES ---
        # Peer-to-peer connections (DeFi / Open Source / Cooperation)
        degrees = dict(G.degree())
        non_hub = [n for n, d in degrees.items() if 1 < d < 10]
        if len(non_hub) >= 2:
            a, b = np.random.choice(non_hub, size=2, replace=False)
            if not G.has_edge(a, b):
                G.add_edge(a, b)

        # Record
        degrees = dict(G.degree())
        all_deg = list(degrees.values())
        max_deg = max(all_deg) if all_deg else 0
        total_e = G.number_of_edges()
        hub_share = max_deg / (2 * total_e) if total_e > 0 else 0
        alive = sum(1 for d in all_deg if d > 0)
        survival = alive / len(all_deg) if all_deg else 0

        history.append((step, gini(all_deg), hub_share, survival, total_e))

    return history

# =============================================================================
# VISUALIZATIONS
# =============================================================================

def plot_gini_comparison(hist_a, hist_b, filename="gini_comparison.png"):
    print("[*] Plotting Gini Comparison...")
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    steps_a = [h[0] for h in hist_a]
    steps_b = [h[0] for h in hist_b]

    # Gini
    axes[0].plot(steps_a, [h[1] for h in hist_a], color='red', linewidth=2,
                 label='No Intervention (Collapse)')
    axes[0].plot(steps_b, [h[1] for h in hist_b], color='cyan', linewidth=2,
                 label='Noosphere (Hawking + DeFi)')
    axes[0].set_ylabel("Gini Coefficient")
    axes[0].set_title("GINI COEFFICIENT: COLLAPSE vs NOOSPHERE")
    axes[0].legend()
    axes[0].grid(True, color='#222222')

    # Hub Share
    axes[1].plot(steps_a, [h[2] for h in hist_a], color='red', linewidth=2,
                 label='No Intervention')
    axes[1].plot(steps_b, [h[2] for h in hist_b], color='cyan', linewidth=2,
                 label='Noosphere')
    axes[1].axhline(y=0.3, color='yellow', linestyle='--', alpha=0.5,
                    label='Event Horizon (30%)')
    axes[1].set_ylabel("Hub Share (% of Edges)")
    axes[1].legend()
    axes[1].grid(True, color='#222222')

    # Survival Rate
    axes[2].plot(steps_a, [h[3] for h in hist_a], color='red', linewidth=2,
                 label='No Intervention')
    axes[2].plot(steps_b, [h[3] for h in hist_b], color='cyan', linewidth=2,
                 label='Noosphere')
    axes[2].set_ylabel("Survival Rate")
    axes[2].set_xlabel("Time (Steps)")
    axes[2].legend()
    axes[2].grid(True, color='#222222')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_noosphere_comparison(G_collapse, G_noosphere, filename="noosphere_mitigation.png"):
    print("[*] Plotting Noosphere Side-by-Side...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    for idx, (G, title) in enumerate([(G_collapse, "WITHOUT Noosphere\n(Pure Collapse)"),
                                       (G_noosphere, "WITH Noosphere\n(Hawking + DeFi)")]):
        ax = axes[idx]
        ax.set_facecolor('black')

        pos = nx.spring_layout(G, iterations=30, seed=42)
        degrees = dict(G.degree())

        # Node colors and sizes
        node_colors = []
        node_sizes = []
        for n in G.nodes():
            d = degrees.get(n, 0)
            if d > 20:
                node_colors.append('#FF0000')  # Red = Black Hole
                node_sizes.append(d * 4)
            elif d > 5:
                node_colors.append('#FFD700')  # Gold = Galaxy
                node_sizes.append(d * 2)
            elif d > 0:
                node_colors.append('#00ffff')  # Cyan = Alive
                node_sizes.append(10)
            else:
                node_colors.append('#222222')  # Dark = Dead
                node_sizes.append(3)

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='white', alpha=0.08, width=0.3)

        xs = [pos[n][0] for n in G.nodes()]
        ys = [pos[n][1] for n in G.nodes()]
        ax.scatter(xs, ys, c=node_colors, s=node_sizes, zorder=5, alpha=0.8)

        alive = sum(1 for d in degrees.values() if d > 0)
        g = gini(list(degrees.values()))
        ax.set_title(title, color='white', fontsize=14, fontweight='bold')
        ax.text(0.5, -0.05, f"Survival: {alive}/{len(G)} | Gini: {g:.3f}",
                transform=ax.transAxes, ha='center', color='gray', fontsize=10)
        ax.axis('off')

    plt.suptitle("FINANCIAL BLACK HOLES: COLLAPSE vs NOOSPHERE MITIGATION",
                 color='white', fontsize=16, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def generate_blackhole_gif(filename="financial_blackhole.gif"):
    print("[*] Rendering Financial Black Hole GIF...")
    fig = plt.figure(figsize=(8, 8), dpi=100)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor('black')

    anim_G = build_post_reheating_graph(150)  # Smaller for animation
    pos = nx.spring_layout(anim_G, iterations=50, seed=42)

    noosphere_active = False

    def update(frame):
        nonlocal noosphere_active
        ax.cla()
        ax.set_axis_off()
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        degrees = dict(anim_G.degree())

        # Phase: First half = Collapse, Second half = Noosphere kicks in
        if frame < FRAMES // 2:
            phase_label = "GRAVITATIONAL COLLAPSE"
            bg = '#0a0000'
            # Collapse: poor -> rich
            poor = [n for n, d in degrees.items() if 0 < d <= 2]
            if poor:
                richest = max(degrees, key=degrees.get)
                donor = np.random.choice(poor)
                nbs = list(anim_G.neighbors(donor))
                if nbs:
                    nb = np.random.choice(nbs)
                    anim_G.remove_edge(donor, nb)
                    if not anim_G.has_edge(nb, richest) and nb != richest:
                        anim_G.add_edge(nb, richest)
        else:
            phase_label = "NOOSPHERE ACTIVATED"
            bg = '#000a0a'
            noosphere_active = True

            # Still some collapse
            poor = [n for n, d in degrees.items() if 0 < d <= 2]
            if poor:
                richest = max(degrees, key=degrees.get)
                donor = np.random.choice(poor)
                nbs = list(anim_G.neighbors(donor))
                if nbs:
                    nb = np.random.choice(nbs)
                    anim_G.remove_edge(donor, nb)
                    if not anim_G.has_edge(nb, richest) and nb != richest:
                        anim_G.add_edge(nb, richest)

            # Hawking Radiation
            degrees = dict(anim_G.degree())
            richest = max(degrees, key=degrees.get)
            rich_nbs = list(anim_G.neighbors(richest))
            if len(rich_nbs) > 3:
                leaked = np.random.choice(rich_nbs)
                anim_G.remove_edge(richest, leaked)
                isolated = [n for n, d in degrees.items() if d <= 1 and n != richest]
                if isolated:
                    recv = np.random.choice(isolated)
                    if not anim_G.has_edge(leaked, recv):
                        anim_G.add_edge(leaked, recv)

            # DeFi Bridge
            non_hub = [n for n, d in degrees.items() if 1 < d < 8]
            if len(non_hub) >= 2:
                a, b = np.random.choice(non_hub, size=2, replace=False)
                if not anim_G.has_edge(a, b):
                    anim_G.add_edge(a, b)

        fig.patch.set_facecolor(bg)

        # Draw
        degrees = dict(anim_G.degree())
        node_colors = []
        node_sizes = []
        for n in anim_G.nodes():
            d = degrees.get(n, 0)
            if d > 15:
                node_colors.append('#FF0000')
                node_sizes.append(d * 5)
                # Pull toward center (gravitational attraction)
                pos[n] = pos[n] * 0.98
            elif d > 3:
                node_colors.append('#FFD700' if not noosphere_active else '#00ffcc')
                node_sizes.append(d * 2)
            elif d > 0:
                node_colors.append('#444444')
                node_sizes.append(5)
            else:
                node_colors.append('#111111')
                node_sizes.append(1)

        edges = list(anim_G.edges())
        if edges:
            nx.draw_networkx_edges(anim_G, pos, ax=ax, edge_color='white',
                                   alpha=0.1, width=0.3)

        xs = [pos[n][0] for n in anim_G.nodes()]
        ys = [pos[n][1] for n in anim_G.nodes()]
        ax.scatter(xs, ys, c=node_colors, s=node_sizes, zorder=5, alpha=0.8)

        g = gini(list(degrees.values()))
        ax.text(0, 1.3, f"TAMESIS: {phase_label}", color='white',
                ha='center', fontweight='bold', fontsize=12)
        ax.text(0, 1.15, f"Gini = {g:.3f}", color='gray',
                ha='center', fontsize=9)

    ani = animation.FuncAnimation(fig, update, frames=FRAMES, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=10)
    plt.close(fig)
    print(f"    Saved: {path}")

# =============================================================================
# MAIN
# =============================================================================

def run_simulation():
    print("=" * 60)
    print("  TAMESIS: FINANCIAL BLACK HOLES & NOOSPHERE MITIGATION")
    print("=" * 60)

    # Build two identical economies
    G_base = build_post_reheating_graph()
    G_collapse = copy.deepcopy(G_base)
    G_noosphere = copy.deepcopy(G_base)

    # Scenario A: Pure Collapse
    print("\n--- SCENARIO A: PURE COLLAPSE (No Intervention) ---")
    hist_a = simulate_collapse(G_collapse)

    # Scenario B: Noosphere Intervention
    print("\n--- SCENARIO B: NOOSPHERE (Hawking + DeFi) ---")
    hist_b = simulate_noosphere(G_noosphere)

    # Report
    deg_a = list(dict(G_collapse.degree()).values())
    deg_b = list(dict(G_noosphere.degree()).values())
    alive_a = sum(1 for d in deg_a if d > 0)
    alive_b = sum(1 for d in deg_b if d > 0)

    print(f"\n{'='*60}")
    print(f"  RESULTS")
    print(f"{'='*60}")
    print(f"  Scenario A (Collapse):  Gini={gini(deg_a):.3f}  Alive={alive_a}/{N_NODES}")
    print(f"  Scenario B (Noosphere): Gini={gini(deg_b):.3f}  Alive={alive_b}/{N_NODES}")
    print(f"{'='*60}")

    # Visualizations
    plot_gini_comparison(hist_a, hist_b)
    plot_noosphere_comparison(G_collapse, G_noosphere)
    generate_blackhole_gif()

    print("\n[SUCCESS] Financial Black Holes Simulation Completed.")
    print("=" * 60)
    print("INTERPRETATION:")
    print("  Without Noosphere: Black Holes devour everything (Too Big to Fail).")
    print("  With Noosphere:    Hawking Radiation + DeFi stabilize the system.")
    print("=" * 60)

if __name__ == "__main__":
    run_simulation()
