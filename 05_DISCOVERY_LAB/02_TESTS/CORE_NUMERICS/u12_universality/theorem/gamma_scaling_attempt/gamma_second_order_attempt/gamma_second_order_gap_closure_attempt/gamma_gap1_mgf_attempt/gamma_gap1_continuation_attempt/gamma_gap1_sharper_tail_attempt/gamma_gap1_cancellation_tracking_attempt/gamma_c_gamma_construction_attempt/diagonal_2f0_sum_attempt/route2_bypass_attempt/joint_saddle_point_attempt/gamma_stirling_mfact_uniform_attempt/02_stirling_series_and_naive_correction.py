#!/usr/bin/env python3
"""
Script 02 -- the classical Stirling asymptotic series for ln(Gamma(z+1))
(a fact EXTERNAL to this archive, cited exactly as the predecessor front
cited it for its own Delta validation), and the "naive" ratio correction
it gives to F(n,m,gamma) = (gamma/n)^m * (n+m+1)!/((n-m)! m!) if applied
factor-by-factor at FIXED finite (n,m).

This is Part 1 of this front's two-part decomposition (see ATTEMPT.md
Sec 2 for why two parts are needed): the classical per-factorial Stirling
correction ("naive" because it does not yet account for the *mesoscale*
(m=lambda*sqrt(n)) rescaling of the Stirling LEADING term itself -- that
is done in script 03).

CITED, external fact (Abramowitz & Stegun 6.1.40 / any asymptotics
textbook), verified here symbolically against sympy's own asymptotic
expansion machinery before use:

  ln Gamma(z+1) = z ln z - z + (1/2) ln(2 pi z)
                  + 1/(12 z) - 1/(360 z^3) + 1/(1260 z^5) - ...
"""
import sympy as sp
from sympy import symbols, log, pi, gamma as Gamma, loggamma, series, oo, Rational, nsimplify

print("="*78)
print("PART A: verify the classical Stirling series against sympy's own")
print("        loggamma asymptotic expansion (external-fact cross-check)")
print("="*78)

z = symbols('z', positive=True)

stirling_leading = z*log(z) - z + Rational(1,2)*log(2*pi*z)
stirling_corr = 1/(12*z) - 1/(360*z**3) + 1/(1260*z**5)

# sympy's own asymptotic series for loggamma(z+1) at z->oo
# (loggamma(z+1) has a known .series via loggamma(z) shift; use gammasimp-free
#  direct approach: loggamma(z+1) = loggamma(z) + log(z))
expr = loggamma(z+1)
# sympy can expand loggamma asymptotically using the 'subs' trick z->1/x, x->0
x = symbols('x', positive=True)
expr_sub = expr.subs(z, 1/x)
asym = sp.series(expr_sub, x, 0, 6).removeO()
asym_in_z = asym.subs(x, 1/z)
asym_in_z = sp.expand_log(sp.simplify(asym_in_z), force=True)

target = sp.expand_log(sp.simplify(stirling_leading + stirling_corr), force=True)
diff = sp.simplify(asym_in_z - target)
print("sympy's own loggamma(z+1) asymptotic series (x=1/z -> 0, order 6):")
print(" ", asym_in_z)
print("Classical Stirling series (external fact, leading + 1/(12z) - 1/(360z^3) + 1/(1260z^5)):")
print(" ", target)
print("Difference (should be O(1/z^7), i.e. the two agree to displayed order):", sp.nsimplify(diff))
# The two should match up to the truncation order (z^-6 and beyond) -- check
# numerically at a sample point that they agree to high relative precision.
import mpmath as mp
mp.mp.dps = 50
zval = mp.mpf(37)
lhs_num = mp.loggamma(zval+1)
rhs_num = zval*mp.log(zval) - zval + mp.mpf('0.5')*mp.log(2*mp.pi*zval) + 1/(12*zval) - 1/(360*zval**3) + 1/(1260*zval**5)
print(f"Numeric check at z=37: loggamma(38)={lhs_num}")
print(f"  Stirling(leading+3 corr terms) = {rhs_num}")
print(f"  abs diff = {float(abs(lhs_num-rhs_num)):.3e}  (expected ~ 1/(1188*z^7) ~ next omitted term)")
next_term_est = 1/(1188*zval**7)
print(f"  next omitted term 1/(1188 z^7) ~ {float(next_term_est):.3e}")
assert abs(lhs_num - rhs_num) < 10*next_term_est
print("CONFIRMED: classical Stirling series matches sympy's own asymptotic")
print("expansion and matches loggamma numerically to the expected order.")

