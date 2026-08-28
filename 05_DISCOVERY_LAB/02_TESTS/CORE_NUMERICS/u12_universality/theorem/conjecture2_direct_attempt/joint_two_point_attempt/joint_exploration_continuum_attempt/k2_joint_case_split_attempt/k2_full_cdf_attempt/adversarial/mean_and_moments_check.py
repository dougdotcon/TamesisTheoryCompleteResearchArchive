#!/usr/bin/env python3
"""
INDEPENDENT check of ATTEMPT.md's Corollaries D2.1-D2.4 (mean recovery,
P(T=n), second/third moment limits) and D2.5 (uniform convergence rate).

No .py file from any front in this lineage was read. The Proposicao D2
closed form is transcribed once (as the object under test); the cited
THEOREM.md target formulas (Estagio 3's phi_n^(2), the K=2 continuum
density from Estagio 15/24) are transcribed from THEOREM.md's own prose,
independently re-read in this session (see the adversarial report), NOT
from ATTEMPT.md's citation of them.
"""
import sympy as sp

n, k, x = sp.symbols('n k x', positive=True)

D2 = k * (k + 1) * (2 * n**2 - 3 * n + k - k**2) / (n**3 * (n - 1))

print("=" * 70)
print("Corollary D2.1: P(T=n) = 1 - F(n-1) should equal 2/n^2")
print("=" * 70)
F_at_boundary = sp.simplify(D2.subs(k, n - 1))
P_Tn = sp.simplify(1 - F_at_boundary)
claim = sp.Rational(2) / n**2
diff = sp.simplify(P_Tn - claim)
print(f"  1 - F(n-1) = {P_Tn}")
print(f"  claimed 2/n^2 = {claim}")
print(f"  diff = {diff}   {'OK' if diff == 0 else 'MISMATCH'}")
assert diff == 0

print()
print("=" * 70)
print("Corollary D2.2: mean recovery.")
print("  phi_n^(2) = 1 - (1/n) * sum_{k=0}^{n-1} F(k)   [standard identity")
print("  for a nonnegative integer r.v. T<=n, phi := E[T]/n = E[M_n^(2)]]")
print("=" * 70)

k_int = sp.symbols('k', integer=True, nonnegative=True)
D2_k = D2.subs(k, k_int)
S = sp.summation(D2_k, (k_int, 0, n - 1))
S = sp.simplify(S)
phi_derived = sp.simplify(1 - S / n)
print(f"  sum_{{k=0}}^{{n-1}} F(k) = {S}")
print(f"  phi_n^(2) [derived from D2] = {sp.expand(phi_derived)}")

# THEOREM.md Estagio 3 (independently re-read from THEOREM.md in this
# session, lines ~1432-1457): phi_n^(2) = 8/15 + 1/(30n) + 7/(10n^2)
#                                          + 1/(5n^3)
phi_cited = sp.Rational(8, 15) + sp.Rational(1, 30) / n + sp.Rational(7, 10) / n**2 + sp.Rational(1, 5) / n**3
diff_phi = sp.simplify(phi_derived - phi_cited)
print(f"  phi_n^(2) [THEOREM.md Estagio 3, independently re-read] "
      f"= {phi_cited}")
print(f"  diff = {sp.nsimplify(diff_phi)}   "
      f"{'OK -- zero symbolic remainder confirmed' if diff_phi == 0 else 'MISMATCH'}")
assert diff_phi == 0

print()
print("=" * 70)
print("Corollary D2.3/D2.4: second/third moment n->oo limits.")
print("  E[(M_n^(2))^r] = 1 - r/n^r * sum_{k=0}^{n-1} k^(r-1) * (n - F(k)")
print("  -- easier: use E[X^r] for X=T via the tail-sum identity in terms")
print("  of M = T/n directly: E[M^r] = sum_{k=0}^{n-1} [(k+1)/n)^r -")
print("  (k/n)^r] * (1-F(k)) + 1^r * ... -- instead we just integrate")
print("  numerically-symbolically via the direct pmf: pmf(k) = F(k)-F(k-1)")
print("  for k=1..n, F(-1):=0, and E[M^r] = sum_k (k/n)^r * pmf(k).")
print("=" * 70)

F_full = sp.Piecewise((0, k_int < 0), (1, k_int >= n), (D2_k, True))
pmf_k = sp.simplify(F_full.subs(k_int, k_int) - F_full.subs(k_int, k_int - 1))
# Build pmf directly instead via D2(k)-D2(k-1) for 1<=k<=n-1, plus
# pmf(0)=D2(0)=0, pmf(n)=1-D2(n-1).
pmf_generic = sp.simplify(D2.subs(k, k_int) - D2.subs(k, k_int - 1))
print(f"  pmf(k) [for 1<=k<=n-1] = D2(k)-D2(k-1) = {sp.factor(pmf_generic)}")

