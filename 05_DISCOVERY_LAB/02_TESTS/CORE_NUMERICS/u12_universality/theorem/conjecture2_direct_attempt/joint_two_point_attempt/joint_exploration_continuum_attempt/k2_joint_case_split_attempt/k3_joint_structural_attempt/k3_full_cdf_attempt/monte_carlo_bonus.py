"""
K3-FULL-CDF-ATTEMPT -- bonus large-n Monte Carlo triangulation of
Proposicao D3, direct simulation of Definition 4's K=3 model (own random
permutations and reroute targets -- not the reduced/decomposition model,
an independently-coded simulation path). NOT a substitute for the exact
results elsewhere in this front (decomposition_theorem.py,
symbolic_derivation_full_cdf.py, final_verification.py) -- reported only
as an additional triangulation, per this lineage's established
convention (cf. Estagio 35 Sec.7).

Reserved seed range for this front: 20260920000-20260920999 (confirmed
unused before first use -- see ATTEMPT.md Sec.9 for the grep check).
"""
import numpy as np
from fractions import Fraction


def F_conjectured(nval, kval):
    nval = Fraction(nval)
    kval = Fraction(kval)
    c2 = 3 * nval ** 2 - 9 * nval - 5
    c1 = 3 * nval ** 2 - 11 * nval - 2
    c0 = 3 * nval ** 4 - 12 * nval ** 3 + 12 * nval ** 2 + 2 * nval
    quartic = kval ** 4 - 4 * kval ** 3 - c2 * kval ** 2 + c1 * kval + c0
    D = nval ** 4 * (nval - 1) * (nval - 2)
    return float(kval * (kval + 1) * quartic / D)


def simulate_once(n, rng):
    pi = rng.permutation(n)
    f = pi.copy()
    U = rng.integers(0, n, size=3)
    f[0], f[1], f[2] = U[0], U[1], U[2]
    seen = np.full(n, -1, dtype=np.int64)
    cyc_count = 0
    for x in range(n):
        if seen[x] != -1:
            continue
        path = []
        pos_in_path = {}  # O(1) membership/index lookup (was an O(len) list scan)
        cur = x
        while seen[cur] == -1 and cur not in pos_in_path:
            pos_in_path[cur] = len(path)
            path.append(cur)
            cur = f[cur]
        if cur in pos_in_path:
            # closed a NEW cycle within this path: nodes from the repeat
            # point onward are cyclic, everything before is a non-cyclic
            # tail leading into it.
            idx = pos_in_path[cur]
            for p in path[:idx]:
                seen[p] = 0
            for p in path[idx:]:
                seen[p] = 1
                cyc_count += 1
        else:
            # reached an already-classified node (seen[cur] in {0,1}):
            # every node on THIS path is a tail leading into that
            # (distinct) region, hence NOT cyclic itself, regardless of
            # whether cur is cyclic or not.
            for p in path:
                seen[p] = 0
    return cyc_count


def run(n, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    Ts = np.empty(trials, dtype=np.int64)
    for i in range(trials):
        Ts[i] = simulate_once(n, rng)
    return Ts


if __name__ == "__main__":
    cells = [
        (200, 200_000, 20260920001),
        (2000, 30_000, 20260920002),
        (5000, 10_000, 20260920003),
    ]
    print(f"{'n':>6} {'trials':>8} {'k':>6}  {'D3 pred':>10} {'MC est':>10} {'s.e.':>8} {'z':>6}")
    for n, trials, seed in cells:
        Ts = run(n, trials, seed)
        for frac in (0.25, 0.5, 0.75):
            k = int(frac * n)
            pred = F_conjectured(n, k)
            est = float(np.mean(Ts <= k))
            se = (est * (1 - est) / trials) ** 0.5
            z = (est - pred) / se if se > 0 else float('nan')
            print(f"{n:>6} {trials:>8} {k:>6}  {pred:>10.6f} {est:>10.6f} {se:>8.5f} {z:>6.2f}")
