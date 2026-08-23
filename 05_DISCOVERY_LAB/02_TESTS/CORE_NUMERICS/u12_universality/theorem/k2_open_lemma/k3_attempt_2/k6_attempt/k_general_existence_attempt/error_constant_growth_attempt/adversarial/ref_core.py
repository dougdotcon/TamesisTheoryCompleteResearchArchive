"""
ref_core.py -- HOSTILE REFEREE, wave-11 adversarial pass on
`error_constant_growth_attempt/ATTEMPT.md`.

WRITTEN FROM SCRATCH.  Nothing here is imported, copied or transcribed from the
target directory's own scripts (core.py etc.), which were NOT read before this
file was written and run.  The only things taken from prose (and only from the
*predecessor* documents, whose results are already PROVED and are explicitly
declared reusable by the task) are:

  (RE-1) the exact discrete transition rules of `k3_attempt_2/ATTEMPT.md` §2:
             g(a,b,r) = 1/m + (r/m) h(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r),  m=n-a
             h(a,b,r) = 1/n + (r/n) h(a,b+1,r-1) + ((n-1-a-b-r)/n) g(a,b+1,r)
         re-expressed in the (m,b) coordinates used downstream as
             g_r(m,b) = 1/m + (r/m) h_{r-1}(n-m+1,b) + ((m-1-r-b)/m) g_r(m-1,b)
             h_r(a,b) = 1/n + (r/n) h_{r-1}(a,b+1) + ((n-1-a-b-r)/n) g_r(n-a,b+1)

  (RE-2) the exact base facts g_0(m,b)=1/(b+1), h_0(a,b)=(n-a+1)/(n(b+2))
         (PROVED, k3_attempt_2 §3).  Used only as a cross-check: the simulator
         below re-derives them from (RE-1).

  (RE-3) the already-PROVED closed forms
             c_k^{(r)}(b) = r!/(r-k)! / prod_{i=1}^{k+1}(r+b+i)
             d_k^{(r)}(b) = C(k+2,2) r!/(r-k-1)! / prod_{i=1}^{k+2}(r+b+i)
         used ONLY as targets to reproduce.  The ladder built here does NOT use
         them: F_r and G_r are obtained by solving my own ODEs, derived by hand
         in REFEREE_REPORT.md Part 1, and are then *compared* to (RE-3).

Everything else -- the eps^2 matching, the H_r ODE, the L_r relation, the ODE
solver, the residuals, the constants -- is re-derived here independently.

Exact arithmetic only (fractions.Fraction).
"""

from fractions import Fraction as Fr

# ---------------------------------------------------------------------------
# 1.  Dense univariate polynomials over Q.  Coefficient list, index = degree.
# ---------------------------------------------------------------------------


def ptrim(p):
    while len(p) > 1 and p[-1] == 0:
        p = p[:-1]
    return p


def pzero():
    return [Fr(0)]


def pconst(c):
    return [Fr(c)]


def padd(p, q):
    n = max(len(p), len(q))
    return ptrim([(p[i] if i < len(p) else Fr(0)) + (q[i] if i < len(q) else Fr(0))
                  for i in range(n)])


def psub(p, q):
    n = max(len(p), len(q))
    return ptrim([(p[i] if i < len(p) else Fr(0)) - (q[i] if i < len(q) else Fr(0))
                  for i in range(n)])


def pscale(p, c):
    c = Fr(c)
    return ptrim([c * x for x in p])


