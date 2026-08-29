"""
Independent referee re-derivation and verification of ATTEMPT.md Section 4's
saddle-point scaling law claim:
    Exact crossing condition: (j*+m+1)(n-j*-m) / [(j*+1)(n-j*)] * (1-gamma) = 1
    Claimed asymptotic:       j* ~ m*(1-gamma)/gamma   as m,n -> infinity, m=o(n)

We:
 (1) Re-derive the crossing condition from scratch via sympy (ratio of
     consecutive summand terms), independent of the target's script.
 (2) Cross-validate j* via BRUTE-FORCE ARGMAX of the summand (not the
     ratio test) at several (n,m,gamma) -- a genuinely different method
     than the target's ratio-walk, to rule out an off-by-one/ratio-logic
     bug being silently self-consistent.
 (3) Independently re-derive the leading asymptotic j* ~ m(1-g)/g via
     sympy limit computation on the EXACT crossing condition (solving for
     the ratio j/m as m,n -> infinity together, m=o(n)), not just the
     hand-wavy "drop O(1) shifts" argument.
 (4) Extend the numerical convergence check to a DISJOINT (n,m,gamma) grid
     from target's script 05, and quantify the subleading correction rate.
"""
from fractions import Fraction as F
import sympy as sp

def summand(n, m, j, g):
    from math import comb
    return comb(j + m, m) * comb(n - j, m) * (1 - g) ** j

def find_jstar_by_ratio(n, m, g):
    """Same idea as target's script 05 (ratio walk) -- own implementation."""
    j = 0
    while j <= n - m - 1:
        ratio = F(j + m + 1, j + 1) * F(n - j - m, n - j) * (1 - g)
        if ratio <= 1:
            break
        j += 1
    return j

def find_jstar_by_argmax(n, m, g):
    """Genuinely different method: brute-force scan the summand values
    (exact Fraction) and take argmax directly -- no ratio logic at all."""
    best_j, best_val = 0, F(0)
    for j in range(0, n - m + 1):
        val = summand(n, m, j, g)
        if val > best_val:
            best_val = val
            best_j = j
    return best_j

print("="*70)
print("(1) Symbolic re-derivation of the crossing condition from scratch")
print("="*70)
j, n, m, g = sp.symbols('j n m g')
from sympy import binomial
tj = binomial(j+m, m) * binomial(n-j, m) * (1-g)**j
tj1 = tj.subs(j, j+1)
ratio = sp.factor(sp.simplify(tj1/tj))
print("ratio(j) = t_{j+1}/t_j =", ratio)
# claimed crossing condition (from ATTEMPT.md):
claimed = sp.factor(((j+m+1)*(n-j-m)) / ((j+1)*(n-j)) * (1-g))
diff = sp.simplify(ratio - claimed)
print("difference vs ATTEMPT.md's stated crossing-condition LHS:", diff)
assert diff == 0
print("CONFIRMED: the crossing-condition expression in ATTEMPT.md Sec.4 is")
print("exactly the term ratio t_{j+1}/t_j -- an accurate restatement, not")
print("an unjustified assertion.")

print()
print("="*70)
print("(2) Cross-validate j* via brute-force ARGMAX (different method) vs")
print("    the ratio-walk method, at a range of (n,m,gamma) NOT identical")
print("    to target's script 03/05 grids")
print("="*70)
mism = 0; tot = 0
for n_val in [50, 137, 300, 521]:
    for m_val in [3, 7, 15]:
        if m_val > n_val:
            continue
        for g_num, g_den in [(1,3), (2,5), (3,4), (1,10)]:
            g_val = F(g_num, g_den)
            j1 = find_jstar_by_ratio(n_val, m_val, g_val)
            j2 = find_jstar_by_argmax(n_val, m_val, g_val)
            tot += 1
            if j1 != j2:
                mism += 1
                print(f"  MISMATCH n={n_val} m={m_val} g={g_val}: ratio-walk={j1} argmax={j2}")
