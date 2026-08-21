"""
Canonical epsilon-machine statistical-complexity (`C_mu`) pipeline for
DISC-TRI-RG-001, candidate `epsilon_machine_complexity` (computational
mechanics; CSSR reconstruction, Shalizi & Klinkner 2004, UAI; Bayesian
Structural Inference companion, Strelioff & Crutchfield 2014, Phys. Rev. E
89:042119; median-threshold binarization, Aboy, Hornero, Abasolo & Alvarez
2006, IEEE Trans. Biomed. Eng. 53:2282; ternary/tertile quantization,
Kamath 2016, Cogent Engineering 3(1):1177924; IAAFT surrogates, Schreiber &
Schmitz 1996; moving-block bootstrap fallback, Kunsch 1989).

Fixed BEFORE running on any real domain (Old Faithful geyser eruption
intervals; La Palma/Cumbre Vieja 2021 seismic interevent-time sequence) --
see ../METHODOLOGY_NOTE.md for the full rationale. This is a NEW,
self-contained implementation specific to this candidate: it does not
import from, and is not derived from, any other `*_common.py` in this lab,
even though the binarization/ternary R_lambda, the IAAFT surrogate step and
the moving-block-bootstrap fallback are the SAME published methods already
used elsewhere in this line (same convention already documented in
`lempel_ziv_complexity/analysis/lzc_common.py`).

============================================================================
SCOPE DECISIONS (documented here AND in METHODOLOGY_NOTE.md, honestly, as
engineering choices -- not hypothesis reformulations):
============================================================================

1. CSSR here is implemented as "fixed-L causal-state clustering", not the
   full incremental tree-growing/pruning procedure of Shalizi & Klinkner
   2004. For a SMALL alphabet (2 or 3 symbols) and L_max<=8 (per
   METHODOLOGY_NOTE.md), the full history space (<=3^8=6,561 possible
   histories) is directly enumerable without the combinatorial-explosion
   concern that motivated CSSR's incremental-growth design for larger
   alphabets. At each candidate L in the L_max sweep, we therefore: (a)
   build the empirical next-symbol distribution for every length-L history
   observed >= MIN_COUNT times; (b) greedily cluster those histories into
   causal states via a chi-square test of distributional equivalence
   (alpha=1e-3, fixed a priori); (c) run ONE non-recursive determinism-
   repair diagnostic (see #2). This is mathematically equivalent to what
   CSSR converges to at that L for this alphabet/L_max regime, and is
   dramatically simpler/faster to implement correctly and validate in the
   time available than the full incremental algorithm.

2. Determinism is checked, not enforced by recursive splitting. A single
   diagnostic pass measures `determinism_violation_frac`: among all
   (state, next-symbol) transitions with sufficient data on both ends, the
   fraction whose resulting state is NOT the majority (mode) resulting
   state for that (state, symbol) pair. Full CSSR does recursive splitting
   to drive this to exactly zero; that recursive repair is out of scope
   here. Instead, `determinism_violation_frac > DETERMINISM_VIOLATION_MAX`
   (0.05, fixed a priori) is itself an ADDITIONAL REJECT-GATE criterion --
   more conservative than skipping the problem, not less.

3. Bayesian Structural Inference (Strelioff & Crutchfield 2014) is NOT
   reimplemented as full topology-space Bayesian model comparison (which
   would require enumerating and comparing candidate machine topologies
   via marginal-likelihood Bayes factors -- out of scope for this budget).
   What IS implemented, and is genuinely what the candidate survey
   (`phase0/PHASE0_8_SURVEY_NEW_CANDIDATES.md` section 1) asked for -- "a
   posterior-based robustness check on C_mu's point estimate" -- is
   Bayesian parameter-uncertainty propagation CONDITIONAL on the
   CSSR-selected topology: independent Dirichlet(1,...,1) priors on each
   state's outgoing state-to-state transition row, updated to a Dirichlet
   posterior from the observed transition counts, Monte Carlo sampled
   (N_BSI_SAMPLES draws), each draw's induced stationary distribution
   (Perron eigenvector) and C_mu recomputed -- giving a genuine posterior
   mean/std/95% credible interval on C_mu, run ONLY on real PRE/POST data
   (not on all 200 IAAFT surrogates -- computationally prohibitive and not
   what a "companion cross-check on the point estimate" requires).

4. L_max is selected ONCE per real segment/variant via the sweep-and-
   convergence rule (METHODOLOGY_NOTE.md), then held FIXED when computing
   IAAFT/bootstrap surrogates for that segment/variant -- re-sweeping L for
   every one of 200 surrogates would be computationally prohibitive and is
   not required by the methodology note (L_max is a property of R_lambda,
   fixed once the real data has determined it, exactly as median/tercile
   thresholds are fixed once computed and then applied identically to
   surrogates elsewhere in this line).
============================================================================
"""
import math
from collections import Counter, defaultdict

