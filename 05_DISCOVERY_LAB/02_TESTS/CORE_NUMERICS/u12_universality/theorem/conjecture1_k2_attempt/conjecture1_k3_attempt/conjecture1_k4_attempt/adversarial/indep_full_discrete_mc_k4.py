# Adversarial referee — raw large-n discrete simulation of the FULL K=4
# model.  This is the key independent surface against a hypothetical
# systematic error inherited across the K=2/K=3/K=4 lineage: it shares
# NONE of the continuum machinery (no PD(1), no Lemma 1, no region
# classification, no shape collapse, no per-r formula) and none of my
# own other scripts' code paths for ground truth.
#
# Per trial: uniform random permutation pi of {0..n-1}; 4 distinct
# sources; 4 iid uniform destinations (with replacement); f = pi with
# f[x_i]=u_i; M = #cyclic nodes of f, found by POINTER DOUBLING (a
# fourth, independent cyclic-set algorithm: for T >= n, the image of
# f^T is exactly the set of on-cycle nodes — tails are shorter than n,
# and every cycle node is f^T of the node T steps behind it on its own
# cycle).  KS of M/n against F(x) = 1 - (1-x^2)^4 (the CDF of
# 8x(1-x^2)^3), mean vs 128/315.
#
# Scales: n=10000 and n=20000 (the document's), PLUS n=40000 (a scale
# the front never ran — a genuinely new point on the convergence curve).
# Seeds: 20260851010 / 011 / 012 (referee-reserved range).

import numpy as np
from scipy import stats
import json

def cyclic_count_pointer_doubling(f):
    n = len(f)
    T = 1
    F = f.copy()
    while T < n:                      # after loop: F = f^(2^k), 2^k >= n
        F = F[F]
        T *= 2
    return np.unique(F).size


def run_scale(n, trials, seed):
    rng = np.random.default_rng(seed)
    vals = np.empty(trials)
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=4, replace=False)
        us = rng.integers(0, n, size=4)
        f = pi
        f[sources] = us               # pi not reused afterwards
        vals[t] = cyclic_count_pointer_doubling(f) / n
    ks = stats.kstest(vals, lambda x: 1 - (1 - np.asarray(x) ** 2) ** 4)
    mean = vals.mean()
    se = vals.std(ddof=1) / np.sqrt(trials)
    z = (mean - 128 / 315) / se
    print(f"n={n:6d}, trials={trials}: KS D={ks.statistic:.5f} "
          f"p={ks.pvalue:.4f}   mean(M4/n)={mean:.6f}+/-{se:.6f} "
          f"vs 128/315={128/315:.6f} (z={z:+.2f})")
    return dict(n=n, trials=trials, seed=seed, D=float(ks.statistic),
                p=float(ks.pvalue), mean=float(mean), se=float(se),
                z=float(z))


# quick self-test of the pointer-doubling counter vs a naive oracle
rng0 = np.random.default_rng(20260851013)
for _ in range(200):
    n0 = int(rng0.integers(5, 30))
    f0 = rng0.integers(0, n0, size=n0)
    # naive: y cyclic iff f^t(y)=y for some 1<=t<=n0
    cnt = 0
    for y in range(n0):
        cur = y
        for _ in range(n0):
            cur = f0[cur]
            if cur == y:
                cnt += 1
                break
    assert cnt == cyclic_count_pointer_doubling(f0)
print("pointer-doubling counter self-test vs naive oracle "
      "(200 random functional graphs): OK\n")

RES = []
RES.append(run_scale(10000, 4000, 20260851010))
RES.append(run_scale(20000, 2000, 20260851011))
RES.append(run_scale(40000, 1200, 20260851012))

with open("indep_full_discrete_mc_k4_results.json", "w") as fh:
    json.dump(RES, fh, indent=1)
print("\nresults written to indep_full_discrete_mc_k4_results.json")
