"""
ADVERSARIAL REFEREE SCRIPT 1 (written from scratch, imports nothing from the
target directory).

Purpose: compute the rate coefficient

    c_K := K * [ phi_K/4 + F_{K-1}(1,1) - phi_K ]

EXACTLY (fractions.Fraction) straight from the RAW definition, with
F_r(t,b) taken from the already-PROVED closed form of
k6_attempt/ATTEMPT.md section 2.3, re-transcribed by hand here:

    F_r(t,b) = sum_{k=0}^{r}  r!/(r-k)!  *  t^k / prod_{i=1}^{k+1} (r+b+i)

and phi_K from THEOREM.md section 5.2 (Lemma 2):

    phi_K = 4^K (K!)^2 / (2K+1)!

Three INDEPENDENT routes to F_{K-1}(1,1) are computed and cross-checked:
  (A) the closed-form sum above, evaluated term by term;
  (B) the diagonal coefficient recursion that the closed form solves
      (k6_attempt section 2.3):
          c_0^{(r)}(b) = 1/(1+r+b),
          c_k^{(r)}(b) = r/(k+1+r+b) * c_{k-1}^{(r-1)}(b+1),
      summed at t=1, i.e. sum_k c_k^{(r)}(b);
  (C) my own hand-derived collapse
          F_{K-1}(1,1) = [(K-1)! K! / (2K)!] * (4^K - C(2K,K))/2.

Then c_K is compared against my own hand-derived closed form
    c_K = [ (K+2) phi_K - 2 ] / 4
and against the manifestly positive telescoping sum
    c_K = (1/4) sum_{j=1}^{K-1} j phi_j / (2j+3).

Nothing here is floating point except explicitly-labelled display columns.
"""

from fractions import Fraction as Fr
from math import comb, factorial
import sys


def phi(K):
    """Wallis integral int_0^1 (1-t^2)^K dt = 4^K (K!)^2/(2K+1)!  (exact)."""
    return Fr(4 ** K * factorial(K) ** 2, factorial(2 * K + 1))


def F_closed(r, t, b):
    """k6_attempt section 2.3 closed form, transcribed by hand. t is a Fraction."""
    total = Fr(0)
    for k in range(0, r + 1):
        num = Fr(factorial(r), factorial(r - k))
        den = 1
        for i in range(1, k + 2):
            den *= (r + b + i)
        total += num * (t ** k) / den
    return total


def F_recursion(r, b):
    """
    F_r(1,b) via the DIAGONAL COEFFICIENT RECURSION (not the closed form):
        c_0^{(r)}(b) = 1/(1+r+b)
        c_k^{(r)}(b) = r/(k+1+r+b) * c_{k-1}^{(r-1)}(b+1)
    At t=1, F_r(1,b) = sum_{k=0}^{r} c_k^{(r)}(b).
    """
    memo = {}

    def coeff(rr, k, bb):
        key = (rr, k, bb)
        if key in memo:
            return memo[key]
        if k == 0:
            val = Fr(1, 1 + rr + bb)
        else:
            val = Fr(rr, k + 1 + rr + bb) * coeff(rr - 1, k - 1, bb + 1)
        memo[key] = val
        return val

    return sum(coeff(r, k, b) for k in range(0, r + 1))


def F_mycollapse(K):
    """My own hand-derived collapse of F_{K-1}(1,1)."""
    return (Fr(factorial(K - 1) * factorial(K), factorial(2 * K))
            * Fr(4 ** K - comb(2 * K, K), 2))


def c_raw(K):
    """RAW definition, using the closed-form F."""
    return K * (phi(K) / 4 + F_closed(K - 1, Fr(1), 1) - phi(K))


def c_theoremA(K):
    return ((K + 2) * phi(K) - 2) / 4


def c_telescope(K):
    return Fr(1, 4) * sum(Fr(j) * phi(j) / (2 * j + 3) for j in range(1, K))


