"""
INDEPENDENT, FROM-SCRATCH referee check.

Re-implements the "reduced model" T(L) / composition-sum route to P_nn(n,K)
directly from the PROVED Lemma 5 formulas quoted in THEOREM.md Estagio 35
and re-derived in general form by the predecessor front's ATTEMPT.md Sec.4
(general_k_joint_attempt), WITHOUT reading any .py file from any front in
this lineage.

Formulas used (all already PROVED, cited from prose only):

  x_u := L_u / n

  P0(s)        = x_s * sum_{S subseteq Others(s)} |S|! * prod_{u in S} x_u
  P_same(s,s') = x_s*x_s' * sum_{S subseteq M} (|S|+1)! * prod_{u in S} x_u
  P_disjoint(s,s') = x_s*x_s' *
        sum_{S1,S2 subseteq M, S1 cap S2 = empty} |S1|! |S2|! prod_S1 x prod_S2 x
  P_{s,s'} = P_same(s,s') + P_disjoint(s,s')

  (M := {0,...,K-1} \\ {s,s'} , Others(s) := {0,...,K-1} \\ {s})

T(L) := sum over ALL ORDERED PAIRS of distinct "roles" among the n-K
non-source roles (O outside roles, always cyclic; interior positions
1..L_s-1 of each arc s) of P(both roles cyclic | L), built directly and
literally from the "role list" (no algebraic collapse into pieces A/B/C/D
-- that collapse is the TARGET's own construction in its Sec 2.3, and is
independently re-derived and checked separately in piece_bcd_check.py; here
we sidestep it entirely and just brute-loop over role pairs, which is a
strictly more elementary and therefore more trustworthy re-implementation
of the predecessor's own Sec 5.1 description of T(L)):

  - both outside                      : contributes 1
  - outside & interior (s,i)          : contributes P0(s) * i / L_s
  - same arc, (s,i),(s,i'), i != i'   : contributes P0(s) * min(i,i') / L_s
  - different arcs (s,i),(s',i')      : contributes P_{s,s'} * i/L_s * i'/L_{s'}

  P_nn(n,K) = (1 / C(n,K)) * sum_{compositions L, O=n-sum(L)>=0} T(L) / [(n-K)(n-K-1)]

Internally, P0/P_same use an elementary-symmetric-polynomial DP (a standard,
well-known technique -- not read from any front's code) for speed; P_disjoint
is left as a literal brute enumeration over the 3^|M| assignments (this is
the part that would be circular to speed up via the target's own P_same===
P_disjoint bonus identity, so it is deliberately NOT used here -- this
script's P_disjoint computation is fully independent of the target's Claim 1).
"""
import sys
import time
from fractions import Fraction
from itertools import product as iproduct
from math import comb, factorial


def elementary_symmetric_full(Lvals):
    """e_full[k] = sum over k-subsets of Lvals (integers) of the product.
    Pure integer DP, O(K^2)."""
    K = len(Lvals)
    e = [0] * (K + 1)
    e[0] = 1
    for Li in Lvals:
        for k in range(min(len(e) - 1, K), 0, -1):
            e[k] += Li * e[k - 1]
    return e  # length K+1, e[k] integer


def delete_one(e_full, Lremoved, maxk):
    """Given e_full[k] (elementary symmetric of a full multiset) and one
    element value Lremoved that is a member of that multiset, return
    e_rest[k] for k=0..maxk, the elementary symmetric polynomial of the
    multiset with that one element removed. Uses the exact identity
    e_full(t) = e_rest(t) * (1 + Lremoved * t)  =>
    e_rest[k] = e_full[k] - Lremoved * e_rest[k-1]."""
    e_rest = [0] * (maxk + 1)
    e_rest[0] = 1
    for k in range(1, maxk + 1):
        e_rest[k] = e_full[k] - Lremoved * e_rest[k - 1]
    return e_rest


def P0_all(Lvals, n, K):
    """Return list P0[s] for s=0..K-1, each an exact Fraction."""
    e_full = elementary_symmetric_full(Lvals)
    out = []
    for s in range(K):
        e_others = delete_one(e_full, Lvals[s], K - 1)
        num = 0
        # P0(s) = x_s * sum_k k! e_others[k] = (Lvals[s]/n) * sum_k k! e_others[k]/n^k
        # put everything over n^K: num/n^K where
        # num = Lvals[s] * sum_k k! * e_others[k] * n^{K-1-k}
        acc = 0
        for k in range(0, K):
            acc += factorial(k) * e_others[k] * (n ** (K - 1 - k))
        num = Lvals[s] * acc
        out.append(Fraction(num, n ** K))
    return out


