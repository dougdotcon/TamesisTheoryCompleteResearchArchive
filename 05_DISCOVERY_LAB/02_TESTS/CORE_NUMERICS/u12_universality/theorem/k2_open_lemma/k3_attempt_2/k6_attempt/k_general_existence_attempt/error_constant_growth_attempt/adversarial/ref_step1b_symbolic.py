"""
STEP 1b -- symbolic strengthening of STEP 1.

PART I   symbolic-b ladder: rerun MY OWN eps^0/eps^1/eps^2 ladder with b a sympy
         Symbol (so no integer-b coincidence can survive) and compare H_r(t,b)
         to Theorem 1's closed form, r = 0..RSYM.

PART II  symbolic r,k,b: the coefficient recursion implied by MY OWN H_r ODE,
         derived by hand in REFEREE_REPORT.md Part 1.3 (NOT copied from the
         target's Sec 3.2 -- that section was read only afterwards, and the
         comparison is reported in the report), written with Gamma functions and
         checked to simplify to 0 for generic r,k,b.  Two branches: general
         k>=1, and the k=0 boundary where the K_{r-2} constant branch fires and
         all index-(k-1) objects vanish.
"""

import sys
import sympy as sp

RSYM = int(sys.argv[1]) if len(sys.argv) > 1 else 9

t = sp.Symbol('t')
b = sp.Symbol('b')

print("=" * 78)
print("STEP 1b  symbolic verification")
print("=" * 78)

# ---------------------------------------------------------------------------
# PART I -- symbolic-b ladder
# ---------------------------------------------------------------------------


def poly_coeffs(expr, var, deg):
    p = sp.Poly(sp.expand(expr), var)
    return [sp.simplify(p.coeff_monomial(var ** k)) for k in range(deg + 1)]


def solve_ode_sym(rhs, r, bb, var):
    """t X' + (1+r+b) X = rhs  ->  x_k = rhs_k/(k+1+r+b)."""
    rhs = sp.expand(rhs)
    p = sp.Poly(rhs, var)
    d = p.degree() if rhs != 0 else 0
    out = 0
    for k in range(d + 1):
        ck = p.coeff_monomial(var ** k)
        if ck != 0:
            out += sp.together(ck / (k + 1 + r + bb)) * var ** k
    return sp.expand(out)


s = sp.Symbol('s')

F = {}
G = {}
H = {}
Hh = {}
K = {}
L = {}

BMAX = RSYM + 2
# b index is a symbolic shift: represent level-(r) object at "b + j" by storing
# the expression as a function of a formal symbol and substituting b -> b+j.
# Simplest correct approach: store each object as a python lambda of (bexpr).


def build():
    # r = 0
    F[0] = lambda bb: sp.Integer(1) / (bb + 1) + 0 * t
    G[0] = lambda bb: sp.Integer(0) * t
    H[0] = lambda bb: sp.Integer(0) * t
    Hh[0] = lambda bb: (1 - s) * F[0](bb + 1).subs(t, 1 - s)
    K[0] = lambda bb: (sp.Integer(1)
                       + (1 - s) * G[0](bb + 1).subs(t, 1 - s)
                       - (1 + bb + 0) * F[0](bb + 1).subs(t, 1 - s))
    L[0] = lambda bb: ((1 - s) * H[0](bb + 1).subs(t, 1 - s)
                       - (1 + bb + 0) * G[0](bb + 1).subs(t, 1 - s))

    for r in range(1, RSYM + 1):
        def mk(r):
            def Fr_(bb):
                Hh1 = Hh[r - 1](bb)
                rhs = 1 + r * Hh1.subs(s, 1 - t)
                return solve_ode_sym(sp.expand(rhs), r, bb, t)

            def Gr_(bb):
                Hh1 = Hh[r - 1](bb)
                K1 = K[r - 1](bb)
                Fp = sp.diff(F[r](bb), t)
                Fpp = sp.diff(F[r](bb), t, 2)
                rhs = (r * sp.diff(Hh1, s).subs(s, 1 - t)
                       + r * K1.subs(s, 1 - t)
                       + t / 2 * Fpp + (1 + r + bb) * Fp)
                return solve_ode_sym(sp.expand(rhs), r, bb, t)

            def Hr_(bb):
                Hh1 = Hh[r - 1](bb)
                K1 = K[r - 1](bb)
                L1 = L[r - 1](bb)
                Ff = F[r](bb)
                Gg = G[r](bb)
                rhs = (r * (sp.Rational(1, 2) * sp.diff(Hh1, s, 2).subs(s, 1 - t)
                            + sp.diff(K1, s).subs(s, 1 - t)
                            + L1.subs(s, 1 - t))
                       + t / 2 * sp.diff(Gg, t, 2)
                       - t / 6 * sp.diff(Ff, t, 3)
                       + (1 + r + bb) * (sp.diff(Gg, t)
                                         - sp.Rational(1, 2) * sp.diff(Ff, t, 2)))
                return solve_ode_sym(sp.expand(rhs), r, bb, t)

            def Hhr_(bb):
                return (1 - s) * F[r](bb + 1).subs(t, 1 - s)

            def Kr_(bb):
                return sp.expand(1 + r * Hh[r - 1](bb + 1)
                                 + (1 - s) * G[r](bb + 1).subs(t, 1 - s)
                                 - (1 + bb + r) * F[r](bb + 1).subs(t, 1 - s))

            def Lr_(bb):
                return sp.expand(r * K[r - 1](bb + 1)
                                 + (1 - s) * H[r](bb + 1).subs(t, 1 - s)
                                 - (1 + bb + r) * G[r](bb + 1).subs(t, 1 - s))
            return Fr_, Gr_, Hr_, Hhr_, Kr_, Lr_

        f_, g_, h_, hh_, k_, l_ = mk(r)
        F[r], G[r], H[r], Hh[r], K[r], L[r] = f_, g_, h_, hh_, k_, l_


