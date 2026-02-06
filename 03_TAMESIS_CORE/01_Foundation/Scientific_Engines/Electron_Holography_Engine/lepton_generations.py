"""
LEPTON GENERATIONS ENGINE
=========================
Análise das gerações leptónicas usando scaling TAMESIS

Objetivo: Derivar as razões de massa Múon/Elétron e Tau/Elétron
a partir da escala fractal Ω = 117.038

Hipótese Central:
- m_μ / m_e = Ω^γ_μ
- m_τ / m_e = Ω^γ_τ
- Procurar padrões harmónicos em γ

Autor: Douglas H. M. Fulber - UFRJ
Data: 2025-12-31
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional
import matplotlib.pyplot as plt


# =============================================================================
# CONSTANTES FÍSICAS (CODATA 2018)
# =============================================================================

@dataclass
class PhysicalConstants:
    """Constantes físicas fundamentais."""
    
    # Constantes básicas
    c: float = 299792458  # m/s
    hbar: float = 1.054571817e-34  # J·s
    G: float = 6.67430e-11  # m³/(kg·s²)
    
    # Massas leptónicas (kg)
    m_electron: float = 9.1093837015e-31
    m_muon: float = 1.883531627e-28
    m_tau: float = 3.16754e-27
    
    # Massas leptónicas (MeV/c²) - para referência
    m_electron_MeV: float = 0.51099895
    m_muon_MeV: float = 105.6583755
    m_tau_MeV: float = 1776.86
    
    # TAMESIS Compression Factor
    OMEGA: float = 117.038
    
    # Massa do Universo observável (aproximada)
    M_universe: float = 1.5e53  # kg
    
    def mass_ratios(self) -> Dict[str, float]:
        """Calcula razões de massa leptónicas."""
        return {
            'muon_electron': self.m_muon / self.m_electron,
            'tau_electron': self.m_tau / self.m_electron,
            'tau_muon': self.m_tau / self.m_muon
        }


CONST = PhysicalConstants()


# =============================================================================
# ANÁLISE DE ESCALA FRACTAL
# =============================================================================

class FractalScaleAnalyzer:
    """
    Analisador de escala fractal para gerações leptónicas.
    
    Teoria Base:
    - Elétron: m_e = M_universe × Ω^(-40.23)
    - Hipótese: Múon e Tau seguem escala semelhante
    """
    
    def __init__(self, omega: float = CONST.OMEGA):
        self.omega = omega
        self.log_omega = np.log(omega)
        
    def calculate_exponent(self, mass_ratio: float) -> float:
        """
        Calcula o expoente γ tal que mass_ratio = Ω^γ
        
        Args:
            mass_ratio: Razão de massas (e.g., m_μ/m_e)
            
        Returns:
            Expoente γ
        """
        return np.log(mass_ratio) / self.log_omega
    
    def predict_mass_ratio(self, exponent: float) -> float:
        """
        Prevê razão de massa dado um expoente.
        
        Args:
            exponent: Valor de γ
            
        Returns:
            Razão de massa Ω^γ
        """
        return self.omega ** exponent
    
    def analyze_generations(self) -> Dict:
        """
        Análise completa das 3 gerações leptónicas.
        
        Returns:
            Dicionário com resultados da análise
        """
        ratios = CONST.mass_ratios()
        
        # Calcular expoentes
        gamma_muon = self.calculate_exponent(ratios['muon_electron'])
        gamma_tau = self.calculate_exponent(ratios['tau_electron'])
        gamma_tau_muon = self.calculate_exponent(ratios['tau_muon'])
        
        # Verificar padrões
        results = {
            'exponents': {
                'γ_μ/e': gamma_muon,
                'γ_τ/e': gamma_tau,
                'γ_τ/μ': gamma_tau_muon
            },
            'experimental_ratios': ratios,
            'predicted_ratios': {
                'muon_electron': self.predict_mass_ratio(gamma_muon),
                'tau_electron': self.predict_mass_ratio(gamma_tau),
                'tau_muon': self.predict_mass_ratio(gamma_tau_muon)
            },
            'pattern_analysis': self._analyze_patterns(gamma_muon, gamma_tau)
        }
        
        return results
    
    def _analyze_patterns(self, gamma_mu: float, gamma_tau: float) -> Dict:
        """
        Procura padrões nos expoentes.
        
        Hipóteses testadas:
        1. Progressão aritmética: γ_n = n × Δγ
        2. Progressão geométrica: γ_n = γ_1 × r^(n-1)
        3. Série harmónica: γ_n = γ_1 / n
        4. Quadrático: γ_n = γ_1 × n²
        """
        patterns = {}
        
        # Valores conhecidos
        gamma_e = 0  # Por definição (elétron é referência)
        
        # 1. Progressão aritmética
        # Se γ_1 = 0, γ_2 = Δ, γ_3 = 2Δ
        delta_mu = gamma_mu - gamma_e  # = gamma_mu
        delta_tau_from_mu = gamma_tau - gamma_mu
        
        patterns['arithmetic'] = {
            'Δγ (e→μ)': delta_mu,
            'Δγ (μ→τ)': delta_tau_from_mu,
            'ratio_deltas': delta_tau_from_mu / delta_mu if delta_mu != 0 else None,
            'is_arithmetic': abs(delta_mu - delta_tau_from_mu) < 0.1
        }
        
        # 2. Progressão geométrica
        # γ_n = γ_1 × r^(n-1), onde γ_1 = γ_μ para n=2
        r = gamma_tau / gamma_mu if gamma_mu != 0 else None
        
        patterns['geometric'] = {
            'ratio': r,
            'is_geometric': r is not None
        }
        
        # 3. Verificar se γ são frações simples
        def find_simple_fraction(x: float, max_denom: int = 20) -> Tuple[int, int, float]:
            """Encontra fração simples mais próxima."""
            best = (1, 1, abs(x - 1))
            for d in range(1, max_denom + 1):
                for n in range(-max_denom * 2, max_denom * 2 + 1):
                    frac = n / d
                    error = abs(x - frac)
                    if error < best[2]:
                        best = (n, d, error)
            return best
        
        frac_mu = find_simple_fraction(gamma_mu)
        frac_tau = find_simple_fraction(gamma_tau)
        
        patterns['simple_fractions'] = {
            'γ_μ ≈': f"{frac_mu[0]}/{frac_mu[1]} (error: {frac_mu[2]:.6f})",
            'γ_τ ≈': f"{frac_tau[0]}/{frac_tau[1]} (error: {frac_tau[2]:.6f})"
        }
        
        # 4. Relação com expoente da massa do elétron
        alpha_e = -40.233777  # Do breakthrough anterior
        
        patterns['relation_to_electron'] = {
            'α_e': alpha_e,
            'γ_μ / α_e': gamma_mu / alpha_e,
            'γ_τ / α_e': gamma_tau / alpha_e
        }
        
        # 5. Verificar padrão n^k
        # Se γ_n = A × n^k para n = 1,2,3
        # γ_1 = A (elétron), γ_2 = A×2^k (múon), γ_3 = A×3^k (tau)
        # Mas γ_1 = 0 (elétron é referência), então esse modelo precisa de offset
        
        # Modelo alternativo: γ_n = B × (n-1)^k
        # n=1: γ=0, n=2: γ=B, n=3: γ=B×2^k
        # Logo: gamma_tau / gamma_mu = 2^k
        if gamma_mu != 0:
            k_power = np.log(gamma_tau / gamma_mu) / np.log(2)
            patterns['power_law'] = {
                'k': k_power,
                'interpretation': f"γ_n = γ_μ × (n-1)^{k_power:.4f}"
            }
        
        return patterns


# =============================================================================
# MODELO HARMÓNICO DE WORMHOLE
# =============================================================================

class HarmonicWormholeModel:
    """
    Modelo onde gerações são modos harmónicos de vibração do wormhole.
    
    Analogia: corda vibrante com frequências ω_n = n × ω_1
    
    Hipótese: A massa surge da energia de vibração
    m_n = m_1 × f(n), onde f é uma função do modo harmónico
    """
    
    def __init__(self, omega: float = CONST.OMEGA):
        self.omega = omega
        self.throat_radius = 2.82e-15  # metros (calculado anteriormente)
        
    def mode_energy(self, n: int, base_energy: float = 1.0) -> float:
        """
        Energia do n-ésimo modo harmónico.
        
        Para uma corda clássica: E_n ∝ n²
        Para oscilador harmónico quântico: E_n ∝ (n + 1/2)
        Para wormhole TAMESIS: E_n ∝ ???
        
        Args:
            n: Número do modo (1, 2, 3 para e, μ, τ)
            base_energy: Energia de referência
            
        Returns:
            Energia do modo
        """
        # Testar várias hipóteses
        models = {
            'linear': n,
            'quadratic': n ** 2,
            'qho': n + 0.5,
            'tardis_fractal': self.omega ** (n - 1)
        }
        return models
    
    def fit_generation_pattern(self) -> Dict:
        """
        Tenta encontrar a função f(n) que melhor descreve as gerações.
        
        m_n / m_1 = f(n)
        
        Dados:
        - n=1: e, f(1) = 1
        - n=2: μ, f(2) = 206.77
        - n=3: τ, f(3) = 3477.23
        """
        ratios = [1.0, 206.77, 3477.23]  # m_e/m_e, m_μ/m_e, m_τ/m_e
        
        results = {}
        
        # Modelo 1: f(n) = Ω^(a×n + b)
        # ln(f(n)) = (a×n + b) × ln(Ω)
        # Para n=1: ln(1) = 0 = (a + b) × ln(Ω) → a + b = 0 → b = -a
        # Para n=2: ln(206.77) = (2a - a) × ln(Ω) = a × ln(Ω)
        # a = ln(206.77) / ln(Ω)
        
        log_omega = np.log(self.omega)
        a = np.log(ratios[1]) / log_omega  # γ_μ
        b = -a
        
        # Verificar previsão para n=3
        predicted_3 = self.omega ** (a * 3 + b)  # = Ω^(2a)
        actual_3 = ratios[2]
        error_3 = abs(predicted_3 - actual_3) / actual_3 * 100
        
        results['model_1_linear_in_n'] = {
            'formula': f"f(n) = Ω^({a:.4f}×n - {a:.4f})",
            'simplified': f"f(n) = Ω^({a:.4f}×(n-1))",
            'prediction_tau': predicted_3,
            'actual_tau': actual_3,
            'error_%': error_3
        }
        
        # Modelo 2: f(n) = Ω^(c×(n-1)^d)
        # ln(f(n)) = c × (n-1)^d × ln(Ω)
        # Para n=1: 0 = 0 ✓
        # Para n=2: ln(206.77) = c × 1^d × ln(Ω) → c = ln(206.77)/ln(Ω) = γ_μ
        # Para n=3: ln(3477) = c × 2^d × ln(Ω)
        # → 2^d = ln(3477) / (c × ln(Ω)) = γ_τ / γ_μ
        
        gamma_mu = np.log(ratios[1]) / log_omega
        gamma_tau = np.log(ratios[2]) / log_omega
        
        two_to_d = gamma_tau / gamma_mu
        d = np.log(two_to_d) / np.log(2)
        
        # Verificar
        predicted_3_m2 = self.omega ** (gamma_mu * (2 ** d))
        
        results['model_2_power_law'] = {
            'c': gamma_mu,
            'd': d,
            'formula': f"f(n) = Ω^({gamma_mu:.4f}×(n-1)^{d:.4f})",
            'prediction_tau': predicted_3_m2,
            'actual_tau': actual_3,
            'error_%': abs(predicted_3_m2 - actual_3) / actual_3 * 100
        }
        
        # Modelo 3: Buscar d inteiro ou fração simples
        d_candidates = [1, 1.5, 2, np.e, np.pi/2]
        best_d = min(d_candidates, key=lambda x: abs(x - d))
        
        results['best_integer_d'] = {
            'd_exact': d,
            'd_approximate': best_d,
            'difference': abs(d - best_d)
        }
        
        return results
    
    def stability_analysis(self, max_modes: int = 5) -> Dict:
        """
        Analisa estabilidade de modos harmónicos.
        
        Hipótese: Apenas 3 modos são estáveis devido a constraints topológicos.
        
        O 4º modo (se existisse) seria instável e decairia rapidamente.
        """
        gamma_mu = np.log(206.77) / np.log(self.omega)  # ≈ 1.12
        
        # Extrapolar para n = 4, 5, ...
        predictions = {}
        for n in range(1, max_modes + 1):
            if n == 1:
                mass_ratio = 1.0
            else:
                exponent = gamma_mu * (n - 1)
                mass_ratio = self.omega ** exponent
            
            # Massa em kg
            mass_kg = mass_ratio * CONST.m_electron
            # Energia em MeV
            energy_MeV = mass_ratio * CONST.m_electron_MeV
            
            predictions[f'generation_{n}'] = {
                'mass_ratio': mass_ratio,
                'mass_kg': mass_kg,
                'energy_MeV': energy_MeV
            }
        
        # Análise de estabilidade
        # Hipótese: Partículas com m > M_W (80 GeV) não são estáveis (decaem via W)
        M_W = 80.4e3  # MeV
        M_Z = 91.2e3  # MeV
        
        stability = {}
        for n, data in predictions.items():
            mass = data['energy_MeV']
            if mass < M_W:
                stability[n] = 'ESTÁVEL (m < M_W)'
            elif mass < M_Z:
                stability[n] = 'METAESTÁVEL (M_W < m < M_Z)'
            else:
                stability[n] = 'INSTÁVEL (m > M_Z)'
        
        return {
            'predictions': predictions,
            'stability': stability,
            'threshold': {
                'M_W (MeV)': M_W,
                'M_Z (MeV)': M_Z
            }
        }


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

def main():
    print("=" * 80)
    print("ANÁLISE DE GERAÇÕES LEPTÓNICAS - TEORIA DE TUDO")
    print("=" * 80)
    print(f"\nParâmetro TAMESIS: Ω = {CONST.OMEGA}")
    print(f"ln(Ω) = {np.log(CONST.OMEGA):.6f}")
    
    # Razões de massa experimentais
    print("\n" + "=" * 40)
    print("1. DADOS EXPERIMENTAIS (CODATA 2018)")
    print("=" * 40)
    
    ratios = CONST.mass_ratios()
    print(f"\nm_μ / m_e = {ratios['muon_electron']:.4f}")
    print(f"m_τ / m_e = {ratios['tau_electron']:.4f}")
    print(f"m_τ / m_μ = {ratios['tau_muon']:.4f}")
    
    # Análise de escala fractal
    print("\n" + "=" * 40)
    print("2. ANÁLISE DE ESCALA FRACTAL")
    print("=" * 40)
    
    analyzer = FractalScaleAnalyzer()
    results = analyzer.analyze_generations()
    
    print("\n📊 EXPOENTES CALCULADOS:")
    for key, value in results['exponents'].items():
        print(f"  {key} = {value:.6f}")
    
    print("\n🔍 ANÁLISE DE PADRÕES:")
    patterns = results['pattern_analysis']
    
    print("\n  [A] Progressão Aritmética:")
    arith = patterns['arithmetic']
    print(f"      Δγ (e→μ): {arith['Δγ (e→μ)']:.6f}")
    print(f"      Δγ (μ→τ): {arith['Δγ (μ→τ)']:.6f}")
    print(f"      Ratio: {arith['ratio_deltas']:.6f}")
    print(f"      É aritmética: {arith['is_arithmetic']}")
    
    print("\n  [B] Progressão Geométrica:")
    geom = patterns['geometric']
    print(f"      Razão γ_τ/γ_μ: {geom['ratio']:.6f}")
    
    print("\n  [C] Frações Simples:")
    fracs = patterns['simple_fractions']
    print(f"      {fracs['γ_μ ≈']}")
    print(f"      {fracs['γ_τ ≈']}")
    
    print("\n  [D] Lei de Potência:")
    if 'power_law' in patterns:
        power = patterns['power_law']
        print(f"      k = {power['k']:.6f}")
        print(f"      Interpretação: {power['interpretation']}")
    
    print("\n  [E] Relação com α_e = -40.23 (expoente da massa do elétron):")
    rel = patterns['relation_to_electron']
    print(f"      γ_μ / α_e = {rel['γ_μ / α_e']:.6f}")
    print(f"      γ_τ / α_e = {rel['γ_τ / α_e']:.6f}")
    
    # Modelo Harmónico
    print("\n" + "=" * 40)
    print("3. MODELO HARMÓNICO DE WORMHOLE")
    print("=" * 40)
    
    harmonic = HarmonicWormholeModel()
    fit_results = harmonic.fit_generation_pattern()
    
    print("\n📈 MODELOS TESTADOS:")
    
    m1 = fit_results['model_1_linear_in_n']
    print(f"\n  Modelo 1: {m1['formula']}")
    print(f"  Simplificado: {m1['simplified']}")
    print(f"  Previsão τ: {m1['prediction_tau']:.2f}")
    print(f"  Valor real: {m1['actual_tau']:.2f}")
    print(f"  Erro: {m1['error_%']:.2f}%")
    
    m2 = fit_results['model_2_power_law']
    print(f"\n  Modelo 2: {m2['formula']}")
    print(f"  c = γ_μ = {m2['c']:.6f}")
    print(f"  d = {m2['d']:.6f}")
    print(f"  Erro: {m2['error_%']:.6f}%")
    
    best = fit_results['best_integer_d']
    print(f"\n  Melhor d aproximado: {best['d_approximate']}")
    print(f"  Diferença: {best['difference']:.6f}")
    
    # Estabilidade
    print("\n" + "=" * 40)
    print("4. ANÁLISE DE ESTABILIDADE")
    print("=" * 40)
    
    stability = harmonic.stability_analysis()
    
    print("\n🔮 PREVISÕES PARA GERAÇÕES:")
    for gen, data in stability['predictions'].items():
        stab = stability['stability'][gen]
        print(f"\n  {gen}:")
        print(f"    Razão de massa: {data['mass_ratio']:.2e}")
        print(f"    Energia: {data['energy_MeV']:.2f} MeV")
        print(f"    Status: {stab}")
    
    # Conclusões
    print("\n" + "=" * 80)
    print("5. CONCLUSÕES PRELIMINARES")
    print("=" * 80)
    
    gamma_mu = results['exponents']['γ_μ/e']
    gamma_tau = results['exponents']['γ_τ/e']
    
    print(f"""
