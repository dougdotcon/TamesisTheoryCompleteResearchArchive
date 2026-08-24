"""
INDEPENDENT re-derivation of the K=3 destination-combinatorics shapes.
Fresh cycle-detection + classification code (not reading enumerate_
destination_combinatorics.py). Computes:
  (1) P(shape | m1,m2,m3) exact polynomial, for all 7 shapes, via my own
      classification of all 64 raw g:{1,2,3}->{1,2,3,'OUT'} maps.
  (2) target-level probability = integral over simplex (weight 6).
  (3) compares against ATTEMPT.md's claimed values:
      T1a=9/20, T1b=1/8, T1c=1/60, T2a=1/8, T2b=1/40, T3=1/120, T0=1/4.
"""
import sympy as sp
from itertools import product

m1, m2, m3 = sp.symbols('m1 m2 m3', positive=True)
M = {1: m1, 2: m2, 3: m3}
m0 = 1 - m1 - m2 - m3  # OUT mass

NODES = [1, 2, 3]

def cycle_nodes(g):
    """g: dict i -> target in {1,2,3,'OUT'}. Return set of nodes on a genuine cycle."""
    on_cycle = set()
    for start in NODES:
        seen = []
        cur = start
        for _ in range(4):
            if cur == 'OUT':
                break
            if cur in seen:
                # found a cycle; check if 'start' is part of it
                idx = seen.index(cur)
                cyc = seen[idx:]
                if start in cyc:
                    on_cycle.add(start)
                break
            seen.append(cur)
            cur = g[cur]
    return on_cycle

def classify(g):
    """Return a canonical shape signature: frozenset of cycles (each cycle
    itself a tuple of nodes in cyclic order isn't needed, just the sets)."""
    oc = cycle_nodes(g)
    if len(oc) == 0:
        return ('T0',)
    # find actual cycles among on-cycle nodes
    cycles = []
    visited = set()
    for i in oc:
        if i in visited:
            continue
        cyc = [i]
        cur = g[i]
        while cur != i:
            cyc.append(cur)
            cur = g[cur]
        visited.update(cyc)
        cycles.append(frozenset(cyc))
    cycles = frozenset(cycles)
    sizes = sorted(len(c) for c in cycles)
    if sizes == [1]:
        return ('T1a',)
    if sizes == [2]:
        return ('T1b',)
    if sizes == [3]:
        return ('T1c',)
    if sizes == [1, 1]:
        return ('T2a',)
    if sizes == [1, 2]:
        return ('T2b',)
    if sizes == [1, 1, 1]:
        return ('T3',)
    raise ValueError(f"unexpected cycles {cycles}")

# Enumerate all 64 raw configs, classify, and build P(shape|m) polynomial.
targets = [1, 2, 3, 'OUT']
shape_prob = {}
shape_count = {}
all_configs_by_shape = {}
total_prob_check = 0
for combo in product(targets, repeat=3):
    g = {1: combo[0], 2: combo[1], 3: combo[2]}
    shape = classify(g)[0]
    prob_this_config = 1
    for i in NODES:
        t = g[i]
        prob_this_config *= (M[t] if t != 'OUT' else m0)
    shape_prob[shape] = shape_prob.get(shape, 0) + prob_this_config
    shape_count[shape] = shape_count.get(shape, 0) + 1
    all_configs_by_shape.setdefault(shape, []).append(g)
    total_prob_check += prob_this_config

print("Raw config counts per shape (independent classification):")
for k in ['T0', 'T1a', 'T1b', 'T1c', 'T2a', 'T2b', 'T3']:
    print(f"  {k}: {shape_count.get(k,0)}")
print("  TOTAL:", sum(shape_count.values()), "(should be 64)")
assert sum(shape_count.values()) == 64

# sanity: total probability (summed poly over all shapes) should be
# (m1+m2+m3+m0)^3 = 1 identically
total_poly = sp.expand(sum(shape_prob.values()))
print("\nSum of all P(shape|m) polys, should simplify to 1:", sp.simplify(total_poly - 1))
assert sp.simplify(total_poly - 1) == 0

print("\nMatching document's raw-config counts (16,24,9,2,9,3,1):")
expected_counts = {'T0':16,'T1a':24,'T1b':9,'T1c':2,'T2a':9,'T2b':3,'T3':1}
for k,v in expected_counts.items():
    assert shape_count[k] == v, f"MISMATCH at {k}: got {shape_count[k]}, expected {v}"
print("PASS: raw counts match exactly (independent re-confirmation).")

# Now integrate each P(shape|m) over the simplex with weight 6 -> target prob
def simplex_integral(expr):
    e = sp.integrate(expr, (m3, 0, 1 - m1 - m2))
    e = sp.integrate(e, (m2, 0, 1 - m1))
    e = sp.integrate(e, (m1, 0, 1))
    return sp.nsimplify(sp.simplify(e))

print("\nTarget-level probabilities (integral of 6*P(shape|m) over simplex):")
computed_target_probs = {}
for k in ['T0', 'T1a', 'T1b', 'T1c', 'T2a', 'T2b', 'T3']:
    poly = sp.expand(shape_prob[k])
    val = simplex_integral(6 * poly)
    computed_target_probs[k] = val
    print(f"  P_{k} = {val}")

expected = {'T1a': sp.Rational(9,20), 'T1b': sp.Rational(1,8), 'T1c': sp.Rational(1,60),
            'T2a': sp.Rational(1,8), 'T2b': sp.Rational(1,40), 'T3': sp.Rational(1,120),
            'T0': sp.Rational(1,4)}
print("\nComparing to document's claimed values:")
all_match = True
for k, v in expected.items():
    ok = (computed_target_probs[k] == v)
    all_match &= ok
    print(f"  {k}: computed={computed_target_probs[k]}  document={v}  MATCH={ok}")

total = sum(computed_target_probs.values())
print("\nSum of all 7 target probabilities:", total, "(should be 1)")
assert total == 1
print("\nALL MATCH:" , all_match)
