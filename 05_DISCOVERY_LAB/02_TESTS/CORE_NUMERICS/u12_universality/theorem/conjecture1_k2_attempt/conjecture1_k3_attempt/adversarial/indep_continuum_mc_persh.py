"""
INDEPENDENT continuum Monte Carlo, PER-SHAPE, of the K=3 recipe.
Fresh implementation (not reading mc_recipe_check_k3.py or any other
front script). Draws (m1,m2,m3,m0) ~ Dirichlet(1,1,1,1) [= uniform density
6 on the simplex, per Lemma 1], u1,u2,u3 ~ Uniform(0,1) iid, classifies via
an independent cycle-detection routine, computes M3 = (1-m1-m2-m3) +
sum_{on-cycle i} (m_{target(i)} - P_i), bins samples by shape, and checks:
  (a) empirical P(shape) vs ATTEMPT.md's claimed target probabilities
  (b) empirical CDF of M3 | shape vs ATTEMPT.md's closed-form densities
      (via KS test against the exact symbolic CDF, computed here
      independently by integrating the document's REPORTED formulas --
      this checks whether those reported formulas are actually correct,
      which is the point: we are not assuming they're right).
Also computes the aggregate density vs 6x(1-x^2)^2 as a top-level check.

Seeds: numpy SeedSequence, referee-reserved range 20260844000+, per
DISC-DEC-063 (confirmed unused before this run, see main session log).
"""
import numpy as np
import sympy as sp
from scipy import stats

rng = np.random.default_rng(np.random.SeedSequence(20260844001))

N = 8_000_000

# Draw (m1,m2,m3) ~ uniform density 6 on simplex via Dirichlet(1,1,1,1)
g = rng.standard_gamma(1.0, size=(N, 4))
g /= g.sum(axis=1, keepdims=True)
m1, m2, m3, m0 = g[:, 0], g[:, 1], g[:, 2], g[:, 3]

u1 = rng.random(N)
u2 = rng.random(N)
u3 = rng.random(N)

# region boundaries in fixed order: [0,m1) region1, [m1,m1+m2) region2,
# [m1+m2, m1+m2+m3) region3, [m1+m2+m3, 1) OUT
b1 = m1
b2 = m1 + m2
b3 = m1 + m2 + m3

def region_and_offset(u):
    r = np.full(N, 4, dtype=np.int8)  # 4 = OUT
    P = np.zeros(N)
    in1 = u < b1
    in2 = (~in1) & (u < b2)
    in3 = (~in1) & (~in2) & (u < b3)
    inO = (~in1) & (~in2) & (~in3)
    r[in1] = 1; P[in1] = u[in1]
    r[in2] = 2; P[in2] = u[in2] - b1[in2]
    r[in3] = 3; P[in3] = u[in3] - b2[in3]
    r[inO] = 4; P[inO] = u[inO] - b3[inO]  # unused for OUT
    return r, P

g1, P1 = region_and_offset(u1)
g2, P2 = region_and_offset(u2)
g3, P3 = region_and_offset(u3)
gg = np.stack([g1, g2, g3], axis=1)  # shape (N,3), values 1,2,3,4(=OUT)
PP = np.stack([P1, P2, P3], axis=1)
mm = np.stack([m1, m2, m3], axis=1)

# ---- independent cycle classification, vectorized per-sample ----
# For each sample, node i (0,1,2 for sources 1,2,3) has target gg[:,i]
# (1,2,3, or 4=OUT). Determine on-cycle set via forward walk (<=3 steps).
def target_of(node_idx, gg):
    # node_idx: which source (0,1,2); returns target array (1..4)
    return gg[:, node_idx]

# forward walk from each start node (0,1,2), track visited, detect return
on_cycle = np.zeros((N, 3), dtype=bool)
for start in range(3):
    cur = np.full(N, start, dtype=np.int8)  # current node index 0..2, or -1 if hit OUT
    alive = np.ones(N, dtype=bool)
    path = [cur.copy()]
    for step in range(3):
        tgt = np.full(N, -1, dtype=np.int8)
        valid = alive
        tval = gg[np.arange(N), np.where(valid, cur, 0)]
        newcur = np.where(tval == 4, -1, tval - 1).astype(np.int8)  # -1 = OUT
        # check if newcur == start -> on cycle
        closes = valid & (newcur == start)
        on_cycle[closes, start] = True
        alive = valid & (newcur != -1) & (~closes)
        cur = np.where(alive, newcur, cur)
        if not alive.any():
            break

