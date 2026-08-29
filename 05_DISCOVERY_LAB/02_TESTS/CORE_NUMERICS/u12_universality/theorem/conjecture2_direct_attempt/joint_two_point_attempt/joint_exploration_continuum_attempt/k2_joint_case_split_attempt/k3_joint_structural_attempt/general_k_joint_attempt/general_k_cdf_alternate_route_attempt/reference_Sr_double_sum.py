"""
Reference implementation of S_r(n,K,k), built from CITED (not re-derived)
results:

  * Proposicao S and the Full Cycle-Count Decomposition Theorem, K free
    (Estagio 41, THEOREM.md): T = O + sum_{s in S} V_s, (V_s) mutually
    independent given S, V_s ~ Uniform{1,...,L_s}; P(S=A|L) =
    |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a).

  * The exchangeability reduction to S_r(n,K,k) := sum over the full
    composition simplex of (O+Sigma)*Count_r(L_0,...,L_{r-1};k-O),
    Sigma:=L_0+...+L_{r-1} (Estagio 44, general_k_closed_cdf_attempt
    Section 2 -- an elementary exchangeability argument, PROVED, 96/96
    verified against D1/D2/D3 there).

  * Layer 1's closed form for the K-r untouched-source marginalization
    (Estagio 44, general_k_closed_cdf_attempt Section 4.1 -- PROVED,
    verified two independent ways there):
        InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),  N:=n-V-O  (r<K)
        InnerJ(V,O) = n*C(N+r-1,r-1),                     N:=n-V-O  (r=K)
    with S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{k-O} C(V-1,r-1)*InnerJ(V,O).

This script implements this DOUBLE sum directly (the "Camada 1 done,
Camada 2+3 done the ORIGINAL nested way" reference point this front
starts from), and independently verifies it two ways:
  (a) against the fresh Definition-4 brute force of this front
      (bruteforce_definition4_general_k.py's cache), via full assembly
      P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r)*r!/n^{r+1} * S_r(n,K,k)
  (b) against the three already-PROVED closed forms D1 (K=1, Estagio
      27), D2 (K=2, Estagio 42), D3 (K=3, Estagio 40), cited verbatim.

This is the STARTING POINT this front's new route (the W-collapse in
w_collapse_identity.py) is checked against -- not itself the new
content of this front.
"""
from fractions import Fraction
from math import comb
import json


def InnerJ_direct(n, K, r, V, O):
    """The CITED Layer-1 closed form (Estagio 44 Section 4.1), evaluated
    directly (integer arithmetic, exact)."""
    b = K - r
    N = n - V - O
    if N < 0:
        return 0
    if b == 0:
        c1 = comb(N + r - 1, r - 1) if r > 0 else (1 if N == 0 else 0)
        return n * c1
    A1 = comb(N + r - 1, K - 1) if (N + r - 1 >= 0) else 0
    A2 = comb(N + r - 1, K) if (N + r - 1 >= 0) else 0
    return (O + V) * A1 + r * A2


def Sr_double_sum(n, K, r, k):
    """S_r(n,K,k) via the ORIGINAL nested O-then-V sum (Estagio 44's own
    Camada 2 / Camada 3 organization, done here in the un-closed,
    directly-summed way as a reference)."""
    total = 0
    for O in range(0, k + 1):
        t = k - O
        for V in range(r, t + 1):
            cV = comb(V - 1, r - 1) if r > 0 else (1 if V == 0 else 0)
            total += cV * InnerJ_direct(n, K, r, V, O)
    return total


def unconditional_cdf_via_Sr(n, K, k):
    """P(T<=k) assembled from S_r via the exchangeability reduction
    (cited, Estagio 44 Section 2):
        P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r)*r!/n^{r+1} * S_r(n,K,k)
    Exact Fraction arithmetic."""
    total = Fraction(0)
    for r in range(0, K + 1):
        Sr = Sr_double_sum(n, K, r, k)
        total += Fraction(comb(K, r) * comb(r, r) * __import__('math').factorial(r), n ** (r + 1)) * Sr
    return total / comb(n, K)


D1 = lambda n, k: Fraction(k * (k + 1), n ** 2)
D2 = lambda n, k: Fraction(k * (k + 1) * (2 * n ** 2 - 3 * n + k - k ** 2), n ** 3 * (n - 1))
D3 = lambda n, k: Fraction(
    k * (k + 1) * (k ** 4 - 4 * k ** 3 - (3 * n ** 2 - 9 * n - 5) * k ** 2
                    + (3 * n ** 2 - 11 * n - 2) * k + (3 * n ** 4 - 12 * n ** 3 + 12 * n ** 2 + 2 * n)),
    n ** 4 * (n - 1) * (n - 2))


if __name__ == "__main__":
    print("Reference S_r double-sum, verification (a): vs. fresh brute force")
    print("=" * 70)
    with open("bruteforce_cdf_cache.json") as fh:
        bf_cache = json.load(fh)
    all_ok = True
    for (n, K) in [(4, 1), (4, 2), (5, 2), (5, 3), (6, 3), (6, 4), (7, 3), (7, 4)]:
        bf = [Fraction(x) for x in bf_cache[f"{n}_{K}"]]
        for k in range(n + 1):
            got = unconditional_cdf_via_Sr(n, K, k)
            ok = (got == bf[k])
            all_ok = all_ok and ok
            status = "OK" if ok else "MISMATCH"
            if not ok:
                print(f"  n={n} K={K} k={k}: reference={got} brute_force={bf[k]}  {status}")
    print(f"All (n,K,k) cells matched brute force: {all_ok}")

    print()
    print("Verification (b): vs. already-PROVED closed forms D1/D2/D3")
    print("=" * 70)
    all_ok2 = True
    for n in range(3, 9):
        for k in range(0, n):  # domain 0<=k<=n-1
            v1 = unconditional_cdf_via_Sr(n, 1, k)
            d1 = D1(n, k)
            ok1 = (v1 == d1)
            v2 = unconditional_cdf_via_Sr(n, 2, k)
            d2 = D2(n, k)
            ok2 = (v2 == d2)
            v3 = unconditional_cdf_via_Sr(n, 3, k)
            d3 = D3(n, k)
            ok3 = (v3 == d3)
            all_ok2 = all_ok2 and ok1 and ok2 and ok3
            if not (ok1 and ok2 and ok3):
                print(f"  n={n} k={k}: D1 ok={ok1} D2 ok={ok2} D3 ok={ok3}")
    print(f"All D1/D2/D3 cells matched (n=3..8, all valid k): {all_ok2}")
    print()
    print(f"REFERENCE ENGINE STATUS: brute-force check = {all_ok}, "
          f"D1/D2/D3 check = {all_ok2}")
