#!/usr/bin/env python3
"""
Adjudicacao de mesa - constant_fits (DISC-CORE-NUMERICS-001, frente constant-fit-adjudication)

Criterios pre-declarados em METHODOLOGY_NOTE.md (fixados ANTES dos fetches).
Valores de referencia: PROVENANCE.md (fetch 2026-08-21) - nunca de memoria.

Roda em foreground; saida: adjudication_results.json + adjudication.log (via tee no shell).
"""

import json
import math
from fractions import Fraction

results = {"date": "2026-08-21", "front": "constant-fit-adjudication",
           "line": "DISC-CORE-NUMERICS-001", "subclaims": {}}

# =====================================================================
# (a) sin^2 theta_W = 3/13, nucleo: "CONFIRMED, 0.19% error"
# =====================================================================
claim = float(Fraction(3, 13))          # 0.230769230769...
schemes = {
    # nome: (valor PDG 2025, incerteza) - PROVENANCE.md itens 1a/1b
    "MS-bar (s^2_Z(M_Z))":        (0.23122, 0.00006),
    "on-shell (s^2_W)":           (0.22342, 0.00009),
    "efetivo leptonico (s^2_l)":  (0.23154, 0.00006),
}
a = {"claim": "sin^2 theta_W = 3/13", "claim_value": claim, "schemes": {}}
for name, (v, u) in schemes.items():
    delta = claim - v
    a["schemes"][name] = {
        "pdg_value": v, "pdg_unc": u,
        "delta": delta,
        "delta_percent": 100 * abs(delta) / v,
        "sigma": abs(delta) / u,
    }
# esquema mais caridoso = menor sigma
charit = min(a["schemes"], key=lambda k: a["schemes"][k]["sigma"])
a["most_charitable_scheme"] = charit
a["most_charitable_sigma"] = a["schemes"][charit]["sigma"]
# checagem aritmetica do rotulo interno "0.19%" (contra o MS-bar que o nucleo cita)
a["internal_percent_label"] = 0.19
a["internal_percent_recomputed_msbar"] = a["schemes"]["MS-bar (s^2_Z(M_Z))"]["delta_percent"]
# checagem on-shell tree-level a partir das massas PDG 2025 (2a rota, diagnostico)
mW, mZ = 80.3692, 91.1880
a["onshell_from_masses_1_minus_mW2_over_mZ2"] = 1 - (mW / mZ) ** 2
# criterio pre-declarado: consistente se sigma <= 2 no esquema mais caridoso
a["verdict_consistency"] = ("consistente" if a["most_charitable_sigma"] <= 2
                            else "inconsistente como formulado")
a["verdict_identifiability"] = (
    "nao-identificavel (tuning): razao selecionada por varredura contra o alvo "
    "0.23122 (electroweak/README.md:25 'scanned ... to match the observed CODATA "
    "value'; torsion_angle.py:15 target_s2w=0.23122); esquema de comparacao "
    "tambem escolhido a posteriori")
results["subclaims"]["a_sin2thetaW"] = a

# =====================================================================
# (b) alpha^-1 = Omega^1.03 (nucleo: beta=1.033, "0.003% error")
# =====================================================================
OMEGA = 117.038
ALPHA_INV_CODATA = 137.035999177   # +/- 0.000000021 (CODATA 2022, NIST)
ALPHA_INV_UNC = 0.000000021
b = {"claim": "alpha^-1 = Omega^beta, Omega=117.038, beta~1.03(3)",
     "codata_alpha_inv": ALPHA_INV_CODATA, "codata_unc": ALPHA_INV_UNC}
# expoente exato que resolve Omega^x = alpha^-1 (sempre existe -> ajuste exato por construcao)
x_star = math.log(ALPHA_INV_CODATA) / math.log(OMEGA)
b["exact_exponent_x_star"] = x_star
# quantos digitos de beta o alvo absorve: sensibilidade d(alpha^-1)/d(beta)
sens = ALPHA_INV_CODATA * math.log(OMEGA)   # ~652 por unidade de beta
b["sensitivity_dalpha_dbeta"] = sens
b["delta_alpha_for_beta_step_1e-3"] = sens * 1e-3
b["delta_alpha_for_beta_step_1e-4"] = sens * 1e-4
# incerteza de beta necessaria para reproduzir alpha^-1 dentro da incerteza CODATA
b["beta_precision_needed_for_codata_unc"] = ALPHA_INV_UNC / sens
# aritmetica interna do nucleo: Omega^1.033 = ? (rotulo "137.04, 0.003%")
b["omega_pow_1.033"] = OMEGA ** 1.033
b["omega_pow_1.03"] = OMEGA ** 1.03
b["core_quoted_value"] = 137.04
b["error_percent_of_omega_1.033_vs_codata"] = (
    100 * abs(OMEGA ** 1.033 - ALPHA_INV_CODATA) / ALPHA_INV_CODATA)
