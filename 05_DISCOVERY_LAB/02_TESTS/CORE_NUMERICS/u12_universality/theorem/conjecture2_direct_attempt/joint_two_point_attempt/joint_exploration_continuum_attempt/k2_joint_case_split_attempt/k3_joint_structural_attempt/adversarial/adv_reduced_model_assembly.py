"""
Independent, from-scratch verification of the ASSEMBLY step of
Proposition NN3: combine Lemma 1 (governing-source arc lengths
(L0,L1,L2,O) uniform over compositions of n into 3 positive + 1 nonneg
part) with Lemma 5's closed-form single/cross-arc probabilities to
compute P_nn(n,3) exactly, via exact Fraction arithmetic (own T(L)
formula, independently built, not copied from assemble_pnn3.py), and
compare against the claimed closed form (35n^3+38n^2+23n+6)/(140n^3).

This checks a DIFFERENT thing from adv_raw_brute_k3.py: not whether
Definition 4's raw model matches the formula (already independently
confirmed there), but whether the reduced case-split machinery (Lemma 1
+ Lemma 5, both independently re-verified in adv_lemma1_m3.py /
adv_lemma5_check.py) correctly ASSEMBLES into Proposition NN3 -- i.e.
whether the §4.1 aggregation step itself is correct.

No .py file from any front in the lineage was read.
"""
from fractions import Fraction
import sys


def P_single(pos, L_self, L_a, L_b, n):
    # P(interior position `pos` of an arc with the OTHER two arc lengths
    # L_a, L_b is cyclic) -- L_self unused (formula is independent of it,
    # per Lemma 5 / the "governing-source" fact).
    return Fraction(pos * (2*L_a*L_b + L_a*n + L_b*n + n**2), n**3)


def P_cross(posA, posB, L_other, n):
    # P(interior positions posA in arc A, posB in arc B jointly cyclic),
    # where L_other is the length of the THIRD, uninvolved arc.
    return Fraction(2 * posA * posB * (2*L_other + n), n**3)


def T(L0, L1, L2, n):
    O = n - L0 - L1 - L2
    assert O >= 0

    total = Fraction(0)

    # OO term
    total += Fraction(O * (O - 1))

    # helper: per-arc interior positions
    def interior(Ls):
        return list(range(1, Ls))  # 1..Ls-1

    Ls = {0: L0, 1: L1, 2: L2}
    others = {0: (L1, L2), 1: (L0, L2), 2: (L0, L1)}

    single_sum = {}
    for s in (0, 1, 2):
        La, Lb = others[s]
        s_sum = Fraction(0)
        for pos in interior(Ls[s]):
            s_sum += P_single(pos, Ls[s], La, Lb, n)
        single_sum[s] = s_sum

    # O-arc term (both orders)
    oa = Fraction(0)
    for s in (0, 1, 2):
        oa += single_sum[s]
    total += 2 * O * oa

    # same-arc term (both orders): for arc s, sum over i<i' of P(both)=P(min)
    for s in (0, 1, 2):
        La, Lb = others[s]
        pos_list = interior(Ls[s])
        same = Fraction(0)
        m = len(pos_list)
        for idx, pos in enumerate(pos_list):
            # number of pos' > pos within interior positions after this one
            remaining = m - idx - 1
            same += P_single(pos, Ls[s], La, Lb, n) * remaining
        total += 2 * same

    # cross-arc term, both orders, for each unordered pair {s,t}
    pairs = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]  # (s, t, other-arc-index)
    for s, t, other in pairs:
        Ls_other = Ls[other]
        cross = Fraction(0)
        for i in interior(Ls[s]):
            for j in interior(Ls[t]):
                cross += P_cross(i, j, Ls_other, n)
        total += 2 * cross

    return total


def compositions(n):
    """All (L0,L1,L2) with L0,L1,L2 >= 1 and L0+L1+L2 <= n."""
    for L0 in range(1, n - 1):
        for L1 in range(1, n - L0):
            for L2 in range(1, n - L0 - L1 + 1):
                if L0 + L1 + L2 <= n:
                    yield (L0, L1, L2)


def compute_pnn3_reduced(n):
    from math import comb
    num_compositions = comb(n, 3)
    total_T_over = Fraction(0)
    denom_role_pairs = (n - 3) * (n - 4)
    count_comps = 0
    for (L0, L1, L2) in compositions(n):
        count_comps += 1
        t = T(L0, L1, L2, n)
        total_T_over += t
    assert count_comps == num_compositions, (count_comps, num_compositions)
    result = total_T_over / (num_compositions * denom_role_pairs)
    return result


def claimed(n):
    return Fraction(35*n**3 + 38*n**2 + 23*n + 6, 140*n**3)


if __name__ == '__main__':
    ns = [int(x) for x in sys.argv[1:]] or list(range(6, 21))
    all_ok = True
    for n in ns:
        val = compute_pnn3_reduced(n)
        c = claimed(n)
        ok = (val == c)
        all_ok = all_ok and ok
        print(f"n={n:3d}: reduced-model P_nn = {val}   closed-form = {c}   match={ok}")
    print()
    print(f"REDUCED_MODEL_ASSEMBLY_MATCHES_CLOSED_FORM: {all_ok}")
