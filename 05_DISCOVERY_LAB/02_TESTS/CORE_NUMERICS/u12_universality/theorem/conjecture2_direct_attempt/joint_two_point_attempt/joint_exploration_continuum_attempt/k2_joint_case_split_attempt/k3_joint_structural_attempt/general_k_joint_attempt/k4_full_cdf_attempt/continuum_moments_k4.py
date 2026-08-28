"""
K4-FULL-CDF-ATTEMPT: elementary continuum-moment cross-check targets for
K=4, derived directly (simple calculus, no new theorem) from the CITED
general-K continuum density f_{M_K}(x) = 2*K*x*(1-x^2)^(K-1), Estagio 24,
THEOREM.md (PROVED for every K>=1, conditional only to the single
classical PD(1) citation already accepted throughout this archive's
K=1..4 line since Estagio 3 -- treated as PROVED per this archive's own
convention).

This script:
  1. Symbolically integrates f_{M_K}(x) for general K to confirm the
     closed elementary-product formulas used as citation targets in
     ATTEMPT.md Sections 6.2-6.3 (phi_K, E[M_K^2], E[M_K^3]).
  2. Specializes to K=4: phi_4, E[M_4^2], E[M_4^3].
  3. Self-consistency: reproduces the ALREADY-CITED values phi_4=128/315
     (Estagio 4/24), E[M_K^2]=1/(K+1) for every K (Estagio 24), and
     E[M_5^3]=256/3003 (Estagio 24, explicitly stated there as a K=5
     instance) -- confirming this script's own general-moment formula is
     consistent with THEOREM.md's own text, not merely internally
     self-consistent.
"""
import sympy as sp

x, K = sp.symbols('x K', positive=True, integer=True)
Kc = sp.Symbol('K', positive=True)  # for symbolic-K integration (real K)

f = 2 * Kc * x * (1 - x**2)**(Kc - 1)

print("Continuum density (CITED, Estagio 24, general K):")
print("  f_{M_K}(x) =", f)
print()

for m in (1, 2, 3):
    Emom = sp.integrate(x**m * f, (x, 0, 1))
    Emom = sp.simplify(Emom)
    print(f"E[M_K^{m}] (general K, symbolic) = {Emom}")

print()
print("=" * 78)
print("Specializing to K=4:")
print("=" * 78)
f4 = f.subs(Kc, 4)
f4 = sp.expand(f4)
print("f_{M_4}(x) = 8x(1-x^2)^3 =", f4)
phi4 = sp.integrate(x * f4, (x, 0, 1))
EM4_2 = sp.integrate(x**2 * f4, (x, 0, 1))
EM4_3 = sp.integrate(x**3 * f4, (x, 0, 1))
print("phi_4      = E[M_4]   =", phi4, "  (cited target: 128/315, Estagio 4/24)")
print("E[M_4^2]            =", EM4_2, "  (cited target: 1/5 = 1/(K+1), Estagio 24)")
print("E[M_4^3]            =", EM4_3, "  (NOT separately stated in THEOREM.md for K=4;")
print("                                  derived here directly from the cited density)")

assert phi4 == sp.Rational(128, 315)
assert EM4_2 == sp.Rational(1, 5)
assert EM4_3 == sp.Rational(128, 1155)
print()
print("All three match the expected/derived targets exactly.")

print()
print("=" * 78)
print("Self-consistency cross-check: does this script's own K=5 value")
print("match THEOREM.md Estagio 24's explicitly-stated E[M_5^3]=256/3003?")
print("=" * 78)
f5 = f.subs(Kc, 5)
EM5_3 = sp.integrate(x**3 * f5, (x, 0, 1))
print("E[M_5^3] =", EM5_3, "  (cited: 256/3003, Estagio 24)")
assert EM5_3 == sp.Rational(256, 3003)
print("MATCH -- confirms this script's elementary-integration route against")
print("an independently-stated value already on record in THEOREM.md.")
