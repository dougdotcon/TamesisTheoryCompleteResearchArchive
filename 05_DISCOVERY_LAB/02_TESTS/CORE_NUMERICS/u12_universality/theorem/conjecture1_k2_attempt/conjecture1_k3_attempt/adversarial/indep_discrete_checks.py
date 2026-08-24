"""
INDEPENDENT discrete-permutation checks, built entirely from scratch
(no reading of mechanism_check_k3.py, discrete_k3_full_distribution_mc.py,
or mc_lemma1_k3_check.py). Two checks:

  CHECK A (Lemma 1, discrete): for a genuine uniform random permutation of
  [n], with 3 fixed distinct source labels, compute the (m1,m2,m3) region
  counts via first-principles cycle-walking (my own routine), across
  several n, and test convergence to uniform-density-6-on-simplex.

  CHECK B (full mechanism, discrete): build permutation pi, override 3
  source labels' outputs to random destinations u1,u2,u3 (i.i.d. WITH
  replacement -- collisions and fixed points allowed), get the TRUE cyclic
  set via a from-scratch generic functional-graph orbit tracer (color
  marking, handling "already resolved" inheritance correctly -- the exact
  scenario the document's own bug was about), and independently compute a
  PREDICTED cyclic count via region assignment + cycle detection among the
  3 sources + the (distance+1) discrete arc-size rule. Compare exactly.

Seeds: referee-reserved range 20260844000+ (DISC-DEC-063).
"""
import numpy as np

# ---------------------------------------------------------------
# Region assignment: given permutation array pi (pi[y] = image of y),
# and 3 distinct marked labels, compute for every point y in [n]:
#   region[y] in {1,2,3,0(=OUT)}
#   dist[y]   = forward pi-steps from y to the region's owning source
#               (0 if y itself is a source; irrelevant/unset if OUT)
# ---------------------------------------------------------------
def compute_regions(pi, sources):
    n = len(pi)
    src_set = {s: i+1 for i, s in enumerate(sources)}  # label -> region id 1,2,3
    visited = np.zeros(n, dtype=bool)
    region = np.zeros(n, dtype=np.int8)
    dist = np.full(n, -1, dtype=np.int64)

    for start in range(n):
        if visited[start]:
            continue
        # walk the cycle containing 'start' fully (cycles are disjoint)
        cyc = []
        cur = start
        while not visited[cur]:
            visited[cur] = True
            cyc.append(cur)
            cur = pi[cur]
        L = len(cyc)
        marked_positions = [(idx, src_set[cyc[idx]]) for idx in range(L) if cyc[idx] in src_set]
        if not marked_positions:
            for y in cyc:
                region[y] = 0  # OUT
                dist[y] = -1
            continue
        # for each position in the cycle, find forward distance to the
        # NEXT marked position (cyclically), and which region that is.
        K = len(marked_positions)
        for idx in range(L):
            # binary/linear search for next marked position >= idx (cyclic)
            best = None
            for (mp, reg) in marked_positions:
                d = (mp - idx) % L
                if best is None or d < best[0]:
                    best = (d, reg)
            d, reg = best
            region[cyc[idx]] = reg
            dist[cyc[idx]] = d
    return region, dist

# faster region assignment for larger n (linear per cycle, not quadratic)
def compute_regions_fast(pi, sources):
    n = len(pi)
    src_set = {s: i+1 for i, s in enumerate(sources)}
    visited = np.zeros(n, dtype=bool)
    region = np.zeros(n, dtype=np.int8)
    dist = np.full(n, -1, dtype=np.int64)
    for start in range(n):
        if visited[start]:
            continue
        cyc = []
        cur = start
        while not visited[cur]:
            visited[cur] = True
            cyc.append(cur)
            cur = pi[cur]
        L = len(cyc)
        marked_idx = [idx for idx in range(L) if cyc[idx] in src_set]
        if not marked_idx:
            for y in cyc:
                region[y] = 0
                dist[y] = -1
            continue
        K = len(marked_idx)
        # for each idx in 0..L-1, next marked position cyclically (linear scan via doubling)
        ext = marked_idx + [m + L for m in marked_idx]
        j = 0
        for idx in range(L):
            while ext[j] < idx:
                j += 1
            nxt = ext[j]
            d = nxt - idx
            reg = src_set[cyc[nxt % L]]
            region[cyc[idx]] = reg
            dist[cyc[idx]] = d
    return region, dist


# ---------------------------------------------------------------
# CHECK A: Lemma 1, discrete convergence to uniform density 6 on simplex
# ---------------------------------------------------------------
def check_lemma1(n, trials, rng):
    m = np.zeros((trials, 3))
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=3, replace=False)
        region, dist = compute_regions_fast(pi, sources)
        for r in (1, 2, 3):
            m[t, r-1] = np.sum(region == r) / n
    return m

print("="*70)
print("CHECK A -- independent discrete Lemma 1 check")
print("="*70)
rng = np.random.default_rng(np.random.SeedSequence(20260844010))
from scipy import stats

