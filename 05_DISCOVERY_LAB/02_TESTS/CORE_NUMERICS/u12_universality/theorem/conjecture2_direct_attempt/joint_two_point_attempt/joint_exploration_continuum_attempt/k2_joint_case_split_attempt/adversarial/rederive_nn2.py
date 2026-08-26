"""
Independent re-derivation of Proposition NN2 (P_nn(n,2) closed form) from
Lemma 1 + Lemma 2 alone (both already independently verified by brute force
in lemma1_ref.py / lemma2_ref.py), WITHOUT using the target document's own
stated T(p,q) formula -- we build our own "value(role1,role2)" case split
from scratch (outside-outside / outside-arc / same-arc / cross-arc), sum it
over all (p,q) and all ordered role pairs using exact Fraction arithmetic
(a direct nested loop, not the document's sympy closed-form summation), and
compare the resulting P_nn(n,2) to Proposition NN2's claimed closed form
(10n^2+7n+2)/(30n^2).

This checks the DERIVATION MECHANISM (mandate item 6: work through the
case-split myself, confirm no case is missed/double-counted), not just the
final numeric answer (which brute_k2_ref.py already confirms independently
via full Definition-4 enumeration).
"""
from fractions import Fraction


def value(role1, role2, n, p, q):
    """
    role: ('outside',) or ('arc1', i) or ('arc2', i), i in 1..p-1 or 1..q-1.
    Returns P(both roles' points cyclic), using Lemma 2's (R1)-(R5)
    (independently verified in lemma2_ref.py) and the trivial fact
    'outside' points are always cyclic (Prop 4 Step 2 / this doc's Sec 3.1).
    """
    t1, t2 = role1[0], role2[0]
    if t1 == 'outside' and t2 == 'outside':
        return Fraction(1)
    if t1 == 'outside' and t2 == 'arc1':
        i = role2[1]
        return Fraction(i * (n + q), n * n)          # R1
    if t1 == 'outside' and t2 == 'arc2':
        i = role2[1]
        return Fraction(i * (n + p), n * n)           # R2
    if t1 == 'arc1' and t2 == 'outside':
        i = role1[1]
        return Fraction(i * (n + q), n * n)           # R1
    if t1 == 'arc2' and t2 == 'outside':
        i = role1[1]
        return Fraction(i * (n + p), n * n)           # R2
    if t1 == 'arc1' and t2 == 'arc1':
        i, ip = role1[1], role2[1]
        return Fraction(min(i, ip) * (n + q), n * n)  # R3
    if t1 == 'arc2' and t2 == 'arc2':
        i, ip = role1[1], role2[1]
        return Fraction(min(i, ip) * (n + p), n * n)  # R4
    if t1 == 'arc1' and t2 == 'arc2':
        i, ip = role1[1], role2[1]
        return Fraction(2 * i * ip, n * n)            # R5
    if t1 == 'arc2' and t2 == 'arc1':
        i, ip = role1[1], role2[1]
        return Fraction(2 * i * ip, n * n)            # R5 (symmetric)
    raise ValueError((role1, role2))


def T_pq_direct(n, p, q):
    """Direct enumeration of T(p,q) = sum over ALL ordered pairs of distinct
    roles among the n-2 non-source positions, of value(role1,role2)."""
    O = n - p - q
    roles = [('outside',)] * 0  # placeholder; build list of distinct role objects
    role_list = []
    for _ in range(O):
        role_list.append(('outside',))
    for i in range(1, p):
        role_list.append(('arc1', i))
    for i in range(1, q):
        role_list.append(('arc2', i))
    assert len(role_list) == n - 2, (n, p, q, len(role_list))

    total = Fraction(0)
    m = len(role_list)
    for a in range(m):
        for b in range(m):
            if a == b:
                continue
            total += value(role_list[a], role_list[b], n, p, q)
    return total


def P_nn2_direct(n, verbose=True):
    """Full double sum over (p,q) with p,q>=1,p+q<=n, using our own T_pq_direct."""
    total = Fraction(0)
    npairs = 0
    for p in range(1, n):
        for q in range(1, n - p + 1):
            Tpq = T_pq_direct(n, p, q)
            total += Tpq
            npairs += 1
    # average over (p,q) uniform on C(n,2) pairs, then average over role assignment
    n_pq_pairs = n * (n - 1) // 2
    assert npairs == n_pq_pairs, (npairs, n_pq_pairs)
    Pnn2 = (Fraction(2, n * (n - 1))) * total / ((n - 2) * (n - 3))
    if verbose:
        print(f"n={n}: direct re-derivation P_nn(n,2) = {Pnn2} ({float(Pnn2):.6f})")
    return Pnn2


def proposition_nn2_formula(n):
    return Fraction(10 * n * n + 7 * n + 2, 30 * n * n)


if __name__ == "__main__":
    print("Independent re-derivation of Proposition NN2 from Lemma 1 + Lemma 2 alone")
    print("(own case-split code, NOT the document's sympy summation), compared to")
    print("the document's claimed closed form (10n^2+7n+2)/(30n^2):\n")
    all_match = True
    for n in range(4, 13):
        got = P_nn2_direct(n, verbose=False)
        predicted = proposition_nn2_formula(n)
        match = (got == predicted)
        all_match = all_match and match
        print(f"  n={n:2d}: re-derived={got} ({float(got):.6f})  "
              f"Prop.NN2 formula={predicted} ({float(predicted):.6f})  "
              f"{'MATCH' if match else 'MISMATCH'}")
    print()
    print("ALL MATCH" if all_match else "MISMATCHES FOUND")
