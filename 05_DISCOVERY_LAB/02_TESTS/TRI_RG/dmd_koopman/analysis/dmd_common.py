"""
Canonical DMD / Koopman spectral-gap pipeline for DISC-TRI-RG-001,
candidate `dmd_koopman` (14th candidate identified for this test line
overall; 3rd and last of the 3 genuinely new candidates found in the
2026-08-20 Phase 0.7 survey -- see ../../phase0/PHASE0_7_SURVEY_NEW_CANDIDATES.md,
candidate 3).

Fixed BEFORE running on any real domain (Italy COVID-19 first-wave
lockdown 2020-03-09; Kilauea 2018 May-3 fissure opening) -- see
../METHODOLOGY_NOTE.md for the full rationale.

*** A PRIORI DEMOTION (METHODOLOGY_NOTE.md section 0): the single
dominant REAL eigenvalue's growth/decay rate is mathematically identical
to critical_slowing_down's AC1/variance in the near-fixed-point regime
(arXiv:2608.14716, arXiv:2508.19655) -- it is computed here ONLY as a
diagnostic (`real_dominant_rate`), never used in any significance
decision. The PRIMARY channel is the frequency (`f_dom`) and damping
ratio (`zeta`) of the least-damped complex-conjugate DMD/Koopman
eigenvalue pair -- targets Hopf/Neimark-Sacker oscillatory instability, a
class the CSD literature documents as a structural blind spot of
AC1/variance (arXiv:2605.28260). ***

Method (METHODOLOGY_NOTE.md "R_lambda"):
  1. Detrend (linear) + standardize (zero mean, unit variance) each
     segment before anything else.
  2. tau: rqa_common.estimate_tau (time-delayed mutual information,
     Fraser & Swinney 1986), imported unmodified.
  3. d (delay/Hankel-row dimension): d = clip(floor(N/HANKEL_D_DIVISOR),
     D_MIN, D_MAX) -- a length-sufficiency rule in the spirit of Arbabi &
     Mezic (2017)'s "d as large as practical" Hankel-DMD convergence
     theory, NOT a False-Nearest-Neighbors resolvability gate (see
     METHODOLOGY_NOTE.md section 1.3 for why this is a *different kind*
     of gate than RQA/LLE's FNN gate -- it is a length check, not a
     dynamical-resolvability check, and it always passes for long-enough
     segments regardless of whether the underlying dynamics are white
     noise or a genuine oscillator).
  4. Shared-embedding convention: (tau, d) estimated ONCE from PRE, the
     SAME (tau, d) applied to POST and to every surrogate of both. Rank r
     (Gavish-Donoho) is recomputed INDEPENDENTLY per condition (real PRE,
     real POST, each surrogate) -- analogous to LLE's Theiler window /
     RQA's epsilon.
  5. Hankel matrix H: column j = (x_j, x_{j+tau}, ..., x_{j+(d-1)*tau}),
     j=0..T-1, T = N-(d-1)*tau. X1 = H[:, :-1], X2 = H[:, 1:] (Koopman
     shift operator advances the COLUMN index by 1 native sample of the
     already-processed series, NOT by tau -- standard Hankel-DMD/HAVOK
     convention).
  6. Rank truncation r: Gavish & Donoho (2014) optimal hard threshold,
     unknown-noise case, general aspect-ratio formula (reduces to the
     omega(1)=2.858 special case at beta=1).
  7. Exact DMD (Tu, Rowley, Luchtenburg, Brunton & Kutz 2014): Atilde =
     U_r^H X2 V_r S_r^-1, eigendecompose Atilde.
  8. f_dom, zeta of the least-damped complex-conjugate eigenvalue pair
     (PRIMARY); inter-modal spectral gap between the top-2 distinct MODES
     by magnitude (COMPANION); dominant real eigenvalue's decay rate
     (DIAGNOSTIC-ONLY, demoted a priori); finite-rank reconstruction
     residual (secondary diagnostic).
  9. IAAFT surrogates (Schreiber & Schmitz 1996) are the PRIMARY
     significance test: N_SURROGATES=200, N_IAAFT_ITER=50, seed=12345.

Any agent applying this pipeline to real data MUST import and call
`run_dmd_analysis` rather than reimplementing any of this.
"""
import os
import sys

