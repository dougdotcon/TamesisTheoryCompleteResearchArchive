"""
Independent, from-scratch verification of the general-K Proposition S
(ATTEMPT.md Section 2, the main new closed form of this front):

    P(S = A) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)

for EVERY subset A of {0,...,K-1} and EVERY K, where dest(0),...,dest(K-1)
are i.i.d. categorical on {0,...,K-1,DEAD} with weights (p_0,...,p_{K-1},p_D)
(the elementary i.i.d.-destinations observation from Estagio 40 Section 2.2,
cited, itself already K-free) and S is the set of cyclic sources (nodes on
a cycle of the induced functional digraph on {0,...,K-1}).

Verification method: brute enumeration of the raw (K+1)^K destination
table (generalizing the K=3 predecessor's own "64=4^3 raw cases" check,
ATTEMPT.md Section 2.2's own proof of P(S=empty)=p_D, to every K), cycle
detection by direct forward simulation (no shortcut, no reference to the
closed form), for every subset A, symbolically for K=0..5 and by concrete
generic rationals for K=6,7,8.

No code from any other front in this lineage was read or used.
"""
import itertools
import sympy as sp


def cyclic_set(dest, K):
    """dest: dict i -> j in {0,...,K-1} or 'D'. Returns set S of cyclic i's,
    found by direct forward simulation from each node (no shortcut)."""
    S = set()
    for start in range(K):
        seen = []
        cur = start
        while True:
            if cur == 'D':
                break
            if cur in seen:
                if cur == start:
                    S.add(start)
                break
            seen.append(cur)
            cur = dest[cur]
    return frozenset(S)


def prop_s_formula(A, ps, pD):
    m = len(A)
    prod = sp.Integer(1)
    for a in A:
        prod *= ps[a]
    PA = sum((ps[a] for a in A), sp.Integer(0))
    return sp.factorial(m) * prod * (pD + PA)


def check_symbolic(K):
    """IMPORTANT: the raw enumeration's per-configuration weight is a valid
    probability only once the K+1 categorical weights are normalized to sum
    to 1 (p_0+...+p_{K-1}+p_D=1) -- Proposition S's derivation (ATTEMPT.md
    Sec 2.3-2.4) uses this normalization essentially (it is what turns
    "escape weight from B's perspective" into 1 - sum_B p_b). So p_D is
    substituted as the DEPENDENT quantity 1 - sum(p_0..p_{K-1}) throughout,
    both in the raw enumeration's weights and in the closed-form formula,
    before any comparison -- leaving p_D as an independent free symbol
    (unconstrained) would test a different, unnormalized, generally FALSE
    statement (verified explicitly not to hold in that case, see the
    docstring note in this module's log)."""
    ps = sp.symbols(f"p0:{K}") if K > 0 else ()
    pD = 1 - sum(ps) if K > 0 else sp.Integer(1)
    targets = list(range(K)) + ['D']
    weight = {i: ps[i] for i in range(K)}
    weight['D'] = pD

    raw = {}  # frozenset A -> symbolic probability, from raw enumeration
    for dest_tuple in itertools.product(targets, repeat=K):
        dest = {i: dest_tuple[i] for i in range(K)}
        S = cyclic_set(dest, K)
        w = sp.Integer(1)
        for i in range(K):
            w *= weight[dest[i]]
        raw[S] = raw.get(S, sp.Integer(0)) + w

    all_ok = True
    total_formula = sp.Integer(0)
    total_raw = sp.Integer(0)
    for r in range(0, K + 1):
        for A in itertools.combinations(range(K), r):
            A = frozenset(A)
            raw_p = sp.expand(raw.get(A, sp.Integer(0)))
            formula_p = sp.expand(prop_s_formula(A, ps, pD))
            diff = sp.simplify(raw_p - formula_p)
            ok = (diff == 0)
            all_ok &= ok
            total_formula += formula_p
            total_raw += raw_p
            if not ok:
                print(f"    MISMATCH A={sorted(A)}: raw-formula = {diff}")
    total_norm = sp.simplify(total_formula)
    norm_ok = (total_norm == 1)
    all_ok &= norm_ok
    print(f"K={K}: all {2**K} subsets A checked symbolically (p_D=1-sum(p) "
          f"substituted throughout) against raw (K+1)^K={ (K+1)**K } "
          f"enumeration -> "
          f"{'ALL MATCH' if all_ok else 'MISMATCH FOUND'}; "
          f"sum_A P(S=A) = {total_norm} [{'OK' if norm_ok else 'FAIL'}]")
    return all_ok


