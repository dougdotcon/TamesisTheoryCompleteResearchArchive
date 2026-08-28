#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check #4: the Full Cycle-Count Decomposition
Theorem, general K -- position-level reduced model, built directly from
prose (ATTEMPT.md Section 1.2/3.1 + THEOREM.md's Definitions), with NO
reference anywhere in this construction to "who the cycle predecessor is"
or to Lemma 4's conclusion. Cyclicity, S, and each V_s are all read off
purely from DIRECT FORWARD SIMULATION of the resulting position-level
functional graph. This is exactly the adversarial spirit the task asked
for: if pred(s) uniqueness / distinctness and the resulting independence
of (V_s)_{s in S} are true, they must EMERGE from raw simulation, not be
assumed.

Reduced model (position-level, exactly as ATTEMPT.md Section 1.2
describes the arcs): fix concrete arc lengths L_0,...,L_{K-1} and an
outside count O (all positive integers). The position space is:
  - O "outside" points, each with deterministic self-loop (always cyclic,
    trivially, and irrelevant to what we're testing) -- we track T's O
    contribution separately and do not need to simulate these explicitly.
  - For each source s in {0,...,K-1}: ARC(s) has positions 1,...,L_s,
    with position L_s being the source itself. Deterministic successor
    within the arc: position i -> i+1 for i=1,...,L_s-1. The SOURCE's own
    successor (position L_s's successor) is NOT deterministic -- it is
    determined by U_s, a target chosen uniformly at random among all n
    positions (n = O + sum L_t): with probability O/n it goes to a fixed
    "OUTSIDE/DEAD" absorbing point (never returns), and with probability
    L_t/n for each t, it lands UNIFORMLY on one of the L_t positions of
    ARC(t) (position j in {1,...,L_t} each with probability 1/n).

We enumerate ALL n^K raw joint target choices (each U_s ranges over the n
raw positions: O "dead" choices bundled as one outcome-class, plus
sum_t L_t individual named positions) EXACTLY, build the resulting
position-level functional graph, and determine cyclicity by DIRECT
FORWARD SIMULATION from every position (no shortcut).

From this raw simulation we read off, per configuration:
  - S: the sources s such that the SOURCE POSITION L_s of ARC(s) is
    cyclic (equivalently, the source itself lies on a cycle)
  - for s in S: V_s := number of cyclic positions within ARC(s)
  - T := O + sum_{s in S} V_s (checked against a DIRECT independent count
    of ALL cyclic positions across the whole graph, including the O
    outside points which are trivially always cyclic)

Checks:
  (i) bookkeeping identity T = O + sum_{s in S} V_s holds in every single
      one of the n^K raw configurations (n = O + sum L_t).
  (ii) the FULL JOINT empirical distribution of (V_s)_{s in S}, for every
       observed value of S, matches the predicted product of independent
       Uniform{1,...,L_s} distributions EXACTLY -- checked at the level of
       every cell of the joint product space (not just marginals), which
       is the correct adversarial target since independence claims can
       hold marginally but fail jointly.

Run at concrete (K, (L_0,...,L_{K-1}), O) configurations spanning
K=4,5,6 -- values NOT tested by the front's own position-level script
(which the front states reaches only K=1..5, "11 configurations").
"""
import itertools
from fractions import Fraction
from collections import defaultdict


def simulate_config(L, O):
    """L: tuple of arc lengths L_0,...,L_{K-1}. O: outside count.
    Enumerate all n^K raw target choices for U_0,...,U_{K-1} exactly,
    where each U_s independently ranges over a full "raw position list"
    of size n = O + sum(L): O generic outside-labeled slots (all
    equivalent, mapped to a single DEAD absorbing sink) plus, for each
    t, L_t individually-numbered slots (t, j) for j=1..L_t.
    Returns: dict raw_config -> (T, O_check, S, V_dict) computed by pure
    forward simulation of the resulting position-level functional graph,
    with NO use of "predecessor" or Lemma 4 in the construction."""
    K = len(L)
    n = O + sum(L)

    # Build the raw "slot list" each U_s ranges over: 'DEAD' (representing
    # any of the O outside points -- since they're absorbing and
    # interchangeable for our purposes, but we enumerate with the correct
    # MULTIPLICITY O so probabilities come out right) plus (t,j) for each
    # t in 0..K-1, j in 1..L_t.
    # NOTE: tag each of the O "outside" raw positions with a distinct index
    # ('DEAD', k) so that itertools.product below enumerates all n^K
    # genuinely distinct raw target-tuples (matching a true random target
    # drawn uniformly over n distinct positions) -- an earlier version of
    # this script used O identical 'DEAD' entries, which itertools.product
    # (and the results dict keyed by the raw tuple) silently collapsed into
    # fewer than n^K distinct keys whenever two different raw draws both
    # picked (possibly different) DEAD slots, undercounting P(DEAD) events.
    # Caught by an internal assertion (total_configs == n**K failing) before
    # any conclusion was drawn from this script.
    raw_slots = [('DEAD', k) for k in range(O)]
    for t in range(K):
        for j in range(1, L[t] + 1):
            raw_slots.append((t, j))
    assert len(raw_slots) == n

    results = {}
    for U in itertools.product(raw_slots, repeat=K):
        # Build position-level functional graph succ: nodes are (t,j) for
        # each t,j (arc positions) -- we do NOT explicitly model the O
        # outside points as separate nodes (they are always cyclic,
        # trivially self-looped, and contribute O to T deterministically;
        # modeling them explicitly would just add O fixed points, doesn't
        # change anything about S/V_s).
        succ = {}
        for t in range(K):
            for j in range(1, L[t]):
                succ[(t, j)] = (t, j + 1)
            # position (t, L[t]) is the source itself: its successor is
            # determined by U[t]
            target = U[t]
            if isinstance(target, tuple) and target[0] == 'DEAD':
                succ[(t, L[t])] = 'DEAD'
            else:
                succ[(t, L[t])] = target

        # direct forward simulation cycle detection over all (t,j) nodes
        nodes = list(succ.keys())
        color = {node: 0 for node in nodes}
        cyclic_positions = set()
        for start in nodes:
            if color[start] != 0:
                continue
            path = []
            cur = start
            while cur != 'DEAD' and color.get(cur, 2) == 0:
                color[cur] = 1
                path.append(cur)
                cur = succ.get(cur, 'DEAD')
            if cur != 'DEAD' and color.get(cur) == 1:
                idx = path.index(cur)
                cyclic_positions.update(path[idx:])
            for node in path:
                if color[node] == 1:
                    color[node] = 2

        S = frozenset(t for t in range(K) if (t, L[t]) in cyclic_positions)
        V = {}
        for t in S:
            V[t] = sum(1 for j in range(1, L[t] + 1) if (t, j) in cyclic_positions)

        T = O + sum(V.values())
        # independent direct count of ALL cyclic positions (should equal T
        # minus nothing extra, i.e. total cyclic positions across arcs,
        # plus O outside points which we're counting deterministically)
        total_cyclic_direct = O + len(cyclic_positions)
        assert total_cyclic_direct == T, "internal consistency check failed"

        results[U] = (T, S, V)
    return results, n


def check_config(K, L, O, label=""):
    results, n = simulate_config(L, O)
    total_configs = len(results)
    assert total_configs == n ** K

    bookkeeping_ok = True
    S_counts = defaultdict(int)
    # joint distribution of V given S: {S: {tuple_of_V_values_in_sorted(S)_order: count}}
    joint_V_given_S = defaultdict(lambda: defaultdict(int))

    for U, (T, S, V) in results.items():
        rhs = O + sum(V.values())
        if rhs != T:
            bookkeeping_ok = False
        S_counts[S] += 1
        s_sorted = sorted(S)
        v_tuple = tuple(V[s] for s in s_sorted)
        joint_V_given_S[S][v_tuple] += 1

    # Check independence + uniformity: for each S with count(S)>0, the
    # conditional joint distribution of (V_s)_{s in S} must be EXACTLY
    # uniform over the product space prod_{s in S} {1,...,L_s} (i.e. every
    # cell hit with EQUAL count = S_counts[S] / prod(L_s)).
    all_independence_ok = True
    detail_lines = []
    for S, count in S_counts.items():
        s_sorted = sorted(S)
        prod_L = 1
        for s in s_sorted:
            prod_L *= L[s]
        expected_per_cell = Fraction(count, prod_L)
        dist = joint_V_given_S[S]
        num_cells_expected = prod_L
        num_cells_observed = len(dist)
        cells_ok = True
        if num_cells_observed != num_cells_expected:
            cells_ok = False
        else:
            for v_tuple, cnt in dist.items():
                if Fraction(cnt) != expected_per_cell:
                    cells_ok = False
                    break
            # also check every possible cell in the product space is present
            for combo in itertools.product(*[range(1, L[s] + 1) for s in s_sorted]):
                if combo not in dist:
                    cells_ok = False
                    break
        all_independence_ok &= cells_ok
        detail_lines.append(
            f"    S={sorted(S)}: P(S)={count}/{total_configs}, "
            f"joint(V_s)_{{s in S}} cells observed={num_cells_observed} "
            f"(expected {num_cells_expected}), "
            f"uniform-product-match={'OK' if cells_ok else 'FAIL'}")

    print(f"  [{label}] K={K} L={L} O={O} (n={n}, n^K={n**K} raw configs): "
          f"bookkeeping={'OK' if bookkeeping_ok else 'FAIL'}, "
          f"joint independence+uniformity of (V_s|S)={'ALL OK' if all_independence_ok else 'FAIL'}")
    for line in detail_lines:
        print(line)
    return bookkeeping_ok and all_independence_ok


if __name__ == '__main__':
    print("=" * 78)
    print("Position-level Decomposition Theorem check: fresh reduced model,")
    print("built purely from prose, direct forward simulation, NO reference to")
    print("'predecessor' anywhere in the construction -- checking (i) bookkeeping")
    print("T=O+sum V_s and (ii) the FULL JOINT distribution of (V_s)_{s in S}")
    print("(not just marginals) against independent-uniform, at K=4,5,6")
    print("=" * 78)

    configs = [
        (4, (2, 2, 2, 2), 1, "K=4 small"),
        (4, (3, 2, 4, 2), 2, "K=4 mixed L"),
        (5, (2, 2, 2, 2, 2), 1, "K=5 small"),
        (5, (3, 2, 2, 3, 2), 3, "K=5 mixed L"),
        (6, (1, 1, 1, 1, 1, 1), 1, "K=6 minimal (n^K=7^6=117649)"),
        (6, (2, 1, 1, 1, 1, 1), 2, "K=6 mixed small L (n^K=8^6=262144)"),
    ]
    all_ok = True
    for K, L, O, label in configs:
        all_ok &= check_config(K, L, O, label)
    print()
    print("OVERALL:", "ALL CONFIGS PASS" if all_ok else "FAILURE DETECTED")
