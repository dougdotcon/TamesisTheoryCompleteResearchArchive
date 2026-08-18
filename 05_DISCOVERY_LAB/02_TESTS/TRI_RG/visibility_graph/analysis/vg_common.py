"""
Canonical natural-visibility-graph + box-covering-renormalization pipeline
for DISC-TRI-RG-001, candidate `grafo-de-visibilidade`.

Fixed BEFORE running on any real domain (geomagnetic storm 17/03/2015,
Hurricane Harvey/2017 hydrology) -- see ../METHODOLOGY_NOTE.md for the full
rationale. This is a NEW, self-contained implementation specific to this
test line: it does not import from, and is not derived from,
`mse_multiscale_entropy/analysis/mse_common.py`, `dfa_multiscale_entropy/
analysis/dfa_common.py`, or any other pipeline in this lab, even though the
IAAFT surrogate step is conceptually the same published method (Schreiber &
Schmitz 1996) required by the methodology note for cross-line consistency,
and the moving-block-bootstrap fallback (if triggered) is conceptually the
same published method (Kunsch 1989) used as the DFA-line's Adendo ao Gap (c).

Method:
  1. Natural visibility graph (Lacasa, Luque, Ballesteros, Luque & Nuno 2008,
     PNAS 105:4972), UNDIRECTED, UNWEIGHTED, original criterion (not HVG, not
     weighted-by-slope): nodes a<b are connected iff, for every c with
     a<c<b,
         y_c < y_b + (y_a - y_b) * (t_b - t_c) / (t_b - t_a)
  2. Box-covering (Song, Havlin & Makse 2005, Nature 433:392) by
     NODE-COVERING (declared a priori in METHODOLOGY_NOTE.md Gap (a) to
     eliminate the node- vs edge-covering ambiguity documented in the
     literature): a box of size l_B is a node set where the shortest-path
     distance between ANY two members is < l_B (strictly). N_B(l_B) is
     approximated by the standard greedy compact-box-burning (CBB, Song et
     al. 2007) procedure, R_REPEATS=50 random seed orders per l_B, MEDIAN
     taken.
  3. d_B (primary I(X)): OLS fit of log(N_B(l_B)) vs log(l_B),
     N_B(l_B) ~ l_B^{-d_B}.
  4. C (companion channel): mean local clustering coefficient of the
     visibility graph (Lacasa & Toral 2010, Phys. Rev. E 82:036120).
  5. IAAFT surrogates (Schreiber & Schmitz 1996) are the PRIMARY
     significance test here (METHODOLOGY_NOTE.md Gap (e)) -- same pattern
     as mse-multiscale-entropy in this lab, unlike CSD/DFA-original/SOC
     where IAAFT/Poisson was secondary.

CBB implementation note (a concrete algorithmic choice not fully specified
by "compact-box-burning" alone, documented honestly here rather than left
implicit): exact minimum diameter-<l_B node-set cover is NP-hard, so, like
all practical box-covering implementations, this uses a greedy approximation.
Concretely: given the full all-pairs shortest-path distance matrix D of the
graph (computed ONCE per graph, reused across all l_B/repeats -- this is the
key optimization that makes R_REPEATS=50 x N_SCALES<=15 tractable), a box is
grown as the ball of radius r = floor((l_B-1)/2) around a randomly chosen
still-uncovered "seed" node, restricted to still-uncovered nodes. By the
triangle inequality, any two members of such a ball are at distance
<= 2r <= l_B-1 < l_B, so this ball ALWAYS satisfies the box's diameter
constraint by construction (it is a conservative/sufficient, not necessarily
maximal, box). Seeds are visited in a uniformly random order (one random
permutation of all nodes per repeat) and each still-uncovered node in that
order becomes the seed of a new box once reached; N_B(l_B) is the number of
boxes formed once every node is covered. This is the seed-radius-burning
variant of CBB widely used in the box-covering literature as a tractable
proxy for the exact (NP-hard) minimum cover, and is what "greedy
compact-box-burning" concretely means in this module.

Scale grid (domain-agnostic, METHODOLOGY_NOTE.md Gap (a)):
  l_B_min=2, l_B_max=floor(diam(G)/4), N_SCALES=min(15, l_B_max-l_B_min+1)
  log-spaced unique integers. If l_B_max gives fewer than 4 distinct l_B
  values, the segment is explicitly rejected (status="insufficient_scales"),
  never silently proceeding with an unreliable log-log fit.

Any agent applying this pipeline to real data MUST import and call
`run_vg_analysis` (or the lower-level helpers) rather than reimplementing
any of this, so "same formula, no per-domain reformulation" is a literal
code-identity guarantee, matching the discipline already used elsewhere in
this lab.
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

# ---- fixed constants (METHODOLOGY_NOTE.md Gaps (a), (d), (e) -- identical
# for every domain this pipeline is ever applied to; no per-domain tuning) --
L_B_MIN = 2                    # smallest box size (Gap (a))
L_B_MAX_DIAM_DIVISOR = 4       # l_B_max = floor(diam(G)/4)
N_SCALES_CAP = 15              # cap on log-spaced l_B values
MIN_SCALES_REQUIRED = 4        # below this, reject as insufficient-power
R_REPEATS = 50                 # random seed orders per l_B, median taken (Gap (a))
MIN_FIT_POINTS = 4             # same as MIN_SCALES_REQUIRED, kept as a named constant
                                # for the OLS fit specifically
MAX_N_PER_SEGMENT = 5000       # subsampling cap, Gap (d)
N_SURROGATES = 200             # IAAFT surrogate pairs (Schreiber & Schmitz 1996), Gap (e)
N_IAAFT_ITER = 50              # IAAFT iterations per surrogate, Gap (e)
SEED = 12345                   # Gap (e)

# Moving-block bootstrap (Kunsch 1989) constants -- NOT part of the original
# METHODOLOGY_NOTE.md Gap (e) primary protocol, but PRE-AUTHORIZED there as a
# fallback ("adicionar teste complementar de bootstrap por blocos moveis...
# como PRIMARIO, mesma correcao ja aplicada 2x nesta linha (DFA, SOC), ANTES
# de tocar dado real") if synthetic validation shows the same IAAFT low-power
# failure mode already documented for DFA-alpha.
#
# VALIDATION_NOTE.md: this machinery WAS exercised empirically against the
# positive control (25 moving-block resamples of each of PRE and POST), but
# the failure mode found for d_B here is NOT the DFA-alpha pattern (IAAFT
# computing d_B but its null distribution matching the real value too
# closely -- a POWER problem). Instead, d_B is frequently simply
# UNDEFINED ("insufficient_scales", METHODOLOGY_NOTE.md Gap (a)'s own
# diam(G)>=20 scale-grid requirement not met) for realistic stochastic
# PRE/POST segments at N<=MAX_N_PER_SEGMENT -- a graph-topology problem
# the bootstrap resamples inherit unchanged (25/25 resamples of both PRE
# and POST stayed "insufficient_scales" in that empirical check), since
# resampling blocks of the SAME segment does not change its length or its
# visibility-graph small-world diameter-scaling regime. The C channel, by
# contrast, showed strong genuine IAAFT power (~14.6 sigma on the positive
# control) without needing this fallback at all. See VALIDATION_NOTE.md for
# the full discussion; this constant/machinery is kept available (and
# `run_vg_analysis(..., run_bootstrap=True)` still works) for a future
# agent who wants an extra confirmatory test on C, but it is not required
# and does not, by itself, resolve d_B's non-computability.
N_BOOTSTRAP = 1000


# --------------------------------------------------------------------------
# Gap (d): subsampling for O(N^2) cost, applied identically to every domain
# --------------------------------------------------------------------------

def subsample_segment(x, max_n=MAX_N_PER_SEGMENT):
    """Uniform-stride decimation to at most `max_n` samples.

    If len(x) <= max_n, returns x unchanged (stride=1, subsampled=False).
    Otherwise stride = ceil(N / max_n), x[::stride] (Gap (d) -- identical
    rule for every domain, fixed a priori, decided before knowing whether
    any given segment actually exceeds the limit; same honest-risk framing
    already used for the analogous MSE-line bearing decimation).
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
# Gap (a): natural visibility graph (Lacasa et al. 2008)
# --------------------------------------------------------------------------

