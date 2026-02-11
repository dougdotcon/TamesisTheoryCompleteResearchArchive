
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time

def simulate_pralaya(num_nodes=100, initial_connectivity=0.1, steps=20):
    """
    Simula o processo de Pralaya (Dissolução) como uma Transição de Fase em um Grafo.
    
    Conceitos Vaisheshika mapeados:
    - Nós: Parmanus (Átomos/Bits)
    - Arestas: Dyanukas/Samavaya (Inerência/Conexão Forte)
    - Adrista: Energia de Coesão Inicial
    - Entropy (Ruído): Força de Expansão/Repulsão que cresce com o tempo
    """
    
    print(f"--- INICIANDO SIMULAÇÃO DE PRALAYA (N={num_nodes}) ---")
    
    # 1. Criação do Universo Ativo (Kalpa) - Alta Conectividade
    # Usamos um grafo aleatório geométrico ou Erdos-Renyi para representar a estrutura
    G = nx.erdos_renyi_graph(num_nodes, initial_connectivity)
    
    # Atribui força de ligação (Samavaya) a cada aresta
    # Samavaya varia entre 0.0 e 1.0
    for u, v in G.edges():
        G[u][v]['samavaya'] = np.random.uniform(0.5, 1.0) # Ligações inicialmente fortes
        
    print(f"Tempo T=0 (Kalpa/Vida):")
    print(f"  - Arestas (Dyanukas): {G.number_of_edges()}")
    print(f"  - Componentes Conectados: {nx.number_connected_components(G)}")
    largest_cc = len(max(nx.connected_components(G), key=len)) if len(G) > 0 else 0
    print(f"  - Maior Componente (Matter Bulk): {largest_cc}/{num_nodes}")
    print("-" * 40)
    
    # 2. Processo de Dissolução (Entropia Crescente)
    history_largest_component = []
    connectivity_threshold = 0.0 # Nível de ruído ambiente
    
    broken_graph = False
    
    for t in range(steps):
        # Aumenta a Entropia do Sistema (Expansão do Universo / Dark Energy)
        entropy_noise = (t / steps) * 1.5 # Vai de 0.0 a 1.5
        
        edges_to_remove = []
        for u, v in G.edges():
            bond_strength = G[u][v]['samavaya']
            
            # Pralaya Condition: Se o Ruído (Entropia) superar a Coesão (Samavaya)
            # A aresta quebra (Samavaya rompido -> Samyoga desfeito)
            if entropy_noise > bond_strength:
                edges_to_remove.append((u, v))
                
        G.remove_edges_from(edges_to_remove)
        
        # Análise Topológica
        num_components = nx.number_connected_components(G)
        largest_cc = len(max(nx.connected_components(G), key=len)) if len(G) > 0 else 0
        history_largest_component.append(largest_cc)
        
        # Detecta transição de fase (Percolation Threshold Reverso)
        if not broken_graph and largest_cc < (num_nodes * 0.1): # Menos de 10% conectado
            print(f"*** ALERTA DE PRALAYA *** Tempo T={t}: O Grande Colapso ocorreu.")
            print(f"    (O Grafo perdeu sua componente gigante. A geometria espaço-temporal se desfez.)")
            broken_graph = True

        if t % 5 == 0 or t == steps - 1:
             print(f"Tempo T={t} | Ruído Escalar: {entropy_noise:.2f}")
             print(f"  - Arestas Restantes: {G.number_of_edges()}")
             print(f"  - Maior Cluster: {largest_cc}")

    print("-" * 40)
    print("RESUMO FINAL DA DISSOLUÇÃO:")
    print(f"Átomos Isolados (Parmanus Livres): {num_nodes - G.number_of_edges()}") # Aprox
    print(f"O Universo retornou ao estado de poeira (Dust).")
    
    # Plotting
    plt.figure(figsize=(10, 6))
    # Ruído Escalar estimado para o eixo X
    noise_levels = [(t / steps) * 1.5 for t in range(steps)]
    
    plt.plot(noise_levels, history_largest_component, marker='x', linestyle='--', color='red')
    plt.title('Vaisheshika Dissolution (Pralaya): Topological Collapse')
    plt.xlabel('Entropy Noise Level (Time)')
    plt.ylabel('Size of Largest Connected Component (Matter Bulk)')
    plt.axvline(x=1.0, color='k', linestyle=':', label='Theoretical Pralaya Threshold (Noise > Cohesion)')
    plt.legend()
    plt.grid(True)
    
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\vaisheshika_pralaya.png"
    plt.savefig(output_path)
    print(f"Gráfico salvo em: {output_path}")
    
    return history_largest_component

if __name__ == "__main__":
    simulate_pralaya()
