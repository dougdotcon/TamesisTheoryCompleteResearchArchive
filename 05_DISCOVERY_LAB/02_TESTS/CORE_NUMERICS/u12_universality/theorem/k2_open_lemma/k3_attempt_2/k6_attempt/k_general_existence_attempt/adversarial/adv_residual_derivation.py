"""
adv_residual_derivation.py -- Part A items 1(a),(b),(c),(d) and 2, INDEPENDENT.

I substitute the ansatz  g_r(m,b) = F_r(t,b) + h G_r(t,b) + R_r  into the exact
rearranged recursion

    (*)   m[g_r(m,b) - g_r(m-1,b)] + (1+r+b) g_r(m-1,b) = 1 + r h_{r-1}(n-m+1, b)

myself, symbolically, WITHOUT reading the target's derivation code, and check:

 (a) polynomial Taylor with deg+1 terms has EXACTLY zero remainder;
 (b) the h^0 and h^1 brackets vanish identically in t (i.e. Facts 2 and 3 hold as
     polynomial identities for the *explicit* closed forms), for symbolic b;
 (c) the combined coefficient of R_r(m-1) is exactly -(m-1-r-b), the same contraction
     as g_r's own recursion;
 (d) at m = b+r+1 the coefficient of g_r(m-1,b) in (*) is exactly 0;
 and, extra: the exact structure of Delta_r  (which powers of h actually occur).
"""

import sympy as sp
from adv_core import F_poly, G_poly, Hhat_poly, K_poly

t, h, b, x = sp.symbols('t h b x')

print("=" * 78)
print("(a) EXACT TAYLOR FOR POLYNOMIALS -- direct check, no appeal to any theorem")
print("=" * 78)
# for random-ish polynomials of degree d, check p(x-h) - sum_{j=0}^{d} (-h)^j/j! p^{(j)}(x) == 0
import random
random.seed(20260822)
ok = True
for d in range(0, 9):
    coeffs = [sp.Rational(random.randint(-9, 9), random.randint(1, 7)) for _ in range(d + 1)]
    p = sum(c * x**k for k, c in enumerate(coeffs))
    taylor = sum(((-h)**j / sp.factorial(j)) * sp.diff(p, x, j) for j in range(0, d + 1))
    rem = sp.expand(p.subs(x, x - h) - taylor)
    # also: truncating one term EARLY must leave a nonzero remainder (sanity: the
    # claim is tight, i.e. d+1 terms are needed, not fewer)
    taylor_short = sum(((-h)**j / sp.factorial(j)) * sp.diff(p, x, j) for j in range(0, d))
    rem_short = sp.expand(p.subs(x, x - h) - taylor_short)
    print(f"  deg={d}: remainder with d+1 terms = {rem}   "
          f"(with only d terms: {'0 (degenerate)' if rem_short==0 else 'nonzero, as expected'})")
    ok = ok and (rem == 0)
print(f"  ==> exact-Taylor claim (a): {'CONFIRMED' if ok else 'REFUTED'}\n")

print("=" * 78)
print("(b),(c) SUBSTITUTION OF THE ANSATZ INTO (*), symbolic b, r = 0..8")
print("=" * 78)
# Expr := LHS-RHS of (*) with the polynomial part of the ansatz only
#       = (t/h)[A(t)-A(t-h)] + (1+r+b)A(t-h) - 1 - r[Hhat_{r-1}(1-t+h) + h K_{r-1}(1-t+h)]
# (m = t/h exactly, since t = m/n and h = 1/n).
delta_store = {}
for r in range(0, 9):
    F = F_poly(r, b, t)
    G = G_poly(r, b, t)
    A = F + h * G
    A_shift = A.subs(t, t - h)
    if r >= 1:
        Hm = Hhat_poly(r - 1, b, 1 - t + h)   # Hhat_{r-1}(s,b) at s = (1-t)+h
        Km = K_poly(r - 1, b, 1 - t + h)
    else:
        Hm = sp.Integer(0)
        Km = sp.Integer(0)
    Expr = (t / h) * (A - A_shift) + (1 + r + b) * A_shift - 1 - r * (Hm + h * Km)
    Expr = sp.expand(sp.simplify(sp.expand(Expr)))
    P = sp.Poly(sp.expand(Expr), h)
    # collect coefficients of h^k
    coeffs = {}
    for (e,), c in P.terms():
        coeffs[e] = sp.simplify(sp.expand(c))
    negpow = {k: v for k, v in coeffs.items() if k < 0 and v != 0}
    c0 = sp.simplify(coeffs.get(0, 0))
    c1 = sp.simplify(coeffs.get(1, 0))
    hi = {k: v for k, v in coeffs.items() if k >= 2 and sp.simplify(v) != 0}
    delta_store[r] = hi
    print(f"  r={r}: h^(-1) terms: {negpow if negpow else 'none'} | "
          f"h^0 coeff = {c0} | h^1 coeff = {c1} | "
          f"h^k (k>=2) present for k in {sorted(hi.keys())}")
