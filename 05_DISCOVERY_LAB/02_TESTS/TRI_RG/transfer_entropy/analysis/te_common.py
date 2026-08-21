"""
Canonical bivariate/directional Transfer Entropy pipeline for
DISC-TRI-RG-001, candidate `transfer_entropy` (Schreiber 2000, *Phys.
Rev. Lett.* 85:461; Kraskov, Stoegbauer & Grassberger 2004, *Phys. Rev.
E* 69:066138; Frenzel & Pompe 2007, *Phys. Rev. Lett.* 99:204101;
Ragwitz & Kantz 2002, *Phys. Rev. E* 65:056201; Staniek & Lehnertz 2008,
*Phys. Rev. Lett.* 100:158101; Schreiber & Schmitz 1996; Quian Quiroga,
Kraskov, Kreuz & Grassberger 2002).

Fixed BEFORE running on any real domain (CHB-MIT EEG seizure onset,
Kahramanmaras Turkey earthquake doublet) -- see ../METHODOLOGY_NOTE.md
for the full rationale. Self-contained implementation for this test
line, per this lab's established per-candidate convention (fresh
implementation of IAAFT etc. even though the published method is the
same one used elsewhere in the lab). The Bandt-Pompe ordinal-pattern
code IS reused (imported, not reimplemented) from
`permutation_entropy/analysis/pe_common.py`, and the MI-based `tau`
estimator IS reused (imported) from `rqa/analysis/rqa_common.py`, per
explicit task instructions and METHODOLOGY_NOTE.md.

No IDTxl / JIDT available in this environment (checked before
implementing, not assumed) -- IDTxl is not on the PyPI index reachable
via this session's proxy; JIDT needs a JVM + jpype, also unavailable.
KSG-CMI implemented directly here and validated against known analytical
cases in validate_synthetic.py BEFORE any real-data use.
"""
import math
import os
import sys

import numpy as np
from scipy.spatial import cKDTree
from scipy.special import digamma

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", "rqa", "analysis"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", "permutation_entropy", "analysis"))
from rqa_common import estimate_tau  # noqa: E402  (audited, reused unmodified per METHODOLOGY_NOTE.md)
from pe_common import ordinal_pattern_codes  # noqa: E402  (audited, reused unmodified)

# ---------------------------------------------------------------------
# Fixed constants (METHODOLOGY_NOTE.md) -- identical for every domain
# this pipeline is ever applied to; no per-domain tuning.
# ---------------------------------------------------------------------
K_NN = 4                    # KSG-CMI neighbors AND Ragwitz-Kantz local-prediction neighbors
M_MAX = 10                  # Ragwitz-Kantz embedding-dimension search grid, m=1..M_MAX
U_HORIZON = 1                # prediction horizon (Schreiber 2000 default), NOT swept
M_SYM = 4                    # Bandt-Pompe ordinal order for Symbolic TE (reused from pe_common)
TAU_SYM = 1                  # Bandt-Pompe delay for Symbolic TE (reused from pe_common)
N_SYM_STATES = math.factorial(M_SYM)  # 24

MAX_N_PER_SEGMENT = 4000     # computational-budget cap, gap of METHODOLOGY_NOTE.md
N_ABS_MIN = 30                # absolute floor to attempt any TE computation at all
N_MIN_SUBWINDOW = 200         # sub-windowing floor (nonstationarity mitigation)
N_SUBWINDOWS_TARGET = 8       # sub-windowing target (not a guarantee)

N_SURROGATES = 200            # both IAAFT and circular-shift, per METHODOLOGY_NOTE.md
N_IAAFT_ITER = 50
SEED = 12345                  # IAAFT stream
SEED_SHIFT = 67890            # circular-shift stream, deliberately distinct

_EPS_SHRINK = 1.0 - 1e-10


# =======================================================================
# Own-history embedding selection: tau (reused MI-minimum) + Ragwitz-Kantz m
# =======================================================================

def select_tau(x):
    """tau via rqa_common.estimate_tau (Fraser & Swinney 1986 MI-minimum,
    ACF zero-crossing fallback); if that ALSO fails ("tau_not_resolved"),
    fall back to tau=1 (METHODOLOGY_NOTE.md's own-history-embedding
    tolerance argument -- distinct, and explicitly less strict, than the
    hard-reject convention used by rqa/largest_lyapunov_exponent for
    full Takens-attractor reconstruction)."""
    res = estimate_tau(x)
    if res["status"] == "ok":
        return int(res["tau"]), res["method"]
    return 1, "fallback_tau_1"


