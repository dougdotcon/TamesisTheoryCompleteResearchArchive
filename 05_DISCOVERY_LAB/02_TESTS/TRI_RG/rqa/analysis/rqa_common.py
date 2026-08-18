"""
Canonical Recurrence Quantification Analysis (RQA) pipeline for
DISC-TRI-RG-001, candidate `rqa` (7th and final candidate identified for
this test line, see ../../phase0/PHASE0_5_SURVEY_NEW_CANDIDATES.md,
candidate 4).

Fixed BEFORE running on any real domain (NASA PCoE IMS/Rexnord bearing
run-to-failure, Kilauea 2018 volcanic seismology) -- see
../METHODOLOGY_NOTE.md for the full rationale. This is a NEW, self-contained
implementation specific to this test line: it does not import from, and is
not derived from, `visibility_graph/analysis/vg_common.py`,
`mse_multiscale_entropy/analysis/mse_common.py`, or any other pipeline in
this lab, even though the IAAFT surrogate step is conceptually the same
published method (Schreiber & Schmitz 1996) required by the methodology
note for cross-line consistency, and the moving-block-bootstrap fallback
(if triggered) is conceptually the same published method (Kunsch 1989)
used as the DFA-line's Adendo ao Gap (c) / SOC-line / VG-line fallback.

Method (METHODOLOGY_NOTE.md Gap (a)):
  1. Takens delay embedding: y_i = (x_i, x_{i+tau}, ..., x_{i+(m-1)*tau}).
     - tau: first local minimum of the time-delayed average mutual
       information (Fraser & Swinney 1986, Phys. Rev. A 33:1134), 16-bin
       histogram, lag = 1 .. min(200, floor(N/10)). Fallback (documented a
       priori, not chosen after seeing which domain needs it): first
       zero-crossing of the linear autocorrelation, if no MI local minimum
       is found in range.
     - m: False Nearest Neighbors (Kennel, Brown & Abarbanel 1992, Phys.
       Rev. A 45:3403), R_tol=10, A_tol=2, m=1..10, stop at first m with
       FNN fraction < 1%. Domain REJECTED (embedding_not_resolved) if no
       m<=10 works -- never forced to an arbitrary m.
     - Shared-embedding convention: (m, tau) estimated ONCE from PRE, the
       SAME (m, tau) applied to POST and to every surrogate of both (never
       re-estimated per condition/surrogate).
  2. Recurrence matrix: Chebyshev (max-norm) distance, fixed recurrence
     rate RR_target=0.05 (Marwan et al. 2007, Physics Reports 438:237),
     epsilon found independently per condition (closed-form quantile
     threshold of the pairwise-distance distribution -- mathematically
     equivalent to a converged bisection search on a monotonic threshold
     function, see `find_epsilon_for_rr` docstring) so THAT condition's own
     recurrence matrix hits RR_target. Theiler window w=tau excluded from
     recurrence counting (|i-j| <= w masked out, including the main
     diagonal).
  3. %DET (determinism, l_min=2) and ENTR (Shannon entropy of the diagonal
     line-length distribution P(l), l>=l_min) -- exact Marwan et al. 2007
     formulas.
  4. MAX_N_PER_SEGMENT=5000 subsampling (uniform stride decimation),
     applied identically regardless of domain (Gap (d)).
  5. IAAFT surrogates (Schreiber & Schmitz 1996) are the PRIMARY
     significance test (Gap (e)): N_SURROGATES=200, N_IAAFT_ITER=50,
     seed=12345, PRE/POST surrogates generated independently from their own
     real series, each surrogate re-run through the ALREADY-FIXED real
     (m, tau) + its own per-surrogate epsilon search + %DET/ENTR. Two-tailed
     p-values for Delta_DET and Delta_ENTR.

Any agent applying this pipeline to real data MUST import and call
`run_rqa_analysis` (or the lower-level helpers) rather than reimplementing
any of this, so "same formula, no per-domain reformulation" is a literal
code-identity guarantee, matching the discipline already used elsewhere in
this lab.
"""
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist

# ---- fixed constants (METHODOLOGY_NOTE.md Gaps (a), (d), (e) -- identical
# for every domain this pipeline is ever applied to; no per-domain tuning) --

# tau (Gap a): time-delayed mutual information
MI_N_BINS = 16                  # standard literature convention
MI_LAG_MAX_CAP = 200            # min(200, floor(N/10))
MI_LAG_MAX_N_DIVISOR = 10

