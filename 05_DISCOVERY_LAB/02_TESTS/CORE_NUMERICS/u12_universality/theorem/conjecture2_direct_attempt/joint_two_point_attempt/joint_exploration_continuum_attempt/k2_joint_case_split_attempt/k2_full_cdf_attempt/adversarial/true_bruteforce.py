#!/usr/bin/env python3
"""
INDEPENDENT adversarial re-verification of ATTEMPT.md's Proposicao D2.

Written entirely from THEOREM.md's Definition 4 (prose) and the target
ATTEMPT.md's own restatement of Definition 4 in section 1.2 -- NO .py file
from k2_full_cdf_attempt, k2_joint_case_split_attempt, k3_joint_structural_
attempt, k3_full_cdf_attempt, general_k_joint_attempt, or any ancestor was
opened, read, or imported to produce this script.

Definition 4 (K=2 instance), as stated in THEOREM.md Sec 7.2 / ATTEMPT.md
Sec 1.2:
    pi        : uniform random permutation of [n] = {0, ..., n-1}
    sources   : {0, 1}  (fixed WLOG by Definition 4's own exchangeability)
    U0, U1    : i.i.d. Uniform([n]), independent of pi
    f(i)      := U_i        for i in {0, 1}
    f(i)      := pi(i)      otherwise
    T         := #{cyclic points of f}   (points i with f^k(i) = i for
                                           some k >= 1)
    M_n^(2)   := T / n

This script enumerates EVERY (pi, U0, U1) triple exactly (n! * n^2 of
them), computes T for each by direct functional-graph cycle detection,
and tabulates the exact distribution of T as Fraction(count, n! * n^2).

It then compares P(T <= k) against Proposicao D2's claimed closed form

    P(M_n^(2) <= k/n) = k(k+1)(2n^2 - 3n + k - k^2) / (n^3 (n-1))         (0 <= k <= n-1)
    P(M_n^(2) <= k/n) = 1                                                (k >= n)

Usage: python3 true_bruteforce.py <n_min> <n_max>
"""
import sys
import itertools
from fractions import Fraction


def cyclic_count(f, n):
    """Return the number of points i in [0,n) lying on a cycle of the
    functional graph i -> f[i]. Standard 3-color (white/gray/black) DFS,
    O(n) total. Written from scratch."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    cyclic = [False] * n
    for start in range(n):
        if color[start] != WHITE:
            continue
        path = []
        node = start
        while color[node] == WHITE:
            color[node] = GRAY
            path.append(node)
            node = f[node]
        if color[node] == GRAY:
            # node is on the current path -> found a genuine cycle.
            idx = path.index(node)
            for c in path[idx:]:
                cyclic[c] = True
        # mark everything in path as done
        for c in path:
            color[c] = BLACK
    return sum(cyclic)


def d2_formula(n, k):
    """Proposicao D2's claimed closed form, transcribed EXACTLY from
    ATTEMPT.md section 4.3 (as a rational-arithmetic check target only --
    this function is never used to generate data, only to compare)."""
    if k >= n:
        return Fraction(1)
    if k < 0:
        return Fraction(0)
    num = k * (k + 1) * (2 * n * n - 3 * n + k - k * k)
    den = n ** 3 * (n - 1)
    return Fraction(num, den)


def true_bruteforce_cdf(n):
    """Return dict k -> Fraction P(T <= k), by full exhaustive enumeration
    of Definition 4's K=2 model."""
    total = 0
    count_T = [0] * (n + 1)
    for pi in itertools.permutations(range(n)):
        for U0 in range(n):
            for U1 in range(n):
                f = list(pi)
                f[0] = U0
                f[1] = U1
                T = cyclic_count(f, n)
                count_T[T] += 1
                total += 1
    cdf = {}
    running = 0
    for k in range(n + 1):
        running += count_T[k]
        cdf[k] = Fraction(running, total)
    return cdf, total, count_T


def main():
    n_min = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n_max = int(sys.argv[2]) if len(sys.argv) > 2 else 8

    all_ok = True
    total_checks = 0
    for n in range(n_min, n_max + 1):
        cdf, total, count_T = true_bruteforce_cdf(n)
        print(f"n={n}  total_configs={total}  raw_counts={count_T}")
        n_ok = True
        for k in range(0, n):  # 0 <= k <= n-1 is D2's claimed domain
            claim = d2_formula(n, k)
            actual = cdf[k]
            total_checks += 1
            if claim != actual:
                n_ok = False
                all_ok = False
                print(f"  MISMATCH at n={n}, k={k}: bruteforce={actual}  "
                      f"D2_formula={claim}")
            else:
                print(f"  k={k}: OK  P(T<={k}) = {actual}")
        # sanity: k=n must give 1
        if cdf[n] != Fraction(1):
            print(f"  SANITY FAIL: P(T<=n) != 1 at n={n}: {cdf[n]}")
            all_ok = False
        print(f"  n={n}: {'ALL MATCH' if n_ok else 'MISMATCH FOUND'}")
        print()

    print(f"TOTAL COMPARISONS: {total_checks}")
    print("VERDICT:", "ALL PASSED" if all_ok else "AT LEAST ONE MISMATCH")


if __name__ == "__main__":
    main()
