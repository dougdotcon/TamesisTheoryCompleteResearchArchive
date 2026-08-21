#!/usr/bin/env python3
"""DISC-CORE-NUMERICS-001 / frente mc-internal-consistency.

Adjudicacao de mesa da consistencia interna do valor congelado
M_c = 5.292674126388712e-16 kg (contrato tamesis-mc-v1.0).

Deterministico: nenhum RNG, nenhuma dependencia externa alem de stdlib.
Criterios de decisao fixados a priori em ../METHODOLOGY_NOTE.md.

Saida: impressa (salva em compute_mc_consistency.log pelo runner) e
results.json neste diretorio.
"""

import json
import math
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Constantes congeladas do contrato (lidas de config/tamesis_mc_v1.yaml,
# linhas 7-24 — valores INTERNOS do nucleo, nao referencia externa)
# ---------------------------------------------------------------------------
CONTRACT = {
    "G": 6.67430e-11,            # m^3 kg^-1 s^-2
    "hbar": 1.054571817e-34,     # J s
    "c": 299792458.0,            # m s^-1
    "H0_km_s_Mpc": 70.0,
    "H0_si": 2.268545502662652e-18,   # s^-1 (si_value congelado)
    "Mc_frozen": 5.292674126388712e-16,  # kg (derived_quantities.Mc_kg)
    "phase_space_root": 8,
}

# ---------------------------------------------------------------------------
# Referencias externas com proveniencia (fetch 2026-08-21, ver nota):
#   G, hbar, c, m_P: NIST CODATA 2022 (physics.nist.gov/cgi-bin/cuu/Value?...)
#   au exato: IAU 2012 Res. B2; pc = 648000/pi au: IAU 2015 Res. B2
# ---------------------------------------------------------------------------
CODATA = {
    "G": 6.67430e-11,
    "G_rel_unc": 2.2e-5,
    "hbar": 1.054571817e-34,     # exato (definicao SI 2019, truncado CODATA)
    "c": 299792458.0,            # exato
    "m_P": 2.176434e-8,          # kg, CODATA 2022, u_r = 1.1e-5
    "m_P_rel_unc": 1.1e-5,
    "amu": 1.66053906660e-27,    # kg (valor usado pelo proprio contrato,
                                 # mc_model.py:106; coincide com CODATA 2018)
}
AU_M = 149597870700.0            # m, exato (IAU 2012 B2)
PC_M = (648000.0 / math.pi) * AU_M   # m, exato (IAU 2015 B2)
MPC_M = PC_M * 1.0e6

# Valores internos do nucleo inventariados (arquivo:linha em RESULTS_SUMMARY)
OMEGA = 117.038                  # 01_Foundation/README.md:17,46
MC_CLAIMS = {
    "frozen_contract": 5.292674126388712e-16,   # tamesis_mc_v1.yaml:63
    "killer_prediction_2p2e14": 2.2e-14,        # Killer_Prediction/interference_sim.py:10 etc.
    "paper08_order_1e14": 1.0e-14,              # 08_.../paper.html:410 (ordem de grandeza)
    "foundation_omega4_claim": 1.16e-16,        # 01_Foundation/README.md:97
}

results = {}


def planck(G, hbar, c):
    l_P = math.sqrt(hbar * G / c**3)
    m_P = math.sqrt(hbar * c / G)
    a_P = c**2 / l_P
    return l_P, m_P, a_P


def mc_root8(G, hbar, c, H0_si, two_pi_branch=False):
    _, m_P, a_P = planck(G, hbar, c)
    a0 = c * H0_si
    if two_pi_branch:
        a0 /= 2.0 * math.pi
    return m_P * (a0 / a_P) ** 0.125


def h0_si(h0_km_s_mpc):
    return h0_km_s_mpc * 1000.0 / MPC_M


print("=" * 72)
print("A1 - VERIFICACAO ARITMETICA DO CONTRATO (constantes congeladas)")
print("=" * 72)

mc_a1 = mc_root8(CONTRACT["G"], CONTRACT["hbar"], CONTRACT["c"], CONTRACT["H0_si"])
rel_a1 = abs(mc_a1 - CONTRACT["Mc_frozen"]) / CONTRACT["Mc_frozen"]
h0_si_recalc = h0_si(CONTRACT["H0_km_s_Mpc"])
rel_h0 = abs(h0_si_recalc - CONTRACT["H0_si"]) / CONTRACT["H0_si"]
l_P, m_P_contract, a_P = planck(CONTRACT["G"], CONTRACT["hbar"], CONTRACT["c"])
m_P_dev_vs_codata = abs(m_P_contract - CODATA["m_P"]) / CODATA["m_P"]

print(f"l_P (contrato)                    = {l_P:.12e} m")
print(f"m_P (contrato, sqrt(hbar c/G))    = {m_P_contract:.12e} kg")
print(f"m_P CODATA 2022 tabulado          = {CODATA['m_P']:.6e} kg")
print(f"  desvio relativo                 = {m_P_dev_vs_codata:.3e}  (tol sanidade 2.2e-5)")
print(f"a_P = c^2/l_P                     = {a_P:.12e} m/s^2")
print(f"a0 = c*H0_si (ramo do contrato)   = {CONTRACT['c']*CONTRACT['H0_si']:.12e} m/s^2")
print(f"M_c recomputado                   = {mc_a1:.15e} kg")
print(f"M_c congelado                     = {CONTRACT['Mc_frozen']:.15e} kg")
print(f"  desvio relativo                 = {rel_a1:.3e}  (criterio C1: <= 1e-9)")
print(f"H0 70 km/s/Mpc -> SI (Mpc IAU)    = {h0_si_recalc:.15e} s^-1")
print(f"H0 si_value congelado             = {CONTRACT['H0_si']:.15e} s^-1")
print(f"  desvio relativo                 = {rel_h0:.3e}  (criterio C1: <= 1e-6)")

c1_pass = (rel_a1 <= 1e-9) and (rel_h0 <= 1e-6)
print(f"C1 (aritmetica do contrato): {'APROVADO' if c1_pass else 'REPROVADO'}")

results["A1"] = {
    "mc_recomputed_kg": mc_a1,
    "mc_frozen_kg": CONTRACT["Mc_frozen"],
    "rel_dev_mc": rel_a1,
    "h0_si_recomputed": h0_si_recalc,
    "h0_si_frozen": CONTRACT["H0_si"],
    "rel_dev_h0": rel_h0,
    "m_P_contract": m_P_contract,
    "m_P_codata": CODATA["m_P"],
    "m_P_rel_dev": m_P_dev_vs_codata,
    "a_P": a_P,
    "C1_pass": c1_pass,
}

print()
print("=" * 72)
print("A2 - OS DOIS RAMOS DE a0 (H0 = 70 km/s/Mpc, constantes do contrato)")
print("=" * 72)

mc_cH0 = mc_a1
mc_cH0_2pi = mc_root8(CONTRACT["G"], CONTRACT["hbar"], CONTRACT["c"],
                      CONTRACT["H0_si"], two_pi_branch=True)
shift = (2.0 * math.pi) ** 0.125
a0_A = CONTRACT["c"] * CONTRACT["H0_si"] / (2 * math.pi)
a0_B = CONTRACT["c"] * CONTRACT["H0_si"]

print(f"a0_B = cH0        (ramo do contrato; FALSIFICADO por SPARC-002) = {a0_B:.6e} m/s^2")
print(f"a0_A = cH0/(2pi)  (ramo SOBREVIVENTE em SPARC-002)              = {a0_A:.6e} m/s^2")
print(f"M_c[a0=cH0]      = {mc_cH0:.15e} kg   (= valor congelado)")
print(f"M_c[a0=cH0/2pi]  = {mc_cH0_2pi:.15e} kg")
print(f"fator de deslocamento (2pi)^(1/8) = {shift:.15f}")
print(f"razao M_c_congelado / M_c_ramo_sobrevivente = {mc_cH0/mc_cH0_2pi:.15f}")
print(f"excesso percentual do valor congelado sobre o ramo sobrevivente = "
      f"{(mc_cH0/mc_cH0_2pi - 1)*100:.4f} %")

# C2: ramo do contrato e o falsificado; diferenca induzida > 1%?
c2_diff_pct = (mc_cH0 / mc_cH0_2pi - 1) * 100
c2_pass = c2_diff_pct <= 1.0  # o ramo usado NAO e o sobrevivente, entao so passa se a diferenca fosse <=1%
print(f"C2 (coerencia com ramo sobrevivente): "
      f"{'APROVADO' if c2_pass else 'REPROVADO'} "
      f"(contrato usa a0=cH0, ramo falsificado; diferenca {c2_diff_pct:.2f}% > 1%)"
      if not c2_pass else "C2: APROVADO")

results["A2"] = {
    "a0_contract_branch_cH0": a0_B,
    "a0_surviving_branch_cH0_over_2pi": a0_A,
    "mc_cH0": mc_cH0,
    "mc_cH0_over_2pi": mc_cH0_2pi,
    "shift_factor_2pi_pow_1_8": shift,
    "frozen_over_surviving_ratio": mc_cH0 / mc_cH0_2pi,
    "excess_percent": c2_diff_pct,
    "sparc002_verdict": "H_A_SURVIVES_H_B_FALSIFIED (result_primary.json)",
    "C2_pass": c2_pass,
}

print()
print("=" * 72)
print("A3 - SENSIBILIDADE A H0 (ambos os ramos)")
print("=" * 72)

sens = {}
for h0 in (67.4, 70.0, 73.0):
    hsi = h0_si(h0)
    m_b = mc_root8(CONTRACT["G"], CONTRACT["hbar"], CONTRACT["c"], hsi)
    m_a = mc_root8(CONTRACT["G"], CONTRACT["hbar"], CONTRACT["c"], hsi, True)
    sens[str(h0)] = {"mc_cH0": m_b, "mc_cH0_over_2pi": m_a}
    print(f"H0 = {h0:5.1f}: M_c[cH0] = {m_b:.6e} kg "
          f"({(m_b/mc_cH0-1)*100:+.3f}% vs congelado) | "
          f"M_c[cH0/2pi] = {m_a:.6e} kg")
print("Nota: M_c ~ H0^(1/8); a variacao 67.4-73 muda M_c em ~1%, "
      "muito menor que o fator (2pi)^(1/8) de ~26% entre ramos.")
results["A3"] = sens

print()
print("=" * 72)
print("A4 - OUTRAS DERIVACOES DE M_c NO NUCLEO")
print("=" * 72)

# (a) M_P * Omega^-4
mc_omega = CODATA["m_P"] * OMEGA ** (-4)
dev_omega = abs(mc_omega - MC_CLAIMS["foundation_omega4_claim"]) / MC_CLAIMS["foundation_omega4_claim"]
print(f"(a) M_P * Omega^-4, Omega = {OMEGA} (01_Foundation/README.md:97)")
print(f"    recomputado = {mc_omega:.6e} kg | alegado = 1.16e-16 kg | "
      f"desvio = {dev_omega*100:.3f}%  -> {'fiel' if dev_omega <= 0.05 else 'infiel'} (tol 5%)")

# (b) (hbar^2/(G c))^(1/4) -- rascunho PRL / paper 08
# dimensoes: hbar = kg m^2 s^-1 ; G = m^3 kg^-1 s^-2 ; c = m s^-1
# hbar^2/(Gc): kg exponent = 2-(-1) = 3 ; m = 4-3-1 = 0 ; s = -2-(-2)-(-1) = 1
# => (kg^3 s)^(1/4) = kg^(3/4) s^(1/4)  (NAO tem dimensao de massa)
val_b = (CODATA["hbar"] ** 2 / (CODATA["G"] * CODATA["c"])) ** 0.25
dev_b = abs(val_b - 2.2e-14) / 2.2e-14
print(f"(b) (hbar^2/(Gc))^(1/4) (08_.../prl_submission.html:239, paper.html:410)")
print(f"    dimensao: kg^(3/4) s^(1/4) -> DIMENSIONALMENTE INCONSISTENTE (nao e massa)")
print(f"    valor numerico da expressao como escrita (SI) = {val_b:.6e}")
print(f"    alegado ~ 2.2e-14 kg | razao alegado/calculado = {2.2e-14/val_b:.1f}x")
print(f"    -> infiel: a expressao escrita NAO reproduz 2.2e-14 (desvio {dev_b*100:.0f}%)")

# (c) (hbar * m_atom * c^3 / (4G))^(1/3) -- 01_Mc_Derivation/index.html:255
# dimensoes: hbar m c^3 / G = (kg m^2 s^-1)(kg)(m^3 s^-3)/(m^3 kg^-1 s^-2)
#   kg: 1+1-(-1)=3 ; m: 2+3-3=2 ; s: -1-3-(-2)=-2  => (kg^3 m^2 s^-2)^(1/3)
val_c_1u = (CODATA["hbar"] * CODATA["amu"] * CODATA["c"] ** 3 / (4 * CODATA["G"])) ** (1.0 / 3.0)
# m_atom necessario para bater 2.2e-14:
m_atom_needed = (2.2e-14) ** 3 * 4 * CODATA["G"] / (CODATA["hbar"] * CODATA["c"] ** 3)
amu_check = 2.2e-14 / CODATA["amu"]
print(f"(c) (hbar*m_atom*c^3/(4G))^(1/3) (01_Mc_Derivation/index.html:255)")
print(f"    dimensao: kg m^(2/3) s^(-2/3) -> DIMENSIONALMENTE INCONSISTENTE (nao e massa)")
print(f"    valor com m_atom = 1 u = {val_c_1u:.6e} (unidades mistas)")
print(f"    m_atom necessario p/ reproduzir 2.2e-14 = {m_atom_needed:.3e} kg "
      f"(= {m_atom_needed/CODATA['amu']:.2e} u; nenhum atomo fisico)")
print(f"    checagem lateral: 2.2e-14 kg = {amu_check:.3e} u, mas o arquivo alega "
      f"'~320 million amu' (3.2e8 u) -> discrepancia interna de {amu_check/3.2e8:.1e}x")

results["A4"] = {
    "omega4": {"recomputed": mc_omega, "claimed": 1.16e-16, "rel_dev": dev_omega,
               "faithful": dev_omega <= 0.05},
    "prl_hbar2_Gc_quarter": {
        "dimension": "kg^(3/4) s^(1/4) - not a mass",
        "numeric_value_as_written": val_b,
        "claimed": 2.2e-14,
        "claimed_over_computed": 2.2e-14 / val_b,
        "faithful": False,
    },
    "mc_derivation_cubic": {
        "dimension": "kg m^(2/3) s^(-2/3) - not a mass",
        "value_with_m_atom_1u": val_c_1u,
        "m_atom_needed_for_2p2e14_kg": m_atom_needed,
        "claimed_amu_in_file": 3.2e8,
        "actual_amu_of_2p2e14": amu_check,
        "faithful": False,
    },
}

print()
print("=" * 72)
print("A5 - MATRIZ DE RAZOES ENTRE OS VALORES DE M_c DO NUCLEO")
print("=" * 72)

vals = dict(MC_CLAIMS)
vals["surviving_branch_cH0_over_2pi"] = mc_cH0_2pi
keys = list(vals.keys())
ratio_matrix = {}
max_ratio = 1.0
print(f"{'':38s}" + "".join(f"{k[:14]:>16s}" for k in keys))
for ki in keys:
    row = {}
    line = f"{ki:38s}"
    for kj in keys:
        r = vals[ki] / vals[kj]
        row[kj] = r
        big = max(r, 1 / r)
        if big > max_ratio:
            max_ratio = big
        line += f"{r:16.3f}"
    ratio_matrix[ki] = row
    print(line)
print(f"\nmaior razao par-a-par = {max_ratio:.1f}x "
      f"({math.log10(max_ratio):.2f} ordens de grandeza)")

# C3: todos os pares dentro de fator 2? algum par > fator 10?
pairs_over_10 = []
pairs_over_2 = []
for i, ki in enumerate(keys):
    for kj in keys[i + 1:]:
        big = max(vals[ki] / vals[kj], vals[kj] / vals[ki])
        if big > 10:
            pairs_over_10.append((ki, kj, big))
        elif big > 2:
            pairs_over_2.append((ki, kj, big))
c3_pass = len(pairs_over_10) == 0 and len(pairs_over_2) == 0
print(f"pares com razao > 10x: {len(pairs_over_10)}")
for p in pairs_over_10:
    print(f"  {p[0]} vs {p[1]}: {p[2]:.1f}x")
print(f"pares com razao entre 2x e 10x: {len(pairs_over_2)}")
for p in pairs_over_2:
    print(f"  {p[0]} vs {p[1]}: {p[2]:.1f}x")
print(f"C3 (coerencia entre formulacoes): "
      f"{'APROVADO' if c3_pass else 'REPROVADO' if pairs_over_10 else 'TENSAO'}")

results["A5"] = {
    "values": vals,
    "ratio_matrix": ratio_matrix,
    "max_pairwise_ratio": max_ratio,
    "pairs_over_10x": [[a, b, r] for a, b, r in pairs_over_10],
    "pairs_2x_to_10x": [[a, b, r] for a, b, r in pairs_over_2],
    "C3_pass": c3_pass,
}

print()
print("=" * 72)
print("VEREDITO (criterios de METHODOLOGY_NOTE.md)")
print("=" * 72)
verdict = "CONSISTENTE_COMO_FORMULADO" if (c1_pass and c2_pass and c3_pass) \
    else "INCONSISTENTE_COMO_FORMULADO"
print(f"C1 aritmetica do contrato      : {'APROVADO' if c1_pass else 'REPROVADO'}")
print(f"C2 ramo a0 sobrevivente        : {'APROVADO' if c2_pass else 'REPROVADO'}")
print(f"C3 coerencia entre formulacoes : {'APROVADO' if c3_pass else 'REPROVADO'}")
print(f"VEREDITO GLOBAL: {verdict}")

results["verdict"] = {
    "C1_contract_arithmetic": c1_pass,
    "C2_surviving_a0_branch": c2_pass,
    "C3_cross_formulation_coherence": c3_pass,
    "global": verdict,
}

with open(os.path.join(OUT_DIR, "results.json"), "w") as f:
    json.dump(results, f, indent=2)
print(f"\nresults.json gravado em {os.path.join(OUT_DIR, 'results.json')}")
