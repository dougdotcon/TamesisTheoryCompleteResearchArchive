"""REFEREE: independent M-CLUST(b) Monte-Carlo engine.

Adversarial review of `x0_asymmetry_attempt/ATTEMPT.md` sec 5.1-5.2.

Own implementation, written from `mclust_rigor/DERIVATION_MCLUST_FIXED.md`
sec 1 and `generalization_u_alpha/DERIVATIONS.md` sec 3.5.  Imports nothing
from `ualpha_sim.py`, `mclust_validate.py`, `mclust_residual_validate.py`,
`mclust_aggregation_validate.py`, `mclust_global_validate.py`,
`x0_asymmetry_walk_measure.py` or `x0_asym_validate.py`.

--------------------------------------------------------------------------
DELIBERATE STRATEGY DIFFERENCE vs. the target's stage-B eps measurement
--------------------------------------------------------------------------
The target measures  eps := P(x0 on a cycle of f | x0 in R)  by
rejection-sampling one x0 inside R per walk and SIMULATING THE WALK step by
step with a visited-stamp array, counting the two terminal codes ST_NORM_X0
and ST_RR_X0 over 3-5 x 10^5 walks per cell (157-483 cyclic events per
cell).

This referee never simulates a walk.  It builds the whole functional graph
f, computes the EXACT cyclic set of f, and reads eps off directly as

        eps_hat = sum_instances |cyc & R| / sum_instances |R|

which uses EVERY point of R in every instance rather than one sampled x0
per walk.  At n = 65536 that is ~3 x 10^4 conditionally-sampled points per
instance instead of 1, so the same wall time buys ~10^2 x more events.  It
also removes, by construction, every possible walk-bookkeeping bug (visited
stamps, chain handling, arc-start accounting, step budget), because there
is no walk.

The two channels of eps are separated exactly as well: for a cyclic x, its
unique predecessor ON THE CYCLE is y = f^-1(x) restricted to the cyclic set.

    y not in R  =>  f(y) = pi(y), so x was reached by a NORMAL pi-step
                    (only possible if pi^-1(x) not in R, i.e. x is a RUN
                    START) -- the target's `n_norm_x0` channel;
    y in R      =>  x was reached by a uniform f-DRAW -- the target's
                    `n_rr_x0` channel.

Cyclic set: primary algorithm is iterated squaring with an ADAPTIVE stop
(iterate F <- F[F] until the image mask stops shrinking, then one more),
audited on a configurable fraction of instances by a completely different
algorithm (vectorised in-degree peeling).  `selftest` additionally checks
both against brute-force orbit following on random small maps, and checks
the MECHANISM construction against two independent definitions of R (the
pi-cycle offset construction and the backward pi^-k membership test).

Seeds: np.random.SeedSequence(20260823701 / 702 / 703) -- never used by any
document in this lineage (checked against 20260822018, 918302033,
720330339, 20260822901-904, 20260822910-911, 20260822941-945).
"""
import argparse
import json
import math
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ mechanism
def build_instance(n, b, c, rng):
    """Return (pi, inR, f).

    M-CLUST(b), verbatim from DERIVATION_MCLUST_FIXED.md sec 1:
      * pi uniform permutation of [n];
      * each point independently a SEED with probability c/n;
      * block of a seed s = {s, pi(s), ..., pi^(b-1)(s)};
      * R = union of the blocks;
      * EVERY point of R (seed or shadowed interior member alike) gets one
        i.i.d. Uniform[n] destination, fixed in advance;
      * f = pi off R.
    """
    pi = rng.permutation(n).astype(np.int32)
    seeds = np.flatnonzero(rng.random(n) < (c / n)).astype(np.int32)
    inR = np.zeros(n, dtype=bool)
    if seeds.size:
        cur = seeds
        inR[cur] = True
        for _ in range(b - 1):
            cur = pi[cur]
            inR[cur] = True
    f = pi.copy()
    Rpts = np.flatnonzero(inR).astype(np.int32)
    if Rpts.size:
        f[Rpts] = rng.integers(0, n, Rpts.size, dtype=np.int32)
    return pi, inR, f


