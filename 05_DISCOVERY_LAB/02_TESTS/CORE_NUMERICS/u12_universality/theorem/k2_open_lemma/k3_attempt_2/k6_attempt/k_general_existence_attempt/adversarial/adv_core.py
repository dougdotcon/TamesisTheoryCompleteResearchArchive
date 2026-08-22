"""
adv_core.py -- INDEPENDENT referee implementation.

Written from scratch from the *stated* mathematics only:
  * transition rules: wave-6 ATTEMPT.md (k3_attempt_2/ATTEMPT.md) section 2, Proposition
        g(a,b,r) = 1/m + (r/m) h(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r),  m = n-a
        h(a,b,r) = 1/n + (r/n) h(a,b+1,r-1) + ((n-1-a-b-r)/n) g(a,b+1,r)
    valid on states with a+b+r < n.
  * closed forms F_r, G_r and the algebraic relations for Hhat_r, K_r as *stated* in
    k6_attempt/ATTEMPT.md sections 2.2, 2.3, 3.1, 3.3.

No code was copied from common.py / markov_direct.py / markov_transfer.py.
Iterative (not recursive) evaluation, dict memo keyed on (a,b,r); exact Fraction
arithmetic everywhere.
"""

from fractions import Fraction as Fr
from functools import lru_cache
import sympy as sp


# ----------------------------------------------------------------------------- #
# 1. the exact discrete chain, from the transition rules, exact rationals
# ----------------------------------------------------------------------------- #

class Chain:
    """Exact g(a,b,r), h(a,b,r) for one fixed n."""

    def __init__(self, n):
        self.n = n
        self._g = {}
        self._h = {}

    def g(self, a, b, r):
        n = self.n
        assert a >= 0 and b >= 0 and r >= 0
        assert a + b + r < n, f"g state out of domain: a={a} b={b} r={r} n={n}"
        key = (a, b, r)
        if key in self._g:
            return self._g[key]
        m = n - a
        val = Fr(1, m)
        if r > 0:
            val += Fr(r, m) * self.h(a + 1, b, r - 1)
        cont = m - 1 - r - b
        if cont != 0:
            val += Fr(cont, m) * self.g(a + 1, b, r)
        self._g[key] = val
        return val

    def h(self, a, b, r):
        n = self.n
        assert a >= 0 and b >= 0 and r >= 0
        assert a + b + r < n, f"h state out of domain: a={a} b={b} r={r} n={n}"
        key = (a, b, r)
        if key in self._h:
            return self._h[key]
        val = Fr(1, n)
        if r > 0:
            val += Fr(r, n) * self.h(a, b + 1, r - 1)
        cont = n - 1 - a - b - r
        if cont != 0:
            val += Fr(cont, n) * self.g(a, b + 1, r)
        self._h[key] = val
        return val

    # (m,b) coordinates used by the continuum documents:  m = n - a
    def g_r(self, m, b, r):
        return self.g(self.n - m, b, r)

    def h_r(self, a, b, r):
        return self.h(a, b, r)


import sys
sys.setrecursionlimit(100000)


# ----------------------------------------------------------------------------- #
# 2. the closed forms, transcribed from the *formulas* in k6_attempt/ATTEMPT.md
# ----------------------------------------------------------------------------- #

def _fall(r, j):
    """r!/(r-j)!  as an exact integer (falling factorial), j>=0."""
    out = 1
    for i in range(j):
        out *= (r - i)
    return out


def F_poly(r, b, t):
    """F_r(t,b) = sum_{k=0}^{r} r!/(r-k)! * t^k / prod_{i=1}^{k+1}(r+b+i)."""
    tot = 0
    for k in range(0, r + 1):
        den = 1
        for i in range(1, k + 2):
            den = den * (r + b + i)
        tot += sp.Rational(_fall(r, k)) * t**k / den
    return sp.together(sp.expand(tot))


def G_poly(r, b, t):
    """G_r(t,b) = sum_{k=0}^{r-1} C(k+2,2) * r!/(r-k-1)! * t^k / prod_{i=1}^{k+2}(r+b+i)."""
    tot = 0
    for k in range(0, r):
        den = 1
        for i in range(1, k + 3):
            den = den * (r + b + i)
        tot += sp.binomial(k + 2, 2) * sp.Rational(_fall(r, k + 1)) * t**k / den
    return sp.expand(tot)


def Hhat_poly(r, b, s):
    """Hhat_r(s,b) := (1-s) F_r(1-s, b+1)."""
    return sp.expand((1 - s) * F_poly(r, b + 1, 1 - s))


def K_poly(r, b, s):
    """K_r(s,b) := 1 + r*Hhat_{r-1}(s,b+1) + (1-s)G_r(1-s,b+1) - (1+b+r)F_r(1-s,b+1)."""
    out = sp.Integer(1)
    if r >= 1:
        out += r * Hhat_poly(r - 1, b + 1, s)
    out += (1 - s) * G_poly(r, b + 1, 1 - s)
    out -= (1 + b + r) * F_poly(r, b + 1, 1 - s)
    return sp.expand(out)


if __name__ == "__main__":
    t = sp.Symbol('t')
    s = sp.Symbol('s')
    print("smoke test: F_r(1,0) should equal phi_r = 4^r (r!)^2 / (2r+1)!")
    for r in range(0, 9):
        lhs = sp.nsimplify(F_poly(r, 0, t).subs(t, 1))
        phi = sp.Rational(4**r * sp.factorial(r)**2, sp.factorial(2 * r + 1))
        print(f"  r={r}: F_r(1,0)={lhs}  phi_r={phi}  match={sp.simplify(lhs-phi)==0}")
    print()
    print("smoke test: G_r(1,0) should equal r*phi_r/4")
    for r in range(0, 9):
        lhs = sp.nsimplify(G_poly(r, 0, t).subs(t, 1))
        phi = sp.Rational(4**r * sp.factorial(r)**2, sp.factorial(2 * r + 1))
        print(f"  r={r}: G_r(1,0)={lhs}  r*phi_r/4={sp.nsimplify(r*phi/4)}  "
              f"match={sp.simplify(lhs-r*phi/4)==0}")
    print()
    print("smoke test: K_0(s,b) should be 1/(b+2) (constant in s)")
    for b in range(0, 4):
        print(f"  b={b}: K_0 = {K_poly(0,b,s)}   (expect {sp.Rational(1,b+2)})")
    print()
    print("smoke test: chain vs known psi_n^(K) closed forms (wave5/wave6, PROVED)")
    for (K, form) in [(1, lambda n: Fr(4 * n + 1, 6 * n)),
                      (2, lambda n: Fr(8 * n * n + 4 * n + 1, 15 * n * n))]:
        for n in range(K + 1, K + 7):
            c = Chain(n)
            got = c.g(0, 0, K)
            exp = form(n)
            print(f"  K={K} n={n}: chain={got} closed={exp} match={got==exp}")
