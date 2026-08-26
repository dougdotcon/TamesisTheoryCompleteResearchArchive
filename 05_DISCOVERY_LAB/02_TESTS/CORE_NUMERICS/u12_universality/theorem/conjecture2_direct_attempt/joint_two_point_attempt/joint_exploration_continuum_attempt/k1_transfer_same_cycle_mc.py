"""
Dedicated large-n check of the K=1 transferred prediction:

  P_n^{(1)}(0,1 both cyclic)                 -> 1/2   (PROVED exactly,
                                                          second_moment_bridge_exact.py)
  P_n^{(1)}(same final cycle | both cyclic)   =  1/2   (Theorem J's Corollary,
                                                          EXACT at every finite n,K --
                                                          not a limit -- so this MC
                                                          serves as a harness-correctness
                                                          check, not new evidence)
  P_n^{(1)}(0,1 both cyclic AND same cycle)   -> 1/4   (the NEW transferred claim:
                                                          product of the two facts
                                                          above, via the exact identity
                                                          P(same,both)=(1/2)P(both) that
                                                          holds at every finite n)

This script directly measures all three quantities at large n via fresh
Monte Carlo, as an empirical triangulation of ATTEMPT.md's Theorem
(transferred), independent of the exact-enumeration proof.

Cycle-labeling: extends the O(n) functional-graph walk to also assign a
cycle id to every cyclic point, so "same final cycle" can be read off
directly (not re-derived from anything already assumed).

Seeds: reserved block 20260874000-20260875000.
"""
import numpy as np
import json
import time

SEED = 20260874200


def cyclic_and_cycle_id(f, n):
    color = np.zeros(n, dtype=np.int8)
    cycle_id = -np.ones(n, dtype=np.int64)
    next_id = 0
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
            cid = next_id
            next_id += 1
            for node in path[idx:]:
                cycle_id[node] = cid
        for node in path:
            color[node] = 2
    return cycle_id


def run(n, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    both_count = 0
    same_count = 0
    for _ in range(trials):
        perm = rng.permutation(n)
        R = rng.choice(n, size=1, replace=False)
        targets = rng.integers(0, n, size=1)
        f = perm.copy()
        f[R] = targets
        cid = cyclic_and_cycle_id(f, n)
        c0, c1 = cid[0], cid[1]
        if c0 != -1 and c1 != -1:
            both_count += 1
            if c0 == c1:
                same_count += 1
    p_both = both_count / trials
    p_same_given_both = same_count / both_count if both_count > 0 else float('nan')
    p_same_and_both = same_count / trials
    return p_both, p_same_given_both, p_same_and_both, both_count, same_count


if __name__ == "__main__":
    n = 2500
    trials = 60000
    t0 = time.time()
    p_both, p_sgb, p_sab, both_count, same_count = run(n, trials, SEED)
    elapsed = time.time() - t0

    se_both = (p_both * (1 - p_both) / trials) ** 0.5
    se_sab = (p_sab * (1 - p_sab) / trials) ** 0.5
    se_sgb = (p_sgb * (1 - p_sgb) / both_count) ** 0.5 if both_count > 0 else float('nan')

    print(f"n={n} K=1 trials={trials} seed={SEED}  [{elapsed:.1f}s]")
    print(f"P(both cyclic)            = {p_both:.5f}  se={se_both:.5f}  target=0.5     "
          f"diff={p_both-0.5:+.5f}  z={(p_both-0.5)/se_both:+.2f}")
    print(f"P(same | both cyclic)     = {p_sgb:.5f}  se={se_sgb:.5f}  target=0.5     "
          f"diff={p_sgb-0.5:+.5f}  z={(p_sgb-0.5)/se_sgb:+.2f}   "
          f"[Theorem J Corollary -- EXACT at every finite n, this is a harness check]")
    print(f"P(same AND both cyclic)   = {p_sab:.5f}  se={se_sab:.5f}  target=0.25    "
          f"diff={p_sab-0.25:+.5f}  z={(p_sab-0.25)/se_sab:+.2f}   "
          f"[the NEW transferred prediction]")

    results = {
        "n": n, "trials": trials, "seed": SEED,
        "p_both": p_both, "se_both": se_both,
        "p_same_given_both": p_sgb, "se_same_given_both": se_sgb,
        "p_same_and_both": p_sab, "se_same_and_both": se_sab,
        "both_count": both_count, "same_count": same_count,
        "elapsed_s": elapsed,
    }
    with open("k1_transfer_same_cycle_mc_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("\nSaved k1_transfer_same_cycle_mc_results.json")
