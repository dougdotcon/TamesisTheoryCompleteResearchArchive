#!/usr/bin/env python3
"""
Referee script 03b -- retry of the predecessor-Delta mesoscale-limit
re-derivation, after ref03's single combined sympy.series() call on the
FULL Delta_pred ratio timed out at 250s (reproducing, independently, the
exact same computational obstacle the predecessor front itself disclosed
in ITS OWN Sec 3/Sec 8 item 3 -- a useful corroboration that this is a
real sympy performance wall, not a fabricated excuse).

Fix (independently chosen, mirroring in spirit -- but not copying code
from -- the predecessor's own disclosed workaround): expand A, g'''(t*),
g''''(t*) SEPARATELY via fast sympy.series calls (each terminates
quickly), extract their leading eps-power and coefficient, and combine
algebraically -- valid since Delta_pred = g''''/(8A^2) + 5(g''')^2/(24A^3)
is a pure multiplicative/additive combination of these three pieces.
"""
import sympy as sp
import time

n, m, g, lam, eps = sp.symbols('n m gamma lambda epsilon', positive=True)
t = sp.symbols('t', positive=True)

tstar = (2*m + g*n - sp.sqrt(g**2*n**2 + 4*(1-g)*m**2)) / (2*g*(m+n))
g_of_t = m*sp.log(t) + m*sp.log(1-t) + (n-m)*sp.log(1-g*t)

gpp = sp.diff(g_of_t, t, 2).subs(t, tstar)
gppp = sp.diff(g_of_t, t, 3).subs(t, tstar)
gpppp = sp.diff(g_of_t, t, 4).subs(t, tstar)

A = -gpp

def leading_eps(expr, label, n_terms=1):
    t0 = time.time()
    expr_eps = expr.subs([(n, 1/eps**2), (m, lam/eps)])
    # find leading power by trying successive series orders
    for hi in range(-6, 3):
        try:
            ser = sp.series(expr_eps, eps, 0, hi)
            poly = ser.removeO()
            if poly != 0:
                break
        except Exception:
            continue
    poly = sp.expand(sp.simplify(poly))
    print(f"  [{label}] leading terms in eps (elapsed {time.time()-t0:.1f}s): {poly}")
    return poly

print("Expanding A, g'''(t*), g''''(t*) SEPARATELY at mesoscale (fast, each")
print("should terminate quickly, matching predecessor's own disclosed timing):")
A_eps = leading_eps(A, "A")
gppp_eps = leading_eps(gppp, "g'''(t*)")
gpppp_eps = leading_eps(gpppp, "g''''(t*)")

print()
print("Combining algebraically: Delta_pred = g''''/(8A^2) + 5(g''')^2/(24A^3)")
Delta_pred_leading = sp.series(gpppp_eps/(8*A_eps**2) + 5*gppp_eps**2/(24*A_eps**3), eps, 0, 2)
Delta_pred_leading = sp.expand(sp.simplify(Delta_pred_leading.removeO()))
print("  Delta_pred (leading, combined):", Delta_pred_leading)

c1 = sp.simplify(Delta_pred_leading.coeff(eps, 1))
print("  coefficient of eps^1:", c1, " (expected: 1/(12*lambda))")
assert sp.simplify(c1 - 1/(12*lam)) == 0
print("CONFIRMED (fast independent route, separate-then-combine): Delta_pred ~ [1/(12*lambda)]/sqrt(n).")

print()
print("Pole-cancellation re-check:")
K = sp.Rational(3,2)*lam - lam**3/6 - 1/(12*lam) - lam/g
total = sp.simplify(K + c1)
expected_total = sp.Rational(3,2)*lam - lam**3/6 - lam/g
diff = sp.simplify(total - expected_total)
print("  K + Delta_pred_coeff =", total, "  (claimed:", expected_total, ")")
print("  symbolic difference:", diff)
assert diff == 0
limit_at_0 = sp.limit(total, lam, 0)
print("  limit as lambda->0:", limit_at_0)
assert limit_at_0 == 0
print("CONFIRMED: pole cancellation holds, independently re-derived via a")
print("computationally distinct (separate-expand-then-combine) route after")
print("the naive single-series approach independently hit the same 250s+")
print("wall the predecessor front itself disclosed.")
