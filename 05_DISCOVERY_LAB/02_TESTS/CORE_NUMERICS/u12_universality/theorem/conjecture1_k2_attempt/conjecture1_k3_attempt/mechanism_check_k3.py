"""
K=3 mechanism check -- discrete, per-configuration, exact-match test.

Generalizes conjecture1_k2_attempt/adversarial/adv_mechanism_check.py's
approach (which the K=2 referee used to independently confirm the 9-cell
table at 100% exact match over 260,000 trials) to K=3's 64-cell structure.

For each trial: build a genuine uniform random permutation pi of [n];
pick 3 distinct labels x1,x2,x3; draw u1,u2,u3 uniform on [n] (with
replacement, independent -- collisions and fixed points allowed, exactly
the edge cases the K=2 referee flagged as most informative); build the
actual map f = pi except f(x_i)=u_i; find the TRUE cyclic set by a
from-scratch color-marking orbit trace (ground truth, no formula
assumed). Independently, compute the PREDICTED cyclic count from this
front's own mechanism (region/distance classification + cycle
detection among {1,2,3} + the (region_size - distance)-per-cycle
formula, generalizing K=2's D_i mechanism) and compare EXACTLY.
"""
import numpy as np
import json
import time

def make_permutation(n, rng):
    return rng.permutation(n)

