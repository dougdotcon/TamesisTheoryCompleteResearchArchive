"""
Canonical SOC-avalanche (branching/power-law) analysis pipeline for
DISC-TRI-RG-001, candidate `soc-avalanches`.

Fixed BEFORE running on any real domain (Ridgecrest 2019 seismicity, GOES
solar-flare X-ray flux) -- see ../METHODOLOGY_NOTE.md for the full
rationale. This is a NEW, self-contained implementation specific to this
test line: it does not import from, and is not derived from,
`critical_slowing_down/analysis/csd_common.py`,
`wavelet_multiresolution/analysis/wtmm_common.py`, or
`dfa_multiscale_entropy/analysis/dfa_common.py`, even though it follows the
same module discipline used across this lab: fixed constants at module
level, a single `run_soc_pipeline()` entry point any future agent can
import and call unmodified on real data, no per-domain tuning.

Method summary (METHODOLOGY_NOTE.md gaps a/b/c):

  (a) Binning & avalanche extraction (Beggs & Plenz 2003; Priesemann et al.
      2014): `lambda` = mean inter-event interval (IEI) of the COMBINED
      PRE+POST event stream, computed ONCE and reused unmodified for both
      segments' binning (never recalculated per-segment -- this is the
      deliberate anti-STAI-style bias-avoidance rule spelled out in the
      methodology note). Non-overlapping bins of width `lambda`; avalanche
      = maximal run of consecutive non-empty bins, delimited by an empty
      bin or the segment edge. `s` = sum of event counts in the avalanche's
      bins (the PRIMARY channel is event COUNT, not energy/magnitude
      weighting). `T` = number of bins spanned.

  (b) `tau`: MLE power-law fit (Clauset, Shalizi & Newman 2009, SIAM Review
      51:661) over the avalanche-size distribution. `s` is DISCRETE
      (integer event counts), so this module implements the DISCRETE
      power-law MLE (Clauset et al. section 3.2), not the continuous
      closed-form -- treating integer count data as if drawn from a
      continuous Pareto (as the popular closed-form `1 + n/sum(log(x/xmin))`
      formula assumes) systematically biases `tau` low for small-`s`-heavy
      count distributions, which is exactly the case here. No `powerlaw`
      package is available in this environment (verified: `import powerlaw`
      raises `ModuleNotFoundError`), so the discrete MLE is implemented
      directly against `scipy.special.zeta` (Hurwitz zeta), which gives an
      EXACT (not approximate) discrete power-law MLE via numerical
      maximization of the exact discrete log-likelihood -- strictly more
      faithful to Clauset et al. than the approximate closed-form the paper
      itself offers as a shortcut. `s_min` is chosen by minimizing the
      Kolmogorov-Smirnov statistic between the fitted discrete power law
      and the empirical CCDF, scanning candidate `s_min` over the observed
      unique values of `s` (never a fixed hand-picked threshold).
      Uncertainty on `tau` is a non-parametric bootstrap (resampling with
      replacement from the observed avalanches >= s_min, refit per
      resample) -- see N_MLE_BOOTSTRAP below for the exact count and the
      documented performance trade-off.

  (c) `sigma`: branching ratio, mean of n_{t+1}/n_t over consecutive-bin
      pairs strictly WITHIN avalanches (Beggs & Plenz convention).

  (d) Null model: N_SURROGATES=1000 independent homogeneous-Poisson
      surrogates per segment (same mean rate `mu`, same time span as the
      real segment), re-binned with the SAME fixed `lambda` from the real
      combined data (never recalculated per surrogate), refit with the
      same MLE/xmin-search pipeline. Two-tailed test: `p = fraction of
      surrogates with |Delta_x_surrogate| >= |Delta_x_real|`, seed=12345.

  (e) PRIMARY tau significance test -- paired bootstrap of Delta_tau
      (METHODOLOGY_NOTE.md "Adendo ao Gap (c)", added AFTER synthetic
      validation of (d) above, BEFORE any real data was touched): the
      Poisson-surrogate test in (d) loses power when PRE and POST have very
      different mean event rates (a rate-mismatched synthetic transition
      control with a real tau difference of 1.5 vs 3.0 gave p_tau=0.285
      under (d) alone -- Poisson surrogates drawn at very different rates
      have very different tau variance under the same shared lambda,
      inflating the combined null's dispersion). Fix: reuse the tau MLE
      uncertainty bootstrap distribution ALREADY computed per segment in
      (b) above (`bootstrap_tau_uncertainty`, independent non-parametric
      resampling of that segment's own observed avalanches, no new
      resampling) for PRE and POST independently, pair the i-th PRE draw
      with the i-th POST draw (standard two-sample paired-bootstrap
      convention, same one used in the dfa-multiscale-entropy addendum) to
      form `Delta_tau_boot_i = tau_boot_POST_i - tau_boot_PRE_i`, and report
      the 95% percentile CI plus `p_bootstrap_tau = 2*min(frac<=0,
      frac>=0)`. This is now the PRIMARY significance test for tau; the
      Poisson surrogate in (d) continues to be computed and reported as a
      SECONDARY/complementary check (it still answers a distinct, valid
      question -- "is there structure beyond pure rate-matched randomness?"
      -- and remains the only implemented significance test for sigma).

Documented performance optimizations (explicitly permitted by the
methodology note when N_SURROGATES=1000 with a full MLE refit per
surrogate would otherwise be too slow -- "otimize com numpy vetorizado ou
reduza o bootstrap de incerteza do MLE", NOT allowed to reduce
N_SURROGATES itself):
  1. The `s_min` candidate search is capped (`XMIN_CANDIDATE_CAP` for real
     segments, a smaller `SURROGATE_XMIN_CANDIDATE_CAP` for the 2000
     per-run surrogate refits) -- if more unique `s` values exist than the
     cap, candidates are subsampled evenly across the sorted unique values,
     preserving representative coverage of the search space rather than
     exhaustively testing every unique value. This is the numpy/algorithmic
     optimization the note explicitly anticipates.
  2. The non-parametric MLE-uncertainty bootstrap (`N_MLE_BOOTSTRAP`) is
     only run for the two REAL segments (PRE, POST), never per-surrogate --
     running it per surrogate would multiply the cost by N_MLE_BOOTSTRAP
     for no methodological gain, since the surrogate loop IS itself the
     resampling-based significance test; only a single point estimate of
     `tau_surrogate`/`sigma_surrogate` is needed per surrogate draw.
  3. KS-statistic computation for a given `(alpha, xmin)` candidate uses
     `np.searchsorted` against the sorted tail rather than an O(n^2)
     pairwise comparison.

Any agent applying this pipeline to real data MUST import and call
`run_soc_pipeline` (or the lower-level helpers) rather than reimplementing
any of this, matching the "same formula, no per-domain reformulation"
discipline already used for `csd_common.py`, `wtmm_common.py`, and
`dfa_common.py` in this lab.
"""
import numpy as np
from scipy.special import zeta as _hurwitz_zeta
from scipy.optimize import minimize_scalar