# contagem de graus de liberdade
b["free_continuous_params"] = 1
b["data_points_fit"] = 1
b["test_dof"] = 0
b["verdict_consistency"] = (
    "tautologicamente exata (ajuste de 1 parametro a 1 dado; x*=%.6f sempre existe); "
    "aritmetica interna do rotulo '137.04 / 0.003%%' e apenas arredondamento de beta "
    "a 3-4 digitos" % x_star)
b["verdict_identifiability"] = (
    "nao-identificavel (tuning): beta nao tem derivacao independente no nucleo "
    "(paper_origin_omega 'In Progress', RESEARCH_RESULTS.md:211); a propria "
    "AUDITORIA.md do paper_fine_structure ja classifica 'coincidencia numerica, "
    "nao derivacao' (E0/H1)")
results["subclaims"]["b_alpha_inv"] = b

# =====================================================================
# (c) bounce: xi=100 -> N=61.7, n_s=0.967 ("Planck compatible")
# =====================================================================
NS_PLANCK, NS_UNC = 0.965, 0.004     # arXiv:1807.06209 abstract, 68% CL
c = {"claim": "xi=100 -> N=61.7, n_s=0.967", "planck_ns": NS_PLANCK,
     "planck_ns_unc": NS_UNC}
ns_claim = 0.967
c["sigma_vs_planck"] = abs(ns_claim - NS_PLANCK) / NS_UNC
# sensibilidade: mesma conta com o valor de tabela 4-casas usual (0.9649 +/- 0.0042)
# NAO usado no veredito (nao fetchado); apenas mostra que a conclusao nao muda
c["sigma_sensitivity_if_0.9649_0.0042"] = abs(ns_claim - 0.9649) / 0.0042
# identificabilidade: n_s = 1 - 2/N e consequencia algebrica de N (limite Starobinsky,
# exatamente a formula usada em optimize_inflation.py:92-93)
c["ns_from_N_61.7"] = 1 - 2 / 61.7
c["ns_from_N_60"] = 1 - 2 / 60
c["xi_grid_scanned"] = [1.0, 10.0, 100.0, 1000.0, 3000.0, 5000.0, 10000.0]  # scan_xi.py:46
c["selection_rule_in_code"] = "N_target=60.0, ns_target=0.965 (optimize_inflation.py:97-99)"
c["verdict_consistency"] = (
    "consistente numericamente (%.2f sigma vs Planck 2018 n_s=0.965+/-0.004) - mas "
    "trivialmente: qualquer modelo com N~60 na classe Starobinsky da n_s=1-2/N~0.967"
    % c["sigma_vs_planck"])
c["verdict_identifiability"] = (
    "nao-identificavel (tuning): xi varrido em grade {1,10,100,1000,...} e 100 "
    "selecionado por dar N>60 (tabela rotula a linha 'TARGET'); n_s=1-2/N e entao "
    "consequencia algebrica do proprio alvo N=60 - o codigo o declara: 'se "
    "conseguirmos N=60, teremos n_s correto automaticamente' "
    "(optimize_inflation.py:95). n_s nao e predicao do mecanismo de bounce.")
results["subclaims"]["c_bounce_ns"] = c

# =====================================================================
# (d) rho_Lambda ~ 1/L_H^2: "CONFIRMED" com x1.46 (46%)
# =====================================================================
G, G_UNC = 6.67430e-11, 0.00015e-11          # CODATA 2022 (NIST)
H0_KMSMPC, H0_UNC = 67.4, 0.5                # Planck 2018 abstract
OMEGA_M, OMEGA_M_UNC = 0.315, 0.007          # Planck 2018 abstract
AU = 149597870700.0                          # definicao IAU (exata)
PC = (648000 / math.pi) * AU                 # definicao (exata)
MPC = 1e6 * PC
C_LIGHT = 299792458.0                        # definicao SI (exata)

H0 = H0_KMSMPC * 1000.0 / MPC                # s^-1
rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)   # kg/m^3
omega_L = 1 - OMEGA_M                        # plano (base-LCDM do proprio Planck VI)
rho_L_obs = omega_L * rho_crit
# incerteza (propagacao 1a ordem; G negligivel)
rel_unc = math.sqrt((2 * H0_UNC / H0_KMSMPC) ** 2 + (OMEGA_M_UNC / omega_L) ** 2
                    + (G_UNC / G) ** 2)
rho_L_unc = rho_L_obs * rel_unc

d = {"claim": "rho_Lambda ~ 1/L_H^2 'CONFIRMED', holographic 8.5e-27 vs observed 5.8e-27",
     "core_holographic": 8.5e-27, "core_observed": 5.8e-27,
     "rho_crit_planck_kg_m3": rho_crit,
     "rho_Lambda_obs_from_planck_kg_m3": rho_L_obs,
     "rho_Lambda_obs_unc_kg_m3": rho_L_unc,
     "relative_unc_percent": 100 * rel_unc}
