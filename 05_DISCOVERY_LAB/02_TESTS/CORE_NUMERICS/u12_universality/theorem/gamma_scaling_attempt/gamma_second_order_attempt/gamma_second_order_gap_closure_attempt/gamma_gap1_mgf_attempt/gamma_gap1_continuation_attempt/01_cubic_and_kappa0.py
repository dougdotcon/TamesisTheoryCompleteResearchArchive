"""
01_cubic_and_kappa0.py

Front: GAMMA-GAP1-CONTINUATION-ATTEMPT (wave 21, front a).
Fresh, independent symbolic derivation (no .py file from any ancestor front
was read) of:

  (A) x(D) := delta(D) + tau(M)/2  as an exact cubic polynomial in D,
      cross-checked against the (adversarially-corrected) closed forms
      quoted in gamma_gap1_mgf_attempt/ATTEMPT.md Section 2 (prose only,
      not code, was read).
  (B) The EXACT constant kappa_0(gamma) in the wave-17 front's own
      truncation K := ceil( sqrt( (4/beta) n ln n ) ), beta := gamma(2-gamma)/2
      -- quoted verbatim from gamma_scaling_attempt/ATTEMPT.md Section 5
      (prose only). This pins down kappa_0(gamma) = 4/beta = 8/(gamma(2-gamma)),
      which is NOT the gamma-independent illustrative constant kappa_0=2.25
      used for concreteness by the Gap-1 front (Estagio 33).

Ingredients used (all CITED, none re-derived from first principles beyond
what is already accepted in this lineage):
  tau(m) := sum_{i=1}^m ((k-i)/n)^2                      [cited, THEOREM.md lineage]
  delta(D) = D*(2*k*(1-gamma) - D - 1) / (2*n)            [cited, wave-17 identity
                                                            sigma_k(m)-sigma_k(x) =
                                                            (m-x)(2k-m-x-1)/(2n) at x=gamma*k]
  K := ceil( sqrt( (4/beta) * n * ln(n) ) ), beta := gamma*(2-gamma)/2
                                                          [cited verbatim, wave-17
                                                           front's own Theorem 2 proof,
                                                           gamma_scaling_attempt/ATTEMPT.md
                                                           Section 5, "Define, for
                                                           gamma in (0,1] and n>=3 ...
                                                           K := ceil(sqrt((4/beta) n ln n))"]

No .py file of any ancestor/sibling front was opened, read, or imported.
Reserved seed block 20260900000-20260900999 (unused here -- exact symbolic
algebra only, no randomness).
"""
import sympy as sp

k, n, gamma, D, m, i = sp.symbols('k n gamma D m i', positive=True)

print("=" * 78)
print("PART A: fresh symbolic re-derivation of x(D) = delta(D) + tau(M)/2")
print("=" * 78)

# tau(m) := sum_{i=1}^m ((k-i)/n)^2, closed form via sympy summation
i_sym = sp.symbols('i_sym', integer=True, positive=True)
tau_m_summand = ((k - i_sym) / n) ** 2
tau_closed = sp.summation(tau_m_summand, (i_sym, 1, m))
tau_closed = sp.simplify(tau_closed)
print("\ntau(m) closed form (sympy.summation):")
sp.pprint(tau_closed)

# delta(D), cited exact identity
delta_D = D * (2 * k * (1 - gamma) - D - 1) / (2 * n)
print("\ndelta(D) (cited exact identity):")
sp.pprint(sp.simplify(delta_D))

# M = gamma*k + D; substitute into tau, form x(D) = delta(D) + tau(M)/2
M_expr = gamma * k + D
tau_of_M = tau_closed.subs(m, M_expr)
x_of_D = sp.expand(delta_D + tau_of_M / 2)

x_poly = sp.Poly(x_of_D, D)
coeffs = x_poly.all_coeffs()[::-1]  # ascending order: c0, c1, c2, c3
labels = ['c0', 'c1', 'c2', 'c3']
c_fresh = {}
print("\nx(D) expanded as a polynomial in D (ascending powers):")
for lbl, co in zip(labels, coeffs):
    co_s = sp.simplify(co)
    c_fresh[lbl] = co_s
    print(f"  {lbl} = {co_s}")

deg = x_poly.degree()
print(f"\nDegree of x(D) in D: {deg} (expect exactly 3 -- confirms exact cubic, "
      f"no higher-order terms, since tau is exactly cubic in m and its 4th "
      f"derivative is identically 0)")
assert deg == 3, "x(D) is not exactly cubic -- STOP, contradicts predecessor"

