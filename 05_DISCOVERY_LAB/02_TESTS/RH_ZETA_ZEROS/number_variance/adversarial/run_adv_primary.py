"""
Analise primaria ADVERSARIAL: computa V_hat(L), z_A, z_B na grade COMPLETA de
DESIGN.json para zeros1 e zeros3, usando o estimador e os modelos construidos
do zero (estimator_adv.py), sobre dado real (load_data_adv.py). Primeira vez
que dado real e usado nesta reproducao -- todas as validacoes sinteticas ja
passaram antes deste ponto.

zeros4.txt NAO e tocado.
"""
import json
import time
import numpy as np
import math

from estimator_adv import (block_number_variance, model_A, sieve_primes,
                             model_B_exact, model_B_bounded_zeros3)
from load_data_adv import load_zeros1, load_zeros3

t_start = time.time()

# grade travada (copiada do DESIGN.json, ja lido no plano -- design, nao
# resultado)
zeros1_grid = [
    (1, 11.22418720159839, 2227), (1.5, 16.836280802397585, 1484),
    (2, 22.44837440319678, 1113), (3, 33.67256160479517, 742),
    (4, 44.89674880639356, 556), (6, 67.34512320959034, 371),
    (8, 89.79349761278712, 278), (12, 134.69024641918068, 185),
    (16, 179.58699522557424, 139), (24, 269.38049283836136, 92),
    (32, 359.1739904511485, 69), (48, 538.7609856767227, 46),
    (64, 718.347980902297, 34), (96, 1077.5219713534455, 23),
    (128, 1436.695961804594, 17), (192, 2155.043942706891, 11),
]
zeros3_grid = [
    (1, 26.312958680598655, 95), (1.5, 39.46943802089798, 63),
    (2, 52.62591736119731, 47), (3, 78.93887604179596, 31),
    (4, 105.25183472239462, 23), (6, 157.87775208359193, 15),
    (8, 210.50366944478924, 11),
]

T_zeros1 = 74920.827498994
logT_zeros1 = 11.22418720159839
T_zeros3 = 267653395647.0
logT_zeros3 = 26.312958680598655
P_cutoff_zeros3 = 200000000

PRIMARY_MULT = {"zeros1": 192, "zeros3": 8}
SECONDARY_MULT = {"zeros1": 128, "zeros3": 6}

results = {"zeros1": {"grid": []}, "zeros3": {"grid": []}}

# ---------------- zeros1 ----------------
print("=== Carregando zeros1.txt ===")
gammas1, x1 = load_zeros1()
print(f"n={x1.size}  x_range={x1.max()-x1.min():.6f}")

print("=== Crivo de primos ate T_zeros1 ===")
primes1 = sieve_primes(int(math.ceil(T_zeros1)))
print(f"n_primes = {primes1.size}")

# prime powers p^k <= T_zeros1 (exato, dataset pequeno o bastante)
pk_list, k_list, logp_list = [], [], []
n_pp = 0
for p in primes1:
    p = int(p)
    logp = math.log(p)
    pk = p
    k = 1
    while pk <= T_zeros1:
        pk_list.append(float(pk)); k_list.append(k); logp_list.append(logp)
        n_pp += 1
        if pk > T_zeros1 / p:
            break
        pk *= p
        k += 1
pk_arr1 = np.array(pk_list, dtype=np.float64)
k_arr1 = np.array(k_list, dtype=np.float64)
logp_arr1 = np.array(logp_list, dtype=np.float64)
print(f"n_prime_powers (zeros1) = {n_pp}  (pre-registro cita 7.486)")

for mult, L, B in zeros1_grid:
    res = block_number_variance(x1, L, B)
    V_hat, SE, n_used = res["V_hat"], res["SE"], res["n_blocks_used"]
    VA = float(model_A(L))
    VB = float(model_B_exact(L, T_zeros1, logT_zeros1, pk_arr1, k_arr1, logp_arr1))
    z_A = (V_hat - VA) / SE if SE > 0 else float("nan")
    z_B = (V_hat - VB) / SE if SE > 0 else float("nan")
    entry = dict(mult=mult, L=L, B_design=B, B_used=n_used, V_hat=V_hat, SE=SE,
                  model_A=VA, z_A=z_A, model_B=VB, z_B=z_B,
                  is_primary=(mult == PRIMARY_MULT["zeros1"]),
                  is_secondary=(mult == SECONDARY_MULT["zeros1"]))
    results["zeros1"]["grid"].append(entry)
    tag = " <== PRIMARIO" if entry["is_primary"] else (" <== secundario" if entry["is_secondary"] else "")
    print(f"  mult={mult:<6} L={L:10.3f} B={n_used:3d}  V_hat={V_hat:.4f} SE={SE:.4f}  "
          f"A={VA:.4f} z_A={z_A:9.2f}  B={VB:.4f} z_B={z_B:8.2f}{tag}")

