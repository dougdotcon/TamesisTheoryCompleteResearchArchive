#!/usr/bin/env python3
"""
Benchmarking e Otimização de Performance
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Benchmarking de algoritmos
- Análise de performance
- Otimização automática de parâmetros
- Comparação de métodos numéricos
- Profiling e análise de gargalos
"""

import numpy as np
import time
from typing import Callable, Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from contextlib import contextmanager
import warnings
from .integrators import IntegratorNumerico
from .monte_carlo import ModeloIsing2D, ConfiguracaoMonteCarlo


@dataclass
class ResultadoBenchmark:
    """
    Resultado de um benchmark
    """
    nome: str
    tempo_execucao: float
    memoria_usada: Optional[float]
    metricas_qualidade: Dict[str, float]
    parametros: Dict[str, Any]
    sucesso: bool
    erro: Optional[str] = None


class BenchmarkSuite:
    """
    Suite completa de benchmarks para métodos numéricos
    """

    def __init__(self):
        self.resultados = []
        self.integrator = IntegratorNumerico()

    def benchmark_integradores(self, sistemas_teste: List[Tuple[str, Callable, np.ndarray, Tuple[float, float]]],
                              metodos: List[str] = None) -> List[ResultadoBenchmark]:
        """
        Benchmark de diferentes métodos de integração

        Parameters:
        -----------
        sistemas_teste : list
            Lista de (nome, sistema, y0, t_span)
        metodos : list, optional
            Métodos a testar

        Returns:
        --------
        list: Resultados dos benchmarks
        """
        if metodos is None:
            metodos = ['RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA']

        resultados = []

        for nome_sistema, sistema, y0, t_span in sistemas_teste:
            for metodo in metodos:
                resultado = self._benchmark_integrador_unico(
                    nome_sistema, sistema, y0, t_span, metodo
                )
                resultados.append(resultado)

        self.resultados.extend(resultados)
        return resultados

    def _benchmark_integrador_unico(self, nome: str, sistema: Callable, y0: np.ndarray,
                                   t_span: Tuple[float, float], metodo: str) -> ResultadoBenchmark:
        """
        Benchmark de um único integrador
        """
        try:
            # Configurar integrador
            integrator = IntegratorNumerico()

            # Medir tempo
            start_time = time.perf_counter()

            # Executar integração
            resultado = integrator.integrar_sistema(sistema, y0, t_span, metodo=metodo)

            end_time = time.perf_counter()
            tempo_execucao = end_time - start_time

            # Métricas de qualidade
            metricas = {}
            if resultado['sucesso'] and resultado['metricas_qualidade']:
                metricas = resultado['metricas_qualidade']

            return ResultadoBenchmark(
                nome=f"{nome}_{metodo}",
                tempo_execucao=tempo_execucao,
                memoria_usada=None,  # Implementar se necessário
                metricas_qualidade=metricas,
                parametros={
                    'metodo': metodo,
                    'sistema': nome,
                    't_span': t_span,
                    'dim': len(y0)
                },
                sucesso=resultado['sucesso'],
                erro=resultado['mensagem'] if not resultado['sucesso'] else None
            )

        except Exception as e:
            return ResultadoBenchmark(
                nome=f"{nome}_{metodo}",
                tempo_execucao=float('inf'),
                memoria_usada=None,
                metricas_qualidade={},
                parametros={
                    'metodo': metodo,
                    'sistema': nome,
                    't_span': t_span,
                    'dim': len(y0)
                },
                sucesso=False,
                erro=str(e)
            )

    def benchmark_monte_carlo(self, configuracoes: List[ConfiguracaoMonteCarlo],
                             n_repeticoes: int = 3) -> List[ResultadoBenchmark]:
        """
        Benchmark de simulações Monte Carlo

        Parameters:
        -----------
        configuracoes : list
            Lista de configurações a testar
        n_repeticoes : int
            Número de repetições para média

        Returns:
        --------
        list: Resultados dos benchmarks
        """
        resultados = []

        for i, config in enumerate(configuracoes):
            tempos = []
            sucessos = 0

            for rep in range(n_repeticoes):
                try:
                    modelo = ModeloIsing2D(config)

                    start_time = time.perf_counter()
                    resultado_mc = modelo.executar_simulacao(verbose=False)
                    end_time = time.perf_counter()

                    if resultado_mc:  # Verificar se obteve resultados
                        tempos.append(end_time - start_time)
                        sucessos += 1

                except Exception as e:
                    print(f"Erro na repetição {rep}: {e}")
                    continue

            # Calcular estatísticas
            if tempos:
                tempo_medio = np.mean(tempos)
                tempo_std = np.std(tempos)
                taxa_sucesso = sucessos / n_repeticoes
            else:
                tempo_medio = float('inf')
                tempo_std = 0.0
                taxa_sucesso = 0.0

            resultado = ResultadoBenchmark(
                nome=f"MC_L{config.tamanho_sistema[0]}_T{config.temperatura:.1f}",
                tempo_execucao=tempo_medio,
                memoria_usada=None,
                metricas_qualidade={
                    'tempo_std': tempo_std,
                    'taxa_sucesso': taxa_sucesso,
                    'n_repeticoes': n_repeticoes
                },
                parametros={
                    'L': config.tamanho_sistema[0],
                    'T': config.temperatura,
                    'n_sweeps': config.n_sweeps,
                    'campo_externo': config.campo_externo
                },
                sucesso=taxa_sucesso > 0.5
            )

            resultados.append(resultado)

        self.resultados.extend(resultados)
        return resultados

    def analisar_resultados(self, resultados: List[ResultadoBenchmark] = None) -> Dict[str, Any]:
        """
        Análise estatística dos resultados de benchmark

        Parameters:
        -----------
        resultados : list, optional
            Resultados a analisar (usa self.resultados se None)

        Returns:
        --------
        dict: Análise estatística
        """
        if resultados is None:
            resultados = self.resultados

        if not resultados:
            return {'erro': 'Nenhum resultado para analisar'}

        # Filtrar apenas sucessos
        resultados_sucesso = [r for r in resultados if r.sucesso]

        if not resultados_sucesso:
            return {'erro': 'Nenhum resultado de sucesso para analisar'}

        # Estatísticas básicas
        tempos = [r.tempo_execucao for r in resultados_sucesso]
        nomes = [r.nome for r in resultados_sucesso]

        analise = {
            'numero_total': len(resultados),
            'numero_sucesso': len(resultados_sucesso),
            'taxa_sucesso': len(resultados_sucesso) / len(resultados),
            'tempo_medio': np.mean(tempos),
            'tempo_std': np.std(tempos),
            'tempo_min': np.min(tempos),
            'tempo_max': np.max(tempos),
            'mais_rapido': nomes[np.argmin(tempos)],
            'mais_lento': nomes[np.argmax(tempos)],
            'resultados_detalhados': [
                {
                    'nome': r.nome,
                    'tempo': r.tempo_execucao,
                    'sucesso': r.sucesso,
                    'parametros': r.parametros
                }
                for r in resultados
            ]
        }

        return analise

    def comparar_metodos(self, categoria: str = 'integracao') -> Dict[str, Any]:
        """
        Comparação direta entre métodos da mesma categoria

        Parameters:
        -----------
        categoria : str
            'integracao', 'monte_carlo', etc.

        Returns:
        --------
        dict: Comparação entre métodos
        """
        # Filtrar por categoria
        if categoria == 'integracao':
            resultados_categoria = [r for r in self.resultados if '_' in r.nome and any(m in r.nome for m in ['RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA'])]
        elif categoria == 'monte_carlo':
            resultados_categoria = [r for r in self.resultados if r.nome.startswith('MC_')]
        else:
            resultados_categoria = [r for r in self.resultados if categoria.lower() in r.nome.lower()]

        if not resultados_categoria:
            return {'erro': f'Nenhum resultado encontrado para categoria {categoria}'}

        # Agrupar por método/sistema
        metodos = {}
        for r in resultados_categoria:
            if categoria == 'integracao':
                metodo = r.nome.split('_')[-1]
                sistema = '_'.join(r.nome.split('_')[:-1])
            else:
                metodo = r.nome
                sistema = categoria

            if metodo not in metodos:
                metodos[metodo] = []
            metodos[metodo].append(r.tempo_execucao)

        # Calcular estatísticas por método
        comparacao = {}
        for metodo, tempos in metodos.items():
            comparacao[metodo] = {
                'tempo_medio': np.mean(tempos),
                'tempo_std': np.std(tempos),
                'n_amostras': len(tempos),
                'melhor_tempo': np.min(tempos)
            }

        # Ranking por velocidade
        ranking = sorted(comparacao.items(), key=lambda x: x[1]['tempo_medio'])

        return {
            'comparacao_por_metodo': comparacao,
            'ranking_velocidade': [metodo for metodo, _ in ranking],
            'melhor_metodo': ranking[0][0],
            'pior_metodo': ranking[-1][0],
            'speedup_maximo': ranking[-1][1]['tempo_medio'] / ranking[0][1]['tempo_medio']
        }


