"""
core.py -- from-scratch machinery for the all-orders epsilon-ladder.

WRITTEN FROM SCRATCH for wave 11 front (b) (DISC-DEC-047).  Nothing is imported
or copied from any sibling / predecessor directory.  The only things taken from
predecessor documents are *mathematical statements* (re-transcribed here from
their prose, then re-verified against my own independent objects):

  (RE-TRANSCRIBED STATEMENT 1) the exact (a,b,r) transition rules, from
      k3_attempt_2/ATTEMPT.md Sec.2 (PROVED there):
        g(a,b,r) = 1/m + (r/m) h(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r),  m=n-a
        h(a,b,r) = 1/n + (r/n) h(a,b+1,r-1) + ((n-1-a-b-r)/n) g(a,b+1,r)
  (RE-TRANSCRIBED STATEMENT 2) the PROVED closed forms used only as GROUND TRUTH
      to check my ladder against (never used to build it):
        c_k^(r)(b) = r!/(r-k)!   / prod_{i=1..k+1}(r+b+i)              [k6 Sec.2.3]
        d_k^(r)(b) = C(k+2,2) r!/(r-k-1)! / prod_{i=1..k+2}(r+b+i)     [k6 Sec.3.3]
        e_k^(r)(b) = (3k+8)(k+1)(k+2)(k+3)/24 * r!/(r-k-2)!
                                        / prod_{i=1..k+3}(r+b+i)      [Estagio 8 Thm 1]

Everything else -- the general-order epsilon matching, the ODE ladder, the
polynomial arithmetic, the exact discrete simulator -- is built here.

Exact arithmetic only: fractions.Fraction for numeric b, sympy for symbolic b.
"""

from fractions import Fraction
from functools import lru_cache
import math

# ---------------------------------------------------------------------------
# 1.  Dense univariate polynomial in t over an arbitrary exact coefficient ring
# ---------------------------------------------------------------------------


class Poly:
    """Dense polynomial in t.  c[k] is the coefficient of t^k."""

    __slots__ = ("c",)

    def __init__(self, c=None):
        self.c = list(c) if c else []

    @staticmethod
    def const(a):
        return Poly([a]) if a != 0 else Poly()

    @staticmethod
    def zero():
        return Poly()

    def coeff(self, k):
        if 0 <= k < len(self.c):
            return self.c[k]
        return 0

    def deg(self):
        d = len(self.c) - 1
        while d >= 0 and self.c[d] == 0:
            d -= 1
        return d

    def __add__(self, o):
        n = max(len(self.c), len(o.c))
        return Poly([self.coeff(k) + o.coeff(k) for k in range(n)])

    def __sub__(self, o):
        n = max(len(self.c), len(o.c))
        return Poly([self.coeff(k) - o.coeff(k) for k in range(n)])

    def scal(self, a):
        return Poly([a * x for x in self.c])

    def shift(self, j=1):
        """multiply by t^j"""
        if not self.c:
            return Poly()
        return Poly([0] * j + list(self.c))

    def deriv(self, i=1):
        c = list(self.c)
        for _ in range(i):
            c = [k * c[k] for k in range(1, len(c))]
        return Poly(c)

    def ev(self, t):
        acc = 0
        for a in reversed(self.c):
            acc = acc * t + a
        return acc

    def __repr__(self):
        return "Poly(%r)" % (self.c,)