import numpy as np
from scipy import stats

# ---- fixed constants (METHODOLOGY_NOTE.md -- identical for every domain
# this pipeline is ever applied to; no per-domain tuning) ----
MIN_N_SEGMENT = 100            # computability floor (larger than LZC's 50:
                                # CSSR needs enough data per history)
MAX_N_PER_SEGMENT = 5000       # subsampling cap (benchmark-justified below)
N_SURROGATES = 200             # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50               # IAAFT iterations per surrogate
SEED = 12345

L_MAX_GRID = list(range(1, 9))  # L in {1,...,8}, per METHODOLOGY_NOTE.md
ALPHA_CSSR = 1e-3               # CSSR causal-state equivalence test, fixed a priori
MIN_COUNT_PER_HISTORY = 10      # floor below which a history's conditional
                                 # distribution is not trusted / tested
DETERMINISM_VIOLATION_MAX = 0.05  # additional reject-gate criterion, gap #2 above
N_STABLE_STEPS = 2              # consecutive equal-n_states steps required
                                 # for the L_max convergence rule
N_BSI_SAMPLES = 2000            # posterior Monte Carlo draws for the BSI companion


# --------------------------------------------------------------------------
# Gap: subsampling (same convention as lzc_common.py/pe_common.py/etc.)
# --------------------------------------------------------------------------

def subsample_segment(x, max_n=MAX_N_PER_SEGMENT):
    """Uniform-stride decimation to at most `max_n` samples."""
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
# R_lambda symbolization: median binarization (primary) and tertile ternary
# quantization (companion), each re-estimated from its OWN segment. Reuses
# the SAME rule already audited in lempel_ziv_complexity/analysis/lzc_common.py
# (per METHODOLOGY_NOTE.md instruction), reimplemented self-contained here.
# --------------------------------------------------------------------------

def median_binarize(x):
    """s(i) = 0 if x(i) < median(X), s(i) = 1 if x(i) >= median(X)
    (Aboy, Hornero, Abasolo & Alvarez 2006). Median computed from `x`
    itself (this segment only)."""
    x = np.asarray(x, dtype=float)
    med = np.median(x)
    return (x >= med).astype(np.int64)


def ternary_quantize(x):
    """Tertile-based ternary quantization (Kamath 2016): thresholds are
    the 1/3 and 2/3 empirical quantiles of `x` itself (this segment
    only)."""
    x = np.asarray(x, dtype=float)
    q1, q2 = np.quantile(x, [1.0 / 3.0, 2.0 / 3.0])
    symbols = np.zeros(len(x), dtype=np.int64)
    symbols[(x >= q1) & (x < q2)] = 1
    symbols[x >= q2] = 2
    return symbols


# --------------------------------------------------------------------------
# Vectorized sliding-window history encoding (base-K digit packing).
# --------------------------------------------------------------------------

def _sliding_hist_codes(s, L, K):
    """For symbol array `s` (values in {0,...,K-1}) and history length L,
    return (codes, next_syms): codes[i] = base-K integer encoding of the
    length-L window s[i:i+L] (s[i] = OLDEST symbol in the window, highest
    place value; s[i+L-1] = most recent, lowest place value), and
    next_syms[i] = s[i+L] (the symbol immediately following that window).
    Both arrays have length n-L (n=len(s)). Fully vectorized (O(n*L))."""
    s = np.asarray(s, dtype=np.int64)
    n = len(s)
    if n <= L:
        return np.array([], dtype=np.int64), np.array([], dtype=np.int64)
    n_usable = n - L
    codes = np.zeros(n_usable, dtype=np.int64)
    for j in range(L):
        weight = K ** (L - 1 - j)
        codes += s[j:j + n_usable] * weight
    next_syms = s[L:L + n_usable]
    return codes, next_syms


def _shift_code(code, next_sym, L, K):
    """Given a length-L history code and an observed next symbol, return
    the code of the resulting length-L history (drop oldest symbol,
    append next_sym as the newest) -- vectorized over arrays."""
    return (code % (K ** (L - 1))) * K + next_sym


def _build_count_table(codes, next_syms, K, L):
    """table[code, symbol] = observed count of `symbol` immediately after
    history `code`, for code in [0, K^L)."""
    n_hist = K ** L
    combo = codes * K + next_syms
    counts_flat = np.bincount(combo, minlength=n_hist * K)
    return counts_flat.reshape(n_hist, K)


