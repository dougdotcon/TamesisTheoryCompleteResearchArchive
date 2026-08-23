"""ref2_walk.py -- the referee's OWN step-by-step walk simulator for M-CLUST(b),
used to measure the per-target closure elevation lambda(t) as a function of the
traversed mass t.

Independent of the target front's `elev_pool_probe.py` (not read before this
file was written and working).  Independent of every predecessor's
`*_walk_measure.py`.

Design
------
G walks run in lock-step, one per instance, vectorised over instances.  When a
walk ends a fresh walk is started in the SAME instance; per-walk state is reset
for free by a stamp trick (visited / consumed arrays hold the walk id, not a
boolean).  Errors are cluster bootstrap over instances.

What is recorded, at every NORMAL pi-step (i.e. every step taken from a point
of R^c), in bins of the traversed mass t = (#visited)/n:

    pool      = |U_rem| - (#normal steps already taken)     <- the claim of 3.1
    w_master  = n_live / ((1-t) n)      density the master formula assigns
    w_exact   = n_live / pool           density (3.1) assigns
    hit       = 1{ pi(x) in Y_live }

with Y an EXOGENOUS probe set of m points drawn uniformly from R^c when the
instance is built (note R^c = U_rem \\ R exactly, proved in ref2_mc selftest),
and n_live the number of probe points not yet consumed as a pi-image.

In parallel a Horvitz-Thompson estimator on the walk's OWN live closure targets
is accumulated (n_targ = x0 plus every point first reached by an f-draw --
these are exactly the visited points whose pi-preimage is unvisited, hence the
only visited points a normal pi-step can land on).

Two deterministic audits run on EVERY normal step:
    (a) pi(x) must lie in U_rem;
    (b) pi(x) must not already have been consumed as an image in this walk.

Seeds: numpy SeedSequence, values 20260824910+ (fresh, never used in this
archive -- checked by grep).
"""
import json
import math
import os
import sys
import time

import numpy as np

import ref2_mc as M

BIN_EDGES = np.array([0.0, 0.0025, 0.005, 0.01, 0.02, 0.035,
                      0.06, 0.10, 0.18, 0.32, 1.01])
NBIN = len(BIN_EDGES) - 1


def build_batch(rng, G, n, b, c, m_probe):
    """Build G independent instances; return flat arrays and per-instance data."""
    f = np.empty(G * n, dtype=np.int64)
    Rm = np.empty(G * n, dtype=bool)
    inU = np.empty(G * n, dtype=bool)
    isprobe = np.zeros(G * n, dtype=bool)
    pool0 = np.empty(G, dtype=np.int64)
    nnotR = np.empty(G, dtype=np.int64)
    for g in range(G):
        pi = rng.permutation(n).astype(np.int64)
        sm = rng.random(n) < (c / n)
        R = M.build_R(pi, sm, b)
        # revealed images  I = { pi^j(s) : s seed, 1<=j<=b-1 }
        I = np.zeros(n, dtype=bool)
        cur = np.flatnonzero(sm)
        for _ in range(b - 1):
            cur = pi[cur]
            I[cur] = True
        U = ~I
        ff = pi.copy()
        nR = int(R.sum())
        if nR:
            ff[R] = rng.integers(0, n, size=nR, dtype=np.int64)
        sl = slice(g * n, (g + 1) * n)
        f[sl] = ff
        Rm[sl] = R
        inU[sl] = U
        notR_idx = np.flatnonzero(~R)
        nnotR[g] = notR_idx.size
        sel = rng.choice(notR_idx, size=min(m_probe, notR_idx.size),
                         replace=False)
        pr = np.zeros(n, dtype=bool)
        pr[sel] = True
        isprobe[sl] = pr
        pool0[g] = int(U.sum())
    return f, Rm, inU, isprobe, pool0, nnotR


