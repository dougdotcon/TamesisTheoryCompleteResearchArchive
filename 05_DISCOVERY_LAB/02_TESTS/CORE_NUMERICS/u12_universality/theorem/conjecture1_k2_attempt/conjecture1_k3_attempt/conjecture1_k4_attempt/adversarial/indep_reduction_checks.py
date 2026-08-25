# Adversarial referee — reduction checks: the general K-parametrized
# method of the K=4 document, applied at K=3 and K=2, must reproduce the
# already-adversarially-reviewed K=3 and K=2 group-level densities.
#
# Everything below is MY OWN implementation of the general method
# (independent classification + my own re-derived per-r formula), with
# the "established" reference polynomials built as direct sympy
# expressions from the K=3 ATTEMPT.md Section 4 table and the K=4
# document's own Section 5 (r-grouped) table — NEVER via
# sympify-of-strings (the exact pitfall the document's Section 5 bug
# note describes: sympify parses a FRESH Symbol('x') without the
# positive=True assumption, producing a same-printing but distinct
# symbol; we also demonstrate that pitfall explicitly at the end, to
# confirm the document's diagnosis of its own bug is accurate).
#
# Exact arithmetic throughout.

import itertools
from collections import defaultdict
import sympy as sp
from sympy import Rational, factorial, binomial, symbols, integrate, \
    simplify, expand

x = symbols("x", positive=True)
Q = symbols("Q", positive=True)


def cycle_nodes(g, K):
    OUT = K
    on = set()
    for i in range(K):
        cur = i
        for _ in range(K):
            t = g[cur]
            if t == OUT:
                break
            cur = t
            if cur == i:
                on.add(i)
                break
    return frozenset(on)


def general_fr(K, r):
    """My own re-derived per-r density formula, general K:
    f_r(x) = C(K,r) * K! * x^r * Int_0^{1-x} (1-Q) Q^(noff-1)/(noff-1)!
             * (1-x-Q)^(r-1)/(r-1)! dQ,  noff=K-r;  boundary cases:
    r=K: C(K,K)*K!*x^K*(1-x)^(K-1)/(K-1)!;  r=0: x * density of OUT
    (OUT ~ Beta(1,K) under uniform-K! on Delta_K: density K(1-x)^(K-1))."""
    noff = K - r
    if r == 0:
        return expand(K * (1 - x) ** (K - 1) * x)
    if noff == 0:
        return expand(factorial(K) * x ** K * (1 - x) ** (K - 1)
                      / factorial(K - 1))
    integrand = (1 - Q) * Q ** (noff - 1) / factorial(noff - 1) \
        * (1 - x - Q) ** (r - 1) / factorial(r - 1)
    I = integrate(integrand, (Q, 0, 1 - x))
    return expand(binomial(K, r) * factorial(K) * x ** r * I)


print("=" * 72)
print("K=3 reduction — my general method vs the established K=3 groups")
print("=" * 72)
# established group-level densities, built as direct sympy expressions
# from conjecture1_k3_attempt/ATTEMPT.md Section 4's per-shape table,
# summed into r_on groups:
#   r=0: T0 = 3x^3-6x^2+3x
#   r=1: T1a = 3x(x-1)^2(2x+1)
#   r=2: T1b + T2a = 2 * (3/2)x^2(x-1)^2(x+2)
#   r=3: T1c + T2b + T3 = x^3(x-1)^2 * (1 + 3/2 + 1/2)
established_k3 = {
    0: expand(3 * x**3 - 6 * x**2 + 3 * x),
    1: expand(3 * x * (x - 1) ** 2 * (2 * x + 1)),
    2: expand(2 * Rational(3, 2) * x**2 * (x - 1) ** 2 * (x + 2)),
    3: expand((1 + Rational(3, 2) + Rational(1, 2)) * x**3 * (x - 1) ** 2),
}
# the K=4 document's own Section 5 comparison table values (transcribed):
k4doc_k3 = {
    0: expand(3 * x**3 - 6 * x**2 + 3 * x),
    1: expand(6 * x**4 - 9 * x**3 + 3 * x),
    2: expand(3 * x**5 - 9 * x**3 + 6 * x**2),
    3: expand(3 * x**5 - 6 * x**4 + 3 * x**3),
}
tot = sp.Integer(0)
for r in range(4):
    mine = general_fr(3, r)
    ok1 = simplify(mine - established_k3[r]) == 0
    ok2 = simplify(mine - k4doc_k3[r]) == 0
    print(f"r={r}: my general method = {mine}")
    print(f"      established K=3   = {established_k3[r]}  MATCH={ok1}")
    print(f"      K=4 doc Sec.5 row = {k4doc_k3[r]}  MATCH={ok2}")
    assert ok1 and ok2
    tot += mine