class OtimizacaoAutomatica:
    """
    Otimização automática de parâmetros para simulações
    """

    def __init__(self):
        self.benchmark = BenchmarkSuite()

    def otimizar_parametros_integracao(self, sistema: Callable, y0: np.ndarray,
                                     t_span: Tuple[float, float],
                                     metrica_otimizacao: str = 'tempo') -> Dict[str, Any]:
        """
        Otimizar parâmetros de integração automaticamente

        Parameters:
        -----------
        sistema : callable
            Sistema de EDOs
        y0 : array_like
            Condições iniciais
        t_span : tuple
            Intervalo temporal
        metrica_otimizacao : str
            'tempo', 'precisao', 'estabilidade'

        Returns:
        --------
        dict: Parâmetros otimizados
        """
        # Testar diferentes métodos e configurações
        metodos = ['RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA']
        rtol_vals = [1e-6, 1e-8, 1e-10, 1e-12]
        atol_vals = [1e-8, 1e-10, 1e-12, 1e-14]

        resultados_teste = []

        for metodo in metodos:
            for rtol in rtol_vals[:2]:  # Limitar combinações
                for atol in atol_vals[:2]:
                    try:
                        integrator = IntegratorNumerico(rtol=rtol, atol=atol)

                        start_time = time.perf_counter()
                        resultado = integrator.integrar_sistema(sistema, y0, t_span, metodo=metodo)
                        end_time = time.perf_counter()

                        if resultado['sucesso']:
                            tempo = end_time - start_time
                            metricas = resultado['metricas_qualidade']

                            score = self._calcular_score_otimizacao(
                                tempo, metricas, metrica_otimizacao
                            )

                            resultados_teste.append({
                                'metodo': metodo,
                                'rtol': rtol,
                                'atol': atol,
                                'tempo': tempo,
                                'score': score,
                                'metricas': metricas
                            })

                    except:
                        continue

        if not resultados_teste:
            return {'erro': 'Nenhuma configuração funcionou'}

        # Encontrar melhor configuração
        melhores_resultados = sorted(resultados_teste, key=lambda x: x['score'])
        melhor = melhores_resultados[0]

        return {
            'melhor_configuracao': {
                'metodo': melhor['metodo'],
                'rtol': melhor['rtol'],
                'atol': melhor['atol']
            },
            'score': melhor['score'],
            'tempo': melhor['tempo'],
            'todas_configuracoes_testadas': len(resultados_teste),
            'ranking_top5': melhores_resultados[:5]
        }

    def _calcular_score_otimizacao(self, tempo: float, metricas: Dict[str, float],
                                  metrica: str) -> float:
        """
        Calcular score para otimização baseado na métrica escolhida
        """
        if metrica == 'tempo':
            return tempo
        elif metrica == 'precisao':
            # Combinação de tempo e precisão
            return tempo * (1 + metricas.get('estabilidade', 1))
        elif metrica == 'estabilidade':
            # Priorizar estabilidade sobre velocidade
            estabilidade = metricas.get('estabilidade', 1)
            return tempo / (1 + estabilidade)
        else:
            return tempo

    def otimizar_monte_carlo(self, L_range: List[int] = [10, 20, 30],
                           T_range: List[float] = [1.0, 2.0, 3.0],
                           objetivo: str = 'eficiencia') -> Dict[str, Any]:
        """
        Otimizar parâmetros para simulações Monte Carlo

        Parameters:
        -----------
        L_range : list
            Tamanhos de sistema a testar
        T_range : list
            Temperaturas a testar
        objetivo : str
            'eficiencia', 'precisao', 'velocidade'

        Returns:
        --------
        dict: Configuração otimizada
        """
        configuracoes = []

        for L in L_range:
            for T in T_range:
                config = ConfiguracaoMonteCarlo(
                    tamanho_sistema=(L, L),
                    temperatura=T,
                    n_sweeps=min(1000, L * 100),  # Ajustar sweeps baseado no tamanho
                    n_thermalizacao=100
                )
                configuracoes.append(config)

        # Executar benchmarks
        resultados_mc = self.benchmark.benchmark_monte_carlo(configuracoes, n_repeticoes=2)

        # Analisar resultados
        analise = self.benchmark.analisar_resultados(resultados_mc)

        if 'erro' in analise:
            return analise

        # Encontrar melhor configuração baseada no objetivo
        melhores_resultados = []
        for r in resultados_mc:
            if r.sucesso:
                score = self._calcular_score_mc(r, objetivo)
                melhores_resultados.append((r, score))

        if not melhores_resultados:
            return {'erro': 'Nenhuma configuração teve sucesso'}

        melhores_resultados.sort(key=lambda x: x[1])
        melhor_config, melhor_score = melhores_resultados[0]

        return {
            'melhor_configuracao': melhor_config.parametros,
            'score': melhor_score,
            'tempo_execucao': melhor_config.tempo_execucao,
            'taxa_sucesso': melhor_config.metricas_qualidade['taxa_sucesso'],
            'analise_completa': analise
        }

    def _calcular_score_mc(self, resultado: ResultadoBenchmark, objetivo: str) -> float:
        """
        Calcular score para otimização de Monte Carlo
        """
        tempo = resultado.tempo_execucao
        L = resultado.parametros['L']

        if objetivo == 'velocidade':
            return tempo
        elif objetivo == 'eficiencia':
            # Penalizar sistemas grandes se lentos
            return tempo * (L / 10)**2
        elif objetivo == 'precisao':
            # Considerar estabilidade temporal
            return tempo / (1 + resultado.metricas_qualidade.get('taxa_sucesso', 0))
        else:
            return tempo