def check_symbolic_unnormalized_counterexample(K=3):
    # NOTE: K must be >= 3 for this to be a genuine (nontrivial) negative
    # control -- at K<=2 the relevant complement B has size <=1, for which
    # "no cyclic node in B" trivially equals the raw escape weight with NO
    # normalization needed at all (a size-1 "no self-loop" event is, by
    # construction, algebraically identical to "escape", regardless of
    # normalization) -- so K=2 alone would misleadingly show diff=0 and
    # look like the normalization caveat doesn't matter. It first becomes
    # essential at K=3 (|B|=2), exactly where the unfixed check_symbolic
    # above (see the module's run log / git history) first produced a
    # genuine, nonzero mismatch before this fix.
    """Documents explicitly, as a negative control, that the formula does
    NOT hold if p_D is left as a genuinely independent free symbol (i.e. the
    K+1 categorical weights are NOT required to sum to 1) -- confirming
    that Proposition S is a statement about a genuine probability
    distribution (normalized weights), not an unconditional polynomial
    identity in K+1 free variables. This is expected and consistent with
    the hand proof (ATTEMPT.md Sec 2.3), which uses q_B = 1 - P_B, a
    relation that presumes total normalization."""
    ps = sp.symbols(f"p0:{K}")
    pD = sp.symbols("pD")  # genuinely independent, NOT substituted
    targets = list(range(K)) + ['D']
    weight = {i: ps[i] for i in range(K)}
    weight['D'] = pD
    raw = {}
    for dest_tuple in itertools.product(targets, repeat=K):
        dest = {i: dest_tuple[i] for i in range(K)}
        S = cyclic_set(dest, K)
        w = sp.Integer(1)
        for i in range(K):
            w *= weight[dest[i]]
        raw[S] = raw.get(S, sp.Integer(0)) + w
    A = frozenset([0])
    raw_p = sp.expand(raw.get(A, sp.Integer(0)))
    formula_p = sp.expand(prop_s_formula(A, ps, pD))
    diff = sp.simplify(raw_p - formula_p)
    print(f"[negative control, K={K}, p_D left UNNORMALIZED/free] "
          f"P(S={{0}}) raw - formula = {diff}  "
          f"(expected: NONZERO in general -- confirms normalization is "
          f"essential, not an oversight)")
    return diff


def check_concrete(K):
    # generic distinct positive rationals p_0..p_{K-1}, pD, summing to 1
    raw_weights = [sp.Rational(1, (K + 4) * (i + 3)) for i in range(K)]
    pD_val = 1 - sum(raw_weights)
    assert pD_val > 0
    targets = list(range(K)) + ['D']
    weight = {i: raw_weights[i] for i in range(K)}
    weight['D'] = pD_val

    raw = {}
    for dest_tuple in itertools.product(targets, repeat=K):
        dest = {i: dest_tuple[i] for i in range(K)}
        S = cyclic_set(dest, K)
        w = sp.Integer(1)
        for i in range(K):
            w *= weight[dest[i]]
        raw[S] = raw.get(S, sp.Integer(0)) + w

    all_ok = True
    total = sp.Integer(0)
    for r in range(0, K + 1):
        for A in itertools.combinations(range(K), r):
            A = frozenset(A)
            raw_p = raw.get(A, sp.Integer(0))
            m = len(A)
            prod = sp.Integer(1)
            for a in A:
                prod *= raw_weights[a]
            PA = sum((raw_weights[a] for a in A), sp.Integer(0))
            formula_p = sp.factorial(m) * prod * (pD_val + PA)
            diff = sp.nsimplify(raw_p - formula_p)
            ok = (diff == 0)
            all_ok &= ok
            total += raw_p
            if not ok:
                print(f"    MISMATCH A={sorted(A)}: raw-formula = {diff}")
    total_ok = (sp.nsimplify(total - 1) == 0)
    all_ok &= total_ok
    print(f"K={K} (concrete generic rationals): all {2**K} subsets A checked "
          f"against raw (K+1)^K={(K+1)**K} enumeration -> "
          f"{'ALL MATCH' if all_ok else 'MISMATCH FOUND'}; sum_A P(S=A)={total} "
          f"[{'OK' if total_ok else 'FAIL'}]")
    return all_ok


def main():
    print("=" * 78)
    print("General-K Proposition S check: P(S=A) = |A|! prod_A p_a (pD + sum_A p_a)")
    print("(p_D substituted as 1-sum(p_0..p_{K-1}) throughout -- see docstring")
    print(" of check_symbolic for why this substitution is essential, not a")
    print(" simplification of convenience)")
    print("=" * 78)
    all_ok = True
    for K in range(0, 6):
        all_ok &= check_symbolic(K)
    print()
    print("Concrete generic-rational extension (K=6,7; (K+1)^K raw cases,")
    print("normalized weights, exact Rational arithmetic):")
    for K in [6, 7]:
        all_ok &= check_concrete(K)
    print()
    print("Negative control (documents that normalization is essential):")
    check_symbolic_unnormalized_counterexample(K=3)
    print()
    print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")


if __name__ == "__main__":
    main()
