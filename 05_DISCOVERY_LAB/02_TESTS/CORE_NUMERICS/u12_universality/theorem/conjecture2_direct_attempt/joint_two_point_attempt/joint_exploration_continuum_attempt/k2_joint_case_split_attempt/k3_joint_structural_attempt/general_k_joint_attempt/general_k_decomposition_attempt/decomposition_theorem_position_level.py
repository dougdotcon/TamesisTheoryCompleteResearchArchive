"""
Independent, from-scratch, POSITION-LEVEL verification of the general-K
Full Cycle-Count Decomposition Theorem (ATTEMPT.md Section 3):

    T = O + sum_{s in S} V_s,   (V_s)_{s in S} mutually independent given S,
    V_s ~ Uniform{1,...,L_s}.

This script does NOT assume Lemma 4 (Cycle-Predecessor Uniqueness) or any
of ATTEMPT.md's own formulas -- it builds a fresh, explicit "governing-
source reduced model" directly from the prose description of Definition 4
and the (cited, already-PROVED per Estagio 38) Governing-Source Reindexing
fact, then determines cyclicity by RAW forward simulation on the resulting
position-level functional graph, with NO reference to "who the cycle
predecessor is" -- that fact, if true, must emerge from the simulation, not
be assumed by it.

Reduced model, for a FIXED composition (L_0,...,L_{K-1}, O), n = O + sum L:
  - "OUT" is one absorbing node (the O outside points are collapsed to one
    representative for cycle-detection purposes -- legitimate since they
    are always mutually non-interacting and always individually cyclic;
    O itself is added back into T directly, exactly as Definition 4 implies).
  - ARC(t) has positions 1,...,L_t (position L_t = source t itself).
    position i (i < L_t) has deterministic successor i+1 within ARC(t)
    (unaffected by reroutes -- only the source's own image is redirected).
  - Source t's image (position L_t's successor) is U_t, which lands: in
    ARC(r) at a uniform position in {1,...,L_r} with probability L_r/n
    (r != t allowed AND r == t allowed -- landing back inside t's own arc,
    including on t itself, is a valid outcome), or hits "OUT" with
    probability O/n.
  - This exactly reproduces Definition 4's actual per-source target law
    (U_t uniform on all n slots, partitioned into the K+1 regions).

For each configuration, T := O + #{cyclic positions across all arcs} is
computed by DIRECT forward simulation from every position (no shortcut),
and separately S (cyclic sources) and, for s in S, V_s (# cyclic positions
in ARC(s)) are recorded. The full JOINT empirical law of (V_s)_{s in S},
conditional on S, is compared exactly (via Fraction arithmetic, summing
over the whole n^K raw target-choice space for the fixed L) against the
predicted product of independent Uniform{1,...,L_s} laws.

No code from any other front in this lineage was read or used.
"""
import itertools
from fractions import Fraction


def cyclic_positions(successor, nodes):
    """successor: dict node -> node (or 'OUT'). Returns set of cyclic nodes
    among `nodes`, by direct forward simulation (no shortcut)."""
    cyc = set()
    for start in nodes:
        seen = []
        cur = start
        while True:
            if cur == 'OUT':
                break
            if cur in seen:
                if cur == start:
                    cyc.add(start)
                break
            seen.append(cur)
            cur = successor[cur]
    return cyc


