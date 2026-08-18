"""Checagem de multiplicidade oculta REFEITA com o sinal CORRIGIDO --
DISC-COSMOLOGY-MOND-SPARC-004, PREREGISTRATION.md Secao 5b / Secao 6.

Contexto: a checagem adversarial original (`hidden_companion_check.json/.md`)
foi feita sobre `result_primary.json` (v1, AFETADO pelo bug de assimetria de
ruido astrometrico da Secao 5b) -- sinal bruto grande (delta_obs_newt =
+0.227 a +0.047). Apos a correcao do bug (Secao 5b) e a reexecucao real
(`result_primary_v2.json`), o sinal residual real ficou MUITO menor
(delta_obs_newt = +0.1486 a +0.0430). Esta checagem REFAZ os 3 itens da
checagem adversarial original usando o sinal CORRIGIDO como alvo de
comparacao, com a pipeline CORRIGIDA (`delta_obs_newt.py` pos-Secao-5b,
ruido astrometrico simetrico nos dois ramos em TODAS as chamadas abaixo).

NAO edita delta_obs_newt.py nem deprojection_common.py -- so' CHAMA as
funcoes publicas ja travadas la (don.run_delta_obs_newt,
don.astrometric_noise_sigma_v_si, dc.sample_eccentricity,
dc.sample_orbital_geometry, dc.G_SI/MSUN_KG/AU_M/MAS_YR_TO_KM_S_PER_PC).
Confirmado via `git diff` ao final da sessao que os dois arquivos travados
permanecem intocados.

===========================================================================
Item 1 -- estimativa analitica (inflacao de massa fotometrica, Chae
Eqs. 11-13, mesmo raciocinio da checagem original, reimplementado aqui de
forma propria e ligado aos M1_Msun/M2_Msun REAIS de cada sistema, em vez de
um numero de populacao abstrato)
===========================================================================
Mecanismo: uma companheira nao resolvida faz o pipeline de massa
(relacao massa-luminosidade M(L)=L^(1/3.5), Chae Sec.2.2/3.2) interpretar a
luz combinada (estrela catalogada + companheira oculta) como se fosse uma
unica estrela -- como M(L) e' concava (expoente 1/3.5<1), a massa catalogada
SUBESTIMA a massa total verdadeira daquele componente. Para um componente
afetado com fracao de luz da sub-componente minoritaria kappa (<=0.5,
distribuicao de diferenca de magnitude Delta_M_G via lei de potencia
gamma_M=-0.7, Tokovinin 2008), o fator de inflacao e'
B(kappa)=kappa^(1/3.5)+(1-kappa)^(1/3.5)>=1, e a massa VERDADEIRA daquele
componente e' M_true = B(kappa)*M_cat.

===========================================================================
Item 2 -- teste direto RUWE alto (>1.2) vs. baixo, pipeline CORRIGIDA
===========================================================================
Reexecuta don.run_delta_obs_newt (com ruido astrometrico simetrico no ramo
mock, Secao 5b) separadamente nos dois subconjuntos de RUWE_max=max(RUWE1,
RUWE2), amostra de descoberta completa (30.203 sistemas).

===========================================================================
Item 3 -- simulacao Monte Carlo PROPRIA de injecao (mass inflation +
photocenter wobble), zero fisica MOND, varredura de f_multi em [0.25,0.47]
===========================================================================
Gera um `v_p` sintetico para um subconjunto PURAMENTE Newtoniano (zero MOND)
com a MESMA distribuicao real de massa/separacao/excentricidade/erro de PM
da amostra de descoberta real (30.203 sistemas), injetando:
  1. Inflacao de massa (Item 1 acima) -- atribuicao 40% brilhante so'/30%
     fraco so'/30% ambos (Chae Sec.3.2), kappa amostrado independentemente
     para cada componente afetado.
  2. Wobble de fotocentro -- formula padrao de astrometria binaria:
     fracao de deslocamento do fotocentro em relacao ao baricentro,
     beta = M_a/(M_a+M_b) - L_a/(L_a+L_b) (M_a,M_b massas verdadeiras da
     sub-componente nao resolvida, derivadas do MESMO kappa via
     mass-luminosity), semi-eixo interno a_in log-uniforme em
     [0.01,d_pc] UA (Belokurov et al. 2020, citado por Chae -- limite
     superior = 1 arcsec nao resolvido), orbita interna circular
     aproximada (fase uniforme, simplificacao declarada), velocidade de
     wobble = |beta|*v_orb_inner, somada VETORIALMENTE (angulo relativo
     aleatorio) ao v_p externo.
  3. O `M_tot` passado a `don.run_delta_obs_newt` (usado para g_N em AMBOS
     os ramos, real e mock -- e' o mesmo array compartilhado) e' SEMPRE a
     massa catalogada NAO-corrigida (M1_Msun+M2_Msun reais), exatamente
     como o pipeline real opera (nao sabe da companheira oculta).
  4. O v_p sintetico "real" recebe o MESMO orcamento de ruido astrometrico
     Gaussiano simetrico (por sistema, dos erros de PM reais do Gaia) que o
     ramo mock interno de don.run_delta_obs_newt tambem recebe -- replica
     fielmente o fato de que o v_p real observado tambem carrega ruido de
     medida sobre qualquer movimento verdadeiro (com ou sem wobble).

Pergunta central: existe f_multi em [0.25,0.47] cujo delta_obs_newt
sintetico (zero MOND) reproduza, DENTRO do IC 95% bootstrap, o sinal real
corrigido em TODOS os 5 bins simultaneamente?
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import delta_obs_newt as don
import deprojection_common as dc
import run_primary_analysis_v2 as rpa

THIS_DIR = Path(__file__).resolve().parent
RESULT_PRIMARY_V2_PATH = THIS_DIR / "result_primary_v2.json"
OUT_JSON = THIS_DIR / "hidden_companion_check_v2.json"
OUT_MD = THIS_DIR / "hidden_companion_check_v2.md"

RUWE_THRESHOLD = 1.2
GAMMA_M = -0.7
DELTA_MAG_RANGE = (0.01, 5.0)  # mag, cauda inferior protegida de singularidade
F_MULTI_SWEEP = [0.25, 0.30, 0.35, 0.40, 0.47]  # faixa observacional (Tokovinin 2014b,
                                                  # Riddle+2015, Moe & Stefano 2017,
                                                  # Raghavan+2010), extremos incluidos

N_MC = 200
N_BOOTSTRAP = 500  # reduzido de 1000 (analise primaria) para viabilizar 7 reexecucoes
                    # completas nesta checagem adversarial -- mesma pratica ja usada na
                    # checagem original (n_bootstrap=300 la, 500 aqui, ainda >> 100 exigido
                    # por Chae para mediana de bin bem determinada)

SEED_ITEM2_HIGH = 741852963
SEED_ITEM2_LOW = 741852964
SEED_ITEM3_BASE = 963258741  # + offset por f_multi/cenario abaixo


# ---------------------------------------------------------------------
# Item 1 + companion-mass injection (reusado pelo Item 3)
# ---------------------------------------------------------------------

def sample_delta_mag(n: int, rng: np.random.Generator) -> np.ndarray:
    """Delta_M_G ~ lei de potencia gamma_M=-0.7 (Tokovinin 2008) em
    [DELTA_MAG_RANGE], inversao de CDF fechada."""
    u = rng.random(n)
    g1 = GAMMA_M + 1.0
    lo, hi = DELTA_MAG_RANGE
    a_g1, b_g1 = lo ** g1, hi ** g1
    delta_mag = (a_g1 + u * (b_g1 - a_g1)) ** (1.0 / g1)
    return delta_mag


def sample_kappa(n: int, rng: np.random.Generator) -> np.ndarray:
    """kappa = fracao de luz da sub-componente MINORITARIA (<=0.5) de um
    par nao resolvido, derivada de Delta_M_G."""
    delta_mag = sample_delta_mag(n, rng)
    kappa = 1.0 / (1.0 + 10.0 ** (0.4 * delta_mag))
    return kappa


def B_of_kappa(kappa: np.ndarray) -> np.ndarray:
    """Fator de inflacao de massa B(kappa)=kappa^(1/3.5)+(1-kappa)^(1/3.5)>=1
    (Chae Eq.12, concavidade da relacao massa-luminosidade)."""
    return kappa ** (1.0 / 3.5) + (1.0 - kappa) ** (1.0 / 3.5)


def photocenter_beta(kappa: np.ndarray) -> np.ndarray:
    """Fracao de deslocamento fotocentro-baricentro para a sub-componente
    MINORITARIA (fracao de luz kappa): beta = fracao_de_massa - fracao_de_luz.
    """
    B = B_of_kappa(kappa)
    mass_frac_minority = kappa ** (1.0 / 3.5) / B
    return mass_frac_minority - kappa


def sample_companion_injection(M1_cat: np.ndarray, M2_cat: np.ndarray,
                                f_multi: float, rng: np.random.Generator):
    """Gap declarado da Secao 4 / checagem adversarial: decide, por
    sistema, se ha' companheira oculta (prob. f_multi), qual componente
    e' afetado (40% brilhante/30% fraco/30% ambos, Chae Sec.3.2), e
    calcula M1_true/M2_true (massa verdadeira, inflada por B(kappa))."""
    n = M1_cat.shape[0]
    u_has = rng.random(n)
    has_multi = u_has < f_multi
    u_which = rng.random(n)
    affects_bright = has_multi & (u_which < 0.40)
    affects_faint = has_multi & (u_which >= 0.40) & (u_which < 0.70)
    affects_both = has_multi & (u_which >= 0.70)

    kappa_bright = sample_kappa(n, rng)
    kappa_faint = sample_kappa(n, rng)

    mask1 = affects_bright | affects_both
    mask2 = affects_faint | affects_both

    M1_true = M1_cat.copy()
    M2_true = M2_cat.copy()
    M1_true[mask1] = M1_cat[mask1] * B_of_kappa(kappa_bright[mask1])
    M2_true[mask2] = M2_cat[mask2] * B_of_kappa(kappa_faint[mask2])

    return {
        "M1_true": M1_true, "M2_true": M2_true,
        "kappa_bright": kappa_bright, "kappa_faint": kappa_faint,
        "has_multi": has_multi,
        "affects_bright": affects_bright, "affects_faint": affects_faint,
        "affects_both": affects_both,
        "mask1": mask1, "mask2": mask2,
    }


def item1_analytic_estimate(M1_cat: np.ndarray, M2_cat: np.ndarray,
                             real_delta_obs_newt: list, seed_base: int = 13579):
    """Item 1: para cada f_multi da varredura, injeta APENAS inflacao de
    massa (sem orbita/wobble) na amostra real de M1/M2 catalogados, calcula
    o deslocamento populacional esperado em log10(g/gN) (aproximacao de
    1a ordem: g reflete a dinamica com Mtot_true, gN do pipeline usa
    Mtot_cat -- entao o deslocamento esperado e' ~log10(Mtot_true/Mtot_cat),
    aproximadamente CONSTANTE atraves dos bins, pois o mecanismo de massa
    nao depende de gN/separacao). Compara com o sinal real CORRIGIDO por
    bin."""
    Mtot_cat = M1_cat + M2_cat
    out = {}
    for f_multi in F_MULTI_SWEEP:
        rng = np.random.default_rng(seed_base + int(round(f_multi * 1000)))
        inj = sample_companion_injection(M1_cat, M2_cat, f_multi, rng)
        Mtot_true = inj["M1_true"] + inj["M2_true"]
        log10_shift = np.log10(Mtot_true / Mtot_cat)
        median_shift = float(np.median(log10_shift))
        mean_shift = float(np.mean(log10_shift))
        # NOTA (bug corrigido apos 1a execucao, 2026-08-18): a fracao do sinal
        # real coberta deve usar mean_shift, NAO median_shift. median_shift e'
        # matematicamente 0 sempre que f_multi<0.5 (menos da metade da
        # populacao tem shift!=0, e o shift dos nao-afetados e' exatamente 0
        # -- entao a MEDIANA do array de shifts por sistema e' 0 por
        # construcao, independente da magnitude do shift nos afetados). Isso
        # e' matematicamente correto mas NAO e' o proxy util para o que
        # queremos comparar: o deslocamento que a mistura de sistemas
        # afetados/nao-afetados produz na MEDIANA de log10(g/gN) da amostra
        # INTEIRA (a estatistica real de delta_obs-newt) nao e' a mediana dos
        # shifts individuais (um funcional linear-em-posicao-de-shift nao
        # comuta com a mediana) -- e' melhor aproximada pela MEDIA
        # populacional do shift, que pondera corretamente a fracao afetada
        # pela magnitude tipica do shift. Confirmado empiricamente: a
        # simulacao MC completa Item 3 "mass-only" (f_multi=0.40, sem
        # wobble) produziu delta_obs_newt~+0.03-0.05 em todos os bins,
        # batendo bem com mean_shift(f_multi=0.40)=+0.054 calculado aqui --
        # NAO com median_shift=0.0000.
        frac_of_real_per_bin = [
            (mean_shift / d) if d != 0 else None for d in real_delta_obs_newt
        ]
        out[f"{f_multi:.2f}"] = {
            "f_multi": f_multi,
            "median_log10_Mtot_true_over_cat_population": median_shift,
            "mean_log10_Mtot_true_over_cat_population": mean_shift,
            "frac_has_multi": float(inj["has_multi"].mean()),
            "interpretation": (
                "Deslocamento esperado de log10(g/gN) por inflacao de massa "
                "SOZINHA (sem wobble), populacional (MEDIA, nao mediana -- ver "
                "nota no codigo-fonte), aproximadamente constante atraves dos "
                "bins (mecanismo nao depende de gN). Validado empiricamente "
                "contra o resultado mass-only completo do Item 3."
            ),
            "fraction_of_real_delta_obs_newt_per_bin": frac_of_real_per_bin,
        }
    return out


# ---------------------------------------------------------------------
# Item 3 -- gerador de v_p sintetico com companheiras ocultas injetadas
# (mass inflation + photocenter wobble), reimplementado do zero (nao
# reaproveita don.generate_synthetic_vp_newtonian -- so' as funcoes
# publicas dc.sample_eccentricity/dc.sample_orbital_geometry, exigido
# pela mesma metodologia de desprojecao, exatamente como a checagem
# adversarial original ja fez)
# ---------------------------------------------------------------------

def generate_vp_with_hidden_companions(
    s: np.ndarray, M1_cat: np.ndarray, M2_cat: np.ndarray,
    e_m: np.ndarray, e_lo: np.ndarray, e_hi: np.ndarray,
    alpha: np.ndarray, dpm_sig: np.ndarray, d_mean_pc: np.ndarray,
    pmra_err1: np.ndarray, pmra_err2: np.ndarray,
    pmde_err1: np.ndarray, pmde_err2: np.ndarray,
    f_multi: float, rng: np.random.Generator, include_wobble: bool = True,
):
    n = s.shape[0]
    Mtot_cat = M1_cat + M2_cat

    inj = sample_companion_injection(M1_cat, M2_cat, f_multi, rng)
    Mtot_true = inj["M1_true"] + inj["M2_true"]

    # ---- orbita EXTERNA (par largo), zero fisica MOND, massa VERDADEIRA
    #      (inflada) usada na dinamica -- mesma matematica de
    #      don.generate_synthetic_vp_newtonian, reimplementada aqui porque
    #      aquela funcao so' aceita M_tot (nao M1/M2 separados) e nao
    #      suporta massa inflada por sub-componente ----
    e_true, use_individual = dc.sample_eccentricity(e_m, e_lo, e_hi, alpha, dpm_sig, 1, rng)
    i_true, phi0_true, phi_true = dc.sample_orbital_geometry(e_true, rng)

    cos_phi, sin_phi = np.cos(phi_true), np.sin(phi_true)
    cos_i2 = np.cos(i_true) ** 2
    r_true = s[None, :] / np.sqrt(cos_phi ** 2 + cos_i2 * sin_phi ** 2)

    nu_true = phi_true  # mesma convencao ja verificada em validate_synthetic_newtonian.py
    a_true = r_true * (1.0 + e_true * np.cos(nu_true)) / (1.0 - e_true ** 2)
    v_true_sq = dc.G_SI * Mtot_true[None, :] * (2.0 / r_true - 1.0 / a_true)
    if not np.all(v_true_sq > 0):
        raise RuntimeError("vis-viva produziu v^2<=0 -- orbita externa nao-fisica")
    v_true = np.sqrt(v_true_sq)

    numer = -(cos_phi + e_true * np.cos(phi0_true))
    denom = sin_phi + e_true * np.sin(phi0_true)
    psi_true = np.arctan2(numer, denom)
    cos_psi2 = np.cos(psi_true) ** 2
    sin_psi2 = np.sin(psi_true) ** 2

    v_p_outer = (v_true * np.sqrt(cos_psi2 + cos_i2 * sin_psi2))[0]

    pa_outer = rng.uniform(0.0, 2.0 * np.pi, size=n)
    v_ra = v_p_outer * np.cos(pa_outer)
    v_de = v_p_outer * np.sin(pa_outer)

    wobble_speed_total = np.zeros(n)
    frac_nonzero_wobble = 0.0

    if include_wobble:
        # ---- wobble de fotocentro para cada componente potencialmente
        #      afetado (bright/faint), somado vetorialmente com fase
        #      independente se ambos afetados -- orbita interna circular
        #      aproximada, a_in log-uniforme em [0.01,d_pc] UA (Belokurov
        #      et al. 2020 citado por Chae) ----
        def wobble_component(mask, kappa, M_true_component):
            sp_ra = np.zeros(n)
            sp_de = np.zeros(n)
            if not np.any(mask):
                return sp_ra, sp_de, np.zeros(n, dtype=bool)
            a_in_au = 10.0 ** rng.uniform(
                np.log10(0.01), np.log10(np.maximum(d_mean_pc, 0.02)), size=n
            )
            a_in_si = a_in_au * dc.AU_M
            v_orb = np.sqrt(dc.G_SI * M_true_component / np.maximum(a_in_si, 1.0))
            beta = np.abs(photocenter_beta(kappa))
            speed = beta * v_orb
            phase = rng.uniform(0.0, 2.0 * np.pi, size=n)
            sp_ra[mask] = (speed * np.cos(phase))[mask]
            sp_de[mask] = (speed * np.sin(phase))[mask]
            return sp_ra, sp_de, mask

        ra1, de1, m1 = wobble_component(inj["mask1"], inj["kappa_bright"], inj["M1_true"])
        ra2, de2, m2 = wobble_component(inj["mask2"], inj["kappa_faint"], inj["M2_true"])

        v_ra = v_ra + ra1 + ra2
        v_de = v_de + de1 + de2
        wobble_speed_total = np.sqrt((ra1 + ra2) ** 2 + (de1 + de2) ** 2)
        frac_nonzero_wobble = float((m1 | m2).mean())

    v_p_clean = np.sqrt(v_ra ** 2 + v_de ** 2)

    # ---- ruido astrometrico simetrico (mesmo orcamento real do Gaia por
    #      sistema) aplicado ao v_p "real" sintetico, exatamente como o
    #      v_p real observado ja carrega por construcao (Secao 5b) ----
    sigma_v_ra_si, sigma_v_de_si = don.astrometric_noise_sigma_v_si(
        pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc
    )
    v_ra_noisy = v_ra + rng.normal(0.0, sigma_v_ra_si, size=n)
    v_de_noisy = v_de + rng.normal(0.0, sigma_v_de_si, size=n)
    v_p_final = np.sqrt(v_ra_noisy ** 2 + v_de_noisy ** 2)

    diagnostics = {
        "n": int(n),
        "f_multi_target": float(f_multi),
        "gamma_M": float(GAMMA_M),
        "include_wobble": bool(include_wobble),
        "frac_has_multi": float(inj["has_multi"].mean()),
        "frac_affects_bright_only": float(inj["affects_bright"].mean()),
        "frac_affects_faint_only": float(inj["affects_faint"].mean()),
        "frac_affects_both": float(inj["affects_both"].mean()),
        "median_Mtot_true_over_cat": float(np.median(Mtot_true / Mtot_cat)),
        "mean_log10_Mtot_true_over_cat": float(np.mean(np.log10(Mtot_true / Mtot_cat))),
        "median_wobble_speed_km_s_population_all_incl_zero": float(np.median(wobble_speed_total) / 1000.0)
        if include_wobble else 0.0,
        "median_wobble_speed_km_s_affected_only": (
            float(np.median(wobble_speed_total[wobble_speed_total > 0]) / 1000.0)
            if include_wobble and np.any(wobble_speed_total > 0) else 0.0
        ),
        "frac_nonzero_wobble": frac_nonzero_wobble,
        "median_v_p_clean_km_s": float(np.median(v_p_clean) / 1000.0),
        "median_v_p_final_with_noise_km_s": float(np.median(v_p_final) / 1000.0),
    }

    return v_p_final, Mtot_cat, diagnostics


def run_item3_scenario(s, M1_cat, M2_cat, e_m, e_lo, e_hi, alpha, dpm_sig,
                        d_mean_pc, pmra_err1, pmra_err2, pmde_err1, pmde_err2,
                        f_multi, seed, include_wobble=True):
    rng = np.random.default_rng(seed)
    v_p_synth, Mtot_cat, diag = generate_vp_with_hidden_companions(
        s, M1_cat, M2_cat, e_m, e_lo, e_hi, alpha, dpm_sig, d_mean_pc,
        pmra_err1, pmra_err2, pmde_err1, pmde_err2, f_multi, rng,
        include_wobble=include_wobble,
    )
    result = don.run_delta_obs_newt(
        s, v_p_synth, Mtot_cat, e_m, e_lo, e_hi, alpha, dpm_sig,
        pmra_err1=pmra_err1, pmra_err2=pmra_err2,
        pmde_err1=pmde_err1, pmde_err2=pmde_err2, d_mean_pc=d_mean_pc,
        bin_edges=don.BIN_EDGES_LOG_GN_SPARC003,
        n_mc=N_MC, n_bootstrap=N_BOOTSTRAP, seed=seed + 7,
    )
    result["injection_diagnostics"] = diag
    return result


# ---------------------------------------------------------------------
# Item 2 -- RUWE alto vs. baixo, pipeline corrigida
# ---------------------------------------------------------------------

def run_ruwe_subset(mask, s, v_p_real, Mtot_cat, e_m, e_lo, e_hi, alpha, dpm_sig,
                     pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc, seed):
    return don.run_delta_obs_newt(
        s[mask], v_p_real[mask], Mtot_cat[mask],
        e_m[mask], e_lo[mask], e_hi[mask], alpha[mask], dpm_sig[mask],
        pmra_err1=pmra_err1[mask], pmra_err2=pmra_err2[mask],
        pmde_err1=pmde_err1[mask], pmde_err2=pmde_err2[mask],
        d_mean_pc=d_mean_pc[mask],
        bin_edges=don.BIN_EDGES_LOG_GN_SPARC003,
        n_mc=N_MC, n_bootstrap=N_BOOTSTRAP, seed=seed,
    )


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------

def ci_overlap(lo1, hi1, lo2, hi2):
    return (lo1 <= hi2) and (lo2 <= hi1)


def main():
    t0 = time.time()
    print("=" * 78)
    print("Checagem de multiplicidade oculta v2 (sinal CORRIGIDO) -- "
          "DISC-COSMOLOGY-MOND-SPARC-004")
    print("=" * 78)

    with open(RESULT_PRIMARY_V2_PATH) as f:
        primary_v2 = json.load(f)
    real_delta = primary_v2["official_run_delta_obs_newt_output"]["delta_obs_newt_primary"]
    real_ci_lo = primary_v2["official_run_delta_obs_newt_output"]["bootstrap"]["ci95_lo"]
    real_ci_hi = primary_v2["official_run_delta_obs_newt_output"]["bootstrap"]["ci95_hi"]
    real_g_over_gN_bin0 = primary_v2["bins"][0]["g_over_gN_real_linear"]
    print(f"\nSinal real CORRIGIDO (delta_obs_newt_primary, v2): "
          f"{[f'{x:+.4f}' for x in real_delta]}")
    print(f"g/gN real bruto bin0 = {real_g_over_gN_bin0:.4f} "
          f"(gatilho de multiplicidade: {real_g_over_gN_bin0 > 1})")

    # ------------------------------------------------------------------
    print("\n[1] Carregando amostra de descoberta (30.203 sistemas, reusa "
          "run_primary_analysis_v2.load_discovery_sample)...")
    disc, n_holdout_declared, n_holdout_confirmed = rpa.load_discovery_sample()
    n_sys = len(disc)
    v_p_real_si, dmu_mas_yr = rpa.compute_vp_real_si(disc)
    s_m = disc["sepAU"].to_numpy(dtype=np.float64) * dc.AU_M
    M1_cat = disc["M1_Msun"].to_numpy(dtype=np.float64) * dc.MSUN_KG
    M2_cat = disc["M2_Msun"].to_numpy(dtype=np.float64) * dc.MSUN_KG
    Mtot_cat = disc["Mtot_Msun"].to_numpy(dtype=np.float64) * dc.MSUN_KG
    assert np.allclose(Mtot_cat, M1_cat + M2_cat, rtol=1e-9), \
        "Mtot_Msun catalogado != M1_Msun+M2_Msun -- inconsistencia de dados"
    e_m = disc["e"].to_numpy(dtype=np.float64)
    e_lo = disc["e0"].to_numpy(dtype=np.float64)
    e_hi = disc["e1"].to_numpy(dtype=np.float64)
    alpha = disc["alpha"].to_numpy(dtype=np.float64)
    dpm_sig = disc["dpm_sig"].to_numpy(dtype=np.float64)
    pmra_err1 = disc["e_pmRA1"].to_numpy(dtype=np.float64)
    pmra_err2 = disc["e_pmRA2"].to_numpy(dtype=np.float64)
    pmde_err1 = disc["e_pmDE1"].to_numpy(dtype=np.float64)
    pmde_err2 = disc["e_pmDE2"].to_numpy(dtype=np.float64)
    d_mean_pc = disc["d_mean_pc"].to_numpy(dtype=np.float64)
    RUWE1 = disc["RUWE1"].to_numpy(dtype=np.float64)
    RUWE2 = disc["RUWE2"].to_numpy(dtype=np.float64)
    RUWE_max = np.maximum(RUWE1, RUWE2)
    print(f"    n_sys={n_sys}")

    # ==================================================================
    # ITEM 1 -- estimativa analitica
    # ==================================================================
    print("\n[2] Item 1 -- estimativa analitica de inflacao de massa "
          "(sem orbita/wobble), varredura f_multi = "
          f"{F_MULTI_SWEEP}...")
    item1 = item1_analytic_estimate(M1_cat, M2_cat, real_delta)
    for k, v in item1.items():
        print(f"    f_multi={k}: deslocamento populacional mediano de "
              f"log10(Mtot_true/Mtot_cat) = {v['median_log10_Mtot_true_over_cat_population']:+.4f} dex")

    # ==================================================================
    # ITEM 2 -- RUWE alto vs. baixo
    # ==================================================================
    print(f"\n[3] Item 2 -- RUWE_max=max(RUWE1,RUWE2), limiar={RUWE_THRESHOLD}, "
          "pipeline CORRIGIDA (ruido simetrico no ramo mock)...")
    mask_high = RUWE_max > RUWE_THRESHOLD
    mask_low = ~mask_high
    n_high, n_low = int(mask_high.sum()), int(mask_low.sum())
    print(f"    n_RUWE_alto={n_high} ({n_high/n_sys*100:.2f}%), "
          f"n_RUWE_baixo={n_low} ({n_low/n_sys*100:.2f}%)")

    t_i2a = time.time()
    result_high = run_ruwe_subset(
        mask_high, s_m, v_p_real_si, Mtot_cat, e_m, e_lo, e_hi, alpha, dpm_sig,
        pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc, SEED_ITEM2_HIGH,
    )
    print(f"    RUWE alto: delta_obs_newt = "
          f"{[f'{x:+.4f}' for x in result_high['delta_obs_newt_primary']]} "
          f"({time.time()-t_i2a:.1f}s)")

    t_i2b = time.time()
    result_low = run_ruwe_subset(
        mask_low, s_m, v_p_real_si, Mtot_cat, e_m, e_lo, e_hi, alpha, dpm_sig,
        pmra_err1, pmra_err2, pmde_err1, pmde_err2, d_mean_pc, SEED_ITEM2_LOW,
    )
    print(f"    RUWE baixo: delta_obs_newt = "
          f"{[f'{x:+.4f}' for x in result_low['delta_obs_newt_primary']]} "
          f"({time.time()-t_i2b:.1f}s)")

    diff_high_minus_low = [
        h - l for h, l in zip(result_high["delta_obs_newt_primary"], result_low["delta_obs_newt_primary"])
    ]
    ci_no_overlap = [
        not ci_overlap(result_high["bootstrap"]["ci95_lo"][b], result_high["bootstrap"]["ci95_hi"][b],
                        result_low["bootstrap"]["ci95_lo"][b], result_low["bootstrap"]["ci95_hi"][b])
        for b in range(5)
    ]
    print(f"    diferenca (alto-baixo) por bin: {[f'{x:+.4f}' for x in diff_high_minus_low]}")
    print(f"    IC95% nao se sobrepoe por bin: {ci_no_overlap}")

    # fracao RUWE alto por bin (confundidor, mesma checagem da versao anterior)
    log_gN_proj = don.projected_log_gN(s_m, Mtot_cat)
    bin_idx, in_range = don.assign_bins_by_projected_gN(log_gN_proj, don.BIN_EDGES_LOG_GN_SPARC003)
    ruwe_frac_per_bin = []
    ruwe_median_per_bin = []
    n_per_bin = []
    for b in range(5):
        m = in_range & (bin_idx == b)
        n_per_bin.append(int(m.sum()))
        ruwe_frac_per_bin.append(float(mask_high[m].mean()))
        ruwe_median_per_bin.append(float(np.median(RUWE_max[m])))
    print(f"    fracao RUWE alto por bin: {[f'{x:.4f}' for x in ruwe_frac_per_bin]}")

    # ==================================================================
    # ITEM 3 -- MC de injecao propria
    # ==================================================================
    print(f"\n[4] Item 3 -- simulacao MC propria de injecao (mass+wobble), "
          f"varredura f_multi = {F_MULTI_SWEEP}, n_mc={N_MC}, "
          f"n_bootstrap={N_BOOTSTRAP}...")
    item3 = {}
    for idx, f_multi in enumerate(F_MULTI_SWEEP):
        seed = SEED_ITEM3_BASE + idx * 10_000_019
        t_s = time.time()
        res = run_item3_scenario(
            s_m, M1_cat, M2_cat, e_m, e_lo, e_hi, alpha, dpm_sig, d_mean_pc,
            pmra_err1, pmra_err2, pmde_err1, pmde_err2, f_multi, seed,
            include_wobble=True,
        )
        elapsed_s = time.time() - t_s
        print(f"    f_multi={f_multi:.2f}: delta_obs_newt = "
              f"{[f'{x:+.4f}' for x in res['delta_obs_newt_primary']]} "
              f"({elapsed_s:.1f}s)")
        item3[f"{f_multi:.2f}"] = res

    # referencia sem wobble (mass only), f_multi=0.40, mesma pratica da checagem original
    print("    referencia mass-only (sem wobble), f_multi=0.40...")
    seed_mass_only = SEED_ITEM3_BASE + 99_000_001
    res_mass_only = run_item3_scenario(
        s_m, M1_cat, M2_cat, e_m, e_lo, e_hi, alpha, dpm_sig, d_mean_pc,
        pmra_err1, pmra_err2, pmde_err1, pmde_err2, 0.40, seed_mass_only,
        include_wobble=False,
    )
    print(f"    mass-only f_multi=0.40: delta_obs_newt = "
          f"{[f'{x:+.4f}' for x in res_mass_only['delta_obs_newt_primary']]}")

    # ---- pergunta central: existe f_multi cujo IC95% sintetico cubra o
    #      IC95% real (ou pelo menos o valor central real) em TODOS os 5
    #      bins simultaneamente? ----
    central_question = {}
    for f_multi in F_MULTI_SWEEP:
        k = f"{f_multi:.2f}"
        r = item3[k]
        overlaps_per_bin = [
            ci_overlap(r["bootstrap"]["ci95_lo"][b], r["bootstrap"]["ci95_hi"][b],
                       real_ci_lo[b], real_ci_hi[b])
            for b in range(5)
        ]
        ratio_per_bin = [
            (r["delta_obs_newt_primary"][b] / real_delta[b]) if real_delta[b] != 0 else None
            for b in range(5)
        ]
        central_question[k] = {
            "synthetic_delta_obs_newt": r["delta_obs_newt_primary"],
            "synthetic_ci95_lo": r["bootstrap"]["ci95_lo"],
            "synthetic_ci95_hi": r["bootstrap"]["ci95_hi"],
            "ci95_overlaps_real_per_bin": overlaps_per_bin,
            "all_5_bins_overlap": bool(all(overlaps_per_bin)),
            "synthetic_over_real_ratio_per_bin": ratio_per_bin,
        }
    any_f_multi_explains_all = any(
        v["all_5_bins_overlap"] for v in central_question.values()
    )
    print(f"\n    Existe f_multi em {F_MULTI_SWEEP} com IC95% sintetico "
          f"sobrepondo o IC95% real em TODOS os 5 bins? {any_f_multi_explains_all}")
    for k, v in central_question.items():
        print(f"      f_multi={k}: overlap por bin={v['ci95_overlaps_real_per_bin']}, "
              f"todos os 5? {v['all_5_bins_overlap']}")

    elapsed = time.time() - t0
    print(f"\nTempo total: {elapsed:.1f}s")

    # ------------------------------------------------------------------
    # Monta resultado
    # ------------------------------------------------------------------
    result = {
        "test_id": "DISC-COSMOLOGY-MOND-SPARC-004",
        "role": "hidden_companion_check_v2_refeito_apos_correcao_secao5b",
        "run_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "preregistration_path": "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/PREREGISTRATION.md",
        "supersedes": {
            "previous_check_path": "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/analysis/hidden_companion_check.json",
            "note": (
                "hidden_companion_check.json/.md (v1) foi calculado sobre "
                "result_primary.json (v1), AFETADO pelo bug de assimetria de "
                "ruido astrometrico (Secao 5b). Sinal bruto la' era muito maior "
                "(+0.227 a +0.047) do que o sinal corrigido usado aqui "
                "(+0.1486 a +0.0430, result_primary_v2.json). v1 e' MANTIDO sem "
                "alteracao por transparencia historica, mas suas conclusoes "
                "quantitativas (fracao do sinal explicada por multiplicidade) "
                "NAO devem mais ser usadas -- usar este arquivo (v2) em seu lugar."
            ),
        },
        "target_signal_used": {
            "source": "result_primary_v2.json (pipeline CORRIGIDA, Secao 5b)",
            "delta_obs_newt_primary": real_delta,
            "delta_obs_newt_ci95_lo": real_ci_lo,
            "delta_obs_newt_ci95_hi": real_ci_hi,
            "g_over_gN_real_linear_bin0": real_g_over_gN_bin0,
        },
        "locked_pipeline_files_used": [
            "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/analysis/delta_obs_newt.py",
            "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/analysis/deprojection_common.py",
        ],
        "locked_pipeline_files_note": (
            "Nenhum dos dois arquivos foi editado nesta checagem -- confirmado "
            "via git diff. Todas as chamadas a don.run_delta_obs_newt (itens 2 "
            "e 3) usam a versao CORRIGIDA (pos-Secao-5b) com ruido astrometrico "
            "simetrico no ramo mock (pmra_err1,pmra_err2,pmde_err1,pmde_err2,"
            "d_mean_pc sempre fornecidos)."
        ),
        "n_discovery_used": int(n_sys),
        "n_mc": N_MC,
        "n_bootstrap": N_BOOTSTRAP,
        "ruwe_threshold": RUWE_THRESHOLD,
        "f_multi_sweep": F_MULTI_SWEEP,
        "gamma_M": GAMMA_M,
        "delta_mag_range": list(DELTA_MAG_RANGE),
        "item1_analytic_mass_inflation_estimate": item1,
        "item2_ruwe_direct_test": {
            "ruwe_threshold": RUWE_THRESHOLD,
            "n_systems_ruwe_high": n_high,
            "n_systems_ruwe_low": n_low,
            "fraction_ruwe_high": n_high / n_sys,
            "ruwe_high": result_high,
            "ruwe_low": result_low,
            "delta_obs_newt_diff_high_minus_low": diff_high_minus_low,
            "ci95_no_overlap_per_bin": ci_no_overlap,
            "ruwe_high_fraction_per_bin": ruwe_frac_per_bin,
            "ruwe_median_per_bin": ruwe_median_per_bin,
            "n_systems_per_bin_full_sample": n_per_bin,
        },
        "item3_monte_carlo_injection": {k: v for k, v in item3.items()},
        "item3_mass_only_reference_f_multi_0.40": res_mass_only,
        "central_question_f_multi_explains_full_signal": {
            "definition": (
                "Para cada f_multi, verifica se o IC95% bootstrap do "
                "delta_obs_newt SINTETICO (zero MOND) se sobrepoe ao IC95% "
                "bootstrap do delta_obs_newt REAL corrigido em TODOS os 5 "
                "bins simultaneamente -- criterio formal de 'multiplicidade "
                "sozinha explica o sinal inteiro, dentro da incerteza "
                "estatistica, sem precisar de nenhum boost MOND'."
            ),
            "results_per_f_multi": central_question,
            "any_f_multi_in_range_explains_all_5_bins": any_f_multi_explains_all,
        },
        "elapsed_seconds": elapsed,
    }

    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nResultado completo salvo em {OUT_JSON}")

    return result


if __name__ == "__main__":
    main()
