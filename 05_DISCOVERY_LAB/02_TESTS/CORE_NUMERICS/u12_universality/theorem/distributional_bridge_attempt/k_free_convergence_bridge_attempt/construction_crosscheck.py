"""
Cross-check: does the "gap-vector + categorical destinations + Decomposition
Theorem" reduced model (built directly from the CITED facts -- Governing-
Source Reindexing, i.i.d. categorical destinations, landing-position-
uniform, and the general-K Full Cycle-Count Decomposition Theorem, all
already PROVED in THEOREM.md / general_k_decomposition_attempt/ATTEMPT.md,
none re-derived here) reproduce the SAME law of T as the literal, true,
from-scratch brute force of Definition 4 (true_definition4_bruteforce.py,
this directory)?

This is a pure sanity check that this front's own understanding/use of the
cited facts is correct -- it is NOT needed for Theorem A's proof (which
cites those facts directly) but is included because this archive's
convention requires independent verification of every claim relied upon.

Reduced-model sampler (Monte Carlo, reserved seeds -- see bottom):
  1. Draw a uniform random K-subset of {1,...,n} (the "divider set"),
     sorted D_(1)<...<D_(K); L_j := D_(j)-D_(j-1) (D_(0):=0), j=1..K
     (0-indexed below as L_0,...,L_{K-1}); O := n-D_(K).
     [Governing-Source Reindexing, cited]
  2. p_i := L_i/n (i=0..K-1), p_D := O/n. For each source j=0,...,K-1,
     draw dest(j) i.i.d. categorical(p_0,...,p_{K-1},p_D).
     [i.i.d. categorical destinations, cited]
  3. S := set of s with dest-chase from s returning to s before DEAD.
  4. For s in S: k_s := uniform random position in {1,...,L_s}
     (independently over s in S) -- landing position within the arc.
     [landing-position-uniform, cited] V_s := L_s - k_s + 1.
  5. T := O + sum_{s in S} V_s.  [Decomposition Theorem, cited]

No code from any other front is used; written fresh from the cited
theorem statements only.
"""
import math
import random
from collections import Counter

from true_definition4_bruteforce import exact_T_distribution


def sample_reduced_T(n, K, rng):
    # step 1: uniform K-subset of {1,...,n} via random.sample
    dividers = sorted(rng.sample(range(1, n + 1), K))
    Ls = []
    prev = 0
    for d in dividers:
        Ls.append(d - prev)
        prev = d
    O = n - dividers[-1]
    assert sum(Ls) + O == n

    # step 2: categorical destinations
    weights = Ls + [O]  # index K = DEAD
    dest = [rng.choices(range(K + 1), weights=weights, k=1)[0] for _ in range(K)]

    # step 3: find S = union of cycles of the functional graph on {0,...,K-1}
    # induced by dest, absorbing at K (=DEAD)
    S = set()
    for start in range(K):
        path = []
        x = start
        seen_this_path = set()
        while x < K and x not in seen_this_path:
            seen_this_path.add(x)
            path.append(x)
            x = dest[x]
        if x < K and x in seen_this_path:
            # found a cycle; the cycle is path[idx:] where path[idx]==x
            idx = path.index(x)
            for p in path[idx:]:
                S.add(p)
        # else: hit DEAD or merged into an already-known trajectory; either
        # way, cycle membership (if any) will be found when we process the
        # actual cycle nodes as `start` values themselves, so no action
        # needed here beyond what's already recorded.

    # step 4+5
    T = O
    for s in S:
        k_s = rng.randint(1, Ls[s])
        V_s = Ls[s] - k_s + 1
        T += V_s
    return T


def empirical_pmf(n, K, trials, seed):
    rng = random.Random(seed)
    c = Counter()
    for _ in range(trials):
        T = sample_reduced_T(n, K, rng)
        c[T] += 1
    return c


if __name__ == "__main__":
    RESERVED_SEED_BASE = 20260933100  # inside this front's reserved range
    cases = [(4, 1), (5, 1), (4, 2), (5, 2), (6, 2), (5, 3), (6, 3)]
    trials = 400000
    print(f"{'n':>3} {'K':>3} {'exact E[T]/n':>14} {'MC E[T]/n':>12} {'max |pmf diff|':>16} {'trials':>8}")
    for idx, (n, K) in enumerate(cases):
        exact_counts, exact_total = exact_T_distribution(n, K)
        exact_mean = sum(k * c for k, c in exact_counts.items()) / exact_total
        exact_pmf = {k: c / exact_total for k, c in exact_counts.items()}

        seed = RESERVED_SEED_BASE + idx
        mc_counts = empirical_pmf(n, K, trials, seed)
        mc_mean = sum(k * c for k, c in mc_counts.items()) / trials
        mc_pmf = {k: c / trials for k, c in mc_counts.items()}

        all_keys = set(exact_pmf) | set(mc_pmf)
        max_diff = max(abs(exact_pmf.get(k, 0.0) - mc_pmf.get(k, 0.0)) for k in all_keys)
        print(f"{n:>3} {K:>3} {exact_mean/n:>14.6f} {mc_mean/n:>12.6f} {max_diff:>16.6f} {trials:>8} (seed={seed})")