# --------------------------------------------------------------------------
# Fixed constants (METHODOLOGY_NOTE.md gaps a/b/c -- identical for every
# domain this pipeline is ever applied to; no per-domain tuning)
# --------------------------------------------------------------------------
N_SURROGATES = 1000            # homogeneous-Poisson surrogates per segment (methodology floor)
SEED = 12345
N_MLE_BOOTSTRAP = 500          # non-parametric MLE uncertainty resamples for REAL PRE/POST only
                                # (methodology floor is >=200; 500 chosen for a materially tighter
                                # CI than the floor while remaining fast -- see perf note above,
                                # this bootstrap is NOT run per-surrogate)
MIN_TAIL_N = 10                # minimum avalanches required at/above a candidate s_min to accept
                                # it as a candidate (Clauset et al. use a >=50 rule of thumb for
                                # large empirical corpora; this pipeline is expected to be applied
                                # to catalogs from hundreds to low-thousands of avalanches, so a
                                # lower floor is used -- documented deviation from the >=50
                                # convention, chosen so smaller real catalogs are not silently
                                # unable to produce any fit at all)
ALPHA_BOUNDS = (1.01, 8.0)     # bounded search range for the power-law exponent
XMIN_CANDIDATE_CAP = 150       # max s_min candidates tested for the two REAL segments
SURROGATE_XMIN_CANDIDATE_CAP = 40  # smaller cap used inside the 2*N_SURROGATES refit loop
                                    # (documented perf optimization, see module docstring)


# --------------------------------------------------------------------------
# Gap (a): lambda, binning, avalanche extraction
# --------------------------------------------------------------------------

def compute_lambda(combined_events):
    """Mean inter-event interval (IEI) of the COMBINED PRE+POST event stream.

    This is computed ONCE from the concatenated, sorted combined stream and
    reused unmodified for binning PRE and POST separately (see module
    docstring / METHODOLOGY_NOTE.md gap (a) -- prevents a pure rate change
    between PRE and POST from mechanically inducing or erasing a structural
    difference in tau/sigma).
    """
    combined = np.sort(np.asarray(combined_events, dtype=float))
    if len(combined) < 2:
        raise ValueError("Need >=2 combined events to compute a mean IEI.")
    iei = np.diff(combined)
    return float(np.mean(iei))


def bin_counts(events, lam, t_min=None, t_max=None):
    """Bin `events` into non-overlapping windows of width `lam` covering
    [t_min, t_max] (defaults to the segment's own observed span).

    Returns (counts, edges).
    """
    events = np.sort(np.asarray(events, dtype=float))
    if t_min is None:
        t_min = float(events[0]) if len(events) else 0.0
    if t_max is None:
        t_max = float(events[-1]) if len(events) else t_min
    span = t_max - t_min
    n_bins = max(1, int(np.ceil(span / lam))) if span > 0 else 1
    edges = t_min + lam * np.arange(n_bins + 1)
    if edges[-1] <= t_max:
        edges[-1] = t_max + max(1e-9, 1e-9 * abs(t_max))
    counts, _ = np.histogram(events, bins=edges)
    return counts, edges


