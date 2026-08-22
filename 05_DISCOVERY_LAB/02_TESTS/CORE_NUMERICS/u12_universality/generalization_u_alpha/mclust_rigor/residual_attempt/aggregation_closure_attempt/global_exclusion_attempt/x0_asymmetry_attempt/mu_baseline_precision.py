"""x0_asymmetry_attempt -- CONTROL, high-precision arm.

Wave 9, DISC-DEC-041 front (a).

`mu_baseline_control.py` finds a small POSITIVE offset of phi(M-U at finite
n) over phi_U(c) in 5 of its 6 completed cells, but at 6000 replicates per
cell the per-cell resolution is only ~0.7% relative -- enough to see a
consistent sign, not enough to call any single cell significant.  This arm
spends the replicates instead of the breadth: ONE value of c, three values
of n, and enough replicates for ~0.1-0.3% resolution, so that

  (a) the existence of the offset can be settled per-cell rather than only
      by a sign test over cells, and
  (b) its n-scaling is visible: an O(1/n) offset must shrink 4x per
      fourfold n, an O(1/sqrt(n)) offset 2x.

c = 50 is chosen because it is in the middle of the grid this whole line
uses and because `mu_baseline_control.py` happened to show its largest
offsets there -- a choice made BEFORE these runs, and recorded here as
such; the point of the arm is the n-scaling, which is choice-independent.

OWN implementation; reuses the M-U builder and the cyclic-set routine from
`mu_baseline_control.py` (same front, same file family -- the convention
the predecessor documents already use for scripts within one front).
Seeds: np.random.SeedSequence(20260822945) -- fresh.
"""
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x0_asym_formula import phi_U
from mu_baseline_control import build_f_MU, cyclic_fraction

SEED_ROOT = 20260822945
CELLS = [(4096, 50.0, 200000), (16384, 50.0, 100000), (65536, 50.0, 40000)]


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "mu_baseline_precision.log"), "w")

    def say(m):
        print(m, flush=True)
        log.write(m + "\n")
        log.flush()

    say("# mu_baseline_precision | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# own implementation, SeedSequence(%d)" % SEED_ROOT)
    say(f"{'n':>7} {'c':>6} {'n_rep':>7} | {'phi_mc':>10} {'sem':>9} | {'phi_U':>9} | "
        f"{'dev%':>7} {'z':>7} | {'n*dev%':>9} {'sqrt(n)*dev%':>13}")
    spawns = np.random.SeedSequence(SEED_ROOT).spawn(len(CELLS))
    out = {"seed_root": SEED_ROOT, "cells": []}
    for (n, c, n_rep), ss in zip(CELLS, spawns):
        rng = np.random.default_rng(ss)
        tot = 0.0
        tot2 = 0.0
        for _ in range(n_rep):
            v = cyclic_fraction(build_f_MU(n, c, rng), n)
            tot += v
            tot2 += v * v
        m = tot / n_rep
        var = (tot2 - n_rep * m * m) / (n_rep - 1)
        sem = math.sqrt(var / n_rep)
        pu = phi_U(c)
        dev = 100 * (m - pu) / pu
        z = (m - pu) / sem
        out["cells"].append(dict(n=n, c=c, n_rep=n_rep, phi_mc=m, sem=sem,
                                 phi_U=pu, dev_pct=dev, z=z))
        say(f"{n:7d} {c:6.1f} {n_rep:7d} | {m:10.6f} {sem:9.6f} | {pu:9.6f} | "
            f"{dev:+6.3f}% {z:+7.2f} | {n * dev:9.1f} {math.sqrt(n) * dev:13.2f}")
    say("# wall %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "mu_baseline_precision_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved mu_baseline_precision_results.json")
    log.close()


if __name__ == "__main__":
    main()
