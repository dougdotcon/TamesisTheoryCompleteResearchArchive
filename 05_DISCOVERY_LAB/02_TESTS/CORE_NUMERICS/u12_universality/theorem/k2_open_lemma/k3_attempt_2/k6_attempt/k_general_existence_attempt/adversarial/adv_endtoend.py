"""
adv_endtoend.py -- the decisive end-to-end referee check.

Independently:
  1. compute Delta_r(t,b,h) from MY OWN substitution (adv_residual_derivation.py's
     method) for concrete r,b;
  2. verify the EXACT residual recursion of the target's section 3
        R_r(m) = ((m-1-r-b)/m) R_r(m-1) + (1/m)[ r eps^h_{r-1}(n-m+1,b,n) - Delta_r(t,b,h) ]
     holds EXACTLY (Fraction arithmetic) at every valid m, for many (r,b,n),
     INCLUDING at the base case m=b+r+1 where the target claims the coefficient
     kills the undefined term;
  3. verify the target's section 6 identity for eps^h_r EXACTLY;
  4. build the constants A_r(b), B_r(b), C_r(b), D_r(b) by the target's OWN stated
     recursion (D_0=C_0=0) and test whether the claimed bounds
        |R_r(m,b,n)| <= D_r(b)/n^2      and     |eps^h_r(a,b,n)| <= C_r(b)/n^2
     actually hold, over the whole domain, for every (r,b,n) reachable.
"""

from fractions import Fraction as Fr
import math
import sys
import sympy as sp
from adv_core import Chain, F_poly, G_poly, Hhat_poly, K_poly, _fall
from adv_numerics import F_fr, G_fr, Hhat_fr, K_fr, R, EH

sys.setrecursionlimit(200000)
t, h = sp.symbols('t h')

DELTA_CACHE = {}


def delta_coeffs(r, bval):
    """Delta_r(t,b,h) = sum_{k>=2} h^k * q_k(t,b);  return {k: q_k as sympy poly in t}."""
    key = (r, bval)
    if key in DELTA_CACHE:
        return DELTA_CACHE[key]
    F = F_poly(r, bval, t)
    G = G_poly(r, bval, t)
    A = F + h * G
    A_shift = A.subs(t, t - h)
    if r >= 1:
        Hm = Hhat_poly(r - 1, bval, 1 - t + h)
        Km = K_poly(r - 1, bval, 1 - t + h)
    else:
        Hm = sp.Integer(0)
        Km = sp.Integer(0)
    Expr = (t / h) * (A - A_shift) + (1 + r + bval) * A_shift - 1 - r * (Hm + h * Km)
    Expr = sp.expand(sp.cancel(sp.together(sp.expand(Expr))))
    P = sp.Poly(Expr, h)
    out = {}
    for (e,), c in P.terms():
        c = sp.expand(c)
        if c == 0:
            continue
        assert e >= 2, f"r={r} b={bval}: NONZERO h^{e} term survives -- brackets did NOT cancel: {c}"
        out[e] = sp.Poly(c, t)
    DELTA_CACHE[key] = out
    return out


def delta_value(r, bval, m, n):
    """exact Fraction value of Delta_r(t,b,h) at t=m/n, h=1/n."""
    co = delta_coeffs(r, bval)
    tv = Fr(m, n)
    tot = Fr(0)
    for k, poly in co.items():
        cval = Fr(0)
        for (e,), c in poly.terms():
            cval += Fr(sp.Rational(c).p, sp.Rational(c).q) * (tv ** e)
        tot += cval * Fr(1, n) ** k
    return tot


def norm_of_poly(poly_in_x):
    """sum of |coefficients| of a sympy polynomial, as an exact Fraction."""
    p = sp.Poly(sp.expand(poly_in_x), sp.Symbol('__z'))
    return None


