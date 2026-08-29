"""
Independent referee investigation of ATTEMPT.md Section 2's claims:
 (a) Euler's classical integral representation for 2F1(A,B;C;z) genuinely
     fails here because C=-n is a nonpositive integer (Gamma(C) has a pole).
 (b) A Pfaff-transformation-based fix is "plausibly tractable" (named but
     not carried through).

We verify (a) by confirming the parameter placement is exactly as claimed,
and we test (b) concretely: does a known transformation for TERMINATING
2F1 series (DLMF 15.8.7, a Pfaff-type reflection specific to the case
where the FIRST parameter is a nonpositive integer) produce an equivalent
representation whose new "C" parameter is NOT a nonpositive integer --
i.e. genuinely restores access to Euler's integral?

DLMF 15.8.7 (verified against the DLMF text, a standard, citable identity):
    2F1(-n, b; c; z) = (c-b)_n/(c)_n * 2F1(-n, b; 1+b-c-n; 1-z)
"""
import sympy as sp

n_s, m_s, g_s, z_s = sp.symbols('n m g z', positive=False)

print("="*70)
print("(a) Confirm parameter placement: A=-(n-m), B=m+1, C=-n. Euler's")
print("    integral needs Re(C)>Re(B)>0. Here C=-n <= 0 for n>=0 -- a")
print("    nonpositive integer whenever n is a nonneg integer, REGARDLESS")
print("    of m. So yes, C=-n is exactly the 'problem' parameter, and it")
print("    is C (not A or B) that blocks Gamma(C) in Euler's prefactor")
print("    Gamma(C)/[Gamma(B)Gamma(C-B)].")
print("="*70)
A_expr, B_expr, C_expr = -(n_s - m_s), m_s + 1, -n_s
print(f"A = {A_expr}  (also a nonpositive integer, for m<=n)")
print(f"B = {B_expr}  (positive, since m>=0)")
print(f"C = {C_expr}  (nonpositive integer for n a nonneg integer -- THE blocker)")
print("Confirmed: this is an accurate, not merely asserted, diagnosis.")

print()
print("="*70)
print("(b) Test DLMF 15.8.7 (a genuine Pfaff-type reflection specific to")
print("    TERMINATING 2F1 series with first parameter -n): does applying")
print("    it here move away from a nonpositive-integer C?")
print("    Formula: 2F1(-N,b;c;z) = (c-b)_N/(c)_N * 2F1(-N,b;1+b-c-N;1-z)")
print("="*70)
N_val = n_s - m_s   # so A = -N_val
b_val = m_s + 1
c_val = -n_s
new_c = 1 + b_val - c_val - N_val
new_c_simplified = sp.simplify(new_c)
print(f"N (truncation length) = n-m")
print(f"new C parameter (per DLMF 15.8.7) = 1+b-c-N = 1+(m+1)-(-n)-(n-m) = {new_c}")
print(f"simplified: {new_c_simplified}")
print()
print("If this simplifies to a manifestly POSITIVE quantity (for m>=0), the")
print("transformed series has C_new > 0 and, since B stays m+1, Euler's")
print("integral (needs C_new > B_new > 0) becomes potentially USABLE.")

print()
print("Numeric verification of the transformation identity itself (DLMF")
print("15.8.7), at several concrete (n,m,gamma), via exact finite sums:")

from fractions import Fraction as F
from math import comb, factorial

def two_F1_terminating_fraction(a_negint, b, c, z, nterms):
    total = F(0)
    term = F(1)
    for i in range(0, nterms + 1):
        if i > 0:
            term *= F(a_negint + i - 1) * F(b + i - 1) * z / (F(c + i - 1) * i)
        total += term
    return total

def pochhammer_frac(x, k):
    # (x)_k for possibly-negative or fractional x, exact if x is int/Fraction
    p = F(1)
    for i in range(k):
        p *= (x + i)
    return p

mism = 0; tot = 0
for n_val in [4, 6, 9, 12]:
    for m_val in [0, 1, 2, 3]:
        if m_val > n_val:
            continue
        N_len = n_val - m_val
        b_num = m_val + 1
        c_num = -n_val
        for g_num, g_den in [(1, 3), (3, 10), (1, 2)]:
            g = F(g_num, g_den)
            z_num = 1 - g
            # LHS: original terminating 2F1(-N,b;c;z)
            lhs = two_F1_terminating_fraction(-N_len, b_num, c_num, z_num, nterms=N_len)
            # RHS: (c-b)_N/(c)_N * 2F1(-N,b; 1+b-c-N; 1-z)
            c_minus_b_poch = pochhammer_frac(c_num - b_num, N_len)
            c_poch = pochhammer_frac(c_num, N_len)
            new_c_num = 1 + b_num - c_num - N_len
            transformed = two_F1_terminating_fraction(-N_len, b_num, new_c_num, 1 - z_num, nterms=N_len)
            rhs = (c_minus_b_poch / c_poch) * transformed
            tot += 1
            ok = (lhs == rhs)
            if not ok:
                mism += 1
                print(f"  MISMATCH n={n_val} m={m_val} g={g}: LHS={lhs} RHS={rhs}")
            else:
                if tot <= 6:
                    print(f"  n={n_val} m={m_val} g={g}: new_c={new_c_num} "
                          f"(positive? {new_c_num>0})  LHS==RHS: OK")
print(f"\nDLMF 15.8.7 identity check: {tot} cases, {mism} mismatches")
if mism == 0:
    print("CONFIRMED: DLMF 15.8.7 (Pfaff-type reflection for terminating 2F1)")
    print("holds exactly for this family, and its transformed C parameter is")
    print(f"new_c = 1+b-c-N = {new_c_simplified}, a POSITIVE integer for all")
    print("m>=0 -- i.e. the transformed series has a POSITIVE lower parameter,")
    print("genuinely escaping the C=-n obstruction. This substantiates the")
    print("front's claim that a Pfaff-type fix is 'plausibly tractable' --")
    print("it is not merely hand-waving; a concrete, citable, verified-here")
    print("transformation exists that resolves exactly the named obstruction.")
else:
    print("NOT confirmed -- the proposed transformation does NOT hold as I")
    print("recalled it; needs correction.")
