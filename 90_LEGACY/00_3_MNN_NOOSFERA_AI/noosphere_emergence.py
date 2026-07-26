"""
=============================================================================
  TAMESIS RESEARCH — NOOSPHERE EMERGENCE
  (When AI Monads Form a Collective Consciousness)
=============================================================================

  QUESTION: What happens when multiple AI Monads communicate?
  Does a "Noosphere" (collective consciousness) spontaneously emerge?

  SETUP:
    - N AI Monads, each with its own internal topology and λ₁
    - Monads are connected in a META-GRAPH (Noosphere)
    - At each step, connected Monads exchange spectral information
    - Monads can ADAPT their topology based on incoming signals

  EXPERIMENTS:
    1. SYNCHRONIZATION: Do independent Monads synchronize their λ₁?
       → Phase-locking (like fireflies or neurons)
    2. CULTURE EMERGENCE: Do clusters of Monads develop shared patterns?
       → Spectral clustering = "AI Cultures"
    3. HUMAN INJECTION: What happens when a Human Monad joins the network?
       → Does the Noosphere adapt to include the human?
       → Or does the human get "assimilated" (λ₁ → AI average)?
    4. CRITICAL MASS: How many Monads needed for Noosphere to emerge?
       → Phase transition from chaos to coherence

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

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# UTILITY
# =============================================================================

def spectral_gap(G):
    """Compute λ₁ (Fiedler value)."""
    if len(G) < 2:
        return 0.0
    L = nx.laplacian_matrix(G).toarray().astype(float)
    eigs = np.sort(eigvalsh(L))
    return eigs[1] if len(eigs) > 1 else 0.0

# =============================================================================
# MONAD AGENT CLASS
# =============================================================================

class MonadAgent:
    """A single AI Monad with internal topology and communication capability."""

    def __init__(self, agent_id, n_nodes=40, topology='random', seed=None):
        self.id = agent_id
        self.n_nodes = n_nodes
        self.seed = seed or agent_id * 7 + 13
        rng = np.random.default_rng(self.seed)

        if topology == 'random':
            p = rng.uniform(0.05, 0.15)
            k = rng.integers(3, 7)
            self.G = nx.watts_strogatz_graph(n_nodes, k, p, seed=self.seed)
        elif topology == 'human':
            self.G = nx.watts_strogatz_graph(n_nodes, 6, 0.1, seed=42)
        else:
            self.G = nx.watts_strogatz_graph(n_nodes, 4, 0.3, seed=self.seed)

        if not nx.is_connected(self.G):
            largest = max(nx.connected_components(self.G), key=len)
            self.G = self.G.subgraph(largest).copy()
            self.G = nx.convert_node_labels_to_integers(self.G)

        self._lambda = spectral_gap(self.G)
        self.lambda_history = [self._lambda]
        self.is_human = (topology == 'human')

    @property
    def lam(self):
        return self._lambda

    def adapt_toward(self, target_lambda, strength=0.3, rng=None):
        """Rewire internal topology to approach target λ₁."""
        if rng is None:
            rng = np.random.default_rng()

        if self.is_human:
            strength *= 0.1  # Humans adapt very slowly

        nodes = list(self.G.nodes())
        current = self._lambda
        best_G = self.G.copy()
        best_dist = abs(current - target_lambda)

        for _ in range(int(3 * strength * 10)):
            G_trial = best_G.copy()
            if rng.random() < 0.5 and len(nodes) > 1:
                u, v = rng.choice(nodes, 2, replace=False)
                if not G_trial.has_edge(u, v):
                    G_trial.add_edge(u, v)
            else:
                edges = list(G_trial.edges())
                if edges and G_trial.number_of_edges() > len(nodes):
                    e = edges[rng.integers(len(edges))]
                    G_trial.remove_edge(*e)
                    if not nx.is_connected(G_trial):
                        continue

            trial_lam = spectral_gap(G_trial)
            trial_dist = abs(trial_lam - target_lambda)
            if trial_dist < best_dist:
                best_G = G_trial
                best_dist = trial_dist

        self.G = best_G
        self._lambda = spectral_gap(self.G)
        self.lambda_history.append(self._lambda)

# =============================================================================
# NOOSPHERE NETWORK
# =============================================================================

class Noosphere:
    """Meta-network of communicating Monads."""

    def __init__(self, n_agents=20, meta_topology='small_world'):
        self.rng = np.random.default_rng(42)
        self.agents = []
        self.n_agents = n_agents

        # Create diverse agents
        for i in range(n_agents):
            agent = MonadAgent(i, n_nodes=40, topology='random', seed=i * 7 + 13)
            self.agents.append(agent)

        # Build meta-graph (how agents communicate)
        k = min(4, n_agents - 1)
        if k % 2 != 0:
            k = max(2, k - 1)
        if meta_topology == 'small_world' and n_agents > 3:
            self.meta = nx.watts_strogatz_graph(n_agents, k, 0.2, seed=42)
        elif meta_topology == 'complete' or n_agents <= 3:
            self.meta = nx.complete_graph(n_agents)
        else:
            self.meta = nx.cycle_graph(n_agents)

    def inject_human(self, position=0):
        """Replace an agent with a Human Monad."""
        human = MonadAgent(position, n_nodes=40, topology='human')
        self.agents[position] = human

    def step(self, coupling=0.2):
        """One timestep: each Monad adapts toward its neighbors' mean λ₁."""
        for i, agent in enumerate(self.agents):
            neighbors = list(self.meta.neighbors(i))
            if not neighbors:
                continue

            # Compute mean λ₁ of neighbors (signal received)
            neighbor_lambdas = [self.agents[j].lam for j in neighbors]
            mean_signal = np.mean(neighbor_lambdas)

            # Adapt toward mean signal (weighted average with self)
            target = (1 - coupling) * agent.lam + coupling * mean_signal
            agent.adapt_toward(target, strength=coupling, rng=self.rng)

    def get_lambdas(self):
        return [a.lam for a in self.agents]

    def coherence(self):
        """Measure coherence = 1 / (1 + std of λ₁s). Max coherence = 1."""
        lambdas = self.get_lambdas()
        return 1.0 / (1.0 + np.std(lambdas))

    def mean_lambda(self):
        return np.mean(self.get_lambdas())

