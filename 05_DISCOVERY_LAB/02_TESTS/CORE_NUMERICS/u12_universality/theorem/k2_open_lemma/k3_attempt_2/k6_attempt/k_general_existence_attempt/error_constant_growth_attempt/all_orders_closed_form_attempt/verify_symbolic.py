"""
verify_symbolic.py -- symbolic (sympy) verification of every algebraic step of
the proof of Theorem A / Theorem B / Theorem M.

Notation used throughout:
    A_j^(r)(b) := r!/(r-j)! * 1/prod_{i=1}^{j+1}(r+b+i)
                = Gamma(r+1)/Gamma(r-j+1) * Gamma(r+b+1)/Gamma(r+b+j+2)
    P_j(m)     := (m+j)!/m! = prod_{i=1}^{j}(m+i) = Gamma(m+j+1)/Gamma(m+1)

    ghat_r(m,b) := sum_{j=0}^{r} A_j^(r)(b) P_j(m) / n^j          (Theorem A)
    hhat_r(a,b) := ((n-a+1)/n) * ghat_r(n-a+1, b+1)               (Theorem B)

Steps proved here:
  S1  A_j^(r)(b) * (j+1+r+b) = r * A_{j-1}^(r-1)(b+1)      [symbolic r,j,b]
  S2  (1+r+b) A_0^(r)(b) = 1                               [symbolic r,b]
  S3  P_j(m) - P_j(m-1) = j P_{j-1}(m) ;  P_j(m-1) = m P_{j-1}(m)  (j>=1)
  S4  prod_{i=1}^{j}(x+i) = sum_k c(j+1,k+1) x^k           [Stirling gen. id.]
  S5  the full non-source identity, symbolic m,n,b, concrete r
  S6  the full source identity (Theorem B <-> source rule), symbolic a,n,b
  S7  the eps^p / t^k extraction: Theorem A  =>  Theorem M
  S8  the h-side closed form, symbolic
"""

import sys
import sympy as sp

RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
JMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 12

r, j, b, m, n, a, k, x, eps, t, s = sp.symbols(
    "r j b m n a k x eps t s", positive=True)


def A_sym(rr, jj, bb):
    """A_j^(r)(b) in Gamma form (valid as a meromorphic identity)."""
    return (sp.gamma(rr + 1) / sp.gamma(rr - jj + 1)
            * sp.gamma(rr + bb + 1) / sp.gamma(rr + bb + jj + 2))


def P_sym(jj, mm):
    return sp.gamma(mm + jj + 1) / sp.gamma(mm + 1)


print("=" * 78)
print("S1 -- A_j^(r)(b) * (j+1+r+b)  ==  r * A_{j-1}^(r-1)(b+1)")
print("      SYMBOLIC in r, j, b")
print("=" * 78)
lhs = A_sym(r, j, b) * (j + 1 + r + b)
rhs = r * A_sym(r - 1, j - 1, b + 1)
d = sp.simplify(sp.expand_func(lhs) - sp.expand_func(rhs))
print("   simplify(LHS - RHS) =", d, "   -> ", d == 0)

print()
print("=" * 78)
print("S2 -- (1+r+b) * A_0^(r)(b) == 1     SYMBOLIC in r, b")
print("=" * 78)
d = sp.simplify(sp.expand_func((1 + r + b) * A_sym(r, 0, b)) - 1)
print("   simplify(...) =", d, "   -> ", d == 0)

print()
print("=" * 78)
print("S3 -- P_j(m) - P_j(m-1) = j P_{j-1}(m)  and  P_j(m-1) = m P_{j-1}(m)")
print("      SYMBOLIC in m, j (Gamma form), plus concrete j=0..%d" % JMAX)
print("=" * 78)
d1 = sp.simplify(sp.expand_func(P_sym(j, m) - P_sym(j, m - 1)
                                - j * P_sym(j - 1, m)))
d2 = sp.simplify(sp.expand_func(P_sym(j, m - 1) - m * P_sym(j - 1, m)))
print("   symbolic-j:  d1 =", d1, "  d2 =", d2, "  ->",
      (d1 == 0 and d2 == 0))
bad = 0
for jj in range(1, JMAX + 1):
    Pj = sp.prod([m + i for i in range(1, jj + 1)])
    Pjm1 = sp.prod([m - 1 + i for i in range(1, jj + 1)])
    Pjm = sp.prod([m + i for i in range(1, jj)])
    if sp.expand(Pj - Pjm1 - jj * Pjm) != 0:
        bad += 1
    if sp.expand(Pjm1 - m * Pjm) != 0:
        bad += 1
print("   concrete j=1..%d (expanded polynomials in m): failures = %d"
      % (JMAX, bad))

print()
print("=" * 78)
print("S4 -- prod_{i=1}^{j}(x+i) = sum_{k} c(j+1,k+1) x^k   (own Stirling impl)")
print("=" * 78)
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


bad = 0
for jj in range(0, JMAX + 4):
    lhs = sp.expand(sp.prod([x + i for i in range(1, jj + 1)]))
    rhs = sp.expand(sum(stirling1u(jj + 1, kk + 1) * x ** kk
                        for kk in range(0, jj + 1)))
    if sp.expand(lhs - rhs) != 0:
        bad += 1
