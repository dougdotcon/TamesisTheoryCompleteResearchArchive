"""Estatistica corrigida delta_obs-newt -- DISC-COSMOLOGY-MOND-SPARC-004,
PREREGISTRATION.md Secao 4c ("Adendo de metodologia").

Implementa EXATAMENTE o Adendo 4c: nao redefine nada de deprojection_common.py
(PROIBIDO editar aquele arquivo) -- so' chama `run_mc_deprojection` duas vezes
(ramo REAL, ramo MOCK) e implementa a logica de diferenca/comparacao em torno
dela, mais o protocolo de bootstrap do Gap (e) item 3 (agora aplicado a
delta_obs-newt em vez de a0 diretamente) e a predicao delta_AQUAL(bin;a0).

===========================================================================
Decisao de design 1 -- em que gN os sistemas sao binados
===========================================================================
PREREGISTRATION.md Secao 4c / Gap (d): "5 bins de log10(gN) JA FIXADOS em
SPARC-003 ... reaproveitadas sem modificacao -- nenhum novo binning definido
a partir do resultado deste teste". As bordas fixas de SPARC-003 (Secao 2
daquele pre-registro) foram calculadas sobre gN PROJETADO = G*M_tot/s^2 (s =
separacao projetada OBSERVADA, nunca desprojetada) -- exatamente como em
`../../COSMOLOGY_WIDE_BINARIES/analysis/run_preregistered_analysis.py`
(BIN_EDGES_LOG_GN, ver `assign_bins_by_projected_gN` abaixo). Este modulo
usa a MESMA convencao: cada sistema e' atribuido a UM bin fixo por
log10(G*M_tot/s^2), IDENTICO para os ramos real e mock (s e M_tot sao os
mesmos dos dois lados) e IDENTICO em toda replica de bootstrap -- nunca o
gN desprojetado (g_N_i, que varia por sorteio MC) e' usado para decidir a
qual bin um sistema pertence. Isso preserva "nenhum novo binning definido a
partir do resultado" (a atribuicao de bin nao depende de nenhuma velocidade,
real ou mock, nem de nenhum sorteio de Monte Carlo).

===========================================================================
Decisao de design 2 -- estatistica primaria vs. bootstrap (Gap e itens 1-3)
===========================================================================
"Primaria" (nao-bootstrap, PARTE 1 item 3 da tarefa): para cada bin, agrupa
TODOS os pares (realizacao MC, sistema) do bin -- shape (n_mc, n_sys_bin) --
e toma UMA mediana pooled sobre esse conjunto inteiro, separadamente para o
ramo real e o ramo mock; delta_obs-newt(bin) = mediana_real - mediana_mock.
Isso usa a informacao completa das n_mc=200 realizacoes (mesma logica de
"pooled_median_all_draws_all_systems" ja usada em
validation_synthetic_newtonian.json), sem qualquer pareamento real-mock por
indice de sorteio -- o pareamento por indice so' e' exigido explicitamente
pelo Adendo 4c/Gap (e) item 3 PARA O BOOTSTRAP, no qual cada sistema
reamostrado usa UM par (real,mock) do MESMO indice de realizacao MC
(preservando a correlacao real-mock por sistema/sorteio dentro de cada
replica). Fora do bootstrap nao ha essa exigencia de pareamento -- os dois
ramos ja sao, por construcao, geometrias orbitais independentes (Adendo 4c:
"geometria orbital... sorteada independentemente da usada no calculo real").

===========================================================================
Decisao de design 3 -- geracao do v_p mock / boost MOND do controle positivo
===========================================================================
`generate_synthetic_vp_newtonian` reimplementa de forma limpa e reutilizavel
a logica ja usada e validada em `validate_synthetic_newtonian.py`
(`generate_synthetic_vp`): UMA realizacao "verdadeira" da geometria orbital
(e,i,phi0,phi via deprojection_common, Gaps a-b), r_true por projecao
geometrica direta (Gap c), v_true via vis-viva Kepleriana EXATA (2 corpos,
Newtoniana pura), v_p sintetico por projecao direta de volta (Gap c,
direcao direta). Convencao de anomalia verdadeira nu_true=phi_true (NAO
phi_true-phi0_true) -- mesma convencao ja verificada empiricamente em
validate_synthetic_newtonian.py (produz sinal correto batendo com Eq.16 de
Chae, ver docstring daquele modulo).

Boost MOND opcional (`a0_boost`, usado SOMENTE pelo controle positivo da
revalidacao, Parte 2 item 2 da tarefa): multiplica o v_p sintetico PURO por
sqrt(nu(gN_true/a0_boost)), onde gN_true=G*M_tot/r_true^2 e' a aceleracao
Newtoniana 3D "verdadeira" daquela unica realizacao geradora (nao a
projetada, fixa por sistema, usada so' para BINAGEM -- ver Decisao 1). Como
v_p = v_true * fator_de_projecao e multiplicacao comuta, multiplicar v_true
por sqrt(nu(...)) antes de projetar ou multiplicar v_p_synth por
sqrt(nu(...)) depois de projetar da' EXATAMENTE o mesmo resultado -- este
modulo aplica no v_p_synth final, ja projetado, por simplicidade.
"""

