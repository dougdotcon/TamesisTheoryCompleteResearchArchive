"""
Adversarial re-derivation A: tau(m) cubic form and Delta-tau(k) closed form.
Written fresh from THEOREM.md + predecessor ATTEMPT.md prose only.
No .py file of any front in this lineage was opened.
"""
import sympy as sp

m, k, n, gamma, i = sp.symbols('m k n gamma i', positive=True)

# --- Part A: tau(m) cubic closed form, from its defining sum ---
tau_sum = sp.summation(((k - i) / n) ** 2, (i, 1, m))
tau_sum = sp.expand(tau_sum)

tau_claimed = (1 / n**2) * (m**3 / 3 + m**2 * (sp.Rational(1, 2) - k) + m * (k**2 - k + sp.Rational(1, 6)))

diffA = sp.simplify(tau_sum - tau_claimed)
print("Part A: tau(m) sum - claimed cubic form, simplified difference =", diffA)
assert diffA == 0, "Part A FAILED"
print("Part A PASS: tau(m) cubic closed form confirmed by direct symbolic summation.\n")

# --- Part B: classical binomial raw moments, symbolic check for k=1..6 ---
p = sp.symbols('p', positive=True)
maxk_check = 6
all_pass = True
for kk in range(1, maxk_check + 1):
    Msum = sp.symbols('Msum')
    pmf = lambda mm: sp.binomial(kk, mm) * p**mm * (1 - p)**(kk - mm)
    EM1 = sp.simplify(sum(mm * pmf(mm) for mm in range(0, kk + 1)))
    EM2 = sp.simplify(sum(mm**2 * pmf(mm) for mm in range(0, kk + 1)))
    EM3 = sp.simplify(sum(mm**3 * pmf(mm) for mm in range(0, kk + 1)))
    EM1c = kk * p
    EM2c = kk * (kk - 1) * p**2 + kk * p
    EM3c = kk * (kk - 1) * (kk - 2) * p**3 + 3 * kk * (kk - 1) * p**2 + kk * p
    d1 = sp.simplify(EM1 - EM1c)
    d2 = sp.simplify(EM2 - EM2c)
    d3 = sp.simplify(EM3 - EM3c)
    ok = (d1 == 0 and d2 == 0 and d3 == 0)
    all_pass = all_pass and ok
    print(f"Part B k={kk}: E[M]diff={d1}, E[M^2]diff={d2}, E[M^3]diff={d3}  {'PASS' if ok else 'FAIL'}")
assert all_pass, "Part B FAILED"
print("Part B PASS: classical binomial raw moment formulas confirmed for k=1..6.\n")

# --- Part C route 1: Delta-tau(k) via moment substitution (general k, symbolic gamma) ---
EM1g = k * gamma
EM2g = k * (k - 1) * gamma**2 + k * gamma
EM3g = k * (k - 1) * (k - 2) * gamma**3 + 3 * k * (k - 1) * gamma**2 + k * gamma

def tau_of(mval):
    return (1 / n**2) * (mval**3 / 3 + mval**2 * (sp.Rational(1, 2) - k) + mval * (k**2 - k + sp.Rational(1, 6)))

E_tau_M = (1 / n**2) * (EM3g / 3 + EM2g * (sp.Rational(1, 2) - k) + EM1g * (k**2 - k + sp.Rational(1, 6)))
tau_gk = tau_of(gamma * k)

delta_tau_route1 = sp.simplify(E_tau_M - tau_gk)

delta_tau_claimed = (-k**2 * gamma * (1 - gamma)**2 + sp.Rational(1, 6) * k * gamma * (1 - gamma) * (5 - 4 * gamma)) / n**2

diffC1 = sp.simplify(delta_tau_route1 - delta_tau_claimed)
print("Part C route 1 (moment substitution): Delta-tau(k) route1 - claimed, simplified =", diffC1)
assert diffC1 == 0, "Part C route 1 FAILED"
print("Route1 =", sp.simplify(delta_tau_route1))
print("Part C route 1 PASS.\n")

