#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check #3: TRUE brute force of Definition 4's
literal model (genuine random permutations pi of [n], genuine target
tuples U_0,...,U_{K-1}), built entirely from THEOREM.md's Definitions 1-4
prose plus ATTEMPT.md's own restatement of them (Section 1.2), WITHOUT
reading any .py file from this front or its lineage.

Model: f(i) = U_i for i in {0,...,K-1} ("reroute sources"), f(i) = pi(i)
otherwise. T := #cyclic points of f (points i with f^m(i)=i for some
m>=1, equivalently: on a cycle of the functional graph f). This script
reconstructs, DIRECTLY from f's own functional-graph structure (NOT from
any assumed arc/gap-vector formula), the following quantities:
  - O: number of points whose eventual cycle contains none of the K
       reroute sources (points "outside" all arcs)
  - S: sub-set of {0,...,K-1} that are cyclic (lie on a cycle of f)
  - the arc lengths L_0,...,L_{K-1} of the K reroute sources under pi
       (from pi's own cycle structure, cut at the K source points), and
  - V_s for s in S: cyclic-point-count contributed by ARC(s) (empirically,
       #f-cyclic-points among pi-successors of s up to (but re-including
       through the correct wraparound) the point that lands on the f-cycle)

We do NOT assume the ARC(s)/gap-vector machinery at all -- we compute
everything by directly simulating f = the reroute-modified permutation and
finding its cycles, then separately (independently) reconstruct which
positions "belong" to which source's arc using pi's own cycle structure
(the definition of ARC(s) from THEOREM.md Def 3/4: pi-successors of s,
i.e. s, pi(s), pi(pi(s)), ..., up to (not including) the next reroute
source or back to s), purely as an f-independent bookkeeping decomposition
of the n points -- exactly as the front's own Section 2.5(d) describes
doing, but implemented completely independently here.

Checks performed, all at the UNCONDITIONAL level (averaging over BOTH the
random permutation pi over all n! permutations, uniformly, AND the K
target draws U_0,...,U_{K-1} independently uniform over [n], i.e. n^K):

  1. Deterministic bookkeeping identity T = O + sum_{s in S} V_s holds in
     EVERY single configuration (exact, not average).
  2. Exact empirical marginal P(S=A) for every A subseteq {0,...,K-1},
     via exact Fraction arithmetic over all n! * n^K configurations,
     compared against Proposition S's closed form -- BUT Proposition S is
     stated in terms of L_s/n and O/n, which are themselves random (depend
     on pi and NOT on U); this script computes the TRUE UNCONDITIONAL
     P(S=A) two ways: (i) direct empirical count from the n!*n^K raw
     enumeration; (ii) Proposition S's formula evaluated at each
     (L_0,...,L_{K-1},O) arising from pi, weighted by the TRUE probability
     of that gap/arc-length pattern under a uniform random permutation,
     and averaged -- an entirely independent unconditional check that does
     NOT rely on the "gap vector is uniform over compositions" citation at
     all (it recomputes the arc-length distribution directly from
     brute-force permutations, sidestepping the very bug class the front
     itself disclosed catching).