def main():
    Krange = list(range(1, 51))
    print("=" * 100)
    print("PART 1: three independent routes to F_{K-1}(1,1), K = 1..50")
    print("=" * 100)
    bad = 0
    for K in Krange:
        a = F_closed(K - 1, Fr(1), 1)
        b = F_recursion(K - 1, 1)
        c = F_mycollapse(K)
        d = (Fr(2 * K + 1) * phi(K) - 1) / (2 * K)   # target's Lemma 1 statement
        if not (a == b == c == d):
            bad += 1
            print("  MISMATCH at K=%d: closed=%s recursion=%s mine=%s lemma1=%s"
                  % (K, a, b, c, d))
    print("  K=1..50: closed form == recursion == my collapse == [(2K+1)phi_K-1]/(2K)"
          "  -> mismatches: %d" % bad)

    print()
    print("=" * 100)
    print("PART 2: c_K from RAW definition vs Theorem A closed form vs telescoping sum")
    print("=" * 100)
    print("%3s  %-34s  %-12s  %-8s  %-8s  %-8s" %
          ("K", "c_K (exact, from RAW definition)", "float", "==ThmA", "==tele", "c_K>0"))
    bad2 = 0
    for K in Krange:
        cr = c_raw(K)
        ca = c_theoremA(K)
        ct = c_telescope(K)
        ok_a = (cr == ca)
        ok_t = (cr == ct)
        pos = (cr > 0)
        if not (ok_a and ok_t):
            bad2 += 1
        if K <= 14 or K % 10 == 0:
            print("%3d  %-34s  %-12.8f  %-8s  %-8s  %-8s" %
                  (K, str(cr), float(cr), ok_a, ok_t, pos))
    print("  ... (all K=1..50 checked)")
    print("  mismatches RAW vs ThmA vs telescope over K=1..50: %d" % bad2)
    print("  c_1 == 0 exactly?  %s   (c_1 = %s)" % (c_raw(1) == 0, c_raw(1)))
    print("  c_K > 0 for all 2<=K<=50? %s" %
          all(c_raw(K) > 0 for K in range(2, 51)))

    print()
    print("=" * 100)
    print("PART 3: large-K spot checks (exact rationals, RAW definition)")
    print("=" * 100)
    for K in (100, 200, 500, 1000, 5000):
        cr = c_raw(K)
        ca = c_theoremA(K)
        ct = c_telescope(K)
        print("  K=%-6d  RAW==ThmA: %-6s  RAW==telescope: %-6s  c_K>0: %-6s  "
              "c_K ~ %.10f   sqrt(pi K)/8 ~ %.10f"
              % (K, cr == ca, cr == ct, cr > 0, float(cr),
                 (3.141592653589793 * K) ** 0.5 / 8))

    print()
    print("=" * 100)
    print("PART 4: spot-check of specific exact fractions quoted in the target's table")
    print("=" * 100)
    quoted = {2: Fr(1, 30), 3: Fr(1, 14), 6: Fr(1093, 6006), 9: Fr(11773, 41990)}
    for K, val in sorted(quoted.items()):
        got = c_raw(K)
        print("  K=%-3d quoted %-14s  computed %-14s  match: %s"
              % (K, str(val), str(got), got == val))

    print()
    print("=" * 100)
    print("PART 5: anchor sanity -- F_r(1,0) must equal phi_r (k6 section 2.3 table)")
    print("=" * 100)
    ok = all(F_closed(r, Fr(1), 0) == phi(r) for r in range(0, 41))
    print("  F_r(1,0) == phi_r for r=0..40 : %s" % ok)
    for r in range(0, 7):
        print("    r=%d  F_r(1,0)=%-12s phi_r=%-12s" % (r, F_closed(r, Fr(1), 0), phi(r)))

    print()
    print("OVERALL: %s" % ("ALL EXACT CHECKS PASSED" if (bad == 0 and bad2 == 0 and ok)
                           else "FAILURES PRESENT"))


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