import numpy as np

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "rqa", "analysis")
)
from rqa_common import (  # noqa: E402  (audited, reused unmodified per METHODOLOGY_NOTE.md)
    estimate_tau,
    subsample_segment,
    iaaft_surrogate,
    moving_block_bootstrap_resample,
)

# ---- fixed constants (METHODOLOGY_NOTE.md -- identical for every domain
# this pipeline is ever applied to; no per-domain tuning) ----

HANKEL_D_DIVISOR = 10       # d ~= N / 10 (Arbabi-Mezic "as large as practical" spirit)
D_MIN = 10                  # floor: room for a few complex-pair modes + the real mode
D_MAX = 100                 # a priori compute-tractability ceiling
MIN_HANKEL_COLS = 50        # min T-1 columns for a stable SVD/regression (same floor
                             # convention as LLE's D2_MIN_PAIRS / MIN_THEILER_POINTS)

EPS_IMAG_REL = 1e-6         # relative tolerance for real-vs-complex eigenvalue classification

MAX_N_PER_SEGMENT = 200000  # subsampling cap (same as lempel_ziv_complexity's Kilauea cap)
N_SURROGATES = 200          # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50
SEED = 12345

N_BOOTSTRAP = 1000          # pre-authorized fallback, only if triggered


# ==========================================================================
# Pre-processing: linear detrend + standardize
# ==========================================================================

def detrend_standardize(x):
    """Linear (least-squares) detrend + zero-mean/unit-variance standardize.
    Returns (processed_series, info dict with slope/intercept/std used)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    t = np.arange(n, dtype=float)
    if n >= 2:
        slope, intercept = np.polyfit(t, x, 1)
        detrended = x - (slope * t + intercept)
    else:
        slope, intercept = 0.0, float(x[0]) if n == 1 else 0.0
        detrended = x - intercept
    std = float(np.std(detrended))
    if std <= 0:
        return detrended, {"slope": float(slope), "intercept": float(intercept),
                            "std": std, "status": "degenerate_std"}
    standardized = detrended / std
    return standardized, {"slope": float(slope), "intercept": float(intercept),
                           "std": std, "status": "ok"}


# ==========================================================================
# d: length-sufficiency rule (METHODOLOGY_NOTE.md section 1.3) -- NOT an
# FNN-style dynamical-resolvability gate; see module docstring.
# ==========================================================================

def estimate_d(n, tau, divisor=HANKEL_D_DIVISOR, d_min=D_MIN, d_max=D_MAX,
                min_hankel_cols=MIN_HANKEL_COLS):
    """d = clip(floor(N/divisor), d_min, d_max). Rejects
    (status='hankel_insufficient_length') if the resulting Hankel matrix
    would have fewer than d_min rows worth of headroom, or fewer than
    min_hankel_cols usable DMD-regression columns (T-1)."""
    d_raw = int(np.floor(n / divisor))
    if d_raw < d_min:
        return {"d": None, "status": "hankel_insufficient_length",
                "reason": f"floor(N/{divisor})={d_raw} < D_MIN={d_min}"}
    d = int(np.clip(d_raw, d_min, d_max))
    T = n - (d - 1) * tau
    if T - 1 < min_hankel_cols:
        return {"d": None, "status": "hankel_insufficient_length", "T": int(T),
                "reason": f"T-1={T - 1} < MIN_HANKEL_COLS={min_hankel_cols}"}
    return {"d": d, "T": int(T), "status": "ok"}


# ==========================================================================
# Hankel matrix construction
# ==========================================================================

def hankel_matrix(x, d, tau):
    """Column j = (x_j, x_{j+tau}, ..., x_{j+(d-1)*tau}), j=0..T-1,
    T = N-(d-1)*tau. Returns array shape (d, T)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    T = n - (d - 1) * tau
    if T <= 0:
        return np.empty((d, 0))
    idx = np.arange(T)[None, :] + tau * np.arange(d)[:, None]
    return x[idx]


