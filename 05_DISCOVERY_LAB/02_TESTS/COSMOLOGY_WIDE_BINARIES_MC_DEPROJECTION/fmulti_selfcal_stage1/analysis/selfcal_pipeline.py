"""Pipeline de auto-calibracao de f_multi -- SPARC-FMULTI-STAGE1
(DISC-DEC-023, retomada de DISC-COSMOLOGY-MOND-SPARC-004).

Implementa o procedimento iterativo de Chae (2023) especificado
verbatim em ../PROVENANCE_CHAE_EQS.md Secao 5 e operacionalizado em
../METHODOLOGY_ADDENDUM.md Secao 2:

  1. Para um f_multi tentativo, injeta massa de companheira oculta
     (companion_injection.py, Eqs. 11-13) POR REALIZACAO MC -- a MESMA
     massa injetada e' usada para computar g_N no ramo REAL e no ramo
     MOCK daquela realizacao (Chae Sec.3.4: "masses ... fixed for both
     real data and mock data").
  2. Ramo MOCK recebe adicionalmente um boost de velocidade de wobble de
     fotocentro (Chae Sec.3.4 item 7) para o(s) componente(s) com
     companheira injetada.
  3. delta_obs-newt(bin) = mediana_real(log g/gN) - mediana_mock(log g/gN),
     pooled sobre (n_mc x sistemas do bin) -- MESMA convencao ja usada em
     ../../analysis/delta_obs_newt.py (Decisao de design 2 daquele modulo).
  4. Bisseccao sobre f_multi ate' que delta_obs-newt no bin-ancora (maior
     aceleracao da grade fixa) seja consistente com zero.

Reusa (NAO edita, so' importa) as funcoes publicas ja travadas de
../../analysis/deprojection_common.py (dc.sample_eccentricity,
dc.sample_orbital_geometry, dc.G_SI/MSUN_KG/AU_M) -- e' o mesmo padrao ja
seguido por ../../analysis/hidden_companion_check_v2.py. NAO importa nem
depende de ../../analysis/delta_obs_newt.py (que assume M_tot FIXO por
sistema atraves de todas as realizacoes MC -- incompativel com a
auto-calibracao, que exige M_tot variando POR realizacao devido a' injecao
estocastica de companheira. Ver METHODOLOGY_ADDENDUM.md Secao 1a).

NAO le nenhum arquivo de dado real desta linha (quality_filtered_sample.parquet,
hwang_eccentricity_subset.parquet, discovery_holdout_split.json) -- ver
METHODOLOGY_ADDENDUM.md Secao 5. Todas as validacoes desta pasta (Estagio 1)
usam populacoes 100% sinteticas construidas por build_synthetic_population.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

THIS_DIR = Path(__file__).resolve().parent
LOCKED_ANALYSIS_DIR = THIS_DIR.parent.parent / "analysis"
sys.path.insert(0, str(LOCKED_ANALYSIS_DIR))
import deprojection_common as dc  # noqa: E402  (arquivo LOCKED, so' importado, nunca editado)

import companion_injection as ci  # noqa: E402

G_SI = dc.G_SI
AU_M = dc.AU_M
MAS_YR_TO_KM_S_PER_PC = dc.MAS_YR_TO_KM_S_PER_PC


def nu_aqual(x: np.ndarray) -> np.ndarray:
    """nu(x) = 1/(1-exp(-sqrt(x))) -- funcao 'simple' (McGaugh, Lelli &
    Schombert 2016), identica a' ja travada em delta_obs_newt.py."""
    x = np.asarray(x, dtype=np.float64)
    return 1.0 / (1.0 - np.exp(-np.sqrt(x)))


def delta_aqual(gN_bin: np.ndarray, a0: float) -> np.ndarray:
    """delta_AQUAL(bin;a0) = log10(nu(gN_bin/a0)) -- identico ao Adendo 4c
    de PREREGISTRATION.md, reusado aqui para o ajuste de a0 da Validacao B."""
    return np.log10(nu_aqual(np.asarray(gN_bin, dtype=np.float64) / a0))


