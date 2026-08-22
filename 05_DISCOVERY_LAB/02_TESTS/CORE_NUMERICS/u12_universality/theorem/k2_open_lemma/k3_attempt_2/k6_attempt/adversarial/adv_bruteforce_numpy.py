"""
PART A, item 2 (adversarial referee, k6_attempt).

Independent, from-scratch brute force for psi_n^{(K)} at K=6, using a
DIFFERENT optimization strategy from the front's fast_bruteforce.py: instead
of looping over itertools.product(targets, repeat=K) per permutation with a
Python-level walk simulation and multiprocessing over permutations, this
script vectorizes over the ENTIRE U-tuple space at once (numpy), simulating
the walk for all n^K reroute-tuples simultaneously for each of the n!
permutations, using a visited-set array and early stopping per row (not a
bounded n+1 step re-walk of the whole path every time, and no
itertools.product/Fraction in the hot loop at all).

Raw definition (THEOREM.md Definition 4, identical to psi_bruteforce_ref.py /
fast_bruteforce.py): pi a permutation of {0,...,n-1} (0-indexed here), sources
= {0,...,K-1}, reference (generic) point x* = K. f(i) = U_i for i in sources,
f(i) = pi(i) otherwise. psi_n^{(K)} = P(x* is cyclic under f), averaged over
uniform pi and uniform iid U_1..U_K.

Exact (integer) counting throughout -- final ratio formed once via Python's
Fraction from exact int numerator/denominator, exactly mirroring the
"integer counts, Fraction formed once at the end" discipline the front itself
uses (independently re-derived here as a natural choice, not copied).
"""
import sys
import time
import itertools
import numpy as np
import math
from fractions import Fraction as F


def count_cyclic_numpy(n, K):
    xstar = K
    sources = K  # source indices are 0..K-1
    N = n ** K  # size of the U-tuple space

    # Build the U-tuple table once: U_arr[j, s] = value of U_s for the j-th
    # U-tuple (lexicographic base-n encoding), s=0..K-1.
    U_arr = np.empty((N, K), dtype=np.int32)
    idx = np.arange(N, dtype=np.int64)
    tmp = idx.copy()
    for s in range(K - 1, -1, -1):
        U_arr[:, s] = tmp % n
        tmp //= n
    # sanity: after loop tmp should be all zeros
    assert np.all(tmp == 0)

    row_idx = np.arange(N)
    total_success = 0

    perms = itertools.permutations(range(n))
    nperm = 0
    for perm in perms:
        nperm += 1
        perm_arr = np.array(perm, dtype=np.int32)  # perm_arr[i] = pi(i)

        state = np.full(N, xstar, dtype=np.int32)
        visited = np.zeros((N, n), dtype=bool)
        visited[:, xstar] = True
        outcome = np.full(N, -1, dtype=np.int8)  # -1 unresolved, 1 success, 0 fail

        for _step in range(n + 2):
            unresolved = (outcome == -1)
            if not unresolved.any():
                break
            cur = state
            # non-source branch: pi(cur)
            next_nonsource = perm_arr[cur]
            # source branch: U_arr[row, cur] -- only meaningful where cur < K
            cur_clamped = np.minimum(cur, K - 1)
            next_source = U_arr[row_idx, cur_clamped]
            is_source = cur < sources
            nxt = np.where(is_source, next_source, next_nonsource)

            success = unresolved & (nxt == xstar)
            outcome[success] = 1

            already_visited = visited[row_idx, nxt]
            fail = unresolved & (~success) & already_visited
            outcome[fail] = 0

            cont = unresolved & (~success) & (~fail)
            # advance state and mark visited only for continuing rows
            state = np.where(cont, nxt, state)
            visited[row_idx[cont], nxt[cont]] = True

        assert np.all(outcome != -1), "some rows failed to resolve within n+2 steps"
        total_success += int(outcome.sum())  # outcome is 0/1, sum = success count

    denom_perms = nperm
    assert denom_perms == math.factorial(n)
    total_combos = denom_perms * N
    return total_success, total_combos


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    t0 = time.time()
    succ, denom = count_cyclic_numpy(n, K)
    dt = time.time() - t0
    frac = F(succ, denom)
    print(f"K={K} n={n}  successes={succ}  total_combos={denom}  psi={frac} = {float(frac):.10f}  time={dt:.1f}s")
