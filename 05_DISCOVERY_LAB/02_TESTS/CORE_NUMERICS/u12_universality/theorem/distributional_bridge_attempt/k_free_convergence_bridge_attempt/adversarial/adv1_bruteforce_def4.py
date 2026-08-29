"""
Independent, from-scratch exact brute-force enumeration of THEOREM.md
Definition 4: fix K reroute sources at {0,...,K-1}, pi a uniform random
permutation of [n] = {0,...,n-1}, reroute targets U_0,...,U_{K-1} i.i.d.
uniform on [n] (independent of pi). f(i) := U_i for i a rerouted source,
f(i) := pi(i) otherwise. T := #{cyclic points of f}.

This script is written completely fresh from the mathematical definition
in THEOREM.md, without reading any of the target front's .py files
(true_definition4_bruteforce.py, construction_crosscheck.py, etc.). It is
used ONLY to cross-check the specific exact E[T]/n values the target
claims match THEOREM.md's own reported table:
  n=4, K=1: 11/16
  n=5, K=1: 17/25
  n=4, K=2: 113/192
and (bonus) a couple more cells reported by THEOREM.md itself (n=5,K=2:
356/625; n=6,K=2: 151/270; n=2,K=1: 3/4; n=3,K=1: 19/27) as additional
sanity checks, plus one K=3 cell to touch a third value of K.
"""
from fractions import Fraction
from itertools import permutations, product


def cyclic_count(f, n):
    """f: list of length n, f[i] in {0,...,n-1}. Returns #cyclic points."""
    color = [0] * n  # 0 unvisited, 1 in-progress, 2 done
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
            # cur is in the current path -> found a cycle
            idx = path.index(cur)
            for node in path[idx:]:
                cyclic[node] = True
        for node in path:
            color[node] = 2
    return sum(cyclic)


def exact_ET_over_n(n, K):
    """Exact E[T]/n as a Fraction, by full enumeration of Def. 4."""
    assert K <= n
    total = Fraction(0)
    count = 0
    sources = list(range(K))
    for pi in permutations(range(n)):
        for U in product(range(n), repeat=K):
            f = list(pi)
            for idx, s in enumerate(sources):
                f[s] = U[idx]
            T = cyclic_count(f, n)
            total += T
            count += 1
    E_T = total / count
    return E_T / n, count


CASES = [
    (2, 1, Fraction(3, 4)),
    (3, 1, Fraction(19, 27)),
    (4, 1, Fraction(11, 16)),
    (5, 1, Fraction(17, 25)),
    (4, 2, Fraction(113, 192)),
    (5, 2, Fraction(356, 625)),
    (6, 2, Fraction(151, 270)),
    (4, 3, None),  # no THEOREM.md target value quoted; sanity-run only
]

if __name__ == "__main__":
    print(f"{'n':>3} {'K':>3} {'#configs':>10} {'computed E[T]/n':>20} {'target':>12} {'match':>7}")
    all_ok = True
    for n, K, target in CASES:
        val, cnt = exact_ET_over_n(n, K)
        ok = (target is None) or (val == target)
        all_ok = all_ok and ok
        print(f"{n:>3} {K:>3} {cnt:>10} {str(val):>20} {str(target):>12} {str(ok):>7}")
    print()
    print("ALL MATCH:", all_ok)
