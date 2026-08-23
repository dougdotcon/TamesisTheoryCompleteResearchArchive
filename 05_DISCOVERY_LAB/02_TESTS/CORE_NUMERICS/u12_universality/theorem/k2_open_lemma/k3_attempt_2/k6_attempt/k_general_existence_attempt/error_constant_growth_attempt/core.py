"""
core.py -- error_constant_growth_attempt (wave 10, front (b), DISC-DEC-045)

Written from scratch for this attempt.  NOTHING is imported or copied from any
sibling/predecessor directory.  The already-PROVED closed forms of F_r and G_r
and the already-PROVED exact (a,b,r) transition rules are RE-TRANSCRIBED here
from their stated formulas (labeled REUSE below), which is the convention every
predecessor document in this lineage uses.

Everything is exact: fractions.Fraction throughout.  No floating point enters
any object defined here.

--------------------------------------------------------------------------
REUSE 1 -- the exact discrete transition rules
  (k3_attempt_2/ATTEMPT.md SS2, Proposition, PROVED; restated in
   k6_attempt/ATTEMPT.md SS2.2 and k_general_existence_attempt/ATTEMPT.md SS3/SS6)

  With m := n - a (size of the still-unassigned pi-target pool),
  and writing g_r(m,b) := g(n-m, b, r),  h_r(a,b) := h(a,b,r):

    g_r(m,b) = 1/m + (r/m) h_{r-1}(n-m+1, b) + ((m-1-r-b)/m) g_r(m-1, b)
    h_r(a,b) = 1/n + (r/n) h_{r-1}(a, b+1) + ((n-1-a-b-r)/n) g_r(n-a, b+1)

  valid on the domain a+b+r < n, i.e. m >= b+r+1 for g_r and a <= n-b-r-1 for h_r.
  At m = b+r+1 the coefficient (m-1-r-b)/m is exactly 0, so the g_r recursion is
  self-starting there.

REUSE 2 -- the leading-order closed form
  (k6_attempt/ATTEMPT.md SS2.3, Theorem, PROVED, general r)

    F_r(t,b) = sum_{k=0}^{r}  [ r!/(r-k)! ] * t^k / prod_{i=1}^{k+1} (r+b+i)

REUSE 3 -- the O(1/n) closed form
  (k6_attempt/ATTEMPT.md SS3.3, Theorem, PROVED, general r)

    G_r(t,b) = sum_{k=0}^{r-1} C(k+2,2) * [ r!/(r-k-1)! ] * t^k
                                 / prod_{i=1}^{k+2} (r+b+i)

REUSE 4 -- the definitions of Hhat_r and K_r
  (k6_attempt/ATTEMPT.md SS2.2 and SS3.1; these are DEFINITIONS, not claims)

    Hhat_r(s,b) = (1-s) F_r(1-s, b+1)
    K_r(s,b)    = 1 + r Hhat_{r-1}(s,b+1) + (1-s) G_r(1-s,b+1)
                    - (1+b+r) F_r(1-s, b+1)

NEW IN THIS DOCUMENT -- the third-order (eps^2) pair (H_r, L_r).
  Derived in ATTEMPT.md SS3 of this directory by pushing the SAME eps-matching
  one order further.  Definitions used here:

    t H_r'(t,b) + (1+r+b) H_r(t,b)
       = r[ (1/2) Hhat''_{r-1}(1-t,b) + K'_{r-1}(1-t,b) + L_{r-1}(1-t,b) ]
         + (t/2) G_r''(t,b) - (t/6) F_r'''(t,b)
         + (1+r+b)[ G_r'(t,b) - (1/2) F_r''(t,b) ]

    L_r(s,b) = r K_{r-1}(s,b+1) + (1-s) H_r(1-s,b+1) - (1+b+r) G_r(1-s,b+1)

  base cases H_0 == 0, L_0 == 0 (exact).  Primes on Hhat_{r-1}, K_{r-1} are d/ds,
  evaluated at s = 1-t.  The ODE has a unique polynomial solution because the
  coefficient (k+1+r+b) of t^k on the left is never 0 for r,b >= 0, k >= 0.
"""

from fractions import Fraction as Fr
from functools import lru_cache

# ---------------------------------------------------------------------------
# A minimal exact polynomial type: coefficient tuple, index = power.
# All coefficients are fractions.Fraction.  Immutable (tuples) so it is hashable
# and can be memoised.
# ---------------------------------------------------------------------------


