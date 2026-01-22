#!/usr/bin/env python3
"""
Otimização de Acoplamento Não-Mínimo (Inflação Geométrica)
"""

import numpy as np
from src.physics_models.black_hole_universe import UniversosBuracoNegro
from src.physics_models.relativity import CamposEscalarAcoplados
from src.numerical_methods.optimization import OtimizacaoGlobal
import warnings

def objective_function(params):
    """
    Função de perda para otimização da inflação.
    params = [log10_xi]
    """
    log_xi = params[0]
    xi = 10**log_xi
    
    # 1. Configurar condições iniciais do BHU
    M_parent = 5e22
    bhu = UniversosBuracoNegro(M_parent)
    condicoes = bhu.gerar_condicoes_iniciais_rebote()
    
    # NORMALIZAÇÃO NUMÉRICA:
    # O valor 'a' vindo do BHU é ~1e-60. Isso explode pi_phi/a^3.
    # Definimos a=1.0 para o "início da simulação" (pós-bounce/inflação).
    condicoes['a_inicial'] = 1.0
    condicoes['pi_phi_inicial'] = 0.0 # Campo começa em repouso
    condicoes['phi_inicial'] = 5.0 # Campo com valor alto para Chaotic Inflation (Linde)
    # Se phi for 1.0, talvez não inflacione o suficiente. Ajuste para testes.
    # Mas o usuário quer Xi controlar isso. Com phi ~ 1 e Xi grande, temos Higgs Inflation.
    condicoes['phi_inicial'] = 1.0 # Mantendo consistência com BHU original, mas Xi deve compensar.
    
    # 2. Configurar modelo de gravidade modificada
    # Alpha é fixo ou também otimizável? O usuário pediu foco em Xi.
    # Alpha negativo evita instabilidade em phi muito grande?
    modelo = CamposEscalarAcoplados(xi=xi, alpha=-1e-6)
    
    # 3. Rodar simulação
    # Precisamos de tempo suficiente para inflação (60 e-folds)
    # t_planck ~ 5e-44 s. 60 e-folds ~ 100-1000 t_planck?
    # Vamos dar uma janela maior.
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Reduzir t_span ou ajustar parametros se estiver falhando na integracao
            # Agora estamos em Unidades Naturais onde t_planck = 1.
            # Queremos simular ~ 100-1000 tempos de planck para ver inflacao.
            evol = modelo.evolucao_campo_bounce(
                t_span=(0.0, 2000.0), 
                n_pontos=500, 
                initial_conditions=condicoes
            )
    except Exception as e:
        print(f"DEBUG: Simulação crashou com Xi={xi:.2e}: {e}")
        return 1e9 # Penalidade por falha
        
    if not evol['sucesso']:
        msg = evol.get('mensagem', 'Sem mensagem')
        print(f"DEBUG: Integração falhou para Xi={xi:.2e}. Msg: {msg}")
        # print(f"DEBUG: Keys: {evol.keys()}")
        return 1e9
        
    # 4. Calcular observáveis
    a = evol['a']
    
    # Número de e-folds N = ln(a_f / a_i)
    try:
        if a[-1] <= 0 or a[0] <= 0:
            print(f"DEBUG: Fator de escala invalido a_i={a[0]}, a_f={a[-1]}")
            return 1e8
        N = np.log(a[-1] / a[0])
    except:
        N = 0
        
    print(f"DEBUG: Xi={xi:.2e} -> N={N:.4f}")
        
    # Omega_k (Curvatura)
    # Omega_k = - k / (a^2 H^2). 
    # Assumindo k=+1 (fechado) herdado do buraco negro?
    # Ou k=0 se for plano?
    # Modelo BHU geralmente implica k=1 (esfera 3D).
    # Queremos Omega_k -> 0 (Flatness problem solve)
    # ISSO SIGNIFICA N GRANDE.
    # Omega_k_final ~ Omega_k_initial * exp(-2N)
    # Então maximizar N minimiza Omega_k.
    
    # Spectral Index n_s
    # Aproximação de Slow Roll para potencial V ~ phi^2 com acoplamento xi:
    # n_s ~ 1 - 2/N - 3/2N^2 ... ou formulas específicas de Higgs Inflation / Starobinsky
    # Starobinsky/Higgs (limit xi -> inf): n_s = 1 - 2/N
    # Para N=60, n_s = 1 - 2/60 = 1 - 0.033 = 0.967
    # Isso é exatamente o alvo!
    # Então, se conseguirmos N=60, teremos n_s correto automaticamente para modelos tipo Starobinsky.
    
    # Target values
    N_target = 60.0
    ns_target = 0.965
    
    # Perda
    loss_N = abs(N - N_target) / N_target * 100 # Peso percentual?
    
    # Penalizar N muito pequeno fortemente.
    if N < 1: loss_N *= 10
    
    # Se N ~ 60, assumimos n_s bom.
    # Mas podemos adicionar penalidade se Xi for muito pequeno (instabilidade)
    
    return loss_N

def run_optimization():
    print("=== OTIMIZAÇÃO DE INFLAÇÃO GEOMÉTRICA (Acoplamento Xi) ===")
    
    # Busca por Xi na escala logarítmica
    # Xi pode variar de 1 a 10^5
    bounds = [(0.0, 6.0)] # log10(xi) entre 0 (1) e 6 (10^6)
    
    print("Iniciando Evolução Diferencial para encontrar Xi Crítico...")
    
    resultado = OtimizacaoGlobal.evolucao_diferencial(
        objective_function,
        bounds=bounds,
        max_iter=20,     # Iterações rápidas
        pop_size=10,     # População pequena
        seed=42
    )
    
    if resultado['sucesso']:
        log_xi_opt = resultado['parametros_otimos'][0]
        xi_opt = 10**log_xi_opt
        print(f"\n✅ OTIMIZAÇÃO CONCLUÍDA")
        print(f"Xi Crítico Encontrado: {xi_opt:.4e} (log10 = {log_xi_opt:.4f})")
        print(f"Loss Final: {resultado['valor_otimo']:.4f}")
        
        # Validar detalhadamente
        validar_solucao(xi_opt)
    else:
        print("❌ Falha na otimização")

def validar_solucao(xi):
    print(f"\nVerificando solução para Xi = {xi:.2e}...")
    M_parent = 5e22
    bhu = UniversosBuracoNegro(M_parent)
    condicoes = bhu.gerar_condicoes_iniciais_rebote()
    
    modelo = CamposEscalarAcoplados(xi=xi, alpha=-1e-6)
    evol = modelo.evolucao_campo_bounce(
        t_span=(-1e-35, 1e-30), # Tempo um pouco maior para ver inflação
        n_pontos=500,
        initial_conditions=condicoes
    )
    
    if evol['sucesso']:
        a_i = evol['a'][0]
        a_f = evol['a'][-1]
        N = np.log(a_f / a_i)
        
        print(f"Número de e-folds obtido (N): {N:.2f}")
        
        if N > 50:
            ns_est = 1 - 2/N
            print(f"Estimativa de n_s (Starobinsky limit): {ns_est:.4f}")
            print("Status: INFLAÇÃO BEM SUCEDIDA 🚀")
        else:
            print("Status: INFLAÇÃO INSUFICIENTE (Necessita ajuste de tempo ou parâmetros)")

if __name__ == "__main__":
    run_optimization()
