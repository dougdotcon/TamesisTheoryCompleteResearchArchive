# Fresh, from-scratch symbolic derivation (sympy) of the exact cubic-in-D
# closed form of x(D) := delta(D) + tau(M)/2, the combined log-correction
# whose Taylor remainder is exactly what Gap 1 (Estagio 26 Section 5 /
# predecessor ATTEMPT.md Section 5) needs a bound on.
#
# Ingredients, both cited from the archive's own prose (not re-derived from
# a first-principles combinatorial definition, since sigma_k(m) itself is
# not restated in the required-reading sections -- only the two identities
# below, both already PROVED/used in the lineage, are used as black boxes):
#
#   tau(m) := sum_{i=1}^m ((k-i)/n)^2          [defined in gamma_second_order
#                                                _attempt/ATTEMPT.md Section 4]
#   delta(D) := sigma_k(m) - s(k), m = gamma*k + D, via the wave-17 front's
#   own exact algebraic identity
#       sigma_k(m) - sigma_k(x) = (m-x)(2k-m-x-1)/(2n),  x = gamma*k
#   (quoted in gamma_second_order_attempt/ATTEMPT.md line 289; used here
#   exactly as stated, not re-derived from sigma_k's own definition, which
#   this front's required reading does not include).
#
# No .py file of any prior front was opened, read, or imported. This script
# is written fresh from the mathematical prose only.
#
# Output: the exact coefficients c0,c1,c2,c3 of x(D) = c0+c1*D+c2*D^2+c3*D^3,
# cross-checked two ways (symbolic Poly extraction vs. hand-substitution),
# plus the gamma=1 degenerate-case consistency check (D=0 a.s. there).

import sympy as sp

k, n, gamma, m, D = sp.symbols('k n gamma m D', real=True)
i = sp.symbols('i', integer=True)

print("=" * 78)
print("PART A: tau(m) closed form, re-derived and checked against the sum")
print("=" * 78)

tau_sum = sp.summation(((k - i) / n) ** 2, (i, 1, m))
tau_closed = (sp.Rational(1, 3) * m**3
              + m**2 * (sp.Rational(1, 2) - k)
              + m * (k**2 - k + sp.Rational(1, 6))) / n**2
diff_tau = sp.simplify(tau_sum - tau_closed)
print("tau(m) [sympy summation] - tau(m) [claimed closed form] =", diff_tau)
assert diff_tau == 0, "tau(m) closed form FAILED"
print("PASS: tau(m) closed form confirmed via sympy.summation, exact zero difference.")

print()
print("=" * 78)
print("PART B: delta(D), exact, from the cited identity")
print("=" * 78)

delta_D = D * (2 * k * (1 - gamma) - D - 1) / (2 * n)
print("delta(D) =", sp.simplify(delta_D))
print("Sanity: delta(0) =", delta_D.subs(D, 0), "(must be 0, since m=gamma*k there)")
assert sp.simplify(delta_D.subs(D, 0)) == 0

print()
print("=" * 78)
print("PART C: x(D) := delta(D) + tau(M)/2, M = gamma*k + D -- exact cubic")
print("=" * 78)

M_expr = gamma * k + D
tau_M = sp.expand(tau_closed.subs(m, M_expr))
x_D = sp.expand(delta_D + tau_M / 2)
x_poly = sp.Poly(x_D, D)

print("x(D) as a polynomial in D (degree check):", x_poly.degree(), "(must be 3)")
assert x_poly.degree() == 3

c3 = sp.simplify(x_poly.coeff_monomial(D**3))
c2 = sp.simplify(x_poly.coeff_monomial(D**2))
c1 = sp.simplify(x_poly.coeff_monomial(D**1))
c0 = sp.simplify(x_poly.coeff_monomial(D**0))

print("\nc3 =", c3)
print("c2 =", c2)
print("c1 =", c1)
print("c0 =", c0)

print()
print("=" * 78)
print("PART D: cross-check against hand-derived formulas (independent route)")
print("=" * 78)

# tau'(m), tau''(m) via direct differentiation of tau_closed, then hand
# assembly of c0..c3 from delta(D) = a*D - D^2/(2n) - D/(2n) [a=k(1-gamma)/n]
# plus tau(M)/2 = tau(gk)/2 + tau'(gk)/2 D + tau''(gk)/4 D^2 + (1/(6n^2)) D^3
# (tau is exactly cubic, so this Taylor expansion in D is itself EXACT, no
# remainder term -- tau'''= 2/n^2 constant).
tau_p = sp.diff(tau_closed, m)
tau_pp = sp.diff(tau_closed, m, 2)
a = k * (1 - gamma) / n

c0_hand = sp.simplify(tau_closed.subs(m, gamma * k) / 2)
c1_hand = sp.simplify(a - sp.Rational(1, 2) / n + tau_p.subs(m, gamma * k) / 2)
c2_hand = sp.simplify(-sp.Rational(1, 2) / n + tau_pp.subs(m, gamma * k) / 4)
c3_hand = sp.Rational(1, 6) / n**2

print("c0 - c0_hand =", sp.simplify(c0 - c0_hand))
print("c1 - c1_hand =", sp.simplify(c1 - c1_hand))
print("c2 - c2_hand =", sp.simplify(c2 - c2_hand))
print("c3 - c3_hand =", sp.simplify(c3 - c3_hand))
for lhs, rhs, name in [(c0, c0_hand, "c0"), (c1, c1_hand, "c1"),
                        (c2, c2_hand, "c2"), (c3, c3_hand, "c3")]:
    assert sp.simplify(lhs - rhs) == 0, f"{name} mismatch"
print("PASS: two independent derivation routes (Poly-extraction vs. exact")
print("Taylor-in-D of the cubic tau) agree exactly on all four coefficients.")

print()
print("=" * 78)
print("PART E: gamma = 1 degenerate-case consistency check")
print("=" * 78)
print("At gamma=1, M=k a.s. (D=0 a.s.), so only c0 matters: x(0) = c0 must")
print("equal tau(k)/2 exactly (independent of c1,c2,c3, which multiply D=0).")
c0_at_1 = sp.simplify(c0.subs(gamma, 1))
tau_k_half = sp.simplify(tau_closed.subs(m, k) / 2)
print("c0(gamma=1)   =", c0_at_1)
print("tau(k)/2      =", tau_k_half)
print("difference    =", sp.simplify(c0_at_1 - tau_k_half))
assert sp.simplify(c0_at_1 - tau_k_half) == 0
print("PASS.")

print()
print("=" * 78)
print("SUMMARY: x(D) = c0 + c1*D + c2*D^2 + c3*D^3, EXACT (no approximation,")
print("no truncation range restriction), with:")
print("  c0 = tau(gamma*k)/2")
print("  c1 = k(1-gamma)/n - 1/(2n) + [tau'(gamma*k)]/2")
print("  c2 = -1/(2n) + [tau''(gamma*k)]/4")
print("  c3 = 1/(6n^2)")
print("This is the object whose degree-2 Taylor remainder (in x, equivalently")
print("degree-3-in-D Taylor-Lagrange) Gap 1 needs a summable-over-k bound on.")
print("=" * 78)
