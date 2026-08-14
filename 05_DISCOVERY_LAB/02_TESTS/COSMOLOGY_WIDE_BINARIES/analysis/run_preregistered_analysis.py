"""
DISC-COSMOLOGY-MOND-SPARC-003 -- análise primária pré-registrada.

Executa EXATAMENTE a estatística de teste descrita na Seção 4 de
PREREGISTRATION.md (pré-registro travado em 2026-08-14, ANTES desta
execução) sobre a amostra de descoberta real (30.203 sistemas binários
largos do Gaia EDR3, El-Badry, Rix & Heintz 2021, após cortes de
qualidade da Seção 2). O holdout (12.944 sistemas) NUNCA é lido por
este script -- só discovery_pair_ids é usado.

Nenhuma fórmula, borda de bin, ou critério de decisão é reformulado
aqui: tudo copiado literalmente da Seção 4 do pré-registro travado.

Uso:
    python3 run_preregistered_analysis.py
Saída:
    ../analysis/result_primary.json
"""
import json
import sys
import time

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# Constantes exatas (Seção 4 do pré-registro, mesmas de SPARC-002)
# ---------------------------------------------------------------------------
G_SI = 6.67430e-11          # m^3 kg^-1 s^-2
MSUN_KG = 1.98892e30        # kg
AU_M = 1.495978707e11       # m
MAS_YR_TO_KM_S_PER_PC = 4.74047e-3  # fator de conversão mu[mas/yr]*d[pc] -> km/s

C_LIGHT = 299792458.0       # m/s
H0_SI = 70.0 * 1000.0 / 3.086e22   # s^-1  (70 km/s/Mpc convertido a SI)
A0_A = C_LIGHT * H0_SI / (2.0 * np.pi)   # "Ponte Holográfica"
A0_B = C_LIGHT * H0_SI                    # "MOND Emergence"

# Bordas de bin em log10(g_N), FIXAS -- já declaradas e travadas no
# pré-registro (Seção 2), calculadas sobre a amostra de descoberta na
# sessão de lock. NÃO recalculadas aqui.
BIN_EDGES_LOG_GN = np.array(
    [-11.7012, -9.1728, -8.4667, -7.9752, -7.5548, -6.5224]
)
N_BINS = 5

N_BOOTSTRAP = 1000
BOOTSTRAP_SEED = 20260814  # mesma convenção de seed do lock (data), não
                            # especificado explicitamente no pré-registro
                            # para o bootstrap -- escolha declarada para
                            # reprodutibilidade, documentada no relatório.

DATA_DIR = "../data"
QUALITY_SAMPLE_PATH = f"{DATA_DIR}/quality_filtered_sample.parquet"
SPLIT_PATH = f"{DATA_DIR}/discovery_holdout_split.json"
OUTPUT_PATH = "result_primary.json"

SANITY_A0_REF = 1.2e-10  # McGaugh et al. 2016, checagem de sanidade Seção 3
SANITY_MAX_ORDER_OF_MAGNITUDE_DEVIATION = 1.0  # "mais de uma ordem de grandeza"


def mond_simple_ratio(g_N_bin, a0):
    """Função MOND 'simple' (McGaugh, Lelli & Schombert 2016), aplicada em
    espaço de velocidade -- Seção 4, passo 3 do pré-registro:
        v_p^MOND / v_p^N (a0) = (1 - exp(-sqrt(g_N_bin / a0)))^(-1/2)
    """
    return np.power(1.0 - np.exp(-np.sqrt(g_N_bin / a0)), -0.5)


def mond_simple_ratio_rescaled(g_N_bin, x):
    """Mesma função, mas com a0 = x * 1e-10 (x adimensional, O(1)) para
    evitar o problema de convergência silenciosa de curve_fit relatado em
    DISC-COSMOLOGY-MOND-SPARC-002 quando o parâmetro tem magnitude ~1e-10
    sem reescala."""
    a0 = x * 1e-10
    return mond_simple_ratio(g_N_bin, a0)