print("\n" + "-" * 78)
print("Cross-check against gamma_gap1_mgf_attempt/ATTEMPT.md Section 2's")
print("adversarially-CORRECTED closed forms (prose, quoted verbatim, not code):")
print("-" * 78)

# Predecessor's (corrected) closed forms, quoted verbatim from the ATTEMPT.md prose:
c0_predecessor = (gamma * k / (12 * n ** 2)) * (
    2 * gamma ** 2 * k ** 2 - 6 * gamma * k ** 2 + 3 * gamma * k + 6 * k ** 2 - 6 * k + 1
)
c1_predecessor = (1 / n ** 2) * (
    (gamma ** 2 * k ** 2) / 2 - gamma * k ** 2 - gamma * k * n + (gamma * k) / 2
    + (k ** 2) / 2 + k * n - k / 2 - n / 2 + sp.Rational(1, 12)
)
c2_predecessor = (2 * gamma * k - 2 * k - 2 * n + 1) / (4 * n ** 2)
c3_predecessor = sp.Rational(1, 6) / n ** 2

preds = {'c0': c0_predecessor, 'c1': c1_predecessor, 'c2': c2_predecessor, 'c3': c3_predecessor}

all_match = True
for lbl in labels:
    diff = sp.simplify(c_fresh[lbl] - preds[lbl])
    match = (diff == 0)
    all_match = all_match and match
    print(f"  {lbl}: fresh - predecessor(corrected) = {diff}  ->  MATCH: {match}")

print(f"\nAll four coefficients match the adversarially-corrected predecessor "
      f"forms exactly: {all_match}")
assert all_match, "Mismatch against predecessor's corrected c_i -- investigate"

# Numeric spot check, gamma=1/2, k=10, n=100 (the point the referee used for c0)
subs_pt = {gamma: sp.Rational(1, 2), k: 10, n: 100}
c0_num = sp.nsimplify(c_fresh['c0'].subs(subs_pt))
print(f"\nNumeric spot check (gamma=1/2, k=10, n=100): c0 = {c0_num} "
      f"(referee's confirmed correct value: 51/4000 = {sp.Rational(51,4000)})")
assert c0_num == sp.Rational(51, 4000)

print("\n" + "=" * 78)
print("PART B: pinning down kappa_0(gamma), the EXACT wave-17 truncation constant")
print("=" * 78)

beta = gamma * (2 - gamma) / 2
K_squared_over_nlnn = sp.simplify(4 / beta)  # K^2 ~ (4/beta) n ln n  (ignoring ceiling)
kappa0_gamma = sp.simplify(K_squared_over_nlnn)
print(f"\nWave-17 front's own truncation (gamma_scaling_attempt/ATTEMPT.md Section 5, "
      f"quoted verbatim):")
print(f"  K := ceil( sqrt( (4/beta) * n * ln(n) ) ),  beta := gamma*(2-gamma)/2")
print(f"\nHence K^2 = (4/beta) n ln n + O(sqrt(n ln n))  (ceiling correction),")
print(f"i.e. in the Gap-1 front's own notation 'K^2 = kappa_0 * n * ln n':")
print(f"\n  kappa_0(gamma) = 4/beta = {kappa0_gamma}")

kappa0_at_1 = kappa0_gamma.subs(gamma, 1)
print(f"\nkappa_0(gamma=1)      = {kappa0_at_1}")
print(f"kappa_0(gamma=0.5)    = {kappa0_gamma.subs(gamma, sp.Rational(1,2))}")
print(f"kappa_0(gamma=0.1)    = {sp.nsimplify(kappa0_gamma.subs(gamma, sp.Rational(1,10)))} "
      f"= {float(kappa0_gamma.subs(gamma, sp.Rational(1,10))):.4f}")
print(f"kappa_0(gamma=0.01)   = {float(kappa0_gamma.subs(gamma, sp.Rational(1,100))):.4f}")
limit_g0 = sp.limit(kappa0_gamma, gamma, 0, dir='+')
print(f"\nlim_{{gamma->0+}} kappa_0(gamma) = {limit_g0}")

print(f"\n*** CENTRAL FINDING ***")
print(f"kappa_0 is NOT a gamma-independent constant. The illustrative value")
print(f"kappa_0=2.25 used by the Gap-1 front (Estagio 33) for concreteness is")
print(f"neither the correct value at any single gamma (kappa_0(1)=8, not 2.25),")
print(f"nor a valid stand-in for a gamma-independent constant, since the true")
print(f"kappa_0(gamma) = 8/(gamma(2-gamma)) diverges as gamma -> 0+.")

print("\nDone.")
