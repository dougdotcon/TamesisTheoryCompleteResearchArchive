#!/usr/bin/env python3
"""
Métodos de Otimização para Física Computacional
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Otimização por mínimos quadrados
- Métodos de otimização global
- Validação de convergência
- Análise de sensibilidade
"""

import numpy as np
from scipy.optimize import minimize, least_squares, differential_evolution, basinhopping
from scipy.optimize import curve_fit, minimize_scalar
from typing import Callable, Tuple, Dict, Optional, Union, List
import warnings
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ConfiguracaoOtimizacao:
    """
    Configuração para algoritmos de otimização
    """
    metodo: str = 'L-BFGS-B'
    max_iter: int = 1000
    tol: float = 1e-9
    bounds: Optional[List[Tuple[float, float]]] = None
    constraints: Optional[List[Dict]] = None
    seed: Optional[int] = None

    def __post_init__(self):
        metodos_validos = ['L-BFGS-B', 'SLSQP', 'trust-constr', 'Nelder-Mead', 'Powell']
        if self.metodo not in metodos_validos:
            warnings.warn(f"Método {self.metodo} não é padrão. Verifique se é válido.")

        if self.seed is not None:
            np.random.seed(self.seed)


class OtimizadorFisico(ABC):
    """
    Classe base abstrata para otimizadores físicos
    """

    def __init__(self, config: ConfiguracaoOtimizacao):
        self.config = config
        self.historia_otimizacao = []
        self.melhor_solucao = None
        self.melhor_valor = np.inf

    @abstractmethod
    def funcao_objetivo(self, params: np.ndarray) -> float:
        """Função objetivo a ser minimizada/maximizada"""
        pass

    @abstractmethod
    def calcular_gradiente(self, params: np.ndarray) -> np.ndarray:
        """Calcula gradiente da função objetivo"""
        pass

    def otimizar(self, params_iniciais: np.ndarray, verbose: bool = True) -> Dict:
        """
        Executa otimização completa

        Parameters:
        -----------
        params_iniciais : array_like
            Parâmetros iniciais
        verbose : bool
            Mostrar progresso

        Returns:
        --------
        dict: Resultados da otimização
        """
        if verbose:
            print(f"Iniciando otimização com método {self.config.metodo}")
            print(f"Parâmetros iniciais: {params_iniciais}")

        # Callback para armazenar história
        def callback(xk):
            valor = self.funcao_objetivo(xk)
            self.historia_otimizacao.append({
                'parametros': xk.copy(),
                'valor': valor,
                'iteracao': len(self.historia_otimizacao)
            })

            if valor < self.melhor_valor:
                self.melhor_valor = valor
                self.melhor_solucao = xk.copy()

        try:
            if self.config.metodo in ['L-BFGS-B', 'SLSQP', 'trust-constr']:
                # Otimização com bounds e constraints
                resultado = minimize(
                    self.funcao_objetivo,
                    params_iniciais,
                    method=self.config.metodo,
                    bounds=self.config.bounds,
                    constraints=self.config.constraints,
                    callback=callback,
                    options={
                        'maxiter': self.config.max_iter,
                        'ftol': self.config.tol,
                        'gtol': self.config.tol
                    }
                )

            elif self.config.metodo in ['Nelder-Mead', 'Powell']:
                # Otimização sem derivadas
                resultado = minimize(
                    self.funcao_objetivo,
                    params_iniciais,
                    method=self.config.metodo,
                    callback=callback,
                    options={
                        'maxiter': self.config.max_iter,
                        'ftol': self.config.tol
                    }
                )

            else:
                raise ValueError(f"Método {self.config.metodo} não suportado")

            # Preparar resultados
            resultados = {
                'sucesso': resultado.success,
                'mensagem': resultado.message,
                'parametros_otimos': resultado.x,
                'valor_otimo': resultado.fun,
                'numero_iteracoes': resultado.nit,
                'numero_avaliacoes': resultado.nfev,
                'historia': self.historia_otimizacao,
                'melhor_solucao': self.melhor_solucao,
                'melhor_valor': self.melhor_valor,
                'configuracao': self.config.__dict__
            }

            if hasattr(resultado, 'njev'):
                resultados['numero_gradientes'] = resultado.njev

            if verbose:
                print(f"Otimização {'bem-sucedida' if resultado.success else 'falhou'}")
                print(f"Valor ótimo: {resultado.fun:.6e}")
                print(f"Número de iterações: {resultado.nit}")

            return resultados

        except Exception as e:
            return {
                'sucesso': False,
                'mensagem': f"Erro na otimização: {str(e)}",
                'parametros_otimos': None,
                'valor_otimo': None,
                'numero_iteracoes': 0,
                'numero_avaliacoes': 0,
                'historia': self.historia_otimizacao
            }

    def analise_sensibilidade(self, params_otimos: np.ndarray,
                            perturbacao: float = 1e-6) -> Dict[str, np.ndarray]:
        """
        Análise de sensibilidade dos parâmetros ótimos
        """
        n_params = len(params_otimos)
        sensibilidades = np.zeros(n_params)

        valor_base = self.funcao_objetivo(params_otimos)

        for i in range(n_params):
            # Perturbação positiva
            params_pert_pos = params_otimos.copy()
            params_pert_pos[i] += perturbacao
            valor_pert_pos = self.funcao_objetivo(params_pert_pos)

            # Perturbação negativa
            params_pert_neg = params_otimos.copy()
            params_pert_neg[i] -= perturbacao
            valor_pert_neg = self.funcao_objetivo(params_pert_neg)

            # Sensibilidade finita
            sensibilidades[i] = (valor_pert_pos - valor_pert_neg) / (2 * perturbacao)

        # Normalizar sensibilidades
        sensibilidades_normalizadas = sensibilidades / np.max(np.abs(sensibilidades))

        return {
            'sensibilidades': sensibilidades,
            'sensibilidades_normalizadas': sensibilidades_normalizadas,
            'parametros': params_otimos,
            'valor_base': valor_base,
            'perturbacao': perturbacao
        }


