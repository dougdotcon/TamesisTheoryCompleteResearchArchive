"""
lcd_bsweep.py -- T2, the b-sweep dose-response test (DERIVATION_PREREG.md
SS3). Fixed cell c=1000, n=65536 (the target cell of the parent front).
Sweep b in {1,5,20,50,100}; for each b, measure ONLY the far-tail bucket
phi(cyclic | x0 in R^c, L>2000) -- the SAME absolute threshold at every b --
against phi_U(c'') (c'' depends on b via c_double_prime). Isolates the
effect of b alone, holding (c,n) and the L-window fixed.

Reuses sc_engine.py / sc_formula.py unmodified, by import.
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sc_engine as eng
import sc_formula as fm

N_PER_B = 2000
THRESHOLD = 2000
CELL_N = 65536
CELL_C = 1000

B_SEEDS = [
    (1, 20260827010),
    (5, 20260827011),
    (20, 20260827012),
    (50, 20260827013),
    (100, 20260827014),
]


def measure_far_tail(n, b, c, N, seed_seq, threshold, log=print, log_every=200):
    ss = np.random.SeedSequence(seed_seq)
    children = ss.spawn(N)

    n_far = np.zeros(N, dtype=np.int64)
    cyc_far = np.zeros(N, dtype=np.int64)
    rho_meas = np.zeros(N, dtype=float)

    t0 = time.time()
    for i in range(N):
        rng = np.random.default_rng(children[i])
        inst = eng.build_instance(n, b, c, rng)
        pi, R_mask, f = inst["pi"], inst["R_mask"], inst["f"]
        cyclic = eng.cyclic_mask_peeling(f)
        cyc_len = eng.pi_cycle_lengths(pi)

        Rc_mask = ~R_mask
        far_mask = Rc_mask & (cyc_len > threshold)

        n_far[i] = far_mask.sum()
        cyc_far[i] = cyclic[far_mask].sum()
        rho_meas[i] = R_mask.mean()

        if log_every and (i + 1) % log_every == 0:
            elapsed = time.time() - t0
            log(f"    [{i+1}/{N}] elapsed={elapsed:.1f}s "
                f"({elapsed/(i+1)*1000:.1f}ms/instance)")

    with np.errstate(invalid="ignore", divide="ignore"):
        r_far = cyc_far / n_far

    def m_sem(x):
        x = x[np.isfinite(x)]
        return x.mean(), x.std(ddof=1) / np.sqrt(len(x)), len(x)

    phi_far = m_sem(r_far)
    n_far_total = int(n_far.sum())
    phi_U_cpp = fm.phi_U(fm.c_double_prime(b, c, n))
    rho_mean = rho_meas.mean()

    return dict(phi_far=phi_far, n_far_total=n_far_total, phi_U_cpp=phi_U_cpp,
                rho_mean=rho_mean)


if __name__ == "__main__":
    print(f"lcd_bsweep.py T2 -- b-sweep dose response, c={CELL_C} n={CELL_N}, "
          f"threshold L>{THRESHOLD}, N={N_PER_B} per b")
    print(f"{'b':>5} {'rho':>8} {'phi_U(cpp)':>12} {'phi_far':>10} {'SEM':>10} "
          f"{'dev%':>9} {'z':>8} {'n_pts':>10}")

    results = []
    for (b, seed) in B_SEEDS:
        res = measure_far_tail(CELL_N, b, CELL_C, N_PER_B, seed, THRESHOLD,
                                log=print, log_every=max(1, N_PER_B // 4))
        mean, sem, cnt = res["phi_far"]
        phi_U_cpp = res["phi_U_cpp"]
        dev = 100 * (mean / phi_U_cpp - 1) if sem > 0 else float("nan")
        z = (mean - phi_U_cpp) / sem if sem > 0 else float("nan")
        results.append((b, res["rho_mean"], phi_U_cpp, mean, sem, dev, z, res["n_far_total"]))
        print(f"{b:5d} {res['rho_mean']:8.4f} {phi_U_cpp:12.6f} {mean:10.6f} {sem:10.6f} "
              f"{dev:+9.2f} {z:+8.2f} {res['n_far_total']:10d}")

    print("\n--- summary table ---")
    print(f"{'b':>5} {'dev%':>9} {'z':>8}")
    for (b, rho, phi_U_cpp, mean, sem, dev, z, npts) in results:
        print(f"{b:5d} {dev:+9.2f} {z:+8.2f}")

    devs = [abs(r[5]) for r in results]
    print(f"\nmax|dev%|={max(devs):.2f}  min|dev%|={min(devs):.2f}  "
          f"ratio={max(devs)/min(devs):.2f}x")
    print(f"b=1 |dev%|={abs(results[0][5]):.2f}  b=100 |dev%|={abs(results[-1][5]):.2f}  "
          f"ratio(b=100/b=1)={abs(results[-1][5])/abs(results[0][5]):.2f}x")
