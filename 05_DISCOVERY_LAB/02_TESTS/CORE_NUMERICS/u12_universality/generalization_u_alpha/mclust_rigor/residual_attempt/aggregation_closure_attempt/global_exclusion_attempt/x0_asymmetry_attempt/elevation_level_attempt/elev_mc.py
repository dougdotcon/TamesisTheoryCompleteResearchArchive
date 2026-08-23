#!/usr/bin/env python3
"""
elev_mc.py -- own M-CLUST(b) Monte-Carlo engine (wave 10 front (a)).

Written from the mechanism as stated in DERIVATION_MCLUST_FIXED.md SS1 /
`residual_attempt/ATTEMPT.md` SS1.  Nothing imported or copied from any script of
`residual_attempt/`, `aggregation_closure_attempt/`, `global_exclusion_attempt/`,
`x0_asymmetry_attempt/`, `x0_asymmetry_attempt/adversarial/`, `mclust_rigor/`, or
`ualpha_sim.py`.

Mechanism:
    pi          uniform permutation of [n]
    seed_i      i.i.d. Bernoulli(c/n), independent of pi
    block(s)    {s, pi(s), ..., pi^{b-1}(s)}
    R           union of blocks
    f(x)        uniform on [n], i.i.d., for x in R;  pi(x) otherwise

Per instance it reports the exact cyclic set of f and the three quantities
  phi      = |cyc| / n
  phi_notR = |cyc \\ R| / |R^c|
  eps      = |cyc & R| / |R|
accumulated as RATIOS OF SUMS across instances (the estimator that makes
phi = (1-rho) phi_notR + rho eps an exact identity; the referee's SS1(iii) point).

Three independent constructions are cross-checked in `selftest`:
  * R by forward pi-iteration from the seeds   vs  R by a backward membership test
  * cyclic set by adaptive iterated squaring   vs  cyclic set by in-degree peeling
    vs  brute-force orbit following on small maps
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np


# ---------------------------------------------------------------- construction

def build_R(pi, seed_idx, n, b):
    """R = union of blocks {s, pi(s), ..., pi^{b-1}(s)} over seeds s."""
    R = np.zeros(n, dtype=bool)
    pos = seed_idx.copy()
    for _ in range(b):
        R[pos] = True
        pos = pi[pos]
    return R


def build_R_backward(pi_inv, seed_mask, n, b):
    """Independent construction: x in R  iff  some pi^{-k}(x), 0<=k<=b-1, is a seed."""
    R = seed_mask.copy()
    pos = np.arange(n)
    for _ in range(1, b):
        pos = pi_inv[pos]
        R |= seed_mask[pos]
    return R


def build_Urem(pi, seed_idx, n, b):
    """U_rem = { y : NO seed among pi^{-1}(y), ..., pi^{-(b-1)}(y) }.
    Complement built forward: mark pi(s), ..., pi^{b-1}(s) for every seed s."""
    I = np.zeros(n, dtype=bool)
    if b > 1:
        pos = pi[seed_idx]
        for _ in range(b - 1):
            I[pos] = True
            pos = pi[pos]
    return ~I


def build_f(rng, pi, R, n):
    f = pi.copy()
    k = int(R.sum())
    if k:
        f[R] = rng.integers(0, n, size=k, dtype=np.int64).astype(pi.dtype)
    return f


def make_instance(rng, n, b, c, want_Urem=False):
    pi = rng.permutation(n).astype(np.int32)
    seed_mask = rng.random(n) < (c / n)
    seed_idx = np.flatnonzero(seed_mask).astype(np.int32)
    R = build_R(pi, seed_idx, n, b)
    f = build_f(rng, pi, R, n)
    out = dict(pi=pi, seed_mask=seed_mask, seed_idx=seed_idx, R=R, f=f)
    if want_Urem:
        out["Urem"] = build_Urem(pi, seed_idx, n, b)
    return out


# ------------------------------------------------------------------ cyclic set

def cyclic_mask_squaring(f, n):
    """image(f^m) for m >= n is exactly the set of cyclic points."""
    F = f
    k = 1
    while k < n:
        F = F[F]
        k *= 2
    m = np.zeros(n, dtype=bool)
    m[F] = True
    return m


def cyclic_mask_peel(f, n):
    """Independent construction: repeatedly delete points of in-degree 0."""
    indeg = np.bincount(f, minlength=n).astype(np.int32)
    alive = np.ones(n, dtype=bool)
    frontier = np.flatnonzero(indeg == 0)
    while frontier.size:
        alive[frontier] = False
        tgt = f[frontier]
        np.subtract.at(indeg, tgt, 1)
        cand = tgt[indeg[tgt] == 0]
        frontier = np.unique(cand[alive[cand]])
    return alive


def cyclic_mask_bruteforce(f, n):
    """Follow every orbit explicitly (only for tiny n, used in selftest)."""
    out = np.zeros(n, dtype=bool)
    for x in range(n):
        seen = {}
        y = x
        step = 0
        while y not in seen:
            seen[y] = step
            y = int(f[y])
            step += 1
        # x is cyclic iff x itself lies on the cycle reached from x
        cyc_start = seen[y]
        out[x] = seen[x] >= cyc_start
    return out


# ---------------------------------------------------------------- measurements

def run_cell(n, b, c, n_rep, seed_seq, audit_every=200, report_notR=True):
    rng = np.random.default_rng(seed_seq)
    tot_cyc = 0
    tot_cycR = 0
    tot_R = 0
    tot_chA = 0   # cyclic point of R reached by a normal pi-step (run-start channel)
    tot_chB = 0   # cyclic point of R reached by an f-draw
    per_inst = []          # (cyc, cycR, R, chA, chB) for the cluster bootstrap
    n_audit = 0
    t0 = time.time()
    for i in range(n_rep):
        inst = make_instance(rng, n, b, c)
        f, R, pi = inst["f"], inst["R"], inst["pi"]
        cyc = cyclic_mask_squaring(f, n)
        if audit_every and (i % audit_every == 0):
            assert np.array_equal(cyc, cyclic_mask_peel(f, n)), "cyclic-set audit failed"
            n_audit += 1
        nc = int(cyc.sum())
        nR = int(R.sum())
        cycR = cyc & R
        ncR = int(cycR.sum())
        # channel split for the cyclic points of R: look at the unique f-predecessor
        # on the cycle.  x cyclic  =>  its cycle predecessor y satisfies f(y)=x.
        chA = chB = 0
        if ncR:
            idx = np.flatnonzero(cycR)
            # predecessor of x among cyclic points: invert f restricted to cyc
            pred = np.full(n, -1, dtype=np.int64)
            ci = np.flatnonzero(cyc)
            pred[f[ci]] = ci
            y = pred[idx]
            chA = int(np.count_nonzero(~R[y]))     # y not in R  => f(y)=pi(y): normal step
            chB = ncR - chA
        tot_cyc += nc
        tot_cycR += ncR
        tot_R += nR
        tot_chA += chA
        tot_chB += chB
        per_inst.append((nc, ncR, nR, chA, chB))
    per_inst = np.array(per_inst, dtype=np.float64)
    wall = time.time() - t0

    N = float(n) * n_rep
    phi = tot_cyc / N
    eps = tot_cycR / tot_R if tot_R else float("nan")
    phi_notR = (tot_cyc - tot_cycR) / (N - tot_R)

    # cluster bootstrap over instances
    B = 3000
    rb = np.random.default_rng(np.random.SeedSequence([int(seed_seq.entropy) if hasattr(seed_seq, "entropy") else 0, 987654321]))
    # chunked so that the resampling never materialises a B x n_rep x 5 array
    # (that is several GB at n_rep = 4e4 and was OOM-killing workers)
    S = np.empty((B, 5))
    CH = max(1, int(2e7 // max(n_rep, 1)))
    done = 0
    while done < B:
        m_ = min(CH, B - done)
        idx = rb.integers(0, n_rep, size=(m_, n_rep))
        S[done:done + m_] = per_inst[idx].sum(axis=1)
        done += m_
    phi_b = S[:, 0] / N
    eps_b = S[:, 1] / np.maximum(S[:, 2], 1.0)
    notR_b = (S[:, 0] - S[:, 1]) / (N - S[:, 2])
    chA_b = S[:, 3] / np.maximum(S[:, 2], 1.0)
    chB_b = S[:, 4] / np.maximum(S[:, 2], 1.0)

    return dict(
        n=n, b=b, c=c, n_rep=n_rep,
        rho_formula=1.0 - (1.0 - c / n) ** b,
        rho_measured=tot_R / N,
        phi_mc=phi, sem_phi=float(phi_b.std(ddof=1)),
        eps=eps, sem_eps=float(eps_b.std(ddof=1)),
        phi_notR=phi_notR, sem_phi_notR=float(notR_b.std(ddof=1)),
        chA=tot_chA / tot_R if tot_R else float("nan"), sem_chA=float(chA_b.std(ddof=1)),
        chB=tot_chB / tot_R if tot_R else float("nan"), sem_chB=float(chB_b.std(ddof=1)),
        n_cyc_total=tot_cyc, n_cycR_total=tot_cycR, n_R_total=tot_R,
        n_audit=n_audit, wall_s=wall,
    )


# -------------------------------------------------------------------- selftest

def selftest():
    ok = True
    rng = np.random.default_rng(np.random.SeedSequence(20260823800))

    print("== cyclic set: squaring vs peeling vs brute force (n small) ==")
    for trial in range(300):
        n = int(rng.integers(3, 40))
        f = rng.integers(0, n, size=n).astype(np.int32)
        a = cyclic_mask_squaring(f, n)
        b_ = cyclic_mask_peel(f, n)
        c_ = cyclic_mask_bruteforce(f, n)
        if not (np.array_equal(a, b_) and np.array_equal(a, c_)):
            print("  FAIL at trial", trial, n, f, a.astype(int), b_.astype(int), c_.astype(int))
            ok = False
            break
    else:
        print("  [ok ] 300 random small maps agree on all three algorithms")

    print("== R: forward block painting vs backward membership test ==")
    for (n, b, c) in ((4096, 1, 50.0), (4096, 8, 40.0), (8192, 50, 150.0), (8192, 200, 60.0)):
        bad = 0
        for _ in range(30):
            pi = rng.permutation(n).astype(np.int32)
            sm = rng.random(n) < (c / n)
            si = np.flatnonzero(sm).astype(np.int32)
            pi_inv = np.empty(n, dtype=np.int32)
            pi_inv[pi] = np.arange(n, dtype=np.int32)
            R1 = build_R(pi, si, n, b)
            R2 = build_R_backward(pi_inv, sm, n, b)
            bad += int(not np.array_equal(R1, R2))
        print(f"  [{'ok ' if bad == 0 else 'FAIL'}] n={n} b={b} c={c}: {bad} mismatches / 30")
        ok = ok and bad == 0

    print("== densities: |R|/n vs rho, run starts vs rho_start, |U_rem|/n vs (1-c/n)^(b-1) ==")
    for (n, b, c) in ((65536, 100, 400.0), (65536, 300, 150.0), (65536, 400, 100.0), (65536, 1, 50.0)):
        vals = []
        M = 400
        for _ in range(M):
            pi = rng.permutation(n).astype(np.int32)
            sm = rng.random(n) < (c / n)
            si = np.flatnonzero(sm).astype(np.int32)
            pi_inv = np.empty(n, dtype=np.int32)
            pi_inv[pi] = np.arange(n, dtype=np.int32)
            R = build_R(pi, si, n, b)
            U = build_Urem(pi, si, n, b)
            runstart = R & ~R[pi_inv]
            vals.append([R.mean(), runstart.mean(), U.mean()])
        vals = np.array(vals)
        acc = vals.mean(axis=0)
        sem = vals.std(axis=0, ddof=1) / math.sqrt(M)
        pr = 1 - (1 - c / n) ** b
        prs = (c / n) * (1 - c / n) ** b
        pu = (1 - c / n) ** (b - 1)
        print(f"  b={b:>4} c={c:>6.0f}: rho {acc[0]:.6f}+-{sem[0]:.6f} vs {pr:.6f} (z={(acc[0]-pr)/sem[0]:+.2f})"
              f" | rho_start {acc[1]:.4e}+-{sem[1]:.1e} vs {prs:.4e} (z={(acc[1]-prs)/sem[1]:+.2f})"
              f" | |U_rem|/n {acc[2]:.6f}+-{sem[2]:.6f} vs {pu:.6f} (z={(acc[2]-pu)/sem[2]:+.2f})")
        for i, (want, nm) in enumerate(((pr, "rho"), (prs, "rho_start"), (pu, "Urem"))):
            z = (acc[i] - want) / sem[i]
            if abs(z) > 4.0:
                print(f"    FAIL {nm}: z={z:.3g}")
                ok = False

    print("== shadowing: x notin R  =>  pi(x) notin R\\RunStarts, and pi(x) in U_rem ==")
    for (n, b, c) in ((65536, 100, 400.0), (65536, 300, 150.0)):
        for _ in range(10):
            pi = rng.permutation(n).astype(np.int32)
            sm = rng.random(n) < (c / n)
            si = np.flatnonzero(sm).astype(np.int32)
            pi_inv = np.empty(n, dtype=np.int32)
            pi_inv[pi] = np.arange(n, dtype=np.int32)
            R = build_R(pi, si, n, b)
            U = build_Urem(pi, si, n, b)
            notR = np.flatnonzero(~R)
            img = pi[notR]
            runstart = R & ~R[pi_inv]
            bad1 = int(np.count_nonzero(R[img] & ~runstart[img]))
            bad2 = int(np.count_nonzero(~U[img]))
            if bad1 or bad2:
                print(f"  FAIL b={b}: {bad1} images in R\\RunStarts, {bad2} images outside U_rem")
                ok = False
                break
        else:
            print(f"  [ok ] b={b} c={c}: pi(R^c) subset of U_rem and meets R only at run starts")

    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(0 if selftest() else 1)
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--b", type=int, required=True)
    ap.add_argument("--c", type=float, required=True)
    ap.add_argument("--reps", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    r = run_cell(a.n, a.b, a.c, a.reps, np.random.SeedSequence(a.seed))
    json.dump(r, open(a.out, "w"), indent=1)
    print(json.dumps(r))
