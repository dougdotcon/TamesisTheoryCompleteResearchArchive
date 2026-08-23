"""
adv_reduction.py -- independent T2: formula-free reduction test on the
6-cell grid (Claim 4 / ATTEMPT.md sec 6-7), scoring the own-engine-measured
phi(cyclic|x0 in R^c) and full phi(cyclic) against phi_U(c'')/phi_REDB
(formula of record) and phi_cond_C/phi_REDC (this front's refuted
candidate).

No formula enters the measurement side. Errors: delta-method ratio
estimator across i.i.d. instances (see adv_diagnostic.py for the formula).

Independent of short_cycle_dynamics_attempt/*.py, elevation_level_attempt/*.py
and its adversarial/*.py -- none read or imported.
"""
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from adv_engine import build_instance, cyclic_mask_peeling
from adv_diagnostic import ratio_delta_sem
from adv_formula import (phi_REDB_cond, phi_REDB_full, phi_cond_C_v2,
                          phi_REDC_full)


def run_chunk(args):
    (b, c, n, n_inst, seed_entropy) = args
    rng = np.random.default_rng(np.random.SeedSequence(seed_entropy))
    Rc_total = np.zeros(n_inst, dtype=np.int64)
    Rc_cyclic = np.zeros(n_inst, dtype=np.int64)
    full_total = np.zeros(n_inst, dtype=np.int64)
    full_cyclic = np.zeros(n_inst, dtype=np.int64)
    for i in range(n_inst):
        inst = build_instance(n, b, c, rng)
        R = inst["R"]
        f = inst["f"]
        cyc = cyclic_mask_peeling(f)
        Rc = ~R
        Rc_total[i] = Rc.sum()
        Rc_cyclic[i] = (cyc & Rc).sum()
        full_total[i] = n
        full_cyclic[i] = cyc.sum()
    return dict(Rc_total=Rc_total, Rc_cyclic=Rc_cyclic,
                full_total=full_total, full_cyclic=full_cyclic)


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

    return dict(Rc_total=cat("Rc_total"), Rc_cyclic=cat("Rc_cyclic"),
                full_total=cat("full_total"), full_cyclic=cat("full_cyclic"))


