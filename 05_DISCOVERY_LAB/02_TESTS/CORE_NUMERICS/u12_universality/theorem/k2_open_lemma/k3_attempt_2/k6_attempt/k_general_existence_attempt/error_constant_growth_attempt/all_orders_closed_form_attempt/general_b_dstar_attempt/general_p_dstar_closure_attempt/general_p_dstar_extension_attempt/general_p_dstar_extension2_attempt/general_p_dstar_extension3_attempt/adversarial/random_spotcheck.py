"""
Randomized stress test beyond the exhaustive grids, this referee's own
reserved seed range 20260885000-20260885999 (confirmed unused elsewhere
in the archive before first use -- see REFEREE_REPORT.md). Reaches
further in r and b than either exhaustive grid in run_full_sweep.py,
matching (and slightly exceeding) the target document's own randomized
stress-test region (r<=400, b<=60), sampled instead of swept.
"""
import time
import numpy as np
import assemble as asm
import ground_truth as gt
import ingredients as ing

SEED = 20260885000


def run(n_samples=400, p_lo=41, p_hi=80, r_max=400, b_max=60, log=print):
    ing._extend_Q_ladder(p_hi)
    ing._warm_up_moments(2 * p_hi)
    rng = np.random.default_rng(np.random.SeedSequence(SEED))
    checks = 0
    fails = 0
    t0 = time.time()
    cache_assemblers = {}
    for _ in range(n_samples):
        p = int(rng.integers(p_lo, p_hi + 1))
        r = int(rng.integers(0, r_max + 1))
        b = int(rng.integers(0, b_max + 1))
        key = (p, b)
        if key not in cache_assemblers:
            cache_assemblers[key] = asm.Assembler(p, b)
        a = cache_assemblers[key]
        got = a.D_star(r)
        want = gt.D_star(p, r, b)
        checks += 1
        if got != want:
            fails += 1
            log(f"MISMATCH random p={p} r={r} b={b} got={got} want={want}")
    dt = time.time() - t0
    log(f"random_spotcheck: seed={SEED}, n_samples={n_samples}, "
        f"p in [{p_lo},{p_hi}], r in [0,{r_max}], b in [0,{b_max}]")
    log(f"  distinct (p,b) Assembler builds: {len(cache_assemblers)}")
    log(f"  {checks} checks, {fails} fails, {dt:.1f}s")
    return checks, fails


if __name__ == "__main__":
    run()
