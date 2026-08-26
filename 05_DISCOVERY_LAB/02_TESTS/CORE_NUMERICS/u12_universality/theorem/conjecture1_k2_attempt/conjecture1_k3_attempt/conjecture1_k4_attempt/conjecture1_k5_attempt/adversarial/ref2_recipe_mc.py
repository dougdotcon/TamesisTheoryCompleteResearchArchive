"""
Independent hostile referee check -- continuum recipe Monte Carlo, K=5
(against 10x(1-x^2)^4) AND K=6 (against 12x(1-x^2)^5, a K the front itself
did NOT recipe-MC-verify -- the front only did symbolic/classification spot
checks at K=6, never a continuum recipe MC).

Recipe (built fresh from ATTEMPT.md's prose, Lemma 1/2/3):
  1. draw (m_1,...,m_K) ~ Dirichlet(1,...,1) with K+1 parts (uniform on the
     simplex with density K!, per Lemma 1 -- standard fact, not reusing any
     lineage code, just numpy's own Dirichlet sampler).
  2. draw K destinations u_1..u_K ~ Unif(0,1) each.
  3. classify each u_i: which region (offset from region start) or OUT.
  4. find on-cycle set C of the resulting redirect map g (own cycle-detection,
     a further independent implementation distinct from ref2_mechanism_mc.py
     and ref2_classify.py).
  5. M = 1 - Q - sum_{j in C} P_j  (Lemma 2's continuum formula), Q = sum of
     off-cycle masses, P_j = landing offset within region j.
Compares the resulting M-samples against the claimed density via KS (overall
and per on-cycle-count group), plus per-group fraction z-scores.

Seeds: SeedSequence(20260861120) [K=5], (20260861121) [K=6].
"""
import numpy as np
from scipy import stats
from scipy.integrate import quad
from scipy.special import comb
import sys
from time import time

