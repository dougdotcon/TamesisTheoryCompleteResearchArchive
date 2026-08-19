"""
Synthetic validation of `evt_hill_common.py`, BEFORE any real domain is
touched (heat wave PDX 2021 / Hurricane Florence Cape Fear gauge -- see
../METHODOLOGY_NOTE.md). Three parts, in order:

  1. Code-correctness diagnostic: xi_Hill/xi_MLE on series drawn from
     distributions with a KNOWN theoretical tail index (standard Pareto,
     Student-t) -- confirms the estimator itself is implemented
     correctly, independent of any significance test.
  2. Negative control: PRE and POST both independent draws from the SAME
     heavy-tailed distribution (same Student-t df) -- no genuine
     tail-index change. Delta_xi should NOT survive the gap (f)
     randomization test.
  3. Positive control (the critical power test): PRE and POST drawn from
     GENUINELY DIFFERENT tail-index regimes (Student-t df=10 vs df=3;
     robustness variant: Pareto shape=4 vs shape=1.5). Delta_xi SHOULD
     fall outside the gap (f) randomization null.

Every scenario uses `run_evt_hill_analysis` UNMODIFIED (the same public
entry point any agent must use for real data) -- nothing here
reimplements or shortcuts the pipeline. Full results written to
`validation_synthetic.json`.
"""
import json
import time

import numpy as np

from evt_hill_common import run_evt_hill_analysis, select_k_star, SEED, N_RANDOMIZATIONS

N_PER_SEGMENT_CORRECTNESS = 20_000   # large N for a clean code-correctness check
N_PER_SEGMENT_CONTROL = 6_000        # per-segment N for negative/positive controls
N_RAND_VALIDATION = N_RANDOMIZATIONS  # 200, same budget as the real-data protocol


def _rel_err(est, theory):
    if est is None or theory == 0:
        return None
    return float((est - theory) / theory)


def code_correctness_pareto(alpha=3.0, n=N_PER_SEGMENT_CORRECTNESS, seed=SEED):
    """Standard Pareto (numpy Generator.pareto = Lomax/Pareto-II shifted by
    +1 to strict Pareto-I support [1, inf)): P(X>x) = x^{-alpha} for x>=1.
    Theoretical Hill tail index xi = 1/alpha.
    """
    rng = np.random.default_rng(seed)
    x = rng.pareto(alpha, n) + 1.0
    xi_theory = 1.0 / alpha
    r = select_k_star(x, np.random.default_rng(seed + 1))
    return {
        "distribution": f"Pareto(alpha={alpha}), Lomax+1 construction",
        "n": n, "xi_theoretical": xi_theory,
        "k_star": r.get("k_star"), "xi_Hill": r.get("xi_Hill"), "xi_MLE": r.get("xi_MLE"),
        "rel_err_xi_Hill": _rel_err(r.get("xi_Hill"), xi_theory),
        "rel_err_xi_MLE": _rel_err(r.get("xi_MLE"), xi_theory),
        "status": r.get("status"),
    }


def code_correctness_student_t(df=4.0, n=N_PER_SEGMENT_CORRECTNESS, seed=SEED):
    """Student-t with `df` degrees of freedom: P(X>x) ~ C*x^{-df} as
    x->inf (regularly varying tail of index df -- standard EVT result for
    the t-distribution). Theoretical Hill tail index xi = 1/df.
    """
    rng = np.random.default_rng(seed)
    x = rng.standard_t(df, n)
    xi_theory = 1.0 / df
    r = select_k_star(x, np.random.default_rng(seed + 1))
    return {
        "distribution": f"Student-t(df={df})",
        "n": n, "xi_theoretical": xi_theory,
        "k_star": r.get("k_star"), "xi_Hill": r.get("xi_Hill"), "xi_MLE": r.get("xi_MLE"),
        "rel_err_xi_Hill": _rel_err(r.get("xi_Hill"), xi_theory),
        "rel_err_xi_MLE": _rel_err(r.get("xi_MLE"), xi_theory),
        "status": r.get("status"),
    }


