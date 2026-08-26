# Direct, high-precision (mpmath dps=50) evaluation of the EXACT quantities
# Gap 1 is about, via the exact Binomial pmf -- no Hoeffding, no order
# counting, no Taylor-remainder shortcut anywhere in this script. This is
# the "ground truth" this front's analytic bulk/tail argument (see
# 03_bulk_tail_split_check.py and ATTEMPT.md Section 3) is checked against.
#
# For each (n, gamma, k):
#   x(D) = c0 + c1*D + c2*D^2 + c3*D^3   (exact cubic, script 01)
#   R_exact(k)  := | E_M[e^{-x(D)}] - (1 - E[x] + E[x^2]/2) |         (*)
#   R_bound(k)  := (1/6) * E_M[ |x(D)|^3 * e^{|x(D)|} ]               (**)
# (**) is Gap 1's own literal target quantity (the RHS of the elementary
# Taylor-remainder inequality |e^{-x}-(1-x+x^2/2)| <= (|x|^3/6) e^{|x|}
# quoted in the predecessor ATTEMPT.md Section 5, Gap 1). By that elementary,
# always-true pointwise inequality plus linearity of expectation + triangle
# inequality, R_exact(k) <= R_bound(k) always -- checked below as a pure
# implementation sanity check, not a claim requiring proof.
#
# Gap 1 asks for a bound Sigma_k e^{-s(k)} R_bound(k) = o(1) as n -> oo,
# uniform for k <= K ~ sqrt(n ln n). This script computes
#   W_exact(n,gamma) := Sigma_{k=1}^{K} e^{-s(k)} R_exact(k)   (the TRUE quantity)
#   W_bound(n,gamma) := Sigma_{k=1}^{K} e^{-s(k)} R_bound(k)   (Gap 1's literal target)
# directly, with NO approximation beyond (i) an adaptively-widened but
# disclosed truncation of the m-summation window around the Binomial mean
# (standard in this lineage; widened until missed tail mass is below the
# mpmath dps=50 floor) and (ii) truncating the k-sum at K itself (the tail
# k>K piece is already handled elsewhere in the lineage, per Estagio 26/the
# wave-17 front's own rho(K) bound -- not re-derived or re-claimed here).
#
# No .py file of any prior front was opened, read, or imported. Seeds: none
# used -- everything here is deterministic (exact pmf + mpmath), per this
# front's reserved block 20260890000-20260890999 (disclosed unused, as the
# object under study needs no randomization).

import mpmath as mp
import math, time, sys

mp.mp.dps = 50


def make_coeffs(k, n, gamma):
    k = mp.mpf(k); n = mp.mpf(n); g = mp.mpf(gamma)
    c3 = mp.mpf(1) / (6 * n ** 2)
    c2 = (2 * g * k - 2 * k - 2 * n + 1) / (4 * n ** 2)
    c1 = (g ** 2 * k ** 2 / 2 - g * k ** 2 - g * k * n + g * k / 2 + k ** 2 / 2
          + k * n - k / 2 - n / 2 + mp.mpf(1) / 12) / n ** 2
    m0 = g * k
    tau_m0 = (m0 ** 3 / 3 + m0 ** 2 * (mp.mpf(1) / 2 - k) + m0 * (k ** 2 - k + mp.mpf(1) / 6)) / n ** 2
    c0 = tau_m0 / 2
    return c0, c1, c2, c3


def x_of_D(D, c0, c1, c2, c3):
    return c0 + c1 * D + c2 * D ** 2 + c3 * D ** 3


def s_of_k(k, n, gamma):
    k = mp.mpf(k); n = mp.mpf(n); g = mp.mpf(gamma)
    beta = g * (2 - g) / 2
    return beta * k ** 2 / n - g * k / (2 * n)


