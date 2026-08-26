"""
Independent, from-scratch, POSITION-LEVEL cross-check of Lemma 4
(Cycle-Predecessor Uniqueness), including its second (harder) claim:
that ARC(s)'s cyclic point-set is exactly {k,...,L_s}, where k is the
landing position of U_{pred(s)} within ARC(s), and that this is
INDEPENDENT of any other (non-cycle-forming) incoming edge into ARC(s).

Method: build the full 3-arc functional graph explicitly at the level of
concrete positions (no shortcut, no reuse of the cycle-predecessor idea
in the *construction* -- only in the *prediction* we're testing against),
determine cyclicity of every position by direct forward-graph traversal,
and compare against Lemma 4's closed-form prediction.

Exhaustive over all arc-length triples L0,L1,L2 in {1,2,3,4}, all 64
destination assignments dest: {0,1,2}->{0,1,2,DEAD}, and all valid
landing positions for each non-DEAD source.

No .py file from any front in the lineage was read.
"""
import itertools

NODES = (0, 1, 2)
DEAD = 'DEAD'
DESTS = NODES + (DEAD,)


def source_cyclic_set(dest):
    """Cyclic nodes of the reduced 3-node functional graph (same def as
    adv_lemma4_cycle_predecessor.py, re-derived independently here)."""
    cset = set()
    for s in NODES:
        cur = dest[s]
        seen = {s}
        is_cyc = False
        while True:
            if cur == DEAD:
                break
            if cur == s:
                is_cyc = True
                break
            if cur in seen:
                break
            seen.add(cur)
            cur = dest[cur]
        if is_cyc:
            cset.add(s)
    return cset


def pred_of(dest, s, cset):
    cands = [t for t in NODES if dest[t] == s and t in cset]
    assert len(cands) == 1, (dest, s, cset, cands)
    return cands[0]


def simulate_positions(L, dest, pos):
    """L: dict s->L_s. dest: dict s->target or DEAD. pos: dict s->landing
    position within dest[s]'s arc (only meaningful if dest[s]!=DEAD).
    Returns dict (s,i)->bool cyclic for i in 1..L[s]."""
    def f(node):
        s, i = node
        if i < L[s]:
            return (s, i + 1)
        # i == L[s]: this IS the source s itself (the tail)
        if dest[s] == DEAD:
            return None
        return (dest[s], pos[s])

    cyclic = {}
    for s in NODES:
        for i in range(1, L[s] + 1):
            node = (s, i)
            cur = f(node)
            seen = {node}
            is_cyc = False
            steps = 0
            while cur is not None:
                if cur == node:
                    is_cyc = True
                    break
                if cur in seen:
                    is_cyc = False
                    break
                seen.add(cur)
                cur = f(cur)
                steps += 1
                if steps > 1000:
                    raise RuntimeError("unexpected non-termination")
            cyclic[node] = is_cyc
    return cyclic


def predicted_cyclic_set_for_arc(L, dest, pos, s, cset):
    """Lemma 4's closed-form prediction for ARC(s)'s cyclic positions."""
    if s not in cset:
        return set()
    t = pred_of(dest, s, cset)
    k = pos[t]  # position where U_t landed within ARC(s) = dest[t]'s arc
    return set(range(k, L[s] + 1))


def run(max_L=4):
    total_configs = 0
    mismatches = []
    extra_incoming_configs_checked = 0

    L_values = range(1, max_L + 1)
    for L0, L1, L2 in itertools.product(L_values, repeat=3):
        L = {0: L0, 1: L1, 2: L2}
        for dest_tuple in itertools.product(DESTS, repeat=3):
            dest = {i: dest_tuple[i] for i in NODES}
            cset = source_cyclic_set(dest)

            # enumerate all valid position choices for sources with dest != DEAD
            pos_domains = []
            active_sources = [s for s in NODES if dest[s] != DEAD]
            for s in active_sources:
                pos_domains.append(range(1, L[dest[s]] + 1))

            if active_sources:
                pos_choices_iter = itertools.product(*pos_domains)
            else:
                pos_choices_iter = [()]

            for pos_choice in pos_choices_iter:
                pos = dict(zip(active_sources, pos_choice))
                total_configs += 1

                sim_cyclic = simulate_positions(L, dest, pos)

                for s in NODES:
                    predicted = predicted_cyclic_set_for_arc(L, dest, pos, s, cset)
                    actual = {i for i in range(1, L[s] + 1) if sim_cyclic[(s, i)]}
                    if predicted != actual:
                        mismatches.append({
                            'L': dict(L), 'dest': dict(dest), 'pos': dict(pos),
                            's': s, 'predicted': sorted(predicted),
                            'actual': sorted(actual), 'cset': sorted(cset),
                        })

                # track whether this config has a genuine "extra inert incoming edge"
                for s in cset:
                    preds_all = [t for t in NODES if dest[t] == s]
                    if len(preds_all) >= 2:
                        extra_incoming_configs_checked += 1

    return total_configs, mismatches, extra_incoming_configs_checked


if __name__ == '__main__':
    total_configs, mismatches, extra_count = run(max_L=4)
    print(f"Total (L, dest, pos) configurations checked: {total_configs}")
    print(f"Configs with a genuine extra (non-pred) incoming edge into a "
          f"cyclic arc: {extra_count}")
    print(f"Mismatches between Lemma 4's prediction and direct simulation: "
          f"{len(mismatches)}")
    for m in mismatches[:20]:
        print("  MISMATCH:", m)
    print()
    print(f"LEMMA4_POSITION_LEVEL_OK: {len(mismatches) == 0}")