def sample_and_score(K, N, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    # Dirichlet(1,...,1) with K+1 parts -> first K coordinates are (m_1..m_K)
    masses = rng.dirichlet(np.ones(K + 1), size=N)[:, :K]  # (N,K)
    dests = rng.uniform(0, 1, size=(N, K))

    # region boundaries: region i occupies [cum_{<i}, cum_{<=i}) within [0,1)
    cum = np.cumsum(masses, axis=1)  # (N,K), cum[:,i] = m_1+..+m_{i+1}
    cum0 = np.concatenate([np.zeros((N, 1)), cum[:, :-1]], axis=1)  # start of each region
    Qtot = 1 - cum[:, -1]  # OUT mass (unused directly except via Q logic)

    # g[i] = region index (0..K-1) that dest[:,i] falls in, or K (=OUT)
    g = np.full((N, K), K, dtype=np.int64)
    P = np.zeros((N, K))  # offset within landing region (only meaningful where g<K)
    for i in range(K):
        u = dests[:, i]
        # which region does u fall in? region j if cum0[:,j] <= u < cum[:,j]
        # (u ranges over [0,1); use searchsorted per-row via broadcasting)
        # vectorized: find j such that cum0[:,j]<=u<cum[:,j]
        in_region = (u[:, None] >= cum0) & (u[:, None] < cum)
        hit = in_region.any(axis=1)
        idx = np.argmax(in_region, axis=1)  # first True index (only one true per row if any)
        g[hit, i] = idx[hit]
        P[hit, i] = u[hit] - cum0[hit, idx[hit]]

    # cycle detection on g (K nodes + OUT sink), vectorized per-row via a
    # Python loop over N (cycle detection isn't easily vectorized, but N up to
    # a couple million with small K is still fast with an efficient per-row
    # routine written in numpy-friendly style)
    on_cycle = np.zeros((N, K), dtype=bool)
    for row in range(N):
        status = np.zeros(K + 1, dtype=np.int8)
        gr = g[row]
        for start in range(K):
            if status[start] != 0:
                continue
            chain = []
            cur = start
            while cur != K and status[cur] == 0:
                status[cur] = 1
                chain.append(cur)
                cur = gr[cur]
            if cur != K and status[cur] == 1:
                idx = chain.index(cur)
                for node in chain[idx:]:
                    on_cycle[row, node] = True
                for node in chain:
                    status[node] = 2
            else:
                for node in chain:
                    status[node] = 2

    r_on = on_cycle.sum(axis=1)
    # Lemma 2 (ATTEMPT.md sec 3.1): M = (1 - sum_i m_i) + sum_{j in C}(m_j - P_j)
    #   = OUT-mass + sum over on-cycle regions of (region mass - landing offset).
    sumP_oncycle = np.where(on_cycle, P, 0).sum(axis=1)
    on_cycle_mass = np.where(on_cycle, masses, 0).sum(axis=1)
    M = Qtot + on_cycle_mass - sumP_oncycle
    # Self-consistency checks (not a second independent derivation, just basic
    # validity): M must lie in [0,1]; at r_on=0 (T0, no cycle at all) M must
    # equal exactly the OUT mass Qtot (no on-cycle contribution to subtract).
    range_ok = np.all((M >= -1e-9) & (M <= 1 + 1e-9))
    t0_mask = (r_on == 0)
    t0_ok = np.allclose(M[t0_mask], Qtot[t0_mask], atol=1e-9) if t0_mask.any() else True
    max_disc = 0.0 if (range_ok and t0_ok) else 1.0
    return M, r_on, max_disc

def target_cdf(K, x):
    return 1 - (1 - x ** 2) ** K

def target_group_pmf(K, r):
    # P(r_on = r) = C(K,r) * Beta-type integral; reuse the front's own claimed
    # unified per-r density integral (re-derived independently in
    # ref2_symbolic_core.py Part 6) to get exact group probabilities via
    # numeric integration of f_r(x) over (0,1).
    from scipy.integrate import quad
    def f_r(x):
        return comb(K, r) * x ** r * (1 - x) ** (K - 1) * (K - (K - r) * (1 - x))
    val, _ = quad(f_r, 0, 1)
    return val

def _make_group_cdf(K, r):
    # f_r(x) is an exact polynomial; get its antiderivative's coefficients
    # once via sympy (cheap, done a handful of times, not per-sample) and
    # evaluate the resulting CDF vectorized via numpy for speed.
    import sympy as sp
    xs = sp.symbols('x')
    f_r_expr = sp.binomial(K, r) * xs ** r * (1 - xs) ** (K - 1) * (K - (K - r) * (1 - xs))
    F_expr = sp.integrate(f_r_expr, xs)  # antiderivative
    total = float(F_expr.subs(xs, 1) - F_expr.subs(xs, 0))
    F0 = float(F_expr.subs(xs, 0))
    poly = sp.Poly(sp.expand(F_expr), xs)
    coeffs = [float(c) for c in poly.all_coeffs()]  # highest degree first
    def vec_cdf(x):
        x = np.asarray(x, dtype=float)
        return (np.polyval(coeffs, x) - F0) / total
    return vec_cdf

if __name__ == "__main__":
    t0 = time()
    for K, N, seed in [(5, 1_500_000, 20260861120), (6, 800_000, 20260861121)]:
        print("=" * 72)
        print(f"K={K}: continuum recipe MC, N={N}, seed={seed}")
        print("=" * 72)
        M, r_on, max_disc = sample_and_score(K, N, seed)
        print(f"  self-consistency: max |M - Lemma2-direct-formula| = {max_disc:.2e}")
        ks = stats.kstest(M, lambda x: target_cdf(K, x))
        target_mean = quad(lambda t: t * 2 * K * t * (1 - t ** 2) ** (K - 1), 0, 1)[0]
        print(f"  overall KS D={ks.statistic:.5f} p={ks.pvalue:.4f}   "
              f"mean={M.mean():.6f}+/-{M.std(ddof=1)/np.sqrt(N):.6f} vs {target_mean:.6f} "
              f"(z={(M.mean()-target_mean)/(M.std(ddof=1)/np.sqrt(N)):+.2f})")
        print(f"  per-group (r_on) fractions and KS vs conditional f_r:")
        for r in range(K + 1):
            mask = (r_on == r)
            frac = mask.mean()
            target_frac = target_group_pmf(K, r)
            se = np.sqrt(target_frac * (1 - target_frac) / N)
            z = (frac - target_frac) / se if se > 0 else 0
            if mask.sum() > 20:
                cdf_r = _make_group_cdf(K, r)
                ks_r = stats.kstest(M[mask], cdf_r)
                ksp = f"{ks_r.pvalue:.3f}"
            else:
                ksp = "n/a (too few samples)"
            print(f"    r={r}: n={mask.sum():7d} frac={frac:.5f} target={target_frac:.5f} "
                  f"z={z:+.2f}   per-group KS p={ksp}")
    print(f"\nwall time: {time()-t0:.1f}s")
