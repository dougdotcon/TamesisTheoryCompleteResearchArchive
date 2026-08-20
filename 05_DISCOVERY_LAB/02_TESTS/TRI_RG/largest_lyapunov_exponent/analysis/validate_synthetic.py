"""
Synthetic validation of `lle_common.py`, run and committed BEFORE any real
PRE/POST segment (Kilauea 2018 May-17 explosive onset, MIT-BIH afdb record
04936) is touched -- required by METHODOLOGY_NOTE.md's mandatory validation
gate, mirroring the EXACT two-stage design already used by `rqa`
(`../../rqa/analysis/validate_synthetic.py`, `../../rqa/VALIDATION_NOTE.md`)
because this candidate reuses the SAME audited FNN/mutual-information
embedding machinery that structurally blocked RQA's white-noise positive
control.

Checks, all synthetic, all seeded for reproducibility:

0a. Rosenstein/Kantz-Schreiber CODE-CORRECTNESS diagnostic against a KNOWN
    analytic answer (NOT part of the identifiability validation itself,
    clearly labeled supplementary): logistic map (r=4, fully chaotic),
    theoretical lambda_1 = ln(2) ~= 0.693 nats/iteration. The embedding
    dimension is FORCED to m=2, tau=1 here ONLY (bypassing the FNN gate) --
    this is a deliberate, explicitly-labeled exception used ONLY to test
    whether compute_lambda1's divergence-curve + Kantz-Schreiber code
    recovers the right order of magnitude/sign against ground truth when
    a sufficient embedding is known a priori; it is NEVER used this way in
    the real pipeline (run_lle_analysis always applies the mandatory FNN
    hard-reject gate with no forced m). Discovered here (before any
    validation-control or real-data calculation): the raw "largest stable
    window" rule alone is NOT sufficient -- a bounded chaotic attractor's
    divergence-curve PLATEAU (post-saturation) is trivially "stable across
    m" (near-zero slope everywhere) and, being longer than the true
    exponential-growth segment, wins the naive rule, silently returning
    lambda_1~=0. Fixed by adding a joint R²>=0.95 goodness-of-fit gate
    (MIN_R2_FOR_LINEAR_REGION in lle_common.py) -- documented in
    METHODOLOGY_NOTE.md and in lle_common.py's module-level comment. This is
    a mechanical-rule refinement made during code-correctness testing, NOT a
    reformulation of R_lambda/I(X) after seeing real or validation-control
    results.

0b. Full-pipeline (FNN-gated, no forced m) sanity check on a deterministic
    but NON-chaotic signal: a clean sine wave with a tiny (1e-6 relative)
    dither (same technique/rationale as rqa's own diagnostic -- breaks
    floating-point-exact recurrences that spuriously blow up FNN's ratio
    criterion). Expected and CORRECT result: FNN/MI resolve normally, D2
    comes out near 1.0 (a periodic orbit is a 1-D closed curve), and
    lambda_1's linear-region search correctly finds NO stable exponential-
    growth region (status="linear_region_not_resolved") -- a periodic
    signal has no genuine positive Lyapunov exponent, so finding nothing is
    the CORRECT behavior, not a bug.

1. Positive control v1 -- the central identifiability test, EXACTLY as
   specified in METHODOLOGY_NOTE.md: PRE = white Gaussian noise. POST =
   logistic map (r=4) rank-remapped onto PRE's exact marginal. Given the
   EXACT SAME audited FNN code RQA's validation already found never resolves
   m<=10 for white noise, this is EXPECTED (but tested, not assumed) to hit
   embedding_not_resolved here too.

1b. Positive control v2 (Roessler-sourced POST) -- the ONE pre-declared
   additional validation attempt (METHODOLOGY_NOTE.md), triggered only if
   check 1 hits embedding_not_resolved: PRE = fGn-like H=0.7 (resolves FNN).
   POST = Roessler system x-coordinate, rank-remapped onto PRE. Decision
   rule fixed a priori: p<0.05 with clear null separation on EITHER channel
   (lambda_1 or D2) -> validation passes; neither -> candidate closed at the
   validation stage, no third attempt.

2. Negative control: PRE and POST = two INDEPENDENT realizations of the SAME
   linear process (fGn-like, H=0.7 fixed, independent seeds) -- probes the
   spectral/linear risk directly, exercises the full pipeline end-to-end.

3. Structural-wall characterization (supplementary, cheap -- tau/m only, no
   lambda_1/D2): fGn-H / AR(1)-phi resolvability sweep + explicit
   bootstrap-on-white-noise check, confirming (not assuming) the SAME
   FNN wall already characterized for RQA reproduces here (expected, since
   the embedding code is imported unmodified from rqa_common.py).

4. IAAFT power-check verdict per channel (lambda_1, D2), PLUS the addendum
   decision rule applied mechanically to positive_control_v2.

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lle_common import (
    run_lle_analysis, estimate_tau, estimate_m, compute_lle_features,
    compute_lambda1, theiler_window, moving_block_bootstrap_resample,
    N_SURROGATES, N_IAAFT_ITER, SEED,
)


# --------------------------------------------------------------------------
# Synthetic generators (same technique/spirit as rqa's validate_synthetic.py,
# independent implementation for this candidate)
# --------------------------------------------------------------------------

def colored_noise(n, spectral_exponent, rng):
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
    total = n + burn_in
    x = np.empty(total, dtype=float)
    x[0] = x0
    for i in range(1, total):
        x[i] = r * x[i - 1] * (1.0 - x[i - 1])
    return x[burn_in:]


def rank_remap_to_reference(x, reference):
    x = np.asarray(x, dtype=float)
    reference = np.asarray(reference, dtype=float)
    assert len(x) == len(reference)
    ranks = np.argsort(np.argsort(x))
    ref_sorted = np.sort(reference)
    return ref_sorted[ranks]


def estimate_spectral_exponent(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    spectrum = np.fft.rfft(x - x.mean())
    power = np.abs(spectrum) ** 2
    freqs = np.fft.rfftfreq(n)
    mask = freqs > 0
    slope, _ = np.polyfit(np.log(freqs[mask]), np.log(power[mask] + 1e-300), 1)
    return float(-slope)


def ar1_process(n, phi, rng):
    e = rng.standard_normal(n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def rossler_x(n_out, sample_dt=0.15, dt_internal=0.01, a=0.2, b=0.2, c=5.7,
              burn_in_time=200.0, x0=(1.0, 1.0, 1.0)):
    """Roessler system (Roessler 1976), same parameters/integration scheme
    already validated by rqa's validate_synthetic.py (sample_dt=0.15 chosen
    there because it empirically gives a spectral exponent close to fGn
    H=0.7's target 2H+1=2.4)."""
    def deriv(s):
        x, y, z = s
        return np.array([-y - z, x + a * y, b + z * (x - c)])

    steps_per_sample = max(1, round(sample_dt / dt_internal))
    burn_in_steps = int(round(burn_in_time / dt_internal))
    total_steps = burn_in_steps + n_out * steps_per_sample
    s = np.array(x0, dtype=float)
    h = dt_internal
    xs = np.empty(n_out)
    k = 0
    for i in range(total_steps):
        k1 = deriv(s)
        k2 = deriv(s + h / 2 * k1)
        k3 = deriv(s + h / 2 * k2)
        k4 = deriv(s + h * k3)
        s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if i >= burn_in_steps and (i - burn_in_steps) % steps_per_sample == 0:
            if k < n_out:
                xs[k] = s[0]
                k += 1
    return xs


