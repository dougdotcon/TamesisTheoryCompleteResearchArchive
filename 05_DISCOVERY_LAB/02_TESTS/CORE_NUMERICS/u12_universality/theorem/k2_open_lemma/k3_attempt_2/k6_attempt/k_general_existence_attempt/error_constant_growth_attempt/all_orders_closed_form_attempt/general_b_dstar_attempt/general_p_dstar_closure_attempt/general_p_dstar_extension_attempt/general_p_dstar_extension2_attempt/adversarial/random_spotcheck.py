"""
Referee's own randomized stress test, seeded from this referee's
reserved range 20260871000+ (confirmed unused elsewhere in the
archive before first use -- see REFEREE_REPORT.md). Samples (p,r,b)
triples reaching further in r,b than the main exhaustive sweep, and
also covers the reduced-scale p=41..60 region.
"""
import time
import numpy as np
from fractions import Fraction

from assemble import Assembler
from ground_truth import D_star as gt_D_star

SEED = 20260871000

def run(n_samples, p_lo, p_hi, r_max, b_max, tag):
    rng = np.random.default_rng(np.random.SeedSequence(SEED))
    checks = 0
    fails = 0
    t0 = time.time()
    asm_cache = {}
    for _ in range(n_samples):
        p = int(rng.integers(p_lo, p_hi + 1))
        r = int(rng.integers(0, r_max + 1))
        b = int(rng.integers(0, b_max + 1))
        if r < p:
            r = p + int(rng.integers(0, 5))  # avoid trivial all-zero draws dominating
        if p not in asm_cache:
            asm_cache[p] = Assembler()
        got = asm_cache[p].D_star(p, r, b)
        want = gt_D_star(p, r, b)
        checks += 1
        if got != want:
            fails += 1
            print(f"MISMATCH [{tag}] p={p} r={r} b={b} got={got} want={want}")
    t1 = time.time()
    print(f"[{tag}] seed={SEED} n={n_samples} p in [{p_lo},{p_hi}] r<= {r_max} b<= {b_max}: "
          f"{checks} checks, {fails} fails, {t1 - t0:.1f}s")
    return checks, fails


if __name__ == "__main__":
    total_checks = 0
    total_fails = 0
    c, f = run(300, 21, 40, 300, 40, "beyond-main-sweep p in 21..40")
    total_checks += c
    total_fails += f
    c, f = run(200, 41, 60, 100, 20, "reduced-scale-region p in 41..60")
    total_checks += c
    total_fails += f
    print(f"TOTAL random_spotcheck: {total_checks} checks, {total_fails} fails")
