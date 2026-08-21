"""
RH-REAL Fase 0 -- Item 5 (reconstruido): momentos de zeta na linha critica.

evidence_level: exploratory_only. NAO e pre-registro; nenhuma alegacao.
Plano: TRIAGE_NOTE.md secao 2.3 + adendo (integrais janeladas, T0=2000).

Computa momentos janelados Ibar_k(T) = (1/(T-T0)) int_{T0}^{T} |Z(t)|^{2k} dt
para k=1,2,3 sobre grade t in [2000, 30000], passo 0.05, e compara:
  k=1: teorema Hardy-Littlewood  int_0^T |zeta|^2 = T log(T/2pi) + (2gamma-1)T + E(T)
  k=2: termo lider de Ingham (1/2pi^2) T log^4 T (e variante log^4(T/2pi))
  k=3: termo lider conjectural Keating-Snaith/CFKRS g3*a3/9! * T log^9 T,
       g3 = 42, a3 computado numericamente (produto de Euler), com
       auto-checagem a2 = 6/pi^2.
"""
import json
import time
from pathlib import Path

import numpy as np

from rs_zeta import Z

HERE = Path(__file__).resolve().parent
EULER_GAMMA = 0.5772156649015329
T0 = 2000.0
T_MAX = 30000.0
STEP = 0.05
CHECKPOINTS = [5000.0, 10000.0, 20000.0, 30000.0]


def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if s[p]:
            s[p * p:: p] = False
    return np.nonzero(s)[0]


def a_k(k, prime_limit=2_000_000, mmax=60):
    """Fator aritmetico a_k = prod_p [(1-1/p)^{k^2} sum_m d_k(p^m)^2 p^{-m}],
    d_k(p^m) = C(m+k-1, k-1). Produto numerico sobre primos <= prime_limit."""
    from math import comb, log, log1p
    primes = sieve_primes(prime_limit)
    log_a = 0.0
    for p in primes:
        x = 1.0 / p
        s = 0.0
        xm = 1.0
        for m in range(mmax):
            c = comb(m + k - 1, k - 1)
            s += (c * c) * xm
            xm *= x
            if xm * ((m + k) ** (2 * (k - 1))) < 1e-18:
                break
        log_a += k * k * log1p(-x) + log(s)
    return float(np.exp(log_a))


def main():
    t0 = time.time()
    grid = np.arange(T0, T_MAX + STEP / 2, STEP)
    print(f"[item5] grade: {len(grid)} pontos em [{T0}, {T_MAX}], passo {STEP}")
    z = Z(grid)
    t_eval = time.time() - t0
    print(f"[item5] avaliacao de Z: {t_eval:.1f}s")

    z2 = z * z
    z4 = z2 * z2
    z6 = z4 * z2

    # fator aritmetico com auto-checagem
    t1 = time.time()
    a2 = a_k(2)
    a3 = a_k(3)
    a2_exact = 6.0 / np.pi**2
    print(f"[item5] a2 numerico = {a2:.8f} vs 6/pi^2 = {a2_exact:.8f} "
          f"(rel dif {abs(a2 - a2_exact) / a2_exact:.2e}); a3 = {a3:.8f} "
          f"({time.time()-t1:.1f}s)")
    a2_ok = abs(a2 - a2_exact) / a2_exact < 1e-3

    from math import factorial
    g3_over = 42.0 / factorial(9)          # g3 a3 / 9! com g3=42

    results = {"evidence_level": "exploratory_only",
               "plan": "TRIAGE_NOTE.md sec 2.3 + adendo (janela [T0,T])",
               "grid": {"T0": T0, "T_max": T_MAX, "step": STEP,
                        "n_points": int(len(grid)),
                        "eval_seconds": t_eval},
               "arithmetic_factors": {
                   "a2_numeric": a2, "a2_exact_6_over_pi2": a2_exact,
                   "a2_selfcheck_passed": bool(a2_ok), "a3_numeric": a3},
               "checkpoints": []}

    cum2 = np.concatenate([[0], np.cumsum((z2[1:] + z2[:-1]) / 2 * STEP)])
    cum4 = np.concatenate([[0], np.cumsum((z4[1:] + z4[:-1]) / 2 * STEP)])
    cum6 = np.concatenate([[0], np.cumsum((z6[1:] + z6[:-1]) / 2 * STEP)])

    def hl2(T):
        return T * np.log(T / (2 * np.pi)) + (2 * EULER_GAMMA - 1) * T

    for T in CHECKPOINTS:
        i = int(round((T - T0) / STEP))
        W = grid[i] - T0
        emp1 = cum2[i] / W
        emp2 = cum4[i] / W
        emp3 = cum6[i] / W
        th1 = (hl2(T) - hl2(T0)) / W
        ing_a = ((T * np.log(T) ** 4) - (T0 * np.log(T0) ** 4)) / (2 * np.pi**2) / W
        ing_b = ((T * np.log(T / (2 * np.pi)) ** 4)
                 - (T0 * np.log(T0 / (2 * np.pi)) ** 4)) / (2 * np.pi**2) / W
        ks3 = g3_over * a3 * ((T * np.log(T) ** 9) - (T0 * np.log(T0) ** 9)) / W
        row = {
            "T": T,
            "k1": {"empirical": float(emp1), "hardy_littlewood": float(th1),
                   "ratio": float(emp1 / th1)},
            "k2": {"empirical": float(emp2),
                   "ingham_leading_log4T": float(ing_a),
                   "ratio_log4T": float(emp2 / ing_a),
                   "ingham_leading_log4_T_over_2pi": float(ing_b),
                   "ratio_log4_T_over_2pi": float(emp2 / ing_b)},
            "k3": {"empirical": float(emp3),
                   "ks_cfkrs_leading_42a3_over_9fact_log9T": float(ks3),
                   "ratio": float(emp3 / ks3)},
        }
        results["checkpoints"].append(row)
        print(f"  T={T:>7.0f}: I1 emp/HL = {emp1:8.4f}/{th1:8.4f} "
              f"(razao {emp1/th1:.4f}) | I2 emp/Ingham(log^4 T) = "
              f"{emp2:9.2f}/{ing_a:9.2f} (razao {emp2/ing_a:.4f}; "
              f"com log^4(T/2pi): {emp2/ing_b:.4f}) | "
              f"I3 emp/KS-lider = {emp3:11.1f}/{ks3:11.1f} "
              f"(razao {emp3/ks3:.4f})")

    results["runtime_seconds_total"] = time.time() - t0
    json.dump(results, open(HERE / "item5_moments_result.json", "w"), indent=2)
    print(f"[item5] total {results['runtime_seconds_total']:.1f}s; "
          f"salvo item5_moments_result.json")


if __name__ == "__main__":
    main()
