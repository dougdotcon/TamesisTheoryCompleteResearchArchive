"""
K4-FULL-CDF-ATTEMPT: Proposicao S and the Full Cycle-Count Decomposition
Theorem, instantiated at K=4 (CITED from THEOREM.md Estagio 41 / the
general_k_decomposition_attempt ATTEMPT.md, NOT re-derived here -- this
script only re-verifies the K=4 instance from scratch, independently).

Sources fixed at {0,1,2,3}.  Arc lengths L0,L1,L2,L3 (each >=1), O := n -
L0-L1-L2-L3 (>=0).  p_i := L_i/n, p_D := O/n.

Proposicao S (general K, CITED):
    P(S=A) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)
for every A subseteq {0,1,2,3}.

This script:
  1. Verifies Proposicao S at K=4 against the raw 5^4=625 destination-table
     enumeration (symbolic weights p0,p1,p2,p3,pD with pD=1-sum, exact
     sympy rational algebra) -- fresh code, no shortcut.
  2. Verifies the Full Cycle-Count Decomposition Theorem at K=4 against a
     from-scratch position-level reduced model (explicit small functional
     graphs on the L0+L1+L2+L3 arc positions, enumerating all n^4 landing
     choices) at several small (n, L) configurations.
  3. Verifies the *unconditional* decomposition (Prop S + Decomposition
     Theorem, averaged over the composition simplex) against a completely
     fresh true brute force of Definition 4's actual K=4 model at small n.

No .py file from any other front was read; this is written from scratch
from the prose citations in THEOREM.md Estagio 41 and the
general_k_decomposition_attempt/ATTEMPT.md prose (Proposicao S's general
statement, Sections 2.4 there).
"""
import itertools
from fractions import Fraction
import sympy as sp

K = 4
SOURCES = list(range(K))

# ---------------------------------------------------------------------
# Part 1: Proposicao S at K=4, symbolic weights, vs raw 5^4 destination
# table (DEAD is treated as an extra "flavor").
# ---------------------------------------------------------------------

def prop_S_formula(A, p, pD):
    """P(S=A) via Proposicao S, general K (cited)."""
    m = len(A)
    fact = sp.factorial(m)
    prod = sp.Integer(1)
    for a in A:
        prod *= p[a]
    ssum = sum(p[a] for a in A)
    return fact * prod * (pD + ssum)


def prop_S_raw_symbolic():
    """Raw enumeration over all (K+1)^K destination combinations
    dest: {0,..,K-1} -> {0,...,K-1, DEAD}, symbolic weights."""
    p = sp.symbols('p0 p1 p2 p3', positive=True)
    pD = 1 - sum(p)
    weight = {i: p[i] for i in range(K)}
    weight['D'] = pD

    # accumulate P(S=A) for each subset A by raw enumeration
    subset_probs = {frozenset(A): sp.Integer(0)
                     for r in range(K + 1)
                     for A in itertools.combinations(SOURCES, r)}

    targets = list(range(K)) + ['D']
    for dest_tuple in itertools.product(targets, repeat=K):
        dest = dict(zip(SOURCES, dest_tuple))
        # determine cyclic set S: node s cyclic iff iterating dest from s
        # returns to s before hitting 'D'
        S = set()
        for s in SOURCES:
            cur = s
            seen = set()
            cyclic = False
            while True:
                if cur == 'D':
                    cyclic = False
                    break
                if cur in seen:
                    cyclic = (cur == s) or (s in seen)
                    # more careful: standard functional graph cyclicity
                    break
                seen.add(cur)
                cur = dest[cur]
            # redo properly: forward-iterate at most K+1 steps
            cur = s
            path = []
            cyclic = False
            for _ in range(K + 1):
                path.append(cur)
                if cur == 'D':
                    break
                cur = dest[cur]
            # s is cyclic iff following dest from s returns to s without
            # hitting 'D' first
            cur = dest[s]
            steps = 0
            cyclic = False
            visited = {s}
            while cur != 'D' and steps <= K:
                if cur == s:
                    cyclic = True
                    break
                if cur in visited:
                    break
                visited.add(cur)
                cur = dest[cur]
                steps += 1
            if cyclic:
                S.add(s)
        w = sp.Integer(1)
        for s in SOURCES:
            w *= weight[dest[s]]
        subset_probs[frozenset(S)] += w

    for key in subset_probs:
        subset_probs[key] = sp.expand(subset_probs[key])
    return subset_probs, p, pD


