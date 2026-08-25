# Adversarial referee — RAW-625 exact moment computation for K=4.
#
# This is the referee's strongest independent symbolic surface: it does
# NOT use the shape collapse, the sigma-independence argument, the
# W=1-Q / weighted-forest identity, the (m,P)->(P,D) change of
# variables, or the per-r integral formula.  It uses only:
#   (i)  Lemma 1: (m1..m4) uniform, density 24, on Delta_4
#        (independently re-proved in indep_lemma1_k4.py);
#   (ii) the referee's OWN classification of each raw config's on-cycle
#        set (indep cycle detection, same as indep_shapes_k4.py Part A);
#   (iii) M = 1 - sum_{k off-cycle} m_k - sum_{i on-cycle} P_i, the arc
#        formula validated discretely and per-configuration by the
#        mechanism check (indep_discrete_checks_k4.py).
#
# For every raw config g (all 625), grouped by (C, sigma):
#   E[M^p 1{config class}] =
#     Int_{Delta_4} 24 * S_off(m) * B_p(m) dm
# where S_off(m) = sum over that class's off-target assignments of the
# product of target masses (RAW enumeration, no closed form assumed) and
#   B_p(m) = Int over P_i in (0, m_{g(i)}), i in C, of
#            (1 - sum_off m - sum P)^p dP        (density 1 per P_i).
# The final Delta_4 integral is exact via the Dirichlet monomial formula.
#
# Compared against the document's five claimed per-r polynomials:
#   E[M^p 1{r_on=r}] must equal Int_0^1 x^p f_r(x) dx  for p=0..8.
# Since each claimed f_r is a polynomial of degree <= 7, matching
# moments p=0..8 on [0,1] pins the density: if the true per-group
# marginal had any degree-<=7 polynomial density differing from f_r, a
# mismatch would show at some p<=8 (difference orthogonal to all
# polynomials of degree <=8 implies zero for degree-<=7 differences,
# with one power to spare).
#
# Exact arithmetic (sympy.Rational) throughout.

import itertools
from collections import defaultdict
import sympy as sp
from sympy import Rational, factorial, symbols, integrate, expand, simplify

x = symbols("x", positive=True)
m1, m2, m3, m4 = symbols("m1 m2 m3 m4", positive=True)
MS = [m1, m2, m3, m4]
OUT = 4
OUTm = 1 - m1 - m2 - m3 - m4
w = {0: m1, 1: m2, 2: m3, 3: m4, OUT: OUTm}
PMAX = 8


def cycle_nodes(g):
    on = set()
    for i in range(4):
        cur = i
        for _ in range(4):
            t = g[cur]
            if t == OUT:
                break
            cur = t
            if cur == i:
                on.add(i)
                break
    return frozenset(on)


def simplex_integral(poly):
    """Exact Int_{Delta_4} of a polynomial in m1..m4 via
    Int prod m_i^{a_i} dm = prod a_i! / (sum a_i + 4)!."""
    P = sp.Poly(expand(poly), m1, m2, m3, m4)
    tot = Rational(0)
    for mono, coeff in zip(P.monoms(), P.coeffs()):
        num = sp.prod([factorial(k) for k in mono])
        tot += Rational(coeff) * Rational(num, factorial(sum(mono) + 4))
    return tot


# ---- collect off-target weight sums per (C, sigma) from RAW enumeration
print("collecting raw off-target weight sums per (C, sigma)...")
Soff = defaultdict(lambda: sp.Integer(0))
count = defaultdict(int)
for g in itertools.product(range(5), repeat=4):
    on = cycle_nodes(g)
    sigma = tuple((i, g[i]) for i in sorted(on))
    term = sp.Integer(1)
    for k in range(4):
        if k not in on:
            term *= w[g[k]]
    Soff[(on, sigma)] += term
    count[(on, sigma)] += 1
nclasses = len(Soff)
print(f"(C, sigma) classes: {nclasses}  (expected 65 = 1+4+12+24+24)")
assert nclasses == 65
assert sum(count.values()) == 625

# ---- per-class exact moments
print("computing exact E[M^p 1{class}] for p=0..8, all 65 classes...")
per_r_mom = defaultdict(lambda: [Rational(0)] * (PMAX + 1))
Ps = symbols("P0 P1 P2 P3", positive=True)
for (on, sigma), S in Soff.items():
    r = len(on)
    offlist = [k for k in range(4) if k not in on]
    A = 1 - sum(MS[k] for k in offlist)
    Ponvars = [Ps[i] for i in range(r)]
    onlist = sorted(on)
    targets = dict(sigma)          # i -> g(i), the region u_i lands in
    for p in range(PMAX + 1):
        integrand = (A - sum(Ponvars)) ** p if r > 0 else A ** p
        # integrate each P over (0, m_{g(i)})
        expr = integrand
        for idx, i in enumerate(onlist):
            expr = integrate(expr, (Ponvars[idx], 0, MS[targets[i]]))
        val = simplex_integral(24 * S * expr)
        per_r_mom[r][p] += val

# ---- compare with the document's claimed per-r polynomials
claimed = {
    0: -4 * x**4 + 12 * x**3 - 12 * x**2 + 4 * x,
    1: -12 * x**5 + 32 * x**4 - 24 * x**3 + 4 * x,
    2: -12 * x**6 + 24 * x**5 - 24 * x**3 + 12 * x**2,
    3: -4 * x**7 + 24 * x**5 - 32 * x**4 + 12 * x**3,
    4: -4 * x**7 + 12 * x**6 - 12 * x**5 + 4 * x**4,
}
print()
allok = True
for r in range(5):
    for p in range(PMAX + 1):
        want = integrate(x**p * claimed[r], (x, 0, 1))
        got = per_r_mom[r][p]
        ok = simplify(got - want) == 0
        if not ok:
            allok = False
            print(f"  MISMATCH r={r} p={p}: raw625={got}, claimed={want}")
    print(f"r={r}: all moments p=0..{PMAX} match the claimed f_r exactly "
          f"(e.g. p=0: {per_r_mom[r][0]}, p=1: {per_r_mom[r][1]})")
assert allok

# ---- totals vs 8x(1-x^2)^3
target = 8 * x * (1 - x**2) ** 3
print()
for p in range(PMAX + 1):
    tot = sum(per_r_mom[r][p] for r in range(5))
    want = integrate(x**p * target, (x, 0, 1))
    assert simplify(tot - want) == 0, (p, tot, want)
print(f"total E[M^p], p=0..{PMAX}, all match 8x(1-x^2)^3's moments exactly")
print(f"  E[M]   = {sum(per_r_mom[r][1] for r in range(5))}  (=128/315)")
print(f"  E[M^2] = {sum(per_r_mom[r][2] for r in range(5))}  (=1/5)")
print(f"  E[M^3] = {sum(per_r_mom[r][3] for r in range(5))}  (=128/1155)")
print("\nRAW-625 MOMENT CHECK: PASS — the five per-r densities and their")
print("sum are exactly reproduced from the raw 625-config enumeration,")
print("using none of the document's collapse machinery.")
