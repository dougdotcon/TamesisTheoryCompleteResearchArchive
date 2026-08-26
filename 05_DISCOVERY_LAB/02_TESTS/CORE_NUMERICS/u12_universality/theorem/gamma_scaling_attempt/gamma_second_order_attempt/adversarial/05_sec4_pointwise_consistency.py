"""
Internal-consistency check of Sec 4's pointwise heuristic:

  A_k/e^{-s(k)} - 1  ~=  Q(k;n,gamma) := k*gamma(1-gamma)/(2n)
                                          - k^3[1-(1-gamma)^3]/(6 n^2)
                                          + k^3 gamma(1-gamma)^3/(2 n^2)

at k = Theta(sqrt(n)) (the range that actually dominates the sum
Sum_k e^{-s(k)} * (A_k/e^{-s(k)} - 1) = E_n).

This is NOT a proof-level check (Sec 4 is explicitly heuristic / not
claimed proved) -- it is exactly what the mandate calls "internal
consistency": does the pointwise approximation actually track the exact
A_k at the k-scale that matters, with error shrinking as n grows (as a
genuine o(1)-per-term statement should)?

Built independently: A_k evaluated via the same O(1)-per-(k,m) cumulative
log-product trick as script 04, but here evaluated exactly (no k-truncation
needed since we only look at individual k values), for k drawn from the
sqrt(n) *typical* scale k = round(t*sqrt(n/beta)) for a few t.
"""
import numpy as np
from scipy.stats import binom
from scipy.special import logsumexp


def build_cumlog(n):
    j = np.arange(0, n, dtype=np.float64)
    h = np.log1p(-j / n)
    return np.concatenate(([0.0], np.cumsum(h)))


def A_k_exact(k, n, gamma, cumlog, std_width=15.0):
    mean = gamma * k
    sd = np.sqrt(max(k * gamma * (1 - gamma), 1e-300))
    lo = max(0, int(np.floor(mean - std_width * sd)) - 1)
    hi = min(k, int(np.ceil(mean + std_width * sd)) + 1)
    m = np.arange(lo, hi + 1)
    logP = cumlog[k] - cumlog[k - m]
    logpmf = binom.logpmf(m, k, gamma)
    return np.exp(logsumexp(logpmf + logP))


def s_of_k(k, n, gamma):
    beta = gamma * (2 - gamma) / 2
    return beta * k * k / n - gamma * k / (2 * n)


def Q_heuristic(k, n, gamma):
    term1 = k * gamma * (1 - gamma) / (2 * n)
    term2 = -k ** 3 * (1 - (1 - gamma) ** 3) / (6 * n ** 2)
    term3 = k ** 3 * gamma * (1 - gamma) ** 3 / (2 * n ** 2)
    return term1 + term2 + term3


print(f"{'n':>9} {'gamma':>6} {'t (k=t*sqrt(n/beta))':>10} {'k':>8} "
      f"{'A_k/e^-s(k) - 1':>18} {'Q(k;n,gamma)':>16} {'abs diff':>12} {'rel diff':>10}")

for n in [4096, 65536, 1048576]:
    for gamma in [0.3, 0.7]:
        beta = gamma * (2 - gamma) / 2
        cumlog = build_cumlog(n)
        for t in [0.5, 1.0, 2.0]:
            k = max(1, int(round(t * np.sqrt(n / beta))))
            if k > n:
                continue
            Ak = A_k_exact(k, n, gamma, cumlog)
            sk = s_of_k(k, n, gamma)
            lhs = Ak / np.exp(-sk) - 1
            rhs = Q_heuristic(k, n, gamma)
            print(f"{n:9d} {gamma:6.2f} {t:10.2f} {k:8d} {lhs:18.8e} {rhs:16.8e} "
                  f"{abs(lhs - rhs):12.3e} {abs(lhs - rhs) / max(abs(lhs), 1e-30):10.3e}")
    print()
