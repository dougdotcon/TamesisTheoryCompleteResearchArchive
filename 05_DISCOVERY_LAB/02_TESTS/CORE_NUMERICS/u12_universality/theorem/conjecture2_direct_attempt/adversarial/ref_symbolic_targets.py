"""Referee re-derivation (independent, from ATTEMPT.md prose only) of every
symbolic claim in conjecture2_direct_attempt/ATTEMPT.md Sections 2, 3.1, 3.2,
3.4 and the Section 3.5 harness targets.

No script of the front was read or reused. Exact sympy arithmetic throughout;
floats only for printing reference values.

Checks:
  [S1] Route A: E[min(1, E/c)] = (1 - e^-c)/c          (M(c)^2 = min(1,E/c))
  [S2] Route B: E[M_K^2] from the conjectured density 2Kx(1-x^2)^{K-1}
       equals 1/(K+1) (symbolic in K), two independent integration routes
       (direct in x, and substitution u = x^2 -> Beta integral).
  [S3] Poisson(c)-mixture of {1 (K=0); 1/(K+1) (K>=1)} = (1 - e^-c)/c.
  [S4] Cross-check against the archive's PROVED densities:
       K=1: f=2x        -> E[M_1^2] = 1/2  (THEOREM.md Sec 5.3)
       K=2: f=4x(1-x^2) -> E[M_2^2] = 1/3  (conjecture1_k2_attempt)
       K=3: f=6x(1-x^2)^2 -> E[M_3^2] = 1/4 (conjecture1_k3_attempt)
  [S5] p=1 consistency: E[min(1, sqrt(E/c))] = int_0^1 e^{-c t^2} dt
       (the conjectured law's mean equals the PROVED phi_inf(c)).
  [S6] Necessary-condition sandwich for the target second moment:
       phi_inf(c)^2 <= (1-e^-c)/c <= phi_inf(c) on a numeric grid
       (must hold for the true law of M(c) in [0,1]; the conjectured
       target must satisfy it or the target itself would be refuted).
  [S7] Lemma B1/B2/B3 continuum arithmetic: E[L]=1/2 for L~U(0,1);
       f_{L|same}=2*l integrates to 1; joint density 1 on the simplex
       integrates to 1/2 = P(different).
  [S8] Lemma B4 inequality: e^{-c*l} < e^{-c*l^2} for l in (0,1), c>0,
       i.e. the intact-block bound is strictly below the marginal.
  [S9] Section 3.5 harness targets: phi_inf(1), phi_inf(4), (1-e^-1),
       (1-e^-4)/4 to >= 6 decimals (are 0.74682 / 0.63212 / 0.44104 /
       0.24542 the right numbers?).
"""
import sympy as sp

c, e_, x, u, l, t = sp.symbols('c e x u l t', positive=True)
K = sp.Symbol('K', integer=True, positive=True)

FAIL = 0


def check(name, ok, detail=""):
    global FAIL
    tag = "PASS" if ok else "FAIL"
    if not ok:
        FAIL += 1
    print(f"[{tag}] {name}" + (f"  {detail}" if detail else ""))


target = (1 - sp.exp(-c)) / c

# [S1] Route A -----------------------------------------------------------
routeA = sp.integrate((e_ / c) * sp.exp(-e_), (e_, 0, c)) \
       + sp.integrate(sp.exp(-e_), (e_, c, sp.oo))
routeA = sp.simplify(routeA)
check("S1 route A: E[min(1,E/c)] == (1-e^-c)/c",
      sp.simplify(routeA - target) == 0, f"routeA={routeA}")

# [S2] E[M_K^2] two ways -------------------------------------------------
mk2_direct = sp.simplify(sp.integrate(x**2 * 2 * K * x * (1 - x**2)**(K - 1),
                                      (x, 0, 1)))
check("S2a E[M_K^2] direct integral == 1/(K+1)",
      sp.simplify(mk2_direct - 1 / (K + 1)) == 0, f"got {mk2_direct}")

# substitution u = x^2: integral becomes K * int_0^1 u (1-u)^{K-1} du = K*B(2,K)
mk2_beta = sp.simplify(K * sp.integrate(u * (1 - u)**(K - 1), (u, 0, 1)))
check("S2b E[M_K^2] Beta-route == 1/(K+1)",
      sp.simplify(mk2_beta - 1 / (K + 1)) == 0, f"got {mk2_beta}")

# [S3] Poisson mixture ---------------------------------------------------
Kk = sp.Symbol('k', integer=True, nonnegative=True)
mix = sp.exp(-c) * (1 + sp.summation(c**Kk / sp.factorial(Kk) / (Kk + 1),
                                     (Kk, 1, sp.oo)))
mix = sp.simplify(mix)
check("S3 Poisson mixture (K=0 term 1, K>=1 term 1/(K+1)) == (1-e^-c)/c",
      sp.simplify(mix - target) == 0, f"mix={mix}")

# [S4] proved-instance anchors ------------------------------------------
m1 = sp.integrate(x**2 * 2 * x, (x, 0, 1))
m2 = sp.integrate(x**2 * 4 * x * (1 - x**2), (x, 0, 1))
m3 = sp.integrate(x**2 * 6 * x * (1 - x**2)**2, (x, 0, 1))
check("S4 K=1 (proved density 2x): E[M_1^2] == 1/2", m1 == sp.Rational(1, 2), f"{m1}")
check("S4 K=2 (proved density 4x(1-x^2)): E[M_2^2] == 1/3", m2 == sp.Rational(1, 3), f"{m2}")
check("S4 K=3 (proved density 6x(1-x^2)^2): E[M_3^2] == 1/4", m3 == sp.Rational(1, 4), f"{m3}")
# also: normalization of each proved density
for kk, dens in ((1, 2 * x), (2, 4 * x * (1 - x**2)), (3, 6 * x * (1 - x**2)**2)):
    nrm = sp.integrate(dens, (x, 0, 1))
    check(f"S4 K={kk} density normalizes to 1", nrm == 1, f"{nrm}")

