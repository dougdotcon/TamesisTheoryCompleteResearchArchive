"""
adv_diagnostic.py -- independent T1: the diagnostic split (Claims 2 and 3).

For each cell, build N own-engine M-CLUST(b) instances (no formula on the
measurement side), and for every x0 in R^c split by its pi-cycle length L:
  - "su" bucket: L <= b (claim: this equals the untouched-short population,
    and phi(cyclic|su) should be EXACTLY 1 -- a tautological consequence of
    Claim 1, checked here as a hard sanity check, not a free result).
  - "long" bucket: L > b, compared to phi_U(c'') (phi_REDB's conditional
    argument).
  - long bucket further split into L-bins (b,2b],(2b,5b],(5b,20b],(20b,inf)
    to test Claim 3 (the non-monotonic L-dependence).

All errors are delta-method, treating each instance as one i.i.d. cluster
(ratio-of-sums estimator R = sum(cyclic_i)/sum(total_i) across instances;
Var(R) via the standard ratio delta-method: d_i = cyclic_i - R*total_i,
Var(R) ~= Var(d)/(N * mean(total)^2)) -- this matches the sems reported
elsewhere in this lineage (e.g. elevation_level_attempt/adversarial sec 5.2
states "errors are delta-method (instances are i.i.d.)").

Independent of short_cycle_dynamics_attempt/*.py, elevation_level_attempt/*.py
and its adversarial/*.py -- none read or imported.
"""
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from adv_engine import build_instance, cyclic_mask_peeling
from adv_formula import c_pp, phi_U_scalar

BIN_EDGES_FACTORS = [1, 2, 5, 20, None]  # b, 2b, 5b, 20b, inf


def ratio_delta_sem(cyclic_arr, total_arr):
    """Delta-method SEM for R = sum(cyclic)/sum(total), instances i.i.d."""
    N = len(total_arr)
    total_arr = np.asarray(total_arr, dtype=np.float64)
    cyclic_arr = np.asarray(cyclic_arr, dtype=np.float64)
    Xbar = total_arr.mean()
    Ssum = total_arr.sum()
    if Ssum == 0 or Xbar == 0:
        return float("nan"), float("nan")
    R = cyclic_arr.sum() / Ssum
    d = cyclic_arr - R * total_arr
    varR = d.var(ddof=1) / (N * Xbar ** 2)
    return R, np.sqrt(max(varR, 0.0))


def run_chunk(args):
    (b, c, n, n_inst, seed_entropy) = args
    rng = np.random.default_rng(np.random.SeedSequence(seed_entropy))
    edges = [b * f if f is not None else np.inf for f in BIN_EDGES_FACTORS]
    nbins = len(edges) - 1

    su_total = np.zeros(n_inst, dtype=np.int64)
    su_cyclic = np.zeros(n_inst, dtype=np.int64)
    long_total = np.zeros(n_inst, dtype=np.int64)
    long_cyclic = np.zeros(n_inst, dtype=np.int64)
    overall_total = np.zeros(n_inst, dtype=np.int64)
    overall_cyclic = np.zeros(n_inst, dtype=np.int64)
    bin_total = np.zeros((nbins, n_inst), dtype=np.int64)
    bin_cyclic = np.zeros((nbins, n_inst), dtype=np.int64)
    su_violation = 0  # x0 in su bucket that is NOT cyclic -- should stay 0

    for i in range(n_inst):
        inst = build_instance(n, b, c, rng)
        R = inst["R"]
        L = inst["cyc_len_pi"]
        f = inst["f"]
        cyc = cyclic_mask_peeling(f)
        Rc = ~R

        su_mask = Rc & (L <= b)
        long_mask = Rc & (L > b)

        su_total[i] = su_mask.sum()
        su_cyclic[i] = (cyc & su_mask).sum()
        su_violation += int(su_mask.sum() - (cyc & su_mask).sum())

        long_total[i] = long_mask.sum()
        long_cyclic[i] = (cyc & long_mask).sum()

        overall_total[i] = Rc.sum()
        overall_cyclic[i] = (cyc & Rc).sum()

        for k in range(nbins):
            lo, hi = edges[k], edges[k + 1]
            bmask = long_mask & (L > lo) & (L <= hi)
            bin_total[k, i] = bmask.sum()
            bin_cyclic[k, i] = (cyc & bmask).sum()

    return dict(su_total=su_total, su_cyclic=su_cyclic,
                long_total=long_total, long_cyclic=long_cyclic,
                overall_total=overall_total, overall_cyclic=overall_cyclic,
                bin_total=bin_total, bin_cyclic=bin_cyclic,
                su_violation=su_violation)


