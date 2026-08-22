"""
Exact brute-force computation of psi_n^{(K)} and psi_n^{(K),R}, the two "component"
quantities that the Reduction Lemma of ATTEMPT.md decomposes phi_n^{(K)} (Definition 4
of THEOREM.md) into:

  psi_n^{(K)}   := P( a fixed point NOT among the K rerouted sources is cyclic )
  psi_n^{(K),R} := P( a fixed point THAT IS one of the K rerouted sources is cyclic )

Model, matching Definition 1 / Definition 4 of THEOREM.md, conditioned on the K
rerouted sources being exactly {1,...,K} (WLOG by exchangeability): pi a uniform
permutation of [n]; U_1,...,U_K i.i.d. uniform on [n], independent of pi; f(i)=U_i for
i<=K, f(i)=pi(i) otherwise. Exhaustive enumeration over all n! permutations x n^K
reroute-target tuples, exact rational arithmetic (fractions.Fraction).

phi_n^{(K)} = (K/n) psi_n^{(K),R} + (1 - K/n) psi_n^{(K)}   -- exact identity, checked
in derive_closed_forms.py against THEOREM.md's own phi_n^{(2)} table.
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
    # Usage: python3 psi_bruteforce.py K nmax reference
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ref = sys.argv[3] if len(sys.argv) > 3 else "generic"
    for n in range(K + 1, nmax + 1):
        t0 = time.time()
        val = psi_n_K(n, K, ref)
        dt = time.time() - t0
        print(f"K={K} n={n} ref={ref} psi={val} = {float(val):.8f}  time={dt:.1f}s")
        sys.stdout.flush()
