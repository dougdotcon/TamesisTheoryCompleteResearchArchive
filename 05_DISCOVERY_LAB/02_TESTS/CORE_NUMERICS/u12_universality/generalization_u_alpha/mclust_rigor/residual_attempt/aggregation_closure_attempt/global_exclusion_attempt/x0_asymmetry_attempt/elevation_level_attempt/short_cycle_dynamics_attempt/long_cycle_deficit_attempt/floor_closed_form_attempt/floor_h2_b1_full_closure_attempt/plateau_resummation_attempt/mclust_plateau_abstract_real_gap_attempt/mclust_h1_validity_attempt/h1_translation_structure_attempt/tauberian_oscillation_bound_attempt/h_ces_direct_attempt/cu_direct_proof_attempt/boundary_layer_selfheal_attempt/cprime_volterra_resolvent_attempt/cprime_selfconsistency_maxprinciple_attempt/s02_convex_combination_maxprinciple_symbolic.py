"""
s02_convex_combination_maxprinciple_symbolic.py

Front: CPRIME-SELFCONSISTENCY-MAXPRINCIPLE-ATTEMPT

Purpose:
  (A) Prove, exactly, that (E2)'s own convolution kernel has total weight
      EXACTLY 1 -- i.e. Phi(x,y) is an exact CONVEX COMBINATION of the
      boundary value 1 and W-values along the characteristic path. This is
      THEOREM 1 (the "maximum principle for Phi", magnitude version) of this
      front's ATTEMPT.md, Sec 2.
  (B) Prove, exactly (via BRIDGE-1/2 confirmed in s01, restated here in
      original (s,g) units for direct legibility against the mandate's own
      W formula), that the coefficient SUM g + (1-s-g) = 1-s <= 1, with BOTH
      individual coefficients nonnegative ONLY when s+g<=1 (the SAFE
      regime); for s+g>1 the (1-s-g) coefficient is negative and the
      "convex combination" structure of W itself (not just of Phi via E2)
      breaks down.
  (C) Demonstrate, via a clean algebraic/fixed-point argument (not
      simulation), that even in the fully SAFE regime, the crude
      "sup-level" maximum principle produces a VACUOUS bound: the map
      T(M):=max(1,(1-s)*M) satisfies T(M)<=M for every M>=1, s in[0,1], so
      iterating never produces a contradiction that could pin down a finite
      value of M -- any candidate bound M_Phi=M, however large, is
      consistent with T(M)<=M. This is the precise, rigorous sense in which
      the naive maximum principle "does not close (B)".
"""
import sympy as sp

print("=" * 70)
print("Part A: (E2)'s convolution weight sums to EXACTLY 1")
print("=" * 70)

y, v, eps = sp.symbols('y v eps', positive=True)

# (E2), cited verbatim (Sec 0.1 of every ancestor, not re-derived):
#   Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv
# Total weight = boundary weight + integral of the kernel weight over v in [0,y]
boundary_weight = sp.exp(-y/eps)
kernel_weight_density = sp.exp(-v/eps) / eps
integral_weight = sp.integrate(kernel_weight_density, (v, 0, y))
total_weight = sp.simplify(boundary_weight + integral_weight)
print("boundary weight e^{-y/eps}                       =", boundary_weight)
print("integral of (1/eps)e^{-v/eps} dv over [0,y]        =", integral_weight)
print("TOTAL weight (boundary + integral)                 =", total_weight)
assert sp.simplify(total_weight - 1) == 0, "Weights do not sum to 1!"
print("CONFIRMED: total weight = 1 EXACTLY, for every y>=0, eps>0.")
print()
print("Since e^{-y/eps} >= 0 and (1/eps)e^{-v/eps} >= 0 pointwise (trivial,")
print("both are exponentials of real arguments), Phi(x,y) is an EXACT CONVEX")
print("COMBINATION (nonnegative weights, summing to exactly 1) of the")
print("constant boundary value 1 and the path-values {W(x+v,y-v): v in[0,y]}.")
print()
print("THEOREM 1 (Phi convex-combination maximum principle), consequence:")
print("  inf_{path} W  <=  Phi(x,y)  <=  max(1, sup_{path} W)")
print("  and more precisely, since the boundary weight contributes '1' with")
print("  its own share: Phi(x,y) <= max(1, sup_{path} W) always; and if")
print("  sup_path W <= 1 then Phi(x,y) <= 1 as well (the '1' does not need")
print("  a separate max() in that sub-case, but max(1,.) is always valid).")

print()
print("=" * 70)
print("Part B: the ORIGINAL W's own coefficient sum, and the sign regime")
print("=" * 70)

s, g = sp.symbols('s g', nonnegative=True)
coeff_avg = g            # coefficient of Avg_g[Phi] in W
coeff_psi = 1 - s - g     # coefficient of Psi in W
coeff_sum = sp.simplify(coeff_avg + coeff_psi)
print("coefficient of Avg_g[Phi]:  g")
print("coefficient of Psi:         (1-s-g)")
print("SUM:                       ", coeff_sum, " = 1-s")
assert sp.simplify(coeff_sum - (1-s)) == 0

