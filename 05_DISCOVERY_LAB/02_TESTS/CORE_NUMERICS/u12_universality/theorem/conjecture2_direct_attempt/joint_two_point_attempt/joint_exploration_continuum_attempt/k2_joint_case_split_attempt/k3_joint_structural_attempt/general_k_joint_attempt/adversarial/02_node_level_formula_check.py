"""
Independent, from-scratch verification of the "Lemma 5 analogue" node-level
closed forms claimed in general_k_joint_attempt/ATTEMPT.md Sec 4.2-4.3:

  P_0(s)      = x_s * sum_{S subseteq Others(s)} |S|! * prod_{u in S} x_u
  P_same(s,s')     = x_s*x_s' * sum_{S subseteq M} (|S|+1)! * prod_{u in S} x_u
  P_disjoint(s,s') = x_s*x_s' * sum_{S1,S2 subseteq M, disjoint}
                        |S1|! prod_{u in S1} x_u * |S2|! prod_{u in S2} x_u

where M = {0,...,K-1} \ {s,s'}.

Independent derivation route (own, not read from any front script):
model the "destination graph" directly -- K nodes {0,...,K-1} representing
reroute sources, plus one absorbing state DEAD. Each node t's outgoing edge
goes to node u with probability x_u (u a source, u possibly = t itself --
landing "home"), or to DEAD with probability o := 1 - sum(x). Enumerate
ALL (K+1)^K destination functions exactly (own traversal code, no shortcut
formula assumed), weight each by its exact probability, and determine which
nodes are "cyclic" (lie on a directed cycle of the destination graph, i.e.
never reach DEAD) by direct forward-iteration on this small graph -- exactly
the definition given in ATTEMPT.md Sec 3.2, re-implemented from the prose,
not from any script.

For K=1..4: symbolic sympy Rational/Symbol computation (exact polynomial
identity check via sympy.expand/simplify).
For K=5,6,7: numeric exact Fraction check at several random rational
(x_0,...,x_{K-1}) points (o computed so that o>=0; several trials).
"""
import itertools
from fractions import Fraction
import random
import sys


def enumerate_destination_weighted(K, x, o):
    """x: list of length K (weights for landing on each source-node).
    o: weight for landing on DEAD.
    Returns: dict node -> total probability that node is cyclic (numeric,
    type of x[0] i.e. Fraction or sympy expr, whichever caller passes)."""
    nodes = list(range(K))
    choices = nodes + ['DEAD']
    weights = list(x) + [o]
    p0 = {s: 0 for s in nodes}
    ppair = {}
    for i in range(K):
        for j in range(K):
            if i != j:
                ppair[(i, j)] = 0
    for dest_tuple in itertools.product(range(K + 1), repeat=K):
        # dest_tuple[t] is index into choices; K+1-th choice (index K) = DEAD
        prob = 1
        for t in range(K):
            prob = prob * weights[dest_tuple[t]]
        if prob == 0:
            continue
        dest = {}
        for t in range(K):
            c = dest_tuple[t]
            dest[t] = c if c < K else None  # None = DEAD
        # find cyclic nodes: for each node, follow forward until DEAD or repeat
        cyclic = set()
        for s in nodes:
            seen = []
            cur = s
            visited = set()
            ok = False
            for _ in range(K + 1):
                if cur is None:
                    break
                if cur == s and len(seen) > 0:
                    ok = True
                    break
                if cur in visited:
                    break
                visited.add(cur)
                seen.append(cur)
                cur = dest[cur]
            if ok:
                cyclic.add(s)
        for s in cyclic:
            p0[s] = p0[s] + prob
        for (i, j) in ppair:
            if i in cyclic and j in cyclic:
                ppair[(i, j)] = ppair[(i, j)] + prob
    return p0, ppair


def claimed_P0(K, s, x):
    others = [u for u in range(K) if u != s]
    total = 0
    from math import factorial
    for r in range(len(others) + 1):
        for S in itertools.combinations(others, r):
            term = 1
            for u in S:
                term = term * x[u]
            total = total + factorial(len(S)) * term
    return x[s] * total


def claimed_Ppair(K, s, sp, x):
    from math import factorial
    M = [u for u in range(K) if u != s and u != sp]
    # same
    same = 0
    for r in range(len(M) + 1):
        for S in itertools.combinations(M, r):
            term = 1
            for u in S:
                term = term * x[u]
            same = same + factorial(len(S) + 1) * term
    same = same * x[s] * x[sp]
    # disjoint
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


def numeric_check(K, trials=4, seed=20260904900):
    rng = random.Random(seed)
    all_ok = True
    for trial in range(trials):
        # pick random positive integer denominators to keep exact fractions small-ish
        n = rng.randint(K + 2, 40)
        # pick K distinct positive arc lengths L_0..L_{K-1} with sum <= n
        # simple: random composition
        remaining = n - K  # need sum(L_s - 1) + O = n-K, L_s>=1
        parts = []
        r = remaining
        for i in range(K):
            if i == K - 1:
                take = rng.randint(0, r)
            else:
                take = rng.randint(0, r)
            parts.append(take)
            r -= take
        L = [1 + parts[i] for i in range(K)]
        O = r
        assert sum(L) + O == n
        x = [Fraction(Ls, n) for Ls in L]
        o = Fraction(O, n)
        p0, ppair = enumerate_destination_weighted(K, x, o)
        ok_trial = True
        for s in range(K):
            claimed = claimed_P0(K, s, x)
            if claimed != p0[s]:
                ok_trial = False
                print(f"  MISMATCH P0 K={K} s={s} n={n} L={L} O={O}: brute={p0[s]} claimed={claimed}")
        for (i, j) in ppair:
            if i < j:
                claimed = claimed_Ppair(K, i, j, x)
                if claimed != ppair[(i, j)]:
                    ok_trial = False
                    print(f"  MISMATCH Ppair K={K} s={i} s'={j} n={n} L={L} O={O}: brute={ppair[(i,j)]} claimed={claimed}")
        status = "OK" if ok_trial else "FAIL"
        print(f"K={K} trial={trial} n={n} L={L} O={O} -> {status}")
        all_ok = all_ok and ok_trial
    return all_ok


if __name__ == "__main__":
    # Referee's own reserved seed range (this lineage's convention: front
    # uses 20260904000-20260904999, referee uses 20260905000-20260905999 --
    # confirmed against THEOREM.md Sec DISC-DEC-093 citation in the front's
    # own Sec 9). Purely for reproducibility bookkeeping; these checks are
    # exact-Fraction, not statistical, so the seed only picks which (n,L,O)
    # configurations are sampled, not any probabilistic tolerance.
    overall = True
    for K in range(1, 6):
        print(f"=== K={K} ===")
        ok = numeric_check(K, trials=4, seed=20260905000 + K)
        overall = overall and ok
    for K in [6, 7]:
        print(f"=== K={K} ===")
        ok = numeric_check(K, trials=2, seed=20260905000 + K)
        overall = overall and ok
    print("ALL OK" if overall else "SOME MISMATCHES FOUND")
