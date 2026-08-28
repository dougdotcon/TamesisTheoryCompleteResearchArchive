"""
K4-FULL-CDF-ATTEMPT: bonus Monte Carlo triangulation (not a substitute
for the exact derivation/verification of Sections 2-6).  Direct
simulation of Definition 4's actual K=4 model: own random permutation
pi (via numpy Fisher-Yates) and own i.i.d. targets U0..U3, NOT the
reduced/decomposition model -- an end-to-end sanity check on the whole
chain from Definition 4 down to Proposicao D4.

Reserved seeds: 20260926001-20260926006 (this front's own range,
20260926000-20260926999, grep-confirmed unused before first use -- see
ATTEMPT.md Section 9).
"""
import numpy as np
import sympy as sp
import pickle
import math

n_sym, k_sym = sp.symbols('n k')
with open('F_generic.pkl', 'rb') as f:
    F = pickle.load(f)

K = 4


def D4_pred(nv, kv):
    return float(sp.Rational(F.subs({n_sym: sp.Integer(nv), k_sym: sp.Integer(kv)})))


def cyclic_count(f, n):
    state = np.zeros(n, dtype=np.int8)
    cyclic = np.zeros(n, dtype=bool)
    for start in range(n):
        if state[start] != 0:
            continue
        path = []
        pos = {}
        cur = start
        while state[cur] == 0:
            state[cur] = 1
            pos[cur] = len(path)
            path.append(cur)
            cur = f[cur]
        if state[cur] == 1:
            idx = pos[cur]
            for node in path[idx:]:
                cyclic[node] = True
        for node in path:
            state[node] = 2
    return int(cyclic.sum())


def simulate(n, trials, seed):
    rng = np.random.default_rng(seed)
    Ts = np.empty(trials, dtype=np.int64)
    for i in range(trials):
        pi = rng.permutation(n)
        f = pi.copy()
        U = rng.integers(0, n, size=K)
        f[:K] = U
        Ts[i] = cyclic_count(f, n)
    return Ts


if __name__ == "__main__":
    cells = [
        (100, 200000, 25, 20260926001),
        (100, 200000, 50, 20260926002),
        (100, 200000, 75, 20260926003),
        (500, 30000, 125, 20260926004),
        (500, 30000, 250, 20260926005),
        (500, 30000, 375, 20260926006),
    ]
    print(f"{'n':>6} {'trials':>8} {'k':>6} {'D4 pred':>10} {'MC est':>10} {'s.e.':>8} {'z':>7}")
    for n, trials, k, seed in cells:
        Ts = simulate(n, trials, seed)
        est = float(np.mean(Ts <= k))
        se = math.sqrt(est * (1 - est) / trials) if 0 < est < 1 else 1e-9
        pred = D4_pred(n, k)
        z = (est - pred) / se if se > 0 else float('nan')
        print(f"{n:>6} {trials:>8} {k:>6} {pred:>10.6f} {est:>10.6f} {se:>8.5f} {z:>7.2f}")
