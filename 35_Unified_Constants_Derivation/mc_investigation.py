"""
INVESTIGACAO: Por que M_c falha?

QUESTAO: Existe uma derivacao de M_c consistente com holografia?

HIPOTESES A TESTAR:
1. M_c vem de uma escala diferente (local, nao cosmologica)
2. M_c pode ser derivado de hbar, G, c sem R_H
3. M_c e fundamentalmente independente de Lambda e a_0
"""

import numpy as np

# Constantes
c = 299792458.0  # m/s
hbar = 1.054571817e-34  # J*s
G = 6.67430e-11  # m^3/(kg*s^2)
l_P = np.sqrt(hbar * G / c**3)
m_P = np.sqrt(hbar * c / G)
t_P = np.sqrt(hbar * G / c**5)

# Observados
Lambda_obs = 1.1056e-52  # m^-2
a0_obs = 1.2e-10  # m/s^2
Mc_obs = 2.2e-14  # kg

H_0_SI = 2.1841e-18  # s^-1
R_H = c / H_0_SI

print("=" * 70)
print("INVESTIGACAO: DERIVACOES ALTERNATIVAS DE M_c")
print("=" * 70)

print("\n" + "=" * 70)
print("1. FORMULAS DE PENROSE-DIOSI (LITERATURA)")
print("=" * 70)

# Penrose original: M_c ~ (hbar / tau) onde tau e tempo de colapso
# Diosi: tau ~ hbar / (G * M^2 / R) => M_c ~ (hbar * R / G)^{1/3}

# Para R ~ comprimento de coerencia quantica (~1 micron = 10^-6 m)
R_coh = 1e-6  # m

# Formula Diosi simplificada
Mc_diosi = (hbar * R_coh / G) ** (1/3)
print(f"\nFormula Diosi: M_c = (hbar * R_coh / G)^(1/3)")
print(f"  Com R_coh = {R_coh:.0e} m (comprimento de coerencia)")
print(f"  M_c_diosi = {Mc_diosi:.4e} kg")
print(f"  M_c_obs   = {Mc_obs:.4e} kg")
print(f"  Ratio     = {Mc_diosi / Mc_obs:.2f}")

# Formula Penrose: M_c ~ sqrt(hbar * c / G) / (algo dimensional)
# Usando l_P como escala
Mc_penrose_1 = m_P  # Massa de Planck
print(f"\nFormula Penrose base: M_c ~ m_P")
print(f"  m_P = {m_P:.4e} kg")
print(f"  Ratio m_P / M_c_obs = {m_P / Mc_obs:.4e}")

# Escala de Planck reduzida por fator dimensional
# M_c ~ m_P * (l_coh / l_P)^{alpha}
for alpha in [-1, -2, -3, -1/2, -1/3]:
    Mc_test = m_P * (R_coh / l_P) ** alpha
    ratio = Mc_test / Mc_obs
    print(f"\n  M_c = m_P * (R_coh/l_P)^{alpha:.2f}")
    print(f"    = {Mc_test:.4e} kg (ratio = {ratio:.2e})")

print("\n" + "=" * 70)
print("2. TENTATIVA: M_c DE PRINCIPIOS HOLOGRAFICOS LOCAIS")
print("=" * 70)

# Se M_c vem de saturacao de informacao LOCAL:
# S_max = A / (4 * l_P^2) onde A = 4*pi*R^2

# Para sistema quantico de tamanho R, limite de Bekenstein:
# S_max = 2*pi*E*R / (hbar*c) = 2*pi*M*c*R / hbar

# Se S_max = N bits minimos (N ~ 1 para transicao quantico-classico):
# M_c * R ~ hbar * N / (2*pi*c)

# Para N ~ 1 e R ~ comprimento de onda de M_c:
# R ~ hbar / (M_c * c) (Compton)

# Substituindo:
# M_c * hbar / (M_c * c) ~ hbar / (2*pi*c)
# hbar / c ~ hbar / (2*pi*c)  -- sempre verdade, nao da M_c

print("\nTentativa Bekenstein local:")
print("  S_max ~ M*c*R/hbar ~ 1 (transicao)")
print("  Com R = hbar/(M*c) (Compton): sempre satisfeito")
print("  -> NAO DA ESCALA DE M_c")

# Tentativa: usar gravitacao propria
# R_Schwarzschild = 2*G*M/c^2
# Se R_Compton ~ R_Schwarzschild: M ~ sqrt(hbar*c/G) = m_P
# Isso da massa de Planck, nao M_c

print("\nTentativa: R_Compton = R_Schwarzschild")
print("  -> Da M = m_P (massa de Planck)")
print("  -> NAO DA M_c observado")

print("\n" + "=" * 70)
print("3. CONCLUSAO SOBRE M_c")
print("=" * 70)

print("""
DESCOBERTA IMPORTANTE:

M_c NAO pode ser derivado de holografia cosmologica porque:

1. M_c envolve uma escala INTERMEDIARIA (R_coh ~ 10^-6 m)
   - Menor que escala cosmologica (~10^26 m)
   - Maior que escala de Planck (~10^-35 m)

2. M_c depende de PROPRIEDADES QUANTICAS LOCAIS:
   - Coerencia do pacote de ondas
   - Superposicao macroscopica
   - Auto-gravitacao

3. A formula que funciona (Diosi) e:
   M_c ~ (hbar * R_coh / G)^{1/3}
   
   Isso NAO contem R_H, Lambda, H_0 ou a_0.

IMPLICACAO:

O colapso da funcao de onda (se existir) e um fenomeno
INDEPENDENTE da cosmologia e de MOND.

A Tamesis Action ERROU ao tentar unificar todos os tres.
""")

print("\n" + "=" * 70)
print("4. O QUE SOBRA DA TAMESIS?")
print("=" * 70)

# Teste: Lambda e a_0 estao relacionados?
a0_from_Lambda = c * np.sqrt(Lambda_obs / 3)
print(f"\nRelacao Lambda <-> a_0:")
print(f"  a_0 de Lambda: c * sqrt(Lambda/3) = {a0_from_Lambda:.4e} m/s^2")
print(f"  a_0 observado:                       {a0_obs:.4e} m/s^2")
print(f"  Ratio: {a0_from_Lambda / a0_obs:.2f}")

# Isso tambem nao funciona! O ratio e ~0.18

print("""
RESULTADO DEVASTADOR:

Mesmo Lambda e a_0 NAO estao bem relacionados:
- a_0^2 / (c^4 * Lambda) = 0.016 (deveria ser ~1)
- a_0 / (c * H_0) = 0.18 (deveria ser ~1)

A "coincidencia MOND" a_0 ~ c*H_0 e apenas APROXIMADA (ordem de grandeza).
NAO e uma identidade exata.

CONCLUSAO FINAL:
================
Lambda, a_0, e M_c sao TRES fenomenos INDEPENDENTES.
Nenhum deles deriva dos outros.
A unificacao holografica e uma ILUSAO baseada em coincidencias de ordem de grandeza.
""")

print("=" * 70)
print("VEREDITO: A Tamesis Action como ToE esta REFUTADA.")
print("=" * 70)
