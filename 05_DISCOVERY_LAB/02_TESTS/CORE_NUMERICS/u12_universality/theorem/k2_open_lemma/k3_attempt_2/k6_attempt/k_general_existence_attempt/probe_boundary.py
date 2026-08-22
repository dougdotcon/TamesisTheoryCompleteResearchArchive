"""
CRUX EXPERIMENT: is the base-case point m=b+r+1 (t=(b+r+1)/n -> 0 as n->inf)
consistent with the bulk two-term ansatz F_r(t,b)+(1/n)G_r(t,b) to O(1/n^2),
or does it carry a genuine O(1/n) discrepancy (a boundary layer)?

For fixed small r,b, compute g_r(b+r+1,b) exactly (direct recursion) for a
range of n, and compare to F_r(t0,b)+G_r(t0,b)/n at t0=(b+r+1)/n. Report
n*(true-approx) and n^2*(true-approx) to see which one stabilizes (converges
to a finite nonzero constant) as n grows -- that identifies the true order of
the residual at the boundary point.
"""
from fractions import Fraction as Frac
import sympy as sp
from common import direct_gh, F_closed, G_closed

def probe(r, b, ns):
    print(f"--- r={r} b={b} ---  (base point m=b+r+1={b+r+1})")
    for n in ns:
        m0 = b + r + 1
        if m0 > n:
            continue
        g, h = direct_gh(n, r)
        true_val = g(r, n - m0, b)  # g_r(m0,b), a=n-m0
        t0 = sp.Rational(m0, n)
        approx0 = F_closed(r, t0, b)
        approx1 = G_closed(r, t0, b) / n
        approx = approx0 + approx1
        true_sym = sp.Rational(true_val.numerator, true_val.denominator)
        resid = sp.nsimplify(true_sym - approx)
        resid_n = sp.nsimplify(resid * n)
        resid_n2 = sp.nsimplify(resid * n * n)
        print(f"  n={n:4d} t0={float(t0):.5f} true={true_val} resid={sp.simplify(resid)} "
              f"n*resid={float(resid_n):+.6f} n^2*resid={float(resid_n2):+.6f}")

if __name__ == "__main__":
    probe(1, 0, [3, 5, 10, 20, 40, 80, 160, 320])
    probe(2, 0, [4, 8, 16, 32, 64, 128, 256])
    probe(1, 1, [4, 8, 16, 32, 64, 128, 256])
