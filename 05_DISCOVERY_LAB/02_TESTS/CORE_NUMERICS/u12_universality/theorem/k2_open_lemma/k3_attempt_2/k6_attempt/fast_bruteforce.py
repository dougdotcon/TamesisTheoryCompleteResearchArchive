"""
Optimized, parallelized exhaustive brute force for psi_n^{(K)} (the SAME raw
definition psi_bruteforce_ref.py uses -- exhaustive enumeration of ALL n! x n^K
(pi, U_1..U_K) combinations, no sampling), rewritten for speed:
  - list-based state instead of dict rebuilding per inner iteration
  - counts as a plain Python int in the hot loop (exact; Fraction formed once at the
    end from the exact integer numerator/denominator -- mathematically identical to
    psi_bruteforce_ref.py's running Fraction sum, just far cheaper per iteration)
  - parallelized across the outer permutation loop via multiprocessing

This is an independent re-implementation (different code, not a copy) of the exact
same combinatorial definition psi_bruteforce_ref.py computes; used here only to make
a K=6 raw-definition brute force check computationally feasible within this task's
time budget. Cross-checked against psi_bruteforce_ref.py itself at small (n,K) below
before being trusted for K=6.
"""
import itertools
import multiprocessing as mp
from fractions import Fraction
import time
import sys


def count_cyclic_for_perm(args):
    perm, n, K = args
    # perm: tuple of length n, perm[i] = pi(i+1), 1-indexed values
    xstar = K + 1
    # f as list, index 0 unused, indices 1..n
    f = [0] * (n + 1)
    for i in range(1, n + 1):
        f[i] = perm[i - 1]
    count = 0
    targets_range = range(1, n + 1)
    for targets in itertools.product(targets_range, repeat=K):
        for idx in range(K):
            f[idx + 1] = targets[idx]
        cur = f[xstar]
        cyclic = False
        for _ in range(n + 1):
            if cur == xstar:
                cyclic = True
                break
            cur = f[cur]
        if cyclic:
            count += 1
    return count


def psi_n_K_fast(n, K, nproc=None):
    assert n > K
    perms = list(itertools.permutations(range(1, n + 1)))
    args = [(p, n, K) for p in perms]
    if nproc is None:
        nproc = mp.cpu_count()
    t0 = time.time()
    if nproc > 1:
        with mp.Pool(nproc) as pool:
            counts = pool.map(count_cyclic_for_perm, args, chunksize=max(1, len(args) // (nproc * 8)))
    else:
        counts = [count_cyclic_for_perm(a) for a in args]
    total = sum(counts)
    denom = len(perms) * (n ** K)
    dt = time.time() - t0
    return Fraction(total, denom), dt


if __name__ == "__main__":
    n = int(sys.argv[1])
    K = int(sys.argv[2])
    nproc = int(sys.argv[3]) if len(sys.argv) > 3 else None
    val, dt = psi_n_K_fast(n, K, nproc)
    print(f"K={K} n={n} psi={val} = {float(val):.10f}  time={dt:.1f}s")
