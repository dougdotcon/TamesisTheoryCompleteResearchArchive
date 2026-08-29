#!/usr/bin/env python3
"""
s01_new_identities_symbolic.py -- BOUNDARY-LAYER-SELFHEAL-ATTEMPT
(wave 30, front c, DISC-DEC-138)

Fresh, from-scratch sympy verification of every symbolic identity this
front's new proof of E_full = O(1/z^3) under (C') ALONE (no (C'')) relies
on. Nothing here is imported from any ancestor's or referee's script --
every derivation below is written independently from the mathematical
content of the cited background (R'=zR-1, R(z):=int_0^inf e^{-u^2/2-uz}du,
K(y,t) closed-form decomposition of h1_translation_structure_attempt /
h_ces_direct_attempt / cu_direct_proof_attempt, all read in full before
writing this script).

Five independent checks:
  Part 1: R''(z) = (1+z^2)R(z) - z   (closed form for R'', from R'=zR-1)
  Part 2: Q_u(z) := int_u^inf e^{-w^2/2-wz} dw  satisfies
          d/du Q_u(z) = -e^{-u^2/2-uz}   (trivial FTC, symbolic check)
          AND matches the alternate closed form e^{-u^2/2-uz}*R(u+z)
          (two representations of the SAME object, cross-checked)
  Part 3: the Fubini/order-swap identity
          int_0^inf u * [int_u^inf g(w)dw] du = int_0^inf g(w)*w^2/2 dw
          verified on a concrete g (not the abstract Q_u itself, to keep
          this a genuinely independent sanity check of the SWAP TECHNIQUE)
  Part 4: the elementary IBP/FTC identity
          int_0^h e^{-h'/eps} phi'(h') dh'
            = e^{-h/eps} phi(h) - phi(0) + (1/eps) int_0^h e^{-h'/eps} phi(h') dh'
          verified on a concrete non-trivial phi (matches wave-25's own
          concrete-test-function verification style, written fresh here)
  Part 5: R''(z) <= 2/z^3 for z>0, via the elementary substitution
          w=s/z, e^{-s^2/(2z^2)}<=1 -- a SIMPLER, self-contained bound,
          independent of the predecessor's integrating-factor Gordon-type
          machinery (not re-derived here since it is already an
          established, independently-referee-verified fact of record;
          this script derives its OWN, elementary alternative route to
          the one specific bound this front's new proof actually needs).
"""
import sympy as sp

print("=" * 78)
print("PART 1: R''(z) = (1+z^2)R(z) - z, from R'=zR-1")
print("=" * 78)

z = sp.symbols('z', positive=True)
R = sp.Function('R')

# R'(z) = z*R(z) - 1  is the defining ODE (cited background fact of
# record, re-derivable from R(z):=int_0^inf e^{-u^2/2-uz}du by
# differentiating under the integral sign and one integration by parts --
# NOT re-derived here since this ODE itself is already an established,
# independently-verified fact of record throughout this entire 10-wave
# sub-lineage; this script's job is the NEW identities built on top of it).
ode_rhs = z * R(z) - 1
Rprime = sp.diff(R(z), z)

# Differentiate the ODE itself w.r.t. z to get R'' in terms of R, R':
#   R''(z) = R(z) + z*R'(z)
Rpp_raw = sp.diff(ode_rhs, z)
print(f"d/dz[z*R(z)-1] = {Rpp_raw}")

# substitute R'(z) -> z*R(z)-1 (the ODE itself) to eliminate R', leaving
# R'' purely in terms of R(z) and z:
Rpp_closed = Rpp_raw.subs(sp.Derivative(R(z), z), ode_rhs)
Rpp_closed = sp.expand(Rpp_closed)
print(f"substituting R'(z)=z*R(z)-1: R''(z) = {Rpp_closed}")

target = (1 + z**2) * R(z) - z
diff1 = sp.simplify(Rpp_closed - target)
print(f"claimed closed form: R''(z) = (1+z^2)*R(z) - z")
print(f"residual (Rpp_closed - claimed): {diff1}")
assert diff1 == 0, "Part 1 FAILED: R'' closed-form identity does not hold"
print("Part 1: PASS (R''(z) = (1+z^2)*R(z) - z, exact symbolic identity)")

print()
print("=" * 78)
print("PART 2: Q_u(z) := int_u^inf e^{-w^2/2-wz} dw satisfies")
print("        d/du Q_u(z) = -e^{-u^2/2-uz}, and matches e^{-u^2/2-uz}*R(u+z)")
print("=" * 78)

