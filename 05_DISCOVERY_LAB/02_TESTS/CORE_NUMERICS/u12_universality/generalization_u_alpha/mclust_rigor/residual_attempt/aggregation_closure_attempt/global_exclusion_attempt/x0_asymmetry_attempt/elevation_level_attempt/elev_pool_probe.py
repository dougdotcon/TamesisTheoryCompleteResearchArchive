#!/usr/bin/env python3
"""
elev_pool_probe.py -- T1 + T2 of DERIVATION_PREREG.md:  measure the per-target
closure elevation AS A FUNCTION OF THE TRAVERSED MASS t, directly from the
mechanism, with a step-by-step walk simulator written from scratch.

Two estimators are accumulated at every NORMAL pi-step of a surviving walk
(current position x not in R; reroute steps are governed by q_CLUST and are out of
scope here), in bins of the traversed mass s = n_vis/n:

    pool      = |U_rem| - (# normal steps already taken)      <- THIS FRONT's claim
    w_master  = n_test_live / ((1-s) n)     the density the master formula assigns
    w_exact   = n_test_live / pool          the density this front derives
    hit       = 1{ pi(x) in Y_test }

with `Y_test` an EXOGENOUS set of M points drawn uniformly from U_rem \\ R at
instance-construction time (independent of the walk), `n_test_live` the number of
its members not yet consumed as an image.  Then, per bin,

    lambda_measured = sum hit / sum w_master        (the elevation, measured)
    lambda_model    = sum w_exact / sum w_master    (the elevation, this front)
    ratio_exact     = sum hit / sum w_exact         (must be 1 if the claim holds)

`P_lead = 1/(1-rho)` -- the constant that phi_CAND/phi_EPSR use -- is printed
alongside.  The same three numbers are also accumulated using the walk's REAL live
arc starts instead of the exogenous probe, as a cross-check that the exogenous set
is a faithful stand-in.

Own implementation; imports only `elev_mc` and `elev_formula` from THIS subfolder.
"""
import argparse
import json
import math
import time

import numpy as np
from bisect import bisect_right

import elev_formula as F
import elev_mc as MC

BIN_EDGES = np.array([0.0, 0.005, 0.010, 0.020, 0.035, 0.060, 0.100, 0.180, 1.0])
NB = len(BIN_EDGES) - 1


