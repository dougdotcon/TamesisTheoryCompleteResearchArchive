# Adversarial referee — independent destination-combinatorics + assembly
# check for K=4.  Built ONLY from the documents' prose; none of the
# front's scripts were read.
#
#   Part A: my own classification of all 5^4=625 raw configs
#           g:{1,2,3,4}->{1,2,3,4,OUT} by (r_on, cycle type), via my own
#           cycle detection; compare against the document's Section 3
#           table (125/200/180/96/24 raw configs; 12 shape types;
#           N(r_on,n_off) constancy across subset/cycle-type choices);
#           also the analytic cross-check N = E*(E+n_off)^(n_off-1) with
#           E = r_on+1.
#   Part B: the off-cycle weight W_C by MY OWN brute-force symbolic
#           enumeration for n_off=1,2,3,4: sum over all off-target
#           assignments with no cycle inside the off-set of the product
#           of target masses; check it equals 1-Q identically, AND that
#           it equals the weighted-forest closed form E*(E+Q)^(n_off-1)
#           before substituting E=1-Q.
#   Part C: MY OWN re-derivation of the per-r density formula (done by
#           hand in the report; here the integral is evaluated exactly):
#             f_r(x) = C(4,r) * 24 * x^r *
#                Int_0^{1-x} (1-Q) Q^(n_off-1)/(n_off-1)!
#                          * (1-x-Q)^(r-1)/(r-1)! dQ
#           for r=1..4 (n_off=4-r), r=0 via the no-cycle weight route
#           AND via a literal 625-term brute-force sum (my own version);
#           compare each against the document's five claimed per-r
#           polynomials, their integrals (1/5,2/5,2/7,1/10,1/70), the
#           final sum vs 8x(1-x^2)^3, and the moments
#           E[M4]=128/315, E[M4^2]=1/5, E[M4^3]=128/1155.
#   Part D: per-r target-level probabilities via a SECOND independent
#           route: P(r_on=r) = C(4,r) * sum over cycle perms of E_m[
#           prod_on m_{sigma(i)} ... ] -- i.e. direct symbolic simplex
#           integration of my own P(shape|m) polynomials, never using
#           the x-marginalized densities.
#
# Exact arithmetic (sympy.Rational) throughout.

import itertools
import sympy as sp
from sympy import Rational, factorial, binomial, symbols, integrate, \
    simplify, expand

x = symbols("x", positive=True)
Q = symbols("Q", positive=True)
m1, m2, m3, m4 = symbols("m1 m2 m3 m4", positive=True)
MS = [m1, m2, m3, m4]
OUT = 4  # target code for OUT; regions are 0..3


def cycle_nodes(g):
    """My own cycle detection on a functional digraph over {0,1,2,3}
    with terminal OUT=4.  Node i is on a cycle iff iterating g from i
    returns to i within 4 steps."""
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


def cycle_type(g, on):
    """Cycle type (sorted tuple of cycle lengths) of g restricted to the
    on-cycle set."""
    seen = set()
    lens = []
    for i in sorted(on):
        if i in seen:
            continue
        # walk the cycle through i
        cyc = [i]
        cur = g[i]
        while cur != i:
            cyc.append(cur)
            cur = g[cur]
        for c in cyc:
            seen.add(c)
        lens.append(len(cyc))
    return tuple(sorted(lens, reverse=True))


print("=" * 72)
print("PART A — my own classification of all 625 raw configurations")
print("=" * 72)
from collections import defaultdict
by_r = defaultdict(int)
by_shape = defaultdict(int)              # (r_on, cycle_type) -> count
by_cell = {}                             # config -> (on, ctype)
noffcount = defaultdict(set)             # (r_on, n_off) -> set of counts per (C, sigma)
percfg = defaultdict(int)                # (frozenset C, sigma as tuple) -> raw count
for g in itertools.product(range(5), repeat=4):
    on = cycle_nodes(g)
    ct = cycle_type(g, on)
    r = len(on)
    by_r[r] += 1
    by_shape[(r, ct)] += 1
    by_cell[g] = (on, ct)
    sigma = tuple(g[i] for i in sorted(on))
    percfg[(on, sigma)] += 1

print("per-r_on raw counts:", dict(sorted(by_r.items())))
assert dict(by_r) == {0: 125, 1: 200, 2: 180, 3: 96, 4: 24}, by_r
print("shape types (r_on, cycle type) -> raw count:")
for k in sorted(by_shape):
    print("   ", k, "->", by_shape[k])
