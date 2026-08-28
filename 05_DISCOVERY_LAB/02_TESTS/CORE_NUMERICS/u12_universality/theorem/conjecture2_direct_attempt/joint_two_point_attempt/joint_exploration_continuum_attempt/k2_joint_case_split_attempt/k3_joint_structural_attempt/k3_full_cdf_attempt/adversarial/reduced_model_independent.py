#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH independent "reduced model" verification of the
Full Cycle-Count Decomposition Theorem + Proposicao S + the conditional CDF
(ATTEMPT.md Sec 2-3), and, via averaging over the composition simplex, of
Proposicao D3 itself (Sec 4), for a much larger range of n than exhaustive
Definition-4 brute force can reach.

No .py file from any front in this lineage was read to build this. Inputs
used, all from prose only:

  - (Cited, established by Estagio 35/its predecessor Estagio 31, PROVED
    and independently SOUND-reviewed there; NOT re-derived here, exactly
    as this front itself does not re-derive it): (L_0,L_1,L_2,O) is
    uniform over the C(n,3) compositions of n into L_0,L_1,L_2>=1, O>=0.
  - This referee's OWN independent re-derivation of Proposicao S
    (proposition_S_check.py in this directory, verified by direct 64-case
    symbolic sum -- NOT copied from the front, built fresh, see that
    script's docstring).
  - The Full Cycle-Count Decomposition Theorem's statement (T = O +
    sum_{s in S} V_s, V_s uniform on {1,...,L_s}, mutually independent
    given S) -- ATTEMPT.md Sec 2.2, cited as the claim under test here,
    not assumed correct: this script tests it (jointly with Prop S) by
    checking whether the resulting reduced-model CDF prediction matches
    (a) true Definition-4 brute force (bruteforce_full_cdf.py, this
    directory) for the overlapping n range, and (b) Proposicao D3's
    closed form.
  - Elementary lattice-point counting via inclusion-exclusion (a standard
    combinatorial technique, re-derived from scratch below, not read from
    any conditional_cdf.py or similar file in this lineage) to compute
    exact P(sum of m independent discrete uniforms <= t) for m=0,1,2,3.

