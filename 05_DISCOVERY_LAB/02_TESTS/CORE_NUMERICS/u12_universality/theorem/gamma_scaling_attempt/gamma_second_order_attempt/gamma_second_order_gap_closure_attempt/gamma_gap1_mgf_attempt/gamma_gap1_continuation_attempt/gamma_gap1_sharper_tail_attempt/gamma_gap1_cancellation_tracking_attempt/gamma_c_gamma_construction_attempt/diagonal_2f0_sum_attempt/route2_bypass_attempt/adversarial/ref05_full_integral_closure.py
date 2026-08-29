"""
Push the Pfaff-fix (ref04) through to a genuinely usable CLOSED-FORM
integral representation for T(n,m), and verify it end-to-end against
the exact finite sum. This goes beyond what the target's own front
attempted (they named the Pfaff idea but did not carry it through) --
purely for OUR OWN assessment of whether it is a red herring or a real
lead, per the dispatch mandate item (d). Not claimed as part of the
target's own contribution -- an independent extension by this review.

Derivation (worked by hand from the three already-verified pieces --
ref04's Pfaff identity DLMF 15.8.7, and Euler's integral applied to the
transformed series with new_c=2m+2):

  T(n,m) = C(n,m) * 2F1(-(n-m), m+1; -n; 1-g)                      [original identity, script 02 / ref01]
         = C(n,m) * (c-b)_N/(c)_N * 2F1(-N, m+1; 2m+2; g)          [DLMF 15.8.7, N=n-m, c=-n, b=m+1; ref04]
         = C(n,m) * [(n+m+1)! m! / ((2m+1)! n!)] * 2F1(-N,m+1;2m+2;g)
              [using (c-b)_N = (-(n+m+1))_N = (-1)^N (n+m+1)!/(2m+1)!,
               (c)_N = (-n)_N = (-1)^N n!/m!  -- exact Pochhammer-to-
               factorial identities, verified below]
         = C(n,m) * [(n+m+1)! m! / ((2m+1)! n!)] *
             [(2m+1)!/(m!)^2] * Integral_0^1 t^m(1-t)^m(1-g t)^N dt
              [Euler's integral, valid since new_c=2m+2 > b=m+1 > 0]
         = [(n+m+1)! / ((n-m)! (m!)^2)] * Integral_0^1 t^m(1-t)^m(1-g t)^(n-m) dt
         = C(n+m+1, 2m+1) * (2m+1)!/(m!)^2 * Integral_0^1 t^m(1-t)^m(1-g t)^(n-m) dt
         = C(n+m+1, 2m+1) * E_{t~Beta(m+1,m+1)}[ (1-g t)^(n-m) ]
              [since (2m+1)!/(m!)^2 = 1/B(m+1,m+1), the Beta(m+1,m+1)
               normalizing constant]

This FINAL closed form is verified end-to-end below.
"""
import sympy as sp
import mpmath as mp
from fractions import Fraction as F
from math import comb

mp.mp.dps = 50

print("="*70)
print("(0) Verify the Pochhammer-to-factorial identities used by hand,")
print("    symbolically, for general n,m (N=n-m)")
print("="*70)
n_s, m_s = sp.symbols('n m', positive=True, integer=True)
N_s = n_s - m_s
# (c-b)_N with c=-n,b=m+1: (-(n+m+1))_N should equal (-1)^N (n+m+1)!/(2m+1)!
lhs1 = sp.rf(-(n_s+m_s+1), N_s)
rhs1 = (-1)**N_s * sp.factorial(n_s+m_s+1)/sp.factorial(2*m_s+1)
# check numerically at several small (n,m) since symbolic RisingFactorial
# simplification with symbolic N is unreliable in general
mism = 0
for nv in [4,6,9,12]:
    for mv in [0,1,2,4]:
        if mv > nv: continue
        Nv = nv-mv
        l = sp.rf(-(nv+mv+1), Nv)
        r = (-1)**Nv * sp.factorial(nv+mv+1)/sp.factorial(2*mv+1)
        if sp.simplify(l-r) != 0:
            mism += 1
            print(f"  MISMATCH (c-b)_N check at n={nv},m={mv}: {l} vs {r}")
