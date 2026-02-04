#!/usr/bin/env python3
"""
PRIMZEIT-RIEMANN OSCILLATOR: NUMERICAL VERIFICATION SUITE
==========================================================

Este módulo implementa verificações numéricas para o framework
Primzeit-Riemann descrito em PROF_FORMAL.tex.

AVISO: Verificação numérica ≠ prova matemática.
       Serve para refutar rapidamente ideias erradas.

Autor: Framework de Verificação
Data: 2026
"""

import numpy as np
from scipy import linalg, special, stats
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from functools import lru_cache
import warnings

# Tentar importar mpmath para alta precisão
try:
    import mpmath
    mpmath.mp.dps = 50  # 50 dígitos de precisão
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    warnings.warn("mpmath não instalado. Usando precisão padrão.")

# =============================================================================
# PARTE 1: FUNÇÕES FUNDAMENTAIS
# =============================================================================

def sieve_primes(n_max):
    """Crivo de Eratóstenes para gerar primos até n_max."""
    is_prime = np.ones(n_max + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(np.sqrt(n_max)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return np.where(is_prime)[0]

def prime_time(primes):
    """
    Calcula o tempo primo: t_k = θ(p_k) = Σ log(p_j) para j=1..k
    
    Esta é a variável temporal fundamental do oscilador.
    """
    return np.cumsum(np.log(primes))

def riemann_zeros(n_zeros):
    """
    Retorna os primeiros n_zeros zeros não-triviais de ζ(s).
    
    Usa mpmath se disponível, senão usa tabela conhecida.
    """
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
        # Primeiros 30 zeros (valores conhecidos)
        known_zeros = [
            14.134725142, 21.022039639, 25.010857580, 30.424876126,
            32.935061588, 37.586178159, 40.918719012, 43.327073281,
            48.005150881, 49.773832478, 52.970321478, 56.446247697,
            59.347044003, 60.831778525, 65.112544048, 67.079810529,
            69.546401711, 72.067157674, 75.704690699, 77.144840069,
            79.337375020, 82.910380854, 84.735492981, 87.425274613,
            88.809111208, 92.491899271, 94.651344041, 95.870634228,
            98.831194218, 101.317851006
        ]
        return np.array(known_zeros[:min(n_zeros, len(known_zeros))])

def counting_function_N(t):
    """
    N(T) = número de zeros com 0 < γ < T
    
    Fórmula assintótica: N(T) ≈ (T/2π) log(T/2πe) + 7/8 + S(T)
    onde S(T) = O(log T)
    """
    if t <= 0:
        return 0
    return (t / (2 * np.pi)) * np.log(t / (2 * np.pi * np.e)) + 7/8

# =============================================================================
# PARTE 2: CONSTRUÇÃO DO OPERADOR H (VERSÃO MATRICIAL)
# =============================================================================

class PrimzeitOperator:
    """
    Operador H = H_0 + H_r discretizado.
    
    H_0 = K ⊗ I + I ⊗ P  (diagonal em representação de momento)
    H_r = Σ_p α_p T_{log p}  (translações)
    
    Parâmetros:
        N_grid: tamanho da grade de discretização
        kappa: constante de acoplamento (default 0.01)
        epsilon: expoente de decaimento (default 0.1)
        n_primes: número de primos a incluir
    """
    
    def __init__(self, N_grid=256, kappa=0.01, epsilon=0.1, n_primes=50):
        self.N = N_grid
        self.kappa = kappa
        self.epsilon = epsilon
        
        # Gerar primos
        self.primes = sieve_primes(10000)[:n_primes]
        
        # Coeficientes α_p = κ * log(p) / p^(1/2 + ε)
        self.alpha = kappa * np.log(self.primes) / (self.primes ** (0.5 + epsilon))
        
        # Grade no espaço de momento (ξ > 0 para Hardy space)
        self.xi = np.linspace(0.1, 100, N_grid)
        self.dxi = self.xi[1] - self.xi[0]
        
        # Peso do espaço de Hardy: w(ξ) = (1 + ξ)^(2s), s = 1
        self.s = 1.0
        self.weight = (1 + self.xi) ** (2 * self.s)
        
        # Construir matriz
        self._build_matrix()
    
    def _build_matrix(self):
        """Constrói a matriz H no espaço de Fourier."""
        N = self.N
        
        # H_0 = ξ (operador de momento, diagonal)
        self.H0 = np.diag(self.xi)
        
        # H_r no espaço de Fourier: multiplicação por m(ξ) = Σ α_p p^{-iξ}
        # Isso é um operador de multiplicação!
        self.m_xi = np.zeros(N, dtype=complex)
        for p, alpha in zip(self.primes, self.alpha):
            self.m_xi += alpha * (p ** (-1j * self.xi))
        
        # H_r como matriz diagonal (no espaço de Fourier)
        self.Hr = np.diag(self.m_xi.real)  # Parte real para auto-adjunticidade
        
        # H total
        self.H = self.H0 + self.Hr
    
    def eigenvalues(self):
        """Calcula os autovalores de H."""
        # Como H é diagonal no espaço de Fourier, os autovalores são triviais
        # Precisamos de uma construção mais sofisticada...
        
        # Para capturar estrutura não-trivial, vamos adicionar acoplamento
        # entre modos via convolução (aproximação)
        H_coupled = self._build_coupled_matrix()
        eigenvals = np.linalg.eigvalsh(H_coupled)
        return np.sort(eigenvals)
    
    def _build_coupled_matrix(self):
        """Constrói matriz com acoplamento entre modos."""
        N = self.N
        H = np.diag(self.xi).astype(complex)
        
        # Adicionar acoplamento via translações (convolução discreta)
        for p, alpha in zip(self.primes, self.alpha):
            log_p = np.log(p)
            # Operador de translação T_{log p} no espaço de posição
            # corresponde a multiplicação por e^{-iξ log p} no espaço de Fourier
            phase = np.exp(-1j * self.xi * log_p)
            
            # Matriz de rank-1 para acoplamento (aproximação)
            # (T_a f)(x) ≈ Σ_k e^{-iξ_k a} <f, φ_k> φ_k
            coupling = alpha * np.outer(phase, np.conj(phase)) / N
            H += coupling
        
        # Simetrizar para garantir Hermitianidade
        H = (H + H.conj().T) / 2
        return H.real  # Auto-adjunto real

    def trace_regularized(self, phi_func, Lambda=50):
        """
        Calcula Tr_reg(φ(H)) com cutoff espectral.
        
        phi_func: função teste φ: R → R
        Lambda: cutoff espectral
        """
        eigenvals = self.eigenvalues()
        # Aplicar cutoff
        mask = np.abs(eigenvals) <= Lambda
        return np.sum(phi_func(eigenvals[mask]))

# =============================================================================
# PARTE 3: TESTES DE CORRESPONDÊNCIA
# =============================================================================

def test_correspondence(n_test=100, verbose=True):
    """
    Testa a correspondência t_k ↔ γ_{n(k)} onde n(k) = N(t_k).
    
    Verifica: |t_k - γ_{n(k)}| < C para alguma constante C
    """
    # Gerar primos e tempos
    primes = sieve_primes(10000)[:n_test]
    t = prime_time(primes)
    
    # Obter zeros de Riemann
    max_n_needed = int(counting_function_N(t[-1]) * 1.5) + 10
    zeros = riemann_zeros(min(max_n_needed, 500))
    
    results = []
    for k in range(len(t)):
        t_k = t[k]
        n_k = int(counting_function_N(t_k))
        
        if n_k > 0 and n_k <= len(zeros):
            gamma_nk = zeros[n_k - 1]  # índice 0-based
            error = abs(t_k - gamma_nk)
            results.append({
                'k': k + 1,
                'p_k': primes[k],
                't_k': t_k,
                'n(k)': n_k,
                'gamma_n(k)': gamma_nk,
                'error': error
            })
    
    errors = [r['error'] for r in results]
    
    if verbose:
        print("=" * 60)
        print("TESTE DE CORRESPONDÊNCIA: t_k ↔ γ_{n(k)}")
        print("=" * 60)
        print(f"Primos testados: {len(results)}")
        print(f"Erro médio: {np.mean(errors):.4f}")
        print(f"Erro máximo: {np.max(errors):.4f}")
        print(f"Erro mínimo: {np.min(errors):.4f}")
        print(f"Desvio padrão: {np.std(errors):.4f}")
        print()
        print("Primeiros 10 resultados:")
        print("-" * 60)
        for r in results[:10]:
            print(f"k={r['k']:3d}, p={r['p_k']:5d}, t={r['t_k']:8.3f}, "
                  f"n(k)={r['n(k)']:3d}, γ={r['gamma_n(k)']:8.3f}, "
                  f"erro={r['error']:.4f}")
    
    return results, errors

# =============================================================================
# PARTE 4: ESTATÍSTICAS GUE
# =============================================================================

def test_gue_statistics(n_zeros=200, verbose=True):
    """
    Testa se os espaçamentos dos zeros seguem estatística GUE.
    
    Distribuição de Wigner surmise: P(s) = (π/2) s exp(-πs²/4)
    """
    zeros = riemann_zeros(n_zeros)
    
    if len(zeros) < 10:
        print("Poucos zeros disponíveis para análise GUE.")
        return None
    
    # Calcular espaçamentos
    spacings = np.diff(zeros)
    
    # Densidade local: d(γ) ≈ log(γ)/(2π)
    densities = np.log(zeros[:-1]) / (2 * np.pi)
    
    # Espaçamentos normalizados
    normalized_spacings = spacings * densities
    
    # Média deve ser ~1 após normalização
    mean_spacing = np.mean(normalized_spacings)
    normalized_spacings = normalized_spacings / mean_spacing
    
    # Distribuição de Wigner
    def wigner_surmise(s):
        return (np.pi / 2) * s * np.exp(-np.pi * s**2 / 4)
    
    # Criar histograma
    bins = np.linspace(0, 4, 50)
    hist, bin_edges = np.histogram(normalized_spacings, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Valores teóricos GUE
    wigner_values = wigner_surmise(bin_centers)
    
    # Calcular erro L2
    l2_error = np.sqrt(np.mean((hist - wigner_values)**2))
    
    # Teste de Kolmogorov-Smirnov
    # CDF de Wigner
    def wigner_cdf(s):
        return 1 - np.exp(-np.pi * s**2 / 4)
    
    ks_stat, ks_pvalue = stats.kstest(normalized_spacings, wigner_cdf)
    
    if verbose:
        print("=" * 60)
        print("TESTE DE ESTATÍSTICA GUE")
        print("=" * 60)
        print(f"Zeros analisados: {len(zeros)}")
        print(f"Espaçamento médio normalizado: {mean_spacing:.4f}")
        print(f"Erro L2 vs Wigner: {l2_error:.4f}")
        print(f"Teste KS: estatística = {ks_stat:.4f}, p-valor = {ks_pvalue:.4f}")
        if ks_pvalue > 0.05:
            print("✓ Não rejeitamos hipótese GUE (p > 0.05)")
        else:
            print("✗ Rejeitamos hipótese GUE (p < 0.05)")
    
    return {
        'normalized_spacings': normalized_spacings,
        'histogram': (hist, bin_centers),
        'wigner': wigner_values,
        'l2_error': l2_error,
        'ks_stat': ks_stat,
        'ks_pvalue': ks_pvalue
    }

# =============================================================================
# PARTE 5: TESTE DA FÓRMULA DE TRAÇO
# =============================================================================

def test_trace_formula(n_zeros=100, n_primes=500, verbose=True):
    """
    Testa a fórmula de traço explícita:
    
    Σ_n φ(γ_n) ≈ -Σ_p (log p / p^{1/2}) φ̂(log p) + termos suaves
    
    Usa função teste φ(t) = exp(-t²/2σ²) (Gaussiana)
    """
    zeros = riemann_zeros(n_zeros)
    primes = sieve_primes(10000)[:n_primes]
    
    if len(zeros) < 10:
        print("Poucos zeros para teste de fórmula de traço.")
        return None
    
    # Função teste: Gaussiana
    sigma = 10.0
    def phi(t):
        return np.exp(-t**2 / (2 * sigma**2))
    
    # Transformada de Fourier de Gaussiana: φ̂(ω) = σ√(2π) exp(-σ²ω²/2)
    def phi_hat(omega):
        return sigma * np.sqrt(2 * np.pi) * np.exp(-sigma**2 * omega**2 / 2)
    
    # LADO ESPECTRAL: Σ φ(γ_n)
    spectral_side = np.sum(phi(zeros))
    
    # LADO ARITMÉTICO: Σ_p contribuições
    log_primes = np.log(primes)
    arithmetic_side = 0
    for p in primes:
        log_p = np.log(p)
        # Contribuição de von Mangoldt: Λ(n)/n^{1/2}
        arithmetic_side -= (log_p / np.sqrt(p)) * phi_hat(log_p)
    
    # Termos suaves (aproximação do termo principal)
    # Integral principal ~ ∫ φ(t) (log t / 2π) dt
    t_grid = np.linspace(1, zeros[-1], 1000)
    # Usar scipy.integrate para compatibilidade com numpy 2.0
    from scipy.integrate import trapezoid
    smooth_term = trapezoid(phi(t_grid) * np.log(t_grid) / (2 * np.pi), t_grid)
    
    total_arithmetic = arithmetic_side + smooth_term
    
    # Erro relativo
    relative_error = abs(spectral_side - total_arithmetic) / abs(spectral_side)
    
    if verbose:
        print("=" * 60)
        print("TESTE DA FÓRMULA DE TRAÇO EXPLÍCITA")
        print("=" * 60)
        print(f"Zeros usados: {len(zeros)}, Primos usados: {len(primes)}")
        print(f"Parâmetro σ: {sigma}")
        print()
        print(f"Lado espectral Σφ(γ_n):     {spectral_side:.6f}")
        print(f"Lado aritmético (primos):   {arithmetic_side:.6f}")
        print(f"Termo suave:                {smooth_term:.6f}")
        print(f"Total aritmético:           {total_arithmetic:.6f}")
        print()
        print(f"Erro relativo: {relative_error * 100:.2f}%")
        if relative_error < 0.1:
            print("✓ Boa concordância (erro < 10%)")
        elif relative_error < 0.3:
            print("~ Concordância moderada (10% < erro < 30%)")
        else:
            print("✗ Concordância fraca (erro > 30%)")
    
    return {
        'spectral_side': spectral_side,
        'arithmetic_side': arithmetic_side,
        'smooth_term': smooth_term,
        'total_arithmetic': total_arithmetic,
        'relative_error': relative_error
    }

# =============================================================================
# PARTE 6: TESTE DO OPERADOR H
# =============================================================================

def test_operator_spectrum(N_grid=128, n_primes=30, verbose=True):
    """
    Constrói o operador H e analisa seu espectro.
    
    Compara com zeros de Riemann para verificar qualquer correspondência.
    """
    print("=" * 60)
    print("CONSTRUÇÃO E ANÁLISE DO OPERADOR H")
    print("=" * 60)
    
    # Construir operador
    H_op = PrimzeitOperator(N_grid=N_grid, n_primes=n_primes)
    
    print(f"Dimensão da matriz: {N_grid} x {N_grid}")
    print(f"Primos incluídos: {n_primes}")
    print(f"κ = {H_op.kappa}, ε = {H_op.epsilon}")
    print()
    
    # Calcular autovalores
    eigenvals = H_op.eigenvalues()
    
    # Filtrar autovalores positivos (análogos aos γ_n > 0)
    positive_eigenvals = eigenvals[eigenvals > 0]
    
    print(f"Autovalores calculados: {len(eigenvals)}")
    print(f"Autovalores positivos: {len(positive_eigenvals)}")
    print()
    
    # Comparar com zeros de Riemann
    zeros = riemann_zeros(50)
    
    if verbose:
        print("Comparação: primeiros autovalores vs zeros de Riemann")
        print("-" * 60)
        print(f"{'n':>3} {'Autovalor':>12} {'Zero ζ':>12} {'Razão':>10}")
        print("-" * 60)
        
        n_compare = min(10, len(positive_eigenvals), len(zeros))
        for i in range(n_compare):
            ev = positive_eigenvals[i]
            z = zeros[i]
            ratio = ev / z if z != 0 else float('inf')
            print(f"{i+1:3d} {ev:12.4f} {z:12.4f} {ratio:10.4f}")
    
    # Análise de correlação
    n_corr = min(len(positive_eigenvals), len(zeros))
    if n_corr > 5:
        correlation = np.corrcoef(positive_eigenvals[:n_corr], zeros[:n_corr])[0, 1]
        print()
        print(f"Correlação (primeiros {n_corr}): {correlation:.4f}")
    
    return {
        'eigenvalues': eigenvals,
        'positive_eigenvalues': positive_eigenvals,
        'zeros': zeros
    }

# =============================================================================
# PARTE 7: VISUALIZAÇÕES
# =============================================================================

def plot_all_results():
    """Gera visualizações de todos os testes."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Correspondência t_k vs γ_{n(k)}
    ax1 = axes[0, 0]
    results, errors = test_correspondence(n_test=50, verbose=False)
    if results:
        t_vals = [r['t_k'] for r in results]
        gamma_vals = [r['gamma_n(k)'] for r in results]
        ax1.scatter(t_vals, gamma_vals, alpha=0.6, s=20)
        max_val = max(max(t_vals), max(gamma_vals))
        ax1.plot([0, max_val], [0, max_val], 'r--', label='y = x')
        ax1.set_xlabel('t_k (tempo primo)')
        ax1.set_ylabel('γ_{n(k)} (zero de ζ)')
        ax1.set_title('Correspondência Primzeit-Zeros')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
    
    # 2. Estatística GUE
    ax2 = axes[0, 1]
    gue_results = test_gue_statistics(n_zeros=100, verbose=False)
    if gue_results:
        hist, bin_centers = gue_results['histogram']
        ax2.bar(bin_centers, hist, width=bin_centers[1]-bin_centers[0], 
                alpha=0.6, label='Dados')
        s = np.linspace(0, 4, 100)
        wigner = (np.pi / 2) * s * np.exp(-np.pi * s**2 / 4)
        ax2.plot(s, wigner, 'r-', lw=2, label='Wigner surmise')
        ax2.set_xlabel('Espaçamento normalizado s')
        ax2.set_ylabel('Densidade')
        ax2.set_title('Distribuição de Espaçamentos (GUE)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    # 3. Distribuição de erros
    ax3 = axes[1, 0]
    if results:
        ax3.hist(errors, bins=20, alpha=0.7, edgecolor='black')
        ax3.axvline(np.mean(errors), color='r', linestyle='--', 
                    label=f'Média = {np.mean(errors):.2f}')
        ax3.set_xlabel('|t_k - γ_{n(k)}|')
        ax3.set_ylabel('Frequência')
        ax3.set_title('Distribuição de Erros na Correspondência')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    # 4. Zeros de Riemann
    ax4 = axes[1, 1]
    zeros = riemann_zeros(100)
    ax4.scatter(range(1, len(zeros)+1), zeros, s=10, alpha=0.7)
    # Curva assintótica: γ_n ~ 2πn / log(n)
    n_vals = np.arange(1, len(zeros)+1)
    asymptotic = 2 * np.pi * n_vals / np.log(n_vals + 1)
    ax4.plot(n_vals, asymptotic, 'r--', label='Assintótico: 2πn/log(n)')
    ax4.set_xlabel('n')
    ax4.set_ylabel('γ_n')
    ax4.set_title('Zeros de Riemann vs Assintótico')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('primzeit_verification_plots.png', dpi=150)
    plt.show()
    print("\nGráficos salvos em 'primzeit_verification_plots.png'")

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

def run_all_tests():
    """Executa todos os testes de verificação."""
    print("\n" + "=" * 70)
    print("   PRIMZEIT-RIEMANN OSCILLATOR: SUITE DE VERIFICAÇÃO NUMÉRICA")
    print("=" * 70)
    print()
    
    if HAS_MPMATH:
        print("✓ mpmath disponível - usando alta precisão")
    else:
        print("⚠ mpmath não disponível - usando precisão padrão")
    print()
    
    # Teste 1: Correspondência
    print("\n" + "─" * 70)
    test_correspondence(n_test=100)
    
    # Teste 2: GUE
    print("\n" + "─" * 70)
    test_gue_statistics(n_zeros=200)
    
    # Teste 3: Fórmula de traço
    print("\n" + "─" * 70)
    test_trace_formula(n_zeros=100, n_primes=500)
    
    # Teste 4: Operador H
    print("\n" + "─" * 70)
    test_operator_spectrum(N_grid=128, n_primes=30)
    
    print("\n" + "=" * 70)
    print("   VERIFICAÇÃO COMPLETA")
    print("=" * 70)
    print()
    print("LEMBRETE: Verificação numérica ≠ prova matemática!")
    print("Estes testes servem para guiar intuição, não para provar teoremas.")
    print()

if __name__ == "__main__":
    run_all_tests()
    
    # Descomentar para gerar gráficos:
    # plot_all_results()