E_M2 = sp.summation((k_int / n)**2 * pmf_generic, (k_int, 1, n - 2))
E_M2 += ((n - 1) / n)**2 * (D2.subs(k, n - 1) - D2.subs(k, n - 2))
E_M2 += 1 * (1 - D2.subs(k, n - 1))
E_M2 = sp.simplify(sp.expand(E_M2))
print(f"  E[(M_n^(2))^2] [derived] = {sp.nsimplify(E_M2)}")
lim2 = sp.limit(E_M2, n, sp.oo)
print(f"  limit as n->oo = {lim2}   "
      f"{'OK (matches 1/3, Estagio 15/24)' if lim2 == sp.Rational(1, 3) else 'MISMATCH'}")
assert lim2 == sp.Rational(1, 3)

E_M3 = sp.summation((k_int / n)**3 * pmf_generic, (k_int, 1, n - 2))
E_M3 += ((n - 1) / n)**3 * (D2.subs(k, n - 1) - D2.subs(k, n - 2))
E_M3 += 1 * (1 - D2.subs(k, n - 1))
E_M3 = sp.simplify(sp.expand(E_M3))
print(f"  E[(M_n^(2))^3] [derived] = {sp.nsimplify(E_M3)}")
lim3 = sp.limit(E_M3, n, sp.oo)
print(f"  limit as n->oo = {lim3}")

# Independent computation of the K=2 continuum third moment directly
# from f_{M_2}(x) = 4x(1-x^2) (THEOREM.md Estagio 15, independently
# re-read this session), NOT from ATTEMPT.md's own transcription of it.
f_M2 = 4 * x * (1 - x**2)
E_M2_cont_3 = sp.integrate(x**3 * f_M2, (x, 0, 1))
print(f"  continuum E[M_2^3] = int_0^1 x^3 * 4x(1-x^2) dx "
      f"[independently integrated from THEOREM.md Estagio 15's density] "
      f"= {E_M2_cont_3}")
diff3 = sp.simplify(lim3 - E_M2_cont_3)
print(f"  diff (finite-n limit vs continuum) = {diff3}   "
      f"{'OK' if diff3 == 0 else 'MISMATCH'}")
assert diff3 == 0
assert E_M2_cont_3 == sp.Rational(8, 35)

print()
print("=" * 70)
print("Corollary D2.5: uniform convergence rate |F_n(x)-F_2(x)| <= 12/n")
print("=" * 70)
F2_cont = 1 - (1 - x**2)**2
F2_cont = sp.expand(F2_cont)
print(f"  Continuum CDF F_2(x) = 1-(1-x^2)^2 = {F2_cont}  "
      f"[from f_M2=4x(1-x^2), independently integrated]")
F2_check = sp.integrate(f_M2, (x, 0, x))
# sympy can't integrate to a variable upper bound directly this way;
# use a dummy symbol.
xi = sp.symbols('xi', positive=True)
F2_from_density = sp.integrate(f_M2.subs(x, xi), (xi, 0, x))
diff_F2 = sp.simplify(F2_from_density - F2_cont)
print(f"  F_2(x) via direct integration of the density = "
      f"{sp.expand(F2_from_density)}, diff vs 2x^2-x^4 form = {diff_F2}")
assert diff_F2 == 0

Fn = D2.subs(k, x * n)
gap = sp.cancel(Fn - F2_cont)
print(f"  F_n^(2)(x) - F_2(x) [k:=xn substituted into D2, sp.cancel] "
      f"= {gap}")

num, den = sp.fraction(gap)
num = sp.expand(num)
den = sp.expand(den)
print(f"  numerator N(n,x) = {num}")
print(f"  denominator = {den}")

claimed_N = -n * x**4 - n * x**2 + 2 * n * x + x**2 - 3 * x
claimed_den = n * (n - 1)
diff_num = sp.simplify(num - claimed_N)
diff_den = sp.simplify(den - claimed_den)
print(f"  claimed N(n,x) = {claimed_N}, diff = {diff_num}   "
      f"{'OK' if diff_num == 0 else 'MISMATCH'}")
print(f"  claimed denominator n(n-1) = {claimed_den}, diff = {diff_den}   "
      f"{'OK' if diff_den == 0 else 'MISMATCH'}")
assert diff_num == 0
assert diff_den == 0

# Verify |N(n,x)| <= 4n+4 on [0,1], n>=1, by the coefficient-sum bound
# claimed, PLUS an independent direct check via calculus (max over x of
# each n-power's coefficient polynomial in x, on [0,1]).
n1_coeff = sp.Poly(num, n).all_coeffs()  # highest degree first (degree 1 in n)
print(f"  N(n,x) as a polynomial in n: coeffs (n^1, n^0) = {n1_coeff}")
coeff_n1 = sp.expand(n1_coeff[0])  # coefficient of n^1
coeff_n0 = sp.expand(n1_coeff[1])  # coefficient of n^0
print(f"    coeff of n^1 (as poly in x) = {coeff_n1}")
print(f"    coeff of n^0 (as poly in x) = {coeff_n0}")


