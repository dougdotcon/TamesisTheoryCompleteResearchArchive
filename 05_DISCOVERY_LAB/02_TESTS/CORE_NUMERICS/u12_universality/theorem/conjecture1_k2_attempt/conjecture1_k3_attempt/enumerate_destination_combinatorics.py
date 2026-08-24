"""
K=3 destination combinatorics: exhaustive classification of the 64 raw
(target_1,target_2,target_3) configurations (each u_i lands in region
1,2,3, or OUT) by the induced cycle structure of the redirect digraph
g: {1,2,3} -> {1,2,3,OUT}.

This is a pure combinatorics check (no probability/measure yet) verifying
by brute force -- not by hand -- the classification into 7 mutually
exclusive "shapes" used in derive_step2_k3_symbolic.py:
  T0  : no cycle among {1,2,3} (everything eventually drains to OUT)
  T1a : exactly one self-loop (3 sub-types by which node)
  T1b : exactly one 2-cycle, third node NOT self-looping (3 sub-types)
  T1c : one 3-cycle (2 sub-types: the two orientations)
  T2a : exactly two self-loops, third node not self-looping (3 sub-types)
  T2b : one self-loop + one 2-cycle on the other two nodes (3 sub-types)
  T3  : three self-loops (1 sub-type)
"""
import itertools

nodes = [1, 2, 3]
targets = [1, 2, 3, 'OUT']

def cycles_of(g):
    """Return list of cycles (as tuples in traversal order) among {1,2,3}
    under g, using exact functional-graph cycle detection (treat OUT as
    an absorbing non-node)."""
    found = []
    classified = set()
    for start in nodes:
        if start in classified:
            continue
        path = [start]
        cur = start
        seen_positions = {start: 0}
        while True:
            nxt = g[cur]
            if nxt == 'OUT':
                # whole path drains, no cycle among these
                classified.update(path)
                break
            if nxt in classified:
                # feeds into an already-discovered structure (cycle or
                # drain) from a previous start -- this path itself has
                # no NEW cycle among its own (as-yet-unclassified) nodes
                classified.update(path)
                break
            if nxt in seen_positions:
                cyc = tuple(path[seen_positions[nxt]:])
                found.append(cyc)
                classified.update(path)
                break
            path.append(nxt)
            seen_positions[nxt] = len(path) - 1
            cur = nxt
    return found

shape_counts = {}
shape_examples = {}
all_configs = list(itertools.product(targets, repeat=3))
assert len(all_configs) == 64

for cfg in all_configs:
    g = {1: cfg[0], 2: cfg[1], 3: cfg[2]}
    cycs = cycles_of(g)
    sizes = sorted(len(c) for c in cycs)
    if sizes == []:
        shape = 'T0'
    elif sizes == [1]:
        shape = 'T1a'
    elif sizes == [2]:
        shape = 'T1b'
    elif sizes == [3]:
        shape = 'T1c'
    elif sizes == [1, 1]:
        shape = 'T2a'
    elif sizes == [1, 2]:
        shape = 'T2b'
    elif sizes == [1, 1, 1]:
        shape = 'T3'
    else:
        shape = f'UNEXPECTED_{sizes}'
    shape_counts[shape] = shape_counts.get(shape, 0) + 1
    shape_examples.setdefault(shape, []).append((cfg, cycs))

print("Shape counts (raw configs out of 64):")
total = 0
for shape in ['T0', 'T1a', 'T1b', 'T1c', 'T2a', 'T2b', 'T3']:
    c = shape_counts.get(shape, 0)
    total += c
    print(f"  {shape}: {c}")
print(f"  TOTAL: {total}  (must be 64)")
assert total == 64
assert not any(k.startswith('UNEXPECTED') for k in shape_counts)
print("\nAll 64 raw configs classified into exactly these 7 shapes. No leftover cases.")

print("\nOne example config + its cycle decomposition, per shape:")
for shape in ['T0', 'T1a', 'T1b', 'T1c', 'T2a', 'T2b', 'T3']:
    cfg, cycs = shape_examples[shape][0]
    print(f"  {shape}: g={cfg} -> cycles {cycs}")

# Sanity: T1a should split evenly 3 ways (which node self-loops), etc.
print("\nSub-type breakdown (by which node(s) are on the cycle(s)):")
for shape in ['T1a', 'T1b', 'T2a', 'T2b']:
    sub = {}
    for cfg, cycs in shape_examples[shape]:
        key = tuple(sorted(tuple(sorted(c)) for c in cycs))
        sub[key] = sub.get(key, 0) + 1
    print(f"  {shape}: {sub}")
for shape in ['T1c']:
    sub = {}
    for cfg, cycs in shape_examples[shape]:
        key = cycs[0]
        sub[key] = sub.get(key, 0) + 1
    print(f"  {shape}: {sub}")
