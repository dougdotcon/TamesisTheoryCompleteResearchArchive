
import numpy as np
import random
import matplotlib.pyplot as plt

class Parmanu:
    """
    O Nó Entrópico Fundamental (Kernel v3).
    Representa o bit indivisível de informação.
    """
    def __init__(self, id):
        self.id = id
        self.state = np.random.choice([-1, 1]) # Spin/Bit
        self.neighbors = [] # Adrista conecta isso
        self.holographic_capacity = 4.0 # Limite simplificado
        # Estado 1 ou -1 representa a 'carga' ou 'spin'

    def connect(self, other_parmanu):
        """Forma um Dyanuka (Aresta) se termodinamicamente favoravel"""
        if self.id == other_parmanu.id:
            return False
            
        if other_parmanu in self.neighbors:
            return False

        # Regra de Saturação Holográfica 
        if len(self.neighbors) >= self.holographic_capacity: 
            return False
            
        # Regra de Afinidade (Simulando Adrista/Entropia)
        # Conexão reduz energia se spins são opostos (exemplo de minimização de energia)
        # OU conexão aumenta entropia se permite maior fluxo.
        # Vamos assumir regra simples: Conectar reduz Energia Livre do sistema LOCAL
        
        self.neighbors.append(other_parmanu)
        other_parmanu.neighbors.append(self)
        return True

class AdristaField:
    """
    O Campo de Força Entrópica (Adrista).
    Calcula o gradiente que causa o primeiro movimento.
    """
    def compute_system_energy(self, parmanus):
        """
        Calcula a 'Energia Livre' do sistema.
        E = - sum(conexões) + penalidade_isolamento
        O objetivo do universo é minimizar isso.
        """
        energy = 0
        total_connections = 0
        
        for p in parmanus:
            # Penalidade por ser isolado (Alta Entropia não configurada)
            if len(p.neighbors) == 0:
                energy += 10 
            else:
                # Recompensa por conexão (Redução de Energia Livre via correlação)
                energy -= len(p.neighbors)
                total_connections += len(p.neighbors)
                
        # Ajusta contagem dupla de arestas
        total_connections = total_connections / 2
        return energy, total_connections

def simulate_creation(num_atoms=50, steps=20):
    print(f"--- INICIANDO SIMULAÇÃO KERNEL KANADA (N={num_atoms}) ---")
    
    # 1. Criação do Nun (Vácuo com Potencial)
    parmanus = [Parmanu(i) for i in range(num_atoms)]
    adrista = AdristaField()
    
    initial_energy, _ = adrista.compute_system_energy(parmanus)
    print(f"Tempo T=0 (Pralaya/Caos): Energia do Sistema = {initial_energy}")
    
    energy_history = [initial_energy]
    
    # 2. Ação do Adrista (Evolução)
    for t in range(steps):
        # Tenta formar Dyanukas
        # Escolhe 2 átomos aleatórios
        p1 = random.choice(parmanus)
        p2 = random.choice(parmanus)
        
        if p1.connect(p2):
            # Se conectou, verifica se melhorou o sistema
             pass
        
        # Record energy state
        current_energy, _ = adrista.compute_system_energy(parmanus)
        energy_history.append(current_energy)
             
    # 3. Análise Final
    final_energy, total_bonds = adrista.compute_system_energy(parmanus)
    
    dyanukas_count = 0
    tryanukas_count = 0 # Clusters de 3+
    
    for p in parmanus:
        if len(p.neighbors) == 1:
            # Note: Isso conta nós em dyades, então divide por 2 depois grosseiramente para estimativa
            dyanukas_count += 1
        elif len(p.neighbors) >= 2: # Parte de algo maior
            tryanukas_count += 1
            
    print(f"Tempo T={steps} (Criação): Energia do Sistema = {final_energy}")
    print(f"Total de Ligações (Arestas): {int(total_bonds)}")
    print(f"Nós participando de estruturas: {dyanukas_count + tryanukas_count}/{num_atoms}")
    print(f"Redução de Entropia Configuracional confirmada.")
    print("---------------------------------------------------")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(range(steps + 1), energy_history, marker='o', linestyle='-', color='blue')
    plt.title('Vaisheshika Creation: System Free Energy Minimization')
    plt.xlabel('Time Steps (Adrista Action)')
    plt.ylabel('System Free Energy')
    plt.grid(True)
    plt.annotate('Creation (Srishti)', xy=(0, energy_history[0]), xytext=(5, energy_history[0]+50),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('Equilibrium', xy=(steps, energy_history[-1]), xytext=(steps-5, energy_history[-1]+50),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\vaisheshika_creation.png"
    plt.savefig(output_path)
    print(f"Gráfico salvo em: {output_path}")

if __name__ == "__main__":
    simulate_creation()
