"""Reexecucao adversarial INDEPENDENTE do Estagio 2 (SPARC-FMULTI-STAGE2,
DISC-DEC-029) -- AGENTS.md passo 7.

Escrito do ZERO a partir da leitura completa de
../../PREREGISTRATION_STAGE2.md, ../../METHODOLOGY_ADDENDUM.md e
../../PROVENANCE_CHAE_EQS.md -- ANTES de ler
../../analysis/run_stage2_primary_analysis.py ou
../../results/result_stage2_primary.json. Reusa (nao reimplementa) o
pipeline ja travado e adversarialmente verificado do Estagio 1
(../../analysis/selfcal_pipeline.py, ../../analysis/companion_injection.py)
e o modulo LOCKED ../../../analysis/deprojection_common.py -- exatamente o
que a tarefa de reexecucao adversarial autoriza (nao e' preciso re-derivar
a mecanica orbital/injecao de massa do zero, so' a sequencia de chamadas do
driver e a logica de decisao).

Sequencia de chamadas EXATA da Secao 4.1-4.6 do pre-registro:
  1. calibrate_f_multi(..., return_raw=True) sobre os 30.203 sistemas de
     descoberta reais -> f_multi_hat
  2. delta_obs-newt(bin) corrigido = calib["final_result"]["delta_obs_newt_primary"]
  3. fit_a0() nos 5 valores corrigidos, x0=1.0 e x0=5.0
  4. bootstrap_a0_refit() sobre calib["final_raw"] (NAO uma chamada manual
     reconstruida de run_delta_obs_newt_selfcal -- confirmado por inspecao
     de ../../analysis/selfcal_pipeline.py linhas 436-487 que
     calibrate_f_multi(return_raw=True) ja propaga a MESMA seed+777 usada
     para "final_result" para dentro de "final_raw", eliminando o risco de
     descasamento de semente que a Secao 4.5/12.4 do pre-registro
     identificou como o ponto de maior risco de erro silencioso desta
     especificacao)
  5. Regra de decisao Secao 5 (camada mecanica + camada interpretativa de
     correcao de vies)
  6. Gatilhos de checagem adversarial de descoberta de nulo, Secao 6 (1-5)

Disciplina do holdout selado (Secao 8 do pre-registro, linha vermelha):
o unico acesso a discovery_holdout_split.json neste script extrai
EXCLUSIVAMENTE a chave "discovery_pair_ids" (mais "seed"/"n_discovery" para
documentacao) -- a chave "holdout_pair_ids" NUNCA e referenciada em nenhuma
linha deste arquivo (grep-check separado confirma isso, ver
../ADVERSARIAL_DEBUNKER_REPORT.md Secao 1.2). catalog.parquet (catalogo bruto
completo, nao filtrado) NUNCA e aberto por este script.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# Localizacao dos modulos LOCKED reaproveitados (Parte 1 do mandato:
# pode reusar analysis/selfcal_pipeline.py e analysis/companion_injection.py,
# ja verificados adversarialmente em DISC-DEC-023/026 -- mas o DRIVER abaixo
# (sequencia de chamadas + logica de decisao) e' escrito do zero aqui).
# ---------------------------------------------------------------------
REPO = Path("/home/user/TamesisTheoryCompleteResearchArchive")
TEST_DIR = REPO / "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION"
WB_DIR = REPO / "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES"
STAGE1_DIR = TEST_DIR / "fmulti_selfcal_stage1"
LOCKED_ANALYSIS_DIR = TEST_DIR / "analysis"
SELFCAL_DIR = STAGE1_DIR / "analysis"
OUT_DIR = Path(__file__).resolve().parent.parent / "results"
OUT_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(LOCKED_ANALYSIS_DIR))
sys.path.insert(0, str(SELFCAL_DIR))

import deprojection_common as dc  # noqa: E402  (LOCKED, so' importado)
from delta_obs_newt import BIN_EDGES_LOG_GN_SPARC003  # noqa: E402  (LOCKED)
from selfcal_pipeline import (  # noqa: E402  (Estagio 1, ja verificado adversarialmente)
    calibrate_f_multi,
    fit_a0,
    bootstrap_a0_refit,
)

# ---------------------------------------------------------------------
# Parametros fixados pelo pre-registro (Secao 4.6) -- NAO escolhidos por
# este script, copiados literalmente da tabela travada.
# ---------------------------------------------------------------------
SEED_STAGE2 = 20260822
ANCHOR_BIN = 4
N_MC = 200
N_BOOTSTRAP = 2000
F_LO, F_HI = 0.0, 0.9
XTOL = 5e-4
INCLUDE_WOBBLE = True

A0_A = 1.082288e-10  # cH0/(2pi), "Ponte Holografica"
A0_B = 6.800218e-10  # cH0, "MOND Emergence"
BIAS_FACTOR_LO, BIAS_FACTOR_HI = 1.4, 1.6  # residuo conhecido do Estagio 1 (Secao 7)

LITERATURE_F_MULTI_LO, LITERATURE_F_MULTI_HI = 0.25, 0.47


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_discovery_sample() -> pd.DataFrame:
    """Carrega a amostra de descoberta real (30.203 sistemas), NUNCA o
    holdout. Unico ponto de contato com discovery_holdout_split.json --
    extrai SOMENTE discovery_pair_ids/seed/n_discovery, holdout_pair_ids
    jamais referenciado por nome em nenhuma linha deste arquivo."""
    qfs = pd.read_parquet(WB_DIR / "data" / "quality_filtered_sample.parquet")
    hwang = pd.read_parquet(STAGE1_DIR.parent / "data" / "hwang_eccentricity_subset.parquet")

    with open(WB_DIR / "data" / "discovery_holdout_split.json") as f:
        split = json.load(f)
    discovery_pair_ids = list(split["discovery_pair_ids"])
    split_seed = split["seed"]
    n_discovery_expected = split["n_discovery"]
    del split  # descarta o dict inteiro imediatamente apos extrair discovery only

    discovery_set = set(discovery_pair_ids)
    del discovery_pair_ids

    qfs = qfs.assign(pair_id=qfs["Source1"].astype(str) + "_" + qfs["Source2"].astype(str))
    disc = qfs[qfs["pair_id"].isin(discovery_set)].reset_index(drop=True)
    assert len(disc) == n_discovery_expected == 30203, (
        f"contagem de descoberta inesperada: {len(disc)} (split.seed={split_seed})"
    )

    hwang = hwang.assign(pair_id=hwang["source_id1"].astype(str) + "_" + hwang["source_id2"].astype(str))
    before = len(disc)
    disc = disc.merge(
        hwang[["pair_id", "e", "e0", "e1", "alpha", "dpm_sig"]], on="pair_id", how="left"
    )
    assert len(disc) == before, "merge com Hwang duplicou/perdeu linhas"
    n_missing_ecc = int(disc["e"].isna().sum())
    log(f"amostra de descoberta carregada: {len(disc)} sistemas "
        f"(split seed={split_seed}); sistemas sem entrada Hwang (e=NaN): {n_missing_ecc}")
    return disc


def build_pipeline_inputs(disc: pd.DataFrame) -> dict:
    """Constroi todos os arrays SI exigidos pela assinatura de
    calibrate_f_multi/run_delta_obs_newt_selfcal, Secao 4.2 do pre-registro."""
    s_m = disc["sepAU"].to_numpy(dtype=np.float64) * dc.AU_M
    M1_cat_kg = disc["M1_Msun"].to_numpy(dtype=np.float64) * dc.MSUN_KG
    M2_cat_kg = disc["M2_Msun"].to_numpy(dtype=np.float64) * dc.MSUN_KG
    d_mean_pc = disc["d_mean_pc"].to_numpy(dtype=np.float64)

    dmu_mas_yr = np.sqrt(
        (disc["pmRA1"].to_numpy(dtype=np.float64) - disc["pmRA2"].to_numpy(dtype=np.float64)) ** 2
        + (disc["pmDE1"].to_numpy(dtype=np.float64) - disc["pmDE2"].to_numpy(dtype=np.float64)) ** 2
    )
    v_p_km_s = dc.MAS_YR_TO_KM_S_PER_PC * dmu_mas_yr * d_mean_pc
    v_p_real_si = v_p_km_s * 1000.0  # km/s -> m/s

    e_m = disc["e"].to_numpy(dtype=np.float64)
    e_lo = disc["e0"].to_numpy(dtype=np.float64)
    e_hi = disc["e1"].to_numpy(dtype=np.float64)
    alpha_ecc = disc["alpha"].to_numpy(dtype=np.float64)
    dpm_sig = disc["dpm_sig"].to_numpy(dtype=np.float64)

    pmra_err1 = disc["e_pmRA1"].to_numpy(dtype=np.float64)
    pmra_err2 = disc["e_pmRA2"].to_numpy(dtype=np.float64)
    pmde_err1 = disc["e_pmDE1"].to_numpy(dtype=np.float64)
    pmde_err2 = disc["e_pmDE2"].to_numpy(dtype=np.float64)

    log(f"v_p_real: mediana={np.median(v_p_real_si)/1000.0:.4f} km/s, "
        f"min={v_p_real_si.min()/1000.0:.4f}, max={v_p_real_si.max()/1000.0:.4f}")

    return dict(
        s=s_m, v_p_real=v_p_real_si, M1_cat=M1_cat_kg, M2_cat=M2_cat_kg,
        e_m=e_m, e_lo=e_lo, e_hi=e_hi, alpha_ecc=alpha_ecc, dpm_sig=dpm_sig,
        d_mean_pc=d_mean_pc,
        pmra_err1=pmra_err1, pmra_err2=pmra_err2, pmde_err1=pmde_err1, pmde_err2=pmde_err2,
    )


def apply_decision_rule(a0_fit: float, ci_lo: float, ci_hi: float) -> dict:
    """Secao 5 do pre-registro -- camada mecanica + camada interpretativa
    de correcao de vies. Implementada aqui do zero a partir da leitura da
    Secao 5/7, nao copiada de nenhum script do agente primario."""
    a_falsified = not (ci_lo <= A0_A <= ci_hi)
    b_falsified = not (ci_lo <= A0_B <= ci_hi)

    if a_falsified and b_falsified:
        mechanical_verdict = "BOTH_FALSIFIED"
    elif a_falsified and not b_falsified:
        mechanical_verdict = "H_A_FALSIFIED"
    elif b_falsified and not a_falsified:
        mechanical_verdict = "H_B_FALSIFIED"
    else:
        mechanical_verdict = "INCONCLUSIVE"

    # Camada interpretativa: dividir a0_fit e os dois limites do IC pelo
    # fator de vies residual conhecido (1.4-1.6x) -- verificar se isso
    # traria a0_A e/ou a0_B de volta para dentro do intervalo.
    bias_checks = {}
    rescued_any = False
    for label, factor in (("bias_1.4x", BIAS_FACTOR_LO), ("bias_1.6x", BIAS_FACTOR_HI)):
        a0_fit_corr = a0_fit / factor
        ci_lo_corr = ci_lo / factor
        ci_hi_corr = ci_hi / factor
        a_rescued = ci_lo_corr <= A0_A <= ci_hi_corr
        b_rescued = ci_lo_corr <= A0_B <= ci_hi_corr
        bias_checks[label] = dict(
            factor=factor, a0_fit_corrected=a0_fit_corr,
            ci95_lo_corrected=ci_lo_corr, ci95_hi_corrected=ci_hi_corr,
            a0_A_rescued=bool(a_rescued), a0_B_rescued=bool(b_rescued),
        )
        rescued_any = rescued_any or a_rescued or b_rescued

    if mechanical_verdict != "INCONCLUSIVE" and rescued_any:
        final_verdict = "INCONCLUSIVE_BIAS_LAYER"
    else:
        final_verdict = mechanical_verdict

    return dict(
        a0_A_falsified_mechanical=bool(a_falsified),
        a0_B_falsified_mechanical=bool(b_falsified),
        mechanical_verdict=mechanical_verdict,
        bias_correction_layer=bias_checks,
        bias_layer_rescues_any_hypothesis=bool(rescued_any),
        final_verdict=final_verdict,
    )


def check_section6_triggers(calib: dict, delta_corrected: np.ndarray,
                             a0_fit_x1: float | None, a0_fit_x5: float | None,
                             ci_x1: dict, ci_x1_reseed: dict) -> dict:
    """Secao 6, itens 1-5, checados explicitamente a partir da leitura do
    pre-registro (nao copiado do agente primario)."""
    triggers = {}

    # item 1: a0_fit corrigido fora da faixa plausivel de AMBAS H_A/H_B por
    # mais de uma ordem de grandeza
    both_bounds = [A0_A, A0_B]
    if a0_fit_x1 is not None:
        ratio_to_nearest = min(abs(np.log10(a0_fit_x1 / b)) for b in both_bounds)
        item1 = ratio_to_nearest > 1.0
    else:
        ratio_to_nearest = None
        item1 = True  # a0_fit nao convergiu -- tratado como gatilho
    triggers["item1_a0_fit_gt_1_order_outside_both"] = dict(
        fired=bool(item1), log10_distance_to_nearest_target=ratio_to_nearest,
    )

    # item 2: converged_bracket False, ou f_multi_hat a menos de xtol da borda
    f_hat = calib["f_multi_calibrated"]
    near_lo = abs(f_hat - F_LO) < XTOL
    near_hi = abs(f_hat - F_HI) < XTOL
    item2 = (not calib["converged_bracket"]) or near_lo or near_hi
    triggers["item2_bracket_not_converged_or_at_edge"] = dict(
        fired=bool(item2), converged_bracket=calib["converged_bracket"],
        f_multi_hat=f_hat, near_f_lo=bool(near_lo), near_f_hi=bool(near_hi),
    )

    # item 3: f_multi_hat fora de 0.25-0.47
    item3 = not (LITERATURE_F_MULTI_LO <= f_hat <= LITERATURE_F_MULTI_HI)
    triggers["item3_f_multi_outside_literature_range"] = dict(
        fired=bool(item3), f_multi_hat=f_hat,
        literature_range=[LITERATURE_F_MULTI_LO, LITERATURE_F_MULTI_HI],
    )

    # item 4: padrao qualitativo do delta_obs-newt(bin) corrigido -- deve
    # decair de bins de menor gN para maior (mesma direcao do vies de
    # wobble conhecido do Estagio 1, 0.15-0.22 dex) -- inverter essa
    # direcao ou trocar sinais sem razao fisica clara, ou exceder 1 ordem
    # de grandeza acima de 0.15-0.22 dex e' o gatilho.
    d = np.asarray(delta_corrected, dtype=np.float64)
    monotonic_declining = bool(np.all(np.diff(d) <= 1e-6))  # tolerancia numerica pequena
    max_abs = float(np.nanmax(np.abs(d)))
    magnitude_order_above = max_abs > 10 * 0.22  # mais de 1 ordem acima do teto conhecido
    sign_flip_without_reason = bool(np.any(np.diff(np.sign(d)) != 0) and not monotonic_declining)
    item4 = (not monotonic_declining) or magnitude_order_above
    triggers["item4_pattern_inconsistent_with_known_wobble_bias"] = dict(
        fired=bool(item4), delta_corrected=d.tolist(),
        monotonic_declining_with_gN=monotonic_declining,
        max_abs_dex=max_abs, magnitude_more_than_1_order_above_022dex=magnitude_order_above,
        sign_flip_detected=sign_flip_without_reason,
    )

    # item 5: robustez a N_bootstrap/seed do bootstrap -- checado
    # separadamente em check_seed_bootstrap_robustness() abaixo (grava no
    # dict de retorno principal, nao aqui, porque exige uma reexecucao
    # completa do bootstrap com parametros diferentes).
    triggers["item5_bootstrap_robustness"] = "ver bootstrap_robustness_check no JSON de resultado"

    any_fired = any(
        v.get("fired", False) for v in triggers.values() if isinstance(v, dict)
    )
    triggers["any_trigger_1_to_4_fired"] = bool(any_fired)
    return triggers


def main() -> None:
    t0 = time.time()
    log("=== Reexecucao adversarial independente -- SPARC-FMULTI-STAGE2 ===")
    log(f"parametros: SEED_STAGE2={SEED_STAGE2}, N_MC={N_MC}, N_BOOTSTRAP={N_BOOTSTRAP}, "
        f"anchor_bin={ANCHOR_BIN}, xtol={XTOL}")

    disc = load_discovery_sample()
    inputs = build_pipeline_inputs(disc)

    log("Passo 1: calibrate_f_multi(...) sobre os 30.203 sistemas reais (return_raw=True)")
    t1 = time.time()
    calib = calibrate_f_multi(
        **inputs,
        bin_edges=BIN_EDGES_LOG_GN_SPARC003, anchor_bin=ANCHOR_BIN,
        n_mc=N_MC, seed=SEED_STAGE2,
        f_lo=F_LO, f_hi=F_HI, xtol=XTOL, include_wobble=INCLUDE_WOBBLE,
        n_bootstrap_final=N_BOOTSTRAP, return_raw=True,
    )
    log(f"  calibrate_f_multi concluido em {time.time()-t1:.1f}s")
    f_multi_hat = calib["f_multi_calibrated"]
    converged = calib["converged_bracket"]
    log(f"  f_multi_hat={f_multi_hat:.4f}  converged_bracket={converged}  "
        f"bracket={calib['bracket']}")

    log("Passo 2: extrair delta_obs-newt(bin) corrigido de calib['final_result']")
    delta_corrected = np.array(calib["final_result"]["delta_obs_newt_primary"], dtype=np.float64)
    gN_bin_median = np.array(calib["final_result"]["gN_bin_median_si"], dtype=np.float64)
    n_sys_per_bin = calib["final_result"]["n_systems_per_bin"]
    log(f"  delta_obs-newt(bin) = {delta_corrected.tolist()}")
    log(f"  gN_bin_median (SI) = {gN_bin_median.tolist()}")
    log(f"  n_sys_per_bin = {n_sys_per_bin}")

    log("Passo 3: fit_a0() nos 5 valores corrigidos, x0=1.0 e x0=5.0")
    a0_fit_x1 = fit_a0(gN_bin_median, delta_corrected, x0=1.0)
    a0_fit_x5 = fit_a0(gN_bin_median, delta_corrected, x0=5.0)
    log(f"  a0_fit(x0=1.0)={a0_fit_x1}")
    log(f"  a0_fit(x0=5.0)={a0_fit_x5}")
    if a0_fit_x1 is not None and a0_fit_x5 is not None:
        agree = abs(np.log10(a0_fit_x1) - np.log10(a0_fit_x5)) < 0.01
        log(f"  convergencia x0=1.0 vs x0=5.0: {'CONCORDAM' if agree else 'DIVERGEM'} "
            f"(diff log10={abs(np.log10(a0_fit_x1)-np.log10(a0_fit_x5)):.6f})")
    else:
        agree = False
        log("  convergencia x0=1.0 vs x0=5.0: FALHA (um dos dois nao convergiu)")

    log("Passo 4-5: bootstrap_a0_refit() sobre calib['final_raw'] "
        "(mesma seed+777 de final_result, SEM reconstrucao manual)")
    t2 = time.time()
    ci = bootstrap_a0_refit(
        calib["final_raw"], n_bins=5, n_bootstrap=N_BOOTSTRAP,
        seed=SEED_STAGE2 + 999_999, x0_list=(1.0, 5.0),
    )
    log(f"  bootstrap_a0_refit concluido em {time.time()-t2:.1f}s")
    ci_x1 = ci["x0=1.0"]
    ci_x5 = ci["x0=5.0"]
    log(f"  IC95%(x0=1.0) = [{ci_x1['ci95_lo_si_m_s2']}, {ci_x1['ci95_hi_si_m_s2']}] "
        f"(n_valid={ci_x1['n_valid']}/{N_BOOTSTRAP})")
    log(f"  IC95%(x0=5.0) = [{ci_x5['ci95_lo_si_m_s2']}, {ci_x5['ci95_hi_si_m_s2']}] "
        f"(n_valid={ci_x5['n_valid']}/{N_BOOTSTRAP})")
    ci_lo_hi_agree = (
        ci_x1["ci95_lo_si_m_s2"] is not None and ci_x5["ci95_lo_si_m_s2"] is not None
        and abs(np.log10(ci_x1["ci95_lo_si_m_s2"]) - np.log10(ci_x5["ci95_lo_si_m_s2"])) < 0.05
        and abs(np.log10(ci_x1["ci95_hi_si_m_s2"]) - np.log10(ci_x5["ci95_hi_si_m_s2"])) < 0.05
    )
    log(f"  concordancia dos ICs x0=1.0 vs x0=5.0: {'SIM' if ci_lo_hi_agree else 'NAO/DIVERGEM'}")

    log("Passo 6: regra de decisao Secao 5 (camada mecanica + interpretativa de vies)")
    decision = apply_decision_rule(a0_fit_x1, ci_x1["ci95_lo_si_m_s2"], ci_x1["ci95_hi_si_m_s2"])
    log(f"  veredito mecanico: {decision['mechanical_verdict']}")
    log(f"  camada de vies resgata alguma hipotese?: {decision['bias_layer_rescues_any_hypothesis']}")
    log(f"  veredito final: {decision['final_verdict']}")

    log("Passo 7: gatilhos Secao 6 (itens 1-4; item 5 checado separadamente abaixo)")
    triggers = check_section6_triggers(calib, delta_corrected, a0_fit_x1, a0_fit_x5, ci_x1, None)
    for k, v in triggers.items():
        if isinstance(v, dict) and "fired" in v:
            log(f"  {k}: fired={v['fired']}")

    log("Checagem extra: robustez do IC a seed/N_bootstrap diferentes (gatilho item 5)")
    t3 = time.time()
    ci_seed_alt = bootstrap_a0_refit(
        calib["final_raw"], n_bins=5, n_bootstrap=N_BOOTSTRAP,
        seed=SEED_STAGE2 + 13_579, x0_list=(1.0,),
    )
    ci_nboot_1000 = bootstrap_a0_refit(
        calib["final_raw"], n_bins=5, n_bootstrap=1000,
        seed=SEED_STAGE2 + 999_999, x0_list=(1.0,),
    )
    log(f"  reexecucoes de robustez concluidas em {time.time()-t3:.1f}s")

    def _falsified(lo, hi, target):
        return not (lo <= target <= hi)

    bootstrap_robustness = dict(
        original=dict(seed=SEED_STAGE2 + 999_999, n_bootstrap=N_BOOTSTRAP,
                      ci95_lo=ci_x1["ci95_lo_si_m_s2"], ci95_hi=ci_x1["ci95_hi_si_m_s2"],
                      a0_A_falsified=_falsified(ci_x1["ci95_lo_si_m_s2"], ci_x1["ci95_hi_si_m_s2"], A0_A),
                      a0_B_falsified=_falsified(ci_x1["ci95_lo_si_m_s2"], ci_x1["ci95_hi_si_m_s2"], A0_B)),
        alt_seed=dict(seed=SEED_STAGE2 + 13_579, n_bootstrap=N_BOOTSTRAP,
                      ci95_lo=ci_seed_alt["x0=1.0"]["ci95_lo_si_m_s2"],
                      ci95_hi=ci_seed_alt["x0=1.0"]["ci95_hi_si_m_s2"],
                      a0_A_falsified=_falsified(ci_seed_alt["x0=1.0"]["ci95_lo_si_m_s2"],
                                                 ci_seed_alt["x0=1.0"]["ci95_hi_si_m_s2"], A0_A),
                      a0_B_falsified=_falsified(ci_seed_alt["x0=1.0"]["ci95_lo_si_m_s2"],
                                                 ci_seed_alt["x0=1.0"]["ci95_hi_si_m_s2"], A0_B)),
        n_bootstrap_1000=dict(seed=SEED_STAGE2 + 999_999, n_bootstrap=1000,
                               ci95_lo=ci_nboot_1000["x0=1.0"]["ci95_lo_si_m_s2"],
                               ci95_hi=ci_nboot_1000["x0=1.0"]["ci95_hi_si_m_s2"],
                               a0_A_falsified=_falsified(ci_nboot_1000["x0=1.0"]["ci95_lo_si_m_s2"],
                                                          ci_nboot_1000["x0=1.0"]["ci95_hi_si_m_s2"], A0_A),
                               a0_B_falsified=_falsified(ci_nboot_1000["x0=1.0"]["ci95_lo_si_m_s2"],
                                                          ci_nboot_1000["x0=1.0"]["ci95_hi_si_m_s2"], A0_B)),
    )
    robust = (
        bootstrap_robustness["original"]["a0_A_falsified"] == bootstrap_robustness["alt_seed"]["a0_A_falsified"]
        == bootstrap_robustness["n_bootstrap_1000"]["a0_A_falsified"]
        and bootstrap_robustness["original"]["a0_B_falsified"] == bootstrap_robustness["alt_seed"]["a0_B_falsified"]
        == bootstrap_robustness["n_bootstrap_1000"]["a0_B_falsified"]
    )
    triggers["item5_bootstrap_robustness"] = dict(fired=bool(not robust), details=bootstrap_robustness)
    log(f"  item5 (nao-robusto a seed/N_bootstrap): fired={not robust}")

    any_fired_final = any(
        (v.get("fired", False) if isinstance(v, dict) else False) for v in triggers.values()
    )
    triggers["any_trigger_1_to_5_fired"] = bool(any_fired_final)

    result = dict(
        test_id="SPARC-FMULTI-STAGE2",
        role="adversarial_independent_reproduction",
        preregistration="../../PREREGISTRATION_STAGE2.md (DISC-DEC-029)",
        params=dict(seed_stage2=SEED_STAGE2, n_mc=N_MC, n_bootstrap=N_BOOTSTRAP,
                    anchor_bin=ANCHOR_BIN, f_lo=F_LO, f_hi=F_HI, xtol=XTOL,
                    include_wobble=INCLUDE_WOBBLE),
        n_discovery_systems=int(len(disc)),
        f_multi_hat=f_multi_hat,
        converged_bracket=bool(converged),
        bracket=calib["bracket"],
        delta_obs_newt_corrected=delta_corrected.tolist(),
        gN_bin_median_si=gN_bin_median.tolist(),
        n_systems_per_bin=n_sys_per_bin,
        frac_has_multi=calib["final_result"]["frac_has_multi"],
        frac_nonzero_wobble=calib["final_result"]["frac_nonzero_wobble"],
        a0_fit_x0_1=a0_fit_x1,
        a0_fit_x0_5=a0_fit_x5,
        a0_fit_x0_agreement=bool(agree),
        ci95_x0_1=ci_x1,
        ci95_x0_5=ci_x5,
        ci95_x0_agreement=bool(ci_lo_hi_agree),
        decision=decision,
        section6_triggers=triggers,
        a0_A=A0_A, a0_B=A0_B,
        runtime_seconds=time.time() - t0,
    )

    out_path = OUT_DIR / "result_adversarial_stage2.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    log(f"resultado escrito em {out_path}")
    log(f"=== concluido em {time.time()-t0:.1f}s ===")


if __name__ == "__main__":
    main()
