"""
Independent, from-scratch check that the "reduced model" underlying the
whole K-free machinery (Governing-Source Reindexing + i.i.d. categorical
destinations + landing-position-uniform + the Decomposition Theorem
T = O + sum_{s in S} V_s) reproduces the EXACT full pmf of T under true
Definition 4 -- not just the mean (already checked in adv1). This goes a
bit beyond the mandate's explicit ask but is cheap and is the real
foundation Theorem A's coupling stands on, so it is worth checking with
exact enumeration rather than sampling.

Reduced model, exact enumeration:
  - the K divider positions (sorted) are a uniform random K-subset of
    {1,...,n}  (C(n,K) equally likely subsets)
  - given the resulting gap vector (L_0,...,L_{K-1}, O), each of the K
    "arc sources" independently chooses a target uniform on {1,...,n};
    dest(j) = t if the target falls in arc t's range, else DEAD
  - within-arc landing position k_t = target - cumL(t) (in {1,...,L_t})
  - S = cyclic sources of the functional graph induced by dest
  - T = O + sum_{t in S} (L_t - k_t + 1)

This is compared, cell by cell (exact Fraction pmf), against the TRUE
brute-force Definition 4 model (independently re-implemented here, not
reusing adv1_bruteforce_def4.py's code, to keep this script standalone).
"""
from fractions import Fraction
from itertools import permutations, product, combinations
from collections import Counter


def cyclic_count(f, n):
    color = [0] * n
    cyclic = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        cur = start
        while color[cur] == 0:
            color[cur] = 1
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:
            idx = path.index(cur)
            for node in path[idx:]:
                cyclic[node] = True
        for node in path:
            color[node] = 2
    return sum(cyclic)


def true_def4_pmf(n, K):
    """Exact pmf of T under literal Definition 4, as a Counter of exact counts."""
    counts = Counter()
    total_configs = 0
    sources = list(range(K))
    for pi in permutations(range(n)):
        for U in product(range(n), repeat=K):
            f = list(pi)
            for idx, s in enumerate(sources):
                f[s] = U[idx]
            T = cyclic_count(f, n)
            counts[T] += 1
            total_configs += 1
    return counts, total_configs


def reduced_model_pmf(n, K):
    """
    Exact pmf of T under the reduced-model recipe, enumerated exactly:
    sum over C(n,K) divider subsets (equal weight) x n^K target choices
    (equal weight within each subset).
    """
    counts = Counter()
    total_configs = 0
    for dividers in combinations(range(1, n + 1), K):  # sorted K-subset of {1,...,n}
        cumL = [0] + list(dividers)  # cumL[0..K]
        L = [cumL[t + 1] - cumL[t] for t in range(K)]
        O = n - cumL[K]
        # each of K sources chooses target uniform on {1,...,n}
        for targets in product(range(1, n + 1), repeat=K):
            dest = [None] * K
            k_pos = [None] * K
            for j, tgt in enumerate(targets):
                # find which arc t (0..K-1) tgt falls into: (cumL[t], cumL[t+1]]
                placed = False
                for t in range(K):
                    if cumL[t] < tgt <= cumL[t + 1]:
                        dest[j] = t
                        k_pos[j] = tgt - cumL[t]  # in {1,...,L[t]}
                        placed = True
                        break
                if not placed:
                    dest[j] = 'DEAD'
            # find S: cyclic sources of functional graph on {0,...,K-1} via dest
            # dest[j] tells where "arc j"'s governing reroute points to.
            # walk from each t in 0..K-1 following dest, absorbing at DEAD
            color = [0] * K  # 0 unvisited, 1 active, 2 done
            cyclic_src = [False] * K
            for start in range(K):
                if color[start] != 0:
                    continue
                path = []
                cur = start
                while True:
                    if cur == 'DEAD':
                        break
                    if color[cur] == 2:
                        break
                    if color[cur] == 1:
                        idx = path.index(cur)
                        for node in path[idx:]:
                            cyclic_src[node] = True
                        break
                    color[cur] = 1
                    path.append(cur)
                    cur = dest[cur]
                for node in path:
                    if color[node] != 2:
                        color[node] = 2
            T = O
            for t in range(K):
                if cyclic_src[t]:
                    V_t = L[t] - k_pos[t] + 1
                    T += V_t
            counts[T] += 1
            total_configs += 1
    return counts, total_configs


def compare(n, K):
    true_counts, true_total = true_def4_pmf(n, K)
    red_counts, red_total = reduced_model_pmf(n, K)
    all_T = sorted(set(true_counts) | set(red_counts))
    ok = True
    print(f"--- n={n}, K={K} ---  (true_total={true_total}, reduced_total={red_total})")
    for T in all_T:
        p_true = Fraction(true_counts.get(T, 0), true_total)
        p_red = Fraction(red_counts.get(T, 0), red_total)
        match = (p_true == p_red)
        ok = ok and match
        print(f"  T={T:>3}  P_true={str(p_true):>10}  P_reduced={str(p_red):>10}  match={match}")
    print(f"  FULL PMF MATCH for (n={n},K={K}):", ok)
    print()
    return ok


if __name__ == "__main__":
    all_ok = True
    for n, K in [(4, 1), (5, 2), (6, 2), (5, 3)]:
        all_ok = compare(n, K) and all_ok
    print("ALL CELLS: reduced model exactly reproduces true Definition 4's full pmf:", all_ok)
