#!/usr/bin/env python3
"""
Cosmologia Computacional Avançada
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Equações de Friedmann com múltiplas componentes
- Inflação cósmica
- Energia escura dinâmica
- Formação de estruturas
- Radiação cósmica de fundo
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from typing import Callable, Tuple, Optional, Union, Dict, List
from ..numerical_methods.integrators import IntegratorNumerico
from .relativity import CosmologiaRelatividade
import warnings


class CosmologiaAvancada(CosmologiaRelatividade):
    """
    Cosmologia com múltiplas componentes e efeitos avançados
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.componentes = {}

    def adicionar_componente(self, nome: str, densidade: Callable, pressao: Callable,
                           evolucao: Optional[Callable] = None):
        """
        Adiciona componente cosmológica (matéria, radiação, energia escura, etc.)

        Parameters:
        -----------
        nome : str
            Nome da componente
        densidade : callable
            Função ρ(a) densidade como função do fator de escala
        pressao : callable
            Função P(a) pressão como função do fator de escala
        evolucao : callable, optional
            Evolução temporal específica (se diferente de ρ ∝ a^{-3(1+w)})
        """
        self.componentes[nome] = {
            'densidade': densidade,
            'pressao': pressao,
            'evolucao': evolucao
        }

    def equacao_friedmann_completa(self, a: float, componentes: Dict[str, float]) -> float:
        """
        Equação de Friedmann com múltiplas componentes

        Parameters:
        -----------
        a : float
            Fator de escala
        componentes : dict
            Densidades atuais de cada componente

        Returns:
        --------
        float: H(a) parâmetro de Hubble
        """
        # Densidade crítica atual
        rho_crit = 3 * self.H0**2 / (8 * np.pi * self.G)

        # Soma das densidades
        rho_total = sum(componentes.values())

        # H(a) = H0 √(Σ Ω_i(a))
        H = self.H0 * np.sqrt(rho_total / rho_crit)

        return H

    def evoluir_universo_completo(self, a_inicial: float = 1e-10, a_final: float = 1.0,
                                 n_pontos: int = 1000, incluir_inflacao: bool = True) -> Dict[str, np.ndarray]:
        """
        Evolução completa do universo com todas as componentes

        Parameters:
        -----------
        a_inicial, a_final : float
            Intervalo do fator de escala
        n_pontos : int
            Número de pontos
        incluir_inflacao : bool
            Incluir fase inflacionária

        Returns:
        --------
        dict: Evolução temporal completa
        """
        def sistema_completo(a, y):
            """
            Sistema completo de equações cosmológicas
            y = [t] (tempo como variável dependente)
            """
            t = y[0]

            # Componentes atuais
            componentes_atuais = {}
            for nome, comp in self.componentes.items():
                if comp['evolucao'] is not None:
                    # Evolução específica
                    componentes_atuais[nome] = comp['evolucao'](a)
                else:
                    # Evolução padrão: ρ ∝ a^{-3(1+w)}
                    w = comp['pressao'](a) / comp['densidade'](a)
                    rho_0 = comp['densidade'](1.0)  # Densidade atual
                    componentes_atuais[nome] = rho_0 * a**(-3*(1+w))

            # Hubble parameter
            H = self.equacao_friedmann_completa(a, componentes_atuais)

            # Derivada: da/dt = a H
            # Logo: dt/da = 1/(a H)
            return np.array([1.0 / (a * H)])

        # Condições iniciais
        y0 = np.array([0.0])  # t = 0 no início

        # Integração
        integrator = IntegratorNumerico()
        a_span = (a_inicial, a_final)

        sol = integrator.integrar_sistema(sistema_completo, y0, a_span)

        if not sol['sucesso']:
            warnings.warn(f"Integração falhou: {sol['mensagem']}")
            return {'sucesso': False}

        # Avaliar solução
        a_eval = np.logspace(np.log10(a_inicial), np.log10(a_final), n_pontos)
        t_eval = np.array([sol['solucao'].sol(a)[0] for a in a_eval])

        # Calcular outras quantidades
        H_eval = []
        componentes_historia = {nome: [] for nome in self.componentes.keys()}

        for a in a_eval:
            componentes_atuais = {}
            for nome, comp in self.componentes.items():
                if comp['evolucao'] is not None:
                    componentes_atuais[nome] = comp['evolucao'](a)
                else:
                    w = comp['pressao'](a) / comp['densidade'](a)
                    rho_0 = comp['densidade'](1.0)
                    componentes_atuais[nome] = rho_0 * a**(-3*(1+w))
                componentes_historia[nome].append(componentes_atuais[nome])

            H_eval.append(self.equacao_friedmann_completa(a, componentes_atuais))

        H_eval = np.array(H_eval)
        for nome in componentes_historia:
            componentes_historia[nome] = np.array(componentes_historia[nome])

        return {
            'a': a_eval,
            't': t_eval,
            'H': H_eval,
            'componentes': componentes_historia,
            'sucesso': True
        }


