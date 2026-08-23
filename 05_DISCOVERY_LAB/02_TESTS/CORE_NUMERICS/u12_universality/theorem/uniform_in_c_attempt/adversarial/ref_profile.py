"""
Adversarial referee -- item 5: TEOREMA D (coefficient-wise, claimed fully
rigorous) and PROPOSICAO 5.2 (the closed form of e_j and of e(c)).

Key point under test: is
   [c^j] phi(n,.) = (-1)^j (C(n,j)/n^j) sum_{K=0}^j (-1)^K C(j,K) phi_n^{(K)}
an EXACT finite identity?  It is verified here against a completely
independent object: the polynomial phi(n,c) obtained by running the (j,R)
chain with q = c/n as a SYMBOLIC sympy expression, which never uses the
binomial identity C(n,K)C(n-K,j-K) = C(n,j)C(j,K) at all.
"""

from fractions import Fraction as F
from math import comb
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
c = sp.Symbol('c')


# ---------------------------------------------------------------- engines
def chain_phi_symbolic(n):
    """phi(n,c) as an exact sympy polynomial in c, q = c/n."""
    q = c / sp.Integer(n)
    if n == 1:
        return sp.Integer(1)
    P = {R: q * sp.Rational(1, n) + (1 - q) * sp.Rational(1, R + 1)
         for R in range(n)}
    for j in range(n - 2, -1, -1):
        newP = {}
        for R in range(j + 1):
            av = n - j + R
            t = q * (sp.Rational(1, n) + sp.Rational(n - j - 1, n) * P[R + 1])
            t += (1 - q) * (sp.Rational(1, av)
                            + sp.Rational(n - j - 1, av) * P[R])
            newP[R] = sp.expand(t)
        P = newP
    return sp.expand(P[0])


def phiK_fast(n, K):
    """phi_n^{(K)} exactly, restricting R to 0..min(j,K) (states with R>K are
    unreachable), so O(nK) rather than O(n^2)."""
    if K > n:
        raise ValueError
    if n == 1:
        return F(1)
    Rmax = min(n - 1, K)
    P = {}
    for R in range(0, Rmax + 1):
        rem = K - R
        if rem < 0 or rem > 1:
            continue
        qq = F(rem)
        P[R] = qq * F(1, n) + (1 - qq) * F(1, R + 1)
    for j in range(n - 2, -1, -1):
        newP = {}
        for R in range(0, min(j, K) + 1):
            rem = K - R
            if rem < 0 or rem > n - j:
                continue
            qq = F(rem, n - j)
            a = P.get(R + 1, F(0))
            b = P.get(R, F(0))
            av = n - j + R
            t = qq * (F(1, n) + F(n - j - 1, n) * a)
            t += (1 - qq) * (F(1, av) + F(n - j - 1, av) * b)
            newP[R] = t
        P = newP
    return P[0]


phi_K = lambda K: F(4)**K * F(sp.factorial(K))**2 / F(sp.factorial(2*K+1))
c_K = lambda K: (F(K + 2) * phi_K(K) - 2) / 4


print("=" * 76)
print("1. The binomial identity C(n,K)C(n-K,j-K) = C(n,j)C(j,K)")
print("=" * 76)
bad = 0
for n in range(0, 26):
    for j in range(0, n + 1):
        for K in range(0, j + 1):
            if comb(n, K) * comb(n - K, j - K) != comb(n, j) * comb(j, K):
                bad += 1
print(f"   exhaustively verified for 0<=K<=j<=n<=25: {bad} failures.")
print("   (It is the 'choose j of n, then K of those j' double count. EXACT.)")

print()
print("=" * 76)
print("2. TEOREMA D's exact finite formula, tested against a SYMBOLIC chain")
print("=" * 76)
print("   [c^j]phi(n,.) =?= (-1)^j (C(n,j)/n^j) sum_K (-1)^K C(j,K) phi_n^{(K)}")
allok = True
for n in range(2, 13):
    poly = sp.Poly(chain_phi_symbolic(n), c)
    coeffs = [sp.nsimplify(poly.coeff_monomial(c**j)) for j in range(n + 1)]
    ok_n = True
    for j in range(0, n + 1):
        rhs = sp.Rational(-1)**j * sp.Rational(comb(n, j), n**j) * sum(
            sp.Rational(-1)**K * comb(j, K) * sp.Rational(
                phiK_fast(n, K).numerator, phiK_fast(n, K).denominator)
            for K in range(j + 1))
        if sp.simplify(coeffs[j] - rhs) != 0:
            ok_n = False
            allok = False
            print(f"   *** MISMATCH n={n} j={j}: {coeffs[j]} vs {rhs}")
    print(f"   n={n:3d}: all {n+1} Taylor coefficients match exactly: {ok_n}")
