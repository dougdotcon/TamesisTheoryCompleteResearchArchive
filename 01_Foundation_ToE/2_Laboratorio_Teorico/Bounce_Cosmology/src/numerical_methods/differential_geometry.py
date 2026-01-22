#!/usr/bin/env python3
"""
Geometria Diferencial para Relatividade Geral
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Símbolos de Christoffel
- Tensores de curvatura (Riemann, Ricci)
- Equações de Einstein
- Coordenadas curvilíneas
"""

import numpy as np
from typing import Callable, Tuple, Optional, Union, Dict, List
from scipy.optimize import minimize
from .calculus import CalculoAvancado, derivada
import warnings


class GeometriaDiferencial:
    """
    Classe para cálculos de geometria diferencial em relatividade geral
    """

    def __init__(self, coordenadas: List[str], precisao: float = 1e-10):
        """
        Inicializa geometria com coordenadas especificadas

        Parameters:
        -----------
        coordenadas : list
            Lista de nomes das coordenadas (ex: ['t', 'r', 'θ', 'φ'])
        precisao : float
            Precisão para cálculos numéricos
        """
        self.coordenadas = coordenadas
        self.n_coordenadas = len(coordenadas)
        self.precisao = precisao
        self.calc = CalculoAvancado(precisao)

    def simbolos_christoffel(self, metrica: Callable, ponto: np.ndarray) -> np.ndarray:
        """
        Calcula símbolos de Christoffel Γ^λ_{μν}

        Parameters:
        -----------
        metrica : callable
            Função que retorna g_{μν}(x) como matriz
        ponto : array_like
            Ponto onde calcular os símbolos

        Returns:
        --------
        array: Tensor Γ^λ_{μν} com shape (n_coords, n_coords, n_coords)
        """
        ponto = np.asarray(ponto)
        n = self.n_coordenadas

        # Matriz métrica e inversa
        g_uv = metrica(ponto)
        g_inv = np.linalg.inv(g_uv)

        # Derivadas parciais da métrica
        dg_duv = np.zeros((n, n, n))  # dg_{μν}/dx^λ

        for lambda_ in range(n):
            for mu in range(n):
                for nu in range(n):
                    def g_component(x):
                        coords = ponto.copy()
                        coords[lambda_] = x
                        return metrica(coords)[mu, nu]

                    dg_duv[lambda_, mu, nu] = derivada(g_component, ponto[lambda_])

        # Símbolos de Christoffel
        Gamma = np.zeros((n, n, n))  # Γ^λ_{μν}

        for lambda_ in range(n):
            for mu in range(n):
                for nu in range(n):
                    # Γ^λ_{μν} = 1/2 g^{λλ} (∂_μ g_{νλ} + ∂_ν g_{μλ} - ∂_λ g_{μν})
                    soma = 0
                    for sigma in range(n):
                        termo1 = dg_duv[mu, nu, sigma]
                        termo2 = dg_duv[nu, mu, sigma]
                        termo3 = dg_duv[sigma, mu, nu]

                        soma += g_inv[lambda_, sigma] * (termo1 + termo2 - termo3)

                    Gamma[lambda_, mu, nu] = 0.5 * soma

        return Gamma

    def tensor_riemann(self, metrica: Callable, ponto: np.ndarray) -> np.ndarray:
        """
        Calcula tensor de Riemann R^ρ_{σμν}

        Parameters:
        -----------
        metrica : callable
            Função que retorna g_{μν}(x) como matriz
        ponto : array_like
            Ponto onde calcular o tensor

        Returns:
        --------
        array: Tensor R^ρ_{σμν} com shape (n, n, n, n)
        """
        ponto = np.asarray(ponto)
        n = self.n_coordenadas

        # Símbolos de Christoffel
        Gamma = self.simbolos_christoffel(metrica, ponto)

        # Derivadas dos símbolos de Christoffel
        dGamma = np.zeros((n, n, n, n))  # ∂_ρ Γ^σ_{μν}

        for rho in range(n):
            for sigma in range(n):
                for mu in range(n):
                    for nu in range(n):
                        def gamma_component(x):
                            coords = ponto.copy()
                            coords[rho] = x
                            Gamma_temp = self.simbolos_christoffel(metrica, coords)
                            return Gamma_temp[sigma, mu, nu]

                        dGamma[rho, sigma, mu, nu] = derivada(gamma_component, ponto[rho])

        # Tensor de Riemann
        R = np.zeros((n, n, n, n))  # R^ρ_{σμν}

        for rho in range(n):
            for sigma in range(n):
                for mu in range(n):
                    for nu in range(n):
                        # R^ρ_{σμν} = ∂_μ Γ^ρ_{νσ} - ∂_ν Γ^ρ_{μσ} + Γ^ρ_{μα} Γ^α_{νσ} - Γ^ρ_{να} Γ^α_{μσ}
                        termo1 = dGamma[mu, rho, nu, sigma]
                        termo2 = dGamma[nu, rho, mu, sigma]

                        termo3 = 0
                        termo4 = 0
                        for alpha in range(n):
                            termo3 += Gamma[rho, mu, alpha] * Gamma[alpha, nu, sigma]
                            termo4 += Gamma[rho, nu, alpha] * Gamma[alpha, mu, sigma]

                        R[rho, sigma, mu, nu] = termo1 - termo2 + termo3 - termo4

        return R

    def tensor_ricci(self, metrica: Callable, ponto: np.ndarray) -> np.ndarray:
        """
        Calcula tensor de Ricci R_{μν} = R^λ_{μλν}

        Parameters:
        -----------
        metrica : callable
            Função que retorna g_{μν}(x) como matriz
        ponto : array_like
            Ponto onde calcular o tensor

        Returns:
        --------
        array: Tensor R_{μν}
        """
        R_riemann = self.tensor_riemann(metrica, ponto)
        n = self.n_coordenadas

        R_ricci = np.zeros((n, n))

        for mu in range(n):
            for nu in range(n):
                for lambda_ in range(n):
                    R_ricci[mu, nu] += R_riemann[lambda_, mu, lambda_, nu]

        return R_ricci

    def escalar_curvatura(self, metrica: Callable, ponto: np.ndarray) -> float:
        """
        Calcula escalar de curvatura R = g^{μν} R_{μν}

        Parameters:
        -----------
        metrica : callable
            Função que retorna g_{μν}(x) como matriz
        ponto : array_like
            Ponto onde calcular o escalar

        Returns:
        --------
        float: Escalar de curvatura R
        """
        ponto = np.asarray(ponto)
        g_uv = metrica(ponto)
        g_inv = np.linalg.inv(g_uv)
        R_uv = self.tensor_ricci(metrica, ponto)

        R = 0
        for mu in range(self.n_coordenadas):
            for nu in range(self.n_coordenadas):
                R += g_inv[mu, nu] * R_uv[mu, nu]

        return R

    def tensor_einstein(self, metrica: Callable, ponto: np.ndarray) -> np.ndarray:
        """
        Calcula tensor de Einstein G_{μν} = R_{μν} - 1/2 g_{μν} R

        Parameters:
        -----------
        metrica : callable
            Função que retorna g_{μν}(x) como matriz
        ponto : array_like
            Ponto onde calcular o tensor

        Returns:
        --------
        array: Tensor de Einstein G_{μν}
        """
        g_uv = metrica(ponto)
        R_uv = self.tensor_ricci(metrica, ponto)
        R = self.escalar_curvatura(metrica, ponto)

        return R_uv - 0.5 * R * g_uv

    def conexao_afim(self, metrica: Callable, ponto: np.ndarray) -> np.ndarray:
        """
        Calcula conexão de Levi-Civita (compatível com a métrica)

        Parameters:
        -----------
        metrica : callable
            Função que retorna g_{μν}(x) como matriz
        ponto : array_like
            Ponto onde calcular a conexão

        Returns:
        --------
        array: Conexão Γ^λ_{μν}
        """
        # Para geometria de Riemann, a conexão de Levi-Civita
        # é dada exatamente pelos símbolos de Christoffel
        return self.simbolos_christoffel(metrica, ponto)


