# Adversarial referee — large independent continuum Monte Carlo of the
# K=4 recipe, with per-r_on KS tests against the document's claimed
# closed-form group densities, per-group probability z-tests, and a
# sub-shape (cycle-type) sigma-exchangeability test the document itself
# never ran distributionally.
#
# Third classification implementation (vectorized numpy), sharing no
# code with indep_shapes_k4.py's enumeration classifier, my discrete
# checks, or (obviously) any of the front's scripts.
#
# Model per sample: (m1..m4, OUT) ~ Dirichlet(1,1,1,1,1) [= Lemma 1,
# independently proved]; u_1..u_4 ~ Unif(0,1) iid; classify each u_i by
# region interval; g(i) = region; on-cycle detection; and
#   M = 1 - sum_{k off-cycle} m_k - sum_{i on-cycle} P_i
# with P_i the offset of u_i within its target region.
#
# Seed: 20260851030 (referee range).  N = 8,000,000 in 8 chunks.

import numpy as np
from scipy import stats
from fractions import Fraction
import json

SEED = 20260851030
N_TOTAL = 8_000_000
CHUNK = 1_000_000

# ---- claimed per-r densities (transcribed from ATTEMPT.md Section 4) --
claimed_polys = {   # coefficient dicts: power -> coeff
    0: {4: -4, 3: 12, 2: -12, 1: 4},
    1: {5: -12, 4: 32, 3: -24, 1: 4},
    2: {6: -12, 5: 24, 3: -24, 2: 12},
    3: {7: -4, 5: 24, 4: -32, 3: 12},
    4: {7: -4, 6: 12, 5: -12, 4: 4},
}
claimed_probs = {0: Fraction(1, 5), 1: Fraction(2, 5), 2: Fraction(2, 7),
                 3: Fraction(1, 10), 4: Fraction(1, 70)}


def conditional_cdf(r):
    """Exact conditional CDF for group r as a float-coefficient
    polynomial evaluator, F_r(x) = int_0^x f_r / p_r."""
    p = claimed_probs[r]
    coeffs = {}          # power -> Fraction, of the integrated poly
    for k, c in claimed_polys[r].items():
        coeffs[k + 1] = Fraction(c, k + 1) / p
    powers = sorted(coeffs)
    fl = [(k, float(coeffs[k])) for k in powers]

    def F(x):
        x = np.asarray(x)
        out = np.zeros_like(x, dtype=float)
        for k, c in fl:
            out += c * x ** k
        return np.clip(out, 0.0, 1.0)
    return F


# sanity: conditional CDFs must hit 1 at x=1
for r in range(5):
    F = conditional_cdf(r)
    assert abs(F(np.array([1.0]))[0] - 1.0) < 1e-12, r

def total_cdf(x):
    return 1.0 - (1.0 - np.asarray(x) ** 2) ** 4


rng = np.random.default_rng(SEED)
Ms = []
rs = []
subshape = []       # encoded cycle-type id
IDX4 = np.arange(4)

def classify_chunk(nc):
    m = rng.dirichlet(np.ones(5), size=nc)      # cols 0..3 regions, 4 OUT
    u = rng.random((nc, 4))
    e = np.cumsum(m[:, :4], axis=1)             # e1..e4 edges
    g = np.zeros((nc, 4), dtype=np.int8)
    P = np.zeros((nc, 4))
    for i in range(4):
        ui = u[:, i]
        gi = (ui[:, None] >= e).sum(axis=1)     # 0..4 (4=OUT)
        g[:, i] = gi
        starts = np.where(gi == 0, 0.0,
                          e[np.arange(nc), np.clip(gi - 1, 0, 3)])
        P[:, i] = ui - starts                   # offset in target region
    # on-cycle detection: iterate up to 4 steps; OUT (4) absorbing
    on = np.zeros((nc, 4), dtype=bool)
    for i in range(4):
        cur = g[:, i].astype(np.int64)
        for _ in range(4):
            nxt = np.where(cur == 4, 4, 0)
            act = cur < 4
            nxt = np.where(act, g[np.arange(nc), np.clip(cur, 0, 3)], 4)
            cur = nxt
            on[:, i] |= (cur == i)
    r_on = on.sum(axis=1)
    M = 1.0 - (m[:, :4] * (~on)).sum(axis=1) - (P * on).sum(axis=1)
    # sub-shape: number of self-loops among on-cycle nodes; plus
    # involution test to split (2,2) from (4,) at r=4
    self_loop = (g == IDX4[None, :]) & on
    nself = self_loop.sum(axis=1)
    g2 = np.where(g < 4, np.take_along_axis(
        np.concatenate([g, np.full((nc, 1), 4, dtype=np.int8)], axis=1),
        np.clip(g, 0, 4).astype(np.int64), axis=1), 4)
    is_invol = ((g2 == IDX4[None, :]) | ~on).all(axis=1)
    # encode: code = r*10 + subcode
    sub = np.zeros(nc, dtype=np.int16)
    sub[r_on == 1] = 10
    sub[(r_on == 2) & (nself == 2)] = 20      # (1,1)
    sub[(r_on == 2) & (nself == 0)] = 21      # (2,)
    sub[(r_on == 3) & (nself == 3)] = 30      # (1,1,1)
    sub[(r_on == 3) & (nself == 1)] = 31      # (2,1)
    sub[(r_on == 3) & (nself == 0)] = 32      # (3,)
    sub[(r_on == 4) & (nself == 4)] = 40      # (1,1,1,1)
    sub[(r_on == 4) & (nself == 2)] = 41      # (2,1,1)
    sub[(r_on == 4) & (nself == 0) & is_invol] = 42     # (2,2)
    sub[(r_on == 4) & (nself == 1)] = 43      # (3,1)
    sub[(r_on == 4) & (nself == 0) & ~is_invol] = 44    # (4,)
    return M, r_on, sub


