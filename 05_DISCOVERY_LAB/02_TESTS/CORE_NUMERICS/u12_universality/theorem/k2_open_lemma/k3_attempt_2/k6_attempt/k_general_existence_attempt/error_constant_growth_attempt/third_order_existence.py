"""
third_order_existence.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

The claim "D*_r(b) = max_t|H_r(t,b)| is the TRUE constant" is only meaningful if
the THREE-term expansion exists, i.e. if

    R^(3)_r(m,b,n)   := g_r(m,b) - F_r(t,b) - G_r(t,b)/n - H_r(t,b)/n^2
    eps^(3)_r(a,b,n) := h_r(a,b) - Hhat_r(s,b) - K_r(s,b)/n - L_r(s,b)/n^2

are O(1/n^3) uniformly.  The discrete-Gronwall argument of
k_general_existence_attempt/ATTEMPT.md SS3-SS6 applies VERBATIM one order up:
its only inputs are (i) that the h^0, h^1 (now also h^2) brackets of the
substitution vanish identically in t, and (ii) that everything in sight is a
polynomial of bounded degree, so the Taylor expansions are exact and finite.
(i) at order h^2 is exactly the H_r ODE of this document; (ii) is unchanged.

This script supplies the two computational ingredients that argument needs, and
then tests the resulting bound against real data:

  STEP 1  build Delta^(3)_r(t,b,h) exactly and CHECK its h^0, h^1 and h^2
          coefficients all vanish identically in t (so Delta^(3)_r = O(h^3)).
  STEP 2  compute A3_r(b) := sum_{k>=3} ||q^(3)_k(.,b)||  and
          B3_r(b) := ||L_{r-1}(.,b+1)||*r + (1+b+r)||H_r(1-.,b+1)||,
          then run the SAME recursion to get finite D3_r(b), C3_r(b).
  STEP 3  verify |R^(3)_r(m,b,n)| <= D3_r(b)/n^3 and
          |eps^(3)_r(a,b,n)| <= C3_r(b)/n^3 on exhaustive exact data.

Exact arithmetic throughout.
"""

import sys
from fractions import Fraction as Fr
from functools import lru_cache
import core as C
import loose_bound as LB      # reuse ONLY my own bivariate helpers from this dir

sys.setrecursionlimit(100000)
RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 24
BMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 4


@lru_cache(maxsize=None)
def Delta3(r, b):
    """Exact bivariate polynomial: the h-expansion residue of substituting the
    THREE-term ansatz into the exact non-source recursion (*)."""
    F, G, H = C.F(r, b), C.G(r, b), C.H(r, b)
    Fmh, Gmh, Hmh = (LB.bv_sub_t_minus_h(F), LB.bv_sub_t_minus_h(G),
                     LB.bv_sub_t_minus_h(H))
    # m[ (F+hG+h^2 H)(t) - (F+hG+h^2 H)(t-h) ]  with m = t/h
    at_t = LB.bv_add(LB.bv_from_t(F),
                     LB.bv_add({(i, j + 1): v for (i, j), v in LB.bv_from_t(G).items()},
                               {(i, j + 2): v for (i, j), v in LB.bv_from_t(H).items()}))
    at_tmh = LB.bv_add(Fmh, LB.bv_add({(i, j + 1): v for (i, j), v in Gmh.items()},
                                      {(i, j + 2): v for (i, j), v in Hmh.items()}))
    out = LB.bv_mul_t(LB.bv_div_h(LB.bv_add(at_t, at_tmh, -1)))
    # + (1+r+b) * (ansatz at t-h)
    out = LB.bv_add(out, LB.bv_scale(at_tmh, 1 + r + b))
    # - 1
    out = LB.bv_add(out, {(0, 0): Fr(1)}, -1)
    # - r [ Hhat_{r-1}(s) + h K_{r-1}(s) + h^2 L_{r-1}(s) ],  s = (1-t)+h
    if r >= 1:
        hh = LB.bv_sub_s_eq_1mt_plus_h(C.Hhat(r - 1, b))
        kk = LB.bv_sub_s_eq_1mt_plus_h(C.Kpol(r - 1, b))
        ll = LB.bv_sub_s_eq_1mt_plus_h(C.L(r - 1, b))
        kk = {(i, j + 1): v for (i, j), v in kk.items()}
        ll = {(i, j + 2): v for (i, j), v in ll.items()}
        out = LB.bv_add(out, LB.bv_scale(LB.bv_add(hh, LB.bv_add(kk, ll)), r), -1)
    return out


print("=" * 96)
print("STEP 1.  Delta^(3)_r(t,b,h) has vanishing h^0, h^1 AND h^2 coefficients")
print("         (h^0 = Fact 2, h^1 = Fact 3, h^2 = the NEW H_r ODE).")
print("=" * 96)
ok = True
for b in range(0, BMAX + 1):
    for r in range(0, RMAX + 1):
        D = Delta3(r, b)
        for j in (0, 1, 2):
            q = LB.bv_h_coeff(D, j)
            if q:
                ok = False
                print("   FAIL r=%d b=%d : h^%d coefficient is %s" % (r, b, j, q))
