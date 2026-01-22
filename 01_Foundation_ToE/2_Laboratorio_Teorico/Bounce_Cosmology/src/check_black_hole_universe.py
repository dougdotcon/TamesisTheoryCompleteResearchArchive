#!/usr/bin/env python3
"""
Script de Verificação da Hipótese do Universo Buraco Negro (Gaztañaga)
"""

import numpy as np
import matplotlib.pyplot as plt
from .physics_models.black_hole_universe import UniversosBuracoNegro, validar_multiverso
from .physics_models.relativity import CamposEscalarAcoplados

def run_simulation():
    print("=== VERIFICAÇÃO DE MULTIVERSOS (BHU) ===")
    
    # 1. Definir o "Universo Pai"
    # Massa estimada do nosso universo observável ~ 5e22 M_sol
    M_parent = 5e22 
    
    print(f"\n1. Analisando Universo Pai com Massa M = {M_parent:.2e} M_sol")
    bhu = UniversosBuracoNegro(M_parent)
    
    # 2. Verificar Condição de Gaztañaga (R_s == R_H)
    match, razao = bhu.verificar_condicao_bhu(H0_target=70.0)
    print(f"   Raio de Schwarzschild: {bhu.R_s_km:.2e} km")
    print(f"   Razão Rs/RH: {razao:.4f}")
    
    if match:
        print("   ✅ CONSISTENTE: A massa é compatível com um Universo BN com H0 ~ 70.")
    else:
        print("   ⚠️ AVISO: A massa não bate exatamente com H0=70 (esperado devido a incertezas).")

    # 3. Gerar Condições Iniciais para o Rebote (Big Bang do Filho)
    print("\n2. Gerando Condições Iniciais para o Universo Filho...")
    condicoes = bhu.gerar_condicoes_iniciais_rebote()
    
    print("   Parâmetros no Horizonte de Eventos (Início):")
    for k, v in condicoes.items():
        print(f"   - {k}: {v:.2e}")

    # 4. Simular a Dinâmica do Rebote (Universo Filho)
    print("\n3. Executando Simulação de Rebote Gravitacional Modificado...")
    # Usamos o modelo de Campo Escalar Não-Mínimo (Gravidade Modificada)
    modelo_bounce = CamposEscalarAcoplados(xi=1e4, alpha=-1e-6) # Parâmetros ajustados
    
    # A simulação deve mostrar a transição
    evol = modelo_bounce.evolucao_campo_bounce(
        t_span=(-1e-35, 1e-32), # Escala de tempo muito pequena (Planckian)
        n_pontos=500,
        initial_conditions=condicoes
    )
    
    if evol['sucesso']:
        print("   ✅ Simulação concluída com sucesso!")
        
        # Análise básica dos resultados
        a_final = evol['a'][-1]
        H_final = (evol['a'][-1] - evol['a'][-2]) / (evol['t'][-1] - evol['t'][-2]) / evol['a'][-1]
        
        print(f"   Fator de escala final: {a_final:.2e}")
        print(f"   Hubble final estimativo: {H_final:.2e}")
        
        # Plot simples (se possível mostrar)
        try:
            plt.figure(figsize=(10, 6))
            plt.subplot(2, 1, 1)
            plt.plot(evol['t'], evol['a'])
            plt.title('Fator de Escala a(t) - Universo Filho')
            plt.ylabel('a(t)')
            plt.yscale('log')
            
            plt.subplot(2, 1, 2)
            plt.plot(evol['t'], evol['phi'])
            plt.title('Campo Escalar (Ordem Termodinâmica)')
            plt.xlabel('Tempo')
            plt.ylabel('phi')
            
            plt.tight_layout()
            plt.savefig('bhu_simulation_results.png')
            print("   📊 Gráfico gerado: bhu_simulation_results.png")
        except Exception as e:
            print(f"   (Plot não gerado: {e})")
            
    else:
        print("   ❌ Falha na simulação do rebote.")

if __name__ == "__main__":
    run_simulation()
