"""
odd_part.py -- the H_{2k-1}(r,b) machine, written FRESH for this front (no
predecessor .py file opened, read, or imported).

Cited, PROVED input (THEOREM.md "Estagio 16"/"Estagio 21";
general_p_dstar_extension_attempt/adversarial/REFEREE_REPORT.md Sec.2a-2b,
restated in general_p_dstar_extension2_attempt/ATTEMPT.md Sec.2.3):

  H_{2k-1}(r,b) := P_b * S_{2k-1}(N,r),  N=2r+b+1,
  the originally-cited recursion:
    S_1(N,m) = (m+1) C(N,m+1)
    S_{2k-1}(N,m) = (N-2m)^{2k-2}(m+1)C(N,m+1)
                    + 2N * sum_{s odd,1<=s<=2k-3} C(2k-2,s) S_s(N-1,m-1)
  and the closed factorization S_{2k-1}(N,m) = A_k(N,m) * C(N,m+1)
  (A_1(N,m):=m+1), which -- using the elementary factorial identity
  C(N-1,m) = (m+1)/N * C(N,m+1) -- yields, dividing through by C(N,m+1):
    A_k(N,m) = (m+1) [ (N-2m)^{2k-2}
                 + 2 sum_{s odd,1<=s<=2k-3} C(2k-2,s) A_{(s+1)/2}(N-1,m-1) ]

REPARAMETRIZATION used here (native to this front, an algebraic observation
made to reach full scale for p up to 80 in practical time): setting
x := m and y := N-2m, the recursion above only ever needs A_j evaluated at
(m-1, (N-1)-2(m-1)) = (x-1, y+1) -- i.e. A_k is really a function of the
TWO variables (x,y) alone, with NO other dependence on N or m individually:

    A_k(x,y) = (x+1) [ y^{2k-2}
                 + 2 sum_{s odd,1<=s<=2k-3} C(2k-2,s) A_{(s+1)/2}(x-1,y+1) ]
    A_1(x,y) = x+1

This is built ONCE as an exact BIVARIATE polynomial in (x,y) -- independent
of any specific (r,b) -- for k=1,...,p_max, then evaluated at x=r, y=beta
(beta=b+1) for any (r,b) pair (H_{2k-1}(r,b) = A_k(r,beta)/(r+1)). This
turns an O(p) rebuild per (p,b) pair into a single build per p, amortized
across all b -- necessary for this front's full-scale target
(p=41..80, r<=200, b<=30): confirmed, before being trusted, to agree
exactly with a per-(p,b) direct-substitution route (self_test below) and
with brute-force cross-checks of the ORIGINAL cited S_{2k-1} recursion.

Bivariate polynomials are represented as a list of univariate (ascending
Fraction-list) polynomials in y, indexed by power of x -- i.e.
bpoly[i] = the y-polynomial coefficient of x^i.
"""
from fractions import Fraction
from math import comb

from ingredients import poly_add, poly_mul, poly_scale, poly_eval, poly_trim, poly_compose_linear

ZERO_Y = [Fraction(0)]
ONE_Y = [Fraction(1)]


# ----------------------------------------------------------------------
# Bivariate polynomial utilities: bpoly = list of y-polys, index = x-power.
# ----------------------------------------------------------------------

def bpoly_trim(A):
    A = [poly_trim(c) for c in A]
    while len(A) > 1 and A[-1] == ZERO_Y:
        A.pop()
    return A


def bpoly_add(A, B):
    n = max(len(A), len(B))
    out = []
    for i in range(n):
        ca = A[i] if i < len(A) else ZERO_Y
        cb = B[i] if i < len(B) else ZERO_Y
        out.append(poly_add(ca, cb))
    return bpoly_trim(out)


def bpoly_scale(A, s):
    return bpoly_trim([poly_scale(c, s) for c in A])


def bpoly_mul(A, B):
    out = [list(ZERO_Y) for _ in range(len(A) + len(B) - 1)]
    for i, ca in enumerate(A):
        if ca == ZERO_Y:
            continue
        for j, cb in enumerate(B):
            if cb == ZERO_Y:
                continue
            out[i + j] = poly_add(out[i + j], poly_mul(ca, cb))
    return bpoly_trim(out)


