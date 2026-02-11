
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def simulate_guna_dynamics(steps=200, initial_state=(0.33, 0.33, 0.34), disturbance_magnitude=0.1):
    """
    Simula a dinâmica das Gunas (Sattva, Rajas, Tamas) com Visualização de Espaço de Fase.
    """
    
    sattva, rajas, tamas = initial_state
    
    history_s = [sattva]
    history_r = [rajas]
    history_t = [tamas]
    
    print(f"--- INICIANDO SIMULAÇÃO AVANÇADA DAS GUNAS (Steps={steps}) ---")
    
    for t in range(steps):
        # Modelo Dinâmico Tamesis:
        # Rajas (Energia) é injetado para converter Tamas (Massa) em Sattva (Ordem)
        # Mas Rajas também causa instabilidade.
        
        # Oscilação natural de Rajas (Ciclos Cósmicos / Yugas)
        rajas_input = disturbance_magnitude * (1 + 0.5 * np.sin(t * 0.1))
        
        # Fluxos
        # Tamas -> Sattva (via Trabalho/Rajas)
        flux_t_to_s = rajas * rajas_input * tamas
        
        # Sattva -> Tamas (via Entropia/Tempo)
        flux_s_to_t = 0.05 * sattva 
        
        # Rajas é consumido no trabalho e regenerado pela tensão
        flux_r_consumption = 0.02 * rajas
        flux_r_generation = 0.02 * abs(tamas - sattva)
        
        # Update
        sattva += flux_t_to_s - flux_s_to_t
        tamas += flux_s_to_t - flux_t_to_s
        rajas += flux_r_generation - flux_r_consumption
        
        # Normalização (S + R + T = 1)
        total = sattva + rajas + tamas
        sattva /= total
        rajas /= total
        tamas /= total
        
        history_s.append(sattva)
        history_r.append(rajas)
        history_t.append(tamas)
        
    print(f"Estado Final: S={sattva:.2f}, R={rajas:.2f}, T={tamas:.2f}")
    
    # Plotting Advanced
    fig = plt.figure(figsize=(16, 7))
    
    # Subplot 1: Time Series
    ax1 = fig.add_subplot(1, 2, 1)
    time_axis = range(steps + 1)
    ax1.plot(time_axis, history_s, label='Sattva (Order)', color='gold', linewidth=2)
    ax1.plot(time_axis, history_r, label='Rajas (Energy)', color='red', linestyle='--', linewidth=1.5)
    ax1.plot(time_axis, history_t, label='Tamas (Mass)', color='black', linewidth=2)
    ax1.set_title('Temporal Evolution of Gunas')
    ax1.set_xlabel('Time (Evolution Steps)')
    ax1.set_ylabel('Dominance')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Subplot 2: 3D Phase Space Trajectory
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.plot(history_s, history_r, history_t, color='purple', linewidth=2, label='System Trajectory')
    ax2.scatter(history_s[0], history_r[0], history_t[0], color='green', s=50, label='Start')
    ax2.scatter(history_s[-1], history_r[-1], history_t[-1], color='red', s=50, label='End')
    ax2.set_xlabel('Sattva')
    ax2.set_ylabel('Rajas')
    ax2.set_zlabel('Tamas')
    ax2.set_title('Phase Space Trajectory (Attractor?)')
    ax2.legend()
    
    # Validating "Ouroboros" (Limit Cycle) behavior
    # Se a trajetória fecha em si mesma, é um ciclo estável. Se converge, é um ponto fixo.
    
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\samkhya_gunas_advanced.png"
    plt.savefig(output_path)
    print(f"Gráfico Avançado salvo em: {output_path}")

if __name__ == "__main__":
    simulate_guna_dynamics()