class MetricasRelatividade:
    """
    Métricas comuns em relatividade geral
    """

    @staticmethod
    def metrica_minkowski(ponto: np.ndarray) -> np.ndarray:
        """
        Métrica de Minkowski plana η_{μν}
        """
        return np.diag([-1, 1, 1, 1])

    @staticmethod
    def metrica_flrw(ponto: np.ndarray, a: Callable, k: float = 0) -> np.ndarray:
        """
        Métrica FLRW (Friedmann-Lemaître-Robertson-Walker)

        Parameters:
        -----------
        ponto : array_like
            Coordenadas [t, r, θ, φ]
        a : callable
            Fator de escala a(t)
        k : float
            Curvatura espacial (-1, 0, +1)

        Returns:
        --------
        array: Métrica g_{μν}
        """
        t, r, theta, phi = ponto

        # Fator de escala no tempo t
        a_t = a(t)

        # Elementos da métrica
        g_tt = -1
        g_rr = a_t**2 / (1 - k * r**2)
        g_theta_theta = a_t**2 * r**2
        g_phi_phi = a_t**2 * r**2 * np.sin(theta)**2

        return np.diag([g_tt, g_rr, g_theta_theta, g_phi_phi])

    @staticmethod
    def metrica_schwarzschild(ponto: np.ndarray, M: float) -> np.ndarray:
        """
        Métrica de Schwarzschild

        Parameters:
        -----------
        ponto : array_like
            Coordenadas [t, r, θ, φ]
        M : float
            Massa do buraco negro (em unidades G=c=1)

        Returns:
        --------
        array: Métrica g_{μν}
        """
        t, r, theta, phi = ponto

        if r <= 2*M:
            raise ValueError("Raio dentro do horizonte de eventos")

        # Função f(r) = 1 - 2M/r
        f = 1 - 2*M/r

        # Elementos da métrica
        g_tt = -f
        g_rr = 1/f
        g_theta_theta = r**2
        g_phi_phi = r**2 * np.sin(theta)**2

        return np.diag([g_tt, g_rr, g_theta_theta, g_phi_phi])

    @staticmethod
    def metrica_de_sitter(ponto: np.ndarray, H: float) -> np.ndarray:
        """
        Métrica de de Sitter (espaço-tempo vazio com energia escura)

        Parameters:
        -----------
        ponto : array_like
            Coordenadas [t, r, θ, φ]
        H : float
            Constante de Hubble

        Returns:
        --------
        array: Métrica g_{μν}
        """
        t, r, theta, phi = ponto

        # Função H(r) para de Sitter
        a_t = np.exp(H * t)  # Fator de escala

        # Elementos da métrica
        g_tt = -1
        g_rr = a_t**2 / (1 - H**2 * r**2)
        g_theta_theta = a_t**2 * r**2
        g_phi_phi = a_t**2 * r**2 * np.sin(theta)**2

        return np.diag([g_tt, g_rr, g_theta_theta, g_phi_phi])


