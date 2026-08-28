"""
Independent check of Corollary NN K.2's ingredient: the Theorem J Corollary,
"P(same cycle | both query points cyclic) = 1/2 exactly, at every finite
n,K" -- re-tested directly on fresh raw brute-force data (own code, full
Definition-4 model), not merely cited, for K=1..4 at several n.
"""
import itertools
from fractions import Fraction


def cyclic_and_samecycle(f, p, q, n):
    # returns (p_cyclic, q_cyclic, same_cycle_if_both_cyclic)
    def orbit_cycle_members(start):
        cur = f[start]
        seen = [start]
        for _ in range(n):
            if cur == start:
                return True, set(seen)
            if cur in seen:
                return False, None
            seen.append(cur)
            cur = f[cur]
        return False, None

    p_cyc, p_cycle = orbit_cycle_members(p)
    q_cyc, q_cycle = orbit_cycle_members(q)
    same = None
    if p_cyc and q_cyc:
        same = (p in q_cycle)  # q_cycle contains q's whole cycle; if p also cyclic and in it -> same cycle
    return p_cyc, q_cyc, same


def run(n, K):
    q1, q2 = n - 2, n - 1
    total = 0
    both = 0
    same_count = 0
    for pi in itertools.permutations(range(n)):
        for U in itertools.product(range(n), repeat=K):
            f = list(pi)
            for i in range(K):
                f[i] = U[i]
            total += 1
            p_cyc, q_cyc, same = cyclic_and_samecycle(f, q1, q2, n)
            if p_cyc and q_cyc:
                both += 1
                if same:
                    same_count += 1
    return Fraction(same_count, both), Fraction(both, total), total


if __name__ == "__main__":
    cases = [(1, 3), (1, 5), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6)]
    for K, n in cases:
        ratio, pnn, total = run(n, K)
        print(f"K={K} n={n} configs={total} P(same|both cyclic)={ratio} P_nn={pnn} "
              f"-> {'OK 1/2' if ratio == Fraction(1,2) else 'MISMATCH!!'}")