from __future__ import annotations

import numpy as np

import deprojection_common as dc

# ---------------------------------------------------------------------
# Bordas de bin FIXAS, reaproveitadas SEM modificacao de
# ../../COSMOLOGY_WIDE_BINARIES/PREREGISTRATION.md Secao 2 /
# ../../COSMOLOGY_WIDE_BINARIES/analysis/run_preregistered_analysis.py
# (BIN_EDGES_LOG_GN), calculadas sobre log10(G*M_tot/s^2) [SI] da amostra
# de descoberta na sessao de lock de SPARC-003.
# ---------------------------------------------------------------------
BIN_EDGES_LOG_GN_SPARC003 = np.array(
    [-11.7012, -9.1728, -8.4667, -7.9752, -7.5548, -6.5224]
)
N_BINS = 5


# ---------------------------------------------------------------------
# nu(x) e delta_AQUAL(bin;a0) -- Adendo 4c
# ---------------------------------------------------------------------

def nu_aqual(x: np.ndarray) -> np.ndarray:
    """nu(x) = 1/(1-exp(-sqrt(x))), funcao de interpolacao 'simple'
    (McGaugh, Lelli & Schombert 2016), ja travada em SPARC-002/003/004."""
    x = np.asarray(x, dtype=np.float64)
    return 1.0 / (1.0 - np.exp(-np.sqrt(x)))


def delta_aqual(gN_bin: np.ndarray, a0: float) -> np.ndarray:
    """delta_AQUAL(bin;a0) = log10(nu(gN_bin/a0)) -- Adendo 4c."""
    return np.log10(nu_aqual(np.asarray(gN_bin, dtype=np.float64) / a0))


# ---------------------------------------------------------------------
# Binagem fixa por gN PROJETADO (Decisao de design 1)
# ---------------------------------------------------------------------

def projected_log_gN(s: np.ndarray, M_tot: np.ndarray) -> np.ndarray:
    """log10(G*M_tot/s^2) [SI], gN PROJETADO (nao desprojetado) -- a
    mesma quantidade que definiu as bordas de bin de SPARC-003."""
    s = np.asarray(s, dtype=np.float64)
    M_tot = np.asarray(M_tot, dtype=np.float64)
    gN = dc.G_SI * M_tot / s ** 2
    return np.log10(gN)


def assign_bins_by_projected_gN(log_gN_proj: np.ndarray,
                                 bin_edges: np.ndarray = BIN_EDGES_LOG_GN_SPARC003):
    """Atribui cada sistema a um dos len(bin_edges)-1 bins fixos via
    np.digitize sobre as bordas internas (identico a
    run_preregistered_analysis.py::assign_bins). Retorna (bin_idx,
    in_range) -- in_range=False para sistemas fora de
    [bin_edges[0], bin_edges[-1]] (excluidos de qualquer bin)."""
    bin_edges = np.asarray(bin_edges, dtype=np.float64)
    inner_edges = bin_edges[1:-1]
    bin_idx = np.digitize(log_gN_proj, inner_edges)
    in_range = (log_gN_proj >= bin_edges[0]) & (log_gN_proj <= bin_edges[-1])
    return bin_idx, in_range


# ---------------------------------------------------------------------
# Geracao do v_p sintetico Newtoniano puro (+ boost MOND opcional)
# ---------------------------------------------------------------------

