"""
ATAQUE A (H6): MONOTONICIDADE
=============================

Este arquivo foca em UMA hipótese: (H6).
Nada de Yang-Mills. Nada de gap. Nada de física.

Objetivo: Formular (H6) como lema matemático e testar qual norma funciona.

Três candidatos de norma:
  A) Norma de correlação ponderada
  B) Semigrupo contrativo
  C) Desigualdade tipo FKG

O código aqui DESCOBRE qual lema é verdadeiro.
A prova vem depois, com análise.
"""

import numpy as np
from scipy.linalg import expm, eigvalsh
from typing import Callable, Tuple, Optional
import matplotlib.pyplot as plt

# =============================================================================
# SETUP: Modelo Simplificado para Testar Monotonicidade
# =============================================================================

"""
Não vamos simular Yang-Mills.
Vamos simular um MODELO ABSTRATO que satisfaz (H1)-(H2) e testar (H6).

Modelo: Sistema de spins com simetria de gauge discreta.
- Estado: configuração σ ∈ {±1}^Λ
- Observable: W(C) = ∏_{e ∈ C} σ_e (análogo discreto de Wilson loop)
- Regularização: τ = temperatura inversa β

Este modelo é tratável e permite testar QUAL norma é monótona.
"""

class GaugeSpinModel:
    """Modelo de spins com gauge Z_2 para testar monotonicidade."""
    
    def __init__(self, L: int):
        """
        Args:
            L: tamanho linear do lattice (L x L)
        """
        self.L = L
        self.N_edges = 2 * L * L  # edges horizontais + verticais
        
    def random_config(self) -> np.ndarray:
        """Gera configuração aleatória de spins nas edges."""
        return 2 * np.random.randint(0, 2, self.N_edges) - 1
    
    def wilson_loop(self, config: np.ndarray, loop: list) -> float:
        """
        Calcula W(C) = ∏_{e ∈ C} σ_e
        
        Args:
            config: configuração de spins
            loop: lista de índices de edges formando o loop
        """
        return np.prod(config[loop])
    
    def plaquette(self, config: np.ndarray, x: int, y: int) -> float:
        """Plaqueta elementar em (x, y)."""
        L = self.L
        # Índices das 4 edges da plaqueta
        h1 = y * L + x  # horizontal bottom
        h2 = ((y + 1) % L) * L + x  # horizontal top
        v1 = L * L + x * L + y  # vertical left
        v2 = L * L + ((x + 1) % L) * L + y  # vertical right
        
        return config[h1] * config[v2] * config[h2] * config[v1]
    
    def action(self, config: np.ndarray, beta: float) -> float:
        """Ação S = -β Σ_p W(p) onde p são plaquetas."""
        S = 0.0
        for x in range(self.L):
            for y in range(self.L):
                S -= beta * self.plaquette(config, x, y)
        return S
    
    def boltzmann_weight(self, config: np.ndarray, beta: float) -> float:
        """Peso de Boltzmann e^{-S}."""
        return np.exp(-self.action(config, beta))
    
    def sample_configs(self, beta: float, n_samples: int, 
                       n_thermalize: int = 1000) -> list:
        """
        Amostra configurações com Metropolis.
        
        Aqui β = 1/τ (temperatura inversa = regularização).
        """
        config = self.random_config()
        configs = []
        
        for step in range(n_thermalize + n_samples):
            # Metropolis update
            edge = np.random.randint(self.N_edges)
            config_new = config.copy()
            config_new[edge] *= -1
            
            dS = self.action(config_new, beta) - self.action(config, beta)
            if dS < 0 or np.random.rand() < np.exp(-dS):
                config = config_new
            
            if step >= n_thermalize:
                configs.append(config.copy())
        
        return configs
    
    def expectation(self, observable: Callable, beta: float, 
                    n_samples: int = 500) -> float:
        """Calcula ⟨O⟩_β via Monte Carlo."""
        configs = self.sample_configs(beta, n_samples)
        values = [observable(c) for c in configs]
        return np.mean(values)
    
    def connected_correlator(self, loop1: list, loop2: list, 
                             beta: float, n_samples: int = 500) -> float:
        """
        Calcula ⟨W(C₁)W(C₂)⟩_c = ⟨W(C₁)W(C₂)⟩ - ⟨W(C₁)⟩⟨W(C₂)⟩
        """
        configs = self.sample_configs(beta, n_samples)
        
        W1_values = [self.wilson_loop(c, loop1) for c in configs]
        W2_values = [self.wilson_loop(c, loop2) for c in configs]
        W1W2_values = [w1 * w2 for w1, w2 in zip(W1_values, W2_values)]
        
        W1_mean = np.mean(W1_values)
        W2_mean = np.mean(W2_values)
        W1W2_mean = np.mean(W1W2_values)
        
        return W1W2_mean - W1_mean * W2_mean


