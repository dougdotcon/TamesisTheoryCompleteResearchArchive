"""R5: Monte Carlo of the exact derived recipe (Step A: (m1,m2) via the
CORRECT generative order; Step B: 4-group draw; Step C: M2 given group),
KS-tested against 4x(1-x^2). This checks the recipe's *internal*
consistency with the (already exact, symbolically proved) target density
-- confirmatory, not independent of Step A/B's correctness (R4 is the
independent check for that).
"""
import json
import numpy as np
from scipy.stats import kstest

SEED0 = 20260835000
root = np.random.SeedSequence(SEED0)
child = root.spawn(2)[1]  # distinct child from R4's spawn(1)[0]
rng = np.random.default_rng(child)

N = 2_000_000

L = rng.random(N)
same = rng.random(N) < L
m1 = np.empty(N)
m2 = np.empty(N)
idxI = np.where(same)[0]
Lv = L[idxI]
A = rng.random(idxI.size) * Lv
m1[idxI] = Lv - A
m2[idxI] = A
idxII = np.where(~same)[0]
L1v = L[idxII]
W = rng.random(idxII.size)
m1[idxII] = L1v
m2[idxII] = (1 - L1v) * W

# group draw: A prob 2 m1 m2, B prob m1(1-m2), C prob m2(1-m1), D prob rest
pA = 2 * m1 * m2
pB = m1 * (1 - m2)
pC = m2 * (1 - m1)
pD = 1 - m1 - m2
# sanity: these must sum to 1
tot = pA + pB + pC + pD
assert np.allclose(tot, 1.0), tot.min()

u = rng.random(N)
cA = pA
cB = cA + pB
cC = cB + pC
# cD = 1

M2 = np.empty(N)

maskA = u < cA
maskB = (~maskA) & (u < cB)
maskC = (~maskA) & (~maskB) & (u < cC)
maskD = (~maskA) & (~maskB) & (~maskC)

nA, nB, nC, nD = maskA.sum(), maskB.sum(), maskC.sum(), maskD.sum()
print(f"group counts: A={nA} B={nB} C={nC} D={nD} (N={N})")

D1a = rng.random(nA) * m1[maskA]
D2a = rng.random(nA) * m2[maskA]
M2[maskA] = 1 - D1a - D2a

D1b = rng.random(nB) * m1[maskB]
M2[maskB] = 1 - m2[maskB] - D1b

D2c = rng.random(nC) * m2[maskC]
M2[maskC] = 1 - m1[maskC] - D2c

M2[maskD] = 1 - m1[maskD] - m2[maskD]

assert np.all(M2 > -1e-9) and np.all(M2 < 1 + 1e-9), (M2.min(), M2.max())

cdf_target = lambda t: 2 * t ** 2 - t ** 4
st = kstest(M2, cdf_target)
mean_mc = float(M2.mean())
sem_mc = float(M2.std(ddof=1) / np.sqrt(N))
target_mean = 8.0 / 15
print(f"KS D={st.statistic:.5f} p={st.pvalue:.4f} (N={N})")
print(f"mean={mean_mc:.6f} +/- {sem_mc:.6f} vs 8/15={target_mean:.6f} "
      f"z={(mean_mc - target_mean) / sem_mc:+.2f}")

out = dict(N=N, KS_D=float(st.statistic), KS_p=float(st.pvalue),
           mean_mc=mean_mc, sem_mc=sem_mc, target_mean=target_mean,
           z_mean=float((mean_mc - target_mean) / sem_mc))
with open(__file__.replace('.py', '.json'), 'w') as fh:
    json.dump(out, fh, indent=2)
print("saved", __file__.replace('.py', '.json'))