def sine_with_dither(n, period, dither_frac, rng):
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
            "m": result["m"], "tau": result["tau"],
            "lambda1_pre": result["lambda1_pre"], "lambda1_post": result["lambda1_post"],
            "d2_pre": result["d2_pre"], "d2_post": result["d2_post"],
            "delta_lambda1": result["delta_lambda1"], "delta_d2": result["delta_d2"],
            "p_lambda1": result["p_lambda1"], "p_d2": result["p_d2"],
            "surrogate_lambda1_mean": result["surrogate_lambda1_mean"],
            "surrogate_lambda1_std": result["surrogate_lambda1_std"],
            "surrogate_lambda1_n_valid": result["surrogate_lambda1_n_valid"],
            "surrogate_lambda1_n_undefined": result["surrogate_lambda1_n_undefined"],
            "surrogate_d2_mean": result["surrogate_d2_mean"],
            "surrogate_d2_std": result["surrogate_d2_std"],
            "surrogate_d2_n_valid": result["surrogate_d2_n_valid"],
            "surrogate_d2_n_undefined": result["surrogate_d2_n_undefined"],
            "diagnostics": result["diagnostics"],
            "real_pre_lambda1_status": result["real_pre"]["lambda1_result"]["status"],
            "real_post_lambda1_status": result["real_post"]["lambda1_result"]["status"],
            "real_pre_d2_status": result["real_pre"]["d2_result"]["status"],
            "real_post_d2_status": result["real_post"]["d2_result"]["status"],
            "real_pre_lambda1_r2": result["real_pre"]["lambda1_result"].get("r_squared"),
            "real_post_lambda1_r2": result["real_post"]["lambda1_result"].get("r_squared"),
        })
    else:
        d.update({
            "tau_info": {k: v for k, v in result["tau_info"].items() if k != "mi_curve"},
            "m_info": (
                None if result.get("m_info") is None else
                {k: v for k, v in result["m_info"].items() if k != "fnn_curve"}
            ),
            "fnn_curve": (
                None if result.get("m_info") is None else
                [{"m": r["m"], "fraction": r.get("fraction"), "status": r.get("status")}
                 for r in result["m_info"]["fnn_curve"]]
            ),
            "diagnostics": result["diagnostics"],
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

    # ---- 0a. Rosenstein/Kantz-Schreiber code-correctness diagnostic
    # against a KNOWN analytic answer (embedding FORCED, bypassing FNN --
    # see module docstring). ----
    N_DIAG_A = 3000
    logi = logistic_map(N_DIAG_A, x0=0.234567891, r=4.0, burn_in=500)
    w_diag = theiler_window(logi)
    lambda1_diag = compute_lambda1(logi, m_star=2, tau=1, w=w_diag["w"]) if w_diag["status"] == "ok" else None
    results["code_correctness_diagnostic_logistic_forced_embedding"] = {
        "description": (
            "Logistic map (r=4), N=3000, embedding FORCED to m=2, tau=1 "
            "(bypassing the mandatory FNN gate ONLY for this diagnostic -- "
            "NEVER done in the real pipeline). Tests whether "
            "compute_lambda1's Rosenstein divergence-curve + Kantz-Schreiber "
            "code recovers the theoretical lambda_1=ln(2)~=0.693 "
            "nats/iteration against ground truth, given a known-sufficient "
            "embedding. NOT a PRE/POST identifiability test."
        ),
        "n_samples": N_DIAG_A, "theiler_window": w_diag,
        "lambda1_result": lambda1_diag,
        "theoretical_lambda1": float(np.log(2)),
    }

    # ---- 0b. Full-pipeline (FNN-gated) sanity check on a non-chaotic
    # deterministic signal (dithered sine wave). ----
    rng0 = np.random.default_rng(909)
    N_DIAG_B = 1000
    sine = sine_with_dither(N_DIAG_B, period=50, dither_frac=1e-6, rng=rng0)
    tau_diag = estimate_tau(sine)
    m_diag = estimate_m(sine, tau_diag["tau"]) if tau_diag["status"] == "ok" else None
    feat_diag = (compute_lle_features(sine, m_diag["m"], tau_diag["tau"])
                 if (m_diag is not None and m_diag["status"] == "ok") else None)
    results["code_correctness_diagnostic_sine_full_pipeline"] = {
        "description": (
            "Deterministic sine wave (period=50) with a 1e-6-relative "
            "Gaussian dither, N=1000, run through the FULL FNN-gated "
            "pipeline (no forced m). Expected and CORRECT result: FNN/MI "
            "resolve normally, D2~=1.0 (periodic orbit = 1-D closed curve), "
            "and lambda_1's linear-region search finds NO stable "
            "exponential-growth region (a periodic signal has zero genuine "
            "Lyapunov exponent) -- 'linear_region_not_resolved' here is the "
            "CORRECT answer, not a failure."
        ),
        "n_samples": N_DIAG_B,
        "tau": tau_diag,
        "m": (None if m_diag is None else {k: v for k, v in m_diag.items() if k != "fnn_curve"}),
        "features": feat_diag,
    }

    # ---- 1. Positive control v1: PRE = white Gaussian noise, POST =
    # logistic map (r=4) rank-remapped onto PRE. EXACT METHODOLOGY_NOTE.md
    # specification. ----
    N_CTRL = 2000
    rng_pos = np.random.default_rng(424242)
    pos_pre = rng_pos.standard_normal(N_CTRL)
    logi_raw = logistic_map(N_CTRL, x0=0.234567891, r=4.0, burn_in=500)
    pos_post = rank_remap_to_reference(logi_raw, pos_pre)

    pos_spec_pre = estimate_spectral_exponent(pos_pre)
    pos_spec_post = estimate_spectral_exponent(pos_post)

    t0 = time.time()
    pos_result = run_lle_analysis(pos_pre, pos_post, seed=SEED)
    t_pos = time.time() - t0

    results["positive_control"] = _pipeline_summary(
        pos_result,
        extra={
            "description": (
                "PRE = iid Gaussian white noise. POST = logistic map (r=4), "
                "rank-remapped onto PRE's exact empirical marginal. Tests "
                "whether the mandatory FNN gate resolves for the literal "
                "METHODOLOGY_NOTE.md positive-control PRE."
            ),
            "n_pre": N_CTRL, "n_post": N_CTRL,
            "spectral_exponent_pre": pos_spec_pre, "spectral_exponent_post": pos_spec_post,
            "marginal_match": "exact (rank-remap of POST onto PRE's sorted values)",
            "wall_clock_seconds": t_pos,
        },
    )

    # ---- 2. Negative control: PRE, POST = two independent fGn-like H=0.7
    # realizations. ----
    N_NEG = N_CTRL
    rng_neg_pre = np.random.default_rng(555001)
    rng_neg_post = np.random.default_rng(555002)
    neg_pre = fgn_like(N_NEG, H=0.7, rng=rng_neg_pre)
    neg_post = fgn_like(N_NEG, H=0.7, rng=rng_neg_post)

    t0 = time.time()
    neg_result = run_lle_analysis(neg_pre, neg_post, seed=SEED)
    t_neg = time.time() - t0

    results["negative_control"] = _pipeline_summary(
        neg_result,
        extra={
            "description": (
                "PRE and POST = two INDEPENDENT realizations of the SAME "
                "linear process (fGn-like, H=0.7 fixed, independent seeds "
                "555001/555002). Same autocorrelation structure, no genuine "
                "change -- p should typically be non-significant for both "
                "channels. H=0.7 resolves FNN (see structural_wall_"
                "characterization below)."
            ),
            "n_pre": N_NEG, "n_post": N_NEG, "wall_clock_seconds": t_neg,
        },
    )

    # ---- 1b. Positive control v2 -- Roessler-sourced POST (the ONE
    # pre-authorized additional attempt, triggered by positive_control (v1)
    # hitting embedding_not_resolved). ----
    rng_pos2_pre = np.random.default_rng(424242)
    pos2_pre = fgn_like(N_CTRL, H=0.7, rng=rng_pos2_pre)
    rossler_raw = rossler_x(N_CTRL, sample_dt=0.15)
    pos2_post = rank_remap_to_reference(rossler_raw, pos2_pre)

    pos2_spec_pre = estimate_spectral_exponent(pos2_pre)
    pos2_spec_post = estimate_spectral_exponent(pos2_post)
    pos2_spec_rossler_raw = estimate_spectral_exponent(rossler_raw)

    t0 = time.time()
    pos2_result = run_lle_analysis(pos2_pre, pos2_post, seed=SEED)
    t_pos2 = time.time() - t0

    results["positive_control_v2_rossler"] = _pipeline_summary(
        pos2_result,
        extra={
            "description": (
                "METHODOLOGY_NOTE.md's ONE pre-authorized additional "
                "validation attempt. PRE = fGn-like H=0.7 (resolves FNN). "
                "POST = Roessler system (a=0.2, b=0.2, c=5.7, RK4, "
                "dt_internal=0.01, sample_dt=0.15) x-coordinate, "
                "rank-remapped onto PRE's exact empirical distribution."
            ),
            "n_pre": N_CTRL, "n_post": N_CTRL,
            "spectral_exponent_pre": pos2_spec_pre, "spectral_exponent_post": pos2_spec_post,
            "spectral_exponent_rossler_raw_pre_remap": pos2_spec_rossler_raw,
            "spectral_exponent_target_fgn_H0.7": 2 * 0.7 + 1,
            "marginal_match": "exact (rank-remap of POST onto PRE's sorted values)",
            "rossler_params": {"a": 0.2, "b": 0.2, "c": 5.7, "sample_dt": 0.15,
                                "dt_internal": 0.01, "burn_in_time": 200.0},
            "wall_clock_seconds": t_pos2,
        },
    )

    # ---- 3. Structural-wall characterization (supplementary, cheap --
    # tau/m only). ----
    sweep_fgn = []
    for H in [0.1, 0.3, 0.5, 0.6, 0.7, 0.9]:
        rng_h = np.random.default_rng(100 + int(H * 10))
        x = fgn_like(N_CTRL, H, rng_h)
        tau_i = estimate_tau(x)
        m_i = estimate_m(x, tau_i["tau"]) if tau_i["status"] == "ok" else {"status": "tau_failed"}
        sweep_fgn.append({"H": H, "tau": tau_i.get("tau"), "m_status": m_i["status"], "m": m_i.get("m")})

    sweep_ar1 = []
    for phi in [0.0, 0.3, 0.5, 0.7, 0.9, 0.95]:
        rng_p = np.random.default_rng(200 + int(phi * 10))
        x = ar1_process(N_CTRL, phi, rng_p)
        tau_i = estimate_tau(x)
        m_i = estimate_m(x, tau_i["tau"]) if tau_i["status"] == "ok" else {"status": "tau_failed"}
        sweep_ar1.append({"phi": phi, "tau": tau_i.get("tau"), "m_status": m_i["status"], "m": m_i.get("m")})

    rng_boot = np.random.default_rng(999)
    white_for_boot = rng_boot.standard_normal(N_CTRL)
    boot_rng = np.random.default_rng(SEED)
    n_resolved = 0
    n_boot_checks = 25
    boot_details = []
    for _ in range(n_boot_checks):
        resampled = moving_block_bootstrap_resample(white_for_boot, L=20, rng=boot_rng)
        tau_i = estimate_tau(resampled)
        if tau_i["status"] != "ok":
            boot_details.append({"tau_status": tau_i["status"]})
            continue
        m_i = estimate_m(resampled, tau_i["tau"])
        if m_i["status"] == "ok":
            n_resolved += 1
        boot_details.append({"tau": tau_i["tau"], "m_status": m_i["status"]})

    results["structural_wall_characterization"] = {
        "description": (
            "Supplementary checks confirming (not assuming) the FNN wall "
            "already characterized for RQA reproduces here, since the "
            "embedding code is imported unmodified from rqa_common.py."
        ),
        "fgn_H_sweep_N2000": sweep_fgn,
        "ar1_phi_sweep_N2000": sweep_ar1,
        "bootstrap_on_white_noise": {
            "n_bootstrap_resamples_tested": n_boot_checks,
            "n_resolved_embedding": n_resolved,
            "block_length_L": 20,
            "verdict": ("BOOTSTRAP_DOES_NOT_RESOLVE" if n_resolved == 0 else
                        f"BOOTSTRAP_PARTIALLY_RESOLVES ({n_resolved}/{n_boot_checks})"),
            "details_first_5": boot_details[:5],
        },
    }

    # ---- 4. IAAFT power-check verdict, PER CHANNEL. ----
    pos = results["positive_control"]
    neg = results["negative_control"]

    pos_computable = pos["status"] == "ok"
    neg_computable = neg["status"] == "ok"

    if not pos_computable:
        l1_verdict = d2_verdict = "NOT_COMPUTABLE_EMBEDDING_NOT_RESOLVED"
        sigma_l1 = sigma_d2 = None
        pos_p_l1 = pos_p_d2 = None
    else:
        pos_p_l1, pos_p_d2 = pos["p_lambda1"], pos["p_d2"]
        sigma_l1 = sigma_equivalent(pos["delta_lambda1"], pos["surrogate_lambda1_mean"], pos["surrogate_lambda1_std"])
        sigma_d2 = sigma_equivalent(pos["delta_d2"], pos["surrogate_d2_mean"], pos["surrogate_d2_std"])
        l1_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_l1 is not None and pos_p_l1 < 0.05) else "IAAFT_LOW_POWER"
        d2_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_d2 is not None and pos_p_d2 < 0.05) else "IAAFT_LOW_POWER"

    neg_p_l1 = neg.get("p_lambda1")
    neg_p_d2 = neg.get("p_d2")
    neg_nonsig_l1 = neg_computable and (neg_p_l1 is None or neg_p_l1 >= 0.05)
    neg_nonsig_d2 = neg_computable and (neg_p_d2 is None or neg_p_d2 >= 0.05)

    results["iaaft_power_check"] = {
        "lambda1_channel": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_lambda1_positive": pos_p_l1 if pos_computable else None,
            "p_lambda1_negative": neg_p_l1,
            "sigma_equivalent_positive": sigma_l1,
            "correctly_nonsignificant_negative": neg_nonsig_l1,
            "verdict": l1_verdict,
        },
        "D2_channel": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_d2_positive": pos_p_d2 if pos_computable else None,
            "p_d2_negative": neg_p_d2,
            "sigma_equivalent_positive": sigma_d2,
            "correctly_nonsignificant_negative": neg_nonsig_d2,
            "verdict": d2_verdict,
        },
        "overall_note": (
            "Both channels share the SAME verdict for positive_control (v1) "
            "because the failure occurs at the shared EMBEDDING step "
            "(tau/m estimated once from PRE via the mandatory FNN hard-"
            "reject gate), which is upstream of and common to lambda_1 and "
            "D2 alike. NOT_COMPUTABLE_EMBEDDING_NOT_RESOLVED means FNN "
            "never dropped below the 1% threshold for ANY m in 1..10 -- so "
            "lambda_1/D2 could not even be computed, let alone tested for "
            "IAAFT power. This is DISTINCT from IAAFT_LOW_POWER."
        ),
    }

    # ---- 4b. Addendum decision rule, applied mechanically to
    # positive_control_v2's result -- FINAL, pre-authorized verdict; no
    # further redesign authorized. ----
    pos2 = results["positive_control_v2_rossler"]
    pos2_computable = pos2["status"] == "ok"

    if not pos2_computable:
        pos2_p_l1 = pos2_p_d2 = None
        sigma_l1_v2 = sigma_d2_v2 = None
        v2_l1_verdict = v2_d2_verdict = "NOT_COMPUTABLE"
    else:
        pos2_p_l1, pos2_p_d2 = pos2["p_lambda1"], pos2["p_d2"]
        sigma_l1_v2 = sigma_equivalent(pos2["delta_lambda1"], pos2["surrogate_lambda1_mean"], pos2["surrogate_lambda1_std"])
        sigma_d2_v2 = sigma_equivalent(pos2["delta_d2"], pos2["surrogate_d2_mean"], pos2["surrogate_d2_std"])
        v2_l1_verdict = "IAAFT_HAS_REAL_POWER" if (pos2_p_l1 is not None and pos2_p_l1 < 0.05) else "IAAFT_LOW_POWER"
        v2_d2_verdict = "IAAFT_HAS_REAL_POWER" if (pos2_p_d2 is not None and pos2_p_d2 < 0.05) else "IAAFT_LOW_POWER"

    any_power_v2 = pos2_computable and (
        (pos2_p_l1 is not None and pos2_p_l1 < 0.05) or
        (pos2_p_d2 is not None and pos2_p_d2 < 0.05)
    )

    final_verdict = "VALIDATION_PASSED_PROCEED_TO_REAL_DATA" if any_power_v2 else \
        "VALIDATION_FAILED_CLOSE_AT_VALIDATION_STAGE_NO_THIRD_ATTEMPT"

    # if v1 actually resolved (did not hit embedding_not_resolved), the
    # Roessler redesign was never triggered/needed -- report that plainly.
    v1_triggered_redesign = (pos["status"] != "ok")

    results["addendum_decision_rossler"] = {
        "description": (
            "Mechanical application of METHODOLOGY_NOTE.md's ONE "
            "pre-authorized additional validation attempt: if EITHER "
            "channel shows p<0.05 with clear null separation, validation "
            "passes; if NEITHER does, close the candidate at the "
            "validation stage without touching real data -- no third "
            "attempt."
        ),
        "v1_hit_embedding_not_resolved_triggering_this_attempt": v1_triggered_redesign,
        "lambda1_channel": {
            "p_lambda1": pos2_p_l1, "sigma_equivalent": sigma_l1_v2,
            "significant_at_0.05": pos2_computable and pos2_p_l1 is not None and pos2_p_l1 < 0.05,
            "verdict": v2_l1_verdict,
        },
        "D2_channel": {
            "p_d2": pos2_p_d2, "sigma_equivalent": sigma_d2_v2,
            "significant_at_0.05": pos2_computable and pos2_p_d2 is not None and pos2_p_d2 < 0.05,
            "verdict": v2_d2_verdict,
        },
        "any_channel_shows_power": any_power_v2,
        "final_verdict": final_verdict,
    }

    results["pipeline_config"] = (
        pos_result["config"] if pos_result["status"] == "ok" else neg_result["config"]
    )
    results["wall_clock_seconds_total"] = time.time() - t_start

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results["iaaft_power_check"], indent=2))
    print(json.dumps(results["structural_wall_characterization"]["bootstrap_on_white_noise"], indent=2))
    print(json.dumps(results["addendum_decision_rossler"], indent=2))
    print(f"\nWrote {out_path}")
    print(f"Total wall clock: {results['wall_clock_seconds_total']:.1f}s")


if __name__ == "__main__":
    main()
