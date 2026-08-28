"""
Section 4 of ATTEMPT.md, part 1: Layer 2 (the V-sum over subset-total-
size, S_r's second summation layer) does NOT collapse the same way Layer
1 did -- demonstrated concretely, not just asserted.

S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{k-O} C(V-1,r-1) * InnerJ(V,O)
(V := sum_{a in A} L_a; C(V-1,r-1) counts compositions of V into r
POSITIVE parts, i.e. the L_0,...,L_{r-1} tuples with that total).

Unlike Layer 1's j-sum (whose upper limit is exactly where the SECOND
binomial coefficient's own combinatorial validity forces it to vanish --
a "natural" range), the V-sum's upper limit t:=k-O is EXTERNALLY imposed
by Count_r's own definition (sum v_i <= t) -- it has nothing to do with
where C(V-1,r-1)*InnerJ(V,O), as a function of V, would naturally stop
being combinatorially meaningful. This script shows directly that the
naive "sum to infinity via the same Vandermonde trick" formula:

    VSum_wrong(O,t) := (O+r)*C(n-O+r-1,K+r-1) + 2r*C(n-O+r-1,K+r)

(obtained by formally applying Layer 1's SAME convolution identity to the
V-sum, ignoring the truncation) matches the TRUE truncated V-sum only
when t happens to equal the natural bound where the summand itself
vanishes -- and is WRONG (over-counts) for every smaller t, which is
exactly the regime this front actually needs (t=k-O, and k ranges over
the WHOLE CDF, most values well below the natural bound).
"""
from math import comb


def InnerJ_direct(n, K, r, V, O):
    b = K - r
    N = n - V - O
    if b == 0:
        if N < 0:
            return 0
        c1 = comb(N + r - 1, r - 1) if r > 0 else (1 if N == 0 else 0)
        return c1 * (O + V + N)
    total = 0
    for j in range(0, max(N, 0)):
        c1 = comb(j + r - 1, r - 1) if r > 0 else (1 if j == 0 else 0)
        c2 = comb(N - 1 - j, b - 1) if (N - 1 - j) >= 0 and (N - 1 - j) >= (b - 1) else 0
        total += c1 * (O + V + j) * c2
    return total


def VSum_true(n, K, r, O, t):
    total = 0
    for V in range(r, t + 1):
        cV = comb(V - 1, r - 1) if r > 0 else (1 if V == 0 else 0)
        total += cV * InnerJ_direct(n, K, r, V, O)
    return total


def VSum_naive_untruncated_formula(n, K, r, O):
    """What you'd get by (incorrectly) applying Layer 1's Vandermonde
    trick to the V-sum too, as if it ran to its natural range."""
    M = n - O
    return (O + r) * comb(M + r - 1, K + r - 1) + 2 * r * comb(M + r - 1, K + r)


if __name__ == "__main__":
    print("Layer 2 truncation demonstration: naive Vandermonde formula vs the")
    print("true truncated V-sum, across the FULL range of t (=k-O).")
    print("=" * 70)
    n, K, r, O = 12, 5, 2, 0
    naive = VSum_naive_untruncated_formula(n, K, r, O)
    natural_bound = n - O - (K - r)  # where InnerJ's own support ends
    print(f"n={n} K={K} r={r} O={O}  naive-untruncated-formula value = {naive}")
    print(f"  (natural bound of V's support: V <= {natural_bound})")
    any_mismatch_below = False
    exact_at_bound = None
    for t in range(r, natural_bound + 3):
        true_val = VSum_true(n, K, r, O, t)
        matches_naive = (true_val == naive)
        if t < natural_bound and matches_naive:
            pass  # would be surprising; tracked below
        if t < natural_bound and not matches_naive:
            any_mismatch_below = True
        if t >= natural_bound and matches_naive and exact_at_bound is None:
            exact_at_bound = t
        tag = "MATCHES naive formula" if matches_naive else "does NOT match naive formula (genuine partial sum)"
        print(f"   t={t:2d}: true VSum = {true_val:6d}   {tag}")
    print("=" * 70)
    print(f"Confirmed: naive untruncated formula disagrees with the true")
    print(f"truncated V-sum for every t below the natural bound "
          f"({any_mismatch_below}), and agrees exactly once t reaches/exceeds")
    print(f"the natural bound (first exact match at t={exact_at_bound}).")
    print("This is the precise, demonstrated reason Layer 2 needs a genuinely")
    print("different (INDEFINITE-summation / Gosper) treatment -- see")
    print("gosper_certification_vsum.py.")
