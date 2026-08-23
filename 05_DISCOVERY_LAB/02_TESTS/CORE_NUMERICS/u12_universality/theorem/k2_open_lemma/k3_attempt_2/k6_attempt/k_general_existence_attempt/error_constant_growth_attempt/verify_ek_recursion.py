"""
verify_ek_recursion.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

Two-stage verification, exactly mirroring the methodology k6_attempt used to turn
its d_k^{(r)}(b) *conjecture* into a PROVED theorem (verify_dk_recursion.py):

  STAGE A.  Derive, by hand, the coefficient-of-t^k form of the H_r ODE (the
            "defining recursion" for e_k^{(r)}(b)), then CHECK THE RECURSION
            ITSELF, exhaustively and exactly, against the ODE-solved H_r for
            every integer r <= RMAX, every k >= 0 and every b <= BMAX --
            including every boundary index.  This certifies that the recursion
            written below really is the ODE, with no algebra slip.

  STAGE B.  Check that the conjectured closed form SATISFIES that recursion,
            (B1) symbolically for GENERIC r,k,b (gamma-function closed forms,
                 no looping over values), split into the general k>=1 case and
                 the k=0 boundary case, exactly as k6_attempt had to split;
            (B2) exhaustively and exactly for every integer r <= RMAX, k, b,
                 which covers all the integer boundary cases where the
                 falling factorials degenerate.

  A + B + the base case (H_0 == 0, an exact fact, not an asymptotic one)
  is a complete induction on r for the closed form -- CONDITIONAL on the H_r ODE
  itself, whose own status is discussed in ATTEMPT.md SS3.

-------------------------------------------------------------------------------
THE RECURSION (derived by hand in ATTEMPT.md SS3.2 of this directory; * = new):

 (k+1+r+b) e_k^{(r)}(b)  =  r * T  +  U ,   with

 T = (1/2)(k+1)(k+2) c_{k+1}^{(r-1)}(b+1)                 [ (1/2)Hhat''_{r-1} ]
   - (k+1)(r-1)      c_k^{(r-2)}(b+2)                     ]
   - (k+1)           d_k^{(r-1)}(b+1)                     ] -K'_{r-1}
   + (k+1)(b+r)      c_{k+1}^{(r-1)}(b+1)                 ]
   + (r-1) [k==0]                                         ]
   + (r-1)(r-2)      c_{k-1}^{(r-3)}(b+3)                 ]
   + (r-1)           d_{k-1}^{(r-2)}(b+2)                 ] L_{r-1}
   - (r-1)(b+r)      c_k^{(r-2)}(b+2)                     ]
   + e_{k-1}^{(r-1)}(b+1)                                 ]
   - (b+r)           d_k^{(r-1)}(b+1)                     ]

 U = (1/2)k(k+1)            d_{k+1}^{(r)}(b)              [ (t/2)G_r''      ]
   - (1/6)k(k+1)(k+2)       c_{k+2}^{(r)}(b)              [ -(t/6)F_r'''    ]
   + (1+r+b)(k+1)           d_{k+1}^{(r)}(b)              [ (1+r+b)G_r'     ]
   - (1/2)(1+r+b)(k+1)(k+2) c_{k+2}^{(r)}(b)              [ -(1+r+b)F_r''/2 ]
-------------------------------------------------------------------------------
"""

import sys
from fractions import Fraction as Fr
import core as C

RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
BMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6


# ---------------------------------------------------------------------------
# exact-integer closed forms, with the correct out-of-range conventions
# ---------------------------------------------------------------------------

def cc(k, r, b):
    """c_k^{(r)}(b); 0 unless 0<=k<=r and r>=0."""
    if r < 0 or k < 0 or k > r:
        return Fr(0)
    num = Fr(1)
    for i in range(k):
        num *= (r - i)
    den = Fr(1)
    for i in range(1, k + 2):
        den *= (r + b + i)
    return num / den


def dd(k, r, b):
    """d_k^{(r)}(b); 0 unless 0<=k<=r-1."""
    if r < 0 or k < 0 or k > r - 1:
        return Fr(0)
    num = Fr(1)
    for i in range(k + 1):
        num *= (r - i)
    den = Fr(1)
    for i in range(1, k + 3):
        den *= (r + b + i)
    return Fr((k + 1) * (k + 2), 2) * num / den


