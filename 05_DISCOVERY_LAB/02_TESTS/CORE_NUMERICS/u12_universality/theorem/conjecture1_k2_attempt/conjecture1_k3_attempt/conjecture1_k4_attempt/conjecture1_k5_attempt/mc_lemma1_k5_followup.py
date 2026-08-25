#!/usr/bin/env python3
"""Follow-up (higher power, FRESH seeds) for the two flagged statistics of
mc_lemma1_k5_check.py.  The original run is NOT rerun or replaced — its
results stand as reported; this is an additional, disclosed follow-up to
adjudicate chance vs. real effect on:
  (a) exchangeability KS(m1,m2) at n=1000 (original p=0.0039) — note this
      statistic tests a symmetry that holds EXACTLY at every finite n by
      construction (the five source slots are exchangeable by i.i.d.
      sampling), so a persistent rejection could only indicate a code bug,
      not a math effect; also note ks_2samp's nominal p-value assumes
      independent samples, while m1,m2 from the same trial are negatively
      correlated, so nominal p is approximate here anyway;
  (b) KS(L vs t^5) at n=5000 (original p=0.0085, D=0.0213) — if a real
      discretization bias were responsible, the n=1000 scale (5x the bias)
      would have shown a much larger D; it showed D=0.0098, p=0.29.
Seeds (front range, fresh): 20260860023 (n=1000, 40000 trials),
20260860024 (n=5000, 20000 trials).
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


def sample(n, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    ms = np.empty((trials, K))
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=K, replace=False)
        ms[t] = np.asarray(region_sizes(pi, [int(s) for s in sources]),
                           dtype=float) / n
    return ms


out = {}
ms = sample(1000, 40000, 20260860023)
ks12 = stats.ks_2samp(ms[:, 0], ms[:, 1])
ks15 = stats.ks_2samp(ms[:, 0], ms[:, 4])
print(f"n=1000, trials=40000 (seed 20260860023): "
      f"exchangeability KS(m1,m2) p={ks12.pvalue:.4f}, "
      f"KS(m1,m5) p={ks15.pvalue:.4f}")
out["n1000"] = {"trials": 40000, "seed": 20260860023,
                "ex12_p": float(ks12.pvalue), "ex15_p": float(ks15.pvalue)}

ms = sample(5000, 20000, 20260860024)
L = ms.sum(axis=1)
ksL = stats.kstest(L, lambda t: np.clip(t, 0, 1) ** 5)
print(f"n=5000, trials=20000 (seed 20260860024): "
      f"KS(L vs t^5) D={ksL.statistic:.5f} p={ksL.pvalue:.4f}")
out["n5000"] = {"trials": 20000, "seed": 20260860024,
                "L_D": float(ksL.statistic), "L_p": float(ksL.pvalue)}

with open("mc_lemma1_k5_followup.json", "w") as fh:
    json.dump(out, fh, indent=1)
ok = out["n1000"]["ex12_p"] > 0.01 and out["n5000"]["L_p"] > 0.01
print("FOLLOW-UP RESOLVES BOTH AS CHANCE" if ok
      else "FOLLOW-UP DOES NOT RESOLVE — INVESTIGATE FURTHER")