def bpoly_shift_y(A, dy):
    """Substitute y -> y + dy in each x-coefficient (a y-poly)."""
    return [poly_compose_linear(c, Fraction(1), Fraction(dy)) for c in A]


def bpoly_shift_x(A, dx):
    """Substitute x -> x + dx (A's outer index is x-power); same algorithm
    as poly_compose_linear but with y-poly-valued coefficients."""
    result = [list(ZERO_Y)]
    power = [Fraction(1)]  # (x+dx)^0, a plain x-only poly (Fraction list)
    base = [Fraction(dx), Fraction(1)]  # dx + 1*x
    for k, coeff_ypoly in enumerate(A):
        if coeff_ypoly != ZERO_Y:
            term_bpoly = [poly_scale(coeff_ypoly, p_i) for p_i in power]
            result = bpoly_add(result, term_bpoly)
        if k != len(A) - 1:
            power = poly_mul(power, base)
    return bpoly_trim(result)


def bpoly_eval_y(A, y_val):
    """Collapse a bpoly to a plain x-poly (ascending Fraction list) by
    evaluating every y-poly coefficient at y=y_val."""
    return poly_trim([poly_eval(c, y_val) for c in A])


def y_power_bpoly(n):
    """The bpoly representing y^n (x^0 coefficient only)."""
    yp = [Fraction(0)] * (n + 1)
    yp[n] = Fraction(1)
    return [yp]


X_PLUS_1 = [ONE_Y, ONE_Y]  # (x+1) as a bpoly: x^0 coeff=1, x^1 coeff=1


# ----------------------------------------------------------------------
# The A_k(x,y) bivariate table, built ONCE per k_max (independent of r,b).
# ----------------------------------------------------------------------

_A_all = {}  # single persistent, monotonically-growing table: k -> A_k(x,y)
_A_max_built = [0]


def build_A_table(k_max):
    """Return dict k -> A_k(x,y), bpoly, for k=1,...,k_max. Built ONCE,
    incrementally extended (never rebuilt from scratch) as larger k_max
    values are requested across the run, and reusable for every (r,b)
    pair -- this single running table is what makes the full-scale sweep
    (p up to 80, b up to 30) tractable: the expensive bivariate recursion
    is paid for once, not once per (p,b) pair."""
    if k_max > _A_max_built[0]:
        for k in range(_A_max_built[0] + 1, k_max + 1):
            if k == 1:
                _A_all[1] = [list(ONE_Y), list(ONE_Y)]  # x+1
            else:
                bracket = y_power_bpoly(2 * k - 2)
                for s in range(1, 2 * k - 2, 2):
                    jj = (s + 1) // 2
                    shifted = bpoly_shift_x(bpoly_shift_y(_A_all[jj], 1), -1)  # A_jj(x-1,y+1)
                    coeff = 2 * comb(2 * k - 2, s)
                    bracket = bpoly_add(bracket, bpoly_scale(shifted, Fraction(coeff)))
                _A_all[k] = bpoly_mul(X_PLUS_1, bracket)
        _A_max_built[0] = k_max
    return {k: _A_all[k] for k in range(1, k_max + 1)}


def poly_div_exact(a, root):
    """Divide polynomial a (ascending Fraction list) by (x - root) exactly,
    via synthetic division; asserts zero remainder."""
    n = len(a)
    desc = list(reversed(a))
    quotient_desc = [Fraction(0)] * (n - 1)
    carry = desc[0]
    quotient_desc[0] = carry
    for i in range(1, n - 1):
        carry = desc[i] + carry * root
        quotient_desc[i] = carry
    remainder = desc[-1] + carry * root
    if remainder != 0:
        raise ValueError(f"poly_div_exact: nonzero remainder {remainder}")
    return poly_trim(list(reversed(quotient_desc)))


_H_table_cache = {}


