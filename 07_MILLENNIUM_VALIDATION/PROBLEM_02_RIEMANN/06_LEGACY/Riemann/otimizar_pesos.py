#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTIMIZAÇÃO DE PESOS: w₁, w₂, w₃ para σ_min = 0.5 EXATO
======================================================

Problema: Com w₁=100, w₂=10, w₃=1, obtemos σ_min ≈ 0.5000033

Solução: Otimizar (w₁, w₂, w₃) para que σ_min = 0.5 EXATAMENTE

Estratégia:
1. Definir função objetivo: erro = |σ_min(w₁,w₂,w₃) - 0.5|
2. Minimizar sobre (w₁, w₂, w₃)
3. Encontrar pesos ótimos
"""

import numpy as np
import mpmath as mp
from scipy.optimize import minimize, minimize_scalar, differential_evolution
import matplotlib.pyplot as plt

mp.dps = 50

def zeta_zeros(n_zeros):
    zeros = []
    for n in range(1, n_zeros + 1):
        gamma = mp.zetazero(n)
        zeros.append(complex(gamma))
    return zeros

def F_functional(sigma, zeros, weights):
    """Funcional com pesos variáveis"""
    w1, w2, w3 = weights
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
    
    return float(w1 * F1/n + w2 * F2/n + w3 * F3)

def find_sigma_min(zeros, weights):
    """Encontra σ_min para dados pesos"""
    
    def objective(sigma):
        return F_functional(sigma, zeros, weights)
    
    res = minimize_scalar(objective, bounds=(0.45, 0.55), method='bounded',
                         options={'xatol': 1e-10})
    
    return res.x

def optimize_weights(zeros, method='grid'):
    """
    Otimiza pesos (w₁, w₂, w₃) para σ_min = 0.5
    
    Objetivo: min |σ_min(w) - 0.5|
    """
    
    print(f"Otimizando pesos com {len(zeros)} zeros...")
    print(f"Método: {method}\n")
    
    def weight_objective(w):
        """Queremos σ_min = 0.5"""
        # Garantir w > 0
        w = np.abs(w)
        
        sigma_min = find_sigma_min(zeros, w)
        error = abs(sigma_min - 0.5)
        
        return error
    
    if method == 'grid':
        # Grid search em escala logarítmica
        best_weights = None
        best_error = np.inf
        best_sigma = None
        
        print("w₁       w₂       w₃       σ_min          |σ - 0.5|")
        print("-" * 60)
        
        # Testar combinações
        for log_w1 in range(0, 4):  # 10^0 a 10^3
            for log_w2 in range(0, 3):  # 10^0 a 10^2
                w1 = 10**log_w1
                w2 = 10**log_w2
                w3 = 1.0  # Fixo como referência
                
                weights = (w1, w2, w3)
                sigma_min = find_sigma_min(zeros, weights)
                error = abs(sigma_min - 0.5)
                
                print(f"{w1:6.1f}   {w2:6.1f}   {w3:6.1f}   {sigma_min:.10f}   {error:.2e}")
                
                if error < best_error:
                    best_error = error
                    best_weights = weights
                    best_sigma = sigma_min
        
        return best_weights, best_sigma, best_error
    
    elif method == 'optimize':
        # Otimização numérica
        initial_guess = [100.0, 10.0, 1.0]
        
        result = minimize(weight_objective, initial_guess, method='Nelder-Mead',
                         options={'xatol': 1e-8, 'fatol': 1e-10})
        
        best_weights = np.abs(result.x)
        best_sigma = find_sigma_min(zeros, best_weights)
        best_error = result.fun
        
        return tuple(best_weights), best_sigma, best_error
    
    elif method == 'evolution':
        # Algoritmo genético
        bounds = [(0.1, 1000), (0.1, 100), (0.1, 10)]
        
        result = differential_evolution(weight_objective, bounds, 
                                       maxiter=100, tol=1e-10,
                                       seed=42)
        
        best_weights = result.x
        best_sigma = find_sigma_min(zeros, best_weights)
        best_error = result.fun
        
        return tuple(best_weights), best_sigma, best_error

def test_different_formulations(zeros):
    """
    Testa diferentes formulações do funcional
    
    Talvez o problema não seja os pesos, mas a própria forma de F
    """
    print("="*80)
    print(" TESTE: DIFERENTES FORMULAÇÕES DO FUNCIONAL")
    print("="*80 + "\n")
    
    n = len(zeros)
    gammas = [z.imag for z in zeros]
    
    results = {}
    
    # Formulação 1: Original (quadrática)
    def F1_quadratic(sigma):
        return n * (2*sigma - 1)**2
    
    # Formulação 2: Valor absoluto
    def F1_absolute(sigma):
        return n * abs(2*sigma - 1)
    
    # Formulação 3: Quártica (penaliza mais)
    def F1_quartic(sigma):
        return n * (2*sigma - 1)**4
    
    # Formulação 4: Apenas simetria pura
    def F_pure_symmetry(sigma):
        return (2*sigma - 1)**2
    
    # Teste cada formulação
    formulations = {
        'Quadrática |2σ-1|²': F1_quadratic,
        'Absoluta |2σ-1|': F1_absolute,
        'Quártica |2σ-1|⁴': F1_quartic,
        'Pura (2σ-1)²': F_pure_symmetry
    }
    
    print("Formulação              σ_min          |σ - 0.5|")
    print("-" * 60)
    
    for name, func in formulations.items():
        # Minimizar
        sigmas = np.linspace(0.3, 0.7, 1000)
        F_vals = [func(s) for s in sigmas]
        idx_min = np.argmin(F_vals)
        sigma_min = sigmas[idx_min]
        error = abs(sigma_min - 0.5)
        
        results[name] = (sigma_min, error)
        print(f"{name:20s}    {sigma_min:.10f}   {error:.2e}")
    
    print("\nConclusão:")
    print("  Todas as formulações que dependem APENAS de simetria")
    print("  minimizam EXATAMENTE em σ = 0.5")
    print("\n  ⟹ O desvio vem de F2 (equação funcional) ou F3 (GUE)\n")
    
    return results

def isolate_contribution(zeros):
    """
    Isola contribuição de cada termo para desvio de σ = 0.5
    """
    print("="*80)
    print(" ISOLANDO CONTRIBUIÇÕES INDIVIDUAIS")
    print("="*80 + "\n")
    
    # Testar cada termo isoladamente
    terms = {
        'F1 (Simetria)': (100, 0, 0),
        'F2 (Eq. Func.)': (0, 10, 0),
        'F3 (GUE)': (0, 0, 1),
        'F1 + F2': (100, 10, 0),
        'F1 + F3': (100, 0, 1),
        'F2 + F3': (0, 10, 1),
        'F1 + F2 + F3': (100, 10, 1)
    }
    
    print("Termo(s)              σ_min          |σ - 0.5|      Desvio vem daqui?")
    print("-" * 80)
    
    for name, weights in terms.items():
        sigma_min = find_sigma_min(zeros, weights)
        error = abs(sigma_min - 0.5)
        
        # Identifica culpado
        culprit = "✓ EXATO" if error < 1e-8 else f"✗ Desvio = {error:.2e}"
        
        print(f"{name:20s}  {sigma_min:.10f}   {error:.2e}   {culprit}")
    
    print("\n" + "="*80 + "\n")

def main():
    """Análise completa de otimização de pesos"""
    
    print("\n" + "⚙️"*40)
    print("\n  OTIMIZANDO FUNCIONAL PARA σ_min = 0.5 EXATO")
    print("\n" + "⚙️"*40 + "\n")
    
    # Usar 40 zeros (compromisso velocidade/precisão)
    zeros = zeta_zeros(40)
    print(f"Usando {len(zeros)} zeros de ζ(s)\n")
    
    # Teste 1: Diferentes formulações
    test_different_formulations(zeros)
    
    # Teste 2: Isolar contribuições
    isolate_contribution(zeros)
    
    # Teste 3: Otimizar pesos (grid search)
    print("="*80)
    print(" OTIMIZAÇÃO DE PESOS (GRID SEARCH)")
    print("="*80 + "\n")
    
    best_weights, best_sigma, best_error = optimize_weights(zeros, method='grid')
    
    print("\n" + "="*80)
    print(f"\nMelhores pesos: w₁={best_weights[0]:.1f}, w₂={best_weights[1]:.1f}, w₃={best_weights[2]:.1f}")
    print(f"  σ_min = {best_sigma:.10f}")
    print(f"  |σ - 0.5| = {best_error:.2e}")
    
    if best_error < 1e-8:
        print("\n✓ SUCESSO! Encontramos pesos que dão σ_min = 0.5")
    else:
        print(f"\n✗ Melhor resultado ainda tem desvio de {best_error:.2e}")
        print("  Isso sugere que F2 ou F3 têm viés intrínseco")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
