"""
Canonical Lempel-Ziv Complexity (LZC) pipeline for DISC-TRI-RG-001,
candidate `lempel-ziv-complexity` (Lempel & Ziv 1976, IEEE Trans. Info.
Theory 22:75; Kaspar & Schuster 1987, Phys. Rev. A 36:842; median-
threshold binarization, Aboy, Hornero, Abasolo & Alvarez 2006, IEEE
Trans. Biomed. Eng. 53:2282; ternary/tertile quantization, Kamath 2016,
Cogent Engineering 3(1):1177924).

Fixed BEFORE running on any real domain (Daphnet Freezing-of-Gait,
Kilauea 2018 LERZ seismicity) -- see ../METHODOLOGY_NOTE.md for the full
rationale. This is a NEW, self-contained implementation specific to this
test line: it does not import from, and is not derived from, any other
`*_common.py` in this lab, even though the IAAFT surrogate step and the
moving-block-bootstrap fallback are the SAME published methods (Schreiber
& Schmitz 1996; Kunsch 1989) required by the methodology note for
cross-line consistency.

Method (METHODOLOGY_NOTE.md gaps (a)-(d)):
  1. Binarize/quantize each segment INDEPENDENTLY (median split for the
     primary channel, tertile split for the companion channel) -- the
     threshold(s) are re-estimated from that segment's own empirical
     distribution, never inherited from PRE into POST.
  2. Run the classical LZ76 greedy-parsing algorithm (Kaspar & Schuster's
     implementation of Lempel & Ziv 1976) on the resulting symbolic
     string to get the raw parse count c(n).
  3. Normalize: b(n) = n / log_alpha(n) (alpha=2 for binary, alpha=3 for
     ternary), LZC = c(n) / b(n) (Kaspar & Schuster 1987).
  4. IAAFT surrogates (Schreiber & Schmitz 1996) are the PRIMARY
     significance test for BOTH channels: N_SURROGATES=200,
     N_IAAFT_ITER=50, seed=12345, PRE/POST surrogates generated
     independently from their own real series, two-tailed p-values on
     Delta_LZC_median / Delta_LZC_ternary.

Unlike every other candidate in this line, there is NO embedding, NO
delay, NO scale grid: R_lambda is a single, domain-agnostic threshold
rule reapplied per segment. This structurally avoids the FNN/Takens
non-resolution failure mode that closed RQA at validation.

Any agent applying this pipeline to real data MUST import and call
`run_lzc_analysis` (or the lower-level helpers) rather than
reimplementing any of this, so "same formula, no per-domain
reformulation" is a literal code-identity guarantee, matching the
discipline already used across this lab.
"""
import math

import numpy as np

# ---- fixed constants (METHODOLOGY_NOTE.md gaps (a)-(d) -- identical for
# every domain this pipeline is ever applied to; no per-domain tuning) ----
MIN_N_SEGMENT = 50          # computability floor, gap (d)
MAX_N_PER_SEGMENT = 200000  # subsampling cap, gap (d) (benchmark-justified)
N_SURROGATES = 200          # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50           # IAAFT iterations per surrogate
SEED = 12345


# --------------------------------------------------------------------------
# Gap (d): subsampling
# --------------------------------------------------------------------------

