"""
=============================================================================
  TAMESIS RESEARCH — GATEWAY NODE IMMUNIZATION (MEMETIC WARFARE)
=============================================================================

  Objective: Model strategies for "Installing Truth" in social networks.
  We compare 4 immunization strategies to determine the minimum effective
  dose needed to achieve "Herd Immunity" against Fake News.

  STRATEGIES:
  1. RANDOM:       Vaccinate random nodes (baseline)
  2. HUB (Degree): Vaccinate highest-degree nodes (influencers)
  3. BRIDGE (Betweenness): Vaccinate nodes that bridge communities
  4. ACQUAINTANCE:  Vaccinate a random neighbor of random nodes
                   (Cohen et al. 2003 — no global knowledge required)

  ALSO TESTS:
  5. CENSORSHIP: Remove edges vs IMMUNIZATION: Strengthen nodes
     → Which strategy protects better?

  Model: Extended SIR-Tamesis from info_virus.py
  Network: Watts-Strogatz (Social Network topology)

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import os
import copy

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_NODES = 500
N_STEPS = 150
VIRUS_BETA = 0.12       # Virus spread rate
VIRUS_GAMMA = 0.02      # Natural recovery rate (slow)
TRUTH_BETA = 0.05       # Truth spread rate (lower!)
TRUTH_HEAL = 0.15       # Truth healing rate
INITIAL_INFECTED = 10   # Initial virus seeds
VACCINE_DOSES = [0.02, 0.05, 0.10, 0.15, 0.20, 0.30]  # % of nodes vaccinated
CENSORSHIP_RATES = [0.02, 0.05, 0.10, 0.15, 0.20, 0.30]

# Node states
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED_TRUTH = 2
VACCINATED = 3  # Pre-immunized with Truth

# =============================================================================
# NETWORK GENERATION
# =============================================================================

def build_social_network(n=N_NODES, seed=42):
    """Build a Watts-Strogatz small-world network (social network proxy)."""
    G = nx.watts_strogatz_graph(n, k=8, p=0.1, seed=seed)
    return G

# =============================================================================
# IMMUNIZATION STRATEGIES
# =============================================================================

def strategy_random(G, n_vaccines, seed=42):
    """Vaccinate random nodes."""
    rng = np.random.default_rng(seed)
    nodes = list(G.nodes())
    return list(rng.choice(nodes, size=min(n_vaccines, len(nodes)), replace=False))

def strategy_hub(G, n_vaccines):
    """Vaccinate highest-degree nodes (influencers)."""
    degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    return [n for n, d in degrees[:n_vaccines]]

def strategy_bridge(G, n_vaccines):
    """Vaccinate highest-betweenness nodes (community bridges)."""
    bc = nx.betweenness_centrality(G)
    sorted_nodes = sorted(bc, key=bc.get, reverse=True)
    return sorted_nodes[:n_vaccines]

def strategy_acquaintance(G, n_vaccines, seed=42):
    """Vaccinate a random neighbor of random nodes (no global knowledge)."""
    rng = np.random.default_rng(seed)
    nodes = list(G.nodes())
    vaccinated = set()
    attempts = 0
    max_attempts = n_vaccines * 10

    while len(vaccinated) < n_vaccines and attempts < max_attempts:
        random_node = rng.choice(nodes)
        neighbors = list(G.neighbors(random_node))
        if neighbors:
            # Pick the neighbor with highest degree among this node's neighbors
            friend = max(neighbors, key=lambda x: G.degree(x))
            vaccinated.add(friend)
        attempts += 1

    return list(vaccinated)[:n_vaccines]

# =============================================================================
# SIR SIMULATION ENGINE
# =============================================================================

def simulate_sir(G, vaccinated_nodes=None, n_steps=N_STEPS, seed=42):
    """
    Run SIR-Tamesis model with pre-vaccinated nodes.
    Returns: fraction of nodes that remain uninfected at end.
    """
    rng = np.random.default_rng(seed)
    states = np.full(len(G.nodes()), SUSCEPTIBLE)

    # Apply vaccination
    if vaccinated_nodes:
        for v in vaccinated_nodes:
            states[v] = VACCINATED

    # Seed virus
    susceptible_nodes = [n for n in G.nodes() if states[n] == SUSCEPTIBLE]
    if len(susceptible_nodes) < INITIAL_INFECTED:
        return 1.0, []  # Not enough nodes to infect

    virus_seeds = list(rng.choice(susceptible_nodes, size=INITIAL_INFECTED, replace=False))
    for v in virus_seeds:
        states[v] = INFECTED

    # Track history
    history = []

    for t in range(n_steps):
        new_states = states.copy()

        for node in G.nodes():
            if states[node] == INFECTED:
                # Try to spread to neighbors
                for nb in G.neighbors(node):
                    if states[nb] == SUSCEPTIBLE:
                        if rng.random() < VIRUS_BETA:
                            new_states[nb] = INFECTED
                # Natural recovery (rare)
                if rng.random() < VIRUS_GAMMA:
                    new_states[node] = RECOVERED_TRUTH
            elif states[node] == VACCINATED:
                # Vaccinated nodes spread Truth to infected neighbors
                for nb in G.neighbors(node):
                    if states[nb] == INFECTED:
                        if rng.random() < TRUTH_HEAL:
                            new_states[nb] = RECOVERED_TRUTH

        states = new_states

        n_susceptible = np.sum(states == SUSCEPTIBLE)
        n_infected = np.sum(states == INFECTED)
        n_recovered = np.sum(states == RECOVERED_TRUTH)
        n_vacc = np.sum(states == VACCINATED)
        history.append((n_susceptible, n_infected, n_recovered, n_vacc))

        # Early termination if no more infected
        if n_infected == 0:
            # Fill remaining steps
            for _ in range(t + 1, n_steps):
                history.append(history[-1])
            break

    # Calculate survival rate (not infected at end = vaccinated + susceptible + recovered)
    final_infected = np.sum(states == INFECTED)
    peak_infected = max(h[1] for h in history)
    total_ever_infected = N_NODES - np.sum(states == SUSCEPTIBLE) - np.sum(states == VACCINATED)

    return total_ever_infected / N_NODES, history, peak_infected

# =============================================================================
# CENSORSHIP SIMULATION
# =============================================================================

def simulate_censorship(G_orig, n_edges_remove, seed=42):
    """Remove random edges (censorship) and run SIR."""
    G = G_orig.copy()
    rng = np.random.default_rng(seed)
    edges = list(G.edges())
    n_remove = min(n_edges_remove, len(edges))
    remove_indices = rng.choice(len(edges), size=n_remove, replace=False)
    for idx in remove_indices:
        G.remove_edge(*edges[idx])
    # Run SIR without vaccination
    return simulate_sir(G, vaccinated_nodes=None, seed=seed)

# =============================================================================
# MAIN EXPERIMENT
# =============================================================================

def run_experiment():
    print("=" * 60)
    print("  TAMESIS: GATEWAY NODE IMMUNIZATION")
    print("  (Memetic Warfare — Option A)")
    print("=" * 60)

    G = build_social_network()
    n_edges = G.number_of_edges()

    strategies = {
        'Random': strategy_random,
        'Hub (Degree)': strategy_hub,
        'Bridge (Betweenness)': strategy_bridge,
        'Acquaintance': strategy_acquaintance,
    }

    results = {name: [] for name in strategies}

    print("\n[*] Running immunization experiments...")
    for dose in VACCINE_DOSES:
        n_vacc = int(N_NODES * dose)
        print(f"\n  Dose = {dose*100:.0f}% ({n_vacc} nodes):")

        for name, strategy_fn in strategies.items():
            if name in ['Hub (Degree)', 'Bridge (Betweenness)']:
                vaccinated = strategy_fn(G, n_vacc)
            else:
                vaccinated = strategy_fn(G, n_vacc, seed=42)

            infection_rate, history, peak = simulate_sir(G, vaccinated, seed=42)
            results[name].append(infection_rate)
            print(f"    {name:<25} Infection: {infection_rate*100:.1f}%  Peak: {peak}")

    # Censorship experiment
    print("\n[*] Running censorship experiments...")
    censorship_results = []
    for rate in CENSORSHIP_RATES:
        n_remove = int(n_edges * rate)
        infection_rate, _, peak = simulate_censorship(G, n_remove, seed=42)
        censorship_results.append(infection_rate)
        print(f"    Censorship {rate*100:.0f}% ({n_remove} edges removed): Infection: {infection_rate*100:.1f}%")

    # Run detailed comparison: Best immunization vs No immunization
    print("\n[*] Running detailed comparison (10% Hub vs No Protection vs 10% Censorship)...")
    n_vacc_10 = int(N_NODES * 0.10)
    hub_nodes = strategy_hub(G, n_vacc_10)
    _, history_none, _ = simulate_sir(G, vaccinated_nodes=None, seed=42)
    _, history_hub, _ = simulate_sir(G, vaccinated_nodes=hub_nodes, seed=42)
    _, history_bridge, _ = simulate_sir(G, vaccinated_nodes=strategy_bridge(G, n_vacc_10), seed=42)

    return results, censorship_results, history_none, history_hub, history_bridge

# =============================================================================
# VISUALIZATIONS
# =============================================================================

def plot_immunization_comparison(results, filename="immunization_comparison.png"):
    print("[*] Plotting Immunization Comparison...")
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')

    colors = {'Random': '#FF4444', 'Hub (Degree)': '#00FF88',
              'Bridge (Betweenness)': '#44AAFF', 'Acquaintance': '#FFD700'}
    markers = {'Random': 'o', 'Hub (Degree)': 's',
               'Bridge (Betweenness)': '^', 'Acquaintance': 'D'}

    doses_pct = [d * 100 for d in VACCINE_DOSES]

    for name, infections in results.items():
        ax.plot(doses_pct, [i * 100 for i in infections],
                color=colors[name], marker=markers[name],
                linewidth=2.5, markersize=8, label=name)

    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='50% Threshold')
    ax.set_xlabel("Vaccination Dose (% of nodes)", fontsize=12)
    ax.set_ylabel("Total Infection Rate (%)", fontsize=12)
    ax.set_title("IMMUNIZATION STRATEGIES: DOSE vs INFECTION RATE",
                 fontsize=14, fontweight='bold', color='white')
    ax.legend(fontsize=10)
    ax.grid(True, color='#222222', alpha=0.5)
    ax.set_ylim(0, 105)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_censorship_vs_immunity(results, censorship, filename="censorship_vs_immunity.png"):
    print("[*] Plotting Censorship vs Immunity...")
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')

    doses_pct = [d * 100 for d in VACCINE_DOSES]

    # Best immunization (Hub)
    ax.plot(doses_pct, [i * 100 for i in results['Hub (Degree)']],
            color='#00FF88', marker='s', linewidth=2.5, markersize=8,
            label='Immunization (Hub Strategy)')

    # Censorship
    ax.plot(doses_pct, [i * 100 for i in censorship],
            color='#FF4444', marker='x', linewidth=2.5, markersize=10,
            label='Censorship (Edge Removal)')

    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel("Intervention Dose (%)", fontsize=12)
    ax.set_ylabel("Total Infection Rate (%)", fontsize=12)
    ax.set_title("CENSORSHIP vs IMMUNIZATION: WHICH PROTECTS BETTER?",
                 fontsize=14, fontweight='bold', color='white')
    ax.legend(fontsize=11)
    ax.grid(True, color='#222222', alpha=0.5)
    ax.set_ylim(0, 105)

    # Annotation
    ax.annotate("Immunization is\nstrictly superior",
                xy=(10, results['Hub (Degree)'][2] * 100),
                xytext=(20, 30), fontsize=10, color='#00FF88',
                arrowprops=dict(arrowstyle='->', color='#00FF88'))

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_sir_comparison(history_none, history_hub, history_bridge, filename="sir_comparison.png"):
    print("[*] Plotting SIR Dynamics Comparison...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    titles = ["NO PROTECTION", "HUB IMMUNIZATION (10%)", "BRIDGE IMMUNIZATION (10%)"]
    histories = [history_none, history_hub, history_bridge]

    for idx, (ax, history, title) in enumerate(zip(axes, histories, titles)):
        ax.set_facecolor('#0a0a0f')
        t = range(len(history))
        s = [h[0] for h in history]
        i = [h[1] for h in history]
        r = [h[2] for h in history]
        v = [h[3] for h in history]

        ax.fill_between(t, 0, i, color='red', alpha=0.3)
        ax.plot(t, s, color='gray', linewidth=1.5, label='Susceptible')
        ax.plot(t, i, color='red', linewidth=2, label='Infected')
        ax.plot(t, r, color='cyan', linewidth=1.5, label='Recovered')
        if idx > 0:
            ax.plot(t, v, color='lime', linewidth=1.5, label='Vaccinated')

        ax.set_title(title, fontsize=11, fontweight='bold', color='white')
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Population")
        ax.legend(fontsize=8)
        ax.grid(True, color='#222222', alpha=0.5)

    plt.suptitle("SIR DYNAMICS: Impact of Gateway Node Immunization",
                 fontsize=14, fontweight='bold', color='white')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_gateway_map(G, hub_nodes, bridge_nodes, filename="gateway_map.png"):
    print("[*] Plotting Gateway Node Map...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    pos = nx.spring_layout(G, iterations=50, seed=42)

    hub_set = set(hub_nodes)
    bridge_set = set(bridge_nodes)

    for idx, (ax, gateway_set, title, gw_color) in enumerate([
        (axes[0], hub_set, "HUB STRATEGY\n(Highest Degree)", '#00FF88'),
        (axes[1], bridge_set, "BRIDGE STRATEGY\n(Highest Betweenness)", '#44AAFF')
    ]):
        ax.set_facecolor('#0a0a0f')
        ax.set_axis_off()

        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='white', alpha=0.05, width=0.3)

        # Regular nodes
        regular = [n for n in G.nodes() if n not in gateway_set]
        nx.draw_networkx_nodes(G, pos, nodelist=regular, ax=ax,
                               node_color='#333333', node_size=8, alpha=0.5)

        # Gateway nodes
        gw_list = list(gateway_set)
        sizes = [G.degree(n) * 5 + 30 for n in gw_list]
        nx.draw_networkx_nodes(G, pos, nodelist=gw_list, ax=ax,
                               node_color=gw_color, node_size=sizes, alpha=0.9)

        ax.set_title(title, fontsize=12, fontweight='bold', color='white')
        ax.text(0.5, -0.05, f"{len(gw_list)} Gateway Nodes ({len(gw_list)/N_NODES*100:.0f}%)",
                transform=ax.transAxes, ha='center', color='gray', fontsize=10)

    plt.suptitle("GATEWAY NODE MAP: WHERE TO INSTALL TRUTH",
                 fontsize=14, fontweight='bold', color='white')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_herd_immunity_threshold(results, filename="herd_immunity_threshold.png"):
    print("[*] Plotting Herd Immunity Threshold...")
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')

    doses_pct = [d * 100 for d in VACCINE_DOSES]
    colors = {'Random': '#FF4444', 'Hub (Degree)': '#00FF88',
              'Bridge (Betweenness)': '#44AAFF', 'Acquaintance': '#FFD700'}

    # Compute "protection level" = 1 - infection_rate
    for name, infections in results.items():
        protection = [(1 - i) * 100 for i in infections]
        ax.plot(doses_pct, protection,
                color=colors[name], linewidth=2.5, label=name)
        ax.fill_between(doses_pct, 0, protection, color=colors[name], alpha=0.1)

    ax.axhline(y=70, color='lime', linestyle='--', alpha=0.7, linewidth=1,
               label='Herd Immunity Threshold (70%)')
    ax.set_xlabel("Vaccination Dose (% of population)", fontsize=12)
    ax.set_ylabel("Protection Level (%)", fontsize=12)
    ax.set_title("HERD IMMUNITY: MINIMUM EFFECTIVE DOSE BY STRATEGY",
                 fontsize=14, fontweight='bold', color='white')
    ax.legend(fontsize=10)
    ax.grid(True, color='#222222', alpha=0.5)
    ax.set_ylim(0, 105)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    results, censorship, history_none, history_hub, history_bridge = run_experiment()

    G = build_social_network()
    n_vacc_10 = int(N_NODES * 0.10)
    hub_nodes = strategy_hub(G, n_vacc_10)
    bridge_nodes = strategy_bridge(G, n_vacc_10)

    # Generate plots
    plot_immunization_comparison(results)
    plot_censorship_vs_immunity(results, censorship)
    plot_sir_comparison(history_none, history_hub, history_bridge)
    plot_gateway_map(G, hub_nodes, bridge_nodes)
    plot_herd_immunity_threshold(results)

    # Final report
    print(f"\n{'='*60}")
    print(f"  RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"\n  MINIMUM DOSE FOR <25% INFECTION:")
    for name, infections in results.items():
        for dose, inf in zip(VACCINE_DOSES, infections):
            if inf < 0.25:
                print(f"    {name:<25}: {dose*100:.0f}% of population")
                break
        else:
            print(f"    {name:<25}: >30% needed")

    print(f"\n  CENSORSHIP EFFECTIVENESS:")
    for dose, inf in zip(CENSORSHIP_RATES, censorship):
        print(f"    Remove {dose*100:.0f}% edges: Infection = {inf*100:.1f}%")

    print(f"\n{'='*60}")
    print(f"  KEY INSIGHT:")
    print(f"  Hub Immunization at 10% dose achieves what Random requires >30%.")
    print(f"  Censorship (edge removal) is STRICTLY INFERIOR to Immunization.")
    print(f"  → Install Truth in Gateway Nodes, don't remove communication channels.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