# ==========================================================================
# Gavish & Donoho (2014) optimal hard threshold, unknown-noise case,
# general aspect-ratio formula (eq. 5 of the paper; reduces to omega(1)
# ~= 2.858 at beta=1, the special case cited literally in the task).
# ==========================================================================

def gavish_donoho_rank(X=None, sv=None, d=None, T=None):
    """Returns dict: r (int, >=1), singular_values (list), tau_star,
    omega_beta, beta, status.

    Accepts EITHER the raw data matrix `X` (d x T) OR its precomputed
    singular values `sv` (+ its shape `d`, `T`) -- the latter avoids a
    redundant full SVD when the caller (compute_dmd_features/exact_dmd)
    already needs the SVD of the same matrix for the DMD projection
    itself. Mathematically identical result either way -- this is a
    performance refactor only, not a change to R_lambda/I(X)."""
    if sv is None:
        if X is None:
            return {"r": None, "singular_values": [], "tau_star": None,
                    "omega_beta": None, "beta": None, "status": "empty_matrix"}
        d, T = X.shape
        if d == 0 or T == 0:
            return {"r": None, "singular_values": [], "tau_star": None,
                    "omega_beta": None, "beta": None, "status": "empty_matrix"}
        sv = np.linalg.svd(X, compute_uv=False)
    else:
        if d == 0 or T == 0 or len(sv) == 0:
            return {"r": None, "singular_values": [], "tau_star": None,
                    "omega_beta": None, "beta": None, "status": "empty_matrix"}
    m, n = min(d, T), max(d, T)
    beta = m / n
    omega_beta = 0.56 * beta ** 3 - 0.95 * beta ** 2 + 1.82 * beta + 1.43
    y_med = float(np.median(sv))
    tau_star = omega_beta * y_med
    r = int(np.sum(sv > tau_star))
    r = max(r, 1)
    return {"r": r, "singular_values": sv.tolist(), "tau_star": float(tau_star),
            "omega_beta": float(omega_beta), "beta": float(beta), "status": "ok"}


# ==========================================================================
# Exact DMD (Tu, Rowley, Luchtenburg, Brunton & Kutz 2014)
# ==========================================================================

def exact_dmd(X1, X2, r, svd=None):
    """Returns dict: eigenvalues (complex array), Atilde, U_r, S_r, V_r,
    reconstruction_residual (relative Frobenius norm of X2 - Atilde-
    projected reconstruction), status.

    `svd`, if given, is a precomputed (U, S, Vh) = np.linalg.svd(X1,
    full_matrices=False) tuple -- avoids a redundant SVD when the caller
    already computed it for gavish_donoho_rank. Mathematically identical
    either way (performance refactor only)."""
    if svd is None:
        U, S, Vh = np.linalg.svd(X1, full_matrices=False)
    else:
        U, S, Vh = svd
    r = min(r, len(S))
    if r < 1:
        return {"status": "rank_too_small"}
    U_r = U[:, :r]
    S_r = S[:r]
    V_r = Vh.conj().T[:, :r]
    if np.any(S_r <= 0):
        return {"status": "degenerate_singular_values"}
    Atilde = U_r.conj().T @ X2 @ V_r @ np.diag(1.0 / S_r)
    eigvals, W = np.linalg.eig(Atilde)

    # finite-rank reconstruction residual (secondary diagnostic)
    X2_hat = U_r @ (Atilde @ (U_r.conj().T @ X1))
    denom = np.linalg.norm(X2)
    residual = float(np.linalg.norm(X2 - X2_hat) / denom) if denom > 0 else None

    return {
        "status": "ok", "eigenvalues": eigvals, "Atilde": Atilde,
        "U_r": U_r, "S_r": S_r, "V_r": V_r,
        "reconstruction_residual": residual, "r_used": int(r),
    }