def subsample_segment(x, max_n=MAX_N_PER_SEGMENT):
    """Uniform-stride decimation to at most `max_n` samples.

    If len(x) <= max_n, returns x unchanged (stride=1, subsampled=False).
    Otherwise stride = ceil(N / max_n), x[::stride] -- identical
    convention already used elsewhere in this lab (rqa_common.py,
    vg_common.py, pe_common.py) for this computational-budget rule.
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
# Gap (a): R_lambda -- median binarization (primary) and tertile ternary
# quantization (companion), each re-estimated from its OWN segment.
# --------------------------------------------------------------------------

def median_binarize(x):
    """Median-threshold binarization (Aboy, Hornero, Abasolo & Alvarez
    2006): s(i) = 0 if x(i) < median(X), s(i) = 1 if x(i) >= median(X).
    The median is computed from `x` itself (this segment only). Returns
    an int array of 0/1 the same length as x."""
    x = np.asarray(x, dtype=float)
    med = np.median(x)
    return (x >= med).astype(np.int64)


def ternary_quantize(x):
    """Tertile-based ternary quantization (Kamath 2016): thresholds are
    the 1/3 and 2/3 empirical quantiles of `x` itself (this segment
    only). Returns an int array of {0,1,2} the same length as x."""
    x = np.asarray(x, dtype=float)
    q1, q2 = np.quantile(x, [1.0 / 3.0, 2.0 / 3.0])
    symbols = np.zeros(len(x), dtype=np.int64)
    symbols[(x >= q1) & (x < q2)] = 1
    symbols[x >= q2] = 2
    return symbols


# --------------------------------------------------------------------------
# LZ76 greedy-parsing complexity (Lempel & Ziv 1976, Kaspar & Schuster
# 1987's canonical implementation). Validated against the worked example
# in Kaspar & Schuster 1987 itself: s=[1,0,0,1,1,1,1,0,1,1,0,0,0,0,1,0]
# (binary string "1001111011000010") gives c(n)=6 -- confirmed in
# validate_synthetic.py's code-correctness diagnostic (check 0) before
# any use on real or even stochastic-synthetic data.
# --------------------------------------------------------------------------

def lz76_complexity_naive(symbols):
    """Raw LZ76 parse count c(n) for a sequence of integer symbols (any
    alphabet size). Standard greedy-parsing algorithm: scans the
    sequence, incrementing the complexity count each time a new
    substring is found that has not appeared as a previously-parsed
    "phrase" extended by one new symbol (Lempel & Ziv 1976; this exact
    iterative i/k/l formulation is Kaspar & Schuster 1987's canonical
    reimplementation, widely reused in the LZC literature).

    KNOWN PERFORMANCE DEFECT, discovered when applying this pipeline to
    real data (segments of ~40,000-200,000 samples): this nested-loop
    implementation restarts its candidate-match search from i=0 at
    EVERY phrase boundary, giving ~O(n^2/log n) total work for typical
    (near-random) data -- confirmed empirically (N=20,000 already takes
    ~6s; N=79,043 takes ~97s; N=200,000 was killed after >30 CPU-minutes
    without finishing). `METHODOLOGY_NOTE.md` Gap (d)'s computational
    budget assumed this parsing step was "O(N) e barato" -- true only
    for the small N=3,000 used in synthetic validation, false at real-
    data scale. Kept here ONLY as a slow-but-trusted reference for
    cross-validating `lz76_complexity_fast` below (never called on real
    or full synthetic-validation data by the production pipeline).
    """
    n = len(symbols)
    if n == 0:
        return 0
    if n == 1:
        return 1
    s = symbols
    i, k, l = 0, 1, 1
    c = 1
    k_max = 1
    stop = False
    while not stop:
        if s[i + k - 1] == s[l + k - 1]:
            k += 1
            if l + k > n:
                c += 1
                stop = True
        else:
            if k > k_max:
                k_max = k
            i += 1
            if i == l:
                c += 1
                l += k_max
                if l + 1 > n:
                    stop = True
                else:
                    i = 0
                    k = 1
                    k_max = 1
            else:
                k = 1
    return c


# --------------------------------------------------------------------------
# Fast O(n log n) reimplementation of the SAME c(n), added after the
# performance defect above was discovered applying the pipeline to real
# data. Computes, for each LZ76 phrase start l, k_max = 1 + max_{i<l}
# LCP(suffix_i, suffix_l) (capped at n-l) via a suffix array + Kasai LCP
# array + sparse-table range-minimum-query + Fenwick-tree order
# statistics (predecessor/successor of the current suffix's rank among
# already-seen ranks) -- mathematically identical to what the naive
# nested loop above computes (the naive loop tries every candidate start
# i in [0,l) in turn, extends k while symbols match, and records k at
# the point of failure -- i.e. LCP(suffix_i,suffix_l)+1; the max over
# all i is LPF[l]+1; a well-known suffix-array lemma -- for a query rank
# r and any subset S of ranks, max_{y in S} LCP(query,y) is achieved by
# one of the two immediate S-neighbors of r in rank order, since
# LCP(x,y) for ranks r1<r2 equals min(lcp_array[r1+1..r2]), a range-min
# that can only shrink or stay equal as the range widens -- proves the
# predecessor/successor check suffices).
#
# Verified bit-exact against lz76_complexity_naive on: the Kaspar &
# Schuster 1987 worked example; 500 random small sequences (N<60,
# alphabet 2/3); 300 structured sequences (constant, periodic, run-
# length, mixed alphabet, N<400); N=79,043 ternary-alphabet random data
# (the exact Daphnet POST-primary segment length); the real Daphnet
# PRE-robust segment (N=36,472, both channels); a decimated slice of
# the real Kilauea PRE segment (N=20,000, both channels). Zero
# mismatches in every check. ~30-95x faster at N=20,000-79,043 in this
# cross-validation; N=200,000 (the real-data subsampling cap) computes
# in ~2.4s, versus an estimated >12 CPU-minutes for the naive version.
# --------------------------------------------------------------------------

def _build_suffix_array(arr):
    """Prefix-doubling suffix array (numpy-vectorized sort per
    doubling step). Returns (sa, rank): sa[r] = start position of the
    rank-r suffix (ascending order); rank[i] = rank of the suffix
    starting at position i."""
    n = len(arr)
    if n == 0:
        return np.array([], dtype=np.int64), np.array([], dtype=np.int64)
    rank = arr.astype(np.int64).copy()
    k = 1
    sa = np.argsort(rank, kind="stable")
    tmp = np.empty(n, dtype=np.int64)
    tmp[sa[0]] = 0
    for idx in range(1, n):
        tmp[sa[idx]] = tmp[sa[idx - 1]] + (1 if rank[sa[idx]] != rank[sa[idx - 1]] else 0)
    rank = tmp
    while True:
        if rank.max() == n - 1:
            break
        second = np.full(n, -1, dtype=np.int64)
        second[: n - k] = rank[k:]
        order = np.lexsort((second, rank))
        tmp = np.empty(n, dtype=np.int64)
        tmp[order[0]] = 0
        for idx in range(1, n):
            prev, cur = order[idx - 1], order[idx]
            same = (rank[cur] == rank[prev]) and (second[cur] == second[prev])
            tmp[cur] = tmp[prev] + (0 if same else 1)
        rank = tmp
        sa = order
        k *= 2
        if k > n:
            break
    sa = np.argsort(rank, kind="stable")
    return sa, rank


def _kasai_lcp(arr, sa, rank):
    """Kasai's O(n) LCP array: lcp[r] = LCP(suffix at sa[r-1], suffix at
    sa[r]) for r=1..n-1 (lcp[0] unused/0)."""
    n = len(arr)
    lcp = np.zeros(n, dtype=np.int64)
    h = 0
    for i in range(n):
        r = rank[i]
        if r > 0:
            j = sa[r - 1]
            while i + h < n and j + h < n and arr[i + h] == arr[j + h]:
                h += 1
            lcp[r] = h
            if h > 0:
                h -= 1
        else:
            h = 0
    return lcp


def _build_sparse_table(lcp):
    """Sparse table for O(1) range-minimum-query over `lcp`."""
    n = len(lcp)
    if n == 0:
        return None
    log_n = max(1, int(np.floor(np.log2(n))) + 1)
    table = np.zeros((log_n, n), dtype=np.int64)
    table[0] = lcp
    j = 1
    while (1 << j) <= n:
        half = 1 << (j - 1)
        table[j, : n - (1 << j) + 1] = np.minimum(
            table[j - 1, : n - (1 << j) + 1], table[j - 1, half: n - (1 << j) + 1 + half]
        )
        j += 1
    return table


def _rmq_query(table, lo, hi):
    """min(lcp[lo..hi]) inclusive, lo<=hi, via the sparse table."""
    if lo > hi:
        return 0
    length = hi - lo + 1
    j = length.bit_length() - 1
    return int(min(table[j, lo], table[j, hi - (1 << j) + 1]))


class _FenwickOrderStats:
    """Fenwick tree (BIT) over integer keys in [0, n) supporting insert
    and O(log n) predecessor/successor-by-order queries via binary
    lifting -- an order-statistics-tree substitute with no external
    dependency."""

    def __init__(self, n):
        self.n = n
        self.LOG = max(1, n.bit_length())
        self.tree = [0] * (n + 1)
        self.count = 0

    def insert(self, i):
        self.count += 1
        i += 1
        while i <= self.n:
            self.tree[i] += 1
            i += i & (-i)

    def prefix_sum(self, i):
        if i < 0:
            return 0
        i = min(i, self.n - 1) + 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def find_by_order(self, k):
        pos = 0
        remaining = k
        bit = 1 << self.LOG
        while bit > 0:
            nxt = pos + bit
            if nxt <= self.n and self.tree[nxt] < remaining:
                pos = nxt
                remaining -= self.tree[nxt]
            bit >>= 1
        return pos

    def predecessor(self, r):
        cnt = self.prefix_sum(r - 1)
        if cnt == 0:
            return None
        return self.find_by_order(cnt)

    def successor(self, r):
        cnt = self.prefix_sum(r)
        if cnt >= self.count:
            return None
        return self.find_by_order(cnt + 1)


def lz76_complexity_fast(symbols):
    """Fast O(n log n) computation of the SAME c(n) as
    `lz76_complexity_naive` -- see the section docstring above for the
    equivalence proof and cross-validation summary. This is the version
    actually used by `normalized_lzc`/the production pipeline."""
    n = len(symbols)
    if n == 0:
        return 0
    if n == 1:
        return 1
    arr = np.asarray(symbols, dtype=np.int64)
    sa, rank = _build_suffix_array(arr)
    lcp = _kasai_lcp(arr, sa, rank)
    table = _build_sparse_table(lcp)

    fen = _FenwickOrderStats(n)
    fen.insert(int(rank[0]))

    c = 1
    l = 1
    while l < n:
        r_l = int(rank[l])
        best_lcp = 0
        pred = fen.predecessor(r_l)
        if pred is not None:
            best_lcp = max(best_lcp, _rmq_query(table, pred + 1, r_l))
        succ = fen.successor(r_l)
        if succ is not None:
            best_lcp = max(best_lcp, _rmq_query(table, r_l + 1, succ))
        k_max = min(best_lcp + 1, n - l)
        c += 1
        l_next = l + k_max
        for p in range(l, min(l_next, n)):
            fen.insert(int(rank[p]))
        l = l_next
    return c


def lz76_complexity(symbols):
    """Public entry point used throughout this pipeline: the fast,
    cross-validated O(n log n) implementation. See
    `lz76_complexity_naive`/`lz76_complexity_fast` docstrings above for
    the performance-defect discovery, the fix, and the equivalence
    proof/validation summary."""
    return lz76_complexity_fast(symbols)


def normalized_lzc(symbols, alphabet_size):
    """LZC = c(n) / b(n), b(n) = n / log_alpha(n) (Kaspar & Schuster
    1987). Returns (LZC, c_n, b_n, n). If n < 2 (b(n) undefined, log(1)=0
    or n=0), returns (None, c_n, None, n) -- caller must handle via the
    MIN_N_SEGMENT floor (gap (d)), this function never silently
    substitutes a value."""
    n = len(symbols)
    c_n = lz76_complexity(symbols)
    if n < 2:
        return None, c_n, None, n
    b_n = n / math.log(n, alphabet_size)
    if b_n == 0:
        return None, c_n, None, n
    return float(c_n / b_n), c_n, float(b_n), n


def compute_lzc_channels(x):
    """Run both R_lambda variants (median binarization, tertile ternary
    quantization) on one segment `x` and compute normalized LZC for each.

    Returns a dict with `status` ("ok" or "insufficient_samples") and,
    when "ok": n_samples_used, LZC_median, c_n_median, b_n_median,
    LZC_ternary, c_n_ternary, b_n_ternary.
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < MIN_N_SEGMENT:
        return {"status": "insufficient_samples", "n_samples_used": int(n),
                "min_n_segment": MIN_N_SEGMENT}

    bin_symbols = median_binarize(x)
    tern_symbols = ternary_quantize(x)

    lzc_med, c_med, b_med, _ = normalized_lzc(bin_symbols.tolist(), alphabet_size=2)
    lzc_tern, c_tern, b_tern, _ = normalized_lzc(tern_symbols.tolist(), alphabet_size=3)

    return {
        "status": "ok",
        "n_samples_used": int(n),
        "LZC_median": lzc_med, "c_n_median": int(c_med), "b_n_median": b_med,
        "LZC_ternary": lzc_tern, "c_n_ternary": int(c_tern), "b_n_ternary": b_tern,
    }


