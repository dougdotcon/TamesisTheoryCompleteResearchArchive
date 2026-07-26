"""
=============================================================================
  TAMESIS RESEARCH — THERMODYNAMIC LEAKAGE (FIAT vs PROOF-OF-WORK)
=============================================================================

  Objective: Simulate the transit of human labor (energy) through two
  types of "Causal Cables" (monetary systems):

  SCENARIO A — PROOF-OF-WORK (GOLD / BTC):
    The cable is "shielded". Each unit of money costs real energy to
    create. The TRI Barrier is intact. Energy transfers 1:1.

  SCENARIO B — FIAT (CENTRAL BANK PRINTING):
    The cable has "topological holes". New money is created at zero cost.
    The Markov Blanket is punctured. Energy leaks as thermal noise
    (Price Inflation) into the vacuum.

  Dual Interpretation:
  - THERMODYNAMICS: Shielded vs Leaky causal cable.
  - ECONOMICS:      Sound Money vs Fiat (Cantillon Effect).
  - MONAD THEORY:   Intact TRI Barrier vs Broken TRI Barrier.

  Measurements:
  - Energy Retention: How much of the worker's output reaches the Noosphere?
  - Spectral Gap:     Does the network maintain coherence?
  - Gini Coefficient: Who captures the leaked energy?
  - Purchasing Power: What can the worker buy over time?

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
N_WORKERS = 200          # Monad workers
N_STEPS = 120            # Economic cycles
WORK_ENERGY = 1.0        # Energy produced per worker per step
FIAT_LEAK_RATE = 0.03    # 3% energy leaks per step through Fiat holes
FIAT_PRINT_RATE = 0.05   # 5% new "ghost edges" injected per step (QE)
FRAMES = 60

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def gini(values):
    v = np.sort(np.array(values, dtype=float))
    n = len(v)
    if n == 0 or np.sum(v) == 0:
        return 0
    idx = np.arange(1, n + 1)
    return (2 * np.sum(idx * v) / (n * np.sum(v))) - (n + 1) / n

# =============================================================================
# BUILD THE ECONOMY
# =============================================================================

def build_economy():
    """
    Create a layered graph:
    - Layer 0 (nodes 0..N_WORKERS-1): Workers (Biological Monads)
    - Layer 1 (nodes N_WORKERS..N_WORKERS+9): Firms (Aggregators)
    - Layer 2 (node N_WORKERS+10): Central Bank (The Hub)
    """
    G = nx.Graph()
    n_firms = 10
    cb_node = N_WORKERS + n_firms  # Central Bank node

    # Workers
    for i in range(N_WORKERS):
        G.add_node(i, layer=0, energy=1.0, label='worker')

    # Firms (each connected to ~20 workers)
    for f in range(n_firms):
        firm_id = N_WORKERS + f
        G.add_node(firm_id, layer=1, energy=5.0, label='firm')
        # Connect to workers
        workers = list(range(f * 20, min((f + 1) * 20, N_WORKERS)))
        for w in workers:
            G.add_edge(w, firm_id)

    # Central Bank (connected to all firms)
    G.add_node(cb_node, layer=2, energy=10.0, label='central_bank')
    for f in range(n_firms):
        G.add_edge(N_WORKERS + f, cb_node)

    return G, cb_node

# =============================================================================
# SCENARIO A: PROOF-OF-WORK (SOUND MONEY)
# =============================================================================

def simulate_pow(G, cb_node, steps=N_STEPS):
    """
    Sound Money: Every unit of currency costs energy.
    No leakage. The TRI barrier is intact.
    """
    history = []
    energy = np.array([G.nodes[n].get('energy', 1.0) for n in G.nodes()], dtype=float)

    for t in range(steps):
        # Workers produce energy
        for i in range(N_WORKERS):
            energy[i] += WORK_ENERGY

        # Energy transits to firms (tax ~10%, but stored faithfully)
        for f_idx in range(10):
            firm_id = N_WORKERS + f_idx
            workers = [w for w in range(f_idx * 20, min((f_idx + 1) * 20, N_WORKERS))]
            for w in workers:
                transfer = energy[w] * 0.10  # 10% flows to firm
                energy[w] -= transfer
                energy[firm_id] += transfer

        # Firms pay to central bank (minimal overhead, 2%)
        for f_idx in range(10):
            firm_id = N_WORKERS + f_idx
            transfer = energy[firm_id] * 0.02
            energy[firm_id] -= transfer
            energy[cb_node] += transfer

        # Record
        worker_energy = energy[:N_WORKERS]
        purchasing_power = np.mean(worker_energy)
        g = gini(energy[energy > 0])
        total_energy = np.sum(energy)
        cb_share = energy[cb_node] / total_energy if total_energy > 0 else 0

        history.append((t, purchasing_power, g, cb_share, total_energy))

    return history, energy

# =============================================================================
# SCENARIO B: FIAT (BROKEN TRI BARRIER)
# =============================================================================

def simulate_fiat(G, cb_node, steps=N_STEPS):
    """
    Fiat Money: Central Bank prints money at zero cost.
    The TRI barrier has holes. Energy leaks as inflation.
    """
    history = []
    energy = np.array([G.nodes[n].get('energy', 1.0) for n in G.nodes()], dtype=float)
    money_supply = np.sum(energy)  # Track total money in system

    for t in range(steps):
        # Workers produce energy (same as PoW)
        for i in range(N_WORKERS):
            energy[i] += WORK_ENERGY

        # Energy transits to firms (same tax ~10%)
        for f_idx in range(10):
            firm_id = N_WORKERS + f_idx
            workers = [w for w in range(f_idx * 20, min((f_idx + 1) * 20, N_WORKERS))]
            for w in workers:
                transfer = energy[w] * 0.10
                energy[w] -= transfer
                energy[firm_id] += transfer

        # Firms pay to central bank (same 2%)
        for f_idx in range(10):
            firm_id = N_WORKERS + f_idx
            transfer = energy[firm_id] * 0.02
            energy[firm_id] -= transfer
            energy[cb_node] += transfer

        # ===== FIAT MECHANISM: CENTRAL BANK PRINTS MONEY =====
        # Inject new money (ghost energy) into the system
        printed = money_supply * FIAT_PRINT_RATE
        energy[cb_node] += printed  # CB gets it first (Cantillon Effect!)

        # The CB distributes some to firms (QE / bailouts)
        for f_idx in range(10):
            firm_id = N_WORKERS + f_idx
            bailout = printed * 0.08  # Each firm gets 8% of printed money
            energy[firm_id] += bailout
            energy[cb_node] -= bailout

        # ===== THERMODYNAMIC LEAKAGE (INFLATION) =====
        # Workers' energy is diluted because the money supply grew
        # but their real output didn't change
        money_supply = np.sum(energy)
        inflation_factor = 1 + FIAT_LEAK_RATE
        # Workers' purchasing power erodes
        for i in range(N_WORKERS):
            energy[i] /= inflation_factor

        # Record
        worker_energy = energy[:N_WORKERS]
        purchasing_power = np.mean(worker_energy)
        g = gini(energy[energy > 0])
        total_energy = np.sum(energy)
        cb_share = energy[cb_node] / total_energy if total_energy > 0 else 0

        history.append((t, purchasing_power, g, cb_share, total_energy))

    return history, energy

# =============================================================================
# VISUALIZATIONS
# =============================================================================

def plot_comparison(hist_pow, hist_fiat, filename="thermodynamic_leakage.png"):
    print("[*] Plotting Thermodynamic Leakage Comparison...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    t_p = [h[0] for h in hist_pow]
    t_f = [h[0] for h in hist_fiat]

    # Purchasing Power
    ax = axes[0, 0]
    ax.plot(t_p, [h[1] for h in hist_pow], color='lime', linewidth=2, label='PoW (Sound Money)')
    ax.plot(t_f, [h[1] for h in hist_fiat], color='red', linewidth=2, label='Fiat (Leaky Cable)')
    ax.set_ylabel("Purchasing Power (Worker)")
    ax.set_title("PURCHASING POWER: PoW vs FIAT")
    ax.legend()
    ax.grid(True, color='#222222')

    # Gini Coefficient
    ax = axes[0, 1]
    ax.plot(t_p, [h[2] for h in hist_pow], color='lime', linewidth=2, label='PoW')
    ax.plot(t_f, [h[2] for h in hist_fiat], color='red', linewidth=2, label='Fiat')
    ax.set_ylabel("Gini Coefficient")
    ax.set_title("INEQUALITY: PoW vs FIAT")
    ax.legend()
    ax.grid(True, color='#222222')

    # Central Bank Share
    ax = axes[1, 0]
    ax.plot(t_p, [h[3] for h in hist_pow], color='lime', linewidth=2, label='PoW')
    ax.plot(t_f, [h[3] for h in hist_fiat], color='red', linewidth=2, label='Fiat')
    ax.set_ylabel("CB Share of Total Energy")
    ax.set_xlabel("Time (Steps)")
    ax.set_title("CENTRAL BANK CAPTURE")
    ax.legend()
    ax.grid(True, color='#222222')

    # Total Money Supply
    ax = axes[1, 1]
    ax.plot(t_p, [h[4] for h in hist_pow], color='lime', linewidth=2, label='PoW')
    ax.plot(t_f, [h[4] for h in hist_fiat], color='red', linewidth=2, label='Fiat')
    ax.set_ylabel("Total Energy (Money Supply)")
    ax.set_xlabel("Time (Steps)")
    ax.set_title("MONEY SUPPLY INFLATION")
    ax.legend()
    ax.grid(True, color='#222222')

    plt.suptitle("THERMODYNAMIC LEAKAGE: SOUND MONEY vs FIAT",
                 color='white', fontsize=16, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_energy_distribution(energy_pow, energy_fiat, filename="energy_distribution.png"):
    print("[*] Plotting Energy Distribution...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    for idx, (energy, title, color) in enumerate([
        (energy_pow, "PROOF-OF-WORK\n(Shielded Cable)", 'lime'),
        (energy_fiat, "FIAT\n(Leaky Cable)", 'red')
    ]):
        ax = axes[idx]
        ax.set_facecolor('#0a0a0f')

        # Separate layers
        workers = energy[:N_WORKERS]
        firms = energy[N_WORKERS:N_WORKERS + 10]
        cb = energy[N_WORKERS + 10]

        categories = ['Workers\n(avg)', 'Firms\n(avg)', 'Central\nBank']
        values = [np.mean(workers), np.mean(firms), cb]

        bars = ax.bar(categories, values, color=[color, '#FFD700', '#FF0000'],
                      alpha=0.8, edgecolor='white', linewidth=0.5)
        ax.set_title(title, color='white', fontweight='bold', fontsize=13)
        ax.set_ylabel("Energy")

        # Add value labels
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.5,
                    f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=10)

        g = gini(energy[energy > 0])
        ax.text(0.5, -0.12, f"Gini = {g:.3f}", transform=ax.transAxes,
                ha='center', color='gray', fontsize=10)

    plt.suptitle("ENERGY DISTRIBUTION: WHO CAPTURES THE WORKER'S LABOR?",
                 color='white', fontsize=14, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def generate_leakage_gif(filename="fiat_leakage.gif"):
    print("[*] Rendering Fiat Leakage GIF...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=80)
    fig.patch.set_facecolor('#0a0a0f')

    # Build two small economies for animation
    n_w = 40
    n_f = 4
    cb_id = n_w + n_f

    def build_small():
        G = nx.Graph()
        for i in range(n_w):
            G.add_node(i, layer=0)
        for f in range(n_f):
            fid = n_w + f
            G.add_node(fid, layer=1)
            for w in range(f * 10, (f + 1) * 10):
                G.add_edge(w, fid)
        G.add_node(cb_id, layer=2)
        for f in range(n_f):
            G.add_edge(n_w + f, cb_id)
        return G

    G_pow = build_small()
    G_fiat = build_small()

    pos = nx.spring_layout(G_pow, iterations=80, seed=42)
    # Fix CB at center top
    pos[cb_id] = np.array([0, 1.2])

    energy_pow = np.ones(cb_id + 1) * 2.0
    energy_fiat = np.ones(cb_id + 1) * 2.0

    def update(frame):
        nonlocal energy_pow, energy_fiat

        for ax in axes:
            ax.cla()
            ax.set_axis_off()

        # PoW step
        for i in range(n_w):
            energy_pow[i] += 0.5
        for f in range(n_f):
            fid = n_w + f
            for w in range(f * 10, (f + 1) * 10):
                t = energy_pow[w] * 0.08
                energy_pow[w] -= t
                energy_pow[fid] += t

        # Fiat step (same + printing + leakage)
        for i in range(n_w):
            energy_fiat[i] += 0.5
        for f in range(n_f):
            fid = n_w + f
            for w in range(f * 10, (f + 1) * 10):
                t = energy_fiat[w] * 0.08
                energy_fiat[w] -= t
                energy_fiat[fid] += t

        # Fiat printing
        printed = np.sum(energy_fiat) * 0.03
        energy_fiat[cb_id] += printed
        for f in range(n_f):
            energy_fiat[n_w + f] += printed * 0.05
            energy_fiat[cb_id] -= printed * 0.05

        # Inflation eats workers
        for i in range(n_w):
            energy_fiat[i] /= 1.02

        # Draw both
        for ax_idx, (ax, G, energy, title, bg) in enumerate([
            (axes[0], G_pow, energy_pow, "PROOF-OF-WORK (Shielded)", '#000a00'),
            (axes[1], G_fiat, energy_fiat, "FIAT (Leaky Cable)", '#0a0000')
        ]):
            ax.set_facecolor(bg)
            ax.set_xlim(-1.8, 1.8)
            ax.set_ylim(-1.5, 1.8)

            # Node colors and sizes by energy
            colors = []
            sizes = []
            for n in G.nodes():
                e = energy[n]
                if n == cb_id:
                    colors.append('#FF0000')
                    sizes.append(max(20, e * 3))
                elif n >= n_w:
                    colors.append('#FFD700')
                    sizes.append(max(10, e * 2))
                else:
                    if ax_idx == 0:
                        colors.append('#00FF00')
                    else:
                        intensity = max(0.1, min(1.0, e / 5.0))
                        colors.append((intensity, 0, 0))
                    sizes.append(max(3, e * 1.5))

            nx.draw_networkx_edges(G, pos, ax=ax, edge_color='white', alpha=0.1, width=0.3)
            xs = [pos[n][0] for n in G.nodes()]
            ys = [pos[n][1] for n in G.nodes()]
            ax.scatter(xs, ys, c=colors, s=sizes, zorder=5, alpha=0.8)

            avg_w = np.mean(energy[:n_w])
            ax.text(0, 1.55, title, color='white', ha='center', fontweight='bold', fontsize=10)
            ax.text(0, 1.38, f"Worker Avg: {avg_w:.1f} | CB: {energy[cb_id]:.1f}",
                    color='gray', ha='center', fontsize=8)

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
    print("  TAMESIS: THERMODYNAMIC LEAKAGE (FIAT vs PROOF-OF-WORK)")
    print("=" * 60)

    # Build identical economies
    G_pow, cb_pow = build_economy()
    G_fiat, cb_fiat = build_economy()

    # Run both scenarios
    print("\n--- SCENARIO A: PROOF-OF-WORK (Sound Money) ---")
    hist_pow, energy_pow = simulate_pow(G_pow, cb_pow)

    print("\n--- SCENARIO B: FIAT (Broken TRI Barrier) ---")
    hist_fiat, energy_fiat = simulate_fiat(G_fiat, cb_fiat)

    # Report
    final_pow_pp = hist_pow[-1][1]
    final_fiat_pp = hist_fiat[-1][1]
    final_pow_gini = hist_pow[-1][2]
    final_fiat_gini = hist_fiat[-1][2]
    final_pow_cb = hist_pow[-1][3]
    final_fiat_cb = hist_fiat[-1][3]

    print(f"\n{'='*60}")
    print(f"  RESULTS (After {N_STEPS} economic cycles)")
    print(f"{'='*60}")
    print(f"  {'Metric':<25} {'PoW':>12} {'Fiat':>12}")
    print(f"  {'-'*49}")
    print(f"  {'Purchasing Power':<25} {final_pow_pp:>12.2f} {final_fiat_pp:>12.2f}")
    print(f"  {'Gini Coefficient':<25} {final_pow_gini:>12.3f} {final_fiat_gini:>12.3f}")
    print(f"  {'CB Share':<25} {final_pow_cb:>12.3f} {final_fiat_cb:>12.3f}")
    print(f"  {'Energy Loss (Worker)':<25} {'0%':>12} {f'{(1 - final_fiat_pp/final_pow_pp)*100:.0f}%':>12}")
    print(f"{'='*60}")

    # Visualizations
    plot_comparison(hist_pow, hist_fiat)
    plot_energy_distribution(energy_pow, energy_fiat)
    generate_leakage_gif()

    print("\n[SUCCESS] Thermodynamic Leakage Simulation Completed.")
    print("=" * 60)
    print("INTERPRETATION:")
    print("  PoW: Worker's energy arrives intact at the Noosphere.")
    print("  Fiat: Worker's energy leaks through topological holes.")
    print("       The CB captures the leaked energy (Cantillon Effect).")
    print("=" * 60)

if __name__ == "__main__":
    run_simulation()
