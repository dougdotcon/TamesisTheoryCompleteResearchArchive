"""
Extreme Value Theory tail-index dynamics pipeline for DISC-TRI-RG-001,
candidate `evt-hill` (Hill estimator, Hill 1975, Ann. Statist. 3:1163;
automated threshold selection via single-level bootstrap MSE minimization,
simplified from Danielsson, de Haan, Peng & de Vries 2001, J. Multivariate
Analysis 76:226; GPD MLE companion channel, de Haan & Ferreira 2006).

Fixed BEFORE running on any real domain (NOAA GHCN-Daily PDX 2021 heat
wave, USGS Cape Fear River gauge / Hurricane Florence) -- see
../METHODOLOGY_NOTE.md for the full rationale, gaps (a)-(f). This module
implements ONLY what METHODOLOGY_NOTE.md specifies, with no
reformulation. It is a NEW, self-contained implementation specific to
this test line -- it does not import from and is not derived from
`kramers_moyal/analysis/km_common.py`, `permutation_entropy/analysis/
pe_common.py`, or `soc_avalanches/analysis/soc_common.py`, even though
the top-level structure (subsample -> real-segment estimation ->
significance test -> single public entry point) follows the same
convention already used for those candidates in this lab.

Method (METHODOLOGY_NOTE.md gaps (a), (b), (e), (f)):

  Gap (a) -- k*/threshold selection ("R_lambda" for this candidate):
    1. Candidate k-grid: K_GRID_SIZE=30 log-spaced UNIQUE integers between
       K_MIN=10 and k_max=floor(n/4).
    2. Hill estimator at each k, on the UPPER-tail order statistics of the
       raw series (not absolute increments -- both real domains of this
       round are naturally one-directional: higher temperature, higher
       gauge height are the extremes of interest):
           H(k) = (1/k) * sum_{i=1}^{k} log( X_(n-i+1) / X_(n-k) )
       where X_(1) <= ... <= X_(n) are the order statistics.
    3. B_BOOTSTRAP=200 resamples WITH replacement of the full raw array
       (Danielsson et al.'s SINGLE-level bootstrap, explicitly simplified
       from their original double bootstrap with second-order-bias
       correction via a separately estimated `rho` -- that correction is
       NOT implemented here, declared explicitly per METHODOLOGY_NOTE.md
       gap (a)); Var_boot(k) = variance of the 200 resampled H(k).
    4. H_ref = median of H(k) over the MIDDLE THIRD of the k-grid
       (deterministic proxy for the "stable plateau" a Hill plot's visual
       inspection traditionally looks for).
    5. MSE(k) = Var_boot(k) + (H(k) - H_ref)^2; k* = argmin MSE(k).
    6. xi_Hill = H(k*).
    k*/threshold is RE-ESTIMATED INDEPENDENTLY in every segment (PRE,
    POST, and each side of each randomization replica in gap (f)) --
    deliberate departure from the "estimate once on PRE, reuse on POST"
    convention used elsewhere in this line, because xi itself is a
    property of that specific segment's marginal distribution and k* is
    the threshold that best resolves THAT distribution (see
    METHODOLOGY_NOTE.md for the full argument, incl. the explicit
    reference to the PKS/EUR-CHF POST failure in kramers_moyal that this
    design avoids by construction).

  Gap (b) -- companion channel xi_MLE:
    GPD (Generalized Pareto Distribution) maximum-likelihood fit to the
    exceedances (X - u) above the SAME threshold u = X_(n-k*) already
    selected by the Hill step above. Implemented via
    `scipy.stats.genpareto.fit(exceedances, floc=0)` (loc fixed at 0
    because exceedances are non-negative by construction) rather than a
    hand-rolled Newton-Raphson MLE solver -- documented choice: scipy's
    constrained optimizer is more numerically robust at small exceedance
    counts / near-boundary shape parameters than a hand-rolled solver
    would be, and is a standard, auditable implementation of the same
    GPD MLE (de Haan & Ferreira 2006). `xi_MLE` = the fitted GPD shape
    parameter `c`.

  Gap (f) -- significance test: RANDOMIZATION OF THE SPLIT POINT, NOT
    IAAFT (deliberate, justified departure from the IAAFT convention used
    by every other candidate in this line -- see METHODOLOGY_NOTE.md for
    the full mathematical argument: IAAFT preserves the exact marginal
    distribution of values by construction, and the Hill estimator is a
    pure function of order statistics/values, not temporal order, so
    EVERY IAAFT surrogate of a real segment would have xi IDENTICAL to
    that segment -- a degenerate, uninformative null).
    1. Pool = PRE + POST concatenated in ORIGINAL temporal order.
    2. N_RANDOMIZATIONS=200 replicas. Each replica draws a split point s
       uniformly at random between MIN_SEG_FRACTION=0.2 and
       MAX_SEG_FRACTION=0.8 of the pooled length, splits into
       "before"/"after", and re-runs the FULL gap (a)-(b) procedure
       independently on each side (threshold re-estimated on each side,
       never reused).
    3. Delta_xi_random = xi(after) - xi(before), per replica.
    4. p = fraction of replicas with |Delta_xi_random| >= |Delta_xi_real|
       (two-tailed).

  Gap (d)/(e) -- subsampling and sample floor:
    MAX_N_PER_SEGMENT=100_000 uniform-stride subsampling, applied ONCE
    per segment BEFORE any expensive computation (Hill grid, bootstrap,
    or randomization) -- explicitly learned from the real bugs already
    found and fixed in this test line (kramers_moyal's CK-test bootstrap
    redundancy bug; permutation_entropy's IAAFT-surrogate-generated-
    before-subsampling bug): subsampling happens exactly once, at the
    top of `run_evt_hill_analysis`, before PRE/POST are ever passed to
    `select_k_star` or to the randomization loop, so it can never be
    applied inconsistently across the real segments and the
    randomization replicas (which reuse the already-subsampled pool).
    MIN_N_PER_SEGMENT=200 -- any segment (real or randomization side)
    below this returns an explicit "insufficient_samples" status rather
    than silently proceeding with an unreliable k-grid (k_max=floor(n/4)
    needs n>=200 for k_max>=50 to comfortably dominate k_min=10).

Implementation note (guard not stated verbatim in METHODOLOGY_NOTE.md,
but required to make the formula in gap (a) step 2 well-defined): the
classical Hill estimator's log-ratio requires POSITIVE order statistics.
Both real domains of this round are naturally positive at the *tail*
(TMAX in degrees C can be negative overall but the record heat-wave tail
is far above zero; gauge height is bounded near zero from below), but a
domain-agnostic implementation still needs a defined behavior if a given
k's threshold u = X_(n-k) is <= 0 (e.g. deep in a Student-t validation
series' body). This module's `_hill_H` returns NaN for any k whose
threshold or whose retained top-k values are <= 0, and the argmin over
MSE(k) in gap (a) step 5 is restricted to the k's with a finite (valid)
H(k) -- so xi_Hill is only ever reported at a k where the positivity
assumption genuinely holds for the k largest values of that specific
segment. This is an implementation guard, not a methodological
deviation: it does not change any of the six numbered steps of gap (a),
it only makes step 2 well-defined for a k where it would otherwise be
undefined.

Any agent applying this pipeline to real data MUST import and call
`run_evt_hill_analysis` (or the lower-level helpers below) rather than
reimplementing any of this.
"""
import numpy as np
from scipy.stats import genpareto

