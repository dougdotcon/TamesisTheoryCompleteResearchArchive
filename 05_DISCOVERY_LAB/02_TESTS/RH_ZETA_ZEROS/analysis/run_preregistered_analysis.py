"""
Analise pre-registrada de DISC-RH-ZERO-GAP-RUNS-001.

Implementa EXATAMENTE a Secao 4-5 de ../PREREGISTRATION.md:
- grade c em {0.10,0.20,0.30} x r em {2,3}
- estatistica: contagem de posicoes com r gaps consecutivos todos >= c
  (janelas sobrepostas)
- nulo: 10.000 permutacoes aleatorias independentes do mesmo
  multiconjunto de gaps (seed 20260812)
- p-valor de uma cauda (direcao pre-registrada: real > nulo)
- correcao de Bonferroni sobre as 6 celulas (limiar 0.05/6)
- rodado em zeros1.txt (primario) e zeros3.txt (secundario/generalizacao,
  reportado separadamente, NAO parte do criterio de decisao primario)

Nenhum dado fabricado. Falha de leitura de arquivo e erro fatal.
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"

C_GRID = [0.10, 0.20, 0.30]
R_GRID = [2, 3]
N_PERMUTATIONS = 10000
SEED = 20260812
BONFERRONI_THRESHOLD = 0.05 / (len(C_GRID) * len(R_GRID))


def load_zeros1():
    path = DATA_DIR / "zeros1.txt"
    vals = np.array([float(x) for x in open(path).read().split()])
    assert len(vals) == 100000, f"esperado 100000 zeros, achado {len(vals)}"
    assert np.all(np.diff(vals) > 0)
    return vals


def load_zeros3():
    """Zeros #10^12+1..+10^4 como offsets de gamma=267653395647.
    Dados numericos comecam na linha 10 (1-indexed) do arquivo."""
    path = DATA_DIR / "zeros3.txt"
    lines = open(path).readlines()
    data_lines = lines[9:]  # linha 10 em diante (0-indexed: [9:])
    vals = np.array([float(x) for x in data_lines if x.strip()])
    assert len(vals) == 10000, f"esperado 10000 valores, achado {len(vals)}"
    base = 267653395647.0
    gammas = base + vals
    assert np.all(np.diff(gammas) > 0), "zeros3 deveria estar em ordem crescente"
    return gammas


def normalized_spacings(gammas):
    g = gammas[:-1]
    raw_gaps = np.diff(gammas)
    mean_local_spacing = 2 * np.pi / np.log(g / (2 * np.pi))
    return raw_gaps / mean_local_spacing


def count_runs(spacings, c, r):
    """Numero de posicoes i tais que spacings[i..i+r-1] sao todos >= c
    (janelas sobrepostas permitidas, conforme Secao 4)."""
    above = spacings >= c
    n = len(above)
    count = 0
    for i in range(n - r + 1):
        if above[i:i + r].all():
            count += 1
    return count


def count_runs_vectorized(spacings, c, r):
    """Versao vetorizada (equivalente) para performance nas 10k permutacoes."""
    above = (spacings >= c).astype(np.int32)
    # soma movel de tamanho r via cumsum
    cs = np.concatenate([[0], np.cumsum(above)])
    window_sums = cs[r:] - cs[:-r]
    return int(np.sum(window_sums == r))


def permutation_test(spacings, c, r, n_perm, seed):
    observed = count_runs_vectorized(spacings, c, r)
    rng = np.random.default_rng(seed)
    null_counts = np.empty(n_perm, dtype=np.int64)
    for k in range(n_perm):
        perm = rng.permutation(spacings)
        null_counts[k] = count_runs_vectorized(perm, c, r)
    p_value = (1 + np.sum(null_counts >= observed)) / (n_perm + 1)
    p_value_inverse = (1 + np.sum(null_counts <= observed)) / (n_perm + 1)
    return {
        "c": c,
        "r": r,
        "observed_count": observed,
        "null_mean": float(np.mean(null_counts)),
        "null_std": float(np.std(null_counts)),
        "p_value_real_greater": float(p_value),
        "p_value_real_lower_inverse": float(p_value_inverse),
        "significant_predicted_direction": bool(p_value < BONFERRONI_THRESHOLD),
        "significant_inverse_direction": bool(p_value_inverse < BONFERRONI_THRESHOLD),
    }


def run_grid(spacings, label):
    print(f"\n=== Grade de permutacao: {label} ({len(spacings)} gaps) ===")
    cells = []
    for c in C_GRID:
        for r in R_GRID:
            res = permutation_test(spacings, c, r, N_PERMUTATIONS, SEED)
            cells.append(res)
            print(f"  c={c:.2f} r={r}: observado={res['observed_count']}, "
                  f"nulo_media={res['null_mean']:.1f}+/-{res['null_std']:.1f}, "
                  f"p(real>nulo)={res['p_value_real_greater']:.5f}, "
                  f"sig={res['significant_predicted_direction']}")
    return cells


def aggregate_verdict(cells):
    n_support = sum(1 for c in cells if c["significant_predicted_direction"])
    n_inverse = sum(1 for c in cells if c["significant_inverse_direction"])
    if n_inverse > 0:
        base_verdict = "INVERSE_SIGNAL"
    elif n_support >= 5:
        base_verdict = "STRONG_SUPPORT"
    elif n_support >= 2:
        base_verdict = "PARTIAL_SUPPORT"
    else:
        base_verdict = "NO_SUPPORT"
    return base_verdict, n_support, n_inverse


def main():
    gammas1 = load_zeros1()
    ns1 = normalized_spacings(gammas1)
    primary_cells = run_grid(ns1, "PRIMARIO (zeros1.txt)")
    primary_verdict, n_sup, n_inv = aggregate_verdict(primary_cells)
    print(f"\n[VEREDITO PRIMARIO] {primary_verdict} ({n_sup}/6 celulas suportam H na direcao prevista, {n_inv} inversas)")

    gammas3 = load_zeros3()
    ns3 = normalized_spacings(gammas3)
    secondary_cells = run_grid(ns3, "SECUNDARIO/GENERALIZACAO (zeros3.txt, regime ~10^12)")
    secondary_verdict, n_sup2, n_inv2 = aggregate_verdict(secondary_cells)
    print(f"\n[NOTA INFORMATIVA -- nao e o criterio de decisao] Grade secundaria: {secondary_verdict} ({n_sup2}/6, {n_inv2} inversas)")

    result = {
        "test_id": "DISC-RH-ZERO-GAP-RUNS-001",
        "c_grid": C_GRID,
        "r_grid": R_GRID,
        "n_permutations": N_PERMUTATIONS,
        "seed": SEED,
        "bonferroni_threshold": BONFERRONI_THRESHOLD,
        "primary": {
            "dataset": "zeros1.txt (100k zeros reais, Odlyzko)",
            "n_gaps": len(ns1),
            "cells": primary_cells,
            "n_cells_supporting": n_sup,
            "n_cells_inverse": n_inv,
            "verdict": primary_verdict,
        },
        "secondary_informational": {
            "dataset": "zeros3.txt (10k zeros perto de #10^12, Odlyzko)",
            "n_gaps": len(ns3),
            "cells": secondary_cells,
            "n_cells_supporting": n_sup2,
            "n_cells_inverse": n_inv2,
            "verdict": secondary_verdict,
            "note": "informativo/generalizacao apenas -- NAO parte do criterio de decisao primario (PREREGISTRATION.md Secao 4)",
        },
    }
    out_path = HERE / "result_primary.json"
    json.dump(result, open(out_path, "w"), indent=2)
    print(f"\nResultado salvo em {out_path}")
    return result


if __name__ == "__main__":
    main()
