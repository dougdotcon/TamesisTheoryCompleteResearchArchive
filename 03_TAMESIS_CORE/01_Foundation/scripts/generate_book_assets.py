
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os

# Ensure assets directory exists
ASSETS_DIR = r"c:\Users\Douglas\Desktop\ToE\assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_composition_chart():
    """Generates a pie chart comparing Standard Model vs Unified Model."""
    labels = ['Matéria Comum (4%)', 'Matéria Escura (26%)', 'Energia Escura (70%)']
    sizes_standard = [4, 26, 70]
    
    labels_unified = ['Matéria (Nós Topológicos)', 'Potencial Informacional (Vácuo)']
    sizes_unified = [4, 96]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Custom colors
    colors_std = ['#ff9999', '#66b3ff', '#99ff99']
    colors_uni = ['#ff9999', '#c2c2f0']
    
    ax1.pie(sizes_standard, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors_std)
    ax1.set_title('Modelo Padrão (Atual)')
    
    ax2.pie(sizes_unified, labels=labels_unified, autopct='%1.1f%%', startangle=90, colors=colors_uni)
    ax2.set_title('Modelo Unificado (Holográfico)')
    
    plt.suptitle('Reinterpretação da Composição do Universo', fontsize=16)
    plt.savefig(os.path.join(ASSETS_DIR, 'fig_composition.png'), dpi=300)
    plt.close()
    print("Generated fig_composition.png")

def generate_entropy_life_chart():
    """Generates a graph showing Entropy vs Life."""
    t = np.linspace(0, 10, 100)
    entropy_universe = 0.5 * t**2  # Increasing entropy
    entropy_life = 10 - 0.8 * t**2 # Local negentropy
    
    # Ensure life doesn't go below zero for plot nicely
    entropy_life = np.maximum(entropy_life, 2)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, entropy_universe, label='Entropia do Universo (2ª Lei)', color='red', linewidth=3)
    plt.plot(t, entropy_life, label='Entropia de Sistemas Vivos (Vida)', color='green', linewidth=3, linestyle='--')
    
    plt.fill_between(t, entropy_life, entropy_universe, color='gray', alpha=0.1, label='Trabalho Dissipativo')
    
    plt.title('A Vida como Resistência Termodinâmica', fontsize=14)
    plt.xlabel('Tempo')
    plt.ylabel('Entropia (S)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.annotate('Morte Térmica', xy=(9, 40), xytext=(6, 35),
                 arrowprops=dict(facecolor='black', shrink=0.05))
                 
    plt.annotate('Complexidade Biológica', xy=(2, 9), xytext=(4, 15),
                 arrowprops=dict(facecolor='green', shrink=0.05))

    plt.savefig(os.path.join(ASSETS_DIR, 'fig_entropy_life.png'), dpi=300)
    plt.close()
    print("Generated fig_entropy_life.png")

def generate_omega_scaling():
    """Generates a visual representation of Omega scaling."""
    levels = ['Planck', 'Partícula', 'Célula', 'Humano', 'Planeta', 'Galáxia', 'Universo']
    scales = [-35, -15, -6, 0, 7, 21, 26] # approx log meters
    
    plt.figure(figsize=(12, 6))
    plt.plot(scales, np.zeros_like(scales), '-o', color='purple', markersize=10)
    
    for i, (txt, x) in enumerate(zip(levels, scales)):
        plt.text(x, 0.1, txt, ha='center', fontsize=12, rotation=45)
        plt.text(x, -0.2, f'10^{{{x}}} m', ha='center', fontsize=10)
        
        # Draw harmonic lines
        if i < len(scales)-1:
             mid = (scales[i] + scales[i+1])/2
             plt.text(mid, 0.05, r'$\times \Omega^n$', ha='center', color='blue', fontsize=8)

    plt.title('A Escala Harmônica do Universo ($\Omega = 117.038$)', fontsize=14)
    plt.yticks([])
    plt.xlabel('Escala Logarítmica (Metros)')
    plt.ylim(-0.5, 0.5)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    
    plt.savefig(os.path.join(ASSETS_DIR, 'fig_omega_scale.png'), dpi=300)
    plt.close()
    print("Generated fig_omega_scale.png")

def generate_synchronicity_network():
    """Generates a network graph for synchronicity."""
    G = nx.Graph()
    
    # Central Node
    G.add_node("Observador", size=3000, color='red')
    
    # Concepts
    concepts = ["Ideia", "Evento Físico", "Sonho", "Número", "Passado", "Futuro"]
    for c in concepts:
        G.add_node(c, size=1000, color='skyblue')
        G.add_edge("Observador", c, weight=2)
    
    # Cross connections (Acausal)
    G.add_edge("Sonho", "Evento Físico", weight=1, style='dashed')
    G.add_edge("Ideia", "Número", weight=1, style='dashed')
    
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(8, 8))
    
    # Draw nodes
    node_sizes = [G.nodes[n].get('size', 1000) for n in G.nodes]
    node_colors = [G.nodes[n].get('color', 'skyblue') for n in G.nodes]
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Draw solid edges
    solid_edges = [(u, v) for (u, v, d) in G.edges(data=True) if d.get('style') != 'dashed']
    nx.draw_networkx_edges(G, pos, edgelist=solid_edges, width=2)
    
    # Draw dashed edges (Synchronicities)
    dashed_edges = [(u, v) for (u, v, d) in G.edges(data=True) if d.get('style') == 'dashed']
    nx.draw_networkx_edges(G, pos, edgelist=dashed_edges, width=2, style='dashed', edge_color='orange')

    plt.title('Rede de Ressonância Não-Local (Sincronicidade)', fontsize=14)
    plt.axis('off')
    
    plt.savefig(os.path.join(ASSETS_DIR, 'fig_synchronicity_network.png'), dpi=300)
    plt.close()
    print("Generated fig_synchronicity_network.png")

if __name__ == "__main__":
    print("Generating assets...")
    generate_composition_chart()
    generate_entropy_life_chart()
    generate_omega_scaling()
    generate_synchronicity_network()
    print("Done.")