if __name__ == "__main__":
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        log.append(s)

    # the referee's own pre-registered 6-cell grid, target cell last
    CELLS = [
        (50, 400, 65536, 1500),
        (100, 400, 65536, 1500),
        (100, 600, 65536, 1500),
        (200, 150, 65536, 1500),
        (400, 100, 65536, 1500),
        (100, 1000, 65536, 2000),  # target cell, extra instances
    ]
    base_seeds = [20260826020, 20260826021, 20260826022,
                  20260826023, 20260826024, 20260826025]

    chi2_redb_cond = 0.0
    chi2_redc_cond = 0.0
    chi2_redb_full = 0.0
    chi2_redc_full = 0.0
    t0 = time.time()

    rows = []
    for (b, c, n, N), seed in zip(CELLS, base_seeds):
        t1 = time.time()
        P(f"=== b={b},c={c},n={n}  N={N}  seed={seed} ===")
        res = run_cell(b, c, n, N, seed)

        Rc_R, Rc_sem = ratio_delta_sem(res["Rc_cyclic"], res["Rc_total"])
        full_R, full_sem = ratio_delta_sem(res["full_cyclic"], res["full_total"])

        redb_cond = phi_REDB_cond(b, c, n)
        redc_cond = phi_cond_C_v2(b, c, n)
        redb_full = phi_REDB_full(b, c, n)
        redc_full = phi_REDC_full(b, c, n)

        z_redb_c = (Rc_R - redb_cond) / Rc_sem
        z_redc_c = (Rc_R - redc_cond) / Rc_sem
        z_redb_f = (full_R - redb_full) / full_sem
        z_redc_f = (full_R - redc_full) / full_sem

        chi2_redb_cond += z_redb_c ** 2
        chi2_redc_cond += z_redc_c ** 2
        chi2_redb_full += z_redb_f ** 2
        chi2_redc_full += z_redc_f ** 2

        dev_redb_c = 100 * (Rc_R / redb_cond - 1)
        dev_redc_c = 100 * (Rc_R / redc_cond - 1)
        dev_redb_f = 100 * (full_R / redb_full - 1)
        dev_redc_f = 100 * (full_R / redc_full - 1)

        P(f"  phi(cyclic|x0 in R^c) measured = {Rc_R:.6f} +/- {Rc_sem:.6f} "
          f"(n_pts={int(res['Rc_total'].sum())})")
        P(f"    vs phi_REDB_cond={redb_cond:.6f}: dev={dev_redb_c:+.2f}% z={z_redb_c:+.2f}")
        P(f"    vs phi_REDC_cond={redc_cond:.6f}: dev={dev_redc_c:+.2f}% z={z_redc_c:+.2f}")
        P(f"  full phi(cyclic) measured = {full_R:.6f} +/- {full_sem:.6f}")
        P(f"    vs phi_REDB_full={redb_full:.6f}: dev={dev_redb_f:+.2f}% z={z_redb_f:+.2f}")
        P(f"    vs phi_REDC_full={redc_full:.6f}: dev={dev_redc_f:+.2f}% z={z_redc_f:+.2f}")
        P(f"  [cell elapsed {time.time()-t1:.1f}s]")
        P("")

        rows.append(dict(b=b, c=c, n=n, z_redb_full=z_redb_f, z_redc_full=z_redc_f,
                          z_redb_cond=z_redb_c, z_redc_cond=z_redc_c))

    P("=== POOLED chi^2 over 6 cells ===")
    P(f"  conditional scoring: phi_REDB chi2={chi2_redb_cond:.2f}  "
      f"phi_REDC chi2={chi2_redc_cond:.2f}  "
      f"ratio={chi2_redc_cond/chi2_redb_cond:.2f}x")
    P(f"  full-phi scoring:    phi_REDB chi2={chi2_redb_full:.2f}  "
      f"phi_REDC chi2={chi2_redc_full:.2f}  "
      f"ratio={chi2_redc_full/chi2_redb_full:.2f}x")

    # target-cell success criterion (DERIVATION_PREREG sec 3, T2):
    # reduce |z| on target cell by >=30% without |z| on any other cell
    # exceeding max(2*its own phi_REDB |z|, 2.5)
    target_row = rows[-1]
    z_before = abs(target_row["z_redb_full"])
    z_after = abs(target_row["z_redc_full"])
    reduction_pct = 100 * (1 - z_after / z_before) if z_before > 0 else float("nan")
    P("")
    P(f"=== Pre-registered T2 success criterion (target cell) ===")
    P(f"  target cell |z| before (phi_REDB) = {z_before:.2f}, "
      f"after (phi_REDC) = {z_after:.2f}, change = {reduction_pct:+.1f}% "
      f"(need >= +30% reduction to succeed)")
    other_ok = True
    for r in rows[:-1]:
        bound = max(2 * abs(r["z_redb_full"]), 2.5)
        ok = abs(r["z_redc_full"]) <= bound
        other_ok = other_ok and ok
        P(f"  cell b={r['b']},c={r['c']}: |z_REDB|={abs(r['z_redb_full']):.2f} "
          f"|z_REDC|={abs(r['z_redc_full']):.2f} bound={bound:.2f} "
          f"{'OK' if ok else 'EXCEEDS BOUND'}")
    success = (reduction_pct >= 30) and other_ok
    P(f"  T2 SUCCESS CRITERION: {'MET' if success else 'NOT MET -- REFUTED'}")

    P(f"\nTOTAL elapsed: {time.time()-t0:.1f}s")

    with open("adv_reduction.log", "w") as fh:
        fh.write("\n".join(log) + "\n")
