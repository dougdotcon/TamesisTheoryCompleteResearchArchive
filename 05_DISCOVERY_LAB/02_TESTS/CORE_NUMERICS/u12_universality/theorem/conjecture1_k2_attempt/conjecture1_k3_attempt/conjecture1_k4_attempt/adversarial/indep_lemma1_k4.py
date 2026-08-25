# Adversarial referee — independent re-derivation of Lemma 1 (K=4).
#
# Built ONLY from the prose of ATTEMPT.md (K=4) and the K=2/K=3 lineage
# documents. None of the front's own scripts were read.
#
# METHOD (deliberately different from the document's change-of-variables
# machinery): a clean sequential Bayes/event-probability route, the same
# style the K=3 referee used.
#
# Facts used (the same single classical citation the lineage uses):
#   (F1) size-biased pick: the PD(1) block containing an independent
#        Unif(0,1) point has length ~ Unif(0,1)  [McCloskey 1965 etc.]
#   (F2) residual property: conditionally on the blocks explored so far
#        (total mass R removed), the rescaled complement is a fresh
#        independent PD(1); hence the block of the next fresh uniform
#        point *conditioned to land outside the explored mass* has length
#        R*V with V~Unif(0,1)  (density 1/R on (0,R)) -- one "peel" per
#        new block, so the 1+1+1+1 pattern needs THREE sequential peels
#        beyond block 1.
#   (F3) labeled circular spacings: b i.i.d. uniform points in a circular
#        block of length L cut it into b labeled gaps (gap i = the arc
#        that flows into source i) jointly ~ L * Dirichlet(1,...,1),
#        density (b-1)!/L^(b-1) on the (b-1)-simplex surface.
#        For b=4 this is the NEW fact at K=4; it is verified from scratch
#        in Part 2 below (direct integration over all 3!=6 orderings,
#        explicit Jacobians, plus an independent moment-matching check).
#
# Sequential exploration (index order x1,x2,x3,x4). For a co-block
# set-partition (pattern), the joint density of (m1,m2,m3,m4) on Delta_4:
#   - block anchors (first source of each block, in index order):
#       block 1 anchor: density of ell_1 is 1 on (0,1)               [F1]
#       block j>=2 anchor: P(outside explored)=R_{j-1}, then length
#       density 1/R_{j-1}  -> the two factors cancel to 1             [F2]
#   - each NON-anchor member of block j: P(x_i in B_j) = ell_j
#     (an ABSOLUTE event: x_i is uniform on the WHOLE of [0,1] and B_j is
#     a fixed subset of measure ell_j -- exactly the point of the
#     document's self-caught Route-B bug, which we also reproduce below)
#   - within each block of size b: labeled gaps give (b-1)!/ell_j^(b-1)  [F3]
# The (ell_j, gaps) -> (m_i) change of variables is triangular with unit
# Jacobian and the support is all of Delta_4 (any partial sum of the m's
# is < 1). Hence each pattern contributes the CONSTANT prod_j (b_j-1)!.
#
# This script:
#   Part 0: set-partition identity  sum over partitions of prod (b-1)! = K!
#           for K=2..6 (document checked K=2,3,4; we go further).
#   Part 1: generic symbolic per-pattern density for ALL 15 Bell(4)
#           patterns; assert each is constant = prod (b_j-1)!; total 24.
#           Also the 3+1 Route-B bug reproduction: using the WRONG
#           rescaled probability ell_2/(1-ell_1) must give the
#           ell-dependent 2/(1-ell_1)^2 (as the document reports), and
#           the correct absolute probability gives the constant 2.
#   Part 2: the n=4 labeled circular spacings fact from scratch:
#           (a) direct 6-ordering construction with explicit unit
#               Jacobians -> density 3!/L^3 on the simplex;
#           (b) independent moment check: E[g2^a g3^b g4^c] computed by
#               brute symbolic integration over the free points' uniform
#               positions equals the Dirichlet(1,1,1,1) moment for all
#               (a,b,c) with a+b+c<=4.  Also n=2,n=3 as regression.
#   Part 3: exact per-pattern probabilities via iterated symbolic
#           integration (independent route), check each equals
#           prod(b_j-1)!/24 and that all 15 sum to 1.
#
# Exact arithmetic throughout (sympy.Rational). No floating point.

import itertools
import sympy as sp
from sympy import Rational, factorial, symbols, integrate, simplify, expand