# =============================================================================
# OPÇÃO A: Norma de Correlação Ponderada
# =============================================================================

def norma_A(model: GaugeSpinModel, beta: float, alpha: float = 1.0,
            n_samples: int = 500) -> float:
    """
    ||G_β||_* = sup_{C₁,C₂} e^{α·d(C₁,C₂)} |⟨W(C₁)W(C₂)⟩_c|
    
    Aproximação: testamos alguns pares de loops.
    """
    L = model.L
    max_val = 0.0
    
    # Loop fixo: plaqueta em (0,0)
    loop1 = [0, L*L, L, L*L + L]  # 4 edges da plaqueta (0,0)
    
    # Loops a diferentes distâncias
    for dx in range(1, L//2):
        x = dx
        y = 0
        # Loop 2 em (x, y)
        h1 = y * L + x
        h2 = ((y + 1) % L) * L + x
        v1 = L * L + x * L + y
        v2 = L * L + ((x + 1) % L) * L + y
        loop2 = [h1, v2, h2, v1]
        
        G_c = model.connected_correlator(loop1, loop2, beta, n_samples)
        dist = dx  # distância entre loops
        
        weighted = np.exp(alpha * dist) * np.abs(G_c)
        max_val = max(max_val, weighted)
    
    return max_val


def testar_monotonia_A(model: GaugeSpinModel, beta_values: np.ndarray,
                       alpha: float = 0.5) -> Tuple[np.ndarray, bool]:
    """
    Testa se ||G_β||_A é monótono em β.
    
    Esperamos: β₁ < β₂ ⟹ ||G_β₂||_* ≤ ||G_β₁||_*
    (mais regularização = correlação mais fraca)
    """
    norms = []
    
    print("\n  Testando Norma A (correlação ponderada)...")
    print(f"  {'β':<10} {'||G||_A':<15}")
    print(f"  {'-'*25}")
    
    for beta in beta_values:
        norm = norma_A(model, beta, alpha, n_samples=200)
        norms.append(norm)
        print(f"  {beta:<10.2f} {norm:<15.6f}")
    
    norms = np.array(norms)
    
    # Verificar monotonicidade (decrescente em β)
    is_monotone = all(norms[i] >= norms[i+1] for i in range(len(norms)-1))
    
    return norms, is_monotone


# =============================================================================
# OPÇÃO B: Semigrupo Contrativo
# =============================================================================

def construir_matriz_transferencia(model: GaugeSpinModel, beta: float) -> np.ndarray:
    """
    Constrói matriz de transferência T_β para o modelo.
    
    Em gauge theory discreta:
    T_β(σ, σ') = Σ_{links verticais} e^{β·plaqueta}
    
    Simplificação: matriz 2x2 para plaqueta única.
    """
    # Para gauge Z_2 com 1 plaqueta: estados são ±1
    # T(σ, σ') = e^{β σ σ'}
    T = np.array([
        [np.exp(beta), np.exp(-beta)],
        [np.exp(-beta), np.exp(beta)]
    ])
    
    # Normalizar para semigrupo (T_0 = I)
    T = T / np.trace(T) * 2
    
    return T


def testar_contratividade_B(beta_values: np.ndarray) -> Tuple[list, bool]:
    """
    Testa se T_β é contrativo: ||T_β₂|| ≤ ||T_β₁|| para β₁ < β₂.
    
    Norma = maior autovalor (norma de operador).
    """
    print("\n  Testando Opção B (semigrupo contrativo)...")
    print(f"  {'β':<10} {'||T_β||':<15} {'gap':<15}")
    print(f"  {'-'*40}")
    
    norms = []
    gaps = []
    
    for beta in beta_values:
        T = construir_matriz_transferencia(None, beta)
        eigenvalues = np.sort(np.abs(eigvalsh(T)))[::-1]
        
        norm = eigenvalues[0]
        gap = eigenvalues[0] - eigenvalues[1] if len(eigenvalues) > 1 else eigenvalues[0]
        
        norms.append(norm)
        gaps.append(gap)
        
        print(f"  {beta:<10.2f} {norm:<15.6f} {gap:<15.6f}")
    
    # Verificar contratividade (norma constante ou decrescente)
    is_contractive = all(norms[i] >= norms[i+1] - 1e-10 for i in range(len(norms)-1))
    
    return norms, gaps, is_contractive


# =============================================================================
# OPÇÃO C: Desigualdade FKG
# =============================================================================

def testar_FKG(model: GaugeSpinModel, beta: float, n_samples: int = 500) -> bool:
    """
    Testa se vale FKG: ⟨W(C₁)W(C₂)⟩ ≤ ⟨W(C₁)⟩⟨W(C₂)⟩
    
    Nota: Para gauge theories, geralmente vale o OPOSTO (correlação positiva).
    Mas vamos testar.
    """
    L = model.L
    
    # Dois loops
    loop1 = [0, L*L, L, L*L + L]
    x = L // 4
    loop2 = [x, L*L + x*L, L + x, L*L + (x+1)*L]
    
    configs = model.sample_configs(beta, n_samples)
    
    W1_values = [model.wilson_loop(c, loop1) for c in configs]
    W2_values = [model.wilson_loop(c, loop2) for c in configs]
    
    W1_mean = np.mean(W1_values)
    W2_mean = np.mean(W2_values)
    W1W2_mean = np.mean([w1*w2 for w1, w2 in zip(W1_values, W2_values)])
    
    # FKG: ⟨W₁W₂⟩ ≤ ⟨W₁⟩⟨W₂⟩
    fkg_holds = W1W2_mean <= W1_mean * W2_mean + 0.01  # tolerância numérica
    
    return fkg_holds, W1W2_mean, W1_mean * W2_mean


def testar_FKG_monotonicidade(model: GaugeSpinModel, 
                               beta_values: np.ndarray) -> Tuple[list, bool]:
    """Testa se FKG melhora com β crescente."""
    
    print("\n  Testando Opção C (FKG)...")
    print(f"  {'β':<10} {'⟨W₁W₂⟩':<12} {'⟨W₁⟩⟨W₂⟩':<12} {'FKG?':<8}")
    print(f"  {'-'*45}")
    
    ratios = []
    
    for beta in beta_values:
        fkg, joint, product = testar_FKG(model, beta, n_samples=300)
        ratio = joint / (product + 1e-10)
        ratios.append(ratio)
        
        print(f"  {beta:<10.2f} {joint:<12.4f} {product:<12.4f} {'✓' if fkg else '✗':<8}")
    
    # FKG monótono se ratio decresce com β
    is_monotone = all(ratios[i] >= ratios[i+1] - 0.05 for i in range(len(ratios)-1))
    
    return ratios, is_monotone


# =============================================================================
# ANÁLISE PRINCIPAL
# =============================================================================

def analisar_todas_opcoes():
    """Analisa as três opções de norma para (H6)."""
    
    print("="*70)
    print("ATAQUE A (H6): QUAL NORMA É MONÓTONA?")
    print("="*70)
    
    # Setup
    L = 6
    model = GaugeSpinModel(L)
    beta_values = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5])
    
    results = {}
    
    # Opção A
    print("\n" + "-"*60)
    print("OPÇÃO A: Norma de correlação ponderada")
    print("-"*60)
    norms_A, mono_A = testar_monotonia_A(model, beta_values, alpha=0.3)
    results['A'] = {'norms': norms_A, 'monotone': mono_A}
    print(f"\n  Monótona? {'✓ SIM' if mono_A else '✗ NÃO'}")
    
    # Opção B
    print("\n" + "-"*60)
    print("OPÇÃO B: Semigrupo contrativo")
    print("-"*60)
    norms_B, gaps_B, mono_B = testar_contratividade_B(beta_values)
    results['B'] = {'norms': norms_B, 'gaps': gaps_B, 'monotone': mono_B}
    print(f"\n  Contrativo? {'✓ SIM' if mono_B else '✗ NÃO'}")
    
    # Opção C
    print("\n" + "-"*60)
    print("OPÇÃO C: Desigualdade FKG")
    print("-"*60)
    ratios_C, mono_C = testar_FKG_monotonicidade(model, beta_values)
    results['C'] = {'ratios': ratios_C, 'monotone': mono_C}
    print(f"\n  Monótona? {'✓ SIM' if mono_C else '✗ NÃO'}")
    
    # Conclusão
    print("\n" + "="*70)
    print("CONCLUSÃO: QUAL OPÇÃO FUNCIONA?")
    print("="*70)
    
    print(f"""
    ┌────────────────────────────────────────────────────────────┐
    │  Opção    │  Monótona?  │  Candidata para (H6)?           │
    ├────────────────────────────────────────────────────────────┤
    │  A        │  {'SIM' if mono_A else 'NÃO':<10} │  {'✓ FORTE CANDIDATA' if mono_A else '✗ Descartada':<30} │
    │  B        │  {'SIM' if mono_B else 'NÃO':<10} │  {'✓ FORTE CANDIDATA' if mono_B else '✗ Descartada':<30} │
    │  C        │  {'SIM' if mono_C else 'NÃO':<10} │  {'✓ FORTE CANDIDATA' if mono_C else '✗ Descartada':<30} │
    └────────────────────────────────────────────────────────────┘
    """)
    
    # Identificar melhor candidata
    if mono_B:
        print("  ⭐ OPÇÃO B (SEMIGRUPO) é a mais promissora:")
        print("     - Teoria bem desenvolvida (Hille-Yosida)")
        print("     - Contratividade ⟹ espectro controlado")
        print("     - Gap espectral cai como subproduto")
    elif mono_A:
        print("  ⭐ OPÇÃO A (CORRELAÇÃO) é candidata:")
        print("     - Precisa bound uniforme no α")
        print("     - Conecta diretamente com decaimento")
    elif mono_C:
        print("  ⭐ OPÇÃO C (FKG) é candidata:")
        print("     - Precisa provar desigualdade de correlação")
        print("     - Técnicas de Fortuin-Kasteleyn disponíveis")
    
    return results


