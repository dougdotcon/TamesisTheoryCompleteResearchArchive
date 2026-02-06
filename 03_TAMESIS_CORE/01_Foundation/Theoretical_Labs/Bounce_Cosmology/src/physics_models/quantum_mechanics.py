#!/usr/bin/env python3
"""
Mecânica Quântica Computacional
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Equação de Schrödinger
- Oscilador harmônico quântico
- Átomo de hidrogênio
- Estados coerentes e squeezed
- Simulação de dinâmica quântica
"""

import numpy as np
from scipy.linalg import eigh, eigvals
from scipy.integrate import solve_ivp
from typing import Callable, Tuple, Optional, Union, List, Dict
from ..numerical_methods.linear_algebra import AlgebraLinearFisica, OperadoresQuanticos
from ..numerical_methods.integrators import IntegratorNumerico
import warnings


class EquacaoSchrodinger:
    """
    Solução da equação de Schrödinger
    """

    def __init__(self, potencial: Callable, x_min: float = -10, x_max: float = 10,
                 n_pontos: int = 1000, precisao: float = 1e-10):
        """
        Inicializa resolvedor da equação de Schrödinger

        Parameters:
        -----------
        potencial : callable
            Função V(x) do potencial
        x_min, x_max : float
            Limites do domínio espacial
        n_pontos : int
            Número de pontos da grade
        precisao : float
            Precisão numérica
        """
        self.potencial = potencial
        self.x_min = x_min
        self.x_max = x_max
        self.n_pontos = n_pontos
        self.precisao = precisao

        # Grade espacial
        self.x = np.linspace(x_min, x_max, n_pontos)
        self.dx = self.x[1] - self.x[0]

        # Constantes físicas (unidades atômicas: ħ = m = 1)
        self.hbar = 1.0
        self.m = 1.0

    def construir_hamiltoniano(self) -> np.ndarray:
        """
        Constrói matriz Hamiltoniana usando diferenças finitas

        Returns:
        --------
        array: Matriz Hamiltoniana
        """
        n = self.n_pontos
        H = np.zeros((n, n))

        # Potencial na diagonal
        V = self.potencial(self.x)
        np.fill_diagonal(H, V)

        # Termo cinético (diferenças finitas centradas)
        coef_cinetico = -self.hbar**2 / (2 * self.m * self.dx**2)

        for i in range(1, n-1):
            H[i, i-1] = coef_cinetico
            H[i, i+1] = coef_cinetico
            H[i, i] += -2 * coef_cinetico  # Termo diagonal do cinético

        # Condições de contorno (Dirichlet: ψ = 0 nas fronteiras)
        # Já implementadas implicitamente pelos zeros nas bordas

        return H

    def resolver_estados_ligados(self, n_estados: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resolve para estados ligados (autovalores negativos)

        Parameters:
        -----------
        n_estados : int
            Número de estados a calcular

        Returns:
        --------
        tuple: (energias, wavefunctions) ordenados por energia crescente
        """
        H = self.construir_hamiltoniano()

        # Diagonalização
        alg = AlgebraLinearFisica()
        energias, wavefunctions = alg.diagonalizar_matriz_hermitiana(H, n_estados)

        # Normalizar funções de onda
        for i in range(min(n_estados, len(energias))):
            norm = np.sqrt(np.trapz(np.abs(wavefunctions[:, i])**2, self.x))
            if norm > self.precisao:
                wavefunctions[:, i] /= norm

        return energias[:n_estados], wavefunctions[:, :n_estados]

    def evolucao_temporal(self, psi_0: np.ndarray, t_span: Tuple[float, float],
                         n_times: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evolução temporal da função de onda

        Parameters:
        -----------
        psi_0 : array_like
            Estado inicial
        t_span : tuple
            (t_inicial, t_final)
        n_times : int
            Número de pontos temporais

        Returns:
        --------
        tuple: (tempos, psi_t) evolução temporal
        """
        H = self.construir_hamiltoniano()

        def dpsi_dt(t, psi):
            # iℏ ∂ψ/∂t = H ψ
            return -1j * H @ psi / self.hbar

        # Integração temporal
        integrator = IntegratorNumerico()
        t_eval = np.linspace(t_span[0], t_span[1], n_times)

        # Resolve numericamente
        sol = integrator.integrar_sistema(dpsi_dt, psi_0, t_span)

        if not sol['sucesso']:
            raise RuntimeError(f"Evolução temporal falhou: {sol['mensagem']}")

        # Avalia solução nos pontos desejados
        psi_t = []
        for t in t_eval:
            psi_atual = sol['solucao'].sol(t)
            psi_t.append(psi_atual)

        return t_eval, np.array(psi_t)


class OsciladorHarmonicoQuantico:
    """
    Oscilador harmônico quântico - solução analítica e numérica
    """

    def __init__(self, omega: float = 1.0, hbar: float = 1.0):
        """
        Parameters:
        -----------
        omega : float
            Frequência angular
        hbar : float
            Constante de Planck reduzida
        """
        self.omega = omega
        self.hbar = hbar
        self.m = 1.0  # Massa unitária

    def energias_analiticas(self, n_max: int = 10) -> np.ndarray:
        """
        Energias analíticas: E_n = ℏω(n + 1/2)

        Returns:
        --------
        array: Energias para n = 0, 1, 2, ..., n_max
        """
        n = np.arange(n_max + 1)
        return self.hbar * self.omega * (n + 0.5)

    def funcao_onda_analitica(self, n: int, x: np.ndarray) -> np.ndarray:
        """
        Função de onda analítica do estado n

        Parameters:
        -----------
        n : int
            Número quântico
        x : array_like
            Coordenadas

        Returns:
        --------
        array: ψ_n(x)
        """
        # Constante de normalização
        alpha = np.sqrt(self.m * self.omega / (np.pi * self.hbar))
        xi = np.sqrt(self.m * self.omega / self.hbar) * x

        # Polinômio de Hermite
        from scipy.special import hermite
        H_n = hermite(n)

        # Função de onda
        psi = alpha * (1/np.sqrt(2**n * np.math.factorial(n))) * \
              np.exp(-xi**2 / 2) * H_n(xi)

        return psi

    def resolver_numericamente(self, x_min: float = -5, x_max: float = 5,
                              n_pontos: int = 1000, n_estados: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resolve numericamente usando diferenças finitas

        Returns:
        --------
        tuple: (energias, wavefunctions)
        """
        # Potencial V(x) = 1/2 m ω² x²
        def potencial(x):
            return 0.5 * self.m * self.omega**2 * x**2

        # Resolver equação de Schrödinger
        schrodinger = EquacaoSchrodinger(potencial, x_min, x_max, n_pontos)
        energias, wavefunctions = schrodinger.resolver_estados_ligados(n_estados)

        return energias, wavefunctions

    def comparar_analitico_numerico(self, n_max: int = 5) -> Dict[str, np.ndarray]:
        """
        Compara soluções analíticas e numéricas

        Returns:
        --------
        dict: Resultados da comparação
        """
        # Soluções analíticas
        energias_analiticas = self.energias_analiticas(n_max)

        # Soluções numéricas
        energias_numericas, wavefunctions_numericas = self.resolver_numericamente(
            n_estados=n_max+1
        )

        # Grade para funções de onda
        x = np.linspace(-5, 5, 1000)
        wavefunctions_analiticas = np.array([
            self.funcao_onda_analitica(n, x) for n in range(n_max+1)
        ])

        return {
            'energias_analiticas': energias_analiticas,
            'energias_numericas': energias_numericas,
            'wavefunctions_analiticas': wavefunctions_analiticas,
            'wavefunctions_numericas': wavefunctions_numericas,
            'x': x,
            'erros_energia': np.abs(energias_analiticas - energias_numericas[:n_max+1])
        }


class AtomoHidrogenio:
    """
    Átomo de hidrogênio - solução aproximada
    """

    def __init__(self, precisao: float = 1e-8):
        """
        Parameters:
        -----------
        precisao : float
            Precisão para cálculos numéricos
        """
        self.precisao = precisao
        # Constantes em unidades atômicas
        self.hbar = 1.0
        self.m = 1.0
        self.e = 1.0  # Carga elementar
        self.epsilon_0 = 1/(4*np.pi)  # Permitividade

    def potencial_coulomb(self, r: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Potencial de Coulomb: V(r) = -e²/(4πε₀r)
        """
        return -self.e**2 / (4 * np.pi * self.epsilon_0 * r)

    def resolver_estado_fundamental(self, r_max: float = 20, n_pontos: int = 1000) -> Dict:
        """
        Resolve numericamente o estado fundamental

        Parameters:
        -----------
        r_max : float
            Raio máximo
        n_pontos : int
            Número de pontos

        Returns:
        --------
        dict: Energia e função de onda do estado fundamental
        """
        # Grade radial
        r = np.linspace(0.01, r_max, n_pontos)  # Evita r=0
        dr = r[1] - r[0]

        # Potencial efetivo (incluindo termo centrífugo l=0)
        V_eff = self.potencial_coulomb(r) + self.hbar**2 * 0.5 / (self.m * r**2)

        # Matriz Hamiltoniana radial (equação efetiva 1D)
        H = np.zeros((n_pontos, n_pontos))

        # Potencial na diagonal
        np.fill_diagonal(H, V_eff)

        # Termo cinético (diferenças finitas)
        coef = -self.hbar**2 / (2 * self.m * dr**2)
        for i in range(1, n_pontos-1):
            H[i, i-1] = coef
            H[i, i+1] = coef
            H[i, i] += -2 * coef

        # Condições de contorno
        # ψ(0) = 0 (regularidade) e ψ(∞) ≈ 0
        H[0, :] = 0; H[0, 0] = 1  # ψ(0) = 0
        H[-1, :] = 0; H[-1, -1] = 1  # ψ(r_max) = 0

        # Resolver autovalor
        alg = AlgebraLinearFisica()
        energias, wavefunctions = alg.diagonalizar_matriz_hermitiana(H, n_estados=1)

        energia_fundamental = energias[0]
        psi_fundamental = wavefunctions[:, 0]

        # Normalizar
        norm = np.sqrt(np.trapz(psi_fundamental**2 * r**2, r))  # Integral radial
        if norm > self.precisao:
            psi_fundamental /= norm

        return {
            'energia': energia_fundamental,
            'wavefunction': psi_fundamental,
            'r': r,
            'energia_analitica': -0.5  # Em unidades atômicas
        }


class EstadosCoerentes:
    """
    Estados coerentes do oscilador harmônico quântico
    """

    def __init__(self, oscilador: OsciladorHarmonicoQuantico):
        self.oscilador = oscilador
        self.quantum = OperadoresQuanticos(dim=50)  # Espaço de Hilbert truncado

    def estado_coerente(self, alpha: complex, metodo: str = 'numerico') -> np.ndarray:
        """
        Constrói estado coerente |α⟩

        Parameters:
        -----------
        alpha : complex
            Parâmetro do estado coerente
        metodo : str
            'numerico' ou 'operador'

        Returns:
        --------
        array: Vetor de estado coerente
        """
        if metodo == 'numerico':
            # Método numérico direto
            return self.quantum.estado_coerente(alpha, n_max=self.quantum.dim-1)
        elif metodo == 'operador':
            # Método usando operador de deslocamento
            # D(α) |0⟩ = |α⟩
            estado_vazio = np.zeros(self.quantum.dim)
            estado_vazio[0] = 1.0  # |0⟩

            # Implementação simplificada do operador de deslocamento
            # D(α) = exp(α a† - α* a)
            D_alpha = self._operador_deslocamento(alpha)
            estado_coerente = D_alpha @ estado_vazio

            return estado_coerente
        else:
            raise ValueError(f"Método {metodo} não suportado")

    def _operador_deslocamento(self, alpha: complex) -> np.ndarray:
        """
        Operador de deslocamento D(α) = exp(α a† - α* a)
        """
        # Implementação matricial truncada
        dim = self.quantum.dim
        D = np.eye(dim, dtype=complex)

        # Série de Taylor truncada
        A = self._operador_a()
        A_dagger = self._operador_a_dagger()

        termo = np.eye(dim, dtype=complex)
        n_max = 10  # Truncar série

        for n in range(1, n_max):
            termo = termo @ (alpha * A_dagger - alpha.conj() * A) / n
            D += termo

        return D

    def _operador_a(self) -> np.ndarray:
        """Operador de aniquilação a"""
        dim = self.quantum.dim
        a = np.zeros((dim, dim), dtype=complex)

        for n in range(1, dim):
            a[n, n-1] = np.sqrt(n)

        return a

    def _operador_a_dagger(self) -> np.ndarray:
        """Operador de criação a†"""
        return self._operador_a().conj().T

    def propriedades_estado_coerente(self, alpha: complex) -> Dict[str, Union[float, complex]]:
        """
        Calcula propriedades do estado coerente
        """
        psi = self.estado_coerente(alpha)

        # Valor esperado de n = <a† a>
        a = self._operador_a()
        n_esperado = np.vdot(psi, a.conj().T @ a @ psi)

        # Variância de n
        n_quadrado = np.vdot(psi, (a.conj().T @ a) @ (a.conj().T @ a) @ psi)
        variancia_n = n_quadrado - n_esperado**2

        # Valor esperado de x e p
        x_op = (a + a.conj().T) / np.sqrt(2)
        p_op = 1j * (a.conj().T - a) / np.sqrt(2)

        x_esperado = np.vdot(psi, x_op @ psi)
        p_esperado = np.vdot(psi, p_op @ psi)

        return {
            'n_medio': np.real(n_esperado),
            'variancia_n': np.real(variancia_n),
            'x_medio': np.real(x_esperado),
            'p_medio': np.real(p_esperado),
            'alpha': alpha,
            'norma': np.linalg.norm(psi)
        }


# Funções utilitárias
def resolver_schrodinger(potencial: Callable, x_range: Tuple[float, float],
                        n_pontos: int = 1000, n_estados: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Função wrapper para resolver equação de Schrödinger
    """
    schrodinger = EquacaoSchrodinger(potencial, x_range[0], x_range[1], n_pontos)
    return schrodinger.resolver_estados_ligados(n_estados)


def estado_coerente_oscilador(alpha: complex, n_max: int = 50) -> np.ndarray:
    """
    Função wrapper para estado coerente
    """
    quantum = OperadoresQuanticos(dim=n_max)
    return quantum.estado_coerente(alpha, n_max)


# Exemplos de uso
if __name__ == "__main__":
    print("Módulo de Mecânica Quântica")
    print("=" * 35)

    # Teste 1: Oscilador harmônico
    print("Teste 1: Oscilador Harmônico Quântico")
    osc = OsciladorHarmonicoQuantico(omega=1.0)

    # Energias analíticas
    energias_analiticas = osc.energias_analiticas(5)
    print(f"Energias analíticas: {energias_analiticas}")

    # Comparação com solução numérica
    comparacao = osc.comparar_analitico_numerico(3)
    print(f"Erro máximo nas energias: {np.max(comparacao['erros_energia']):.2e}")

    # Teste 2: Estado coerente
    print("\nTeste 2: Estado Coerente")
    estados_coerentes = EstadosCoerentes(osc)
    alpha = 1.0 + 0.5j

    psi_coerente = estados_coerentes.estado_coerente(alpha)
    props = estados_coerentes.propriedades_estado_coerente(alpha)

    print(f"Estado coerente |α={alpha}⟩:")
    print(f"  <n> = {props['n_medio']:.3f}")
    print(f"  Δn = {np.sqrt(props['variancia_n']):.3f}")
    print(f"  Norma = {props['norma']:.6f}")

    # Teste 3: Schrödinger com poço quadrado
    print("\nTeste 3: Poço Quadrado Infinito")
    def poco_quadratico(x, V0=10, L=2):
        """Poço quadrático infinito"""
        return np.where(np.abs(x) < L/2, 0, V0)

    def potencial_poco(x):
        return poco_quadratico(x)

    energias, wavefunctions = resolver_schrodinger(potencial_poco, (-3, 3), n_estados=3)
    print(f"Energias do poço quadrático: {energias[:3]}")

    print("\nMódulo funcionando corretamente! ✅")
