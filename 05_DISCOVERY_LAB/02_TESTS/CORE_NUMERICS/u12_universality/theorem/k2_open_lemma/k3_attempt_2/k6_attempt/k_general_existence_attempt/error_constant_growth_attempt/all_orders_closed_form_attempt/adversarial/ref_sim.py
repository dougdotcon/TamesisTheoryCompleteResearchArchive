"""
ADVERSARIAL REFEREE, item 1: from-scratch exact simulator of the RAW recursion,
and from-scratch evaluation of the Theorem A / Theorem B closed forms.

Written without reading any .py file in the parent directory.

Ground-truth transition rules re-transcribed from k3_attempt_2/ATTEMPT.md Sec.2
(PROVED there, taken as input, in their ORIGINAL (a,b,r) form -- NOT from the
target document's rewritten (*)/(**) form, so that the target's own
transcription is independently exercised):

    NON-SOURCE (m := n-a):
      g(a,b,r) = 1/m + (r/m) h(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r)
    SOURCE:
      h(a,b,r) = 1/n + (r/n) h(a,b+1,r-1) + ((n-1-a-b-r)/n) g(a,b+1,r)

    valid for every reachable state with a+b+r < n.

Target's rewrite (to be CHECKED, not assumed):
    g_r(m,b) := g(n-m, b, r),  h_r(a,b) := h(a,b,r)
    (*)  m[g_r(m,b)-g_r(m-1,b)] + (1+r+b) g_r(m-1,b) = 1 + r h_{r-1}(n-m+1,b)
    (**) h_r(a,b) = 1/n + (r/n) h_{r-1}(a,b+1) + [(1-a/n)-(1+b+r)/n] g_r(n-a,b+1)
"""
from fractions import Fraction as F
import sys
sys.setrecursionlimit(100000)


# ---------------------------------------------------------------- raw solver
class Raw:
    """Exact solver for the RAW (a,b,r) recursion, iterative (no recursion depth
    issues), filling states in increasing order of a+b so every dependency is
    already present.  No out-of-domain state is ever created."""

    def __init__(self, n):
        self.n = n
        self.g = {}
        self.h = {}
        self._solve()

    def _solve(self):
        n = self.n
        g, h = self.g, self.h
        # valid states: a,b,r >= 0 and a+b+r < n.  Every call increases a+b by 1
        # and never increases r, so fill by decreasing... actually fill by
        # DEcreasing (a+b) for fixed r, and increasing r.
        for r in range(0, n):
            for sab in range(n - 1 - r, -1, -1):          # s = a+b, downward
                for a in range(0, sab + 1):
                    b = sab - a
                    m = n - a
                    # ---- g(a,b,r)
                    val = F(1, m)
                    if r > 0:
                        val += F(r, m) * h[(a + 1, b, r - 1)]
                    coef = F(m - 1 - r - b, m)
                    if coef != 0:
                        val += coef * g[(a + 1, b, r)]
                    else:
                        # coef == 0 exactly <=> m-1-r-b == 0 <=> a+b+r == n-1,
                        # the top of the ladder: the referenced state
                        # (a+1,b,r) has a+1+b+r == n, OUT OF DOMAIN.
                        assert a + b + r == n - 1, (a, b, r, n)
                        assert (a + 1, b, r) not in g
                    g[(a, b, r)] = val
                    # ---- h(a,b,r)
                    val = F(1, n)
                    if r > 0:
                        val += F(r, n) * h[(a, b + 1, r - 1)]
                    coef = F(n - 1 - a - b - r, n)
                    if coef != 0:
                        val += coef * g[(a, b + 1, r)]
                    else:
                        assert a + b + r == n - 1, (a, b, r, n)
                        assert (a, b + 1, r) not in g
                    h[(a, b, r)] = val

    # -- accessors in the target document's (m,b) / (a,b) coordinates
    def gr(self, r, m, b):
        assert b + r + 1 <= m <= self.n, ("g out of domain", r, m, b, self.n)
        return self.g[(self.n - m, b, r)]

    def hr(self, r, a, b):
        assert 0 <= a <= self.n - b - r - 1, ("h out of domain", r, a, b, self.n)
        return self.h[(a, b, r)]


# ------------------------------------------------- Theorem A / B closed forms
def A(r, j, b):
    """A_j^{(r)}(b) = r!/(r-j)! / prod_{i=1}^{j+1} (r+b+i).  Zero for j>r."""
    if j > r or j < 0:
        return F(0)
    num = 1
    for i in range(r - j + 1, r + 1):
        num *= i                                  # r!/(r-j)!
    den = 1
    for i in range(1, j + 2):
        den *= (r + b + i)
    return F(num, den)


