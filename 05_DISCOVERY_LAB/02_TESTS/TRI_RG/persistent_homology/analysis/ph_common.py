"""
Canonical Persistent Homology / TDA (Vietoris-Rips filtration over a Takens
embedding) pipeline for DISC-TRI-RG-001, candidate `persistent-homology`
(11th and LAST candidate identified for this test line, see
../../phase0/PHASE0_6_SURVEY_NEW_CANDIDATES.md, candidate 3).

Fixed BEFORE running on any real domain (LIGO GW150914 strain, S&P500
around the Lehman Brothers bankruptcy) -- see ../METHODOLOGY_NOTE.md for
the full rationale. This is a NEW, self-contained implementation specific
to this test line: it does not import from, and is not derived from,
`rqa/analysis/rqa_common.py` or any other pipeline in this lab, even though
(a) the tau-via-mutual-information step is the SAME published method
(Fraser & Swinney 1986) already audited and working in `rqa_common.py`
(only the FNN embedding-dimension step failed there, and this candidate
deliberately does not use FNN at all -- see METHODOLOGY_NOTE.md Gap (a)),
and (b) the IAAFT surrogate step is conceptually the same published method
(Schreiber & Schmitz 1996) required by the methodology note for cross-line
consistency, and the moving-block-bootstrap fallback (if triggered) is
conceptually the same published method (Kunsch 1989) used elsewhere in
this lab.

Method (METHODOLOGY_NOTE.md Gaps (a), (b), (e)):
  1. Takens delay embedding: y_i = (x_i, x_{i+tau}, ..., x_{i+(m-1)*tau}).
     - m = 3, FIXED a priori (NOT FNN-estimated, NOT re-estimated per
       series) -- deliberately different from RQA's FNN rule, because
       persistent H1 detection of a loop feature does not need the same
       "fully unfold the attractor to avoid false neighbors" condition
       that a recurrence-threshold statistic like RQA's %DET needs
       (Perea & Harer 2015 use small fixed embedding dimensions for
       exactly this reason; Takens only requires m > 2*d_box, and a
       simple loop has d_box=1, so m=3 is comfortably sufficient).
     - tau: first local minimum of the time-delayed mutual information
       (Fraser & Swinney 1986, Phys. Rev. A 33:1134), 16-bin histogram,
       lag = 1 .. min(200, floor(N/10)). Fallback: first zero-crossing of
       the linear autocorrelation, if no MI local minimum is found in
       range -- SAME rule already audited and working in
       `rqa/analysis/rqa_common.py` (that part of RQA never failed; only
       its FNN step failed), reimplemented independently here (not
       imported across candidate directories).
     - UNLIKE RQA's shared-embedding convention (m,tau estimated once
       from PRE, reused everywhere): tau here is recalculated
       INDEPENDENTLY for EVERY series -- real PRE, real POST, and every
       IAAFT surrogate of both -- because MI-based tau estimation is
       cheap (no O(N^2) FNN neighbor search), so per-series
       recalculation is more faithful and does not introduce the same
       cost/bias tradeoff that motivated fixing (m,tau) from PRE alone
       in RQA (METHODOLOGY_NOTE.md Gap (e)).
  2. Sub-window design (controls the measured >O(N^2)-in-practice Rips
     cost, Phase 0.6: 3240 points = 16.4s/diagram single-core):
     N_WINDOW=200 embedded points per persistence diagram. Within each
     segment (PRE or POST), up to K_SUBWINDOWS_MAX=10 non-overlapping
     windows of N_WINDOW embedded points, evenly spaced to span the
     FULL available segment (not just the start) when more than 10
     non-overlapping windows are possible -- implemented as
     stride = M // K, starts = 0, stride, 2*stride, ..., (K-1)*stride
     (see `select_subwindow_starts` docstring for why this stride
     guarantees both non-overlap and full-segment coverage). If a
     segment has fewer than N_WINDOW embedded points available (cannot
     form even one window), the segment is REJECTED as
     `insufficient_samples` -- reported honestly, never forced.
  3. Vietoris-Rips + persistence: `ripser.ripser(point_cloud, maxdim=1)`
     on each N_WINDOW-point sub-window (H0/H1 only, per METHODOLOGY_NOTE.md
     Gap (b)). Max-H1-persistence = max(death-birth) over H1 features (0
     if none exist -- well-defined, not undefined). Total-H1-persistence
     = sum(death-birth) over all H1 features (0 if none). Any H1 feature
     with a non-finite death (essential class, not expected for a finite
     point cloud under maxdim=1 Vietoris-Rips in practice, but guarded
     explicitly rather than assumed impossible) is EXCLUDED from both
     statistics and counted separately -- an implementation detail the
     methodology note does not discuss explicitly, documented here rather
     than silently handled.
     I(X) primary = median (over the up-to-10 sub-windows) of
     max-H1-persistence. I(X) companion = median of total-H1-persistence.
  4. IAAFT surrogates (Schreiber & Schmitz 1996) are the PRIMARY
     significance test (Gap (e)): N_SURROGATES=200, N_IAAFT_ITER=50,
     seed=12345, PRE and POST surrogates generated INDEPENDENTLY from
     their own real series. Each surrogate goes through the FULL pipeline
     (its own recalculated tau, m=3, sub-windowing, Rips, persistence).
     Two-tailed p-values: p = fraction of surrogates with
     |Delta_surrogate| >= |Delta_real| (same convention as every other
     candidate in this line), computed separately for
     Delta_median_max_persistence and Delta_median_total_persistence.

Any agent applying this pipeline to real data MUST import and call
`run_ph_analysis` (or the lower-level helpers) rather than reimplementing
any of this, matching the discipline already used elsewhere in this lab.
"""
import numpy as np
from ripser import ripser

