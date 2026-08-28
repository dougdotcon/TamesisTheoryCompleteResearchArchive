#!/usr/bin/env python3
"""
INDEPENDENT re-derivation of "Proposicao S (K=2)" from the raw 9-case
destination table, from scratch, using sympy. No .py file from any front
in this lineage was read to write this script -- only the mathematical
description in ATTEMPT.md Sec 2.1 (dest(0), dest(1) i.i.d. categorical on
{0, 1, DEAD} with weights (p0, p1, pD); source s is cyclic iff iterating
dest from s returns to s before DEAD).

We build the 3x3 table of (dest(0), dest(1)) outcomes completely from
first principles (functional graph on 2 labelled nodes {0,1} plus a DEAD
sink) and re-derive which subset S of {0,1} ends up "cyclic" for each of
the 9 cases, by literally tracing the 2-node functional graph -- not by
copying ATTEMPT.md's own trace table.
"""
import sympy as sp

p0, p1, pD = sp.symbols('p0 p1 pD', positive=True)


def cyclic_subset(dest0, dest1):
    """dest0, dest1 in {0, 1, 'D'}. Returns frozenset of {0,1} that are
    cyclic under the map d: 0->dest0, 1->dest1 (D is an absorbing sink,
    never cyclic, and never has an out-edge back into {0,1})."""
    d = {0: dest0, 1: dest1}

    def is_cyclic(start):
        node = start
        seen = set()
        while True:
            if node == 'D':
                return False
            if node in seen:
                # we looped back without hitting 'D' -- but the only way
                # to loop within {0,1} without revisiting start first is
                # to hit start again (2-node graph), so this branch means
                # we returned to 'start' eventually.
                return node == start or start in seen
            seen.add(node)
            if node == start and len(seen) > 1:
                return True
            node = d[node]

    # Simpler, fully explicit approach for a 2-node graph: enumerate the
    # forward orbit up to length 3 (more than enough since |{0,1,D}|=3)
    # and check whether 'start' reappears before 'D' does.
    def cyclic_explicit(start):
        node = start
        for _ in range(3):
            node = d[node]
            if node == start:
                return True
            if node == 'D':
                return False
        return False

    S = set()
    for s in (0, 1):
        if cyclic_explicit(s):
            S.add(s)
    return frozenset(S)


weights = {0: p0, 1: p1, 'D': pD}

# All 9 raw (dest0, dest1) combinations.
cases = []
for dest0 in (0, 1, 'D'):
    for dest1 in (0, 1, 'D'):
        w = weights[dest0] * weights[dest1]
        S = cyclic_subset(dest0, dest1)
        cases.append((dest0, dest1, S, w))

print("Raw 9-case trace (dest(0), dest(1)) -> S:")
for dest0, dest1, S, w in cases:
    print(f"  dest(0)={dest0}, dest(1)={dest1}  ->  S={sorted(S) if S else '{}'}"
          f"   weight={w}")

# Aggregate by S.
targets = {
    frozenset(): sp.simplify(pD),
    frozenset({0}): sp.expand(p0 * (p0 + pD)),
    frozenset({1}): sp.expand(p1 * (p1 + pD)),
    frozenset({0, 1}): sp.expand(2 * p0 * p1),
}

print()
print("Aggregated P(S=A), raw sum vs claimed closed form (ATTEMPT.md Sec 2.1):")
all_ok = True
total = 0
for S_key, claim in targets.items():
    raw_sum = sum(w for (d0, d1, S, w) in cases if S == S_key)
    raw_sum_sub = sp.expand(raw_sum.subs(pD, 1 - p0 - p1))
    claim_sub = sp.expand(claim.subs(pD, 1 - p0 - p1))
    diff = sp.simplify(raw_sum_sub - claim_sub)
    label = sorted(S_key) if S_key else '{}'
    ok = (diff == 0)
    all_ok &= ok
    total += raw_sum
    print(f"  S={label}: raw_sum={sp.factor(raw_sum)}  claimed={claim}  "
          f"diff(after pD=1-p0-p1)={diff}  {'OK' if ok else 'MISMATCH'}")

total_sub = sp.expand(total.subs(pD, 1 - p0 - p1))
print(f"\n  sum of all 4 P(S=.) (raw) = {sp.simplify(total)}  "
      f"(should be (p0+p1+pD)^2 = 1 on the simplex): "
      f"after pD=1-p0-p1 -> {sp.simplify(total_sub)}")

print()
print("VERDICT:", "Proposicao S (K=2) INDEPENDENTLY CONFIRMED, 0 discrepancies"
      if all_ok else "MISMATCH FOUND -- Proposicao S REFUTED")
