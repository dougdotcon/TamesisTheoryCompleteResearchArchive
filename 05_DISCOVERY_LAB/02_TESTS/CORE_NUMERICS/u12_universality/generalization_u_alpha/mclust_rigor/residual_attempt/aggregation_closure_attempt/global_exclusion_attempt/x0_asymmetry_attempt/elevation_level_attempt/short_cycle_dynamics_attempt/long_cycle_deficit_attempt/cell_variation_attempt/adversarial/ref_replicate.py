"""
ref_replicate.py -- SECOND independent replicate of the two cells whose
first-replicate result carries the most weight in this review's argument:
  G1b (own-b resolved at N=6000, dev=-4.089%, z=-5.945, share=79.8% --
       highest H2-share in G1, breaks monotonicity, flips G1 sub-group
       classification) and
  G4c (b=1 companion sign-flipped relative to DOC's run, dev_b1=+0.382%
       vs doc's -1.98% -- drives the G4 sub-group flip in the hybrid
       re-analysis).
Fresh seeds, continuing this referee's reserved range (20260840100+),
confirmed unused before use.
"""
import time
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ref_measure as rm  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
_SC_DIR = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, _SC_DIR)
import sc_formula  # noqa: E402

NN = 65536
N_WORKERS = 4

CELLS = [
    ("G1b", 50, 1000, 4000, 20260840119, 20260840121),
    ("G4c", 26, 1500, 3000, 20260840120, 20260840122),
]

log_path = os.path.join(_HERE, "ref_replicate.log")
with open(log_path, "w") as fh:
    def log(msg):
        print(msg)
        fh.write(msg + "\n")
        fh.flush()

    log("ref_replicate.py -- second independent replicate, G1b and G4c")
    for cell_id, b, c, N, seed_own, seed_b1 in CELLS:
        threshold = 20 * b
        cpp_own = sc_formula.c_double_prime(b, c, NN)
        phi_ref_own = float(sc_formula.phi_U(cpp_own))
        phi_ref_b1 = float(sc_formula.phi_U(c))
        rho = sc_formula.rho_of(b, c, NN)
        log(f"--- cell {cell_id} (2nd replicate): b={b} c={c} rho={rho:.4f} "
            f"threshold={threshold} N={N} ---")

        t0 = time.time()
        r_own = rm.phi_far_and_z(NN, b, c, N, np.random.SeedSequence(seed_own),
                                  threshold, phi_ref_own, nworkers=N_WORKERS)
        t1 = time.time()
        r_b1 = rm.phi_far_and_z(NN, 1, c, N, np.random.SeedSequence(seed_b1),
                                 threshold, phi_ref_b1, nworkers=N_WORKERS)
        t2 = time.time()

        log(f"  own-b  seed={seed_own}: dev%={r_own['dev_pct']:+.3f} z={r_own['z']:+.3f} "
            f"({t1-t0:.1f}s)")
        log(f"  b=1    seed={seed_b1}: dev%={r_b1['dev_pct']:+.3f} z={r_b1['z']:+.3f} "
            f"({t2-t1:.1f}s)")
        if r_own['dev_pct'] < 0 and abs(r_own['z']) >= 2:
            share, sem_share = rm.h2_share(r_own['dev_pct'], r_b1['dev_pct'],
                                            r_own['sem_pct'], r_b1['sem_pct'])
            log(f"  H2 share = {share*100:.1f}% +- {sem_share*100:.1f}pp")
        else:
            log("  H2 share = EXCLUDED")
        log("")
print("done")
