"""aggregation_closure_attempt -- stage 1: DIRECT test of the new per-target
lemma derived in ATTEMPT.md (this subfolder) sec 3:

    P(pi(x) = y | x not in R, y not in R)
        = (1 - c/n) / [ (1-rho) * n ]          (continuum limit, n->infty, b fixed)

derived via a sequential-exposure argument (see ATTEMPT.md sec 3 for the
full derivation): conditioning on x not in R exposes x's b-1 backward-image
predecessors {x, pi^-1(x), ..., pi^-(b-2)(x)} as already-used *images* of
pi, so pi(x) is EXACTLY uniform (given a uniform random permutation, up to
O(b/n) short-cycle corrections) over the N' = n-b+1 remaining candidate
points; a further factor (1-c/n) enters because, given pi(x)=y (a generic
point disjoint from x's window), y's own R-membership check collapses to
"is y itself a seed" (all of y's OTHER b-1 backward-window checks are
already guaranteed clear by x not in R) -- an independent fresh Bernoulli
draw, probability c/n of failing (y in R).

This script tests the AGGREGATE form directly (this is the quantity that
actually matters for the finite-n hazard correction): for an EXOGENOUS
random test set Y_test subset [n], chosen independently of (pi, marks) each
instance, measure

    P(pi(x) in Y_test | x not in R)

empirically and compare to the closed-form prediction

    K_valid * (1-c/n) / [(1-rho) * n],   K_valid := |Y_test \\ R| (measured)

against the CRUDER leading-order form (predecessor's ATTEMPT.md sec 6, the
phi_CAND / phi_V4 candidate) K_valid/[(1-rho)*n] (dropping the (1-c/n)
factor), and against the NAIVE unconditional-uniform null K_test/n (no
elevation at all -- the assumption implicitly baked into phi_NEW's
unmodified 1/(1-t) crowding hazard).

Own implementation (does not import any file from residual_attempt/ or
mclust_rigor/). Seeds: SeedSequence(20260822901) -- NOT
SeedSequence(918302033), NOT SeedSequence(720330339), NOT
SeedSequence(20260822018) (wave 4). Never reused elsewhere in this
subfolder.
"""
import json
import math
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def build_instance(n, b, c, rng):
    """Own implementation of M-CLUST(b) (re-read from
    DERIVATION_MCLUST_FIXED.md sec 1 / ATTEMPT.md sec 1, independently
    written -- structurally the same vectorized block-expansion as
    mclust_walk_diagnostic.py's build_instance but re-typed from scratch,
    not imported)."""
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
    total_hits_R = 0  # sanity: pi(x) in R | x not in R, should match c/n
    k_valid_sum = 0.0
    k_valid_sq_sum = 0.0
    oversample_factor = 1.0 / max(1e-6, 1.0 - rho) + 0.5

    for _ in range(n_inst):
        pi, in_R = build_instance(n, b, c, rng)
        not_R = ~in_R

        # exogenous test set, drawn independent of (pi, marks) via the same
        # rng stream (logically independent draws -- no closed-form
        # dependency on pi/in_R introduced by sharing the PRNG object)
        y_test_idx = rng.choice(n, size=k_test, replace=False)
        mask_test = np.zeros(n, dtype=bool)
        mask_test[y_test_idx] = True
        k_valid = int(np.count_nonzero(mask_test & not_R))
        k_valid_sum += k_valid
        k_valid_sq_sum += k_valid * k_valid

        # oversample candidate x's, filter to x not in R, take first m_x
        draw_n = int(m_x * oversample_factor) + 64
        cand = rng.integers(0, n, size=draw_n)
        cand = cand[not_R[cand]]
        while cand.size < m_x:
            extra = rng.integers(0, n, size=draw_n)
            extra = extra[not_R[extra]]
            cand = np.concatenate([cand, extra])
        x_valid = cand[:m_x]

        y = pi[x_valid]
        total_hits_R += int(np.count_nonzero(in_R[y]))
        total_hits += int(np.count_nonzero(mask_test[y]))
        total_trials += m_x

    empirical_rate = total_hits / total_trials
    sem_rate = math.sqrt(empirical_rate * (1 - empirical_rate) / total_trials)
    empirical_rate_R = total_hits_R / total_trials
    sem_rate_R = math.sqrt(empirical_rate_R * (1 - empirical_rate_R) / total_trials)

    k_valid_mean = k_valid_sum / n_inst
    k_valid_var = k_valid_sq_sum / n_inst - k_valid_mean ** 2
    k_valid_sem = math.sqrt(max(k_valid_var, 0.0) / n_inst)

    pred_exact = k_valid_mean * (1.0 - c / n) / ((1.0 - rho) * n)
    pred_leading = k_valid_mean / ((1.0 - rho) * n)  # predecessor's simplified form
    pred_naive = k_valid_mean / n  # null: no elevation at all (phi_NEW's assumption)

    z_exact = (empirical_rate - pred_exact) / sem_rate
    z_leading = (empirical_rate - pred_leading) / sem_rate
    z_naive = (empirical_rate - pred_naive) / sem_rate

    return dict(
        n=n, b=b, c=c, rho=rho, n_inst=n_inst, m_x=m_x, k_test=k_test,
        total_trials=total_trials, total_hits=total_hits,
        empirical_rate=empirical_rate, sem_rate=sem_rate,
        empirical_rate_R=empirical_rate_R, sem_rate_R=sem_rate_R,
        c_over_n=c / n,
        k_valid_mean=k_valid_mean, k_valid_sem=k_valid_sem,
        pred_exact=pred_exact, pred_leading=pred_leading, pred_naive=pred_naive,
        z_exact=z_exact, z_leading=z_leading, z_naive=z_naive,
        dev_exact_pct=(empirical_rate - pred_exact) / pred_exact * 100,
        dev_leading_pct=(empirical_rate - pred_leading) / pred_leading * 100,
        dev_naive_pct=(empirical_rate - pred_naive) / pred_naive * 100,
    )


