#!/usr/bin/env python3
"""Independent discrete-permutation Monte Carlo check of Lemma 1 at K=5.

Fresh code; no prior front/referee script read or imported; no continuum
PD(1)/stick-breaking machinery anywhere — a genuine uniform permutation of
[n] is built, 5 distinct sources drawn, and the five region masses
(m_1..m_5) measured by raw cycle-walking, exactly per Lemma 1's own
definition (m_i = #points whose pi-flow reaches x_i first, /n).

Lemma 1 (K=5) predicts (m_1..m_5) ~ uniform on the simplex, i.e.
Dirichlet(1,1,1,1,1;1):  E[m_i]=1/6, E[m_i^2]=1/21, Cov(m_i,m_j)=-1/252,
L=sum m_i ~ Beta(5,1) (CDF t^5), each m_i ~ Beta(1,5), exchangeable.

Scales/seeds (front range): n=300 -> 20260860020 (15000 trials),
n=1000 -> 20260860021 (10000), n=5000 -> 20260860022 (6000).
Registered expectation: possible small-n KS rejection at n=300 (the
lineage's standard discretization-bias signature), no rejection at
alpha=0.01 by n=1000, 5000; all moment |z| < 3.
"""
import json
import numpy as np
from scipy import stats

K = 5


def region_sizes(pi, sources):
    n = len(pi)
    src_pos = {s: i for i, s in enumerate(sources)}
    sizes = [0] * K
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
        if not any(w in src_pos for w in cyc):
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
            sizes[src_pos[cyc[nxt[i] % L]]] += 1
            visited[cyc[i]] = True
    return sizes


def run_scale(n, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    ms = np.empty((trials, K))
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=K, replace=False)
        sizes = region_sizes(pi, [int(s) for s in sources])
        ms[t] = np.asarray(sizes, dtype=float) / n
    out = {"n": n, "trials": trials, "seed": seed}
    # moments
    tgt_mean, tgt_m2, tgt_cov = 1 / 6, 1 / 21, -1 / 252
    zs = []
    for i in range(K):
        est = ms[:, i].mean()
        se = ms[:, i].std(ddof=1) / np.sqrt(trials)
        zs.append((f"E[m{i+1}]", est, (est - tgt_mean) / se))
    v = ms[:, 0] ** 2
    est = v.mean(); se = v.std(ddof=1) / np.sqrt(trials)
    zs.append(("E[m1^2]", est, (est - tgt_m2) / se))
    w = (ms[:, 0] - ms[:, 0].mean()) * (ms[:, 1] - ms[:, 1].mean())
    est = w.mean(); se = w.std(ddof=1) / np.sqrt(trials)
    zs.append(("Cov(m1,m2)", est, (est - tgt_cov) / se))
    out["moments"] = [(nm, float(e), float(z)) for nm, e, z in zs]
    worst = max(abs(z) for _, _, z in zs)
    print(f"n={n}: " + "  ".join(f"{nm}={e:.5f}(z={z:+.2f})"
                                 for nm, e, z in zs))
    # KS tests
    L = ms.sum(axis=1)
    ks_L = stats.kstest(L, lambda t: np.clip(t, 0, 1) ** 5)
    pooled = ms.ravel()
    ks_m = stats.kstest(pooled, lambda t: 1 - (1 - np.clip(t, 0, 1)) ** 5)
    ks_ex12 = stats.ks_2samp(ms[:, 0], ms[:, 1])
    ks_ex15 = stats.ks_2samp(ms[:, 0], ms[:, 4])
    print(f"   KS(L vs t^5): D={ks_L.statistic:.5f} p={ks_L.pvalue:.4f}   "
          f"KS(pooled m vs Beta(1,5)): D={ks_m.statistic:.5f} p={ks_m.pvalue:.4f}")
    print(f"   exchangeability KS(m1,m2): p={ks_ex12.pvalue:.4f}   "
          f"KS(m1,m5): p={ks_ex15.pvalue:.4f}   worst moment |z|={worst:.2f}")
    out["ks"] = {"L": [float(ks_L.statistic), float(ks_L.pvalue)],
                 "pooled": [float(ks_m.statistic), float(ks_m.pvalue)],
                 "ex12": float(ks_ex12.pvalue), "ex15": float(ks_ex15.pvalue)}
    out["worst_moment_z"] = float(worst)
    return out


results = [run_scale(300, 15000, 20260860020),
           run_scale(1000, 10000, 20260860021),
           run_scale(5000, 6000, 20260860022)]
with open("mc_lemma1_k5_check.json", "w") as fh:
    json.dump(results, fh, indent=1)

okz = all(r["worst_moment_z"] < 3 for r in results)
ok_large = all(min(r["ks"]["L"][1], r["ks"]["pooled"][1],
                   r["ks"]["ex12"], r["ks"]["ex15"]) > 0.01
               for r in results if r["n"] >= 1000)
print("moment criterion (<3 all scales):", "PASS" if okz else "FAIL")
print("KS criterion (no rejection at alpha=0.01, n>=1000):",
      "PASS" if ok_large else "FAIL")
print("ALL CHECKS PASSED" if (okz and ok_large) else "SOME CHECKS FAILED")
