"""
Shared closed-form implementations, re-typed independently from the target
document's stated formulas (Proposicao 2.1, Corolario A1 as cited, Theorem 1,
Theorem 3, Lemma 4.1, Lemma 4.2), used by check02..check06.

These are the FORMULAS ATTEMPT.md claims -- implementing them independently
lets us stress-test the claimed IDENTITIES/INEQUALITIES themselves at scale.
(Their correctness as a re-derivation from primary sources is separately
confirmed in check01.py, which re-derives them from Theorem A/B/Reduction
Lemma A read directly from the primary sources, not from here.)

Exact arithmetic: fractions.Fraction.
High precision: mpmath, via log-gamma so K, n can be very large without ever
forming huge integer factorials.
"""
from fractions import Fraction as F
from math import comb, factorial

import mpmath as mp


# ---------------------------------------------------------------------------
# Exact (Fraction) versions
# ---------------------------------------------------------------------------

def phi_K(K):
    """phi_K = 4^K (K!)^2 / (2K+1)!  (Wallis integral mean, cited)."""
    return F(4**K * factorial(K)**2, factorial(2 * K + 1))


def g_of_i(i, n):
    """g(i;n) = prod_{l=1}^i (1+l/n) = (n+i)!/(n! n^i)."""
    prod = F(1)
    for l in range(1, i + 1):
        prod *= F(n + l, n)
    return prod


def psi_K_closed(K, n):
    """Corolario A1: psi_n^{(K)} = (phi_K/4^K) sum_{j=0}^K C(2K+1,K-j) g(j;n)."""
    pref = phi_K(K) / F(4)**K
    total = F(0)
    for j in range(0, K + 1):
        total += comb(2 * K + 1, K - j) * g_of_i(j, n)
    return pref * total


def psiR_K_closed(K, n):
    """Proposicao 2.1: psi_n^{(K),R} = kappa * sum_{i=1}^K C(2K,K-i) g(i;n),
    kappa = (K-1)!K!/(2K)!.  K>=1."""
    assert K >= 1
    kappa = F(factorial(K - 1) * factorial(K), factorial(2 * K))
    total = F(0)
    for i in range(1, K + 1):
        total += comb(2 * K, K - i) * g_of_i(i, n)
    return kappa * total


def phi_n_K_closed(K, n):
    """phi_n^{(K)} via (2.1), K < n. For K=0 -> 1 identically."""
    if K == 0:
        return F(1)
    assert n > K
    psR = psiR_K_closed(K, n)
    ps = psi_K_closed(K, n)
    return F(K, n) * psR + (1 - F(K, n)) * ps


def T_of_nK(K, n):
    """T(n,K) := n(phi_n^{(K)} - phi_K), K>=0, n>=K+1 (K=0 -> T=0 always)."""
    return n * (phi_n_K_closed(K, n) - phi_K(K))


def Q_exact(n):
    """Ramanujan Q(n) = sum_{j=0}^{n-1} prod_{i=1}^j (1-i/n), exact Fraction.
    O(n) work."""
    total = F(1)  # j=0 term
    term = F(1)
    for j in range(1, n):
        term *= F(n - j, n)
        total += term
    return total


def M_K_theorem3(K):
    """Theorem 3: M_K = Q(K+1) - (K+1) phi_K, computed via the exact Q()."""
    return Q_exact(K + 1) - (K + 1) * phi_K(K)


# ---------------------------------------------------------------------------
# High-precision (mpmath) versions, for large K/n via log-gamma (O(1) per
# call for phi_K; O(K) per call for the closed forms' finite sums, which is
# unavoidable since they are genuinely K-term sums; O(n) for Q).
# ---------------------------------------------------------------------------

def phi_K_mp(K):
    """phi_K via log-gamma, exact-in-spirit at whatever mp.mp.dps is set."""
    K = mp.mpf(K)
    lg = K * mp.log(4) + 2 * mp.loggamma(K + 1) - mp.loggamma(2 * K + 2)
    return mp.e**lg


def g_of_i_mp(i, n):
    prod = mp.mpf(1)
    n = mp.mpf(n)
    for l in range(1, i + 1):
        prod *= (1 + mp.mpf(l) / n)
    return prod


def logbinom(n, k):
    return mp.loggamma(n + 1) - mp.loggamma(k + 1) - mp.loggamma(n - k + 1)


def psi_K_closed_mp(K, n):
    pref = phi_K_mp(K) / mp.mpf(4)**K
    total = mp.mpf(0)
    for j in range(0, K + 1):
        cb = mp.e**logbinom(2 * K + 1, K - j)
        total += cb * g_of_i_mp(j, n)
    return pref * total


def psiR_K_closed_mp(K, n):
    assert K >= 1
    kappa = mp.e**(mp.loggamma(K) + mp.loggamma(K + 1) - mp.loggamma(2 * K + 1))
    total = mp.mpf(0)
    for i in range(1, K + 1):
        cb = mp.e**logbinom(2 * K, K - i)
        total += cb * g_of_i_mp(i, n)
    return kappa * total


def phi_n_K_closed_mp(K, n):
    if K == 0:
        return mp.mpf(1)
    assert n > K
    psR = psiR_K_closed_mp(K, n)
    ps = psi_K_closed_mp(K, n)
    Kn = mp.mpf(K) / mp.mpf(n)
    return Kn * psR + (1 - Kn) * ps


def T_of_nK_mp(K, n):
    return mp.mpf(n) * (phi_n_K_closed_mp(K, n) - phi_K_mp(K))


def Q_mp(n):
    """Ramanujan Q(n) via mpmath, O(n) work, safe for n up to ~1e5-1e6
    within a script's patience; see numpy-based Q_np for very large n."""
    total = mp.mpf(1)
    term = mp.mpf(1)
    n_mp = mp.mpf(n)
    for j in range(1, n):
        term *= (n_mp - j) / n_mp
        total += term
    return total


def M_K_theorem3_mp(K):
    return Q_mp(K + 1) - (K + 1) * phi_K_mp(K)
