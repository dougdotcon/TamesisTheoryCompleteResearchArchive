"""
Canonical Multiscale Permutation Entropy (PE) + Jensen-Shannon
Complexity-Entropy Causality Plane pipeline for DISC-TRI-RG-001,
candidate `entropia-de-permutacao` (Bandt & Pompe 2002, PRL 88:174102;
Costa, Goldberger & Peng 2002/2005; Rosso, Larrondo, Martin, Plastino &
Fuentes 2007, PRL 99:154102; MPR statistical complexity construction,
Martin, Plastino & Rosso 2006, Physica A 369:439; Lamberti, Martin,
Plastino & Rosso 2004, Physica A 334:119).

Fixed BEFORE running on any real domain (VitalDB EEG anesthesia
induction, PhysioNet European ST-T Database transient ischemia) -- see
../METHODOLOGY_NOTE.md for the full rationale. This is a NEW,
self-contained implementation specific to this test line: it does not
import from, and is not derived from,
`mse_multiscale_entropy/analysis/mse_common.py` or
`rqa/analysis/rqa_common.py`, even though the coarse-graining formula
and the IAAFT surrogate step are the SAME published methods (Costa et
al.; Schreiber & Schmitz 1996) required by the methodology note for
cross-line consistency.

Method (METHODOLOGY_NOTE.md gaps (a)-(e)):
  1. Coarse-grain the (non-overlapping-block) series at scale `s`:
         x_j^(s) = (1/s) * sum_{i=(j-1)*s+1}^{j*s} x_i
     -- Costa et al.'s original definition, reused unmodified.
  2. On EACH coarse-grained series x^(s), build the ordinal-pattern
     (Bandt & Pompe 2002) empirical distribution P(s) over the m!=24
     possible permutations of an embedding window of length m=4 FIXED,
     delay tau_BP=1 FIXED (the coarse-graining scale `s` itself already
     plays the role of the multiscale time separation).
  3. H_S(s) = normalized Shannon entropy of P(s) (divided by log(m!)).
     PCI (Permutation Complexity Index) = sum of H_S(s) over the scale
     grid -- primary channel, mirrors CI in MSE.
  4. C_JS(s) = Q_0 * J[P(s), P_e] * H_S(s) -- Jensen-Shannon statistical
     complexity (Rosso et al. 2007 / MPR construction), P_e the uniform
     distribution over the m! permutations, Q_0 the standard MPR
     normalization constant. MCI (Multiscale Complexity Index) = sum of
     C_JS(s) over the same grid -- companion channel.
  5. IAAFT surrogates (Schreiber & Schmitz 1996) are the PRIMARY
     significance test for BOTH channels (gap (e)), same protocol
     already used for MSE/VG/RQA in this lab: N_SURROGATES=200,
     N_IAAFT_ITER=50, seed=12345, PRE/POST surrogates generated
     independently from their own real series, two-tailed p-values on
     the aggregated (summed-over-scales) Delta_PCI / Delta_MCI.

Scale grid (domain-agnostic, gap (a) of METHODOLOGY_NOTE.md):
  s_min = 1, s_max = floor(N / 120) (120 = 5*m! = 5*24, Riedl, Mueller &
  Wessel 2013, Eur. Phys. J. Special Topics 222:249, sample floor per
  scale for m=4), N_SCALES = min(15, s_max) log-spaced unique integers.
  If s_max < 1 the segment is too short even at s=1 -- an explicit
  "insufficient_samples" status is returned, never a silent partial
  result.

Any agent applying this pipeline to real data MUST import and call
`run_pe_analysis` (or the lower-level helpers) rather than
reimplementing any of this, so "same formula, no per-domain
reformulation" is a literal code-identity guarantee, matching the
discipline already used for `mse_common.py` / `rqa_common.py` in this
lab.
"""
import math

import numpy as np

