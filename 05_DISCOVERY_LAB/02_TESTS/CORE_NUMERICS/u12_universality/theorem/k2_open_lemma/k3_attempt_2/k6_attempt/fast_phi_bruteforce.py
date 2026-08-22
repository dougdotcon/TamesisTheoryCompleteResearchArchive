"""
Optimized, parallelized brute force for phi_n^{(K)} itself (Definition 4: full average
of #cyclic/n over ALL n reference points), the SAME quantity phi_bruteforce_full.py
computes -- independent re-implementation for speed (array state, int counts, no
Fraction in the hot loop, multiprocessing across permutations), used to make a K=6
check of the Lemma-A recombination feasible within this task's time budget.
"""
import itertools
import multiprocessing as mp
from fractions import Fraction
import time
import sys


def sum_cyclic_for_perm(args):
    perm, n, K = args
    f = [0] * (n + 1)
    for i in range(1, n + 1):
        f[i] = perm[i - 1]
    total_ncyc = 0
    targets_range = range(1, n + 1)
    for targets in itertools.product(targets_range, repeat=K):
        for idx in range(K):
            f[idx + 1] = targets[idx]
        ncyc = 0
        for x in range(1, n + 1):
            cur = f[x]
            for _ in range(n + 1):
                if cur == x:
                    ncyc += 1
                    break
                cur = f[cur]
        total_ncyc += ncyc
    return total_ncyc


def phi_n_K_fast(n, K, nproc=None):
    assert n > K
    perms = list(itertools.permutations(range(1, n + 1)))
    args = [(p, n, K) for p in perms]
    if nproc is None:
        nproc = mp.cpu_count()
    t0 = time.time()
    with mp.Pool(nproc) as pool:
        sums = pool.map(sum_cyclic_for_perm, args, chunksize=max(1, len(args) // (nproc * 8)))
    total_ncyc = sum(sums)
    num_combos = len(perms) * (n ** K)
    dt = time.time() - t0
    # phi = average of (ncyc/n) over all combos = total_ncyc / (n * num_combos)
    return Fraction(total_ncyc, n * num_combos), dt


if __name__ == "__main__":
    n = int(sys.argv[1])
    K = int(sys.argv[2])
    nproc = int(sys.argv[3]) if len(sys.argv) > 3 else None
    val, dt = phi_n_K_fast(n, K, nproc)
    print(f"K={K} n={n} phi={val} = {float(val):.10f}  time={dt:.1f}s")
