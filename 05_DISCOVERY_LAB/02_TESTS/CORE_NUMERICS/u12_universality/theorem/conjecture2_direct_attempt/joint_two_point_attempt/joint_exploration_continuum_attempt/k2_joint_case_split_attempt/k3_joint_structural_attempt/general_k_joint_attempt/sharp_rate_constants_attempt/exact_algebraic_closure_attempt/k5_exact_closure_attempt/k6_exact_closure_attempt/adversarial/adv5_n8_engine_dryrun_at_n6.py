"""
K6-EXACT-CLOSURE-ATTEMPT.

Bonus fifth-scale (relative to the guaranteed n=6,7 checks) exhaustive
brute-force cross-check of Proposicao D6 against Definition 4, at n=8,
K=6 -- the domain-adjacent data point (the claimed exact-closure domain
starts at n=8 for K=6, following the K+2 pattern established at
K=2,3,4,5; verified separately, not assumed, in k6_exact_closure.py).

n=8, K=6: total configurations = 8! * 8^6 = 40320 * 262144 =
10,569,646,080 (~10.57 billion) -- about 8x the K=5 predecessor's own
n=8 bonus check (1,321,205,760 configurations, ~31 minutes single
process there). Sequential single-process throughput in this
environment for K=6 was measured at ~820,000-850,000 configs/s
(n=6,7 runs, bruteforce_definition4_k6.py) -- at that rate, n=8 alone
would take roughly 3.5 hours single-process. This script instead
parallelizes across all available CPU cores (multiprocessing.Pool) to
bring this into a feasible wall-clock window, WITHOUT changing the
underlying enumeration in any way (still every single one of the
10.57 billion (pi, U) pairs, no reduced/decomposition-model shortcut,
no importance sampling) -- only the outer loop over permutations pi is
split into contiguous chunks and distributed across worker processes;
each worker still performs the identical exhaustive inner n^6-tuple
enumeration and identical O(n) cycle-counting per configuration as the
single-process engine in bruteforce_definition4_k6.py (written
independently here, not imported, but mathematically the same
Definition-4 model).

Honesty discipline (matching this lineage's own convention, most
recently the K=5 predecessor's own n=8 bonus-check disclosure): if this
job does not complete within the time actually available in this
session, that is reported plainly, with however much progress was made,
rather than silently omitted or extrapolated.
"""
import sys
import time
import multiprocessing as mp
from itertools import permutations, product
from math import factorial

K = 6
N = 6  # REFEREE dry-run patch: temporarily set to 6 to validate the multiprocessing engine cheaply (the target's own file manifest claims this was done but left no log)


def count_cyclic_points(f, n):
    color = [0] * n
    depth = [0] * n
    cyclic = 0
    for start in range(n):
        if color[start]:
            continue
        walk = []
        v = start
        while color[v] == 0:
            color[v] = 1
            depth[v] = len(walk)
            walk.append(v)
            v = f[v]
        if color[v] == 1:
            cyclic += len(walk) - depth[v]
        for u in walk:
            color[u] = 2
    return cyclic


def process_chunk(chunk):
    """chunk: list of permutation tuples (length N). Returns counts
    list of length N+1 (T=0..N) accumulated over this chunk's full
    n^K target-tuple enumeration for every pi in chunk."""
    n = N
    counts = [0] * (n + 1)
    U_tuples = list(product(range(n), repeat=K))
    for pi in chunk:
        pi = list(pi)
        for U in U_tuples:
            f = pi[:]
            for i in range(K):
                f[i] = U[i]
            T = count_cyclic_points(f, n)
            counts[T] += 1
    return counts


def main():
    t_start = time.time()
    n = N
    all_perms = list(permutations(range(n)))
    total_perms = len(all_perms)
    assert total_perms == factorial(n)

    num_workers = mp.cpu_count()
    # fine-grained chunks for progress visibility: aim for roughly
    # 8 chunks per worker
    num_chunks = max(num_workers * 8, 1)
    chunk_size = (total_perms + num_chunks - 1) // num_chunks
    chunks = [all_perms[i:i + chunk_size] for i in range(0, total_perms, chunk_size)]
    print(f"n={n} K={K}  total permutations={total_perms}  "
          f"n^K={n**K}  total configs={total_perms * n**K}")
    print(f"num_workers={num_workers}  num_chunks={len(chunks)}  "
          f"chunk_size~={chunk_size}")
    sys.stdout.flush()

    counts = [0] * (n + 1)
    done_perms = 0
    with mp.Pool(processes=num_workers) as pool:
        for i, chunk_counts in enumerate(pool.imap_unordered(process_chunk, chunks)):
            for t_, c in enumerate(chunk_counts):
                counts[t_] += c
            done_perms += sum(chunk_counts) // (n ** K)
            elapsed = time.time() - t_start
            done_configs = done_perms * n ** K
            rate = done_configs / elapsed if elapsed > 0 else 0.0
            frac = done_perms / total_perms
            eta = (total_perms - done_perms) / (done_perms / elapsed) if done_perms > 0 else float('inf')
            print(f"  chunk {i+1}/{len(chunks)} done: {done_perms}/{total_perms} "
                  f"perms ({100*frac:.1f}%), {elapsed:.0f}s elapsed, "
                  f"{rate:.0f} cfg/s, ETA {eta:.0f}s", flush=True)

    total_elapsed = time.time() - t_start
    total_configs = sum(counts)
    expected_total = factorial(n) * n ** K
    assert total_configs == expected_total, (total_configs, expected_total)
    print(f"\nDONE. n={n} K={K}  total configs={total_configs}  "
          f"elapsed={total_elapsed:.1f}s  rate={total_configs/total_elapsed:.0f} cfg/s")
    print("counts (T=0..%d):" % n, counts)

    from fractions import Fraction
    cum = 0
    cdf = []
    for c in counts:
        cum += c
        cdf.append(Fraction(cum, total_configs))
    print("\nP(T<=k) for k=0..%d:" % n)
    for kk, val in enumerate(cdf):
        print(f"  k={kk}: {val} = {float(val):.14f}")

    print("\nCross-check against Proposicao D6 (see d6_predicted in "
          "bruteforce_definition4_k6.py) is performed separately by "
          "n8_crosscheck_k6.py, reading this script's own printed counts.")


if __name__ == "__main__":
    main()