def _trim(c):
    i = len(c)
    while i > 0 and c[i - 1] == 0:
        i -= 1
    return tuple(c[:i])


class Poly(object):
    __slots__ = ("c",)

    def __init__(self, coeffs=()):
        self.c = _trim(tuple(Fr(x) for x in coeffs))

    # -- constructors -------------------------------------------------------
    @staticmethod
    def const(v):
        return Poly((Fr(v),))

    @staticmethod
    def x():
        return Poly((Fr(0), Fr(1)))

    # -- basics -------------------------------------------------------------
    def deg(self):
        return len(self.c) - 1  # -1 for the zero polynomial

    def coeff(self, k):
        return self.c[k] if 0 <= k < len(self.c) else Fr(0)

    def is_zero(self):
        return len(self.c) == 0

    def __eq__(self, o):
        return isinstance(o, Poly) and self.c == o.c

    def __hash__(self):
        return hash(self.c)

    def __repr__(self):
        if self.is_zero():
            return "Poly(0)"
        return "Poly(" + " + ".join("%s*x^%d" % (self.c[k], k)
                                    for k in range(len(self.c)) if self.c[k] != 0) + ")"

    # -- ring operations ----------------------------------------------------
    def __add__(self, o):
        if not isinstance(o, Poly):
            o = Poly.const(o)
        n = max(len(self.c), len(o.c))
        return Poly(tuple(self.coeff(k) + o.coeff(k) for k in range(n)))

    __radd__ = __add__

    def __neg__(self):
        return Poly(tuple(-a for a in self.c))

    def __sub__(self, o):
        if not isinstance(o, Poly):
            o = Poly.const(o)
        return self + (-o)

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, Poly):
            f = Fr(o)
            return Poly(tuple(a * f for a in self.c))
        if self.is_zero() or o.is_zero():
            return Poly()
        out = [Fr(0)] * (len(self.c) + len(o.c) - 1)
        for i, a in enumerate(self.c):
            if a == 0:
                continue
            for j, bb in enumerate(o.c):
                if bb != 0:
                    out[i + j] += a * bb
        return Poly(out)

    __rmul__ = __mul__

    # -- calculus / substitution -------------------------------------------
    def deriv(self, times=1):
        p = self
        for _ in range(times):
            if p.deg() < 1:
                p = Poly()
                break
            p = Poly(tuple(p.c[k] * k for k in range(1, len(p.c))))
        return p

    def shift_1_minus_x(self):
        """Return the polynomial q with q(x) = self(1-x)."""
        # Horner in (1-x): build up by repeated multiplication.
        one_minus_x = Poly((Fr(1), Fr(-1)))
        out = Poly()
        for k in range(len(self.c) - 1, -1, -1):
            out = out * one_minus_x + Poly.const(self.c[k])
        return out

    def mul_x(self):
        return Poly((Fr(0),) + self.c) if not self.is_zero() else Poly()

    def eval(self, x):
        acc = Fr(0)
        for k in range(len(self.c) - 1, -1, -1):
            acc = acc * x + self.c[k]
        return acc

    def coeff_sum_norm(self):
        """||p|| := sum_k |a_k|   (the SS4 coefficient-sum norm of the target doc)."""
        return sum((abs(a) for a in self.c), Fr(0))


ZERO = Poly()


# ---------------------------------------------------------------------------
# REUSE 2/3: the already-PROVED closed forms, transcribed from their statements.
# Returned as Poly in the variable t, for concrete integers r >= 0, b >= 0.
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def F(r, b):
    """F_r(t,b) = sum_{k=0}^r [r!/(r-k)!] t^k / prod_{i=1}^{k+1}(r+b+i)."""
    coeffs = []
    fall = Fr(1)          # r!/(r-k)!  (falling factorial), k = 0 -> 1
    den = Fr(r + b + 1)   # prod_{i=1}^{k+1}(r+b+i), k = 0 -> (r+b+1)
    for k in range(r + 1):
        if k > 0:
            fall *= (r - k + 1)
            den *= (r + b + k + 1)
        coeffs.append(fall / den)
    return Poly(coeffs)


