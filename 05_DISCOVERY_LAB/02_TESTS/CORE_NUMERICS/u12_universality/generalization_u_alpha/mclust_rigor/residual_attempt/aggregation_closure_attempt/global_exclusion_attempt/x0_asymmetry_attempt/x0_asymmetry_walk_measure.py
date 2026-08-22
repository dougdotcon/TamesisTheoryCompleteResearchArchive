"""x0_asymmetry_attempt -- stage 1: DIRECT walk-level measurement of the
per-target closure elevation, SPLIT BY TARGET IDENTITY (x0 vs. the other
live arc starts).

Wave 9, DISC-DEC-041 front (a), `MCLUST-X0-ASYMMETRY-ATTEMPT`.

The hypothesis under test is the one named (untested) in
`global_exclusion_attempt/ATTEMPT.md` sec 6 item (b):

  "uma possivel assimetria entre x0 (fixo desde o inicio, nunca criado por
   um sorteio de reroteamento) e os OUTROS membros de Y_live (todos criados
   dinamicamente por sobrevivencia de reroteamento) -- o formalismo de
   sec 2-3 assume ambos se comportam identicamente sob a mesma elevacao P,
   mas isso nao foi testado separadamente."

------------------------------------------------------------------------
ESTIMATOR (own design; the SPLIT is what is new -- the predecessor's
`global_exclusion_walk_measure.py` measured only the AGGREGATE elevation
over all of Y_live, and split by ARC DEPTH instead of by target identity)
------------------------------------------------------------------------
At every NORMAL pi-step of the walk (current position x not in R; reroute
steps are governed by q_CLUST(s), out of scope here and already
reconfirmed by residual_attempt sec 3.1), with n_vis points visited so far:

    w      := 1 / (n - n_vis)          [ = 1/((1-s)n), the NON-elevated
                                          per-target closure density that
                                          the inherited master formula
                                          assigns to EACH live arc start ]
    A-weight  = w                       (the single target x0)
    B-weight  = w   if the CURRENT arc's own start is not x0, else 0
    C-weight  = (K - 1 - [B active]) * w    (all remaining live arc starts)

and the corresponding indicator of the step actually closing onto that
category.  Horvitz-Thompson ratios

    lambda_0     = sum(hit_A) / sum(A-weight)
    lambda_other = (sum(hit_B)+sum(hit_C)) / (sum(B-weight)+sum(C-weight))

are consistent estimators of the true per-target elevation of x0 and of the
reroute-created arc starts respectively (each event carries its own weight,
so K and s varying inside the sample is already accounted for; the walk's
stopping time is predictable, so optional stopping applies).  Under the
formalism of phi_CAND / phi_CAND5 / phi_GLOBAL both equal the SAME constant
P (=1/(1-rho) or (1-c/n)^-(b-1)).

B and C are kept separate as a diagnostic (does "the current arc's own
start" behave differently from "an older arc's start"?), but the
pre-registered test is lambda_0 vs lambda_other.

TWO METHODOLOGICAL REFINEMENTS over the predecessor's measurement, both
required for the split to mean anything:

 1. x0 is drawn conditioned on x0 NOT IN R (rejection).  The predecessor
    drew x0 uniformly over [n]; for the rho (up to 0.60) fraction of walks
    with x0 in R, x0 is structurally almost impossible to close into (the
    shadowing lemma) yet still contributes a full 1/((1-s)n) share of the
    aggregate weight -- which biases an AGGREGATE elevation downwards and
    would completely destroy an x0-vs-others split.  Conditioning on
    x0 not in R is also exactly the conditioning under which the
    predecessors' formula is meant to apply (phi_CAND = (1-rho)*phi_V4,
    phi_V4 ~ P(cyclic | x0 not in R)).
 2. Terminal events are classified by HOW they happened: a NORMAL pi-step
    closing onto x0 (the only kind of event the lambda_0 estimator may
    count) is separated from an f-DRAW landing on x0 (also makes x0 cyclic
    -- the traversed orbit closes -- but is a reroute event, not a
    pi-closure, and must NOT enter the hazard estimator).

Stage 2 of the same script measures eps := P(cyclic | x0 in R) by
rejection-sampling x0 INSIDE R -- the quantity that phi_CAND, phi_CAND5 and
phi_GLOBAL all set to exactly 0 via the (1-rho) dilution factor.

Uncertainties are CLUSTER bootstrap over instances (walks sharing one
(pi, R, f) instance are correlated; a naive per-walk sem would understate
the error).

------------------------------------------------------------------------
OWN IMPLEMENTATION.  Imports nothing from residual_attempt/,
aggregation_closure_attempt/, global_exclusion_attempt/ or ualpha_sim.py.
The mechanism is re-read from DERIVATION_MCLUST_FIXED.md sec 1.
Seeds: np.random.SeedSequence(20260822941) -- fresh; not
20260822018 / 918302033 / 720330339 / 20260822901-904 / 20260822910-911.
"""
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_ROOT = 20260822941
SEED_ROOT_REPLICATE = 20260822942


