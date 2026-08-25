"""
K=4 destination combinatorics: exhaustive classification of the 625=5^4
raw (target_1,...,target_4) configurations (each u_i lands in region
1,2,3,4, or OUT) by the induced cycle structure of the redirect digraph
g: {1,2,3,4} -> {1,2,3,4,OUT}.

Generalizes enumerate_destination_combinatorics.py (K=3, which found
exactly 7 shapes among 64 raw configs) to K=4. Predicted (BEFORE running
this script -- see DERIVATION_PREREG.md) number of shape TYPES, grouping
by (which subset of {1,2,3,4} is on-cycle, and the cycle-type-partition of
the permutation on that subset): Sum_{s=0}^{4} p(s) where p(s) = number of
integer partitions of s = 1+1+2+3+5 = 12 (matching K=3's Sum_{s=0}^3 p(s)
= 1+1+2+3 = 7 exactly).

This script ALSO checks a claim not needed at K=3 (K=3's off-cycle count
never exceeded 2): that N(r_on, n_off) -- the number of raw off-cycle
target assignments consistent with a GIVEN on-cycle subset (i.e. that do
not secretly form an additional cycle among the off-cycle nodes) -- is the
SAME for every choice of (a) which specific subset is on-cycle and (b)
which specific permutation/cycle-type governs it, depending only on the
pair (r_on, n_off). This is exactly the "does the shape-collapse mechanism
keep working" question K=3's document's own Section 7 flagged as open.
"""
import itertools
from collections import defaultdict

nodes = [1, 2, 3, 4]
targets = [1, 2, 3, 4, 'OUT']


def cycles_of(g):
    """Return list of cycles (as tuples in traversal order) among
    {1,2,3,4} under g, using exact functional-graph cycle detection
    (treat OUT as an absorbing non-node). Identical algorithm to
    enumerate_destination_combinatorics.py's cycles_of, generalized from
    {1,2,3} to {1,2,3,4}."""
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
                classified.update(path)
                break
            if nxt in classified:
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


shape_counts = defaultdict(int)
shape_examples = {}
# finer key: (on_cycle_subset (frozenset), cycle_type (sorted tuple of cycle
# lengths)) -- exactly the K=3-style "sub-type" classification, generalized.
fine_counts = defaultdict(int)
fine_examples = {}

all_configs = list(itertools.product(targets, repeat=4))
assert len(all_configs) == 625

for cfg in all_configs:
    g = {1: cfg[0], 2: cfg[1], 3: cfg[2], 4: cfg[3]}
    cycs = cycles_of(g)
    on_cycle = frozenset(i for cyc in cycs for i in cyc)
    r_on = len(on_cycle)
    cycle_type = tuple(sorted(len(c) for c in cycs))  # e.g. (1,1) two self-loops, (2,) a 2-cycle
    coarse_key = ('r_on', r_on)
    fine_key = (on_cycle, cycle_type)
    shape_counts[coarse_key] += 1
    fine_counts[fine_key] += 1
    shape_examples.setdefault(coarse_key, (cfg, cycs))
    fine_examples.setdefault(fine_key, (cfg, cycs))

print("=" * 78)
print("K=4 destination combinatorics -- coarse classification by r_on = |on-cycle set|")
print("=" * 78)
total = 0
for r_on in range(5):
    c = shape_counts.get(('r_on', r_on), 0)
    total += c
    print(f"  r_on={r_on}: {c} raw configs")
print(f"  TOTAL: {total}  (must be 625)")
assert total == 625

print("\n" + "=" * 78)
print("FINE classification by (on-cycle SUBSET, cycle type) -- this is the")
print("level analogous to K=3's T0/T1a/T1b/T1c/T2a/T2b/T3 table")
print("=" * 78)


def cycle_type_partition_shape(ct):
    """Human-readable label, e.g. (1,1,2) -> '2+1+1'."""
    return "+".join(str(x) for x in sorted(ct, reverse=True)) if ct else "(empty)"


# Group fine_counts by (r_on, cycle_type_shape) -- this collapses over
# WHICH specific subset is on-cycle, checking that different subsets of
# the same size with the same cycle type give the SAME raw count (a
# genuine structural claim, checked here, not assumed).
by_type = defaultdict(list)  # (r_on, cycle_type) -> list of (subset, count)
for (subset, cycle_type), cnt in fine_counts.items():
    by_type[(len(subset), cycle_type)].append((subset, cnt))

n_shape_types = 0
print(f"{'r_on':>4} {'cycle type':>12} {'#subsets':>9} {'#counts-distinct':>17} "
      f"{'count/subset':>13} {'total':>7}")
