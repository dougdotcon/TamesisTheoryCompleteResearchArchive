"""
Independent sanity check of the TRANSITION RULES themselves (markov_transfer.py's
g/h recursion), separate from the symbolic telescoping-sum solution: a direct
memoized exact-fraction recursion for CONCRETE small n, compared against
psi_bruteforce_ref.py's exhaustive enumeration. If markov_transfer.py's symbolic
closed forms had a bug in the *summation* step (but the transition rules themselves
were right), this script -- which never sums anything, just recurses -- would still
match brute force while the closed form might not; conversely if the transition
rules themselves were wrong, this would disagree with brute force regardless of any
summation. Matching brute force here is therefore an independent check of the model,
not merely of the algebra.
"""
from fractions import Fraction as F
from functools import lru_cache
import sys
from psi_bruteforce_ref import psi_n_K


def psi_markov(n, K):
    n = F(n)

    @lru_cache(maxsize=None)
    def g(a, b, r):
        m = n - a
        term = F(1, 1) / m
        if r >= 1:
            term += F(r, 1) / m * h(a + 1, b, r - 1)
        frac_cont = (m - 1 - r - b) / m
        if frac_cont != 0:
            term += frac_cont * g(a + 1, b, r)
        return term

    @lru_cache(maxsize=None)
    def h(a, b, r):
        term = F(1, 1) / n
        if r >= 1:
            term += F(r, 1) / n * h(a, b + 1, r - 1)
        frac_cont = (n - 1 - a - b - r) / n
        if frac_cont != 0:
            term += frac_cont * g(a, b + 1, r)
        return term

    return g(F(0), F(0), K)


if __name__ == "__main__":
    for K in [1, 2, 3]:
        for n in range(K + 1, 9):
            mine = psi_markov(n, K)
            bf = psi_n_K(n, K, "generic")
            status = "OK" if mine == bf else "MISMATCH"
            print(f"K={K} n={n} markov={mine} brute={bf} {status}")
            sys.stdout.flush()
