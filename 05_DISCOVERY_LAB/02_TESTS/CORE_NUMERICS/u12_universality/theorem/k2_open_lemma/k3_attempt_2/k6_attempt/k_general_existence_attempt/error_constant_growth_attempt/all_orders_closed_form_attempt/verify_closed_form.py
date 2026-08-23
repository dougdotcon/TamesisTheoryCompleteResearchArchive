"""
verify_closed_form.py -- exhaustive exact verification of

  CONJECTURE M  (multiplier = unsigned Stirling number of the first kind):
      [t^k] Phi[p]_r(t,b)
          = c(k+p+1, k+1) * r!/(r-k-p)! * 1/prod_{i=1}^{k+p+1}(r+b+i)
      where c(n,m) = |s(n,m)| counts permutations of n letters with m cycles.

  CLAIM A  (the resummation -- an EXACT finite closed form for g_r(m,b)):
      g_r(m,b) = sum_{j=0}^{r}  r!/(r-j)!  * 1/prod_{i=1}^{j+1}(r+b+i)
                                * (m+j)!/(m! n^j)

  CLAIM B  (the h-side):
      h_r(a,b) = ((n-a+1)/n) * g_r(n-a+1, b+1)

All arithmetic exact (fractions.Fraction).
"""

import sys
from fractions import Fraction
from core import Ladder, Chain, _ff, _denom, phi_wallis
import math

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
RMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 20
BMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 6

# --- unsigned Stirling numbers of the first kind, own implementation --------
_C = {}


def stirling1u(n, m):
    """|s(n,m)| : permutations of n letters with exactly m cycles."""
    if n < 0 or m < 0:
        return 0
    if n == 0:
        return 1 if m == 0 else 0
    if m == 0:
        return 0
    key = (n, m)
    v = _C.get(key)
    if v is None:
        v = (n - 1) * stirling1u(n - 1, m) + stirling1u(n - 1, m - 1)
        _C[key] = v
    return v


def coeff_closed(k, p, r, b):
    """CONJECTURE M."""
    if k < 0 or k + p > r:
        return Fraction(0)
    return Fraction(stirling1u(k + p + 1, k + 1) * _ff(r, k, p),
                    _denom(k, p, r, b))


def g_closed(m, b, r, n):
    """CLAIM A."""
    tot = Fraction(0)
    P = 1                                # (m+j)!/m!
    for j in range(0, r + 1):
            # A_j = r!/(r-j)! / prod_{i=1}^{j+1}(r+b+i)
        A = Fraction(_ff(r, j, 0), _denom(j, 0, r, b))
        tot += A * Fraction(P, n ** j)
        P *= (m + j + 1)
    return tot


def h_closed(a, b, r, n):
    """CLAIM B."""
    return Fraction(n - a + 1, n) * g_closed(n - a + 1, b + 1, r, n)


# ---------------------------------------------------------------------------
print("=" * 78)
print("SANITY -- stirling1u against its own row-sum identity  sum_m c(n,m)=n!")
print("=" * 78)
bad = 0
for n in range(0, 16):
    if sum(stirling1u(n, m) for m in range(0, n + 1)) != math.factorial(n):
        bad += 1
# and against the generating identity prod_{i=0}^{n-1}(x+i) = sum_m c(n,m)x^m
for n in range(0, 12):
    for x in range(1, 6):
        lhs = 1
        for i in range(0, n):
            lhs *= (x + i)
        rhs = sum(stirling1u(n, m) * x ** m for m in range(0, n + 1))
        if lhs != rhs:
            bad += 1
print("  row sums + rising-factorial generating identity: failures =", bad)

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("V1 -- CONJECTURE M vs the ODE-solved ladder, exhaustive")
print("     p=0..%d, r=0..%d, b=0..%d, every k including out-of-range"
      % (PMAX, RMAX, BMAX))
print("=" * 78)
L = Ladder(Fraction(0))
checks = 0
bad = 0
for p in range(0, PMAX + 1):
    for r in range(0, RMAX + 1):
        for d in range(0, BMAX + 1):
            P = L.phi(p, r, d)
            for k in range(0, r + 4):
                got = P.coeff(k)
                want = coeff_closed(k, p, r, Fraction(d))
                checks += 1
                if got != want:
                    bad += 1
                    if bad < 8:
                        print("   MISMATCH p=%d r=%d b=%d k=%d: got %s want %s"
                              % (p, r, d, k, got, want))
