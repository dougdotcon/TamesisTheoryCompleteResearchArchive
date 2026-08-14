"""
Canonical wavelet log-cumulant (WCM) pipeline for DISC-TRI-RG-001, candidate
`wavelet-multiresolution-scaling`.

Fixed BEFORE running on any real domain (seismology/Tohoku, EEG seizure/CHB-MIT)
-- see ../METHODOLOGY_NOTE.md for the full rationale, including the honest
substitution of the wavelet-leader/WTMM maxima-line method (mentioned in Phase 0)
for the computationally tractable wavelet-coefficient log-cumulant method (WCM),
a standard, citable variant of the same log-cumulant multifractal formalism
(Castaing, Gagne & Hopfinger 1990; Delbeke & Abry 2000; Wendt, Abry & Jaffard 2007).

All scale/window parameters are fixed constants applied identically across every
domain -- no per-domain tuning. Any agent analyzing a domain MUST import and call
the functions here rather than reimplementing them, so "same formula, no
per-domain reformulation" is a literal code-identity guarantee.
"""
import numpy as np
import pywt

WAVELET = "db4"                 # Daubechies, 4 vanishing moments -- fixed for all domains
MIN_COEFFS_PER_SCALE = 16       # scales with fewer wavelet coefficients than this are dropped
N_SURROGATES = 200              # IAAFT surrogate pairs (Schreiber & Schmitz 1996)
N_IAAFT_ITER = 50               # IAAFT iterations per surrogate
SEED = 12345