def ee(k, r, b):
    """e_k^{(r)}(b) -- THE CONJECTURED CLOSED FORM; 0 unless 0<=k<=r-2."""
    if r < 0 or k < 0 or k > r - 2:
        return Fr(0)
    num = Fr(1)
    for i in range(k + 2):
        num *= (r - i)
    den = Fr(1)
    for i in range(1, k + 4):
        den *= (r + b + i)
    return Fr((3 * k + 8) * (k + 1) * (k + 2) * (k + 3), 24) * num / den


def rhs_of_recursion(k, r, b, e_src, c_src=cc, d_src=dd):
    """r*T + U.  e_src supplies e_{k-1}^{(r-1)}(b+1)."""
    T = Fr(0)
    T += Fr((k + 1) * (k + 2), 2) * c_src(k + 1, r - 1, b + 1)
    T -= Fr(k + 1) * (r - 1) * c_src(k, r - 2, b + 2)
    T -= Fr(k + 1) * d_src(k, r - 1, b + 1)
    T += Fr(k + 1) * (b + r) * c_src(k + 1, r - 1, b + 1)
    if k == 0:
        T += Fr(r - 1)
    T += Fr((r - 1) * (r - 2)) * c_src(k - 1, r - 3, b + 3)
    T += Fr(r - 1) * d_src(k - 1, r - 2, b + 2)
    T -= Fr((r - 1) * (b + r)) * c_src(k, r - 2, b + 2)
    T += e_src(k - 1, r - 1, b + 1)
    T -= Fr(b + r) * d_src(k, r - 1, b + 1)

    U = Fr(0)
    U += Fr(k * (k + 1), 2) * d_src(k + 1, r, b)
    U -= Fr(k * (k + 1) * (k + 2), 6) * c_src(k + 2, r, b)
    U += Fr((1 + r + b) * (k + 1)) * d_src(k + 1, r, b)
    U -= Fr((1 + r + b) * (k + 1) * (k + 2), 2) * c_src(k + 2, r, b)
    return Fr(r) * T + U


# ---------------------------------------------------------------------------
print("=" * 92)
print("STAGE A.  Is the hand-derived recursion really the H_r ODE?")
print("          Feed it the ODE-SOLVED e's (core.H) on the right and compare to the")
print("          ODE-SOLVED e_k^{(r)}(b) on the left.  r=0..%d, b=0..%d, all k." % (RMAX, BMAX))
print("=" * 92)


def e_ode(k, r, b):
    if r < 0 or k < 0:
        return Fr(0)
    return C.H(r, b).coeff(k)


def c_ode(k, r, b):
    if r < 0 or k < 0:
        return Fr(0)
    return C.F(r, b).coeff(k)


def d_ode(k, r, b):
    if r < 0 or k < 0:
        return Fr(0)
    return C.G(r, b).coeff(k)


tot = bad = 0
firstbad = None
for b in range(0, BMAX + 1):
    for r in range(0, RMAX + 1):
        for k in range(0, r + 3):
            tot += 1
            lhs = Fr(k + 1 + r + b) * e_ode(k, r, b)
            rhs = rhs_of_recursion(k, r, b, e_ode, c_ode, d_ode)
            if lhs != rhs:
                bad += 1
                if firstbad is None:
                    firstbad = (r, k, b, lhs, rhs)
print("  checks: %d   mismatches: %d" % (tot, bad))
if firstbad:
    print("  FIRST MISMATCH r=%d k=%d b=%d lhs=%s rhs=%s" % firstbad)
else:
    print("  The recursion IS the ODE, exactly, at every index checked.")

print()
print("=" * 92)
print("STAGE B2.  Does the CONJECTURED CLOSED FORM satisfy that recursion?")
print("           Exact integers, r=0..%d, b=0..%d, all k (all boundaries included)."
      % (RMAX, BMAX))
print("=" * 92)
tot = bad = 0
firstbad = None
for b in range(0, BMAX + 1):
    for r in range(0, RMAX + 1):
        for k in range(0, r + 3):
            tot += 1
            lhs = Fr(k + 1 + r + b) * ee(k, r, b)
            rhs = rhs_of_recursion(k, r, b, ee, cc, dd)
            if lhs != rhs:
                bad += 1
                if firstbad is None:
                    firstbad = (r, k, b, lhs, rhs)
