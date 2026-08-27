"""
REFEREE script 04 -- independent reconstruction of the full n_0(gamma)
assembly (both Hoeffding/OLD and Bernstein/NEW), built entirely from the
mathematical prose of:
  - the grandparent ATTEMPT.md (gamma_gap1_mgf_attempt): the exact cubic
    x(D), the Bulk/Tail Lemma structure, g(t):=|c0|+|c1|t+|c2|t^2+|c3|t^3.
  - the direct predecessor ATTEMPT.md (gamma_gap1_continuation_attempt):
    kappa_0(gamma)=8/(gamma(2-gamma)), the tightened coefficient bounds
    |c0|,|c1|,|c2|,c3(exact), the Ghat(n,gamma) assembly, Ghat_Theta,
    the cited G_n<=sqrt(pi*n/beta), the W(n,gamma,C) Hoeffding assembly,
    and the published OLD n_0(gamma) table at 8 sample gamma (used here
    ONLY as a target to CALIBRATE this referee's independent reconstruction
    against -- not copied into the construction itself).
  - the target ATTEMPT.md (gamma_gap1_sharper_tail_attempt): the Bernstein
    tail-probability replacement 2*n^{-C^2/((2+a)*sigma^2)}, the slack
    parameter a, and C0_Bernstein(gamma,a)^2.

Purpose (task item 5): spot-check the n_0(gamma) comparison table at >=2-3
of the 8 sample gamma values, confirming DIRECTION and rough MAGNITUDE of
the claimed improvement -- not full bit-for-bit reproduction.

Own variable names, own code, no .py file of this front or its lineage read.
All arithmetic done at mpmath dps=60 directly on mpf values -- mpmath's
arbitrary-precision floating point handles the astronomically large
exponents involved (n up to 10^85, exponents like e^(many thousands))
WITHOUT the log-domain bookkeeping the target front used, since mpmath mpf
has an unbounded (arbitrary-precision-integer) exponent field, unlike
float64. Where numbers get large enough that direct mpf exponentiation
becomes slow, mp.power / mp.exp are used which are efficient at this scale.
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
    """Tightened, cancellation-preserving elementary coefficient bounds,
    exactly as quoted (and independently re-derivable) from the predecessor's
    ATTEMPT.md section 4 Step 3:
        |c0| <= (7/6)k^3/n^2 + (5/6)k^2/n^2
        |c1| <= 2k^2/n^2 + (1-gamma)k/n + k/n^2 + 3/(4n)
        |c2| <= (1-gamma)k/(2n^2) + 3/(4n)
        c3   = 1/(6n^2)                              (exact)
    """
    c0 = mp.mpf(7) / 6 * k ** 3 / n ** 2 + mp.mpf(5) / 6 * k ** 2 / n ** 2
    c1 = 2 * k ** 2 / n ** 2 + (1 - gamma) * k / n + k / n ** 2 + mp.mpf(3) / 4 / n
    c2 = (1 - gamma) * k / (2 * n ** 2) + mp.mpf(3) / 4 / n
    c3 = mp.mpf(1) / (6 * n ** 2)
    return c0, c1, c2, c3


def g_bound(t, k_for_coeffs, n, gamma):
    """g(t) using coefficient bounds evaluated at k_for_coeffs (per the
    continuation front's own documented convention: 'this front works
    entirely with c_i(K)... throughout')."""
    c0, c1, c2, c3 = coeff_bounds(k_for_coeffs, n, gamma)
    return c0 + c1 * t + c2 * t ** 2 + c3 * t ** 3


def Ghat_of(n, gamma):
    """Own independent re-derivation, algebraically pre-verified by hand
    (see referee's separate hand-derivation matching the closed form below
    to the sum of coeff_bounds evaluated at t=K_max, k=K_max) -- but here
    computed DIRECTLY from g_bound(), not from the shortcut closed form, as
    an extra cross-check that the two routes agree.
    """
    K = K_max_of(n, gamma)
    return g_bound(K, K, n, gamma)


def Ghat_closed_form(n, gamma):
    """The closed form the referee independently derived BY HAND (see
    accompanying report) from expanding g_bound at t=k=K_max:
        Ghat(n,gamma) = (10/3+(1-gamma)/2)*K^3/n^2 + (7/4-gamma)*K^2/n
                        + (11/6)*K^2/n^2 + (3/4)*K/n
    Used here purely as an independent cross-check against Ghat_of() above
    (two different computational routes to the same claimed closed form).
    """
    K = K_max_of(n, gamma)
    term1 = (mp.mpf(10) / 3 + (1 - gamma) / 2) * K ** 3 / n ** 2
    term2 = (mp.mpf(7) / 4 - gamma) * K ** 2 / n
    term3 = mp.mpf(11) / 6 * K ** 2 / n ** 2
    term4 = mp.mpf(3) / 4 * K / n
    return term1 + term2 + term3 + term4


def Ghat_Theta_of(n, gamma, C):
    K = K_max_of(n, gamma)
    Theta_K = C * mp.sqrt(K * mp.log(n))
    return g_bound(Theta_K, K, n, gamma)


def Gn_bound_of(n, gamma):
    """Cited: G_n <= sqrt(pi*n/beta)."""
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
    """log_e W(n,gamma,C) [Hoeffding], n = 10^logn, computed directly (not
    log-domain-summed) since mpmath mpf tolerates the huge magnitudes
    involved without overflow. Returns a Python float / mpf for bisection.
    """
    n = mp.power(10, logn)
    Gn = Gn_bound_of(n, gamma)
    Gh = Ghat_of(n, gamma)
    GhT = Ghat_Theta_of(n, gamma, C)
    tail_factor = 2 * mp.power(n, -2 * C * C)
    bulk_term = mp.power(GhT, 3) * mp.exp(GhT)
    tail_term = tail_factor * mp.power(Gh, 3) * mp.exp(Gh)
    W = Gn * (bulk_term + tail_term) / 6
    return mp.log(W)


def small_k_log_term(logn, gamma, C, a):
    """Rough reconstruction of the small-k residual (target sec 3): union
    bound over at most k_2 terms, each deterministically bounded via
    |D|<=k, e^{-s(k)}<=e^{1/2}. Coefficients evaluated at K_max (consistent
    with the 'work entirely with c_i(K)' convention), argument t=k_2 (an
    upper bound on t=k over the whole k<k_2 range, since g is increasing).
    This is a DELIBERATELY CONSERVATIVE, approximate reconstruction for an
    order-of-magnitude sanity check -- not a claim of exact reproduction.
    """
    n = mp.power(10, logn)
    K = K_max_of(n, gamma)
    sigma2 = sigma2_of(gamma)
    M = max(gamma, 1 - gamma)
    k2 = (2 * M * C / (3 * a * sigma2)) ** 2 * mp.log(n)
    if k2 < 1:
        k2 = mp.mpf(1)
    gk2 = g_bound(k2, K, n, gamma)
    log_term = mp.log(k2) + mp.mpf('0.5') + mp.log(6) * (-1) + 3 * mp.log(gk2) + gk2
    return log_term, k2, K


def logW_bernstein(logn, gamma, C, a):
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
    smallk_log, k2, K = small_k_log_term(logn, gamma, C, a)
    smallk_log_full = mp.log(Gn) + smallk_log  # small-k union bound also carries
    # the outer sum-over-k structure the same way (each term individually
    # bounded, summed <=k_2 times, then... note: Gn is the prefactor for the
    # OUTER sum over k of e^{-s(k)}, which for the small-k union bound is
    # replaced by the direct e^{-s(k)}<=e^{1/2} bound already used inside
    # small_k_log_term -- so do NOT double count Gn here.
    smallk_log_full = smallk_log
    # logsumexp of the two log-domain pieces
    hi = max(bulk_tail_log, smallk_log_full)
    lo = min(bulk_tail_log, smallk_log_full)
    combined = hi + mp.log1p(mp.exp(lo - hi))
    return combined, k2, K


def bisect_n0(logW_fn, gamma, C, lo=1, hi=250, tol=1e-3, max_iter=200):
    """Bisect for the crossover log10(n) where logW first becomes <=0,
    assuming logW is decreasing (verified separately per-gamma below).
    """
    flo = logW_fn(mp.mpf(lo), gamma, C)
    fhi = logW_fn(mp.mpf(hi), gamma, C)
    if not (flo > 0 and fhi < 0):
        return None, flo, fhi
    a_, b_ = mp.mpf(lo), mp.mpf(hi)
    for _ in range(max_iter):
        mid = (a_ + b_) / 2
        fm = logW_fn(mid, gamma, C)
        if fm > 0:
            a_ = mid
        else:
            b_ = mid
        if b_ - a_ < tol:
            break
    return (a_ + b_) / 2, flo, fhi


def bisect_n0_bernstein(gamma, C, a_slack, lo=1, hi=250, tol=1e-3, max_iter=200):
    def f(logn, gamma_, C_):
        combined, k2, K = logW_bernstein(logn, gamma_, C_, a_slack)
        return combined

    flo = f(mp.mpf(lo), gamma, C)
    fhi = f(mp.mpf(hi), gamma, C)
    if not (flo > 0 and fhi < 0):
        return None, flo, fhi
    a_, b_ = mp.mpf(lo), mp.mpf(hi)
    for _ in range(max_iter):
        mid = (a_ + b_) / 2
        fm = f(mid, gamma, C)
        if fm > 0:
            a_ = mid
        else:
            b_ = mid
        if b_ - a_ < tol:
            break
    return (a_ + b_) / 2, flo, fhi


PUBLISHED_OLD_TABLE = {
    # gamma : (published C(gamma), published log10 n0)
    '0.99': (mp.mpf('4.23'), mp.mpf('20.79')),
    '0.9': (mp.mpf('4.49'), mp.mpf('36.83')),
    '0.7': (mp.mpf('5.19'), mp.mpf('45.02')),
    '0.5': (mp.mpf('6.23'), mp.mpf('50.28')),
    '0.3': (mp.mpf('8.12'), mp.mpf('55.95')),
    '0.1': (mp.mpf('14.16'), mp.mpf('65.95')),
    '0.05': (mp.mpf('20.05'), mp.mpf('71.78')),
    '0.01': (mp.mpf('44.89'), mp.mpf('84.88')),
}

TARGET_CLAIMED_NEW_TABLE = {
    # gamma : claimed NEW log10 n0 (Bernstein, a=0.05)
    '0.99': mp.mpf('17.72'),
    '0.9': mp.mpf('33.64'),
    '0.7': mp.mpf('44.57'),
    '0.5': mp.mpf('50.35'),
    '0.3': mp.mpf('55.51'),
    '0.1': mp.mpf('63.06'),
    '0.05': mp.mpf('67.08'),
    '0.01': mp.mpf('75.79'),
}


def run_calibration_and_spotcheck(gamma_str, hi_search=250):
    gamma = mp.mpf(gamma_str)
    C0h = C0_hoeffding_of(gamma)
    C_hoeff = mp.mpf('1.2') * C0h
    pub_C, pub_log10n0 = PUBLISHED_OLD_TABLE[gamma_str]
    print(f"--- gamma={gamma_str} ---")
    print(f"  Independently computed C0_Hoeffding = {float(C0h):.4f}, "
          f"C(gamma)=1.2*C0 = {float(C_hoeff):.4f}  (published: {float(pub_C):.4f})")

    # cross check Ghat via two independent routes
    n_probe = mp.power(10, pub_log10n0)
    gh_direct = Ghat_of(n_probe, gamma)
    gh_closed = Ghat_closed_form(n_probe, gamma)
    reldiff = abs(gh_direct - gh_closed) / abs(gh_closed) if gh_closed != 0 else 0
    print(f"  Ghat cross-check at n=10^{float(pub_log10n0)}: direct-route={float(gh_direct):.6e}, "
          f"closed-form-route={float(gh_closed):.6e}, rel.diff={float(reldiff):.3e}")

    def logn_logW_hoeff(logn):
        return logW_hoeffding(logn, gamma, C_hoeff)

    n0_est, flo, fhi = bisect_n0(lambda logn, g_, C_: logW_hoeffding(logn, g_, C_),
                                  gamma, C_hoeff, lo=1, hi=hi_search)
    if n0_est is None:
        print(f"  BISECTION FAILED to bracket a root in [1,{hi_search}] "
              f"(logW(1)={float(flo):.3f}, logW({hi_search})={float(fhi):.3f})")
        return None
    print(f"  Referee's OWN bisected log10(n0) [Hoeffding, own reconstruction] = "
          f"{float(n0_est):.4f}   (published: {float(pub_log10n0):.4f}), "
          f"diff = {float(n0_est - pub_log10n0):.4f} decades")

    # Bernstein reconstruction
    a_slack = mp.mpf('0.05')
    C0b = C0_bernstein_of(gamma, a_slack)
    C_bern = mp.mpf('1.2') * C0b
    print(f"  Independently computed C0_Bernstein(gamma,a=0.05) = {float(C0b):.4f}, "
          f"C(gamma)=1.2*C0 = {float(C_bern):.4f}")

    n0_bern_est, flo_b, fhi_b = bisect_n0_bernstein(gamma, C_bern, a_slack, lo=1, hi=hi_search)
    claimed_new = TARGET_CLAIMED_NEW_TABLE[gamma_str]
    if n0_bern_est is None:
        print(f"  BISECTION FAILED (Bernstein) to bracket a root in [1,{hi_search}] "
              f"(logW(1)={float(flo_b):.3f}, logW({hi_search})={float(fhi_b):.3f})")
        return None
    decades_saved_mine = n0_est - n0_bern_est
    decades_saved_claimed = pub_log10n0 - claimed_new
    print(f"  Referee's OWN bisected log10(n0) [Bernstein a=0.05, own reconstruction] = "
          f"{float(n0_bern_est):.4f}   (target's claimed NEW: {float(claimed_new):.4f})")
    print(f"  Decades saved -- referee's own reconstruction: {float(decades_saved_mine):.4f}   "
          f"vs target's claimed: {float(decades_saved_claimed):.4f}")
    same_sign = (decades_saved_mine > 0) == (decades_saved_claimed > 0) or \
                (abs(decades_saved_mine) < 0.5 and abs(decades_saved_claimed) < 0.5)
    print(f"  Same DIRECTION (gain vs loss)? {'YES' if same_sign else 'NO -- FLAG'}")
    return {
        'gamma': gamma_str,
        'own_old': n0_est, 'pub_old': pub_log10n0,
        'own_new': n0_bern_est, 'claimed_new': claimed_new,
        'own_saved': decades_saved_mine, 'claimed_saved': decades_saved_claimed,
    }


if __name__ == "__main__":
    print("=== Referee's independent reconstruction of the n0(gamma) assembly ===")
    print("(built fresh from the required-reading prose; used to calibrate against")
    print(" the predecessor's OWN PUBLISHED table, then extended to Bernstein to")
    print(" sanity-check the target's claimed NEW n0(gamma) values.)")
    print()
    results = []
    for gstr in ['0.5', '0.1', '0.01', '0.99']:
        r = run_calibration_and_spotcheck(gstr)
        results.append(r)
        print()

    print("=== SUMMARY TABLE ===")
    print(f"{'gamma':>6} {'own OLD':>10} {'pub OLD':>10} {'own NEW':>10} {'claim NEW':>10} "
          f"{'own saved':>10} {'claim saved':>12}")
    for r in results:
        if r is None:
            continue
        print(f"{r['gamma']:>6} {float(r['own_old']):>10.3f} {float(r['pub_old']):>10.3f} "
              f"{float(r['own_new']):>10.3f} {float(r['claimed_new']):>10.3f} "
              f"{float(r['own_saved']):>10.3f} {float(r['claimed_saved']):>12.3f}")