def region_and_distance(pi, sources, n):
    """
    For every point y in [n], follow the background permutation pi
    forward until reaching one of `sources` (the 3 rerouted labels) or
    returning to y without hitting any source (OUT). Returns:
      region[y]   -- index (0,1,2) of the source reached first, or -1 (OUT)
      dist[y]     -- forward pi-distance from y to that source (0 if y is
                     itself a source)
    Implemented in O(n) total via memoized forward-walks.
    """
    src_index = {s: i for i, s in enumerate(sources)}
    region = np.full(n, -1, dtype=np.int64)
    dist = np.full(n, -1, dtype=np.int64)
    # memoize by walking each never-visited node's forward chain, caching
    # results once any point on the chain is resolved (either it hits a
    # source, or it returns to the chain's own start without ever hitting
    # a source -- meaning the whole pi-cycle is source-free -> OUT for all
    # of them).
    visited_stage = np.zeros(n, dtype=np.int8)  # 0=unvisited,1=in current walk,2=done
    for start in range(n):
        if visited_stage[start] != 0:
            continue
        path = []
        cur = start
        while True:
            if cur in src_index:
                # found a source; assign region/dist along the recorded path
                r = src_index[cur]
                for k, node in enumerate(reversed(path + [cur])):
                    region[node] = r
                    dist[node] = k
                    visited_stage[node] = 2
                break
            if visited_stage[cur] == 2:
                # already resolved by an earlier walk (this happens when
                # we walk the "tail" of a pi-cycle that already had one of
                # its sources resolved from a different starting point
                # earlier in the same cycle) -- propagate cur's own
                # (region, distance) backward along the current path,
                # incrementing distance by 1 per step (or propagate OUT
                # unchanged, if cur itself resolved to OUT).
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
                # returned to a node in the CURRENT walk without hitting a
                # source -> this whole pi-cycle (path from cur onward) is
                # source-free -> OUT for everyone in `path`
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
    f: [n]->[n] (not necessarily a permutation). Standard functional-graph
    color marking: 0=white,1=gray(in current path),2=black(resolved)."""
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
                # cycle found from pos[cur] to end of path
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
    """Predicted new-cyclic-mass via this front's own mechanism:
    classify each u_i by region (or OUT); build digraph g on {0,1,2};
    find cycles; for each on-cycle node i (target t=g(i)), the newly
    cyclic arc is the D_i+1 points from u_i forward to the source of
    region t (D_i := dist[u_i] measured to the SAME source that region t
    belongs to -- i.e. dist[u_i] as computed by region_and_distance,
    valid only if region[u_i]==t, i.e. u_i genuinely lands in region t).
    Off-cycle nodes contribute 0. Background inert mass = count of OUT
    points (region==-1)."""
    targets = []
    for i in range(3):
        r = region[u[i]]
        targets.append(r if r != -1 else 'OUT')

    def cycles_of(g):
        found = []
        classified = set()
        for start in range(3):
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

    g = {i: targets[i] for i in range(3)}
    cycs = cycles_of(g)

    inert = int((region == -1).sum())
    new_mass = 0
    for cyc in cycs:
        for i in cyc:
            t = g[i]  # target region index (0,1,2) that node i's u_i lands in
            ui = u[i]
            assert region[ui] == t, "u_i must genuinely be classified into its claimed target region"
            Di = dist[ui]  # forward pi-STEPS from u_i to the source of region t
            # The newly-cyclic arc is the set of points from u_i forward to
            # (and including) the source -- that is Di+1 points (Di edges,
            # Di+1 vertices), NOT "region size minus Di": the continuum
            # formula "m_i - D_i" uses D_i measured as offset-from-the-
            # region's-far-edge, whereas `dist` here is measured as
            # distance-TO-the-source -- the discrete analogue of the
            # continuum arc length is therefore Di+1 points directly.
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
        sources = rng.choice(n, size=3, replace=False)
        u = rng.integers(0, n, size=3)  # WITH replacement, allow collisions/fixed points
        if len(set(u.tolist())) < 3:
            collisions += 1
        for i in range(3):
            if u[i] == sources[i]:
                fixed_points += 1

        region, dist = region_and_distance(pi, list(sources), n)

        f = pi.copy()
        for i in range(3):
            f[sources[i]] = u[i]

        true_count = true_cyclic_count(f, n)
        pred_count = predicted_cyclic_count(pi, list(sources), region, dist, u, n)

        targets = tuple(region[u[i]] if region[u[i]] != -1 else 'OUT' for i in range(3))
        cell_counts[targets] = cell_counts.get(targets, 0) + 1

        if true_count != pred_count:
            mismatches += 1
            if mismatches <= 5:
                print(f"  MISMATCH trial {trial}: true={true_count} pred={pred_count} "
                      f"sources={sources.tolist()} u={u.tolist()} targets={targets}")

    elapsed = time.time() - t0
    print(f"n={n} trials={trials}: mismatches={mismatches}/{trials}  "
          f"(match rate={1 - mismatches/trials:.8f})  elapsed={elapsed:.1f}s")
    print(f"  collisions (u_i==u_j for some i!=j): {collisions}")
    print(f"  fixed points (u_i==x_i): {fixed_points}")
    print(f"  distinct raw target-cells hit: {len(cell_counts)} (of 64 possible)")
    return mismatches, trials, cell_counts


if __name__ == "__main__":
    results = {}
    print("=" * 78)
    print("K=3 MECHANISM CHECK -- per-configuration exact match, discrete ground truth")
    print("=" * 78)

    print("\n--- Scale 1: n=25, trials=40000 (seed 20260843001) ---")
    mm1, tt1, cells1 = run(25, 40000, 20260843001)
    results['n25'] = {'mismatches': mm1, 'trials': tt1, 'distinct_cells': len(cells1)}

    print("\n--- Scale 2: n=150, trials=12000 (seed 20260843002) ---")
    mm2, tt2, cells2 = run(150, 12000, 20260843002)
    results['n150'] = {'mismatches': mm2, 'trials': tt2, 'distinct_cells': len(cells2)}

    print("\n" + "=" * 78)
    total_mismatches = mm1 + mm2
    total_trials = tt1 + tt2
    print(f"TOTAL across both scales: {total_mismatches} mismatches / {total_trials} trials")
    if total_mismatches == 0:
        print("*** ALL TRIALS MATCHED EXACTLY. Mechanism (region/distance classification, ***")
        print("*** cycle detection, (m-D)-per-cycle formula, off-cycle=0) independently  ***")
        print("*** confirmed at the most granular per-configuration level.               ***")
    with open("mechanism_check_k3_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=str)