assert len(by_shape) == 12, len(by_shape)
# per-r shape-type counts must be 1,1,2,3,5 (partition numbers)
sh_per_r = defaultdict(int)
for (r, ct) in by_shape:
    sh_per_r[r] += 1
assert dict(sh_per_r) == {0: 1, 1: 1, 2: 2, 3: 3, 4: 5}, sh_per_r
print("shape types per r_on:", dict(sorted(sh_per_r.items())),
      " = partition numbers p(0..4) -> total 12  OK")

# N(r_on, n_off) constancy: for each specific (C, sigma) the number of
# raw configs must depend only on (r_on, n_off)
for (on, sigma), cnt in percfg.items():
    noffcount[(len(on), 4 - len(on))].add(cnt)
print("N(r_on,n_off) values (must be singletons):")
claimedN = {(0, 4): 125, (1, 3): 50, (2, 2): 15, (3, 1): 4, (4, 0): 1}
for k in sorted(noffcount):
    vals = noffcount[k]
    print("   ", k, "->", sorted(vals))
    assert len(vals) == 1, (k, vals)
    assert vals == {claimedN[k]}, (k, vals)
# analytic forest-count cross-check: N = E*(E+n_off)^(n_off-1), E=r+1
for (r, noff), _ in claimedN.items():
    if noff == 0:
        pred = 1
    else:
        E = r + 1
        pred = E * (E + noff) ** (noff - 1)
    assert pred == claimedN[(r, noff)], (r, noff, pred)
print("analytic N = (r+1)*(r+1+n_off)^(n_off-1) matches all five  OK")
# coarse totals
tot = sum(binomial(4, r) * factorial(r) * claimedN[(r, 4 - r)]
          for r in range(5))
assert tot == 625
print("sum_r C(4,r) r! N(r,4-r) =", tot, " OK")
print("PART A: PASS\n")


print("=" * 72)
print("PART B — off-cycle weight W_C by my own symbolic enumeration")
print("=" * 72)
# n_off off-cycle nodes with symbolic masses q_1..q_noff; external
# (on-cycle regions + OUT) combined weight e.  Each off node targets:
# external (weight e) or one of the off nodes (weight q_l), such that NO
# cycle forms among the off nodes (a cycle would put them on-cycle,
# contradiction; self-loops count as cycles).  Sum the products.
e = symbols("e", positive=True)
for noff in range(1, 5):
    qs = symbols(f"q1:{noff+1}", positive=True)
    total = sp.Integer(0)
    nvalid = 0
    # targets: 0..noff-1 = off node index, noff = external
    for assign in itertools.product(range(noff + 1), repeat=noff):
        # detect cycles among off nodes
        has_cycle = False
        for i in range(noff):
            cur = i
            for _ in range(noff):
                t = assign[cur]
                if t == noff:
                    break
                cur = t
                if cur == i:
                    has_cycle = True
                    break
            if has_cycle:
                break
        if has_cycle:
            continue
        nvalid += 1
        w = sp.Integer(1)
        for i in range(noff):
            w *= e if assign[i] == noff else qs[assign[i]]
        total += w
    total = expand(total)
    Qsum = sum(qs)
    forest = expand(e * (e + Qsum) ** (noff - 1))
    print(f"n_off={noff}: valid assignments={nvalid}, "
          f"W == e*(e+Q)^(n_off-1): {simplify(total - forest) == 0}")
    assert simplify(total - forest) == 0
    # substitute e = 1 - Q  ->  W = 1 - Q
    sub = expand(total.subs(e, 1 - Qsum))
    assert simplify(sub - (1 - Qsum)) == 0
    print(f"          with e = 1-Q:  W = 1-Q identically: "
          f"{simplify(sub - (1 - Qsum)) == 0}")
print("PART B: PASS  (includes n_off=3, the case exceeding K=3's max, "
      "and n_off=4)\n")


print("=" * 72)
print("PART C — per-r densities via my own re-derived formula")
print("=" * 72)
# My own derivation (see report Section 4 for the hand derivation):
# fix C (|C|=r>=1) and a cycle permutation sigma on C.  Change variables
# m_j = D_j + P_{sigma^-1(j)} (unit Jacobian): joint density of
# ({P_i},{D_j}, off-masses) = 24*(1-Q) on {all>0, sum P + sum D + Q < 1},
# independent of sigma -> factor r!.  M = 1 - sum P - Q; the D's are free
# on {sum D < x} (volume x^r/r!); s := sum P has surface density
# s^{r-1}/(r-1)!; Q has surface density Q^{n_off-1}/(n_off-1)!.
claimed = {
    0: -4 * x**4 + 12 * x**3 - 12 * x**2 + 4 * x,
    1: -12 * x**5 + 32 * x**4 - 24 * x**3 + 4 * x,
    2: -12 * x**6 + 24 * x**5 - 24 * x**3 + 12 * x**2,
    3: -4 * x**7 + 24 * x**5 - 32 * x**4 + 12 * x**3,
    4: -4 * x**7 + 12 * x**6 - 12 * x**5 + 4 * x**4,
}
claimed_probs = {0: Rational(1, 5), 1: Rational(2, 5), 2: Rational(2, 7),
                 3: Rational(1, 10), 4: Rational(1, 70)}