print(f"\nzeros1 total elapsed: {time.time()-t_start:.1f}s")

# ---------------- zeros3 ----------------
t1 = time.time()
print("\n=== Carregando zeros3.txt ===")
offsets3, base3, Nprime_base3, x3 = load_zeros3()
print(f"n={x3.size}  x_range={x3.max()-x3.min():.6f}")

print("=== Crivo de primos ate P_cutoff (200M) ===")
primes3 = sieve_primes(P_cutoff_zeros3)
print(f"n_primes = {primes3.size}  (pre-registro cita 11.078.937)")

for mult, L, B in zeros3_grid:
    res = block_number_variance(x3, L, B)
    V_hat, SE, n_used = res["V_hat"], res["SE"], res["n_blocks_used"]
    VA = float(model_A(L))
    V_lower, V_upper = model_B_bounded_zeros3(L, T_zeros3, logT_zeros3, P_cutoff_zeros3, primes3)
    # alvo B = borda mais proxima do intervalo (Secao 7 do pre-registro)
    if V_lower <= V_hat <= V_upper:
        VB_target = V_hat
        z_B = 0.0
    elif V_hat < V_lower:
        VB_target = V_lower
        z_B = (V_hat - V_lower) / SE if SE > 0 else float("nan")
    else:
        VB_target = V_upper
        z_B = (V_hat - V_upper) / SE if SE > 0 else float("nan")
    z_A = (V_hat - VA) / SE if SE > 0 else float("nan")
    entry = dict(mult=mult, L=L, B_design=B, B_used=n_used, V_hat=V_hat, SE=SE,
                  model_A=VA, z_A=z_A, model_B_lower=V_lower, model_B_upper=V_upper,
                  z_B=z_B, is_primary=(mult == PRIMARY_MULT["zeros3"]),
                  is_secondary=(mult == SECONDARY_MULT["zeros3"]))
    results["zeros3"]["grid"].append(entry)
    tag = " <== PRIMARIO" if entry["is_primary"] else (" <== secundario" if entry["is_secondary"] else "")
    print(f"  mult={mult:<6} L={L:10.3f} B={n_used:3d}  V_hat={V_hat:.4f} SE={SE:.4f}  "
          f"A={VA:.4f} z_A={z_A:9.2f}  B=[{V_lower:.4f},{V_upper:.4f}] z_B={z_B:8.2f}{tag}")

print(f"\nzeros3 total elapsed: {time.time()-t1:.1f}s")
print(f"\nTOTAL elapsed: {time.time()-t_start:.1f}s")

# ---------------- resumo pontos decisivos primarios ----------------
z1_primary = next(e for e in results["zeros1"]["grid"] if e["is_primary"])
z3_primary = next(e for e in results["zeros3"]["grid"] if e["is_primary"])

print("\n" + "=" * 70)
print("PONTOS DECISIVOS PRIMARIOS (adversarial, independente)")
print("=" * 70)
print(f"zeros1  L={z1_primary['L']:.2f}  V_hat={z1_primary['V_hat']:.4f}  SE={z1_primary['SE']:.4f}  "
      f"z_A={z1_primary['z_A']:.2f}  z_B={z1_primary['z_B']:.2f}")
print(f"zeros3  L={z3_primary['L']:.2f}  V_hat={z3_primary['V_hat']:.4f}  SE={z3_primary['SE']:.4f}  "
      f"z_A={z3_primary['z_A']:.2f}  z_B={z3_primary['z_B']:.2f}")