def run_cell(seed_int, n, b, c, G=256, n_batches=2, iters=120000,
             m_probe=1000, verbose=True):
    rng = np.random.default_rng(np.random.SeedSequence(seed_int))
    base = (np.arange(G) * n).astype(np.int64)
    slots = np.arange(G)

    # wc : sum of w_master * lambda_closedform(t)  -- lets the CLOSED FORM (3.1)
    #      (which uses the ENSEMBLE-MEAN pool A*n) be compared bin by bin
    #      against the PER-STEP pool law (we/wm), which is what the target's
    #      "lambda model (3.1)" column actually measures.
    acc = {k: np.zeros((G, NBIN)) for k in
           ("hit", "wm", "we", "cnt", "hitT", "wT", "wTm", "wc",
            "s_pool", "s_fresh", "s_nvis", "s_nnorm")}
    p_ = c / float(n)
    rho_ = 1.0 - (1.0 - p_) ** b
    A_ = (1.0 - rho_) / (1.0 - p_)          # mean |U_rem| / n
    delta_ = p_ / (1.0 - rho_)              # chain-mass factor, section 6.3
    tot = dict(steps=0, normal=0, walks=0, cyc=0, dead=0, budget=0,
               audit_U=0, audit_cons=0, abandoned=0,
               term_arc=0, term_chainR=0, term_other=0)
    nvis_end = []

    for batch in range(n_batches):
        t0 = time.time()
        f, Rm, inU, isprobe, pool0, nnotR = build_batch(
            rng, G, n, b, c, m_probe)
        vis = np.zeros(G * n, dtype=np.int64)
        cons = np.zeros(G * n, dtype=np.int64)
        wid = np.ones(G, dtype=np.int64)
        nprobe = np.minimum(m_probe, nnotR).astype(np.float64)

        # ---- start the first walk in every slot -------------------------
        def start_walks(mask):
            """(re)start walks in the slots selected by boolean mask."""
            k = int(mask.sum())
            if k == 0:
                return
            idx = np.flatnonzero(mask)
            cand = rng.integers(0, n, size=k, dtype=np.int64)
            bad = Rm[base[idx] + cand]
            while bad.any():
                nb = int(bad.sum())
                cand[bad] = rng.integers(0, n, size=nb, dtype=np.int64)
                bad = Rm[base[idx] + cand]
            x0[idx] = cand
            cur[idx] = cand
            vis[base[idx] + cand] = 2 * wid[idx] + 1
            nvis[idx] = 1
            nnorm[idx] = 0
            nlive[idx] = nprobe[idx]
            ntarg[idx] = 1
            nstep[idx] = 0

        x0 = np.zeros(G, dtype=np.int64)
        cur = np.zeros(G, dtype=np.int64)
        nvis = np.zeros(G, dtype=np.int64)
        nnorm = np.zeros(G, dtype=np.int64)
        nlive = np.zeros(G, dtype=np.float64)
        ntarg = np.zeros(G, dtype=np.int64)
        nstep = np.zeros(G, dtype=np.int64)
        start_walks(np.ones(G, dtype=bool))

        cap = 4 * n
        draining = False
        active = np.ones(G, dtype=bool)
        it = 0
        while True:
            if it >= iters and not draining:
                draining = True
            if draining and not active.any():
                break
            it += 1
            if it > iters + 40 * n:
                break
            act = np.flatnonzero(active)
            if act.size == 0:
                break
            x = cur[act]
            gx = base[act] + x
            y = f[gx]
            gy = base[act] + y
            isR = Rm[gx]
            nrm = ~isR
            tot["steps"] += act.size

            # -------- record on normal steps ---------------------------
            if nrm.any():
                aN = act[nrm]
                gyN = gy[nrm]
                poolN = (pool0[aN] - nnorm[aN]).astype(np.float64)
                tN = nvis[aN] / float(n)
                wm = nlive[aN] / ((1.0 - tN) * n)
                we = nlive[aN] / poolN
                hitp = isprobe[gyN] & (cons[gyN] != wid[aN])
                wT = ntarg[aN] / poolN
                wTm = ntarg[aN] / ((1.0 - tN) * n)
                hitT = (vis[gyN] == 2 * wid[aN] + 1)
                # audits
                tot["audit_U"] += int(np.count_nonzero(~inU[gyN]))
                tot["audit_cons"] += int(np.count_nonzero(cons[gyN] == wid[aN]))
                bidx = np.searchsorted(BIN_EDGES, tN, side="right") - 1
                np.clip(bidx, 0, NBIN - 1, out=bidx)
                lin = aN * NBIN + bidx
                ml = G * NBIN
                acc["hit"] += np.bincount(lin, weights=hitp.astype(float),
                                          minlength=ml).reshape(G, NBIN)
                acc["wm"] += np.bincount(lin, weights=wm, minlength=ml
                                         ).reshape(G, NBIN)
                acc["we"] += np.bincount(lin, weights=we, minlength=ml
                                         ).reshape(G, NBIN)
                acc["cnt"] += np.bincount(lin, minlength=ml).reshape(G, NBIN)
                acc["hitT"] += np.bincount(lin, weights=hitT.astype(float),
                                           minlength=ml).reshape(G, NBIN)
                acc["wT"] += np.bincount(lin, weights=wT, minlength=ml
                                         ).reshape(G, NBIN)
                acc["wTm"] += np.bincount(lin, weights=wTm, minlength=ml
                                          ).reshape(G, NBIN)
                lam_cf = (1.0 - tN) / (A_ - tN / (1.0 + delta_))
                acc["wc"] += np.bincount(lin, weights=wm * lam_cf,
                                         minlength=ml).reshape(G, NBIN)
                acc["s_pool"] += np.bincount(lin, weights=poolN,
                                             minlength=ml).reshape(G, NBIN)
                acc["s_fresh"] += np.bincount(lin, weights=(1.0 - tN) * n,
                                              minlength=ml).reshape(G, NBIN)
                acc["s_nvis"] += np.bincount(lin, weights=nvis[aN].astype(float),
                                             minlength=ml).reshape(G, NBIN)
                acc["s_nnorm"] += np.bincount(lin,
                                              weights=nnorm[aN].astype(float),
                                              minlength=ml).reshape(G, NBIN)
                cons[gyN] = wid[aN]
                nlive[aN] -= hitp
                nnorm[aN] += 1
                tot["normal"] += aN.size

            # -------- advance / terminate ------------------------------
            nstep[act] += 1
            closed = (y == x0[act])
            visited = ((vis[gy] >> 1) == wid[act]) & (~closed)
            cont = (~closed) & (~visited)
            over = nstep[act] > cap

            if cont.any():
                aC = act[cont]
                gyC = gy[cont]
                # tag: 1 = reached by an f-draw (a live closure target),
                #      0 = reached by a normal pi-step
                # a visited point can only be hit by a normal pi-step if it
                # lies in U_rem; chain points of R outside U_rem are NOT live
                # closure targets (their pi-predecessor is itself in R, so the
                # walk never steps from it)
                tag = (isR[cont] & inU[gyC]).astype(np.int64)
                vis[gyC] = 2 * wid[aC] + tag
                ntarg[aC] += tag
                nvis[aC] += 1
                cur[aC] = y[cont]

            fin = closed | visited | over
            if fin.any():
                aF = act[fin]
                tot["walks"] += int(fin.sum())
                nc = int(np.count_nonzero(closed[fin]))
                tot["cyc"] += nc
                tot["dead"] += int(np.count_nonzero(visited[fin]))
                tot["budget"] += int(np.count_nonzero(
                    over[fin] & ~closed[fin] & ~visited[fin]))
                nvis_end.append(nvis[aF].copy())
                # classify the terminal landing for the dead ones
                dmask = visited[fin]
                if dmask.any():
                    gyD = gy[fin][dmask]
                    aD = aF[dmask]
                    isT = (vis[gyD] == 2 * wid[aD] + 1)
                    inRD = Rm[gyD]
                    tot["term_arc"] += int(np.count_nonzero(isT & ~inRD))
                    tot["term_chainR"] += int(np.count_nonzero(isT & inRD))
                    tot["term_other"] += int(np.count_nonzero(~isT))
                wid[aF] += 1
                if draining:
                    active[aF] = False
                else:
                    m = np.zeros(G, dtype=bool)
                    m[aF] = True
                    start_walks(m)
        if verbose:
            print("    batch %d/%d done  (%.1fs, %d normal steps so far)"
                  % (batch + 1, n_batches, time.time() - t0, tot["normal"]),
                  flush=True)

    out = dict(n=n, b=b, c=c, G=G, n_batches=n_batches, iters=iters,
               m_probe=m_probe, seed=seed_int,
               bin_edges=BIN_EDGES.tolist(), tot=tot,
               acc={k: v.tolist() for k, v in acc.items()},
               nvis_end_mean=float(np.concatenate(nvis_end).mean())
               if nvis_end else 0.0)
    return out


