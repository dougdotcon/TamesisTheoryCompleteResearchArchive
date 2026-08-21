"""
RH-REAL Fase 0 -- Item 6 (reconstruido): TCL de Selberg para log|zeta(1/2+it)|.

evidence_level: exploratory_only. NAO e pre-registro; nenhuma alegacao.
Plano: TRIAGE_NOTE.md secao 2.4.

Em cada altura T de {1e4, 1e6, 1e8, 1e10}: N=4000 pontos t ~ U[T, 2T]
(seed 20260821); X = log|Z(t)|. Estatisticas: media, variancia (com erro
padrao), assimetria, curtose-excesso, KS contra N(0, sigma_modelo).
Modelos comparados (concorrentes NOMEADOS):
  A (Selberg / Radziwill-Soundararajan arXiv:1509.06827): var = (1/2) loglog T
  B (lognormal "ingenuo", sem o fator 1/2):               var = loglog T
"""
import json
import time
from pathlib import Path

import numpy as np

from rs_zeta import Z

HERE = Path(__file__).resolve().parent
HEIGHTS = [1e4, 1e6, 1e8, 1e10]
N_SAMPLES = 4000
SEED = 20260821


def ks_stat_normal(x, sigma):
    """Estatistica KS de x contra N(0, sigma^2) + p-valor assintotico
    (formula de Kolmogorov, 100 termos)."""
    from math import erf, sqrt, exp
    xs = np.sort(x) / sigma
    n = len(xs)
    cdf = 0.5 * (1 + np.array([erf(v / sqrt(2)) for v in xs]))
    d_plus = np.max(np.arange(1, n + 1) / n - cdf)
    d_minus = np.max(cdf - np.arange(0, n) / n)
    d = max(d_plus, d_minus)
    lam = (sqrt(n) + 0.12 + 0.11 / sqrt(n)) * d
    p = 2 * sum((-1) ** (j - 1) * exp(-2 * j * j * lam * lam)
                for j in range(1, 101))
    return float(d), float(min(max(p, 0.0), 1.0))


def main():
    rng = np.random.default_rng(SEED)
    out = {"evidence_level": "exploratory_only",
           "plan": "TRIAGE_NOTE.md sec 2.4", "seed": SEED,
           "n_samples_per_height": N_SAMPLES, "heights": []}
    for T in HEIGHTS:
        t0 = time.time()
        ts = rng.uniform(T, 2 * T, N_SAMPLES)
        z = Z(ts)
        absz = np.abs(z)
        # log|Z|: pontos exatamente em zeros tem prob. 0; nenhum clip
        x = np.log(absz)
        dt = time.time() - t0
        m = float(np.mean(x))
        v = float(np.var(x, ddof=1))
        # erro padrao da variancia via momentos (nao-Gaussiano)
        m4 = float(np.mean((x - m) ** 4))
        se_v = float(np.sqrt((m4 - v * v * (N_SAMPLES - 3) / (N_SAMPLES - 1))
                             / N_SAMPLES))
        skew = float(np.mean((x - m) ** 3) / v ** 1.5)
        kurt = float(m4 / v ** 2 - 3)
        llT = float(np.log(np.log(T)))
        vA = 0.5 * llT           # Selberg
        vB = llT                 # concorrente nomeado
        ksA = ks_stat_normal(x, np.sqrt(vA))
        ksB = ks_stat_normal(x, np.sqrt(vB))
        zA = (v - vA) / se_v
        zB = (v - vB) / se_v
        row = {"T": T, "eval_seconds": dt, "mean": m,
               "variance": v, "se_variance": se_v,
               "skewness": skew, "excess_kurtosis": kurt,
               "loglogT": llT,
               "model_A_selberg_var": vA, "z_off_model_A": float(zA),
               "model_B_naive_var": vB, "z_off_model_B": float(zB),
               "KS_model_A": {"D": ksA[0], "p": ksA[1]},
               "KS_model_B": {"D": ksB[0], "p": ksB[1]}}
        out["heights"].append(row)
        print(f"  T={T:.0e}: media={m:+.4f} var={v:.4f}+-{se_v:.4f} "
              f"skew={skew:+.3f} kurt={kurt:+.3f} | "
              f"A=(1/2)loglogT={vA:.4f} (z={zA:+.1f}) "
              f"B=loglogT={vB:.4f} (z={zB:+.1f}) | "
              f"KS_A D={ksA[0]:.4f} p={ksA[1]:.2e} | {dt:.1f}s")
    json.dump(out, open(HERE / "item6_selberg_result.json", "w"), indent=2)
    print("[item6] salvo item6_selberg_result.json")


if __name__ == "__main__":
    main()
