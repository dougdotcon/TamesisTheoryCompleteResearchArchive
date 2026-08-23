"""
Exact symbolic derivation of f_{M_2}(x) for the K=2 whole-space model,
generalizing THEOREM.md Section 5.3's K=1 computation.

All steps exact (sympy.Rational / symbolic), no floating point.
"""
import sympy as sp

x, m1, m2, ell, a, l1, l2, w = sp.symbols('x m1 m2 ell a l1 l2 w', positive=True)

print("="*70)
print("STEP A: joint density of (m1,m2) -- claimed uniform(2) on triangle T")
print("="*70)

# --- Case I: same background block ---
# L ~ Unif(0,1), A | L=ell ~ Unif(0,ell) [forward arc-distance x1->x2]
# m1 = L - A, m2 = A
# Joint (L,A) density on 0<a<ell<1: f_L(ell)*f_{A|L}(a) = 1 * (1/ell)
# BUT this is the density GIVEN Same=1 which already happened with
# probability ell -- so the correct joint (unconditional) density of
# (L,A,Same=1) is f_L(ell) * P(Same=1|ell) * f_{A|Same=1,ell}(a)
#                = 1        * ell           * (1/ell)              = 1
f_L_A_same1 = sp.Integer(1)  # constant, on 0<a<ell<1
print("f_(L,A)(ell,a) restricted to Same=1, i.e. P(L in dell,Same=1,A in da) density:")
print(" =", f_L_A_same1, " on {0<a<ell<1}")

# change of variables (ell,a) -> (m1,m2) = (ell-a, a); Jacobian = 1
Jac1 = sp.Matrix([[sp.diff(ell, m1), sp.diff(ell, m2)],
                   [sp.diff(a, m1), sp.diff(a, m2)]])
# do it directly: ell = m1+m2, a = m2
ell_expr = m1 + m2
a_expr = m2
J = sp.Matrix([[sp.diff(ell_expr, m1), sp.diff(ell_expr, m2)],
               [sp.diff(a_expr, m1), sp.diff(a_expr, m2)]])
detJ = sp.simplify(J.det())
print("Jacobian det d(ell,a)/d(m1,m2) =", detJ)
f_I = sp.simplify(f_L_A_same1 * sp.Abs(detJ))
print("=> f_I(m1,m2) [Case I, same-block contribution to joint density] =", f_I)

# --- Case II: different background blocks ---
# L1 ~ Unif(0,1) = m1. Given L1=ell, P(Same=0|ell)=1-ell, and (by the
# residual/stick-breaking property) L2/(1-ell) ~ Unif(0,1) independent
# of ell, i.e. L2 = (1-ell)*w, w~Unif(0,1).
# Joint (L1,Same=0,L2) density:
#   f_{L1}(ell) * P(Same=0|ell) * f_{L2|Same=0,ell}(m2)
# f_{L2|Same=0,ell}(m2) = 1/(1-ell) for 0<m2<1-ell  [density of (1-ell)*w]
f_L1_L2_same0 = sp.Integer(1) * (1 - ell) * (1 / (1 - ell))
f_L1_L2_same0 = sp.simplify(f_L1_L2_same0)
print("\nf_(L1,L2)(ell,m2) restricted to Same=0, density:")
print(" =", f_L1_L2_same0, " on {0<ell<1, 0<m2<1-ell}")
# here m1 = ell directly (Jacobian 1)
f_II = f_L1_L2_same0.subs(ell, m1)
print("=> f_II(m1,m2) [Case II, different-block contribution] =", f_II)

f_total = sp.simplify(f_I + f_II)
print("\nTOTAL joint density f_(m1,m2)(m1,m2) = f_I + f_II =", f_total)
print("Claimed: constant 2 on triangle T={m1>0,m2>0,m1+m2<1}. Match:",
      sp.simplify(f_total - 2) == 0)

# sanity: total probability check
T_area_check = sp.integrate(sp.integrate(f_total, (m2, 0, 1 - m1)), (m1, 0, 1))
print("Total mass check (should be 1):", T_area_check)

# sanity: P(Same=1) should be 1/2 = integral of f_I over T
P_same1 = sp.integrate(sp.integrate(f_I, (m2, 0, 1 - m1)), (m1, 0, 1))
print("P(Same=1) = integral of f_I over T (should be 1/2):", P_same1)
P_same0 = sp.integrate(sp.integrate(f_II, (m2, 0, 1 - m1)), (m1, 0, 1))
print("P(Same=0) = integral of f_II over T (should be 1/2):", P_same0)

print()
print("="*70)
print("STEP B/C: assembling f_{M_2}(x) via the 4-group decomposition")
print("="*70)