def build_H_table(p_max, b):
    """Return dict k -> H_{2k-1}(r,b), polynomial in r (ascending Fraction
    list), for k=1,...,p_max, fixed b. Uses the bpoly A_k(x,y) table
    (built once, shared across every b) collapsed at y=beta."""
    key = (p_max, b)
    if key in _H_table_cache:
        return _H_table_cache[key]
    beta = Fraction(b + 1)
    A = build_A_table(p_max)
    H = {}
    for k in range(1, p_max + 1):
        if k == 1:
            H[k] = [Fraction(1)]
        else:
            a_k0_r = bpoly_eval_y(A[k], beta)  # A_k(r, beta), poly in r=x
            H[k] = poly_div_exact(a_k0_r, Fraction(-1))
    _H_table_cache[key] = H
    return H


# ----------------------------------------------------------------------
# Independent cross-checks
# ----------------------------------------------------------------------

def S_odd_direct(k, N, m):
    """Brute-force, independent re-implementation of the ORIGINALLY-cited
    S_{2k-1}(N,m) recursion -- no A_k factorization, no bivariate
    reparametrization at all -- used purely as a cross-check."""
    cache = {}

    def C(n, r):
        if r < 0 or r > n or n < 0:
            return Fraction(0)
        return Fraction(comb(n, r))

    def S(kk, NN, mm):
        key = (kk, NN, mm)
        if key in cache:
            return cache[key]
        if kk == 1:
            val = (mm + 1) * C(NN, mm + 1)
        else:
            val = (Fraction(NN - 2 * mm) ** (2 * kk - 2)) * (mm + 1) * C(NN, mm + 1)
            total = Fraction(0)
            for s in range(1, 2 * kk - 2, 2):
                jj = (s + 1) // 2
                total += comb(2 * kk - 2, s) * S(jj, NN - 1, mm - 1)
            val += 2 * NN * total
        cache[key] = val
        return val

    return S(k, N, m)


def S_odd_closed_sum(k, N, m):
    """A FOURTH, independent definition/route:
        S_{2k-1}(N,m) = sum_{i=0}^{m} (N-2i)^{2k-1} C(N,i)
    used as an additional independent cross-check."""
    total = Fraction(0)
    for i in range(0, m + 1):
        total += (Fraction(N - 2 * i) ** (2 * k - 1)) * comb(N, i)
    return total


def H_odd_via_S(k, r, b):
    """H_{2k-1}(r,b) := P_b * S_{2k-1}(N,r), computed via brute-force
    S_odd_direct (not the bpoly route) -- an independent cross-check."""
    import math as _m
    N = 2 * r + b + 1
    S = S_odd_direct(k, N, r)
    P_b = Fraction(_m.factorial(r) * _m.factorial(r + b), _m.factorial(N))
    return P_b * S


def a_k_direct_substitution(k, r, b):
    """A THIRD route, independent of the bpoly table: the ORIGINAL
    depth-indexed recursion a_k^{(d)}(r), built by direct numeric
    substitution at a FIXED (r,b) (not bivariate at all), exactly as one
    would implement it without the (x,y)-reparametrization insight. Used
    to cross-validate that the bpoly route's collapse-at-y=beta genuinely
    agrees with the "obvious" per-(r,b) recursive route."""
    beta = b + 1
    cache = {}

    def a(kk, d):
        key = (kk, d)
        if key in cache:
            return cache[key]
        if kk == 1:
            val = Fraction(r - d + 1)
        else:
            bracket = Fraction((beta + d) ** (2 * kk - 2))
            for s in range(1, 2 * kk - 2, 2):
                jj = (s + 1) // 2
                bracket += 2 * comb(2 * kk - 2, s) * a(jj, d + 1)
            val = Fraction(r - d + 1) * bracket
        cache[key] = val
        return val

    return a(k, 0)


