"""
Analise pre-registrada de DISC-RH-GAP-EXTREME-VALUE-SCALING-001.

Implementa EXATAMENTE a Secao 4-5 de ../PREREGISTRATION.md sobre
zeros1.txt (../../RH_ZETA_ZEROS/data/zeros1.txt, reaproveitado).
zeros5.txt permanece intocado (reservado para o Gate).

Nenhum dado fabricado. Falha de leitura de arquivo e erro fatal.
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ZEROS1_PATH = HERE.parent.parent / "RH_ZETA_ZEROS" / "data" / "zeros1.txt"

N_GRID = [500, 1000, 2000, 5000, 10000]
N_BOOTSTRAP = 10000
SEED = 20260812
BETA_GUE = -1.0 / 3.0
BETA_POISSON = -1.0


def load_zeros1():
    vals = np.array([float(x) for x in open(ZEROS1_PATH).read().split()])
    assert len(vals) == 100000, f"esperado 100000 zeros, achado {len(vals)}"
    assert np.all(np.diff(vals) > 0)
    return vals


def normalized_spacings(gammas):
    g = gammas[:-1]
    raw_gaps = np.diff(gammas)
    mean_local_spacing = 2 * np.pi / np.log(g / (2 * np.pi))
    return raw_gaps / mean_local_spacing


def block_minima(spacings, n):
    """Minimos de blocos nao-sobrepostos e contiguos de tamanho n."""
    n_blocks = len(spacings) // n
    trimmed = spacings[: n_blocks * n].reshape(n_blocks, n)
    return trimmed.min(axis=1)


def fit_slope(medians, n_grid):
    log_n = np.log(np.array(n_grid, dtype=float))
    log_med = np.log(np.array(medians, dtype=float))
    # OLS: log_med = alpha + beta*log_n
    A = np.vstack([np.ones_like(log_n), log_n]).T
    coeffs, _, _, _ = np.linalg.lstsq(A, log_med, rcond=None)
    alpha, beta = coeffs
    return alpha, beta


def main():
    gammas = load_zeros1()
    spacings = normalized_spacings(gammas)
    print(f"[0] {len(spacings)} gaps normalizados reais carregados (zeros1.txt)")

    per_n_block_minima = {}
    medians = []
    for n in N_GRID:
        bm = block_minima(spacings, n)
        per_n_block_minima[n] = bm
        med = float(np.median(bm))
        medians.append(med)
        print(f"    N={n:6d}: n_blocos={len(bm)}, mediana do minimo de bloco={med:.6f}")

    alpha, beta = fit_slope(medians, N_GRID)
    print(f"\n[1] Ajuste OLS: log(mediana_min) = {alpha:.4f} + {beta:.4f}*log(N)")
    print(f"    beta observado = {beta:.4f}")
    print(f"    H_GUE prevista: {BETA_GUE:.4f}  |  H_Poisson prevista: {BETA_POISSON:.4f}")

    print(f"\n[2] Bootstrap ({N_BOOTSTRAP} replicas, seed={SEED})")
    rng = np.random.default_rng(SEED)
    boot_betas = np.empty(N_BOOTSTRAP)
    for k in range(N_BOOTSTRAP):
        boot_medians = []
        for n in N_GRID:
            bm = per_n_block_minima[n]
            resampled = rng.choice(bm, size=len(bm), replace=True)
            boot_medians.append(np.median(resampled))
        _, b = fit_slope(boot_medians, N_GRID)
        boot_betas[k] = b

    ci_low, ci_high = np.percentile(boot_betas, [2.5, 97.5])
    print(f"    IC 95% de beta: [{ci_low:.4f}, {ci_high:.4f}]")

    gue_in_ci = ci_low <= BETA_GUE <= ci_high
    poisson_in_ci = ci_low <= BETA_POISSON <= ci_high

    print(f"\n[3] H_GUE (-1/3) dentro do IC? {gue_in_ci}")
    print(f"    H_Poisson (-1) dentro do IC? {poisson_in_ci}")

    if gue_in_ci and not poisson_in_ci:
        verdict = "H_GUE_SURVIVES_H_POISSON_FALSIFIED"
    elif poisson_in_ci and not gue_in_ci:
        verdict = "H_POISSON_SURVIVES_H_GUE_FALSIFIED"
    elif gue_in_ci and poisson_in_ci:
        verdict = "BOTH_SURVIVE_INCONCLUSIVE"
    else:
        verdict = "BOTH_FALSIFIED"

    print(f"\n[VEREDITO] {verdict}")

    result = {
        "test_id": "DISC-RH-GAP-EXTREME-VALUE-SCALING-001",
        "n_grid": N_GRID,
        "n_blocks_per_n": {str(n): len(per_n_block_minima[n]) for n in N_GRID},
        "median_block_minima": medians,
        "ols_alpha": float(alpha),
        "ols_beta_observed": float(beta),
        "beta_gue_predicted": BETA_GUE,
        "beta_poisson_predicted": BETA_POISSON,
        "n_bootstrap": N_BOOTSTRAP,
        "seed": SEED,
        "beta_ci_95_low": float(ci_low),
        "beta_ci_95_high": float(ci_high),
        "gue_in_ci": bool(gue_in_ci),
        "poisson_in_ci": bool(poisson_in_ci),
        "verdict": verdict,
    }
    out_path = HERE / "result_primary.json"
    json.dump(result, open(out_path, "w"), indent=2)
    print(f"\nResultado salvo em {out_path}")
    return result


if __name__ == "__main__":
    main()
