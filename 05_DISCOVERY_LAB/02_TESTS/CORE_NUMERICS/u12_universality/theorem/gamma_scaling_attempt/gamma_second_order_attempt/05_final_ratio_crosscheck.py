"""
Final consolidated cross-check: compute R_n = phi(n,gamma n)/phi_inf(gamma n)
directly from this front's own fresh S_n = sum_k A_k implementation, and
sqrt(n)*(R_n - target), at n=262144 for a few gamma, to compare against
the wave-17 front's own printed table (ATTEMPT.md Sec 7.1) as one more
independent confirmation using a totally independent codepath (this
front never opened that front's .py scripts).
"""
import math
from math import erf
from scipy.stats import binom
import numpy as np


def beta_of(g):
    return g * (2 - g) / 2.0


def s_of_k(k, n, g):
    b = beta_of(g)
    return b * k * k / n - g * k / (2 * n)


def A_k(k, n, g, nstd=14.0):
    mean = g * k
    std = math.sqrt(k * g * (1 - g)) if 0 < g < 1 else 0.0
    m_lo = max(0, int(math.floor(mean - nstd * std - 1)))
    m_hi = min(k, int(math.ceil(mean + nstd * std + 1)))
    if m_hi <= 0:
        return 1.0
    i = np.arange(1, m_hi + 1)
    terms = 1.0 - (k - i) / n
    logterms = np.log(terms)
    logP = np.concatenate(([0.0], np.cumsum(logterms)))
    ms = np.arange(m_lo, m_hi + 1)
    pmf = binom.pmf(ms, k, g)
    Pvals = np.exp(logP[m_lo:m_hi + 1])
    return float(np.sum(pmf * Pvals))


def S_n(n, g, Kmult=25.0):
    b = beta_of(g)
    Kcut = min(n, int(math.sqrt(n / b) * Kmult) + 50)
    return sum(A_k(k, n, g) for k in range(1, Kcut + 1))


def phi_inf(c):
    # phi_inf(c) = (sqrt(pi)/2) c^{-1/2} erf(sqrt(c))
    return (math.sqrt(math.pi) / 2) * c ** -0.5 * erf(math.sqrt(c))


def target(g):
    return math.sqrt(2 / (2 - g))


def C_closed(g):
    return -(2 / (3 * math.sqrt(math.pi))) * math.sqrt(g) * (6 - 8 * g + 3 * g ** 2) / (2 - g) ** 2


if __name__ == "__main__":
    n = 262144
    print(f"n={n}")
    print(f"{'gamma':>6} {'target':>14} {'R_n (this front)':>18} {'R_n-target':>12} "
          f"{'sqrt(n)*(R_n-target)':>20} {'C(gamma) closed form':>20}")
    for g in (0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 1.0):
        Sn = S_n(n, g)
        Rn = (Sn / n) / phi_inf(g * n)
        t = target(g)
        val = math.sqrt(n) * (Rn - t)
        print(f"{g:>6.2f} {t:>14.9f} {Rn:>18.10f} {Rn-t:>12.3e} {val:>20.6f} {C_closed(g):>20.6f}")