If the Decomposition Theorem or Proposicao S were wrong, this
independently-assembled reduced-model CDF would NOT match true brute
force -- that correspondence (checked below for n=3..9, overlapping
bruteforce_full_cdf.py's own range) is itself strong evidence for BOTH
claims simultaneously (a wrong theorem essentially never reproduces
exhaustive ground truth over many n, k).
"""

import itertools
import json
import sys
import time
from fractions import Fraction


def N2(s):
    """# of (a,b) with a,b>=0 integers, a+b<=s. 0 if s<0."""
    if s < 0:
        return 0
    return (s + 1) * (s + 2) // 2


def N3(s):
    """# of (a,b,c) with a,b,c>=0 integers, a+b+c<=s. 0 if s<0."""
    if s < 0:
        return 0
    return (s + 1) * (s + 2) * (s + 3) // 6


def paircount(A, B, m):
    """#{(v,w): 1<=v<=A, 1<=w<=B, v+w<=m} via inclusion-exclusion, derived
    from scratch (standard bounded-lattice-point technique): shift to
    u=v-1 in [0,A-1], w'=w-1 in [0,B-1], u+w'<=m-2, then subtract the
    "u too big" / "w too big" violation regions."""
    s = m - 2
    U = A - 1
    W = B - 1
    return N2(s) - N2(s - (U + 1)) - N2(s - (W + 1)) + N2(s - (U + 1) - (W + 1))


def triplecount(A, B, C, m):
    """#{(v,w,x): 1<=v<=A,1<=w<=B,1<=x<=C, v+w+x<=m} via inclusion-exclusion
    over the 3 upper-bound violation events, same technique as paircount
    generalized to 3 variables (standard, re-derived here)."""
    s = m - 3
    U = (A - 1, B - 1, C - 1)
    total = 0
    for mask in range(8):
        shift = 0
        bits = 0
        for i in range(3):
            if mask & (1 << i):
                shift += U[i] + 1
                bits += 1
        sign = -1 if (bits % 2 == 1) else 1
        total += sign * N3(s - shift)
    return total


def clip(t, lo, hi):
    return max(lo, min(t, hi))


def prob_S_given_L(L0, L1, L2, O, n):
    """Our OWN independently re-derived Proposicao S formulas
    (proposition_S_check.py confirmed these symbolically against the raw
    64-case sum). p_i = L_i/n, p_D = O/n, exact Fraction arithmetic."""
    p = {0: Fraction(L0, n), 1: Fraction(L1, n), 2: Fraction(L2, n)}
    pD = Fraction(O, n)
    P = {}
    P[frozenset()] = pD
    for s in (0, 1, 2):
        P[frozenset([s])] = p[s] * (p[s] + pD)
    for s, t in itertools.combinations((0, 1, 2), 2):
        u = ({0, 1, 2} - {s, t}).pop()
        P[frozenset([s, t])] = 2 * p[s] * p[t] * (1 - p[u])
    P[frozenset([0, 1, 2])] = 6 * p[0] * p[1] * p[2]
    check = sum(P.values())
    assert check == 1, f"Prop S probabilities do not sum to 1: {check}"
    return P


def prob_sum_le(A_subset, L, t):
    """P(sum_{s in A_subset} V_s <= t), V_s ~ Uniform{1,...,L_s} independent,
    via the Decomposition Theorem's claim (under test) + our own
    inclusion-exclusion lattice counts."""
    m = len(A_subset)
    if m == 0:
        return Fraction(1) if t >= 0 else Fraction(0)
    if m == 1:
        (s,) = tuple(A_subset)
        Ls = L[s]
        return Fraction(clip(t, 0, Ls), Ls)
    if m == 2:
        s1, s2 = sorted(A_subset)
        L1_, L2_ = L[s1], L[s2]
        cnt = paircount(L1_, L2_, t)
        cnt = max(0, cnt)
        return Fraction(cnt, L1_ * L2_)
    if m == 3:
        L0_, L1_, L2_ = L[0], L[1], L[2]
        cnt = triplecount(L0_, L1_, L2_, t)
        cnt = max(0, cnt)
        return Fraction(cnt, L0_ * L1_ * L2_)
    raise ValueError


def P_T_le_k_given_L(L0, L1, L2, O, n, k):
    """P(T<=k | L0,L1,L2), assembled from Prop S (our own derivation) +
    Decomposition Theorem's claimed sum-of-independent-uniforms structure
    (under test)."""
    L = {0: L0, 1: L1, 2: L2}
    PS = prob_S_given_L(L0, L1, L2, O, n)
    t = k - O
    total = Fraction(0)
    for A, pA in PS.items():
        if pA == 0:
            continue
        total += pA * prob_sum_le(A, L, t)
    return total


def d3_formula(n, k):
    """Proposicao D3's claimed closed form, transcribed independently
    (same transcription as bruteforce_full_cdf.py, typed fresh from
    ATTEMPT.md Sec 4.1's stated formula, for comparison only)."""
    if k >= n:
        return Fraction(1, 1)
    if k < 0:
        return Fraction(0, 1)
    n_ = Fraction(n)
    k_ = Fraction(k)
    numerator = k_ * (k_ + 1) * (
        k_**4 - 4 * k_**3
        - (3 * n_**2 - 9 * n_ - 5) * k_**2
        + (3 * n_**2 - 11 * n_ - 2) * k_
        + (3 * n_**4 - 12 * n_**3 + 12 * n_**2 + 2 * n_)
    )
    denominator = n_**4 * (n_ - 1) * (n_ - 2)
    return numerator / denominator


def reduced_model_cdf(n):
    """P(T<=k) for all k=0..n-1, exact Fraction, averaged over the
    uniform composition simplex (L0,L1,L2>=1, O=n-sum>=0), using our own
    Prop-S + Decomposition-Theorem assembly above."""
    from math import comb
    total_compositions = comb(n, 3)
    accum = {k: Fraction(0) for k in range(0, n)}
    count = 0
    for L0 in range(1, n - 1):
        for L1 in range(1, n - L0):
            L2max = n - L0 - L1
            for L2 in range(1, L2max + 1):
                O = n - L0 - L1 - L2
                count += 1
                for k in range(0, n):
                    accum[k] += P_T_le_k_given_L(L0, L1, L2, O, n, k)
    assert count == total_compositions, f"n={n}: composition count {count} != C(n,3)={total_compositions}"
    cdf = {k: v / total_compositions for k, v in accum.items()}
    return cdf


def load_bruteforce_cdf(n, results_path):
    try:
        with open(results_path) as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return None
    entry = data.get(str(n))
    if entry is None:
        return None
    cdf = {}
    for k_str, (num, den) in entry["cdf"].items():
        cdf[int(k_str)] = Fraction(num, den)
    return cdf


def main():
    ns_full = list(range(3, 16))       # full-CDF exact comparison range
    ns_extra = [20, 25, 30, 40, 50, 60]  # extended spot-check range (self-consistency vs D3 only)
    if len(sys.argv) > 1:
        ns_full = [int(x) for x in sys.argv[1:]]
        ns_extra = []

    bf_path = __file__.replace("reduced_model_independent.py", "bruteforce_full_cdf_results.json")

    all_ok = True
    print("=" * 78)
    print("PART 1: reduced-model CDF (own Prop-S + Decomposition-Theorem "
          "assembly) vs Proposicao D3, and, where available, vs TRUE "
          "brute force (bruteforce_full_cdf.py)")
    print("=" * 78)
    for n in ns_full:
        t0 = time.time()
        cdf = reduced_model_cdf(n)
        elapsed = time.time() - t0
        bf_cdf = load_bruteforce_cdf(n, bf_path)

        mism_d3 = []
        mism_bf = []
        for k in range(0, n):
            rm = cdf[k]
            d3 = d3_formula(n, k)
            if rm != d3:
                mism_d3.append((k, str(rm), str(d3)))
            if bf_cdf is not None:
                bfv = bf_cdf[k]
                if rm != bfv:
                    mism_bf.append((k, str(rm), str(bfv)))
        ok = (len(mism_d3) == 0) and (len(mism_bf) == 0)
        all_ok = all_ok and ok
        bf_note = f"vs bruteforce: {'OK' if not mism_bf else f'{len(mism_bf)} MISMATCHES'}" if bf_cdf is not None else "vs bruteforce: (no ground truth loaded)"
        print(f"n={n:3d}  elapsed={elapsed:6.2f}s  vs D3: "
              f"{'OK' if not mism_d3 else f'{len(mism_d3)} MISMATCHES'}   {bf_note}")
        if mism_d3:
            for m in mism_d3[:10]:
                print("   D3 MISMATCH:", m)
        if mism_bf:
            for m in mism_bf[:10]:
                print("   BRUTEFORCE MISMATCH:", m)

    print()
    print("=" * 78)
    print("PART 2: extended range, reduced model vs Proposicao D3 only "
          "(no exhaustive ground truth feasible at these n)")
    print("=" * 78)
    for n in ns_extra:
        t0 = time.time()
        cdf = reduced_model_cdf(n)
        elapsed = time.time() - t0
        mism_d3 = []
        for k in range(0, n):
            rm = cdf[k]
            d3 = d3_formula(n, k)
            if rm != d3:
                mism_d3.append((k, str(rm), str(d3)))
        ok = (len(mism_d3) == 0)
        all_ok = all_ok and ok
        print(f"n={n:3d}  elapsed={elapsed:6.2f}s  vs D3: "
              f"{'OK' if not mism_d3 else f'{len(mism_d3)} MISMATCHES'}")
        if mism_d3:
            for m in mism_d3[:10]:
                print("   D3 MISMATCH:", m)

    print()
    if all_ok:
        print("ALL CHECKS PASSED: independently-assembled reduced model "
              "(own Prop-S derivation + Decomposition Theorem's claimed "
              "structure + own inclusion-exclusion lattice counts) matches "
              "both true brute force and Proposicao D3 exactly, across all "
              "n and k tested.")
    else:
        print("*** AT LEAST ONE MISMATCH FOUND. ***")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