print("  checks: %d   mismatches: %d" % (tot, bad))
if firstbad:
    print("  FIRST MISMATCH r=%d k=%d b=%d lhs=%s rhs=%s" % firstbad)
else:
    print("  The closed form satisfies the recursion at every index checked.")

print()
print("=" * 92)
print("STAGE B1.  SYMBOLIC r,k,b via gamma-function closed forms (no looping).")
print("=" * 92)
try:
    import sympy as sp
except Exception as ex:                                    # pragma: no cover
    print("  sympy unavailable (%s) -- STAGE B1 skipped" % ex)
    sys.exit(0)

r, k, b = sp.symbols("r k b", positive=True)
g = sp.gamma


def sc(kk, rr, bb):
    return g(rr + 1) / g(rr - kk + 1) * g(rr + bb + 1) / g(rr + bb + kk + 2)


def sd(kk, rr, bb):
    return sp.Rational(1, 2) * (kk + 1) * (kk + 2) * g(rr + 1) / g(rr - kk) \
        * g(rr + bb + 1) / g(rr + bb + kk + 3)


def se(kk, rr, bb):
    return sp.Rational(1, 24) * (3 * kk + 8) * (kk + 1) * (kk + 2) * (kk + 3) \
        * g(rr + 1) / g(rr - kk - 1) * g(rr + bb + 1) / g(rr + bb + kk + 4)


def sym_rhs(kk, delta_k0, e_src=se):
    T = 0
    T += sp.Rational(1, 2) * (kk + 1) * (kk + 2) * sc(kk + 1, r - 1, b + 1)
    T -= (kk + 1) * (r - 1) * sc(kk, r - 2, b + 2)
    T -= (kk + 1) * sd(kk, r - 1, b + 1)
    T += (kk + 1) * (b + r) * sc(kk + 1, r - 1, b + 1)
    if delta_k0:
        T += (r - 1)
    T += (r - 1) * (r - 2) * (0 if delta_k0 else sc(kk - 1, r - 3, b + 3))
    T += (r - 1) * (0 if delta_k0 else sd(kk - 1, r - 2, b + 2))
    T -= (r - 1) * (b + r) * sc(kk, r - 2, b + 2)
    T += (0 if delta_k0 else e_src(kk - 1, r - 1, b + 1))
    T -= (b + r) * sd(kk, r - 1, b + 1)

    U = 0
    U += sp.Rational(1, 2) * kk * (kk + 1) * sd(kk + 1, r, b)
    U -= sp.Rational(1, 6) * kk * (kk + 1) * (kk + 2) * sc(kk + 2, r, b)
    U += (1 + r + b) * (kk + 1) * sd(kk + 1, r, b)
    U -= sp.Rational(1, 2) * (1 + r + b) * (kk + 1) * (kk + 2) * sc(kk + 2, r, b)
    return r * T + U


def normalise(expr, kk):
    """Divide by a common gamma scale so every term becomes RATIONAL in (r,k,b),
    then simplify.  The scale is nonzero for generic r,k,b, so vanishing of the
    normalised expression is equivalent to vanishing of the original."""
    scale = g(r + 1) * g(r + b + 1) / (g(r - kk - 1) * g(r + b + kk + 4))
    out = sp.expand(sp.gammasimp(sp.expand(expr / scale)))
    return sp.cancel(sp.together(out))


print("  general case, k >= 1, symbolic r,k,b:")
expr = (k + 1 + r + b) * se(k, r, b) - sym_rhs(k, delta_k0=False)
res = normalise(expr, k)
print("    (LHS - RHS)/scale  simplifies to :", res)
ok1 = (sp.simplify(res) == 0)

print("  boundary case k = 0, symbolic r,b:")
expr0 = (0 + 1 + r + b) * se(0, r, b) - sym_rhs(sp.Integer(0), delta_k0=True)
res0 = normalise(expr0, sp.Integer(0))
print("    (LHS - RHS)/scale  simplifies to :", res0)
ok0 = (sp.simplify(res0) == 0)

print()
print("  STAGE B1 verdict: general k>=1 : %s ;  k=0 : %s" % (ok1, ok0))
