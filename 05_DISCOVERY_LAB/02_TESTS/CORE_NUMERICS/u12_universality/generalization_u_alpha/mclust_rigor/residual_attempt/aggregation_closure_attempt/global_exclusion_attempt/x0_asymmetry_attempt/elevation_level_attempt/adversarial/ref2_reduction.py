"""ref2_reduction.py -- the referee's own formula-free test of the reduction
claim (4.1) of `elevation_level_attempt/ATTEMPT.md`.

Claim under test
----------------
    conditioned on x0 notin R, M-CLUST(b) at (c, n)  ==  M-U at (c', n')

with, in the document,  n' = (1-rho) n ,  c' = c(1-rho)          [convention A]

The referee's own matching analysis (ref2_algebra.py section 8) says the
expected world AND pool of M-CLUST(b)|x0 notin R are

    world |R^c|   = n (1-c/n)^b        pool |U_rem| = n (1-c/n)^(b-1)

while M-U at (C, N) has world N-C and pool N.  Both match exactly iff

    N = n (1-c/n)^(b-1) ,  C = c (1-c/n)^(b-1)                    [convention B]

which is the document's own secondary convention n'=(1-rho)(n+c) to O(c^2/n).
Convention A undershoots both world and pool by ~c(1-rho) points.  Both are
simulated here so the data can choose.

Everything is measured; no master formula, no quadrature, no elevation model
and no eps model enters on either side.

Seeds: SeedSequence(20260824920 + job index), fresh.
Run:   python3 ref2_reduction.py <job_index>      (one job per process)
       python3 ref2_reduction.py list
"""
import json
import os
import sys
import time

import numpy as np

import ref2_mc as M

# (b, c, n) source cells, spanning rho
CELLS = [
    (50, 400, 65536),
    (100, 400, 65536),
    (100, 600, 65536),
    (200, 150, 65536),
    (400, 100, 65536),
    (100, 1000, 65536),
]

N_INST_CLUST = 300000
N_INST_MU = 400000
SEED_BASE = 20260824920


def conventions(b, c, n):
    p = c / n
    rho = 1.0 - (1.0 - p) ** b
    NA = int(round((1.0 - rho) * n))
    CA = c * (1.0 - rho)
    NB = int(round(n * (1.0 - p) ** (b - 1)))
    CB = c * (1.0 - p) ** (b - 1)
    return dict(rho=rho, NA=NA, CA=CA, NB=NB, CB=CB)


def jobs():
    out = []
    for (b, c, n) in CELLS:
        cv = conventions(b, c, n)
        out.append(dict(kind="clust", b=b, c=c, n=n, n_inst=N_INST_CLUST,
                        tag="clust_b%d_c%d" % (b, c)))
        out.append(dict(kind="mu", b=1, c=cv["CA"], n=cv["NA"],
                        n_inst=N_INST_MU,
                        tag="muA_b%d_c%d" % (b, c)))
        out.append(dict(kind="mu", b=1, c=cv["CB"], n=cv["NB"],
                        n_inst=N_INST_MU,
                        tag="muB_b%d_c%d" % (b, c)))
    return out


def run_job(j, ji):
    rng = np.random.default_rng(np.random.SeedSequence(SEED_BASE + ji))
    n, b, c, N = j["n"], j["b"], j["c"], j["n_inst"]
    a_cyc = np.empty(N, dtype=np.int32)
    a_cyc_notR = np.empty(N, dtype=np.int32)
    a_notR = np.empty(N, dtype=np.int32)
    t0 = time.time()
    for i in range(N):
        pi, sm, R, f = M.build_instance(rng, n, b, c)
        cyc = M.cyclic_set(f)
        a_cyc[i] = cyc.sum()
        nR_c = ~R
        a_cyc_notR[i] = np.count_nonzero(cyc & nR_c)
        a_notR[i] = np.count_nonzero(nR_c)
        if (i + 1) % 50000 == 0:
            print("   %s %d/%d  (%.0fs)" % (j["tag"], i + 1, N,
                                            time.time() - t0), flush=True)
    np.savez_compressed("parts/red_%s.npz" % j["tag"],
                        n_cyc=a_cyc, n_cyc_notR=a_cyc_notR, n_notR=a_notR,
                        meta=np.array([n, b, c, N, SEED_BASE + ji],
                                      dtype=np.float64))
    print("[done] %s  %.0fs" % (j["tag"], time.time() - t0), flush=True)


if __name__ == "__main__":
    os.makedirs("parts", exist_ok=True)
    J = jobs()
    if sys.argv[1] == "list":
        for i, j in enumerate(J):
            print(i, j)
    else:
        ji = int(sys.argv[1])
        run_job(J[ji], ji)
