#!/usr/bin/env python3
"""Raw discrete finite-n simulation of the full K=5 model.

Fresh code; no prior front/referee script read or imported.  Uses NONE of
the region/shape/formula machinery — only a genuine uniform random
permutation, 5 rerouted labels, i.i.d. uniform destinations, and a
from-scratch color-marking orbit trace for the TRUE cyclic set of f.

Targets: KS of M_5/n against F(x) = 1 - (1-x^2)^5, mean against
phi_5 = 256/693 = 0.369408...

Scales/seeds (front range): n=10000 -> 20260860010 (4000 trials),
n=20000 -> 20260860011 (2000 trials).
"""
import json
import numpy as np
from scipy import stats

K = 5


def true_cyclic_count(f):
    n = len(f)
    color = [0] * n
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


def run_scale(n, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    vals = np.empty(trials)
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=K, replace=False)
        us = rng.integers(0, n, size=K)
        f = pi.tolist()
        for i in range(K):
            f[int(sources[i])] = int(us[i])
        vals[t] = true_cyclic_count(f) / n
    ks = stats.kstest(vals, lambda x: 1 - (1 - np.clip(x, 0, 1) ** 2) ** 5)
    mean = vals.mean()
    se = vals.std(ddof=1) / np.sqrt(trials)
    phi5 = 256 / 693
    z = (mean - phi5) / se
    print(f"n={n}, trials={trials}: KS D={ks.statistic:.5f} "
          f"p={ks.pvalue:.4f}  mean(M5/n)={mean:.6f}+/-{se:.6f} "
          f"vs 256/693={phi5:.6f} (z={z:+.2f})")
    return {"n": n, "trials": trials, "seed": seed,
            "ks_D": float(ks.statistic), "ks_p": float(ks.pvalue),
            "mean": float(mean), "se": float(se), "z": float(z)}


results = [run_scale(10000, 4000, 20260860010),
           run_scale(20000, 2000, 20260860011)]
with open("discrete_k5_full_distribution_mc.json", "w") as fh:
    json.dump(results, fh, indent=1)
ok = all(r["ks_p"] > 0.01 and abs(r["z"]) < 3 for r in results)
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
