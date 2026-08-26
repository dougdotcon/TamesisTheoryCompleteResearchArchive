"""
Gap 2 closure -- symbolic verification (sympy).

Written from scratch, from the mathematical prose of THEOREM.md and the
predecessor gamma_second_order_attempt/ATTEMPT.md only. No .py file from
any prior front was opened or imported.

Checks:
  (A) tau(m) := sum_{i=1}^m ((k-i)/n)^2 has the claimed exact cubic-in-m
      closed form, for several concrete symbolic/numeric k.
  (B) The classical Binomial(k,p) raw-moment formulas E[M], E[M^2], E[M^3]
      (via factorial moments) match direct pmf summation, for several k.
  (C) Delta_tau(k) := E_M[tau(M)] - tau(gamma*k)  (M ~ Bin(k,gamma))
      equals the exact closed form
        Delta_tau(k) = [ -k^2*g*(1-g)^2 + k*g*(1-g)*(5-4g)/6 ] / n^2
      via (i) direct symbolic substitution of the raw moments into the
      cubic tau(m), and (ii) direct pmf summation for concrete small k.
  (D) Consistency check: the exact Delta_tau(k) equals the *exact* 3rd-order
      Taylor expansion of tau about m=gamma*k (tau is a cubic polynomial,
      so its own 3rd order Taylor expansion is itself, exactly, no
      remainder) -- i.e.
        Delta_tau(k) = tau''(gamma*k)*Var(M)/2 + tau'''(gamma*k)*mu3(M)/6
      using the classical 2nd/3rd central Binomial moments
      Var(M)=k*g*(1-g), mu3(M)=k*g*(1-g)*(1-2g).
"""
import sympy as sp

k, n, m, g, i = sp.symbols('k n m gamma i', positive=True)

print("=" * 70)
print("(A) tau(m) closed form")
print("=" * 70)

# definition: tau(m) = sum_{i=1}^m ((k-i)/n)^2
tau_sum = sp.summation(((k - i) / n) ** 2, (i, 1, m))
tau_sum = sp.expand(tau_sum)

tau_claimed = (m**3 / 3 + m**2 * (sp.Rational(1, 2) - k) + m * (k**2 - k + sp.Rational(1, 6))) / n**2
tau_claimed = sp.expand(tau_claimed)

diff_A = sp.simplify(tau_sum - tau_claimed)
print("sympy closed-form of sum_{i=1}^m ((k-i)/n)^2 :", sp.factor(tau_sum))
print("claimed cubic form                            :", sp.factor(tau_claimed))
print("difference (should be exactly 0):", diff_A)
assert diff_A == 0, "tau(m) cubic closed form MISMATCH"
print("PASS: tau(m) cubic closed form confirmed symbolically, exact for all m,k,n.\n")

print("=" * 70)
print("(B) Binomial raw moments via factorial moments vs direct pmf sum")
print("=" * 70)
p = sp.symbols('p', positive=True)
for kk in [1, 2, 3, 4, 5]:
    M = sp.symbols('M')
    mm = sp.symbols('mm', integer=True, nonnegative=True)
    pmf = sp.binomial(kk, mm) * p**mm * (1 - p)**(kk - mm)
    E1_direct = sp.summation(mm * pmf, (mm, 0, kk))
    E2_direct = sp.summation(mm**2 * pmf, (mm, 0, kk))
    E3_direct = sp.summation(mm**3 * pmf, (mm, 0, kk))
    E1_direct = sp.simplify(E1_direct)
    E2_direct = sp.simplify(E2_direct)
    E3_direct = sp.simplify(E3_direct)

    E1_formula = kk * p
    E2_formula = kk * (kk - 1) * p**2 + kk * p
    E3_formula = kk * (kk - 1) * (kk - 2) * p**3 + 3 * kk * (kk - 1) * p**2 + kk * p

    d1 = sp.simplify(E1_direct - E1_formula)
    d2 = sp.simplify(E2_direct - E2_formula)
    d3 = sp.simplify(E3_direct - E3_formula)
    print(f"k={kk}: E[M]-formula={d1}, E[M^2]-formula={d2}, E[M^3]-formula={d3}")
    assert d1 == 0 and d2 == 0 and d3 == 0, f"Binomial moment mismatch at k={kk}"
print("PASS: classical Binomial raw-moment formulas confirmed at k=1..5.\n")

print("=" * 70)
print("(C) Delta_tau(k) exact closed form: two independent derivations")
print("=" * 70)

