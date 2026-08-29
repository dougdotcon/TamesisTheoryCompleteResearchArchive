#!/usr/bin/env python3
"""
Script 03c -- symbolic simplification/combination of Delta_m with the
CITED predecessor Delta, and a couple of algebraic sanity checks.
"""
import sympy as sp
from sympy import symbols, Rational, simplify, nsimplify, factor

lam, g = symbols('lambda gamma', positive=True)

K = -lam**3/6 + Rational(3,2)*lam - 1/(12*lam) - lam/g     # Delta_m's coefficient
Delta_pred_coeff = 1/(12*lam)                               # predecessor's Delta coefficient (CITED)

total = sp.simplify(K + Delta_pred_coeff)
print("Delta_m coefficient K(lambda,gamma)      =", K)
print("predecessor Delta coefficient (CITED)    =", Delta_pred_coeff)
print("SUM (Delta_m + Delta) coefficient        =", total)
print("Factored:", sp.factor(total))

# sanity numeric spot checks
import mpmath as mp
for lamv, gv in [(1, 0.5), (2, 0.3), (0.5, 0.8)]:
    Kv = float(K.subs({lam: lamv, g: gv}))
    tv = float(total.subs({lam: lamv, g: gv}))
    print(f"lambda={lamv}, gamma={gv}: K={Kv:.6f}, total={tv:.6f}, "
          f"check = 3*lam/2 - lam^3/6 - lam/gamma "
          f"= {1.5*lamv - lamv**3/6 - lamv/gv:.6f}")

print()
print("Confirmed: the +1/(12*lambda) and -1/(12*lambda) pieces of Delta_m and")
print("the predecessor's Delta cancel EXACTLY and symbolically -- a genuine,")
print("checkable algebraic fact, not a coincidence of rounding.")
print()
print("Delta_total(lambda,gamma) := Delta_m + Delta")
print("                            = (3*lambda/2 - lambda^3/6 - lambda/gamma) / sqrt(n)")
