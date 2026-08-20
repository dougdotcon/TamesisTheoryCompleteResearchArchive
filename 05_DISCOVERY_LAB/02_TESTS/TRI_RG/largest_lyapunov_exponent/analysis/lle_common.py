"""
Canonical Largest Lyapunov Exponent (LLE, Rosenstein et al. 1993 algorithm)
pipeline for DISC-TRI-RG-001, candidate `largest_lyapunov_exponent` (13th
candidate identified for this test line overall; 2nd of 3 genuinely new
candidates found in the 2026-08-20 Phase 0.7 survey -- see
../../phase0/PHASE0_7_SURVEY_NEW_CANDIDATES.md, candidate 2).

Fixed BEFORE running on any real domain (Kilauea 2018 May-17 explosive
onset, MIT-BIH afdb record 04936) -- see ../METHODOLOGY_NOTE.md for the full
rationale. This candidate REUSES (imports directly, does not reimplement)
the audited tau (time-delayed mutual information, Fraser & Swinney 1986) and
m (False Nearest Neighbors, Kennel, Brown & Abarbanel 1992) estimators from
`rqa/analysis/rqa_common.py`, per METHODOLOGY_NOTE.md's explicit instruction
that this is the SAME embedding machinery already audited for that
candidate. The rest of this module (Rosenstein divergence-curve estimator,
Kantz-Schreiber automated scaling-region rule, Theiler window via mean
spectral frequency, correlation dimension D2, IAAFT surrogate significance
test) is new/self-contained for this candidate.

*** MANDATORY, NON-NEGOTIABLE RULE (METHODOLOGY_NOTE.md, "REGRA
OBRIGATORIA"): if FNN never resolves m<=10 for a segment, this module MUST
return status="embedding_not_resolved" and MUST NOT fall back to a forced
default m. Unlike RQA's %DET/ENTR (which simply fail to compute on an
unresolved embedding), the raw Rosenstein divergence-curve slope does NOT
fail cleanly on noise -- it silently returns a spurious numeric value even
on a meaningless embedding (Provenzale, Smith, Vio & Murante 1992, Physica D
58:31). This hard-reject gate is implemented as an early `return` in
`run_lle_analysis`, BEFORE any lambda_1/D2 computation is attempted -- see
that function's body. ***

Method (METHODOLOGY_NOTE.md "R_lambda"):
  1. tau: rqa_common.estimate_tau (time-delayed mutual information,
     Fraser & Swinney 1986), imported unmodified.
  2. m: rqa_common.estimate_m / rqa_common.fnn_fraction (False Nearest
     Neighbors, Kennel, Brown & Abarbanel 1992, R_tol=10, A_tol=2, m<=10),
     imported unmodified. HARD REJECT (embedding_not_resolved) if no m<=10
     resolves -- see mandatory rule above.
  3. Shared-embedding convention: (m, tau) estimated ONCE from PRE, the SAME
     (m, tau) applied to POST and to every surrogate of both.
  4. Theiler window w = round(1 / mean_spectral_frequency) (Rosenstein et
     al. 1993's own convention -- DIFFERENT from RQA's w=tau convention, not
     a conflation). Computed INDEPENDENTLY per condition (real PRE, real
     POST, each surrogate) -- analogous to RQA's per-condition epsilon, NOT
     shared like (m, tau).
  5. Rosenstein divergence curve <ln d_j(k)>, k=0..K_max
     (K_max=min(200, floor(M/2))), Euclidean nearest-neighbor search
     excluding |i-j|<=w.
  6. Automated linear-fit region via the Kantz & Schreiber (2004)
     convergence criterion: divergence curves recomputed at m*, m*+1, m*+2;
     largest contiguous window (min length 5) where the fitted slope changes
     by <10% between m*->m*+1 and m*+1->m*+2 is selected. lambda_1 = slope
     at m=m* in that window. If no window is stable: status
     "linear_region_not_resolved" for that segment's lambda_1.
  7. D2 (Grassberger & Procaccia 1983): correlation integral C(r) over pairs
     |i-j|>w, SAME automated scaling-region rule applied to log C(r) vs
     log r across m*, m*+1, m*+2.
  8. MAX_N_PER_SEGMENT=5000 subsampling (uniform stride decimation).
  9. IAAFT surrogates (Schreiber & Schmitz 1996) are the PRIMARY
     significance test: N_SURROGATES=200, N_IAAFT_ITER=50, seed=12345.

Any agent applying this pipeline to real data MUST import and call
`run_lle_analysis` rather than reimplementing any of this.
"""
import os
import sys

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import pdist, squareform

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "rqa", "analysis")
)
from rqa_common import (  # noqa: E402  (audited, reused unmodified per METHODOLOGY_NOTE.md)
    estimate_tau,
    estimate_m,
    takens_embed,
    subsample_segment,
    iaaft_surrogate,
    moving_block_bootstrap_resample,
)