# ---- fixed constants (METHODOLOGY_NOTE.md Gaps (a), (b), (e) -- identical
# for every domain this pipeline is ever applied to; no per-domain tuning) --

# tau (Gap a): time-delayed mutual information (same rule as RQA's, own
# reimplementation)
MI_N_BINS = 16                  # standard literature convention
MI_LAG_MAX_CAP = 200            # min(200, floor(N/10))
MI_LAG_MAX_N_DIVISOR = 10

# m (Gap a): FIXED, not FNN-estimated -- the central deliberate deviation
# from RQA's embedding rule, see module docstring.
M_FIXED = 3

# Sub-window design (Gap b)
N_WINDOW = 200                  # embedded points per Rips diagram
K_SUBWINDOWS_MAX = 10           # up to this many non-overlapping sub-windows

# Vietoris-Rips (Gap b)
MAXDIM = 1                      # H0/H1 only

N_SURROGATES = 200              # IAAFT surrogate pairs (Schreiber & Schmitz 1996), Gap (e)
N_IAAFT_ITER = 50               # IAAFT iterations per surrogate, Gap (e)
SEED = 12345                    # Gap (e)

# Moving-block bootstrap (Kunsch 1989) -- NOT part of the original
# METHODOLOGY_NOTE.md Gap (e) primary protocol, but PRE-AUTHORIZED there as
# a fallback ("bootstrap por blocos moveis pre-autorizado (Kunsch 1989),
# mesma correcao ja aplicada 2x nesta linha") if synthetic validation shows
# the same IAAFT low-power failure mode already documented for DFA-alpha.
# See VALIDATION_NOTE.md for whether this path was exercised/needed.
N_BOOTSTRAP = 1000


# ==========================================================================
# Gap (a): tau via time-delayed mutual information (Fraser & Swinney 1986)
# -- same rule already audited/working in rqa/analysis/rqa_common.py,
# reimplemented independently here (no cross-candidate import).
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
# Takens embedding, m FIXED (Gap a -- the deliberate deviation from RQA)
# ==========================================================================

def takens_embed(x, m=M_FIXED, tau=1):
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
# Gap (b): sub-window selection -- up to K_SUBWINDOWS_MAX non-overlapping
# windows of N_WINDOW points, evenly spaced across the FULL segment.
# ==========================================================================

