"""
Independent ground truth for D^{*(p)}_r(b) via Corollary A3, for this
extension front (p=11..20). Written fresh in this directory (own
unsigned-Stirling recurrence), not imported from the closure attempt's or
any predecessor's ground_truth.py -- same discipline as every predecessor
in this lineage.

Corollary A3 (cited, PROVED, not re-derived):
    D^{*(p)}_r(b) = sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)
    c_j^{(r)}(b) = r! / [ (r-j)! * prod_{i=1}^{j+1} (r+b+i) ]
    c(N,M)       = unsigned Stirling numbers of the first kind.
"""

from fractions import Fraction
from functools import lru_cache
import math


@lru_cache(maxsize=None)
def stirling1_unsigned(n, k):
    """Unsigned Stirling numbers of the first kind c(n,k), own recurrence."""
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    if k > n:
        return 0
    return stirling1_unsigned(n - 1, k - 1) + (n - 1) * stirling1_unsigned(n - 1, k)


def c_stirling(N, M):
    if M < 0 or M > N:
        return 0
    return stirling1_unsigned(N, M)


def c_j_r_b(j, r, b):
    """c_j^{(r)}(b), exact Fraction."""
    if j > r or j < 0:
        return Fraction(0)
    num = Fraction(math.factorial(r))
    denom = Fraction(math.factorial(r - j))
    prod = 1
    for i in range(1, j + 2):
        prod *= (r + b + i)
    denom *= prod
    return num / denom


def D_star(p, r, b):
    """D^{*(p)}_r(b), exact Fraction, via Corollary A3."""
    total = Fraction(0)
    for j in range(p, r + 1):
        cj = c_j_r_b(j, r, b)
        if cj == 0:
            continue
        st = c_stirling(j + 1, j + 1 - p)
        if st == 0:
            continue
        total += cj * st
    return total


def phi_r(r):
    """varphi_r = 4^r (r!)^2 / (2r+1)! (normalisation aid only)."""
    return Fraction(4 ** r * math.factorial(r) ** 2, math.factorial(2 * r + 1))


if __name__ == "__main__":
    print("=== ground_truth.py (extension front): sanity checks ===")

    # Cross-check against the closure attempt's already-established p=1..10
    # instances is done in assemble_ext.py (it imports nothing from the
    # closure attempt's own scripts, but reproduces the same printed
    # calibration numbers as an internal sanity gate before trusting this
    # ground truth for p=11..20). Here: the same b=0,1 PROVED-formula
    # checks the closure attempt itself ran, as a minimal self-contained
    # smoke test that this fresh Stirling implementation is correct.

    fails = 0
    for r in range(0, 60):
        lhs = D_star(1, r, 0)
        rhs = Fraction(r, 4) * phi_r(r)
        if lhs != rhs:
            fails += 1
            print("MISMATCH p=1,b=0,r=", r, lhs, rhs)
    print(f"p=1,b=0 vs r/4*varphi_r: r=0..59, fails={fails}")

    fails2 = 0
    for r in range(0, 60):
        lhs = D_star(2, r, 0)
        rhs = Fraction(r * (3 * r + 1), 32) * phi_r(r) - Fraction(r, 12)
        if lhs != rhs:
            fails2 += 1
            print("MISMATCH p=2,b=0,r=", r, lhs, rhs)
    print(f"p=2,b=0 vs r(3r+1)/32*varphi_r - r/12: r=0..59, fails={fails2}")

    def D1_b1(r):
        return Fraction(r + 1, 4) * phi_r(r) - Fraction(1, 4)

    def D4_b1(r):
        return Fraction((r + 1) * (105 * r ** 3 + 1765 * r ** 2 + 3314 * r + 1536), 6144) * phi_r(r) \
            - Fraction(45 * r ** 3 + 229 * r ** 2 + 306 * r + 120, 480)

    fails3 = 0
    for r in range(0, 80):
        if D_star(1, r, 1) != D1_b1(r):
            fails3 += 1
    for r in range(0, 80):
        if D_star(4, r, 1) != D4_b1(r):
            fails3 += 1
    print(f"p=1,4 b=1 vs PROVED formulas: r=0..79, fails={fails3}")

    # r<p vanishing boundary, extended further than the closure attempt
    # (p up to 20, since this front needs that range)
    fails4 = 0
    checks4 = 0
    for p in range(1, 21):
        for r in range(0, min(p, 12)):
            for b in range(0, 6):
                checks4 += 1
                if D_star(p, r, b) != 0:
                    fails4 += 1
                    print("MISMATCH r<p nonzero:", p, r, b)
    print(f"r<p vanishing (p up to 20): {checks4} checks, fails={fails4}")

    total_fails = fails + fails2 + fails3 + fails4
    assert total_fails == 0, "GROUND TRUTH SELF-CHECK FAILURE"
    print("=== all ground_truth.py sanity checks passed ===")
