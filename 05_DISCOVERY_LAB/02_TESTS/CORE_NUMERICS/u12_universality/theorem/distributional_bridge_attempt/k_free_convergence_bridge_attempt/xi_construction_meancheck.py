"""
Small additional check: does the (xi,eta)-based discrete construction used
throughout coupling_bound_check.py (dividers D_i=ceil(n*xi_i), conditioned
on no collision) reproduce the EXACT known mean of M_n^{(K)} at small
(n,K) where the exact value is available from
true_definition4_bruteforce.py (itself cross-checked against THEOREM.md's
own reported table in this front's ATTEMPT.md)? Reserved seeds only.
"""
import random
from fractions import Fraction as Fr

from coupling_bound_check import run_one_trial
from true_definition4_bruteforce import exact_T_distribution

RESERVED_SEED_BASE = 20260933150

if __name__ == "__main__":
    cases = [(6, 2), (5, 1), (5, 3)]
    trials = 300000
    print(f"{'n':>3} {'K':>3} {'MC mean (no-collision-cond.)':>30} {'exact unconditional mean':>26} {'kept/trials':>12}")
    for idx, (n, K) in enumerate(cases):
        counts, total = exact_T_distribution(n, K)
        exact_mean = sum(Fr(k, 1) * Fr(c, total) for k, c in counts.items()) / n

        seed = RESERVED_SEED_BASE + idx
        rng = random.Random(seed)
        tot = 0.0
        cnt = 0
        for _ in range(trials):
            r = run_one_trial(n, K, rng)
            if r["collision"]:
                continue
            tot += r["Mn"]
            cnt += 1
        mc_mean = tot / cnt
        print(f"{n:>3} {K:>3} {mc_mean:>30.6f} {float(exact_mean):>26.6f} {cnt:>6}/{trials} (seed={seed})")