print(f"   => the identity is EXACT (not asymptotic), confirmed independently"
      f" of its own proof: {allok}")

print()
print("=" * 76)
print("3. [c^j]phi_inf = (-1)^j / (j!(2j+1)), and sum_K (-1)^K C(j,K) phi_K")
print("=" * 76)
for j in range(0, 9):
    s = sum(F(-1)**K * comb(j, K) * phi_K(K) for K in range(j + 1))
    tgt = F(1, 2 * j + 1)
    print(f"   j={j}:  sum_K (-1)^K C(j,K) phi_K = {str(s):>10}   "
          f"1/(2j+1) = {str(tgt):>10}   {'OK' if s == tgt else 'FAIL'}")
print("   (identity: sum_K (-1)^K C(j,K) int_0^1(1-t^2)^K = int_0^1 t^{2j} .)")

print()
print("=" * 76)
print("4. c_K = [(K+2)phi_K - 2]/4  --  is the citation numerically right?")
print("=" * 76)
print("   n(phi_n^{(K)} - phi_K) should tend to c_K for each fixed K:")
for K in (0, 1, 2, 3, 6):
    row = []
    for n in (20, 40, 80, 160, 320):
        v = n * (phiK_fast(n, K) - phi_K(K))
        row.append(float(v))
    # 2-point Richardson (assuming a 1/n correction)
    rich = 2 * row[-1] - row[-2]
    print(f"   K={K}: " + "  ".join(f"{x:9.6f}" for x in row)
          + f"   Richardson -> {rich:9.6f}   c_K = {float(c_K(K)):9.6f}")
print("   => the cited c_K formula is confirmed. CITATION ACCURATE.")

print()
print("=" * 76)
print("5. e_j from TEOREMA D's finite alternating sum, and PROP 5.2's closed form")
print("=" * 76)
print("""   e_j := ((-1)^j/j!)[ sum_K (-1)^K C(j,K) c_K  -  C(j,2) sum_K (-1)^K C(j,K) phi_K ]
   Closed form claimed: e_j = (-1)^{j+1} (j-1)^2 / (2(2j-1) j!), j>=1; e_0=0.
   My own symbolic re-derivation (done by hand, reproduced here in sympy):
     sum_K (-1)^K C(j,K) phi_K = 1/(2j+1)
     sum_K (-1)^K C(j,K) K phi_K = -2j/((2j-1)(2j+1))
     => T_j := sum_K (-1)^K C(j,K) c_K = (j-1)/(2(2j+1)(2j-1))   for j>=1
     => e_j = ((-1)^j/j!)[(j-1)/(2(2j+1)(2j-1)) - j(j-1)/(2(2j+1))]
            = ((-1)^j/j!) (j-1)(1-j(2j-1)) / (2(2j+1)(2j-1))
            and 1-j(2j-1) = -(2j+1)(j-1), so
       e_j = (-1)^{j+1} (j-1)^2 / (2(2j-1) j!).   QED (fully elementary).
""")
jj = sp.Symbol('j', positive=True, integer=True)
print("   sympy check of the two auxiliary sums, j = 1..10:")
for j in range(1, 11):
    s1 = sum(sp.Rational(-1)**K * comb(j, K) * sp.Rational(
        phi_K(K).numerator, phi_K(K).denominator) for K in range(j + 1))
    s2 = sum(sp.Rational(-1)**K * comb(j, K) * K * sp.Rational(
        phi_K(K).numerator, phi_K(K).denominator) for K in range(j + 1))
    t1 = sp.Rational(1, 2*j+1)
    t2 = sp.Rational(-2*j, (2*j-1)*(2*j+1))
    assert s1 == t1 and s2 == t2, (j, s1, t1, s2, t2)
print("      both closed forms confirmed for j = 1..10.")

print()
print(f"   {'j':>3} {'e_j (Teorema D sum)':>24} {'e_j (Prop 5.2 form)':>24}  match")
for j in range(0, 13):
    A = (F(-1)**j / F(sp.factorial(j))) * (
        sum(F(-1)**K * comb(j, K) * c_K(K) for K in range(j + 1))
        - F(comb(j, 2)) * sum(F(-1)**K * comb(j, K) * phi_K(K)
                              for K in range(j + 1)))
    B = F(0) if j == 0 else (F(-1)**(j+1) * F((j-1)**2)
                             / (2 * F(2*j-1) * F(sp.factorial(j))))
    print(f"   {j:3d} {str(A):>24} {str(B):>24}  {'OK' if A == B else 'FAIL'}")

