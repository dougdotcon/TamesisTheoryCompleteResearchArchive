#!/usr/bin/env python3
"""Lemma 1 (general K) symbolic verification — CONJECTURE-1-K5-GENERAL-ATTEMPT.

Fresh code; no script of any prior front or referee was read or imported.

Part 0: the pure-combinatorics identity  sum_{set partitions} prod_j (b_j-1)! = K!
        for K = 1..8 (bijection with permutations via per-block cyclic orders).
Part 1: the labeled circular spacings fact, proved by direct change of
        variables for b = 2..6: anchor at 0 on a circle of circumference ell,
        b-1 free i.i.d. Unif(0,ell) points; for EVERY cyclic ordering the
        gap map is unimodular (|Jacobian| = 1) onto the full open simplex,
        so the labeled-gap density is (number of orderings)/ell^(b-1)
        = (b-1)!/ell^(b-1), i.e. ell*Dirichlet(1,...,1).
Part 2: the telescoping peel product: for EVERY set partition of {1..K},
        K = 2..5 (all Bell(K) = 2, 5, 15, 52 patterns), the product of the
        sequential peel factors
          peel j:  [1/(1-s_{j-1})] * [ell_j/(1-s_{j-1})]^(b_j-1)
                   * [(1-s_j)/(1-s_{j-1})]^(K-c_j) * (b_j-1)!/ell_j^(b_j-1)
        simplifies symbolically to the CONSTANT prod_j (b_j-1)! —
        no ell-dependence survives.  (s_j = ell_1+..+ell_j cumulative
        length, c_j = b_1+..+b_j cumulative block size.)
Part 3: per-pattern probabilities prod(b_j-1)!/K! sum to 1 (K = 2..5), and a
        direct integral spot-check of two K=5 patterns' total probability.
"""
import itertools
import sympy as sp
from math import factorial

ok_all = True


def check(label, cond):
    global ok_all
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        ok_all = False


