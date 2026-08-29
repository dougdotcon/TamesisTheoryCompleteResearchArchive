"""
Independent referee check #8/#9: fresh re-implementation of the FULL
W_tight(n,gamma,C,a) assembly from the target's own §9 formulas (quoted in
its ATTEMPT.md, NOT read from any of the target's own .py scripts), to
independently recompute n0(gamma) at several sample gamma and check against
the target's published table.

Also checks:
 - K_real(n,gamma) := sqrt(4 n ln n / beta) + 1 is a valid upper bound on
   the true ceiling K := ceil(sqrt((4/beta) n ln n)) for all n>=2 (elementary
   ceil(x)<=x+1 fact) -- spot-checked numerically.
 - K_max/K_real -> 2 as n->infinity (the "~2x tighter" claim).
 - k-uniformity spot check: max|x_k(D)| over the true range, at k=K_real,
   is >= the same quantity at smaller k (monotonicity in k), sampled at
   several k across [1, K_real].
"""
from mpmath import mp, mpf, log, sqrt, exp, pi, ceil, findroot, log10

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
    """Exact max of |x_k(D)| over D in [Dlo,Dhi] via endpoints + interior
    critical points of x'(D)=c1+2c2D+3c3D^2=0 (quadratic formula, exact)."""
    c0, c1, c2, c3 = c_coeffs(gamma, k, n)
    candidates = [Dlo, Dhi]
    # roots of 3*c3*D^2 + 2*c2*D + c1 = 0
    A, B, C_ = 3*c3, 2*c2, c1
    disc = B**2 - 4*A*C_
    if disc >= 0 and A != 0:
        sq = sqrt(disc)
        r1 = (-B + sq)/(2*A)
        r2 = (-B - sq)/(2*A)
        for r in (r1, r2):
            if Dlo <= r <= Dhi:
                candidates.append(r)
    vals = [abs(x_of_D((c0, c1, c2, c3), D)) for D in candidates]
    return max(vals)

def K_real_of(n, gamma):
    beta = beta_of(gamma)
    return sqrt(4*n*log(n)/beta) + 1

def true_K_ceil(n, gamma):
    beta = beta_of(gamma)
    return ceil(sqrt(4*n*log(n)/beta))

def C0_tight_sq(gamma, a):
    beta = beta_of(gamma)
    sigma2 = sigma2_of(gamma)
    gamma_star = 1 - sqrt(mpf(2))/2
    if gamma >= gamma_star:
        lam = mpf(4)
    else:
        lam = 4*(1-gamma)**2/(gamma*(2-gamma))
    return (2+a)*sigma2*(lam + mpf('0.5'))

def logW_tight(n, gamma, C, a):
    beta = beta_of(gamma)
    sigma2 = sigma2_of(gamma)
    M = max(gamma, 1-gamma)
    Kr = K_real_of(n, gamma)
    Dmin_K = -gamma*Kr
    Dmax_K = (1-gamma)*Kr
    ThetaK = C*sqrt(Kr*log(n))
    # bulk radius intersected with true support
    lo_b = max(Dmin_K, -ThetaK)
    hi_b = min(Dmax_K, ThetaK)
    H_Theta = exact_max_abs_x(Kr, n, gamma, lo_b, hi_b)
    H_K = exact_max_abs_x(Kr, n, gamma, Dmin_K, Dmax_K)

    k2 = (2*M*C/(3*a*sigma2))**2 * log(n)
    k2c = ceil(k2)
    Dmin_k2 = -gamma*k2c
    Dmax_k2 = (1-gamma)*k2c
    H_k2 = exact_max_abs_x(k2c, n, gamma, Dmin_k2, Dmax_k2)

    logGn = mpf('0.5')*(log(pi) + log(n) - log(beta))
    log_bulk = 3*log(H_Theta) + H_Theta
    log_tail = log(2) - (C**2/((2+a)*sigma2))*log(n) + 3*log(H_K) + H_K
    # logaddexp
    m = max(log_bulk, log_tail)
    log_bulk_tail_sum = m + log(exp(log_bulk-m) + exp(log_tail-m))
    log_bulk_tail_term = logGn + log(mpf(1)/6) + log_bulk_tail_sum

    log_smallk_term = log(mpf(1)/6) + log(k2c) + mpf('0.5') + 3*log(H_k2) + H_k2

    m2 = max(log_bulk_tail_term, log_smallk_term)
    logW = m2 + log(exp(log_bulk_tail_term-m2) + exp(log_smallk_term-m2))
    return logW, dict(H_Theta=H_Theta, H_K=H_K, H_k2=H_k2, k2=k2c, Kr=Kr,
                       log_bulk_tail_term=log_bulk_tail_term, log_smallk_term=log_smallk_term)