derived = {}
for r in range(1, 5):
    noff = 4 - r
    if noff == 0:
        # no Q integral: f_4(x) = C(4,4)*24*x^4*(1-x)^{r-1}/(r-1)!  with
        # s = 1-x exactly, W=1 (empty product):
        f = binomial(4, 4) * 24 * x**4 * (1 - x) ** (4 - 1) / factorial(3)
        f = expand(f)
    else:
        integrand = (1 - Q) * Q ** (noff - 1) / factorial(noff - 1) \
            * (1 - x - Q) ** (r - 1) / factorial(r - 1)
        I = integrate(integrand, (Q, 0, 1 - x))
        f = expand(binomial(4, r) * 24 * x**r * I)
    derived[r] = f
    match = simplify(f - claimed[r]) == 0
    print(f"r={r}: my formula -> {f}")
    print(f"      document    -> {expand(claimed[r])}   MATCH={match}")
    assert match

# r=0 route 1: no-cycle weight with external = OUT only: W0 = OUT = x at
# OUT=x (forest identity, my Part B at n_off=4 with e=OUT, Q=sum all m,
# e+Q=1).  Density of OUT under uniform-24 on Delta_4: OUT~Beta(1,4),
# density 4(1-t)^3 at OUT=t... careful: density of OUT at value t is
# 4 t^3?  OUT = 1-sum m; sum m ~ Beta(4,1) (density 4 s^3); so OUT has
# density 4(1-t)^3.  f_0(x) = 4(1-x)^3 * x.
f0_route1 = expand(4 * (1 - x) ** 3 * x)
print(f"r=0 route 1 (forest weight * OUT density): {f0_route1}")
assert simplify(f0_route1 - claimed[0]) == 0

# r=0 route 2: literal brute-force sum over the 125 no-cycle configs of
# prod of target masses, then exact marginalization over Delta_4 at
# OUT=x.  P_T0(m) = sum over no-cycle g of prod_i w_{g(i)}, w_j = m_j,
# w_OUT = 1-m1-m2-m3-m4.  Then f_0(x) = d/dx' [ ... ] -- easier: the
# conditional density of OUT at x carries weight:
#   f_0(x) = Int_{sum m = 1-x} 24 * P_T0(m) dS   (surface integral)
# computed by substituting m4 = (1-x) - m1 - m2 - m3 and integrating
# m1,m2,m3 over the scaled simplex (the (m1,m2,m3)->surface map has unit
# surface-density factor in these coordinates).
OUTm = 1 - m1 - m2 - m3 - m4
w = {0: m1, 1: m2, 2: m3, 3: m4, OUT: OUTm}
PT0 = sp.Integer(0)
n0 = 0
for g, (on, ct) in by_cell.items():
    if len(on) == 0:
        n0 += 1
        PT0 += w[g[0]] * w[g[1]] * w[g[2]] * w[g[3]]
assert n0 == 125
PT0 = expand(PT0)
# sanity: forest identity says PT0 == OUTm (times 1) identically:
print("brute-force P_T0(m) == (1-m1-m2-m3-m4) identically:",
      simplify(PT0 - OUTm) == 0)
assert simplify(PT0 - OUTm) == 0
sub = PT0.subs(m4, (1 - x) - m1 - m2 - m3)
I = integrate(sub, (m3, 0, (1 - x) - m1 - m2))
I = integrate(I, (m2, 0, (1 - x) - m1))
I = integrate(I, (m1, 0, 1 - x))
f0_route2 = expand(24 * I)
print(f"r=0 route 2 (literal 625/125-term brute-force sum): {f0_route2}")
assert simplify(f0_route2 - claimed[0]) == 0
derived[0] = f0_route1

