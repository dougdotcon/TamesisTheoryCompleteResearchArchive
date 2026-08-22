"""aggregation_closure_attempt -- stage 1b: refined direct lemma test.

lemma_direct_test.py (v1) found the exact-form prediction
  K_valid * (1-c/n) / [(1-rho) n]
over-predicts the hit rate on an EXOGENOUS random test set Y_test by an
amount that GROWS with b (up to -3.35 sigma / -1.76% at b=300), while the
naive unconditional-uniform null is wrong by 40-150 sigma (confirms the
elevation is real and roughly the right size, but flags a genuine
second-order gap worth chasing down before trusting the formula).

Diagnosis (done analytically in ATTEMPT.md sec 3.3, confirmed here): pi(x),
given x not in R, is EXACTLY uniform over the N' = n-b+1 candidate points
EXCLUDING the b-1 points {x, pi^-1(x), ..., pi^-(b-2)(x)} already exposed as
*images* along x's own backward chain (pi cannot map x to any of them --
injectivity). If the exogenous Y_test happens to contain one of THESE b-1
excluded points (unavoidable at the ~b*k_test/n rate when Y_test is chosen
independent of x), that Y_test member has probability EXACTLY 0 of being
pi(x) for MOST x -- not the generic elevated density -- so counting it in
K_valid over-predicts. (For the REAL walk mechanism this never arises: the
b-1 excluded points are literally the CURRENT arc's own just-visited history,
which can never simultaneously be an EARLIER arc's start point without the
walk having already closed there first -- so Y_live is automatically disjoint
from x's own window by construction. This script exists to isolate and
confirm that this is exactly a test-harness artifact of choosing an
X-INDEPENDENT Y_test, not a flaw in the elevation formula itself.)

Fix: for each x, dynamically compute its own b-1-point excluded window and
subtract any overlap with Y_test from K_valid before predicting.

Own implementation. Seeds: SeedSequence(20260822902) -- fresh, distinct from
lemma_direct_test.py's SeedSequence(20260822901) and from every seed used in
../residual_attempt/ or wave 4.
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
    pred_const = (1.0 - c / n) / ((1.0 - rho) * n)

    total_trials = 0
    total_hits = 0
    sum_pred_uncorrected = 0.0
    sum_pred_corrected = 0.0
    overlap_events = 0
    oversample_factor = 1.0 / max(1e-6, 1.0 - rho) + 0.5

    for _ in range(n_inst):
        pi, in_R = build_instance(n, b, c, rng)
        not_R = ~in_R
        pi_inv = np.empty(n, dtype=np.int64)
        pi_inv[pi] = np.arange(n, dtype=np.int64)

        y_test_idx = rng.choice(n, size=k_test, replace=False)
        mask_test = np.zeros(n, dtype=bool)
        mask_test[y_test_idx] = True
        k_valid_total = int(np.count_nonzero(mask_test & not_R))

        draw_n = int(m_x * oversample_factor) + 64
        cand = rng.integers(0, n, size=draw_n)
        cand = cand[not_R[cand]]
        while cand.size < m_x:
            extra = rng.integers(0, n, size=draw_n)
            extra = extra[not_R[extra]]
            cand = np.concatenate([cand, extra])
        x_valid = cand[:m_x]

        # overlap count: how many of x's OWN excluded window points
        # {x, pi^-1(x), ..., pi^-(b-2)(x)} (b-1 points) are in Y_test.
        cur = x_valid.copy()
        overlap = np.zeros(m_x, dtype=np.int64)
        for _step in range(b - 1):
            # only subtract window points that were ACTUALLY counted in
            # K_valid_total, i.e. that are in Y_test AND in R^c (a window
            # point can be non-seed -- guaranteed by x not in R -- yet
            # still land in R via an unconstrained point one step further
            # back; such a point was never part of K_valid_total and must
            # not be subtracted)
            overlap += mask_test[cur] & not_R[cur]
            cur = pi_inv[cur]
        overlap_events += int(overlap.sum())

        k_eff = k_valid_total - overlap  # per-x effective live-target count
        sum_pred_uncorrected += m_x * pred_const * k_valid_total
        sum_pred_corrected += pred_const * k_eff.sum()

        y = pi[x_valid]
        total_hits += int(np.count_nonzero(mask_test[y]))
        total_trials += m_x

    rate_emp = total_hits / total_trials
    sem_emp = math.sqrt(rate_emp * (1 - rate_emp) / total_trials)
    rate_pred_uncorr = sum_pred_uncorrected / total_trials
    rate_pred_corr = sum_pred_corrected / total_trials

    z_uncorr = (rate_emp - rate_pred_uncorr) / sem_emp
    z_corr = (rate_emp - rate_pred_corr) / sem_emp

    return dict(
        n=n, b=b, c=c, rho=rho, n_inst=n_inst, m_x=m_x, k_test=k_test,
        total_trials=total_trials, total_hits=total_hits,
        overlap_events=overlap_events,
        mean_overlap_per_x=overlap_events / total_trials,
        rate_emp=rate_emp, sem_emp=sem_emp,
        rate_pred_uncorrected=rate_pred_uncorr,
        rate_pred_corrected=rate_pred_corr,
        z_uncorrected=z_uncorr, z_corrected=z_corr,
        dev_uncorrected_pct=(rate_emp - rate_pred_uncorr) / rate_pred_uncorr * 100,
        dev_corrected_pct=(rate_emp - rate_pred_corr) / rate_pred_corr * 100,
    )


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "lemma_direct_test_v2.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# lemma_direct_test_v2 | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# own implementation, SeedSequence(20260822902), fresh (not reused)")

    n0 = 65536
    cells_spec = [
        (n0, 100, 400.0),
        (n0, 50, 400.0),
        (n0, 200, 150.0),
        (n0, 300, 150.0),
        (n0, 100, 600.0),
        (n0, 400, 100.0),
    ]
    n_small = 8000
    cells = [(n_small, b, c0 * n_small / n0) for (_, b, c0) in cells_spec]

    seed_root = np.random.SeedSequence(20260822902)
    spawns = seed_root.spawn(len(cells))

    n_inst = 300
    m_x = 3000
    k_test = 300

    out = {"cells": []}
    for (n, b, c), ss in zip(cells, spawns):
        rng = np.random.default_rng(ss)
        row = run_cell(n, b, c, n_inst, m_x, k_test, rng)
        out["cells"].append(row)
        say(("n=%5d b=%3d c=%7.3f rho=%.4f | mean overlap/x=%.3f (b*k_test/n=%.3f) | "
             "emp=%.6f+-%.6f")
            % (n, b, c, row["rho"], row["mean_overlap_per_x"], b * k_test / n,
               row["rate_emp"], row["sem_emp"]))
        say(("  uncorrected pred=%.6f (z=%+6.2f, dev=%+.2f%%) | "
             "corrected pred=%.6f (z=%+6.2f, dev=%+.2f%%)")
            % (row["rate_pred_uncorrected"], row["z_uncorrected"], row["dev_uncorrected_pct"],
               row["rate_pred_corrected"], row["z_corrected"], row["dev_corrected_pct"]))

    chi2_uncorr = sum(r["z_uncorrected"] ** 2 for r in out["cells"])
    chi2_corr = sum(r["z_corrected"] ** 2 for r in out["cells"])
    say("\n# chi2 across %d cells: uncorrected=%.2f  window-corrected=%.2f"
        % (len(out["cells"]), chi2_uncorr, chi2_corr))
    say("# total wall time: %.1f s" % (time.time() - t0))

    with open(os.path.join(HERE, "lemma_direct_test_v2_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved lemma_direct_test_v2_results.json")
    log.close()


if __name__ == "__main__":
    main()