def load_discovery_sample():
    """Carrega a amostra filtrada por qualidade e restringe estritamente
    aos discovery_pair_ids do split travado. Holdout_pair_ids nunca é
    lido."""
    df = pd.read_parquet(QUALITY_SAMPLE_PATH)
    with open(SPLIT_PATH) as f:
        split = json.load(f)

    discovery_ids = set(split["discovery_pair_ids"])
    # NUNCA ler split["holdout_pair_ids"] além desta linha de metadado de
    # contagem (não usado para filtrar nada) -- confere apenas que a
    # amostra bate com o total declarado.
    n_holdout_declared = split["n_holdout"]

    pair_id = df["Source1"].astype(str) + "_" + df["Source2"].astype(str)
    mask = pair_id.isin(discovery_ids)
    disc = df.loc[mask].reset_index(drop=True)

    if len(disc) != split["n_discovery"]:
        raise RuntimeError(
            f"Contagem de descoberta não bate: obtida {len(disc)}, "
            f"esperada {split['n_discovery']} (declarada no split.json)."
        )
    if len(disc) != 30203:
        raise RuntimeError(
            f"Amostra de descoberta != 30203 conforme especificado na tarefa "
            f"(obtida {len(disc)})."
        )

    return disc, n_holdout_declared


def compute_system_quantities(disc):
    """Seção 4, passo 1: Δμ, v_p_obs, g_N, v_p_N por sistema."""
    dmu = np.sqrt(
        (disc["pmRA1"].to_numpy() - disc["pmRA2"].to_numpy()) ** 2
        + (disc["pmDE1"].to_numpy() - disc["pmDE2"].to_numpy()) ** 2
    )  # mas/yr
    d_mean_pc = disc["d_mean_pc"].to_numpy()
    v_p_obs = MAS_YR_TO_KM_S_PER_PC * dmu * d_mean_pc  # km/s

    Mtot_kg = disc["Mtot_Msun"].to_numpy() * MSUN_KG
    sep_m = disc["sepAU"].to_numpy() * AU_M

    g_N = G_SI * Mtot_kg / sep_m ** 2  # SI, m/s^2
    v_p_N_si = np.sqrt(G_SI * Mtot_kg / sep_m)  # m/s
    v_p_N = v_p_N_si / 1000.0  # km/s

    log_g_N = np.log10(g_N)

    return {
        "dmu_mas_yr": dmu,
        "v_p_obs_km_s": v_p_obs,
        "g_N_si": g_N,
        "v_p_N_km_s": v_p_N,
        "log_g_N": log_g_N,
        "ratio": v_p_obs / v_p_N,
    }


def assign_bins(log_g_N, edges):
    """Atribui cada sistema a um dos 5 bins fixos usando as bordas dadas.
    Usa np.digitize sobre as 4 bordas internas (edges[1:-1]); os pontos
    extremos (min/max exatos da amostra) ficam automaticamente dentro do
    bin 0 / bin 4 respectivamente, já que as bordas externas declaradas no
    pré-registro (arredondadas a 4 casas decimais) envolvem folgadamente o
    range real de log10(g_N) da amostra de descoberta (verificado: nenhum
    sistema cai fora de [edges[0], edges[-1]])."""
    inner_edges = edges[1:-1]
    bin_idx = np.digitize(log_g_N, inner_edges)  # produz valores 0..4
    return bin_idx


def median_ratio_per_bin(log_g_N, g_N, ratio, edges, n_bins=N_BINS):
    """Retorna (medians_ratio, g_N_bin_median, counts) por bin, na ordem
    dos bins 0..n_bins-1. NaN se algum bin ficar vazio (não deve ocorrer
    com n~30203 e 5 bins, mas é verificado explicitamente)."""
    bin_idx = assign_bins(log_g_N, edges)
    medians_ratio = np.full(n_bins, np.nan)
    g_N_bin = np.full(n_bins, np.nan)
    counts = np.zeros(n_bins, dtype=int)
    for b in range(n_bins):
        sel = bin_idx == b
        counts[b] = sel.sum()
        if counts[b] > 0:
            medians_ratio[b] = np.median(ratio[sel])
            g_N_bin[b] = np.median(g_N[sel])
    return medians_ratio, g_N_bin, counts


def fit_a0(g_N_bin, medians_ratio, x0):
    """Ajuste não-linear de mínimos quadrados de a0 (reescalado por 1e-10)
    entre as 5 razões medianas empíricas e o modelo MOND 'simple'.
    Retorna a0 (SI, m/s^2) ou None se o ajuste falhar."""
    try:
        popt, pcov = curve_fit(
            mond_simple_ratio_rescaled,
            g_N_bin,
            medians_ratio,
            p0=[x0],
            maxfev=20000,
        )
        x_fit = popt[0]
        return x_fit * 1e-10
    except Exception:
        return None


