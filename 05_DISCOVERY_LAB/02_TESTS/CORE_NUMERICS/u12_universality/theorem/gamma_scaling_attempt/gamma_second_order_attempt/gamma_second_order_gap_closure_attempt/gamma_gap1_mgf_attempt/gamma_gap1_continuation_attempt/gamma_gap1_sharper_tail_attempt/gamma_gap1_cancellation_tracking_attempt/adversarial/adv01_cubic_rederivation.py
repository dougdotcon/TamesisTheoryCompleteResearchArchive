"""
Independent referee re-derivation #1: the exact cubic coefficients c0..c3
of x(D) := delta(D) + tau(M)/2, M = gamma*k + D.

Written from scratch, from the raw definitions quoted in the required
reading (THEOREM.md / ancestor ATTEMPT.md prose), WITHOUT reading the
target's own scripts.

Definitions (all cited from the required reading, not re-derived from
first principles beyond what's given):
  tau(m) := sum_{i=1}^m ((k-i)/n)^2
  delta(D) = D*(2*k*(1-gamma) - D - 1) / (2*n)     [cited, wave-17 exact identity]
  x(D) := delta(D) + tau(M)/2,  M = gamma*k + D
"""
import sympy as sp

k, n, gamma, D, m, i = sp.symbols('k n gamma D m i', positive=True)

# tau(m) as a function of integer m: sum_{i=1}^m ((k-i)/n)^2
m_sym = sp.symbols('m', positive=True, integer=True)
tau_m = sp.summation(((k - i)/n)**2, (i, 1, m_sym))
tau_m = sp.simplify(sp.expand(tau_m))
print("tau(m) closed form:")
sp.pprint(tau_m)
print()

# Substitute m -> M = gamma*k + D
M = gamma*k + D
tau_M = tau_m.subs(m_sym, M)
tau_M = sp.expand(tau_M)

delta_D = D*(2*k*(1-gamma) - D - 1) / (2*n)

x_D = sp.expand(delta_D + tau_M/2)

# Extract as polynomial in D
poly = sp.Poly(x_D, D)
coeffs = poly.all_coeffs()  # highest degree first
# poly should be degree 3 in D
print("Degree in D:", poly.degree())
c3 = sp.simplify(poly.coeff_monomial(D**3))
c2 = sp.simplify(poly.coeff_monomial(D**2))
c1 = sp.simplify(poly.coeff_monomial(D**1))
c0 = sp.simplify(poly.coeff_monomial(D**0))

print("\nMy independently re-derived coefficients:")
print("c0 =", c0)
print("c1 =", c1)
print("c2 =", c2)
print("c3 =", c3)

# Now compare against the target's §2 quoted forms:
target_c0 = gamma*k*(2*gamma**2*k**2 - 6*gamma*k**2 + 3*gamma*k + 6*k**2 - 6*k + 1) / (12*n**2)
target_c1 = (gamma**2*k**2/2 - gamma*k**2 - gamma*k*n + gamma*k/2 + k**2/2 + k*n - k/2 - n/2 + sp.Rational(1,12)) / n**2
target_c2 = (2*gamma*k - 2*k - 2*n + 1) / (4*n**2)
target_c3 = sp.Rational(1,6) / n**2

print("\nDifference (mine - target), should be exactly 0 each:")
diff0 = sp.simplify(c0 - target_c0)
diff1 = sp.simplify(c1 - target_c1)
diff2 = sp.simplify(c2 - target_c2)
diff3 = sp.simplify(c3 - target_c3)
print("diff c0 =", diff0)
print("diff c1 =", diff1)
print("diff c2 =", diff2)
print("diff c3 =", diff3)

all_match = all(d == 0 for d in (diff0, diff1, diff2, diff3))
print("\nALL FOUR COEFFICIENTS MATCH TARGET'S §2 TRANSCRIPTION EXACTLY:", all_match)

# Numeric spot check at gamma=1/2, k=10, n=100 (same point grandparent referee used)
vals = {gamma: sp.Rational(1,2), k: 10, n: 100}
c0_num = c0.subs(vals)
print("\nNumeric spot check c0(gamma=1/2,k=10,n=100) =", c0_num, "== 51/4000?", c0_num == sp.Rational(51,4000))