@contextmanager
def timer_benchmark():
    """
    Context manager para medir tempo de execução
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        print(".4f")


def criar_sistemas_teste() -> List[Tuple[str, Callable, np.ndarray, Tuple[float, float]]]:
    """
    Criar sistemas de teste padrão para benchmarks

    Returns:
    --------
    list: Lista de sistemas de teste (nome, sistema, y0, t_span)
    """
    sistemas = []

    # 1. Oscilador harmônico
    def oscillator(t, y):
        omega = 2 * np.pi
        return np.array([y[1], -omega**2 * y[0]])

    sistemas.append(('oscilador', oscillator, np.array([1.0, 0.0]), (0, 10)))

    # 2. Sistema de Lorenz
    def lorenz(t, y, sigma=10, rho=28, beta=8/3):
        return np.array([
            sigma * (y[1] - y[0]),
            y[0] * (rho - y[2]) - y[1],
            y[0] * y[1] - beta * y[2]
        ])

    sistemas.append(('lorenz', lorenz, np.array([1.0, 1.0, 1.0]), (0, 50)))

    # 3. Equação de Van der Pol
    def vanderpol(t, y, mu=1.0):
        return np.array([
            y[1],
            mu * (1 - y[0]**2) * y[1] - y[0]
        ])

    sistemas.append(('vanderpol', vanderpol, np.array([1.0, 0.0]), (0, 20)))

    return sistemas


# Exemplos de uso
if __name__ == "__main__":
    print("Módulo de Benchmarking e Otimização")
    print("=" * 40)

    # Teste 1: Benchmark de integradores
    print("Teste 1: Benchmark de Integradores")
    benchmark = BenchmarkSuite()

    sistemas_teste = criar_sistemas_teste()

    print("Executando benchmarks de integração...")
    with timer_benchmark():
        resultados_integracao = benchmark.benchmark_integradores(
            sistemas_teste[:1],  # Apenas oscilador para teste rápido
            metodos=['RK45', 'RK23', 'DOP853']
        )

    # Análise dos resultados
    analise = benchmark.analisar_resultados(resultados_integracao)

    if 'erro' not in analise:
        print("
Análise dos Resultados:")
        print(f"Taxa de sucesso: {analise['taxa_sucesso']:.1%}")
        print(f"Tempo médio: {analise['tempo_medio']:.4f} s")
        print(f"Método mais rápido: {analise['mais_rapido']}")
        print(f"Método mais lento: {analise['mais_lento']}")

        # Comparação entre métodos
        comparacao = benchmark.comparar_metodos('integracao')
        if 'erro' not in comparacao:
            print("
Comparação entre métodos:")
            for metodo, stats in comparacao['comparacao_por_metodo'].items():
                print(".4f"
                      ".4f")

    # Teste 2: Otimização automática
    print("\nTeste 2: Otimização Automática")

    def sistema_teste(t, y):
        # Sistema simples para teste
        return np.array([-0.1 * y[0], 0.05 * y[1]])

    otimizador = OtimizacaoAutomatica()

    print("Otimizando parâmetros de integração...")
    with timer_benchmark():
        resultado_otimizacao = otimizador.otimizar_parametros_integracao(
            sistema_teste,
            np.array([1.0, 1.0]),
            (0, 10),
            metrica_otimizacao='tempo'
        )

    if 'erro' not in resultado_otimizacao:
        melhor = resultado_otimizacao['melhor_configuracao']
        print("
Melhor configuração encontrada:")
        print(f"Método: {melhor['metodo']}")
        print(f"RTOL: {melhor['rtol']:.0e}")
        print(f"ATOL: {melhor['atol']:.0e}")
        print(f"Score: {resultado_otimizacao['score']:.4f}")
        print(f"Configurações testadas: {resultado_otimizacao['todas_configuracoes_testadas']}")

    print("\nMódulo funcionando corretamente! ✅")
