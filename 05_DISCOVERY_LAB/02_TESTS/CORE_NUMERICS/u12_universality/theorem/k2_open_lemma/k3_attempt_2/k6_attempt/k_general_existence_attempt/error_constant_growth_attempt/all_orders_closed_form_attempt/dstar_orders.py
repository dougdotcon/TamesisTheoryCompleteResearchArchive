"""
dstar_orders.py -- the sharp order-p residual constants D*^(p)_r(0) = Phi[p]_r(1,b=0),
their exact closed forms (fitted then tested far out of sample), and the
leading-in-r coefficient across orders.

Everything exact (Fraction).  The order-3 and order-4 closed forms are
NUMERICALLY VERIFIED (exact rational, huge out-of-sample range), NOT proved.
"""

import sys
from fractions import Fraction
from core import _ff, _denom, phi_wallis

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5
RTEST = int(sys.argv[2]) if len(sys.argv) > 2 else 300

_C = {}


def s1(N, M):
    if N < 0 or M < 0:
        return 0
    if N == 0:
        return 1 if M == 0 else 0
    if M == 0:
        return 0
    key = (N, M)
    v = _C.get(key)
    if v is None:
        v = (N - 1) * s1(N - 1, M) + s1(N - 1, M - 1)
        _C[key] = v
    return v


def ck(k, r, b):
    if k < 0 or k > r:
        return Fraction(0)
    return Fraction(_ff(r, k, 0), _denom(k, 0, r, b))


def D(p, r, b):
    """Phi[p]_r(1,b) = sum_j c_j^(r)(b) e_p(1..j),  e_p(1..j)=c(j+1,j+1-p)."""
    return sum(ck(j, r, b) * s1(j + 1, j + 1 - p) for j in range(p, r + 1))


def solve(A, bv):
    nv = len(A[0])
    M = [A[i][:] + [bv[i]] for i in range(len(A))]
    piv = 0
    for col in range(nv):
        sel = None
        for i in range(piv, len(M)):
            if M[i][col] != 0:
                sel = i
                break
        if sel is None:
            continue
        M[piv], M[sel] = M[sel], M[piv]
        pv = M[piv][col]
        M[piv] = [x / pv for x in M[piv]]
        for i in range(len(M)):
            if i != piv and M[i][col] != 0:
                f = M[i][col]
                M[i] = [x - f * y for x, y in zip(M[i], M[piv])]
        piv += 1
    return [M[i][nv] for i in range(nv)]


print("=" * 78)
print("D*^(p)_r(0) closed forms at b = 0")
print("  basis for order p: {r^p..r} * varphi_r   plus   {r^(p-1)..r^0}")
print("=" * 78)
known = {
    0: "varphi_r",
    1: "(r/4) varphi_r",
    2: "r(3r+1)/32 varphi_r - r/12",
}
for p in range(0, PMAX + 1):
    fns = ([(lambda q: (lambda r: Fraction(r ** q) * phi_wallis(r)))(q)
            for q in range(p, 0, -1)]
           + [(lambda q: (lambda r: Fraction(r ** q)))(q)
              for q in range(p, -1, -1)])
    nm = (["r^%d phi" % q for q in range(p, 0, -1)]
          + ["r^%d" % q for q in range(p, -1, -1)])
    if p == 0:
        fns = [lambda r: phi_wallis(r), lambda r: Fraction(1)]
        nm = ["phi", "1"]
    rows = list(range(1, len(fns) + 1))
    A = [[f(r) for f in fns] for r in rows]
    bv = [D(p, r, 0) for r in rows]
    sol = solve(A, bv)
    bad = sum(1 for r in range(0, RTEST + 1)
              if sum(sol[i] * fns[i](r) for i in range(len(fns))) != D(p, r, 0))
    expr = " + ".join("(%s)*%s" % (sol[i], nm[i])
                      for i in range(len(fns)) if sol[i] != 0)
    print("  p=%d : %s" % (p, expr if expr else "0"))
    print("        fitted on %d points; out-of-sample exact failures r=0..%d: %d"
          % (len(rows), RTEST, bad))
    if p in known:
        print("        (already PROVED elsewhere: %s)" % known[p])

print()
print("=" * 78)
print("The leading-in-r coefficient across orders")
print("  observed:  D*^(p)_r(0) = [ (2p-1)!!/(4^p p!) ] r^p varphi_r + lower")
print("=" * 78)
for p in range(0, PMAX + 1):
    dfac = 1
    for i in range(2 * p - 1, 0, -2):
        dfac *= i
    fac = 1
    for i in range(1, p + 1):
        fac *= i
    print("  p=%d : (2p-1)!!/(4^p p!) = %s" % (p, Fraction(dfac, 4 ** p * fac)))

print()
print("  first values D*^(p)_r(0), r rows / p columns:")
print("     r  |" + "".join("%22d" % p for p in range(0, min(PMAX, 4) + 1)))
for r in range(0, 12):
    print("   %3d |" % r + "".join("%22s" % D(p, r, 0)
                                   for p in range(0, min(PMAX, 4) + 1)))

print()
print("=" * 78)
print("b >= 1 : does the same basis close?  (it does NOT -- same phenomenon")
print("         the predecessor reported for order 2 at b>=1)")
print("=" * 78)
for p in (2, 3):
    for bb in (1, 2, 3):
        fns = ([(lambda q: (lambda r: Fraction(r ** q) * phi_wallis(r)))(q)
                for q in range(p, 0, -1)]
               + [(lambda q: (lambda r: Fraction(r ** q)))(q)
                  for q in range(p, -1, -1)])
        rows = list(range(1, len(fns) + 1))
        A = [[f(r) for f in fns] for r in rows]
        bv = [D(p, r, bb) for r in rows]
        sol = solve(A, bv)
        bad = sum(1 for r in range(0, 61)
                  if sum(sol[i] * fns[i](r) for i in range(len(fns)))
                  != D(p, r, bb))
        print("  p=%d b=%d : out-of-sample exact failures r=0..60 : %d"
              % (p, bb, bad))
