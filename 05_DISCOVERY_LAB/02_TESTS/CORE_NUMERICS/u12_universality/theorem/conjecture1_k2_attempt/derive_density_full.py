"""
Full exact symbolic derivation of f_{M_2}(x), K=2 whole-space model.
Generalizes THEOREM.md Sec 5.3 (K=1). All arithmetic exact (sympy.Rational
/ symbolic integration), no floating point except final numeric display.

Method: for each of the 4 groups (A,B,C,D), build the JOINT density of
(m1, m2, and whatever internal uniforms determine M2) directly on its
natural domain, then marginalize step by step (never invoking a Dirac
delta) to reach f_group(x). Sum the four. Compare to 4x(1-x^2).
"""
import sympy as sp

x, m1, m2, d1, d2, sigma, ell = sp.symbols('x m1 m2 d1 d2 sigma ell', positive=True)

print("="*70)
print("GROUP D: M2 = 1-m1-m2 deterministic given (m1,m2); prob(D|m1,m2)=1-m1-m2")
print("Step-A density of (m1,m2) is 2 on T={m1,m2>0,m1+m2<1}.")
print("="*70)

# joint 'mass' over (m1,m2) restricted to group D: 2*(1-m1-m2)
weight_D = 2*(1 - m1 - m2)
# marginal density of L=m1+m2 under this weight: integrate over m2 in (0,ell) with m1=ell-m2
L_marginal_weighted = sp.integrate(weight_D.subs(m1, ell - m2), (m2, 0, ell))
L_marginal_weighted = sp.simplify(L_marginal_weighted)
print("weighted marginal density of L=m1+m2 (group D mass at each ell):", L_marginal_weighted)
# M2 = 1-L => density in x: f_D(x) = [above](ell=1-x) * |d ell/dx|=1
f_D = sp.simplify(L_marginal_weighted.subs(ell, 1 - x))
print("=> f_D(x) =", f_D)
massD = sp.integrate(f_D, (x, 0, 1))
print("total probability mass of Group D (sanity, direct):", sp.simplify(massD))
# cross check directly via double integral
massD_direct = sp.integrate(sp.integrate(weight_D, (m2, 0, 1 - m1)), (m1, 0, 1))
print("total probability mass of Group D (direct double integral):", sp.simplify(massD_direct))

print()
print("="*70)
print("GROUP B: M2 = 1-m2-D1, D1~U(0,m1); prob(B|m1,m2)=m1(1-m2)")
print("="*70)
# joint density over (m1,m2,d1): 2 [step A] * m1(1-m2) [P(B)] * (1/m1) [density of D1|m1]
#   = 2(1-m2), on 0<d1<m1, m1,m2>0, m1+m2<1
joint_B = 2*(1 - m2)
print("joint density of (m1,m2,d1) restricted to group B (indep of d1!) =", joint_B,
      " on {0<d1<m1, (m1,m2) in T}")
# M2 = 1-m2-d1. Fix x; want density of M2 at x by integrating out (m1,m2,d1)
# subject to 1-m2-d1 = x, i.e. d1 = 1-m2-x, with constraints 0<d1<m1<1-m2.
# So for fixed m2 (with 0<m2<1-x, ensuring d1=1-m2-x>0), integrate over m1
# in (d1, 1-m2) i.e. m1 in (1-m2-x, 1-m2) [range length x], contributing a
# factor of "1" per unit m1 times |d(m2)/d(m2)| -- since we already used up
# the d1 degree of freedom to pin down x, we get, for each valid m2, an
# integral over m1 of length x of the constant integrand joint_B (which is
# indep of d1,m1):
m1_range_len = x  # (1-m2) - (1-m2-x) = x, always, as derived by hand
f_B_integrand = joint_B * m1_range_len  # integrate over that m1-strip
f_B = sp.integrate(f_B_integrand, (m2, 0, 1 - x))
f_B = sp.simplify(f_B)
print("=> f_B(x) =", f_B)

