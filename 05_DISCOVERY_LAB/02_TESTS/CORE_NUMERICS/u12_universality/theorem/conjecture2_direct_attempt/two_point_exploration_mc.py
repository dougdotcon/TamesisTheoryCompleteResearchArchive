"""
NUMERICALLY EXPLORED (not proof) -- ATTEMPT.md Section 3.4-3.5.

Goal: directly measure, from the finite-n discrete model M_n(c)
(Definition 1 of THEOREM.md: uniform permutation + independent
Bernoulli(c/n) reroutes to a uniform target), the conditional joint
probability

    g(ell) := P(point 0 cyclic AND point 1 cyclic | same background
                pi-cycle, of length ell)

as a function of ell/n, and compare it against two analytically simple
CANDIDATE closed forms:

  (a) "perfect same-fate correlation" guess: g(ell) = exp(-c * ell^2)
      -- IDENTICAL to Theorem 1's single-point marginal
      P(cyclic | own block length = ell). This is what g(ell) would
      equal if, given they share a block, points 0 and 1 were ALWAYS
      cyclic together or not together (rho=1 in the normalized-
      correlation sense of correlation_ratio_analysis.py). NOTE (added
      after an initial mislabel, corrected here -- see ATTEMPT.md
      Section 3.5's Honest process note): this quantity is NOT the
      "fully-intact-block" probability -- that smaller, EXACTLY provable
      quantity is (1-c/n)^ell -> exp(-c*ell) as n->infinity, verified
      separately in intact_block_lower_bound_check.py, and is a genuine
      rigorous LOWER bound on g(ell) (zero violations over 5000+
      verified trials), strictly below exp(-c*ell^2) since ell<1.
  (b) "conditionally independent" guess: g(ell) = exp(-2*c*ell^2)
      (i.e. as if, given ell, points 0 and 1's cyclic statuses were
      independent draws each with marginal success probability
      exp(-c ell^2); rho=0 in the same sense).

This is exploratory data informing the OPEN sub-problem named in
ATTEMPT.md Section 3.4 (the joint mark-exploration step), not a proof,
and not new evidence toward Conjecture 2 itself (which concerns the
UNCONDITIONAL law of M(c), not this conditional quantity -- a quantity
that does not appear anywhere in THEOREM.md and is introduced fresh in
this document).

Cyclic-set computation uses the standard O(n) functional-graph
peeling algorithm (repeatedly strip in-degree-0 nodes; survivors are
exactly the cyclic points).
"""
import numpy as np
from collections import deque
import json
import sys

def cyclic_mask(f, n):
    indeg = np.bincount(f, minlength=n)
    removed = np.zeros(n, dtype=bool)
    q = deque(int(i) for i in np.nonzero(indeg == 0)[0])
    while q:
        i = q.popleft()
        removed[i] = True
        j = int(f[i])
        indeg[j] -= 1
        if indeg[j] == 0 and not removed[j]:
            q.append(j)
    return ~removed  # True = cyclic


def pi_cycle_containing_0(pi, n):
    # trace forward from 0 under pi until back to 0; return (in_same_set(1), length)
    y = pi[0]
    length = 1
    found1 = (y == 1)
    while y != 0:
        y = pi[y]
        length += 1
        if y == 1:
            found1 = True
    return found1, length


def run(c, n, trials, seed):
    rng = np.random.default_rng(seed)
    same_ell = []       # ell values where points 0,1 shared a pi-cycle
    same_both_cyc = []  # 1/0 whether both cyclic, aligned with same_ell
    marginal_cyc_frac = []  # per-trial fraction cyclic (for M(c)^2 sanity check)
    marginal_pt_cyc = []    # per-trial: is point 0 cyclic (for phi_infty(c) sanity check)
    all_ell = []             # own pi-cycle length of point 0, EVERY trial (not just same-cycle)
    all_pt0_cyc = []         # whether point 0 is cyclic, EVERY trial -- to measure the TRUE
                              # finite-n marginal P(point0 cyclic | own cycle length = ell)
                              # directly, as an independent check on whether guessA=exp(-c*ell^2)
                              # is even a good approximation to the correct finite-n marginal
                              # (as opposed to just the n->infinity continuum target).

    for t in range(trials):
        pi = rng.permutation(n)
        same, ell = pi_cycle_containing_0(pi, n)

        reroute = rng.random(n) < (c / n)
        targets = rng.integers(0, n, size=n)
        f = np.where(reroute, targets, pi)

        cmask = cyclic_mask(f, n)
        marginal_cyc_frac.append(cmask.mean())
        marginal_pt_cyc.append(bool(cmask[0]))
        all_ell.append(ell)
        all_pt0_cyc.append(bool(cmask[0]))

        if same:
            same_ell.append(ell)
            same_both_cyc.append(bool(cmask[0]) and bool(cmask[1]))

    return {
        "c": c, "n": n, "trials": trials, "seed": seed,
        "same_ell": same_ell,
        "same_both_cyc": same_both_cyc,
        "marginal_cyc_frac": marginal_cyc_frac,
        "marginal_pt_cyc": marginal_pt_cyc,
        "all_ell": all_ell,
        "all_pt0_cyc": all_pt0_cyc,
    }


