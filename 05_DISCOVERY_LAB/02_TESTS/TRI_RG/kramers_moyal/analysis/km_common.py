"""
Kramers-Moyal / stochastic Fokker-Planck reconstruction pipeline for
DISC-TRI-RG-001, candidate `kramers-moyal` (Risken 1996, *The
Fokker-Planck Equation*; Friedrich, Peinke & Renner 2000, PRL 84:5224;
Ragwitz & Kantz 2001, PRL 87:254501; Gottschall & Peinke 2008, New J.
Phys. 10:083034; Livina & Lenton 2007, GRL 34:L03712; Ritchie & Sieber
2016, arXiv:1609.07271, for the a priori `kappa` demotion).

Fixed BEFORE running on any real domain (EUR/CHF tick-a-tick, SNB shock;
PhysioNet vfdb malignant ventricular arrhythmia) -- see
../METHODOLOGY_NOTE.md for the exact, already-locked specification this
module implements without deviation. New, self-contained implementation
for this test line (not imported from mse_common.py / rqa_common.py /
vg_common.py / pe_common.py), reusing only the SAME published protocols
(IAAFT: Schreiber & Schmitz 1996) already used across this lab for
cross-line consistency.

Method (METHODOLOGY_NOTE.md gaps (a)-(e)):
  (a) Markov-Einstein / Chapman-Kolmogorov test for `tau_ME`. Geometric
      candidate-lag grid, N_BINS_X=10 quantile bins from PRE (shared with
      gap (b)). At each candidate lag: 1-step transition matrix P1
      (binned), CK convolution prediction P2_CK = P1 @ P1 for the 2-step
      transition, compared against the DIRECTLY estimated 2-step
      transition P2_direct via a chi-square distance between the two
      transition histograms, bootstrap p-value (N_BOOTSTRAP_CK=200,
      resampling of time indices with replacement -- see
      `ck_test_at_lag` docstring for the exact resampling scheme and its
      rationale). `tau_ME` = smallest grid lag with p_ck_test>=0.05 AT
      that lag AND the following 2 grid points. If none found:
      "markov_property_not_established", not a forced fallback.
  (b) D1(x)/D2(x)/D3(x)/D4(x) estimation at tau_ME, same N_BINS_X=10 PRE
      bins, MIN_SAMPLES_PER_BIN=30 floor (undefined bins -> NaN, never
      extrapolated). Stationary density p_st(x) reconstructed from
      D1/D2 (standard stationary Fokker-Planck solution). PKS = weighted
      excess kurtosis of p_st (primary channel). beta_D2 = OLS slope of
      D2(x) vs x (companion channel). kappa = -D1'(x*) computed and
      reported but marked `diagnostic_only=True` and NEVER fed into any
      p-value/decision logic -- Ritchie & Sieber 2016's algebraic
      identity between kappa and AC1/variance (the `critical_slowing_
      down` basis, already closed negative in this line) is resolved a
      priori, not discovered post-hoc.
  (c)/(d) PRE/POST segment convention and MAX_N_PER_SEGMENT=50000
      subsampling (uniform-stride decimation) are domain-agnostic here;
      subsampling is applied ONCE, at the very top of
      `run_km_analysis`, before the CK-test grid, before D1..D4, before
      ANY surrogate generation -- learned explicitly from the real bug
      found in `permutation_entropy/analysis/pe_common.py` (subsampling
      applied inconsistently, discovered only at the real-data step; see
      that line's RESULTS_SUMMARY.md, "Correcao de desempenho").
  (e) IAAFT surrogates (Schreiber & Schmitz 1996), N_SURROGATES=200,
      N_IAAFT_ITER=50, seed=12345, PRE/POST surrogates generated
      independently from their own real series. Each surrogate reuses
      the ALREADY-FIXED tau_ME (in samples) and x-bins from the real PRE
      -- never re-estimated per surrogate (explicitly authorized by
      METHODOLOGY_NOTE.md gap (e), also keeps cost bounded: re-running
      the CK-test-with-bootstrap 200+ times would be prohibitively
      expensive and is not required). Two-tailed p-values for
      Delta_PKS and Delta_beta_D2.

Any agent applying this pipeline to real data MUST import and call
`run_km_analysis` rather than reimplementing any of this -- "same
formula, no per-domain reformulation", matching the discipline already
used for every other _common.py module in this lab/line.
"""
import math

import numpy as np

# ---- fixed constants (METHODOLOGY_NOTE.md gaps (a)-(e) -- identical for
# every domain this pipeline is ever applied to; no per-domain tuning) ----
N_BINS_X = 10                    # quantile bins from PRE, shared CK-test + D1/D2
N_LAG_MAX = 20                   # cap on candidate-lag grid points
LAG_GROWTH = 1.5                 # geometric growth factor for the lag grid
LAG_MAX_FRAC = 0.05              # candidate lag capped at 5% of PRE segment length
N_BOOTSTRAP_CK = 200             # bootstrap replicas for the CK chi-square test
MIN_SAMPLES_PER_BIN = 30         # floor for D1..D4 AND for CK chi-square rows
CK_ALPHA = 0.05                  # non-rejection threshold for the CK test
CK_ROBUST_NEXT = 2               # confirm non-rejection at the next 2 grid points too
MAX_N_PER_SEGMENT = 50000        # subsampling cap, gap (d)
N_SURROGATES = 200               # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50                # IAAFT iterations per surrogate
SEED = 12345


# --------------------------------------------------------------------------
# Gap (d): subsampling -- applied ONCE, at the very top of run_km_analysis,
# before anything else (see module docstring / permutation_entropy bug).
# --------------------------------------------------------------------------

def subsample_segment(x, max_n=MAX_N_PER_SEGMENT):
    """Uniform-stride decimation to at most `max_n` samples. Identical
    convention already used across this lab (rqa_common.py, vg_common.py,
    pe_common.py) for this line."""
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
# Shared N_BINS_X=10 quantile binning, computed ONCE from PRE (gap (a)/(b))
# --------------------------------------------------------------------------