def select_subwindow_starts(M, n_window=N_WINDOW, k_max=K_SUBWINDOWS_MAX):
    """Choose up to k_max non-overlapping window start indices into an
    array of M embedded points, each window n_window points wide, spanning
    the FULL available range when more than k_max non-overlapping windows
    are possible.

    K = min(k_max, M // n_window)  (largest number of non-overlapping
    windows possible, capped at k_max). stride = M // K. starts =
    0, stride, 2*stride, ..., (K-1)*stride.

    This stride choice guarantees BOTH properties required by
    METHODOLOGY_NOTE.md Gap (b) simultaneously:
      - non-overlap: since K <= M // n_window, K*n_window <= M, so
        M/K >= n_window: because n_window is an integer and stride =
        floor(M/K) >= n_window follows directly (an integer <= a real
        number a is <= floor(a)), the gap between consecutive starts
        (stride) is always >= n_window, so windows [start, start+n_window)
        never overlap.
      - full-segment coverage: the last window starts at (K-1)*stride and
        ends at (K-1)*stride+n_window <= K*stride <= M, i.e. windows are
        spread with equal stride from the very start to as close to the
        very end of the segment as an integer number of non-overlapping
        windows allows (not clustered at the start).

    Returns (starts: list[int], K: int). Empty list if M < n_window
    (caller is responsible for reporting `insufficient_samples`).
    """
    if M < n_window:
        return [], 0
    max_possible = M // n_window
    K = min(k_max, max_possible)
    stride = M // K
    starts = [i * stride for i in range(K)]
    return starts, K


# ==========================================================================
# Gap (b): Vietoris-Rips + H1 persistence on one N_WINDOW-point sub-window
# ==========================================================================

def h1_persistence_stats(point_cloud, maxdim=MAXDIM):
    """Run ripser on one embedded point cloud, extract H1 birth-death
    pairs, and compute max-H1-persistence and total-H1-persistence.

    Well-defined (not undefined) when no H1 feature exists: both
    statistics are 0.0 in that case, per METHODOLOGY_NOTE.md Gap (b).

    Any H1 feature with a non-finite death (essential class -- not
    expected in practice for a finite point cloud under maxdim=1
    Vietoris-Rips, but guarded rather than assumed impossible) is
    EXCLUDED from both statistics and counted in `n_infinite_dropped`,
    an implementation detail the methodology note does not discuss
    explicitly.

    Returns dict: max_persistence, total_persistence, n_h1_features
    (finite only), n_infinite_dropped, diagram (list of [birth,death]).
    """
    result = ripser(np.asarray(point_cloud, dtype=float), maxdim=maxdim)
    dgm1 = result["dgms"][1] if len(result["dgms"]) > 1 else np.empty((0, 2))
    if dgm1.shape[0] == 0:
        return {"max_persistence": 0.0, "total_persistence": 0.0,
                "n_h1_features": 0, "n_infinite_dropped": 0, "diagram": []}

    finite_mask = np.isfinite(dgm1[:, 1])
    n_infinite = int((~finite_mask).sum())
    dgm1_finite = dgm1[finite_mask]

    if dgm1_finite.shape[0] == 0:
        return {"max_persistence": 0.0, "total_persistence": 0.0,
                "n_h1_features": 0, "n_infinite_dropped": n_infinite, "diagram": []}

    lifetimes = dgm1_finite[:, 1] - dgm1_finite[:, 0]
    return {
        "max_persistence": float(lifetimes.max()),
        "total_persistence": float(lifetimes.sum()),
        "n_h1_features": int(dgm1_finite.shape[0]),
        "n_infinite_dropped": n_infinite,
        "diagram": dgm1_finite.tolist(),
    }


# ==========================================================================
# Full I(X) computation for one segment: embed -> sub-window -> Rips ->
# median max/total persistence across sub-windows.
# ==========================================================================

def compute_ph_features(x, m=M_FIXED, tau=None, n_window=N_WINDOW, k_max=K_SUBWINDOWS_MAX,
                         recompute_tau=True):
    """Full per-segment pipeline: estimate tau (unless given), Takens-embed
    with FIXED m, select up to k_max non-overlapping N_WINDOW sub-windows
    spanning the segment, run Rips+H1 persistence on each, and return the
    median max/total persistence across sub-windows (I(X) primary and
    companion).

    Returns dict with status in {"ok", "tau_not_resolved",
    "insufficient_samples"}. On "ok": median_max_persistence,
    median_total_persistence, per_window (list of h1_persistence_stats
    dicts), n_subwindows_used, tau, tau_info, M (embedded point count),
    n_samples.
    """
    x = np.asarray(x, dtype=float)
    n_samples = int(len(x))

    tau_info = None
    if tau is None:
        tau_info = estimate_tau(x)
        if tau_info["status"] != "ok":
            return {"status": "tau_not_resolved", "tau_info": tau_info,
                    "n_samples": n_samples}
        tau = tau_info["tau"]

    Y = takens_embed(x, m=m, tau=tau)
    M = int(Y.shape[0])

    starts, K = select_subwindow_starts(M, n_window=n_window, k_max=k_max)
    if K == 0:
        return {"status": "insufficient_samples", "tau_info": tau_info, "tau": tau,
                "m": m, "M": M, "n_samples": n_samples, "n_window_required": n_window}

    per_window = []
    for s in starts:
        window = Y[s:s + n_window]
        per_window.append(h1_persistence_stats(window))

    max_vals = np.array([w["max_persistence"] for w in per_window], dtype=float)
    total_vals = np.array([w["total_persistence"] for w in per_window], dtype=float)

    return {
        "status": "ok",
        "tau": int(tau),
        "tau_info": tau_info,
        "m": int(m),
        "M": M,
        "n_samples": n_samples,
        "n_subwindows_used": K,
        "subwindow_starts": starts,
        "per_window": per_window,
        "median_max_persistence": float(np.median(max_vals)),
        "median_total_persistence": float(np.median(total_vals)),
    }


