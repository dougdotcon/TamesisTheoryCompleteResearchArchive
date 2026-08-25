#!/usr/bin/env python3
"""
r02_symbolic_check.py -- wave 17 front (d) PLATEAU-RESUMMATION-ATTEMPT

Independent EXACT symbolic verification (sympy, symbolic c) that the
(P,Q)-family solve implemented in r01_family_series.py produces coefficient
functions that satisfy the established recursion ODEs *identically*:

  for k = 1..KMAX:
     b_k' - c s b_k + c a_{k-1}/k - c b_{k-1}  == 0   (exact simplify)
  and a_{k+1} == [a_k' - c a_k + c w_k]/(k+1) is used to build a_{k+1},
  whose construction is checked by evaluating the g-series PDE residual
  indirectly through the b-ODE chain (the a-step is an explicit assignment,
  so the only nontrivial thing to verify is the b-solve and the erfcx
  derivative bookkeeping).

Representation: (P, Q) pairs of sympy polynomials in s with coefficients in
Q(c, r) where r = sqrt(pi*c/2); E(s) = erfcx(s*sqrt(c/2)) is kept ABSTRACT,
using only E'(s) = c*s*E - sqrt(2c/pi) (itself verified symbolically below
from the definition of erfcx). This mirrors r01's algebra but in exact
arithmetic with SYMBOLIC c -- a strictly stronger check than any numeric c.

Deterministic; no randomness.
"""

import sympy as sp

s, c = sp.symbols('s c', positive=True)
sc = sp.sqrt(2 * c / sp.pi)      # sqrt(2c/pi)
rt = sp.sqrt(sp.pi * c / 2)      # sqrt(pi c/2)

KMAX = 6


def deriv_F(P, Q):
    """d/ds of P + Q E with E' = c s E - sc"""
    dP = sp.expand(sp.diff(P, s) - sc * Q)
    dQ = sp.expand(sp.diff(Q, s) + c * s * Q)
    return dP, dQ


def bsolve(A, B):
    """bounded-branch solve of b' - c s b = A + B E in the family, exactly.
    Solve E-part V' = B, then U by undetermined coefficients descending,
    kappa pinned by the s^0 consistency relation."""
    A = sp.expand(A)
    B = sp.expand(B)
    V0 = sp.integrate(B, s)                       # zero constant term
    kappa = sp.Symbol('kappa')
    V = V0 + kappa
    R = sp.expand(A + sc * V)
    Rp = sp.Poly(R, s)
    d = Rp.degree() if R != 0 else 0
    u = {}
    for j in range(d, 0, -1):
        uj1 = u.get(j + 1, 0)
        u[j - 1] = sp.expand(((j + 1) * uj1 - Rp.coeff_monomial(s**j
                              if j else 1)) / c)
    # consistency at s^0:  u_1 = r_0
    r0 = Rp.coeff_monomial(1)
    u1 = u.get(1, 0)
    sol = sp.solve(sp.expand(u1 - r0), kappa)
    assert len(sol) == 1, "kappa consistency must pin exactly one constant"
    kap = sol[0]
    U = sum(sp.expand(ui.subs(kappa, kap)) * s**i for i, ui in u.items())
    V = sp.expand(V0 + kap)
    return sp.expand(U), V


def main():
    # 0) verify the E-derivative identity from the erfcx definition
    x = sp.Symbol('x', positive=True)
    E = sp.exp(c * x**2 / 2) * sp.erfc(x * sp.sqrt(c / 2))
    resid = sp.simplify(sp.diff(E, x) - (c * x * E - sp.sqrt(2 * c / sp.pi)))
    print(f"E'(s) - [c s E - sqrt(2c/pi)] simplifies to: {resid}")
    assert resid == 0

    aP = {0: sp.Integer(1), 1: -c}
    aQ = {0: sp.Integer(0), 1: sp.Integer(0)}
    bP = {0: sp.Integer(0)}
    bQ = {0: sp.Integer(0)}
    all_ok = True
    for k in range(1, KMAX):
        A = sp.expand(-c * aP[k - 1] / k + c * bP[k - 1])
        B = sp.expand(-c * aQ[k - 1] / k + c * bQ[k - 1])
        U, V = bsolve(A, B)
        bP[k], bQ[k] = U, V
        # verify the b-ODE identically: (U+VE)' - csb = A + B E
        dU, dV = deriv_F(U, V)
        res_nonE = sp.simplify(dU - c * s * U - A)
        res_E = sp.simplify(dV - c * s * V - B)
        ok = (res_nonE == 0 and res_E == 0)
        all_ok &= ok
        print(f"k={k}: b_k ODE residual (non-E, E) = ({res_nonE}, {res_E})"
              f"  {'OK' if ok else 'FAIL'}")
        # w_k and a_{k+1}
        wP = sp.expand(aP[k - 1] / k + (1 - s) * U - bP[k - 1])
        wQ = sp.expand(aQ[k - 1] / k + (1 - s) * V - bQ[k - 1])
        dP, dQ = deriv_F(aP[k], aQ[k])
        aP[k + 1] = sp.expand((dP - c * aP[k] + c * wP) / (k + 1))
        aQ[k + 1] = sp.expand((dQ - c * aQ[k] + c * wQ) / (k + 1))

    # cross-check known closed forms of record (symbolic c!)
    print()
    tests = [
        ("b_1 = sqrt(pi c/2) E", bP[1], sp.Integer(0), bQ[1], rt),
        ("b_2 = -c - (c/2)rt(1-2s)E", bP[2], -c, bQ[2],
         sp.expand(-(c / 2) * rt * (1 - 2 * s))),
        ("b_3 (referee closed form)", bP[3], sp.expand(c**2 * (8 - 7 * s) / 12),
         bQ[3], sp.expand(sp.sqrt(2 * sp.pi) * c**sp.Rational(3, 2)
                          * (7 * c * s**2 - 8 * c * s + 2 * c + 7) / 24)),
        ("a_2 = (c/2)[c+1+(1-s)rt E]", aP[2], sp.expand(c * (c + 1) / 2),
         aQ[2], sp.expand((c / 2) * (1 - s) * rt)),
    ]
    for name, gotP, wantP, gotQ, wantQ in tests:
        rP = sp.simplify(gotP - wantP)
        rQ = sp.simplify(gotQ - wantQ)
        ok = (rP == 0 and rQ == 0)
        all_ok &= ok
        print(f"{name:32s} residual (P,Q)=({rP},{rQ})  {'OK' if ok else 'FAIL'}")

    # a_3(0), a_4(0) closed forms at s=0 (symbolic c)
    a3_0 = sp.simplify((aP[3] + aQ[3]).subs(s, 0)
                       - (-(c**3 / 2 + 5 * c**2 / 2 + (c**2 + 3 * c / 2) * rt) / 3))
    print(f"a_3(0) - closed form = {a3_0}  {'OK' if a3_0 == 0 else 'FAIL'}")
    all_ok &= (a3_0 == 0)
    a4_0_num = (aP[4] + aQ[4]).subs(s, 0).subs(c, 1000)
    print(f"a_4(0)|c=1000 = {sp.N(a4_0_num, 16)}  (anchor 47146963944.14)")
    all_ok &= abs(sp.N(a4_0_num, 20) - sp.N(47146963944.14, 20)) < 1
    print()
    print(f"ALL SYMBOLIC CHECKS: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
