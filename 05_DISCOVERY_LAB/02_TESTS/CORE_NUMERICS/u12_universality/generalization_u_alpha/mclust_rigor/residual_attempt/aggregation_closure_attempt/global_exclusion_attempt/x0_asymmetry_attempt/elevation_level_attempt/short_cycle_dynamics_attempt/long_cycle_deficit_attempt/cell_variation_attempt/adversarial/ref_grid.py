"""
ref_grid.py -- referee's independent re-simulation of a 9-cell subset of the
13-cell cell_variation_attempt design, fresh seeds (20260840100+, this
front's own referee-reserved range per DECISION_LEDGER.yaml DISC-DEC-057),
own from-scratch measurement code (ref_measure.py).

Cell selection (9 of 13, chosen to cover every mandate priority):
  A     (hub G1/G2/G3)         b=100,  c=1000, N=3000
  G1b   (ambiguous at N=2000)  b=50,   c=1000, N=6000  (3x front's N)
  G1d   (G1 extreme)           b=200,  c=1000, N=2500
  G2a   (required extreme)     b=100,  c=200,  N=4000  (2x front's N)
  G2d   (required extreme)     b=100,  c=2000, N=4000  (2x front's N)
  G3c   (G3, rho~0.785-0.788)  b=50,   c=2000, N=2500
  G3d   (G3, rho~0.785-0.788)  b=1007, c=100,  N=2000
  B     (hub G4)               b=400,  c=100,  N=2500
  G4c   (G4, rho~0.452-0.458)  b=26,   c=1500, N=2000

Every cell uses threshold=20*b_orig for BOTH its own-b and its b=1
companion condition (matched-threshold design, per DERIVATION_PREREG.md S2).
n=65536 throughout.

Raw per-instance (n_far_i, cyc_far_i) arrays are saved to ref_grid_raw.npz
for downstream re-analysis (ref_analysis.py): alternate exclusion rules,
bootstrap cross-checks, re-groupings, etc.
"""

import time
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ref_measure as rm  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
_SC_DIR = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, _SC_DIR)
import sc_engine  # noqa: E402
import sc_formula  # noqa: E402

N_WORKERS = 4
NN = 65536

CELLS = [
    # id,    b,    c,    N
    ("A",    100,  1000, 3000),
    ("G1b",  50,   1000, 6000),
    ("G1d",  200,  1000, 2500),
    ("G2a",  100,  200,  4000),
    ("G2d",  100,  2000, 4000),
    ("G3c",  50,   2000, 2500),
    ("G3d",  1007, 100,  2000),
    ("B",    400,  100,  2500),
    ("G4c",  26,   1500, 2000),
]

SEED_BASE = 20260840100


def log(msg, fh):
    print(msg)
    fh.write(msg + "\n")
    fh.flush()


