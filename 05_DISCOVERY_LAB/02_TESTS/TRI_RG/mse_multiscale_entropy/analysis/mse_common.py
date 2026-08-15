"""
Canonical Multiscale Sample Entropy (MSE) pipeline for DISC-TRI-RG-001,
candidate `mse-multiscale-entropy` (Costa, Goldberger & Peng, 2002 PRL
89:068102; 2005 Phys. Rev. E 71:021906).

Fixed BEFORE running on any real domain (geomagnetic Dst/SYM-H March 1989
storm, FEMTO/PRONOSTIA bearing degradation) -- see ../METHODOLOGY_NOTE.md
for the full rationale. This is a NEW, self-contained implementation
specific to this test line: it does not import from, and is not derived
from, `critical_slowing_down/analysis/csd_common.py`,
`dfa_multiscale_entropy/analysis/dfa_common.py`, or
`wavelet_multiresolution/analysis/wtmm_common.py`, even though the IAAFT
surrogate step is conceptually the same published method (Schreiber &
Schmitz 1996) required by the methodology note for cross-line consistency.

Method:
  1. Coarse-grain the (non-overlapping-block) series at scale tau:
         x_j^(tau) = (1/tau) * sum_{i=(j-1)*tau+1}^{j*tau} x_i
     -- Costa et al.'s original definition, gap (a) of METHODOLOGY_NOTE.md.
  2. At each scale, compute SampEn(m=2, r) of the coarse-grained series
     (Richman & Moorman 2000), with `r = 0.15 * SD(original series at
     tau=1)` fixed across ALL scales (Costa et al.'s original convention,
     NOT the later "r rescaled per scale" variant).
  3. CI (Complexity Index) = sum of SampEn(tau) over the scale grid --
     primary channel. beta = OLS slope of SampEn(tau) vs log(tau) --
     secondary/companion channel.
  4. IAAFT surrogates (Schreiber & Schmitz 1996) are the PRIMARY
     significance test here (gap (c) of METHODOLOGY_NOTE.md) -- unlike
     DFA/CSD/SOC in this lab, where IAAFT/Poisson was secondary.

Scale grid (domain-agnostic, gap (a) of METHODOLOGY_NOTE.md):
  tau_min = 1, tau_max = floor(N / 200), N_SCALES = min(20, tau_max)
  log-spaced integer values of tau, rounded to unique integers.
  (MIN_POINTS_AT_COARSEST = 200, Yentes et al. 2013, Ann. Biomed. Eng.
  41:349 -- floor for a reliable SampEn m=2 estimate at the coarsest scale.)

Any agent applying this pipeline to real data MUST import and call
`run_mse_pipeline` (or the lower-level helpers) rather than reimplementing
any of this, so "same formula, no per-domain reformulation" is a literal
code-identity guarantee, matching the discipline already used for
`dfa_common.py` and `wtmm_common.py` in this lab.
"""
import numpy as np
from scipy.spatial import cKDTree

# ---- fixed constants (METHODOLOGY_NOTE.md gaps (a), (b), (c) -- identical
# for every domain this pipeline is ever applied to; no per-domain tuning) --
MIN_POINTS_AT_COARSEST = 200   # Yentes et al. 2013 floor for reliable SampEn(m=2)
TAU_MIN = 1                    # Costa et al. universal starting scale
N_SCALES_CAP = 20              # cap on log-spaced tau values
SAMPEN_M = 2                   # embedding dimension (Richman & Moorman 2000)
SAMPEN_R_FRACTION = 0.15       # r = 0.15 * SD(original series), fixed across scales
MIN_FIT_POINTS = 3             # minimum (log tau, SampEn) points to trust the beta slope
N_SURROGATES = 200             # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50              # IAAFT iterations per surrogate
SEED = 12345


# --------------------------------------------------------------------------
# Gap (a): coarse-graining and scale grid
# --------------------------------------------------------------------------

