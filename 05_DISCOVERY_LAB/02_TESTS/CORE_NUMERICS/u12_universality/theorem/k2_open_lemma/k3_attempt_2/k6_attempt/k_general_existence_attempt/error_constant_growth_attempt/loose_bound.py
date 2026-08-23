"""
loose_bound.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

The other half of open item (ii): the growth in r of the constants D_r(b), C_r(b)
that the existing discrete-Gronwall proof actually produces, so that the gap
against the TRUE constant D*_r(b) can be quantified rather than just noticed.

Definitions reproduced VERBATIM from k_general_existence_attempt/ATTEMPT.md
(SS4 as corrected by the post-adversarial addendum, SS5, SS6):

  Delta_r(t,b,h) := (t/h)[F_r(t,b) - F_r(t-h,b)]  +  t[G_r(t,b) - G_r(t-h,b)]
                     + (1+r+b)[F_r(t-h,b) + h G_r(t-h,b)]
                     - 1 - r[ Hhat_{r-1}((1-t)+h, b) + h K_{r-1}((1-t)+h, b) ]
      -- an exact polynomial in (t,h); its h^0 and h^1 coefficients vanish
         identically (Facts 2 and 3), which this script re-checks.
  Delta_r = sum_{k>=2} h^k q_k(t,b)   and   A_r(b) := sum_{k>=2} ||q_k(.,b)||
  B_r(b) := ||K_{r-1}(.,b+1)|| + (1+b+r)||G_r(.,b+1)||
  D_r(b) := [ r C_{r-1}(b) + A_r(b) ] / (r+b+1)
  C_r(b) := B_r(b) + r C_{r-1}(b+1) + 2 D_r(b+1)
  D_0(b) = C_0(b) = 0
  where ||p|| := sum_k |a_k| is the SS4 coefficient-sum norm.

All arithmetic exact (fractions.Fraction).  Floats only for display.
"""

import sys
from fractions import Fraction as Fr
from functools import lru_cache
from math import comb, log
import core as C

RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18


# ---------------------------------------------------------------------------
# minimal bivariate polynomial in (t,h): dict {(i,j): Fraction} for t^i h^j
# ---------------------------------------------------------------------------

def bv_from_t(p):
    return {(i, 0): c for i, c in enumerate(p.c) if c != 0}


def bv_add(a, b, sign=1):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Fr(0)) + sign * v
        if out[k] == 0:
            del out[k]
    return out


def bv_scale(a, f):
    f = Fr(f)
    if f == 0:
        return {}
    return {k: v * f for k, v in a.items()}


def bv_mul_t(a):
    return {(i + 1, j): v for (i, j), v in a.items()}


def bv_div_h(a):
    out = {}
    for (i, j), v in a.items():
        assert j >= 1, "not divisible by h: monomial t^%d h^%d" % (i, j)
        out[(i, j - 1)] = v
    return out


def bv_sub_t_minus_h(p):
    """univariate p(t) -> bivariate p(t-h)."""
    out = {}
    for i, c in enumerate(p.c):
        if c == 0:
            continue
        for l in range(i + 1):
            key = (l, i - l)
            out[key] = out.get(key, Fr(0)) + c * comb(i, l) * ((-1) ** (i - l))
    return {k: v for k, v in out.items() if v != 0}


def bv_sub_s_eq_1mt_plus_h(p):
    """univariate p(s) -> bivariate p((1-t)+h)."""
    out = {}
    for i, c in enumerate(p.c):
        if c == 0:
            continue
        for j in range(i + 1):                 # choose h^j
            coef = c * comb(i, j)
            # remaining (1-t)^(i-j)
            e = i - j
            for l in range(e + 1):             # t^l
                key = (l, j)
                out[key] = out.get(key, Fr(0)) + coef * comb(e, l) * ((-1) ** l)
    return {k: v for k, v in out.items() if v != 0}


