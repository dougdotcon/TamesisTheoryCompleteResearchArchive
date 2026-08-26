"""
Large-n Monte Carlo, coarse convergence check for the second-moment
fixed-K bridge: does P_n^{(K)}(x_0,x_1 both cyclic) approach the
already-PROVED continuum target E[M_K^2]=1/(K+1) (Estagio 24) as n grows,
for K=2,3,4,5 (beyond exact-enumeration reach)?

This is explicitly NOT a precise rate-extraction study (multiplying the
MC noise on p_hat by n, to see the O(1/n) coefficient the way
second_moment_bridge_exact.py did exactly for K=0,1, would require
prohibitively many trials -- noted honestly in ATTEMPT.md). It is a
coarse sanity check that the exact small-n numbers (which have not yet
visibly converged by n=6,7 for K>=2 -- see second_moment_bridge_exact.log)
are at least heading toward 1/(K+1), not toward something else, as n
grows by two to three orders of magnitude beyond exact-enumeration
reach.

Cyclic-set detection: standard O(n) functional-graph algorithm
(3-color DFS-iterative walk with in-place path tracking), applied once
per trial to get the cyclic status of ALL n points, then read off
points 0 and 1 -- much cheaper than re-chasing forward from each query
point separately.

Seeds: reserved block 20260874000-20260875000 (grep-confirmed unused
before first use, see PREREG.md). Uses numpy.random.SeedSequence /
default_rng per the archive's numerics discipline.
"""
import numpy as np
import json
import time

SEED_BASE = 20260874100  # offset from the block start, K=1 case used none


def cyclic_mask(f, n):
    """Return a boolean array: cyclic_mask[i] = True iff i is cyclic
    under f (an array of length n with f[i] = image of i). O(n)."""
    color = np.zeros(n, dtype=np.int8)  # 0 unvisited, 1 in-path, 2 done
    is_cyclic = np.zeros(n, dtype=bool)
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = f[x]
        if color[x] == 1:
            idx = path.index(x)
            for node in path[idx:]:
                is_cyclic[node] = True
        for node in path:
            color[node] = 2
    return is_cyclic


def run_trial_batch(n, K, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    both_count = 0
    for _ in range(trials):
        perm = rng.permutation(n)
        R = rng.choice(n, size=K, replace=False)
        targets = rng.integers(0, n, size=K)
        f = perm.copy()
        f[R] = targets
        cyc = cyclic_mask(f, n)
        if cyc[0] and cyc[1]:
            both_count += 1
    p_hat = both_count / trials
    se = (p_hat * (1 - p_hat) / trials) ** 0.5
    return p_hat, se, both_count


if __name__ == "__main__":
    results = []
    configs = [
        # (n, K, trials, seed)
        (2000, 2, 40000, SEED_BASE + 0),
        (2000, 3, 40000, SEED_BASE + 1),
        (2000, 4, 40000, SEED_BASE + 2),
        (2000, 5, 40000, SEED_BASE + 3),
    ]
    for (n, K, trials, seed) in configs:
        t0 = time.time()
        p_hat, se, cnt = run_trial_batch(n, K, trials, seed)
        elapsed = time.time() - t0
        target = 1 / (K + 1)
        z = (p_hat - target) / se if se > 0 else float('nan')
        print(f"n={n} K={K} trials={trials} seed={seed}: "
              f"p_hat={p_hat:.5f} se={se:.5f} target=1/{K+1}={target:.5f} "
              f"diff={p_hat-target:+.5f} z={z:+.2f} n*diff={n*(p_hat-target):+.2f} "
              f"[{elapsed:.1f}s]")
        results.append({"n": n, "K": K, "trials": trials, "seed": seed,
                         "p_hat": p_hat, "se": se, "target": target,
                         "diff": p_hat - target, "z": z, "n_diff": n * (p_hat - target),
                         "elapsed_s": elapsed})
    with open("second_moment_bridge_mc_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("\nSaved second_moment_bridge_mc_results.json")