def bucket_marginal(result, nbins=8):
    """Bucket the TRUE finite-n marginal P(point0 cyclic | own cycle length=ell)
    against guessA=exp(-c*ell^2), using EVERY trial (not conditioned on point 1
    at all) -- a direct check of whether guessA is a good approximation to the
    finite-n marginal itself, independent of any joint-probability question."""
    n = result["n"]
    c = result["c"]
    ell = np.array(result["all_ell"], dtype=float) / n
    cyc = np.array(result["all_pt0_cyc"], dtype=float)
    edges = np.linspace(0, 1, nbins + 1)
    rows = []
    for b in range(nbins):
        lo, hi = edges[b], edges[b + 1]
        sel = (ell >= lo) & (ell < hi) if b < nbins - 1 else (ell >= lo) & (ell <= hi)
        cnt = int(sel.sum())
        if cnt == 0:
            continue
        mid = 0.5 * (lo + hi)
        emp = cyc[sel].mean()
        se = cyc[sel].std(ddof=1) / np.sqrt(cnt) if cnt > 1 else float('nan')
        guessA = np.exp(-c * mid**2)
        rows.append({
            "ell_mid": mid, "n_samples": cnt, "empirical_marginal": emp, "se": se,
            "guessA_exp(-c*ell^2)": guessA,
            "z_vs_A": (emp - guessA) / se if se == se and se > 0 else None,
        })
    return rows


def bucket_analysis(result, nbins=8):
    n = result["n"]
    c = result["c"]
    ell = np.array(result["same_ell"], dtype=float) / n
    both = np.array(result["same_both_cyc"], dtype=float)
    edges = np.linspace(0, 1, nbins + 1)
    rows = []
    for b in range(nbins):
        lo, hi = edges[b], edges[b + 1]
        sel = (ell >= lo) & (ell < hi) if b < nbins - 1 else (ell >= lo) & (ell <= hi)
        cnt = int(sel.sum())
        if cnt == 0:
            continue
        mid = 0.5 * (lo + hi)
        emp = both[sel].mean()
        se = both[sel].std(ddof=1) / np.sqrt(cnt) if cnt > 1 else float('nan')
        guessA = np.exp(-c * mid**2)          # fully-intact-only
        guessB = np.exp(-2 * c * mid**2)      # naive independence
        rows.append({
            "ell_mid": mid, "n_samples": cnt,
            "empirical_g": emp, "se": se,
            "guessA_exp(-c*ell^2)": guessA,
            "guessB_exp(-2c*ell^2)": guessB,
            "z_vs_A": (emp - guessA) / se if se == se and se > 0 else None,
            "z_vs_B": (emp - guessB) / se if se == se and se > 0 else None,
        })
    return rows


if __name__ == "__main__":
    c = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 40000
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 20260858010
    outfile = sys.argv[5] if len(sys.argv) > 5 else "two_point_exploration_mc_results.json"
    print(f"Running MC: c={c}, n={n}, trials={trials}, seed={seed}")
    result = run(c, n, trials, seed)

    mf = np.array(result["marginal_cyc_frac"])
    mp = np.array(result["marginal_pt_cyc"], dtype=float)
    target_mean = 0.5 * np.sqrt(np.pi / c) if c > 0 else 1.0
    import math
    target_mean = math.erf(math.sqrt(c)) * 0.5 * math.sqrt(math.pi / c)
    target_2mom = (1 - math.exp(-c)) / c
    print(f"marginal P(point0 cyclic) MC = {mp.mean():.5f}  (target phi_infty({c})={target_mean:.5f})")
    print(f"E[fraction cyclic]   MC = {mf.mean():.5f}  (target phi_infty({c})={target_mean:.5f})")
    print(f"E[(fraction cyclic)^2] MC = {(mf**2).mean():.5f}  (target (1-e^-c)/c={target_2mom:.5f})")
    print(f"n_same_cycle_trials = {len(result['same_ell'])} / {trials}  (target ~0.5)")

    rows = bucket_analysis(result, nbins=8)
    print()
    print("Conditional JOINT g(ell) = P(both cyclic | same pi-cycle, length ell):")
    print(f"{'ell_mid':>8} {'n':>6} {'empirical_g':>12} {'se':>10} {'guessA':>10} {'z_A':>8} {'guessB':>10} {'z_B':>8}")
    for r in rows:
        zA = f"{r['z_vs_A']:.2f}" if r['z_vs_A'] is not None else "  n/a"
        zB = f"{r['z_vs_B']:.2f}" if r['z_vs_B'] is not None else "  n/a"
        print(f"{r['ell_mid']:8.3f} {r['n_samples']:6d} {r['empirical_g']:12.5f} {r['se']:10.5f} "
              f"{r['guessA_exp(-c*ell^2)']:10.5f} {zA:>8} {r['guessB_exp(-2c*ell^2)']:10.5f} {zB:>8}")

    mrows = bucket_marginal(result, nbins=8)
    print()
    print("TRUE finite-n MARGINAL P(point0 cyclic | own cycle length ell) vs guessA (sanity check):")
    print(f"{'ell_mid':>8} {'n':>6} {'empirical_marg':>14} {'se':>10} {'guessA':>10} {'z_A':>8}")
    for r in mrows:
        zA = f"{r['z_vs_A']:.2f}" if r['z_vs_A'] is not None else "  n/a"
        print(f"{r['ell_mid']:8.3f} {r['n_samples']:6d} {r['empirical_marginal']:14.5f} {r['se']:10.5f} "
              f"{r['guessA_exp(-c*ell^2)']:10.5f} {zA:>8}")

    out = {
        "c": c, "n": n, "trials": trials, "seed": seed,
        "marginal_pt_cyc_mean": float(mp.mean()),
        "marginal_cyc_frac_mean": float(mf.mean()),
        "marginal_cyc_frac_sq_mean": float((mf**2).mean()),
        "target_mean_phi_infty": target_mean,
        "target_second_moment": target_2mom,
        "n_same_cycle_trials": len(result["same_ell"]),
        "bucket_rows": rows,
        "marginal_bucket_rows": mrows,
    }
    with open(outfile, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nWrote {outfile}")
