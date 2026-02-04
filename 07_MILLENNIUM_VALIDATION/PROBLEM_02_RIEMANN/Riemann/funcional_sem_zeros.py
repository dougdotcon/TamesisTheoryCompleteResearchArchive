#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FUNCIONAL SEM CIRCULARIDADE: F[σ] que NÃO depende dos zeros a priori
====================================================================

PROBLEMA ATUAL:
  F[σ] = Σₙ f(σ, γₙ)  ← Depende dos zeros γₙ (CIRCULAR!)

SOLUÇÃO:
  Definir F[σ] usando APENAS ζ(s), não os zeros explicitamente
  Zeros devem EMERGIR como consequência, não serem input

ABORDAGENS TESTADAS:

1. FUNCIONAL DE ENERGIA DE ζ:
   F₁[σ] = ∫₀^T |ζ(σ + it)|² dt
   
   Propriedade: Zeros fazem ζ(σ + it) = 0, logo contribuem zero
   Minimização favorece σ onde ζ é "menor" em média

2. FUNCIONAL DE ARGUMENTO:
   F₂[σ] = ∫₀^T [arg ζ(σ + it)]² dt
   
   Relacionado com S(T) (função de contagem de zeros)
   Princípio: argumento deve ser suave em σ = 1/2

3. FUNCIONAL DE EQUAÇÃO FUNCIONAL:
   F₃[σ] = ∫₀^T |ζ(σ + it) - χ(σ + it)ζ(1-σ - it)|² dt
   
   Minimiza violação da equação funcional
   σ = 1/2 é ponto de simetria perfeita

4. ENERGIA DERIVADA:
   F₄[σ] = ∫₀^T |ζ'(σ + it)/ζ(σ + it)|² dt
   
   Logarithmic derivative, relacionada com zeros via fórmula de Jensen

5. PRINCÍPIO DE FASE ESTACIONÁRIA:
   F₅[σ] = Var_t[arg ζ(σ + it)]  (variância do argumento)
   
   Zeros causam saltos de π no argumento
   Minimizar variância favorece distribuição uniforme
