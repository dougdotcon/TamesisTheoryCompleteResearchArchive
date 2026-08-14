"""
Canonical DFA-1 (order-1 Detrended Fluctuation Analysis) pipeline for
DISC-TRI-RG-001, candidate `dfa-multiscale-entropy`.

Fixed BEFORE running on any real domain (physiology/PhysioNet Apnea-ECG a04,
paleoclimate/GISP2 Younger Dryas->Preboreal) -- see ../METHODOLOGY_NOTE.md
for the full rationale. This is a NEW, self-contained implementation
specific to this test line: it does not import from, and is not derived
from, `critical_slowing_down/analysis/csd_common.py` or
`wavelet_multiresolution/analysis/wtmm_common.py`, even though the IAAFT
surrogate step is conceptually the same published method (Schreiber &
Schmitz 1996) required by the methodology note for cross-line consistency.

Method (Peng et al. 1994 Phys. Rev. E 49:1685; 1995 Chaos 5:82-87):
  1. Integrate the (mean-centered) series x -> profile y(k) = sum_{i<=k}(x_i - mean(x)).
  2. Partition y into non-overlapping blocks of length n.
  3. Locally detrend each block with an order-1 (linear) least-squares fit.
  4. F(n) = sqrt(mean over blocks of the mean squared residual).
  5. alpha = slope of log F(n) vs log n (ordinary least squares).

Scale grid (dimensionless fraction of segment length N -- never an absolute
physical unit, since the domains have incommensurate sampling grids):
  n_min = 4, n_max = floor(0.25*N), N_SCALES = 20 log-spaced values of n,
  rounded to unique integers.

Three reported channels:
  - alpha  : regression over the full [n_min, n_max] range.
  - alpha1 : short-term, regression over [n_min, 16] (Peng/Iyengar convention).
  - alpha2 : long-term, regression over [16, n_max], only defined if n_max >= 16
             (otherwise explicitly None -- never silently substituted).

Any agent applying this pipeline to real data MUST import and call
`run_dfa_pipeline` (or the lower-level helpers) rather than reimplementing
any of this, so "same formula, no per-domain reformulation" is a literal
code-identity guarantee, matching the discipline already used for
`csd_common.py` and `wtmm_common.py` in this lab.
"""
import numpy as np

# ---- fixed constants (METHODOLOGY_NOTE.md gap (a) and (c) -- identical for
# every domain this pipeline is ever applied to; no per-domain tuning) ----
N_MIN = 4                  # Peng et al. minimum block length for a stable order-1 fit
N_MAX_FRAC = 0.25          # n_max = floor(0.25 * N) -- >=4 non-overlapping blocks at coarsest scale
N_SCALES = 20              # log-spaced n values between n_min and n_max
N_SPLIT = 16               # alpha1/alpha2 boundary (Peng et al.; Iyengar et al. 1996)
MIN_FIT_POINTS = 3         # minimum number of (log n, log F) points to trust a regression slope
N_SURROGATES = 200         # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50          # IAAFT iterations per surrogate
N_BOOTSTRAP = 1000         # moving-block bootstrap resamples (Kunsch 1989) per segment,
                            # per METHODOLOGY_NOTE.md "Adendo ao Gap (c)"
SEED = 12345


# --------------------------------------------------------------------------
# Core DFA-1
# --------------------------------------------------------------------------

def scale_grid(N, n_min=N_MIN, n_max_frac=N_MAX_FRAC, n_scales=N_SCALES):
    """Log-spaced integer scale grid n in [n_min, floor(n_max_frac*N)], unique values.

    Raises ValueError if the segment is too short to yield n_max >= n_min.
    """
    n_max = int(np.floor(n_max_frac * N))
    if n_max < n_min:
        raise ValueError(
            f"Segment too short for DFA: N={N} gives n_max={n_max} < n_min={n_min} "
            f"(need N >= {int(np.ceil(n_min / n_max_frac))})."
        )
    raw = np.exp(np.linspace(np.log(n_min), np.log(n_max), n_scales))
    scales = np.unique(np.round(raw).astype(int))
    scales = scales[(scales >= n_min) & (scales <= n_max)]
    return scales, n_max


