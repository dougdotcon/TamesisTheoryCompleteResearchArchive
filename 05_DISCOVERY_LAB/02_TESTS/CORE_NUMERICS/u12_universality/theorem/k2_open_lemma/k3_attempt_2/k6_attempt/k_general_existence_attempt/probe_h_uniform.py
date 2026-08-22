"""
Same uniform-boundedness probe as probe_uniform.py, but for h_r(a,b) itself
(including at a=0, h_r's OWN boundary point -- the region symmetric to g_r's
m=b+r+1 boundary, and also the region g_r's own m=n extreme draws on).
"""
import sys
sys.setrecursionlimit(1000000)
import sympy as sp
from common import direct_gh, Hhat_closed, K_closed


def scan_h(r, b, n, sample_as=None):
    g, h = direct_gh(n, r)
    if sample_as is None:
        maxa = n - b - r - 2
        if maxa < 1:
            maxa = 1
        pts = sorted(set(int(round(maxa * i / 24)) for i in range(25)))
        sample_as = [a for a in pts if 0 <= a <= maxa]
    worst = (None, None)
    for a in sample_as:
        true_val = h(r, a, b)
        s0 = sp.Rational(a, n)
        approx = Hhat_closed(r, s0, b) + K_closed(r, s0, b) / n
        true_sym = sp.Rational(true_val.numerator, true_val.denominator)
        resid = true_sym - approx
        n2resid = float(resid * n * n)
        if worst[0] is None or abs(n2resid) > abs(worst[1]):
            worst = (a, n2resid)
    return worst


if __name__ == "__main__":
    for (r, b) in [(1, 0), (2, 0), (3, 0)]:
        print(f"=== h_{r} b={b} ===")
        for n in [50, 100, 200, 400]:
            worst = scan_h(r, b, n)
            print(f"  n={n:4d}  worst |n^2*resid_h| = {abs(worst[1]):.6f} at a={worst[0]} (s={worst[0]/n:.4f})")
