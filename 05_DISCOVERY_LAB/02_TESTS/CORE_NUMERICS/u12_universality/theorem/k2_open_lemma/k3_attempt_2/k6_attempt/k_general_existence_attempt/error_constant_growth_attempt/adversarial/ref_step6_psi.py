"""
STEP 6 -- two more independent cross-checks.

(6a) psi_n^{(K)} = g_K(n,0) is a polynomial in 1/n of degree K (a fact I do NOT
     assume: I fit degree K from K+1 values of n and then VALIDATE the fit
     out-of-sample on fresh n; a wrong degree would fail out-of-sample).  Its
     1/n^2 coefficient must equal H_K(1,0) if Corollary 2a is right.  All exact
     rational arithmetic, my own Chain, my own Lagrange interpolation.

(6b) the improved bound D'_r/D'_{r-1} pushed to r=45 (target claims 1.240).
"""

import sys
from fractions import Fraction as Fr

from ref_core import Ladder, Chain, peval
from ref_bivar import constants
from ref_step4_helpers import dstar_exact

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
RBIG = int(sys.argv[2]) if len(sys.argv) > 2 else 45

print("=" * 78)
print("STEP 6  psi_n^{(K)} interpolation, and the improved bound at large r")
print("=" * 78)


def lagrange_coeffs(pts):
    """pts = [(x_i, y_i)] ; return exact coefficient list of the interpolant."""
    n = len(pts)
    coeffs = [Fr(0)] * n
    for i, (xi, yi) in enumerate(pts):
        basis = [Fr(1)]
        den = Fr(1)
        for j, (xj, _) in enumerate(pts):
            if i == j:
                continue
            newb = [Fr(0)] * (len(basis) + 1)
            for k, c in enumerate(basis):
                newb[k] += c * (-xj)
                newb[k + 1] += c
            basis = newb
            den *= (xi - xj)
        for k in range(n):
            coeffs[k] += yi * basis[k] / den
    return coeffs


print()
print("(6a) exact 1/n-expansion of psi_n^{(K)} = g_K(n,0), from my own simulator")
lad = Ladder(KMAX + 1, 3)
for K in range(1, KMAX + 1):
    fit_n = list(range(K + 2, 2 * K + 4))[:K + 1]
    val_n = list(range(2 * K + 5, 2 * K + 10))
    pts = []
    for n in fit_n:
        ch = Chain(n, K, 0)
        pts.append((Fr(1, n), ch.g[(K, n, 0)]))
    co = lagrange_coeffs(pts)
    okoos = True
    for n in val_n:
        ch = Chain(n, K, 0)
        pred = sum(co[k] * Fr(1, n) ** k for k in range(len(co)))
        if pred != ch.g[(K, n, 0)]:
            okoos = False
    c2 = co[2] if len(co) > 2 else Fr(0)
    HK = peval(lad.H[(K, 0)], 1)
    print("   K=%d  fit on n=%s, validated out-of-sample on n=%s : %s"
          % (K, fit_n, val_n, "PASS" if okoos else "FAIL"))
    print("        expansion: " + " + ".join("%s/n^%d" % (co[k], k) if k else str(co[k])
                                             for k in range(len(co))))
    print("        1/n^2 coefficient = %-14s   H_K(1,0) = %-14s   match=%s"
          % (c2, HK, c2 == HK))

print()
print("(6b) improved bound at large r (Proposition 6)")
ladb = Ladder(RBIG + 2, 1)
D_o, C_o = constants(ladb, RBIG, 1, order=2, kappa=2, geo=False)
D_i, C_i = constants(ladb, RBIG, 1, order=2, kappa=1, geo=True)
print("      r     D'_r(0)          D'_r/D'_{r-1}   C'_r/C'_{r-1}   D_r/D_{r-1}   D*_r(0)")
for r in [30, 35, 40, 44, 45]:
    if r > RBIG:
        break
    print("   %5d %14.6g %14.6f %14.6f %14.4f %12.4f"
          % (r, float(D_i[(r, 0)]), float(D_i[(r, 0)] / D_i[(r - 1, 0)]),
             float(C_i[(r, 0)] / C_i[(r - 1, 0)]),
             float(D_o[(r, 0)] / D_o[(r - 1, 0)]), float(dstar_exact(r, 0))))