def dfa_fluctuation(x, scales):
    """Compute F(n) for each n in `scales` via order-1 DFA (Peng et al. 1994/1995).

    x: 1-D real array, raw (non-integrated) series in chronological order.
    scales: array-like of block lengths n (non-overlapping partition of the
        integrated profile).

    Returns (scales_used, F_n): both float arrays, filtered to the n values
    for which at least one full block fits (n <= N).
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    y = np.cumsum(x - np.mean(x))  # integrated profile

    scales_used = []
    F_n = []
    for n in scales:
        n = int(n)
        n_blocks = N // n
        if n_blocks < 1:
            continue
        trimmed = y[: n_blocks * n].reshape(n_blocks, n)
        t = np.arange(n, dtype=float)
        t_mean = t.mean()
        t_centered = t - t_mean
        t_var = np.sum(t_centered ** 2)
        y_mean = trimmed.mean(axis=1)
        # vectorized per-block ordinary least-squares linear fit
        slope = (trimmed - y_mean[:, None]).dot(t_centered) / t_var
        intercept = y_mean - slope * t_mean
        fit = slope[:, None] * t[None, :] + intercept[:, None]
        resid = trimmed - fit
        F = np.sqrt(np.mean(resid ** 2))
        scales_used.append(n)
        F_n.append(F)

    return np.array(scales_used, dtype=int), np.array(F_n, dtype=float)


def fit_alpha(scales, F_n, n_lo, n_hi, min_points=MIN_FIT_POINTS):
    """OLS slope of log F(n) vs log n restricted to n in [n_lo, n_hi].

    Returns a dict {alpha, intercept, n_points, scales} or None if fewer
    than `min_points` scales fall in range (never silently substituted).
    """
    mask = (scales >= n_lo) & (scales <= n_hi)
    if mask.sum() < min_points:
        return None
    logn = np.log(scales[mask].astype(float))
    logF = np.log(F_n[mask])
    slope, intercept = np.polyfit(logn, logF, 1)
    return {
        "alpha": float(slope),
        "intercept": float(intercept),
        "n_points": int(mask.sum()),
        "scales": scales[mask].tolist(),
    }


def compute_alphas(x, n_min=N_MIN, n_max_frac=N_MAX_FRAC, n_scales=N_SCALES,
                    n_split=N_SPLIT, min_points=MIN_FIT_POINTS):
    """Run the full DFA-1 scale grid on one segment and fit the three channels.

    Returns a dict with n_samples, n_min, n_max, scales_used, F_n, and the
    three channel fits (alpha, alpha1, alpha2 -- alpha2 is None if
    n_max < n_split, alpha1/alpha2 are None if too few scale points fall in
    their respective sub-range).
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    scales, n_max = scale_grid(N, n_min=n_min, n_max_frac=n_max_frac, n_scales=n_scales)
    scales_used, F_n = dfa_fluctuation(x, scales)

    alpha_full = fit_alpha(scales_used, F_n, n_min, n_max, min_points=min_points)
    alpha1 = fit_alpha(scales_used, F_n, n_min, n_split, min_points=min_points)
    if n_max >= n_split:
        alpha2 = fit_alpha(scales_used, F_n, n_split, n_max, min_points=min_points)
    else:
        alpha2 = None  # explicitly undefined per METHODOLOGY_NOTE.md gap (a)

    return {
        "n_samples": int(N),
        "n_min": int(n_min),
        "n_max": int(n_max),
        "n_split": int(n_split),
        "scales_used": scales_used.tolist(),
        "F_n": F_n.tolist(),
        "alpha": alpha_full,
        "alpha1": alpha1,
        "alpha2": alpha2,
        "max_min_ratio": max_min_ratio(x),
    }


# --------------------------------------------------------------------------
# Marginal-degeneracy diagnostic (governance lesson from
# wavelet-multiresolution-scaling, METHODOLOGY_EXTENSIONS.md)
# --------------------------------------------------------------------------

MAX_MIN_RATIO_ALERT_THRESHOLD = 190.0  # diagnostic threshold from the binomial-cascade IAAFT failure


