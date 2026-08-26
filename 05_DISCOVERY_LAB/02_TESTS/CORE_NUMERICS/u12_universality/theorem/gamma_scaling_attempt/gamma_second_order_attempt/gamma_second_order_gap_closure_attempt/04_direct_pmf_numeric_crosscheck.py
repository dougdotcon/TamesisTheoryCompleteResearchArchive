"""
Gap 2 closure -- independent NUMERIC (not symbolic) cross-check of
Delta_tau(k) = E_M[tau(M)] - tau(gamma*k), M ~ Bin(k, gamma).

This script never uses the closed-form Delta_tau formula to *compute*
E_M[tau(M)]; instead it computes E_M[tau(M)] by direct high-precision
weighted summation over the full support m=0..k of the exact Binomial
pmf (mpmath, dps=50), for k values up to several hundred (well beyond
what sympy's exact symbolic summation in script 01 covered, k=1..6) and
several (n, gamma), then compares against the closed form. This is a
second, structurally different implementation (floating high-precision
numerics vs exact symbolic algebra) of the same claim, per this
lineage's convention of independent symbolic + numeric cross-checks.
"""
from mpmath import mp, mpf, binomial, exp, log

mp.dps = 50


def tau(m, k, n):
    m = mpf(m)
    k = mpf(k)
    n = mpf(n)
    return (m**3 / 3 + m**2 * (mpf('0.5') - k) + m * (k**2 - k + mpf(1) / 6)) / n**2


def E_tau_direct(k, n, gamma, kfloat=None):
    """E_M[tau(M)] via direct pmf summation, M ~ Bin(k, gamma)."""
    g = mpf(gamma)
    total = mpf(0)
    for m in range(0, k + 1):
        # binomial pmf via log-space for numerical stability at larger k
        logpmf = mp.loggamma(k + 1) - mp.loggamma(m + 1) - mp.loggamma(k - m + 1)
        if m > 0:
            logpmf += m * mp.log(g)
        if k - m > 0:
            logpmf += (k - m) * mp.log(1 - g)
        pmf = exp(logpmf)
        total += pmf * tau(m, k, n)
    return total


def delta_tau_closed(k, n, gamma):
    g = mpf(gamma)
    kk = mpf(k)
    return (-kk**2 * g * (1 - g)**2 + kk * g * (1 - g) * (5 - 4 * g) / 6) / mpf(n)**2


print("=" * 95)
print("Direct pmf summation E_M[tau(M)] - tau(gamma k)  vs  closed-form Delta_tau(k)")
print("(second, independent numeric implementation -- no symbolic algebra used here)")
print("=" * 95)
print(f"{'gamma':>7} {'n':>10} {'k':>6} {'E[tau(M)]-tau(gk) direct':>28} {'closed form':>20} {'abs diff':>14}")

test_cases = []
for gamma in [mpf('0.1'), mpf('0.5'), mpf('0.9')]:
    for n in [10000, 200000]:
        for k in [5, 50, 250, 700]:
            test_cases.append((gamma, n, k))

max_abs_diff = mpf(0)
for gamma, n, k in test_cases:
    tau_gk = tau(gamma * k, k, n)
    direct = E_tau_direct(k, n, gamma) - tau_gk
    closed = delta_tau_closed(k, n, gamma)
    diff = abs(direct - closed)
    max_abs_diff = max(max_abs_diff, diff)
    print(f"{float(gamma):7.2f} {n:10d} {k:6d} {float(direct):28.16e} {float(closed):20.16e} {float(diff):14.3e}")

print()
print(f"Max |direct - closed-form| across all {len(test_cases)} test cases: {float(max_abs_diff):.3e}")
print("(should be at the mpmath dps=50 rounding floor -- i.e. numerically exact agreement)")
assert max_abs_diff < mpf('1e-40'), "Direct pmf summation disagrees with closed form beyond rounding!"
print("PASS: independent high-precision numeric summation confirms the closed form exactly.")