class OtimizacaoMinimosQuadrados:
    """
    Otimização por mínimos quadrados para ajuste de curvas
    """

    def __init__(self, modelo_func: Callable, dados_x: np.ndarray, dados_y: np.ndarray,
                 sigma_y: Optional[np.ndarray] = None):
        """
        Parameters:
        -----------
        modelo_func : callable
            Função modelo f(x, *params)
        dados_x : array_like
            Valores x dos dados
        dados_y : array_like
            Valores y dos dados
        sigma_y : array_like, optional
            Incertezas em y
        """
        self.modelo_func = modelo_func
        self.dados_x = np.asarray(dados_x)
        self.dados_y = np.asarray(dados_y)
        self.sigma_y = np.asarray(sigma_y) if sigma_y is not None else np.ones_like(dados_y)

        if len(self.dados_x) != len(self.dados_y):
            raise ValueError("dados_x e dados_y devem ter mesmo tamanho")

    def ajustar_curva(self, params_iniciais: np.ndarray,
                     bounds: Optional[List[Tuple[float, float]]] = None) -> Dict:
        """
        Ajuste de curva usando mínimos quadrados
        """
        def residuo(params):
            """Função resíduo para mínimos quadrados"""
            y_modelo = self.modelo_func(self.dados_x, *params)
            return (y_modelo - self.dados_y) / self.sigma_y

        try:
            if bounds is not None:
                resultado = least_squares(
                    residuo,
                    params_iniciais,
                    bounds=bounds,
                    method='trf',
                    max_nfev=1000
                )
            else:
                resultado = least_squares(
                    residuo,
                    params_iniciais,
                    method='lm',
                    max_nfev=1000
                )

            # Calcular chi-quadrado
            residuos = residuo(resultado.x)
            chi_quadrado = np.sum(residuos**2)
            chi_quadrado_reduzido = chi_quadrado / (len(self.dados_y) - len(params_iniciais))

            # Calcular matriz de covariância
            try:
                jacobiana = resultado.jac
                covariancia = np.linalg.inv(jacobiana.T @ jacobiana)
                erros_params = np.sqrt(np.diag(covariancia))
            except:
                covariancia = None
                erros_params = np.full(len(params_iniciais), np.nan)

            return {
                'sucesso': resultado.success,
                'mensagem': resultado.message,
                'parametros_otimos': resultado.x,
                'erros_parametros': erros_params,
                'chi_quadrado': chi_quadrado,
                'chi_quadrado_reduzido': chi_quadrado_reduzido,
                'graus_liberdade': len(self.dados_y) - len(params_iniciais),
                'covariancia': covariancia,
                'numero_iteracoes': resultado.nfev,
                'status': resultado.status
            }

        except Exception as e:
            return {
                'sucesso': False,
                'mensagem': f"Erro no ajuste: {str(e)}",
                'parametros_otimos': None,
                'erros_parametros': None,
                'chi_quadrado': None,
                'chi_quadrado_reduzido': None
            }

    def bootstrap(self, params_otimos: np.ndarray, n_bootstrap: int = 1000) -> Dict[str, np.ndarray]:
        """
        Análise de incertezas usando bootstrap
        """
        params_bootstrap = []

        print(f"Executando análise bootstrap com {n_bootstrap} amostras...")

        for i in range(n_bootstrap):
            # Gerar amostra bootstrap
            indices = np.random.choice(len(self.dados_y), len(self.dados_y), replace=True)
            x_bootstrap = self.dados_x[indices]
            y_bootstrap = self.dados_y[indices]
            sigma_bootstrap = self.sigma_y[indices]

            # Criar otimizador temporário
            otimizador_temp = OtimizacaoMinimosQuadrados(
                self.modelo_func, x_bootstrap, y_bootstrap, sigma_bootstrap
            )

            # Ajuste
            resultado = otimizador_temp.ajustar_curva(params_otimos)

            if resultado['sucesso']:
                params_bootstrap.append(resultado['parametros_otimos'])

            if (i + 1) % (n_bootstrap // 10) == 0:
                progresso = (i + 1) / n_bootstrap * 100
                print(".1f")

        params_bootstrap = np.array(params_bootstrap)

        # Calcular estatísticas
        params_medios = np.mean(params_bootstrap, axis=0)
        params_std = np.std(params_bootstrap, axis=0)
        params_percentis = np.percentile(params_bootstrap, [16, 50, 84], axis=0)

        return {
            'parametros_medios': params_medios,
            'parametros_std': params_std,
            'parametros_percentis': params_percentis,
            'todas_amostras': params_bootstrap,
            'n_sucessos': len(params_bootstrap),
            'n_total': n_bootstrap
        }


class OtimizacaoGlobal:
    """
    Métodos de otimização global para problemas complexos
    """

    @staticmethod
    def evolucao_diferencial(funcao_objetivo: Callable,
                           bounds: List[Tuple[float, float]],
                           max_iter: int = 100,
                           pop_size: int = 20,
                           seed: Optional[int] = None) -> Dict:
        """
        Otimização por evolução diferencial
        """
        if seed is not None:
            np.random.seed(seed)

        def callback(xk, convergence):
            pass

        try:
            resultado = differential_evolution(
                funcao_objetivo,
                bounds,
                maxiter=max_iter,
                popsize=pop_size,
                callback=callback,
                seed=seed
            )

            return {
                'sucesso': resultado.success,
                'mensagem': resultado.message,
                'parametros_otimos': resultado.x,
                'valor_otimo': resultado.fun,
                'numero_iteracoes': resultado.nit,
                'numero_avaliacoes': resultado.nfev,
                'populacao_final': resultado.population,
                'scores_populacao': resultado.population_energies
            }

        except Exception as e:
            return {
                'sucesso': False,
                'mensagem': f"Erro na evolução diferencial: {str(e)}",
                'parametros_otimos': None,
                'valor_otimo': None
            }

    @staticmethod
    def simulated_annealing(funcao_objetivo: Callable,
                          params_iniciais: np.ndarray,
                          bounds: List[Tuple[float, float]],
                          T_inicial: float = 1.0,
                          T_minima: float = 0.01,
                          max_iter: int = 1000) -> Dict:
        """
        Simulated annealing para otimização global
        """
        # Implementação simplificada
        melhor_solucao = params_iniciais.copy()
        melhor_valor = funcao_objetivo(params_iniciais)

        solucao_atual = params_iniciais.copy()
        valor_atual = melhor_valor

        T = T_inicial
        historia = []

        for i in range(max_iter):
            # Gerar candidato
            candidato = solucao_atual + np.random.normal(0, 0.1, len(params_iniciais))

            # Aplicar bounds
            for j, (min_val, max_val) in enumerate(bounds):
                candidato[j] = np.clip(candidato[j], min_val, max_val)

            # Avaliar candidato
            valor_candidato = funcao_objetivo(candidato)

            # Critério de aceitação Metropolis
            delta_E = valor_candidato - valor_atual
            if delta_E < 0 or np.random.random() < np.exp(-delta_E / T):
                solucao_atual = candidato.copy()
                valor_atual = valor_candidato

                if valor_candidato < melhor_valor:
                    melhor_solucao = candidato.copy()
                    melhor_valor = valor_candidato

            # Resfriamento
            T = T_inicial * np.exp(-i / (max_iter / 10))
            if T < T_minima:
                T = T_minima

            historia.append({
                'iteracao': i,
                'temperatura': T,
                'melhor_valor': melhor_valor,
                'valor_atual': valor_atual
            })

        return {
            'parametros_otimos': melhor_solucao,
            'valor_otimo': melhor_valor,
            'historia': historia,
            'numero_iteracoes': max_iter
        }


# Funções utilitárias para uso direto
def otimizar_minimos_quadrados(modelo_func: Callable, dados_x: np.ndarray,
                              dados_y: np.ndarray, params_iniciais: np.ndarray,
                              sigma_y: Optional[np.ndarray] = None) -> Dict:
    """
    Função wrapper para otimização por mínimos quadrados
    """
    otimizador = OtimizacaoMinimosQuadrados(modelo_func, dados_x, dados_y, sigma_y)
    return otimizador.ajustar_curva(params_iniciais)


def benchmark_otimizadores(funcao_objetivo: Callable, params_iniciais: np.ndarray,
                          bounds: Optional[List[Tuple[float, float]]] = None) -> Dict:
    """
    Benchmark de diferentes algoritmos de otimização
    """
    metodos = ['L-BFGS-B', 'SLSQP', 'Nelder-Mead', 'Powell']
    resultados = {}

    print("Benchmark de otimizadores:")
    print("-" * 50)

    for metodo in metodos:
        config = ConfiguracaoOtimizacao(metodo=metodo, bounds=bounds)

        # Criar otimizador simples
        class OtimizadorSimples(OtimizadorFisico):
            def funcao_objetivo(self, params):
                return funcao_objetivo(params)

            def calcular_gradiente(self, params):
                # Gradiente numérico simples
                eps = 1e-8
                grad = np.zeros_like(params)
                for i in range(len(params)):
                    params_pert = params.copy()
                    params_pert[i] += eps
                    grad[i] = (funcao_objetivo(params_pert) - funcao_objetivo(params)) / eps
                return grad

        otimizador = OtimizadorSimples(config)
        resultado = otimizador.otimizar(params_iniciais, verbose=False)

        resultados[metodo] = resultado

        print("15"
              "6.2e"
              "6.2e")

    return resultados


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo: Ajuste de oscilador harmônico
    print("Exemplo: Ajuste de parâmetros de oscilador harmônico")
    print("=" * 60)

    # Gerar dados simulados
    np.random.seed(42)
    x_dados = np.linspace(0, 10, 50)
    omega_verdadeiro = 2.0
    amplitude_verdadeira = 1.5
    fase_verdadeira = 0.5

    # Modelo: A * cos(ω*x + φ)
    def modelo_oscilador(x, amplitude, omega, fase):
        return amplitude * np.cos(omega * x + fase)

    y_verdadeiro = modelo_oscilador(x_dados, amplitude_verdadeira, omega_verdadeiro, fase_verdadeira)
    ruido = np.random.normal(0, 0.1, len(x_dados))
    y_dados = y_verdadeiro + ruido

    # Ajuste
    params_iniciais = [1.0, 1.0, 0.0]
    resultado = otimizar_minimos_quadrados(
        modelo_oscilador, x_dados, y_dados, params_iniciais
    )

    if resultado['sucesso']:
        print("Ajuste bem-sucedido:")
        print(f"Amplitude: {resultado['parametros_otimos'][0]:.3f} ± {resultado['erros_parametros'][0]:.3f}")
        print(f"Frequência ω: {resultado['parametros_otimos'][1]:.3f} ± {resultado['erros_parametros'][1]:.3f}")
        print(f"Fase φ: {resultado['parametros_otimos'][2]:.3f} ± {resultado['erros_parametros'][2]:.3f}")
        print(f"χ² reduzido: {resultado['chi_quadrado_reduzido']:.3f}")
    else:
        print(f"Erro no ajuste: {resultado['mensagem']}")

    # Benchmark de otimizadores
    def funcao_teste(params):
        # Função de Rosenbrock (problema de teste clássico)
        x, y = params
        return (1 - x)**2 + 100 * (y - x**2)**2

    print("Benchmark de otimizadores na função de Rosenbrock:")
    resultados_benchmark = benchmark_otimizadores(
        funcao_teste, [0.0, 0.0], bounds=[(-2, 2), (-2, 2)]
    )
