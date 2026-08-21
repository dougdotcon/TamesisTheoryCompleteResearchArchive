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
REVISION (dated in METHODOLOGY_NOTE.md's addendum, `DISC-DEC-011`): this
module now implements FULL INCREMENTAL CSSR (Shalizi & Klinkner 2004, UAI;
Shalizi, Shalizi & Crutchfield, arXiv:cs/0210025), replacing the earlier
"fixed-L causal-state clustering" simplification (scope decisions #1/#2 of
the original implementation, preserved only in the historical record --
`VALIDATION_NOTE.md`, `validate_synthetic.py`/`.json` -- and NOT in this
file). This is an implementation-completeness correction: `I(X)=C_mu`
primary / `h_mu` companion, the IAAFT+bootstrap significance protocol, and
the median/ternary R_lambda symbolization are ALL unchanged from the
original METHODOLOGY_NOTE.md -- only the causal-state reconstruction
engine underneath `R_lambda` changed.

============================================================================
SCOPE DECISIONS (documented here AND in METHODOLOGY_NOTE.md's addendum,
honestly, as engineering choices -- not hypothesis reformulations):
============================================================================

1. CSSR is now implemented as genuine INCREMENTAL growth (`cssr_incremental_
   grow`): starting from the single causal state containing the length-0
   (empty) history, history length L is grown one step at a time from 1 up
   to L_max. At each step L: (a) build the empirical next-symbol
   distribution for every length-L history observed >= MIN_COUNT_PER_HISTORY
   times; (b) for each such history, in descending-count order, test it
   FIRST against the causal state its length-(L-1) SUFFIX already belongs
   to (chi-square equivalence test, alpha=1e-3, fixed a priori) -- this is
   the step the earlier fixed-L clustering did NOT do, and is precisely
   what lets statistically-indistinguishable-but-nominally-different
   histories of different lengths (e.g. "111" and "11111", both landing in
   the SAME true causal state) merge into one state, which the earlier
   from-scratch-at-every-L clustering could never achieve; (c) if that
   fails (or the suffix itself was not itself classified), test against
   every OTHER state discovered so far at this L, and only create a new
   state if none match. This exactly implements the "grow" half of Shalizi
   & Klinkner's algorithm.

2. Determinism (unifilarity) is now ENFORCED by genuine recursive
   splitting (`_determinize`), not merely diagnosed. After the grow step at
   each L, states are iteratively split until every (state, symbol)
   transition with sufficient empirical evidence
   (>= DETERMINIZE_MIN_TRANSITION_COUNT occurrences, fixed a priori, a
   lower floor than MIN_COUNT_PER_HISTORY since per-symbol transition
   counts are finer-grained than per-history totals) leads to exactly ONE
   resulting causal state -- histories within a state that disagree on
   the resulting state for some symbol are split into separate states,
   using each history's *transition signature* (the tuple, over symbols,
   of resulting-state ids where known) as the splitting criterion, greedily
   grouped by pairwise signature compatibility (histories agreeing on every
   symbol both have evidence for), iterated to a fixed point (capped at
   MAX_DETERMINIZE_ITERS=30, fixed a priori -- exceeding the cap without
   convergence is itself folded into the NOT_DETERMINISTIC reject-gate
   criterion below, never silently accepted). `determinism_violation_frac`
   is still computed and reported (same formula as before, on real
   occurrences) as a POST-determinize sanity check -- it should be ~0 by
   construction; a nonzero value beyond DETERMINISM_VIOLATION_MAX now
   signals a genuine reconstruction problem (e.g. the iteration cap was
   hit), not an accepted-but-imperfect approximation.

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
   surrogates elsewhere in this line). UNCHANGED by this revision, except
   that "holding L fixed" for a surrogate now means growing the surrogate's
   OWN incremental CSSR from L=1 up to that fixed L (genuine CSSR is
   inherently sequential -- you cannot jump straight to L=8 without passing
   through the grow+determinize steps at L=1,...,7 first) and reading off
   the state at that L, rather than reclustering from scratch at a single L
   as the earlier implementation did.
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

DETERMINIZE_MIN_TRANSITION_COUNT = 5  # floor (fixed a priori, independent of
                                 # MIN_COUNT_PER_HISTORY) below which a
                                 # specific (history, symbol) empirical
                                 # transition is not trusted as evidence
                                 # during the unifilarity/determinize split
                                 # step -- lower than MIN_COUNT_PER_HISTORY
                                 # because per-symbol transition counts are
                                 # finer-grained than per-history totals
