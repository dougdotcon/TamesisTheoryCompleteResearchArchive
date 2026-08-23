"""
sc_reduction.py -- T2/T3: formula-free direct measurement of phi(cyclic|x0 in
R^c) and full phi, on the pre-registered 6-cell grid, compared against
phi_U(c') (superseded), phi_U(c'') (phi_REDB's conditional), phi_REDB (full),
phi_cond_C / phi_REDC (this front's candidate).

No walk is simulated: the whole functional graph f is built once per
instance and the cyclic mask is computed once (in-degree peeling); phi_full
and phi_Rc are then exact per-instance ratios over that one graph -- the same
"whole functional graph, no walk" methodology the predecessor referee used
(elevation_level_attempt/adversarial/REFEREE_REPORT.md, referenced via
x0_asymmetry_attempt §5.6 in the mandate's Background section).
"""

import sys
import time
import numpy as np
import sc_engine as eng
import sc_formula as fm

GRID = [
    (65536, 50, 400),
    (65536, 100, 400),
    (65536, 100, 600),
    (65536, 200, 150),
    (65536, 400, 100),
    (65536, 100, 1000),  # target cell
]

SEEDS = [20260825910, 20260825911, 20260825912, 20260825913, 20260825914, 20260825915]


def measure_cell(n, b, c, N, seed_seq, log=print, log_every=500):
    ss = np.random.SeedSequence(seed_seq)
    children = ss.spawn(N)

    rho_meas = np.zeros(N)
    phi_full = np.zeros(N)
    n_Rc = np.zeros(N, dtype=np.int64)
    cyc_Rc = np.zeros(N, dtype=np.int64)
    n_R = np.zeros(N, dtype=np.int64)
    cyc_R = np.zeros(N, dtype=np.int64)

    t0 = time.time()
    for i in range(N):
        rng = np.random.default_rng(children[i])
        inst = eng.build_instance(n, b, c, rng)
        R_mask, f = inst["R_mask"], inst["f"]
        cyclic = eng.cyclic_mask_peeling(f)

        rho_meas[i] = R_mask.mean()
        phi_full[i] = cyclic.mean()
        Rc = ~R_mask
        n_Rc[i] = Rc.sum()
        cyc_Rc[i] = cyclic[Rc].sum()
        n_R[i] = R_mask.sum()
        cyc_R[i] = cyclic[R_mask].sum()

        if log_every and (i + 1) % log_every == 0:
            elapsed = time.time() - t0
            log(f"    [{i+1}/{N}] elapsed={elapsed:.1f}s ({elapsed/(i+1)*1000:.2f}ms/inst)")

    return dict(rho_meas=rho_meas, phi_full=phi_full, n_Rc=n_Rc, cyc_Rc=cyc_Rc,
                n_R=n_R, cyc_R=cyc_R)


def m_sem(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    return x.mean(), x.std(ddof=1) / np.sqrt(len(x))


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    cell_idx = int(sys.argv[2]) if len(sys.argv) > 2 else None
    seed_override = int(sys.argv[3]) if len(sys.argv) > 3 else None

    cells = GRID if cell_idx is None else [GRID[cell_idx]]
    seeds = SEEDS if cell_idx is None else [seed_override if seed_override else SEEDS[cell_idx]]

    for (n, b, c), sd in zip(cells, seeds):
        print(f"\n=== cell n={n} b={b} c={c}  seed={sd}  N={N} ===")
        res = measure_cell(n, b, c, N, sd)

        rho_m, rho_sem = m_sem(res["rho_meas"])
        phi_m, phi_sem = m_sem(res["phi_full"])
        with np.errstate(invalid="ignore", divide="ignore"):
            r_Rc = res["cyc_Rc"] / res["n_Rc"]
            r_R = res["cyc_R"] / res["n_R"]
        phi_Rc_m, phi_Rc_sem = m_sem(r_Rc)
        phi_R_m, phi_R_sem = m_sem(r_R)

        c_prime = c * (1 - rho_m)  # superseded convention, for reference only
        c_dp = fm.c_double_prime(b, c, n)
        phiU_cp = fm.phi_U(c_prime)
        phiU_cpp = fm.phi_U(c_dp)
        phi_condC = fm.phi_cond_C(b, c, n)
        v_REDB = fm.phi_REDB(b, c, n)
        v_REDC = fm.phi_REDC(b, c, n)

        print(f"rho: measured {rho_m:.5f}+-{rho_sem:.5f}  formula {fm.rho_of(b,c,n):.5f}")
        print(f"phi(cyclic|x0 in R^c): measured {phi_Rc_m:.6f}+-{phi_Rc_sem:.6f}")
        print(f"  vs phi_U(c') [superseded]  = {phiU_cp:.6f}  "
              f"dev={100*(phi_Rc_m/phiU_cp-1):+.3f}%  z={(phi_Rc_m-phiU_cp)/phi_Rc_sem:+.2f}")
        print(f"  vs phi_U(c'') [phi_REDB]   = {phiU_cpp:.6f}  "
              f"dev={100*(phi_Rc_m/phiU_cpp-1):+.3f}%  z={(phi_Rc_m-phiU_cpp)/phi_Rc_sem:+.2f}")
        print(f"  vs phi_cond_C [this front] = {phi_condC:.6f}  "
              f"dev={100*(phi_Rc_m/phi_condC-1):+.3f}%  z={(phi_Rc_m-phi_condC)/phi_Rc_sem:+.2f}")
        print(f"phi(cyclic|x0 in R) [eps channel]: measured {phi_R_m:.6f}+-{phi_R_sem:.6f}")
        print(f"phi FULL: measured {phi_m:.6f}+-{phi_sem:.6f}")
        print(f"  vs phi_REDB (full) = {v_REDB:.6f}  "
              f"dev={100*(phi_m/v_REDB-1):+.3f}%  z={(phi_m-v_REDB)/phi_sem:+.2f}")
        print(f"  vs phi_REDC (full) = {v_REDC:.6f}  "
              f"dev={100*(phi_m/v_REDC-1):+.3f}%  z={(phi_m-v_REDC)/phi_sem:+.2f}")