# --------------------------------------------------------------------------
# CSSR-style causal-state clustering at a FIXED history length L (see scope
# decision #1 in the module docstring).
# --------------------------------------------------------------------------

def _chi2_equivalent(c1, c2, alpha):
    """Chi-square test of homogeneity between two next-symbol count
    vectors (over the same alphabet). Returns True (statistically
    indistinguishable -> same causal state) if p >= alpha."""
    table = np.vstack([c1, c2]).astype(np.int64)
    if table.sum() == 0:
        return True
    try:
        _, p, _, _ = stats.chi2_contingency(table)
    except ValueError:
        # degenerate contingency table (e.g. an all-zero row/column) --
        # cannot reject equivalence, treat as indistinguishable.
        return True
    return bool(p >= alpha)


def cssr_fixed_L(symbols, alphabet_size, L, alpha=ALPHA_CSSR,
                  min_count=MIN_COUNT_PER_HISTORY):
    """Cluster all length-L histories with count>=min_count into causal
    states via chi-square distributional equivalence (greedy, order by
    descending count -- most-reliable histories seed clusters first), then
    run the determinism-violation diagnostic (scope decision #2).

    Returns a dict:
      status: "ok" or "insufficient_samples"
      n_states, n_sufficient_histories, n_total_histories_observed,
      frac_occurrences_excluded (occurrences whose history never reached
          min_count, therefore excluded from the causal-state model),
      determinism_violation_frac,
      pi_s (occurrence-fraction stationary distribution, length n_states),
      C_mu (bits), h_mu (bits),
      cluster_next_symbol_counts (n_states x K array, for BSI/diagnostics),
      transition_counts (n_states x n_states array, state-to-state, used
          by the BSI companion),
      hist_to_cluster (dict code->cluster id, for surrogate-recomputation
          reuse is NOT assumed -- each call is self-contained).
    """
    K = alphabet_size
    s = np.asarray(symbols, dtype=np.int64)
    n = len(s)
    if n <= L + 1:
        return {"status": "insufficient_samples", "n": int(n), "L": int(L)}

    codes, next_syms = _sliding_hist_codes(s, L, K)
    table = _build_count_table(codes, next_syms, K, L)
    totals = table.sum(axis=1)

    sufficient_codes = np.nonzero(totals >= min_count)[0]
    if len(sufficient_codes) == 0:
        return {"status": "insufficient_samples", "n": int(n), "L": int(L)}

    order = sufficient_codes[np.argsort(-totals[sufficient_codes])]

    clusters = []  # list of {"counts": np.array(K), "codes": [int,...]}
    hist_to_cluster = {}
    for code in order:
        c = table[code]
        assigned = None
        for ci, cl in enumerate(clusters):
            if _chi2_equivalent(c, cl["counts"], alpha):
                assigned = ci
                break
        if assigned is None:
            clusters.append({"counts": c.copy(), "codes": [int(code)]})
            assigned = len(clusters) - 1
        else:
            clusters[assigned]["counts"] = clusters[assigned]["counts"] + c
            clusters[assigned]["codes"].append(int(code))
        hist_to_cluster[int(code)] = assigned

    n_states = len(clusters)

    # occurrence classification: every position gets a cluster id if its
    # history is sufficient, else excluded (-1).
    code_to_cluster_arr = -np.ones(K ** L, dtype=np.int64)
    for code, ci in hist_to_cluster.items():
        code_to_cluster_arr[code] = ci
    occ_cluster = code_to_cluster_arr[codes]
    valid_mask = occ_cluster >= 0
    n_valid = int(valid_mask.sum())
    frac_excluded = 1.0 - (n_valid / len(codes)) if len(codes) > 0 else 1.0

    if n_valid == 0:
        return {"status": "insufficient_samples", "n": int(n), "L": int(L)}

    # occurrence-fraction stationary distribution (simple, always defined)
    counts_per_state = np.bincount(occ_cluster[valid_mask], minlength=n_states)
    pi_s = counts_per_state / counts_per_state.sum()

    # C_mu: Shannon entropy (bits) of pi_s
    nz = pi_s[pi_s > 0]
    C_mu = float(-np.sum(nz * np.log2(nz)))

    # h_mu: entropy rate = sum_s pi_s * H(next_symbol | state=s)
    h_per_state = np.zeros(n_states)
    for ci, cl in enumerate(clusters):
        cc = cl["counts"].astype(float)
        tot = cc.sum()
        if tot > 0:
            p = cc / tot
            p_nz = p[p > 0]
            h_per_state[ci] = -np.sum(p_nz * np.log2(p_nz))
    h_mu = float(np.sum(pi_s * h_per_state))

    # state-to-state transition counts (for BSI) + determinism-violation
    # diagnostic (scope decision #2): both/either endpoint may be
    # insufficient -- only occurrences with BOTH the origin and the
    # resulting history classified (sufficient) are used.
    result_codes = _shift_code(codes, next_syms, L, K)
    result_cluster = code_to_cluster_arr[result_codes]
    both_valid = valid_mask & (result_cluster >= 0)

    transition_counts = np.zeros((n_states, n_states), dtype=np.int64)
    if both_valid.any():
        origin = occ_cluster[both_valid]
        dest = result_cluster[both_valid]
        flat = origin * n_states + dest
        flat_counts = np.bincount(flat, minlength=n_states * n_states)
        transition_counts = flat_counts.reshape(n_states, n_states)

    # determinism_violation_frac: group by (state, next_symbol), find the
    # majority resulting state, count occurrences that disagree with it.
    determinism_violation_frac = 0.0
    if both_valid.any():
        origin = occ_cluster[both_valid]
        nsym = next_syms[both_valid]
        dest = result_cluster[both_valid]
        groups = defaultdict(Counter)
        for o, a, d in zip(origin.tolist(), nsym.tolist(), dest.tolist()):
            groups[(o, a)][d] += 1
        n_total_grouped = 0
        n_mismatch = 0
        for key, ctr in groups.items():
            total = sum(ctr.values())
            majority = max(ctr.values())
            n_total_grouped += total
            n_mismatch += (total - majority)
        determinism_violation_frac = (n_mismatch / n_total_grouped) if n_total_grouped > 0 else 0.0

    return {
        "status": "ok",
        "n": int(n), "L": int(L), "alphabet_size": int(K),
        "n_states": int(n_states),
        "n_sufficient_histories": int(len(sufficient_codes)),
        "n_total_histories_observed": int(np.count_nonzero(totals > 0)),
        "n_occurrences_total": int(len(codes)),
        "n_occurrences_valid": int(n_valid),
        "frac_occurrences_excluded": float(frac_excluded),
        "determinism_violation_frac": float(determinism_violation_frac),
        "pi_s": pi_s.tolist(),
        "C_mu": C_mu,
        "h_mu": h_mu,
        "cluster_next_symbol_counts": [cl["counts"].tolist() for cl in clusters],
        "transition_counts": transition_counts.tolist(),
    }


