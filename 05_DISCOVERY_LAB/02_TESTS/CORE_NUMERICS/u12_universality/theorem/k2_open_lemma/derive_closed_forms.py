"""
Symbolic closed-form derivation and full verification, tying together:

  1. psi_n^{(2)}   (generic-point quantity) -- symbolically summed in closed form from
     the case formulas of psi_k2_case_formula.py (cases a,b,c), verified against exact
     brute force (psi_bruteforce.py) for n=3..8.

  2. psi_n^{(2),R} (rerouted-point-itself quantity) -- NOT independently derived by hand
     here; obtained by exact rational interpolation from 3 brute-force data points
     (n=6,7,8) and then verified to match exactly on 3 further points (n=3,4,5). This
     piece is flagged in ATTEMPT.md as "confirmed by exact fit", not "derived from
     first principles" -- it plays no role in the K=2 Open Lemma proof itself (only
     boundedness in [0,1] is needed there), only in the bonus exact-rate result.

  3. phi_n^{(2)} (THEOREM.md Definition 4's actual quantity, SS7.4's table) recovered via
     the exact identity phi_n^{(2)} = (2/n) psi_n^{(2),R} + (1-2/n) psi_n^{(2)}, and
     verified against every value in THEOREM.md SS7.4's table (n=2..8).

Run: python3 derive_closed_forms.py
"""
import sympy as sp

n, L, p, q, d = sp.symbols('n L p q d', positive=True, integer=True)

print("=" * 70)
print("STEP 1: symbolic closed form of psi_n^{(2)} from the case sums")
print("=" * 70)

# case (a): sum_{L=1}^n (n-L)(n-L-1) / [n(n-1)(n-2)]
sumA = sp.summation((n - L) * (n - L - 1), (L, 1, n))
caseA = sp.simplify(sumA / (n * (n - 1) * (n - 2)))
print("case (a) total contribution:", sp.factor(caseA))

# case (b): sum_{L=1}^n (L-1)(n-L)*L*(3n-L+1) / [2 n^3 (n-1)(n-2)]
sumB = sp.summation((L - 1) * (n - L) * L * (3 * n - L + 1), (L, 1, n))
caseB = sp.simplify(sumB / (2 * n ** 3 * (n - 1) * (n - 2)))
print("case (b) total contribution:", sp.factor(caseB))

# case (c): needs T(L,n) = sum_{1<=p<q<=L-1} (L-q)(n+q-p), then sum over L
inner = sp.summation((L - q) * (n + q - p), (p, 1, q - 1))
T = sp.summation(inner, (q, 1, L - 1))
sumT = sp.summation(T, (L, 1, n))
caseC = sp.simplify(2 * sumT / (n ** 3 * (n - 1) * (n - 2)))
print("case (c) total contribution:", sp.factor(caseC))

psi2_closed = sp.simplify(caseA + caseB + caseC)
print("\npsi_n^{(2)} CLOSED FORM =", sp.factor(psi2_closed))
print("expanded around n=infinity:", sp.apart(psi2_closed, n))

# cross-check against brute force values (hardcoded from psi_bruteforce.py K=2 generic run)
bf_generic = {3: sp.Rational(17, 27), 4: sp.Rational(29, 48), 5: sp.Rational(221, 375),
              6: sp.Rational(313, 540), 7: sp.Rational(421, 735), 8: sp.Rational(109, 192)}
print("\nverification against brute force (psi_bruteforce.py, ref=generic):")
all_ok = True
for nn, val in bf_generic.items():
    pred = psi2_closed.subs(n, nn)
    ok = sp.simplify(pred - val) == 0
    all_ok &= ok
    print(f"  n={nn}: brute={val} closed_form={pred}  match={ok}")
print("ALL MATCH:", all_ok)

print()
print("=" * 70)
print("STEP 2: psi_n^{(2),R} by exact rational interpolation (fit, not derived)")
print("=" * 70)
bf_rerouted = {3: sp.Rational(17, 27), 4: sp.Rational(55, 96), 5: sp.Rational(27, 50),
               6: sp.Rational(14, 27), 7: sp.Rational(74, 147), 8: sp.Rational(63, 128)}

A, B, C = sp.symbols('A B C')
eqs = [sp.Eq(A * nn ** 2 + B * nn + C, 15 * nn ** 2 * bf_rerouted[nn]) for nn in (6, 7, 8)]
sol = sp.solve(eqs, [A, B, C])
psiR_closed = sp.simplify((sol[A] * n ** 2 + sol[B] * n + sol[C]) / (15 * n ** 2))
psiR_closed = sp.factor(psiR_closed)
print("fit on n=6,7,8 gives psi_n^{(2),R} =", psiR_closed)
print("verification on n=3,4,5 (held out of the fit):")
all_ok2 = True
for nn in (3, 4, 5, 6, 7, 8):
    pred = psiR_closed.subs(n, nn)
    ok = sp.simplify(pred - bf_rerouted[nn]) == 0
    all_ok2 &= ok
    print(f"  n={nn}: brute={bf_rerouted[nn]} fit={pred}  match={ok}")
print("ALL MATCH (6/6, only 3 free params):", all_ok2)

print()
print("=" * 70)
print("STEP 3: recombine to get phi_n^{(2)} and check against THEOREM.md SS7.4 table")
print("=" * 70)
phi2_closed = sp.simplify((sp.Integer(2) / n) * psiR_closed + (1 - sp.Integer(2) / n) * psi2_closed)
phi2_closed = sp.factor(phi2_closed)
print("phi_n^{(2)} CLOSED FORM =", phi2_closed)
print("apart (n -> infinity expansion):", sp.apart(phi2_closed, n))

phi2_limit = sp.Rational(8, 15)
dev = sp.simplify(phi2_closed - phi2_limit)
print("\nphi_n^{(2)} - phi_2 =", sp.factor(dev))
print("apart:", sp.apart(dev, n))
print("=> leading order is Theta(1/n) [coefficient 1/30], NOT Theta(1/n^2).")

theorem_table = {2: sp.Rational(3, 4), 3: sp.Rational(17, 27), 4: sp.Rational(113, 192),
                  5: sp.Rational(356, 625), 6: sp.Rational(151, 270), 7: sp.Rational(569, 1029),
                  8: sp.Rational(281, 512)}
print("\nverification against THEOREM.md SS7.4's own table (all 7 values, n=2..8):")
all_ok3 = True
for nn, val in theorem_table.items():
    pred = phi2_closed.subs(n, nn)
    ok = sp.simplify(pred - val) == 0
    all_ok3 &= ok
    print(f"  n={nn}: THEOREM.md={val} closed_form={pred}  match={ok}")
print("ALL MATCH (including n=2, outside the n>K=2 derivation range):", all_ok3)