def extract_avalanches(counts):
    """Extract avalanches (maximal runs of consecutive non-empty bins) from
    a bin-count array, vectorized run-detection (Beggs & Plenz 2003).

    Returns a list of dicts: {s, T, start_bin, bin_counts}.
    """
    counts = np.asarray(counts, dtype=int)
    nonzero = counts > 0
    if not nonzero.any():
        return []
    padded = np.concatenate(([False], nonzero, [False]))
    d = np.diff(padded.astype(np.int8))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]  # exclusive
    avalanches = []
    for st, en in zip(starts, ends):
        seg = counts[st:en]
        avalanches.append({
            "s": int(seg.sum()),
            "T": int(en - st),
            "start_bin": int(st),
            "bin_counts": seg.tolist(),
        })
    return avalanches


# --------------------------------------------------------------------------
# Gap (c) secondary channel: branching ratio sigma (Beggs & Plenz convention)
# --------------------------------------------------------------------------

def branching_ratio_sigma(avalanches):
    """sigma = <n_{t+1}> / <n_t>: the RATIO OF THE MEANS of n_{t+1} and n_t
    pooled over all consecutive-bin pairs strictly WITHIN avalanches
    (Beggs & Plenz 2003 convention; border-empty bins excluded by
    construction, since an avalanche's bin_counts never contains a zero by
    definition). This is deliberately NOT the mean of the per-pair ratios
    n_{t+1}/n_t -- that alternative estimator is badly biased upward by
    small-n_t pairs (e.g. a lone 1->3 transition contributes a ratio of 3.0
    to the average regardless of how rare/noisy it is), confirmed
    empirically during module validation (a branching_ratio=1 synthetic
    generative process gave a mean-of-ratios sigma of ~7 -- clearly a
    small-sample-ratio pathology, not a real branching-ratio estimate).
    Ratio-of-means is both the literal reading of the methodology note's
    `<n_{t+1}> / <n_t>` notation (each `< >` is a separate pooled average)
    and the numerically stable estimator; it also reproduces the expected
    downward bias direction from coarse temporal binning documented in the
    subsampling literature (Priesemann et al. 2009 PRL, 2014). Returns None
    if no avalanche has >=2 bins (no valid consecutive pair exists)."""
    n_t, n_t1 = [], []
    for av in avalanches:
        c = av["bin_counts"]
        if len(c) >= 2:
            arr = np.asarray(c, dtype=float)
            n_t.extend(arr[:-1].tolist())
            n_t1.extend(arr[1:].tolist())
    if not n_t:
        return None
    mean_nt = float(np.mean(n_t))
    if mean_nt == 0:
        return None
    return float(np.mean(n_t1)) / mean_nt


def count_sigma_pairs(avalanches):
    """Number of consecutive-bin (n_t, n_{t+1}) pairs feeding
    branching_ratio_sigma -- a diagnostic, since a segment dominated by
    single-bin avalanches (common when a shared, combined-stream-derived
    lambda is much better matched to a co-analyzed higher-activity segment
    than to a lower-activity one) can leave sigma estimated from very few
    pairs and hence highly noisy. Always report this alongside sigma."""
    n = 0
    for av in avalanches:
        T = av["T"]
        if T >= 2:
            n += T - 1
    return int(n)


# --------------------------------------------------------------------------
# Gap (b): discrete power-law MLE (Clauset, Shalizi & Newman 2009 sec 3.2)
# --------------------------------------------------------------------------

def _negloglik_discrete(alpha, xmin, sum_log_x, n):
    z = _hurwitz_zeta(alpha, xmin)
    if not np.isfinite(z) or z <= 0:
        return np.inf
    return n * np.log(z) + alpha * sum_log_x


def fit_alpha_discrete_mle(x_tail, xmin, bounds=ALPHA_BOUNDS):
    """Exact discrete power-law MLE of alpha (=tau) given fixed xmin, by
    bounded numerical maximization of the discrete log-likelihood
    (Clauset et al. 2009 eq. 3.5) using the Hurwitz zeta normalization
    constant. Discrete negative log-likelihood is convex in alpha for fixed
    xmin, so Brent's method (scipy `minimize_scalar(method='bounded')`)
    converges reliably."""
    x_tail = np.asarray(x_tail, dtype=float)
    n = len(x_tail)
    sum_log_x = float(np.sum(np.log(x_tail)))
    res = minimize_scalar(_negloglik_discrete, bounds=bounds, method="bounded",
                           args=(xmin, sum_log_x, n))
    return float(res.x)


def ks_discrete(x_tail, alpha, xmin):
    """KS statistic between the fitted discrete power law CCDF and the
    empirical CCDF, evaluated at each unique observed value >= xmin."""
    x_tail = np.sort(np.asarray(x_tail, dtype=float))
    n = len(x_tail)
    uniq = np.unique(x_tail)
    counts_ge = n - np.searchsorted(x_tail, uniq, side="left")
    ccdf_emp = counts_ge / n
    z_xmin = _hurwitz_zeta(alpha, xmin)
    ccdf_theory = _hurwitz_zeta(alpha, uniq) / z_xmin
    return float(np.max(np.abs(ccdf_emp - ccdf_theory)))


