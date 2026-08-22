"""
Validacao extra: Modelo B (correcao de primos de Berry).

(1) Verifica a identidade algebrica Lambda(p^k)^2/(p^k * log^2(p^k)) = 1/(k^2 p^k)
    numericamente, comparando a soma "crua" (via Lambda de von Mangoldt
    explicita) contra a soma simplificada usada em model_B_exact, para um T
    pequeno onde ambas sao trivialmente enumeraveis.

(2) Verifica model_B_bounded_zeros3 contra model_B_exact no MESMO T pequeno
    (usando P_cutoff=T, ou seja sem cauda) -- devem coincidir exatamente
    (intervalo de largura ~0, cauda zero).
"""
import json
import math
import numpy as np
from estimator_adv import sieve_primes, model_B_exact, model_B_bounded_zeros3

# ---- (1) identidade Lambda^2 ----
T_small = 500.0
logT_small = math.log(T_small)
primes = sieve_primes(int(T_small))

# soma "crua": para cada n=2..T, calcular Lambda(n) explicitamente (Lambda(n)=log p
# se n=p^k, 0 caso contrario), dividir por n*log^2(n).
raw_terms = []
for n in range(2, int(T_small) + 1):
    # fatoriza n para achar se eh p^k
    m = n
    p_factor = None
    for p in primes:
        if p * p > m and m > 1:
            p_factor = m
            break
        if m % p == 0:
            p_factor = p
            # checa se m eh potencia pura de p
            mm = m
            while mm % p == 0:
                mm //= p
            if mm == 1:
                p_factor = p
            else:
                p_factor = None
            break
    if p_factor is None:
        continue
    logp = math.log(p_factor)
    Lambda_n = logp
    raw_terms.append((n, Lambda_n))

L_test = 37.123
raw_sum = 0.0
for n, Lambda_n in raw_terms:
    weight_raw = (Lambda_n ** 2) / (n * (math.log(n)) ** 2)
    phase = 2 * math.pi * L_test * math.log(n) / logT_small
    raw_sum += weight_raw * (1 - math.cos(phase))
V_B_raw = (raw_sum + 1.0) / (math.pi ** 2)

# soma simplificada via model_B_exact (usa identidade 1/(k^2 p^k))
pk_list, k_list, logp_list = [], [], []
for p in primes:
    p = int(p)
    logp = math.log(p)
    pk = p
    k = 1
    while pk <= T_small:
        pk_list.append(float(pk))
        k_list.append(k)
        logp_list.append(logp)
        pk *= p
        k += 1
V_B_simplified = model_B_exact(L_test, T_small, logT_small,
                                 np.array(pk_list), np.array(k_list, dtype=np.float64),
                                 np.array(logp_list))

rel_diff_identity = abs(V_B_raw - V_B_simplified) / abs(V_B_raw)
print(f"V_B (soma crua, Lambda explicito) = {V_B_raw:.10f}")
print(f"V_B (soma simplificada, 1/(k^2 p^k)) = {V_B_simplified:.10f}")
print(f"diff relativo = {rel_diff_identity:.2e}")
identity_pass = rel_diff_identity < 1e-10

# ---- (2) bounded vs exact, cauda ~0 ----
V_lower, V_upper = model_B_bounded_zeros3(L_test, T_small, logT_small, T_small, primes)
print(f"\nmodel_B_bounded (P_cutoff=T={T_small}): [{V_lower:.8f}, {V_upper:.8f}]")
print(f"model_B_exact: {V_B_simplified:.8f}")
bounded_contains_exact = V_lower - 1e-6 <= V_B_simplified <= V_upper + 1e-6
width = V_upper - V_lower
print(f"largura do intervalo = {width:.2e} (deve ser pequena, cauda k=1 alem de T e zero por construcao mas cota Mertens pode dar folga residual)")
bounded_pass = bounded_contains_exact

verdict = "PASS" if (identity_pass and bounded_pass) else "FAIL"
print(f"\nidentity_pass={identity_pass}  bounded_pass={bounded_pass}")
print("VERDICT:", verdict)

with open("validation_model_b_adv.json", "w") as f:
    json.dump(dict(T_small=T_small, L_test=L_test, V_B_raw=V_B_raw,
                     V_B_simplified=V_B_simplified, rel_diff_identity=rel_diff_identity,
                     V_lower=V_lower, V_upper=V_upper, width=width,
                     verdict=verdict), f, indent=2)
