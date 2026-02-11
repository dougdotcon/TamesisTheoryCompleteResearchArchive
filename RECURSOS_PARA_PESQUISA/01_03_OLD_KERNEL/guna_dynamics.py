
import numpy as np
import matplotlib.pyplot as plt

def simulate_guna_dynamics(steps=100, initial_state=(0.33, 0.33, 0.34), disturbance_magnitude=0.05):
    """
    Simula a dinâmica das Gunas (Sattva, Rajas, Tamas) como um sistema de equações diferenciais acopladas.
    
    Tamesis Kernel v3 Interpretation:
    - Sattva (S): Informação Estruturada / Ordem (Baixa Entropia)
    - Rajas (R): Energia Livre / Função de Transferência (Movimento)
    - Tamas (T): Massa / Inércia / Saturação (Alta Entropia)
    
    A conservação total é 1.0 (S + R + T = 1).
    """
    
    sattva, rajas, tamas = initial_state
    
    history_s = [sattva]
    history_r = [rajas]
    history_t = [tamas]
    
    print(f"--- INICIANDO SIMULAÇÃO DAS GUNAS (Steps={steps}) ---")
    print(f"Estado Inicial: S={sattva:.2f}, R={rajas:.2f}, T={tamas:.2f}")
    
    for t in range(steps):
        # A Perturbação (Purusha Observation) injeta energia no sistema
        # Se Rajas é alto, a conversão é rápida.
        
        # Modelo Dinâmico Tamesis:
        # 1. Rajas consome Tamas para criar Sattva (Trabalho converte Massa em Ordem)
        # 2. Entropia natural degrada Sattva em Tamas (Decaimento)
        
        # Fator de conversão baseado em Rajas (Atividade)
        conversion_rate = rajas * disturbance_magnitude
        
        # Fator de decaimento natural (2ª Lei)
        decay_rate = 0.02 
        
        # Equações de Fluxo:
        # Tamas -> Sattva (via Rajas): O esforço organiza o caos
        d_tamas_to_sattva = conversion_rate * tamas
        
        # Sattva -> Tamas (via Decaimento): A ordem se desfaz em inércia se não mantida
        d_sattva_to_tamas = decay_rate * sattva
        
        # Atualização de Estados
        new_sattva = sattva + d_tamas_to_sattva - d_sattva_to_tamas
        new_tamas = tamas - d_tamas_to_sattva + d_sattva_to_tamas
        
        # Rajas flutua com base na "tensão" do sistema (diferença de potencial)
        # Se o sistema está muito desequilibrado, Rajas tende a aumentar para corrigir
        rajas_fluctuation = (new_tamas - new_sattva) * 0.01
        new_rajas = rajas + rajas_fluctuation
        
        # Normalização (Conservation Law)
        total = new_sattva + new_rajas + new_tamas
        sattva = new_sattva / total
        rajas = new_rajas / total
        tamas = new_tamas / total
        
        history_s.append(sattva)
        history_r.append(rajas)
        history_t.append(tamas)
        
    print(f"Estado Final: S={sattva:.2f}, R={rajas:.2f}, T={tamas:.2f}")
    
    # Plotting
    plt.figure(figsize=(10, 6))
    time_axis = range(steps + 1)
    
    plt.plot(time_axis, history_s, label='Sattva (Ordem/Luz)', color='gold', linewidth=2)
    plt.plot(time_axis, history_r, label='Rajas (Energia/Ação)', color='red', linestyle='--', linewidth=1.5)
    plt.plot(time_axis, history_t, label='Tamas (Massa/Inércia)', color='black', linewidth=2)
    
    plt.title('Samkhya Interface: Guna Dynamics Simulation')
    plt.xlabel('Time (Evolution Steps)')
    plt.ylabel('Relative Dominance (Probability)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\samkhya_gunas.png"
    plt.savefig(output_path)
    print(f"Gráfico salvo em: {output_path}")

if __name__ == "__main__":
    simulate_guna_dynamics()
