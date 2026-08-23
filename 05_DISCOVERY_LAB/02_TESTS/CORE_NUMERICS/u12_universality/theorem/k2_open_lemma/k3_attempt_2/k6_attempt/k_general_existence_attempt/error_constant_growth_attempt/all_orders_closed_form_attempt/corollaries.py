"""
corollaries.py -- the tidy binomial forms of Theorem A, the exact psi_n^(K)
formula, and the all-orders sharp residual constants D*^(p)_r(b).
"""

import sys
from fractions import Fraction
import math
from core import Chain, _ff, _denom, phi_wallis

_C = {}


def stirling1u(N, M):
    if N < 0 or M < 0:
        return 0
    if N == 0:
        return 1 if M == 0 else 0
    if M == 0:
        return 0
    key = (N, M)
    v = _C.get(key)
    if v is None:
        v = (N - 1) * stirling1u(N - 1, M) + stirling1u(N - 1, M - 1)
        _C[key] = v
    return v


def c_k(k, r, b):
    """the ALREADY-PROVED leading-order coefficient  c_k^(r)(b)."""
    if k < 0 or k > r:
        return Fraction(0)
    return Fraction(_ff(r, k, 0), _denom(k, 0, r, b))


def g_A(m, b, r, n):
    """Theorem A in its primary form."""
    tot = Fraction(0)
    P = 1
    for j in range(0, r + 1):
        tot += c_k(j, r, b) * Fraction(P, n ** j)
        P *= (m + j + 1)
    return tot


def g_binom(m, b, r, n):
    """Theorem A in binomial form:
       g_r(m,b) = r!(r+b)!/(2r+b+1)! * sum_j C(2r+b+1, r-j) (m+j)!/(m! n^j)"""
    N = 2 * r + b + 1
    pre = Fraction(math.factorial(r) * math.factorial(r + b), math.factorial(N))
    tot = Fraction(0)
    P = 1
    for j in range(0, r + 1):
        tot += math.comb(N, r - j) * Fraction(P, n ** j)
        P *= (m + j + 1)
    return pre * tot


def h_binom(a, b, r, n):
    N = 2 * r + b + 2
    pre = Fraction(math.factorial(r) * math.factorial(r + b + 1),
                   math.factorial(N))
    tot = Fraction(0)
    P = 1                      # (n-a+1+j)!/(n-a)!  built up
    base = n - a
    P = base + 1
    for j in range(0, r + 1):
        tot += math.comb(N, r - j) * Fraction(P, n ** (j + 1))
        P *= (base + j + 2)
    return pre * tot


def psi_binom(K, n):
    """psi_n^(K) = varphi_K/4^K * sum_j C(2K+1,K-j) (n+j)!/(n! n^j)"""
    tot = Fraction(0)
    P = 1
    for j in range(0, K + 1):
        tot += math.comb(2 * K + 1, K - j) * Fraction(P, n ** j)
        P *= (n + j + 1)
    return Fraction(phi_wallis(K), 4 ** K) * tot


ok = fail = 0


def check(name, cond):
    global ok, fail
    if cond:
        ok += 1
        print("   [PASS] %s" % name)
    else:
        fail += 1
        print("   [FAIL] %s" % name)


print("=" * 78)
print("C1 -- the binomial forms agree with the primary form and the simulator")
print("=" * 78)
bad = 0
cnt = 0
for n in range(2, 26):
    ch = Chain(n)
    for r in range(0, min(n, 9)):
        for b in range(0, min(n - r, 7)):
            for m in range(b + r + 1, n + 1):
                if (n - m) + b + r >= n:
                    continue
                cnt += 1
                v = ch.g_r(m, b, r)
                if v != g_A(m, b, r, n) or v != g_binom(m, b, r, n):
                    bad += 1
            for a in range(0, n - b - r):
                cnt += 1
                if ch.h_r(a, b, r) != h_binom(a, b, r, n):
                    bad += 1
check("%d exact checks of both binomial forms vs the simulator" % cnt, bad == 0)

bad = 0
for K in range(0, 9):
    for n in range(K + 1, 30):
        if psi_binom(K, n) != Chain(n).g(0, 0, K):
            bad += 1
check("psi_n^(K) = varphi_K/4^K sum_j C(2K+1,K-j)(n+j)!/(n! n^j),"
      " K<=8, n<=29", bad == 0)

