"""
Independent, from-scratch, RAW-DEFINITION verification of the Key Lemma
(ATTEMPT.md Section 2.3):

    R(B) := P(no node of B lies on a cycle of the functional graph induced
             by an independent random target choice per node, each node
             choosing uniformly at random -- with its OWN weights p_1,...,p_m
             over "land on node j in B" and weight q over "escape") = q,
             i.e. R(B) = q = 1 - sum(p_i), for EVERY finite m and EVERY
             choice of weights p_1,...,p_m,q >= 0 summing to 1.

This script does NOT use the F/G algebra of algebraic_identity_check.py at
all -- it recomputes R(B) from the RAW DEFINITION: enumerate every one of
the (m+1)^m functions dest: {0,...,m-1} -> {0,...,m-1,'ESC'}, detect (by
direct forward simulation, no shortcut) which nodes lie on a cycle, and sum
the weighted probability of "no node cyclic" -- exactly generalizing the
predecessor K=3 front's own "brute symbolic sum over the 64 raw cases"
verification of P(S=empty)=p_D (ATTEMPT.md Section 2.2's proof, which cites
"a direct symbolic sum over all 64 cases confirms equals exactly p_D" as ITS
OWN level of proof for that one fact) -- here done for general m.

No code from any other front in this lineage was read or used.
"""
import itertools
import sympy as sp


def raw_no_cycle_probability_symbolic(m):
    """Symbolic (free p_0..p_{m-1}, q = 1 - sum) computation of R(B) via
    brute enumeration of all (m+1)^m destination functions, cycle-detecting
    each one by direct forward simulation (no algebraic shortcut)."""
    ps = sp.symbols(f"p0:{m}")
    q = 1 - sum(ps)
    targets = list(range(m)) + ['ESC']
    weight = {i: ps[i] for i in range(m)}
    weight['ESC'] = q

    total = sp.Integer(0)
    for dest_tuple in itertools.product(targets, repeat=m):
        dest = {i: dest_tuple[i] for i in range(m)}
        # cycle detection: for each node, forward-simulate until ESC or a repeat
        has_cycle = False
        for start in range(m):
            seen = set()
            cur = start
            while True:
                if cur == 'ESC':
                    break
                if cur in seen:
                    if cur == start:
                        has_cycle = True
                    break
                seen.add(cur)
                cur = dest[cur]
            if has_cycle:
                break
        if not has_cycle:
            w = sp.Integer(1)
            for i in range(m):
                w *= weight[dest[i]]
            total += w
    return sp.expand(total), q


def main():
    print("=" * 78)
    print("Raw-definition check: R(B) computed by brute (m+1)^m enumeration")
    print("with direct cycle detection, compared to the claimed q = 1-sum(p_i)")
    print("=" * 78)
    all_ok = True
    # symbolic (free p_i) for small m: fully general, K-free/size-free proof-level check
    for m in range(0, 6):
        R, q = raw_no_cycle_probability_symbolic(m)
        diff = sp.simplify(sp.expand(R - q))
        ok = (diff == 0)
        all_ok &= ok
        print(f"m={m}: symbolic R(B) - q = {diff}   [{'OK' if ok else 'FAIL'}]  "
              f"(({m+1})^{m}={ (m+1)**m } raw cases enumerated)")

    print()
    print("Concrete-rational extension, m=6,7 (raw enumeration is large; use")
    print("fixed but generic rational weights instead of fully free symbols,")
    print("still EXACT arithmetic, no floating point):")
    for m in [6, 7]:
        # generic distinct rationals summing to < 1
        raw = [sp.Rational(1, (m + 5) * (i + 3)) for i in range(m)]
        s = sum(raw)
        # normalize slightly so sum < 1 strictly (already true by construction)
        ps_vals = raw
        q_val = 1 - s
        targets = list(range(m)) + ['ESC']
        weight = {i: ps_vals[i] for i in range(m)}
        weight['ESC'] = q_val
        total = sp.Integer(0)
        for dest_tuple in itertools.product(targets, repeat=m):
            dest = {i: dest_tuple[i] for i in range(m)}
            has_cycle = False
            for start in range(m):
                seen = set()
                cur = start
                while True:
                    if cur == 'ESC':
                        break
                    if cur in seen:
                        if cur == start:
                            has_cycle = True
                        break
                    seen.add(cur)
                    cur = dest[cur]
                if has_cycle:
                    break
            if not has_cycle:
                w = sp.Integer(1)
                for i in range(m):
                    w *= weight[dest[i]]
                total += w
        diff = sp.nsimplify(total - q_val)
        ok = (diff == 0)
        all_ok &= ok
        print(f"m={m}: concrete R(B) - q = {diff}   [{'OK' if ok else 'FAIL'}]  "
              f"(({m+1})^{m}={(m+1)**m} raw cases enumerated)")

    print()
    print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")


if __name__ == "__main__":
    main()
