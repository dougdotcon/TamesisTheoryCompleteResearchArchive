"""ecoef2.py -- the compact closed form of e(c), and its exact coefficients.

The coefficients found in probe_taylor.py,
    e_j = (-1)^{j+1} (j-1)^2 / ( 2 (2j-1) j! ),   j >= 1,   e_0 = 0,
resum (ATTEMPT.md SS5.5) into

    e(c) = (1/2) int_0^1 [ 1 - (1 + c t^2 + c^2 t^4) e^{-c t^2} ] dt / t^2
         = (sqrt(c)/2) int_0^{sqrt c} [ 1 - (1+u^2+u^4) e^{-u^2} ] du / u^2 ,

from which  e(c) ~ (sqrt c / 2) * int_0^inf ... = (sqrt c/2)(sqrt(pi)/4)
= sqrt(pi c)/8  follows by an elementary three-term Gamma evaluation.
This script checks all three representations against each other.
"""

import sympy as sp
import mpmath as mp
from ecoef import e_of_c

mp.mp.dps = 40


def e_compact(c):
    c = mp.mpf(c)
    if c == 0:
        return mp.mpf(0)
    f = lambda t: (1 - (1 + c * t ** 2 + c ** 2 * t ** 4) * mp.e ** (-c * t * t)) / t ** 2
    return mp.quad(f, [0, 1]) / 2


def e_series(c, N=200):
    c = mp.mpf(c)
    s = mp.mpf(0)
    for j in range(1, N):
        s += (-1) ** (j + 1) * mp.mpf((j - 1) ** 2) / (2 * (2 * j - 1) * mp.factorial(j)) * c ** j
    return s


if __name__ == "__main__":
    print("=== ecoef2.py ===")
    print("\n--- three representations of e(c) ---")
    print("      c        SS5 integral        compact integral     power series")
    for c in [0.25, 1, 2, 3, 5, 10, 25, 60, 100]:
        a, b = e_of_c(c), e_compact(c)
        d = e_series(c) if c <= 25 else mp.mpf('nan')
        print("  %7s  %+.16f  %+.16f  %s"
              % (c, a, b, mp.nstr(d, 17) if d == d else "(series truncated)"))
        assert abs(a - b) < mp.mpf('1e-18'), (c, a, b)

    print("\n--- exact coefficient closed form e_j = (-1)^{j+1}(j-1)^2/(2(2j-1) j!) ---")
    j = sp.symbols('j')
    c = sp.symbols('c')
    N = 12
    def Iser(k):
        return sum((-c) ** m / (sp.factorial(m) * (2 * m + 2 * k + 1)) for m in range(N + 2))
    e = sp.expand((c * (Iser(0) - Iser(1)) + 2 * Iser(0) - 2) / 4 - c ** 2 / 2 * Iser(2))
    p = sp.Poly(e, c)
    allok = True
    for jj in range(1, N):
        got = sp.nsimplify(p.coeff_monomial(c ** jj))
        want = sp.Rational((-1) ** (jj + 1) * (jj - 1) ** 2, 2 * (2 * jj - 1) * sp.factorial(jj))
        ok = sp.simplify(got - want) == 0
        allok &= ok
        print("   j=%2d  e_j = %-22s  closed form %-22s  %s"
              % (jj, got, want, ok))
    print("  all match:", allok)

    print("\n--- the large-c constant: int_0^inf [1-(1+u^2+u^4)e^{-u^2}]/u^2 du ---")
    A = mp.quad(lambda u: (1 - (1 + u ** 2 + u ** 4) * mp.e ** (-u * u)) / u ** 2,
                [0, 1, mp.inf])
    print("   numerical A     = %s" % mp.nstr(A, 20))
    print("   sqrt(pi)/4      = %s" % mp.nstr(mp.sqrt(mp.pi) / 4, 20))
    print("   => e(c) ~ sqrt(pi c)/8 = %s * sqrt(c)" % mp.nstr(mp.sqrt(mp.pi) / 8, 12))
    print("\n   c            e(c)/sqrt(c)     sqrt(pi)/8 = %s" % mp.nstr(mp.sqrt(mp.pi) / 8, 12))
    for c in [10 ** k for k in range(2, 11)]:
        print("   %-12s %s" % (c, mp.nstr(e_of_c(c) / mp.sqrt(c), 12)))