# ---------------------------------------------------------------------------
# 2.  The general-order epsilon ladder  (THE NEW OBJECT OF THIS DOCUMENT)
# ---------------------------------------------------------------------------
#
# Notation.  eps := 1/n, t := m/n, s := a/n.
#
#   g_r(m,b) = sum_{p>=0} eps^p * Phi[p]_r(t,b)      "receiver" side
#   h_r(a,b) = sum_{p>=0} eps^p * Psi[p]_r(s,b)      "source"  side
#
# with  Phi[0]=F_r, Phi[1]=G_r, Phi[2]=H_r, Phi[3]=I_r (new here), ...
#       Psi[0]=Hhat_r, Psi[1]=K_r, Psi[2]=L_r, Psi[3]=M_r (new here), ...
#
# We always work with the h-side in the REFLECTED variable
#       eta[p]_r(t,b) := Psi[p]_r(1-t, b).
#
# Derived here (Sec.2 of ATTEMPT.md) from the exact recursion:
#
#   (SOURCE RELATION, all p >= 0, exact, no Taylor needed)
#      eta[p]_r(t,b) = [p==1] + r*eta[p-1]_{r-1}(t,b+1)
#                      + t*Phi[p]_r(t,b+1) - (1+b+r)*Phi[p-1]_r(t,b+1)
#
#   (RECEIVER ODE, all p >= 0)
#      t*(Phi[p]_r)'(t,b) + (1+r+b)*Phi[p]_r(t,b) = RHS_p(t,b),
#      RHS_p = [p==0]
#            + r * sum_{i=0..p}   (-1)^i / i!    * (eta[p-i]_{r-1})^(i)(t,b)
#            + t * sum_{i=2..p+1} (-1)^i / i!    * (Phi[p+1-i]_r)^(i)(t,b)
#            + (1+r+b) * sum_{i=1..p} (-1)^(i+1) / i! * (Phi[p-i]_r)^(i)(t,b)
#
# The ODE is solved coefficient-by-coefficient: if RHS_p = sum_k rho_k t^k then
#      [t^k] Phi[p]_r = rho_k / (k+1+r+b)   (never a zero divisor for r,b>=0).
#
# Base case:  the r=0 instance of the ODE is self-starting (the eta-sum carries
# the factor r=0), so nothing is hard-coded at all.
# ---------------------------------------------------------------------------


class Ladder:
    """Builds Phi[p]_r(.,b) and eta[p]_r(.,b) for a coefficient ring.

    `b0` is the base value of b (an int/Fraction, or a sympy Symbol).  Levels
    are indexed by (r, d) with the actual b being `b0 + d`; d only ever grows
    as r shrinks, which is exactly how the recursion consumes it.
    """

    def __init__(self, b0, one=Fraction(1), inv=None):
        self.b0 = b0
        self.one = one
        # inv(x) returns 1/x in the ring
        self.inv = inv if inv is not None else (lambda x: self.one / x)
        self._phi = {}
        self._eta = {}
        self._fact = [1]
        for i in range(1, 30):
            self._fact.append(self._fact[-1] * i)

    def bval(self, d):
        return self.b0 + d

    # -- Phi[p]_r at b = b0 + d ---------------------------------------------
    def phi(self, p, r, d=0):
        if p < 0 or r < 0:
            return Poly()
        key = (p, r, d)
        if key in self._phi:
            return self._phi[key]
        b = self.bval(d)
        rhs = Poly()
        if p == 0:
            rhs = rhs + Poly.const(self.one)
        # r * sum_i (-1)^i/i! * (eta[p-i]_{r-1})^(i)
        if r > 0:
            for i in range(0, p + 1):
                e = self.eta(p - i, r - 1, d)
                if e.deg() < 0:
                    continue
                sgn = self.one if i % 2 == 0 else -self.one
                rhs = rhs + e.deriv(i).scal(r * sgn * self.inv(self._fact[i]))
        # t * sum_{i=2..p+1} (-1)^i/i! * (Phi[p+1-i]_r)^(i)
        for i in range(2, p + 2):
            q = self.phi(p + 1 - i, r, d)
            if q.deg() < 0:
                continue
            sgn = self.one if i % 2 == 0 else -self.one
            rhs = rhs + q.deriv(i).scal(sgn * self.inv(self._fact[i])).shift(1)
        # (1+r+b) * sum_{i=1..p} (-1)^(i+1)/i! * (Phi[p-i]_r)^(i)
        for i in range(1, p + 1):
            q = self.phi(p - i, r, d)
            if q.deg() < 0:
                continue
            sgn = -self.one if i % 2 == 0 else self.one
            rhs = rhs + q.deriv(i).scal((1 + r + b) * sgn * self.inv(self._fact[i]))
        out = Poly([rhs.coeff(k) * self.inv(k + 1 + r + b) for k in range(len(rhs.c))])
        self._phi[key] = out
        return out

    # -- eta[p]_r at b = b0 + d ---------------------------------------------
    def eta(self, p, r, d=0):
        if p < 0 or r < 0:
            return Poly()
        key = (p, r, d)
        if key in self._eta:
            return self._eta[key]
        b = self.bval(d)
        out = Poly()
        if p == 1:
            out = out + Poly.const(self.one)
        if r > 0:
            out = out + self.eta(p - 1, r - 1, d + 1).scal(r * self.one)
        out = out + self.phi(p, r, d + 1).shift(1)
        out = out - self.phi(p - 1, r, d + 1).scal((1 + b + r) * self.one)
        self._eta[key] = out
        return out