def main():
    t0 = time.time()
    log_path = os.path.join(HERE, "lemma_direct_test.log")
    log = open(log_path, "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# lemma_direct_test | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# tests P(pi(x)=y | x not in R, y not in R) aggregate form,")
    say("# own implementation, SeedSequence(20260822901), fresh (not reused)")

    # n scaled down from the 65536 grid used in ../mclust_residual_validate.py
    # so that many INSTANCES (not just many x-samples per instance) are
    # affordable -- c scaled proportionally with n so rho is EXACTLY
    # unchanged (rho depends only on c/n and b).
    n0 = 65536
    cells_spec = [
        (n0, 100, 400.0),   # rho=0.4579 (most extreme single point in wave4 grid)
        (n0, 50, 400.0),    # rho=0.2637
        (n0, 200, 150.0),   # rho=0.3676
        (n0, 300, 150.0),   # rho=0.497 (residual_attempt's new stress cell)
        (n0, 100, 600.0),   # rho=0.601 (residual_attempt's most extreme stress cell)
    ]
    n_small = 8000
    cells = [(n_small, b, c0 * n_small / n0) for (_, b, c0) in cells_spec]

    seed_root = np.random.SeedSequence(20260822901)
    spawns = seed_root.spawn(len(cells))

    n_inst = 300
    m_x = 3000
    k_test = 300

    out = {"cells": []}
    for (n, b, c), ss in zip(cells, spawns):
        rng = np.random.default_rng(ss)
        row = run_cell(n, b, c, n_inst, m_x, k_test, rng)
        out["cells"].append(row)
        say(("n=%5d b=%3d c=%7.3f rho=%.4f | sanity P(pi(x) in R|x notin R)="
             "%.6f+-%.6f (target c/n=%.6f, z=%.2f)")
            % (n, b, c, row["rho"], row["empirical_rate_R"], row["sem_rate_R"],
               row["c_over_n"], (row["empirical_rate_R"] - row["c_over_n"]) / row["sem_rate_R"]))
        say(("  P(pi(x) in Y_test|x notin R): emp=%.6f+-%.6f | "
             "pred_exact(1-c/n)/((1-rho)n)=%.6f (z=%+5.2f, dev=%+.2f%%) | "
             "pred_leading 1/((1-rho)n)=%.6f (z=%+5.2f, dev=%+.2f%%) | "
             "pred_naive 1/n=%.6f (z=%+5.2f, dev=%+.2f%%)")
            % (row["empirical_rate"], row["sem_rate"],
               row["pred_exact"], row["z_exact"], row["dev_exact_pct"],
               row["pred_leading"], row["z_leading"], row["dev_leading_pct"],
               row["pred_naive"], row["z_naive"], row["dev_naive_pct"]))
        say("  wall=%.1fs" % (time.time() - t0))

    chi2_exact = sum(r["z_exact"] ** 2 for r in out["cells"])
    chi2_leading = sum(r["z_leading"] ** 2 for r in out["cells"])
    chi2_naive = sum(r["z_naive"] ** 2 for r in out["cells"])
    say("\n# chi2 across %d cells: exact-form=%.2f  leading-form=%.2f  naive-null=%.2f"
        % (len(out["cells"]), chi2_exact, chi2_leading, chi2_naive))
    say("# total wall time: %.1f s" % (time.time() - t0))

    with open(os.path.join(HERE, "lemma_direct_test_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved lemma_direct_test_results.json")
    log.close()


if __name__ == "__main__":
    main()
