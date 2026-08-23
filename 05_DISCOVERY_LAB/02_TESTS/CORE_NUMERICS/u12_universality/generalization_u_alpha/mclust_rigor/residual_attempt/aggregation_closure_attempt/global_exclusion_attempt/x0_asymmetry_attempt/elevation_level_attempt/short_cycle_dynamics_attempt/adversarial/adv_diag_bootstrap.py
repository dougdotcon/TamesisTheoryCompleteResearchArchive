"""
adv_diag_bootstrap.py -- follow-up stability check on the L-binned
near-b excess (Claim 3's most novel sub-claim). The first adv_diagnostic.py
run (seed 20260826010, target cell, N=2500) produced a much LARGER (b,2b]
excess (+874%) than ATTEMPT.md's own reported figure (+267.7%) for the
same cell -- both wildly significant by the delta-method z-score, yet
several sigma apart from each other. This script checks whether that is
(i) a real discrepancy, or (ii) an artefact of a heavy-tailed, rare-event
-dominated bin where the naive delta-method SE (which assumes the sample
variance of N~2000-2500 per-instance ratios is a reliable plug-in) understates
true between-run variability, by:
  (a) re-running the target cell with a FRESH, independent seed and larger N,
  (b) computing both the delta-method SE and a cluster (instance-level)
      bootstrap SE for the (b,2b] bin specifically,
  (c) reporting the empirical skewness / rare-event structure of the
      per-instance ratio in that bin.

Fresh seed, not reused elsewhere: SeedSequence(20260826030).
"""
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from adv_engine import build_instance, cyclic_mask_peeling
from adv_diagnostic import ratio_delta_sem
from adv_formula import c_pp, phi_U_scalar


def run_chunk(args):
    (b, c, n, n_inst, seed_entropy, edges) = args
    rng = np.random.default_rng(np.random.SeedSequence(seed_entropy))
    nbins = len(edges) - 1
    bin_total = np.zeros((nbins, n_inst), dtype=np.int64)
    bin_cyclic = np.zeros((nbins, n_inst), dtype=np.int64)
    for i in range(n_inst):
        inst = build_instance(n, b, c, rng)
        R = inst["R"]
        L = inst["cyc_len_pi"]
        f = inst["f"]
        cyc = cyclic_mask_peeling(f)
        Rc = ~R
        long_mask = Rc & (L > b)
        for k in range(nbins):
            lo, hi = edges[k], edges[k + 1]
            bmask = long_mask & (L > lo) & (L <= hi)
            bin_total[k, i] = bmask.sum()
            bin_cyclic[k, i] = (cyc & bmask).sum()
    return bin_total, bin_cyclic


def bootstrap_se(cyclic_arr, total_arr, n_boot=3000, rng=None):
    N = len(total_arr)
    rng = rng or np.random.default_rng(0)
    ratios = np.empty(n_boot)
    for bidx in range(n_boot):
        idx = rng.integers(0, N, size=N)
        tot = total_arr[idx].sum()
        cyc = cyclic_arr[idx].sum()
        ratios[bidx] = cyc / tot if tot > 0 else np.nan
    return np.nanmean(ratios), np.nanstd(ratios)


if __name__ == "__main__":
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        log.append(s)

    b, c, n = 100, 1000, 65536
    N = 4000
    n_workers = 4
    base_seed = 20260826030
    bin_labels = ["(b,2b]", "(2b,5b]", "(5b,20b]", "(20b,inf)"]
    edges = [b, 2 * b, 5 * b, 20 * b, np.inf]

    P(f"=== bootstrap stability re-run, target cell b={b},c={c},n={n}, "
      f"N={N}, seed={base_seed} (FRESH, independent of the N=2500 run) ===")

    ss = np.random.SeedSequence(base_seed)
    children = ss.spawn(n_workers)
    per_worker = [N // n_workers] * n_workers
    for i in range(N - sum(per_worker)):
        per_worker[i] += 1
    args = [(b, c, n, per_worker[i], children[i].entropy, edges) for i in range(n_workers)]

    t0 = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        for r in ex.map(run_chunk, args):
            results.append(r)
    bin_total = np.concatenate([r[0] for r in results], axis=1)
    bin_cyclic = np.concatenate([r[1] for r in results], axis=1)
    P(f"  simulation elapsed {time.time()-t0:.1f}s")

    cpp = c_pp(b, c, n)
    puc = phi_U_scalar(cpp)
    P(f"  phi_U(c'') = {puc:.6f}")

    boot_rng = np.random.default_rng(np.random.SeedSequence(20260826031))
    for k, blabel in enumerate(bin_labels):
        tot = bin_total[k]
        cyc = bin_cyclic[k]
        n_pts = int(tot.sum())
        n_nonzero_inst = int((tot > 0).sum())
        R_delta, sem_delta = ratio_delta_sem(cyc, tot)
        R_boot, sem_boot = bootstrap_se(cyc.astype(np.float64), tot.astype(np.float64),
                                         n_boot=3000, rng=boot_rng)
        dev = 100 * (R_delta / puc - 1)
        z_delta = (R_delta - puc) / sem_delta if sem_delta > 0 else float("nan")
        z_boot = (R_delta - puc) / sem_boot if sem_boot > 0 else float("nan")
        # per-instance ratio distribution shape (for nonzero-total instances)
        mask_nz = tot > 0
        per_inst_ratio = np.where(mask_nz, cyc / np.maximum(tot, 1), np.nan)
        finite = per_inst_ratio[mask_nz]
        frac_inst_all1 = float(np.mean(finite >= 0.999)) if finite.size else float("nan")
        P(f"  bin {blabel}: n_pts={n_pts}  n_instances_with_data={n_nonzero_inst}/{N}")
        P(f"    R (pooled ratio) = {R_delta:.6f}  dev={dev:+.2f}%")
        P(f"    delta-method SEM = {sem_delta:.6f}  (z={z_delta:+.2f})")
        P(f"    cluster-bootstrap SEM (3000 reps) = {sem_boot:.6f}  (z={z_boot:+.2f})")
        P(f"    fraction of contributing instances whose bin-ratio is >=0.999 "
          f"(i.e. dominated by an untouched-cycle event): {100*frac_inst_all1:.1f}%")

    P(f"\nTOTAL elapsed: {time.time()-t0:.1f}s")
    with open("adv_diag_bootstrap.log", "w") as fh:
        fh.write("\n".join(log) + "\n")
