"""
ADVERSARIAL SCRIPT 7 -- independent reproduction of Section 4.2's
concrete demonstration that the naive "same Vandermonde trick as Layer
1" formula for the Layer-2 V-sum disagrees with the true truncated sum
below the natural bound, at the exact representative cell the target
document quotes (n=12, K=5, r=2, O=0, natural bound V<=9).

Built entirely from scratch: InnerJ_closed (independently re-derived and
verified in script2_layer1.py) plus a fresh brute truncated V-sum, plus
the front's own claimed VSum_naive formula (re-derived independently
here as "one further application of the identical convolution
technique" per the target's own description, then checked against the
brute sum).
"""
from math import comb


def safe_comb(a, b):
    if a < 0 or b < 0 or b > a:
        return 0
    return comb(a, b)


def InnerJ_closed(n, K, r, V, O):
    N = n - V - O
    if r == K:
        return n * safe_comb(N + r - 1, r - 1)
    return (O + V) * safe_comb(N + r - 1, K - 1) + r * safe_comb(N + r - 1, K)


def brute_Vsum(n, K, r, O, t):
    total = 0
    for V in range(r, t + 1):
        cV = safe_comb(V - 1, r - 1) if r >= 1 else (1 if V == 0 else 0)
        total += cV * InnerJ_closed(n, K, r, V, O)
    return total


def VSum_naive(n, K, r, O):
    """The target's own claimed naive-Vandermonde formula, re-derived
    independently as 'one further application of the identical
    convolution technique' applied to the FULL (untruncated) V-range:
      VSum_naive(O) = (O+r)*C(n-O+r-1,K+r-1) + 2r*C(n-O+r-1,K+r)
    (this referee re-derived this by the same two-step Vandermonde
    technique used for InnerJ in script2_layer1.py, applied one level
    up; not re-derived from scratch in this script's comments for
    brevity -- the numeric check below is what matters)."""
    return (O + r) * safe_comb(n - O + r - 1, K + r - 1) + 2 * r * safe_comb(n - O + r - 1, K + r)


if __name__ == "__main__":
    n, K, r, O = 12, 5, 2, 0
    natural_bound = n - O - (K - r)
    print(f"(n,K,r,O)=({n},{K},{r},{O}), natural bound V<={natural_bound}")
    naive = VSum_naive(n, K, r, O)
    print("VSum_naive value (constant, independent of t):", naive)
    print()
    print("t : true (brute, independent implementation) : naive : match")
    all_disagree_below_bound = True
    for t in range(2, natural_bound + 1):
        true_sum = brute_Vsum(n, K, r, O, t)
        match = (true_sum == naive)
        if t < natural_bound and match:
            all_disagree_below_bound = False
        print(f"{t:2d} : {true_sum:6d} : {naive:6d} : {match}")
    print()
    print("Target document's own reported sequence (t=2..9):")
    print("  1584, 3852, 6120, 7968, 9228, 9930, 10224, 10296")
    reproduced = [brute_Vsum(n, K, r, O, t) for t in range(2, 10)]
    print("  this referee's independent reproduction:")
    print(" ", ", ".join(str(x) for x in reproduced))
    print("  EXACT MATCH:", reproduced == [1584, 3852, 6120, 7968, 9228, 9930, 10224, 10296])
    print()
    print("Naive formula disagrees with the true sum at every t strictly")
    print("below the natural bound, matching only once t reaches it:",
          all_disagree_below_bound and (brute_Vsum(n, K, r, O, natural_bound) == naive))
