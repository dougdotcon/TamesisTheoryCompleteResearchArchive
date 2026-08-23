"""
Ground truth for D^{*(p)}_r(b), built ONLY from the already-PROVED Corollary A3 of
all_orders_closed_form_attempt/ATTEMPT.md:

    D^{*(p)}_r(b) = sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)

with c_j^{(r)}(b) = r! / (r-j)! / prod_{i=1}^{j+1} (r+b+i)   (its own §4)
and c(N,M) the unsigned Stirling numbers of the first kind (own from-scratch table,
standard recursion c(n,k) = c(n-1,k-1) + (n-1)*c(n-1,k), n,k>=0, c(0,0)=1).

Exact fractions.Fraction throughout. Nothing here is imported from any sibling or
predecessor directory (written from scratch). This module is the SOLE ground truth
every derived closed form in this directory is checked against.
"""
from fractions import Fraction as F
import math


def factorial(n):
    return math.factorial(n)


def binom(n, k):
    if k < 0 or k > n or n < 0:
        return 0
    return math.comb(n, k)


_STIRLING_CACHE = {0: [[1]]}


def _stirling1_table(nmax):
    S = [[0] * (nmax + 1) for _ in range(nmax + 1)]
    S[0][0] = 1
    for i in range(1, nmax + 1):
        for j in range(0, i + 1):
            S[i][j] = (S[i - 1][j - 1] if j - 1 >= 0 else 0) + (i - 1) * S[i - 1][j]
    return S


_STAB = _stirling1_table(500)


def stirling1(n, k):
    """Unsigned Stirling number of the first kind c(n,k) = |s(n,k)|."""
    if n < 0 or k < 0 or k > n:
        return 0
    if n >= len(_STAB):
        raise ValueError(f"stirling1 table too small for n={n}")
    return _STAB[n][k]


def phi_r(r):
    return F(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))


def c_j_r_b(j, r, b):
    """c_j^{(r)}(b) = r!/(r-j)! / prod_{i=1}^{j+1} (r+b+i), else 0 if j>r or j<0."""
    if j > r or j < 0:
        return F(0)
    num = F(factorial(r), factorial(r - j))
    denom = 1
    for i in range(1, j + 2):
        denom *= (r + b + i)
    return num / denom


def Dstar(p, r, b):
    """D^{*(p)}_r(b), ground truth, via Corollary A3."""
    total = F(0)
    for j in range(p, r + 1):
        total += c_j_r_b(j, r, b) * stirling1(j + 1, j + 1 - p)
    return total


if __name__ == "__main__":
    # Smoke test: reproduce the PROVED b=0 and b=1 calibration formulas exactly.
    print("Smoke test against PROVED calibration formulas")
    ok = True
    for r in range(0, 30):
        d0 = Dstar(0, r, 0)
        if d0 != phi_r(r):
            ok = False
            print("FAIL D*(0)_r(0)", r)
        d1 = Dstar(1, r, 0)
        if d1 != F(r, 4) * phi_r(r):
            ok = False
            print("FAIL D*(1)_r(0)", r)
    for r in range(0, 40):
        lhs = Dstar(1, r, 1)
        rhs = F(r + 1, 4) * phi_r(r) - F(1, 4)
        if lhs != rhs:
            ok = False
            print("FAIL D*(1)_r(1)", r)
        lhs2 = Dstar(2, r, 1)
        rhs2 = F((r + 1) * (3 * r + 8), 32) * phi_r(r) - F(5 * r + 6, 24)
        if lhs2 != rhs2:
            ok = False
            print("FAIL D*(2)_r(1)", r)
        lhs3 = Dstar(3, r, 1)
        rhs3 = F((r + 1) * (5 * r ** 2 + 39 * r + 32), 128) * phi_r(r) - F((r + 1) * (7 * r + 12), 48)
        if lhs3 != rhs3:
            ok = False
            print("FAIL D*(3)_r(1)", r)
        lhs4 = Dstar(4, r, 1)
        rhs4 = F((r + 1) * (105 * r ** 3 + 1765 * r ** 2 + 3314 * r + 1536), 6144) * phi_r(r) - \
            F(45 * r ** 3 + 229 * r ** 2 + 306 * r + 120, 480)
        if lhs4 != rhs4:
            ok = False
            print("FAIL D*(4)_r(1)", r)
    print("ALL OK" if ok else "FAILURES ABOVE")
