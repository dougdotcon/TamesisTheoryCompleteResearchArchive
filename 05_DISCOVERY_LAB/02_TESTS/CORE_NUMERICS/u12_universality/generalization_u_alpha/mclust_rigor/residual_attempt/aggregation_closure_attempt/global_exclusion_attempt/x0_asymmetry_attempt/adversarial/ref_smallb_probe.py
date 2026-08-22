"""REFEREE: eps at SMALL b, including b = 1 (M-CLUST(1) = M-U).

At small b almost every point of R is a run start (rho_start/rho -> 1 - c/n
as b -> 1), so eps is dominated by the run-start channel and the referee's
correction factor phi_runstart/phi_cond is at its largest (0.75-0.82 at
small c).  This is the cleanest possible separation of the two competing
leading-order accounts of that channel, and it is a corner of the parameter
space the target never measured.

Seed: np.random.SeedSequence(20260823706) -- fresh.
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

SEED = 20260823706
CELLS = [(16384, 1, 10.0, 20000), (16384, 1, 50.0, 20000),
         (16384, 1, 200.0, 20000), (16384, 2, 50.0, 20000),
         (16384, 4, 50.0, 20000), (16384, 8, 50.0, 20000),
         (65536, 1, 50.0, 12000), (65536, 2, 400.0, 12000)]


def main():
    spawns = np.random.SeedSequence(SEED).spawn(len(CELLS) + 4)
    brng = np.random.default_rng(np.random.SeedSequence(SEED).spawn(50)[49])
    out = {"seed_root": SEED, "cells": []}
    print("%7s %4s %7s %8s | %-11s %-11s | %-30s | %-24s"
          % ("n", "b", "c", "rho", "rs frac", "(formula)",
             "run-start rate meas/tgt/ref", "eps meas/tgt/ref"))
    for i, (n, b, c, nrep) in enumerate(CELLS):
        rng = np.random.default_rng(spawns[i])
        rows = np.empty((nrep, 6))
        t0 = time.time()
        for j in range(nrep):
            pi, inR, f = build_instance(n, b, c, rng)
            mask = cyclic_mask_square(f, n)
            if j % 1000 == 0:
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
            rows[j] = (cyc.size, Rp.size, cycR.size, cycR.size - nB, nB, n_rs)
        m = nrep
        specs = {"eps": (2, 1), "chA_over_rs": (3, 5), "chB": (4, 1),
                 "rsfrac": (5, 1), "phi": (0, None)}
        pt, sem = {}, {}
        acc = {k: [] for k in specs}
        for k, (a, d) in specs.items():
            num = rows[:, a]
            den = rows[:, d] if d is not None else np.full(m, float(n))
            pt[k] = num.sum() / den.sum()
        done = 0
        while done < 3000:
            r = min(200, 3000 - done)
            idx = brng.integers(0, m, size=(r, m))
            for k, (a, d) in specs.items():
                num = rows[:, a]
                den = rows[:, d] if d is not None else np.full(m, float(n))
                acc[k].append(num[idx].sum(axis=1) / den[idx].sum(axis=1))
            done += r
        for k in specs:
            sem[k] = float(np.std(np.concatenate(acc[k])))
        rho = RF.rho_of(c, n, b)
        rs = RF.rho_start_of(c, n, b)
        v4, T = RF.phi_V4_and_T(c, n, b)
        prs = RF.phi_runstart(c, n, b)
        # P(cyclic via pi-step | run start) directly
        eA_t, eA_r = (rs / rho) * v4, (rs / rho) * prs
        eB_t, eB_r = c * T / ((1 - rho) * n), (1 + c * T) / ((1 - rho) * n)
        row = dict(n=n, b=b, c=c, rho=rho, n_rep=nrep, wall_s=time.time() - t0,
                   rs_frac_meas=pt["rsfrac"], rs_frac_formula=rs / rho,
                   p_runstart_meas=pt["chA_over_rs"], sem_p_runstart=sem["chA_over_rs"],
                   phi_V4=v4, phi_runstart=prs,
                   eps=pt["eps"], sem_eps=sem["eps"],
                   eps_target=eA_t + eB_t, eps_referee=eA_r + eB_r,
                   phi_mc=pt["phi"], sem_phi=sem["phi"])
        out["cells"].append(row)
        print("%7d %4d %7.1f %8.5f | %.5f     %.5f     | %.5f+-%.5f  %.3f  %.3f | %.4e  %.3f  %.3f"
              % (n, b, c, rho, pt["rsfrac"], rs / rho,
                 pt["chA_over_rs"], sem["chA_over_rs"],
                 pt["chA_over_rs"] / v4, pt["chA_over_rs"] / prs,
                 pt["eps"], pt["eps"] / (eA_t + eB_t), pt["eps"] / (eA_r + eB_r)),
              flush=True)
    with open(os.path.join(HERE, "ref_smallb_probe.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("# saved ref_smallb_probe.json")
    print("# columns 'run-start rate meas/tgt/ref' are P(cyclic via a pi-step |")
    print("#   x0 is a run start) divided by phi_V4 (the target's claim) and by")
    print("#   phi_runstart (the referee's).  1.000 = the claim is right.")


if __name__ == "__main__":
    main()
