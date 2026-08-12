"""
RH-REAL (DISC-RH-REAL-001) -- Fase 0: triagem numerica exploratoria.

NAO e um teste pre-registrado. evidence_level: exploratory_only (ver
METHODOLOGY_EXTENSIONS.md). Objetivo: checar um lote de conjecturas
falsificaveis conhecidas da literatura (levantadas nesta sessao) contra
zeros reais de zeta (Odlyzko, ver ../data/PROVENANCE.md), para triagem --
nao para produzir nenhuma alegacao sobre RH em si.

Nenhum dado fabricado/embutido. Falha de leitura de arquivo e erro fatal.
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"


def load_zeros1():
    """100.000 primeiros zeros reais, um por linha (parte imaginaria)."""
    path = DATA_DIR / "zeros1.txt"
    vals = np.array([float(x) for x in open(path).read().split()])
    assert len(vals) == 100000, f"esperado 100000 zeros, achado {len(vals)}"
    assert np.all(np.diff(vals) > 0), "zeros deveriam estar em ordem crescente"
    return vals


def normalized_spacings(gammas):
    """delta_n = (gamma_{n+1}-gamma_n) * log(gamma_n/2pi) / (2pi) -- espacamento
    medio local normalizado para 1 (formula padrao, ver item 2 do
    levantamento de literatura desta sessao)."""
    g = gammas[:-1]
    raw_gaps = np.diff(gammas)
    mean_local_spacing = 2 * np.pi / np.log(g / (2 * np.pi))
    return raw_gaps / mean_local_spacing


def item2_gue_nearest_neighbor(norm_spacings):
    """Item 2: espacamentos normalizados vs. Wigner surmise GUE (aproximacao
    de forma fechada para a distribuicao exata de Gaudin -- nao e a mesma
    coisa, mas e a comparacao padrao usada na literatura, ex. Odlyzko)."""
    s = norm_spacings
    mean_s = float(np.mean(s))
    # Wigner surmise GUE (beta=2): p(s) = (32/pi^2) s^2 exp(-4 s^2/pi)
    hist, edges = np.histogram(s, bins=60, range=(0, 3), density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    wigner = (32 / np.pi**2) * centers**2 * np.exp(-4 * centers**2 / np.pi)
    max_abs_dev = float(np.max(np.abs(hist - wigner)))
    rmse = float(np.sqrt(np.mean((hist - wigner) ** 2)))
    return {
        "mean_normalized_spacing": mean_s,
        "n_spacings": len(s),
        "histogram_vs_wigner_surmise_max_abs_dev": max_abs_dev,
        "histogram_vs_wigner_surmise_rmse": rmse,
        "note": "comparado contra a Wigner surmise GUE (aproximacao de forma fechada), nao a distribuicao exata de Gaudin",
    }


def item3_riemann_von_mangoldt(gammas):
    """Item 3: N(T) ~ (T/2pi) log(T/2pi e) + 7/8, checado em varios T reais
    (contagem real de zeros <= T vs. formula)."""
    checks = []
    for frac in [0.1, 0.25, 0.5, 0.75, 1.0]:
        idx = int(len(gammas) * frac) - 1
        T = gammas[idx]
        n_real = idx + 1  # zeros com indice <= idx, 1-based
        n_formula = (T / (2 * np.pi)) * np.log(T / (2 * np.pi * np.e)) + 7 / 8
        checks.append({
            "T": float(T),
            "n_real": int(n_real),
            "n_formula_leading_term": float(n_formula),
            "residual_n_real_minus_formula": float(n_real - n_formula),
        })
    return checks


def item7_small_gaps(norm_spacings):
    """Item 7: liminf de gaps normalizados < 0.50895 (Inoue 2026, RH-condicional).
    Nao pode confirmar/refutar um liminf com dado finito -- reporta o minimo
    observado como cota empirica."""
    return {
        "min_normalized_gap_observed": float(np.min(norm_spacings)),
        "threshold_inoue_2026": 0.50895,
        "min_below_threshold": bool(np.min(norm_spacings) < 0.50895),
        "note": "liminf nao e testavel com dado finito -- isto e apenas o minimo ja observado nos primeiros 100k zeros",
    }


def item8_large_gaps(norm_spacings):
    """Item 8: existencia de gaps > 3.18x o espacamento medio local (Bui & Milinovich 2014/2017)."""
    max_gap = float(np.max(norm_spacings))
    return {
        "max_normalized_gap_observed": max_gap,
        "threshold_bui_milinovich": 3.18,
        "max_exceeds_threshold": bool(max_gap > 3.18),
    }


def item9_consecutive_moderate_gaps(norm_spacings, c=0.5, r_values=(2, 3)):
    """Item 9 (questao em aberto, arXiv:2412.15481): runs de r gaps
    consecutivos normalizados >= c."""
    above = norm_spacings >= c
    results = {}
    for r in r_values:
        count = 0
        run = 0
        for a in above:
            run = run + 1 if a else 0
            if run >= r:
                count += 1
        results[f"r={r}"] = {
            "n_runs_of_at_least_r_consecutive_gaps_ge_c": int(count),
            "c": c,
        }
    return results


def item1_pair_correlation(gammas, norm_spacings, max_lag=8):
    """Item 1: correlacao de pares (Montgomery), aproximada via pares
    proximos (lag <= max_lag) -- nao todos os pares (custaria O(n^2))."""
    # posicoes normalizadas acumuladas (soma de espacamentos normalizados)
    cumulative = np.concatenate([[0.0], np.cumsum(norm_spacings)])
    diffs_by_lag = {}
    for lag in range(1, max_lag + 1):
        d = cumulative[lag:] - cumulative[:-lag]
        diffs_by_lag[lag] = d

    # historia agregada de todos os pares proximos (lag 1..max_lag), u in (0, max_lag+1)
    all_diffs = np.concatenate(list(diffs_by_lag.values()))
    hist, edges = np.histogram(all_diffs, bins=80, range=(0, max_lag + 1), density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    r2_gue = 1 - (np.sin(np.pi * centers) / (np.pi * centers + 1e-12)) ** 2
    # normalizar r2_gue para densidade de pares (nao e uma densidade de probabilidade
    # normalizada para 1 -- e a funcao de correlacao de pares crua). Reportamos
    # apenas a forma qualitativa (repulsao de nivel perto de u=0), nao um teste
    # quantitativo formal.
    near_zero_mask = centers < 0.3
    far_field_mask = centers > 1.0
    # histograma normalizado por np.histogram(density=True) integra a 1 sobre
    # TODO o dominio (0, max_lag+1) -- entao a densidade "sem correlacao" nao
    # e ~1, e ~1/(max_lag+1) (uniforme). Comparacao correta: densidade perto
    # de u=0 deveria ser MUITO MENOR que a densidade uniforme de fundo
    # (repulsao de nivel), nao comparada a um valor absoluto de 1.
    uniform_background = 1.0 / (max_lag + 1)
    return {
        "n_pairs_used": int(len(all_diffs)),
        "max_lag": max_lag,
        "mean_density_near_u_lt_0.3": float(np.mean(hist[near_zero_mask])),
        "mean_density_u_gt_1.0": float(np.mean(hist[far_field_mask])),
        "uniform_background_expected": uniform_background,
        "suppression_ratio_near_zero_vs_background": float(np.mean(hist[near_zero_mask]) / uniform_background),
        "note": "checagem qualitativa de repulsao de nivel perto de u=0 via pares proximos (lag<=8); densidade e normalizada por np.histogram(density=True) sobre o dominio (0,max_lag+1), entao 'sem correlacao' equivale a densidade uniforme ~1/(max_lag+1), nao a 1 -- nao e um teste quantitativo formal contra R2(u) completo",
    }


def main():
    gammas = load_zeros1()
    print(f"[0] {len(gammas)} zeros reais carregados de zeros1.txt (Odlyzko)")
    print(f"    primeiro zero: {gammas[0]:.9f} (esperado ~14.134725142)")

    ns = normalized_spacings(gammas)

    print("\n[Item 2] GUE nearest-neighbor spacing (Wigner surmise)")
    r2 = item2_gue_nearest_neighbor(ns)
    print(f"    media do espacamento normalizado: {r2['mean_normalized_spacing']:.4f} (esperado ~1.0)")
    print(f"    RMSE histograma vs. Wigner surmise: {r2['histogram_vs_wigner_surmise_rmse']:.4f}")

    print("\n[Item 3] Formula de Riemann-von Mangoldt N(T)")
    r3 = item3_riemann_von_mangoldt(gammas)
    for c in r3:
        print(f"    T={c['T']:.1f}: N_real={c['n_real']}, N_formula={c['n_formula_leading_term']:.1f}, residuo={c['residual_n_real_minus_formula']:.2f}")

    print("\n[Item 7] Gap minimo (Inoue 2026, limiar 0.50895, RH-condicional)")
    r7 = item7_small_gaps(ns)
    print(f"    minimo observado: {r7['min_normalized_gap_observed']:.6f}")

    print("\n[Item 8] Gap maximo (Bui & Milinovich, limiar 3.18)")
    r8 = item8_large_gaps(ns)
    print(f"    maximo observado: {r8['max_normalized_gap_observed']:.4f}, excede 3.18? {r8['max_exceeds_threshold']}")

    print("\n[Item 9] Runs de gaps moderados consecutivos (questao aberta, arXiv:2412.15481)")
    r9 = item9_consecutive_moderate_gaps(ns)
    for k, v in r9.items():
        print(f"    {k}: {v['n_runs_of_at_least_r_consecutive_gaps_ge_c']} runs (c={v['c']})")

    print("\n[Item 1] Correlacao de pares (Montgomery) -- checagem qualitativa")
    r1 = item1_pair_correlation(gammas, ns)
    print(f"    densidade media perto de u<0.3: {r1['mean_density_near_u_lt_0.3']:.4f} (fundo uniforme esperado: {r1['uniform_background_expected']:.4f})")
    print(f"    densidade media para u>1.0: {r1['mean_density_u_gt_1.0']:.4f} (deveria ~= fundo uniforme, sem correlacao)")
    print(f"    razao de supressao perto de u=0 vs. fundo: {r1['suppression_ratio_near_zero_vs_background']:.3f} (deveria ser << 1, repulsao de nivel)")

    result = {
        "n_zeros_used": len(gammas),
        "data_source": "Odlyzko zeros1.txt (ver ../data/PROVENANCE.md)",
        "evidence_level": "exploratory_only",
        "item1_pair_correlation": r1,
        "item2_gue_nearest_neighbor": r2,
        "item3_riemann_von_mangoldt": r3,
        "item7_small_gaps": r7,
        "item8_large_gaps": r8,
        "item9_consecutive_moderate_gaps": r9,
    }
    out_path = HERE / "phase0_triage_result.json"
    json.dump(result, open(out_path, "w"), indent=2)
    print(f"\n[fim] Resultado salvo em {out_path}")
    return result


if __name__ == "__main__":
    main()
