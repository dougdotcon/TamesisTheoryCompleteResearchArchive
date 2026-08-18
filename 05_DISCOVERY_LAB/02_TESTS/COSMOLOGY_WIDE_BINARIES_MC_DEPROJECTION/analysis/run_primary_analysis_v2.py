"""
DISC-COSMOLOGY-MOND-SPARC-004 -- analise primaria REEXECUTADA com a
pipeline CORRIGIDA (PREREGISTRATION.md Secao 5b, "Correcao de bug pos-lock:
assimetria de ruido astrometrico no ramo mock"). Substitui
`run_primary_analysis.py` (mantido intacto, NAO sobrescrito, para
transparencia historica -- aquele resultado, `result_primary.json`, e'
DOCUMENTADAMENTE afetado pelo bug identificado em
`analysis/null_discovery_sparc004.md`: o ramo mock nunca carregava ruido
astrometrico, enquanto o ramo real carrega SEMPRE, por construcao, o erro
de medida Gaia genuino).

Diferenca UNICA em relacao a `run_primary_analysis.py`: as chamadas a
`don.run_delta_obs_newt` (oficial) e a `don.generate_synthetic_vp_newtonian`
(reproducao manual) agora recebem `pmra_err1,pmra_err2,pmde_err1,pmde_err2,
d_mean_pc` de CADA sistema real -- o ramo mock passa a carregar ruido
astrometrico Gaussiano simetrico de mesma magnitude/origem do que ja esta
embutido no `v_p_real` observado (Secao 5b / `astrometric_noise_sigma_v_si`
+ Decisao de design 4 de `delta_obs_newt.py`). O ramo REAL (v_p observado)
e' EXATAMENTE o mesmo de antes -- ja carrega ruido genuino por construcao,
nao precisa (nem pode) de ruido sintetico adicional. Todo o resto (amostra
de descoberta, 30.203 sistemas, N_MC=200, N_BOOTSTRAP=1000, seed=12345,
bordas de bin, ajuste de a0 em 2 pontos de partida, checagem de sanidade,
gatilho de multiplicidade oculta) e' IDENTICO, sem reformulacao.

Executa EXATAMENTE a estatistica de teste descrita em PREREGISTRATION.md
(Secoes 4/4c/5b) sobre a amostra de DESCOBERTA real (30.203 sistemas
binarios largos do Gaia EDR3, El-Badry, Rix & Heintz 2021, apos cortes de
qualidade + cruzamento com excentricidades de Hwang, Ting & Zakamska
2022). O holdout (12.944 sistemas) NUNCA e' lido -- so' discovery_pair_ids
e' usado, e a disjuncao com holdout_pair_ids e' verificada
programaticamente abaixo.

NAO edita deprojection_common.py (PROIBIDO) -- so' CHAMA as funcoes
publicas ja travadas la (dc.run_mc_deprojection). `delta_obs_newt.py` FOI
editado nesta sessao (autorizado pela Secao 5b) para corrigir o bug -- este
script chama as funcoes publicas atualizadas do arquivo corrigido
(don.run_delta_obs_newt, don.generate_synthetic_vp_newtonian,
don.astrometric_noise_sigma_v_si, don.projected_log_gN,
don.assign_bins_by_projected_gN, don.delta_aqual), sem modifica-las aqui.

===========================================================================
Por que a pipeline de real/mock/bootstrap e' reproduzida manualmente aqui,
alem de chamar don.run_delta_obs_newt diretamente
===========================================================================
`don.run_delta_obs_newt` (chamada abaixo, seção "Passo 3 -- chamada
oficial") retorna o resultado primario oficial (delta_obs_newt por bin,
IC95% em delta via bootstrap, contagens, diagnosticos de geracao mock) --
essa e' a chamada literal pedida pela tarefa ("Rode run_delta_obs_newt").
Mas a funcao NAO expoe as 1000 amostras de bootstrap por bin
individualmente (so' resume em percentis/media/desvio) -- e o Passo 5 da
tarefa exige reajustar a0 EM CADA replica de bootstrap para construir o
IC95% em a0 (nao em delta). Como e' PROIBIDO editar o arquivo para expor
esse array interno, este script reproduz a MESMA computacao (mesmas
sementes documentadas explicitamente no docstring de
don.run_delta_obs_newt: seed_real=seed, seed_mock_true=seed+111111111,
seed_mock_recovery=seed+222222222, seed_bootstrap=seed+333333333) chamando
SOMENTE as funcoes publicas ja travadas (dc.run_mc_deprojection,
don.generate_synthetic_vp_newtonian) -- produzindo, por construcao
deterministica (mesma semente => mesmo numpy Generator PCG64 => mesma
sequencia de sorteios), os MESMOS arrays log_g_ratio_real/mock que
don.run_delta_obs_newt computou internamente. Verificado explicitamente
abaixo (secao "Checagem cruzada") que o delta_obs_newt_primary e o IC95%
em delta recomputados aqui batem BIT-A-BIT (dentro de tolerancia de ponto
flutuante) com o retorno oficial de don.run_delta_obs_newt -- confirmando
que a reproducao e' fiel antes de usa-la para o refit de a0 por replica.

===========================================================================
Decisao de design -- gN_bin (eixo x do ajuste de a0) por replica de
bootstrap
===========================================================================
PREREGISTRATION.md Gap (e) item 3: "delta_obs-newt por bin recalculado
(mesmas bordas fixas) e a0 reajustado ... em cada replica". A atribuicao
de bin de cada SISTEMA e' fixa (Decisao de design 1 de delta_obs_newt.py,
nunca resorteada por replica), mas o valor REPRESENTATIVO de gN usado como
eixo-x do ajuste MOND por bin (gN_bin_median) e' recalculado a cada
replica a partir da mediana de gN projetado dos sistemas REAMOSTRADOS
naquele bin -- mesma formula usada na secao primaria (mediana de gN_proj
dentro do bin), agora aplicada ao array reamostrado, seguindo literalmente
a palavra "recalculado" da Secao 4c. Documentado explicitamente aqui como
decisao de implementacao (nao especificada em maior detalhe pelo
pre-registro).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

import delta_obs_newt as don
import deprojection_common as dc

THIS_DIR = Path(__file__).resolve().parent
MC_DEPROJ_DIR = THIS_DIR.parent
CWB_DIR = MC_DEPROJ_DIR.parent / "COSMOLOGY_WIDE_BINARIES"

QF_SAMPLE_PATH = CWB_DIR / "data" / "quality_filtered_sample.parquet"
SPLIT_PATH = CWB_DIR / "data" / "discovery_holdout_split.json"
HWANG_SUBSET_PATH = MC_DEPROJ_DIR / "data" / "hwang_eccentricity_subset.parquet"
OUT_JSON = THIS_DIR / "result_primary_v2.json"
RESULT_PRIMARY_V1_PATH = THIS_DIR / "result_primary.json"

# ---------------------------------------------------------------------
# Constantes exatas -- identicas as ja travadas em SPARC-002/003/004
# ---------------------------------------------------------------------
C_LIGHT = 299792458.0
H0_SI = 70.0 * 1000.0 / 3.086e22  # s^-1 (70 km/s/Mpc -> SI)
A0_A = C_LIGHT * H0_SI / (2.0 * np.pi)  # "Ponte Holografica"
A0_B = C_LIGHT * H0_SI                  # "MOND Emergence"

N_MC = 200
N_BOOTSTRAP = 1000
SEED = 12345  # mesma semente ja usada em toda a linha (revalidacao/lock)

SANITY_A0_REF = 1.2e-10  # McGaugh et al. 2016, checagem de sanidade Secao 3
SANITY_MAX_ORDER_OF_MAGNITUDE_DEVIATION = 1.0

CROSSCHECK_TOL = 1e-9  # tolerancia de ponto flutuante para checagem cruzada


# ---------------------------------------------------------------------
# Modelo MOND reescalado (licao de SPARC-002/003: reescalar a0~1e-10 para
# O(1) antes de ajustar, para evitar convergencia trivial de curve_fit)
# ---------------------------------------------------------------------

def delta_aqual_rescaled(gN_bin, x):
    """delta_AQUAL(bin; a0=x*1e-10), x adimensional O(1)."""
    a0 = x * 1e-10
    return don.delta_aqual(gN_bin, a0)


def fit_a0(gN_bin, delta_vals, x0):
    try:
        popt, _ = curve_fit(
            delta_aqual_rescaled, gN_bin, delta_vals, p0=[x0], maxfev=20000,
        )
        return float(popt[0]) * 1e-10
    except Exception:
        return None


# ---------------------------------------------------------------------
# Passo 1 -- carrega amostra de DESCOBERTA (nunca o holdout)
# ---------------------------------------------------------------------

def load_discovery_sample():
    qf = pd.read_parquet(QF_SAMPLE_PATH)
    hw = pd.read_parquet(HWANG_SUBSET_PATH)
    with open(SPLIT_PATH) as f:
        split = json.load(f)

    n_holdout_declared = split["n_holdout"]
    discovery_ids = set(split["discovery_pair_ids"])
    holdout_ids = set(split["holdout_pair_ids"])

    qf = qf.rename(columns={"Source1": "source_id1", "Source2": "source_id2"})
    qf["source_id1"] = qf["source_id1"].astype(np.int64)
    qf["source_id2"] = qf["source_id2"].astype(np.int64)

    merged = qf.merge(hw, on=["source_id1", "source_id2"], how="inner")
    if len(merged) != len(qf):
        raise RuntimeError(
            f"Cruzamento com catalogo de Hwang incompleto: {len(merged)} de "
            f"{len(qf)} sistemas de quality_filtered_sample.parquet tem "
            f"contraparte em hwang_eccentricity_subset.parquet."
        )

    pair_id = merged["source_id1"].astype(str) + "_" + merged["source_id2"].astype(str)
    mask_discovery = pair_id.isin(discovery_ids)
    mask_holdout = pair_id.isin(holdout_ids)

    disc = merged.loc[mask_discovery].reset_index(drop=True)
    disc_pair_ids = set(pair_id[mask_discovery])
    holdout_pair_ids_in_merged = set(pair_id[mask_holdout])

    # Prova programatica explicita: nenhum par usado esta no holdout, e
    # nenhum par de descoberta esta faltando (checagem de disjuncao +
    # contagem exata, nao so' confianca no merge/isin).
    if not disc_pair_ids.isdisjoint(holdout_pair_ids_in_merged):
        raise RuntimeError(
            "VIOLACAO: interseccao nao-vazia entre pares de descoberta "
            "usados e pares de holdout -- holdout selado teria sido tocado."
        )
    if len(disc) != split["n_discovery"]:
        raise RuntimeError(
            f"Contagem de descoberta nao bate: obtida {len(disc)}, "
            f"esperada {split['n_discovery']}."
        )
    if len(disc) != 30203:
        raise RuntimeError(
            f"Amostra de descoberta != 30203 (obtida {len(disc)})."
        )
    if int(mask_holdout.sum()) != n_holdout_declared:
        raise RuntimeError(
            f"Contagem de holdout no merged nao bate com o declarado: "
            f"obtida {int(mask_holdout.sum())}, esperada {n_holdout_declared} "
            f"(so' contada para verificacao, holdout NUNCA usado na analise)."
        )

    return disc, n_holdout_declared, int(mask_holdout.sum())


# ---------------------------------------------------------------------
# Passo 2 -- v_p observado real (Chae 2023 Eq. 4, ja travada em SPARC-003)
# ---------------------------------------------------------------------

def compute_vp_real_si(disc: pd.DataFrame) -> np.ndarray:
    dmu_mas_yr = np.sqrt(
        (disc["pmRA1"].to_numpy(dtype=np.float64) - disc["pmRA2"].to_numpy(dtype=np.float64)) ** 2
        + (disc["pmDE1"].to_numpy(dtype=np.float64) - disc["pmDE2"].to_numpy(dtype=np.float64)) ** 2
    )
    d_mean_pc = disc["d_mean_pc"].to_numpy(dtype=np.float64)
    v_p_km_s = dc.MAS_YR_TO_KM_S_PER_PC * dmu_mas_yr * d_mean_pc
    v_p_si = v_p_km_s * 1000.0  # km/s -> m/s (SI, unidade exigida pela pipeline)
    return v_p_si, dmu_mas_yr


def main():
    t0 = time.time()
    print("=" * 78)
    print("DISC-COSMOLOGY-MOND-SPARC-004 -- analise primaria (dado real)")
    print("=" * 78)

    # ------------------------------------------------------------------
    print("\n[1] Carregando amostra de descoberta (30.203 sistemas)...")
    disc, n_holdout_declared, n_holdout_confirmed = load_discovery_sample()
    n_sys = len(disc)
    print(f"    n_discovery carregado = {n_sys}")
    print(f"    n_holdout declarado (NUNCA lido/usado) = {n_holdout_declared}, "
          f"confirmado disjunto = {n_holdout_confirmed}")

    # ------------------------------------------------------------------
    print("\n[2] Calculando v_p observado real (Chae 2023 Eq. 4)...")
    v_p_real_si, dmu_mas_yr = compute_vp_real_si(disc)
    s_m = disc["sepAU"].to_numpy(dtype=np.float64) * dc.AU_M
    M_tot_kg = disc["Mtot_Msun"].to_numpy(dtype=np.float64) * dc.MSUN_KG
    e_m = disc["e"].to_numpy(dtype=np.float64)
    e_lo = disc["e0"].to_numpy(dtype=np.float64)
    e_hi = disc["e1"].to_numpy(dtype=np.float64)
    alpha = disc["alpha"].to_numpy(dtype=np.float64)
    dpm_sig = disc["dpm_sig"].to_numpy(dtype=np.float64)
    # ---- Secao 5b: erros de PM por componente + distancia media, usados
    #      para dar ao ramo MOCK o MESMO orcamento de ruido astrometrico
    #      que o ramo real ja carrega, por construcao, no v_p_real_si acima
    pmra_err1 = disc["e_pmRA1"].to_numpy(dtype=np.float64)
    pmra_err2 = disc["e_pmRA2"].to_numpy(dtype=np.float64)
    pmde_err1 = disc["e_pmDE1"].to_numpy(dtype=np.float64)
    pmde_err2 = disc["e_pmDE2"].to_numpy(dtype=np.float64)
    d_mean_pc_arr = disc["d_mean_pc"].to_numpy(dtype=np.float64)
    print(f"    v_p_real: mediana={np.median(v_p_real_si)/1000.0:.4f} km/s, "
          f"min={v_p_real_si.min()/1000.0:.4f}, max={v_p_real_si.max()/1000.0:.4f}")
    print(f"    dmu: mediana={np.median(dmu_mas_yr):.4f} mas/yr")
    sigma_v_ra_si_check, sigma_v_de_si_check = don.astrometric_noise_sigma_v_si(
        pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc_arr,
    )
    print(f"    [Secao 5b] sigma_v_ra (mediana) = "
          f"{np.median(sigma_v_ra_si_check)/1000.0:.4f} km/s, "
          f"sigma_v_de (mediana) = {np.median(sigma_v_de_si_check)/1000.0:.4f} km/s "
          f"-- orcamento de ruido que o ramo MOCK passa a carregar")

    # ------------------------------------------------------------------
    print(f"\n[3] Rodando don.run_delta_obs_newt (n_mc={N_MC}, "
          f"n_bootstrap={N_BOOTSTRAP}, seed={SEED}) -- chamada OFICIAL, "
          f"pipeline CORRIGIDA (Secao 5b: ramo mock agora recebe ruido "
          f"astrometrico simetrico)...")
    t_official0 = time.time()
    official = don.run_delta_obs_newt(
        s_m, v_p_real_si, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig,
        pmra_err1=pmra_err1, pmra_err2=pmra_err2,
        pmde_err1=pmde_err1, pmde_err2=pmde_err2, d_mean_pc=d_mean_pc_arr,
        bin_edges=don.BIN_EDGES_LOG_GN_SPARC003,
        n_mc=N_MC, n_bootstrap=N_BOOTSTRAP, seed=SEED,
    )
    t_official1 = time.time()
    print(f"    tempo: {t_official1 - t_official0:.1f}s")
    print(f"    n_systems_per_bin = {official['n_systems_per_bin']}")
    print(f"    delta_obs_newt_primary = {[f'{x:+.4f}' for x in official['delta_obs_newt_primary']]}")
    print(f"    median_real_log_g_ratio_primary (log10 g/gN, ANTES de subtrair mock) = "
          f"{[f'{x:+.4f}' for x in official['median_real_log_g_ratio_primary']]}")
    print(f"    IC95% delta = lo{[f'{x:+.4f}' for x in official['bootstrap']['ci95_lo']]} "
          f"hi{[f'{x:+.4f}' for x in official['bootstrap']['ci95_hi']]}")

    # ------------------------------------------------------------------
    print("\n[4] Reproduzindo a pipeline interna (mesmas sementes documentadas) "
          "para extrair delta_obs-newt POR REPLICA de bootstrap (necessario "
          "para o refit de a0 do Passo 5 -- don.run_delta_obs_newt nao expoe "
          "esse array, so' o resumo em percentis)...")
    seed_real = SEED
    seed_mock_true = SEED + 111_111_111
    seed_mock_recovery = SEED + 222_222_222
    seed_bootstrap = SEED + 333_333_333

    log_gN_proj = don.projected_log_gN(s_m, M_tot_kg)
    bin_idx, in_range = don.assign_bins_by_projected_gN(log_gN_proj, don.BIN_EDGES_LOG_GN_SPARC003)
    gN_proj = dc.G_SI * M_tot_kg / s_m ** 2

    t_repro0 = time.time()
    out_real = dc.run_mc_deprojection(
        s_m, v_p_real_si, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig,
        n_mc=N_MC, seed=seed_real,
    )
    log_g_ratio_real = out_real["log_g_ratio"]

    rng_mock_true = np.random.default_rng(seed_mock_true)
    v_p_mock, mock_diag = don.generate_synthetic_vp_newtonian(
        s_m, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig, rng_mock_true,
        sigma_v_ra_si=sigma_v_ra_si_check, sigma_v_de_si=sigma_v_de_si_check,
    )
    out_mock = dc.run_mc_deprojection(
        s_m, v_p_mock, M_tot_kg, e_m, e_lo, e_hi, alpha, dpm_sig,
        n_mc=N_MC, seed=seed_mock_recovery,
    )
    log_g_ratio_mock = out_mock["log_g_ratio"]
    t_repro1 = time.time()
    print(f"    tempo (real+mock MC): {t_repro1 - t_repro0:.1f}s")

    # ---- checagem cruzada: reproducao bate com a chamada oficial? ----
    n_bins = don.N_BINS
    delta_repro_primary = np.full(n_bins, np.nan)
    gN_bin_repro_primary = np.full(n_bins, np.nan)
    n_sys_per_bin_repro = np.zeros(n_bins, dtype=int)
    for b in range(n_bins):
        mask = in_range & (bin_idx == b)
        n_sys_per_bin_repro[b] = int(mask.sum())
        real_vals = log_g_ratio_real[:, mask]
        mock_vals = log_g_ratio_mock[:, mask]
        delta_repro_primary[b] = np.median(real_vals) - np.median(mock_vals)
        gN_bin_repro_primary[b] = np.median(gN_proj[mask])

    crosscheck_delta_ok = bool(np.allclose(
        delta_repro_primary, np.array(official["delta_obs_newt_primary"]),
        atol=CROSSCHECK_TOL, rtol=0,
    ))
    crosscheck_counts_ok = bool(
        n_sys_per_bin_repro.tolist() == official["n_systems_per_bin"]
    )
    print(f"    Checagem cruzada -- delta_obs_newt_primary reproduzido == oficial "
          f"(tol={CROSSCHECK_TOL:.0e})? {crosscheck_delta_ok}")
    print(f"    Checagem cruzada -- contagem por bin reproduzida == oficial? "
          f"{crosscheck_counts_ok}")
    if not (crosscheck_delta_ok and crosscheck_counts_ok):
        raise RuntimeError(
            "Reproducao manual da pipeline interna NAO bate com a chamada "
            "oficial de don.run_delta_obs_newt -- PARANDO (nao prosseguir "
            "com refit de a0 por bootstrap sobre uma reproducao nao-fiel). "
            "Isso indicaria um bug real na reproducao (nao na pipeline "
            "travada) -- reportar sem corrigir os arquivos travados."
        )

    # ------------------------------------------------------------------
    print(f"\n[5] Bootstrap: {N_BOOTSTRAP} replicas pareadas, reajustando a0 "
          f"em cada uma (Gap e item 3 + Passo 4 do procedimento)...")
    rng_boot = np.random.default_rng(seed_bootstrap)
    boot_delta = np.full((N_BOOTSTRAP, n_bins), np.nan)
    boot_gN_bin = np.full((N_BOOTSTRAP, n_bins), np.nan)
    boot_a0_x0_1 = np.full(N_BOOTSTRAP, np.nan)
    boot_a0_x0_5 = np.full(N_BOOTSTRAP, np.nan)
    n_failed_empty_bin = 0
    n_failed_fit_x0_1 = 0
    n_failed_fit_x0_5 = 0
    n_disagree_x0 = 0

    t_boot0 = time.time()
    for rep in range(N_BOOTSTRAP):
        resample = rng_boot.integers(0, n_sys, size=n_sys)
        mc_draw = rng_boot.integers(0, N_MC, size=n_sys)

        real_paired = log_g_ratio_real[mc_draw, resample]
        mock_paired = log_g_ratio_mock[mc_draw, resample]
        gN_proj_r = gN_proj[resample]
        bin_idx_r = bin_idx[resample]
        in_range_r = in_range[resample]

        rep_delta = np.full(n_bins, np.nan)
        rep_gN_bin = np.full(n_bins, np.nan)
        for b in range(n_bins):
            m = in_range_r & (bin_idx_r == b)
            if m.sum() == 0:
                continue
            rep_delta[b] = np.median(real_paired[m]) - np.median(mock_paired[m])
            rep_gN_bin[b] = np.median(gN_proj_r[m])

        boot_delta[rep] = rep_delta
        boot_gN_bin[rep] = rep_gN_bin

        if np.any(np.isnan(rep_delta)) or np.any(np.isnan(rep_gN_bin)):
            n_failed_empty_bin += 1
            continue

        a0_rep_1 = fit_a0(rep_gN_bin, rep_delta, x0=1.0)
        a0_rep_5 = fit_a0(rep_gN_bin, rep_delta, x0=5.0)

        if a0_rep_1 is None or not np.isfinite(a0_rep_1) or a0_rep_1 <= 0:
            n_failed_fit_x0_1 += 1
        else:
            boot_a0_x0_1[rep] = a0_rep_1

        if a0_rep_5 is None or not np.isfinite(a0_rep_5) or a0_rep_5 <= 0:
            n_failed_fit_x0_5 += 1
        else:
            boot_a0_x0_5[rep] = a0_rep_5

        if (a0_rep_1 is not None and a0_rep_5 is not None
                and np.isfinite(a0_rep_1) and np.isfinite(a0_rep_5)):
            rel_diff = abs(a0_rep_1 - a0_rep_5) / max(abs(a0_rep_1), abs(a0_rep_5), 1e-30)
            if rel_diff >= 1e-4:
                n_disagree_x0 += 1

        if (rep + 1) % 200 == 0:
            print(f"    ... {rep + 1}/{N_BOOTSTRAP} replicas concluidas")
    t_boot1 = time.time()
    print(f"    tempo bootstrap: {t_boot1 - t_boot0:.1f}s")

    # ---- checagem cruzada do IC95% em delta (deve bater com oficial) ----
    ci_lo_delta_repro = np.nanpercentile(boot_delta, 2.5, axis=0)
    ci_hi_delta_repro = np.nanpercentile(boot_delta, 97.5, axis=0)
    crosscheck_ci_ok = bool(np.allclose(
        ci_lo_delta_repro, np.array(official["bootstrap"]["ci95_lo"]), atol=CROSSCHECK_TOL, rtol=0,
    ) and np.allclose(
        ci_hi_delta_repro, np.array(official["bootstrap"]["ci95_hi"]), atol=CROSSCHECK_TOL, rtol=0,
    ))
    print(f"    Checagem cruzada -- IC95% de delta (reproduzido == oficial)? {crosscheck_ci_ok}")
    if not crosscheck_ci_ok:
        raise RuntimeError(
            "IC95% de delta_obs-newt reproduzido nao bate com o oficial de "
            "don.run_delta_obs_newt -- PARANDO, nao confiar no refit de a0 "
            "por bootstrap derivado dessa reproducao."
        )

    n_valid_x0_1 = int(np.sum(~np.isnan(boot_a0_x0_1)))
    n_valid_x0_5 = int(np.sum(~np.isnan(boot_a0_x0_5)))
    print(f"    Replicas com bin vazio: {n_failed_empty_bin}/{N_BOOTSTRAP}")
    print(f"    Replicas validas (x0=1.0): {n_valid_x0_1}/{N_BOOTSTRAP} "
          f"(falhas de fit: {n_failed_fit_x0_1})")
    print(f"    Replicas validas (x0=5.0): {n_valid_x0_5}/{N_BOOTSTRAP} "
          f"(falhas de fit: {n_failed_fit_x0_5})")
    print(f"    Replicas onde x0=1.0 e x0=5.0 discordam (rel_diff>=1e-4): {n_disagree_x0}")

    a0_ci_lo_x0_1, a0_ci_hi_x0_1 = (
        np.nanpercentile(boot_a0_x0_1, [2.5, 97.5]) if n_valid_x0_1 > 0 else (np.nan, np.nan)
    )
    a0_ci_lo_x0_5, a0_ci_hi_x0_5 = (
        np.nanpercentile(boot_a0_x0_5, [2.5, 97.5]) if n_valid_x0_5 > 0 else (np.nan, np.nan)
    )
    print(f"    IC95% a0 (bootstrap, refit x0=1.0): [{a0_ci_lo_x0_1:.6e}, {a0_ci_hi_x0_1:.6e}] m/s^2")
    print(f"    IC95% a0 (bootstrap, refit x0=5.0): [{a0_ci_lo_x0_5:.6e}, {a0_ci_hi_x0_5:.6e}] m/s^2")

    # ------------------------------------------------------------------
    print("\n[6] Ajuste principal de a0 (dado real, realizacao MC primaria) "
          "-- 2 pontos de partida...")
    gN_bin_median = np.array(official["gN_bin_median_si"])
    delta_primary = np.array(official["delta_obs_newt_primary"])

    x0_1, x0_2 = 1.0, 5.0  # a0 = 1e-10 e a0 = 5e-10
    a0_fit_1 = fit_a0(gN_bin_median, delta_primary, x0_1)
    a0_fit_2 = fit_a0(gN_bin_median, delta_primary, x0_2)

    convergence_ok = bool(
        a0_fit_1 is not None and a0_fit_2 is not None
        and np.isfinite(a0_fit_1) and np.isfinite(a0_fit_2)
        and abs(a0_fit_1 - a0_fit_2) / max(abs(a0_fit_1), abs(a0_fit_2), 1e-30) < 1e-6
    )
    print(f"    Fit com a0_0={x0_1*1e-10:.2e}: a0_fit = "
          f"{a0_fit_1:.6e} m/s^2" if a0_fit_1 is not None else "    Fit com a0_0=1e-10 FALHOU")
    print(f"    Fit com a0_0={x0_2*1e-10:.2e}: a0_fit = "
          f"{a0_fit_2:.6e} m/s^2" if a0_fit_2 is not None else "    Fit com a0_0=5e-10 FALHOU")
    print(f"    Convergencia (mesmo valor a partir de 2 p0 diferentes)? {convergence_ok}")

    a0_fit = a0_fit_1 if a0_fit_1 is not None else a0_fit_2

    # ------------------------------------------------------------------
    print("\n[7] H_A / H_B dentro do IC95% de a0 (bootstrap x0=1.0)?")
    if n_valid_x0_1 > 0:
        a0_A_survives = bool(a0_ci_lo_x0_1 <= A0_A <= a0_ci_hi_x0_1)
        a0_B_survives = bool(a0_ci_lo_x0_1 <= A0_B <= a0_ci_hi_x0_1)
    else:
        a0_A_survives = False
        a0_B_survives = False
    print(f"    a0_A (Ponte Holografica) = {A0_A:.6e} m/s^2 -> dentro do IC? {a0_A_survives}")
    print(f"    a0_B (MOND Emergence)    = {A0_B:.6e} m/s^2 -> dentro do IC? {a0_B_survives}")

    if a0_A_survives and a0_B_survives:
        verdict = "INCONCLUSIVE_BOTH_SURVIVE"
    elif a0_A_survives and not a0_B_survives:
        verdict = "H_A_SUPPORTED_H_B_FALSIFIED"
    elif a0_B_survives and not a0_A_survives:
        verdict = "H_B_SUPPORTED_H_A_FALSIFIED"
    else:
        verdict = "BOTH_FALSIFIED"
    print(f"    Veredito bruto (Secao 5, ANTES da pre-condicao de sanidade): {verdict}")

    # ------------------------------------------------------------------
    print("\n[8] Checagem de sanidade obrigatoria (Secao 3): a0_fit compativel "
          f"com {SANITY_A0_REF:.2e} m/s^2 (McGaugh et al. 2016) dentro de 1 "
          "ordem de grandeza?")
    if a0_fit is not None and a0_fit > 0:
        log_ratio_to_ref = float(abs(np.log10(a0_fit / SANITY_A0_REF)))
        sanity_pass = bool(log_ratio_to_ref <= SANITY_MAX_ORDER_OF_MAGNITUDE_DEVIATION)
    else:
        log_ratio_to_ref = None
        sanity_pass = False
    print(f"    a0_fit={a0_fit} vs a0_ref={SANITY_A0_REF:.2e} -> "
          f"|log10(razao)|={log_ratio_to_ref} -> PASSA? {sanity_pass}")
    if not sanity_pass:
        print("    *** ATENCAO: checagem de sanidade da Secao 3 FALHOU. Segundo "
              "o pre-registro, o veredito H_A/H_B NAO deve ser aceito sem "
              "investigar a causa. Resultado reportado integralmente mesmo assim. ***")

    # ------------------------------------------------------------------
    print("\n[9] Gatilho pre-declarado (Gap e, simplificacao de multiplicidade "
          "oculta) -- g/gN REAL (antes de subtrair o mock) > 1 em algum bin?")
    median_real_log_g_ratio = np.array(official["median_real_log_g_ratio_primary"])
    g_over_gN_real = 10.0 ** median_real_log_g_ratio
    bins_with_real_gt_1 = (median_real_log_g_ratio > 0.0).tolist()
    any_real_gt_1 = bool(np.any(median_real_log_g_ratio > 0.0))
    print(f"    median log10(g/gN) real por bin: {median_real_log_g_ratio.tolist()}")
    print(f"    g/gN real por bin: {g_over_gN_real.tolist()}")
    print(f"    Bins com g/gN real > 1: {bins_with_real_gt_1}")
    if any_real_gt_1:
        print("    *** GATILHO ACIONADO: g/gN real > 1 em pelo menos um bin -- "
              "checagem adversarial de multiplicidade oculta OBRIGATORIA "
              "(Secao 6 do pre-registro), a ser feita por agente separado. "
              "NAO implementada aqui. ***")
    else:
        print("    Gatilho NAO acionado (g/gN real <= 1 em todos os bins).")

    elapsed = time.time() - t0
    print(f"\nTempo total: {elapsed:.1f}s")

    # ------------------------------------------------------------------
    # Monta resultado completo
    # ------------------------------------------------------------------
    result = {
        "test_id": "DISC-COSMOLOGY-MOND-SPARC-004",
        "preregistration_path": (
            "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/PREREGISTRATION.md"
        ),
        "analysis_script": (
            "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/analysis/run_primary_analysis_v2.py"
        ),
        "supersedes": {
            "previous_result_path": (
                "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/analysis/result_primary.json"
            ),
            "note": (
                "result_primary.json (v1) e' MANTIDO sem alteracao, por "
                "transparencia historica -- documentadamente afetado pelo "
                "bug de assimetria de ruido astrometrico descrito em "
                "analysis/null_discovery_sparc004.md e corrigido conforme "
                "PREREGISTRATION.md Secao 5b. Este arquivo (result_primary_v2.json) "
                "e' o resultado com a pipeline CORRIGIDA -- substitui v1 como "
                "o resultado a ser usado para qualquer veredito H_A/H_B."
            ),
        },
        "section5b_bugfix_applied": True,
        "locked_pipeline_files_used": [
            "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/analysis/delta_obs_newt.py",
            "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/analysis/deprojection_common.py",
        ],
        "locked_pipeline_files_note": (
            "deprojection_common.py NAO foi editado (permanece PROIBIDO). "
            "delta_obs_newt.py FOI editado nesta sessao -- autorizado "
            "explicitamente pela Secao 5b do pre-registro, que ja "
            "documentava a correcao exigida (injecao de ruido astrometrico "
            "simetrico no ramo mock) como a acao correta a tomar apos a "
            "checagem adversarial ter encontrado o bug."
        ),
        "run_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note_first_time_real_vp_used": (
            "A analise primaria original (result_primary.json, v1) foi a "
            "PRIMEIRA execucao deste teste sobre v_p observado real -- toda "
            "validacao/revalidacao anterior aquele ponto "
            "(validation_synthetic_newtonian.json, "
            "revalidation_delta_obs_newt.json) usou somente v_p sintetico "
            "em AMBOS os ramos. Esta execucao (v2) reusa o MESMO v_p_real_si "
            "observado (nenhuma mudanca no ramo real -- ja carrega ruido "
            "genuino por construcao); a UNICA mudanca e' que o ramo MOCK "
            "agora tambem carrega ruido astrometrico simetrico (Secao 5b), "
            "revalidado sinteticamente em revalidation_delta_obs_newt_v2.json "
            "antes desta execucao real, conforme exigido pelo pre-registro."
        ),
        "n_discovery_used": int(n_sys),
        "n_holdout_declared_not_used": int(n_holdout_declared),
        "n_holdout_confirmed_disjoint_not_used": int(n_holdout_confirmed),
        "holdout_seal_check": (
            "Verificado programaticamente: interseccao entre pair_ids de "
            "descoberta usados e pair_ids de holdout (discovery_holdout_split.json) "
            "e' vazia; nenhum dado FISICO (velocidade, massa, separacao, "
            "excentricidade) do holdout foi lido em nenhum momento -- so' a "
            "LISTA de identificadores foi usada para a checagem de disjuncao."
        ),
        "constants": {
            "G_SI": dc.G_SI,
            "MSUN_KG": dc.MSUN_KG,
            "AU_M": dc.AU_M,
            "mas_yr_to_km_s_per_pc": dc.MAS_YR_TO_KM_S_PER_PC,
            "c_light_m_s": C_LIGHT,
            "H0_km_s_Mpc": 70.0,
            "H0_si_s^-1": H0_SI,
        },
        "vp_formula": {
            "description": (
                "v_p = 4.74047e-3 * dmu[mas/yr] * d_mean_pc[pc] (km/s), "
                "Chae (2023) Eq. 4, ja travada em SPARC-003 Secao 4. "
                "dmu = sqrt((pmRA1-pmRA2)^2 + (pmDE1-pmDE2)^2)."
            ),
            "columns_used_catalog_el_badry_2021": [
                "pmRA1", "pmRA2", "pmDE1", "pmDE2", "d_mean_pc (derivado de Plx1/Plx2)",
                "sepAU", "Mtot_Msun (derivado de Gmag1/Gmag2 via Mamajek)",
            ],
            "median_dmu_mas_yr": float(np.median(dmu_mas_yr)),
            "median_vp_real_km_s": float(np.median(v_p_real_si / 1000.0)),
            "min_vp_real_km_s": float(v_p_real_si.min() / 1000.0),
            "max_vp_real_km_s": float(v_p_real_si.max() / 1000.0),
        },
        "section5b_astrometric_noise_correction": {
            "description": (
                "Ramo MOCK (generate_synthetic_vp_newtonian, chamado "
                "internamente por don.run_delta_obs_newt) agora recebe "
                "sigma_v_ra_si/sigma_v_de_si calculados por "
                "don.astrometric_noise_sigma_v_si a partir de "
                "e_pmRA1,e_pmRA2,e_pmDE1,e_pmDE2 (mas/yr, El-Badry+2021, "
                "COLUMN_DICTIONARY.md) e d_mean_pc de CADA sistema real -- "
                "mesma propagacao de erro/conversao SI usada pelo v_p_real "
                "acima. RA/DE tratados como independentes (colunas de "
                "correlacao pmRApmDEcor1/2 nao presentes em "
                "quality_filtered_sample.parquet)."
            ),
            "columns_used": ["e_pmRA1", "e_pmRA2", "e_pmDE1", "e_pmDE2", "d_mean_pc"],
            "median_sigma_v_ra_km_s": float(np.median(sigma_v_ra_si_check) / 1000.0),
            "median_sigma_v_de_km_s": float(np.median(sigma_v_de_si_check) / 1000.0),
            "applied_to_mock_branch_confirmed": bool(
                official["section5b_mock_astrometric_noise_correction_applied"]
            ),
        },
        "a0_A_holographic_bridge": {"formula": "c*H0/(2*pi)", "value_si_m_s2": A0_A},
        "a0_B_mond_emergence": {"formula": "c*H0", "value_si_m_s2": A0_B},
        "n_bins": n_bins,
        "bin_edges_log10_gN_projected_fixed_from_sparc003": don.BIN_EDGES_LOG_GN_SPARC003.tolist(),
        "n_mc": N_MC,
        "n_bootstrap": N_BOOTSTRAP,
        "seed": SEED,
        "seeds_derived": {
            "seed_real": seed_real,
            "seed_mock_true_geometry": seed_mock_true,
            "seed_mock_recovery": seed_mock_recovery,
            "seed_bootstrap": seed_bootstrap,
        },
        "official_run_delta_obs_newt_output": official,
        "crosscheck_manual_reproduction_vs_official": {
            "delta_obs_newt_primary_matches": crosscheck_delta_ok,
            "n_systems_per_bin_matches": crosscheck_counts_ok,
            "bootstrap_ci95_delta_matches": crosscheck_ci_ok,
            "tolerance_abs": CROSSCHECK_TOL,
            "note": (
                "Confirma que a reproducao manual (necessaria para extrair "
                "delta_obs-newt POR REPLICA de bootstrap, nao exposto pelo "
                "retorno de don.run_delta_obs_newt) usando as mesmas sementes "
                "documentadas produz resultados identicos (dentro de tolerancia "
                "de ponto flutuante) aos da chamada oficial da funcao travada."
            ),
        },
        "bins": [
            {
                "bin_index": b,
                "log10_gN_range": [
                    float(don.BIN_EDGES_LOG_GN_SPARC003[b]),
                    float(don.BIN_EDGES_LOG_GN_SPARC003[b + 1]),
                ],
                "n_systems": int(official["n_systems_per_bin"][b]),
                "gN_bin_median_si_m_s2": float(official["gN_bin_median_si"][b]),
                "log10_gN_bin_median": float(np.log10(official["gN_bin_median_si"][b])),
                "median_real_log10_g_over_gN": float(official["median_real_log_g_ratio_primary"][b]),
                "median_mock_log10_g_over_gN": float(official["median_mock_log_g_ratio_primary"][b]),
                "g_over_gN_real_linear": float(10.0 ** official["median_real_log_g_ratio_primary"][b]),
                "g_over_gN_real_gt_1": bool(official["median_real_log_g_ratio_primary"][b] > 0.0),
                "delta_obs_newt_primary": float(official["delta_obs_newt_primary"][b]),
                "delta_obs_newt_ci95_lo": float(official["bootstrap"]["ci95_lo"][b]),
                "delta_obs_newt_ci95_hi": float(official["bootstrap"]["ci95_hi"][b]),
            }
            for b in range(n_bins)
        ],
        "fit_a0_primary": {
            "model": "delta_AQUAL(bin;a0) = log10(nu(gN_bin/a0)), nu(x)=1/(1-exp(-sqrt(x)))",
            "rescaling": "a0 = x * 1e-10, ajustado em x (licao de convergencia de SPARC-002)",
            "convergence_check": {
                "x0_1": x0_1,
                "a0_0_1_si": x0_1 * 1e-10,
                "a0_fit_from_x0_1_si_m_s2": a0_fit_1,
                "x0_2": x0_2,
                "a0_0_2_si": x0_2 * 1e-10,
                "a0_fit_from_x0_2_si_m_s2": a0_fit_2,
                "converged_to_same_value": convergence_ok,
            },
            "a0_fit_si_m_s2": a0_fit,
            "a0_fit_x1e-10_units": (a0_fit / 1e-10) if a0_fit is not None else None,
        },
        "bootstrap_a0_refit": {
            "n_bootstrap": N_BOOTSTRAP,
            "n_replicas_failed_empty_bin": int(n_failed_empty_bin),
            "gN_bin_recomputed_per_replica": True,
            "gN_bin_recompute_note": (
                "gN_bin (eixo-x do ajuste MOND por bin) recalculado a cada "
                "replica como mediana de gN projetado dos sistemas REAMOSTRADOS "
                "naquele bin -- decisao de implementacao documentada no "
                "docstring deste script (a atribuicao de bin por sistema e' "
                "fixa, Design Decision 1 de delta_obs_newt.py, mas o valor "
                "representativo de gN do bin varia com a reamostragem)."
            ),
            "refit_x0_1p0": {
                "a0_0_si": 1.0e-10,
                "n_valid_replicas": n_valid_x0_1,
                "n_failed_fit": int(n_failed_fit_x0_1),
                "ci95_lo_si_m_s2": float(a0_ci_lo_x0_1) if n_valid_x0_1 > 0 else None,
                "ci95_hi_si_m_s2": float(a0_ci_hi_x0_1) if n_valid_x0_1 > 0 else None,
                "mean_si_m_s2": float(np.nanmean(boot_a0_x0_1)) if n_valid_x0_1 > 0 else None,
                "std_si_m_s2": float(np.nanstd(boot_a0_x0_1)) if n_valid_x0_1 > 0 else None,
            },
            "refit_x0_5p0": {
                "a0_0_si": 5.0e-10,
                "n_valid_replicas": n_valid_x0_5,
                "n_failed_fit": int(n_failed_fit_x0_5),
                "ci95_lo_si_m_s2": float(a0_ci_lo_x0_5) if n_valid_x0_5 > 0 else None,
                "ci95_hi_si_m_s2": float(a0_ci_hi_x0_5) if n_valid_x0_5 > 0 else None,
                "mean_si_m_s2": float(np.nanmean(boot_a0_x0_5)) if n_valid_x0_5 > 0 else None,
                "std_si_m_s2": float(np.nanstd(boot_a0_x0_5)) if n_valid_x0_5 > 0 else None,
            },
            "n_replicas_x0_disagreement": int(n_disagree_x0),
            "primary_ci_used_for_decision": "refit_x0_1p0 (consistente com x0 primario usado no fit principal)",
        },
        "decision": {
            "a0_ci95_used_lo_si_m_s2": float(a0_ci_lo_x0_1) if n_valid_x0_1 > 0 else None,
            "a0_ci95_used_hi_si_m_s2": float(a0_ci_hi_x0_1) if n_valid_x0_1 > 0 else None,
            "a0_A_within_ci95": a0_A_survives,
            "a0_B_within_ci95": a0_B_survives,
            "verdict_section5_raw": verdict,
            "verdict_note": (
                "Veredito bruto calculado conforme Secao 5, mas NAO deve ser "
                "aceito como final se a pre-condicao de sanidade (Secao 3/4b) "
                "abaixo falhar -- mesma regra ja usada em SPARC-002/003. "
                "Reexecucao adversarial independente (Secao 6) ainda pendente "
                "antes de catalogar qualquer resultado."
            ),
        },
        "sanity_check_section3": {
            "reference_a0_mcgaugh2016_si_m_s2": SANITY_A0_REF,
            "a0_fit_si_m_s2": a0_fit,
            "abs_log10_ratio_fit_to_reference": log_ratio_to_ref,
            "passes_within_one_order_of_magnitude": sanity_pass,
        },
        "adversarial_trigger_hidden_multiplicity": {
            "description": (
                "Gap (e) / simplificacao declarada da Secao 4: se g/gN REAL "
                "(mediana, ANTES de subtrair o mock) vier > 1 de forma "
                "consistente em algum bin, isso e' o gatilho pre-declarado "
                "para a checagem adversarial obrigatoria de multiplicidade "
                "oculta (f_multi nao corrigida, Secao 6) -- NAO implementada "
                "aqui, delegada a agente adversarial separado."
            ),
            "median_real_log10_g_over_gN_per_bin": median_real_log_g_ratio.tolist(),
            "g_over_gN_real_linear_per_bin": g_over_gN_real.tolist(),
            "bins_with_g_over_gN_real_gt_1": bins_with_real_gt_1,
            "any_bin_triggers_adversarial_check": any_real_gt_1,
        },
        "eccentricity_sampling_diagnostics": {
            "fraction_individual_eccentricity_real_branch": float(out_real["use_individual_ecc"].mean()),
            "fraction_individual_eccentricity_mock_branch_true_geometry": float(
                mock_diag["use_individual_ecc"].mean()
            ),
            "note": (
                "Fracao de sistemas que usaram a Gaussiana truncada individual "
                "de Hwang (dpm_sig>3, e/e0/e1 validos, e<0.99) em vez do "
                "fallback populacional p(e;alpha) -- Gap (a) da Secao 4."
            ),
        },
        "elapsed_seconds": elapsed,
    }

    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nResultado completo salvo em {OUT_JSON}")

    return result


if __name__ == "__main__":
    main()