print(f"{tot} checks, {mism} mismatches between ratio-walk and brute-force argmax")
assert mism == 0
print("CONFIRMED: the ratio-walk locator used by the target is not just")
print("self-consistent -- it agrees with an entirely different (brute-force")
print("argmax) computation of the same j*, everywhere tested.")

print()
print("="*70)
print("(3) Independent asymptotic derivation via sympy: solve the crossing")
print("    condition for the leading behavior of j as m,n->oo with n->oo")
print("    fastest (m=o(n)), then m,j->oo together.")
print("="*70)
# Take crossing condition ((j+m+1)(n-j-m))/((j+1)(n-j)) * (1-g) = 1
# Step 1: let n -> infinity at fixed j,m first (this isolates the m=o(n) limit)
lhs = ((j+m+1)*(n-j-m)) / ((j+1)*(n-j)) * (1-g)
lhs_n_to_inf = sp.limit(lhs, n, sp.oo)
print("Taking n->oo at fixed j,m (isolates the (n-j-m)/(n-j)->1 factor):")
print("  limit =", lhs_n_to_inf)
# This should be (j+m+1)/(j+1) * (1-g)
expected_after_n_limit = (j+m+1)/(j+1)*(1-g)
assert sp.simplify(lhs_n_to_inf - expected_after_n_limit) == 0
print("  matches (j+m+1)/(j+1)*(1-g) exactly, confirming the n->oo step of")
print("  ATTEMPT.md's derivation.")
print()
print("Step 2: setting this equal to 1 and solving for j in terms of m:")
eq = sp.Eq(expected_after_n_limit, 1)
sol = sp.solve(eq, j)
print("  exact solution j =", sol)
j_exact_finite_n_removed = sol[0]
j_exact_simplified = sp.simplify(j_exact_finite_n_removed)
print("  simplified:", j_exact_simplified)
print()
print("Step 3: leading behavior as m -> infinity of this exact j(m):")
leading = sp.limit(j_exact_simplified/m, m, sp.oo)
print("  lim_{m->oo} j(m)/m =", leading)
predicted = (1-g)/g
diff2 = sp.simplify(leading - predicted)
print("  ATTEMPT.md's claimed limit (1-g)/g:", predicted, " difference:", diff2)
assert diff2 == 0
print("CONFIRMED INDEPENDENTLY (fully symbolic, sympy limit -- not just the")
print("informal 'drop O(1) shifts' argument in the prose): j*/m -> (1-g)/g")
print("as m->infinity (after first sending n->infinity / m=o(n)), i.e.")
print("j* ~ m(1-gamma)/gamma is a mathematically correct leading-order")
print("asymptotic of the EXACT discrete crossing condition.")

print()
print("="*70)
print("(4) Independent numeric convergence check, DISJOINT grid from target's")
print("    script 05 (target: n in {4e3,4e4,4e5,4e6}, m in {20,63,200,632},")
print("    m/sqrt(n) ~ 0.316 fixed). Here: m/sqrt(n) ~ 0.5 fixed, different")
print("    gamma set, to see if the same asymptotic law and rate hold.")
print("="*70)
import math
for g_num, g_den in [(2,3), (1,4), (7,10)]:
    g_val = F(g_num, g_den)
    predicted = float((1-g_val)/g_val)
    print(f"gamma={g_val} (predicted (1-g)/g = {predicted:.6f})")
    for n_val in [10_000, 100_000, 1_000_000, 10_000_000]:
        m_val = int(round(0.5*math.sqrt(n_val)))
        jstar = find_jstar_by_ratio(n_val, m_val, g_val)
        ratio_val = jstar/m_val
        rel_dev = abs(ratio_val-predicted)/predicted*100
        print(f"   n={n_val:>9d} m={m_val:>5d} (m/n={m_val/n_val:.6f}): j*={jstar:>7d} "
              f"j*/m={ratio_val:.6f}  rel.dev={rel_dev:.4f}%  "
              f"(m/n * const = {m_val/n_val*100*10:.4f} for comparison)")