def negative_control_student_t(df=6.0, n=N_PER_SEGMENT_CONTROL, seed=SEED,
                                n_randomizations=N_RAND_VALIDATION):
    """PRE and POST: two INDEPENDENT draws from the SAME Student-t(df).
    No genuine tail-index change -- Delta_xi should be unremarkable
    relative to the randomization null.
    """
    rng_pre = np.random.default_rng(seed + 1001)
    rng_post = np.random.default_rng(seed + 1002)
    pre = rng_pre.standard_t(df, n)
    post = rng_post.standard_t(df, n)
    t0 = time.time()
    r = run_evt_hill_analysis(pre, post, seed=seed, n_randomizations=n_randomizations)
    elapsed = time.time() - t0
    return {
        "scenario": f"negative_control_student_t(df={df})",
        "n_per_segment": n, "elapsed_seconds": elapsed,
        "xi_Hill_pre": r["real_pre"].get("xi_Hill"), "xi_Hill_post": r["real_post"].get("xi_Hill"),
        "xi_MLE_pre": r["real_pre"].get("xi_MLE"), "xi_MLE_post": r["real_post"].get("xi_MLE"),
        "delta_xi_Hill": r.get("delta_xi_Hill"), "delta_xi_MLE": r.get("delta_xi_MLE"),
        "p_xi_Hill": r.get("p_xi_Hill"), "p_xi_MLE": r.get("p_xi_MLE"),
        "random_delta_xi_Hill_mean": r["randomization"].get("random_delta_xi_Hill_mean"),
        "random_delta_xi_Hill_std": r["randomization"].get("random_delta_xi_Hill_std"),
        "random_delta_xi_MLE_mean": r["randomization"].get("random_delta_xi_MLE_mean"),
        "random_delta_xi_MLE_std": r["randomization"].get("random_delta_xi_MLE_std"),
        "n_valid_replicas": r["randomization"].get("n_valid_replicas"),
        "n_skipped": r["randomization"].get("n_skipped"),
        "status": r.get("status"),
        "full_result": r,
    }


def positive_control_student_t(df_pre=10.0, df_post=3.0, n=N_PER_SEGMENT_CONTROL, seed=SEED,
                                n_randomizations=N_RAND_VALIDATION):
    """PRE = Student-t(df=10) (xi_theory=0.1, moderate tail). POST =
    Student-t(df=3) (xi_theory=0.333, much heavier tail) -- a genuine
    difference in tail behavior, NOT a spectral/nonlinear rank-remap
    trick (that technique from other candidates in this line does not
    apply here since this is not a spectral surrogate test).
    """
    rng_pre = np.random.default_rng(seed + 2001)
    rng_post = np.random.default_rng(seed + 2002)
    pre = rng_pre.standard_t(df_pre, n)
    post = rng_post.standard_t(df_post, n)
    t0 = time.time()
    r = run_evt_hill_analysis(pre, post, seed=seed, n_randomizations=n_randomizations)
    elapsed = time.time() - t0
    return {
        "scenario": f"positive_control_student_t(df_pre={df_pre},df_post={df_post})",
        "n_per_segment": n, "elapsed_seconds": elapsed,
        "xi_theoretical_pre": 1.0 / df_pre, "xi_theoretical_post": 1.0 / df_post,
        "xi_Hill_pre": r["real_pre"].get("xi_Hill"), "xi_Hill_post": r["real_post"].get("xi_Hill"),
        "xi_MLE_pre": r["real_pre"].get("xi_MLE"), "xi_MLE_post": r["real_post"].get("xi_MLE"),
        "delta_xi_Hill": r.get("delta_xi_Hill"), "delta_xi_MLE": r.get("delta_xi_MLE"),
        "p_xi_Hill": r.get("p_xi_Hill"), "p_xi_MLE": r.get("p_xi_MLE"),
        "random_delta_xi_Hill_mean": r["randomization"].get("random_delta_xi_Hill_mean"),
        "random_delta_xi_Hill_std": r["randomization"].get("random_delta_xi_Hill_std"),
        "random_delta_xi_MLE_mean": r["randomization"].get("random_delta_xi_MLE_mean"),
        "random_delta_xi_MLE_std": r["randomization"].get("random_delta_xi_MLE_std"),
        "n_valid_replicas": r["randomization"].get("n_valid_replicas"),
        "n_skipped": r["randomization"].get("n_skipped"),
        "status": r.get("status"),
        "full_result": r,
    }