def fit_a0(gN_bin: np.ndarray, delta_vals: np.ndarray, x0: float) -> float | None:
    """Ajuste de minimos quadrados de a0 (unico parametro livre, reescalado
    a0=x*1e-10 -- licao de convergencia de SPARC-002, ja' reaplicada em
    run_primary_analysis_v2.py). Retorna None se o ajuste falhar OU se
    convergir para um a0 nao-positivo (guarda adicionada 2026-08-22 apos
    revisao adversarial -- ver ADVERSARIAL_VERIFICATION.md item 5: sem
    isso, um a0 nao-positivo geraria log10(a0_fit/a0_true)=nan silencioso,
    que comparacoes booleanas a jusante avaliariam como False em vez de
    sinalizar falha de convergencia. bootstrap_a0_refit ja' tinha este
    guarda; fit_a0 nao tinha -- agora ambos sao consistentes)."""
    from scipy.optimize import curve_fit

    def _model(gN, x):
        return delta_aqual(gN, x * 1e-10)

    try:
        popt, _ = curve_fit(_model, gN_bin, delta_vals, p0=[x0], maxfev=20000)
        a0_fit = float(popt[0]) * 1e-10
        if not np.isfinite(a0_fit) or a0_fit <= 0:
            return None
        return a0_fit
    except Exception:
        return None


# ---------------------------------------------------------------------
# Helper: desprojecao (Gap c / Eqs.7-9 de Chae) suportando v_p com uma
# dimensao extra de realizacao MC (n_mc,n_sys) -- dc.deproject so' aceita
# v_p (n_sys,) fixo por sistema, insuficiente aqui porque v_p_mock varia
# por realizacao devido a' injecao estocastica de massa/wobble.
# ---------------------------------------------------------------------

def _deproject_varying_vp(s, v_p_2d, e_sample, i, phi0, phi):
    """Identico a dc.deproject em formula (Gap c), mas aceita v_p_2d
    shape (n_mc,n_sys) em vez de (n_sys,)."""
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)
    cos_i2 = np.cos(i) ** 2
    numer = -(cos_phi + e_sample * np.cos(phi0))
    denom = sin_phi + e_sample * np.sin(phi0)
    psi = np.arctan2(numer, denom)
    cos_psi2 = np.cos(psi) ** 2
    sin_psi2 = np.sin(psi) ** 2
    r = s[None, :] / np.sqrt(cos_phi ** 2 + cos_i2 * sin_phi ** 2)
    v = v_p_2d / np.sqrt(cos_psi2 + cos_i2 * sin_psi2)
    return r, v


def _generate_outer_vp_varying_mass(s, Mtot_2d, e_sample, i, phi0, phi,
                                     a0_boost: float | None = None):
    """Mesma formula de geracao de v_p sintetico (vis-viva Newtoniana pura)
    ja usada e validada em delta_obs_newt.py::generate_synthetic_vp_newtonian,
    mas com Mtot variando por realizacao MC (shape (n_mc,n_sys) em vez de
    (n_sys,)) -- necessario porque a massa injetada de companheira oculta
    varia estocasticamente por realizacao (companion_injection.py).
    Convencao nu_true=phi_true identica, ja verificada empiricamente
    (validate_synthetic_newtonian.py, docstring de delta_obs_newt.py).
    """
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)
    cos_i2 = np.cos(i) ** 2
    r_true = s[None, :] / np.sqrt(cos_phi ** 2 + cos_i2 * sin_phi ** 2)

    nu_true = phi
    a_true = r_true * (1.0 + e_sample * np.cos(nu_true)) / (1.0 - e_sample ** 2)
    v_true_sq = G_SI * Mtot_2d * (2.0 / r_true - 1.0 / a_true)
    v_true_sq = np.clip(v_true_sq, 1e-6, None)  # protecao numerica (ver nota abaixo)
    v_true = np.sqrt(v_true_sq)

    gN_true = G_SI * Mtot_2d / r_true ** 2
    if a0_boost is not None:
        boost = np.sqrt(nu_aqual(gN_true / a0_boost))
        v_true = v_true * boost

    numer = -(cos_phi + e_sample * np.cos(phi0))
    denom = sin_phi + e_sample * np.sin(phi0)
    psi = np.arctan2(numer, denom)
    cos_psi2 = np.cos(psi) ** 2
    sin_psi2 = np.sin(psi) ** 2
    v_p_outer = v_true * np.sqrt(cos_psi2 + cos_i2 * sin_psi2)
    return v_p_outer, r_true, gN_true, psi


