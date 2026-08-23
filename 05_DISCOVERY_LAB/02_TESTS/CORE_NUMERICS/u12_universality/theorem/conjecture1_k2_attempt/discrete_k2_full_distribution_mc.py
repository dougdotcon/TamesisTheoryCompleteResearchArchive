"""R4: raw, from-scratch simulation of the DISCRETE finite-n K=2 model
(THEOREM.md Definition 4: uniform permutation of [n], two fixed rerouted
indices 0,1, i.i.d. uniform targets), for large n, as an independent
cross-check of the derived continuum density f_{M_2}(x)=4x(1-x^2) that
does NOT reuse any of this document's continuum machinery (no PD(1)
stick-breaking, no (m1,m2)/group decomposition -- pure discrete
functional-graph simulation + a generic cyclic-point finder).

Seed: numpy.random.SeedSequence(20260835000), spawned with a distinct
child from R3's use of the same root (spawn(2) below).
"""
import json
import time
import numpy as np
from scipy.stats import kstest

SEED0 = 20260835000
root = np.random.SeedSequence(SEED0)
# spawn two independent children off the same root: [0] already consumed
# directly by R3 (root itself, via default_rng(root)); use spawn here to
# get a demonstrably distinct child stream for R4.
child = root.spawn(1)[0]
rng = np.random.default_rng(child)


def cyclic_fraction(f, n):
    """f: length-n int array, functional graph i -> f[i]. Return count of
    cyclic points, via iterative 3-color path marking (O(n), no
    recursion)."""
    color = np.zeros(n, dtype=np.int8)  # 0 unvisited, 1 on-path, 2 done
    cyclic = np.zeros(n, dtype=bool)
    path = np.empty(n, dtype=np.int64)
    for start in range(n):
        if color[start] != 0:
            continue
        plen = 0
        v = start
        while color[v] == 0:
            color[v] = 1
            path[plen] = v
            plen += 1
            v = f[v]
        if color[v] == 1:
            # found a new cycle: v is on current path; find its index
            # scan path backward for v (path[plen-1..0])
            k = plen - 1
            while path[k] != v:
                k -= 1
            for idx in range(k, plen):
                cyclic[path[idx]] = True
        # mark whole path as done
        for idx in range(plen):
            color[path[idx]] = 2
    return int(cyclic.sum())


def run(n, trials, rng):
    fracs = np.empty(trials)
    t0 = time.time()
    for t in range(trials):
        perm = rng.permutation(n)
        f = perm.copy()
        u0 = int(rng.integers(0, n))
        u1 = int(rng.integers(0, n))
        f[0] = u0
        f[1] = u1
        c = cyclic_fraction(f, n)
        fracs[t] = c / n
    dt = time.time() - t0
    return fracs, dt


def main():
    n = 10000
    trials = 10000
    print(f"Running discrete K=2 simulation: n={n}, trials={trials} ...")
    fracs, dt = run(n, trials, rng)
    print(f"done in {dt:.1f}s")

    cdf_target = lambda t: 2 * t ** 2 - t ** 4  # F(x)=int_0^x 4u(1-u^2)du
    st = kstest(fracs, cdf_target)
    mean_mc = float(fracs.mean())
    sem_mc = float(fracs.std(ddof=1) / np.sqrt(trials))
    target_mean = 8.0 / 15
    z_mean = (mean_mc - target_mean) / sem_mc

    print(f"KS D={st.statistic:.5f} p={st.pvalue:.4f} (n_discrete={n}, trials={trials})")
    print(f"mean(M2/n)={mean_mc:.6f} +/- {sem_mc:.6f}  vs phi_2=8/15={target_mean:.6f}  "
          f"z={z_mean:+.2f}")

    out = dict(n=n, trials=trials, seed_root=SEED0,
               KS_D=float(st.statistic), KS_p=float(st.pvalue),
               mean_mc=mean_mc, sem_mc=sem_mc, target_mean=target_mean,
               z_mean=float(z_mean), runtime_sec=dt)
    with open(__file__.replace('.py', '.json'), 'w') as fh:
        json.dump(out, fh, indent=2)
    print("saved", __file__.replace('.py', '.json'))


if __name__ == "__main__":
    main()
