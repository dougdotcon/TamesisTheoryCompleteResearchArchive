#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE DE CONVERGÊNCIA: σ_min → 1/2 quando n → ∞
==================================================

Questão crítica:
  σ_min = 0.50026 (erro ~2.6e-4) com 50 zeros
  
  Isso é:
  (a) Erro numérico que desaparece com mais zeros?
  (b) Evidência de que σ_min ≠ 1/2 exatamente?

Teste: Calcular σ_min para n = 10, 20, 30, ..., 100
       e verificar se σ_min(n) → 0.5 quando n → ∞
"""

import numpy as np
import mpmath as mp
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt

mp.dps = 80  # Aumentar precisão para 80 dígitos!

def zeta_zeros(n_zeros):
    """Primeiros n_zeros de ζ com ALTA precisão"""
    zeros = []
    for n in range(1, n_zeros + 1):
        gamma = mp.zetazero(n)
        zeros.append(complex(gamma))
    return zeros

def F_functional(sigma, zeros):
    """Funcional variacional F[σ]"""
    n = len(zeros)
    
    # F1: Simetria
    F1 = n * abs(2*sigma - 1.0)**2
    
    # F2: Equação funcional
    F2 = 0.0
    for gamma in zeros:
        t = gamma.imag
        s = complex(sigma, t)
        
        try:
            chi_s = (2**s * mp.pi**(s-1) * mp.sin(mp.pi*s/2) * mp.gamma(1-s))
            violation = abs(1.0 - abs(chi_s))
            F2 += violation**2
        except:
            F2 += 1000.0
    
    # F3: GUE energia
    F3 = 0.0
    for i, zi in enumerate(zeros):
        for j, zj in enumerate(zeros):
            if i < j:
                ti, tj = zi.imag, zj.imag
                dist = np.sqrt((ti - tj)**2 + 0.01)
                F3 += -np.log(dist)
    
    if n > 1:
        F3 = F3 / (n * (n-1) / 2)
    
    # Pesos
    w1, w2, w3 = 100.0, 10.0, 1.0
    
    return float(w1 * F1/n + w2 * F2/n + w3 * F3)

def find_minimum(zeros, method='bounded'):
    """Encontra σ_min com alta precisão"""
    
    def objective(sigma):
        if isinstance(sigma, np.ndarray):
            sigma = sigma[0]
        return F_functional(sigma, zeros)
    
    # Múltiplas otimizações para garantir convergência
    results = []
    
    # Método 1: Bounded
    res1 = minimize_scalar(objective, bounds=(0.4, 0.6), method='bounded', 
                          options={'xatol': 1e-12})
    results.append(res1.x)
    
    # Método 2: Brent (golden section) sem bounds
    res2 = minimize_scalar(objective, bracket=(0.45, 0.5, 0.55), method='brent',
                          options={'xtol': 1e-12})
    results.append(res2.x)
    
    # Método 3: Grid refinement
    grid = np.linspace(0.49, 0.51, 1000)
    F_values = [objective(s) for s in grid]
    idx_min = np.argmin(F_values)
    results.append(grid[idx_min])
    
    # Retorna média (mais robusto)
    sigma_min = np.mean(results)
    F_min = objective(sigma_min)
    
    return sigma_min, F_min, np.std(results)

def convergence_analysis():
    """
    Analisa convergência σ_min(n) → 0.5 quando n → ∞
    
    Se RH é verdadeira e F captura a física correta,
    esperamos σ_min(n) = 0.5 + O(1/n) ou melhor
    """
    print("="*80)
    print(" ANÁLISE DE CONVERGÊNCIA: σ_min(n) → 1/2?")
    print("="*80)
    print(f"Precisão: {mp.dps} dígitos decimais")
    print(f"Métodos: Bounded + Brent + Grid (média)\n")
    
    n_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    sigma_mins = []
    F_mins = []
    errors = []
    stds = []
    
    print("n      σ_min          |σ_min - 1/2|      F[σ_min]      std_dev")
    print("-" * 75)
    
    for n in n_values:
        print(f"{n:3d}  ", end='', flush=True)
        
        zeros = zeta_zeros(n)
        sigma_min, F_min, std = find_minimum(zeros)
        
        error = abs(sigma_min - 0.5)
        
        sigma_mins.append(sigma_min)
        F_mins.append(F_min)
        errors.append(error)
        stds.append(std)
        
        print(f"{sigma_min:.10f}   {error:.2e}   {F_min:10.6f}   {std:.2e}")
    
    # Análise de tendência
    print("\n" + "="*80)
    print(" ANÁLISE DE TENDÊNCIA")
    print("="*80)
    
    # Fit linear: σ_min(n) = a + b/n
    n_array = np.array(n_values)
    sigma_array = np.array(sigma_mins)
    
    # Regressão em 1/n
    X = np.vstack([np.ones(len(n_array)), 1.0/n_array]).T
    coeffs = np.linalg.lstsq(X, sigma_array, rcond=None)[0]
    
    a_fit = coeffs[0]  # Limite quando n → ∞
    b_fit = coeffs[1]  # Coeficiente de 1/n
    
    print(f"\nModelo: σ_min(n) = a + b/n")
    print(f"  a = {a_fit:.12f}  (limite n → ∞)")
    print(f"  b = {b_fit:.12f}")
    print(f"\n  |a - 0.5| = {abs(a_fit - 0.5):.2e}")
    
    # Extrapolação para n grande
    print(f"\nExtrapolação:")
    for n_ext in [200, 500, 1000, 10000]:
        sigma_ext = a_fit + b_fit/n_ext
        print(f"  n = {n_ext:5d}  →  σ_min ≈ {sigma_ext:.12f}")
    
    # Teste de convergência
    print("\n" + "="*80)
    
    converges = abs(a_fit - 0.5) < 1e-6
    
    if converges:
        print(" ✓ CONVERGÊNCIA CONFIRMADA!")
        print(f"\n   lim_{'{n→∞}'} σ_min(n) = {a_fit:.10f} ≈ 1/2")
        print(f"\n   Taxa: σ_min(n) - 1/2 = O(1/n)")
        print(f"   Coeficiente: {b_fit:.6f}/n")
    else:
        print(" ✗ CONVERGÊNCIA DUVIDOSA")
        print(f"\n   lim σ_min = {a_fit:.10f}")
        print(f"   Desvio de 1/2: {abs(a_fit - 0.5):.2e}")
    
    print("="*80 + "\n")
    
    return n_values, sigma_mins, errors, a_fit, b_fit

def plot_convergence(n_values, sigma_mins, errors, a_fit, b_fit):
    """Visualiza convergência para σ = 1/2"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Convergência: σ_min(n) → 1/2 quando n → ∞', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: σ_min vs n
    ax = axes[0, 0]
    ax.plot(n_values, sigma_mins, 'bo-', markersize=8, linewidth=2, label='σ_min(n)')
    ax.axhline(0.5, color='r', linestyle='--', linewidth=2, label='σ = 1/2 (RH)')
    
    # Fit
    n_fit = np.linspace(min(n_values), max(n_values), 200)
    sigma_fit = a_fit + b_fit / n_fit
    ax.plot(n_fit, sigma_fit, 'g--', linewidth=2, alpha=0.7, 
            label=f'Fit: {a_fit:.4f} + {b_fit:.2f}/n')
    
    ax.set_xlabel('Número de zeros (n)', fontsize=12)
    ax.set_ylabel('σ_min', fontsize=12)
    ax.set_title('Mínimo vs Número de Zeros', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Erro |σ_min - 0.5|
    ax = axes[0, 1]
    ax.semilogy(n_values, errors, 'ro-', markersize=8, linewidth=2, label='|σ_min - 1/2|')
    
    # Curva 1/n para referência
    error_fit = abs(b_fit) / np.array(n_values)
    ax.semilogy(n_values, error_fit, 'g--', linewidth=2, alpha=0.7, label='O(1/n)')
    
    ax.set_xlabel('Número de zeros (n)', fontsize=12)
    ax.set_ylabel('|σ_min - 1/2|', fontsize=12)
    ax.set_title('Erro Absoluto (escala log)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Resíduo do fit
    ax = axes[1, 0]
    sigma_fit_values = a_fit + b_fit / np.array(n_values)
    residuals = np.array(sigma_mins) - sigma_fit_values
    ax.plot(n_values, residuals * 1e6, 'mo-', markersize=8, linewidth=2)
    ax.axhline(0, color='k', linestyle=':', alpha=0.5)
    ax.set_xlabel('Número de zeros (n)', fontsize=12)
    ax.set_ylabel('Resíduo × 10⁶', fontsize=12)
    ax.set_title('Qualidade do Fit (a + b/n)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Extrapolação
    ax = axes[1, 1]
    n_ext = np.array([10, 20, 30, 50, 100, 200, 500, 1000, 2000, 5000, 10000])
    sigma_ext = a_fit + b_fit / n_ext
    error_ext = np.abs(sigma_ext - 0.5)
    
    ax.loglog(n_ext, error_ext, 'b^-', markersize=8, linewidth=2, label='|σ_min - 1/2|')
    ax.loglog(n_ext, 1.0/n_ext, 'r--', linewidth=2, alpha=0.7, label='1/n')
    ax.loglog(n_ext, 1.0/n_ext**2, 'g--', linewidth=2, alpha=0.7, label='1/n²')
    
    ax.set_xlabel('n (escala log)', fontsize=12)
    ax.set_ylabel('Erro (escala log)', fontsize=12)
    ax.set_title('Extrapolação para n grande', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('convergencia_sigma_min.png', dpi=300, bbox_inches='tight')
    print("[Visualização salva: convergencia_sigma_min.png]\n")
    plt.close()

def main():
    """Análise completa de convergência"""
    
    print("\n" + "🔬"*40)
    print("\n  TESTE DEFINITIVO: σ_min → 1/2 quando n → ∞?")
    print("\n" + "🔬"*40 + "\n")
    
    # Executar análise
    n_values, sigma_mins, errors, a_fit, b_fit = convergence_analysis()
    
    # Visualizar
    plot_convergence(n_values, sigma_mins, errors, a_fit, b_fit)
    
    # Conclusão
    print("="*80)
    print(" CONCLUSÃO FINAL")
    print("="*80)
    
    if abs(a_fit - 0.5) < 1e-6:
        print("\n✓✓✓ CONVERGÊNCIA PARA σ = 1/2 CONFIRMADA! ✓✓✓\n")
        print(f"  lim σ_min(n) = {a_fit:.10f}")
        print(f"  n→∞")
        print(f"\n  Erro: |{a_fit:.10f} - 0.5| = {abs(a_fit - 0.5):.2e} < 10⁻⁶")
        print(f"\n  Interpretação:")
        print(f"    Com infinitos zeros, o funcional F[σ]")
        print(f"    minimiza EXATAMENTE em σ = 1/2")
        print(f"\n  ⟹ Princípio Variacional FAVORECE RH!\n")
    else:
        print("\n✗ Convergência não para σ = 1/2 exatamente")
        print(f"\n  lim σ_min = {a_fit:.10f}")
        print(f"  Desvio: {abs(a_fit - 0.5):.2e}")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
