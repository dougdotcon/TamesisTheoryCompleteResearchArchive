#!/usr/bin/env python3
"""
Adversarial referee -- Step C/D assembly (ATTEMPT.md Sec.4) re-derived from
scratch. Own derivation route (documented in REFEREE_REPORT.md), sympy exact.

Part 1: per-r integral (my own re-derivation of the marginalization)
        f_r(x) = C(K,r) K! r! * (x^r/r!) *
                 Int_0^{1-x} (1-Q) Q^(n-1)/(n-1)! (1-x-Q)^(r-1)/(r-1)! dQ
        evaluated exactly for every K=1..12, r=1..K-1, plus edges r=0, r=K,
        compared against the unified closed form
        C(K,r) x^r (1-x)^(K-1) [K-(K-r)(1-x)].
Part 2: symbolic-K Beta-route: the same integral via Q=(1-x)v gives
        (1-x)^(K-1)[B(n,r)-(1-x)B(n+1,r)] scaling -> unified form, with
        symbolic K, r (n=K-r).
Part 3: sum over r = 2Kx(1-x^2)^(K-1): explicit K=1..12, and symbolic-K via
        Sum().doit() -- reproducing the sympy Piecewise artifact the front
        disclosed (Sec.6 item 1), then extracting the x<=1 branch.
Part 4: K=5 instance: the six group polynomials, probabilities
        1/6,5/14,25/84,5/36,1/28,1/252, moments 256/693 (= Wallis 4^K(K!)^2/(2K+1)!),
        1/6, 256/3003.
Part 5: reductions K=1,2,3,4 group-by-group vs the published lineage
        polynomials (transcribed from PROSE, built on this script's own x).
Part 6: E[M_K^2] = 1/(K+1) symbolically for symbolic K, and E[M_K] = Wallis.
Part 7: K=6 exact targets for the beyond-front MC: P(r), f_r coefficients,
        E[M_6]=phi_6, E[M_6^2]=1/7.
"""
import sympy as sp
import sys, math

x = sp.Symbol('x', positive=True)
Q = sp.Symbol('Q', positive=True)
ok = True

def unified(K, r):
    return sp.binomial(K, r)*x**r*(1-x)**(K-1)*(K-(K-r)*(1-x))

def per_r_integral(K, r):
    n = K - r
    if r == 0:
        # M = 1-Q, weight (1-Q), mass-sum density K! Q^(K-1)/(K-1)!
        fq = sp.factorial(K)*Q**(K-1)/sp.factorial(K-1)*(1-Q)
        return sp.expand(fq.subs(Q, 1-x))
    if r == K:
        return sp.expand(sp.factorial(K)*x**K*(1-x)**(K-1)/sp.factorial(K-1))
    integ = sp.integrate((1-Q)*Q**(n-1)/sp.factorial(n-1) *
                         (1-x-Q)**(r-1)/sp.factorial(r-1), (Q, 0, 1-x))
    return sp.expand(sp.binomial(K, r)*sp.factorial(K)*x**r*integ)

print("="*72)
print("PART 1: per-r integral vs unified closed form, K=1..12, all r")
print("="*72)
for K in range(1, 13):
    allok = True
    for r in range(0, K+1):
        d = sp.simplify(per_r_integral(K, r) - sp.expand(unified(K, r)))
        if d != 0:
            allok = False
            print(f"  K={K} r={r}: MISMATCH {d}")
    ok &= allok
    print(f"  K={K}: all r=0..{K} match unified form  {'PASS' if allok else 'FAIL'}")

print()
print("="*72)
print("PART 2: symbolic-(K,r) Beta route")
print("="*72)
Ks, rs = sp.symbols('K r', positive=True, integer=True)
ns = Ks - rs
v = sp.Symbol('v', positive=True)
# Int_0^{1-x} (1-Q)Q^(n-1)(1-x-Q)^(r-1) dQ ; Q=(1-x)v
inner = sp.integrate((1-(1-x)*v)*v**(ns-1)*(1-v)**(rs-1), (v, 0, 1))
inner = sp.simplify(inner)
full = sp.binomial(Ks, rs)*sp.factorial(Ks)*x**rs/(sp.factorial(ns-1)*sp.factorial(rs-1)) \
       * (1-x)**(ns+rs-1) * inner
