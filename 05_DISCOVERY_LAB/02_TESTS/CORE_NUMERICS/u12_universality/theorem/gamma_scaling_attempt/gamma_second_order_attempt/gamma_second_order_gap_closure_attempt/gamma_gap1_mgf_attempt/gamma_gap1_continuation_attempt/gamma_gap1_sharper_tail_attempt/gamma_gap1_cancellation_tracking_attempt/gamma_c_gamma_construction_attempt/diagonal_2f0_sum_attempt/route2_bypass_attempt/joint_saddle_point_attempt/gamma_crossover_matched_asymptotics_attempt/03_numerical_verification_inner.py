"""
03_numerical_verification_inner.py

GAMMA-CROSSOVER-MATCHED-ASYMPTOTICS-ATTEMPT (wave 34), DISC-DEC-151.

High-precision (mpmath) numerical verification of script 02's new closed
form:

    term_m(n,gamma) = 1/gamma + A_m(gamma)/n + O(1/n^2),   m = 0,...,6 fixed,
    A_m(gamma) = m(m+3)/(2*gamma) - m(m+1)/gamma^2,

against DIRECT high-precision evaluation of the EXACT term_m(n,gamma)
formula (Beta-integral route, cited/re-verified script 01), pushed to very
large n (up to 10^12) to see the predicted O(1/n) convergence rate
cleanly, and the SECOND-order residual (after subtracting A_m/n) shrink
like O(1/n^2) -- confirming not just that the limit is right but that the
claimed RATE (and hence the specific A_m(gamma) coefficient) is right.

term_m(n,gamma) is evaluated via I(n,m,gamma) = Integral_0^1 t^m(1-t)^m
(1-gamma*t)^(n-m) dt, computed via the s=n*t substitution
(I = (1/n) * Integral_0^n (s/n)^m (1-s/n)^m (1-gamma*s/n)^(n-m) ds), which
keeps the integration variable at O(1) scale even for huge n (avoiding the
t~O(1/n)-scale quadrature difficulties predecessor fronts reported for
their own, different, m=Theta(sqrt(n)) mesoscale quadratures) -- an
independent, fresh evaluator, not importing any ancestor script.
"""
import mpmath as mp


def term_m_exact(n_val, m_val, gamma_val, dps=80):
    """Exact term_m(n,gamma) via the s=n*t substituted Beta integral."""
    mp.mp.dps = dps
    g = mp.mpf(gamma_val)
    n_mp = mp.mpf(n_val)

    def integrand(s):
        t = s / n_mp
        base = t ** m_val * (1 - t) ** m_val
        return base * (1 - g * t) ** (n_val - m_val)

    # seed quadrature with an interior point near the s^m*exp(-gamma s) peak,
    # s* ~ m/gamma (from the leading-order Watson kernel s^m exp(-gamma s)),
    # plus a handful of width markers so mpmath's tanh-sinh finds the bulk
    # of the mass reliably even though m is small and n is huge.
    if m_val == 0:
        nodes = [0, 5 / g, n_mp]
    else:
        speak = mp.mpf(m_val) / g
        nodes = [0, speak, speak + 5 * mp.sqrt(m_val + 1) / g, min(n_mp, speak + 40 / g)]
        nodes = sorted(set(x for x in nodes if x <= n_mp))
        if nodes[-1] != n_mp:
            nodes.append(n_mp)
    I = mp.quad(integrand, nodes) / n_mp
    Bm = mp.factorial(m_val) ** 2 / mp.factorial(2 * m_val + 1)
    Tnm = mp.binomial(n_val + m_val + 1, 2 * m_val + 1) * I / Bm
    return (g ** m_val / n_mp ** m_val) * mp.factorial(m_val) * Tnm


def A_m(m_val, gamma_val):
    g = mp.mpf(gamma_val)
    mm = mp.mpf(m_val)
    return mm * (mm + 3) / (2 * g) - mm * (mm + 1) / g ** 2


print("=" * 100)
print("Part A: leading O(1/n) check -- n*(term_m(n,gamma) - 1/gamma) -> A_m(gamma)")
print("=" * 100)
print(f"{'m':>2} {'gamma':>5} {'n':>14} {'n*(term_m-1/g)':>22} {'A_m predicted':>18} "
      f"{'rel.err':>12}")

gammas = ['0.3', '0.5', '0.8']
m_values = [0, 1, 2, 3, 5]
n_values = [10 ** 3, 10 ** 5, 10 ** 7, 10 ** 9, 10 ** 12]