def astrometric_noise_sigma_v_si(pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc):
    """Identica a' ja travada em delta_obs_newt.py::astrometric_noise_sigma_v_si
    -- reimplementada aqui (formula trivial, sem dependencia de estado) para
    manter este modulo autocontido sem importar delta_obs_newt.py."""
    sigma_dmu_ra = np.sqrt(pmra_err1 ** 2 + pmra_err2 ** 2)
    sigma_dmu_de = np.sqrt(pmde_err1 ** 2 + pmde_err2 ** 2)
    to_v_si = MAS_YR_TO_KM_S_PER_PC * d_mean_pc * 1000.0
    return to_v_si * sigma_dmu_ra, to_v_si * sigma_dmu_de


def _inject_astrometric_noise(v_p_clean, sigma_v_ra_si, sigma_v_de_si, rng):
    """Decompoe em vetor 2D via angulo de posicao isotropico, injeta ruido
    Gaussiano por componente, retoma magnitude -- identico ao procedimento
    da Secao 5b/Decisao de design 4 de delta_obs_newt.py."""
    shape = v_p_clean.shape
    pa = rng.uniform(0.0, 2.0 * np.pi, size=shape)
    v_ra = v_p_clean * np.cos(pa) + rng.normal(0.0, sigma_v_ra_si, size=shape)
    v_de = v_p_clean * np.sin(pa) + rng.normal(0.0, sigma_v_de_si, size=shape)
    return np.sqrt(v_ra ** 2 + v_de ** 2)


def _wobble_component_mc(mask_2d, kappa_2d, M_component_true_2d, d_mean_pc, rng):
    """Wobble de fotocentro vetorizado sobre (n_mc,n_sys) -- mesma
    aproximacao (orbita interna circular, fase uniforme, a_in log-uniforme
    em [0.01,d_pc] UA) ja declarada e usada em hidden_companion_check_v2.py,
    agora com uma realizacao INDEPENDENTE de (a_in, fase) por MC draw."""
    shape = mask_2d.shape
    d_floor = np.maximum(d_mean_pc[None, :], 0.02)
    a_in_au = 10.0 ** rng.uniform(np.log10(0.01), np.log10(np.broadcast_to(d_floor, shape)))
    a_in_si = a_in_au * AU_M
    v_orb = np.sqrt(G_SI * M_component_true_2d / np.maximum(a_in_si, 1.0))
    beta = np.abs(ci.photocenter_beta(kappa_2d))
    speed = beta * v_orb
    phase = rng.uniform(0.0, 2.0 * np.pi, size=shape)
    sp_ra = np.where(mask_2d, speed * np.cos(phase), 0.0)
    sp_de = np.where(mask_2d, speed * np.sin(phase), 0.0)
    return sp_ra, sp_de