def verify_prop_S():
    print("=" * 78)
    print("PART 1: Proposicao S at K=4 vs raw 5^4=625 destination enumeration")
    print("=" * 78)
    subset_probs, p, pD = prop_S_raw_symbolic()
    all_ok = True
    for r in range(K + 1):
        for A in itertools.combinations(SOURCES, r):
            raw = subset_probs[frozenset(A)]
            formula = sp.expand(prop_S_formula(A, p, pD))
            diff = sp.simplify(raw - formula)
            ok = (diff == 0)
            all_ok &= ok
            print(f"  A={A!s:14s} raw-formula diff={diff}  {'OK' if ok else 'MISMATCH'}")
    total = sp.simplify(sum(subset_probs.values()) - 1)
    print(f"  sum of all P(S=A) - 1 = {total}  {'OK' if total == 0 else 'MISMATCH'}")
    all_ok &= (total == 0)
    print("ALL PROP-S CHECKS PASSED." if all_ok else "SOME PROP-S CHECKS FAILED.")
    return all_ok


# ---------------------------------------------------------------------
# Part 2: Decomposition Theorem given L, via a from-scratch position-level
# reduced model (K=4).
# ---------------------------------------------------------------------

def reduced_model_pmf(n, L):
    """Build the position-level functional graph for K=4 directly from
    Definition 4's prose: ARC(s) has positions 1..L[s] (position L[s] is
    the source itself); within-arc successor i->i+1 deterministic (this
    models pi restricted to the arc, i.e. pi(i)=i+1 for i<L[s], and
    pi(L[s])=s's own next-arc/gap start which is irrelevant here since
    the source's own f-value is overridden); source s's own outgoing
    edge f(s) = landing slot of U_s among n total slots, enumerated
    exactly (all n^4 raw choices).  Positions outside all arcs (there are
    O of them) are always cyclic and excluded from bookkeeping.  Returns:
    dict {(S_tuple, V_tuple): count} where S_tuple is the sorted tuple of
    cyclic sources and V_tuple gives, for each s in S, the value
    V_s = L[s]-k_s+1 (landing position within its own arc, converted).
    """
    O = n - sum(L)
    assert O >= 0
    # slot layout: positions 0..n-1.  Arc s occupies a contiguous block of
    # L[s] slots; landing "in ARC(s) at position i" (i=1..L[s], 1=start
    # away-from-source .. L[s]=the source itself) maps to slot
    # arc_start[s] + (i-1).  Positions outside all arcs are the remaining
    # O slots (labelled 'OUT').
    arc_start = {}
    cur = 0
    for s in range(K):
        arc_start[s] = cur
        cur += L[s]
    slot_region = {}  # slot -> ('ARC', s, i) or ('OUT',)
    for s in range(K):
        for i in range(1, L[s] + 1):
            slot_region[arc_start[s] + (i - 1)] = ('ARC', s, i)
    for slot in range(cur, n):
        slot_region[slot] = ('OUT',)

    results = {}
    for U in itertools.product(range(n), repeat=K):
        dest = {}
        for s in range(K):
            reg = slot_region[U[s]]
            if reg[0] == 'ARC':
                dest[s] = (reg[1], reg[2])  # (arc, landing pos within arc)
            else:
                dest[s] = 'OUT'

        # Build full functional graph on the K sources plus "OUT"/interior
        # positions is unnecessary: cyclicity of source s depends only on
        # iterating "which arc does U_s land in" (dest[s][0] if ARC, else
        # dead).  This matches Section 2 of the general-K Decomposition
        # Theorem citation.
        def dest_arc(s):
            d = dest[s]
            return d[0] if d != 'OUT' else 'D'

        S = []
        for s in range(K):
            cur_node = dest_arc(s)
            visited = {s}
            cyclic = False
            steps = 0
            while cur_node != 'D' and steps <= K:
                if cur_node == s:
                    cyclic = True
                    break
                if cur_node in visited:
                    break
                visited.add(cur_node)
                cur_node = dest_arc(cur_node)
                steps += 1
            if cyclic:
                S.append(s)
        S = tuple(sorted(S))

        # For s in S, V_s = L[s] - k_s + 1 where k_s is the landing
        # position (within ARC(s)) of U_{pred(s)}.  pred(s) is the unique
        # t with dest_arc(t)=s and t cyclic.
        V = {}
        for s in S:
            preds = [t for t in S if dest_arc(t) == s]
            assert len(preds) == 1, (S, dest, preds)
            t = preds[0]
            i_land = dest[t][1]  # landing position within ARC(s)
            V[s] = L[s] - i_land + 1
        V_tuple = tuple(V[s] for s in S)
        key = (S, V_tuple)
        results[key] = results.get(key, 0) + 1
    total = n ** K
    return {k_: Fraction(v, total) for k_, v in results.items()}