def build_instance(n, b, c, rng):
    """M-CLUST(b): pi uniform; seeds i.i.d. Bernoulli(c/n); block of a seed s
    is {s, pi(s), ..., pi^(b-1)(s)}; R = union of blocks; every point of R
    gets an i.i.d. uniform destination fixed in advance; f = pi off R.
    (Re-read from DERIVATION_MCLUST_FIXED.md sec 1.)"""
    pi = rng.permutation(n)
    inR = rng.random(n) < (c / n)
    front = np.flatnonzero(inR)
    for _ in range(b - 1):
        if front.size == 0:
            break
        front = pi[front]
        inR[front] = True
    f = pi.copy()
    idx = np.flatnonzero(inR)
    notidx = np.flatnonzero(~inR)
    if idx.size:
        f[idx] = rng.integers(0, n, idx.size)
    return pi.tolist(), inR.tolist(), f.tolist(), idx, notidx


def rho_of(c, n, b):
    return 1.0 - (1.0 - c / n) ** b


# terminal-status codes
ST_NORM_X0 = 0     # normal pi-step closed onto x0            -> cyclic
ST_NORM_OTHER = 1  # normal pi-step closed onto other visited -> killed
ST_RR_X0 = 2       # f-draw landed on x0                      -> cyclic
ST_RR_OTHER = 3    # f-draw landed on other visited           -> killed
ST_TRUNC = 4


S_EDGES = [0.0, 0.005, 0.01, 0.02, 0.035, 0.06, 0.10, 0.25, 1.01]
N_SBIN = len(S_EDGES) - 1


def sbin_table(n):
    """nv -> s-bin index, precomputed (the equal-width binning used in the
    first run put every event in bin 0: walks terminate at visited mass
    ~0.03-0.15, never near 1)."""
    tab = []
    j = 0
    for nv in range(n + 1):
        sv = nv / n
        while j < N_SBIN - 1 and sv >= S_EDGES[j + 1]:
            j += 1
        tab.append(j)
    return tab


