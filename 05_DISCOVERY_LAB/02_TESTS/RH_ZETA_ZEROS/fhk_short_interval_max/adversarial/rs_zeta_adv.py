"""Adversarial, from-scratch Riemann-Siegel Z(t) evaluator.

Written for the adversarial reproduction of DISC-RH-FHK-SHORT-INTERVAL-MAX-001
WITHOUT reading the primary's engine (rs_zeta.py) or any primary code.

    Z(t) = 2 * sum_{n=1}^{N} cos(theta(t) - t*ln n)/sqrt(n)
           + (-1)^(N-1) * (t/2pi)^(-1/4) * Psi(p)

with a = sqrt(t/2pi), N = floor(a), p = a - N,
Psi(p) = cos(2pi(p^2 - p - 1/16))/cos(2pi p) (removable singularities at
p = 1/4, 3/4 handled by 6th-order local Taylor series derived symbolically
in sympy_psi_coeffs.py), and

    theta(t) = Im log Gamma(1/4 + i t/2) - (t/2) ln pi   (exact, scipy).

First-order (C0-only) remainder: rigorous error bound (Gabcke 1979)
|err| <= 0.053 * (t/2pi)^(-3/4)  => <= 2.2e-4 at t = 1e4, smaller above.
"""

import numpy as np
from scipy.special import loggamma

TWO_PI = 2.0 * np.pi
LN_PI = np.log(np.pi)

# Taylor coefficients of Psi around p0 = 1/4 (sympy_psi_coeffs.py output).
# Around p0 = 3/4 the coefficients are a_k * (-1)^k for k odd sign-flipped:
# derived independently; both sets pasted verbatim from the sympy run.
_PSI_TAYLOR_14 = np.array([
    0.50000000000000000000,
    -1.0000000000000000000,
    2.4674011002723396547,
    -1.6449340668482264365,
    0.27717591495256192663,
    4.6856706083984139107,
    -7.9790310669362389940,
])
_PSI_TAYLOR_34 = np.array([
    0.50000000000000000000,
    1.0000000000000000000,
    2.4674011002723396547,
    1.6449340668482264365,
    0.27717591495256192663,
    -4.6856706083984139107,
    -7.9790310669362389940,
])
_SING_HALFWIDTH = 0.03


def psi_rs(p):
    """Psi(p) = cos(2pi(p^2-p-1/16))/cos(2pi p), vectorized, p in [0,1)."""
    p = np.asarray(p, dtype=np.float64)
    num = np.cos(TWO_PI * (p * p - p - 0.0625))
    den = np.cos(TWO_PI * p)
    near14 = np.abs(p - 0.25) < _SING_HALFWIDTH
    near34 = np.abs(p - 0.75) < _SING_HALFWIDTH
    safe_den = np.where(near14 | near34, 1.0, den)
    out = num / safe_den
    if np.any(near14):
        dp = p[near14] - 0.25
        out[near14] = np.polyval(_PSI_TAYLOR_14[::-1], dp)
    if np.any(near34):
        dp = p[near34] - 0.75
        out[near34] = np.polyval(_PSI_TAYLOR_34[::-1], dp)
    return out


def theta_rs(t):
    """Riemann-Siegel theta, exact via complex loggamma."""
    t = np.asarray(t, dtype=np.float64)
    z = 0.25 + 0.5j * t
    return np.imag(loggamma(z)) - 0.5 * t * LN_PI


class ZEvaluator:
    """Vectorized Z(t) with per-height cached ln n / 1/sqrt(n) tables."""

    def __init__(self, max_chunk_elems=12_000_000):
        self.max_chunk_elems = int(max_chunk_elems)
        self._nmax_cached = 0
        self._lnn = None
        self._invsqrtn = None

    def _ensure_tables(self, nmax):
        if nmax > self._nmax_cached:
            n = np.arange(1, nmax + 1, dtype=np.float64)
            self._lnn = np.log(n)
            self._invsqrtn = 1.0 / np.sqrt(n)
            self._nmax_cached = nmax

    def z(self, t):
        """Z(t) for a 1-D array of t (t >= ~500 for stated accuracy)."""
        t = np.asarray(t, dtype=np.float64)
        a = np.sqrt(t / TWO_PI)
        N = np.floor(a).astype(np.int64)
        p = a - N
        nmax = int(N.max())
        self._ensure_tables(nmax)
        theta = theta_rs(t)

        out = np.empty_like(t)
        rows_per_chunk = max(1, self.max_chunk_elems // nmax)
        for i0 in range(0, t.size, rows_per_chunk):
            sl = slice(i0, min(i0 + rows_per_chunk, t.size))
            tt = t[sl]
            th = theta[sl]
            NN = N[sl]
            nm = int(NN.max())
            phase = th[:, None] - np.outer(tt, self._lnn[:nm])
            terms = np.cos(phase)
            terms *= self._invsqrtn[:nm][None, :]
            # mask n <= N(t): n index j corresponds to n = j+1
            mask = (np.arange(1, nm + 1)[None, :] <= NN[:, None])
            terms *= mask
            out[sl] = 2.0 * terms.sum(axis=1)

        remainder = (np.where(N % 2 == 1, 1.0, -1.0)
                     * (t / TWO_PI) ** -0.25 * psi_rs(p))
        return out + remainder

    def max_log_abs_z(self, t0, n_grid=512):
        """M*(t0) = max over the locked grid of log|Z(t)|.

        Grid: t0 + j*(2pi/n_grid), j = 0..n_grid-1 (half-open [t0, t0+2pi)).
        """
        step = TWO_PI / n_grid
        tgrid = t0 + step * np.arange(n_grid)
        z = self.z(tgrid)
        return float(np.max(np.log(np.abs(z))))


# ---- locked design: offsets ----

HEIGHTS = [1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10]
M_PER_HEIGHT = [2000, 2000, 2000, 2000, 2000, 1600, 1000]
N_CAL = [80, 80, 60, 60, 24, 16, 8]
PRIMARY_SEED_BASE = 20260822
CAL_SEED_BASE = 77770707


def primary_starts(k):
    """Locked offsets: sort(default_rng(20260822*100+k).uniform(T, 2T, M))."""
    T = HEIGHTS[k]
    M = M_PER_HEIGHT[k]
    rng = np.random.default_rng(PRIMARY_SEED_BASE * 100 + k)
    return np.sort(rng.uniform(T, 2 * T, M))


def calibration_starts(k):
    """Disposable-band offsets for my own grid-bias calibration.

    Spec gives seed 77770707 and band [2T+10, 2.1T] but not the exact law;
    adopted (declared in ADVERSARIAL_NOTE.md): per-height rng
    default_rng(77770707*100+k), uniform on [2T+10, hi], hi = 2.1T except
    k=6 where hi = 2.1T - 2pi so no grid point exceeds 2.1e10 (sealed
    holdout untouched). Second-order impact only (|c_T| < 0.005).
    """
    T = HEIGHTS[k]
    lo = 2 * T + 10
    hi = 2.1 * T - (TWO_PI if k == 6 else 0.0)
    rng = np.random.default_rng(CAL_SEED_BASE * 100 + k)
    return np.sort(rng.uniform(lo, hi, N_CAL[k]))
