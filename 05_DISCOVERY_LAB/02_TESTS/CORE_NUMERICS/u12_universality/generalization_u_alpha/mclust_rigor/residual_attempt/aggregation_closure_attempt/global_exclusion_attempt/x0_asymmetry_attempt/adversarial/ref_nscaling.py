"""REFEREE: an n-scaling test of eps that the target never performed.

Both channels of eps are pure finite-n effects, so their derived forms make a
sharp prediction about how eps moves when n is changed at fixed (b, c) -- a
direction of the parameter space in which the target's leading-order formula
was never checked, and in which a formula that merely happens to have about
the right magnitude at n = 65536 would be expected to fail.

For each of two stress cells the same (b, c) is run at n = 32768, 65536 and
131072 (rho therefore moves a lot: e.g. b=100,c=400 gives rho = 0.706 /
0.458 / 0.262).  Measured eps and its two channels are compared against the
target's leading order and against the referee's corrected one.

Seed: np.random.SeedSequence(20260823705) -- fresh.
"""
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref_formula as RF                                       # noqa: E402
from ref_mclust_mc import build_instance, cyclic_mask_square, cyclic_mask_peel  # noqa: E402

SEED = 20260823705
CELLS = [(32768, 100, 400.0, 6000), (65536, 100, 400.0, 6000),
         (131072, 100, 400.0, 4000),
         (32768, 200, 150.0, 6000), (65536, 200, 150.0, 6000),
         (131072, 200, 150.0, 4000)]


def run(n, b, c, n_rep, ss):
    rng = np.random.default_rng(ss)
    rows = np.empty((n_rep, 6))
    t0 = time.time()
    for i in range(n_rep):
        pi, inR, f = build_instance(n, b, c, rng)
        mask = cyclic_mask_square(f, n)
        if i % 500 == 0:
            assert (mask == cyclic_mask_peel(f, n)).all()
        inv = np.empty(n, dtype=np.int32)
        inv[pi] = np.arange(n, dtype=np.int32)
        Rp = np.flatnonzero(inR)
        n_rs = int((~inR[inv[Rp]]).sum())
        cyc = np.flatnonzero(mask)
        pred = np.empty(n, dtype=np.int32)
        pred[f[cyc]] = cyc
        cycR = Rp[mask[Rp]]
        nB = int(inR[pred[cycR]].sum()) if cycR.size else 0
        rows[i] = (cyc.size, Rp.size, cycR.size, cycR.size - nB, nB, n_rs)
    return rows, time.time() - t0


def boot(rows, specs, nb, rng):
    m = rows.shape[0]
    pt = {k: rows[:, a].sum() / rows[:, d].sum() for k, (a, d) in specs.items()}
    acc = {k: [] for k in specs}
    done = 0
    while done < nb:
        r = min(200, nb - done)
        idx = rng.integers(0, m, size=(r, m))
        for k, (a, d) in specs.items():
            acc[k].append(rows[:, a][idx].sum(axis=1) / rows[:, d][idx].sum(axis=1))
        done += r
    return pt, {k: float(np.std(np.concatenate(v))) for k, v in acc.items()}


def main():
    spawns = np.random.SeedSequence(SEED).spawn(len(CELLS) + 4)
    brng = np.random.default_rng(np.random.SeedSequence(SEED).spawn(50)[49])
    out = {"seed_root": SEED, "cells": []}
    print("%7s %4s %7s %7s | %-24s | %-22s | %-22s"
          % ("n", "b", "c", "rho", "eps meas / tgt / ref",
             "run-start meas/tgt/ref", "f-draw meas/tgt/ref"))
    for i, (n, b, c, nrep) in enumerate(CELLS):
        rows, wall = run(n, b, c, nrep, spawns[i])
        pt, sem = boot(rows, {"eps": (2, 1), "chA": (3, 1), "chB": (4, 1),
                              "rsfrac": (5, 1)}, 3000, brng)
        rho = RF.rho_of(c, n, b)
        rs = RF.rho_start_of(c, n, b)
        v4, T = RF.phi_V4_and_T(c, n, b)
        prs = RF.phi_runstart(c, n, b)
        eA_t, eA_r = (rs / rho) * v4, (rs / rho) * prs
        eB_t, eB_r = c * T / ((1 - rho) * n), (1 + c * T) / ((1 - rho) * n)
        row = dict(n=n, b=b, c=c, rho=rho, n_rep=nrep, wall_s=wall,
                   eps=pt["eps"], sem_eps=sem["eps"],
                   chA=pt["chA"], sem_chA=sem["chA"],
                   chB=pt["chB"], sem_chB=sem["chB"],
                   rs_frac_meas=pt["rsfrac"], rs_frac_formula=rs / rho,
                   eps_target=eA_t + eB_t, eps_referee=eA_r + eB_r,
                   chA_target=eA_t, chA_referee=eA_r,
                   chB_target=eB_t, chB_referee=eB_r)
        out["cells"].append(row)
        print("%7d %4d %7.1f %7.4f | %.3e  %.3f  %.3f | %.3e  %.3f %.3f | %.3e  %.3f %.3f"
              % (n, b, c, rho, pt["eps"], pt["eps"] / (eA_t + eB_t),
                 pt["eps"] / (eA_r + eB_r), pt["chA"], pt["chA"] / eA_t,
                 pt["chA"] / eA_r, pt["chB"], pt["chB"] / eB_t, pt["chB"] / eB_r),
              flush=True)
    with open(os.path.join(HERE, "ref_nscaling.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("# saved ref_nscaling.json")


if __name__ == "__main__":
    main()
