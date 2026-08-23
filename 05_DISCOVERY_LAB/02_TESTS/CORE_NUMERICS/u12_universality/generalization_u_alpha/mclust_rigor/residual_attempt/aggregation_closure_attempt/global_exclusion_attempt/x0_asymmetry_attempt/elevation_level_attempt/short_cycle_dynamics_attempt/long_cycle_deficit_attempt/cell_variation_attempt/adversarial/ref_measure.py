"""
ref_measure.py -- REFEREE's own from-scratch far-tail measurement code for
cell_variation_attempt.

Independence discipline (per the referee mandate):
  - Imports ONLY sc_engine.py / sc_formula.py (short_cycle_dynamics_attempt/,
    three directories up from this adversarial/ folder), already
    adversarially verified SOUND by two independent referees earlier in this
    lineage. These are treated as trusted infrastructure, exactly as every
    prior referee in this lineage has done.
  - Does NOT import, open, or read cv_measure.py, cv_grid.py, cv_analysis.py,
    or their .log files. The measurement logic below (definition of "far
    tail", the R^c / L>threshold population, the two-condition matched
    design) is re-derived directly from DERIVATION_PREREG.md's prose (S2)
    and cross-checked against short_cycle_dynamics_attempt/ATTEMPT.md's own
    T1 prose description (the (20b,infinity) far-tail bin), NOT from any
    front script.

Methodology (from DERIVATION_PREREG.md S2, re-derived independently):
  For a cell (b, c) at n=65536, threshold := 20*b (the ORIGINAL cell's own
  far-tail edge -- fixed once per cell, reused unchanged for the b=1
  companion condition):

  "own-b deficit": build an M-CLUST(b) instance at the cell's own b. Compute
    R_mask (union of b-point forward blocks from every seed), f (i.i.d.
    reroute inside R, pi outside), the pi-cycle length L(x) for every x, and
    the f-cyclic mask (in-degree peeling, exact). Restrict attention to
    points with R_mask[x]==False (x0 in R^c) AND L(x) > threshold. Estimate
    phi_far = P(x0 cyclic in f | x0 in R^c, L>threshold) by POOLING
    (sum of cyclic points in that population) / (sum of population size)
    across N independent instances (a ratio estimator, cluster=instance).
    Compare against phi_U(c''(b,c,n)) (sc_formula.c_double_prime /
    sc_formula.phi_U).

  "b=1 deficit": IDENTICAL measurement (same threshold=20*b_orig, same c,
    same n) but the underlying instance is built at b=1. Compare against
    phi_U(c''(1,c,n)) = phi_U(c) exactly (c''(1,c,n) = c*(1-c/n)^0 = c).

  H2 share := dev_b1% / dev_own%  (signed ratio of raw deviations), defined
  only when dev_own% < 0 and |z_own| >= 2 (matches DERIVATION_PREREG.md S2's
  locked exclusion rule).

SEM: Cochran-style ratio-estimator delta method, cluster = instance
  (independently re-derived here from first principles, not taken from any
  front or sibling-referee script -- see docstring on `ratio_estimator_sem`
  below for the derivation).

Parallelized across worker processes (multiprocessing.Pool) purely for
wall-clock feasibility -- verified bit-identical to single-process on a
throwaway seed before use (see ref_timing_check.py/.log).
"""

import sys
import os
import numpy as np
from collections import deque
import multiprocessing as mp

# --- import trusted infra (sc_engine.py, sc_formula.py), three dirs up ------
_HERE = os.path.dirname(os.path.abspath(__file__))
_SC_DIR = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
if _SC_DIR not in sys.path:
    sys.path.insert(0, _SC_DIR)

import sc_engine  # noqa: E402
import sc_formula  # noqa: E402


def cycle_lengths_fast(pi):
    """Cycle-length label for every point of permutation pi, O(n).
    Independently written (not sc_engine.pi_cycle_lengths): avoids an O(n)
    Python-level 'for start in range(n)' outer scan by using a vectorized
    np.argmax to find the next unvisited start (permutations of n=65536 have
    O(log n) distinct cycles, so this outer loop runs ~11-20 times, not n
    times). Cross-checked for exact agreement with sc_engine.pi_cycle_lengths
    below (ref_measure_selftest)."""
    n = pi.shape[0]
    remaining = np.ones(n, dtype=bool)
    cyc_len = np.empty(n, dtype=np.int64)
    while remaining.any():
        start = int(np.argmax(remaining))
        members = []
        x = start
        while remaining[x]:
            remaining[x] = False
            members.append(x)
            x = pi[x]
        L = len(members)
        cyc_len[np.array(members, dtype=np.int64)] = L
    return cyc_len


def one_instance_counts(n, b, c, threshold, rng):
    """Build one M-CLUST(b) instance; return (n_far, cyc_far) for the
    population {x : R_mask[x]==False and L(x) > threshold}."""
    inst = sc_engine.build_instance(n, b, c, rng)
    pi, R_mask, f = inst["pi"], inst["R_mask"], inst["f"]
    L = cycle_lengths_fast(pi)
    pop_mask = (~R_mask) & (L > threshold)
    n_far = int(pop_mask.sum())
    if n_far == 0:
        return 0, 0
    cyclic_mask = sc_engine.cyclic_mask_peeling(f)
    cyc_far = int(cyclic_mask[pop_mask].sum())
    return n_far, cyc_far


