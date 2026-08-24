"""
R_MC1 (pre-registered): independent discrete-permutation check of Lemma 1
at K=3 -- does NOT touch continuum PD(1)/stick-breaking machinery at all.
Generalizes conjecture1_k2_attempt/adversarial/adv_lemma1_discrete_check.py
(the K=2 referee's own independent check) to three sources.

Draw a uniform random permutation pi of [n]; pick 3 distinct labels
x1,x2,x3; compute (m1,m2,m3) = region sizes via the SAME region_and_distance
routine validated (0 mismatches, 52,000 trials) in mechanism_check_k3.py's
own ground-truth cross-check. Compare (m1/n,m2/n,m3/n) moments and the
marginal/sum distributions against the exact Dirichlet(1,1,1,1) targets
implied by Lemma 1 (uniform density 6 on the simplex): each m_i ~ Beta(1,3)
(marginal density 3(1-x)^2), L=m1+m2+m3 has density 3*ell^2 on (0,1),
E[m_i]=1/4, E[m_i^2]=1/10, E[m_i*m_j]=1/20 (i!=j), Cov(m_i,m_j)=-1/80.
"""
import numpy as np
from scipy import stats
import json

from mechanism_check_k3 import region_and_distance


def L_cdf(x):
    return x ** 3  # integral 0^x 3t^2 dt


def marginal_cdf(x):
    return 1 - (1 - x) ** 3  # Beta(1,3) CDF


def run(n, trials, seed):
    rng = np.random.default_rng(seed)
    m1s = np.empty(trials)
    m2s = np.empty(trials)
    m3s = np.empty(trials)
    for t in range(trials):
        pi = rng.permutation(n)
        sources = rng.choice(n, size=3, replace=False)
        region, dist = region_and_distance(pi, list(sources), n)
        m1s[t] = (region == 0).sum() / n
        m2s[t] = (region == 1).sum() / n
        m3s[t] = (region == 2).sum() / n

    Ls = m1s + m2s + m3s
    all_m = np.concatenate([m1s, m2s, m3s])

    print(f"n={n} trials={trials}")
    print(f"  E[m1]={m1s.mean():.5f} E[m2]={m2s.mean():.5f} E[m3]={m3s.mean():.5f}  (target 1/4=0.25)")
    for name, arr in [('m1', m1s), ('m2', m2s), ('m3', m3s)]:
        z = (arr.mean() - 0.25) / (arr.std(ddof=1) / np.sqrt(trials))
        print(f"    z[{name}]={z:+.2f}")
    print(f"  E[m1^2]={np.mean(m1s**2):.5f} (target 1/10=0.1)")
    print(f"  E[m1*m2]={np.mean(m1s*m2s):.5f} (target 1/20=0.05)")
    print(f"  Cov(m1,m2)={np.cov(m1s,m2s)[0,1]:.5f} (target -1/80={-1/80:.5f})")
    ks_L = stats.kstest(Ls, L_cdf)
    print(f"  KS(L=m1+m2+m3 vs 3ell^2 CDF ell^3): D={ks_L.statistic:.5f} p={ks_L.pvalue:.4f}")
    ks_m = stats.kstest(all_m, marginal_cdf)
    print(f"  KS(pooled m_i vs Beta(1,3)): D={ks_m.statistic:.5f} p={ks_m.pvalue:.4f}")
    ks_exch = stats.ks_2samp(m1s, m2s)
    print(f"  Exchangeability KS(m1 vs m2): D={ks_exch.statistic:.5f} p={ks_exch.pvalue:.4f}")
    return {
        'n': n, 'trials': trials,
        'E_m1': float(m1s.mean()), 'E_m2': float(m2s.mean()), 'E_m3': float(m3s.mean()),
        'E_m1sq': float(np.mean(m1s**2)), 'E_m1m2': float(np.mean(m1s*m2s)),
        'cov_m1m2': float(np.cov(m1s, m2s)[0, 1]),
        'ks_L_D': float(ks_L.statistic), 'ks_L_p': float(ks_L.pvalue),
        'ks_marg_D': float(ks_m.statistic), 'ks_marg_p': float(ks_m.pvalue),
    }


if __name__ == "__main__":
    print("=" * 78)
    print("R_MC1 -- Lemma 1 at K=3, independent discrete-permutation check")
    print("=" * 78)
    results = []
    for n, trials, seed in [(300, 15000, 20260843020), (1000, 10000, 20260843021), (5000, 6000, 20260843022)]:
        print()
        results.append(run(n, trials, seed))
    with open("mc_lemma1_k3_check_results.json", "w") as fh:
        json.dump(results, fh, indent=2)