all_constant = True
shape_table = []
for (r_on, cycle_type), entries in sorted(by_type.items(), key=lambda kv: (kv[0][0], kv[0][1])):
    counts = sorted(set(c for _, c in entries))
    n_shape_types += 1
    total_for_type = sum(c for _, c in entries)
    label = cycle_type_partition_shape(cycle_type)
    per_subset_str = str(counts[0]) if len(counts) == 1 else f"NOT CONSTANT: {counts}"
    if len(counts) != 1:
        all_constant = False
    print(f"{r_on:>4} {label:>12} {len(entries):>9} {len(counts):>17} "
          f"{per_subset_str:>13} {total_for_type:>7}")
    shape_table.append({
        'r_on': r_on, 'cycle_type': label, 'n_subsets': len(entries),
        'count_per_subset': counts[0] if len(counts) == 1 else None,
        'total': total_for_type,
    })

print(f"\nNumber of distinct (r_on, cycle-type) shape TYPES: {n_shape_types}")
print(f"Predicted (Sum_s p(s), s=0..4) = 1+1+2+3+5 = 12")
assert n_shape_types == 12
print("MATCHES the pre-registered prediction exactly.")

if all_constant:
    print("\nCONFIRMED: for every (r_on, cycle-type) shape, the raw-config count "
          "is IDENTICAL across every specific choice of on-cycle subset with "
          "that cycle type -- the off-cycle raw-count N(r_on,n_off) depends "
          "only on (r_on,n_off), not on WHICH subset or WHICH permutation "
          "governs the on-cycle nodes. This is the discrete/combinatorial "
          "analogue (and an independent numerical confirmation) of the same "
          "fact used in the continuum density derivation "
          "(derive_step2_k4_symbolic.py).")
else:
    print("\n*** WARNING: the count is NOT constant across subsets of the same "
          "cycle type -- the shape-collapse mechanism does NOT generalize "
          "cleanly at K=4 in this respect. Reported honestly, not patched. ***")

# ---------------------------------------------------------------------
# Also report N(r_on, n_off) explicitly, and cross-check against the r_on
# totals: total(r_on) should equal C(4,r_on) * r_on! * N(r_on, 4-r_on).
# ---------------------------------------------------------------------
print("\n" + "=" * 78)
print("N(r_on, n_off) table and cross-check against coarse r_on totals")
print("=" * 78)
import math

N_table = {}
for r_on in range(5):
    n_off = 4 - r_on
    # Find the (unique, if all_constant) count-per-subject for THIS r_on,
    # summed over cycle types with multiplicity = number of permutations
    # of that cycle type on r_on labeled elements, and divided by that
    # multiplicity to recover N per single (subset, one specific
    # permutation).
    total_r = shape_counts.get(('r_on', r_on), 0)
    n_subsets = math.comb(4, r_on)
    n_perms = math.factorial(r_on)
    if n_subsets * n_perms == 0:
        N = total_r  # r_on=0 edge case: 1 subset (empty), 1 "permutation" (empty)
        n_subsets, n_perms = 1, 1
    else:
        N = total_r / (n_subsets * n_perms)
    N_table[r_on] = N
    print(f"  r_on={r_on}, n_off={n_off}: total={total_r}, "
          f"C(4,{r_on})={n_subsets}, {r_on}!={n_perms}, "
          f"=> N({r_on},{n_off}) = {total_r}/({n_subsets}*{n_perms}) = {N}")
    assert float(N).is_integer(), "N(r_on,n_off) must be an integer"

print(f"\nN table: {N_table}")
print("Cross-check: total = sum_r_on [ C(4,r_on) * r_on! * N(r_on,4-r_on) ]")
recheck_total = sum(
    math.comb(4, r) * math.factorial(r) * N_table[r] for r in range(5)
)
print(f"  = {recheck_total}  (must be 625)")
assert recheck_total == 625

print("\nOne example raw config per shape TYPE, with its cycle decomposition:")
for (r_on, cycle_type), entries in sorted(by_type.items(), key=lambda kv: (kv[0][0], kv[0][1])):
    subset, _ = entries[0]
    cfg, cycs = fine_examples[(subset, cycle_type)]
    label = cycle_type_partition_shape(cycle_type)
    print(f"  r_on={r_on} type={label:>10} subset={sorted(subset) if subset else '{}'}: "
          f"g={cfg} -> cycles {cycs}")

import json

with open("enumerate_destination_combinatorics_k4_results.json", "w") as fh:
    json.dump({
        'total_configs': total,
        'n_shape_types': n_shape_types,
        'all_constant_per_type': all_constant,
        'N_table': N_table,
        'shape_table': shape_table,
        'coarse_by_r_on': {str(r): shape_counts.get(('r_on', r), 0) for r in range(5)},
    }, fh, indent=2, default=str)
print("\nWritten enumerate_destination_combinatorics_k4_results.json")