# route 1: substitute the (now-confirmed) raw moment formulas into tau(m),
# linearity of expectation, then subtract tau(gamma*k).
EM1 = k * g
EM2 = k * (k - 1) * g**2 + k * g
EM3 = k * (k - 1) * (k - 2) * g**3 + 3 * k * (k - 1) * g**2 + k * g

a_coef = sp.Rational(1, 3)
b_coef = sp.Rational(1, 2) - k
c_coef = k**2 - k + sp.Rational(1, 6)

E_tau_M = (a_coef * EM3 + b_coef * EM2 + c_coef * EM1) / n**2
tau_gk = (a_coef * (g * k)**3 + b_coef * (g * k)**2 + c_coef * (g * k)) / n**2

Delta_tau_route1 = sp.simplify(sp.expand(E_tau_M - tau_gk))

Delta_tau_claimed = (-k**2 * g * (1 - g)**2 + k * g * (1 - g) * (5 - 4 * g) / 6) / n**2
Delta_tau_claimed = sp.simplify(Delta_tau_claimed)

diff_C1 = sp.simplify(Delta_tau_route1 - Delta_tau_claimed)
print("Delta_tau (route 1, moment substitution)      :", sp.factor(Delta_tau_route1))
print("Delta_tau (claimed closed form)                :", sp.factor(Delta_tau_claimed))
print("difference (should be exactly 0):", diff_C1)
assert diff_C1 == 0, "Delta_tau closed form MISMATCH (route 1)"
print("PASS: route 1 (moment substitution) confirmed.\n")

# route 2: direct pmf summation for several concrete small k (fully
# independent of the factorial-moment machinery of route 1/part B).
print("route 2: direct pmf summation, concrete k")
for kk in [1, 2, 3, 4, 5, 6]:
    mm = sp.symbols('mm', integer=True, nonnegative=True)
    pmf = sp.binomial(kk, mm) * g**mm * (1 - g)**(kk - mm)
    tau_of_mm = (a_coef.subs(k, kk) * mm**3 + b_coef.subs(k, kk) * mm**2 + c_coef.subs(k, kk) * mm) / n**2
    E_tau_direct = sp.summation(tau_of_mm * pmf, (mm, 0, kk))
    E_tau_direct = sp.simplify(E_tau_direct)
    tau_gk_kk = tau_gk.subs(k, kk)
    Delta_direct = sp.simplify(E_tau_direct - tau_gk_kk)
    Delta_target = sp.simplify(Delta_tau_claimed.subs(k, kk))
    diff = sp.simplify(Delta_direct - Delta_target)
    print(f"  k={kk}: direct-pmf Delta_tau - claimed = {diff}")
    assert diff == 0, f"Delta_tau route-2 mismatch at k={kk}"
print("PASS: route 2 (direct pmf summation, k=1..6) confirmed independently.\n")

print("=" * 70)
print("(D) Consistency: exact Delta_tau == exact 3rd-order Taylor of the")
print("    cubic tau(m) about m=gamma*k (no remainder, since tau is cubic)")
print("=" * 70)
tau_m = a_coef * m**3 + b_coef * m**2 + c_coef * m  # times 1/n^2 implicit
tau_m = tau_m  # keep as n^2 * tau(m) for convenience, matches earlier scaling
tau1 = sp.diff(tau_m, m)
tau2 = sp.diff(tau_m, m, 2)
tau3 = sp.diff(tau_m, m, 3)

Var_M = k * g * (1 - g)              # classical Binomial variance
mu3_M = k * g * (1 - g) * (1 - 2 * g)  # classical Binomial 3rd central moment

taylor3_n2 = tau2.subs(m, g * k) * Var_M / 2 + tau3.subs(m, g * k) * mu3_M / 6
taylor3 = sp.simplify(taylor3_n2 / n**2)

diff_D = sp.simplify(taylor3 - Delta_tau_claimed)
print("tau''(gamma k):", sp.factor(tau2.subs(m, g*k)))
print("tau'''(gamma k) (constant):", tau3)
print("3rd-order Taylor (exact, no remainder) reconstruction:", sp.factor(taylor3))
print("difference vs claimed Delta_tau (should be exactly 0):", diff_D)
assert diff_D == 0, "Taylor-consistency check MISMATCH"
print("PASS: exact algebra matches exact 3rd-order Taylor reconstruction.\n")

print("ALL SYMBOLIC CHECKS (A)-(D) PASSED.")