target = sp.binomial(Ks, rs)*x**rs*(1-x)**(Ks-1)*(Ks-(Ks-rs)*(1-x))
diff = sp.simplify(sp.gammasimp(full - target))
print("  symbolic-(K,r) integral minus unified form simplifies to:", diff)
p2 = (diff == 0)
if not p2:
    # try harder
    diff2 = sp.simplify(sp.gammasimp(sp.expand_func(full/target)))
    print("  ratio simplifies to:", diff2)
    p2 = (diff2 == 1)
ok &= p2
print(f"  {'PASS' if p2 else 'FAIL'}")

print()
print("="*72)
print("PART 3: sum over r = 2Kx(1-x^2)^(K-1)")
print("="*72)
for K in range(1, 13):
    s = sum(unified(K, r) for r in range(K+1))
    d = sp.simplify(sp.expand(s) - sp.expand(2*K*x*(1-x**2)**(K-1)))
    ok &= (d == 0)
    print(f"  K={K}: sum-2Kx(1-x^2)^(K-1) = {d}  {'PASS' if d==0 else 'FAIL'}")
# symbolic K, reproducing the disclosed Piecewise artifact
r2 = sp.Symbol('r', nonnegative=True, integer=True)
S1 = sp.Sum(sp.binomial(Ks, r2)*x**r2, (r2, 0, Ks)).doit()
print("  one-line artifact reproduction: Sum C(K,r)x^r .doit() =")
print("   ", S1)
is_pw = isinstance(S1, sp.Piecewise)
print(f"  -> Piecewise artifact reproduced: {is_pw}")
def branch_x_le_1(expr):
    if isinstance(expr, sp.Piecewise):
        for e, c in expr.args:
            if c == sp.true or (c.has(x) and sp.simplify(c.subs(x, sp.Rational(1,2)))):
                return e
        return expr.args[0][0]
    return expr
b1 = branch_x_le_1(S1)
d1 = sp.simplify(b1 - (1+x)**Ks)
S2 = sp.Sum((Ks-r2)*sp.binomial(Ks, r2)*x**r2, (r2, 0, Ks)).doit()
b2 = branch_x_le_1(S2)
d2 = sp.simplify(b2 - Ks*(1+x)**(Ks-1))
print(f"  branch(x<=1) of S1 - (1+x)^K = {d1}   "
      f"branch of S2 - K(1+x)^(K-1) = {d2}")
p3 = (d1 == 0 and d2 == 0)
ok &= p3
print(f"  symbolic-K binomial identities (after branch extraction): "
      f"{'PASS' if p3 else 'FAIL'}")

print()
print("="*72)
print("PART 4: K=5 instance")
print("="*72)
claim5 = {0: 5*x*(1-x)**4,
          1: 5*x*(1-x)**4*(1+4*x),
          2: 10*x**2*(1-x)**4*(2+3*x),
          3: 10*x**3*(1-x)**4*(3+2*x),
          4: 5*x**4*(1-x)**4*(4+x),
          5: 5*x**5*(1-x)**4}
probs5 = [sp.Rational(1,6), sp.Rational(5,14), sp.Rational(25,84),
          sp.Rational(5,36), sp.Rational(1,28), sp.Rational(1,252)]
p4 = True
for r in range(6):
    d = sp.simplify(unified(5, r) - claim5[r])
    pr = sp.integrate(unified(5, r), (x, 0, 1))
    okr = (d == 0) and (sp.simplify(pr - probs5[r]) == 0)
    p4 &= okr
    print(f"  r={r}: poly match diff={d}; P(r)={pr} vs {probs5[r]}  "
          f"{'PASS' if okr else 'FAIL'}")
