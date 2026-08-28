"""
BONUS, secondary (per the mandate: "do NOT attempt the full symbolic-in-K
CDF derivation unless [Prop S + Decomposition Theorem] close easily and you
have significant time left; the PRIMARY target is the K-general
Decomposition Theorem and P(S=A) formula"). This script demonstrates only
that the conditional CDF P(T<=k | L_0,...,L_{K-1}) IS algorithmically
computable in closed algebraic form for general K, by directly generalizing
Estagio 40's K=3 Section 3 formula:

    P(T<=k | L) = sum_{A subseteq {0,...,K-1}} P(S=A | L) *
                  P(O + sum_{s in A} V_s <= k),

where, given S=A, the V_s (s in A) are independent Uniform{1,...,L_s} (the
Decomposition Theorem, PROVED general-K in Section 3 of ATTEMPT.md), so the
inner probability is an elementary |A|-fold lattice-point count -- computed
here by direct enumeration for concrete small L (exact, no shortcut),
NOT via a symbolic-in-(n,K) closed form (that is explicitly NOT attempted
here, and remains open -- see ATTEMPT.md Section 5).

This is included only to demonstrate that Proposition S + the Decomposition
Theorem TOGETHER give, in principle, an algorithmic route to the K-general
conditional CDF -- exactly as claimed in ATTEMPT.md Section 4 -- verified
here against the SAME from-scratch position-level reduced model used in
decomposition_theorem_position_level.py, for several small concrete
(K, L, O). It is NOT a claim that a closed-form-in-(n,K) CDF (Estagio 40
Section 3-4's K=3 achievement, generalized) has been derived here.

No code from any other front in this lineage was read or used.
"""
import itertools
from fractions import Fraction


def prop_s(A, L, O, n):
    m = len(A)
    fact = 1
    for i in range(1, m + 1):
        fact *= i
    prod = Fraction(1)
    for a in A:
        prod *= Fraction(L[a], n)
    PA = sum(Fraction(L[a], n) for a in A)
    pD = Fraction(O, n)
    return fact * prod * (pD + PA)


def lattice_count_le(Ls, threshold):
    """#{(v_1,...,v_m) : 1<=v_i<=L_i, sum v_i <= threshold} / prod(L_i),
    by direct enumeration (exact, small-L only -- this is a demonstration,
    not a scalable algorithm)."""
    if not Ls:
        return Fraction(1) if threshold >= 0 else Fraction(0)
    total = 0
    count = 0
    ranges = [range(1, L + 1) for L in Ls]
    for combo in itertools.product(*ranges):
        count += 1
        if sum(combo) <= threshold:
            total += 1
    return Fraction(total, count)


def conditional_cdf_general_k(K, L, O, k):
    n = O + sum(L)
    total = Fraction(0)
    for r in range(0, K + 1):
        for A in itertools.combinations(range(K), r):
            pA = prop_s(A, L, O, n)
            Ls_A = [L[a] for a in A]
            thresh = k - O
            frac = lattice_count_le(Ls_A, thresh)
            total += pA * frac
    return total


def ground_truth_cdf_position_level(K, L, O, k):
    """Independent ground truth: build the SAME position-level reduced
    model as decomposition_theorem_position_level.py (fresh here, not
    imported), enumerate all n^K raw target choices, compute T exactly for
    each, and return the exact fraction with T<=k."""
    n = O + sum(L)
    slots = []
    for s in range(K):
        for i in range(1, L[s] + 1):
            slots.append((s, i))
    for _ in range(O):
        slots.append('OUT')
    assert len(slots) == n

    count_le = 0
    total = 0
    for target_choice in itertools.product(slots, repeat=K):
        successor = {}
        for s in range(K):
            for i in range(1, L[s]):
                successor[(s, i)] = (s, i + 1)
            successor[(s, L[s])] = target_choice[s]
        all_positions = [(s, i) for s in range(K) for i in range(1, L[s] + 1)]
        cyc = set()
        for start in all_positions:
            seen = []
            cur = start
            while True:
                if cur == 'OUT':
                    break
                if cur in seen:
                    if cur == start:
                        cyc.add(start)
                    break
                seen.append(cur)
                cur = successor[cur]
        T = O + len(cyc)
        total += 1
        if T <= k:
            count_le += 1
    return Fraction(count_le, total)


def main():
    print("=" * 78)
    print("BONUS (secondary): general-K conditional CDF machinery demo")
    print("=" * 78)
    configs = [
        ((2, 2), 1, 2),
        ((3, 1), 0, 2),
        ((2, 1, 2), 1, 3),
        ((1, 1, 1, 1), 0, 4),
    ]
    all_ok = True
    for L, O, K in configs:
        n = O + sum(L)
        for k in range(0, n + 1):
            pred = conditional_cdf_general_k(K, L, O, k)
            truth = ground_truth_cdf_position_level(K, L, O, k)
            ok = (pred == truth)
            all_ok &= ok
            status = 'OK' if ok else 'MISMATCH'
            print(f"K={K} L={L} O={O} n={n} k={k}: predicted={pred} "
                  f"truth={truth}  [{status}]")
    print()
    print("ALL MATCH" if all_ok else "MISMATCH FOUND")
    print()
    print("(Demonstration only: this shows Prop S + Decomposition Theorem")
    print(" TOGETHER algorithmically produce the exact conditional CDF for")
    print(" any concrete K, L. A single elementary closed-form-in-(n,K) CDF")
    print(" -- the K-general analogue of Estagio 40's Proposicao D3 -- is")
    print(" NOT attempted here; see ATTEMPT.md Section 5 for why this is")
    print(" correctly out of primary scope for this front.)")


if __name__ == "__main__":
    main()
