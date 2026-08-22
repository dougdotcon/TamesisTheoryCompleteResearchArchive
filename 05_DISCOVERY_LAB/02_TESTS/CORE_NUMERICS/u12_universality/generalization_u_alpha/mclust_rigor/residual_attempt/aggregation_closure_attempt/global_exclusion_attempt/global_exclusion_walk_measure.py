"""global_exclusion_attempt -- stage 1: direct walk-level measurement of the
per-target-set closure density, split by ARC DEPTH, to test the hypothesis
named in aggregation_closure_attempt/ATTEMPT.md sec 7.2:

  "the effective candidate pool for pi(x) at visited-mass t has size
  ~ n(1-t) [not just n], because order t*n points (not just the b-1 in
  x's own local window) have already been consumed as images of pi by
  PRIOR NORMAL STEPS, over the WHOLE walk -- so the per-target density
  relevant to H(t) should scale like 1/[(1-t)n], not 1/n."

OWN implementation. Does not import mclust_walk_diagnostic.py,
mclust_residual_v4.py, mclust_residual_v5.py, mclust_aggregation_validate.py,
or lemma_direct_test_v3_fullscale.py -- re-derives the mechanism build and
walk loop from DERIVATION_MCLUST_FIXED.md sec 1 / aggregation_closure_attempt
sec 2 directly (own reading), extended with explicit tracking of:

  - K: number of LIVE arc-starts (x0 + surviving-reroute targets not yet
    closed onto) at the moment of each event -- NOT tracked by any
    predecessor script.
  - arc_depth: number of consecutive NORMAL pi-steps taken on the CURRENT
    arc so far (0 = standing exactly on an arc-start; d = d normal steps
    since the arc began). This is the quantity that controls whether x's
    own local backward window (b-1 points) OVERLAPS the walk's own visited
    history (overlap is total once arc_depth >= b-1) -- the mechanism this
    front's own sec-by-sec derivation (see ATTEMPT.md sec 2) argues should
    NOT change the R-elevation P (a pure marks-conditioning fact, argued
    analytically to be depth-independent) but DOES change the raw pool-size
    subtraction by a max O(b/n) amount. This script tests that prediction
    directly instead of trusting the algebra alone.

For every NORMAL step (not reroute steps -- reroute steps are governed by
q_CLUST(s), already reconfirmed correct by residual_attempt sec 3.1, and are
out of scope here), we log:

    s_before   = n_visited/n immediately before the step
    K_before   = number of live arc-starts immediately before the step
    depth_before = arc_depth of the CURRENT position (the point taking the
                   step), i.e. of x, not of the destination
    p0         = K_before / ((1-s_before)*n)   [naive, non-elevated model:
                 K live targets uniformly spread over the (1-s)n remaining
                 not-yet-pi-consumed pool, no R-elevation at all]
    hit        = 1 if the step closes (dest already visited), else 0

Aggregated on the fly into 2D histograms over (s-bin, depth-bin) of
sum(hit), sum(p0), count -- NOT into a per-event list (memory: tens of
millions of normal steps per run otherwise). The empirical elevation
estimate per bin is a Horvitz-Thompson-style ratio sum(hit)/sum(p0), valid
even though K and s vary within a bin (each event's own p0 already accounts
for its own K,s).

Seeds: SeedSequence(20260822910) -- fresh, not reused from residual_attempt
(918302033, 720330339) or aggregation_closure_attempt (20260822901-904).
"""
import json
import math
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def build_instance(n, b, c, rng):
    """Own implementation of M-CLUST(b) (re-read from DERIVATION_MCLUST_FIXED.md
    sec 1 directly, not copied from any predecessor script)."""
    pi = rng.permutation(n).astype(np.int64)
    in_R = rng.random(n) < c / n
    cur = np.flatnonzero(in_R)
    for _ in range(b - 1):
        cur = pi[cur]
        in_R[cur] = True
    R_mask = in_R
    f = pi.copy()
    R_idx = np.flatnonzero(R_mask)
    if R_idx.size:
        f[R_idx] = rng.integers(0, n, R_idx.size)
    return pi, R_mask, f


def rho_of(c, n, b):
    return 1.0 - (1.0 - c / n) ** b