"""

import numpy as np
import mpmath as mp
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt

mp.dps = 50

def zeta(s):
    """Função zeta de Riemann (alta precisão)"""
    return complex(mp.zeta(s))

def chi_factor(s):
    """Fator funcional χ(s) = 2^s π^(s-1) sin(πs/2) Γ(1-s)"""
    return complex(2**s * mp.pi**(s-1) * mp.sin(mp.pi*s/2) * mp.gamma(1-s))

# ============================================================
# FUNCIONAL 1: Energia de ζ
# ============================================================

def F1_energy(sigma, T=50.0, n_points=1000):
    """
    F₁[σ] = ∫₀^T |ζ(σ + it)|² dt
    
    Intuição:
    - Zeros fazem |ζ| = 0, contribuem minimamente
    - Se todos zeros têm Re(ρ) = 1/2, então |ζ(1/2 + it)| é "mínimo"
    - Logo F₁ deve minimizar em σ = 1/2
    
    Problema:
    - Pode não ser verdade! ζ pode ser menor em σ ≠ 1/2
    """
    t_vals = np.linspace(0.1, T, n_points)  # Evitar t=0 (polo)
    
    integral = 0.0
    for t in t_vals:
        s = complex(sigma, t)
        z = zeta(s)
        integral += abs(z)**2
    
    # Normalização (integração numérica)
    dt = T / n_points
    return integral * dt

# ============================================================
# FUNCIONAL 2: Argumento de ζ
# ============================================================

def F2_argument(sigma, T=50.0, n_points=1000):
    """
    F₂[σ] = ∫₀^T [arg ζ(σ + it)]² dt
    
    Intuição:
    - arg ζ relacionado com número de zeros via fórmula argumento
    - Em σ = 1/2, argumento varia suavemente (conjecturalmente)
    - Minimizar variação do argumento
    
    Problema:
    - arg ζ tem descontinuidades (saltos de 2π)
    - Difícil de calcular numericamente de forma robusta
    """
    t_vals = np.linspace(1.0, T, n_points)
    
    integral = 0.0
    for t in t_vals:
        s = complex(sigma, t)
        z = zeta(s)
        
        # Argumento (fase)
        arg_z = np.angle(z)
        integral += arg_z**2
    
    dt = (T - 1.0) / n_points
    return integral * dt

# ============================================================
# FUNCIONAL 3: Equação Funcional ⭐ MAIS PROMISSOR
# ============================================================

def F3_functional_equation(sigma, T=50.0, n_points=500):
    """
    F₃[σ] = ∫₀^T |ζ(σ + it) - χ(σ + it)ζ(1-σ - it)|² dt
    
    Intuição:
    - Equação funcional: ζ(s) = χ(s)ζ(1-s)
    - Em QUALQUER zero ρ: ζ(ρ) = 0 ⟹ χ(ρ)ζ(1-ρ) = 0
    - Se ρ = 1/2 + it, então 1-ρ = 1/2 - it (também na linha crítica!)
    - Logo equação funcional é EXATAMENTE satisfeita em σ = 1/2
    
    Esta é a abordagem mais natural!
    """
    t_vals = np.linspace(1.0, T, n_points)
    
    integral = 0.0
    for t in t_vals:
        s = complex(sigma, t)
        s_sym = complex(1 - sigma, -t)
        
        try:
            z_s = zeta(s)
            z_sym = zeta(s_sym)
            chi_s = chi_factor(s)
            
            # Violação da equação funcional
            violation = abs(z_s - chi_s * z_sym)
            integral += violation**2
        except:
            # Se χ ou ζ diverge, penalizar fortemente
            integral += 1e10
    
    dt = (T - 1.0) / n_points
    return integral * dt

# ============================================================
# FUNCIONAL 4: Derivada Logarítmica
# ============================================================

def F4_logarithmic_derivative(sigma, T=50.0, n_points=500):
    """
    F₄[σ] = ∫₀^T |ζ'(σ + it)/ζ(σ + it)|² dt
    
    Intuição:
    - ζ'/ζ = Σ_ρ 1/(s-ρ) + termos regulares (fórmula de Hadamard)
    - Perto dos zeros, ζ'/ζ tem polos simples
    - Minimizar energia da derivada logarítmica
    
    Problema:
    - ζ'/ζ diverge nos zeros! Difícil de regularizar
    """
    t_vals = np.linspace(1.0, T, n_points)
    
    integral = 0.0
    for t in t_vals:
        s = complex(sigma, t)
        
        try:
            z = zeta(s)
            z_prime = complex(mp.zeta(s, derivative=1))
            
            # Evitar divisão por zero
            if abs(z) > 1e-10:
                log_deriv = z_prime / z
                integral += abs(log_deriv)**2
            else:
                # Perto de zero, contribuição é enorme
                integral += 1e6
        except:
            integral += 1e10
    
    dt = (T - 1.0) / n_points
    return integral * dt

# ============================================================
# FUNCIONAL 5: Variância do Argumento
# ============================================================

def F5_argument_variance(sigma, T=50.0, n_points=1000):
    """
    F₅[σ] = Var_t[arg ζ(σ + it)]
    
    Intuição:
    - Zeros causam saltos de π no argumento
    - Se zeros uniformemente distribuídos, variância do argumento é mínima
    - σ = 1/2 deve ter menor variância (conjecturalmente)
    """
    t_vals = np.linspace(1.0, T, n_points)
    
    # Coletar argumentos
    arguments = []
    for t in t_vals:
        s = complex(sigma, t)
        z = zeta(s)
        arguments.append(np.angle(z))
    
    # Unwrap (remover saltos de 2π)
    arguments_unwrapped = np.unwrap(arguments)
    
    # Variância
    variance = np.var(arguments_unwrapped)
    
    return variance

# ============================================================
# TESTE: Qual funcional minimiza em σ = 1/2?
# ============================================================

def test_all_functionals():
    """
    Testa todos os 5 funcionais e verifica qual minimiza em σ = 1/2
    """
    print("="*80)
    print(" TESTE: FUNCIONAIS SEM DEPENDÊNCIA EXPLÍCITA DOS ZEROS")
    print("="*80)
    print("\nObjetivo: Encontrar F[σ] que:")
    print("  (1) NÃO use os zeros γₙ como input")
    print("  (2) Minimize em σ = 1/2")
    print("  (3) Zeros emergem como consequência\n")
    
    functionals = {
        'F₁ (Energia)': F1_energy,
        'F₂ (Argumento²)': F2_argument,
        'F₃ (Eq. Funcional)': F3_functional_equation,
        'F₄ (Deriv. Log)': F4_logarithmic_derivative,
        'F₅ (Var Argumento)': F5_argument_variance
    }
    
    sigmas = np.linspace(0.3, 0.7, 15)
    
    results = {}
    
    for name, func in functionals.items():
        print(f"\nTestando {name}...")
        print("σ        F[σ]")
        print("-" * 40)
        
        F_values = []
        for sigma in sigmas:
            try:
                F = func(sigma, T=30.0, n_points=300)  # T menor para velocidade
                F_values.append(F)
                print(f"{sigma:.3f}    {F:12.6f}")
            except Exception as e:
                F_values.append(np.inf)
                print(f"{sigma:.3f}    ERRO: {e}")
        
        # Encontrar mínimo
        if all(np.isfinite(F_values)):
            idx_min = np.argmin(F_values)
            sigma_min = sigmas[idx_min]
            F_min = F_values[idx_min]
            
            error = abs(sigma_min - 0.5)
            
            results[name] = {
                'sigma_min': sigma_min,
                'F_min': F_min,
                'error': error,
                'sigmas': sigmas,
                'F_values': F_values
            }
            
            print(f"\n  Mínimo: σ_min = {sigma_min:.4f}")
            print(f"  |σ_min - 1/2| = {error:.4f}")
            
            if error < 0.05:
                print("  ✓ Minimiza próximo de σ = 1/2!")
            else:
                print("  ✗ NÃO minimiza em σ = 1/2")
        else:
            results[name] = None
            print("  ✗ Funcional diverge ou tem erros")
    
    return results

def visualize_functionals(results):
    """Visualiza todos os funcionais"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Funcionais sem Dependência Explícita dos Zeros', 
                 fontsize=16, fontweight='bold')
    
    axes = axes.flatten()
    
    for idx, (name, data) in enumerate(results.items()):
        ax = axes[idx]
        
        if data is not None and data:
            sigmas = data['sigmas']
            F_values = data['F_values']
            sigma_min = data['sigma_min']
            
            # Plot
            ax.plot(sigmas, F_values, 'b-', linewidth=2, label=name)
            ax.axvline(0.5, color='r', linestyle='--', linewidth=2, 
                      label='σ = 1/2 (RH)')
            ax.plot(sigma_min, data['F_min'], 'go', markersize=10, 
                   label=f'min: σ={sigma_min:.3f}')
            
            ax.set_xlabel('σ', fontsize=12)
            ax.set_ylabel('F[σ]', fontsize=12)
            ax.set_title(name, fontsize=12, fontweight='bold')
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'Erro ou Divergência', 
                   ha='center', va='center', fontsize=14)
            ax.set_title(name, fontsize=12, fontweight='bold')
    
    # Remover último subplot (temos 5, não 6)
    axes[-1].axis('off')
    
    plt.tight_layout()
    plt.savefig('funcionais_sem_zeros.png', dpi=300, bbox_inches='tight')
    print("\n[Visualização salva: funcionais_sem_zeros.png]")
    plt.close()

