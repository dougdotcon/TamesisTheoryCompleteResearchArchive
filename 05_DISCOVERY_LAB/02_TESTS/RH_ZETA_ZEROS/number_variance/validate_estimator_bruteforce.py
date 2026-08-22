"""
VALIDACAO (b) -- correcao da IMPLEMENTACAO do estimador exato
(`_exact_window_integral` e `block_number_variance`), independente de
qualquer modelo teorico. Dois processos de ground truth:

1. Processo de Poisson (taxa 1): V(L)=L EXATO para qualquer L (sem
   correlacao, memoryless) -- ground truth analitico fechado, testado
   na FAIXA COMPLETA de L usada na analise primaria real (ate ~2200),
   usando o MESMO desenho de blocos adaptativo (`block_number_variance`,
   factor=4, min_B) que sera usado no dado real.
2. Cross-check por forca bruta: para uma amostra de L (incluindo os L
   que geraram desvio "descritivo" em validate_gue.py, L=40..320, e
   os L primarios reais L~210 e L~2155), compara a integral EXATA
   (`_exact_window_integral`) contra uma integracao numerica
   independente em grade fina (trapezoidal, 500k pontos) do mesmo
   processo em escada n(L;y). Tolerancia de diferenca relativa
   declarada: <0.5%.

evidence_level: validacao pre-lock. Nenhum dado real de zeta tocado.
"""
import json
import time
from pathlib import Path

import numpy as np

from estimator import _exact_window_integral, block_number_variance

HERE = Path(__file__).resolve().parent
SEED = 20260822_02

L_GRID_POISSON = [1, 5, 10, 20, 40, 80, 160, 210.5, 320, 500, 1000, 1500, 2155.0]
L_GRID_BRUTEFORCE_CHECK = [1, 5, 20, 40, 80, 160, 210.5, 320, 1000, 2155.0]
FACTOR = 4.0
MIN_B = 10
N_POINTS_POISSON = 300_000
FINE_GRID_N = 500_001
TOL_REL = 0.005


def main():
    log_lines = []

    def log(msg):
        print(msg)
        log_lines.append(msg)

    t0 = time.time()
    rng = np.random.default_rng(SEED)
    gaps = rng.exponential(1.0, size=N_POINTS_POISSON)
    x = np.cumsum(gaps)
    x.sort()
    x_range = x[-1] - x[0]
    log(f"[validate_estimator_bruteforce] Poisson N={N_POINTS_POISSON} seed={SEED} x_range={x_range:.1f}")

    # --- Parte 1: block_number_variance (o MESMO codigo do run_primary) vs V(L)=L ---
    result = {"seed": SEED, "n_points": N_POINTS_POISSON, "x_range": float(x_range), "poisson_check": {},
              "bruteforce_check": {}}
    all_pass_1 = True
    for L in L_GRID_POISSON:
        L = float(L)
        B_target = max(MIN_B, int(np.floor(x_range / (FACTOR * L))))
        edges = np.linspace(x[0], x[-1], B_target + 1)
        out = block_number_variance(x, edges, L, min_block_width_factor=3.0)
        if out["V_hat"] is None:
            log(f"  L={L:9.1f}  dado insuficiente (nao deveria ocorrer aqui)")
            all_pass_1 = False
            continue
        z = (out["V_hat"] - L) / out["SE"] if out["SE"] and out["SE"] > 0 else float("nan")
        passed = abs(z) < 4.0  # limiar generoso (4 sigma) -- ground truth exato, so checa ausencia de vies grosseiro
        all_pass_1 = all_pass_1 and passed
        result["poisson_check"][str(L)] = {
            "V_hat": out["V_hat"], "SE": out["SE"], "true_V": L, "z": float(z),
            "n_blocks_used": out["n_blocks_used"], "pass": passed,
        }
        log(f"  Poisson L={L:9.1f}  B={out['n_blocks_used']:4d}  V_hat={out['V_hat']:9.3f}  "
            f"SE={out['SE']:.3f}  true=L={L:.1f}  z={z:+.3f}  {'PASS' if passed else 'FAIL'}")

    log(f"\n[Parte 1] all_pass={all_pass_1}")

    # --- Parte 2: cross-check exato vs forca bruta (grade fina LOCAL) ---
    # Nota de processo: a 1a tentativa usou uma grade fina de contagem FIXA
    # (500001 pontos) abrangendo TODO o range Poisson (~300000) para
    # qualquer L -- isso da espacamento de grade ~0.6, adequado para L
    # grande mas GROSSEIRO DEMAIS para L pequeno (L=1,5,20), subamostrando
    # a estrutura fina da funcao escada nessa escala e produzindo um
    # V_brute enviesado (nao um bug do metodo exato) -- ver
    # validation_estimator_bruteforce_run1_FAILED.log. Corrigido aqui:
    # janela local de integracao de largura 20*L (nao o range inteiro) com
    # espacamento de grade fixo em L/2000, garantindo resolucao << L para
    # qualquer L testado.
    all_pass_2 = True
    x2 = x
    for L in L_GRID_BRUTEFORCE_CHECK:
        L = float(L)
        y_center = x2[0] + x_range / 2.0
        half_window = min(10.0 * L, x_range / 2 - L)
        y_lo, y_hi = y_center - half_window, y_center + half_window
        integral, span = _exact_window_integral(x2, y_lo, y_hi, L)
        V_exact = integral / span

        n_grid = int(2 * half_window / (L / 2000.0)) + 1
        n_grid = min(n_grid, 4_000_001)  # teto de seguranca de memoria/tempo
        ys = np.linspace(y_lo, y_hi, n_grid)
        counts = (np.searchsorted(x2, ys + L / 2, side="right") -
                  np.searchsorted(x2, ys - L / 2, side="left"))
        V_brute = float(np.mean((counts - L) ** 2))
        grid_spacing = (y_hi - y_lo) / (n_grid - 1)

        rel_diff = abs(V_exact - V_brute) / max(abs(V_brute), 1e-12)
        passed = rel_diff < TOL_REL
        all_pass_2 = all_pass_2 and passed
        result["bruteforce_check"][str(L)] = {
            "V_exact": V_exact, "V_brute_finegrid": V_brute, "rel_diff": float(rel_diff),
            "grid_spacing": grid_spacing, "grid_spacing_over_L": grid_spacing / L,
            "window_width_over_L": 2 * half_window / L, "pass": passed,
        }
        log(f"  L={L:9.1f}  janela={2*half_window/L:.0f}*L  grade_espac/L={grid_spacing/L:.5f}  "
            f"V_exact={V_exact:.5f}  V_brute={V_brute:.5f}  rel_diff={rel_diff:.5f}  "
            f"{'PASS' if passed else 'FAIL'}")

    log(f"\n[Parte 2] all_pass={all_pass_2}")

    result["all_pass"] = bool(all_pass_1 and all_pass_2)
    result["wall_time_s"] = time.time() - t0
    log(f"\n[RESULTADO FINAL] all_pass={result['all_pass']}  wall_time={result['wall_time_s']:.1f}s")

    json.dump(result, open(HERE / "validation_estimator_bruteforce.json", "w"), indent=2)
    open(HERE / "validation_estimator_bruteforce.log", "w").write("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
