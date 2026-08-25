"""
Direct verification of the claimed exact lower bound (ATTEMPT.md
Section 3.3, "intact-block certificate"):

   {none of the ell points of the shared background cycle got
    independently selected for reroute}  ==>  {both point0 and point1
    are cyclic under f}

and that this event has probability EXACTLY (1-c/n)^ell in the
finite-n model (a trivial Bernoulli calculation), hence
P(both cyclic | same cycle, ell) >= (1-c/n)^ell exactly, for every
finite n -- so in particular the CONTINUUM target for this lower bound
is e^{-c*ell/n} as n->infinity, NOT e^{-c*(ell/n)^2} (Theorem 1's own
MARGINAL single-point formula, an unrelated, larger quantity called
"guessA" in two_point_exploration_mc.py -- that script's "guessA" name
was a MISLABEL of what it actually computes; see the Honest process
note in ATTEMPT.md Section 3.5).

This script (a) checks the logical implication directly, trial by
trial, on every same-cycle sample (must NEVER be violated -- any
violation is a bug), and (b) checks the aggregate probability of the
intact-block event against the exact finite-n formula (1-c/n)^ell.
"""
import numpy as np
from collections import deque

def cyclic_mask(f, n):
    indeg = np.bincount(f, minlength=n)
    removed = np.zeros(n, dtype=bool)
    q = deque(int(i) for i in np.nonzero(indeg == 0)[0])
    while q:
        i = q.popleft()
        removed[i] = True
        j = int(f[i])
        indeg[j] -= 1
        if indeg[j] == 0 and not removed[j]:
            q.append(j)
    return ~removed

def pi_cycle_containing_0(pi, n):
    members = [0]
    y = pi[0]
    while y != 0:
        members.append(y)
        y = pi[y]
    return members  # list of labels in the cycle containing 0

def run(c, n, trials, seed):
    rng = np.random.default_rng(seed)
    violations = 0
    intact_count = 0
    same_cycle_trials = 0
    intact_prob_check = []  # (ell, was_intact)
    for t in range(trials):
        pi = rng.permutation(n)
        members = pi_cycle_containing_0(pi, n)
        ell = len(members)
        if 1 not in members:
            continue
        same_cycle_trials += 1
        reroute = rng.random(n) < (c / n)
        targets = rng.integers(0, n, size=n)
        f = np.where(reroute, targets, pi)
        intact = not reroute[np.array(members)].any()
        cmask = cyclic_mask(f, n)
        both_cyclic = bool(cmask[0]) and bool(cmask[1])
        if intact:
            intact_count += 1
            if not both_cyclic:
                violations += 1
                print(f"  VIOLATION at trial {t}: intact block but not both cyclic! ell={ell}")
        intact_prob_check.append((ell, intact, both_cyclic))
    return same_cycle_trials, intact_count, violations, intact_prob_check

if __name__ == "__main__":
    c, n, trials, seed = 1.0, 4000, 20000, 20260858012
    same_n, intact_n, violations, checks = run(c, n, trials, seed)
    print(f"c={c} n={n} trials={trials} seed={seed}")
    print(f"same-cycle trials: {same_n}, intact-block among them: {intact_n}")
    print(f"LOGICAL VIOLATIONS (intact but not both cyclic): {violations}  (must be 0)")

    # aggregate check of P(intact | ell) vs (1-c/n)^ell, bucketed -- AND, in the
    # SAME buckets from the SAME trials, P(both cyclic | ell), to directly confirm
    # (within one self-consistent run) that emp_P(both) >= emp_P(intact) always,
    # exactly as the pointwise logical implication requires.
    import collections
    buckets = collections.defaultdict(lambda: [0, 0, 0])  # count, intact_hits, both_hits
    for ell, intact, both in checks:
        b = int(8 * ell / n)
        b = min(b, 7)
        buckets[b][0] += 1
        buckets[b][1] += int(intact)
        buckets[b][2] += int(both)
    print(f"\n{'bucket':>7} {'ell_mid/n':>10} {'n':>6} {'emp_P(intact)':>14} {'(1-c/n)^ell':>14} {'emp_P(both)':>12} {'both>=intact?':>13}")
    for b in sorted(buckets):
        cnt, intact_hits, both_hits = buckets[b]
        mid = (b + 0.5) / 8
        ell_approx = mid * n
        target = (1 - c / n) ** ell_approx
        emp_intact = intact_hits / cnt
        emp_both = both_hits / cnt
        print(f"{b:7d} {mid:10.3f} {cnt:6d} {emp_intact:14.5f} {target:14.5f} {emp_both:12.5f} {str(emp_both>=emp_intact):>13}")