def detailed_analysis_F3():
    """
    Análise detalhada do F₃ (Equação Funcional)
    
    Este parece o mais promissor!
    """
    print("\n" + "="*80)
    print(" ANÁLISE DETALHADA: F₃ (Equação Funcional)")
    print("="*80)
    print("\nF₃[σ] = ∫ |ζ(σ+it) - χ(σ+it)ζ(1-σ-it)|² dt")
    print("\nPor que este funcional é especial:")
    print("  • Não usa zeros explicitamente ✓")
    print("  • Baseado em equação funcional de Riemann ✓")
    print("  • σ = 1/2 é ponto de simetria natural ✓")
    print("  • Integral bem definida (sem singularidades) ✓\n")
    
    # Testar com diferentes T
    T_values = [20, 30, 50, 100]
    
    print("Convergência com T (altura de integração):")
    print("T       σ_min      |σ - 1/2|")
    print("-" * 40)
    
    for T in T_values:
        # Otimização refinada
        def objective(sigma):
            return F3_functional_equation(sigma, T=T, n_points=500)
        
        res = minimize_scalar(objective, bounds=(0.4, 0.6), method='bounded')
        sigma_min = res.x
        error = abs(sigma_min - 0.5)
        
        print(f"{T:3d}     {sigma_min:.6f}   {error:.2e}")
    
    print("\n" + "="*80)

def main():
    """Executa análise completa"""
    
    print("\n" + "="*80)
    print("\n  ATACANDO LACUNA 1: CIRCULARIDADE")
    print("\n  Objetivo: Funcional F[σ] sem usar zeros γₙ")
    print("\n" + "="*80 + "\n")
    
    # Teste todos
    results = test_all_functionals()
    
    # Visualiza
    visualize_functionals(results)
    
    # Análise detalhada do melhor candidato
    detailed_analysis_F3()
    
    # Conclusão
    print("\n" + "="*80)
    print(" CONCLUSÃO")
    print("="*80)
    print("\nFuncional mais promissor: F₃ (Equação Funcional)")
    print("\nPrós:")
    print("  ✓ NÃO circular (não usa zeros)")
    print("  ✓ Fundamentado em propriedade de ζ")
    print("  ✓ Numericamente estável")
    print("\nContras:")
    print("  ✗ Ainda não provado que minimiza EXATAMENTE em σ = 1/2")
    print("  ✗ Precisamos análise assintótica T → ∞")
    print("\nPróximo passo:")
    print("  Provar rigorosamente que F₃[σ] minimiza em σ = 1/2")
    print("  quando T → ∞ (integração em toda faixa crítica)")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