results_A = []
for gamma_val in gammas:
    for m_val in m_values:
        for n_val in n_values:
            # dps must scale with BOTH n (bigger n needs more guard digits to
            # resolve the O(1/n) signal after subtracting the O(1) leading
            # term) AND m (the prefactor C(n+m+1,2m+1) carries m-dependent
            # cancellation against (n-m)!, needing extra guard digits at
            # larger m) -- a first version of this script used a fixed
            # +40 guard independent of m, which was NOT enough at n=10^12,
            # m>=3 (residuals spuriously blew up to O(1)-O(10^4) instead of
            # shrinking). See Self-caught issues in ATTEMPT.md for the full
            # diagnosis of what was actually going on (a SECOND, more subtle
            # bug: `g`/`Am_pred` were being computed ONCE per (gamma,m) pair
            # -- OUTSIDE the n_val loop -- at whatever mpmath global
            # precision (mp.mp.dps) happened to be active at that point in
            # the loop, which is NOT necessarily the higher dps needed for
            # the largest n in that pair's inner loop; mpf objects freeze in
            # the precision they were created at and do NOT gain accuracy
            # retroactively when mp.mp.dps is later raised. Fixed by
            # recomputing gamma and A_m(gamma) FRESH, at the SAME dps as
            # term_m_exact, immediately before every comparison below.
            dps = max(80, int(mp.log10(mp.mpf(n_val))) + 40 + 10 * m_val)
            tm = term_m_exact(n_val, m_val, gamma_val, dps=dps)
            g = mp.mpf(gamma_val)  # fresh, at the CURRENT (post-tm) high dps
            Am_pred = A_m(m_val, gamma_val)  # fresh, same dps
            lhs = n_val * (tm - 1 / g)
            if Am_pred != 0:
                rel_err = abs((lhs - Am_pred) / Am_pred)
            else:
                rel_err = abs(lhs)  # absolute, since predicted is exactly 0
            results_A.append((m_val, gamma_val, n_val, lhs, Am_pred, rel_err))
            print(f"{m_val:>2} {gamma_val:>5} {n_val:>14} {mp.nstr(lhs, 12):>22} "
                  f"{mp.nstr(Am_pred, 12):>18} {mp.nstr(rel_err, 6):>12}")

print()
print("Convergence check: for m>=1 (A_m != 0), relative error should shrink")
print("roughly like 1/n as n grows (confirming the NEXT order is O(1/n^2),")
print("consistent with the claimed rate, not just the claimed limit).")
print()
print(f"{'m':>2} {'gamma':>5} {'n1':>12} {'n2':>12} {'err1':>14} {'err2':>14} "
      f"{'ratio (expect ~n2/n1)':>24}")
by_key = {}
for (m_val, gamma_val, n_val, lhs, Am_pred, rel_err) in results_A:
    by_key.setdefault((m_val, gamma_val), []).append((n_val, rel_err))
for (m_val, gamma_val), lst in by_key.items():
    if m_val == 0:
        continue  # A_0=0 exactly; relative-error framing not meaningful the same way
    lst.sort()
    for i in range(len(lst) - 1):
        n1, e1 = lst[i]
        n2, e2 = lst[i + 1]
        if e1 == 0:
            continue
        ratio = e1 / e2
        expect = mp.mpf(n2) / mp.mpf(n1)
        print(f"{m_val:>2} {gamma_val:>5} {n1:>12} {n2:>12} {mp.nstr(e1, 6):>14} "
              f"{mp.nstr(e2, 6):>14} {mp.nstr(ratio, 6):>10} (expect ~{mp.nstr(expect, 6)})")

print()
print("=" * 100)
print("Part B: m=0 special case -- confirm EXPONENTIAL (not power-law) convergence")
print("=" * 100)
print("A_0(gamma)=0 predicts term_0(n,gamma)-1/gamma decays FASTER than any")
print("power of 1/n. Cited exact formula: term_0=(1-(1-gamma)^(n+1))/gamma,")
print("so term_0-1/gamma = -(1-gamma)^(n+1)/gamma -- literally exponential.")
print("Confirmed directly (both routes, Beta-integral quadrature and cited")
print("closed form, agree):")
for gamma_val in gammas:
    g = mp.mpf(gamma_val)
    for n_val in [100, 1000]:
        mp.mp.dps = 80
        tm = term_m_exact(n_val, 0, gamma_val, dps=80)
        diff_quad = tm - 1 / g
        diff_closed = -(1 - g) ** (n_val + 1) / g
        print(f"  gamma={gamma_val} n={n_val}: quad diff={mp.nstr(diff_quad, 10)}, "
              f"closed-form diff={mp.nstr(diff_closed, 10)}, "
              f"agree to {mp.nstr(abs(diff_quad - diff_closed), 6)}")

print()
print("ALL PART A-B NUMERICAL CHECKS COMPLETE. See printed relative errors")
print("and convergence ratios above for the quantitative verdict (summarized")
print("in ATTEMPT.md).")
