"""R3: Monte Carlo check of Step A's claim that (m1,m2) is uniform
(density 2) on the triangle T={m1,m2>0,m1+m2<1}, via a from-scratch
simulation of the two-case recipe (own draws, not reusing the sympy
change-of-variables computation in derive_density_symbolic.py).

Seed: numpy.random.SeedSequence(20260835000) (this front's reserved
block, confirmed unused elsewhere in the archive before this front).
"""
import json
import numpy as np
from scipy.stats import kstest

SEED0 = 20260835000
root = np.random.SeedSequence(SEED0)
rng = np.random.default_rng(root)

N = 2_000_000

# CORRECT generative order (matches Fact C's actual construction): draw
# L1 = L (the block containing x1) UNCONDITIONALLY first, L~Unif(0,1)
# (Fact A). THEN decide Same via Bernoulli(L) -- x2 lands in B_1 (same
# block) with probability exactly Leb(B_1)=L, given the partition and x1.
# (An earlier version of this script incorrectly flipped a fair 1/2 coin
# for Same *before* drawing L as if independent of it -- that silently
# assumes L|Same=1 ~ Unif(0,1) again, which is FALSE: conditioning on
# Same=1 size-biases L upward (density 2*ell, not uniform) since larger
# blocks are more likely to capture x2 too. Caught by exactly this
# script's own moment/KS checks failing badly on the first run -- see
# r3_step_a_mc_BUGGY_FIRST_ATTEMPT.log kept alongside for the record.)
L = rng.random(N)
same = rng.random(N) < L  # P(Same=1 | L=ell) = ell

m1 = np.empty(N)
m2 = np.empty(N)

# Case I (same background block, given L): A|L~Unif(0,L), m1=L-A, m2=A
idxI = np.where(same)[0]
Lv = L[idxI]
A = rng.random(idxI.size) * Lv
m1[idxI] = Lv - A
m2[idxI] = A

# Case II (different blocks, given L1=L): W~Unif(0,1) indep, L2=(1-L1)*W
idxII = np.where(~same)[0]
L1v = L[idxII]
W = rng.random(idxII.size)
L2 = (1 - L1v) * W
m1[idxII] = L1v
m2[idxII] = L2

print(f"N={N}")
print("--- exact targets for Unif(density=2) on T={m1,m2>0,m1+m2<1} ---")
# E[m1]=E[m2]=1/3 ; E[m1^2]=E[m2^2]=1/6 ; E[m1*m2]=1/12 ; Var(m1)=1/6-1/9=1/18
target_mean = 1.0 / 3
target_m1m1 = 1.0 / 6
target_m1m2 = 1.0 / 12
print(f"target E[m1]=E[m2]={target_mean:.6f}, E[m1^2]=E[m2^2]={target_m1m1:.6f}, "
      f"E[m1*m2]={target_m1m2:.6f}")

mean_m1, mean_m2 = m1.mean(), m2.mean()
sem_m1, sem_m2 = m1.std(ddof=1) / np.sqrt(N), m2.std(ddof=1) / np.sqrt(N)
print(f"MC E[m1]={mean_m1:.6f} (z={ (mean_m1-target_mean)/sem_m1:+.2f} ), "
      f"E[m2]={mean_m2:.6f} (z={ (mean_m2-target_mean)/sem_m2:+.2f} )")

m1m2 = m1 * m2
mean_m1m2 = m1m2.mean()
sem_m1m2 = m1m2.std(ddof=1) / np.sqrt(N)
print(f"MC E[m1*m2]={mean_m1m2:.6f} (z={(mean_m1m2-target_m1m2)/sem_m1m2:+.2f})")

m1sq = m1 * m1
mean_m1sq = m1sq.mean()
sem_m1sq = m1sq.std(ddof=1) / np.sqrt(N)
print(f"MC E[m1^2]={mean_m1sq:.6f} (z={(mean_m1sq-target_m1m1)/sem_m1sq:+.2f})")

# exchangeability check: KS test comparing empirical dist of m1 vs m2
# (two-sample KS -- should NOT reject; they must be identically distributed)
ks_exch = kstest(m1, m2)
print(f"Exchangeability check (2-sample KS, m1 vs m2): "
      f"D={ks_exch.statistic:.5f} p={ks_exch.pvalue:.4f}")

# marginal of L=m1+m2 has exact target density 2*ell, i.e. CDF ell^2
Lsum = m1 + m2
ks_L = kstest(Lsum, lambda t: t ** 2)
print(f"Marginal L=m1+m2 KS vs CDF ell^2: D={ks_L.statistic:.5f} p={ks_L.pvalue:.4f}")

out = dict(
    N=N, seed=SEED0,
    mean_m1=float(mean_m1), mean_m2=float(mean_m2), target_mean=target_mean,
    z_m1=float((mean_m1 - target_mean) / sem_m1),
    z_m2=float((mean_m2 - target_mean) / sem_m2),
    mean_m1m2=float(mean_m1m2), target_m1m2=target_m1m2,
    z_m1m2=float((mean_m1m2 - target_m1m2) / sem_m1m2),
    mean_m1sq=float(mean_m1sq), target_m1sq=target_m1m1,
    z_m1sq=float((mean_m1sq - target_m1m1) / sem_m1sq),
    exch_ks_D=float(ks_exch.statistic), exch_ks_p=float(ks_exch.pvalue),
    Lsum_ks_D=float(ks_L.statistic), Lsum_ks_p=float(ks_L.pvalue),
)
with open(__file__.replace('.py', '.json'), 'w') as fh:
    json.dump(out, fh, indent=2)
print("saved", __file__.replace('.py', '.json'))