def run_walk(n, pi, Rm, f, x0, visited, stamp, max_steps, acc, sbin_acc,
             sbtab, track):
    """One trajectory.  `acc` is an 8-slot list accumulating
    [S_A, S_B, S_C, hit_A, hit_B, hit_C, hit_nonarcstart, hit_A_own]; note
    S_B (the weight of "the current arc's own start, when that is not x0")
    is IDENTICALLY the weight of "x0 as an OLDER arc start", so the pair
    (hit_A_own, hit_A - hit_A_own) against (S_A - S_B, S_B) gives the
    structure-matched split of x0's own elevation into "x0 is still the
    current arc's start" vs "x0 is now an older arc start" -- directly
    comparable to lambda_B and lambda_C respectively; `sbin_acc` is a
    flat list of 6*n_sbin slots with the same weights/hits binned in s.
    Returns (status, n_visited)."""
    visited[x0] = stamp
    nv = 1
    cur = x0
    K = 1                      # live arc starts (x0 + reroute survivors)
    arc_start = x0             # start of the arc the walk is currently on
    arc_set = {x0}
    hasB = 0                   # 1 if arc_start != x0
    nC = 0                     # K - 1 - hasB
    for _ in range(max_steps):
        if Rm[cur]:
            dest = f[cur]
            if visited[dest] == stamp:
                return (ST_RR_X0 if dest == x0 else ST_RR_OTHER), nv
            if not Rm[dest]:
                # dest survives -> becomes the new (current) arc start; the
                # previous arc start joins the "older arc starts" category.
                K += 1
                arc_start = dest
                hasB = 1            # dest != x0 (x0 is already visited)
                nC = K - 1 - hasB
                arc_set.add(dest)
        else:
            w = 1.0 / (n - nv)
            if track:
                acc[0] += w
                if hasB:
                    acc[1] += w
                if nC:
                    acc[2] += nC * w
                sb = sbtab[nv]
                o = 6 * sb
                sbin_acc[o] += w
                sbin_acc[o + 1] += (w if hasB else 0.0) + nC * w
            dest = pi[cur]
            if visited[dest] == stamp:
                if dest == x0:
                    if track:
                        acc[3] += 1.0
                        if not hasB:
                            acc[7] += 1.0
                        sbin_acc[6 * sb + 2] += 1.0
                    return ST_NORM_X0, nv
                if dest == arc_start:
                    if track:
                        acc[4] += 1.0
                        sbin_acc[6 * sb + 3] += 1.0
                elif dest in arc_set:
                    if track:
                        acc[5] += 1.0
                        sbin_acc[6 * sb + 3] += 1.0
                else:
                    if track:
                        acc[6] += 1.0
                        sbin_acc[6 * sb + 4] += 1.0
                return ST_NORM_OTHER, nv
        visited[dest] = stamp
        nv += 1
        cur = dest
    return ST_TRUNC, nv


def _col(arr, spec):
    return arr[:, spec].sum(axis=1) if isinstance(spec, (list, tuple)) else arr[:, spec]


def cluster_bootstrap_all(arr, ratios_spec, n_boot, rng, chunk=250):
    """Cluster (over-instance) bootstrap of several sum(num)/sum(den) ratios,
    all resampled JOINTLY (one common instance resample per replicate, so
    derived quantities such as lambda_0/lambda_other are correctly
    correlated).  `ratios_spec` maps a name -> (num_cols, den_cols).
    Returns {name: (point, sem)} plus the raw replicate arrays."""
    m = arr.shape[0]
    cols = {k: (_col(arr, nu), _col(arr, de)) for k, (nu, de) in ratios_spec.items()}
    point = {}
    for k, (nu, de) in cols.items():
        d = de.sum()
        point[k] = nu.sum() / d if d > 0 else float("nan")
    reps = {k: [] for k in cols}
    done = 0
    while done < n_boot:
        r = min(chunk, n_boot - done)
        idx = rng.integers(0, m, size=(r, m))
        for k, (nu, de) in cols.items():
            with np.errstate(invalid="ignore", divide="ignore"):
                reps[k].append(nu[idx].sum(axis=1) / de[idx].sum(axis=1))
        done += r
    reps = {k: np.concatenate(v) for k, v in reps.items()}
    sem = {k: float(np.nanstd(v)) for k, v in reps.items()}
    return point, sem, reps


