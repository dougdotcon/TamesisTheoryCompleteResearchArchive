"""
Adversarial referee script 02.

Independent (fresh, from-scratch) symbolic re-derivation of x(D) :=
delta(D) + tau(M)/2 as an exact cubic polynomial in D, and of its four
coefficients c_0..c_3, using ONLY the prose definitions cited in this
lineage (never reading any .py file of any front):

  tau(m) := sum_{i=1}^m ((k-i)/n)^2           [cited, gamma_gap1_mgf_attempt]
  M = gamma*k + D
  delta(D) = D*(2*k*(1-gamma) - D - 1)/(2*n)  [cited exact identity,
                                                wave-17 front's own
                                                sigma_k(m)-sigma_k(x) identity
                                                at x=gamma*k]

Then: independently checks (numerically, over a grid, with EXACT
rational arithmetic -- no floats, no roundoff) the tightened coefficient
bounds claimed in the target front's Sec 4 Step 3:

  |c_0| <= (7/6) k^3/n^2 + (5/6) k^2/n^2
  |c_1| <= 2 k^2/n^2 + (1-gamma) k/n + k/n^2 + 3/(4n)
  |c_2| <= (1-gamma) k/(2 n^2) + 3/(4n)
  c_3   =  1/(6 n^2)                              (exact, not just a bound)
"""
import sympy as sp

k, n, m, D, i = sp.symbols('k n m D i', positive=True)
gamma = sp.symbols('gamma', positive=True)

# --- tau(m), derived fresh via sympy.summation ---
tau_m = sp.summation(((k - i) / n) ** 2, (i, 1, m))
tau_m = sp.expand(tau_m)
print("tau(m) =", tau_m)

# sanity: tau(0) should be 0
print("tau(0) =", sp.simplify(tau_m.subs(m, 0)))
assert sp.simplify(tau_m.subs(m, 0)) == 0

# tau(m)/2 with m -> M = gamma*k + D
M = gamma * k + D
tau_over_2 = sp.expand(tau_m.subs(m, M) / 2)

# delta(D), cited exact identity
delta_D = sp.expand(D * (2 * k * (1 - gamma) - D - 1) / (2 * n))

x_D = sp.expand(delta_D + tau_over_2)

# extract as polynomial in D
poly = sp.Poly(x_D, D)
coeffs = poly.all_coeffs()  # highest degree first
deg = poly.degree()
print("degree of x(D) in D:", deg)
assert deg == 3, "x(D) is not exactly cubic in D -- contradicts the cited fact!"

c3_, c2_, c1_, c0_ = [sp.simplify(c) for c in coeffs]  # highest->lowest: D^3,D^2,D^1,D^0
print("\nFresh (route A: direct substitution + Poly) coefficients:")
print("c0 =", c0_)
print("c1 =", c1_)
print("c2 =", c2_)
print("c3 =", c3_)

# --- Route B: derivative-based assembly, tau, tau', tau'' at m=gamma*k ---
tau_p = sp.diff(tau_m, m)
tau_pp = sp.diff(tau_m, m, 2)

c0_B = sp.simplify(tau_m.subs(m, gamma * k) / 2)
c1_B = sp.simplify(k * (1 - gamma) / n - 1 / (2 * n) + tau_p.subs(m, gamma * k) / 2)
c2_B = sp.simplify(-1 / (2 * n) + tau_pp.subs(m, gamma * k) / 4)
c3_B = sp.Rational(1, 6) / n ** 2

print("\nRoute B (derivative-based, cited formula) coefficients:")
print("c0 =", c0_B)
print("c1 =", c1_B)
print("c2 =", c2_B)
print("c3 =", c3_B)

print("\nCross-check route A vs route B (should be exactly zero):")
for name, a, b in [("c0", c0_, c0_B), ("c1", c1_, c1_B),
                    ("c2", c2_, c2_B), ("c3", c3_, c3_B)]:
    d = sp.simplify(a - b)
    print(f"  {name}: diff = {d}")
    assert d == 0, f"MISMATCH in {name} between the two independent routes!"

# numeric spot check at the referee's own historical test point gamma=1/2,k=10,n=100
spot = {gamma: sp.Rational(1, 2), k: 10, n: 100}
c0_spot = c0_.subs(spot)
print(f"\nSpot check c0(gamma=1/2,k=10,n=100) = {c0_spot} = {float(c0_spot)}")
assert c0_spot == sp.Rational(51, 4000), "c0 spot check FAILED vs Estagio 33's own corrected value!"

print("\n=== Cubic structure of x(D) independently CONFIRMED (route A vs B, exact zero diff). ===\n")

# ---------------------------------------------------------------------
# Now independently verify the target front's Sec.4 Step 3 tightened
# coefficient bounds via exact rational-number grid evaluation.
# ---------------------------------------------------------------------

c0_bound = sp.Rational(7, 6) * k ** 3 / n ** 2 + sp.Rational(5, 6) * k ** 2 / n ** 2
c1_bound = 2 * k ** 2 / n ** 2 + (1 - gamma) * k / n + k / n ** 2 + sp.Rational(3, 4) / n
c2_bound = (1 - gamma) * k / (2 * n ** 2) + sp.Rational(3, 4) / n
c3_exact_claim = sp.Rational(1, 6) / n ** 2

n_vals = [10, 30, 100, 1000, 10000, 100000, 1000000]
gamma_vals = [sp.Rational(1, 100), sp.Rational(1, 20), sp.Rational(1, 10),
              sp.Rational(3, 10), sp.Rational(1, 2), sp.Rational(7, 10),
              sp.Rational(9, 10), sp.Rational(99, 100), sp.Rational(999, 1000)]

total_checks = 0
violations = []

for nv in n_vals:
    kmax = max(1, nv // 2)
    # sample k across [1, kmax]: endpoints + several interior points
    k_samples = sorted(set([1, max(1, kmax // 8), max(1, kmax // 4),
                             max(1, 3 * kmax // 8), max(1, kmax // 2),
                             max(1, 5 * kmax // 8), max(1, 3 * kmax // 4),
                             kmax]))
    for gv in gamma_vals:
        for kv in k_samples:
            subs_map = {n: nv, gamma: gv, k: kv}
            c0v = c0_.subs(subs_map)
            c1v = c1_.subs(subs_map)
            c2v = c2_.subs(subs_map)
            c3v = c3_.subs(subs_map)

            c0b = c0_bound.subs(subs_map)
            c1b = c1_bound.subs(subs_map)
            c2b = c2_bound.subs(subs_map)
            c3claim = c3_exact_claim.subs(subs_map)

            total_checks += 4
            if not (abs(c0v) <= c0b):
                violations.append(("c0", nv, gv, kv, c0v, c0b))
            if not (abs(c1v) <= c1b):
                violations.append(("c1", nv, gv, kv, c1v, c1b))
            if not (abs(c2v) <= c2b):
                violations.append(("c2", nv, gv, kv, c2v, c2b))
            if c3v != c3claim:
                violations.append(("c3_exact", nv, gv, kv, c3v, c3claim))

print(f"Total pointwise inequality checks: {total_checks}")
print(f"Violations found: {len(violations)}")
for v in violations[:30]:
    print("  VIOLATION:", v)

assert len(violations) == 0, "Coefficient bounds FAILED at some grid point(s)!"
print("\n=== ALL coefficient bounds (|c0|,|c1|,|c2| <= claimed; c3 exact) ===")
print("=== independently CONFIRMED over", total_checks, "exact-rational checks. ===")