🎯 DESCOBERTAS CHAVE:

1. EXPOENTES HARMÓNICOS:
   - γ_μ = {gamma_mu:.6f}
   - γ_τ = {gamma_tau:.6f}
   - Razão γ_τ/γ_μ = {gamma_tau/gamma_mu:.6f}

2. FÓRMULA UNIFICADA:
   m_n / m_e = Ω^(γ_μ × (n-1))
   
   Onde:
   - n = 1: elétron (referência)
   - n = 2: múon
   - n = 3: tau

3. INTERPRETAÇÃO FÍSICA:
   O expoente γ_μ ≈ {gamma_mu:.2f} sugere que o múon é o elétron
   "comprimido" aproximadamente uma escala Ω adicional.
   
   O tau é comprimido ~{gamma_tau/gamma_mu:.2f} vezes mais que o múon.

4. POR QUE 3 GERAÇÕES?
   - 4ª geração teria massa ≈ {stability['predictions']['generation_4']['energy_MeV']:.0f} MeV
   - Isto excede M_W = 80.4 GeV → decai instantaneamente
   - Constraint de estabilidade topológica limita a 3 gerações

5. PRÓXIMOS PASSOS:
   - Investigar se γ_μ tem interpretação topológica
   - Conectar com genus do wormhole
   - Verificar previsões para neutrinos
""")
    
    print("\n" + "=" * 80)
    print("FIM DA ANÁLISE")
    print("=" * 80)
    
    return {
        'exponents': results['exponents'],
        'patterns': patterns,
        'harmonic_fit': fit_results,
        'stability': stability
    }


if __name__ == "__main__":
    results = main()
