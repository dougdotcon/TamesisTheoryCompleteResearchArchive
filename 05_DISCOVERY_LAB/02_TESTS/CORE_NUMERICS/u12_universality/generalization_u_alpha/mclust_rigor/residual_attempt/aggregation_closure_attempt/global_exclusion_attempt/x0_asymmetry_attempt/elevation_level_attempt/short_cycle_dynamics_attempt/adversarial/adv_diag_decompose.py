"""
adv_diag_decompose.py -- decompose the (b,2b] and (2b,5b] "long" bins into
their UNTOUCHED-cycle vs TOUCHED-cycle sub-populations, to determine whether
the large near-b excess (Claim 3) is driven mainly by the (tautologically
cyclic-1) untouched sub-population's weight, or by a genuinely elevated
conditional rate among TOUCHED cycles' surviving R^c remainder (the
"self-contained residual arc" effect ATTEMPT.md sec 3.1 names but does not
separately quantify).

Also checks directly: is the untouched sub-population, extended past L<=b,
STILL exactly cyclic with probability 1 for L up to 5b? (a sharper form of
Claim 1/Claim 3's own stated mechanism).

Fresh seed, not reused: SeedSequence(20260826032).
"""
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from adv_engine import build_instance, cyclic_mask_peeling, pi_cycle_labels_lengths
from adv_diagnostic import ratio_delta_sem
from adv_formula import c_pp, phi_U_scalar


def run_chunk(args):
    (b, c, n, n_inst, seed_entropy, edges) = args
    rng = np.random.default_rng(np.random.SeedSequence(seed_entropy))
    nbins = len(edges) - 1
    # per bin: untouched-subpop (total,cyclic), touched-subpop (total,cyclic)
    ut_total = np.zeros((nbins, n_inst), dtype=np.int64)
    ut_cyclic = np.zeros((nbins, n_inst), dtype=np.int64)
    to_total = np.zeros((nbins, n_inst), dtype=np.int64)
    to_cyclic = np.zeros((nbins, n_inst), dtype=np.int64)

    for i in range(n_inst):
        pi = rng.permutation(n)
        p = c / n
        seeds = rng.random(n) < p
        R = np.zeros(n, dtype=bool)
        R[seeds] = True
        cur = np.nonzero(seeds)[0]
        for _ in range(b - 1):
            cur = pi[cur]
            R[cur] = True
        f = pi.copy()
        nR = int(R.sum())
        if nR > 0:
            f[R] = rng.integers(0, n, size=nR)
        cyc = cyclic_mask_peeling(f)

        labels, L = pi_cycle_labels_lengths(pi)
        ncomp = labels.max() + 1
        seed_count_per_cycle = np.bincount(labels, weights=seeds.astype(np.int64),
                                            minlength=ncomp)
        has_seed_per_cycle = seed_count_per_cycle > 0
        has_seed_point = has_seed_per_cycle[labels]

        Rc = ~R
        for k in range(nbins):
            lo, hi = edges[k], edges[k + 1]
            in_bin = Rc & (L > lo) & (L <= hi)
            untouched_mask = in_bin & (~has_seed_point)
            touched_mask = in_bin & has_seed_point
            ut_total[k, i] = untouched_mask.sum()
            ut_cyclic[k, i] = (cyc & untouched_mask).sum()
            to_total[k, i] = touched_mask.sum()
            to_cyclic[k, i] = (cyc & touched_mask).sum()

    return ut_total, ut_cyclic, to_total, to_cyclic


if __name__ == "__main__":
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        log.append(s)

    b, c, n = 100, 1000, 65536
    N = 3000
    n_workers = 4
    base_seed = 20260826032
    bin_labels = ["(b,2b]", "(2b,5b]", "(5b,20b]"]
    edges = [b, 2 * b, 5 * b, 20 * b]

    P(f"=== decomposition run, target cell b={b},c={c},n={n}, N={N}, "
      f"seed={base_seed} ===")

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
    ut_total = np.concatenate([r[0] for r in results], axis=1)
    ut_cyclic = np.concatenate([r[1] for r in results], axis=1)
    to_total = np.concatenate([r[2] for r in results], axis=1)
    to_cyclic = np.concatenate([r[3] for r in results], axis=1)
    P(f"  simulation elapsed {time.time()-t0:.1f}s")

    cpp = c_pp(b, c, n)
    puc = phi_U_scalar(cpp)
    P(f"  phi_U(c'') = {puc:.6f}")

    for k, blabel in enumerate(bin_labels):
        P(f"\n  bin {blabel}:")
        utt, utc = ut_total[k], ut_cyclic[k]
        tot_, toc = to_total[k], to_cyclic[k]
        n_ut = int(utt.sum())
        n_to = int(tot_.sum())
        R_ut, sem_ut = ratio_delta_sem(utc, utt)
        R_to, sem_to = ratio_delta_sem(toc, tot_)
        P(f"    UNTOUCHED sub-pop: n_pts={n_ut}  phi={R_ut:.9f} +/- {sem_ut:.9f}  "
          f"(theory: exactly 1.0)")
        P(f"    TOUCHED   sub-pop: n_pts={n_to}  phi={R_to:.6f} +/- {sem_to:.6f}  "
          f"phi_U(c'')={puc:.6f}  dev={100*(R_to/puc-1):+.2f}%  "
          f"z={(R_to-puc)/sem_to:+.2f}")
        weight_ut = n_ut / (n_ut + n_to)
        recon = weight_ut * R_ut + (1 - weight_ut) * R_to
        P(f"    weight(untouched)={100*weight_ut:.2f}%  "
          f"reconstructed overall bin avg={recon:.6f} "
          f"(dev vs phi_U(c'')={100*(recon/puc-1):+.2f}%)")

    P(f"\nTOTAL elapsed: {time.time()-t0:.1f}s")
    with open("adv_diag_decompose.log", "w") as fh:
        fh.write("\n".join(log) + "\n")