def fit_powerlaw_clauset(s_values, min_tail_n=MIN_TAIL_N, candidate_cap=XMIN_CANDIDATE_CAP,
                          alpha_bounds=ALPHA_BOUNDS):
    """Full Clauset/Shalizi/Newman (2009) discrete power-law fit: scan
    candidate s_min over unique observed avalanche sizes, MLE-fit alpha at
    each, pick the (alpha, s_min) pair minimizing the KS statistic.

    Returns a dict with tau (=alpha), xmin, D (KS stat), n_tail, n_total,
    n_candidates_tested, reason ('ok' or a failure reason with tau=None).
    """
    s = np.asarray(s_values, dtype=float)
    s = s[s > 0]
    n_total = int(len(s))
    if n_total < min_tail_n:
        return {"tau": None, "xmin": None, "D": None, "n_tail": 0,
                "n_total": n_total, "n_candidates_tested": 0,
                "reason": "insufficient_data"}

    s_sorted = np.sort(s)
    uniq_vals = np.unique(s_sorted)
    tail_counts = len(s_sorted) - np.searchsorted(s_sorted, uniq_vals, side="left")
    candidates = uniq_vals[tail_counts >= min_tail_n]
    # Exclude any candidate xmin whose tail is degenerate (a single distinct
    # value repeated -- e.g. a pile-up artifact at a hard truncation cap in
    # simulated data, or a clipping/saturation artifact in real instrument
    # data). A one-point tail has no slope information: any sufficiently
    # steep discrete power law concentrates ~all mass at xmin and gives a
    # spuriously "perfect" KS=0 fit with alpha pinned at the search bound,
    # which would otherwise always win the KS-minimization search and mask
    # every other candidate. Discovered empirically during synthetic
    # validation of this module (a branching-process generator's hard
    # max_cluster_size cap produced exactly this artifact).
    if len(candidates) > 0:
        valid_mask = np.array([
            len(np.unique(s[s >= xmin])) >= 2 for xmin in candidates
        ])
        candidates = candidates[valid_mask]
    if len(candidates) == 0:
        return {"tau": None, "xmin": None, "D": None, "n_tail": 0,
                "n_total": n_total, "n_candidates_tested": 0,
                "reason": "no_valid_xmin_candidate"}

    if len(candidates) > candidate_cap:
        idx = np.unique(np.linspace(0, len(candidates) - 1, candidate_cap).astype(int))
        candidates = candidates[idx]

    best = None
    for xmin in candidates:
        tail = s[s >= xmin]
        alpha = fit_alpha_discrete_mle(tail, xmin, bounds=alpha_bounds)
        D = ks_discrete(tail, alpha, xmin)
        if best is None or D < best["D"]:
            best = {"tau": alpha, "xmin": float(xmin), "D": D, "n_tail": int(len(tail))}

    best["n_total"] = n_total
    best["n_candidates_tested"] = int(len(candidates))
    best["reason"] = "ok"
    return best


def bootstrap_tau_uncertainty(s_values, xmin, n_boot=N_MLE_BOOTSTRAP, rng=None,
                               alpha_bounds=ALPHA_BOUNDS):
    """Non-parametric bootstrap uncertainty on tau: resample the observed
    avalanches >= xmin WITH REPLACEMENT (same size as the observed tail),
    refit alpha via MLE at the SAME fixed xmin per resample (Clauset et al.
    2009 sec 4).

    `tau_boot_values` (the raw per-resample alpha draws, in draw order) is
    included in the returned dict specifically so it can be reused, without
    any new resampling, by `paired_bootstrap_tau_test` below (gap (c)
    addendum) -- this is the single bootstrap distribution the pipeline
    already pays for; the paired test just re-reads it."""
    if rng is None:
        rng = np.random.default_rng()
    s = np.asarray(s_values, dtype=float)
    tail = s[s >= xmin]
    n = len(tail)
    if n < 2 or n_boot < 1:
        return {"tau_std": None, "tau_ci95": (None, None), "n_boot": 0, "tau_boot_mean": None,
                "tau_boot_values": []}
    boot_taus = np.empty(n_boot)
    for i in range(n_boot):
        resample = rng.choice(tail, size=n, replace=True)
        boot_taus[i] = fit_alpha_discrete_mle(resample, xmin, bounds=alpha_bounds)
    lo, hi = np.percentile(boot_taus, [2.5, 97.5])
    return {
        "tau_std": float(np.std(boot_taus)),
        "tau_ci95": (float(lo), float(hi)),
        "n_boot": int(n_boot),
        "tau_boot_mean": float(np.mean(boot_taus)),
        "tau_boot_values": boot_taus.tolist(),
    }


