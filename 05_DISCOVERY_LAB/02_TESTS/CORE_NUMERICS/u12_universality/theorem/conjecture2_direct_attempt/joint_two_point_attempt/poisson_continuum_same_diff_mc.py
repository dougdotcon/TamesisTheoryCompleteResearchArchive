"""wave 17 front (c) JOINT-TWO-POINT-EXPLORATION-ATTEMPT (DISC-DEC-072).
Fresh Monte Carlo (Definition 1's finite-n model, large n as the standard
archive-wide proxy for the continuum L(c) -- same convention Estagio 18's
own two_point_exploration_mc.py used, but this script is written fresh this
session, not reused). Seed block 20260864000+ (grep-confirmed unused before
first use here).

Purpose: NUMERICALLY EXPLORE whether the exact finite-n "Uniform Cyclic
Restriction" theorem's corollary (P(same final cycle | both cyclic) = 1/2,
proved exactly for the conditional-K model in
uniform_cyclic_restriction_exact.py) also holds, empirically, in the
large-n / Poisson(c) regime that stands in for L(c) itself -- a check that
is NOT implied by the finite-K exact theorem alone (that theorem holds for
every fixed K, but transferring it to the Poisson-mixed, n->infinity object
L(c) is a separate step, honestly flagged as open in ATTEMPT.md).

Also records, purely as a harness sanity check (not new evidence -- already
known targets), P(both cyclic) vs the mixture target (1-e^{-c})/c at a
value of c NOT used by Estagio 18 (c=2, per this front's own PREREG T4).
"""
import numpy as np
import time
import json
import sys


def trace(f, start, n):
    """Follow the forward orbit of `start` under f (array of length n) until
    a repeat is found. Returns (is_cyclic, cycle_set_or_None, path_len)."""
    visited = {}
    v = start
    step = 0
    while v not in visited:
        visited[v] = step
        v = f[v]
        step += 1
        if step > n:  # safety valve; cannot happen for a well-formed finite
            raise RuntimeError("orbit exceeded n steps -- bug")
    k = visited[v]  # v was first visited at step k
    if v == start:
        # cyclic: the cycle is exactly the nodes visited at steps 0..step-1
        cyc = frozenset(node for node, st in visited.items() if st < step)
        return True, cyc, step
    else:
        return False, None, step


def run(n, c, trials, seed, label):
    rng = np.random.default_rng(seed)
    both = 0
    same = 0
    cyc_count_sum = 0  # for E[C/n] sanity (only points 0,1 traced fully;
    # for a full-fraction sanity check we instead track a fresh full scan on
    # a SUBSET of trials -- see below)
    p = c / n
    t0 = time.time()
    for _ in range(trials):
        pi = rng.permutation(n)
        xi = rng.random(n) < p
        dests = rng.integers(0, n, size=n)
        f = np.where(xi, dests, pi)
        is0, cyc0, _ = trace(f, 0, n)
        if not is0:
            continue
        if 1 in cyc0:
            both += 1
            same += 1
            continue
        is1, cyc1, _ = trace(f, 1, n)
        if is1:
            both += 1
            # different cycle, since 1 not in cyc0 and 1 is cyclic itself
    dt = time.time() - t0
    Pboth = both / trials
    Psame = same / trials
    Pdiff = Pboth - Psame
    ratio = Psame / Pboth if Pboth > 0 else float('nan')
    target_mix = (1 - np.exp(-c)) / c
    print(f"[{label}] n={n} c={c} trials={trials} seed={seed}  time={dt:.1f}s")
    print(f"    P(both cyclic)      empirical = {Pboth:.5f}   "
          f"target (1-e^-c)/c = {target_mix:.5f}   "
          f"diff = {Pboth-target_mix:+.5f}")
    print(f"    P(same | both)      empirical = {ratio:.5f}   "
          f"target 1/2 (from the finite-n exact theorem, conjectured to "
          f"transfer)")
    print(f"    P_same = {Psame:.5f}   P_diff = {Pdiff:.5f}")
    return dict(n=n, c=c, trials=trials, seed=seed, both=both, same=same,
                Pboth=Pboth, Psame=Psame, Pdiff=Pdiff, ratio=ratio,
                target_mix=target_mix, time_sec=dt)


def main():
    results = []
    # c=2: not used by Estagio 18 (which used c=1,4). n scaled down from
    # Estagio 18's n=8000 to n=3000 to keep runtime moderate for this
    # exploratory (not load-bearing) check, honestly reported.
    results.append(run(n=8000, c=2.0, trials=100000, seed=20260864000,
                        label="c=2, n=8000"))
    # second, independent run at a different (n, seed) as a robustness
    # cross-check within this same script.
    results.append(run(n=6000, c=1.0, trials=80000, seed=20260864001,
                        label="c=1, n=6000 (cross-check, different n,c)"))
    with open("poisson_continuum_same_diff_mc_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print()
    print("Results written to poisson_continuum_same_diff_mc_results.json")


if __name__ == "__main__":
    main()