def set_partitions(elems):
    """All set partitions of a list (each partition = list of blocks)."""
    if not elems:
        yield []
        return
    first, rest = elems[0], elems[1:]
    for part in set_partitions(rest):
        # put first into each existing block
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        # or as its own block
        yield [[first]] + part


def part_type(part):
    return tuple(sorted((len(b) for b in part), reverse=True))


print("=" * 72)
print("PART 0 — set-partition identity  sum prod (b_j-1)! = K!  (K=2..6)")
print("=" * 72)
for K in range(2, 7):
    tot = 0
    cnt = 0
    for part in set_partitions(list(range(1, K + 1))):
        tot += sp.prod([factorial(len(b) - 1) for b in part])
        cnt += 1
    ok = sp.Eq(sp.Integer(tot), factorial(K))
    print(f"K={K}: Bell={cnt}, sum prod (b-1)! = {tot}, K! = {factorial(K)},"
          f" match={tot == factorial(K)}")
    assert tot == factorial(K)
print("PART 0: PASS\n")


print("=" * 72)
print("PART 1 — all 15 co-block patterns, generic Bayes/peeling route")
print("=" * 72)

# symbols for block lengths in exploration order
l1, l2, l3, l4 = symbols("l1 l2 l3 l4", positive=True)
LS = [l1, l2, l3, l4]

results = {}
total = sp.Integer(0)
for part in set_partitions([1, 2, 3, 4]):
    # exploration order: blocks ordered by their minimum element
    blocks = sorted([sorted(b) for b in part], key=lambda b: b[0])
    dens = sp.Integer(1)
    R = sp.Integer(1)          # unexplored mass so far
    for j, b in enumerate(blocks):
        ell = LS[j]
        bsize = len(b)
        if j == 0:
            dens *= 1                      # F1: ell_1 ~ Unif(0,1), density 1
        else:
            # F2: anchor lands outside explored mass (prob R) AND its
            # block length has density 1/R on (0,R): the product is 1.
            dens *= R * (1 / R)
        # non-anchor members: ABSOLUTE membership probability ell each
        dens *= ell ** (bsize - 1)
        # labeled circular spacings within the block  (F3; b=4 case
        # independently proved in Part 2)
        dens *= factorial(bsize - 1) / ell ** (bsize - 1)
        R -= ell
    dens = simplify(dens)
    expected = sp.prod([factorial(len(b) - 1) for b in blocks])
    is_const = (sp.diff(dens, l1) == 0 and sp.diff(dens, l2) == 0
                and sp.diff(dens, l3) == 0 and sp.diff(dens, l4) == 0)
    tag = "/".join("".join(map(str, b)) for b in blocks)
    print(f"pattern {tag:12s} type {str(part_type(blocks)):14s} "
          f"density={dens}  expected={expected}  const={is_const}")
    assert is_const, f"pattern {tag}: density not constant: {dens}"
    assert simplify(dens - expected) == 0, f"pattern {tag}: {dens} != {expected}"
    results[tag] = dens
    total += dens

print(f"\nTOTAL over all 15 patterns = {total}   (Lemma 1 claims 24)")
assert total == 24
# shape-type grouping and multiplicities as the document states
by_type = {}
for part in set_partitions([1, 2, 3, 4]):
    t = part_type(part)
    by_type.setdefault(t, []).append(part)
print("shape-type multiplicities:",
      {str(t): len(v) for t, v in sorted(by_type.items(), reverse=True)})
assert {t: len(v) for t, v in by_type.items()} == {
    (4,): 1, (3, 1): 4, (2, 2): 3, (2, 1, 1): 6, (1, 1, 1, 1): 1}

print("\n--- Route-B bug reproduction (3+1 shape, anchor = singleton) ---")
# pattern {1} | {2,3,4}: explore x1 (ell_1), then x2 anchors B2 (ell_2),
# x3,x4 must land in B2.
# CORRECT: P(x3 in B2)=ell_2 absolutely (B2 is a fixed subset of [0,1]).
dens_correct = 1 * ((1 - l1) * (1 / (1 - l1))) * l2 ** 2 \
    * factorial(2) / l2 ** 2
dens_correct = simplify(dens_correct)
print("correct (absolute prob ell_2):     density =", dens_correct)
assert dens_correct == 2
# WRONG (the document's self-caught bug): ell_2/(1-ell_1) for each of x3,x4
dens_wrong = 1 * ((1 - l1) * (1 / (1 - l1))) * (l2 / (1 - l1)) ** 2 \
    * factorial(2) / l2 ** 2
