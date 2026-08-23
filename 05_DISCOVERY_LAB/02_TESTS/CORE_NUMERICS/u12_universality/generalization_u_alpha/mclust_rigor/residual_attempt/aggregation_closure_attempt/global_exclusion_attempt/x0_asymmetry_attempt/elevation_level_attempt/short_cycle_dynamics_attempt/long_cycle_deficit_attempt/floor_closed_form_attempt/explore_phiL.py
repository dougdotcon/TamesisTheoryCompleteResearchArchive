import sys, os
sys.path.insert(0, "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt")
import numpy as np
import sc_engine as E
import sc_formula as F

# THROWAWAY exploratory seed (not for final report), reserved-throwaway range for front (b)
ss = np.random.SeedSequence(20260833900)

n = 65536
c = 1000
b = 1
N = 300  # instances, but use ALL n points per instance as x0 candidates (exchangeability)

bin_edges = np.array([1, 50, 200, 500, 1000, 2000, 4000, 8000, 16384, 32768, 65536])
counts = np.zeros(len(bin_edges)-1)
cyclic = np.zeros(len(bin_edges)-1)

children = ss.spawn(N)
for k in range(N):
    rng = np.random.default_rng(children[k])
    pi = E.build_pi(n, rng)
    seed_mask = E.build_seeds(n, c, rng)
    R_mask = E.build_R_mask(n, b, pi, seed_mask)
    f = E.build_f(n, pi, R_mask, rng)
    cyc_mask = E.cyclic_mask_peeling(f)
    clens = E.pi_cycle_lengths(pi)

    notseed = ~seed_mask
    L_all = clens[notseed]
    cyc_all = cyc_mask[notseed]
    idx = np.digitize(L_all, bin_edges) - 1  # bin index for each point
    for bi in range(len(bin_edges)-1):
        sel = idx == bi
        counts[bi] += sel.sum()
        cyclic[bi] += cyc_all[sel].sum()

print("bin edges:", bin_edges.tolist())
for bi in range(len(bin_edges)-1):
    if counts[bi] > 0:
        phat = cyclic[bi]/counts[bi]
        se = np.sqrt(phat*(1-phat)/counts[bi])
        mid_t = 0.5*(bin_edges[bi]+bin_edges[bi+1])/n
        pred_pointwise = np.exp(-c*mid_t**2)
        print(f"  L in [{bin_edges[bi]},{bin_edges[bi+1]}): n_pts={int(counts[bi])} phat={phat:.5f}+-{se:.5f}  pred_e^-c*t^2(mid)={pred_pointwise:.5f}")
    else:
        print(f"  L in [{bin_edges[bi]},{bin_edges[bi+1]}): n_pts=0")

print("\nphi_U(c) =", F.phi_U(c))
