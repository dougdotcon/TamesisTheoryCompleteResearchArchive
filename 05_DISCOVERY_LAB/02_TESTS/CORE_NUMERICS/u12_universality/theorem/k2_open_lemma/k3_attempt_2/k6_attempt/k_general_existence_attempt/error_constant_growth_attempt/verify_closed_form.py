"""
verify_closed_form.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

The conjectured third-order closed form, found by inspecting the exact
ODE-solved H_r(t,b):

    H_r(t,b) = sum_{k=0}^{r-2} e_k^{(r)}(b) t^k ,

    e_k^{(r)}(b) = P(k) * FF(r,k+2) / prod_{i=1}^{k+3} (r+b+i) ,
    P(k) := (3k+8)(k+1)(k+2)(k+3)/24 ,   FF(r,j) := r(r-1)...(r-j+1) = r!/(r-j)! .

This slots into the already-PROVED family:
    c_k^{(r)}(b) = 1        * FF(r,k)   / prod_{i=1}^{k+1}(r+b+i)   [k6 SS2.3, PROVED]
    d_k^{(r)}(b) = C(k+2,2) * FF(r,k+1) / prod_{i=1}^{k+2}(r+b+i)   [k6 SS3.3, PROVED]
    e_k^{(r)}(b) = P(k)     * FF(r,k+2) / prod_{i=1}^{k+3}(r+b+i)   [NEW, this doc]

This script performs the two *exact* checks that a fit alone would not license:

  V1: exhaustive exact-rational comparison of the closed form against the
      ODE-solved H_r(.,b), for every r <= RMAX, every k, and many b.
  V2: the same with SYMBOLIC b (sympy), so the b-dependence is verified as a
      rational-function identity, not only at sampled integers.

(The symbolic-(r,k,b) proof of the defining coefficient recursion is a separate
 script, verify_ek_recursion.py.)
"""

import sys
from fractions import Fraction as Fr
import core as C

RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 45
BMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 8


def P(k):
    return Fr((3 * k + 8) * (k + 1) * (k + 2) * (k + 3), 24)


def FF(r, j):
    v = Fr(1)
    for i in range(j):
        v *= (r - i)
    return v


def e_closed(r, k, b):
    den = Fr(1)
    for i in range(1, k + 4):
        den *= (r + b + i)
    return P(k) * FF(r, k + 2) / den


print("=" * 90)
print("V1.  Closed form vs ODE-solved H_r, exact rationals, r=0..%d, b=0..%d," % (RMAX, BMAX))
print("     every coefficient index k (including k out of range, where both must be 0).")
print("=" * 90)
tot = 0
bad = 0
first_bad = None
for b in range(0, BMAX + 1):
    for r in range(0, RMAX + 1):
        Hp = C.H(r, b)
        # check every k from 0 to r (deliberately past the claimed top index r-2)
        for k in range(0, r + 2):
            tot += 1
            lhs = Hp.coeff(k)
            rhs = e_closed(r, k, b)
            if lhs != rhs:
                bad += 1
                if first_bad is None:
                    first_bad = (r, k, b, lhs, rhs)
print("  checks: %d   mismatches: %d" % (tot, bad))
if first_bad:
    print("  FIRST MISMATCH r=%d k=%d b=%d  ODE=%s  closed=%s" % first_bad)
else:
    print("  ALL EXACT.  (Note k=r-1 and k=r are included: FF(r,k+2)=0 there, and the")
    print("   ODE solution's coefficient is 0 there too -- the closed form self-truncates.)")

print()
print("=" * 90)
print("V1b. Degree check: deg H_r = r-2 for r>=2, H_0=H_1=0.")
print("=" * 90)
okdeg = True
for b in range(0, BMAX + 1):
    for r in range(0, RMAX + 1):
        want = -1 if r < 2 else r - 2
        got = C.H(r, b).deg()
        if got != want:
            okdeg = False
            print("  FAIL r=%d b=%d deg=%d want=%d" % (r, b, got, want))
print("  all degrees as predicted:", okdeg)

print()
print("=" * 90)
print("V2.  SYMBOLIC b.  Re-run the whole (F,G,Hhat,K,H,L) ladder with b a sympy")
print("     Symbol, and compare H_r(t,b) to the closed form as a rational function.")
print("=" * 90)
try:
    import sympy as sp