def generate_synthetic_vp_newtonian(s: np.ndarray, M_tot: np.ndarray,
                                     e_m: np.ndarray, e_lo: np.ndarray,
                                     e_hi: np.ndarray, alpha: np.ndarray,
                                     dpm_sig: np.ndarray,
                                     rng: np.random.Generator,
                                     a0_boost: float | None = None):
    """Gera UMA realizacao 'verdadeira' de orbita Kepleriana Newtoniana
    pura (Gaps a-c de deprojection_common.py) e projeta de volta para um
    v_p sintetico observavel. Reimplementacao limpa/reutilizavel da logica
    ja usada e validada em validate_synthetic_newtonian.py::generate_synthetic_vp
    (mesmas formulas, mesma convencao de anomalia verdadeira nu_true=phi_true
    -- ver Decisao de design 3 no docstring do modulo).

    Se `a0_boost` != None: multiplica o v_p sintetico puro por
    sqrt(nu_aqual(gN_true/a0_boost)) -- boost MOND explicito, usado SOMENTE
    pelo controle positivo da revalidacao (Adendo 4c, Parte 2 item 2).

    Retorna (v_p_synth, diagnostics), v_p_synth shape (n_sys,) SI.
    """
    s = np.asarray(s, dtype=np.float64)
    M_tot = np.asarray(M_tot, dtype=np.float64)
    n = s.shape[0]

    e_true, use_individual = dc.sample_eccentricity(
        e_m, e_lo, e_hi, alpha, dpm_sig, 1, rng)
    i_true, phi0_true, phi_true = dc.sample_orbital_geometry(e_true, rng)

    cos_phi, sin_phi = np.cos(phi_true), np.sin(phi_true)
    cos_i2 = np.cos(i_true) ** 2

    r_true = s[None, :] / np.sqrt(cos_phi ** 2 + cos_i2 * sin_phi ** 2)

    # nu_true = phi_true (NAO phi_true - phi0_true) -- convencao
    # autoconsistente com a parametrizacao interna de deprojection_common.py
    # (periastro em phi=0), verificada empiricamente em
    # validate_synthetic_newtonian.py (bate em sinal/ordem de grandeza com
    # Eq.16 de Chae; a convencao alternativa nu=phi-phi0 produz sinal
    # ERRADO). Reaproveitada aqui sem rederivacao.
    nu_true = phi_true
    a_true = r_true * (1.0 + e_true * np.cos(nu_true)) / (1.0 - e_true ** 2)
    v_true_sq = dc.G_SI * M_tot[None, :] * (2.0 / r_true - 1.0 / a_true)
    if not np.all(v_true_sq > 0):
        raise RuntimeError(
            "vis-viva produziu v^2<=0 -- orbita nao-fisica, checar geometria"
        )
    v_true = np.sqrt(v_true_sq)

    numer = -(cos_phi + e_true * np.cos(phi0_true))
    denom = sin_phi + e_true * np.sin(phi0_true)
    psi_true = np.arctan2(numer, denom)
    cos_psi2 = np.cos(psi_true) ** 2
    sin_psi2 = np.sin(psi_true) ** 2

    v_p_synth = v_true * np.sqrt(cos_psi2 + cos_i2 * sin_psi2)

    g_true = v_true_sq / r_true
    gN_true = dc.G_SI * M_tot[None, :] / r_true ** 2

    v_p_synth = v_p_synth[0]
    gN_true = gN_true[0]
    g_true = g_true[0]

    diagnostics = {
        "e_true": e_true[0],
        "i_true": i_true[0],
        "phi0_true": phi0_true[0],
        "phi_true": phi_true[0],
        "r_true_AU": r_true[0] / dc.AU_M,
        "v_true_kms": v_true[0] / 1e3,
        "log_g_true_over_gN_true": np.log10(g_true / gN_true),
        "gN_true_si": gN_true,
        "use_individual_ecc": use_individual,
        "a0_boost": None,
    }

    if a0_boost is not None:
        boost = np.sqrt(nu_aqual(gN_true / a0_boost))
        v_p_synth = v_p_synth * boost
        diagnostics["a0_boost"] = float(a0_boost)
        diagnostics["boost_factor_median"] = float(np.median(boost))
        diagnostics["boost_factor_min_max"] = (float(boost.min()), float(boost.max()))

    return v_p_synth, diagnostics


# ---------------------------------------------------------------------
# Estatistica primaria delta_obs-newt(bin) + bootstrap (Adendo 4c / Gap e)
# ---------------------------------------------------------------------