# ---------------------------------------------------------------------------
# 3.  GROUND TRUTH closed forms (re-transcribed, used only for checking)
# ---------------------------------------------------------------------------


def _denom(k, j, r, b):
    """prod_{i=1}^{k+j+1} (r+b+i)"""
    acc = 1
    for i in range(1, k + j + 2):
        acc *= (r + b + i)
    return acc


def _ff(r, k, j):
    """r!/(r-k-j)!  -- zero when k+j > r"""
    if k + j > r or k < 0:
        return 0
    acc = 1
    for i in range(r - k - j + 1, r + 1):
        acc *= i
    return acc


def c_closed(k, r, b):
    """PROVED (k6 Sec.2.3):  order-1 coefficient."""
    if k < 0 or k > r:
        return Fraction(0)
    return Fraction(_ff(r, k, 0), _denom(k, 0, r, b))


def d_closed(k, r, b):
    """PROVED (k6 Sec.3.3):  order-1/n coefficient, multiplier C(k+2,2)."""
    if k < 0 or k > r - 1:
        return Fraction(0)
    mult = Fraction((k + 1) * (k + 2), 2)
    return mult * Fraction(_ff(r, k, 1), _denom(k, 1, r, b))


def e_closed(k, r, b):
    """PROVED (Estagio 8 Thm 1): order-1/n^2 coefficient,
    multiplier (3k+8)/4 * C(k+3,3)."""
    if k < 0 or k > r - 2:
        return Fraction(0)
    mult = Fraction((3 * k + 8) * (k + 1) * (k + 2) * (k + 3), 24)
    return mult * Fraction(_ff(r, k, 2), _denom(k, 2, r, b))


def phi_wallis(r):
    """varphi_r = 4^r (r!)^2 / (2r+1)!"""
    return Fraction(4 ** r * math.factorial(r) ** 2, math.factorial(2 * r + 1))


# ---------------------------------------------------------------------------
# 4.  From-scratch exact discrete simulator of the true recursion
# ---------------------------------------------------------------------------


class Chain:
    """Exact memoized evaluation of g(a,b,r), h(a,b,r) for a fixed n.

    Implements RE-TRANSCRIBED STATEMENT 1 verbatim, in Fraction arithmetic.
    """

    def __init__(self, n):
        self.n = n
        self._g = {}
        self._h = {}

    def g(self, a, b, r):
        key = (a, b, r)
        v = self._g.get(key)
        if v is not None:
            return v
        n = self.n
        m = n - a
        assert a + b + r < n, (a, b, r, n)
        val = Fraction(1, m)
        if r > 0:
            val += Fraction(r, m) * self.h(a + 1, b, r - 1)
        rest = m - 1 - r - b
        if rest > 0:
            val += Fraction(rest, m) * self.g(a + 1, b, r)
        self._g[key] = val
        return val

    def h(self, a, b, r):
        key = (a, b, r)
        v = self._h.get(key)
        if v is not None:
            return v
        n = self.n
        assert a + b + r < n, (a, b, r, n)
        val = Fraction(1, n)
        if r > 0:
            val += Fraction(r, n) * self.h(a, b + 1, r - 1)
        rest = n - 1 - a - b - r
        if rest > 0:
            val += Fraction(rest, n) * self.g(a, b + 1, r)
        self._h[key] = val
        return val

    # convenience wrappers in the (m,b) coordinates of the documents
    def g_r(self, m, b, r):
        return self.g(self.n - m, b, r)

    def h_r(self, a, b, r):
        return self.h(a, b, r)


