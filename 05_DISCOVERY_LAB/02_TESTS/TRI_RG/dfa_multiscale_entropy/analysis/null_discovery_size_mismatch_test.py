"""
Adversarial null test #2 (sample-size imbalance): does the DFA-1 pipeline
itself (dfa_common.py, UNMODIFIED, imported not reimplemented) produce a
spurious systematic Delta alpha / Delta alpha1 / Delta alpha2 purely from
comparing a short segment (N=2747, PRE) against a much longer segment
(N=9195, POST) of the exact SAME underlying process (same H, independent
draws each rep -- true null, no real change), simply because:
  (a) the log-spaced scale grid n in [4, floor(0.25*N)] spans a DIFFERENT
      absolute range for different N, so the sub-grid actually landing in
      [4,16] (alpha1) or [16,n_max] (alpha2) differs in density/scales
      between PRE and POST even under identical H, and
  (b) finite-sample DFA-1 alpha estimation is not perfectly unbiased at
      small nor large N.

Method: for several H values bracketing the real observed range, draw
N_REPS independent (PRE, POST) pairs from the SAME fGn(H) generator
(Davies-Harte, reusing validate_synthetic.py's generator unmodified) with
the exact real sample sizes (primary: 2747 vs 9195; robustness: 1373 vs
4597), run dfa_common.compute_alphas (unmodified) on each side, and collect
the empirical null distribution of Delta alpha / Delta alpha1 / Delta
alpha2 under "no true change, only N differs".
"""
import sys, os, json
import numpy as np

ANALYSIS_DIR = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/TRI_RG/dfa_multiscale_entropy/analysis"
sys.path.insert(0, ANALYSIS_DIR)
from dfa_common import compute_alphas  # noqa: E402 -- pipeline import, unmodified

sys.path.insert(0, ANALYSIS_DIR)
from validate_synthetic import davies_harte_fgn  # noqa: E402 -- generator import, unmodified


def channel(alphas, ch):
    e = alphas.get(ch)
    return None if e is None else e["alpha"]


def run_null(H, n_pre, n_post, n_reps, seed):
    rng = np.random.default_rng(seed)
    deltas = {"alpha": [], "alpha1": [], "alpha2": []}
    for _ in range(n_reps):
        pre = davies_harte_fgn(n_pre, H, rng)
        post = davies_harte_fgn(n_post, H, rng)
        a_pre = compute_alphas(pre)
        a_post = compute_alphas(post)
        for ch in deltas:
            v_pre = channel(a_pre, ch)
            v_post = channel(a_post, ch)
            if v_pre is not None and v_post is not None:
                deltas[ch].append(v_post - v_pre)
    return {ch: np.array(v) for ch, v in deltas.items()}


def summarize(deltas, real_delta_alpha, real_delta_alpha1, real_delta_alpha2):
    out = {}
    real = {"alpha": real_delta_alpha, "alpha1": real_delta_alpha1, "alpha2": real_delta_alpha2}
    for ch, arr in deltas.items():
        mean = float(np.mean(arr))
        std = float(np.std(arr))
        rd = real[ch]
        z = (rd - mean) / std if std > 0 else float("inf")
        # empirical two-tailed p: fraction of null |delta| >= |real delta - null mean| is not quite
        # right; use the more standard "fraction of null draws at least as extreme as real, centered
        # on the null mean" (percentile-based), i.e. how far into the null tail the real value sits.
        frac_ge = float(np.mean(arr >= rd)) if rd >= mean else float(np.mean(arr <= rd))
        out[ch] = {
            "n_valid": int(len(arr)),
            "null_mean": mean,
            "null_std": std,
            "null_p2_5": float(np.percentile(arr, 2.5)),
            "null_p97_5": float(np.percentile(arr, 97.5)),
            "real_delta": rd,
            "z_vs_null": z,
            "one_sided_tail_frac": frac_ge,
        }
    return out


def main():
    N_REPS = 150
    results = {}

    # Real observed values (from result_apnea_a04.json)
    real_primary = {"alpha": -0.1344233799812632, "alpha1": 0.5688004909633396, "alpha2": -0.36571415823614806}
    real_robust = {"alpha": -0.16908083861494616, "alpha1": 0.3342453440667993, "alpha2": -0.34643227233716845}

    H_values = [0.5, 0.70, 0.76, 0.87, 0.94]  # brackets PRE alpha1(0.76), PRE alpha(0.94), and generic HRV range

    results["primary_size_mismatch_N2747_vs_N9195"] = {}
    for H in H_values:
        deltas = run_null(H, 2747, 9195, N_REPS, seed=1000 + int(H * 100))
        results["primary_size_mismatch_N2747_vs_N9195"][str(H)] = summarize(
            deltas, real_primary["alpha"], real_primary["alpha1"], real_primary["alpha2"]
        )
        print(f"[primary sizes] H={H}: done")

    results["robustness_size_mismatch_N1373_vs_N4597"] = {}
    for H in H_values:
        deltas = run_null(H, 1373, 4597, N_REPS, seed=2000 + int(H * 100))
        results["robustness_size_mismatch_N1373_vs_N4597"][str(H)] = summarize(
            deltas, real_robust["alpha"], real_robust["alpha1"], real_robust["alpha2"]
        )
        print(f"[robustness sizes] H={H}: done")

    # Also equal-size control (same N=2747 both sides) at H=0.87 to isolate
    # pure size-mismatch effect from pure finite-sample-noise effect.
    results["equal_size_control_N2747_H0.87"] = summarize(
        run_null(0.87, 2747, 2747, N_REPS, seed=99999),
        real_primary["alpha"], real_primary["alpha1"], real_primary["alpha2"],
    )
    print("[equal size control] done")

    out_path = "/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/null_size_mismatch_result.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_path}")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