# ---- fixed constants (METHODOLOGY_NOTE.md -- identical for every domain
# this pipeline is ever applied to; no per-domain tuning) ----

FNN_M_MAX = 10                    # a priori ceiling for the FNN hard-reject gate
K_MAX_CAP = 200                   # divergence-curve horizon cap
K_MAX_M_DIVISOR = 2               # K_max = min(K_MAX_CAP, floor(M/2))
MIN_FIT_LEN = 5                   # minimum contiguous window length for slope fitting
SLOPE_STABILITY_TOL = 0.10        # Kantz-Schreiber convergence tolerance (relative)
MIN_R2_FOR_LINEAR_REGION = 0.95   # goodness-of-fit gate, see note below
N_EXTRA_M_FOR_CONVERGENCE = 2     # test m*, m*+1, m*+2 (this many beyond m*)
# MIN_R2_FOR_LINEAR_REGION: added during code-correctness testing (logistic
# map, m=2, tau=1 forced), BEFORE any synthetic-validation or real-data
# calculation -- documented in METHODOLOGY_NOTE.md. Without this gate, a
# bounded chaotic attractor's divergence-curve PLATEAU (post-saturation,
# where the curve is flat because distances are capped by the attractor's
# diameter) is trivially "stable across m" (near-zero slope at every m,
# satisfying the relative-tolerance test vacuously) and -- being longer than
# the true ballistic/exponential-growth segment -- would otherwise WIN the
# "largest stable window" rule, silently returning lambda_1~=0 instead of
# the genuine divergence rate. Requiring R²>=0.95 (standard "well-fit line"
# convention) at m* is a joint, mechanical, pre-declared criterion -- not
# eyeballing -- that cleanly separates the genuine linear-growth region
# (R²>0.9999 on the logistic-map diagnostic) from the saturated plateau
# (R²~0.005 on the same diagnostic, see analysis notebook / VALIDATION_NOTE.md).

D2_N_RADII = 30                   # log-spaced radii for the correlation integral
D2_MIN_PAIRS = 50                 # below this, C(r) undefined at that radius

MAX_N_PER_SEGMENT = 5000          # subsampling cap (same convention as RQA/VG)
N_SURROGATES = 200                # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50
SEED = 12345

N_BOOTSTRAP = 1000                 # pre-authorized fallback, only if triggered
MIN_THEILER_POINTS = 30            # below this, Theiler-window computation is unreliable


# ==========================================================================
# Theiler window: reciprocal of the mean frequency of the power spectrum
# (Rosenstein et al. 1993's own convention -- distinct from RQA's w=tau)
# ==========================================================================

