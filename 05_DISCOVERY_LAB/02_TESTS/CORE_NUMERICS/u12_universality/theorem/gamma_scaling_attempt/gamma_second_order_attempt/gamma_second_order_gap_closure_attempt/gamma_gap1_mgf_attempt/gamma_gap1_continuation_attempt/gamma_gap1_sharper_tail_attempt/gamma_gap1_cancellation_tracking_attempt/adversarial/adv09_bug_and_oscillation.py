"""
Independent referee check #9: (a) directly reproduce the effect of the
self-caught bug described in the target's §8 (using H_K instead of H_k2
in the small-k residual term) to confirm the diagnosis is accurate, and
(b) confirm no spurious oscillation in log W_tight beyond the found n0,
at a couple of representative gamma values, using MY OWN independent
assembly (from adv08), not the target's scripts.
"""
from mpmath import mp, mpf, log, sqrt, exp, pi, ceil, log10

mp.dps = 120

def beta_of(gamma):
    return gamma*(2-gamma)/2

def sigma2_of(gamma):
    return gamma*(1-gamma)

def c_coeffs(gamma, k, n):
    gamma = mpf(gamma); k = mpf(k); n = mpf(n)
    c0 = gamma*k*(2*gamma**2*k**2 - 6*gamma*k**2 + 3*gamma*k + 6*k**2 - 6*k + 1) / (12*n**2)
    c1 = (gamma**2*k**2/2 - gamma*k**2 - gamma*k*n + gamma*k/2 + k**2/2 + k*n - k/2 - n/2 + mpf(1)/12) / n**2
    c2 = (2*gamma*k - 2*k - 2*n + 1) / (4*n**2)
    c3 = mpf(1)/6 / n**2
    return c0, c1, c2, c3

def x_of_D(c, D):
    c0, c1, c2, c3 = c
    return c0 + c1*D + c2*D**2 + c3*D**3

def exact_max_abs_x(k, n, gamma, Dlo, Dhi):
    c0, c1, c2, c3 = c_coeffs(gamma, k, n)
    candidates = [Dlo, Dhi]
    A, B, C_ = 3*c3, 2*c2, c1
    disc = B**2 - 4*A*C_
    if disc >= 0 and A != 0:
        sq = sqrt(disc)
        for r in ((-B+sq)/(2*A), (-B-sq)/(2*A)):
            if Dlo <= r <= Dhi:
                candidates.append(r)
    return max(abs(x_of_D((c0,c1,c2,c3), D)) for D in candidates)

def K_real_of(n, gamma):
    beta = beta_of(gamma)
    return sqrt(4*n*log(n)/beta) + 1

def logW_tight(n, gamma, C, a, use_buggy_smallk=False):
    beta = beta_of(gamma)
    sigma2 = sigma2_of(gamma)
    M = max(gamma, 1-gamma)
    Kr = K_real_of(n, gamma)
    Dmin_K = -gamma*Kr
    Dmax_K = (1-gamma)*Kr
    ThetaK = C*sqrt(Kr*log(n))
    lo_b = max(Dmin_K, -ThetaK)
    hi_b = min(Dmax_K, ThetaK)
    H_Theta = exact_max_abs_x(Kr, n, gamma, lo_b, hi_b)
    H_K = exact_max_abs_x(Kr, n, gamma, Dmin_K, Dmax_K)

    k2 = (2*M*C/(3*a*sigma2))**2 * log(n)
    k2c = ceil(k2)

    if use_buggy_smallk:
        H_smallk = H_K   # THE BUG: using the K-scale value instead of k2-scale
    else:
        Dmin_k2 = -gamma*k2c
        Dmax_k2 = (1-gamma)*k2c
        H_smallk = exact_max_abs_x(k2c, n, gamma, Dmin_k2, Dmax_k2)

    logGn = mpf('0.5')*(log(pi) + log(n) - log(beta))
    log_bulk = 3*log(H_Theta) + H_Theta
    log_tail = log(2) - (C**2/((2+a)*sigma2))*log(n) + 3*log(H_K) + H_K
    m = max(log_bulk, log_tail)
    log_bulk_tail_sum = m + log(exp(log_bulk-m) + exp(log_tail-m))
    log_bulk_tail_term = logGn + log(mpf(1)/6) + log_bulk_tail_sum

    log_smallk_term = log(mpf(1)/6) + log(k2c) + mpf('0.5') + 3*log(H_smallk) + H_smallk

    m2 = max(log_bulk_tail_term, log_smallk_term)
    logW = m2 + log(exp(log_bulk_tail_term-m2) + exp(log_smallk_term-m2))
    return logW

print("=== Part (a): reproducing the self-caught bug's qualitative effect ===")
print("(gamma=0.5, C=1.595, a=0.05 -- the target's own reported working point)")
gamma = mpf('0.5'); C = mpf('1.595'); a = mpf('0.05')
print(f"{'log10(n)':>10} {'logW (FIXED, H_k2)':>22} {'logW (BUGGY, H_K)':>22}")
for t in [10, 20, 30, 35, 40, 44, 50, 60, 70]:
    n = mpf(10)**t
    lw_fixed = logW_tight(n, gamma, C, a, use_buggy_smallk=False)
    lw_buggy = logW_tight(n, gamma, C, a, use_buggy_smallk=True)
    print(f"{t:>10} {float(lw_fixed):>22.4f} {float(lw_buggy):>22.4f}")

print("\nExpectation per target's §8 disclosure: the FIXED version should decay")
print("(logW decreasing, eventually crossing below 0), while the BUGGY version")
print("should NOT decay properly (should grow or stay large/positive, 'no sign")
print("of a crossing... up to n=10^44').")

print("\n\n=== Part (b): no-spurious-oscillation check beyond n0, my own assembly ===")
for gamma, C, log10n0_target in [(mpf('0.5'), mpf('1.595'), 35.49), (mpf('0.01'), mpf('2.022'), 61.17)]:
    print(f"\ngamma={float(gamma)}, C={float(C)}: scanning log10(n) from n0-2 to n0+20 decades")
    prev = None
    increasing_found = False
    for t_offset_tenths in range(-20, 201, 5):  # step 0.5 decades
        t = float(log10n0_target) + t_offset_tenths/10.0
        n = mpf(10)**mpf(t)
        lw = logW_tight(n, gamma, C, a)
        if prev is not None and lw > prev + mpf('1e-6'):
            increasing_found = True
            print(f"  LOCAL INCREASE at log10(n)={t:.2f}: logW={float(lw):.6f} > prev={float(prev):.6f}")
        prev = lw
    print(f"  increasing_found = {increasing_found}  (False = clean monotone decay, matches target's own claim)")