u, w = sp.symbols('u w', positive=True)

# Route 1: define Q_u(z) directly as the tail integral and differentiate
# w.r.t. u via the Leibniz rule (fundamental theorem of calculus for the
# lower limit of an integral) -- purely symbolic, no assumption about R.
g = sp.exp(-w**2 / 2 - w * z)
# d/du [int_u^inf g(w) dw] = -g(u)   (Leibniz / FTC, upper limit fixed at
# +infinity contributes 0 since it does not depend on u)
dQdu_route1 = -g.subs(w, u)
print(f"Route 1 (direct FTC on the tail integral): d/du Q_u(z) = {dQdu_route1}")

# Route 2: use the ALTERNATE closed form Q_u(z) = e^{-u^2/2-uz} * R(u+z)
# (an object this front's own s01 derivation Step 1 introduces, re-derived
# fresh here symbolically using ONLY the defining ODE R'(zeta)=zeta*R(zeta)-1,
# now evaluated at zeta=u+z) and differentiate via the product rule,
# supplying d/du[R(u+z)] = R'(u+z) = (u+z)*R(u+z)-1 EXPLICITLY (the ODE),
# rather than letting sympy's own chain-rule machinery differentiate
# R(u+z) symbolically (which produces an opaque Subs(...) wrapper object
# that cannot be pattern-matched against directly -- avoided here by
# building the product rule by hand, term by term, which is mathematically
# equivalent and fully transparent).
expo = sp.exp(-u**2 / 2 - u * z)
dexpo_du = sp.diff(expo, u)
Rprime_at_uz = (u + z) * R(u + z) - 1   # the ODE, evaluated at zeta=u+z
dQdu_route2 = sp.expand(dexpo_du * R(u + z) + expo * Rprime_at_uz)
print(f"Route 2 (product rule, R'(u+z) supplied via the ODE by hand):")
print(f"  d/du Q_u(z) = {dQdu_route2}")

diff2 = sp.simplify(dQdu_route2 - dQdu_route1)
print(f"residual (Route2 - Route1): {diff2}")
assert diff2 == 0, "Part 2 FAILED: the two representations of Q_u(z) disagree"
print("Part 2: PASS -- both representations of Q_u(z) give the SAME")
print("  derivative -e^{-u^2/2-uz}; confirms Q_u(z)=int_u^inf e^{-w^2/2-wz}dw")
print("  = e^{-u^2/2-uz}*R(u+z) are the SAME function (up to a constant,")
print("  pinned by matching value at u->infinity, both ->0).")

print()
print("=" * 78)
print("PART 3: Fubini/order-swap identity")
print("  int_0^inf u*[int_u^inf g(w)dw] du = int_0^inf g(w)*w^2/2 dw")
print("  (verified on a CONCRETE g, independent sanity check of the SWAP")
print("   TECHNIQUE this front's Step 5 applies to g(w)=e^{-w^2/2-wz})")
print("=" * 78)

# concrete test: g(w) = exp(-w)  (simple, both sides have closed forms)
g_test = sp.exp(-w)
inner = sp.integrate(g_test, (w, u, sp.oo))
print(f"g(w) = exp(-w);  int_u^inf g(w)dw = {inner}")
lhs = sp.integrate(u * inner, (u, 0, sp.oo))
rhs = sp.integrate(g_test * w**2 / 2, (w, 0, sp.oo))
print(f"LHS = int_0^inf u*(int_u^inf g dw) du = {lhs}")
print(f"RHS = int_0^inf g(w)*w^2/2 dw          = {rhs}")
diff3 = sp.simplify(lhs - rhs)
print(f"residual: {diff3}")
assert diff3 == 0, "Part 3 FAILED: order-swap identity does not hold on test g"

# second concrete test, a different decay profile, to guard against a
# coincidence special to exp(-w):
g_test2 = w * sp.exp(-w**2)
inner2 = sp.integrate(g_test2, (w, u, sp.oo))
lhs2 = sp.integrate(u * inner2, (u, 0, sp.oo))
rhs2 = sp.integrate(g_test2 * w**2 / 2, (w, 0, sp.oo))
diff3b = sp.simplify(lhs2 - rhs2)
print(f"second test g(w)=w*exp(-w^2): LHS={lhs2}, RHS={rhs2}, residual={diff3b}")
assert diff3b == 0, "Part 3 FAILED on second test function"
print("Part 3: PASS on two independent test functions -- the order-swap")
print("  (Tonelli, both integrands nonnegative) technique is confirmed sound.")