# Given (m1,m2), the four groups:
# A: M2 = 1 - D1 - D2, D1~U(0,m1), D2~U(0,m2) indep; prob 2*m1*m2
# B: M2 = 1 - m2 - D1, D1~U(0,m1); prob m1*(1-m2)
# C: M2 = 1 - m1 - D2, D2~U(0,m2); prob m2*(1-m1)
# D: M2 = 1 - m1 - m2 deterministic; prob 1-m1-m2
#
# We want f_{M2}(x) = d/dx P(M2<=x)
#       = integral over T of 2 * [ P(A)*f_{A}(x|m1,m2)
#                                  + P(B)*f_{B}(x|m1,m2)
#                                  + P(C)*f_{C}(x|m1,m2)
#                                  + P(D)*delta_{1-m1-m2}(x) ] dm1 dm2
#
# We'll instead build the CDF P(M2<=x) directly (safer than densities of
# sums with deltas), then differentiate at the end. This avoids handling
# Dirac deltas symbolically.

# --- Group A: M2 = 1 - D1 - D2, D1~U(0,m1) indep D2~U(0,m2) ---
# P(M2 <= x | A, m1,m2) = P(D1+D2 >= 1-x)
# D1+D2 has a distribution on [0,m1+m2]; compute P(D1+D2>=t) exactly via
# convolution of two uniforms (trapezoid distribution), t = 1-x.
d1, d2, t = sp.symbols('d1 d2 t', positive=True)


def prob_sum_uniforms_ge(t_val, mm1, mm2):
    """P(D1+D2 >= t_val) for D1~U(0,mm1), D2~U(0,mm2) indep, exact piecewise
    via direct double integral (valid symbolically for mm1,mm2>0)."""
    # joint density 1/(mm1*mm2) on box [0,mm1]x[0,mm2]
    # We integrate over the box region where d1+d2>=t_val.
    expr = sp.integrate(
        sp.integrate(1 / (mm1 * mm2), (d2, sp.Max(0, t_val - d1), mm2)),
        (d1, 0, mm1)
    )
    return expr


# We will instead directly get the CDF contribution to P(M2<=x) from group
# A by integrating over the whole triangle T the (m1,m2)-conditional
# probability P(D1+D2 >= 1-x), weighted by 2*(2 m1 m2) [group prob * step-A
# density], but only where 1-x <= m1+m2 (else probability is 0 since
# D1+D2 <= m1+m2 always) -- sympy's piecewise/Max will need care, so we
# split the (m1,m2,x) integration manually using known convolution CDF.

print("Computing Group A's contribution to P(M2<=x) ... (symbolic, exact)")

# Closed form: P(D1+D2 <= s) for D1~U(0,m1),D2~U(0,m2), s in [0,m1+m2]:
# standard trapezoidal (Irwin-Hall generalization). We just need
# P(D1+D2 >= t) = 1 - P(D1+D2<=t).
# Use sympy's stats module for a clean, independently-checkable route.
from sympy.stats import Uniform, density, P as PROB, E as EXPECT
from sympy import Symbol

# We'll do the whole thing by hand-integration rather than sympy.stats
# (sympy.stats symbolic CDF of a sum can be slow/fragile); use direct
# case-split polynomial formula for P(D1+D2<=s), D1~U(0,a),D2~U(0,b),
# standard result:
#   for 0<=s<=min(a,b):      s^2/(2ab)
#   for min(a,b)<=s<=max(a,b): (2s - min(a,b))/(2*max(a,b))   [linear]
#      -- actually let's not hardcode; verify via direct integration
#         below instead, case by case with sympy doing the algebra.

s = sp.symbols('s', positive=True)


def cdf_sum_uniforms(s_val, aa, bb):
    """Exact P(D1+D2<=s_val), D1~U(0,aa), D2~U(0,bb), via direct
    integration, valid (piecewise) for s_val in [0,aa+bb]. Returns a
    sympy Piecewise in s_val given symbolic aa,bb (assumed aa<=bb WLOG by
    caller, or handled generally)."""
    d1_, d2_ = sp.symbols('d1_ d2_', positive=True)
    # integral over region d1 in [0,aa], d2 in [0,bb], d1+d2<=s_val
    # = integral_{d1=0}^{min(aa,s_val)} min(bb, s_val-d1) - 0  d d1 (when >=0)
    expr = sp.integrate(
        sp.Min(bb, sp.Max(0, s_val - d1_)),
        (d1_, 0, sp.Min(aa, s_val))
    ) / (aa * bb)
    return sp.simplify(expr)


# quick numeric sanity of cdf_sum_uniforms before using it symbolically
import random
random.seed(0)
for _ in range(5):
    aa_n = sp.Rational(random.randint(1, 9), 10)
    bb_n = sp.Rational(random.randint(1, 9), 10)
    s_n = sp.Rational(random.randint(0, 20), 20) * (aa_n + bb_n)
    val = cdf_sum_uniforms(s_n, aa_n, bb_n)
    # brute force via Monte-Carlo-free numeric double integral check
    import scipy.integrate as si
    fA, fB = float(aa_n), float(bb_n)
    fS = float(s_n)
    numeric, _ = si.dblquad(lambda d2v, d1v: 1.0 / (fA * fB),
                             0, fA,
                             lambda d1v: 0, lambda d1v: max(0.0, min(fB, fS - d1v)))
    print(f"  check aa={aa_n},bb={bb_n},s={s_n}: symbolic={float(val):.6f} numeric={numeric:.6f}")

print("cdf_sum_uniforms sanity checks done (see values above).")