print(f"(c-b)_N = (-1)^N (n+m+1)!/(2m+1)! : checked at 4x4 grid, {mism} mismatches")
assert mism == 0

mism = 0
for nv in [4,6,9,12]:
    for mv in [0,1,2,4]:
        if mv > nv: continue
        Nv = nv-mv
        l = sp.rf(-nv, Nv)
        r = (-1)**Nv * sp.factorial(nv)/sp.factorial(mv)
        if sp.simplify(l-r) != 0:
            mism += 1
            print(f"  MISMATCH (c)_N check at n={nv},m={mv}: {l} vs {r}")
print(f"(c)_N = (-1)^N n!/m! : checked at 4x4 grid, {mism} mismatches")
assert mism == 0
print("Both hand-derivation steps confirmed exact.")

print()
print("="*70)
print("(1) FINAL closed form, end-to-end numeric verification (mpmath dps=50)")
print("    T(n,m) =?= C(n+m+1,2m+1) * (2m+1)!/(m!)^2 *")
print("               Integral_0^1 t^m (1-t)^m (1-g t)^(n-m) dt")
print("="*70)

def T_nm_fraction(n, m, g):
    total = F(0)
    for j in range(0, n - m + 1):
        total += comb(j + m, m) * comb(n - j, m) * ((1 - g) ** j)
    return total

max_rel_err = mp.mpf(0)
tests = [(5,0),(5,1),(5,2),(5,4),(20,4),(30,7),(50,0),(12,6),(8,3),(15,5)]
n_checks = 0
for n_val, m_val in tests:
    if m_val > n_val:
        continue
    N_val = n_val - m_val
    for g_num, g_den in [(1, 3), (3, 10), (1, 2), (4, 5)]:
        g_val = mp.mpf(g_num) / mp.mpf(g_den)
        exact = T_nm_fraction(n_val, m_val, F(g_num, g_den))
        exact_mp = mp.mpf(exact.numerator) / mp.mpf(exact.denominator)

        Cnorm = mp.binomial(n_val + m_val + 1, 2 * m_val + 1)
        beta_pref = mp.factorial(2 * m_val + 1) / (mp.factorial(m_val) ** 2)
        integrand = lambda t: t ** m_val * (1 - t) ** m_val * (1 - g_val * t) ** N_val
        integral_val = mp.quad(integrand, [0, 1])
        predicted = Cnorm * beta_pref * integral_val

        rel_err = abs(predicted - exact_mp) / abs(exact_mp)
        max_rel_err = max(max_rel_err, rel_err)
        n_checks += 1

print(f"Checked {n_checks} (n,m,gamma) triples.")
print(f"Max relative error: {mp.nstr(max_rel_err, 10)}")
assert max_rel_err < mp.mpf('1e-45'), "CLOSED FORM FAILED verification"
print()
print("CONFIRMED to full quadrature precision (<1e-45 relative error):")
print()
print("  T(n,m) = C(n+m+1, 2m+1) * E_{t~Beta(m+1,m+1)}[ (1-gamma*t)^(n-m) ]")
print()
print("This is a genuine, previously-unwritten (by the target) usable")
print("closed-form integral representation. The integrand t^m(1-t)^m is")
print("(up to normalization) EXACTLY the Beta(m+1,m+1) density -- the")
print("CONTINUUM analogue of the median order-statistic distribution the")
print("target independently found in Sec.3! This ties the target's Sec.2")
print("(2F1) and Sec.3 (order statistic) findings into a single coherent")
print("object via the Pfaff-type fix they named but did not execute --")
print("substantiating that it is a genuinely promising, not a red-herring,")
print("next step, and handing a future front a clean, classical Beta-type")
print("integral (ready for Watson's-lemma/Laplace analysis) in place of")
print("raw Pochhammer-sum manipulation. This does NOT by itself close")
print("C(gamma) -- the coupled outer m-sum Laplace analysis (target's own")
print("Sec.5) is still required -- but it is a concrete, verified partial")
print("advance beyond what the target itself reached on this specific")
print("named-but-unexecuted next step.")