def self_test():
    checks = 0
    fails = 0

    # (0) bpoly route vs the direct per-(r,b) depth-recursion route (a
    #     THIRD, independent implementation of the same math, no
    #     bivariate machinery at all).
    for k in range(1, 12):
        for r in range(0, 10):
            for b in (0, 1, 2, 5, 8):
                checks += 1
                H_table = build_H_table(max(k, 1), b)
                got = poly_eval(H_table[k], Fraction(r))
                if k == 1:
                    want = Fraction(1)
                else:
                    want = a_k_direct_substitution(k, r, b) / (r + 1)
                if got != want:
                    fails += 1
                    print(f"MISMATCH direct-substitution k={k} r={r} b={b}: {got} vs {want}")

    # (1) Against brute-force S_odd_direct (original cited recursion, no
    #     A_k factorization at all).
    for k in range(1, 10):
        for r in range(0, 10):
            for b in (0, 1, 2, 5, 8):
                checks += 1
                H_table = build_H_table(max(k, 1), b)
                got = poly_eval(H_table[k], Fraction(r))
                want = H_odd_via_S(k, r, b)
                if got != want:
                    fails += 1
                    print(f"MISMATCH S_odd_direct k={k} r={r} b={b}: {got} vs {want}")

    # (1b) Against the fourth, independent closed-sum definition of
    #      S_{2k-1}, also via P_b, k up to 8.
    for k in range(1, 9):
        for r in range(0, 10):
            for b in (0, 1, 3, 7):
                checks += 1
                import math as _m
                N = 2 * r + b + 1
                S = S_odd_closed_sum(k, N, r)
                P_b = Fraction(_m.factorial(r) * _m.factorial(r + b), _m.factorial(N))
                want = P_b * S
                H_table = build_H_table(max(k, 1), b)
                got = poly_eval(H_table[k], Fraction(r))
                if got != want:
                    fails += 1
                    print(f"MISMATCH S_odd_closed_sum k={k} r={r} b={b}: {got} vs {want}")

    # (2) Two printed base cases: H_1=1, H_3=(b+1)^2+4r
    #     (cited in THEOREM.md "Estagio 16"/"Estagio 21").
    for b in range(0, 6):
        H_table = build_H_table(3, b)
        for r in range(0, 15):
            checks += 1
            if poly_eval(H_table[1], Fraction(r)) != 1:
                fails += 1
                print(f"MISMATCH H_1 b={b} r={r}")
            checks += 1
            want_H3 = (b + 1) ** 2 + 4 * r
            got_H3 = poly_eval(H_table[2], Fraction(r))
            if got_H3 != want_H3:
                fails += 1
                print(f"MISMATCH H_3 b={b} r={r}: got={got_H3} want={want_H3}")

    # (3) Degree bound deg_r H_{2k-1}(r,b) = k-1, leading coefficient
    #     4^{k-1}(k-1)! (b-independent) -- CITED as PROVED (wave-16
    #     referee), re-checked numerically here up to k=80 (this front's
    #     target range).
    import math as _m
    for k in range(1, 81):
        H_table = build_H_table(k, 0)  # build once, reuse across b below
        for b in (0, 1, 3, 7, 30):
            H_table_b = build_H_table(k, b)
            poly = poly_trim(H_table_b[k])
            checks += 1
            expected_deg = k - 1
            actual_deg = len(poly) - 1
            if actual_deg != expected_deg:
                fails += 1
                print(f"MISMATCH degree k={k} b={b}: got_deg={actual_deg} want_deg={expected_deg}")
            else:
                checks += 1
                lead = poly[-1]
                want_lead = Fraction(4 ** (k - 1) * _m.factorial(k - 1))
                if lead != want_lead:
                    fails += 1
                    print(f"MISMATCH leading coeff k={k} b={b}: got={lead} want={want_lead}")

    # (4) Cross-consistency between two different k_max table-build sizes.
    for k in range(1, 7):
        for b in (0, 4):
            H_a = build_H_table(6, b)[k]
            H_b = build_H_table(20, b)[k]
            for r in range(0, 8):
                checks += 1
                va = poly_eval(H_a, Fraction(r))
                vb = poly_eval(H_b, Fraction(r))
                if va != vb:
                    fails += 1
                    print(f"MISMATCH k_max-consistency k={k} b={b} r={r}: {va} vs {vb}")

    print(f"odd_part.py self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = self_test()
    print("odd_part.py: OK" if ok else "odd_part.py: FAILED")