def probe_cell(n, b, c, n_inst, walks_per_inst, seed, M_test=1000, audit=True):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    rho = 1.0 - (1.0 - c / n) ** b

    # per-instance accumulators, one row per instance (cluster bootstrap unit)
    acc = np.zeros((n_inst, NB, 6))   # hit, w_exact, w_master, hitL, wL_exact, wL_master
    n_steps_total = 0
    n_walks = 0
    n_cyc = 0
    audit_fail = 0
    t0 = time.time()

    for inst_i in range(n_inst):
        pi = rng.permutation(n).astype(np.int32)
        seed_mask = rng.random(n) < (c / n)
        seed_idx = np.flatnonzero(seed_mask).astype(np.int32)
        R = MC.build_R(pi, seed_idx, n, b)
        Urem = MC.build_Urem(pi, seed_idx, n, b)
        nU = int(Urem.sum())
        notR_idx = np.flatnonzero(~R)

        cand = np.flatnonzero(Urem & ~R)
        Yt = rng.choice(cand, size=min(M_test, cand.size), replace=False)
        in_test = np.zeros(n, dtype=bool)
        in_test[Yt] = True
        M_here = int(in_test.sum())

        stamp = np.zeros(n, dtype=np.int32)      # visited stamp
        is_arc = np.zeros(n, dtype=np.int32)     # arc-start stamp
        cons = np.zeros(n, dtype=np.int32)       # "already used as a pi-image" stamp
        cur_stamp = 0

        # python-level aliases (the inner loop is hot)
        piL = pi.tolist()
        RL = R.tolist()
        UL = Urem.tolist()
        inTL = in_test.tolist()
        edges = BIN_EDGES.tolist()
        binacc = [0.0] * (NB * 6)
        notR_list = notR_idx
        draws = None
        di = 0

        for w in range(walks_per_inst):
            cur_stamp += 1
            x0 = int(notR_list[rng.integers(0, notR_list.size)])
            stamp[x0] = cur_stamp
            is_arc[x0] = cur_stamp
            n_vis = 1
            consumed = 0
            n_test_live = M_here
            K = 1
            K_inU = 1 if UL[x0] else 0
            cur = x0
            cyclic = False
            n_walks += 1

            while True:
                if RL[cur]:
                    # --- reroute: chain of uniform f-draws
                    if draws is None or di >= draws.size:
                        draws = rng.integers(0, n, size=8192)
                        di = 0
                    D = int(draws[di])
                    di += 1
                    if stamp[D] == cur_stamp:
                        cyclic = (D == x0)
                        break
                    stamp[D] = cur_stamp
                    n_vis += 1
                    if RL[D]:
                        cur = D               # chain continues
                        continue
                    is_arc[D] = cur_stamp
                    K += 1
                    if UL[D]:
                        K_inU += 1
                    cur = D
                    continue

                # --- normal pi-step from cur (cur not in R)
                s = n_vis / n
                pool = nU - consumed
                y = piL[cur]
                if audit and (n_steps_total & 4095) == 0:
                    # deterministic checks: the image must live in U_rem, and must
                    # not have been consumed already (injectivity)
                    if (not UL[y]) or cons[y] == cur_stamp:
                        audit_fail += 1
                bi = bisect_right(edges, s) - 1
                if bi < 0:
                    bi = 0
                elif bi >= NB:
                    bi = NB - 1
                o = bi * 6
                wm = n_test_live / ((1.0 - s) * n)
                binacc[o + 1] += n_test_live / pool
                binacc[o + 2] += wm
                binacc[o + 4] += K_inU / pool
                binacc[o + 5] += K / ((1.0 - s) * n)
                if inTL[y]:
                    binacc[o] += 1.0
                    n_test_live -= 1
                if is_arc[y] == cur_stamp:
                    binacc[o + 3] += 1.0
                n_steps_total += 1

                consumed += 1
                cons[y] = cur_stamp
                if stamp[y] == cur_stamp:
                    cyclic = (y == x0)
                    break
                stamp[y] = cur_stamp
                n_vis += 1
                cur = y

            if cyclic:
                n_cyc += 1

        acc[inst_i] = np.array(binacc).reshape(NB, 6)

    wall = time.time() - t0

    # ---- bin summaries with a cluster bootstrap over instances
    B = 2000
    rb = np.random.default_rng(np.random.SeedSequence([seed, 55555]))
    idx = rb.integers(0, n_inst, size=(B, n_inst))
    boot = acc[idx].sum(axis=1)          # B x NB x 6
    tot = acc.sum(axis=0)                # NB x 6

    bins = []
    for k in range(NB):
        h, we, wm, hL, weL, wmL = tot[k]
        if wm <= 0:
            continue
        lam_meas = h / wm
        lam_model = we / wm
        ratio = h / we if we > 0 else float("nan")
        bh, bwe, bwm, bhL, bweL, bwmL = (boot[:, k, j] for j in range(6))
        with np.errstate(invalid="ignore", divide="ignore"):
            lam_meas_b = bh / bwm
            ratio_b = bh / bwe
            lam_measL_b = bhL / bwmL
            ratioL_b = bhL / bweL
        bins.append(dict(
            bin=k, lo=float(BIN_EDGES[k]), hi=float(BIN_EDGES[k + 1]),
            n_hits=float(h), n_hitsL=float(hL),
            lam_measured=float(lam_meas), sem_lam=float(np.nanstd(lam_meas_b, ddof=1)),
            lam_model=float(lam_model),
            ratio_exact=float(ratio), sem_ratio=float(np.nanstd(ratio_b, ddof=1)),
            lam_measured_live=float(hL / wmL) if wmL > 0 else float("nan"),
            sem_lam_live=float(np.nanstd(lam_measL_b, ddof=1)),
            lam_model_live=float(weL / wmL) if wmL > 0 else float("nan"),
            ratio_exact_live=float(hL / weL) if weL > 0 else float("nan"),
            sem_ratio_live=float(np.nanstd(ratioL_b, ddof=1)),
        ))

    # aggregate (all bins pooled)
    H, WE, WM, HL, WEL, WML = tot.sum(axis=0)
    agg = dict(
        lam_measured=float(H / WM), lam_model=float(WE / WM), ratio_exact=float(H / WE),
        lam_measured_live=float(HL / WML), lam_model_live=float(WEL / WML),
        ratio_exact_live=float(HL / WEL),
    )
    bH, bWE, bWM, bHL, bWEL, bWML = (boot.sum(axis=1)[:, j] for j in range(6))
    agg["sem_lam"] = float(np.nanstd(bH / bWM, ddof=1))
    agg["sem_ratio"] = float(np.nanstd(bH / bWE, ddof=1))
    agg["sem_lam_live"] = float(np.nanstd(bHL / bWML, ddof=1))
    agg["sem_ratio_live"] = float(np.nanstd(bHL / bWEL, ddof=1))

    return dict(n=n, b=b, c=c, rho=rho, P_lead=1.0 / (1.0 - rho),
                P_exact=(1.0 - c / n) ** (-(b - 1)),
                n_inst=n_inst, walks_per_inst=walks_per_inst, M_test=M_test,
                n_walks=n_walks, n_steps=n_steps_total, audit_fail=audit_fail,
                phi_notR_walk=n_cyc / n_walks, wall_s=wall, bins=bins, agg=agg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=65536)
    ap.add_argument("--b", type=int, required=True)
    ap.add_argument("--c", type=float, required=True)
    ap.add_argument("--inst", type=int, default=600)
    ap.add_argument("--walks", type=int, default=30)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    r = probe_cell(a.n, a.b, a.c, a.inst, a.walks, a.seed)
    json.dump(r, open(a.out, "w"), indent=1)
    print(f"n={r['n']} b={r['b']} c={r['c']:.0f} rho={r['rho']:.4f} P_lead={r['P_lead']:.4f} "
          f"walks={r['n_walks']} steps={r['n_steps']} audit_fail={r['audit_fail']} wall={r['wall_s']:.0f}s")
    print(f"{'bin':>16} {'hits':>9} | {'lam meas':>9} {'sem':>7} | {'lam model':>9} | "
          f"{'P_lead':>7} | {'ratio_exact':>11} {'sem':>7}")
    for bn in r["bins"]:
        print(f"[{bn['lo']:.3f},{bn['hi']:.3f}] {bn['n_hits']:>9.0f} | {bn['lam_measured']:>9.4f} "
              f"{bn['sem_lam']:>7.4f} | {bn['lam_model']:>9.4f} | {r['P_lead']:>7.4f} | "
              f"{bn['ratio_exact']:>11.5f} {bn['sem_ratio']:>7.5f}")
    a_ = r["agg"]
    print(f"{'AGG':>16} {'':>9} | {a_['lam_measured']:>9.4f} {a_['sem_lam']:>7.4f} | "
          f"{a_['lam_model']:>9.4f} | {r['P_lead']:>7.4f} | {a_['ratio_exact']:>11.5f} {a_['sem_ratio']:>7.5f}")


if __name__ == "__main__":
    main()
