"""
ADVERSARIAL REFEREE, item 1 (symbolic half): independent re-derivation of the
four facts (P1)-(P4) of the target's Sec.4.1, and of the ASSEMBLED identities
(*) and (**) for the closed forms, fully symbolically.

Everything here is written from scratch against my own hand derivation.
"""
import sympy as sp

r, j, b, m, n, a, k, t, eps = sp.symbols('r j b m n a k t epsilon', positive=True)

FAIL = []


def check(tag, expr, want=0):
    e = sp.simplify(sp.together(sp.expand(expr - want)))
    ok = (e == 0)
    print(f"  [{'OK ' if ok else 'FAIL'}] {tag}   -> {e}")
    if not ok:
        FAIL.append(tag)
    return ok


print("=" * 74)
print("S1-S3 : the four elementary facts, symbolically in r, j, b, m")
print("=" * 74)

# A_j^{(r)}(b) = r!/(r-j)! / prod_{i=1}^{j+1}(r+b+i)
#             = Gamma(r+1)/Gamma(r-j+1) * Gamma(r+b+1)/Gamma(r+b+j+2)
Asym = (sp.gamma(r + 1) / sp.gamma(r - j + 1)) * (sp.gamma(r + b + 1) / sp.gamma(r + b + j + 2))


def Ag(rr, jj, bb):
    return (sp.gamma(rr + 1) / sp.gamma(rr - jj + 1)) * (sp.gamma(rr + bb + 1) / sp.gamma(rr + bb + jj + 2))


# (P1)  A_j^{(r)}(b) * (j+1+r+b) = r * A_{j-1}^{(r-1)}(b+1)
check("P1  A_j^{(r)}(b)(j+1+r+b) = r A_{j-1}^{(r-1)}(b+1)",
      Ag(r, j, b) * (j + 1 + r + b) - r * Ag(r - 1, j - 1, b + 1))

# (P2)  (1+r+b) A_0 = 1
check("P2  (1+r+b) A_0^{(r)}(b) = 1", (1 + r + b) * Ag(r, 0, b), 1)

# (P3)  P_j(m)-P_j(m-1) = j P_{j-1}(m) ;  P_j(m-1) = m P_{j-1}(m)
Pg = lambda jj, mm: sp.gamma(mm + jj + 1) / sp.gamma(mm + 1)
check("P3a P_j(m)-P_j(m-1) = j P_{j-1}(m)",
      Pg(j, m) - Pg(j, m - 1) - j * Pg(j - 1, m))
check("P3b P_j(m-1) = m P_{j-1}(m)",
      Pg(j, m - 1) - m * Pg(j - 1, m))

# P3 again as honest polynomials in m for j = 1..14 (no Gamma sleight of hand)
Ppoly = lambda jj, mm: sp.prod([mm + i for i in range(1, jj + 1)])
bad = 0
for jj in range(1, 15):
    if sp.expand(Ppoly(jj, m) - Ppoly(jj, m - 1) - jj * Ppoly(jj - 1, m)) != 0:
        bad += 1
    if sp.expand(Ppoly(jj, m - 1) - m * Ppoly(jj - 1, m)) != 0:
        bad += 1
print(f"  [{'OK ' if bad==0 else 'FAIL'}] P3 as expanded polynomials in m, j=1..14 : {bad} failures")
if bad:
    FAIL.append("P3poly")

# P1 again with honest finite products, r,j,b integers, no Gamma
bad = 0
for rr in range(1, 13):
    for jj in range(1, rr + 1):
        for bb in range(0, 6):
            L = (sp.Rational(sp.ff(rr, jj)) / sp.prod([rr + bb + i for i in range(1, jj + 2)])) * (jj + 1 + rr + bb)
            Rr = rr * (sp.Rational(sp.ff(rr - 1, jj - 1)) / sp.prod([(rr - 1) + (bb + 1) + i for i in range(1, jj + 1)]))
            if sp.simplify(L - Rr) != 0:
                bad += 1
print(f"  [{'OK ' if bad==0 else 'FAIL'}] P1 as honest finite products, r<=12,j<=r,b<=5 : {bad} failures")
if bad:
    FAIL.append("P1finite")


