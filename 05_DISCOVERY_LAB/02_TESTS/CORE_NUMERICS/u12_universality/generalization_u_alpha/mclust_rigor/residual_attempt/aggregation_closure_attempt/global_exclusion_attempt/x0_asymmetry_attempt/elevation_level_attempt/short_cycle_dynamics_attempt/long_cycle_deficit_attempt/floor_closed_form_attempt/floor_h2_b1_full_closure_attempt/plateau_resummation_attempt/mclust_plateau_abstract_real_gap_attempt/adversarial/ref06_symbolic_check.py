#!/usr/bin/env python3
"""
Independent sympy symbolic verification of:
  (1) R'(x) = x*R(x) - 1, for R(x) = sqrt(pi/2)*erfcx(x/sqrt(2))
  (2) the closure identity R^{(n+1)}(x) = x*R^{(n)}(x) + n*R^{(n-1)}(x), n=1..6
  (3) the psi_n(0) = gamma_n * R^{(n-1)}(0) bookkeeping for n=1..4, matched
      against the record's own already-established psi_n(0) values
  (4) the arithmetic equivalence gamma_5 = 209/24  <=>  d4 = 209/8
      via the relation d_{n} = sqrt(2/pi) * psi_{n+1}(0) (re-derived below
      from the definitions y(eps):=Pi(c)*sqrt(2c/pi), Pi(c)=sum eps^n psi_n(0),
      both stated in the target document's Sec 0 restatement of the record).
"""
import sympy as sp

x, n = sp.symbols('x n', real=True)

# erfcx via sympy: erfcx(z) = exp(z**2)*erfc(z)
z = x / sp.sqrt(2)
erfcx_expr = sp.exp(z**2) * sp.erfc(z)
R = sp.sqrt(sp.pi / 2) * erfcx_expr

print("=== (1) R'(x) = x*R(x) - 1 ===")
Rp = sp.diff(R, x)
residual1 = sp.simplify(Rp - (x * R - 1))
print("R'(x) - (x*R(x)-1) simplifies to:", residual1)
assert residual1 == 0, "FAIL: R'=xR-1 identity"
print("PASS\n")

print("=== (2) Closure identity R^{(n+1)} = x*R^{(n)} + n*R^{(n-1)}, n=1..6 ===")
# build derivative list R^{(0)}=R, R^{(1)}=R', ...
Rders = [R]
for i in range(1, 9):
    Rders.append(sp.diff(Rders[-1], x))

all_pass = True
for nn in range(1, 7):
    lhs = Rders[nn + 1]
    rhs = x * Rders[nn] + nn * Rders[nn - 1]
    resid = sp.simplify(lhs - rhs)
    ok = (resid == 0)
    all_pass &= ok
    print(f"  n={nn}: residual simplifies to {resid}  ->  {'PASS' if ok else 'FAIL'}")
assert all_pass
print("ALL PASS\n")

print("=== (3) psi_n(0) = gamma_n * R^{(n-1)}(0), n=1..4, matched to established psi_n(0) ===")
R_at_0 = [sp.simplify(Rders[i].subs(x, 0)) for i in range(0, 6)]
for i, val in enumerate(R_at_0):
    print(f"  R^{{({i})}}(0) = {val}")

# established (record, machine-verified elsewhere) psi_n(0) values:
psi_established = {
    1: sp.sqrt(sp.pi / 2),
    2: sp.Integer(-2),
    3: sp.Rational(7, 2) * sp.sqrt(sp.pi / 2),
    4: sp.Rational(-34, 3),
}
gamma_established = {1: sp.Integer(1), 2: sp.Integer(2), 3: sp.Rational(7, 2), 4: sp.Rational(17, 3)}

for nn in range(1, 5):
    Rprev0 = R_at_0[nn - 1]  # R^{(n-1)}(0)
    gamma_n_recovered = sp.simplify(psi_established[nn] / Rprev0)
    matches = sp.simplify(gamma_n_recovered - gamma_established[nn]) == 0
    print(f"  n={nn}: psi_n(0)={psi_established[nn]}, R^({nn-1})(0)={Rprev0}, "
          f"recovered gamma_n={gamma_n_recovered}, established gamma_n={gamma_established[nn]}, "
          f"match={matches}")
    assert matches
print("ALL 4/4 MATCH\n")

print("=== (4) gamma_5=209/24  <=>  d4=209/8 ===")
# d_n = sqrt(2/pi) * psi_{n+1}(0)   [re-derived: y(eps):=Pi(c)*sqrt(2c/pi),
#   Pi(c) = sum_k eps^k psi_k(0)  (eps=1/sqrt(c)), so
#   y = sqrt(2/pi)*(1/eps)*sum_k eps^k psi_k(0) = sqrt(2/pi)*sum_k eps^{k-1} psi_k(0)
#   => coefficient of eps^n in y is sqrt(2/pi)*psi_{n+1}(0), i.e. d_n = sqrt(2/pi)*psi_{n+1}(0) ]
gamma5 = sp.Rational(209, 24)
R4_at_0 = R_at_0[4]  # R^{(4)}(0)
psi5_0 = sp.simplify(gamma5 * R4_at_0)
d4_predicted = sp.simplify(sp.sqrt(sp.Rational(2, 1) / sp.pi) * psi5_0)
d4_conjectured = sp.Rational(209, 8)
print(f"  R^(4)(0) = {R4_at_0}")
print(f"  psi5(0) = gamma_5 * R^(4)(0) = {psi5_0}")
print(f"  d4 predicted from gamma_5 via d4 = sqrt(2/pi)*psi5(0) = {d4_predicted}")
print(f"  d4 conjectured (record) = {d4_conjectured}")
equiv = sp.simplify(d4_predicted - d4_conjectured) == 0
print(f"  EXACT MATCH: {equiv}")
assert equiv

# cross-check the d0..d3 <-> psi1..psi4 mapping too, as a consistency check
# on the re-derived relation d_n = sqrt(2/pi)*psi_{n+1}(0)
print("\n  Cross-check d0..d3 via the same mapping:")
d_conjectured_or_derived = {
    0: sp.Integer(1),
    1: -2 * sp.sqrt(sp.Rational(2, 1) / sp.pi),
    2: sp.Rational(7, 2),
    3: -sp.Rational(34, 3) * sp.sqrt(sp.Rational(2, 1) / sp.pi),
}
for nn in range(0, 4):
    pred = sp.simplify(sp.sqrt(sp.Rational(2, 1) / sp.pi) * psi_established[nn + 1])
    match = sp.simplify(pred - d_conjectured_or_derived[nn]) == 0
    print(f"    d{nn}: predicted={pred}  established={d_conjectured_or_derived[nn]}  match={match}")
    assert match
print("  ALL d0..d3 CONSISTENT WITH THE psi-BOOKKEEPING MAPPING\n")

print("ALL SYMBOLIC CHECKS PASSED.")
