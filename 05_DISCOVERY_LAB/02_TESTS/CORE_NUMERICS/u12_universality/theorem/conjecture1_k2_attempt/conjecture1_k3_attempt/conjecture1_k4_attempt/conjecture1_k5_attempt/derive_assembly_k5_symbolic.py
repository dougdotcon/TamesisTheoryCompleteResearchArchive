#!/usr/bin/env python3
"""Assembly of f_{M_K}: K=5 instance + general-K sum + reduction checks.

Fresh code; no prior front/referee script read or imported.  All reference
polynomials from the already-reviewed K=1..4 documents are transcribed from
their PROSE and built directly with this script's own symbol x (never
sympify from string — the K=4 document's disclosed pitfall).

Part A: per-r densities at K=5 via the marginalization integral
          f_r(x) = C(K,r) * K! * x^r *
                   Int_{Q=0}^{1-x} (1-Q) Q^(n-1)/(n-1)! (1-x-Q)^(r-1)/(r-1)! dQ
        (r>=1, n=K-r>=1; edge cases r=0 and r=K handled directly), and the
        registered unified closed form
          f_r(x) = C(K,r) x^r (1-x)^(K-1) [K - (K-r)(1-x)].
Part B: symbolic sum = 10x(1-x^2)^4 exactly.
Part C: per-r probabilities, moments, Wallis cross-check.
Part D: reductions — the same unified formula at K=1,2,3,4 reproduces the
        published group-by-group densities exactly.
Part E: general-K sum = 2Kx(1-x^2)^(K-1) for K=1..12, plus the two binomial
        identities used in the by-hand general proof.
"""
import sympy as sp
from math import comb, factorial

x, Q = sp.symbols('x Q', positive=True)
r_, K_ = sp.symbols('r K', positive=True, integer=True)
ok_all = True


def check(label, cond):
    global ok_all
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        ok_all = False


def f_r_integral(K, r):
    """Direct marginalization route (the derivation's own integral)."""
    n = K - r
    if r == 0:
        # M = 1-Q with weight (1-Q); density of Q-slice = Q^(K-1)/(K-1)!
        # f_0(x) = K! * (1-Q) * Q^(K-1)/(K-1)! at Q=1-x, |dQ/dx|=1
        return sp.expand(sp.Rational(factorial(K), factorial(K - 1))
                         * x * (1 - x) ** (K - 1))
    if n == 0:
        # no off nodes: f = K! x^K/(K)!... full: C(K,K)*K!*r!*(x^r/r!)*s^(r-1)/(r-1)!
        return sp.expand(sp.Rational(factorial(K), factorial(K - 1))
                         * x ** K * (1 - x) ** (K - 1))
    integrand = (1 - Q) * Q ** (n - 1) / factorial(n - 1) \
        * (1 - x - Q) ** (r - 1) / factorial(r - 1)
    I = sp.integrate(integrand, (Q, 0, 1 - x))
    return sp.expand(comb(K, r) * factorial(K) * x ** r * I)


def f_r_unified(K, r):
    return sp.expand(comb(K, r) * x ** r * (1 - x) ** (K - 1)
                     * (K - (K - r) * (1 - x)))


# ---------------------------------------------------------------- Part A
print("=" * 72)
print("Part A: K=5 per-r densities, integral route vs unified closed form")
K = 5
fs = []
for r in range(K + 1):
    fi = f_r_integral(K, r)
    fu = f_r_unified(K, r)
    fs.append(fi)
    print(f"  r={r}: f_r(x) = {sp.factor(fi)}")
    check(f"K=5 r={r}: integral route == unified closed form",
          sp.simplify(fi - fu) == 0)

# registered factored forms
reg = [5 * x * (1 - x) ** 4,
       5 * x * (1 - x) ** 4 * (1 + 4 * x),
       10 * x ** 2 * (1 - x) ** 4 * (2 + 3 * x),
       10 * x ** 3 * (1 - x) ** 4 * (3 + 2 * x),
       5 * x ** 4 * (1 - x) ** 4 * (4 + x),
       5 * x ** 5 * (1 - x) ** 4]
for r in range(6):
    check(f"K=5 r={r}: matches registered factored form",
          sp.simplify(fs[r] - sp.expand(reg[r])) == 0)

# ---------------------------------------------------------------- Part B
print("=" * 72)
print("Part B: symbolic sum")
fM5 = sp.expand(sum(fs))
target = sp.expand(10 * x * (1 - x ** 2) ** 4)
print(f"  sum   = {fM5}")
print(f"  target= {target}")
check("f_M5(x) == 10x(1-x^2)^4 exactly", sp.simplify(fM5 - target) == 0)

# ---------------------------------------------------------------- Part C
print("=" * 72)
print("Part C: probabilities and moments (exact)")
probs_reg = [sp.Rational(1, 6), sp.Rational(5, 14), sp.Rational(25, 84),
             sp.Rational(5, 36), sp.Rational(1, 28), sp.Rational(1, 252)]
tot = 0
for r in range(6):
    p = sp.integrate(fs[r], (x, 0, 1))
    tot += p
    print(f"  P(r_on={r}) = {p}")
    check(f"P(r_on={r}) == registered {probs_reg[r]}", sp.simplify(p - probs_reg[r]) == 0)
check("probabilities sum to 1", sp.simplify(tot - 1) == 0)