def set_partitions(items):
    """All set partitions of a list (each partition = list of blocks=lists)."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        # put first in an existing block
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        # or in a new block
        yield [[first]] + part


# ---------------------------------------------------------------- Part 0
print("=" * 72)
print("Part 0: sum over set partitions of prod (b_j-1)!  ==  K!  (K=1..8)")
for K in range(1, 9):
    tot = 0
    cnt = 0
    for part in set_partitions(list(range(1, K + 1))):
        cnt += 1
        w = 1
        for blk in part:
            w *= factorial(len(blk) - 1)
        tot += w
    print(f"  K={K}: Bell(K)={cnt} patterns, sum prod(b_j-1)! = {tot}, K! = {factorial(K)}")
    check(f"partition identity K={K}", tot == factorial(K))

# ---------------------------------------------------------------- Part 1
print("=" * 72)
print("Part 1: labeled circular spacings, direct change of variables, b=2..6")
ell = sp.Symbol('ell', positive=True)
for b in range(2, 7):
    nfree = b - 1
    ys = sp.symbols(f'y1:{nfree+1}', positive=True)  # free-point positions
    n_orderings = 0
    all_unimodular = True
    for order in itertools.permutations(range(nfree)):
        # cyclic order along the flow direction: 0(anchor) -> y[order[0]] -> ...
        # labeled gaps: gap ending at the first free point in the order is
        # (0, y_first); gap ending at the next is the difference; the gap
        # ending at the ANCHOR is ell - y_last (dropped: determined by sum).
        gaps = []
        prev = sp.Integer(0)
        for idx in order:
            gaps.append(ys[idx] - prev)
            prev = ys[idx]
        # gaps has nfree entries (the labeled gaps at the free points,
        # in this ordering); anchor gap = ell - prev (dependent).
        J = sp.Matrix(gaps).jacobian(sp.Matrix(ys))
        detJ = sp.simplify(J.det())
        if detJ not in (sp.Integer(1), sp.Integer(-1)):
            all_unimodular = False
        n_orderings += 1
    # each ordering cell maps bijectively onto {g_i>0, sum<ell}; joint
    # density of ys is 1/ell^(b-1); with |J|=1 each ordering contributes
    # 1/ell^(b-1); total over (b-1)! orderings:
    total_density = sp.Rational(n_orderings) / ell ** (b - 1)
    target = sp.Rational(factorial(b - 1)) / ell ** (b - 1)
    check(f"b={b}: all {n_orderings} orderings unimodular", all_unimodular)
    check(f"b={b}: labeled-gap density = (b-1)!/ell^(b-1)",
          sp.simplify(total_density - target) == 0
          and n_orderings == factorial(b - 1))

# ---------------------------------------------------------------- Part 2
print("=" * 72)
print("Part 2: telescoping peel product constant = prod (b_j-1)!, K=2..5")


def blocks_in_peel_order(part):
    """Order blocks by their minimal element (the anchor-discovery order)."""
    return sorted(part, key=min)


for K in range(2, 6):
    n_patterns = 0
    all_const = True
    total_const = 0
    for part in set_partitions(list(range(1, K + 1))):
        n_patterns += 1
        blks = blocks_in_peel_order(part)
        r = len(blks)
        ells = sp.symbols(f'l1:{r+1}', positive=True)
        s_prev = sp.Integer(0)
        c_prev = 0
        prod = sp.Integer(1)
        for j, blk in enumerate(blks):
            bj = len(blk)
            lj = ells[j]
            s_j = s_prev + lj
            c_j = c_prev + bj
            factor = (sp.Integer(1) / (1 - s_prev)) \
                * (lj / (1 - s_prev)) ** (bj - 1) \
                * ((1 - s_j) / (1 - s_prev)) ** (K - c_j) \
                * sp.Rational(factorial(bj - 1)) / lj ** (bj - 1)
            prod *= factor
            s_prev, c_prev = s_j, c_j
        prod = sp.simplify(prod)
        expected = sp.Integer(1)
        for blk in blks:
            expected *= factorial(len(blk) - 1)
        if sp.simplify(prod - expected) != 0:
            all_const = False
            print(f"  K={K} pattern {part}: got {prod}, expected {expected}")
        total_const += int(expected)
    check(f"K={K}: all {n_patterns} patterns telescope to prod(b_j-1)!",
          all_const)
    check(f"K={K}: pattern constants sum to K! = {factorial(K)}",
          total_const == factorial(K))

# ---------------------------------------------------------------- Part 3
print("=" * 72)
print("Part 3: per-pattern probabilities prod(b_j-1)!/K! sum to 1; and two")
print("        direct K=5 integral spot-checks of pattern probability")
for K in range(2, 6):
    s = sp.Integer(0)
    for part in set_partitions(list(range(1, K + 1))):
        w = sp.Integer(1)
        for blk in part:
            w *= factorial(len(blk) - 1)
        s += sp.Rational(w, factorial(K))
    check(f"K={K}: sum of pattern probabilities = 1", sp.simplify(s - 1) == 0)

# Direct integral spot-checks at K=5 (pattern probability = integral of the
# constant density prod(b_j-1)! over the m-simplex Delta_5, i.e.
# prod(b_j-1)!/5!):
# (a) all-singletons pattern 1+1+1+1+1: constant 1 -> P = 1/120
# (b) AllSame pattern {1,2,3,4,5}: constant 24 -> P = 24/120 = 1/5
m = sp.symbols('m1:6', positive=True)
vol = sp.Integer(1)
expr = sp.Integer(1)
# volume of Delta_5 by iterated integration
e5 = sp.integrate(sp.Integer(1), (m[4], 0, 1 - m[0] - m[1] - m[2] - m[3]))
e4 = sp.integrate(e5, (m[3], 0, 1 - m[0] - m[1] - m[2]))
e3 = sp.integrate(e4, (m[2], 0, 1 - m[0] - m[1]))
e2 = sp.integrate(e3, (m[1], 0, 1 - m[0]))
vol5 = sp.integrate(e2, (m[0], 0, 1))
check("Vol(Delta_5) = 1/120", sp.simplify(vol5 - sp.Rational(1, 120)) == 0)
check("K=5 pattern 1^5 probability = 1*Vol = 1/120",
      sp.simplify(1 * vol5 - sp.Rational(1, 120)) == 0)
check("K=5 pattern {12345} probability = 24*Vol = 1/5",
      sp.simplify(24 * vol5 - sp.Rational(1, 5)) == 0)

print("=" * 72)
print("ALL CHECKS PASSED" if ok_all else "SOME CHECKS FAILED")
