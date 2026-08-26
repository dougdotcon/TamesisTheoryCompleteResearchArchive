"""
gap_lemma_m3_unittest.py

Fresh, independent spot-check (own script, not reading the predecessor's
gap_lemma_unittest.py) of the Marked-Point Gap Structure Lemma (predecessor
ATTEMPT.md Sec 2, Lemma 1, PROVED there for general m, cited by name and
statement here) at m=3, the case this front needs.

Checks BOTH claims of Lemma 1 by exhaustive enumeration of all n!
permutations, marks S={0,1,2}:
  (a) the contracted permutation sigma on S is uniform on S_3 (6 outcomes,
      each probability 1/6).
  (b) (g(0),g(1),g(2),O) is uniform over all compositions of n-3 into 4
      nonnegative parts, independent of sigma.

Also checks this front's OWN new corollary (ATTEMPT.md Sec 2.2, PROVED):
governing-source-indexed arc lengths L_s := a_{sigma^{-1}(s)} have the SAME
uniform-over-compositions law, independent of sigma -- i.e. topology can be
marginalized out. This is the key simplification this front's Three-Source
Redirect-Structure Lemma depends on.
"""

from fractions import Fraction
from itertools import permutations
from collections import Counter
import sys


def contracted_and_gaps(pi, n, marks):
    """Given permutation pi (as tuple/list) and marks (list of 3 ints),
    compute sigma (dict mark->mark) and g(mark) for each mark, and O."""
    mark_set = set(marks)
    sigma = {}
    g = {}
    for s in marks:
        x = pi[s]
        gap = 0
        while x not in mark_set:
            gap += 1
            x = pi[x]
        sigma[s] = x
        g[s] = gap
    O = n - len(marks) - sum(g.values())
    return sigma, g, O


def sigma_to_perm_tuple(sigma, marks):
    """Represent sigma as a tuple of images in mark order, for hashing."""
    return tuple(sigma[m] for m in marks)


def run(n, marks=(0, 1, 2)):
    marks = list(marks)
    sigma_counts = Counter()
    gap_counts = Counter()  # keyed by (g0,g1,g2,O)
    # governing-source indexed arc lengths L_s = g(sigma^{-1}(s)) + 1
    Lgov_counts = Counter()
    joint_counts = Counter()  # (sigma_tuple, (g0,g1,g2)) -> count, to check independence

    total = 0
    for pi in permutations(range(n)):
        sigma, g, O = contracted_and_gaps(pi, n, marks)
        sigma_tuple = sigma_to_perm_tuple(sigma, marks)
        gvec = tuple(g[m] for m in marks)
        sigma_counts[sigma_tuple] += 1
        gap_counts[gvec + (O,)] += 1
        joint_counts[(sigma_tuple, gvec)] += 1

        # governing-source indexed: L_s = g(sigma^{-1}(s)) + 1
        sigma_inv = {v: k for k, v in sigma.items()}
        Lvec = tuple(g[sigma_inv[s]] + 1 for s in marks)
        Lgov_counts[Lvec] += 1

        total += 1

    return total, sigma_counts, gap_counts, joint_counts, Lgov_counts


def check(n):
    total, sigma_counts, gap_counts, joint_counts, Lgov_counts = run(n)

    # (a) sigma uniform on S_3
    n_topologies = len(sigma_counts)
    ok_a = (n_topologies == 6)
    counts_a = set(sigma_counts.values())
    ok_a = ok_a and (len(counts_a) == 1)

    # (b) (g0,g1,g2,O) uniform over compositions of n-3 into 4 parts, and
    # independent of sigma (joint counts should factor: count(sigma,g) =
    # count(sigma)*count(g)/total, i.e. every (sigma,g) pair with sigma in
    # support and g in support should have the SAME count = (n-3)! since
    # Lemma 1's proof gives exactly (n-m)! per (sigma,g) pair).
    counts_b = set(gap_counts.values())
    ok_b = (len(counts_b) == 1)
    from math import factorial
    expected_per_cell = factorial(n - 3)
    # gap_counts is marginalized over the 6 topologies, so each cell should
    # be 6*(n-3)! (joint_counts, per (sigma,gap) pair, is the (n-3)! one).
    ok_b_value = all(v == 6 * expected_per_cell for v in gap_counts.values())

    joint_vals = set(joint_counts.values())
    ok_independence = (len(joint_vals) == 1) and (list(joint_vals)[0] == expected_per_cell)

    # governing-source-indexed L should have the SAME distribution as
    # gap_counts (up to the shift a_s = g_s+1, i.e. compositions of n-3
    # into (L0-1,L1-1,L2-1,O))
    Lgov_as_gaps = Counter()
    for Lvec, c in Lgov_counts.items():
        gvec = tuple(x - 1 for x in Lvec)
        O = n - 3 - sum(gvec)
        Lgov_as_gaps[gvec + (O,)] += c
    ok_gov_matches = (Lgov_as_gaps == gap_counts)

    return {
        'n': n, 'total': total, 'n_topologies': n_topologies,
        'ok_a_uniform_topology': ok_a,
        'ok_b_uniform_gaps': ok_b, 'ok_b_value_matches_(n-3)!': ok_b_value,
        'ok_independence_sigma_gaps': ok_independence,
        'ok_governing_source_reindex_matches': ok_gov_matches,
    }


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [4, 5, 6, 7]
    all_ok = True
    for n in ns:
        res = check(n)
        print(res)
        all_ok &= all(v for k, v in res.items() if k.startswith('ok_'))
    print("ALL CHECKS PASS" if all_ok else "SOME CHECK FAILED")
