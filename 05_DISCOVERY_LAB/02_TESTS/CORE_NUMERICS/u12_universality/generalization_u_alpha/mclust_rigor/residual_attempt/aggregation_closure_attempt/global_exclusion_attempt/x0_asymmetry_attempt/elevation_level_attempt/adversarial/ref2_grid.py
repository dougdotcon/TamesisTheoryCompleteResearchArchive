"""ref2_grid.py -- the referee's own fresh validation grid for M-CLUST(b).

Same 24 cells as ATTEMPT.md section 9 (18 standard + 6 "extreme"), but with
the referee's own engine (ref2_mc.py) and fresh seeds 20260824940+.
100 000 instances per cell (5x the target's 20 000).

For every instance we retain
    |cyc| , |cyc \\ R| , |R^c|
so that the analysis can form, with a cluster bootstrap over instances,
    phi          = sum|cyc| / (N n)
    phi_notR     = sum|cyc \\ R| / sum|R^c|      <- the conditional half,
                                                   the quantity the reduction
                                                   claim (4.2) is ABOUT
    eps          = sum|cyc & R| / sum|R|

Run:  python3 ref2_grid.py <cell_index>
      python3 ref2_grid.py list
"""
import os
import sys
import time

import numpy as np

import ref2_mc as M

CELLS = [
    (32768, 8, 10), (32768, 8, 40), (32768, 8, 160),
    (65536, 50, 10), (65536, 50, 50), (65536, 50, 150), (65536, 50, 400),
    (65536, 100, 10), (65536, 100, 50), (65536, 100, 150),
    (65536, 100, 400), (65536, 100, 600),
    (65536, 200, 5), (65536, 200, 20), (65536, 200, 60), (65536, 200, 150),
    (65536, 300, 150), (65536, 400, 100),
    # extreme
    (65536, 200, 600), (65536, 800, 100), (65536, 100, 1000),
    (65536, 400, 300), (131072, 200, 800), (131072, 400, 400),
]
N_INST = 60000
SEED_BASE = 20260824940


def run(ci):
    n, b, c = CELLS[ci]
    rng = np.random.default_rng(np.random.SeedSequence(SEED_BASE + ci))
    a_cyc = np.empty(N_INST, dtype=np.int32)
    a_cyc_notR = np.empty(N_INST, dtype=np.int32)
    a_notR = np.empty(N_INST, dtype=np.int32)
    t0 = time.time()
    for i in range(N_INST):
        pi, sm, R, f = M.build_instance(rng, n, b, c)
        cyc = M.cyclic_set(f)
        a_cyc[i] = cyc.sum()
        nc = ~R
        a_cyc_notR[i] = np.count_nonzero(cyc & nc)
        a_notR[i] = np.count_nonzero(nc)
        if (i + 1) % 25000 == 0:
            print("   cell%02d n=%d b=%d c=%d  %d/%d (%.0fs)"
                  % (ci, n, b, c, i + 1, N_INST, time.time() - t0), flush=True)
    np.savez_compressed("parts/grid_%02d.npz" % ci, n_cyc=a_cyc,
                        n_cyc_notR=a_cyc_notR, n_notR=a_notR,
                        meta=np.array([n, b, c, N_INST, SEED_BASE + ci],
                                      dtype=np.float64))
    print("[done] cell%02d %.0fs" % (ci, time.time() - t0), flush=True)


if __name__ == "__main__":
    os.makedirs("parts", exist_ok=True)
    if sys.argv[1] == "list":
        for i, cl in enumerate(CELLS):
            print(i, cl)
    else:
        run(int(sys.argv[1]))
