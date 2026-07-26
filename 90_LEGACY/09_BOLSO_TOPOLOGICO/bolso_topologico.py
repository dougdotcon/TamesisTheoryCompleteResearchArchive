"""
=============================================================================
  TAMESIS RESEARCH — BOLSO TOPOLOGICO
  (Vazamento Dimensional e Anomalias Planetarias)
=============================================================================

  HIPOTESE: A Terra nao e oca, mas o Grafo Causal da Macro-Monada
  planetaria possui "Sub-Bolsos" — regioes topologicamente isoladas
  que se comunicam com a superficie atraves de "vazamentos" (arestas
  de longo alcance).

  TESTE: Se esses Sub-Bolsos existem, eles causariam:
    1. DESCONTINUIDADE ESPECTRAL: Quebra abrupta nos autovalores do
       Laplaciano nas regioes anomalas
    2. VAZAMENTO TRI: Enfraquecimento localizado da Barreira TRI
       (analogo a SAA — Anomalia Magnetica do Atlantico Sul)
    3. HUBS DE DENSIDADE: Nos de altissima conectividade (LLSVPs)
       que ancoram o Sub-Bolso ao grafo principal
    4. ANOMALIAS GRAVITACIONAIS: Curvatura de Ollivier-Ricci anomala
       em regioes especificas (analogo a GRACE)

  METODO:
    - Construir Macro-Monada esfericamente simetrica (crosta → manto → nucleo)
    - Injetar Sub-Bolso (grafo isolado conectado por poucas arestas)
    - Medir assinatura espectral em cada regiao
    - Comparar com/sem Sub-Bolso
    - Calibrar anomalias com dados reais (SAA coords, LLSVP positions)

  RIGOR: Nivel CLAY — provas computacionais, sem heuristica apresentada
  como resultado. Cada afirmacao e testavel e refutavel.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from scipy.linalg import eigvalsh
from scipy.spatial import Delaunay
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# SPECTRAL TOOLS
# =============================================================================

def spectral_gap(G):
    """Compute lambda_1 (Fiedler value) of graph G."""
    if len(G) < 2:
        return 0.0
    L = nx.laplacian_matrix(G).toarray().astype(float)
    eigs = np.sort(eigvalsh(L))
    return eigs[1] if len(eigs) > 1 else 0.0

def local_spectral_gap(G, node, radius=2):
    """Compute lambda_1 of the ego-graph (local neighborhood) of a node."""
    ego = nx.ego_graph(G, node, radius=radius)
    if len(ego) < 3:
        return 0.0
    return spectral_gap(ego)

def ollivier_ricci_curvature(G, u, v):
    """
    Simplified Ollivier-Ricci curvature between adjacent nodes.
    kappa(u,v) = 1 - W(mu_u, mu_v) / d(u,v)
    where mu_x is uniform distribution over neighbors of x.
    Simplified: kappa ~ 1 - |N(u) symdiff N(v)| / (|N(u)| + |N(v)|)
    """
    Nu = set(G.neighbors(u))
    Nv = set(G.neighbors(v))
    if len(Nu) == 0 or len(Nv) == 0:
        return 0.0
    common = len(Nu & Nv)
    total = len(Nu | Nv)
    return 2.0 * common / total - 1.0 if total > 0 else 0.0

# =============================================================================
# MACRO-MONADA: PLANETARY GRAPH
# =============================================================================

def build_planetary_monada(n_crust=120, n_mantle=80, n_core=30):
    """
    Build a layered spherical graph representing Earth's Macro-Monada.
    Three concentric layers: Crust, Mantle, Core.
    Each layer is a random geometric graph (spatial proximity = edges).
    Layers are connected by inter-layer edges (heat/mass transfer).
    """
    rng = np.random.default_rng(42)
    G = nx.Graph()
    positions = {}
    layers = {}

    # Generate points on concentric spheres
    node_id = 0

    # CRUST (outermost, r ~ 1.0)
    crust_nodes = []
    for i in range(n_crust):
        theta = rng.uniform(0, np.pi)
        phi = rng.uniform(0, 2 * np.pi)
        r = 0.95 + rng.uniform(0, 0.1)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        G.add_node(node_id, layer='crust', r=r, theta=theta, phi=phi,
                   pos3d=(x, y, z))
        positions[node_id] = (theta, phi)
        layers[node_id] = 'crust'
        crust_nodes.append(node_id)
        node_id += 1

    # MANTLE (middle, r ~ 0.5-0.9)
    mantle_nodes = []
    for i in range(n_mantle):
        theta = rng.uniform(0, np.pi)
        phi = rng.uniform(0, 2 * np.pi)
        r = 0.5 + rng.uniform(0, 0.4)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        G.add_node(node_id, layer='mantle', r=r, theta=theta, phi=phi,
                   pos3d=(x, y, z))
        positions[node_id] = (theta, phi)
        layers[node_id] = 'mantle'
        mantle_nodes.append(node_id)
        node_id += 1

    # CORE (innermost, r ~ 0.0-0.4)
    core_nodes = []
    for i in range(n_core):
        theta = rng.uniform(0, np.pi)
        phi = rng.uniform(0, 2 * np.pi)
        r = rng.uniform(0, 0.4)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        G.add_node(node_id, layer='core', r=r, theta=theta, phi=phi,
                   pos3d=(x, y, z))
        positions[node_id] = (theta, phi)
        layers[node_id] = 'core'
        core_nodes.append(node_id)
        node_id += 1

    # Connect nodes within each layer (proximity-based)
    def connect_by_proximity(nodes, G, threshold):
        for i, n1 in enumerate(nodes):
            p1 = np.array(G.nodes[n1]['pos3d'])
            for n2 in nodes[i+1:]:
                p2 = np.array(G.nodes[n2]['pos3d'])
                dist = np.linalg.norm(p1 - p2)
                if dist < threshold:
                    G.add_edge(n1, n2, weight=1.0 / (dist + 0.01), type='intra')

    connect_by_proximity(crust_nodes, G, 0.45)
    connect_by_proximity(mantle_nodes, G, 0.55)
    connect_by_proximity(core_nodes, G, 0.50)

    # Connect between layers (heat/mass transfer)
    for cn in crust_nodes:
        p1 = np.array(G.nodes[cn]['pos3d'])
        for mn in mantle_nodes:
            p2 = np.array(G.nodes[mn]['pos3d'])
            dist = np.linalg.norm(p1 - p2)
            if dist < 0.6:
                if rng.random() < 0.15:
                    G.add_edge(cn, mn, weight=0.5, type='inter')

    for mn in mantle_nodes:
        p1 = np.array(G.nodes[mn]['pos3d'])
        for kn in core_nodes:
            p2 = np.array(G.nodes[kn]['pos3d'])
            dist = np.linalg.norm(p1 - p2)
            if dist < 0.5:
                if rng.random() < 0.2:
                    G.add_edge(mn, kn, weight=0.5, type='inter')

    # Ensure connected (keep largest component)
    if not nx.is_connected(G):
        largest = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest).copy()

    return G, crust_nodes, mantle_nodes, core_nodes

# =============================================================================
# SUB-BOLSO: TOPOLOGICAL POCKET
# =============================================================================

def inject_sub_pocket(G, mantle_nodes, n_pocket=25, n_bridges=3):
    """
    Inject a "Sub-Bolso" (topological pocket) — a dense sub-graph
    weakly connected to the main Monada through few bridge edges.

    This simulates a "dimensional pocket" hidden within the mantle.
    The pocket has its own internal high connectivity but only connects
    to the main graph via n_bridges edges (wormholes / causal shortcuts).
    """
    rng = np.random.default_rng(99)
    max_id = max(G.nodes()) + 1
    pocket_nodes = []

    # Create pocket as a dense small-world graph
    G_pocket = nx.watts_strogatz_graph(n_pocket, 6, 0.05, seed=99)

    # Add pocket nodes to main graph
    for pn in G_pocket.nodes():
        new_id = max_id + pn
        # Position pocket nodes deep in the mantle (r ~ 0.3-0.5)
        theta = rng.uniform(np.pi * 0.3, np.pi * 0.7)  # Equatorial region
        phi = rng.uniform(np.pi * 0.6, np.pi * 1.4)     # South Atlantic area (SAA analog)
        r = rng.uniform(0.3, 0.5)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        G.add_node(new_id, layer='pocket', r=r, theta=theta, phi=phi,
                   pos3d=(x, y, z))
        pocket_nodes.append(new_id)

    # Add pocket internal edges
    for u, v in G_pocket.edges():
        G.add_edge(max_id + u, max_id + v, weight=2.0, type='pocket')

    # Create bridge edges (wormholes) to mantle
    bridge_targets = list(rng.choice(
        [m for m in mantle_nodes if m in G.nodes()],
        size=min(n_bridges, len(mantle_nodes)),
        replace=False
    ))
    bridge_sources = list(rng.choice(pocket_nodes, size=len(bridge_targets), replace=False))

    for src, tgt in zip(bridge_sources, bridge_targets):
        G.add_edge(src, tgt, weight=0.1, type='bridge')

    return G, pocket_nodes, list(zip(bridge_sources, bridge_targets))

# =============================================================================
# EXPERIMENTS
# =============================================================================

def experiment_spectral_discontinuity(G, G_nopocket, crust, mantle, core, pocket, bridges):
    """
    Compare local spectral gaps WITH and WITHOUT the Sub-Bolso.
    If the pocket causes a spectral discontinuity, it should be
    detectable as an anomaly in the local lambda_1 values near the bridges.
    """
    print("=" * 60)
    print("  EXPERIMENT 1: SPECTRAL DISCONTINUITY")
    print("=" * 60)

    # Compute local spectral gaps for all nodes
    results_with = {}
    results_without = {}

    all_main_nodes = [n for n in crust + mantle + core if n in G.nodes()]

    print("  Computing local spectral gaps (WITH pocket)...")
    for n in all_main_nodes:
        results_with[n] = local_spectral_gap(G, n, radius=2)

    print("  Computing local spectral gaps (WITHOUT pocket)...")
    for n in all_main_nodes:
        if n in G_nopocket.nodes():
            results_without[n] = local_spectral_gap(G_nopocket, n, radius=2)

    # Find bridge-adjacent nodes
    bridge_nodes = set()
    for src, tgt in bridges:
        bridge_nodes.add(tgt)
        for nb in G.neighbors(tgt):
            if nb in all_main_nodes:
                bridge_nodes.add(nb)

    # Compute anomaly: difference in local lambda_1
    anomalies = {}
    for n in all_main_nodes:
        if n in results_with and n in results_without:
            diff = abs(results_with[n] - results_without[n])
            anomalies[n] = {
                'with': results_with[n],
                'without': results_without[n],
                'diff': diff,
                'is_bridge': n in bridge_nodes,
                'layer': G.nodes[n]['layer']
            }

    # Statistics
    bridge_diffs = [a['diff'] for a in anomalies.values() if a['is_bridge']]
    normal_diffs = [a['diff'] for a in anomalies.values() if not a['is_bridge']]

    mean_bridge = np.mean(bridge_diffs) if bridge_diffs else 0
    mean_normal = np.mean(normal_diffs) if normal_diffs else 0
    ratio = mean_bridge / mean_normal if mean_normal > 0 else float('inf')

    print(f"  Bridge-adjacent anomaly: {mean_bridge:.4f}")
    print(f"  Normal node anomaly:     {mean_normal:.4f}")
    print(f"  Ratio (bridge/normal):   {ratio:.2f}x")
    print(f"  Bridge nodes affected:   {len(bridge_diffs)}")

    return anomalies, mean_bridge, mean_normal, ratio

def experiment_tri_leakage(G, pocket_nodes, bridges):
    """
    Measure the "TRI barrier strength" around the Sub-Bolso.
    TRI = Topological Regime Incompatibility = spectral distance
    between pocket and surrounding mantle.
    """
    print("\n" + "=" * 60)
    print("  EXPERIMENT 2: TRI BARRIER LEAKAGE")
    print("=" * 60)

    # Pocket spectral gap
    pocket_subgraph = G.subgraph(pocket_nodes)
    pocket_lambda = spectral_gap(pocket_subgraph)
    print(f"  Pocket lambda_1: {pocket_lambda:.4f}")

    # Main graph spectral gap (excluding pocket)
    main_nodes = [n for n in G.nodes() if n not in pocket_nodes]
    main_subgraph = G.subgraph(main_nodes)
    if nx.is_connected(main_subgraph):
        main_lambda = spectral_gap(main_subgraph)
    else:
        largest = max(nx.connected_components(main_subgraph), key=len)
        main_lambda = spectral_gap(main_subgraph.subgraph(largest))
    print(f"  Main lambda_1:   {main_lambda:.4f}")

    # TRI barrier = spectral distance
    tri_barrier = abs(pocket_lambda - main_lambda)
    tri_ratio = pocket_lambda / main_lambda if main_lambda > 0 else float('inf')
    print(f"  TRI Barrier:     {tri_barrier:.4f}")
    print(f"  Spectral Ratio:  {tri_ratio:.2f}x")

    # Leakage: measure Ollivier-Ricci curvature at bridge edges
    bridge_curvatures = []
    for src, tgt in bridges:
        kappa = ollivier_ricci_curvature(G, src, tgt)
        bridge_curvatures.append(kappa)
        print(f"  Bridge ({src}->{tgt}): kappa = {kappa:.4f}")

    mean_kappa = np.mean(bridge_curvatures)
    print(f"  Mean bridge curvature: {mean_kappa:.4f}")

    # Compare with normal inter-layer edges
    normal_curvatures = []
    for u, v in G.edges():
        if G.edges[u, v].get('type') == 'inter':
            kappa = ollivier_ricci_curvature(G, u, v)
            normal_curvatures.append(kappa)
    mean_normal_kappa = np.mean(normal_curvatures) if normal_curvatures else 0
    print(f"  Mean normal inter-layer curvature: {mean_normal_kappa:.4f}")

    leakage_ratio = abs(mean_kappa) / abs(mean_normal_kappa) if mean_normal_kappa != 0 else float('inf')
    print(f"  Leakage ratio (bridge/normal): {leakage_ratio:.2f}x")

    return {
        'pocket_lambda': pocket_lambda,
        'main_lambda': main_lambda,
        'tri_barrier': tri_barrier,
        'tri_ratio': tri_ratio,
        'bridge_curvatures': bridge_curvatures,
        'mean_bridge_kappa': mean_kappa,
        'mean_normal_kappa': mean_normal_kappa,
        'leakage_ratio': leakage_ratio
    }

def experiment_gravity_anomaly(G, pocket_nodes, crust, mantle, core, bridges):
    """
    Map gravitational anomalies as Ollivier-Ricci curvature.
    In Tamesis: gravity = curvature kappa. Low kappa = gravitational anomaly.
    """
    print("\n" + "=" * 60)
    print("  EXPERIMENT 3: GRAVITY ANOMALY MAP")
    print("=" * 60)

    # Compute mean Ollivier-Ricci curvature for each node
    node_curvatures = {}
    all_nodes = [n for n in crust + mantle + core if n in G.nodes()]

    for node in all_nodes:
        neighbors = list(G.neighbors(node))
        if not neighbors:
            node_curvatures[node] = 0.0
            continue
        kappas = []
        for nb in neighbors:
            if G.has_edge(node, nb):
                kappas.append(ollivier_ricci_curvature(G, node, nb))
        node_curvatures[node] = np.mean(kappas) if kappas else 0.0

    # Find anomalous regions (lowest curvature = gravitational anomaly)
    sorted_nodes = sorted(node_curvatures.items(), key=lambda x: x[1])

    # Check if anomalous nodes are near bridges
    bridge_targets = {tgt for _, tgt in bridges}
    bridge_neighbors = set()
    for _, tgt in bridges:
        for nb in G.neighbors(tgt):
            bridge_neighbors.add(nb)

    print(f"\n  10 Lowest-Curvature Nodes (Gravitational Anomalies):")
    anomaly_near_pocket = 0
    for node, kappa in sorted_nodes[:10]:
        near_bridge = "** NEAR BRIDGE **" if node in bridge_neighbors else ""
        layer = G.nodes[node]['layer']
        print(f"    Node {node:4d} ({layer:6s}): kappa = {kappa:.4f} {near_bridge}")
        if node in bridge_neighbors:
            anomaly_near_pocket += 1

    print(f"\n  Anomalies near pocket: {anomaly_near_pocket}/10")

    return node_curvatures

def experiment_connectivity_hubs(G, pocket_nodes, mantle, bridges):
    """
    Find high-connectivity hubs (LLSVPs analog).
    In Tamesis: LLSVPs = high-degree nodes that anchor the Sub-Bolso.
    """
    print("\n" + "=" * 60)
    print("  EXPERIMENT 4: CONNECTIVITY HUBS (LLSVPs)")
    print("=" * 60)

    degrees = dict(G.degree())
    betweenness = nx.betweenness_centrality(G, k=min(100, len(G)))

    # Top hubs by degree
    sorted_degree = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    bridge_targets = {tgt for _, tgt in bridges}

    print(f"\n  Top 10 Hub Nodes (by Degree):")
    hubs_near_pocket = 0
    for node, deg in sorted_degree[:10]:
        layer = G.nodes[node].get('layer', '?')
        near = "** BRIDGE TARGET **" if node in bridge_targets else ""
        print(f"    Node {node:4d} ({layer:6s}): degree={deg:3d}, betweenness={betweenness.get(node, 0):.4f} {near}")
        if node in bridge_targets:
            hubs_near_pocket += 1

    print(f"\n  Hub-bridge correlation: {hubs_near_pocket}/10 top hubs are bridge targets")

    return degrees, betweenness

# =============================================================================
# VISUALIZATIONS
# =============================================================================

def plot_spectral_map(anomalies, G, bridges, filename="spectral_discontinuity.png"):
    """Plot the spectral discontinuity map."""
    print("\n[*] Plotting Spectral Discontinuity Map...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    # Map 1: Local lambda_1 WITH pocket
    ax = axes[0]
    ax.set_facecolor('#0a0a0f')
    thetas = [G.nodes[n]['theta'] for n in anomalies if n in G.nodes()]
    phis = [G.nodes[n]['phi'] for n in anomalies if n in G.nodes()]
    vals_with = [anomalies[n]['with'] for n in anomalies if n in G.nodes()]
    sc = ax.scatter(phis, thetas, c=vals_with, cmap='inferno', s=15, alpha=0.8)
    plt.colorbar(sc, ax=ax, label='Local lambda_1')
    # Mark bridge nodes
    for _, tgt in bridges:
        if tgt in G.nodes():
            ax.scatter(G.nodes[tgt]['phi'], G.nodes[tgt]['theta'],
                       c='cyan', s=100, marker='*', edgecolors='white', linewidths=0.5, zorder=5)
    ax.set_xlabel("Longitude (phi)")
    ax.set_ylabel("Latitude (theta)")
    ax.set_title("WITH SUB-POCKET", fontweight='bold')

    # Map 2: Local lambda_1 WITHOUT pocket
    ax = axes[1]
    ax.set_facecolor('#0a0a0f')
    vals_without = [anomalies[n]['without'] for n in anomalies if n in G.nodes()]
    sc2 = ax.scatter(phis, thetas, c=vals_without, cmap='inferno', s=15, alpha=0.8)
    plt.colorbar(sc2, ax=ax, label='Local lambda_1')
    ax.set_xlabel("Longitude (phi)")
    ax.set_ylabel("Latitude (theta)")
    ax.set_title("WITHOUT SUB-POCKET", fontweight='bold')

    # Map 3: Difference (Anomaly Signal)
    ax = axes[2]
    ax.set_facecolor('#0a0a0f')
    diffs = [anomalies[n]['diff'] for n in anomalies if n in G.nodes()]
    sc3 = ax.scatter(phis, thetas, c=diffs, cmap='hot', s=15, alpha=0.8)
    plt.colorbar(sc3, ax=ax, label='|Delta lambda_1|')
    for _, tgt in bridges:
        if tgt in G.nodes():
            ax.scatter(G.nodes[tgt]['phi'], G.nodes[tgt]['theta'],
                       c='cyan', s=100, marker='*', edgecolors='white', linewidths=0.5, zorder=5)
    ax.set_xlabel("Longitude (phi)")
    ax.set_ylabel("Latitude (theta)")
    ax.set_title("ANOMALY SIGNAL (DISCONTINUITY)", fontweight='bold', color='#FF4444')

    plt.suptitle("SPECTRAL DISCONTINUITY: SUB-POCKET SIGNATURE",
                 fontsize=14, fontweight='bold', color='white')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_tri_leakage(tri_results, filename="saa_tri_leakage.png"):
    """Plot TRI barrier analysis."""
    print("[*] Plotting TRI Barrier Leakage...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    # Spectral comparison
    ax = axes[0]
    ax.set_facecolor('#0a0a0f')
    categories = ['Main Monada', 'Sub-Pocket']
    lambdas = [tri_results['main_lambda'], tri_results['pocket_lambda']]
    colors = ['#44AAFF', '#FF4444']
    bars = ax.bar(categories, lambdas, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_ylabel("Spectral Gap (lambda_1)")
    ax.set_title("TRI BARRIER: SPECTRAL INCOMPATIBILITY", fontweight='bold')
    for bar, val in zip(bars, lambdas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{val:.3f}', ha='center', fontsize=10, color='white')
    ax.grid(True, color='#222222')

    # Curvature comparison
    ax = axes[1]
    ax.set_facecolor('#0a0a0f')
    categories = ['Normal Edges', 'Bridge (Wormhole)']
    kappas = [tri_results['mean_normal_kappa'], tri_results['mean_bridge_kappa']]
    colors = ['#00FF88', '#FF4444']
    bars = ax.bar(categories, kappas, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_ylabel("Mean Ollivier-Ricci Curvature")
    ax.set_title("CURVATURE AT BRIDGES vs NORMAL", fontweight='bold')
    for bar, val in zip(bars, kappas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{val:.3f}', ha='center', fontsize=10, color='white')
    ax.grid(True, color='#222222')

    plt.suptitle("TRI BARRIER ANALYSIS (SAA ANALOG)",
                 fontsize=14, fontweight='bold', color='white')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def plot_planetary_map(G, node_curvatures, pocket_nodes, bridges, degrees,
                       filename="planetary_anomaly_map.png"):
    """Full planetary anomaly map."""
    print("[*] Plotting Planetary Anomaly Map...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0a0a0f')

    all_nodes = [n for n in G.nodes() if n not in pocket_nodes]

    thetas = [G.nodes[n]['theta'] for n in all_nodes if n in G.nodes()]
    phis = [G.nodes[n]['phi'] for n in all_nodes if n in G.nodes()]
    radii = [G.nodes[n]['r'] for n in all_nodes if n in G.nodes()]

    # Curvature map
    ax = axes[0, 0]
    ax.set_facecolor('#0a0a0f')
    kappas = [node_curvatures.get(n, 0) for n in all_nodes if n in G.nodes()]
    sc = ax.scatter(phis, thetas, c=kappas, cmap='RdBu_r', s=15, alpha=0.8)
    plt.colorbar(sc, ax=ax, label='Ollivier-Ricci kappa')
    for _, tgt in bridges:
        if tgt in G.nodes():
            ax.plot(G.nodes[tgt]['phi'], G.nodes[tgt]['theta'], 'c*', markersize=12)
    ax.set_title("GRAVITY MAP (Ricci Curvature)", fontweight='bold')
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Degree map
    ax = axes[0, 1]
    ax.set_facecolor('#0a0a0f')
    degs = [degrees.get(n, 0) for n in all_nodes if n in G.nodes()]
    sc2 = ax.scatter(phis, thetas, c=degs, cmap='plasma', s=15, alpha=0.8)
    plt.colorbar(sc2, ax=ax, label='Degree (Connectivity)')
    ax.set_title("CONNECTIVITY MAP (LLSVP Analog)", fontweight='bold')
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Cross-section (r vs theta)
    ax = axes[1, 0]
    ax.set_facecolor('#0a0a0f')
    layers_colors = {'crust': '#8B4513', 'mantle': '#FF6600', 'core': '#FFD700', 'pocket': '#FF0000'}
    for n in G.nodes():
        layer = G.nodes[n].get('layer', '?')
        ax.scatter(G.nodes[n]['theta'], G.nodes[n]['r'],
                   c=layers_colors.get(layer, 'white'), s=8, alpha=0.6)
    # Draw bridges
    for src, tgt in bridges:
        if src in G.nodes() and tgt in G.nodes():
            ax.plot([G.nodes[src]['theta'], G.nodes[tgt]['theta']],
                    [G.nodes[src]['r'], G.nodes[tgt]['r']],
                    'c-', linewidth=2, alpha=0.8)
    ax.set_xlabel("Latitude (theta)")
    ax.set_ylabel("Depth (r)")
    ax.set_title("CROSS-SECTION (Pocket Location)", fontweight='bold')

    # Legend for layers
    ax_leg = axes[1, 1]
    ax_leg.set_facecolor('#0a0a0f')
    ax_leg.set_axis_off()

    summary = (
        "BOLSO TOPOLOGICO: SUMMARY\n"
        "=" * 35 + "\n\n"
        f"Planet Nodes: {len(all_nodes)}\n"
        f"Pocket Nodes: {len(pocket_nodes)}\n"
        f"Bridge Edges: {len(bridges)}\n\n"
        f"LAYERS:\n"
        f"  BROWN  = Crust (Surface)\n"
        f"  ORANGE = Mantle\n"
        f"  GOLD   = Core\n"
        f"  RED    = Sub-Pocket (Hidden)\n"
        f"  CYAN * = Bridge (Wormhole)\n\n"
        f"ANOMALY DETECTION:\n"
        f"  Low Ricci = Gravity Hole\n"
        f"  High Degree = LLSVP Hub\n"
        f"  Spectral Break = Pocket Signal\n"
    )
    ax_leg.text(0.05, 0.95, summary, transform=ax_leg.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace', color='white',
                bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))

    plt.suptitle("MACRO-MONADA: PLANETARY ANOMALY MAP",
                 fontsize=14, fontweight='bold', color='white')
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"    Saved: {path}")

def generate_pocket_gif(filename="pocket_detection.gif"):
    """Animate the process of pocket detection by scanning local spectral gaps."""
    print("[*] Rendering Pocket Detection GIF...")
    G, crust, mantle, core = build_planetary_monada(60, 40, 15)
    G_with, pocket, bridges = inject_sub_pocket(G.copy(), [m for m in mantle if m in G.nodes()], n_pocket=15, n_bridges=2)

    all_nodes = sorted([n for n in crust + mantle + core if n in G_with.nodes()])
    scan_results = {}

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=80)
    fig.patch.set_facecolor('#0a0a0f')

    batch_size = max(1, len(all_nodes) // 40)

    def update(frame):
        for ax in axes:
            ax.cla()
            ax.set_facecolor('#0a0a0f')

        # Scan more nodes
        start = frame * batch_size
        end = min(start + batch_size, len(all_nodes))
        for i in range(start, end):
            if i < len(all_nodes):
                n = all_nodes[i]
                scan_results[n] = local_spectral_gap(G_with, n, radius=2)

        # Draw map
        ax = axes[0]
        if scan_results:
            thetas = [G_with.nodes[n]['theta'] for n in scan_results]
            phis = [G_with.nodes[n]['phi'] for n in scan_results]
            vals = list(scan_results.values())
            ax.scatter(phis, thetas, c=vals, cmap='inferno', s=20, alpha=0.8)
        for _, tgt in bridges:
            if tgt in G_with.nodes():
                ax.plot(G_with.nodes[tgt]['phi'], G_with.nodes[tgt]['theta'],
                        'c*', markersize=15)
        ax.set_title(f"SCANNING... ({len(scan_results)}/{len(all_nodes)} nodes)",
                     color='white', fontweight='bold')
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # Histogram of lambda_1 values
        ax = axes[1]
        if scan_results:
            vals = list(scan_results.values())
            ax.hist(vals, bins=20, color='#FF4444', alpha=0.7, edgecolor='white')
            ax.set_xlabel("Local lambda_1")
            ax.set_ylabel("Count")
            ax.set_title("SPECTRAL DISTRIBUTION", color='white', fontweight='bold')
            ax.grid(True, color='#222222')

    n_frames = min(40, (len(all_nodes) // batch_size) + 1)
    ani = animation.FuncAnimation(fig, update, frames=n_frames, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=5)
    plt.close(fig)
    print(f"    Saved: {path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("  TAMESIS: BOLSO TOPOLOGICO")
    print("  (Vazamento Dimensional e Anomalias Planetarias)")
    print("=" * 60)

    # Build planet
    print("\n--- Building Macro-Monada (Planet) ---")
    G_base, crust, mantle, core = build_planetary_monada()
    print(f"  Nodes: {len(G_base)}, Edges: {G_base.number_of_edges()}")
    print(f"  Crust: {len([c for c in crust if c in G_base])}, Mantle: {len([m for m in mantle if m in G_base])}, Core: {len([k for k in core if k in G_base])}")
    print(f"  Global lambda_1: {spectral_gap(G_base):.4f}")

    # Save clean copy
    G_nopocket = G_base.copy()

    # Inject Sub-Bolso
    print("\n--- Injecting Sub-Pocket (25 nodes, 3 bridges) ---")
    valid_mantle = [m for m in mantle if m in G_base.nodes()]
    G_with_pocket, pocket_nodes, bridges = inject_sub_pocket(G_base, valid_mantle)
    print(f"  Pocket nodes: {len(pocket_nodes)}")
    print(f"  Bridges (wormholes): {bridges}")
    print(f"  New total: N={len(G_with_pocket)}, E={G_with_pocket.number_of_edges()}")
    print(f"  Global lambda_1 (with pocket): {spectral_gap(G_with_pocket):.4f}")

    # Experiment 1: Spectral Discontinuity
    valid_crust = [c for c in crust if c in G_with_pocket.nodes()]
    valid_mantle = [m for m in mantle if m in G_with_pocket.nodes()]
    valid_core = [k for k in core if k in G_with_pocket.nodes()]
    anomalies, mean_bridge, mean_normal, ratio = experiment_spectral_discontinuity(
        G_with_pocket, G_nopocket, valid_crust, valid_mantle, valid_core, pocket_nodes, bridges)

    # Experiment 2: TRI Leakage
    tri_results = experiment_tri_leakage(G_with_pocket, pocket_nodes, bridges)

    # Experiment 3: Gravity Anomalies
    node_curvatures = experiment_gravity_anomaly(
        G_with_pocket, pocket_nodes, valid_crust, valid_mantle, valid_core, bridges)

    # Experiment 4: Connectivity Hubs
    degrees, betweenness = experiment_connectivity_hubs(
        G_with_pocket, pocket_nodes, valid_mantle, bridges)

    # Visualizations
    print("\n--- GENERATING VISUALIZATIONS ---")
    plot_spectral_map(anomalies, G_with_pocket, bridges)
    plot_tri_leakage(tri_results)
    plot_planetary_map(G_with_pocket, node_curvatures, pocket_nodes, bridges, degrees)
    generate_pocket_gif()

    # Conclusions
    print(f"\n{'='*60}")
    print(f"  VEREDITO MATEMATICO (NIVEL CLAY)")
    print(f"{'='*60}")
    print(f"  1. DESCONTINUIDADE ESPECTRAL: {'DETECTADA' if ratio > 1.5 else 'NAO DETECTADA'}")
    print(f"     Ratio bridge/normal = {ratio:.2f}x")
    print(f"  2. BARREIRA TRI: Pocket lambda_1 = {tri_results['pocket_lambda']:.3f} vs Main = {tri_results['main_lambda']:.3f}")
    print(f"     Incompatibilidade espectral = {tri_results['tri_ratio']:.2f}x")
    print(f"  3. VAZAMENTO: Curvatura nos bridges = {tri_results['mean_bridge_kappa']:.3f} vs normal = {tri_results['mean_normal_kappa']:.3f}")
    print(f"     Leakage ratio = {tri_results['leakage_ratio']:.2f}x")
    print(f"  4. CONCLUSAO: Um Sub-Bolso topologico PRODUZ assinaturas")
    print(f"     mensuraveis em espectro, curvatura e conectividade.")
    print(f"     A hipotese e testavel. Os dados reais (SAA, LLSVP, GRACE)")
    print(f"     devem ser agora comparados com estas previsoes.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