def ragwitz_kantz_m(x, tau, k_pred=K_NN, m_max=M_MAX):
    """Ragwitz & Kantz 2002 local-constant-prediction-error embedding
    dimension selection, tau FIXED (from select_tau above). Euclidean
    norm (own-history-embedding-selection role, distinct from the
    Chebyshev norm used by the KSG-CMI estimator itself -- two different
    roles, both fixed a priori per METHODOLOGY_NOTE.md).

    For each m in 1..m_max: build delay vectors X_i (dim m, delay tau),
    predict x_{i+1} as the mean of the k_pred nearest neighbors' next
    values (self excluded), normalized MSE = <(pred-actual)^2>/var(x).
    Returns (m_star, errors) -- m_star = argmin, ALWAYS resolves over the
    finite grid (no FNN-style non-convergence failure mode; the whole
    point of this criterion per METHODOLOGY_NOTE.md).
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    tau = int(tau)
    sigma2 = float(np.var(x))
    errors = []
    for m in range(1, m_max + 1):
        n_vec = n - (m - 1) * tau - U_HORIZON
        if n_vec < k_pred + 2 or sigma2 <= 0:
            errors.append(float("inf"))
            continue
        idx = np.arange(n_vec)[:, None] + np.arange(m)[None, :] * tau
        X = x[idx]                                  # (n_vec, m)
        last_col_index = idx[:, -1]                  # time index of the last embedding coordinate
        targets = x[last_col_index + U_HORIZON]       # x_{i+u}, u=1
        tree = cKDTree(X)
        kq = min(k_pred + 1, n_vec)
        _, nn_idx = tree.query(X, k=kq, p=2)
        if kq == 1:
            errors.append(float("inf"))
            continue
        nn_idx = nn_idx[:, 1:]                        # drop self (distance 0)
        preds = targets[nn_idx].mean(axis=1)
        mse = float(np.mean((preds - targets) ** 2))
        errors.append(mse / sigma2)
    errors = np.array(errors, dtype=float)
    if not np.any(np.isfinite(errors)):
        return None, errors.tolist()
    m_star = int(np.argmin(errors)) + 1
    return m_star, errors.tolist()


def own_history_embedding(x):
    """Full own-history embedding selection for one channel: tau (reused
    MI-minimum, tau=1 fallback) then Ragwitz-Kantz m. Returns a dict;
    status="embedding_not_resolved" only in the degenerate case where
    Ragwitz-Kantz cannot form even m=1 vectors (segment far too short)."""
    tau, tau_method = select_tau(x)
    m_star, errors = ragwitz_kantz_m(x, tau)
    if m_star is None:
        return {"status": "embedding_not_resolved", "tau": tau, "tau_method": tau_method,
                "rk_errors": errors}
    return {"status": "ok", "m": m_star, "tau": tau, "tau_method": tau_method,
            "rk_errors": errors}


# =======================================================================
# KSG-CMI estimator (Kraskov et al. 2004 / Frenzel & Pompe 2007) -> TE
# =======================================================================

def _embed_history(x, m, tau, t_indices):
    """History vectors [x[t], x[t-tau], ..., x[t-(m-1)*tau]] for each
    t in t_indices (all t assumed >= (m-1)*tau)."""
    x = np.asarray(x, dtype=float)
    offsets = np.arange(m) * tau
    idx = t_indices[:, None] - offsets[None, :]
    return x[idx]


def ksg_cmi(A, B, C, k=K_NN):
    """KSG conditional-mutual-information estimator, I(A;B|C)
    (Kraskov et al. 2004; Frenzel & Pompe 2007 eq. 8), Chebyshev/max
    norm throughout, self excluded, NO explicit Theiler-window exclusion
    (deliberate simplification, METHODOLOGY_NOTE.md). A, B, C: 2D arrays
    (N, dA)/(N, dB)/(N, dC), same N (row i is the same sample across all
    three). Returns a float (nats)."""
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)
    C = np.atleast_2d(C)
    if A.shape[0] != A.size and A.ndim == 1:
        pass
    N = A.shape[0]
    if N <= k + 1:
        return None
    joint = np.hstack([A, B, C])
    AC = np.hstack([A, C])
    BC = np.hstack([B, C])

    tree_joint = cKDTree(joint)
    kq = min(k + 1, N)
    dists, _ = tree_joint.query(joint, k=kq, p=np.inf)
    eps = dists[:, kq - 1]  # k-th neighbor distance (index 0 = self, distance 0)

    eps_search = np.where(eps > 0, eps * _EPS_SHRINK, 1e-12)

    tree_AC = cKDTree(AC)
    tree_BC = cKDTree(BC)
    tree_C = cKDTree(C)

    n_ac_lists = tree_AC.query_ball_point(AC, eps_search, p=np.inf)
    n_bc_lists = tree_BC.query_ball_point(BC, eps_search, p=np.inf)
    n_c_lists = tree_C.query_ball_point(C, eps_search, p=np.inf)

    n_ac = np.array([max(len(lst) - 1, 0) for lst in n_ac_lists], dtype=float)
    n_bc = np.array([max(len(lst) - 1, 0) for lst in n_bc_lists], dtype=float)
    n_c = np.array([max(len(lst) - 1, 0) for lst in n_c_lists], dtype=float)

    cmi = (digamma(k) - np.mean(digamma(n_ac + 1)) - np.mean(digamma(n_bc + 1))
           + np.mean(digamma(n_c + 1)))
    return float(cmi)


def te_ksg(x_source, y_target, mx, taux, my, tauy, u=U_HORIZON, k=K_NN):
    """TE(source->target) via KSG-CMI: A=Y_future, B=X_past, C=Y_past.
    Returns (te_value, n_points_used) or (None, 0) if the segment is too
    short for the given (mx,taux,my,tauy,u)."""
    x_source = np.asarray(x_source, dtype=float)
    y_target = np.asarray(y_target, dtype=float)
    N = min(len(x_source), len(y_target))
    start = max((mx - 1) * taux, (my - 1) * tauy)
    end = N - u
    if end <= start:
        return None, 0
    t_indices = np.arange(start, end)

    Yp = _embed_history(y_target, my, tauy, t_indices)
    Xp = _embed_history(x_source, mx, taux, t_indices)
    Yf = y_target[t_indices + u].reshape(-1, 1)

    val = ksg_cmi(Yf, Xp, Yp, k=k)
    return val, len(t_indices)


# =======================================================================
# Symbolic Transfer Entropy (Staniek & Lehnertz 2008), reusing
# pe_common.ordinal_pattern_codes (m=4, tau_BP=1, audited elsewhere)
# =======================================================================

def te_symbolic(x_source, y_target, m=M_SYM, tau=TAU_SYM, u=1, n_symbols=N_SYM_STATES):
    """Discrete/plug-in Symbolic Transfer Entropy (Schreiber 2000 formula
    applied to Bandt-Pompe ordinal-pattern symbols, Staniek & Lehnertz
    2008). History length = 1 SYMBOL (the symbol already encodes m raw
    samples of history -- standard STE convention). u=1 here is ONE
    SYMBOL STEP ahead, a different unit than u=1 RAW SAMPLE in te_ksg
    (named explicitly in METHODOLOGY_NOTE.md, not an inconsistency).
    Returns (te_value_bits, n_points_used) or (None, 0)."""
    sx = ordinal_pattern_codes(x_source, m=m, tau=tau)
    sy = ordinal_pattern_codes(y_target, m=m, tau=tau)
    N = min(len(sx), len(sy))
    if N <= u:
        return None, 0
    sx = sx[:N]
    sy = sy[:N]
    n_pts = N - u
    if n_pts < 1:
        return None, 0

    sy_future = sy[u:u + n_pts].astype(np.int64)
    sy_past = sy[:n_pts].astype(np.int64)
    sx_past = sx[:n_pts].astype(np.int64)

    ns = n_symbols
    idx_joint = (sy_future * ns + sy_past) * ns + sx_past
    counts_joint = np.bincount(idx_joint, minlength=ns ** 3).astype(float)

    idx_ypxp = sy_past * ns + sx_past
    counts_ypxp = np.bincount(idx_ypxp, minlength=ns * ns).astype(float)

    idx_yfyp = sy_future * ns + sy_past
    counts_yfyp = np.bincount(idx_yfyp, minlength=ns * ns).astype(float)

    counts_yp = np.bincount(sy_past, minlength=ns).astype(float)

    te = 0.0
    nz_idx = np.nonzero(counts_joint)[0]
    for idx in nz_idx:
        yf = idx // (ns * ns)
        rem = idx % (ns * ns)
        yp = rem // ns
        xp = rem % ns
        c_joint = counts_joint[idx]
        c_ypxp = counts_ypxp[yp * ns + xp]
        c_yfyp = counts_yfyp[yf * ns + yp]
        c_yp = counts_yp[yp]
        if c_ypxp <= 0 or c_yp <= 0:
            continue
        p_joint = c_joint / n_pts
        p_yf_given_yp_xp = c_joint / c_ypxp
        p_yf_given_yp = c_yfyp / c_yp
        if p_yf_given_yp_xp > 0 and p_yf_given_yp > 0:
            te += p_joint * math.log2(p_yf_given_yp_xp / p_yf_given_yp)
    return float(te), int(n_pts)


# =======================================================================
# Sub-windowing scheme (nonstationarity mitigation, METHODOLOGY_NOTE.md)
# =======================================================================

def subwindow_scheme(n, n_min_subwindow=N_MIN_SUBWINDOW, n_target=N_SUBWINDOWS_TARGET,
                      n_abs_min=N_ABS_MIN):
    """Returns (boundaries, status) where boundaries is a list of
    (start,end) index pairs (contiguous, non-overlapping, half-open),
    status in {"insufficient_samples","single_window","subwindowed"}."""
    if n < n_abs_min:
        return [], "insufficient_samples"
    if n < n_min_subwindow:
        return [(0, n)], "single_window"
    l_sub = max(n_min_subwindow, n // n_target)
    n_sub = n // l_sub
    if n_sub <= 1:
        return [(0, n)], "single_window"
    boundaries = [(i * l_sub, (i + 1) * l_sub) for i in range(n_sub)]
    return boundaries, "subwindowed"


def _subsample_pair(x, y, max_n=MAX_N_PER_SEGMENT):
    """ONE stride decision (from the shared length) applied IDENTICALLY
    to both channels -- preserves exact temporal pairing between X and Y
    (distinct from the independent per-channel decimation used by
    univariate candidates elsewhere in this lab, METHODOLOGY_NOTE.md)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = min(len(x), len(y))
    x, y = x[:n], y[:n]
    if n <= max_n:
        return x, y, {"n_original": int(n), "n_used": int(n), "stride": 1, "subsampled": False}
    stride = int(np.ceil(n / max_n))
    xd, yd = x[::stride], y[::stride]
    return xd, yd, {"n_original": int(n), "n_used": int(len(xd)), "stride": int(stride), "subsampled": True}


