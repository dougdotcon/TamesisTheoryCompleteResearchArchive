"""
Independent referee check #6:
 - re-derive Estagio 37's own threshold-formula structure from its
   ATTEMPT.md prose: C0_Bernstein(gamma,a)^2 = (2+a)*sigma^2(gamma)*(lambdahat(gamma)+1/2)
   with sigma^2(gamma)=gamma(1-gamma), lambdahat(gamma)=16(7/4-gamma)/beta(gamma),
   beta(gamma)=gamma(2-gamma)/2.
 - combine with THIS front's lambda_tight(gamma) in place of lambdahat(gamma):
   C0_tight_Bernstein(gamma,a)^2 := (2+a)*sigma^2(gamma)*(lambda_tight(gamma)+1/2)
 - verify: on [gamma*,1) (lambda_tight=4): C0^2 = 9/2*(2+a)*gamma*(1-gamma),
   vertex at gamma=1/2 giving 9a/8+9/4
 - verify: on (0,gamma*): lim_{gamma->0+} C0_tight_Bernstein^2 = 2a+4 (exact, sympy.limit)
 - verify: sup_gamma C0_tight_Bernstein^2 = max(9a/8+9/4, 2a+4) = 2a+4 for every a>0
 - compare against Estagio 37's own sup_gamma C0_Bernstein(gamma,a)^2 = 28a+56
   -- confirm 28a+56 = 14*(2a+4) EXACTLY (symbolic identity, not just numeric).
"""
import sympy as sp

gamma, a = sp.symbols('gamma a', positive=True)

# --- Re-derive Estagio 37's own C0_Bernstein(gamma,a)^2 structure from its
# cited definitions (beta, lambdahat), as prose-quoted in the sharper_tail
# ATTEMPT.md ("hatlambda(gamma):=16(7/4-gamma)/beta(gamma)")
beta = gamma*(2-gamma)/2
lambdahat = 16*(sp.Rational(7,4)-gamma)/beta
sigma2 = gamma*(1-gamma)

C0_Bernstein_old_sq = (2+a)*sigma2*(lambdahat + sp.Rational(1,2))
C0_Bernstein_old_sq = sp.simplify(C0_Bernstein_old_sq)
print("Re-derived C0_Bernstein(gamma,a)^2 (Estagio 37 structure) =")
sp.pprint(C0_Bernstein_old_sq)

sup_old = sp.limit(C0_Bernstein_old_sq, gamma, 0, dir='+')
print("\nlim_{gamma->0+} C0_Bernstein_old^2 =", sp.simplify(sup_old), "  (Estagio 37 claims sup=28a+56)")
print("Matches 28a+56 exactly?", sp.simplify(sup_old - (28*a+56)) == 0)

# --- This front's lambda_tight(gamma) ---
lambda_tight_pieceA = sp.Integer(4)                      # gamma >= gamma*
lambda_tight_pieceB = 4*(1-gamma)**2/(gamma*(2-gamma))    # gamma < gamma*

C0_tight_A = sp.simplify((2+a)*sigma2*(lambda_tight_pieceA + sp.Rational(1,2)))
C0_tight_B = sp.simplify((2+a)*sigma2*(lambda_tight_pieceB + sp.Rational(1,2)))

print("\nC0_tight_Bernstein^2 on [gamma*,1) (lambda_tight=4):")
sp.pprint(C0_tight_A)
target_A = sp.Rational(9,2)*(2+a)*gamma*(1-gamma)
print("Matches 9/2*(2+a)*gamma*(1-gamma)?", sp.simplify(C0_tight_A - target_A) == 0)

# vertex at gamma=1/2
vertex_val = sp.simplify(C0_tight_A.subs(gamma, sp.Rational(1,2)))
print("Vertex value at gamma=1/2:", vertex_val, " (target claims 9a/8+9/4)")
print("Matches 9a/8+9/4 exactly?", sp.simplify(vertex_val - (sp.Rational(9,8)*a + sp.Rational(9,4))) == 0)
# confirm it IS the vertex (max) of the downward parabola on [0,1]
dA = sp.diff(C0_tight_A, gamma)
crit = sp.solve(sp.Eq(dA, 0), gamma)
print("Critical point(s) of C0_tight_A in gamma:", crit)

print("\nC0_tight_Bernstein^2 on (0,gamma*) (lambda_tight piece B):")
sp.pprint(sp.simplify(C0_tight_B))

lim_B0 = sp.limit(C0_tight_B, gamma, 0, dir='+')
print("\nlim_{gamma->0+} C0_tight_Bernstein_pieceB^2 =", sp.simplify(lim_B0), "  (target claims 2a+4)")
print("Matches 2a+4 exactly?", sp.simplify(lim_B0 - (2*a+4)) == 0)

# sup = max(9a/8+9/4, 2a+4) = 2a+4 for a>0
diff_sup = sp.simplify((2*a+4) - (sp.Rational(9,8)*a + sp.Rational(9,4)))
print("\n(2a+4) - (9a/8+9/4) =", diff_sup, "  (should be 7a/8+7/4, hence >0 for all a>-2, in particular a>0)")

# Flagship 14x ratio, exact algebraic identity for ALL a (not just a=0.05)
print("\n--- Flagship 14x check (exact algebraic identity for ALL a) ---")
ratio_identity = sp.simplify((28*a+56) - 14*(2*a+4))
print("(28a+56) - 14*(2a+4) =", ratio_identity, " (should be identically 0)")
print("Symbolic ratio (28a+56)/(2a+4) simplified:", sp.simplify((28*a+56)/(2*a+4)))

# Numeric spot check at a=0.05 as used in both fronts
a_val = sp.Rational(5,100)
print(f"\nAt a=0.05: old sup = {sp.N(sup_old.subs(a,a_val))}, new sup = {sp.N((2*a_val+4))}, "
      f"ratio = {sp.N(sup_old.subs(a,a_val)/(2*a_val+4))}")