# shape classification per sample
# count self-loops (target(i)==i), and cycle structure among on-cycle nodes
# self-loop: gg[:,i]-1 == i  (i.e., target index equals own index)
self_loop = np.zeros((N, 3), dtype=bool)
for i in range(3):
    self_loop[:, i] = (gg[:, i] - 1 == i)

n_selfloop = self_loop.sum(axis=1)
n_oncycle = on_cycle.sum(axis=1)

# 2-cycle detection: i,j on-cycle, not self-loop, g(i)=j+1, g(j)=i+1
shape = np.full(N, '', dtype=object)
new_mass = np.zeros(N)

is_T0 = (n_oncycle == 0)
is_T3 = (n_selfloop == 3)
is_T1c = (n_oncycle == 3) & (n_selfloop == 0)
is_T1a = (n_selfloop == 1) & (n_oncycle == 1)
is_T2a = (n_selfloop == 2) & (n_oncycle == 2)
# T1b: n_oncycle==2, n_selfloop==0 (a single 2-cycle, third node off)
is_T1b = (n_oncycle == 2) & (n_selfloop == 0)
# T2b: n_oncycle==3, n_selfloop==1 (self-loop + 2-cycle)
is_T2b = (n_oncycle == 3) & (n_selfloop == 1)

assert (is_T0.sum()+is_T1a.sum()+is_T1b.sum()+is_T1c.sum()+is_T2a.sum()+is_T2b.sum()+is_T3.sum()) == N, "classification not exhaustive!"

shape[is_T0] = 'T0'
shape[is_T1a] = 'T1a'
shape[is_T1b] = 'T1b'
shape[is_T1c] = 'T1c'
shape[is_T2a] = 'T2a'
shape[is_T2b] = 'T2b'
shape[is_T3] = 'T3'

# compute new_mass = sum over on-cycle i of (m_{target(i)} - P_i)
for i in range(3):
    tgt = gg[:, i]  # 1,2,3,4
    is_region = tgt != 4
    target_m = np.where(tgt == 1, mm[:, 0], np.where(tgt == 2, mm[:, 1], mm[:, 2]))
    contrib = np.where(on_cycle[:, i], target_m - PP[:, i], 0.0)
    new_mass += contrib

M3 = (1 - m1 - m2 - m3) + new_mass

print("Sample counts per shape (N=%d):" % N)
counts = {}
for s in ['T0','T1a','T1b','T1c','T2a','T2b','T3']:
    c = (shape == s).sum()
    counts[s] = c
    print(f"  {s}: {c}  (empirical P={c/N:.6f})")

expected_p = {'T1a': 9/20, 'T1b': 1/8, 'T1c': 1/60, 'T2a': 1/8, 'T2b': 1/40, 'T3': 1/120, 'T0': 1/4}
print("\nComparing empirical P(shape) to document's claimed target probabilities (z-scores):")
for s in ['T0','T1a','T1b','T1c','T2a','T2b','T3']:
    p_hat = counts[s]/N
    p0 = expected_p[s]
    se = np.sqrt(p0*(1-p0)/N)
    z = (p_hat - p0)/se
    print(f"  {s}: p_hat={p_hat:.6f}  p0={p0:.6f}  z={z:+.2f}")

print("\nOverall M3 vs 6x(1-x^2)^2:")
D, pks = stats.kstest(M3, lambda x: 6*(x**2/2 - x**4/2 + x**6/6))
# CDF of 6x(1-x^2)^2 = 6x -12x^3+6x^5 -> integral: 3x^2 -3x^4 + x^6
cdf_full = lambda x: 3*x**2 - 3*x**4 + x**6
D, pks = stats.kstest(M3, cdf_full)
print(f"  KS D={D:.5f}  p={pks:.4f}   mean={M3.mean():.6f} (target 16/35={16/35:.6f}) z={(M3.mean()-16/35)/(M3.std()/np.sqrt(N)):+.2f}")

# Save per-shape M3 arrays for the closed-form KS check (next script)
np.savez('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/persh_samples.npz',
          **{s: M3[shape==s] for s in ['T0','T1a','T1b','T1c','T2a','T2b','T3']})
print("\nSaved per-shape M3 samples for closed-form CDF comparison.")