def bv_h_coeff(a, j):
    """the coefficient of h^j, as a dict {i: coeff} (a polynomial in t)."""
    return {i: v for (i, jj), v in a.items() if jj == j}


def bv_hdeg(a):
    return max((j for (_, j) in a), default=-1)


def coeff_sum_norm_dict(d):
    return sum((abs(v) for v in d.values()), Fr(0))


# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def Delta(r, b):
    """The exact bivariate polynomial Delta_r(t,b,h)."""
    F = C.F(r, b)
    G = C.G(r, b)
    Fmh = bv_sub_t_minus_h(F)
    Gmh = bv_sub_t_minus_h(G)
    # (t/h)[F(t) - F(t-h)]
    d1 = bv_add(bv_from_t(F), Fmh, -1)
    d1 = bv_mul_t(bv_div_h(d1))
    # t[G(t) - G(t-h)]
    d2 = bv_mul_t(bv_add(bv_from_t(G), Gmh, -1))
    out = bv_add(d1, d2)
    # (1+r+b)[F(t-h) + h G(t-h)]
    third = bv_add(Fmh, {(i, j + 1): v for (i, j), v in Gmh.items()})
    out = bv_add(out, bv_scale(third, 1 + r + b))
    # -1
    out = bv_add(out, {(0, 0): Fr(1)}, -1)
    # - r [ Hhat_{r-1}((1-t)+h,b) + h K_{r-1}((1-t)+h,b) ]
    if r >= 1:
        hh = bv_sub_s_eq_1mt_plus_h(C.Hhat(r - 1, b))
        kk = bv_sub_s_eq_1mt_plus_h(C.Kpol(r - 1, b))
        kk = {(i, j + 1): v for (i, j), v in kk.items()}
        out = bv_add(out, bv_scale(bv_add(hh, kk), r), -1)
    return out


@lru_cache(maxsize=None)
def A(r, b):
    """A_r(b) = sum_{k>=2} ||q_k(.,b)||, and a check that q_0 = q_1 = 0."""
    D = Delta(r, b)
    q0 = bv_h_coeff(D, 0)
    q1 = bv_h_coeff(D, 1)
    assert not q0, "h^0 bracket did not vanish at r=%d b=%d: %s" % (r, b, q0)
    assert not q1, "h^1 bracket did not vanish at r=%d b=%d: %s" % (r, b, q1)
    tot = Fr(0)
    for j in range(2, bv_hdeg(D) + 1):
        tot += coeff_sum_norm_dict(bv_h_coeff(D, j))
    return tot


@lru_cache(maxsize=None)
def B(r, b):
    kn = C.Kpol(r - 1, b + 1).coeff_sum_norm() if r >= 1 else Fr(0)
    return kn + (1 + b + r) * C.G(r, b + 1).coeff_sum_norm()


@lru_cache(maxsize=None)
def Dloose(r, b):
    if r == 0:
        return Fr(0)
    return (r * Cloose(r - 1, b) + A(r, b)) / Fr(r + b + 1)