# m (Gap a): False Nearest Neighbors (Kennel, Brown & Abarbanel 1992)
FNN_R_TOL = 10.0                # original paper value
FNN_A_TOL = 2.0                 # original paper value
FNN_M_MAX = 10                  # a priori ceiling
FNN_THRESHOLD_FRAC = 0.01       # stop at first m with FNN fraction < 1%
FNN_MIN_POINTS = 30             # below this, m-scan aborted, embedding rejected

# Recurrence matrix (Gap a): fixed recurrence rate, Chebyshev distance
RR_TARGET = 0.05                # Marwan et al. 2007 standard convention
L_MIN = 2                       # minimum diagonal line length for DET/ENTR
MIN_EMBEDDED_POINTS = 10        # below this, recurrence computation undefined

MAX_N_PER_SEGMENT = 5000        # subsampling cap, Gap (d)
N_SURROGATES = 200              # IAAFT surrogate pairs (Schreiber & Schmitz 1996), Gap (e)
N_IAAFT_ITER = 50               # IAAFT iterations per surrogate, Gap (e)
SEED = 12345                    # Gap (e)

# Moving-block bootstrap (Kunsch 1989) -- NOT part of the original
# METHODOLOGY_NOTE.md Gap (e) primary protocol, but PRE-AUTHORIZED there as a
# fallback ("adicionar teste complementar de bootstrap por blocos moveis...
# como PRIMARIO, mesma correcao ja aplicada 2x nesta linha (DFA, SOC), ANTES
# de tocar dado real") if synthetic validation shows the same IAAFT low-power
# failure mode already documented for DFA-alpha. See VALIDATION_NOTE.md for
# whether this path was exercised/needed for RQA.
N_BOOTSTRAP = 1000


# ==========================================================================
# Gap (d): subsampling for O(N^2) cost, applied identically to every domain
# ==========================================================================