print()
print("=" * 74)
print("S5/S6 : the ASSEMBLED identities (*) and (**) for the closed forms,")
print("        with SYMBOLIC m, a, n, b at each r = 0..9")
print("=" * 74)


def Aex(rr, jj, bb):
    """exact A_j^{(r)}(b) with symbolic b, integer r,j."""
    if jj > rr or jj < 0:
        return sp.Integer(0)
    return sp.Rational(sp.ff(rr, jj)) / sp.prod([rr + bb + i for i in range(1, jj + 2)])


def ghat(rr, mm, bb, nn):
    return sum(Aex(rr, jj, bb) * sp.prod([mm + i for i in range(1, jj + 1)]) / nn ** jj
               for jj in range(0, rr + 1))


def hhat(rr, aa, bb, nn):
    return (nn - aa + 1) / nn * ghat(rr, nn - aa + 1, bb + 1, nn)


for rr in range(0, 10):
    # (*)
    L = m * (ghat(rr, m, b, n) - ghat(rr, m - 1, b, n)) + (1 + rr + b) * ghat(rr, m - 1, b, n)
    R = 1 + (rr * hhat(rr - 1, n - m + 1, b, n) if rr > 0 else 0)
    ok1 = sp.simplify(sp.expand(L - R)) == 0
    # (**)
    L2 = hhat(rr, a, b, n)
    R2 = sp.Rational(1, 1) / n + (rr / n * hhat(rr - 1, a, b + 1, n) if rr > 0 else 0) \
        + ((n - a) / n - (1 + b + rr) / n) * ghat(rr, n - a, b + 1, n)
    ok2 = sp.simplify(sp.expand(L2 - R2)) == 0
    print(f"  r={rr}:  (*) {'OK ' if ok1 else 'FAIL'}    (**) {'OK ' if ok2 else 'FAIL'}")
    if not ok1:
        FAIL.append(f"(*) r={rr}")
    if not ok2:
        FAIL.append(f"(**) r={rr}")


print()
print("=" * 74)
print("S-extra : (*) proved at SYMBOLIC r as well, via the P1/P2/P3 route")
print("=" * 74)
# The referee's own one-line proof, done symbolically at symbolic j:
#   j>=1 term of  m[g(m)-g(m-1)] + (1+r+b) g(m-1)  is
#       A_j/n^j * ( m*j*P_{j-1}(m) + (1+r+b)*m*P_{j-1}(m) )
#     = A_j (j+1+r+b) * m P_{j-1}(m) / n^j
#     = r A_{j-1}^{(r-1)}(b+1) * m P_{j-1}(m) / n^j          (P1)
# so the whole j>=1 block equals (r m / n) * ghat_{r-1}(m, b+1). Check the
# per-term identity symbolically in (r,j,b,m,n):
term_lhs = Ag(r, j, b) / n ** j * (m * (Pg(j, m) - Pg(j, m - 1)) + (1 + r + b) * Pg(j, m - 1))
term_rhs = (r * m / n) * Ag(r - 1, j - 1, b + 1) * Pg(j - 1, m) / n ** (j - 1)
check("per-term  j>=1  (symbolic r,j,b,m,n)", term_lhs - term_rhs)

print()
print("=" * 74)
print("S4 : the Stirling / rising-factorial generating identity, own code")
print("=" * 74)


def unsigned_stirling_first(N, M):
    """own implementation: c(N,M) = c(N-1,M-1) + (N-1) c(N-1,M)"""
    C = [[0] * (N + 1) for _ in range(N + 1)]
    C[0][0] = 1
    for i in range(1, N + 1):
        for q in range(1, i + 1):
            C[i][q] = C[i - 1][q - 1] + (i - 1) * C[i - 1][q]
    return C[N][M]


bad = 0
for N in range(0, 18):
    for M in range(0, N + 1):
        if unsigned_stirling_first(N, M) != int(abs(sp.functions.combinatorial.numbers.stirling(N, M, kind=1, signed=True))):
            bad += 1
print(f"  [{'OK ' if bad==0 else 'FAIL'}] own c(N,M) vs sympy stirling(kind=1), N<=17 : {bad} failures")
if bad:
    FAIL.append("stirling-impl")