def compute_quantile_bins(x, n_bins=N_BINS_X):
    """N_BINS_X quantile-edge bin boundaries from `x` (meant to be called
    on the real PRE segment only). The outer edges are widened to +-inf
    so that ANY future value (POST, surrogates, out-of-sample tails)
    always falls into one of the n_bins buckets rather than being
    silently dropped -- an explicit design choice, documented here."""
    x = np.asarray(x, dtype=float)
    qs = np.linspace(0.0, 1.0, n_bins + 1)
    edges = np.quantile(x, qs).astype(float)
    edges[0] = -np.inf
    edges[-1] = np.inf
    return edges


def bin_index(x, edges, n_bins=N_BINS_X):
    """Bin index in [0, n_bins-1] for each value of `x`, using the
    n_bins-1 interior (finite) edges of `edges`."""
    x = np.asarray(x, dtype=float)
    interior = edges[1:-1]
    idx = np.digitize(x, interior)
    return np.clip(idx, 0, n_bins - 1)


def bin_centers_from_edges(edges, x_ref, n_bins=N_BINS_X):
    """Bin 'centers' for reporting/OLS/kurtosis: the median of the
    REFERENCE (PRE) sample's own values within each bin -- avoids the
    undefined-midpoint problem for the +-inf outer edges."""
    idx = bin_index(x_ref, edges, n_bins)
    x_ref = np.asarray(x_ref, dtype=float)
    centers = np.full(n_bins, np.nan)
    for b in range(n_bins):
        vals = x_ref[idx == b]
        if len(vals) > 0:
            centers[b] = float(np.median(vals))
    return centers


# --------------------------------------------------------------------------
# Gap (a): candidate-lag grid (geometric, growth 1.5, native dt to 5% of
# segment length or N_LAG_MAX points, whichever first)
# --------------------------------------------------------------------------

def lag_grid_samples(n_pre_used, n_lag_max=N_LAG_MAX, growth=LAG_GROWTH, max_frac=LAG_MAX_FRAC):
    """Geometric candidate-lag grid IN SAMPLES: starts at 1 sample (=dt),
    growth factor `growth`, unique increasing integers, stopping at
    `n_lag_max` points OR when the lag would exceed `max_frac` of the
    segment length (in samples -- equivalent to `max_frac` of the
    segment length in time units, since dt cancels: L*dt > f*N*dt <=>
    L > f*N). Returns (lags_samples: list[int], max_lag_samples: float).
    """
    max_lag_samples = max_frac * n_pre_used
    lags = []
    k = 1.0
    safety = 0
    while len(lags) < n_lag_max and safety < 500:
        safety += 1
        L = max(1, int(round(k)))
        if L > max_lag_samples:
            break
        if not lags or L != lags[-1]:
            lags.append(L)
        k *= growth
    return lags, float(max_lag_samples)


# --------------------------------------------------------------------------
# Gap (a): Chapman-Kolmogorov test at one candidate lag
# --------------------------------------------------------------------------

def _transition_counts(b1, b2, n_bins=N_BINS_X):
    C = np.zeros((n_bins, n_bins), dtype=float)
    np.add.at(C, (b1, b2), 1.0)
    return C


def _transition_probs(C):
    row_sums = C.sum(axis=1)
    P = np.zeros_like(C)
    valid = row_sums > 0
    P[valid] = C[valid] / row_sums[valid, None]
    return P, row_sums


def _ck_chi2_stat(b1, b2, b3, n_bins=N_BINS_X, min_samples_per_bin=MIN_SAMPLES_PER_BIN):
    """Chi-square distance between the DIRECTLY estimated 2-step
    transition histogram (b1->b3, at lag 2L) and the CK-convolution
    PREDICTION built from the 1-step transition matrix (b1->b2, at lag
    L), P2_CK = P1 @ P1. Only rows (starting bins b1) with at least
    `min_samples_per_bin` in BOTH the 1-step and 2-step data are
    included, and only cells with nonzero predicted count -- reuses the
    already-declared MIN_SAMPLES_PER_BIN floor (gap (b)) here too, for
    the same reason: an unstable few-sample row/cell would inject noise
    into the chi-square sum, not signal.
    """
    C1 = _transition_counts(b1, b2, n_bins)
    P1, row_sums1 = _transition_probs(C1)
    C2 = _transition_counts(b1, b3, n_bins)
    row_sums2 = C2.sum(axis=1)
    P2_ck = P1 @ P1

    chi2 = 0.0
    n_rows_used = 0
    for b in range(n_bins):
        if row_sums2[b] < min_samples_per_bin or row_sums1[b] < min_samples_per_bin:
            continue
        E = row_sums2[b] * P2_ck[b]
        O = C2[b]
        mask = E > 1e-12
        if not np.any(mask):
            continue
        chi2 += float(np.sum((O[mask] - E[mask]) ** 2 / E[mask]))
        n_rows_used += 1
    return chi2, n_rows_used


def _markov_bootstrap_triples(b1, b2, max_t, n_bins, rng):
    """One bootstrap replica of a 2-step (b1,b2,b3) triple set, built by
    RESAMPLING TIME INDICES WITH REPLACEMENT from the pool of actually
    OBSERVED 1-step transitions, conditioned on the current bin, at
    EACH of the two simulated steps (a nonparametric "conditional
    Markov bootstrap", Politis 2003-style). Starting bins are drawn
    from the empirical b1 marginal (with replacement); the 1st and 2nd
    simulated steps both resample a transition-target INDEX (with
    replacement) from the pool of real indices t' with b1[t']==current
    bin, and take the OBSERVED b2[t'] as the next state -- so the
    resulting simulated (b1,b2,b3) triples are, by construction, an
    EXACT realization of a 2-step Markov chain driven by the empirical
    1-step kernel, with the same finite-sample noise level (same total
    N) as the real triple set. See `ck_test_at_lag` docstring for why
    this replaces a naive whole-triple case-resampling bootstrap."""
    pools = [np.where(b1 == b)[0] for b in range(n_bins)]

    start_idx = rng.integers(0, len(b1), size=max_t)
    b1_sim = b1[start_idx]

    def _resample_step(current_bins):
        nxt = np.empty(max_t, dtype=int)
        for b in range(n_bins):
            mask = current_bins == b
            cnt = int(mask.sum())
            if cnt == 0:
                continue
            pool = pools[b]
            if len(pool) == 0:
                nxt[mask] = b  # no observed transition from this bin; stay put (guarded, should not occur given MIN_SAMPLES_PER_BIN)
            else:
                chosen = pool[rng.integers(0, len(pool), size=cnt)]
                nxt[mask] = b2[chosen]
        return nxt

    b2_sim = _resample_step(b1_sim)
    b3_sim = _resample_step(b2_sim)
    return b1_sim, b2_sim, b3_sim