print("  %d exact checks, %d mismatches" % (checks, bad))

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("V1b -- the three ALREADY-PROVED multipliers are the p=0,1,2 slices")
print("=" * 78)
bad = 0
for k in range(0, 25):
    if stirling1u(k + 1, k + 1) != 1:
        bad += 1
    if stirling1u(k + 2, k + 1) != (k + 1) * (k + 2) // 2:
        bad += 1
    num = (3 * k + 8) * (k + 1) * (k + 2) * (k + 3)
    if Fraction(stirling1u(k + 3, k + 1)) != Fraction(num, 24):
        bad += 1
print("  c(k+1,k+1)=1 ; c(k+2,k+1)=C(k+2,2) ; c(k+3,k+1)=(3k+8)(k+1)(k+2)(k+3)/24")
print("  failures over k=0..24 :", bad)

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("V2 -- CLAIM A vs the EXACT DISCRETE SIMULATOR (the real recursion)")
print("     every valid (m,b,r) for every n in range")
print("=" * 78)
NMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 26
checks = 0
bad = 0
worst = None
for n in range(2, NMAX + 1):
    ch = Chain(n)
    for r in range(0, min(n, 9)):
        for b in range(0, min(n - r, 7)):
            for m in range(b + r + 1, n + 1):
                a = n - m
                if a + b + r >= n:
                    continue
                got = ch.g_r(m, b, r)
                want = g_closed(m, b, r, n)
                checks += 1
                if got != want:
                    bad += 1
                    if worst is None:
                        worst = (n, m, b, r, got, want)
print("  %d exact checks against the simulator, %d mismatches" % (checks, bad))
if worst:
    print("  first mismatch:", worst)

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("V3 -- CLAIM B vs the EXACT DISCRETE SIMULATOR")
print("=" * 78)
checks = 0
bad = 0
worst = None
for n in range(2, NMAX + 1):
    ch = Chain(n)
    for r in range(0, min(n, 9)):
        for b in range(0, min(n - r, 7)):
            for a in range(0, n - b - r):
                got = ch.h_r(a, b, r)
                want = h_closed(a, b, r, n)
                checks += 1
                if got != want:
                    bad += 1
                    if worst is None:
                        worst = (n, a, b, r, got, want)
print("  %d exact checks against the simulator, %d mismatches" % (checks, bad))
if worst:
    print("  first mismatch:", worst)

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("V4 -- psi_n^(K) = g_K(n,0) against the PROVED exact formulas of waves 5/6")
print("=" * 78)


def psi_closed(K, n):
    return g_closed(n, 0, K, n)


bad = 0
for n in range(2, 30):
    if psi_closed(1, n) != Fraction(4 * n + 1, 6 * n):
        bad += 1
for n in range(3, 30):
    if psi_closed(2, n) != Fraction(8 * n ** 2 + 4 * n + 1, 15 * n ** 2):
        bad += 1
for n in range(4, 30):
    if psi_closed(3, n) != Fraction(64 * n ** 3 + 48 * n ** 2 + 25 * n + 6,
                                    140 * n ** 3):
        bad += 1
for n in range(5, 30):
    want = Fraction(128 * n ** 4 + 128 * n ** 3 + 103 * n ** 2 + 52 * n + 12,
                    315 * n ** 4)
    if psi_closed(4, n) != want:
        bad += 1
print("  psi_n^(1),(2),(3),(4) vs PROVED closed forms: failures =", bad)

# psi_n^(3),R = h_2(0,0)
bad = 0
for n in range(4, 30):
    want = (Fraction(11, 30) + Fraction(13, 20 * n) + Fraction(23, 60 * n ** 2)
            + Fraction(1, 10 * n ** 3))
    if h_closed(0, 0, 2, n) != want:
        bad += 1
print("  psi_n^(3),R = h_2(0,0) vs PROVED closed form: failures =", bad)

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("V5 -- the n->infinity limit reproduces varphi_K  (Open Lemma value)")
print("=" * 78)
bad = 0
for K in range(0, 15):
    # leading term: j-sum with (m+j)!/(m! n^j) -> 1 at t=1 as n->inf
    lim = sum(Fraction(_ff(K, j, 0), _denom(j, 0, K, 0)) for j in range(0, K + 1))
    if lim != phi_wallis(K):
        bad += 1
print("  sum_{j=0}^{K} K!/(K-j)! / prod_{i=1}^{j+1}(K+i)  ==  varphi_K :",
      "failures =", bad)
