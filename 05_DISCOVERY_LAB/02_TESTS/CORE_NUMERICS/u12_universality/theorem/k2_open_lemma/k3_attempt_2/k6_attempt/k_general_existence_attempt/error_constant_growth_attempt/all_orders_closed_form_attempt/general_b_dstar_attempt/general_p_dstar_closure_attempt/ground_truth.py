"""
Independent, from-scratch ground truth for D^{*(p)}_r(b) via Corollary A3.

Written without reading or importing ANY script from the parent
(general_b_dstar_attempt) or the referee (adversarial/) directories --
only the printed formula (Corollary A3) and the printed calibration
formulas were read, per task instructions.

Corollary A3:  D^{*(p)}_r(b) = sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)
    c_j^{(r)}(b) = r! / [ (r-j)! * prod_{i=1}^{j+1} (r+b+i) ]
    c(N,M)       = unsigned Stirling numbers of the first kind.

All arithmetic exact (fractions.Fraction). c(N,M) built here from scratch
via the standard recurrence c(n,k) = c(n-1,k-1) + (n-1)*c(n-1,k).
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
    """varphi_r = 4^r (r!)^2 / (2r+1)!  (as recorded in the sibling referee
    report, error_constant_growth_attempt/adversarial/REFEREE_REPORT.md,
    used here only as a printable normalisation aid, not as derivation
    input)."""
    return Fraction(4 ** r * math.factorial(r) ** 2, math.factorial(2 * r + 1))


if __name__ == "__main__":
    print("=== ground_truth.py: sanity checks against PROVED calibration formulas ===")

    # b=0, p=1: D^{*(1)}_r(0) = r/4 * varphi_r
    fails = 0
    for r in range(0, 60):
        lhs = D_star(1, r, 0)
        rhs = Fraction(r, 4) * phi_r(r)
        if lhs != rhs:
            fails += 1
            print("MISMATCH p=1,b=0,r=", r, lhs, rhs)
    print(f"p=1,b=0 vs r/4*varphi_r: r=0..59, fails={fails}")

    # b=0, p=2: D^{*(2)}_r(0) = r(3r+1)/32 * varphi_r - r/12
    fails = 0
    for r in range(0, 60):
        lhs = D_star(2, r, 0)
        rhs = Fraction(r * (3 * r + 1), 32) * phi_r(r) - Fraction(r, 12)
        if lhs != rhs:
            fails += 1
            print("MISMATCH p=2,b=0,r=", r, lhs, rhs)
    print(f"p=2,b=0 vs r(3r+1)/32*varphi_r - r/12: r=0..59, fails={fails}")

    # b=1, p=1..4 (PROVED calibration formulas quoted in the parent document)
    def D1_b1(r):
        return Fraction(r + 1, 4) * phi_r(r) - Fraction(1, 4)

    def D2_b1(r):
        return Fraction((r + 1) * (3 * r + 8), 32) * phi_r(r) - Fraction(5 * r + 6, 24)

    def D3_b1(r):
        return Fraction((r + 1) * (5 * r ** 2 + 39 * r + 32), 128) * phi_r(r) \
            - Fraction((r + 1) * (7 * r + 12), 48)

    def D4_b1(r):
        return Fraction((r + 1) * (105 * r ** 3 + 1765 * r ** 2 + 3314 * r + 1536), 6144) * phi_r(r) \
            - Fraction(45 * r ** 3 + 229 * r ** 2 + 306 * r + 120, 480)

    for p, f in [(1, D1_b1), (2, D2_b1), (3, D3_b1), (4, D4_b1)]:
        fails = 0
        for r in range(0, 80):
            lhs = D_star(p, r, 1)
            rhs = f(r)
            if lhs != rhs:
                fails += 1
                print(f"MISMATCH p={p},b=1,r=", r, lhs, rhs)
        print(f"p={p},b=1 vs PROVED formula: r=0..79, fails={fails}")

    # r<p must give 0 (empty Corollary-A3 sum)
    fails = 0
    checks = 0
    for p in range(1, 9):
        for r in range(0, p):
            for b in range(0, 10):
                checks += 1
                if D_star(p, r, b) != 0:
                    fails += 1
                    print("MISMATCH r<p nonzero:", p, r, b)
    print(f"r<p vanishing: {checks} checks, fails={fails}")

    print("=== all ground_truth.py sanity checks done ===")
