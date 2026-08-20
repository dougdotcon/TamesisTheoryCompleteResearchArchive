"""
Synthetic validation of `ph_common.py`, run and committed BEFORE any real
PRE/POST segment (LIGO GW150914 strain, S&P500 around the Lehman Brothers
bankruptcy) is touched -- required by METHODOLOGY_NOTE.md Gap (c)
"Validacao obrigatoria de PODER, ANTES de qualquer dado real": since IAAFT
is the PRIMARY significance test for this candidate (Gap (e)), this script
must confirm IAAFT has real power to detect a genuine nonlinear/dynamical
change in max/total H1 persistence before the pipeline can be applied to
real data -- exactly the same requirement already used for every other
candidate in this line, and the DECISIVE test of the central
identifiability risk this candidate was formalized to check: Phase 0.6's
own informal check (noisy sinusoid, 9 noise levels) found max-H1-
persistence correlated with an RQA-%DET analog at r~=0.92 in the
structure-degradation regime most relevant to detecting a transition --
but RQA's %DET itself NEVER showed real IAAFT power (p=1.0 on both
channels, even in its best-case positive-control redesign, see
../../rqa/VALIDATION_NOTE.md). A high raw correlation between two
statistics in noise-degradation does not by itself imply persistent
homology inherits RQA's lack of power -- this script tests that directly.

Checks, all synthetic, all seeded for reproducibility:

0. Embedding+Rips CODE-CORRECTNESS diagnostic (NOT part of the
   identifiability validation itself, reported separately and clearly
   labeled as supplementary): a clean, strongly periodic deterministic
   sine wave, Takens-embedded with m=3, should trace out a clear closed
   loop in phase space and give a large, unambiguous max-H1-persistence
   value -- confirms the embedding/sub-window/Rips/persistence-extraction
   code is right before testing it on genuinely ambiguous stochastic data
   (mirrors how `rqa` and `kramers_moyal` used a deterministic diagnostic
   first).

1. Negative control: PRE and POST = two INDEPENDENT realizations of the
   SAME fGn-like process (H=0.7 fixed, independent seeds) -- probes
   Gap (c)'s named spectral/linear risk directly: same H, no genuine
   structural change, p should typically be non-significant for both
   channels.

2. Positive control -- THE central power test for this candidate, EXACTLY
   as specified in METHODOLOGY_NOTE.md Gap (c): PRE = white Gaussian
   noise. POST = logistic map (r=4, fully chaotic) rank-remapped onto
   PRE's own exact empirical distribution (same technique used throughout
   this line: mse_multiscale_entropy, visibility_graph, rqa,
   kramers_moyal) so PRE and POST share an EXACTLY identical marginal and
   (both being near-broadband processes) closely matched spectra. IAAFT
   surrogates preserve spectrum+marginal but destroy the logistic map's
   determinism; if max/total-H1-persistence respond to that determinism
   specifically, the real Delta should sit outside the IAAFT null
   (p small) for at least one channel. *** THIS IS THE DECISIVE CHECK OF
   THE r~=0.92 IDENTIFIABILITY RISK NAMED IN METHODOLOGY_NOTE.md Gap (c):
   unlike RQA, this candidate's embedding does NOT depend on FNN (m=3 is
   FIXED), so white noise as PRE is NOT expected to block the embedding
   step the way it blocked RQA's shared-embedding convention -- this
   check can actually run to completion, unlike RQA's Gap (b) positive
   control. ***

3. IAAFT power-check verdict, reported per channel (max_persistence,
   total_persistence), honestly, whichever pattern emerges -- this is the
   central scientific question of this validation: does persistent
   homology carry power RQA's %DET never demonstrated, or does it inherit
   the same lack of power despite the r~=0.92 raw correlation in
   noise-degradation?

4. If either channel shows low IAAFT power (mirroring DFA-alpha's
   pattern): the pre-authorized moving-block bootstrap (Kunsch 1989)
   fallback (METHODOLOGY_NOTE.md Gap (c)) is exercised on that channel
   and re-validated, exactly as done for `rqa` and `kramers_moyal`.

5. Wall-clock cost of a single full run_ph_analysis call (N~=3000,
   N_SURROGATES=200) is measured and reported explicitly (task
   requirement), so the real-domain step's tractability is known before
   it is attempted.

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ph_common import (
    run_ph_analysis, estimate_tau, compute_ph_features, run_block_bootstrap_test,
    moving_block_bootstrap_resample, N_SURROGATES, N_IAAFT_ITER, SEED, M_FIXED,
    N_WINDOW, K_SUBWINDOWS_MAX,
)


# --------------------------------------------------------------------------
# Synthetic generators (independent implementation for this test line, same
# spirit/technique as rqa's/kramers_moyal's validate_synthetic.py but not
# imported from them)
# --------------------------------------------------------------------------

def colored_noise(n, spectral_exponent, rng):
    """Gaussian colored noise, PSD ~ 1/f^exponent, FFT-filtering spectral
    synthesis. exponent=0 ~ white noise. Used here as an fGn-like generator:
    an fGn of Hurst exponent H has PSD ~ f^-(2H+1), so exponent=2H+1
    approximates fGn with that H (standard spectral-synthesis approximation,
    same technique used throughout this line, not a literal Davies-Harte
    exact-covariance fGn generator)."""
    white = rng.standard_normal(n)
    spectrum = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n)
    scale = np.zeros_like(freqs)
    scale[1:] = freqs[1:] ** (-spectral_exponent / 2.0)
    x = np.fft.irfft(spectrum * scale, n=n)
    return (x - x.mean()) / x.std()


def fgn_like(n, H, rng):
    return colored_noise(n, 2 * H + 1, rng)


def logistic_map(n, x0, r=4.0, burn_in=500):
    """Fully chaotic logistic map trajectory x_{k+1} = r*x_k*(1-x_k), r=4."""
    total = n + burn_in
    x = np.empty(total, dtype=float)
    x[0] = x0
    for i in range(1, total):
        x[i] = r * x[i - 1] * (1.0 - x[i - 1])
    return x[burn_in:]


def rank_remap_to_reference(x, reference):
    """Return a series with `reference`'s EXACT empirical distribution,
    reordered to match x's temporal rank order."""
    x = np.asarray(x, dtype=float)
    reference = np.asarray(reference, dtype=float)
    assert len(x) == len(reference)
    ranks = np.argsort(np.argsort(x))
    ref_sorted = np.sort(reference)
    return ref_sorted[ranks]