# --------------------------------------------------------------------------
# Adendo ao Gap (c): PRIMARY tau significance test -- paired bootstrap of
# Delta_tau, reusing the per-segment MLE bootstrap distributions above.
# Added AFTER the synthetic validation of the Poisson-surrogate test (d)
# showed it loses power under PRE/POST rate mismatch (see METHODOLOGY_NOTE.md
# "Adendo ao Gap (c)" and module docstring gap (e) above). NO new resampling
# is performed here -- purely a vectorized numpy re-read/pairing of the
# `tau_boot_values` each segment's own `bootstrap_tau_uncertainty` call
# already computed inside `analyze_segment`.
# --------------------------------------------------------------------------

def paired_bootstrap_tau_test(tau_boot_values_pre, tau_boot_values_post):
    """PRIMARY significance test for Delta_tau. Pairs the i-th PRE MLE
    bootstrap draw with the i-th POST MLE bootstrap draw (standard
    two-sample paired-bootstrap convention -- same convention used in the
    dfa-multiscale-entropy addendum) to form
    `Delta_tau_boot_i = tau_boot_POST_i - tau_boot_PRE_i`, entirely from the
    bootstrap distributions PRE and POST already computed independently by
    `bootstrap_tau_uncertainty` (resampling each segment's OWN observed
    avalanches -- never a cross-segment resample). Reports the 95%
    percentile CI of `Delta_tau_boot` and
    `p_bootstrap_tau = 2*min(frac<=0, frac>=0)` (two-tailed, matching the
    bicaudal convention used for the Poisson-surrogate test).

    Unlike the Poisson-surrogate null, this test does NOT require PRE and
    POST to share a rate: each segment's bootstrap distribution is built
    purely from its own observed avalanche sizes, so a PRE/POST rate
    mismatch cannot inflate or deflate either distribution's own dispersion
    the way it does for rate-driven Poisson surrogates.

    Returns a dict; `reason` is 'ok', 'missing_bootstrap_distribution' (one
    or both segments had no tau fit / no bootstrap at all), or
    'insufficient_bootstrap_draws' (fewer than 2 paired draws available)."""
    if tau_boot_values_pre is None or tau_boot_values_post is None:
        return {
            "delta_tau_boot_ci95": (None, None), "p_bootstrap_tau": None,
            "n_paired": 0, "delta_tau_boot_mean": None, "delta_tau_boot_std": None,
            "delta_tau_boot_values": [], "reason": "missing_bootstrap_distribution",
        }
    pre = np.asarray(tau_boot_values_pre, dtype=float)
    post = np.asarray(tau_boot_values_post, dtype=float)
    n = int(min(len(pre), len(post)))
    if n < 2:
        return {
            "delta_tau_boot_ci95": (None, None), "p_bootstrap_tau": None,
            "n_paired": n, "delta_tau_boot_mean": None, "delta_tau_boot_std": None,
            "delta_tau_boot_values": [], "reason": "insufficient_bootstrap_draws",
        }
    delta = post[:n] - pre[:n]
    lo, hi = np.percentile(delta, [2.5, 97.5])
    frac_le0 = float(np.mean(delta <= 0))
    frac_ge0 = float(np.mean(delta >= 0))
    p_bootstrap_tau = float(min(2.0 * min(frac_le0, frac_ge0), 1.0))
    return {
        "delta_tau_boot_ci95": (float(lo), float(hi)),
        "p_bootstrap_tau": p_bootstrap_tau,
        "n_paired": n,
        "delta_tau_boot_mean": float(np.mean(delta)),
        "delta_tau_boot_std": float(np.std(delta)),
        "delta_tau_boot_values": delta.tolist(),
        "reason": "ok",
    }


# --------------------------------------------------------------------------
# Segment-level analysis (binning + avalanche extraction + tau + sigma)
# --------------------------------------------------------------------------

def analyze_segment(events, lam, do_mle_bootstrap=True, n_mle_bootstrap=N_MLE_BOOTSTRAP,
                     rng=None, min_tail_n=MIN_TAIL_N, candidate_cap=XMIN_CANDIDATE_CAP):
    """Run the fixed lambda -> bin -> avalanche -> (tau, sigma) pipeline on
    one segment's event timestamps. `lam` must already be fixed (from the
    combined PRE+POST stream, per gap (a) -- never recomputed here)."""
    events = np.sort(np.asarray(events, dtype=float))
    n_events = int(len(events))
    if n_events < 2:
        return {
            "n_events": n_events, "duration": None, "mu": None,
            "t_min": None, "t_max": None, "lambda": float(lam),
            "n_bins": 0, "n_avalanches": 0, "s_values": [],
            "tau_fit": {"tau": None, "xmin": None, "D": None, "n_tail": 0,
                        "n_total": 0, "n_candidates_tested": 0, "reason": "too_few_events"},
            "sigma": None, "n_sigma_pairs": 0, "tau_bootstrap": None, "avalanches": [],
        }
    t_min, t_max = float(events[0]), float(events[-1])
    duration = t_max - t_min
    mu = (n_events / duration) if duration > 0 else None

    counts, edges = bin_counts(events, lam, t_min, t_max)
    avalanches = extract_avalanches(counts)
    s_values = np.array([a["s"] for a in avalanches], dtype=float)

    tau_fit = fit_powerlaw_clauset(s_values, min_tail_n=min_tail_n, candidate_cap=candidate_cap)
    sigma = branching_ratio_sigma(avalanches)
    n_sigma_pairs = count_sigma_pairs(avalanches)

    result = {
        "n_events": n_events, "duration": duration, "mu": mu,
        "t_min": t_min, "t_max": t_max, "lambda": float(lam),
        "n_bins": int(len(counts)), "n_avalanches": len(avalanches),
        "s_values": s_values.astype(int).tolist(),
        "tau_fit": tau_fit, "sigma": sigma, "n_sigma_pairs": n_sigma_pairs,
        "avalanches": avalanches,
    }

    if do_mle_bootstrap and tau_fit.get("tau") is not None:
        if rng is None:
            rng = np.random.default_rng()
        result["tau_bootstrap"] = bootstrap_tau_uncertainty(
            s_values, tau_fit["xmin"], n_boot=n_mle_bootstrap, rng=rng)
    else:
        result["tau_bootstrap"] = None

    return result