def _worker(args):
    n, b, c, threshold, seed_int = args
    rng = np.random.default_rng(seed_int)
    return one_instance_counts(n, b, c, threshold, rng)


def measure_far_tail(n, b, c, N, seed_seq, threshold, nworkers=4):
    """Pooled ratio estimator phi_far = sum(cyc_far_i) / sum(n_far_i) across
    N independent instances, plus per-instance (n_far_i, cyc_far_i) arrays
    for the delta-method SEM. Returns dict."""
    children = seed_seq.spawn(N)
    seed_ints = [int(c_.generate_state(1)[0]) for c_ in children]
    args = [(n, b, c, threshold, s) for s in seed_ints]
    if nworkers > 1:
        with mp.Pool(nworkers) as pool:
            results = pool.map(_worker, args, chunksize=max(1, N // (nworkers * 8)))
    else:
        results = [_worker(a) for a in args]
    n_far = np.array([r[0] for r in results], dtype=np.float64)
    cyc_far = np.array([r[1] for r in results], dtype=np.float64)
    return dict(n_far=n_far, cyc_far=cyc_far)


def ratio_estimator_sem(n_far, cyc_far):
    """Cochran ratio-estimator delta-method SEM for R = sum(y)/sum(x), with
    (x_i,y_i) = (n_far_i, cyc_far_i) treated as cluster-level (instance-level)
    sums (standard theory: e.g. Cochran 1977 SS6.9, "ratio estimator variance").

    Derivation (first principles): R_hat = Ybar/Xbar (Ybar,Xbar = sample means
    of y_i,x_i over N clusters). Let d_i = y_i - R_hat*x_i. To first order
    (delta method / Taylor expansion of the ratio around the true ratio),
    Var(R_hat) ~= Var(dbar)/Xbar^2 = [s_d^2/N] / Xbar^2, where
    s_d^2 = (1/(N-1)) sum (d_i - dbar)^2. Since dbar = Ybar - R_hat*Xbar = 0
    identically (R_hat is defined so this holds exactly), this simplifies to
    s_d^2 = (1/(N-1)) sum d_i^2 = (1/(N-1)) sum (y_i - R_hat*x_i)^2.
    So SEM(R_hat) = sqrt( sum((y_i-R_hat*x_i)^2) / (N-1) ) / (sqrt(N)*Xbar).
    """
    N = len(n_far)
    R_hat = cyc_far.sum() / n_far.sum()
    xbar = n_far.mean()
    d = cyc_far - R_hat * n_far
    s_d2 = np.sum(d ** 2) / (N - 1)
    sem = np.sqrt(s_d2 / N) / xbar
    return R_hat, sem


def phi_far_and_z(n, b, c, N, seed_seq, threshold, phi_ref, nworkers=4):
    """Full per-condition measurement: phi_far, SEM, dev%, z against phi_ref."""
    res = measure_far_tail(n, b, c, N, seed_seq, threshold, nworkers=nworkers)
    phi_far, sem = ratio_estimator_sem(res["n_far"], res["cyc_far"])
    dev_pct = 100.0 * (phi_far / phi_ref - 1.0)
    sem_pct = 100.0 * sem / phi_ref
    z = (phi_far - phi_ref) / sem
    total_pop = int(res["n_far"].sum())
    return dict(phi_far=phi_far, sem=sem, dev_pct=dev_pct, sem_pct=sem_pct,
                z=z, total_pop=total_pop, n_far=res["n_far"], cyc_far=res["cyc_far"])


def h2_share(dev_own_pct, dev_b1_pct, sem_own_pct, sem_b1_pct):
    """H2 share = dev_b1%/dev_own%, delta-method SEM for the ratio of two
    INDEPENDENT quantities (disjoint RNG streams -> independent samples):
    for R = A/B with A,B independent, Var(R)/R^2 ~= Var(A)/A^2 + Var(B)/B^2
    (standard delta-method result for a ratio of independent random
    variables, first order Taylor expansion around the means)."""
    share = dev_b1_pct / dev_own_pct
    rel_var = (sem_b1_pct / dev_b1_pct) ** 2 + (sem_own_pct / dev_own_pct) ** 2
    sem_share = abs(share) * np.sqrt(rel_var)
    return share, sem_share


if __name__ == "__main__":
    # Quick self-check: cycle_lengths_fast matches sc_engine.pi_cycle_lengths
    # exactly, on several random permutations. No RNG "data" claim -- pure
    # code-correctness smoke test; uses the archive's disclosed-throwaway
    # seed convention (9999000xx), OUTSIDE this referee's reserved
    # 20260840000+ range, discarded, not counted in any reported number.
    rng = np.random.default_rng(np.random.SeedSequence(999900020))
    fails = 0
    for trial in range(10):
        n = rng.integers(100, 5000)
        pi = rng.permutation(int(n))
        a = sc_engine.pi_cycle_lengths(pi)
        b = cycle_lengths_fast(pi)
        if not np.array_equal(a, b):
            fails += 1
            print(f"MISMATCH trial={trial} n={n}")
    print(f"cycle_lengths_fast selftest: {10-fails}/10 OK" if fails == 0
          else f"cycle_lengths_fast selftest: {fails} FAILURES")
    sys.exit(1 if fails else 0)