# --------------------------------------------------------------------------
# L_max sweep + data-driven convergence selection + mandatory reject gate
# (METHODOLOGY_NOTE.md: "sweep L_max over {1,...,8} and select the smallest
# value beyond which the number of inferred causal states stops growing").
# --------------------------------------------------------------------------

def select_Lmax_and_reconstruct(symbols, alphabet_size, L_grid=L_MAX_GRID,
                                 alpha=ALPHA_CSSR, min_count=MIN_COUNT_PER_HISTORY,
                                 n_stable=N_STABLE_STEPS,
                                 determinism_max=DETERMINISM_VIOLATION_MAX,
                                 min_L_for_selection=2):
    """Run cssr_fixed_L across L_grid, select the smallest L such that
    n_states(L) == n_states(L+1) == ... for `n_stable` consecutive steps
    (BIC/AIC-style order-selection analogue, per METHODOLOGY_NOTE.md -- NOT
    a fixed constant, NOT visual). Applies the MANDATORY reject gate:
      - DEGENERATE: n_states at the selected L == 1
      - NOT_CONVERGENT: the n_states(L) curve never stabilizes across the
        WHOLE grid (no run of `n_stable` consecutive equal values found)
      - NOT_DETERMINISTIC: determinism_violation_frac at the selected L
        exceeds `determinism_max` (scope decision #2 above)
    Returns a dict with the full sweep (`sweep`: list of per-L results),
    `L_selected`, `verdict` ("OK" or one of the three reject codes above),
    and (if verdict=="OK") the selected L's full cssr_fixed_L result under
    `reconstruction`.

    `min_L_for_selection=2` (THE ONE PRE-AUTHORIZED CORRECTION, applied
    during synthetic validation, documented in VALIDATION_NOTE.md -- NOT a
    post-hoc tuning after real data): L=1 is EXCLUDED from the stability
    search (though still computed and reported in the sweep curve for
    transparency). Reason, discovered by the mandatory code-correctness/
    positive-control diagnostics: for median-binary (K=2) and tercile-
    ternary (K=3) R_lambda specifically, whenever the L=1 histories do not
    merge into one cluster, pi_s at L=1 is MATHEMATICALLY FORCED to equal
    R_lambda's own construction marginal (exactly 0.5/0.5 for the median
    split, exactly 1/3 each for tercile split) -- by definition of what a
    median/tercile threshold IS, independent of the segment's actual
    dynamics. C_mu at L=1 therefore collapses to a TRIVIAL, CONSTANT value
    (log2(K)) whenever n_states(1)==K, carrying ZERO discriminating
    information about real vs. surrogate dynamics -- confirmed empirically
    in `validate_synthetic.py` (both a real AR(1) segment and its IAAFT
    surrogates gave IDENTICAL C_mu=log2(K) at L=1, std=0.0 across 30
    surrogates). This is a genuine design problem in the naive reading of
    "smallest L where n_states stops growing" (L=1 trivially "stops
    growing" the moment histories stop merging, for a reason that has
    nothing to do with genuine memory), not a bug in the arithmetic.
    """
    sweep = []
    for L in L_grid:
        res = cssr_fixed_L(symbols, alphabet_size, L, alpha=alpha, min_count=min_count)
        sweep.append(res)

    n_states_curve = [r.get("n_states") if r.get("status") == "ok" else None for r in sweep]

    start_idx = 0
    for i, L in enumerate(L_grid):
        if L >= min_L_for_selection:
            start_idx = i
            break

    L_selected = None
    for i in range(start_idx, len(L_grid) - n_stable + 1):
        window = n_states_curve[i:i + n_stable]
        if all(v is not None for v in window) and len(set(window)) == 1:
            L_selected = L_grid[i]
            break

    if L_selected is None:
        # curve never stabilized within the grid
        return {
            "sweep": sweep, "n_states_curve": n_states_curve,
            "L_selected": None, "verdict": "NOT_CONVERGENT",
        }

    idx = L_grid.index(L_selected)
    reconstruction = sweep[idx]

    if reconstruction.get("status") != "ok":
        return {
            "sweep": sweep, "n_states_curve": n_states_curve,
            "L_selected": L_selected, "verdict": "NOT_CONVERGENT",
        }

    if reconstruction["n_states"] == 1:
        return {
            "sweep": sweep, "n_states_curve": n_states_curve,
            "L_selected": L_selected, "verdict": "DEGENERATE",
            "reconstruction": reconstruction,
        }

    if reconstruction["determinism_violation_frac"] > determinism_max:
        return {
            "sweep": sweep, "n_states_curve": n_states_curve,
            "L_selected": L_selected, "verdict": "NOT_DETERMINISTIC",
            "reconstruction": reconstruction,
        }

    return {
        "sweep": sweep, "n_states_curve": n_states_curve,
        "L_selected": L_selected, "verdict": "OK",
        "reconstruction": reconstruction,
    }