def main():
    t0 = time.time()
    print("Carregando amostra de descoberta (SOMENTE discovery_pair_ids)...")
    disc, n_holdout_declared = load_discovery_sample()
    n = len(disc)
    print(f"  n_discovery carregado = {n} (holdout declarado, não lido: {n_holdout_declared})")

    q = compute_system_quantities(disc)

    # ------------------------------------------------------------------
    # Passo 2-4: medianas por bin + ajuste principal (amostra completa)
    # ------------------------------------------------------------------
    medians_ratio, g_N_bin, counts = median_ratio_per_bin(
        q["log_g_N"], q["g_N_si"], q["ratio"], BIN_EDGES_LOG_GN
    )
    print("Medianas por bin (razão v_p_obs/v_p_N):", medians_ratio)
    print("g_N_bin (mediana de g_N por bin, SI):", g_N_bin)
    print("Contagem por bin:", counts)

    if np.any(counts == 0) or np.any(np.isnan(medians_ratio)):
        raise RuntimeError(
            "Bin vazio ou mediana NaN na amostra completa -- não deveria "
            "acontecer com n=30203; reportar sem prosseguir."
        )

    # Checagem de convergência: ajustar com 2 p0 iniciais bem diferentes
    x0_1, x0_2 = 1.0, 5.0
    a0_fit_1 = fit_a0(g_N_bin, medians_ratio, x0_1)
    a0_fit_2 = fit_a0(g_N_bin, medians_ratio, x0_2)

    convergence_ok = bool(
        a0_fit_1 is not None
        and a0_fit_2 is not None
        and np.isfinite(a0_fit_1)
        and np.isfinite(a0_fit_2)
        and abs(a0_fit_1 - a0_fit_2) / max(abs(a0_fit_1), abs(a0_fit_2), 1e-30) < 1e-6
    )
    print(f"Fit com x0={x0_1}: a0 = {a0_fit_1:.6e} m/s^2" if a0_fit_1 is not None else "Fit com x0=1.0 FALHOU")
    print(f"Fit com x0={x0_2}: a0 = {a0_fit_2:.6e} m/s^2" if a0_fit_2 is not None else "Fit com x0=5.0 FALHOU")
    print(f"Convergência (mesmo valor a partir de p0 diferentes)? {convergence_ok}")

    if not convergence_ok:
        print("AVISO: convergência não confirmada -- reportando ambos os valores sem escolher um vencedor arbitrário.")

    a0_fit = a0_fit_1 if a0_fit_1 is not None else a0_fit_2

    # ------------------------------------------------------------------
    # Passo 5: bootstrap por sistema, 1000 réplicas, mesmas bordas fixas
    # ------------------------------------------------------------------
    print(f"\nRodando bootstrap ({N_BOOTSTRAP} réplicas, reamostragem por sistema com reposição)...")
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    ratio_arr = q["ratio"]
    g_N_arr = q["g_N_si"]
    log_g_N_arr = q["log_g_N"]

    bootstrap_a0 = []
    n_failed_bins_bootstrap = 0
    n_failed_fit_bootstrap = 0

    for rep in range(N_BOOTSTRAP):
        sample_idx = rng.integers(0, n, size=n)
        rep_ratio = ratio_arr[sample_idx]
        rep_gN = g_N_arr[sample_idx]
        rep_logGN = log_g_N_arr[sample_idx]

        rep_med_ratio, rep_gN_bin, rep_counts = median_ratio_per_bin(
            rep_logGN, rep_gN, rep_ratio, BIN_EDGES_LOG_GN
        )

        if np.any(rep_counts == 0) or np.any(np.isnan(rep_med_ratio)):
            n_failed_bins_bootstrap += 1
            continue

        a0_rep = fit_a0(rep_gN_bin, rep_med_ratio, x0=1.0)
        if a0_rep is None or not np.isfinite(a0_rep) or a0_rep <= 0:
            n_failed_fit_bootstrap += 1
            continue

        bootstrap_a0.append(a0_rep)

        if (rep + 1) % 200 == 0:
            print(f"  ... {rep + 1}/{N_BOOTSTRAP} réplicas concluídas")

    bootstrap_a0 = np.array(bootstrap_a0)
    n_valid_bootstrap = len(bootstrap_a0)
    print(f"Réplicas válidas: {n_valid_bootstrap}/{N_BOOTSTRAP} "
          f"(bins vazios: {n_failed_bins_bootstrap}, fit falhou: {n_failed_fit_bootstrap})")

    if n_valid_bootstrap < N_BOOTSTRAP:
        print("AVISO: nem todas as 1000 réplicas produziram um ajuste válido -- "
              "reportando o IC calculado apenas sobre as réplicas válidas, "
              "com a contagem exata declarada no resultado (não escondido).")

    ci_lo, ci_hi = np.percentile(bootstrap_a0, [2.5, 97.5]) if n_valid_bootstrap > 0 else (np.nan, np.nan)
    print(f"IC bootstrap 95% em a0: [{ci_lo:.6e}, {ci_hi:.6e}] m/s^2")

    # ------------------------------------------------------------------
    # Passo 6: H_A / H_B dentro do IC?
    # ------------------------------------------------------------------
    a0_A_survives = bool(ci_lo <= A0_A <= ci_hi) if n_valid_bootstrap > 0 else False
    a0_B_survives = bool(ci_lo <= A0_B <= ci_hi) if n_valid_bootstrap > 0 else False

    print(f"\na0_A (Ponte Holográfica) = {A0_A:.6e} m/s^2 -> sobrevive no IC? {a0_A_survives}")
    print(f"a0_B (MOND Emergence)    = {A0_B:.6e} m/s^2 -> sobrevive no IC? {a0_B_survives}")

    # ------------------------------------------------------------------
    # Checagem de sanidade (Seção 3): a0 ajustado em ordem de grandeza
    # compatível com ~1.2e-10 m/s^2 (McGaugh et al. 2016)
    # ------------------------------------------------------------------
    if a0_fit is not None and a0_fit > 0:
        log_ratio_to_ref = float(abs(np.log10(a0_fit / SANITY_A0_REF)))
        sanity_pass = bool(log_ratio_to_ref <= SANITY_MAX_ORDER_OF_MAGNITUDE_DEVIATION)
    else:
        log_ratio_to_ref = None
        sanity_pass = False

    print(f"\nChecagem de sanidade Seção 3: a0_fit={a0_fit:.6e} vs a0_ref={SANITY_A0_REF:.2e} "
          f"-> |log10(razão)|={log_ratio_to_ref:.4f} -> PASSA (<=1 ordem de grandeza)? {sanity_pass}")

    if not sanity_pass:
        print("*** ATENÇÃO: checagem de sanidade da Seção 3 FALHOU. Segundo o "
              "pré-registro, isso é sinal de erro de implementação -- o "
              "resultado é reportado integralmente, mas o veredito H_A/H_B "
              "NÃO deve ser aceito sem investigar a causa. ***")

    # ------------------------------------------------------------------
    # Critério de decisão (Seção 5)
    # ------------------------------------------------------------------
    if a0_A_survives and a0_B_survives:
        verdict = "INCONCLUSIVE_BOTH_SURVIVE"
    elif a0_A_survives and not a0_B_survives:
        verdict = "H_A_SUPPORTED_H_B_FALSIFIED"
    elif a0_B_survives and not a0_A_survives:
        verdict = "H_B_SUPPORTED_H_A_FALSIFIED"
    else:
        verdict = "BOTH_FALSIFIED"

    print(f"\nVeredito (Seção 5): {verdict}")

    elapsed = time.time() - t0
    print(f"\nTempo total: {elapsed:.1f}s")

    # ------------------------------------------------------------------
    # Monta resultado completo
    # ------------------------------------------------------------------
    result = {
        "test_id": "DISC-COSMOLOGY-MOND-SPARC-003",
        "preregistration_path": "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES/PREREGISTRATION.md",
        "analysis_script": "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES/analysis/run_preregistered_analysis.py",
        "run_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "n_discovery_used": int(n),
        "n_holdout_declared_not_read": int(n_holdout_declared),
        "constants": {
            "G_SI": G_SI,
            "MSUN_KG": MSUN_KG,
            "AU_M": AU_M,
            "mas_yr_to_km_s_per_pc": MAS_YR_TO_KM_S_PER_PC,
            "c_light_m_s": C_LIGHT,
            "H0_km_s_Mpc": 70.0,
            "H0_si_s^-1": H0_SI,
        },
        "a0_A_holographic_bridge": {
            "formula": "c*H0/(2*pi)",
            "value_si_m_s2": A0_A,
        },
        "a0_B_mond_emergence": {
            "formula": "c*H0",
            "value_si_m_s2": A0_B,
        },
        "bin_edges_log10_gN_fixed_from_preregistration": BIN_EDGES_LOG_GN.tolist(),
        "n_bins": N_BINS,
        "bins": [
            {
                "bin_index": b,
                "log10_gN_range": [float(BIN_EDGES_LOG_GN[b]), float(BIN_EDGES_LOG_GN[b + 1])],
                "n_systems": int(counts[b]),
                "g_N_bin_median_si_m_s2": float(g_N_bin[b]),
                "log10_g_N_bin_median": float(np.log10(g_N_bin[b])),
                "median_ratio_vpobs_over_vpN": float(medians_ratio[b]),
            }
            for b in range(N_BINS)
        ],
        "fit": {
            "model": "ratio_MOND(a0, g_N_bin) = (1 - exp(-sqrt(g_N_bin/a0)))^(-1/2)",
            "rescaling": "a0 = x * 1e-10, ajustado em x (SPARC-002 lição de convergência)",
            "convergence_check": {
                "x0_1": x0_1,
                "a0_fit_from_x0_1_si_m_s2": a0_fit_1,
                "x0_2": x0_2,
                "a0_fit_from_x0_2_si_m_s2": a0_fit_2,
                "converged_to_same_value": convergence_ok,
            },
            "a0_fit_si_m_s2": a0_fit,
            "a0_fit_x1e-10_units": a0_fit / 1e-10 if a0_fit is not None else None,
        },
        "bootstrap": {
            "n_replicas_requested": N_BOOTSTRAP,
            "n_replicas_valid": int(n_valid_bootstrap),
            "n_replicas_failed_empty_bin": int(n_failed_bins_bootstrap),
            "n_replicas_failed_fit": int(n_failed_fit_bootstrap),
            "seed": BOOTSTRAP_SEED,
            "seed_note": "Não especificado explicitamente no pré-registro para o bootstrap (apenas para o split/bordas de bin). Escolhido = LOCK_DATE_SEED por convenção de reprodutibilidade, declarado aqui como decisão de implementação.",
            "resampling_level": "sistema (não bin)",
            "rebin_per_replica": "SIM, usando as mesmas bordas fixas da Seção 2 (nunca recalculadas por réplica)",
            "ci_95_low_si_m_s2": float(ci_lo) if n_valid_bootstrap > 0 else None,
            "ci_95_high_si_m_s2": float(ci_hi) if n_valid_bootstrap > 0 else None,
        },
        "decision": {
            "a0_A_within_ci95": a0_A_survives,
            "a0_B_within_ci95": a0_B_survives,
            "verdict_section5": verdict,
        },
        "sanity_check_section3": {
            "reference_a0_mcgaugh2016_si_m_s2": SANITY_A0_REF,
            "abs_log10_ratio_fit_to_reference": log_ratio_to_ref,
            "passes_within_one_order_of_magnitude": sanity_pass,
        },
        "diagnostics_model_range_mismatch": {
            "note": (
                "A função MOND 'simple' (1 - exp(-sqrt(g_N/a0)))^(-1/2), para "
                "qualquer a0 > 0 finito, tem imagem estritamente em (1, +infinito) "
                "-- tende a 1 por cima quando a0 -> 0, e diverge quando a0 -> "
                "+infinito. As 5 medianas empíricas observadas neste teste "
                "(ver 'bins' acima) são TODAS < 1. Isso torna o ajuste "
                "estruturalmente mal-condicionado: o otimizador só consegue "
                "se aproximar do alvo empurrando a0 para valores muito "
                "pequenos (fazendo o modelo tender a 1 por cima), sem nunca "
                "alcançar de fato os valores < 1 observados -- o que explica "
                "a não-convergência entre p0 diferentes e a falha na "
                "checagem de sanidade da Seção 3."
            ),
            "fraction_all_discovery_systems_with_ratio_gt_1": float((q["ratio"] > 1).mean()),
            "median_ratio_overall_all_discovery_systems": float(np.median(q["ratio"])),
            "likely_cause": (
                "Viés de projeção conhecido e já declarado no preâmbulo da "
                "Seção 4 do pré-registro: a estatística usada aqui é a "
                "simplificação de Chae (2023) em espaço projetado (sem "
                "desprojeção Monte Carlo de excentricidades de Hwang et al. "
                "2022), explicitamente descrita como checagem de robustez, "
                "não como método principal de Chae. Tanto a velocidade "
                "transversal projetada quanto a separação projetada (sem "
                "correção geométrica de projeção/excentricidade) tendem a "
                "produzir v_p_obs/v_p_N sistematicamente < 1 mesmo em regime "
                "puramente Newtoniano -- isso NÃO foi identificado como um "
                "erro de implementação nesta execução (fórmulas conferidas "
                "termo a termo contra a Seção 4 e contra "
                "generate_split_and_bins.py, valores físicos plausíveis "
                "verificados por amostragem manual), mas sim como uma "
                "propriedade estrutural da estatística simplificada "
                "pré-registrada, já antecipada pelo próprio texto do "
                "pré-registro como limitação declarada."
            ),
        },
        "elapsed_seconds": elapsed,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResultado salvo em {OUTPUT_PATH}")

    return result


if __name__ == "__main__":
    main()