def decomposition_formula_pmf(n, L):
    """Predicted joint pmf of (S, (V_s)_{s in S}) from Prop S + the claim
    that, given S, the V_s are mutually independent Uniform{1,...,L_s}."""
    O = n - sum(L)
    p = [Fraction(L[i], n) for i in range(K)]
    pD = Fraction(O, n)
    out = {}
    for r in range(K + 1):
        for A in itertools.combinations(SOURCES, r):
            m = len(A)
            fact = 1
            for j in range(1, m + 1):
                fact *= j
            prod = 1
            for a in A:
                prod *= p[a]
            ssum = sum(p[a] for a in A)
            PA = fact * prod * (pD + ssum)
            if PA == 0:
                continue
            # distribute uniformly over all V combos
            ranges = [range(1, L[a] + 1) for a in A]
            n_combos = 1
            for a in A:
                n_combos *= L[a]
            for V_combo in itertools.product(*ranges):
                key = (A, V_combo)
                out[key] = out.get(key, Fraction(0)) + PA * Fraction(1, n_combos)
    return out


def verify_decomposition_given_L():
    print()
    print("=" * 78)
    print("PART 2: Decomposition Theorem given L, K=4, position-level reduced model")
    print("=" * 78)
    configs = [
        (7, (1, 1, 1, 1)),
        (8, (2, 1, 1, 1)),
        (8, (1, 2, 1, 2)),
        (9, (2, 2, 1, 1)),
        (7, (1, 1, 1, 2)),
    ]
    all_ok = True
    for n, L in configs:
        reduced = reduced_model_pmf(n, L)
        formula = decomposition_formula_pmf(n, L)
        keys = set(reduced) | set(formula)
        mismatches = 0
        for k_ in keys:
            a = reduced.get(k_, Fraction(0))
            b = formula.get(k_, Fraction(0))
            if a != b:
                mismatches += 1
        ok = (mismatches == 0)
        all_ok &= ok
        print(f"  n={n} L={L}: {len(keys)} joint cells, mismatches={mismatches}  {'OK' if ok else 'FAIL'}")
    print("Decomposition Theorem (given L) CONFIRMED." if all_ok else "FAILED.")
    return all_ok


# ---------------------------------------------------------------------
# Part 3: unconditional check against a fresh true brute force of
# Definition 4's actual K=4 model.
# ---------------------------------------------------------------------