MAX_DETERMINIZE_ITERS = 30      # cap on recursive-splitting iterations per
                                 # history length L; exceeding it without
                                 # convergence feeds the NOT_DETERMINISTIC
                                 # reject gate, never silently accepted


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
# Full incremental CSSR (Shalizi & Klinkner 2004, UAI; Shalizi, Shalizi &
# Crutchfield, arXiv:cs/0210025) -- replaces the earlier fixed-L clustering
# (see the REVISION note and scope decisions #1/#2 in the module docstring).
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


def _shift_code_scalar(code, next_sym, L, K):
    """Scalar version of `_shift_code` (drop the oldest symbol of a
    length-L history, append `next_sym` as the newest -- the resulting
    history code, also length L)."""
    return (code % (K ** (L - 1))) * K + next_sym


def _determinize(code_to_state, table, L, K,
                  min_transition_count=DETERMINIZE_MIN_TRANSITION_COUNT,
                  max_iters=MAX_DETERMINIZE_ITERS):
    """Recursive causal-state splitting until every (state, symbol)
    transition with sufficient empirical evidence (>=min_transition_count
    occurrences of that exact history->symbol pair) leads to exactly ONE
    resulting state (unifilarity) -- CSSR's determinize step, genuinely
    enforced (scope decision #2 of the module docstring), not merely
    diagnosed. `code_to_state`: length-K^L array, state id per history code
    (-1 = not classified). `table`: K^L x K next-symbol count table for
    this L. Returns (new_code_to_state, n_iterations_used, converged bool).
    """
    code_to_state = code_to_state.copy()
    classified_codes = np.nonzero(code_to_state >= 0)[0]
    if len(classified_codes) == 0:
        return code_to_state, 0, True

    n_iters = 0
    converged = False
    for it in range(max_iters):
        n_iters = it + 1
        members_by_state = defaultdict(list)
        for code in classified_codes:
            members_by_state[int(code_to_state[code])].append(int(code))

        changed = False
        new_assignment = {}
        next_id = 0
        # deterministic order: by ascending old state id
        for old_sid in sorted(members_by_state.keys()):
            codes_list = sorted(members_by_state[old_sid], key=lambda c: -table[c].sum())
            groups = []  # [{"sig": {a: target_state}, "codes": [...]}]
            for code in codes_list:
                sig = {}
                for a in range(K):
                    if table[code, a] >= min_transition_count:
                        shifted = _shift_code_scalar(code, a, L, K)
                        if 0 <= shifted < len(code_to_state) and code_to_state[shifted] >= 0:
                            sig[a] = int(code_to_state[shifted])
                placed = False
                for g in groups:
                    compatible = True
                    for a, t in sig.items():
                        if a in g["sig"] and g["sig"][a] != t:
                            compatible = False
                            break
                    if compatible:
                        g["sig"].update(sig)
                        g["codes"].append(code)
                        placed = True
                        break
                if not placed:
                    groups.append({"sig": dict(sig), "codes": [code]})
            if len(groups) > 1:
                changed = True
            for g in groups:
                for code in g["codes"]:
                    new_assignment[code] = next_id
                next_id += 1

        for code, sid in new_assignment.items():
            code_to_state[code] = sid

        if not changed:
            converged = True
            break

    return code_to_state, n_iters, converged


def _determinism_violation_frac_occ(codes, next_syms, code_to_state, L, K):
    """Post-determinize sanity check (same formula as the pre-revision
    diagnostic, computed on ACTUAL occurrences, not just the count table):
    among all (state, next-symbol) transitions with sufficient data on
    both ends, the fraction whose resulting state is NOT the majority
    (mode) resulting state for that (state, symbol) pair. Should be ~0
    after a converged `_determinize` call; a nonzero value here signals a
    genuine reconstruction problem (e.g. the determinize iteration cap was
    hit), which feeds the NOT_DETERMINISTIC reject gate."""
    occ_cluster = code_to_state[codes]
    valid_mask = occ_cluster >= 0
    if not valid_mask.any():
        return 0.0
    result_codes = _shift_code(codes, next_syms, L, K)
    result_cluster = code_to_state[result_codes]
    both_valid = valid_mask & (result_cluster >= 0)
    if not both_valid.any():
        return 0.0
    origin = occ_cluster[both_valid]
    nsym = next_syms[both_valid]
    dest = result_cluster[both_valid]
    groups = defaultdict(Counter)
    for o, a, d in zip(origin.tolist(), nsym.tolist(), dest.tolist()):
        groups[(o, a)][d] += 1
    n_total = 0
    n_mismatch = 0
    for key, ctr in groups.items():
        total = sum(ctr.values())
        majority = max(ctr.values())
        n_total += total
        n_mismatch += (total - majority)
    return (n_mismatch / n_total) if n_total > 0 else 0.0


