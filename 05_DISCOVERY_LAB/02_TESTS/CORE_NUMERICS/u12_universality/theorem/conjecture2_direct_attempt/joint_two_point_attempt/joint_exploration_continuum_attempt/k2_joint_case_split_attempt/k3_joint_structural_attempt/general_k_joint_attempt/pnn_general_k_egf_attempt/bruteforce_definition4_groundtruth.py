"""
Ground-truth brute force of THEOREM.md's Definition 4, written completely
fresh from the mathematical prose (no .py file from any front read,
per the front's hard constraint):

  pi: uniform random permutation of [n].
  K reroute sources fixed at {0,...,K-1}.
  U_0,...,U_{K-1} i.i.d. Uniform([n]), independent of pi.
  f(i) := U_i for i in sources, f(i) := pi(i) otherwise.
  A node q is "cyclic" for f iff iterating f from q returns to q.

P_nn(n,K) := P(n-2, n-1 both cyclic for f)  (query points fixed WLOG,
disjoint from the sources per Definition 4's own exchangeability, so
n >= K+2).

This enumerates ALL n! permutations times n^K target tuples exactly
(exact Fraction arithmetic, no floating point) -- the single most
trustworthy reference point in this front's own verification, used to
validate every reduced-model formula (P_0, P_same, P_disjoint, and the
full T(L)/composition-sum assembly) built in the other scripts here.
"""
import itertools
from fractions import Fraction
import time


def is_cyclic(f, q):
    seen = set()
    cur = q
    while True:
        cur = f[cur]
        if cur == q:
            return True
        if cur in seen:
            return False
        seen.add(cur)


def brute_force_pnn(n, K):
    assert n >= K + 2
    q1, q2 = n - 2, n - 1
    sources = list(range(K))
    total = 0
    both = 0
    for perm in itertools.permutations(range(n)):
        for targets in itertools.product(range(n), repeat=K):
            f = list(perm)
            for idx, s in enumerate(sources):
                f[s] = targets[idx]
            total += 1
            if is_cyclic(f, q1) and is_cyclic(f, q2):
                both += 1
    return Fraction(both, total)


if __name__ == "__main__":
    print("Ground-truth brute force of Definition 4, P_nn(n,K) = P(n-2,n-1 both cyclic)")
    print("=" * 78)
    # already-PROVED closed forms this cross-checks against:
    #   K=1 (Estagio 27): (3n+1)/(6n)
    #   K=2 (Estagio 31, Prop NN2): (10n^2+7n+2)/(30n^2)
    #   K=3 (Estagio 35, Prop NN3): (35n^3+38n^2+23n+6)/(140n^3)
    cases = [
        (1, 3), (1, 4), (1, 5), (1, 6),
        (2, 4), (2, 5), (2, 6),
        (3, 5), (3, 6), (3, 7),
    ]
    for K, n in cases:
        t0 = time.time()
        val = brute_force_pnn(n, K)
        dt = time.time() - t0
        print(f"K={K}, n={n}: P_nn = {val}   ({dt:.2f}s)")

    def nn1(n):
        return Fraction(3 * n + 1, 6 * n)

    def nn2(n):
        return Fraction(10 * n ** 2 + 7 * n + 2, 30 * n ** 2)

    def nn3(n):
        return Fraction(35 * n ** 3 + 38 * n ** 2 + 23 * n + 6, 140 * n ** 3)

    print("\nCross-check against already-PROVED closed forms (Estagio 27/31/35):")
    all_ok = True
    for K, n in cases:
        val = brute_force_pnn(n, K)
        expected = {1: nn1, 2: nn2, 3: nn3}[K](n)
        ok = (val == expected)
        all_ok = all_ok and ok
        print(f"  K={K},n={n}: brute={val}  formula={expected}  match={ok}")
    print(f"\nALL MATCH already-PROVED closed forms: {all_ok}")
