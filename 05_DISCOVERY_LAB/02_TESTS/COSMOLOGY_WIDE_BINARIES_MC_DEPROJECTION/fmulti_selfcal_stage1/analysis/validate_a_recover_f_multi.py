"""Validacao A -- SPARC-FMULTI-STAGE1: recuperacao de f_multi verdadeiro em
populacao sintetica 100% Newtoniana (zero MOND) com multiplicidade oculta
conhecida e RUWE-correlacionado. Criterios de aceitacao A1-A4 fixados
ANTES desta execucao em ../METHODOLOGY_ADDENDUM.md Secao 3.

NAO le nenhum arquivo de dado real desta linha (ver METHODOLOGY_ADDENDUM.md
Secao 5) -- toda a populacao e' sintetica (build_synthetic_population.py).
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

import delta_obs_newt as don  # noqa: E402  (LOCKED, so' para BIN_EDGES_LOG_GN_SPARC003)
import build_synthetic_population as bp  # noqa: E402
import selfcal_pipeline as sp  # noqa: E402

RESULTS_DIR = THIS_DIR.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

N_SYS = 8000
N_MC = 120
N_BOOTSTRAP = 400
ANCHOR_BIN = 4  # bin de maior aceleracao da grade fixa (5 bins, indice 0-4)
TOL_F_MULTI = 0.05  # criterio A1/A4 (METHODOLOGY_ADDENDUM.md Secao 3)
BIN_EDGES = don.BIN_EDGES_LOG_GN_SPARC003

# Cenarios pre-declarados: f_multi_true variados, sempre com wobble
# fotocentrico verdadeiro ativo (mecanismo mais realista/completo) e RUWE
# sintetico correlacionado (construido em build_fake_real_dataset).
SCENARIOS = [
    {"name": "f_multi_true=0.00", "f_multi_true": 0.00, "seed_cat": 9001, "seed_fake": 9002, "seed_calib": 9003},
    {"name": "f_multi_true=0.35", "f_multi_true": 0.35, "seed_cat": 9101, "seed_fake": 9102, "seed_calib": 9103},
    {"name": "f_multi_true=0.47", "f_multi_true": 0.47, "seed_cat": 9201, "seed_fake": 9202, "seed_calib": 9203},
]


def run_scenario(scn: dict) -> dict:
    t0 = time.time()
    rng_cat = np.random.default_rng(scn["seed_cat"])
    cat = bp.generate_structural_catalog(N_SYS, rng_cat)

    rng_fake = np.random.default_rng(scn["seed_fake"])
    fake = bp.build_fake_real_dataset(
        cat, f_multi_true=scn["f_multi_true"], a0_true=None,
        include_wobble_true=True, rng=rng_fake,
    )

    # ---- A3: sem correcao (f_multi=0 fixo), delta deve mostrar vies
    #      positivo detectavel (controle de que o desenho tem poder) ----
    uncorrected = sp.run_delta_obs_newt_selfcal(
        cat["s_m"], fake["v_p_fake_real"], cat["M1_cat_kg"], cat["M2_cat_kg"],
        cat["e_m"], cat["e_lo"], cat["e_hi"], cat["alpha_ecc"], cat["dpm_sig"],
        cat["d_mean_pc"], cat["e_pmRA1"], cat["e_pmRA2"], cat["e_pmDE1"], cat["e_pmDE2"],
        f_multi=0.0, bin_edges=BIN_EDGES, n_mc=N_MC, seed=scn["seed_calib"] + 1,
        include_wobble=True, n_bootstrap=N_BOOTSTRAP,
    )
    delta_uncorr = np.array(uncorrected["delta_obs_newt_primary"])
    ci_lo_uncorr = np.array(uncorrected["bootstrap"]["ci95_lo"])
    bins_significant_positive_uncorrected = (ci_lo_uncorr > 0.0).tolist()
    a3_pass = bool(
        scn["f_multi_true"] == 0.0
        or np.any(ci_lo_uncorr > 0.0)  # ao menos 1 bin com vies detectavel
    )

    # ---- Auto-calibracao (o pipeline sob teste) ----
    calib = sp.calibrate_f_multi(
        cat["s_m"], fake["v_p_fake_real"], cat["M1_cat_kg"], cat["M2_cat_kg"],
        cat["e_m"], cat["e_lo"], cat["e_hi"], cat["alpha_ecc"], cat["dpm_sig"],
        cat["d_mean_pc"], cat["e_pmRA1"], cat["e_pmRA2"], cat["e_pmDE1"], cat["e_pmDE2"],
        bin_edges=BIN_EDGES, anchor_bin=ANCHOR_BIN, n_mc=N_MC, seed=scn["seed_calib"],
        f_lo=0.0, f_hi=0.9, xtol=5e-3, include_wobble=True, n_bootstrap_final=N_BOOTSTRAP,
    )
    f_calibrated = calib["f_multi_calibrated"]
    a1_pass = bool(abs(f_calibrated - scn["f_multi_true"]) <= TOL_F_MULTI)

    fr = calib["final_result"]
    delta_corr = np.array(fr["delta_obs_newt_primary"])
    ci_lo_corr = np.array(fr["bootstrap"]["ci95_lo"])
    ci_hi_corr = np.array(fr["bootstrap"]["ci95_hi"])
    bins_ci_contains_zero = ((ci_lo_corr <= 0.0) & (ci_hi_corr >= 0.0)).tolist()
    a2_pass = bool(all(bins_ci_contains_zero))

    # ---- A4: RUWE correlacionado com has_multi_true. Nao aplicavel
    #      (N/A, tratado como PASS vacuo, nao FAIL) quando f_multi_true=0
    #      -- sem nenhum sistema com companheira injetada nesta realizacao,
    #      nao ha' grupo "com multiplicidade" para checar correlacao
    #      contra: a checagem so' faz sentido quando ha' multiplicidade
    #      verdadeira presente para o RUWE sintetico carregar sinal de. ----
    ruwe = fake["RUWE_synth"]
    has_multi = fake["has_multi_true"]
    if not has_multi.any():
        a4_pass = True
        a4_not_applicable = True
        ruwe_median_multi = None
        ruwe_median_clean = float(np.median(ruwe[~has_multi]))
    else:
        a4_not_applicable = False
        ruwe_median_multi = float(np.median(ruwe[has_multi]))
        ruwe_median_clean = float(np.median(ruwe[~has_multi])) if (~has_multi).any() else None
        a4_pass = bool(
            ruwe_median_clean is not None and ruwe_median_multi > ruwe_median_clean
        )

    elapsed = time.time() - t0
    scenario_pass = bool(a1_pass and a2_pass and a3_pass and a4_pass)

    return {
        "scenario": scn["name"],
        "f_multi_true": scn["f_multi_true"],
        "n_sys": N_SYS, "n_mc": N_MC, "n_bootstrap": N_BOOTSTRAP,
        "seeds": scn,
        "f_multi_calibrated": f_calibrated,
        "converged_bracket": calib["converged_bracket"],
        "bracket": calib["bracket"],
        "checks": {
            "A1_recover_f_multi_within_tol": {
                "pass": a1_pass, "f_multi_true": scn["f_multi_true"],
                "f_multi_calibrated": f_calibrated,
                "abs_diff": abs(f_calibrated - scn["f_multi_true"]), "tol": TOL_F_MULTI,
            },
            "A2_all_bins_ci_contain_zero_after_correction": {
                "pass": a2_pass, "delta_corrected": delta_corr.tolist(),
                "ci95_lo": ci_lo_corr.tolist(), "ci95_hi": ci_hi_corr.tolist(),
                "bins_ci_contains_zero": bins_ci_contains_zero,
            },
            "A3_uncorrected_shows_detectable_bias": {
                "pass": a3_pass, "delta_uncorrected_f_multi_0": delta_uncorr.tolist(),
                "ci95_lo_uncorrected": ci_lo_uncorr.tolist(),
                "bins_significant_positive": bins_significant_positive_uncorrected,
            },
            "A4_ruwe_correlates_with_true_multiplicity": {
                "pass": a4_pass, "not_applicable": a4_not_applicable,
                "ruwe_median_has_multi_true": ruwe_median_multi,
                "ruwe_median_clean": ruwe_median_clean,
                "frac_has_multi_true": fake["diagnostics"]["frac_has_multi_true"],
            },
        },
        "scenario_pass_all_checks": scenario_pass,
        "elapsed_seconds": elapsed,
    }


def main():
    print("=" * 78)
    print("Validacao A -- recuperacao de f_multi verdadeiro (populacao Newtoniana)")
    print("=" * 78)
    results = []
    for scn in SCENARIOS:
        print(f"\n--- Cenario: {scn['name']} ---")
        r = run_scenario(scn)
        results.append(r)
        print(f"  f_multi_true={r['f_multi_true']:.3f} -> calibrado={r['f_multi_calibrated']:.4f} "
              f"(convergiu no bracket: {r['converged_bracket']})")
        print(f"  A1 (|dif|<={TOL_F_MULTI}): {r['checks']['A1_recover_f_multi_within_tol']['pass']}")
        print(f"  A2 (todos bins CI contem 0 pos-correcao): {r['checks']['A2_all_bins_ci_contain_zero_after_correction']['pass']}")
        print(f"  A3 (sem correcao mostra vies detectavel): {r['checks']['A3_uncorrected_shows_detectable_bias']['pass']}")
        print(f"  A4 (RUWE correlaciona com multiplicidade verdadeira): {r['checks']['A4_ruwe_correlates_with_true_multiplicity']['pass']}")
        print(f"  VEREDITO DO CENARIO: {'PASS' if r['scenario_pass_all_checks'] else 'FAIL'} "
              f"({r['elapsed_seconds']:.1f}s)")

    all_pass = bool(all(r["scenario_pass_all_checks"] for r in results))
    summary = {
        "validation": "A_recover_f_multi",
        "run_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tol_f_multi": TOL_F_MULTI,
        "anchor_bin": ANCHOR_BIN,
        "bin_edges_log10_gN": BIN_EDGES.tolist(),
        "scenarios": results,
        "all_scenarios_pass": all_pass,
    }
    out_path = RESULTS_DIR / "validation_A_results.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n{'='*78}\nVEREDITO GERAL DA VALIDACAO A: {'PASS' if all_pass else 'FAIL'}")
    print(f"Resultado completo salvo em {out_path}")
    return summary


if __name__ == "__main__":
    main()
