"""residual_attempt -- stage A/B (DISC-DEC-033, front MCLUST-RESIDUAL-RIGOR).

Sanity check ONLY: reuses the MC values already recorded in
../mclust_validate_results.json (wave 4, own seeds SeedSequence(20260822018))
-- no new simulation here, exactly the same reuse discipline as
../mclust_decompose.py. Purpose: cheaply screen the candidate "next-order"
correction (between-chain R-depletion, X(s)) BEFORE spending a fresh
simulation budget on it in mclust_residual_validate.py.

Hypothesis under test (derived from scratch, see ATTEMPT.md sec 2-3):
wave 4's phi_NEW used q_CLUST(s) = s/(1-rho) treating rho as CONSTANT
throughout the walk (R-depletion negligible, justified by "each encounter
consumes ~1 R point, c*s/n << rho"). But EVERY "chain-continue" step ALSO
consumes a fresh R point, not just the terminating run-start step -- the
expected number of chain-continue consumptions per encounter is
rho/(1-rho), not 1. Accumulated over ~c*s encounters by arc-mass s, this
gives an extra depleted-R fraction

    x(s) = X(s)/n,   dx/ds = (c/n) * rho_eff(s)/(1-rho_eff(s))
    rho_eff(s) = rho - c*s/n - x(s)          (fresh R remaining/n)

which was explicitly flagged (but not tested) as a candidate next-order
term in DERIVATION_MCLUST_FIXED.md sec 6, bullet 2 ("o proximo termo
prop c*s/n ... nao testado separadamente").

This also requires the KILL probability itself to be corrected: a chain
draw at arc-mass s can land on mass already consumed by earlier chains'
continue-steps (x(s)) as well as ordinary arc mass (s) --

    kappa(s) = s + x(s)                       (true per-draw kill prob)
    q_CLUST_v2(s) = kappa(s) / (1 - rho_eff(s))

Everything reduces to wave 4's phi_NEW exactly when x(s) -> 0 (rho small
or c/n -> 0), so this is a genuine "next order" refinement, not a
different mechanism.
"""
import json
import math
import os

import numpy as np
from scipy import integrate
from scipy.interpolate import interp1d

HERE = os.path.dirname(os.path.abspath(__file__))
WAVE4 = os.path.join(os.path.dirname(HERE), "mclust_rigor")
# residual_attempt/ IS inside mclust_rigor/, so WAVE4 == HERE's parent is
# mclust_rigor itself when this script lives in residual_attempt/.
WAVE4 = os.path.dirname(HERE)


def phi_U(c):
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0, 1)
    return v


def rho_of(c, n, b):
    return 1.0 - (1.0 - c / n) ** b


def H_NEW(t, rho):
    """wave-4 phi_NEW integrand (rho held constant along the walk)."""
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    return t - (1.0 - t) * (t + rho * math.log(1.0 - t)) / (1.0 - rho)


def phi_NEW(c, n, b):
    rho = rho_of(c, n, b)
    v, _ = integrate.quad(lambda t: math.exp(-c * H_NEW(t, rho)), 0, 1, limit=200)
    return v


# --------------------------------------------------------- next-order (v2)
def solve_x(c, n, rho, n_steps=4000):
    """Integrate dx/ds = (c/n) * rho_eff/(1-rho_eff), rho_eff = rho - c s/n - x,
    x(0)=0, on s in [0,1), via RK4 on a uniform grid. Returns arrays
    (s_grid, x_grid, rho_eff_grid). Clips rho_eff to [0, 1-1e-9] defensively
    (should stay in range for the parameter grid tested; a clip event is
    reported by the caller if it ever triggers)."""
    s_grid = np.linspace(0.0, 1.0 - 1e-9, n_steps + 1)
    h = s_grid[1] - s_grid[0]
    x = np.empty(n_steps + 1)
    x[0] = 0.0
    clipped = False

    def deriv(s, xv):
        nonlocal clipped
        rho_eff = rho - c * s / n - xv
        if rho_eff < 0.0:
            rho_eff = 0.0
            clipped = True
        if rho_eff > 1.0 - 1e-9:
            rho_eff = 1.0 - 1e-9
            clipped = True
        return (c / n) * rho_eff / (1.0 - rho_eff)

    for i in range(n_steps):
        s = s_grid[i]
        k1 = deriv(s, x[i])
        k2 = deriv(s + h / 2, x[i] + h / 2 * k1)
        k3 = deriv(s + h / 2, x[i] + h / 2 * k2)
        k4 = deriv(s + h, x[i] + h * k3)
        x[i + 1] = x[i] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    rho_eff_grid = np.clip(rho - c * s_grid / n - x, 0.0, 1.0 - 1e-9)
    return s_grid, x, rho_eff_grid, clipped


def phi_V2(c, n, b, n_steps=4000, return_diag=False):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        v = phi_U(c)
        return (v, dict(x_max=0.0, clipped=False)) if return_diag else v
    s_grid, x_grid, rho_eff_grid, clipped = solve_x(c, n, rho, n_steps)
    kappa_grid = s_grid + x_grid
    q_grid = kappa_grid / (1.0 - rho_eff_grid)
    # (1-q(s))/(1-s) on the grid, then H(t) = t - (1-t) * cumulative_integral
    integrand = (1.0 - q_grid) / (1.0 - s_grid)
    # cumulative trapezoid
    cum = np.zeros_like(s_grid)
    cum[1:] = np.cumsum((integrand[1:] + integrand[:-1]) / 2.0 * np.diff(s_grid))
    H_grid = s_grid - (1.0 - s_grid) * cum
    H_grid[0] = 0.0
    integrand_phi = np.exp(-c * H_grid)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    v = trapz(integrand_phi, s_grid)
    # add the tiny [1-1e-9, 1] tail using H->1 continuity (negligible)
    if return_diag:
        return v, dict(x_max=x_grid[-1], rho_eff_min=rho_eff_grid[-1], clipped=clipped)
    return v


def main():
    with open(os.path.join(WAVE4, "mclust_validate_results.json")) as fh:
        d = json.load(fh)

    print(f"{'n':>7} {'b':>4} {'c':>7} {'rho':>7} {'bc/n':>8} | {'MC':>9} | "
          f"{'OLD dev%':>9} | {'NEW dev%':>9} | {'V2 dev%':>9} | {'x_max':>8}")
    rows = []
    for r in d["cells"]:
        n, b, c = r["n"], r["b"], r["c"]
        rho = r["rho_formula"]
        mc = r["phi_mc"]
        old = r["phi_old"]
        new = r["phi_new"]
        v2, diag = phi_V2(c, n, b, return_diag=True)
        dev = lambda x: (mc - x) / x * 100
        bcn = b * c / n
        print(f"{n:7d} {b:4d} {c:7.1f} {rho:7.4f} {bcn:8.4f} | {mc:9.6f} | "
              f"{dev(old):9.2f} | {dev(new):9.2f} | {dev(v2):9.2f} | {diag['x_max']:8.5f}"
              + ("  [CLIPPED]" if diag["clipped"] else ""))
        rows.append(dict(n=n, b=b, c=c, rho=rho, bcn=bcn, mc=mc, sem=r["sem"],
                          phi_old=old, phi_new=new, phi_v2=v2,
                          dev_old_pct=dev(old), dev_new_pct=dev(new),
                          dev_v2_pct=dev(v2), x_max=diag["x_max"],
                          clipped=diag["clipped"]))

    with open(os.path.join(HERE, "stageA_reuse_check.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    print("\nsaved stageA_reuse_check.json")


if __name__ == "__main__":
    main()
