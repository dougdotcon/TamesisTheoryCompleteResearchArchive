"""
Independent, from-scratch ground truth for D^{*(p)}_r(b), built ONLY from
Corollary A3 as stated in the referee task (THEOREM.md "Estagio 9",
all_orders_closed_form_attempt/ATTEMPT.md Sec 4.3):

    D^{*(p)}_r(b) := sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)

    c_j^{(r)}(b) := r! / (r-j)! / prod_{i=1}^{j+1} (r+b+i)

    c(N,M) = unsigned Stirling numbers of the first kind, standard
    recurrence c(n,k) = c(n-1,k-1) + (n-1)*c(n-1,k), c(0,0)=1.

Written fresh by the referee. No predecessor .py file was read or used.
All arithmetic is exact (Python ints / fractions.Fraction).
"""
from fractions import Fraction
from functools import lru_cache
import math

# ---------------------------------------------------------------------
# unsigned Stirling numbers of the first kind, via the standard
# recurrence, memoized. c(n,k) = c(n-1,k-1) + (n-1) c(n-1,k), c(0,0)=1.
# ---------------------------------------------------------------------

_stirling1_cache = {(0, 0): 1}


def stirling1_unsigned(n, k):
    """unsigned Stirling number of the first kind c(n,k)."""
    if k < 0 or k > n:
        return 0
    if (n, k) in _stirling1_cache:
        return _stirling1_cache[(n, k)]
    if n == 0:
        val = 1 if k == 0 else 0
    else:
        val = stirling1_unsigned(n - 1, k - 1) + (n - 1) * stirling1_unsigned(n - 1, k)
    _stirling1_cache[(n, k)] = val
    return val


def c_j_r_b(j, r, b):
    """c_j^{(r)}(b) = r!/(r-j)! / prod_{i=1}^{j+1}(r+b+i), exact Fraction."""
    if j > r or j < 0:
        return Fraction(0)
    num = 1
    for t in range(r - j + 1, r + 1):
        num *= t
    den = 1
    for i in range(1, j + 2):
        den *= (r + b + i)
    return Fraction(num, den)


def D_star(p, r, b):
    """D^{*(p)}_r(b) via Corollary A3, exact Fraction. 0 if r < p (empty sum)."""
    if r < p:
        return Fraction(0)
    total = Fraction(0)
    for j in range(p, r + 1):
        cst = stirling1_unsigned(j + 1, j + 1 - p)
        if cst == 0:
            continue
        total += c_j_r_b(j, r, b) * cst
    return total


# -----------------------------------------------------------------------
# Self-test: calibrate against every PROVED formula quoted in THEOREM.md
# and the target document that the referee can independently verify by
# hand / by an alternate closed form, PLUS internal consistency checks.
# -----------------------------------------------------------------------

def varphi_r(r):
    return Fraction(4 ** r * math.factorial(r) ** 2, math.factorial(2 * r + 1))


def self_test():
    checks = 0
    fails = 0

    # p=1, b=0: D^{*(1)}_r(0) = r/4 * varphi_r  (Estagio 14 Teorema D1 reduces
    # to b=0 calibration quoted in general_p_dstar_closure_attempt Sec 3.1)
    for r in range(0, 60):
        got = D_star(1, r, 0)
        want = Fraction(r, 4) * varphi_r(r)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=1,b=0,r=", r, got, want)

    # p=2, b=0: D^{*(2)}_r(0) = r(3r+1)/32 * varphi_r - r/12
    for r in range(0, 60):
        got = D_star(2, r, 0)
        want = Fraction(r * (3 * r + 1), 32) * varphi_r(r) - Fraction(r, 12)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=2,b=0,r=", r, got, want)

    # p=1, b=1: D^{*(1)}_r(1) = (r+1)/4 * varphi_r - 1/4
    for r in range(0, 80):
        got = D_star(1, r, 1)
        want = Fraction(r + 1, 4) * varphi_r(r) - Fraction(1, 4)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=1,b=1,r=", r, got, want)

    # p=2, b=1
    for r in range(0, 80):
        got = D_star(2, r, 1)
        want = Fraction((r + 1) * (3 * r + 8), 32) * varphi_r(r) - Fraction(5 * r + 6, 24)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=2,b=1,r=", r, got, want)

    # p=3, b=1
    for r in range(0, 80):
        got = D_star(3, r, 1)
        want = (Fraction((r + 1) * (5 * r ** 2 + 39 * r + 32), 128) * varphi_r(r)
                - Fraction((r + 1) * (7 * r + 12), 48))
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=3,b=1,r=", r, got, want)

    # p=4, b=1
    for r in range(0, 80):
        got = D_star(4, r, 1)
        want = (Fraction((r + 1) * (105 * r ** 3 + 1765 * r ** 2 + 3314 * r + 1536), 6144) * varphi_r(r)
                - Fraction(45 * r ** 3 + 229 * r ** 2 + 306 * r + 120, 480))
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=4,b=1,r=", r, got, want)

    # p=1,b=2 (wave-15 closure attempt's Theorem D1 instance, cited)
    for r in range(0, 60):
        got = D_star(1, r, 2)
        want = (Fraction((r + 2) * (r + 3), 2 * (2 * r + 3))) * varphi_r(r) - Fraction(r + 2, 2 * (r + 1))
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=1,b=2,r=", r, got, want)

    # r<p vanishing boundary, p=1..40
    for p in range(1, 41):
        for r in range(0, p):
            got = D_star(p, r, 3)
            checks += 1
            if got != 0:
                fails += 1
                print("FAIL vanishing p=", p, "r=", r, got)

    # non-negativity smoke test (D^{*(p)}_r(b) known non-negative throughout
    # this whole lineage's calibration set)
    for p in [1, 2, 3, 21, 30, 40]:
        for r in range(p, p + 20):
            for b in range(0, 5):
                got = D_star(p, r, b)
                checks += 1
                if got < 0:
                    fails += 1
                    print("FAIL non-negativity p,r,b=", p, r, b, got)

    print(f"ground_truth.py self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = self_test()
    print("ground_truth.py:", "OK" if ok else "FAILED")