def R_by_cycle_offsets(pi, seeds, b, n):
    """INDEPENDENT construction of R, used only by the selftest.

    Decomposes pi into cycles, labels every point by (cycle, position), and
    marks positions p, p+1, ..., p+b-1 (mod cycle length) for each seed --
    i.e. uses the algebraic meaning of "b points forward along pi" instead of
    iterating the permutation b-1 times.
    """
    seen = np.zeros(n, dtype=bool)
    inR = np.zeros(n, dtype=bool)
    seedset = np.zeros(n, dtype=bool)
    seedset[seeds] = True
    for start in range(n):
        if seen[start]:
            continue
        cyc = []
        x = start
        while not seen[x]:
            seen[x] = True
            cyc.append(x)
            x = int(pi[x])
        L = len(cyc)
        for j, v in enumerate(cyc):
            if seedset[v]:
                for k in range(min(b, L)):
                    inR[cyc[(j + k) % L]] = True
    return inR


def R_by_backward_test(pi, seeds, b, n):
    """INDEPENDENT construction of R, used only by the selftest.

    z in R  iff  some pi^-k(z), k = 0..b-1, is a seed.  Implemented by
    walking BACKWARDS along pi from every point (the opposite direction from
    build_instance), which is the literal reading of the shadowing statement
    in DERIVATION_MCLUST_FIXED.md sec 1.
    """
    inv = np.empty(n, dtype=np.int32)
    inv[pi] = np.arange(n, dtype=np.int32)
    seedset = np.zeros(n, dtype=bool)
    seedset[seeds] = True
    cur = np.arange(n, dtype=np.int32)
    inR = seedset.copy()
    for _ in range(b - 1):
        cur = inv[cur]
        inR |= seedset[cur]
    return inR


# ------------------------------------------------------------------ cyclic set
def cyclic_mask_square(f, n):
    """Image of f^(2^k) once the image has stopped shrinking = cycle set."""
    F = f
    prev = n + 1
    mask = np.zeros(n, dtype=bool)
    for _ in range(64):
        mask[:] = False
        mask[F] = True
        cnt = int(mask.sum())
        if cnt == prev:
            break
        prev = cnt
        F = F[F]
    else:                                              # pragma: no cover
        raise RuntimeError("squaring did not converge")
    return mask


def cyclic_mask_peel(f, n):
    """AUDITOR: vectorised in-degree peeling.  A point survives iff it is on
    a cycle.  Completely different algorithm from squaring."""
    indeg = np.bincount(f, minlength=n).astype(np.int32)
    alive = np.ones(n, dtype=bool)
    frontier = np.flatnonzero(indeg == 0).astype(np.int32)
    while frontier.size:
        alive[frontier] = False
        tgt = f[frontier]
        np.subtract.at(indeg, tgt, 1)
        nxt = tgt[(indeg[tgt] == 0) & alive[tgt]]
        frontier = np.unique(nxt)
    return alive


def cyclic_mask_brute(f, n):
    """AUDITOR for tiny n: x is cyclic iff its forward orbit returns to x."""
    out = np.zeros(n, dtype=bool)
    for x in range(n):
        y = int(f[x])
        for _ in range(n + 2):
            if y == x:
                out[x] = True
                break
            y = int(f[y])
    return out


