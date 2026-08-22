"""
adv_symbolic_r.py -- Facts 2 and 3 for SYMBOLIC r (not just concrete r), done
independently by the referee, plus two sharp predictions of the target's own
argument that the target never states, derived here and tested.

Fact 2 coefficient form (hand-derivable, reproduced symbolically):
    (k+1+r+b) c_k^(r)(b) = [k==0] + r c_{k-1}^(r-1)(b+1)

Fact 3 coefficient form, extracted BY ME from the G_r ODE
    t G' + (1+r+b) G = r Hhat'_{r-1}(1-t,b) + r K_{r-1}(1-t,b)
                        + (t/2) F'' + (1+r+b) F'
using Hhat_{r-1}(1-t,b) = t F_{r-1}(t,b+1) and
      K_{r-1}(1-t,b) = 1 + (r-1) t F_{r-2}(t,b+2) + t G_{r-1}(t,b+1)
                         - (b+r) F_{r-1}(t,b+1):

  k>=1: (k+1+r+b) d_k^(r)(b)
        = -r(k+1) c_k^(r-1)(b+1)
          + r[(r-1) c_{k-1}^(r-2)(b+2) + d_{k-1}^(r-1)(b+1) - (b+r) c_k^(r-1)(b+1)]
          + [k(k+1)/2 + (1+r+b)(k+1)] c_{k+1}^(r)(b)
  k=0 : (1+r+b) d_0^(r)(b)
        = -r c_0^(r-1)(b+1) + r[1 - (b+r) c_0^(r-1)(b+1)]
          + (1+r+b) c_1^(r)(b)

SHARP PREDICTIONS of the target's own machinery, derived here independently:
  P1: R_1(m,b,n) == 0 exactly, for every m,b,n  (Delta_1 == 0, eps^h_0 == 0).
  P2: R_2(m,0,n) == 1/(15 n^2) exactly, for EVERY m (not only the base case the
      target probed) -- because Delta_2 = (2/15)h^2 (t-independent) and
      eps^h_1(a,b,n) = 2/((b+3)(b+4)) h^2 (a-independent), so beta(k)=1/(5k n^2)
      and the telescoping sum collapses to the constant 1/(15 n^2).
"""

import sympy as sp
from fractions import Fraction as Fr
from adv_core import Chain
from adv_numerics import R, EH

r, k, b = sp.symbols('r k b', positive=True)


def c_sym(rr, kk, bb):
    """c_k^(r)(b) = r!/(r-k)! / prod_{i=1}^{k+1}(r+b+i), via gamma functions."""
    return (sp.gamma(rr + 1) / sp.gamma(rr - kk + 1)) * \
           (sp.gamma(rr + bb + 1) / sp.gamma(rr + bb + kk + 2))


def d_sym(rr, kk, bb):
    """d_k^(r)(b) = C(k+2,2) * r!/(r-k-1)! / prod_{i=1}^{k+2}(r+b+i)."""
    return sp.binomial(kk + 2, 2) * (sp.gamma(rr + 1) / sp.gamma(rr - kk)) * \
           (sp.gamma(rr + bb + 1) / sp.gamma(rr + bb + kk + 3))


print("=" * 88)
print("FACT 2, symbolic r,k,b")
print("=" * 88)
lhs = (k + 1 + r + b) * c_sym(r, k, b)
rhs = r * c_sym(r - 1, k - 1, b + 1)
diff = sp.simplify(sp.expand_func(sp.simplify(lhs - rhs)))
print(f"  k>=1 case:  LHS-RHS simplify = {diff}")
lhs0 = (1 + r + b) * c_sym(r, 0, b)
print(f"  k=0  case:  (1+r+b)c_0^(r)(b) - 1 = {sp.simplify(sp.expand_func(lhs0 - 1))}")
print()

print("=" * 88)
print("FACT 3, symbolic r,k,b -- recursion extracted independently from the ODE")
print("=" * 88)
L = (k + 1 + r + b) * d_sym(r, k, b)
Rr = (-r * (k + 1) * c_sym(r - 1, k, b + 1)
      + r * ((r - 1) * c_sym(r - 2, k - 1, b + 2)
             + d_sym(r - 1, k - 1, b + 1)
             - (b + r) * c_sym(r - 1, k, b + 1))
      + (k * (k + 1) / 2 + (1 + r + b) * (k + 1)) * c_sym(r, k + 1, b))
diff3 = sp.simplify(sp.expand_func(sp.simplify(L - Rr)))
print(f"  general k>=1 case:  LHS-RHS simplify = {diff3}")

L0 = (1 + r + b) * d_sym(r, 0, b)
R0 = (-r * c_sym(r - 1, 0, b + 1)
      + r * (1 - (b + r) * c_sym(r - 1, 0, b + 1))
      + (1 + r + b) * c_sym(r, 1, b))
