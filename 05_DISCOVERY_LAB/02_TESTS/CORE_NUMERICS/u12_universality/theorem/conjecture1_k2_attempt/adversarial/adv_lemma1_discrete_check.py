"""
ADVERSARIAL REFEREE — independent check of Lemma 1 (Step A, ATTEMPT.md sec 2.2).

Goal: test the claim that (m1, m2) -- defined via a genuinely DISCRETE, finite-n
uniform random permutation model (NOT the continuum PD(1)/stick-breaking machinery
the front's own scripts use) -- converges to the uniform law on the triangle
T = {m1,m2>0, m1+m2<1} with density 2, as claimed by Lemma 1.

This is built entirely from scratch: it does NOT import or read any of the front's
scripts (derive_density_symbolic.py, derive_density_full.py, r2_k1_sanity.py,
mc_step_a_check.py, discrete_k2_full_distribution_mc.py, mc_recipe_check.py,
bonus_limitsim_crosscheck.py). It uses the DISCRETE permutation ensemble
(Definition 1/4 of THEOREM.md) directly, which is a genuinely different generative
route than the continuum PD(1)-partition-plus-stick-breaking route that a
symbolic/continuum check would use -- so a good match here is evidence that isn't
just "the same citation checking itself."

Method: for each trial, draw a fresh uniform random permutation pi of [n]. Fix two
distinct labels x1, x2 (WLOG by exchangeability -- but we also randomize the pair
across trials as an extra robustness check). Trace forward from x1 to find its
cycle C1 (length L1); check whether x2 in C1.
  - If yes (same cycle): let A = forward steps from x1 to x2. m1 = L1 - A (mass
    reaching x1 first), m2 = A (mass reaching x2 first).
  - If no: trace x2's own cycle C2 (length L2). m1 = L1, m2 = L2.
Normalize (m1/n, m2/n) and accumulate statistics: compare to the exact moments of
Uniform(T) (a symmetric Dirichlet(1,1,1) marginal pair) and to the two 1-D KS
targets:
  - marginal of m1 alone: density 2(1-x), CDF F(x) = 2x - x^2
  - marginal of L := m1+m2: density 2*ell, CDF F(ell) = ell^2

Exact target moments under Unif(T) (Dirichlet(1,1,1)):
  E[m1] = E[m2] = 1/3
  E[m1^2] = E[m2^2] = 1/6
  E[m1*m2] = 1/12
  Cov(m1,m2) = -1/36
"""
import numpy as np
from scipy import stats
import json
import time

def trace_cycle(pi, start):
    """Return (list of nodes in forward order starting at start, dict node->index)."""
    seq = [start]
    pos = {start: 0}
    cur = pi[start]
    while cur != start:
        seq.append(cur)
        pos[cur] = len(seq) - 1
        cur = pi[cur]
    return seq, pos

def run_trials(n, n_trials, seed):
    rng = np.random.default_rng(seed)
    m1s = np.empty(n_trials)
    m2s = np.empty(n_trials)
    same_block_count = 0
    for t in range(n_trials):
        pi = rng.permutation(n)
        # randomize which two distinct labels play the role of x1, x2 (robustness;
        # WLOG-valid by exchangeability of a uniform random permutation, but we
        # do NOT rely on that argument alone -- we test it empirically too)
        x1, x2 = rng.choice(n, size=2, replace=False)
        seq, pos = trace_cycle(pi, x1)
        L1 = len(seq)
        if x2 in pos:
            same_block_count += 1
            A = pos[x2]           # forward steps x1 -> x2
            m1 = L1 - A
            m2 = A
        else:
            seq2, pos2 = trace_cycle(pi, x2)
            L2 = len(seq2)
            m1 = L1
            m2 = L2
        m1s[t] = m1 / n
        m2s[t] = m2 / n
    return m1s, m2s, same_block_count / n_trials


def main():
    results = {}
    # Use two different n to see convergence trend (finite-n discretization bias
    # should shrink as n grows). Seeds from the referee's reserved block.
    configs = [
        (300, 60000, 20260836001),
        (1000, 40000, 20260836002),
        (3000, 20000, 20260836003),
    ]
    for n, n_trials, seed in configs:
        t0 = time.time()
        m1s, m2s, p_same = run_trials(n, n_trials, seed)
        L = m1s + m2s
        dt = time.time() - t0

        # exact targets
        target = dict(E_m1=1/3, E_m2=1/3, E_m1sq=1/6, E_m2sq=1/6, E_m1m2=1/12,
                      Cov=-1/36, P_same_block=None)  # P(same block) has no fixed
        # target for P(same block): under Lemma 1's own case split,
        # P(Same=1) = E_ell[ell] = 1/2 (since L1~Unif(0,1) and P(Same|L1=ell)=ell)
        target['P_same_block'] = 0.5

        Em1 = m1s.mean(); Em2 = m2s.mean()
        Em1sq = (m1s**2).mean(); Em2sq = (m2s**2).mean()
        Em1m2 = (m1s*m2s).mean()
        cov = Em1m2 - Em1*Em2
        se_m1 = m1s.std(ddof=1) / np.sqrt(n_trials)
        se_m1sq = (m1s**2).std(ddof=1) / np.sqrt(n_trials)
        se_m1m2 = (m1s*m2s).std(ddof=1) / np.sqrt(n_trials)

        z_Em1 = (Em1 - target['E_m1']) / se_m1
        z_Em1sq = (Em1sq - target['E_m1sq']) / se_m1sq
        z_Em1m2 = (Em1m2 - target['E_m1m2']) / se_m1m2

        se_psame = np.sqrt(p_same*(1-p_same)/n_trials)
        z_psame = (p_same - 0.5) / se_psame

        # KS test: marginal of m1 vs CDF F(x)=2x-x^2 on (0,1)
        def cdf_m1(x):
            return 2*x - x**2
        ks_m1 = stats.kstest(m1s, cdf_m1)

        # KS test: marginal of L=m1+m2 vs CDF F(ell)=ell^2
        def cdf_L(x):
            return x**2
        ks_L = stats.kstest(L, cdf_L)

        # exchangeability check: m1 vs m2 should have identical marginal law
        # (2-sample KS)
        ks_exch = stats.ks_2samp(m1s, m2s)

        results[f"n={n}"] = dict(
            n=n, n_trials=n_trials, seed=seed, time_sec=round(dt, 2),
            P_same_block=p_same, z_P_same=z_psame,
            E_m1=Em1, z_E_m1=z_Em1,
            E_m1sq=Em1sq, z_E_m1sq=z_Em1sq,
            E_m1m2=Em1m2, z_E_m1m2=z_Em1m2,
            Cov_m1m2=cov, Cov_target=-1/36,
            KS_m1_vs_2xminusx2=dict(D=ks_m1.statistic, p=ks_m1.pvalue),
            KS_L_vs_ell2=dict(D=ks_L.statistic, p=ks_L.pvalue),
            KS_exchangeability_m1_vs_m2=dict(D=ks_exch.statistic, p=ks_exch.pvalue),
        )
        print(f"--- n={n}, trials={n_trials} (time {dt:.1f}s) ---")
        for k, v in results[f"n={n}"].items():
            print(f"  {k}: {v}")
        print()

    with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv_lemma1_discrete_check.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

if __name__ == "__main__":
    main()