# regra ternaria travada (Secao 7 do pre-registro)
def classify(z1p, z3p):
    reject_z = 3.0
    accept_z = 2.0
    berry = (abs(z1p["z_A"]) >= reject_z and abs(z3p["z_A"]) >= reject_z and
             abs(z1p["z_B"]) < accept_z and abs(z3p["z_B"]) < accept_z)
    gue = (abs(z1p["z_B"]) >= reject_z and abs(z3p["z_B"]) >= reject_z and
           abs(z1p["z_A"]) < accept_z and abs(z3p["z_A"]) < accept_z)
    if berry:
        return "BERRY_FAVORED", None
    if gue:
        return "GUE_FAVORED", None
    both_rejected = (abs(z1p["z_A"]) >= reject_z and abs(z3p["z_A"]) >= reject_z and
                      abs(z1p["z_B"]) >= reject_z and abs(z3p["z_B"]) >= reject_z)
    if both_rejected:
        return "INCONCLUSIVE", "NEITHER_MODEL"
    underpowered = (abs(z1p["z_A"]) < reject_z or abs(z3p["z_A"]) < reject_z or
                      abs(z1p["z_B"]) < reject_z or abs(z3p["z_B"]) < reject_z) and not both_rejected
    # PARTIAL_DISAGREEMENT: datasets apontam em direcoes diferentes
    z1_berry_like = abs(z1p["z_A"]) >= reject_z and abs(z1p["z_B"]) < accept_z
    z3_berry_like = abs(z3p["z_A"]) >= reject_z and abs(z3p["z_B"]) < accept_z
    z1_gue_like = abs(z1p["z_B"]) >= reject_z and abs(z1p["z_A"]) < accept_z
    z3_gue_like = abs(z3p["z_B"]) >= reject_z and abs(z3p["z_A"]) < accept_z
    if (z1_berry_like and z3_gue_like) or (z1_gue_like and z3_berry_like):
        return "INCONCLUSIVE", "PARTIAL_DISAGREEMENT"
    return "INCONCLUSIVE", "UNDERPOWERED_OR_MIXED"


verdict, subcase = classify(z1_primary, z3_primary)
print(f"\nVEREDITO TERNARIO (regra travada Secao 7): {verdict}" + (f" / {subcase}" if subcase else ""))

# S1: checagem de sinal primario vs secundario
z1_secondary = next(e for e in results["zeros1"]["grid"] if e["is_secondary"])
z3_secondary = next(e for e in results["zeros3"]["grid"] if e["is_secondary"])
s1_zeros1 = (np.sign(z1_primary["z_A"]) == np.sign(z1_secondary["z_A"]))
s1_zeros3 = (np.sign(z3_primary["z_A"]) == np.sign(z3_secondary["z_A"]))
print(f"\nS1 (sinal z_A primario==secundario): zeros1={s1_zeros1}  zeros3={s1_zeros3}")

# 23/23: Modelo B mais perto que Modelo A em distancia absoluta, em toda a grade
closer_count = 0
total_count = 0
for e in results["zeros1"]["grid"]:
    total_count += 1
    dA = abs(e["V_hat"] - e["model_A"])
    dB = abs(e["V_hat"] - e["model_B"])
    if dB < dA:
        closer_count += 1
for e in results["zeros3"]["grid"]:
    total_count += 1
    dA = abs(e["V_hat"] - e["model_A"])
    Bt = e["model_B_lower"] if e["V_hat"] < e["model_B_lower"] else (
        e["model_B_upper"] if e["V_hat"] > e["model_B_upper"] else e["V_hat"])
    dB = abs(e["V_hat"] - Bt)
    if dB < dA:
        closer_count += 1
print(f"\nModelo B mais perto que Modelo A (distancia absoluta) em {closer_count}/{total_count} pontos "
      f"(pre-registro cita 23/23)")

results["summary"] = dict(
    z1_primary=z1_primary, z3_primary=z3_primary,
    verdict=verdict, subcase=subcase,
    s1_zeros1=bool(s1_zeros1), s1_zeros3=bool(s1_zeros3),
    closer_to_B_count=closer_count, total_grid_points=total_count,
    n_primes_zeros1=int(primes1.size), n_prime_powers_zeros1=n_pp,
    n_primes_zeros3_sieve=int(primes3.size),
    total_wall_time_s=time.time() - t_start,
)

with open("adv_primary_result.json", "w") as f:
    json.dump(results, f, indent=2, default=lambda o: float(o) if isinstance(o, (np.floating,)) else o)

print("\nSalvo em adv_primary_result.json")