def max_min_ratio(x):
    """max(x)/min(x) of the raw segment values.

    This diagnostic is only meaningful for a series that is a genuinely
    positive physical quantity bounded away from zero (RR intervals in ms,
    ice-core proxy values used on a positive physical scale -- the expected
    real-data input for this pipeline). Taking abs() of a signed,
    zero-crossing series (e.g. a zero-mean fGn/fBm draw) is NOT a sound
    substitute: such a series has values arbitrarily close to zero with
    positive probability, so max(|x|)/min(|x|) diverges as a near-certain
    artifact of the sample, not a genuine heavy-tail/degenerate-marginal
    signal -- that would make the alert fire on literally every zero-mean
    control and be useless as a diagnostic. So for a series with any
    non-positive value, this function returns ratio=None with an explicit
    'not_applicable' flag rather than a misleading number.
    """
    x = np.asarray(x, dtype=float)
    if np.any(x <= 0):
        return {
            "ratio": None, "basis": "signed_or_zero_crossing", "max": None, "min": None,
            "flag": "not_applicable_series_not_strictly_positive",
        }
    mx, mn = float(np.max(x)), float(np.min(x))
    ratio = mx / mn if mn > 0 else float("inf")
    flag = "degenerate_marginal" if ratio >= MAX_MIN_RATIO_ALERT_THRESHOLD else "ok"
    return {"ratio": ratio, "basis": "raw_positive", "max": mx, "min": mn, "flag": flag}


# --------------------------------------------------------------------------
# IAAFT surrogates (Schreiber & Schmitz 1996)
# --------------------------------------------------------------------------

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate.

    Preserves the linear power spectrum (amplitude spectrum of the FFT) and
    the exact empirical amplitude distribution of x; destroys any
    higher-order nonlinear phase structure beyond what a linear Gaussian
    process with the same spectrum/marginal would produce.
    """
    if rng is None:
        rng = np.random.default_rng()
    x = np.asarray(x, dtype=float)
    n = len(x)
    sorted_x = np.sort(x)
    amp_spectrum = np.abs(np.fft.rfft(x))
    surrogate = rng.permutation(x).astype(float)
    for _ in range(n_iter):
        fft_surr = np.fft.rfft(surrogate)
        phases = np.angle(fft_surr)
        new_fft = amp_spectrum * np.exp(1j * phases)
        surrogate = np.fft.irfft(new_fft, n=n)
        ranks = np.argsort(np.argsort(surrogate))
        surrogate = sorted_x[ranks]
    return surrogate


# --------------------------------------------------------------------------
# Moving-block bootstrap (Kunsch 1989) -- complementary significance test,
# added to METHODOLOGY_NOTE.md "Adendo ao Gap (c)" AFTER the synthetic
# validation showed the IAAFT bicaudal test (above) has low power to detect
# genuine changes in `alpha`: IAAFT surrogates preserve the exact linear
# amplitude spectrum of each segment, and `alpha` is essentially a spectral
# quantity for a self-similar Gaussian process, so the IAAFT null
# distribution of Delta alpha ends up centered almost exactly on the real
# Delta alpha (positive control PRE=fGn H=0.5 / POST=fGn H=0.9 -> IAAFT
# p_alpha=0.255, not significant, despite an unambiguous-by-construction
# change). This block bootstrap answers a different, broader question --
# "does Delta alpha exceed finite-sample estimation variability?" -- without
# depending on preserving the spectrum. IAAFT is still computed and reported
# above as a complementary/secondary check (it answers a real, narrower
# question about nonlinear structure beyond the linear spectrum); this test
# is the primary significance test for Delta alpha per the addendum.
# --------------------------------------------------------------------------

def moving_block_bootstrap_resample(x, L, rng):
    """One moving-block-bootstrap resample of `x` (Kunsch 1989).

    Blocks of length `L`, start index drawn uniformly at random (with
    replacement, i.e. blocks may overlap and repeat), concatenated until at
    least as long as the original series, then trimmed to exactly len(x) so
    the resample has the same length as the input.
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    L = int(L)
    if L < 1:
        L = 1
    if L > N:
        L = N  # degenerate safety fallback; not expected in practice since
                # L = n_max = floor(0.25*N) < N by construction
    n_blocks_needed = int(np.ceil(N / L))
    starts = rng.integers(0, N - L + 1, size=n_blocks_needed)
    pieces = [x[s:s + L] for s in starts]
    resampled = np.concatenate(pieces)[:N]
    return resampled


