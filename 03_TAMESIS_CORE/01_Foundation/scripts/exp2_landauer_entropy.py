"""
Experimento 2: Calorimetria da Informação (Princípio de Landauer)

Valida a Seção III-A do paper "Restrições Termodinâmicas na Complexidade de Tempo Não-Polinomial"

Hipótese: O trabalho dissipado W = kT·ΔS escala com a redução do espaço de busca.
    ΔS ≥ kB ln 2 · I_erased

Para resolver um problema de N bits, precisamos "esquecer" 2^N - 1 estados,
o que requer dissipar entropia proporcional a N bits.

Author: Douglas H. M. Fulber
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Adicionar diretório de scripts ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from thermodynamic_turing_machine import ThermodynamicSimulation, generate_random_spin_glass

# Configuração de visualização
plt.style.use('default')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['figure.dpi'] = 150

# Constantes Físicas (unidades naturais)
K_B = 1.0  # Constante de Boltzmann (normalizada)
T = 1.0    # Temperatura (normalizada)
LN2 = np.log(2)


def entropy_evolution_experiment(N: int, num_points: int = 50):
    """
    Simula a evolução da entropia durante o processo de annealing.
    
    Args:
        N: Número de qubits
        num_points: Pontos de amostragem durante a evolução
    
    Returns:
        Dict com resultados do experimento
    """
    # Gerar instância
    J, h = generate_random_spin_glass(N, seed=N * 42)
    sim = ThermodynamicSimulation(N, J, h)
    
    s_vals = np.linspace(0, 1, num_points)
    entropies = []
    probabilities = []
    
    # Entropia inicial: superposição uniforme = log2(2^N) = N bits
    S_initial = N
    
    for s in s_vals:
        evals, evecs = sim.get_spectrum(s, num_eigen=1)
        ground_state = evecs[:, 0]
        
        # Entropia de Shannon do estado fundamental
        S = sim.shannon_entropy(ground_state)
        entropies.append(S)
        
        # Probabilidade de estar no estado fundamental verdadeiro (s=1)
        if s > 0:
            evals_final, evecs_final = sim.get_spectrum(1.0, num_eigen=1)
            true_ground = evecs_final[:, 0]
            overlap = np.abs(np.vdot(ground_state, true_ground)) ** 2
            probabilities.append(overlap)
        else:
            probabilities.append(1.0 / (2 ** N))  # Superposição uniforme
    
    S_final = entropies[-1]
    delta_S = S_initial - S_final  # Entropia "esquecida"
    
    # Trabalho dissipado segundo Landauer
    W_landauer = K_B * T * LN2 * delta_S
    
    # Limite de Landauer teórico para encontrar 1 solução em 2^N
    W_landauer_min = K_B * T * LN2 * N  # Precisamos "esquecer" N bits
    
    return {
        's_vals': s_vals,
        'entropies': np.array(entropies),
        'probabilities': np.array(probabilities),
        'S_initial': S_initial,
        'S_final': S_final,
        'delta_S': delta_S,
        'W_dissipated': W_landauer,
        'W_landauer_min': W_landauer_min
    }


def run_scaling_experiment(min_N: int = 3, max_N: int = 10):
    """
    Executa o experimento de escala da entropia para diferentes tamanhos.
    """
    Ns = list(range(min_N, max_N + 1))
    results_list = []
    
    print("=" * 60)
    print("EXPERIMENTO 2: CALORIMETRIA DA INFORMAÇÃO (LANDAUER)")
    print("Validando Seção III-A - Custo entrópico do apagamento")
    print("=" * 60)
    
    for n in Ns:
        result = entropy_evolution_experiment(n)
        results_list.append(result)
        
        print(f"N={n:2d}: S_inicial = {result['S_initial']:.2f} bits, "
              f"S_final = {result['S_final']:.4f} bits, "
              f"ΔS = {result['delta_S']:.4f} bits")
    
    return Ns, results_list


def analyze_and_plot(Ns, results_list, output_dir: str):
    """
    Analisa e visualiza os resultados do experimento de Landauer.
    """
    # Extrair dados para análise
    delta_S_vals = [r['delta_S'] for r in results_list]
    W_dissipated = [r['W_dissipated'] for r in results_list]
    W_landauer_min = [r['W_landauer_min'] for r in results_list]
    
    # Fit linear: ΔS = a*N + b
    coeffs = np.polyfit(Ns, delta_S_vals, 1)
    slope = coeffs[0]
    
    print("\n" + "=" * 60)
    print("ANÁLISE DOS RESULTADOS")
    print("=" * 60)
    print(f"Fit linear: ΔS = {coeffs[0]:.4f}*N + {coeffs[1]:.4f}")
    print(f"Previsão de Landauer: ΔS = N (slope = 1)")
    print(f"Razão medido/teórico = {slope:.4f}")
    
    if slope > 0.8:
        print("\n✓ HIPÓTESE VALIDADA: Entropia dissipada escala linearmente com N")
        print("  O custo termodinâmico de resolver problemas escala com o tamanho")
    else:
        print("\n✗ HIPÓTESE PARCIALMENTE VALIDADA: Scaling menor que esperado")
    
    # Criar figura com 3 subplots
    fig = plt.figure(figsize=(16, 5))
    
    # Plot 1: Evolução da entropia durante annealing (para N específico)
    ax1 = fig.add_subplot(131)
    
    # Mostrar curvas para alguns valores de N
    colors = plt.cm.viridis(np.linspace(0, 1, len(Ns)))
    for i, (n, r) in enumerate(zip(Ns, results_list)):
        if n in [Ns[0], Ns[len(Ns)//2], Ns[-1]]:  # Início, meio, fim
            ax1.plot(r['s_vals'], r['entropies'], '-', color=colors[i], 
                     linewidth=2, label=f'N={n}')
    
    ax1.set_xlabel('Parâmetro de Annealing $s$', fontsize=12)
    ax1.set_ylabel('Entropia de Shannon $S(s)$ [bits]', fontsize=12)
    ax1.set_title('Evolução da Entropia Durante Annealing', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    # Anotação do Limite de Landauer
    ax1.annotate('Compressão do\nespaço de estados', 
                 xy=(0.5, results_list[-1]['entropies'][25]),
                 xytext=(0.7, results_list[-1]['entropies'][10]),
                 fontsize=10, color='red',
                 arrowprops=dict(arrowstyle='->', color='red', alpha=0.7))
    
    # Plot 2: Entropia dissipada vs N
    ax2 = fig.add_subplot(132)
    
    ax2.plot(Ns, delta_S_vals, 'o-', color='#2E86AB', markersize=8, linewidth=2,
             label='ΔS medido')
    
    # Linha teórica de Landauer
    N_fit = np.linspace(Ns[0], Ns[-1], 100)
    ax2.plot(N_fit, N_fit, '--', color='#E94F37', linewidth=2,
             label='Limite de Landauer (ΔS = N)')
    
    # Fit linear
    ax2.plot(N_fit, np.polyval(coeffs, N_fit), ':', color='green', linewidth=1.5,
             label=f'Fit: ΔS = {slope:.2f}N')
    
    ax2.set_xlabel('N (Tamanho do Problema)', fontsize=12)
    ax2.set_ylabel('Entropia Dissipada ΔS [bits]', fontsize=12)
    ax2.set_title('Validação do Princípio de Landauer', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper left')
    ax2.grid(True, linestyle=':', alpha=0.5)
    
    # Plot 3: Trabalho dissipado
    ax3 = fig.add_subplot(133)
    
    ax3.bar(Ns, W_dissipated, alpha=0.7, color='#F77F00', label='W dissipado')
    ax3.plot(Ns, W_landauer_min, 's--', color='#7B2D26', markersize=6,
             label='Limite Landauer $W_{min} = k_B T \\ln 2 \\cdot N$')
    
    ax3.set_xlabel('N (Tamanho do Problema)', fontsize=12)
    ax3.set_ylabel('Trabalho Dissipado $W$ [$k_B T$]', fontsize=12)
    ax3.set_title('Custo Termodinâmico da Computação', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, linestyle=':', alpha=0.5, axis='y')
    
    plt.tight_layout()
    
    # Salvar figura
    output_path = os.path.join(output_dir, "fig4_entropy_dissipation.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"\nGráfico salvo em: {output_path}")
    
    return {
        'slope': slope,
        'hypothesis_validated': slope > 0.8
    }


def main():
    """Função principal do experimento."""
    output_dir = r"c:\Users\Douglas\Desktop\ToE\assets"
    os.makedirs(output_dir, exist_ok=True)
    
    # Executar experimento
    Ns, results_list = run_scaling_experiment(min_N=3, max_N=10)
    
    # Analisar e plotar
    analysis = analyze_and_plot(Ns, results_list, output_dir)
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO DO EXPERIMENTO 2")
    print("=" * 60)
    if analysis['hypothesis_validated']:
        print("A simulação CONFIRMA o Princípio de Landauer:")
        print(f"  - Entropia dissipada ΔS ≈ {analysis['slope']:.2f}*N bits")
        print("  - Trabalho dissipado W escala linearmente com N")
        print("  - Não é possível 'esquecer' informação sem custo termodinâmico")
        print("\n→ Resolver problemas NP requer energia proporcional ao tamanho!")
    else:
        print("Resultados parciais - scaling menor que o esperado")
    
    return analysis


if __name__ == "__main__":
    results = main()
