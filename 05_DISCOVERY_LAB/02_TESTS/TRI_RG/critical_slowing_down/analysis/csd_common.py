"""
Canonical Critical Slowing Down (CSD) analysis pipeline for DISC-TRI-RG-001.

Fixed BEFORE running on any of the 3 target domains (GISP2, PhysioNet SDDB,
NASDAQ) -- see ../METHODOLOGY_NOTE.md for the rationale. All scale parameters
are FRACTIONS of the input segment length, never absolute physical units, so
this module is called unmodified across every domain (no per-domain tuning).

Any agent/script analyzing a domain MUST import and call run_csd_pipeline()
from here rather than reimplementing the pipeline, so "same formula, no
per-domain reformulation" is a literal code-identity guarantee, not just a
methodological intention.
"""
import numpy as np
from scipy.stats import kendalltau

BANDWIDTH_FRAC = 0.20   # Gaussian kernel detrend bandwidth (Dakos et al. 2012 default)
WINDOW_FRAC = 0.50      # rolling window size for AC1/variance (Dakos et al. 2012 default)
STEP_FRAC = 0.02        # rolling window step size
N_SURROGATES = 1000     # AR(1) constant-parameter surrogate count (Dakos et al. 2008 PNAS)
SEED = 12345


def gaussian_detrend(x, bandwidth_frac=BANDWIDTH_FRAC):
    x = np.asarray(x, dtype=float)
    n = len(x)
    bw = max(1.0, bandwidth_frac * n)
    idx = np.arange(n)
    trend = np.empty(n)
    for i in idx:
        w = np.exp(-0.5 * ((idx - i) / bw) ** 2)
        trend[i] = np.sum(w * x) / np.sum(w)
    return x - trend, trend


def rolling_ac1_variance(residuals, window_frac=WINDOW_FRAC, step_frac=STEP_FRAC):
    residuals = np.asarray(residuals, dtype=float)
    n = len(residuals)
    win = max(10, int(round(window_frac * n)))
    step = max(1, int(round(step_frac * n)))
    ac1_vals, var_vals, centers = [], [], []
    start = 0
    while start + win <= n:
        seg = residuals[start:start + win]
        ac1 = np.corrcoef(seg[:-1], seg[1:])[0, 1]
        var = np.var(seg, ddof=1)
        ac1_vals.append(ac1)
        var_vals.append(var)
        centers.append(start + win / 2.0)
        start += step
    return np.array(centers), np.array(ac1_vals), np.array(var_vals)


def kendall_trend(centers, values):
    tau, p = kendalltau(centers, values)
    return float(tau), float(p)


def fit_ar1(residuals):
    residuals = np.asarray(residuals, dtype=float)
    x = residuals[:-1]
    y = residuals[1:]
    a = float(np.sum(x * y) / np.sum(x * x))
    eps = y - a * x
    sigma = float(np.std(eps, ddof=1))
    return a, sigma


def generate_ar1_surrogate(n, a, sigma, rng):
    x = np.empty(n)
    x[0] = rng.normal(0, sigma / np.sqrt(max(1e-12, 1 - a ** 2)))
    for t in range(1, n):
        x[t] = a * x[t - 1] + rng.normal(0, sigma)
    return x


def surrogate_null_test(residuals, n_surrogates=N_SURROGATES, seed=SEED):
    rng = np.random.default_rng(seed)
    a, sigma = fit_ar1(residuals)
    n = len(residuals)
    real_centers, real_ac1, real_var = rolling_ac1_variance(residuals)
    real_tau_ac1, _ = kendall_trend(real_centers, real_ac1)
    real_tau_var, _ = kendall_trend(real_centers, real_var)

    surr_tau_ac1 = np.empty(n_surrogates)
    surr_tau_var = np.empty(n_surrogates)
    for i in range(n_surrogates):
        surr = generate_ar1_surrogate(n, a, sigma, rng)
        c, ac1s, vars_ = rolling_ac1_variance(surr)
        surr_tau_ac1[i], _ = kendall_trend(c, ac1s)
        surr_tau_var[i], _ = kendall_trend(c, vars_)

    p_ac1 = float(np.mean(surr_tau_ac1 >= real_tau_ac1))
    p_var = float(np.mean(surr_tau_var >= real_tau_var))
    return {
        "ar1_a": a,
        "ar1_sigma": sigma,
        "real_tau_ac1": real_tau_ac1,
        "real_tau_var": real_tau_var,
        "p_ac1_onetail": p_ac1,
        "p_var_onetail": p_var,
        "n_surrogates": n_surrogates,
        "surrogate_tau_ac1_mean": float(np.mean(surr_tau_ac1)),
        "surrogate_tau_ac1_std": float(np.std(surr_tau_ac1)),
        "surrogate_tau_var_mean": float(np.mean(surr_tau_var)),
        "surrogate_tau_var_std": float(np.std(surr_tau_var)),
    }


def run_csd_pipeline(x):
    """x: 1-D array of the pre-transition segment values (already time-ordered,
    any units). Segment SELECTION (which rows count as "pre-transition", and
    the primary-vs-robustness split) happens OUTSIDE this function, identically
    across domains per METHODOLOGY_NOTE.md -- this function only implements the
    fixed-fraction detrend/window/surrogate pipeline itself."""
    x = np.asarray(x, dtype=float)
    residuals, trend = gaussian_detrend(x)
    result = surrogate_null_test(residuals)
    result["n_samples"] = int(len(x))
    result["bandwidth_frac"] = BANDWIDTH_FRAC
    result["window_frac"] = WINDOW_FRAC
    result["step_frac"] = STEP_FRAC
    return result