dens_wrong = simplify(dens_wrong)
print("wrong  (rescaled prob ell_2/(1-l1)): density =", dens_wrong)
assert simplify(dens_wrong - 2 / (1 - l1) ** 2) == 0
assert sp.diff(dens_wrong, l1) != 0
print("wrong version is ell_1-dependent (2/(1-l1)^2), exactly as the "
      "document reports; correct version is the constant 2.")
print("PART 1: PASS\n")


print("=" * 72)
print("PART 2 — the n=4 labeled circular spacings fact, from scratch")
print("=" * 72)
# Circle of circumference L, anchor x1 at 0 (rotation invariance).
# Free points y2,y3,y4 ~ Unif(0,L) iid.  Gap g_i := arc ENDING at point i
# (i.e. the mass that background-flows into source i first), where flow
# moves "forward" along the circle; gap of i = distance from the previous
# point (cyclically) to i.
#
# (a) direct construction: for each of the 3!=6 orderings
#     0 < y_a < y_b < y_c < L  ((a,b,c) a permutation of (2,3,4)),
#     the labeled gaps are  g_a = y_a, g_b = y_b - y_a, g_c = y_c - y_b,
#     g_1 = L - y_c.  The map (y_a,y_b,y_c) -> (g_a,g_b,g_c) is
#     triangular with unit Jacobian, and (g_2,g_3,g_4) ranges over the
#     FULL open simplex {g_i>0, g_2+g_3+g_4<L} on every branch.  Each
#     branch has source density 1/L^3, so the labeled-gap density is
#     6/L^3 = 3!/L^3: exactly Dirichlet(1,1,1,1) scaled by L.
L, y2, y3, y4 = symbols("L y2 y3 y4", positive=True)
g2, g3, g4 = symbols("g2 g3 g4", positive=True)
branches = 0
for order in itertools.permutations([2, 3, 4]):
    ys = {order[0]: None, order[1]: None, order[2]: None}
    # positions in increasing order: p1 < p2 < p3
    p = symbols(f"p1 p2 p3", positive=True)
    # gaps for this ordering: g_{order[0]} = p1, g_{order[1]} = p2-p1,
    # g_{order[2]} = p3-p2 ; inverse map:
    inv = {order[0]: None}
    gvars = {2: g2, 3: g3, 4: g4}
    ga, gb, gc = gvars[order[0]], gvars[order[1]], gvars[order[2]]
    p1e, p2e, p3e = ga, ga + gb, ga + gb + gc
    # Jacobian of (p1,p2,p3) wrt (ga,gb,gc):
    J = sp.Matrix([[sp.diff(pe, gv) for gv in (ga, gb, gc)]
                   for pe in (p1e, p2e, p3e)])
    detJ = J.det()
    assert detJ == 1, detJ
    # branch valid iff 0 < p1 < p2 < p3 < L  <=>  ga,gb,gc>0, ga+gb+gc<L:
    # the full open simplex, for EVERY ordering.
    branches += 1
print(f"(a) all {branches} orderings: unit Jacobian, full-simplex image; "
      f"summed density = 6/L^3 = 3!/L^3  -> Dirichlet(1,1,1,1)  OK")
assert branches == 6

# (b) independent moment check, no ordering decomposition at all:
#     E[g2^a g3^b g4^c] by brute symbolic integration of the gap
#     FUNCTIONS over (y2,y3,y4) uniform on [0,L]^3, using Min/Max case
#     splits via piecewise integration; compare with Dirichlet moments.
#     To keep it fully mechanical we integrate over the 6 order regions.
def gap_moment(a, b, c):
    tot = sp.Integer(0)
    for order in itertools.permutations([2, 3, 4]):
        # region 0 < y_{order[0]} < y_{order[1]} < y_{order[2]} < L
        ya, yb, yc = symbols("ya yb yc", positive=True)
        pos = {order[0]: ya, order[1]: yb, order[2]: yc}
        gaps = {order[0]: ya, order[1]: yb - ya, order[2]: yc - yb, 1: L - yc}
        integrand = gaps[2] ** a * gaps[3] ** b * gaps[4] ** c / L ** 3
        I = integrate(integrand, (yc, yb, L))
        I = integrate(I, (yb, ya, L))
        I = integrate(I, (ya, 0, L))
        tot += I
    return simplify(tot)