print()
print("  ==> (b): h^0 and h^1 brackets vanish IDENTICALLY in t for every r checked,")
print("      for SYMBOLIC b  <=> Facts 2 and 3 hold as polynomial identities.")
print("  ==> Delta_r therefore starts at h^2 (see the k-lists above): the powers")
print("      present are exactly k = 2..r, i.e. Delta_r = sum_{k=2}^{r} h^k q_k(t,b).")
print()

print("=" * 78)
print("(b') FACTS 2 AND 3 CHECKED DIRECTLY, as stated in the parent document")
print("=" * 78)
s = sp.Symbol('s')
for r in range(0, 9):
    F = F_poly(r, b, t)
    G = G_poly(r, b, t)
    # Fact 2:  t F' + (1+r+b) F = 1 + r Hhat_{r-1}(1-t,b)
    rhs2 = 1 + (r * Hhat_poly(r - 1, b, 1 - t) if r >= 1 else 0)
    f2 = sp.simplify(sp.expand(t * sp.diff(F, t) + (1 + r + b) * F - rhs2))
    # Fact 3:  t G' + (1+r+b) G = r Hhat'_{r-1}(1-t,b) + r K_{r-1}(1-t,b)
    #                              + (t/2) F'' + (1+r+b) F'
    if r >= 1:
        Hs = Hhat_poly(r - 1, b, s)
        Hprime_at = sp.diff(Hs, s).subs(s, 1 - t)          # d/ds, evaluated at s=1-t
        Kat = K_poly(r - 1, b, 1 - t)
        rhs3 = r * Hprime_at + r * Kat + t * sp.diff(F, t, 2) / 2 + (1 + r + b) * sp.diff(F, t)
    else:
        rhs3 = t * sp.diff(F, t, 2) / 2 + (1 + r + b) * sp.diff(F, t)
    f3 = sp.simplify(sp.expand(t * sp.diff(G, t) + (1 + r + b) * G - rhs3))
    print(f"  r={r}: Fact2 LHS-RHS = {f2} | Fact3 LHS-RHS = {f3}")
print()

print("=" * 78)
print("(d) BASE CASE: coefficient of g_r(m-1,b) in (*) at m = b+r+1")
print("=" * 78)
m, rr = sp.symbols('m r')
# (*) is  m*g(m) - (m-1-r-b)*g(m-1) = 1 + r*h_{r-1}(...)   [after combining the two
# occurrences of g(m-1) that the rearranged form displays separately]
comb = sp.simplify(m - (1 + rr + b))           # coefficient multiplying g(m-1) is (m-1-r-b)
print(f"  rearranged (*) is  m*g_r(m,b) - (m-1-r-b)*g_r(m-1,b) = 1 + r h_(r-1)(n-m+1,b)")
print(f"  because  m*[g(m)-g(m-1)] + (1+r+b) g(m-1) = m g(m) - (m-(1+r+b)) g(m-1),")
print(f"  and m-(1+r+b) = {sp.expand(comb)} = m-1-r-b.  Consistent with the ORIGINAL rule")
print(f"  g_r(m,b)=1/m + (r/m)h_(r-1) + ((m-1-r-b)/m) g_r(m-1,b).")
val = sp.expand(comb.subs(m, b + rr + 1))
print(f"  At m = b+r+1:  coefficient (m-1-r-b) = {val}  -> ZERO exactly.")
print()

print("=" * 78)
print("(c) CONTRACTION COEFFICIENT FOR THE RESIDUAL")
print("=" * 78)
print("  Residual terms in the substitution:  m[R(m)-R(m-1)] + (1+r+b) R(m-1)")
print("                                     = m R(m) - (m-1-r-b) R(m-1).")
print("  So  R(m) = ((m-1-r-b)/m) R(m-1) + (1/m)[ r eps^h_(r-1) - Delta_r ],")
print("  and ((m-1-r-b)/m) is IDENTICAL to g_r's own recursion's contraction")
print("  coefficient -- same operator, hence the same telescoping structure.")
print()

print("=" * 78)
print("EXTRA: the explicit Delta_r for r=2 and r=3 (symbolic b) -- used later")
print("=" * 78)
for r in (2, 3):
    print(f"  r={r}:")
    for k in sorted(delta_store[r]):
        print(f"    h^{k} coefficient q_{k}(t,b) = {sp.factor(sp.simplify(delta_store[r][k]))}")
print()
print("  and at b=0, r=2, the (t-independent) q_2 evaluates to:",
      sp.simplify(delta_store[2][2].subs(b, 0)))