if __name__ == "__main__":
    cells = {
        # name : (n, b, c, seed, G, n_batches, iters)
        "b100_c600": (65536, 100, 600, 20260824911, 256, 4, 60000),
        "b400_c100": (65536, 400, 100, 20260824912, 256, 4, 60000),
        "b200_c150": (65536, 200, 150, 20260824913, 256, 4, 60000),
        "b8_c160": (32768, 8, 160, 20260824914, 384, 4, 60000),
        "b100_c1000": (65536, 100, 1000, 20260824915, 256, 4, 60000),
        "b50_c400": (65536, 50, 400, 20260824916, 256, 4, 60000),
        "b100_c150": (65536, 100, 150, 20260824917, 256, 4, 60000),
        "b300_c150": (65536, 300, 150, 20260824918, 256, 4, 60000),
        "b800_c100": (65536, 800, 100, 20260824919, 256, 4, 60000),
    }
    which = sys.argv[1:] if len(sys.argv) > 1 else list(cells)
    for name in which:
        n, b, c, sd, G, nb, iters = cells[name]
        print("[cell %s] n=%d b=%d c=%d seed=%d" % (name, n, b, c, sd),
              flush=True)
        t0 = time.time()
        res = run_cell(sd, n, b, c, G=G, n_batches=nb, iters=iters)
        res["wall_s"] = time.time() - t0
        with open("ref2_walk_%s.json" % name, "w") as fh:
            json.dump(res, fh)
        t = res["tot"]
        print("  -> normal steps %d, walks %d, cyc %d, audits (U=%d cons=%d), "
              "%.1fs" % (t["normal"], t["walks"], t["cyc"], t["audit_U"],
                         t["audit_cons"], res["wall_s"]), flush=True)