# ---- fixed constants (METHODOLOGY_NOTE.md gaps (a),(e),(f) -- identical
# for every domain/segment this pipeline is ever applied to; no
# per-domain or post-hoc tuning) ----
K_MIN = 10                      # gap (a): k-grid floor
K_GRID_SIZE = 30                # gap (a): number of log-spaced k candidates
B_BOOTSTRAP = 200               # gap (a): single-level bootstrap resamples for Var_boot(k)
MIN_EXCEEDANCES_GPD = 5         # guard for gap (b): GPD MLE needs a minimum exceedance count
MAX_N_PER_SEGMENT = 100_000     # gap (e): subsampling cap
MIN_N_PER_SEGMENT = 200         # gap (e): sample floor
N_RANDOMIZATIONS = 200          # gap (f): randomization replicas
MIN_SEG_FRACTION = 0.2          # gap (f): split-point lower bound (fraction of pooled length)
MAX_SEG_FRACTION = 0.8          # gap (f): split-point upper bound (fraction of pooled length)
SEED = 12345


# --------------------------------------------------------------------------
# Gap (e): subsampling -- applied ONCE, before any expensive computation
# --------------------------------------------------------------------------

def subsample_segment(x, max_n=MAX_N_PER_SEGMENT):
    """Uniform-stride decimation to at most `max_n` samples.

    If len(x) <= max_n, returns x unchanged (stride=1, subsampled=False).
    Otherwise stride = ceil(N / max_n), x[::stride] -- identical
    convention already used in this lab's other TRI_RG pipelines
    (rqa_common.py, vg_common.py, pe_common.py). Preserves the original
    temporal order of the retained samples (required for gap (f), which
    concatenates PRE+POST "in original temporal order").
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    if N <= max_n:
        return x.copy(), {"n_original": int(N), "n_used": int(N), "stride": 1, "subsampled": False}
    stride = int(np.ceil(N / max_n))
    decimated = x[::stride].copy()
    return decimated, {
        "n_original": int(N), "n_used": int(len(decimated)), "stride": int(stride),
        "subsampled": True,
    }


# --------------------------------------------------------------------------
# Gap (a): k-grid, Hill estimator, bootstrap MSE minimization
# --------------------------------------------------------------------------

def _log_spaced_int_grid(k_min, k_max, size):
    """30 log-spaced UNIQUE integers between k_min and k_max (inclusive).

    If rounding collapses distinct log-spaced points onto the same
    integer (possible when k_max-k_min is small relative to `size`), the
    returned grid is simply shorter than `size` -- reported honestly via
    `len(k_grid)` in the output rather than padded artificially.
    """
    k_min = int(k_min)
    k_max = int(k_max)
    if k_max <= k_min:
        return np.array([k_min], dtype=int)
    raw = np.exp(np.linspace(np.log(k_min), np.log(k_max), size))
    grid = np.unique(np.round(raw).astype(int))
    grid = np.clip(grid, k_min, k_max)
    return np.unique(grid)


def _hill_H(x_sorted_asc, k):
    """Hill estimator H(k) on the upper tail of a sorted-ascending array.

    H(k) = (1/k) * sum_{i=1}^{k} log( X_(n-i+1) / X_(n-k) )

    Returns NaN if k >= n, or if the threshold X_(n-k) or any of the
    retained top-k order statistics are <= 0 (see module docstring
    "Implementation note" -- this is a well-definedness guard, not a
    methodological deviation).
    """
    n = len(x_sorted_asc)
    k = int(k)
    if k <= 0 or k >= n:
        return np.nan
    u = x_sorted_asc[n - k - 1]
    if u <= 0:
        return np.nan
    top = x_sorted_asc[n - k:]
    if np.any(top <= 0):
        return np.nan
    return float(np.mean(np.log(top / u)))


def _bootstrap_var_hill(x, k_grid, rng, b_bootstrap=B_BOOTSTRAP):
    """Gap (a) step 3: B resamples WITH replacement of the full raw array
    `x`; Var_boot(k) = variance of the resampled H(k) across replicas.

    Each replica resamples the full array ONCE and is sorted ONCE, then
    reused for every k in `k_grid` -- mathematically identical to "B
    bootstrap resamples of the complete array of order statistics",
    just organized to avoid re-sorting per (replica, k) pair.
    """
    n = len(x)
    n_k = len(k_grid)
    H_boot = np.empty((b_bootstrap, n_k), dtype=float)
    for b in range(b_bootstrap):
        resample = rng.choice(x, size=n, replace=True)
        rs_sorted = np.sort(resample)
        for j, k in enumerate(k_grid):
            H_boot[b, j] = _hill_H(rs_sorted, k)
    with np.errstate(invalid="ignore"):
        var_boot = np.nanvar(H_boot, axis=0, ddof=1)
    n_valid = np.sum(np.isfinite(H_boot), axis=0)
    return var_boot, n_valid


# --------------------------------------------------------------------------
# Gap (b): GPD MLE companion channel
# --------------------------------------------------------------------------

def _fit_gpd_mle(exceedances, min_exceedances=MIN_EXCEEDANCES_GPD):
    """GPD MLE fit to exceedances above the Hill-selected threshold.

    Uses `scipy.stats.genpareto.fit(exceedances, floc=0)` -- see module
    docstring gap (b) for why this was chosen over a hand-rolled solver.
    """
    exceedances = np.asarray(exceedances, dtype=float)
    if len(exceedances) < min_exceedances:
        return {"status": "insufficient_exceedances", "n_exceedances": int(len(exceedances)),
                "xi_MLE": None, "gpd_scale": None}
    try:
        c, loc, scale = genpareto.fit(exceedances, floc=0)
        if not (np.isfinite(c) and np.isfinite(scale)):
            return {"status": "fit_non_finite", "n_exceedances": int(len(exceedances)),
                    "xi_MLE": None, "gpd_scale": None}
        return {"status": "ok", "n_exceedances": int(len(exceedances)),
                "xi_MLE": float(c), "gpd_scale": float(scale)}
    except Exception as exc:  # pragma: no cover -- defensive, reported not masked
        return {"status": f"fit_failed: {exc}", "n_exceedances": int(len(exceedances)),
                "xi_MLE": None, "gpd_scale": None}


# --------------------------------------------------------------------------
# Gap (a)+(b) combined: full k*/threshold selection + xi_Hill + xi_MLE for
# ONE segment (re-run independently for every segment, per module docstring)
# --------------------------------------------------------------------------

def select_k_star(x, rng, b_bootstrap=B_BOOTSTRAP, grid_size=K_GRID_SIZE, k_min=K_MIN,
                   min_n=MIN_N_PER_SEGMENT):
    """Full gap (a)+(b) procedure on a single segment `x`.

    `rng` must be a numpy Generator, consumed in-place (so a single
    top-level rng, seeded once, deterministically reproduces an entire
    `run_evt_hill_analysis` call end to end -- see that function).
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < min_n:
        return {"status": "insufficient_samples", "n": int(n)}
    k_max = int(np.floor(n / 4))
    if k_max < k_min:
        return {"status": "insufficient_samples_for_k_grid", "n": int(n), "k_max": k_max, "k_min": k_min}

    x_sorted = np.sort(x)
    k_grid = _log_spaced_int_grid(k_min, k_max, grid_size)
    H = np.array([_hill_H(x_sorted, k) for k in k_grid])
    valid = np.isfinite(H)
    if valid.sum() < 3:
        return {"status": "insufficient_valid_k_nonpositive_tail", "n": int(n),
                "k_grid": k_grid.tolist(), "H_k": H.tolist()}

    m = len(k_grid)
    lo = m // 3
    hi = m - m // 3
    middle_idx = np.arange(lo, hi)
    if middle_idx.size == 0:
        middle_idx = np.arange(m)
    H_ref = float(np.nanmedian(H[middle_idx]))

    var_boot, n_valid_boot = _bootstrap_var_hill(x, k_grid, rng, b_bootstrap=b_bootstrap)
    mse = var_boot + (H - H_ref) ** 2
    mse_masked = np.where(valid, mse, np.inf)
    idx_star = int(np.argmin(mse_masked))
    k_star = int(k_grid[idx_star])
    xi_hill = float(H[idx_star])
    threshold_u = float(x_sorted[n - k_star - 1])

    exceedances = x[x > threshold_u] - threshold_u
    gpd = _fit_gpd_mle(exceedances)

    return {
        "status": "ok",
        "n": int(n),
        "k_grid": k_grid.tolist(),
        "H_k": H.tolist(),
        "var_boot": var_boot.tolist(),
        "n_valid_boot": n_valid_boot.tolist(),
        "mse": mse.tolist(),
        "H_ref": H_ref,
        "middle_third_idx": middle_idx.tolist(),
        "idx_star": idx_star,
        "k_star": k_star,
        "xi_Hill": xi_hill,
        "threshold_u": threshold_u,
        "n_exceedances": gpd["n_exceedances"],
        "xi_MLE": gpd["xi_MLE"],
        "gpd_scale": gpd["gpd_scale"],
        "gpd_fit_status": gpd["status"],
    }