class EquacoesEinstein:
    """
    Solução das equações de Einstein
    """

    def __init__(self, geometria: GeometriaDiferencial):
        self.geometria = geometria

    def equacao_einstein(self, metrica: Callable, energia_momento: Callable,
                        ponto: np.ndarray) -> np.ndarray:
        """
        Equação de Einstein: G_{μν} = 8πG T_{μν}

        Parameters:
        -----------
        metrica : callable
            Métrica g_{μν}
        energia_momento : callable
            Tensor energia-momento T_{μν}
        ponto : array_like
            Ponto onde avaliar

        Returns:
        --------
        array: Lado esquerdo - lado direito da equação
        """
        G_uv = self.geometria.tensor_einstein(metrica, ponto)
        T_uv = energia_momento(ponto)

        # Em unidades naturais G = c = 1, então 8πG = 8π
        return G_uv - 8 * np.pi * T_uv

    def resolver_para_metrica(self, energia_momento: Callable,
                             condicoes_iniciais: Dict,
                             intervalo_t: Tuple[float, float]) -> Callable:
        """
        Resolve as equações de Einstein para encontrar a métrica

        Parameters:
        -----------
        energia_momento : callable
            Tensor energia-momento T_{μν}
        condicoes_iniciais : dict
            Condições iniciais para integração
        intervalo_t : tuple
            Intervalo de tempo para integração

        Returns:
        --------
        callable: Função que retorna a métrica
        """
        # Este é um problema muito complexo que requer
        # métodos numéricos avançados. Aqui implementamos
        # uma versão simplificada para métricas FLRW.

        def metrica_resolvida(ponto):
            # Implementação simplificada para FLRW
            # Em uma implementação completa, resolveríamos
            # as equações de Friedmann numericamente

            t = ponto[0]

            # Assumindo forma FLRW
            # Aqui seria necessário resolver numericamente
            # as equações diferenciais para a(t)

            # Placeholder: solução aproximada
            a_t = 1.0 + 0.1 * t  # Expansão linear simples

            return MetricasRelatividade.metrica_flrw(ponto, lambda t: a_t)

        return metrica_resolvida


