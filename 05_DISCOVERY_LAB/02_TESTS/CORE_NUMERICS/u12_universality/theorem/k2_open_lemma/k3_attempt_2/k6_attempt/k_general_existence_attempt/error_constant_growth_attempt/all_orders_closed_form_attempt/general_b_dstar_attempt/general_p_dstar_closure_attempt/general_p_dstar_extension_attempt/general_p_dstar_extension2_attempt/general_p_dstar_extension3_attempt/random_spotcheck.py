"""
random_spotcheck.py -- randomized stress test beyond the exhaustive grid,
seeded from this front's reserved range (GENERAL-P-DSTAR-EXTENSION3-ATTEMPT,
wave 19, front (c), DISC-DEC-083): `20260884000-20260884999`. Confirmed
unused elsewhere in the archive before first use (see ATTEMPT.md Sec.0).
The referee range `20260885000+` is not touched.
"""
import time
from fractions import Fraction

import numpy as np

from ground_truth import D_star as ground_truth_D_star
from assemble import Assembler
from odd_part import build_A_table

SEED = 20260884000


def run(n_samples=400, p_range=(41, 80), r_max=400, b_max=60, seed=SEED, log=True):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    build_A_table(p_range[1])  # ensure the shared table covers the sampled p's

    checks = 0
    fails = 0
    t0 = time.time()
    asm_cache = {}
    for _ in range(n_samples):
        p = int(rng.integers(p_range[0], p_range[1] + 1))
        b = int(rng.integers(0, b_max + 1))
        r = int(rng.integers(0, r_max + 1))
        if (p, b) not in asm_cache:
            asm_cache[(p, b)] = Assembler(p, b)
        asm = asm_cache[(p, b)]
        got = asm.D_star(r)
        want = ground_truth_D_star(p, r, b)
        checks += 1
        if got != want:
            fails += 1
            print(f"MISMATCH random p={p} r={r} b={b}: got={got} want={want}")
    t1 = time.time()
    if log:
        print(f"random_spotcheck: seed={seed}, n_samples={n_samples}, "
              f"p in {p_range}, r in (0,{r_max}), b in (0,{b_max})")
        print(f"  distinct (p,b) Assembler builds: {len(asm_cache)}")
        print(f"  {checks} checks, {fails} fails, {t1 - t0:.1f}s")
    return checks, fails


if __name__ == "__main__":
    checks, fails = run()
    print("random_spotcheck: OK" if fails == 0 else "random_spotcheck: FAILED")