except Exception as ex:                                    # pragma: no cover
    print("  sympy unavailable (%s) -- V2 skipped" % ex)
    sys.exit(0)

t, bs = sp.symbols("t b")


def sF(r, bb):
    tot = 0
    for k in range(r + 1):
        ff = sp.Integer(1)
        for i in range(k):
            ff *= (r - i)
        den = sp.Integer(1)
        for i in range(1, k + 2):
            den *= (r + bb + i)
        tot += sp.together(ff / den) * t ** k
    return sp.expand(tot)


def sG(r, bb):
    tot = 0
    for k in range(r):
        ff = sp.Integer(1)
        for i in range(k + 1):
            ff *= (r - i)
        den = sp.Integer(1)
        for i in range(1, k + 3):
            den *= (r + bb + i)
        tot += sp.Rational((k + 1) * (k + 2), 2) * sp.together(ff / den) * t ** k
    return sp.expand(tot)


def sub1m(expr):
    return sp.expand(expr.subs(t, 1 - t))


def sHhat(r, bb):
    """as a polynomial in t standing for the variable s"""
    return sp.expand((1 - t) * sF(r, bb + 1).subs(t, 1 - t))


def sK(r, bb):
    out = sp.Integer(1)
    if r >= 1:
        out += r * sHhat(r - 1, bb + 1)
    out += (1 - t) * sG(r, bb + 1).subs(t, 1 - t)
    out -= (1 + bb + r) * sF(r, bb + 1).subs(t, 1 - t)
    return sp.expand(out)


_cacheH = {}
_cacheL = {}


def sH(r, bb):
    key = (r, sp.srepr(bb))
    if key in _cacheH:
        return _cacheH[key]
    if r == 0:
        _cacheH[key] = sp.Integer(0)
        return _cacheH[key]
    Fp = sF(r, bb)
    Gp = sG(r, bb)
    rhs = sp.Integer(0)
    piece = (sp.Rational(1, 2) * sp.diff(sHhat(r - 1, bb), t, 2)
             + sp.diff(sK(r - 1, bb), t, 1)
             + sL(r - 1, bb))
    rhs += r * piece.subs(t, 1 - t)
    rhs += sp.Rational(1, 2) * t * sp.diff(Gp, t, 2)
    rhs -= sp.Rational(1, 6) * t * sp.diff(Fp, t, 3)
    rhs += (1 + r + bb) * (sp.diff(Gp, t, 1) - sp.Rational(1, 2) * sp.diff(Fp, t, 2))
    rhs = sp.expand(rhs)
    poly = sp.Poly(rhs, t)
    out = sp.Integer(0)
    for k in range(poly.degree() + 1 if rhs != 0 else 0):
        out += sp.together(poly.coeff_monomial(t ** k) / (k + 1 + r + bb)) * t ** k
    out = sp.expand(out)
    _cacheH[key] = out
    return out


def sL(r, bb):
    key = (r, sp.srepr(bb))
    if key in _cacheL:
        return _cacheL[key]
    if r == 0:
        _cacheL[key] = sp.Integer(0)
        return _cacheL[key]
    out = r * sK(r - 1, bb + 1)
    out += (1 - t) * sH(r, bb + 1).subs(t, 1 - t)
    out -= (1 + bb + r) * sG(r, bb + 1).subs(t, 1 - t)
    out = sp.expand(out)
    _cacheL[key] = out
    return out


def sE_closed(r, bb):
    tot = 0
    for k in range(max(0, r - 1)):
        ff = sp.Integer(1)
        for i in range(k + 2):
            ff *= (r - i)
        den = sp.Integer(1)
        for i in range(1, k + 4):
            den *= (r + bb + i)
        tot += sp.Rational((3 * k + 8) * (k + 1) * (k + 2) * (k + 3), 24) * sp.together(ff / den) * t ** k
    return sp.expand(tot)


RSYM = int(sys.argv[3]) if len(sys.argv) > 3 else 11
allok = True
for r in range(0, RSYM + 1):
    diff = sp.simplify(sp.together(sH(r, bs) - sE_closed(r, bs)))
    ok = (diff == 0)
    allok &= ok
    print("  r=%2d : simplify( H_r(t,b) - closed_form ) == 0  ->  %s" % (r, ok))
    if not ok:
        print("        residue:", diff)
print("  symbolic-b verification, r=0..%d : %s" % (RSYM, allok))