# =======================================================================
# Aggregate TE (both directions, both estimators) over a sub-windowed segment
# =======================================================================

def aggregate_segment_te(x, y, mx, taux, my, tauy):
    """Compute TE_XY/TE_YX (KSG) and STE_XY/STE_YX (Symbolic) per
    sub-window of (x,y), aggregate each by MEDIAN across sub-windows
    (METHODOLOGY_NOTE.md). Returns a dict with per-subwindow raw values
    (transparency) and the aggregated (median) primary/companion
    channels: TE_net, TE_sum, STE_net, STE_sum."""
    n = min(len(x), len(y))
    boundaries, sw_status = subwindow_scheme(n)
    if sw_status == "insufficient_samples":
        return {"status": "insufficient_samples", "n": int(n)}

    te_xy_list, te_yx_list = [], []
    ste_xy_list, ste_yx_list = [], []
    n_valid_ksg, n_valid_sym = 0, 0

    for (s, e) in boundaries:
        xs, ys = x[s:e], y[s:e]
        te_xy, _ = te_ksg(xs, ys, mx, taux, my, tauy)
        te_yx, _ = te_ksg(ys, xs, my, tauy, mx, taux)
        if te_xy is not None and te_yx is not None:
            te_xy_list.append(te_xy)
            te_yx_list.append(te_yx)
            n_valid_ksg += 1

        ste_xy, _ = te_symbolic(xs, ys)
        ste_yx, _ = te_symbolic(ys, xs)
        if ste_xy is not None and ste_yx is not None:
            ste_xy_list.append(ste_xy)
            ste_yx_list.append(ste_yx)
            n_valid_sym += 1

    result = {
        "status": "ok",
        "n": int(n),
        "subwindow_status": sw_status,
        "n_subwindows_scheme": len(boundaries),
        "n_subwindows_valid_ksg": n_valid_ksg,
        "n_subwindows_valid_symbolic": n_valid_sym,
        "TE_XY_per_subwindow": te_xy_list,
        "TE_YX_per_subwindow": te_yx_list,
        "STE_XY_per_subwindow": ste_xy_list,
        "STE_YX_per_subwindow": ste_yx_list,
    }
    if n_valid_ksg > 0:
        te_xy_med = float(np.median(te_xy_list))
        te_yx_med = float(np.median(te_yx_list))
        result["TE_XY"] = te_xy_med
        result["TE_YX"] = te_yx_med
        result["TE_net"] = te_xy_med - te_yx_med
        result["TE_sum"] = te_xy_med + te_yx_med
    else:
        result["TE_XY"] = result["TE_YX"] = result["TE_net"] = result["TE_sum"] = None
    if n_valid_sym > 0:
        ste_xy_med = float(np.median(ste_xy_list))
        ste_yx_med = float(np.median(ste_yx_list))
        result["STE_XY"] = ste_xy_med
        result["STE_YX"] = ste_yx_med
        result["STE_net"] = ste_xy_med - ste_yx_med
        result["STE_sum"] = ste_xy_med + ste_yx_med
    else:
        result["STE_XY"] = result["STE_YX"] = result["STE_net"] = result["STE_sum"] = None
    return result