# ==========================================================================
# Gap (e): IAAFT surrogates (Schreiber & Schmitz 1996) -- independent
# reimplementation for this test line (same published method as
# rqa/analysis/rqa_common.py's, not imported from it).
# ==========================================================================

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate.

    Preserves the linear power spectrum (FFT amplitude spectrum) and the
    exact empirical amplitude distribution (histogram) of `x`; destroys
    any nonlinear phase/temporal structure beyond what a linear Gaussian
    process with the same spectrum and marginal would produce.
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


def run_block_bootstrap_test(pre_segment, post_segment, block_length=None, real_pre=None,
                              real_post=None, n_bootstrap=N_BOOTSTRAP, seed=SEED,
                              m=M_FIXED, n_window=N_WINDOW, k_max=K_SUBWINDOWS_MAX):
    """Moving-block bootstrap (Kunsch 1989) significance test for
    Delta_median_max_persistence / Delta_median_total_persistence. PRE and
    POST resampled independently, n_bootstrap times each, i-th pairing.
    Each resample gets its OWN recalculated tau (matching the real/
    surrogate convention -- tau is cheap, recomputed everywhere in this
    pipeline). block_length defaults to max(2*median_real_tau, 10) if not
    given, tied to the pipeline's own timescale (same spirit as other
    lines' block-length choices in this lab).
    """
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    if real_pre is None:
        real_pre = compute_ph_features(pre, m=m, n_window=n_window, k_max=k_max)
    if real_post is None:
        real_post = compute_ph_features(post, m=m, n_window=n_window, k_max=k_max)

    if block_length is None:
        taus = [d["tau"] for d in (real_pre, real_post) if d.get("status") == "ok"]
        block_length = max(2 * int(np.median(taus)), 10) if taus else 10
    L = int(block_length)

    rng = np.random.default_rng(seed)

    max_boot_pre, total_boot_pre = [], []
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(pre, L, rng)
        feat = compute_ph_features(resampled, m=m, n_window=n_window, k_max=k_max)
        max_boot_pre.append(feat["median_max_persistence"] if feat["status"] == "ok" else None)
        total_boot_pre.append(feat["median_total_persistence"] if feat["status"] == "ok" else None)

    max_boot_post, total_boot_post = [], []
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(post, L, rng)
        feat = compute_ph_features(resampled, m=m, n_window=n_window, k_max=k_max)
        max_boot_post.append(feat["median_max_persistence"] if feat["status"] == "ok" else None)
        total_boot_post.append(feat["median_total_persistence"] if feat["status"] == "ok" else None)

    def _pair_deltas(pre_vals, post_vals):
        deltas, n_undef = [], 0
        for vp, vq in zip(pre_vals, post_vals):
            if vp is None or vq is None:
                n_undef += 1
            else:
                deltas.append(vq - vp)
        return np.array(deltas, dtype=float), n_undef

    delta_max_boot, n_undef_max = _pair_deltas(max_boot_pre, max_boot_post)
    delta_total_boot, n_undef_total = _pair_deltas(total_boot_pre, total_boot_post)

    def _percentile_ci95(arr):
        lo, hi = np.percentile(arr, [2.5, 97.5])
        return (float(lo), float(hi))

    def _bootstrap_two_tailed_p(delta_arr, delta_real):
        if delta_real is None or len(delta_arr) == 0:
            return None
        return float(np.mean(np.abs(delta_arr) >= abs(delta_real)))

    delta_max_real = None
    delta_total_real = None
    if real_pre.get("status") == "ok" and real_post.get("status") == "ok":
        delta_max_real = real_post["median_max_persistence"] - real_pre["median_max_persistence"]
        delta_total_real = real_post["median_total_persistence"] - real_pre["median_total_persistence"]

    result = {
        "bootstrap_block_length": L,
        "bootstrap_n_bootstrap": int(n_bootstrap),
        "bootstrap_seed": int(seed),
    }
    for name, deltas, n_undef, delta_real in (
        ("max_persistence", delta_max_boot, n_undef_max, delta_max_real),
        ("total_persistence", delta_total_boot, n_undef_total, delta_total_real),
    ):
        n_valid = len(deltas)
        if n_valid == 0:
            ci95, p, mean_d, std_d = (None, None), None, None, None
        else:
            ci95 = _percentile_ci95(deltas)
            p = _bootstrap_two_tailed_p(deltas, delta_real)
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


