"""
Independent hostile referee check -- discrete per-configuration mechanism
check for K=5, built entirely from scratch: a from-scratch ground-truth
orbit tracer on a genuine uniform random permutation of [n] with K=5 rerouted
labels and iid uniform (with-replacement) destinations, versus the predicted
cyclic-mass formula described in ATTEMPT.md's prose (Lemma 2, sec 3.1):

    M_pred = #{points in source-free background cycles}
             + sum_{i in cyc(g)} (D_i + 1)

where g:{1..5}->{1..5,OUT} is the region-level redirect map, cyc(g) is its
on-cycle set, and D_i is the discrete forward distance from destination u_i
to its landing region's own source.

INDEPENDENCE: no .py file of the front or of any prior front/referee (incl.
the stalled prior referee attempt in this same directory) was read. Ground
truth uses a completely generic functional-graph cyclic-node detector (status-
marking pointer chase), not tied to the K=5 mechanism at all -- it would find
the true cyclic set for ANY finite function, making it a genuine independent
oracle.

Seeds: SeedSequence(20260861100), (...101), (...102) -- referee-reserved
range 20260861000+. The prior (stalled, abandoned) referee attempt in this
directory used seed 20260861040 in its own ref_symbolic_lemma1.py (confirmed
by grep before this script ran, not by reading that .py file); this script
avoids collision by starting at 20260861100.
"""
import numpy as np
import sys
from time import time

K = 5

def true_cyclic_count(f):
    """Generic functional-graph cyclic-node oracle: f is an array of length n
    with f[y] in [0,n). Returns boolean array is_cyclic."""
    n = len(f)
    status = np.zeros(n, dtype=np.int8)  # 0 unvisited, 1 in-progress, 2 resolved
    is_cyclic = np.zeros(n, dtype=bool)
    for start in range(n):
        if status[start] != 0:
            continue
        chain = []
        cur = start
        while status[cur] == 0:
            status[cur] = 1
            chain.append(cur)
            cur = f[cur]
        if status[cur] == 1:
            idx = chain.index(cur)
            for node in chain[idx:]:
                is_cyclic[node] = True
            for node in chain:
                status[node] = 2
        else:
            for node in chain:
                status[node] = 2
    return is_cyclic

def region_assign(perm, sources):
    """Given background permutation perm (array length n) and K distinct
    source labels, return:
      region[y]  = index (0..K-1) of the source y's region belongs to, or -1 if
                   y is in a source-free background cycle (OUT/untouched)
      dist[y]    = discrete forward distance from y to its region's own source
                   (0 for the source itself)
      out_count  = total number of points in source-free cycles
    """
    n = len(perm)
    visited = np.zeros(n, dtype=bool)
    region = -np.ones(n, dtype=np.int64)
    dist = -np.ones(n, dtype=np.int64)
    source_set = {s: i for i, s in enumerate(sources)}
    out_count = 0
    for start in range(n):
        if visited[start]:
            continue
        cyc = []
        cur = start
        while not visited[cur]:
            visited[cur] = True
            cyc.append(cur)
            cur = perm[cur]
        # cyc is the full background cycle containing 'start', in forward order
        src_positions = [(pos, source_set[node]) for pos, node in enumerate(cyc) if node in source_set]
        if not src_positions:
            out_count += len(cyc)
            continue
        L = len(cyc)
        # for each node, find the NEXT source position forward (cyclically)
        src_positions.sort()
        m = len(src_positions)
        for k in range(m):
            pos_k, src_idx_k = src_positions[k]
            pos_prev = src_positions[k - 1][0]  # previous source position (wraps)
            # region k spans (pos_prev, pos_k] cyclically
            span_start = (pos_prev + 1) % L
            p = span_start
            d = (pos_k - p) % L
            while True:
                node = cyc[p]
                region[node] = src_idx_k
                dist[node] = d
                if p == pos_k:
                    break
                p = (p + 1) % L
                d -= 1
    return region, dist, out_count