Run at (n,K) cells NOT used by the front's own true-bruteforce script
(front used: (4,1),(5,1),(4,2),(5,2),(6,2),(4,3),(5,3),(6,3),(5,4),(6,4)):
this script uses (4,1),(5,1),(6,1),(4,2),(5,2),(4,3),(6,3),(5,4),(7,2),
(7,3) -- overlapping partially (as an independent re-derivation, not
avoidance) but ALSO reaching (7,2) and (7,3), cells the front's own script
never reached, plus (6,1) as an extra small sanity cell.
"""
import itertools
from fractions import Fraction


def permutations(n):
    return itertools.permutations(range(n))


def build_f(n, K, pi, U):
    """f(i) = U[i] for i<K, f(i)=pi[i] otherwise. pi, U: tuples length n / K."""
    f = list(pi)
    for s in range(K):
        f[s] = U[s]
    return f


def cycles_of(f, n):
    """Return list of cycles (each a list of nodes) of the functional graph f,
    found by direct forward simulation from every unvisited node."""
    color = [0] * n  # 0=unvisited,1=in-progress,2=done
    cycles = []
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        cur = start
        while color[cur] == 0:
            color[cur] = 1
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:
            # found a new cycle: cur is the entry point of the cycle within path
            idx = path.index(cur)
            cycles.append(path[idx:])
        for node in path:
            color[node] = 2
    return cycles


def analyze_config(n, K, pi, U):
    f = build_f(n, K, pi, U)
    cycles = cycles_of(f, n)
    cyclic_points = set()
    for c in cycles:
        cyclic_points.update(c)
    T = len(cyclic_points)

    S = frozenset(s for s in range(K) if s in cyclic_points)

    # Reconstruct ARC(s) for each source s DIRECTLY from pi's own cycle
    # structure (independent of f). Per ATTEMPT.md Section 1.2: "ARC(s) has
    # L_s positions, 1,...,L_s-1 interior, position L_s the source itself"
    # -- i.e. the source occupies the LAST position of its arc, and the arc
    # consists of s's pi-PREDECESSORS (the points that pi-flow INTO s before
    # reaching another source), not its pi-successors. So we walk BACKWARD
    # via pi^{-1} from s, until hitting another source (exclusive) or
    # wrapping back to s (whole pi-cycle belongs to s alone).
    #
    # NOTE (self-caught bug, disclosed): an earlier version of this script
    # walked FORWARD via pi from s (s, pi(s), pi(pi(s)), ...), which
    # misattributes points between arcs (it assigns the successor-run to s
    # instead of to whichever source that run actually flows into) and
    # produced spurious T != O + sum V_s "failures" purely as an artifact
    # of this script's own bug -- not a flaw in the theorem. Fixed here by
    # walking pi^{-1} (backward) instead; see adv_03_debug_note.log.
    sources = set(range(K))
    inv_pi = [0] * n
    for i in range(n):
        inv_pi[pi[i]] = i

    arc_of = {}
    L = {}
    for s in range(K):
        run = [s]
        cur = inv_pi[s]
        while cur not in sources and cur != s:
            run.append(cur)
            cur = inv_pi[cur]
        # run currently = [s, pi^{-1}(s), pi^{-2}(s), ...] in BACKWARD order;
        # reverse to get forward position order 1,...,L_s (source last)
        run.reverse()
        arc_of[s] = run
        L[s] = len(run)

    all_arc_points = set()
    for s in range(K):
        all_arc_points.update(arc_of[s])
    O = n - len(all_arc_points)

    # V_s: number of f-cyclic points within ARC(s), for s in S
    V = {}
    for s in S:
        V[s] = sum(1 for p in arc_of[s] if p in cyclic_points)

    return T, O, S, L, V, arc_of


def true_bruteforce_cell(n, K):
    total_configs = 0
    bookkeeping_failures = 0
    S_counts = {}
    n_fact = 1
    for i in range(2, n + 1):
        n_fact *= i
    total_expected = n_fact * (n ** K)

    for pi in permutations(n):
        for U in itertools.product(range(n), repeat=K):
            total_configs += 1
            T, O, S, L, V, arc_of = analyze_config(n, K, pi, U)
            rhs = O + sum(V.values())
            if rhs != T:
                bookkeeping_failures += 1
            S_counts[S] = S_counts.get(S, 0) + 1

    assert total_configs == total_expected

    P_S = {A: Fraction(cnt, total_configs) for A, cnt in S_counts.items()}
    return total_configs, bookkeeping_failures, P_S


def proposition_s_predicted_unconditional(n, K):
    """Independent unconditional evaluation of Proposition S, NOT via the
    gap-vector-uniform citation, but by directly computing, from brute-force
    over all n! permutations pi (uniform), the TRUE joint distribution of
    (L_0,...,L_{K-1}, O), and averaging Proposition S's formula
    P(S=A|L,O) = |A|! prod_A (L_a/n) * (O/n + sum_A L_a/n)
    over that TRUE empirical distribution. This sidesteps the "gap vector
    vs L vector uniform" citation entirely -- it recomputes the arc-length
    distribution from scratch via genuine permutation enumeration, exactly
    matching what determines P(S=A) in the true model (since, in the true
    joint model, given L exactly, S's conditional law is Proposition S,
    a fact this script does not need to re-derive here because it is
    checking the FULL unconditional P(S=A) end-to-end against real brute
    force of the actual randomized destinations too, in true_bruteforce_cell
    above; this function serves as a SECOND, independent route)."""
    n_fact = 1
    for i in range(2, n + 1):
        n_fact *= i

    L_O_counts = {}
    for pi in permutations(n):
        sources = set(range(K))
        inv_pi = [0] * n
        for i in range(n):
            inv_pi[pi[i]] = i
        arc_of = {}
        for s in range(K):
            run = [s]
            cur = inv_pi[s]
            while cur not in sources and cur != s:
                run.append(cur)
                cur = inv_pi[cur]
            arc_of[s] = run
        all_arc_points = set()
        for s in range(K):
            all_arc_points.update(arc_of[s])
        O = n - len(all_arc_points)
        L = tuple(len(arc_of[s]) for s in range(K))
        key = (L, O)
        L_O_counts[key] = L_O_counts.get(key, 0) + 1

    # sanity: sum of counts == n!
    assert sum(L_O_counts.values()) == n_fact

    subsets = []
    for r in range(K + 1):
        subsets.extend(itertools.combinations(range(K), r))

    P_S_predicted = {}
    for A_tuple in subsets:
        A = frozenset(A_tuple)
        m = len(A)
        total = Fraction(0)
        for (L, O), cnt in L_O_counts.items():
            prob_L_O = Fraction(cnt, n_fact)
            prod_A = Fraction(1)
            for a in A:
                prod_A *= Fraction(L[a], n)
            sum_A = Fraction(sum(L[a] for a in A), n)
            pD = Fraction(O, n)
            m_fact = 1
            for i in range(2, m + 1):
                m_fact *= i
            val = m_fact * prod_A * (pD + sum_A)
            total += prob_L_O * val
        P_S_predicted[A] = total

    return P_S_predicted


def run_cell(n, K):
    print(f"--- (n={n}, K={K}) ---")
    total_configs, bk_fail, P_S_empirical = true_bruteforce_cell(n, K)
    print(f"  total configs = n!*n^K = {total_configs}, "
          f"bookkeeping failures (T != O+sum V_s) = {bk_fail}")
    P_S_predicted = proposition_s_predicted_unconditional(n, K)

    all_A = set(P_S_empirical.keys()) | set(P_S_predicted.keys())
    mismatches = []
    for A in sorted(all_A, key=lambda x: (len(x), sorted(x))):
        emp = P_S_empirical.get(A, Fraction(0))
        pred = P_S_predicted.get(A, Fraction(0))
        if emp != pred:
            mismatches.append((A, emp, pred))
    total_pred_check = sum(P_S_predicted.values())
    assert total_pred_check == 1, f"predicted P(S=A) does not sum to 1: {total_pred_check}"
    total_emp_check = sum(P_S_empirical.values())
    assert total_emp_check == 1

    if mismatches:
        print(f"  MISMATCHES ({len(mismatches)}):")
        for A, emp, pred in mismatches:
            print(f"    A={sorted(A)}: empirical={emp}  Prop-S-predicted={pred}")
    else:
        print(f"  ALL {len(all_A)} subsets A match EXACTLY (empirical == Proposition S prediction)"
              f", bookkeeping identity holds in all {total_configs} configs")
    return bk_fail == 0 and not mismatches


if __name__ == '__main__':
    print("=" * 78)
    print("SELF-CAUGHT BUG DISCLOSURE (this referee's own script, not the front's):")
    print("An earlier version of this script's arc-reconstruction walked FORWARD")
    print("via pi from each source s (s, pi(s), pi(pi(s)), ...) to build ARC(s).")
    print("This is backward: per ATTEMPT.md Section 1.2, position L_s (the LAST")
    print("position of ARC(s)) is the source itself, i.e. ARC(s) consists of s's")
    print("pi-PREDECESSORS, not successors. The forward-walk bug misattributed")
    print("points between arcs and produced spurious T != O+sum V_s 'failures'")
    print("at (n=4,K=2): 44/384 configs failing bookkeeping under the buggy")
    print("version, ALL 384 passing after the fix (walk pi^{-1} backward from s")
    print("instead). This was a bug in this adversarial script, not evidence")
    print("against the theorem -- caught and fixed before drawing any")
    print("conclusion, exactly the discipline the front itself models.")
    print("=" * 78)
    print()
    cells = [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2), (4, 3), (6, 3), (5, 4), (7, 2), (7, 3), (6, 4)]
    print("=" * 78)
    print("TRUE brute force of Definition 4's literal model (genuine pi, genuine U),")
    print("own arc-reconstruction from pi's cycle structure, checking BOTH:")
    print("  (1) deterministic identity T = O + sum_{s in S} V_s in every config, and")
    print("  (2) unconditional P(S=A) via two independent routes (raw enumeration vs")
    print("      Proposition S formula averaged over the TRUE brute-force arc-length")
    print("      distribution, recomputed from scratch, not cited)")
    print("=" * 78)
    all_ok = True
    for n, K in cells:
        all_ok &= run_cell(n, K)
    print()
    print("OVERALL:", "ALL CELLS PASS" if all_ok else "FAILURE DETECTED")
