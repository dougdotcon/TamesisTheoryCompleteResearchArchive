"""
cv_grid.py -- driver for CELL-VARIATION-ATTEMPT (DISC-DEC-057 front e).
Runs T0, then all 13 cells x 2 conditions (own-b, b=1) in the locked order
and seeds of DERIVATION_PREREG.md SS3/SS6. Prints a running log (redirect to
cv_grid.log) and a final machine-parseable summary block.
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cv_measure import measure_far_tail, t0_engine_sanity  # noqa: E402

N = 65536

# (id, b, c, own_seed, b1_seed, group_string)
CELLS = [
    ("A",   100,  1000, 20260839001, 20260839002, "G1;G2;G3"),
    ("G1a", 25,   1000, 20260839003, 20260839004, "G1"),
    ("G1b", 50,   1000, 20260839005, 20260839006, "G1"),
    ("G1d", 200,  1000, 20260839007, 20260839008, "G1"),
    ("G2a", 100,  200,  20260839009, 20260839010, "G2"),
    ("G2b", 100,  500,  20260839011, 20260839012, "G2"),
    ("G2d", 100,  2000, 20260839013, 20260839014, "G2"),
    ("G3a", 335,  300,  20260839015, 20260839016, "G3"),
    ("G3c", 50,   2000, 20260839017, 20260839018, "G3"),
    ("G3d", 1007, 100,  20260839019, 20260839020, "G3"),
    ("B",   400,  100,  20260839021, 20260839022, "G4"),
    ("G4b", 80,   500,  20260839023, 20260839024, "G4"),
    ("G4c", 26,   1500, 20260839025, 20260839026, "G4"),
]

N_PER_RUN = 2000
NWORKERS = 4


def main():
    t_start = time.time()
    print(f"cv_grid.py -- CELL-VARIATION-ATTEMPT full grid, N={N_PER_RUN} per "
          f"measurement, nworkers={NWORKERS}, {len(CELLS)} cells x 2 conditions")
    print(f"started {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")

    ok = t0_engine_sanity()
    if not ok:
        print("T0 FAILED -- stopping per pre-registered refutation rule.")
        sys.exit(1)

    print("\n=== main grid ===")
    print(f"{'id':>5} {'cond':>6} {'b':>5} {'c':>6} {'thr':>6} {'rho_f':>7} "
          f"{'rho_m':>7} {'phi_U':>10} {'phi_far':>10} {'SEM':>10} "
          f"{'dev%':>9} {'z':>8} {'n_far':>10} {'t(s)':>7}")

    rows = []
    for (cid, b, c, seed_own, seed_b1, group) in CELLS:
        threshold = 20 * b

        r_own = measure_far_tail(N, b, c, N_PER_RUN, seed_own, threshold,
                                  nworkers=NWORKERS, log=print, log_every=0,
                                  label=f"{cid}-own")
        print(f"{cid:>5} {'own-b':>6} {b:5d} {c:6d} {threshold:6d} "
              f"{r_own['rho_formula']:7.4f} {r_own['rho_meas']:7.4f} "
              f"{r_own['phi_U_target']:10.6f} {r_own['phi_far']:10.6f} "
              f"{r_own['sem']:10.6f} {r_own['dev']:+9.3f} {r_own['z']:+8.3f} "
              f"{r_own['n_far_total']:10d} {r_own['elapsed']:7.1f}")

        r_b1 = measure_far_tail(N, 1, c, N_PER_RUN, seed_b1, threshold,
                                 nworkers=NWORKERS, log=print, log_every=0,
                                 label=f"{cid}-b1")
        print(f"{cid:>5} {'b=1':>6} {1:5d} {c:6d} {threshold:6d} "
              f"{r_b1['rho_formula']:7.4f} {r_b1['rho_meas']:7.4f} "
              f"{r_b1['phi_U_target']:10.6f} {r_b1['phi_far']:10.6f} "
              f"{r_b1['sem']:10.6f} {r_b1['dev']:+9.3f} {r_b1['z']:+8.3f} "
              f"{r_b1['n_far_total']:10d} {r_b1['elapsed']:7.1f}")

        rows.append(dict(cid=cid, b=b, c=c, group=group, own=r_own, b1=r_b1))

    elapsed_total = time.time() - t_start
    print(f"\ntotal grid elapsed: {elapsed_total:.1f}s ({elapsed_total/60:.2f} min)")

    print("\n=== MACHINE-PARSEABLE SUMMARY (for cv_analysis.py) ===")
    print("cid,b,c,group,rho_formula,cpp_own,phiU_own,phi_own,sem_own,dev_own,z_own,"
          "cpp_b1,phiU_b1,phi_b1,sem_b1,dev_b1,z_b1")
    for row in rows:
        o, b1 = row["own"], row["b1"]
        print(f"{row['cid']},{row['b']},{row['c']},{row['group']},"
              f"{o['rho_formula']:.6f},{o['cpp']:.6f},{o['phi_U_target']:.6f},"
              f"{o['phi_far']:.6f},{o['sem']:.6f},{o['dev']:.6f},{o['z']:.6f},"
              f"{b1['cpp']:.6f},{b1['phi_U_target']:.6f},"
              f"{b1['phi_far']:.6f},{b1['sem']:.6f},{b1['dev']:.6f},{b1['z']:.6f}")

    print("\ncv_grid.py DONE")


if __name__ == "__main__":
    main()
