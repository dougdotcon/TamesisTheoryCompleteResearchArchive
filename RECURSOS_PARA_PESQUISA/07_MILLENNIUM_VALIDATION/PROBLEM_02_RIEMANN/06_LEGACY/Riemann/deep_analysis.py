#!/usr/bin/env python3
"""
ANÁLISE PROFUNDA DOS RESULTADOS - PRIMZEIT-RIEMANN
===================================================

Este script analisa em detalhe o que os testes numéricos revelam
sobre as lacunas do framework Primzeit-Riemann.

Baseado nos resultados da verificação inicial.
"""

import numpy as np
from scipy import stats
from scipy.integrate import trapezoid
import matplotlib.pyplot as plt

try:
    import mpmath
    mpmath.mp.dps = 50
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def sieve_primes(n_max):
    is_prime = np.ones(n_max + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(np.sqrt(n_max)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return np.where(is_prime)[0]

def prime_time(primes):
    return np.cumsum(np.log(primes))

def riemann_zeros(n_zeros):
    if HAS_MPMATH:
        zeros = []
        for n in range(1, n_zeros + 1):
            try:
                gamma_n = float(mpmath.im(mpmath.zetazero(n)))
                zeros.append(gamma_n)
            except:
                break
        return np.array(zeros)
    else:
        known_zeros = [
            14.134725142, 21.022039639, 25.010857580, 30.424876126,
            32.935061588, 37.586178159, 40.918719012, 43.327073281,
            48.005150881, 49.773832478, 52.970321478, 56.446247697,
            59.347044003, 60.831778525, 65.112544048, 67.079810529,
            69.546401711, 72.067157674, 75.704690699, 77.144840069
        ]
        return np.array(known_zeros[:min(n_zeros, len(known_zeros))])

def counting_function_N(t):
    if t <= 0:
        return 0
    return (t / (2 * np.pi)) * np.log(t / (2 * np.pi * np.e)) + 7/8

# =============================================================================
# ANÁLISE 1: POR QUE A CORRESPONDÊNCIA FALHA
# =============================================================================

def analyze_correspondence_failure():
    """
    Análise detalhada de por que t_k ≠ γ_k e o que isso significa.
    """
    print("\n" + "=" * 70)
    print("ANÁLISE 1: INCOMPATIBILIDADE DE ESCALAS")
    print("=" * 70)
    
    primes = sieve_primes(10000)[:200]
    t = prime_time(primes)
    zeros = riemann_zeros(500)
    
    # Calcular razões t_k / γ_k
    n_compare = min(len(t), len(zeros))
    ratios = t[:n_compare] / zeros[:n_compare]
    
    print("\nTeorema: t_k ~ k log k, mas γ_k ~ 2πk / log k")
    print("Portanto: t_k / γ_k ~ (log k)² / (2π) → ∞")
    print()
    
    print("Verificação numérica:")
    print("-" * 50)
    print(f"{'k':>5} {'t_k':>12} {'γ_k':>12} {'t_k/γ_k':>12} {'(log k)²/2π':>14}")
    print("-" * 50)
    
    for k in [10, 20, 50, 100, 150, 200]:
        if k <= n_compare:
            theoretical_ratio = (np.log(k))**2 / (2 * np.pi)
            print(f"{k:5d} {t[k-1]:12.3f} {zeros[k-1]:12.3f} "
                  f"{ratios[k-1]:12.4f} {theoretical_ratio:14.4f}")
    
    print()
    print("CONCLUSÃO: A correspondência DIRETA t_k ↔ γ_k é IMPOSSÍVEL.")
    print("           As escalas divergem como (log k)².")
    
    # A correspondência correta
    print("\n" + "-" * 70)
    print("CORRESPONDÊNCIA CORRETA: t_k ↔ γ_{n(k)} onde n(k) = N(t_k)")
    print("-" * 70)
    
    correct_matches = []
    for k in range(len(t)):
        n_k = int(counting_function_N(t[k]))
        if 0 < n_k <= len(zeros):
            error = abs(t[k] - zeros[n_k - 1])
            correct_matches.append((k+1, primes[k], t[k], n_k, zeros[n_k-1], error))
    
    print(f"\n{'k':>5} {'p_k':>6} {'t_k':>10} {'n(k)':>6} {'γ_{n(k)}':>12} {'erro':>10}")
    print("-" * 55)
    for match in correct_matches[::20][:10]:  # Mostrar a cada 20
        k, p, tk, nk, gamma, err = match
        print(f"{k:5d} {p:6d} {tk:10.3f} {nk:6d} {gamma:12.3f} {err:10.4f}")
    
    errors = [m[5] for m in correct_matches]
    print(f"\nErro médio: {np.mean(errors):.4f}")
    print(f"Erro máximo: {np.max(errors):.4f}")
    
    return correct_matches

# =============================================================================
# ANÁLISE 2: POR QUE A FÓRMULA DE TRAÇO FALHA
# =============================================================================

def analyze_trace_formula_failure():
    """
    Análise de por que a fórmula de traço não fecha numericamente.
    """
    print("\n" + "=" * 70)
    print("ANÁLISE 2: FALHA NA FÓRMULA DE TRAÇO")
    print("=" * 70)
    
    zeros = riemann_zeros(200)
    primes = sieve_primes(50000)[:2000]
    
    # Fórmula explícita de Riemann-von Mangoldt:
    # Σ φ(γ) = φ̂(0) log(2π) - Σ_p Σ_m (log p / p^{m/2}) [φ̂(m log p) + φ̂(-m log p)]
    
    # Testar com diferentes funções φ
    sigmas = [5, 10, 20, 50]
    
    print("\nTestando fórmula de traço com Gaussiana φ(t) = exp(-t²/2σ²)")
    print("Fórmula esperada: Σφ(γ_n) = -Σ_p (Λ(p)/√p) φ̂(log p) + termos")
    print()
    print(f"{'σ':>6} {'Σφ(γ)':>15} {'-Σprimos':>15} {'Erro rel.':>12}")
    print("-" * 50)
    
    for sigma in sigmas:
        # Função teste
        phi = lambda t, s=sigma: np.exp(-t**2 / (2 * s**2))
        
        # Transformada de Fourier
        phi_hat = lambda w, s=sigma: s * np.sqrt(2*np.pi) * np.exp(-s**2 * w**2 / 2)
        
        # Lado espectral
        spectral = np.sum(phi(zeros))
        
        # Lado aritmético (contribuição dos primos)
        arithmetic = 0
        for p in primes:
            log_p = np.log(p)
            # Contribuição: -(log p / √p) * φ̂(log p)
            arithmetic -= (log_p / np.sqrt(p)) * phi_hat(log_p)
        
        error = abs(spectral - arithmetic) / abs(spectral) if spectral != 0 else float('inf')
        print(f"{sigma:6.0f} {spectral:15.6f} {arithmetic:15.6f} {error*100:11.2f}%")
    
    print()
    print("PROBLEMA: A fórmula de traço ASSUME que os γ_n são autovalores de H.")
    print("          Mas isso é exatamente o que queremos provar!")
    print()
    print("CIRCULARIDADE: Não podemos usar a fórmula explícita de ζ para provar")
    print("               que spec(H) = {γ_n}, porque a fórmula já assume isso.")

# =============================================================================
# ANÁLISE 3: O QUE O OPERADOR H REALMENTE FAZ
# =============================================================================

def analyze_operator_structure():
    """
    Análise da estrutura real do operador H discretizado.
    """
    print("\n" + "=" * 70)
    print("ANÁLISE 3: ESTRUTURA DO OPERADOR H")
    print("=" * 70)
    
    # Construir H com diferentes parâmetros
    N = 256
    primes = sieve_primes(10000)[:100]
    kappa = 0.01
    epsilon = 0.1
    
    # Coeficientes α_p
    alpha = kappa * np.log(primes) / (primes ** (0.5 + epsilon))
    
    print(f"\nParâmetros: N={N}, n_primes={len(primes)}, κ={kappa}, ε={epsilon}")
    print(f"Σ|α_p| = {np.sum(np.abs(alpha)):.6f}")
    print(f"Σα_p² = {np.sum(alpha**2):.8f}")
    
    # Grade de momento
    xi = np.linspace(0.1, 100, N)
    
    # Multiplicador de Fourier m(ξ) = Σ α_p p^{-iξ}
    m_values = []
    for xi_val in xi:
        m = np.sum(alpha * (primes ** (-1j * xi_val)))
        m_values.append(m)
    m_values = np.array(m_values)
    
    print(f"\nMultiplicador m(ξ) = Σ α_p p^{{-iξ}}:")
    print(f"  max|m(ξ)| = {np.max(np.abs(m_values)):.6f}")
    print(f"  média|m(ξ)| = {np.mean(np.abs(m_values)):.6f}")
    
    # O operador H no espaço de Fourier é H = ξ + m(ξ)
    # Os "autovalores" são simplesmente ξ + Re(m(ξ))
    pseudo_eigenvals = xi + np.real(m_values)
    
    print("\nAUTOVALORES DE H (aproximação diagonal):")
    print("  H é essencialmente diagonal: λ_j ≈ ξ_j + Re(m(ξ_j))")
    print("  Isso dá espectro CONTÍNUO, não discreto!")
    
    # Comparar com zeros
    zeros = riemann_zeros(50)
    
    print("\n" + "-" * 50)
    print("PROBLEMA FUNDAMENTAL:")
    print("-" * 50)
    print("O operador H, como construído, tem espectro CONTÍNUO ≈ ℝ")
    print("Os zeros de ζ formam um conjunto DISCRETO.")
    print("NÃO HÁ RAZÃO para que spec(H) = {γ_n}!")
    print()
    print("Para obter espectro discreto, precisaríamos de:")
    print("  1. Um espaço de Hilbert diferente (compacto)")
    print("  2. Uma perturbação que crie lacunas espectrais")
    print("  3. Condições de contorno que discretizem o espectro")

# =============================================================================
# ANÁLISE 4: O QUE SERIA NECESSÁRIO
# =============================================================================

def what_would_be_needed():
    """
    Síntese do que faltaria para uma prova real.
    """
    print("\n" + "=" * 70)
    print("ANÁLISE 4: O QUE FALTA PARA UMA PROVA")
    print("=" * 70)
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    LACUNAS FUNDAMENTAIS                              ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  1. DISCRETIZAÇÃO DO ESPECTRO                                        ║
║     • H tem espectro contínuo = ℝ                                    ║
║     • Zeros de ζ são discretos                                       ║
║     • Nenhum mecanismo conhecido para transformar um no outro        ║
║                                                                      ║
║  2. IDENTIFICAÇÃO ESPECTRAL                                          ║
║     • Provar spec(H) ⊇ {γ_n} requer nova matemática                  ║
║     • Quantização aritmética não existe                              ║
║     • Não há formalismo onde "log p = órbitas"                       ║
║                                                                      ║
║  3. IMPLICAÇÃO RH                                                    ║
║     • Mesmo SE spec(H) = {γ_n}, isso não força Re(ρ) = 1/2           ║
║     • O operador codifica γ_n, não σ + iγ_n                          ║
║     • A parte real está PERDIDA na construção                        ║
║                                                                      ║
║  4. CONEXÃO ADÉLICA                                                  ║
║     • Connes mostrou: operador HP deve viver em L²(𝔸_ℚ/ℚ*)          ║
║     • Nosso H vive em ℓ²(R_W) ⊗ H²_w (espaço clássico)              ║
║     • Não há functor conhecido conectando os dois                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    print("CONCLUSÃO NUMÉRICA:")
    print("-" * 70)
    print("Os testes confirmam que o framework Primzeit-Riemann é um")
    print("PROGRAMA DE PESQUISA interessante, não uma prova.")
    print()
    print("O que os números mostram:")
    print("  ✓ Correspondência t_k ↔ γ_{n(k)} funciona (erro < 10)")
    print("  ✗ Fórmula de traço não fecha (erro > 500%)")
    print("  ✗ Operador H não tem estrutura espectral correta")
    print("  ✗ Não há mecanismo para forçar Re(ρ) = 1/2")

# =============================================================================
# EXPERIMENTO: BUSCAR ESTRUTURA OCULTA
# =============================================================================

def search_hidden_structure():
    """
    Tenta encontrar alguma estrutura não-trivial nos dados.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTO: BUSCANDO ESTRUTURA OCULTA")
    print("=" * 70)
    
    zeros = riemann_zeros(500)
    primes = sieve_primes(10000)[:500]
    t = prime_time(primes)
    
    # 1. Correlação entre espaçamentos
    print("\n1. CORRELAÇÃO DE ESPAÇAMENTOS")
    zero_spacings = np.diff(zeros)
    prime_spacings = np.diff(t)
    
    # Normalizar
    zero_spacings_norm = zero_spacings / np.mean(zero_spacings)
    prime_spacings_norm = prime_spacings / np.mean(prime_spacings)
    
    n_corr = min(len(zero_spacings_norm), len(prime_spacings_norm))
    corr = np.corrcoef(zero_spacings_norm[:n_corr], prime_spacings_norm[:n_corr])[0,1]
    print(f"   Correlação espaçamentos normalizados: {corr:.4f}")
    
    # 2. Transformada de Fourier dos zeros
    print("\n2. FREQUÊNCIAS DOMINANTES NOS ZEROS")
    if len(zeros) > 100:
        from scipy.fft import fft, fftfreq
        
        # Zeros como sinal
        n = len(zeros)
        signal = zeros - np.mean(zeros)
        ft = np.abs(fft(signal))
        freqs = fftfreq(n, d=np.mean(np.diff(zeros)))
        
        # Top 5 frequências
        idx = np.argsort(ft[1:n//2])[-5:][::-1] + 1
        print("   Top 5 frequências:")
        for i in idx:
            print(f"     f = {freqs[i]:.4f}, amplitude = {ft[i]:.2f}")
        
        # Comparar com log p
        print("\n   Comparação com log(primos):")
        log_primes = np.log(primes[:10])
        for i, lp in enumerate(log_primes):
            print(f"     log(p_{i+1}) = log({primes[i]}) = {lp:.4f}")
    
    # 3. Pair correlation
    print("\n3. PAIR CORRELATION FUNCTION")
    # r(x) = densidade de pares com separação x
    spacings = []
    for i in range(min(100, len(zeros))):
        for j in range(i+1, min(100, len(zeros))):
            spacings.append(zeros[j] - zeros[i])
    
    spacings = np.array(spacings)
    
    # Normalizar pela densidade média
    mean_density = len(zeros[:100]) / (zeros[99] - zeros[0])
    normalized_spacings = spacings * mean_density
    
    # Histograma
    hist, bins = np.histogram(normalized_spacings, bins=50, range=(0, 10), density=True)
    
    # Montgomery's conjecture: 1 - (sin(πx)/(πx))²
    x = (bins[:-1] + bins[1:]) / 2
    montgomery = 1 - (np.sin(np.pi * x) / (np.pi * x + 1e-10))**2
    
    # Erro
    error = np.sqrt(np.mean((hist - montgomery)**2))
    print(f"   Erro L2 vs Montgomery: {error:.4f}")
    
    return {
        'spacing_correlation': corr,
        'montgomery_error': error
    }

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "█" * 70)
    print("   ANÁLISE PROFUNDA DO FRAMEWORK PRIMZEIT-RIEMANN")
    print("█" * 70)
    
    analyze_correspondence_failure()
    analyze_trace_formula_failure()
    analyze_operator_structure()
    search_hidden_structure()
    what_would_be_needed()
    
    print("\n" + "█" * 70)
    print("   FIM DA ANÁLISE")
    print("█" * 70)
    print()

if __name__ == "__main__":
    main()