f5 = sum(unified(5, r) for r in range(6))
m1 = sp.integrate(x*f5, (x, 0, 1)); m2 = sp.integrate(x**2*f5, (x, 0, 1))
m3 = sp.integrate(x**3*f5, (x, 0, 1)); m0 = sp.integrate(f5, (x, 0, 1))
wallis5 = sp.Rational(4**5*math.factorial(5)**2, math.factorial(11))
okm = (m0 == 1 and m1 == sp.Rational(256,693) and m1 == wallis5
       and m2 == sp.Rational(1,6) and m3 == sp.Rational(256,3003))
p4 &= okm
print(f"  int f=({m0}); E[M5]={m1} (Wallis {wallis5}); E[M5^2]={m2}; E[M5^3]={m3} "
      f"{'PASS' if okm else 'FAIL'}")
ok &= p4

print()
print("="*72)
print("PART 5: reductions K=1..4, group by group (published lineage polys)")
print("="*72)
published = {
 1: {0: x, 1: x},
 2: {0: 2*x*(1-x), 1: 2*x*(1-x**2), 2: 2*x**2*(1-x)},
 3: {0: 3*x-6*x**2+3*x**3, 1: 3*x-9*x**3+6*x**4,
     2: 6*x**2-9*x**3+3*x**5, 3: 3*x**3-6*x**4+3*x**5},
 4: {0: -4*x**4+12*x**3-12*x**2+4*x, 1: -12*x**5+32*x**4-24*x**3+4*x,
     2: -12*x**6+24*x**5-24*x**3+12*x**2, 3: -4*x**7+24*x**5-32*x**4+12*x**3,
     4: -4*x**7+12*x**6-12*x**5+4*x**4}}
p5 = True
for K in range(1, 5):
    for r in range(K+1):
        d = sp.simplify(unified(K, r) - published[K][r])
        if d != 0:
            p5 = False
            print(f"  K={K} r={r}: MISMATCH {d}")
    print(f"  K={K}: all {K+1} published group densities reproduced exactly  "
          f"{'PASS' if p5 else 'FAIL'}")
ok &= p5

print()
print("="*72)
print("PART 6: E[M_K]=Wallis and E[M_K^2]=1/(K+1), symbolic K")
print("="*72)
t = sp.Symbol('t', positive=True)
fK = 2*Ks*x*(1-x**2)**(Ks-1)
EM2 = sp.simplify(sp.integrate(x**2*fK, (x, 0, 1)))
d6 = sp.simplify(EM2 - 1/(Ks+1))
EM1 = sp.simplify(sp.integrate(x*fK, (x, 0, 1)))
wallis = sp.simplify(sp.integrate((1-t**2)**Ks, (t, 0, 1)))
d6b = sp.simplify(sp.gammasimp(EM1 - wallis))
p6 = (d6 == 0 and d6b == 0)
ok &= p6
print(f"  E[M_K^2]-1/(K+1) = {d6};  E[M_K]-int(1-t^2)^K dt = {d6b}  "
      f"{'PASS' if p6 else 'FAIL'}")

print()
print("="*72)
print("PART 7: K=6 exact targets (for the beyond-front K=6 MC)")
print("="*72)
p7 = True
prs = []
for r in range(7):
    pr = sp.integrate(unified(6, r), (x, 0, 1))
    prs.append(pr)
    print(f"  K=6 P(r={r}) = {pr}")
s7 = sp.simplify(sum(prs) - 1)
f6 = sum(unified(6, r) for r in range(7))
d7 = sp.simplify(f6 - 12*x*(1-x**2)**5)
m16 = sp.integrate(x*f6, (x, 0, 1)); m26 = sp.integrate(x**2*f6, (x, 0, 1))
wallis6 = sp.Rational(4**6*math.factorial(6)**2, math.factorial(13))
p7 = (s7 == 0 and d7 == 0 and m16 == wallis6 and m26 == sp.Rational(1,7))
ok &= p7
print(f"  sum P(r)-1 = {s7}; f6 - 12x(1-x^2)^5 = {d7}; "
      f"E[M6]={m16} (Wallis {wallis6}); E[M6^2]={m26}  {'PASS' if p7 else 'FAIL'}")

print()
print("OVERALL:", "ALL PASS" if ok else "*** SOME CHECK FAILED ***")
sys.exit(0 if ok else 1)
