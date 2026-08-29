"""
05_saddle_scaling_check.py

Route 2 / option (iii) continued: a genuinely new quantitative claim
about the order-statistic reformulation of script 03 -- the leading-
order scaling of the saddle point j*(m,n,gamma) (the true maximizer of
the T(n,m) summand, i.e. the mode of the tilted order-statistic
distribution) as m,n -> infinity with m << n.

Derivation (own, from scratch; see ATTEMPT.md Sec.4 for the full
write-up): the exact discrete crossing condition for j* is
    (j*+m+1)(n-j*-m) / [(j*+1)(n-j*)] * (1-gamma) = 1.
For m,j* = o(n) (in particular m=O(sqrt n), the range relevant to the
outer m-sum), (n-j*-m)/(n-j*) = 1+O(m/n) -> 1, so to LEADING order,
dropping O(1) shifts as m,j*->infinity:
    (j*+m)/j*  ->  1/(1-gamma)          =>   j* ~ m(1-gamma)/gamma.

This script verifies this CLAIM numerically (own fresh exact-Fraction
ratio-test locator for j*, re-derived independently of script 03's
version though the method is the same idea) at growing (m,n) with
m/n -> 0, checking j*/m -> (1-gamma)/gamma.
"""
from fractions import Fraction as F


def find_jstar(n, m, g):
    """Largest j with ratio(j)>1, i.e. the mode location, via exact
    Fraction ratio test -- own implementation."""
    j = 0
    while j <= n - m - 1:
        ratio = F(j + m + 1, j + 1) * F(n - j - m, n - j) * (1 - g)
        if ratio <= 1:
            break
        j += 1
    return j


def main():
    L = []
    def p(s=""):
        print(s)
        L.append(str(s))

    p("=" * 70)
    p("Convergence of j*/m -> (1-gamma)/gamma as m,n -> infinity, m<<n")
    p("=" * 70)
    for g_num, g_den in [(1, 2), (3, 10), (9, 10), (1, 5)]:
        g = F(g_num, g_den)
        predicted = float((1 - g) / g)
        p(f"gamma = {g}  (predicted limit (1-g)/g = {predicted:.6f})")
        for n, m in [(4000, 20), (40000, 63), (400000, 200), (4000000, 632)]:
            jstar = find_jstar(n, m, g)
            ratio = jstar / m
            p(f"    n={n:>9d} m={m:>5d} (m/n={m/n:.5f}):  j*={jstar:>6d}  "
              f"j*/m={ratio:.6f}  (rel. dev. from predicted: "
              f"{abs(ratio - predicted) / predicted * 100:.3f}%)")
        p("")

    with open("05_saddle_scaling_check.log", "w") as f:
        f.write("\n".join(L) + "\n")
    p("Log written to 05_saddle_scaling_check.log")


if __name__ == "__main__":
    main()