diff30 = sp.simplify(sp.expand_func(sp.simplify(L0 - R0)))
print(f"  k=0 boundary case:  LHS-RHS simplify = {diff30}")
print()
print("  (cross-check the same two recursions numerically over many concrete (r,k,b))")


def c_num(rr, kk, bb):
    if kk < 0 or kk > rr:
        return Fr(0)
    num = 1
    for i in range(kk):
        num *= (rr - i)
    den = 1
    for i in range(1, kk + 2):
        den *= (rr + bb + i)
    return Fr(num, den)


def d_num(rr, kk, bb):
    if kk < 0 or kk > rr - 1:
        return Fr(0)
    num = 1
    for i in range(kk + 1):
        num *= (rr - i)
    den = 1
    for i in range(1, kk + 3):
        den *= (rr + bb + i)
    return Fr((kk + 2) * (kk + 1) // 2 * num, den)


bad2 = bad3 = tested = 0
for rr in range(1, 16):
    for bb in range(0, 8):
        for kk in range(0, rr + 2):
            tested += 1
            # Fact 2
            l = (kk + 1 + rr + bb) * c_num(rr, kk, bb)
            rgt = (Fr(1) if kk == 0 else Fr(0)) + rr * c_num(rr - 1, kk - 1, bb + 1)
            if l != rgt:
                bad2 += 1
            # Fact 3
            L = (kk + 1 + rr + bb) * d_num(rr, kk, bb)
            if kk == 0:
                Rq = (-rr * c_num(rr - 1, 0, bb + 1)
                      + rr * (1 - (bb + rr) * c_num(rr - 1, 0, bb + 1))
                      + (1 + rr + bb) * c_num(rr, 1, bb))
            else:
                Rq = (-rr * (kk + 1) * c_num(rr - 1, kk, bb + 1)
                      + rr * ((rr - 1) * c_num(rr - 2, kk - 1, bb + 2)
                              + d_num(rr - 1, kk - 1, bb + 1)
                              - (bb + rr) * c_num(rr - 1, kk, bb + 1))
                      + Fr(kk * (kk + 1), 2) * c_num(rr, kk + 1, bb)
                      + (1 + rr + bb) * (kk + 1) * c_num(rr, kk + 1, bb))
            if L != Rq:
                bad3 += 1
                if bad3 <= 5:
                    print(f"    Fact3 MISMATCH r={rr} k={kk} b={bb}: {L} vs {Rq}")
print(f"  numeric: {tested} (r,k,b) triples;  Fact2 mismatches={bad2}  Fact3 mismatches={bad3}")
print()

print("=" * 88)
print("SHARP PREDICTION P1:  R_1(m,b,n) == 0 exactly, every m,b,n")
print("=" * 88)
bad = 0
tot = 0
for n in [3, 5, 8, 13, 21, 34, 55]:
    for bb in range(0, min(4, n - 2)):
        ch = Chain(n)
        for m in range(bb + 2, n + 1):
            tot += 1
            if R(ch, 1, bb, m) != 0:
                bad += 1
                if bad <= 4:
                    print(f"    VIOLATION n={n} b={bb} m={m}: {R(ch,1,bb,m)}")
print(f"  {tot} exact evaluations, nonzero residuals = {bad}   "
      f"{'-> P1 CONFIRMED' if bad==0 else '-> P1 REFUTED'}")
print()

print("=" * 88)
print("SHARP PREDICTION P2:  R_2(m,0,n) == 1/(15 n^2) exactly, EVERY m")
print("=" * 88)
bad = 0
tot = 0
for n in [4, 6, 9, 14, 22, 35, 56, 90]:
    ch = Chain(n)
    for m in range(3, n + 1):
        tot += 1
        if R(ch, 2, 0, m) != Fr(1, 15 * n * n):
            bad += 1
            if bad <= 4:
                print(f"    VIOLATION n={n} m={m}: {R(ch,2,0,m)} != {Fr(1,15*n*n)}")
print(f"  {tot} exact evaluations, deviations from 1/(15n^2) = {bad}   "
      f"{'-> P2 CONFIRMED' if bad==0 else '-> P2 REFUTED'}")
print()
print("  and the general-b version predicted by the same computation:")
print("     eps^h_1(a,b,n) = 2/((b+3)(b+4)) / n^2, independent of a:")
bad = 0
for n in [6, 11, 20, 33]:
    ch = Chain(n)
    for bb in range(0, 4):
        for a in range(0, n - bb - 1):
            pred = Fr(2, (bb + 3) * (bb + 4) * n * n)
            if EH(ch, 1, bb, a) != pred:
                bad += 1
                if bad <= 3:
                    print(f"    VIOLATION n={n} b={bb} a={a}: {EH(ch,1,bb,a)} != {pred}")
print(f"  deviations = {bad}  {'-> CONFIRMED' if bad==0 else '-> REFUTED'}")
