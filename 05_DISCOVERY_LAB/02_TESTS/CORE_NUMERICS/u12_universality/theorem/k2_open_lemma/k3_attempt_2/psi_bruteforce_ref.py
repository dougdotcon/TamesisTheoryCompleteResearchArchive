"""
Self-contained copy of the exhaustive brute-force enumeration logic already used and
validated in ../psi_bruteforce.py (wave 5, K2-OPEN-LEMMA attempt) -- reproduced here
verbatim (not modified) so this K3-OPEN-LEMMA-ATTEMPT-2 directory is self-contained
and reproducible without a relative import into a sibling directory. Enumerates ALL
n! x n^K (pi, U_1,...,U_K) combinations exactly (fractions.Fraction), no sampling.
"""
import itertools
from fractions import Fraction
import time
import sys


def is_cyclic(f, n, start):
    cur = f[start]
    for _ in range(n + 1):
        if cur == start:
            return True
        cur = f[cur]
    return False


def psi_n_K(n, K, reference="generic"):
    """reference='generic': test point is K+1 (not rerouted).
    reference='rerouted': test point is 1 (one of the K rerouted sources)."""
    assert n > K
    xstar = K + 1 if reference == "generic" else 1
    total = Fraction(0)
    count = 0
    sources = list(range(1, K + 1))
    for perm in itertools.permutations(range(1, n + 1)):
        pi = {i + 1: perm[i] for i in range(n)}
        for targets in itertools.product(range(1, n + 1), repeat=K):
            f = dict(pi)
            for idx, s in enumerate(sources):
                f[s] = targets[idx]
            total += 1 if is_cyclic(f, n, xstar) else 0
            count += 1
    return total / count


if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ref = sys.argv[3] if len(sys.argv) > 3 else "generic"
    for n in range(K + 1, nmax + 1):
        t0 = time.time()
        val = psi_n_K(n, K, ref)
        dt = time.time() - t0
        print(f"K={K} n={n} ref={ref} psi={val} = {float(val):.8f}  time={dt:.1f}s")
        sys.stdout.flush()