# ---- fixed constants (METHODOLOGY_NOTE.md gaps (a)-(e) -- identical for
# every domain this pipeline is ever applied to; no per-domain tuning) ----
M_EMBED = 4                     # Bandt-Pompe embedding order, FIXED (not re-estimated)
TAU_BP = 1                      # Bandt-Pompe embedding delay, FIXED
S_MIN = 1                       # coarse-graining scale grid floor
N_MIN_PER_SCALE = 5 * math.factorial(M_EMBED)   # 5*24 = 120, Riedl-Mueller-Wessel 2013
N_SCALES_CAP = 15               # cap on log-spaced scale values
MAX_N_PER_SEGMENT = 20000       # subsampling cap, gap (d)
N_SURROGATES = 200              # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50               # IAAFT iterations per surrogate
SEED = 12345

N_STATES = math.factorial(M_EMBED)   # m! = 24 possible ordinal patterns
_UNIFORM_PE = np.full(N_STATES, 1.0 / N_STATES, dtype=float)
_LOG_N_STATES = math.log(N_STATES)


# --------------------------------------------------------------------------
# Gap (d): subsampling
# --------------------------------------------------------------------------

def subsample_segment(x, max_n=MAX_N_PER_SEGMENT):
    """Uniform-stride decimation to at most `max_n` samples.

    If len(x) <= max_n, returns x unchanged (stride=1, subsampled=False).
    Otherwise stride = ceil(N / max_n), x[::stride] -- identical
    convention already used in rqa_common.py / vg_common.py for this lab.
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


# --------------------------------------------------------------------------
# Gap (a): coarse-graining and scale grid (identical formula to MSE, but a
# fresh implementation -- see module docstring)
# --------------------------------------------------------------------------

def coarse_grain(x, s):
    """Non-overlapping block-average coarse-graining at scale `s`
    (Costa, Goldberger & Peng 2002/2005):
        x_j^(s) = (1/s) * sum_{i=(j-1)*s+1}^{j*s} x_i

    Returns a float array of length floor(N/s). Trailing points that do
    not fill a complete block of length s are dropped (Costa et al.'s
    convention -- no padding of partial blocks).
    """
    x = np.asarray(x, dtype=float)
    s = int(s)
    if s == 1:
        return x.copy()
    n_blocks = len(x) // s
    if n_blocks < 1:
        return np.array([], dtype=float)
    trimmed = x[: n_blocks * s].reshape(n_blocks, s)
    return trimmed.mean(axis=1)


def scale_grid(N, s_min=S_MIN, n_min_per_scale=N_MIN_PER_SCALE, n_scales_cap=N_SCALES_CAP):
    """Log-spaced integer scale grid s in [s_min, s_max], unique values.

    s_max = floor(N / n_min_per_scale); N_SCALES = min(n_scales_cap,
    s_max). Returns (scales, s_max, status) where status is "ok" or
    "insufficient_samples" (s_max < s_min, i.e. fewer than
    n_min_per_scale samples even at s=1) -- in the latter case `scales`
    is an empty array and callers must not silently proceed.
    """
    s_max = int(np.floor(N / n_min_per_scale))
    if s_max < s_min:
        return np.array([], dtype=int), s_max, "insufficient_samples"
    n_scales = min(n_scales_cap, s_max)
    if n_scales <= 1:
        raw = np.array([s_min], dtype=float)
    else:
        raw = np.exp(np.linspace(np.log(s_min), np.log(s_max), n_scales))
    scales = np.unique(np.round(raw).astype(int))
    scales = scales[(scales >= s_min) & (scales <= s_max)]
    return scales, s_max, "ok"


# --------------------------------------------------------------------------
# Gap (b): Bandt-Pompe ordinal-pattern embedding + distribution
# --------------------------------------------------------------------------

def ordinal_pattern_codes(x, m=M_EMBED, tau=TAU_BP):
    """Bandt & Pompe (2002) ordinal-pattern code for every embedding
    vector of `x` at order `m`, delay `tau`. Ties are broken by keeping
    the original (temporal) order among equal values (stable sort) --
    the standard Bandt & Pompe convention.

    Each embedding vector's ordinal pattern (the permutation of
    {0,...,m-1} given by argsort of the vector) is mapped to a unique
    integer in [0, m!) via its Lehmer code, computed vectorized over all
    embedding vectors at once (fast even for N up to
    MAX_N_PER_SEGMENT=20000; m is fixed at 4 so the O(m^2) Lehmer-code
    step is a small constant-size loop).

    Returns an int64 array of length N - (m-1)*tau (>= 0; empty if the
    series is too short for even one embedding vector).
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    tau = int(tau)
    m = int(m)
    n_vec = n - (m - 1) * tau
    if n_vec < 1:
        return np.array([], dtype=np.int64)

    if tau == 1:
        windows = np.lib.stride_tricks.sliding_window_view(x, m)
    else:
        idx = np.arange(n_vec)[:, None] + np.arange(m)[None, :] * tau
        windows = x[idx]

    order = np.argsort(windows, axis=1, kind="stable")  # (n_vec, m), permutation of 0..m-1

    codes = np.zeros(n_vec, dtype=np.int64)
    for i in range(m):
        fact = math.factorial(m - 1 - i)
        if fact == 0:
            fact = 1
        less = np.zeros(n_vec, dtype=np.int64)
        for j in range(i + 1, m):
            less += (order[:, j] < order[:, i]).astype(np.int64)
        codes += less * fact
    return codes