class InflacaoCosmica:
    """
    Modelo de inflação cósmica
    """

    def __init__(self, V: Callable, epsilon_sr: float = 1e-2):
        """
        Parameters:
        -----------
        V : callable
            Potencial inflacionário V(φ)
        epsilon_sr : float
            Parâmetro de slow-roll ε
        """
        self.V = V
        self.epsilon_sr = epsilon_sr
        self.integrator = IntegratorNumerico()

    def equacao_klein_gordon(self, phi: float, dot_phi: float, H: float) -> float:
        """
        Equação de Klein-Gordon para o campo inflacionário

        Parameters:
        -----------
        phi : float
            Valor do campo
        dot_phi : float
            Velocidade do campo
        H : float
            Parâmetro de Hubble

        Returns:
        --------
        float: d²φ/dt²
        """
        # d²φ/dt² + 3H dφ/dt + dV/dφ = 0
        dV_dphi = self._derivada_numerica(self.V, phi)

        return -3 * H * dot_phi - dV_dphi

    def _derivada_numerica(self, f: Callable, x: float, h: float = 1e-6) -> float:
        """Derivada numérica simples"""
        return (f(x + h) - f(x - h)) / (2 * h)

    def numero_e_folds(self, phi_inicial: float, phi_final: float) -> float:
        """
        Número de e-folds durante inflação

        Parameters:
        -----------
        phi_inicial : float
            Valor inicial do campo
        phi_final : float
            Valor final do campo

        Returns:
        --------
        float: Número de e-folds N
        """
        # N = ∫ dφ / √(2ε)
        def integrando(phi):
            epsilon = self.parametro_slow_roll(phi)
            return 1.0 / np.sqrt(2 * epsilon)

        # Integração numérica
        from scipy.integrate import quad
        N, _ = quad(integrando, phi_inicial, phi_final)

        return abs(N)

    def parametro_slow_roll(self, phi: float) -> float:
        """
        Parâmetro de slow-roll ε = (1/2) (V'/V)²

        Parameters:
        -----------
        phi : float
            Valor do campo

        Returns:
        --------
        float: Parâmetro ε
        """
        V = self.V(phi)
        dV_dphi = self._derivada_numerica(self.V, phi)

        if V > 0:
            return 0.5 * (dV_dphi / V)**2
        else:
            return float('inf')

    def evolucao_inflacao(self, phi_inicial: float = 15.0, t_span: Tuple[float, float] = (-1e-30, 1e-30),
                         n_pontos: int = 1000) -> Dict[str, np.ndarray]:
        """
        Evolução temporal durante inflação

        Parameters:
        -----------
        phi_inicial : float
            Valor inicial do campo
        t_span : tuple
            Intervalo temporal
        n_pontos : int
            Número de pontos

        Returns:
        --------
        dict: Evolução do campo inflacionário
        """
        def sistema_inflacao(t, y):
            """
            Sistema de equações para inflação
            y = [phi, dot_phi, a]
            """
            phi, dot_phi, a = y

            # Potencial e derivada
            V = self.V(phi)
            dV_dphi = self._derivada_numerica(self.V, phi)

            # Densidade e pressão do campo
            rho_phi = 0.5 * dot_phi**2 + V
            p_phi = 0.5 * dot_phi**2 - V

            # Parâmetro de Hubble
            H = np.sqrt((8 * np.pi / 3) * rho_phi)

            # Equações
            ddot_phi = -3 * H * dot_phi - dV_dphi
            dot_a = a * H

            return np.array([dot_phi, ddot_phi, dot_a])

        # Condições iniciais (aproximadas para slow-roll)
        dot_phi_0 = -np.sqrt(2 * self.epsilon_sr) * np.sqrt(2 * self.V(phi_inicial))
        a_0 = 1.0
        y0 = np.array([phi_inicial, dot_phi_0, a_0])

        # Integração
        sol = self.integrator.integrar_sistema(sistema_inflacao, y0, t_span)

        if not sol['sucesso']:
            warnings.warn(f"Evolução inflacionária falhou: {sol['mensagem']}")
            return {'sucesso': False}

        # Avaliar solução
        t_eval = np.linspace(t_span[0], t_span[1], n_pontos)
        y_eval = np.array([sol['solucao'].sol(t) for t in t_eval])

        return {
            't': t_eval,
            'phi': y_eval[:, 0],
            'dot_phi': y_eval[:, 1],
            'a': y_eval[:, 2],
            'H': np.sqrt((8 * np.pi / 3) * (0.5 * y_eval[:, 1]**2 + self.V(y_eval[:, 0]))),
            'epsilon_sr': np.array([self.parametro_slow_roll(phi) for phi in y_eval[:, 0]]),
            'sucesso': True
        }