def cssr_incremental_grow(symbols, alphabet_size, L_max, alpha=ALPHA_CSSR,
                           min_count=MIN_COUNT_PER_HISTORY):
    """Full incremental CSSR: grow causal states from the single L=0 state
    (all histories) up to L_max, one history length at a time.

    At each L=1,...,L_max:
      (1) GROW -- for every length-L history observed >=min_count times, in
          descending-count order: test it FIRST against the causal state
          its length-(L-1) SUFFIX already belongs to (the state's L-1
          aggregate next-symbol distribution); if that state has not yet
          been "claimed" this round by an earlier history, seed a new
          current-round state for it and test against the OLD (L-1)
          aggregate directly. If the suffix test fails (or the suffix
          itself was not classified at L-1), fall back to testing against
          every OTHER state discovered so far this round, and only create a
          brand-new state if none match (chi-square equivalence,
          alpha=1e-3, fixed a priori).
      (2) DETERMINIZE -- recursively split states (`_determinize`) until
          unifilar.

    Returns {"sweep": [per-L summary dicts, L=1..L_max], "per_L": {L: {...}}}
    where `per_L[L]` carries everything needed to finalize a reconstruction
    (pi_s/C_mu/h_mu/transition_counts) at that L without re-growing.
    """
    K = alphabet_size
    s = np.asarray(symbols, dtype=np.int64)
    n = len(s)

    global_counts = np.bincount(s, minlength=K).astype(np.int64) if n > 0 else np.zeros(K, dtype=np.int64)
    prev_code_to_state = np.zeros(1, dtype=np.int64)   # L=0: 1 history (empty), state 0
    prev_states_counts = [global_counts]

    sweep = []
    per_L = {}

    for L in range(1, L_max + 1):
        if n <= L:
            sweep.append({"L": int(L), "status": "insufficient_samples", "n_states": None,
                           "determinism_violation_frac": None})
            continue

        codes, next_syms = _sliding_hist_codes(s, L, K)
        table = _build_count_table(codes, next_syms, K, L)
        totals = table.sum(axis=1)
        n_hist_total = K ** L

        sufficient = np.nonzero(totals >= min_count)[0]
        if len(sufficient) == 0:
            sweep.append({"L": int(L), "status": "insufficient_samples", "n_states": None,
                           "determinism_violation_frac": None})
            continue

        order = sufficient[np.argsort(-totals[sufficient])]

        # ---- (1) GROW ----
        code_to_state = -np.ones(n_hist_total, dtype=np.int64)
        current_counts = []          # list of np.array(K), this round's aggregates
        state_of_parent = {}         # old (L-1) state id -> this-round state id

        for code in order:
            code = int(code)
            c = table[code]
            suffix = (code % (K ** (L - 1))) if L > 1 else 0
            parent = None
            if 0 <= suffix < len(prev_code_to_state):
                p = int(prev_code_to_state[suffix])
                if p >= 0:
                    parent = p

            assigned = None
            if parent is not None:
                if parent in state_of_parent:
                    csid = state_of_parent[parent]
                    if _chi2_equivalent(c, current_counts[csid], alpha):
                        assigned = csid
                elif parent < len(prev_states_counts) and _chi2_equivalent(c, prev_states_counts[parent], alpha):
                    csid = len(current_counts)
                    current_counts.append(np.zeros(K, dtype=np.int64))
                    state_of_parent[parent] = csid
                    assigned = csid

            if assigned is None:
                for csid in range(len(current_counts)):
                    if _chi2_equivalent(c, current_counts[csid], alpha):
                        assigned = csid
                        break

            if assigned is None:
                assigned = len(current_counts)
                current_counts.append(np.zeros(K, dtype=np.int64))
                if parent is not None and parent not in state_of_parent:
                    state_of_parent[parent] = assigned

            current_counts[assigned] = current_counts[assigned] + c
            code_to_state[code] = assigned

        # ---- (2) DETERMINIZE ----
        code_to_state, n_det_iters, det_converged = _determinize(code_to_state, table, L, K)

        classified = np.nonzero(code_to_state >= 0)[0]
        if len(classified) == 0:
            sweep.append({"L": int(L), "status": "insufficient_samples", "n_states": None,
                           "determinism_violation_frac": None})
            continue

        n_states = int(code_to_state[classified].max()) + 1
        states_counts = [np.zeros(K, dtype=np.int64) for _ in range(n_states)]
        for code in classified.tolist():
            states_counts[int(code_to_state[code])] = states_counts[int(code_to_state[code])] + table[code]

        dvf = _determinism_violation_frac_occ(codes, next_syms, code_to_state, L, K)

        sweep.append({
            "L": int(L), "status": "ok", "n_states": int(n_states),
            "n_sufficient_histories": int(len(sufficient)),
            "n_total_histories_observed": int(np.count_nonzero(totals > 0)),
            "determinism_violation_frac": float(dvf),
            "determinize_iterations": int(n_det_iters),
            "determinize_converged": bool(det_converged),
        })

        per_L[L] = {
            "code_to_state": code_to_state, "states_counts": states_counts,
            "table": table, "codes": codes, "next_syms": next_syms,
        }

        prev_code_to_state = code_to_state
        prev_states_counts = states_counts

    return {"sweep": sweep, "per_L": per_L}


