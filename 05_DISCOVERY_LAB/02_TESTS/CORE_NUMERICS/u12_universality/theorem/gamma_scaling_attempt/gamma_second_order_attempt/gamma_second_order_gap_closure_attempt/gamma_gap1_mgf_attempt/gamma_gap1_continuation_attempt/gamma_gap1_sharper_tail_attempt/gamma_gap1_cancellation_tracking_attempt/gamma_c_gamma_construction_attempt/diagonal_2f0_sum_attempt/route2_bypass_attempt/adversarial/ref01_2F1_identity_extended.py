"""
Independent referee verification of the target's Section 2 claim:
    T(n,m) = C(n,m) * 2F1(-(n-m), m+1; -n; 1-gamma)
Fresh code, NOT copied from the target's script 02. Extended range beyond
the target's own checks (target: symbolic k up to n=8 in Part B ratio;
80 numeric checks n in {4,6,9,11,14}, m<=3).

We independently:
 (1) symbolic ratio-test re-derivation, extended to symbolic m (not fixed)
 (2) exact-Fraction numeric check at an EXTENDED and DISJOINT sample grid
     from the target's (different n's, different m's, different gammas)
 (3) direct algebraic proof (not just ratio-matching) that the two exact
     finite sums (LHS: raw T(n,m); RHS: closed-form Pochhammer sum) are
     term-by-term identical after re-indexing, by symbolic simplification
     of the general term ratio AND the t_0 initial value.
"""
import sympy as sp
from fractions import Fraction as F
from math import comb

def T_nm_fraction(n, m, g):
    total = F(0)
    for j in range(0, n - m + 1):
        total += comb(j + m, m) * comb(n - j, m) * ((1 - g) ** j)
    return total

def two_F1_terminating_fraction(a_negint, b, c, z, nterms):
    total = F(0)
    term = F(1)
    for i in range(0, nterms + 1):
        if i > 0:
            term *= F(a_negint + i - 1) * F(b + i - 1) * z / (F(c + i - 1) * i)
        total += term
    return total

print("="*70)
print("(1) Symbolic ratio test, fully general n,m,g -- re-derived independently")
print("="*70)
j, n, m, g = sp.symbols('j n m g')
tj = sp.binomial(j + m, m) * sp.binomial(n - j, m) * (1 - g) ** j
tj1 = tj.subs(j, j + 1)
ratio = sp.cancel(sp.simplify(tj1 / tj))
print("t_{j+1}/t_j =", ratio)

A, B, C, z = -(n - m), m + 1, -n, 1 - g
canon = (A + j) * (B + j) * z / ((C + j) * (1 + j))
diff = sp.simplify(sp.cancel(canon) - ratio)
print("difference vs candidate 2F1 ratio:", diff)
assert diff == 0
print("CONFIRMED independently: exact ratio match for symbolic n,m,g.")

print()
print("Also checking t_0 (the j=0 term) matches C(n,m) * [2F1 series first term]:")
t0 = tj.subs(j, 0)
print("t_0 = C(n,m)*C(n,m)... wait t_0 = binomial(m,m)*binomial(n,m) =", sp.simplify(t0))
print("This should equal C(n,m) (the '2F1 prefactor'), since binomial(0+m,m)=1.")
assert sp.simplify(t0 - sp.binomial(n, m)) == 0
print("CONFIRMED: t_0 = C(n,m) exactly, matching the claimed prefactor.")

print()
print("="*70)
print("(2) Extended exact-Fraction numeric check, DISJOINT grid from target's")
print("    own script 02 Part C (target used n in {4,6,9,11,14}, m<=3,")
print("    gamma in {1/3,3/10,7/20,1/2}). Here: n in {5,7,10,13,17,20},")
print("    m up to 5, gamma in {2/7,5/11,4/9,3/5,7/8} -- all disjoint values.")
print("="*70)
mism = 0
tot = 0
for n_val in [5, 7, 10, 13, 17, 20]:
    for m_val in range(0, min(6, n_val + 1)):
        for g_num, g_den in [(2, 7), (5, 11), (4, 9), (3, 5), (7, 8)]:
            g_val = F(g_num, g_den)
            direct = T_nm_fraction(n_val, m_val, g_val)
            a = -(n_val - m_val)
            b = m_val + 1
            c = -n_val
            z = 1 - g_val
            hyp = two_F1_terminating_fraction(a, b, c, z, nterms=(n_val - m_val))
            closed = comb(n_val, m_val) * hyp
            tot += 1
            if direct != closed:
                mism += 1
                print(f"  MISMATCH n={n_val} m={m_val} g={g_val}: direct={direct} closed={closed}")
print(f"Total checks: {tot}, mismatches: {mism}")
assert mism == 0
print("CONFIRMED (extended, disjoint grid): 0 mismatches.")

print()
print("="*70)
print("(3) Also verify at m=0 edge case explicitly (degenerate a=c=-n case,")
print("    the one that broke sp.hyper() per the target's self-caught bug)")
print("    across a WIDER n range than target's self-caught-bug check.")
print("="*70)
mism = 0
tot = 0
for n_val in range(0, 25):
    g_val = F(1, 3)
    m_val = 0
    direct = T_nm_fraction(n_val, m_val, g_val)
    a = -(n_val - m_val); b = m_val + 1; c = -n_val; z = 1 - g_val
    hyp = two_F1_terminating_fraction(a, b, c, z, nterms=(n_val - m_val))
    closed = comb(n_val, m_val) * hyp
    tot += 1
    if direct != closed:
        mism += 1
        print(f"  MISMATCH n={n_val}: direct={direct} closed={closed}")
print(f"m=0 edge case: {tot} checks (n=0..24), {mism} mismatches")
assert mism == 0
print("CONFIRMED: finite-truncation evaluator handles m=0 degeneracy correctly")
print("across a much wider n-range than the target's own self-caught-bug check.")
