#!/usr/bin/env python3
"""
Adversarial referee -- own exhaustive classification of raw destination maps
g: {1..K} -> {1..K, OUT}, for K=5 (6^5=7776) and K=6 (7^6=117649).
Fresh cycle-detection code, built only from the prose definitions.

Checks (pre-registered in the front's prereg; re-verified independently):
  * per-r_on raw counts (K=5: 1296,2160,2160,1440,600,120; sum 7776)
  * number of (r_on, cycle-type) shape types = sum_{s<=K} p(s) (19 at K=5, 30 at K=6)
  * N(r, n_off) -- raw off-config count for a FIXED on-part (C, sigma) -- is
    constant across every specific (C, sigma) and equals the labeled-forest
    count (r+1)*(r+1+n_off)^(n_off-1)
  * cross-foot: sum_r binom(K,r) r! N(r,K-r) = (K+1)^K
"""
import itertools, math, sys
from collections import Counter, defaultdict

def cycle_nodes(g, K):
    """Nodes of {0..K-1} on cycles of g; g[i] in {0..K-1} or -1 (OUT)."""
    on = set()
    for start in range(K):
        seen = {}
        x, t = start, 0
        while x != -1 and x not in seen:
            seen[x] = t
            x = g[x]; t += 1
        if x != -1:  # closed a cycle at node x
            # nodes from seen[x] onward are on the cycle
            for node, tm in seen.items():
                if tm >= seen[x]:
                    on.add(node)
    return on

def cycle_type(g, C):
    """Sorted tuple of cycle lengths of g restricted to C (a permutation)."""
    C = set(C); lens = []
    left = set(C)
    while left:
        s = left.pop()
        L, x = 1, g[s]
        while x != s:
            left.discard(x); x = g[x]; L += 1
        lens.append(L)
    return tuple(sorted(lens))

def npartitions(s):
    if s == 0: return 1
    parts = [0]*(s+1); parts[0] = 1
    for k in range(1, s+1):
        for j in range(k, s+1):
            parts[j] += parts[j-k]
    return parts[s]

overall_ok = True
for K in (5, 6):
    print("="*72)
    print(f"K={K}: enumerating all {(K+1)**K} raw maps")
    print("="*72)
    per_r = Counter()
    shapes = Counter()
    onpart_count = Counter()   # (C_frozen, sigma_tuple) -> raw off-config count
    for g in itertools.product(range(-1, K), repeat=K):
        C = cycle_nodes(g, K)
        r = len(C)
        per_r[r] += 1
        ct = cycle_type(g, C) if r else ()
        shapes[(r, ct)] += 1
        sigma = tuple(sorted((i, g[i]) for i in C))
        onpart_count[(frozenset(C), sigma)] += 1
    print(f"  per-r raw counts: {[per_r[r] for r in range(K+1)]} "
          f"(sum {sum(per_r.values())})")
    if K == 5:
        want = [1296, 2160, 2160, 1440, 600, 120]
        ok = [per_r[r] for r in range(6)] == want and sum(per_r.values()) == 7776
        overall_ok &= ok
        print(f"  vs front's pre-registered {want}: {'PASS' if ok else 'FAIL'}")
    nshapes = len(shapes)
    want_shapes = sum(npartitions(s) for s in range(K+1))
    ok = nshapes == want_shapes
    overall_ok &= ok
    print(f"  shape types: {nshapes} vs sum_(s<=K) p(s) = {want_shapes} "
          f"{'PASS' if ok else 'FAIL'}")
    # N(r, n_off) constancy + forest-count formula
    byr = defaultdict(set)
    for (C, sigma), cnt in onpart_count.items():
        byr[len(C)].add(cnt)
    ok_all = True
    for r in range(K+1):
        n = K - r
        vals = byr[r]
        forest = (r+1)*((r+1+n)**(n-1)) if n >= 1 else 1
        ok = (len(vals) == 1) and (vals == {forest})
        ok_all &= ok
        print(f"  r={r}: N(r,{n}) values={sorted(vals)} vs (r+1)(r+1+n)^(n-1)={forest} "
              f"{'PASS' if ok else 'FAIL'}")
    overall_ok &= ok_all
    crossfoot = sum(math.comb(K, r)*math.factorial(r) *
                    ((r+1)*((r+1+K-r)**(K-r-1)) if K-r >= 1 else 1)
                    for r in range(K+1))
    ok = crossfoot == (K+1)**K
    overall_ok &= ok
    print(f"  cross-foot sum_r C(K,r) r! N = {crossfoot} vs {(K+1)**K} "
          f"{'PASS' if ok else 'FAIL'}")

print()
print("OVERALL:", "ALL PASS" if overall_ok else "*** SOME CHECK FAILED ***")
sys.exit(0 if overall_ok else 1)