def pattern_distribution(x, m=M_EMBED, tau=TAU_BP):
    """Empirical ordinal-pattern distribution P over the m! possible
    patterns (Bandt & Pompe 2002), as a length-m! probability array
    (zero-count patterns included explicitly, needed for the
    Jensen-Shannon divergence against the uniform P_e below).

    Returns (P, n_windows), or (None, 0) if the series has fewer than
    one full embedding vector.
    """
    codes = ordinal_pattern_codes(x, m=m, tau=tau)
    n_windows = len(codes)
    if n_windows == 0:
        return None, 0
    n_states = math.factorial(m)
    counts = np.bincount(codes, minlength=n_states)
    P = counts.astype(float) / n_windows
    return P, n_windows


# --------------------------------------------------------------------------
# H_S (normalized Shannon entropy) and C_JS (Jensen-Shannon statistical
# complexity, Rosso et al. 2007 / MPR construction)
# --------------------------------------------------------------------------

def normalized_shannon_entropy(P):
    """H_S = -sum_pi p(pi)*ln(p(pi)) / ln(m!), normalized to [0,1]."""
    P = np.asarray(P, dtype=float)
    nz = P[P > 0]
    S = -np.sum(nz * np.log(nz))
    n_states = len(P)
    return float(S / math.log(n_states))


def _shannon_entropy_nats(P):
    """Non-normalized Shannon entropy in nats, -sum p*ln(p) (0*ln(0):=0)."""
    P = np.asarray(P, dtype=float)
    nz = P[P > 0]
    return float(-np.sum(nz * np.log(nz)))


def jensen_shannon_divergence(P, Pe):
    """J[P, P_e] = S[(P+P_e)/2] - S[P]/2 - S[P_e]/2 (Shannon entropy in
    nats, natural log) -- the Jensen-Shannon divergence between the
    observed ordinal-pattern distribution P and the uniform reference
    P_e (Lamberti et al. 2004; Rosso et al. 2007)."""
    P = np.asarray(P, dtype=float)
    Pe = np.asarray(Pe, dtype=float)
    M = 0.5 * (P + Pe)
    return _shannon_entropy_nats(M) - 0.5 * _shannon_entropy_nats(P) - 0.5 * _shannon_entropy_nats(Pe)


def q0_constant(n_states):
    """Q_0, the standard MPR normalization constant (Lamberti et al.
    2004; Rosso et al. 2007) that keeps C_JS bounded in an [0,1]-ish
    range:
        Q_0 = -2 * [ ((N+1)/N)*ln(N+1) - 2*ln(2N) + ln(N) ]^-1
    where N = m! is the number of accessible ordinal-pattern states.
    """
    N = float(n_states)
    bracket = ((N + 1.0) / N) * math.log(N + 1.0) - 2.0 * math.log(2.0 * N) + math.log(N)
    return -2.0 / bracket


