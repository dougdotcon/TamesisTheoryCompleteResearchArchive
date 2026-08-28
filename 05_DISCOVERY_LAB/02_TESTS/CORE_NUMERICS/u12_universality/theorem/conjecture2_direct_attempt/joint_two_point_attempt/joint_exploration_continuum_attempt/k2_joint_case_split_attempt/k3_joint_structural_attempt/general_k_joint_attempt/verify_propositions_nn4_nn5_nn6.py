"""
Independent numeric cross-check of Propositions NN4, NN5, NN6 (this
front's new closed forms) against the reduced-model exact computation of
assemble_pnn_general_k.py, at many n values per K, beyond any fitting
range. Also reproduces the ALREADY-PROVED K=1,2,3 closed forms as a
self-consistency floor (Section 5.2 of ATTEMPT.md).
"""
from fractions import Fraction
from assemble_pnn_general_k import P_nn


def predict(coeffs, n):
    # coeffs[j] is the coefficient of 1/n^j, j=0..K
    total = Fraction(0)
    for j, c in enumerate(coeffs):
        total += c / Fraction(n) ** j
    return total


def coeffs_from_numerator(num_high_to_low, den):
    """num_high_to_low[i] is the coefficient of n^{K-i} in the numerator
    (index 0 = coefficient of n^K, index K = coefficient of n^0), so that
    P_nn(n,K) = sum_i num_high_to_low[i] * n^{K-i} / (den * n^K). Dividing
    through by n^K: the coefficient of 1/n^j (j=0..K) is exactly
    num_high_to_low[j] / den (index 0 -> constant term c_0, from the n^K
    numerator term; index K -> the 1/n^K term, from the n^0 numerator
    term) -- no reversal needed, 'high to low' already lines up with
    c_0..c_K in that same order."""
    return [Fraction(c, den) for c in num_high_to_low]


PROPOSITIONS = {
    1: coeffs_from_numerator([3, 1], 6),
    2: coeffs_from_numerator([10, 7, 2], 30),
    3: coeffs_from_numerator([35, 38, 23, 6], 140),
    4: coeffs_from_numerator([126, 187, 177, 98, 24], 630),
    5: coeffs_from_numerator([462, 874, 1139, 989, 514, 120], 2772),
    6: coeffs_from_numerator([1716, 3958, 6616, 7933, 6472, 3204, 720], 12012),
}

RANGES = {
    1: range(4, 15),
    2: range(4, 15),
    3: range(6, 15),
    4: range(6, 26),
    5: range(7, 14),
    6: range(8, 14),
}

if __name__ == '__main__':
    all_ok = True
    for K in [1, 2, 3, 4, 5, 6]:
        coeffs = PROPOSITIONS[K]
        ok_count = 0
        total_count = 0
        for n in RANGES[K]:
            v = P_nn(n, K)
            p = predict(coeffs, n)
            ok = (v == p)
            total_count += 1
            ok_count += int(ok)
            if not ok:
                all_ok = False
                print(f"MISMATCH K={K} n={n}: reduced-model={v} predicted={p}")
        print(f"K={K}: {ok_count}/{total_count} exact matches over n in "
              f"{RANGES[K].start}..{RANGES[K].stop-1}")
    print()
    print("ALL MATCH" if all_ok else "SOME MISMATCHES FOUND")