@lru_cache(maxsize=None)
def G(r, b):
    """G_r(t,b) = sum_{k=0}^{r-1} C(k+2,2) [r!/(r-k-1)!] t^k / prod_{i=1}^{k+2}(r+b+i)."""
    if r == 0:
        return ZERO
    coeffs = []
    fall = Fr(1)                       # r!/(r-k-1)!, k = 0 -> r
    for i in range(r, r - 1, -1):
        fall *= i
    den = Fr(r + b + 1) * Fr(r + b + 2)  # prod_{i=1}^{k+2}, k=0 -> (r+b+1)(r+b+2)
    for k in range(r):
        if k > 0:
            fall *= (r - k)
            den *= (r + b + k + 2)
        binom = Fr((k + 2) * (k + 1), 2)
        coeffs.append(binom * fall / den)
    return Poly(coeffs)


# ---------------------------------------------------------------------------
# REUSE 4: Hhat_r and K_r -- definitions, as polynomials in s.
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def Hhat(r, b):
    """Hhat_r(s,b) = (1-s) F_r(1-s, b+1), as a polynomial in s."""
    return Poly((Fr(1), Fr(-1))) * F(r, b + 1).shift_1_minus_x()


@lru_cache(maxsize=None)
def Kpol(r, b):
    """K_r(s,b) = 1 + r Hhat_{r-1}(s,b+1) + (1-s)G_r(1-s,b+1) - (1+b+r)F_r(1-s,b+1)."""
    out = Poly.const(1)
    if r >= 1:
        out = out + Hhat(r - 1, b + 1) * r
    out = out + Poly((Fr(1), Fr(-1))) * G(r, b + 1).shift_1_minus_x()
    out = out - F(r, b + 1).shift_1_minus_x() * (1 + b + r)
    return out


# ---------------------------------------------------------------------------
# NEW: the third-order pair (H_r, L_r).
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def H(r, b):
    """H_r(t,b): the eps^2 term of g_r.  Polynomial in t.  H_0 == 0."""
    if r == 0:
        return ZERO
    Fr_ = F(r, b)
    Gr_ = G(r, b)
    # right-hand side of the H_r ODE, as a polynomial in t
    rhs = ZERO
    if r >= 1:
        # r * [ (1/2)Hhat''_{r-1}(1-t,b) + K'_{r-1}(1-t,b) + L_{r-1}(1-t,b) ]
        piece = (Hhat(r - 1, b).deriv(2) * Fr(1, 2)
                 + Kpol(r - 1, b).deriv(1)
                 + L(r - 1, b))
        rhs = rhs + piece.shift_1_minus_x() * r
    # + (t/2) G_r'' - (t/6) F_r''' + (1+r+b)[ G_r' - (1/2) F_r'' ]
    rhs = rhs + (Gr_.deriv(2) * Fr(1, 2)).mul_x()
    rhs = rhs - (Fr_.deriv(3) * Fr(1, 6)).mul_x()
    rhs = rhs + (Gr_.deriv(1) - Fr_.deriv(2) * Fr(1, 2)) * (1 + r + b)
    # solve  t y' + (1+r+b) y = rhs  coefficientwise:  y_k = rhs_k / (k+1+r+b)
    return Poly(tuple(rhs.coeff(k) / Fr(k + 1 + r + b) for k in range(len(rhs.c))))


@lru_cache(maxsize=None)
def L(r, b):
    """L_r(s,b) = r K_{r-1}(s,b+1) + (1-s)H_r(1-s,b+1) - (1+b+r)G_r(1-s,b+1)."""
    if r == 0:
        return ZERO
    out = Kpol(r - 1, b + 1) * r
    out = out + Poly((Fr(1), Fr(-1))) * H(r, b + 1).shift_1_minus_x()
    out = out - G(r, b + 1).shift_1_minus_x() * (1 + b + r)
    return out


# ---------------------------------------------------------------------------
# Independent exact simulator of the discrete chain (REUSE 1), exact Fractions.
# ---------------------------------------------------------------------------

class Chain(object):
    """Exact memoised evaluation of g_r(m,b) and h_r(a,b) for one fixed n."""

    def __init__(self, n):
        self.n = n
        self._g = {}
        self._h = {}

    def g(self, r, m, b):
        n = self.n
        assert r >= 0 and b >= 0
        assert m >= b + r + 1, "g_r(m,b) out of domain: m=%d, b+r+1=%d" % (m, b + r + 1)
        assert m <= n
        key = (r, m, b)
        v = self._g.get(key)
        if v is not None:
            return v
        if r == 0:
            v = Fr(1, b + 1)
        else:
            acc = Fr(1, m) + Fr(r, m) * self.h(r - 1, n - m + 1, b)
            if m - 1 - r - b > 0:
                acc += Fr(m - 1 - r - b, m) * self.g(r, m - 1, b)
            v = acc
        self._g[key] = v
        return v

    def h(self, r, a, b):
        n = self.n
        assert r >= 0 and b >= 0 and a >= 0
        assert a + b + r < n, "h_r(a,b) out of domain: a=%d b=%d r=%d n=%d" % (a, b, r, n)
        key = (r, a, b)
        v = self._h.get(key)
        if v is not None:
            return v
        acc = Fr(1, n)
        if r >= 1:
            acc += Fr(r, n) * self.h(r - 1, a, b + 1)
        c = n - 1 - a - b - r
        if c > 0:
            acc += Fr(c, n) * self.g(r, n - a, b + 1)
        self._h[key] = acc
        return acc


