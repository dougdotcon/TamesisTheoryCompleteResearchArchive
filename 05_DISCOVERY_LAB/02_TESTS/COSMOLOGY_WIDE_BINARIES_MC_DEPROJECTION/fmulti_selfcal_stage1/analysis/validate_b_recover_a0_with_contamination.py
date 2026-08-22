"""Validacao B -- SPARC-FMULTI-STAGE1: recuperacao de a0 verdadeiro sob
contaminacao de multiplicidade oculta conhecida SIMULTANEA. Criterios de
aceitacao B1-B3 fixados ANTES desta execucao em
../METHODOLOGY_ADDENDUM.md Secao 3.

NAO le nenhum arquivo de dado real desta linha -- populacao 100% sintetica
(build_synthetic_population.py), mesma disciplina da Validacao A.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))
LOCKED_ANALYSIS_DIR = THIS_DIR.parent.parent / "analysis"
sys.path.insert(0, str(LOCKED_ANALYSIS_DIR))

import delta_obs_newt as don  # noqa: E402
import build_synthetic_population as bp  # noqa: E402
import selfcal_pipeline as sp  # noqa: E402

RESULTS_DIR = THIS_DIR.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

N_SYS = 8000
N_MC = 120
N_BOOTSTRAP = 400
N_BOOTSTRAP_A0_REFIT = 300
ANCHOR_BIN = 4
TOL_F_MULTI = 0.05
BIN_EDGES = don.BIN_EDGES_LOG_GN_SPARC003

A0_TRUE = 1.2e-10  # McGaugh et al. 2016 -- mesmo valor de teste ja usado no
                     # controle positivo do Adendo 4c de PREREGISTRATION.md
A0_TOL_LOG10 = 0.30  # tolerancia de 0.30 dex (~2x em a0) para "recuperado"
                       # -- mais folgada que a checagem de sanidade de 1
                       # ordem de grandeza ja usada no resto da linha,
                       # porque aqui a pergunta e' se o a0 RECUPERADO bate
                       # com o a0 INJETADO, nao com um valor de referencia
                       # externo -- ver METHODOLOGY_ADDENDUM.md Secao 4
                       # (degenerescencia a0/f_multi conhecida a priori).

SCENARIOS = [
    {"name": "a0_true=1.2e-10, f_multi_true=0.35",
     "f_multi_true": 0.35, "a0_true": A0_TRUE,
     "seed_cat": 8001, "seed_fake": 8002, "seed_calib": 8003},
    {"name": "a0_true=1.2e-10, f_multi_true=0.47",
     "f_multi_true": 0.47, "a0_true": A0_TRUE,
     "seed_cat": 8101, "seed_fake": 8102, "seed_calib": 8103},
]


def _check_anchor_bin_mond_negligible(gN_bin_median, a0_true, anchor_bin) -> dict:
    gN_anchor = gN_bin_median[anchor_bin]
    delta_aqual_anchor = float(sp.delta_aqual(np.array([gN_anchor]), a0_true)[0])
    return {
        "gN_anchor_si": float(gN_anchor),
        "delta_aqual_predicted_at_anchor": delta_aqual_anchor,
        "negligible": bool(abs(delta_aqual_anchor) < 0.01),
    }


def run_scenario(scn: dict) -> dict:
    t0 = time.time()
    rng_cat = np.random.default_rng(scn["seed_cat"])
    cat = bp.generate_structural_catalog(N_SYS, rng_cat)

    rng_fake = np.random.default_rng(scn["seed_fake"])
    fake = bp.build_fake_real_dataset(
        cat, f_multi_true=scn["f_multi_true"], a0_true=scn["a0_true"],
        include_wobble_true=True, rng=rng_fake,
    )

    # ---- checagem a priori: o bin-ancora e' insensivel ao a0_true? ----
    log_gN_proj_cat = np.log10(sp.G_SI * cat["Mtot_cat_kg"] / cat["s_m"] ** 2)
    inner_edges = BIN_EDGES[1:-1]
    bin_idx_cat = np.digitize(log_gN_proj_cat, inner_edges)
    in_range_cat = (log_gN_proj_cat >= BIN_EDGES[0]) & (log_gN_proj_cat <= BIN_EDGES[-1])
    gN_bin_median_cat = np.array([
        np.median(10.0 ** log_gN_proj_cat[in_range_cat & (bin_idx_cat == b)])
        for b in range(5)
    ])
    anchor_check = _check_anchor_bin_mond_negligible(gN_bin_median_cat, scn["a0_true"], ANCHOR_BIN)

    # ---- B1: pipeline NAO corrigido (f_multi=0 fixo) -- deve mostrar
    #      a0 enviesado (o mesmo modo de falha que reprovou v1/v2 sobre
    #      dado real) ----
    uncorrected = sp.run_delta_obs_newt_selfcal(
        cat["s_m"], fake["v_p_fake_real"], cat["M1_cat_kg"], cat["M2_cat_kg"],
        cat["e_m"], cat["e_lo"], cat["e_hi"], cat["alpha_ecc"], cat["dpm_sig"],
        cat["d_mean_pc"], cat["e_pmRA1"], cat["e_pmRA2"], cat["e_pmDE1"], cat["e_pmDE2"],
        f_multi=0.0, bin_edges=BIN_EDGES, n_mc=N_MC, seed=scn["seed_calib"] + 1,
        include_wobble=True, n_bootstrap=None, return_raw=True,
    )
    gN_bin_uncorr = np.array(uncorrected["gN_bin_median_si"])
    delta_uncorr = np.array(uncorrected["delta_obs_newt_primary"])
    a0_fit_uncorr = sp.fit_a0(gN_bin_uncorr, delta_uncorr, x0=1.0)
    a0_fit_uncorr_ci = sp.bootstrap_a0_refit(
        uncorrected["_raw"], n_bins=5, n_bootstrap=N_BOOTSTRAP_A0_REFIT,
        seed=scn["seed_calib"] + 11,
    )
    b1_biased = bool(
        a0_fit_uncorr is not None
        and abs(np.log10(a0_fit_uncorr / scn["a0_true"])) > A0_TOL_LOG10
    )

    # ---- Auto-calibracao de f_multi (pipeline sob teste) ----
    calib = sp.calibrate_f_multi(
        cat["s_m"], fake["v_p_fake_real"], cat["M1_cat_kg"], cat["M2_cat_kg"],
        cat["e_m"], cat["e_lo"], cat["e_hi"], cat["alpha_ecc"], cat["dpm_sig"],
        cat["d_mean_pc"], cat["e_pmRA1"], cat["e_pmRA2"], cat["e_pmDE1"], cat["e_pmDE2"],
        bin_edges=BIN_EDGES, anchor_bin=ANCHOR_BIN, n_mc=N_MC, seed=scn["seed_calib"],
        f_lo=0.0, f_hi=0.9, xtol=5e-3, include_wobble=True, n_bootstrap_final=N_BOOTSTRAP,
    )
    f_calibrated = calib["f_multi_calibrated"]
    b3_pass = bool(abs(f_calibrated - scn["f_multi_true"]) <= TOL_F_MULTI)

    # ---- B2: pipeline CORRIGIDO -- refaz com return_raw=True no f_multi
    #      calibrado para poder reajustar a0 com IC bootstrap ----
    corrected = sp.run_delta_obs_newt_selfcal(
        cat["s_m"], fake["v_p_fake_real"], cat["M1_cat_kg"], cat["M2_cat_kg"],
        cat["e_m"], cat["e_lo"], cat["e_hi"], cat["alpha_ecc"], cat["dpm_sig"],
        cat["d_mean_pc"], cat["e_pmRA1"], cat["e_pmRA2"], cat["e_pmDE1"], cat["e_pmDE2"],
        f_multi=f_calibrated, bin_edges=BIN_EDGES, n_mc=N_MC, seed=scn["seed_calib"] + 777,
        include_wobble=True, n_bootstrap=None, return_raw=True,
    )
    gN_bin_corr = np.array(corrected["gN_bin_median_si"])
    delta_corr = np.array(corrected["delta_obs_newt_primary"])
    a0_fit_corr = sp.fit_a0(gN_bin_corr, delta_corr, x0=1.0)
    a0_fit_corr_ci = sp.bootstrap_a0_refit(
        corrected["_raw"], n_bins=5, n_bootstrap=N_BOOTSTRAP_A0_REFIT,
        seed=scn["seed_calib"] + 22,
    )
    ci_x1 = a0_fit_corr_ci.get("x0=1.0", {})
    a0_within_ci = bool(
        ci_x1.get("ci95_lo_si_m_s2") is not None
        and ci_x1["ci95_lo_si_m_s2"] <= scn["a0_true"] <= ci_x1["ci95_hi_si_m_s2"]
    )
    a0_close_in_log = bool(
        a0_fit_corr is not None
        and abs(np.log10(a0_fit_corr / scn["a0_true"])) <= A0_TOL_LOG10
    )
    b2_pass = bool(a0_within_ci or a0_close_in_log)
    b2_inconclusive_by_design = bool(not b2_pass)

    elapsed = time.time() - t0
    scenario_pass = bool(b1_biased and (b2_pass) and b3_pass)

    return {
        "scenario": scn["name"],
        "f_multi_true": scn["f_multi_true"], "a0_true_si_m_s2": scn["a0_true"],
        "n_sys": N_SYS, "n_mc": N_MC, "n_bootstrap": N_BOOTSTRAP,
        "seeds": scn,
        "anchor_bin_mond_negligibility_check": anchor_check,
        "f_multi_calibrated": f_calibrated,
        "converged_bracket": calib["converged_bracket"],
        "checks": {
            "B1_uncorrected_pipeline_is_biased": {
                "pass": b1_biased,
                "a0_fit_uncorrected_si_m_s2": a0_fit_uncorr,
                "a0_fit_uncorrected_bootstrap_ci": a0_fit_uncorr_ci,
                "abs_log10_ratio_to_a0_true": (
                    abs(np.log10(a0_fit_uncorr / scn["a0_true"])) if a0_fit_uncorr else None
                ),
                "tol_log10": A0_TOL_LOG10,
            },
            "B2_corrected_pipeline_recovers_a0_or_honestly_inconclusive": {
                "pass": b2_pass,
                "inconclusive_by_design": b2_inconclusive_by_design,
                "a0_fit_corrected_si_m_s2": a0_fit_corr,
                "a0_fit_corrected_bootstrap_ci": a0_fit_corr_ci,
                "a0_true_within_ci95": a0_within_ci,
                "a0_close_in_log10_tol": a0_close_in_log,
            },
            "B3_f_multi_calibration_stable_with_a0_true_present": {
                "pass": b3_pass, "f_multi_true": scn["f_multi_true"],
                "f_multi_calibrated": f_calibrated,
                "abs_diff": abs(f_calibrated - scn["f_multi_true"]), "tol": TOL_F_MULTI,
            },
        },
        "scenario_pass_all_checks": scenario_pass,
        "elapsed_seconds": elapsed,
    }


def main():
    print("=" * 78)
    print("Validacao B -- recuperacao de a0 sob contaminacao de multiplicidade conhecida")
    print("=" * 78)
    results = []
    for scn in SCENARIOS:
        print(f"\n--- Cenario: {scn['name']} ---")
        r = run_scenario(scn)
        results.append(r)
        print(f"  checagem a priori (bin-ancora insensivel a a0_true): "
              f"{r['anchor_bin_mond_negligibility_check']}")
        print(f"  f_multi_true={r['f_multi_true']:.3f} -> calibrado={r['f_multi_calibrated']:.4f}")
        b1 = r["checks"]["B1_uncorrected_pipeline_is_biased"]
        print(f"  B1 (nao-corrigido enviesado): {b1['pass']} "
              f"(a0_fit_uncorr={b1['a0_fit_uncorrected_si_m_s2']})")
        b2 = r["checks"]["B2_corrected_pipeline_recovers_a0_or_honestly_inconclusive"]
        print(f"  B2 (corrigido recupera a0_true OU inconclusivo honesto): {b2['pass']} "
              f"(a0_fit_corr={b2['a0_fit_corrected_si_m_s2']}, "
              f"IC95={b2['a0_fit_corrected_bootstrap_ci']})")
        b3 = r["checks"]["B3_f_multi_calibration_stable_with_a0_true_present"]
        print(f"  B3 (f_multi calibrado estavel): {b3['pass']}")
        print(f"  VEREDITO DO CENARIO: {'PASS' if r['scenario_pass_all_checks'] else 'FAIL'} "
              f"({r['elapsed_seconds']:.1f}s)")

    all_pass = bool(all(r["scenario_pass_all_checks"] for r in results))
    any_inconclusive_by_design = bool(any(
        r["checks"]["B2_corrected_pipeline_recovers_a0_or_honestly_inconclusive"]["inconclusive_by_design"]
        for r in results
    ))
    summary = {
        "validation": "B_recover_a0_with_contamination",
        "run_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "a0_true_si_m_s2": A0_TRUE, "a0_tol_log10": A0_TOL_LOG10,
        "tol_f_multi": TOL_F_MULTI, "anchor_bin": ANCHOR_BIN,
        "bin_edges_log10_gN": BIN_EDGES.tolist(),
        "scenarios": results,
        "all_scenarios_pass": all_pass,
        "any_scenario_inconclusive_by_design": any_inconclusive_by_design,
    }
    out_path = RESULTS_DIR / "validation_B_results.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n{'='*78}\nVEREDITO GERAL DA VALIDACAO B: {'PASS' if all_pass else 'FAIL'}")
    print(f"Resultado completo salvo em {out_path}")
    return summary


if __name__ == "__main__":
    main()
