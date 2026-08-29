"""
K5-EXACT-CLOSURE-ATTEMPT.

Fresh, independent, fully-exhaustive brute-force implementation of
THEOREM.md Definition 4 (the u12 permutation-with-reroutes ensemble),
general K, used here at K=5. Written from scratch from Definition 4's
own prose (THEOREM.md lines 859-872) -- no code imported from any
ancestor front.

Model: n points labelled 0..n-1. K reroute sources fixed WLOG at
{0,...,K-1} (exchangeability, standard and unquestioned in this
lineage -- we still enumerate ALL n! permutations pi and ALL n^K target
tuples U, not a reduced model, so this is a genuine ground truth,
independent of any "arc decomposition"/Lemma-1-style theory).

f(i) := U_i        if i < K (i is a source)
f(i) := pi(i)       otherwise

T := #{cyclic points of f} := #{i : iterating f from i returns to i}.
(M_n^{(K)} = T/n, not used directly here -- we report the exact
distribution of T.)

Cyclic-point counting on a general functional graph (each node has
out-degree exactly 1, since f is a total function [n]->[n], not
necessarily a bijection because U_i need not avoid collisions): use the
standard O(n) "rho-shaped graph" algorithm -- follow f from each
unvisited node, colour nodes IN_PROGRESS while on the current walk,
DONE once resolved; when the walk revisits an IN_PROGRESS node, the
newly-closed loop is exactly the cyclic points found on this walk.

Outputs, for each n tested: exact (Fraction) P(T<=k) for every
k=0,...,n, from an exhaustive enumeration of all n!*n^K (pi,U) pairs.
"""
import sys
from fractions import Fraction
from itertools import permutations, product
from math import factorial
import time


def count_cyclic_points(f, n):
    """f: list of length n, f[i] in [0,n). Returns #cyclic points."""
    color = [0] * n  # 0=unvisited,1=in progress,2=done
    order = [0] * n  # position of node within current walk (for cycle extraction)
    cyclic_count = 0
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        v = start
        while color[v] == 0:
            color[v] = 1
            order[v] = len(path)
            path.append(v)
            v = f[v]
        if color[v] == 1:
            # v is on the current path -> path[order[v]:] is a genuine cycle
            cyclic_count += len(path) - order[v]
        # mark all as done
        for u in path:
            color[u] = 2
    return cyclic_count


def exact_T_distribution(n, K):
    """Returns dict k -> Fraction count / (n! * n^K) style: actually
    returns (counts: list length n+1 of ints, total: int) so caller can
    build exact Fractions without repeated GCD overhead."""
    assert 0 <= K <= n
    counts = [0] * (n + 1)
    total = 0
    base = list(range(K, n))  # non-source labels, to be permuted
    # iterate over all permutations of the FULL [0,n) (K sources' pi-images
    # matter too, even though they'll be overridden at those K positions for
    # f -- pi itself must still be a genuine bijection of all n points, and
    # its restriction to non-source domain positions, plus where it SENDS
    # the K source positions under pi, all affect pi's role as substrate).
    #
    # Actually: since f(i)=pi(i) is used only for i>=K, and pi is a
    # bijection of the FULL domain [0,n), pi(i) for i<K plays NO role in f
    # at all (it's overridden). But pi must still be a bijection overall,
    # so which VALUES land in the image "under" the K source domain
    # positions still constrains which values remain available for the
    # non-source domain positions' images. We do this correctly and
    # honestly by enumerating full permutations of [0,n) (all n! of them),
    # not a shortcut -- this is deliberately the expensive, fully faithful
    # version.
    for pi in permutations(range(n)):
        for U in product(range(n), repeat=K):
            f = list(pi)
            for i in range(K):
                f[i] = U[i]
            T = count_cyclic_points(f, n)
            counts[T] += 1
            total += 1
    return counts, total


def cdf_from_counts(counts, total):
    cum = 0
    out = []
    for k in range(len(counts)):
        cum += counts[k]
        out.append(Fraction(cum, total))
    return out


if __name__ == "__main__":
    K = 5
    for n in [5, 6]:
        t0 = time.time()
        counts, total = exact_T_distribution(n, K)
        elapsed = time.time() - t0
        expected_total = factorial(n) * n**K
        assert total == expected_total, (total, expected_total)
        cdf = cdf_from_counts(counts, total)
        print(f"n={n} K={K}  total configs={total}  elapsed={elapsed:.1f}s")
        print(f"  counts (T=0..{n}): {counts}")
        print(f"  P(T<=k) for k=0..{n}:")
        for k, val in enumerate(cdf):
            print(f"    k={k}: {val} = {float(val):.10f}")
        sys.stdout.flush()
    print("DONE.")