def subsample_segment(x, max_n=MAX_N_PER_SEGMENT):
    """Uniform-stride decimation to at most `max_n` samples.

    If len(x) <= max_n, returns x unchanged (stride=1, subsampled=False).
    Otherwise stride = ceil(N / max_n), x[::stride] (Gap (d) -- identical
    rule for every domain, fixed a priori, decided before knowing whether
    any given segment actually exceeds the limit).
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    if N <= max_n:
        return x.copy(), {"n_original": int(N), "n_used": int(N), "stride": 1, "subsampled": False}
    stride = int(np.ceil(N / max_n))
    decimated = x[::stride]
    return decimated, {
        "n_original": int(N), "n_used": int(len(decimated)), "stride": int(stride),
        "subsampled": True,
    }


# ==========================================================================
# Gap (a): tau via time-delayed mutual information (Fraser & Swinney 1986)
# ==========================================================================

def _mutual_information(x, lag, n_bins=MI_N_BINS, edges=None):
    """Average mutual information I(x_t; x_{t+lag}), 16-bin 2D histogram
    over the FULL series range (same bin edges reused across every lag for
    a consistent comparison), natural-log units (base is irrelevant for
    locating the minimum)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    if lag >= n:
        return np.nan
    a = x[: n - lag]
    b = x[lag:]
    if edges is None:
        lo, hi = x.min(), x.max()
        if hi <= lo:
            return np.nan
        edges = np.linspace(lo, hi, n_bins + 1)
    hist2d, _, _ = np.histogram2d(a, b, bins=[edges, edges])
    p_xy = hist2d / hist2d.sum()
    p_x = p_xy.sum(axis=1, keepdims=True)
    p_y = p_xy.sum(axis=0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = p_xy / (p_x * p_y)
        term = p_xy * np.log(ratio)
    term = np.where((p_xy > 0) & np.isfinite(term), term, 0.0)
    return float(term.sum())


def _first_zero_crossing_acf(x, lag_max):
    """Fallback: first lag in [1, lag_max] where the linear autocorrelation
    crosses (or reaches) zero from above -- standard fallback convention
    when MI is monotone decreasing without a local minimum in range."""
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    var = np.dot(x, x)
    if var <= 0:
        return None
    for lag in range(1, lag_max + 1):
        acf = np.dot(x[: len(x) - lag], x[lag:]) / var
        if acf <= 0:
            return lag
    return None


def estimate_tau(x, lag_max_cap=MI_LAG_MAX_CAP, lag_max_n_divisor=MI_LAG_MAX_N_DIVISOR,
                  n_bins=MI_N_BINS):
    """tau = first local minimum of time-delayed mutual information,
    lag=1..min(200, floor(N/10)); fallback = first zero-crossing of the
    linear autocorrelation if no local minimum is found (both decisions
    fixed a priori in METHODOLOGY_NOTE.md Gap (a)).

    Returns dict: tau (int or None), method ("mi_local_minimum" or
    "acf_zero_crossing_fallback" or None), mi_curve (list), lag_max (int),
    status ("ok" or "tau_not_resolved").
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    lag_max = min(lag_max_cap, int(np.floor(n / lag_max_n_divisor)))
    if lag_max < 2:
        return {"tau": None, "method": None, "mi_curve": [], "lag_max": lag_max,
                "status": "tau_not_resolved", "reason": "lag_max_too_small"}

    lo, hi = x.min(), x.max()
    edges = np.linspace(lo, hi, n_bins + 1) if hi > lo else None
    mi_curve = [_mutual_information(x, lag, n_bins=n_bins, edges=edges)
                for lag in range(1, lag_max + 1)]

    tau = None
    for k in range(1, len(mi_curve) - 1):
        if (np.isfinite(mi_curve[k - 1]) and np.isfinite(mi_curve[k]) and np.isfinite(mi_curve[k + 1])
                and mi_curve[k] < mi_curve[k - 1] and mi_curve[k] < mi_curve[k + 1]):
            tau = k + 1  # lag is 1-indexed, k is 0-indexed into mi_curve
            break

    if tau is not None:
        return {"tau": int(tau), "method": "mi_local_minimum", "mi_curve": mi_curve,
                "lag_max": lag_max, "status": "ok"}

    fallback_tau = _first_zero_crossing_acf(x, lag_max)
    if fallback_tau is not None:
        return {"tau": int(fallback_tau), "method": "acf_zero_crossing_fallback",
                "mi_curve": mi_curve, "lag_max": lag_max, "status": "ok"}

    return {"tau": None, "method": None, "mi_curve": mi_curve, "lag_max": lag_max,
            "status": "tau_not_resolved", "reason": "no_mi_minimum_no_acf_zero_crossing"}


# ==========================================================================
# Takens embedding
# ==========================================================================

def takens_embed(x, m, tau):
    """y_i = (x_i, x_{i+tau}, ..., x_{i+(m-1)*tau}), i=0..N-(m-1)*tau-1.
    Returns array shape (M, m), M = N-(m-1)*tau (>=0)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    M = n - (m - 1) * tau
    if M <= 0:
        return np.empty((0, m))
    idx = np.arange(M)[:, None] + tau * np.arange(m)[None, :]
    return x[idx]


# ==========================================================================
# Gap (a): m via False Nearest Neighbors (Kennel, Brown & Abarbanel 1992)
# ==========================================================================

def fnn_fraction(x, m, tau, r_tol=FNN_R_TOL, a_tol=FNN_A_TOL):
    """FNN fraction at embedding dimension m, for the given tau, per Kennel,
    Brown & Abarbanel (1992). Nearest-neighbor search uses Euclidean
    distance in the m-dim reconstructed space (standard convention for FNN;
    distinct from the Chebyshev metric used later for the RR-based
    recurrence matrix itself, which is a separate, later step per Gap (a)).

    A point i's neighbor j is FALSE if EITHER:
      1. |x_{i+m*tau} - x_{j+m*tau}| / R_i^m > r_tol   (Kennel criterion 1)
      2. sqrt(R_i^m^2 + (x_{i+m*tau}-x_{j+m*tau})^2) / R_A > a_tol
         (Kennel/Abarbanel criterion 2, R_A = attractor size = std(x))

    Points with R_i^m == 0 (coincident nearest neighbor) are excluded from
    the fraction (undefined ratio, standard convention).

    Returns dict: fraction (float or None), n_valid (int), n_points (int),
    status ("ok" or "insufficient_points").
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    npts = n - m * tau  # need x[i + m*tau] defined for i = 0..npts-1
    if npts < FNN_MIN_POINTS:
        return {"fraction": None, "n_valid": 0, "n_points": npts, "status": "insufficient_points"}

    Y_m = takens_embed(x, m, tau)[:npts]  # shape (npts, m); takens_embed gives N-(m-1)*tau >= npts rows
    tree = cKDTree(Y_m)
    dist, idx = tree.query(Y_m, k=2)
    r_m = dist[:, 1]
    nn_idx = idx[:, 1]

    valid = r_m > 0
    if not np.any(valid):
        return {"fraction": None, "n_valid": 0, "n_points": npts, "status": "degenerate_zero_distances"}

    R_A = float(np.std(x))
    ext_diff = x[np.arange(npts) + m * tau] - x[nn_idx + m * tau]

    r_m_v = r_m[valid]
    ext_diff_v = ext_diff[valid]

    crit1 = np.abs(ext_diff_v) / r_m_v > r_tol
    r_m1 = np.sqrt(r_m_v ** 2 + ext_diff_v ** 2)
    crit2 = (r_m1 / R_A) > a_tol if R_A > 0 else np.zeros_like(crit1, dtype=bool)

    is_false = crit1 | crit2
    n_valid = int(valid.sum())
    fraction = float(is_false.sum()) / n_valid

    return {"fraction": fraction, "n_valid": n_valid, "n_points": npts, "status": "ok"}


def estimate_m(x, tau, m_max=FNN_M_MAX, r_tol=FNN_R_TOL, a_tol=FNN_A_TOL,
                threshold=FNN_THRESHOLD_FRAC):
    """m = first value in 1..m_max whose FNN fraction < threshold (1%).
    Domain REJECTED (status="embedding_not_resolved") if no m<=m_max works
    -- never forced to an arbitrary m (METHODOLOGY_NOTE.md Gap (a)).

    Returns dict: m (int or None), fnn_curve (list of per-m dicts),
    status ("ok" or "embedding_not_resolved"), reason (if rejected).
    """
    fnn_curve = []
    for m in range(1, m_max + 1):
        res = fnn_fraction(x, m, tau, r_tol=r_tol, a_tol=a_tol)
        fnn_curve.append({"m": m, **res})
        if res["status"] == "insufficient_points":
            # larger m only shrinks npts further -- stop scanning early
            return {"m": None, "fnn_curve": fnn_curve, "status": "embedding_not_resolved",
                    "reason": f"insufficient_points_at_m={m}"}
        if res["status"] == "ok" and res["fraction"] is not None and res["fraction"] < threshold:
            return {"m": m, "fnn_curve": fnn_curve, "status": "ok"}

    return {"m": None, "fnn_curve": fnn_curve, "status": "embedding_not_resolved",
            "reason": f"no_m_le_{m_max}_below_threshold"}


# ==========================================================================
# Gap (a): recurrence matrix, fixed RR, Chebyshev distance, Theiler window
# ==========================================================================

def find_epsilon_for_rr(D, mask, rr_target=RR_TARGET):
    """epsilon such that the fraction of MASKED pairs with distance <=
    epsilon equals rr_target, i.e. the RR_target-quantile of the
    Theiler-window-excluded pairwise-distance distribution.

    This is a closed-form implementation of "epsilon search to hit
    RR_target": since RR(epsilon) = P(D <= epsilon | mask) is monotonically
    non-decreasing in epsilon, its inverse at rr_target IS exactly the
    value a bisection search on RR(epsilon) - rr_target would converge to
    (up to float precision) -- np.quantile computes this directly rather
    than iterating, mathematically equivalent to "bisection or similar"
    per METHODOLOGY_NOTE.md Gap (a), just without the iteration loop.
    """
    vals = D[mask]
    if vals.size == 0:
        return None
    return float(np.quantile(vals, rr_target))


def diagonal_run_lengths(R):
    """All diagonal True-run lengths in boolean matrix R (M x M), across
    every diagonal offset, vectorized (no per-diagonal Python loop -- see
    module-level performance note below).

    Geometry: for offset d = j - i, diag_seq[d + M - 1, i] = R[i, i + d]
    (valid range only). Built via a single "skew" pass (M row-assignments,
    each a vectorized numpy slice write) producing shifted of shape
    (M, 2M-1), then diag_seq = shifted.T has one ROW per diagonal, values
    ordered by increasing i (temporal order) along each row -- run-length
    encoding is then done for ALL diagonals simultaneously via one
    pad + diff + argwhere pass (not one Python loop iteration per
    diagonal), which is what keeps this tractable at M up to
    MAX_N_PER_SEGMENT=5000 (diagonal count ~2M, naive per-diagonal Python
    looping would be far slower).
    """
    M = R.shape[0]
    if M == 0:
        return np.array([], dtype=int)
    R = np.asarray(R, dtype=bool)
    width = 2 * M - 1
    shifted = np.zeros((M, width), dtype=bool)
    for i in range(M):
        shifted[i, (M - 1 - i):(2 * M - 1 - i)] = R[i]
    diag_seq = shifted.T  # (width, M): row = diagonal, col = position (increasing i)

    padded = np.zeros((width, M + 2), dtype=bool)
    padded[:, 1:-1] = diag_seq
    d = np.diff(padded.astype(np.int8), axis=1)
    starts = np.argwhere(d == 1)
    ends = np.argwhere(d == -1)
    if len(starts) == 0:
        return np.array([], dtype=int)
    lengths = ends[:, 1] - starts[:, 1]
    return lengths


def compute_det_entr(Y, tau, rr_target=RR_TARGET, l_min=L_MIN):
    """Full recurrence-matrix + %DET/ENTR computation for one already-
    embedded segment Y (shape (M, m)).

    Theiler window w=tau: pairs with |i-j| <= w excluded from BOTH the
    epsilon search and the recurrence matrix itself (this also removes the
    main diagonal, i=j, since tau >= 1).

    %DET = sum_{l>=l_min} l*P(l) / sum_{l>=1} l*P(l)   (Marwan et al. 2007)
    ENTR = -sum_{l>=l_min} p(l) ln p(l), p(l) = P(l) / sum_{l>=l_min} P(l)
           (Shannon entropy of the diagonal-line-length distribution,
           normalized over l>=l_min, standard Marwan et al. 2007 convention
           -- same l_min as %DET for consistency).

    Returns dict: status ("ok" / "recurrence_undefined" / "insufficient_embedded_points"),
    M (n embedded points), epsilon, achieved_rr, DET, ENTR, n_lines,
    mean_diagonal_length, l_min.
    """
    M = Y.shape[0]
    if M < MIN_EMBEDDED_POINTS:
        return {"status": "insufficient_embedded_points", "M": int(M), "epsilon": None,
                "achieved_rr": None, "DET": None, "ENTR": None, "n_lines": 0,
                "mean_diagonal_length": None, "l_min": l_min}

    D = cdist(Y, Y, metric="chebyshev")
    ii, jj = np.meshgrid(np.arange(M), np.arange(M), indexing="ij")
    mask = np.abs(ii - jj) > tau

    if not np.any(mask):
        return {"status": "recurrence_undefined", "M": int(M), "epsilon": None,
                "achieved_rr": None, "DET": None, "ENTR": None, "n_lines": 0,
                "mean_diagonal_length": None, "l_min": l_min}

    epsilon = find_epsilon_for_rr(D, mask, rr_target=rr_target)
    if epsilon is None:
        return {"status": "recurrence_undefined", "M": int(M), "epsilon": None,
                "achieved_rr": None, "DET": None, "ENTR": None, "n_lines": 0,
                "mean_diagonal_length": None, "l_min": l_min}

    R = (D <= epsilon) & mask
    achieved_rr = float(R[mask].mean()) if mask.any() else None

    lengths = diagonal_run_lengths(R)
    if lengths.size == 0:
        return {"status": "ok", "M": int(M), "epsilon": epsilon, "achieved_rr": achieved_rr,
                "DET": 0.0, "ENTR": 0.0, "n_lines": 0, "mean_diagonal_length": None,
                "l_min": l_min}

    total_L = float(lengths.sum())
    ge_lmin = lengths[lengths >= l_min]
    det_L = float(ge_lmin.sum())
    DET = det_L / total_L if total_L > 0 else None

    if ge_lmin.size == 0:
        ENTR = 0.0
    else:
        counts = np.bincount(ge_lmin)
        counts = counts[counts > 0]
        p_l = counts / counts.sum()
        ENTR = float(-np.sum(p_l * np.log(p_l)))

    return {
        "status": "ok", "M": int(M), "epsilon": epsilon, "achieved_rr": achieved_rr,
        "DET": DET, "ENTR": ENTR, "n_lines": int(lengths.size),
        "mean_diagonal_length": float(lengths.mean()), "l_min": l_min,
    }


# ==========================================================================
# Full pipeline for one segment, GIVEN an already-fixed (m, tau)
# ==========================================================================

def compute_rqa_features(x, m, tau, rr_target=RR_TARGET, l_min=L_MIN):
    """Embed `x` with the GIVEN (m, tau) (not re-estimated -- shared-
    embedding convention, METHODOLOGY_NOTE.md Gap (a)) and compute
    %DET/ENTR via the fixed-RR recurrence matrix. Returns compute_det_entr's
    dict plus n_samples (pre-embedding) and m/tau used."""
    x = np.asarray(x, dtype=float)
    Y = takens_embed(x, m, tau)
    result = compute_det_entr(Y, tau, rr_target=rr_target, l_min=l_min)
    result["n_samples"] = int(len(x))
    result["m"] = int(m)
    result["tau"] = int(tau)
    return result


# ==========================================================================
# Gap (e): IAAFT surrogates (Schreiber & Schmitz 1996)
# ==========================================================================

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate.

    Preserves the linear power spectrum (FFT amplitude spectrum) and the
    exact empirical amplitude distribution (histogram) of `x`; destroys any
    nonlinear phase/temporal structure beyond what a linear Gaussian process
    with the same spectrum and marginal would produce. Independent
    reimplementation for this test line (same published method as
    `visibility_graph/analysis/vg_common.py`, Schreiber & Schmitz 1996, not
    imported from it).
    """
    if rng is None:
        rng = np.random.default_rng()
    x = np.asarray(x, dtype=float)
    n = len(x)
    target_sorted = np.sort(x)
    target_amp = np.abs(np.fft.rfft(x))

    current = rng.permutation(x).astype(float)
    for _ in range(n_iter):
        spectrum = np.fft.rfft(current)
        phase = np.angle(spectrum)
        spectrum_matched = target_amp * np.exp(1j * phase)
        series_spectrum_matched = np.fft.irfft(spectrum_matched, n=n)
        rank_order = np.argsort(np.argsort(series_spectrum_matched))
        current = target_sorted[rank_order]
    return current


# ==========================================================================
# Moving-block bootstrap (Kunsch 1989) -- pre-authorized fallback, only
# exercised as a PRIMARY test if validate_synthetic.py's power check
# requires it (see VALIDATION_NOTE.md for whether this path was taken).
# ==========================================================================

def moving_block_bootstrap_resample(x, L, rng):
    """One moving-block-bootstrap resample of `x` (Kunsch 1989): blocks of
    length L, start index drawn uniformly at random with replacement,
    concatenated until >= len(x), then trimmed to exactly len(x)."""
    x = np.asarray(x, dtype=float)
    N = len(x)
    L = int(L)
    if L < 1:
        L = 1
    if L > N:
        L = N
    n_blocks_needed = int(np.ceil(N / L))
    starts = rng.integers(0, N - L + 1, size=n_blocks_needed)
    pieces = [x[s:s + L] for s in starts]
    return np.concatenate(pieces)[:N]


def _percentile_ci95(arr):
    lo, hi = np.percentile(arr, [2.5, 97.5])
    return (float(lo), float(hi))


def _bootstrap_two_tailed_p(delta_arr):
    frac_le0 = float(np.mean(delta_arr <= 0))
    frac_ge0 = float(np.mean(delta_arr >= 0))
    return float(2 * min(frac_le0, frac_ge0))


def run_block_bootstrap_test(pre_segment, post_segment, m, tau, real_pre=None, real_post=None,
                              n_bootstrap=N_BOOTSTRAP, seed=SEED, rr_target=RR_TARGET, l_min=L_MIN):
    """Moving-block bootstrap (Kunsch 1989) significance test for
    Delta_DET / Delta_ENTR, block length L = tau-based (block length =
    max(2*tau, 10), tied to the embedding's own timescale, same spirit as
    other lines' block-length choices in this lab). PRE and POST resampled
    independently, n_bootstrap times each, i-th pairing. Each resample is
    embedded with the SAME already-fixed (m, tau) (never re-estimated),
    matching the real/surrogate convention."""
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    if real_pre is None:
        real_pre = compute_rqa_features(pre, m, tau, rr_target=rr_target, l_min=l_min)
    if real_post is None:
        real_post = compute_rqa_features(post, m, tau, rr_target=rr_target, l_min=l_min)

    L = max(2 * tau, 10)
    rng = np.random.default_rng(seed)

    det_boot_pre, entr_boot_pre = [], []
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(pre, L, rng)
        feat = compute_rqa_features(resampled, m, tau, rr_target=rr_target, l_min=l_min)
        det_boot_pre.append(feat["DET"] if feat["status"] == "ok" else None)
        entr_boot_pre.append(feat["ENTR"] if feat["status"] == "ok" else None)

    det_boot_post, entr_boot_post = [], []
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(post, L, rng)
        feat = compute_rqa_features(resampled, m, tau, rr_target=rr_target, l_min=l_min)
        det_boot_post.append(feat["DET"] if feat["status"] == "ok" else None)
        entr_boot_post.append(feat["ENTR"] if feat["status"] == "ok" else None)

    def _pair_deltas(pre_vals, post_vals):
        deltas, n_undef = [], 0
        for vp, vq in zip(pre_vals, post_vals):
            if vp is None or vq is None:
                n_undef += 1
            else:
                deltas.append(vq - vp)
        return np.array(deltas, dtype=float), n_undef

    delta_det_boot, n_undef_det = _pair_deltas(det_boot_pre, det_boot_post)
    delta_entr_boot, n_undef_entr = _pair_deltas(entr_boot_pre, entr_boot_post)

    result = {
        "bootstrap_block_length": int(L),
        "bootstrap_n_bootstrap": int(n_bootstrap),
        "bootstrap_seed": int(seed),
    }
    for name, deltas, n_undef in (("DET", delta_det_boot, n_undef_det),
                                   ("ENTR", delta_entr_boot, n_undef_entr)):
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


# ==========================================================================
# Full PRE/POST transition test pipeline (public entry point)
# ==========================================================================

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def run_rqa_analysis(pre_series, post_series, seed=SEED, n_mc=None,
                      n_iter=N_IAAFT_ITER, max_n=MAX_N_PER_SEGMENT,
                      rr_target=RR_TARGET, l_min=L_MIN,
                      run_bootstrap=False, n_bootstrap=N_BOOTSTRAP):
    """Run the full RQA transition test between a PRE and a POST segment,
    per METHODOLOGY_NOTE.md Gaps (a), (d), (e).

    `n_mc` (alias for the surrogate count, defaults to N_SURROGATES=200 if
    None) mirrors the calling convention requested for this candidate's
    public entry point.

    Steps:
      1. Gap (d) subsampling applied to PRE and POST independently BEFORE
         anything else (embedding, recurrence, AND surrogate generation all
         operate on the subsampled series).
      2. tau estimated from (subsampled) PRE via time-delayed MI (fallback:
         ACF zero-crossing).
      3. m estimated from (subsampled) PRE via FNN, using that tau. If no
         m<=10 resolves FNN<1%, the WHOLE domain is rejected
         (status="embedding_not_resolved") -- no further computation.
      4. (m, tau) FIXED from PRE, applied to POST (shared-embedding
         convention) and to every surrogate of both.
      5. %DET/ENTR computed for real PRE and POST via the fixed-RR
         recurrence matrix (each condition gets its OWN epsilon).
      6. IAAFT is the PRIMARY significance test: N_SURROGATES independent
         PRE/POST surrogate pairs, each generated from its OWN real
         (already-subsampled) segment, seed=12345. Two-tailed:
         p = fraction of surrogates with |Delta_surrogate| >= |Delta_real|.
      7. If `run_bootstrap=True`, ALSO runs the moving-block bootstrap
         (Kunsch 1989) fallback test (pre-authorized in METHODOLOGY_NOTE.md
         Gap (e) if synthetic validation shows IAAFT has insufficient
         power). Off by default.

    Returns a dict with everything a downstream agent needs to report a
    result without recomputing anything: m, tau (from PRE), epsilon per
    condition, %DET/ENTR (PRE/POST/Delta), IAAFT null distributions,
    p-values, diagnostics (n used, subsampling info, whether embedding/FNN
    succeeded), and (if requested) the bootstrap fallback result.
    """
    n_surrogates = N_SURROGATES if n_mc is None else int(n_mc)

    pre_raw = np.asarray(pre_series, dtype=float)
    post_raw = np.asarray(post_series, dtype=float)

    pre, pre_sub_info = subsample_segment(pre_raw, max_n=max_n)
    post, post_sub_info = subsample_segment(post_raw, max_n=max_n)

    tau_info = estimate_tau(pre)
    if tau_info["status"] != "ok":
        return {
            "status": "tau_not_resolved",
            "tau_info": tau_info,
            "m_info": None,
            "diagnostics": {"pre_subsampling": pre_sub_info, "post_subsampling": post_sub_info},
        }
    tau = tau_info["tau"]

    m_info = estimate_m(pre, tau)
    if m_info["status"] != "ok":
        return {
            "status": "embedding_not_resolved",
            "tau_info": tau_info,
            "m_info": m_info,
            "diagnostics": {"pre_subsampling": pre_sub_info, "post_subsampling": post_sub_info},
        }
    m = m_info["m"]

    real_pre = compute_rqa_features(pre, m, tau, rr_target=rr_target, l_min=l_min)
    real_post = compute_rqa_features(post, m, tau, rr_target=rr_target, l_min=l_min)

    DET_pre = real_pre["DET"] if real_pre["status"] == "ok" else None
    DET_post = real_post["DET"] if real_post["status"] == "ok" else None
    ENTR_pre = real_pre["ENTR"] if real_pre["status"] == "ok" else None
    ENTR_post = real_post["ENTR"] if real_post["status"] == "ok" else None

    delta_DET_real = _delta(DET_post, DET_pre)
    delta_ENTR_real = _delta(ENTR_post, ENTR_pre)

    rng = np.random.default_rng(seed)
    surr_delta_DET, surr_delta_ENTR = [], []
    n_undef_DET, n_undef_ENTR = 0, 0

    for _ in range(n_surrogates):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        feat_pre_s = compute_rqa_features(surr_pre, m, tau, rr_target=rr_target, l_min=l_min)
        feat_post_s = compute_rqa_features(surr_post, m, tau, rr_target=rr_target, l_min=l_min)

        det_pre_s = feat_pre_s["DET"] if feat_pre_s["status"] == "ok" else None
        det_post_s = feat_post_s["DET"] if feat_post_s["status"] == "ok" else None
        det_delta = _delta(det_post_s, det_pre_s)
        if det_delta is None:
            n_undef_DET += 1
        else:
            surr_delta_DET.append(det_delta)

        entr_pre_s = feat_pre_s["ENTR"] if feat_pre_s["status"] == "ok" else None
        entr_post_s = feat_post_s["ENTR"] if feat_post_s["status"] == "ok" else None
        entr_delta = _delta(entr_post_s, entr_pre_s)
        if entr_delta is None:
            n_undef_ENTR += 1
        else:
            surr_delta_ENTR.append(entr_delta)

    surr_delta_DET = np.array(surr_delta_DET, dtype=float)
    surr_delta_ENTR = np.array(surr_delta_ENTR, dtype=float)

    if delta_DET_real is None or len(surr_delta_DET) == 0:
        p_DET = None
    else:
        p_DET = float(np.mean(np.abs(surr_delta_DET) >= abs(delta_DET_real)))

    if delta_ENTR_real is None or len(surr_delta_ENTR) == 0:
        p_ENTR = None
    else:
        p_ENTR = float(np.mean(np.abs(surr_delta_ENTR) >= abs(delta_ENTR_real)))

    result = {
        "status": "ok",
        "m": m,
        "tau": tau,
        "tau_info": tau_info,
        "m_info": m_info,
        "real_pre": real_pre,
        "real_post": real_post,
        "DET_pre": DET_pre,
        "DET_post": DET_post,
        "ENTR_pre": ENTR_pre,
        "ENTR_post": ENTR_post,
        "delta_DET": delta_DET_real,
        "delta_ENTR": delta_ENTR_real,
        "p_DET": p_DET,
        "p_ENTR": p_ENTR,
        "surrogate_DET_mean": float(np.mean(surr_delta_DET)) if len(surr_delta_DET) else None,
        "surrogate_DET_std": float(np.std(surr_delta_DET)) if len(surr_delta_DET) else None,
        "surrogate_DET_n_valid": int(len(surr_delta_DET)),
        "surrogate_DET_n_undefined": int(n_undef_DET),
        "surrogate_ENTR_mean": float(np.mean(surr_delta_ENTR)) if len(surr_delta_ENTR) else None,
        "surrogate_ENTR_std": float(np.std(surr_delta_ENTR)) if len(surr_delta_ENTR) else None,
        "surrogate_ENTR_n_valid": int(len(surr_delta_ENTR)),
        "surrogate_ENTR_n_undefined": int(n_undef_ENTR),
        "diagnostics": {
            "pre_subsampling": pre_sub_info,
            "post_subsampling": post_sub_info,
            "pre_status": real_pre["status"],
            "post_status": real_post["status"],
            "pre_M": real_pre["M"],
            "post_M": real_post["M"],
        },
        "config": {
            "rr_target": rr_target,
            "l_min": l_min,
            "max_n_per_segment": max_n,
            "n_surrogates": n_surrogates,
            "n_iaaft_iter": n_iter,
            "seed": seed,
        },
    }

    if run_bootstrap:
        boot_result = run_block_bootstrap_test(
            pre, post, m, tau, real_pre=real_pre, real_post=real_post,
            n_bootstrap=n_bootstrap, seed=seed, rr_target=rr_target, l_min=l_min,
        )
        result.update(boot_result)

    return result
