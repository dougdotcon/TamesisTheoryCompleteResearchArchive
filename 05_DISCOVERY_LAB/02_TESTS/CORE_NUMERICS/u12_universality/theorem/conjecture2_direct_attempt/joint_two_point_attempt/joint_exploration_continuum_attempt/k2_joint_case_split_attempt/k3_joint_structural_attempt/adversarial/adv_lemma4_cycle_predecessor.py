"""
Independent, from-scratch verification of Lemma 4 (Cycle-Predecessor
Uniqueness) as stated in ATTEMPT.md section 3.2.

Claim: fix dest: {0,1,2} -> {0,1,2,DEAD}. Say s is "cyclic" iff iterating
dest from s returns to s before hitting DEAD. Then: if s is cyclic, there
is a UNIQUE t in {0,1,2} with dest(t)=s AND t itself cyclic.

This is a pure functional-graph fact about the 4^3=64 possible functions
dest. Verified here by direct, exhaustive enumeration of all 64 functions.

No .py file from any front in the lineage was read; this is written fresh
from the mathematical statement in ATTEMPT.md.
"""
import itertools

NODES = (0, 1, 2)
DEAD = 'DEAD'
DESTS = NODES + (DEAD,)


def is_cyclic(dest, s):
    """s is cyclic iff iterating dest from s returns to s without ever
    hitting DEAD first."""
    cur = dest[s]
    seen = {s}
    while True:
        if cur == DEAD:
            return False
        if cur == s:
            return True
        if cur in seen:
            # would only happen if we hit a DIFFERENT cycle not containing s
            # (shouldn't happen for functional graphs starting at s and not
            # yet having returned to s) -- but guard anyway.
            return False
        seen.add(cur)
        cur = dest[cur]


def cyclic_set(dest):
    return {s for s in NODES if is_cyclic(dest, s)}


def predecessors_in(dest, s, restrict_to):
    """All t in restrict_to with dest[t] == s."""
    return [t for t in restrict_to if dest[t] == s]


def run():
    all_dest_functions = list(itertools.product(DESTS, repeat=3))
    assert len(all_dest_functions) == 64

    total_checked = 0
    total_cyclic_node_instances = 0
    failures = []

    detail_rows = []

    for dest_tuple in all_dest_functions:
        dest = {i: dest_tuple[i] for i in NODES}
        total_checked += 1
        cset = cyclic_set(dest)
        for s in cset:
            total_cyclic_node_instances += 1
            # candidates: t in {0,1,2} with dest[t]==s AND t cyclic
            preds_all = predecessors_in(dest, s, NODES)  # all incoming edges (regardless of cyclic)
            preds_cyclic = [t for t in preds_all if t in cset]
            row = {
                'dest': dest_tuple, 's': s, 'cyclic_set': sorted(cset),
                'all_incoming': preds_all, 'cyclic_incoming': preds_cyclic,
            }
            detail_rows.append(row)
            if len(preds_cyclic) != 1:
                failures.append(row)

    return total_checked, total_cyclic_node_instances, failures, detail_rows


if __name__ == '__main__':
    total_checked, total_cyclic_instances, failures, detail_rows = run()
    print(f"Total dest functions checked: {total_checked} (expect 64)")
    print(f"Total (dest, cyclic s) instances checked: {total_cyclic_instances}")
    print(f"Failures (uniqueness violated): {len(failures)}")
    for f in failures[:20]:
        print("  FAIL:", f)

    # Also verify: a non-cyclic-forming incoming edge into ARC(s) (t' != pred(s),
    # dest[t']==s, t' NOT cyclic) can indeed coexist -- i.e. the "extra in-degree"
    # scenario Lemma 4 discusses really does occur among the 64 cases (sanity
    # that the lemma isn't vacuous).
    extra_indegree_cases = 0
    for dest_tuple in itertools.product(DESTS, repeat=3):
        dest = {i: dest_tuple[i] for i in NODES}
        cset = cyclic_set(dest)
        for s in cset:
            preds_all = predecessors_in(dest, s, NODES)
            preds_noncyclic = [t for t in preds_all if t not in cset and t != s]
            # also could have dest[t]==s with t==s excluded trivially since s in cset means dest chain from s eventually = s;
            if len(preds_noncyclic) >= 1:
                extra_indegree_cases += 1

    print(f"\nNumber of (dest, cyclic s) instances with an EXTRA non-cyclic "
          f"incoming edge into ARC(s) (the 'inert extra source' scenario "
          f"Lemma 4 discusses): {extra_indegree_cases}")

    ok = (len(failures) == 0) and (total_checked == 64)
    print(f"\nLEMMA4_UNIQUENESS_OK: {ok}")