def P(j, m):
    """P_j(m) = (m+j)!/m! = prod_{i=1}^{j}(m+i)."""
    v = 1
    for i in range(1, j + 1):
        v *= (m + i)
    return v


def g_hat(r, m, b, n):
    """Theorem A closed form (a pure expression; no domain restriction)."""
    return sum(A(r, j, b) * F(P(j, m), n ** j) for j in range(0, r + 1))


def h_hat(r, a, b, n):
    """Theorem B: h_r(a,b) = (n-a+1)/n * g_hat_r(n-a+1, b+1)."""
    return F(n - a + 1, n) * g_hat(r, n - a + 1, b + 1, n)


def g_hat_binom(r, m, b, n):
    """Binomial form claimed in Sec.4 of the target."""
    from math import comb, factorial
    N = 2 * r + b + 1
    pref = F(factorial(r) * factorial(r + b), factorial(N))
    return pref * sum(F(comb(N, r - j) * P(j, m), n ** j) for j in range(0, r + 1))


def h_hat_binom(r, a, b, n):
    from math import comb, factorial
    N = 2 * r + b + 2
    pref = F(factorial(r) * factorial(r + b + 1), factorial(N))
    return pref * sum(F(comb(N, r - j) * P(j + 1, n - a), n ** (j + 1))
                      for j in range(0, r + 1))


# ------------------------------------------------------------------ the sweep
def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 26
    rmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    bmax = int(sys.argv[3]) if len(sys.argv) > 3 else 6

    print("=" * 74)
    print("REFEREE CHECK 1: raw recursion  vs  Theorem A / Theorem B closed form")
    print("=" * 74)

    ng = nh = nstar = nstarstar = nbg = nbh = 0
    bad = []
    for n in range(2, nmax + 1):
        R = Raw(n)
        for r in range(0, min(rmax, n - 1) + 1):
            for b in range(0, min(bmax, n - 1 - r) + 1):
                # ---- Theorem A
                for m in range(b + r + 1, n + 1):
                    lhs = R.gr(r, m, b)
                    rhs = g_hat(r, m, b, n)
                    ng += 1
                    if lhs != rhs:
                        bad.append(("A", n, r, b, m, lhs, rhs))
                    if g_hat_binom(r, m, b, n) != lhs:
                        bad.append(("Abin", n, r, b, m))
                    nbg += 1
                # ---- Theorem B
                for a in range(0, n - b - r):
                    lhs = R.hr(r, a, b)
                    rhs = h_hat(r, a, b, n)
                    nh += 1
                    if lhs != rhs:
                        bad.append(("B", n, r, b, a, lhs, rhs))
                    if h_hat_binom(r, a, b, n) != lhs:
                        bad.append(("Bbin", n, r, b, a))
                    nbh += 1
                # ---- the target's REWRITTEN rules (*) and (**), against RAW
                for m in range(b + r + 1, n + 1):
                    L = m * (R.gr(r, m, b) - (R.gr(r, m - 1, b) if m - 1 >= b + r + 1
                                              else F(0)))
                    L += (1 + r + b) * ((R.gr(r, m - 1, b) if m - 1 >= b + r + 1
                                        else F(0)))
                    Rt = F(1)
                    if r > 0:
                        Rt += r * R.hr(r - 1, n - m + 1, b)
                    nstar += 1
                    if L != Rt:
                        bad.append(("(*)", n, r, b, m, L, Rt))
                for a in range(0, n - b - r):
                    L = R.hr(r, a, b)
                    Rt = F(1, n)
                    if r > 0:
                        Rt += F(r, n) * R.hr(r - 1, a, b + 1)
                    coef = F(n - a, n) - F(1 + b + r, n)
                    if coef != 0:
                        Rt += coef * R.gr(r, n - a, b + 1)
                    nstarstar += 1
                    if L != Rt:
                        bad.append(("(**)", n, r, b, a, L, Rt))

    print(f"  n<= {nmax}, r<= {rmax}, b<= {bmax}")
    print(f"  Theorem A   : {ng:7d} exact checks")
    print(f"  Theorem B   : {nh:7d} exact checks")
    print(f"  A binomial  : {nbg:7d} exact checks")
    print(f"  B binomial  : {nbh:7d} exact checks")
    print(f"  rule (*)  raw-vs-rewritten : {nstar:7d}")
    print(f"  rule (**) raw-vs-rewritten : {nstarstar:7d}")
    print(f"  TOTAL       : {ng+nh+nbg+nbh+nstar+nstarstar:7d}")
    print(f"  MISMATCHES  : {len(bad)}")
    for x in bad[:10]:
        print("   ", x)
    return len(bad)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