done = 0
while done < N_TOTAL:
    nc = min(CHUNK, N_TOTAL - done)
    M, r_on, sub = classify_chunk(nc)
    Ms.append(M)
    rs.append(r_on)
    subshape.append(sub)
    done += nc
M = np.concatenate(Ms)
r_on = np.concatenate(rs)
sub = np.concatenate(subshape)
N = len(M)
print(f"N = {N:,} samples,  seed = {SEED}")

RES = {"seed": SEED, "N": N}

# ---- per-group probabilities --------------------------------------
print("\nper-r_on group probabilities:")
for r in range(5):
    cnt = int((r_on == r).sum())
    p0 = float(claimed_probs[r])
    z = (cnt - N * p0) / np.sqrt(N * p0 * (1 - p0))
    print(f"  r={r}: count={cnt:8d}  frac={cnt/N:.6f}  claimed={p0:.6f}"
          f"  z={z:+.2f}")
    RES[f"prob_r{r}"] = dict(count=cnt, frac=cnt / N, claimed=p0,
                             z=float(z))
    assert abs(z) < 4.0, f"group probability r={r} rejected"

# ---- per-group KS tests vs claimed conditional densities ----------
print("\nper-r_on KS tests vs claimed conditional closed forms:")
for r in range(5):
    samp = M[r_on == r]
    F = conditional_cdf(r)
    ks = stats.kstest(samp, F)
    print(f"  r={r}: n={len(samp):8d}  KS D={ks.statistic:.6f}  "
          f"p={ks.pvalue:.4f}")
    RES[f"ks_r{r}"] = dict(n=int(len(samp)), D=float(ks.statistic),
                           p=float(ks.pvalue))

# ---- overall KS vs 8x(1-x^2)^3 ------------------------------------
ks_tot = stats.kstest(M, total_cdf)
mean = M.mean()
se = M.std(ddof=1) / np.sqrt(N)
target_mean = 128 / 315
z = (mean - target_mean) / se
print(f"\noverall: KS D={ks_tot.statistic:.6f} p={ks_tot.pvalue:.4f}   "
      f"mean={mean:.6f}+/-{se:.6f} vs 128/315={target_mean:.6f} "
      f"(z={z:+.2f})")
RES["overall"] = dict(D=float(ks_tot.statistic), p=float(ks_tot.pvalue),
                      mean=float(mean), se=float(se), z=float(z))

# ---- sub-shape sigma-exchangeability test -------------------------
# theory: within a group r, every cycle type has probability
# proportional to its number of permutations, and the SAME conditional
# M law.  Both tested here (the document never tested this
# distributionally).
perm_frac = {10: (1, 1),
             20: (1, 2), 21: (1, 2),
             30: (1, 6), 31: (3, 6), 32: (2, 6),
             40: (1, 24), 41: (6, 24), 42: (3, 24), 43: (8, 24),
             44: (6, 24)}
names = {10: "(1)", 20: "(1,1)", 21: "(2)", 30: "(1,1,1)", 31: "(2,1)",
         32: "(3)", 40: "(1^4)", 41: "(2,1,1)", 42: "(2,2)", 43: "(3,1)",
         44: "(4)"}
print("\nsub-shape (cycle-type) tests within each r_on group:")
worst_p = 1.0
for r in (2, 3, 4):
    grp = M[r_on == r]
    ngrp = len(grp)
    F = conditional_cdf(r)
    for code, (num, den) in perm_frac.items():
        if code // 10 != r:
            continue
        s = M[sub == code]
        pfrac = num / den
        zc = (len(s) - ngrp * pfrac) / np.sqrt(ngrp * pfrac * (1 - pfrac))
        ks = stats.kstest(s, F)
        worst_p = min(worst_p, ks.pvalue)
        print(f"  r={r} ct={names[code]:8s}: n={len(s):7d} "
              f"(frac z={zc:+.2f} vs {num}/{den})   KS vs group law: "
              f"D={ks.statistic:.5f} p={ks.pvalue:.4f}")
        RES[f"sub_{code}"] = dict(n=int(len(s)), z=float(zc),
                                  ks_p=float(ks.pvalue))
        assert abs(zc) < 4.0

print(f"\nworst sub-shape KS p = {worst_p:.4f}  "
      f"({sum(1 for k in RES if k.startswith('sub_'))} tests)")

with open("indep_continuum_mc_perr_k4_results.json", "w") as fh:
    json.dump(RES, fh, indent=1)
print("results written to indep_continuum_mc_perr_k4_results.json")
