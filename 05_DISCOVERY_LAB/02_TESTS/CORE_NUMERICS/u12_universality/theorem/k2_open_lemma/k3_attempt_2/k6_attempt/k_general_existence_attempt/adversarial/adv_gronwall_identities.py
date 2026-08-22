"""
adv_gronwall_identities.py -- Part A items 2 and 3, INDEPENDENT.

 2. the coefficient-sum lemma  |p(x)| <= sum|a_k| on x in [0,1], and its derivative
    version -- checked for correctness AND for whether it is being applied only at
    arguments that really lie in [0,1] (t, 1-t, s, 1-s).
 3. the falling-factorial telescoping identity
        prod_{i=k+1}^{m} (i-j)/i = C(k,j)/C(m,j)
    and the summation
        sum_{k=j}^{m} (1/k) C(k,j) = C(m,j)/j
    re-derived from scratch (symbolically where possible, numerically over many
    concrete triples), plus an explicit construction of the CRUDE bound
    (prod alpha <= 1) to confirm it really produces a log-n factor.
"""

import math
import random
from fractions import Fraction as Fr
import sympy as sp

print("=" * 84)
print("ITEM 2 -- the coefficient-sum lemma")
print("=" * 84)
x = sp.Symbol('x')
random.seed(4242)
bad = 0
for trial in range(400):
    d = random.randint(0, 6)
    co = [Fr(random.randint(-20, 20), random.randint(1, 9)) for _ in range(d + 1)]
    norm = sum(abs(c) for c in co)
    for _ in range(30):
        xv = Fr(random.randint(0, 1000), 1000)          # x in [0,1]
        val = sum(c * xv**k for k, c in enumerate(co))
        if abs(val) > norm:
            bad += 1
print(f"  |p(x)| <= sum|a_k| on x in [0,1]: violations in 12000 random samples = {bad}")

# is x in [0,1] actually needed?
p = 1 + x  # coeffs sum = 2
print(f"  is x in [0,1] needed?  p(x)=1+x has ||p||=2 but p(1.5)={float(p.subs(x,sp.Rational(3,2)))} > 2"
      f"  -> YES, the hypothesis is essential.")

# derivative bound d! * ||p||
bad2 = 0
worst_slack = None
for trial in range(300):
    d = random.randint(1, 6)
    co = [Fr(random.randint(-20, 20), random.randint(1, 9)) for _ in range(d + 1)]
    norm = sum(abs(c) for c in co)
    poly = sum(sp.Rational(c) * x**k for k, c in enumerate(co))
    for j in range(0, d + 1):
        dp = sp.diff(poly, x, j)
        for _ in range(12):
            xv = sp.Rational(random.randint(0, 1000), 1000)
            v = abs(dp.subs(x, xv))
            if v > sp.factorial(d) * norm:
                bad2 += 1
print(f"  |p^(j)(x)| <= d! * ||p|| on [0,1]: violations = {bad2}")

print()
print("  WHERE IS IT APPLIED?  ranges of the arguments in this problem:")
print("    t   = m/n,      m in [b+r+1, n]   ->  t   in ( 0, 1 ]        OK")
print("    1-t             (Taylor centre of Hhat_{r-1}, K_{r-1})      ->  [0, 1)   OK")
print("    s   = a/n,      a in [0, n-b-r-1] ->  s   in [ 0, 1 )        OK")
print("    1-s = (n-a)/n                      ->  ( 0, 1 ]              OK")
print("    NB  s := (1-t)+h = (n-m+1)/n  is the ARGUMENT of h_{r-1}, but the Taylor")
print("        expansions in Delta_r are centred at 1-t and evaluated there, so the")
print("        polynomials are never evaluated outside [0,1].  s itself satisfies")
print("        s = (n-m+1)/n <= 1 iff m >= 1, and m >= b+r+1 >= 1, so s in (0,1] too.")
print()

print("=" * 84)
print("ITEM 3a -- falling-factorial product identity  prod_{i=k+1}^m (i-j)/i = C(k,j)/C(m,j)")
print("=" * 84)
# symbolic derivation from scratch:
kk, mm, jj = sp.symbols('k m j', positive=True, integer=True)
lhs_sym = (sp.gamma(mm - jj + 1) / sp.gamma(kk - jj + 1)) / (sp.gamma(mm + 1) / sp.gamma(kk + 1))
rhs_sym = (sp.gamma(kk + 1) / (sp.gamma(jj + 1) * sp.gamma(kk - jj + 1))) / \
          (sp.gamma(mm + 1) / (sp.gamma(jj + 1) * sp.gamma(mm - jj + 1)))