def Psame_all_pairs(Lvals, n, K):
    """Return dict {(s,sp): P_same(s,sp)} for s<sp, exact Fraction."""
    e_full = elementary_symmetric_full(Lvals)
    out = {}
    for s in range(K):
        e_no_s = delete_one(e_full, Lvals[s], K - 1)
        for sp in range(s + 1, K):
            e_M = delete_one(e_no_s, Lvals[sp], K - 2)
            acc = 0
            for k in range(0, K - 1):
                acc += factorial(k + 1) * e_M[k] * (n ** (K - 2 - k))
            num = Lvals[s] * Lvals[sp] * acc
            out[(s, sp)] = Fraction(num, n ** K)
    return out


def Pdisjoint_all_pairs(Lvals, n, K):
    """Literal brute double-subset sum over M for every pair (s,sp), s<sp.
    3^(K-2) assignments per pair -- deliberately NOT using the P_same===
    P_disjoint collapse (that is the claim being checked elsewhere, not an
    assumed tool here)."""
    out = {}
    idxs = list(range(K))
    for s in range(K):
        for sp in range(s + 1, K):
            M = [u for u in idxs if u != s and u != sp]
            m = len(M)
            acc_num = 0  # will divide by n^(2 + sum of exponents) at the end per term
            # accumulate per (|S1|,|S2|) to keep pure-integer products
            for assign in iproduct((0, 1, 2), repeat=m):
                if m == 0:
                    S1, S2 = (), ()
                else:
                    S1 = tuple(M[i] for i in range(m) if assign[i] == 1)
                    S2 = tuple(M[i] for i in range(m) if assign[i] == 2)
                prod1 = 1
                for u in S1:
                    prod1 *= Lvals[u]
                prod2 = 1
                for u in S2:
                    prod2 *= Lvals[u]
                term_int = factorial(len(S1)) * factorial(len(S2)) * prod1 * prod2
                k = len(S1) + len(S2)
                acc_num += term_int * (n ** (K - 2 - k))
            num = Lvals[s] * Lvals[sp] * acc_num
            out[(s, sp)] = Fraction(num, n ** K)
    return out


def T_of_L(Lvals, n, K):
    O = n - sum(Lvals)
    assert O >= 0
    P0 = P0_all(Lvals, n, K)
    Psame = Psame_all_pairs(Lvals, n, K)
    Pdis = Pdisjoint_all_pairs(Lvals, n, K)
    Ppair = {}
    for s in range(K):
        for sp in range(s + 1, K):
            Ppair[(s, sp)] = Psame[(s, sp)] + Pdis[(s, sp)]
            Ppair[(sp, s)] = Ppair[(s, sp)]

    total = Fraction(0)
    # Piece A: outside-outside, ordered pairs
    total += Fraction(O * (O - 1))

    # Piece B: outside & interior (both orders) -> factor 2, and sum over s,i
    for s in range(K):
        Ls = Lvals[s]
        if Ls >= 2:
            sum_i = Fraction((Ls - 1) * Ls, 2)  # sum_{i=1}^{Ls-1} i
            total += 2 * O * P0[s] * sum_i / Ls

    # Piece C: same arc, i != i', ordered pairs, min(i,i') governs
    for s in range(K):
        Ls = Lvals[s]
        m = Ls - 1
        if m >= 2:
            # sum_{i != i', 1<=i,i'<=m} min(i,i')  computed by direct double loop
            # (m <= n <= ~16 in our test cases, trivial cost)
            s_min = 0
            for i in range(1, m + 1):
                for ip in range(1, m + 1):
                    if i != ip:
                        s_min += min(i, ip)
            total += P0[s] * Fraction(s_min, Ls)

    # Piece D: cross arc, ordered pairs (s,i),(s',i'), s != s'
    for s in range(K):
        Ls = Lvals[s]
        if Ls < 2:
            continue
        sum_i_s = Fraction((Ls - 1) * Ls, 2)
        for sp in range(K):
            if sp == s:
                continue
            Lsp = Lvals[sp]
            if Lsp < 2:
                continue
            sum_i_sp = Fraction((Lsp - 1) * Lsp, 2)
            total += Ppair[(s, sp)] * (sum_i_s / Ls) * (sum_i_sp / Lsp)

    return total


def gen_compositions(K, n):
    """Yield all K-tuples of positive integers with sum <= n."""
    def rec(prefix, remaining_slots, cap):
        if remaining_slots == 0:
            yield tuple(prefix)
            return
        # need at least 1 per remaining slot
        max_here = cap - (remaining_slots - 1)
        for v in range(1, max_here + 1):
            prefix.append(v)
            yield from rec(prefix, remaining_slots - 1, cap - v)
            prefix.pop()
    yield from rec([], K, n)


