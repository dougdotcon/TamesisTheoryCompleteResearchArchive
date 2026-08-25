#!/usr/bin/env python3
"""Destination combinatorics at K=5 (and a K=6 beyond-target count check).

Fresh code; no prior front/referee script read or imported.

Enumerate all (K+1)^K raw redirect maps g:{0..K-1} -> {0..K-1, OUT},
classify by (on-cycle set C, cycle type of g|C), and verify:
  - per-r_on raw counts (K=5 registered: 1296,2160,2160,1440,600,120)
  - number of shape types = sum_{s=0}^{K} p(s)  (K=5: 19; K=6: 30)
  - N(r_on, n_off) := number of off-part assignments is IDENTICAL across
    every specific on-set and cycle-permutation realizing that r_on, and
    equals the labeled-forest count (r+1)*(r+1+n_off)^(n_off-1)
  - cross-check: sum_r C(K,r) r! N(r,K-r) = (K+1)^K
"""
import itertools
import json
from math import comb, factorial

results = {}
ok_all = True


def check(label, cond):
    global ok_all
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        ok_all = False


def on_cycle_set(g, K):
    """Nodes on cycles of g (OUT = K, absorbing)."""
    on = []
    for i in range(K):
        v = i
        for _ in range(K + 1):
            if v == K:
                break
            v = g[v]
            if v == i:
                on.append(i)
                break
    return tuple(on)


def cycle_type(g, C):
    """Sorted cycle lengths of the permutation g restricted to C."""
    seen = set()
    lens = []
    for i in C:
        if i in seen:
            continue
        L = 0
        v = i
        while v not in seen:
            seen.add(v)
            v = g[v]
            L += 1
        lens.append(L)
    return tuple(sorted(lens))


def num_partitions(s):
    if s == 0:
        return 1
    parts = [0] * (s + 1)
    parts[0] = 1
    for k in range(1, s + 1):
        for tot in range(k, s + 1):
            parts[tot] += parts[tot - k]
    return parts[s]


for K in (5, 6):
    print("=" * 72)
    print(f"K = {K}: enumerating all {(K+1)**K} raw maps")
    per_r = {}
    shapes = {}
    off_counts = {}          # (frozen on-set, sigma-as-tuple) -> raw count
    for g in itertools.product(range(K + 1), repeat=K):
        C = on_cycle_set(g, K)
        r = len(C)
        per_r[r] = per_r.get(r, 0) + 1
        ct = cycle_type(g, C)
        shapes[(r, ct)] = shapes.get((r, ct), 0) + 1
        sigma = tuple(g[i] for i in C)
        key = (C, sigma)
        off_counts[key] = off_counts.get(key, 0) + 1
    per_r_list = [per_r.get(r, 0) for r in range(K + 1)]
    print(f"  per-r_on raw counts: {per_r_list} (sum {sum(per_r_list)})")
    print(f"  shape types: {len(shapes)}")
    for (r, ct), cnt in sorted(shapes.items()):
        print(f"    r_on={r}, cycle type {ct}: {cnt} raw configs")
    expected_types = sum(num_partitions(s) for s in range(K + 1))
    check(f"K={K}: shape-type count = sum p(s) = {expected_types}",
          len(shapes) == expected_types)
    check(f"K={K}: total raw configs = (K+1)^K",
          sum(per_r_list) == (K + 1) ** K)

    # N(r, n_off) constancy across every (C, sigma)
    n_by_r = {}
    constancy = True
    for (C, sigma), cnt in off_counts.items():
        r = len(C)
        if r in n_by_r and n_by_r[r] != cnt:
            constancy = False
        n_by_r[r] = cnt
    check(f"K={K}: N(r,n_off) constant across all (on-set, sigma) choices",
          constancy)
    forest_ok = True
    for r in range(K + 1):
        n_off = K - r
        forest = (r + 1) * (r + 1 + n_off) ** (n_off - 1) if n_off >= 1 else 1
        got = n_by_r.get(r)
        print(f"  r={r}: N(r,{n_off}) = {got}, forest formula "
              f"(r+1)(r+1+n_off)^(n_off-1) = {forest}")
        if got != forest:
            forest_ok = False
    check(f"K={K}: N matches labeled-forest count", forest_ok)
    cross = sum(comb(K, r) * factorial(r) * n_by_r[r] for r in range(K + 1))
    check(f"K={K}: sum_r C(K,r) r! N(r,K-r) = (K+1)^K",
          cross == (K + 1) ** K)

    results[f"K{K}"] = {
        "per_r_raw_counts": per_r_list,
        "shape_types": len(shapes),
        "shapes": {f"r{r}_ct{ct}": cnt for (r, ct), cnt in sorted(shapes.items())},
        "N_by_r": {str(r): n_by_r[r] for r in range(K + 1)},
    }

# Registered K=5 predictions
check("K=5 registered per-r counts 1296,2160,2160,1440,600,120",
      results["K5"]["per_r_raw_counts"] == [1296, 2160, 2160, 1440, 600, 120])
check("K=5 registered 19 shape types", results["K5"]["shape_types"] == 19)
check("K=6 registered 30 shape types", results["K6"]["shape_types"] == 30)

with open("enumerate_destination_combinatorics_k5.json", "w") as fh:
    json.dump(results, fh, indent=1)
print("=" * 72)
print("ALL CHECKS PASSED" if ok_all else "SOME CHECKS FAILED")
