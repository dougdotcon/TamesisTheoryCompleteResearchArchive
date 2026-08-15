"""
Synthetic validation of `mse_common.py`, run and committed BEFORE any real
PRE/POST segment (Dst/SYM-H March 1989 storm, FEMTO/PRONOSTIA bearing) is
touched -- required by METHODOLOGY_NOTE.md "Validacao obrigatoria adicional
(ANTES de qualquer dado real)": since IAAFT is the PRIMARY significance test
for this candidate (unlike DFA/CSD/SOC in this lab, where it was secondary),
this script must confirm IAAFT has real power to detect a genuine nonlinear
change in CI/beta before the pipeline can be applied to real data.

Three checks, all synthetic, all seeded for reproducibility:

1. Costa et al. sanity check: white noise (SampEn should DECREASE with
   scale -- short-range structure only, beta<0) vs. long-range-correlated
   ("1/f-like", spectral exponent ~1) noise (SampEn should stay relatively
   FLAT/high across scales, beta ~ 0 or mildly positive). Both series are
   built with a spectral-synthesis (FFT-filtering) colored-noise generator
   implemented directly below (independent of dfa_common.py's Davies-Harte
   fGn generator -- this test line does not import from that module).

2. Positive control -- the central identifiability test for this
   candidate. PRE = linear Gaussian white noise. POST = the logistic map
   in the fully chaotic regime (r=4), a genuine deterministic nonlinear
   process, RANK-REMAPPED onto PRE's own exact empirical distribution so
   the two series share an EXACTLY identical marginal (histogram) by
   construction. Amplitude spectrum is matched only approximately, but
   the mismatch is small by construction: the logistic map at r=4 is
   ergodic with an autocorrelation function that is analytically zero at
   every nonzero lag (it is topologically conjugate to the tent map /
   Bernoulli shift), i.e. its power spectrum is theoretically flat --
   the same as white noise's. The periodogram-slope estimator below
   empirically confirms both series have a spectral exponent close to 0.
   IAAFT surrogates preserve the (matched) amplitude spectrum and the
   (exactly matched) marginal but destroy the logistic map's deterministic
   phase relationships, so if CI/beta genuinely respond to that
   determinism (and not just to spectrum+marginal), the real Delta_CI /
   Delta_beta should sit outside the IAAFT null distribution (p small).

3. Negative control: PRE and POST = two INDEPENDENT realizations of the
   SAME nonlinear process (logistic map, r=4, different initial
   conditions) -- a stringent negative control (nonlinear vs. nonlinear,
   not just noise vs. noise), where p should be typically non-significant.

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mse_common import compute_mse, run_mse_pipeline, N_SURROGATES, N_IAAFT_ITER, SEED


# --------------------------------------------------------------------------
# Synthetic generators (independent of dfa_common.py / wtmm_common.py)
# --------------------------------------------------------------------------

def colored_noise(n, spectral_exponent, rng):
    """Gaussian colored noise with power spectral density S(f) ~ 1/f^exponent,
    via the standard FFT-filtering spectral-synthesis method: draw white
    Gaussian noise, scale each Fourier component's amplitude by
    f^(-exponent/2), inverse-transform, z-score. exponent=0 reduces to
    (approximately) white noise; exponent=1 is classic "1/f"/pink noise.
    The DC component is zeroed (no meaningful "frequency 0" scaling).
    """
    white = rng.standard_normal(n)
    spectrum = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n)
    scale = np.zeros_like(freqs)
    scale[1:] = freqs[1:] ** (-spectral_exponent / 2.0)
    x = np.fft.irfft(spectrum * scale, n=n)
    return (x - x.mean()) / x.std()


def logistic_map(n, x0, r=4.0, burn_in=500):
    """Fully chaotic logistic map trajectory x_{k+1} = r*x_k*(1-x_k), r=4.
    Discards `burn_in` transient iterations before returning `n` points."""
    total = n + burn_in
    x = np.empty(total, dtype=float)
    x[0] = x0
    for i in range(1, total):
        x[i] = r * x[i - 1] * (1.0 - x[i - 1])
    return x[burn_in:]


def rank_remap_to_reference(x, reference):
    """Return a series with `reference`'s EXACT empirical distribution
    (same multiset of values), reordered to match x's temporal rank order
    -- i.e. a monotonic, order-preserving transform of x. Requires
    len(x) == len(reference)."""
    x = np.asarray(x, dtype=float)
    reference = np.asarray(reference, dtype=float)
    assert len(x) == len(reference)
    ranks = np.argsort(np.argsort(x))
    ref_sorted = np.sort(reference)
    return ref_sorted[ranks]


def estimate_spectral_exponent(x):
    """Periodogram-slope estimate of the spectral exponent (S(f) ~ f^-exponent):
    OLS slope of log(power) vs log(freq) over nonzero frequencies; exponent
    = -slope. Used only as an empirical diagnostic to confirm the
    PRE/POST spectral match claimed in the positive control, not as part
    of the pipeline itself."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    spectrum = np.fft.rfft(x - x.mean())
    power = np.abs(spectrum) ** 2
    freqs = np.fft.rfftfreq(n)
    mask = freqs > 0
    slope, _ = np.polyfit(np.log(freqs[mask]), np.log(power[mask] + 1e-300), 1)
    return float(-slope)


