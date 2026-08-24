"""
R_MC3 (pre-registered): Monte Carlo check of the derived RECIPE itself
(not independent of Step A/B by construction -- confirmatory of internal
consistency, exactly as conjecture1_k2_attempt/ATTEMPT.md's own R5).

Draw (m1,m2,m3) ~ uniform on the simplex (via Dirichlet(1,1,1,1), taking
the first 3 coordinates -- Lemma 1). Draw u1,u2,u3 ~ Unif(0,1) i.i.d.
Classify the raw (target1,target2,target3) configuration exactly as the
continuum model does; find cycles among {1,2,3}; compute M_3 via THIS
FRONT'S OWN derived formula (M_3 = 1 - sum(off-cycle m) - sum(on-cycle
positions), positions read directly off where each u_i falls within its
target region). Compare the resulting empirical density of M_3 against
6x(1-x^2)^2 via KS test -- this exercises the exact same continuum
recipe the symbolic derivation integrates, as an independent numerical
sanity check on the bookkeeping (arithmetic, region boundaries, off-by-one
in the continuum -- as opposed to the discrete correspondence bug caught
and fixed in mechanism_check_k3.py).
"""
import numpy as np
from scipy import stats
import json


def cycles_of(g, nodes=(0, 1, 2)):
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
    return 1 - (1 - x ** 2) ** 3


def run(N, seed):
    rng = np.random.default_rng(seed)
    # (m1,m2,m3,m4) ~ Dirichlet(1,1,1,1) -> (m1,m2,m3) uniform on the simplex
    dirich = rng.dirichlet([1, 1, 1, 1], size=N)
    m = dirich[:, :3]  # shape (N,3)
    u = rng.uniform(0, 1, size=(N, 3))

    M3 = np.empty(N)
    cum = np.cumsum(m, axis=1)  # boundaries [m1, m1+m2, m1+m2+m3]

    for k in range(N):
        m1, m2, m3 = m[k]
        c1, c2, c3 = cum[k]
        # classify each u_i
        target = [None, None, None]
        pos = [None, None, None]  # position within target region, measured from start of region
        for i in range(3):
            ui = u[k, i]
            if ui < c1:
                target[i] = 0
                pos[i] = ui  # offset from 0
            elif ui < c2:
                target[i] = 1
                pos[i] = ui - c1
            elif ui < c3:
                target[i] = 2
                pos[i] = ui - c2
            else:
                target[i] = 'OUT'
                pos[i] = None

        g = {0: target[0], 1: target[1], 2: target[2]}
        cycs = cycles_of(g)

        L = m1 + m2 + m3
        inert = 1 - L
        new_mass = 0.0
        m_arr = [m1, m2, m3]
        for cyc in cycs:
            for i in cyc:
                t = g[i]
                # arc length = m_t - pos[i]  (continuum formula: distance
                # from position pos[i] forward to the source, which sits
                # at the END of region t, i.e. at offset m_t)
                new_mass += (m_arr[t] - pos[i])
        M3[k] = inert + new_mass

    ks = stats.kstest(M3, target_cdf)
    mean = M3.mean()
    se = M3.std(ddof=1) / np.sqrt(N)
    target_mean = 16.0 / 35.0
    z = (mean - target_mean) / se
    print(f"N={N}: KS D={ks.statistic:.5f} p={ks.pvalue:.4f}  mean={mean:.6f} +/- {se:.6f} "
          f"vs 16/35={target_mean:.6f} (z={z:+.2f})")
    return {'N': N, 'ks_D': float(ks.statistic), 'ks_p': float(ks.pvalue),
            'mean': float(mean), 'se': float(se), 'z': float(z)}


if __name__ == "__main__":
    print("=" * 78)
    print("R_MC3 -- Monte Carlo check of the derived continuum recipe (K=3)")
    print("=" * 78)
    r = run(2_000_000, 20260843030)
    with open("mc_recipe_check_k3_results.json", "w") as fh:
        json.dump(r, fh, indent=2)