m0 = sp.integrate(fM5, (x, 0, 1))
m1 = sp.integrate(x * fM5, (x, 0, 1))
m2 = sp.integrate(x ** 2 * fM5, (x, 0, 1))
m3 = sp.integrate(x ** 3 * fM5, (x, 0, 1))
print(f"  int f = {m0}, E[M5] = {m1}, E[M5^2] = {m2}, E[M5^3] = {m3}")
check("normalization = 1", sp.simplify(m0 - 1) == 0)
check("E[M5] = 256/693", sp.simplify(m1 - sp.Rational(256, 693)) == 0)
# independent Wallis target: 4^K (K!)^2/(2K+1)! at K=5
wallis = sp.Rational(4 ** 5 * factorial(5) ** 2, factorial(11))
check(f"E[M5] equals THEOREM.md 5.2 Wallis value {wallis}",
      sp.simplify(m1 - wallis) == 0)
check("E[M5^2] = 1/6 (the 1/(K+1) pattern of Estagio 18)",
      sp.simplify(m2 - sp.Rational(1, 6)) == 0)
check("E[M5^3] = 256/3003", sp.simplify(m3 - sp.Rational(256, 3003)) == 0)

# ---------------------------------------------------------------- Part D
print("=" * 72)
print("Part D: reduction checks against the published K=1..4 group densities")
# K=1 (THEOREM.md 5.3): branches x and x, sum 2x
pub1 = [x, x]
# K=2 (Estagio 15 / conjecture1_k2_attempt): D, B+C, A
pub2 = [2 * x * (1 - x), 2 * x * (1 - x ** 2), 2 * x ** 2 * (1 - x)]
# K=3 (conjecture1_k3_attempt, grouped by r_on as tabulated in the K=4 doc §5)
pub3 = [3 * x ** 3 - 6 * x ** 2 + 3 * x,
        6 * x ** 4 - 9 * x ** 3 + 3 * x,
        3 * x ** 5 - 9 * x ** 3 + 6 * x ** 2,
        3 * x ** 5 - 6 * x ** 4 + 3 * x ** 3]
# K=4 (conjecture1_k4_attempt §4)
pub4 = [-4 * x ** 4 + 12 * x ** 3 - 12 * x ** 2 + 4 * x,
        -12 * x ** 5 + 32 * x ** 4 - 24 * x ** 3 + 4 * x,
        -12 * x ** 6 + 24 * x ** 5 - 24 * x ** 3 + 12 * x ** 2,
        -4 * x ** 7 + 24 * x ** 5 - 32 * x ** 4 + 12 * x ** 3,
        -4 * x ** 7 + 12 * x ** 6 - 12 * x ** 5 + 4 * x ** 4]
for Kred, pub in ((1, pub1), (2, pub2), (3, pub3), (4, pub4)):
    allok = True
    for r in range(Kred + 1):
        mine = f_r_unified(Kred, r)
        if sp.simplify(mine - sp.expand(pub[r])) != 0:
            allok = False
            print(f"  K={Kred} r={r}: MISMATCH mine={mine} pub={sp.expand(pub[r])}")
    check(f"K={Kred}: unified formula reproduces published groups r=0..{Kred}",
          allok)
    total = sp.expand(sum(f_r_unified(Kred, r) for r in range(Kred + 1)))
    check(f"K={Kred}: sum == 2Kx(1-x^2)^(K-1)",
          sp.simplify(total - 2 * Kred * x * (1 - x ** 2) ** (Kred - 1)) == 0)

# ---------------------------------------------------------------- Part E
print("=" * 72)
print("Part E: general-K sum and the two binomial identities of the proof")
for K in range(1, 13):
    total = sp.expand(sum(f_r_unified(K, r) for r in range(K + 1)))
    check(f"K={K}: sum_r f_r == 2Kx(1-x^2)^(K-1)",
          sp.simplify(total - 2 * K * x * (1 - x ** 2) ** (K - 1)) == 0)

# the two identities used in the by-hand general proof, with symbolic K.
# NOTE (process, disclosed): sympy evaluates these finite sums into a
# Piecewise guarded by "x <= 1" (an artifact of its hypergeometric
# summation machinery; the sums are finite polynomials, so the identity
# holds for every x, but sympy only certifies the branch it evaluated).
# Our density domain is x in (0,1), so the x<=1 branch is the relevant
# one; we extract it explicitly rather than fighting the Piecewise.
def branch_at_x_le_1(expr):
    return sp.piecewise_fold(expr).subs(sp.Symbol('dummy'), 0) \
        if not expr.has(sp.Piecewise) else \
        [e for e, c in sp.piecewise_fold(expr).args
         if c.subs(x, sp.Rational(1, 2)) == True][0]


s1 = sp.Sum(sp.binomial(K_, r_) * x ** r_, (r_, 0, K_)).doit()
s2 = sp.Sum(r_ * sp.binomial(K_, r_) * x ** r_, (r_, 0, K_)).doit()
s1b = branch_at_x_le_1(s1) if s1.has(sp.Piecewise) else s1
s2b = branch_at_x_le_1(s2) if s2.has(sp.Piecewise) else s2
check("Sum C(K,r) x^r = (1+x)^K (symbolic K, x in (0,1) branch)",
      sp.simplify(s1b - (1 + x) ** K_) == 0)
check("Sum r C(K,r) x^r = K x (1+x)^(K-1) (symbolic K, x in (0,1) branch)",
      sp.simplify(s2b - K_ * x * (1 + x) ** (K_ - 1)) == 0)
# hence Sum (K-r) C(K,r) x^r = K(1+x)^K/(1+x) ... = K(1+x)^(K-1):
check("Sum (K-r) C(K,r) x^r = K(1+x)^(K-1) (symbolic K, derived)",
      sp.simplify(K_ * s1b - s2b - K_ * (1 + x) ** (K_ - 1)) == 0)

print("=" * 72)
print("ALL CHECKS PASSED" if ok_all else "SOME CHECKS FAILED")