print()
print("SAFE regime (s+g<=1): both coefficients >=0 (g>=0 always given; need")
print("  1-s-g>=0 i.e. s+g<=1). Sum = 1-s <= 1 -- a SUB-convex combination")
print("  (weights nonneg, summing to <=1, not exactly 1 unless s=0).")
print()
print("UNSAFE regime (s+g>1): coefficient of Psi, (1-s-g), is NEGATIVE.")
print("  W is then a SIGNED (not convex) combination of Avg_g[Phi] and Psi --")
print("  the maximum-principle argument of Part A cannot be applied to THIS")
print("  decomposition of W itself in this regime (though Part A's Theorem 1")
print("  for Phi remains valid REGARDLESS, since it depends only on E2's own")
print("  kernel weights, not on W's internal sign structure -- the issue is")
print("  specifically that bounding sup W via g*M_Phi+(1-s-g)*M_Psi stops")
print("  being valid once (1-s-g)<0, since then a LARGE negative Psi could")
print("  make W LARGE, not merely bounded by max(M_Phi,M_Psi)).")

print()
print("=" * 70)
print("Part C: the crude sup-level maximum principle is a NON-CONTRACTION")
print("(vacuity of the naive iterated bound, safe regime only, s in [0,1])")
print("=" * 70)

M, s_sym = sp.symbols('M s_sym', positive=True)
# crude bound (safe regime, using Avg_g[Phi]<=M, Psi<=M_Psi<=M via the
# ALREADY-CITED DISC-DEC-100 Sec 8.2 fact M_Psi<=M_Phi, cited not re-derived here):
#   sup W <= (1-s)*M   =>   T(M) := max(1, (1-s)*M)
T_of_M = sp.Piecewise((1, (1-s_sym)*M <= 1), ((1-s_sym)*M, True))
# Show T(M) <= M for all M>=1, s in [0,1]:
diff_TM = sp.simplify((1-s_sym)*M - M)   # = -s_sym*M <= 0 for s_sym,M>=0
print("(1-s)*M - M =", diff_TM, "  (<=0 for all s>=0, M>=0: since s*M>=0)")
print("=> (1-s)*M <= M  for all s in [0,1], M>=0.")
print("=> T(M) = max(1,(1-s)*M) <= max(1,M) = M  for every M>=1 (since M>=1")
print("   already dominates the '1' branch).")
print()
print("CONSEQUENCE: for EVERY candidate value M>=1 (however large), the")
print("inequality 'M_Phi satisfies M_Phi <= T(M_Phi)' one would need for a")
print("genuine maximum-principle CONTRADICTION-based proof of finiteness is")
print("instead ALWAYS SATISFIED AS T(M)<=M (not T(M)>M for large M, which is")
print("what would be needed to rule out large M). The map T is a NON-EXPANSIVE")
print("but NOT a CONTRACTION (its Lipschitz constant in M is exactly (1-s)<=1,")
print("with EQUALITY 1 attained at s=0 -- the single most important slice,")
print("since M_Phi is a GLOBAL sup that must in particular dominate the s=0")
print("slice). This is the precise mechanism, verified here by direct")
print("algebra rather than assumed: no finite bound on M_Phi can be extracted")
print("from the crude sup-level maximum principle alone, even restricted to")
print("the fully SAFE regime s+g<=1 where every coefficient is nonnegative.")

print()
print("Numerical spot check across a small grid (s,M), confirming T(M)<=M")
print("always, with equality approached only as s->0:")
print(f"{'s':>6} {'M':>8} {'(1-s)*M':>10} {'T(M)':>8} {'T(M)<=M?':>10}")
for s_val in [sp.Rational(0), sp.Rational(1,10), sp.Rational(1,2), sp.Rational(9,10)]:
    for M_val in [1, 5, 100, 10**6]:
        val = (1-s_val)*M_val
        Tval = max(1, val)
        ok = Tval <= M_val
        print(f"{float(s_val):6.2f} {M_val:8d} {float(val):10.3f} {float(Tval):8.3f} {str(ok):>10}")

print()
print("ALL CHECKS PASSED. Summary:")
print(" (A) Phi(x,y) is an EXACT convex combination (weights sum to 1) of")
print("     boundary=1 and path-values of W -- THEOREM 1, unconditional,")
print("     follows for free from (E2)'s own definition.")
print(" (B) W's OWN internal decomposition (g, 1-s-g) is only a genuine")
print("     (sub-)convex combination for s+g<=1; the coefficient (1-s-g)")
print("     goes negative for s+g>1, EXACTLY the threshold s01 identified.")
print(" (C) Even restricted to the safe regime, the crude sup-level")
print("     iteration T(M)=max(1,(1-s)*M) is a NON-CONTRACTION (Lipschitz")
print("     constant (1-s)<=1, =1 at s=0) -- it can never certify a finite")
print("     bound on M_Phi by itself. This is proved here directly, not")
print("     merely observed numerically.")