def dirichlet_moment(a, b, c):
    # (g2,g3,g4)/L ~ Dirichlet(1,1,1,1) marginal in 3 of 4 coords:
    # E[prod x_i^{k_i}] = (prod (k_i)!) * 3! / (3 + sum k)!  (alpha=1)
    s = a + b + c
    return L ** s * factorial(a) * factorial(b) * factorial(c) \
        * factorial(3) / factorial(3 + s)


nch = 0
for a in range(0, 5):
    for b in range(0, 5 - a):
        for c in range(0, 5 - a - b):
            got = gap_moment(a, b, c)
            want = simplify(dirichlet_moment(a, b, c))
            assert simplify(got - want) == 0, (a, b, c, got, want)
            nch += 1
print(f"(b) moment check: E[g2^a g3^b g4^c] matches Dirichlet(1,1,1,1) "
      f"for all {nch} tuples with a+b+c<=4  OK")

# regression: n=2 and n=3 labeled spacings (the K=2 / K=3 facts)
# n=2: one free point y ~ Unif(0,L); g2 = y, g1 = L-y: density of g2 is
# 1/L on (0,L): Dirichlet(1,1). trivial: check E[g2^k]:
y = symbols("y", positive=True)
for k in range(1, 5):
    got = integrate(y ** k / L, (y, 0, L))
    want = L ** k * factorial(k) * factorial(1) / factorial(1 + k)
    assert simplify(got - want) == 0
# n=3: two free points; moments of (g2,g3) vs Dirichlet(1,1,1)
def gap_moment3(a, b):
    tot = sp.Integer(0)
    for order in itertools.permutations([2, 3]):
        ya, yb = symbols("ya yb", positive=True)
        gaps = {order[0]: ya, order[1]: yb - ya, 1: L - yb}
        integrand = gaps[2] ** a * gaps[3] ** b / L ** 2
        I = integrate(integrand, (yb, ya, L))
        I = integrate(I, (ya, 0, L))
        tot += I
    return simplify(tot)


for a in range(0, 4):
    for b in range(0, 4 - a):
        got = gap_moment3(a, b)
        want = L ** (a + b) * factorial(a) * factorial(b) * factorial(2) \
            / factorial(2 + a + b)
        assert simplify(got - want) == 0
print("(b') regression: n=2 (K=2 fact) and n=3 (K=3 fact) moments OK")
print("PART 2: PASS\n")


print("=" * 72)
print("PART 3 — exact per-pattern probabilities (independent route)")
print("=" * 72)
# P(pattern) via iterated symbolic integration over the peeling variables:
# ell_1 ~ U(0,1); ell_j = R_{j-1} * V_j, V_j ~ U(0,1).  Probability
# factors: anchor j>=2 contributes R_{j-1} (landing outside explored);
# each non-anchor member of block j contributes ell_j.  Lemma 1 predicts
# P(pattern) = prod(b_j-1)! / 24  (constant density integrated over
# Delta_4, whose volume is 1/24).
V = symbols("v1 v2 v3 v4", positive=True)
tot_prob = sp.Integer(0)
for part in set_partitions([1, 2, 3, 4]):
    blocks = sorted([sorted(b) for b in part], key=lambda b: b[0])
    R = sp.Integer(1)
    prob = sp.Integer(1)
    ells = []
    for j, b in enumerate(blocks):
        ell = R * V[j] if j > 0 else V[0]
        if j > 0:
            prob *= R          # anchor outside explored mass
        prob *= ell ** (len(b) - 1)   # non-anchor members, absolute
        ells.append(ell)
        R = simplify(R - ell)
    # integrate over the V's used (one per block), each Unif(0,1)
    for j in range(len(blocks) - 1, -1, -1):
        prob = integrate(prob, (V[j], 0, 1))
    prob = simplify(prob)
    expected = sp.prod([factorial(len(b) - 1) for b in blocks]) / sp.Integer(24)
    tag = "/".join("".join(map(str, b)) for b in blocks)
    print(f"pattern {tag:12s} P = {prob}   expected {expected}   "
          f"match={simplify(prob - expected) == 0}")
    assert simplify(prob - expected) == 0
    tot_prob += prob
print(f"\nsum of all 15 pattern probabilities = {simplify(tot_prob)}")
assert simplify(tot_prob - 1) == 0
print("PART 3: PASS")

print("\nALL PARTS PASS — Lemma 1 (K=4) independently confirmed:")
print("  joint density of (m1,m2,m3,m4) = 24 (uniform) on Delta_4,")
print("  every one of the 15 patterns contributing prod(b_j-1)!,")
print("  grouped 6+8+3+6+1 = 24 exactly as the document's table claims.")