def pmul(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j, b in enumerate(q):
            if b == 0:
                continue
            out[i + j] += a * b
    return ptrim(out)


def pdiff(p):
    if len(p) <= 1:
        return pzero()
    return ptrim([p[k] * k for k in range(1, len(p))])


def pdiffn(p, n):
    for _ in range(n):
        p = pdiff(p)
    return p


def peval(p, x):
    x = Fr(x)
    acc = Fr(0)
    for c in reversed(p):
        acc = acc * x + c
    return acc


def preflect(p):
    """P(x) -> P(1-x)."""
    # Horner in (1-x)
    one_minus = [Fr(1), Fr(-1)]
    acc = pzero()
    for c in reversed(p):
        acc = padd(pmul(acc, one_minus), pconst(c))
    return acc


def pnorm1(p):
    """coefficient-sum norm  ||p|| = sum |a_k|  (the norm used by the lineage)."""
    return sum(abs(c) for c in p)


def pxmul(p):
    """multiply by x."""
    return ptrim([Fr(0)] + list(p))


# ---------------------------------------------------------------------------
# 2.  The ODE solver for   t X'(t) + (1+r+b) X(t) = RHS(t).
#     Coefficient of t^k on the left is (k+1+r+b) x_k, never 0 for r,b>=0,k>=0.
# ---------------------------------------------------------------------------


def solve_ode(rhs, r, b):
    return ptrim([rhs[k] / Fr(k + 1 + r + b) for k in range(len(rhs))])


# ---------------------------------------------------------------------------
# 3.  The ladder, built from MY OWN eps^0 / eps^1 / eps^2 matching.
#
#     eps^0 :  t F' + (1+r+b) F   = 1 + r*Hhat_{r-1}(1-t,b)
#     eps^1 :  t G' + (1+r+b) G   = r*Hhat'_{r-1}(1-t,b) + r*K_{r-1}(1-t,b)
#                                   + (t/2) F'' + (1+r+b) F'
#     eps^2 :  t H' + (1+r+b) H   = r*[ (1/2) Hhat''_{r-1}(1-t,b)
#                                       + K'_{r-1}(1-t,b) + L_{r-1}(1-t,b) ]
#                                   + (t/2) G'' - (t/6) F'''
#                                   + (1+r+b) [ G' - (1/2) F'' ]
#
#     h-side (pure algebra, a = n s exactly, no shift):
#       Hhat_r(s,b) = (1-s) F_r(1-s,b+1)
#       K_r(s,b)    = 1 + r Hhat_{r-1}(s,b+1) + (1-s) G_r(1-s,b+1)
#                       - (1+b+r) F_r(1-s,b+1)
#       L_r(s,b)    = r K_{r-1}(s,b+1) + (1-s) H_r(1-s,b+1)
#                       - (1+b+r) G_r(1-s,b+1)
#
#     (' = d/ds on the hatted objects, evaluated at s = 1-t.)
# ---------------------------------------------------------------------------


class Ladder:
    """F,G,H in t;  Hhat,K,L in s.  Keys (r,b)."""

    def __init__(self, R, B):
        self.R = R
        self.B = B
        self.BMAX = B + R + 2
        self.F, self.G, self.H = {}, {}, {}
        self.Hh, self.K, self.L = {}, {}, {}
        self._build()

    def _sub1m(self, p):
        """polynomial in s -> same polynomial evaluated at s = 1-t (poly in t)."""
        return preflect(p)

    def _build(self):
        # ---- r = 0 -------------------------------------------------------
        r = 0
        for b in range(0, self.BMAX + 1):
            self.F[(r, b)] = pconst(Fr(1, b + 1))     # exact: g_0 = 1/(b+1)
            self.G[(r, b)] = pzero()                  # exact: no 1/n term
            self.H[(r, b)] = pzero()                  # exact: no 1/n^2 term
        for b in range(0, self.BMAX):
            self._hside(r, b)

        # ---- r >= 1 ------------------------------------------------------
        for r in range(1, self.R + 1):
            bhi = self.BMAX - r
            for b in range(0, bhi + 1):
                Hh1 = self.Hh[(r - 1, b)]
                K1 = self.K[(r - 1, b)]
                L1 = self.L[(r - 1, b)]

                # eps^0
                rhs = padd(pconst(1), pscale(self._sub1m(Hh1), r))
                F = solve_ode(rhs, r, b)
                self.F[(r, b)] = F

                # eps^1
                Fp, Fpp, Fppp = pdiff(F), pdiffn(F, 2), pdiffn(F, 3)
                rhs = pscale(self._sub1m(pdiff(Hh1)), r)
                rhs = padd(rhs, pscale(self._sub1m(K1), r))
                rhs = padd(rhs, pscale(pxmul(Fpp), Fr(1, 2)))
                rhs = padd(rhs, pscale(Fp, 1 + r + b))
                G = solve_ode(rhs, r, b)
                self.G[(r, b)] = G

                # eps^2
                Gp, Gpp = pdiff(G), pdiffn(G, 2)
                rhs = pscale(self._sub1m(pdiffn(Hh1, 2)), Fr(r, 2))
                rhs = padd(rhs, pscale(self._sub1m(pdiff(K1)), r))
                rhs = padd(rhs, pscale(self._sub1m(L1), r))
                rhs = padd(rhs, pscale(pxmul(Gpp), Fr(1, 2)))
                rhs = psub(rhs, pscale(pxmul(Fppp), Fr(1, 6)))
                rhs = padd(rhs, pscale(Gp, 1 + r + b))
                rhs = psub(rhs, pscale(Fpp, Fr(1 + r + b, 2)))
                H = solve_ode(rhs, r, b)
                self.H[(r, b)] = H

            for b in range(0, bhi):
                self._hside(r, b)

    def _hside(self, r, b):
        F1 = self.F[(r, b + 1)]
        G1 = self.G[(r, b + 1)]
        H1 = self.H[(r, b + 1)]
        # Hhat_r(s,b) = (1-s) F_r(1-s,b+1)
        oneminus = [Fr(1), Fr(-1)]
        self.Hh[(r, b)] = pmul(oneminus, preflect(F1))
        # K_r(s,b)
        K = pconst(1)
        if r >= 1:
            K = padd(K, pscale(self.Hh[(r - 1, b + 1)], r))
        K = padd(K, pmul(oneminus, preflect(G1)))
        K = psub(K, pscale(preflect(F1), 1 + b + r))
        self.K[(r, b)] = K
        # L_r(s,b)
        L = pzero()
        if r >= 1:
            L = padd(L, pscale(self.K[(r - 1, b + 1)], r))
        L = padd(L, pmul(oneminus, preflect(H1)))
        L = psub(L, pscale(preflect(G1), 1 + b + r))
        self.L[(r, b)] = L


# ---------------------------------------------------------------------------
# 4.  Already-PROVED closed forms, transcribed ONLY as comparison targets.
# ---------------------------------------------------------------------------


def falling(r, k):
    """r!/(r-k)!  ; 0 if k>r ; 1 if k=0."""
    if k < 0:
        return 0
    if k > r:
        return 0
    v = 1
    for i in range(k):
        v *= (r - i)
    return v


def denom(r, b, upto):
    v = 1
    for i in range(1, upto + 1):
        v *= (r + b + i)
    return v


def c_closed(r, k, b):
    if k < 0 or k > r:
        return Fr(0)
    return Fr(falling(r, k), denom(r, b, k + 1))


def d_closed(r, k, b):
    if k < 0 or k > r - 1:
        return Fr(0)
    return Fr((k + 1) * (k + 2) // 2 * falling(r, k + 1), denom(r, b, k + 2))


def e_closed(r, k, b):
    """TARGET DOCUMENT's Theorem 1 -- the object under test."""
    if k < 0 or k > r - 2:
        return Fr(0)
    num = (3 * k + 8) * (k + 1) * (k + 2) * (k + 3) * falling(r, k + 2)
    return Fr(num, 24 * denom(r, b, k + 3))


def phi(r):
    """Wallis mean phi_r = 4^r (r!)^2/(2r+1)!  (exact rational)."""
    import math
    return Fr(4 ** r * math.factorial(r) ** 2, math.factorial(2 * r + 1))


# ---------------------------------------------------------------------------
# 5.  My own exact simulator of the discrete recursion (RE-1), for a given n.
# ---------------------------------------------------------------------------


class Chain:
    """Exact g_r(m,b), h_r(a,b) for one fixed n, r=0..R, b=0..B."""

    def __init__(self, n, R, B):
        self.n = n
        self.R = R
        self.B = B
        self.g = {}
        self.h = {}
        self._build()

    def _build(self):
        n = self.n
        BMAX = self.B + self.R + 2
        for r in range(0, self.R + 1):
            # ---- g_r(m,b) for m = b+r+1 .. n
            for b in range(0, BMAX - r + 1):
                lo = b + r + 1
                if lo > n:
                    continue
                prev = Fr(0)          # g_r(b+r, b): coefficient below is 0
                for m in range(lo, n + 1):
                    val = Fr(1, m)
                    if r >= 1:
                        a = n - m + 1
                        val += Fr(r, m) * self.h[(r - 1, a, b)]
                    coef = m - 1 - r - b
                    if coef != 0:
                        val += Fr(coef, m) * prev
                    self.g[(r, m, b)] = val
                    prev = val
            # ---- h_r(a,b) for a = 0 .. n-b-r-1
            for b in range(0, BMAX - r):
                hi = n - b - r - 1
                for a in range(0, hi + 1):
                    val = Fr(1, n)
                    if r >= 1:
                        val += Fr(r, n) * self.h[(r - 1, a, b + 1)]
                    coef = n - 1 - a - b - r
                    if coef != 0:
                        val += Fr(coef, n) * self.g[(r, n - a, b + 1)]
                    self.h[(r, a, b)] = val