assert simplify(tot - 6 * x * (1 - x**2) ** 2) == 0
print(f"sum = {expand(tot)} = 6x(1-x^2)^2  MATCH")

# cross-check my classification collapses correctly at K=3 (64 configs,
# 7 shapes) and per-r raw counts:
by_r = defaultdict(int)
shapes = set()
for g in itertools.product(range(4), repeat=3):
    on = cycle_nodes(g, 3)
    r = len(on)
    by_r[r] += 1
    # cycle type
    ct = []
    seen = set()
    for i in sorted(on):
        if i in seen:
            continue
        cyc = [i]
        cur = g[i]
        while cur != i:
            cyc.append(cur)
            cur = g[cur]
        seen.update(cyc)
        ct.append(len(cyc))
    shapes.add((r, tuple(sorted(ct, reverse=True))))
print(f"K=3 raw per-r counts: {dict(sorted(by_r.items()))} "
      f"(K=3 doc: T0=16; r=1:24; r=2: 9+9=18; r=3: 2+3+1=6)")
assert dict(by_r) == {0: 16, 1: 24, 2: 18, 3: 6}
assert len(shapes) == 7
print(f"7 shape types at K=3 confirmed: {sorted(shapes)}")

print()
print("=" * 72)
print("K=2 reduction — my general method vs the established K=2 groups")
print("=" * 72)
established_k2 = {          # from conjecture1_k3_attempt/ATTEMPT.md Sec.5
    0: expand(2 * x * (1 - x)),                 # T0
    1: expand(2 * x * (1 - x**2)),              # single self, other off
    2: expand(x**2 * (1 - x) + x**2 * (1 - x)),  # both-self + 2-cycle
}
tot2 = sp.Integer(0)
for r in range(3):
    mine = general_fr(2, r)
    ok = simplify(mine - established_k2[r]) == 0
    print(f"r={r}: my general method = {mine}   established = "
          f"{established_k2[r]}   MATCH={ok}")
    assert ok
    tot2 += mine
assert simplify(tot2 - 4 * x * (1 - x**2)) == 0
print(f"sum = {expand(tot2)} = 4x(1-x^2)  MATCH")

print()
print("=" * 72)
print("K=5 spot extension (NOT claimed by the document; referee probe)")
print("=" * 72)
# The forest identity W=1-Q was verified by my own enumeration for
# n_off<=4. For K=5 the formula would need n_off=4 at r=1 — which my
# Part B enumeration DID cover.  As a probe (not part of the verdict):
tot5 = sum(general_fr(5, r) for r in range(6))
print(f"sum over r=0..5 of my general formula at K=5: {expand(tot5)}")
print(f"10x(1-x^2)^4 = {expand(10 * x * (1 - x**2) ** 4)}")
print(f"equal: {simplify(tot5 - 10 * x * (1 - x**2) ** 4) == 0}")
print("(consistent with Conjecture 1 at K=5 — contingent on W=1-Q at "
      "n_off=4, verified, and Lemma 1 at K=5, NOT verified here; "
      "recorded as a probe only, no claim.)")

print()
print("=" * 72)
print("sympify fresh-symbol pitfall — confirming the document's Sec.5 bug")
print("=" * 72)
expr_direct = 3 * x**3 - 6 * x**2 + 3 * x
expr_sympify = sp.sympify("3*x**3 - 6*x**2 + 3*x")
diff = sp.simplify(expr_direct - expr_sympify)
xs = list(expr_sympify.free_symbols)[0]
print(f"x (positive=True) is xs (no assumptions)?  {x is xs}   "
      f"x == xs? {x == xs}")
print(f"simplify(direct - sympified) = {diff}  (nonzero iff the pitfall "
      f"is real)")
print(f"srepr distinct: {sp.srepr(x)}  vs  {sp.srepr(xs)}")
assert (diff == 0) == (x == xs)
if diff != 0:
    print("CONFIRMED: sympify('...') creates a distinct Symbol('x') "
          "without the positive=True assumption; the difference does "
          "not cancel — exactly the false-MISMATCH failure mode the "
          "document reports having caught and fixed.  (My comparisons "
          "above never use sympify-of-strings.)")
print("\nALL REDUCTION CHECKS PASS")