build()


def e_closed_sym(r, k, bb):
    if k < 0 or k > r - 2:
        return sp.Integer(0)
    num = sp.Integer((3 * k + 8) * (k + 1) * (k + 2) * (k + 3))
    fall = sp.Integer(1)
    for i in range(k + 2):
        fall *= (r - i)
    den = sp.Integer(1)
    dd = sp.Integer(1)
    for i in range(1, k + 4):
        dd *= (r + bb + i)
    return sp.together(num * fall / (24 * dd))


print()
print("PART I -- symbolic-b ladder vs Theorem 1 closed form")
allz = True
for r in range(0, RSYM + 1):
    Hr = sp.expand(H[r](b))
    closed = sum(e_closed_sym(r, k, b) * t ** k for k in range(0, max(0, r - 1)))
    diff = sp.simplify(sp.together(sp.expand(Hr - closed)))
    ok = (diff == 0)
    allz = allz and ok
    print("   r=%2d  simplify(H_r(t,b) - closed_form) = %s" % (r, diff))
print("   ALL ZERO:", allz)

# also record F,G symbolic-b agreement (validation one order down)
print()
print("PART I' -- symbolic-b validation one order down (F_r, G_r)")


def c_closed_sym(r, k, bb):
    if k < 0 or k > r:
        return sp.Integer(0)
    fall = sp.Integer(1)
    for i in range(k):
        fall *= (r - i)
    dd = sp.Integer(1)
    for i in range(1, k + 2):
        dd *= (r + bb + i)
    return sp.together(fall / dd)


def d_closed_sym(r, k, bb):
    if k < 0 or k > r - 1:
        return sp.Integer(0)
    fall = sp.Integer(1)
    for i in range(k + 1):
        fall *= (r - i)
    dd = sp.Integer(1)
    for i in range(1, k + 3):
        dd *= (r + bb + i)
    return sp.together(sp.Integer((k + 1) * (k + 2)) * fall / (2 * dd))


okFG = True
for r in range(0, RSYM + 1):
    dF = sp.simplify(sp.expand(F[r](b) - sum(c_closed_sym(r, k, b) * t ** k
                                             for k in range(0, r + 1))))
    dG = sp.simplify(sp.expand(G[r](b) - sum(d_closed_sym(r, k, b) * t ** k
                                             for k in range(0, max(0, r)))))
    okFG = okFG and (dF == 0) and (dG == 0)
    print("   r=%2d  F diff=%s   G diff=%s" % (r, dF, dG))
print("   ALL ZERO:", okFG)

# ---------------------------------------------------------------------------
# PART II -- symbolic r,k,b in the coefficient recursion of my own H_r ODE
# ---------------------------------------------------------------------------
print()
print("PART II -- symbolic r,k,b:  (k+1+r+b) e_k^(r)(b) = r*T + U")