print()
print("=" * 78)
print("C2 -- the exact psi_n^(K) polynomials, written out, K = 0..8")
print("      (K=1..5 match the PROVED formulas of waves 5 / k3_attempt_2;")
print("       K=6,7,8 are new outputs of the formula)")
print("=" * 78)
import sympy as sp
nn = sp.Symbol("n", positive=True)
for K in range(0, 9):
    tot = 0
    P = sp.Integer(1)
    for j in range(0, K + 1):
        tot += sp.Rational(math.comb(2 * K + 1, K - j)) * P / nn ** j
        P *= (nn + j + 1)
    expr = sp.nsimplify(sp.Rational(phi_wallis(K).numerator,
                                    phi_wallis(K).denominator)
                        / sp.Integer(4) ** K) * tot
    expr = sp.cancel(sp.together(sp.expand(expr)))
    print("   psi_n^(%d) = %s" % (K, expr))

print()
print("=" * 78)
print("C3 -- the sharp all-orders residual constants")
print("     D*^(p)_r(b) = Phi[p]_r(1,b) = sum_j c_j^(r)(b) * e_p(1,...,j)")
print("     with e_p(1..j) = c(j+1, j+1-p)  (elementary symmetric = Stirling)")
print("=" * 78)


def Dstar(p, r, b):
    tot = Fraction(0)
    for j in range(p, r + 1):
        tot += c_k(j, r, b) * stirling1u(j + 1, j + 1 - p)
    return tot


def Dstar_direct(p, r, b):
    tot = Fraction(0)
    for k in range(0, r - p + 1):
        tot += Fraction(stirling1u(k + p + 1, k + 1) * _ff(r, k, p),
                        _denom(k, p, r, b))
    return tot


bad = sum(1 for p in range(0, 6) for r in range(0, 30) for b in range(0, 4)
          if Dstar(p, r, b) != Dstar_direct(p, r, b))
check("the two evaluations of D*^(p)_r(b) agree, p<=5, r<=29, b<=3", bad == 0)

print()
print("   the ALREADY-PROVED entries recovered:")
check("p=0: D*^(0)_r(0) = varphi_r  (r<=60)",
      all(Dstar(0, r, 0) == phi_wallis(r) for r in range(0, 61)))
check("p=1: D*^(1)_r(0) = r varphi_r/4  (r<=60)",
      all(Dstar(1, r, 0) == Fraction(r, 4) * phi_wallis(r)
          for r in range(0, 61)))
check("p=2: D*^(2)_r(0) = r(3r+1)/32 varphi_r - r/12  (r<=60)",
      all(Dstar(2, r, 0) == Fraction(r * (3 * r + 1), 32) * phi_wallis(r)
          - Fraction(r, 12) for r in range(0, 61)))

print()
print("   NEW, order 1/n^3 -- fit a closed form in the basis")
print("   {r^3 phi_r, r^2 phi_r, r phi_r, r^2, r, 1} and then TEST it far out")
import itertools
basis = [lambda r: Fraction(r ** 3) * phi_wallis(r),
         lambda r: Fraction(r ** 2) * phi_wallis(r),
         lambda r: Fraction(r) * phi_wallis(r),
         lambda r: Fraction(r ** 2),
         lambda r: Fraction(r),
         lambda r: Fraction(1)]
names = ["r^3 phi_r", "r^2 phi_r", "r phi_r", "r^2", "r", "1"]
rows = list(range(1, 7))
Amat = [[f(r) for f in basis] for r in rows]
bvec = [Dstar(3, r, 0) for r in rows]
# exact Gaussian elimination
M = [row[:] + [bvec[i]] for i, row in enumerate(Amat)]
nvar = len(basis)
piv = 0
for col in range(nvar):
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
sol = [M[i][nvar] for i in range(nvar)]
print("   fitted: " + " + ".join("(%s)*%s" % (sol[i], names[i])
                                 for i in range(nvar) if sol[i] != 0))
bad = 0
for r in range(0, 121):
    v = sum(sol[i] * basis[i](r) for i in range(nvar))
    if v != Dstar(3, r, 0):
        bad += 1
check("the fitted form reproduces D*^(3)_r(0) EXACTLY for r=0..120"
      " (fitted on 6 points, tested on 121)", bad == 0)

print()
print("   the same fit at b=1,2,3 (does the shape survive?)")
for bb in range(1, 4):
    bvec = [Dstar(3, r, bb) for r in rows]
    M = [row[:] + [bvec[i]] for i, row in enumerate(Amat)]
    piv = 0
    for col in range(nvar):
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
    s2 = [M[i][nvar] for i in range(nvar)]
    bad = sum(1 for r in range(0, 61)
              if sum(s2[i] * basis[i](r) for i in range(nvar))
              != Dstar(3, r, bb))
    print("      b=%d : fit %s  -> extrapolation failures r=0..60: %d"
          % (bb, [str(x) for x in s2], bad))

print()
print("=" * 78)
print("SUMMARY:  %d passed, %d failed" % (ok, fail))
print("=" * 78)
