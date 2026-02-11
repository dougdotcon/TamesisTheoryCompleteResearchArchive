
import numpy as np
import matplotlib.pyplot as plt

def vedic_particle_simulation():
    print("--- SIMULAÇÃO: INTERAÇÃO AGNI (BOSON) vs SOMA (FERMION) ---")
    
    # 1. DEFINIÇÃO DAS PARTÍCULAS (Segundo a tese de Roy)
    # Soma (Matéria/Férmion): Tem massa, ocupa espaço (Exclusão de Pauli).
    # Agni (Luz/Bóson): Não tem massa, carrega força, pode se sobrepor.
    
    grid_size = 50
    universe_grid = np.zeros((grid_size, grid_size))
    
    # Inicializando Soma (Matéria Fria) no centro
    soma_density = 100.0
    universe_grid[20:30, 20:30] = soma_density
    
    # Inicializando Agni (Energia Cinética) nas bordas, movendo-se para dentro
    # Na simulação simplificada, a 'intensidade' de Agni é um parâmetro global
    agni_intensity = 50.0
    
    print(f"Estado Inicial: Massa (Soma) concentrada. Energia (Agni) injetada.")
    
    # 2. O RITUAL (Yajna) / A REAÇÃO FÍSICA
    # Hino: "Agni, o devorador, consome o Soma e libera Luz."
    # Física: Aniquilação ou Conversão de Massa em Energia.
    
    time_steps = 15
    energy_output = []
    mass_remaining = []
    
    current_mass = np.sum(universe_grid)
    
    for t in range(time_steps):
        if current_mass <= 0:
            break

        # Interação: Agni 'ataca' Soma 
        # Taxa de conversão baseada na 'Voracidade' de Agni (seção transversal de reação)
        reaction_rate = 0.05 * agni_intensity 
        
        # A quantidade convertida não pode exceder a massa existente
        converted_mass = min(current_mass, reaction_rate * 10) 
        
        # E = mc^2 (Simplificado para escala da simulação)
        # Vamos usar um c^2 arbitrário mas grande para mostrar a magnitude
        c_squared = 9e4 
        liberated_energy = converted_mass * c_squared
        
        # Atualiza o grid (Soma desaparece)
        # Reduzimos uniformemente para simplificar a visualização do agregado
        percentage_lost = converted_mass / current_mass
        universe_grid *= (1.0 - percentage_lost)
        
        current_mass = np.sum(universe_grid)
        
        mass_remaining.append(current_mass)
        energy_output.append(liberated_energy)
        
        print(f"Tempo {t}: Massa Restante = {current_mass:.2f} | Energia Liberada = {liberated_energy:.2e} Joules")

    # 3. VISUALIZAÇÃO
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Time (Yajna Cycles)')
    ax1.set_ylabel('Mass (Soma/Fermions)', color=color)
    ax1.plot(range(len(mass_remaining)), mass_remaining, color=color, marker='o', label='Soma Remaining')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Energy Output (Agni/Bosons)', color=color)  # we already handled the x-label with ax1
    ax2.plot(range(len(energy_output)), energy_output, color=color, linestyle='--', marker='x', label='Agni Output (E=mc²)')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Vedic Physics Decoded: Yajna as Mass-Energy Conversion Reactor')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\quantum_veda_agni_soma.png"
    plt.savefig(output_path)
    print(f"Gráfico salvo em: {output_path}")

if __name__ == "__main__":
    vedic_particle_simulation()