def ck_test_at_lag(x, L, edges, n_bootstrap=N_BOOTSTRAP_CK, rng=None,
                    n_bins=N_BINS_X, min_samples_per_bin=MIN_SAMPLES_PER_BIN):
    """Chapman-Kolmogorov test at one candidate lag L (in samples).

    Significance (METHODOLOGY_NOTE.md gap (a)): "bootstrap resampling of
    time indices with replacement". IMPLEMENTATION NOTE -- TWO real
    implementation problems were found and fixed during this session's
    mandatory CK-test correctness diagnostic, BEFORE any stochastic
    PRE/POST control was run (full account in ../VALIDATION_NOTE.md,
    "CK-test bootstrap: two implementation problems found and fixed"):

    (1) A first, literal reading -- resample whole (x1,x2,x3) TRIPLES
        with replacement, using ALL n-2L overlapping (stride-1) triples,
        and recompute chi2 on each resample -- was structurally broken:
        naive case-resampling with replacement inflates the effective
        estimation noise well beyond the single non-resampled full-
        sample estimate's noise level, so the bootstrap null was
        SYSTEMATICALLY LARGER than chi2_observed even for a genuinely
        Markov process -- p_ck_test~1.0 for EVERY process tried
        (including deliberately non-Markov ones), i.e. zero power to
        ever reject.

    (2) Fixed with a CONDITIONAL ("Markov") bootstrap
        (`_markov_bootstrap_triples`): each replica resamples TIME
        INDICES with replacement from the pool of observed 1-step
        transitions, CONDITIONED on the current bin at each of the two
        simulated steps, so bootstrap triples are, by construction, an
        exact realization of a chain Markov with the empirical 1-step
        kernel P1. This alone was STILL miscalibrated in the opposite
        direction at LARGER lags: the "observed" statistic, built from
        ALL n-2L overlapping (stride-1) triples, has adjacent triples
        sharing L-1 of their L-sample span -- massive redundancy that
        collapses their EFFECTIVE independent sample size far below the
        nominal n-2L. The conditional bootstrap, by contrast, draws
        max_t EFFECTIVELY INDEPENDENT triples per replica (fresh random
        start bin + independently resampled steps) -- a much LARGER
        effective sample size, hence LOWER sampling noise, than the
        real overlapping-window data. This mismatch showed up
        empirically as chi2_observed growing systematically with lag
        (real windows becoming relatively "noisier" due to redundancy)
        while chi2_bootstrap_mean stayed roughly flat, producing FALSE
        REJECTIONS at large lags even for a genuinely Markov OU process.

    FINAL fix: use NON-OVERLAPPING (stride-L) block starts
    t=0,L,2L,3L,... for BOTH the observed triples and the bootstrap
    (rather than every t=0,1,2,...). This removes the overlap-driven
    redundancy from the observed estimate, matching its effective
    sample size/independence structure to what the conditional
    bootstrap already produces -- verified in ../VALIDATION_NOTE.md to
    correctly pass a genuinely Markov OU process at EVERY grid lag (no
    more large-lag false rejections) while still correctly rejecting a
    genuine non-Markov generator (OU + slow additive colored-noise
    contamination) at short lags. The unavoidable cost: fewer available
    "rows" at large L (n/L blocks instead of n-2L), so the
    insufficient-samples floor triggers earlier at large lags -- an
    honest consequence of using less-redundant data, not silently
    substituted.

    p_ck_test = fraction of bootstrap replicas with chi2_replica >=
    chi2_observed (chi2_observed computed once, on the real,
    non-resampled stride-L block set).
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    L = int(L)
    max_start = n - 1 - 2 * L
    if max_start < 0:
        return {
            "status": "insufficient_samples", "lag_samples": int(L),
            "n_valid_blocks": 0,
        }
    n_blocks = max_start // L + 1
    min_valid = min_samples_per_bin * n_bins
    if n_blocks < min_valid:
        return {
            "status": "insufficient_samples", "lag_samples": int(L),
            "n_valid_blocks": int(n_blocks),
        }

    starts = np.arange(n_blocks) * L
    b1 = bin_index(x[starts], edges, n_bins)
    b2 = bin_index(x[starts + L], edges, n_bins)
    b3 = bin_index(x[starts + 2 * L], edges, n_bins)

    chi2_obs, n_rows_used = _ck_chi2_stat(b1, b2, b3, n_bins, min_samples_per_bin)

    if rng is None:
        rng = np.random.default_rng(SEED)
    chi2_boot = np.empty(n_bootstrap, dtype=float)
    for i in range(n_bootstrap):
        b1_sim, b2_sim, b3_sim = _markov_bootstrap_triples(b1, b2, n_blocks, n_bins, rng)
        chi2_b, _ = _ck_chi2_stat(b1_sim, b2_sim, b3_sim, n_bins, min_samples_per_bin)
        chi2_boot[i] = chi2_b

    p_val = float(np.mean(chi2_boot >= chi2_obs))
    return {
        "status": "ok",
        "lag_samples": int(L),
        "n_valid_blocks": int(n_blocks),
        "n_rows_used": int(n_rows_used),
        "chi2_observed": float(chi2_obs),
        "chi2_bootstrap_mean": float(np.mean(chi2_boot)),
        "chi2_bootstrap_std": float(np.std(chi2_boot)),
        "p_ck_test": p_val,
    }


def find_tau_me(x_pre, dt, edges, n_lag_max=N_LAG_MAX, growth=LAG_GROWTH,
                 max_frac=LAG_MAX_FRAC, n_bootstrap=N_BOOTSTRAP_CK,
                 min_samples_per_bin=MIN_SAMPLES_PER_BIN, alpha=CK_ALPHA,
                 robust_next=CK_ROBUST_NEXT, seed=SEED, n_bins=N_BINS_X):
    """Full CK-test grid scan on the real PRE segment, per
    METHODOLOGY_NOTE.md gap (a). tau_ME = smallest grid lag with
    p_ck_test >= alpha AT that lag AND the following `robust_next` grid
    points. Every grid lag is evaluated (simplicity over premature
    optimization -- the grid is capped at N_LAG_MAX=20 points and
    MAX_N_PER_SEGMENT=50000 already bounds per-lag cost). If no lag
    satisfies the robustness window: status
    "markov_property_not_established", no forced fallback.
    """
    n_pre = len(x_pre)
    lags, max_lag_samples = lag_grid_samples(n_pre, n_lag_max, growth, max_frac)
    rng = np.random.default_rng(seed)

    grid_results = []
    for L in lags:
        res = ck_test_at_lag(x_pre, L, edges, n_bootstrap=n_bootstrap, rng=rng,
                              n_bins=n_bins, min_samples_per_bin=min_samples_per_bin)
        res["delta_tau_time"] = float(L * dt)
        grid_results.append(res)

    tau_me_L = None
    tau_me_idx = None
    for i in range(len(grid_results)):
        if i + robust_next >= len(grid_results):
            break
        window = grid_results[i:i + robust_next + 1]
        if all(r["status"] == "ok" and r["p_ck_test"] >= alpha for r in window):
            tau_me_L = grid_results[i]["lag_samples"]
            tau_me_idx = i
            break

    status = "ok" if tau_me_L is not None else "markov_property_not_established"
    return {
        "status": status,
        "tau_me_samples": tau_me_L,
        "tau_me_time": float(tau_me_L * dt) if tau_me_L is not None else None,
        "tau_me_grid_index": tau_me_idx,
        "lag_grid_samples": lags,
        "max_lag_samples_cap": max_lag_samples,
        "n_grid_points": len(lags),
        "ck_grid_results": grid_results,
    }


# --------------------------------------------------------------------------
# Gap (b): D1(x)/D2(x)/D3(x)/D4(x) at tau_ME, standard Kramers-Moyal
# conditional-moment estimator (Dn = Mn / (n! * tau_ME))
# --------------------------------------------------------------------------

def compute_km_coefficients(x, L_star, dt, edges, n_bins=N_BINS_X,
                             min_samples_per_bin=MIN_SAMPLES_PER_BIN):
    """D1..D4(x) per bin at fixed lag L_star (in samples), using the
    SAME bin edges (from PRE) applied to `x` (PRE, POST, or a
    surrogate). Bins with fewer than `min_samples_per_bin` samples are
    left as NaN (never extrapolated), per METHODOLOGY_NOTE.md gap (b).
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    L_star = int(L_star)
    tau_time = L_star * dt

    D1 = np.full(n_bins, np.nan)
    D2 = np.full(n_bins, np.nan)
    D3 = np.full(n_bins, np.nan)
    D4 = np.full(n_bins, np.nan)
    n_samples_bin = np.zeros(n_bins, dtype=int)

    if n <= L_star:
        return {
            "D1": D1.tolist(), "D2": D2.tolist(), "D3": D3.tolist(), "D4": D4.tolist(),
            "n_samples_per_bin": n_samples_bin.tolist(),
            "tau_used_samples": L_star, "tau_used_time": float(tau_time),
            "status": "insufficient_samples",
        }

    idx = np.arange(n - L_star)
    b1 = bin_index(x[idx], edges, n_bins)
    increments = x[idx + L_star] - x[idx]

    for b in range(n_bins):
        mask = b1 == b
        cnt = int(mask.sum())
        n_samples_bin[b] = cnt
        if cnt < min_samples_per_bin:
            continue
        d = increments[mask]
        M1 = float(np.mean(d))
        M2 = float(np.mean(d ** 2))
        M3 = float(np.mean(d ** 3))
        M4 = float(np.mean(d ** 4))
        D1[b] = M1 / tau_time
        D2[b] = M2 / (2.0 * tau_time)
        D3[b] = M3 / (6.0 * tau_time)
        D4[b] = M4 / (24.0 * tau_time)

    return {
        "D1": D1.tolist(), "D2": D2.tolist(), "D3": D3.tolist(), "D4": D4.tolist(),
        "n_samples_per_bin": n_samples_bin.tolist(),
        "tau_used_samples": L_star, "tau_used_time": float(tau_time),
        "status": "ok",
    }


