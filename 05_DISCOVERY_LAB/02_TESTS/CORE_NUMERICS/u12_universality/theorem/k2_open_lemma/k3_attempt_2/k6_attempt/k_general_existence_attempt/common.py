"""
Shared exact-arithmetic building blocks for the general-existence attempt.

- direct_g / direct_h: exact fractions.Fraction memoized recursion implementing
  ../ATTEMPT.md sec 2's Proposition verbatim (the SAME transition rules already
  proved and independently checked against brute force upstream). No summation,
  no symbolic algebra -- a plain recursion, general in (n, r, b).
- F_r, G_r, Hhat_r, K_r: the closed forms PROVED in k6_attempt/ATTEMPT.md
  Theorem sec 2.3 (F_r), sec 3.3 (G_r), and the algebraic Relations of sec 2.2/3.1
  (Hhat_r, K_r), reproduced here from the stated formulas (not re-derived) using
  sympy.Rational / symbolic b, so they can be evaluated exactly at any rational
  t=m/n and any concrete integer or symbolic b.

All arithmetic is exact (Fraction or sympy.Rational) -- no floating point is
used in any computation whose result is asserted to be exact.
"""
from fractions import Fraction as Frac
from functools import lru_cache
import sympy as sp

t, s, b_sym, r_sym, k_sym = sp.symbols('t s b r k', positive=False)


def direct_gh(n, K, bmax=6):
    """
    Return memoized callables g(m,b), h(a,b) computing g_K-level / general-r
    values via the SAME two-function ladder as ../markov_direct.py, but exposing
    g_r(m,b), h_r(a,b) for every r=0..K and a range of b, not just b=0.
    n: python int. Returns (g, h) where g(r,m,b) and h(r,a,b) are exact Fraction
    memoized functions of (r,m,b) resp. (r,a,b), valid for 0<=r<=K.
    """
    n_ = Frac(n)

    @lru_cache(maxsize=None)
    def g(r, a, b):
        # g_r(m,b) with m=n-a; recursion is on 'a' (# of pi-queries so far)
        m = n_ - a
        if m <= b + r:
            raise ValueError(f"g called out of domain: r={r} a={a} b={b} m={m}")
        term = Frac(1, 1) / m
        if r >= 1:
            term += Frac(r, 1) / m * h(r - 1, a + 1, b)
        frac_cont = (m - 1 - r - b) / m
        if frac_cont != 0:
            term += frac_cont * g(r, a + 1, b)
        return term

    @lru_cache(maxsize=None)
    def h(r, a, b):
        term = Frac(1, 1) / n_
        if r >= 1:
            term += Frac(r, 1) / n_ * h(r - 1, a, b + 1)
        frac_cont = (n_ - 1 - a - b - r) / n_
        if frac_cont != 0:
            term += frac_cont * g(r, a, b + 1)
        return term

    return g, h


# ---------------------------------------------------------------------------
# Closed forms from k6_attempt/ATTEMPT.md, reproduced verbatim (not re-derived)
# ---------------------------------------------------------------------------

def F_closed(r, tt, bb):
    """F_r(t,b) = sum_{k=0}^r [r!/(r-k)!] * t^k / prod_{i=1}^{k+1}(r+b+i)   (sec 2.3 Theorem)"""
    total = sp.Integer(0)
    for kk in range(0, r + 1):
        num = sp.factorial(r) / sp.factorial(r - kk)
        denom = sp.prod([(r + bb + i) for i in range(1, kk + 2)])
        total += num * tt**kk / denom
    return sp.nsimplify(sp.together(total))


def G_closed(r, tt, bb):
    """G_r(t,b) = sum_{k=0}^{r-1} C(k+2,2) * r!/(r-k-1)! * t^k / prod_{i=1}^{k+2}(r+b+i)  (sec 3.3 Theorem)"""
    if r == 0:
        return sp.Integer(0)
    total = sp.Integer(0)
    for kk in range(0, r):
        num = sp.binomial(kk + 2, 2) * sp.factorial(r) / sp.factorial(r - kk - 1)
        denom = sp.prod([(r + bb + i) for i in range(1, kk + 3)])
        total += num * tt**kk / denom
    return sp.nsimplify(sp.together(total))


def Hhat_closed(r, ss, bb):
    """Hhat_r(s,b) = (1-s) F_r(1-s, b+1)   (sec 2.2 algebraic Relation)"""
    return sp.together((1 - ss) * F_closed(r, 1 - ss, bb + 1))


def K_closed(r, ss, bb):
    """
    K_r(s,b) relation (sec 3.1):
      K_r(s,b) = 1 + r*Hhat_{r-1}(s,b+1) + (1-s)*G_r(1-s,b+1) - (1+b+r)*F_r(1-s,b+1)
    with base case K_0(s,b) = 1/(b+2) (exact, all s).
    """
    if r == 0:
        return sp.nsimplify(sp.Rational(1, 1) / (bb + 2))
    term1 = sp.Integer(1)
    term2 = r * Hhat_closed(r - 1, ss, bb + 1)
    term3 = (1 - ss) * G_closed(r, 1 - ss, bb + 1)
    term4 = (1 + bb + r) * F_closed(r, 1 - ss, bb + 1)
    return sp.together(term1 + term2 + term3 - term4)


if __name__ == "__main__":
    # smoke test: F_r(1,0) should match phi_r = 4^r(r!)^2/(2r+1)!
    for r in range(0, 7):
        val = F_closed(r, 1, 0)
        phi_r = sp.Rational(4**r * sp.factorial(r)**2, sp.factorial(2 * r + 1))
        print(r, val, phi_r, sp.simplify(val - phi_r) == 0)