def max_abs_on_01(expr, sym):
    """Exact max of |expr| on [0,1] via calculus: critical points of expr
    (roots of derivative in (0,1)) plus endpoints 0,1."""
    crit = sp.solve(sp.diff(expr, sym), sym)
    candidates = [sp.Rational(0), sp.Rational(1)] + [c for c in crit if c.is_real and 0 <= c <= 1]
    vals = [sp.Abs(expr.subs(sym, c)) for c in candidates]
    return max(vals, key=lambda v: float(v))


max_n1 = max_abs_on_01(coeff_n1, x)
max_n0 = max_abs_on_01(coeff_n0, x)
print(f"  max|coeff_n1(x)| on [0,1] = {max_n1} (exact, via calculus)")
print(f"  max|coeff_n0(x)| on [0,1] = {max_n0} (exact, via calculus)")
print(f"  ATTEMPT.md's crude coefficient-sum bound claims both are "
      f"<= 4 -- checking directly:")
print(f"    max_n1 <= 4 ? {bool(max_n1 <= 4)}   "
      f"max_n0 <= 4 ? {bool(max_n0 <= 4)}")
assert max_n1 <= 4 and max_n0 <= 4

print(f"  => |N(n,x)| <= max_n1*n + max_n0 <= 4n + 4 for n>=1, x in "
      f"[0,1] -- CONFIRMED (independently, via exact calculus, not just "
      f"the coefficient-sum heuristic).")

# Now the arithmetic chain: |gap| = |N|/(n(n-1)) <= (4n+4)/(n(n-1)).
# Claimed: n(n-1) >= n^2/2 for n>=2, giving (4n+4)/(n^2/2) = 8/n+8/n^2
# <= 12/n using 8/n^2 <= 4/n for n>=2.
nn = sp.symbols('nn', integer=True, positive=True)
ineq1 = sp.simplify((nn * (nn - 1)) - nn**2 / 2)  # should be >=0 for n>=2
print()
print(f"  n(n-1) - n^2/2 = {ineq1} = n(n-2)/2 -- >=0 for n>=2? "
      f"checking n=2..20:")
for nv in range(2, 21):
    val = ineq1.subs(nn, nv)
    if val < 0:
        print(f"    FAIL at n={nv}: {val}")
        raise AssertionError("n(n-1)>=n^2/2 fails")
print("    OK for n=2..20 (and n(n-2)/2>=0 for all integer n>=2, trivially)")

bound1 = sp.simplify((4 * nn + 4) / (nn**2 / 2))
bound1 = sp.expand(bound1)
print(f"  (4n+4)/(n^2/2) = {bound1}")
bound2_check = sp.simplify(bound1 - sp.Rational(12, 1) / nn)
print(f"  (8/n+8/n^2) - 12/n = -4/n + 8/n^2 = {sp.simplify(sp.Rational(-4,1)/nn + sp.Rational(8,1)/nn**2)}")
print(f"  need -4/n+8/n^2 <= 0  <=>  n>=2 (equality at n=2) -- checking:")
for nv in range(2, 21):
    v = sp.Rational(-4, nv) + sp.Rational(8, nv**2)
    ok = v <= 0
    if not ok:
        print(f"    FAIL at n={nv}: {v}")
        raise AssertionError("8/n^2<=4/n fails for some n>=2")
print("    OK for n=2..20 (n=2 gives exact equality -4/2+8/4=-2+2=0, "
      "confirming the bound is tight there, not slack)")

print()
print("  Full inequality chain independently verified: for n>=2, "
      "x in [0,1]:")
print("    |F_n(x)-F_2(x)| = |N(n,x)|/(n(n-1)) <= (4n+4)/(n(n-1)) "
      "<= (4n+4)/(n^2/2) = 8/n+8/n^2 <= 12/n.")

# Sanity: also numerically scan a dense grid to make sure no accidental
# sign/off-by-one bug slipped through the symbolic algebra above.
import random
print()
print("  Numeric sanity scan: n=2..50, x on a dense grid, direct |gap| "
      "vs 12/n bound:")
worst_ratio = 0.0
rng = random.Random(20260923502)  # reserved sub-range, see report
gap_fn = sp.lambdify((n, x), gap, 'math')
for nv in range(2, 51):
    for i in range(200):
        xv = i / 199.0
        g = abs(gap_fn(nv, xv))
        bound = 12.0 / nv
        ratio = g / bound if bound > 0 else 0
        worst_ratio = max(worst_ratio, ratio)
        if g > bound + 1e-9:
            raise AssertionError(f"BOUND VIOLATED n={nv} x={xv}: gap={g} bound={bound}")
print(f"  worst observed |gap|/(12/n) ratio over the grid = "
      f"{worst_ratio:.4f} (<=1 required; comfortably inside)")
print("  No violation found. Corollary D2.5's bound holds on the scan.")

print()
print("ALL CHECKS PASSED.")
