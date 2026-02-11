
import time
import random
import matplotlib.pyplot as plt

class Narayanastra:
    """
    Simulação da Arma Autônoma do Mahabharata (Narayanastra).
    Lógica: Grey Goo / Swarm que se alimenta de energia cinética (Rajas).
    Tamesis Theory: Um algoritmo de feedback positivo que converte Agressão em Replicação.
    """
    def __init__(self):
        self.swarm_count = 1000  # Unidades iniciais
        self.active = True
        self.replication_rate = 1.5  # Fator de crescimento exponencial
        self.history_swarm = []
        self.history_rajas = []
        self.history_damage = []

    def scan_battlefield(self, enemies):
        """
        Sensor de Rajas: Detecta a soma de agressão/movimento dos alvos.
        Input: Lista de entidades com nível de 'aggression' (0-100+).
        """
        total_rajas = sum([u['aggression'] for u in enemies])
        return total_rajas

    def engage(self, rajas_level):
        self.history_rajas.append(rajas_level)
        self.history_swarm.append(self.swarm_count)
        
        if rajas_level == 0:
            print(f">> CONDICIONAL ATIVADA: Ameaça Zero.")
            print(f">> PROTOCOLO: Cessar Fogo. Entrando em Standby.")
            # self.swarm_count = 1000 # Opcional: Reset
            damage = 0
        else:
            # Lógica de Multiplicação: O ataque escala com a defesa
            new_units = int(self.swarm_count * self.replication_rate * (rajas_level / 100)) # Ajuste p/ escala
            if new_units == 0 and rajas_level > 0: new_units = 50
            
            self.swarm_count += new_units
            damage = self.swarm_count * 10 
            
            print(f">> AMEAÇA: {rajas_level} | SWARM: {self.swarm_count} | DANO: {damage}")
            
        self.history_damage.append(damage)
        return damage

def battle_simulation_visual():
    print("--- INÍCIO DA EXECUÇÃO DO PROTOCOLO NARAYANASTRA (VISUAL) ---")
    
    weapon = Narayanastra()
    
    # Simulação de Rodadas
    rounds = 15
    
    # Cenário: Resistência Inicial -> Escalada -> Pico -> Rendição
    aggression_profile = [50, 60, 80, 100, 150, 200, 300, 400, 500, 600, 200, 100, 50, 0, 0]
    
    for r, agg in enumerate(aggression_profile):
        enemies = [{'aggression': agg}]
        rajas = weapon.scan_battlefield(enemies)
        weapon.engage(rajas)
        
    # Plotting Insights
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Rajas vs Time
    ax1.plot(range(rounds), aggression_profile, 'r-o', label='Enemy Aggression (Rajas)')
    ax1.set_title('Input: Enemy Resistance Levels')
    ax1.set_xlabel('Battle Rounds')
    ax1.set_ylabel('Aggression Units')
    ax1.grid(True)
    ax1.legend()
    
    # Plot 2: Swarm Growth (Exponential Feedback)
    ax2.plot(range(rounds), weapon.history_swarm, 'k-x', label='Swarm Units (Narayanastra)')
    ax2.set_title('Output: Swarm Replication Growth')
    ax2.set_xlabel('Battle Rounds')
    ax2.set_ylabel('Unit Count (Log Scale)')
    ax2.set_yscale('log')
    ax2.grid(True)
    ax2.legend()
    
    plt.suptitle('Narayanastra Algorithm: Feedback Loop Analysis', fontsize=16)
    
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\astra_feedback_loop.png"
    plt.savefig(output_path)
    print(f"Gráfico de Insights salvo em: {output_path}")

if __name__ == "__main__":
    battle_simulation_visual()
