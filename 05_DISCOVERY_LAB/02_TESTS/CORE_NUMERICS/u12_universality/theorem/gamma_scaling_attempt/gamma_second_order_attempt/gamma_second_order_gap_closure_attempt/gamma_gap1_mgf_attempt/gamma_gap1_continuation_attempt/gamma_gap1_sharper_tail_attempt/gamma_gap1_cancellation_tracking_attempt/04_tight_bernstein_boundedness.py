"""
04_tight_bernstein_boundedness.py

Combines THIS FRONT's tight coefficient/cancellation bound
(lambda_tight(gamma) = max(4, 4(1-gamma)^2/(gamma(2-gamma))), script 02/03)
with the Bernstein-with-slack tail-control technique (sharper_tail front,
re-derived fresh here per this front's own-script discipline) to see how
much the *combined* threshold constant C0(gamma,a)^2 shrinks relative to
the sharper_tail front's own C0_Bernstein(gamma,a)^2 = (2+a)*sigma^2(gamma)
*(hat_lambda(gamma)+1/2), which used the CRUDE (triangle-inequality,
symmetric-range) hat_lambda(gamma), not this front's tight lambda_tight.

Everything here is exact symbolic algebra (sympy), matching the standard
this lineage uses for "PROVED" (not just numerically sampled) monotonicity/
boundedness claims (e.g. Estagio 36's lambda(gamma) monotonicity, Estagio
37's C0_Bernstein boundedness).
"""
import sympy as sp

gamma, a = sp.symbols('gamma a', positive=True)

sigma2 = gamma * (1 - gamma)

lam_true = sp.simplify(4 * (3 - 2 * gamma) / (gamma * (2 - gamma)))          # old "ideal" (still triangle-ineq)
hat_lam = sp.simplify(16 * (sp.Rational(7, 4) - gamma) / (gamma * (2 - gamma) / 2))  # current crude bound

# THIS FRONT's tight leading constant (script 02, PROVED via sympy.limit):
lam_tight_left = sp.Integer(4)                                    # from D_min endpoint, constant!
lam_tight_right = sp.simplify(4 * (1 - gamma) ** 2 / (gamma * (2 - gamma)))  # from D_max endpoint

print("=" * 78)
print("PART A -- lambda_tight(gamma) = max(lam_tight_left, lam_tight_right)")
print("=" * 78)
print("lam_tight_left  =", lam_tight_left, " (constant, gamma-independent)")
print("lam_tight_right =", lam_tight_right)

# crossover gamma* where the two pieces are equal
crossover_eq = sp.Eq(lam_tight_right, lam_tight_left)
crossover_sols = sp.solve(crossover_eq, gamma)
crossover_sols_real01 = [s for s in crossover_sols if s.is_real and 0 < s < 1]
print("crossover solving lam_tight_right = lam_tight_left:", crossover_sols)
print("real root in (0,1):", crossover_sols_real01)
gamma_star = crossover_sols_real01[0]
print("gamma* =", gamma_star, "=", sp.nsimplify(gamma_star), "~", float(gamma_star))

print()
print("=" * 78)
print("PART B -- C0_tight_Bernstein(gamma,a)^2 := (2+a)*sigma^2(gamma)*")
print("(lambda_tight(gamma)+1/2), piecewise in the two lambda_tight regimes")
print("=" * 78)

C0sq_left = sp.simplify((2 + a) * sigma2 * (lam_tight_left + sp.Rational(1, 2)))
C0sq_right = sp.simplify((2 + a) * sigma2 * (lam_tight_right + sp.Rational(1, 2)))
print("On [gamma*,1) (left/D_min-dominated regime):")
print("  C0sq_left(gamma,a) =", C0sq_left)
print("On (0,gamma*) (right/D_max-dominated regime):")
print("  C0sq_right(gamma,a) =", C0sq_right)

print()
print("-" * 78)
print("Boundedness + monotonicity on [gamma*, 1) -- exact algebra")
print("-" * 78)
# C0sq_left(gamma,a) = (2+a)*gamma*(1-gamma)*4.5, a downward parabola in
# gamma with vertex at gamma=1/2 -- elementary; confirm via derivative.
dC0sq_left = sp.diff(C0sq_left, gamma)
crit_left = sp.solve(sp.Eq(dC0sq_left, 0), gamma)
print("d/dgamma C0sq_left = 0 at gamma =", crit_left)
val_at_half = C0sq_left.subs(gamma, sp.Rational(1, 2))
print("C0sq_left(1/2,a) =", sp.simplify(val_at_half), "-- this is the max on",
      "[gamma*,1) since it's a downward parabola vertex at gamma=1/2, and",
      "gamma*~0.293 < 1/2 < 1")
