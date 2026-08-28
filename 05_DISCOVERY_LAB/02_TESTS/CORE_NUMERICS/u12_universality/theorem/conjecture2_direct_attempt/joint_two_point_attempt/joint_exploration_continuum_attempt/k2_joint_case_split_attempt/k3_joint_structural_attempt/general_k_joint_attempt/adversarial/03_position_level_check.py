"""
Independent, from-scratch position-level check of the general-K single-point
and cross-arc formulas (ATTEMPT.md Sec 4.2-4.3), including the "landing
position uniform, independent of cycle structure" claim (Sec 4.1) that
converts node-level P_0(s)/P_pair(s,s') into position-level predictions
  P(pos i in ARC(s) cyclic) = (i/L_s) * P_0(s)
  P(pos i in ARC(s), pos i' in ARC(s') both cyclic) = (i/L_s)(i'/L_s') * P_{s,s'}

Own construction of the actual position-by-position functional graph (not
the node abstraction): for K arcs of given lengths L_0..L_{K-1}, interior
position j of arc s (1<=j<L_s) has deterministic outgoing edge -> position
j+1 of arc s (the unmodified permutation chain). The source itself (j=L_s)
has outgoing edge = wherever its i.i.d. Uniform([n]) target lands: one of
the n slots, of which sum(L_u) land inside some arc (at a uniformly random
position within it) and O := n - sum(L_u) land "outside" (which this
sub-model treats as an absorbing DEAD state, since outside points are
independently and unconditionally cyclic per Sec 3.1, never re-entering
any arc).

This enumerates ALL n^K target choices exactly (own code, Fraction
arithmetic), builds the graph, determines cyclicity of every specific
position by direct forward traversal, and compares against the claimed
closed-form predictions built from the (already independently verified)
node-level P_0/P_pair formulas.
"""
import itertools
from fractions import Fraction
from math import factorial


def claimed_P0(K, s, x):
    others = [u for u in range(K) if u != s]
    total = 0
    for r in range(len(others) + 1):
        for S in itertools.combinations(others, r):
            term = 1
            for u in S:
                term = term * x[u]
            total = total + factorial(len(S)) * term
    return x[s] * total


def claimed_Ppair(K, s, sp, x):
    M = [u for u in range(K) if u != s and u != sp]
    same = 0
    for r in range(len(M) + 1):
        for S in itertools.combinations(M, r):
            term = 1
            for u in S:
                term = term * x[u]
            same = same + factorial(len(S) + 1) * term
    same = same * x[s] * x[sp]
    disj = 0
    for r1 in range(len(M) + 1):
        for S1 in itertools.combinations(M, r1):
            rest = [u for u in M if u not in S1]
            for r2 in range(len(rest) + 1):
                for S2 in itertools.combinations(rest, r2):
                    t1 = 1
                    for u in S1:
                        t1 = t1 * x[u]
                    t2 = 1
                    for u in S2:
                        t2 = t2 * x[u]
                    disj = disj + factorial(len(S1)) * t1 * factorial(len(S2)) * t2
    disj = disj * x[s] * x[sp]
    return same + disj


def position_level_bruteforce(L, O):
    """L: list of arc lengths (>=1 each). O: number of outside slots.
    Returns dict (s,i) -> exact Fraction P(position i of arc s is cyclic),
    and dict ((s,i),(s',i')) -> P(both cyclic), via exhaustive enumeration
    of all n^K target choices, n = sum(L)+O, K=len(L)."""
    K = len(L)
    n = sum(L) + O
    # enumerate all target "slots" 0..n-1; map slot -> (arc, pos) or None(outside)
    slot_map = []  # index -> ('arc', s, pos) or ('out',)
    for s in range(K):
        for pos in range(1, L[s] + 1):
            slot_map.append(('arc', s, pos))
    for _ in range(O):
        slot_map.append(('out',))
    assert len(slot_map) == n

    cyclic_count = {}
    pair_count = {}
    for s in range(K):
        for i in range(1, L[s] + 1):
            cyclic_count[(s, i)] = 0
    total = 0

    for targets in itertools.product(range(n), repeat=K):
        total += 1
        # build outgoing edge for each arc's source node
        # dest[s] = ('arc', s2, pos2) or ('out',)
        dest = {}
        for t in range(K):
            dest[t] = slot_map[targets[t]]

        # function: given (s,i), returns next (s,i) or 'OUT'
        def nxt(s, i):
            if i < L[s]:
                return (s, i + 1)
            else:
                d = dest[s]
                if d[0] == 'out':
                    return 'OUT'
                else:
                    return (d[1], d[2])

        # determine cyclic positions: for every (s,i) check via forward iter
        cyclic_here = set()
        for s in range(K):
            for i in range(1, L[s] + 1):
                cur = (s, i)
                start = (s, i)
                seen = set()
                is_cyc = False
                for _ in range(sum(L) + 1):
                    cur = nxt(*cur)
                    if cur == 'OUT':
                        break
                    if cur == start:
                        is_cyc = True
                        break
                    if cur in seen:
                        break
                    seen.add(cur)
                if is_cyc:
                    cyclic_here.add((s, i))
        for key in cyclic_here:
            cyclic_count[key] += 1
        for k1 in cyclic_here:
            for k2 in cyclic_here:
                if k1 != k2:
                    pair_count[(k1, k2)] = pair_count.get((k1, k2), 0) + 1

    cyclic_prob = {k: Fraction(v, total) for k, v in cyclic_count.items()}
    pair_prob = {k: Fraction(v, total) for k, v in pair_count.items()}
    return cyclic_prob, pair_prob, total


def check(L, O):
    K = len(L)
    n = sum(L) + O
    x = [Fraction(Ls, n) for Ls in L]
    cyclic_prob, pair_prob, total = position_level_bruteforce(L, O)
    ok = True
    for s in range(K):
        P0 = claimed_P0(K, s, x)
        for i in range(1, L[s] + 1):
            claimed = Fraction(i, L[s]) * P0
            got = cyclic_prob[(s, i)]
            if claimed != got:
                ok = False
                print(f"  MISMATCH single s={s} i={i}: brute={got} claimed={claimed}")
    for s in range(K):
        for sp in range(K):
            if s == sp:
                continue
            Pss = claimed_Ppair(K, s, sp, x)
            for i in range(1, L[s] + 1):
                for ip in range(1, L[sp] + 1):
                    claimed = Fraction(i, L[s]) * Fraction(ip, L[sp]) * Pss
                    got = pair_prob.get(((s, i), (sp, ip)), Fraction(0))
                    if claimed != got:
                        ok = False
                        print(f"  MISMATCH pair s={s}i={i} s'={sp}i'={ip}: brute={got} claimed={claimed}")
    print(f"L={L} O={O} n={n} configs={total} -> {'OK' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    cases = [
        ([2], 1),
        ([3], 0),
        ([2, 2], 0),
        ([1, 3], 1),
        ([2, 2, 2], 0),
        ([1, 2, 1], 1),
        ([2, 1, 1, 1], 0),
    ]
    overall = True
    for L, O in cases:
        overall = check(L, O) and overall
    print("ALL OK" if overall else "SOME MISMATCHES")