# ------------------------------------------------------------------ selftest
def selftest():
    rng = np.random.default_rng(20260823700)
    for _ in range(300):
        n = int(rng.integers(3, 80))
        f = rng.integers(0, n, n, dtype=np.int32)
        a = cyclic_mask_square(f, n)
        b_ = cyclic_mask_peel(f, n)
        d = cyclic_mask_brute(f, n)
        assert (a == d).all() and (b_ == d).all(), n
    print("  cyclic set: squaring == peeling == brute force on 300 random maps  OK")

    for _ in range(120):
        n = int(rng.integers(6, 200))
        b = int(rng.integers(1, 12))
        c = float(rng.uniform(0.5, 6.0))
        pi = rng.permutation(n).astype(np.int32)
        seeds = np.flatnonzero(rng.random(n) < (c / n)).astype(np.int32)
        inR = np.zeros(n, dtype=bool)
        if seeds.size:
            cur = seeds
            inR[cur] = True
            for _ in range(b - 1):
                cur = pi[cur]
                inR[cur] = True
        m1 = R_by_cycle_offsets(pi, seeds, b, n)
        m2 = R_by_backward_test(pi, seeds, b, n)
        assert (inR == m1).all(), ("cycle-offset R mismatch", n, b)
        assert (inR == m2).all(), ("backward R mismatch", n, b)
    print("  R construction: forward-iteration == pi-cycle-offset == backward"
          " pi^-k test on 120 random instances  OK")

    # shadowing lemma, empirically: an interior block member has pi^-1 in R
    rng2 = np.random.default_rng(20260823700 + 1)
    pi, inR, f = build_instance(4096, 20, 40.0, rng2)
    inv = np.empty(4096, dtype=np.int32)
    inv[pi] = np.arange(4096, dtype=np.int32)
    Rp = np.flatnonzero(inR)
    run_start = Rp[~inR[inv[Rp]]]
    print("  |R|=%d run starts=%d  (rho_start*n predicted %.1f)"
          % (Rp.size, run_start.size, 40.0 * (1 - 40.0 / 4096) ** 20))

    # cross-check the eps channel split against literal orbit following
    for trial in range(6):
        n = 2048
        rng3 = np.random.default_rng(20260823700 + 10 + trial)
        pi, inR, f = build_instance(n, 8, 30.0, rng3)
        mask = cyclic_mask_square(f, n)
        cyc = np.flatnonzero(mask)
        pred = np.full(n, -1, dtype=np.int32)
        pred[f[cyc]] = cyc
        for x in cyc[inR[cyc]][:20]:
            # follow the orbit back to x and check who the last hop was
            y = int(f[x])
            prevy = int(x)
            while y != x:
                prevy = y
                y = int(f[y])
            assert prevy == pred[x], ("pred mismatch", x)
    print("  cycle-predecessor map matches literal orbit following  OK")
    print("selftest OK")


# ------------------------------------------------------------------ one cell
def run_cell(n, b, c, n_rep, ss, audit_every=100):
    rng = np.random.default_rng(ss)
    rows = np.empty((n_rep, 6), dtype=np.float64)
    n_audit = 0
    t0 = time.time()
    for i in range(n_rep):
        pi, inR, f = build_instance(n, b, c, rng)
        mask = cyclic_mask_square(f, n)
        if i % audit_every == 0:
            assert (mask == cyclic_mask_peel(f, n)).all(), (n, b, c, i)
            n_audit += 1
        cyc = np.flatnonzero(mask)
        nR = int(inR.sum())
        cycR = mask & inR
        n_cycR = int(cycR.sum())
        if n_cycR:
            pred = np.empty(n, dtype=np.int32)
            pred[f[cyc]] = cyc
            xs = np.flatnonzero(cycR)
            ys = pred[xs]
            n_chB = int(inR[ys].sum())          # predecessor in R -> f-draw
            n_chA = n_cycR - n_chB              # predecessor off R -> pi-step
        else:
            n_chA = n_chB = 0
        rows[i] = (cyc.size, nR, n_cycR, n_chA, n_chB, n)
    return rows, time.time() - t0, n_audit


def boot_ratios(rows, specs, n_boot, rng, chunk=200):
    """Cluster (over-instance) bootstrap of several sum(num)/sum(den) ratios,
    resampled JOINTLY so derived quantities stay correlated."""
    m = rows.shape[0]
    point, sem = {}, {}
    nums = {k: rows[:, a] for k, (a, d) in specs.items()}
    dens = {k: (rows[:, d] if isinstance(d, int) else np.full(m, float(d)))
            for k, (a, d) in specs.items()}
    for k in specs:
        point[k] = nums[k].sum() / dens[k].sum()
    reps = {k: [] for k in specs}
    done = 0
    while done < n_boot:
        r = min(chunk, n_boot - done)
        idx = rng.integers(0, m, size=(r, m))
        for k in specs:
            reps[k].append(nums[k][idx].sum(axis=1) / dens[k][idx].sum(axis=1))
        done += r
    for k in specs:
        sem[k] = float(np.std(np.concatenate(reps[k])))
    return point, sem


