"""REFEREE: direct test of the TWO heuristic steps inside the target's eps.

Adversarial review of `x0_asymmetry_attempt/ATTEMPT.md` sec 5.2.

The target's leading-order eps is

    eps = (rho_start/rho) * phi_cond          <-- RUN-START channel
        + (c/((1-rho) n)) * T                 <-- F-DRAW channel

with two separate assertions:

  (a) "conditionally on being a run start, x0 is a live target since t = 0
      with the same elevation as any arc start, hence its return probability
      is at leading order the same phi_cond = phi_V4";
  (b) E[#f-draws] = (c/(1-rho)) * T.

Both are testable EXACTLY, with no walk simulation, from the functional
graph alone:

  (a)  P(cyclic via a pi-step | x0 is a run start)
         = #{x in R : pi^-1(x) not in R, x cyclic, cycle-pred(x) not in R}
           / #{x in R : pi^-1(x) not in R}
       (a cyclic x in R whose cycle predecessor y is not in R satisfies
        f(y) = pi(y) = x, so x is necessarily a run start; conversely a run
        start reached by a pi-step has its cycle predecessor off R).
       The target asserts this equals phi_cond; measure it and compare
       against BOTH phi_cond and the referee's corrected prediction
       phi_runstart (see ref_formula.phi_runstart).

  (b)  P(cyclic via an f-draw | x0 in R)
         = #{x in R : x cyclic, cycle-pred(x) in R} / |R|
       equals E[#f-draws]/n at leading order, so
       E[#f-draws]_measured = n * that ratio.
       Compare against  c T/(1-rho)  (target) and  (1 + c T)/(1-rho)
       (referee: the target forgets the chain of draws the walk makes AT x0
       itself before it moves anywhere).

Own implementation; reuses only this referee's own ref_mclust_mc engine.
Seed: np.random.SeedSequence(20260823704) -- fresh.
"""
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref_formula as RF                                    # noqa: E402
from ref_mclust_mc import build_instance, cyclic_mask_square, cyclic_mask_peel  # noqa: E402

SEED = 20260823704

CELLS = [(32768, 8, 10.0), (32768, 8, 160.0),
         (65536, 50, 10.0), (65536, 200, 5.0),
         (65536, 100, 150.0),
         (65536, 50, 400.0), (65536, 200, 150.0), (65536, 100, 400.0),
         (65536, 400, 100.0), (65536, 300, 150.0), (65536, 100, 600.0)]


def run_cell(n, b, c, n_rep, ss, audit_every=200):
    rng = np.random.default_rng(ss)
    rows = np.empty((n_rep, 8))
    t0 = time.time()
    for i in range(n_rep):
        pi, inR, f = build_instance(n, b, c, rng)
        mask = cyclic_mask_square(f, n)
        if i % audit_every == 0:
            assert (mask == cyclic_mask_peel(f, n)).all()
        inv = np.empty(n, dtype=np.int32)
        inv[pi] = np.arange(n, dtype=np.int32)
        Rp = np.flatnonzero(inR)
        is_run_start = ~inR[inv[Rp]]                 # pi^-1(x) not in R
        n_rs = int(is_run_start.sum())
        cyc = np.flatnonzero(mask)
        pred = np.empty(n, dtype=np.int32)
        pred[f[cyc]] = cyc
        cycR = Rp[mask[Rp]]
        if cycR.size:
            predR = inR[pred[cycR]]
            n_chB = int(predR.sum())
            n_chA = cycR.size - n_chB
            # all channel-A points must be run starts:
            assert not inR[inv[cycR[~predR]]].any()
        else:
            n_chA = n_chB = 0
        rows[i] = (n, Rp.size, n_rs, cyc.size, cycR.size, n_chA, n_chB,
                   int((mask & ~inR).sum()))
    return rows, time.time() - t0


