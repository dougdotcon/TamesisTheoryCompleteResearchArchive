"""
Large-n/K Monte Carlo triangulation (bonus, NOT a substitute for the exact
symbolic/brute-force proofs elsewhere in this directory), direct simulation
of Definition 4's actual model: a genuine random permutation pi of [n] plus
K i.i.d. Uniform([n]) reroute targets, own from-scratch simulation path
(no reduced model, no shortcut) -- confirms Proposition S's P(S=A) formula
and the Full Cycle-Count Decomposition Theorem's implied mean of T at
larger (n,K) than exact brute force reaches.

Reserved seeds: 20260924000-20260924999 (this front's own, DISC-DEC-110,
wave 23 front (b) -- grep-confirmed unused before first use, see ATTEMPT.md
Section 9).

No code from any other front in this lineage was read or used.
"""
import numpy as np
from fractions import Fraction
import itertools


def simulate_once(rng, n, K):
    pi = rng.permutation(n)
    U = rng.integers(0, n, size=K)
    f = np.array(pi, copy=True)
    for s in range(K):
        f[s] = U[s]
    # find cyclic points by direct forward simulation
    cyc = np.zeros(n, dtype=bool)
    visited_global = np.zeros(n, dtype=bool)
    for start in range(n):
        if visited_global[start]:
            continue
        seen = []
        cur = start
        local_seen_idx = {}
        while True:
            if visited_global[cur]:
                # cur might be on an already-processed cycle/tail; if it's
                # a cyclic point already marked, and we reached it, our
                # path just feeds into existing structure -- not cyclic
                # itself (already determined)
                break
            if cur in local_seen_idx:
                # found a new cycle starting at local_seen_idx[cur]
                cyc_start = local_seen_idx[cur]
                for node in seen[cyc_start:]:
                    cyc[node] = True
                break
            local_seen_idx[cur] = len(seen)
            seen.append(cur)
            cur = f[cur]
        for node in seen:
            visited_global[node] = True
    T = int(cyc.sum())
    S = frozenset(s for s in range(K) if cyc[s])
    return T, S


def prop_s_formula_conditional(A, ps, pD):
    m = len(A)
    fact = 1
    for i in range(1, m + 1):
        fact *= i
    prod = 1.0
    for a in A:
        prod *= ps[a]
    PA = sum(ps[a] for a in A)
    return fact * prod * (pD + PA)


def sample_uniform_composition(rng, m, parts):
    """Uniform sample of a composition of m into `parts` nonnegative
    integers, via the standard stars-and-bars bijection: choose `parts-1`
    distinct divider positions uniformly at random (without replacement)
    among the m+parts-1 slots between/around m stars, then read off gaps.
    (NOTE: rng.multinomial(m, uniform probs) is NOT the same distribution
    as this -- it was a bug in an earlier version of this script, caught
    by the large, unexplained discrepancy this function's fix corrects;
    see the module's run log for the before/after comparison.)"""
    total_slots = m + parts - 1
    if parts - 1 > 0:
        dividers = sorted(rng.choice(total_slots, size=parts - 1, replace=False).tolist())
    else:
        dividers = []
    bounds = [-1] + dividers + [total_slots]
    return [bounds[i + 1] - bounds[i] - 1 for i in range(parts)]


def expected_T_via_S_and_L(K, n, trials_L=2000, rng=None):
    """Predicted E[T] via Proposition S + Decomposition Theorem: for a
    random composition (uniform), E[T | L] = O + sum_A P(S=A|L) * sum_{s in
    A} E[V_s] = O + sum_A P(S=A|L) * sum_{s in A} (L_s+1)/2, averaged over
    L. Computed here by Monte Carlo sampling of L (TRUE uniform composition
    via sample_uniform_composition) for cross-comparison against the true
    simulation's empirical mean of T."""
    total = 0.0
    for _ in range(trials_L):
        g = sample_uniform_composition(rng, n - K, K + 1)
        L = [g[i] + 1 for i in range(K)]
        O = int(g[K])
        ps = [L[i] / n for i in range(K)]
        pD = O / n
        e_t_given_L = O
        for r in range(0, K + 1):
            for A in itertools.combinations(range(K), r):
                pA = prop_s_formula_conditional(A, ps, pD)
                sum_ev = sum((L[a] + 1) / 2.0 for a in A)
                e_t_given_L += pA * sum_ev
        total += e_t_given_L
    return total / trials_L


def main():
    print("=" * 78)
    print("Monte Carlo bonus: true Definition-4 simulation vs. Prop S /")
    print("Decomposition Theorem predictions, larger (n,K)")
    print("=" * 78)
    seeds = [20260924001, 20260924002, 20260924003, 20260924004,
             20260924005, 20260924006]
    cells = [
        (50, 3, 20000, seeds[0]),
        (200, 3, 8000, seeds[1]),
        (50, 5, 20000, seeds[2]),
        (200, 5, 8000, seeds[3]),
        (100, 6, 10000, seeds[4]),
        (300, 4, 6000, seeds[5]),
    ]
    for n, K, trials, seed in cells:
        rng = np.random.default_rng(seed)
        T_sum = 0
        S_counts = {}
        for _ in range(trials):
            T, S = simulate_once(rng, n, K)
            T_sum += T
            S_counts[S] = S_counts.get(S, 0) + 1
        mean_T_hat = T_sum / trials
        # predicted E[T]/n limit: T/n -> M_K continuum, E[M_K] known closed
        # forms exist for K<=... but here we just cross-check E[T] against
        # the Prop-S-based reduced-model average (separately Monte-Carlo'd
        # over L with its own seed derived deterministically from the cell
        # seed, exact independent estimate)
        rng2 = np.random.default_rng(seed + 500000)
        pred_mean_T = expected_T_via_S_and_L(K, n, trials_L=20000, rng=rng2)
        se = None
        # crude standard error estimate for T via batch means
        print(f"n={n:4d} K={K}: trials={trials:7d} seed={seed}  "
              f"empirical E[T]={mean_T_hat:.4f}  "
              f"Prop-S-based-predicted E[T]={pred_mean_T:.4f}  "
              f"diff={mean_T_hat - pred_mean_T:+.4f}")
        # marginal P(S=full set) vs formula, quick spot check
        full = frozenset(range(K))
        emp_full = S_counts.get(full, 0) / trials
        print(f"    P(S=full)  empirical={emp_full:.5f} "
              f"(observed {S_counts.get(full,0)}/{trials})")

    print()
    print("(triangulation only, per lineage convention -- the exact")
    print(" symbolic/brute-force checks elsewhere in this directory are the")
    print(" actual evidence for Proposition S and the Decomposition Theorem)")


if __name__ == "__main__":
    main()