def bootstrap_alpha_distribution(x, L, n_bootstrap, rng,
                                  n_min=N_MIN, n_max_frac=N_MAX_FRAC,
                                  n_scales=N_SCALES, n_split=N_SPLIT,
                                  min_points=MIN_FIT_POINTS):
    """Generate `n_bootstrap` moving-block resamples of segment `x` (block
    length `L`) and compute DFA-1 alpha/alpha1/alpha2 (via the SAME
    `compute_alphas`, unmodified) on each.

    Returns {"alpha": [...], "alpha1": [...], "alpha2": [...]}, each a list
    of length n_bootstrap containing the channel's alpha value or None where
    that channel is undefined for that particular resample (never silently
    substituted -- same discipline as the IAAFT loop in run_dfa_pipeline).
    """
    out = {ch: [] for ch in _CHANNELS}
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(x, L, rng)
        alphas = compute_alphas(resampled, n_min=n_min, n_max_frac=n_max_frac,
                                 n_scales=n_scales, n_split=n_split,
                                 min_points=min_points)
        for ch in _CHANNELS:
            out[ch].append(_channel_value(alphas, ch))
    return out


def _percentile_ci95(arr):
    lo, hi = np.percentile(arr, [2.5, 97.5])
    return (float(lo), float(hi))


def _bootstrap_two_tailed_p(delta_arr):
    """p = 2*min(frac(Delta<=0), frac(Delta>=0)), standard two-tailed
    percentile bootstrap p-value construction (METHODOLOGY_NOTE.md addendum)."""
    frac_le0 = float(np.mean(delta_arr <= 0))
    frac_ge0 = float(np.mean(delta_arr >= 0))
    return float(2 * min(frac_le0, frac_ge0))


def run_block_bootstrap_test(pre_segment, post_segment,
                              real_pre=None, real_post=None,
                              n_bootstrap=N_BOOTSTRAP, seed=SEED,
                              n_min=N_MIN, n_max_frac=N_MAX_FRAC,
                              n_scales=N_SCALES, n_split=N_SPLIT,
                              min_points=MIN_FIT_POINTS):
    """Moving-block bootstrap (Kunsch 1989) significance test for Delta
    alpha / Delta alpha1 / Delta alpha2, per METHODOLOGY_NOTE.md "Adendo ao
    Gap (c)".

    Block length `L` for each segment is that segment's OWN `n_max` (the
    coarsest scale already used by that segment's DFA scale grid, as
    returned by `compute_alphas` -- fixed a priori, tied to the analysis
    itself, not an arbitrary bootstrap choice). PRE and POST are resampled
    independently, `n_bootstrap` times each, with the SAME fixed `seed`
    convention (default 12345) used elsewhere in this module. The i-th PRE
    resample is paired with the i-th POST resample to form
    `Delta alpha_boot_i = alpha_boot_POST_i - alpha_boot_PRE_i`.

    If `real_pre`/`real_post` (the `compute_alphas` output for the real
    segments) are already available, pass them in to avoid recomputing;
    otherwise they are computed here.

    Returns a dict with, per channel (alpha, alpha1, alpha2):
      - delta_{channel}_boot_ci95: (low, high) 95% percentile CI of
        Delta alpha_boot, or (None, None) if no bootstrap pair was valid.
      - p_bootstrap_{channel}: two-tailed percentile p-value, or None.
      - delta_{channel}_boot_mean/std/n_valid/n_undefined: null-distribution
        summary stats and channel-undefined bookkeeping.
    plus block_length_pre/post, n_bootstrap, seed for provenance.
    """
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    if real_pre is None:
        real_pre = compute_alphas(pre, n_min=n_min, n_max_frac=n_max_frac,
                                   n_scales=n_scales, n_split=n_split,
                                   min_points=min_points)
    if real_post is None:
        real_post = compute_alphas(post, n_min=n_min, n_max_frac=n_max_frac,
                                    n_scales=n_scales, n_split=n_split,
                                    min_points=min_points)

    L_pre = real_pre["n_max"]
    L_post = real_post["n_max"]

    rng = np.random.default_rng(seed)
    boot_pre = bootstrap_alpha_distribution(pre, L_pre, n_bootstrap, rng,
                                             n_min=n_min, n_max_frac=n_max_frac,
                                             n_scales=n_scales, n_split=n_split,
                                             min_points=min_points)
    boot_post = bootstrap_alpha_distribution(post, L_post, n_bootstrap, rng,
                                              n_min=n_min, n_max_frac=n_max_frac,
                                              n_scales=n_scales, n_split=n_split,
                                              min_points=min_points)

    result = {
        "bootstrap_block_length_pre": int(L_pre),
        "bootstrap_block_length_post": int(L_post),
        "bootstrap_n_bootstrap": int(n_bootstrap),
        "bootstrap_seed": int(seed),
    }

    for ch in _CHANNELS:
        pre_vals = boot_pre[ch]
        post_vals = boot_post[ch]
        deltas = []
        n_undef = 0
        for v_pre, v_post in zip(pre_vals, post_vals):
            if v_pre is None or v_post is None:
                n_undef += 1
            else:
                deltas.append(v_post - v_pre)
        deltas = np.array(deltas, dtype=float)
        n_valid = len(deltas)
        if n_valid == 0:
            ci95 = (None, None)
            p = None
            mean_d = None
            std_d = None
        else:
            ci95 = _percentile_ci95(deltas)
            p = _bootstrap_two_tailed_p(deltas)
            mean_d = float(np.mean(deltas))
            std_d = float(np.std(deltas))
        result[f"delta_{ch}_boot_ci95"] = ci95
        result[f"p_bootstrap_{ch}"] = p
        result[f"delta_{ch}_boot_mean"] = mean_d
        result[f"delta_{ch}_boot_std"] = std_d
        result[f"delta_{ch}_boot_n_valid"] = n_valid
        result[f"delta_{ch}_boot_n_undefined"] = n_undef

    return result


