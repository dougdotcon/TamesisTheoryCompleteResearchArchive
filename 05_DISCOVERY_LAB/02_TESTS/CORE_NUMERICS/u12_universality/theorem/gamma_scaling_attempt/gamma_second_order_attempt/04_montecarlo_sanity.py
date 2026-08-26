"""
Independent Monte Carlo sanity check of Definition 1 (direct simulation
of pi, xi, U as specified) against the exact A_k-sum formula for
phi(n, gamma*n), at a moderate n where brute-force enumeration is
infeasible but direct simulation is cheap. Only place in this front
that consumes randomness -- uses numpy's SeedSequence with the
reserved block 20260872000-20260873000 (front's own reservation,
DISC-DEC-078 wave 18 front (b)).
"""
import numpy as np
import math
from fractions import Fraction as Fr

RESERVED_LO, RESERVED_HI = 20260872000, 20260873000


def A_k(k, n, q: Fr):
    total = Fr(0)
    for m in range(0, k + 1):
        binom = math.comb(k, m)
        prod = Fr(1)
        for i in range(1, m + 1):
            prod *= (1 - Fr(k - i, n))
        total += binom * q ** m * (1 - q) ** (k - m) * prod
    return total


def exact_nphi(n, q: Fr):
    return sum(A_k(k, n, q) for k in range(1, n + 1))


def simulate_once(n, gamma, rng):
    pi = rng.permutation(n)  # pi[i] in 0..n-1, treat as 0-indexed image of i
    xi = rng.random(n) < gamma
    U = rng.integers(0, n, size=n)
    f = np.where(xi, U, pi)
    # count cyclic points via functional graph cycle detection
    visited = np.zeros(n, dtype=np.int64)
    on_cycle = np.zeros(n, dtype=bool)
    stamp = 0
    for start in range(n):
        if visited[start]:
            continue
        stamp += 1
        path = []
        x = start
        while visited[x] == 0:
            visited[x] = stamp
            path.append(x)
            x = f[x]
        if visited[x] == stamp:
            idx = path.index(x)
            for y in path[idx:]:
                on_cycle[y] = True
    return on_cycle.sum()


if __name__ == "__main__":
    seed_seq = np.random.SeedSequence(RESERVED_LO)
    rng = np.random.default_rng(seed_seq)

    print("Monte Carlo sanity check of Definition 1 vs exact A_k-sum formula")
    print(f"(seed block reserved: {RESERVED_LO}-{RESERVED_HI}, entropy={seed_seq.entropy})")
    print("=" * 78)

    trials_list = [60_000]
    for n, gamma in [(60, Fr(1, 2)), (100, Fr(3, 10)), (150, Fr(7, 10))]:
        exact = exact_nphi(n, gamma) / n
        exact_f = float(exact)
        trials = trials_list[0]
        per_trial = np.empty(trials)
        for t in range(trials):
            per_trial[t] = simulate_once(n, float(gamma), rng) / n
        mc_mean = per_trial.mean()
        # proper empirical stderr across trials (accounts for within-trial
        # correlation among the n cyclic-point indicators, unlike a naive
        # independent-Bernoulli formula)
        se = 3 * per_trial.std(ddof=1) / math.sqrt(trials)
        print(f"n={n:>4} gamma={float(gamma):.3f}  exact phi={exact_f:.6f}  "
              f"MC phi={mc_mean:.6f} (+-{se:.6f}, {trials} trials, empirical 3*SEM)  "
              f"within band={abs(mc_mean-exact_f) < se}")