x = sp.Symbol('x')
bad = 0
for N in range(0, 16):
    lhs = sp.expand(sp.prod([x + i for i in range(0, N)]))     # x(x+1)...(x+N-1)
    rhs = sp.expand(sum(unsigned_stirling_first(N, M) * x ** M for M in range(0, N + 1)))
    if sp.expand(lhs - rhs) != 0:
        bad += 1
print(f"  [{'OK ' if bad==0 else 'FAIL'}] sum_M c(N,M)x^M = x(x+1)..(x+N-1), N<=15 : {bad} failures")
if bad:
    FAIL.append("stirling-gf")

# the HOMOGENISED form actually used in Sec.3.2:
#   prod_{i=1}^{j}(t + i*eps) = sum_{k=0}^{j} c(j+1,k+1) t^k eps^{j-k}
bad = 0
for jj in range(0, 15):
    lhs = sp.expand(sp.prod([t + i * eps for i in range(1, jj + 1)]))
    rhs = sp.expand(sum(unsigned_stirling_first(jj + 1, kk + 1) * t ** kk * eps ** (jj - kk)
                        for kk in range(0, jj + 1)))
    if sp.expand(lhs - rhs) != 0:
        bad += 1
        print("     homogenised FAIL at j =", jj)
print(f"  [{'OK ' if bad==0 else 'FAIL'}] HOMOGENISED prod_(t+i eps) = sum c(j+1,k+1)t^k eps^(j-k), j<=14 : {bad} failures")
if bad:
    FAIL.append("stirling-homog")

# the four multiplier identifications the target's table claims
bad = 0
for N in range(1, 30):
    if unsigned_stirling_first(N, N) != 1:
        bad += 1
    if N >= 1 and unsigned_stirling_first(N, N - 1) != sp.binomial(N, 2):
        bad += 1
    if N >= 2 and unsigned_stirling_first(N, N - 2) != sp.Rational(3 * N - 1, 4) * sp.binomial(N, 3):
        bad += 1
    if N >= 3 and unsigned_stirling_first(N, N - 3) != sp.binomial(N, 2) * sp.binomial(N, 4):
        bad += 1
print(f"  [{'OK ' if bad==0 else 'FAIL'}] c(N,N)=1, c(N,N-1)=C(N,2), c(N,N-2)=(3N-1)/4 C(N,3), "
      f"c(N,N-3)=C(N,2)C(N,4), N<=29 : {bad} failures")
if bad:
    FAIL.append("stirling-4ids")

# and the target's stated equivalent multiplier form for I_r
bad = 0
for kk in range(0, 30):
    lhs = sp.binomial(kk + 4, 2) * sp.binomial(kk + 4, 4)
    rhs = sp.Rational((kk + 1) * (kk + 2) * (kk + 3) ** 2 * (kk + 4) ** 2, 48)
    if sp.simplify(lhs - rhs) != 0:
        bad += 1
print(f"  [{'OK ' if bad==0 else 'FAIL'}] C(k+4,2)C(k+4,4) = (k+1)(k+2)(k+3)^2(k+4)^2/48, k<=29 : {bad} failures")
if bad:
    FAIL.append("Ir-multiplier-alt")

# and that Theorem M's p=1,2 slices ARE the published d_k, e_k multipliers
bad = 0
for kk in range(0, 30):
    if unsigned_stirling_first(kk + 2, kk + 1) != sp.binomial(kk + 2, 2):
        bad += 1
    if unsigned_stirling_first(kk + 3, kk + 1) != sp.Rational(
            (3 * kk + 8) * (kk + 1) * (kk + 2) * (kk + 3), 24):
        bad += 1
print(f"  [{'OK ' if bad==0 else 'FAIL'}] Thm M p=1,2 == published d_k, e_k multipliers, k<=29 : {bad} failures")
if bad:
    FAIL.append("ThmM-vs-published")

print()
print("=" * 74)
print("VERDICT:", "ALL SYMBOLIC CHECKS PASS" if not FAIL else f"FAILURES: {FAIL}")
print("=" * 74)
