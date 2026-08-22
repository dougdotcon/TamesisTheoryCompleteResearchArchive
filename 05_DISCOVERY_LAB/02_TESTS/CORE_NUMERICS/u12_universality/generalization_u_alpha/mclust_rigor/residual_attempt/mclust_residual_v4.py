"""residual_attempt -- stage E (DISC-DEC-033).

Third candidate correction, motivated by TWO independent lines of
evidence developed in ATTEMPT.md secs 3-6:

  1. A properly-conditioned (sliding-window-style, same technique wave 4
     used for the encounter rate) calculation of P(pi(x)=y | x not in R,
     y not in R) for a fixed target y gives, to leading order in c/n,
     (1/n)/(1-rho) -- i.e. a MULTIPLICATIVE elevation of the per-target
     closure hazard by 1/(1-rho), not the pool-SUBTRACTION model
     1/(1-s-rho) tried in mclust_residual_v3.py (which reduced exactly,
     and unhelpfully, to the already-refuted phi_OLD).

  2. Direct-walk empirical measurement (mclust_walk_diagnostic.py):
     inverting the survival curve S(t) to extract H_true(t) directly
     from the mechanism and comparing its small-t (leading quadratic)
     behavior to wave 4's H_NEW(t) shows the TRUE quadratic coefficient
     of H(t) sits close to 1/(1-rho) across the 3 stress cells tested
     (rho=0.26,0.37,0.46: empirical ~1.4-1.9 vs wave-4's predicted
     (1-rho/2)/(1-rho) ~1.18-1.42, vs candidate 1/(1-rho) ~1.36-1.85 --
     matching within roughly 2-10%, notably closer than wave 4's form).

Candidate model: keep q_CLUST(s) = s/(1-rho) EXACTLY as wave 4 derived
(independently re-validated in mclust_walk_diagnostic.py stage: both the
per-draw kill probability and the chain-level eventual-kill probability
match s and s/(1-rho) respectively, to within a few percent, no
systematic bias found there) but replace the STANDARD hazard 1/(1-s)
(inherited unmodified from M-U, wave 4 sec 4) with the MULTIPLICATIVELY
elevated hazard(s) = 1/[(1-rho)(1-s)], over the ORIGINAL domain t in
[0,1) (no truncation -- this is the key structural difference from
mclust_residual_v3.py's 1/(1-s-rho) model, which forced truncation to
t in [0,1-rho) and collapsed to phi_OLD).

    F(s) = (1-q_CLUST(s)) * [(1-t)/(1-s)]^(1/(1-rho))
    H_v4(t) = t - (1-t)^(1/(1-rho)) * int_0^t (1-q_CLUST(s))*(1-s)^(-1/(1-rho)) ds
    E[S(t)] = (1-t)^(1/(1-rho)) * exp(-c*H_v4(t))
    phi_v4(c) = int_0^1 E[S(t)] / [(1-rho)(1-t)] dt

No closed form found (unlike phi_NEW / phi_v3); integrated numerically.
Consistency checks: rho->0 recovers 1/(1-rho)->1, H_v4->H_NEW->t^2
(pure M-U); implemented so H_v4(0)=0 and (empirically checked below)
H_v4(1^-) -> 1 as required by the general theory.
"""
import json
import math
import os

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
WAVE4 = os.path.dirname(HERE)


def phi_U(c):
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0, 1)
    return v


def rho_of(c, n, b):
    return 1.0 - (1.0 - c / n) ** b


def H_NEW(t, rho):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    return t - (1.0 - t) * (t + rho * math.log(1.0 - t)) / (1.0 - rho)


def phi_NEW(c, n, b):
    rho = rho_of(c, n, b)
    v, _ = integrate.quad(lambda t: math.exp(-c * H_NEW(t, rho)), 0, 1, limit=200)
    return v


def q_clust(s, rho):
    return s / (1.0 - rho) if rho > 1e-12 else s


def H_v4(t, rho, n_steps=400):
    """Numeric integral (no closed form): t - (1-t)^p * int_0^t (1-q(s))(1-s)^{-p} ds,
    p = 1/(1-rho)."""
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    p = 1.0 / (1.0 - rho)
    s_grid = np.linspace(0.0, t, n_steps + 1)
    integrand = (1.0 - q_clust(s_grid, rho)) * np.power(np.clip(1.0 - s_grid, 1e-15, None), -p)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    inner = trapz(integrand, s_grid)
    return t - ((1.0 - t) ** p) * inner


def phi_V4(c, n, b, n_outer=400, n_inner=250, return_diag=False):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        v = phi_U(c)
        return (v, dict(H_end=1.0)) if return_diag else v
    p = 1.0 / (1.0 - rho)
    t_grid = np.linspace(0.0, 1.0 - 1e-7, n_outer + 1)
    H_vals = np.array([H_v4(t, rho, n_inner) for t in t_grid])
    ES = np.power(np.clip(1.0 - t_grid, 1e-15, None), p) * np.exp(-c * H_vals)
    integrand_phi = ES / ((1.0 - rho) * np.clip(1.0 - t_grid, 1e-15, None))
    trapz = getattr(np, "trapezoid", None) or np.trapz
    v = trapz(integrand_phi, t_grid)
    if return_diag:
        return v, dict(H_end=H_vals[-1], t_end=t_grid[-1])
    return v


def main():
    with open(os.path.join(WAVE4, "mclust_validate_results.json")) as fh:
        d = json.load(fh)

    # sanity: rho->0 check and H(1^-)->1 check on one representative rho
    print("sanity: rho=0.3 H_v4 near t=1:",
          H_v4(0.999, 0.3), " (should be close to 1)")
    print("sanity: rho->0 phi_v4(c=50) vs phi_U(50):",
          phi_V4(50.0, 10**9, 1), phi_U(50.0))

    print(f"\n{'n':>7} {'b':>4} {'c':>7} {'rho':>7} {'bc/n':>8} | {'MC':>9} | "
          f"{'OLD dev%':>9} | {'NEW dev%':>9} | {'V4 dev%':>9}")
    rows = []
    for r in d["cells"]:
        n, b, c = r["n"], r["b"], r["c"]
        rho = r["rho_formula"]
        mc = r["phi_mc"]
        old = r["phi_old"]
        new = r["phi_new"]
        v4 = phi_V4(c, n, b)
        dev = lambda x: (mc - x) / x * 100
        bcn = b * c / n
        print(f"{n:7d} {b:4d} {c:7.1f} {rho:7.4f} {bcn:8.4f} | {mc:9.6f} | "
              f"{dev(old):9.2f} | {dev(new):9.2f} | {dev(v4):9.2f}")
        rows.append(dict(n=n, b=b, c=c, rho=rho, bcn=bcn, mc=mc, sem=r["sem"],
                          phi_old=old, phi_new=new, phi_v4=v4,
                          dev_old_pct=dev(old), dev_new_pct=dev(new),
                          dev_v4_pct=dev(v4)))

    with open(os.path.join(HERE, "stageE_v4_reuse_check.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    print("\nsaved stageE_v4_reuse_check.json")


if __name__ == "__main__":
    main()
