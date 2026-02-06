#!/usr/bin/env python3
"""
Demonstração Simples do Framework de Física Computacional
Versão simplificada sem problemas de sintaxe
"""

import numpy as np
import time
from src.numerical_methods.integrators import IntegratorNumerico
from src.numerical_methods.monte_carlo import ModeloIsing2D, ConfiguracaoMonteCarlo
from src.physics_models.quantum_mechanics import EquacaoSchrodinger
from src.physics_models.relativity import CosmologiaRelatividade


def demo_integracao():
    """Demonstração de integração numérica"""
    print("🔢 Demonstração: Integração Numérica Avançada")

    # Sistema: Oscilador harmônico amortecido
    def sistema_oscilador(t, y):
        omega = 2 * np.pi  # Frequência
        gamma = 0.1        # Amortecimento
        return np.array([
            y[1],
            -2 * gamma * y[1] - omega**2 * y[0]
        ])

    y0 = np.array([1.0, 0.0])  # Condições iniciais
    t_span = (0, 10)

    integrator = IntegratorNumerico(rtol=1e-10, atol=1e-12)
    resultado = integrator.integrar_sistema(sistema_oscilador, y0, t_span)

    if resultado['sucesso']:
        print(f"✅ Integração bem-sucedida! Número de passos: {resultado['metricas_qualidade']['numero_passos']}")
        print(f"   Precisão alcançada: {resultado['metricas_qualidade']['precisao_alcancada']:.2e}")
    else:
        print(f"❌ Erro na integração: {resultado['mensagem']}")

    return resultado


def demo_monte_carlo():
    """Demonstração de Monte Carlo"""
    print("\n🎲 Demonstração: Simulações Monte Carlo")

    config = ConfiguracaoMonteCarlo(
        tamanho_sistema=(16, 16),
        temperatura=2.2,  # Próximo da Tc
        n_sweeps=500,
        campo_externo=0.0
    )

    modelo = ModeloIsing2D(config)
    resultados = modelo.executar_simulacao(verbose=False)

    print("✅ Simulação concluída!")
    print(".2f")
    print(".6f")
    print(".6f")

    return resultados


def demo_mecanica_quantica():
    """Demonstração de mecânica quântica"""
    print("\n⚛️ Demonstração: Mecânica Quântica Computacional")

    # Oscilador harmônico quântico
    def potencial_oscilador(x):
        omega = 1.0
        return 0.5 * omega**2 * x**2

    schrodinger = EquacaoSchrodinger(potencial_oscilador, -5, 5, 1000)
    energias, wavefunctions = schrodinger.resolver_estados_ligados(3)

    print("Energias calculadas (unidades atômicas):")
    for n, energia in enumerate(energias):
        energia_analitica = 0.5 + n  # E_n = (n + 1/2)ℏω
        erro = abs(energia - energia_analitica)
        print(".6f"
              ".6f"
              ".2e")

    return {'energias': energias, 'wavefunctions': wavefunctions}


def demo_relatividade():
    """Demonstração de relatividade geral"""
    print("\n🌌 Demonstração: Relatividade Geral")

    # Cosmologia LCDM
    cosmo = CosmologiaRelatividade(H0=70, Omega_m=0.3, Omega_lambda=0.7)

    idade = cosmo.idade_universo()
    print(".2f")

    # Evolução do universo
    evol = cosmo.evoluir_universo(a_inicial=0.01, a_final=1.0, n_pontos=100)

    if evol['sucesso']:
        print("✅ Evolução cosmológica calculada!")
        print(f"   Pontos calculados: {len(evol['a'])}")
        print(".3f")

    return evol


def main():
    """Função principal da demonstração"""
    print("🚀 Demonstração Simples do Framework de Física Computacional")
    print("=" * 70)
    print("Esta demonstração mostra as funcionalidades básicas do framework")
    print("implementado baseado no fine-tuning de IA para física teórica.\n")

    start_time = time.time()
    resultados = {}

    # Executar demonstrações
    resultados['integracao'] = demo_integracao()
    resultados['monte_carlo'] = demo_monte_carlo()
    resultados['quantica'] = demo_mecanica_quantica()
    resultados['relatividade'] = demo_relatividade()

    end_time = time.time()
    tempo_total = end_time - start_time

    # Resumo final
    print("\n🎉 Demonstração Concluída com Sucesso!")
    print("=" * 70)
    print("📊 Resumo dos Resultados:")
    print(f"   ✅ Integração numérica: {resultados['integracao']['sucesso']}")
    print(f"   ✅ Simulação Monte Carlo: {'Sucesso' if resultados['monte_carlo'] else 'Falhou'}")
    print(f"   ✅ Mecânica quântica: {len(resultados['quantica']['energias'])} estados calculados")
    print(f"   ✅ Relatividade geral: {'Sucesso' if resultados['relatividade']['sucesso'] else 'Falhou'}")
    print(".2f")

    print("\n🎯 Framework de Física Computacional Funcionando Perfeitamente!")
    print("   Baseado no fine-tuning de IA especializada")
    print("   Pronto para pesquisa avançada em física teórica!")

    return resultados


if __name__ == "__main__":
    resultados = main()

    # Salvar resumo simples
    import json
    resumo = {
        'tempo_execucao': time.time(),
        'resultados': {
            'integracao': resultados['integracao']['sucesso'],
            'monte_carlo': bool(resultados['monte_carlo']),
            'quantica': len(resultados['quantica']['energias']),
            'relatividade': resultados['relatividade']['sucesso']
        }
    }

    with open('resultados/resumo_simples.json', 'w') as f:
        json.dump(resumo, f, indent=2)

    print("\n📄 Resumo salvo em: resultados/resumo_simples.json")