def log_cumulants(x, wavelet=WAVELET, min_coeffs=MIN_COEFFS_PER_SCALE):
    """Wavelet-coefficient log-cumulant multifractal analysis (WCM).

    Returns C1_slope (~ H + 0.5, up to the fixed normalization implied by this
    wavelet/mode choice) and C2_slope (second-order log-cumulant: 0 for an exactly
    monofractal process, negative for a genuine multifractal cascade), estimated
    by linear regression of the per-scale sample mean / variance of log2|d_j,k|
    against scale index j (j=1 finest ... j=n_levels coarsest).
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    max_level = pywt.dwt_max_level(n, pywt.Wavelet(wavelet).dec_len)
    coeffs = pywt.wavedec(x, wavelet, level=max_level, mode="periodization")
    detail_coeffs = coeffs[1:]  # coeffs[0] = coarsest approximation; rest = detail, coarsest first
    n_levels = len(detail_coeffs)

    js, c1s, c2s, counts = [], [], [], []
    for idx, d in enumerate(detail_coeffs):
        j = n_levels - idx  # idx=0 (coarsest detail) -> j=n_levels ... idx=last (finest) -> j=1
        d = np.asarray(d, dtype=float)
        d = d[np.abs(d) > 1e-300]
        if len(d) < min_coeffs:
            continue
        logabs = np.log2(np.abs(d))
        js.append(j)
        c1s.append(float(np.mean(logabs)))
        c2s.append(float(np.var(logabs, ddof=1)))
        counts.append(int(len(d)))

    js = np.array(js, dtype=float)
    c1s = np.array(c1s, dtype=float)
    c2s = np.array(c2s, dtype=float)
    order = np.argsort(js)
    js, c1s, c2s = js[order], c1s[order], c2s[order]

    if len(js) < 3:
        raise ValueError(
            f"Only {len(js)} usable scales (need >=3 for a regression) -- "
            f"segment too short for wavelet '{wavelet}' with min_coeffs={min_coeffs}."
        )

    C1_slope, C1_intercept = np.polyfit(js, c1s, 1)
    C2_slope, C2_intercept = np.polyfit(js, c2s, 1)

    return {
        "n_levels_used": int(len(js)),
        "j_values": js.tolist(),
        "mean_logabs_per_j": c1s.tolist(),
        "var_logabs_per_j": c2s.tolist(),
        "coeff_counts_per_j": counts,
        "C1_slope": float(C1_slope),
        "C1_intercept": float(C1_intercept),
        "C2_slope": float(C2_slope),
        "C2_intercept": float(C2_intercept),
        "n_samples": int(n),
        "wavelet": wavelet,
        "min_coeffs_per_scale": min_coeffs,
    }


def iaaft_surrogate(x, n_iter=N_IAAFT_ITER, rng=None):
    """Iterative Amplitude Adjusted Fourier Transform surrogate (Schreiber & Schmitz 1996).

    Preserves the linear power spectrum (hence H/monofractal scaling) and the exact
    amplitude distribution of x, destroys higher-order nonlinear phase structure."""
    if rng is None:
        rng = np.random.default_rng()
    x = np.asarray(x, dtype=float)
    n = len(x)
    sorted_x = np.sort(x)
    amp_spectrum = np.abs(np.fft.rfft(x))
    surrogate = rng.permutation(x).astype(float)
    for _ in range(n_iter):
        fft_surr = np.fft.rfft(surrogate)
        phases = np.angle(fft_surr)
        new_fft = amp_spectrum * np.exp(1j * phases)
        surrogate = np.fft.irfft(new_fft, n=n)
        ranks = np.argsort(np.argsort(surrogate))
        surrogate = sorted_x[ranks]
    return surrogate


def transition_test(pre, post, n_surrogates=N_SURROGATES, n_iter=N_IAAFT_ITER, seed=SEED):
    """Two-tailed IAAFT surrogate test for a genuine multifractal-structure change
    between a PRE and a POST segment (see METHODOLOGY_NOTE.md gap 3)."""
    rng = np.random.default_rng(seed)
    pre = np.asarray(pre, dtype=float)
    post = np.asarray(post, dtype=float)

    real_pre = log_cumulants(pre)
    real_post = log_cumulants(post)
    real_dC2 = real_post["C2_slope"] - real_pre["C2_slope"]
    real_dC1 = real_post["C1_slope"] - real_pre["C1_slope"]

    surr_dC2 = np.empty(n_surrogates)
    surr_dC1 = np.empty(n_surrogates)
    failures = 0
    for i in range(n_surrogates):
        try:
            surr_pre = iaaft_surrogate(pre, n_iter=n_iter, rng=rng)
            surr_post = iaaft_surrogate(post, n_iter=n_iter, rng=rng)
            lc_pre = log_cumulants(surr_pre)
            lc_post = log_cumulants(surr_post)
            surr_dC2[i] = lc_post["C2_slope"] - lc_pre["C2_slope"]
            surr_dC1[i] = lc_post["C1_slope"] - lc_pre["C1_slope"]
        except ValueError:
            surr_dC2[i] = np.nan
            surr_dC1[i] = np.nan
            failures += 1

    valid2 = surr_dC2[~np.isnan(surr_dC2)]
    valid1 = surr_dC1[~np.isnan(surr_dC1)]
    p_dC2 = float(np.mean(np.abs(valid2) >= abs(real_dC2))) if len(valid2) else float("nan")
    p_dC1 = float(np.mean(np.abs(valid1) >= abs(real_dC1))) if len(valid1) else float("nan")

    return {
        "real_pre": real_pre,
        "real_post": real_post,
        "real_dC2": float(real_dC2),
        "real_dC1": float(real_dC1),
        "p_dC2_twotail": p_dC2,
        "p_dC1_twotail": p_dC1,
        "n_surrogates_requested": int(n_surrogates),
        "n_surrogate_failures": int(failures),
        "surrogate_dC2_mean": float(np.mean(valid2)) if len(valid2) else None,
        "surrogate_dC2_std": float(np.std(valid2)) if len(valid2) else None,
        "surrogate_dC1_mean": float(np.mean(valid1)) if len(valid1) else None,
        "surrogate_dC1_std": float(np.std(valid1)) if len(valid1) else None,
    }