# ==========================================================================
# Mode classification: real vs. complex-conjugate pairs; primary-pair
# selection; spectral-gap companion; demoted real-eigenvalue diagnostic.
# ==========================================================================

def classify_modes(eigvals, eps_imag_rel=EPS_IMAG_REL):
    """Splits eigenvalues into real modes and complex-conjugate-pair modes.

    Returns dict:
      real_modes: list of {lambda, abs_lambda}
      complex_pairs: list of {lambda_plus (Im>=0), lambda_minus, abs_lambda}
      status
    """
    eigvals = np.asarray(eigvals)
    abs_vals = np.abs(eigvals)
    is_real = np.abs(eigvals.imag) < eps_imag_rel * np.maximum(abs_vals, 1e-300)

    real_modes = [{"lambda": complex(eigvals[i]), "abs_lambda": float(abs_vals[i])}
                  for i in np.where(is_real)[0]]

    complex_idx = np.where(~is_real)[0]
    used = np.zeros(len(complex_idx), dtype=bool)
    complex_pairs = []
    cvals = eigvals[complex_idx]
    for i in range(len(complex_idx)):
        if used[i]:
            continue
        # find best-matching conjugate partner: closest to conj(cvals[i])
        target = np.conj(cvals[i])
        dists = np.abs(cvals - target)
        dists[used] = np.inf
        dists[i] = np.inf
        if len(dists) == 0 or not np.any(np.isfinite(dists)):
            continue
        j = int(np.argmin(dists))
        used[i] = True
        used[j] = True
        a, b = cvals[i], cvals[j]
        lam_plus = a if a.imag >= b.imag else b
        lam_minus = b if a.imag >= b.imag else a
        complex_pairs.append({
            "lambda_plus": complex(lam_plus), "lambda_minus": complex(lam_minus),
            "abs_lambda": float(abs(lam_plus)),
        })

    return {"real_modes": real_modes, "complex_pairs": complex_pairs, "status": "ok"}


def freq_damping(lam, dt=1.0):
    """f_dom = arg(lam)/(2*pi*dt); zeta = -ln|lam| / sqrt(ln|lam|^2 + arg(lam)^2)."""
    mod = abs(lam)
    if mod <= 0:
        return None, None
    ln_mod = np.log(mod)
    arg = np.angle(lam)
    f_dom = arg / (2 * np.pi * dt)
    denom = np.sqrt(ln_mod ** 2 + arg ** 2)
    zeta = (-ln_mod / denom) if denom > 0 else None
    return float(f_dom), (float(zeta) if zeta is not None else None)


def select_primary_channels(mode_info, dt=1.0):
    """From classify_modes() output, selects:
      - primary complex-conjugate pair (largest |lambda| among complex_pairs)
        -> f_dom, zeta ('no_complex_mode' if complex_pairs is empty)
      - companion spectral gap: top-2 DISTINCT modes by magnitude (each
        complex pair counted ONCE, each real eigenvalue counted once)
      - diagnostic real_dominant_rate: ln|lambda|/dt of the largest-magnitude
        real mode (demoted a priori, see module docstring)
    """
    complex_pairs = mode_info["complex_pairs"]
    real_modes = mode_info["real_modes"]

    if len(complex_pairs) == 0:
        primary = {"status": "no_complex_mode", "f_dom": None, "zeta": None,
                   "abs_lambda": None}
    else:
        best = max(complex_pairs, key=lambda p: p["abs_lambda"])
        f_dom, zeta = freq_damping(best["lambda_plus"], dt=dt)
        primary = {"status": "ok", "f_dom": f_dom, "zeta": zeta,
                   "abs_lambda": best["abs_lambda"]}

    distinct_mode_mags = [p["abs_lambda"] for p in complex_pairs] + \
                          [m["abs_lambda"] for m in real_modes]
    distinct_mode_mags.sort(reverse=True)
    if len(distinct_mode_mags) >= 2:
        spectral_gap = float(distinct_mode_mags[0] - distinct_mode_mags[1])
    else:
        spectral_gap = None

    if len(real_modes) == 0:
        real_diag = {"status": "no_real_mode", "real_dominant_rate": None,
                     "abs_lambda": None}
    else:
        best_real = max(real_modes, key=lambda m: m["abs_lambda"])
        mod = best_real["abs_lambda"]
        rate = float(np.log(mod) / dt) if mod > 0 else None
        real_diag = {"status": "ok", "real_dominant_rate": rate,
                     "abs_lambda": mod}

    return {"primary": primary, "spectral_gap": spectral_gap, "real_diagnostic": real_diag,
            "n_complex_pairs": len(complex_pairs), "n_real_modes": len(real_modes)}


