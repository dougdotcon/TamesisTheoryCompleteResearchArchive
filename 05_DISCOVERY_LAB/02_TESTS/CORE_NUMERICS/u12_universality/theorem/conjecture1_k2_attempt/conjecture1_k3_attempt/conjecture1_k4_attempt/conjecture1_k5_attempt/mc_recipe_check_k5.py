#!/usr/bin/env python3
"""Continuum Monte Carlo of the derived K=5 recipe, with per-group KS.

Fresh code; no prior front/referee script read or imported.  Independent
re-implementation of the mechanism (vectorized), NOT reusing the symbolic
integration: draw (m_1..m_5) ~ Dirichlet(1,...,1) (Lemma 1), u_1..u_5 ~
Unif(0,1); classify each u into regions by cumulative boundaries; find the
cycles of g by vectorized iteration; M = 1 - sum_off m - sum_on P.

Checks: overall KS vs F(x)=1-(1-x^2)^5; mean vs 256/693; per-r_on group
fractions vs the registered exact probabilities (1/6, 5/14, 25/84, 5/36,
1/28, 1/252); per-group KS vs the registered conditional densities
f_r(x)/P(r) (exact CDFs via Fraction integration of the polynomials).

Seed (front range): 20260860030, N = 2,000,000.
"""
import json
from fractions import Fraction
from math import comb
import numpy as np
from scipy import stats

K = 5
N = 2_000_000
SEED = 20260860030
rng = np.random.default_rng(np.random.SeedSequence(SEED))

m = rng.dirichlet(np.ones(K + 1), size=N)[:, :K]   # 5 region masses
u = rng.random((N, K))
# classify: boundaries c_0=0 < c_1 < ... < c_5 = sum m; u in region j if
# c_j <= u < c_{j+1}; else OUT.  Position P = u - c_j.
cum = np.cumsum(m, axis=1)                          # c_1..c_5
lo = np.concatenate([np.zeros((N, 1)), cum[:, :-1]], axis=1)
g = np.full((N, K), K, dtype=np.int8)               # default OUT
P = np.zeros((N, K))
for j in range(K):
    for i in range(K):
        hit = (u[:, i] >= lo[:, j]) & (u[:, i] < cum[:, j])
        g[hit, i] = j
        P[hit, i] = u[hit, i] - lo[hit, j]

# vectorized cycle detection on the 5-node functional graph (OUT absorbing)
gg = np.concatenate([g, np.full((N, 1), K, dtype=np.int8)], axis=1)  # node K -> K
on_cycle = np.zeros((N, K), dtype=bool)
it = np.tile(np.arange(K, dtype=np.int8), (N, 1))
cur = it.copy()
for t in range(K):
    cur = np.take_along_axis(gg, cur.astype(np.intp), axis=1)
    on_cycle |= (cur == it)

Q = np.where(~on_cycle, m, 0.0).sum(axis=1)
S = np.where(on_cycle, P, 0.0).sum(axis=1)
M = 1.0 - Q - S
r_on = on_cycle.sum(axis=1)

out = {"seed": SEED, "N": N}
ok_all = True

# overall KS + mean
ks = stats.kstest(M, lambda x: 1 - (1 - np.clip(x, 0, 1) ** 2) ** 5)
mean = M.mean()
se = M.std(ddof=1) / np.sqrt(N)
z = (mean - 256 / 693) / se
print(f"overall: KS D={ks.statistic:.5f} p={ks.pvalue:.4f}  "
      f"mean={mean:.6f}+/-{se:.6f} vs 256/693 (z={z:+.2f})")
out["overall"] = {"ks_D": float(ks.statistic), "ks_p": float(ks.pvalue),
                  "mean": float(mean), "z": float(z)}
ok_all &= ks.pvalue > 0.01 and abs(z) < 3

# group fractions
probs = [Fraction(1, 6), Fraction(5, 14), Fraction(25, 84),
         Fraction(5, 36), Fraction(1, 28), Fraction(1, 252)]
out["groups"] = {}
for r in range(K + 1):
    nr = int((r_on == r).sum())
    p = float(probs[r])
    zf = (nr - N * p) / np.sqrt(N * p * (1 - p))
    print(f"r_on={r}: count={nr} frac={nr/N:.6f} target={p:.6f} (z={zf:+.2f})")
    out["groups"][str(r)] = {"count": nr, "z_frac": float(zf)}
    ok_all &= abs(zf) < 3.5

# per-group KS against conditional densities f_r/P(r);
# f_r(x) = C(5,r)[5 x^r (1-x)^4 - (5-r) x^r (1-x)^5]; build exact
# coefficient lists with Fraction, integrate to CDF, evaluate with numpy.
def poly_coeffs_fr(r):
    # (1-x)^4 and (1-x)^5 expansions
    c4 = [Fraction(comb(4, j) * (-1) ** j) for j in range(5)]
    c5 = [Fraction(comb(5, j) * (-1) ** j) for j in range(6)]
    coeffs = {}
    for j, cj in enumerate(c4):
        coeffs[r + j] = coeffs.get(r + j, Fraction(0)) + 5 * comb(5, r) * cj
    for j, cj in enumerate(c5):
        coeffs[r + j] = coeffs.get(r + j, Fraction(0)) - (5 - r) * comb(5, r) * cj
    return coeffs


for r in range(K + 1):
    sel = M[r_on == r]
    coeffs = poly_coeffs_fr(r)
    Pr = probs[r]
    # CDF of conditional density: (1/Pr) * sum c_d x^(d+1)/(d+1)
    cdf_c = {d + 1: c / (d + 1) / Pr for d, c in coeffs.items()}
    degs = sorted(cdf_c)
    cs = np.array([float(cdf_c[d]) for d in degs])
    ds = np.array(degs, dtype=float)

    def cdf(x, cs=cs, ds=ds):
        xx = np.clip(np.asarray(x, dtype=float), 0, 1)[:, None]
        return (cs[None, :] * xx ** ds[None, :]).sum(axis=1)

    ksr = stats.kstest(sel, cdf)
    print(f"r_on={r}: n={len(sel)}  KS vs conditional f_{r}: "
          f"D={ksr.statistic:.5f} p={ksr.pvalue:.4f}")
    out["groups"][str(r)]["ks_p"] = float(ksr.pvalue)
    ok_all &= ksr.pvalue > 0.01

with open("mc_recipe_check_k5.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("ALL CHECKS PASSED" if ok_all else "SOME CHECKS FAILED")
