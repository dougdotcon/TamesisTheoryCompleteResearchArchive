"""
R_MC3 (pre-registered): Monte Carlo check of the derived RECIPE itself
(not independent of Step A/B by construction -- confirmatory of internal
consistency, exactly as conjecture1_k3_attempt's own R_MC3).

Draw (m1,m2,m3,m4) ~ uniform on the 4-simplex (via Dirichlet(1,1,1,1,1),
taking the first 4 coordinates -- Lemma 1). Draw u1,u2,u3,u4 ~ Unif(0,1)
i.i.d. Classify the raw (target1,...,target4) configuration exactly as
the continuum model does; find cycles among {1,2,3,4}; compute M_4 via
THIS FRONT'S OWN derived formula (M_4 = 1 - sum(off-cycle m) - sum(on-cycle
positions), positions read directly off where each u_i falls within its
target region). Compare the resulting empirical density of M_4 against
8x(1-x^2)^3 via KS test -- an independent numerical sanity check on the
bookkeeping (arithmetic, region boundaries), as opposed to the discrete
correspondence already validated in mechanism_check_k4.py.
"""
import numpy as np
from scipy import stats
import json

K = 4


def cycles_of(g, nodes=(0, 1, 2, 3)):
    found = []
    classified = set()
    for start in nodes:
        if start in classified:
            continue
        path = [start]
        cur = start
        seen = {start: 0}
        while True:
            nxt = g[cur]
            if nxt == 'OUT':
                classified.update(path)
                break
            if nxt in classified:
                classified.update(path)
                break
            if nxt in seen:
                found.append(tuple(path[seen[nxt]:]))
                classified.update(path)
                break
            path.append(nxt)
            seen[nxt] = len(path) - 1
            cur = nxt
    return found


def target_cdf(x):
    return 1 - (1 - x ** 2) ** 4


def run(N, seed):
    rng = np.random.default_rng(seed)
    # (m1,...,m5) ~ Dirichlet(1,1,1,1,1) -> (m1,...,m4) uniform on the 4-simplex
    dirich = rng.dirichlet([1, 1, 1, 1, 1], size=N)
    m = dirich[:, :K]  # shape (N,4)
    u = rng.uniform(0, 1, size=(N, K))

    M4 = np.empty(N)
    cum = np.cumsum(m, axis=1)  # boundaries [m1, m1+m2, m1+m2+m3, m1+m2+m3+m4]

    for k in range(N):
        mvals = m[k]
        cvals = cum[k]
        target = [None] * K
        pos = [None] * K
        for i in range(K):
            ui = u[k, i]
            placed = False
            prev_c = 0.0
            for r in range(K):
                if ui < cvals[r]:
                    target[i] = r
                    pos[i] = ui - prev_c
                    placed = True
                    break
                prev_c = cvals[r]
            if not placed:
                target[i] = 'OUT'
                pos[i] = None

        g = {i: target[i] for i in range(K)}
        cycs = cycles_of(g)

        L = mvals.sum()
        inert = 1 - L
        new_mass = 0.0
        for cyc in cycs:
            for i in cyc:
                t = g[i]
                new_mass += (mvals[t] - pos[i])
        M4[k] = inert + new_mass

    ks = stats.kstest(M4, target_cdf)
    mean = M4.mean()
    se = M4.std(ddof=1) / np.sqrt(N)
    target_mean = 128.0 / 315.0
    z = (mean - target_mean) / se
    print(f"N={N}: KS D={ks.statistic:.5f} p={ks.pvalue:.4f}  mean={mean:.6f} +/- {se:.6f} "
          f"vs 128/315={target_mean:.6f} (z={z:+.2f})")
    return {'N': N, 'ks_D': float(ks.statistic), 'ks_p': float(ks.pvalue),
            'mean': float(mean), 'se': float(se), 'z': float(z)}


if __name__ == "__main__":
    print("=" * 78)
    print("R_MC3 -- Monte Carlo check of the derived continuum recipe (K=4)")
    print("=" * 78)
    r = run(2_000_000, 20260850030)
    with open("mc_recipe_check_k4_results.json", "w") as fh:
        json.dump(r, fh, indent=2)