def positive_control_pareto_robustness(alpha_pre=4.0, alpha_post=1.5, n=N_PER_SEGMENT_CONTROL,
                                        seed=SEED, n_randomizations=N_RAND_VALIDATION):
    """Robustness variant of the positive control, using standard Pareto
    (Lomax+1) instead of Student-t, so the power finding does not depend
    on one specific distributional family. PRE alpha=4 (xi=0.25,
    moderate), POST alpha=1.5 (xi=0.667, much heavier).
    """
    rng_pre = np.random.default_rng(seed + 3001)
    rng_post = np.random.default_rng(seed + 3002)
    pre = rng_pre.pareto(alpha_pre, n) + 1.0
    post = rng_post.pareto(alpha_post, n) + 1.0
    t0 = time.time()
    r = run_evt_hill_analysis(pre, post, seed=seed, n_randomizations=n_randomizations)
    elapsed = time.time() - t0
    return {
        "scenario": f"positive_control_pareto_robustness(alpha_pre={alpha_pre},alpha_post={alpha_post})",
        "n_per_segment": n, "elapsed_seconds": elapsed,
        "xi_theoretical_pre": 1.0 / alpha_pre, "xi_theoretical_post": 1.0 / alpha_post,
        "xi_Hill_pre": r["real_pre"].get("xi_Hill"), "xi_Hill_post": r["real_post"].get("xi_Hill"),
        "xi_MLE_pre": r["real_pre"].get("xi_MLE"), "xi_MLE_post": r["real_post"].get("xi_MLE"),
        "delta_xi_Hill": r.get("delta_xi_Hill"), "delta_xi_MLE": r.get("delta_xi_MLE"),
        "p_xi_Hill": r.get("p_xi_Hill"), "p_xi_MLE": r.get("p_xi_MLE"),
        "random_delta_xi_Hill_mean": r["randomization"].get("random_delta_xi_Hill_mean"),
        "random_delta_xi_Hill_std": r["randomization"].get("random_delta_xi_Hill_std"),
        "random_delta_xi_MLE_mean": r["randomization"].get("random_delta_xi_MLE_mean"),
        "random_delta_xi_MLE_std": r["randomization"].get("random_delta_xi_MLE_std"),
        "n_valid_replicas": r["randomization"].get("n_valid_replicas"),
        "n_skipped": r["randomization"].get("n_skipped"),
        "status": r.get("status"),
        "full_result": r,
    }


def positive_control_student_t_unbalanced(df_pre=10.0, df_post=3.0, n_pre=1500, n_post=6000,
                                           seed=SEED, n_randomizations=N_RAND_VALIDATION):
    """Supplementary check, added AFTER the balanced positive control
    (part 3a) revealed that the gap (f) randomization null is shifted
    toward the real effect's direction when PRE and POST have EQUAL
    length and the true transition sits exactly in the middle of the
    pooled series (every random split point then necessarily mixes PRE
    and POST on at least one side). This repeats the SAME tail-index
    jump with an UNBALANCED split (n_pre << n_post, true boundary near
    the edge of the [0.2,0.8] split-point range) -- closer to what
    METHODOLOGY_NOTE.md gap (d) actually specifies for the real domains
    (PRE/POST windows of very different length is the norm, not the
    exception, per soc_avalanches's own real segments). See
    ../VALIDATION_NOTE.md section 3 for the full discussion.
    """
    rng_pre = np.random.default_rng(seed + 2001)
    rng_post = np.random.default_rng(seed + 2002)
    pre = rng_pre.standard_t(df_pre, n_pre)
    post = rng_post.standard_t(df_post, n_post)
    t0 = time.time()
    r = run_evt_hill_analysis(pre, post, seed=seed, n_randomizations=n_randomizations)
    elapsed = time.time() - t0
    s = np.array(r["randomization"]["split_points"])
    delta = np.array(r["randomization"]["random_delta_xi_Hill"])
    corr_split_delta = float(np.corrcoef(s, delta)[0, 1]) if len(s) > 1 else None
    return {
        "scenario": f"positive_control_student_t_UNBALANCED(df_pre={df_pre},df_post={df_post},"
                    f"n_pre={n_pre},n_post={n_post})",
        "n_pre": n_pre, "n_post": n_post, "true_boundary_index": n_pre, "elapsed_seconds": elapsed,
        "split_range": r["randomization"].get("split_range"),
        "xi_Hill_pre": r["real_pre"].get("xi_Hill"), "xi_Hill_post": r["real_post"].get("xi_Hill"),
        "delta_xi_Hill": r.get("delta_xi_Hill"), "delta_xi_MLE": r.get("delta_xi_MLE"),
        "p_xi_Hill": r.get("p_xi_Hill"), "p_xi_MLE": r.get("p_xi_MLE"),
        "random_delta_xi_Hill_mean": r["randomization"].get("random_delta_xi_Hill_mean"),
        "random_delta_xi_Hill_std": r["randomization"].get("random_delta_xi_Hill_std"),
        "corr_split_point_vs_random_delta_xi_Hill": corr_split_delta,
        "status": r.get("status"),
        "full_result": r,
    }