def bisect_n0(gamma, C, a, lo10=5, hi10=90, tol=1e-4):
    """Bisection in log10(n) for logW(n)=0 crossing (searching for the point
    beyond which logW stays negative)."""
    def f(t):
        n = mpf(10)**mpf(t)
        lw, _ = logW_tight(n, gamma, C, a)
        return lw
    flo = f(lo10)
    fhi = f(hi10)
    # expand hi if needed
    tries = 0
    while flo < 0 and tries < 5:
        lo10 -= 10
        flo = f(lo10)
        tries += 1
    tries = 0
    while fhi > 0 and tries < 8:
        hi10 += 20
        fhi = f(hi10)
        tries += 1
    a_, b_ = lo10, hi10
    fa, fb = flo, fhi
    if fa*fb > 0:
        return None  # no sign change found in range
    for _ in range(200):
        mid = (a_+b_)/2
        fm = f(mid)
        if fm > 0:
            a_ = mid
        else:
            b_ = mid
        if b_-a_ < tol:
            break
    return (a_+b_)/2

# ============================================================
# PART A: K_real validity + K_max/K_real ~ 2 ratio check
# ============================================================
print("=== PART A: K_real validity and K_max/K_real ratio ===")
for gamma in [mpf('0.5'), mpf('0.1'), mpf('0.9'), mpf('0.01'), mpf('0.99')]:
    for n in [mpf(10)**10, mpf(10)**30, mpf(10)**60]:
        Kr = K_real_of(n, gamma)
        Ktrue = true_K_ceil(n, gamma)
        ok = Ktrue <= Kr
        beta = beta_of(gamma)
        Kmax_continuation = 4*sqrt(n*log(n)/beta)
        ratio = Kmax_continuation/Kr
        print(f"gamma={float(gamma):.2f} n=1e{int(log10(n))}: K_real={float(Kr):.6g} "
              f"K_true_ceil={float(Ktrue):.6g} valid_upper_bound={ok}  K_max/K_real={float(ratio):.4f}")
print()

# ============================================================
# PART B: k-uniformity spot check (max|x_k(D)| over true range,
# monotone-ish in k, dominated by value at k=K_real)
# ============================================================
print("=== PART B: k-uniformity spot check (H_k <= H_{K_real} for k<=K_real) ===")
import random
random.seed(20260938001)  # NOT drawing from the target's reserved block; my own referee seed
violations = 0
checks = 0
for gamma in [mpf('0.01'), mpf('0.1'), mpf('0.5'), mpf('0.9'), mpf('0.99')]:
    for n in [mpf(10)**15, mpf(10)**30]:
        Kr = K_real_of(n, gamma)
        H_full_K = exact_max_abs_x(Kr, n, gamma, -gamma*Kr, (1-gamma)*Kr)
        for frac in [mpf('0.001'), mpf('0.01'), mpf('0.1'), mpf('0.5'), mpf('0.9'), mpf('0.999')]:
            k = max(mpf(1), frac*Kr)
            Dlo, Dhi = -gamma*k, (1-gamma)*k
            H_k = exact_max_abs_x(k, n, gamma, Dlo, Dhi)
            checks += 1
            if H_k > H_full_K:
                violations += 1
                print(f"  VIOLATION: gamma={float(gamma)} n=1e{int(log10(n))} k-frac={float(frac)} "
                      f"H_k={float(H_k)} > H_K={float(H_full_K)}")
print(f"Total checks: {checks}, violations: {violations}")
print()

# ============================================================
# PART C: recompute n0(gamma) at sample points using the target's own
# reported C(gamma), margin, and a=0.05, then compare log10(n0).
# ============================================================
print("=== PART C: independent recomputation of n0(gamma) at target's reported C(gamma) ===")
a = mpf('0.05')
targets = [
    # gamma,   C(gamma) reported,  target's log10(n0)
    (mpf('0.5'),  mpf('1.595'), mpf('35.49')),
    (mpf('0.01'), mpf('2.022'), mpf('61.17')),
    (mpf('0.9'),  mpf('0.957'), mpf('19.09')),
    (mpf('0.99'), mpf('0.317'), mpf('15.42')),
    (mpf('0.1'),  mpf('1.818'), mpf('47.72')),
]
for gamma, Cval, target_log10n0 in targets:
    # sanity: also recompute C0_tight_sq and compare against target's own C(gamma)
    C0sq = C0_tight_sq(gamma, a)
    print(f"\ngamma={float(gamma)}: my C0_tight^2={float(C0sq):.6f}  sqrt={float(sqrt(C0sq)):.6f}  "
          f"target's C(gamma)={float(Cval)} (should be margin*sqrt(C0sq), margin close to 1.0x-1.05x)")
    n0_found = bisect_n0(gamma, Cval, a, lo10=5, hi10=90)
    if n0_found is None:
        print(f"  gamma={float(gamma)}: bisection FAILED to find a sign change in [5,90] decades")
    else:
        print(f"  gamma={float(gamma)}: MY log10(n0) = {float(n0_found):.3f}   "
              f"TARGET's log10(n0) = {float(target_log10n0)}   "
              f"diff = {float(n0_found-target_log10n0):.3f} decades")