def generate_mock_vp(s, Mtot_true_2d, inj, e_m, e_lo, e_hi, alpha_ecc, dpm_sig,
                      d_mean_pc, rng, include_wobble: bool = True,
                      a0_boost: float | None = None):
    """Gera v_p do ramo MOCK (orbita externa via vis-viva com Mtot_true_2d
    + wobble de fotocentro opcional), n_mc = Mtot_true_2d.shape[0].
    Geometria orbital EXTERNA sorteada aqui (independente de qualquer outro
    sorteio de geometria no chamador -- mesma disciplina de independencia
    de sementes ja usada em delta_obs_newt.py)."""
    n_mc, n_sys = Mtot_true_2d.shape
    e_sample, _ = dc.sample_eccentricity(e_m, e_lo, e_hi, alpha_ecc, dpm_sig, n_mc, rng)
    i, phi0, phi = dc.sample_orbital_geometry(e_sample, rng)

    v_p_outer, r_true, gN_true, _ = _generate_outer_vp_varying_mass(
        s, Mtot_true_2d, e_sample, i, phi0, phi, a0_boost=a0_boost,
    )
    # Reconstroi as componentes RA/DE do vetor de velocidade projetado a
    # partir da magnitude v_p_outer usando um angulo de posicao isotropico
    # (a pipeline nunca rastreia orientacao fisica alem da magnitude v_p --
    # mesma justificativa de delta_obs_newt.py Decisao de design 4) --
    # necessario para somar VETORIALMENTE o wobble de fotocentro abaixo.
    pa_outer = rng.uniform(0.0, 2.0 * np.pi, size=(n_mc, n_sys))
    v_ra = v_p_outer * np.cos(pa_outer)
    v_de = v_p_outer * np.sin(pa_outer)

    frac_nonzero_wobble = 0.0
    if include_wobble:
        ra1, de1 = _wobble_component_mc(inj["mask1"], inj["kappa_1"], inj["M1_true"], d_mean_pc, rng)
        ra2, de2 = _wobble_component_mc(inj["mask2"], inj["kappa_2"], inj["M2_true"], d_mean_pc, rng)
        v_ra = v_ra + ra1 + ra2
        v_de = v_de + de1 + de2
        frac_nonzero_wobble = float((inj["mask1"] | inj["mask2"]).mean())

    v_p_mock_clean = np.sqrt(v_ra ** 2 + v_de ** 2)
    return v_p_mock_clean, {"frac_nonzero_wobble": frac_nonzero_wobble}