def build_visibility_graph(y, t=None):
    """Natural visibility graph, original Lacasa et al. (2008) criterion,
    undirected, unweighted.

    Vectorized per-node (not a Python O(N^3)/O(N^2 log N) triple loop): the
    original visibility condition
        y_c < y_b + (y_a - y_b) * (t_b - t_c) / (t_b - t_a)   for all a<c<b
    is algebraically equivalent (dividing through by (t_c - t_a) > 0) to the
    standard slope-based reformulation
        s(a, b) > s(a, c)   for all a<c<b,   s(a, x) := (y_x - y_a) / (t_x - t_a)
    which lets each row `a` be resolved in one vectorized pass over
    `c = a+1 .. N-1` using a running (exclusive) prefix max of the slopes,
    instead of re-checking every intermediate c for every candidate b. Total
    cost O(N) per row, O(N^2) overall -- the accepted complexity per
    METHODOLOGY_NOTE.md, but without a Python-level triple loop.

    Returns adj: list[set[int]] of length N (undirected adjacency), and
    n_edges: int.
    """
    y = np.asarray(y, dtype=float)
    N = len(y)
    if t is None:
        t = np.arange(N, dtype=float)
    else:
        t = np.asarray(t, dtype=float)

    adj = [set() for _ in range(N)]
    n_edges = 0
    for a in range(N - 1):
        rest = np.arange(a + 1, N)
        s = (y[rest] - y[a]) / (t[rest] - t[a])
        # exclusive running max: prefix_max[k] = max(s[0..k-1]), prefix_max[0] = -inf
        prefix_max = np.empty_like(s)
        prefix_max[0] = -np.inf
        if len(s) > 1:
            np.maximum.accumulate(s[:-1], out=prefix_max[1:])
        visible = s > prefix_max
        b_indices = rest[visible]
        for b in b_indices:
            adj[a].add(int(b))
            adj[int(b)].add(a)
            n_edges += 1
    return adj, n_edges


