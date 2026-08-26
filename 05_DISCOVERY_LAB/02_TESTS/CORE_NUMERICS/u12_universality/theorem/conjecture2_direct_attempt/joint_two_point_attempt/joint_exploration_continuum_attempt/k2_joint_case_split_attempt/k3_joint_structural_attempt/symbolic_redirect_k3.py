"""
symbolic_redirect_k3.py

Symbolic (exact, sympy.Rational) version of redirect_core_k3.py: derives
P_single and P_joint as exact CLOSED-FORM RATIONAL FUNCTIONS of the
symbols L0,L1,L2,n (and the query position(s) i,i'), rather than numeric
Fractions at concrete integers.

This is the same 64-destination-case reduction as redirect_core_k3.py
(verified there against direct position-level enumeration, and against
brute_force_k3.py ground truth via assemble_pnn3.py) -- reimplemented with
sympy symbols so that the outer sums over arc positions and over
compositions (L0,L1,L2) can be done in closed form (sympy.summation),
producing an actual symbolic derivation of P_nn(n,3), in the same spirit
as the predecessor's symbolic_sum_pnn2.py for K=2.

Key structural facts, established computationally in redirect_core_k3.py's
own case analysis and re-derived here symbolically (both used as
consistency checks against the numeric fits of assemble_pnn3.py):

  - P_single(s,i) is LINEAR in i: exactly one 'constrained' source
    (pred(s)) appears per contributing case, replacing that source's own
    bucket weight (L_target/n) by (i/n) -- so every term is proportional
    to i, with an i-independent coefficient. Hence
    P_single(s,i) = i * A_s(L0,L1,L2,n).

  - P_joint((s,k),(s,k')), k<k' (same arc) = P_single(s,k) = k*A_s
    (the "nearer point's own marginal" fact, matching Lemma 2's (R3),
    verified computationally across many configs, see
    redirect_verify_symbolic.py).

  - P_joint((s,k),(s',k')), s!=s' (different arcs), is BILINEAR in k,k':
    exactly two DISTINCT constrained sources (pred(s), pred(s')) appear
    per contributing case, so every term is proportional to k*k'. Hence
    P_joint((s,k),(s',k')) = k*k'*B_{s,s'}(L0,L1,L2,n).
"""

import sympy as sp

n, L0, L1, L2, i, ip = sp.symbols('n L0 L1 L2 i ip', positive=True)
Lsyms = {0: L0, 1: L1, 2: L2}
O_expr = n - L0 - L1 - L2


def analyze_dest(dest):
    """Same structural logic as redirect_core_k3.analyze_dest -- purely
    combinatorial (doesn't depend on numeric vs symbolic values)."""
    cyclic = {}
    for s in range(3):
        seen = {s}
        x = dest[s]
        steps = 0
        result = False
        while steps < 4:
            if x == 'D':
                result = False
                break
            if x == s:
                result = True
                break
            if x in seen:
                result = False
                break
            seen.add(x)
            x = dest[x]
            steps += 1
        cyclic[s] = result
    pred = {}
    for s in range(3):
        if not cyclic[s]:
            pred[s] = None
            continue
        candidates = [t for t in range(3) if dest[t] == s and cyclic[t]]
        assert len(candidates) == 1
        pred[s] = candidates[0]
    return cyclic, pred


def all_dest_combos():
    from itertools import product
    return list(product([0, 1, 2, 'D'], repeat=3))


def p_single_symbolic(s, query_symbol):
    """Returns exact sympy expression for P(position `query_symbol` in
    ARC(s) cyclic), as a function of L0,L1,L2,n and query_symbol."""
    total = sp.Integer(0)
    for dest in all_dest_combos():
        dest_map = {0: dest[0], 1: dest[1], 2: dest[2]}
        cyclic, pred = analyze_dest(dest_map)
        if not cyclic[s]:
            continue
        p = pred[s]
        w = sp.Integer(1)
        for t in range(3):
            if t == p:
                w *= query_symbol / n
            else:
                target = dest_map[t]
                if target == 'D':
                    w *= O_expr / n
                else:
                    w *= Lsyms[target] / n
        total += w
    return sp.simplify(total)


def p_joint_cross_symbolic(s1, s2, sym1, sym2):
    """s1 != s2. Returns exact sympy expression for
    P((s1,sym1) cyclic AND (s2,sym2) cyclic)."""
    assert s1 != s2
    total = sp.Integer(0)
    for dest in all_dest_combos():
        dest_map = {0: dest[0], 1: dest[1], 2: dest[2]}
        cyclic, pred = analyze_dest(dest_map)
        if not cyclic[s1] or not cyclic[s2]:
            continue
        p1, p2 = pred[s1], pred[s2]
        assert p1 != p2
        constraint = {p1: sym1, p2: sym2}
        w = sp.Integer(1)
        for t in range(3):
            if t in constraint:
                w *= constraint[t] / n
            else:
                target = dest_map[t]
                if target == 'D':
                    w *= O_expr / n
                else:
                    w *= Lsyms[target] / n
        total += w
    return sp.simplify(total)


if __name__ == "__main__":
    A0 = p_single_symbolic(0, i)
    print("P_single(arc0, i) =", A0)
    print("  as i * A0:", sp.simplify(A0 / i))

    A1 = p_single_symbolic(1, i)
    print("P_single(arc1, i) =", A1)

    A2 = p_single_symbolic(2, i)
    print("P_single(arc2, i) =", A2)

    B01 = p_joint_cross_symbolic(0, 1, i, ip)
    print("P_joint(arc0=i, arc1=ip) =", B01)
    print("  as i*ip*B01:", sp.simplify(B01 / (i * ip)))

    B02 = p_joint_cross_symbolic(0, 2, i, ip)
    print("P_joint(arc0=i, arc2=ip) =", B02)

    B12 = p_joint_cross_symbolic(1, 2, i, ip)
    print("P_joint(arc1=i, arc2=ip) =", B12)
