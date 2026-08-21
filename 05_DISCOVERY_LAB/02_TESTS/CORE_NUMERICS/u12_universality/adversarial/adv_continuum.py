"""M4: direct simulation of the n->infinity limit object (no finite-n effects).

Limit derivation (independent, from the ensemble definition only):
 - cycle masses of a uniform permutation -> Poisson-Dirichlet(1),
   sampled by stick-breaking with U(0,1), truncated at residual < 1e-9;
 - rerouted points -> K ~ Poisson(c) positions uniform on [0,1],
   each with an independent uniform destination u_i;
 - jump map g on reroutes: g(i) = first reroute forward (increasing
   coordinate, wrapping) from u_i on u_i's cycle; absorbed if that cycle
   has no reroute.
 - cyclic mass of a realization
     = mass of reroute-free cycles
       + sum over nodes j lying on cycles of g of seglen(j),
   where seglen(j) = forward distance from u_j to position of g(j)
   (the closed f-loops are exactly the segments traversed along
   g-cycles; segments are pairwise disjoint since each lies in the arc
   ending at its target reroute and each g-cycle node has a unique
   predecessor on the cycle).
Unbiased estimator of phi_inf(c). Truncation bias <= K * 1e-9.
"""
import bisect
import json
import math
import sys
import numpy as np

EPS = 1e-9


def one_realization(c, rng):
    # stick-breaking cycles
    starts = [0.0]
    lens = []
    rem = 1.0
    while rem > EPS and len(lens) < 5000:
        u = rng.random()
        L = rem * u
        lens.append(L)
        starts.append(starts[-1] + L)
        rem -= L
    covered = starts[-1]
    ncyc = len(lens)

    K = rng.poisson(c)
    if K == 0:
        return 1.0
    # reroute positions
    pos = []
    for _ in range(K):
        x = rng.random()
        if x < covered:
            pos.append(x)
    K = len(pos)
    if K == 0:
        return 1.0
    cyc_of = [bisect.bisect_right(starts, x) - 1 for x in pos]
    # per-cycle sorted reroute coords (relative) with node ids
    percyc = {}
    for j, (x, ci) in enumerate(zip(pos, cyc_of)):
        percyc.setdefault(ci, []).append((x - starts[ci], j))
    for ci in percyc:
        percyc[ci].sort()

    # mass of reroute-free cycles (residual mass treated as reroute-free:
    # bias <= EPS)
    free_mass = rem
    for ci in range(ncyc):
        if ci not in percyc:
            free_mass += lens[ci]

    # destinations and jump map g
    g = [None] * K
    seglen = [0.0] * K
    for j in range(K):
        u = rng.random()
        if u >= covered:
            continue  # lands in residual dust -> absorbed (prob <= EPS)
        ci = bisect.bisect_right(starts, u) - 1
        lst = percyc.get(ci)
        if not lst:
            continue  # reroute-free cycle -> absorbed
        rel = u - starts[ci]
        coords = [t[0] for t in lst]
        idx = bisect.bisect_left(coords, rel)
        if idx == len(coords):
            tgt_coord, tgt = lst[0]
            d = (lens[ci] - rel) + tgt_coord
        else:
            tgt_coord, tgt = lst[idx]
            d = tgt_coord - rel
        g[j] = tgt
        seglen[j] = d

    # nodes on cycles of g (iterative coloring)
    color = [0] * K  # 0 unvisited, 1 in progress, 2 done
    on_cycle = [False] * K
    for s in range(K):
        if color[s]:
            continue
        path = []
        v = s
        while v is not None and color[v] == 0:
            color[v] = 1
            path.append(v)
            v = g[v]
        if v is not None and color[v] == 1:
            # found new cycle: nodes from v to end of path
            i = path.index(v)
            for w in path[i:]:
                on_cycle[w] = True
        for w in path:
            color[w] = 2

    cyc_mass = free_mass + sum(seglen[j] for j in range(K) if on_cycle[j])
    return cyc_mass


def estimate(c, N, rng):
    tot = 0.0
    tot2 = 0.0
    for _ in range(N):
        v = one_realization(c, rng)
        tot += v
        tot2 += v * v
    mean = tot / N
    var = max(tot2 / N - mean * mean, 0.0) * N / (N - 1)
    return mean, math.sqrt(var / N)


if __name__ == "__main__":
    ss = np.random.SeedSequence(271828)
    cs = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
    Ns = {0.5: 200_000, 50.0: 200_000}
    out = []
    for c, st in zip(cs, ss.spawn(len(cs))):
        rng = np.random.default_rng(st)
        N = Ns.get(c, 50_000)
        mean, sem = estimate(c, N, rng)
        theorem = (1 + c) ** -0.5
        print(f"[M4] c={c}: phi_inf={mean:.6f}±{sem:.6f} theorem={theorem:.6f} "
              f"dev={mean-theorem:+.6f} ({(mean-theorem)/sem:+.1f} sem) N={N}", flush=True)
        out.append(dict(c=c, N=N, phi_inf=mean, sem=sem, theorem=theorem,
                        dev=mean - theorem, dev_over_sem=(mean - theorem) / sem))
    with open("adv_continuum.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("saved adv_continuum.json", flush=True)