def _finalize_reconstruction(entry, L, K):
    """Given one `per_L[L]` growth entry, compute the full reconstruction
    dict (pi_s, C_mu, h_mu, transition_counts, determinism_violation_frac,
    frac_occurrences_excluded) -- same output shape as the pre-revision
    `cssr_fixed_L`, for downstream (BSI, reject-gate, run_variant_analysis)
    compatibility."""
    code_to_state = entry["code_to_state"]
    codes = entry["codes"]
    next_syms = entry["next_syms"]
    states_counts = entry["states_counts"]
    n_states = len(states_counts)

    occ_cluster = code_to_state[codes]
    valid_mask = occ_cluster >= 0
    n_valid = int(valid_mask.sum())
    frac_excluded = 1.0 - (n_valid / len(codes)) if len(codes) > 0 else 1.0
    if n_valid == 0:
        return {"status": "insufficient_samples"}

    counts_per_state = np.bincount(occ_cluster[valid_mask], minlength=n_states)
    pi_s = counts_per_state / counts_per_state.sum()

    nz = pi_s[pi_s > 0]
    C_mu = float(-np.sum(nz * np.log2(nz)))

    h_per_state = np.zeros(n_states)
    for ci in range(n_states):
        cc = states_counts[ci].astype(float)
        tot = cc.sum()
        if tot > 0:
            p = cc / tot
            p_nz = p[p > 0]
            h_per_state[ci] = -np.sum(p_nz * np.log2(p_nz))
    h_mu = float(np.sum(pi_s * h_per_state))

    result_codes = _shift_code(codes, next_syms, L, K)
    result_cluster = code_to_state[result_codes]
    both_valid = valid_mask & (result_cluster >= 0)
    transition_counts = np.zeros((n_states, n_states), dtype=np.int64)
    if both_valid.any():
        origin = occ_cluster[both_valid]
        dest = result_cluster[both_valid]
        flat = origin * n_states + dest
        flat_counts = np.bincount(flat, minlength=n_states * n_states)
        transition_counts = flat_counts.reshape(n_states, n_states)

    dvf = _determinism_violation_frac_occ(codes, next_syms, code_to_state, L, K)

    return {
        "status": "ok", "L": int(L), "alphabet_size": int(K), "n_states": int(n_states),
        "n_occurrences_total": int(len(codes)), "n_occurrences_valid": int(n_valid),
        "frac_occurrences_excluded": float(frac_excluded),
        "determinism_violation_frac": float(dvf),
        "pi_s": pi_s.tolist(), "C_mu": C_mu, "h_mu": h_mu,
        "cluster_next_symbol_counts": [sc.tolist() for sc in states_counts],
        "transition_counts": transition_counts.tolist(),
    }


