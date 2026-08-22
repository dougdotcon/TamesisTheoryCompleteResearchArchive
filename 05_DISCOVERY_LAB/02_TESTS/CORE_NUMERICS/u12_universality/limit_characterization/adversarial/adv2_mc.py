"""Surface (b): large-n Monte Carlo, own vectorized simulator.

Cyclic points via iterated composition (doubling): h = f^(2^17) (2^17 >= n),
number of cyclic points = number of distinct values in h (image of f^m,
m>=n, equals the cyclic set; every value of h is cyclic, and every cyclic
point is attained). Distinct counting via np.unique per replica row.

Validation (seed 13131313):
 - c=0  => phi = 1 exactly.
 - c=n  => pure uniform random map: E[#cyclic] ~ sqrt(pi*n/2).
 - n=256: compare against independent stack-walk detector, per-replica equality.

Measurement (seed 77003917 + cell index): n=65536,
c in {0.37, 2.71828, 7.5, 23} (fresh values, not on the old grid).
"""
import numpy as np, json, math, sys, time

ROOT = sys.path[0]

def simulate_batch(n, c, B, rng):
    """Return array (B,) of cyclic fractions."""
    # permutations, batched
    f = np.empty((B, n), dtype=np.int32)
    for b in range(B):
        f[b] = rng.permutation(n).astype(np.int32)
    if c > 0:
        mask = rng.random((B, n)) < (c / n)
        dest = rng.integers(0, n, size=(B, n), dtype=np.int32)
        f = np.where(mask, dest, f)
    # doubling: h = f^(2^k) with 2^k >= n
    k = max(1, int(math.ceil(math.log2(max(n, 2)))))
    h = f
    rows = np.arange(B)[:, None]
    for _ in range(k):
        h = h[rows, h]
    # distinct count per row
    hs = np.sort(h, axis=1)
    distinct = 1 + (hs[:, 1:] != hs[:, :-1]).sum(axis=1)
    return distinct / n

def stack_walk_cyclic(f):
    n = len(f)
    state = np.zeros(n, dtype=np.int8)
    order = np.zeros(n, dtype=np.int64)
    onc = np.zeros(n, dtype=bool)
    for s in range(n):
        if state[s]:
            continue
        stack = []
        v = s
        while state[v] == 0:
            state[v] = 1
            order[v] = len(stack)
            stack.append(v)
            v = f[v]
        if state[v] == 1:
            for w in stack[order[v]:]:
                onc[w] = True
        for w in stack:
            state[w] = 2
    return onc.sum()

def validate():
    rng = np.random.default_rng(13131313)
    rep = {}
    # c=0 -> phi=1
    fr = simulate_batch(1024, 0.0, 8, rng)
    rep["c0_all_one"] = bool(np.all(fr == 1.0))
    # c=n -> pure random map (mask prob 1 -> all rerouted uniform)
    n = 1024
    fr = simulate_batch(n, float(n), 400, rng)
    mean_cyc = fr.mean() * n
    sem = fr.std(ddof=1) / math.sqrt(len(fr)) * n
    # E[#cyclic] for uniform random map on n points: sum_k prod_{j<k}(1-j/n) ~ sqrt(pi n/2) - 1/3...
    exact = 0.0
    prod = 1.0
    for kk in range(n):
        exact += prod          # P(walk from x still fresh after k steps) summed = E[rho length]...
        prod *= (n - 1 - kk) / n
    # E[#cyclic] = sqrt(pi n /2) asymptotically; use asymptotic benchmark
    bench = math.sqrt(math.pi * n / 2)
    rep["cn_random_map"] = {"mean_cyc": mean_cyc, "sem": sem, "benchmark_sqrt_pin2": bench,
                            "z": (mean_cyc - bench) / sem}
    # cross-detector check n=256
    ok = True
    for _ in range(50):
        n2 = 256
        f = rng.permutation(n2).astype(np.int32)
        mask = rng.random(n2) < (2.5 / n2)
        dest = rng.integers(0, n2, size=n2, dtype=np.int32)
        f = np.where(mask, dest, f)
        a = simulate_batch_from(f)
        b = stack_walk_cyclic(f)
        if a != b:
            ok = False
            break
    rep["cross_detector_50trials"] = ok
    return rep

def simulate_batch_from(f):
    n = len(f)
    k = max(1, int(math.ceil(math.log2(n))))
    h = f.copy()
    for _ in range(k):
        h = h[h]
    return len(np.unique(h))

if __name__ == "__main__":
    t0 = time.time()
    val = validate()
    print("VALIDATION:", json.dumps(val, indent=1), flush=True)
    assert val["c0_all_one"] and val["cross_detector_50trials"] and abs(val["cn_random_map"]["z"]) < 4

    n = 65536
    cs = [0.37, 2.71828, 7.5, 23.0]
    NSAMP = 6000
    BATCH = 250
    out = {"n": n, "validation": val, "cells": {}}
    for ci, c in enumerate(cs):
        rng = np.random.default_rng(77003917 + ci)
        vals = []
        nb = NSAMP // BATCH
        for b in range(nb):
            vals.append(simulate_batch(n, c, BATCH, rng))
        vals = np.concatenate(vals)
        m = float(vals.mean()); sem = float(vals.std(ddof=1)/math.sqrt(len(vals)))
        phi = 0.5*math.sqrt(math.pi/c)*math.erf(math.sqrt(c))
        z = (m - phi)/sem
        out["cells"][str(c)] = {"N": int(len(vals)), "mean": m, "sem": sem,
                                "phi_claim": phi, "dev": m - phi, "z": z}
        print(f"c={c}: phi_MC = {m:.6f} +- {sem:.6f}  claim {phi:.6f}  dev {m-phi:+.6f}  z={z:+.2f}  [{time.time()-t0:.0f}s]", flush=True)
    with open(ROOT + "/adv2_mc.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"saved adv2_mc.json  total {time.time()-t0:.0f}s")
