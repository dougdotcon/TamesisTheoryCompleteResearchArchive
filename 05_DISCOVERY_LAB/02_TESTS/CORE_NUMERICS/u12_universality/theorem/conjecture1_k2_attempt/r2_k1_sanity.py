"""R2: reproduce THEOREM.md Sec 5.3's f_{M_1}(x)=2x using the SAME
marginalization machinery as derive_density_full.py's Group derivations,
as a sanity check that the general method is being applied correctly.
"""
import sympy as sp

x, m1, d1 = sp.symbols('x m1 d1', positive=True)

# K=1: single region, mass m1=L~Unif(0,1) [Fact A, density 1 on (0,1)].
# u1 self (lands in region1, prob m1) or out (prob 1-m1).

# self: joint density of (m1,d1) = 1 [f_L] * (1/m1)[density D1|m1] * m1[[wait: prob(self|m1)=m1, times density of D1|m1=1/m1]
#   = 1 * m1 * (1/m1) = 1, on 0<d1<m1<1
joint_self = sp.Integer(1)
# marginal density of D1=d1: integrate over m1 in (d1,1)
f_D1 = sp.integrate(joint_self, (m1, d1, 1))
f_D1 = sp.simplify(f_D1)
print("marginal density of D1 within self-branch:", f_D1)
f_self = sp.simplify(f_D1.subs(d1, 1 - x))
print("f_self(x) [M1=1-D1] =", f_self)

# out: weight = 1*(1-m1) [f_L * prob(out|m1)], M1=1-m1 deterministic
ell = sp.symbols('ell', positive=True)
weight_out = 1 * (1 - ell)
f_out = sp.simplify(weight_out.subs(ell, 1 - x))
print("f_out(x) [M1=1-m1] =", f_out)

f_M1 = sp.simplify(f_self + f_out)
print("f_M1(x) = f_self+f_out =", f_M1)
print("Matches 2x:", sp.simplify(f_M1 - 2 * x) == 0)

mean_check = sp.integrate(x * f_M1, (x, 0, 1))
print("mean check (should be phi_1=2/3):", mean_check)