# [S5] p=1 consistency of the conjectured law's mean ---------------------
mean_conj = sp.integrate(sp.sqrt(e_ / c) * sp.exp(-e_), (e_, 0, c)) \
          + sp.integrate(sp.exp(-e_), (e_, c, sp.oo))
phi_inf = sp.integrate(sp.exp(-c * t**2), (t, 0, 1))
diff = sp.simplify(sp.expand(sp.simplify(mean_conj - phi_inf)))
# both should equal (1/2)sqrt(pi/c) erf(sqrt c); allow rewrite
diff2 = sp.simplify(diff.rewrite(sp.erf))
check("S5 E[min(1,sqrt(E/c))] == int_0^1 e^{-ct^2} dt (mean == phi_inf, exact)",
      diff2 == 0, f"diff={diff2}")

# [S6] sandwich on a grid ------------------------------------------------
import mpmath as mp
ok6 = True
worst = None
for cv in [0.01, 0.1, 0.25, 0.5, 1, 2, 3, 4, 6, 8, 10, 20, 50, 100]:
    m2v = (1 - mp.e**(-cv)) / cv
    mev = float(mp.quad(lambda tt: mp.e**(-cv * tt * tt), [0, 1]))
    if not (mev**2 - 1e-12 <= m2v <= mev + 1e-12):
        ok6 = False
        worst = (cv, m2v, mev)
check("S6 phi_inf(c)^2 <= (1-e^-c)/c <= phi_inf(c) on grid c in [0.01,100]",
      ok6, f"violation at {worst}" if worst else "")

# [S7] Lemma B1/B2/B3 continuum arithmetic -------------------------------
check("S7 B1: E[L] = 1/2 for L~Unif(0,1)",
      sp.integrate(l, (l, 0, 1)) == sp.Rational(1, 2))
check("S7 B2: f_{L|same}(l)=2l integrates to 1",
      sp.integrate(2 * l, (l, 0, 1)) == 1)
l1, l2 = sp.symbols('l1 l2', positive=True)
simplex_mass = sp.integrate(sp.integrate(1, (l2, 0, 1 - l1)), (l1, 0, 1))
check("S7 B3: density 1 on {l1+l2<1} has total mass 1/2 == P(different)",
      simplex_mass == sp.Rational(1, 2), f"{simplex_mass}")
# B3 marginal sanity: from joint density 1 on the simplex, the marginal of L1 is (1-l1),
# and the sub-density identity 1*(1-l1)*(1/(1-l1)) == 1 is trivially exact:
check("S7 B3: 1*(1-l1)*(1/(1-l1)) == 1 (the residual-rescaling arithmetic)",
      sp.simplify(1 * (1 - l1) * (1 / (1 - l1)) - 1) == 0)

# [S8] Lemma B4 inequality ----------------------------------------------
# e^{-c l} < e^{-c l^2}  <=>  l^2 < l  <=>  0 < l < 1
ineq = sp.simplify(l - l**2)  # >0 on (0,1)
check("S8 l - l^2 > 0 on (0,1) => e^{-cl} < e^{-cl^2} strictly (c>0)",
      sp.reduce_inequalities(ineq > 0, l) is not sp.false and
      all((vv - vv**2) > 0 for vv in [0.01, 0.3, 0.5, 0.7, 0.99]))

# [S9] harness targets ---------------------------------------------------
phi1 = float(mp.quad(lambda tt: mp.e**(-1 * tt * tt), [0, 1]))
phi4 = float(mp.quad(lambda tt: mp.e**(-4 * tt * tt), [0, 1]))
t1 = float(1 - mp.e**-1)
t4 = float((1 - mp.e**-4) / 4)
print(f"      phi_inf(1) = {phi1:.7f}   (ATTEMPT quotes 0.74682)")
print(f"      (1-e^-1)   = {t1:.7f}   (ATTEMPT quotes 0.63212)")
print(f"      phi_inf(4) = {phi4:.7f}   (ATTEMPT quotes 0.44104)")
print(f"      (1-e^-4)/4 = {t4:.7f}   (ATTEMPT quotes 0.24542)")
check("S9 phi_inf(1) rounds to 0.74682", abs(phi1 - 0.74682) < 5e-6)
check("S9 (1-e^-1)  rounds to 0.63212", abs(t1 - 0.63212) < 5e-6)
check("S9 phi_inf(4) rounds to 0.44104", abs(phi4 - 0.44104) < 5e-6)
check("S9 (1-e^-4)/4 rounds to 0.24542", abs(t4 - 0.24542) < 5e-6)

# general-p moment of the conjectured law (referee bonus, for the record):
p = sp.Symbol('p', positive=True)
mom = sp.integrate((e_ / c)**(p / 2) * sp.exp(-e_), (e_, 0, c)) \
    + sp.exp(-c)
mom = sp.simplify(mom)
print(f"      [record] E[min(1,sqrt(E/c))^p] = {mom}")
mom2 = sp.simplify(mom.subs(p, 2))
check("S9b general-p formula reduces at p=2 to (1-e^-c)/c",
      sp.simplify(mom2 - target) == 0, f"{mom2}")

print()
print("TOTAL FAILURES:", FAIL)
assert FAIL == 0, "AT LEAST ONE SYMBOLIC CHECK FAILED"
print("ALL SYMBOLIC CHECKS PASSED")