def adjacency_to_csr(adj):
    N = len(adj)
    rows, cols = [], []
    for i, nbrs in enumerate(adj):
        for j in nbrs:
            rows.append(i)
            cols.append(j)
    data = np.ones(len(rows), dtype=np.int8)
    return csr_matrix((data, (rows, cols)), shape=(N, N))


def all_pairs_shortest_path(adj):
    """Full unweighted all-pairs shortest-path distance matrix, computed
    ONCE per graph and reused for every l_B and R_REPEATS repeat (the key
    optimization that makes the box-covering grid tractable). Uses scipy's
    C-implemented Dijkstra with unweighted=True (equivalent to BFS from
    every node for an unweighted graph).
    """
    g = adjacency_to_csr(adj)
    D = shortest_path(g, method="D", directed=False, unweighted=True)
    return D


def graph_diameter(D):
    """Diameter = max finite pairwise distance. A natural visibility graph
    is always connected (consecutive time points a, a+1 are always mutually
    visible by construction -- no intermediate c can exist), so D should
    never contain inf; this is checked explicitly rather than assumed.
    """
    finite = np.isfinite(D)
    if not finite.all():
        n_inf = int((~finite).sum())
        return None, {"connected": False, "n_disconnected_pairs": n_inf}
    diam = float(D.max())
    return diam, {"connected": True, "n_disconnected_pairs": 0}


# --------------------------------------------------------------------------
# Companion channel: mean clustering coefficient (Lacasa & Toral 2010)
# --------------------------------------------------------------------------

