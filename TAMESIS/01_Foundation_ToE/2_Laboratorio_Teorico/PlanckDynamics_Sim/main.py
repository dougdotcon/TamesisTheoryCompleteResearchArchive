#!/usr/bin/env python3
"""
TESTE DE HIPÓTESES DE FÍSICA TEÓRICA
Época de Planck com Leis Dinâmicas e Universo TARDIS

Arquivo principal para executar as simulações validadas.
Utilize este arquivo como ponto de entrada principal do projeto.

Autor: Sistema de Simulação de Física Teórica
Data: Agosto 2025
"""

import sys
import os

# Adicionar pasta src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Função principal - executa simulação V3.0 avançada baseada em métodos numéricos"""

    print("=" * 80)
    print("SISTEMA AVANÇADO DE FÍSICA TEÓRICA V3.0")
    print("Simulação Computacional com Métodos Numéricos Avançados")
    print("=" * 80)
    print()
    print("🔬 Hipóteses testadas:")
    print("1. Leis físicas dinâmicas durante eventos supercosmicos")
    print("2. Universo TARDIS: compressão quântica espaço-temporal")
    print()
    print("🚀 Executando simulação V3.0 com:")
    print("   • Múltiplos métodos numéricos (Runge-Kutta, diferenças finitas)")
    print("   • Validação rigorosa e benchmarking")
    print("   • Estrutura modular e bem documentada")
    print("   • Integração com bibliotecas científicas")
    print()

    try:
        # Importar e executar simulador V3.0
        from main_physics_test_v2 import PhysicsTestSystemV3

        system = PhysicsTestSystemV3()
        results = system.run_complete_simulation()

        if results.get('simulation_success', False):
            print("\n" + "=" * 80)
            print("✅ SIMULAÇÃO V3.0 CONCLUÍDA COM SUCESSO!")
            print("=" * 80)
            print()
            print("📊 RESULTADOS PRINCIPAIS:")
            print(f"   • Pontos simulados: {results['total_points']}")
            print(f"   • Range temporal: {results['time_range'][0]:.0e} - {results['time_range'][1]:.0e}")
            print(f"   • Compressão final: {results['final_compression_factor']:.1f}x")
            print(".1%")
            print(f"   • Validações: {sum(results['validation_status'].values())}/{len(results['validation_status'])} ✅")
            print()
            print("📁 Arquivos gerados:")
            print(f"   • Resultados: {results['result_file']}")
            print(f"   • Visualizações: {results['visualization_file']}")
            print()
            print("🔬 NOVOS RECURSOS V3.0:")
            print("   • Mecânica quântica com diferenças finitas")
            print("   • Simulações Monte Carlo")
            print("   • Benchmarking de métodos numéricos")
            print("   • Validação rigorosa com métricas físicas")
            print()
            print("📖 Consulte README.md para documentação completa")

        else:
            print("❌ Simulação falhou. Verifique os logs acima.")
            error_msg = results.get('error', 'Erro desconhecido')
            print(f"Detalhes: {error_msg}")
            return 1

    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("Certifique-se de que todos os arquivos estão na pasta 'src/'")
        print("Execute: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