print()
print("="*70)
print("GROUP C: M2 = 1-m1-D2, D2~U(0,m2); prob(C|m1,m2)=m2(1-m1)  [mirror of B]")
print("="*70)
joint_C = 2*(1 - m1)
m2_range_len = x
f_C_integrand = joint_C * m2_range_len
f_C = sp.integrate(f_C_integrand, (m1, 0, 1 - x))
f_C = sp.simplify(f_C)
print("=> f_C(x) =", f_C)

print()
print("="*70)
print("GROUP A: M2 = 1-D1-D2, D1~U(0,m1),D2~U(0,m2) indep; prob(A|m1,m2)=2 m1 m2")
print("="*70)
# joint density of (m1,m2,d1,d2) restricted to group A:
#   2 [step A] * 2 m1 m2 [P(A)] * (1/m1) * (1/m2) [densities of D1,D2] = 4
# CONSTANT, on {0<d1<m1, 0<d2<m2, m1,m2>0, m1+m2<1}
joint_A = sp.Integer(4)
print("joint density of (m1,m2,d1,d2) restricted to group A =", joint_A,
      " (constant) on {0<d1<m1,0<d2<m2,(m1,m2) in T}")

# Step 1: marginalize out m1 (given d1: m1 ranges over (d1, 1-m2)) and
#         m2 (given d2: m2 ranges over (d2, 1-m1)) jointly.
# For fixed (d1,d2), the (m1,m2) region is {m1>d1, m2>d2, m1+m2<1}, a
# triangle of area (1-d1-d2)^2/2 when d1+d2<1 (else empty).
area_m1m2 = sp.Rational(1, 2) * (1 - d1 - d2) ** 2
g_d1d2 = sp.simplify(joint_A * area_m1m2)
print("marginal joint density of (D1,D2)=(d1,d2) within group A =", g_d1d2,
      " on {d1,d2>0, d1+d2<1}")

# Step 2: marginal density of sigma = d1+d2 (for fixed sigma, d1 ranges
# over (0,sigma), length sigma; integrand g_d1d2 depends only on d1+d2):
f_sigma = sp.integrate(g_d1d2.subs(d2, sigma - d1), (d1, 0, sigma))
f_sigma = sp.simplify(f_sigma)
print("marginal density of sigma=D1+D2 within group A, f_sigma(sigma) =", f_sigma)

# Step 3: M2 = 1-sigma => f_A(x) = f_sigma(1-x)
f_A = sp.simplify(f_sigma.subs(sigma, 1 - x))
print("=> f_A(x) =", f_A)

print()
print("="*70)
print("SUMMING ALL FOUR GROUPS")
print("="*70)
f_M2 = sp.simplify(f_A + f_B + f_C + f_D)
print("f_A(x) =", f_A)
print("f_B(x) =", f_B)
print("f_C(x) =", f_C)
print("f_D(x) =", f_D)
print()
print("f_{M2}(x) = f_A+f_B+f_C+f_D =", f_M2)

target = 4 * x * (1 - x ** 2)
diff = sp.simplify(f_M2 - target)
print("Target 4x(1-x^2) =", sp.expand(target))
print("Symbolic difference f_M2 - target =", diff)
print("EXACT MATCH:", diff == 0)

print()
print("="*70)
print("CROSS-CHECKS")
print("="*70)
mass_total = sp.integrate(f_M2, (x, 0, 1))
print("Total mass integral_0^1 f_M2 dx (should be 1):", sp.simplify(mass_total))
mean_total = sp.integrate(x * f_M2, (x, 0, 1))
print("Mean integral_0^1 x*f_M2 dx (should be phi_2 = 8/15):", sp.simplify(mean_total))
print("phi_2 exact value check:", sp.Rational(8, 15))

# second moment as an extra necessary-condition check beyond the mean
second_moment_derived = sp.integrate(x ** 2 * f_M2, (x, 0, 1))
second_moment_target = sp.integrate(x ** 2 * target, (x, 0, 1))
print("E[M2^2] from derived density:", sp.simplify(second_moment_derived))
print("E[M2^2] from target 4x(1-x^2):", sp.simplify(second_moment_target))
