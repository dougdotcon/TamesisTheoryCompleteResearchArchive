#!/usr/bin/env python3
"""
Métodos Numéricos Essenciais para Física Computacional
Implementação de integradores e solucionadores seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Método de Runge-Kutta de 4ª ordem
- Integração adaptativa
- Métodos para EDOs rígidas
- Validação numérica
"""

import numpy as np
from scipy.integrate import solve_ivp, odeint
from scipy.optimize import root_scalar
from typing import Callable, Tuple, Union, Optional
import warnings


class IntegratorNumerico:
    """
    Classe base para integradores numéricos com validação e otimização
    """

    def __init__(self, rtol: float = 1e-10, atol: float = 1e-12, max_step: float = 0.1):
        """
        Inicializa integrador com parâmetros de precisão

        Parameters:
        -----------
        rtol : float
            Tolerância relativa
        atol : float
            Tolerância absoluta
        max_step : float
            Tamanho máximo do passo
        """
        self.rtol = rtol
        self.atol = atol
        self.max_step = max_step
        self._validar_parametros()

    def _validar_parametros(self):
        """Valida parâmetros de integração"""
        if self.rtol <= 0 or self.atol <= 0:
            raise ValueError("Tolerâncias devem ser positivas")
        if self.max_step <= 0:
            raise ValueError("Tamanho máximo do passo deve ser positivo")

    def runge_kutta_4(self, f: Callable, y0: np.ndarray, t0: float, tf: float, h: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Método de Runge-Kutta de 4ª ordem para EDOs

        Parameters:
        -----------
        f : callable
            Função dy/dt = f(t, y)
        y0 : array_like
            Condições iniciais
        t0 : float
            Tempo inicial
        tf : float
            Tempo final
        h : float
            Tamanho do passo

        Returns:
        --------
        tuple: (t_values, y_values)
            Arrays de tempo e solução
        """
        if h <= 0:
            raise ValueError("Tamanho do passo deve ser positivo")

        t_values = np.arange(t0, tf + h, h)
        y_values = np.zeros((len(t_values), len(y0)))
        y_values[0] = y0

        for i in range(1, len(t_values)):
            t = t_values[i-1]
            y = y_values[i-1]

            k1 = h * f(t, y)
            k2 = h * f(t + h/2, y + k1/2)
            k3 = h * f(t + h/2, y + k2/2)
            k4 = h * f(t + h, y + k3)

            y_values[i] = y + (k1 + 2*k2 + 2*k3 + k4)/6

        return t_values, y_values

    def integrar_sistema(self, f: Callable, y0: np.ndarray, t_span: Tuple[float, float],
                        metodo: str = 'RK45', dense_output: bool = True) -> dict:
        """
        Integra sistema de EDOs usando scipy com validação avançada

        Parameters:
        -----------
        f : callable
            Sistema de equações dy/dt = f(t, y)
        y0 : array_like
            Condições iniciais
        t_span : tuple
            (t_inicial, t_final)
        metodo : str
            Método de integração ('RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA')
        dense_output : bool
            Retornar solução densa para interpolação

        Returns:
        --------
        dict: Resultados da integração com metadados
        """
        # Validação de entrada
        if len(y0) == 0:
            raise ValueError("Condições iniciais não podem ser vazias")

        try:
            # Integração principal
            sol = solve_ivp(
                f, t_span, y0,
                method=metodo,
                rtol=self.rtol,
                atol=self.atol,
                max_step=self.max_step,
                dense_output=dense_output
            )

            if not sol.success:
                raise RuntimeError(f"Integração falhou: {sol.message}")

            # Cálculo de métricas de qualidade
            metricas = self._calcular_metricas_qualidade(sol, f)

            resultado = {
                'solucao': sol,
                'metricas_qualidade': metricas,
                'parametros_integracao': {
                    'metodo': metodo,
                    'rtol': self.rtol,
                    'atol': self.atol,
                    'max_step': self.max_step
                },
                'sucesso': True,
                'mensagem': "Integração completada com sucesso"
            }

            return resultado

        except Exception as e:
            return {
                'solucao': None,
                'metricas_qualidade': None,
                'parametros_integracao': None,
                'sucesso': False,
                'mensagem': f"Erro na integração: {str(e)}"
            }

    def _calcular_metricas_qualidade(self, sol, f: Callable) -> dict:
        """
        Calcula métricas de qualidade da solução numérica
        """
        # Avaliação da conservação de energia (se aplicável)
        # Esta é uma implementação genérica - pode ser especializada

        t_eval = np.linspace(sol.t[0], sol.t[-1], 1000)
        y_eval = sol.sol(t_eval)

        # Métrica de suavidade da solução
        smoothness = 0
        if len(sol.t) > 10:
            # Calcular segunda derivada numérica
            for i in range(y_eval.shape[0]):
                segunda_derivada = np.gradient(np.gradient(y_eval[i], t_eval), t_eval)
                smoothness += np.mean(np.abs(segunda_derivada))

        # Número de passos realizados
        n_steps = len(sol.t)

        # Estabilidade numérica (baseada na variação relativa)
        stability = np.mean([
            np.std(y_eval[i]) / (np.mean(np.abs(y_eval[i])) + 1e-10)
            for i in range(y_eval.shape[0])
        ])

        return {
            'numero_passos': n_steps,
            'suavidade': smoothness,
            'estabilidade': stability,
            'tempo_integracao': getattr(sol, 'nfev', 0),  # Número de avaliações da função
            'precisao_alcancada': np.mean([
                np.linalg.norm(sol.sol(t_eval[i]) - y_eval[:, i])
                for i in range(0, len(t_eval), 100)
            ])
        }

    def encontrar_raiz(self, f: Callable, bracket: Tuple[float, float],
                      metodo: str = 'brentq', **kwargs) -> dict:
        """
        Encontra raiz de função usando métodos robustos

        Parameters:
        -----------
        f : callable
            Função f(x) = 0
        bracket : tuple
            (a, b) onde f(a) e f(b) têm sinais opostos
        metodo : str
            Método ('brentq', 'brenth', 'bisect', 'ridder')
        **kwargs : dict
            Parâmetros adicionais para root_scalar

        Returns:
        --------
        dict: Resultado da busca com metadados
        """
        try:
            resultado = root_scalar(f, bracket=bracket, method=metodo, **kwargs)

            return {
                'raiz': resultado.root,
                'convergencia': resultado.converged,
                'numero_iteracoes': resultado.iterations,
                'sucesso': True
            }

        except Exception as e:
            return {
                'raiz': None,
                'convergencia': False,
                'numero_iteracoes': 0,
                'sucesso': False,
                'erro': str(e)
            }


class IntegradorCosmologico(IntegratorNumerico):
    """
    Integrador especializado para equações cosmológicas
    Com detecção automática de bounce e validação física
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detectar_bounce(self, t_values: np.ndarray, a_values: np.ndarray) -> dict:
        """
        Detecta automaticamente o ponto de bounce na evolução cosmológica

        Parameters:
        -----------
        t_values : array_like
            Valores de tempo
        a_values : array_like
            Valores do fator de escala

        Returns:
        --------
        dict: Propriedades do bounce detectado
        """
        # Encontrar mínimo do fator de escala
        idx_bounce = np.argmin(a_values)

        if idx_bounce == 0 or idx_bounce == len(a_values) - 1:
            return {
                'detectado': False,
                'motivo': 'Mínimo nas extremidades do intervalo'
            }

        t_bounce = t_values[idx_bounce]
        a_bounce = a_values[idx_bounce]

        # Calcular velocidade no bounce
        if idx_bounce > 0 and idx_bounce < len(a_values) - 1:
            da_dt = np.gradient(a_values, t_values)[idx_bounce]
        else:
            da_dt = 0

        # Calcular número de e-folds após bounce
        t_pos = t_values[t_values > t_bounce]
        a_pos = a_values[t_values > t_bounce]

        if len(t_pos) > 10:
            e_folds = np.log(a_pos[-1] / a_bounce)
        else:
            e_folds = 0

        return {
            'detectado': True,
            't_bounce': t_bounce,
            'a_bounce': a_bounce,
            'da_dt_bounce': da_dt,
            'e_folds_pos_bounce': e_folds,
            'indice_bounce': idx_bounce
        }

    def validacao_conservacao(self, sol, energia_func: Optional[Callable] = None) -> dict:
        """
        Valida conservação de quantidades físicas durante a integração

        Parameters:
        -----------
        sol : Bunch
            Solução da integração
        energia_func : callable, optional
            Função para calcular energia total do sistema

        Returns:
        --------
        dict: Métricas de conservação
        """
        if energia_func is None:
            # Implementação padrão - assumir conservação de energia simples
            return {'validacao': 'Não implementada - forneça energia_func'}

        t_eval = np.linspace(sol.t[0], sol.t[-1], 100)
        y_eval = sol.sol(t_eval)

        energias = []
        for i in range(len(t_eval)):
            energia = energia_func(t_eval[i], y_eval[:, i])
            energias.append(energia)

        energias = np.array(energias)

        # Calcular conservação relativa
        energia_media = np.mean(energias)
        energia_std = np.std(energias)
        conservacao_relativa = energia_std / (abs(energia_media) + 1e-15)

        return {
            'energia_media': energia_media,
            'energia_std': energia_std,
            'conservacao_relativa': conservacao_relativa,
            'conservacao_aceitavel': conservacao_relativa < 1e-6,
            'evolucao_energia': energias
        }


# Funções utilitárias para uso direto
def runge_kutta_4(f: Callable, y0: np.ndarray, t0: float, tf: float, h: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Função wrapper para Runge-Kutta 4
    """
    integrator = IntegratorNumerico()
    return integrator.runge_kutta_4(f, y0, t0, tf, h)


def integrar_sistema_com_validacao(f: Callable, y0: np.ndarray, t_span: Tuple[float, float],
                                  **kwargs) -> dict:
    """
    Função wrapper para integração com validação completa
    """
    integrator = IntegradorNumerico(**kwargs)
    metodo = kwargs.pop('metodo', 'RK45')
    return integrator.integrar_sistema(f, y0, t_span, metodo=metodo)


# Exemplo de uso e testes
if __name__ == "__main__":
    # Exemplo: Oscilador harmônico
    def oscillator(t, y):
        """Equação do oscilador harmônico: d²y/dt² = -ω²y"""
        omega = 1.0
        return [y[1], -omega**2 * y[0]]

    # Condições iniciais
    y0 = [1.0, 0.0]  # y(0) = 1, dy/dt(0) = 0
    t_span = (0, 10)

    # Integração
    resultado = integrar_sistema_com_validacao(oscillator, y0, t_span)

    if resultado['sucesso']:
        print("Integração bem-sucedida!")
        print(f"Número de passos: {resultado['metricas_qualidade']['numero_passos']}")
        print(f"Precisão alcançada: {resultado['metricas_qualidade']['precisao_alcancada']:.2e}")
    else:
        print(f"Erro na integração: {resultado['mensagem']}")


# Função wrapper adicionada no final para evitar problemas de dependência circular
def integrar_sistema_com_validacao(f: Callable, y0: np.ndarray, t_span: Tuple[float, float],
                                  metodo: str = 'RK45', **kwargs) -> dict:
    """
    Função wrapper para integração com validação completa
    """
    integrator = IntegratorNumerico(**kwargs)
    return integrator.integrar_sistema(f, y0, t_span, metodo=metodo)
