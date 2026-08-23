"""mc_check.py -- Monte Carlo validation of chain.py against the RAW model.

This is the one place randomness is used.  It simulates Definition 1 of
THEOREM.md literally (uniform permutation pi, i.i.d. Bernoulli(c/n) marks,
uniform reroute targets, count cyclic points by cycle detection on the
functional digraph) and compares the empirical cyclic fraction against
chain.py's phi_mixed_exact -- an entirely different computation.

Seed: numpy.random.SeedSequence entropy drawn fresh for this session,
      109988594598087819892849058742026646086
      (recorded in ATTEMPT.md SS0; no other randomness anywhere in this front).
"""

from fractions import Fraction
import numpy as np
from chain import phi_mixed_exact, phi_condK_exact

ENTROPY = 109988594598087819892849058742026646086


def cyclic_fraction(f, n):
    """Number of cyclic points of the mapping f: [n]->[n] (0-indexed)."""
    # standard iterative colouring: 0 unvisited, 1 in progress, 2 done
    color = np.zeros(n, dtype=np.int8)
    oncyc = np.zeros(n, dtype=bool)
    for start in range(n):
        if color[start]:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = f[x]
        if color[x] == 1:                     # found a new cycle through x
            i = path.index(x)
            for y in path[i:]:
                oncyc[y] = True
        for y in path:
            color[y] = 2
    return int(oncyc.sum())


def mc_phi(n, c, trials, rng):
    q = c / n
    tot = 0
    for _ in range(trials):
        pi = rng.permutation(n)
        f = pi.copy()
        mask = rng.random(n) < q
        if mask.any():
            f[mask] = rng.integers(0, n, size=int(mask.sum()))
        tot += cyclic_fraction(f, n)
    return tot / (trials * n)


def mc_phi_condK(n, K, trials, rng):
    tot = 0
    for _ in range(trials):
        pi = rng.permutation(n)
        f = pi.copy()
        S = rng.choice(n, size=K, replace=False)
        f[S] = rng.integers(0, n, size=K)
        tot += cyclic_fraction(f, n)
    return tot / (trials * n)


if __name__ == "__main__":
    ss = np.random.SeedSequence(ENTROPY)
    rng = np.random.default_rng(ss)
    print("=== mc_check.py : raw-model Monte Carlo vs chain.py ===")
    print("SeedSequence entropy =", ENTROPY)
    print()
    T = 200000
    print("phi(n,c):   n    c      chain(exact)      MC(%d)        |diff|   2se" % T)
    for n, c in [(6, 1), (6, 3), (10, 2), (10, 7), (20, 5), (20, 20), (40, 12)]:
        ex = float(phi_mixed_exact(n, Fraction(c)))
        mc = mc_phi(n, c, T, rng)
        se = (ex * (1 - ex) / (T * n)) ** 0.5 * 2      # crude, points correlated
        print("           %3d %5s   %.9f    %.9f   %.2e  ~%.1e"
              % (n, c, ex, mc, abs(ex - mc), se))
    print()
    print("phi_n^{(K)}: n    K      chain(exact)      MC(%d)        |diff|" % T)
    for n, K in [(6, 2), (10, 3), (10, 9), (20, 6), (30, 15), (40, 40)]:
        ex = float(phi_condK_exact(n, K))
        mc = mc_phi_condK(n, K, T, rng)
        print("           %3d %5d   %.9f    %.9f   %.2e"
              % (n, K, ex, mc, abs(ex - mc)))