def enumerate_config(L, O, K):
    """L: tuple of arc lengths L_0..L_{K-1}. O: outside count.
    Enumerates exactly the n^K raw (region, position)-choices per source
    (equivalent to the true U_0,...,U_{K-1} in [n]) and for each builds the
    reduced functional graph, computes T, S, and per-s V_s."""
    n = O + sum(L)
    # arc nodes: (s, i) for s in 0..K-1, i in 1..L_s ; (s, L_s) is source s itself
    arc_nodes = {s: [(s, i) for i in range(1, L[s] + 1)] for s in range(K)}
    all_positions = []
    for s in range(K):
        all_positions.extend(arc_nodes[s])

    # each source's raw target choice: a "slot" in [0, n) -- slot space is
    # (region, position-within-region) with region in {0..K-1,'OUT'}, plus
    # a canonical bijection slot<->(region,pos) so raw enumeration over
    # n^K exactly matches enumerating U_0,...,U_{K-1} in [n]^K.
    slots = []
    for s in range(K):
        for i in range(1, L[s] + 1):
            slots.append((s, i))
    for _ in range(O):
        slots.append('OUT')
    assert len(slots) == n

    results = []  # list of (T, S(frozenset), {s: V_s for s in S})
    for target_choice in itertools.product(slots, repeat=K):
        # build successor map
        successor = {}
        for s in range(K):
            for i in range(1, L[s]):
                successor[(s, i)] = (s, i + 1)
            # source s's own successor (position (s, L_s)) is its target
            landing = target_choice[s]
            successor[(s, L[s])] = landing

        cyc = cyclic_positions(successor, all_positions)
        S = frozenset(s for s in range(K) if (s, L[s]) in cyc)
        Vs = {}
        for s in S:
            Vs[s] = sum(1 for i in range(1, L[s] + 1) if (s, i) in cyc)
        T = O + len(cyc)
        results.append((T, S, Vs))
    return results, n


def check_config(L, O, K, label=""):
    results, n = enumerate_config(L, O, K)
    total = len(results)
    all_ok = True

    # (1) bookkeeping identity: T == O + sum(Vs.values()) always
    for T, S, Vs in results:
        if T != O + sum(Vs.values()):
            all_ok = False
            print(f"    BOOKKEEPING FAIL: T={T} O={O} Vs={Vs}")

    # (2) conditional joint law of (V_s)_{s in S} given S: for each observed
    # S, compare empirical joint counts to the predicted product of
    # independent Uniform{1,...,L_s}
    by_S = {}
    for T, S, Vs in results:
        by_S.setdefault(S, []).append(Vs)

    for S, records in by_S.items():
        nS = len(records)
        # empirical joint pmf
        joint_counts = {}
        for Vs in records:
            key = tuple(sorted(Vs.items()))
            joint_counts[key] = joint_counts.get(key, 0) + 1
        # predicted: product of uniforms, each cell should have EQUAL count
        # (since independent uniforms over finite discrete sets give a
        # uniform joint distribution on the product space)
        expected_cells = 1
        for s in S:
            expected_cells *= L[s]
        expected_count_per_cell = Fraction(nS, expected_cells)
        ok = True
        if len(joint_counts) != expected_cells:
            ok = False
        else:
            for key, cnt in joint_counts.items():
                if Fraction(cnt) != expected_count_per_cell:
                    ok = False
                    break
        all_ok &= ok
        if not ok:
            print(f"    JOINT LAW FAIL for S={sorted(S)}: "
                  f"cells found={len(joint_counts)} expected={expected_cells}, "
                  f"counts={joint_counts}")

    print(f"{label} L={L} O={O} K={K} n={n}: {total} raw target-configs "
          f"({n}^{K}); {'ALL CHECKS PASS' if all_ok else 'FAILURES FOUND'} "
          f"(bookkeeping identity + joint independence/uniformity of "
          f"(V_s)_s given S, for every observed S)")
    return all_ok


def main():
    print("=" * 78)
    print("Position-level Decomposition Theorem check (fresh reduced model,")
    print("no reference to Lemma 4's stated conclusion -- cyclicity found by")
    print("direct forward simulation on an independently built graph)")
    print("=" * 78)
    all_ok = True
    configs = [
        ((2,), 1, 1),
        ((3,), 0, 1),
        ((2, 2), 1, 2),
        ((3, 2), 0, 2),
        ((2, 3), 1, 2),
        ((2, 2, 2), 0, 3),
        ((3, 2, 1), 1, 3),
        ((1, 1, 1), 2, 3),
        ((2, 2, 2, 1), 0, 4),
        ((1, 2, 1, 2), 1, 4),
        ((1, 1, 1, 1, 1), 0, 5),
    ]
    for L, O, K in configs:
        all_ok &= check_config(L, O, K)

    print()
    print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")


if __name__ == "__main__":
    main()
