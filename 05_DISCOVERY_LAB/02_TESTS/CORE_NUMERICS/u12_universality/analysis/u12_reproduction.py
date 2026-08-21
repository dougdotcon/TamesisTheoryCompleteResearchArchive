"""
Frente u12-universality (DISC-CORE-NUMERICS-001 / DISC-DEC-013)
Reproducao INDEPENDENTE da alegacao U_1/2: phi(c) = (1+c)^(-1/2).

Implementacao propria, do zero (nao reutiliza codigo do arquivo):
- ensemble: permutacao uniforme + reroteamento Bernoulli(c/n) uniforme
- observavel: fracao de pontos ciclicos (peeling de Kahn, O(n))
- fit do expoente alpha em (1+c)^(-alpha), espelho do protocolo do
  arquivo (n=2000, nao ponderado) + fit-limite (n=4000, ponderado)
- comparacao de modelos concorrentes do Atlas (AIC), criterios
  pre-declarados em ../METHODOLOGY_NOTE.md

Uso:
  python3 u12_reproduction.py primary     # grade A1 + fits + AIC
  python3 u12_reproduction.py adversarial # 2o seed set + grade nova
"""

import json
import sys
import numpy as np
from scipy.optimize import curve_fit, minimize_scalar

# ---------------------------------------------------------------- ensemble

def sample_phi(n, c, rng):
    """Uma amostra de phi = fracao de pontos ciclicos do ensemble U_1/2."""
    f = rng.permutation(n)
    mask = rng.random(n) < (c / n)
    k = int(mask.sum())
    if k:
        f[mask] = rng.integers(0, n, size=k)
    # pontos ciclicos: peeling por grau de entrada (Kahn)
    indeg = np.bincount(f, minlength=n)
    stack = list(np.flatnonzero(indeg == 0))
    removed = 0
    while stack:
        v = stack.pop()
        removed += 1
        w = f[v]
        indeg[w] -= 1
        if indeg[w] == 0:
            stack.append(w)
    return (n - removed) / n


def run_grid(n_values, c_values, n_samples, seed_base):
    """Roda a grade; um substream de RNG por celula (n, c)."""
    ss = np.random.SeedSequence(seed_base)
    children = ss.spawn(len(n_values) * len(c_values))
    cells = []
    idx = 0
    for n in n_values:
        for c in c_values:
            rng = np.random.default_rng(children[idx]); idx += 1
            phis = np.array([sample_phi(n, c, rng) for _ in range(n_samples)])
            cells.append({
                "n": n, "c": c, "n_samples": n_samples,
                "phi_mean": float(phis.mean()),
                "phi_std": float(phis.std(ddof=1)),
                "phi_sem": float(phis.std(ddof=1) / np.sqrt(n_samples)),
                "phi_theory": float((1 + c) ** -0.5),
                "samples": phis.tolist(),
            })
            print(f"  n={n:5d} c={c:5.1f}  phi={phis.mean():.4f} "
                  f"+/- {phis.std(ddof=1)/np.sqrt(n_samples):.4f}  "
                  f"teoria={(1+c)**-0.5:.4f}", flush=True)
    return cells

# ---------------------------------------------------------------- fits

def power_law(c, alpha):
    return (1.0 + c) ** (-alpha)


def fit_alpha_unweighted(c_arr, phi_arr):
    popt, pcov = curve_fit(power_law, c_arr, phi_arr, p0=[0.5],
                           bounds=(0.05, 2.0))
    return float(popt[0]), float(np.sqrt(pcov[0, 0]))


def fit_alpha_weighted(c_arr, phi_arr, sem_arr):
    popt, pcov = curve_fit(power_law, c_arr, phi_arr, p0=[0.5],
                           sigma=sem_arr, absolute_sigma=True,
                           bounds=(0.05, 2.0))
    return float(popt[0]), float(np.sqrt(pcov[0, 0]))


def bootstrap_alpha(cells, n_boot, seed, weighted=False):
    """Bootstrap nao parametrico: reamostra as amostras de cada celula."""
    rng = np.random.default_rng(seed)
    c_arr = np.array([cell["c"] for cell in cells])
    samples = [np.array(cell["samples"]) for cell in cells]
    alphas = []
    for _ in range(n_boot):
        means, sems = [], []
        for s in samples:
            idx = rng.integers(0, len(s), size=len(s))
            b = s[idx]
            means.append(b.mean())
            sems.append(b.std(ddof=1) / np.sqrt(len(b)))
        try:
            if weighted:
                a, _ = fit_alpha_weighted(c_arr, np.array(means), np.array(sems))
            else:
                a, _ = fit_alpha_unweighted(c_arr, np.array(means))
            alphas.append(a)
        except RuntimeError:
            pass
    alphas = np.array(alphas)
    return {
        "n_boot_ok": int(len(alphas)),
        "alpha_median": float(np.median(alphas)),
        "ci95": [float(np.percentile(alphas, 2.5)),
                 float(np.percentile(alphas, 97.5))],
    }

# ------------------------------------------------- comparacao de modelos