def scale_grid(N, tau_min=TAU_MIN, min_points_at_coarsest=MIN_POINTS_AT_COARSEST,
                n_scales_cap=N_SCALES_CAP):
    """Log-spaced integer scale grid tau in [tau_min, tau_max], unique values.

    tau_max = floor(N / min_points_at_coarsest); N_SCALES = min(n_scales_cap,
    tau_max). Raises ValueError if the segment is too short to yield
    tau_max >= tau_min (i.e. N < min_points_at_coarsest).
    """
    tau_max = int(np.floor(N / min_points_at_coarsest))
    if tau_max < tau_min:
        raise ValueError(
            f"Segment too short for MSE: N={N} gives tau_max={tau_max} < "
            f"tau_min={tau_min} (need N >= {min_points_at_coarsest})."
        )
    n_scales = min(n_scales_cap, tau_max)
    if n_scales <= 1:
        raw = np.array([tau_min], dtype=float)
    else:
        raw = np.exp(np.linspace(np.log(tau_min), np.log(tau_max), n_scales))
    scales = np.unique(np.round(raw).astype(int))
    scales = scales[(scales >= tau_min) & (scales <= tau_max)]
    return scales, tau_max


def coarse_grain(x, tau):
    """Non-overlapping block-average coarse-graining at scale `tau`
    (Costa, Goldberger & Peng 2002/2005):
        x_j^(tau) = (1/tau) * sum_{i=(j-1)*tau+1}^{j*tau} x_i

    Returns a float array of length floor(N/tau). Trailing points that do
    not fill a complete block of length tau are dropped (standard
    convention -- Costa et al. do not pad partial blocks).
    """
    x = np.asarray(x, dtype=float)
    tau = int(tau)
    if tau == 1:
        return x.copy()
    n_blocks = len(x) // tau
    if n_blocks < 1:
        return np.array([], dtype=float)
    trimmed = x[: n_blocks * tau].reshape(n_blocks, tau)
    return trimmed.mean(axis=1)


# --------------------------------------------------------------------------
# Gap (b): SampEn (Richman & Moorman 2000)
# --------------------------------------------------------------------------

def sample_entropy(x, m=SAMPEN_M, r=None):
    """Sample entropy SampEn(m, r) of series `x` (Richman & Moorman 2000),
    Chebyshev (max-norm) distance convention.

    Embedding vectors u_m(i) = x[i:i+m] are formed for i = 0, ..., N-m-1
    (the same index range is used for the m-dimensional and (m+1)-
    dimensional vectors, per Richman & Moorman's original definition, so
    the two match counts are directly comparable):
        B = #{(i,j): i != j, d_inf(u_m(i), u_m(j)) <= r}
        A = #{(i,j): i != j, d_inf(u_{m+1}(i), u_{m+1}(j)) <= r}
        SampEn = -ln(A / B)

    Match counts are obtained via a KD-tree with Chebyshev metric
    (scipy.spatial.cKDTree, p=inf) rather than an O(N^2) Python double
    loop, so this scales to real-data segment lengths, not just the
    moderate synthetic validation series used here.

    Returns a float, or None (explicit, never silently substituted) if
    either B or A is zero, i.e. SampEn is undefined at this (m, r, N) --
    either no template pair exists at all (B=0) or every m-length match
    happens to extend to an (m+1)-length match with a probability
    indistinguishable from certainty in this finite sample (A=0, which
    would make the ratio 0 and SampEn formally +infinity -- not a usable
    finite estimate).
    """
    if r is None:
        raise ValueError("sample_entropy requires an explicit tolerance r.")
    x = np.asarray(x, dtype=float)
    N = len(x)
    n_vec = N - m  # number of (m)- and (m+1)-length template vectors
    if n_vec < 2 or r <= 0:
        return None

    Xm = np.lib.stride_tricks.sliding_window_view(x, m)[:n_vec]
    Xm1 = np.lib.stride_tricks.sliding_window_view(x, m + 1)[:n_vec]

    tree_m = cKDTree(Xm)
    tree_m1 = cKDTree(Xm1)

    # count_neighbors(self, r, p=inf) sums, over every point in the tree,
    # the number of points (including itself) within Chebyshev distance r
    # -- i.e. it counts ORDERED pairs (i, j) with d_inf(i, j) <= r,
    # including the n_vec self-pairs (i == i, distance 0). Subtract those
    # to get the i != j count required by the SampEn definition.
    B_with_self = tree_m.count_neighbors(tree_m, r, p=np.inf)
    A_with_self = tree_m1.count_neighbors(tree_m1, r, p=np.inf)
    B = B_with_self - n_vec
    A = A_with_self - n_vec

    if B <= 0 or A <= 0:
        return None
    return float(-np.log(A / B))


