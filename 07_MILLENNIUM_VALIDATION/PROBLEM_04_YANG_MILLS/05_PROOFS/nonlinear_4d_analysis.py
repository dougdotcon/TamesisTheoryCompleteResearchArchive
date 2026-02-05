"""
ANÁLISE NÃO-LINEAR EM d=4: PROBLEMA DE REGULARIDADE
====================================================
Estudo dos obstáculos para extensão do argumento Wilson-Itô
ao caso não-linear Yang-Mills em 4 dimensões.

O PROBLEMA CENTRAL:
- Em d=4, a teoria é crítica (dimensionalmente)
- Produtos de distribuições são mal definidos
- Necessita renormalização estocástica (Hairer)

Autor: Sistema Tamesis
Data: 4 de fevereiro de 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, dblquad
from scipy.special import gamma, kv  # Bessel K
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. ANÁLISE DIMENSIONAL
# =============================================================================

class DimensionalAnalysis:
    """
    Análise dimensional para Yang-Mills em d dimensões.
    
    [A_μ] = (d-2)/2 em unidades de massa
    [g] = (4-d)/2
    """
    
    def __init__(self, d=4, N=3):
        self.d = d
        self.N = N
        
    def field_dimension(self):
        """Dimensão canônica do campo A_μ."""
        return (self.d - 2) / 2
    
    def coupling_dimension(self):
        """Dimensão do coupling g."""
        return (4 - self.d) / 2
    
    def is_renormalizable(self):
        """Teoria é renormalizável se [g] ≥ 0."""
        return self.coupling_dimension() >= 0
    
    def is_critical(self):
        """Teoria é crítica (marginal) se [g] = 0."""
        return abs(self.coupling_dimension()) < 1e-10
    
    def superficial_divergence(self, n_ext_legs, n_loops):
        """
        Grau de divergência superficial.
        D = d*L - 2*I + sum([campos externos])
        Para YM puro com n pernas externas:
        D = 4 - n (em d=4)
        """
        if self.d == 4:
            return 4 - n_ext_legs
        else:
            # Fórmula geral
            return self.d - n_ext_legs * self.field_dimension()
    
    def print_analysis(self):
        """Imprime análise dimensional."""
        print(f"\n{'='*60}")
        print(f"ANÁLISE DIMENSIONAL: Yang-Mills em d={self.d}")
        print(f"{'='*60}")
        print(f"  [A_μ] = {self.field_dimension()}")
        print(f"  [g] = {self.coupling_dimension()}")
        print(f"  Renormalizável: {'Sim' if self.is_renormalizable() else 'Não'}")
        print(f"  Crítica: {'Sim' if self.is_critical() else 'Não'}")
        
        if self.d == 4:
            print(f"\n  Divergências superficiais:")
            for n in [2, 3, 4]:
                D = self.superficial_divergence(n, 1)
                status = "DIVERGE" if D >= 0 else "finito"
                print(f"    {n} pernas: D = {D} ({status})")

# =============================================================================
# 2. REGULARIDADE EM ESPAÇOS DE BESOV
# =============================================================================

class BesovRegularity:
    """
    Análise de regularidade em espaços de Besov B^s_{p,q}.
    
    Em d=4, o campo livre tem regularidade:
    A ∈ B^{-1-ε}_{∞,∞} para qualquer ε > 0
    
    Para produtos bem definidos, precisamos:
    s₁ + s₂ > 0 (regra de Bony)
    """
    
    def __init__(self, d=4):
        self.d = d
        
    def free_field_regularity(self):
        """
        Regularidade do campo livre gaussiano.
        Em d dimensões: s = 1 - d/2
        """
        return 1 - self.d / 2
    
    def product_regularity(self, s1, s2):
        """
        Regularidade do produto de duas distribuições.
        Bony: u·v bem definido se s1 + s2 > 0
        """
        return s1 + s2
    
    def is_product_defined(self, s1, s2):
        """Produto é bem definido?"""
        return self.product_regularity(s1, s2) > 0
    
    def cubic_term_analysis(self):
        """
        Análise do termo cúbico [A, [A, A]].
        Regularidade: 3s onde s é regularidade de A.
        """
        s = self.free_field_regularity()
        cubic_reg = 3 * s
        return cubic_reg
    
    def quadratic_term_analysis(self):
        """
        Análise do termo quadrático [A, ∂A].
        Regularidade: 2s - 1 (perda de 1 derivada).
        """
        s = self.free_field_regularity()
        quad_reg = 2 * s - 1
        return quad_reg
    
    def print_analysis(self):
        """Imprime análise de regularidade."""
        s = self.free_field_regularity()
        
        print(f"\n{'='*60}")
        print(f"ANÁLISE DE REGULARIDADE BESOV: d={self.d}")
        print(f"{'='*60}")
        print(f"  Campo livre A ∈ B^{s:.1f}")
        
        # Termos da ação YM
        print(f"\n  Termos não-lineares:")
        
        # ∂A · ∂A
        reg_kinetic = 2 * (s - 1)
        print(f"    (∂A)² : regularidade = {reg_kinetic:.1f}")
        
        # A · ∂A
        reg_quad = self.quadratic_term_analysis()
        print(f"    A·∂A  : regularidade = {reg_quad:.1f}")
        
        # A² · (∂A)
        reg_cubic = 2*s + (s-1)
        print(f"    A²·∂A : regularidade = {reg_cubic:.1f}")
        
        # A⁴
        reg_quartic = 4 * s
        print(f"    A⁴    : regularidade = {reg_quartic:.1f}")
        
        print(f"\n  Diagnóstico:")
        if self.d == 4:
            print(f"    ⚠️ Em d=4, s = {s:.1f}")
            print(f"    ⚠️ Produtos A·A têm regularidade 2s = {2*s:.1f} < 0")
            print(f"    ⚠️ PRODUTOS SÃO MAL DEFINIDOS!")
            print(f"    → Necessita RENORMALIZAÇÃO ESTOCÁSTICA")
        elif self.d == 3:
            print(f"    ✓ Em d=3, s = {s:.1f}")
            print(f"    ✓ Produtos A·A têm regularidade 2s = {2*s:.1f} < 0")
            print(f"    ✓ Mas subcrítico: renormalização tratável")
        elif self.d == 2:
            print(f"    ✓ Em d=2, s = {s:.1f}")
            print(f"    ✓ Teoria super-renormalizável")

# =============================================================================
# 3. CONTAGENS DE POTÊNCIA UV
# =============================================================================

class UVPowerCounting:
    """
    Contagem de potência UV para diagramas de Feynman.
    Em d=4, YM é marginalmente renormalizável.
    """
    
    def __init__(self, d=4, N=3):
        self.d = d
        self.N = N
        
    def propagator_uv(self, k):
        """
        Propagador no UV: G(k) ~ 1/k²
        """
        return 1 / (k**2 + 1e-10)
    
    def loop_integral_divergence(self, n_props, n_vertices):
        """
        Divergência de integral de loop.
        
        Para L loops com n propagadores:
        ∫ d^{dL}k / k^{2n}
        
        Diverge se dL - 2n ≥ 0
        """
        L = n_props - n_vertices + 1  # Relação topológica
        power = self.d * L - 2 * n_props
        return power
    
    def one_loop_self_energy(self):
        """
        Auto-energia de 1 loop (2 pernas externas).
        Π(p) ~ ∫ d^d k / k² (k-p)² ~ Λ^{d-4} (em d=4: log Λ)
        """
        return self.d - 4
    
    def one_loop_vertex(self):
        """
        Correção de vértice de 1 loop (3 pernas).
        Γ³ ~ ∫ d^d k / k⁶ ~ Λ^{d-6}
        """
        return self.d - 6
    
    def one_loop_4vertex(self):
        """
        Correção de 4-vértice de 1 loop.
        Γ⁴ ~ ∫ d^d k / k⁸ ~ Λ^{d-8}
        """
        return self.d - 8
    
    def print_analysis(self):
        """Imprime análise de contagem de potência."""
        print(f"\n{'='*60}")
        print(f"CONTAGEM DE POTÊNCIA UV: d={self.d}")
        print(f"{'='*60}")
        
        se = self.one_loop_self_energy()
        v3 = self.one_loop_vertex()
        v4 = self.one_loop_4vertex()
        
        print(f"\n  Divergências de 1-loop:")
        print(f"    Auto-energia Π(p): ~ Λ^{se} {'(log Λ em d=4)' if self.d==4 else ''}")
        print(f"    Vértice 3pt Γ³:    ~ Λ^{v3} {'(finito)' if v3 < 0 else ''}")
        print(f"    Vértice 4pt Γ⁴:    ~ Λ^{v4} {'(finito)' if v4 < 0 else ''}")
        
        if self.d == 4:
            print(f"\n  Em d=4:")
            print(f"    • Apenas auto-energia diverge (log)")
            print(f"    • Vértices convergem")
            print(f"    • TEORIA É RENORMALIZÁVEL")
            print(f"    • Mas liberdade assintótica complica IR!")

# =============================================================================
# 4. HAIRER'S REGULARITY STRUCTURES
# =============================================================================

class RegularityStructures:
    """
    Análise via estruturas de regularidade de Hairer.
    
    Para SPDEs com ruído branco espaço-temporal,
    a subcriticalidade requer:
    
    α_min + 2 > 0  (para equações parabólicas)
    
    onde α_min é a regularidade mínima necessária.
    """
    
    def __init__(self, d=4):
        self.d = d
        
    def noise_regularity(self):
        """
        Regularidade do ruído branco espaço-temporal.
        ξ ∈ C^{-(d+2)/2 - ε} em escala parabólica.
        """
        return -(self.d + 2) / 2
    
    def heat_kernel_regularity_gain(self):
        """
        Ganho de regularidade do kernel do calor.
        P_t: C^α → C^{α+2}
        """
        return 2
    
    def fixed_point_regularity(self):
        """
        Regularidade mínima para fixed point de
        u = P * ξ + P * F(u)
        
        Para Φ⁴ em d dimensões:
        α = 2 - d/2 - ε
        """
        return 2 - self.d / 2
    
    def subcriticality_index(self):
        """
        Índice de subcriticalidade.
        
        Teoria é subcrítica se α_min + 2 > 0.
        Em d=4: α_min = 0, logo marginal.
        """
        alpha = self.fixed_point_regularity()
        return alpha + 2
    
    def is_subcritical(self):
        """Teoria é subcrítica?"""
        return self.subcriticality_index() > 0
    
    def print_analysis(self):
        """Imprime análise via estruturas de regularidade."""
        print(f"\n{'='*60}")
        print(f"ESTRUTURAS DE REGULARIDADE (HAIRER): d={self.d}")
        print(f"{'='*60}")
        
        noise_reg = self.noise_regularity()
        kernel_gain = self.heat_kernel_regularity_gain()
        fp_reg = self.fixed_point_regularity()
        sc_idx = self.subcriticality_index()
        
        print(f"\n  Regularidades:")
        print(f"    Ruído ξ:        {noise_reg:.2f}")
        print(f"    Ganho de P_t:   +{kernel_gain}")
        print(f"    Fixed point:    {fp_reg:.2f}")
        
        print(f"\n  Subcriticalidade:")
        print(f"    Índice = α_min + 2 = {sc_idx:.2f}")
        
        if sc_idx > 0:
            print(f"    ✓ SUBCRÍTICO: teoria de regularidade aplicável")
        elif abs(sc_idx) < 0.1:
            print(f"    ⚠️ CRÍTICO: caso marginal, correções log")
        else:
            print(f"    ❌ SUPERCRÍTICO: teoria não se aplica diretamente")
        
        if self.d == 4:
            print(f"\n  DIAGNÓSTICO PARA d=4:")
            print(f"    • Caso crítico (marginal)")
            print(f"    • Estruturas de regularidade padrão FALHAM")
            print(f"    • Necessita: extensão para caso crítico")
            print(f"    • Ou: redução dimensional via simetrias")

# =============================================================================
# 5. ANÁLISE DO TERMO NÃO-LINEAR DE FORÇA
# =============================================================================

class NonlinearForceAnalysis:
    """
    Análise da força não-linear f(A) = -d*_A F(A).
    
    Em coordenadas:
    f^a_μ = ∂_ν F^a_{νμ} + g f^{abc} A^b_ν F^c_{νμ}
    
    onde F_{μν} = ∂_μ A_ν - ∂_ν A_μ + g [A_μ, A_ν]
    """
    
    def __init__(self, d=4, N=3, g=1.0):
        self.d = d
        self.N = N
        self.g = g
        self.b0 = 11 * N / 3
        
    def linear_force(self, k):
        """
        Parte linear da força: f_lin = -□A
        Transformada: f_lin(k) = k² A(k)
        """
        return k**2
    
    def quadratic_force_scaling(self, k1, k2):
        """
        Parte quadrática: f_quad ~ g [A, ∂A]
        Scaling: g * k * A²
        """
        return self.g * (k1 + k2)
    
    def cubic_force_scaling(self, k1, k2, k3):
        """
        Parte cúbica: f_cubic ~ g² [A, [A, A]]
        Scaling: g² * A³
        """
        return self.g**2
    
    def uv_behavior(self, Lambda):
        """
        Comportamento UV da força.
        
        Em d=4 com liberdade assintótica:
        g(Λ) → 0 quando Λ → ∞
        
        Mas: A(Λ) ~ flutuações aumentam
        """
        # Running coupling
        log_L = np.log(Lambda / 100)
        denom = 1 + self.b0 * self.g**2 * log_L / (8 * np.pi**2)
        if denom > 0:
            g_eff = np.sqrt(self.g**2 / denom)
        else:
            g_eff = np.inf
            
        # Flutuações do campo
        A_fluct = Lambda**(2 - self.d/2)  # Regularidade s = 1 - d/2
        
        return g_eff, A_fluct
    
    def ir_behavior(self, mu):
        """
        Comportamento IR da força.
        
        Coupling cresce no IR → não-linearidade domina
        """
        Lambda_QCD = 100 * np.exp(-8 * np.pi**2 / (self.b0 * self.g**2))
        
        if mu < Lambda_QCD:
            return np.inf, np.inf  # Não perturbativo
        
        log_ratio = np.log(mu / 100)
        denom = 1 + self.b0 * self.g**2 * log_ratio / (8 * np.pi**2)
        if denom > 0:
            g_eff = np.sqrt(self.g**2 / denom)
        else:
            g_eff = np.inf
            
        return g_eff, mu**(2 - self.d/2)
    
    def print_analysis(self):
        """Imprime análise da força não-linear."""
        print(f"\n{'='*60}")
        print(f"ANÁLISE DA FORÇA NÃO-LINEAR: d={self.d}")
        print(f"{'='*60}")
        
        print(f"\n  Estrutura da força:")
        print(f"    f(A) = -d*_A F(A)")
        print(f"         = ∂²A + g[A,∂A] + g²[A,[A,A]]")
        print(f"         = LINEAR + QUADRÁTICO + CÚBICO")
        
        print(f"\n  Comportamento por escala:")
        
        scales = [1000, 100, 10, 1, 0.1]
        print(f"    {'μ':<10} {'g(μ)':<12} {'|A|':<12} {'g|A|²':<12}")
        print(f"    {'-'*46}")
        
        for mu in scales:
            if mu < 0.08:  # Abaixo de Λ_QCD
                print(f"    {mu:<10.2f} {'∞':^12} {'∞':^12} {'NÃO-PERT':^12}")
            else:
                g_eff, A_fluct = self.ir_behavior(mu)
                nonlin = g_eff * A_fluct**2 if not np.isinf(g_eff) else np.inf
                if np.isinf(g_eff):
                    print(f"    {mu:<10.2f} {'∞':^12} {'∞':^12} {'NÃO-PERT':^12}")
                else:
                    print(f"    {mu:<10.2f} {g_eff:<12.4f} {A_fluct:<12.4f} {nonlin:<12.4f}")
        
        print(f"\n  Diagnóstico:")
        print(f"    • UV: g → 0, mas produtos de A são singulares")
        print(f"    • IR: g → ∞ (Landau pole), teoria não-perturbativa")
        print(f"    • Termo g[A,∂A] requer renormalização")
        print(f"    • Termo g²[A,[A,A]] ainda mais singular")

# =============================================================================
# 6. ESTRATÉGIAS DE RENORMALIZAÇÃO
# =============================================================================

class RenormalizationStrategies:
    """
    Estratégias para lidar com singularidades em d=4.
    """
    
    def __init__(self):
        pass
    
    def list_strategies(self):
        """Lista estratégias possíveis."""
        strategies = {
            "BPHZ": {
                "descrição": "Subtração de divergências ordem por ordem",
                "status": "Funciona para diagramas, não para SPDEs",
                "aplicável_d4": True
            },
            "Regularização_dimensional": {
                "descrição": "d = 4 - ε, tomar ε → 0",
                "status": "Padrão em QFT perturbativa",
                "aplicável_d4": True
            },
            "Hairer_parabólico": {
                "descrição": "Estruturas de regularidade para SPDEs",
                "status": "Funciona d < 4 (subcrítico)",
                "aplicável_d4": False
            },
            "CCHS": {
                "descrição": "Extensão de Hairer para sistemas gauge",
                "status": "d=2,3 completo; d=4 aberto",
                "aplicável_d4": False
            },
            "Lattice": {
                "descrição": "Discretização → limite contínuo",
                "status": "Rigoroso, mas limite é o problema",
                "aplicável_d4": True
            },
            "Redução_dimensional": {
                "descrição": "Usar simetrias para reduzir efetivamente d",
                "status": "Específico para cada teoria",
                "aplicável_d4": "Depende"
            }
        }
        return strategies
    
    def print_strategies(self):
        """Imprime estratégias."""
        print(f"\n{'='*60}")
        print(f"ESTRATÉGIAS DE RENORMALIZAÇÃO PARA d=4")
        print(f"{'='*60}")
        
        for name, info in self.list_strategies().items():
            print(f"\n  {name}:")
            print(f"    Descrição: {info['descrição']}")
            print(f"    Status: {info['status']}")
            app = info['aplicável_d4']
            if app == True:
                print(f"    Aplicável d=4: ✓")
            elif app == False:
                print(f"    Aplicável d=4: ❌")
            else:
                print(f"    Aplicável d=4: {app}")

# =============================================================================
# 7. PROPOSTA: WILSON-ITÔ RENORMALIZADO
# =============================================================================

class WilsonItoRenormalized:
    """
    Proposta de Wilson-Itô com renormalização.
    
    Ideia: usar a estrutura Wilson-Itô mas com
    contratermos que absorvem as divergências.
    """
    
    def __init__(self, d=4, N=3, g0=1.0, Lambda_UV=100):
        self.d = d
        self.N = N
        self.g0 = g0
        self.Lambda_UV = Lambda_UV
        self.b0 = 11 * N / 3
        
    def renormalized_force(self, phi, a, counterterms=True):
        """
        Força renormalizada:
        f_ren = f_bare - δf
        
        onde δf são os contratermos.
        """
        # Força bare (linear para simplificar)
        g = self.running_coupling(a)
        m2_eff = -self.b0 * g**2 / (16 * np.pi**2)
        
        f_bare = m2_eff * phi
        
        if counterterms:
            # Contratermo de massa
            delta_m2 = self.mass_counterterm(a)
            f_ren = (m2_eff - delta_m2) * phi
        else:
            f_ren = f_bare
            
        return f_ren
    
    def mass_counterterm(self, a):
        """
        Contratermo de massa (1-loop).
        
        δm² ~ g² Λ² (em d=4 com regularização por cutoff)
        ou
        δm² ~ g² μ² log(Λ/μ) (com reg. dimensional)
        """
        g = self.running_coupling(a)
        
        # Usando cutoff
        log_div = np.log(self.Lambda_UV / a) if a > 0 else 0
        
        # Coeficiente do contratermo (esquemático)
        delta_m2 = self.N * g**2 / (16 * np.pi**2) * a**2 * log_div
        
        return delta_m2
    
    def running_coupling(self, mu):
        """Coupling running g(μ)."""
        log_ratio = np.log(mu / self.Lambda_UV)
        denom = 1 + self.b0 * self.g0**2 * log_ratio / (8 * np.pi**2)
        if denom > 0:
            return np.sqrt(self.g0**2 / denom)
        return np.inf
    
    def check_finiteness(self, a_values):
        """
        Verifica se a força renormalizada é finita.
        """
        print(f"\n{'='*60}")
        print(f"VERIFICAÇÃO DE FINITUDE (Wilson-Itô Renormalizado)")
        print(f"{'='*60}")
        
        phi_test = 1.0
        
        print(f"\n  {'a':<10} {'f_bare':<15} {'δf':<15} {'f_ren':<15}")
        print(f"  {'-'*55}")
        
        all_finite = True
        for a in a_values:
            if a < 0.08:  # Landau pole
                print(f"  {a:<10.4f} {'LANDAU':^15} {'POLE':^15} {'-':^15}")
                continue
                
            g = self.running_coupling(a)
            m2_eff = -self.b0 * g**2 / (16 * np.pi**2)
            f_bare = m2_eff * phi_test
            delta_f = self.mass_counterterm(a) * phi_test
            f_ren = f_bare - delta_f
            
            status = "✓" if np.isfinite(f_ren) else "❌"
            if not np.isfinite(f_ren):
                all_finite = False
                
            print(f"  {a:<10.4f} {f_bare:<15.6f} {delta_f:<15.6f} {f_ren:<15.6f} {status}")
        
        return all_finite

# =============================================================================
# 8. MAIN
# =============================================================================

def main():
    print("="*70)
    print("ANÁLISE NÃO-LINEAR EM d=4: PROBLEMAS DE REGULARIDADE")
    print("="*70)
    
    # 1. Análise dimensional
    dim = DimensionalAnalysis(d=4)
    dim.print_analysis()
    
    # 2. Regularidade Besov
    besov = BesovRegularity(d=4)
    besov.print_analysis()
    
    # 3. Contagem UV
    uv = UVPowerCounting(d=4)
    uv.print_analysis()
    
    # 4. Estruturas de regularidade
    reg = RegularityStructures(d=4)
    reg.print_analysis()
    
    # 5. Força não-linear
    force = NonlinearForceAnalysis(d=4)
    force.print_analysis()
    
    # 6. Estratégias
    strat = RenormalizationStrategies()
    strat.print_strategies()
    
    # 7. Wilson-Itô renormalizado
    wir = WilsonItoRenormalized(d=4)
    a_values = [100, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1]
    wir.check_finiteness(a_values)
    
    # Conclusão
    print("\n" + "="*70)
    print("CONCLUSÃO: OBSTÁCULOS PARA d=4")
    print("="*70)
    print("""
    ┌────────────────────────────────────────────────────────────────┐
    │ PROBLEMAS IDENTIFICADOS EM d=4                                │
    ├────────────────────────────────────────────────────────────────┤
    │                                                                │
    │  1. CRITICALIDADE DIMENSIONAL                                 │
    │     • [g] = 0 → teoria é marginal                             │
    │     • Correções logarítmicas em todo lugar                    │
    │                                                                │
    │  2. REGULARIDADE BESOV                                        │
    │     • Campo livre A ∈ B^{-1-ε}                                │
    │     • Produtos A·A têm regularidade -2-2ε < 0                 │
    │     • PRODUTOS SÃO MAL DEFINIDOS                              │
    │                                                                │
    │  3. ESTRUTURAS DE REGULARIDADE                                │
    │     • Índice de subcriticalidade = 0 (marginal)               │
    │     • Teoria de Hairer NÃO se aplica diretamente             │
    │                                                                │
    │  4. FORÇA NÃO-LINEAR                                          │
    │     • Termos g[A,∂A] e g²[A,[A,A]] são singulares            │
    │     • Renormalização necessária                               │
    │                                                                │
    │  CAMINHOS POSSÍVEIS:                                          │
    │  (a) Regularização dimensional d = 4-ε                        │
    │  (b) Extensão crítica de estruturas de regularidade          │
    │  (c) Lattice + limite cuidadoso                               │
    │  (d) Redução via simetrias gauge                              │
    │                                                                │
    │  STATUS: ❌ EXTENSÃO NÃO-LINEAR PERMANECE ABERTA             │
    │                                                                │
    └────────────────────────────────────────────────────────────────┘
    """)

if __name__ == "__main__":
    main()
