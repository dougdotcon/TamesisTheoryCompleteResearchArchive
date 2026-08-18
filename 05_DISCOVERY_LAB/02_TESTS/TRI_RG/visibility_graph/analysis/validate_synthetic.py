"""
Synthetic validation of `vg_common.py`, run and committed BEFORE any real
PRE/POST segment (geomagnetic storm 17/03/2015, Hurricane Harvey/2017
hydrology) is touched -- required by METHODOLOGY_NOTE.md Gap (b)
"Validacao obrigatoria de PODER, ANTES de qualquer dado real": since IAAFT
is the PRIMARY significance test for this candidate (Gap (e)), this script
must confirm IAAFT has real power to detect a genuine nonlinear change in
d_B/C before the pipeline can be applied to real data -- exactly the same
requirement already used for `mse_multiscale_entropy` in this lab.

Four checks, all synthetic, all seeded for reproducibility:

0. Box-covering CODE-CORRECTNESS diagnostic (NOT part of the identifiability
   validation itself, reported separately and clearly labeled as
   supplementary): a deterministic sawtooth/ramp series is used because
   pure near-collinear stretches suppress visibility-graph hub formation
   and (unlike stochastic noise) reliably produce a large graph diameter,
   letting N_B(l_B) actually be computed across >=4 scales so the OLS
   log-log fit and the CBB seed-radius-burning implementation can be sanity
   checked (N_B monotonically non-increasing in l_B; d_B > 0) at all. This
   check exists because of finding (*) below: realistic stochastic PRE/POST
   series essentially never reach that regime.

(*) Structural finding, discovered BY this validation, not assumed: natural
    visibility graphs of stochastic (noise-like/chaotic) time series are
    strongly small-world -- their diameter grows only ~log(N) (empirically
    9-17 for N in [1000, 15000] across white noise, AR(1), fGn H up to 0.95,
    random walk, logistic map r=4) because a landscape's global extrema act
    as visibility hubs. METHODOLOGY_NOTE.md Gap (a) requires
    l_B_max=floor(diam(G)/4) >= 5 (i.e. diam(G) >= 20) for the >=4-scale
    floor to be met. Under Gap (d)'s MAX_N_PER_SEGMENT=5000 cap, this is
    essentially never reached for the stochastic process families used in
    checks 1-2 below (diam stays roughly 10-19 even at N=5000). This is
    reported honestly as a finding of THIS validation, not smoothed over --
    see VALIDATION_NOTE.md for the full discussion and its consequence for
    the d_B channel specifically (distinct from, and more fundamental than,
    a low-IAAFT-power problem: d_B is not merely underpowered here, it is
    typically NOT COMPUTABLE at realistic N under Gap (a)'s own grid rule).

1. Positive control -- the central identifiability test for this candidate,
   EXACTLY as specified in METHODOLOGY_NOTE.md Gap (b): PRE = white Gaussian
   noise. POST = logistic map (r=4, fully chaotic) rank-remapped onto PRE's
   own exact empirical distribution (same technique validated in
   mse_multiscale_entropy/analysis/validate_synthetic.py) so PRE and POST
   share an EXACTLY identical marginal, and (empirically, via the same
   periodogram-slope diagnostic used there) closely matched flat spectra.
   IAAFT surrogates preserve spectrum+marginal but destroy the logistic
   map's determinism; if C/d_B respond to that determinism specifically,
   the real Delta should sit outside the IAAFT null (p small).

2. Negative control: PRE and POST = two INDEPENDENT realizations of the SAME
   linear process (fGn, fixed H=0.7, independent seeds) -- probes Gap (b)'s
   named redundancy risk (visibility-graph d_B as a monotone reparametrization
   of Hurst H) directly: same H, no genuine structural change, p should be
   typically non-significant for both channels.

3. IAAFT power-check verdict (positive vs negative control), reported
   PER CHANNEL (d_B, C) separately per the task's explicit requirement, plus
   the box-covering scale-achievability diagnostic that explains why d_B's
   verdict may be "not computable" rather than "not significant".

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vg_common import (
    run_vg_analysis, compute_vg_features, fit_d_b, build_visibility_graph,
    all_pairs_shortest_path, graph_diameter, l_b_grid, N_SURROGATES, N_IAAFT_ITER, SEED,
)


# --------------------------------------------------------------------------
# Synthetic generators (independent implementation for this test line, same
# spirit/technique as mse_multiscale_entropy's validate_synthetic.py but not
# imported from it)
# --------------------------------------------------------------------------

def colored_noise(n, spectral_exponent, rng):
    """Gaussian colored noise, PSD ~ 1/f^exponent, FFT-filtering spectral
    synthesis. exponent=0 ~ white noise. Used here as an fGn-like generator:
    an fGn of Hurst exponent H has PSD ~ f^-(2H+1), so exponent=2H+1
    approximates fGn with that H (standard spectral-synthesis approximation,
    same technique as mse_multiscale_entropy's validate_synthetic.py, not a
    literal Davies-Harte exact-covariance fGn generator)."""
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


def sawtooth_ramp(n, n_teeth, rng, noise_frac=0.0):
    """Deterministic piecewise-linear sawtooth: n_teeth linear ramps of
    equal length, each from 0 to 1. Used ONLY for the box-covering
    code-correctness diagnostic (check 0) -- near-collinear stretches
    suppress visibility-graph hub formation, reliably yielding a large
    diameter unlike stochastic noise (see module docstring finding (*)).
    """
    teeth_len = n // n_teeth
    ramp = np.tile(np.linspace(0.0, 1.0, teeth_len, endpoint=False), n_teeth)
    ramp = np.concatenate([ramp, np.linspace(0.0, 1.0, n - len(ramp))])
    if noise_frac > 0:
        ramp = ramp + noise_frac * rng.standard_normal(n)
    return ramp


# --------------------------------------------------------------------------
# Reporting helpers
# --------------------------------------------------------------------------

def _pipeline_summary(result, extra=None):
    d = {
        "d_B_pre": result["d_B_pre"],
        "d_B_post": result["d_B_post"],
        "C_pre": result["C_pre"],
        "C_post": result["C_post"],
        "delta_d_B": result["delta_d_B"],
        "delta_C": result["delta_C"],
        "p_d_B": result["p_d_B"],
        "p_C": result["p_C"],
        "surrogate_d_B_mean": result["surrogate_d_B_mean"],
        "surrogate_d_B_std": result["surrogate_d_B_std"],
        "surrogate_d_B_n_valid": result["surrogate_d_B_n_valid"],
        "surrogate_d_B_n_undefined": result["surrogate_d_B_n_undefined"],
        "surrogate_C_mean": result["surrogate_C_mean"],
        "surrogate_C_std": result["surrogate_C_std"],
        "surrogate_C_n_valid": result["surrogate_C_n_valid"],
        "surrogate_C_n_undefined": result["surrogate_C_n_undefined"],
        "diagnostics": result["diagnostics"],
        "real_pre_diam": result["real_pre"]["diam"],
        "real_post_diam": result["real_post"]["diam"],
        "real_pre_status": result["real_pre"]["status"],
        "real_post_status": result["real_post"]["status"],
        "real_pre_l_B_grid": result["real_pre"]["l_B_grid"],
        "real_post_l_B_grid": result["real_post"]["l_B_grid"],
    }
    if "delta_d_B_boot_ci95" in result:
        d["bootstrap"] = {
            "delta_d_B_boot_ci95": result["delta_d_B_boot_ci95"],
            "p_bootstrap_d_B": result["p_bootstrap_d_B"],
            "delta_d_B_boot_n_valid": result["delta_d_B_boot_n_valid"],
            "delta_C_boot_ci95": result["delta_C_boot_ci95"],
            "p_bootstrap_C": result["p_bootstrap_C"],
            "delta_C_boot_n_valid": result["delta_C_boot_n_valid"],
        }
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

    # ---- 0. Box-covering code-correctness diagnostic (supplementary, NOT
    # part of the identifiability validation -- see module docstring) ----
    rng0 = np.random.default_rng(909)
    N_DIAG = 2000
    sawtooth = sawtooth_ramp(N_DIAG, n_teeth=1, rng=rng0, noise_frac=0.0)  # pure ramp
    adj, n_edges = build_visibility_graph(sawtooth)
    D = all_pairs_shortest_path(adj)
    diam, conn_info = graph_diameter(D)
    scales, l_b_max, grid_status = l_b_grid(diam) if diam is not None else (np.array([]), None, "disconnected")
    diag_feat = compute_vg_features(sawtooth, seed=SEED)
    n_b = diag_feat["N_B_median"]
    monotone_nonincreasing = bool(n_b == sorted(n_b, reverse=True)) if n_b else None
    results["box_covering_code_diagnostic"] = {
        "description": (
            "Deterministic pure linear ramp, N=2000 (near-collinear series "
            "suppress visibility-graph hub formation and reliably produce a "
            "large diameter, unlike stochastic noise -- see finding (*) in "
            "the module docstring). NOT a PRE/POST identifiability test; "
            "exists only to confirm the box-covering/CBB/OLS-fit code "
            "produces a sane result AT ALL when the l_B grid is achievable."
        ),
        "n_samples": N_DIAG,
        "n_edges": n_edges,
        "diam": diam,
        "l_B_max": l_b_max,
        "grid_status": grid_status,
        "status": diag_feat["status"],
        "l_B_grid": diag_feat["l_B_grid"],
        "N_B_median": diag_feat["N_B_median"],
        "d_B": diag_feat["d_B"],
        "C": diag_feat["C"],
        "N_B_monotone_nonincreasing_in_l_B": monotone_nonincreasing,
    }

    # ---- 1. Positive control: PRE = white Gaussian noise, POST = logistic
    # map (r=4) rank-remapped onto PRE's exact marginal -- EXACT
    # METHODOLOGY_NOTE.md Gap (b) specification. ----
    N_CTRL = 2000
    rng_pos = np.random.default_rng(424242)
    pos_pre = rng_pos.standard_normal(N_CTRL)
    logi_raw = logistic_map(N_CTRL, x0=0.234567891, r=4.0, burn_in=500)
    pos_post = rank_remap_to_reference(logi_raw, pos_pre)

    pos_spec_pre = estimate_spectral_exponent(pos_pre)
    pos_spec_post = estimate_spectral_exponent(pos_post)

    t0 = time.time()
    pos_result = run_vg_analysis(pos_pre, pos_post, seed=SEED)
    t_pos = time.time() - t0

    results["positive_control"] = _pipeline_summary(
        pos_result,
        extra={
            "description": (
                "PRE = iid Gaussian white noise (linear). POST = logistic map "
                "(r=4, fully chaotic, genuine deterministic nonlinear process), "
                "rank-remapped onto PRE's own sorted values so PRE and POST "
                "share an EXACTLY identical empirical marginal by construction. "
                "Amplitude-spectrum match documented empirically via "
                "periodogram-slope spectral_exponent (both near-flat)."
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
    # named Hurst-redundancy risk directly. ----
    N_NEG = N_CTRL
    rng_neg_pre = np.random.default_rng(555001)
    rng_neg_post = np.random.default_rng(555002)
    neg_pre = fgn_like(N_NEG, H=0.7, rng=rng_neg_pre)
    neg_post = fgn_like(N_NEG, H=0.7, rng=rng_neg_post)

    t0 = time.time()
    neg_result = run_vg_analysis(neg_pre, neg_post, seed=SEED)
    t_neg = time.time() - t0

    results["negative_control"] = _pipeline_summary(
        neg_result,
        extra={
            "description": (
                "PRE and POST = two INDEPENDENT realizations of the SAME "
                "linear process (fGn-like spectral-synthesis generator, fixed "
                "H=0.7, independent seeds 555001/555002). Probes "
                "METHODOLOGY_NOTE.md Gap (b)'s named risk directly: same "
                "Hurst structure, no genuine change -- p should typically be "
                "non-significant for both channels."
            ),
            "n_pre": N_NEG, "n_post": N_NEG,
            "wall_clock_seconds": t_neg,
        },
    )

    # ---- 3. IAAFT power-check verdict, PER CHANNEL (task requirement:
    # report d_B and C power separately, do not force a pass). ----
    pos = results["positive_control"]
    neg = results["negative_control"]

    pos_dB_computable = pos["real_pre_status"] == "ok" and pos["real_post_status"] == "ok"
    neg_dB_computable = neg["real_pre_status"] == "ok" and neg["real_post_status"] == "ok"

    pos_p_dB, pos_p_C = pos["p_d_B"], pos["p_C"]
    neg_p_dB, neg_p_C = neg["p_d_B"], neg["p_C"]

    pos_sig_dB = pos_p_dB is not None and pos_p_dB < 0.05
    pos_sig_C = pos_p_C is not None and pos_p_C < 0.05
    neg_nonsig_dB = neg_p_dB is None or neg_p_dB >= 0.05
    neg_nonsig_C = neg_p_C is None or neg_p_C >= 0.05

    sigma_dB = sigma_equivalent(pos["delta_d_B"], pos["surrogate_d_B_mean"], pos["surrogate_d_B_std"])
    sigma_C = sigma_equivalent(pos["delta_C"], pos["surrogate_C_mean"], pos["surrogate_C_std"])

    if not pos_dB_computable:
        dB_verdict = "NOT_COMPUTABLE_INSUFFICIENT_SCALES"
    elif pos_sig_dB:
        dB_verdict = "IAAFT_HAS_REAL_POWER"
    else:
        dB_verdict = "IAAFT_LOW_POWER"

    C_verdict = "IAAFT_HAS_REAL_POWER" if pos_sig_C else "IAAFT_LOW_POWER"

    results["iaaft_power_check"] = {
        "d_B_channel": {
            "positive_control_computable": pos_dB_computable,
            "negative_control_computable": neg_dB_computable,
            "p_d_B_positive": pos_p_dB,
            "p_d_B_negative": neg_p_dB,
            "sigma_equivalent_positive": sigma_dB,
            "significant_at_0.05_positive": pos_sig_dB,
            "correctly_nonsignificant_negative": neg_nonsig_dB,
            "verdict": dB_verdict,
        },
        "C_channel": {
            "p_C_positive": pos_p_C,
            "p_C_negative": neg_p_C,
            "sigma_equivalent_positive": sigma_C,
            "significant_at_0.05_positive": pos_sig_C,
            "correctly_nonsignificant_negative": neg_nonsig_C,
            "verdict": C_verdict,
        },
        "overall_note": (
            "d_B verdict of NOT_COMPUTABLE_INSUFFICIENT_SCALES is DISTINCT from "
            "IAAFT_LOW_POWER: it means METHODOLOGY_NOTE.md Gap (a)'s own scale-grid "
            "requirement (>=4 distinct l_B, i.e. diam(G)>=20) was not met for this "
            "process/N at all, so no p-value could be formed -- not that d_B was "
            "computed but the IAAFT null failed to separate from it. See "
            "VALIDATION_NOTE.md for the full discussion and why the moving-block "
            "bootstrap fallback (pre-authorized in METHODOLOGY_NOTE.md Gap (e) for a "
            "LOW-POWER IAAFT finding) does not, by itself, resolve a "
            "NOT_COMPUTABLE finding: bootstrap resamples of the SAME real segment "
            "have essentially the same length/diameter distribution as the "
            "original, so they hit the identical insufficient-scales rejection."
        ),
    }

    results["pipeline_config"] = pos_result["config"]
    results["generator_notes"] = {
        "colored_noise_fgn_like": (
            "FFT-filtering spectral synthesis: white Gaussian noise scaled "
            "per-frequency by f^(-exponent/2), inverse-transformed, z-scored. "
            "fGn-like approximation via exponent=2H+1 (spectral relation for "
            "fractional Gaussian noise); same technique as "
            "mse_multiscale_entropy/analysis/validate_synthetic.py, "
            "independent implementation."
        ),
        "logistic_map": "x_{k+1} = 4*x_k*(1-x_k), burn_in=500 discarded transient iterations.",
        "rank_remap": (
            "POST = sorted(PRE)[argsort(argsort(logistic_map_raw))] -- POST is "
            "an exact permutation of PRE's own values, reordered by the "
            "logistic map's temporal rank structure."
        ),
        "sawtooth_ramp": (
            "Deterministic piecewise-linear ramp(s) 0->1, used ONLY for the "
            "box-covering code-correctness diagnostic (check 0), not a "
            "PRE/POST identifiability control."
        ),
    }
    results["wall_clock_seconds_total"] = time.time() - t_start

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results["iaaft_power_check"], indent=2))
    print(f"\nWrote {out_path}")
    print(f"Total wall clock: {results['wall_clock_seconds_total']:.1f}s")


if __name__ == "__main__":
    main()
