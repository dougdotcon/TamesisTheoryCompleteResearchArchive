"""
Synthetic validation of `dfa_common.py`, run and committed BEFORE any real
PRE/POST segment (PhysioNet Apnea-ECG a04, GISP2) is touched -- required by
METHODOLOGY_NOTE.md "Validacao contra dado sintetico".

fGn (fractional Gaussian noise) generator: exact circulant-embedding method
of Davies & Harte (1987), "Tests for Hurst effect", Biometrika 74:95-101,
with the Wood & Chan (1994, J. Comput. Graph. Statist. 3:409-432) padding
fallback for H close to 1 where the minimal 2n-embedding can produce
slightly negative eigenvalues. This machine has neither `fbm` nor
`stochastic` installed (checked explicitly below / at run time), so the
generator is implemented directly here from the cited papers rather than
assumed available.

DFA-1 of an fGn sample recovers alpha = H directly (Peng et al.); DFA-1 of
its cumulative sum (fBm) recovers alpha = H + 1. This is exploited below:
white noise is fGn(H=0.5) fed directly (alpha ~ 0.5 expected); the random
walk is its cumulative sum (alpha ~ 1.5 expected).

Also validates the moving-block bootstrap (Kunsch 1989) significance test
added in METHODOLOGY_NOTE.md "Adendo ao Gap (c) -- teste complementar de
bootstrap por blocos": `run_dfa_pipeline` (called below for the positive and
negative controls) now computes it automatically alongside IAAFT, using the
same fixed seed=12345 convention; this script surfaces those fields and adds
an explicit `bootstrap_power_check` verdict block (item 5 of the
methodology-note validation checklist).

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import sys
import os

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dfa_common import compute_alphas, run_dfa_pipeline, max_min_ratio, MAX_MIN_RATIO_ALERT_THRESHOLD


def davies_harte_fgn(n, H, rng, pad_factor_max=8, tol=1e-8):
    """Exact fGn(n, H) via Davies-Harte circulant embedding (see module docstring)."""
    pad = 1
    while pad <= pad_factor_max:
        g = pad * n  # embedding half-length (need g >= n-1; use g=pad*n for margin)
        lags = np.concatenate([np.arange(0, g + 1), np.arange(g - 1, 0, -1)])
        r = 0.5 * (np.abs(lags - 1) ** (2 * H) - 2 * np.abs(lags) ** (2 * H) + np.abs(lags + 1) ** (2 * H))
        eigs = np.fft.fft(r).real
        m = 2 * g
        if eigs.min() >= -tol * m:
            eigs = np.clip(eigs, 0.0, None)  # Wood & Chan fallback: clip residual tiny negatives
            break
        pad *= 2
    else:
        raise RuntimeError(f"Davies-Harte embedding failed to reach non-negative eigenvalues for H={H}, n={n}")

    V = np.zeros(m, dtype=complex)
    V[0] = rng.standard_normal() * np.sqrt(eigs[0] / m)
    V[g] = rng.standard_normal() * np.sqrt(eigs[g] / m)
    u1 = rng.standard_normal(g - 1)
    u2 = rng.standard_normal(g - 1)
    k = np.arange(1, g)
    Vk = np.sqrt(eigs[k] / (2 * m)) * (u1 + 1j * u2)
    V[1:g] = Vk
    V[m - 1:m - g:-1] = np.conj(Vk)  # V[m-k] = conj(V[k]) for k=1..g-1

    Y = np.fft.fft(V)
    fgn = Y.real[:n]
    return fgn


def check_fbm_stochastic_available():
    for name in ("fbm", "stochastic"):
        try:
            __import__(name)
            return name
        except ImportError:
            continue
    return None


def main():
    results = {}
    lib = check_fbm_stochastic_available()
    results["fgn_generator_method"] = (
        f"'{lib}' package found but NOT used -- Davies-Harte circulant embedding "
        f"implemented directly (Davies & Harte 1987; Wood & Chan 1994 padding fallback), "
        f"documented in validate_synthetic.py, for full control/citability."
        if lib else
        "Neither 'fbm' nor 'stochastic' is installed in this environment (checked at run "
        "time via ImportError). Used Davies & Harte (1987) exact circulant-embedding "
        "method for fGn, with the Wood & Chan (1994) padding fallback for eigenvalue "
        "negativity near H=1, implemented directly in validate_synthetic.py."
    )

    rng_master = np.random.default_rng(SEED := 999999)  # separate from pipeline SEED=12345, for generator draws

    # ---- 1. Sanity: white noise (alpha ~ 0.5) and random walk (alpha ~ 1.5) ----
    N_SANITY = 4000
    white = davies_harte_fgn(N_SANITY, 0.5, rng_master)
    walk = np.cumsum(white if False else davies_harte_fgn(N_SANITY, 0.5, rng_master))
    # (walk uses an independent fGn(H=0.5) draw, then integrated -> fBm(H=0.5), alpha ~ H+1 = 1.5)

    white_fit = compute_alphas(white)
    walk_fit = compute_alphas(walk)

    results["sanity"] = {
        "white_noise": {
            "n_samples": N_SANITY,
            "alpha": white_fit["alpha"]["alpha"],
            "alpha1": white_fit["alpha1"]["alpha"] if white_fit["alpha1"] else None,
            "alpha2": white_fit["alpha2"]["alpha"] if white_fit["alpha2"] else None,
            "max_min_ratio": white_fit["max_min_ratio"],
            "theoretical_alpha": 0.5,
        },
        "random_walk": {
            "n_samples": N_SANITY,
            "alpha": walk_fit["alpha"]["alpha"],
            "alpha1": walk_fit["alpha1"]["alpha"] if walk_fit["alpha1"] else None,
            "alpha2": walk_fit["alpha2"]["alpha"] if walk_fit["alpha2"] else None,
            "max_min_ratio": walk_fit["max_min_ratio"],
            "theoretical_alpha": 1.5,
        },
    }

    # ---- 2. Positive control: PRE = fGn(H=0.5), POST = fGn(H=0.9), independent draws ----
    N_CTRL = 4000
    rng_gen = np.random.default_rng(424242)
    pos_pre = davies_harte_fgn(N_CTRL, 0.5, rng_gen)
    pos_post = davies_harte_fgn(N_CTRL, 0.9, rng_gen)
    pos_result = run_dfa_pipeline(pos_pre, pos_post)
    results["positive_control"] = {
        "pre_H_nominal": 0.5,
        "post_H_nominal": 0.9,
        "n_pre": N_CTRL,
        "n_post": N_CTRL,
        "alpha_pre": pos_result["real_pre"]["alpha"]["alpha"],
        "alpha_post": pos_result["real_post"]["alpha"]["alpha"],
        "alpha1_pre": pos_result["real_pre"]["alpha1"]["alpha"] if pos_result["real_pre"]["alpha1"] else None,
        "alpha1_post": pos_result["real_post"]["alpha1"]["alpha"] if pos_result["real_post"]["alpha1"] else None,
        "alpha2_pre": pos_result["real_pre"]["alpha2"]["alpha"] if pos_result["real_pre"]["alpha2"] else None,
        "alpha2_post": pos_result["real_post"]["alpha2"]["alpha"] if pos_result["real_post"]["alpha2"] else None,
        "delta_alpha": pos_result["delta_alpha"],
        "delta_alpha1": pos_result["delta_alpha1"],
        "delta_alpha2": pos_result["delta_alpha2"],
        "p_alpha": pos_result["p_alpha"],
        "p_alpha1": pos_result["p_alpha1"],
        "p_alpha2": pos_result["p_alpha2"],
        "max_min_ratio_pre": pos_result["real_pre"]["max_min_ratio"],
        "max_min_ratio_post": pos_result["real_post"]["max_min_ratio"],
        "surrogate_max_min_ratio_pre": pos_result["surrogate_max_min_ratio_pre"],
        "surrogate_max_min_ratio_post": pos_result["surrogate_max_min_ratio_post"],
        "surrogate_alpha_mean": pos_result["surrogate_alpha_mean"],
        "surrogate_alpha_std": pos_result["surrogate_alpha_std"],
        "surrogate_alpha_n_valid": pos_result["surrogate_alpha_n_valid"],
        # Moving-block bootstrap (Kunsch 1989), METHODOLOGY_NOTE.md "Adendo
        # ao Gap (c)" -- PRIMARY significance test, added because the IAAFT
        # test above (p_alpha=0.255) has low power to detect this
        # unambiguous-by-construction change in alpha.
        "delta_alpha_boot_ci95": pos_result["delta_alpha_boot_ci95"],
        "delta_alpha1_boot_ci95": pos_result["delta_alpha1_boot_ci95"],
        "delta_alpha2_boot_ci95": pos_result["delta_alpha2_boot_ci95"],
        "p_bootstrap_alpha": pos_result["p_bootstrap_alpha"],
        "p_bootstrap_alpha1": pos_result["p_bootstrap_alpha1"],
        "p_bootstrap_alpha2": pos_result["p_bootstrap_alpha2"],
        "delta_alpha_boot_mean": pos_result["delta_alpha_boot_mean"],
        "delta_alpha_boot_std": pos_result["delta_alpha_boot_std"],
        "bootstrap_block_length_pre": pos_result["bootstrap_block_length_pre"],
        "bootstrap_block_length_post": pos_result["bootstrap_block_length_post"],
        "bootstrap_n_bootstrap": pos_result["bootstrap_n_bootstrap"],
    }

    # ---- 3. Negative control: PRE and POST = fGn(same H), independent draws ----
    H_NEG = 0.7
    rng_gen2 = np.random.default_rng(13131313)
    neg_pre = davies_harte_fgn(N_CTRL, H_NEG, rng_gen2)
    neg_post = davies_harte_fgn(N_CTRL, H_NEG, rng_gen2)
    neg_result = run_dfa_pipeline(neg_pre, neg_post)
    results["negative_control"] = {
        "H_nominal": H_NEG,
        "n_pre": N_CTRL,
        "n_post": N_CTRL,
        "alpha_pre": neg_result["real_pre"]["alpha"]["alpha"],
        "alpha_post": neg_result["real_post"]["alpha"]["alpha"],
        "alpha1_pre": neg_result["real_pre"]["alpha1"]["alpha"] if neg_result["real_pre"]["alpha1"] else None,
        "alpha1_post": neg_result["real_post"]["alpha1"]["alpha"] if neg_result["real_post"]["alpha1"] else None,
        "alpha2_pre": neg_result["real_pre"]["alpha2"]["alpha"] if neg_result["real_pre"]["alpha2"] else None,
        "alpha2_post": neg_result["real_post"]["alpha2"]["alpha"] if neg_result["real_post"]["alpha2"] else None,
        "delta_alpha": neg_result["delta_alpha"],
        "delta_alpha1": neg_result["delta_alpha1"],
        "delta_alpha2": neg_result["delta_alpha2"],
        "p_alpha": neg_result["p_alpha"],
        "p_alpha1": neg_result["p_alpha1"],
        "p_alpha2": neg_result["p_alpha2"],
        "max_min_ratio_pre": neg_result["real_pre"]["max_min_ratio"],
        "max_min_ratio_post": neg_result["real_post"]["max_min_ratio"],
        "surrogate_max_min_ratio_pre": neg_result["surrogate_max_min_ratio_pre"],
        "surrogate_max_min_ratio_post": neg_result["surrogate_max_min_ratio_post"],
        # Moving-block bootstrap (Kunsch 1989), METHODOLOGY_NOTE.md "Adendo
        # ao Gap (c)" -- PRIMARY significance test; must stay correctly
        # non-significant here (same H, independent draws -- no real change).
        "delta_alpha_boot_ci95": neg_result["delta_alpha_boot_ci95"],
        "delta_alpha1_boot_ci95": neg_result["delta_alpha1_boot_ci95"],
        "delta_alpha2_boot_ci95": neg_result["delta_alpha2_boot_ci95"],
        "p_bootstrap_alpha": neg_result["p_bootstrap_alpha"],
        "p_bootstrap_alpha1": neg_result["p_bootstrap_alpha1"],
        "p_bootstrap_alpha2": neg_result["p_bootstrap_alpha2"],
        "delta_alpha_boot_mean": neg_result["delta_alpha_boot_mean"],
        "delta_alpha_boot_std": neg_result["delta_alpha_boot_std"],
        "bootstrap_block_length_pre": neg_result["bootstrap_block_length_pre"],
        "bootstrap_block_length_post": neg_result["bootstrap_block_length_post"],
        "bootstrap_n_bootstrap": neg_result["bootstrap_n_bootstrap"],
    }

    # ---- 4. Marginal-degeneracy diagnostic check ----
    # The zero-mean fGn/fBm draws above are signed and cross zero, so
    # max_min_ratio() correctly reports them as "not applicable" (see
    # dfa_common.max_min_ratio docstring for why abs()-based ratios on a
    # zero-crossing series would be a meaningless, trivially-huge artifact).
    # To actually exercise the diagnostic (and prove it does NOT just always
    # fire, nor always stay silent), build two POSITIVE-valued synthetic
    # analogs bounded away from zero:
    #   - "well_behaved_positive": RR-interval-like series, baseline 800 +
    #     fGn(H=0.5) fluctuations of std ~40ms (physiologically plausible
    #     range, comparable to real PhysioNet RR intervals) -> low ratio.
    #   - "degenerate_positive": exp() of a wide-variance fGn draw -- a
    #     positive, heavy-tailed construction in the same spirit as the
    #     multiplicative cascade that produced the ~190x diagnostic ratio
    #     for wavelet-multiresolution-scaling -> ratio should exceed the
    #     alert threshold, confirming the check actually detects it.
    rng_diag = np.random.default_rng(777)
    rr_like = 800.0 + 40.0 * davies_harte_fgn(N_CTRL, 0.5, rng_diag)
    rr_ratio = max_min_ratio(rr_like)

    heavy_tail_like = np.exp(1.5 * davies_harte_fgn(N_CTRL, 0.5, rng_diag))
    heavy_tail_ratio = max_min_ratio(heavy_tail_like)

    ratios = {
        "white_noise": results["sanity"]["white_noise"]["max_min_ratio"],
        "random_walk": results["sanity"]["random_walk"]["max_min_ratio"],
        "positive_control_pre": results["positive_control"]["max_min_ratio_pre"],
        "positive_control_post": results["positive_control"]["max_min_ratio_post"],
        "negative_control_pre": results["negative_control"]["max_min_ratio_pre"],
        "negative_control_post": results["negative_control"]["max_min_ratio_post"],
        "well_behaved_positive_rr_like": rr_ratio,
        "degenerate_positive_synthetic": heavy_tail_ratio,
    }
    numeric_ratios = {k: v["ratio"] for k, v in ratios.items() if v["ratio"] is not None}
    results["marginal_degeneracy_check"] = {
        "alert_threshold": MAX_MIN_RATIO_ALERT_THRESHOLD,
        "ratios": ratios,
        "any_above_threshold": any(v >= MAX_MIN_RATIO_ALERT_THRESHOLD for v in numeric_ratios.values()),
        "note": (
            "The zero-mean fGn/fBm draws used for the alpha-detection sanity/positive/"
            "negative checks are signed and cross zero, so max_min_ratio() reports them "
            "as not_applicable (see dfa_common.max_min_ratio docstring) rather than a "
            "meaningless abs()-based number. The diagnostic itself is exercised instead "
            "on two purpose-built POSITIVE synthetic series bounded away from zero: a "
            "well-behaved RR-interval-like series (baseline 800 +/- fGn fluctuations, "
            "low ratio, as real PhysioNet RR intervals should look) and a deliberately "
            "heavy-tailed positive construction (exp of wide-variance fGn, in the same "
            "spirit as the multiplicative cascade that produced the ~190x threshold for "
            "wavelet-multiresolution-scaling) to confirm the check actually fires when "
            "it should. Real PRE/POST segments (RR intervals, GISP2 proxy values) will "
            "be strictly positive and this same function applies to them unmodified."
        ),
    }

    # ---- 5. Explicit bootstrap-power validation check (METHODOLOGY_NOTE.md
    # "Adendo ao Gap (c)" item 5): confirm the block bootstrap recovers power
    # in the positive control where IAAFT failed, and stays correctly
    # non-significant in the negative control. ----
    pos_ci = results["positive_control"]["delta_alpha_boot_ci95"]
    pos_p_boot = results["positive_control"]["p_bootstrap_alpha"]
    pos_ci_excludes_zero = (pos_ci[0] is not None) and not (pos_ci[0] <= 0.0 <= pos_ci[1])
    pos_significant = (pos_p_boot is not None) and (pos_p_boot < 0.05)

    neg_ci = results["negative_control"]["delta_alpha_boot_ci95"]
    neg_p_boot = results["negative_control"]["p_bootstrap_alpha"]
    neg_ci_includes_zero = (neg_ci[0] is not None) and (neg_ci[0] <= 0.0 <= neg_ci[1])
    neg_correctly_nonsignificant = (neg_p_boot is not None) and (neg_p_boot >= 0.05)

    results["bootstrap_power_check"] = {
        "positive_control": {
            "iaaft_p_alpha": results["positive_control"]["p_alpha"],
            "iaaft_significant_at_0.05": results["positive_control"]["p_alpha"] is not None
                and results["positive_control"]["p_alpha"] < 0.05,
            "bootstrap_p_alpha": pos_p_boot,
            "bootstrap_delta_alpha_ci95": pos_ci,
            "bootstrap_ci_excludes_zero": pos_ci_excludes_zero,
            "bootstrap_significant_at_0.05": pos_significant,
            "power_recovered": bool(pos_ci_excludes_zero and pos_significant),
        },
        "negative_control": {
            "iaaft_p_alpha": results["negative_control"]["p_alpha"],
            "bootstrap_p_alpha": neg_p_boot,
            "bootstrap_delta_alpha_ci95": neg_ci,
            "bootstrap_ci_includes_zero": neg_ci_includes_zero,
            "bootstrap_correctly_nonsignificant": neg_correctly_nonsignificant,
        },
        "note": (
            "Per METHODOLOGY_NOTE.md 'Adendo ao Gap (c)', the moving-block "
            "bootstrap (Kunsch 1989) is now the PRIMARY significance test for "
            "Delta alpha; IAAFT is retained as a complementary/secondary check "
            "(a narrower question about nonlinear structure beyond each "
            "segment's linear spectrum). power_recovered=true and "
            "bootstrap_correctly_nonsignificant=true together are the pass "
            "condition for closing the synthetic-validation gate before any "
            "real PRE/POST segment (PhysioNet Apnea-ECG, GISP2) is touched."
        ),
    }

    results["pipeline_config"] = pos_result["config"]

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