# --------------------------------------------------------------------------
# Gap (c): homogeneous-Poisson surrogate generator
# --------------------------------------------------------------------------

def poisson_surrogate(mu, duration, rng):
    """One realization of a homogeneous Poisson process with rate `mu` over
    span [0, duration]: event COUNT ~ Poisson(mu * duration), timestamps
    i.i.d. Uniform(0, duration)."""
    if mu is None or duration is None or duration <= 0 or mu <= 0:
        return np.array([])
    n = rng.poisson(mu * duration)
    if n == 0:
        return np.array([])
    return np.sort(rng.uniform(0, duration, size=int(n)))


# --------------------------------------------------------------------------
# Full transition-test pipeline
# --------------------------------------------------------------------------

def run_lambda_robustness(pre_events, post_events, lam_primary,
                           min_tail_n=MIN_TAIL_N, candidate_cap=XMIN_CANDIDATE_CAP):
    """Robustness check (METHODOLOGY_NOTE.md gap (a)): repeat the REAL
    tau/sigma computation (point estimates only, no surrogate re-test, no
    MLE bootstrap -- documented simplification: this checks sensitivity of
    the POINT ESTIMATE to the bin-width choice, not a re-run of the full
    1000-surrogate significance test at 3x the cost) at
    lambda_robustez = 2*lambda_primary and lambda_primaria/2."""
    out = {}
    for label, lam_r in (("lambda_x2", 2.0 * lam_primary), ("lambda_div2", lam_primary / 2.0)):
        rp = analyze_segment(pre_events, lam_r, do_mle_bootstrap=False,
                              min_tail_n=min_tail_n, candidate_cap=candidate_cap)
        po = analyze_segment(post_events, lam_r, do_mle_bootstrap=False,
                              min_tail_n=min_tail_n, candidate_cap=candidate_cap)
        tp, tpo = rp["tau_fit"].get("tau"), po["tau_fit"].get("tau")
        sp, spo = rp["sigma"], po["sigma"]
        out[label] = {
            "lambda": lam_r,
            "tau_pre": tp, "tau_post": tpo,
            "delta_tau": None if (tp is None or tpo is None) else tpo - tp,
            "sigma_pre": sp, "sigma_post": spo,
            "delta_sigma": None if (sp is None or spo is None) else spo - sp,
            "n_avalanches_pre": rp["n_avalanches"], "n_avalanches_post": po["n_avalanches"],
        }
    return out