def run_cell(cell, ss, say, mode, n_boot=2000):
    """mode: "A" = x0 drawn uniformly from R^c (the conditioning under which
    the predecessors' phi_V4 is defined; the only mode that tracks the
    elevation estimator);  "B" = x0 drawn uniformly from R (measures
    eps = P(cyclic | x0 in R));  "U" = x0 uniform on [n] (cross-check of this
    simulator against the phi_mc already recorded by the predecessors)."""
    assert mode in ("A", "B", "U", "R")
    in_R = (mode == "B")
    track = (mode in ("A", "R"))
    n, b, c = cell["n"], cell["b"], cell["c"]
    n_walks = cell["n_walks_" + ("A" if mode == "R" else mode)]
    rebuild_every = cell["rebuild_every"]
    max_steps = n
    n_sbin = N_SBIN
    rng = np.random.default_rng(ss)
    boot_rng = np.random.default_rng(ss.spawn(1)[0])
    rho = rho_of(c, n, b)

    visited = np.zeros(n, dtype=np.int64).tolist()
    sbtab = sbin_table(n)
    stamp = 0
    per_inst = []
    sbin_acc = [0.0] * (6 * n_sbin)
    counts = [0, 0, 0, 0, 0]
    t_start = time.time()
    n_inst = int(math.ceil(n_walks / rebuild_every))
    done = 0
    for _ in range(n_inst):
        pi, Rm, f, R_idx, notR_idx = build_instance(n, b, c, rng)
        pool = R_idx if mode == "B" else (notR_idx if mode in ("A", "R") else None)
        if pool is not None and pool.size == 0:
            continue
        k = min(rebuild_every, n_walks - done)
        x0s = (rng.integers(0, n, k) if pool is None
               else pool[rng.integers(0, pool.size, k)])
        acc = [0.0] * 8
        ic = [0, 0, 0, 0, 0]
        for x0 in x0s:
            stamp += 1
            st, nv = run_walk(n, pi, Rm, f, int(x0), visited, stamp,
                              max_steps, acc, sbin_acc, sbtab, track=track)
            ic[st] += 1
            counts[st] += 1
        done += k
        per_inst.append(acc + [float(v) for v in ic] + [float(k)])
        if done >= n_walks:
            break

    wall = time.time() - t_start
    n_cyc = counts[ST_NORM_X0] + counts[ST_RR_X0]
    out = dict(n=n, b=b, c=c, rho=rho, mode=mode, x0_in_R=bool(in_R),
               n_walks=done, wall_s=wall,
               n_instances=len(per_inst),
               n_norm_x0=counts[ST_NORM_X0], n_norm_other=counts[ST_NORM_OTHER],
               n_rr_x0=counts[ST_RR_X0], n_rr_other=counts[ST_RR_OTHER],
               n_trunc=counts[ST_TRUNC],
               phi_hat=n_cyc / done if done else float("nan"))
    # columns: 0..7 acc [S_A,S_B,S_C,hit_A,hit_B,hit_C,hit_nonarc,hit_A_own],
    #          8..12 status counts, 13 n_walks
    arr = np.asarray(per_inst, dtype=float)
    spec = {"phi": ([8, 10], 13)}
    if track:
        # S_A_own = S_A - S_B and hit_A_old = hit_A - hit_A_own are appended
        # as extra columns 14, 15 so the same joint bootstrap covers them.
        arr = np.hstack([arr,
                         (arr[:, 0] - arr[:, 1])[:, None],
                         (arr[:, 3] - arr[:, 7])[:, None]])
        spec.update({"l0": (3, 0), "lB": (4, 1), "lC": (5, 2),
                     "lO": ([4, 5], [1, 2]),
                     "l0own": (7, 14), "l0old": (15, 1)})
    pt, sem, reps = cluster_bootstrap_all(arr, spec, n_boot, boot_rng)
    out["phi_hat_boot"] = pt["phi"]
    out["phi_sem"] = sem["phi"]
    if track:
        with np.errstate(invalid="ignore", divide="ignore"):
            rat = reps["l0"] / reps["lO"]
        out.update(dict(
            lambda_x0=pt["l0"], sem_lambda_x0=sem["l0"],
            lambda_curr_arc=pt["lB"], sem_lambda_curr_arc=sem["lB"],
            lambda_older_arcs=pt["lC"], sem_lambda_older_arcs=sem["lC"],
            lambda_other=pt["lO"], sem_lambda_other=sem["lO"],
            ratio_x0_over_other=pt["l0"] / pt["lO"] if pt["lO"] else float("nan"),
            sem_ratio=float(np.nanstd(rat)),
            sem_diff=float(np.nanstd(reps["l0"] - reps["lO"])),
            sum_wA=float(arr[:, 0].sum()), sum_wB=float(arr[:, 1].sum()),
            sum_wC=float(arr[:, 2].sum()),
            hit_A=int(arr[:, 3].sum()), hit_B=int(arr[:, 4].sum()),
            hit_C=int(arr[:, 5].sum()), hit_nonarcstart=int(arr[:, 6].sum()),
            lambda_x0_own_arc=pt["l0own"], sem_lambda_x0_own_arc=sem["l0own"],
            lambda_x0_older=pt["l0old"], sem_lambda_x0_older=sem["l0old"],
            hit_A_own=int(arr[:, 7].sum()),
            sbin=sbin_acc, n_sbin=n_sbin, s_edges=S_EDGES))
    return out


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    t0 = time.time()
    log_path = os.path.join(HERE, "x0_asymmetry_walk_measure_%s.log" % which)
    log = open(log_path, "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# x0_asymmetry_walk_measure stage %s | started %s"
        % (which, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
    say("# own implementation; SeedSequence(%d); cluster bootstrap over instances"
        % (SEED_ROOT_REPLICATE if which == "R" else SEED_ROOT))

    # The 4 stress cells used by every predecessor in this line, plus two
    # mid-rho controls (b=50/c=400, b=200/c=150) so the asymmetry can be
    # tracked as a function of rho rather than only at the extreme.
    # walk counts calibrated from a pilot of this same script so that each
    # cell yields ~1.2-2.8e4 NORMAL-step closures onto x0 -> ~0.6-0.9%
    # statistical resolution on lambda_x0, which is the binding precision
    # (the asymmetry that would be needed to close the residual is 1-4%,
    # see ATTEMPT.md sec 2.3 -- computed BEFORE this run, from already
    # recorded MC data).
    cells = [
        dict(n=65536, b=100, c=400.0, n_walks_A=300000, n_walks_B=500000, n_walks_U=150000, rebuild_every=25),
        dict(n=65536, b=300, c=150.0, n_walks_A=240000, n_walks_B=400000, n_walks_U=150000, rebuild_every=25),
        dict(n=65536, b=100, c=600.0, n_walks_A=320000, n_walks_B=500000, n_walks_U=150000, rebuild_every=25),
        dict(n=65536, b=400, c=100.0, n_walks_A=200000, n_walks_B=300000, n_walks_U=120000, rebuild_every=25),
        dict(n=65536, b=50,  c=400.0, n_walks_A=200000, n_walks_B=400000, n_walks_U=120000, rebuild_every=25),
        dict(n=65536, b=200, c=150.0, n_walks_A=200000, n_walks_B=300000, n_walks_U=120000, rebuild_every=25),
    ]
    # stage R = independent REPLICATION of stage A on a subset of cells with a
    # DIFFERENT root seed, run because two of the six stage-A cells showed a
    # -3.4 / -3.7 sigma asymmetry and the six ratios failed a homogeneity test
    # -- a single realisation is not enough to call that real.
    root = np.random.SeedSequence(SEED_ROOT_REPLICATE if which == "R" else SEED_ROOT)
    # stage A uses spawn slots 0..5, stage B 100..105, stage U 150..155
    spawns = root.spawn(200)
    offset = {"A": 0, "B": 100, "U": 150, "R": 0}[which]

    out = {"stage": which, "seed_root": SEED_ROOT, "cells": []}
    if which == "R":
        cells = [cells[i] for i in (1, 2, 3)]   # b=300/c=150, b=100/c=600, b=400/c=100
    for i, cell in enumerate(cells):
        r = run_cell(cell, spawns[i + offset], say, mode=which)
        out["cells"].append(r)
        if which == "B":
            say("n=%d b=%d c=%.1f rho=%.4f [x0 IN R] walks=%d | eps=P(cyc|x0 in R)="
                "%.6f +- %.6f  (norm_x0=%d rr_x0=%d) | rho*eps=%.6f | wall=%.1fs"
                % (r["n"], r["b"], r["c"], r["rho"], r["n_walks"], r["phi_hat"],
                   r["phi_sem"], r["n_norm_x0"], r["n_rr_x0"],
                   r["rho"] * r["phi_hat"], r["wall_s"]))
        elif which == "U":
            say("n=%d b=%d c=%.1f rho=%.4f [x0 UNIFORM, cross-check] walks=%d | "
                "phi_hat=%.6f +- %.6f | wall=%.1fs"
                % (r["n"], r["b"], r["c"], r["rho"], r["n_walks"],
                   r["phi_hat"], r["phi_sem"], r["wall_s"]))
        else:                                   # stages A and R
            P_lead = 1.0 / (1.0 - r["rho"])
            P_exact = (1.0 - r["c"] / r["n"]) ** (-(r["b"] - 1))
            dl = r["lambda_x0"] - r["lambda_other"]
            sd = r["sem_diff"]
            say("n=%d b=%d c=%.1f rho=%.4f [x0 NOT in R] walks=%d inst=%d | "
                "phi_A=%.6f+-%.6f | wall=%.1fs"
                % (r["n"], r["b"], r["c"], r["rho"], r["n_walks"],
                   r["n_instances"], r["phi_hat"], r["phi_sem"], r["wall_s"]))
            say("   P_lead=%.4f P_exact=%.4f | lambda_x0=%.4f+-%.4f  "
                "lambda_other=%.4f+-%.4f  (curr_arc=%.4f+-%.4f  older=%.4f+-%.4f)"
                % (P_lead, P_exact, r["lambda_x0"], r["sem_lambda_x0"],
                   r["lambda_other"], r["sem_lambda_other"],
                   r["lambda_curr_arc"], r["sem_lambda_curr_arc"],
                   r["lambda_older_arcs"], r["sem_lambda_older_arcs"]))
            say("   ratio lambda_x0/lambda_other = %.4f +- %.4f   (z_diff=%.2f)  "
                "| hits A/B/C/nonarc = %d/%d/%d/%d"
                % (r["ratio_x0_over_other"], r["sem_ratio"],
                   dl / sd if sd else float("nan"),
                   r["hit_A"], r["hit_B"], r["hit_C"], r["hit_nonarcstart"]))
            say("   structure-matched: x0-as-current-arc-start=%.4f+-%.4f vs "
                "other-current-arc-start=%.4f+-%.4f | x0-as-older=%.4f+-%.4f vs "
                "other-older=%.4f+-%.4f"
                % (r["lambda_x0_own_arc"], r["sem_lambda_x0_own_arc"],
                   r["lambda_curr_arc"], r["sem_lambda_curr_arc"],
                   r["lambda_x0_older"], r["sem_lambda_x0_older"],
                   r["lambda_older_arcs"], r["sem_lambda_older_arcs"]))
            say("   z(lambda_x0 vs P_lead)=%.2f  z(lambda_other vs P_lead)=%.2f"
                % ((r["lambda_x0"] - P_lead) / r["sem_lambda_x0"],
                   (r["lambda_other"] - P_lead) / r["sem_lambda_other"]))

    say("# total wall %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "x0_asymmetry_walk_measure_%s_results.json" % which), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved x0_asymmetry_walk_measure_%s_results.json" % which)
    log.close()


if __name__ == "__main__":
    main()