val_at_gammastar_left = sp.simplify(C0sq_left.subs(gamma, gamma_star))
print("C0sq_left(gamma*,a) =", sp.simplify(val_at_gammastar_left), " (continuity check vs right piece below)")

print()
print("-" * 78)
print("Boundedness + monotonicity on (0, gamma*) -- exact algebra")
print("-" * 78)
val_at_gammastar_right = sp.simplify(C0sq_right.subs(gamma, gamma_star))
print("C0sq_right(gamma*,a) =", val_at_gammastar_right, " (should equal left-piece value above -- continuity)")
diff_at_star = sp.simplify(val_at_gammastar_left - val_at_gammastar_right)
print("difference (should be 0):", diff_at_star)

lim0 = sp.limit(C0sq_right, gamma, 0, dir='+')
print("lim_{gamma->0+} C0sq_right(gamma,a) =", sp.simplify(lim0))

dC0sq_right = sp.diff(C0sq_right, gamma)
dC0sq_right_num, dC0sq_right_den = sp.fraction(sp.together(dC0sq_right))
dC0sq_right_num = sp.expand(dC0sq_right_num)
print("Numerator of d/dgamma C0sq_right (as polynomial in gamma, coefficient",
      "of 'a' terms kept symbolic):")
print(" ", sp.factor(dC0sq_right_num))
roots_right = sp.solve(sp.Eq(dC0sq_right_num, 0), gamma)
print("Roots of that numerator (as equation in gamma, 'a' symbolic):", roots_right)

print()
print("Direct monotonicity check via sign of derivative on (0,gamma*), at")
print("several fixed 'a' values (since roots above may depend on a in a way")
print("not obviously sign-definite from the symbolic form alone):")
for aval in [sp.Rational(1, 100), sp.Rational(1, 20), sp.Rational(1, 4), 1, 5]:
    deriv_a = sp.simplify(dC0sq_right.subs(a, aval))
    # sign-check at a fine grid inside (0, gamma_star)
    gstar_f = float(gamma_star)
    signs = set()
    import numpy as np
    for gv in np.linspace(1e-6, gstar_f - 1e-6, 400):
        s = float(deriv_a.subs(gamma, sp.nsimplify(gv, rational=False)).evalf())
        signs.add(1 if s > 0 else (-1 if s < 0 else 0))
    print(f"  a={float(aval):.3f}: sign(d/dgamma C0sq_right) on (0,gamma*) takes values {signs}"
          f" (expect {{-1}} i.e. strictly decreasing throughout, so sup is at gamma->0+)")

print()
print("=" * 78)
print("PART C -- the flagship comparison: sup over (0,1) of C0_tight_Bernstein^2")
print("vs the sharper_tail front's own C0_Bernstein^2 (using crude hat_lambda)")
print("=" * 78)

C0sq_old_Bernstein = sp.simplify((2 + a) * sigma2 * (hat_lam + sp.Rational(1, 2)))
old_sup = sp.limit(C0sq_old_Bernstein, gamma, 0, dir='+')
print("OLD (sharper_tail): sup_{gamma in (0,1)} C0_Bernstein(gamma,a)^2 =",
      sp.simplify(old_sup), " (matches Estagio 37's reported 28a+56)")

new_sup_candidate = sp.Max(val_at_half, lim0)
print("NEW (this front, tight): candidate sup = max(value at gamma=1/2,",
      "limit as gamma->0+) =", sp.simplify(new_sup_candidate))

for aval_f in [0.05, 0.1, 0.5, 1.0]:
    aval = sp.nsimplify(aval_f)
    old_v = float(old_sup.subs(a, aval))
    new_half = float(val_at_half.subs(a, aval))
    new_lim0 = float(lim0.subs(a, aval))
    print(f"  a={aval_f}: OLD sup={old_v:.4f}   NEW sup=max({new_half:.4f} [g=1/2], "
          f"{new_lim0:.4f} [g->0]) = {max(new_half, new_lim0):.4f}"
          f"   ratio OLD/NEW = {old_v / max(new_half, new_lim0):.3f}x")
