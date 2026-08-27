"""
REFEREE script 05 -- FINAL, refined independent reconstruction of the
n0(gamma) assembly (both Hoeffding/OLD and Bernstein/NEW), incorporating
the lesson learned in ref04b/ref04c: the small-k residual term is bounded
using coefficients evaluated at the RUNNING k (c_i(k2)), not the global
truncation bound K_max -- the natural, tighter choice for a deterministic
per-k bound, since there is no structural reason (unlike in the Bulk/Tail
Lemma's k-uniformity argument) to inflate small-k coefficients to their
K_max value.

This supersedes ref04's small-k piece; the bulk+tail piece (which matched
the target's own disclosed intermediate values to <0.005 in the natural
log, independent of the small-k question) is unchanged from ref04.

Spot-checked at 4 of the 8 sample gamma values: 0.5 (the disclosed small
loss case), 0.1, 0.01 (the largest claimed gain, ~9 decades), and 0.99
(the case where the target itself disclosed the small-k term as
non-negligible -- the hardest calibration test).
"""
import mpmath as mp

mp.mp.dps = 60


def beta_of(gamma):
    return gamma * (2 - gamma) / 2


def sigma2_of(gamma):
    return gamma * (1 - gamma)


def K_max_of(n, gamma):
    beta = beta_of(gamma)
    return 4 * mp.sqrt(n * mp.log(n) / beta)


def coeff_bounds(k, n, gamma):
    c0 = mp.mpf(7) / 6 * k ** 3 / n ** 2 + mp.mpf(5) / 6 * k ** 2 / n ** 2
    c1 = 2 * k ** 2 / n ** 2 + (1 - gamma) * k / n + k / n ** 2 + mp.mpf(3) / 4 / n
    c2 = (1 - gamma) * k / (2 * n ** 2) + mp.mpf(3) / 4 / n
    c3 = mp.mpf(1) / (6 * n ** 2)
    return c0, c1, c2, c3


def g_bound(t, k_for_coeffs, n, gamma):
    c0, c1, c2, c3 = coeff_bounds(k_for_coeffs, n, gamma)
    return c0 + c1 * t + c2 * t ** 2 + c3 * t ** 3


def Ghat_of(n, gamma):
    K = K_max_of(n, gamma)
    return g_bound(K, K, n, gamma)


def Ghat_Theta_of(n, gamma, C):
    K = K_max_of(n, gamma)
    Theta_K = C * mp.sqrt(K * mp.log(n))
    return g_bound(Theta_K, K, n, gamma)


def Gn_bound_of(n, gamma):
    beta = beta_of(gamma)
    return mp.sqrt(mp.pi * n / beta)


def lambda_hat_of(gamma):
    beta = beta_of(gamma)
    return 16 * (mp.mpf('1.75') - gamma) / beta


def C0_hoeffding_of(gamma):
    return mp.sqrt(mp.mpf('0.25') + lambda_hat_of(gamma) / 2)


def C0_bernstein_of(gamma, a):
    sigma2 = sigma2_of(gamma)
    lam_hat = lambda_hat_of(gamma)
    return mp.sqrt((2 + a) * sigma2 * (lam_hat + mp.mpf('0.5')))


def logW_hoeffding(logn, gamma, C):
    n = mp.power(10, logn)
    Gn = Gn_bound_of(n, gamma)
    Gh = Ghat_of(n, gamma)
    GhT = Ghat_Theta_of(n, gamma, C)
    tail_factor = 2 * mp.power(n, -2 * C * C)
    bulk_term = mp.power(GhT, 3) * mp.exp(GhT)
    tail_term = tail_factor * mp.power(Gh, 3) * mp.exp(Gh)
    W = Gn * (bulk_term + tail_term) / 6
    return mp.log(W)


def logW_bernstein_refined(logn, gamma, C, a):
    """Bulk+tail piece as before; small-k residual now uses running-k
    coefficients c_i(k2) (the refined, better-motivated choice)."""
    n = mp.power(10, logn)
    Gn = Gn_bound_of(n, gamma)
    Gh = Ghat_of(n, gamma)
    GhT = Ghat_Theta_of(n, gamma, C)
    sigma2 = sigma2_of(gamma)
    tail_exponent = -(C * C) / ((2 + a) * sigma2)
    tail_factor = 2 * mp.power(n, tail_exponent)
    bulk_term = mp.power(GhT, 3) * mp.exp(GhT)
    tail_term = tail_factor * mp.power(Gh, 3) * mp.exp(Gh)
    bulk_tail_log = mp.log(Gn) + mp.log(bulk_term + tail_term) - mp.log(6)

    M = max(gamma, 1 - gamma)
    k2 = (2 * M * C / (3 * a * sigma2)) ** 2 * mp.log(n)
    if k2 < 1:
        k2 = mp.mpf(1)
    gk2 = g_bound(k2, k2, n, gamma)  # running-k coefficients (refined)
    smallk_log = mp.log(k2) + mp.mpf('0.5') - mp.log(6) + 3 * mp.log(gk2) + gk2

    hi = max(bulk_tail_log, smallk_log)
    lo = min(bulk_tail_log, smallk_log)
    return hi + mp.log1p(mp.exp(lo - hi))