print("   r=0..%d, b=0..%d : all three brackets vanish identically in t : %s"
      % (RMAX, BMAX, ok))
print("   => Delta^(3)_r = sum_{k>=3} h^k q^(3)_k(t,b),  hence |Delta^(3)_r| <= A3_r(b) h^3")
print("      uniformly on t in [0,1], by the SS4 coefficient-sum lemma, unchanged.")


@lru_cache(maxsize=None)
def A3(r, b):
    D = Delta3(r, b)
    tot = Fr(0)
    for j in range(3, LB.bv_hdeg(D) + 1):
        tot += LB.coeff_sum_norm_dict(LB.bv_h_coeff(D, j))
    return tot


@lru_cache(maxsize=None)
def B3(r, b):
    """||r L_{r-1}(.,b+1) - (1+b+r) H_r(1-.,b+1)||  <=  r||L_{r-1}|| + (1+b+r)||H_r(1-.)||"""
    lt = r * C.L(r - 1, b + 1).coeff_sum_norm() if r >= 1 else Fr(0)
    return lt + (1 + b + r) * C.H(r, b + 1).shift_1_minus_x().coeff_sum_norm()


@lru_cache(maxsize=None)
def D3(r, b):
    if r == 0:
        return Fr(0)
    return (r * C3(r - 1, b) + A3(r, b)) / Fr(r + b + 1)


@lru_cache(maxsize=None)
def C3(r, b):
    if r == 0:
        return Fr(0)
    return B3(r, b) + r * C3(r - 1, b + 1) + D3(r, b + 1)


print()
print("=" * 96)
print("STEP 2.  The induction closes: finite A3_r(b), B3_r(b), D3_r(b), C3_r(b).")
print("=" * 96)
print("   %3s %3s | %-14s %-14s %-16s %-16s" % ("r", "b", "A3_r(b)", "B3_r(b)", "D3_r(b)", "C3_r(b)"))
for b in (0, 1):
    for r in range(1, 9):
        print("   %3d %3d | %-14.6g %-14.6g %-16.6g %-16.6g"
              % (r, b, float(A3(r, b)), float(B3(r, b)), float(D3(r, b)), float(C3(r, b))))

print()
print("=" * 96)
print("STEP 3.  Test the resulting bound against exhaustive exact data.")
print("         |R^(3)_r(m,b,n)| <= D3_r(b)/n^3  for EVERY valid m and n <= NMAX.")
print("=" * 96)
NMAX = 90
print("   %3s %3s | %-16s %-16s %-10s %-8s" %
      ("r", "b", "max n^3|R^(3)|", "D3_r(b)", "ratio", "viol"))
for b in (0, 1):
    for r in range(1, 7):
        best = Fr(0)
        viol = 0
        for n in range(b + r + 1, NMAX + 1):
            ch = C.Chain(n)
            bd = D3(r, b) / Fr(n) ** 3
            for m in range(b + r + 1, n + 1):
                v = abs(C.R3_resid(ch, r, m, b))
                if v * n ** 3 > best:
                    best = v * n ** 3
                if v > bd:
                    viol += 1
        d3 = D3(r, b)
        print("   %3d %3d | %-16.9f %-16.6g %-10.4f %-8d"
              % (r, b, float(best), float(d3), float(best / d3) if d3 else float("nan"), viol))

print()
print("   |eps^(3)_r(a,b,n)| <= C3_r(b)/n^3 for EVERY valid a and n <= NMAX")
print("   %3s %3s | %-16s %-16s %-10s %-8s" %
      ("r", "b", "max n^3|eps^(3)|", "C3_r(b)", "ratio", "viol"))
for b in (0, 1):
    for r in range(1, 7):
        best = Fr(0)
        viol = 0
        for n in range(b + r + 2, NMAX + 1):
            ch = C.Chain(n)
            bd = C3(r, b) / Fr(n) ** 3
            for a in range(0, n - b - r):
                v = abs(C.eps_h3_resid(ch, r, a, b))
                if v * n ** 3 > best:
                    best = v * n ** 3
                if v > bd:
                    viol += 1
        c3 = C3(r, b)
        print("   %3d %3d | %-16.9f %-16.6g %-10.4f %-8d"
              % (r, b, float(best), float(c3), float(best / c3) if c3 else float("nan"), viol))

print()
print("=" * 96)
print("STEP 4.  Consequence: n^2 R_r(m,b,n) -> H_r(t,b) uniformly, with an explicit rate")
print("         | n^2 R_r(m,b,n) - H_r(t,b) | <= D3_r(b)/n .")
print("         So limsup_n max_m n^2|R_r| = max_{t in [0,1]}|H_r(t,b)| = H_r(1,b) =: D*_r(b),")
print("         since every coefficient of H_r(.,b) is > 0 (closed form) and the grid")
print("         {m/n} becomes dense in [0,1].")
print("=" * 96)
for (r, b) in [(3, 0), (4, 0), (5, 0), (3, 1)]:
    print("   r=%d b=%d : D*_r(b) = %-14s = %.9f ;  rate constant D3_r(b) = %.6g"
          % (r, b, C.H(r, b).eval(Fr(1)), float(C.H(r, b).eval(Fr(1))), float(D3(r, b))))
