"""
Independent brute-force check of phi_n^{(K)} ITSELF (Definition 4 of THEOREM.md: the
full average of #cyclic/n over ALL n points, conditioned on sources={1,...,K}) --
deliberately NOT built from psi_bruteforce_ref.py's single-reference-point machinery
(different code path, same underlying model), as the strongest available cross-check
on the Lemma-A recombination phi_n^{(K)} = (K/n) psi_n^{(K),R} + (1-K/n) psi_n^{(K)}
computed by markov_transfer.py's phi_closed_form(K).
"""
import itertools
from fractions import Fraction
import sys
import time


def is_cyclic(f, n, start):
    cur = f[start]
    for _ in range(n + 1):
        if cur == start:
            return True
        cur = f[cur]
    return False


def phi_n_K(n, K):
    assert n > K
    sources = list(range(1, K + 1))
    total = Fraction(0)
    count = 0
    for perm in itertools.permutations(range(1, n + 1)):
        pi = {i + 1: perm[i] for i in range(n)}
        for targets in itertools.product(range(1, n + 1), repeat=K):
            f = dict(pi)
            for idx, s in enumerate(sources):
                f[s] = targets[idx]
            ncyc = sum(1 for x in range(1, n + 1) if is_cyclic(f, n, x))
            total += Fraction(ncyc, n)
            count += 1
    return total / count


if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    for n in range(K + 1, nmax + 1):
        t0 = time.time()
        v = phi_n_K(n, K)
        print(f"K={K} n={n} phi={v} = {float(v):.8f} time={time.time()-t0:.1f}s")
        sys.stdout.flush()
