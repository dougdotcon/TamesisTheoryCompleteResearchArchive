"""
Independent, from-scratch re-derivation + brute-force check of the
"Marked-Point Gap Structure Lemma" (target document's Lemma 1), worked out
BEFORE reading the target document's own proof closely (per adversarial
mandate item 5(i)). This file only imports our own cycle_utils (for
independence, though a plain forward-walk suffices here since pi is an
actual bijection, not a general functional graph).

Claim to check, for m marked points S subset of [n], pi uniform on Sym([n]):
  (a) The "contracted permutation" sigma on S -- sigma(s) := first point of
      S reached walking forward along pi from s -- is uniform on Sym(S).
  (b) The gap sizes g(s) (# of non-marked points strictly between s and
      sigma(s) along pi) together with O := n-m-sum(g(s)) (# of points in
      pi-cycles touching no marked point at all) are, independent of sigma,
      uniform over all compositions of n-m into m+1 nonnegative parts.

We test m=2 (the case actually used downstream) and m=3, for several n,
by full enumeration of Sym([n]).
"""
import sys
import itertools
from fractions import Fraction
from collections import Counter


def contracted_and_gaps(pi, S):
    """
    pi: tuple, pi[i] = image of i under the permutation.
    S: list of m marked points.
    Returns (sigma_dict, gaps_dict, O) where:
      sigma_dict[s] = next marked point reached walking forward from s
                      (s itself if s is a fixed point of the induced walk,
                       i.e. if pi(s) eventually returns to s before hitting
                       another marked point -- this happens when s is alone
                       in its own pi-cycle among marked points).
      gaps_dict[s]  = number of unmarked points strictly between s and
                      sigma_dict[s] along pi (0 if sigma(s) = pi(s)).
      O             = number of points in pi-cycles that contain NO marked
                      point at all.
    """
    n = len(pi)
    Sset = set(S)
    sigma = {}
    gaps = {}
    visited_in_walk = set()  # points consumed by walking from a marked start
    for s in S:
        node = pi[s]
        steps = 0
        while node not in Sset:
            node = pi[node]
            steps += 1
            if steps > n:  # safety; cannot happen for a real permutation
                raise RuntimeError("infinite loop; pi is not a valid permutation")
        sigma[s] = node
        gaps[s] = steps  # number of unmarked points strictly between s and sigma(s)

    # O: points that are in a pi-cycle disjoint from S entirely.
    # Determine cycles of pi; a cycle "touches" S if it contains any marked point.
    seen = [False] * n
    touched_points = 0
    for i in range(n):
        if seen[i]:
            continue
        cyc = []
        node = i
        while not seen[node]:
            seen[node] = True
            cyc.append(node)
            node = pi[node]
        if any((c in Sset) for c in cyc):
            touched_points += len(cyc)
    O = n - touched_points
    return sigma, gaps, O


def sigma_as_permutation_signature(sigma, S):
    """Represent sigma: S->S as a tuple in the order of S, for hashing/counting."""
    return tuple(sigma[s] for s in S)


def compositions_count(total, parts):
    """Number of compositions of `total` into `parts` nonnegative integers = C(total+parts-1, parts-1)."""
    from math import comb
    return comb(total + parts - 1, parts - 1)


def run_check(n, m, verbose=True):
    S = list(range(m))  # marked points fixed at {0,...,m-1} WLOG
    sigma_counts = Counter()
    gap_tuple_counts = Counter()
    joint_counts = Counter()  # (sigma_sig, gap_tuple) -> count
    total = 0

    for pi_tuple in itertools.permutations(range(n)):
        sigma, gaps, O = contracted_and_gaps(pi_tuple, S)
        sig = sigma_as_permutation_signature(sigma, S)
        gap_tuple = tuple(gaps[s] for s in S) + (O,)
        assert sum(gap_tuple) == n - m, f"gap sum mismatch: {gap_tuple} n={n} m={m}"
        sigma_counts[sig] += 1
        gap_tuple_counts[gap_tuple] += 1
        joint_counts[(sig, gap_tuple)] += 1
        total += 1

    # Check (a): sigma uniform on Sym(S) -- m! outcomes, each with count total/m!.
    import math
    m_fact = math.factorial(m)
    expected_sigma_count = total // m_fact if total % m_fact == 0 else None
    sigma_ok = (len(sigma_counts) == m_fact) and all(
        c == total / m_fact for c in sigma_counts.values()
    )
    # More precisely with Fractions:
    sigma_fracs = {k: Fraction(v, total) for k, v in sigma_counts.items()}
    sigma_uniform = all(v == Fraction(1, m_fact) for v in sigma_fracs.values()) and len(sigma_fracs) == m_fact

    # Check (b): gap-compositions uniform over all compositions of n-m into m+1 parts,
    # and INDEPENDENT of sigma (joint = product of marginals).
    n_compositions = compositions_count(n - m, m + 1)
    gap_fracs = {k: Fraction(v, total) for k, v in gap_tuple_counts.items()}
    gaps_uniform = (len(gap_fracs) == n_compositions) and all(
        v == Fraction(1, n_compositions) for v in gap_fracs.values()
    )

    # Independence check: for every observed (sig, gap_tuple) pair, joint prob
    # should equal sigma_prob * gap_prob = (1/m!) * (1/n_compositions).
    expected_joint = Fraction(1, m_fact) * Fraction(1, n_compositions)
    independence_ok = True
    n_joint_cells = m_fact * n_compositions
    joint_fracs = {k: Fraction(v, total) for k, v in joint_counts.items()}
    if len(joint_fracs) != n_joint_cells:
        independence_ok = False
    else:
        independence_ok = all(v == expected_joint for v in joint_fracs.values())

    ok = sigma_uniform and gaps_uniform and independence_ok
    if verbose:
        print(f"n={n} m={m}: total_perms={total} "
              f"sigma_uniform={sigma_uniform} (|support|={len(sigma_counts)}, expect {m_fact}) "
              f"gaps_uniform={gaps_uniform} (|support|={len(gap_tuple_counts)}, expect {n_compositions}) "
              f"independent={independence_ok} (|joint support|={len(joint_counts)}, expect {n_joint_cells}) "
              f"=> {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    results = []
    for m, ns in [(2, [2, 3, 4, 5, 6, 7]), (3, [3, 4, 5, 6, 7])]:
        for n in ns:
            results.append((n, m, run_check(n, m)))
    all_ok = all(r[2] for r in results)
    print()
    print("ALL PASS" if all_ok else "SOME FAILURES")
    print(f"total cells checked: {len(results)}")