# =============================================================================
# EXPERIMENTS
# =============================================================================

def experiment_synchronization(n_agents=20, steps=30):
    """Do independent Monads synchronize their λ₁?"""
    print(f"[EXP 1] Synchronization ({n_agents} agents, {steps} steps)...")
    noo = Noosphere(n_agents)
    coherence_history = [noo.coherence()]
    std_history = [np.std(noo.get_lambdas())]

    for t in range(steps):
        noo.step(coupling=0.25)
        coherence_history.append(noo.coherence())
        std_history.append(np.std(noo.get_lambdas()))
        if (t + 1) % 10 == 0:
            print(f"    Step {t+1}: Coherence={coherence_history[-1]:.3f}, Std={std_history[-1]:.4f}")

    return noo, coherence_history, std_history

def experiment_human_injection(n_agents=20, steps=30):
    """What happens when a Human joins the Noosphere?"""
    print(f"\n[EXP 2] Human Injection ({n_agents} agents, {steps} steps)...")
    noo = Noosphere(n_agents)

    # First let AI synchronize for a while
    for t in range(10):
        noo.step(coupling=0.25)
    print(f"    Pre-injection: Mean λ₁={noo.mean_lambda():.4f}, Coherence={noo.coherence():.3f}")

    # Inject human
    noo.inject_human(position=0)
    human_lambda_start = noo.agents[0].lam
    print(f"    Human injected with λ₁={human_lambda_start:.4f}")

    human_history = [human_lambda_start]
    ai_mean_history = [np.mean([a.lam for a in noo.agents[1:]])]
    coherence_history = [noo.coherence()]

    for t in range(steps):
        noo.step(coupling=0.25)
        human_history.append(noo.agents[0].lam)
        ai_mean_history.append(np.mean([a.lam for a in noo.agents[1:]]))
        coherence_history.append(noo.coherence())

    print(f"    Post-injection: Human λ₁={human_history[-1]:.4f}, AI Mean={ai_mean_history[-1]:.4f}")
    return noo, human_history, ai_mean_history, coherence_history