def run_cell(b, c, n, n_instances, base_entropy, n_workers=4):
    ss = np.random.SeedSequence(base_entropy)
    children = ss.spawn(n_workers)
    per_worker = [n_instances // n_workers] * n_workers
    for i in range(n_instances - sum(per_worker)):
        per_worker[i] += 1
    args = [(b, c, n, per_worker[i], children[i].entropy) for i in range(n_workers)]
    results = []
    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        for r in ex.map(run_chunk, args):
            results.append(r)

    def cat(key):
        return np.concatenate([r[key] for r in results])

    def catbin(key):
        return np.concatenate([r[key] for r in results], axis=1)

    su_violation = sum(r["su_violation"] for r in results)
    return dict(
        su_total=cat("su_total"), su_cyclic=cat("su_cyclic"),
        long_total=cat("long_total"), long_cyclic=cat("long_cyclic"),
        overall_total=cat("overall_total"), overall_cyclic=cat("overall_cyclic"),
        bin_total=catbin("bin_total"), bin_cyclic=catbin("bin_cyclic"),
        su_violation=su_violation,
    )


if __name__ == "__main__":
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        log.append(s)

    CELLS = [
        (100, 1000, 65536, "target b=100,c=1000,n=65536", 2500),
        (400, 100, 65536, "b=400,c=100,n=65536", 2000),
        (200, 150, 65536, "b=200,c=150,n=65536", 2000),
    ]

    # fresh seeds, 20260826010-012 (own T1 run)
    base_seeds = [20260826010, 20260826011, 20260826012]

    all_results = {}
    t0 = time.time()
    for (b, c, n, label, N), base_seed in zip(CELLS, base_seeds):
        t1 = time.time()
        P(f"=== {label}  N={N}  seed={base_seed} ===")
        res = run_cell(b, c, n, N, base_seed)
        all_results[label] = res

        # (i) su sanity check -- must be exactly 1.0
        su_R, su_sem = ratio_delta_sem(res["su_cyclic"], res["su_total"])
        su_tot = int(res["su_total"].sum())
        P(f"  su (short, L<=b) bucket: total_pts={su_tot}  "
          f"phi(cyclic|su)={su_R:.9f} +/- {su_sem:.9f}  "
          f"violations(not cyclic)={res['su_violation']}")

        # (ii) long bucket vs phi_U(c'')
        cpp = c_pp(b, c, n)
        puc = phi_U_scalar(cpp)
        long_R, long_sem = ratio_delta_sem(res["long_cyclic"], res["long_total"])
        long_tot = int(res["long_total"].sum())
        dev = 100 * (long_R / puc - 1)
        z = (long_R - puc) / long_sem if long_sem > 0 else float("nan")
        P(f"  long (L>b) bucket: total_pts={long_tot}  phi={long_R:.6f} +/- "
          f"{long_sem:.6f}  phi_U(c'')={puc:.6f}  dev={dev:+.2f}%  z={z:+.2f}")

        # (iii) overall Rc
        ov_R, ov_sem = ratio_delta_sem(res["overall_cyclic"], res["overall_total"])
        ov_tot = int(res["overall_total"].sum())
        dev_o = 100 * (ov_R / puc - 1)
        z_o = (ov_R - puc) / ov_sem if ov_sem > 0 else float("nan")
        w_short_meas = su_tot / ov_tot
        P(f"  overall (x0 in R^c) bucket: total_pts={ov_tot}  phi={ov_R:.6f} "
          f"+/- {ov_sem:.6f}  phi_U(c'')={puc:.6f}  dev={dev_o:+.2f}%  z={z_o:+.2f}"
          f"  w_short_measured={100*w_short_meas:.3f}%")

        # (iv) L-binned structure (Claim 3)
        bin_labels = ["(b,2b]", "(2b,5b]", "(5b,20b]", "(20b,inf)"]
        for k, blabel in enumerate(bin_labels):
            bt = res["bin_total"][k]
            bcy = res["bin_cyclic"][k]
            R_k, sem_k = ratio_delta_sem(bcy, bt)
            tot_k = int(bt.sum())
            if tot_k == 0 or np.isnan(sem_k) or sem_k == 0:
                P(f"    bin {blabel}: total_pts={tot_k}  (insufficient data)")
                continue
            dev_k = 100 * (R_k / puc - 1)
            z_k = (R_k - puc) / sem_k
            P(f"    bin {blabel}: n={tot_k}  phi={R_k:.6f} +/- {sem_k:.6f}  "
              f"dev={dev_k:+.2f}%  z={z_k:+.2f}")

        P(f"  [cell elapsed {time.time()-t1:.1f}s]")
        P("")

    P(f"TOTAL elapsed: {time.time()-t0:.1f}s")

    with open("adv_diagnostic.log", "w") as fh:
        fh.write("\n".join(log) + "\n")