# --------------------------------------------------------------------------
# Stationary density reconstruction from D1(x)/D2(x)
# --------------------------------------------------------------------------

def reconstruct_stationary_density(D1, D2, bin_centers):
    """p_st(x) ~ (1/D2(x)) * exp(cumulative_trapezoidal_integral(2*D1/D2
    dx)), standard stationary Fokker-Planck solution, normalized to sum
    to 1 over the bins used.

    Undefined-bin handling (explicit design choice, documented here per
    task instructions): bins with undefined D1 or D2 (below
    MIN_SAMPLES_PER_BIN, or D2<=0) are SKIPPED, not interpolated -- the
    cumulative integral and the final probability mass are computed only
    over the (sorted-by-bin-center) subsequence of DEFINED bins. This is
    the more conservative choice: it never fabricates a density value in
    a region with no reliable D1/D2 estimate, at the cost of an
    irregular (non-uniform) integration step size across a gap of
    skipped bins (trapezoidal rule already handles unequal spacing
    correctly, using the actual bin-center distance from the diff() of
    the defined bin centers).
    """
    D1 = np.asarray(D1, dtype=float)
    D2 = np.asarray(D2, dtype=float)
    bc = np.asarray(bin_centers, dtype=float)
    n = len(D1)

    defined = np.isfinite(D1) & np.isfinite(D2) & (D2 > 0) & np.isfinite(bc)
    n_defined = int(defined.sum())
    if n_defined < 3:
        return {
            "status": "insufficient_defined_bins", "n_defined": n_defined,
            "n_undefined_bins": int(n - n_defined), "p_st": [None] * n,
        }

    idx_defined_unsorted = np.where(defined)[0]
    order = np.argsort(bc[idx_defined_unsorted])
    idx_defined = idx_defined_unsorted[order]
    bc_d = bc[idx_defined]
    D1_d = D1[idx_defined]
    D2_d = D2[idx_defined]

    integrand = 2.0 * D1_d / D2_d
    cum = np.zeros(len(bc_d))
    cum[1:] = np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(bc_d))

    log_p_unnorm = cum - np.log(D2_d)
    log_p_unnorm = log_p_unnorm - np.max(log_p_unnorm)  # numerical stability
    p_unnorm = np.exp(log_p_unnorm)
    Z = float(np.sum(p_unnorm))
    p_defined = p_unnorm / Z

    p_full = np.full(n, np.nan)
    for j, i in enumerate(idx_defined):
        p_full[i] = float(p_defined[j])

    return {
        "status": "ok",
        "n_defined": n_defined,
        "n_undefined_bins": int(n - n_defined),
        "p_st": [None if not np.isfinite(v) else float(v) for v in p_full],
        "bin_indices_used_sorted_by_center": idx_defined.tolist(),
    }


