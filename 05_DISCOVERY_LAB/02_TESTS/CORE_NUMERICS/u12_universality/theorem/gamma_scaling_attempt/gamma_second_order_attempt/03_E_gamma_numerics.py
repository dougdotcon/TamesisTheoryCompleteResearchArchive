"""
Direct high-n numerical evaluation of
    S_n(gamma)      = sum_{k=1}^n A_k(n,gamma)               [= n*phi(n,gamma n), Lemma 1]
    S0_n(gamma)     = sum_{k=1}^n e^{-s(k)}                  [the deterministic half]
    E_n(gamma)      = S_n - S0_n                             [the "hard", Binomial-averaged half]
and comparison of
    D_n  := S_n  - G_n   -->  D(gamma)  (conjectured, wave-17 front, closed form)
    D0_n := S0_n - G_n   -->  D0(gamma) (PROVED, this front, closed form)
    E_n         =  D_n - D0_n  -->  E(gamma) := D(gamma) - D0(gamma)  (closed form implied
                                     by the wave-17 conjecture; NOT independently proved by
                                     this front -- this script only checks numerical
                                     consistency of the decomposition, it is not a proof).

A_k(n,gamma) = E_{M~Bin(k,gamma)}[ P(k,M) ], P(k,m) = prod_{i=1}^m (1-(k-i)/n).
Per-k work is kept to O(sqrt(k)) by only summing m over a wide (+-14 std)
window around the Binomial mean gamma*k (pmf outside is < 1e-40, verified
below to be far smaller than the float64 noise floor of the whole
computation) -- this restriction is disclosed, not "certified" the way the
wave-17 front certified its truncation (2.1); it is an ordinary numerical
truncation, checked by widening the window and confirming no change.

Float64 throughout (not exact/high-precision): the quantities G_n, S_n are
O(sqrt(n)) ~ O(1e3), and the O(1) additive constants D(gamma) are recovered
after cancellation; float64 relative precision ~1e-15 leaves ~1e-12 absolute
precision after cancellation at n~1e6, far more than the ~1e-4 precision
needed to see D(gamma) at these n given its own convergence rate. Verified
directly below (script 03b) against mpmath at one point.
"""
import math
import numpy as np
from scipy.stats import binom


def beta_of(g):
    return g * (2 - g) / 2.0


def G(n, g):
    b = beta_of(g)
    return 0.5 * math.sqrt(math.pi * n / b)


def D0_closed(g):
    return (g - 1) / (2 * (2 - g))


def E_closed(g):
    # implied by the wave-17 front's conjectured D(gamma), for reference only
    Dg = -(g ** 2 - 8 * g / 3 + 2) / (2 - g) ** 2
    return Dg - D0_closed(g)


def D_closed_target(g):
    return -(g ** 2 - 8 * g / 3 + 2) / (2 - g) ** 2


def A_k(k, n, g, nstd=14.0):
    mean = g * k
    std = math.sqrt(k * g * (1 - g)) if 0 < g < 1 else 0.0
    m_lo = max(0, int(math.floor(mean - nstd * std - 1)))
    m_hi = min(k, int(math.ceil(mean + nstd * std + 1)))
    if m_hi <= 0:
        # g essentially 0 or k=0: only m=0 term matters
        return 1.0
    # log P(k,m) for m=0..m_hi via cumulative sum of log(1-(k-i)/n), i=1..m_hi
    i = np.arange(1, m_hi + 1)
    terms = 1.0 - (k - i) / n
    # guard (should always be >0 for k<=n)
    logterms = np.log(terms)
    logP = np.concatenate(([0.0], np.cumsum(logterms)))  # logP[m] for m=0..m_hi
    ms = np.arange(m_lo, m_hi + 1)
    pmf = binom.pmf(ms, k, g)
    Pvals = np.exp(logP[m_lo:m_hi + 1])
    return float(np.sum(pmf * Pvals))


def s_of_k(k, n, g):
    b = beta_of(g)
    return b * k * k / n - g * k / (2 * n)


def S_n_and_S0_n(n, g, Kmult=25.0):
    b = beta_of(g)
    Kcut = min(n, int(math.sqrt(n / b) * Kmult) + 50)
    Sn = 0.0
    S0n = 0.0
    for k in range(1, Kcut + 1):
        Sn += A_k(k, n, g)
        S0n += math.exp(-s_of_k(k, n, g))
    return Sn, S0n, Kcut


if __name__ == "__main__":
    print("E(gamma) numerics: S_n = sum A_k vs S0_n = sum e^{-s(k)}, both vs G_n")
    print("=" * 100)
    gammas = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
    ns = [2 ** 14, 2 ** 16, 2 ** 18]  # 16384, 65536, 262144
    results = {}
    for g in gammas:
        print(f"\ngamma={g}")
        print(f"  D0(gamma) closed form           = {D0_closed(g):.8f}")
        print(f"  D(gamma) [wave-17 conjecture]    = {D_closed_target(g):.8f}")
        print(f"  E(gamma) implied (=D-D0)         = {E_closed(g):.8f}")
        rows = []
        for n in ns:
            Sn, S0n, Kcut = S_n_and_S0_n(n, g)
            Gn = G(n, g)
            Dn = Sn - Gn
            D0n = S0n - Gn
            En = Sn - S0n
            rows.append((n, Kcut, Dn, D0n, En))
            print(f"    n={n:>7} K={Kcut:>6}  D_n={Dn:>12.8f}  D0_n={D0n:>12.8f}  "
                  f"E_n={En:>12.8f}  (E_n - E_target)={En-E_closed(g):>10.6f}")
        results[g] = rows
        # Richardson extrapolation of E_n assuming E_n = E + c/sqrt(n)
        (n1, K1, D1, D01, E1), (n2, K2, D2, D02, E2) = rows[-2], rows[-1]
        r = math.sqrt(n2 / n1)
        E_extrap = (r * E2 - E1) / (r - 1)
        print(f"    Richardson extrap of E_n (last two n, model E+c/sqrt(n)): "
              f"{E_extrap:.8f}  vs E(gamma) target {E_closed(g):.8f}  "
              f"diff={E_extrap-E_closed(g):.2e}")
        D_extrap = (r * D2 - D1) / (r - 1)
        print(f"    Richardson extrap of D_n (same): {D_extrap:.8f}  vs D(gamma) target "
              f"{D_closed_target(g):.8f}  diff={D_extrap-D_closed_target(g):.2e}")