def run_soc_pipeline(pre_events, post_events, n_surrogates=N_SURROGATES, seed=SEED,
                      n_mle_bootstrap=N_MLE_BOOTSTRAP, min_tail_n=MIN_TAIL_N,
                      candidate_cap=XMIN_CANDIDATE_CAP,
                      surrogate_candidate_cap=SURROGATE_XMIN_CANDIDATE_CAP,
                      compute_robustness=True):
    """Run the full SOC-avalanche transition test between a PRE and a POST
    event stream. Segment SELECTION (which events count as "pre-transition"
    vs "post-transition", the Mc completeness cut, the primary-vs-robustness
    50%-split) happens OUTSIDE this function per METHODOLOGY_NOTE.md gap (d)
    -- this function only implements the fixed lambda/binning/avalanche/MLE/
    surrogate pipeline itself, unmodified across domains.

    pre_events, post_events: 1-D arrays of event timestamps (any consistent
    time unit), sorted or unsorted.

    Returns a single dict with everything a downstream agent needs to report
    a result without recomputing anything:
      - lambda: the single IEI-derived bin width used for both segments
      - real_pre, real_post: full analyze_segment() output (avalanches,
        tau_fit incl. xmin/D, tau_bootstrap CI, sigma, s_values, mu, duration)
      - tau_pre, tau_post, delta_tau (None if either tau_fit failed)
      - sigma_pre, sigma_post, delta_sigma (None if either sigma undefined)
      - p_tau, p_sigma: two-tailed Poisson-surrogate p-values (fraction of
        surrogates with |Delta_surrogate| >= |Delta_real|) -- SECONDARY/
        complementary significance check for tau (see paired_bootstrap_tau
        below for the PRIMARY tau test), still the only significance test
        for sigma
      - surrogate_delta_tau_values / surrogate_delta_sigma_values: the null
        distributions themselves, plus mean/std summaries
      - n_surrogates_valid_tau/sigma, n_surrogates_undefined_tau/sigma:
        bookkeeping for surrogates where a channel could not be fit
      - paired_bootstrap_tau: PRIMARY significance test for Delta_tau
        (METHODOLOGY_NOTE.md "Adendo ao Gap (c)") -- dict with
        delta_tau_boot_ci95 (95% percentile CI), p_bootstrap_tau, n_paired,
        delta_tau_boot_mean/std, delta_tau_boot_values (see
        paired_bootstrap_tau_test docstring); also exposed at top level as
        p_bootstrap_tau / delta_tau_boot_ci95 for convenience
      - robustness: lambda*2 / lambda/2 point-estimate sensitivity check
        (gap (a)), unless compute_robustness=False
      - config: exact fixed parameters used, for provenance
    """
    pre = np.sort(np.asarray(pre_events, dtype=float))
    post = np.sort(np.asarray(post_events, dtype=float))
    combined = np.sort(np.concatenate([pre, post]))
    lam = compute_lambda(combined)

    master_rng = np.random.default_rng(seed)

    real_pre = analyze_segment(pre, lam, do_mle_bootstrap=True, n_mle_bootstrap=n_mle_bootstrap,
                                rng=master_rng, min_tail_n=min_tail_n, candidate_cap=candidate_cap)
    real_post = analyze_segment(post, lam, do_mle_bootstrap=True, n_mle_bootstrap=n_mle_bootstrap,
                                 rng=master_rng, min_tail_n=min_tail_n, candidate_cap=candidate_cap)

    tau_pre = real_pre["tau_fit"].get("tau")
    tau_post = real_post["tau_fit"].get("tau")
    delta_tau = None if (tau_pre is None or tau_post is None) else tau_post - tau_pre

    sigma_pre = real_pre["sigma"]
    sigma_post = real_post["sigma"]
    delta_sigma = None if (sigma_pre is None or sigma_post is None) else sigma_post - sigma_pre

    surr_delta_tau, surr_delta_sigma = [], []
    n_surr_tau_undef, n_surr_sigma_undef = 0, 0

    for _ in range(n_surrogates):
        s_pre = poisson_surrogate(real_pre["mu"], real_pre["duration"], master_rng)
        s_post = poisson_surrogate(real_post["mu"], real_post["duration"], master_rng)
        if len(s_pre) < 2 or len(s_post) < 2:
            n_surr_tau_undef += 1
            n_surr_sigma_undef += 1
            continue
        a_pre = analyze_segment(s_pre, lam, do_mle_bootstrap=False,
                                 min_tail_n=min_tail_n, candidate_cap=surrogate_candidate_cap)
        a_post = analyze_segment(s_post, lam, do_mle_bootstrap=False,
                                  min_tail_n=min_tail_n, candidate_cap=surrogate_candidate_cap)

        t_pre, t_post = a_pre["tau_fit"].get("tau"), a_post["tau_fit"].get("tau")
        if t_pre is not None and t_post is not None:
            surr_delta_tau.append(t_post - t_pre)
        else:
            n_surr_tau_undef += 1

        sg_pre, sg_post = a_pre["sigma"], a_post["sigma"]
        if sg_pre is not None and sg_post is not None:
            surr_delta_sigma.append(sg_post - sg_pre)
        else:
            n_surr_sigma_undef += 1

    surr_delta_tau = np.array(surr_delta_tau, dtype=float)
    surr_delta_sigma = np.array(surr_delta_sigma, dtype=float)

    p_tau = (None if (delta_tau is None or len(surr_delta_tau) == 0)
             else float(np.mean(np.abs(surr_delta_tau) >= abs(delta_tau))))
    p_sigma = (None if (delta_sigma is None or len(surr_delta_sigma) == 0)
               else float(np.mean(np.abs(surr_delta_sigma) >= abs(delta_sigma))))

    # Adendo ao Gap (c) -- PRIMARY tau significance test: paired bootstrap of
    # Delta_tau, reusing (no new resampling) the tau_boot_values each segment's
    # own bootstrap_tau_uncertainty call already produced above via
    # analyze_segment's do_mle_bootstrap=True path, under the SAME master_rng/
    # seed as the rest of this module.
    tb_pre = real_pre.get("tau_bootstrap")
    tb_post = real_post.get("tau_bootstrap")
    tb_pre_values = tb_pre.get("tau_boot_values") if tb_pre else None
    tb_post_values = tb_post.get("tau_boot_values") if tb_post else None
    paired_bootstrap_tau = paired_bootstrap_tau_test(tb_pre_values, tb_post_values)

    result = {
        "lambda": lam,
        "real_pre": real_pre,
        "real_post": real_post,
        "tau_pre": tau_pre, "tau_post": tau_post, "delta_tau": delta_tau,
        "sigma_pre": sigma_pre, "sigma_post": sigma_post, "delta_sigma": delta_sigma,
        "n_sigma_pairs_pre": real_pre["n_sigma_pairs"], "n_sigma_pairs_post": real_post["n_sigma_pairs"],
        "p_tau": p_tau, "p_sigma": p_sigma,
        "paired_bootstrap_tau": paired_bootstrap_tau,
        "p_bootstrap_tau": paired_bootstrap_tau["p_bootstrap_tau"],
        "delta_tau_boot_ci95": paired_bootstrap_tau["delta_tau_boot_ci95"],
        "n_surrogates": n_surrogates,
        "n_surrogates_valid_tau": int(len(surr_delta_tau)),
        "n_surrogates_undefined_tau": int(n_surr_tau_undef),
        "n_surrogates_valid_sigma": int(len(surr_delta_sigma)),
        "n_surrogates_undefined_sigma": int(n_surr_sigma_undef),
        "surrogate_delta_tau_mean": float(np.mean(surr_delta_tau)) if len(surr_delta_tau) else None,
        "surrogate_delta_tau_std": float(np.std(surr_delta_tau)) if len(surr_delta_tau) else None,
        "surrogate_delta_sigma_mean": float(np.mean(surr_delta_sigma)) if len(surr_delta_sigma) else None,
        "surrogate_delta_sigma_std": float(np.std(surr_delta_sigma)) if len(surr_delta_sigma) else None,
        "surrogate_delta_tau_values": surr_delta_tau.tolist(),
        "surrogate_delta_sigma_values": surr_delta_sigma.tolist(),
        "config": {
            "seed": seed,
            "n_surrogates": n_surrogates,
            "n_mle_bootstrap": n_mle_bootstrap,
            "min_tail_n": min_tail_n,
            "candidate_cap": candidate_cap,
            "surrogate_candidate_cap": surrogate_candidate_cap,
            "alpha_bounds": list(ALPHA_BOUNDS),
        },
    }

    if compute_robustness:
        result["robustness"] = run_lambda_robustness(pre, post, lam,
                                                       min_tail_n=min_tail_n,
                                                       candidate_cap=candidate_cap)

    return result