GRID18 = ([(32768, 8, c) for c in (10.0, 40.0, 160.0)]
          + [(65536, 50, c) for c in (10.0, 50.0, 150.0, 400.0)]
          + [(65536, 100, c) for c in (10.0, 50.0, 150.0, 400.0)]
          + [(65536, 200, c) for c in (5.0, 20.0, 60.0, 150.0)]
          + [(65536, 300, 150.0), (65536, 100, 600.0), (65536, 400, 100.0)])

STRESS6 = [(65536, 100, 400.0), (65536, 300, 150.0), (65536, 100, 600.0),
           (65536, 400, 100.0), (65536, 50, 400.0), (65536, 200, 150.0)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", choices=("g18", "s6"), default="g18")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--nrep", type=int, default=8000)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--only", type=int, default=-1,
                    help="run only cell index (for parallel launching)")
    ap.add_argument("--nboot", type=int, default=4000)
    args = ap.parse_args()

    cells = GRID18 if args.grid == "g18" else STRESS6
    spawns = np.random.SeedSequence(args.seed).spawn(len(cells) + 8)
    boot_rng = np.random.default_rng(np.random.SeedSequence(args.seed).spawn(64)[63])

    idxs = range(len(cells)) if args.only < 0 else [args.only]
    out = {"seed_root": args.seed, "grid": args.grid, "n_rep": args.nrep,
           "cells": []}
    for i in idxs:
        n, b, c = cells[i]
        rows, wall, n_audit = run_cell(n, b, c, args.nrep, spawns[i])
        specs = {
            "phi": (0, 5),          # sum|cyc| / sum n
            "eps": (2, 1),          # sum|cyc & R| / sum|R|
            "chA": (3, 1),
            "chB": (4, 1),
            "rho": (1, 5),
        }
        pt, sem = boot_ratios(rows, specs, args.nboot, boot_rng)
        # phi_notR = (sum|cyc| - sum|cyc&R|) / (sum n - sum |R|)
        num = rows[:, 0] - rows[:, 2]
        den = rows[:, 5] - rows[:, 1]
        extra = np.column_stack([rows, num, den])
        pt2, sem2 = boot_ratios(extra, {"phiA": (6, 7)}, args.nboot, boot_rng)
        row = dict(n=n, b=b, c=c, n_rep=args.nrep,
                   rho_formula=1.0 - (1.0 - c / n) ** b,
                   rho_measured=pt["rho"],
                   phi_mc=pt["phi"], sem_phi=sem["phi"],
                   phi_mc_plain=float(rows[:, 0].mean() / n),
                   sem_phi_plain=float(rows[:, 0].std(ddof=1) / math.sqrt(args.nrep) / n),
                   eps=pt["eps"], sem_eps=sem["eps"],
                   chA=pt["chA"], sem_chA=sem["chA"],
                   chB=pt["chB"], sem_chB=sem["chB"],
                   phi_notR=pt2["phiA"], sem_phi_notR=sem2["phiA"],
                   n_cycR_total=float(rows[:, 2].sum()),
                   n_chA_total=float(rows[:, 3].sum()),
                   n_chB_total=float(rows[:, 4].sum()),
                   n_audit=n_audit, wall_s=wall)
        out["cells"].append(row)
        print("n=%6d b=%3d c=%6.1f rho=%.4f | phi=%.6f+-%.6f | eps=%.3e+-%.2e "
              "(events %d = A %d + B %d) | phi(x0 notin R)=%.6f | %.0fs"
              % (n, b, c, row["rho_formula"], row["phi_mc"], row["sem_phi"],
                 row["eps"], row["sem_eps"], row["n_cycR_total"],
                 row["n_chA_total"], row["n_chB_total"], row["phi_notR"], wall),
              flush=True)
    fn = os.path.join(HERE, "ref_mc_%s.json" % args.tag)
    with open(fn, "w") as fh:
        json.dump(out, fh, indent=2)
    print("# saved", fn)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    else:
        main()
