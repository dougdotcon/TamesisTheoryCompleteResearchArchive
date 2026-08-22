"""
Referee check #3: raw finite-n simulation of the K=1 model (Definition 4,
K=1: one uniformly random index of a uniform permutation pi of [n] is
rerouted to a uniform target), completely independent of any of the
continuum/PD(1) machinery. Computes the FULL cyclic-mass fraction
(not just P(x0 cyclic)) for many trials at large n, and compares its
empirical distribution to the claimed limiting density f(x) = 2x on (0,1)
(THEOREM.md Lemma 2, S5.3) via a Kolmogorov-Smirnov test against the CDF
F(x) = x^2.

This is a first-principles check: no PD(1)/GEM stick-breaking assumed,
no exploration-process heuristic used -- literal permutation + reroute,
literal cycle-count on the resulting functional graph.
"""
import numpy as np
from scipy import stats

def cyclic_mass_fraction(n, rng):
    pi = rng.permutation(n)  # pi[i] = image of i, 0-indexed
    i_star = rng.integers(0, n)
    U = rng.integers(0, n)
    f = pi.copy()
    f[i_star] = U
    # find cyclic points: standard functional-graph rho-detection via
    # "does iterating from x eventually return to x" -- equivalently,
    # points that lie on some cycle of f. Use the classic method:
    # a point is cyclic iff it is reachable from itself, detectable by
    # the "two-pointer"/tortoise-hare per start, but for O(n) total we
    # instead find all cycles by tracking visited/instack arrays.
    color = np.zeros(n, dtype=np.int8)  # 0 unvisited, 1 in-progress, 2 done
    on_cycle = np.zeros(n, dtype=bool)
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = f[x]
        if color[x] == 1:
            # found a new cycle starting at x within 'path'
            idx = path.index(x)
            for p in path[idx:]:
                on_cycle[p] = True
        for p in path:
            color[p] = 2
    return on_cycle.sum() / n


if __name__ == "__main__":
    rng = np.random.default_rng(31415926)
    n = 4000
    trials = 4000
    samples = np.array([cyclic_mass_fraction(n, rng) for _ in range(trials)])
    print(f"n={n} trials={trials}")
    print(f"mean(M1) empirical = {samples.mean():.5f}  target (Lemma2 K=1 mean) = {2/3:.5f}")

    # KS test against F(x) = x^2 (density 2x)
    D, p = stats.kstest(samples, lambda x: x**2)
    print(f"KS vs F(x)=x^2 (density 2x):  D={D:.5f}  p={p:.4f}")

    # histogram-based sanity check
    hist, edges = np.histogram(samples, bins=10, range=(0,1), density=True)
    mids = 0.5*(edges[:-1]+edges[1:])
    print("bin-mid  empirical-density  target-density(2x)")
    for m, h in zip(mids, hist):
        print(f"{m:.2f}     {h:.3f}              {2*m:.3f}")