R_, K_, B_ = sp.symbols('R K B')


def C(r, k, bb):
    return sp.gamma(r + 1) / sp.gamma(r - k + 1) * sp.gamma(r + bb + 1) / sp.gamma(r + bb + k + 2)


def D(r, k, bb):
    return ((k + 1) * (k + 2) / sp.Integer(2)
            * sp.gamma(r + 1) / sp.gamma(r - k)
            * sp.gamma(r + bb + 1) / sp.gamma(r + bb + k + 3))


def E(r, k, bb):
    return ((3 * k + 8) * (k + 1) * (k + 2) * (k + 3) / sp.Integer(24)
            * sp.gamma(r + 1) / sp.gamma(r - k - 1)
            * sp.gamma(r + bb + 1) / sp.gamma(r + bb + k + 4))


def build_rhs(r, k, bb, kzero):
    """r*T + U, my own hand-derived coefficient extraction of the H_r ODE RHS.

       T = [ (1/2) Hhat''_{r-1}(1-t,b) + K'_{r-1}(1-t,b) + L_{r-1}(1-t,b) ]_k
       U = [ (t/2)G_r'' - (t/6)F_r''' + (1+r+b)G_r' - ((1+r+b)/2)F_r'' ]_k
    """
    # (1/2) Hhat''_{r-1}(1-t,b) ; Hhat_{r-1}(1-t,b) = t F_{r-1}(t,b+1)
    T = sp.Rational(1, 2) * (k + 1) * (k + 2) * C(r - 1, k + 1, bb + 1)
    # K'_{r-1}(1-t,b) = -d/dt[ 1 + (r-1) t F_{r-2}(t,b+2) + t G_{r-1}(t,b+1)
    #                          - (b+r) F_{r-1}(t,b+1) ]
    T += -(r - 1) * (k + 1) * C(r - 2, k, bb + 2)
    T += -(k + 1) * D(r - 1, k, bb + 1)
    T += (bb + r) * (k + 1) * C(r - 1, k + 1, bb + 1)
    # L_{r-1}(1-t,b) = (r-1) K_{r-2}(1-t,b+1) + t H_{r-1}(t,b+1)
    #                  - (b+r) G_{r-1}(t,b+1)
    #   K_{r-2}(1-t,b+1) = 1 + (r-2) t F_{r-3}(t,b+3) + t G_{r-2}(t,b+2)
    #                        - (b+r) F_{r-2}(t,b+2)
    if kzero:
        T += (r - 1) * 1                       # the constant branch, k=0 only
        T += -(r - 1) * (bb + r) * C(r - 2, 0, bb + 2)
        T += -(bb + r) * D(r - 1, 0, bb + 1)
        # index-(k-1) objects all vanish at k=0
    else:
        T += (r - 1) * (r - 2) * C(r - 3, k - 1, bb + 3)
        T += (r - 1) * D(r - 2, k - 1, bb + 2)
        T += -(r - 1) * (bb + r) * C(r - 2, k, bb + 2)
        T += E(r - 1, k - 1, bb + 1)
        T += -(bb + r) * D(r - 1, k, bb + 1)

    U = sp.Rational(1, 2) * k * (k + 1) * D(r, k + 1, bb)
    U += -sp.Rational(1, 6) * k * (k + 1) * (k + 2) * C(r, k + 2, bb)
    U += (1 + r + bb) * (k + 1) * D(r, k + 1, bb)
    U += -sp.Rational(1, 2) * (1 + r + bb) * (k + 1) * (k + 2) * C(r, k + 2, bb)
    return r * T + U


lhs = (K_ + 1 + R_ + B_) * E(R_, K_, B_)
rhs = build_rhs(R_, K_, B_, kzero=False)
dif = sp.simplify(sp.expand(sp.simplify(sp.gammasimp(lhs - rhs))))
print("   general k>=1, symbolic r,k,b :  LHS-RHS = %s" % dif)

lhs0 = (0 + 1 + R_ + B_) * E(R_, 0, B_)
rhs0 = build_rhs(R_, 0, B_, kzero=True)
dif0 = sp.simplify(sp.expand(sp.simplify(sp.gammasimp(lhs0 - rhs0))))
print("   k=0 boundary,  symbolic r,b  :  LHS-RHS = %s" % dif0)
print()
print("PART II verdict:", "BOTH ZERO" if (dif == 0 and dif0 == 0) else "NOT ZERO")