# --------------------------------------------------------------------------
# Gap (d): IAAFT surrogates (Schreiber & Schmitz 1996)
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
# Pre-authorized fallback: moving-block bootstrap (Kunsch 1989), added
# here (not used unless synthetic validation shows low IAAFT power for a
# channel, per METHODOLOGY_NOTE.md gap (d)) -- same machinery/API style
# already used in rqa_common.py / pe_common.py for this lab.
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
                              seed=SEED, max_n=MAX_N_PER_SEGMENT):
    """Moving-block bootstrap (Kunsch 1989) significance test for
    Delta_LZC_median / Delta_LZC_ternary, PRE and POST resampled
    independently `n_bootstrap` times each, i-th pairing (matching this
    lab's convention). Block length L defaults to max(N//20, 10) if not
    given. Only invoked for a channel if the synthetic validation shows
    IAAFT has low power for it (METHODOLOGY_NOTE.md gap (d) pre-
    authorized fallback) -- NOT part of the default pipeline.
    """
    pre_raw = np.asarray(pre_segment, dtype=float)
    post_raw = np.asarray(post_segment, dtype=float)
    pre, _ = subsample_segment(pre_raw, max_n=max_n)
    post, _ = subsample_segment(post_raw, max_n=max_n)

    real_pre = compute_lzc_channels(pre)
    real_post = compute_lzc_channels(post)

    if L is None:
        L = max(len(pre) // 20, 10)

    rng = np.random.default_rng(seed)

    def _boot_series(segment, n):
        med_vals, tern_vals = [], []
        for _ in range(n):
            resampled = moving_block_bootstrap_resample(segment, L, rng)
            feat = compute_lzc_channels(resampled)
            if feat["status"] == "ok":
                med_vals.append(feat["LZC_median"])
                tern_vals.append(feat["LZC_ternary"])
            else:
                med_vals.append(None)
                tern_vals.append(None)
        return med_vals, tern_vals

    med_boot_pre, tern_boot_pre = _boot_series(pre, n_bootstrap)
    med_boot_post, tern_boot_post = _boot_series(post, n_bootstrap)

    def _pair_deltas(pre_vals, post_vals):
        deltas, n_undef = [], 0
        for vp, vq in zip(pre_vals, post_vals):
            if vp is None or vq is None:
                n_undef += 1
            else:
                deltas.append(vq - vp)
        return np.array(deltas, dtype=float), n_undef

    delta_med_boot, n_undef_med = _pair_deltas(med_boot_pre, med_boot_post)
    delta_tern_boot, n_undef_tern = _pair_deltas(tern_boot_pre, tern_boot_post)

    def _two_tailed_p(deltas):
        if len(deltas) == 0:
            return None
        frac_le0 = float(np.mean(deltas <= 0))
        frac_ge0 = float(np.mean(deltas >= 0))
        return float(2 * min(frac_le0, frac_ge0))

    delta_med_real = None
    delta_tern_real = None
    if real_pre["status"] == "ok" and real_post["status"] == "ok":
        if real_pre["LZC_median"] is not None and real_post["LZC_median"] is not None:
            delta_med_real = real_post["LZC_median"] - real_pre["LZC_median"]
        if real_pre["LZC_ternary"] is not None and real_post["LZC_ternary"] is not None:
            delta_tern_real = real_post["LZC_ternary"] - real_pre["LZC_ternary"]

    return {
        "bootstrap_block_length": int(L),
        "bootstrap_n_bootstrap": int(n_bootstrap),
        "bootstrap_seed": int(seed),
        "delta_LZC_median_real": delta_med_real,
        "delta_LZC_ternary_real": delta_tern_real,
        "bootstrap_delta_LZC_median_mean": float(np.mean(delta_med_boot)) if len(delta_med_boot) else None,
        "bootstrap_delta_LZC_median_std": float(np.std(delta_med_boot)) if len(delta_med_boot) else None,
        "bootstrap_delta_LZC_median_p": _two_tailed_p(delta_med_boot),
        "bootstrap_delta_LZC_median_n_valid": int(len(delta_med_boot)),
        "bootstrap_delta_LZC_median_n_undefined": int(n_undef_med),
        "bootstrap_delta_LZC_ternary_mean": float(np.mean(delta_tern_boot)) if len(delta_tern_boot) else None,
        "bootstrap_delta_LZC_ternary_std": float(np.std(delta_tern_boot)) if len(delta_tern_boot) else None,
        "bootstrap_delta_LZC_ternary_p": _two_tailed_p(delta_tern_boot),
        "bootstrap_delta_LZC_ternary_n_valid": int(len(delta_tern_boot)),
        "bootstrap_delta_LZC_ternary_n_undefined": int(n_undef_tern),
    }


# --------------------------------------------------------------------------
# Full PRE/POST transition test pipeline (public entry point)
# --------------------------------------------------------------------------

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def run_lzc_analysis(pre_series, post_series, seed=SEED, n_surrogates=N_SURROGATES,
                      n_iter=N_IAAFT_ITER, max_n=MAX_N_PER_SEGMENT, n_mc=None):
    """Run the full LZC (median + ternary) transition test between a PRE
    and a POST segment, per METHODOLOGY_NOTE.md gaps (a)-(d). This is
    the single entry point a real-data script must call WITHOUT
    modification, exactly as `run_pe_analysis`/`run_km_analysis` are
    called elsewhere in this lab.

    IAAFT is the PRIMARY significance test for BOTH channels: `n_surrogates`
    independent PRE/POST surrogate pairs, each surrogate generated from
    its OWN real segment (never cross-segment), fixed seed=12345
    convention used elsewhere in this lab. Two-tailed test: p = fraction
    of surrogates with |Delta_LZC_median_surrogate| >=
    |Delta_LZC_median_real| (and equivalently for Delta_LZC_ternary).

    `n_mc` overrides `n_surrogates` when given (validation-script
    convenience for smaller/faster runs); when None, `n_surrogates` is
    used unchanged.

    Returns a dict:
      status: "ok" if BOTH real_pre and real_post reached "ok" in
          compute_lzc_channels, else "insufficient_samples"
      real_pre, real_post: full compute_lzc_channels() output
      LZC_median_pre/post, LZC_ternary_pre/post: real values
      delta_LZC_median, delta_LZC_ternary: real POST - PRE
      p_LZC_median, p_LZC_ternary: two-tailed IAAFT surrogate p-values
      surrogate_LZC_median_mean/std/n_valid/n_undefined,
      surrogate_LZC_ternary_mean/std/n_valid/n_undefined
      surrogate_LZC_median_deltas, surrogate_LZC_ternary_deltas: FULL
          null arrays (needed for honest sigma-equivalent reporting)
      config: exact fixed parameters used (provenance)
    """
    n_surr = n_mc if n_mc is not None else n_surrogates

    pre_raw = np.asarray(pre_series, dtype=float)
    post_raw = np.asarray(post_series, dtype=float)

    # Gap (d): subsample ONCE, up front, before anything else touches the
    # series -- including IAAFT surrogate generation. Mirrors the
    # convention already established (and audited) for MAX_N_PER_SEGMENT
    # elsewhere in this lab (see pe_common.py's run_pe_analysis docstring
    # for the full rationale): without this, IAAFT would run at the full
    # un-subsampled segment length, defeating the entire point of the
    # computational-budget rule this gap declares.
    pre, pre_sub_info = subsample_segment(pre_raw, max_n=max_n)
    post, post_sub_info = subsample_segment(post_raw, max_n=max_n)

    real_pre = compute_lzc_channels(pre)
    real_post = compute_lzc_channels(post)

    config = {
        "min_n_segment": MIN_N_SEGMENT, "max_n_per_segment": max_n,
        "n_surrogates": n_surr, "n_iaaft_iter": n_iter, "seed": seed,
        "pre_subsample_info": pre_sub_info, "post_subsample_info": post_sub_info,
    }

    if real_pre["status"] != "ok" or real_post["status"] != "ok":
        return {
            "status": "insufficient_samples",
            "real_pre": real_pre,
            "real_post": real_post,
            "config": config,
        }

    LZCm_pre, LZCm_post = real_pre["LZC_median"], real_post["LZC_median"]
    LZCt_pre, LZCt_post = real_pre["LZC_ternary"], real_post["LZC_ternary"]

    delta_med_real = _delta(LZCm_post, LZCm_pre)
    delta_tern_real = _delta(LZCt_post, LZCt_pre)

    rng = np.random.default_rng(seed)
    surr_delta_med = []
    surr_delta_tern = []
    n_undef_med = 0
    n_undef_tern = 0

    for _ in range(n_surr):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        feat_pre_s = compute_lzc_channels(surr_pre)
        feat_post_s = compute_lzc_channels(surr_post)

        med_pre_s = feat_pre_s["LZC_median"] if feat_pre_s["status"] == "ok" else None
        med_post_s = feat_post_s["LZC_median"] if feat_post_s["status"] == "ok" else None
        d_med = _delta(med_post_s, med_pre_s)
        if d_med is None:
            n_undef_med += 1
        else:
            surr_delta_med.append(d_med)

        tern_pre_s = feat_pre_s["LZC_ternary"] if feat_pre_s["status"] == "ok" else None
        tern_post_s = feat_post_s["LZC_ternary"] if feat_post_s["status"] == "ok" else None
        d_tern = _delta(tern_post_s, tern_pre_s)
        if d_tern is None:
            n_undef_tern += 1
        else:
            surr_delta_tern.append(d_tern)

    surr_delta_med = np.array(surr_delta_med, dtype=float)
    surr_delta_tern = np.array(surr_delta_tern, dtype=float)

    if delta_med_real is None or len(surr_delta_med) == 0:
        p_med = None
    else:
        p_med = float(np.mean(np.abs(surr_delta_med) >= abs(delta_med_real)))

    if delta_tern_real is None or len(surr_delta_tern) == 0:
        p_tern = None
    else:
        p_tern = float(np.mean(np.abs(surr_delta_tern) >= abs(delta_tern_real)))

    return {
        "status": "ok",
        "real_pre": real_pre,
        "real_post": real_post,
        "LZC_median_pre": LZCm_pre, "LZC_median_post": LZCm_post,
        "LZC_ternary_pre": LZCt_pre, "LZC_ternary_post": LZCt_post,
        "delta_LZC_median": delta_med_real,
        "delta_LZC_ternary": delta_tern_real,
        "p_LZC_median": p_med,
        "p_LZC_ternary": p_tern,
        "surrogate_LZC_median_mean": float(np.mean(surr_delta_med)) if len(surr_delta_med) else None,
        "surrogate_LZC_median_std": float(np.std(surr_delta_med)) if len(surr_delta_med) else None,
        "surrogate_LZC_median_n_valid": int(len(surr_delta_med)),
        "surrogate_LZC_median_n_undefined": int(n_undef_med),
        "surrogate_LZC_ternary_mean": float(np.mean(surr_delta_tern)) if len(surr_delta_tern) else None,
        "surrogate_LZC_ternary_std": float(np.std(surr_delta_tern)) if len(surr_delta_tern) else None,
        "surrogate_LZC_ternary_n_valid": int(len(surr_delta_tern)),
        "surrogate_LZC_ternary_n_undefined": int(n_undef_tern),
        "surrogate_LZC_median_deltas": surr_delta_med.tolist(),
        "surrogate_LZC_ternary_deltas": surr_delta_tern.tolist(),
        "config": config,
    }
