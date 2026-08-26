"""
Independent hostile referee check -- Lemma 1 (general K) discrete-permutation
MC at K=5: does NOT touch continuum PD(1)/stick-breaking machinery at all.
Builds a genuine uniform random permutation of [n], marks K=5 distinct labels
as sources, and defines m_i (rescaled by n) as the discrete "arc" of points
whose forward flow reaches source i before any other source (0 for points in
source-free cycles). Checks the resulting (m_1,...,m_5)/n against the claimed
continuum law: uniform density 5! on the simplex {m_i>0, sum m_i<1} -- via
per-mass and pairwise moments, marginal L=sum(m_i) vs Beta(5,1) (density
5*l^4), pooled single-mass marginal vs Beta(1,4), and exchangeability.

INDEPENDENCE: fresh code, own region-assignment routine (re-derived here, not
reusing ref2_mechanism_mc.py's region_assign on purpose -- written
independently a second time as an extra cross-check that the two
implementations agree).

Seeds: SeedSequence(20260861110/111/112) -- referee range, 3 scales.
"""
import numpy as np
from scipy import stats
import sys
from time import time

K = 5

def region_sizes(perm, sources):
    """Independent (re-derived) region-size routine: returns array of K region
    sizes (# points whose forward background flow reaches that source first)."""
    n = len(perm)
    visited = np.zeros(n, dtype=bool)
    sizes = np.zeros(K, dtype=np.int64)
    source_set = {s: i for i, s in enumerate(sources)}
    for start in range(n):
        if visited[start]:
            continue
        cyc = []
        cur = start
        while not visited[cur]:
            visited[cur] = True
            cyc.append(cur)
            cur = perm[cur]
        src_positions = sorted((pos, source_set[node]) for pos, node in enumerate(cyc) if node in source_set)
        if not src_positions:
            continue  # OUT, contributes to no region
        L = len(cyc)
        m = len(src_positions)
        for k in range(m):
            pos_k, idx_k = src_positions[k]
            pos_prev = src_positions[k - 1][0]
            span_start = (pos_prev + 1) % L
            count = (pos_k - span_start) % L + 1
            sizes[idx_k] += count
    return sizes

def run_scale(n, n_trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    M = np.zeros((n_trials, K))
    for t in range(n_trials):
        perm = rng.permutation(n)
        sources = rng.choice(n, size=K, replace=False)
        M[t] = region_sizes(perm, sources) / n
    return M

if __name__ == "__main__":
    t0 = time()
    scales = [(300, 15000, 20260861110), (1200, 8000, 20260861111), (5000, 4000, 20260861112)]
    for n, trials, seed in scales:
        M = run_scale(n, trials, seed)
        print(f"\n=== n={n}, trials={trials}, seed={seed} ===")
        m1 = M[:, 0]
        Em1 = m1.mean()
        target_Em1 = 1 / (K + 1)
        z_Em1 = (Em1 - target_Em1) / (np.sqrt(np.var(m1, ddof=1) / trials))
        Em1sq = (m1 ** 2).mean()
        target_Em1sq = 2 / ((K + 1) * (K + 2))  # Beta(1,K) second moment
        z_Em1sq = (Em1sq - target_Em1sq) / (np.sqrt(np.var(m1 ** 2, ddof=1) / trials))
        cov12 = np.cov(M[:, 0], M[:, 1], ddof=1)[0, 1]
        target_cov = -1 / ((K + 1) ** 2 * (K + 2))  # Dirichlet(1,...,1;K+1 total incl. residual) cov
        print(f"  E[m1]={Em1:.5f} (target {target_Em1:.5f}, z={z_Em1:+.2f})")
        print(f"  E[m1^2]={Em1sq:.5f} (target {target_Em1sq:.5f}, z={z_Em1sq:+.2f})")
        print(f"  Cov(m1,m2)={cov12:.6f} (target {target_cov:.6f})")

        L = M.sum(axis=1)
        # L = sum of K masses ~ Beta(K,1) marginal (density K*l^(K-1)) under
        # Lemma 1 (K! density on simplex => marginal of the SUM is K*l^(K-1))
        ks_L = stats.kstest(L, lambda x: x ** K)
        print(f"  KS(L vs l^{K}): D={ks_L.statistic:.5f} p={ks_L.pvalue:.4f}")

        pooled = M.flatten()
        ks_pooled = stats.kstest(pooled, lambda x: 1 - (1 - x) ** K)  # Beta(1,K-1)... actually marginal m_i ~ Beta(1,K)
        print(f"  KS(pooled m_i vs Beta(1,{K})): D={ks_pooled.statistic:.5f} p={ks_pooled.pvalue:.4f}")

        ks_ex1 = stats.ks_2samp(M[:, 0], M[:, 1])
        ks_ex2 = stats.ks_2samp(M[:, 0], M[:, 4])
        print(f"  exchangeability KS(m1,m2): p={ks_ex1.pvalue:.4f}   KS(m1,m5): p={ks_ex2.pvalue:.4f}")

    print(f"\nwall time: {time()-t0:.1f}s")
    print("\nNote: this script reports statistics for the record (matching the "
          "lineage's own discretization-bias-then-convergence signature); pass/"
          "fail judgment is made in REFEREE_REPORT.md, exactly as the target "
          "document and its own prior referees do for the analogous check.")