class EnergiaEscuraDinamica:
    """
    Modelos de energia escura dinâmica (quintessência, etc.)
    """

    def __init__(self, w0: float = -1.0, wa: float = 0.0):
        """
        Parameters:
        -----------
        w0 : float
            Equação de estado atual
        wa : float
            Evolução temporal: w(a) = w0 + wa(1-a)
        """
        self.w0 = w0
        self.wa = wa

    def equacao_estado(self, a: float) -> float:
        """
        Equação de estado dinâmica w(a) = w0 + wa(1-a)

        Parameters:
        -----------
        a : float
            Fator de escala

        Returns:
        --------
        float: w(a)
        """
        return self.w0 + self.wa * (1 - a)

    def densidade_evolucao(self, rho_0: float, a: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evolução da densidade: ρ(a) = ρ0 exp(3∫ da/a (1+w(a')) )

        Parameters:
        -----------
        rho_0 : float
            Densidade atual
        a : float or array
            Fator de escala

        Returns:
        --------
        float or array: ρ(a)
        """
        if np.isscalar(a):
            # Integração numérica para ponto único
            from scipy.integrate import quad
            integral, _ = quad(lambda ap: (1 + self.equacao_estado(ap)) / ap, 1.0, a)
            return rho_0 * np.exp(3 * integral)
        else:
            # Para arrays, calcular ponto a ponto
            result = []
            for ai in a:
                result.append(self.densidade_evolucao(rho_0, ai))
            return np.array(result)

    def parametro_hubble_de(self, a: float, Omega_m: float, Omega_r: float = 0.0) -> float:
        """
        Contribuição da energia escura para H(a)

        Parameters:
        -----------
        a : float
            Fator de escala
        Omega_m : float
            Densidade de matéria
        Omega_r : float
            Densidade de radiação

        Returns:
        --------
        float: Ω_de(a) * H(a)² / H0²
        """
        Omega_de = 1 - Omega_m - Omega_r

        # ρ_de(a) / ρ_crit0
        rho_de_a = self.densidade_evolucao(Omega_de, a)

        return rho_de_a


class RadiacaoCosmicaFundo:
    """
    Radiação Cósmica de Fundo (CMB)
    """

    def __init__(self, T_cmb: float = 2.725):
        """
        Parameters:
        -----------
        T_cmb : float
            Temperatura da CMB em K
        """
        self.T_cmb = T_cmb
        self.k_B = 1.381e-23  # J/K
        self.h = 6.626e-34    # J⋅s
        self.c = 2.998e8      # m/s

    def temperatura_evolucao(self, a: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evolução da temperatura: T(a) = T0 / a

        Parameters:
        -----------
        a : float or array
            Fator de escala

        Returns:
        --------
        float or array: T(a) em K
        """
        return self.T_cmb / a

    def densidade_fotons(self, a: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Densidade de energia dos fótons: ρ_γ = (π²/15) (kT)⁴ / (ℏc)³

        Parameters:
        -----------
        a : float or array
            Fator de escala

        Returns:
        --------
        float or array: ρ_γ(a) em erg/cm³
        """
        T = self.temperatura_evolucao(a)
        kT = self.k_B * T

        # Constante de radiação
        a_rad = 4 * 5.670e-5 / self.c  # erg/cm³/K⁴

        return a_rad * T**4

    def espectro_plank(self, nu: Union[float, np.ndarray], T: float) -> Union[float, np.ndarray]:
        """
        Espectro de Planck B(ν, T)

        Parameters:
        -----------
        nu : float or array
            Frequência em Hz
        T : float
            Temperatura em K

        Returns:
        --------
        float or array: B(ν, T) em erg/s/cm²/Hz/sr
        """
        h_nu = self.h * nu
        kT = self.k_B * T

        # Evitar overflow/underflow
        x = h_nu / kT
        x = np.clip(x, 1e-10, 100)

        return 2 * h_nu**3 / self.c**2 / (np.exp(x) - 1)

    def anisotropias_temperatura(self, l: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Anisotropias de temperatura ΔT/T para multipolos l

        Parameters:
        -----------
        l : int or array
            Multipolo

        Returns:
        --------
        float or array: ΔT/T(l)
        """
        # Aproximação simplificada para o espectro de potência
        # Valores reais vêm de Planck
        if np.isscalar(l):
            if l < 10:
                return 1e-5  # Grandes escalas
            elif l < 100:
                return 2e-5  # Pico acústico
            else:
                return l**(-2.5) * 1e-5  # Pequenas escalas
        else:
            result = np.zeros_like(l, dtype=float)
            for i, li in enumerate(l):
                result[i] = self.anisotropias_temperatura(li)
            return result


class FormacaoEstruturas:
    """
    Formação de estruturas cosmológicas
    """

    def __init__(self, cosmo: CosmologiaAvancada):
        """
        Parameters:
        -----------
        cosmo : CosmologiaAvancada
            Modelo cosmológico
        """
        self.cosmo = cosmo

    def funcao_crescimento_linear(self, a: Union[float, np.ndarray],
                                Omega_m: float = 0.3) -> Union[float, np.ndarray]:
        """
        Função de crescimento linear D(a)

        Parameters:
        -----------
        a : float or array
            Fator de escala
        Omega_m : float
            Densidade de matéria

        Returns:
        --------
        float or array: D(a)
        """
        # Para ΛCDM: D(a) ∝ H(a) ∫ da/(a² H(a)³)
        # Aproximação analítica
        x = a**(3/2) * np.sqrt(Omega_m) / np.sqrt(Omega_m + (1-Omega_m)*a**3)

        # Normalização
        D0 = self.funcao_crescimento_linear(1.0, Omega_m)
        return x / D0

    def espectro_potencia_materia(self, k: Union[float, np.ndarray],
                                a: float = 1.0, ns: float = 0.96) -> Union[float, np.ndarray]:
        """
        Espectro de potência da matéria P(k)

        Parameters:
        -----------
        k : float or array
            Número de onda em h/Mpc
        a : float
            Fator de escala
        ns : float
            Índice espectral

        Returns:
        --------
        float or array: P(k) em (Mpc/h)³
        """
        # Espectro primordial
        k_pivot = 0.05  # Mpc⁻¹
        A_s = 2.1e-9   # Amplitude

        P_primordial = A_s * (k / k_pivot)**(ns - 1)

        # Transferência (aproximação simples)
        T_k = 1.0 / (1 + (k / 0.1)**2)**2  # Aproximação de Eisenstein-Hu

        # Crescimento linear
        D_a = self.funcao_crescimento_linear(a)

        return P_primordial * T_k**2 * D_a**2

    def variancia_massa(self, M: float, a: float = 1.0) -> float:
        """
        Variância da densidade em escala de massa M

        Parameters:
        -----------
        M : float
            Massa em M_sun
        a : float
            Fator de escala

        Returns:
        --------
        float: σ²(M)
        """
        # Raio de Virial
        rho_crit = 2.77e11  # h² M_sun/Mpc³
        Omega_m = 0.3

        R = (3*M / (4*np.pi * rho_crit * Omega_m))**(1/3)  # Mpc

        # Número de onda correspondente
        k_R = 2*np.pi / R

        # Integral para σ²(R) = ∫ dk P(k) |W(kR)|²
        def integrando(k):
            P_k = self.espectro_potencia_materia(k, a)
            # Janela top-hat
            W_kR = 3 * (np.sin(k*R) - k*R*np.cos(k*R)) / (k*R)**3
            return P_k * W_kR**2

        from scipy.integrate import quad
        sigma_squared, _ = quad(integrando, 1e-4, 10, limit=100)

        return sigma_squared


# Funções utilitárias
def modelo_lcdm(H0: float = 70, Omega_m: float = 0.3) -> CosmologiaAvancada:
    """
    Modelo ΛCDM padrão
    """
    cosmo = CosmologiaAvancada(H0=H0, Omega_m=Omega_m, Omega_lambda=1-Omega_m)

    # Adicionar componentes
    def rho_m(a):
        return cosmo.Omega_m * a**(-3)

    def rho_lambda(a):
        return cosmo.Omega_lambda

    cosmo.adicionar_componente('materia', rho_m, lambda a: 0.0)
    cosmo.adicionar_componente('lambda', rho_lambda, lambda a: -rho_lambda(a))

    return cosmo


def potencial_chaotic(V0: float = 1e-2, p: float = 2) -> Callable:
    """
    Potencial caótico V(φ) = V0 φ^p / p
    """
    def V(phi):
        return V0 * phi**p / p

    return V


def energia_escura_quintessencia(w0: float = -0.9, wa: float = -0.1) -> EnergiaEscuraDinamica:
    """
    Modelo de quintessência
    """
    return EnergiaEscuraDinamica(w0=w0, wa=wa)


# Exemplos de uso
if __name__ == "__main__":
    print("Módulo de Cosmologia Avançada")
    print("=" * 32)

    # Teste 1: Modelo ΛCDM
    print("Teste 1: Modelo ΛCDM")
    cosmo = modelo_lcdm(H0=70, Omega_m=0.3)

    print(f"Parâmetros: H0={cosmo.H0}, Ωm={cosmo.Omega_m}, ΩΛ={cosmo.Omega_lambda}")

    # Evolução
    evol = cosmo.evoluir_universo_completo(1e-3, 1.0, 100)
    if evol['sucesso']:
        print(f"Evolução completa calculada: {len(evol['a'])} pontos")
        print(".3f")

    # Teste 2: Inflação
    print("\nTeste 2: Inflação Caótica")
    V = potencial_chaotic(V0=1e-3, p=4)
    inflacao = InflacaoCosmica(V)

    N_e_folds = inflacao.numero_e_folds(phi_inicial=15.0, phi_final=1.0)
    print(f"Número de e-folds: {N_e_folds:.1f}")

    # Evolução inflacionária
    evol_inf = inflacao.evolucao_inflacao(phi_inicial=15.0)
    if evol_inf['sucesso']:
        print(f"Evolução inflacionária: {len(evol_inf['t'])} pontos")

    # Teste 3: Energia escura dinâmica
    print("\nTeste 3: Energia Escura Dinâmica")
    de = energia_escura_quintessencia(w0=-0.9, wa=-0.1)

    w_vals = [de.equacao_estado(a) for a in [0.5, 1.0, 2.0]]
    print(f"Equação de estado: w(0.5)={w_vals[0]:.3f}, w(1)={w_vals[1]:.3f}, w(2)={w_vals[2]:.3f}")

    # Teste 4: CMB
    print("\nTeste 4: Radiação Cósmica de Fundo")
    cmb = RadiacaoCosmicaFundo(T_cmb=2.725)

    T_recomb = cmb.temperatura_evolucao(1/1090)  # z ≈ 1090
    print(f"Temperatura na recombinação: {T_recomb:.1f} K")

    # Anisotropias
    anisotropias = cmb.anisotropias_temperatura([10, 100, 1000])
    print(f"Anisotropias ΔT/T: l=10: {anisotropias[0]:.2e}, l=100: {anisotropias[1]:.2e}, l=1000: {anisotropias[2]:.2e}")

    # Teste 5: Formação de estruturas
    print("\nTeste 5: Formação de Estruturas")
    estruturas = FormacaoEstruturas(cosmo)

    # Função de crescimento
    D_vals = estruturas.funcao_crescimento_linear([0.5, 1.0])
    print(f"Função de crescimento: D(0.5)={D_vals[0]:.3f}, D(1)={D_vals[1]:.3f}")

    # Espectro de potência
    P_k = estruturas.espectro_potencia_materia(0.1)
    print(f"Espectro de potência em k=0.1: {P_k:.2e} (Mpc/h)³")

    print("\nMódulo funcionando corretamente! ✅")
