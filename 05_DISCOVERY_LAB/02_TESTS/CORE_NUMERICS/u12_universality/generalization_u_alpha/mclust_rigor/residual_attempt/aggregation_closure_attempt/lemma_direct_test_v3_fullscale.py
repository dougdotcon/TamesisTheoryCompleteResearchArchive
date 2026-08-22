"""aggregation_closure_attempt -- stage 1c: does the small residual in
lemma_direct_test.py's exact-form prediction shrink as n grows (finite-n
artifact of testing at a SCALED-DOWN n=8000) or stay fixed (real missing
second-order term)? Reruns the SAME (uncorrected exact-form) test at the
FULL production scale n=65536, same b,c as mclust_residual_validate.py's
grid, with no rescaling.

(lemma_direct_test_v2.py's "window-corrected" attempt made the fit WORSE,
not better, despite a seemingly valid subtraction argument -- diagnosed in
ATTEMPT.md sec 3.4 as evidence the b*k_test/n-scale mismatch is a
finite-n/finite-k_test artifact of the test harness rather than a genuine
missing physical term, since the correction should not have made things
worse if it were fixing a real effect; this script isolates finite-n
convergence directly instead of chasing the flawed correction further.)

Own implementation. Seeds: SeedSequence(20260822903) -- fresh, distinct
from every other seed in this file tree.
"""
import json
import math
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def build_instance(n, b, c, rng):
    pi = rng.permutation(n).astype(np.int64)
    in_R = rng.random(n) < c / n
    cur = np.flatnonzero(in_R)
    for _ in range(b - 1):
        cur = pi[cur]
        in_R[cur] = True
    return pi, in_R


def rho_of(c, n, b):
    return 1.0 - (1.0 - c / n) ** b


def run_cell(n, b, c, n_inst, m_x, k_test, rng):
    rho = rho_of(c, n, b)
    total_trials = 0
    total_hits = 0
    k_valid_sum = 0.0

    oversample_factor = 1.0 / max(1e-6, 1.0 - rho) + 0.5
    for _ in range(n_inst):
        pi, in_R = build_instance(n, b, c, rng)
        not_R = ~in_R
        y_test_idx = rng.choice(n, size=k_test, replace=False)
        mask_test = np.zeros(n, dtype=bool)
        mask_test[y_test_idx] = True
        k_valid = int(np.count_nonzero(mask_test & not_R))
        k_valid_sum += k_valid

        draw_n = int(m_x * oversample_factor) + 64
        cand = rng.integers(0, n, size=draw_n)
        cand = cand[not_R[cand]]
        while cand.size < m_x:
            extra = rng.integers(0, n, size=draw_n)
            extra = extra[not_R[extra]]
            cand = np.concatenate([cand, extra])
        x_valid = cand[:m_x]

        y = pi[x_valid]
        total_hits += int(np.count_nonzero(mask_test[y]))
        total_trials += m_x

    rate_emp = total_hits / total_trials
    sem_emp = math.sqrt(rate_emp * (1 - rate_emp) / total_trials)
    k_valid_mean = k_valid_sum / n_inst
    pred_exact = k_valid_mean * (1.0 - c / n) / ((1.0 - rho) * n)
    z = (rate_emp - pred_exact) / sem_emp
    return dict(n=n, b=b, c=c, rho=rho, k_valid_mean=k_valid_mean,
                rate_emp=rate_emp, sem_emp=sem_emp, pred_exact=pred_exact,
                z=z, dev_pct=(rate_emp - pred_exact) / pred_exact * 100,
                b_ktest_over_n=b * k_test / n)


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "lemma_direct_test_v3_fullscale.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# lemma_direct_test_v3_fullscale | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# SeedSequence(20260822903), fresh")

    n0 = 65536
    cells_spec = [
        (n0, 100, 400.0),
        (n0, 300, 150.0),
        (n0, 100, 600.0),
        (n0, 400, 100.0),
    ]
    seed_root = np.random.SeedSequence(20260822903)
    spawns = seed_root.spawn(len(cells_spec))

    n_inst = 60
    m_x = 4000
    k_test = 300

    out = {"cells": []}
    for (n, b, c), ss in zip(cells_spec, spawns):
        rng = np.random.default_rng(ss)
        row = run_cell(n, b, c, n_inst, m_x, k_test, rng)
        out["cells"].append(row)
        say(("n=%6d b=%3d c=%6.1f rho=%.4f b*k_test/n=%.4f | emp=%.6f+-%.6f | "
             "pred_exact=%.6f (z=%+6.2f, dev=%+.2f%%) | wall=%.1fs")
            % (n, b, c, row["rho"], row["b_ktest_over_n"],
               row["rate_emp"], row["sem_emp"], row["pred_exact"], row["z"],
               row["dev_pct"], time.time() - t0))

    chi2 = sum(r["z"] ** 2 for r in out["cells"])
    say("\n# chi2 across %d cells: %.2f" % (len(out["cells"]), chi2))
    say("# total wall time: %.1f s" % (time.time() - t0))

    with open(os.path.join(HERE, "lemma_direct_test_v3_fullscale_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved lemma_direct_test_v3_fullscale_results.json")
    log.close()


if __name__ == "__main__":
    main()
