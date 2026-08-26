"""
ground_truth.py -- independent, from-scratch ground-truth implementation of
Corollary A3 (cited, PROVED input, THEOREM.md "Estagio 9" /
all_orders_closed_form_attempt/ATTEMPT.md Sec.4.3):

    D^{*(p)}_r(b) := sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)

    c_j^{(r)}(b) := r! / (r-j)! / prod_{i=1}^{j+1} (r+b+i)

    c(n,k) := unsigned Stirling numbers of the first kind,
              c(n,k) = c(n-1,k-1) + (n-1)*c(n-1,k),  c(0,0)=1.

Written FRESH for this front (GENERAL-P-DSTAR-EXTENSION3-ATTEMPT, wave 19,
front (c), DISC-DEC-083). No predecessor .py file was opened, read, or
imported. Exact fractions.Fraction / int arithmetic throughout, no floats.
"""
from fractions import Fraction
from functools import lru_cache
import math

# ----------------------------------------------------------------------
# Unsigned Stirling numbers of the first kind, via the standard recurrence
# c(n,k) = c(n-1,k-1) + (n-1)*c(n-1,k), c(0,0)=1, c(n,0)=0 for n>=1,
# c(0,k)=0 for k>=1.
# ----------------------------------------------------------------------

_stirling_cache = {(0, 0): 1}


def stirling1_unsigned(n, k):
    """c(n,k), unsigned Stirling number of the first kind. Memoized."""
    if k < 0 or k > n:
        return 0
    if (n, k) in _stirling_cache:
        return _stirling_cache[(n, k)]
    if n == 0:
        val = 1 if k == 0 else 0
    else:
        val = stirling1_unsigned(n - 1, k - 1) + (n - 1) * stirling1_unsigned(n - 1, k)
    _stirling_cache[(n, k)] = val
    return val


def build_stirling_table(n_max):
    """Precompute all c(n,k) for n=0..n_max, k=0..n, bottom-up (avoids deep
    recursion for large n)."""
    table = [[0] * (n_max + 1) for _ in range(n_max + 1)]
    table[0][0] = 1
    for n in range(1, n_max + 1):
        for k in range(0, n + 1):
            a = table[n - 1][k - 1] if k - 1 >= 0 else 0
            b = table[n - 1][k] if k <= n - 1 else 0
            table[n][k] = a + (n - 1) * b
    return table


# ----------------------------------------------------------------------
# Corollary A3, direct sum, exact Fraction arithmetic.
# ----------------------------------------------------------------------

def D_star(p, r, b, stirling_table=None):
    """D^{*(p)}_r(b), Corollary A3, exact Fraction."""
    if r < p:
        return Fraction(0)
    n_max = r + 1
    if stirling_table is not None and len(stirling_table) > n_max:
        c = lambda n, k: stirling_table[n][k] if 0 <= k <= n else 0
    else:
        c = stirling1_unsigned

    total = Fraction(0)
    # Build incrementally for j = 0 .. r:
    #   falling_j := r!/(r-j)!   (falling factorial)
    #   denom_j   := prod_{i=1}^{j+1} (r+b+i)
    falling = Fraction(1)  # r!/(r-0)! = 1
    denom = r + b + 1  # prod_{i=1}^{1} (r+b+i), for j=0 (j+1=1)
    for j in range(0, r + 1):
        if j >= 1:
            falling *= (r - j + 1)
            denom *= (r + b + j + 1)
        if j >= p:
            cj = Fraction(falling, denom)
            sk = c(j + 1, j + 1 - p)
            if sk:
                total += cj * sk
    return total


# ----------------------------------------------------------------------
# Self-tests
# ----------------------------------------------------------------------

def _direct_D_star_naive(p, r, b):
    """A maximally literal, unoptimized re-implementation of the same sum,
    recomputing every factorial from scratch each time -- used purely as an
    internal cross-check of the incremental version above."""
    total = Fraction(0)
    for j in range(p, r + 1):
        num = Fraction(math.factorial(r), math.factorial(r - j))
        den = 1
        for i in range(1, j + 2):
            den *= (r + b + i)
        cj = num / den
        sk = stirling1_unsigned(j + 1, j + 1 - p)
        total += cj * sk
    return total


def self_test():
    checks = 0
    fails = 0

    # (0) internal cross-check: incremental vs naive re-implementation.
    for p in range(0, 6):
        for r in range(p, p + 12):
            for b in range(0, 5):
                a = D_star(p, r, b)
                bb = _direct_D_star_naive(p, r, b)
                checks += 1
                if a != bb:
                    fails += 1
                    print(f"MISMATCH internal p={p} r={r} b={b}: {a} vs {bb}")

    # (1) Teorema 3 (THEOREM.md, "Estagio 8", D^*_r(0) := lim_n max_m n^2|R_r|,
    # i.e. the order-1/n^2 sharp error constant, matching p=2 in the
    # general-p indexing -- NOT p=1; confirmed by direct numerical match
    # below, not assumed):
    #   D^*_r(0) = r(3r+1)/32 * varphi_r - r/12,  varphi_r = 4^r (r!)^2/(2r+1)!
    def varphi(rr):
        return Fraction(4 ** rr * math.factorial(rr) ** 2, math.factorial(2 * rr + 1))

    def teorema3(rr):
        return Fraction(rr * (3 * rr + 1), 32) * varphi(rr) - Fraction(rr, 12)

    for r in range(0, 40):
        want = teorema3(r)
        got = D_star(2, r, 0)
        checks += 1
        if got != want:
            fails += 1
            print(f"MISMATCH Teorema3 (p=2) r={r}: got={got} want={want}")

    # (2) r<p vanishing boundary (Corollary A3's own empty-sum boundary).
    for p in range(1, 45):
        for r in range(0, p):
            checks += 1
            if D_star(p, r, 3) != 0:
                fails += 1
                print(f"MISMATCH r<p boundary p={p} r={r}")

    # (3) non-negativity smoke test at several (p,b) including large p.
    for (p, b) in [(1, 0), (5, 2), (21, 0), (40, 5), (60, 10), (80, 30)]:
        for r in range(p, p + 5):
            checks += 1
            val = D_star(p, r, b)
            # not asserting sign (no such theorem cited); just confirms no crash
            # and exactness (Fraction, denominator sane).
            if not isinstance(val, Fraction):
                fails += 1
                print(f"MISMATCH type p={p} r={r} b={b}")

    # (4) cached factorial-equivalent (falling-factorial increment) matches
    # math.factorial ratio exactly, for r up to 300 (used heavily downstream).
    for r in range(0, 300):
        checks += 1
        got = Fraction(1)
        for j in range(1, min(r, 5) + 1):
            got *= (r - j + 1)
        want = Fraction(math.factorial(r), math.factorial(r - min(r, 5)))
        if got != want:
            fails += 1
            print(f"MISMATCH falling-factorial r={r}")

    print(f"ground_truth.py self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = self_test()
    print("ground_truth.py: OK" if ok else "ground_truth.py: FAILED")
