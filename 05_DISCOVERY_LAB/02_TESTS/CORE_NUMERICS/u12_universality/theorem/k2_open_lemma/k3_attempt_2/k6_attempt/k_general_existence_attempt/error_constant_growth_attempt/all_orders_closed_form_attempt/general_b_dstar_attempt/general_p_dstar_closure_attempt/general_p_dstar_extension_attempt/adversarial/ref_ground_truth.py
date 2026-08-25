# Hostile-referee ground truth (extension front): OWN from-scratch Corollary A3.
#   D*(p)_r(b) = sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p),
#   c_j^{(r)}(b) = r! / [ (r-j)! * prod_{i=1}^{j+1} (r+b+i) ],
#   c(n,k) = unsigned Stirling numbers of the first kind,
#            c(0,0)=1, c(n,k) = c(n-1,k-1) + (n-1) c(n-1,k).
# Own Stirling table, own summation (single common denominator -> one Fraction).
# None of the target front's .py files were read. Exact arithmetic only.

from fractions import Fraction
from math import factorial
import sys

_STIRLING_ROWS = [[1]]  # row n holds c(n, k) for k=0..n


def stirling_row(n):
    """Unsigned Stirling first kind, row n (cached, own recurrence)."""
    while len(_STIRLING_ROWS) <= n:
        m = len(_STIRLING_ROWS)          # building row m from row m-1
        prev = _STIRLING_ROWS[m - 1]
        row = [0] * (m + 1)
        for k in range(0, m + 1):
            v = 0
            if k >= 1:
                v += prev[k - 1]
            if k <= m - 1:
                v += (m - 1) * prev[k]
            row[k] = v
        _STIRLING_ROWS.append(row)
    return _STIRLING_ROWS[n]


def D_star(p, r, b):
    """Corollary A3, exact. Single common denominator prod_{i=1}^{r+1}(r+b+i)."""
    if r < p:
        return Fraction(0)
    # suffix products: tail[j] = prod_{i=j+2}^{r+1} (r+b+i)
    tail = [1] * (r + 2)
    for j in range(r - 1, -1, -1):
        tail[j] = tail[j + 1] * (r + b + j + 2)
    denom = 1
    for i in range(1, r + 2):
        denom *= (r + b + i)
    num = 0
    falling = 1
    for j in range(0, r + 1):        # falling = r!/(r-j)!
        if j > 0:
            falling *= (r - j + 1)
        if j >= p:
            row = stirling_row(j + 1)
            num += falling * row[j + 1 - p] * tail[j]
    return Fraction(num, denom)


def varphi(r):
    return Fraction(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))


def main():
    fails = 0
    checks = 0

    # PROVED calibration formulas (upstream, accepted):
    for r in range(0, 61):
        vr = varphi(r)
        checks += 1
        if D_star(1, r, 0) != Fraction(r, 4) * vr:
            fails += 1; print("FAIL p=1 b=0 r=", r)
        checks += 1
        if D_star(2, r, 0) != Fraction(r * (3 * r + 1), 32) * vr - Fraction(r, 12):
            fails += 1; print("FAIL p=2 b=0 r=", r)
        checks += 1
        if D_star(1, r, 1) != Fraction(r + 1, 4) * vr - Fraction(1, 4):
            fails += 1; print("FAIL p=1 b=1 r=", r)
        # parent's Theorem D1 instance p=1, b=2
        checks += 1
        if D_star(1, r, 2) != Fraction((r + 2) * (r + 3), 2 * (2 * r + 3)) * vr \
                - Fraction(r + 2, 2 * (r + 1)):
            fails += 1; print("FAIL p=1 b=2 r=", r)
        # closure attempt's PROVED p=4, b=1 calibration row
        checks += 1
        want = Fraction((r + 1) * (105 * r ** 3 + 1765 * r ** 2 + 3314 * r + 1536), 6144) * vr \
            - Fraction(45 * r ** 3 + 229 * r ** 2 + 306 * r + 120, 480)
        if D_star(4, r, 1) != want:
            fails += 1; print("FAIL p=4 b=1 r=", r)
    print(f"calibration vs 5 PROVED formulas, r=0..60: {checks} checks, fails={fails}")

    # r < p vanishing boundary through p=20
    v_checks = 0
    for p in range(1, 21):
        for r in range(0, p):
            for b in (0, 1, 2, 7, 30):
                v_checks += 1
                if D_star(p, r, b) != 0:
                    fails += 1; print("FAIL vanish", p, r, b)
    checks += v_checks
    print(f"r<p vanishing, p=1..20, b in {{0,1,2,7,30}}: {v_checks} checks")

    print(f"TOTAL ground-truth self-checks: {checks}, fails={fails}")
    assert fails == 0
    print("ALL REFEREE GROUND-TRUTH SELF-CHECKS PASSED")


if __name__ == "__main__":
    main()
