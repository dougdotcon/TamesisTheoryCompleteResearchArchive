"""
Section 2 of ATTEMPT.md: reduce the 2^K-subset sum to a sum over subset
SIZE r (0..K), by exchangeability -- exactly the mandate's avenue (a),
and the same reorganization principle
`pnn_general_k_egf_attempt/ATTEMPT.md` used for P_nn(n,K) (there:
Governing-Source Reindexing lets "sum over all C(K-1,r) actual subsets"
be replaced by "C(K-1,r) times one representative value").

Starting from `proposition_s_and_conditional_cdf.py`'s cond_cdf, and using
P(S=A|L) = r! prod_{a in A}(L_a/n) (p_D + sum_{a in A} p_a) (Proposition
S, cited): the prod_{a in A} L_a factor in P(S=A|L)'s numerator cancels
EXACTLY against the prod_{a in A} L_a denominator already present in
Count_r/prod L_a (the same cancellation Estagio 40 Section 3 noted at
K=3) -- leaving, per subset A of size r:

    r! (O + Sigma_A) / n^{r+1} * Count_r(L_A ; k-O),   Sigma_A := sum_{a in A} L_a

Averaged over the FULL composition simplex (all K coordinates, not just
A), the domain is symmetric under permuting {0,...,K-1}, so for fixed r:

    sum_{L,O} sum_{|A|=r} [term(A,L,O)] = C(K,r) * sum_{L,O} term({0,...,r-1},L,O)

This defines S_r(n,K,k) := sum over the FULL composition simplex of
(O+Sigma) * Count_r(L_0,...,L_{r-1} ; k-O), where Sigma:=L_0+...+L_{r-1},
and gives:

    P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r) * r!/n^{r+1} * S_r(n,K,k)

This script (a) defines S_r as a direct, ground-truth composition-simplex
sum, (b) verifies the exchangeability reduction above by direct
comparison against `unconditional_cdf_slow` (the "raw" Section-1 engine)
for EVERY k, 0<=k<=n, at several (n,K) -- confirming, crucially, that
NO regime-splitting on k is needed for this identity (unlike Estagio 40's
K=3 derivation, which needed three separate regimes for a different
reason -- see Section 4/ATTEMPT.md for the precise diagnosis of why this
particular reformulation avoids that), and (c) cross-checks the resulting
P(T<=k) against the three ALREADY-PROVED closed forms Proposicao D1
(K=1, Estagio 27), Proposicao D2 (K=2, Estagio 42), Proposicao D3 (K=3,
Estagio 40) -- cited here as fixed target formulas, not re-derived.
"""
from fractions import Fraction
from itertools import product
from math import comb, factorial

from proposition_s_and_conditional_cdf import unconditional_cdf_slow
from bruteforce_definition4_general_k import bruteforce_cdf


def count_le(Ls, t):
    r = len(Ls)
    if r == 0:
        return 1 if t >= 0 else 0
    if t < r:
        return 0
    cnt = 0
    for v in product(*[range(1, L + 1) for L in Ls]):
        if sum(v) <= t:
            cnt += 1
    return cnt


def comp_count(m, parts):
    """Number of compositions of m into `parts` nonnegative parts."""
    if m < 0:
        return 0
    if parts == 0:
        return 1 if m == 0 else 0
    return comb(m + parts - 1, parts - 1)


def S_r_direct(n, K, r, k):
    """Ground-truth S_r(n,K,k): sum over the FULL composition simplex of
    (O+Sigma)*Count_r(L_0..L_{r-1}; k-O), with the K-r untouched sources
    L_r,...,L_{K-1} marginalized out via the composition-counting
    multiplicity comp_count(remaining - (K-r), K-r)."""
    total = 0
    b = K - r
    for O in range(0, n + 1):
        for L in product(range(1, n + 1), repeat=r):
            Sigma = sum(L)
            if Sigma + O > n:
                continue
            remaining = n - Sigma - O
            mult = comp_count(remaining - b, b) if b > 0 else (1 if remaining == 0 else 0)
            if mult == 0:
                continue
            cnt = count_le(L, k - O)
            total += (O + Sigma) * cnt * mult
    return total


def assemble(n, K, k):
    total = Fraction(0)
    for r in range(0, K + 1):
        Sr = S_r_direct(n, K, r, k)
        total += comb(K, r) * factorial(r) * Fraction(Sr, n ** (r + 1))
    return total / comb(n, K)


D1 = lambda n, k: Fraction(k * (k + 1), n ** 2)
D2 = lambda n, k: Fraction(k * (k + 1) * (2 * n ** 2 - 3 * n + k - k ** 2), n ** 3 * (n - 1))
D3 = lambda n, k: Fraction(
    k * (k + 1) * (k ** 4 - 4 * k ** 3 - (3 * n ** 2 - 9 * n - 5) * k ** 2
                   + (3 * n ** 2 - 11 * n - 2) * k + (3 * n ** 4 - 12 * n ** 3 + 12 * n ** 2 + 2 * n)),
    n ** 4 * (n - 1) * (n - 2))


if __name__ == "__main__":
    print("Exchangeability reduction check: S_r-based assembly vs raw Section-1")
    print("engine, ALL k, no regime split -- plus D1/D2/D3 cross-check.")
    print("=" * 70)
    all_ok = True

    print("(a) vs unconditional_cdf_slow (raw Section-1 engine), full k range:")
    for n, K in [(4, 1), (4, 2), (5, 2), (5, 3), (6, 3), (7, 4)]:
        for k in range(0, n + 1):
            a = assemble(n, K, k)
            b = unconditional_cdf_slow(n, K, k)
            ok = (a == b)
            all_ok = all_ok and ok
            print(f"   n={n} K={K} k={k}: assemble={a}  raw={b}  {'OK' if ok else 'MISMATCH!'}")

    print("(b) vs true Definition-4 brute force, full k range:")
    for n, K in [(5, 2), (6, 3)]:
        bf, _ = bruteforce_cdf(n, K)
        for k in range(0, n + 1):
            a = assemble(n, K, k)
            ok = (a == bf[k])
            all_ok = all_ok and ok
            print(f"   n={n} K={K} k={k}: assemble={a}  bruteforce={bf[k]}  {'OK' if ok else 'MISMATCH!'}")

    print("(c) vs already-PROVED D1/D2/D3 (0<=k<=n-1 -- their stated domain):")
    count = 0
    for n in range(3, 9):
        for k in range(0, n):
            for K, D in [(1, D1), (2, D2), (3, D3)]:
                if K >= n:
                    continue
                a = assemble(n, K, k)
                b = D(n, k)
                ok = (a == b)
                all_ok = all_ok and ok
                count += 1
                if not ok:
                    print(f"   MISMATCH n={n} K={K} k={k}: assemble={a} D{K}={b}")
    print(f"   {count} D1/D2/D3 comparisons done.")

    print("=" * 70)
    print(f"ALL CHECKS MATCH: {all_ok}")
    if not all_ok:
        raise SystemExit(1)
