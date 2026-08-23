"""
ADVERSARIAL REFEREE -- independent full-density check of f_{M2}(x)=4x(1-x^2),
at LARGER n and comparable/greater trial count than the front's own R4
(discrete_k2_full_distribution_mc.py: n=10000, trials=10000). Built entirely
from scratch (same from-scratch orbit-tracer as adv_mechanism_check.py, not
reusing any of the front's code).

n=20000 (2x front's R4), trials=12000.
"""
import numpy as np
from scipy import stats
import json, time

def find_cyclic_count(f, n):
    color = np.zeros(n, dtype=np.int8)
    cyclic_count = 0
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        pos_in_path = {}
        cur = start
        while color[cur] == 0:
            color[cur] = 1
            pos_in_path[cur] = len(path)
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:
            idx = pos_in_path[cur]
            cyclic_count += (len(path) - idx)
        for node in path:
            color[node] = 2
    return cyclic_count

def run(n, n_trials, seed):
    rng = np.random.default_rng(seed)
    m2_frac = np.empty(n_trials)
    t0 = time.time()
    for t in range(n_trials):
        pi = rng.permutation(n)
        x1, x2 = rng.choice(n, size=2, replace=False)
        u1 = int(rng.integers(0, n))
        u2 = int(rng.integers(0, n))
        f = np.array(pi, copy=True)
        f[x1] = u1
        f[x2] = u2
        M2 = find_cyclic_count(f, n)
        m2_frac[t] = M2 / n
    dt = time.time() - t0
    return m2_frac, dt

def target_cdf(x):
    return 2*x**2 - x**4

def main():
    n, n_trials, seed = 20000, 12000, 20260836021
    m2_frac, dt = run(n, n_trials, seed)
    ks = stats.kstest(m2_frac, target_cdf)
    mean = m2_frac.mean()
    se = m2_frac.std(ddof=1) / np.sqrt(n_trials)
    target_mean = 8/15
    z = (mean - target_mean) / se
    var = m2_frac.var(ddof=1)
    ex2 = (m2_frac**2).mean()
    target_ex2 = 1/3

    out = dict(n=n, n_trials=n_trials, seed=seed, time_sec=round(dt,2),
               KS_D=float(ks.statistic), KS_p=float(ks.pvalue),
               mean=float(mean), target_mean=target_mean, z_mean=float(z),
               E_x2=float(ex2), target_E_x2=target_ex2)
    print(json.dumps(out, indent=2))
    with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv_aggregate_r4_scaleup.json","w") as fh:
        json.dump(out, fh, indent=2)

if __name__ == "__main__":
    main()