# ==========================================================================
# Full pipeline for one segment, GIVEN an already-fixed (tau, d)
# ==========================================================================

def compute_dmd_features(x, d, tau, dt=1.0):
    """Full DMD-feature pipeline for one segment: detrend+standardize ->
    Hankel(d,tau) -> Gavish-Donoho rank -> exact DMD -> mode classification
    -> primary/companion/diagnostic channels.

    Returns dict: status, f_dom, zeta, spectral_gap, real_dominant_rate,
    reconstruction_residual, r, n_complex_pairs, n_real_modes, plus
    intermediate objects for auditability (rank_info without singular
    vectors, mode_info).
    """
    x_proc, prep_info = detrend_standardize(x)
    if prep_info["status"] != "ok":
        return {"status": "degenerate_series", "prep_info": prep_info}

    H = hankel_matrix(x_proc, d, tau)
    T = H.shape[1]
    if T < 2:
        return {"status": "hankel_insufficient_length", "prep_info": prep_info}

    X1, X2 = H[:, :-1], H[:, 1:]
    if X1.shape[1] < 1:
        return {"status": "hankel_insufficient_length", "prep_info": prep_info}

    # single SVD of X1, reused for BOTH the Gavish-Donoho rank threshold
    # and the exact-DMD projection below (performance refactor only --
    # mathematically identical to computing it twice).
    U, S, Vh = np.linalg.svd(X1, full_matrices=False)
    rank_info = gavish_donoho_rank(sv=S, d=X1.shape[0], T=X1.shape[1])
    if rank_info["status"] != "ok":
        return {"status": "rank_not_computable", "prep_info": prep_info, "rank_info": rank_info}
    r = rank_info["r"]

    dmd_result = exact_dmd(X1, X2, r, svd=(U, S, Vh))
    if dmd_result["status"] != "ok":
        return {"status": "dmd_not_computable", "prep_info": prep_info,
                "rank_info": {"r": r, "beta": rank_info["beta"], "tau_star": rank_info["tau_star"]},
                "dmd_status": dmd_result["status"]}

    mode_info = classify_modes(dmd_result["eigenvalues"])
    channels = select_primary_channels(mode_info, dt=dt)

    return {
        "status": "ok",
        "prep_info": prep_info,
        "rank_info": {"r": r, "beta": rank_info["beta"], "tau_star": rank_info["tau_star"],
                      "omega_beta": rank_info["omega_beta"],
                      "n_singular_values": len(rank_info["singular_values"])},
        "reconstruction_residual": dmd_result["reconstruction_residual"],
        "f_dom": channels["primary"]["f_dom"],
        "zeta": channels["primary"]["zeta"],
        "primary_status": channels["primary"]["status"],
        "spectral_gap": channels["spectral_gap"],
        "real_dominant_rate": channels["real_diagnostic"]["real_dominant_rate"],
        "real_diagnostic_status": channels["real_diagnostic"]["status"],
        "n_complex_pairs": channels["n_complex_pairs"],
        "n_real_modes": channels["n_real_modes"],
        "n_samples": int(len(x)), "d": int(d), "tau": int(tau), "T": int(T),
    }