# Each walk's trajectory terminates at its FIRST closure event -- so a
# single walk contributes exactly ONE "hit" (closure) total, however many
# thousands of "fresh" (non-hit) normal steps it logs along the way. A fine
# 15-bin depth histogram (first version of this script) starved most bins
# of hits (a handful each, from ~2500 walks) and gave unusable sem. The
# hypothesis under test (ATTEMPT.md sec 2/7.2 recap: elevation should be
# roughly CONSTANT across depth, since it is argued to be a pure
# marks-conditioning fact independent of window/history overlap; only a
# tiny O(b/n) pool-size term should depend on depth) only needs TWO depth
# categories to test at reasonable power: SHALLOW (arc_depth < b-1, x's own
# local window not yet fully absorbed into the walk's own visited history)
# vs DEEP (arc_depth >= b-1, window fully absorbed). The threshold b-1 is
# cell-specific (depends on b), so depth_bin takes b_minus_1 explicitly.
N_DEPTH_BINS = 2   # 0 = shallow (depth < b-1), 1 = deep (depth >= b-1)
N_S_BINS = 8


def depth_bin(d, b_minus_1):
    return 0 if d < b_minus_1 else 1


def run_walk(n, pi, R_mask, f, x0, max_steps, b_minus_1,
             hit_hist, p0_hist, cnt_hist, s_edges):
    """Single trajectory. Accumulates into the (s_bin, depth_bin) histograms
    in place for every NORMAL step (fresh or closure). Returns status."""
    visited = np.zeros(n, dtype=bool)
    visited[x0] = True
    n_visited = 1
    K = 1  # x0 itself is a live arc-start
    arc_depth = 0
    cur = x0
    for _ in range(max_steps):
        in_r = R_mask[cur]
        dest = f[cur] if in_r else pi[cur]
        if not in_r:
            s_before = n_visited / n
            p0 = K / (max(1e-9, 1.0 - s_before) * n)
            sbin = min(int(s_before * N_S_BINS), N_S_BINS - 1)
            dbin = depth_bin(arc_depth, b_minus_1)
            hit = 1 if visited[dest] else 0
            hit_hist[sbin, dbin] += hit
            p0_hist[sbin, dbin] += p0
            cnt_hist[sbin, dbin] += 1
        if visited[dest]:
            status = "CYCLIC" if dest == x0 else "KILLED"
            return status, n_visited
        if in_r:
            if R_mask[dest]:
                pass  # continue: chain still inside R, arc identity unresolved
            else:
                K += 1
                arc_depth = 0  # dest becomes a fresh arc-start
        else:
            arc_depth += 1
        visited[dest] = True
        n_visited += 1
        cur = dest
    return "TRUNCATED", n_visited