def _mse_summary(mse_result):
    return {
        "n_samples": mse_result["n_samples"],
        "tau_max": mse_result["tau_max"],
        "scales_used": mse_result["scales_used"],
        "r": mse_result["r"],
        "sampen_values": mse_result["sampen_values"],
        "n_scales_undefined": mse_result["n_scales_undefined"],
        "CI": mse_result["CI"],
        "beta": None if mse_result["beta"] is None else mse_result["beta"]["beta"],
    }


def _pipeline_summary(label, result, extra=None):
    d = {
        "CI_pre": result["CI_pre"],
        "CI_post": result["CI_post"],
        "beta_pre": result["beta_pre"],
        "beta_post": result["beta_post"],
        "delta_CI": result["delta_CI"],
        "delta_beta": result["delta_beta"],
        "p_CI": result["p_CI"],
        "p_beta": result["p_beta"],
        "surrogate_CI_mean": result["surrogate_CI_mean"],
        "surrogate_CI_std": result["surrogate_CI_std"],
        "surrogate_CI_n_valid": result["surrogate_CI_n_valid"],
        "surrogate_CI_n_undefined": result["surrogate_CI_n_undefined"],
        "surrogate_beta_mean": result["surrogate_beta_mean"],
        "surrogate_beta_std": result["surrogate_beta_std"],
        "surrogate_beta_n_valid": result["surrogate_beta_n_valid"],
        "surrogate_beta_n_undefined": result["surrogate_beta_n_undefined"],
        "real_pre_sampen_values": result["real_pre"]["sampen_values"],
        "real_post_sampen_values": result["real_post"]["sampen_values"],
        "scales_used_pre": result["real_pre"]["scales_used"],
        "scales_used_post": result["real_post"]["scales_used"],
    }
    if extra:
        d.update(extra)
    return d


