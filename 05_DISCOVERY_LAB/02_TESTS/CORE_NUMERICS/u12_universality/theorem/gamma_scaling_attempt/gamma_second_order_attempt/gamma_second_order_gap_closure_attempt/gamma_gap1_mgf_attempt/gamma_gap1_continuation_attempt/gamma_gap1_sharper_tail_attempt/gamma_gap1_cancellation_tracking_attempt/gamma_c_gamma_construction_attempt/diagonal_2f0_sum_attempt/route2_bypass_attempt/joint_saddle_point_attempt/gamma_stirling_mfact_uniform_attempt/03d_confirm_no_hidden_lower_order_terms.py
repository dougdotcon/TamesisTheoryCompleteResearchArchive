#!/usr/bin/env python3
"""
Script 03d -- explicit confirmation that B(n,m,gamma) = ln F + ln I_leading
- ln T_prof, expanded in eps=1/sqrt(n) at m=lambda/eps, genuinely has ZERO
coefficient at every order eps^k for k<1 (not merely "not printed" by a
sympy series() call that might silently drop exact zeros without full
disclosure) -- and separately re-derive K(lambda,gamma) via sympy.limit
(a genuinely different code path than .series(), matching the referee-
grade cross-check discipline used throughout this lineage), to guard
against a bug specific to the .series() machinery itself.
"""
import sympy as sp
from sympy import symbols, sqrt, log, exp, pi, Rational, limit, oo, simplify

n, m, g, lam, eps = symbols('n m gamma lambda epsilon', positive=True)
t = symbols('t', positive=True)

tstar = (2*m + g*n - sp.sqrt(g**2*n**2 + 4*(1-g)*m**2)) / (2*g*(m+n))
g_of_t = m*log(t) + m*log(1-t) + (n-m)*log(1-g*t)
g_at_tstar = g_of_t.subs(t, tstar)
gpp = sp.diff(g_of_t, t, 2)
A_curv = -gpp.subs(t, tstar)

lnF = m*log(g/n) + sp.loggamma(n+m+2) - sp.loggamma(n-m+1) - sp.loggamma(m+1)
lnIlead = g_at_tstar + Rational(1,2)*log(2*pi) - Rational(1,2)*log(A_curv)
lnTprof = log(1/g) - ((2-g)/(2*g)) * lam**2

A_total = lnF + lnIlead
n_sub = 1/eps**2
m_sub = lam/eps
A_total_eps = A_total.subs([(n, n_sub), (m, m_sub)])
B_expr = A_total_eps - lnTprof

print("="*90)
print("PART A: explicit coefficient extraction at orders eps^-4 .. eps^1,")
print("via sympy.series with as_leading_term / coeff extraction (not just")
print("visual inspection of a truncated printout)")
print("="*90)

# Request a wider series and inspect the full polynomial-in-eps (after
# clearing any log(eps) pieces, which if present would show up as
# separate symbolic terms, not hidden).
ser = sp.series(B_expr, eps, 0, 2)
print("Full series object (repr, to catch any O() or log(eps) residue):")
print(" ", ser)
poly_part = ser.removeO()
poly_part = sp.expand(poly_part)
print()
print("Expanded polynomial-in-eps part:", poly_part)

# Extract coefficients at each power from -4 to 1 explicitly
coeffs = {}
for k in range(-4, 2):
    c = poly_part.coeff(eps, k)
    coeffs[k] = sp.simplify(c)
    print(f"  coefficient of eps^{k}: {coeffs[k]}")

assert all(coeffs[k] == 0 for k in range(-4, 1)), "NONZERO LOWER-ORDER TERM FOUND"
print()
print("CONFIRMED: coefficients of eps^-4, eps^-3, eps^-2, eps^-1, and eps^0")
print("are ALL exactly 0 (symbolic, exact) -- B(n,m,gamma) genuinely starts")
print("at eps^1, matching (and non-trivially re-confirming) the already-cited")
print("fact that T_prof(lambda,gamma) IS the correct leading-order limit,")
print("via a route (this front's own F+I_leading construction) independent")
print("of however the original T_prof derivation was internally organized.")

print()
print("="*90)
print("PART B: independent re-derivation of K(lambda,gamma) via sympy.limit")
print("(coefficient-by-order extraction), NOT via .series() -- a genuinely")
print("different code path, matching this lineage's own cross-check discipline")
print("="*90)

# K(lambda,gamma) = lim_{eps->0} B_expr / eps  (since B_expr = K*eps + O(eps^2))
K_via_limit = sp.limit(B_expr/eps, eps, 0)
K_via_limit = sp.simplify(K_via_limit)
print("K(lambda,gamma) via sympy.limit(B/eps, eps->0):")
print(" ", K_via_limit)

K_from_series = coeffs[1]
diff = sp.simplify(K_via_limit - K_from_series)
print("K(lambda,gamma) from series() coefficient extraction (Part A):")
print(" ", K_from_series)
print("Symbolic difference (should be exactly 0):", diff)
assert diff == 0
print("CONFIRMED: sympy.limit (independent code path) and sympy.series")
print("(Part A) give IDENTICAL K(lambda,gamma), matching the expected")
print("closed form 3*lambda/2 - lambda^3/6 - 1/(12*lambda) - lambda/gamma.")

expected = Rational(3,2)*lam - lam**3/6 - 1/(12*lam) - lam/g
print("Difference from the claimed closed form:", sp.simplify(K_via_limit - expected))
assert sp.simplify(K_via_limit - expected) == 0
print("EXACT MATCH to the claimed closed form K(lambda,gamma) confirmed.")