def coeff_norm(expr, var):
    p = sp.Poly(sp.expand(expr), var)
    tot = Fr(0)
    for _, c in p.terms():
        rc = sp.Rational(c)
        tot += abs(Fr(rc.p, rc.q))
    return tot


print("=" * 92)
print("STEP 2 -- the EXACT residual recursion of section 3, verified with exact rationals")
print("=" * 92)
tot_checks = 0
tot_bad = 0
for (r, bval) in [(1, 0), (2, 0), (2, 3), (3, 0), (3, 2), (4, 0), (4, 1), (5, 0), (6, 0)]:
    for n in [max(bval + r + 2, 9), max(bval + r + 4, 13), 20, 27]:
        if n <= bval + r + 1:
            continue
        ch = Chain(n)
        j = bval + r + 1
        bad = 0
        for m in range(j, n + 1):
            lhs = R(ch, r, bval, m)
            alpha = Fr(m - 1 - r - bval, m)
            if m == j:
                prev = Fr(0)          # coefficient is exactly 0, value irrelevant
                assert alpha == 0
            else:
                prev = R(ch, r, bval, m - 1)
            a_src = n - m + 1
            if r >= 1:
                eh = EH(ch, r - 1, bval, a_src)
            else:
                eh = Fr(0)
            rhs = alpha * prev + Fr(1, m) * (r * eh - delta_value(r, bval, m, n))
            tot_checks += 1
            if lhs != rhs:
                bad += 1
                tot_bad += 1
                if bad <= 3:
                    print(f"    MISMATCH r={r} b={bval} n={n} m={m}: LHS={lhs} RHS={rhs} diff={lhs-rhs}")
        print(f"  r={r} b={bval} n={n:>3}: m = {j}..{n}  -> {n-j+1} identities, mismatches = {bad}")
print(f"  TOTAL: {tot_checks} exact identity checks, {tot_bad} mismatches")
print()

print("=" * 92)
print("STEP 3 -- the section 6 identity for eps^h_r, verified with exact rationals")
print("=" * 92)
tot_checks = 0
tot_bad = 0
for (r, bval) in [(1, 0), (2, 0), (2, 2), (3, 0), (3, 1), (4, 0), (5, 0)]:
    for n in [max(bval + r + 3, 11), 18, 25]:
        if n <= bval + r + 1:
            continue
        ch = Chain(n)
        bad = 0
        for a in range(0, n - bval - r):
            s = Fr(a, n)
            lhs = EH(ch, r, bval, a)
            term1 = Fr(1, n * n) * (r * K_fr(r - 1, bval + 1, s) if r >= 1 else Fr(0)
                                    ) - Fr(1, n * n) * (1 + bval + r) * G_fr(r, bval + 1, 1 - s)
            term2 = Fr(r, n) * (EH(ch, r - 1, bval + 1, a) if r >= 1 else Fr(0))
            coef = (1 - s) - Fr(1 + bval + r, n)
            if coef == 0:
                term3 = Fr(0)
            else:
                term3 = coef * R(ch, r, bval + 1, n - a)
            rhs = term1 + term2 + term3
            tot_checks += 1
            if lhs != rhs:
                bad += 1
                tot_bad += 1
                if bad <= 3:
                    print(f"    MISMATCH r={r} b={bval} n={n} a={a}: diff={lhs-rhs}")
        print(f"  r={r} b={bval} n={n:>3}: a = 0..{n-bval-r-1} -> {n-bval-r} identities, mismatches = {bad}")
print(f"  TOTAL: {tot_checks} exact identity checks, {tot_bad} mismatches")
print()

print("=" * 92)
print("STEP 4 -- build A_r(b), B_r(b), D_r(b), C_r(b) by the DOCUMENT'S OWN recursion")
print("           and test the claimed uniform bounds against real data")
print("=" * 92)


def A_const(r, bval):
    """A_r(b) = sum_{k=2}^{r} ||q_k(.,b)||  (coefficient-sum norms)."""
    co = delta_coeffs(r, bval)
    tot = Fr(0)
    for k, poly in co.items():
        tot += coeff_norm(poly.as_expr(), t)
    return tot