def chi2(model_vals, phi, sem):
    return float(np.sum(((phi - model_vals) / sem) ** 2))


def fit_1param(fun, c, phi, sem, lo, hi):
    """Minimiza chi2 de um modelo de 1 parametro por busca escalar."""
    res = minimize_scalar(
        lambda p: chi2(fun(c, p), phi, sem), bounds=(lo, hi),
        method="bounded", options={"xatol": 1e-10})
    return float(res.x), chi2(fun(c, res.x), phi, sem)


def model_comparison(cells):
    """Ajusta as formas do Atlas aos mesmos dados; AIC = chi2 + 2k."""
    c = np.array([cell["c"] for cell in cells])
    phi = np.array([cell["phi_mean"] for cell in cells])
    sem = np.array([cell["phi_sem"] for cell in cells])
    out = {}

    # U_1/2 fixa (0 params)
    x2 = chi2((1 + c) ** -0.5, phi, sem)
    out["U_half_fixed"] = {"form": "(1+c)^(-1/2)", "k": 0,
                           "chi2": x2, "aic": x2}
    # U_1/2 livre (1 param)
    a, x2 = fit_1param(lambda c, p: (1 + c) ** (-p), c, phi, sem, 0.05, 2.0)
    out["U_half_free"] = {"form": "(1+c)^(-alpha)", "k": 1,
                          "alpha": a, "chi2": x2, "aic": x2 + 2}
    # U_1 exponencial: literal e livre
    x2 = chi2(np.exp(-c), phi, sem)
    out["U1_exp_literal"] = {"form": "exp(-c)", "k": 0, "chi2": x2, "aic": x2}
    lam, x2 = fit_1param(lambda c, p: np.exp(-p * c), c, phi, sem, 1e-4, 5.0)
    out["U1_exp_free"] = {"form": "exp(-lambda*c)", "k": 1,
                          "lambda": lam, "chi2": x2, "aic": x2 + 2}
    # U_2 Lindblad: literal e livre
    x2 = chi2((1 + c) ** -2.0, phi, sem)
    out["U2_lindblad_literal"] = {"form": "(1+c)^(-2)", "k": 0,
                                  "chi2": x2, "aic": x2}
    b, x2 = fit_1param(lambda c, p: (1 + p * c) ** -2.0, c, phi, sem,
                       1e-4, 5.0)
    out["U2_lindblad_free"] = {"form": "(1+beta*c)^(-2)", "k": 1,
                               "beta": b, "chi2": x2, "aic": x2 + 2}
    # U_inf multi-threshold: 1/(1+c^m), m livre
    m, x2 = fit_1param(lambda c, p: 1.0 / (1 + c ** p), c, phi, sem,
                       0.05, 8.0)
    out["Uinf_free"] = {"form": "1/(1+c^m)", "k": 1, "m": m,
                        "chi2": x2, "aic": x2 + 2}
    # U_0 threshold: phi=1 se c<c*, b se c>=c*  (2 params: c*, b)
    best = None
    cs_grid = np.linspace(0.01, 60.0, 2400)
    for cstar in cs_grid:
        lo_mask = c < cstar
        vals = np.where(lo_mask, 1.0, 0.0)
        hi_mask = ~lo_mask
        if hi_mask.sum() > 0:
            w = 1.0 / sem[hi_mask] ** 2
            b = float(np.sum(w * phi[hi_mask]) / np.sum(w))  # WLS otimo
        else:
            b = 0.0
        vals = np.where(lo_mask, 1.0, b)
        x2 = chi2(vals, phi, sem)
        if best is None or x2 < best[2]:
            best = (float(cstar), b, x2)
    out["U0_threshold"] = {"form": "1 se c<c*, b se c>=c*", "k": 2,
                           "c_star": best[0], "b": best[1],
                           "chi2": best[2], "aic": best[2] + 4}
    return out

# ---------------------------------------------------------------- runs

C_MIRROR = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]


