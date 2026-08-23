"""ref2_null_family.py -- how much of phi_RED's chi2 gain is specific to its
functional form, and how much would ANY correction of roughly the right size
buy?  (Referee report of the predecessor front, section 5.8, applied to this
front's own headline number.)

Method.  Take phi_EPSR (the formula of record) and multiply it by
(1 + a * g(cell)) for a ONE-PARAMETER family of generic, undated shapes g, with
a chosen to MINIMISE chi2 on the very grid being scored.  A zero-parameter
formula that beats the best one-parameter ad-hoc rescaling of its predecessor
is doing something the "any positive correction" objection cannot explain.

Also fits the single-constant "measured elevation" model the previous front
used: phi_V4 with P = P_lead*(1+a*rho) (one fitted parameter).
"""
import math
import sys

import numpy as np

import ref2_formula as F

# --- grid: (n,b,c, phi_mc, sem) ------------------------------------------
GRID_TGT = [
    (32768, 8, 10, 0.279944, 0.001045), (32768, 8, 40, 0.138028, 0.000506),
    (32768, 8, 160, 0.068857, 0.000251), (65536, 50, 10, 0.278910, 0.001005),
    (65536, 50, 50, 0.123341, 0.000462), (65536, 50, 150, 0.068806, 0.000253),
    (65536, 50, 400, 0.038341, 0.000144), (65536, 100, 10, 0.279245, 0.001043),
    (65536, 100, 50, 0.120783, 0.000449), (65536, 100, 150, 0.064180, 0.000237),
    (65536, 100, 400, 0.032920, 0.000122), (65536, 100, 600, 0.023201, 0.000085),
    (65536, 200, 5, 0.392217, 0.001427), (65536, 200, 20, 0.192938, 0.000717),
    (65536, 200, 60, 0.105143, 0.000392), (65536, 200, 150, 0.057935, 0.000216),
    (65536, 300, 150, 0.051624, 0.000194), (65536, 400, 100, 0.065915, 0.000245),
    (65536, 200, 600, 0.015106, 0.000056), (65536, 800, 100, 0.048962, 0.000188),
    (65536, 100, 1000, 0.013780, 0.000051), (65536, 400, 300, 0.020960, 0.000079),
    (131072, 200, 800, 0.017229, 0.000064), (131072, 400, 400, 0.024225, 0.000091),
]

SHAPES = {
    "rho": lambda b, c, n, rho: rho,
    "rho^2": lambda b, c, n, rho: rho ** 2,
    "rho/(1-rho)": lambda b, c, n, rho: rho / (1 - rho),
    "bc/n": lambda b, c, n, rho: b * c / n,
    "rho*bc/n": lambda b, c, n, rho: rho * b * c / n,
    "-ln(1-rho)": lambda b, c, n, rho: -math.log(1 - rho),
    "rho^2/(1-rho)": lambda b, c, n, rho: rho ** 2 / (1 - rho),
}


def run(grid, label):
    print("=" * 92)
    print("null-family test on %s (%d cells)" % (label, len(grid)))
    print("=" * 92)
    rows = []
    for (n, b, c, pm, sem) in grid:
        rho = float(F.rho_of(b, c, n))
        rows.append(dict(n=n, b=b, c=c, rho=rho, pm=pm, sem=sem,
                         EPSR=float(F.phi_EPSR(b, c, n)),
                         CAND=float(F.phi_CAND(b, c, n)),
                         RED=float(F.phi_RED(b, c, n)),
                         REDB=float(F.phi_REDB(b, c, n)),
                         RED2=float(F.phi_RED2(b, c, n)),
                         REDX=float(F.phi_REDX(b, c, n))))

    def chi2(vals):
        return sum(((r["pm"] - v) / r["sem"]) ** 2 for r, v in zip(rows, vals))

    print("  zero-parameter formulas:")
    for k in ("CAND", "EPSR", "RED", "REDB", "RED2", "REDX"):
        print("     %-6s chi2 = %9.2f   below-MC = %d/%d"
              % (k, chi2([r[k] for r in rows]),
                 sum(1 for r in rows if r["pm"] > r[k]), len(rows)))
    print("  one-parameter ad-hoc rescalings  phi_EPSR*(1 + a*g), a fitted on "
          "THIS grid:")
    best = None
    for name, g in SHAPES.items():
        gs = [g(r["b"], r["c"], r["n"], r["rho"]) for r in rows]
        # least squares in a: minimise sum ((pm - E(1+a g))/sem)^2
        A = sum((r["EPSR"] * gv / r["sem"]) ** 2 for r, gv in zip(rows, gs))
        B = sum((r["pm"] - r["EPSR"]) * r["EPSR"] * gv / r["sem"] ** 2
                for r, gv in zip(rows, gs))
        a = B / A
        v = [r["EPSR"] * (1 + a * gv) for r, gv in zip(rows, gs)]
        x = chi2(v)
        print("     g=%-14s a_hat=%+8.4f  chi2 = %9.2f   below-MC = %d/%d"
              % (name, a, x, sum(1 for r, vv in zip(rows, v) if r["pm"] > vv),
                 len(rows)))
        if best is None or x < best[1]:
            best = (name, x)
    print("  best 1-parameter ad-hoc family: g=%s, chi2=%.2f" % best)
    # one-parameter "measured constant elevation" model: P = P_lead*(1+a*rho)
    print("  one-parameter constant-elevation model  phi_CAND with "
          "P = P_lead*(1+a*rho):")
    bestP = None
    for a in np.linspace(0.0, 0.20, 41):
        v = []
        for r in rows:
            rho = r["rho"]
            P = (1 / (1 - rho)) * (1 + a * rho)
            c = r["c"]
            H = lambda t: F.H_closed(t, P)
            phiV4 = F._int01(lambda t: P * (1 - t) ** (P - 1)
                             * np.exp(-c * float(H(t))))
            v.append(float((1 - rho) * phiV4))
        x = chi2(v)
        if bestP is None or x < bestP[1]:
            bestP = (a, x)
    print("     best a = %.3f  chi2 = %.2f  (1 fitted parameter)" % bestP)


if __name__ == "__main__":
    run(GRID_TGT, "the TARGET's own recorded 24-cell grid (cheap triage)")
