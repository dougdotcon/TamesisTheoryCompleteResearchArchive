"""
RH-REAL Fase 0 -- Item 10 (reconstruido): maximo de |zeta| em intervalos
curtos (Fyodorov-Hiary-Keating, arXiv:1202.4713; ordem lider provada em
arXiv:1612.08575).

evidence_level: exploratory_only. NAO e pre-registro; nenhuma alegacao.
Plano: TRIAGE_NOTE.md secao 2.5.

Em cada altura T de {1e5, 1e7, 1e9} (+1e11 com M=100 se custo projetado
< 5 min, decisao registrada aqui no log): M=300 intervalos de comprimento
2pi, inicios ~ U[T, 2T] (seed 20260821), grade de 256 pontos por
intervalo. M* = max log|Z| por intervalo.
Modelos concorrentes NOMEADOS para a media de M*:
  FHK (campo log-correlacionado): loglogT - (3/4) logloglogT + C
  REM/iid:                        loglogT - (1/4) logloglogT + C'
Discriminante: coeficiente da regressao de mean(M*) - loglogT sobre
logloglogT (intercepto livre nos dois modelos).
Viés de grade finita: estimado refinando para 1024 pontos em 20
intervalos por altura.
"""
import json
import time
from pathlib import Path

import numpy as np

from rs_zeta import Z

HERE = Path(__file__).resolve().parent
HEIGHTS = [1e5, 1e7, 1e9]
M_INTERVALS = 300
GRID_PTS = 256
LEN = 2 * np.pi
SEED = 20260821


def max_log_abs(starts, npts):
    """max log|Z| por intervalo [s, s+2pi), grade de npts pontos."""
    offs = np.arange(npts) * (LEN / npts)
    res = np.empty(len(starts))
    # processa em blocos de intervalos para limitar memoria
    block = max(1, int(3e7 / (npts * np.sqrt(starts[0] / LEN))))
    for i in range(0, len(starts), block):
        s = starts[i:i + block]
        ts = (s[:, None] + offs[None, :]).ravel()
        z = Z(ts).reshape(len(s), npts)
        res[i:i + block] = np.log(np.max(np.abs(z), axis=1))
    return res


def main():
    rng = np.random.default_rng(SEED)
    out = {"evidence_level": "exploratory_only",
           "plan": "TRIAGE_NOTE.md sec 2.5", "seed": SEED,
           "interval_length": "2pi", "grid_points": GRID_PTS,
           "heights": []}
    means, sds, lll, llv, ns = [], [], [], [], []

    heights = list(HEIGHTS)
    m_by_height = {T: M_INTERVALS for T in heights}

    # piloto para decidir extensao a 1e11 (M=100)
    t0 = time.time()
    pilot_starts = rng.uniform(1e11, 2e11, 3)
    _ = max_log_abs(pilot_starts, GRID_PTS)
    per_int = (time.time() - t0) / 3
    proj = per_int * 100
    print(f"[item10] piloto 1e11: {per_int:.2f}s/intervalo -> projecao "
          f"M=100: {proj:.0f}s -> {'INCLUIR' if proj < 300 else 'PULAR'} 1e11")
    out["pilot_1e11_seconds_per_interval"] = per_int
    if proj < 300:
        heights.append(1e11)
        m_by_height[1e11] = 100

    for T in heights:
        t0 = time.time()
        M = m_by_height[T]
        starts = rng.uniform(T, 2 * T, M)
        mx = max_log_abs(starts, GRID_PTS)
        # vies de grade: refina 20 intervalos para 1024 pontos
        sub = starts[:20]
        mx_fine = max_log_abs(sub, 1024)
        bias = float(np.mean(mx_fine - mx[:20]))
        dt = time.time() - t0
        mean_mx = float(np.mean(mx))
        sd_mx = float(np.std(mx, ddof=1))
        llT = float(np.log(np.log(T)))
        lllT = float(np.log(np.log(np.log(T))))
        row = {"T": T, "M": M, "eval_seconds": dt,
               "mean_max_log_absZ": mean_mx, "sd": sd_mx,
               "se_mean": sd_mx / np.sqrt(M),
               "grid_bias_256_vs_1024_mean": bias,
               "loglogT": llT, "logloglogT": lllT,
               "fhk_shape_loglogT_minus_0.75_lll": llT - 0.75 * lllT,
               "rem_shape_loglogT_minus_0.25_lll": llT - 0.25 * lllT}
        out["heights"].append(row)
        means.append(mean_mx + bias)  # corrigido pelo vies medio de grade
        sds.append(sd_mx)
        lll.append(lllT)
        llv.append(llT)
        ns.append(M)
        print(f"  T={T:.0e}: M={M} mean(M*)={mean_mx:.4f} sd={sd_mx:.4f} "
              f"se={sd_mx/np.sqrt(M):.4f} vies_grade={bias:+.4f} | "
              f"loglogT={llT:.4f} logloglogT={lllT:.4f} | {dt:.0f}s")

    # regressao: y = mean(M*) - loglogT  contra  x = logloglogT
    y = np.array(means) - np.array(llv)
    x = np.array(lll)
    w = np.array(ns) / np.array(sds) ** 2          # pesos 1/se^2
    X = np.vstack([np.ones_like(x), x]).T
    W = np.diag(w)
    beta, cov = None, None
    XtWX = X.T @ W @ X
    beta = np.linalg.solve(XtWX, X.T @ W @ y)
    cov = np.linalg.inv(XtWX)
    slope, se_slope = float(beta[1]), float(np.sqrt(cov[1, 1]))
    out["regression"] = {
        "y": "mean(M*)+vies_grade - loglogT", "x": "logloglogT",
        "slope": slope, "se_slope": se_slope,
        "fhk_predicted_slope": -0.75, "rem_iid_predicted_slope": -0.25,
        "z_vs_fhk": (slope + 0.75) / se_slope,
        "z_vs_rem": (slope + 0.25) / se_slope,
        "n_heights": len(x),
        "x_range": float(x.max() - x.min()),
        "note_power": ("sinal discriminante = 0.5*amplitude(x); "
                       "comparar com se_slope"),
    }
    print(f"[item10] slope = {slope:+.3f} +- {se_slope:.3f} "
          f"(FHK: -0.75, REM/iid: -0.25) | amplitude logloglogT = "
          f"{x.max()-x.min():.3f}")
    json.dump(out, open(HERE / "item10_fhk_result.json", "w"), indent=2)
    print("[item10] salvo item10_fhk_result.json")


if __name__ == "__main__":
    main()
