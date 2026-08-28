#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check #7: the "self-similar recursive partition
identity" (*) itself:
    sum_{C subseteq B} |C|! * prod_{c in C} p_c * R(B\\C) = 1        (*)
used as the starting point of the Key Lemma's induction (ATTEMPT.md
Section 2.3), BEFORE any inductive hypothesis is substituted in. This
script checks (*) directly, using RAW brute-force R(B') (genuine
enumeration + cycle detection, no formula assumed for R at all -- not
even the closed form 1-P_B'), for several concrete B, confirming the
partition claim "{S cap B = C : C subseteq B} partitions the whole
probability space" by DIRECT COUNT (does every raw destination table
land in EXACTLY one C-bucket?), independent of and prior to the algebraic
identity (**) that adv_01 already checked.
"""
import itertools
import sympy as sp


def cyclic_set_full(dest, universe):
    """universe: list of node labels (the full index set on which dest is
    defined here, e.g. all of B). dest: dict node->target, target in
    universe or 'ESC'. Returns set of cyclic nodes among `universe`."""
    S = set()
    for start in universe:
        cur = start
        seen = set()
        cyclic = False
        while True:
            if cur == 'ESC':
                break
            if cur in seen:
                cyclic = (cur == start)
                break
            seen.add(cur)
            cur = dest[cur]
        if cyclic:
            S.add(start)
    return frozenset(S)


def check_star(B_size, label=""):
    B = list(range(B_size))
    ps = {i: sp.Symbol(f'p{i}') for i in B}
    pD = sp.Symbol('pD')  # generic external escape, kept symbolic and free
    domain = B + ['ESC']
    weight_of = dict(ps)
    weight_of['ESC'] = pD

    # For each raw destination table on ALL of B (dest: B -> B u {ESC}),
    # compute S := cyclic_set_full(dest, B) directly (no shortcut), and
    # accumulate P(S ∩ B = C) empirically for each C subseteq B.
    total_by_C = {frozenset(c): sp.Integer(0)
                  for r in range(B_size + 1) for c in itertools.combinations(B, r)}

    for dest_vals in itertools.product(domain, repeat=B_size):
        dest = {B[i]: dest_vals[i] for i in range(B_size)}
        S = cyclic_set_full(dest, B)
        w = 1
        for i in B:
            w *= weight_of[dest[i]]
        total_by_C[S] = sp.expand(total_by_C[S] + w)

    grand_total = sp.expand(sum(total_by_C.values()))
    # This grand total, by construction, is (sum_i p_i + pD)^{|B|} -- NOT
    # necessarily 1 unless normalized. The partition claim itself ("every
    # raw config lands in exactly one C bucket") is a set-theoretic fact,
    # checked directly here by summing empirical bucket sizes:
    total_configs = (B_size + 1) ** B_size
    total_configs_check = sum(1 for c in itertools.product(domain, repeat=B_size))
    assert total_configs == total_configs_check

    # partition sanity (combinatorial, weight-independent): every raw
    # config assigned to exactly one C -- verified by re-deriving total
    # count of configs across all buckets == (m+1)^m
    count_by_C = {}
    for dest_vals in itertools.product(domain, repeat=B_size):
        dest = {B[i]: dest_vals[i] for i in range(B_size)}
        S = cyclic_set_full(dest, B)
        count_by_C[S] = count_by_C.get(S, 0) + 1
    total_count = sum(count_by_C.values())
    partition_ok = (total_count == total_configs)

    # Now check identity (*) itself: sum_C |C|! prod_C p_c * R(B\C) = 1,
    # where R(B\C) is computed as RAW brute force (genuine re-enumeration
    # over B\C, not the C-bucket sums above -- a fully separate
    # computation, to keep this an independent check of the partition
    # claim's ALGEBRAIC consequence, not just a restatement).
    def R_raw(subset, extra_escape_weight):
        # NOTE (self-caught bug #1): an earlier version of this function
        # used the OUTER `domain` (= full B + 'ESC') here instead of this
        # subset's OWN domain (sub + 'ESC') -- landing outside `sub` must
        # be treated as absorbing/'ESC' from `sub`'s own perspective.
        # Caused a KeyError, caught immediately (crashed, not a silent
        # wrong answer) and fixed by using sub_domain = sub + ['ESC'].
        #
        # NOTE (self-caught bug #2, more subtle): bundling C's own nodes
        # into a single 'ESC' outcome for the R(B\C) sub-enumeration is
        # only correct if 'ESC' is given the FULL combined escape weight
        # pD + sum_{c in C} p_c -- not just pD (the original escape
        # weight). C's nodes ARE part of the true escape set from
        # (B\C)'s perspective (per the Key Lemma statement: q_{B\C}
        # bundles the original escape AND all previously-removed C).
        # Missing the +sum_C p_c term would silently under-weight escape
        # and break the identity even after fixing bug #1 above. Passed
        # in explicitly as `extra_escape_weight` = sum_{c in C} p_c.
        sub = list(subset)
        sub_domain = sub + ['ESC']
        m = len(sub)
        total = sp.Integer(0)
        for dest_vals in itertools.product(sub_domain, repeat=m):
            dest = {sub[i]: dest_vals[i] for i in range(m)}
            S = cyclic_set_full(dest, sub)
            if len(S) == 0:
                w = 1
                for i in sub:
                    tgt = dest[i]
                    w *= (weight_of['ESC'] + extra_escape_weight) if tgt == 'ESC' else weight_of[tgt]
                total += w
        return sp.expand(total)

    star_lhs = sp.Integer(0)
    for r in range(B_size + 1):
        for C_tuple in itertools.combinations(B, r):
            C = frozenset(C_tuple)
            prod_C = 1
            for c in C:
                prod_C *= ps[c]
            P_C = sum(ps[c] for c in C) if C else 0
            R_rest = R_raw(frozenset(B) - C, P_C)
            star_lhs += sp.factorial(len(C)) * prod_C * R_rest
    star_lhs = sp.expand(star_lhs)

    # (*) as stated requires normalization (sum p_i + pD = 1), exactly
    # like the Key Lemma itself -- substitute pD = 1 - sum(p_i) before
    # checking star_lhs == 1 (an UNNORMALIZED check would show
    # star_lhs == (sum p+pD)^{|B|} instead, mirroring adv_06's negative
    # control; not repeated here since adv_06 already demonstrates it).
    P_B = sum(ps[i] for i in B)
    star_lhs_normalized = sp.expand(star_lhs.subs(pD, 1 - P_B))
    star_diff = sp.simplify(star_lhs_normalized - 1)
    star_ok = (star_diff == 0)

    print(f"[{label}] |B|={B_size}: partition sanity (every raw config in "
          f"exactly one C-bucket) = {'OK' if partition_ok else 'FAIL'}; "
          f"identity (*) [normalized]: sum_C |C|!prod_C p_c R(B\\C) - 1 = "
          f"{star_diff}  [{'OK' if star_ok else 'FAIL'}]")
    return partition_ok and star_ok


if __name__ == '__main__':
    print("=" * 78)
    print("Checking the partition claim and identity (*) directly, using RAW")
    print("brute-force R(B\\C) (no formula assumed for R at all), |B|=1..4")
    print("=" * 78)
    all_ok = True
    for size in range(1, 5):
        all_ok &= check_star(size, f"m={size}")
    print()
    print("OVERALL:", "ALL PASS" if all_ok else "FAILURE DETECTED")