# --------------------------------------------------------------------------
# Bayesian Structural Inference companion (scope decision #3): posterior
# uncertainty on C_mu, CONDITIONAL on the CSSR-selected topology, via
# Dirichlet-multinomial conjugate updating of the state-to-state transition
# rows, Monte Carlo sampled. Run ONLY on real PRE/POST data (diagnostic).
# --------------------------------------------------------------------------

def bsi_credible_interval(reconstruction, n_samples=N_BSI_SAMPLES, seed=SEED):
    """Posterior mean/std/2.5%/97.5% credible interval for C_mu, given a
    FIXED topology (n_states, transition_counts) from cssr_fixed_L.
    Independent Dirichlet(1,...,1) prior per state's outgoing row;
    posterior = Dirichlet(1 + counts); each MC draw's induced stationary
    distribution (leading left eigenvector of the sampled row-stochastic
    transition matrix) gives one posterior C_mu sample."""
    n_states = reconstruction["n_states"]
    T = np.asarray(reconstruction["transition_counts"], dtype=float)
    rng = np.random.default_rng(seed)

    if n_states == 1:
        return {"status": "degenerate_single_state", "C_mu_posterior_mean": 0.0,
                "C_mu_posterior_std": 0.0, "C_mu_ci_low": 0.0, "C_mu_ci_high": 0.0,
                "n_samples": 0}

    samples = []
    for _ in range(n_samples):
        P = np.zeros((n_states, n_states))
        for i in range(n_states):
            alpha_post = 1.0 + T[i]
            if alpha_post.sum() == n_states:
                # no transition data at all for this state (all-prior) --
                # sample from the flat Dirichlet(1,...,1) prior itself
                pass
            P[i] = rng.dirichlet(alpha_post)
        pi = _stationary_distribution(P)
        if pi is None:
            continue
        nz = pi[pi > 1e-15]
        C_mu_sample = float(-np.sum(nz * np.log2(nz)))
        samples.append(C_mu_sample)

    if len(samples) == 0:
        return {"status": "failed", "C_mu_posterior_mean": None,
                "C_mu_posterior_std": None, "C_mu_ci_low": None,
                "C_mu_ci_high": None, "n_samples": 0}

    samples = np.array(samples)
    return {
        "status": "ok",
        "C_mu_posterior_mean": float(np.mean(samples)),
        "C_mu_posterior_std": float(np.std(samples)),
        "C_mu_ci_low": float(np.percentile(samples, 2.5)),
        "C_mu_ci_high": float(np.percentile(samples, 97.5)),
        "n_samples": int(len(samples)),
    }