# =======================================================================
# Surrogate constructions
# =======================================================================

def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate
    (Schreiber & Schmitz 1996). Fresh reimplementation for this
    candidate (per-candidate self-containment convention in this lab)."""
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


def circular_shift_pair(x, y, rng, mx=1, taux=1, my=1, tauy=1):
    """Quian Quiroga et al. 2002 circular-shift surrogate: X unchanged,
    Y circularly shifted by a random offset in
    [min_shift, N-min_shift], min_shift=max(N//10, mx*taux, my*tauy, 10)
    (METHODOLOGY_NOTE.md). Returns (x, y_shifted, shift_amount)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = min(len(x), len(y))
    x, y = x[:n], y[:n]
    min_shift = max(n // 10, mx * taux, my * tauy, 10)
    min_shift = min(min_shift, max(n - 1, 1))
    if n - min_shift <= min_shift:
        shift = n // 2 if n > 1 else 0
    else:
        shift = int(rng.integers(min_shift, n - min_shift + 1))
    y_shift = np.roll(y, shift)
    return x, y_shift, int(shift)


# =======================================================================
# Full PRE/POST transition test (public entry point)
# =======================================================================

def _delta(post_val, pre_val):
    return None if (post_val is None or pre_val is None) else (post_val - pre_val)


def _two_tailed_p(real_delta, surr_deltas):
    surr_deltas = np.asarray([d for d in surr_deltas if d is not None], dtype=float)
    if real_delta is None or len(surr_deltas) == 0:
        return None, int(len(surr_deltas))
    p = float(np.mean(np.abs(surr_deltas) >= abs(real_delta)))
    return p, int(len(surr_deltas))


def run_te_analysis(pre_x, pre_y, post_x, post_y,
                     seed=SEED, seed_shift=SEED_SHIFT,
                     n_surrogates=N_SURROGATES, n_iaaft_iter=N_IAAFT_ITER,
                     max_n=MAX_N_PER_SEGMENT):
    """Full bivariate TE PRE/POST transition test, per
    METHODOLOGY_NOTE.md. Single entry point for real-data / synthetic
    scripts -- called WITHOUT modification.

    pre_x/pre_y, post_x/post_y: paired (simultaneous) channel arrays.

    Returns a dict: status ("ok" / "insufficient_samples" /
    "embedding_not_resolved"), embedding info for both channels, real
    PRE/POST aggregated TE_net/TE_sum/STE_net/STE_sum, deltas, and BOTH
    surrogate-null p-values (IAAFT primary + circular-shift companion)
    for all 4 channels, plus config (full provenance).
    """
    pre_x_s, pre_y_s, pre_sub_info = _subsample_pair(pre_x, pre_y, max_n=max_n)
    post_x_s, post_y_s, post_sub_info = _subsample_pair(post_x, post_y, max_n=max_n)

    emb_x = own_history_embedding(pre_x_s)
    emb_y = own_history_embedding(pre_y_s)

    config = {
        "k_nn": K_NN, "m_max": M_MAX, "u_horizon": U_HORIZON,
        "m_sym": M_SYM, "tau_sym": TAU_SYM,
        "max_n_per_segment": max_n, "n_abs_min": N_ABS_MIN,
        "n_min_subwindow": N_MIN_SUBWINDOW, "n_subwindows_target": N_SUBWINDOWS_TARGET,
        "n_surrogates": n_surrogates, "n_iaaft_iter": n_iaaft_iter,
        "seed": seed, "seed_shift": seed_shift,
        "pre_subsample_info": pre_sub_info, "post_subsample_info": post_sub_info,
        "embedding_x": emb_x, "embedding_y": emb_y,
    }

    if emb_x["status"] != "ok" or emb_y["status"] != "ok":
        return {"status": "embedding_not_resolved", "config": config}

    mx, taux = emb_x["m"], emb_x["tau"]
    my, tauy = emb_y["m"], emb_y["tau"]

    real_pre = aggregate_segment_te(pre_x_s, pre_y_s, mx, taux, my, tauy)
    real_post = aggregate_segment_te(post_x_s, post_y_s, mx, taux, my, tauy)

    if real_pre["status"] != "ok" or real_post["status"] != "ok":
        return {"status": "insufficient_samples", "real_pre": real_pre,
                "real_post": real_post, "config": config}

    channels = ["TE_net", "TE_sum", "STE_net", "STE_sum"]
    delta_real = {ch: _delta(real_post.get(ch), real_pre.get(ch)) for ch in channels}

    rng_iaaft = np.random.default_rng(seed)
    rng_shift = np.random.default_rng(seed_shift)

    surr_deltas_iaaft = {ch: [] for ch in channels}
    surr_deltas_shift = {ch: [] for ch in channels}

    for _ in range(n_surrogates):
        # --- IAAFT: per-channel independent surrogates, PRE and POST separately ---
        surr_pre_x = iaaft_surrogate(pre_x_s, n_iter=n_iaaft_iter, rng=rng_iaaft)
        surr_pre_y = iaaft_surrogate(pre_y_s, n_iter=n_iaaft_iter, rng=rng_iaaft)
        surr_post_x = iaaft_surrogate(post_x_s, n_iter=n_iaaft_iter, rng=rng_iaaft)
        surr_post_y = iaaft_surrogate(post_y_s, n_iter=n_iaaft_iter, rng=rng_iaaft)

        agg_pre_i = aggregate_segment_te(surr_pre_x, surr_pre_y, mx, taux, my, tauy)
        agg_post_i = aggregate_segment_te(surr_post_x, surr_post_y, mx, taux, my, tauy)
        for ch in channels:
            d = _delta(agg_post_i.get(ch) if agg_post_i["status"] == "ok" else None,
                       agg_pre_i.get(ch) if agg_pre_i["status"] == "ok" else None)
            surr_deltas_iaaft[ch].append(d)

        # --- circular shift: Y shifted relative to X, PRE and POST separately ---
        s_pre_x, s_pre_y, _ = circular_shift_pair(pre_x_s, pre_y_s, rng_shift, mx, taux, my, tauy)
        s_post_x, s_post_y, _ = circular_shift_pair(post_x_s, post_y_s, rng_shift, mx, taux, my, tauy)

        agg_pre_c = aggregate_segment_te(s_pre_x, s_pre_y, mx, taux, my, tauy)
        agg_post_c = aggregate_segment_te(s_post_x, s_post_y, mx, taux, my, tauy)
        for ch in channels:
            d = _delta(agg_post_c.get(ch) if agg_post_c["status"] == "ok" else None,
                       agg_pre_c.get(ch) if agg_pre_c["status"] == "ok" else None)
            surr_deltas_shift[ch].append(d)

    p_iaaft, n_iaaft_valid = {}, {}
    p_shift, n_shift_valid = {}, {}
    for ch in channels:
        p_iaaft[ch], n_iaaft_valid[ch] = _two_tailed_p(delta_real[ch], surr_deltas_iaaft[ch])
        p_shift[ch], n_shift_valid[ch] = _two_tailed_p(delta_real[ch], surr_deltas_shift[ch])

    return {
        "status": "ok",
        "real_pre": real_pre,
        "real_post": real_post,
        "delta": delta_real,
        "p_iaaft": p_iaaft,
        "n_iaaft_valid": n_iaaft_valid,
        "p_circular_shift": p_shift,
        "n_circular_shift_valid": n_shift_valid,
        "surrogate_deltas_iaaft": surr_deltas_iaaft,
        "surrogate_deltas_circular_shift": surr_deltas_shift,
        "config": config,
    }
