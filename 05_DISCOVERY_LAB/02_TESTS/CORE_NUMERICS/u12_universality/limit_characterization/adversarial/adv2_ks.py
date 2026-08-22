"""Surface (d) extension: distribution-level test of the conditional law.

Hansen-Jaworski Thm 7(ii) (a = K fixed) predicts the limiting DENSITY of
the cyclic fraction x given K corruptions: f_K(x) = 2K x (1-x^2)^{K-1},
i.e. CDF F_K(x) = 1-(1-x^2)^K. KS test of my continuum realizations
(fixed K) against F_K. Seed 90210999.
"""
import numpy as np, json, math, sys
from scipy import stats
from adv2_continuum import one_realization

ROOT = sys.path[0]

if __name__ == "__main__":
    rng = np.random.default_rng(90210999)
    out = {}
    N = 200000
    for K in [1, 2, 3]:
        vals = np.array([one_realization(0.0, rng, K=K) for _ in range(N)])
        cdf = lambda x, K=K: 1.0 - (1.0 - x**2)**K
        res = stats.kstest(vals, cdf)
        out[str(K)] = {"N": N, "mean": float(vals.mean()),
                       "KS_stat": float(res.statistic), "KS_p": float(res.pvalue)}
        print(f"K={K}: mean {vals.mean():.6f}, KS D={res.statistic:.5f}, p={res.pvalue:.4f}", flush=True)
    with open(ROOT + "/adv2_ks.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("saved adv2_ks.json")