def main():
    print("=== Part 1: code-correctness diagnostic (known theoretical xi) ===")
    cc_pareto = code_correctness_pareto()
    cc_t = code_correctness_student_t()
    print(json.dumps({k: v for k, v in cc_pareto.items()}, indent=2))
    print(json.dumps({k: v for k, v in cc_t.items()}, indent=2))

    print("=== Part 2: negative control (same distribution PRE/POST) ===")
    neg = negative_control_student_t()
    print(f"  p_xi_Hill={neg['p_xi_Hill']} p_xi_MLE={neg['p_xi_MLE']} "
          f"delta_xi_Hill={neg['delta_xi_Hill']} delta_xi_MLE={neg['delta_xi_MLE']} "
          f"elapsed={neg['elapsed_seconds']:.1f}s")

    print("=== Part 3: positive control (Student-t df=10 -> df=3) ===")
    pos_t = positive_control_student_t()
    print(f"  p_xi_Hill={pos_t['p_xi_Hill']} p_xi_MLE={pos_t['p_xi_MLE']} "
          f"delta_xi_Hill={pos_t['delta_xi_Hill']} delta_xi_MLE={pos_t['delta_xi_MLE']} "
          f"elapsed={pos_t['elapsed_seconds']:.1f}s")

    print("=== Part 3b: positive control robustness (Pareto alpha=4 -> alpha=1.5) ===")
    pos_p = positive_control_pareto_robustness()
    print(f"  p_xi_Hill={pos_p['p_xi_Hill']} p_xi_MLE={pos_p['p_xi_MLE']} "
          f"delta_xi_Hill={pos_p['delta_xi_Hill']} delta_xi_MLE={pos_p['delta_xi_MLE']} "
          f"elapsed={pos_p['elapsed_seconds']:.1f}s")

    print("=== Part 3c (supplementary): positive control, UNBALANCED PRE/POST lengths ===")
    pos_t_unb = positive_control_student_t_unbalanced()
    print(f"  p_xi_Hill={pos_t_unb['p_xi_Hill']} delta_xi_Hill={pos_t_unb['delta_xi_Hill']} "
          f"corr(split,delta)={pos_t_unb['corr_split_point_vs_random_delta_xi_Hill']} "
          f"elapsed={pos_t_unb['elapsed_seconds']:.1f}s")

    out = {
        "seed": SEED,
        "n_randomizations": N_RAND_VALIDATION,
        "code_correctness": {"pareto": cc_pareto, "student_t": cc_t},
        "negative_control": neg,
        "positive_control_student_t": pos_t,
        "positive_control_pareto_robustness": pos_p,
        "positive_control_student_t_unbalanced_supplementary": pos_t_unb,
    }
    with open("validation_synthetic.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote validation_synthetic.json")


if __name__ == "__main__":
    main()
