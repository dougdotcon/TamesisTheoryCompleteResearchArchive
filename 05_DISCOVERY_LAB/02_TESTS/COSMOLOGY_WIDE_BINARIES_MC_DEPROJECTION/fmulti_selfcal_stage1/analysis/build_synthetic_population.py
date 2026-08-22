"""Construtor de populacao sintetica -- SPARC-FMULTI-STAGE1.

NAO le nenhum arquivo de dado real desta linha (parquet/json do catalogo
El-Badry/Hwang) -- ver METHODOLOGY_ADDENDUM.md Secao 5. Toda a estrutura
(massa, separacao, distancia, erro de PM, excentricidade) e' sorteada de
distribuicoes parametricas documentadas abaixo, escolhidas para refletir a
ORDEM DE GRANDEZA e os CORTES DE QUALIDADE ja caracterizados pelas sessoes
anteriores desta linha (200<sepAU<30000, distancia<200pc, 4<M_G<14 =>
M~0.1-1.2 Msun aproximadamente via a relacao massa-magnitude ja usada),
sem ler o catalogo real em si.

Separa duas responsabilidades:
  1. `generate_structural_catalog` -- so' as colunas ESTRUTURAIS (massa,
     separacao, distancia, erros de PM, parametros de excentricidade) --
     nenhuma velocidade, nenhuma "verdade" de multiplicidade ainda.
  2. `build_fake_real_dataset` -- constroi o v_p "observado" sintetico UMA
     VEZ (uma realizacao GEOMETRICA e de INJECAO DE COMPANHEIRA fixas, "a
     verdade da natureza" para esta validacao), com f_multi_true e
     a0_true (opcional) conhecidos e ESCONDIDOS do pipeline de
     auto-calibracao (que nunca ve' has_multi_true/M*_true diretamente,
     so' o v_p_fake_real resultante -- exatamente como o pipeline real
     nunca sabe quais sistemas reais tem companheiras ocultas).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))
LOCKED_ANALYSIS_DIR = THIS_DIR.parent.parent / "analysis"
sys.path.insert(0, str(LOCKED_ANALYSIS_DIR))

import deprojection_common as dc  # noqa: E402
import companion_injection as ci  # noqa: E402
import selfcal_pipeline as sp  # noqa: E402

MSUN_KG = dc.MSUN_KG
AU_M = dc.AU_M


def generate_structural_catalog(n_sys: int, rng: np.random.Generator) -> dict:
    """Colunas estruturais sinteticas -- ver docstring do modulo para a
    justificativa de cada faixa. Nenhuma velocidade/massa "verdadeira"
    (com companheira) e' decidida aqui -- so' o catalogado/observavel."""
    # massa catalogada por componente: log-uniforme em [0.1,1.2] Msun,
    # aproximando a faixa 4<M_G<14 ja usada como corte de qualidade nesta
    # linha (simplificacao declarada -- nao e' a IMF real, so' cobre a
    # ordem de grandeza e a faixa).
    M1_cat_Msun = 10.0 ** rng.uniform(np.log10(0.1), np.log10(1.2), n_sys)
    M2_cat_Msun = 10.0 ** rng.uniform(np.log10(0.1), np.log10(1.2), n_sys)

    # separacao projetada: log-uniforme em [200,30000] AU (mesmo corte
    # 200<sepAU<30000 ja usado nos cortes de qualidade desta linha).
    sepAU = 10.0 ** rng.uniform(np.log10(200.0), np.log10(30000.0), n_sys)

    # distancia media: log-uniforme em [15,200] pc (corte <200pc ja usado).
    d_mean_pc = 10.0 ** rng.uniform(np.log10(15.0), np.log10(200.0), n_sys)

    # erros de PM por componente (mas/yr): log-normal, mediana ~0.035 mas/yr,
    # dispersao moderada -- ordem de grandeza tipica de erro de PM Gaia EDR3
    # para a faixa de magnitude/distancia da amostra "clean" ja caracterizada
    # (nao lida do catalogo real -- valor de referencia documentado como
    # aproximacao, nao medido).
    def _pm_err():
        return np.clip(rng.lognormal(mean=np.log(0.035), sigma=0.45, size=n_sys), 0.003, 0.5)

    e_pmRA1, e_pmRA2 = _pm_err(), _pm_err()
    e_pmDE1, e_pmDE2 = _pm_err(), _pm_err()

    # excentricidade: forca o ramo FALLBACK POPULACIONAL de
    # dc.sample_eccentricity (e_m/e_lo/e_hi = NaN, dpm_sig=0<3) --
    # p(e;alpha)=(1+alpha)*e^alpha, alpha=1.3 fixo (valor assintotico que
    # o proprio Chae reporta para s>1kau -- Secao 3.1 do Artigo A, ja'
    # verificado por fetch nesta sessao). Simplificacao declarada: nao
    # reproduz a dependencia alpha(s) completa de Hwang, nem o ramo de
    # excentricidade individual (dpm_sig>3) -- irrelevante para o que esta
    # validacao mede (recuperacao de f_multi/a0, nao o Gap (a) de
    # excentricidade, ja validado em outras sessoes desta linha).
    e_m = np.full(n_sys, np.nan)
    e_lo = np.full(n_sys, np.nan)
    e_hi = np.full(n_sys, np.nan)
    dpm_sig = np.zeros(n_sys)
    alpha_ecc = np.full(n_sys, 1.3)

    return {
        "n_sys": n_sys,
        "M1_cat_Msun": M1_cat_Msun, "M2_cat_Msun": M2_cat_Msun,
        "M1_cat_kg": M1_cat_Msun * MSUN_KG, "M2_cat_kg": M2_cat_Msun * MSUN_KG,
        "Mtot_cat_kg": (M1_cat_Msun + M2_cat_Msun) * MSUN_KG,
        "sepAU": sepAU, "s_m": sepAU * AU_M,
        "d_mean_pc": d_mean_pc,
        "e_pmRA1": e_pmRA1, "e_pmRA2": e_pmRA2, "e_pmDE1": e_pmDE1, "e_pmDE2": e_pmDE2,
        "e_m": e_m, "e_lo": e_lo, "e_hi": e_hi, "dpm_sig": dpm_sig, "alpha_ecc": alpha_ecc,
    }


def build_fake_real_dataset(cat: dict, f_multi_true: float,
                             a0_true: float | None, include_wobble_true: bool,
                             rng: np.random.Generator) -> dict:
    """Constroi v_p_fake_real (n_sys,) -- UMA realizacao fixa de
    geometria+injecao de companheira, "a verdade da natureza" para esta
    validacao. Retorna tambem RUWE sintetico correlacionado com
    has_multi_true (ground truth conhecido, usado so' para as checagens de
    consistencia A4/diagnosticos -- NUNCA passado ao pipeline de
    auto-calibracao, que so' recebe v_p_fake_real)."""
    n_sys = cat["n_sys"]
    s_m = cat["s_m"]

    inj_true = ci.sample_companion_injection_mc(
        cat["M1_cat_kg"], cat["M2_cat_kg"], f_multi_true, n_mc=1, rng=rng,
    )
    has_multi_true = inj_true["has_multi"][0]
    mask1, mask2 = inj_true["mask1"][0], inj_true["mask2"][0]
    kappa1, kappa2 = inj_true["kappa_1"][0], inj_true["kappa_2"][0]
    M1_true, M2_true = inj_true["M1_true"][0], inj_true["M2_true"][0]
    Mtot_true = inj_true["Mtot_true"][0]

    e_sample, _ = dc.sample_eccentricity(
        cat["e_m"], cat["e_lo"], cat["e_hi"], cat["alpha_ecc"], cat["dpm_sig"], 1, rng,
    )
    i, phi0, phi = dc.sample_orbital_geometry(e_sample, rng)

    v_p_outer_2d, r_true_2d, gN_true_2d, _ = sp._generate_outer_vp_varying_mass(
        s_m, Mtot_true[None, :], e_sample, i, phi0, phi, a0_boost=a0_true,
    )
    pa = rng.uniform(0.0, 2.0 * np.pi, size=(1, n_sys))
    v_ra = v_p_outer_2d * np.cos(pa)
    v_de = v_p_outer_2d * np.sin(pa)

    if include_wobble_true:
        ra1, de1 = sp._wobble_component_mc(mask1[None, :], kappa1[None, :], M1_true[None, :], cat["d_mean_pc"], rng)
        ra2, de2 = sp._wobble_component_mc(mask2[None, :], kappa2[None, :], M2_true[None, :], cat["d_mean_pc"], rng)
        v_ra = v_ra + ra1 + ra2
        v_de = v_de + de1 + de2

    v_p_clean = np.sqrt(v_ra ** 2 + v_de ** 2)

    sig_ra, sig_de = sp.astrometric_noise_sigma_v_si(
        cat["e_pmRA1"], cat["e_pmRA2"], cat["e_pmDE1"], cat["e_pmDE2"], cat["d_mean_pc"],
    )
    v_p_noisy_2d = sp._inject_astrometric_noise(v_p_clean, sig_ra[None, :], sig_de[None, :], rng)
    v_p_fake_real = v_p_noisy_2d[0]

    # ---- RUWE sintetico com correlacao de VERDADE CONHECIDA a' presenca
    #      de companheira oculta (baseline quase-1 para sistemas limpos,
    #      elevado para has_multi_true=True -- proxy de excesso
    #      astrometrico, mesmo espirito qualitativo do RUWE real de Gaia,
    #      MAGNITUDE nao calibrada contra dado real, so' a CORRELACAO
    #      direcional e' o que esta validacao precisa, ver
    #      METHODOLOGY_ADDENDUM.md Secao 3, item A4). ----
    ruwe_baseline = np.clip(rng.lognormal(mean=np.log(1.02), sigma=0.03, size=n_sys), 0.9, 1.2)
    ruwe_excess = rng.lognormal(mean=np.log(0.35), sigma=0.5, size=n_sys)
    RUWE_synth = np.where(has_multi_true, ruwe_baseline + ruwe_excess, ruwe_baseline)

    return {
        "v_p_fake_real": v_p_fake_real,
        "f_multi_true": float(f_multi_true),
        "a0_true": a0_true,
        "has_multi_true": has_multi_true,
        "RUWE_synth": RUWE_synth,
        "diagnostics": {
            "frac_has_multi_true": float(has_multi_true.mean()),
            "median_v_p_fake_real_km_s": float(np.median(v_p_fake_real) / 1000.0),
            "include_wobble_true": bool(include_wobble_true),
        },
    }
