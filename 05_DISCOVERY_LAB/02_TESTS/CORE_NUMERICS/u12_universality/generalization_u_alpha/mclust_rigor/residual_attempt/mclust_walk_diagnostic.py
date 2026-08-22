"""residual_attempt -- stage D (DISC-DEC-033, MCLUST-RESIDUAL-RIGOR).

Direct single-trajectory walk simulator (own implementation, does not
import ualpha_sim.py or mclust_validate.py) that reproduces the
exploration process narrated in DERIVATIONS.md sec 0 / sec 3.5 and
DERIVATION_MCLUST_FIXED.md literally, step by step, instead of using
the f^(2^k) cyclic-fraction shortcut. This lets us measure, DIRECTLY
from the mechanism (ground truth, no mean-field assumption anywhere),
the two empirical functions wave 4's phi_NEW assumes analytically:

  (a) q_CLUST(s): P(a reroute event occurring at visited-mass-fraction
      s eventually KILLS, i.e. the chain terminates by landing on
      already-visited mass) -- wave 4 derived q_CLUST(s) = s/(1-rho).

  (b) the CLOSURE hazard: P(a NORMAL pi-step taken at visited-mass s
      lands exactly on a previously-visited point) -- the master
      formula (DERIVATIONS.md sec 1, "unaltered" per wave 4 sec 4)
      assumes this is exactly s (i.e. hazard density 1/(1-s), from
      (1-t)/(1-s) survival factors), UNCHANGED from M-U, for ANY
      mechanism in the M-q class including M-CLUST.

Correctness argument for why a single visited-set walk correctly
reproduces both quantities (see ATTEMPT.md sec 4 for the full writeup):
on a uniform random permutation, if the CURRENT arc's forward pi-walk
is ever going to re-enter previously-visited mass, it must land EXACTLY
on the closest (in cycle order) previously-visited point -- which, by
induction, is always an arc-start (never a mid-arc point), because an
older arc's own trajectory would itself have already registered a
closure/kill the first time IT reached that arc-start. So "does the
next pi-step land on visited mass" is exactly the closure event the
master formula models, and no separate arc-start bookkeeping is needed
-- checking membership in the single running `visited` set is enough.

Walk logic (single trajectory from x0, following DERIVATION_MCLUST_FIXED.md
sec 1's mechanism exactly):
    cur = x0; visited = {x0}
    loop:
      if cur in R:              # reroute point (run start or shadowed
                                 # member reached via a PRIOR chain jump)
        dest = f[cur]            # pre-fixed uniform draw
      else:
        dest = pi[cur]           # normal step
      if dest in visited:
        status = CYCLIC if dest == x0 else KILLED
        break
      visited.add(dest); record diagnostic; cur = dest
"""
import json
import math
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def build_instance(n, b, c, rng):
    """Own implementation of M-CLUST(b), re-read from DERIVATION_MCLUST_FIXED.md
    sec 1 (own reading, not copied from mclust_validate.py -- independently
    written here so this diagnostic does not inherit any bug from the
    wave-4 validator)."""
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


