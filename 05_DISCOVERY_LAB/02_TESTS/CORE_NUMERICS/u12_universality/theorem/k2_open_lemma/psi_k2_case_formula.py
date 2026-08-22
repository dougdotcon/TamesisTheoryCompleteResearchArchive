"""
Exact evaluation of psi_n^{(2)} via the hand-derived exploration/coupling CASE ANALYSIS
of ATTEMPT.md SS4 (three cases: neither / exactly one / both of the K=2 sources lie on
x*'s own pi-cycle C_0), as opposed to exhaustive enumeration (psi_bruteforce.py).

This script implements the case formulas directly (not the closed form obtained after
symbolic summation in derive_closed_forms.py) and is the primary cross-check that the
CASE ANALYSIS ITSELF (not just its final summed closed form) is correct: every value
below is checked to agree exactly with psi_bruteforce.py's exhaustive enumeration for
n=3..8 (see k2_open_lemma.log).

Recap of the three cases, given x*'s pi-cycle length L (P(L=l)=1/n exactly, standard):
  (a) neither source 1 nor source 2 lies on C_0: contributes success probability 1.
  (b) exactly one source lies on C_0, at position d in {1,...,L-1} (the other source
      lies somewhere among the other n-L points, entirely unconstrained): contributes
          P_b(L,d) = (L-d)(3n-L+1) / (2n^2)
  (c) both sources lie on C_0, at positions p<q in {1,...,L-1}: contributes
          P_c(L,p,q) = (L-q)(n+q-p) / n^2
Weights come from the classical fact that, given L=l, the other l-1 members of C_0 are
a uniform (l-1)-subset of the other n-1 points of [n], in a uniform cyclic order.
"""
from fractions import Fraction as F
import itertools
import sys


def psi_k2_case_formula(n):
    total = F(0)
    for L in range(1, n + 1):
        m = L - 1
        if n < 2:
            continue
        # (a) neither source on C_0
        p_neither = F((n - 1 - m) * (n - 2 - m), (n - 1) * (n - 2))
        total += F(1, n) * p_neither * F(1)

        # (b) exactly one source on C_0 (times 2 for symmetry: "1 on/2 off" or "2 on/1 off")
        if m >= 1:
            p_one = F(m * (n - 1 - m), (n - 1) * (n - 2))
            s = sum(F((L - d) * (3 * n - L + 1), 2 * n * n) for d in range(1, m + 1))
            e_b = s / m
            total += F(1, n) * 2 * p_one * e_b

        # (c) both sources on C_0
        if m >= 2:
            p_both = F(m * (m - 1), (n - 1) * (n - 2))
            pairs = list(itertools.combinations(range(1, m + 1), 2))
            s = sum(F((L - q) * (n + q - p), n * n) for (p, q) in pairs)
            e_c = s / len(pairs)
            total += F(1, n) * p_both * e_c

    return total


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    for n in range(3, nmax + 1):
        print(n, psi_k2_case_formula(n), float(psi_k2_case_formula(n)))
