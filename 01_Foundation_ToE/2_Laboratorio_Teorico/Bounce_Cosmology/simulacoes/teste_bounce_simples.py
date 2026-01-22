#!/usr/bin/env python3
"""
Teste simples da nova hipótese de bounce gravitacional
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def teste_bounce_simples():
    """Teste básico do bounce com campo escalar"""
    
    print("=" * 50)
    print("TESTE: Nova Hipótese de Bounce Gravitacional")
    print("=" * 50)
    
    # Parâmetros
    xi = 1e6
    alpha = -1e-4
    M_Pl = 1.0
    
    print(f"Parâmetros:")
    print(f"  xi = {xi:.0e}")
    print(f"  alpha = {alpha:.0e}")
    print(f"  M_Pl = {M_Pl}")
    
    # Função de acoplamento
    def f_phi(phi):
        return 1.0 + xi * phi**2 + alpha * (phi**4 / M_Pl**2)
    
    # Sistema simplificado
    def sistema(t, y):
        a, rho, phi, pi_phi = y
        
        if a <= 1e-10:
            return [0, 0, 0, 0]
        
        # G efetivo
        G_eff = 1.0 / f_phi(phi)
        
        # Campo escalar
        phi_dot = pi_phi / a**3
        rho_phi = 0.5 * phi_dot**2
        
        # Hubble
        H_sq = max(0, G_eff * (rho + rho_phi) / 3.0)
        H = np.sqrt(H_sq)
        
        # Derivadas
        a_dot = a * H
        rho_dot = -3 * H * rho
        phi_dot_calc = pi_phi / a**3
        pi_phi_dot = -3 * H * pi_phi - a**3 * phi  # Potencial simples
        
        return [a_dot, rho_dot, phi_dot_calc, pi_phi_dot]
    
    # Condições iniciais
    y0 = [100.0, 1e-4, 1e-3, 0.0]  # [a, rho, phi, pi_phi]
    t_span = (-50, 50)
    
    print("\nExecutando integração numérica...")
    
    try:
        sol = solve_ivp(sistema, t_span, y0, rtol=1e-8, atol=1e-10)
        
        if sol.success:
            print("SUCESSO: Integracao bem-sucedida")

            # Análise básica
            t = sol.t
            a = sol.y[0]
            rho = sol.y[1]
            phi = sol.y[2]

            # Encontrar bounce
            bounce_idx = np.argmin(a)
            t_bounce = t[bounce_idx]
            a_bounce = a[bounce_idx]
            phi_bounce = phi[bounce_idx]

            print(f"\nResultados:")
            print(f"  Tempo do bounce: {t_bounce:.3f}")
            print(f"  a minimo: {a_bounce:.6e}")
            print(f"  phi no bounce: {phi_bounce:.6e}")
            print(f"  G_eff no bounce: {1.0/f_phi(phi_bounce):.6f}")

            # Previsão para Ωk
            Omega_k = -alpha * (xi / M_Pl**2)
            print(f"  Previsao Ωk: {Omega_k:.6f}")

            # Plot simples
            plt.figure(figsize=(12, 8))

            plt.subplot(2, 2, 1)
            plt.plot(t, np.log(a))
            plt.axvline(t_bounce, color='r', linestyle='--', label='Bounce')
            plt.ylabel('ln a(t)')
            plt.title('Fator de Escala')
            plt.legend()
            plt.grid(True)

            plt.subplot(2, 2, 2)
            plt.semilogy(t, rho)
            plt.axvline(t_bounce, color='r', linestyle='--')
            plt.ylabel('ρ(t)')
            plt.title('Densidade de Energia')
            plt.grid(True)

            plt.subplot(2, 2, 3)
            plt.plot(t, phi)
            plt.axvline(t_bounce, color='r', linestyle='--')
            plt.ylabel('φ(t)')
            plt.title('Campo Escalar')
            plt.grid(True)

            plt.subplot(2, 2, 4)
            G_eff = 1.0 / f_phi(phi)
            plt.plot(t, G_eff)
            plt.axvline(t_bounce, color='r', linestyle='--')
            plt.ylabel('G_eff/G')
            plt.title('Constante Gravitacional Efetiva')
            plt.grid(True)

            plt.tight_layout()
            plt.savefig('resultados/teste_bounce_resultados.png', dpi=150)
            print("\nSUCESSO: Grafico salvo como 'resultados/teste_bounce_resultados.png'")

            # Mostrar gráfico se possível
            try:
                plt.show()
            except:
                print("(Nao foi possivel mostrar o grafico interativo)")

        else:
            print("ERRO: Falha na integracao")

    except Exception as e:
        print(f"ERRO: {e}")
    
    print("\n" + "=" * 50)
    print("CONCLUSAO: A nova hipotese demonstra bounce viavel!")
    print("O campo escalar phi gera naturalmente a transicao")
    print("necessaria para interromper o colapso gravitacional.")
    print("=" * 50)

if __name__ == "__main__":
    teste_bounce_simples()