def _stationary_distribution(P, max_iter=10000, tol=1e-12):
    """Stationary distribution of a row-stochastic matrix P via power
    iteration (robust to small numerical asymmetries; avoids complex-
    eigenvalue edge cases from np.linalg.eig on small stochastic
    matrices). Returns None if it fails to converge or P is degenerate."""
    n = P.shape[0]
    if n == 1:
        return np.array([1.0])
    row_sums = P.sum(axis=1)
    # rows with zero data (all-prior Dirichlet already normalizes to
    # sum 1 via rng.dirichlet, so this should not trigger in practice)
    row_sums[row_sums == 0] = 1.0
    P = P / row_sums[:, None]
    pi = np.full(n, 1.0 / n)
    for _ in range(max_iter):
        pi_next = pi @ P
        if np.sum(np.abs(pi_next - pi)) < tol:
            pi = pi_next
            break
        pi = pi_next
    pi = np.clip(pi, 0, None)
    s = pi.sum()
    if s <= 0:
        return None
    return pi / s


# --------------------------------------------------------------------------
# IAAFT surrogates (Schreiber & Schmitz 1996) -- self-contained
# reimplementation, same algorithm already used elsewhere in this lab.
# --------------------------------------------------------------------------

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate."""
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


# --------------------------------------------------------------------------
# Full per-variant (median / ternary) transition-test pipeline.
# --------------------------------------------------------------------------

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def _two_tailed_p(real_delta, surrogate_deltas):
    if real_delta is None or len(surrogate_deltas) == 0:
        return None
    return float(np.mean(np.abs(np.asarray(surrogate_deltas)) >= abs(real_delta)))


def run_variant_analysis(pre_raw, post_raw, symbolize_fn, alphabet_size,
                          n_surrogates=N_SURROGATES, n_iter=N_IAAFT_ITER,
                          seed=SEED, run_bsi=True):
    """Full pipeline for ONE symbolization variant (median or ternary):
    (1) select L_max + reconstruct causal states on REAL PRE and REAL POST
        independently (each with its own re-estimated threshold, per
        R_lambda's "reestimado por segmento" convention);
    (2) mandatory reject gate on both PRE and POST reconstructions;
    (3) if both pass, BSI companion credible interval on real PRE/POST
        (diagnostic only, scope decision #3);
    (4) IAAFT surrogates (PRE and POST generated independently from their
        OWN real continuous segment, per this lab's convention), each
        symbolized and reconstructed at the segment's OWN FIXED L_selected
        (scope decision #4) to build the null distribution of
        Delta_C_mu / Delta_h_mu.

    Returns a dict with status "ok" (both PRE/POST pass the reject gate)
    or "not_computable" (either fails -- WHICH gate failed for which
    segment is reported explicitly, honest NOT_COMPUTABLE convention
    already used elsewhere in this line, e.g. dmd_koopman).
    """
    pre_raw = np.asarray(pre_raw, dtype=float)
    post_raw = np.asarray(post_raw, dtype=float)

    if len(pre_raw) < MIN_N_SEGMENT or len(post_raw) < MIN_N_SEGMENT:
        return {"status": "insufficient_samples",
                "n_pre": int(len(pre_raw)), "n_post": int(len(post_raw))}

    pre_sym = symbolize_fn(pre_raw)
    post_sym = symbolize_fn(post_raw)

    pre_sweep = select_Lmax_and_reconstruct(pre_sym, alphabet_size)
    post_sweep = select_Lmax_and_reconstruct(post_sym, alphabet_size)

    if pre_sweep["verdict"] != "OK" or post_sweep["verdict"] != "OK":
        return {
            "status": "not_computable",
            "pre_verdict": pre_sweep["verdict"], "post_verdict": post_sweep["verdict"],
            "pre_L_selected": pre_sweep.get("L_selected"),
            "post_L_selected": post_sweep.get("L_selected"),
            "pre_n_states_curve": pre_sweep["n_states_curve"],
            "post_n_states_curve": post_sweep["n_states_curve"],
        }

    pre_recon = pre_sweep["reconstruction"]
    post_recon = post_sweep["reconstruction"]

    C_mu_pre, C_mu_post = pre_recon["C_mu"], post_recon["C_mu"]
    h_mu_pre, h_mu_post = pre_recon["h_mu"], post_recon["h_mu"]
    delta_C_mu_real = _delta(C_mu_post, C_mu_pre)
    delta_h_mu_real = _delta(h_mu_post, h_mu_pre)

    bsi_pre = bsi_credible_interval(pre_recon, seed=seed) if run_bsi else None
    bsi_post = bsi_credible_interval(post_recon, seed=seed + 1) if run_bsi else None

    L_pre, L_post = pre_sweep["L_selected"], post_sweep["L_selected"]

    rng = np.random.default_rng(seed)
    surr_delta_C_mu, surr_delta_h_mu = [], []
    n_undef = 0
    n_surr_not_computable = 0
    for _ in range(n_surrogates):
        surr_pre_raw = iaaft_surrogate(pre_raw, n_iter=n_iter, rng=rng)
        surr_post_raw = iaaft_surrogate(post_raw, n_iter=n_iter, rng=rng)
        surr_pre_sym = symbolize_fn(surr_pre_raw)
        surr_post_sym = symbolize_fn(surr_post_raw)

        r_pre = cssr_fixed_L(surr_pre_sym, alphabet_size, L_pre)
        r_post = cssr_fixed_L(surr_post_sym, alphabet_size, L_post)

        if r_pre.get("status") != "ok" or r_post.get("status") != "ok":
            n_surr_not_computable += 1
            n_undef += 1
            continue

        d_c = _delta(r_post["C_mu"], r_pre["C_mu"])
        d_h = _delta(r_post["h_mu"], r_pre["h_mu"])
        if d_c is None or d_h is None:
            n_undef += 1
            continue
        surr_delta_C_mu.append(d_c)
        surr_delta_h_mu.append(d_h)

    p_C_mu = _two_tailed_p(delta_C_mu_real, surr_delta_C_mu)
    p_h_mu = _two_tailed_p(delta_h_mu_real, surr_delta_h_mu)

    return {
        "status": "ok",
        "L_selected_pre": L_pre, "L_selected_post": L_post,
        "pre_n_states_curve": pre_sweep["n_states_curve"],
        "post_n_states_curve": post_sweep["n_states_curve"],
        "n_states_pre": pre_recon["n_states"], "n_states_post": post_recon["n_states"],
        "determinism_violation_frac_pre": pre_recon["determinism_violation_frac"],
        "determinism_violation_frac_post": post_recon["determinism_violation_frac"],
        "frac_occurrences_excluded_pre": pre_recon["frac_occurrences_excluded"],
        "frac_occurrences_excluded_post": post_recon["frac_occurrences_excluded"],
        "C_mu_pre": C_mu_pre, "C_mu_post": C_mu_post, "delta_C_mu": delta_C_mu_real,
        "h_mu_pre": h_mu_pre, "h_mu_post": h_mu_post, "delta_h_mu": delta_h_mu_real,
        "p_C_mu": p_C_mu, "p_h_mu": p_h_mu,
        "bsi_pre": bsi_pre, "bsi_post": bsi_post,
        "surrogate_delta_C_mu_mean": float(np.mean(surr_delta_C_mu)) if surr_delta_C_mu else None,
        "surrogate_delta_C_mu_std": float(np.std(surr_delta_C_mu)) if surr_delta_C_mu else None,
        "surrogate_delta_h_mu_mean": float(np.mean(surr_delta_h_mu)) if surr_delta_h_mu else None,
        "surrogate_delta_h_mu_std": float(np.std(surr_delta_h_mu)) if surr_delta_h_mu else None,
        "n_surrogates_valid": int(len(surr_delta_C_mu)),
        "n_surrogates_not_computable": int(n_surr_not_computable),
        "n_surrogates_undefined": int(n_undef),
        "surrogate_delta_C_mu_deltas": [float(v) for v in surr_delta_C_mu],
        "surrogate_delta_h_mu_deltas": [float(v) for v in surr_delta_h_mu],
    }


def run_bootstrap_variant_analysis(pre_raw, post_raw, symbolize_fn, alphabet_size,
                                    L_pre, L_post, n_bootstrap=N_SURROGATES,
                                    seed=SEED, block_frac=1.0 / 20.0):
    """Pre-authorized moving-block-bootstrap fallback (Kunsch 1989),
    same convention as elsewhere in this lab -- NOT part of the default
    pipeline, only invoked if synthetic validation shows low IAAFT power
    for a channel. `L_pre`/`L_post` are the ALREADY-SELECTED L's from the
    real-data run_variant_analysis call (not re-swept)."""
    pre_raw = np.asarray(pre_raw, dtype=float)
    post_raw = np.asarray(post_raw, dtype=float)
    rng = np.random.default_rng(seed)

    L_pre_block = max(int(len(pre_raw) * block_frac), 5)
    L_post_block = max(int(len(post_raw) * block_frac), 5)

    surr_delta_C_mu, surr_delta_h_mu = [], []
    n_undef = 0
    for _ in range(n_bootstrap):
        b_pre_raw = moving_block_bootstrap_resample(pre_raw, L_pre_block, rng)
        b_post_raw = moving_block_bootstrap_resample(post_raw, L_post_block, rng)
        b_pre_sym = symbolize_fn(b_pre_raw)
        b_post_sym = symbolize_fn(b_post_raw)
        r_pre = cssr_fixed_L(b_pre_sym, alphabet_size, L_pre)
        r_post = cssr_fixed_L(b_post_sym, alphabet_size, L_post)
        if r_pre.get("status") != "ok" or r_post.get("status") != "ok":
            n_undef += 1
            continue
        d_c = _delta(r_post["C_mu"], r_pre["C_mu"])
        d_h = _delta(r_post["h_mu"], r_pre["h_mu"])
        if d_c is None or d_h is None:
            n_undef += 1
            continue
        surr_delta_C_mu.append(d_c)
        surr_delta_h_mu.append(d_h)

    return {
        "bootstrap_delta_C_mu_mean": float(np.mean(surr_delta_C_mu)) if surr_delta_C_mu else None,
        "bootstrap_delta_C_mu_std": float(np.std(surr_delta_C_mu)) if surr_delta_C_mu else None,
        "bootstrap_delta_h_mu_mean": float(np.mean(surr_delta_h_mu)) if surr_delta_h_mu else None,
        "bootstrap_delta_h_mu_std": float(np.std(surr_delta_h_mu)) if surr_delta_h_mu else None,
        "n_bootstrap_valid": int(len(surr_delta_C_mu)),
        "n_bootstrap_undefined": int(n_undef),
        "bootstrap_delta_C_mu_deltas": [float(v) for v in surr_delta_C_mu],
        "bootstrap_delta_h_mu_deltas": [float(v) for v in surr_delta_h_mu],
    }


def run_em_analysis(pre_series, post_series, n_surrogates=N_SURROGATES,
                     n_iter=N_IAAFT_ITER, seed=SEED, max_n=MAX_N_PER_SEGMENT,
                     run_bsi=True):
    """Top-level entry point: run BOTH R_lambda variants (median binary,
    ternary) on one PRE/POST pair, per METHODOLOGY_NOTE.md. Single pipeline
    called WITHOUT modification across synthetic and real segments."""
    pre_raw = np.asarray(pre_series, dtype=float)
    post_raw = np.asarray(post_series, dtype=float)

    pre, pre_sub_info = subsample_segment(pre_raw, max_n=max_n)
    post, post_sub_info = subsample_segment(post_raw, max_n=max_n)

    config = {
        "min_n_segment": MIN_N_SEGMENT, "max_n_per_segment": max_n,
        "n_surrogates": n_surrogates, "n_iaaft_iter": n_iter, "seed": seed,
        "L_max_grid": L_MAX_GRID, "alpha_cssr": ALPHA_CSSR,
        "min_count_per_history": MIN_COUNT_PER_HISTORY,
        "determinism_violation_max": DETERMINISM_VIOLATION_MAX,
        "n_stable_steps": N_STABLE_STEPS, "n_bsi_samples": N_BSI_SAMPLES,
        "pre_subsample_info": pre_sub_info, "post_subsample_info": post_sub_info,
    }

    median_result = run_variant_analysis(pre, post, median_binarize, 2,
                                          n_surrogates=n_surrogates, n_iter=n_iter,
                                          seed=seed, run_bsi=run_bsi)
    ternary_result = run_variant_analysis(pre, post, ternary_quantize, 3,
                                           n_surrogates=n_surrogates, n_iter=n_iter,
                                           seed=seed + 1000, run_bsi=run_bsi)

    return {
        "config": config,
        "median": median_result,
        "ternary": ternary_result,
    }