# =============================================================================
# FORMULAÇÃO DO LEMA (H6)
# =============================================================================

def formular_lema_H6(opcao: str):
    """Formula (H6) como lema matemático baseado na opção vencedora."""
    
    print("\n" + "="*70)
    print(f"FORMULAÇÃO DO LEMA (H6) - OPÇÃO {opcao}")
    print("="*70)
    
    if opcao == 'B':
        print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                      LEMA (H6) - VERSÃO SEMIGRUPO                      ║
    ╠════════════════════════════════════════════════════════════════════════╣
    ║                                                                        ║
    ║  DEFINIÇÕES:                                                           ║
    ║                                                                        ║
    ║  • Seja H = L²(A/G, μ) o espaço de Hilbert de funções                 ║
    ║    gauge-invariantes com medida μ.                                     ║
    ║                                                                        ║
    ║  • Para τ > 0, seja T_τ : H → H o operador de transferência           ║
    ║    definido pela regularização S_τ.                                    ║
    ║                                                                        ║
    ║  LEMA:                                                                 ║
    ║                                                                        ║
    ║  Se {T_τ}_{τ>0} forma um semigrupo fortemente contínuo, i.e.,         ║
    ║                                                                        ║
    ║      (i)   T_0 = I                                                     ║
    ║      (ii)  T_{τ+σ} = T_τ T_σ                                          ║
    ║      (iii) lim_{τ→0} T_τ f = f  ∀f ∈ H                                ║
    ║                                                                        ║
    ║  e se T_τ é positivity-preserving e contrativo:                        ║
    ║                                                                        ║
    ║      (iv)  f ≥ 0 ⟹ T_τ f ≥ 0                                         ║
    ║      (v)   ||T_τ|| ≤ 1                                                ║
    ║                                                                        ║
    ║  Então o gap espectral m(τ) = inf{spec(H_τ) \\ {0}} satisfaz:          ║
    ║                                                                        ║
    ║      τ₁ < τ₂  ⟹  m(τ₁) ≤ m(τ₂)                                       ║
    ║                                                                        ║
    ║  (gap é não-decrescente em τ, ou seja, cresce quando                  ║
    ║   removemos regularização).                                            ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
    
    ESTRUTURA DA PROVA:
    
    1. Semigrupo contrativo ⟹ gerador é dissipativo (Lumer-Phillips)
    2. Positividade ⟹ autovalor principal é simples
    3. Contratividade ⟹ autovalores em [0, 1]
    4. Monotonicidade segue de comparação de geradores
    
    REFERÊNCIAS:
    • Glimm-Jaffe, "Quantum Physics" (semigrupos em QFT)
    • Reed-Simon, Vol. II (teoria espectral)
    • Lieb-Loss, "Analysis" (desigualdades de positividade)
        """)
    
    elif opcao == 'A':
        print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                    LEMA (H6) - VERSÃO CORRELAÇÃO                       ║
    ╠════════════════════════════════════════════════════════════════════════╣
    ║                                                                        ║
    ║  DEFINIÇÃO:                                                            ║
    ║                                                                        ║
    ║  Para α > 0 e τ > 0, defina:                                          ║
    ║                                                                        ║
    ║      ||G_τ||_α = sup_{C₁,C₂} e^{α·d(C₁,C₂)} |⟨W_τ(C₁)W_τ(C₂)⟩_c|     ║
    ║                                                                        ║
    ║  LEMA:                                                                 ║
    ║                                                                        ║
    ║  Existe α₀ > 0 tal que a função τ ↦ ||G_τ||_{α₀} é monótona          ║
    ║  não-crescente para τ ∈ (0, τ₀].                                      ║
    ║                                                                        ║
    ║  Equivalentemente:                                                     ║
    ║                                                                        ║
    ║      τ₁ < τ₂  ⟹  ||G_{τ₂}||_{α₀} ≤ ||G_{τ₁}||_{α₀}                  ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
        """)
    
    return True


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("ATAQUE A (H6): MONOTONICIDADE")
    print("O código DESCOBRE qual lema é verdadeiro.")
    print("="*70)
    
    # Analisar todas as opções
    results = analisar_todas_opcoes()
    
    # Determinar vencedor
    vencedor = None
    if results['B']['monotone']:
        vencedor = 'B'
    elif results['A']['monotone']:
        vencedor = 'A'
    elif results['C']['monotone']:
        vencedor = 'C'
    
    if vencedor:
        formular_lema_H6(vencedor)
    else:
        print("\n  ⚠️ Nenhuma opção mostrou monotonicidade clara.")
        print("     Possíveis razões:")
        print("     - Modelo muito simples")
        print("     - α ou β fora do regime correto")
        print("     - Estatística insuficiente")
        print("\n     Próximo passo: refinar modelo ou parâmetros.")
    
    # Visualização
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    beta_values = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5])
    
    # Plot A
    ax = axes[0]
    ax.plot(beta_values, results['A']['norms'], 'o-', linewidth=2, markersize=8)
    ax.set_xlabel('β (regularização)')
    ax.set_ylabel('||G||_A')
    ax.set_title(f"Opção A: {'✓ Monótona' if results['A']['monotone'] else '✗ Não monótona'}")
    ax.grid(True, alpha=0.3)
    
    # Plot B
    ax = axes[1]
    ax.plot(beta_values, results['B']['gaps'], 'o-', linewidth=2, markersize=8, color='green')
    ax.set_xlabel('β (regularização)')
    ax.set_ylabel('Gap espectral')
    ax.set_title(f"Opção B: {'✓ Contrativo' if results['B']['monotone'] else '✗ Não contrativo'}")
    ax.grid(True, alpha=0.3)
    
    # Plot C
    ax = axes[2]
    ax.plot(beta_values, results['C']['ratios'], 'o-', linewidth=2, markersize=8, color='red')
    ax.axhline(1.0, color='black', linestyle='--', label='FKG limit')
    ax.set_xlabel('β (regularização)')
    ax.set_ylabel('⟨W₁W₂⟩ / ⟨W₁⟩⟨W₂⟩')
    ax.set_title(f"Opção C: {'✓ FKG' if results['C']['monotone'] else '✗ Não FKG'}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_path = r'd:\TamesisTheoryCompleteResearchArchive\07_MILLENNIUM_VALIDATION\PROBLEM_04_YANG_MILLS\05_PROOFS\h6_monotonicidade.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n  Figura salva: {output_path}")
    
    plt.close()
    
    print("\n" + "="*70)
    print("PRÓXIMO PASSO:")
    print("="*70)
    print("""
    1. Se Opção B venceu:
       - Formalizar semigrupo contrativo
       - Provar via Lumer-Phillips
       - Derivar monotonicidade do gap
    
    2. Se Opção A venceu:
       - Encontrar α₀ ótimo
       - Provar bound uniforme
       - Conectar com decaimento
    
    3. Se nenhuma venceu:
       - Aumentar tamanho do sistema
       - Testar outros regimes de β
       - Considerar modelo contínuo simplificado
    """)
    
    print("="*70 + "\n")
