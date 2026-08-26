"""
Independent, from-scratch implementation of Corollary A3 -- the referee's
ground truth for this front's (wave 19, front (c)) main claim.

    D^{*(p)}_r(b) := sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)
    c_j^{(r)}(b)   := r!/(r-j)! / prod_{i=1}^{j+1} (r+b+i)
    c(N,M)         := unsigned Stirling numbers of the first kind

Written entirely from the mathematical description in THEOREM.md /
ATTEMPT.md prose. No .py file from any front in this lineage was opened,
read, or imported. fractions.Fraction throughout -- no floating point.
"""
from fractions import Fraction
from functools import lru_cache

# ---------------------------------------------------------------------
# Unsigned Stirling numbers of the first kind, c(n,k), via the standard
# recurrence c(n,k) = c(n-1,k-1) + (n-1)*c(n-1,k), c(0,0)=1, c(n,0)=0 for
# n>0, c(0,k)=0 for k>0. Own table, built once, reused.
# ---------------------------------------------------------------------
_stirling1_table = [[1]]  # row 0: c(0,0)=1


def _grow_stirling1(n_max):
    while len(_stirling1_table) <= n_max:
        n = len(_stirling1_table)
        prev = _stirling1_table[n - 1]
        row = [0] * (n + 1)
        row[0] = 0
        for k in range(1, n + 1):
            a = prev[k - 1] if k - 1 < len(prev) else 0
            b = prev[k] if k < len(prev) else 0
            row[k] = a + (n - 1) * b
        _stirling1_table.append(row)


def stirling1(n, k):
    """Unsigned Stirling number of the first kind, c(n,k)."""
    if n < 0 or k < 0:
        return 0
    if k > n:
        return 0
    _grow_stirling1(n)
    row = _stirling1_table[n]
    if k >= len(row):
        return 0
    return row[k]


# ---------------------------------------------------------------------
# c_j^{(r)}(b), built incrementally in j for fixed (r,b):
#   c_0^{(r)}(b) = 1/(r+b+1)
#   c_j^{(r)}(b) = c_{j-1}^{(r)}(b) * (r-j+1)/(r+b+j+1),  j=1,...,r
# (falling-factorial ratio r!/(r-j)! advances by a factor (r-j+1) per
# step; the denominator product prod_{i=1}^{j+1}(r+b+i) advances by a
# factor (r+b+j+1) per step -- elementary, checked against a fully naive
# per-term math.factorial computation in self_test below.)
# ---------------------------------------------------------------------
def c_j_array(r, b):
    """Return [c_0^{(r)}(b), c_1^{(r)}(b), ..., c_r^{(r)}(b)] exactly."""
    out = [Fraction(1, r + b + 1)]
    cur = out[0]
    for j in range(1, r + 1):
        cur = cur * Fraction(r - j + 1, r + b + j + 1)
        out.append(cur)
    return out


def D_star(p, r, b):
    """Corollary A3, direct sum, exact Fraction."""
    if r < p:
        return Fraction(0)
    cj = c_j_array(r, b)
    total = Fraction(0)
    for j in range(p, r + 1):
        s = stirling1(j + 1, j + 1 - p)
        if s == 0:
            continue
        total += cj[j] * s
    return total


# ---------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------
def _naive_D_star(p, r, b):
    """Fully naive per-term recomputation, math.factorial, no incremental
    recursion at all -- an independent cross-check of c_j_array's
    correctness."""
    import math
    if r < p:
        return Fraction(0)
    total = Fraction(0)
    for j in range(p, r + 1):
        num = math.factorial(r)
        den_fact = math.factorial(r - j)
        denom_prod = 1
        for i in range(1, j + 2):
            denom_prod *= (r + b + i)
        cj = Fraction(num, den_fact * denom_prod)
        s = stirling1(j + 1, j + 1 - p)
        total += cj * s
    return total


def self_test():
    checks = 0
    fails = 0

    # (1) c_j_array vs naive per-term recomputation
    for r in range(0, 40):
        for b in (0, 1, 3, 7, 20):
            cj = c_j_array(r, b)
            for j in range(0, r + 1):
                num = 1
                for t in range(r - j + 1, r + 1):
                    num *= t
                denom = 1
                for i in range(1, j + 2):
                    denom *= (r + b + i)
                want = Fraction(num, denom)
                checks += 1
                if cj[j] != want:
                    fails += 1
                    print("MISMATCH c_j", r, b, j, cj[j], want)

    # (2) D_star vs fully-naive D_star (independent recomputation)
    for p in (1, 2, 5, 10, 21, 41, 60, 80):
        for r in range(p, p + 15):
            for b in (0, 1, 5):
                checks += 1
                a = D_star(p, r, b)
                w = _naive_D_star(p, r, b)
                if a != w:
                    fails += 1
                    print("MISMATCH D_star", p, r, b, a, w)

    # (3) r < p vanishing boundary
    for p in range(1, 81):
        for r in range(0, p):
            checks += 1
            if D_star(p, r, 3) != 0:
                fails += 1
                print("MISMATCH r<p boundary", p, r)

    # (4) Teorema 3 calibration: THEOREM.md "Estagio 8", D^*_r(0) at the
    # order-1/n^2 level is D^{*(2)}_r(0) = r(3r+1)/32*varphi_r - r/12,
    # varphi_r = 4^r (r!)^2/(2r+1)!.  (Confirmed to be p=2, NOT p=1 --
    # this referee independently derived this from THEOREM.md's own text
    # BEFORE writing any test, so no analogous p=1-vs-p=2 confusion
    # occurred here; see REFEREE_REPORT.md Sec.6 for cross-check against
    # the target front's own self-disclosed version of this same
    # confusion.)
    import math as _math

    def varphi(r):
        return Fraction(4 ** r * (_math.factorial(r)) ** 2, _math.factorial(2 * r + 1))

    def teorema3(r):
        return Fraction(r * (3 * r + 1), 32) * varphi(r) - Fraction(r, 12)

    for r in range(0, 60):
        checks += 1
        a = D_star(2, r, 0)
        w = teorema3(r)
        if a != w:
            fails += 1
            print("MISMATCH Teorema3", r, a, w)

    # (5) Also confirm p=1,b=0 does NOT match Teorema 3 for r>=2 (sanity
    # that we are testing the right index, not a coincidence)
    mismatched_p1 = 0
    for r in range(2, 20):
        if D_star(1, r, 0) != teorema3(r):
            mismatched_p1 += 1
    checks += 1
    if mismatched_p1 != 18:
        fails += 1
        print("UNEXPECTED: p=1 matches Teorema3 more than expected", mismatched_p1)

    print(f"ground_truth.py self_test: {checks} checks, {fails} fails")
    return checks, fails


if __name__ == "__main__":
    self_test()
