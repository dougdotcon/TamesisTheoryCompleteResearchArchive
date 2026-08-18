"""
Synthetic validation of `rqa_common.py`, run and committed BEFORE any real
PRE/POST segment (NASA PCoE IMS/Rexnord bearing run-to-failure, Kilauea
2018 volcanic seismology) is touched -- required by METHODOLOGY_NOTE.md
Gap (b) "Validacao obrigatoria de PODER, ANTES de qualquer dado real":
since IAAFT is the PRIMARY significance test for this candidate (Gap (e)),
this script must confirm IAAFT has real power to detect a genuine
nonlinear change in %DET/ENTR before the pipeline can be applied to real
data -- exactly the same requirement already used for
`mse_multiscale_entropy` and `visibility_graph` in this lab.

Checks, all synthetic, all seeded for reproducibility:

0. Embedding+recurrence CODE-CORRECTNESS diagnostic (NOT part of the
   identifiability validation itself, reported separately and clearly
   labeled as supplementary): a clean deterministic sine wave with a tiny
   (1e-6 relative) dither is used. The dither is necessary and explained
   here rather than left implicit: a PERFECTLY periodic, floating-point-
   exact sine wave produces many embedded points that coincide up to
   machine precision (period 50 recurs exactly every cycle at N=1000,
   20 cycles), which makes the FNN R_tol ratio criterion
   (|ext_diff|/R_i^m > R_tol) blow up on ~1e-16-scale denominators --
   division-by-near-zero numerical noise, not a real dynamical signal. A
   1e-6 relative dither breaks these exact coincidences while leaving the
   signal's genuine dynamics (and its true, small, m=2 attractor
   dimension) intact, and is standard practice for this exact reason. This
   lets FNN cleanly resolve a small m and %DET come out near 1.0,
   confirming the pipeline's code is right before testing it on genuinely
   ambiguous stochastic data (mirrors how `visibility_graph`'s validation
   used a deterministic ramp for exactly this purpose).

1. Positive control -- the central identifiability test for this
   candidate, EXACTLY as specified in METHODOLOGY_NOTE.md Gap (b): PRE =
   white Gaussian noise. POST = logistic map (r=4, fully chaotic) rank-
   remapped onto PRE's own exact empirical distribution (same technique
   validated in mse_multiscale_entropy/analysis/validate_synthetic.py and
   visibility_graph/analysial/validate_synthetic.py) so PRE and POST share
   an EXACTLY identical marginal, and (by construction, both being near-
   broadband/near-flat-spectrum processes) closely matched spectra.
   IAAFT surrogates preserve spectrum+marginal but destroy the logistic
   map's determinism; if %DET/ENTR respond to that determinism
   specifically, the real Delta should sit outside the IAAFT null (p
   small). *** THIS CHECK IS WHERE THE STRUCTURAL FINDING OF THIS
   VALIDATION SHOWS UP -- see module-level and VALIDATION_NOTE.md
   discussion: white noise never resolves FNN<1% for any m<=10, so the
   shared-embedding step itself fails for PRE before %DET/ENTR can even be
   computed. ***

1b. Positive control v2 (Roessler-sourced POST) -- the ONE additional
   validation attempt pre-authorized in METHODOLOGY_NOTE.md's addendum
   (commit 024e7a9) after check 1 above hit embedding_not_resolved: same
   PRE (fGn-like H=0.7, already confirmed to resolve FNN), POST = Roessler
   system x-coordinate (colored/band-limited spectrum, closer to fGn's
   than the logistic map's near-white spectrum) rank-remapped onto PRE.
   Decision rule fixed a priori: p<0.05 with clear null separation on
   EITHER channel -> validation passes; neither -> RQA closed at the
   validation stage, no third attempt.

2. Negative control: PRE and POST = two INDEPENDENT realizations of the
   SAME linear process (fGn-like, fixed H=0.7, independent seeds) --
   probes Gap (b)'s named spectral/linear-risk directly: same H, no
   genuine structural change, p should be typically non-significant for
   both channels. This process DOES resolve FNN cleanly (fGn H=0.7 has
   real, if linear, autocorrelation structure), so this check exercises
   the full pipeline end-to-end including IAAFT.

3. Structural-wall characterization (supplementary, NOT required by
   METHODOLOGY_NOTE.md but run to explicitly test rather than assume,
   per task instructions): (a) an fGn-H / AR(1)-phi sweep showing exactly
   where the FNN-resolvability boundary sits (whiter than H~=0.2 / phi<0.9
   never resolves at N in [2000,5000]); (b) an explicit moving-block-
   bootstrap check on white noise itself (25 resamples) -- pre-authorized
   in METHODOLOGY_NOTE.md Gap (e) as a fallback for a LOW-POWER IAAFT
   finding, tested here to confirm (not assume) that it does NOT resolve a
   STRUCTURAL non-computability finding, mirroring
   `visibility_graph/VALIDATION_NOTE.md`'s reasoning for why bootstrap did
   not fix d_B's analogous problem there.

4. IAAFT power-check verdict, reported per channel, PLUS the embedding-
   resolvability diagnostic that explains why the literal Gap (b) positive
   control could not be run to completion.

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rqa_common import (
    run_rqa_analysis, estimate_tau, estimate_m, compute_rqa_features,
    moving_block_bootstrap_resample, N_SURROGATES, N_IAAFT_ITER, SEED,
)


# --------------------------------------------------------------------------
# Synthetic generators (independent implementation for this test line, same
# spirit/technique as mse_multiscale_entropy's and visibility_graph's
# validate_synthetic.py but not imported from them)
# --------------------------------------------------------------------------

def colored_noise(n, spectral_exponent, rng):
    """Gaussian colored noise, PSD ~ 1/f^exponent, FFT-filtering spectral
    synthesis. exponent=0 ~ white noise. Used here as an fGn-like generator:
    an fGn of Hurst exponent H has PSD ~ f^-(2H+1), so exponent=2H+1
    approximates fGn with that H (standard spectral-synthesis approximation,
    same technique as mse_multiscale_entropy's / visibility_graph's
    validate_synthetic.py, not a literal Davies-Harte exact-covariance fGn
    generator)."""
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


def ar1_process(n, phi, rng):
    e = rng.standard_normal(n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def rossler_x(n_out, sample_dt=0.15, dt_internal=0.01, a=0.2, b=0.2, c=5.7,
              burn_in_time=200.0, x0=(1.0, 1.0, 1.0)):
    """Roessler system (Roessler 1976, Phys. Lett. A 57:397), classic
    chaotic parameters a=0.2, b=0.2, c=5.7, RK4 integration with a fine
    internal step (dt_internal=0.01, standard/sufficient for this system),
    decimated to sample_dt after a burn-in transient. Returns the x-
    coordinate only (n_out samples).

    sample_dt=0.15 was chosen (see METHODOLOGY_NOTE.md addendum rationale
    and VALIDATION_NOTE.md diagnostic table) because it empirically gives a
    periodogram-slope spectral exponent (~2.4) close to fGn H=0.7's target
    exponent (2*H+1=2.4) -- i.e. this sampling rate is what makes Roessler's
    natural colored/band-limited spectrum resemble the fGn PRE's spectrum
    BEFORE any rank-remap is applied, addressing the exact spectral-mismatch
    confound found with the logistic map in the original Gap (b) design.
    """
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
    """Clean deterministic sine wave with a tiny relative dither -- see
    module docstring check 0 for why the dither is necessary (breaks
    floating-point-exact recurrences that spuriously blow up FNN's ratio
    criterion on near-zero denominators)."""
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
            "DET_pre": result["DET_pre"], "DET_post": result["DET_post"],
            "ENTR_pre": result["ENTR_pre"], "ENTR_post": result["ENTR_post"],
            "delta_DET": result["delta_DET"], "delta_ENTR": result["delta_ENTR"],
            "p_DET": result["p_DET"], "p_ENTR": result["p_ENTR"],
            "surrogate_DET_mean": result["surrogate_DET_mean"],
            "surrogate_DET_std": result["surrogate_DET_std"],
            "surrogate_DET_n_valid": result["surrogate_DET_n_valid"],
            "surrogate_DET_n_undefined": result["surrogate_DET_n_undefined"],
            "surrogate_ENTR_mean": result["surrogate_ENTR_mean"],
            "surrogate_ENTR_std": result["surrogate_ENTR_std"],
            "surrogate_ENTR_n_valid": result["surrogate_ENTR_n_valid"],
            "surrogate_ENTR_n_undefined": result["surrogate_ENTR_n_undefined"],
            "diagnostics": result["diagnostics"],
            "real_pre_epsilon": result["real_pre"]["epsilon"],
            "real_post_epsilon": result["real_post"]["epsilon"],
            "real_pre_achieved_rr": result["real_pre"]["achieved_rr"],
            "real_post_achieved_rr": result["real_post"]["achieved_rr"],
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

    # ---- 0. Embedding+recurrence code-correctness diagnostic (NOT part of
    # the identifiability validation -- see module docstring) ----
    rng0 = np.random.default_rng(909)
    N_DIAG = 1000
    sine = sine_with_dither(N_DIAG, period=50, dither_frac=1e-6, rng=rng0)
    tau_diag = estimate_tau(sine)
    m_diag = estimate_m(sine, tau_diag["tau"]) if tau_diag["status"] == "ok" else None
    feat_diag = (compute_rqa_features(sine, m_diag["m"], tau_diag["tau"])
                 if (m_diag is not None and m_diag["status"] == "ok") else None)
    results["code_correctness_diagnostic"] = {
        "description": (
            "Deterministic sine wave (period=50), N=1000, with a tiny "
            "(1e-6 relative) Gaussian dither to break floating-point-exact "
            "recurrences (see module docstring check 0 for why the dither "
            "is necessary). NOT a PRE/POST identifiability test; exists "
            "only to confirm the embedding/FNN/recurrence-matrix/%DET/ENTR "
            "code produces a sane result (small resolved m, %DET near 1.0) "
            "on unambiguous deterministic dynamics before testing on "
            "genuinely ambiguous stochastic data."
        ),
        "n_samples": N_DIAG,
        "tau": tau_diag,
        "m": (None if m_diag is None else
              {k: v for k, v in m_diag.items() if k != "fnn_curve"}),
        "fnn_curve": (None if m_diag is None else
                      [{"m": r["m"], "fraction": r.get("fraction")} for r in m_diag["fnn_curve"]]),
        "features": feat_diag,
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
    pos_result = run_rqa_analysis(pos_pre, pos_post, seed=SEED)
    t_pos = time.time() - t0

    results["positive_control"] = _pipeline_summary(
        pos_result,
        extra={
            "description": (
                "PRE = iid Gaussian white noise (linear, zero autocorrelation). "
                "POST = logistic map (r=4, fully chaotic, genuine deterministic "
                "nonlinear process), rank-remapped onto PRE's own sorted values "
                "so PRE and POST share an EXACTLY identical empirical marginal "
                "by construction. Amplitude-spectrum match documented "
                "empirically via periodogram-slope spectral_exponent (both "
                "near-flat, as expected for two broadband processes)."
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
    # named spectral/linear risk directly, and (unlike white noise) DOES
    # resolve FNN, so exercises the full pipeline end-to-end. ----
    N_NEG = N_CTRL
    rng_neg_pre = np.random.default_rng(555001)
    rng_neg_post = np.random.default_rng(555002)
    neg_pre = fgn_like(N_NEG, H=0.7, rng=rng_neg_pre)
    neg_post = fgn_like(N_NEG, H=0.7, rng=rng_neg_post)

    t0 = time.time()
    neg_result = run_rqa_analysis(neg_pre, neg_post, seed=SEED)
    t_neg = time.time() - t0

    results["negative_control"] = _pipeline_summary(
        neg_result,
        extra={
            "description": (
                "PRE and POST = two INDEPENDENT realizations of the SAME "
                "linear process (fGn-like spectral-synthesis generator, fixed "
                "H=0.7, independent seeds 555001/555002). Probes "
                "METHODOLOGY_NOTE.md Gap (b)'s named spectral/linear risk "
                "directly: same autocorrelation structure, no genuine change "
                "-- p should typically be non-significant for both channels. "
                "H=0.7 was chosen (rather than H=0 white noise) specifically "
                "because it DOES resolve FNN (see structural_wall_characterization "
                "below), letting this check exercise the complete pipeline."
            ),
            "n_pre": N_NEG, "n_post": N_NEG,
            "wall_clock_seconds": t_neg,
        },
    )

    # ---- 1b. Positive control v2 -- Roessler-sourced POST (METHODOLOGY_NOTE.md
    # addendum, commit 024e7a9, the ONE pre-authorized additional validation
    # attempt after positive_control (v1, above) hit embedding_not_resolved
    # for its white-noise PRE). PRE = fGn-like H=0.7 (unchanged, already
    # validated to resolve FNN cleanly in the negative control above). POST =
    # Roessler system x-coordinate, rank-remapped onto PRE's exact marginal
    # -- same rank-remap technique, only the chaotic SOURCE for POST changes
    # (logistic map's near-white spectrum -> Roessler's colored/band-limited
    # spectrum, closer in character to fGn). Fixed a priori decision rule
    # (addendum steps 4-5): if EITHER channel shows p<0.05 with clear null
    # separation, validation passes under this corrected design; if NEITHER
    # does, RQA is closed at the validation stage -- no third attempt. ----
    rng_pos2_pre = np.random.default_rng(424242)
    pos2_pre = fgn_like(N_CTRL, H=0.7, rng=rng_pos2_pre)
    rossler_raw = rossler_x(N_CTRL, sample_dt=0.15)
    pos2_post = rank_remap_to_reference(rossler_raw, pos2_pre)

    pos2_spec_pre = estimate_spectral_exponent(pos2_pre)
    pos2_spec_post = estimate_spectral_exponent(pos2_post)
    pos2_spec_rossler_raw = estimate_spectral_exponent(rossler_raw)

    t0 = time.time()
    pos2_result = run_rqa_analysis(pos2_pre, pos2_post, seed=SEED)
    t_pos2 = time.time() - t0

    results["positive_control_v2_rossler"] = _pipeline_summary(
        pos2_result,
        extra={
            "description": (
                "METHODOLOGY_NOTE.md addendum (commit 024e7a9), the ONE "
                "pre-authorized additional validation attempt. PRE = fGn-like "
                "H=0.7 (same generator/technique as the negative control, "
                "already confirmed to resolve FNN). POST = Roessler system "
                "(a=0.2, b=0.2, c=5.7, classic chaotic regime, RK4 "
                "integration dt_internal=0.01, sampled at dt=0.15) x-"
                "coordinate, rank-remapped onto PRE's exact empirical "
                "distribution. Spectral match reported honestly (periodogram-"
                "slope diagnostic), not required to be perfect per the "
                "addendum's own instruction."
            ),
            "n_pre": N_CTRL, "n_post": N_CTRL,
            "spectral_exponent_pre": pos2_spec_pre,
            "spectral_exponent_post": pos2_spec_post,
            "spectral_exponent_rossler_raw_pre_remap": pos2_spec_rossler_raw,
            "spectral_exponent_target_fgn_H0.7": 2 * 0.7 + 1,
            "marginal_match": "exact (rank-remap of POST onto PRE's sorted values)",
            "rossler_params": {"a": 0.2, "b": 0.2, "c": 5.7, "sample_dt": 0.15,
                                "dt_internal": 0.01, "burn_in_time": 200.0},
            "wall_clock_seconds": t_pos2,
        },
    )

    # ---- 3. Structural-wall characterization (supplementary): (a) fGn-H /
    # AR(1)-phi resolvability sweep, (b) explicit bootstrap-on-white-noise
    # check -- both run to TEST, not assume, per task instructions. ----
    sweep_fgn = []
    for H in [0.1, 0.3, 0.5, 0.6, 0.7, 0.9]:
        rng_h = np.random.default_rng(100 + int(H * 10))
        x = fgn_like(N_CTRL, H, rng_h)
        tau_i = estimate_tau(x)
        m_i = estimate_m(x, tau_i["tau"]) if tau_i["status"] == "ok" else {"status": "tau_failed"}
        sweep_fgn.append({"H": H, "tau": tau_i.get("tau"), "m_status": m_i["status"],
                           "m": m_i.get("m")})

    sweep_ar1 = []
    for phi in [0.0, 0.3, 0.5, 0.7, 0.9, 0.95]:
        rng_p = np.random.default_rng(200 + int(phi * 10))
        x = ar1_process(N_CTRL, phi, rng_p)
        tau_i = estimate_tau(x)
        m_i = estimate_m(x, tau_i["tau"]) if tau_i["status"] == "ok" else {"status": "tau_failed"}
        sweep_ar1.append({"phi": phi, "tau": tau_i.get("tau"), "m_status": m_i["status"],
                           "m": m_i.get("m")})

    # N-independence check for the white-noise wall (Gap (d)'s MAX_N=5000 ceiling)
    sweep_n = []
    for N_test in [2000, 5000]:
        for seed_test in [11, 12]:
            rng_n = np.random.default_rng(seed_test)
            x = rng_n.standard_normal(N_test)
            tau_i = estimate_tau(x)
            m_i = estimate_m(x, tau_i["tau"])
            min_frac = min((r.get("fraction") for r in m_i["fnn_curve"]
                             if r.get("fraction") is not None), default=None)
            sweep_n.append({"N": N_test, "seed": seed_test, "tau": tau_i["tau"],
                             "m_status": m_i["status"], "min_fnn_fraction_seen": min_frac})

    # Explicit bootstrap-on-white-noise check (pre-authorized fallback,
    # tested directly rather than assumed not to help)
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
            "Supplementary checks (not required by METHODOLOGY_NOTE.md, run "
            "to directly TEST the positive control's embedding_not_resolved "
            "finding above rather than leaving it unexplained): (a) an fGn-H "
            "/ AR(1)-phi sweep locating the FNN-resolvability boundary; (b) "
            "confirmation the wall is N-independent within the Gap (d) "
            "MAX_N_PER_SEGMENT=5000 ceiling (more data does not help); (c) an "
            "explicit test of whether the Gap (e) moving-block-bootstrap "
            "fallback resolves it (it does not, tested not assumed -- see "
            "VALIDATION_NOTE.md)."
        ),
        "fgn_H_sweep_N2000": sweep_fgn,
        "ar1_phi_sweep_N2000": sweep_ar1,
        "white_noise_N_independence_check": sweep_n,
        "bootstrap_on_white_noise": {
            "n_bootstrap_resamples_tested": n_boot_checks,
            "n_resolved_embedding": n_resolved,
            "block_length_L": 20,
            "verdict": (
                "BOOTSTRAP_DOES_NOT_RESOLVE" if n_resolved == 0 else
                f"BOOTSTRAP_PARTIALLY_RESOLVES ({n_resolved}/{n_boot_checks})"
            ),
            "details_first_5": boot_details[:5],
        },
    }

    # ---- 4. IAAFT power-check verdict, PER CHANNEL. ----
    pos = results["positive_control"]
    neg = results["negative_control"]

    pos_computable = pos["status"] == "ok"
    neg_computable = neg["status"] == "ok"

    if not pos_computable:
        dET_verdict = "NOT_COMPUTABLE_EMBEDDING_NOT_RESOLVED"
        entr_verdict = "NOT_COMPUTABLE_EMBEDDING_NOT_RESOLVED"
        sigma_DET = sigma_ENTR = None
        pos_p_DET = pos_p_ENTR = None
    else:
        pos_p_DET, pos_p_ENTR = pos["p_DET"], pos["p_ENTR"]
        sigma_DET = sigma_equivalent(pos["delta_DET"], pos["surrogate_DET_mean"], pos["surrogate_DET_std"])
        sigma_ENTR = sigma_equivalent(pos["delta_ENTR"], pos["surrogate_ENTR_mean"], pos["surrogate_ENTR_std"])
        dET_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_DET is not None and pos_p_DET < 0.05) else "IAAFT_LOW_POWER"
        entr_verdict = "IAAFT_HAS_REAL_POWER" if (pos_p_ENTR is not None and pos_p_ENTR < 0.05) else "IAAFT_LOW_POWER"

    neg_p_DET = neg.get("p_DET")
    neg_p_ENTR = neg.get("p_ENTR")
    neg_nonsig_DET = neg_computable and (neg_p_DET is None or neg_p_DET >= 0.05)
    neg_nonsig_ENTR = neg_computable and (neg_p_ENTR is None or neg_p_ENTR >= 0.05)

    results["iaaft_power_check"] = {
        "DET_channel": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_DET_positive": pos_p_DET if pos_computable else None,
            "p_DET_negative": neg_p_DET,
            "sigma_equivalent_positive": sigma_DET,
            "correctly_nonsignificant_negative": neg_nonsig_DET,
            "verdict": dET_verdict,
        },
        "ENTR_channel": {
            "positive_control_computable": pos_computable,
            "negative_control_computable": neg_computable,
            "p_ENTR_positive": pos_p_ENTR if pos_computable else None,
            "p_ENTR_negative": neg_p_ENTR,
            "sigma_equivalent_positive": sigma_ENTR,
            "correctly_nonsignificant_negative": neg_nonsig_ENTR,
            "verdict": entr_verdict,
        },
        "overall_note": (
            "Both channels share the SAME verdict here because the failure "
            "occurs at the shared EMBEDDING step (tau/m estimated once from "
            "PRE), which is upstream of and common to %DET and ENTR alike -- "
            "unlike visibility_graph's single-channel (d_B only) finding. "
            "NOT_COMPUTABLE_EMBEDDING_NOT_RESOLVED means False Nearest "
            "Neighbors (Kennel, Brown & Abarbanel 1992, R_tol=10, A_tol=2) "
            "never dropped below the 1% threshold for ANY m in 1..10 when "
            "applied to the literal Gap (b) positive-control PRE (iid "
            "Gaussian white noise) -- so %DET/ENTR could not even be "
            "computed for that PRE, let alone tested for IAAFT power. This "
            "is DISTINCT from IAAFT_LOW_POWER: no p-value could be formed at "
            "all, not that a p-value was formed but non-significant. See "
            "VALIDATION_NOTE.md for the full discussion, the fGn-H/AR1-phi "
            "resolvability boundary, and why the bootstrap fallback (tested "
            "explicitly above, not assumed) does not resolve it."
        ),
    }

    # ---- 4b. Addendum decision rule (METHODOLOGY_NOTE.md commit 024e7a9,
    # steps 4-5), applied mechanically and honestly to positive_control_v2's
    # result -- this is the FINAL, pre-authorized verdict for this
    # candidate's validation stage; no further redesign is authorized. ----
    pos2 = results["positive_control_v2_rossler"]
    pos2_computable = pos2["status"] == "ok"

    if not pos2_computable:
        pos2_p_DET = pos2_p_ENTR = None
        sigma_DET_v2 = sigma_ENTR_v2 = None
        v2_DET_verdict = v2_ENTR_verdict = "NOT_COMPUTABLE"
    else:
        pos2_p_DET, pos2_p_ENTR = pos2["p_DET"], pos2["p_ENTR"]
        sigma_DET_v2 = sigma_equivalent(pos2["delta_DET"], pos2["surrogate_DET_mean"], pos2["surrogate_DET_std"])
        sigma_ENTR_v2 = sigma_equivalent(pos2["delta_ENTR"], pos2["surrogate_ENTR_mean"], pos2["surrogate_ENTR_std"])
        v2_DET_verdict = "IAAFT_HAS_REAL_POWER" if (pos2_p_DET is not None and pos2_p_DET < 0.05) else "IAAFT_LOW_POWER"
        v2_ENTR_verdict = "IAAFT_HAS_REAL_POWER" if (pos2_p_ENTR is not None and pos2_p_ENTR < 0.05) else "IAAFT_LOW_POWER"

    any_power_v2 = pos2_computable and (
        (pos2_p_DET is not None and pos2_p_DET < 0.05) or
        (pos2_p_ENTR is not None and pos2_p_ENTR < 0.05)
    )

    final_verdict = "VALIDATION_PASSED_PROCEED_TO_REAL_DATA" if any_power_v2 else \
        "VALIDATION_FAILED_CLOSE_AT_VALIDATION_STAGE_NO_THIRD_ATTEMPT"

    results["addendum_decision_rossler"] = {
        "description": (
            "Mechanical application of METHODOLOGY_NOTE.md addendum (commit "
            "024e7a9) steps 4-5 to positive_control_v2_rossler above: "
            "'if EITHER channel shows p<0.05 with clear null separation, "
            "validation passes; if NEITHER does, close RQA at the "
            "validation stage without touching real data -- no third "
            "attempt.'"
        ),
        "DET_channel": {
            "p_DET": pos2_p_DET, "sigma_equivalent": sigma_DET_v2,
            "significant_at_0.05": pos2_computable and pos2_p_DET is not None and pos2_p_DET < 0.05,
            "verdict": v2_DET_verdict,
        },
        "ENTR_channel": {
            "p_ENTR": pos2_p_ENTR, "sigma_equivalent": sigma_ENTR_v2,
            "significant_at_0.05": pos2_computable and pos2_p_ENTR is not None and pos2_p_ENTR < 0.05,
            "verdict": v2_ENTR_verdict,
        },
        "any_channel_shows_power": any_power_v2,
        "final_verdict": final_verdict,
    }

    results["pipeline_config"] = (
        pos_result["config"] if pos_result["status"] == "ok" else neg_result["config"]
    )
    results["generator_notes"] = {
        "colored_noise_fgn_like": (
            "FFT-filtering spectral synthesis: white Gaussian noise scaled "
            "per-frequency by f^(-exponent/2), inverse-transformed, z-scored. "
            "fGn-like approximation via exponent=2H+1 (spectral relation for "
            "fractional Gaussian noise); same technique as "
            "mse_multiscale_entropy/visibility_graph validate_synthetic.py, "
            "independent implementation."
        ),
        "logistic_map": "x_{k+1} = 4*x_k*(1-x_k), burn_in=500 discarded transient iterations.",
        "rank_remap": (
            "POST = sorted(PRE)[argsort(argsort(logistic_map_raw))] -- POST is "
            "an exact permutation of PRE's own values, reordered by the "
            "logistic map's temporal rank structure."
        ),
        "sine_with_dither": (
            "Deterministic sine wave (period 50) plus a 1e-6-relative Gaussian "
            "dither, used ONLY for the embedding/recurrence code-correctness "
            "diagnostic (check 0), not a PRE/POST identifiability control -- "
            "the dither breaks floating-point-exact self-recurrences that "
            "otherwise spuriously blow up FNN's ratio criterion."
        ),
        "rossler_x": (
            "Roessler system (a=0.2, b=0.2, c=5.7, classic chaotic regime), "
            "RK4 integration with dt_internal=0.01, 200 time-unit burn-in, "
            "sampled at dt=0.15 (chosen because it empirically gives a "
            "periodogram-slope spectral exponent close to fGn H=0.7's target "
            "2H+1=2.4 -- see positive_control_v2_rossler). x-coordinate only. "
            "Used for METHODOLOGY_NOTE.md addendum's (commit 024e7a9) "
            "positive_control_v2_rossler, rank-remapped onto the fGn PRE, "
            "same technique as the logistic-map v1 control."
        ),
    }
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