# checagem: o valor 'observed 5.8e-27' do nucleo bate com Planck?
d["core_observed_matches_planck_within"] = abs(5.8e-27 - rho_L_obs) / rho_L_unc
# sigma do 'holographic' contra o observado real
d["sigma_holographic_vs_observed"] = abs(8.5e-27 - rho_L_obs) / rho_L_unc
d["ratio_pred_over_obs"] = 8.5e-27 / rho_L_obs
# 2a rota estrutural: a construcao do script do nucleo (holographic_lambda.py:76-80)
# rho_holo = (L c^2 / 2G) / ((4/3) pi L^3) com L = c/H0  ==>  = 3 H0^2/(8 pi G) = rho_crit
# i.e., a 'predicao holografica' e IDENTICAMENTE a densidade critica;
# ratio pred/obs == rho_crit/(Omega_L rho_crit) == 1/Omega_L, por construcao.
d["structural_identity"] = "rho_holo == rho_crit  =>  ratio == 1/Omega_Lambda"
d["one_over_omega_lambda"] = 1 / omega_L
d["core_quoted_ratio"] = 1.46
# tolerancia pre-declarada encontrada no arquivo:
d["declared_tolerance_found"] = (
    "unica tolerancia no arquivo: 'if 0.1 < ratio < 10' -> 'SUCCESS ... within 1 "
    "order of magnitude' (holographic_lambda.py:91-92); nenhuma tolerancia que "
    "justifique 'CONFIRMED' para 46%% foi declarada em lugar algum")
d["verdict_consistency"] = (
    "inconsistente como formulado: 'CONFIRMED' com desvio de %.0f sigma "
    "(incerteza observacional ~%.1f%%); o criterio interno real era 'dentro de 1 "
    "ordem de magnitude', que sustenta no maximo 'ordem de grandeza correta' - "
    "exatamente o que a AUDITORIA.md interna ja diz"
    % (d["sigma_holographic_vs_observed"], 100 * rel_unc))
d["verdict_identifiability"] = (
    "nao-identificavel como predicao: a construcao usada e identicamente rho_crit "
    "(ratio == 1/Omega_Lambda por identidade algebrica); o desvio de 46%% e apenas "
    "1/0.685, e qualquer fator O(1) no cutoff/horizonte o absorveria")
results["subclaims"]["d_lambda_holography"] = d

# =====================================================================
out = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/constant_fits/adjudication_results.json"
with open(out, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# ------- log legivel -------
print("=" * 72)
print("(a) sin^2 theta_W = 3/13 =", f"{claim:.9f}")
for name, r in a["schemes"].items():
    print(f"    {name:32s} PDG={r['pdg_value']:.5f}({int(round(r['pdg_unc']*1e5))}) "
          f"delta={r['delta']:+.5f} ({r['delta_percent']:.3f}%)  sigma={r['sigma']:.1f}")
print(f"    esquema mais caridoso: {charit}  ->  {a['most_charitable_sigma']:.1f} sigma")
print(f"    on-shell tree-level de mW/mZ (diagnostico): "
      f"{a['onshell_from_masses_1_minus_mW2_over_mZ2']:.5f}")
print(f"    VEREDITO: {a['verdict_consistency']}; {a['verdict_identifiability'][:60]}...")
print("=" * 72)
print("(b) alpha^-1 = Omega^beta")
print(f"    x* exato = ln(137.035999177)/ln(117.038) = {x_star:.9f}")
print(f"    Omega^1.033 = {b['omega_pow_1.033']:.4f}   Omega^1.03 = {b['omega_pow_1.03']:.4f}")
print(f"    sensibilidade: d(alpha^-1)/d(beta) = {sens:.1f}  "
      f"(passo 1e-3 em beta -> {sens*1e-3:.3f} em alpha^-1)")
print(f"    precisao de beta p/ incerteza CODATA: {b['beta_precision_needed_for_codata_unc']:.2e}")
print(f"    dof de teste: {b['test_dof']}  ->  ajuste exato por construcao")
print("=" * 72)
print("(c) bounce n_s")
print(f"    claim 0.967 vs Planck 0.965+/-0.004  ->  {c['sigma_vs_planck']:.2f} sigma")
print(f"    (sensibilidade com 0.9649+/-0.0042: {c['sigma_sensitivity_if_0.9649_0.0042']:.2f} sigma)")
print(f"    n_s(N=61.7) = 1-2/61.7 = {c['ns_from_N_61.7']:.4f}  (algebrico, nao dinamico)")
print("=" * 72)
print("(d) rho_Lambda")
print(f"    rho_crit(Planck H0) = {rho_crit:.3e} kg/m^3")
print(f"    rho_Lambda_obs = {rho_L_obs:.3e} +/- {rho_L_unc:.1e} kg/m^3 "
      f"({100*rel_unc:.1f}%)")
print(f"    nucleo 'observed' 5.8e-27: {d['core_observed_matches_planck_within']:.2f} sigma do Planck (ok)")
print(f"    nucleo 'holographic' 8.5e-27: {d['sigma_holographic_vs_observed']:.1f} sigma do observado")
print(f"    identidade estrutural: ratio == 1/Omega_L = {1/omega_L:.3f} (nucleo cita 1.46)")
print("=" * 72)
print("JSON escrito em", out)
