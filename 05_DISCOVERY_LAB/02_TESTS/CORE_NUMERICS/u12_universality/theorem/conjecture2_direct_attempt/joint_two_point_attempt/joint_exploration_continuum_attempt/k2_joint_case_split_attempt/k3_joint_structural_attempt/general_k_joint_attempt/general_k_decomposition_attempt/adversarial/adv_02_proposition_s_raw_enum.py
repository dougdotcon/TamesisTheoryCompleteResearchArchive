#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check #2: Proposition S, general K, verified
against the raw (K+1)^K destination-table model, fully symbolic (free
p_0,...,p_{K-1}), K=0..5 -- matching the front's own claimed fully-
symbolic reach (its script claims K=0..5 free-symbolic, K=6/7 only at
concrete rational weights). K=6 was ALSO attempted fully symbolically
here (an adversarial attempt to push one step beyond the front's own
symbolic reach) but the naive sp.expand-accumulate-every-term approach
did not finish within a 580s budget for the 117,649-term sum with degree-6
symbolic polynomials re-expanded at every step; it was killed rather than
left to run unbounded (disclosed, not silently dropped). K=6 and K=7 are
instead confirmed at CONCRETE generic rational weights, exact Fraction
arithmetic (adv_02b_proposition_s_k6_concrete.py), matching the front's
own claimed reach for those K exactly.

Model (from ATTEMPT.md Section 1.2/2.1, prose only): destinations
dest(0),...,dest(K-1) are i.i.d. categorical on {0,...,K-1,DEAD} with
weights p_0,...,p_{K-1},p_D (p_D = 1 - sum p_i). For each of the
(K+1)^K raw destination assignments, weight = product of the K
individual categorical probabilities. S(dest) := {s : s is "cyclic",
i.e. iterating dest from s returns to s before hitting DEAD} is computed
by DIRECT FORWARD SIMULATION (no shortcut, no bijection-based short cut).

Proposition S claim to check:
    P(S=A) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)

for every A subseteq {0,...,K-1}, every K.
"""
import itertools
import sympy as sp


def cyclic_set(dest, K):
    """dest: tuple of length K, dest[s] in {0,...,K-1,'DEAD'}.
    Returns S = set of s in {0,...,K-1} that are cyclic (iterating dest
    from s returns to s before hitting DEAD), by direct forward
    simulation -- no algebraic shortcut."""
    S = set()
    for s in range(K):
        cur = s
        seen = set()
        cyclic = False
        while True:
            if cur == 'DEAD':
                cyclic = False
                break
            if cur in seen:
                cyclic = (cur == s)  # returned to s before repeating anything else,
                # but since out-degree 1 everywhere, the first repeat must be s
                # itself if s is on a cycle
                break
            seen.add(cur)
            cur = dest[cur]
        if cyclic:
            S.add(s)
    return frozenset(S)


def check_K(K, verbose=True):
    ps = list(sp.symbols(f'p0:{K}'))
    pD = 1 - sum(ps)
    weight_of = {}
    for i in range(K):
        weight_of[i] = ps[i]
    weight_of['DEAD'] = pD

    domain = list(range(K)) + ['DEAD']
    # raw enumeration over all (K+1)^K destination tuples
    empirical = {}
    total_check = 0
    for dest in itertools.product(domain, repeat=K):
        w = 1
        for s in range(K):
            w *= weight_of[dest[s]]
        S = cyclic_set(dest, K)
        empirical[S] = sp.expand(empirical.get(S, 0) + w)
        total_check += 1

    assert total_check == (K + 1) ** K

    # sanity: probabilities sum to 1
    total_prob = sp.expand(sum(empirical.values()))
    total_prob_simplified = sp.simplify(total_prob - 1)
    assert total_prob_simplified == 0, f"K={K}: empirical probabilities do not sum to 1! residual={total_prob_simplified}"

    all_ok = True
    mismatches = []
    for A_tuple in itertools.chain.from_iterable(
            itertools.combinations(range(K), r) for r in range(K + 1)):
        A = frozenset(A_tuple)
        m = len(A)
        prod_A = 1
        for a in A:
            prod_A *= ps[a]
        sum_A = sum(ps[a] for a in A)
        predicted = sp.factorial(m) * prod_A * (pD + sum_A)
        predicted = sp.expand(predicted)
        emp = empirical.get(A, sp.Integer(0))
        diff = sp.simplify(sp.expand(emp - predicted))
        ok = (diff == 0)
        all_ok &= ok
        if not ok:
            mismatches.append((A, diff))

    print(f"K={K}: raw enumeration size (K+1)^K = {(K+1)**K}, "
          f"num distinct S values observed = {len(empirical)}, "
          f"probabilities sum to 1: OK, "
          f"Proposition S match over all {2**K} subsets A: "
          f"{'ALL OK' if all_ok else 'MISMATCHES: ' + str(mismatches)}")
    return all_ok


if __name__ == '__main__':
    print("=" * 78)
    print("Proposition S vs raw (K+1)^K destination-table enumeration,")
    print("fully symbolic free weights p_0,...,p_{K-1} (p_D = 1-sum), K=0..5")
    print("(matches the front's own claimed fully-symbolic reach; the session's")
    print(" own pre-dispatch spot-check only went to K=4). K=6/7 continued at")
    print(" concrete rational weights in adv_02b_proposition_s_k6_concrete.py.")
    print("=" * 78)
    all_ok = True
    for K in range(0, 6):
        all_ok &= check_K(K)
    print()
    print("OVERALL:", "ALL K PASS" if all_ok else "FAILURE DETECTED")
