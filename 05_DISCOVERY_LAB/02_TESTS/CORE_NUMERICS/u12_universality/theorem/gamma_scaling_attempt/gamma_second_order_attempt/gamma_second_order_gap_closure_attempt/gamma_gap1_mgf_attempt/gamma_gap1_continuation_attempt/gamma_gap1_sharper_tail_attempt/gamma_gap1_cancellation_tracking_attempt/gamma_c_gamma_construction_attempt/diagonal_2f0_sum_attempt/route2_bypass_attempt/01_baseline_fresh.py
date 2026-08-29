"""
01_baseline_fresh.py

Fresh, independently-written baseline for the ROUTE2-BYPASS-ATTEMPT front
(wave 30, front a). NOT copied from any ancestor/predecessor script --
written directly from the mathematical prose of the required reading
(Lemma 1 of gamma_scaling_attempt/ATTEMPT.md; the diagonal_2f0_sum_attempt
ATTEMPT.md's double-sum swap identity, S3).

Part A. Direct evaluator of A_k(n,gamma) from Lemma 1's own definition
        (exact Fraction arithmetic):
            A_k(n,g) = sum_{m=0}^{k} C(k,m) g^m (1-g)^(k-m) * P(k,m)
            P(k,m)   = prod_{i=1}^{m} (1 - (k-i)/n)
        and S_n(g) := sum_{k=1}^n A_k(n,g) = n*phi(n, g n).

Part B. Independent re-derivation of the double-sum swap identity
            S_n'(g) := 1 + S_n(g) = sum_{m=0}^n (g^m/n^m) m! T(n,m)
            T(n,m)  := sum_{j=0}^{n-m} C(j+m,m) C(n-j,m) (1-g)^j
        by directly re-summing the SAME triple structure via a different
        index substitution (k = j+m) -- fresh code, own derivation, cross
        checked against Part A's S_n at many (n,gamma) pairs.

Everything here is exact rational arithmetic (Python Fraction). No
approximation, no randomness anywhere in this script.
"""
import sys
from fractions import Fraction as F
from math import comb


def A_k_direct(n, k, g):
    """A_k(n,g) via Lemma 1's own defining sum over m (exact Fraction g)."""
    total = F(0)
    # incremental product P(k,m) = P(k,m-1) * (1 - (k-m)/n)
    prod = F(1)
    for m in range(0, k + 1):
        if m > 0:
            prod *= (1 - F(k - m, n))
        term = comb(k, m) * (g ** m) * ((1 - g) ** (k - m)) * prod
        total += term
    return total


def S_n_direct(n, g):
    return sum(A_k_direct(n, k, g) for k in range(1, n + 1))


def T_nm(n, m, g):
    """T(n,m) := sum_{j=0}^{n-m} C(j+m,m) C(n-j,m) (1-g)^j, exact."""
    total = F(0)
    for j in range(0, n - m + 1):
        total += comb(j + m, m) * comb(n - j, m) * ((1 - g) ** j)
    return total


def S_n_prime_via_swap(n, g):
    """S_n' = sum_{m=0}^{n} (g^m/n^m) m! T(n,m).  (own re-derivation)"""
    total = F(0)
    for m in range(0, n + 1):
        total += (g ** m) * F(1, n ** m if m > 0 else 1) * F(1) * (
            __import__("math").factorial(m)
        ) * T_nm(n, m, g)
    return total


def main():
    log = []

    def p(s=""):
        print(s)
        log.append(s)

    p("=" * 70)
    p("Part A: sanity of A_k_direct / S_n_direct (own fresh code)")
    p("=" * 70)
    # q=0 sanity: A_k(n,0) = 1 for all k -> S_n(0) = n
    for n in [1, 2, 5, 8]:
        s = S_n_direct(n, F(0))
        ok = (s == n)
        p(f"n={n}, gamma=0: S_n = {s}  (expect {n})  {'OK' if ok else 'MISMATCH'}")
        assert ok

    # q=1 endpoint: S_n(1) = Q(n) = sum_k (n)_k/n^k, cross-check via a
    # SEPARATE direct falling-factorial evaluator (not reusing A_k_direct)
    def Q_n_direct(n):
        total = F(0)
        for k in range(1, n + 1):
            num = F(1)
            for i in range(k):
                num *= F(n - i, n)
            total += num
        return total

    for n in [1, 2, 3, 5, 8, 12]:
        s1 = S_n_direct(n, F(1))
        s2 = Q_n_direct(n)
        ok = (s1 == s2)
        p(f"n={n}, gamma=1: S_n(via A_k)={s1}  Q(n)(direct)={s2}  {'OK' if ok else 'MISMATCH'}")
        assert ok

    p("")
    p("=" * 70)
    p("Part B: fresh re-derivation of the double-sum swap identity")
    p("  S_n' = 1 + S_n =?= sum_m (g^m/n^m) m! T(n,m)")
    p("=" * 70)
    mismatches = 0
    checks = 0
    test_pairs = [
        (3, F(1, 3)), (3, F(1, 2)), (4, F(2, 5)), (5, F(1, 4)),
        (6, F(3, 7)), (7, F(1, 2)), (8, F(2, 9)), (9, F(1, 3)),
        (10, F(3, 10)), (5, F(1, 10)), (5, F(9, 10)), (6, F(1, 6)),
    ]
    for n, g in test_pairs:
        sn = S_n_direct(n, g)
        sn_prime_expected = F(1) + sn
        sn_prime_swap = S_n_prime_via_swap(n, g)
        checks += 1
        ok = (sn_prime_expected == sn_prime_swap)
        if not ok:
            mismatches += 1
        p(f"n={n:2d}, gamma={str(g):>6s}: 1+S_n={str(sn_prime_expected):>14s}  "
          f"swap={str(sn_prime_swap):>14s}  {'OK' if ok else 'MISMATCH'}")

    p("")
    p(f"Part B total: {checks} checks, {mismatches} mismatches")
    assert mismatches == 0

    p("")
    p("=" * 70)
    p("Part C: T(n,m) values for small (n,m) -- for use by script 02")
    p("=" * 70)
    for n in [6, 8]:
        for m in [0, 1, 2, 3]:
            if m <= n:
                val = T_nm(n, m, F(3, 10))
                p(f"T({n},{m}; gamma=3/10) = {val}")

    with open("01_baseline_fresh.log", "w") as f:
        f.write("\n".join(log) + "\n")
    p("")
    p("ALL PART A/B CHECKS PASSED. Log written to 01_baseline_fresh.log")


if __name__ == "__main__":
    main()
