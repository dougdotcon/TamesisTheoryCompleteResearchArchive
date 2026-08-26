"""
assemble_pnn3.py

Assembles P_nn(n,3) from the reduced redirect model (redirect_core_k3.py),
by summing over all compositions (L0,L1,L2,O) of n into 4 positive/
nonnegative parts (L_s>=1, O>=0) -- the K=3 analogue of Proposition NN2's
own T(p,q) assembly (predecessor ATTEMPT.md Sec 4), generalized from 2 arcs
to 3.

T(L0,L1,L2) := sum over all ORDERED pairs of distinct "roles" (among the
n-3 non-source slots: interior arc positions or outside) of
P(both roles cyclic | L). Exact fractions.Fraction throughout.

P_nn(n,3) = [1/C(n,3)] * sum_{compositions (L0,L1,L2,O)} T(L0,L1,L2) /
            [(n-3)(n-4)]

-- matching exactly the predecessor's own K=2 assembly logic (its own
Sec 4), generalized: C(n,3) compositions (Lemma 1 at m=3, cited), and
(n-3)(n-4) the number of ordered ways to place 2 distinct query points
among the n-3 non-source slots (the m=3 analogue of the K=2 "(n-2)(n-3)").
"""

import sys
from fractions import Fraction
from itertools import combinations_with_replacement

from redirect_core_k3 import p_single_cyclic, p_joint_cyclic


def T_of_L(n, L):
    O = n - sum(L)
    total = Fraction(0)

    # OO
    if O >= 2:
        total += O * (O - 1) * Fraction(1)

    # O-arc (both orders): 2 * O * sum_s sum_k p_single(s,k)
    if O >= 1:
        s_sum = Fraction(0)
        for s in range(3):
            for k in range(1, L[s]):
                s_sum += p_single_cyclic(n, L, s, k)
        total += 2 * O * s_sum

    # same-arc pairs (both orders). Uses the verified "monotone" fact
    # (checked computationally, see redirect_direct_check_k3.py output and
    # the smoke test in redirect_core_k3.py): for k<k' in the same arc,
    # P(both cyclic) = P(k cyclic) -- the nearer-to-tail point's own
    # marginal, exactly generalizing Lemma 2's (R3). This turns an O(L^2)
    # loop into O(L).
    for s in range(3):
        Ls = L[s]
        for k in range(1, Ls):
            single = p_single_cyclic(n, L, s, k)
            count_kp_greater = (Ls - 1) - k  # number of k' > k, k' in 1..Ls-1
            if count_kp_greater > 0:
                total += 2 * count_kp_greater * single

    # cross-arc pairs (both orders, s<s' covers each unordered pair once,
    # *2 handles both orderings)
    for s in range(3):
        for sp in range(s + 1, 3):
            for k in range(1, L[s]):
                for kp in range(1, L[sp]):
                    val = p_joint_cyclic(n, L, (s, k), (sp, kp))
                    total += 2 * val

    return total


def all_compositions(n):
    """All (L0,L1,L2) with L_s>=1, sum(L)<=n (O=n-sum>=0)."""
    result = []
    for L0 in range(1, n - 1):
        for L1 in range(1, n - L0):
            for L2 in range(1, n - L0 - L1 + 1):
                if L0 + L1 + L2 <= n:
                    result.append((L0, L1, L2))
    return result


def C(n, k):
    from math import comb
    return comb(n, k)


def p_nn_3_reduced(n, verbose=False):
    comps = all_compositions(n)
    assert len(comps) == C(n, 3), (len(comps), C(n, 3))
    total = Fraction(0)
    for L in comps:
        t = T_of_L(n, L)
        total += t
    P = total / (C(n, 3) * (n - 3) * (n - 4))
    if verbose:
        print(f"  n={n}: {len(comps)} compositions summed", file=sys.stderr)
    return P


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [6, 7, 8]
    for n in ns:
        P = p_nn_3_reduced(n, verbose=True)
        print(f"n={n}: P_nn(n,3) [reduced model] = {P} = {float(P):.10f}")