def run_delta_obs_newt_selfcal(
    s, v_p_real, M1_cat, M2_cat, e_m, e_lo, e_hi, alpha_ecc, dpm_sig,
    d_mean_pc, pmra_err1, pmra_err2, pmde_err1, pmde_err2,
    f_multi: float, bin_edges: np.ndarray, n_mc: int, seed: int,
    include_wobble: bool = True, real_gets_astrometric_noise: bool = False,
    n_bootstrap: int | None = None, return_raw: bool = False,
) -> dict:
    """UMA avaliacao completa de delta_obs-newt(bin; f_multi) -- Passos 1-3
    do docstring do modulo. `real_gets_astrometric_noise=False` por
    padrao porque, em dado REAL, v_p_real JA carrega ruido Gaia genuino por
    construcao (nao se re-injeta ruido em cima de dado real observado) --
    nas validacoes sinteticas desta pasta, o ruido e' injetado UMA VEZ na
    construcao do dataset sintetico "fake real" (build_synthetic_population.py),
    nao aqui. O ramo MOCK sempre recebe ruido astrometrico simetrico
    (Secao 5b, ja' travada), independente desta flag.

    Retorna delta_obs_newt por bin (estimativa pontual, pooled sobre
    n_mc x sistemas) e, se n_bootstrap for dado, IC95% bootstrap.
    """
    s = np.asarray(s, dtype=np.float64)
    v_p_real = np.asarray(v_p_real, dtype=np.float64)
    M1_cat = np.asarray(M1_cat, dtype=np.float64)
    M2_cat = np.asarray(M2_cat, dtype=np.float64)
    n_sys = s.shape[0]
    bin_edges = np.asarray(bin_edges, dtype=np.float64)
    n_bins = len(bin_edges) - 1

    rng_inj = np.random.default_rng(seed)
    rng_real_geom = np.random.default_rng(seed + 111_111_111)
    rng_mock = np.random.default_rng(seed + 222_222_222)
    rng_noise = np.random.default_rng(seed + 333_333_333)

    inj = ci.sample_companion_injection_mc(M1_cat, M2_cat, f_multi, n_mc, rng_inj)
    Mtot_true = inj["Mtot_true"]  # (n_mc, n_sys)

    # ---- binagem fixa por gN projetado usando a massa CATALOGADA (nao
    #      injetada) -- mesma convencao de assign_bins_by_projected_gN em
    #      delta_obs_newt.py: a atribuicao de bin de um sistema nao pode
    #      depender de nenhum sorteio MC nem do f_multi tentativo, senao
    #      "nenhum novo binning definido a partir do resultado" seria
    #      violado a cada trial da bisseccao. ----
    Mtot_cat = M1_cat + M2_cat
    log_gN_proj_cat = np.log10(G_SI * Mtot_cat / s ** 2)
    inner_edges = bin_edges[1:-1]
    bin_idx = np.digitize(log_gN_proj_cat, inner_edges)
    in_range = (log_gN_proj_cat >= bin_edges[0]) & (log_gN_proj_cat <= bin_edges[-1])

    # ---- ramo REAL: geometria independente, Mtot INJETADA (compartilhada
    #      com o ramo mock desta mesma realizacao) ----
    e_sample_r, _ = dc.sample_eccentricity(e_m, e_lo, e_hi, alpha_ecc, dpm_sig, n_mc, rng_real_geom)
    i_r, phi0_r, phi_r = dc.sample_orbital_geometry(e_sample_r, rng_real_geom)
    v_p_real_used = v_p_real[None, :]
    if real_gets_astrometric_noise:
        sig_ra, sig_de = astrometric_noise_sigma_v_si(pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc)
        v_p_real_used = _inject_astrometric_noise(
            np.broadcast_to(v_p_real_used, (n_mc, n_sys)).copy(), sig_ra[None, :], sig_de[None, :], rng_noise,
        )
    r_real, v_real = _deproject_varying_vp(s, np.broadcast_to(v_p_real_used, (n_mc, n_sys)),
                                            e_sample_r, i_r, phi0_r, phi_r)
    gN_real = G_SI * Mtot_true / r_real ** 2
    g_real = v_real ** 2 / r_real
    log_ratio_real = np.log10(g_real / gN_real)

    # ---- ramo MOCK: v_p gerado (vis-viva com Mtot_true + wobble opcional),
    #      ruido astrometrico simetrico (Secao 5b), depois desprojetado com
    #      geometria de RECUPERACAO independente ----
    v_p_mock_clean, mock_diag = generate_mock_vp(
        s, Mtot_true, inj, e_m, e_lo, e_hi, alpha_ecc, dpm_sig, d_mean_pc,
        rng_mock, include_wobble=include_wobble,
    )
    sig_ra, sig_de = astrometric_noise_sigma_v_si(pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc)
    v_p_mock_noisy = _inject_astrometric_noise(
        v_p_mock_clean, np.broadcast_to(sig_ra[None, :], (n_mc, n_sys)),
        np.broadcast_to(sig_de[None, :], (n_mc, n_sys)), rng_noise,
    )
    rng_mock_recovery = np.random.default_rng(seed + 444_444_444)
    e_sample_mr, _ = dc.sample_eccentricity(e_m, e_lo, e_hi, alpha_ecc, dpm_sig, n_mc, rng_mock_recovery)
    i_mr, phi0_mr, phi_mr = dc.sample_orbital_geometry(e_sample_mr, rng_mock_recovery)
    r_mock, v_mock = _deproject_varying_vp(s, v_p_mock_noisy, e_sample_mr, i_mr, phi0_mr, phi_mr)
    gN_mock = G_SI * Mtot_true / r_mock ** 2
    g_mock = v_mock ** 2 / r_mock
    log_ratio_mock = np.log10(g_mock / gN_mock)

    delta_primary = np.full(n_bins, np.nan)
    gN_bin_median = np.full(n_bins, np.nan)
    n_sys_per_bin = np.zeros(n_bins, dtype=int)
    for b in range(n_bins):
        m = in_range & (bin_idx == b)
        n_sys_per_bin[b] = int(m.sum())
        if n_sys_per_bin[b] == 0:
            continue
        delta_primary[b] = np.median(log_ratio_real[:, m]) - np.median(log_ratio_mock[:, m])
        gN_bin_median[b] = np.median(np.exp(np.log(10.0) * log_gN_proj_cat[m]))

    result = {
        "f_multi": float(f_multi),
        "n_bins": n_bins,
        "n_systems_per_bin": n_sys_per_bin.tolist(),
        "gN_bin_median_si": gN_bin_median.tolist(),
        "delta_obs_newt_primary": delta_primary.tolist(),
        "frac_has_multi": inj["frac_has_multi"],
        "frac_nonzero_wobble": mock_diag["frac_nonzero_wobble"],
    }

    if n_bootstrap:
        rng_boot = np.random.default_rng(seed + 555_555_555)
        boot_delta = np.full((n_bootstrap, n_bins), np.nan)
        for rep in range(n_bootstrap):
            resample = rng_boot.integers(0, n_sys, size=n_sys)
            mc_draw = rng_boot.integers(0, n_mc, size=n_sys)
            real_paired = log_ratio_real[mc_draw, resample]
            mock_paired = log_ratio_mock[mc_draw, resample]
            bin_idx_rs = bin_idx[resample]
            in_range_rs = in_range[resample]
            for b in range(n_bins):
                m = in_range_rs & (bin_idx_rs == b)
                if m.sum() == 0:
                    continue
                boot_delta[rep, b] = np.median(real_paired[m]) - np.median(mock_paired[m])
        result["bootstrap"] = {
            "n_bootstrap": n_bootstrap,
            "ci95_lo": np.nanpercentile(boot_delta, 2.5, axis=0).tolist(),
            "ci95_hi": np.nanpercentile(boot_delta, 97.5, axis=0).tolist(),
            "std": np.nanstd(boot_delta, axis=0).tolist(),
        }

    if return_raw:
        result["_raw"] = {
            "log_ratio_real": log_ratio_real,
            "log_ratio_mock": log_ratio_mock,
            "bin_idx": bin_idx,
            "in_range": in_range,
            "log_gN_proj_cat": log_gN_proj_cat,
            "n_sys": n_sys,
            "n_mc": n_mc,
        }

    return result