@lru_cache(maxsize=None)
def Cloose(r, b):
    if r == 0:
        return Fr(0)
    return B(r, b) + r * Cloose(r - 1, b + 1) + 2 * Dloose(r, b + 1)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    print("=" * 96)
    print("CHECK 0.  Reproduce the wave-8 referee's independently computed table")
    print("          (REFEREE_REPORT.md SSA.5) from my own from-scratch implementation.")
    print("=" * 96)
    ref = {  # r : (A_r(0), D_r(0), C_r(0))  from REFEREE_REPORT.md SSA.5
        1: (0.000000, 0.000000, 0.500000),
        2: (0.133333, 0.377778, 2.233333),
        3: (0.464286, 1.791071, 9.019714),
        4: (1.076190, 7.431010, 39.764374),
        5: (2.075036, 33.482818, 202.485138),
        6: (3.594572, 174.072200, 1200.680035),
    }
    print("   %3s %-12s %-12s | %-12s %-12s | %-14s %-14s" %
          ("r", "A_r(0) mine", "referee", "D_r(0) mine", "referee", "C_r(0) mine", "referee"))
    allmatch = True
    for r in range(1, 7):
        a, d, c = float(A(r, 0)), float(Dloose(r, 0)), float(Cloose(r, 0))
        ra, rd, rc = ref[r]
        m = (abs(a - ra) < 5e-6 and abs(d - rd) < 5e-6 and abs(c - rc) < 5e-5)
        allmatch &= m
        print("   %3d %-12.6f %-12.6f | %-12.6f %-12.6f | %-14.6f %-14.6f  %s"
              % (r, a, ra, d, rd, c, rc, "OK" if m else "MISMATCH"))
    print("   independent reproduction of the referee's table:", allmatch)
    # a couple of the referee's non-zero-b entries too
    print("   spot checks at b>0 (referee SSA.5 end-to-end block):")
    for (r, b, rd) in [(2, 2, 0.140952), (3, 1, 1.087000), (3, 5, 0.303012), (4, 3, 2.376231)]:
        print("      D_%d(%d) mine = %.6f   referee = %.6f   %s"
              % (r, b, float(Dloose(r, b)), rd,
                 "OK" if abs(float(Dloose(r, b)) - rd) < 5e-6 else "MISMATCH"))

    print()
    print("=" * 96)
    print("PART 1.  Growth of the LOOSE bound vs the TRUE constant, b=0")
    print("=" * 96)
    print("   %3s | %-16s %-16s %-14s | %-12s %-12s" %
          ("r", "D_r(0) [bound]", "D*_r(0) [true]", "gap D/D*", "D_r/D_{r-1}", "A_r/A_{r-1}"))
    prevD = prevA = None
    for r in range(1, RMAX + 1):
        d = Dloose(r, 0)
        ds = C.H(r, 0).eval(Fr(1))
        a = A(r, 0)
        rd = float(d / prevD) if (prevD and prevD != 0) else float("nan")
        ra = float(a / prevA) if (prevA and prevA != 0) else float("nan")
        print("   %3d | %-16.6g %-16.6g %-14.6g | %-12.6f %-12.6f"
              % (r, float(d), float(ds), (float(d / ds) if ds else float("nan")), rd, ra))
        prevD, prevA = d, a

    print()
    print("=" * 96)
    print("PART 2.  What law does D_r(0) follow?  ratios of ratios / factorial test")
    print("=" * 96)
    print("   %3s | %-14s %-14s %-14s %-14s" %
          ("r", "D_r/D_{r-1}", "(D_r/D_{r-1})/r", "D_r/r!", "log D_r / (r log r)"))
    prev = None
    for r in range(2, RMAX + 1):
        d = Dloose(r, 0)
        rat = float(d / prev) if prev else float("nan")
        fact = 1.0
        for i in range(1, r + 1):
            fact *= i
        print("   %3d | %-14.6f %-14.6f %-14.6g %-14.6f"
              % (r, rat, rat / r, float(d) / fact,
                 log(float(d)) / (r * log(r)) if float(d) > 1 else float("nan")))
        prev = d

    print()
    print("=" * 96)
    print("PART 3.  Same for C_r(0), and for b=1")
    print("=" * 96)
    print("   %3s | %-16s %-14s | %-16s %-16s %-14s" %
          ("r", "C_r(0)", "C_r/C_{r-1}", "D_r(1)", "D*_r(1)", "gap"))
    prevC = None
    for r in range(1, RMAX + 1):
        c = Cloose(r, 0)
        d1 = Dloose(r, 1)
        ds1 = C.H(r, 1).eval(Fr(1))
        print("   %3d | %-16.6g %-14.6f | %-16.6g %-16.6g %-14.6g"
              % (r, float(c), float(c / prevC) if prevC else float("nan"),
                 float(d1), float(ds1), float(d1 / ds1) if ds1 else float("nan")))
        prevC = c