print()
print("=" * 78)
print("PART 4: elementary IBP/FTC identity")
print("  int_0^h e^{-h'/eps} phi'(h') dh'")
print("    = e^{-h/eps}*phi(h) - phi(0) + (1/eps)*int_0^h e^{-h'/eps}phi(h')dh'")
print("  (verified on a concrete non-trivial phi, fresh, own choice of phi)")
print("=" * 78)

hp, h, eps = sp.symbols('hp h eps', positive=True)
# own concrete test function, deliberately DIFFERENT from any ancestor's
# choice (wave 25 used h'^3+sin(h')): pick phi(hp) = hp^2*exp(-hp/3) + cos(hp)
phi = hp**2 * sp.exp(-hp / 3) + sp.cos(hp)
phi_prime = sp.diff(phi, hp)
print(f"phi(hp) = {phi}")
print(f"phi'(hp) = {phi_prime}")

lhs4 = sp.integrate(sp.exp(-hp / eps) * phi_prime, (hp, 0, h))
rhs4 = (sp.exp(-h / eps) * phi.subs(hp, h) - phi.subs(hp, 0)
        + (1 / eps) * sp.integrate(sp.exp(-hp / eps) * phi.subs(hp, hp), (hp, 0, h)))

diff4 = sp.simplify(lhs4 - rhs4)
print(f"residual (LHS - RHS), simplified: {diff4}")
assert diff4 == 0, "Part 4 FAILED: IBP/FTC identity does not hold on test phi"
print("Part 4: PASS -- exact symbolic identity on a fresh concrete phi.")

print()
print("=" * 78)
print("PART 5: R''(z) <= 2/z^3 for all z>0, via an elementary substitution")
print("  (self-contained alternative to the predecessor's Gordon-type")
print("   integrating-factor bound -- independent route to the one bound")
print("   this front's new proof actually needs)")
print("=" * 78)

s, zz = sp.symbols('s z', positive=True)
# R''(z) = int_0^inf w^2 * exp(-w^2/2 - w*z) dw
# substitute w = s/z  =>  dw = ds/z
w_sym = sp.symbols('w', positive=True)
Rpp_integrand = w_sym**2 * sp.exp(-w_sym**2 / 2 - w_sym * zz)
w_sub = s / zz
integrand_sub = Rpp_integrand.subs(w_sym, w_sub) * sp.diff(w_sub, s)
integrand_sub = sp.simplify(integrand_sub)
print(f"after w=s/z substitution, integrand becomes: {integrand_sub}")
# should equal (s^2/z^3) * exp(-s^2/(2z^2)) * exp(-s)
expected_form = (s**2 / zz**3) * sp.exp(-s**2 / (2 * zz**2)) * sp.exp(-s)
diff5 = sp.simplify(integrand_sub - expected_form)
print(f"residual vs expected form (s^2/z^3)*exp(-s^2/(2z^2))*exp(-s): {diff5}")
assert diff5 == 0, "Part 5 FAILED: substitution algebra does not match"

# Since exp(-s^2/(2z^2)) <= 1 for all s,z>0 (trivial, exponent <=0), the
# integrand is bounded above by (s^2/z^3)*exp(-s), whose integral over
# [0,inf) is (1/z^3)*int_0^inf s^2*exp(-s) ds = (1/z^3)*Gamma(3) = 2/z^3.
gamma3 = sp.integrate(s**2 * sp.exp(-s), (s, 0, sp.oo))
print(f"int_0^inf s^2*exp(-s) ds = {gamma3}  (= Gamma(3) = 2!)")
assert gamma3 == 2
print("Part 5: PASS -- R''(z) = (1/z^3)*int_0^inf s^2*exp(-s^2/(2z^2))*exp(-s)ds")
print("  <= (1/z^3)*int_0^inf s^2*exp(-s)ds = 2/z^3, for EVERY z>0, via the")
print("  elementary bound exp(-s^2/(2z^2))<=1 -- no ODE comparison-function")
print("  machinery needed for this specific bound.")

print()
print("=" * 78)
print("ALL 5 PARTS PASSED. Zero discrepancies.")
print("=" * 78)