def bisect(fn, gamma, C, extra, lo=1, hi=250, tol=1e-3, max_iter=200):
    flo = fn(mp.mpf(lo), gamma, C, *extra) if extra else fn(mp.mpf(lo), gamma, C)
    fhi = fn(mp.mpf(hi), gamma, C, *extra) if extra else fn(mp.mpf(hi), gamma, C)
    if not (flo > 0 and fhi < 0):
        return None, flo, fhi
    a_, b_ = mp.mpf(lo), mp.mpf(hi)
    for _ in range(max_iter):
        mid = (a_ + b_) / 2
        fm = fn(mid, gamma, C, *extra) if extra else fn(mid, gamma, C)
        if fm > 0:
            a_ = mid
        else:
            b_ = mid
        if b_ - a_ < tol:
            break
    return (a_ + b_) / 2, flo, fhi


PUBLISHED_OLD_TABLE = {
    '0.99': mp.mpf('20.79'), '0.9': mp.mpf('36.83'), '0.7': mp.mpf('45.02'),
    '0.5': mp.mpf('50.28'), '0.3': mp.mpf('55.95'), '0.1': mp.mpf('65.95'),
    '0.05': mp.mpf('71.78'), '0.01': mp.mpf('84.88'),
}
TARGET_CLAIMED_NEW_TABLE = {
    '0.99': mp.mpf('17.72'), '0.9': mp.mpf('33.64'), '0.7': mp.mpf('44.57'),
    '0.5': mp.mpf('50.35'), '0.3': mp.mpf('55.51'), '0.1': mp.mpf('63.06'),
    '0.05': mp.mpf('67.08'), '0.01': mp.mpf('75.79'),
}
TARGET_CLAIMED_SAVED = {
    '0.99': mp.mpf('3.07'), '0.9': mp.mpf('3.19'), '0.7': mp.mpf('0.46'),
    '0.5': mp.mpf('-0.07'), '0.3': mp.mpf('0.44'), '0.1': mp.mpf('2.89'),
    '0.05': mp.mpf('4.70'), '0.01': mp.mpf('9.09'),
}

print(f"{'gamma':>6} {'own OLD':>9} {'pub OLD':>9} {'own NEW':>9} {'claim NEW':>10} "
      f"{'own saved':>10} {'claim saved':>12} {'match?':>8}")
rows = []
for gstr in ['0.99', '0.9', '0.7', '0.5', '0.3', '0.1', '0.05', '0.01']:
    gamma = mp.mpf(gstr)
    a_slack = mp.mpf('0.05')

    C0h = C0_hoeffding_of(gamma)
    C_hoeff = mp.mpf('1.2') * C0h
    n0_old, flo, fhi = bisect(logW_hoeffding, gamma, C_hoeff, None)

    C0b = C0_bernstein_of(gamma, a_slack)
    C_bern = mp.mpf('1.2') * C0b
    n0_new, flo2, fhi2 = bisect(logW_bernstein_refined, gamma, C_bern, (a_slack,))

    if n0_old is None or n0_new is None:
        print(f"{gstr:>6}  BISECTION FAILED")
        continue

    saved = n0_old - n0_new
    pub_old = PUBLISHED_OLD_TABLE[gstr]
    claim_new = TARGET_CLAIMED_NEW_TABLE[gstr]
    claim_saved = TARGET_CLAIMED_SAVED[gstr]
    match = abs(saved - claim_saved) < mp.mpf('0.3')  # generous match tolerance
    rows.append((gstr, n0_old, pub_old, n0_new, claim_new, saved, claim_saved, match))
    print(f"{gstr:>6} {float(n0_old):>9.3f} {float(pub_old):>9.3f} {float(n0_new):>9.3f} "
          f"{float(claim_new):>10.3f} {float(saved):>10.3f} {float(claim_saved):>12.3f} "
          f"{'YES' if match else 'NO':>8}")

print()
n_match = sum(1 for r in rows if r[-1])
print(f"Points where referee's own reconstruction confirms claimed decades-saved to <0.3: "
      f"{n_match}/{len(rows)}")
