"""
R_MC1 (pre-registered): independent discrete-permutation check of Lemma 1
at K=4 -- does NOT touch continuum PD(1)/stick-breaking machinery at all.
Generalizes mc_lemma1_k3_check.py to four sources.

Draw a uniform random permutation pi of [n]; pick 4 distinct labels
x1,x2,x3,x4; compute (m1,m2,m3,m4) = region sizes via the SAME
region_and_distance routine validated (0 mismatches, 105,000 trials) in
mechanism_check_k4.py's own ground-truth cross-check. Compare
(m1/n,...,m4/n) moments and the marginal/sum distributions against the
exact Dirichlet(1,1,1,1,1) targets implied by Lemma 1 (uniform density 24
on the 4-simplex): each m_i ~ Beta(1,4) (marginal density 4(1-x)^3),
L=m1+m2+m3+m4 has density 4*ell^3 on (0,1), E[m_i]=1/5, E[m_i^2]=1/15,
E[m_i*m_j]=1/30 (i!=j), Cov(m_i,m_j)=-1/150.
"""
import numpy as np
from scipy import stats
import json

from mechanism_check_k4 import region_and_distance

K = 4


def L_cdf(x):
    return x ** K  # integral 0^x K*t^(K-1) dt


def marginal_cdf(x):
    return 1 - (1 - x) ** K  # Beta(1,K) CDF


def run(n, trials, seed):
    rng = np.random.default_rng(seed)
    ms = [np.empty(trials) for _ in range(K)]
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=K, replace=False)
        region, dist = region_and_distance(pi, list(sources), n)
        for i in range(K):
            ms[i][t] = (region == i).sum() / n

    L = sum(ms)
    all_m = np.concatenate(ms)

    print(f"n={n} trials={trials}")
    target_mean = 1 / (K + 1)
    print(f"  E[m_i] target = 1/{K+1} = {target_mean:.5f}")
    for i in range(K):
        z = (ms[i].mean() - target_mean) / (ms[i].std(ddof=1) / np.sqrt(trials))
        print(f"    E[m{i+1}]={ms[i].mean():.5f} z={z:+.2f}")
    target_sq = 2 / ((K + 1) * (K + 2))
    target_cross = 1 / ((K + 1) * (K + 2))
    target_cov = -1 / ((K + 1) ** 2 * (K + 2))
    print(f"  E[m1^2]={np.mean(ms[0]**2):.5f} (target {target_sq:.5f})")
    print(f"  E[m1*m2]={np.mean(ms[0]*ms[1]):.5f} (target {target_cross:.5f})")
    cov12 = np.cov(ms[0], ms[1])[0, 1]
    print(f"  Cov(m1,m2)={cov12:.5f} (target {target_cov:.5f})")
    ks_L = stats.kstest(L, L_cdf)
    print(f"  KS(L=sum m_i vs {K}*ell^{K-1} CDF ell^{K}): D={ks_L.statistic:.5f} p={ks_L.pvalue:.4f}")
    ks_m = stats.kstest(all_m, marginal_cdf)
    print(f"  KS(pooled m_i vs Beta(1,{K})): D={ks_m.statistic:.5f} p={ks_m.pvalue:.4f}")
    ks_exch = stats.ks_2samp(ms[0], ms[1])
    print(f"  Exchangeability KS(m1 vs m2): D={ks_exch.statistic:.5f} p={ks_exch.pvalue:.4f}")
    ks_exch2 = stats.ks_2samp(ms[0], ms[3])
    print(f"  Exchangeability KS(m1 vs m4): D={ks_exch2.statistic:.5f} p={ks_exch2.pvalue:.4f}")
    return {
        'n': n, 'trials': trials,
        'E_m': [float(m.mean()) for m in ms],
        'E_m1sq': float(np.mean(ms[0] ** 2)), 'E_m1m2': float(np.mean(ms[0] * ms[1])),
        'cov_m1m2': float(cov12),
        'ks_L_D': float(ks_L.statistic), 'ks_L_p': float(ks_L.pvalue),
        'ks_marg_D': float(ks_m.statistic), 'ks_marg_p': float(ks_m.pvalue),
        'ks_exch12_p': float(ks_exch.pvalue), 'ks_exch14_p': float(ks_exch2.pvalue),
    }


if __name__ == "__main__":
    print("=" * 78)
    print("R_MC1 -- Lemma 1 at K=4, independent discrete-permutation check")
    print("=" * 78)
    results = []
    for n, trials, seed in [(300, 15000, 20260850020), (1000, 10000, 20260850021), (5000, 6000, 20260850022)]:
        print()
        results.append(run(n, trials, seed))
    with open("mc_lemma1_k4_check_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
