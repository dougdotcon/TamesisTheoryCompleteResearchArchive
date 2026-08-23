"""
ref_common.py -- referee's own from-scratch measurement helpers for the
adversarial review of floor_closed_form_attempt/ATTEMPT.md.

Written without reading or importing any of that front's own scripts
(fcd_t0.py..fcd_t3.py, derive_closed_form.py, solve_2d_system.py,
check_formula_heuristic.py, abstract_sim.py, explore_phiL.py,
explore_ndep.py). Only sc_engine.py / sc_formula.py (parent lineage,
already-adversarially-verified infrastructure) are imported, per the
mandate's explicit permission, plus numpy/scipy.

At b=1, sc_engine.build_R_mask reduces R to exactly seed_mask (re-verified
directly below in ref_identity_check.py), so "x0 not a seed" ==
"seed_mask[x0]==False" is used throughout as the definition of x0 in R^c.
"""

import os
import sys
import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_SC_DIR = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
if _SC_DIR not in sys.path:
    sys.path.insert(0, _SC_DIR)

import sc_engine as E  # noqa: E402
import sc_formula as F  # noqa: E402


def run_one_instance_binned(n, c, rng, bin_edges):
    """Build one b=1 instance and return, for the non-seed points only:
      - per-bin point counts (n_bins,)
      - per-bin sums of the cyclic outcome (0/1) (n_bins,)
      - per-bin per-INSTANCE mean outcome (n_bins,) with nan where the bin
        got zero points in this instance (for cluster-level aggregation)
    bin_edges: array of length n_bins+1, bins are [edges[i], edges[i+1]) in
    L-space except the last bin which is closed on the right (L<=n).
    """
    pi = E.build_pi(n, rng)
    seed_mask = E.build_seeds(n, c, rng)
    # b=1: R = seed_mask exactly (re-verified in ref_identity_check.py)
    R_mask = seed_mask
    f = E.build_f(n, pi, R_mask, rng)
    cyclic_mask = E.cyclic_mask_peeling(f)
    cyc_len = E.pi_cycle_lengths(pi)

    not_seed = ~seed_mask
    L = cyc_len[not_seed]
    outcome = cyclic_mask[not_seed].astype(np.float64)

    n_bins = len(bin_edges) - 1
    # bins[i] <= x < bins[i+1] via searchsorted(side='right')-1. Points with
    # idx==-1 (L below the first edge) or idx>=n_bins do NOT belong to any
    # bin and must be EXCLUDED, not clipped into bin 0/n_bins-1 -- clipping
    # would silently contaminate the boundary bins with out-of-range points
    # (caught during self-test: a first bug in this exact spot inflated the
    # (2000,4000] bin by dumping every L<2000 short-cycle point into it).
    idx_raw = np.searchsorted(bin_edges, L, side="right") - 1
    valid = (idx_raw >= 0) & (idx_raw < n_bins)
    idx = idx_raw[valid]
    outcome_v = outcome[valid]
    counts = np.bincount(idx, minlength=n_bins).astype(np.float64)
    sums = np.bincount(idx, weights=outcome_v, minlength=n_bins)

    inst_means = np.full(n_bins, np.nan)
    nz = counts > 0
    inst_means[nz] = sums[nz] / counts[nz]

    return counts, sums, inst_means


def phi_far_direct_and_binned(n, c, rng, threshold, bin_edges):
    """One instance: measure phi_far(threshold) directly (condition L>threshold
    among non-seed points) AND via the same instance's per-bin counts/sums,
    for the T0-style identity cross-check. bin_edges must cover (threshold, n]
    exactly with the SAME instance data (reuse, not redraw)."""
    pi = E.build_pi(n, rng)
    seed_mask = E.build_seeds(n, c, rng)
    R_mask = seed_mask
    f = E.build_f(n, pi, R_mask, rng)
    cyclic_mask = E.cyclic_mask_peeling(f)
    cyc_len = E.pi_cycle_lengths(pi)

    not_seed = ~seed_mask
    L = cyc_len[not_seed]
    outcome = cyclic_mask[not_seed].astype(np.float64)

    far_mask = L > threshold
    direct_count = far_mask.sum()
    direct_sum = outcome[far_mask].sum()

    n_bins = len(bin_edges) - 1
    idx = np.searchsorted(bin_edges, L, side="right") - 1
    valid = (idx >= 0) & (idx < n_bins) & far_mask
    idxv = idx[valid]
    countsb = np.bincount(idxv, minlength=n_bins).astype(np.float64)
    sumsb = np.bincount(idxv, weights=outcome[valid], minlength=n_bins)

    return direct_count, direct_sum, countsb, sumsb


def candidate1_pred(L_mid, c, n):
    t0 = L_mid / n
    return np.exp(-c * t0 * t0)


def derive_instance_seeds(master_seed, N):
    """Deterministic, reproducible per-instance uint32 seeds derived from a
    single master seed via numpy's SeedSequence.generate_state -- documented
    derivation, not an ad hoc re-seed. Distinct master_seed -> disjoint
    seed streams for all practical purposes (PCG64 generate_state output)."""
    ss = np.random.SeedSequence(master_seed)
    return ss.generate_state(N, dtype=np.uint32)


def run_parallel(n, c, master_seed, N, bin_edges, n_workers=4, chunk=250):
    """Run N instances of run_one_instance_binned across n_workers processes.
    Returns (total_counts, total_sums, inst_means matrix [N, n_bins])."""
    import concurrent.futures
    import ref_mp_worker as W

    seeds = derive_instance_seeds(master_seed, N)
    batches = [seeds[i:i + chunk] for i in range(0, N, chunk)]
    args = [(n, c, b, bin_edges) for b in batches]

    n_bins = len(bin_edges) - 1
    total_counts = np.zeros(n_bins)
    total_sums = np.zeros(n_bins)
    inst_means_chunks = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as ex:
        for tc, ts, im in ex.map(W.run_batch, args):
            total_counts += tc
            total_sums += ts
            inst_means_chunks.append(im)

    inst_means = np.concatenate(inst_means_chunks, axis=0)
    return total_counts, total_sums, inst_means