# --- Part C route 2: Delta-tau(k) via DIRECT pmf summation for concrete k=1..6, symbolic gamma ---
all_pass2 = True
for kk in range(1, 7):
    kkS = sp.Integer(kk)  # BUG #2 FOUND AND FIXED: a plain python int `mval` from
    # range() makes expressions like `mval**3/3` execute as *pure python* integer/
    # float division (e.g. 8/3 -> 2.6667 float) instead of exact sympy Rational,
    # because sympy only intercepts the division once ONE of the two operands is
    # already a sympy object. Every concrete int (kk and each mval) must be wrapped
    # in sp.Integer(...) before arithmetic to stay in exact rational arithmetic.
    pmf = lambda mval: sp.binomial(kkS, mval) * gamma**mval * (1 - gamma)**(kkS - mval)
    # BUG #1 FOUND AND FIXED: tau_of() closes over the free symbol `k`, which must be
    # substituted to the concrete kk value -- the first version of this script left
    # `k` unsubstituted, producing spurious nonzero "differences" that were actually
    # leftover k vs kk mismatch, not a real disagreement with the closed form.
    tau_of_kk = lambda mval: tau_of(mval).subs(k, kkS)
    E_tau_M_direct = sp.nsimplify(sp.expand(sum(pmf(sp.Integer(mv)) * tau_of_kk(sp.Integer(mv)) for mv in range(0, kk + 1))))
    tau_gk_here = tau_of_kk(gamma * kkS)
    delta_direct = sp.nsimplify(sp.expand(E_tau_M_direct - tau_gk_here))
    delta_claim_here = sp.nsimplify(sp.expand(delta_tau_claimed.subs(k, kkS)))
    diff2 = sp.nsimplify(sp.expand(delta_direct - delta_claim_here))
    ok2 = (diff2 == 0)
    all_pass2 = all_pass2 and ok2
    print(f"Part C route2 k={kk}: direct-pmf Delta-tau - claimed, diff = {diff2}  {'PASS' if ok2 else 'FAIL'}")
assert all_pass2, "Part C route 2 FAILED"
print("Part C route 2 PASS: direct pmf summation matches closed form exactly for k=1..6, all symbolic in gamma.\n")

# --- Part D: exact 3rd-order Taylor reconstruction (tau is cubic, so this should be EXACT) ---
D = sp.symbols('D')  # M - gamma*k
Var_M = k * gamma * (1 - gamma)
mu3_M = k * gamma * (1 - gamma) * (1 - 2 * gamma)

tau_expr = tau_of(m)
tau_p = sp.diff(tau_expr, m)
tau_pp = sp.diff(tau_expr, m, 2)
tau_ppp = sp.diff(tau_expr, m, 3)

tau_pp_at = sp.simplify(tau_pp.subs(m, gamma * k))
tau_ppp_at = sp.simplify(tau_ppp.subs(m, gamma * k))  # constant, cubic->3rd deriv const

taylor_recon = sp.simplify(tau_pp_at * Var_M / 2 + tau_ppp_at * mu3_M / 6)
diffD = sp.simplify(taylor_recon - delta_tau_claimed)
print("Part D: exact 3rd-order Taylor reconstruction - claimed closed form, diff =", diffD)
assert diffD == 0, "Part D FAILED"
print("Part D PASS: tau''(gk)*Var/2 + tau'''(gk)*mu3/6 EXACTLY reproduces Delta-tau(k) (as expected, tau cubic => zero remainder).\n")

# --- Sanity: gamma=1 check ---
val_at_gamma1 = sp.simplify(delta_tau_claimed.subs(gamma, 1))
print("Delta-tau(k) at gamma=1:", val_at_gamma1)
assert val_at_gamma1 == 0

print("\nALL PART A-D CHECKS PASSED.")