# --------------------------------------------------------------------------
# Synthetic event-stream generators used ONLY for validation (never on real
# domain data -- see ../analysis/validate_synthetic.py). Kept in this module
# because they encode the exact generative-model choice documented as the
# positive-control rationale (see that script's header for citations).
# --------------------------------------------------------------------------

def generate_branching_events(rng, mu_immigrants, branching_ratio, mean_delay, duration,
                               max_events=200000, max_cluster_size=5000):
    """Event stream from an immigration-birth branching process (Hawkes
    1974; Hawkes & Oakes 1974 cluster representation of a self-exciting
    point process): "immigrant" events form a homogeneous Poisson process
    at rate `mu_immigrants`; every event (immigrant or offspring) spawns
    Poisson(branching_ratio) direct offspring, each offspring's time delay
    from its parent drawn i.i.d. Exponential(mean_delay). Each immigrant's
    full descendant tree is exactly a Galton-Watson branching process with
    Poisson(branching_ratio) offspring distribution, so the marginal
    distribution of (immigrant + all descendants) cluster SIZE is exactly
    the theoretical GW total-progeny distribution used as the positive
    control in validate_synthetic.py (Borel distribution at
    branching_ratio=1, asymptotically ~ n^-1.5; see Otter 1949, Dwass 1969).

    `max_cluster_size`/`max_events` are hard safety caps against the
    occasional very large cluster that a near-critical/critical branching
    process can (rarely, but with positive probability) produce -- this
    truncates the extreme tail of individual runs and is a documented
    simulation simplification, not a property of the underlying model.
    """
    n_imm = rng.poisson(mu_immigrants * duration)
    if n_imm == 0:
        return np.array([])
    imm_times = rng.uniform(0, duration, size=n_imm)
    all_events = []
    total_count = 0
    for t0 in imm_times:
        if total_count >= max_events:
            break
        cluster_events = [t0]
        queue = [t0]
        cluster_size = 1
        while queue and cluster_size < max_cluster_size and total_count < max_events:
            parent_t = queue.pop()
            n_off = rng.poisson(branching_ratio)
            if n_off <= 0:
                continue
            delays = rng.exponential(mean_delay, size=n_off)
            for d in delays:
                if cluster_size >= max_cluster_size or total_count + 1 > max_events:
                    break
                ct = parent_t + d
                cluster_events.append(ct)
                queue.append(ct)
                cluster_size += 1
                total_count += 1
        all_events.extend(cluster_events)
        total_count = len(all_events)
    return np.sort(np.array(all_events, dtype=float))


def generate_homogeneous_poisson_events(rng, mu, duration):
    """Pure homogeneous Poisson process (negative control): no clustering
    structure at all beyond what falls out of chance IEI variability."""
    return poisson_surrogate(mu, duration, rng)