def estimate_spectral_exponent(x):
    """Periodogram-slope estimate of the spectral exponent (diagnostic
    only, confirms the PRE/POST spectral match claimed in the positive
    control, not part of the pipeline itself)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    spectrum = np.fft.rfft(x - x.mean())
    power = np.abs(spectrum) ** 2
    freqs = np.fft.rfftfreq(n)
    mask = freqs > 0
    slope, _ = np.polyfit(np.log(freqs[mask]), np.log(power[mask] + 1e-300), 1)
    return float(-slope)


def sine_clean(n, period, rng, dither_frac=1e-6):
    """Clean deterministic sine wave with a tiny relative dither -- a
    strongly periodic signal that should Takens-embed (m=3) as a clear
    closed loop in phase space, giving a large max-H1-persistence value.
    A tiny dither is included (standard practice, same reasoning already
    documented in rqa's/kramers_moyal's code-correctness diagnostics) to
    avoid any pathological floating-point-exact coincidences in the
    embedded point cloud; unlike RQA's FNN ratio criterion, ripser's Rips
    filtration does not have a near-zero-denominator failure mode, so this
    is precautionary rather than strictly required here."""
    t = np.arange(n)
    clean = np.sin(2 * np.pi * t / period)
    return clean + dither_frac * rng.standard_normal(n)


# --------------------------------------------------------------------------
# Reporting helpers
# --------------------------------------------------------------------------

def _pipeline_summary(result, extra=None):
    d = {"status": result["status"]}
    if result["status"] == "ok":
        d.update({
            "median_max_persistence_pre": result["median_max_persistence_pre"],
            "median_max_persistence_post": result["median_max_persistence_post"],
            "median_total_persistence_pre": result["median_total_persistence_pre"],
            "median_total_persistence_post": result["median_total_persistence_post"],
            "delta_median_max_persistence": result["delta_median_max_persistence"],
            "delta_median_total_persistence": result["delta_median_total_persistence"],
            "p_max_persistence": result["p_max_persistence"],
            "p_total_persistence": result["p_total_persistence"],
            "surrogate_max_persistence_mean": result["surrogate_max_persistence_mean"],
            "surrogate_max_persistence_std": result["surrogate_max_persistence_std"],
            "surrogate_max_persistence_n_valid": result["surrogate_max_persistence_n_valid"],
            "surrogate_max_persistence_n_undefined": result["surrogate_max_persistence_n_undefined"],
            "surrogate_total_persistence_mean": result["surrogate_total_persistence_mean"],
            "surrogate_total_persistence_std": result["surrogate_total_persistence_std"],
            "surrogate_total_persistence_n_valid": result["surrogate_total_persistence_n_valid"],
            "surrogate_total_persistence_n_undefined": result["surrogate_total_persistence_n_undefined"],
            "diagnostics": result["diagnostics"],
        })
    else:
        d.update({
            "real_pre_status": result["real_pre"]["status"],
            "real_post_status": result["real_post"]["status"],
            "real_pre_tau_info": (
                None if result["real_pre"].get("tau_info") is None else
                {k: v for k, v in result["real_pre"]["tau_info"].items() if k != "mi_curve"}
            ),
            "real_post_tau_info": (
                None if result["real_post"].get("tau_info") is None else
                {k: v for k, v in result["real_post"]["tau_info"].items() if k != "mi_curve"}
            ),
        })
    if extra:
        d.update(extra)
    return d


def sigma_equivalent(delta_real, surr_mean, surr_std):
    if delta_real is None or surr_mean is None or surr_std in (None, 0.0):
        return None
    return float((delta_real - surr_mean) / surr_std)


def main():
    t_start = time.time()
    results = {}

    # ---- 0. Embedding+Rips code-correctness diagnostic (NOT part of the
    # identifiability validation -- see module docstring) ----
    rng0 = np.random.default_rng(909)
    N_DIAG = 1000
    sine = sine_clean(N_DIAG, period=50, rng=rng0, dither_frac=1e-6)
    t0 = time.time()
    feat_diag = compute_ph_features(sine, m=M_FIXED)
    t_diag = time.time() - t0
    results["code_correctness_diagnostic"] = {
        "description": (
            "Clean, strongly periodic deterministic sine wave (period=50), "
            "N=1000, tiny (1e-6 relative) dither. A clean periodic signal "
            "should Takens-embed (m=3 FIXED) as a clear closed loop in "
            "phase space, giving a large, unambiguous max-H1-persistence "
            "value. NOT a PRE/POST identifiability test; exists only to "
            "confirm the embedding/sub-window/Rips/persistence-extraction "
            "code produces a sane result on unambiguous deterministic "
            "dynamics before testing on genuinely ambiguous stochastic data."
        ),
        "n_samples": N_DIAG,
        "tau": feat_diag.get("tau"),
        "tau_info": (
            None if feat_diag.get("tau_info") is None else
            {k: v for k, v in feat_diag["tau_info"].items() if k != "mi_curve"}
        ),
        "M_embedded_points": feat_diag.get("M"),
        "n_subwindows_used": feat_diag.get("n_subwindows_used"),
        "median_max_persistence": feat_diag.get("median_max_persistence"),
        "median_total_persistence": feat_diag.get("median_total_persistence"),
        "per_window_max_persistence": (
            None if feat_diag["status"] != "ok" else
            [w["max_persistence"] for w in feat_diag["per_window"]]
        ),
        "status": feat_diag["status"],
        "wall_clock_seconds": t_diag,
    }

    # ---- 1. Negative control: PRE, POST = two independent realizations of
    # the SAME linear process (fGn-like, fixed H=0.7) -- probes Gap (c)'s
    # named spectral/linear risk directly. ----
    N_CTRL = 3000
    rng_neg_pre = np.random.default_rng(555001)
    rng_neg_post = np.random.default_rng(555002)
    neg_pre = fgn_like(N_CTRL, H=0.7, rng=rng_neg_pre)
    neg_post = fgn_like(N_CTRL, H=0.7, rng=rng_neg_post)

    t0 = time.time()
    neg_result = run_ph_analysis(neg_pre, neg_post, seed=SEED)
    t_neg = time.time() - t0

    results["negative_control"] = _pipeline_summary(
        neg_result,
        extra={
            "description": (
                "PRE and POST = two INDEPENDENT realizations of the SAME "
                "linear process (fGn-like spectral-synthesis generator, "
                "fixed H=0.7, independent seeds 555001/555002). Probes "
                "METHODOLOGY_NOTE.md Gap (c)'s named spectral/linear risk "
                "directly: same autocorrelation structure, no genuine "
                "structural change -- p should typically be non-significant "
                "for both channels."
            ),
            "n_pre": N_CTRL, "n_post": N_CTRL,
            "wall_clock_seconds": t_neg,
        },
    )

    # ---- 2. Positive control -- THE central power test, EXACTLY per
    # METHODOLOGY_NOTE.md Gap (c): PRE = white Gaussian noise, POST =
    # logistic map (r=4) rank-remapped onto PRE. ----
    rng_pos = np.random.default_rng(424242)
    pos_pre = rng_pos.standard_normal(N_CTRL)
    logi_raw = logistic_map(N_CTRL, x0=0.234567891, r=4.0, burn_in=500)
    pos_post = rank_remap_to_reference(logi_raw, pos_pre)

    pos_spec_pre = estimate_spectral_exponent(pos_pre)
    pos_spec_post = estimate_spectral_exponent(pos_post)

    t0 = time.time()
    pos_result = run_ph_analysis(pos_pre, pos_post, seed=SEED)
    t_pos = time.time() - t0

    results["positive_control"] = _pipeline_summary(
        pos_result,
        extra={
            "description": (
                "PRE = iid Gaussian white noise (linear, zero "
                "autocorrelation). POST = logistic map (r=4, fully chaotic, "
                "genuine deterministic nonlinear process), rank-remapped "
                "onto PRE's own sorted values so PRE and POST share an "
                "EXACTLY identical empirical marginal by construction. "
                "Amplitude-spectrum match documented empirically via "
                "periodogram-slope spectral_exponent (both near-flat, as "
                "expected for two broadband processes). THIS IS THE "
                "DECISIVE TEST of METHODOLOGY_NOTE.md Gap (c)'s named "
                "r~=0.92 raw-correlation risk against RQA's %DET (which "
                "itself never showed IAAFT power, see ../../rqa/"
                "VALIDATION_NOTE.md) -- unlike RQA, this candidate's m=3 "
                "is FIXED (not FNN-estimated), so white noise does not "
                "block the embedding step here the way it blocked RQA's."
            ),
            "n_pre": N_CTRL, "n_post": N_CTRL,
            "spectral_exponent_pre": pos_spec_pre,
            "spectral_exponent_post": pos_spec_post,
            "marginal_match": "exact (rank-remap of POST onto PRE's sorted values)",
            "wall_clock_seconds": t_pos,
        },
    )

    # ---- 3. IAAFT power-check verdict, PER CHANNEL. ----
    pos = results["positive_control"]
    neg = results["negative_control"]

    pos_computable = pos["status"] == "ok"
    neg_computable = neg["status"] == "ok"

    if not pos_computable:
        max_verdict = "NOT_COMPUTABLE"
        total_verdict = "NOT_COMPUTABLE"
        sigma_max = sigma_total = None
        pos_p_max = pos_p_total = None
    else:
        pos_p_max, pos_p_total = pos["p_max_persistence"], pos["p_total_persistence"]
        sigma_max = sigma_equivalent(pos["delta_median_max_persistence"],
                                      pos["surrogate_max_persistence_mean"],
                                      pos["surrogate_max_persistence_std"])
        sigma_total = sigma_equivalent(pos["delta_median_total_persistence"],
                                        pos["surrogate_total_persistence_mean"],
                                        pos["surrogate_total_persistence_std"])
        max_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_max is not None and pos_p_max < 0.05) else "IAAFT_LOW_POWER"
        total_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_total is not None and pos_p_total < 0.05) else "IAAFT_LOW_POWER"

    neg_p_max = neg.get("p_max_persistence")
    neg_p_total = neg.get("p_total_persistence")
    neg_nonsig_max = neg_computable and (neg_p_max is None or neg_p_max >= 0.05)
    neg_nonsig_total = neg_computable and (neg_p_total is None or neg_p_total >= 0.05)

    results["iaaft_power_check"] = {
        "max_persistence_channel": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_positive": pos_p_max if pos_computable else None,
            "p_negative": neg_p_max,
            "sigma_equivalent_positive": sigma_max,
            "correctly_nonsignificant_negative": neg_nonsig_max,
            "verdict": max_verdict,
        },
        "total_persistence_channel": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_positive": pos_p_total if pos_computable else None,
            "p_negative": neg_p_total,
            "sigma_equivalent_positive": sigma_total,
            "correctly_nonsignificant_negative": neg_nonsig_total,
            "verdict": total_verdict,
        },
        "central_identifiability_question": (
            "METHODOLOGY_NOTE.md Gap (c) names a risk ALREADY MEASURED "
            "empirically in Phase 0.6 (noisy sinusoid, 9 noise levels): "
            "max-H1-persistence correlated with an RQA-%DET analog at "
            "r~=0.92 in the structure-degradation regime most relevant to "
            "detecting a transition. RQA's %DET itself NEVER showed real "
            "IAAFT power (p=1.0 both channels, best-case Roessler "
            "redesign, ../../rqa/VALIDATION_NOTE.md). The verdicts above "
            "answer directly whether persistent homology inherits that "
            "same lack of power despite the raw correlation, or carries "
            "power %DET never demonstrated."
        ),
    }

    # ---- 4. Moving-block bootstrap fallback (Kunsch 1989), exercised on
    # ANY channel that shows IAAFT_LOW_POWER on the positive control,
    # exactly as pre-authorized in METHODOLOGY_NOTE.md Gap (c). ----
    bootstrap_results = {}
    if pos_computable:
        needs_bootstrap = []
        if max_verdict == "IAAFT_LOW_POWER":
            needs_bootstrap.append("max_persistence")
        if total_verdict == "IAAFT_LOW_POWER":
            needs_bootstrap.append("total_persistence")

        if needs_bootstrap:
            t0 = time.time()
            boot = run_block_bootstrap_test(
                pos_pre, pos_post,
                real_pre=pos_result["real_pre"], real_post=pos_result["real_post"],
                n_bootstrap=1000, seed=SEED, m=M_FIXED, n_window=N_WINDOW,
                k_max=K_SUBWINDOWS_MAX,
            )
            t_boot = time.time() - t0
            boot["wall_clock_seconds"] = t_boot
            boot["channels_triggered_by_low_iaaft_power"] = needs_bootstrap
            bootstrap_results = boot

    results["bootstrap_fallback"] = bootstrap_results if bootstrap_results else {
        "triggered": False,
        "reason": "Not needed -- at least one channel already showed IAAFT_HAS_REAL_POWER, "
                  "or the positive control was not computable at all.",
    }
    if bootstrap_results:
        bootstrap_results["triggered"] = True

    results["pipeline_config"] = (
        pos_result["config"] if pos_result["status"] == "ok" else neg_result["config"]
    )
    results["generator_notes"] = {
        "colored_noise_fgn_like": (
            "FFT-filtering spectral synthesis: white Gaussian noise scaled "
            "per-frequency by f^(-exponent/2), inverse-transformed, "
            "z-scored. fGn-like approximation via exponent=2H+1 (spectral "
            "relation for fractional Gaussian noise); same technique used "
            "throughout this line, independent implementation."
        ),
        "logistic_map": "x_{k+1} = 4*x_k*(1-x_k), burn_in=500 discarded transient iterations.",
        "rank_remap": (
            "POST = sorted(PRE)[argsort(argsort(logistic_map_raw))] -- POST "
            "is an exact permutation of PRE's own values, reordered by the "
            "logistic map's temporal rank structure."
        ),
        "sine_clean": (
            "Deterministic sine wave (period 50) plus a tiny 1e-6-relative "
            "Gaussian dither, used ONLY for the embedding/Rips code-"
            "correctness diagnostic (check 0), not a PRE/POST "
            "identifiability control."
        ),
    }
    results["wall_clock_seconds_total"] = time.time() - t_start

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results["iaaft_power_check"], indent=2))
    print(json.dumps({"bootstrap_triggered": results["bootstrap_fallback"].get("triggered", False)}, indent=2))
    print(f"\nWrote {out_path}")
    print(f"Total wall clock: {results['wall_clock_seconds_total']:.1f}s")
    print(f"Single full run_ph_analysis wall clock (positive control, N={N_CTRL}, "
          f"N_SURROGATES={N_SURROGATES}): {t_pos:.1f}s")


if __name__ == "__main__":
    main()
