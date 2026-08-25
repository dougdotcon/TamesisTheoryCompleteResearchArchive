# Adversarial referee — from-scratch discrete checks for K=4.
#
# Check A: independent discrete-permutation Monte Carlo of Lemma 1
#          (four-region mass law ~ uniform on Delta_4), 3 scales,
#          with my own region-assignment routine.
# Check B: discrete mechanism check, rebuilt entirely from scratch:
#          my own ground-truth orbit tracer (cross-validated against a
#          naive f^t-iteration oracle at n=12), my own region/distance
#          assignment, my own (D+1)-points prediction:
#              M_pred = #OUT + sum_{i on cycle of g} (D_i + 1)
#          derived independently: the new cyclic arc contributed by
#          on-cycle member i is the pi-path from u_i to source x_{g(i)}
#          INCLUSIVE at both ends = D_i + 1 points; off-cycle sources
#          contribute nothing; pi-cycles without sources stay cyclic.
#          Exact per-trial comparison, all 625 raw cells tracked,
#          collisions and fixed points allowed and counted.
#          Scales: n=12 (dense collisions, stress) / n=25 / n=150.
#
# Seeds: referee-reserved range 20260851000+ (confirmed unused):
#   Check A: 20260851020 / 021 / 022
#   Check B: 20260851001 / 002 / 003
# None of the front's scripts were read.

import numpy as np
from scipy import stats
import json

RESULTS = {}


# ---------- my own region/distance assignment ----------
def region_and_distance(pi, sources):
    """For permutation pi (array), sources = list of 4 node labels.
    Returns (region, dist): region[y] = index (0..3) of the source
    reached first by background flow from y, or -1 if y's pi-cycle
    contains no source; dist[y] = #pi-steps from y to that source."""
    n = len(pi)
    region = np.full(n, -1, dtype=np.int64)
    dist = np.zeros(n, dtype=np.int64)
    srcidx = {s: i for i, s in enumerate(sources)}
    seen = np.zeros(n, dtype=bool)
    for start in range(n):
        if seen[start]:
            continue
        # extract the pi-cycle through start
        cyc = [start]
        cur = pi[start]
        while cur != start:
            cyc.append(cur)
            cur = pi[cur]
        L = len(cyc)
        for node in cyc:
            seen[node] = True
        spos = [a for a, node in enumerate(cyc) if node in srcidx]
        if not spos:
            continue                       # whole cycle is OUT
        for a in range(L):
            best = None
            for b in spos:
                d = (b - a) % L
                if best is None or d < best[0]:
                    best = (d, b)
            region[cyc[a]] = srcidx[cyc[best[1]]]
            dist[cyc[a]] = best[0]
    return region, dist


# ---------- my own ground-truth cyclic-node tracer ----------
def true_cyclic_count(f):
    """Number of nodes on cycles of the functional graph f (array)."""
    n = len(f)
    color = np.zeros(n, dtype=np.int8)      # 0 new, 1 on path, 2 done
    ncyc = 0
    for s in range(n):
        if color[s]:
            continue
        path = []
        cur = s
        while color[cur] == 0:
            color[cur] = 1
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:                 # new cycle found on this path
            idx = path.index(cur)
            ncyc += len(path) - idx
        for node in path:
            color[node] = 2
    return ncyc


def naive_cyclic_count(f):
    """Oracle: y cyclic iff f^t(y)=y for some 1<=t<=n (tiny n only)."""
    n = len(f)
    cyc = 0
    for y in range(n):
        cur = y
        for _ in range(n):
            cur = f[cur]
            if cur == y:
                cyc += 1
                break
    return cyc


# ---------- my own 4-node cycle detection ----------
def on_cycle_nodes(g):
    """g: list of 4 targets in {0,1,2,3,-1(OUT)}. Node on cycle iff
    iterating returns to it within 4 steps."""
    on = []
    for i in range(4):
        cur = i
        for _ in range(4):
            t = g[cur]
            if t == -1:
                break
            cur = t
            if cur == i:
                on.append(i)
                break
    return on


