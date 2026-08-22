"""
Scan the WHOLE range of m (from base case m=b+r+1 up to m=n), for fixed
(r,b) and growing n, computing n^2*(g_r(m,b) - F_r(t,b) - G_r(t,b)/n) at
each m. If this stays uniformly bounded (does not blow up) as n grows, that
is direct numerical evidence FOR uniform O(1/n^2) existence of the two-term
expansion across the WHOLE domain (not just the bulk, not just the exact
base point) -- i.e. for a genuine discrete-Gronwall-type bound. If it grows
without bound near t->0, that pinpoints a real boundary layer.
"""
import sys
sys.setrecursionlimit(200000)
import sympy as sp
from common import direct_gh, F_closed, G_closed


def scan(r, b, n, sample_ms=None):
    g, h = direct_gh(n, r)
    m0 = b + r + 1
    if sample_ms is None:
        # log-spaced sample of m from m0 to n
        import math
        pts = sorted(set(
            int(round(m0 * (n / m0) ** (i / 24))) for i in range(25)
        ))
        sample_ms = [m for m in pts if m0 <= m <= n]
    worst = (None, None)
    rows = []
    for m in sample_ms:
        a = n - m
        true_val = g(r, a, b)
        t0 = sp.Rational(m, n)
        approx = F_closed(r, t0, b) + G_closed(r, t0, b) / n
        true_sym = sp.Rational(true_val.numerator, true_val.denominator)
        resid = true_sym - approx
        n2resid = float(resid * n * n)
        rows.append((m, float(t0), n2resid))
        if worst[0] is None or abs(n2resid) > abs(worst[1]):
            worst = (m, n2resid)
    return rows, worst


if __name__ == "__main__":
    for (r, b) in [(1, 0), (2, 0), (3, 0), (2, 1)]:
        print(f"=== r={r} b={b} ===")
        for n in [20, 50, 100, 200]:
            rows, worst = scan(r, b, n)
            print(f"  n={n:4d}  worst |n^2*resid| = {abs(worst[1]):.6f} at m={worst[0]} (t={worst[0]/n:.4f})")
        sys.stdout.flush()