# ==========================================================================
# Full PRE/POST transition test pipeline (public entry point)
# ==========================================================================

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def run_dmd_analysis(pre_series, post_series, seed=SEED, n_mc=None, n_iter=N_IAAFT_ITER,
                      max_n=MAX_N_PER_SEGMENT, hankel_d_divisor=HANKEL_D_DIVISOR,
                      d_min=D_MIN, d_max=D_MAX, run_bootstrap=False, n_bootstrap=N_BOOTSTRAP):
    """Run the full DMD/Koopman transition test between a PRE and a POST
    segment, per METHODOLOGY_NOTE.md.

    Steps:
      1. Subsampling (MAX_N_PER_SEGMENT) applied to PRE and POST
         independently.
      2. tau estimated from (subsampled) PRE via rqa_common.estimate_tau.
      3. d estimated from (subsampled) PRE via estimate_d (length-
         sufficiency rule, NOT an FNN-style resolvability gate --
         status="hankel_insufficient_length" if the segment is too short,
         no forced fallback d).
      4. (tau, d) FIXED from PRE, applied to POST and to every surrogate
         of both (shared-embedding convention). Rank r (Gavish-Donoho)
         computed independently per condition.
      5. f_dom/zeta (primary), spectral_gap (companion), real_dominant_rate
         (diagnostic-only, demoted a priori) computed for real PRE/POST.
      6. IAAFT is the PRIMARY significance test: N_SURROGATES independent
         PRE/POST surrogate pairs, each generated from its OWN real
         (already-subsampled) segment, seed=12345. Two-tailed p-values
         for Delta_f_dom, Delta_zeta, Delta_spectral_gap.
      7. If run_bootstrap=True, ALSO runs the moving-block bootstrap
         (Kunsch 1989) fallback. Off by default.

    Returns a dict with everything needed to report a result without
    recomputing anything.
    """
    n_surrogates = N_SURROGATES if n_mc is None else int(n_mc)

    pre_raw = np.asarray(pre_series, dtype=float)
    post_raw = np.asarray(post_series, dtype=float)

    pre, pre_sub_info = subsample_segment(pre_raw, max_n=max_n)
    post, post_sub_info = subsample_segment(post_raw, max_n=max_n)

    tau_info = estimate_tau(pre)
    if tau_info["status"] != "ok":
        return {
            "status": "tau_not_resolved", "tau_info": tau_info, "d_info": None,
            "diagnostics": {"pre_subsampling": pre_sub_info, "post_subsampling": post_sub_info},
        }
    tau = tau_info["tau"]

    d_info = estimate_d(len(pre), tau, divisor=hankel_d_divisor, d_min=d_min, d_max=d_max)
    if d_info["status"] != "ok":
        return {
            "status": "hankel_insufficient_length", "tau_info": tau_info, "d_info": d_info,
            "diagnostics": {"pre_subsampling": pre_sub_info, "post_subsampling": post_sub_info},
        }
    d = d_info["d"]

    real_pre = compute_dmd_features(pre, d, tau)
    real_post = compute_dmd_features(post, d, tau)

    def _get(res, key):
        if res is None or res["status"] != "ok":
            return None
        return res.get(key)

    f_dom_pre, f_dom_post = _get(real_pre, "f_dom"), _get(real_post, "f_dom")
    zeta_pre, zeta_post = _get(real_pre, "zeta"), _get(real_post, "zeta")
    gap_pre, gap_post = _get(real_pre, "spectral_gap"), _get(real_post, "spectral_gap")
    real_rate_pre, real_rate_post = _get(real_pre, "real_dominant_rate"), _get(real_post, "real_dominant_rate")

    delta_f_dom_real = _delta(f_dom_post, f_dom_pre)
    delta_zeta_real = _delta(zeta_post, zeta_pre)
    delta_gap_real = _delta(gap_post, gap_pre)
    delta_real_rate_real = _delta(real_rate_post, real_rate_pre)  # diagnostic-only

    rng = np.random.default_rng(seed)
    surr = {"f_dom": [], "zeta": [], "gap": []}
    n_undef = {"f_dom": 0, "zeta": 0, "gap": 0}

    for _ in range(n_surrogates):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        feat_pre_s = compute_dmd_features(surr_pre, d, tau)
        feat_post_s = compute_dmd_features(surr_post, d, tau)

        for key, subkey in (("f_dom", "f_dom"), ("zeta", "zeta"), ("gap", "spectral_gap")):
            v_pre = _get(feat_pre_s, subkey)
            v_post = _get(feat_post_s, subkey)
            delta = _delta(v_post, v_pre)
            if delta is None:
                n_undef[key] += 1
            else:
                surr[key].append(delta)

    surr_arr = {k: np.array(v, dtype=float) for k, v in surr.items()}

    def _pval(delta_real, arr):
        if delta_real is None or len(arr) == 0:
            return None
        return float(np.mean(np.abs(arr) >= abs(delta_real)))

    p_f_dom = _pval(delta_f_dom_real, surr_arr["f_dom"])
    p_zeta = _pval(delta_zeta_real, surr_arr["zeta"])
    p_gap = _pval(delta_gap_real, surr_arr["gap"])

    result = {
        "status": "ok",
        "tau": tau, "d": d, "tau_info": tau_info, "d_info": d_info,
        "real_pre": real_pre, "real_post": real_post,
        "f_dom_pre": f_dom_pre, "f_dom_post": f_dom_post,
        "zeta_pre": zeta_pre, "zeta_post": zeta_post,
        "spectral_gap_pre": gap_pre, "spectral_gap_post": gap_post,
        "real_dominant_rate_pre": real_rate_pre, "real_dominant_rate_post": real_rate_post,
        "delta_f_dom": delta_f_dom_real, "delta_zeta": delta_zeta_real,
        "delta_spectral_gap": delta_gap_real, "delta_real_dominant_rate": delta_real_rate_real,
        "p_f_dom": p_f_dom, "p_zeta": p_zeta, "p_spectral_gap": p_gap,
        "surrogate_f_dom_mean": float(np.mean(surr_arr["f_dom"])) if len(surr_arr["f_dom"]) else None,
        "surrogate_f_dom_std": float(np.std(surr_arr["f_dom"])) if len(surr_arr["f_dom"]) else None,
        "surrogate_f_dom_n_valid": int(len(surr_arr["f_dom"])),
        "surrogate_f_dom_n_undefined": int(n_undef["f_dom"]),
        "surrogate_zeta_mean": float(np.mean(surr_arr["zeta"])) if len(surr_arr["zeta"]) else None,
        "surrogate_zeta_std": float(np.std(surr_arr["zeta"])) if len(surr_arr["zeta"]) else None,
        "surrogate_zeta_n_valid": int(len(surr_arr["zeta"])),
        "surrogate_zeta_n_undefined": int(n_undef["zeta"]),
        "surrogate_gap_mean": float(np.mean(surr_arr["gap"])) if len(surr_arr["gap"]) else None,
        "surrogate_gap_std": float(np.std(surr_arr["gap"])) if len(surr_arr["gap"]) else None,
        "surrogate_gap_n_valid": int(len(surr_arr["gap"])),
        "surrogate_gap_n_undefined": int(n_undef["gap"]),
        "diagnostics": {
            "pre_subsampling": pre_sub_info, "post_subsampling": post_sub_info,
            "pre_status": real_pre["status"], "post_status": real_post["status"],
            "pre_primary_status": real_pre.get("primary_status"),
            "post_primary_status": real_post.get("primary_status"),
        },
        "config": {
            "max_n_per_segment": max_n, "n_surrogates": n_surrogates,
            "n_iaaft_iter": n_iter, "seed": seed,
            "hankel_d_divisor": hankel_d_divisor, "d_min": d_min, "d_max": d_max,
        },
    }

    if run_bootstrap:
        boot_result = run_block_bootstrap_test_dmd(
            pre, post, d, tau, real_pre=real_pre, real_post=real_post,
            n_bootstrap=n_bootstrap, seed=seed,
        )
        result.update(boot_result)

    return result