def run_walk(n, pi, R_mask, f, x0, max_steps):
    """Single trajectory from x0. Returns (status, events) where events is
    a list of (s_before_event, kind, outcome):
      kind='reroute': outcome in {'kill','continue','survive'}
                       ('continue' = landed on fresh R; 'survive' = landed
                       on fresh non-R; 'kill' = landed on visited mass)
      kind='normal':  outcome in {'closure_x0','closure_other','fresh'}
    s_before_event = |visited|/n at the moment the event's destination is
    drawn (i.e. BEFORE this event's outcome is added to visited)."""
    visited = np.zeros(n, dtype=bool)
    visited[x0] = True
    n_visited = 1
    arc_mass = 1  # counts x0 + every NORMAL pi-step landing (run starts
                   # included, since walking onto a run start is itself a
                   # normal pi-step); chain-continue draws do NOT increment
                   # this -- candidate distinction tested in ATTEMPT.md sec 5
    cur = x0
    events = []
    for _ in range(max_steps):
        in_r = R_mask[cur]
        dest = f[cur] if in_r else pi[cur]
        s_before = n_visited / n
        a_before = arc_mass / n
        if visited[dest]:
            if in_r:
                events.append((s_before, a_before, "reroute", "kill"))
            else:
                events.append((s_before, a_before, "normal",
                                "closure_x0" if dest == x0 else "closure_other"))
            status = "CYCLIC" if dest == x0 else "KILLED"
            return status, events, n_visited, arc_mass
        # fresh landing
        if in_r:
            events.append((s_before, a_before, "reroute",
                            "continue" if R_mask[dest] else "survive"))
        else:
            events.append((s_before, a_before, "normal", "fresh"))
            arc_mass += 1
        visited[dest] = True
        n_visited += 1
        cur = dest
    return "TRUNCATED", events, n_visited, arc_mass


