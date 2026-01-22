
import numpy as np
from scipy.constants import G, hbar, c

# 1. Definir Constantes Fundamentais
H0_si = 70 * 1000 / (3.086e22) # Hubble Constant ~ 2.2e-18 1/s
a0 = c * H0_si                  # Aceleração Crítica ~ 6.8e-10 m/s^2

# 2. Definir Unidades de Planck
l_P = np.sqrt(hbar * G / c**3)
m_P = np.sqrt(hbar * c / G)
t_P = l_P / c
a_P = c / t_P  # Aceleração de Planck

print(f"--- ESCALAS FUNDAMENTAIS ---")
print(f"Massa de Planck (m_P)     = {m_P:.4e} kg")
print(f"Aceleração Planck (a_P)   = {a_P:.4e} m/s^2")
print(f"Aceleração MOND (a0)      = {a0:.4e} m/s^2")

# 3. Razão Adimensional (A Hierarquia)
Xi = a0 / a_P
print(f"Razão Xi (a0/a_P)         = {Xi:.4e}")

# 4. Busca pelo Expoente k
# Hipótese: M_c = m_P * Xi^k
# Alvo: 1e-17 a 1e-14 kg

target_min = 1e-17
target_max = 1e-14

print(f"\n--- BUSCA POR EXPOENTE k (M_c = m_P * Xi^k) ---")
print(f"Target Range: {target_min:.1e} - {target_max:.1e} kg")

best_k = None
best_diff = 999

# Vamos testar expoentes fracionários simples
fractions = [1/2, 1/3, 1/4, 1/5, 1/6, 1/7, 1/8, 2/3, 3/4]

for k in fractions:
    M_test = m_P * (Xi ** k)
    
    # Check if inside range (com margem de magnitude)
    log_test = np.log10(M_test)
    log_min = np.log10(target_min)
    log_max = np.log10(target_max)
    
    match = (M_test >= target_min * 0.01) and (M_test <= target_max * 100)
    
    flag = ""
    if match:
        flag = "<--- MATCH!"
        
    print(f"k = {k:.3f} (1/{1/k:.1f}) -> M_c = {M_test:.3e} kg {flag}")

# Vamos calcular qual k exato daria 10^-15 kg
# 10^-15 = m_P * Xi^k_ideal
# Xi^k_ideal = 10^-15 / m_P
# k_ideal * log(Xi) = log(10^-15/m_P)
k_ideal = np.log(1e-15 / m_P) / np.log(Xi)
print(f"\nExpoente ideal para chegar em 1.0e-15 kg: k = {k_ideal:.4f}")
print(f"Isso é muito próximo de 1/6? (1/6 = {1/6:.4f})")

M_1_6 = m_P * (Xi ** (1/6))
print(f"\nValor para k=1/6: {M_1_6:.3e} kg")
print(f"Em Daltons (aprox): {M_1_6 / 1.66e-27:.2e} Da")

# Formula visual
# M_c = m_P * (a0/aP)^(1/6)
# Substituindo aP e mP:
# M_c = sqrt(hc/G) * [ a0 / (sqrt(c^7/hbar G)) ]^(1/6)
# Isso é complexo. Vamos ver se simplificamos a expressao.
# M_c^6 = m_P^6 * a0 / a_P
# ...