def bootstrap_a0_refit(raw: dict, n_bins: int, n_bootstrap: int, seed: int,
                        x0_list=(1.0, 5.0)) -> dict:
    """Reajusta a0 EM CADA replica de bootstrap (mesma logica de
    run_primary_analysis_v2.py Passo 5) -- recebe o dict `_raw` retornado
    por run_delta_obs_newt_selfcal(...,return_raw=True). Usado pela
    Validacao B para obter um IC95% em a0 (nao so' em delta)."""
    log_ratio_real = raw["log_ratio_real"]
    log_ratio_mock = raw["log_ratio_mock"]
    bin_idx = raw["bin_idx"]
    in_range = raw["in_range"]
    log_gN_proj_cat = raw["log_gN_proj_cat"]
    n_sys = raw["n_sys"]
    n_mc = raw["n_mc"]

    rng_boot = np.random.default_rng(seed)
    boot_a0 = {x0: np.full(n_bootstrap, np.nan) for x0 in x0_list}

    for rep in range(n_bootstrap):
        resample = rng_boot.integers(0, n_sys, size=n_sys)
        mc_draw = rng_boot.integers(0, n_mc, size=n_sys)
        real_paired = log_ratio_real[mc_draw, resample]
        mock_paired = log_ratio_mock[mc_draw, resample]
        bin_idx_r = bin_idx[resample]
        in_range_r = in_range[resample]
        logGN_r = log_gN_proj_cat[resample]

        rep_delta = np.full(n_bins, np.nan)
        rep_gN_bin = np.full(n_bins, np.nan)
        for b in range(n_bins):
            m = in_range_r & (bin_idx_r == b)
            if m.sum() == 0:
                continue
            rep_delta[b] = np.median(real_paired[m]) - np.median(mock_paired[m])
            rep_gN_bin[b] = np.median(10.0 ** logGN_r[m])

        if np.any(np.isnan(rep_delta)) or np.any(np.isnan(rep_gN_bin)):
            continue
        for x0 in x0_list:
            a0_rep = fit_a0(rep_gN_bin, rep_delta, x0=x0)
            if a0_rep is not None and np.isfinite(a0_rep) and a0_rep > 0:
                boot_a0[x0][rep] = a0_rep

    out = {}
    for x0 in x0_list:
        arr = boot_a0[x0]
        n_valid = int(np.sum(~np.isnan(arr)))
        if n_valid > 0:
            lo, hi = np.nanpercentile(arr, [2.5, 97.5])
        else:
            lo, hi = None, None
        out[f"x0={x0}"] = {
            "n_valid": n_valid, "n_bootstrap": n_bootstrap,
            "ci95_lo_si_m_s2": float(lo) if lo is not None else None,
            "ci95_hi_si_m_s2": float(hi) if hi is not None else None,
        }
    return out


