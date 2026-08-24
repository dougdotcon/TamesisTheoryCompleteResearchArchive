"""
R_MC2 (pre-registered): raw discrete finite-n permutation simulation of
the FULL K=3 model, reusing NONE of the continuum/shape machinery except
the ground-truth orbit tracer already validated in mechanism_check_k3.py
(true_cyclic_count) -- i.e. this script does not use region_and_distance,
predicted_cyclic_count, or any shape/group formula at all. It builds a
genuine uniform random permutation of [n], 3 rerouted labels, i.i.d.
uniform destinations, finds the TRUE cyclic set by direct orbit tracing,
and compares the empirical density of M_3/n against the target
6x(1-x^2)^2 via a Kolmogorov-Smirnov test -- exactly generalizing
conjecture1_k2_attempt/ATTEMPT.md's R4 to K=3.
"""
import numpy as np
from scipy import stats
import json
import time

from mechanism_check_k3 import true_cyclic_count


def target_cdf(x):
    # F(x) = integral_0^x 6t(1-t^2)^2 dt = 1 - (1-x^2)^3
    return 1 - (1 - x ** 2) ** 3


def run(n, trials, seed):
    rng = np.random.default_rng(seed)
    vals = np.empty(trials, dtype=np.float64)
    t0 = time.time()
    for trial in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=3, replace=False)
        u = rng.integers(0, n, size=3)
        f = pi.copy()
        for i in range(3):
            f[sources[i]] = u[i]
        c = true_cyclic_count(f, n)
        vals[trial] = c / n
    elapsed = time.time() - t0
    ks = stats.kstest(vals, target_cdf)
    mean = vals.mean()
    se = vals.std(ddof=1) / np.sqrt(trials)
    target_mean = 16.0 / 35.0  # from derive_step2_k3_symbolic.py: integral x*f_M3(x)dx = 16/35
    z = (mean - target_mean) / se
    print(f"n={n} trials={trials}: KS D={ks.statistic:.5f} p={ks.pvalue:.4f}  "
          f"mean(M3/n)={mean:.6f} +/- {se:.6f} vs 16/35={target_mean:.6f} (z={z:+.2f})  "
          f"elapsed={elapsed:.1f}s")
    return {
        'n': n, 'trials': trials, 'ks_D': float(ks.statistic), 'ks_p': float(ks.pvalue),
        'mean': float(mean), 'se': float(se), 'target_mean': target_mean, 'z': float(z),
    }


if __name__ == "__main__":
    print("=" * 78)
    print("R_MC2 -- raw discrete finite-n simulation of the full K=3 model")
    print("Target: f_M3(x) = 6x(1-x^2)^2, CDF F(x) = 1-(1-x^2)^3")
    print("=" * 78)
    results = []
    print("\n--- n=10000, trials=4000, seed 20260843010 ---")
    results.append(run(10000, 4000, 20260843010))
    print("\n--- n=20000, trials=2000, seed 20260843011 (independent, larger n) ---")
    results.append(run(20000, 2000, 20260843011))

    with open("discrete_k3_full_distribution_mc_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