Q0 = q0_constant(N_STATES)  # fixed once, m=4 -> N_STATES=24 is FIXED for this pipeline


def statistical_complexity(P, Pe=_UNIFORM_PE, Q0_const=Q0, H_S=None):
    """C_JS(s) = Q_0 * J[P, P_e] * H_S -- Jensen-Shannon statistical
    complexity (Rosso et al. 2007 / MPR construction). `H_S` may be
    passed in (already computed) to avoid recomputation; if None it is
    computed here from P."""
    if H_S is None:
        H_S = normalized_shannon_entropy(P)
    J = jensen_shannon_divergence(P, Pe)
    return float(Q0_const * J * H_S)


# --------------------------------------------------------------------------
# Full PE/C_JS curve + PCI/MCI channels for one segment
# --------------------------------------------------------------------------

def compute_pe(x, m=M_EMBED, tau=TAU_BP, s_min=S_MIN,
                n_min_per_scale=N_MIN_PER_SCALE, n_scales_cap=N_SCALES_CAP,
                max_n=MAX_N_PER_SEGMENT):
    """Run the full multiscale ordinal-pattern pipeline on one segment:
    subsample if needed (gap (d)), build the scale grid (gap (a)),
    coarse-grain + compute the ordinal-pattern distribution at each
    scale, then H_S(s)/C_JS(s) and their sums PCI/MCI.

    Returns a dict with `status` ("ok" or "insufficient_samples") and,
    when "ok":
      n_samples_original, n_samples_used, subsample_info,
      s_min, s_max, scales_used (list[int]),
      H_S_values, C_JS_values (list[float], one per scale in
          scales_used -- always defined, unlike SampEn/FNN this
          statistic never fails to compute once n_windows>=1),
      n_windows_per_scale (list[int]),
      PCI: sum of H_S_values over the WHOLE grid,
      MCI: sum of C_JS_values over the WHOLE grid,
      n_scales_achieved: len(scales_used).
    When "insufficient_samples": n_samples_original, s_max (< s_min),
    n_min_per_scale -- no scale grid could be formed, nothing computed.
    """
    x_raw = np.asarray(x, dtype=float)
    n_original = int(len(x_raw))
    x_used, sub_info = subsample_segment(x_raw, max_n=max_n)
    N = len(x_used)

    scales, s_max, grid_status = scale_grid(N, s_min=s_min,
                                             n_min_per_scale=n_min_per_scale,
                                             n_scales_cap=n_scales_cap)
    if grid_status == "insufficient_samples":
        return {
            "status": "insufficient_samples",
            "n_samples_original": n_original,
            "n_samples_used": int(N),
            "subsample_info": sub_info,
            "s_min": s_min,
            "s_max": int(s_max),
            "n_min_per_scale": n_min_per_scale,
        }

    H_S_values = []
    C_JS_values = []
    n_windows_per_scale = []
    for s in scales:
        coarse = coarse_grain(x_used, s)
        P, n_windows = pattern_distribution(coarse, m=m, tau=tau)
        n_windows_per_scale.append(int(n_windows))
        if P is None:
            # should not happen given the s_max floor, but never silently
            # substitute -- surface it explicitly if it ever does.
            H_S_values.append(None)
            C_JS_values.append(None)
            continue
        h_s = normalized_shannon_entropy(P)
        c_js = statistical_complexity(P, H_S=h_s)
        H_S_values.append(h_s)
        C_JS_values.append(c_js)

    n_undefined = sum(1 for v in H_S_values if v is None)
    if n_undefined == 0:
        PCI = float(sum(H_S_values))
        MCI = float(sum(C_JS_values))
    else:
        PCI = None
        MCI = None

    return {
        "status": "ok",
        "n_samples_original": n_original,
        "n_samples_used": int(N),
        "subsample_info": sub_info,
        "s_min": int(s_min),
        "s_max": int(s_max),
        "scales_used": scales.tolist(),
        "H_S_values": H_S_values,
        "C_JS_values": C_JS_values,
        "n_windows_per_scale": n_windows_per_scale,
        "n_scales_achieved": int(len(scales)),
        "n_scales_undefined": int(n_undefined),
        "PCI": PCI,
        "MCI": MCI,
        "m": m,
        "tau_bp": tau,
    }