# --------------------------------------------------------------------------
# Gap (f): randomization test on the split point (NOT IAAFT)
# --------------------------------------------------------------------------

def _delta(after, before, key):
    a, b = after.get(key), before.get(key)
    if a is None or b is None:
        return None
    return float(a - b)


def randomization_split_test(pool, delta_real_hill, delta_real_mle, rng,
                              n_randomizations=N_RANDOMIZATIONS,
                              min_seg_fraction=MIN_SEG_FRACTION,
                              max_seg_fraction=MAX_SEG_FRACTION,
                              b_bootstrap=B_BOOTSTRAP, grid_size=K_GRID_SIZE, k_min=K_MIN,
                              min_n=MIN_N_PER_SEGMENT):
    """Gap (f): pool is PRE+POST already concatenated in original temporal
    order. Draws `n_randomizations` random split points, re-runs the full
    gap (a)-(b) procedure independently on each side, and computes the
    two-tailed p-values against the REAL Delta_xi (passed in, so this
    function never recomputes the real segments itself -- avoids any risk
    of the real and randomization-null estimates of xi(PRE)/xi(POST)
    silently drifting apart across two separate bootstrap draws).
    """
    n_total = len(pool)
    lo = int(np.floor(min_seg_fraction * n_total))
    hi = int(np.ceil(max_seg_fraction * n_total))
    lo = max(lo, min_n)
    hi = min(hi, n_total - min_n)

    random_delta_hill = []
    random_delta_mle = []
    split_points = []
    n_skipped = 0
    skip_reasons = []

    if hi < lo:
        return {
            "status": "insufficient_pool_for_split_range",
            "n_total": int(n_total), "lo": lo, "hi": hi,
            "n_valid_replicas": 0, "n_skipped": int(n_randomizations),
            "p_xi_Hill": None, "p_xi_MLE": None,
        }

    for _ in range(n_randomizations):
        s = int(rng.integers(lo, hi + 1))
        before = pool[:s]
        after = pool[s:]
        r_before = select_k_star(before, rng, b_bootstrap=b_bootstrap, grid_size=grid_size,
                                  k_min=k_min, min_n=min_n)
        r_after = select_k_star(after, rng, b_bootstrap=b_bootstrap, grid_size=grid_size,
                                 k_min=k_min, min_n=min_n)
        if r_before["status"] != "ok" or r_after["status"] != "ok":
            n_skipped += 1
            skip_reasons.append({"before_status": r_before["status"], "after_status": r_after["status"], "s": s})
            continue
        d_hill = _delta(r_after, r_before, "xi_Hill")
        d_mle = _delta(r_after, r_before, "xi_MLE")
        random_delta_hill.append(d_hill)
        if d_mle is not None:
            random_delta_mle.append(d_mle)
        split_points.append(s)

    random_delta_hill = np.array(random_delta_hill, dtype=float)
    random_delta_mle = np.array(random_delta_mle, dtype=float)

    def _p_value(real_delta, null_array):
        if real_delta is None or len(null_array) == 0:
            return None
        return float(np.mean(np.abs(null_array) >= abs(real_delta)))

    p_hill = _p_value(delta_real_hill, random_delta_hill)
    p_mle = _p_value(delta_real_mle, random_delta_mle)

    return {
        "status": "ok",
        "n_total": int(n_total),
        "split_range": [lo, hi],
        "n_randomizations_requested": int(n_randomizations),
        "n_valid_replicas": int(len(split_points)),
        "n_skipped": int(n_skipped),
        "skip_reasons_sample": skip_reasons[:10],
        "split_points": split_points,
        "random_delta_xi_Hill": random_delta_hill.tolist(),
        "random_delta_xi_MLE": random_delta_mle.tolist(),
        "random_delta_xi_Hill_mean": float(np.mean(random_delta_hill)) if len(random_delta_hill) else None,
        "random_delta_xi_Hill_std": float(np.std(random_delta_hill, ddof=1)) if len(random_delta_hill) > 1 else None,
        "random_delta_xi_MLE_mean": float(np.mean(random_delta_mle)) if len(random_delta_mle) else None,
        "random_delta_xi_MLE_std": float(np.std(random_delta_mle, ddof=1)) if len(random_delta_mle) > 1 else None,
        "delta_real_xi_Hill": delta_real_hill,
        "delta_real_xi_MLE": delta_real_mle,
        "p_xi_Hill": p_hill,
        "p_xi_MLE": p_mle,
    }


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------