def mean_clustering_coefficient(adj):
    """Mean local clustering coefficient of an undirected unweighted graph
    given as adjacency sets. C_i = 2*e_i / (k_i*(k_i-1)) where e_i = number
    of edges among node i's neighbors, k_i = degree of i (C_i := 0 by
    convention if k_i < 2, standard convention for degree-0/1 nodes).
    O(N * mean_k^2) via set-membership lookups -- efficient for the low
    mean degree typical of visibility graphs, avoids an O(N^3) dense
    matrix-power computation.
    """
    N = len(adj)
    if N == 0:
        return None
    c_vals = np.zeros(N, dtype=float)
    for i in range(N):
        nbrs = list(adj[i])
        k = len(nbrs)
        if k < 2:
            c_vals[i] = 0.0
            continue
        e_i = 0
        for idx_a in range(k):
            a = nbrs[idx_a]
            adj_a = adj[a]
            for idx_b in range(idx_a + 1, k):
                if nbrs[idx_b] in adj_a:
                    e_i += 1
        c_vals[i] = 2.0 * e_i / (k * (k - 1))
    return float(c_vals.mean())


# --------------------------------------------------------------------------
# Gap (a): box-covering grid and CBB (greedy seed-radius burning)
# --------------------------------------------------------------------------

def l_b_grid(diam, l_b_min=L_B_MIN, divisor=L_B_MAX_DIAM_DIVISOR,
             n_scales_cap=N_SCALES_CAP):
    """log-spaced integer l_B grid in [l_b_min, floor(diam/divisor)], unique
    values. Returns (scales, l_b_max, status) where status is "ok" or
    "insufficient_scales" (fewer than MIN_SCALES_REQUIRED unique values) --
    METHODOLOGY_NOTE.md Gap (a): "Se l_B_max render menos de 4 valores
    distintos de l_B, o dominio e REJEITADO... declarado honestamente antes
    de qualquer calculo, nao forcado."
    """
    l_b_max = int(np.floor(diam / divisor))
    if l_b_max < l_b_min:
        return np.array([], dtype=int), l_b_max, "insufficient_scales"
    n_scales = min(n_scales_cap, l_b_max - l_b_min + 1)
    if n_scales <= 1:
        raw = np.array([l_b_min], dtype=float)
    else:
        raw = np.exp(np.linspace(np.log(l_b_min), np.log(l_b_max), n_scales))
    scales = np.unique(np.round(raw).astype(int))
    scales = scales[(scales >= l_b_min) & (scales <= l_b_max)]
    if len(scales) < MIN_SCALES_REQUIRED:
        return scales, l_b_max, "insufficient_scales"
    return scales, l_b_max, "ok"


def cbb_single_covering(D, l_b, order):
    """One CBB covering (seed-radius-burning variant, see module docstring)
    of the graph with distance matrix D, box size l_b, using node visitation
    order `order` (a permutation of range(N)). Returns N_B (int).

    r = floor((l_b - 1) / 2) is the box radius; r=0 (l_b<=2) covers each
    node as its own singleton box regardless of order (short-circuited,
    since a radius-0 ball is always just the seed itself) -- N_B = N.
    """
    N = D.shape[0]
    r = (l_b - 1) // 2
    if r <= 0:
        return N
    uncovered = np.ones(N, dtype=bool)
    n_boxes = 0
    for idx in order:
        if uncovered[idx]:
            in_box = uncovered & (D[idx] <= r)
            uncovered[in_box] = False
            n_boxes += 1
    return n_boxes


def cbb_median_covering(D, l_b, r_repeats, rng):
    """Median N_B(l_b) over `r_repeats` independent random seed orders
    (METHODOLOGY_NOTE.md Gap (a): "resultado MEDIANO sobre R_REPEATS=50
    sementes independentes por l_B, reduz vies de ordem de cobertura").
    r=0 case is order-independent so all repeats give the same N_B; still
    run through the same code path for a uniform provenance trail (cheap:
    the r<=0 short-circuit in cbb_single_covering makes each repeat O(1)).
    """
    N = D.shape[0]
    vals = np.empty(r_repeats, dtype=int)
    for i in range(r_repeats):
        order = rng.permutation(N)
        vals[i] = cbb_single_covering(D, l_b, order)
    return float(np.median(vals)), vals.tolist()