def main():
    t0 = time.time()
    log_path = os.path.join(HERE, "mclust_walk_diagnostic.log")
    log = open(log_path, "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# mclust_walk_diagnostic | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    # Focus on the most extreme stress cells (largest b*c/n, where wave 4's
    # residual is largest) plus one mild control cell, to keep wall time
    # bounded while directly probing the regime of interest.
    # Own seeds, NOT wave 4's SeedSequence(20260822018) and NOT any seed
    # used later in mclust_residual_validate.py (fresh-seed discipline
    # kept separate per script, documented in ATTEMPT.md).
    cells = [
        dict(n=65536, b=100, c=400.0, n_walks=6000, max_steps=40000),
        dict(n=65536, b=50, c=400.0, n_walks=6000, max_steps=40000),
        dict(n=65536, b=200, c=150.0, n_walks=6000, max_steps=40000),
        dict(n=32768, b=8, c=160.0, n_walks=6000, max_steps=40000),
    ]
    seed_root = np.random.SeedSequence(918302033)  # DISC-DEC-033, diagnostic
    spawns = seed_root.spawn(len(cells))

    out = {"cells": []}
    for cell, ss in zip(cells, spawns):
        n, b, c, n_walks, max_steps = cell["n"], cell["b"], cell["c"], cell["n_walks"], cell["max_steps"]
        rho = 1.0 - (1.0 - c / n) ** b
        rng = np.random.default_rng(ss)
        n_cyclic = 0
        n_killed = 0
        n_trunc = 0
        # bin events by visited-mass s into coarse bins for hazard/kill curves
        n_bins = 40
        bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
        reroute_kill = np.zeros(n_bins)
        reroute_continue = np.zeros(n_bins)
        reroute_survive = np.zeros(n_bins)
        normal_closure = np.zeros(n_bins)
        normal_fresh = np.zeros(n_bins)

        rebuild_every = 50  # amortize instance construction over several x0's
        pi = R_mask = f = None
        final_masses = []
        final_arc_masses = []
        # chain-level (not per-draw) kill/survive tally, keyed by the s at
        # which the chain-INITIATING reroute event fired (first draw only)
        chain_kill = np.zeros(n_bins)
        chain_total = np.zeros(n_bins)
        for w in range(n_walks):
            if w % rebuild_every == 0:
                pi, R_mask, f = build_instance(n, b, c, rng)
            x0 = int(rng.integers(0, n))
            status, events, nv, am = run_walk(n, pi, R_mask, f, x0, max_steps)
            final_masses.append(nv / n)
            final_arc_masses.append(am / n)
            if status == "CYCLIC":
                n_cyclic += 1
            elif status == "KILLED":
                n_killed += 1
            else:
                n_trunc += 1
            chain_start_s = None
            for s_before, a_before, kind, outcome in events:
                if kind == "reroute":
                    if chain_start_s is None:
                        chain_start_s = s_before
                    if outcome != "continue":
                        bidx0 = min(int(chain_start_s * n_bins), n_bins - 1)
                        chain_total[bidx0] += 1
                        if outcome == "kill":
                            chain_kill[bidx0] += 1
                        chain_start_s = None
                else:
                    chain_start_s = None
            for s_before, a_before, kind, outcome in events:
                bidx = min(int(s_before * n_bins), n_bins - 1)
                if kind == "reroute":
                    if outcome == "kill":
                        reroute_kill[bidx] += 1
                    elif outcome == "continue":
                        reroute_continue[bidx] += 1
                    else:
                        reroute_survive[bidx] += 1
                else:
                    if outcome in ("closure_x0", "closure_other"):
                        normal_closure[bidx] += 1
                    else:
                        normal_fresh[bidx] += 1

        phi_hat = n_cyclic / n_walks
        sem = math.sqrt(phi_hat * (1 - phi_hat) / n_walks)

        reroute_total = reroute_kill + reroute_continue + reroute_survive
        q_empirical = np.divide(reroute_kill, reroute_total,
                                 out=np.full(n_bins, np.nan), where=reroute_total > 0)
        cont_empirical = np.divide(reroute_continue, reroute_total,
                                    out=np.full(n_bins, np.nan), where=reroute_total > 0)

        normal_total = normal_closure + normal_fresh
        closure_hazard_empirical = np.divide(normal_closure, normal_total,
                                              out=np.full(n_bins, np.nan), where=normal_total > 0)

        bin_mid = (bin_edges[:-1] + bin_edges[1:]) / 2
        chain_kill_prob = np.divide(chain_kill, chain_total,
                                     out=np.full(n_bins, np.nan), where=chain_total > 0)

        # empirical survival curve S(t) = P(final visited mass >= t), on a
        # finer grid than the event bins (directly comparable to wave 4's
        # E[S(t)] = (1-t) exp(-c H_NEW(t,rho)) without any hazard bookkeeping)
        fm = np.array(final_masses)
        am_arr = np.array(final_arc_masses)
        t_grid = np.linspace(0.0, min(0.5, float(fm.max()) if fm.size else 0.5), 60)
        survival = np.array([(fm >= t).mean() for t in t_grid])
        survival_arcmass = np.array([(am_arr >= t).mean() for t in t_grid])

        row = dict(n=n, b=b, c=c, rho=rho, n_walks=n_walks,
                   phi_hat=phi_hat, sem=sem,
                   n_cyclic=n_cyclic, n_killed=n_killed, n_truncated=n_trunc,
                   bin_mid=bin_mid.tolist(),
                   reroute_total=reroute_total.tolist(),
                   q_empirical=q_empirical.tolist(),
                   cont_empirical=cont_empirical.tolist(),
                   normal_total=normal_total.tolist(),
                   closure_hazard_empirical=closure_hazard_empirical.tolist(),
                   chain_total=chain_total.tolist(),
                   chain_kill_prob=chain_kill_prob.tolist(),
                   t_grid=t_grid.tolist(),
                   survival_empirical=survival.tolist(),
                   survival_arcmass_empirical=survival_arcmass.tolist(),
                   final_masses=fm.tolist(),
                   final_arc_masses=am_arr.tolist(),
                   mean_excess_mass=float((fm - am_arr).mean()),
                   max_excess_mass=float((fm - am_arr).max()))
        out["cells"].append(row)
        say("n=%d b=%d c=%.1f rho=%.4f | phi_hat=%.5f+-%.5f (cyc=%d kill=%d trunc=%d / %d) | wall=%.1fs"
            % (n, b, c, rho, phi_hat, sem, n_cyclic, n_killed, n_trunc, n_walks, time.time() - t0))

    say("# total wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "mclust_walk_diagnostic_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved mclust_walk_diagnostic_results.json")
    log.close()


if __name__ == "__main__":
    main()