print("   j=0..%d : failures = %d" % (JMAX + 3, bad))
# and against sympy's own stirling numbers, as an independent implementation
bad = 0
for N in range(0, 18):
    for M in range(0, N + 1):
        if stirling1u(N, M) != sp.functions.combinatorial.numbers.stirling(
                N, M, kind=1, signed=False):
            bad += 1
print("   my stirling1u vs sympy.stirling(kind=1,signed=False), N<=17:"
      " failures =", bad)

print()
print("=" * 78)
print("S5 -- THE NON-SOURCE IDENTITY, symbolic m, n, b, for r = 0..%d" % RMAX)
print("      m[ghat_r(m,b)-ghat_r(m-1,b)] + (1+r+b) ghat_r(m-1,b)")
print("            ==  1 + r * hhat_{r-1}(n-m+1, b)")
print("=" * 78)


def A_num(rr, jj, bb):
    """A_j^(r)(b) for CONCRETE integer r,j and symbolic b."""
    if jj < 0 or jj > rr:
        return sp.Integer(0)
    ff = sp.Integer(1)
    for i in range(rr - jj + 1, rr + 1):
        ff *= i
    den = sp.Integer(1)
    for i in range(1, jj + 2):
        den *= (rr + bb + i)
    return sp.together(ff / den)


def ghat(rr, mm, bb):
    tot = 0
    for jj in range(0, rr + 1):
        P = sp.prod([mm + i for i in range(1, jj + 1)])
        tot += A_num(rr, jj, bb) * P / n ** jj
    return tot


def hhat(rr, aa, bb):
    if rr < 0:
        return sp.Integer(0)
    return (n - aa + 1) / n * ghat(rr, n - aa + 1, bb + 1)


bad = 0
for rr in range(0, RMAX + 1):
    lhs = (m * (ghat(rr, m, b) - ghat(rr, m - 1, b))
           + (1 + rr + b) * ghat(rr, m - 1, b))
    rhs = 1 + rr * hhat(rr - 1, n - m + 1, b)
    d = sp.simplify(sp.together(sp.expand(lhs - rhs)))
    if d != 0:
        bad += 1
        print("   FAIL r=%d : %s" % (rr, d))
print("   r=0..%d : failures = %d" % (RMAX, bad))

print()
print("=" * 78)
print("S6 -- THE SOURCE IDENTITY, symbolic a, n, b, for r = 0..%d" % RMAX)
print("      hhat_r(a,b) == 1/n + (r/n) hhat_{r-1}(a,b+1)")
print("                        + ((n-1-a-b-r)/n) ghat_r(n-a, b+1)")
print("=" * 78)
bad = 0
for rr in range(0, RMAX + 1):
    lhs = hhat(rr, a, b)
    rhs = (sp.Rational(1, 1) / n + sp.Integer(rr) / n * hhat(rr - 1, a, b + 1)
           + (n - 1 - a - b - rr) / n * ghat(rr, n - a, b + 1))
    d = sp.simplify(sp.together(sp.expand(lhs - rhs)))
    if d != 0:
        bad += 1
        print("   FAIL r=%d : %s" % (rr, d))
print("   r=0..%d : failures = %d" % (RMAX, bad))

print()
print("=" * 78)
print("S7 -- Theorem A  =>  Theorem M :  substituting m = t*n, 1/n = eps into")
print("      P_j(m)/n^j  gives  prod_{i=1}^{j}(t+i*eps), whose t^k eps^(j-k)")
print("      coefficient is c(j+1,k+1).   Checked as a 2-variable expansion.")
print("=" * 78)
bad = 0
for jj in range(0, JMAX + 2):
    expr = sp.expand(sp.prod([t + i * eps for i in range(1, jj + 1)]))
    for kk in range(0, jj + 1):
        got = sp.expand(expr).coeff(t, kk).coeff(eps, jj - kk)
        want = stirling1u(jj + 1, kk + 1)
        if sp.simplify(got - want) != 0:
            bad += 1
print("   j=0..%d, all k : failures = %d" % (JMAX + 1, bad))

print()
print("=" * 78)
print("S8 -- the h-side all-orders closed form")
print("      Psi[p]_r(s,b) = sum_k c(k+p+1,k+1) * A_{k+p-1}^(r)(b+1) (1-s)^k")
print("      checked against hhat_r(a,b) expanded in eps with s=a/n")
print("=" * 78)
u = sp.Symbol("u", positive=True)   # u = 1 - s
bad = 0
checks = 0
for rr in range(0, min(RMAX, 7) + 1):
    # hhat_r(a,b) = sum_j A_j^(r)(b+1) prod_{i=1}^{j+1}(u + i eps)
    expr = sum(A_num(rr, jj, b + 1)
               * sp.prod([u + i * eps for i in range(1, jj + 2)])
               for jj in range(0, rr + 1))
    expr = sp.expand(expr)
    for pp in range(0, rr + 2):
        for kk in range(0, rr + 3):
            got = sp.simplify(expr.coeff(eps, pp).coeff(u, kk))
            want = sp.simplify(stirling1u(kk + pp + 1, kk + 1)
                               * A_num(rr, kk + pp - 1, b + 1))
            checks += 1
            if sp.simplify(got - want) != 0:
                bad += 1
                if bad < 5:
                    print("   FAIL r=%d p=%d k=%d: %s vs %s" % (rr, pp, kk,
                                                                got, want))
print("   %d checks, failures = %d" % (checks, bad))