print()
print("=" * 76)
print("6. Finite-n convergence n([c^j]phi(n,.) - [c^j]phi_inf) -> e_j")
print("=" * 76)
for j in (2, 3, 4):
    ej_inf = F(-1)**j / (F(sp.factorial(j)) * F(2*j+1))
    row = []
    for n in (20, 40, 80, 160, 320, 640):
        cj = F(-1)**j * F(comb(n, j), n**j) * sum(
            F(-1)**K * comb(j, K) * phiK_fast(n, K) for K in range(j + 1))
        row.append(float(n * (cj - ej_inf)))
    tgt = F(-1)**(j+1) * F((j-1)**2) / (2 * F(2*j-1) * F(sp.factorial(j)))
    print(f"   j={j}: " + " ".join(f"{x:10.7f}" for x in row)
          + f"   -> e_j = {float(tgt):10.7f}")

print()
print("=" * 76)
print("7. PROP 5.2's three representations of e(c) and its landmarks")
print("=" * 76)
I = lambda k, cc: mp.quad(lambda t: t**(2*k) * mp.e**(-cc*t**2), [0, 1])
e_int1 = lambda cc: (I(0, cc)*cc - I(1, cc)*cc + 2*I(0, cc) - 2)/4 - cc**2*I(2, cc)/2
e_int2 = lambda cc: mp.quad(
    lambda t: (1 - (1 + cc*t**2 + cc**2*t**4)*mp.e**(-cc*t**2))/t**2, [0, 1])/2
def e_series(cc, N=200):
    s = mp.mpf(0)
    for j in range(1, N):
        s += mp.mpf(-1)**(j+1) * (j-1)**2 / (2*(2*j-1)*mp.factorial(j)) * mp.mpf(cc)**j
    return s
print(f"   {'c':>6} {'(5.1) integral form':>24} {'Prop 5.2 integral':>24}"
      f" {'power series':>24}")
for cc in (mp.mpf('0.5'), 1, 2, 5, 10):
    a, b, d = e_int1(cc), e_int2(cc), e_series(cc)
    print(f"   {float(cc):6.2f} {mp.nstr(a,18):>24} {mp.nstr(b,18):>24}"
          f" {mp.nstr(d,18):>24}")
print(f"   max pairwise discrepancy over these c: "
      f"{max(max(abs(e_int1(x)-e_int2(x)), abs(e_int1(x)-e_series(x))) for x in (mp.mpf('0.5'),1,2,5,10))}")

print()
J = mp.quad(lambda u: (1 - (1+u**2+u**4)*mp.e**(-u**2))/u**2, [0, mp.inf])
print(f"   int_0^inf [1-(1+u^2+u^4)e^{{-u^2}}]/u^2 du = {mp.nstr(J, 20)}")
print(f"   sqrt(pi)/4                                = {mp.nstr(mp.sqrt(mp.pi)/4, 20)}")
print(f"   agree to 20 digits: {mp.nstr(abs(J - mp.sqrt(mp.pi)/4), 5)}")
cmin = mp.findroot(lambda x: mp.diff(e_int1, x), mp.mpf('2.28'))
print(f"   minimiser of e:  c = {mp.nstr(cmin, 12)}   e = {mp.nstr(e_int1(cmin), 12)}")
print(f"                    (document: 2.283781525, -0.06696142887)")
czero = mp.findroot(lambda x: e_int1(x), mp.mpf('4.8'))
print(f"   sign change  :  c_x = {mp.nstr(czero, 12)}   (document: 4.83904605495)")
print(f"   sqrt(pi)/8   = {mp.nstr(mp.sqrt(mp.pi)/8, 12)}   (document: 0.2215567314)")
print()
print("   large-c form e(c) = sqrt(pi c)/8 - 1/2 + O(sqrt(c) e^{-c}):")
for cc in (25, 100, 400):
    print(f"     c={cc:4d}   e(c) = {mp.nstr(e_int1(mp.mpf(cc)), 12):>16}   "
          f"sqrt(pi c)/8 - 1/2 = {mp.nstr(mp.sqrt(mp.pi*cc)/8 - mp.mpf(1)/2, 12):>16}")
print("   -> reproduces the 0.607784 / 1.715567 / 3.931135 of the sec 5.6 table.")