# ============================================================
# Check A — Lemma 1 discrete MC
# ============================================================
print("=" * 72)
print("Check A — independent discrete-permutation MC of Lemma 1 (K=4)")
print("=" * 72)
# targets under uniform-on-Delta_4 (Dirichlet(1,1,1,1,1)):
#   E[m_i]=1/5, E[m_i^2]=1/15, Cov(m_i,m_j)=-1/150,
#   m_i ~ Beta(1,4): CDF 1-(1-t)^4
#   L=sum m ~ Beta(4,1): CDF t^4
#   m_i+m_j ~ Beta(2,3)
RESULTS["checkA"] = {}
for n, trials, seed in [(300, 15000, 20260851020),
                        (1000, 10000, 20260851021),
                        (5000, 6000, 20260851022)]:
    rng = np.random.default_rng(seed)
    ms = np.zeros((trials, 4))
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=4, replace=False)
        region, _ = region_and_distance(pi, list(sources))
        for i in range(4):
            ms[t, i] = np.sum(region == i) / n
    L = ms.sum(axis=1)
    Em = ms.mean(axis=0)
    Em1sq = (ms[:, 0] ** 2).mean()
    cov12 = np.cov(ms[:, 0], ms[:, 1])[0, 1]
    se = ms.std(axis=0, ddof=1) / np.sqrt(trials)
    zs = (Em - 0.2) / se
    ks_L = stats.kstest(L, lambda t_: t_ ** 4)
    pooled = ms.reshape(-1)
    ks_m = stats.kstest(pooled, lambda t_: 1 - (1 - t_) ** 4)
    ks_ex12 = stats.ks_2samp(ms[:, 0], ms[:, 1])
    ks_ex14 = stats.ks_2samp(ms[:, 0], ms[:, 3])
    m12 = ms[:, 0] + ms[:, 1]
    ks_b23 = stats.kstest(m12, lambda t_: stats.beta.cdf(t_, 2, 3))
    print(f"n={n}, trials={trials}:")
    print(f"  E[m_i]={np.round(Em,4)}  (target 0.2, |z|max={np.abs(zs).max():.2f})")
    print(f"  E[m1^2]={Em1sq:.5f} (target 1/15={1/15:.5f})   "
          f"Cov(m1,m2)={cov12:.6f} (target -1/150={-1/150:.6f})")
    print(f"  KS L vs t^4: D={ks_L.statistic:.5f} p={ks_L.pvalue:.4f}")
    print(f"  KS pooled m_i vs Beta(1,4): D={ks_m.statistic:.5f} "
          f"p={ks_m.pvalue:.4f}")
    print(f"  KS m1+m2 vs Beta(2,3): D={ks_b23.statistic:.5f} "
          f"p={ks_b23.pvalue:.4f}")
    print(f"  exchangeability KS(m1,m2): p={ks_ex12.pvalue:.3f}   "
          f"KS(m1,m4): p={ks_ex14.pvalue:.3f}")
    RESULTS["checkA"][n] = dict(
        Em=Em.tolist(), zmax=float(np.abs(zs).max()), Em1sq=Em1sq,
        cov12=cov12, ks_L_p=ks_L.pvalue, ks_m_p=ks_m.pvalue,
        ks_b23_p=ks_b23.pvalue, ks_ex12_p=ks_ex12.pvalue,
        ks_ex14_p=ks_ex14.pvalue, seed=seed, trials=trials)

# ============================================================
# Check B — mechanism check, from scratch
# ============================================================
print()
print("=" * 72)
print("Check B — discrete mechanism check (from scratch), 3 scales")
print("=" * 72)
RESULTS["checkB"] = {}
grand_mismatch = 0
for n, trials, seed, oracle in [(12, 30000, 20260851001, True),
                                (25, 60000, 20260851002, False),
                                (150, 20000, 20260851003, False)]:
    rng = np.random.default_rng(seed)
    mismatches = 0
    cells = set()
    ncoll = nfix = 0
    oracle_checked = 0
    examples = []
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=4, replace=False)
        us = rng.integers(0, n, size=4)
        f = pi.copy()
        f[sources] = us
        # ground truth (my tracer)
        M_true = true_cyclic_count(f)
        if oracle and t < 3000:
            M_naive = naive_cyclic_count(f)
            assert M_naive == M_true, (t, list(pi), list(sources), list(us))
            oracle_checked += 1
        # prediction from the document's mechanism (my own rebuild)
        region, dist = region_and_distance(pi, list(sources))
        g = [int(region[us[i]]) for i in range(4)]
        on = on_cycle_nodes(g)
        M_pred = int(np.sum(region == -1)) \
            + sum(int(dist[us[i]]) + 1 for i in on)
        if M_pred != M_true:
            mismatches += 1
            if len(examples) < 3:
                examples.append((list(pi), list(sources), list(us),
                                 M_true, M_pred))
        cells.add(tuple(g))
        if len(set(us.tolist())) < 4:
            ncoll += 1
        if any(us[i] == sources[i] for i in range(4)):
            nfix += 1
    grand_mismatch += mismatches
    print(f"n={n}, trials={trials}: mismatches={mismatches}/{trials}  "
          f"cells hit={len(cells)}/625  collisions={ncoll}  "
          f"fixed-points={nfix}"
          + (f"  (oracle cross-check on {oracle_checked} trials: OK)"
             if oracle else ""))
    if examples:
        print("  EXAMPLES OF MISMATCH:", examples)
    RESULTS["checkB"][n] = dict(
        trials=trials, mismatches=mismatches, cells=len(cells),
        collisions=ncoll, fixed_points=nfix, seed=seed)

print(f"\nTOTAL mismatches: {grand_mismatch} / "
      f"{sum(v['trials'] for v in RESULTS['checkB'].values())}")
assert grand_mismatch == 0, "MECHANISM CHECK FAILED"
print("Check B: PASS — the (D+1)-points mechanism prediction is exact "
      "per configuration,\nincluding the n=12 stress scale (dense "
      "collisions/fixed points), all scales.")

with open("indep_discrete_checks_k4_results.json", "w") as fh:
    json.dump(RESULTS, fh, indent=1)
print("\nresults written to indep_discrete_checks_k4_results.json")
