"""REFEREE: is the referee's eps estimator comparable to the target's?

The target draws 25 x0 uniformly INSIDE R per instance, so its stage-B
estimator converges to the MEAN OF RATIOS

        E[ |cyc & R| / |R| ]

whereas the referee's default estimator is the RATIO OF SUMS

        E[ |cyc & R| ] / E[ |R| ].

|R| fluctuates from instance to instance (its seed count is ~Poisson(c)), and
|cyc & R| is correlated with it, so the two differ at O(CV^2).  This script
computes BOTH on the same instances so the comparison in the report is
apples-to-apples.  Also reports the corresponding two estimators of phi and
of each channel.

Seed: np.random.SeedSequence(20260823707) -- fresh.
"""
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ref_mclust_mc import build_instance, cyclic_mask_square           # noqa: E402
import ref_formula as RF                                              # noqa: E402

SEED = 20260823707
CELLS = [(65536, 400, 100.0, 5000), (65536, 100, 400.0, 5000),
         (65536, 100, 600.0, 5000), (32768, 8, 10.0, 5000)]


def main():
    spawns = np.random.SeedSequence(SEED).spawn(len(CELLS) + 4)
    brng = np.random.default_rng(np.random.SeedSequence(SEED).spawn(30)[29])
    out = {"seed_root": SEED, "cells": []}
    print("%6s %4s %7s | %-24s | %-24s | %8s | %8s"
          % ("n", "b", "c", "eps ratio-of-sums (referee)",
             "eps mean-of-ratios (target-like)", "rel diff", "CV(|R|)"))
    for i, (n, b, c, nrep) in enumerate(CELLS):
        rng = np.random.default_rng(spawns[i])
        X = np.empty(nrep)     # |cyc & R|
        Y = np.empty(nrep)     # |R|
        t0 = time.time()
        for j in range(nrep):
            pi, inR, f = build_instance(n, b, c, rng)
            mask = cyclic_mask_square(f, n)
            X[j] = int((mask & inR).sum())
            Y[j] = int(inR.sum())
        ros = X.sum() / Y.sum()
        mor = float((X / Y).mean())
        # cluster bootstrap of both
        reps_r, reps_m = [], []
        done = 0
        while done < 3000:
            r = min(200, 3000 - done)
            idx = brng.integers(0, nrep, size=(r, nrep))
            reps_r.append(X[idx].sum(axis=1) / Y[idx].sum(axis=1))
            reps_m.append((X[idx] / Y[idx]).mean(axis=1))
            done += r
        sr = float(np.std(np.concatenate(reps_r)))
        sm = float(np.std(np.concatenate(reps_m)))
        cv = float(Y.std(ddof=1) / Y.mean())
        row = dict(n=n, b=b, c=c, n_rep=nrep, eps_ratio_of_sums=ros, sem_ros=sr,
                   eps_mean_of_ratios=mor, sem_mor=sm, cv_R=cv,
                   wall_s=time.time() - t0)
        out["cells"].append(row)
        print("%6d %4d %7.1f | %.5e +- %.1e | %.5e +- %.1e | %+7.3f%% | %7.4f"
              % (n, b, c, ros, sr, mor, sm, 100 * (mor - ros) / ros, cv),
              flush=True)
    with open(os.path.join(HERE, "ref_estimator_check.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("# saved ref_estimator_check.json")


if __name__ == "__main__":
    main()
