"""
random_spotcheck.py -- randomized stress test BEYOND the exhaustive grid
(p=21..40, r<=200, b<=30) run by run_full_sweep.py: larger r, larger b,
and a wider p band, to add assurance against a scale-dependent failure
mode that only appears past the exhaustively-swept range.

Per the task mandate, uses Python's numpy.random.SeedSequence seeded from
this front's reserved range 20260870000-20260870999 (DISC-DEC-078, front
(a)). Confirmed unused elsewhere in the archive before first use (see
DERIVATION_PREREG.md Sec 6 / ATTEMPT.md Sec "Seeds").
"""

import sys
import time
from fractions import Fraction

import numpy as np

sys.setrecursionlimit(5000)  # ground_truth.stirling1_unsigned recurses on
                              # n; large random r needs headroom.

from assemble import Assembler
import ground_truth as gt

SEED = 20260870000


def run(n_samples=400, p_range=(21, 60), r_range=(0, 400), b_range=(0, 60)):
    ss = np.random.SeedSequence(SEED)
    rng = np.random.default_rng(ss)

    checks = 0
    fails = 0
    fail_examples = []
    t0 = time.time()

    # Cache Assembler objects per (p,b) pair encountered, since building
    # one is the expensive part and random sampling will often repeat a
    # (p,b) pair across different r draws.
    cache = {}

    for _ in range(n_samples):
        p = int(rng.integers(p_range[0], p_range[1] + 1))
        r = int(rng.integers(r_range[0], r_range[1] + 1))
        b = int(rng.integers(b_range[0], b_range[1] + 1))
        key = (p, b)
        if key not in cache:
            cache[key] = Assembler(p, b)
        asm = cache[key]
        got = asm.D_star(r)
        want = gt.D_star(p, r, b)
        checks += 1
        if got != want:
            fails += 1
            fail_examples.append((p, r, b, got, want))

    elapsed = time.time() - t0
    print(f"random_spotcheck: seed={SEED}, n_samples={n_samples}, "
          f"p in {p_range}, r in {r_range}, b in {b_range}")
    print(f"  distinct (p,b) Assembler builds: {len(cache)}")
    print(f"  {checks} checks, {fails} fails, {elapsed:.1f}s")
    for ex in fail_examples[:10]:
        print(f"  FAIL: p,r,b,got,want = {ex}")
    return checks, fails


if __name__ == "__main__":
    checks, fails = run()
    print("random_spotcheck: OK" if fails == 0 else "random_spotcheck: FAILURES")