def main():
    log_path = os.path.join(_HERE, "ref_grid.log")
    raw = {}
    seed_table = []
    seed_counter = [SEED_BASE]

    def next_seed(use, N):
        s = seed_counter[0]
        seed_counter[0] += 1
        seed_table.append((s, use, N))
        return s

    with open(log_path, "w") as fh:
        log("ref_grid.py -- referee independent re-simulation", fh)
        log(f"n={NN}, nworkers={N_WORKERS}", fh)
        log("", fh)

        # --- T0: b=1 engine sanity re-check (own code, fresh seed) ---------
        t0_seed = next_seed("T0 sanity (R_mask==seed_mask at b=1)", 40)
        rng = np.random.default_rng(np.random.SeedSequence(t0_seed))
        n_t0, c_t0 = 65536, 1000
        viol = 0
        rho_vals = []
        for _ in range(40):
            inst = sc_engine.build_instance(n_t0, 1, c_t0, rng)
            if not np.array_equal(inst["R_mask"], inst["seed_mask"]):
                viol += 1
            rho_vals.append(inst["R_mask"].mean())
        rho_meas = float(np.mean(rho_vals))
        rho_sem = float(np.std(rho_vals, ddof=1) / np.sqrt(len(rho_vals)))
        rho_formula = c_t0 / n_t0
        z_rho = (rho_meas - rho_formula) / rho_sem if rho_sem > 0 else 0.0
        log(f"T0 seed={t0_seed} N=40: R_mask==seed_mask violations={viol}/40  "
            f"rho_formula={rho_formula:.6f} rho_meas={rho_meas:.6f}+-{rho_sem:.6f} "
            f"z={z_rho:+.3f}", fh)
        log("", fh)

        t_grid0 = time.time()
        for cell_id, b, c, N in CELLS:
            threshold = 20 * b
            cpp_own = sc_formula.c_double_prime(b, c, NN)
            phi_ref_own = float(sc_formula.phi_U(cpp_own))
            phi_ref_b1 = float(sc_formula.phi_U(c))  # c''(1,c,n) = c exactly
            rho = sc_formula.rho_of(b, c, NN)

            log(f"--- cell {cell_id}: b={b} c={c} n={NN} rho={rho:.4f} "
                f"threshold={threshold} N={N} ---", fh)

            t0 = time.time()
            seed_own = next_seed(f"{cell_id} own-b", N)
            r_own = rm.phi_far_and_z(NN, b, c, N, np.random.SeedSequence(seed_own),
                                      threshold, phi_ref_own, nworkers=N_WORKERS)
            t1 = time.time()
            seed_b1 = next_seed(f"{cell_id} b=1", N)
            r_b1 = rm.phi_far_and_z(NN, 1, c, N, np.random.SeedSequence(seed_b1),
                                     threshold, phi_ref_b1, nworkers=N_WORKERS)
            t2 = time.time()

            log(f"  own-b  seed={seed_own}: phi_far={r_own['phi_far']:.6f} "
                f"phi_ref={phi_ref_own:.6f} dev%={r_own['dev_pct']:+.3f} "
                f"z={r_own['z']:+.3f} pop={r_own['total_pop']} ({t1-t0:.1f}s)", fh)
            log(f"  b=1    seed={seed_b1}: phi_far={r_b1['phi_far']:.6f} "
                f"phi_ref={phi_ref_b1:.6f} dev%={r_b1['dev_pct']:+.3f} "
                f"z={r_b1['z']:+.3f} pop={r_b1['total_pop']} ({t2-t1:.1f}s)", fh)

            if r_own['dev_pct'] < 0 and abs(r_own['z']) >= 2:
                share, sem_share = rm.h2_share(r_own['dev_pct'], r_b1['dev_pct'],
                                                r_own['sem_pct'], r_b1['sem_pct'])
                log(f"  H2 share = {share*100:.1f}% +- {sem_share*100:.1f}pp", fh)
            else:
                share, sem_share = None, None
                log(f"  H2 share = EXCLUDED (dev_own>=0 or |z_own|<2)", fh)
            log("", fh)

            raw[f"{cell_id}_own_n_far"] = r_own["n_far"]
            raw[f"{cell_id}_own_cyc_far"] = r_own["cyc_far"]
            raw[f"{cell_id}_b1_n_far"] = r_b1["n_far"]
            raw[f"{cell_id}_b1_cyc_far"] = r_b1["cyc_far"]
            raw[f"{cell_id}_meta"] = np.array([b, c, NN, threshold, rho,
                                                cpp_own, phi_ref_own, phi_ref_b1,
                                                r_own['dev_pct'], r_own['z'],
                                                r_own['sem_pct'],
                                                r_b1['dev_pct'], r_b1['z'],
                                                r_b1['sem_pct'],
                                                (share if share is not None else np.nan),
                                                (sem_share if sem_share is not None else np.nan)])

        t_grid1 = time.time()
        log(f"Full grid ({len(CELLS)} cells x 2 conditions) completed in "
            f"{(t_grid1-t_grid0)/60:.2f} minutes", fh)
        log("", fh)
        log("Seed table:", fh)
        for s, use, N in seed_table:
            log(f"  SeedSequence({s})  {use}  N={N}", fh)

    np.savez(os.path.join(_HERE, "ref_grid_raw.npz"), **raw)
    print("Saved ref_grid_raw.npz")


if __name__ == "__main__":
    main()