# per-r probabilities and total
total_f = sp.Integer(0)
for r in range(5):
    p = integrate(derived[r], (x, 0, 1))
    print(f"r={r}: integral = {p}   claimed {claimed_probs[r]}   "
          f"match={simplify(p - claimed_probs[r]) == 0}")
    assert simplify(p - claimed_probs[r]) == 0
    total_f += derived[r]
total_f = expand(total_f)
target = expand(8 * x * (1 - x**2) ** 3)
print(f"sum of five groups: {total_f}")
print(f"8x(1-x^2)^3       : {target}")
assert simplify(total_f - target) == 0
print("FINAL SUM MATCHES 8x(1-x^2)^3 EXACTLY")

mom1 = integrate(x * total_f, (x, 0, 1))
mom2 = integrate(x**2 * total_f, (x, 0, 1))
mom3 = integrate(x**3 * total_f, (x, 0, 1))
mass = integrate(total_f, (x, 0, 1))
wallis = Rational(4**4 * factorial(4)**2, factorial(9))
print(f"int f = {mass};  E[M4] = {mom1} (128/315? "
      f"{mom1 == Rational(128, 315)}, Wallis 4^K K!^2/(2K+1)! = {wallis});")
print(f"E[M4^2] = {mom2} (1/5? {mom2 == Rational(1, 5)});  "
      f"E[M4^3] = {mom3} (128/1155? {mom3 == Rational(128, 1155)})")
assert mass == 1 and mom1 == Rational(128, 315) == wallis
assert mom2 == Rational(1, 5) and mom3 == Rational(128, 1155)
print("PART C: PASS\n")


print("=" * 72)
print("PART D — per-r probabilities via direct symbolic simplex integration")
print("=" * 72)
# Second independent route: P(r_on = r) = Int_{Delta_4} 24 * P_r(m) dm,
# where P_r(m) = sum over raw configs with |on|=r of prod over
# NON-on-cycle nodes of w_{g(i)} times prod over on-cycle nodes of
# m_{g(i)} (on-cycle node i needs u_i in region g(i): probability
# m_{g(i)}).  Built from my own by_cell classification.
def simplex_integral(poly):
    """Exact integral of a polynomial in m1..m4 over Delta_4 via the
    Dirichlet formula Int prod m_i^{a_i} dm = prod a_i! / (sum a_i+4)!."""
    poly = sp.Poly(expand(poly), m1, m2, m3, m4)
    tot = Rational(0)
    for mono, coeff in zip(poly.monoms(), poly.coeffs()):
        a = sum(mono)
        num = sp.prod([factorial(k) for k in mono])
        tot += coeff * Rational(num, factorial(a + 4))
    return tot


Pr = defaultdict(lambda: sp.Integer(0))
for g, (on, ct) in by_cell.items():
    term = sp.Integer(1)
    for i in range(4):
        if i in on:
            term *= MS[g[i]]        # on-cycle: u_i must be in region g(i)
        else:
            term *= w[g[i]]
    Pr[len(on)] += term
tot_p = Rational(0)
for r in range(5):
    p = 24 * simplex_integral(expand(Pr[r]))
    print(f"P(r_on={r}) = {p}   claimed {claimed_probs[r]}   "
          f"match={p == claimed_probs[r]}")
    assert p == claimed_probs[r]
    tot_p += p
assert tot_p == 1
print(f"sum = {tot_p}  OK")

# sub-shape granularity: P(cycle type | r_on) must be proportional to the
# number of permutations of each cycle type (sigma-exchangeability):
print("\nsub-shape (cycle-type) probabilities, sigma-exchangeability check:")
perm_counts = {(): 1, (1,): 1, (1, 1): 1, (2,): 1,
               (1, 1, 1): 1, (2, 1): 3, (3,): 2,
               (1, 1, 1, 1): 1, (2, 1, 1): 6, (2, 2): 3, (3, 1): 8, (4,): 6}
Psh = defaultdict(lambda: sp.Integer(0))
for g, (on, ct) in by_cell.items():
    term = sp.Integer(1)
    for i in range(4):
        term *= MS[g[i]] if i in on else w[g[i]]
    Psh[(len(on), ct)] += term
for (r, ct) in sorted(Psh):
    p = 24 * simplex_integral(expand(Psh[(r, ct)]))
    if r == 0:
        continue
    nperm_total = factorial(r)
    want = claimed_probs[r] * Rational(perm_counts[ct], nperm_total)
    print(f"  (r={r}, ct={ct}): P = {p}, predicted "
          f"P(r)*#perms/r! = {want}, match={p == want}")
    assert p == want
print("PART D: PASS")
print("\nALL PARTS PASS")
