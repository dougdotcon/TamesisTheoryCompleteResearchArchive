"""aggregation_closure_attempt -- stage 2: phi_V5, the aggregation-closed
candidate.

Derivation (full writeup: ATTEMPT.md sec 3): for x not in R, pi(x) is
EXACTLY uniform (continuum limit, n->infty, b fixed, up to O(b/n) short-
cycle corrections) over the N' = n-b+1 points NOT already exposed as
images along x's own backward pi-chain; a further independent factor
(1-c/n) applies for each such candidate to ALSO be not in R (checking "is
this candidate itself a seed" -- the only unconstrained mark). Hence, for
ANY random set Y_live of "live" (not-yet-closed, guaranteed not in R by
mechanism construction) closure targets whose membership is NOT causally
entangled with x's own current window (true by construction for the real
walk: Y_live's members are earlier, causally PRIOR arc starts, and the
current arc's own window can never overlap an earlier arc's start without
having already closed into it first):

    P(pi(x) in Y_live | x not in R) ~= |Y_live| * (1-c/n)^-(b-1) / n
                                      = |Y_live| * P / n,   P := (1-c/n)^-(b-1)

This directly validates the AGGREGATION step (multiplying a per-target
density by a target count) that residual_attempt/ATTEMPT.md sec 5 could not
close: lemma_direct_test.py / _v3_fullscale.py in this subfolder confirm
this formula on an EXOGENOUS random target set at full production scale
(n=65536) to chi2=1.93 across 4 stress cells (noise level, ~4 expected).

This is the SAME structural elevation phi_V4 (residual_attempt/
mclust_residual_v4.py) used empirically (P = 1/(1-rho) there), but DERIVED
here with the additional (1-c/n)^-(b-1) EXACT form instead of the
1/(1-rho)=(1-c/n)^-b leading-order simplification -- the two differ by
exactly one factor of (1-c/n), which is a ~0.5-1% effect at the most
extreme grid points (c/n up to ~0.0092) -- small, but this is precisely the
scale of the SECOND, unexplained residual residual_attempt/ATTEMPT.md sec 8
point 2 flagged as remaining after phi_CAND.

    q_CLUST(s) = s/(1-rho)                                    [wave 4, unchanged]
    P := (1-c/n)^-(b-1)                                       [this front, derived]
    H_v5(t) = t - (1-t)^P * int_0^t (1-q_CLUST(s)) (1-s)^-P ds
    phi_v5(c,n,b) = int_0^1 P (1-t)^(P-1) exp(-c H_v5(t)) dt
    phi_CAND5(c,n,b) := (1-rho) * phi_v5(c,n,b)               [x0-in-R dilution, unchanged]

Own implementation, does not import mclust_residual_v4.py or any other file
in ../residual_attempt/.
"""
import json
import math
import os

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
MCLUST_RIGOR = os.path.dirname(os.path.dirname(HERE))
RESIDUAL_ATTEMPT = os.path.dirname(HERE)


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


def phi_OLD(c, n, b):
    c_eff = c * (1.0 - c / n) ** b
    return phi_U(c_eff)


def q_clust(s, rho):
    return s / (1.0 - rho) if rho > 1e-12 else s


def elevation_P(c, n, b):
    """P := (1-c/n)^-(b-1), the DERIVED (not fitted) exact elevation
    exponent from the sequential-exposure lemma (ATTEMPT.md sec 3)."""
    return (1.0 - c / n) ** (-(b - 1))


def H_generic(t, rho, P, n_steps=400):
    """H(t) for hazard(s) = P/(1-s), general P (P=1/(1-rho) recovers
    residual_attempt/mclust_residual_v4.py's H_v4 exactly)."""
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    s_grid = np.linspace(0.0, t, n_steps + 1)
    integrand = (1.0 - q_clust(s_grid, rho)) * np.power(np.clip(1.0 - s_grid, 1e-15, None), -P)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    inner = trapz(integrand, s_grid)
    return t - ((1.0 - t) ** P) * inner


def phi_generic(c, n, b, P, n_outer=400, n_inner=250):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    t_grid = np.linspace(0.0, 1.0 - 1e-7, n_outer + 1)
    H_vals = np.array([H_generic(t, rho, P, n_inner) for t in t_grid])
    ES = np.power(np.clip(1.0 - t_grid, 1e-15, None), P) * np.exp(-c * H_vals)
    integrand_phi = ES * P / np.clip(1.0 - t_grid, 1e-15, None)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    return trapz(integrand_phi, t_grid)


def phi_V4(c, n, b, n_outer=400, n_inner=250):
    """Reproduced (own re-implementation, not imported) for side-by-side
    comparison: P = 1/(1-rho), residual_attempt/mclust_residual_v4.py."""
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    return phi_generic(c, n, b, 1.0 / (1.0 - rho), n_outer, n_inner)