def weighted_excess_kurtosis(values, weights):
    """Standard probability-weighted excess-kurtosis formula, treating
    (values, weights) as a discrete distribution over bin centers."""
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    mask = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if int(mask.sum()) < 3:
        return None
    v = values[mask]
    w = weights[mask]
    w = w / w.sum()
    mean = float(np.sum(w * v))
    var = float(np.sum(w * (v - mean) ** 2))
    if var <= 0:
        return None
    m4 = float(np.sum(w * (v - mean) ** 4))
    return float(m4 / (var ** 2) - 3.0)


def compute_PKS(D1, D2, bin_centers):
    """PKS = excess kurtosis of the reconstructed stationary density
    p_st(x), treated as a discrete probability-weighted distribution
    over the (defined) bin centers. Returns (PKS or None, reconstruction
    dict)."""
    recon = reconstruct_stationary_density(D1, D2, bin_centers)
    if recon["status"] != "ok":
        return None, recon
    p_st = np.array([np.nan if v is None else v for v in recon["p_st"]], dtype=float)
    valid = np.isfinite(p_st)
    pks = weighted_excess_kurtosis(np.asarray(bin_centers, dtype=float)[valid], p_st[valid])
    return pks, recon


def compute_beta_D2(D2, bin_centers):
    """beta_D2 = OLS slope of D2(x) vs x over the defined bins (state-
    dependence-of-noise companion channel)."""
    D2 = np.asarray(D2, dtype=float)
    bc = np.asarray(bin_centers, dtype=float)
    mask = np.isfinite(D2) & np.isfinite(bc)
    if int(mask.sum()) < 3:
        return None
    slope, _intercept = np.polyfit(bc[mask], D2[mask], 1)
    return float(slope)


def compute_beta_D2_abs(D2, bin_centers, x_star):
    """beta_D2 (|x-x*| variant) = OLS slope of D2(x) vs |x-x*|, x* a
    FIXED reference point (per METHODOLOGY_NOTE.md gap (b): "ou vs.
    |x-x*|, testado e reportado com o que for mais estável"). Needed
    because a state-dependent diffusion coefficient that is an EVEN/
    symmetric function of x around some center (e.g. D2(x) ~ (1+|x|)^2,
    the textbook multiplicative-noise form) produces a U-shaped D2(x)
    curve whose LINEAR (vs-x) slope is near zero by construction (an
    even function has no net linear trend) even though the state-
    dependence is real and strong -- confirmed empirically during this
    session's synthetic validation (see ../VALIDATION_NOTE.md). `x_star`
    must be a FIXED reference (estimated once from real PRE, reused for
    POST and every surrogate, same convention as tau_ME/bins) for
    Delta_beta_D2 to be well-defined across PRE/POST/surrogates."""
    D2 = np.asarray(D2, dtype=float)
    bc = np.asarray(bin_centers, dtype=float)
    abs_dev = np.abs(bc - float(x_star))
    mask = np.isfinite(D2) & np.isfinite(abs_dev)
    if int(mask.sum()) < 3:
        return None
    slope, _intercept = np.polyfit(abs_dev[mask], D2[mask], 1)
    return float(slope)


def compute_kappa(D1, bin_centers):
    """kappa = -D1'(x*), x* = zero-crossing of D1(x) found by linear
    interpolation between consecutive defined bins with a sign change;
    slope computed by finite difference between the two bracketing
    bins. DIAGNOSTIC ONLY (Ritchie & Sieber 2016 identity with AC1/
    variance, resolved a priori in METHODOLOGY_NOTE.md) -- returned for
    reporting, never used in any significance/decision logic anywhere in
    this module. Returns (kappa or None, x_star or None)."""
    D1 = np.asarray(D1, dtype=float)
    bc = np.asarray(bin_centers, dtype=float)
    mask = np.isfinite(D1) & np.isfinite(bc)
    if int(mask.sum()) < 2:
        return None, None
    order = np.argsort(bc[mask])
    bc_s = bc[mask][order]
    D1_s = D1[mask][order]

    for i in range(len(bc_s) - 1):
        if D1_s[i] == 0.0:
            x_star = float(bc_s[i])
            slope = (D1_s[min(i + 1, len(bc_s) - 1)] - D1_s[max(i - 1, 0)]) / \
                    (bc_s[min(i + 1, len(bc_s) - 1)] - bc_s[max(i - 1, 0)])
            return float(-slope), x_star
        if D1_s[i] * D1_s[i + 1] < 0.0:
            frac = D1_s[i] / (D1_s[i] - D1_s[i + 1])
            x_star = float(bc_s[i] + frac * (bc_s[i + 1] - bc_s[i]))
            slope = (D1_s[i + 1] - D1_s[i]) / (bc_s[i + 1] - bc_s[i])
            return float(-slope), x_star
    return None, None


