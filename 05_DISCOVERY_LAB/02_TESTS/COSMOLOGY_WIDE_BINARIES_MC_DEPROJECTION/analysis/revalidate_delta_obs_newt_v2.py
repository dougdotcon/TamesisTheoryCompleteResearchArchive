"""Revalidacao OBRIGATORIA da CORRECAO pos-lock da Secao 5b -- repete
EXATAMENTE os 2 controles do Adendo 4c (ja em `revalidate_delta_obs_newt.py`)
com a pipeline CORRIGIDA (ruido astrometrico simetrico agora injetado em
AMBOS os ramos sinteticos de cada controle, nao so' no ramo "real").
DISC-COSMOLOGY-MOND-SPARC-004, PREREGISTRATION.md Secao 5b,
"Revalidacao obrigatoria da correcao, ANTES de reaceitar qualquer resultado
real".

Diferenca ESTRUTURAL em relacao a `revalidate_delta_obs_newt.py` (v1):
------------------------------------------------------------------------
v1 gerava os dois lados de cada controle (o lado "real" sintetico E o lado
mock, este ultimo gerado DENTRO de `run_delta_obs_newt`) inteiramente sem
ruido astrometrico -- consistente com o Adendo 4c original, mas e' isso
exatamente que a Secao 5b identificou como a causa da assimetria
(`generate_synthetic_vp_newtonian` do ramo mock nunca carregava ruido,
enquanto o `v_p` REAL de dado de verdade carrega SEMPRE). Aqui:

  - O lado "real" sintetico de CADA controle (gerado explicitamente por
    este script, chamando `don.generate_synthetic_vp_newtonian` com
    `sigma_v_ra_si`/`sigma_v_de_si` calculados dos erros de PM REAIS por
    sistema, Secao 5b) agora carrega ruido astrometrico simetrico -- assim
    como no v1, nenhum v_p REAL observado de sistema real e' usado; so' os
    ERROS de PM (e_pmRA1/2, e_pmDE1/2) e a distancia (d_mean_pc) dos 8000
    sistemas reais da subamostra entram na conta (nao a velocidade).
  - O lado MOCK de CADA controle, gerado INTERNAMENTE por
    `don.run_delta_obs_newt` (agora chamado passando
    `pmra_err1,pmra_err2,pmde_err1,pmde_err2,d_mean_pc`), tambem carrega o
    MESMO orcamento de ruido por sistema -- a correcao da Secao 5b.

Tudo o mais (subamostra de 8000 sistemas, seed=20260818, N_MC=200,
N_BOOTSTRAP=1000, os dois controles, o criterio "noise-aware" ja usado na
primeira revalidacao) e' EXATAMENTE reaproveitado sem modificacao
conceitual -- so' os seeds de geracao dedicados dos dois controles mudam
(novos, distintos dos do v1, para nao reaproveitar por acidente a mesma
sequencia de sorteios "sem ruido" do v1 e mascarar um bug de
implementacao).

===========================================================================
Controle negativo (nulo) -- Adendo 4c item 1, com ruido simetrico (5b)
===========================================================================
Dois ensembles Newtonianos GENUINAMENTE independentes, AGORA ambos com
ruido astrometrico simetrico injetado (real E mock). Criterio: delta_obs-newt
proximo de 0 em cada um dos 5 bins, IC de 95% do bootstrap contendo 0.

===========================================================================
Controle positivo -- Adendo 4c item 2, com ruido simetrico (5b)
===========================================================================
Boost MOND explicito injetado no lado "real" sintetico (APOS o boost, ruido
astrometrico simetrico tambem injetado -- Decisao de design 4 de
delta_obs_newt.py: ruido se aplica DEPOIS do boost, sobre a velocidade
fisica ja boosted). O ramo mock, dentro de `run_delta_obs_newt`, permanece
Newtoniano puro SEM boost, mas agora TAMBEM com ruido astrometrico
simetrico injetado (a correcao 5b). Criterio: mesmo criterio noise-aware ja
usado na primeira revalidacao -- comparar o delta_obs-newt recuperado
contra o piso de ruido do PROPRIO controle negativo (desta v2, nao do v1),
nao uma razao literal ingenua.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import delta_obs_newt as don
import deprojection_common as dc

THIS_DIR = Path(__file__).resolve().parent
DATA_DIR = THIS_DIR.parent / "data"
QF_SAMPLE_PATH = (
    THIS_DIR.parent.parent / "COSMOLOGY_WIDE_BINARIES" / "data" / "quality_filtered_sample.parquet"
)
HWANG_SUBSET_PATH = DATA_DIR / "hwang_eccentricity_subset.parquet"
OUT_JSON = THIS_DIR / "revalidation_delta_obs_newt_v2.json"

# mesma subamostra/seed de validate_synthetic_newtonian.py e do v1, para
# comparabilidade direta com as validacoes anteriores (Secao 4b/4c)
N_SUBSAMPLE = 8000
SUBSAMPLE_SEED = 20260818

N_MC = 200
N_BOOTSTRAP = 1000

# Seeds de geracao do v_p "real" sintetico de CADA controle -- NOVOS,
# dedicados, distintos entre si, distintos dos seeds internos de
# run_delta_obs_newt, e distintos dos seeds usados em
# revalidate_delta_obs_newt.py (v1) -- para nao reaproveitar por acidente a
# mesma sequencia de sorteios "sem ruido" do v1.
SEED_NULL_REAL_TRUE = 511_001_001   # geometria 'verdadeira' do lado "real" -- controle negativo v2
SEED_NULL_RUN = 611_001_001         # seed passado a run_delta_obs_newt -- controle negativo v2

SEED_POS_REAL_TRUE = 512_002_002    # geometria 'verdadeira' do lado "real" -- controle positivo v2
SEED_POS_RUN = 612_002_002          # seed passado a run_delta_obs_newt -- controle positivo v2

A0_TEST = 1.2e-10  # m/s^2, McGaugh et al. 2016 -- valor de teste arbitrario, NAO H_A/H_B


def load_subsample() -> pd.DataFrame:
    qf = pd.read_parquet(QF_SAMPLE_PATH)
    hw = pd.read_parquet(HWANG_SUBSET_PATH)
    qf = qf.rename(columns={"Source1": "source_id1", "Source2": "source_id2"})
    qf["source_id1"] = qf["source_id1"].astype(np.int64)
    qf["source_id2"] = qf["source_id2"].astype(np.int64)
    merged = qf.merge(hw, on=["source_id1", "source_id2"], how="inner")
    assert len(merged) == len(qf), (
        f"cruzamento inesperado: {len(merged)} de {len(qf)}"
    )

    rng_sub = np.random.default_rng(SUBSAMPLE_SEED)
    idx = rng_sub.choice(len(merged), size=N_SUBSAMPLE, replace=False)
    idx.sort()
    sub = merged.iloc[idx].reset_index(drop=True)
    return sub


def extract_arrays(sub: pd.DataFrame):
    s_m = sub["sepAU"].to_numpy(dtype=np.float64) * dc.AU_M
    M_tot_kg = sub["Mtot_Msun"].to_numpy(dtype=np.float64) * dc.MSUN_KG
    e_m = sub["e"].to_numpy(dtype=np.float64)
    e_lo = sub["e0"].to_numpy(dtype=np.float64)
    e_hi = sub["e1"].to_numpy(dtype=np.float64)
    alpha = sub["alpha"].to_numpy(dtype=np.float64)
    dpm_sig = sub["dpm_sig"].to_numpy(dtype=np.float64)
    # ---- Secao 5b: erros de PM por componente + distancia media, usados
    #      SOMENTE para calcular o orcamento de ruido astrometrico
    #      (magnitude), NUNCA para ler nenhum v_p real observado ----
    pmra_err1 = sub["e_pmRA1"].to_numpy(dtype=np.float64)
    pmra_err2 = sub["e_pmRA2"].to_numpy(dtype=np.float64)
    pmde_err1 = sub["e_pmDE1"].to_numpy(dtype=np.float64)
    pmde_err2 = sub["e_pmDE2"].to_numpy(dtype=np.float64)
    d_mean_pc = sub["d_mean_pc"].to_numpy(dtype=np.float64)
    return (s_m, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig,
            pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc)


def run_negative_control(s_m, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig,
                          pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc):
    """Adendo 4c item 1 + correcao Secao 5b: dois ensembles Newtonianos
    independentes, AGORA ambos (real E mock) com ruido astrometrico
    simetrico injetado."""
    sigma_v_ra_si, sigma_v_de_si = don.astrometric_noise_sigma_v_si(
        pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc,
    )

    rng_real_true = np.random.default_rng(SEED_NULL_REAL_TRUE)
    v_p_real_synth, real_diag = don.generate_synthetic_vp_newtonian(
        s_m, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig, rng_real_true,
        sigma_v_ra_si=sigma_v_ra_si, sigma_v_de_si=sigma_v_de_si,
    )

    out = don.run_delta_obs_newt(
        s_m, v_p_real_synth, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig,
        pmra_err1=pmra_err1, pmra_err2=pmra_err2,
        pmde_err1=pmde_err1, pmde_err2=pmde_err2, d_mean_pc=d_mean_pc,
        n_mc=N_MC, n_bootstrap=N_BOOTSTRAP, seed=SEED_NULL_RUN,
    )

    delta = np.array(out["delta_obs_newt_primary"])
    ci_lo = np.array(out["bootstrap"]["ci95_lo"])
    ci_hi = np.array(out["bootstrap"]["ci95_hi"])
    ci_contains_zero = (ci_lo <= 0.0) & (0.0 <= ci_hi)

    out["real_side_generation"] = {
        "kind": "pure_newtonian_synthetic_plus_symmetric_astrometric_noise",
        "seed_real_true_geometry": SEED_NULL_REAL_TRUE,
        "fraction_individual_eccentricity": float(real_diag["use_individual_ecc"].mean()),
        "median_e_true": float(np.median(real_diag["e_true"])),
        "astrometric_noise_injected": real_diag["astrometric_noise_injected"],
        "snr_median": real_diag.get("snr_median"),
    }
    out["ci_contains_zero_per_bin"] = ci_contains_zero.tolist()
    out["passes_negative_control"] = bool(np.all(ci_contains_zero))
    return out


def run_positive_control(s_m, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig,
                          pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc):
    """Adendo 4c item 2 + correcao Secao 5b: boost MOND explicito injetado
    no lado 'real', ruido astrometrico simetrico injetado em AMBOS os
    lados (real E mock, este ultimo dentro de run_delta_obs_newt)."""
    sigma_v_ra_si, sigma_v_de_si = don.astrometric_noise_sigma_v_si(
        pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc,
    )

    rng_real_true = np.random.default_rng(SEED_POS_REAL_TRUE)
    v_p_real_boosted, real_diag = don.generate_synthetic_vp_newtonian(
        s_m, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig, rng_real_true,
        a0_boost=A0_TEST,
        sigma_v_ra_si=sigma_v_ra_si, sigma_v_de_si=sigma_v_de_si,
    )

    out = don.run_delta_obs_newt(
        s_m, v_p_real_boosted, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig,
        pmra_err1=pmra_err1, pmra_err2=pmra_err2,
        pmde_err1=pmde_err1, pmde_err2=pmde_err2, d_mean_pc=d_mean_pc,
        n_mc=N_MC, n_bootstrap=N_BOOTSTRAP, seed=SEED_POS_RUN,
    )

    delta_recovered = np.array(out["delta_obs_newt_primary"])
    gN_bin = np.array(out["gN_bin_median_si"])
    delta_predicted = don.delta_aqual(gN_bin, A0_TEST)

    same_sign = np.sign(delta_recovered) == np.sign(delta_predicted)
    ratio = np.divide(delta_recovered, delta_predicted,
                       out=np.full_like(delta_predicted, np.nan),
                       where=delta_predicted != 0)
    order_of_magnitude_ok = (ratio > 1.0 / 3.0) & (ratio < 3.0)

    ci_lo = np.array(out["bootstrap"]["ci95_lo"])
    ci_hi = np.array(out["bootstrap"]["ci95_hi"])
    predicted_in_ci = (ci_lo <= delta_predicted) & (delta_predicted <= ci_hi)

    out["real_side_generation"] = {
        "kind": "pure_newtonian_synthetic_plus_mond_boost_plus_symmetric_astrometric_noise",
        "seed_real_true_geometry": SEED_POS_REAL_TRUE,
        "a0_boost_test_value_si": A0_TEST,
        "fraction_individual_eccentricity": float(real_diag["use_individual_ecc"].mean()),
        "median_e_true": float(np.median(real_diag["e_true"])),
        "boost_factor_median": real_diag["boost_factor_median"],
        "boost_factor_min_max": real_diag["boost_factor_min_max"],
        "astrometric_noise_injected": real_diag["astrometric_noise_injected"],
        "snr_median": real_diag.get("snr_median"),
    }
    out["delta_aqual_predicted_a0_test"] = delta_predicted.tolist()
    out["same_sign_per_bin"] = same_sign.tolist()
    out["ratio_recovered_over_predicted_per_bin"] = ratio.tolist()
    out["order_of_magnitude_ok_per_bin"] = order_of_magnitude_ok.tolist()
    out["predicted_value_within_bootstrap_ci95_per_bin"] = predicted_in_ci.tolist()
    out["passes_positive_control"] = bool(
        np.all(same_sign) and np.all(order_of_magnitude_ok)
    )
    return out


def main():
    t0 = time.time()
    sub = load_subsample()
    print(f"[revalidate v2] subamostra: {len(sub)} sistemas (seed={SUBSAMPLE_SEED}, "
          f"mesma de validate_synthetic_newtonian.py e do v1)")
    arrays = extract_arrays(sub)

    print("\n" + "=" * 78)
    print("CONTROLE NEGATIVO v2 (nulo, ruido simetrico) -- dois ensembles "
          "Newtonianos independentes")
    print("=" * 78)
    t1 = time.time()
    neg = run_negative_control(*arrays)
    print(f"  tempo: {time.time()-t1:.1f}s")
    for b in range(neg["n_bins"]):
        print(f"  bin {b}: delta_obs-newt={neg['delta_obs_newt_primary'][b]:+.4f}  "
              f"IC95%=[{neg['bootstrap']['ci95_lo'][b]:+.4f}, {neg['bootstrap']['ci95_hi'][b]:+.4f}]  "
              f"contem 0? {neg['ci_contains_zero_per_bin'][b]}")
    print(f"  PASSA controle negativo v2? {neg['passes_negative_control']}")
    print(f"  correcao 5b aplicada ao ramo mock? "
          f"{neg['section5b_mock_astrometric_noise_correction_applied']}")

    print("\n" + "=" * 78)
    print(f"CONTROLE POSITIVO v2 (ruido simetrico) -- boost MOND injetado, "
          f"a0_teste={A0_TEST:.3e} m/s^2")
    print("=" * 78)
    t1 = time.time()
    pos = run_positive_control(*arrays)
    print(f"  tempo: {time.time()-t1:.1f}s")
    for b in range(pos["n_bins"]):
        print(f"  bin {b}: delta_obs-newt recuperado={pos['delta_obs_newt_primary'][b]:+.4f}  "
              f"delta_AQUAL previsto={pos['delta_aqual_predicted_a0_test'][b]:+.4f}  "
              f"razao={pos['ratio_recovered_over_predicted_per_bin'][b]:.3f}  "
              f"mesmo sinal? {pos['same_sign_per_bin'][b]}  "
              f"ordem de grandeza ok? {pos['order_of_magnitude_ok_per_bin'][b]}")
    print(f"  PASSA controle positivo v2 (criterio literal, bin a bin sem piso "
          f"de ruido)? {pos['passes_positive_control']}")
    print(f"  correcao 5b aplicada ao ramo mock? "
          f"{pos['section5b_mock_astrometric_noise_correction_applied']}")

    # ------------------------------------------------------------------
    # Mesmo refinamento noise-aware ja usado na primeira revalidacao
    # (v1): a0_teste=1.2e-10 so' produz sinal MOND detectavel acima do
    # piso de ruido de delta_obs-newt nos bins de MENOR gN (tipicamente
    # bin 0); nos demais o sinal previsto e' genuinamente desprezivel
    # (nu->1) e recuperar ali algo consistente com ruido/zero e' o
    # comportamento CORRETO, nao uma falha de deteccao.
    # ------------------------------------------------------------------
    delta_predicted = np.array(pos["delta_aqual_predicted_a0_test"])
    delta_recovered = np.array(pos["delta_obs_newt_primary"])
    neg_ci_lo = np.array(neg["bootstrap"]["ci95_lo"])
    neg_ci_hi = np.array(neg["bootstrap"]["ci95_hi"])
    noise_floor = (neg_ci_hi - neg_ci_lo) / 2.0

    signal_above_noise_floor = np.abs(delta_predicted) > noise_floor
    detectable_ok = np.array(pos["same_sign_per_bin"]) & np.array(pos["order_of_magnitude_ok_per_bin"])
    undetectable_ok = np.abs(delta_recovered) <= 3.0 * noise_floor

    per_bin_ok_noise_aware = np.where(signal_above_noise_floor, detectable_ok, undetectable_ok)

    pos["noise_floor_analysis"] = {
        "noise_floor_half_ci95_width_negative_control_v2_per_bin": noise_floor.tolist(),
        "signal_above_noise_floor_per_bin": signal_above_noise_floor.tolist(),
        "per_bin_ok_noise_aware": per_bin_ok_noise_aware.tolist(),
        "passes_positive_control_noise_aware": bool(np.all(per_bin_ok_noise_aware)),
        "interpretation": (
            "Mesmo criterio noise-aware da primeira revalidacao (v1), agora "
            "aplicado com o piso de ruido do controle NEGATIVO v2 (pipeline "
            "corrigida) -- razao recuperado/previsto diverge nos bins de gN "
            "alto porque delta_AQUAL previsto ali e' proximo de zero (nu->1), "
            "nao porque o metodo falhou; exige sinal/magnitude corretos so' "
            "onde ha sinal fisicamente detectavel acima do piso de ruido."
        ),
    }
    print("\n  -- Refinamento com piso de ruido v2 (ver 'noise_floor_analysis') --")
    for b in range(pos["n_bins"]):
        tag = "DETECTAVEL" if signal_above_noise_floor[b] else "abaixo do piso de ruido"
        print(f"  bin {b}: piso={noise_floor[b]:.4f}  ({tag})  ok? {per_bin_ok_noise_aware[b]}")
    print(f"  PASSA controle positivo v2 (criterio ciente do piso de ruido)? "
          f"{pos['noise_floor_analysis']['passes_positive_control_noise_aware']}")

    overall_pass_literal = bool(neg["passes_negative_control"] and pos["passes_positive_control"])
    overall_pass_noise_aware = bool(
        neg["passes_negative_control"]
        and pos["noise_floor_analysis"]["passes_positive_control_noise_aware"]
    )
    overall_pass = overall_pass_noise_aware

    print("\n" + "=" * 78)
    print(f"REVALIDACAO v2 -- SECAO 5b (criterio literal bin-a-bin): "
          f"{'PASSOU' if overall_pass_literal else 'FALHOU'}")
    print(f"REVALIDACAO v2 -- SECAO 5b (criterio ciente do piso de ruido): "
          f"{'PASSOU' if overall_pass_noise_aware else 'FALHOU'}")
    print("=" * 78)

    result = {
        "test_id": "DISC-COSMOLOGY-MOND-SPARC-004",
        "section": (
            "PREREGISTRATION.md Secao 5b -- revalidacao obrigatoria da "
            "correcao de assimetria de ruido astrometrico no ramo mock"
        ),
        "n_subsample": N_SUBSAMPLE,
        "subsample_seed": SUBSAMPLE_SEED,
        "subsample_seed_note": (
            "Mesmo seed/N de validate_synthetic_newtonian.py e de "
            "revalidate_delta_obs_newt.py (v1), reaproveitado para "
            "comparabilidade direta."
        ),
        "n_mc": N_MC,
        "n_bootstrap": N_BOOTSTRAP,
        "a0_test": A0_TEST,
        "correction_applied": True,
        "correction_description": (
            "generate_synthetic_vp_newtonian agora aceita "
            "sigma_v_ra_si/sigma_v_de_si (SI, m/s), calculados por "
            "astrometric_noise_sigma_v_si a partir dos erros de PM "
            "reportados pelo Gaia (e_pmRA1/2, e_pmDE1/2, mas/yr) e da "
            "distancia media (d_mean_pc) de CADA sistema real -- "
            "propagacao de erro padrao assumindo independencia RA/DE "
            "(colunas de correlacao nao disponiveis na subamostra "
            "commitada). O ruido e' injetado decompondo v_p sintetico num "
            "vetor 2D via angulo de posicao isotropico, somando ruido "
            "Gaussiano independente por componente, e retomando a "
            "magnitude -- exatamente o mesmo processo de medicao que "
            "gera o v_p real observado. run_delta_obs_newt agora injeta "
            "esse MESMO ruido no ramo mock (antes sempre limpo)."
        ),
        "note_no_real_vp_used": (
            "Em NENHUM momento desta revalidacao o v_p REAL observado de "
            "qualquer sistema real foi lido ou usado -- ambos os lados "
            "(real E mock) de ambos os controles sao v_p SINTETICO gerado "
            "por orbita Kepleriana Newtoniana pura, com ruido astrometrico "
            "simetrico injetado de ambos os lados (Secao 5b). Apenas "
            "separacao/massa/excentricidade/erros de PM/distancia REAIS "
            "dos 8000 sistemas da subamostra (variaveis preditoras e "
            "orcamento de ruido, nunca velocidade real observada) foram "
            "usadas."
        ),
        "negative_control": neg,
        "positive_control": pos,
        "overall_revalidation_pass_literal_criterion": overall_pass_literal,
        "overall_revalidation_pass_noise_aware_criterion": overall_pass_noise_aware,
        "overall_revalidation_pass": overall_pass,
        "wall_time_seconds": time.time() - t0,
    }

    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n[revalidate v2] resultado salvo em {OUT_JSON}")

    return result


if __name__ == "__main__":
    main()
