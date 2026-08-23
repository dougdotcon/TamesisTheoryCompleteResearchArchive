"""Own bivariate polynomial arithmetic over Q in (t,h), plus the exact
substitution objects Delta_r (2-term) and Delta_r^(3) (3-term), and the error
constants A,B,D,C at both orders.  Written from scratch."""

from fractions import Fraction as Fr
from ref_core import pnorm1


def bz():
    return {}


def bfrom_t(p):
    """univariate poly in t -> bivariate."""
    return {(k, 0): c for k, c in enumerate(p) if c != 0}


def badd(P, Q):
    out = dict(P)
    for k, v in Q.items():
        out[k] = out.get(k, Fr(0)) + v
        if out[k] == 0:
            del out[k]
    return out


def bsub(P, Q):
    return badd(P, {k: -v for k, v in Q.items()})


def bscale(P, c):
    c = Fr(c)
    if c == 0:
        return {}
    return {k: v * c for k, v in P.items()}


def bmul(P, Q):
    out = {}
    for (i1, j1), v1 in P.items():
        for (i2, j2), v2 in Q.items():
            k = (i1 + i2, j1 + j2)
            out[k] = out.get(k, Fr(0)) + v1 * v2
    return {k: v for k, v in out.items() if v != 0}


def bconst(c):
    c = Fr(c)
    return {} if c == 0 else {(0, 0): c}


B_T = {(1, 0): Fr(1)}
B_H = {(0, 1): Fr(1)}
B_T_MINUS_H = {(1, 0): Fr(1), (0, 1): Fr(-1)}          # t - h
B_ONEMT_PLUS_H = {(0, 0): Fr(1), (1, 0): Fr(-1), (0, 1): Fr(1)}   # (1-t)+h


def bcompose(p, X):
    """univariate poly p, evaluated at bivariate X (Horner)."""
    acc = {}
    for c in reversed(p):
        acc = badd(bmul(acc, X), bconst(c))
    return acc


def bdiv_h(P):
    """divide by h; asserts every monomial has h-degree >= 1."""
    out = {}
    for (i, j), v in P.items():
        assert j >= 1, "not divisible by h"
        out[(i, j - 1)] = v
    return out


def bmul_t(P):
    return {(i + 1, j): v for (i, j) in P for v in [P[(i, j)]]}


def bh_coeff(P, j):
    """coefficient of h^j, as a univariate poly in t (list)."""
    m = max([i for (i, jj) in P if jj == j], default=-1)
    if m < 0:
        return [Fr(0)]
    out = [Fr(0)] * (m + 1)
    for (i, jj), v in P.items():
        if jj == j:
            out[i] = v
    return out


def bmax_h(P):
    return max([j for (_, j) in P], default=0)


# ---------------------------------------------------------------------------


def delta2(lad, r, b):
    """Delta_r(t,b,h): the exact Taylor tail of the 2-term substitution.

    S = (t/h)[X(t) - X(t-h)] + (1+r+b) X(t-h) - 1 - r*Y((1-t)+h)
    with X = F_r + h G_r  and  Y = Hhat_{r-1} + h K_{r-1}.
    """
    F, G = lad.F[(r, b)], lad.G[(r, b)]
    X = badd(bfrom_t(F), bmul(B_H, bfrom_t(G)))
    Xs = badd(bcompose(F, B_T_MINUS_H), bmul(B_H, bcompose(G, B_T_MINUS_H)))
    term1 = bmul_t(bdiv_h(bsub(X, Xs)))
    term2 = bscale(Xs, 1 + r + b)
    src = bconst(1)
    if r >= 1:
        Y = badd(bcompose(lad.Hh[(r - 1, b)], B_ONEMT_PLUS_H),
                 bmul(B_H, bcompose(lad.K[(r - 1, b)], B_ONEMT_PLUS_H)))
        src = badd(src, bscale(Y, r))
    return bsub(badd(term1, term2), src)


def delta3(lad, r, b):
    """Delta_r^(3)(t,b,h): same, with the third term added."""
    F, G, H = lad.F[(r, b)], lad.G[(r, b)], lad.H[(r, b)]
    HH = bmul(B_H, B_H)
    X = badd(badd(bfrom_t(F), bmul(B_H, bfrom_t(G))), bmul(HH, bfrom_t(H)))
    Xs = badd(badd(bcompose(F, B_T_MINUS_H),
                   bmul(B_H, bcompose(G, B_T_MINUS_H))),
              bmul(HH, bcompose(H, B_T_MINUS_H)))
    term1 = bmul_t(bdiv_h(bsub(X, Xs)))
    term2 = bscale(Xs, 1 + r + b)
    src = bconst(1)
    if r >= 1:
        Y = badd(badd(bcompose(lad.Hh[(r - 1, b)], B_ONEMT_PLUS_H),
                      bmul(B_H, bcompose(lad.K[(r - 1, b)], B_ONEMT_PLUS_H))),
                 bmul(HH, bcompose(lad.L[(r - 1, b)], B_ONEMT_PLUS_H)))
        src = badd(src, bscale(Y, r))
    return bsub(badd(term1, term2), src)


def A_of(lad, r, b, order):
    """A_r(b) = sum_{k>=order} ||q_k(.,b)||  (order=2 for 2-term, 3 for 3-term)."""
    D = delta3(lad, r, b) if order == 3 else delta2(lad, r, b)
    tot = Fr(0)
    for j in range(order, bmax_h(D) + 1):
        tot += pnorm1(bh_coeff(D, j))
    return tot


def brackets_vanish(lad, r, b, order):
    D = delta3(lad, r, b) if order == 3 else delta2(lad, r, b)
    return [all(c == 0 for c in bh_coeff(D, j)) for j in range(0, order)]


def B_of(lad, r, b, order):
    if r == 0:
        return Fr(0)
    if order == 2:
        return (pnorm1(lad.K[(r - 1, b + 1)])
                + (1 + b + r) * pnorm1(lad.G[(r, b + 1)]))
    return (r * pnorm1(lad.L[(r - 1, b + 1)])
            + (1 + b + r) * pnorm1(lad.H[(r, b + 1)]))


def constants(lad, R, B, order, kappa=2, geo=False):
    """D_r(b), C_r(b) by the lineage's recursion.

    kappa : coefficient on D_r(b+1) in the C-recursion (2 = predecessor's
            literal |(1-s)-(1+b+r)/n| <= 2 ; 1 = the [0,1] improvement).
    geo   : if True use the (G1) improvement r/n <= r/(b+r+1) on the
            C_{r-1}(b+1) term (Proposition 6).
    """
    Dc, Cc = {}, {}
    BMAX = lad.BMAX - 1
    assert R <= lad.R and B <= BMAX - R - 1
    for b in range(0, BMAX + 1):
        Dc[(0, b)] = Fr(0)
        Cc[(0, b)] = Fr(0)
    for r in range(1, R + 1):
        # D_r(b) defined for b <= BMAX-r ; needs C_{r-1}(b) (b <= BMAX-r+1-1) OK
        for b in range(0, BMAX - r + 1):
            Dc[(r, b)] = (r * Cc[(r - 1, b)] + A_of(lad, r, b, order)) / (r + b + 1)
        # C_r(b) defined for b <= BMAX-r-1 ; needs D_r(b+1) and C_{r-1}(b+1)
        for b in range(0, BMAX - r):
            coef = Fr(r, b + r + 1) if geo else Fr(r)
            Cc[(r, b)] = (B_of(lad, r, b, order) + coef * Cc[(r - 1, b + 1)]
                          + kappa * Dc[(r, b + 1)])
    return Dc, Cc
