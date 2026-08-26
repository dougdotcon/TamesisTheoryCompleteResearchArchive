"""
Brute-force check of the "Marked-Point Gap Structure Lemma" (this front's
own generalization of THEOREM.md Proposition 4 Step 1 / L~Uniform{1..n}):

For a uniform random permutation pi of [n] and m distinguished points, the
"contracted permutation" on the m marked points (follow pi forward from
each marked point until the next marked point) is a UNIFORM random
permutation of the m marked points (m! outcomes), and -- independently of
which topology occurs -- the m gap sizes (# unmarked points strictly
between a marked point and the next marked point on its own cycle),
together with an "outside" count (points in cycles containing no marked
point at all), form a composition of n-m into m+1 nonnegative parts that
is UNIFORM over all C(n,m) such compositions.

This script checks both claims by exhaustive enumeration for m=2 (n up to
7) and m=3 (n up to 7), exact counts (no sampling).
"""
from itertools import permutations
from fractions import Fraction


def contracted_and_gaps(pi, marks):
    n = len(pi)
    mark_set = set(marks)
    # for each mark, walk forward counting unmarked points until next mark
    gaps = {}
    nxt = {}
    for m in marks:
        x = pi[m]
        cnt = 0
        while x not in mark_set:
            cnt += 1
            x = pi[x]
        gaps[m] = cnt
        nxt[m] = x
    # outside count = n - m - sum(gaps)  [m marks + gap-fillers = accounted,
    # rest is "outside"]
    outside = n - len(marks) - sum(gaps.values())
    return nxt, gaps, outside


def run(n, marks):
    total = 0
    topo_counts = {}
    gap_counts = {}
    for pi_tuple in permutations(range(n)):
        pi = list(pi_tuple)
        nxt, gaps, outside = contracted_and_gaps(pi, marks)
        total += 1
        # topology: represent as tuple of (mark -> next mark) sorted
        topo_key = tuple(sorted(nxt.items()))
        topo_counts[topo_key] = topo_counts.get(topo_key, 0) + 1
        gap_key = tuple(gaps[m] for m in marks) + (outside,)
        gap_counts[gap_key] = gap_counts.get(gap_key, 0) + 1
    return total, topo_counts, gap_counts


def check(n, marks):
    m = len(marks)
    total, topo_counts, gap_counts = run(n, marks)
    import math
    n_topologies = math.factorial(m)
    pred_topo_count = total // n_topologies if total % n_topologies == 0 else None
    topo_ok = (len(topo_counts) == n_topologies and
               all(c == total / n_topologies for c in topo_counts.values()))

    # number of compositions of n-m into m+1 nonneg parts = C(n,m)
    n_comps = math.comb(n, m)
    gap_ok = (len(gap_counts) == n_comps and
              all(abs(c - total / n_comps) < 1e-9 for c in gap_counts.values()))

    print(f"n={n} m={m} marks={marks}: total={total} "
          f"topologies_seen={len(topo_counts)}/{n_topologies} uniform={topo_ok}  "
          f"gap_compositions_seen={len(gap_counts)}/{n_comps} uniform={gap_ok}")
    return topo_ok and gap_ok


if __name__ == "__main__":
    all_ok = True
    for n in range(2, 8):
        ok = check(n, [0, 1])
        all_ok = all_ok and ok
    for n in range(3, 8):
        ok = check(n, [0, 1, 2])
        all_ok = all_ok and ok
    print()
    print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")