def run_scale(n, n_trials, seed, cell_tracker):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    mismatches = 0
    collisions = 0
    fixed_points = 0
    for _ in range(n_trials):
        perm = rng.permutation(n)
        sources = rng.choice(n, size=K, replace=False)
        dests = rng.integers(0, n, size=K)  # with replacement: collisions/fixed pts allowed

        # ---- predicted ----
        region, dist, out_count = region_assign(perm, sources)
        # g[i] = region index of dests[i], or K (OUT sentinel)
        g = np.full(K, K, dtype=np.int64)
        Dvals = np.zeros(K, dtype=np.int64)
        for i in range(K):
            u = dests[i]
            r = region[u]
            if r == -1:
                g[i] = K  # OUT
            else:
                g[i] = r
                Dvals[i] = dist[u]
        # find on-cycle set of g restricted to 0..K-1 (K=OUT is a sink)
        status = np.zeros(K + 1, dtype=np.int8)
        on_cycle = np.zeros(K, dtype=bool)
        for start in range(K):
            if status[start] != 0:
                continue
            chain = []
            cur = start
            while cur != K and status[cur] == 0:
                status[cur] = 1
                chain.append(cur)
                cur = g[cur]
            if cur != K and status[cur] == 1:
                idx = chain.index(cur)
                for node in chain[idx:]:
                    on_cycle[node] = True
                for node in chain:
                    status[node] = 2
            else:
                for node in chain:
                    status[node] = 2
        M_pred = out_count
        for i in range(K):
            # sum over i THEMSELVES on-cycle (i in cyc(g)), crediting D_i+1
            # to region g(i) (which is necessarily also on-cycle, since g maps
            # the on-cycle set into itself) -- NOT over i whose target happens
            # to be on-cycle (an off-cycle node feeding into a cycle still
            # contributes zero, per Lemma 2).
            if on_cycle[i]:
                M_pred += Dvals[i] + 1

        # ---- ground truth ----
        f = perm.copy()
        for i in range(K):
            f[sources[i]] = dests[i]
        is_cyc = true_cyclic_count(f)
        M_true = int(is_cyc.sum())

        if M_pred != M_true:
            mismatches += 1
            if mismatches <= 5:
                print(f"    MISMATCH: n={n} sources={sources} dests={dests} "
                      f"M_pred={M_pred} M_true={M_true}")

        # cell type: 6^5 raw destination-TYPE configuration (0..5 per source:
        # 0..4 = region index, 5 = OUT)
        cell = tuple(int(g[i]) if g[i] < K else K for i in range(K))
        cell_tracker.add(cell)

        n_coll = K - len(set(dests.tolist()))
        if n_coll > 0:
            collisions += 1
        if any(dests[i] == sources[i] for i in range(K)):
            fixed_points += 1

    return mismatches, collisions, fixed_points

if __name__ == "__main__":
    t0 = time()
    total_trials = 0
    total_mismatches = 0
    cell_tracker = set()
    scales = [
        (25, 200000, 20260861100),
        (150, 60000, 20260861101),
        (12, 40000, 20260861102),
    ]
    for n, trials, seed in scales:
        m, coll, fp = run_scale(n, trials, seed, cell_tracker)
        total_trials += trials
        total_mismatches += m
        print(f"n={n:4d} trials={trials:7d} seed={seed}: mismatches={m}  "
              f"collisions={coll}  fixed_points={fp}  cells_hit_so_far={len(cell_tracker)}/7776")
    print(f"\nTOTAL: {total_mismatches} mismatches / {total_trials} trials, "
          f"all cells hit = {len(cell_tracker)}/7776")
    print(f"wall time: {time()-t0:.1f}s")
    ok = (total_mismatches == 0)
    print(f"\nOVERALL: {'ALL PASS (0 mismatches)' if ok else 'FAIL -- MISMATCHES FOUND'}")
    sys.exit(0 if ok else 1)