# ---------------------------------------------------------------------------
# Residuals.
# ---------------------------------------------------------------------------

def R_resid(chain, r, m, b):
    """R_r(m,b,n) = g_r(m,b) - F_r(t,b) - (1/n)G_r(t,b),  t = m/n.  Exact."""
    n = chain.n
    t = Fr(m, n)
    return chain.g(r, m, b) - F(r, b).eval(t) - G(r, b).eval(t) / n


def R3_resid(chain, r, m, b):
    """R^{(3)}_r(m,b,n) = R_r(m,b,n) - (1/n^2)H_r(t,b).  Exact."""
    n = chain.n
    t = Fr(m, n)
    return R_resid(chain, r, m, b) - H(r, b).eval(t) / (n * n)


def eps_h_resid(chain, r, a, b):
    """eps^h_r(a,b,n) = h_r(a,b) - Hhat_r(s,b) - (1/n)K_r(s,b),  s = a/n.  Exact."""
    n = chain.n
    s = Fr(a, n)
    return chain.h(r, a, b) - Hhat(r, b).eval(s) - Kpol(r, b).eval(s) / n


def eps_h3_resid(chain, r, a, b):
    n = chain.n
    s = Fr(a, n)
    return eps_h_resid(chain, r, a, b) - L(r, b).eval(s) / (n * n)


# ---------------------------------------------------------------------------
# Wallis value phi_r = 4^r (r!)^2 / (2r+1)!   (THEOREM.md Lemma 2) -- used only
# as an independent cross-check of F_r(1,0).
# ---------------------------------------------------------------------------

def phi(r):
    num = Fr(4) ** r
    fa = Fr(1)
    for i in range(1, r + 1):
        fa *= i
    den = Fr(1)
    for i in range(1, 2 * r + 2):
        den *= i
    return num * fa * fa / den


if __name__ == "__main__":
    print("=== core.py smoke tests (all exact) ===")
    ok = True

    # (1) F_r(1,0) == phi_r
    for r in range(0, 13):
        a, bb = F(r, 0).eval(Fr(1)), phi(r)
        m = (a == bb)
        ok &= m
        if r <= 8:
            print("  F_%d(1,0) = %-16s phi_%d = %-16s match=%s" % (r, a, r, bb, m))
    print("  F_r(1,0)==phi_r for r=0..12 :", ok)

    # (2) G_r(1,0) == r phi_r / 4
    ok2 = True
    for r in range(0, 13):
        a, bb = G(r, 0).eval(Fr(1)), Fr(r) * phi(r) / 4
        ok2 &= (a == bb)
    print("  G_r(1,0)==r*phi_r/4 for r=0..12 :", ok2)

    # (3) degrees
    print("  degrees: r, deg F, deg G, deg H, deg Hhat, deg K, deg L")
    for r in range(0, 7):
        print("    r=%d  %2d %2d %2d %2d %2d %2d" % (
            r, F(r, 0).deg(), G(r, 0).deg(), H(r, 0).deg(),
            Hhat(r, 0).deg(), Kpol(r, 0).deg(), L(r, 0).deg()))

    # (4) H_r(1,0) for small r, against known exact psi_n^{(K)} 1/n^2 coefficients
    print("  H_1(1,0) =", H(1, 0).eval(Fr(1)), "(known: 0, since psi_n^(1)=(4n+1)/(6n))")
    print("  H_2(1,0) =", H(2, 0).eval(Fr(1)), "(known: 1/15, since psi_n^(2)=(8n^2+4n+1)/(15n^2))")
    print("  H_2(t,0) =", H(2, 0), "(target doc SS7: R_2(m,0,n)=1/(15n^2) for ALL m)")
    print("  H_1(t,0) =", H(1, 0), "(target doc SS7: R_1==0 identically)")