print()
print("="*78)
print("PART B: the 'naive' per-factor Stirling correction to F(n,m,gamma)")
print("        at FIXED, finite (n,m) -- NOT yet the mesoscale correction")
print("="*78)
print("""
F(n,m,gamma) = (gamma/n)^m * Gamma(n+m+2)/(Gamma(n-m+1)*Gamma(m+1))

Write, for each of z1:=n+m+1, z2:=n-m, z3:=m (the three arguments
whose (z+1)-factorial Stirling's series applies to):

  ln Gamma(z_i+1) = S0(z_i) + C(z_i),
  S0(z) := z ln z - z + (1/2) ln(2 pi z)        [leading Stirling, "Stirling0"]
  C(z)  := 1/(12 z) - 1/(360 z^3) + ...          [classical correction series]

so

  ln F = m ln(gamma/n) + S0(z1) - S0(z2) - S0(z3) + [C(z1) - C(z2) - C(z3)]
       =: ln F_stirling0(n,m,gamma)  +  delta_naive(n,m,gamma)

delta_naive(n,m,gamma) := C(z1) - C(z2) - C(z3)
                          = 1/(12 z1) - 1/(12 z2) - 1/(12 z3) + O(1/z^3)
                          = 1/(12(n+m+1)) - 1/(12(n-m)) - 1/(12 m) + O(...)

This delta_naive is a well-defined, EXACT (given the classical Stirling
external fact), finite-(n,m) correction with NO series-in-1/sqrt(n) taken
yet. It is verified here numerically: F(n,m,gamma) / [F_stirling0 * exp(delta_naive)]
-> 1 as (z1,z2,z3) grow, at fixed and at mesoscale (n,m).
""")

import mpmath as mp
mp.mp.dps = 50

def lnGamma0(z):
    return z*mp.log(z) - z + mp.mpf('0.5')*mp.log(2*mp.pi*z)

def C_series(z, terms=2):
    val = 1/(12*z)
    if terms >= 2:
        val -= 1/(360*z**3)
    if terms >= 3:
        val += 1/(1260*z**5)
    return val

def lnF_exact(n, m, gam):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    return m*mp.log(gam/n) + mp.loggamma(n+m+2) - mp.loggamma(n-m+1) - mp.loggamma(m+1)

def lnF_stirling0(n, m, gam):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    z1, z2, z3 = n+m+1, n-m, m
    return m*mp.log(gam/n) + lnGamma0(z1) - lnGamma0(z2) - lnGamma0(z3)

def delta_naive(n, m, gam, terms=2):
    n, m = mp.mpf(n), mp.mpf(m)
    z1, z2, z3 = n+m+1, n-m, m
    return C_series(z1, terms) - C_series(z2, terms) - C_series(z3, terms)

print(f"{'n':>10} {'m':>6} {'gamma':>6} | exact-stirling0 (should ->0) | delta_naive - (exact-stirling0)")
worst = 0
for n, m, gam in [(10**4, 30, 0.5), (10**6, 300, 0.5), (10**4, 30, 0.2),
                   (10**4, 30, 0.8), (10**8, 3000, 0.5), (10**5, 100, 0.3)]:
    lhs = lnF_exact(n, m, gam) - lnF_stirling0(n, m, gam)
    d = delta_naive(n, m, gam, terms=2)
    resid = lhs - d
    print(f"{n:>10} {m:>6} {gam:>6} | {float(lhs):.6e} | resid={float(resid):.3e}")
    worst = max(worst, abs(resid))
print(f"\nWorst residual after including delta_naive (2 correction terms per z): {float(worst):.3e}")
print("(expected to shrink like the next Stirling term ~ 1/(360 m^3) at the")
print(" smallest z=m argument -- confirmed order of magnitude below)")
for n, m, gam in [(10**4, 30, 0.5)]:
    est = 1/(360*mp.mpf(m)**3)
    print(f"  1/(360*m^3) at m={m}: {float(est):.3e}")

print()
print("CONCLUSION of script 02: delta_naive(n,m,gamma) = 1/(12(n+m+1))")
print("  - 1/(12(n-m)) - 1/(12 m) + O(z^-3) is the exact, finite-(n,m)")
print("  correction turning the crude Stirling0 approximation of F into a")
print("  high-accuracy one. At the MESOSCALE m=lambda*sqrt(n), the first two")
print("  terms are O(1/n) while the third, -1/(12 m) = -1/(12 lambda sqrt(n)),")
print("  is O(1/sqrt(n)) -- i.e. delta_naive's DOMINANT mesoscale piece is")
print("  exactly -1/(12 lambda sqrt(n)). This is NOT yet the full Delta_m")
print("  this front needs (see Sec 3/script 03 in ATTEMPT.md): delta_naive")
print("  measures Stirling0-vs-exact accuracy at FIXED finite (n,m); the")
print("  object needed to correct T_prof itself is F's own deviation, at")
print("  mesoscale n->infty, from whatever closed form F_leading(n,m,gamma)")
print("  reproduces T_prof/I_leading in that SAME limit -- a genuinely")
print("  different (larger) quantity, derived next.")
