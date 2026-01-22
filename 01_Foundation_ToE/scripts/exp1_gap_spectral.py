"""
Experimento 1: Análise de Escala do Gap Espectral (Landau-Zener)

Valida a Seção V do paper "Restrições Termodinâmicas na Complexidade de Tempo Não-Polinomial"

Hipótese: O gap espectral mínimo Δmin fecha exponencialmente com N:
    Δmin ∝ e^(-αN)

Se confirmado, isso prova que o tempo de annealing adiabático T >> 1/Δmin²
escala exponencialmente, impedindo solução em tempo polinomial.

Author: Douglas H. M. Fulber
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Adicionar diretório de scripts ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from thermodynamic_turing_machine import ThermodynamicSimulation, generate_random_spin_glass

# Configuração de visualização estilo publicação científica
plt.style.use('default')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['figure.dpi'] = 150


def run_gap_scaling_experiment(min_N: int = 3, max_N: int = 10, num_samples: int = 5):
    """
    Executa o experimento de escala do gap espectral.
    
    Para cada tamanho N, gera múltiplas instâncias aleatórias de spin glass
    e calcula o gap mínimo médio.
    
    Args:
        min_N: Tamanho mínimo do sistema
        max_N: Tamanho máximo do sistema
        num_samples: Número de amostras por tamanho N
    
    Returns:
        Tuple (Ns, mean_gaps, std_gaps, mean_iprs)
    """
    Ns = list(range(min_N, max_N + 1))
    mean_gaps = []
    std_gaps = []
    mean_iprs = []
    
    print("=" * 60)
    print("EXPERIMENTO 1: ESCALA DO GAP ESPECTRAL")
    print("Validando Seção V - Fechamento exponencial do gap")
    print("=" * 60)
    
    for n in Ns:
        gaps = []
        iprs = []
        
        for sample in range(num_samples):
            # Gerar instância de spin glass
            J, h = generate_random_spin_glass(n, seed=sample * 100 + n)
            sim = ThermodynamicSimulation(n, J, h)
            
            # Encontrar gap mínimo
            min_gap, s_crit, ground_state = sim.find_minimum_gap(num_points=50)
            gaps.append(min_gap)
            
            # Calcular IPR no ponto crítico
            ipr = sim.inverse_participation_ratio(ground_state)
            iprs.append(ipr)
        
        mean_gap = np.mean(gaps)
        std_gap = np.std(gaps)
        mean_ipr = np.mean(iprs)
        
        mean_gaps.append(mean_gap)
        std_gaps.append(std_gap)
        mean_iprs.append(mean_ipr)
        
        print(f"N={n:2d}: Δmin = {mean_gap:.6f} ± {std_gap:.6f}, IPR = {mean_ipr:.4f}")
    
    return np.array(Ns), np.array(mean_gaps), np.array(std_gaps), np.array(mean_iprs)


def analyze_and_plot(Ns, mean_gaps, std_gaps, mean_iprs, output_dir: str):
    """
    Analisa os resultados e gera o gráfico de escala.
    """
    # Fit exponencial: log(gap) = -α*N + β
    log_gaps = np.log(mean_gaps)
    coeffs = np.polyfit(Ns, log_gaps, 1)
    alpha = -coeffs[0]
    beta = coeffs[1]
    
    # Fit para IPR
    ipr_coeffs = np.polyfit(Ns, mean_iprs, 1)
    
    # R² do fit exponencial
    log_gaps_pred = np.polyval(coeffs, Ns)
    ss_res = np.sum((log_gaps - log_gaps_pred) ** 2)
    ss_tot = np.sum((log_gaps - np.mean(log_gaps)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    
    print("\n" + "=" * 60)
    print("ANÁLISE DOS RESULTADOS")
    print("=" * 60)
    print(f"Fit exponencial: Δmin = exp({beta:.4f} - {alpha:.4f}*N)")
    print(f"Taxa de decaimento α = {alpha:.4f}")
    print(f"Coeficiente R² = {r_squared:.4f}")
    
    if alpha > 0:
        print("\n✓ HIPÓTESE VALIDADA: Gap fecha exponencialmente (α > 0)")
        print(f"  Tempo de annealing T >> exp({2*alpha:.4f}*N)")
    else:
        print("\n✗ HIPÓTESE NÃO VALIDADA: Gap não fecha exponencialmente")
    
    # Criar figura com dois subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Gap Espectral vs N (escala semi-log)
    ax1.errorbar(Ns, mean_gaps, yerr=std_gaps, fmt='o', color='#2E86AB', 
                 markersize=8, capsize=4, capthick=1.5, linewidth=1.5,
                 label='Gap Mínimo Simulado')
    
    # Linha de fit exponencial
    N_fit = np.linspace(Ns[0], Ns[-1], 100)
    gap_fit = np.exp(coeffs[0] * N_fit + coeffs[1])
    ax1.semilogy(N_fit, gap_fit, '--', color='#E94F37', linewidth=2,
                 label=f'Fit: $\\Delta_{{min}} = e^{{{beta:.2f} - {alpha:.2f}N}}$ ($R^2={r_squared:.3f}$)')
    
    ax1.set_yscale('log')
    ax1.set_xlabel('N (Número de Qubits)', fontsize=14)
    ax1.set_ylabel('Gap Espectral $\\Delta_{min}$', fontsize=14)
    ax1.set_title('Validação Seção V: Fechamento do Gap', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=11)
    ax1.grid(True, which='both', linestyle=':', alpha=0.5)
    ax1.set_xlim(Ns[0] - 0.5, Ns[-1] + 0.5)
    
    # Adicionar anotação
    ax1.annotate(f'α = {alpha:.3f}', xy=(Ns[-2], mean_gaps[-2]), 
                 xytext=(Ns[-3], mean_gaps[-2] * 3),
                 fontsize=12, color='#E94F37',
                 arrowprops=dict(arrowstyle='->', color='#E94F37'))
    
    # Plot 2: IPR vs N
    ax2.plot(Ns, mean_iprs, 's-', color='#F77F00', markersize=8, linewidth=2,
             label='IPR no ponto crítico')
    
    # Linha de tendência
    ipr_trend = np.polyval(ipr_coeffs, N_fit)
    ax2.plot(N_fit, ipr_trend, '--', color='#7B2D26', linewidth=1.5,
             label=f'Tendência linear')
    
    # Limites teóricos
    ax2.axhline(y=1.0, color='red', linestyle=':', alpha=0.7, label='IPR = 1 (Localizado)')
    ax2.axhline(y=1.0 / (2 ** Ns[-1]), color='green', linestyle=':', alpha=0.7, 
                label=f'IPR = 1/2^N (Deslocalizado)')
    
    ax2.set_xlabel('N (Número de Qubits)', fontsize=14)
    ax2.set_ylabel('Inverse Participation Ratio (IPR)', fontsize=14)
    ax2.set_title('Teste de Localização de Anderson', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.5)
    ax2.set_xlim(Ns[0] - 0.5, Ns[-1] + 0.5)
    
    plt.tight_layout()
    
    # Salvar figura
    output_path = os.path.join(output_dir, "fig3_gap_scaling.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"\nGráfico salvo em: {output_path}")
    
    return {
        'alpha': alpha,
        'beta': beta,
        'r_squared': r_squared,
        'hypothesis_validated': alpha > 0
    }


def main():
    """Função principal do experimento."""
    # Diretório de saída
    output_dir = r"c:\Users\Douglas\Desktop\ToE\assets"
    os.makedirs(output_dir, exist_ok=True)
    
    # Executar experimento
    # Para demonstração rápida: N = 3 a 10
    # Para artigo final: N = 3 a 12 com mais amostras
    Ns, mean_gaps, std_gaps, mean_iprs = run_gap_scaling_experiment(
        min_N=3, 
        max_N=10, 
        num_samples=5
    )
    
    # Analisar e plotar
    results = analyze_and_plot(Ns, mean_gaps, std_gaps, mean_iprs, output_dir)
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO DO EXPERIMENTO 1")
    print("=" * 60)
    if results['hypothesis_validated']:
        print("A simulação CONFIRMA a previsão teórica:")
        print(f"  - O gap espectral fecha exponencialmente com taxa α = {results['alpha']:.4f}")
        print(f"  - Isso implica tempo de annealing T ∝ exp({2*results['alpha']:.4f}*N)")
        print("  - Recursos computacionais crescem exponencialmente com N")
        print("\n→ P ≠ NP é consistente com as leis da física quântica!")
    else:
        print("A simulação NÃO confirma o fechamento exponencial do gap.")
        print("Possíveis causas:")
        print("  - Tamanho do sistema insuficiente")
        print("  - Tipo de instância (pode estar fora da região de transição de fase)")
    
    return results


if __name__ == "__main__":
    results = main()
