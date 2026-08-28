"""
Fresh, from-scratch verification of Lemma 1 (Marked-Point Gap Structure,
general m, cited from Estagio 31 / k2_joint_case_split_attempt) plus the
Governing-Source Reindexing corollary (Estagio 35 / k3_joint_structural_
attempt Sec 2), generalized to general K = m marks.

No code read from any other front. Exhaustive enumeration of ALL n!
permutations of [n] for small n, marks fixed at {0,...,K-1}.
"""
from itertools import permutations
from fractions import Fraction
from collections import Counter


def contract_and_gaps(perm, K, n):
    """perm: tuple, perm[i] = pi(i) (0-indexed, values 0..n-1).
    marks = {0,...,K-1}. sigma(s) = first mark hit forward along pi from s
    (following pi(s), pi(pi(s)), ... until landing on a mark).
    g(s) = number of unmarked points strictly between s and sigma(s) along
    that forward chain. O = n - K - sum(g)."""
    marks = set(range(K))
    sigma = {}
    gaps = {}
    for s in range(K):
        cur = perm[s]
        cnt = 0
        while cur not in marks:
            cnt += 1
            cur = perm[cur]
        sigma[s] = cur
        gaps[s] = cnt
    O = n - K - sum(gaps.values())
    return sigma, gaps, O


def check(K, n_values):
    for n in n_values:
        assert n > K
        sigma_counter = Counter()
        gap_counter = Counter()
        a_counter = Counter()   # mark-indexed arc length a_m = g(m)+1
        joint_counter = Counter()
        L_counter = Counter()  # governing-source reindexed arc length L_s
        total = 0
        for perm in permutations(range(n)):
            sigma, gaps, O = contract_and_gaps(perm, K, n)
            sigma_tuple = tuple(sigma[s] for s in range(K))
            gap_tuple = tuple(gaps[s] for s in range(K)) + (O,)
            a_tuple = tuple(gaps[s] + 1 for s in range(K)) + (O,)
            sigma_counter[sigma_tuple] += 1
            gap_counter[gap_tuple] += 1
            a_counter[a_tuple] += 1
            joint_counter[(sigma_tuple, gap_tuple)] += 1
            # governing-source arc lengths: L_s = a_{sigma^{-1}(s)} = g(sigma^{-1}(s))+1
            sigma_inv = {v: k for k, v in sigma.items()}
            L = tuple(gaps[sigma_inv[s]] + 1 for s in range(K))
            O_L = n - K - sum(l - 1 for l in L)
            assert O_L == O
            L_counter[L + (O,)] += 1
            total += 1

        # (a) sigma uniform on S_K
        sigma_counts = list(sigma_counter.values())
        n_topologies = len(sigma_counter)
        expected_topologies = 1
        for k in range(1, K + 1):
            expected_topologies *= k
        ok_sigma_uniform = (n_topologies == expected_topologies and
                             len(set(sigma_counts)) == 1)

        # (b) gap vector uniform over compositions of n-K into K+1 nonneg parts
        gap_counts = list(gap_counter.values())
        ok_gap_uniform = len(set(gap_counts)) == 1

        # (c) joint independence: every (sigma, gap) cell equal
        joint_counts = list(joint_counter.values())
        ok_joint_indep = len(set(joint_counts)) == 1

        # (d) governing-source reindexed L (with O appended) has SAME
        # distribution (same set of keys, same per-key counts) as the
        # mark-indexed arc-length vector a = gap+1 (with O appended).
        ok_L_matches = (dict(L_counter) == dict(a_counter))

        print(f"K={K}, n={n}: total={total} (={__import__('math').factorial(n)}), "
              f"#topologies={n_topologies} (expect {expected_topologies}), "
              f"sigma uniform={ok_sigma_uniform}, gap uniform={ok_gap_uniform} "
              f"(#compositions={len(gap_counter)}), joint indep={ok_joint_indep}, "
              f"governing-source L matches raw gap distribution={ok_L_matches}")
        assert ok_sigma_uniform and ok_gap_uniform and ok_joint_indep and ok_L_matches


if __name__ == '__main__':
    print("=== Lemma 1 (general m) + Governing-Source Reindexing, general K ===")
    check(1, [4, 5, 6])
    check(2, [4, 5, 6])
    check(3, [4, 5, 6, 7])
    check(4, [5, 6, 7])
    check(5, [6, 7])
    print()
    print("ALL CHECKS PASSED for K=1..5: sigma uniform on S_K, gap vector uniform")
    print("over compositions, joint independence of sigma and gaps, and the")
    print("governing-source reindexed arc-length vector (L_0,...,L_{K-1},O) has")
    print("exactly the same law as the raw mark-indexed gap vector, independent")
    print("of sigma -- confirming the Governing-Source Reindexing corollary")
    print("generalizes to arbitrary K by the identical exchangeability argument.")
