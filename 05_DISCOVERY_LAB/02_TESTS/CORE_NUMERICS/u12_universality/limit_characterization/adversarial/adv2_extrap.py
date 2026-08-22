"""Surface (a) part 2: extrapolation of exact finite-n values to n->inf,
and exact small-c determination of the linear coefficient a1
(claim: phi ~ 1 - c/3; old archive form (1+c)^{-1/2} ~ 1 - c/2).

Uses only exact enumeration (adv2_exact.exact_mapsum) — no sampling.
"""
import json, math, sys
import numpy as np
from adv2_exact import exact_mapsum

ROOT = sys.path[0]

def phi_claim(c):
    return 0.5*math.sqrt(math.pi/c)*math.erf(math.sqrt(c))

if __name__ == "__main__":
    with open(ROOT + "/adv2_exact.json") as fh:
        data = json.load(fh)
    ns = np.array([4, 5, 6, 7], dtype=float)
    out = {"extrapolation": {}, "a1": {}}
    print("== extrapolation of exact n=4..7 to n->inf ==", flush=True)
    for c in data["cs"]:
        phis = np.array([data["exact"][str(int(n))][str(c)] for n in ns])
        target = phi_claim(c)
        # fit phi_n = A + B/n + C/n^2 (3 params, 4 points)
        X = np.vstack([np.ones_like(ns), 1/ns, 1/ns**2]).T
        coef, res, *_ = np.linalg.lstsq(X, phis, rcond=None)
        A3 = coef[0]
        # Richardson on 1/n from last pairs: R_n = n*phi_n - (n-1)*phi_{n-1}
        rich1 = ns[1:]*phis[1:] - ns[:-1]*phis[:-1]
        # second-level Richardson (eliminates 1/n and 1/n^2)
        m = ns[1:]
        rich2 = (m[1:]*rich1[1:] - (m[:-1]-0)*rich1[:-1]) / (m[1:]-m[:-1] + (m[1:]-m[1:]) ) if False else None
        out["extrapolation"][str(c)] = {
            "phis_n4_7": phis.tolist(),
            "fit_A_B_C": coef.tolist(),
            "extrap_2nd_order_fit": float(A3),
            "richardson_1n": rich1.tolist(),
            "claimed": target,
            "extrap_minus_claim": float(A3 - target),
            "dev_n7": float(phis[-1] - target),
        }
        print(f"c={c}: n=7 exact {phis[-1]:.6f} | fit A+B/n+C/n^2 -> A = {A3:.6f} | "
              f"claim {target:.6f} | A-claim = {A3-target:+.6f} | Richardson(6,7) = {rich1[-1]:.6f}", flush=True)

    print("== exact small-c linear coefficient a1 (claim 1/3 vs old 1/2) ==", flush=True)
    cs_small = [0.0625, 0.125, 0.25]
    a1_by_n = {}
    for n in [4, 5, 6, 7]:
        vals = {}
        for c in cs_small:
            vals[c] = exact_mapsum(n, c)
        # (1-phi)/c = a1 + a2*c + ... : fit quadratic in c through the three points, take intercept
        x = np.array(cs_small)
        y = np.array([(1 - vals[c]) / c for c in cs_small])
        # quadratic fit exact through 3 points
        p = np.polyfit(x, y, 2)
        a1n = p[2]
        a1_by_n[n] = {"vals": {str(c): vals[c] for c in cs_small}, "a1_intercept": float(a1n)}
        print(f"n={n}: (1-phi)/c at c={cs_small} -> {[f'{v:.6f}' for v in y]} ; intercept a1(n) = {a1n:.6f}", flush=True)
    # extrapolate a1(n) in 1/n (3-param fit over 4 points)
    a1s = np.array([a1_by_n[n]["a1_intercept"] for n in [4,5,6,7]])
    X = np.vstack([np.ones_like(ns), 1/ns, 1/ns**2]).T
    coef, *_ = np.linalg.lstsq(X, a1s, rcond=None)
    a1_inf = float(coef[0])
    out["a1"] = {"by_n": a1_by_n, "extrap_inf": a1_inf,
                 "claim_1_3": 1/3, "old_form_1_2": 0.5,
                 "dist_to_1_3": abs(a1_inf - 1/3), "dist_to_1_2": abs(a1_inf - 0.5)}
    print(f"a1(n) = {a1s.tolist()} -> extrapolated a1(inf) = {a1_inf:.6f}  "
          f"(claim 1/3 = {1/3:.6f}; old form would be 1/2)", flush=True)
    with open(ROOT + "/adv2_extrap.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("saved adv2_extrap.json")
