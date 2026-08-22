"""global_exclusion_attempt -- stage 3: FRESH 18-cell validation of
phi_GLOBAL (mclust_global_formula.py) against phi_CAND and phi_CAND5,
using the SAME 18-cell grid as residual_attempt/mclust_residual_validate.py
and aggregation_closure_attempt/mclust_aggregation_validate.py, for a
direct three-way comparison.

Own implementation (does not import any predecessor validation script;
imports only mclust_global_formula.py, written in THIS subfolder).

Seeds: SeedSequence(20260822911) -- fresh, distinct from
SeedSequence(20260822910) used earlier in this subfolder for
global_exclusion_walk_measure.py, and from every seed used in
residual_attempt/ (918302033, 720330339) and aggregation_closure_attempt/
(20260822901-904).
"""
import json
import math
import os
import time

import numpy as np

from mclust_global_formula import phi_CAND, phi_CAND5, phi_GLOBAL, rho_of

HERE = os.path.dirname(os.path.abspath(__file__))


def build_f_clust(n, b, c, rng):
    pi = rng.permutation(n).astype(np.int64)
    in_R = rng.random(n) < c / n
    cur = np.flatnonzero(in_R)
    for _ in range(b - 1):
        cur = pi[cur]
        in_R[cur] = True
    R = np.flatnonzero(in_R)
    f = pi.copy()
    if R.size:
        f[R] = rng.integers(0, n, R.size)
    return f


def cyclic_fraction(f, n, log2n):
    F = f
    for _ in range(log2n):
        F = F[F]
    mask = np.zeros(n, dtype=bool)
    mask[F] = True
    return mask.sum() / n


def run_cell(n, b, c, n_rep, seed_seq, log2n):
    rng = np.random.default_rng(seed_seq)
    vals = np.empty(n_rep)
    for i in range(n_rep):
        f = build_f_clust(n, b, c, rng)
        vals[i] = cyclic_fraction(f, n, log2n)
    m = vals.mean()
    sem = vals.std(ddof=1) / math.sqrt(n_rep)
    return m, sem


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "mclust_global_validate.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# mclust_global_attempt FRESH 18-cell validation | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# own implementation, SeedSequence(20260822911), fresh (not reused "
        "anywhere else in this file tree)")

    cells = []
    for c in [10.0, 40.0, 160.0]:
        cells.append((32768, 8, c, 3000))
    for c in [10.0, 50.0, 150.0, 400.0]:
        cells.append((65536, 50, c, 4000))
    for c in [10.0, 50.0, 150.0, 400.0]:
        cells.append((65536, 100, c, 4000))
    for c in [5.0, 20.0, 60.0, 150.0]:
        cells.append((65536, 200, c, 4000))
    cells.append((65536, 300, 150.0, 4000))
    cells.append((65536, 100, 600.0, 4000))
    cells.append((65536, 400, 100.0, 4000))
    assert len(cells) == 18

    seed_root = np.random.SeedSequence(20260822911)
    spawns = seed_root.spawn(len(cells))

    out = {"cells": []}
    for (n, b, c, n_rep), ss in zip(cells, spawns):
        log2n = int(math.ceil(math.log2(n))) + 1
        m, sem = run_cell(n, b, c, n_rep, ss, log2n)
        rho = rho_of(c, n, b)
        cand = phi_CAND(c, n, b)
        cand5 = phi_CAND5(c, n, b)
        glob = phi_GLOBAL(c, n, b)
        z_cand = (m - cand) / sem
        z_cand5 = (m - cand5) / sem
        z_glob = (m - glob) / sem
        dev_cand = (m - cand) / cand * 100
        dev_cand5 = (m - cand5) / cand5 * 100
        dev_glob = (m - glob) / glob * 100
        row = dict(n=n, b=b, c=c, n_rep=n_rep, bcn=b * c / n, phi_mc=m, sem=sem,
                   rho=rho, phi_cand=cand, phi_cand5=cand5, phi_global=glob,
                   z_cand=z_cand, z_cand5=z_cand5, z_global=z_glob,
                   dev_cand_pct=dev_cand, dev_cand5_pct=dev_cand5, dev_global_pct=dev_glob)
        out["cells"].append(row)
        say("n=%6d b=%3d c=%6.1f rho=%.4f bc/n=%.4f | MC=%.6f+-%.6f | "
            "CAND dev=%+7.2f%% (z=%+6.2f) | CAND5 dev=%+7.2f%% (z=%+6.2f) | "
            "GLOBAL dev=%+7.2f%% (z=%+6.2f)"
            % (n, b, c, rho, b * c / n, m, sem, dev_cand, z_cand,
               dev_cand5, z_cand5, dev_glob, z_glob))

    chi2_cand = sum(r["z_cand"] ** 2 for r in out["cells"])
    chi2_cand5 = sum(r["z_cand5"] ** 2 for r in out["cells"])
    chi2_glob = sum(r["z_global"] ** 2 for r in out["cells"])
    say("\n# chi2 (CAND, %d cells): %.2f" % (len(out["cells"]), chi2_cand))
    say("# chi2 (CAND5, %d cells): %.2f" % (len(out["cells"]), chi2_cand5))
    say("# chi2 (GLOBAL, %d cells): %.2f" % (len(out["cells"]), chi2_glob))
    say("# wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "mclust_global_validate_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved mclust_global_validate_results.json")
    log.close()


if __name__ == "__main__":
    main()
