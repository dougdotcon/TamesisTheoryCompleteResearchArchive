"""
Monte Carlo exploration (NOT a proof) of the distributional bridge at
larger n than exact enumeration reaches, for:
  (A) fixed-K model (Definition 4): empirical CDF of M_n^{(K)} vs
      target F_K(x) = 1-(1-x^2)^K, for K=2,3, at growing n.
  (B) the actual mixed-c model (Definition 1): empirical CDF of M_n(c)
      vs target F(x) = 1-exp(-c x^2), at growing n.

Reserved seed range: 20260876000-20260877000 (this front's own; the
referee range 20260877000+ is untouched). Every RNG stream used below
is a distinct child of a single SeedSequence rooted at BASE_SEED, drawn
in a fixed deterministic order (recorded per-cell as seed_child_index),
so no seed is reused across cells.

Pure-Python cycle detection (O(n) per sample, plain lists, not numpy
scalar indexing, for speed) -- total work per cell is capped at
~1.5e7 (n * trials) so the whole script finishes in a couple of
minutes.
"""
import numpy as np
import json
import time

BASE_SEED = 20260876000
ss_root = np.random.SeedSequence(BASE_SEED)
_child_counter = [0]


def next_generator():
    _child_counter[0] += 1
    child = ss_root.spawn(1)[0]
    return np.random.Generator(np.random.PCG64(child)), _child_counter[0]


def cyclic_count_list(f, n):
    """f: python list of ints (f[i] in [0,n)). Returns #cyclic points."""
    color = [0] * n  # 0 unvisited, 1 in-progress, 2 done
    ncyc = 0
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        i = start
        while color[i] == 0:
            color[i] = 1
            path.append(i)
            i = f[i]
        if color[i] == 1:
            j = path.index(i)
            ncyc += len(path) - j
        for p in path:
            color[p] = 2
    return ncyc


def sample_fixed_K(rng, n, K):
    pi = rng.permutation(n).tolist()
    if K > 0:
        targets = rng.integers(0, n, size=K).tolist()
        pi[:K] = targets
    return cyclic_count_list(pi, n) / n


def sample_mixed_c(rng, n, c):
    pi = rng.permutation(n).tolist()
    reroute_mask = rng.random(n) < (c / n)
    K = int(reroute_mask.sum())
    if K > 0:
        targets = rng.integers(0, n, size=K).tolist()
        idx = np.flatnonzero(reroute_mask)
        for pos, t in zip(idx, targets):
            pi[pos] = t
    return cyclic_count_list(pi, n) / n


def empirical_cdf_stat(samples_sorted, target_fn, grid):
    N = len(samples_sorted)
    worst = 0.0
    worst_x = None
    for x in grid:
        emp = np.searchsorted(samples_sorted, x, side="right") / N
        tgt = target_fn(x)
        d = abs(emp - tgt)
        if d > worst:
            worst = d
            worst_x = x
    return worst, worst_x


WORK_BUDGET = 15_000_000  # n * trials, per cell


def trials_for(n, cap=250_000, floor=3_000):
    return int(min(cap, max(floor, WORK_BUDGET // n)))


def main():
    results = {"base_seed": BASE_SEED, "part_A_fixed_K": [], "part_B_mixed_c": []}
    grid = np.linspace(0.03, 0.97, 25)

    for K in (2, 3):
        for n in (50, 150, 500, 2000):
            trials = trials_for(n)
            rng, idx = next_generator()
            t0 = time.time()
            samples = np.empty(trials)
            for t in range(trials):
                samples[t] = sample_fixed_K(rng, n, K)
            samples.sort()
            target_fn = lambda x, K=K: 1 - (1 - x ** 2) ** K
            D, worst_x = empirical_cdf_stat(samples, target_fn, grid)
            mean = float(samples.mean())
            m2 = float((samples ** 2).mean())
            se_mean = float(samples.std(ddof=1) / np.sqrt(trials))
            elapsed = time.time() - t0
            row = {
                "K": K, "n": n, "trials": trials, "seed_child_index": idx,
                "D_KS": D, "worst_x": float(worst_x), "n_times_D": n * D,
                "mean": mean, "se_mean": se_mean,
                "second_moment": m2, "target_second_moment": 1.0 / (K + 1),
                "elapsed_sec": round(elapsed, 2),
            }
            results["part_A_fixed_K"].append(row)
            print(f"[A] K={K} n={n:5d} trials={trials:6d} seed#{idx}  D_KS={D:.5f}  "
                  f"n*D={n*D:.4f}  mean={mean:.5f}+-{se_mean:.5f}  "
                  f"E[M^2]={m2:.5f} (target {1/(K+1):.5f})  t={elapsed:.1f}s",
                  flush=True)

    for c in (1.0, 4.0):
        for n in (50, 150, 500, 2000):
            trials = trials_for(n)
            rng, idx = next_generator()
            t0 = time.time()
            samples = np.empty(trials)
            for t in range(trials):
                samples[t] = sample_mixed_c(rng, n, c)
            samples.sort()
            target_fn = lambda x, c=c: 1 - np.exp(-c * x ** 2)
            D, worst_x = empirical_cdf_stat(samples, target_fn, grid)
            mean = float(samples.mean())
            elapsed = time.time() - t0
            row = {
                "c": c, "n": n, "trials": trials, "seed_child_index": idx,
                "D_KS": D, "worst_x": float(worst_x), "n_times_D": n * D,
                "mean": mean, "elapsed_sec": round(elapsed, 2),
            }
            results["part_B_mixed_c"].append(row)
            print(f"[B] c={c} n={n:5d} trials={trials:6d} seed#{idx}  D_KS={D:.5f}  "
                  f"n*D={n*D:.4f}  mean={mean:.5f}  t={elapsed:.1f}s", flush=True)

    with open("monte_carlo_results.json", "w") as fh:
        json.dump(results, fh, indent=1)
    print("wrote monte_carlo_results.json")
    print("BASE_SEED =", BASE_SEED, " total child seeds spawned =", _child_counter[0])


if __name__ == "__main__":
    main()
