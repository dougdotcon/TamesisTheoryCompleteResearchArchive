"""
Fresh, independent check of the wave-17 front's Lemma 1 formula
    n*phi(n,q) = sum_{k=1}^n A_k(n,q),
    A_k(n,q) = sum_{m=0}^k C(k,m) q^m (1-q)^{k-m} * P(k,m),
    P(k,m) = prod_{i=1}^m (1 - (k-i)/n)
against a from-scratch brute-force enumeration of Definition 1
(uniform permutation pi, iid Bernoulli(q) reroute flags xi_i, iid
uniform U_i, f(i)=U_i if xi_i=1 else pi(i); count cyclic points of f),
done independently of the wave-17 front's own derivation text (only
Definition 1 itself, as quoted in ATTEMPT.md Sec.0/THEOREM.md Sec.1,
is used). No script from any prior front was read.

Exact rational arithmetic throughout (fractions.Fraction).
"""
from fractions import Fraction as Fr
from itertools import permutations, product
import math


def cyclic_count(f, n):
    """f: dict/list, 1-indexed images in 1..n. Count points on a
    directed cycle of the functional graph i -> f(i)."""
    on_cycle = [False] * (n + 1)
    visited = [0] * (n + 1)  # 0 = unvisited, else stamps the walk id
    stamp = 0
    for start in range(1, n + 1):
        if visited[start]:
            continue
        stamp += 1
        path = []
        x = start
        while visited[x] == 0:
            visited[x] = stamp
            path.append(x)
            x = f[x]
        if visited[x] == stamp:
            # found a new cycle starting at position of x in path
            idx = path.index(x)
            for y in path[idx:]:
                on_cycle[y] = True
    return sum(on_cycle[1:n + 1])


def brute_force_nphi(n, q: Fr):
    """Exact E[#cyclic points of f] under Definition 1, by full
    enumeration over permutations pi, reroute subsets S, and U-images
    on S. q must be a Fraction so all weights stay exact."""
    total = Fr(0)
    verts = list(range(1, n + 1))
    perms = list(permutations(verts))
    for S_mask in range(2 ** n):
        S = [verts[i] for i in range(n) if (S_mask >> i) & 1]
        m = len(S)
        w_S = q ** m * (1 - q) ** (n - m)
        if w_S == 0:
            continue
        notS = [v for v in verts if v not in S]
        for pi_tuple in perms:
            pi = dict(zip(verts, pi_tuple))
            # base f: pi(i) for i not in S; will overwrite S below
            for U_choice in product(verts, repeat=m):
                f = dict(pi)
                for idx, i in enumerate(S):
                    f[i] = U_choice[idx]
                cc = cyclic_count(f, n)
                total += w_S * Fr(cc) * Fr(1, math.factorial(n)) * Fr(1, n ** m if m > 0 else 1)
    return total


def P(k, m, n):
    prod = Fr(1)
    for i in range(1, m + 1):
        prod *= (1 - Fr(k - i, n))
    return prod


def A_k(k, n, q: Fr):
    total = Fr(0)
    for m in range(0, k + 1):
        binom = math.comb(k, m)
        total += binom * q ** m * (1 - q) ** (k - m) * P(k, m, n)
    return total


def formula_nphi(n, q: Fr):
    return sum(A_k(k, n, q) for k in range(1, n + 1))


if __name__ == "__main__":
    print("Independent brute-force check of the exact double-sum formula")
    print("=" * 70)
    all_ok = True
    for n in (3, 4, 5):
        qs = [Fr(0), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1)] if n < 5 else [Fr(0), Fr(2, 5), Fr(1)]
        for q in qs:
            bf = brute_force_nphi(n, q)
            fm = formula_nphi(n, q)
            ok = (bf == fm)
            all_ok &= ok
            print(f"n={n} q={q!s:>5}  brute={str(bf):>12}  formula={str(fm):>12}  match={ok}")
    print("=" * 70)
    print("ALL MATCH" if all_ok else "MISMATCH FOUND")

    # q=0 and q=1 sanity checks against Definition-1-level reasoning
    print()
    print("Sanity: q=0 -> f=pi a uniform permutation -> phi(n,0) should be 1")
    for n in (3, 4, 5, 6):
        val = formula_nphi(n, Fr(0)) / n
        print(f"  n={n}: phi(n,0) = {val} (expect 1)")

    print()
    print("Sanity: q=1 -> f uniform random FUNCTION -> n*phi(n,n) = Q(n) := sum_k (n)_k/n^k")

    def Qn(n):
        total = Fr(0)
        fall = Fr(1)
        for k in range(1, n + 1):
            fall *= Fr(n - k + 1, n)
            total += fall
        return total

    for n in (3, 4, 5, 6, 7, 10, 20):
        f_val = formula_nphi(n, Fr(1))
        q_val = Qn(n)
        print(f"  n={n}: formula(q=1)={f_val}  Q(n)={q_val}  match={f_val == q_val}")
