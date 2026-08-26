"""
Large-n Monte Carlo triangulation of:
  (a) P_nn(n,2) -> 1/3  (this front's derived closed form)
  (b) P_nn-same(n,2) := P(q1,q2 both cyclic AND same final cycle | K=2,
      source/query disjoint) -> 1/6, via DIRECT simulation (not merely
      invoking Theorem J's Corollary symbolically) -- an independent
      triangulation of the transferred continuum result claimed in
      ATTEMPT.md Sec 6.

Reserved seeds: 20260880000-20260880999 (this front's own block, per
governance; grep-confirmed unused before first use). Referee range
20260881000+ untouched.
"""
import random
from fractions import Fraction
import json
import sys

def sample_once(n, rng):
    # uniform random permutation via Fisher-Yates
    pi = list(range(n))
    for i in range(n - 1, 0, -1):
        j = rng.randint(0, i)
        pi[i], pi[j] = pi[j], pi[i]
    u0 = rng.randrange(n)
    u1 = rng.randrange(n)
    f = list(pi)
    f[0] = u0
    f[1] = u1
    q1, q2 = n - 2, n - 1

    # find cyclic status of q1, q2, and whether same final cycle
    def orbit_cycle(x):
        seen = {}
        path = []
        y = x
        step = 0
        while y not in seen:
            seen[y] = step
            path.append(y)
            step += 1
            y = f[y]
        # y is a repeat; cycle = path[seen[y]:]
        cyc = set(path[seen[y]:])
        return cyc

    c1 = orbit_cycle(q1)
    c2 = orbit_cycle(q2)
    both = (q1 in c1) and (q2 in c2)
    same = both and (c1 == c2)
    return both, same


def run(n, trials, seed):
    rng = random.Random(seed)
    both_count = 0
    same_count = 0
    for _ in range(trials):
        b, s = sample_once(n, rng)
        if b:
            both_count += 1
        if s:
            same_count += 1
    return both_count, same_count


if __name__ == "__main__":
    configs = [
        (200, 200000, 20260880001),
        (2000, 30000, 20260880002),
        (5000, 10000, 20260880003),
    ]
    results = []
    for (n, trials, seed) in configs:
        both_c, same_c = run(n, trials, seed)
        p_both = both_c / trials
        p_same = same_c / trials
        se_both = (p_both * (1 - p_both) / trials) ** 0.5
        se_same = (p_same * (1 - p_same) / trials) ** 0.5
        target_both = 1 / 3
        target_same = 1 / 6
        z_both = (p_both - target_both) / se_both if se_both > 0 else float('nan')
        z_same = (p_same - target_same) / se_same if se_same > 0 else float('nan')
        row = dict(n=n, trials=trials, seed=seed,
                   p_both=p_both, se_both=se_both, z_both=z_both,
                   p_same=p_same, se_same=se_same, z_same=z_same)
        results.append(row)
        print(f"n={n} trials={trials} seed={seed}: "
              f"P(both)={p_both:.5f} se={se_both:.5f} z={z_both:+.2f} (target 1/3={target_both:.5f})  |  "
              f"P(same)={p_same:.5f} se={se_same:.5f} z={z_same:+.2f} (target 1/6={target_same:.5f})")
    with open("monte_carlo_k2_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
