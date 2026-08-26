"""
Independent hostile referee check -- fresh exhaustive classification of the
destination-combinatorics maps at K=5 (6^5=7776 raw configs) and K=6
(7^6=117649, beyond the front's own mandate, matching the front's own K=6
spot-check but re-derived from scratch here).

INDEPENDENCE: fresh classification code, written from ATTEMPT.md's prose
description of the mechanism only (a point contributes new cyclic mass iff
its source lies on a cycle of g:{1..K}->{1..K}u{OUT}); no .py file of the
front or of any prior front/referee was read.
"""
import itertools
from math import comb, factorial
import sys

def classify(K):
    """Enumerate all (K+1)^K raw maps g:{1..K}->{1..K,OUT} (OUT encoded as 0).
    For each, find the on-cycle set C (nodes on a genuine cycle of g restricted
    to {1..K}), r=|C|, n_off=K-r. Return per-r raw counts, shape-type counts
    (distinct (r, cycle-type-of-g|_C) combos), and per-(r,n_off) 'off-raw-count'
    N(r,n_off) := number of raw off-cycle-target assignments for a FIXED on-cycle
    set/cycle-structure (should be constant across all choices, per the
    document's claim)."""
    targets = range(0, K + 1)  # 0 = OUT, 1..K = regions
    per_r_raw = [0] * (K + 1)
    shape_counts = {}  # key: (r, sorted tuple of cycle lengths) -> raw count
    total = 0
    for g in itertools.product(targets, repeat=K):
        # g[i-1] = target of source i (1..K); find on-cycle set among 1..K
        # via pointer-chasing with status marking (0=unvisited,1=in-progress,2=resolved-off,3=resolved-on)
        status = [0] * (K + 1)
        on_cycle = [False] * (K + 1)
        for start in range(1, K + 1):
            if status[start] != 0:
                continue
            chain = []
            cur = start
            while cur != 0 and status[cur] == 0:
                status[cur] = 1
                chain.append(cur)
                cur = g[cur - 1]
            if cur != 0 and status[cur] == 1:
                # found a cycle: the portion of chain from cur's first
                # occurrence onward is the cycle
                idx = chain.index(cur)
                cyc_nodes = chain[idx:]
                for n in cyc_nodes:
                    on_cycle[n] = True
                    status[n] = 3
                for n in chain[:idx]:
                    status[n] = 2
            else:
                for n in chain:
                    status[n] = 2
        C = [i for i in range(1, K + 1) if on_cycle[i]]
        r = len(C)
        per_r_raw[r] += 1
        total += 1
        # cycle type: lengths of the disjoint cycles of g restricted to C
        cyc_lengths = []
        seen = set()
        for node in C:
            if node in seen:
                continue
            cur = node
            length = 0
            while cur not in seen:
                seen.add(cur)
                length += 1
                cur = g[cur - 1]
            cyc_lengths.append(length)
        key = (r, tuple(sorted(cyc_lengths)))
        shape_counts[key] = shape_counts.get(key, 0) + 1
    return total, per_r_raw, shape_counts

def partition_count(n):
    """number of integer partitions of n, p(0)=1."""
    parts = [1] + [0] * n
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            parts[j] += parts[j - i]
    return parts

ALL_PASS = True
def check(name, cond):
    global ALL_PASS
    if not cond:
        ALL_PASS = False
    print(f"  {name}: {'PASS' if cond else 'FAIL'}")

for K, expected_raw in [(5, [1296, 2160, 2160, 1440, 600, 120]), (6, None)]:
    print("=" * 72)
    print(f"K={K}: enumerating all {(K+1)}^{K} = {(K+1)**K} raw maps (fresh classification)")
    print("=" * 72)
    total, per_r_raw, shape_counts = classify(K)
    check(f"total raw configs = {(K+1)**K}", total == (K + 1) ** K)
    print(f"  per-r raw counts: {per_r_raw}")
    if expected_raw is not None:
        check(f"per-r raw counts match front's pre-registered {expected_raw}",
              per_r_raw == expected_raw)
    n_shapes = len(shape_counts)
    p = partition_count(K)
    expected_shapes = sum(p[:K + 1])
    check(f"number of shape types = {n_shapes} vs sum_{{s<=K}} p(s) = {expected_shapes}",
          n_shapes == expected_shapes)

    # N(r, n_off) constancy: for each r, every specific cycle-type key at that r
    # should give the SAME raw count divided by (number of specific label/perm
    # realizations for that cycle type) -- i.e. N(r,n_off) := raw_count_for_this_(r,cycletype)
    # / [C(K,r) * (# permutations of r labeled items with this exact cycle type)]
    # must be identical for every cycle type at fixed r (this is the "off-cycle
    # raw count depends only on (r,n_off)" structural claim).
    from itertools import permutations as iperm
    def num_perms_of_cycle_type(cyc_lengths):
        # number of permutations of r labeled items with given cycle-length multiset
        r = sum(cyc_lengths)
        from collections import Counter
        cnt = Counter(cyc_lengths)
        denom = 1
        for length, mult in cnt.items():
            denom *= (length ** mult) * factorial(mult)
        return factorial(r) // denom

    N_by_r = {}
    consistent = True
    for (r, cyctype), raw_count in shape_counts.items():
        if r == 0:
            N = raw_count  # single "type" at r=0 (empty cycle set), n_off=K
        else:
            nperms = num_perms_of_cycle_type(cyctype)
            denom = comb(K, r) * nperms
            assert raw_count % denom == 0, (r, cyctype, raw_count, denom)
            N = raw_count // denom
        N_by_r.setdefault(r, set()).add(N)
        if len(N_by_r[r]) > 1:
            consistent = False
    check(f"N(r,n_off) constant across every specific on-set/cycle-type choice, all r=0..{K}",
          consistent)
    Ns = {r: list(v)[0] for r, v in N_by_r.items()}
    print(f"  N(r, n_off=K-r) values: {Ns}")
    # analytic cross-check: N(r,n_off) should equal the labeled-forest count
    # (r+1)*(r+1+n_off)^(n_off-1) for n_off>=1, and 1 for n_off=0 (r=K).
    forest_ok = True
    for r, N in Ns.items():
        n_off = K - r
        if n_off == 0:
            expected_N = 1
        else:
            expected_N = (r + 1) * (r + 1 + n_off) ** (n_off - 1)
        if N != expected_N:
            forest_ok = False
            print(f"    MISMATCH at r={r}: N={N} vs forest formula {expected_N}")
    check(f"N(r,n_off) matches the labeled-forest count (r+1)(r+1+n_off)^(n_off-1)",
          forest_ok)

    # cross-foot: sum_r C(K,r) r! N(r,K-r) == (K+1)^K
    crossfoot = sum(comb(K, r) * factorial(r) * Ns[r] for r in range(K + 1))
    check(f"cross-foot sum_r C(K,r) r! N(r,K-r) = {crossfoot} vs {(K+1)**K}",
          crossfoot == (K + 1) ** K)
    print()

print("=" * 72)
print(f"OVERALL: {'ALL PASS' if ALL_PASS else 'SOME FAILED'}")
print("=" * 72)
sys.exit(0 if ALL_PASS else 1)