def main():
    results = {}
    N_SANITY = 4000
    N_CTRL = 4000

    # ---- 1. Costa et al. sanity check: white noise vs. 1/f-like noise ----
    rng_sanity = np.random.default_rng(101)
    white = colored_noise(N_SANITY, 0.0, rng_sanity)
    pink = colored_noise(N_SANITY, 1.0, rng_sanity)

    white_mse = compute_mse(white)
    pink_mse = compute_mse(pink)

    results["sanity_costa_et_al"] = {
        "white_noise": {
            **_mse_summary(white_mse),
            "spectral_exponent_estimated": estimate_spectral_exponent(white),
            "expected": "SampEn decreases with scale (short-range structure only), beta<0",
        },
        "pink_1_over_f_noise": {
            **_mse_summary(pink_mse),
            "spectral_exponent_estimated": estimate_spectral_exponent(pink),
            "expected": "SampEn relatively flat/high across scales, beta near 0 or mildly positive",
        },
        "qualitative_check": {
            "white_beta_negative": white_mse["beta"] is not None and white_mse["beta"]["beta"] < 0,
            "pink_beta_closer_to_zero_than_white": (
                white_mse["beta"] is not None and pink_mse["beta"] is not None
                and abs(pink_mse["beta"]["beta"]) < abs(white_mse["beta"]["beta"])
            ),
            "pink_CI_greater_than_white_CI": (
                white_mse["CI"] is not None and pink_mse["CI"] is not None
                and pink_mse["CI"] > white_mse["CI"]
            ),
        },
    }

    # ---- 2. Positive control: PRE = white Gaussian noise (linear),
    # POST = chaotic logistic map (r=4) rank-remapped onto PRE's exact
    # marginal -- same distribution, closely matched (both ~flat) spectrum,
    # genuine deterministic nonlinear structure in POST that IAAFT (linear
    # spectrum + marginal preserving) should NOT reproduce. ----
    rng_pos = np.random.default_rng(424242)
    pos_pre = rng_pos.standard_normal(N_CTRL)
    logi_raw = logistic_map(N_CTRL, x0=0.234567891, r=4.0, burn_in=500)
    pos_post = rank_remap_to_reference(logi_raw, pos_pre)

    pos_spec_pre = estimate_spectral_exponent(pos_pre)
    pos_spec_post = estimate_spectral_exponent(pos_post)

    pos_result = run_mse_pipeline(pos_pre, pos_post)
    results["positive_control"] = _pipeline_summary(
        "positive_control", pos_result,
        extra={
            "description": (
                "PRE = iid Gaussian white noise (linear). POST = logistic map "
                "(r=4, fully chaotic, genuine deterministic nonlinear process), "
                "rank-remapped onto PRE's own sorted values so PRE and POST "
                "share an EXACTLY identical empirical marginal distribution "
                "by construction (same multiset of values, different temporal "
                "order). Amplitude-spectrum match documented empirically via "
                "periodogram-slope spectral_exponent (both ~0, i.e. ~flat/"
                "white) rather than assumed."
            ),
            "n_pre": N_CTRL,
            "n_post": N_CTRL,
            "spectral_exponent_pre": pos_spec_pre,
            "spectral_exponent_post": pos_spec_post,
            "marginal_match": "exact (rank-remap of POST onto PRE's sorted values)",
        },
    )

    # ---- 3. Negative control: two independent logistic-map realizations
    # (same nonlinear process, different initial conditions) ----
    neg_pre = logistic_map(N_CTRL, x0=0.234567891, r=4.0, burn_in=500)
    neg_post = logistic_map(N_CTRL, x0=0.789123456, r=4.0, burn_in=500)

    neg_result = run_mse_pipeline(neg_pre, neg_post)
    results["negative_control"] = _pipeline_summary(
        "negative_control", neg_result,
        extra={
            "description": (
                "PRE and POST = two independent realizations of the SAME "
                "nonlinear process (logistic map, r=4, different initial "
                "conditions x0=0.234567891 vs x0=0.789123456). A stringent "
                "negative control (nonlinear vs nonlinear, not just noise vs "
                "noise)."
            ),
            "n_pre": N_CTRL,
            "n_post": N_CTRL,
        },
    )

    # ---- 4. IAAFT power-check verdict (the central question this
    # validation exists to answer, per METHODOLOGY_NOTE.md gap (c)) ----
    pos_p_CI = results["positive_control"]["p_CI"]
    pos_p_beta = results["positive_control"]["p_beta"]
    neg_p_CI = results["negative_control"]["p_CI"]
    neg_p_beta = results["negative_control"]["p_beta"]

    pos_sig_CI = pos_p_CI is not None and pos_p_CI < 0.05
    pos_sig_beta = pos_p_beta is not None and pos_p_beta < 0.05
    neg_nonsig_CI = neg_p_CI is not None and neg_p_CI >= 0.05
    neg_nonsig_beta = neg_p_beta is not None and neg_p_beta >= 0.05

    results["iaaft_power_check"] = {
        "positive_control": {
            "p_CI": pos_p_CI,
            "p_beta": pos_p_beta,
            "significant_CI_at_0.05": pos_sig_CI,
            "significant_beta_at_0.05": pos_sig_beta,
            "power_present": bool(pos_sig_CI or pos_sig_beta),
        },
        "negative_control": {
            "p_CI": neg_p_CI,
            "p_beta": neg_p_beta,
            "correctly_nonsignificant_CI": neg_nonsig_CI,
            "correctly_nonsignificant_beta": neg_nonsig_beta,
        },
        "verdict": (
            "IAAFT_HAS_REAL_POWER"
            if (pos_sig_CI or pos_sig_beta) else
            "IAAFT_LOW_POWER_SAME_PATTERN_AS_DFA"
        ),
        "note": (
            "Per METHODOLOGY_NOTE.md gap (c), IAAFT is the PRIMARY significance "
            "test for this candidate (unlike DFA/CSD/SOC in this lab). This "
            "verdict is the pass/fail gate for whether the mse_common.py "
            "pipeline, as specified, is ready for real-data application without "
            "a complementary significance test being added first (the same "
            "correction already applied twice in this line, DFA and SOC)."
        ),
    }

    results["pipeline_config"] = pos_result["config"]
    results["generator_notes"] = {
        "colored_noise": (
            "FFT-filtering spectral synthesis: white Gaussian noise scaled "
            "per-frequency by f^(-exponent/2) in the frequency domain, "
            "inverse-transformed, z-scored. Standard technique, independent "
            "implementation (not dfa_common.py's Davies-Harte fGn generator)."
        ),
        "logistic_map": "x_{k+1} = 4*x_k*(1-x_k), burn_in=500 discarded transient iterations.",
        "rank_remap": (
            "POST = sorted(PRE)[argsort(argsort(logistic_map_raw))] -- POST is "
            "an exact permutation of PRE's own values, reordered by the "
            "logistic map's temporal rank structure. Guarantees an EXACTLY "
            "identical marginal distribution between PRE and POST."
        ),
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
