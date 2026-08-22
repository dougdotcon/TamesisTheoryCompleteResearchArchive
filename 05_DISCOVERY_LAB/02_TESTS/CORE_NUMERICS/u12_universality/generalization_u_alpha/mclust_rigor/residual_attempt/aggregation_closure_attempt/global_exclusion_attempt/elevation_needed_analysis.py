"""global_exclusion_attempt -- stage 1b (analysis, no new simulation):
for each of the 4 stress cells measured directly in
global_exclusion_walk_measure.py, solve for P_needed -- the CONSTANT
elevation exponent that would make the standard phi_CAND-style formula
(hazard(s) = P/(1-s), q_CLUST(s)=s/(1-rho), (1-rho) x0-in-R dilution)
exactly match the true phi_mc value already recorded (with fresh seeds) in
aggregation_closure_attempt/mclust_aggregation_validate_results.json for
these same 4 cells (they are 4 of that script's 18; reused here, not a new
simulation -- cheap analysis only) -- then compares P_needed against the
DIRECTLY MEASURED elev_shallow / elev_deep from
global_exclusion_walk_measure_results.json.

This is the decisive check for whether a depth-dependent RE-WEIGHTING of
the already-measured elevation (the mechanism named in ATTEMPT.md sec 7.2)
could, in principle, close the residual: if P_needed sits between
elev_shallow and elev_deep, a plausible depth-weighted average could reach
it; if P_needed exceeds BOTH, no re-weighting of the measured quantities
can close the gap for that cell, regardless of how depth is weighted.

Own implementation. No new seeds used (root-finds a deterministic function
against already-recorded MC means; does not draw any new random numbers).
"""
import json
import os

import numpy as np
from scipy import optimize

from mclust_global_formula import phi_U, q_clust, rho_of

HERE = os.path.dirname(os.path.abspath(__file__))
AGG = os.path.dirname(HERE)


def H_constP(t, rho, P, n_steps=400):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    s_grid = np.linspace(0.0, t, n_steps + 1)
    integrand = (1.0 - q_clust(s_grid, rho)) * np.power(np.clip(1.0 - s_grid, 1e-15, None), -P)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    inner = trapz(integrand, s_grid)
    return t - ((1.0 - t) ** P) * inner


def phi_constP_diluted(c, n, b, P, n_outer=350, n_inner=200):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    t_grid = np.linspace(0.0, 1.0 - 1e-7, n_outer + 1)
    H_vals = np.array([H_constP(t, rho, P, n_inner) for t in t_grid])
    ES = np.power(np.clip(1.0 - t_grid, 1e-15, None), P) * np.exp(-c * H_vals)
    integrand_phi = ES * P / np.clip(1.0 - t_grid, 1e-15, None)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    v = trapz(integrand_phi, t_grid)
    return (1.0 - rho) * v


def main():
    with open(os.path.join(AGG, "mclust_aggregation_validate_results.json")) as fh:
        agg = json.load(fh)
    with open(os.path.join(HERE, "global_exclusion_walk_measure_results.json")) as fh:
        walk = json.load(fh)

    stress = [(100, 400.0), (300, 150.0), (100, 600.0), (400, 100.0)]
    agg_by_bc = {(r["b"], r["c"]): r for r in agg["cells"]}
    walk_by_bc = {(r["b"], r["c"]): r for r in walk["cells"]}

    rows = []
    print(f"{'b':>4} {'c':>7} | {'P_needed':>9} | {'P_lead':>7} {'P_exact':>8} | "
          f"{'elev_shallow':>12} {'elev_deep':>9} | verdict")
    for (b, c) in stress:
        a = agg_by_bc[(b, c)]
        w = walk_by_bc[(b, c)]
        n = a["n"]
        mc = a["phi_mc"]

        def f(P, c=c, n=n, b=b, mc=mc):
            return phi_constP_diluted(c, n, b, P) - mc

        P_needed = optimize.brentq(f, 1.0, 8.0, xtol=1e-5)
        es = w["elev_by_depth"][0]
        ed = w["elev_by_depth"][1]
        sem_s = w["sem_by_depth"][0]
        sem_d = w["sem_by_depth"][1]
        hi = max(es, ed)
        lo = min(es, ed)
        if P_needed <= hi + 2 * max(sem_s, sem_d):
            verdict = "reachable (P_needed within/near measured range)"
        else:
            gap_pct = (P_needed - hi) / hi * 100
            verdict = f"UNREACHABLE: exceeds both by {gap_pct:.1f}% (not closeable by depth reweighting alone)"
        print(f"{b:4d} {c:7.1f} | {P_needed:9.4f} | "
              f"{1.0/(1.0-rho_of(c,n,b)):7.4f} {(1.0-c/n)**(-(b-1)):8.4f} | "
              f"{es:8.3f}+-{sem_s:.3f} {ed:6.3f}+-{sem_d:.3f} | {verdict}")
        rows.append(dict(b=b, c=c, n=n, mc=mc, sem_mc=a["sem"], P_needed=P_needed,
                          P_lead=1.0 / (1.0 - rho_of(c, n, b)),
                          P_exact=(1.0 - c / n) ** (-(b - 1)),
                          elev_shallow=es, elev_deep=ed,
                          sem_shallow=sem_s, sem_deep=sem_d, verdict=verdict))

    with open(os.path.join(HERE, "elevation_needed_analysis_results.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    print("\nsaved elevation_needed_analysis_results.json")


if __name__ == "__main__":
    main()
