"""
Synthetic validation of `lzc_common.py`, run and committed BEFORE any real
PRE/POST segment (Daphnet Freezing-of-Gait, Kilauea 2018 LERZ seismicity)
is touched -- required by METHODOLOGY_NOTE.md: the central, genuinely
novel empirical question of this candidate is whether IAAFT surrogates
have real power against LZC_median and/or LZC_ternary, given that no
published work has run IAAFT against LZC specifically.

Checks, all synthetic, all seeded for reproducibility:

0. Code-correctness diagnostic (NOT part of the identifiability
   validation itself, reported separately): the LZ76 parse count is
   checked against the exact worked example from Kaspar & Schuster 1987
   itself (binary string "1001111011000010", expected c(n)=6) -- a
   hand-verifiable ground truth, confirming the LZ76 greedy-parsing
   implementation is correct before testing on genuinely ambiguous
   stochastic data. A second sanity diagnostic (constant string vs.
   alternating string vs. iid random) confirms LZC behaves monotonically
   as expected (low for constant/periodic, near 1 for iid random binary).

1. Positive control -- the central identifiability test for this
   candidate: PRE = white Gaussian noise. POST = logistic map (r=4,
   fully chaotic) rank-remapped onto PRE's own exact empirical
   distribution (same technique already validated in
   mse_multiscale_entropy/, permutation_entropy/, and rqa/'s
   validate_synthetic.py) so PRE and POST share an EXACTLY identical
   marginal and (both being near-broadband processes) closely matched
   spectra. Unlike RQA, R_lambda here (median/tertile threshold) does
   NOT require FNN/Takens embedding-dimension resolution -- it is a
   direct pointwise rule, always computable for any N>=MIN_N_SEGMENT --
   so METHODOLOGY_NOTE.md's a priori expectation is that no structural
   non-computability wall analogous to RQA's white-noise FNN failure
   should appear here. Checked explicitly below, not assumed.

2. Negative control: PRE and POST = two INDEPENDENT realizations of the
   SAME linear process (fGn-like, fixed H=0.7, independent seeds) --
   probes the named spectral/Hurst-family redundancy risk (Ziv & Lempel
   1978 asymptotic entropy-rate target, shared with CI/beta of MSE,
   already closed negative) directly: same H, no genuine structural
   change, p should typically be non-significant for both channels under
   IAAFT.

3. IAAFT power-check verdict, reported PER CHANNEL (LZC_median and
   LZC_ternary separately) -- the central, honestly-reported empirical
   answer to whether this candidate survives its own falsification test.

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lzc_common import (
    run_lzc_analysis, compute_lzc_channels, lz76_complexity, lz76_complexity_naive,
    median_binarize, ternary_quantize, run_block_bootstrap_test, N_SURROGATES,
    N_IAAFT_ITER, SEED, MIN_N_SEGMENT,
)


# --------------------------------------------------------------------------
# Synthetic generators (independent implementation for this test line, same
# spirit/technique as other candidates' validate_synthetic.py but not
# imported from them)
# --------------------------------------------------------------------------

def colored_noise(n, spectral_exponent, rng):
    """Gaussian colored noise, PSD ~ 1/f^exponent, FFT-filtering spectral
    synthesis. exponent=0 ~ white noise. Used here as an fGn-like
    generator: an fGn of Hurst exponent H has PSD ~ f^-(2H+1), so
    exponent=2H+1 approximates fGn with that H (same technique as
    other validate_synthetic.py scripts in this lab, not a literal
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
            "LZC_median_pre": result["LZC_median_pre"], "LZC_median_post": result["LZC_median_post"],
            "LZC_ternary_pre": result["LZC_ternary_pre"], "LZC_ternary_post": result["LZC_ternary_post"],
            "delta_LZC_median": result["delta_LZC_median"], "delta_LZC_ternary": result["delta_LZC_ternary"],
            "p_LZC_median": result["p_LZC_median"], "p_LZC_ternary": result["p_LZC_ternary"],
            "surrogate_LZC_median_mean": result["surrogate_LZC_median_mean"],
            "surrogate_LZC_median_std": result["surrogate_LZC_median_std"],
            "surrogate_LZC_median_n_valid": result["surrogate_LZC_median_n_valid"],
            "surrogate_LZC_median_n_undefined": result["surrogate_LZC_median_n_undefined"],
            "surrogate_LZC_ternary_mean": result["surrogate_LZC_ternary_mean"],
            "surrogate_LZC_ternary_std": result["surrogate_LZC_ternary_std"],
            "surrogate_LZC_ternary_n_valid": result["surrogate_LZC_ternary_n_valid"],
            "surrogate_LZC_ternary_n_undefined": result["surrogate_LZC_ternary_n_undefined"],
            "n_samples_used_pre": result["real_pre"]["n_samples_used"],
            "n_samples_used_post": result["real_post"]["n_samples_used"],
        })
    else:
        d.update({"real_pre_diag": result["real_pre"], "real_post_diag": result["real_post"]})
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
    # validation -- see module docstring). Kaspar & Schuster 1987's own
    # worked example, plus a monotonicity sanity check (constant <
    # alternating < random). ----
    ks_example = [1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]
    ks_c = lz76_complexity(ks_example)
    ks_c_naive = lz76_complexity_naive(ks_example)

    rng_diag = np.random.default_rng(11)
    const_seq = [0] * 500
    alt_seq = ([0, 1] * 250)
    rand_seq = rng_diag.integers(0, 2, 500).tolist()
    c_const = lz76_complexity(const_seq)
    c_alt = lz76_complexity(alt_seq)
    c_rand = lz76_complexity(rand_seq)
    c_const_naive = lz76_complexity_naive(const_seq)
    c_alt_naive = lz76_complexity_naive(alt_seq)
    c_rand_naive = lz76_complexity_naive(rand_seq)
    fast_vs_naive_match = (
        ks_c == ks_c_naive and c_const == c_const_naive
        and c_alt == c_alt_naive and c_rand == c_rand_naive
    )

    results["code_correctness_diagnostic"] = {
        "description": (
            "Two checks, PLUS a fast-vs-naive cross-validation. (1) Kaspar "
            "& Schuster 1987's own worked example: binary string "
            "'1001111011000010' (16 symbols) has a documented, hand-"
            "verifiable raw LZ76 parse count c(n)=6. (2) Monotonicity "
            "sanity check on N=500 binary sequences: constant < "
            "alternating-periodic < iid random, expected because LZ76 "
            "finds new phrases fastest in less structured sequences. (3) "
            "`lz76_complexity` (the fast, O(n log n) suffix-array-based "
            "implementation actually used by this pipeline, added after a "
            "real-data performance defect was found in the naive nested-"
            "loop version -- see lzc_common.py module docstring) is cross-"
            "checked here against `lz76_complexity_naive` (the original "
            "slow-but-trusted reference) on all 4 sequences above; the "
            "full validation of this fix (500 random + 300 structured "
            "small-N sequences, plus exact real-data-scale N tests up to "
            "200,000) was run separately before this fix was integrated, "
            "documented in VALIDATION_NOTE.md."
        ),
        "kaspar_schuster_worked_example": ks_example,
        "kaspar_schuster_expected_c": 6,
        "kaspar_schuster_computed_c": ks_c,
        "kaspar_schuster_computed_c_naive_reference": ks_c_naive,
        "kaspar_schuster_match": (ks_c == 6),
        "c_n_constant_N500": c_const,
        "c_n_alternating_N500": c_alt,
        "c_n_random_N500": c_rand,
        "c_n_constant_N500_naive_reference": c_const_naive,
        "c_n_alternating_N500_naive_reference": c_alt_naive,
        "c_n_random_N500_naive_reference": c_rand_naive,
        "fast_vs_naive_reference_match": fast_vs_naive_match,
        "monotonicity_as_expected": bool(c_const < c_alt < c_rand),
        "verdict": (
            "CODE_CORRECT"
            if (ks_c == 6 and c_const < c_alt < c_rand and fast_vs_naive_match)
            else "IMPLEMENTATION_ERROR_CHECK_LZ76"
        ),
    }
    if ks_c != 6 or not fast_vs_naive_match:
        print("FATAL: LZ76 implementation does not match the Kaspar & Schuster "
              "1987 worked example and/or the naive reference implementation "
              "(expected c=6, got %d; fast_vs_naive_match=%s). Aborting before "
              "any further validation." % (ks_c, fast_vs_naive_match))
        sys.exit(1)

    # ---- 1. Positive control: PRE = white Gaussian noise, POST = logistic
    # map (r=4) rank-remapped onto PRE's exact marginal. ----
    N_CTRL = 3000
    rng_pos = np.random.default_rng(424242)
    pos_pre = rng_pos.standard_normal(N_CTRL)
    logi_raw = logistic_map(N_CTRL, x0=0.234567891, r=4.0, burn_in=500)
    pos_post = rank_remap_to_reference(logi_raw, pos_pre)

    pos_spec_pre = estimate_spectral_exponent(pos_pre)
    pos_spec_post = estimate_spectral_exponent(pos_post)

    t0 = time.time()
    pos_result = run_lzc_analysis(pos_pre, pos_post, seed=SEED)
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
    # the SAME linear process (fGn-like, fixed H=0.7). ----
    N_NEG = N_CTRL
    rng_neg_pre = np.random.default_rng(555001)
    rng_neg_post = np.random.default_rng(555002)
    neg_pre = fgn_like(N_NEG, H=0.7, rng=rng_neg_pre)
    neg_post = fgn_like(N_NEG, H=0.7, rng=rng_neg_post)

    t0 = time.time()
    neg_result = run_lzc_analysis(neg_pre, neg_post, seed=SEED)
    t_neg = time.time() - t0

    results["negative_control"] = _pipeline_summary(
        neg_result,
        extra={
            "description": (
                "PRE and POST = two INDEPENDENT realizations of the SAME "
                "linear process (fGn-like spectral-synthesis generator, "
                "fixed H=0.7, independent seeds 555001/555002). Probes "
                "the Ziv & Lempel 1978 asymptotic entropy-rate redundancy "
                "risk (same H, no genuine structural change) -- p should "
                "typically be non-significant for both channels if IAAFT "
                "is correctly calibrated under the null."
            ),
            "n_pre": N_NEG, "n_post": N_NEG,
            "wall_clock_seconds": t_neg,
        },
    )

    # ---- 2b. Differential-Hurst-only control (same discipline already
    # used in permutation_entropy/validate_synthetic.py): PRE = fGn-like
    # H=0.3, POST = fGn-like H=0.9, independent seeds, BOTH purely linear
    # Gaussian self-similar processes with NO nonlinear/deterministic
    # structure -- only a genuine Hurst-exponent shift. Tests directly
    # whether LZC shows spurious IAAFT significance from a pure linear
    # spectral (Hurst) shift alone. ----
    N_HURST = N_CTRL
    rng_hurst_pre = np.random.default_rng(777001)
    rng_hurst_post = np.random.default_rng(777002)
    H_LOW, H_HIGH = 0.3, 0.9
    hurst_pre = fgn_like(N_HURST, H=H_LOW, rng=rng_hurst_pre)
    hurst_post = fgn_like(N_HURST, H=H_HIGH, rng=rng_hurst_post)

    hurst_spec_pre = estimate_spectral_exponent(hurst_pre)
    hurst_spec_post = estimate_spectral_exponent(hurst_post)

    t0 = time.time()
    hurst_result = run_lzc_analysis(hurst_pre, hurst_post, seed=SEED)
    t_hurst = time.time() - t0

    results["differential_hurst_control"] = _pipeline_summary(
        hurst_result,
        extra={
            "description": (
                "PRE = fGn-like H=0.3 (weakly persistent), POST = fGn-"
                "like H=0.9 (strongly persistent), independent seeds "
                "777001/777002. BOTH are purely LINEAR Gaussian self-"
                "similar processes -- no nonlinear or deterministic "
                "structure of any kind, only a genuine Hurst-exponent "
                "shift. Tests whether LZC_median/LZC_ternary show "
                "artificial/spurious IAAFT significance purely from a "
                "linear spectral (Hurst) shift with no genuine complexity "
                "change -- the Ziv & Lempel 1978 asymptotic redundancy "
                "risk, which the same-H negative control above cannot "
                "probe (no H shift there to begin with)."
            ),
            "H_pre": H_LOW, "H_post": H_HIGH,
            "n_pre": N_HURST, "n_post": N_HURST,
            "spectral_exponent_pre": hurst_spec_pre,
            "spectral_exponent_post": hurst_spec_post,
            "spectral_exponent_target_pre_2H+1": 2 * H_LOW + 1,
            "spectral_exponent_target_post_2H+1": 2 * H_HIGH + 1,
            "wall_clock_seconds": t_hurst,
        },
    )

    hurst_computable = results["differential_hurst_control"]["status"] == "ok"
    if hurst_computable:
        hurst_p_med = results["differential_hurst_control"]["p_LZC_median"]
        hurst_p_tern = results["differential_hurst_control"]["p_LZC_ternary"]
        hurst_sigma_med = sigma_equivalent(
            results["differential_hurst_control"]["delta_LZC_median"],
            results["differential_hurst_control"]["surrogate_LZC_median_mean"],
            results["differential_hurst_control"]["surrogate_LZC_median_std"],
        )
        hurst_sigma_tern = sigma_equivalent(
            results["differential_hurst_control"]["delta_LZC_ternary"],
            results["differential_hurst_control"]["surrogate_LZC_ternary_mean"],
            results["differential_hurst_control"]["surrogate_LZC_ternary_std"],
        )
        med_spurious = hurst_p_med is not None and hurst_p_med < 0.05
        tern_spurious = hurst_p_tern is not None and hurst_p_tern < 0.05
    else:
        hurst_p_med = hurst_p_tern = hurst_sigma_med = hurst_sigma_tern = None
        med_spurious = tern_spurious = None

    results["differential_hurst_control_verdict"] = {
        "description": (
            "Mechanical read of the differential_hurst_control result "
            "above: does a PURE linear Hurst shift (H=0.3 -> H=0.9, no "
            "nonlinear content) produce spurious IAAFT significance on "
            "either channel?"
        ),
        "computable": hurst_computable,
        "p_LZC_median": hurst_p_med, "sigma_equivalent_LZC_median": hurst_sigma_med,
        "LZC_median_shows_spurious_significance": med_spurious,
        "p_LZC_ternary": hurst_p_tern, "sigma_equivalent_LZC_ternary": hurst_sigma_tern,
        "LZC_ternary_shows_spurious_significance": tern_spurious,
    }

    # ---- 3. IAAFT power-check verdict, PER CHANNEL. ----
    pos = results["positive_control"]
    neg = results["negative_control"]

    pos_computable = pos["status"] == "ok"
    neg_computable = neg["status"] == "ok"

    if not pos_computable:
        med_verdict = "NOT_COMPUTABLE"
        tern_verdict = "NOT_COMPUTABLE"
        sigma_med = sigma_tern = None
        pos_p_med = pos_p_tern = None
    else:
        pos_p_med, pos_p_tern = pos["p_LZC_median"], pos["p_LZC_ternary"]
        sigma_med = sigma_equivalent(pos["delta_LZC_median"], pos["surrogate_LZC_median_mean"], pos["surrogate_LZC_median_std"])
        sigma_tern = sigma_equivalent(pos["delta_LZC_ternary"], pos["surrogate_LZC_ternary_mean"], pos["surrogate_LZC_ternary_std"])
        med_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_med is not None and pos_p_med < 0.05) else "IAAFT_LOW_POWER"
        tern_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_tern is not None and pos_p_tern < 0.05) else "IAAFT_LOW_POWER"

    neg_p_med = neg.get("p_LZC_median")
    neg_p_tern = neg.get("p_LZC_ternary")
    neg_nonsig_med = neg_computable and (neg_p_med is None or neg_p_med >= 0.05)
    neg_nonsig_tern = neg_computable and (neg_p_tern is None or neg_p_tern >= 0.05)

    results["iaaft_power_check"] = {
        "LZC_median_channel": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_positive": pos_p_med if pos_computable else None,
            "p_negative": neg_p_med,
            "sigma_equivalent_positive": sigma_med,
            "correctly_nonsignificant_negative": neg_nonsig_med,
            "verdict": med_verdict,
        },
        "LZC_ternary_channel": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_positive": pos_p_tern if pos_computable else None,
            "p_negative": neg_p_tern,
            "sigma_equivalent_positive": sigma_tern,
            "correctly_nonsignificant_negative": neg_nonsig_tern,
            "verdict": tern_verdict,
        },
        "overall_note": (
            "No shared embedding step here (unlike RQA) -- LZC_median and "
            "LZC_ternary are computed independently per segment from the "
            "raw values, so a low-power finding for one channel does not "
            "imply the other is uncomputable; each channel's verdict is "
            "reported on its own merits."
        ),
    }

    results["a_priori_hypothesis_check"] = {
        "hypothesis": (
            "METHODOLOGY_NOTE.md gap (b): LZC_median and LZC_ternary risk "
            "redundancy with the Hurst/entropy-rate family already closed "
            "negative in this line (Ziv & Lempel 1978 asymptotic target), "
            "but real published counter-evidence of finite-sample non-"
            "redundancy exists (Villazana et al. 2015; Mateos et al. "
            "2017/2020). No a priori prediction was made about WHICH "
            "channel (if either) would show power -- unlike the PE "
            "candidate's C_JS/H_S asymmetric prediction, LZC_ternary is "
            "explicitly named as a robustness diagnostic, not a purpose-"
            "built chaos/noise discriminator (Nagarajan 2002) -- so both "
            "channels are tested and reported on equal footing."
        ),
        "LZC_median_verdict": med_verdict,
        "LZC_ternary_verdict": tern_verdict,
        "pattern_observed": (
            "BOTH_CHANNELS_SHOW_POWER" if (med_verdict == "IAAFT_HAS_REAL_POWER" and tern_verdict == "IAAFT_HAS_REAL_POWER") else
            "NEITHER_CHANNEL_SHOWS_POWER" if (med_verdict == "IAAFT_LOW_POWER" and tern_verdict == "IAAFT_LOW_POWER") else
            "ONLY_MEDIAN_SHOWS_POWER" if (med_verdict == "IAAFT_HAS_REAL_POWER" and tern_verdict == "IAAFT_LOW_POWER") else
            "ONLY_TERNARY_SHOWS_POWER" if (med_verdict == "IAAFT_LOW_POWER" and tern_verdict == "IAAFT_HAS_REAL_POWER") else
            "NOT_COMPUTABLE_OR_INDETERMINATE"
        ),
    }

    # ---- 4. Pre-authorized bootstrap fallback (METHODOLOGY_NOTE.md gap
    # (d)): triggered AUTOMATICALLY here because check 3 found IAAFT_LOW_POWER
    # for at least one channel (LZC_median) -- this is the ONE bounded,
    # pre-declared correction attempt allowed by this line's escalation
    # discipline. Run for BOTH channels (not just the low-power one) on
    # the SAME positive/negative control series already generated above,
    # so the two significance tests are directly comparable. This does
    # NOT redefine I(X) or R_lambda -- it only tests whether a different,
    # already-pre-authorized significance test recovers power where IAAFT
    # did not. ----
    low_power_channels = [
        ch for ch, v in [("LZC_median", med_verdict), ("LZC_ternary", tern_verdict)]
        if v == "IAAFT_LOW_POWER"
    ]
    bootstrap_triggered = len(low_power_channels) > 0

    if bootstrap_triggered:
        t0 = time.time()
        boot_pos = run_block_bootstrap_test(pos_pre, pos_post, seed=SEED)
        boot_neg = run_block_bootstrap_test(neg_pre, neg_post, seed=SEED)
        t_boot = time.time() - t0

        def _boot_verdict(p):
            return "BOOTSTRAP_HAS_REAL_POWER" if (p is not None and p < 0.05) else "BOOTSTRAP_LOW_POWER"

        boot_med_verdict = _boot_verdict(boot_pos["bootstrap_delta_LZC_median_p"])
        boot_tern_verdict = _boot_verdict(boot_pos["bootstrap_delta_LZC_ternary_p"])
        boot_neg_med_nonsig = (boot_neg["bootstrap_delta_LZC_median_p"] is None
                                or boot_neg["bootstrap_delta_LZC_median_p"] >= 0.05)
        boot_neg_tern_nonsig = (boot_neg["bootstrap_delta_LZC_ternary_p"] is None
                                 or boot_neg["bootstrap_delta_LZC_ternary_p"] >= 0.05)

        results["bootstrap_fallback_check"] = {
            "description": (
                "Triggered because IAAFT showed low power for channel(s): "
                f"{low_power_channels}. Moving-block bootstrap (Kunsch "
                "1989), block_length=max(N//20,10), n_bootstrap=200, "
                "seed=12345, run on the SAME positive/negative control "
                "series as the IAAFT check above. Pre-authorized by "
                "METHODOLOGY_NOTE.md gap (d) -- this is the ONE bounded "
                "correction attempt allowed by this line's escalation "
                "discipline, not a second redesign."
            ),
            "low_power_channels_triggering_this_check": low_power_channels,
            "positive_control": {
                "block_length": boot_pos["bootstrap_block_length"],
                "delta_LZC_median_real": boot_pos["delta_LZC_median_real"],
                "bootstrap_delta_LZC_median_p": boot_pos["bootstrap_delta_LZC_median_p"],
                "delta_LZC_ternary_real": boot_pos["delta_LZC_ternary_real"],
                "bootstrap_delta_LZC_ternary_p": boot_pos["bootstrap_delta_LZC_ternary_p"],
            },
            "negative_control": {
                "block_length": boot_neg["bootstrap_block_length"],
                "delta_LZC_median_real": boot_neg["delta_LZC_median_real"],
                "bootstrap_delta_LZC_median_p": boot_neg["bootstrap_delta_LZC_median_p"],
                "delta_LZC_ternary_real": boot_neg["delta_LZC_ternary_real"],
                "bootstrap_delta_LZC_ternary_p": boot_neg["bootstrap_delta_LZC_ternary_p"],
            },
            "LZC_median_bootstrap_verdict": boot_med_verdict,
            "LZC_median_negative_correctly_nonsignificant": boot_neg_med_nonsig,
            "LZC_ternary_bootstrap_verdict": boot_tern_verdict,
            "LZC_ternary_negative_correctly_nonsignificant": boot_neg_tern_nonsig,
            "wall_clock_seconds": t_boot,
        }
        print(json.dumps(results["bootstrap_fallback_check"], indent=2))
    else:
        results["bootstrap_fallback_check"] = {
            "triggered": False,
            "description": "Not triggered -- no channel showed IAAFT_LOW_POWER.",
        }

    # ---- Final per-channel decision-protocol verdict, combining IAAFT
    # (primary) with the pre-authorized bootstrap fallback where it was
    # triggered. This is a MECHANICAL combination of checks 3 and 4, not a
    # new judgment call. ----
    def _final_channel_verdict(iaaft_verdict, channel_key):
        if iaaft_verdict == "IAAFT_HAS_REAL_POWER":
            return "SURVIVES_PRIMARY_IAAFT_TEST"
        if not bootstrap_triggered or channel_key not in low_power_channels:
            return "NO_POWER_ESTABLISHED"
        boot_verdict = results["bootstrap_fallback_check"].get(f"{channel_key}_bootstrap_verdict")
        boot_neg_ok = results["bootstrap_fallback_check"].get(f"{channel_key}_negative_correctly_nonsignificant")
        if boot_verdict == "BOOTSTRAP_HAS_REAL_POWER" and boot_neg_ok:
            return "SURVIVES_BOOTSTRAP_FALLBACK_TEST"
        return "NO_POWER_ESTABLISHED_EITHER_TEST"

    results["final_decision_protocol_verdict"] = {
        "description": (
            "Mechanical combination of the IAAFT primary test (check 3) "
            "with the pre-authorized bootstrap fallback (check 4, only "
            "run for channels IAAFT found low-power). This is the ONE "
            "correction cycle this line's escalation discipline allows -- "
            "no further redesign is authorized regardless of the outcome "
            "here."
        ),
        "LZC_median": _final_channel_verdict(med_verdict, "LZC_median"),
        "LZC_ternary": _final_channel_verdict(tern_verdict, "LZC_ternary"),
    }

    results["pipeline_config"] = pos_result["config"]
    results["generator_notes"] = {
        "colored_noise_fgn_like": (
            "FFT-filtering spectral synthesis: white Gaussian noise scaled "
            "per-frequency by f^(-exponent/2), inverse-transformed, "
            "z-scored. fGn-like approximation via exponent=2H+1 (spectral "
            "relation for fractional Gaussian noise); same technique as "
            "other validate_synthetic.py scripts in this lab, independent "
            "implementation."
        ),
        "logistic_map": "x_{k+1} = 4*x_k*(1-x_k), burn_in=500 discarded transient iterations.",
        "rank_remap": (
            "POST = sorted(PRE)[argsort(argsort(logistic_map_raw))] -- "
            "POST is an exact permutation of PRE's own values, reordered "
            "by the logistic map's temporal rank structure."
        ),
    }
    results["wall_clock_seconds_total"] = time.time() - t_start

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results["code_correctness_diagnostic"], indent=2, default=str))
    print(json.dumps(results["iaaft_power_check"], indent=2))
    print(json.dumps(results["a_priori_hypothesis_check"], indent=2))
    print(json.dumps(results["differential_hurst_control_verdict"], indent=2))
    print(json.dumps(results["final_decision_protocol_verdict"], indent=2))
    print(f"\nWrote {out_path}")
    print(f"Total wall clock: {results['wall_clock_seconds_total']:.1f}s")


if __name__ == "__main__":
    main()