def calibrate_f_multi(
    s, v_p_real, M1_cat, M2_cat, e_m, e_lo, e_hi, alpha_ecc, dpm_sig,
    d_mean_pc, pmra_err1, pmra_err2, pmde_err1, pmde_err2,
    bin_edges: np.ndarray, anchor_bin: int, n_mc: int, seed: int,
    f_lo: float = 0.0, f_hi: float = 0.9, xtol: float = 5e-4,
    include_wobble: bool = True, n_bootstrap_final: int = 400,
    return_raw: bool = False,
) -> dict:
    """Bisseccao (scipy.optimize.brentq) sobre f_multi ate' que
    delta_obs-newt(anchor_bin; f_multi) = 0 -- METHODOLOGY_ADDENDUM.md
    Secao 2, criterio verbatim do Artigo B (PROVENANCE_CHAE_EQS.md Secao 5).

    return_raw=True (adicionado 2026-08-22, revisao do rascunho de
    PREREGISTRATION_STAGE2_DRAFT.md Secao 4.5/12.4): propaga return_raw=True
    para a chamada final interna de run_delta_obs_newt_selfcal e inclui seu
    dict `_raw` no retorno (chave "final_raw"), sob a MESMA seed+777 ja'
    usada para calcular "final_result" -- elimina a necessidade de um
    chamador externo reexecutar run_delta_obs_newt_selfcal manualmente com
    uma seed reconstruida a mao para alimentar bootstrap_a0_refit, e com ela
    o risco de descasamento de semente entre o ponto central e o IC
    (identificado como o "ponto de maior risco de erro silencioso" da
    especificacao do Estagio 2). Comportamento default (return_raw=False)
    inalterado.
    """

    def point_delta_anchor(f_multi):
        out = run_delta_obs_newt_selfcal(
            s, v_p_real, M1_cat, M2_cat, e_m, e_lo, e_hi, alpha_ecc, dpm_sig,
            d_mean_pc, pmra_err1, pmra_err2, pmde_err1, pmde_err2,
            f_multi=f_multi, bin_edges=bin_edges, n_mc=n_mc, seed=seed,
            include_wobble=include_wobble, n_bootstrap=None,
        )
        return out["delta_obs_newt_primary"][anchor_bin]

    d_lo = point_delta_anchor(f_lo)
    d_hi = point_delta_anchor(f_hi)

    converged = bool(np.sign(d_lo) != np.sign(d_hi) and d_lo != 0 and d_hi != 0)
    if converged:
        f_calibrated = float(brentq(point_delta_anchor, f_lo, f_hi, xtol=xtol))
    else:
        # sem troca de sinal no bracket -- reporta o extremo mais proximo
        # de zero, sinalizado explicitamente como NAO CONVERGIDO (honesto,
        # nao força uma raiz que nao existe no intervalo declarado).
        f_calibrated = float(f_lo if abs(d_lo) < abs(d_hi) else f_hi)

    final = run_delta_obs_newt_selfcal(
        s, v_p_real, M1_cat, M2_cat, e_m, e_lo, e_hi, alpha_ecc, dpm_sig,
        d_mean_pc, pmra_err1, pmra_err2, pmde_err1, pmde_err2,
        f_multi=f_calibrated, bin_edges=bin_edges, n_mc=n_mc, seed=seed + 777,
        include_wobble=include_wobble, n_bootstrap=n_bootstrap_final,
        return_raw=return_raw,
    )

    result = {
        "f_multi_calibrated": f_calibrated,
        "converged_bracket": converged,
        "bracket": {"f_lo": f_lo, "f_hi": f_hi, "delta_anchor_at_f_lo": d_lo, "delta_anchor_at_f_hi": d_hi},
        "anchor_bin": anchor_bin,
        "final_result": final,
    }
    if return_raw:
        result["final_raw"] = final.pop("_raw")
    return result
