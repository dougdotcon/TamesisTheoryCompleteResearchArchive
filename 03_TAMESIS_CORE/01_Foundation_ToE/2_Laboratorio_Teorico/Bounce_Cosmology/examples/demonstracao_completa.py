#!/usr/bin/env python3
"""
Demonstração Completa do Framework de Física Computacional
Exemplo prático mostrando todas as funcionalidades implementadas

Este exemplo demonstra:
- Integração numérica avançada
- Simulações Monte Carlo
- Mecânica quântica computacional
- Relatividade geral numérica
- Cosmologia avançada
- Benchmarking e otimização
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import time

# Importar módulos do framework
from src.numerical_methods.integrators import IntegratorNumerico
from src.numerical_methods.monte_carlo import ModeloIsing2D, ConfiguracaoMonteCarlo
from src.numerical_methods.calculus import CalculoAvancado, FuncoesEspeciais
from src.numerical_methods.linear_algebra import AlgebraLinearFisica
from src.numerical_methods.differential_geometry import GeometriaDiferencial
from src.physics_models.quantum_mechanics import EquacaoSchrodinger, OsciladorHarmonicoQuantico
from src.physics_models.relativity import CosmologiaRelatividade, BuracosNegros
from src.physics_models.cosmology import modelo_lcdm, potencial_chaotic, InflacaoCosmica
from src.numerical_methods.benchmarking import BenchmarkSuite, OtimizacaoAutomatica


def demonstracao_integracao_numerica():
    """
    Demonstração de métodos de integração numérica avançados
    """
    print("🔢 Demonstração 1: Integração Numérica Avançada")
    print("-" * 50)

    # Sistema: Oscilador harmônico amortecido
    def sistema_oscilador(t, y):
        omega = 2 * np.pi  # Frequência
        gamma = 0.1       # Amortecimento
        return np.array([
            y[1],
            -2 * gamma * y[1] - omega**2 * y[0]
        ])

    # Condições iniciais
    y0 = np.array([1.0, 0.0])  # x(0) = 1, v(0) = 0
    t_span = (0, 10)

    # Integração com validação
    integrator = IntegratorNumerico(rtol=1e-10, atol=1e-12)

    print("Integrando sistema oscilador amortecido...")
    resultado = integrator.integrar_sistema(sistema_oscilador, y0, t_span)

    if resultado['sucesso']:
        print("✅ Integração bem-sucedida!")
        print(f"   Número de passos: {resultado['metricas_qualidade']['numero_passos']}")
        print(f"   Precisão alcançada: {resultado['metricas_qualidade']['precisao_alcancada']:.2e}")

        # Plot dos resultados
        t_eval = np.linspace(t_span[0], t_span[1], 1000)
        y_eval = np.array([resultado['solucao'].sol(t) for t in t_eval])

        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.plot(t_eval, y_eval[:, 0], 'b-', linewidth=2, label='Posição')
        plt.xlabel('Tempo')
        plt.ylabel('x(t)')
        plt.title('Posição vs Tempo')
        plt.grid(True, alpha=0.3)
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(y_eval[:, 0], y_eval[:, 1], 'r-', linewidth=1)
        plt.xlabel('x')
        plt.ylabel('dx/dt')
        plt.title('Trajetória de Fase')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('resultados/demonstracao_integracao.png', dpi=300, bbox_inches='tight')
        plt.close()

        print("📊 Gráfico salvo em: resultados/demonstracao_integracao.png")

    return resultado


def demonstracao_monte_carlo():
    """
    Demonstração de simulações Monte Carlo
    """
    print("\n🎲 Demonstração 2: Simulações Monte Carlo")
    print("-" * 45)

    # Configuração para modelo de Ising
    config = ConfiguracaoMonteCarlo(
        tamanho_sistema=(20, 20),
        temperatura=2.0,  # Próximo da temperatura crítica (Tc ≈ 2.27)
        n_sweeps=1000,
        n_thermalizacao=100,
        campo_externo=0.0
    )

    print("Executando simulação Monte Carlo do modelo de Ising...")
    print(f"Sistema: {config.tamanho_sistema[0]}x{config.tamanho_sistema[1]}")
    print(f"Temperatura: {config.temperatura}")
    print(f"Sweeps: {config.n_sweeps}")

    modelo = ModeloIsing2D(config)

    start_time = time.time()
    resultados = modelo.executar_simulacao(verbose=False)
    end_time = time.time()

    print("✅ Simulação concluída!")
    print(".2f"
    print(".6f"
    print(".6f"
    print(".6f"

    # Visualização da configuração final
    plt.figure(figsize=(8, 6))
    plt.imshow(resultados['configuracao_final'], cmap='RdYlBu', origin='lower')
    plt.colorbar(label='Spin')
    plt.title(f'Configuração Final - T = {config.temperatura}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('resultados/demonstracao_ising.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("📊 Gráfico salvo em: resultados/demonstracao_ising.png")

    return resultados


def demonstracao_mecanica_quantica():
    """
    Demonstração de mecânica quântica computacional
    """
    print("\n⚛️ Demonstração 3: Mecânica Quântica Computacional")
    print("-" * 55)

    # Oscilador harmônico quântico
    print("Resolvendo oscilador harmônico quântico...")
    osc = OsciladorHarmonicoQuantico(omega=1.0)

    # Comparação analítica vs numérica
    comparacao = osc.comparar_analitico_numerico(n_max=3)

    print("Energias calculadas:")
    print("Estado | Analítica | Numérica  | Erro")
    print("-" * 35)

    for n in range(4):
        analit = comparacao['energias_analiticas'][n]
        numer = comparacao['energias_numericas'][n]
        erro = comparacao['erros_energia'][n]
        print("5d"
              "6.3f"
              "6.3f"
              "6.2e")

    # Plot das funções de onda
    x = comparacao['x']
    plt.figure(figsize=(12, 8))

    for n in range(3):
        plt.subplot(3, 2, 2*n + 1)
        plt.plot(x, comparacao['wavefunctions_analiticas'][n], 'b-', linewidth=2, label='Analítica')
        plt.plot(x, comparacao['wavefunctions_numericas'][:, n], 'r--', linewidth=2, label='Numérica')
        plt.xlabel('x')
        plt.ylabel(f'ψ_{n}(x)')
        plt.title(f'Estado Fundamental n={n}')
        plt.grid(True, alpha=0.3)
        plt.legend()

        plt.subplot(3, 2, 2*n + 2)
        erro_local = np.abs(comparacao['wavefunctions_analiticas'][n] - comparacao['wavefunctions_numericas'][:, n])
        plt.semilogy(x, erro_local, 'g-', linewidth=2)
        plt.xlabel('x')
        plt.ylabel('Erro absoluto')
        plt.title(f'Erro Local n={n}')
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('resultados/demonstracao_quantica.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("📊 Gráfico salvo em: resultados/demonstracao_quantica.png")

    return comparacao


def demonstracao_relatividade():
    """
    Demonstração de relatividade geral
    """
    print("\n🌌 Demonstração 4: Relatividade Geral")
    print("-" * 40)

    # Cosmologia LCDM
    print("Evolução cosmológica no modelo ΛCDM...")
    cosmo = CosmologiaRelatividade(H0=70, Omega_m=0.3, Omega_lambda=0.7)

    # Calcular idade do universo
    idade = cosmo.idade_universo()
    print(f"Idade do universo: {idade:.2f} Gyr")

    # Evolução do universo
    evol = cosmo.evoluir_universo(a_inicial=0.01, a_final=1.0, n_pontos=200)

    if evol['sucesso']:
        print("✅ Evolução cosmológica calculada!")

        # Plot da evolução
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 3, 1)
        plt.plot(evol['t'], evol['a'], 'b-', linewidth=2)
        plt.xlabel('Tempo (Gyr)')
        plt.ylabel('a(t)')
        plt.title('Fator de Escala')
        plt.grid(True, alpha=0.3)

        plt.subplot(1, 3, 2)
        plt.plot(evol['a'], evol['H'], 'r-', linewidth=2)
        plt.xlabel('a')
        plt.ylabel('H(a)')
        plt.title('Parâmetro de Hubble')
        plt.grid(True, alpha=0.3)
        plt.xscale('log')
        plt.yscale('log')

        plt.subplot(1, 3, 3)
        z = 1/evol['a'] - 1
        plt.plot(z, evol['H'], 'g-', linewidth=2)
        plt.xlabel('z (redshift)')
        plt.ylabel('H(z)')
        plt.title('Expansão Observada')
        plt.grid(True, alpha=0.3)
        plt.xscale('log')
        plt.yscale('log')

        plt.tight_layout()
        plt.savefig('resultados/demonstracao_cosmo.png', dpi=300, bbox_inches='tight')
        plt.close()

        print("📊 Gráfico salvo em: resultados/demonstracao_cosmo.png")

    # Física de buracos negros
    print("\nBuracos Negros:")
    bh = BuracosNegros()

    # Raios de Schwarzschild para diferentes objetos
    objetos = [
        ("Sol", 1.0),
        ("Sagitário A*", 4.1e6),
        ("Buraco negro supermassivo", 1e9)
    ]

    print("Objeto | Massa (M_sun) | Raio Schwarzschild (km)")
    print("-" * 50)

    for nome, massa in objetos:
        R_s = bh.raio_schwarzschild(massa)
        print("20s"
              ".1e"
              ".1e")

    return evol if 'evol' in locals() else None


def demonstracao_benchmarking():
    """
    Demonstração de benchmarking e otimização
    """
    print("\n⚡ Demonstração 5: Benchmarking e Otimização")
    print("-" * 48)

    # Criar suite de benchmarks
    benchmark = BenchmarkSuite()

    # Sistema de teste: Oscilador duplo
    def sistema_duplo(t, y):
        # Dois osciladores acoplados
        omega1, omega2 = 1.0, 1.5
        k = 0.1  # Acoplamento

        return np.array([
            y[1],
            -omega1**2 * y[0] - k * (y[0] - y[2]),
            y[3],
            -omega2**2 * y[2] - k * (y[2] - y[0])
        ])

    y0 = np.array([1.0, 0.0, 0.5, 0.0])
    t_span = (0, 20)

    # Benchmark de diferentes métodos
    print("Comparando métodos de integração...")
    metodos = ['RK45', 'RK23', 'DOP853']

    resultados = benchmark.benchmark_integradores(
        [('oscilador_duplo', sistema_duplo, y0, t_span)],
        metodos=metodos
    )

    # Análise dos resultados
    analise = benchmark.analisar_resultados(resultados)

    if 'erro' not in analise:
        print("\nResultados do Benchmark:")
        print(f"Taxa de sucesso: {analise['taxa_sucesso']:.1%}")
        print(f"Tempo médio: {analise['tempo_medio']:.4f} s")
        print(f"Método mais rápido: {analise['mais_rapido']}")
        print(f"Speedup máximo: {analise['tempo_max'] / analise['tempo_min']:.1f}x")

        # Comparação detalhada
        comparacao = benchmark.comparar_metodos('integracao')

        if 'erro' not in comparacao:
            print("\nComparação por método:")
            for metodo, stats in comparacao['comparacao_por_metodo'].items():
                print("10s"
                      ".4f"
                      ".4f"
                      ".1f")

    # Otimização automática
    print("\nOtimizando parâmetros automaticamente...")
    otimizador = OtimizacaoAutomatica()

    resultado_otimizacao = otimizador.otimizar_parametros_integracao(
        sistema_duplo, y0, t_span, metrica_otimizacao='tempo'
    )

    if 'erro' not in resultado_otimizacao:
        melhor = resultado_otimizacao['melhor_configuracao']
        print("Melhor configuração encontrada:")
        print(f"  Método: {melhor['metodo']}")
        print(f"  RTOL: {melhor['rtol']:.0e}")
        print(f"  ATOL: {melhor['atol']:.0e}")
        print(f"  Tempo: {resultado_otimizacao['tempo']:.4f} s")

    return benchmark.resultados


def demonstracao_funcoes_especiais():
    """
    Demonstração de funções especiais
    """
    print("\n🔬 Demonstração 6: Funções Especiais")
    print("-" * 40)

    calc = CalculoAvancado()

    # Teste de funções especiais
    x_vals = np.linspace(0.1, 3, 100)

    # Função erro
    erf_vals = [FuncoesEspeciais.funcao_erro(x) for x in x_vals]

    # Função Gamma
    gamma_vals = [FuncoesEspeciais.funcao_gamma(x) for x in x_vals]

    # Função de Bessel
    bessel_vals = [FuncoesEspeciais.funcao_bessel_primeira_ordem(0, x) for x in x_vals]

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(x_vals, erf_vals, 'b-', linewidth=2, label='erf(x)')
    plt.xlabel('x')
    plt.ylabel('erf(x)')
    plt.title('Função Erro')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.subplot(1, 3, 2)
    plt.plot(x_vals, gamma_vals, 'r-', linewidth=2, label='Γ(x)')
    plt.xlabel('x')
    plt.ylabel('Γ(x)')
    plt.title('Função Gamma')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.subplot(1, 3, 3)
    plt.plot(x_vals, bessel_vals, 'g-', linewidth=2, label='J₀(x)')
    plt.xlabel('x')
    plt.ylabel('J₀(x)')
    plt.title('Função de Bessel')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig('resultados/demonstracao_funcoes.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("📊 Gráfico salvo em: resultados/demonstracao_funcoes.png")

    # Teste de cálculo avançado
    def f_test(x):
        return np.sin(x**2)

    x_test = 1.5
    derivada_numerica = calc.derivada_numerica(f_test, x_test)
    derivada_analitica = 2 * x_test * np.cos(x_test**2)

            print("\nTeste de derivada numérica:")
        print(f"Ponto x = {x_test}")
        print(f"Derivada analítica: {derivada_analitica:.6f}")
        print(f"Derivada numérica:  {derivada_numerica:.6f}")
        print(f"Erro: {abs(derivada_analitica - derivada_numerica):.2e}")

        return {
            'x_vals': x_vals,
            'erf': erf_vals,
            'gamma': gamma_vals,
            'bessel': bessel_vals
        }


def main():
    """
    Função principal da demonstração
    """
    print("🚀 Demonstração Completa do Framework de Física Computacional")
    print("=" * 70)
    print("Este exemplo demonstra todas as funcionalidades implementadas")
    print("baseadas no fine-tuning de IA para física teórica.\n")

    start_time = time.time()

    # Executar todas as demonstrações
    resultados = {}

    try:
        # 1. Integração numérica
        resultados['integracao'] = demonstracao_integracao_numerica()

        # 2. Monte Carlo
        resultados['monte_carlo'] = demonstracao_monte_carlo()

        # 3. Mecânica quântica
        resultados['quantica'] = demonstracao_mecanica_quantica()

        # 4. Relatividade geral
        resultados['relatividade'] = demonstracao_relatividade()

        # 5. Benchmarking
        resultados['benchmarking'] = demonstracao_benchmarking()

        # 6. Funções especiais
        resultados['funcoes'] = demonstracao_funcoes_especiais()

        end_time = time.time()
        tempo_total = end_time - start_time

        print("
🎉 Demonstração Concluída com Sucesso!")
        print("=" * 70)
        print("📊 Resumo dos Resultados:")
        print(f"   ✅ Integração numérica: {resultados['integracao']['sucesso']}")
        print(f"   ✅ Simulação Monte Carlo: {'Sucesso' if resultados['monte_carlo'] else 'Falhou'}")
        print(f"   ✅ Mecânica quântica: {len(resultados['quantica']['erros_energia'])} estados calculados")
        print(f"   ✅ Relatividade geral: {'Sucesso' if resultados['relatividade'] and resultados['relatividade']['sucesso'] else 'Falhou'}")
        print(f"   ✅ Benchmarking: {len(resultados['benchmarking'])} testes executados")
        print(f"   ✅ Funções especiais: {len(resultados['funcoes']['x_vals'])} pontos calculados")
        print("
⏱️  Tempo total de execução: .2f")
        print("
📁 Gráficos salvos em: resultados/")
        print("   - demonstracao_integracao.png")
        print("   - demonstracao_ising.png")
        print("   - demonstracao_quantica.png")
        print("   - demonstracao_cosmo.png")
        print("   - demonstracao_funcoes.png")

        print("
🎯 Framework de Física Computacional Funcionando Perfeitamente!")
        print("   Baseado no fine-tuning de IA especializada")
        print("   Pronto para pesquisa avançada em física teórica!")

    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()

    return resultados


if __name__ == "__main__":
    # Executar demonstração completa
    resultados = main()

    # Salvar resumo dos resultados
    import json
    with open('resultados/resumo_demonstracao.json', 'w', encoding='utf-8') as f:
        # Preparar dados serializáveis
        resumo_serializavel = {}
        for chave, valor in resultados.items():
            if isinstance(valor, dict):
                resumo_serializavel[chave] = {}
                for k, v in valor.items():
                    if isinstance(v, np.ndarray):
                        resumo_serializavel[chave][k] = v.tolist()
                    elif isinstance(v, (int, float, str, bool, type(None))):
                        resumo_serializavel[chave][k] = v
                    # Ignorar outros tipos não serializáveis
            else:
                resumo_serializavel[chave] = str(valor)

        json.dump(resumo_serializavel, f, indent=2, ensure_ascii=False)

    print("\n📄 Resumo salvo em: resultados/resumo_demonstracao.json")
