#!/usr/bin/env python3
"""
EXEMPLOS AVANÇADOS DE USO - SISTEMA V3.0
Demonstração dos novos recursos implementados baseados no fine-tuning
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def exemplo_basico_simulacao():
    """
    Exemplo básico de simulação usando o sistema V3.0
    """
    print("🚀 Exemplo 1: Simulação Básica com Métodos Avançados")
    print("=" * 60)

    from main_physics_test_v2 import PhysicsTestSystemV3

    # Inicializar sistema
    system = PhysicsTestSystemV3()

    # Executar simulação
    results = system.run_complete_simulation()

    if results.get('simulation_success'):
        print("✅ Simulação concluída!"        print(f"📊 Pontos simulados: {results['total_points']}")
        print(f"🎯 Taxa de convergência: {results['convergence_rate']:.1%}")
        print(f"🔒 Validações aprovadas: {sum(results['validation_status'].values())}/5")
        print(f"📁 Resultados salvos em: {results['result_file']}")
    else:
        print("❌ Simulação falhou")

def exemplo_mecanica_quantica():
    """
    Exemplo de simulação de mecânica quântica usando diferenças finitas
    """
    print("\n🔬 Exemplo 2: Mecânica Quântica - Poço de Potencial")
    print("=" * 60)

    from main_physics_test_v2 import PhysicsTestSystemV3

    system = PhysicsTestSystemV3()

    # Definir potencial (poço quadrado)
    def square_well_potential(x):
        if -1 < x < 1:
            return 0  # Dentro do poço
        else:
            return 1000  # Fora do poço (barreira infinita)

    # Executar simulação QM
    results_qm = system.run_quantum_mechanics_simulation(
        potential_func=square_well_potential,
        x_range=(-2, 2),
        n_points=1000
    )

    print("✅ Simulação QM concluída!"    print(f"📊 Energias calculadas: {results_qm['energies'][:5]}")
    print(f"🔬 Função de onda ground state normalizada: {np.max(results_qm['wavefunctions'][:, 0]):.6f}")

    # Plotar resultados
    plt.figure(figsize=(12, 8))

    # Potencial
    plt.subplot(2, 2, 1)
    plt.plot(results_qm['x'], results_qm['potential'], 'k-', linewidth=2)
    plt.title('Potencial V(x)')
    plt.xlabel('x')
    plt.ylabel('V(x)')
    plt.grid(True)

    # Funções de onda
    plt.subplot(2, 2, 2)
    for i in range(min(3, len(results_qm['energies']))):
        plt.plot(results_qm['x'], results_qm['wavefunctions'][:, i]**2,
                label=f'n={i+1}, E={results_qm["energies"][i]:.3f}')
    plt.title('Densidade de Probabilidade |ψ|²')
    plt.xlabel('x')
    plt.ylabel('|ψ|²')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('resultados/quantum_mechanics_example.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("📁 Gráfico salvo em: resultados/quantum_mechanics_example.png")

def exemplo_monte_carlo():
    """
    Exemplo de simulação Monte Carlo para sistema físico
    """
    print("\n🎲 Exemplo 3: Monte Carlo - Oscilador Harmônico Clássico")
    print("=" * 60)

    from main_physics_test_v2 import PhysicsTestSystemV3

    system = PhysicsTestSystemV3()

    # Executar simulação Monte Carlo
    results_mc = system.run_monte_carlo_simulation(
        n_particles=500,
        temperature=1.0,  # Temperatura reduzida
        box_size=5.0,
        n_steps=50000
    )

    print("✅ Simulação Monte Carlo concluída!"    print(f"📊 Partículas simuladas: {len(results_mc['final_positions'])}")
    print(f"🌡️ Temperatura: {results_mc['temperature']} K")
    print(f"📦 Tamanho da caixa: {results_mc['box_size']}")
    print(f"🎯 Energia média final: {np.mean(results_mc['energy_history'][-1000:]):.6f}")

    # Plotar resultados
    plt.figure(figsize=(12, 6))

    # Posições finais
    plt.subplot(1, 2, 1)
    plt.scatter(results_mc['final_positions'][:, 0],
               results_mc['final_positions'][:, 1],
               alpha=0.6, s=2)
    plt.title('Posições Finais das Partículas')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.grid(True)

    # Histórico de energia
    plt.subplot(1, 2, 2)
    plt.plot(results_mc['energy_history'], alpha=0.7)
    plt.title('Evolução da Energia Total')
    plt.xlabel('Passo Monte Carlo')
    plt.ylabel('Energia')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('resultados/monte_carlo_example.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("📁 Gráfico salvo em: resultados/monte_carlo_example.png")

def exemplo_benchmarking():
    """
    Exemplo de benchmarking entre diferentes métodos numéricos
    """
    print("\n📊 Exemplo 4: Benchmarking de Métodos Numéricos")
    print("=" * 60)

    from main_physics_test_v2 import PhysicsTestSystemV3

    system = PhysicsTestSystemV3()

    # Definir casos de teste
    test_cases = {
        'caso_basico': {'time_range': (0, 100), 'n_points': 500},
        'caso_intermediario': {'time_range': (0, 500), 'n_points': 1000},
        'caso_avancado': {'time_range': (0, 1000), 'n_points': 2000}
    }

    print("🔬 Executando benchmarking...")
    benchmark_results = system.benchmark_multiple_methods(test_cases)

    print("✅ Benchmarking concluído!")
    print("\n📈 RESULTADOS DO BENCHMARKING:")
    print("-" * 40)

    for method, cases in benchmark_results.items():
        print(f"\n🔧 Método: {method.upper()}")
        for case_name, metrics in cases.items():
            if metrics:  # Verificar se há dados
                print(f"  📊 {case_name}:")
                print(f"    ⏱️ Tempo: {metrics.get('time', 'N/A'):.4f}s")
                print(f"    🎯 Precisão: {metrics.get('accuracy', 'N/A')}")
                print(f"    🛡️ Estabilidade: {'✅' if metrics.get('stability', False) else '❌'}")

def exemplo_validacao_rigorosa():
    """
    Exemplo de validação rigorosa dos resultados
    """
    print("\n🔍 Exemplo 5: Validação Rigorosa dos Resultados")
    print("=" * 60)

    from main_physics_test_v2 import PhysicsTestSystemV3, SimulationResults

    system = PhysicsTestSystemV3()

    # Criar resultados simulados para demonstração
    dummy_results = SimulationResults(
        timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"),
        constants_history={
            'G': np.random.normal(6.67430e-11, 1e-12, 1000),
            'c': np.random.normal(299792458, 1, 1000),
            'h': np.random.normal(6.62607015e-34, 1e-35, 1000),
            'alpha': np.random.normal(7.2973525693e-3, 1e-6, 1000)
        },
        tardis_compression=np.exp(np.linspace(0, 5, 1000)),
        time_array=np.linspace(0, 1000, 1000),
        convergence_metrics={'convergence_rate': 0.998, 'method': 'DOP853'},
        validation_results={}
    )

    print("🔬 Executando validação rigorosa...")
    validation_results = system.validate_simulation_results(dummy_results)

    print("✅ Validação concluída!")
    print("\n📋 RESULTADOS DA VALIDAÇÃO:")
    print("-" * 30)

    for criterio, status in validation_results.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {criterio.replace('_', ' ').title()}: {'APROVADO' if status else 'REPROVADO'}")

    print(f"\n📊 Status geral: {sum(validation_results.values())}/{len(validation_results)} critérios aprovados")

    # Mostrar métricas de validação
    print("
🔧 MÉTRICAS DO SISTEMA:"    print(f"  🎯 Taxa de convergência: {system.validation_metrics['convergence_rate']:.1%}")
    print(f"  🛡️ Estabilidade numérica: {'✅' if system.validation_metrics['numerical_stability'] else '❌'}")
    print(f"  ⚡ Conservação de energia: {'✅' if system.validation_metrics['energy_conservation'] else '❌'}")
    print(f"  🌌 Consistência física: {'✅' if system.validation_metrics['physical_consistency'] else '❌'}")

def main():
    """
    Executar todos os exemplos
    """
    print("🎓 EXEMPLOS AVANÇADOS DE USO - SISTEMA V3.0")
    print("Baseado no fine-tuning para IA em física teórica")
    print("=" * 80)

    try:
        exemplo_basico_simulacao()
        exemplo_mecanica_quantica()
        exemplo_monte_carlo()
        exemplo_benchmarking()
        exemplo_validacao_rigorosa()

        print("\n" + "=" * 80)
        print("🎉 TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("=" * 80)
        print("\n📚 Exemplos demonstrados:")
        print("  1. ✅ Simulação básica com métodos avançados")
        print("  2. ✅ Mecânica quântica com diferenças finitas")
        print("  3. ✅ Monte Carlo para sistemas físicos")
        print("  4. ✅ Benchmarking entre métodos numéricos")
        print("  5. ✅ Validação rigorosa dos resultados")
        print("\n📁 Arquivos gerados salvos em: resultados/")
        print("\n🔗 Consulte README.md para documentação completa")

    except Exception as e:
        print(f"\n❌ Erro durante execução dos exemplos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
