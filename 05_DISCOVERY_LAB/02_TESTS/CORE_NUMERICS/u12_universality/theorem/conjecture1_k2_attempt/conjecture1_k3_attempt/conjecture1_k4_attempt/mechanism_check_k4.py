"""
K=4 mechanism check -- discrete, per-configuration, exact-match test.

Generalizes mechanism_check_k3.py (which independently confirmed the K=3
64-cell structure at 0 mismatches / 52,000 trials) to K=4's 625-cell
(5^4) structure. Same method throughout: build a genuine uniform random
permutation pi of [n]; pick 4 distinct labels x1,x2,x3,x4; draw
u1,u2,u3,u4 uniform on [n] WITH replacement (collisions and fixed points
allowed); build the actual map f = pi except f(x_i)=u_i; find the TRUE
cyclic set by a from-scratch color-marking orbit trace (ground truth, no
formula assumed). Independently, compute the PREDICTED cyclic count from
this front's own mechanism (region/distance classification, cycle
detection among {0,1,2,3}, the (D_i+1)-points-per-cycle-member formula,
off-cycle nodes contribute 0) and compare EXACTLY.
"""
import numpy as np
import json
import time

K = 4


def make_permutation(n, rng):
    return rng.permutation(n)


def region_and_distance(pi, sources, n):
    """
    For every point y in [n], follow the background permutation pi
    forward until reaching one of `sources` (the K rerouted labels) or
    returning to y without hitting any source (OUT). Returns:
      region[y]   -- index (0..K-1) of the source reached first, or -1 (OUT)
      dist[y]     -- forward pi-distance from y to that source (0 if y is
                     itself a source)
    Implemented in O(n) total via memoized forward-walks. Identical
    algorithm to mechanism_check_k3.py's region_and_distance, generalized
    from 3 sources to K=len(sources) sources (no other change).
    """
    src_index = {s: i for i, s in enumerate(sources)}
    region = np.full(n, -1, dtype=np.int64)
    dist = np.full(n, -1, dtype=np.int64)
    visited_stage = np.zeros(n, dtype=np.int8)  # 0=unvisited,1=in current walk,2=done
    for start in range(n):
        if visited_stage[start] != 0:
            continue
        path = []
        cur = start
        while True:
            if cur in src_index:
                r = src_index[cur]
                for k, node in enumerate(reversed(path + [cur])):
                    region[node] = r
                    dist[node] = k
                    visited_stage[node] = 2
                break
            if visited_stage[cur] == 2:
                r = region[cur]
                base_d = dist[cur]
                for k, node in enumerate(reversed(path)):
                    if r == -1:
                        region[node] = -1
                        dist[node] = -1
                    else:
                        region[node] = r
                        dist[node] = base_d + k + 1
                    visited_stage[node] = 2
                break
            if visited_stage[cur] == 1:
                for node in path:
                    region[node] = -1
                    dist[node] = -1
                    visited_stage[node] = 2
                break
            visited_stage[cur] = 1
            path.append(cur)
            cur = pi[cur]
    return region, dist


def true_cyclic_count(f, n):
    """From-scratch ground-truth orbit trace for a general function
    f: [n]->[n] (not necessarily a permutation). Identical to
    mechanism_check_k3.py's true_cyclic_count -- K-independent, reused
    verbatim."""
    color = np.zeros(n, dtype=np.int8)
    is_cyclic = np.zeros(n, dtype=bool)
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        pos = {}
        cur = start
        while True:
            if color[cur] == 2:
                for node in path:
                    color[node] = 2
                break
            if cur in pos:
                cyc_start = pos[cur]
                for node in path[cyc_start:]:
                    is_cyclic[node] = True
                for node in path:
                    color[node] = 2
                break
            color[cur] = 1
            pos[cur] = len(path)
            path.append(cur)
            cur = f[cur]
    return int(is_cyclic.sum())