def reconstruct_at_fixed_L(symbols, alphabet_size, L_target, alpha=ALPHA_CSSR,
                            min_count=MIN_COUNT_PER_HISTORY):
    """Grow full incremental CSSR from L=1 up to L_target (inclusive) and
    return the finalized reconstruction AT L_target. Used for IAAFT
    surrogates / bootstrap resamples, where L is already selected (scope
    decision #4, unchanged) -- genuine CSSR is inherently sequential, so
    even a "fixed L" surrogate reconstruction must be reached by growing
    through L=1,...,L_target-1 first, not skipped-to directly."""
    grown = cssr_incremental_grow(symbols, alphabet_size, L_max=L_target,
                                   alpha=alpha, min_count=min_count)
    if L_target not in grown["per_L"]:
        return {"status": "insufficient_samples"}
    return _finalize_reconstruction(grown["per_L"][L_target], L_target, alphabet_size)


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
    """Run ONE full incremental-CSSR growth pass (`cssr_incremental_grow`)
    across L=1..max(L_grid), select the smallest L such that
    n_states(L) == n_states(L+1) == ... for `n_stable` consecutive steps
    (BIC/AIC-style order-selection analogue, per METHODOLOGY_NOTE.md -- NOT
    a fixed constant, NOT visual). Applies the MANDATORY reject gate:
      - DEGENERATE: n_states at the selected L == 1
      - NOT_CONVERGENT: the n_states(L) curve never stabilizes across the
        WHOLE grid (no run of `n_stable` consecutive equal values found)
      - NOT_DETERMINISTIC: determinism_violation_frac at the selected L
        exceeds `determinism_max` (now a POST-determinize sanity check --
        see scope decision #2 in the module docstring; should be ~0 unless
        the determinize iteration cap was hit)
    Returns a dict with the full sweep (`sweep`: list of per-L summaries),
    `L_selected`, `verdict` ("OK" or one of the three reject codes above),
    and (if verdict=="OK") the selected L's full reconstruction dict under
    `reconstruction`.

    `min_L_for_selection=2` (THE ONE PRE-AUTHORIZED CORRECTION FROM THE V1
    VALIDATION, carried over UNCHANGED by this revision -- documented in
    VALIDATION_NOTE.md, not re-derived here): L=1 is EXCLUDED from the
    stability search (though still computed and reported in the sweep curve
    for transparency). Reason, discovered by the mandatory code-correctness/
    positive-control diagnostics: for median-binary (K=2) and tercile-
    ternary (K=3) R_lambda specifically, whenever the L=1 histories do not
    merge into one cluster, pi_s at L=1 is MATHEMATICALLY FORCED to equal
    R_lambda's own construction marginal (exactly 0.5/0.5 for the median
    split, exactly 1/3 each for tercile split) -- by definition of what a
    median/tercile threshold IS, independent of the segment's actual
    dynamics. C_mu at L=1 therefore collapses to a TRIVIAL, CONSTANT value
    (log2(K)) whenever n_states(1)==K, carrying ZERO discriminating
    information about real vs. surrogate dynamics. This property is
    ORTHOGONAL to fixed-L-clustering vs. full incremental CSSR (it is a
    fact about what "state" means at L=1 for a binarized/ternarized series,
    not an artifact of the earlier simplification), so the correction
    remains valid and is kept unchanged under this revision.
    """
    L_max = max(L_grid)
    grown = cssr_incremental_grow(symbols, alphabet_size, L_max=L_max, alpha=alpha, min_count=min_count)
    sweep = grown["sweep"]
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

    if L_selected not in grown["per_L"]:
        return {
            "sweep": sweep, "n_states_curve": n_states_curve,
            "L_selected": L_selected, "verdict": "NOT_CONVERGENT",
        }

    reconstruction = _finalize_reconstruction(grown["per_L"][L_selected], L_selected, alphabet_size)

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
    FIXED topology (n_states, transition_counts) from the CSSR reconstruction.
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

        r_pre = reconstruct_at_fixed_L(surr_pre_sym, alphabet_size, L_pre)
        r_post = reconstruct_at_fixed_L(surr_post_sym, alphabet_size, L_post)

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
        r_pre = reconstruct_at_fixed_L(b_pre_sym, alphabet_size, L_pre)
        r_post = reconstruct_at_fixed_L(b_post_sym, alphabet_size, L_post)
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