def main():
    t0 = time.time()
    log_path = os.path.join(HERE, "global_exclusion_walk_measure.log")
    log = open(log_path, "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# global_exclusion_walk_measure | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# own implementation, SeedSequence(20260822910), fresh")

    # n_walks chosen to give roughly comparable wall time per cell (~90-100s)
    # given the measured per-walk cost differs ~3x across cells (more R-chain
    # traffic at larger b*c/n) -- calibrated from a short pilot run of this
    # same script at 2000-2500 walks/cell (see global_exclusion_walk_measure.log
    # 's first, superseded, 15-depth-bin run for the timing numbers this was
    # based on: 0.0047/0.0076/0.0034/0.0102 s/walk respectively).
    cells = [
        dict(n=65536, b=100, c=400.0, n_walks=20000, max_steps=40000),
        dict(n=65536, b=300, c=150.0, n_walks=12000, max_steps=40000),
        dict(n=65536, b=100, c=600.0, n_walks=25000, max_steps=40000),
        dict(n=65536, b=400, c=100.0, n_walks=9000, max_steps=40000),
    ]
    seed_root = np.random.SeedSequence(20260822910)
    spawns = seed_root.spawn(len(cells))

    s_edges = np.linspace(0.0, 1.0, N_S_BINS + 1)
    out = {"cells": []}
    for cell, ss in zip(cells, spawns):
        n, b, c, n_walks, max_steps = (cell["n"], cell["b"], cell["c"],
                                        cell["n_walks"], cell["max_steps"])
        rho = rho_of(c, n, b)
        P_exact = (1.0 - c / n) ** (-(b - 1))
        P_lead = 1.0 / (1.0 - rho)
        b_minus_1 = b - 1
        rng = np.random.default_rng(ss)

        hit_hist = np.zeros((N_S_BINS, N_DEPTH_BINS))
        p0_hist = np.zeros((N_S_BINS, N_DEPTH_BINS))
        cnt_hist = np.zeros((N_S_BINS, N_DEPTH_BINS))

        rebuild_every = 40
        pi = R_mask = f = None
        n_cyclic = n_killed = n_trunc = 0
        for w in range(n_walks):
            if w % rebuild_every == 0:
                pi, R_mask, f = build_instance(n, b, c, rng)
            x0 = int(rng.integers(0, n))
            status, nv = run_walk(n, pi, R_mask, f, x0, max_steps, b_minus_1,
                                   hit_hist, p0_hist, cnt_hist, s_edges)
            if status == "CYCLIC":
                n_cyclic += 1
            elif status == "KILLED":
                n_killed += 1
            else:
                n_trunc += 1

        # marginal over s (all s), split ONLY by depth bin -- the key test
        depth_hit = hit_hist.sum(axis=0)
        depth_p0 = p0_hist.sum(axis=0)
        depth_cnt = cnt_hist.sum(axis=0)
        elev_by_depth = np.divide(depth_hit, depth_p0,
                                   out=np.full(N_DEPTH_BINS, np.nan),
                                   where=depth_p0 > 0)
        # sem via normal approx on the ratio (hit are ~independent Bernoulli
        # draws with mean p0*elevation; treat p0 as fixed weight per event)
        # Var(sum hit) ~ sum p0*elevation*(1-p0*elevation) approx sum hit
        # (Poisson-ish since p0 is tiny); sem(elev) ~ sqrt(sum hit)/sum p0
        sem_by_depth = np.divide(np.sqrt(np.maximum(depth_hit, 1.0)), depth_p0,
                                  out=np.full(N_DEPTH_BINS, np.nan),
                                  where=depth_p0 > 0)

        # marginal over depth, split by s bin -- secondary check (does the
        # elevation trend with s at all, beyond what (1-s) already captures)
        s_hit = hit_hist.sum(axis=1)
        s_p0 = p0_hist.sum(axis=1)
        elev_by_s = np.divide(s_hit, s_p0, out=np.full(N_S_BINS, np.nan),
                               where=s_p0 > 0)

        row = dict(n=n, b=b, c=c, rho=rho, P_exact=P_exact, P_lead=P_lead,
                   n_walks=n_walks, n_cyclic=n_cyclic, n_killed=n_killed,
                   n_truncated=n_trunc,
                   depth_threshold_b_minus_1=b_minus_1,
                   depth_cnt=depth_cnt.tolist(),
                   depth_hit=depth_hit.tolist(),
                   depth_p0=depth_p0.tolist(),
                   elev_by_depth=elev_by_depth.tolist(),
                   sem_by_depth=sem_by_depth.tolist(),
                   s_edges=s_edges.tolist(),
                   elev_by_s=elev_by_s.tolist())
        out["cells"].append(row)

        say("n=%d b=%d c=%.1f rho=%.4f P_exact=%.4f P_lead=%.4f | "
            "cyc=%d kill=%d trunc=%d/%d | wall=%.1fs"
            % (n, b, c, rho, P_exact, P_lead, n_cyclic, n_killed, n_trunc,
               n_walks, time.time() - t0))
        say("  depth bins: [0]=shallow(depth<%d)  [1]=deep(depth>=%d)"
            % (b_minus_1, b_minus_1))
        say("  elev_by_depth:   " + " ".join(
            "%.3f" % v if not math.isnan(v) else "  nan" for v in elev_by_depth))
        say("  sem_by_depth:    " + " ".join(
            "%.3f" % v if not math.isnan(v) else "  nan" for v in sem_by_depth))
        say("  cnt_by_depth:    " + " ".join("%d" % v for v in depth_cnt))
        say("  hit_by_depth:    " + " ".join("%d" % v for v in depth_hit))
        z_vs_lead = [(elev_by_depth[i] - P_lead) / sem_by_depth[i]
                     if sem_by_depth[i] > 0 and not math.isnan(sem_by_depth[i]) else float("nan")
                     for i in range(N_DEPTH_BINS)]
        z_vs_exact = [(elev_by_depth[i] - P_exact) / sem_by_depth[i]
                      if sem_by_depth[i] > 0 and not math.isnan(sem_by_depth[i]) else float("nan")
                      for i in range(N_DEPTH_BINS)]
        say("  z(elev vs P_lead=%.3f):  %s" % (P_lead,
            " ".join("%.2f" % v for v in z_vs_lead)))
        say("  z(elev vs P_exact=%.3f): %s" % (P_exact,
            " ".join("%.2f" % v for v in z_vs_exact)))

    say("# total wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "global_exclusion_walk_measure_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved global_exclusion_walk_measure_results.json")
    log.close()


if __name__ == "__main__":
    main()