def run_ph_analysis(pre_series, post_series, seed=SEED, n_surrogates=None,
                     n_iter=N_IAAFT_ITER, m=M_FIXED, n_window=N_WINDOW,
                     k_max=K_SUBWINDOWS_MAX, run_bootstrap=False, n_bootstrap=N_BOOTSTRAP):
    """Run the full persistent-homology transition test between a PRE and a
    POST segment, per METHODOLOGY_NOTE.md Gaps (a), (b), (e).

    `n_surrogates` defaults to N_SURROGATES=200 if None.

    Steps:
      1. compute_ph_features on real PRE and real POST INDEPENDENTLY --
         each gets its OWN recalculated tau (Gap (a): unlike RQA, tau is
         NOT shared/fixed from PRE here), m=3 FIXED for both, up to 10
         non-overlapping N_WINDOW=200 sub-windows spanning each segment.
         If EITHER segment cannot resolve tau or has insufficient embedded
         points (< N_WINDOW), the WHOLE domain comparison is rejected with
         that status -- no further computation, no silent workaround.
      2. Delta_median_max_persistence, Delta_median_total_persistence =
         POST - PRE (real).
      3. IAAFT is the PRIMARY significance test: N_SURROGATES independent
         PRE/POST surrogate pairs, each generated from its OWN real
         series, seed=12345. Each surrogate goes through the FULL
         pipeline (its own recalculated tau, m=3, sub-windowing, Rips,
         persistence) -- Gap (e). Two-tailed:
         p = fraction of surrogates with |Delta_surrogate| >= |Delta_real|.
      4. If `run_bootstrap=True`, ALSO runs the moving-block bootstrap
         (Kunsch 1989) fallback test (pre-authorized in METHODOLOGY_NOTE.md
         Gap (e) if synthetic validation shows IAAFT has insufficient
         power). Off by default.

    Returns a dict with everything a downstream agent needs to report a
    result without recomputing anything.
    """
    n_surr = N_SURROGATES if n_surrogates is None else int(n_surrogates)

    pre = np.asarray(pre_series, dtype=float)
    post = np.asarray(post_series, dtype=float)

    real_pre = compute_ph_features(pre, m=m, n_window=n_window, k_max=k_max)
    real_post = compute_ph_features(post, m=m, n_window=n_window, k_max=k_max)

    if real_pre["status"] != "ok" or real_post["status"] != "ok":
        status = "insufficient_samples" if (
            real_pre["status"] == "insufficient_samples" or real_post["status"] == "insufficient_samples"
        ) else "tau_not_resolved"
        return {
            "status": status,
            "real_pre": real_pre,
            "real_post": real_post,
            "config": {
                "m": m, "n_window": n_window, "k_subwindows_max": k_max,
                "n_surrogates": n_surr, "n_iaaft_iter": n_iter, "seed": seed,
            },
        }

    max_pre = real_pre["median_max_persistence"]
    max_post = real_post["median_max_persistence"]
    total_pre = real_pre["median_total_persistence"]
    total_post = real_post["median_total_persistence"]

    delta_max_real = _delta(max_post, max_pre)
    delta_total_real = _delta(total_post, total_pre)

    rng = np.random.default_rng(seed)
    surr_delta_max, surr_delta_total = [], []
    n_undef_max, n_undef_total = 0, 0
    n_tau_fail_pre_surr, n_tau_fail_post_surr = 0, 0
    n_insuff_pre_surr, n_insuff_post_surr = 0, 0

    for _ in range(n_surr):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        feat_pre_s = compute_ph_features(surr_pre, m=m, n_window=n_window, k_max=k_max)
        feat_post_s = compute_ph_features(surr_post, m=m, n_window=n_window, k_max=k_max)

        if feat_pre_s["status"] == "tau_not_resolved":
            n_tau_fail_pre_surr += 1
        elif feat_pre_s["status"] == "insufficient_samples":
            n_insuff_pre_surr += 1
        if feat_post_s["status"] == "tau_not_resolved":
            n_tau_fail_post_surr += 1
        elif feat_post_s["status"] == "insufficient_samples":
            n_insuff_post_surr += 1

        max_pre_s = feat_pre_s["median_max_persistence"] if feat_pre_s["status"] == "ok" else None
        max_post_s = feat_post_s["median_max_persistence"] if feat_post_s["status"] == "ok" else None
        max_delta = _delta(max_post_s, max_pre_s)
        if max_delta is None:
            n_undef_max += 1
        else:
            surr_delta_max.append(max_delta)

        total_pre_s = feat_pre_s["median_total_persistence"] if feat_pre_s["status"] == "ok" else None
        total_post_s = feat_post_s["median_total_persistence"] if feat_post_s["status"] == "ok" else None
        total_delta = _delta(total_post_s, total_pre_s)
        if total_delta is None:
            n_undef_total += 1
        else:
            surr_delta_total.append(total_delta)

    surr_delta_max = np.array(surr_delta_max, dtype=float)
    surr_delta_total = np.array(surr_delta_total, dtype=float)

    if delta_max_real is None or len(surr_delta_max) == 0:
        p_max = None
    else:
        p_max = float(np.mean(np.abs(surr_delta_max) >= abs(delta_max_real)))

    if delta_total_real is None or len(surr_delta_total) == 0:
        p_total = None
    else:
        p_total = float(np.mean(np.abs(surr_delta_total) >= abs(delta_total_real)))

    result = {
        "status": "ok",
        "real_pre": real_pre,
        "real_post": real_post,
        "median_max_persistence_pre": max_pre,
        "median_max_persistence_post": max_post,
        "median_total_persistence_pre": total_pre,
        "median_total_persistence_post": total_post,
        "delta_median_max_persistence": delta_max_real,
        "delta_median_total_persistence": delta_total_real,
        "p_max_persistence": p_max,
        "p_total_persistence": p_total,
        "surrogate_max_persistence_mean": float(np.mean(surr_delta_max)) if len(surr_delta_max) else None,
        "surrogate_max_persistence_std": float(np.std(surr_delta_max)) if len(surr_delta_max) else None,
        "surrogate_max_persistence_n_valid": int(len(surr_delta_max)),
        "surrogate_max_persistence_n_undefined": int(n_undef_max),
        "surrogate_total_persistence_mean": float(np.mean(surr_delta_total)) if len(surr_delta_total) else None,
        "surrogate_total_persistence_std": float(np.std(surr_delta_total)) if len(surr_delta_total) else None,
        "surrogate_total_persistence_n_valid": int(len(surr_delta_total)),
        "surrogate_total_persistence_n_undefined": int(n_undef_total),
        "diagnostics": {
            "pre_status": real_pre["status"],
            "post_status": real_post["status"],
            "pre_tau": real_pre["tau"],
            "post_tau": real_post["tau"],
            "pre_M": real_pre["M"],
            "post_M": real_post["M"],
            "pre_n_subwindows": real_pre["n_subwindows_used"],
            "post_n_subwindows": real_post["n_subwindows_used"],
            "n_surrogate_tau_failures_pre": n_tau_fail_pre_surr,
            "n_surrogate_tau_failures_post": n_tau_fail_post_surr,
            "n_surrogate_insufficient_pre": n_insuff_pre_surr,
            "n_surrogate_insufficient_post": n_insuff_post_surr,
        },
        "config": {
            "m": m, "n_window": n_window, "k_subwindows_max": k_max,
            "n_surrogates": n_surr, "n_iaaft_iter": n_iter, "seed": seed,
        },
    }

    if run_bootstrap:
        boot_result = run_block_bootstrap_test(
            pre, post, real_pre=real_pre, real_post=real_post,
            n_bootstrap=n_bootstrap, seed=seed, m=m, n_window=n_window, k_max=k_max,
        )
        result.update(boot_result)

    return result