# ---------------------------------------------------------------------------
# 5.  Smoke tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("core.py smoke tests")
    print("=" * 70)

    L = Ladder(Fraction(0))

    # (a) order 0 == F_r closed form
    bad = 0
    for r in range(0, 13):
        for d in range(0, 5):
            p0 = L.phi(0, r, d)
            for k in range(0, r + 3):
                if p0.coeff(k) != c_closed(k, r, Fraction(d)):
                    bad += 1
    print("  order-0 vs PROVED c_k^(r)(b):  mismatches =", bad)

    # (b) order 1 == G_r closed form
    bad = 0
    for r in range(0, 13):
        for d in range(0, 5):
            p1 = L.phi(1, r, d)
            for k in range(0, r + 3):
                if p1.coeff(k) != d_closed(k, r, Fraction(d)):
                    bad += 1
    print("  order-1 vs PROVED d_k^(r)(b):  mismatches =", bad)

    # (c) order 2 == H_r closed form
    bad = 0
    for r in range(0, 13):
        for d in range(0, 5):
            p2 = L.phi(2, r, d)
            for k in range(0, r + 3):
                if p2.coeff(k) != e_closed(k, r, Fraction(d)):
                    bad += 1
    print("  order-2 vs PROVED e_k^(r)(b):  mismatches =", bad)

    # (d) F_r(1,0) = varphi_r ; G_r(1,0) = r varphi_r / 4 ;
    #     H_r(1,0) = r(3r+1)/32 varphi_r - r/12
    bad = 0
    for r in range(0, 13):
        if L.phi(0, r, 0).ev(Fraction(1)) != phi_wallis(r):
            bad += 1
        if L.phi(1, r, 0).ev(Fraction(1)) != Fraction(r, 4) * phi_wallis(r):
            bad += 1
        want = Fraction(r * (3 * r + 1), 32) * phi_wallis(r) - Fraction(r, 12)
        if L.phi(2, r, 0).ev(Fraction(1)) != want:
            bad += 1
    print("  F_r(1,0)/G_r(1,0)/H_r(1,0) vs PROVED values: mismatches =", bad)

    # (e) simulator vs PROVED exact psi_n^(1), psi_n^(2)
    bad = 0
    for n in range(2, 10):
        ch = Chain(n)
        if ch.g(0, 0, 1) != Fraction(4 * n + 1, 6 * n):
            bad += 1
    for n in range(3, 10):
        ch = Chain(n)
        if ch.g(0, 0, 2) != Fraction(8 * n * n + 4 * n + 1, 15 * n * n):
            bad += 1
    print("  simulator vs PROVED psi_n^(1), psi_n^(2):  mismatches =", bad)

    # (f) simulator vs the brute-force-confirmed g_6(7,0) = 355081/823543
    ch = Chain(7)
    got = ch.g_r(7, 0, 6)
    print("  g_6(7,0) =", got, " expected 355081/823543 ->",
          got == Fraction(355081, 823543))

    # (g) h-side: psi_n^(3),R = h_2(0,0) = 11/30 + 13/(20n) + 23/(60n^2) + 1/(10n^3)
    e0 = L.eta(0, 2, 0).ev(Fraction(1))   # eta(t=1) = Psi(s=0)
    e1 = L.eta(1, 2, 0).ev(Fraction(1))
    e2 = L.eta(2, 2, 0).ev(Fraction(1))
    e3 = L.eta(3, 2, 0).ev(Fraction(1))
    print("  Hhat_2(0,0)=%s (want 11/30), K_2(0,0)=%s (want 13/20), "
          "L_2(0,0)=%s (want 23/60), M_2(0,0)=%s (want 1/10)"
          % (e0, e1, e2, e3))

    # (h) degrees
    print("  degrees of Phi[p]_8 :", [L.phi(p, 8, 0).deg() for p in range(0, 9)])