def binom_logpmf(m, k, gamma):
    m = mp.mpf(m); k = mp.mpf(k); g = mp.mpf(gamma)
    lg = mp.loggamma(k + 1) - mp.loggamma(m + 1) - mp.loggamma(k - m + 1)
    return lg + m * mp.log(g) + (k - m) * mp.log(1 - g)


def k_expectations(k, n, gamma, window_logtol=mp.mpf(-140)):
    """Exact (Binomial pmf, mpmath dps=50) expectations at fixed k, via an
    adaptively-widened truncation window around the Binomial mean, widened
    until the missed tail's log-pmf (relative to the peak) is below
    window_logtol -- i.e. missed probability mass is far below the dps=50
    rounding floor, not a source of claimed precision loss."""
    k_i = int(k)
    g = mp.mpf(gamma)
    if k_i == 0:
        c0, c1, c2, c3 = make_coeffs(0, n, gamma)
        x0 = x_of_D(mp.mpf(0), c0, c1, c2, c3)
        return mp.mpf(1), x0, x0 ** 2, mp.e ** (-x0), abs(x0) ** 3 * mp.e ** abs(x0)
    mean = g * k_i
    if gamma <= 0 or gamma >= 1:
        m_lo = m_hi = int(round(float(mean)))
    else:
        sigma = mp.sqrt(k_i * g * (1 - g))
        W = mp.mpf(8)
        m_lo, m_hi = 0, k_i
        while True:
            m_lo = max(0, int(mp.floor(mean - W * sigma)))
            m_hi = min(k_i, int(mp.ceil(mean + W * sigma)))
            peak = binom_logpmf(int(round(float(mean))), k_i, gamma)
            edge_lo = binom_logpmf(m_lo, k_i, gamma) - peak
            edge_hi = binom_logpmf(m_hi, k_i, gamma) - peak
            if (m_lo == 0 or edge_lo < window_logtol) and (m_hi == k_i or edge_hi < window_logtol):
                break
            W *= mp.mpf(1.5)
            if W > 300:
                break
    c0, c1, c2, c3 = make_coeffs(k_i, n, gamma)
    Z = mp.mpf(0); E_x = mp.mpf(0); E_x2 = mp.mpf(0); E_negexp = mp.mpf(0); E_bound = mp.mpf(0)
    for m in range(m_lo, m_hi + 1):
        lp = binom_logpmf(m, k_i, gamma)
        p = mp.e ** lp
        D = mp.mpf(m) - mean
        x = x_of_D(D, c0, c1, c2, c3)
        Z += p
        E_x += p * x
        E_x2 += p * x ** 2
        E_negexp += p * mp.e ** (-x)
        E_bound += p * abs(x) ** 3 * mp.e ** abs(x)
    return Z, E_x, E_x2, E_negexp, E_bound


def weighted_sums(n, gamma, K_mult=mp.mpf('1.5')):
    K = int(math.ceil(float(K_mult) * math.sqrt(n * math.log(n))))
    W_exact = mp.mpf(0); W_bound = mp.mpf(0)
    max_R_exact_over_bound = mp.mpf(0)
    min_Z = mp.mpf(1)
    for k in range(1, K + 1):
        Z, E_x, E_x2, E_negexp, E_bound = k_expectations(k, n, gamma)
        min_Z = min(min_Z, Z)
        Taylor2 = 1 - E_x + E_x2 / 2
        R_exact = abs(E_negexp - Taylor2)
        R_bound = E_bound / 6
        w = mp.e ** (-s_of_k(k, n, gamma))
        W_exact += w * R_exact
        W_bound += w * R_bound
        if R_bound > 0:
            max_R_exact_over_bound = max(max_R_exact_over_bound, R_exact / R_bound)
    return K, W_exact, W_bound, max_R_exact_over_bound, min_Z