def theiler_window(x, w_min=1, w_max_frac=0.25):
    """w = round(1 / mean_frequency), mean_frequency = power-weighted mean
    of the positive-frequency periodogram (cycles/sample). Computed
    independently per condition (real PRE, real POST, each surrogate) --
    NOT shared like (m, tau), analogous to RQA's per-condition epsilon.

    w_max_frac caps w at w_max_frac * N (a priori safety cap, avoids a
    degenerate near-DC estimate consuming most of the series as excluded
    neighbors) -- fixed a priori, not tuned after seeing any domain.

    Returns dict: w (int), mean_frequency (float or None), status
    ("ok" or "theiler_not_resolved").
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < MIN_THEILER_POINTS:
        return {"w": None, "mean_frequency": None, "status": "theiler_not_resolved",
                "reason": "insufficient_points"}
    xd = x - x.mean()
    spectrum = np.fft.rfft(xd)
    freqs = np.fft.rfftfreq(n)
    power = np.abs(spectrum) ** 2
    mask = freqs > 0
    if not np.any(mask) or power[mask].sum() <= 0:
        return {"w": None, "mean_frequency": None, "status": "theiler_not_resolved",
                "reason": "degenerate_spectrum"}
    mean_freq = float(np.sum(freqs[mask] * power[mask]) / np.sum(power[mask]))
    if mean_freq <= 0:
        return {"w": None, "mean_frequency": mean_freq, "status": "theiler_not_resolved",
                "reason": "nonpositive_mean_frequency"}
    w = int(round(1.0 / mean_freq))
    w_max = max(w_min, int(np.floor(w_max_frac * n)))
    w = int(np.clip(w, w_min, w_max))
    return {"w": w, "mean_frequency": mean_freq, "status": "ok"}


# ==========================================================================
# Rosenstein divergence curve
# ==========================================================================

def divergence_curve(x, m, tau, w, k_max_cap=K_MAX_CAP, k_max_m_divisor=K_MAX_M_DIVISOR):
    """Rosenstein et al. (1993) divergence curve <ln d_j(k)>, k=0..K_max.

    For each reference point i in the m-dim embedding, the nearest neighbor
    j is found by EUCLIDEAN distance (standard Rosenstein convention,
    distinct from RQA's Chebyshev metric), excluding |i-j|<=w (Theiler
    window). Divergence d_j(k) = ||Y_{i+k} - Y_{j+k}|| is tracked for
    k=0..K_max, restricted to reference points for which i+k and j+k both
    remain within the embedded series. y(k) = mean(ln d_j(k)) over all valid
    reference points with d_j(0) > 0 (coincident-neighbor points excluded,
    same convention as RQA's FNN R_i^m==0 exclusion).

    Returns dict: k (list[int]), y (list[float or nan]), n_used (list[int]),
    M (n embedded points), status.
    """
    x = np.asarray(x, dtype=float)
    Y = takens_embed(x, m, tau)
    M = Y.shape[0]
    if M < MIN_THEILER_POINTS:
        return {"k": [], "y": [], "n_used": [], "M": int(M), "status": "insufficient_embedded_points"}

    tree = cKDTree(Y)
    # query more than 1 neighbor so we can skip points within the Theiler window
    k_query = min(M, max(2, 2 * w + 2))
    dist, idx = tree.query(Y, k=k_query)
    if dist.ndim == 1:
        dist = dist[:, None]
        idx = idx[:, None]

    ref_idx = np.arange(M)
    nn_idx = np.full(M, -1, dtype=int)
    nn_dist = np.full(M, np.nan, dtype=float)
    for col in range(dist.shape[1]):
        cand = idx[:, col]
        cand_dist = dist[:, col]
        unresolved = nn_idx < 0
        far_enough = np.abs(cand - ref_idx) > w
        valid = unresolved & far_enough & (cand_dist > 0)
        nn_idx[valid] = cand[valid]
        nn_dist[valid] = cand_dist[valid]
        if not np.any(nn_idx < 0):
            break
    valid_ref = nn_idx >= 0

    k_max = min(k_max_cap, int(np.floor(M / k_max_m_divisor)))
    if k_max < 1:
        return {"k": [], "y": [], "n_used": [], "M": int(M), "status": "k_max_too_small"}

    ks, ys, n_used_list = [], [], []
    for k in range(0, k_max + 1):
        ok = valid_ref.copy()
        i_plus_k = ref_idx + k
        j_plus_k = nn_idx + k
        in_range = (i_plus_k < M) & (j_plus_k < M)
        ok = ok & in_range
        if not np.any(ok):
            ks.append(k)
            ys.append(float("nan"))
            n_used_list.append(0)
            continue
        diffs = Y[i_plus_k[ok]] - Y[j_plus_k[ok]]
        d = np.sqrt(np.sum(diffs ** 2, axis=1))
        d = d[d > 0]
        if d.size == 0:
            ks.append(k)
            ys.append(float("nan"))
            n_used_list.append(0)
            continue
        ks.append(k)
        ys.append(float(np.mean(np.log(d))))
        n_used_list.append(int(d.size))

    return {"k": ks, "y": ys, "n_used": n_used_list, "M": int(M), "status": "ok"}


# ==========================================================================
# Kantz-Schreiber (2004) automated scaling-region rule -- shared by
# lambda_1 (semi-log divergence curve) and D2 (log-log correlation integral)
# ==========================================================================

def _local_slope(x_vals, y_vals, i1, i2):
    """Least-squares slope of y_vals[i1:i2+1] vs x_vals[i1:i2+1], ignoring
    non-finite y values. Returns (slope, r_squared, n_points) or
    (None, None, n_finite) if fewer than 2 finite points."""
    xs = np.asarray(x_vals[i1:i2 + 1], dtype=float)
    ys = np.asarray(y_vals[i1:i2 + 1], dtype=float)
    finite = np.isfinite(ys)
    n_finite = int(finite.sum())
    if n_finite < 2:
        return None, None, n_finite
    xs_f, ys_f = xs[finite], ys[finite]
    slope, intercept = np.polyfit(xs_f, ys_f, 1)
    pred = slope * xs_f + intercept
    ss_res = float(np.sum((ys_f - pred) ** 2))
    ss_tot = float(np.sum((ys_f - ys_f.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else None
    return float(slope), r2, n_finite


def find_stable_scaling_region(x_vals, y_by_m, m_sorted, tol=SLOPE_STABILITY_TOL,
                                min_len=MIN_FIT_LEN, min_r2=MIN_R2_FOR_LINEAR_REGION):
    """Kantz & Schreiber (2004) automated scaling-region rule, shared by
    lambda_1 and D2. `y_by_m` is a dict {m: y_values_array} for exactly 3
    consecutive increasing m in `m_sorted` (e.g. [m*, m*+1, m*+2]), all
    aligned to the SAME `x_vals` index positions.

    Searches all contiguous windows [i1,i2] of length >= min_len over
    x_vals, fits a local slope at each of the 3 m, and marks the window
    STABLE if the relative slope change is <tol between consecutive m
    (m_sorted[0]->m_sorted[1] AND m_sorted[1]->m_sorted[2]). Returns the
    LARGEST stable window (ties broken by earliest start); if none found,
    status="linear_region_not_resolved".

    Reports lambda_1 (or D2, depending on caller) as the slope at
    m_sorted[0] (the FNN-audited m*) within the selected window -- m*+1 and
    m*+2 are used ONLY to confirm stability, not to recompute the reported
    value (METHODOLOGY_NOTE.md).

    Returns dict: status, window (dict k1,k2 or None), slope_m_star,
    r_squared_m_star, slopes_all_m (dict), n_windows_tested, n_windows_stable.
    """
    n = len(x_vals)
    assert len(m_sorted) == 3, "requires exactly 3 consecutive m for the convergence check"
    m0, m1, m2 = m_sorted

    x_vals = np.asarray(x_vals, dtype=float)

    # Vectorized O(n^2)-space (not O(n^2)-python-loop) slope/R2 evaluation
    # for every candidate window [i1,i2] simultaneously, via prefix sums --
    # mathematically identical to the brute-force per-window least-squares
    # fit in `_local_slope` (closed-form simple-linear-regression identity),
    # just computed without a Python-level double loop over ~n^2/2 windows
    # x 3 m-curves x np.polyfit calls, which is intractable at the K_max<=200
    # scale used here once this is called O(N_SURROGATES) times per PRE/POST
    # pair in `run_lle_analysis`.
    def _prefix_sums(y):
        y = np.asarray(y, dtype=float)
        nan_mask = ~np.isfinite(y)
        y_filled = np.where(nan_mask, 0.0, y)
        x_filled = x_vals
        Sx = np.concatenate([[0.0], np.cumsum(x_filled)])
        Sy = np.concatenate([[0.0], np.cumsum(y_filled)])
        Sxy = np.concatenate([[0.0], np.cumsum(x_filled * y_filled)])
        Sxx = np.concatenate([[0.0], np.cumsum(x_filled * x_filled)])
        Syy = np.concatenate([[0.0], np.cumsum(y_filled * y_filled)])
        Cnan = np.concatenate([[0], np.cumsum(nan_mask.astype(int))])
        return Sx, Sy, Sxy, Sxx, Syy, Cnan

    stats = {m: _prefix_sums(y_by_m[m]) for m in (m0, m1, m2)}

    i1_idx = np.arange(n)[:, None]
    i2_idx = np.arange(n)[None, :]
    length = i2_idx - i1_idx + 1
    len_ok = length >= min_len
    # only the upper-triangular (i2>=i1) region is meaningful
    tri_ok = i2_idx >= i1_idx
    base_valid = len_ok & tri_ok
    n_tested = int(np.sum(base_valid))

    def _window_slope_r2(m):
        Sx, Sy, Sxy, Sxx, Syy, Cnan = stats[m]
        nw = length.astype(float)
        wx = Sx[i2_idx + 1] - Sx[i1_idx]
        wy = Sy[i2_idx + 1] - Sy[i1_idx]
        wxy = Sxy[i2_idx + 1] - Sxy[i1_idx]
        wxx = Sxx[i2_idx + 1] - Sxx[i1_idx]
        wyy = Syy[i2_idx + 1] - Syy[i1_idx]
        wnan = Cnan[i2_idx + 1] - Cnan[i1_idx]

        denom = nw * wxx - wx ** 2
        with np.errstate(divide="ignore", invalid="ignore"):
            slope = (nw * wxy - wx * wy) / denom
            intercept = (wy - slope * wx) / nw
            ss_res = wyy - intercept * wy - slope * wxy
            ss_tot = wyy - (wy ** 2) / nw
            r2 = 1.0 - ss_res / ss_tot

        no_nan = (wnan == 0)
        finite_ok = np.isfinite(slope) & np.isfinite(r2) & (denom > 1e-12) & (ss_tot > 1e-300)
        valid = base_valid & no_nan & finite_ok
        return slope, r2, valid

    s0, r2_0, valid0 = _window_slope_r2(m0)
    s1, _, valid1 = _window_slope_r2(m1)
    s2, _, valid2 = _window_slope_r2(m2)

    valid_all = valid0 & valid1 & valid2
    with np.errstate(divide="ignore", invalid="ignore"):
        denom1_ok = np.abs(s0) > 1e-12
        denom2_ok = np.abs(s1) > 1e-12
        rel1 = np.abs(s1 - s0) / np.where(denom1_ok, np.abs(s0), np.nan)
        rel2 = np.abs(s2 - s1) / np.where(denom2_ok, np.abs(s1), np.nan)

    stable = (
        valid_all & denom1_ok & denom2_ok
        & (rel1 < tol) & (rel2 < tol) & (r2_0 >= min_r2)
    )
    n_stable = int(np.sum(stable))

    if n_stable == 0:
        return {
            "status": "linear_region_not_resolved", "window": None,
            "slope_m_star": None, "r_squared_m_star": None, "slopes_all_m": None,
            "n_windows_tested": n_tested, "n_windows_stable": n_stable,
        }

    # pick the largest stable window (ties broken by earliest start i1)
    length_masked = np.where(stable, length, -1)
    max_len = int(length_masked.max())
    candidates_i1, candidates_i2 = np.where(length_masked == max_len)
    order = np.argsort(candidates_i1)
    i1 = int(candidates_i1[order[0]])
    i2 = int(candidates_i2[order[0]])

    slopes = {m0: float(s0[i1, i2]), m1: float(s1[i1, i2]), m2: float(s2[i1, i2])}
    r2_val = float(r2_0[i1, i2])

    return {
        "status": "ok",
        "window": {"i1": int(i1), "i2": int(i2), "length": int(max_len),
                   "x_start": float(x_vals[i1]), "x_end": float(x_vals[i2])},
        "slope_m_star": slopes[m0],
        "r_squared_m_star": r2_val,
        "slopes_all_m": {str(k): v for k, v in slopes.items()},
        "n_windows_tested": n_tested,
        "n_windows_stable": n_stable,
    }


# ==========================================================================
# lambda_1: Rosenstein divergence curves at m*, m*+1, m*+2 + scaling-region rule
# ==========================================================================

def compute_lambda1(x, m_star, tau, w, k_max_cap=K_MAX_CAP, k_max_m_divisor=K_MAX_M_DIVISOR,
                     tol=SLOPE_STABILITY_TOL, min_len=MIN_FIT_LEN, min_r2=MIN_R2_FOR_LINEAR_REGION):
    """Full lambda_1 pipeline for one already-embedded-dimension-resolved
    segment: computes the Rosenstein divergence curve at m_star, m_star+1,
    m_star+2 (same tau, same w -- w is a property of THIS series, computed
    once by the caller and passed in), then applies the shared Kantz-
    Schreiber scaling-region rule.

    Returns dict: status, lambda_1, r_squared, window, curves (per-m divergence
    curves, for auditability), n_windows_tested/stable.
    """
    m_list = [m_star, m_star + 1, m_star + 2]
    curves = {}
    for m in m_list:
        curves[m] = divergence_curve(x, m, tau, w, k_max_cap=k_max_cap, k_max_m_divisor=k_max_m_divisor)
        if curves[m]["status"] != "ok":
            return {
                "status": "divergence_curve_not_computable", "lambda_1": None,
                "r_squared": None, "window": None, "curves": curves,
                "reason": f"m={m}: {curves[m]['status']}",
            }

    # align on the shortest k-range across the three m (they may differ
    # slightly in M and therefore in k_max)
    common_len = min(len(curves[m]["k"]) for m in m_list)
    if common_len < min_len:
        return {"status": "divergence_curve_not_computable", "lambda_1": None,
                "r_squared": None, "window": None, "curves": curves,
                "reason": "common_k_range_too_short"}

    k_common = np.array(curves[m_list[0]]["k"][:common_len], dtype=float)
    y_by_m = {m: np.array(curves[m]["y"][:common_len], dtype=float) for m in m_list}

    region = find_stable_scaling_region(k_common, y_by_m, m_list, tol=tol, min_len=min_len, min_r2=min_r2)

    if region["status"] != "ok":
        return {
            "status": "linear_region_not_resolved", "lambda_1": None, "r_squared": None,
            "window": None, "curves": curves,
            "n_windows_tested": region["n_windows_tested"],
            "n_windows_stable": region["n_windows_stable"],
        }

    return {
        "status": "ok",
        "lambda_1": region["slope_m_star"],
        "r_squared": region["r_squared_m_star"],
        "window": region["window"],
        "slopes_all_m": region["slopes_all_m"],
        "n_windows_tested": region["n_windows_tested"],
        "n_windows_stable": region["n_windows_stable"],
        "curves": curves,
    }


# ==========================================================================
# D2: correlation dimension (Grassberger & Procaccia 1983), same scaling-
# region rule applied to log C(r) vs log r
# ==========================================================================

def correlation_integral_curve(x, m, tau, w, n_radii=D2_N_RADII, min_pairs=D2_MIN_PAIRS):
    """log C(r) vs log r for embedding dimension m (Grassberger & Procaccia
    1983), pairs restricted to |i-j|>w (same Theiler window as lambda_1).
    Radii log-spaced between the 1st and 99th percentile of the pairwise-
    distance distribution (robust range, avoids extreme outlier radii).

    Returns dict: log_r (list), log_C (list, nan where undefined), M,
    status.
    """
    x = np.asarray(x, dtype=float)
    Y = takens_embed(x, m, tau)
    M = Y.shape[0]
    if M < MIN_THEILER_POINTS:
        return {"log_r": [], "log_C": [], "M": int(M), "status": "insufficient_embedded_points"}

    D = squareform(pdist(Y, metric="euclidean"))
    ii, jj = np.meshgrid(np.arange(M), np.arange(M), indexing="ij")
    mask = np.abs(ii - jj) > w
    if not np.any(mask):
        return {"log_r": [], "log_C": [], "M": int(M), "status": "theiler_window_excludes_all_pairs"}

    dvals = D[mask]
    dvals_pos = dvals[dvals > 0]
    if dvals_pos.size < min_pairs:
        return {"log_r": [], "log_C": [], "M": int(M), "status": "insufficient_pairs"}

    r_lo, r_hi = np.percentile(dvals_pos, [1, 99])
    if r_hi <= r_lo:
        return {"log_r": [], "log_C": [], "M": int(M), "status": "degenerate_distance_range"}
    radii = np.logspace(np.log10(r_lo), np.log10(r_hi), n_radii)

    n_pairs_total = float(dvals.size)
    log_r, log_C = [], []
    for r in radii:
        count = float(np.sum(dvals <= r))
        if count < min_pairs:
            log_r.append(float(np.log(r)))
            log_C.append(float("nan"))
            continue
        c_r = count / n_pairs_total
        log_r.append(float(np.log(r)))
        log_C.append(float(np.log(c_r)))

    return {"log_r": log_r, "log_C": log_C, "M": int(M), "status": "ok"}


def compute_d2(x, m_star, tau, w, n_radii=D2_N_RADII, min_pairs=D2_MIN_PAIRS,
               tol=SLOPE_STABILITY_TOL, min_len=MIN_FIT_LEN, min_r2=MIN_R2_FOR_LINEAR_REGION):
    """Full D2 pipeline: correlation-integral curves at m*, m*+1, m*+2,
    SAME Kantz-Schreiber scaling-region rule as lambda_1, applied to
    log C(r) vs log r."""
    m_list = [m_star, m_star + 1, m_star + 2]
    curves = {}
    for m in m_list:
        curves[m] = correlation_integral_curve(x, m, tau, w, n_radii=n_radii, min_pairs=min_pairs)
        if curves[m]["status"] != "ok":
            return {"status": "correlation_integral_not_computable", "D2": None,
                    "window": None, "curves": curves, "reason": f"m={m}: {curves[m]['status']}"}

    log_r = np.array(curves[m_list[0]]["log_r"], dtype=float)
    y_by_m = {m: np.array(curves[m]["log_C"], dtype=float) for m in m_list}

    region = find_stable_scaling_region(log_r, y_by_m, m_list, tol=tol, min_len=min_len, min_r2=min_r2)
    if region["status"] != "ok":
        return {"status": "scaling_region_not_resolved", "D2": None, "window": None,
                "curves": curves, "n_windows_tested": region["n_windows_tested"],
                "n_windows_stable": region["n_windows_stable"]}

    return {
        "status": "ok", "D2": region["slope_m_star"], "r_squared": region["r_squared_m_star"],
        "window": region["window"], "slopes_all_m": region["slopes_all_m"],
        "n_windows_tested": region["n_windows_tested"], "n_windows_stable": region["n_windows_stable"],
        "curves": curves,
    }


# ==========================================================================
# Full pipeline for one segment, GIVEN an already-fixed (m, tau)
# ==========================================================================

def compute_lle_features(x, m_star, tau, k_max_cap=K_MAX_CAP, k_max_m_divisor=K_MAX_M_DIVISOR,
                          n_radii=D2_N_RADII, tol=SLOPE_STABILITY_TOL, min_len=MIN_FIT_LEN,
                          min_r2=MIN_R2_FOR_LINEAR_REGION):
    """Compute lambda_1 + D2 for one segment given the ALREADY-FIXED (m*,
    tau) (shared-embedding convention). Theiler window w is computed HERE,
    per-condition, from this specific series (NOT shared across
    conditions -- see module docstring)."""
    w_info = theiler_window(x)
    if w_info["status"] != "ok":
        return {"status": "theiler_not_resolved", "w_info": w_info, "lambda1_result": None,
                "d2_result": None}
    w = w_info["w"]

    lambda1_result = compute_lambda1(x, m_star, tau, w, k_max_cap=k_max_cap,
                                      k_max_m_divisor=k_max_m_divisor, tol=tol, min_len=min_len,
                                      min_r2=min_r2)
    d2_result = compute_d2(x, m_star, tau, w, n_radii=n_radii, tol=tol, min_len=min_len, min_r2=min_r2)

    return {
        "status": "ok", "w_info": w_info, "lambda1_result": lambda1_result, "d2_result": d2_result,
        "n_samples": int(len(x)), "m": int(m_star), "tau": int(tau),
    }


# ==========================================================================
# Full PRE/POST transition test pipeline (public entry point)
# ==========================================================================

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def run_lle_analysis(pre_series, post_series, seed=SEED, n_mc=None, n_iter=N_IAAFT_ITER,
                      max_n=MAX_N_PER_SEGMENT, fnn_m_max=FNN_M_MAX, tol=SLOPE_STABILITY_TOL,
                      min_len=MIN_FIT_LEN, run_bootstrap=False, n_bootstrap=N_BOOTSTRAP):
    """Run the full LLE transition test between a PRE and a POST segment,
    per METHODOLOGY_NOTE.md.

    Steps:
      1. Subsampling (MAX_N_PER_SEGMENT=5000) applied to PRE and POST
         independently.
      2. tau estimated from (subsampled) PRE via rqa_common.estimate_tau.
      3. m estimated from (subsampled) PRE via rqa_common.estimate_m
         (FNN, R_tol=10, A_tol=2, m<=10). *** HARD REJECT
         (status="embedding_not_resolved") if no m<=10 resolves -- NO
         fallback to a forced default m. This check happens BEFORE any
         lambda_1/D2 computation is attempted, per the mandatory rule in
         METHODOLOGY_NOTE.md. ***
      4. (m, tau) FIXED from PRE, applied to POST and to every surrogate of
         both (shared-embedding convention). Theiler window w computed
         independently per condition (real PRE, real POST, each surrogate).
      5. lambda_1 (Rosenstein, Kantz-Schreiber scaling region) and D2
         (Grassberger-Procaccia, same scaling-region rule) computed for
         real PRE and POST.
      6. IAAFT is the PRIMARY significance test: N_SURROGATES independent
         PRE/POST surrogate pairs, each generated from its OWN real
         (already-subsampled) segment, seed=12345. Two-tailed p-values for
         Delta_lambda1 and Delta_D2.
      7. If run_bootstrap=True, ALSO runs the moving-block bootstrap
         (Kunsch 1989) fallback (pre-authorized only if synthetic
         validation shows a low-power, not structural, failure). Off by
         default.

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
            "status": "tau_not_resolved", "tau_info": tau_info, "m_info": None,
            "diagnostics": {"pre_subsampling": pre_sub_info, "post_subsampling": post_sub_info},
        }
    tau = tau_info["tau"]

    # *** MANDATORY HARD-REJECT GATE (METHODOLOGY_NOTE.md) -- must occur
    # BEFORE any lambda_1/D2 computation, no forced fallback m. ***
    m_info = estimate_m(pre, tau, m_max=fnn_m_max)
    if m_info["status"] != "ok":
        return {
            "status": "embedding_not_resolved", "tau_info": tau_info, "m_info": m_info,
            "diagnostics": {"pre_subsampling": pre_sub_info, "post_subsampling": post_sub_info},
        }
    m = m_info["m"]

    real_pre = compute_lle_features(pre, m, tau, tol=tol, min_len=min_len)
    real_post = compute_lle_features(post, m, tau, tol=tol, min_len=min_len)

    def _extract(res, key, subkey):
        if res is None or res["status"] != "ok":
            return None
        sub = res.get(f"{subkey}_result")
        if sub is None or sub.get("status") != "ok":
            return None
        return sub.get(key)

    lambda1_pre = _extract(real_pre, "lambda_1", "lambda1")
    lambda1_post = _extract(real_post, "lambda_1", "lambda1")
    d2_pre = _extract(real_pre, "D2", "d2")
    d2_post = _extract(real_post, "D2", "d2")

    delta_lambda1_real = _delta(lambda1_post, lambda1_pre)
    delta_d2_real = _delta(d2_post, d2_pre)

    rng = np.random.default_rng(seed)
    surr_delta_lambda1, surr_delta_d2 = [], []
    n_undef_lambda1, n_undef_d2 = 0, 0

    for _ in range(n_surrogates):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        feat_pre_s = compute_lle_features(surr_pre, m, tau, tol=tol, min_len=min_len)
        feat_post_s = compute_lle_features(surr_post, m, tau, tol=tol, min_len=min_len)

        l1_pre_s = _extract(feat_pre_s, "lambda_1", "lambda1")
        l1_post_s = _extract(feat_post_s, "lambda_1", "lambda1")
        l1_delta = _delta(l1_post_s, l1_pre_s)
        if l1_delta is None:
            n_undef_lambda1 += 1
        else:
            surr_delta_lambda1.append(l1_delta)

        d2_pre_s = _extract(feat_pre_s, "D2", "d2")
        d2_post_s = _extract(feat_post_s, "D2", "d2")
        d2_delta = _delta(d2_post_s, d2_pre_s)
        if d2_delta is None:
            n_undef_d2 += 1
        else:
            surr_delta_d2.append(d2_delta)

    surr_delta_lambda1 = np.array(surr_delta_lambda1, dtype=float)
    surr_delta_d2 = np.array(surr_delta_d2, dtype=float)

    if delta_lambda1_real is None or len(surr_delta_lambda1) == 0:
        p_lambda1 = None
    else:
        p_lambda1 = float(np.mean(np.abs(surr_delta_lambda1) >= abs(delta_lambda1_real)))

    if delta_d2_real is None or len(surr_delta_d2) == 0:
        p_d2 = None
    else:
        p_d2 = float(np.mean(np.abs(surr_delta_d2) >= abs(delta_d2_real)))

    result = {
        "status": "ok",
        "m": m, "tau": tau, "tau_info": tau_info, "m_info": m_info,
        "real_pre": real_pre, "real_post": real_post,
        "lambda1_pre": lambda1_pre, "lambda1_post": lambda1_post,
        "d2_pre": d2_pre, "d2_post": d2_post,
        "delta_lambda1": delta_lambda1_real, "delta_d2": delta_d2_real,
        "p_lambda1": p_lambda1, "p_d2": p_d2,
        "surrogate_lambda1_mean": float(np.mean(surr_delta_lambda1)) if len(surr_delta_lambda1) else None,
        "surrogate_lambda1_std": float(np.std(surr_delta_lambda1)) if len(surr_delta_lambda1) else None,
        "surrogate_lambda1_n_valid": int(len(surr_delta_lambda1)),
        "surrogate_lambda1_n_undefined": int(n_undef_lambda1),
        "surrogate_d2_mean": float(np.mean(surr_delta_d2)) if len(surr_delta_d2) else None,
        "surrogate_d2_std": float(np.std(surr_delta_d2)) if len(surr_delta_d2) else None,
        "surrogate_d2_n_valid": int(len(surr_delta_d2)),
        "surrogate_d2_n_undefined": int(n_undef_d2),
        "diagnostics": {
            "pre_subsampling": pre_sub_info, "post_subsampling": post_sub_info,
            "pre_status": real_pre["status"], "post_status": real_post["status"],
        },
        "config": {
            "max_n_per_segment": max_n, "n_surrogates": n_surrogates,
            "n_iaaft_iter": n_iter, "seed": seed, "slope_stability_tol": tol,
            "min_fit_len": min_len, "fnn_m_max": fnn_m_max,
        },
    }

    if run_bootstrap:
        boot_result = run_block_bootstrap_test_lle(
            pre, post, m, tau, real_pre=real_pre, real_post=real_post,
            n_bootstrap=n_bootstrap, seed=seed, tol=tol, min_len=min_len,
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


def run_block_bootstrap_test_lle(pre_segment, post_segment, m, tau, real_pre=None, real_post=None,
                                  n_bootstrap=N_BOOTSTRAP, seed=SEED, tol=SLOPE_STABILITY_TOL,
                                  min_len=MIN_FIT_LEN):
    """Moving-block bootstrap (Kunsch 1989) significance test for
    Delta_lambda1 / Delta_D2, block length L = max(2*tau, 10) (same
    convention as rqa_common.run_block_bootstrap_test)."""
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    def _extract(res, key, subkey):
        if res is None or res["status"] != "ok":
            return None
        sub = res.get(f"{subkey}_result")
        if sub is None or sub.get("status") != "ok":
            return None
        return sub.get(key)

    if real_pre is None:
        real_pre = compute_lle_features(pre, m, tau, tol=tol, min_len=min_len)
    if real_post is None:
        real_post = compute_lle_features(post, m, tau, tol=tol, min_len=min_len)

    L = max(2 * tau, 10)
    rng = np.random.default_rng(seed)

    l1_boot_pre, d2_boot_pre = [], []
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(pre, L, rng)
        feat = compute_lle_features(resampled, m, tau, tol=tol, min_len=min_len)
        l1_boot_pre.append(_extract(feat, "lambda_1", "lambda1"))
        d2_boot_pre.append(_extract(feat, "D2", "d2"))

    l1_boot_post, d2_boot_post = [], []
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(post, L, rng)
        feat = compute_lle_features(resampled, m, tau, tol=tol, min_len=min_len)
        l1_boot_post.append(_extract(feat, "lambda_1", "lambda1"))
        d2_boot_post.append(_extract(feat, "D2", "d2"))

    def _pair_deltas(pre_vals, post_vals):
        deltas, n_undef = [], 0
        for vp, vq in zip(pre_vals, post_vals):
            if vp is None or vq is None:
                n_undef += 1
            else:
                deltas.append(vq - vp)
        return np.array(deltas, dtype=float), n_undef

    delta_l1_boot, n_undef_l1 = _pair_deltas(l1_boot_pre, l1_boot_post)
    delta_d2_boot, n_undef_d2 = _pair_deltas(d2_boot_pre, d2_boot_post)

    result = {"bootstrap_block_length": int(L), "bootstrap_n_bootstrap": int(n_bootstrap),
              "bootstrap_seed": int(seed)}
    for name, deltas, n_undef in (("lambda1", delta_l1_boot, n_undef_l1),
                                   ("d2", delta_d2_boot, n_undef_d2)):
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
