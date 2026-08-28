#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check #6: the Key Lemma's strongest claim --
R(B) = q_B REGARDLESS of how the escape weight q_B is internally split
among MULTIPLE DISTINGUISHABLE escape flavors (not just one combined
"DEAD"/A-bundle, which is all Proposition S's own application in Section
2.2 ever actually exercises). This is the part of the Key Lemma's
statement that Proposition S's own raw-enumeration checks (adv_02,
adv_02b, adv_03/front's own) do NOT directly stress-test, since in
Proposition S's application the escape set is always effectively a single
bundle "DEAD-or-land-in-A". Here we build a genuinely different raw
model: B = {0,...,m-1} with weights p_0,...,p_{m-1}, and a SEPARATE set
of E >= 1 distinguishable escape flavors with individual weights
e_1,...,e_E (q_B := sum_j e_j). A "dest"-type function is drawn on B,
landing in B union {flavor_1,...,flavor_E}, i.i.d. per node with weights
(p_0,...,p_{m-1},e_1,...,e_E). R(B) := P(no node of B cyclic, where
landing in ANY escape flavor is absorbing/equivalent). Checked, via raw
(m+E)^m enumeration, symbolically free in ALL of p_0..p_{m-1},e_1..e_E,
for several (m,E) combinations, that R(B) depends ONLY on q_B:=sum e_j
(not on the individual e_j's), and equals exactly 1 - sum p_b.
"""
import itertools
import sympy as sp


def R_B_raw(m, E, ps, es):
    """ps: list of m symbols/values, es: list of E symbols/values.
    Domain per node: 0..m-1 (members of B) or ('ESC', j) for j in 0..E-1.
    R(B) = sum over all (m+E)^m raw dest assignments of weight, restricted
    to assignments where NO node of {0,...,m-1} is cyclic (landing in any
    ESC flavor treated as absorbing)."""
    domain = list(range(m)) + [('ESC', j) for j in range(E)]
    weight_of = {i: ps[i] for i in range(m)}
    for j in range(E):
        weight_of[('ESC', j)] = es[j]

    total = 0
    for dest in itertools.product(domain, repeat=m):
        # cyclicity check: iterate dest from each node, ESC absorbs
        any_cyclic = False
        for start in range(m):
            cur = start
            seen = set()
            while True:
                if isinstance(cur, tuple):  # hit an ESC flavor
                    break
                if cur in seen:
                    if cur == start:
                        any_cyclic = True
                    break
                seen.add(cur)
                cur = dest[cur]
            if any_cyclic:
                break
        if not any_cyclic:
            w = 1
            for s in range(m):
                w *= weight_of[dest[s]]
            total += w
    return sp.expand(total)


def check(m, E, label=""):
    """IMPORTANT (self-caught, see adv_06_normalization_note.log): R(B) is
    a PROBABILITY (P(no node of B cyclic)), which only makes sense, and
    only satisfies R(B)=q_B, when the weights are NORMALIZED -- i.e.
    p_0+...+p_{m-1}+e_0+...+e_{E-1} = 1 (the total categorical probability
    over B's true domain, B union the escape flavors). This is not an
    extra assumption smuggled in: q_B is DEFINED as 1-P_B, so P_B+q_B=1
    holds by definition whenever q_B is a single lumped quantity; but when
    q_B is split into E>=2 separately-named flavors e_0..e_{E-1} with
    q_B:=sum(e_j), normalization must be imposed EXPLICITLY as a
    constraint (substituting one e_j as dependent), exactly mirroring the
    front's own disclosed normalization caveat for Proposition S/p_D
    (ATTEMPT.md Section 2.5c) -- generalized here to the multi-flavor Key
    Lemma statement, which that caveat's own text does not explicitly
    re-confirm for E>=2. An UNNORMALIZED version of this exact check was
    run first and found nonzero residuals for every (m,E) tried (see
    adv_06_UNNORMALIZED_negative_control.log) -- expected, not a bug,
    exactly analogous to the front's own documented negative control."""
    ps = list(sp.symbols(f'p0:{m}'))
    P_B = sum(ps)
    es_free = list(sp.symbols(f'e0:{max(E-1,0)}'))  # E-1 free escape weights
    if E >= 1:
        # TRUE normalization: the LAST escape flavor is the fully
        # dependent quantity making sum(p)+sum(e) = 1 EXACTLY (not merely
        # sum(e) = some other free symbol) -- this is what "q_B := 1-P_B"
        # actually means when q_B is split among E flavors.
        e_last = (1 - P_B) - sum(es_free)
        es = es_free + [e_last]
    else:
        es = []

    R = R_B_raw(m, E, ps, es)
    predicted = sp.expand(1 - P_B)
    diff_direct = sp.expand(R - predicted)
    ok_direct = (diff_direct == 0)

    # Split-invariance: recompute with a genuinely DIFFERENT split of the
    # SAME total escape weight (1-P_B) among the E flavors (make e_0 the
    # dependent one instead of e_last) and confirm R is UNCHANGED -- the
    # actual multi-flavor-independence claim, correctly normalized this
    # time.
    if E >= 2:
        es_alt_free = list(sp.symbols(f'f1:{E}'))  # E-1 free symbols f1..f_{E-1}
        e0_alt = (1 - P_B) - sum(es_alt_free)
        es_alt = [e0_alt] + es_alt_free
        R_alt = R_B_raw(m, E, ps, es_alt)
        diff_alt = sp.expand(R_alt - predicted)
        ok_alt = (diff_alt == 0)
    else:
        diff_alt = sp.Integer(0)
        ok_alt = True

    all_ok = ok_direct and ok_alt
    print(f"[{label}] m={m} (|B|), E={E} (# escape flavors), TRUE "
          f"normalization (last flavor = (1-P_B)-sum(other flavors)): "
          f"R(B) - (1-P_B) = {diff_direct}  [{'OK' if ok_direct else 'FAIL'}]; "
          f"alternate split (different flavor dependent): "
          f"R_alt - (1-P_B) = {diff_alt}  [{'OK' if ok_alt else 'FAIL'}]")
    return all_ok


def check_unnormalized_negative_control(m, E, label=""):
    """Deliberate NEGATIVE CONTROL (mirrors ATTEMPT.md's own Section 2.5c
    negative control for Proposition S): run the SAME check WITHOUT
    imposing normalization (p's and e's all genuinely free, unconstrained)
    and confirm it correctly FAILS (nonzero residual) -- demonstrating the
    earlier failing run above was due to missing normalization, not a
    flaw in the Key Lemma itself."""
    ps = list(sp.symbols(f'p0:{m}'))
    es = list(sp.symbols(f'e0:{E}'))
    R = R_B_raw(m, E, ps, es)
    P_B = sum(ps)
    diff = sp.expand(R - (1 - P_B))
    print(f"[{label}] m={m}, E={E}, UNNORMALIZED (no constraint sum p+sum e=1): "
          f"R(B)-(1-P_B) = {'0 (unexpected!)' if diff == 0 else 'nonzero, as expected'}")
    return diff != 0  # returns True (test "passes") iff we correctly see a mismatch


if __name__ == '__main__':
    print("=" * 78)
    print("Key Lemma R(B)=q_B, MULTI-FLAVOR escape stress test (E>=2 distinct")
    print("escape flavors, not just one bundled DEAD/A-escape target) --")
    print("this specifically targets the Key Lemma's strongest claim: R(B)")
    print("'regardless of how the escape weight is internally distributed")
    print("among the individual escape flavors' (ATTEMPT.md Section 2.3)")
    print("=" * 78)
    print()
    print("--- Negative control (unnormalized, should correctly FAIL) ---")
    neg_ok = True
    neg_ok &= check_unnormalized_negative_control(2, 2, "m=2,E=2 unnormalized")
    neg_ok &= check_unnormalized_negative_control(3, 2, "m=3,E=2 unnormalized")
    print("Negative control behaves as expected:", neg_ok)
    print()
    print("--- Main check (correctly normalized) ---")
    all_ok = True
    all_ok &= check(1, 1, "m=1,E=1 (baseline, single flavor)")
    all_ok &= check(1, 2, "m=1,E=2")
    all_ok &= check(2, 1, "m=2,E=1")
    all_ok &= check(2, 2, "m=2,E=2")
    all_ok &= check(2, 3, "m=2,E=3")
    all_ok &= check(3, 2, "m=3,E=2")
    all_ok &= check(3, 3, "m=3,E=3")
    all_ok &= check(4, 2, "m=4,E=2")
    print()
    print("OVERALL:", "ALL PASS" if (all_ok and neg_ok) else "FAILURE DETECTED")