if __name__ == "__main__":
    print("=" * 92)
    print("Part 1: pointwise sanity -- R_exact(k) <= R_bound(k) always (Lagrange remainder,")
    print("elementary calculus; a bug check, not a claim requiring its own proof).")
    print("=" * 92)
    all_ok = True
    for (k, n, gamma) in [(1, 50, mp.mpf('0.5')), (5, 100, mp.mpf('0.5')),
                           (50, 1000, mp.mpf('0.5')), (200, 10000, mp.mpf('0.3')),
                           (10, 500, mp.mpf('0.9')), (3, 200, mp.mpf('0.99'))]:
        Z, E_x, E_x2, E_negexp, E_bound = k_expectations(k, n, gamma)
        R_exact = abs(E_negexp - (1 - E_x + E_x2 / 2))
        R_bound = E_bound / 6
        ok = R_exact <= R_bound
        all_ok &= ok
        print(f"k={k:5d} n={n:6d} gamma={mp.nstr(gamma,3)}: Z={mp.nstr(Z,8)} "
              f"R_exact={mp.nstr(R_exact,6)} R_bound={mp.nstr(R_bound,6)} "
              f"R_exact<=R_bound: {ok}")
    print("ALL POINTWISE CHECKS PASS:", all_ok)
    assert all_ok

    print()
    print("=" * 92)
    print("Part 2: W_exact(n,gamma) and W_bound(n,gamma) := Sigma_k e^{-s(k)} R_*(k),")
    print("k<=K~1.5*sqrt(n ln n), as n grows -- Gap 1 needs W_bound -> 0.")
    print("=" * 92)
    ns = [500, 2000, 8000, 32000]
    gammas = [mp.mpf(x) for x in ['0.1', '0.3', '0.5', '0.7', '0.9', '0.99']]
    results = {}
    t_start = time.time()
    for gamma in gammas:
        row = []
        for n in ns:
            t0 = time.time()
            K, W_exact, W_bound, max_ratio, min_Z = weighted_sums(n, gamma)
            dt = time.time() - t0
            row.append((n, K, W_exact, W_bound, max_ratio, min_Z))
            print(f"gamma={mp.nstr(gamma,3)} n={n:6d} K={K:5d} "
                  f"W_exact={mp.nstr(W_exact,8)} W_bound={mp.nstr(W_bound,8)} "
                  f"max(R_exact/R_bound)={mp.nstr(max_ratio,4)} min_Z={mp.nstr(min_Z,6)} "
                  f"[{dt:.1f}s]", flush=True)
        results[gamma] = row
    print(f"\nTotal Part 2 wall time: {time.time()-t_start:.1f}s")

    print()
    print("=" * 92)
    print("Part 3: empirical decay-rate fit of W_bound(n,gamma) under n -> 4n")
    print("(log-ratio / log(4); e.g. -0.25 matches this front's analytic")
    print("n^{-1/4}*polylog(n) prediction; -0.5 would match the same rate as")
    print("Lemma D0's / Lemma G2's own O(n^{-1/2}) error terms elsewhere in")
    print("this lineage -- either would suffice for Sigma_k e^{-s(k)}R_bound(k)=o(1))")
    print("=" * 92)
    for gamma in gammas:
        row = results[gamma]
        print(f"\ngamma={mp.nstr(gamma,3)}:")
        for i in range(len(row) - 1):
            n0, K0, We0, Wb0, mr0, z0 = row[i]
            n1, K1, We1, Wb1, mr1, z1 = row[i + 1]
            ratio_bound = Wb1 / Wb0
            ratio_exact = We1 / We0
            logratio_n = math.log(n1 / n0)
            rate_bound = float(mp.log(ratio_bound)) / logratio_n
            rate_exact = float(mp.log(ratio_exact)) / logratio_n if We0 != 0 else float('nan')
            print(f"  n {n0}->{n1}: W_bound ratio={mp.nstr(ratio_bound,5)} "
                  f"(fit rate {rate_bound:+.4f}) | "
                  f"W_exact ratio={mp.nstr(ratio_exact,5)} (fit rate {rate_exact:+.4f})")

    print("\nDone.")