def boot(rows, specs, n_boot, rng, chunk=200):
    m = rows.shape[0]
    nums = {k: rows[:, a] for k, (a, d) in specs.items()}
    dens = {k: rows[:, d] for k, (a, d) in specs.items()}
    point = {k: nums[k].sum() / dens[k].sum() for k in specs}
    acc = {k: [] for k in specs}
    done = 0
    while done < n_boot:
        r = min(chunk, n_boot - done)
        idx = rng.integers(0, m, size=(r, m))
        for k in specs:
            acc[k].append(nums[k][idx].sum(axis=1) / dens[k][idx].sum(axis=1))
        done += r
    sem = {k: float(np.std(np.concatenate(acc[k]))) for k in specs}
    return point, sem


def main():
    n_rep = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    spawns = np.random.SeedSequence(SEED).spawn(len(CELLS) + 4)
    brng = np.random.default_rng(np.random.SeedSequence(SEED).spawn(40)[39])
    out = {"seed_root": SEED, "n_rep": n_rep, "cells": []}
    print("%6s %4s %7s %7s | %-30s | %-42s | %s"
          % ("n", "b", "c", "rho",
             "P(cyc via pi | run start)", "E[#f-draws] measured / target / referee",
             "phi_cond meas/model"))
    for i, (n, b, c) in enumerate(CELLS):
        rows, wall = run_cell(n, b, c, n_rep, spawns[i])
        # extra derived columns
        ex = np.column_stack([rows, rows[:, 0] - rows[:, 1],      # 8: n - |R|
                              rows[:, 3] - rows[:, 4]])           # 9: |cyc \ R|
        specs = {"p_rs": (5, 2),        # channel-A events / #run starts
                 "p_fd": (6, 1),        # channel-B events / |R|
                 "eps": (4, 1),
                 "phiA": (9, 8),
                 "phi": (3, 0),
                 "rs_frac": (2, 1)}
        pt, sem = boot(ex, specs, 3000, brng)
        rho = RF.rho_of(c, n, b)
        v4, T = RF.phi_V4_and_T(c, n, b)
        P = 1.0 / (1.0 - rho)
        prs_model = RF.phi_runstart(c, n, b)
        ndraw_meas = n * pt["p_fd"]
        ndraw_meas_sem = n * sem["p_fd"]
        ndraw_tgt = c * T / (1.0 - rho)
        ndraw_ref = (1.0 + c * T) / (1.0 - rho)
        row = dict(n=n, b=b, c=c, rho=rho, n_rep=n_rep, wall_s=wall,
                   p_runstart_meas=pt["p_rs"], sem_p_runstart=sem["p_rs"],
                   phi_cond_meas=pt["phiA"], sem_phi_cond=sem["phiA"],
                   phi_V4_model=v4, phi_runstart_model=prs_model,
                   ratio_meas_over_phicond=pt["p_rs"] / pt["phiA"],
                   ratio_meas_over_phirs=pt["p_rs"] / prs_model,
                   ndraw_meas=ndraw_meas, ndraw_sem=ndraw_meas_sem,
                   ndraw_target=ndraw_tgt, ndraw_referee=ndraw_ref,
                   eps_meas=pt["eps"], sem_eps=sem["eps"],
                   phi_mc=pt["phi"], sem_phi=sem["phi"],
                   rs_frac_meas=pt["rs_frac"],
                   rs_frac_formula=RF.rho_start_of(c, n, b) / rho, T=T, P=P)
        out["cells"].append(row)
        print("%6d %4d %7.1f %7.4f | %.5f+-%.5f (/phi_cond=%.3f /phi_rs=%.3f) | "
              "%7.2f+-%.2f  %7.2f  %7.2f | %.5f / %.5f  %6.1fs"
              % (n, b, c, rho, pt["p_rs"], sem["p_rs"],
                 pt["p_rs"] / pt["phiA"], pt["p_rs"] / prs_model,
                 ndraw_meas, ndraw_meas_sem, ndraw_tgt, ndraw_ref,
                 pt["phiA"], v4, wall), flush=True)
    with open(os.path.join(HERE, "ref_channel_probe.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("# saved ref_channel_probe.json")


if __name__ == "__main__":
    main()
