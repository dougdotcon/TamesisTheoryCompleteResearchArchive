"""K=1 cross-check: P_nn(n,1) with source and query strictly disjoint,
to disambiguate against the two different K=1 formulas appearing in the
archive (distributional_bridge_attempt's P_nn(n,1)=1/2+1/(6n) [source and
query disjoint, matching Lemma P2's P_nn convention] vs
joint_exploration_continuum_attempt's Proposition K1 P_n^{(1)}(both) =
(3n^2-n+2)/(6n^2) [query points 0,1, R uniform over ALL of [n], can equal
a query point]). Fresh brute force, not reading either front's code."""
from fractions import Fraction
from itertools import permutations
import sys


def cyclic_points(f, n):
    cyclic = set()
    color = [0] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = f[x]
        if color[x] == 1:
            idx = path.index(x)
            for y in path[idx:]:
                cyclic.add(y)
        for y in path:
            color[y] = 2
    return cyclic


def run_disjoint(n):
    """source at {0}, query at {n-2,n-1} -- strictly disjoint (P_nn convention)."""
    q1, q2 = n - 2, n - 1
    total = 0
    both = 0
    for pi in permutations(range(n)):
        for u0 in range(n):
            f = list(pi)
            f[0] = u0
            cyc = cyclic_points(f, n)
            total += 1
            if q1 in cyc and q2 in cyc:
                both += 1
    return Fraction(both, total)


def run_overlap_allowed(n):
    """query points fixed at {0,1}; source R={r} uniform over ALL of [n]
    (can equal 0 or 1) -- Proposition K1's convention."""
    q1, q2 = 0, 1
    total = 0
    both = 0
    for pi in permutations(range(n)):
        for r in range(n):
            for u in range(n):
                f = list(pi)
                f[r] = u
                cyc = cyclic_points(f, n)
                total += 1
                if q1 in cyc and q2 in cyc:
                    both += 1
    return Fraction(both, total)


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [3, 4, 5]
    for n in ns:
        pd = run_disjoint(n)
        pred_pnn = Fraction(1, 2) + Fraction(1, 6 * n)
        po = run_overlap_allowed(n)
        pred_k1 = Fraction(3 * n * n - n + 2, 6 * n * n)
        print(f"n={n}: disjoint-source P_nn(n,1)={pd} vs predicted(1/2+1/6n)={pred_pnn} "
              f"[{'OK' if pd==pred_pnn else 'MISMATCH'}]   "
              f"overlap-allowed P_n^(1)(both)={po} vs PropK1={pred_k1} "
              f"[{'OK' if po==pred_k1 else 'MISMATCH'}]")
