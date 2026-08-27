"""
Large-n Monte Carlo triangulation of Definition 4's actual model, for
K=7,8 (this front's new c_1(K) targets) -- a bonus check, not a substitute
for the exact closed forms derived in symbolic_pnn_via_composition_gf.py
and independently confirmed in c1_table_k7_k8.py. Direct simulation, own
random-number generation, reserved seed range only
(20260910000-20260910999).

Written fresh from Definition 4's prose description; no file from any
front read.
"""
import numpy as np
from fractions import Fraction


def simulate_pnn(n, K, trials, seed):
    rng = np.random.default_rng(seed)
    q1, q2 = n - 2, n - 1
    both_count = 0
    for _ in range(trials):
        f = rng.permutation(n)
        targets = rng.integers(0, n, size=K)
        f[:K] = targets

        def is_cyclic(q):
            seen = set()
            cur = q
            while True:
                cur = int(f[cur])
                if cur == q:
                    return True
                if cur in seen:
                    return False
                seen.add(cur)

        if is_cyclic(q1) and is_cyclic(q2):
            both_count += 1
    return both_count, trials


def nn7(nval):
    nv = Fraction(nval)
    return float((6435 * nv ** 7 + 17548 * nv ** 6 + 35958 * nv ** 5 + 55460 * nv ** 4
                  + 62565 * nv ** 3 + 48628 * nv ** 2 + 23148 * nv + 5040) / (51480 * nv ** 7))


def nn8(nval):
    nv = Fraction(nval)
    return float((24310 * nv ** 8 + 76627 * nv ** 7 + 186527 * nv ** 6 + 353609 * nv ** 5
                  + 513865 * nv ** 4 + 552592 * nv ** 3 + 412892 * nv ** 2 + 190224 * nv + 40320)
                 / (218790 * nv ** 8))


if __name__ == "__main__":
    print("Monte Carlo triangulation, K=7,8 (new), reserved seeds 20260910101-20260910104")
    print("=" * 90)
    configs = [
        (7, 300, 200000, 20260910101),
        (7, 3000, 30000, 20260910102),
        (8, 300, 200000, 20260910103),
        (8, 3000, 30000, 20260910104),
    ]
    predfn = {7: nn7, 8: nn8}
    for K, n, trials, seed in configs:
        cnt, tot = simulate_pnn(n, K, trials, seed)
        phat = cnt / tot
        target = predfn[K](n)
        se = (phat * (1 - phat) / tot) ** 0.5
        z = (phat - target) / se if se > 0 else float('nan')
        print(f"K={K}, n={n}, trials={trials}: phat={phat:.5f}  target={target:.5f}  z={z:+.2f}  (seed={seed})")