# --------------------------------------------------------------------------
# Full transition-test pipeline
# --------------------------------------------------------------------------

_CHANNELS = ("alpha", "alpha1", "alpha2")


def _channel_value(alphas_dict, channel):
    """Extract the alpha value for a channel, or None if that channel is undefined."""
    entry = alphas_dict.get(channel)
    return None if entry is None else entry["alpha"]


def run_dfa_pipeline(pre_segment, post_segment,
                      n_surrogates=N_SURROGATES, n_iter=N_IAAFT_ITER,
                      n_bootstrap=N_BOOTSTRAP, seed=SEED,
                      n_min=N_MIN, n_max_frac=N_MAX_FRAC, n_scales=N_SCALES,
                      n_split=N_SPLIT):
    """Run the full DFA-1 transition test between a PRE and a POST segment.

    Computes alpha/alpha1/alpha2 on the real PRE and POST segments, the
    corresponding Delta alphas, a two-tailed IAAFT surrogate null
    distribution (N_SURROGATES independent PRE/POST surrogate pairs, each
    surrogate generated from its OWN real segment) for each channel, per
    METHODOLOGY_NOTE.md gaps (a) and (c), AND a moving-block bootstrap
    (Kunsch 1989) significance test per the "Adendo ao Gap (c)" section
    (see `run_block_bootstrap_test` docstring) -- the PRIMARY significance
    test for Delta alpha, since synthetic validation showed the IAAFT test
    above has low power to detect genuine changes in `alpha` (it preserves
    each segment's exact linear spectrum, and `alpha` is essentially a
    spectral quantity). IAAFT is still computed and reported as a
    complementary/secondary check.

    Returns a single dict with everything a downstream agent needs to report
    a result without recomputing anything:
      - real_pre, real_post: full compute_alphas() output for each segment
        (includes alpha/alpha1/alpha2 fits, scale grids, F(n), max_min_ratio)
      - delta_alpha, delta_alpha1, delta_alpha2: real POST - PRE (None if
        either side's channel is undefined)
      - p_alpha, p_alpha1, p_alpha2: two-tailed IAAFT surrogate p-values
        (fraction of surrogates with |Delta alpha_surrogate| >=
        |Delta alpha_real|), None if the real delta itself is undefined
        (complementary/secondary check -- see module and function docstrings)
      - surrogate_*_mean/std/n_valid: IAAFT null-distribution summary per channel
      - surrogate_max_min_ratio_pre/post: summary stats of the max/min ratio
        across all generated IAAFT surrogates, for the marginal-degeneracy check
      - delta_alpha_boot_ci95, delta_alpha1_boot_ci95, delta_alpha2_boot_ci95:
        95% percentile CI of the moving-block-bootstrap Delta alpha null
        distribution (PRIMARY significance test; excludes 0 <=> significant)
      - p_bootstrap_alpha, p_bootstrap_alpha1, p_bootstrap_alpha2: two-tailed
        percentile bootstrap p-values (PRIMARY significance test)
      - delta_alpha_boot_mean/std/n_valid/n_undefined (and alpha1/alpha2):
        bootstrap null-distribution summary per channel
      - bootstrap_block_length_pre/post, bootstrap_n_bootstrap, bootstrap_seed:
        provenance for the bootstrap test
      - config: the exact fixed parameters used (for provenance)
    """
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    real_pre = compute_alphas(pre, n_min=n_min, n_max_frac=n_max_frac,
                               n_scales=n_scales, n_split=n_split)
    real_post = compute_alphas(post, n_min=n_min, n_max_frac=n_max_frac,
                                n_scales=n_scales, n_split=n_split)

    real_delta = {}
    for ch in _CHANNELS:
        v_pre = _channel_value(real_pre, ch)
        v_post = _channel_value(real_post, ch)
        real_delta[ch] = None if (v_pre is None or v_post is None) else (v_post - v_pre)

    rng = np.random.default_rng(seed)
    surr_delta = {ch: [] for ch in _CHANNELS}
    surr_ratio_pre = []
    surr_ratio_post = []
    n_surrogate_channel_undefined = {ch: 0 for ch in _CHANNELS}

    for _ in range(n_surrogates):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        alphas_pre_s = compute_alphas(surr_pre, n_min=n_min, n_max_frac=n_max_frac,
                                       n_scales=n_scales, n_split=n_split)
        alphas_post_s = compute_alphas(surr_post, n_min=n_min, n_max_frac=n_max_frac,
                                        n_scales=n_scales, n_split=n_split)

        r_pre = alphas_pre_s["max_min_ratio"]["ratio"]
        r_post = alphas_post_s["max_min_ratio"]["ratio"]
        if r_pre is not None:
            surr_ratio_pre.append(r_pre)
        if r_post is not None:
            surr_ratio_post.append(r_post)

        for ch in _CHANNELS:
            v_pre = _channel_value(alphas_pre_s, ch)
            v_post = _channel_value(alphas_post_s, ch)
            if v_pre is None or v_post is None:
                n_surrogate_channel_undefined[ch] += 1
            else:
                surr_delta[ch].append(v_post - v_pre)

    result = {
        "real_pre": real_pre,
        "real_post": real_post,
        "delta_alpha": real_delta["alpha"],
        "delta_alpha1": real_delta["alpha1"],
        "delta_alpha2": real_delta["alpha2"],
        "config": {
            "n_min": n_min,
            "n_max_frac": n_max_frac,
            "n_scales": n_scales,
            "n_split": n_split,
            "n_surrogates": n_surrogates,
            "n_iaaft_iter": n_iter,
            "n_bootstrap": n_bootstrap,
            "seed": seed,
            "max_min_ratio_alert_threshold": MAX_MIN_RATIO_ALERT_THRESHOLD,
        },
        "surrogate_max_min_ratio_pre": {
            "mean": float(np.mean(surr_ratio_pre)) if surr_ratio_pre else None,
            "min": float(np.min(surr_ratio_pre)) if surr_ratio_pre else None,
            "max": float(np.max(surr_ratio_pre)) if surr_ratio_pre else None,
        },
        "surrogate_max_min_ratio_post": {
            "mean": float(np.mean(surr_ratio_post)) if surr_ratio_post else None,
            "min": float(np.min(surr_ratio_post)) if surr_ratio_post else None,
            "max": float(np.max(surr_ratio_post)) if surr_ratio_post else None,
        },
    }

    for ch, p_key in (("alpha", "p_alpha"), ("alpha1", "p_alpha1"), ("alpha2", "p_alpha2")):
        real_d = real_delta[ch]
        valid = np.array(surr_delta[ch], dtype=float)
        n_valid = len(valid)
        n_undef = n_surrogate_channel_undefined[ch]
        if real_d is None or n_valid == 0:
            p = None
        else:
            p = float(np.mean(np.abs(valid) >= abs(real_d)))
        result[p_key] = p
        result[f"surrogate_{ch}_n_valid"] = int(n_valid)
        result[f"surrogate_{ch}_n_undefined"] = int(n_undef)
        result[f"surrogate_{ch}_mean"] = float(np.mean(valid)) if n_valid else None
        result[f"surrogate_{ch}_std"] = float(np.std(valid)) if n_valid else None

    # PRIMARY significance test (METHODOLOGY_NOTE.md "Adendo ao Gap (c)"):
    # moving-block bootstrap, independent of the IAAFT rng stream above but
    # using the SAME fixed seed convention. Reuses real_pre/real_post (and
    # their n_max) already computed, so nothing is recomputed twice.
    boot_result = run_block_bootstrap_test(
        pre, post, real_pre=real_pre, real_post=real_post,
        n_bootstrap=n_bootstrap, seed=seed,
        n_min=n_min, n_max_frac=n_max_frac, n_scales=n_scales, n_split=n_split,
    )
    result.update(boot_result)

    return result
