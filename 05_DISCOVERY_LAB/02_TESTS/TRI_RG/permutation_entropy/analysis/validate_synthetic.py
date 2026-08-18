"""
Synthetic validation of `pe_common.py`, run and committed BEFORE any real
PRE/POST segment (VitalDB EEG anesthesia induction, PhysioNet European
ST-T Database transient ischemia) is touched -- required by
METHODOLOGY_NOTE.md Gap (b): the central, genuinely novel empirical
question of this candidate is whether IAAFT surrogates have real power
against `C_JS`/`MCI` (Rosso et al. 2007's statistical complexity, built
specifically to separate stochastic linear noise from deterministic
chaos) and/or `H_S`/`PCI` (which Zunino et al. 2008 shows is at risk of
being a reparametrization of the Hurst exponent, already closed negative
6x in this line under other names -- DFA-alpha, wavelet h(2), etc.).

Checks, all synthetic, all seeded for reproducibility:

0. Code-correctness diagnostic (NOT part of the identifiability
   validation itself, reported separately): a clean deterministic sine
   wave. On a smooth periodic curve, 4-point windows are overwhelmingly
   monotonic (increasing or decreasing), so the ordinal-pattern
   distribution should be strongly concentrated on just 2 of the 24
   possible patterns -- low H_S, hand-verifiable. This confirms the
   Bandt-Pompe embedding + Lehmer-code counting + H_S/C_JS formulas are
   implemented correctly before testing on genuinely ambiguous
   stochastic data.

1. Positive control -- the central identifiability test for this
   candidate, EXACTLY as specified in METHODOLOGY_NOTE.md Gap (b): PRE =
   white Gaussian noise. POST = logistic map (r=4, fully chaotic) rank-
   remapped onto PRE's own exact empirical distribution (same technique
   already validated in mse_multiscale_entropy/ and rqa/'s
   validate_synthetic.py) so PRE and POST share an EXACTLY identical
   marginal and (both being near-broadband processes) closely matched
   spectra. Unlike RQA, the Bandt-Pompe ordinal-pattern embedding does
   NOT require FNN/Takens embedding-dimension resolution -- it is a
   direct combinatorial statistic on delay vectors, always computable
   for any N>=m -- so METHODOLOGY_NOTE.md's a priori expectation is that
   no structural non-computability wall analogous to RQA's white-noise
   FNN failure should appear here. This is checked explicitly below, not
   assumed.

2. Negative control: PRE and POST = two INDEPENDENT realizations of the
   SAME linear process (fGn-like, fixed H=0.7, independent seeds) --
   probes Gap (b)'s named spectral/linear risk (Zunino et al. 2008)
   directly: same H, no genuine structural change, p should typically be
   non-significant for both channels under IAAFT.

3. IAAFT power-check verdict, reported PER CHANNEL (H_S/PCI and
   C_JS/MCI separately) -- the central, honestly-reported empirical
   answer to METHODOLOGY_NOTE.md's a priori hypothesis that C_JS/MCI
   shows real power (like MSE's CI) while H_S/PCI may not (like
   DFA-alpha).

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_common import (
    run_pe_analysis, compute_pe, pattern_distribution, normalized_shannon_entropy,
    statistical_complexity, N_SURROGATES, N_IAAFT_ITER, SEED, M_EMBED, N_STATES, Q0,
)


# --------------------------------------------------------------------------
# Synthetic generators (independent implementation for this test line, same
# spirit/technique as mse_multiscale_entropy's / rqa's validate_synthetic.py
# but not imported from them)
# --------------------------------------------------------------------------

def colored_noise(n, spectral_exponent, rng):
    """Gaussian colored noise, PSD ~ 1/f^exponent, FFT-filtering spectral
    synthesis. exponent=0 ~ white noise. Used here as an fGn-like
    generator: an fGn of Hurst exponent H has PSD ~ f^-(2H+1), so
    exponent=2H+1 approximates fGn with that H (same technique as
    mse_multiscale_entropy's / rqa's validate_synthetic.py, not a literal
    Davies-Harte exact-covariance fGn generator)."""
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


# --------------------------------------------------------------------------
# Reporting helpers
# --------------------------------------------------------------------------

def _pipeline_summary(result, extra=None):
    d = {"status": result["status"]}
    if result["status"] == "ok":
        d.update({
            "PCI_pre": result["PCI_pre"], "PCI_post": result["PCI_post"],
            "MCI_pre": result["MCI_pre"], "MCI_post": result["MCI_post"],
            "delta_PCI": result["delta_PCI"], "delta_MCI": result["delta_MCI"],
            "p_PCI": result["p_PCI"], "p_MCI": result["p_MCI"],
            "surrogate_PCI_mean": result["surrogate_PCI_mean"],
            "surrogate_PCI_std": result["surrogate_PCI_std"],
            "surrogate_PCI_n_valid": result["surrogate_PCI_n_valid"],
            "surrogate_PCI_n_undefined": result["surrogate_PCI_n_undefined"],
            "surrogate_MCI_mean": result["surrogate_MCI_mean"],
            "surrogate_MCI_std": result["surrogate_MCI_std"],
            "surrogate_MCI_n_valid": result["surrogate_MCI_n_valid"],
            "surrogate_MCI_n_undefined": result["surrogate_MCI_n_undefined"],
            "n_scales_pre": result["real_pre"]["n_scales_achieved"],
            "n_scales_post": result["real_post"]["n_scales_achieved"],
            "scales_used_pre": result["real_pre"]["scales_used"],
            "scales_used_post": result["real_post"]["scales_used"],
            "n_samples_used_pre": result["real_pre"]["n_samples_used"],
            "n_samples_used_post": result["real_post"]["n_samples_used"],
        })
    else:
        d.update({
            "real_pre_diag": {k: v for k, v in result["real_pre"].items()
                               if k not in ("H_S_values", "C_JS_values")},
            "real_post_diag": {k: v for k, v in result["real_post"].items()
                                if k not in ("H_S_values", "C_JS_values")},
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

    # ---- 0. Code-correctness diagnostic (NOT part of the identifiability
    # validation -- see module docstring). Clean deterministic sine wave,
    # single scale (s=1), checked directly against pattern_distribution
    # rather than through the full multiscale sum, so the hand-verifiable
    # claim ("mostly monotonic 4-point windows -> low H_S, concentrated on
    # 2 of 24 patterns") is checked exactly, not diluted by coarse-graining
    # artifacts at other scales. ----
    N_DIAG = 1000
    period = 50
    t = np.arange(N_DIAG)
    sine = np.sin(2 * np.pi * t / period)
    P_diag, n_windows_diag = pattern_distribution(sine, m=M_EMBED, tau=1)
    H_S_diag = normalized_shannon_entropy(P_diag)
    C_JS_diag = statistical_complexity(P_diag, H_S=H_S_diag)
    top_patterns = sorted(
        [(int(i), float(p)) for i, p in enumerate(P_diag) if p > 0],
        key=lambda kv: -kv[1],
    )
    results["code_correctness_diagnostic"] = {
        "description": (
            "Deterministic sine wave (period=50), N=1000, m=4, tau_BP=1, "
            "single scale s=1 (no coarse-graining). NOT a PRE/POST "
            "identifiability test; exists only to confirm the Bandt-Pompe "
            "embedding + Lehmer-code pattern counting + H_S/C_JS formulas "
            "are implemented correctly before testing on genuinely "
            "ambiguous stochastic data. Expectation (hand-verifiable): a "
            "smooth periodic curve is overwhelmingly monotonic across any "
            "4 consecutive samples except near its 2 extrema per cycle, so "
            "the ordinal-pattern distribution should concentrate on ~2 of "
            "the 24 possible patterns (monotonic increasing / monotonic "
            "decreasing), giving LOW H_S."
        ),
        "n_samples": N_DIAG, "period": period, "m": M_EMBED,
        "n_windows": n_windows_diag,
        "n_states": N_STATES,
        "n_patterns_observed": int(np.sum(P_diag > 0)),
        "top_patterns_by_probability": top_patterns[:5],
        "H_S": H_S_diag,
        "C_JS": C_JS_diag,
        "verdict": (
            "CODE_CORRECT_LOW_H_S_AS_EXPECTED"
            if (H_S_diag < 0.6 and top_patterns[0][1] > 0.3)
            else "UNEXPECTED_HIGH_ENTROPY_CHECK_IMPLEMENTATION"
        ),
    }

    # ---- 1. Positive control: PRE = white Gaussian noise, POST = logistic
    # map (r=4) rank-remapped onto PRE's exact marginal -- EXACT
    # METHODOLOGY_NOTE.md Gap (b) specification. ----
    N_CTRL = 3000
    rng_pos = np.random.default_rng(424242)
    pos_pre = rng_pos.standard_normal(N_CTRL)
    logi_raw = logistic_map(N_CTRL, x0=0.234567891, r=4.0, burn_in=500)
    pos_post = rank_remap_to_reference(logi_raw, pos_pre)

    pos_spec_pre = estimate_spectral_exponent(pos_pre)
    pos_spec_post = estimate_spectral_exponent(pos_post)

    t0 = time.time()
    pos_result = run_pe_analysis(pos_pre, pos_post, seed=SEED)
    t_pos = time.time() - t0

    results["positive_control"] = _pipeline_summary(
        pos_result,
        extra={
            "description": (
                "PRE = iid Gaussian white noise (linear, zero "
                "autocorrelation). POST = logistic map (r=4, fully "
                "chaotic, genuine deterministic nonlinear process), "
                "rank-remapped onto PRE's own sorted values so PRE and "
                "POST share an EXACTLY identical empirical marginal by "
                "construction. Amplitude-spectrum match documented "
                "empirically via periodogram-slope spectral_exponent "
                "(both expected near-flat, two broadband processes)."
            ),
            "n_pre": N_CTRL, "n_post": N_CTRL,
            "spectral_exponent_pre": pos_spec_pre,
            "spectral_exponent_post": pos_spec_post,
            "marginal_match": "exact (rank-remap of POST onto PRE's sorted values)",
            "wall_clock_seconds": t_pos,
        },
    )

    # ---- 2. Negative control: PRE, POST = two independent realizations of
    # the SAME linear process (fGn-like, fixed H=0.7) -- probes Gap (b)'s
    # named spectral/linear risk (Zunino et al. 2008) directly. ----
    N_NEG = N_CTRL
    rng_neg_pre = np.random.default_rng(555001)
    rng_neg_post = np.random.default_rng(555002)
    neg_pre = fgn_like(N_NEG, H=0.7, rng=rng_neg_pre)
    neg_post = fgn_like(N_NEG, H=0.7, rng=rng_neg_post)

    t0 = time.time()
    neg_result = run_pe_analysis(neg_pre, neg_post, seed=SEED)
    t_neg = time.time() - t0

    results["negative_control"] = _pipeline_summary(
        neg_result,
        extra={
            "description": (
                "PRE and POST = two INDEPENDENT realizations of the SAME "
                "linear process (fGn-like spectral-synthesis generator, "
                "fixed H=0.7, independent seeds 555001/555002). Probes "
                "METHODOLOGY_NOTE.md Gap (b)'s named spectral/linear risk "
                "(Zunino et al. 2008: H_S ~ near-monotone function of "
                "Hurst H) directly: same H, no genuine structural change "
                "-- p should typically be non-significant for both "
                "channels if IAAFT is correctly calibrated under the null."
            ),
            "n_pre": N_NEG, "n_post": N_NEG,
            "wall_clock_seconds": t_neg,
        },
    )

    # ---- 3. IAAFT power-check verdict, PER CHANNEL -- the central,
    # honestly-reported empirical answer to METHODOLOGY_NOTE.md's a priori
    # hypothesis (C_JS/MCI shows power like MSE's CI; H_S/PCI may not, like
    # DFA-alpha). ----
    pos = results["positive_control"]
    neg = results["negative_control"]

    pos_computable = pos["status"] == "ok"
    neg_computable = neg["status"] == "ok"

    if not pos_computable:
        pci_verdict = "NOT_COMPUTABLE"
        mci_verdict = "NOT_COMPUTABLE"
        sigma_PCI = sigma_MCI = None
        pos_p_PCI = pos_p_MCI = None
    else:
        pos_p_PCI, pos_p_MCI = pos["p_PCI"], pos["p_MCI"]
        sigma_PCI = sigma_equivalent(pos["delta_PCI"], pos["surrogate_PCI_mean"], pos["surrogate_PCI_std"])
        sigma_MCI = sigma_equivalent(pos["delta_MCI"], pos["surrogate_MCI_mean"], pos["surrogate_MCI_std"])
        pci_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_PCI is not None and pos_p_PCI < 0.05) else "IAAFT_LOW_POWER"
        mci_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_MCI is not None and pos_p_MCI < 0.05) else "IAAFT_LOW_POWER"

    neg_p_PCI = neg.get("p_PCI")
    neg_p_MCI = neg.get("p_MCI")
    neg_nonsig_PCI = neg_computable and (neg_p_PCI is None or neg_p_PCI >= 0.05)
    neg_nonsig_MCI = neg_computable and (neg_p_MCI is None or neg_p_MCI >= 0.05)

    results["iaaft_power_check"] = {
        "PCI_channel_H_S": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_PCI_positive": pos_p_PCI if pos_computable else None,
            "p_PCI_negative": neg_p_PCI,
            "sigma_equivalent_positive": sigma_PCI,
            "correctly_nonsignificant_negative": neg_nonsig_PCI,
            "verdict": pci_verdict,
        },
        "MCI_channel_C_JS": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_MCI_positive": pos_p_MCI if pos_computable else None,
            "p_MCI_negative": neg_p_MCI,
            "sigma_equivalent_positive": sigma_MCI,
            "correctly_nonsignificant_negative": neg_nonsig_MCI,
            "verdict": mci_verdict,
        },
        "overall_note": (
            "Unlike RQA (shared embedding step upstream of BOTH channels), "
            "the Bandt-Pompe ordinal-pattern embedding needs no "
            "resolution step -- H_S and C_JS are computed independently "
            "per scale from the same empirical pattern distribution P(s), "
            "so a low-power finding for one channel does not imply the "
            "other is uncomputable; each channel's verdict is reported on "
            "its own merits."
        ),
    }

    a_priori_hypothesis_confirmed = (
        pos_computable and mci_verdict == "IAAFT_HAS_REAL_POWER"
        and pci_verdict == "IAAFT_LOW_POWER"
    )
    results["a_priori_hypothesis_check"] = {
        "hypothesis": (
            "METHODOLOGY_NOTE.md Gap (b): C_JS/MCI (built by Rosso et al. "
            "2007 specifically to separate linear stochastic noise from "
            "deterministic chaos) shows real IAAFT power (like MSE's CI); "
            "H_S/PCI (at risk per Zunino et al. 2008 of reparametrizing "
            "the Hurst exponent, already closed negative 6x in this line) "
            "may not (like DFA-alpha)."
        ),
        "PCI_verdict": pci_verdict,
        "MCI_verdict": mci_verdict,
        "pattern_observed": (
            "HYPOTHESIS_CONFIRMED_MCI_POWER_PCI_NO_POWER" if a_priori_hypothesis_confirmed else
            "BOTH_CHANNELS_SHOW_POWER" if (pci_verdict == "IAAFT_HAS_REAL_POWER" and mci_verdict == "IAAFT_HAS_REAL_POWER") else
            "NEITHER_CHANNEL_SHOWS_POWER" if (pci_verdict == "IAAFT_LOW_POWER" and mci_verdict == "IAAFT_LOW_POWER") else
            "OPPOSITE_PATTERN_PCI_POWER_MCI_NO_POWER" if (pci_verdict == "IAAFT_HAS_REAL_POWER" and mci_verdict == "IAAFT_LOW_POWER") else
            "NOT_COMPUTABLE_OR_INDETERMINATE"
        ),
    }

    results["pipeline_config"] = pos_result["config"]
    results["generator_notes"] = {
        "colored_noise_fgn_like": (
            "FFT-filtering spectral synthesis: white Gaussian noise scaled "
            "per-frequency by f^(-exponent/2), inverse-transformed, "
            "z-scored. fGn-like approximation via exponent=2H+1 (spectral "
            "relation for fractional Gaussian noise); same technique as "
            "mse_multiscale_entropy/rqa validate_synthetic.py, independent "
            "implementation."
        ),
        "logistic_map": "x_{k+1} = 4*x_k*(1-x_k), burn_in=500 discarded transient iterations.",
        "rank_remap": (
            "POST = sorted(PRE)[argsort(argsort(logistic_map_raw))] -- "
            "POST is an exact permutation of PRE's own values, reordered "
            "by the logistic map's temporal rank structure."
        ),
        "sine_diagnostic": (
            "Plain deterministic sine wave (period 50), used ONLY for the "
            "code-correctness diagnostic (check 0), not a PRE/POST "
            "identifiability control. No dither was needed here (unlike "
            "RQA's FNN-based diagnostic) because ordinal-pattern ranking "
            "via stable-sort tie-breaking is well-defined even for exact "
            "ties, and floating-point sine samples essentially never tie "
            "exactly in practice at N=1000/period=50."
        ),
    }
    results["wall_clock_seconds_total"] = time.time() - t_start

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results["code_correctness_diagnostic"], indent=2, default=str))
    print(json.dumps(results["iaaft_power_check"], indent=2))
    print(json.dumps(results["a_priori_hypothesis_check"], indent=2))
    print(f"\nWrote {out_path}")
    print(f"Total wall clock: {results['wall_clock_seconds_total']:.1f}s")


if __name__ == "__main__":
    main()