def B_const(r, bval):
    s = sp.Symbol('s')
    kk = K_poly(r - 1, bval + 1, s) if r >= 1 else sp.Integer(0)
    gg = G_poly(r, bval + 1, t)
    return coeff_norm(kk, s) + (1 + bval + r) * coeff_norm(gg, t)


DC = {}


def DCconst(r, bval):
    """returns (D_r(b), C_r(b)) per the document's own recursion."""
    if (r, bval) in DC:
        return DC[(r, bval)]
    if r == 0:
        DC[(r, bval)] = (Fr(0), Fr(0))
        return DC[(r, bval)]
    Cprev_b = DCconst(r - 1, bval)[1]
    Cprev_b1 = DCconst(r - 1, bval + 1)[1]
    Ar = A_const(r, bval)
    D_r_b = (r * Cprev_b + Ar) / (r + bval + 1)
    # C_r(b) needs D_r(b+1)
    Ar1 = A_const(r, bval + 1)
    Cprev_b1_for_D = DCconst(r - 1, bval + 1)[1]
    D_r_b1 = (r * Cprev_b1_for_D + Ar1) / (r + bval + 2)
    C_r_b = B_const(r, bval) + r * Cprev_b1 + 2 * D_r_b1
    DC[(r, bval)] = (D_r_b, C_r_b)
    return DC[(r, bval)]


print(f"  {'r':>2} {'b':>2} {'A_r(b)':>16} {'D_r(b)':>16} {'C_r(b)':>16}")
for r in range(1, 7):
    for bval in (0, 1, 2):
        D, C = DCconst(r, bval)
        print(f"  {r:>2} {bval:>2} {float(A_const(r,bval)):>16.6f} {float(D):>16.6f} {float(C):>16.6f}")
print()

print("  Testing |R_r(m,b,n)| <= D_r(b)/n^2 over the FULL m-range:")
worstratio = {}
for (r, bval) in [(1, 0), (2, 0), (2, 2), (3, 0), (3, 1), (3, 5), (4, 0), (4, 3), (5, 0), (6, 0)]:
    D, C = DCconst(r, bval)
    viol = 0
    worst = Fr(0)
    for n in [max(bval + r + 2, 12), 20, 33, 48]:
        if n <= bval + r + 1:
            continue
        ch = Chain(n)
        for m in range(bval + r + 1, n + 1):
            v = abs(R(ch, r, bval, m)) * n * n
            if v > worst:
                worst = v
            if D != 0 and v > D:
                viol += 1
            if D == 0 and v != 0:
                viol += 1
    print(f"    r={r} b={bval}: D_r(b)={float(D):.6f}  max n^2|R| observed={float(worst):.6f}  "
          f"violations={viol}  {'OK' if viol==0 else '*** BOUND VIOLATED ***'}")

print()
print("  Testing |eps^h_r(a,b,n)| <= C_r(b)/n^2 over the FULL a-range (incl. a=0):")
for (r, bval) in [(1, 0), (2, 0), (2, 2), (3, 0), (3, 1), (4, 0), (5, 0)]:
    D, C = DCconst(r, bval)
    viol = 0
    worst = Fr(0)
    for n in [max(bval + r + 2, 12), 20, 33, 48]:
        if n <= bval + r + 1:
            continue
        ch = Chain(n)
        for a in range(0, n - bval - r):
            v = abs(EH(ch, r, bval, a)) * n * n
            if v > worst:
                worst = v
            if C != 0 and v > C:
                viol += 1
            if C == 0 and v != 0:
                viol += 1
    print(f"    r={r} b={bval}: C_r(b)={float(C):.6f}  max n^2|eps^h| observed={float(worst):.6f}  "
          f"violations={viol}  {'OK' if viol==0 else '*** BOUND VIOLATED ***'}")