# ==========================================================================
# Moving-block bootstrap (Kunsch 1989) -- pre-authorized fallback, only
# exercised as a PRIMARY test if validate_synthetic.py's power check
# requires it (see VALIDATION_NOTE.md).
# ==========================================================================

def _percentile_ci95(arr):
    lo, hi = np.percentile(arr, [2.5, 97.5])
    return (float(lo), float(hi))


def _bootstrap_two_tailed_p(delta_arr):
    frac_le0 = float(np.mean(delta_arr <= 0))
    frac_ge0 = float(np.mean(delta_arr >= 0))
    return float(2 * min(frac_le0, frac_ge0))


def run_block_bootstrap_test_dmd(pre_segment, post_segment, d, tau, real_pre=None, real_post=None,
                                  n_bootstrap=N_BOOTSTRAP, seed=SEED):
    """Moving-block bootstrap (Kunsch 1989) significance test for
    Delta_f_dom / Delta_zeta / Delta_spectral_gap, block length
    L = max(2*tau, 10) (same convention as rqa_common/lle_common)."""
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    def _get(res, key):
        if res is None or res["status"] != "ok":
            return None
        return res.get(key)

    if real_pre is None:
        real_pre = compute_dmd_features(pre, d, tau)
    if real_post is None:
        real_post = compute_dmd_features(post, d, tau)

    L = max(2 * tau, 10)
    rng = np.random.default_rng(seed)

    boot_pre = {"f_dom": [], "zeta": [], "gap": []}
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(pre, L, rng)
        feat = compute_dmd_features(resampled, d, tau)
        boot_pre["f_dom"].append(_get(feat, "f_dom"))
        boot_pre["zeta"].append(_get(feat, "zeta"))
        boot_pre["gap"].append(_get(feat, "spectral_gap"))

    boot_post = {"f_dom": [], "zeta": [], "gap": []}
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(post, L, rng)
        feat = compute_dmd_features(resampled, d, tau)
        boot_post["f_dom"].append(_get(feat, "f_dom"))
        boot_post["zeta"].append(_get(feat, "zeta"))
        boot_post["gap"].append(_get(feat, "spectral_gap"))

    def _pair_deltas(pre_vals, post_vals):
        deltas, n_undef = [], 0
        for vp, vq in zip(pre_vals, post_vals):
            if vp is None or vq is None:
                n_undef += 1
            else:
                deltas.append(vq - vp)
        return np.array(deltas, dtype=float), n_undef

    result = {"bootstrap_block_length": int(L), "bootstrap_n_bootstrap": int(n_bootstrap),
              "bootstrap_seed": int(seed)}
    for name in ("f_dom", "zeta", "gap"):
        deltas, n_undef = _pair_deltas(boot_pre[name], boot_post[name])
        n_valid = len(deltas)
        if n_valid == 0:
            ci95, p, mean_d, std_d = (None, None), None, None, None
        else:
            ci95 = _percentile_ci95(deltas)
            p = _bootstrap_two_tailed_p(deltas)
            mean_d = float(np.mean(deltas))
            std_d = float(np.std(deltas))
        result[f"delta_{name}_boot_ci95"] = ci95
        result[f"p_bootstrap_{name}"] = p
        result[f"delta_{name}_boot_mean"] = mean_d
        result[f"delta_{name}_boot_std"] = std_d
        result[f"delta_{name}_boot_n_valid"] = n_valid
        result[f"delta_{name}_boot_n_undefined"] = n_undef

    return result