def pawula_ratio(D2, D4):
    """D4/D2^2 per bin -- Pawula (1967) truncation diagnostic, reported
    honestly but never used as an accept/reject gate (METHODOLOGY_NOTE.md
    gap (a))."""
    D2 = np.asarray(D2, dtype=float)
    D4 = np.asarray(D4, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = D4 / (D2 ** 2)
    return [None if not np.isfinite(v) else float(v) for v in ratio]


def compute_segment_features(x, L_star, dt, edges, bin_centers, n_bins=N_BINS_X,
                               min_samples_per_bin=MIN_SAMPLES_PER_BIN, x_star_ref=None):
    """Full per-segment feature bundle at the FIXED (tau_ME, bins):
    D1..D4, reconstructed p_st, PKS, beta_D2 (both the vs-x and vs-
    |x-x_star_ref| variants -- METHODOLOGY_NOTE.md gap (b) explicitly
    authorizes trying both and reporting whichever is more stable),
    kappa (diagnostic), Pawula ratio. `x_star_ref`, when given, is a
    FIXED reference point (estimated once from real PRE, see
    run_km_analysis) used for the |x-x_star_ref| variant -- without it,
    only the vs-x variant is computed. Used identically for real PRE,
    real POST, and every IAAFT surrogate of either."""
    km = compute_km_coefficients(x, L_star, dt, edges, n_bins, min_samples_per_bin)
    if km["status"] != "ok":
        return {
            "km": km, "stationary_density": {"status": "insufficient_samples"},
            "PKS": None, "beta_D2": None, "beta_D2_abs": None,
            "kappa": None, "kappa_x_star": None,
            "kappa_diagnostic_only": True, "pawula_ratio_per_bin": [None] * n_bins,
        }
    pks, recon = compute_PKS(km["D1"], km["D2"], bin_centers)
    beta_d2 = compute_beta_D2(km["D2"], bin_centers)
    beta_d2_abs = compute_beta_D2_abs(km["D2"], bin_centers, x_star_ref) if x_star_ref is not None else None
    kappa, x_star = compute_kappa(km["D1"], bin_centers)
    pawula = pawula_ratio(km["D2"], km["D4"])
    return {
        "km": km,
        "stationary_density": recon,
        "PKS": pks,
        "beta_D2": beta_d2,
        "beta_D2_abs": beta_d2_abs,
        "kappa": kappa,
        "kappa_x_star": x_star,
        "kappa_diagnostic_only": True,
        "pawula_ratio_per_bin": pawula,
    }


# --------------------------------------------------------------------------
# Gap (e): IAAFT surrogates (Schreiber & Schmitz 1996)
# --------------------------------------------------------------------------

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate
    (Schreiber & Schmitz 1996). Preserves the linear power spectrum
    (FFT amplitude) and exact empirical marginal (histogram) of `x`;
    destroys nonlinear/temporal structure beyond a linear Gaussian
    process with the same spectrum+marginal. Independent implementation
    for this test line (same standard algorithm as
    mse_common.py/rqa_common.py/pe_common.py in this lab)."""
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
# same machinery/API style already used elsewhere in this lab -- NOT part
# of the default pipeline, invoked only if synthetic validation shows low
# IAAFT power for a channel.
# --------------------------------------------------------------------------

def moving_block_bootstrap_resample(x, L, rng):
    """One moving-block-bootstrap resample of `x` (Kunsch 1989)."""
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


def run_block_bootstrap_test(pre_segment, post_segment, L_star, dt, edges, bin_centers,
                              block_length=None, n_bootstrap=N_SURROGATES, seed=SEED,
                              n_bins=N_BINS_X, min_samples_per_bin=MIN_SAMPLES_PER_BIN):
    """Moving-block bootstrap (Kunsch 1989) significance test for
    Delta_PKS / Delta_beta_D2, using the SAME fixed (tau_ME, bins) as the
    real analysis -- pre-authorized fallback (METHODOLOGY_NOTE.md gap
    (e)/pe_common.py precedent), NOT invoked unless synthetic validation
    shows low IAAFT power for a channel. Block length defaults to
    max(2*tau_ME_samples, 10)."""
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    if block_length is None:
        block_length = max(2 * int(L_star), 10)

    real_pre = compute_segment_features(pre, L_star, dt, edges, bin_centers, n_bins, min_samples_per_bin)
    real_post = compute_segment_features(post, L_star, dt, edges, bin_centers, n_bins, min_samples_per_bin)
    delta_pks_real = (real_post["PKS"] - real_pre["PKS"]) if (real_pre["PKS"] is not None and real_post["PKS"] is not None) else None
    delta_beta_real = (real_post["beta_D2"] - real_pre["beta_D2"]) if (real_pre["beta_D2"] is not None and real_post["beta_D2"] is not None) else None

    rng = np.random.default_rng(seed)
    pks_boot, beta_boot = [], []
    n_undef_pks = n_undef_beta = 0
    for _ in range(n_bootstrap):
        boot_pre = moving_block_bootstrap_resample(pre, block_length, rng)
        boot_post = moving_block_bootstrap_resample(post, block_length, rng)
        f_pre = compute_segment_features(boot_pre, L_star, dt, edges, bin_centers, n_bins, min_samples_per_bin)
        f_post = compute_segment_features(boot_post, L_star, dt, edges, bin_centers, n_bins, min_samples_per_bin)
        if f_pre["PKS"] is not None and f_post["PKS"] is not None:
            pks_boot.append(f_post["PKS"] - f_pre["PKS"])
        else:
            n_undef_pks += 1
        if f_pre["beta_D2"] is not None and f_post["beta_D2"] is not None:
            beta_boot.append(f_post["beta_D2"] - f_pre["beta_D2"])
        else:
            n_undef_beta += 1

    pks_boot = np.array(pks_boot, dtype=float)
    beta_boot = np.array(beta_boot, dtype=float)

    def _two_tailed_p(real_val, boot_vals):
        if real_val is None or len(boot_vals) == 0:
            return None
        return float(np.mean(np.abs(boot_vals) >= abs(real_val)))

    return {
        "block_length": int(block_length),
        "n_bootstrap": int(n_bootstrap),
        "seed": int(seed),
        "delta_PKS_real": delta_pks_real,
        "delta_beta_D2_real": delta_beta_real,
        "bootstrap_delta_PKS_mean": float(np.mean(pks_boot)) if len(pks_boot) else None,
        "bootstrap_delta_PKS_std": float(np.std(pks_boot)) if len(pks_boot) else None,
        "bootstrap_delta_PKS_p": _two_tailed_p(delta_pks_real, pks_boot),
        "bootstrap_delta_PKS_n_valid": int(len(pks_boot)),
        "bootstrap_delta_PKS_n_undefined": int(n_undef_pks),
        "bootstrap_delta_beta_D2_mean": float(np.mean(beta_boot)) if len(beta_boot) else None,
        "bootstrap_delta_beta_D2_std": float(np.std(beta_boot)) if len(beta_boot) else None,
        "bootstrap_delta_beta_D2_p": _two_tailed_p(delta_beta_real, beta_boot),
        "bootstrap_delta_beta_D2_n_valid": int(len(beta_boot)),
        "bootstrap_delta_beta_D2_n_undefined": int(n_undef_beta),
    }


# --------------------------------------------------------------------------
# Full PRE/POST transition test pipeline (public entry point)
# --------------------------------------------------------------------------

def run_km_analysis(pre_series, post_series, dt, seed=SEED, n_mc=None,
                     max_n=MAX_N_PER_SEGMENT, n_bins=N_BINS_X,
                     n_lag_max=N_LAG_MAX, growth=LAG_GROWTH, max_frac=LAG_MAX_FRAC,
                     n_bootstrap_ck=N_BOOTSTRAP_CK, min_samples_per_bin=MIN_SAMPLES_PER_BIN,
                     n_surrogates=N_SURROGATES, n_iaaft_iter=N_IAAFT_ITER):
    """Run the full Markov-Einstein/Chapman-Kolmogorov + Kramers-Moyal
    transition test between a PRE and a POST segment, per
    METHODOLOGY_NOTE.md gaps (a)-(e). Single entry point a real-data
    script must call WITHOUT modification.

    `dt` is the native sampling interval of BOTH segments (assumed
    equal for PRE/POST, standard assumption for a single continuous
    recording split at one transition point).

    `n_mc` overrides `n_surrogates` when given (validation-script
    convenience for smaller/faster runs); when None, `n_surrogates` is
    used unchanged.

    Returns a dict. When status != "ok" (either "markov_property_not_
    established" from the CK-test grid, or otherwise), no D1..D4/PKS/
    beta_D2/IAAFT computation is attempted -- the CK-test grid
    diagnostics are still returned in full.

    When status == "ok": tau_me_result (full CK-test grid), bin_edges,
    bin_centers, real_pre/real_post (D1..D4, stationary density, PKS,
    beta_D2, kappa+x_star [diagnostic_only], Pawula ratio per bin),
    PKS_pre/post/delta, beta_D2_pre/post/delta, kappa_pre/post/delta
    (diagnostic_only=True, never used below this point for any p-value),
    p_PKS/p_beta_D2 (two-tailed IAAFT surrogate p-values), surrogate
    null-distribution summaries/arrays, subsampling diagnostics, config
    (exact fixed parameters, provenance).
    """
    n_surr = n_mc if n_mc is not None else n_surrogates

    pre_raw = np.asarray(pre_series, dtype=float)
    post_raw = np.asarray(post_series, dtype=float)

    # Gap (d): subsample ONCE, at the very top, before ANYTHING else --
    # the CK-test grid+bootstrap on PRE, D1..D4 estimation, and IAAFT
    # surrogate generation for BOTH PRE and POST all operate on the
    # subsampled series only. See module docstring for the explicit
    # lesson learned from permutation_entropy/analysis/pe_common.py's
    # real subsampling-ordering bug (found at the real-data step there).
    pre, pre_sub_info = subsample_segment(pre_raw, max_n)
    post, post_sub_info = subsample_segment(post_raw, max_n)

    edges = compute_quantile_bins(pre, n_bins)
    bin_centers = bin_centers_from_edges(edges, pre, n_bins)

    tau_me_result = find_tau_me(pre, dt, edges, n_lag_max=n_lag_max, growth=growth,
                                 max_frac=max_frac, n_bootstrap=n_bootstrap_ck,
                                 min_samples_per_bin=min_samples_per_bin, alpha=CK_ALPHA,
                                 robust_next=CK_ROBUST_NEXT, seed=seed, n_bins=n_bins)

    config = {
        "dt": dt, "n_bins_x": n_bins, "n_lag_max": n_lag_max, "lag_growth": growth,
        "lag_max_frac": max_frac, "n_bootstrap_ck": n_bootstrap_ck,
        "min_samples_per_bin": min_samples_per_bin, "ck_alpha": CK_ALPHA,
        "ck_robust_next": CK_ROBUST_NEXT, "max_n_per_segment": max_n,
        "n_surrogates": n_surr, "n_iaaft_iter": n_iaaft_iter, "seed": seed,
        "pre_subsample_info": pre_sub_info, "post_subsample_info": post_sub_info,
    }

    if tau_me_result["status"] != "ok":
        return {
            "status": "markov_property_not_established",
            "tau_me_result": tau_me_result,
            "bin_edges": edges.tolist(),
            "bin_centers": bin_centers.tolist(),
            "config": config,
        }

    L_star = tau_me_result["tau_me_samples"]

    # x_star_ref (for the |x-x*| beta_D2 variant, METHODOLOGY_NOTE.md gap
    # (b)) is estimated ONCE from real PRE's own D1 zero-crossing, then
    # reused unchanged for POST and every surrogate of either -- same
    # "estimate from PRE, reapply everywhere" convention already used for
    # tau_ME and the bins. Fallback to the median bin center if PRE's D1
    # has no clean sign-crossing (kappa/x_star undefined).
    km_pre_probe = compute_km_coefficients(pre, L_star, dt, edges, n_bins, min_samples_per_bin)
    _, x_star_probe = compute_kappa(km_pre_probe.get("D1"), bin_centers) if km_pre_probe["status"] == "ok" else (None, None)
    x_star_ref = x_star_probe if x_star_probe is not None else float(np.median(bin_centers))

    real_pre_feat = compute_segment_features(pre, L_star, dt, edges, bin_centers, n_bins, min_samples_per_bin, x_star_ref=x_star_ref)
    real_post_feat = compute_segment_features(post, L_star, dt, edges, bin_centers, n_bins, min_samples_per_bin, x_star_ref=x_star_ref)

    def _delta(a, b):
        return None if (a is None or b is None) else (a - b)

    delta_PKS = _delta(real_post_feat["PKS"], real_pre_feat["PKS"])
    delta_beta_D2 = _delta(real_post_feat["beta_D2"], real_pre_feat["beta_D2"])
    delta_beta_D2_abs = _delta(real_post_feat["beta_D2_abs"], real_pre_feat["beta_D2_abs"])
    delta_kappa = _delta(real_post_feat["kappa"], real_pre_feat["kappa"])  # diagnostic only

    rng = np.random.default_rng(seed)
    surr_delta_PKS, surr_delta_beta_D2, surr_delta_beta_D2_abs = [], [], []
    n_undef_pks = n_undef_beta = n_undef_beta_abs = 0

    for _ in range(n_surr):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iaaft_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iaaft_iter, rng=rng)
        f_pre = compute_segment_features(surr_pre, L_star, dt, edges, bin_centers, n_bins, min_samples_per_bin, x_star_ref=x_star_ref)
        f_post = compute_segment_features(surr_post, L_star, dt, edges, bin_centers, n_bins, min_samples_per_bin, x_star_ref=x_star_ref)

        d_pks = _delta(f_post["PKS"], f_pre["PKS"])
        if d_pks is None:
            n_undef_pks += 1
        else:
            surr_delta_PKS.append(d_pks)

        d_beta = _delta(f_post["beta_D2"], f_pre["beta_D2"])
        if d_beta is None:
            n_undef_beta += 1
        else:
            surr_delta_beta_D2.append(d_beta)

        d_beta_abs = _delta(f_post["beta_D2_abs"], f_pre["beta_D2_abs"])
        if d_beta_abs is None:
            n_undef_beta_abs += 1
        else:
            surr_delta_beta_D2_abs.append(d_beta_abs)

    surr_delta_PKS = np.array(surr_delta_PKS, dtype=float)
    surr_delta_beta_D2 = np.array(surr_delta_beta_D2, dtype=float)
    surr_delta_beta_D2_abs = np.array(surr_delta_beta_D2_abs, dtype=float)

    p_PKS = None
    if delta_PKS is not None and len(surr_delta_PKS) > 0:
        p_PKS = float(np.mean(np.abs(surr_delta_PKS) >= abs(delta_PKS)))
    p_beta_D2 = None
    if delta_beta_D2 is not None and len(surr_delta_beta_D2) > 0:
        p_beta_D2 = float(np.mean(np.abs(surr_delta_beta_D2) >= abs(delta_beta_D2)))
    p_beta_D2_abs = None
    if delta_beta_D2_abs is not None and len(surr_delta_beta_D2_abs) > 0:
        p_beta_D2_abs = float(np.mean(np.abs(surr_delta_beta_D2_abs) >= abs(delta_beta_D2_abs)))

    return {
        "status": "ok",
        "tau_me_result": tau_me_result,
        "bin_edges": edges.tolist(),
        "bin_centers": bin_centers.tolist(),
        "x_star_ref": x_star_ref,
        "real_pre": real_pre_feat,
        "real_post": real_post_feat,
        "PKS_pre": real_pre_feat["PKS"], "PKS_post": real_post_feat["PKS"], "delta_PKS": delta_PKS,
        "beta_D2_pre": real_pre_feat["beta_D2"], "beta_D2_post": real_post_feat["beta_D2"],
        "delta_beta_D2": delta_beta_D2,
        "beta_D2_abs_pre": real_pre_feat["beta_D2_abs"], "beta_D2_abs_post": real_post_feat["beta_D2_abs"],
        "delta_beta_D2_abs": delta_beta_D2_abs,
        "kappa_pre": real_pre_feat["kappa"], "kappa_post": real_post_feat["kappa"],
        "delta_kappa": delta_kappa, "kappa_diagnostic_only": True,
        "p_PKS": p_PKS, "p_beta_D2": p_beta_D2, "p_beta_D2_abs": p_beta_D2_abs,
        "surrogate_PKS_deltas": surr_delta_PKS.tolist(),
        "surrogate_beta_D2_deltas": surr_delta_beta_D2.tolist(),
        "surrogate_beta_D2_abs_deltas": surr_delta_beta_D2_abs.tolist(),
        "surrogate_PKS_mean": float(np.mean(surr_delta_PKS)) if len(surr_delta_PKS) else None,
        "surrogate_PKS_std": float(np.std(surr_delta_PKS)) if len(surr_delta_PKS) else None,
        "surrogate_PKS_n_valid": int(len(surr_delta_PKS)),
        "surrogate_PKS_n_undefined": int(n_undef_pks),
        "surrogate_beta_D2_mean": float(np.mean(surr_delta_beta_D2)) if len(surr_delta_beta_D2) else None,
        "surrogate_beta_D2_std": float(np.std(surr_delta_beta_D2)) if len(surr_delta_beta_D2) else None,
        "surrogate_beta_D2_n_valid": int(len(surr_delta_beta_D2)),
        "surrogate_beta_D2_n_undefined": int(n_undef_beta),
        "surrogate_beta_D2_abs_mean": float(np.mean(surr_delta_beta_D2_abs)) if len(surr_delta_beta_D2_abs) else None,
        "surrogate_beta_D2_abs_std": float(np.std(surr_delta_beta_D2_abs)) if len(surr_delta_beta_D2_abs) else None,
        "surrogate_beta_D2_abs_n_valid": int(len(surr_delta_beta_D2_abs)),
        "surrogate_beta_D2_abs_n_undefined": int(n_undef_beta_abs),
        "config": config,
    }
