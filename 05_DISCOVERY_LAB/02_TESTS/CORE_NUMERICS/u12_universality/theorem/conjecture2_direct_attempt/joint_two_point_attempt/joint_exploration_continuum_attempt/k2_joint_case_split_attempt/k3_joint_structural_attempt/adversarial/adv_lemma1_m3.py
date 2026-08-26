"""
Independent, from-scratch verification of:
  (1) Lemma 1 (Marked-Point Gap Structure) at m=3, marks {0,1,2}.
  (2) The "Governing-Source Reindexing" corollary (topology sigma
      marginalizes out for governing-source-indexed arc lengths L_s).

Written purely from the mathematical prose in ATTEMPT.md / THEOREM.md.
No .py file from any front in the lineage was read.

Method: exhaustive enumeration of all n! permutations of [n], n=4..7,
exact integer counting (no floats, no randomness).
"""
import itertools
from collections import Counter, defaultdict

MARKS = (0, 1, 2)

def analyze(perm, n):
    """perm: tuple, perm[i] = pi(i). Returns sigma (dict mark->mark),
    g (dict mark->gap size), the a-vector (mark-indexed arc length,
    a[m] = g[m]+1), the L-vector (governing-source indexed arc length),
    and O (outside count)."""
    sigma = {}
    g = {}
    for s in MARKS:
        cur = perm[s]
        cnt = 0
        while cur not in MARKS:
            cnt += 1
            cur = perm[cur]
        sigma[s] = cur
        g[s] = cnt
    a = {m: g[m] + 1 for m in MARKS}
    total_gap = sum(g.values())
    O = n - 3 - total_gap
    # sigma_inv
    sigma_inv = {v: k for k, v in sigma.items()}
    # L_s := a_{sigma^{-1}(s)}  -- arc whose TAIL is s
    L = {s: a[sigma_inv[s]] for s in MARKS}
    return sigma, a, L, O


def sigma_key(sigma):
    return tuple(sigma[m] for m in MARKS)


def run(n):
    assert n >= 4
    total = 0
    sigma_counts = Counter()
    a_composition_counts = Counter()  # composition of n-3 into 4 parts, marginal over sigma
    joint_sigma_a_counts = Counter()  # (sigma, a-composition)
    L_composition_counts = Counter()  # governing-source indexed, marginal
    joint_sigma_L_counts = Counter()

    others = [x for x in range(n) if x not in MARKS]
    for perm_tail in itertools.permutations(range(n)):
        # perm_tail is a full permutation of [n] (a bijection given as tuple)
        perm = perm_tail
        total += 1
        sigma, a, L, O = analyze(perm, n)
        skey = sigma_key(sigma)
        sigma_counts[skey] += 1
        acomp = (a[0], a[1], a[2], O)
        a_composition_counts[acomp] += 1
        joint_sigma_a_counts[(skey, acomp)] += 1
        Lcomp = (L[0], L[1], L[2], O)
        L_composition_counts[Lcomp] += 1
        joint_sigma_L_counts[(skey, Lcomp)] += 1

    assert total == __import__('math').factorial(n)

    results = {}
    results['n'] = n
    results['total'] = total

    # (a) sigma uniform on S_3: 6 topologies, each should have count total/6
    expected_sigma_count = total // 6
    ok_sigma_uniform = (len(sigma_counts) == 6) and all(
        c == expected_sigma_count for c in sigma_counts.values()
    ) and total % 6 == 0
    results['ok_sigma_uniform'] = ok_sigma_uniform
    results['sigma_counts'] = dict(sigma_counts)

    # (b) a-vector (mark-indexed) uniform over compositions of n-3 into 4 parts,
    # independent of sigma: every (sigma, a-comp) cell should equal (n-3)!
    from math import factorial
    expected_cell = factorial(n - 3)
    n_compositions = 0
    # number of compositions of n-3 into 4 nonneg parts = C(n-3+3,3) = C(n,3)
    from math import comb
    expected_num_compositions = comb(n, 3)
    ok_joint_sigma_a = all(c == expected_cell for c in joint_sigma_a_counts.values())
    ok_joint_sigma_a_cellcount = (len(joint_sigma_a_counts) == 6 * expected_num_compositions)
    results['ok_joint_sigma_a_equal_cells'] = ok_joint_sigma_a
    results['ok_joint_sigma_a_cellcount'] = ok_joint_sigma_a_cellcount
    results['expected_cell_value'] = expected_cell
    results['expected_num_compositions'] = expected_num_compositions
    results['num_distinct_a_compositions'] = len(a_composition_counts)
    ok_a_marginal_uniform = all(
        c == expected_cell * 6 for c in a_composition_counts.values()
    )
    results['ok_a_marginal_uniform'] = ok_a_marginal_uniform

    # (c) Governing-source indexed L-vector: same claim, PLUS independence from sigma
    ok_joint_sigma_L = all(c == expected_cell for c in joint_sigma_L_counts.values())
    ok_joint_sigma_L_cellcount = (len(joint_sigma_L_counts) == 6 * expected_num_compositions)
    results['ok_joint_sigma_L_equal_cells'] = ok_joint_sigma_L
    results['ok_joint_sigma_L_cellcount'] = ok_joint_sigma_L_cellcount
    ok_L_marginal_uniform = all(
        c == expected_cell * 6 for c in L_composition_counts.values()
    )
    results['ok_L_marginal_uniform'] = ok_L_marginal_uniform

    # (d) L-composition distribution (as a *set* of composition->count) should be
    # IDENTICAL to a-composition distribution (same support, same counts)
    ok_L_matches_a_distribution = (a_composition_counts == L_composition_counts)
    results['ok_L_matches_a_distribution'] = ok_L_matches_a_distribution

    return results


if __name__ == '__main__':
    all_ok = True
    for n in range(4, 8):
        r = run(n)
        print(f"--- n={n} ---")
        for k, v in r.items():
            if k in ('sigma_counts',):
                continue
            print(f"  {k}: {v}")
        this_ok = all([
            r['ok_sigma_uniform'],
            r['ok_joint_sigma_a_equal_cells'],
            r['ok_joint_sigma_a_cellcount'],
            r['ok_a_marginal_uniform'],
            r['ok_joint_sigma_L_equal_cells'],
            r['ok_joint_sigma_L_cellcount'],
            r['ok_L_marginal_uniform'],
            r['ok_L_matches_a_distribution'],
        ])
        print(f"  ALL_OK_n={n}: {this_ok}")
        all_ok = all_ok and this_ok
    print()
    print(f"FINAL: ALL_OK = {all_ok}")
