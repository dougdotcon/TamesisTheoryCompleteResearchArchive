"""
ADVERSARIAL, INDEPENDENT exhaustive brute-force enumeration of the raw Definition 1/4
model from THEOREM.md, written from scratch for this referee review of
k3_attempt_2/ATTEMPT.md. Deliberately coded differently from the front's
psi_bruteforce_ref.py / phi_bruteforce_full.py:

  - cyclic-point test uses a visited-SET early-stop walk (stops as soon as either the
    start point is revisited [cyclic] or any other previously-visited point is
    revisited [not cyclic]), not a fixed bounded loop of n+1 iterations.
  - success/total is accumulated as plain Python ints (fast) and converted to a single
    fractions.Fraction only at the very end, rather than accumulating a running
    Fraction every iteration.
  - permutations are represented as tuples (not dicts) with 0-indexed points internally
    (point i in the code = point i+1 in the paper's 1-indexed convention), sources are
    points 0..K-1, generic reference point is K, rerouted reference point is 0.

Model (THEOREM.md Definition 1/4): pi uniform random permutation of [n] (0-indexed
here), U_1..U_K i.i.d. uniform on [n], independent of pi and of each other,
f(i) = U_i for i < K (sources), f(i) = pi(i) otherwise.

Provides:
  psi_generic(n, K)   = P(point K is cyclic under f)      [[ψ_n^{(K)}]]
  psi_rerouted(n, K)  = P(point 0 is cyclic under f)       [[ψ_n^{(K),R}]]
  phi_raw(n, K)       = E[#cyclic points] / n, the RAW Definition-4 average over ALL n
                         points (does not use the generic/rerouted split or Lemma A at
                         all -- independent cross-check of the recombination).
"""
import itertools
import sys
import time
from fractions import Fraction


def is_cyclic_from(f, start):
    """f: tuple representing a function [n]->[n] (0-indexed). Returns True iff `start`
    lies on a cycle of f (i.e. following f from `start` returns to `start` before
    hitting any other repeated point)."""
    visited = {start}
    cur = f[start]
    while True:
        if cur == start:
            return True
        if cur in visited:
            return False
        visited.add(cur)
        cur = f[cur]


def _iter_f(n, K):
    """Yield every f as a tuple, built from every (pi, U_1..U_K) combination."""
    idx = list(range(n))
    for perm in itertools.permutations(idx):
        for targets in itertools.product(idx, repeat=K):
            f = list(perm)
            for s in range(K):
                f[s] = targets[s]
            yield tuple(f)


def psi_generic(n, K, verbose=False):
    assert n > K
    succ = 0
    total = 0
    t0 = time.time()
    for f in _iter_f(n, K):
        total += 1
        if is_cyclic_from(f, K):
            succ += 1
    if verbose:
        print(f"  psi_generic n={n} K={K}: {succ}/{total}  ({time.time()-t0:.1f}s)")
    return Fraction(succ, total)


def psi_rerouted(n, K, verbose=False):
    assert n > K
    succ = 0
    total = 0
    t0 = time.time()
    for f in _iter_f(n, K):
        total += 1
        if is_cyclic_from(f, 0):
            succ += 1
    if verbose:
        print(f"  psi_rerouted n={n} K={K}: {succ}/{total}  ({time.time()-t0:.1f}s)")
    return Fraction(succ, total)


def phi_raw(n, K, verbose=False):
    """The RAW Definition-4 average: E[#cyclic points among ALL n]/n. Does not call
    psi_generic/psi_rerouted or use Lemma A -- fully independent code path, exactly the
    kind of check the task asks for (item 6)."""
    assert n > K
    total_cyclic_count = 0
    total_configs = 0
    t0 = time.time()
    for f in _iter_f(n, K):
        total_configs += 1
        c = 0
        for x in range(n):
            if is_cyclic_from(f, x):
                c += 1
        total_cyclic_count += c
    if verbose:
        print(f"  phi_raw n={n} K={K}: sum(#cyclic)={total_cyclic_count} "
              f"configs={total_configs}  ({time.time()-t0:.1f}s)")
    return Fraction(total_cyclic_count, total_configs * n)


if __name__ == "__main__":
    # simple CLI: adv_bruteforce.py <mode> <K> <n>
    mode = sys.argv[1]
    K = int(sys.argv[2])
    n = int(sys.argv[3])
    if mode == "generic":
        print(psi_generic(n, K, verbose=True))
    elif mode == "rerouted":
        print(psi_rerouted(n, K, verbose=True))
    elif mode == "phi":
        print(phi_raw(n, K, verbose=True))
    else:
        raise SystemExit("mode must be generic|rerouted|phi")
