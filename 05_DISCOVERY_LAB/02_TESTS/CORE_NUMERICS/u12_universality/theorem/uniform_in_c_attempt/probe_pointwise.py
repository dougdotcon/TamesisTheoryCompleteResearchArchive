"""probe_pointwise.py -- does n*(phi(n,c) - phi_infty(c)) converge to e(c)?

Also: float-engine precision audit (float64 vs longdouble vs exact Fraction),
and an exact-rational confirmation of [c^2] phi(n,c) = 1/10 - 1/(12 n) + O(1/n^2).
"""

from fractions import Fraction
import numpy as np
import mpmath as mp
from chain import phi_mixed_exact, phi_mixed_fast, phi_condK_exact
from ecoef import e_of_c, phi_inf

mp.mp.dps = 40


def audit_precision():
    print("--- precision audit: float64 vs longdouble vs exact ---")
    for n in (50, 200, 800):
        for c in (1.0, 5.0, 20.0):
            if c > n:
                continue
            a = phi_mixed_fast(n, c, dtype=np.float64)
            b = phi_mixed_fast(n, c, dtype=np.longdouble)
            line = "  n=%-5d c=%-5s f64=%.16f  |f64-f128|=%.2e" % (n, c, a, abs(a - b))
            if n <= 200:
                ex = float(phi_mixed_exact(n, Fraction(c).limit_denominator(10 ** 6)))
                line += "  |f64-exact|=%.2e" % abs(a - ex)
            print(line)


def pointwise():
    print("\n--- n * (phi(n,c) - phi_inf(c))  vs  e(c) ---")
    cs = [0.5, 1.0, 2.0, 5.0, 10.0, 25.0, 60.0]
    ns = [100, 400, 1600, 6400, 25600, 102400]
    print("      c    " + "".join("  n=%-11d" % n for n in ns) + "     e(c)")
    for c in cs:
        row = "  %6.2f " % c
        pinf = phi_inf(c)
        for n in ns:
            if c > n:
                row += "  %-13s" % "--"
                continue
            v = phi_mixed_fast(n, c, rmax=int(c + 12 * (c ** .5 + 1) + 60))
            row += "  %+-13.8f" % (n * (mp.mpf(v) - pinf))
        row += "   %+.8f" % e_of_c(c)
        print(row)


def taylor_c2():
    print("\n--- exact: [c^2] phi(n,c) = (n-1)/(2n) * (1 - 2 phi_n^(1) + phi_n^(2)) ---")
    print("    predicted 1/10 - 1/(12 n) + O(1/n^2)")
    print("      n      [c^2]phi(n,.) exact        n*([c^2]-1/10)      -> -1/12 = %.9f"
          % (-1 / 12))
    for n in (10, 20, 40, 80, 160, 320, 640):
        v = Fraction(n - 1, 2 * n) * (1 - 2 * phi_condK_exact(n, 1) + phi_condK_exact(n, 2))
        print("      %-6d %-26s %+.12f" % (n, str(v)[:26], float(n * (v - Fraction(1, 10)))))
    print("    (exact closed form: (n-1)/(2n) * (phi_n^(2) - 1/3 - 2/(3n^2)) )")


if __name__ == "__main__":
    print("=== probe_pointwise.py ===")
    audit_precision()
    pointwise()
    taylor_c2()
