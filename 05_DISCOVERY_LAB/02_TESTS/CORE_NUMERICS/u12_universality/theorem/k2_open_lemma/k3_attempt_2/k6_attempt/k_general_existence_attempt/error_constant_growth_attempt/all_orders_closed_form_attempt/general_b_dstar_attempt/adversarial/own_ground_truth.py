"""
Independent, from-scratch implementation of Corollary A3 ground truth.
Does NOT import or read general_b_dstar_attempt/ground_truth.py or any other
script from the front under review. Own unsigned-Stirling-first-kind table,
own D^{*(p)}_r(b) implementation, own binomial-with-convention helper.

D^{*(p)}_r(b) := sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)

c_j^{(r)}(b) := r! / [ (r-j)! * prod_{i=1}^{j+1} (r+b+i) ]

c(N,M) = unsigned Stirling numbers of the first kind, via the standard
recurrence c(n,k) = c(n-1,k-1) + (n-1)*c(n-1,k), c(0,0)=1.
"""
from fractions import Fraction
from functools import lru_cache


@lru_cache(maxsize=None)
def stirling1_unsigned(n, k):
    """Unsigned Stirling numbers of the first kind c(n,k), via the classic
    recurrence x(x+1)...(x+n-1) = sum_k c(n,k) x^k."""
    if n == 0 and k == 0:
        return 1
    if n == 0 or k < 0 or k > n:
        return 0
    return stirling1_unsigned(n - 1, k - 1) + (n - 1) * stirling1_unsigned(n - 1, k)


def binom_conv(n, k):
    """Binomial coefficient with the standard combinatorial convention:
    0 if k<0 or k>n (n assumed >=0 integer)."""
    if k < 0 or k > n:
        return 0
    num = 1
    for i in range(k):
        num *= (n - i)
    den = 1
    for i in range(1, k + 1):
        den *= i
    return Fraction(num, den)


def fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def c_j_r_b(j, r, b):
    """c_j^{(r)}(b) = r! / [ (r-j)! * prod_{i=1}^{j+1} (r+b+i) ]"""
    if j > r or j < 0:
        return Fraction(0)
    num = fact(r)
    den = fact(r - j)
    prod = 1
    for i in range(1, j + 2):
        prod *= (r + b + i)
    den *= prod
    return Fraction(num, den)


def D_star(p, r, b):
    """D^{*(p)}_r(b) via Corollary A3, directly."""
    total = Fraction(0)
    for j in range(p, r + 1):
        cj = c_j_r_b(j, r, b)
        st = stirling1_unsigned(j + 1, j + 1 - p)
        total += cj * st
    return total


def varphi(r):
    """varphi_r = 4^r (r!)^2 / (2r+1)!"""
    return Fraction(4 ** r * fact(r) ** 2, fact(2 * r + 1))


if __name__ == "__main__":
    fails = 0
    checks = 0

    # ---- p=0 sanity: D^{*(0)}_r(0) should be varphi_r (well-known, p=0 case
    # of Theorem A / Corollary A3; included purely as an implementation sanity
    # check on the Stirling table & c_j formula, not claimed as part of this
    # front's scope). c(j+1,j+1) = 1 for all j (Stirling identity), so
    # D^{*(0)}_r(0) = sum_j c_j^{(r)}(0). Check this collapses to varphi_r.
    for r in range(0, 40):
        got = D_star(0, r, 0)
        want = varphi(r)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=0,b=0 varphi check", r, got, want)

    # ---- b=0 calibration: p=1 -> r/4 * varphi_r ; p=2 -> r(3r+1)/32 varphi_r - r/12
    for r in range(0, 200):
        got1 = D_star(1, r, 0)
        want1 = Fraction(r, 4) * varphi(r)
        checks += 1
        if got1 != want1:
            fails += 1
            print("FAIL p=1,b=0", r, got1, want1)

        got2 = D_star(2, r, 0)
        want2 = Fraction(r * (3 * r + 1), 32) * varphi(r) - Fraction(r, 12)
        checks += 1
        if got2 != want2:
            fails += 1
            print("FAIL p=2,b=0", r, got2, want2)

    # ---- b=1 calibration, p=1,2,3,4 (from ATTEMPT.md sec 1, itself sourced
    # from the parent document's PROVED / NUMERICALLY VERIFIED calibration --
    # used here only as a target to check the ground-truth *implementation*
    # is not buggy before trusting it for anything else)
    for r in range(0, 200):
        got = D_star(1, r, 1)
        want = Fraction(r + 1, 4) * varphi(r) - Fraction(1, 4)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=1,b=1", r, got, want)

        got = D_star(2, r, 1)
        want = Fraction((r + 1) * (3 * r + 8), 32) * varphi(r) - Fraction(5 * r + 6, 24)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=2,b=1", r, got, want)

        got = D_star(3, r, 1)
        want = Fraction((r + 1) * (5 * r * r + 39 * r + 32), 128) * varphi(r) \
            - Fraction((r + 1) * (7 * r + 12), 48)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=3,b=1", r, got, want)

        got = D_star(4, r, 1)
        want = Fraction((r + 1) * (105 * r ** 3 + 1765 * r ** 2 + 3314 * r + 1536), 6144) * varphi(r) \
            - Fraction(45 * r ** 3 + 229 * r ** 2 + 306 * r + 120, 480)
        checks += 1
        if got != want:
            fails += 1
            print("FAIL p=4,b=1", r, got, want)

    print(f"own_ground_truth.py: {checks} checks, {fails} failures")