def predicted_cyclic_count(pi, sources, region, dist, u, n):
    """Predicted new-cyclic-mass via this front's own mechanism,
    generalized from K=3 to K=4 nodes {0,1,2,3}: classify each u_i by
    region (or OUT); build digraph g on {0,1,2,3}; find cycles; for each
    on-cycle node i (target t=g(i)), the newly cyclic arc is the D_i+1
    points from u_i forward to the source of region t. Off-cycle nodes
    contribute 0."""
    targets = []
    for i in range(K):
        r = region[u[i]]
        targets.append(r if r != -1 else 'OUT')

    def cycles_of(g):
        found = []
        classified = set()
        for start in range(K):
            if start in classified:
                continue
            path = [start]
            cur = start
            seen = {start: 0}
            while True:
                nxt = g[cur]
                if nxt == 'OUT':
                    classified.update(path)
                    break
                if nxt in classified:
                    classified.update(path)
                    break
                if nxt in seen:
                    found.append(tuple(path[seen[nxt]:]))
                    classified.update(path)
                    break
                path.append(nxt)
                seen[nxt] = len(path) - 1
                cur = nxt
        return found

    g = {i: targets[i] for i in range(K)}
    cycs = cycles_of(g)

    inert = int((region == -1).sum())
    new_mass = 0
    for cyc in cycs:
        for i in cyc:
            t = g[i]
            ui = u[i]
            assert region[ui] == t, "u_i must genuinely be classified into its claimed target region"
            Di = dist[ui]
            new_mass += (Di + 1)
    return inert + new_mass


def run(n, trials, seed, log_every=None):
    rng = np.random.default_rng(seed)
    mismatches = 0
    cell_counts = {}
    collisions = 0
    fixed_points = 0
    t0 = time.time()
    for trial in range(trials):
        pi = make_permutation(n, rng)
        sources = rng.choice(n, size=K, replace=False)
        u = rng.integers(0, n, size=K)
        if len(set(u.tolist())) < K:
            collisions += 1
        for i in range(K):
            if u[i] == sources[i]:
                fixed_points += 1

        region, dist = region_and_distance(pi, list(sources), n)

        f = pi.copy()
        for i in range(K):
            f[sources[i]] = u[i]

        true_count = true_cyclic_count(f, n)
        pred_count = predicted_cyclic_count(pi, list(sources), region, dist, u, n)

        targets = tuple(region[u[i]] if region[u[i]] != -1 else 'OUT' for i in range(K))
        cell_counts[targets] = cell_counts.get(targets, 0) + 1

        if true_count != pred_count:
            mismatches += 1
            if mismatches <= 5:
                print(f"  MISMATCH trial {trial}: true={true_count} pred={pred_count} "
                      f"sources={sources.tolist()} u={u.tolist()} targets={targets}")

    elapsed = time.time() - t0
    print(f"n={n} trials={trials}: mismatches={mismatches}/{trials}  "
          f"(match rate={1 - mismatches/trials:.8f})  elapsed={elapsed:.1f}s")
    print(f"  collisions (u_i==u_j for some i!=j, any pair): {collisions}")
    print(f"  fixed points (u_i==x_i): {fixed_points}")
    print(f"  distinct raw target-cells hit: {len(cell_counts)} (of 5**4=625 possible)")
    return mismatches, trials, cell_counts


if __name__ == "__main__":
    results = {}
    print("=" * 78)
    print("K=4 MECHANISM CHECK -- per-configuration exact match, discrete ground truth")
    print("=" * 78)

    print("\n--- Scale 1: n=25, trials=80000 (seed 20260850001) ---")
    mm1, tt1, cells1 = run(25, 80000, 20260850001)
    results['n25'] = {'mismatches': mm1, 'trials': tt1, 'distinct_cells': len(cells1)}

    print("\n--- Scale 2: n=150, trials=25000 (seed 20260850002) ---")
    mm2, tt2, cells2 = run(150, 25000, 20260850002)
    results['n150'] = {'mismatches': mm2, 'trials': tt2, 'distinct_cells': len(cells2)}

    print("\n" + "=" * 78)
    total_mismatches = mm1 + mm2
    total_trials = tt1 + tt2
    print(f"TOTAL across both scales: {total_mismatches} mismatches / {total_trials} trials")
    if total_mismatches == 0:
        print("*** ALL TRIALS MATCHED EXACTLY. Mechanism (region/distance classification, ***")
        print("*** cycle detection, (D+1)-per-cycle formula, off-cycle=0) independently   ***")
        print("*** confirmed at the most granular per-configuration level, K=4.           ***")
    with open("mechanism_check_k4_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=str)