def compute_r(x, fraction=SAMPEN_R_FRACTION):
    """SampEn tolerance r = fraction * SD(x), computed on the ORIGINAL
    (tau=1) series only -- kept fixed across all coarse-graining scales
    (Costa et al.'s original convention; gap (b) of METHODOLOGY_NOTE.md).
    """
    x = np.asarray(x, dtype=float)
    return float(fraction * np.std(x, ddof=0))


# --------------------------------------------------------------------------
# Full MSE curve + CI / beta channels for one segment
# --------------------------------------------------------------------------

def compute_mse(x, m=SAMPEN_M, r_fraction=SAMPEN_R_FRACTION,
                 tau_min=TAU_MIN, min_points_at_coarsest=MIN_POINTS_AT_COARSEST,
                 n_scales_cap=N_SCALES_CAP, min_fit_points=MIN_FIT_POINTS):
    """Run the full MSE scale grid on one segment: coarse-grain at every
    tau in the grid, compute SampEn(tau) at each with r fixed from the
    ORIGINAL series, then derive the CI (primary) and beta (secondary)
    channels.

    Returns a dict:
      n_samples, tau_min, tau_max, scales_used (list[int]),
      sd_original, r (the fixed tolerance),
      sampen_values (list[float|None], one per scale in scales_used,
          None where SampEn was undefined at that scale -- never
          substituted),
      n_scales_valid, n_scales_undefined,
      CI: sum of sampen_values over the WHOLE grid, or None if ANY scale
          in the grid has an undefined SampEn (a sum with an undefined
          term is itself undefined -- never silently reduced to a partial
          sum under the same name),
      CI_partial_sum_valid_only: sum over just the valid (non-None)
          scales, reported ONLY as a diagnostic aid when CI is None --
          NOT a substitute for CI and must not be reported as "the CI",
      beta: OLS-fit dict {beta, intercept, n_points, scales} over the
          valid (tau, SampEn) pairs, or None if fewer than
          `min_fit_points` scales have a defined SampEn.
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    scales, tau_max = scale_grid(N, tau_min=tau_min,
                                  min_points_at_coarsest=min_points_at_coarsest,
                                  n_scales_cap=n_scales_cap)
    r = compute_r(x, fraction=r_fraction)
    sd_original = float(np.std(x, ddof=0))

    sampen_values = []
    for tau in scales:
        coarse = coarse_grain(x, tau)
        sampen_values.append(sample_entropy(coarse, m=m, r=r))

    valid_mask = np.array([v is not None for v in sampen_values])
    n_valid = int(valid_mask.sum())
    n_undefined = int(len(sampen_values) - n_valid)

    if n_undefined == 0:
        CI = float(sum(sampen_values))
    else:
        CI = None
    CI_partial = float(sum(v for v in sampen_values if v is not None)) if n_valid > 0 else None

    if n_valid >= min_fit_points:
        valid_scales = scales[valid_mask]
        valid_vals = np.array([v for v in sampen_values if v is not None], dtype=float)
        log_tau = np.log(valid_scales.astype(float))
        slope, intercept = np.polyfit(log_tau, valid_vals, 1)
        beta = {
            "beta": float(slope),
            "intercept": float(intercept),
            "n_points": int(n_valid),
            "scales": valid_scales.tolist(),
        }
    else:
        beta = None

    return {
        "n_samples": int(N),
        "tau_min": int(tau_min),
        "tau_max": int(tau_max),
        "scales_used": scales.tolist(),
        "sd_original": sd_original,
        "r": r,
        "sampen_values": [None if v is None else float(v) for v in sampen_values],
        "n_scales_valid": n_valid,
        "n_scales_undefined": n_undefined,
        "CI": CI,
        "CI_partial_sum_valid_only": CI_partial,
        "beta": beta,
    }


# --------------------------------------------------------------------------
# Gap (c): IAAFT surrogates (Schreiber & Schmitz 1996)
# --------------------------------------------------------------------------

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate
    (Schreiber & Schmitz 1996).

    Preserves the linear power spectrum (FFT amplitude spectrum) and the
    exact empirical amplitude distribution (histogram) of `x`; destroys
    any nonlinear phase/temporal structure beyond what a linear Gaussian
    process with the same spectrum and marginal would produce. Independent
    reimplementation for this test line -- see module docstring.

    Algorithm: start from a random permutation of x's values, then
    alternately (1) impose the target amplitude spectrum in the frequency
    domain while keeping the current phases, and (2) impose the exact
    target rank order (amplitude distribution) in the time domain, for
    `n_iter` rounds.
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


# --------------------------------------------------------------------------
# Full PRE/POST transition test pipeline
# --------------------------------------------------------------------------

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def run_mse_pipeline(pre_segment, post_segment,
                      n_surrogates=N_SURROGATES, n_iter=N_IAAFT_ITER, seed=SEED,
                      m=SAMPEN_M, r_fraction=SAMPEN_R_FRACTION,
                      tau_min=TAU_MIN, min_points_at_coarsest=MIN_POINTS_AT_COARSEST,
                      n_scales_cap=N_SCALES_CAP, min_fit_points=MIN_FIT_POINTS):
    """Run the full MSE transition test between a PRE and a POST segment,
    per METHODOLOGY_NOTE.md gaps (a)-(c).

    Each segment gets its OWN scale grid (tau_max depends on that
    segment's own N) and its OWN fixed r (0.15 * SD of that segment's
    own tau=1 series) -- consistent with Costa et al.'s per-series
    convention and with how this lab already treats PRE/POST asymmetric
    sample sizes in dfa_common.py/wtmm_common.py.

    IAAFT is the PRIMARY significance test here (unlike DFA/CSD/SOC in
    this lab): N_SURROGATES independent PRE/POST surrogate pairs, each
    surrogate generated from its OWN real segment (never cross-segment),
    same fixed seed=12345 convention used elsewhere in this lab. Two-
    tailed test: p = fraction of surrogates with
    |Delta_CI_surrogate| >= |Delta_CI_real| (and equivalently for beta).

    Returns a dict:
      real_pre, real_post: full compute_mse() output for each segment
      delta_CI, delta_beta: real POST - PRE (None if either side undefined)
      p_CI, p_beta: two-tailed IAAFT surrogate p-values (None if the real
          delta itself is undefined, or if zero valid surrogate deltas)
      surrogate_CI_mean/std/n_valid/n_undefined,
      surrogate_beta_mean/std/n_valid/n_undefined: null-distribution
          summary stats and undefined-channel bookkeeping
      config: exact fixed parameters used (provenance)
    """
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    real_pre = compute_mse(pre, m=m, r_fraction=r_fraction, tau_min=tau_min,
                            min_points_at_coarsest=min_points_at_coarsest,
                            n_scales_cap=n_scales_cap, min_fit_points=min_fit_points)
    real_post = compute_mse(post, m=m, r_fraction=r_fraction, tau_min=tau_min,
                             min_points_at_coarsest=min_points_at_coarsest,
                             n_scales_cap=n_scales_cap, min_fit_points=min_fit_points)

    real_CI_pre = real_pre["CI"]
    real_CI_post = real_post["CI"]
    real_beta_pre = None if real_pre["beta"] is None else real_pre["beta"]["beta"]
    real_beta_post = None if real_post["beta"] is None else real_post["beta"]["beta"]

    delta_CI_real = _delta(real_CI_post, real_CI_pre)
    delta_beta_real = _delta(real_beta_post, real_beta_pre)

    rng = np.random.default_rng(seed)
    surr_delta_CI = []
    surr_delta_beta = []
    n_undef_CI = 0
    n_undef_beta = 0

    for _ in range(n_surrogates):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        mse_pre_s = compute_mse(surr_pre, m=m, r_fraction=r_fraction, tau_min=tau_min,
                                 min_points_at_coarsest=min_points_at_coarsest,
                                 n_scales_cap=n_scales_cap, min_fit_points=min_fit_points)
        mse_post_s = compute_mse(surr_post, m=m, r_fraction=r_fraction, tau_min=tau_min,
                                  min_points_at_coarsest=min_points_at_coarsest,
                                  n_scales_cap=n_scales_cap, min_fit_points=min_fit_points)

        d_CI = _delta(mse_post_s["CI"], mse_pre_s["CI"])
        if d_CI is None:
            n_undef_CI += 1
        else:
            surr_delta_CI.append(d_CI)

        b_pre_s = None if mse_pre_s["beta"] is None else mse_pre_s["beta"]["beta"]
        b_post_s = None if mse_post_s["beta"] is None else mse_post_s["beta"]["beta"]
        d_beta = _delta(b_post_s, b_pre_s)
        if d_beta is None:
            n_undef_beta += 1
        else:
            surr_delta_beta.append(d_beta)

    surr_delta_CI = np.array(surr_delta_CI, dtype=float)
    surr_delta_beta = np.array(surr_delta_beta, dtype=float)

    if delta_CI_real is None or len(surr_delta_CI) == 0:
        p_CI = None
    else:
        p_CI = float(np.mean(np.abs(surr_delta_CI) >= abs(delta_CI_real)))

    if delta_beta_real is None or len(surr_delta_beta) == 0:
        p_beta = None
    else:
        p_beta = float(np.mean(np.abs(surr_delta_beta) >= abs(delta_beta_real)))

    return {
        "real_pre": real_pre,
        "real_post": real_post,
        "CI_pre": real_CI_pre,
        "CI_post": real_CI_post,
        "beta_pre": real_beta_pre,
        "beta_post": real_beta_post,
        "delta_CI": delta_CI_real,
        "delta_beta": delta_beta_real,
        "p_CI": p_CI,
        "p_beta": p_beta,
        "surrogate_CI_mean": float(np.mean(surr_delta_CI)) if len(surr_delta_CI) else None,
        "surrogate_CI_std": float(np.std(surr_delta_CI)) if len(surr_delta_CI) else None,
        "surrogate_CI_n_valid": int(len(surr_delta_CI)),
        "surrogate_CI_n_undefined": int(n_undef_CI),
        "surrogate_beta_mean": float(np.mean(surr_delta_beta)) if len(surr_delta_beta) else None,
        "surrogate_beta_std": float(np.std(surr_delta_beta)) if len(surr_delta_beta) else None,
        "surrogate_beta_n_valid": int(len(surr_delta_beta)),
        "surrogate_beta_n_undefined": int(n_undef_beta),
        "config": {
            "m": m,
            "r_fraction": r_fraction,
            "tau_min": tau_min,
            "min_points_at_coarsest": min_points_at_coarsest,
            "n_scales_cap": n_scales_cap,
            "min_fit_points": min_fit_points,
            "n_surrogates": n_surrogates,
            "n_iaaft_iter": n_iter,
            "seed": seed,
        },
    }