def true_bruteforce_T_pmf(n):
    """Fresh, from-scratch, fully exhaustive enumeration of Definition 4's
    literal K=4 model: pi a permutation of [n], U0..U3 iid targets in
    [0,n), sources fixed at 0,1,2,3.  f(i)=U_i for i<4, else f(i)=pi(i).
    T = #cyclic points of f.  Returns pmf of T as Fraction dict."""
    from itertools import permutations, product
    counts = {}
    total = 0
    for pi in permutations(range(n)):
        f = list(pi)
        for U in product(range(n), repeat=K):
            for s in range(K):
                f[s] = U[s]
            # find cyclic points: forward-iterate from each point; a point
            # i is cyclic iff following f from i returns to i.
            T = 0
            for i in range(n):
                cur = f[i]
                steps = 0
                found = False
                while steps <= n:
                    if cur == i:
                        found = True
                        break
                    cur = f[cur]
                    steps += 1
                if found:
                    T += 1
            counts[T] = counts.get(T, 0) + 1
            total += 1
            f = list(pi)  # reset for next U (f[s] gets overwritten again)
    return {t: Fraction(c, total) for t, c in counts.items()}, total


def decomposition_unconditional_pmf(n):
    """Sum decomposition_formula_pmf(n, L) over the composition simplex of
    L (each L_i>=1, sum L_i <= n), weighted by 1/C(n,4) (uniform over
    compositions of n-4 into 5 nonneg parts -- i.e. over all (L,O) with
    L_i>=1, O>=0, sum=n)."""
    import math
    from itertools import combinations

    out = {}
    n_comps = 0
    for L0 in range(1, n - 2):
        for L1 in range(1, n - L0 - 1):
            for L2 in range(1, n - L0 - L1):
                L3max = n - L0 - L1 - L2  # O>=0 means L3 <= this, L3>=1
                for L3 in range(1, L3max + 1):
                    L = (L0, L1, L2, L3)
                    O = n - sum(L)
                    if O < 0:
                        continue
                    n_comps += 1
                    joint = decomposition_formula_pmf(n, L)
                    for (A, Vc), pr in joint.items():
                        T = O + sum(Vc)
                        out[T] = out.get(T, Fraction(0)) + pr
    for t in out:
        out[t] = out[t] / n_comps
    return out, n_comps


def verify_unconditional():
    print()
    print("=" * 78)
    print("PART 3: unconditional decomposition vs fresh true brute force, K=4")
    print("=" * 78)
    all_ok = True
    for n in (5, 6):
        bf_pmf, bf_total = true_bruteforce_T_pmf(n)
        dec_pmf, n_comps = decomposition_unconditional_pmf(n)
        keys = set(bf_pmf) | set(dec_pmf)
        mism = 0
        for t in sorted(keys):
            a = bf_pmf.get(t, Fraction(0))
            b = dec_pmf.get(t, Fraction(0))
            if a != b:
                mism += 1
                print(f"    MISMATCH n={n} T={t}: bruteforce={a} decomposition={b}")
        ok = (mism == 0)
        all_ok &= ok
        print(f"  n={n}: bruteforce configs={bf_total}, decomposition compositions={n_comps}, mismatches={mism}  {'OK' if ok else 'FAIL'}")
    print("Full unconditional decomposition CONFIRMED against fresh true brute force." if all_ok else "FAILED.")
    return all_ok


if __name__ == "__main__":
    ok1 = verify_prop_S()
    ok2 = verify_decomposition_given_L()
    ok3 = verify_unconditional()
    print()
    print("=" * 78)
    if ok1 and ok2 and ok3:
        print("ALL CHECKS PASSED: Proposicao S and the K=4 Full Cycle-Count")
        print("Decomposition Theorem hold (instantiated from the general-K")
        print("citation, Estagio 41, and independently re-verified here).")
    else:
        print("SOME CHECKS FAILED -- see above.")
    print("=" * 78)