for n, trials in [(400, 6000), (1500, 3000), (6000, 1500)]:
    m = check_lemma1(n, trials, rng)
    L = m.sum(axis=1)
    Em1, Em1sq = m[:,0].mean(), (m[:,0]**2).mean()
    Cov12 = np.cov(m[:,0], m[:,1])[0,1]
    # marginal of m_i should be Beta(1,3) i.e. CDF 1-(1-x)^3
    Dks, pks = stats.kstest(m[:,0], lambda z: 1-(1-z)**3)
    # L = m1+m2+m3 should have CDF x^3 (density 3x^2, since L is the max of the
    # "distinct block coverage"; check against document's own reported L-CDF
    # target 3*ell^2 density -> CDF ell^3)
    DL, pL = stats.kstest(L, lambda z: z**3)
    # exchangeability: m1 vs m2
    Dex, pex = stats.kstest(m[:,0], m[:,1])
    print(f"n={n:5d} trials={trials}: E[m1]={Em1:.4f}(target 0.25) E[m1^2]={Em1sq:.4f}(target 0.1) "
          f"Cov(m1,m2)={Cov12:.5f}(target {-1/80:.5f})")
    print(f"           KS(m1 vs Beta(1,3)): D={Dks:.4f} p={pks:.4f}   KS(L vs x^3): D={DL:.4f} p={pL:.4f}   "
          f"Exchangeability KS(m1,m2): D={Dex:.4f} p={pex:.4f}")

print()
print("="*70)
print("CHECK B -- independent discrete mechanism check (ground truth vs predicted)")
print("="*70)

def true_cyclic_count(f):
    """f: array, f[y] = image of y under the (possibly non-bijective) map."""
    n = len(f)
    status = np.zeros(n, dtype=np.int8)  # 0 unvisited,1 in-progress,2 cyclic,3 noncyclic
    for start in range(n):
        if status[start] != 0:
            continue
        path = []
        cur = start
        while status[cur] == 0:
            status[cur] = 1
            path.append(cur)
            cur = f[cur]
        if status[cur] == 1:
            # found new cycle; locate cur in path
            idx = path.index(cur)
            for y in path[:idx]:
                status[y] = 3
            for y in path[idx:]:
                status[y] = 2
        else:
            # cur already resolved (2 or 3) from a previous walk -> whole path noncyclic
            for y in path:
                status[y] = 3
    return int((status == 2).sum())

def predicted_cyclic_count(pi, sources, dests, region, dist):
    """sources: array of 3 distinct labels. dests: array of 3 destination values
    (may repeat / be fixed points). region,dist precomputed from pi,sources."""
    n = len(pi)
    src_set = list(sources)
    # g[i] = region (1,2,3) or 0(=OUT) that dest[i] lands in
    g = np.array([region[d] for d in dests])
    d_to_src = np.array([dist[d] for d in dests])  # steps from dest[i] to its region's OWN source (if in a region)
    region_count = np.array([np.sum(region == r) for r in (1,2,3)])
    out_count = np.sum(region == 0)

    # cycle detection among {0,1,2} (indices for src_set[0..2]), target = g[i]-1 if g[i]!=0 else OUT
    # note: g[i] tells which REGION dest[i] falls in; that region "belongs to" source index (g[i]-1)
    targets = np.where(g == 0, -1, g - 1)  # -1 = OUT, else 0,1,2 index into src_set

    on_cycle = [False, False, False]
    for start in range(3):
        seen = []
        cur = start
        for _ in range(4):
            if cur == -1:
                break
            if cur in seen:
                idx = seen.index(cur)
                cyc = seen[idx:]
                if start in cyc:
                    on_cycle[start] = True
                break
            seen.append(cur)
            cur = targets[cur]

    new_mass = 0
    for i in range(3):
        if on_cycle[i]:
            new_mass += int(d_to_src[i]) + 1  # discrete arc size = distance+1 points

    predicted = int(out_count) + new_mass
    return predicted

def run_mechanism_check(n, trials, rng):
    mismatches = 0
    cell_hits = set()
    n_collisions = 0
    n_fixedpoints = 0
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=3, replace=False)
        dests = rng.integers(0, n, size=3)  # WITH replacement: collisions/fixed points allowed
        if len(set(dests.tolist())) < 3:
            n_collisions += 1
        if any(dests[i] == sources[i] for i in range(3)):
            n_fixedpoints += 1

        region, dist = compute_regions_fast(pi, sources)

        f = pi.copy()
        for i in range(3):
            f[sources[i]] = dests[i]

        true_count = true_cyclic_count(f)
        pred_count = predicted_cyclic_count(pi, sources, dests, region, dist)

        # raw cell signature (which region/OUT each dest lands in) for coverage tracking
        g = tuple(int(region[d]) for d in dests)
        cell_hits.add(g)

        if true_count != pred_count:
            mismatches += 1
            if mismatches <= 5:
                print(f"  MISMATCH @ trial {t}: n={n} sources={sources} dests={dests} true={true_count} pred={pred_count}")

    return mismatches, len(cell_hits), n_collisions, n_fixedpoints

rngB = np.random.default_rng(np.random.SeedSequence(20260844020))
total_mismatch = 0
total_trials = 0
for n, trials in [(30, 20000), (200, 6000)]:
    mism, ncells, ncoll, nfp = run_mechanism_check(n, trials, rngB)
    total_mismatch += mism
    total_trials += trials
    print(f"n={n:4d} trials={trials}: mismatches={mism}/{trials}  raw cells hit={ncells}/64  "
          f"collisions={ncoll} fixed_points={nfp}")

print(f"\nTOTAL: {total_mismatch} mismatches / {total_trials} trials")