def fit_d_b(l_b_scales, n_b_values, min_fit_points=MIN_FIT_POINTS):
    """OLS fit of log(N_B(l_B)) vs log(l_B): N_B ~ l_B^{-d_B}, so
    d_B = -slope. Returns dict {d_B, intercept, n_points, scales} or None
    if fewer than `min_fit_points` valid (finite, positive) points.
    """
    l_b_scales = np.asarray(l_b_scales, dtype=float)
    n_b_values = np.asarray(n_b_values, dtype=float)
    mask = np.isfinite(l_b_scales) & np.isfinite(n_b_values) & (n_b_values > 0) & (l_b_scales > 0)
    if mask.sum() < min_fit_points:
        return None
    log_l = np.log(l_b_scales[mask])
    log_n = np.log(n_b_values[mask])
    slope, intercept = np.polyfit(log_l, log_n, 1)
    return {
        "d_B": float(-slope),
        "intercept": float(intercept),
        "n_points": int(mask.sum()),
        "scales": l_b_scales[mask].astype(int).tolist(),
    }


# --------------------------------------------------------------------------
# Full visibility-graph + box-covering feature computation for one segment
# --------------------------------------------------------------------------

def compute_vg_features(x, t=None, l_b_min=L_B_MIN, divisor=L_B_MAX_DIAM_DIVISOR,
                         n_scales_cap=N_SCALES_CAP, r_repeats=R_REPEATS,
                         min_fit_points=MIN_FIT_POINTS, seed=SEED):
    """Run the full visibility-graph + box-covering pipeline on one segment.

    Returns a dict:
      status: "ok" or "insufficient_scales" (Gap (a) rejection -- if this
          fires, d_B/C are still computed where possible for diagnostics,
          but d_B is explicitly None and must not be used for any Delta/p).
      n_samples, n_edges, diam, connected,
      l_B_grid (list[int]), N_B_median (list[float]), N_B_repeats (list[list[int]]),
      d_B: fit_d_b() output or None,
      C: mean clustering coefficient (float) -- computed regardless of
          box-covering status, since it does not depend on the l_B grid,
      diagnostics: n_scales_achieved, min_scales_required.
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    adj, n_edges = build_visibility_graph(x, t=t)
    C = mean_clustering_coefficient(adj)
    D = all_pairs_shortest_path(adj)
    diam, conn_info = graph_diameter(D)

    result = {
        "n_samples": int(N),
        "n_edges": int(n_edges),
        "diam": diam,
        "connected": conn_info["connected"],
        "n_disconnected_pairs": conn_info["n_disconnected_pairs"],
        "C": C,
    }

    if diam is None:
        result.update({
            "status": "disconnected_graph", "l_B_grid": [], "N_B_median": [],
            "N_B_repeats": [], "d_B": None,
            "diagnostics": {"n_scales_achieved": 0, "min_scales_required": min_fit_points},
        })
        return result

    scales, l_b_max, status = l_b_grid(diam, l_b_min=l_b_min, divisor=divisor,
                                        n_scales_cap=n_scales_cap)
    result["l_B_max"] = int(l_b_max)

    if status == "insufficient_scales":
        result.update({
            "status": "insufficient_scales", "l_B_grid": scales.astype(int).tolist(),
            "N_B_median": [], "N_B_repeats": [], "d_B": None,
            "diagnostics": {"n_scales_achieved": int(len(scales)),
                             "min_scales_required": min_fit_points},
        })
        return result

    rng = np.random.default_rng(seed)
    n_b_median = []
    n_b_repeats = []
    for l_b in scales:
        med, vals = cbb_median_covering(D, int(l_b), r_repeats, rng)
        n_b_median.append(med)
        n_b_repeats.append(vals)

    d_b_fit = fit_d_b(scales, n_b_median, min_fit_points=min_fit_points)

    result.update({
        "status": "ok",
        "l_B_grid": scales.astype(int).tolist(),
        "N_B_median": n_b_median,
        "N_B_repeats": n_b_repeats,
        "d_B": d_b_fit,
        "diagnostics": {"n_scales_achieved": int(len(scales)),
                         "min_scales_required": min_fit_points},
    })
    return result


# --------------------------------------------------------------------------
# Gap (e): IAAFT surrogates (Schreiber & Schmitz 1996)
# --------------------------------------------------------------------------

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate.

    Preserves the linear power spectrum (FFT amplitude spectrum) and the
    exact empirical amplitude distribution (histogram) of `x`; destroys any
    nonlinear phase/temporal structure beyond what a linear Gaussian process
    with the same spectrum and marginal would produce. Independent
    reimplementation for this test line (see module docstring).
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
# Moving-block bootstrap (Kunsch 1989) -- pre-authorized fallback, only
# exercised as a PRIMARY test if validate_synthetic.py's power check
# requires it (see module-level N_BOOTSTRAP docstring above and
# VALIDATION_NOTE.md for whether this path was taken).
# --------------------------------------------------------------------------

def moving_block_bootstrap_resample(x, L, rng):
    """One moving-block-bootstrap resample of `x` (Kunsch 1989): blocks of
    length L, start index drawn uniformly at random with replacement,
    concatenated until >= len(x), then trimmed to exactly len(x).
    """
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


def _percentile_ci95(arr):
    lo, hi = np.percentile(arr, [2.5, 97.5])
    return (float(lo), float(hi))


def _bootstrap_two_tailed_p(delta_arr):
    frac_le0 = float(np.mean(delta_arr <= 0))
    frac_ge0 = float(np.mean(delta_arr >= 0))
    return float(2 * min(frac_le0, frac_ge0))


def run_block_bootstrap_test(pre_segment, post_segment, real_pre=None, real_post=None,
                              n_bootstrap=N_BOOTSTRAP, seed=SEED, **vg_kwargs):
    """Moving-block bootstrap (Kunsch 1989) significance test for
    Delta_d_B / Delta_C, block length L = that segment's own diameter-based
    l_B_max (largest scale actually used by that segment's own box-covering
    grid -- fixed a priori, tied to the analysis itself, same convention as
    the DFA-line's block-length choice). PRE and POST resampled
    independently, n_bootstrap times each, i-th pairing.
    """
    pre = np.asarray(pre_segment, dtype=float)
    post = np.asarray(post_segment, dtype=float)

    if real_pre is None:
        real_pre = compute_vg_features(pre, seed=seed, **vg_kwargs)
    if real_post is None:
        real_post = compute_vg_features(post, seed=seed, **vg_kwargs)

    L_pre = real_pre.get("l_B_max") or max(2, len(pre) // 20)
    L_post = real_post.get("l_B_max") or max(2, len(post) // 20)

    rng = np.random.default_rng(seed)
    d_b_boot_pre, C_boot_pre = [], []
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(pre, L_pre, rng)
        feat = compute_vg_features(resampled, seed=seed, **vg_kwargs)
        d_b_boot_pre.append(None if feat["d_B"] is None else feat["d_B"]["d_B"])
        C_boot_pre.append(feat["C"])

    d_b_boot_post, C_boot_post = [], []
    for _ in range(n_bootstrap):
        resampled = moving_block_bootstrap_resample(post, L_post, rng)
        feat = compute_vg_features(resampled, seed=seed, **vg_kwargs)
        d_b_boot_post.append(None if feat["d_B"] is None else feat["d_B"]["d_B"])
        C_boot_post.append(feat["C"])

    def _pair_deltas(pre_vals, post_vals):
        deltas, n_undef = [], 0
        for vp, vq in zip(pre_vals, post_vals):
            if vp is None or vq is None:
                n_undef += 1
            else:
                deltas.append(vq - vp)
        return np.array(deltas, dtype=float), n_undef

    delta_d_b_boot, n_undef_d_b = _pair_deltas(d_b_boot_pre, d_b_boot_post)
    delta_C_boot, n_undef_C = _pair_deltas(C_boot_pre, C_boot_post)

    result = {
        "bootstrap_block_length_pre": int(L_pre),
        "bootstrap_block_length_post": int(L_post),
        "bootstrap_n_bootstrap": int(n_bootstrap),
        "bootstrap_seed": int(seed),
    }
    for name, deltas, n_undef in (("d_B", delta_d_b_boot, n_undef_d_b),
                                   ("C", delta_C_boot, n_undef_C)):
        n_valid = len(deltas)
        if n_valid == 0:
            ci95, p, mean_d, std_d = (None, None), None, None, None
        else:
            ci95 = _percentile_ci95(deltas)
            p = _bootstrap_two_tailed_p(deltas)
            mean_d = float(np.mean(deltas))
            std_d = float(np.std(deltas))
        result[f"delta_{name}_boot_ci95"] = ci95
        result[f"p_bootstrap_{name}"] = p
        result[f"delta_{name}_boot_mean"] = mean_d
        result[f"delta_{name}_boot_std"] = std_d
        result[f"delta_{name}_boot_n_valid"] = n_valid
        result[f"delta_{name}_boot_n_undefined"] = n_undef

    return result


# --------------------------------------------------------------------------
# Full PRE/POST transition test pipeline (public entry point)
# --------------------------------------------------------------------------

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def run_vg_analysis(pre_series, post_series, seed=SEED, n_surrogates=N_SURROGATES,
                     n_iter=N_IAAFT_ITER, max_n=MAX_N_PER_SEGMENT,
                     l_b_min=L_B_MIN, divisor=L_B_MAX_DIAM_DIVISOR,
                     n_scales_cap=N_SCALES_CAP, r_repeats=R_REPEATS,
                     min_fit_points=MIN_FIT_POINTS,
                     run_bootstrap=False, n_bootstrap=N_BOOTSTRAP):
    """Run the full visibility-graph + box-covering transition test between
    a PRE and a POST segment, per METHODOLOGY_NOTE.md Gaps (a), (d), (e).

    Applies Gap (d) subsampling to PRE and POST independently BEFORE
    anything else (graph construction, box-covering, AND surrogate
    generation all operate on the subsampled series -- so IAAFT surrogates
    are exactly as long as the series actually analyzed).

    IAAFT is the PRIMARY significance test (Gap (e)): N_SURROGATES
    independent PRE/POST surrogate pairs, each generated from its OWN real
    (already-subsampled) segment, seed=12345. Two-tailed:
    p = fraction of surrogates with |Delta_real| <= |Delta_surrogate|.

    If `run_bootstrap=True`, ALSO runs the moving-block bootstrap
    (Kunsch 1989) fallback test (pre-authorized in METHODOLOGY_NOTE.md Gap
    (e) if synthetic validation shows IAAFT has insufficient power -- see
    VALIDATION_NOTE.md). Off by default so real-data runs do not pay its
    extra cost unless the validation step determined it is needed.

    Returns a dict with everything a downstream agent needs to report a
    result without recomputing anything -- see module docstring and inline
    keys for the full contract: l_B grids used, N_B per l_B, d_B
    (PRE/POST/Delta), C (PRE/POST/Delta), IAAFT null distributions,
    p-values, diagnostics (n used, whether subsampling was applied, n_scales
    achieved), and (if requested) the bootstrap fallback result.
    """
    pre_raw = np.asarray(pre_series, dtype=float)
    post_raw = np.asarray(post_series, dtype=float)

    pre, pre_sub_info = subsample_segment(pre_raw, max_n=max_n)
    post, post_sub_info = subsample_segment(post_raw, max_n=max_n)

    vg_kwargs = dict(l_b_min=l_b_min, divisor=divisor, n_scales_cap=n_scales_cap,
                      r_repeats=r_repeats, min_fit_points=min_fit_points)

    real_pre = compute_vg_features(pre, seed=seed, **vg_kwargs)
    real_post = compute_vg_features(post, seed=seed, **vg_kwargs)

    d_B_pre = None if real_pre["d_B"] is None else real_pre["d_B"]["d_B"]
    d_B_post = None if real_post["d_B"] is None else real_post["d_B"]["d_B"]
    C_pre = real_pre["C"]
    C_post = real_post["C"]

    delta_d_B_real = _delta(d_B_post, d_B_pre)
    delta_C_real = _delta(C_post, C_pre)

    rng = np.random.default_rng(seed)
    surr_delta_d_B = []
    surr_delta_C = []
    n_undef_d_B = 0
    n_undef_C = 0

    for _ in range(n_surrogates):
        surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
        surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)

        feat_pre_s = compute_vg_features(surr_pre, seed=seed, **vg_kwargs)
        feat_post_s = compute_vg_features(surr_post, seed=seed, **vg_kwargs)

        d_pre_s = None if feat_pre_s["d_B"] is None else feat_pre_s["d_B"]["d_B"]
        d_post_s = None if feat_post_s["d_B"] is None else feat_post_s["d_B"]["d_B"]
        d_delta = _delta(d_post_s, d_pre_s)
        if d_delta is None:
            n_undef_d_B += 1
        else:
            surr_delta_d_B.append(d_delta)

        c_delta = _delta(feat_post_s["C"], feat_pre_s["C"])
        if c_delta is None:
            n_undef_C += 1
        else:
            surr_delta_C.append(c_delta)

    surr_delta_d_B = np.array(surr_delta_d_B, dtype=float)
    surr_delta_C = np.array(surr_delta_C, dtype=float)

    if delta_d_B_real is None or len(surr_delta_d_B) == 0:
        p_d_B = None
    else:
        p_d_B = float(np.mean(np.abs(surr_delta_d_B) >= abs(delta_d_B_real)))

    if delta_C_real is None or len(surr_delta_C) == 0:
        p_C = None
    else:
        p_C = float(np.mean(np.abs(surr_delta_C) >= abs(delta_C_real)))

    result = {
        "real_pre": real_pre,
        "real_post": real_post,
        "d_B_pre": d_B_pre,
        "d_B_post": d_B_post,
        "C_pre": C_pre,
        "C_post": C_post,
        "delta_d_B": delta_d_B_real,
        "delta_C": delta_C_real,
        "p_d_B": p_d_B,
        "p_C": p_C,
        "surrogate_d_B_mean": float(np.mean(surr_delta_d_B)) if len(surr_delta_d_B) else None,
        "surrogate_d_B_std": float(np.std(surr_delta_d_B)) if len(surr_delta_d_B) else None,
        "surrogate_d_B_n_valid": int(len(surr_delta_d_B)),
        "surrogate_d_B_n_undefined": int(n_undef_d_B),
        "surrogate_C_mean": float(np.mean(surr_delta_C)) if len(surr_delta_C) else None,
        "surrogate_C_std": float(np.std(surr_delta_C)) if len(surr_delta_C) else None,
        "surrogate_C_n_valid": int(len(surr_delta_C)),
        "surrogate_C_n_undefined": int(n_undef_C),
        "diagnostics": {
            "pre_subsampling": pre_sub_info,
            "post_subsampling": post_sub_info,
            "pre_n_scales_achieved": real_pre["diagnostics"]["n_scales_achieved"],
            "post_n_scales_achieved": real_post["diagnostics"]["n_scales_achieved"],
            "pre_status": real_pre["status"],
            "post_status": real_post["status"],
        },
        "config": {
            "l_b_min": l_b_min,
            "l_b_max_diam_divisor": divisor,
            "n_scales_cap": n_scales_cap,
            "r_repeats": r_repeats,
            "min_fit_points": min_fit_points,
            "max_n_per_segment": max_n,
            "n_surrogates": n_surrogates,
            "n_iaaft_iter": n_iter,
            "seed": seed,
        },
    }

    if run_bootstrap:
        boot_result = run_block_bootstrap_test(
            pre, post, real_pre=real_pre, real_post=real_post,
            n_bootstrap=n_bootstrap, seed=seed, **vg_kwargs,
        )
        result.update(boot_result)

    return result