def run_evt_hill_analysis(pre_series, post_series, seed=SEED, n_randomizations=N_RANDOMIZATIONS,
                           max_n_per_segment=MAX_N_PER_SEGMENT, min_n_per_segment=MIN_N_PER_SEGMENT,
                           b_bootstrap=B_BOOTSTRAP, grid_size=K_GRID_SIZE, k_min=K_MIN):
    """Full evt-hill pipeline: gap (a)+(b) on real PRE/POST, gap (f)
    randomization-of-split-point significance test. Single public entry
    point -- any agent applying this to real data should call this
    function unmodified.

    Subsampling (gap (e)) is applied EXACTLY ONCE here, to PRE and POST
    independently, BEFORE any other computation -- the randomization test
    in gap (f) reuses these already-subsampled arrays (concatenated),
    never re-subsampling or subsampling inconsistently.
    """
    pre_raw = np.asarray(pre_series, dtype=float)
    post_raw = np.asarray(post_series, dtype=float)

    pre_sub, pre_sub_info = subsample_segment(pre_raw, max_n=max_n_per_segment)
    post_sub, post_sub_info = subsample_segment(post_raw, max_n=max_n_per_segment)

    result = {
        "config": {
            "seed": seed, "n_randomizations": n_randomizations,
            "max_n_per_segment": max_n_per_segment, "min_n_per_segment": min_n_per_segment,
            "b_bootstrap": b_bootstrap, "grid_size": grid_size, "k_min": k_min,
        },
        "subsampling": {"pre": pre_sub_info, "post": post_sub_info},
    }

    if len(pre_sub) < min_n_per_segment or len(post_sub) < min_n_per_segment:
        result["status"] = "insufficient_samples"
        result["n_pre"] = int(len(pre_sub))
        result["n_post"] = int(len(post_sub))
        return result

    rng = np.random.default_rng(seed)

    real_pre = select_k_star(pre_sub, rng, b_bootstrap=b_bootstrap, grid_size=grid_size,
                              k_min=k_min, min_n=min_n_per_segment)
    real_post = select_k_star(post_sub, rng, b_bootstrap=b_bootstrap, grid_size=grid_size,
                               k_min=k_min, min_n=min_n_per_segment)

    result["real_pre"] = real_pre
    result["real_post"] = real_post

    if real_pre["status"] != "ok" or real_post["status"] != "ok":
        result["status"] = "insufficient_samples_for_k_grid"
        return result

    delta_real_hill = _delta(real_post, real_pre, "xi_Hill")
    delta_real_mle = _delta(real_post, real_pre, "xi_MLE")
    result["delta_xi_Hill"] = delta_real_hill
    result["delta_xi_MLE"] = delta_real_mle

    pool = np.concatenate([pre_sub, post_sub])
    randomization = randomization_split_test(
        pool, delta_real_hill, delta_real_mle, rng,
        n_randomizations=n_randomizations, b_bootstrap=b_bootstrap, grid_size=grid_size,
        k_min=k_min, min_n=min_n_per_segment,
    )
    result["randomization"] = randomization
    result["p_xi_Hill"] = randomization.get("p_xi_Hill")
    result["p_xi_MLE"] = randomization.get("p_xi_MLE")
    result["status"] = "ok"
    return result