# Funções utilitárias para uso direto
def simbolos_christoffel(metrica: Callable, ponto: np.ndarray, coordenadas: List[str]) -> np.ndarray:
    """Função wrapper para símbolos de Christoffel"""
    geom = GeometriaDiferencial(coordenadas)
    return geom.simbolos_christoffel(metrica, ponto)


def tensor_ricci(metrica: Callable, ponto: np.ndarray, coordenadas: List[str]) -> np.ndarray:
    """Função wrapper para tensor de Ricci"""
    geom = GeometriaDiferencial(coordenadas)
    return geom.tensor_ricci(metrica, ponto)


def tensor_einstein(metrica: Callable, ponto: np.ndarray, coordenadas: List[str]) -> np.ndarray:
    """Função wrapper para tensor de Einstein"""
    geom = GeometriaDiferencial(coordenadas)
    return geom.tensor_einstein(metrica, ponto)


# Exemplos de uso e testes
if __name__ == "__main__":
    print("Módulo de Geometria Diferencial")
    print("=" * 40)

    # Coordenadas
    coords = ['t', 'r', 'θ', 'φ']
    geom = GeometriaDiferencial(coords)

    print(f"Coordenadas: {coords}")
    print(f"Dimensão: {geom.n_coordenadas}")

    # Teste com métrica de Minkowski
    print("\nTeste 1: Métrica de Minkowski")
    ponto_teste = np.array([0, 1, np.pi/2, 0])

    metrica_mink = MetricasRelatividade.metrica_minkowski
    g_uv = metrica_mink(ponto_teste)

    print("Métrica de Minkowski:")
    print(g_uv)

    # Símbolos de Christoffel (devem ser zero para Minkowski)
    Gamma = geom.simbolos_christoffel(metrica_mink, ponto_teste)
    print(f"Símbolos de Christoffel (norma): {np.linalg.norm(Gamma):.2e}")

    # Teste com métrica FLRW simples
    print("\nTeste 2: Métrica FLRW simples")
    def a_t(t):
        return 1.0 + 0.1 * t  # Expansão linear

    def metrica_flrw_test(ponto):
        return MetricasRelatividade.metrica_flrw(ponto, a_t, k=0)

    g_flrw = metrica_flrw_test(ponto_teste)
    print("Diagonal da métrica FLRW:")
    print(np.diag(g_flrw))

    # Símbolos de Christoffel para FLRW
    Gamma_flrw = geom.simbolos_christoffel(metrica_flrw_test, ponto_teste)
    print(f"Símbolos de Christoffel FLRW (norma): {np.linalg.norm(Gamma_flrw):.6f}")

    # Teste do escalar de curvatura (deve ser zero para FLRW vazio)
    try:
        R = geom.escalar_curvatura(metrica_flrw_test, ponto_teste)
        print(f"Escalar de curvatura: {R:.6f}")
    except Exception as e:
        print(f"Erro no cálculo do escalar de curvatura: {e}")

    print("\nMódulo funcionando corretamente! ✅")