print("  prod_{i=k+1}^m (i-j) = (m-j)!/(k-j)! ,  prod_{i=k+1}^m i = m!/k!")
print("  so LHS = (m-j)! k! / ((k-j)! m!)")
print("  and C(k,j)/C(m,j) = [k!/(j!(k-j)!)] * [j!(m-j)!/m!] = k!(m-j)!/((k-j)! m!)")
print(f"  symbolic difference (gamma form), simplified: {sp.simplify(lhs_sym - rhs_sym)}")
mis = 0
tested = 0
for j in range(1, 9):
    for k in range(j, 30):
        for m in range(k, 40):
            prod = Fr(1)
            for i in range(k + 1, m + 1):
                prod *= Fr(i - j, i)
            rhs = Fr(math.comb(k, j), math.comb(m, j))
            tested += 1
            if prod != rhs:
                mis += 1
                if mis < 5:
                    print(f"    MISMATCH j={j} k={k} m={m}: {prod} vs {rhs}")
print(f"  numeric: {tested} concrete (j,k,m) triples tested, mismatches = {mis}")
print()

print("=" * 84)
print("ITEM 3b -- (1/k)C(k,j) = (1/j)C(k-1,j-1) and the hockey-stick sum")
print("=" * 84)
# symbolic
expr = sp.binomial(kk, jj) / kk - sp.binomial(kk - 1, jj - 1) / jj
print(f"  (1/k)C(k,j) - (1/j)C(k-1,j-1)  simplify -> {sp.simplify(sp.expand_func(expr))}")
mis = 0
tested = 0
for j in range(1, 12):
    for k in range(j, 45):
        if Fr(math.comb(k, j), k) != Fr(math.comb(k - 1, j - 1), j):
            mis += 1
        tested += 1
print(f"  numeric summand identity: {tested} (j,k) pairs, mismatches = {mis}")

mis = 0
tested = 0
for j in range(1, 12):
    for m in range(j, 45):
        lhs = sum(Fr(math.comb(k, j), k) for k in range(j, m + 1))
        rhs = Fr(math.comb(m, j), j)
        if lhs != rhs:
            mis += 1
            if mis < 4:
                print(f"    MISMATCH j={j} m={m}: {lhs} vs {rhs}")
        tested += 1
print(f"  numeric  sum_(k=j)^m (1/k)C(k,j) = C(m,j)/j : {tested} (j,m) pairs, mismatches = {mis}")

# hockey stick itself
mis = 0
for j in range(1, 12):
    for m in range(j, 45):
        if sum(math.comb(l, j - 1) for l in range(j - 1, m)) != math.comb(m, j):
            mis += 1
print(f"  numeric hockey stick  sum_(l=j-1)^(m-1) C(l,j-1) = C(m,j): mismatches = {mis}")
print()

print("=" * 84)
print("ITEM 3c -- does the CRUDE bound really produce a log n?  (constructed independently)")
print("=" * 84)
print("  crude:   |R(m)| <= sum_{k=j}^{m} 1 * E/(k n^2) = (E/n^2) * (H_m - H_{j-1})")
print("  exact :  |R(m)| <= (E/n^2) * (1/(C(m,j))) * sum_{k=j}^m C(k,j)/k = E/(j n^2)")
print()
print(f"  {'j':>3} {'m=n':>6} {'crude factor (H_m-H_(j-1))':>28} {'exact factor 1/j':>18} {'crude/exact':>12}")
for j in (1, 3, 6):
    for n in (10, 100, 1000, 10000, 100000):
        if n < j:
            continue
        Hm = sum(Fr(1, k) for k in range(1, n + 1))
        Hj = sum(Fr(1, k) for k in range(1, j))
        crude = float(Hm - Hj)
        exact = 1.0 / j
        print(f"  {j:>3} {n:>6} {crude:>28.6f} {exact:>18.6f} {crude/exact:>12.3f}")
print()
print("  crude factor grows like log n (H_n ~ ln n + gamma);  exact factor is the")
print("  constant 1/j.  So the document's claim that exact telescoping removes a")
print("  spurious log n that the crude bound would introduce is CORRECT, not overstated.")
print(f"  (check: H_100000 = {float(sum(Fr(1,k) for k in range(1,100001))):.5f}, "
      f"ln(100000)+gamma = {math.log(100000)+0.5772156649:.5f})")