# --------------------------------------------------------------------------
# Gap (e): IAAFT surrogates (Schreiber & Schmitz 1996)
# --------------------------------------------------------------------------

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate
    (Schreiber & Schmitz 1996).

    Preserves the linear power spectrum (FFT amplitude spectrum) and the
    exact empirical amplitude distribution (histogram) of `x`; destroys
    any nonlinear phase/temporal structure beyond what a linear Gaussian
    process with the same spectrum and marginal would produce.
    Independent reimplementation for this test line -- see module
    docstring.

    Algorithm: start from a random permutation of x's values, then
    alternately (1) impose the target amplitude spectrum in the
    frequency domain while keeping the current phases, and (2) impose
    the exact target rank order (amplitude distribution) in the time
    domain, for `n_iter` rounds.
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
# Gap (e) pre-authorized fallback: moving-block bootstrap (Kunsch 1989),
# added here (not used unless synthetic validation shows low IAAFT power
# for a channel, per METHODOLOGY_NOTE.md Gap (b)) -- same machinery/API
# style already used in rqa_common.py / soc_avalanches for this lab.
# --------------------------------------------------------------------------

def moving_block_bootstrap_resample(x, L, rng):
    """One moving-block-bootstrap resample of `x` (Kunsch 1989): blocks
    of length L, start index drawn uniformly at random with replacement,
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


def run_block_bootstrap_test(pre_segment, post_segment, L=None, n_bootstrap=N_SURROGATES,
                              seed=SEED, m=M_EMBED, tau=TAU_BP, s_min=S_MIN,
                              n_min_per_scale=N_MIN_PER_SCALE, n_scales_cap=N_SCALES_CAP,
                              max_n=MAX_N_PER_SEGMENT):
    """Moving-block bootstrap (Kunsch 1989) significance test for
    Delta_PCI / Delta_MCI, PRE and POST resampled independently
    `n_bootstrap` times each, i-th pairing (matching rqa_common.py's
    convention). Block length L defaults to max(2*s_max_pre, 10) if not
    given (tied to the segment's own coarsest identifiable timescale).
    Only invoked for a channel if the synthetic validation shows IAAFT
    has low power for it (METHODOLOGY_NOTE.md Gap (b) pre-authorized
    fallback) -- NOT part of the default pipeline.
    """
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    real_pre = compute_pe(pre, m=m, tau=tau, s_min=s_min,
                           n_min_per_scale=n_min_per_scale, n_scales_cap=n_scales_cap, max_n=max_n)
    real_post = compute_pe(post, m=m, tau=tau, s_min=s_min,
                            n_min_per_scale=n_min_per_scale, n_scales_cap=n_scales_cap, max_n=max_n)

    if L is None:
        s_max_pre = real_pre.get("s_max", 1) if real_pre["status"] == "ok" else 1
        L = max(2 * max(s_max_pre, 1), 10)

    rng = np.random.default_rng(seed)

    def _boot_series(segment, n):
        pci_vals, mci_vals = [], []
        for _ in range(n):
            resampled = moving_block_bootstrap_resample(segment, L, rng)
            feat = compute_pe(resampled, m=m, tau=tau, s_min=s_min,
                               n_min_per_scale=n_min_per_scale, n_scales_cap=n_scales_cap, max_n=max_n)
            if feat["status"] == "ok":
                pci_vals.append(feat["PCI"])
                mci_vals.append(feat["MCI"])
            else:
                pci_vals.append(None)
                mci_vals.append(None)
        return pci_vals, mci_vals

    pci_boot_pre, mci_boot_pre = _boot_series(pre, n_bootstrap)
    pci_boot_post, mci_boot_post = _boot_series(post, n_bootstrap)

    def _pair_deltas(pre_vals, post_vals):
        deltas, n_undef = [], 0
        for vp, vq in zip(pre_vals, post_vals):
            if vp is None or vq is None:
                n_undef += 1
            else:
                deltas.append(vq - vp)
        return np.array(deltas, dtype=float), n_undef

    delta_pci_boot, n_undef_pci = _pair_deltas(pci_boot_pre, pci_boot_post)
    delta_mci_boot, n_undef_mci = _pair_deltas(mci_boot_pre, mci_boot_post)

    def _two_tailed_p(deltas):
        if len(deltas) == 0:
            return None
        frac_le0 = float(np.mean(deltas <= 0))
        frac_ge0 = float(np.mean(deltas >= 0))
        return float(2 * min(frac_le0, frac_ge0))

    delta_pci_real = None
    delta_mci_real = None
    if real_pre["status"] == "ok" and real_post["status"] == "ok" and \
            real_pre["PCI"] is not None and real_post["PCI"] is not None:
        delta_pci_real = real_post["PCI"] - real_pre["PCI"]
    if real_pre["status"] == "ok" and real_post["status"] == "ok" and \
            real_pre["MCI"] is not None and real_post["MCI"] is not None:
        delta_mci_real = real_post["MCI"] - real_pre["MCI"]

    return {
        "bootstrap_block_length": int(L),
        "bootstrap_n_bootstrap": int(n_bootstrap),
        "bootstrap_seed": int(seed),
        "delta_PCI_real": delta_pci_real,
        "delta_MCI_real": delta_mci_real,
        "bootstrap_delta_PCI_mean": float(np.mean(delta_pci_boot)) if len(delta_pci_boot) else None,
        "bootstrap_delta_PCI_std": float(np.std(delta_pci_boot)) if len(delta_pci_boot) else None,
        "bootstrap_delta_PCI_ci95": (
            (float(np.percentile(delta_pci_boot, 2.5)), float(np.percentile(delta_pci_boot, 97.5)))
            if len(delta_pci_boot) else None
        ),
        "bootstrap_delta_PCI_p": _two_tailed_p(delta_pci_boot),
        "bootstrap_delta_PCI_n_valid": int(len(delta_pci_boot)),
        "bootstrap_delta_PCI_n_undefined": int(n_undef_pci),
        "bootstrap_delta_MCI_mean": float(np.mean(delta_mci_boot)) if len(delta_mci_boot) else None,
        "bootstrap_delta_MCI_std": float(np.std(delta_mci_boot)) if len(delta_mci_boot) else None,
        "bootstrap_delta_MCI_ci95": (
            (float(np.percentile(delta_mci_boot, 2.5)), float(np.percentile(delta_mci_boot, 97.5)))
            if len(delta_mci_boot) else None
        ),
        "bootstrap_delta_MCI_p": _two_tailed_p(delta_mci_boot),
        "bootstrap_delta_MCI_n_valid": int(len(delta_mci_boot)),
        "bootstrap_delta_MCI_n_undefined": int(n_undef_mci),
    }


# --------------------------------------------------------------------------
# Full PRE/POST transition test pipeline (public entry point)
# --------------------------------------------------------------------------

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def run_pe_analysis(pre_series, post_series, seed=SEED, n_surrogates=N_SURROGATES,
                     n_iter=N_IAAFT_ITER, m=M_EMBED, tau=TAU_BP, s_min=S_MIN,
                     n_min_per_scale=N_MIN_PER_SCALE, n_scales_cap=N_SCALES_CAP,
                     max_n=MAX_N_PER_SEGMENT, n_mc=None):
    """Run the full multiscale permutation-entropy + Jensen-Shannon
    complexity transition test between a PRE and a POST segment, per
    METHODOLOGY_NOTE.md gaps (a)-(e). This is the single entry point a
    real-data script must call WITHOUT modification (per task
    instructions), exactly as `run_mse_pipeline`/`run_rqa_analysis` are
    called elsewhere in this lab.

    Each segment gets its OWN scale grid (s_max depends on that
    segment's own N after subsampling) -- consistent with how this lab
    already treats PRE/POST asymmetric sample sizes elsewhere in this
    line.

    IAAFT is the PRIMARY significance test for BOTH channels (gap (e)):
    `n_surrogates` independent PRE/POST surrogate pairs, each surrogate
    generated from its OWN real segment (never cross-segment), fixed
    seed=12345 convention used elsewhere in this lab. Two-tailed test:
    p = fraction of surrogates with |Delta_PCI_surrogate| >=
    |Delta_PCI_real| (and equivalently for Delta_MCI).

    `n_mc` overrides `n_surrogates` when given (validation-script
    convenience for smaller/faster runs); when None, `n_surrogates` is
    used unchanged.

    Returns a dict:
      status: "ok" if BOTH real_pre and real_post reached "ok" in
          compute_pe, else "insufficient_samples" (with real_pre/
          real_post carrying whichever diagnostic is available -- no
          real/surrogate computation is attempted in that case).
      real_pre, real_post: full compute_pe() output for each segment
      PCI_pre, PCI_post, MCI_pre, MCI_post: real (non-surrogate) values
      delta_PCI, delta_MCI: real POST - PRE (None if either side undefined)
      p_PCI, p_MCI: two-tailed IAAFT surrogate p-values (None if the
          real delta is undefined, or zero valid surrogate deltas)
      surrogate_PCI_mean/std/n_valid/n_undefined,
      surrogate_MCI_mean/std/n_valid/n_undefined: null-distribution
          summary stats and undefined-channel bookkeeping
      surrogate_PCI_deltas, surrogate_MCI_deltas: the FULL null arrays
          (needed for honest sigma-equivalent / distribution reporting
          in the validation step, not just summary stats)
      config: exact fixed parameters used (provenance)
    """
    n_surr = n_mc if n_mc is not None else n_surrogates

    pre_raw = np.asarray(pre_series, dtype=float)
    post_raw = np.asarray(post_series, dtype=float)

    # Gap (d): subsample ONCE, up front, before anything else touches the
    # series -- including IAAFT surrogate generation. This mirrors the
    # convention already established (and audited) for MAX_N_PER_SEGMENT
    # in rqa_common.py's run_rqa_analysis in this same lab/line: without
    # this, IAAFT (FFT + argsort per iteration, N_IAAFT_ITER times,
    # N_SURROGATES times, for BOTH pre and post) would run at the FULL
    # un-subsampled segment length, defeating the entire point of the
    # computational-budget rule Gap (d) declares (and making a real-data
    # segment of, e.g., 10^6+ samples computationally infeasible within
    # the 200-surrogates x 50-iterations protocol). compute_pe()'s own
    # internal subsample_segment() call becomes a no-op here (already
    # <= max_n), so this changes nothing for any series already <= max_n
    # (in particular, every synthetic validation control in this line
    # used N=3000 < max_n=20000, so validate_synthetic.py's results are
    # completely unaffected by this fix).
    pre, pre_sub_info = subsample_segment(pre_raw, max_n=max_n)
    post, post_sub_info = subsample_segment(post_raw, max_n=max_n)

    real_pre = compute_pe(pre, m=m, tau=tau, s_min=s_min,
                           n_min_per_scale=n_min_per_scale, n_scales_cap=n_scales_cap, max_n=max_n)
    real_post = compute_pe(post, m=m, tau=tau, s_min=s_min,
                            n_min_per_scale=n_min_per_scale, n_scales_cap=n_scales_cap, max_n=max_n)

    config = {
        "m": m, "tau_bp": tau, "s_min": s_min, "n_min_per_scale": n_min_per_scale,
        "n_scales_cap": n_scales_cap, "max_n_per_segment": max_n,
        "n_surrogates": n_surr, "n_iaaft_iter": n_iter, "seed": seed,
        "Q0": Q0, "n_states": N_STATES,
        "pre_subsample_info": pre_sub_info, "post_subsample_info": post_sub_info,
    }

    if real_pre["status"] != "ok" or real_post["status"] != "ok":
        return {
            "status": "insufficient_samples",
            "real_pre": real_pre,
            "real_post": real_post,
            "config": config,
        }

    PCI_pre, PCI_post = real_pre["PCI"], real_post["PCI"]
    MCI_pre, MCI_post = real_pre["MCI"], real_post["MCI"]

    delta_PCI_real = _delta(PCI_post, PCI_pre)
    delta_MCI_real = _delta(MCI_post, MCI_pre)

    rng = np.random.default_rng(seed)
    surr_delta_PCI = []
    surr_delta_MCI = []
    n_undef_PCI = 0
    n_undef_MCI = 0

    for _ in range(n_surr):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        pe_pre_s = compute_pe(surr_pre, m=m, tau=tau, s_min=s_min,
                               n_min_per_scale=n_min_per_scale, n_scales_cap=n_scales_cap, max_n=max_n)
        pe_post_s = compute_pe(surr_post, m=m, tau=tau, s_min=s_min,
                                n_min_per_scale=n_min_per_scale, n_scales_cap=n_scales_cap, max_n=max_n)

        pci_pre_s = pe_pre_s["PCI"] if pe_pre_s["status"] == "ok" else None
        pci_post_s = pe_post_s["PCI"] if pe_post_s["status"] == "ok" else None
        d_pci = _delta(pci_post_s, pci_pre_s)
        if d_pci is None:
            n_undef_PCI += 1
        else:
            surr_delta_PCI.append(d_pci)

        mci_pre_s = pe_pre_s["MCI"] if pe_pre_s["status"] == "ok" else None
        mci_post_s = pe_post_s["MCI"] if pe_post_s["status"] == "ok" else None
        d_mci = _delta(mci_post_s, mci_pre_s)
        if d_mci is None:
            n_undef_MCI += 1
        else:
            surr_delta_MCI.append(d_mci)

    surr_delta_PCI = np.array(surr_delta_PCI, dtype=float)
    surr_delta_MCI = np.array(surr_delta_MCI, dtype=float)

    if delta_PCI_real is None or len(surr_delta_PCI) == 0:
        p_PCI = None
    else:
        p_PCI = float(np.mean(np.abs(surr_delta_PCI) >= abs(delta_PCI_real)))

    if delta_MCI_real is None or len(surr_delta_MCI) == 0:
        p_MCI = None
    else:
        p_MCI = float(np.mean(np.abs(surr_delta_MCI) >= abs(delta_MCI_real)))

    return {
        "status": "ok",
        "real_pre": real_pre,
        "real_post": real_post,
        "PCI_pre": PCI_pre,
        "PCI_post": PCI_post,
        "MCI_pre": MCI_pre,
        "MCI_post": MCI_post,
        "delta_PCI": delta_PCI_real,
        "delta_MCI": delta_MCI_real,
        "p_PCI": p_PCI,
        "p_MCI": p_MCI,
        "surrogate_PCI_mean": float(np.mean(surr_delta_PCI)) if len(surr_delta_PCI) else None,
        "surrogate_PCI_std": float(np.std(surr_delta_PCI)) if len(surr_delta_PCI) else None,
        "surrogate_PCI_n_valid": int(len(surr_delta_PCI)),
        "surrogate_PCI_n_undefined": int(n_undef_PCI),
        "surrogate_MCI_mean": float(np.mean(surr_delta_MCI)) if len(surr_delta_MCI) else None,
        "surrogate_MCI_std": float(np.std(surr_delta_MCI)) if len(surr_delta_MCI) else None,
        "surrogate_MCI_n_valid": int(len(surr_delta_MCI)),
        "surrogate_MCI_n_undefined": int(n_undef_MCI),
        "surrogate_PCI_deltas": surr_delta_PCI.tolist(),
        "surrogate_MCI_deltas": surr_delta_MCI.tolist(),
        "config": config,
    }