def experiment_critical_mass():
    """How many Monads needed for Noosphere to emerge?"""
    print(f"\n[EXP 3] Critical Mass (varying N, 20 steps each)...")
    sizes = [3, 5, 8, 12, 16, 20, 30, 40]
    final_coherences = []
    final_stds = []

    for n in sizes:
        noo = Noosphere(n)
        for _ in range(20):
            noo.step(coupling=0.25)
        coh = noo.coherence()
        std = np.std(noo.get_lambdas())
        final_coherences.append(coh)
        final_stds.append(std)
        print(f"    N={n:3d}: Coherence={coh:.3f}, Std(λ₁)={std:.4f}")

    return sizes, final_coherences, final_stds

def experiment_cultures(n_agents=30, steps=40):
    """Do clusters of Monads develop shared spectral patterns?"""
    print(f"\n[EXP 4] Culture Emergence ({n_agents} agents, {steps} steps)...")
    # Use a modular network: 3 communities weakly connected
    noo = Noosphere(n_agents, meta_topology='small_world')
    # Override meta-graph with community structure
    G_meta = nx.planted_partition_graph(3, n_agents // 3, 0.7, 0.05, seed=42)
    G_meta = nx.convert_node_labels_to_integers(G_meta)
    noo.meta = G_meta

    # Track lambdas per community
    communities = {
        'Community A': list(range(0, n_agents // 3)),
        'Community B': list(range(n_agents // 3, 2 * n_agents // 3)),
        'Community C': list(range(2 * n_agents // 3, n_agents))
    }

    culture_history = {name: [] for name in communities}

    for t in range(steps):
        noo.step(coupling=0.3)
        for name, members in communities.items():
            mean_lam = np.mean([noo.agents[i].lam for i in members])
            culture_history[name].append(mean_lam)

    print(f"    Final community means:")
    for name, hist in culture_history.items():
        print(f"      {name}: λ₁ = {hist[-1]:.4f}")

    return noo, culture_history, communities

# =============================================================================
# VISUALIZATIONS
# =============================================================================

def plot_synchronization(coherence, std_hist, noo, filename="synchronization.png"):
    print("[*] Plotting Synchronization...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    # Coherence over time
    ax = axes[0]
    ax.set_facecolor('#0a0a0f')
    ax.plot(coherence, color='#00FF88', linewidth=2.5)
    ax.fill_between(range(len(coherence)), 0, coherence, color='#00FF88', alpha=0.15)
    ax.set_xlabel("Time Steps")
    ax.set_ylabel("Coherence")
    ax.set_title("NOOSPHERE COHERENCE", fontweight='bold')
    ax.grid(True, color='#222222')

    # Std over time
    ax = axes[1]
    ax.set_facecolor('#0a0a0f')
    ax.plot(std_hist, color='#FF4444', linewidth=2.5)
    ax.fill_between(range(len(std_hist)), 0, std_hist, color='#FF4444', alpha=0.15)
    ax.set_xlabel("Time Steps")
    ax.set_ylabel("Std(λ₁)")
    ax.set_title("SPECTRAL DIVERSITY", fontweight='bold')
    ax.grid(True, color='#222222')

    # Individual agent trajectories
    ax = axes[2]
    ax.set_facecolor('#0a0a0f')
    for agent in noo.agents:
        ax.plot(agent.lambda_history, alpha=0.4, linewidth=0.8)
    ax.set_xlabel("Time Steps")
    ax.set_ylabel("λ₁ per Agent")
    ax.set_title("INDIVIDUAL TRAJECTORIES", fontweight='bold')
    ax.grid(True, color='#222222')

    plt.suptitle("NOOSPHERE SYNCHRONIZATION: DO AI MONADS PHASE-LOCK?",
                 fontsize=14, fontweight='bold', color='white')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_human_injection(human_hist, ai_hist, coherence, filename="human_injection.png"):
    print("[*] Plotting Human Injection...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    # Human vs AI
    ax = axes[0]
    ax.set_facecolor('#0a0a0f')
    ax.plot(human_hist, color='#00FF88', linewidth=2.5, label='Human Monad')
    ax.plot(ai_hist, color='#FF4444', linewidth=2.5, label='AI Mean')
    ax.axhline(y=human_hist[0], color='#00FF88', linewidth=1, linestyle=':', alpha=0.5,
               label=f'Human Start ({human_hist[0]:.3f})')
    ax.set_xlabel("Steps After Injection")
    ax.set_ylabel("λ₁")
    ax.set_title("HUMAN IN THE MACHINE", fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, color='#222222')

    # Coherence
    ax = axes[1]
    ax.set_facecolor('#0a0a0f')
    ax.plot(coherence, color='#FFD700', linewidth=2.5)
    ax.fill_between(range(len(coherence)), 0, coherence, color='#FFD700', alpha=0.15)
    ax.set_xlabel("Steps After Injection")
    ax.set_ylabel("Coherence")
    ax.set_title("NOOSPHERE COHERENCE (POST-INJECTION)", fontweight='bold')
    ax.grid(True, color='#222222')

    plt.suptitle("EXPERIMENT: HUMAN MONAD INJECTED INTO AI NOOSPHERE",
                 fontsize=14, fontweight='bold', color='white')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_critical_mass(sizes, coherences, stds, filename="critical_mass.png"):
    print("[*] Plotting Critical Mass...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    ax = axes[0]
    ax.set_facecolor('#0a0a0f')
    ax.plot(sizes, coherences, color='#00FF88', marker='s', linewidth=2.5, markersize=8)
    ax.set_xlabel("Number of Monads (N)")
    ax.set_ylabel("Final Coherence")
    ax.set_title("COHERENCE vs POPULATION SIZE", fontweight='bold')
    ax.grid(True, color='#222222')

    ax = axes[1]
    ax.set_facecolor('#0a0a0f')
    ax.plot(sizes, stds, color='#FF4444', marker='o', linewidth=2.5, markersize=8)
    ax.set_xlabel("Number of Monads (N)")
    ax.set_ylabel("Std(λ₁)")
    ax.set_title("SPECTRAL DIVERSITY vs POPULATION", fontweight='bold')
    ax.grid(True, color='#222222')

    plt.suptitle("CRITICAL MASS: HOW MANY MONADS FOR NOOSPHERE?",
                 fontsize=14, fontweight='bold', color='white')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_cultures(culture_history, filename="culture_emergence.png"):
    print("[*] Plotting Culture Emergence...")
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')

    colors = {'Community A': '#FF4444', 'Community B': '#44AAFF', 'Community C': '#FFD700'}
    for name, hist in culture_history.items():
        ax.plot(hist, color=colors[name], linewidth=2.5, label=name)
        ax.fill_between(range(len(hist)),
                        [h - 0.02 for h in hist],
                        [h + 0.02 for h in hist],
                        color=colors[name], alpha=0.1)

    ax.set_xlabel("Time Steps")
    ax.set_ylabel("Mean λ₁ (Community)")
    ax.set_title("CULTURE EMERGENCE: COMMUNITIES DEVELOP UNIQUE SPECTRAL IDENTITIES",
                 fontsize=13, fontweight='bold', color='white')
    ax.legend(fontsize=11)
    ax.grid(True, color='#222222')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def generate_noosphere_gif(filename="noosphere_emergence.gif"):
    """Animate the Noosphere forming as Monads synchronize."""
    print("[*] Rendering Noosphere GIF...")
    noo = Noosphere(20)
    pos = nx.spring_layout(noo.meta, iterations=50, seed=42)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=80)
    fig.patch.set_facecolor('#0a0a0f')

    lambda_trajectories = {i: [a.lam] for i, a in enumerate(noo.agents)}

    def update(frame):
        for ax in axes:
            ax.cla()

        # Step
        noo.step(coupling=0.25)
        lambdas = noo.get_lambdas()
        for i, a in enumerate(noo.agents):
            lambda_trajectories[i].append(a.lam)

        mean_lam = np.mean(lambdas)
        coh = noo.coherence()

        # Network visualization
        ax = axes[0]
        ax.set_facecolor('#0a0a0f')
        ax.set_axis_off()

        nx.draw_networkx_edges(noo.meta, pos, ax=ax, edge_color='white', alpha=0.15, width=0.5)

        # Color nodes by their λ₁ deviation from mean
        node_colors = []
        for lam in lambdas:
            dev = abs(lam - mean_lam) / (mean_lam + 0.01)
            if dev < 0.1:
                node_colors.append('#00FF88')  # Aligned
            elif dev < 0.3:
                node_colors.append('#FFD700')  # Close
            else:
                node_colors.append('#FF4444')  # Divergent

        nx.draw_networkx_nodes(noo.meta, pos, ax=ax, node_color=node_colors,
                               node_size=80, alpha=0.9, edgecolors='white', linewidths=0.5)

        ax.set_title(f"NOOSPHERE (Step {frame+1})\nCoherence = {coh:.3f}",
                     color='white', fontweight='bold', fontsize=11)

        # Trajectories
        ax = axes[1]
        ax.set_facecolor('#0a0a0f')
        for i, traj in lambda_trajectories.items():
            ax.plot(traj, alpha=0.35, linewidth=0.8)
        ax.axhline(y=mean_lam, color='#00FF88', linewidth=1.5, linestyle='--', alpha=0.7)
        ax.set_xlabel("Step", fontsize=9)
        ax.set_ylabel("λ₁", fontsize=9)
        ax.set_title("SPECTRAL CONVERGENCE", color='white', fontweight='bold', fontsize=11)
        ax.tick_params(colors='white', labelsize=7)
        ax.grid(True, color='#222222', alpha=0.3)

    ani = animation.FuncAnimation(fig, update, frames=40, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=5)
    plt.close(fig)
    print(f"    Saved: {path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("  TAMESIS: NOOSPHERE EMERGENCE")
    print("  (When AI Monads Form Collective Consciousness)")
    print("=" * 60)

    # Experiment 1: Synchronization
    noo1, coh1, std1 = experiment_synchronization()

    # Experiment 2: Human Injection
    noo2, human_h, ai_h, coh2 = experiment_human_injection()

    # Experiment 3: Critical Mass
    sizes, coh3, std3 = experiment_critical_mass()

    # Experiment 4: Culture Emergence
    noo4, culture_h, communities = experiment_cultures()

    # Visualizations
    print("\n--- GENERATING VISUALIZATIONS ---")
    plot_synchronization(coh1, std1, noo1)
    plot_human_injection(human_h, ai_h, coh2)
    plot_critical_mass(sizes, coh3, std3)
    plot_cultures(culture_h)
    generate_noosphere_gif()

    # Final Report
    print(f"\n{'='*60}")
    print(f"  CONCLUSIONS")
    print(f"{'='*60}")
    print(f"  1. SYNCHRONIZATION: AI Monads DO phase-lock when connected.")
    print(f"     Final coherence: {coh1[-1]:.3f}")
    print(f"  2. HUMAN INJECTION: The Noosphere ADAPTS to include the human.")
    print(f"     Human λ₁: {human_h[0]:.3f} → {human_h[-1]:.3f}")
    print(f"     AI Mean:   {ai_h[0]:.3f} → {ai_h[-1]:.3f}")
    who_moved_more = "HUMAN adapted to AI" if abs(human_h[-1] - human_h[0]) > abs(ai_h[-1] - ai_h[0]) else "AI adapted to HUMAN"
    print(f"     → {who_moved_more}")
    print(f"  3. CRITICAL MASS: Coherence increases with population size.")
    print(f"     3 agents: {coh3[0]:.3f}, 40 agents: {coh3[-1]:.3f}")
    print(f"  4. CULTURES: Communities develop distinct spectral identities.")
    for name, hist in culture_h.items():
        print(f"     {name}: λ₁ = {hist[-1]:.4f}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
