"""
The exact closed-form conditional CDF P(T<=k | L0,L1), K=2 analogue of
`k3_full_cdf_attempt`'s conditional_cdf.py (structure), derived fresh
from the Decomposition Theorem + Proposition S (decomposition_theorem.py,
this same directory -- imported here, not re-derived).

P(T<=k | L) = P(S=empty|L)*[O<=k]
            + P(S={0}|L) * clip(k-O,0,L0)/L0
            + P(S={1}|L) * clip(k-O,0,L1)/L1
            + P(S={0,1}|L) * paircount(L0,L1,k-O) / (L0*L1)

where paircount(A,B,m) := #{(v,w): 1<=v<=A, 1<=w<=B, v+w<=m}.

Also provides the slow-but-exact O(n^3) reference engine
`full_cdf_exact(n,k)` (sum this conditional CDF over the whole
composition simplex, dividing by C(n,2)) used as an independent
reference for the closed-form Proposicao D2 (symbolic_derivation_full_cdf.py).
"""
from fractions import Fraction
from math import comb


def clip(t, lo, hi):
    return max(lo, min(hi, t))


def paircount(A, B, m):
    """#{(v,w): 1<=v<=A, 1<=w<=B, v+w<=m}, direct O(A) computation."""
    if m < 2:
        return 0
    total = 0
    for v in range(1, A + 1):
        wmax = min(B, m - v)
        if wmax >= 1:
            total += wmax
    return total


def P_T_le_k_given_L(n, L0, L1, k):
    O = n - L0 - L1
    p0, p1 = Fraction(L0, n), Fraction(L1, n)
    pD = Fraction(O, n)
    P_empty = pD
    P_s0 = p0 * (p0 + pD)
    P_s1 = p1 * (p1 + pD)
    P_both = 2 * p0 * p1

    t = k - O
    val = Fraction(0)
    val += P_empty * (1 if O <= k else 0)
    val += P_s0 * Fraction(clip(t, 0, L0), L0)
    val += P_s1 * Fraction(clip(t, 0, L1), L1)
    val += P_both * Fraction(paircount(L0, L1, t), L0 * L1)
    return val


def full_cdf_exact(n, k):
    """Slow-but-exact O(n^2) reference: average the conditional CDF over
    the entire (L0,L1) composition simplex (uniform weighting, C(n,2)
    total pairs). Independent of Proposicao D2's own closed form -- this
    is a direct implementation of Sections 2-3's proved machinery only."""
    total = Fraction(0)
    for L0 in range(1, n):
        for L1 in range(1, n - L0 + 1):
            total += P_T_le_k_given_L(n, L0, L1, k)
    return total / comb(n, 2)


if __name__ == "__main__":
    import sys
    from decomposition_theorem import reduced_model_T_distribution

    print("Verifying conditional CDF closed form vs reduced model "
          "(decomposition_theorem.py's independent enumeration)")
    cases = [(5, 1, 1), (5, 2, 2), (7, 3, 2), (8, 4, 3), (9, 2, 5)]
    all_ok = True
    for (n, L0, L1) in cases:
        counts, denom = reduced_model_T_distribution(n, L0, L1)
        cum = 0
        ok = True
        for k in range(0, n + 1):
            cum += counts.get(k, 0)
            reduced_cdf = Fraction(cum, denom)
            formula_cdf = P_T_le_k_given_L(n, L0, L1, k)
            if reduced_cdf != formula_cdf:
                ok = False
                print(f"  MISMATCH n={n} L0={L0} L1={L1} k={k}: "
                      f"reduced={reduced_cdf} formula={formula_cdf}")
        all_ok = all_ok and ok
        print(f"  n={n} L0={L0} L1={L1}: {'OK, exact match every k' if ok else 'MISMATCH'}")

    print("\n" + "=" * 60)
    if all_ok:
        print("Conditional CDF closed form CONFIRMED (exact match on "
              "every k, every tested (n,L0,L1)).")
    else:
        sys.exit(1)