def run_primary():
    print("=== GRADE PRIMARIA A1 (seed base 20260821) ===", flush=True)
    cells = run_grid([500, 1000, 2000, 4000], C_MIRROR, 200, 20260821)

    result = {"protocol": "primary", "seed_base": 20260821,
              "n_values": [500, 1000, 2000, 4000], "c_values": C_MIRROR,
              "n_samples": 200}

    # R1b: erro absoluto medio vs teoria em todas as celulas
    errs = [abs(cell["phi_mean"] - cell["phi_theory"]) for cell in cells]
    result["R1b_mean_abs_error"] = float(np.mean(errs))
    result["R1b_pass"] = bool(np.mean(errs) < 0.05)

    # Fit-espelho: n=2000, nao ponderado (protocolo do arquivo)
    cells2000 = [cell for cell in cells if cell["n"] == 2000]
    c_arr = np.array([cell["c"] for cell in cells2000])
    phi_arr = np.array([cell["phi_mean"] for cell in cells2000])
    a, s = fit_alpha_unweighted(c_arr, phi_arr)
    boot = bootstrap_alpha(cells2000, 2000, 424242, weighted=False)
    result["fit_mirror_n2000"] = {"alpha": a, "sigma_curvefit": s,
                                  "bootstrap": boot}
    lo, hi = boot["ci95"]
    overlap_half = lo <= 0.5 <= hi
    overlap_archive = (lo <= 0.541) and (hi >= 0.475)
    close_criterion = abs(a - 0.5) < 0.05
    result["R1a_pass"] = bool((overlap_half or close_criterion)
                              and overlap_archive)

    # Fit-limite: n=4000, ponderado
    cells4000 = [cell for cell in cells if cell["n"] == 4000]
    c4 = np.array([cell["c"] for cell in cells4000])
    p4 = np.array([cell["phi_mean"] for cell in cells4000])
    s4 = np.array([cell["phi_sem"] for cell in cells4000])
    a4, sig4 = fit_alpha_weighted(c4, p4, s4)
    boot4 = bootstrap_alpha(cells4000, 2000, 434343, weighted=True)
    result["fit_limit_n4000"] = {"alpha": a4, "sigma_curvefit": sig4,
                                 "bootstrap": boot4}
    lo4, hi4 = boot4["ci95"]
    result["R1c_pass"] = bool(lo4 <= 0.5 <= hi4)

    # fits por n (descritivo, tendencia de tamanho finito)
    per_n = {}
    for n in [500, 1000, 2000, 4000]:
        cn = [cell for cell in cells if cell["n"] == n]
        an, sn = fit_alpha_unweighted(
            np.array([cell["c"] for cell in cn]),
            np.array([cell["phi_mean"] for cell in cn]))
        per_n[str(n)] = {"alpha": an, "sigma": sn}
    result["alpha_by_n_unweighted"] = per_n

    # R2: comparacao de modelos em n=4000
    mc = model_comparison(cells4000)
    result["model_comparison_n4000"] = mc
    aic_ref = mc["U_half_fixed"]["aic"]
    competitors = ["U0_threshold", "U1_exp_free", "U2_lindblad_free",
                   "Uinf_free"]
    dA = {k: mc[k]["aic"] - aic_ref for k in competitors}
    result["delta_aic_vs_U_half_fixed"] = dA
    result["R2_pass"] = bool(all(v >= 10.0 for v in dA.values()))
    result["R2_not_distinct_from"] = [k for k, v in dA.items() if v < 10.0]

    # remove amostras brutas do JSON principal (mantem so estatisticas)
    for cell in cells:
        del cell["samples"]
    result["cells"] = cells

    with open("result_primary.json", "w") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps({k: v for k, v in result.items() if k != "cells"},
                     indent=2))
    return result


def run_adversarial():
    print("=== GRADE ADVERSARIAL (seed base 777, grade nova) ===", flush=True)
    n_vals = [300, 800, 3000]
    c_vals = [0.3, 0.7, 1.5, 3.0, 7.0, 15.0, 30.0]
    cells = run_grid(n_vals, c_vals, 300, 777)
    result = {"protocol": "adversarial", "seed_base": 777,
              "n_values": n_vals, "c_values": c_vals, "n_samples": 300}

    errs = [abs(cell["phi_mean"] - cell["phi_theory"]) for cell in cells]
    result["R1b_mean_abs_error"] = float(np.mean(errs))
    result["R1b_pass"] = bool(np.mean(errs) < 0.05)

    cells3000 = [cell for cell in cells if cell["n"] == 3000]
    c3 = np.array([cell["c"] for cell in cells3000])
    p3 = np.array([cell["phi_mean"] for cell in cells3000])
    s3 = np.array([cell["phi_sem"] for cell in cells3000])
    a3, sig3 = fit_alpha_weighted(c3, p3, s3)
    boot3 = bootstrap_alpha(cells3000, 2000, 515151, weighted=True)
    result["fit_limit_n3000"] = {"alpha": a3, "sigma_curvefit": sig3,
                                 "bootstrap": boot3}
    lo3, hi3 = boot3["ci95"]
    result["R1c_pass"] = bool(lo3 <= 0.5 <= hi3)

    mc = model_comparison(cells3000)
    result["model_comparison_n3000"] = mc
    aic_ref = mc["U_half_fixed"]["aic"]
    competitors = ["U0_threshold", "U1_exp_free", "U2_lindblad_free",
                   "Uinf_free"]
    dA = {k: mc[k]["aic"] - aic_ref for k in competitors}
    result["delta_aic_vs_U_half_fixed"] = dA
    result["R2_pass"] = bool(all(v >= 10.0 for v in dA.values()))
    result["R2_not_distinct_from"] = [k for k, v in dA.items() if v < 10.0]

    for cell in cells:
        del cell["samples"]
    result["cells"] = cells
    with open("result_adversarial.json", "w") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps({k: v for k, v in result.items() if k != "cells"},
                     indent=2))
    return result


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "primary"
    if mode == "primary":
        run_primary()
    elif mode == "adversarial":
        run_adversarial()
    else:
        raise SystemExit(f"modo desconhecido: {mode}")
