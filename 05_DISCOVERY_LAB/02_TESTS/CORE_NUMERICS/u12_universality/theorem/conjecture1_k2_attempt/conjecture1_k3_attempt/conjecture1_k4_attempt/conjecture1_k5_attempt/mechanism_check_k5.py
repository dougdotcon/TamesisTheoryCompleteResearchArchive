#!/usr/bin/env python3
"""Discrete per-configuration mechanism check at K=5.

Fresh code; no prior front/referee script read or imported.

Each trial: uniform random permutation pi of [n]; 5 distinct reroute
sources; 5 i.i.d. uniform destinations (with replacement — collisions and
fixed points allowed); the actual map f (= pi except f(x_i)=u_i).
GROUND TRUTH: cyclic-node count of f via a from-scratch color-marking
orbit trace.  PREDICTED: this document's own mechanism —
  region(y)  = first source reached by the pi-orbit from y (OUT if none),
  g(i)       = region(u_i), D_i = pi-distance from u_i to its region source,
  M_pred     = #{points in source-free pi-blocks} + sum_{i in cyc(g)} (D_i+1).
Exact integer comparison per trial; raw-cell (6^5) coverage tracked.

Seeds (front-reserved range): n=12 -> 20260860001, n=25 -> 20260860002,
n=150 -> 20260860003.
"""
import json
import numpy as np

K = 5
OUT = K
ok_all = True


def true_cyclic_count(f):
    n = len(f)
    color = [0] * n  # 0 unvisited, 1 in progress, 2 done
    count = 0
    for s in range(n):
        if color[s]:
            continue
        path = []
        v = s
        while color[v] == 0:
            color[v] = 1
            path.append(v)
            v = f[v]
        if color[v] == 1:
            idx = path.index(v)
            count += len(path) - idx
        for w in path:
            color[w] = 2
    return count


def regions_and_distances(pi, sources):
    n = len(pi)
    src_pos = {s: i for i, s in enumerate(sources)}
    region = [-1] * n
    dist = [0] * n
    visited = [False] * n
    for s in range(n):
        if visited[s]:
            continue
        cyc = [s]
        v = pi[s]
        while v != s:
            cyc.append(v)
            v = pi[v]
        L = len(cyc)
        has_src = any(w in src_pos for w in cyc)
        if not has_src:
            for w in cyc:
                visited[w] = True
            continue
        nxt = [None] * L
        j = None
        for i in range(2 * L - 1, -1, -1):
            if cyc[i % L] in src_pos:
                j = i
            if i < L:
                nxt[i] = j
        for i in range(L):
            w = cyc[i]
            region[w] = src_pos[cyc[nxt[i] % L]]
            dist[w] = nxt[i] - i
            visited[w] = True
    return region, dist


def g_cycle_nodes(g):
    on = []
    for i in range(K):
        v = i
        for _ in range(K + 1):
            if v == OUT:
                break
            v = g[v]
            if v == i:
                on.append(i)
                break
    return on


def run_scale(n, trials, seed):
    global ok_all
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    mismatches = 0
    cells = set()
    n_collision = 0
    n_fixedpoint = 0
    for _ in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=K, replace=False)
        us = rng.integers(0, n, size=K)
        if len(set(int(u) for u in us)) < K:
            n_collision += 1
        if any(int(us[i]) == int(sources[i]) for i in range(K)):
            n_fixedpoint += 1
        region, dist = regions_and_distances(pi, [int(s) for s in sources])
        g = tuple(region[int(u)] if region[int(u)] >= 0 else OUT for u in us)
        cells.add(g)
        cyc = g_cycle_nodes(g)
        out_mass = sum(1 for y in range(n) if region[y] < 0)
        m_pred = out_mass + sum(dist[int(us[i])] + 1 for i in cyc)
        f = list(pi)
        for i in range(K):
            f[int(sources[i])] = int(us[i])
        m_true = true_cyclic_count(f)
        if m_true != m_pred:
            mismatches += 1
            if mismatches <= 5:
                print(f"  MISMATCH n={n}: pi={list(pi)} src={list(sources)} "
                      f"u={list(us)} true={m_true} pred={m_pred}")
    print(f"n={n:4d}, trials={trials}: mismatches={mismatches}/{trials}, "
          f"cells hit={len(cells)}/7776, collisions={n_collision}, "
          f"fixed-points={n_fixedpoint}")
    if mismatches:
        ok_all = False
    return {"n": n, "trials": trials, "seed": seed,
            "mismatches": mismatches, "cells_hit": len(cells),
            "collisions": n_collision, "fixed_points": n_fixedpoint}


results = []
results.append(run_scale(12, 30000, 20260860001))
results.append(run_scale(25, 500000, 20260860002))
results.append(run_scale(150, 25000, 20260860003))

combined_cells_note = ("cell coverage reported per scale; full 7776 "
                       "coverage expected at n=25 (500k trials), not at "
                       "n=150 (25k trials < 7776*4)")
with open("mechanism_check_k5_results.json", "w") as fh:
    json.dump({"scales": results, "note": combined_cells_note}, fh, indent=1)
total_mis = sum(r["mismatches"] for r in results)
total_tr = sum(r["trials"] for r in results)
print(f"TOTAL: {total_mis} mismatches / {total_tr} trials")
print("ALL CHECKS PASSED" if total_mis == 0 else "SOME CHECKS FAILED")