def run_delta_obs_newt(s: np.ndarray, v_p_real: np.ndarray, M_tot: np.ndarray,
                        e_m: np.ndarray, e_lo: np.ndarray, e_hi: np.ndarray,
                        alpha: np.ndarray, dpm_sig: np.ndarray,
                        bin_edges: np.ndarray = BIN_EDGES_LOG_GN_SPARC003,
                        n_mc: int = 200, n_bootstrap: int = 1000,
                        seed: int = 12345) -> dict:
    """Implementa o Adendo 4c completo:

    1. Ramo REAL: run_mc_deprojection(..., v_p_real, seed=seed) -- geometria
       orbital sorteada independentemente do ramo mock.
    2. Ramo MOCK: v_p_mock gerado por generate_synthetic_vp_newtonian (orbita
       Kepleriana Newtoniana pura, seed de geometria 'verdadeira' dedicado),
       depois run_mc_deprojection(..., v_p_mock, seed=<outro seed>) --
       geometria orbital de RECUPERACAO tambem independente da do ramo real.
    3. delta_obs-newt(bin) = mediana_real(log10(g/gN)) -
       mediana_mock(log10(g/gN)), pooled sobre (n_mc x sistemas do bin),
       realizacao MC primaria (Decisao de design 2).
    4. Bootstrap: 1000 replicas, reamostragem de sistemas com reposicao;
       cada sistema reamostrado usa UM par (real,mock) do MESMO indice de
       realizacao MC (Gap e item 3), delta_obs-newt recalculado por bin em
       cada replica -- IC de 95% via percentil.
    5. delta_AQUAL(bin;a0) disponivel via `delta_aqual` (nao ajustado aqui --
       o ajuste de a0 fica para o script de analise principal do teste,
       fora do escopo desta revalidacao).

    Todos os arrays de entrada shape (n_sys,), unidades SI (identico a
    run_mc_deprojection). `bin_edges` deve ter n_bins+1 valores em
    log10(gN PROJETADO) [SI].

    Seeds (todos derivados de `seed`, todos distintos e documentados --
    nenhum reaproveitado entre ramos, garantindo independencia geometrica
    real-vs-mock exigida pelo Adendo 4c):
      seed_real           = seed              (run_mc_deprojection, ramo real)
      seed_mock_true       = seed + 111111111  (geometria 'verdadeira' geradora do v_p mock)
      seed_mock_recovery   = seed + 222222222  (run_mc_deprojection, ramo mock)
      seed_bootstrap        = seed + 333333333  (reamostragem bootstrap)

    Retorna dict com delta_obs_newt primario por bin, IC95% bootstrap,
    contagens/gN_bin por bin, diagnosticos da geracao mock, e metadados de
    seed/reprodutibilidade.
    """
    s = np.asarray(s, dtype=np.float64)
    v_p_real = np.asarray(v_p_real, dtype=np.float64)
    M_tot = np.asarray(M_tot, dtype=np.float64)
    e_m = np.asarray(e_m, dtype=np.float64)
    e_lo = np.asarray(e_lo, dtype=np.float64)
    e_hi = np.asarray(e_hi, dtype=np.float64)
    alpha = np.asarray(alpha, dtype=np.float64)
    dpm_sig = np.asarray(dpm_sig, dtype=np.float64)
    bin_edges = np.asarray(bin_edges, dtype=np.float64)
    n_bins = len(bin_edges) - 1
    n_sys = s.shape[0]

    seed_real = seed
    seed_mock_true = seed + 111_111_111
    seed_mock_recovery = seed + 222_222_222
    seed_bootstrap = seed + 333_333_333

    # ---- binagem fixa por gN projetado (Decisao 1) ----
    log_gN_proj = projected_log_gN(s, M_tot)
    bin_idx, in_range = assign_bins_by_projected_gN(log_gN_proj, bin_edges)
    gN_proj = dc.G_SI * M_tot / s ** 2

    # ---- ramo REAL ----
    out_real = dc.run_mc_deprojection(
        s, v_p_real, M_tot, e_m, e_lo, e_hi, alpha, dpm_sig,
        n_mc=n_mc, seed=seed_real,
    )
    log_g_ratio_real = out_real["log_g_ratio"]  # (n_mc, n_sys)

    # ---- gera v_p mock (Newtoniano puro, geometria independente) ----
    rng_mock_true = np.random.default_rng(seed_mock_true)
    v_p_mock, mock_diag = generate_synthetic_vp_newtonian(
        s, M_tot, e_m, e_lo, e_hi, alpha, dpm_sig, rng_mock_true,
    )

    # ---- ramo MOCK (recuperacao, seed INDEPENDENTE de todos os outros) ----
    out_mock = dc.run_mc_deprojection(
        s, v_p_mock, M_tot, e_m, e_lo, e_hi, alpha, dpm_sig,
        n_mc=n_mc, seed=seed_mock_recovery,
    )
    log_g_ratio_mock = out_mock["log_g_ratio"]  # (n_mc, n_sys)

    # ---- delta_obs-newt primario por bin (pooled sobre n_mc x sistemas) ----
    delta_primary = np.full(n_bins, np.nan)
    median_real_primary = np.full(n_bins, np.nan)
    median_mock_primary = np.full(n_bins, np.nan)
    gN_bin_median = np.full(n_bins, np.nan)
    n_sys_per_bin = np.zeros(n_bins, dtype=int)

    for b in range(n_bins):
        mask = in_range & (bin_idx == b)
        n_sys_per_bin[b] = int(mask.sum())
        if n_sys_per_bin[b] == 0:
            continue
        real_vals = log_g_ratio_real[:, mask]
        mock_vals = log_g_ratio_mock[:, mask]
        median_real_primary[b] = np.median(real_vals)
        median_mock_primary[b] = np.median(mock_vals)
        delta_primary[b] = median_real_primary[b] - median_mock_primary[b]
        gN_bin_median[b] = np.median(gN_proj[mask])

    if np.any(n_sys_per_bin == 0):
        raise RuntimeError(
            f"Bin(s) vazio(s) na atribuicao fixa de gN projetado: "
            f"contagens={n_sys_per_bin.tolist()} -- checar bin_edges/amostra."
        )

    # ---- bootstrap (Gap e item 3): reamostra sistemas, par (real,mock)
    #      do MESMO indice de realizacao MC por instancia reamostrada ----
    rng_boot = np.random.default_rng(seed_bootstrap)
    boot_delta = np.full((n_bootstrap, n_bins), np.nan)

    for rep in range(n_bootstrap):
        resample = rng_boot.integers(0, n_sys, size=n_sys)
        mc_draw = rng_boot.integers(0, n_mc, size=n_sys)

        real_paired = log_g_ratio_real[mc_draw, resample]
        mock_paired = log_g_ratio_mock[mc_draw, resample]
        bin_idx_r = bin_idx[resample]
        in_range_r = in_range[resample]

        for b in range(n_bins):
            m = in_range_r & (bin_idx_r == b)
            if m.sum() == 0:
                continue
            boot_delta[rep, b] = np.median(real_paired[m]) - np.median(mock_paired[m])

    ci_lo = np.nanpercentile(boot_delta, 2.5, axis=0)
    ci_hi = np.nanpercentile(boot_delta, 97.5, axis=0)
    n_valid_boot = np.sum(~np.isnan(boot_delta), axis=0)

    return {
        "n_bins": n_bins,
        "bin_edges_log10_gN_projected": bin_edges.tolist(),
        "n_systems_per_bin": n_sys_per_bin.tolist(),
        "gN_bin_median_si": gN_bin_median.tolist(),
        "median_real_log_g_ratio_primary": median_real_primary.tolist(),
        "median_mock_log_g_ratio_primary": median_mock_primary.tolist(),
        "delta_obs_newt_primary": delta_primary.tolist(),
        "bootstrap": {
            "n_bootstrap": n_bootstrap,
            "n_valid_replicas_per_bin": n_valid_boot.tolist(),
            "ci95_lo": ci_lo.tolist(),
            "ci95_hi": ci_hi.tolist(),
            "delta_obs_newt_boot_mean": np.nanmean(boot_delta, axis=0).tolist(),
            "delta_obs_newt_boot_std": np.nanstd(boot_delta, axis=0).tolist(),
        },
        "seeds": {
            "seed_input": seed,
            "seed_real": seed_real,
            "seed_mock_true_geometry": seed_mock_true,
            "seed_mock_recovery": seed_mock_recovery,
            "seed_bootstrap": seed_bootstrap,
        },
        "n_mc": n_mc,
        "n_sys": n_sys,
        "mock_generation_diagnostics": {
            "fraction_individual_eccentricity": float(mock_diag["use_individual_ecc"].mean()),
            "median_e_true": float(np.median(mock_diag["e_true"])),
            "fraction_e_true_gt_0p5": float(np.mean(mock_diag["e_true"] > 0.5)),
            "median_log_g_true_over_gN_true_3d_no_recovery_noise": float(
                np.median(mock_diag["log_g_true_over_gN_true"])
            ),
            "a0_boost": mock_diag["a0_boost"],
        },
    }
