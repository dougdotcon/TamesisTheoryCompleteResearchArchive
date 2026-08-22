"""
Own-from-scratch simulators for the U_alpha adversarial check.
Written WITHOUT reading ualpha_sim.py / predictions.py / posthoc_finiten.py
of the target front. Cycle detection: functional-graph doubling
(g = f^(2^K)), cyclic points = distinct image of g -- same method used
(independently) by the wave-2 adversary; re-implemented from scratch here.
"""
import json, time, sys
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

def cyclic_fraction(f, K):
    g = f.copy()
    for _ in range(K):
        g = g[g]
    return np.unique(g).size / f.size

def run_MU(n, c, rng, K):
    pi = rng.permutation(n)
    R = rng.random(n) < c / n
    f = pi.copy()
    nr = R.sum()
    if nr:
        f[R] = rng.integers(0, n, size=nr)
    return cyclic_fraction(f, K)

def run_MIX(n, c, p, rng, K):
    pi = rng.permutation(n)
    R = rng.random(n) < c / n
    f = pi.copy()
    nr = R.sum()
    if nr:
        idx = np.where(R)[0]
        selfmask = rng.random(nr) < p
        dest = rng.integers(0, n, size=nr)
        dest[selfmask] = idx[selfmask]
        f[idx] = dest
    return cyclic_fraction(f, K)

def run_PREV(n, c, rng, K):
    pi = rng.permutation(n)
    inv = np.empty(n, dtype=np.int64)
    inv[pi] = np.arange(n)
    R = rng.random(n) < c / n
    f = pi.copy()
    if R.any():
        f[R] = inv[R]
    return cyclic_fraction(f, K)

def run_CLUST(n, c, b, rng, K):
    pi = rng.permutation(n)
    seed = rng.random(n) < c / n
    Rmask = seed.copy()
    cur = np.where(seed)[0]
    for _ in range(b - 1):
        cur = pi[cur]
        Rmask[cur] = True
    f = pi.copy()
    nr = Rmask.sum()
    if nr:
        f[Rmask] = rng.integers(0, n, size=nr)
    return cyclic_fraction(f, K)

def run_SHARED(n, c, rng, K):
    pi = rng.permutation(n)
    R = rng.random(n) < c / n
    X = rng.integers(0, n)
    f = pi.copy()
    if R.any():
        f[R] = X
    return cyclic_fraction(f, K)

def run_MU_K1(n, rng, K):
    pi = rng.permutation(n)
    f = pi.copy()
    i = rng.integers(0, n)
    f[i] = rng.integers(0, n)
    return cyclic_fraction(f, K)

def run_MIX_K1(n, p, rng, K):
    pi = rng.permutation(n)
    f = pi.copy()
    i = rng.integers(0, n)
    if rng.random() < p:
        f[i] = i
    else:
        f[i] = rng.integers(0, n)
    return cyclic_fraction(f, K)

def run_PREV_K1(n, rng, K):
    pi = rng.permutation(n)
    inv = np.empty(n, dtype=np.int64)
    inv[pi] = np.arange(n)
    f = pi.copy()
    i = rng.integers(0, n)
    f[i] = inv[i]
    return cyclic_fraction(f, K)

def run_INTRA_K1(n, rng, K):
    pi = rng.permutation(n)
    rows = np.arange(n)
    graph = sp.csr_matrix((np.ones(n, dtype=np.int8), (rows, pi)), shape=(n, n))
    ncomp, labels = connected_components(graph, directed=False)
    order = np.argsort(labels, kind="stable")
    counts = np.bincount(labels, minlength=ncomp)
    starts = np.zeros(ncomp + 1, dtype=np.int64)
    starts[1:] = np.cumsum(counts)
    f = pi.copy()
    i = int(rng.integers(0, n))
    L = labels[i]
    off = int(rng.random() * counts[L])
    off = min(off, counts[L] - 1)
    f[i] = order[starts[L] + off]
    return cyclic_fraction(f, K)

def run_INTRA(n, c, rng, K):
    pi = rng.permutation(n)
    rows = np.arange(n)
    graph = sp.csr_matrix((np.ones(n, dtype=np.int8), (rows, pi)), shape=(n, n))
    ncomp, labels = connected_components(graph, directed=False)
    order = np.argsort(labels, kind="stable")
    counts = np.bincount(labels, minlength=ncomp)
    starts = np.zeros(ncomp + 1, dtype=np.int64)
    starts[1:] = np.cumsum(counts)

    R = rng.random(n) < c / n
    f = pi.copy()
    if R.any():
        ridx = np.where(R)[0]
        Li = labels[ridx]
        offs = (rng.random(len(ridx)) * counts[Li]).astype(np.int64)
        offs = np.minimum(offs, counts[Li] - 1)
        dest = order[starts[Li] + offs]
        f[ridx] = dest
    return cyclic_fraction(f, K)

