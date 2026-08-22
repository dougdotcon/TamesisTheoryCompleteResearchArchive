"""x0_asymmetry_attempt -- CONTROL: is the residual an M-CLUST effect at all?

Wave 9, DISC-DEC-041 front (a).

Why this control exists.  The fresh 18-cell validation in
`x0_asym_validate.py` finds phi_CAND BELOW the Monte-Carlo mean in all 18
cells -- including the four cells with rho <= 0.015, where phi_CAND is
numerically indistinguishable from phi_U(c) and there is essentially no
M-CLUST structure left (the whole b-block correction has switched off).
The offset there is +0.5% to +1.0%.  A sign that is positive in 18 of 18
independent cells is not plausibly noise, so part of what waves 7-9 have
been calling "the M-CLUST residual" may not be an M-CLUST effect at all,
but the finite-n error of the INHERITED master formula itself -- an
approximation `DERIVATIONS.md` sec 6 item 1 has always listed as
"empirically controlled, not fully rigorous".

This script tests that directly, on the simplest possible member of the
family: M-CLUST(1) == M-U (b=1 -> a block is a single seed -> R is exactly
the seed set, every rerouted point gets an independent uniform
destination -- wave 2's original mechanism).  For b=1, rho = c/n exactly,
phi_CAND = phi_U(c) to within 1e-6, and there is no cluster structure and
no shadowing whatsoever.  Any systematic gap between the measured phi and
phi_U(c) = int_0^1 exp(-c t^2) dt is therefore a pure finite-n property of
the master formula, with M-CLUST playing no part.

Grid: c in {10, 50, 150, 400} at n = 16384 and n = 65536, plus two cells at
n = 262144, so the n-scaling of any offset is visible (an O(1/n) or
O(1/sqrt(n) ) offset should shrink by a factor 4 or 2 per fourfold n).

OWN implementation.  Seeds: np.random.SeedSequence(20260822944) -- fresh,
not used by any predecessor or by any other script in this front
(20260822941 walk measurement, 20260822942 replication, 20260822943 the
18-cell validation).
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
from x0_asym_candidate import phi_CAND, phi_EPS

SEED_ROOT = 20260822944


def build_f_MU(n, c, rng):
    """M-U at finite n, written directly (not via the b-block loop): pi
    uniform, each point independently a seed w.p. c/n, seeds get an i.i.d.
    uniform destination.  This is exactly M-CLUST(1)."""
    f = rng.permutation(n)
    seed = rng.random(n) < (c / n)
    idx = np.flatnonzero(seed)
    if idx.size:
        f[idx] = rng.integers(0, n, idx.size)
    return f


def cyclic_fraction(f, n):
    k = int(math.ceil(math.log2(n))) + 1
    F = f
    for _ in range(k):
        F = F[F]
    mask = np.zeros(n, dtype=bool)
    mask[F] = True
    return mask.sum() / n


CELLS = ([(16384, c, 6000) for c in (10.0, 50.0, 150.0, 400.0)]
         + [(65536, c, 6000) for c in (10.0, 50.0, 150.0, 400.0)]
         + [(262144, c, 2500) for c in (50.0, 400.0)])


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "mu_baseline_control.log"), "w")

    def say(m):
        print(m, flush=True)
        log.write(m + "\n")
        log.flush()

    say("# mu_baseline_control (M-U == M-CLUST(1)) | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# own implementation, SeedSequence(%d)" % SEED_ROOT)
    say(f"{'n':>7} {'c':>7} {'n_rep':>6} | {'phi_mc':>9} {'sem':>9} | {'phi_U':>9} | "
        f"{'dev%':>7} {'z':>6} | {'n*dev':>8}")
    spawns = np.random.SeedSequence(SEED_ROOT).spawn(len(CELLS))
    out = {"seed_root": SEED_ROOT, "cells": []}
    chi2 = 0.0
    for (n, c, n_rep), ss in zip(CELLS, spawns):
        rng = np.random.default_rng(ss)
        vals = np.empty(n_rep)
        for i in range(n_rep):
            vals[i] = cyclic_fraction(build_f_MU(n, c, rng), n)
        m = float(vals.mean())
        sem = float(vals.std(ddof=1) / math.sqrt(n_rep))
        pu = phi_U(c)
        dev = 100 * (m - pu) / pu
        z = (m - pu) / sem
        chi2 += z * z
        out["cells"].append(dict(n=n, c=c, n_rep=n_rep, phi_mc=m, sem=sem,
                                 phi_U=pu, dev_pct=dev, z=z,
                                 phi_CAND_b1=phi_CAND(c, n, 1),
                                 phi_EPS_b1=phi_EPS(c, n, 1)))
        say(f"{n:7d} {c:7.1f} {n_rep:6d} | {m:9.6f} {sem:9.6f} | {pu:9.6f} | "
            f"{dev:+6.2f}% {z:+6.2f} | {n * (m - pu) / pu:8.1f}")
    say("")
    say("# chi2 (phi_U vs MC, %d M-U cells): %.2f" % (len(CELLS), chi2))
    say("# wall %.1f s" % (time.time() - t0))
    out["chi2_phiU"] = chi2
    with open(os.path.join(HERE, "mu_baseline_control_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved mu_baseline_control_results.json")
    log.close()


if __name__ == "__main__":
    main()