def P_nn_reduced(n, K, verbose=False):
    total = Fraction(0)
    count = 0
    for Lvals in gen_compositions(K, n):
        total += T_of_L(Lvals, n, K)
        count += 1
    Cnk = comb(n, K)
    assert count == Cnk, f"composition count mismatch: got {count}, expected C({n},{K})={Cnk}"
    result = total / (Cnk * (n - K) * (n - K - 1))
    if verbose:
        print(f"  n={n} K={K}: {count} compositions, P_nn = {result} = {float(result):.8f}")
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("SELF-CONSISTENCY: reduced model vs already-PROVED closed forms")
    print("=" * 70)

    def K1_formula(n):
        return Fraction(3 * n + 1, 6 * n)

    def K2_formula(n):  # Proposition NN2, Estagio 31
        return Fraction(10 * n ** 2 + 7 * n + 2, 30 * n ** 2)

    def K3_formula(n):  # Proposition NN3, Estagio 35
        return Fraction(35 * n ** 3 + 38 * n ** 2 + 23 * n + 6, 140 * n ** 3)

    def K4_formula(n):  # Proposition NN4, predecessor Sec 6.1 (cited, PROVED)
        return Fraction(126 * n ** 4 + 187 * n ** 3 + 177 * n ** 2 + 98 * n + 24, 630 * n ** 4)

    def K5_formula(n):  # Proposition NN5, predecessor Sec 6.1 (cited, PROVED)
        return Fraction(462 * n ** 5 + 874 * n ** 4 + 1139 * n ** 3 + 989 * n ** 2 + 514 * n + 120, 2772 * n ** 5)

    def K6_formula(n):  # Proposition NN6, predecessor Sec 6.1 (cited, PROVED)
        return Fraction(1716 * n ** 6 + 3958 * n ** 5 + 6616 * n ** 4 + 7933 * n ** 3
                         + 6472 * n ** 2 + 3204 * n + 720, 12012 * n ** 6)

    checks = [
        (1, [4, 5, 6, 7], K1_formula),
        (2, [4, 5, 6], K2_formula),
        (3, [5, 6, 7], K3_formula),
        (4, [6, 7], K4_formula),
        (5, [7, 8], K5_formula),
        (6, [8, 9], K6_formula),
    ]

    all_ok = True
    t0 = time.time()
    for K, ns, formula in checks:
        for n in ns:
            got = P_nn_reduced(n, K)
            want = formula(n)
            ok = (got == want)
            all_ok &= ok
            print(f"K={K} n={n:2d}: reduced-model={got}  cited-closed-form={want}  "
                  f"{'MATCH' if ok else '*** MISMATCH ***'}")
    print(f"\nSelf-consistency K=1..6 elapsed: {time.time()-t0:.2f}s   ALL MATCH: {all_ok}")
    if not all_ok:
        sys.exit(1)

    print()
    print("=" * 70)
    print("K=7, K=8: independent reduced-model enumeration vs target's claimed")
    print("NEW closed forms (ATTEMPT.md Sec 3). The two polynomials below are")
    print("copied verbatim from the target's ATTEMPT.md prose (its own claimed")
    print("formulas), purely so we can compare our independently-computed")
    print("number against them -- no .py file was read to obtain them.")
    print("=" * 70)

    def K7_target_formula(nv):
        num = (6435 * nv**7 + 17548 * nv**6 + 35958 * nv**5 + 55460 * nv**4
               + 62565 * nv**3 + 48628 * nv**2 + 23148 * nv + 5040)
        den = 51480 * nv**7
        return Fraction(num, den)

    def K8_target_formula(nv):
        num = (24310 * nv**8 + 76627 * nv**7 + 186527 * nv**6 + 353609 * nv**5
               + 513865 * nv**4 + 552592 * nv**3 + 412892 * nv**2 + 190224 * nv + 40320)
        den = 218790 * nv**8
        return Fraction(num, den)

    k78_ok = True
    for K, ns, formula in [(7, [9, 11, 13], K7_target_formula), (8, [10, 12], K8_target_formula)]:
        for n in ns:
            t0 = time.time()
            got = P_nn_reduced(n, K)
            dt = time.time() - t0
            want = formula(n)
            ok = (got == want)
            k78_ok &= ok
            print(f"K={K} n={n:2d} (took {dt:6.2f}s): reduced-model = {got}")
            print(f"                          target-formula = {want}")
            print(f"                          {'MATCH (exact)' if ok else '*** MISMATCH ***'}")
    print(f"\nALL K=7/K=8 INDEPENDENT CHECKS MATCH TARGET'S CLAIMED CLOSED FORMS: {k78_ok}")
    if not k78_ok:
        sys.exit(1)