def battery(name, grid, N, seed_seq_entropy, mech_fn, n, K, extra_args=(), log=None):
    ss = np.random.SeedSequence(seed_seq_entropy)
    children = ss.spawn(len(grid))
    out = {}
    t0 = time.time()
    for c, child in zip(grid, children):
        rng = np.random.default_rng(child)
        vals = np.empty(N)
        for k in range(N):
            vals[k] = mech_fn(n, c, *extra_args, rng, K)
        mean = vals.mean()
        sem = vals.std(ddof=1) / np.sqrt(N)
        out[str(c)] = {"mean": mean, "sem": sem, "N": N}
        msg = f"[{name}] c={c} mean={mean:.6f} sem={sem:.6f} ({time.time()-t0:.1f}s elapsed)"
        print(msg)
        if log is not None:
            log.write(msg + "\n"); log.flush()
    return out

def battery_K1(name, N, seed, mech_fn, n, K, log=None):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    vals = np.empty(N)
    for k in range(N):
        vals[k] = mech_fn(n, rng, K)
    mean = vals.mean()
    sem = vals.std(ddof=1) / np.sqrt(N)
    msg = f"[K1-{name}] mean={mean:.6f} sem={sem:.6f} N={N} ({time.time()-t0:.1f}s)"
    print(msg)
    if log is not None:
        log.write(msg + "\n"); log.flush()
    return {"mean": mean, "sem": sem, "N": N}

if __name__ == "__main__":
    outdir = "/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad"
    results = {}
    with open(outdir + "/adv_sim.log", "w") as log:
        t_start = time.time()

        # Battery 1
        n1, K1 = 65536, 17
        c_grid1 = [0.3, 3.0, 18.0, 70.0, 220.0]
        log.write("=== BATTERY 1: control/mechanisms, n=65536, K=17 ===\n")
        results["B1_M-U"] = battery("B1-M-U", c_grid1, 3000, 31415926, run_MU, n1, K1, log=log)
        results["B1_M-MIX0.3"] = battery("B1-M-MIX0.3", c_grid1, 3000, 31415927, run_MIX, n1, K1, extra_args=(0.3,), log=log)
        results["B1_M-PREV"] = battery("B1-M-PREV", c_grid1, 3000, 31415928, run_PREV, n1, K1, log=log)
        results["B1_M-CLUST13"] = battery("B1-M-CLUST13", c_grid1, 3000, 31415929, run_CLUST, n1, K1, extra_args=(13,), log=log)

        # Battery 2: CLUST stress b=50
        n2, K2 = 65536, 17
        c_grid2 = [10.0, 50.0, 150.0, 400.0]
        log.write("=== BATTERY 2: M-CLUST(b=50) stress, n=65536, K=17 ===\n")
        results["B2_M-CLUST50"] = battery("B2-M-CLUST50", c_grid2, 2000, 27182818, run_CLUST, n2, K2, extra_args=(50,), log=log)

        # Battery 4: M-SHARED (run before B3 since B3 is the expensive one)
        n4, K4 = 65536, 17
        c_grid4 = [3.0, 18.0, 70.0]
        log.write("=== BATTERY 4: M-SHARED (exploratory), n=65536, K=17 ===\n")
        results["B4_M-SHARED"] = battery("B4-M-SHARED", c_grid4, 2000, 14142135, run_SHARED, n4, K4, log=log)

        # Battery 3: M-INTRA extended, n=131072
        n3, K3 = 131072, 18
        c_grid3 = [20.0, 80.0, 320.0, 1000.0]
        log.write("=== BATTERY 3: M-INTRA extended, n=131072, K=18 ===\n")
        results["B3_M-INTRA"] = battery("B3-M-INTRA", c_grid3, 1200, 16180339, run_INTRA, n3, K3, log=log)

        # Own K=1 battery, n=65536, K=17
        nk, Kk = 65536, 17
        log.write("=== K=1 BATTERY, n=65536, K=17, N=4000 ===\n")
        ss_k1 = np.random.SeedSequence(271828)
        c_k1, c_k2, c_k3, c_k4 = ss_k1.spawn(4)
        results["K1_M-U"] = battery_K1("M-U", 4000, c_k1, run_MU_K1, nk, Kk, log=log)
        results["K1_M-MIX0.3"] = battery_K1("M-MIX0.3", 4000, c_k2, lambda n, rng, K: run_MIX_K1(n, 0.3, rng, K), nk, Kk, log=log)
        results["K1_M-PREV"] = battery_K1("M-PREV", 4000, c_k3, run_PREV_K1, nk, Kk, log=log)
        results["K1_M-INTRA"] = battery_K1("M-INTRA", 4000, c_k4, run_INTRA_K1, nk, Kk, log=log)

        log.write(f"TOTAL TIME: {time.time()-t_start:.1f}s\n")
        print(f"TOTAL TIME: {time.time()-t_start:.1f}s")

    with open(outdir + "/adv_sim_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("done")
