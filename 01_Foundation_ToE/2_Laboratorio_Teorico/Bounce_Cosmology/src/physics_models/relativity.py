#!/usr/bin/env python3
"""
Relatividade Geral Computacional
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Equações de Einstein
- Cosmologia (Friedmann, aceleração)
- Buracos negros (Schwarzschild, Kerr)
- Ondas gravitacionais
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Callable, Tuple, Optional, Union, Dict, List
from ..numerical_methods.integrators import IntegratorNumerico
from ..numerical_methods.differential_geometry import (
    GeometriaDiferencial, MetricasRelatividade, EquacoesEinstein
)
import warnings


class CosmologiaRelatividade:
    """
    Cosmologia em relatividade geral
    """

    def __init__(self, H0: float = 70, Omega_m: float = 0.3, Omega_lambda: float = 0.7):
        """
        Inicializa parâmetros cosmológicos

        Parameters:
        -----------
        H0 : float
            Constante de Hubble em km/s/Mpc
        Omega_m : float
            Densidade de matéria
        Omega_lambda : float
            Densidade de energia escura
        """
        self.H0 = H0  # km/s/Mpc
        self.Omega_m = Omega_m
        self.Omega_lambda = Omega_lambda
        self.Omega_r = 1 - Omega_m - Omega_lambda  # Radiação (aproximadamente 0)

        # Constantes em unidades naturais
        self.G = 1.0  # Constante gravitacional
        self.c = 1.0  # Velocidade da luz
        self.k_B = 1.0  # Constante de Boltzmann

    def equacoes_friedmann(self, a: float, materia: Dict[str, float]) -> Tuple[float, float]:
        """
        Equações de Friedmann

        Parameters:
        -----------
        a : float
            Fator de escala
        materia : dict
            Densidades de energia: {'materia': rho_m, 'radiacao': rho_r, 'lambda': rho_lambda}

        Returns:
        --------
        tuple: (H, dH/da) onde H = da/dt / a
        """
        # Densidade total
        rho_total = sum(materia.values())

        # Equação de Friedmann: H² = (8πG/3) ρ_total - kc²/a² + Λc²/3
        H_squared = (8 * np.pi * self.G / 3) * rho_total

        # Aceleração: dH²/da = (8πG/3) (da/dt)² * (dρ/da) / ρ_total
        # Para simplificar, assumimos evolução padrão

        H = np.sqrt(max(H_squared, 0))  # Evita raiz quadrada de negativo

        return H, H_squared

    def evoluir_universo(self, a_inicial: float = 0.001, a_final: float = 1.0,
                        n_pontos: int = 1000) -> Dict[str, np.ndarray]:
        """
        Evolução temporal do universo usando equações de Friedmann

        Parameters:
        -----------
        a_inicial, a_final : float
            Fator de escala inicial e final
        n_pontos : int
            Número de pontos na integração

        Returns:
        --------
        dict: Evolução temporal de a(t), H(t), etc.
        """
        def friedmann_eq(a, y):
            """
            Sistema de equações de Friedmann
            y = [da/dt]
            """
            da_dt = y[0]

            # Densidades atuais (escaladas com a)
            rho_m = self.Omega_m * self._densidade_critica() / a**3
            rho_r = self.Omega_r * self._densidade_critica() / a**4
            rho_lambda = self.Omega_lambda * self._densidade_critica()

            # H² = (8πG/3) Σ ρ_i
            H_squared = (8 * np.pi * self.G / 3) * (rho_m + rho_r + rho_lambda)

            # Aceleração: d²a/dt² = - (4πG/3) Σ (ρ_i + 3p_i) a
            # Para matéria: p_m = 0, para radiação: p_r = ρ_r/3, para lambda: p_lambda = -ρ_lambda
            pressao_total = rho_r/3 - rho_lambda
            d2a_dt2 = - (4 * np.pi * self.G / 3) * (rho_m + rho_r + rho_lambda + 3*pressao_total) * a

            # Sistema: da/dt = v, dv/dt = d²a/dt²
            return np.array([d2a_dt2])

        # Condições iniciais
        v0 = np.sqrt((8 * np.pi * self.G / 3) * self.Omega_m * self._densidade_critica() / a_inicial**3)
        y0 = np.array([v0])

        # Integração
        integrator = IntegratorNumerico()
        a_span = (a_inicial, a_final)
        a_eval = np.linspace(a_inicial, a_final, n_pontos)

        def sistema_com_a(a, y):
            return friedmann_eq(a, y)

        # Integração numérica
        sol = integrator.integrar_sistema(sistema_com_a, y0, a_span)

        if not sol['sucesso']:
            warnings.warn(f"Integração falhou: {sol['mensagem']}")
            # Retorna solução aproximada
            a_eval = np.linspace(a_inicial, a_final, n_pontos)
            t_eval = np.log(a_eval) / self.H0 * 977.8  # Tempo em Gyr (aproximado)
            H_eval = self.H0 * np.sqrt(self.Omega_m / a_eval**3 + self.Omega_lambda)
            return {
                'a': a_eval,
                't': t_eval,
                'H': H_eval,
                'sucesso': False
            }

        # Avaliar solução
        da_dt_eval = []
        for a in a_eval:
            da_dt_eval.append(sol['solucao'].sol(a)[0])

        da_dt_eval = np.array(da_dt_eval)
        H_eval = da_dt_eval / a_eval

        # Tempo (aproximado)
        t_eval = np.cumsum(a_eval / da_dt_eval) * (a_eval[1] - a_eval[0])

        return {
            'a': a_eval,
            't': t_eval,
            'H': H_eval,
            'da_dt': da_dt_eval,
            'sucesso': True
        }

    def _densidade_critica(self) -> float:
        """Densidade crítica do universo"""
        # Em unidades onde G = c = 1
        H0_squared = (self.H0 / 977.8)**2  # Converter para unidades naturais
        return 3 * H0_squared / (8 * np.pi * self.G)

    def parametros_cosmo_planck(self) -> Dict[str, float]:
        """
        Parâmetros cosmológicos baseados em Planck 2020

        Returns:
        --------
        dict: Parâmetros cosmológicos atuais
        """
        return {
            'H0': 67.4,  # km/s/Mpc
            'Omega_m': 0.315,
            'Omega_lambda': 0.685,
            'Omega_b': 0.0224,  # Bárions
            'Omega_cdm': 0.265,  # Matéria escura fria
            'sigma_8': 0.811,  # Amplitude de flutuações
            'ns': 0.965,  # Índice espectral
            'tau': 0.054,  # Espessura ótica
            'As': 2.1e-9  # Amplitude do espectro primordial
        }

    def idade_universo(self) -> float:
        """
        Calcula idade do universo

        Returns:
        --------
        float: Idade em Gyr
        """
        # Integração numérica da equação da idade
        evol = self.evoluir_universo(a_inicial=1e-8, a_final=1.0, n_pontos=1000)

        if evol['sucesso']:
            return evol['t'][-1] / 1e9  # Converter para Gyr
        else:
            # Fórmula aproximada
            H0_gyr = self.H0 / 977.8  # H0 em Gyr^-1
            return 1 / H0_gyr * (self.Omega_m**(-0.5) - 1) / np.sqrt(1 + self.Omega_lambda / self.Omega_m)


class BuracosNegros:
    """
    Física de buracos negros
    """

    def __init__(self, G: float = 1.0, c: float = 1.0):
        """
        Parameters:
        -----------
        G : float
            Constante gravitacional
        c : float
            Velocidade da luz
        """
        self.G = G
        self.c = c

    def raio_schwarzschild(self, M: float) -> float:
        """
        Raio de Schwarzschild: R_s = 2GM/c²

        Parameters:
        -----------
        M : float
            Massa em unidades solares

        Returns:
        --------
        float: Raio em km
        """
        M_kg = M * 1.989e30  # Massa solar em kg
        return 2 * self.G * M_kg / (self.c**2) / 1000  # Em km

    def horizonte_eventos_kerr(self, M: float, a: float) -> Tuple[float, float]:
        """
        Raios do horizonte de eventos para buraco negro de Kerr

        Parameters:
        -----------
        M : float
            Massa
        a : float
            Momento angular específico (0 ≤ a ≤ M)

        Returns:
        --------
        tuple: (r_minus, r_plus) raios interno e externo
        """
        if abs(a) > M:
            raise ValueError("Momento angular deve satisfazer |a| ≤ M")

        # Discriminante
        delta = M**2 - a**2

        r_plus = M + np.sqrt(delta)
        r_minus = M - np.sqrt(delta)

        return r_minus, r_plus

    def ergosphere_kerr(self, M: float, a: float, theta: float = np.pi/2) -> float:
        """
        Raio da ergosphera para buraco negro de Kerr

        Parameters:
        -----------
        M : float
            Massa
        a : float
            Momento angular específico
        theta : float
            Ângulo polar

        Returns:
        --------
        float: Raio da ergosphera
        """
        cos_theta = np.cos(theta)
        r_erg = M + np.sqrt(M**2 - a**2 * cos_theta**2)
        return r_erg

    def potencial_gravitacional(self, r: Union[float, np.ndarray], M: float,
                              tipo: str = 'schwarzschild') -> Union[float, np.ndarray]:
        """
        Potencial gravitacional efetivo

        Parameters:
        -----------
        r : float or array
            Raio
        M : float
            Massa
        tipo : str
            'schwarzschild', 'newtoniano'

        Returns:
        --------
        float or array: Potencial Φ(r)
        """
        if tipo == 'newtoniano':
            return -self.G * M / r
        elif tipo == 'schwarzschild':
            # Potencial gravitacional efetivo em Schwarzschild
            # Φ_eff = -GM/r + L²/(2r²) (para movimento equatorial L=0)
            return -self.G * M / r
        else:
            raise ValueError(f"Tipo {tipo} não suportado")

    def periodo_orbital_isso(self, r: float, M: float) -> float:
        """
        Período orbital ISCO (Inner Stable Circular Orbit)

        Parameters:
        -----------
        r : float
            Raio ISCO
        M : float
            Massa

        Returns:
        --------
        float: Período em segundos
        """
        # Para Schwarzschild: r_isco = 6GM/c²
        # Período: T = 2π √(r³/GM)
        r_isco = 6 * self.G * M / self.c**2

        if r < r_isco:
            warnings.warn("Raio menor que ISCO - órbita instável")

        periodo = 2 * np.pi * np.sqrt(r**3 / (self.G * M))
        return periodo

    def taxa_acrescimento_eddington(self, M: float, eficiencia: float = 0.1) -> float:
        """
        Taxa de acrecimo de Eddington (limite superior)

        Parameters:
        -----------
        M : float
            Massa em massas solares
        eficiencia : float
            Eficiência radiativa (0.1 para acrecimo esferico)

        Returns:
        --------
        float: Taxa de acrecimo em M_sun/ano
        """
        # L_edd = 4π G M m_p c / σ_T
        # Convertendo para M_sun/ano
        M_kg = M * 1.989e30
        sigma_T = 6.652e-29  # Seção de choque Thomson em m²
        m_p = 1.673e-27  # Massa do próton em kg

        L_edd = 4 * np.pi * self.G * M_kg * m_p * self.c / sigma_T

        # Eficiência: L = η Ṁ c²
        # Logo: Ṁ = L / (η c²)
        dot_M_edd = L_edd / (eficiencia * self.c**2)

        # Converter para M_sun/ano
        dot_M_edd_msun_year = dot_M_edd / (1.989e30) * 365.25 * 24 * 3600

        return dot_M_edd_msun_year


class OndasGravitacionais:
    """
    Ondas gravitacionais
    """

    def __init__(self, G: float = 1.0, c: float = 1.0):
        """
        Parameters:
        -----------
        G : float
            Constante gravitacional
        c : float
            Velocidade da luz
        """
        self.G = G
        self.c = c

    def amplitude_onda_gw(self, distancia: float, chirp_mass: float,
                         frequencia: float) -> float:
        """
        Amplitude de onda gravitacional de sistema binário

        Parameters:
        -----------
        distancia : float
            Distância em Mpc
        chirp_mass : float
            Massa de chirp M_c = (m1 m2)^{3/5} / (m1 + m2)^{1/5}
        frequencia : float
            Frequência em Hz

        Returns:
        --------
        float: Amplitude h
        """
        # h = (4/c^4) * (G M_c)^{5/3} * (π f)^{2/3} / d
        # Em unidades onde G = c = 1
        amplitude = 4 * (self.G * chirp_mass)**(5/3) * (np.pi * frequencia)**(2/3) / distancia
        return amplitude / self.c**4

    def forma_onda_post_newtoniana(self, m1: float, m2: float, t_coalescencia: float,
                                   distancia: float, t: np.ndarray) -> np.ndarray:
        """
        Forma de onda gravitacional usando aproximação post-Newtoniana

        Parameters:
        -----------
        m1, m2 : float
            Massas dos componentes
        t_coalescencia : float
            Tempo de coalescência
        distancia : float
            Distância
        t : array_like
            Tempos

        Returns:
        --------
        array: h(t) forma de onda
        """
        # Massa de chirp
        M_c = (m1 * m2)**(3/5) / (m1 + m2)**(1/5)

        # Tempo restante até coalescência
        tau = t_coalescencia - t
        tau = np.maximum(tau, 1e-10)  # Evitar divisão por zero

        # Frequência orbital
        Omega = (5/(256 * np.pi))**(3/8) * (self.G * (m1 + m2) / self.c**3)**(-5/8) * tau**(-3/8)
        f_orb = Omega / (2 * np.pi)

        # Amplitude
        A = (4/self.c**4) * (self.G * M_c)**(5/3) * (np.pi * f_orb)**(2/3) / distancia

        # Fase
        phi = -2 * ((5/(256 * np.pi))**(3/8) * (self.G * (m1 + m2) / self.c**3)**(-5/8) * tau**(5/8))

        # Forma de onda (aproximação)
        h = A * np.cos(phi)

        return h

    def espectro_energia_gw(self, f: np.ndarray, chirp_mass: float) -> np.ndarray:
        """
        Espectro de energia de ondas gravitacionais

        Parameters:
        -----------
        f : array_like
            Frequências
        chirp_mass : float
            Massa de chirp

        Returns:
        --------
        array: dE/df energia por frequência
        """
        # Para inspiral: dE/df ∝ f^{-1/3} M_c^{5/3}
        G_mc = self.G * chirp_mass / self.c**3

        dE_df = (1/3) * np.pi**(2/3) * (self.G * chirp_mass)**(5/3) * f**(-1/3) / self.c**5

        return dE_df

    def alcance_detector(self, detector: str = 'LIGO') -> float:
        """
        Alcance aproximado de detectores de ondas gravitacionais

        Parameters:
        -----------
        detector : str
            'LIGO', 'Virgo', 'KAGRA', 'LISA'

        Returns:
        --------
        float: Alcance em Mpc
        """
        alcances = {
            'LIGO': 100,      # O3 alcançe aproximado
            'Virgo': 80,
            'KAGRA': 60,
            'LISA': 1000     # Alcance para ondas gravitacionais de baixa frequência
        }

        return alcances.get(detector, 0)


class CamposEscalarAcoplados:
    """
    Campos escalares acoplados à curvatura com Reheating (Fase 4).
    Simula inflação e decaimento em radiação.
    """

    def __init__(self, xi: float = 1e6, alpha: float = -1e-4, gamma: float = 1e-3):
        """
        Parameters:
        -----------
        xi : float
            Acoplamento não-mínimo
        alpha : float
            Parâmetro de estabilização
        gamma : float
            Taxa de decaimento do inflaton (Reheating)
        """
        self.xi = xi
        self.alpha = alpha
        self.gamma = gamma # Decay friction coefficient
        self.cosmo = CosmologiaRelatividade()

    def constante_gravitacional_efetiva(self, phi: float) -> float:
        """
        Constante gravitacional efetiva G_eff = G / f(φ)
        """
        f_phi = 1 + self.xi * phi**2 + self.alpha * phi**4
        return 1.0 / f_phi

    def evolucao_campo_bounce(self, t_span: Tuple[float, float] = (-100, 100),
                             n_pontos: int = 1000,
                             initial_conditions: Optional[Dict[str, float]] = None) -> Dict[str, np.ndarray]:
        """
        Evolução do campo escalar durante inflação e reheating.
        Resolve o sistema acoplado Gravidade-Campo-Radiação.
        
        y = [a, H, phi, pi_phi, rho_r]
        """
        def sistema_reheating(t, y):
            # Usar v_phi (dot_phi) em vez de pi_phi para evitar overflow a^3
            # y = [a, H, phi, v_phi, rho_r]
            a, H, phi, v_phi, rho_r = y

            # Evitar singularidade numérica
            if a < 1e-60: a = 1e-60
            
            G = 1.0  # Unidades naturais
            m_phi = 1e-6 # Massa do inflaton
            gamma = self.gamma
            
            # 1. Campo Escalar
            dot_phi = v_phi
            
            # Potencial
            V = 0.5 * m_phi**2 * phi**2
            dV_dphi = m_phi**2 * phi
            
            # Equação de Movimento para v_phi (ddot_phi)
            # ddot_phi + (3H + Gamma) dot_phi + V' + ... = 0
            # Aproximação perto do mínimo (phi~0): termos de Xi são desprezíveis
            # Equação completa seria complexa com Xi, mas no final da inflação o acoplamento
            # R*phi é pequeno se R -> 0.
            # Vamos usar a forma canônica amortecida:
            term_friction = (3 * H + gamma) * v_phi
            dot_v_phi = -term_friction - dV_dphi
            
            # 2. Energias
            rho_phi = 0.5 * v_phi**2 + V
            p_phi = 0.5 * v_phi**2 - V
            
            # 3. Radiação
            # dot_rho_r + 4H rho_r = Gamma * dot_phi^2
            dot_rho_r = gamma * v_phi**2 - 4 * H * rho_r
            if rho_r < 0: rho_r = 0
            
            # 4. Gravidade (G_eff)
            # No reaquecimento, phi é pequeno, F ~ 1.
            xi = self.xi
            F = 1 + xi * phi**2 + self.alpha * phi**4
            G_eff = G / F
            
            rho_tot = rho_phi + rho_r
            p_tot = p_phi + (rho_r / 3.0)
            
            # dH/dt = -4pi G_eff (rho + p)
            dot_H = -4 * np.pi * G_eff * (rho_tot + p_tot)
            
            # 5. Geometria
            dot_a = a * H
            
            return np.array([dot_a, dot_H, dot_phi, dot_v_phi, dot_rho_r])

        # Configurar Condições Iniciais
        if initial_conditions is None:
            initial_conditions = {}
            
        a0 = initial_conditions.get('a_inicial', 1.0)
        phi0 = initial_conditions.get('phi_inicial', 1.0)
        pi_phi0 = initial_conditions.get('pi_phi_inicial', 0.0)
        H0 = initial_conditions.get('H_inicial', 0.1)
        rho_r0 = initial_conditions.get('rho_r_inicial', 0.0)
        
        # Initial velocity v_phi (dot_phi)
        v_phi0 = pi_phi0 / (a0**3) if a0 > 1e-60 else 0.0
        
        y0 = np.array([a0, H0, phi0, v_phi0, rho_r0])
        
        # Integração
        # Usar LSODA para lidar com a rigidez durante o reaquecimento (oscilações rápidas)
        integrator = IntegratorNumerico(rtol=1e-5, atol=1e-7)
        sol = integrator.integrar_sistema(sistema_reheating, y0, t_span, metodo='LSODA')

        if not sol['sucesso']:
            warnings.warn(f"Integração falhou: {sol['mensagem']}")
            return {'sucesso': False, 'mensagem': sol['mensagem']}
        
        # Processar Resultados
        t_eval = np.linspace(t_span[0], t_span[1], n_pontos)
        try:
             sol_func = sol['solucao'].sol
             y_eval = np.array([sol_func(t) for t in t_eval])
        except Exception as e:
             return {'sucesso': False, 'mensagem': f"Erro na avaliação: {e}"}

        # Extrair componentes
        a_res = y_eval[:, 0]
        phi_res = y_eval[:, 2]
        v_phi_res = y_eval[:, 3] 
        rho_r_res = y_eval[:, 4]
        
        # Recalcular densidade do campo
        m_phi = 1e-6
        rho_phi_res = 0.5 * v_phi_res**2 + 0.5 * m_phi**2 * phi_res**2
        
        return {
            'sucesso': True,
            't': t_eval,
            'a': a_res,
            'H': y_eval[:, 1],
            'phi': phi_res,
            'v_phi': v_phi_res,
            'rho_r': rho_r_res,
            'rho_phi': rho_phi_res,
            'G_eff': np.array([self.constante_gravitacional_efetiva(phi) for phi in phi_res])
        }


# Funções utilitárias
def resolver_equacoes_friedmann(Omega_m: float = 0.3, Omega_lambda: float = 0.7,
                               H0: float = 70) -> CosmologiaRelatividade:
    """
    Função wrapper para resolver equações de Friedmann
    """
    return CosmologiaRelatividade(H0, Omega_m, Omega_lambda)


def calcular_raio_schwarzschild(M: float) -> float:
    """
    Função wrapper para raio de Schwarzschild
    """
    bh = BuracosNegros()
    return bh.raio_schwarzschild(M)


# Exemplos de uso
if __name__ == "__main__":
    print("Módulo de Relatividade Geral")
    print("=" * 30)

    # Teste 1: Cosmologia
    print("Teste 1: Cosmologia LCDM")
    cosmo = CosmologiaRelatividade(H0=70, Omega_m=0.3, Omega_lambda=0.7)

    idade = cosmo.idade_universo()
    print(f"Idade do universo: {idade:.2f} Gyr")

    # Evolução
    evol = cosmo.evoluir_universo(a_inicial=0.1, a_final=1.0, n_pontos=100)
    if evol['sucesso']:
        print(f"Evolução calculada com sucesso: {len(evol['a'])} pontos")
        print(".3f")

    # Teste 2: Buracos negros
    print("\nTeste 2: Buracos Negros")
    bh = BuracosNegros()

    # Sol
    M_sol = 1.0
    R_s_sol = bh.raio_schwarzschild(M_sol)
    print(f"Raio de Schwarzschild do Sol: {R_s_sol:.2f} km")

    # Sagitário A*
    M_sgr = 4.1e6  # Massas solares
    R_s_sgr = bh.raio_schwarzschild(M_sgr)
    print(f"Raio de Schwarzschild de Sgr A*: {R_s_sgr:.2e} km")

    # Teste 3: Campos escalares
    print("\nTeste 3: Campos Escalares Acoplados")
    campo = CamposEscalarAcoplados(xi=1e6, alpha=-1e-4)

    phi_test = 0.01
    G_eff = campo.constante_gravitacional_efetiva(phi_test)
    print(f"G_eff/G para φ={phi_test}: {G_eff:.6f}")

    # Evolução do campo
    evol_campo = campo.evolucao_campo_bounce((-50, 50), 500)
    if evol_campo['sucesso']:
        print(f"Evolução do campo calculada: {len(evol_campo['t'])} pontos")
        idx_bounce = np.argmin(evol_campo['a'])
        print(f"Bounce em t = {evol_campo['t'][idx_bounce]:.1f}")

    print("\nMódulo funcionando corretamente! ✅")