def phi_V5(c, n, b, n_outer=400, n_inner=250):
    """This front's derived candidate: P = (1-c/n)^-(b-1)."""
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    return phi_generic(c, n, b, elevation_P(c, n, b), n_outer, n_inner)


def phi_CAND(c, n, b):
    """residual_attempt's candidate: (1-rho)*phi_V4."""
    rho = rho_of(c, n, b)
    return (1.0 - rho) * phi_V4(c, n, b)


def phi_CAND5(c, n, b):
    """This front's candidate: (1-rho)*phi_V5."""
    rho = rho_of(c, n, b)
    return (1.0 - rho) * phi_V5(c, n, b)


def main():
    print("# sanity checks")
    print("rho->0: phi_V5(c=50,n=1e9,b=1) =", phi_V5(50.0, 10 ** 9, 1),
          " vs phi_U(50) =", phi_U(50.0))
    print("elevation_P at rho=0:", elevation_P(50.0, 10 ** 9, 1), "(should be ~1)")

    rows = []

    # --- cheap reuse check 1: wave 4's own 15-cell grid (their seeds, their MC) ---
    with open(os.path.join(MCLUST_RIGOR, "mclust_validate_results.json")) as fh:
        d_wave4 = json.load(fh)
    print(f"\n== reuse check against wave4 mclust_validate_results.json (15 cells) ==")
    print(f"{'n':>7} {'b':>4} {'c':>7} {'rho':>7} | {'MC':>9} | "
          f"{'NEW dev%':>9} | {'CAND dev%':>9} | {'CAND5 dev%':>10}")
    for r in d_wave4["cells"]:
        n, b, c = r["n"], r["b"], r["c"]
        mc = r["phi_mc"]
        new = r["phi_new"]
        cand = phi_CAND(c, n, b)
        cand5 = phi_CAND5(c, n, b)
        dev = lambda x: (mc - x) / x * 100
        print(f"{n:7d} {b:4d} {c:7.1f} {r['rho_formula']:7.4f} | {mc:9.6f} | "
              f"{dev(new):9.2f} | {dev(cand):9.2f} | {dev(cand5):10.2f}")
        rows.append(dict(source="wave4_grid", n=n, b=b, c=c, rho=r["rho_formula"],
                          mc=mc, sem=r["sem"], phi_new=new, phi_cand=cand, phi_cand5=cand5,
                          dev_new_pct=dev(new), dev_cand_pct=dev(cand), dev_cand5_pct=dev(cand5)))

    # --- cheap reuse check 2: residual_attempt's own fresh-seed 18-cell grid ---
    with open(os.path.join(RESIDUAL_ATTEMPT, "mclust_residual_validate_results.json")) as fh:
        d_prev = json.load(fh)
    print(f"\n== reuse check against residual_attempt mclust_residual_validate_results.json (18 cells) ==")
    print(f"{'n':>7} {'b':>4} {'c':>7} {'rho':>7} | {'MC':>9} | "
          f"{'CAND dev%':>9} | {'CAND5 dev%':>10} | {'CAND z':>8} | {'CAND5 z':>8}")
    chi2_cand_reuse = 0.0
    chi2_cand5_reuse = 0.0
    for r in d_prev["cells"]:
        n, b, c = r["n"], r["b"], r["c"]
        mc = r["phi_mc"]
        sem = r["sem"]
        cand = phi_CAND(c, n, b)
        cand5 = phi_CAND5(c, n, b)
        dev = lambda x: (mc - x) / x * 100
        z_cand = (mc - cand) / sem
        z_cand5 = (mc - cand5) / sem
        chi2_cand_reuse += z_cand ** 2
        chi2_cand5_reuse += z_cand5 ** 2
        print(f"{n:7d} {b:4d} {c:7.1f} {r['rho']:7.4f} | {mc:9.6f} | "
              f"{dev(cand):9.2f} | {dev(cand5):10.2f} | {z_cand:8.2f} | {z_cand5:8.2f}")
        rows.append(dict(source="residual_attempt_grid", n=n, b=b, c=c, rho=r["rho"],
                          mc=mc, sem=sem, phi_cand=cand, phi_cand5=cand5,
                          dev_cand_pct=dev(cand), dev_cand5_pct=dev(cand5),
                          z_cand=z_cand, z_cand5=z_cand5))
    print(f"\nchi2 (CAND, reused 18-cell grid, PREVIOUSLY the final validation there): {chi2_cand_reuse:.2f}")
    print(f"chi2 (CAND5, same 18 cells): {chi2_cand5_reuse:.2f}")

    with open(os.path.join(HERE, "stage2_v5_reuse_check.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    print("\nsaved stage2_v5_reuse_check.json")


if __name__ == "__main__":
    main()
